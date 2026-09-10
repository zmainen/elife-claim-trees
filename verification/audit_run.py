#!/usr/bin/env python3
"""Run a verification script under observation, and record what it actually did.

Only one of the nine verification scripts was ever audited, and auditing it found two
failures that no amount of reading would have caught:

  * a claim recorded `verified` while the function named in its record raised
    `shapes (4,4) and (5,5) not aligned` -- the verdict had been narrated, not observed;
  * a reproduction record naming `fMRI - Choices_singleTrialData.csv` while the code opened
    `Behav - Choices_singleTrialData.csv`.

Both were found by making the script report every path it opened and every value it computed.
That was done for Gaedeke by editing the script to call `used()` at each open. Doing the same
to eight more scripts would mean eight sets of hand-edits, each an opportunity to annotate a
path the code does not take -- which is the very failure being audited.

So this observes from outside instead. It patches `open` and the common loaders, executes the
script in-process, and reads its `ROWS` list afterwards. Nothing is taken from the script's
own account of itself: the file list comes from the file system calls, the results come from
the list the printed table is built from, and an exception is recorded whether or not the
script caught it.

What it emits, beside the script it ran:

  verification/<paper>/provenance.json    files opened, results produced, exceptions raised

Usage:
  python3 verification/audit_run.py <paper-slug> [-- script args]
  python3 verification/audit_run.py --all
  python3 verification/audit_run.py --all --timeout 900
"""

from __future__ import annotations

import argparse
import builtins
import hashlib
import io
import json
import os
import subprocess
import sys
import traceback
from datetime import datetime, timezone

# Captured before anything is patched, so the harness can always read files itself
# even while `builtins.open` is being observed.
REAL_OPEN = builtins.open

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Paths every run touches that say nothing about which data a claim rests on.
NOISE = ("/site-packages/", "/lib/python", "/dist-packages/", "__pycache__",
         "/proc/", "/sys/", "/dev/", "/etc/", ".pyc",
         # An interpreter reads these on any run -- a timezone table and the OS version
         # plist appeared in the first audit beside the actual NIfTI maps, which makes a
         # provenance record harder to read and, worse, harder to trust.
         "/System/", "/usr/share/", "/Library/Frameworks/", "/var/folders/")


def interesting(path: str) -> bool:
    p = str(path)
    return not any(n in p for n in NOISE)


class Observer:
    """Records every file the script opens for reading, with size and content hash."""

    def __init__(self):
        self.opened: dict[str, dict] = {}
        self.errors: list[dict] = []

    def note(self, path, mode="r"):
        try:
            p = os.path.abspath(str(path))
        except Exception:
            return
        if not interesting(p) or "w" in str(mode) or "a" in str(mode):
            return
        if p in self.opened:
            return
        rec = {"path": self._short(p)}
        try:
            with REAL_OPEN(p, "rb") as fh:
                b = fh.read()
            rec["bytes"] = len(b)
            rec["sha256_12"] = hashlib.sha256(b).hexdigest()[:12]
        except Exception as e:                                        # noqa: BLE001
            rec["error"] = f"{type(e).__name__}: {e}"
        self.opened[p] = rec

    @staticmethod
    def _short(p):
        return os.path.relpath(p, ROOT) if p.startswith(ROOT) else p


def install(obs: Observer):
    """Patch the entry points a verification script uses to read data."""
    real_open = builtins.open

    def watched_open(file, mode="r", *a, **kw):
        obs.note(file, mode)
        return real_open(file, mode, *a, **kw)

    builtins.open = watched_open
    io.open = watched_open
    undo = [lambda: (setattr(builtins, "open", real_open), setattr(io, "open", real_open))]

    # pandas and numpy reach the file system through C in some paths, so wrap the readers
    # themselves rather than relying on `open` being called.
    def wrap(mod, name, argno=0):
        fn = getattr(mod, name, None)
        if fn is None:
            return

        def wrapped(*a, **kw):
            if len(a) > argno:
                obs.note(a[argno])
            return fn(*a, **kw)

        setattr(mod, name, wrapped)
        undo.append(lambda: setattr(mod, name, fn))

    for modname, fns in (("pandas", ("read_csv", "read_excel", "read_table", "read_json",
                                     "read_parquet", "read_pickle")),
                         ("numpy", ("load", "loadtxt", "genfromtxt")),
                         ("nibabel", ("load",)),
                         ("scipy.io", ("loadmat",))):
        try:
            mod = __import__(modname, fromlist=["x"])
        except Exception:                                             # noqa: BLE001
            continue
        for fn in fns:
            wrap(mod, fn)

    return lambda: [u() for u in reversed(undo)]


