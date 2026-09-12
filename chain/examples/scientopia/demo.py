"""Run one round of the loop with stand-in players, then let the loop close.

    python3 -m chain.examples.scientopia.demo [target_dir]

Two teams read the library and propose; a funder selects one; the funded team runs its study
and both compose papers; a journal reviews, decides and publishes; the library's catalogue is
re-asked and now holds the publication, so every team's reading of the library is out of date
— which is the loop. Every player's answers come from chain.agents.stub with fixtures under
answers/<player>/<step>.json, recorded as `stub:<player>`, so the store says plainly that
nothing here was decided by anyone. The result stands on its own: process.yaml, personas/,
instructions/, seed/, store/, board.html.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from chain import load, Store, status, ask, answer
from chain.agents import stub
from chain.board import board

HERE = Path(__file__).resolve().parent
COPY = ("process.yaml", "personas", "instructions", "seed", "answers")


def prepare(target: Path) -> Path:
    target.mkdir(parents=True, exist_ok=True)
    if target.resolve() != HERE:
        for name in COPY:
            src, dst = HERE / name, target / name
            if dst.exists():
                shutil.rmtree(dst) if dst.is_dir() else dst.unlink()
            shutil.copytree(src, dst) if src.is_dir() else shutil.copyfile(src, dst)
    if (target / "store").exists():
        shutil.rmtree(target / "store")
    return target


def fixture(root: Path, sid: str, step_id: str) -> Path:
    for p in (root / "answers" / sid / f"{step_id}.json", root / "answers" / f"{step_id}.json"):
        if p.is_file():
            return p
    raise SystemExit(f"no fixture for {sid}/{step_id}")


def answer_pending(proc, store, root, sid, step_id, by=None):
    rd = store.request_dir(sid, step_id)
    out = rd.parent / "answer.json"
    out.write_text(json.dumps(stub.answer(rd, json.loads(fixture(root, sid, step_id).read_text())), indent=2))
    answer(proc, store, root, sid, step_id, out, by=by or f"stub:{sid}", note="a stand-in answer from a fixture")
    out.unlink()


def drive(proc, store, root, sid, goal, log):
    while True:
        done = ask(proc, store, root, sid, goal)
        log.extend((sid,) + d for d in done)
        pending = [d for d in done if d[1] == "pending"]
        if not pending:
            return
        answer_pending(proc, store, root, sid, pending[0][0])


def run(target: Path) -> dict:
    root = prepare(target)
    proc, store = load(root / "process.yaml"), Store(root / "store")
    log = []
    go = lambda sid, goal: drive(proc, store, root, sid, goal, log)
    go("library", "catalogue")
    for team in ("juniper", "larch"):
        go(team, "proposal")
    go("aurora", "select")
    for team in ("juniper", "larch"):
        go(team, "paper")
    go("meridian", "published")
    go("library", "catalogue")                 # the loop: the library has grown
    go("process", "scheme")
    st = status(proc, store, root)
    (root / "board.html").write_text(board(proc, store, root), encoding="utf-8")
    return {"log": log, "status": st}


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE
    r = run(target)
    for sid, step, outcome, where in r["log"]:
        print(f"  {sid:9} {step:13} {outcome:9} {where}")
    print(f"\nboard: {target / 'board.html'}")
