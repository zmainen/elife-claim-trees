#!/usr/bin/env python3
"""The pipeline: layer declarations, the run ledger, and computed state.

A layer runs against a paper and produces a version. Whether that version is still good is
not a matter of memory: the run recorded what it read, by path and content hash, so the
question "is this current" is asked of the files rather than of a person.

The repository already answered this question three times, locally and incompatibly:

    runs/<paper>/manifest.json          prompt path + hash, model, output + hash
    verification/<paper>/provenance.json  argv, interpreter, data commit, files opened
    mappings/<paper>.json               a sha per verdict, discarded on mismatch

plus byte-stable exports, where `git diff` is the check. Four mechanisms, one problem. This
module is the fourth answer, and the point of it is that it is the only one: every layer
appends to one ledger in one shape, so staleness and propagation are computed once.

    python3 scripts/pipeline.py graph            the DAG, from the declaration
    python3 scripts/pipeline.py backfill         write ledgers from what already exists
    python3 scripts/pipeline.py state            the paper x layer matrix
    python3 scripts/pipeline.py state --json     the same, for the site
    python3 scripts/pipeline.py run   <paper> <layer>   run it, and its unmet dependencies
    python3 scripts/pipeline.py run   <paper> <layer> --answer FILE   record an answer made elsewhere
    python3 scripts/pipeline.py approve <paper> <layer> --by NAME   record that someone read it

Usage as a library: `load()`, `state()`.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
from collections import OrderedDict
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required:  pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECL = os.path.join(ROOT, "pipeline", "layers.yaml")

# States a cell can be in. Ordered worst-first for reporting.
OPEN, STALE, ABSENT, BLOCKED, NA, CURRENT = (
    "open", "stale", "absent", "blocked", "n/a", "current")


# ── declaration ───────────────────────────────────────────────────────────────

def load(path: str = DECL) -> dict:
    """Read the declaration and index it by id, checking the graph is well formed."""
    with open(path, encoding="utf-8") as fh:
        decl = yaml.safe_load(fh)
    layers = OrderedDict((l["id"], l) for l in decl["layers"])

    for lid, l in layers.items():
        for dep in l.get("needs") or []:
            if dep not in layers:
                raise SystemExit(f"{lid}: needs unknown layer {dep!r}")
        if l.get("group") and l["group"] not in (decl.get("groups") or {}):
            raise SystemExit(f"{lid}: unknown group {l['group']!r}")
    _toposort(layers)                      # raises on a cycle
    decl["by_id"] = layers
    return decl


def _toposort(layers: dict) -> list[str]:
    """Dependency order. A cycle here would make staleness undecidable."""
    seen, order, stack = set(), [], set()

    def visit(lid):
        if lid in seen:
            return
        if lid in stack:
            raise SystemExit(f"cycle in the pipeline at {lid!r}")
        stack.add(lid)
        for dep in layers[lid].get("needs") or []:
            visit(dep)
        stack.discard(lid)
        seen.add(lid)
        order.append(lid)

    for lid in layers:
        visit(lid)
    return order


def papers(decl_path: str = os.path.join(ROOT, "corpus.yaml")) -> list[str]:
    """Papers the site publishes, in corpus order."""
    with open(decl_path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    out = []
    for _, c in (data.get("corpora") or {}).items():
        if c.get("public") and c.get("in_site_corpus", True):
            out += c.get("papers") or []
    return sorted(out)


# ── paths and hashes ──────────────────────────────────────────────────────────

def expand(patterns, paper: str | None, doi: str | None = None) -> list[str]:
    """Resolve a layer's declared paths for one paper, globbing where they glob."""
    out = []
    for pat in (patterns or []):
        pat = pat.replace("{paper}", paper or "").replace("{doi}", doi or "")
        hits = sorted(glob.glob(os.path.join(ROOT, pat)))
        out += [os.path.relpath(h, ROOT) for h in hits] if hits else [pat]
    return out


def digest(rel: str) -> str | None:
    """Content hash of one file, or None when it does not exist.

    A directory of claim files hashes as the sorted concatenation of its members, so adding
    a claim changes the tree's hash — which is the whole point: it is what makes every
    export downstream of it stale.
    """
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return None
    h = hashlib.sha256()
    if os.path.isdir(p):
        for f in sorted(glob.glob(os.path.join(p, "**", "*"), recursive=True)):
            if os.path.isfile(f):
                h.update(os.path.relpath(f, p).encode())
                h.update(open(f, "rb").read())
    else:
        h.update(open(p, "rb").read())
    return h.hexdigest()[:12]