def third_party_imports(script):
    """Top-level modules the script imports that are not in the standard library."""
    import ast
    try:
        with REAL_OPEN(script, encoding="utf-8") as fh:
            tree = ast.parse(fh.read())
    except (OSError, SyntaxError) as e:
        # Never return "nothing missing" because the check itself broke -- that
        # reads as a clean environment and is how this function first shipped.
        raise RuntimeError(f"could not read {script} to find its imports: {e}") from e
    mods = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            mods |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module and not n.level:
            mods.add(n.module.split(".")[0])
    return sorted(m for m in mods if m not in sys.stdlib_module_names)


def missing_dependencies(script):
    """Which of those are absent here.

    A missing dependency does not always stop a script. meijer-2025-serotonin-additive-r1
    catches the ImportError and records `WARN -- statsmodels/sklearn not installed`, so the
    claim comes out partially verified and nothing says the environment is why. A verdict
    produced by an incomplete environment is not the verdict the script would give, and the
    provenance has to say so or the audit inherits the same blind spot it is checking for.
    """
    import importlib.util
    out = []
    for m in third_party_imports(script):
        try:
            if importlib.util.find_spec(m) is None:
                out.append(m)
        except (ImportError, ValueError, ModuleNotFoundError):
            out.append(m)
    return out


def run(paper: str, argv: list[str], timeout: int | None):
    script = os.path.join(HERE, paper, "verify.py")
    if not os.path.isfile(script):
        return {"paper": paper, "error": "no verify.py"}

    obs = Observer()
    prov = {
        "paper": paper,
        "script": os.path.relpath(script, ROOT),
        "argv": argv,
        "observed_by": "verification/audit_run.py",
        "recorded": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "interpreter": {"executable": sys.executable,
                        "version": sys.version.split()[0]},
    }
    missing = missing_dependencies(script)
    if missing:
        prov["missing_dependencies"] = missing
        print(f"  [audit] MISSING: {', '.join(missing)} — this run is degraded; any verdict "
              f"below may differ from one produced with the full environment "
              f"(see verification/requirements.txt)", flush=True)

    out = io.StringIO()
    real_stdout, real_stderr = sys.stdout, sys.stderr
    real_argv, real_cwd = sys.argv, os.getcwd()
    uninstall = install(obs)

    # The namespace is created here rather than by `runpy`, because every one of these
    # scripts ends in `sys.exit(...)` and runpy discards a module's globals when it exits
    # that way -- taking ROWS with it, so the audit saw a script that printed a table of
    # results and reported "no results". Holding the dict means the results survive the exit
    # that produced them.
    mod_globals = {"__name__": "__main__", "__file__": script, "__builtins__": builtins}
    try:
        sys.argv = ["verify.py"] + argv
        sys.stdout = sys.stderr = _Tee(out, real_stdout)
        os.chdir(os.path.dirname(script))
        with REAL_OPEN(script, "rb") as fh:
            code = compile(fh.read(), script, "exec")
        exec(code, mod_globals)                                       # noqa: S102
        prov["exit"] = "completed"
    except SystemExit as e:
        prov["exit"] = f"SystemExit({e.code})"
    except BaseException as e:                                        # noqa: BLE001
        prov["exit"] = "raised"
        prov["exception"] = {"type": type(e).__name__, "message": str(e),
                             "traceback": traceback.format_exc()[-2500:]}
    finally:
        uninstall()
        sys.stdout, sys.stderr = real_stdout, real_stderr
        sys.argv = real_argv
        os.chdir(real_cwd)

    # The results the printed table is built from, read out of the module rather than
    # scraped from its output.
    rows = mod_globals.get("ROWS") if isinstance(mod_globals, dict) else None
    prov["results"] = [
        {"claim": r[0], "paper_value": str(r[1]), "reproduced_value": str(r[2]),
         "status": str(r[3])}
        for r in (rows or []) if isinstance(r, (list, tuple)) and len(r) >= 4
    ]
    if rows is None:
        prov["results_note"] = ("no ROWS list found in the module — results could not be "
                                "read; the script may have exited before defining it")

    prov["opened"] = sorted(obs.opened.values(), key=lambda r: r["path"])
    prov["stdout_tail"] = out.getvalue()[-4000:]

    repo = mod_globals.get("REPO_DIR") if isinstance(mod_globals, dict) else None
    if repo and os.path.isdir(str(repo)):
        try:
            prov["data_commit"] = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, timeout=30).stdout.strip() or None
        except Exception:                                             # noqa: BLE001
            prov["data_commit"] = None

    dest = os.path.join(HERE, paper, "provenance.json")
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(prov, fh, indent=2)
        fh.write("\n")
    return prov


