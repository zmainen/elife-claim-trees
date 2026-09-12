"""A stand-in agent: the smallest black box that can answer a request.

    python3 -m chain.agents.stub <request_dir> <fixture.json> <answer.json>

It reads only the request directory — INSTRUCTIONS.md, CONTRACT.json, skeleton.json, in/ —
and writes one claims.json. Its "reasoning" is a fixture: for an emitting step the fixture is
the claim set to return; for a judging step it is verdicts keyed by the tail of each item's
reference, filled into the skeleton the request supplied. A real agent replaces this file and
nothing else changes: the request is the whole interface.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def answer(request_dir: Path, fixture: dict) -> dict:
    assert (request_dir / "INSTRUCTIONS.md").is_file(), "an agent is given instructions"
    contract = json.loads((request_dir / "CONTRACT.json").read_text(encoding="utf-8"))
    skel = request_dir / "skeleton.json"
    if not skel.is_file():
        return fixture
    ans = json.loads(skel.read_text(encoding="utf-8"))
    rules = fixture.get("assessments") or {}
    default = fixture.get("default")
    for c in ans["claims"]:
        if c["type"] == "assessment":
            ref = c["about"][0]
            hit = next((v for k, v in rules.items() if ref.endswith(k)), default)
            if hit:
                c.update(verdict=hit["verdict"], text=hit.get("text", ""))
        elif c["type"] == "decision":
            c.update(fixture.get("overall") or {})
    ans.pop("_per_item", None); ans.pop("_overall", None)
    assert contract["judges"], "a skeleton only comes with a judging step"
    return ans


if __name__ == "__main__":
    rd, fx, out = (Path(a) for a in sys.argv[1:4])
    Path(out).write_text(json.dumps(answer(rd, json.loads(fx.read_text())), indent=2) + "\n")