GLOB_CHARS = "*?["


def patterns_of(layer: dict, by_id: dict, paper: str | None, doi=None) -> list[str]:
    """The same inputs as `inputs_of`, unexpanded — the patterns themselves."""
    out = []
    for dep in layer.get("needs") or []:
        out += (by_id[dep].get("produces") or [])
    out += (layer.get("reads") or [])
    return [p.replace("{paper}", paper or "").replace("{doi}", doi or "") for p in out]


def manifest(pat: str) -> str | None:
    """Which files a pattern matches right now — their names, not their contents.

    `digest` already hashes a *directory* as the sorted concatenation of its members, so that
    adding a file to one moves it. Nothing recorded a directory: `expand` resolves
    `claims/{paper}/*.md` into the files that existed at that moment, and staleness then
    re-hashes exactly those paths. A file that appeared afterwards is on nobody's list, so
    nothing looks at it.

    Adding a claim file is precisely that edit, and it is how a gap gets closed — so the one
    change the corpus most needs to notice was the one change it could not. This is the
    missing half: contents per file in `in`, membership per pattern here.
    """
    if not any(ch in pat for ch in GLOB_CHARS):
        return None
    hits = sorted(glob.glob(os.path.join(ROOT, pat)))
    names = [os.path.relpath(h, ROOT) for h in hits]
    return hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()[:12]


def input_sets(layer: dict, by_id: dict, paper: str | None, doi=None) -> list[dict]:
    """Membership fingerprints for every input pattern of this layer that globs."""
    out = []
    for pat in patterns_of(layer, by_id, paper, doi):
        sha = manifest(pat)
        if sha:
            out.append({"pat": pat, "sha": sha})
    return out


def inputs_of(layer: dict, by_id: dict, paper: str | None, doi=None) -> list[str]:
    """Every path a run of this layer reads: its dependencies' outputs, plus `reads`."""
    out = []
    for dep in layer.get("needs") or []:
        out += expand(by_id[dep].get("produces"), paper, doi)
    out += expand(layer.get("reads"), paper, doi)
    return out


# ── the ledger ────────────────────────────────────────────────────────────────

def ledger_path(paper: str) -> str:
    return os.path.join(ROOT, "runs", paper, "ledger.jsonl")


