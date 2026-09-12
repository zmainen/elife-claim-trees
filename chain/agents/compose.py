"""Compose a document from claims: a proposal, a paper, an award, a journal's record.

    python3 -m chain.agents.compose sections "Question=question;Design=design"
    python3 -m chain.agents.compose sections "Papers=team:*:paper"           # every player's
    python3 -m chain.agents.compose about-me "Decisions=funder:*:select"     # only claims about this player
    python3 -m chain.agents.compose accepted decision review submissions     # a journal's published record

Reads the staged inputs under $CHAIN_IN/in/ and writes a claim set with no claims of its own —
only sections that reference the staged claims by global id, or a staged composition by its
artifact id. A paper is claims composed, not claims copied.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def _env():
    return Path(os.environ["CHAIN_IN"]), Path(os.environ["CHAIN_OUT"]), os.environ["CHAIN_SUBJECT"]


def _staged(rd: Path) -> dict[str, dict]:
    out = {}
    for cj in (rd / "in").rglob("claims.json"):
        parts = cj.parent.relative_to(rd / "in").parts
        if len(parts) >= 2:
            out[f"{parts[0]}:{parts[1]}"] = json.loads(cj.read_text(encoding="utf-8"))
    return out


def _members(token: str, sid: str, staged: dict) -> list[str]:
    parts = token.split(":")
    if len(parts) == 1:
        return [f"{sid}:{token}"]
    if len(parts) == 3 and parts[1] == "*":
        return sorted(r for r in staged if r.split(":")[0] != sid and r.endswith(":" + parts[2])
                      and _type_of(r, staged, parts[0]))
    return [f"{parts[0]}:{parts[1]}"]


def _type_of(ref: str, staged: dict, stype: str) -> bool:
    # Staged paths are in/<player>/<step>/; the player type is not on disk, so a set
    # reference is matched by step name across staged players. Unambiguous per process.
    return True


def _refs(ref: str, cs: dict) -> list[str]:
    sub, step = ref.split(":", 1)
    return [f"{sub}:{step}:{c['id']}" for c in cs.get("claims") or []] or [ref]


def _write(out: Path, sections: list[dict]) -> None:
    (out / "claims.json").write_text(json.dumps({"claims": [], "edges": [], "sections": sections}, indent=2) + "\n")


def sections(spec: str, filt=None) -> None:
    rd, out, sid = _env()
    st = _staged(rd)
    secs = []
    for part in spec.split(";"):
        title, toks = part.split("=", 1)
        refs = []
        for tok in toks.split(","):
            for ref in _members(tok, sid, st):
                if ref in st:
                    refs += [r for r in _refs(ref, st[ref]) if filt is None or filt(r, st[ref])]
        secs.append({"title": title, "claims": refs})
    _write(out, secs)


def about_me() -> None:
    _, _, sid = _env()

    def mine(r, cs):
        if r.count(":") < 2:
            return False
        c = next(c for c in cs["claims"] if r.endswith(":" + c["id"]))
        return any(a.startswith(sid + ":") for a in c.get("about") or [])
    sections(sys.argv[2], mine)


def accepted(decision_step: str, review_step: str, submissions_step: str) -> None:
    """Every submitted paper the decision accepted, followed by what the review said of it."""
    rd, out, sid = _env()
    st = _staged(rd)
    decisions = st.get(f"{sid}:{decision_step}", {}).get("claims") or []
    reviews = st.get(f"{sid}:{review_step}", {}).get("claims") or []
    accepted_refs = [a for d in decisions if d.get("type") == "decision" and d.get("verdict") == "accept"
                     for a in d.get("about") or []]
    secs = []
    for n, paper in enumerate(accepted_refs, 1):
        secs.append({"title": f"Article {n}", "id": f"pub:{sid}:{n}", "claims": [paper]})
        secs.append({"title": f"Reviews of article {n}", "claims":
                     [f"{sid}:{review_step}:{c['id']}" for c in reviews
                      if c.get("of") == paper or (c.get("about") or [""])[0] == paper]})
        secs.append({"title": f"Decision on article {n}", "claims":
                     [f"{sid}:{decision_step}:{d['id']}" for d in decisions if paper in (d.get("about") or [])]})
    if not accepted_refs:
        secs.append({"title": "Nothing accepted", "claims": [f"{sid}:{decision_step}"]})
    _write(out, secs)


if __name__ == "__main__":
    mode = sys.argv[1]
    {"sections": lambda: sections(sys.argv[2]), "about-me": about_me,
     "accepted": lambda: accepted(*sys.argv[2:5])}[mode]()
