"""Run the whole cycle for project `alpha` with stub agents and a stand-in human, then revise
the hypotheses and show what goes stale.

    python3 -m chain.examples.scientopia.demo [target_dir]

Model steps are answered by chain.agents.stub from answers/<step>.json; human steps by the same
stub, recorded as `demo-human`, so the store says plainly that no real person decided anything.
The result is a directory that stands on its own: process.yaml, instructions/, store/, board.html.
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


def prepare(target: Path) -> Path:
    target.mkdir(parents=True, exist_ok=True)
    if target.resolve() != HERE:
        shutil.copyfile(HERE / "process.yaml", target / "process.yaml")
        if (target / "instructions").exists():
            shutil.rmtree(target / "instructions")
        shutil.copytree(HERE / "instructions", target / "instructions")
    if (target / "store").exists():
        shutil.rmtree(target / "store")
    return target


def answer_pending(proc, store, root, sid, step_id, fixture: Path, by: str):
    rd = store.request_dir(sid, step_id)
    out = rd.parent / "answer.json"
    out.write_text(json.dumps(stub.answer(rd, json.loads(fixture.read_text())), indent=2))
    answer(proc, store, root, sid, step_id, out, by=by, note=f"demo answer from {fixture.name}")
    out.unlink()


def run(target: Path, fixtures: Path = HERE / "answers") -> dict:
    root = prepare(target)
    proc, store = load(root / "process.yaml"), Store(root / "store")
    log = []

    def drive(sid, goal):
        while True:
            done = ask(proc, store, root, sid, goal)
            log.extend((sid,) + d for d in done)
            pending = [d for d in done if d[1] == "pending"]
            if not pending:
                return
            step_id = pending[0][0]
            step = proc.steps[step_id]
            by = "stub-agent" if step.worker == "model" else "demo-human"
            answer_pending(proc, store, root, sid, step_id, fixtures / f"{step_id}.json", by)

    drive("alpha", "publish")
    drive("process", "scheme")
    before = status(proc, store, root)

    # A revision: the investigator adds a prediction. Everything downstream goes stale; the
    # funding decision and the reviews no longer apply to what is there now.
    ask(proc, store, root, "alpha", "hypotheses", again=True)
    answer_pending(proc, store, root, "alpha", "hypotheses", fixtures / "hypotheses.v2.json", "stub-agent")
    after = status(proc, store, root)

    (root / "board.html").write_text(board(proc, store, root), encoding="utf-8")
    return {"log": log, "before": before, "after": after}


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE
    r = run(target)
    for sid, step, outcome, where in r["log"]:
        print(f"  {sid:8} {step:16} {outcome:9} {where}")
    print(f"\nboard: {target / 'board.html'}")
