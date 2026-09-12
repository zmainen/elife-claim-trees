"""Import the seed corpus into the library as a claim set.

    python3 -m chain.agents.seed        # reads $CHAIN_IN/in/seed/*.json, writes $CHAIN_OUT/claims.json

Each seed file is a claim set as an outside source states it (the planned seed is the
International Brain Laboratory's brain-wide map papers; the files here are placeholders in that
shape). Claims keep their ids under a `source` prefix and gain a `cites` edge to the source.
"""

from __future__ import annotations

import json
import os
from pathlib import Path


def main() -> None:
    rd, out = Path(os.environ["CHAIN_IN"]), Path(os.environ["CHAIN_OUT"])
    claims, edges = [], []
    for f in sorted((rd / "in" / "seed").glob("*.json")):
        src = json.loads(f.read_text(encoding="utf-8"))
        prefix = src.get("source", f.stem)
        for c in src.get("claims") or []:
            claims.append(dict(c, id=f"{prefix}-{c['id']}", by=f"import:{prefix}",
                               source=src.get("citation", prefix)))
        for e in src.get("edges") or []:
            edges.append({"from": f"{prefix}-{e['from']}", "to": f"{prefix}-{e['to']}", "rel": e["rel"]})
    (out / "claims.json").write_text(json.dumps({"claims": claims, "edges": edges}, indent=2) + "\n")


if __name__ == "__main__":
    main()
