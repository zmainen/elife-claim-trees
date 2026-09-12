"""A stand-in player: the smallest black box that can answer a request.

    python3 -m chain.agents.stub <request_dir> <fixture.json> <answer.json>

It reads only the request directory — INSTRUCTIONS.md, PERSONA.md, CONTRACT.json,
skeleton.json, in/ — and writes one claims.json. Its "reasoning" is a fixture: for an emitting
step the fixture is the claim set to return; for a judging step it is verdicts keyed by the
tail of each item's reference and decisions keyed by the judged artifact, filled into the
skeleton the request supplied. A real player replaces this file and nothing else changes: the
request is the whole interface.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def answer(request_dir: Path, fixture: dict) -> dict:
    contract = json.loads((request_dir / "CONTRACT.json").read_text(encoding="utf-8"))
    skel = request_dir / "skeleton.json"
    if not skel.is_file():
        return fixture
    assert (request_dir / "INSTRUCTIONS.md").is_file(), "a judging player is given instructions"
    ans = json.loads(skel.read_text(encoding="utf-8"))
    rules = fixture.get("assessments") or {}
    default = fixture.get("default")
    decisions = fixture.get("decisions") or {}
    for c in ans["claims"]:
        if c["type"] == "assessment":
            ref = c["about"][0]
            hit = next((v for k, v in rules.items() if ref.endswith(k)), default)
            if hit:
                c.update(verdict=hit["verdict"], text=hit.get("text", ""))
        elif c["type"] == "decision":
            target = c["about"][0]
            hit = next((v for k, v in decisions.items() if target.endswith(k)), fixture.get("overall"))
            if hit:
                c.update(hit)
    ans.pop("_per_item", None); ans.pop("_overall", None)
    assert contract["judges"], "a skeleton only comes with a judging step"
    return ans


if __name__ == "__main__":
    rd, fx, out = (Path(a) for a in sys.argv[1:4])
    Path(out).write_text(json.dumps(answer(rd, json.loads(fx.read_text())), indent=2) + "\n")
