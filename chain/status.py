"""Status: computed from the store, never stored.

    absent    never answered
    pending   a request is open and unanswered
    current   answered; every input still as recorded; every upstream current
    stale     an input changed since the answer
    blocked   answered and unchanged, but something upstream is not current

Two overlays on a cell, each from one file: `assessed` (every judgement of this artifact, and
whether each still applies) and `scheme` (what the newest current ruling on the process said
about this step).
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
    if i["kind"] == "set":
        stype, _, dep = i["ref"].split(":")
        now = [f"{s}:{dep}" for s in proc.subject_ids(stype) if store.latest(s, dep)]
        return now != i.get("members", [])
    if i["kind"] == "declaration":
        return step.hash != i["sha"]
    return sha_path(root / i["path"]) != i["sha"]


def _cell(proc, store, root, sid, step_id, memo):
    if (sid, step_id) in memo:
        return memo[(sid, step_id)]
    step = proc.steps[step_id]
    v = store.latest(sid, step_id)
    open_req = (store.request_dir(sid, step_id) / "manifest.json").is_file()
    if v is None:
        memo[(sid, step_id)] = {"state": "pending" if open_req else "absent", "automatic": step.automatic}
        return memo[(sid, step_id)]
    rec = store.run_record(sid, step_id, v) or {}
    moved = [i.get("ref") or i["path"] for i in rec.get("in", []) if _moved(proc, store, root, step, i)]
    if step.judges == "process" and (rec.get("judges") or {}).get("sha") != proc.hash:
        moved.append(proc.path.name)
    upstream = []
    for tok in step.inputs:
        # A set input (`journal:*:published`) goes stale when the field changes — a member's
        # version moved or the membership did — but it never blocks. Reading the field is a
        # snapshot, and a loop cannot be a wait.
        if not is_ref(tok) or proc.is_set(tok):
            continue
        for sub, dep in proc.expand(tok, sid):
            up = _cell(proc, store, root, sub, dep, memo)
            if up["state"] != "current":
                upstream.append(f"{sub}:{dep}")
    st = "stale" if moved else ("blocked" if upstream else "current")
    if open_req and st != "current":
        st = "pending"
    cell = {"state": st, "v": v, "by": rec.get("by"), "when": rec.get("answered"),
            "automatic": step.automatic, "note": rec.get("note"), "request_open": open_req}
    if moved:
        cell["moved"] = moved
    if upstream:
        cell["blocked_by"] = upstream
    memo[(sid, step_id)] = cell
    return cell


def status(proc: Process, store: Store, root: Path, subjects: list[str] | None = None) -> dict:
    out, memo = {}, {}
    for stype in proc.subjects:
        for sid in proc.subject_ids(stype):
            if subjects and sid not in subjects:
                continue
            out[sid] = {step.id: _cell(proc, store, root, sid, step.id, memo) for step in proc.steps_for(stype)}
    judges = [s for s in proc.steps.values() if s.judges and s.judges != "process"]
    for sid, cells in out.items():
        for step_id, cell in cells.items():
            for j in judges:
                for jsid in proc.subject_ids(j.subject):
                    if (sid, step_id) in proc.expand(j.judges, jsid):
                        d = _judgement(proc, store, jsid, j.id, f"{sid}:{step_id}", out)
                        if d:
                            cell.setdefault("assessed", []).append(d)
    ruling = _ruling(proc, store, out)
    for sid, cells in out.items():
        for step_id, cell in cells.items():
            cell["scheme"] = ruling.get(step_id, "unruled")
    return out


def _judgement(proc, store, jsid, judge_id, target, out):
    """What the judging step's latest version said about `target` (one judged artifact)."""
    v = store.latest(jsid, judge_id)
    if v is None:
        return None
    rec = store.run_record(jsid, judge_id, v) or {}
    ans = C.load(store.version_dir(jsid, judge_id, v)) or {}
    cs = ans.get("claims") or []
    items = [c for c in cs if c.get("type") == "assessment" and (c.get("of") == target or
             (c.get("about") or [""])[0].startswith(target + ":"))]
    considered = [c for c in items if c.get("verdict") != "unconsidered"]
    tally = {}
    for c in considered:
        tally[c["verdict"]] = tally.get(c["verdict"], 0) + 1
    decision = next((c for c in cs if c.get("type") == "decision" and target in (c.get("about") or [])), None)
    if not decision and not items:
        return None
    judged_v = ((rec.get("judges") or {}).get("targets") or {}).get(target)
    return {"step": judge_id, "player": jsid, "v": v, "by": rec.get("by"), "when": rec.get("answered"),
            "verdict": (decision or {}).get("verdict"), "text": (decision or {}).get("text", ""),
            "considered": len(considered), "of": len(items), "tally": tally, "judged_v": judged_v,
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
