"""ask and answer.

`ask` stages a request: one directory holding copies of every input the step may read, the
step's INSTRUCTIONS.md, the player's PERSONA.md, a CONTRACT.json saying what may come back, a
manifest naming every input by hash, and for a judging step a skeleton. A step with a command
is run at once by the referee and answered. Any other step waits for a player. `answer` refuses
an answer whose request has gone stale, validates the claim set, and writes the next version
with its run record naming who answered.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import claims as C
from .process import Process, Step, is_ref
from .store import Store, read_json, sha_path, write_json


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def inputs(proc: Process, store: Store, root: Path, sid: str, step: Step) -> tuple[list[dict], list[str]]:
    ins, missing = [], []
    for tok in step.inputs:
        if not is_ref(tok):
            p = root / tok
            if p.exists():
                ins.append({"kind": "path", "path": tok, "sha": sha_path(p)})
            else:
                missing.append(f"{tok} does not exist")
            continue
        members = proc.expand(tok, sid)
        if proc.is_set(tok):
            # Every player of a type: the membership is an input too, so a new player
            # appearing makes the readers of the set stale. A member without a version yet
            # is simply not staged.
            ins.append({"kind": "set", "ref": tok, "path": tok,
                        "members": [f"{s}:{d}" for s, d in members if store.latest(s, d)]})
        for sub, dep in members:
            v = store.latest(sub, dep)
            if v is None:
                if not proc.is_set(tok):
                    missing.append(f"{sub}:{dep} has no version yet")
                continue
            d = store.version_dir(sub, dep, v)
            ins.append({"kind": "step", "ref": f"{sub}:{dep}", "v": v,
                        "path": str(d.relative_to(root)), "sha": sha_path(d)})
    for kind, rel in (("instructions", step.instructions), ("persona", proc.meta(sid).get("persona"))):
        if rel:
            p = root / rel
            if p.is_file():
                ins.append({"kind": kind, "path": rel, "sha": sha_path(p)})
            else:
                missing.append(f"{kind} {rel} does not exist")
    ins.append({"kind": "declaration", "path": str(proc.path.relative_to(root)), "sha": step.hash})
    return ins, missing


def signature(ins: list[dict]) -> list[tuple]:
    return [(i["kind"], i.get("ref") or i["path"], i.get("v") or i.get("sha") or tuple(i.get("members", [])))
            for i in ins]


def stage(proc: Process, store: Store, root: Path, sid: str, step_id: str) -> Path:
    step = proc.steps[step_id]
    ins, missing = inputs(proc, store, root, sid, step)
    if missing:
        raise SystemExit(f"{sid}/{step_id}: cannot ask yet — " + "; ".join(missing))
    store.wipe_request(sid, step_id)
    rd = store.request_dir(sid, step_id)
    (rd / "in").mkdir(parents=True)
    for i in ins:
        if i["kind"] in ("declaration", "set"):
            continue
        src = root / i["path"]
        dst = rd / "in" / (i["ref"].replace(":", "/") if i["kind"] == "step" else i["path"])
        dst.parent.mkdir(parents=True, exist_ok=True)
        (shutil.copytree if src.is_dir() else shutil.copyfile)(src, dst)
        if i["kind"] == "instructions":
            shutil.copyfile(src, rd / "INSTRUCTIONS.md")
        if i["kind"] == "persona":
            shutil.copyfile(src, rd / "PERSONA.md")
    v = (store.latest(sid, step_id) or 0) + 1
    manifest = {"subject": sid, "step": step_id, "v": v, "automatic": step.automatic,
                "question": step.question, "asked": now(), "in": ins}
    contract = {"emits": step.emits, "types": list(C.TYPES), "relations": list(C.RELATIONS),
                "may_reference": sorted(C.refs_in(rd)), "answer": "claims.json"}
    if step.judges:
        if step.judges == "process":
            targets = [("process", proc.as_judged())]
            manifest["judges"] = {"ref": "process", "sha": proc.hash}
            manifest["steps"] = list(proc.steps)
        else:
            targets = []
            for jsub, jstep in proc.expand(step.judges, sid):
                jv = store.latest(jsub, jstep)
                if jv:
                    targets.append((f"{jsub}:{jstep}", C.load(store.version_dir(jsub, jstep, jv)) or {"claims": []}))
            manifest["judges"] = {"ref": step.judges, "targets": {t: store.latest(*t.split(":", 1)) for t, _ in targets}}
        its = C.items(targets, rd)
        manifest["items"] = {r: it["sha"] for r, it in its.items()}
        manifest["targets"] = [t for t, _ in targets]
        prev = store.latest(sid, step_id)
        prior = C.load(store.version_dir(sid, step_id, prev)) if prev else None
        write_json(rd / "skeleton.json", C.skeleton(step, manifest["targets"], its, prior))
        contract["verdicts"], contract["judges"] = step.verdicts, manifest["targets"]
    write_json(rd / "manifest.json", manifest)
    write_json(rd / "CONTRACT.json", contract)
    (rd / "QUESTION.md").write_text(_question(step, manifest, contract), encoding="utf-8")
    return rd


def _question(step: Step, m: dict, c: dict) -> str:
    L = [f"# {m['subject']} · {step.id} · v{m['v']}", "", step.question, "",
         "Read INSTRUCTIONS.md and PERSONA.md if present, then everything under in/. Write claims.json "
         "as CONTRACT.json says. Refer only to what is listed there.", "", "## Staged", ""]
    L += [f"- `in/{i['ref'].replace(':', '/') if i['kind'] == 'step' else i['path']}`  {i['sha']}"
          for i in m["in"] if i["kind"] in ("step", "path", "instructions", "persona")]
    if step.emits:
        L += ["", f"May emit claims of type: {', '.join(step.emits)}."]
    if step.judges:
        L += ["", f"## Judging {', '.join(m['targets'])}", "", f"{len(m.get('items') or {})} items. Fill "
              f"skeleton.json: an assessment per item with a verdict from {step.verdicts}, and a decision "
              f"per judged artifact (accept / reject / partial). Leave what you did not read `unconsidered` "
              f"and mark the decisions `partial`; a partial reading is a legitimate answer."]
    if step.command:
        L += ["", "## Command", "", f"    {step.command}", "", "reads $CHAIN_IN, writes $CHAIN_OUT."]
    return "\n".join(L) + "\n"


def answer(proc: Process, store: Store, root: Path, sid: str, step_id: str, src: Path, *,
           by: str, note: str = "") -> Path:
    step = proc.steps[step_id]
    rd = store.request_dir(sid, step_id)
    if not (rd / "manifest.json").is_file():
        raise SystemExit(f"{sid}/{step_id}: no open request — `ask` first")
    manifest = read_json(rd / "manifest.json")
    fresh, _ = inputs(proc, store, root, sid, step)
    if signature(fresh) != signature(manifest["in"]) or (
            step.judges == "process" and manifest["judges"]["sha"] != proc.hash):
        raise SystemExit(f"{sid}/{step_id}: an input changed since the request — ask again")

    src = Path(src)
    cj = src / "claims.json" if src.is_dir() else src
    ans = json.loads(cj.read_text(encoding="utf-8")) if cj.is_file() else None
    if step.emits or step.judges or ans is not None:
        if ans is None:
            raise SystemExit(f"{sid}/{step_id}: the answer is claims.json")
        for c in ans.get("claims") or []:
            c.setdefault("by", by)
        problems = C.validate(step, sid, ans, C.refs_in(rd), manifest)
        if problems:
            raise SystemExit(f"{sid}/{step_id}: answer rejected —\n  " + "\n  ".join(problems))

    v = manifest["v"]
    vd = store.version_dir(sid, step_id, v)
    if vd.exists():
        raise SystemExit(f"{sid}/{step_id}: v{v} exists")
    if src.is_dir():
        shutil.copytree(src, vd)
    else:
        vd.mkdir(parents=True)
    if ans is not None:
        write_json(vd / "claims.json", ans)
    for name in ("QUESTION.md", "INSTRUCTIONS.md", "PERSONA.md"):
        if (rd / name).is_file():
            shutil.copyfile(rd / name, vd / name)
    rec = {"subject": sid, "step": step_id, "v": v, "automatic": step.automatic, "by": by, "note": note,
           "asked": manifest["asked"], "answered": now(), "in": manifest["in"],
           "judges": manifest.get("judges"), "out": {"path": str(vd.relative_to(root)), "sha": sha_path(vd)}}
    write_json(vd / "run.json", rec)
    store.append(sid, rec)
    store.wipe_request(sid, step_id)
    return vd


def ask(proc: Process, store: Store, root: Path, sid: str, target: str, *, by: str | None = None,
        note: str = "", again: bool = False) -> list[tuple[str, str, str]]:
    """Ask `target`, asking first whatever it needs of the same player that is not current.
    Commands run at once; the first step that waits for a player stops the walk. Idempotent: a
    current target is not re-asked without `again`."""
    from .status import status
    st = status(proc, store, root, [sid])[sid]
    wanted, seen = [], set()

    def walk(step_id, top=False):
        if step_id in seen:
            return
        seen.add(step_id)
        if st[step_id]["state"] == "current" and not (top and again):
            return
        for tok in proc.steps[step_id].inputs:
            if is_ref(tok) and not proc.is_set(tok):
                sub, dep = proc.expand(tok, sid)[0]
                if sub == sid:
                    walk(dep)
        wanted.append(step_id)

    walk(target, top=True)
    done = []
    for step_id in wanted:
        step = proc.steps[step_id]
        rd = stage(proc, store, root, sid, step_id)
        if not step.automatic:
            done.append((step_id, "pending", str(rd.relative_to(root))))
            break
        out = rd / "out"
        out.mkdir()
        pkg_root = str(Path(__file__).resolve().parents[1])
        env = dict(os.environ, CHAIN_IN=str(rd), CHAIN_OUT=str(out), CHAIN_SUBJECT=sid, CHAIN_STEP=step_id,
                   PYTHONPATH=pkg_root + os.pathsep + os.environ.get("PYTHONPATH", ""),
                   PATH=str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", ""))
        rc = subprocess.run(step.command, shell=True, cwd=root, env=env).returncode
        if rc != 0:
            raise SystemExit(f"{sid}/{step_id}: command exited {rc}")
        vd = answer(proc, store, root, sid, step_id, out, by=by or "referee", note=note)
        done.append((step_id, "answered", str(vd.relative_to(root))))
    return done