class _Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for st in self.streams:
            try:
                st.write(s)
            except Exception:                                         # noqa: BLE001
                pass
        return len(s)

    def flush(self):
        for st in self.streams:
            try:
                st.flush()
            except Exception:                                         # noqa: BLE001
                pass


def provenance_of(paper):
    p = os.path.join(HERE, paper, "provenance.json")
    if not os.path.isfile(p):
        return None
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:                                                 # noqa: BLE001
        return None


def papers_with_scripts():
    return sorted(d for d in os.listdir(HERE)
                  if os.path.isfile(os.path.join(HERE, d, "verify.py")))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--timeout", type=int, default=None)
    ap.add_argument("--single", action="store_true",
                    help="internal: audit one script in this interpreter")
    ap.add_argument("args", nargs="*", help="arguments passed through to verify.py")
    a = ap.parse_args()

    papers = papers_with_scripts() if a.all else ([a.paper] if a.paper else [])
    if not papers:
        ap.error("give a paper slug or --all")

    # `--single` is the child half of the subprocess split below. Observing a script means
    # patching `open` and the loaders in the same interpreter that runs it, so several
    # scripts audited in one process share those patches, `sys.modules`, and any global a
    # library was left holding. One script could then change the numbers another produces --
    # which is precisely the class of error this tool exists to catch, so it must not be able
    # to commit it. Each audit gets a clean interpreter.
    if a.single:
        prov = run(papers[0], a.args, a.timeout)
        return 0 if not prov.get("exception") else 0

    summary = []
    for p in papers:
        print(f"\n{'=' * 72}\n  {p}\n{'=' * 72}", flush=True)
        cmd = [sys.executable, os.path.abspath(__file__), "--single", p]
        if a.args:
            cmd += a.args
        try:
            subprocess.run(cmd, timeout=a.timeout, check=False)
        except subprocess.TimeoutExpired:
            print(f"  [audit] timed out after {a.timeout}s", flush=True)
            dest = os.path.join(HERE, p, "provenance.json")
            with open(dest, "w", encoding="utf-8") as fh:
                json.dump({"paper": p, "exit": "timeout",
                           "exception": {"type": "Timeout",
                                         "message": f"killed after {a.timeout}s"},
                           "results": [], "opened": []}, fh, indent=2)
        prov = provenance_of(p) or {"exit": "no provenance written"}
        summary.append((p, prov.get("exit"), len(prov.get("opened", [])),
                        prov.get("results", []), prov.get("exception")))

    print(f"\n{'=' * 72}\n  AUDIT SUMMARY\n{'=' * 72}")
    for p, exit_, nfiles, results, exc in summary:
        counts = {}
        for r in results:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
        tally = " ".join(f"{v}×{k}" for k, v in sorted(counts.items())) or "no results"
        print(f"  {p:38} {exit_ or '?':16} {nfiles:>3} file(s)  {tally}")
        if exc:
            print(f"      raised {exc['type']}: {exc['message'][:90]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
