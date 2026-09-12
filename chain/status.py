"""Status: computed from the store, never stored.

    absent    never answered
    pending   a request is open and unanswered
    current   answered; every input still as recorded; every upstream current
    stale     an input changed since the answer
    blocked   answered and unchanged, but something upstream is not current

Two overlays on a cell, each from one file: `assessed` (the newest judgement of this step's
artifact, and whether it still applies) and `scheme` (what the newest current ruling on the
process said about this step).
"""

from __future__ import annotations

from pathlib import Path

from . import claims as C
from .process import Process, is_ref
from .store import Store, sha_path

STATES = ("absent", "pending", "current", "stale", "blocked")


def _moved(proc, store, root, step, i) -> bool:
    if i["kind"] == "step":
        sub, dep = i["ref"].split(":", 1)
        return store.latest(sub, dep) != i["v"]
    if i["kind"] == "declaration":
        return step.hash != i["sha"]
    return sha_path(root / i["path"]) != i["sha"]


def _cell(proc, store, root, sid, step_id, cells):
    step = proc.steps[step_id]
    v = store.latest(sid, step_id)
    open_req = (store.request_dir(sid, step_id) / "manifest.json").is_file()
    if v is None:
        return {"state": "pending" if open_req else "absent", "worker": step.worker}
    rec = store.run_record(sid, step_id, v) or {}
    moved = [i.get("ref") or i["path"] for i in rec.get("in", []) if _moved(proc, store, root, step, i)]
    if step.judges == "process" and (rec.get("judges") or {}).get("sha") != proc.hash:
        moved.append(proc.path.name)
    upstream = []
    for tok in step.inputs:
        if not is_ref(tok):
            continue
        sub, dep = proc.resolve(tok, sid)
        up = cells.get(dep) if sub == sid else _cell(proc, store, root, sub, dep, {})
        if up and up["state"] != "current":
            upstream.append(f"{sub}:{dep}")
    st = "stale" if moved else ("blocked" if upstream else "current")
    if open_req and st != "current":
        st = "pending"
    cell = {"state": st, "v": v, "by": rec.get("by"), "when": rec.get("answered"),
            "worker": step.worker, "note": rec.get("note"), "request_open": open_req}
    if moved:
        cell["moved"] = moved
    if upstream:
        cell["blocked_by"] = upstream
    return cell


def status(proc: Process, store: Store, root: Path, subjects: list[str] | None = None) -> dict:
    out = {}
    for stype in proc.subjects:
        for sid in proc.subject_ids(stype):
            if subjects and sid not in subjects:
                continue
            cells = {}
            for step in proc.steps_for(stype):
                cells[step.id] = _cell(proc, store, root, sid, step.id, cells)
            out[sid] = cells
    for sid, cells in out.items():
        for step_id, cell in cells.items():
            for j in proc.steps.values():
                if j.judges and j.judges != "process" and proc.resolve(j.judges, sid)[1] == step_id:
                    jsid = sid if j.subject == proc.steps[step_id].subject else j.subject
                    d = _judgement(proc, store, jsid, j.id, out)
                    if d:
                        cell.setdefault("assessed", []).append(d)   # one per judging step
    ruling = _ruling(proc, store, out)
    for sid, cells in out.items():
        for step_id, cell in cells.items():
            cell["scheme"] = ruling.get(step_id, "unruled")
    return out


def _judgement(proc, store, jsid, judge_id, out):
    v = store.latest(jsid, judge_id)
    if v is None:
        return None
    rec = store.run_record(jsid, judge_id, v) or {}
    ans = C.load(store.version_dir(jsid, judge_id, v)) or {}
    items = [c for c in ans.get("claims") or [] if c.get("type") == "assessment"]
    considered = [c for c in items if c.get("verdict") != "unconsidered"]
    tally = {}
    for c in considered:
        tally[c["verdict"]] = tally.get(c["verdict"], 0) + 1
    overall = next((c for c in ans.get("claims") or [] if c.get("type") == "decision"), {})
    return {"step": judge_id, "v": v, "by": rec.get("by"), "when": rec.get("answered"),
            "verdict": overall.get("verdict"), "considered": len(considered), "of": len(items),
            "tally": tally, "judged_v": (rec.get("judges") or {}).get("v"),
            "applies": (out.get(jsid) or {}).get(judge_id, {}).get("state") == "current"}


def _ruling(proc, store, out) -> dict[str, str]:
    verdicts = {}
    for s in proc.steps.values():
        if s.judges != "process":
            continue
        for sid in proc.subject_ids(s.subject):
            cell = (out.get(sid) or {}).get(s.id)
            if not cell or cell["state"] != "current":
                for st in proc.steps:
                    verdicts.setdefault(st, "proposed" if cell and cell["state"] in ("stale", "pending") else "unruled")
                continue
            ans = C.load(store.version_dir(sid, s.id, cell["v"])) or {}
            for c in ans.get("claims") or []:
                if c.get("type") == "assessment" and c.get("about"):
                    verdicts[c["about"][0].split(":", 1)[1]] = c.get("verdict", "unconsidered")
    return verdicts