def read_ledger(paper: str) -> list[dict]:
    p = ledger_path(paper)
    if not os.path.isfile(p):
        return []
    out = []
    with open(p, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def append(paper: str, record: dict) -> None:
    """Append one run record. The ledger is append-only: a version is not edited."""
    p = ledger_path(paper)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")


def _latest(entries: list[dict], layer_id: str) -> dict | None:
    runs = [e for e in entries if e.get("layer") == layer_id]
    if not runs:
        return None
    return max(runs, key=lambda e: (e.get("v", 0), e.get("ran", "")))


def _by_from_output(layer: dict, outs: list[str], paper: str | None = None) -> str | None:
    """Who answered, read out of what the layer produced.

    From outside the command the runner can only record that it invoked something, which is
    how every entry came to say `scripts/pipeline.py run` while the interesting fact — which
    model wrote these claims — lived in a hand-kept manifest.json beside it. A layer that a
    model answers declares `by_from`, and the answer travels in its own output.

    A layer whose output is one file for the whole corpus — `summaries` writes every paper's
    entry into one paper-summaries.json — has no top-level place for the model, so it records
    it inside the paper's entry. When the top-level key is absent and the file is a dict keyed
    by paper, fall back to that entry, so `by_from: model` finds it either way.
    """
    key = layer.get("by_from")
    if not key or not outs:
        return None
    p = os.path.join(ROOT, outs[0])
    if not os.path.isfile(p):
        return None
    try:
        with open(p, encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError):
        return None
    if isinstance(data, dict):
        if data.get(key):
            return data[key]
        if paper and isinstance(data.get(paper), dict):
            return data[paper].get(key) or None
    return None


def record(paper: str, layer: dict, by_id: dict, *, note: str, by: str,
           doi: str | None = None) -> dict:
    """Build a run record for a layer that has just run, hashing what it read and wrote."""
    entries = read_ledger(paper)
    prev = _latest(entries, layer["id"])
    ins = inputs_of(layer, by_id, paper, doi)
    outs = expand(layer.get("produces"), paper, doi)
    by = _by_from_output(layer, outs, paper) or by
    return {
        "layer": layer["id"],
        "v": (prev["v"] + 1) if prev else 1,
        "ran": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "kind": layer.get("kind", "step"),
        "note": note,
        "by": by,
        "in": [{"path": r, "sha": digest(r)} for r in ins if digest(r)],
        "in_sets": input_sets(layer, by_id, paper, doi),
        "out": [{"path": r, "sha": digest(r)} for r in outs if digest(r)],
    }


# ── state ─────────────────────────────────────────────────────────────────────

def keep_versions(rec: dict, root: str = ROOT) -> list[str]:
    """Keep a versioned copy of each single file this run produced under runs/.

    A records layer's output file holds only its latest version — the reader, the
    reconciler, the reviewer and the edge step each overwrite one file per run — so an
    earlier version's bytes are otherwise unrecoverable, and the site's two-version
    comparison has nothing to read the older side from. Copying `<name>.<ext>` to
    `<name>.v<N>.<ext>` beside it, where N is the version this run just recorded, makes each
    version addressable without moving the layer's own output path (which everything
    downstream reads) or touching the ledger.

    Only single files under `runs/`: `claims/` versions itself by archiving the whole tree
    into `runs/<paper>/claim-tree.v<N>/`, and a path outside `runs/` is not this runner's to
    duplicate. Nothing is backfilled — a versioned copy exists only for a version this ran.

    Returns the copies made, for the caller to report and a test to assert.
    """
    made: list[str] = []
    for o in rec.get("out", []):
        path = o["path"]
        if not path.startswith("runs/") or "*" in path:
            continue
        src = os.path.join(root, path)
        if not os.path.isfile(src):
            continue
        stem, ext = os.path.splitext(path)
        kept = f"{stem}.v{rec['v']}{ext}"
        shutil.copyfile(src, os.path.join(root, kept))
        made.append(kept)
    return made


def approvals_path(paper: str) -> str:
    return os.path.join(ROOT, "runs", paper, "approvals.jsonl")


def read_approvals(paper: str) -> list[dict]:
    """Approvals recorded for this paper's layer versions.

    An approval is an operation on a version, not a layer of its own: a person read what a
    layer produced and approved *that* output. It names the version it was granted to, so
    when the layer runs again the approval does not follow — it was given to text that no
    longer exists.
    """
    p = approvals_path(paper)
    if not os.path.isfile(p):
        return []
    out = []
    with open(p, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def approve(paper: str, layer_id: str, v: int, *, by: str, note: str = "") -> dict:
    """Record that a person approved one version of one layer."""
    rec = {"layer": layer_id, "v": v, "by": by, "note": note,
           "when": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    p = approvals_path(paper)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec


def state(decl: dict | None = None, slugs: list[str] | None = None) -> dict:
    """The paper x layer matrix.

    A cell is `current` only if it ran and every input still hashes to what that run
    recorded. It is `stale` if an input moved, `blocked` if something it needs is not
    current, `absent` if it never ran, `n/a` if declared impossible, `open` if it is an
    undecided question.
    """
    decl = decl or load()
    by_id = decl["by_id"]
    slugs = slugs or papers()
    order = _toposort(by_id)
    na = decl.get("not_applicable") or {}

    out = {}
    for paper in slugs:
        entries = read_ledger(paper)
        oks = read_approvals(paper)
        cells = {}
        for lid in order:
            layer = by_id[lid]
            if layer.get("scope") == "corpus":
                cells[lid] = {"state": OPEN if layer.get("open") else CURRENT,
                              "scope": "corpus"}
                continue
            if lid in (na.get(paper) or {}):
                cells[lid] = {"state": NA, "why": na[paper][lid]}
                continue

            run = _latest(entries, lid)
            produced = [r for r in expand(layer.get("produces"), paper) if digest(r)]

            # Propagation, and the reason the graph is walked in dependency order. Only
            # staleness propagates: an input that *changed* since the run makes this output
            # wrong. An input that was never *recorded* is a different complaint — nine of
            # these papers were extracted before the ledger existed, and their exports are
            # perfectly consistent with the claim files they were built from. Conflating the
            # two would paint the whole corpus red and say nothing.
            upstream = [d for d in (layer.get("needs") or [])
                        if by_id[d].get("scope") != "corpus"
                        and cells.get(d, {}).get("state") in (STALE, BLOCKED)]
            unrecorded = [d for d in (layer.get("needs") or [])
                          if by_id[d].get("scope") != "corpus"
                          and cells.get(d, {}).get("state") == ABSENT]

            if not run or run.get("backfilled"):
                # No observed run. Either there is no entry at all, or there is a backfilled
                # one — which records that an artifact exists, not that a run was watched.
                # A backfilled entry carries no inputs, so it cannot answer "is this still
                # current"; saying `unrecorded` is the honest answer and is what the state
                # means. The artifact may be perfectly good.
                st = ABSENT if not produced else "unrecorded"

                # What the entry *does* carry is kept. Declining to assert inputs a backfill
                # never observed is the point of #30; discarding the version, the date and the
                # model alongside them was not. Thirteen of Gaedeke's fifteen `unrecorded`
                # cells have an entry naming all three, and the site rendered every one of
                # them as a bare "no run recorded" directly above the artifact it names —
                # which reads as nothing having happened, in a corpus where something did.
                #
                # `by` is written as the literal "unrecorded" when the backfill could not tell
                # who answered, so it is dropped here rather than rendered as an author.
                if run:
                    by = run.get("by")
                    cells[lid] = {"state": st, "v": run["v"], "ran": run.get("ran"),
                                  "note": run.get("note"), "backfilled": True,
                                  "by": None if by == "unrecorded" else by}
            else:
                moved = [i["path"] for i in run.get("in", []) if digest(i["path"]) != i["sha"]]
                lost = [o["path"] for o in run.get("out", []) if not digest(o["path"])]
                # A pattern whose membership has changed: a file it matches appeared or was
                # removed since the run. Entries recorded before `in_sets` existed carry
                # none, and are left alone rather than guessed at.
                appeared = [x["pat"] for x in run.get("in_sets", []) if manifest(x["pat"]) != x["sha"]]
                st = STALE if (moved or lost or appeared) else CURRENT
                cells[lid] = {"state": st, "v": run["v"], "ran": run.get("ran"),
                              "note": run.get("note"), "by": run.get("by"),
                              "moved": moved, "lost": lost, "appeared": appeared}
            if lid not in cells:
                cells[lid] = {"state": st}
            if st == CURRENT and upstream:
                cells[lid]["state"] = BLOCKED
                cells[lid]["blocked_by"] = upstream
            if unrecorded:
                # Not a state — the artifact may be perfectly good. A gap in how it can be
                # accounted for, which is worth showing beside it rather than instead of it.
                cells[lid]["unrecorded_upstream"] = unrecorded

            # Approval, which is about this cell's version rather than about its inputs.
            # An approval of v2 says nothing about v3, so it is reported beside the state
            # rather than folded into it: the output can be perfectly current and unread.
            ok = max((a for a in oks if a.get("layer") == lid),
                     key=lambda a: (a.get("v", 0), a.get("when", "")), default=None)
            if ok:
                cells[lid]["approved"] = {
                    "v": ok["v"], "by": ok.get("by"), "when": ok.get("when"),
                    "note": ok.get("note"),
                    "applies": bool(run) and ok["v"] == run.get("v"),
                }
        out[paper] = cells
    return out


# ── commands ──────────────────────────────────────────────────────────────────

def cmd_graph(args) -> int:
    """Print the DAG in dependency order, so the declaration can be read as a shape."""
    decl = load()
    by_id, groups = decl["by_id"], decl.get("groups") or {}
    print("pipeline — %d layers, %d groups\n" % (len(by_id), len(groups)))
    for lid in _toposort(by_id):
        l = by_id[lid]
        needs = ", ".join(l.get("needs") or []) or "—"
        flag = " ·OPEN" if l.get("open") else (" ·HUMAN" if l.get("requires_human") else "")
        grp = f"[{l['group']}] " if l.get("group") else ""
        print(f"  {lid:18} {l.get('kind',''):10} {l.get('scope',''):7}{flag}")
        print(f"  {'':18} {grp}needs: {needs}")
        if l.get("produces"):
            print(f"  {'':18} → {', '.join(l['produces'])}")
        print()
    return 0


def cmd_backfill(args) -> int:
    """Write ledgers from the run records the repository already keeps.

    Nothing here invents history. A layer gets an entry only where an artifact of it exists
    on disk; the date comes from the record that carries one, else from git, else the file's
    own mtime. The note says where the entry came from, because a backfilled entry is
    weaker evidence than a recorded one and should not pretend otherwise.
    """
    decl = load()
    by_id = decl["by_id"]
    written = 0

    for paper in papers():
        if read_ledger(paper) and not args.force:
            print(f"  {paper:38} ledger exists — skipping (--force to rewrite)")
            continue
        p = ledger_path(paper)
        if args.force and os.path.isfile(p):
            os.remove(p)

        manifest = os.path.join(ROOT, "runs", paper, "manifest.json")
        man = json.load(open(manifest, encoding="utf-8")) if os.path.isfile(manifest) else {}
        by_role = {r["role"]: r for r in (man.get("roles") or [])}

        n = 0
        for lid in _toposort(by_id):
            layer = by_id[lid]
            if layer.get("scope") == "corpus":
                continue
            outs = [r for r in expand(layer.get("produces"), paper) if digest(r)]
            if not outs:
                continue

            role = by_role.get(lid) or by_role.get(lid.replace("-", "_"))
            ran = man.get("recorded") if role else _git_date(outs[0])
            rec = {
                "layer": lid,
                "v": 1,
                "ran": ran or "unknown",
                "kind": layer.get("kind", "step"),
                "note": "backfilled from " + ("runs/manifest.json" if role else "the artifact on disk"),
                "by": (role or {}).get("model") or "unrecorded",
                "backfilled": True,
                # No `in`. Backfill can name the paths the *declaration* says this layer
                # reads, and hash them as they stand now — but that is a guess about a run
                # nobody observed, in the same shape as a measurement. For Gädeke's
                # claim-tree the guess was false: the claim files were committed
                # 2026-03-30 and the reader outputs the declaration points at on
                # 2026-09-10, five months later, sharing no claim text with them. The
                # entry asserted a lineage that never existed, and `state` read those
                # hashes and called the cell current.
                "out": [{"path": r, "sha": digest(r)} for r in outs],
            }
            append(paper, rec)
            n += 1
        written += n
        print(f"  {paper:38} {n} layer(s)")
    print(f"\n{written} ledger entries written across {len(papers())} papers")
    return 0


def _git_date(rel: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", rel],
            cwd=ROOT, capture_output=True, text=True, timeout=10).stdout.strip()
        return out[:19] + "Z" if out else None
    except Exception:                                                  # noqa: BLE001
        return None


GLYPH = {CURRENT: "✓", STALE: "~", ABSENT: "·", BLOCKED: "!",
         NA: "—", OPEN: "?", "unrecorded": "u"}


def cmd_state(args) -> int:
    decl = load()
    st = state(decl)
    paper_layers = [lid for lid, l in decl["by_id"].items() if l.get("scope") != "corpus"]

    if args.json:
        print(json.dumps(st, indent=2, sort_keys=True))
        return 0

    head = "".join(f"{lid[:7]:>9}" for lid in paper_layers)
    print(f"{'paper':26}{head}")
    for paper, cells in st.items():
        row = "".join(f"{GLYPH.get(cells[lid]['state'], '?'):>9}" for lid in paper_layers)
        print(f"{paper[:25]:26}{row}")

    counts = {}
    for cells in st.values():
        for lid in paper_layers:
            counts[cells[lid]["state"]] = counts.get(cells[lid]["state"], 0) + 1
    print("\n  " + "  ".join(f"{GLYPH.get(k,'?')} {k} {v}" for k, v in sorted(counts.items())))

    stale = [(p, lid, c[lid]) for p, c in st.items() for lid in paper_layers
             if c[lid]["state"] == STALE]
    if stale:
        print(f"\n{len(stale)} stale cell(s) — an input moved, vanished or appeared since the run:")
        for p, lid, cell in stale:
            for path in (cell.get("moved") or [])[:3]:
                print(f"  {p} · {lid}  ←  {path}")
            for path in (cell.get("lost") or [])[:3]:
                print(f"  {p} · {lid}  ←  {path} (output gone)")
    if args.fail_on_stale and stale:
        return 1
    return 0


def cmd_run(args) -> int:
    """Run a layer for one paper, and its unmet dependencies first.

    The command comes from the declaration, so there is one definition of how a layer is
    produced and the site's copy-and-run text cannot drift from what actually runs. A layer
    already `current` is skipped: re-running it would produce the same bytes and a second
    ledger entry claiming to be a new version.
    """
    decl = load()
    by_id = decl["by_id"]
    if args.layer not in by_id:
        print(f"error: no layer {args.layer!r}", file=sys.stderr)
        return 2
    if args.paper not in papers():
        print(f"error: no paper {args.paper!r}", file=sys.stderr)
        return 2

    st = state(decl, [args.paper])[args.paper]

    # Dependency order, restricted to this layer's ancestors — and pruned at the ones that
    # are already satisfied.
    #
    # Walking *through* a satisfied ancestor rebuilds a subtree nothing is waiting for. That
    # was harmless while the induction layers declared no command, because each one printed
    # "no runner declared" and was skipped; now that they run, asking for `coverage` on a
    # paper whose claim tree is current would re-run induction underneath it — three reader
    # calls, a reconciliation and an Opus review, to rebuild inputs to a file that is already
    # correct. A satisfied ancestor is a leaf, which is what make has always done.
    #
    # Satisfied means the outputs are there and nothing says they are wrong: `current`, or
    # `unrecorded` — produced before the ledger existed, and consistent with what it was
    # built from as far as anything can tell. `stale` and `blocked` are rebuilt.
    SATISFIED = (CURRENT, "unrecorded")
    wanted, seen = [], set()

    def walk(lid, target=False):
        if lid in seen:
            return
        seen.add(lid)
        if not target and st.get(lid, {}).get("state") in SATISFIED:
            return
        for dep in by_id[lid].get("needs") or []:
            walk(dep)
        wanted.append(lid)

    walk(args.layer, target=True)
    if args.no_deps:
        wanted = [args.layer]

    doi = _doi_of(args.paper)
    ran = 0
    for lid in wanted:
        layer = by_id[lid]
        if layer.get("scope") == "corpus":
            continue
        cur = st.get(lid, {}).get("state")
        if lid != args.layer and cur == CURRENT:
            continue
        if layer.get("requires_human"):
            print(f"  {lid}: requires a person — not runnable from here")
            if lid == args.layer:
                return 3
            continue
        cmd = layer.get("command")
        if not cmd:
            print(f"  {lid}: no runner declared — skipping"
                  f"{' (this is the layer you asked for)' if lid == args.layer else ''}")
            if lid == args.layer:
                return 3
            continue

        cmd = cmd.replace("{paper}", args.paper).replace("{doi}", doi or "")
        # An answer made somewhere other than the configured backend — a subagent, a person —
        # goes through the same runner and the same validation, so the ledger records it the
        # same way. Before this the answered path could only be taken by calling the CLI by
        # hand, which recorded nothing, and the first end-to-end run of the chain had to live
        # in experiments/ because the ledger could not hold it.
        answered = args.answer if lid == args.layer and args.answer else None
        if answered:
            # The raw reply is kept beside the output, before validation and under the
            # version it will get: a verdict whose prompt and output are not both recorded
            # cannot be disputed, and the prompt is already hashed through `reads`. The CLI
            # is handed the kept copy, so the output's `model` field names a path in the
            # repository rather than wherever the reply happened to be written.
            prev = _latest(read_ledger(args.paper), lid)
            kept = os.path.join("runs", args.paper,
                                f"{lid}.answer.v{(prev['v'] + 1) if prev else 1}.json")
            os.makedirs(os.path.dirname(os.path.join(ROOT, kept)), exist_ok=True)
            shutil.copyfile(answered, os.path.join(ROOT, kept))
            cmd += f" --answer {shlex.quote(kept)}"
        print(f"  {lid}: {cmd}")
        if args.dry_run:
            continue
        rc = subprocess.run(cmd, shell=True, cwd=ROOT).returncode
        if rc != 0:
            print(f"  {lid}: exited {rc}", file=sys.stderr)
            return rc
        rec = record(args.paper, layer, by_id,
                     note=args.note or "ran via scripts/pipeline.py",
                     by="scripts/pipeline.py run", doi=doi)
        # The command is the record. Deriving `by` from its first token gave "cd" for every
        # layer whose command starts by changing directory.
        rec["cmd"] = cmd
        if answered:
            rec["answer"] = {"path": kept, "sha": digest(kept)}
            # The output can only say the answer was supplied; who supplied it is known to
            # whoever ran this, and is the fact the ledger exists to keep.
            if args.by:
                rec["by"] = args.by
        append(args.paper, rec)
        # Keep this version's bytes addressable for the site's two-version comparison. Only
        # single files under runs/; claims/ archives itself into claim-tree.v<N>/.
        for kept in keep_versions(rec):
            print(f"  {lid}: kept {kept}")
        ran += 1

    print(f"\n{ran} layer(s) run" + (" (dry run)" if args.dry_run else ""))
    return 0


def cmd_approve(args) -> int:
    """Record that a person read one version of one layer and approved it.

    The counterpart to `run`, and the half that was missing: `approve()` and the reporting
    in `state()` were both written, and nothing could call them, so approvals.jsonl could
    only be written by hand and every cell in the corpus reads unapproved.

    Approval names a version. It defaults to the version currently on the ledger, because
    approving a version that is not the one on disk is almost always a mistake — but it can
    be named explicitly, since reading v2 and recording it after v3 has run is a coherent
    thing to have done.
    """
    decl = load()
    if args.layer not in decl["by_id"]:
        print(f"error: no layer {args.layer!r}", file=sys.stderr)
        return 2
    if args.paper not in papers():
        print(f"error: no paper {args.paper!r}", file=sys.stderr)
        return 2

    run = _latest(read_ledger(args.paper), args.layer)
    if not run:
        print(f"error: {args.layer} has never run for {args.paper} — "
              f"there is no version to approve", file=sys.stderr)
        return 3

    v = args.v if args.v is not None else run["v"]
    if v > run["v"]:
        print(f"error: {args.layer} is at v{run['v']}; cannot approve v{v}", file=sys.stderr)
        return 3

    rec = approve(args.paper, args.layer, v, by=args.by, note=args.note or "")
    current = " (the current version)" if v == run["v"] else \
              f" (superseded — the ledger is at v{run['v']})"
    print(f"{args.paper}/{args.layer} v{v} approved by {rec['by']}{current}")
    if rec["note"]:
        print(f"  {rec['note']}")
    return 0


def _doi_of(paper: str) -> str | None:
    """The paper's DOI, from its claim-tree index."""
    p = os.path.join(ROOT, "claims", paper, "index.md")
    if not os.path.isfile(p):
        return None
    import re
    m = re.search(r"^doi:\s*(\S+)", open(p, encoding="utf-8").read(), re.M)
    return m.group(1).strip("'\"") if m else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("graph", help="print the declared DAG").set_defaults(fn=cmd_graph)
    b = sub.add_parser("backfill", help="write ledgers from existing artifacts")
    b.add_argument("--force", action="store_true", help="rewrite ledgers that already exist")
    b.set_defaults(fn=cmd_backfill)
    s = sub.add_parser("state", help="the paper x layer matrix")
    s.add_argument("--json", action="store_true")
    s.add_argument("--fail-on-stale", action="store_true", help="exit non-zero if any cell is stale")
    s.set_defaults(fn=cmd_state)
    r = sub.add_parser("run", help="run a layer for one paper, and its unmet dependencies")
    r.add_argument("paper")
    r.add_argument("layer")
    r.add_argument("--no-deps", action="store_true", help="run only the named layer")
    r.add_argument("--dry-run", action="store_true", help="print the commands, run nothing")
    r.add_argument("--note", help="the changelog line for the ledger entry")
    r.add_argument("--answer", metavar="FILE",
                   help="record this file as the named layer's answer instead of calling a "
                        "backend; the raw reply is kept beside the output as a version")
    r.add_argument("--by", help="with --answer: who answered, e.g. the model of the subagent")
    r.set_defaults(fn=cmd_run)
    a = sub.add_parser("approve", help="record that a person approved one version of a layer")
    a.add_argument("paper")
    a.add_argument("layer")
    a.add_argument("--by", required=True, help="who read it")
    a.add_argument("--v", type=int, help="which version (default: the one on the ledger)")
    a.add_argument("--note", help="what they checked")
    a.set_defaults(fn=cmd_approve)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
