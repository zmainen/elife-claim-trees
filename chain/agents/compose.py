"""Compose a document from claims: a proposal, a paper, a published record.

    python3 -m chain.agents.compose "Question=question;Hypotheses=hypotheses;Design=design"

Reads the staged inputs under $CHAIN_IN/in/<subject>/<step>/claims.json and writes a claim set
with no claims of its own — only sections that reference the staged claims by global id, or a
staged composition by its artifact id. A paper is claims composed, not claims copied.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def main(spec: str) -> None:
    rd, out, sid = Path(os.environ["CHAIN_IN"]), Path(os.environ["CHAIN_OUT"]), os.environ["CHAIN_SUBJECT"]
    sections = []
    for part in spec.split(";"):
        title, steps = part.split("=", 1)
        refs = []
        for step in steps.split(","):
            cj = rd / "in" / sid / step / "claims.json"
            cs = json.loads(cj.read_text(encoding="utf-8"))
            refs += [f"{sid}:{step}:{c['id']}" for c in cs.get("claims") or []] or [f"{sid}:{step}"]
        sections.append({"title": title, "claims": refs})
    (out / "claims.json").write_text(json.dumps({"claims": [], "edges": [], "sections": sections}, indent=2) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
