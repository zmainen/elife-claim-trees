#!/usr/bin/env python3
"""Turn reviewed gap-claim drafts into claims, and record who decided.

`gap-claim` drafts what would close each gap and writes candidates; nothing enters the corpus
until a person says so. This is the other side of that gate: it reads the decisions a reviewer
made, writes a claim file for every draft they accepted, and appends an approval naming them.

    python3 scripts/promote.py --decisions reviewed.json            # what it would do
    python3 scripts/promote.py --decisions reviewed.json --write

The decisions file is what the review surface produces, one record per candidate:

    {"paper": "...", "uid": "results-063", "slug": "...", "decision": "accept|reject|edit",
     "claim": "the wording, as edited",  "note": "why", "by": "Zach Mainen",
     "decided_at": "2026-09-11T21:40:00Z"}

An `edit` is an accept whose wording the reviewer changed; both write a claim file, and the
record keeps the draft alongside what was written so the two can be compared later. A reject
writes nothing, and is kept: what a reviewer turned down is evidence about the drafting layer,
and throwing it away would leave only the drafts that happened to be good.

What this deliberately does NOT do: invent relations. A drafted claim enters the tree
unconnected, because `requires`, `supports` and the rest are assertions about logical structure
that neither the drafting layer nor this script is in a position to make.

An earlier version of this note said `edge-inference` would pick them up, and that is false.
`edge-inference` needs only `reconcile`: it runs on the reconciled candidates, upstream of the
claim files, and `claim-tree` then writes the edges it inferred. Nothing downstream of
`claim-tree` decides a relation. So a promoted claim is not merely unconnected for now — no
layer in the pipeline can ever connect it, and the graph gains a node that nothing points at
and that points at nothing.

That is a hole in the pipeline rather than in this script, and it is the reason a promoted
claim should be treated as provisional until a layer exists that asks, of the claim set as it
now stands, what each unconnected claim depends on and supports. Until then this prints what
it is leaving undone rather than implying somebody else will do it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline  # noqa: E402

DECISIONS = ROOT / "review" / "gap-claim-decisions.jsonl"

TEMPLATE = """---
uuid: {uuid}
slug: {slug}
doi: ~
claim: >
  {claim}
claim-type: {claim_type}
role: {role}
concepts: []
priority: {today}
epistemic: {epistemic}

belongings:
[]

assertions:
  - paper-slug: {paper}
    doi: {doi}
    panel: {panel}
    confidence: {epistemic}

provenance:
  drafted-by: gap-claim
  closes-span: {uid}
  span: >
    {span}
  reviewed-by: {by}
  reviewed-on: {decided_at}
  decision: {decision}
{edited_block}---

{body}
"""

# A drafted claim's `role` is the corpus's role vocabulary; `claim-type` is the epistemic
# character of the proposition. The drafting layer answers the first, and the second follows
# from it for every role it can produce.
CLAIM_TYPE = {
    "empirical": "empirical",
    "control": "empirical",
    "interpretation": "interpretive",
    "scope": "assessment",
    "literature-context": "empirical",
}


def load_decisions(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if text.lstrip().startswith("["):
        records = json.loads(text)
    else:
        records = [json.loads(l) for l in text.splitlines() if l.strip()]

    # The review surface appends and never rewrites, so a reviewer who changed their mind is a
    # second record for the same span, and the last one is what they decided. Taken as written,
    # a span accepted and then rejected would be both written and reported as turned down.
    # The earlier records stay in the file: what somebody thought before they thought again is
    # part of the evidence about the drafting layer, which is what this file is for.
    #
    # An `edge` record is not a decision about a draft at all — it is a person saying one of the
    # graph's relations is wrong — and it shares this file only because it is the same kind of
    # thing: a note somebody made while reviewing. Nothing here acts on it.
    latest: dict[tuple[str, str], dict] = {}
    for r in records:
        if r.get("type") == "edge":
            continue
        latest[(r["paper"], r["uid"])] = r
    return list(latest.values())


def candidates(paper: str) -> dict[str, dict]:
    p = ROOT / "runs" / paper / "gap-claim.output.json"
    if not p.is_file():
        return {}
    return {c["uid"]: c for c in json.loads(p.read_text(encoding="utf-8"))["candidates"]}


def write_claim(d: dict, cand: dict) -> Path:
    paper = d["paper"]
    slug = (d.get("slug") or cand["slug"]).strip()
    claim = re.sub(r"\s+", " ", (d.get("claim") or cand["claim"])).strip()
    # The reviewer's role wins over the drafter's. Changing what kind of claim this is was the
    # first thing the first reviewer reached for and could not do; a surface that offers the
    # change and a script that quietly discards it would be worse than not offering it.
    role = (d.get("role") or cand.get("role") or "empirical").strip()
    panel = cand.get("panel") or "~"
    doi = ""
    index = ROOT / "claims" / paper / "index.md"
    if index.is_file():
        m = re.search(r"^doi:\s*(\S+)", index.read_text(encoding="utf-8"), flags=re.M)
        doi = m.group(1) if m else "~"

    edited = ""
    if claim != re.sub(r"\s+", " ", cand["claim"]).strip():
        # The reviewer rewrote it. Both wordings are kept: the difference between what a model
        # drafted and what a scientist accepted is the measurement this whole exercise is for.
        edited = ("  as-drafted: >\n    "
                  + re.sub(r"\s+", " ", cand["claim"]).strip() + "\n")

    out = ROOT / "claims" / paper / f"{slug}.md"
    out.write_text(TEMPLATE.format(
        uuid=uuid.uuid4(), slug=slug, claim=claim,
        claim_type=CLAIM_TYPE.get(role, "empirical"), role=role,
        today=datetime.now(timezone.utc).date().isoformat(),
        epistemic=cand.get("epistemic") or "moderate",
        paper=paper, doi=doi or "~", panel=panel,
        uid=d["uid"], span=re.sub(r"\s+", " ", cand.get("span", "")).strip(),
        by=d.get("by") or "unknown", decided_at=d.get("decided_at") or "",
        decision=d.get("decision") or "accept", edited_block=edited,
        body=(d.get("note") or "").strip(),
    ), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--decisions", default=str(DECISIONS),
                    help=f"the reviewer's decisions (default: {DECISIONS.relative_to(ROOT)})")
    ap.add_argument("--write", action="store_true",
                    help="write the claim files and record the approvals")
    args = ap.parse_args()

    path = Path(args.decisions).expanduser()
    if not path.is_file():
        raise SystemExit(f"no decisions at {path}")
    decisions = load_decisions(path)
    if not decisions:
        raise SystemExit("no decisions to apply")

    by_paper: dict[str, list[dict]] = {}
    for d in decisions:
        by_paper.setdefault(d["paper"], []).append(d)

    total_new, total_rejected = 0, 0
    for paper, ds in sorted(by_paper.items()):
        cands = candidates(paper)
        accepted = [d for d in ds if d.get("decision") in ("accept", "edit")]
        rejected = [d for d in ds if d.get("decision") == "reject"]
        missing = [d["uid"] for d in accepted if d["uid"] not in cands]
        if missing:
            print(f"error: {paper}: no candidate for {', '.join(missing)}", file=sys.stderr)
            return 1
        existing = {f.stem for f in (ROOT / "claims" / paper).glob("*.md")}
        clash = [d for d in accepted if (d.get("slug") or cands[d["uid"]]["slug"]) in existing]
        if clash:
            for d in clash:
                print(f"error: {paper}: {d.get('slug') or cands[d['uid']]['slug']!r} "
                      f"already exists", file=sys.stderr)
            return 1

        print(f"{paper}")
        for d in accepted:
            cand = cands[d["uid"]]
            slug = d.get("slug") or cand["slug"]
            mark = "edited" if d.get("decision") == "edit" else "as drafted"
            if d.get("role") and d["role"] != cand.get("role"):
                mark += f" · retyped {cand.get('role')} → {d['role']}"
            print(f"  + {slug:52} {mark}")
            if args.write:
                write_claim(d, cand)
        for d in rejected:
            print(f"  - {cands.get(d['uid'], {}).get('slug', d['uid']):52} "
                  f"rejected: {(d.get('note') or '').strip()[:60]}")
        total_new += len(accepted)
        total_rejected += len(rejected)

        if args.write:
            who = next((d.get("by") for d in ds if d.get("by")), "unknown")
            run = pipeline._latest(pipeline.read_ledger(paper), "gap-claim")
            if run:
                pipeline.approve(paper, "gap-claim", run["v"], by=who,
                                 note=f"{len(accepted)} of {len(ds)} drafts accepted "
                                      f"into the tree, {len(rejected)} rejected")

    print(f"\n{total_new} claim(s) to add, {total_rejected} rejected")
    if not args.write:
        print("nothing written — pass --write to apply")
        return 0
    print("\nThe claim files are written and the approvals recorded. What follows from that:")
    print("  python3 scripts/pipeline.py state      # coverage and adjudication are now stale")
    print("  the gap verdicts these close no longer match the tree they were judged against")
    print(f"\n  {total_new} claim(s) entered the graph with no relations, and no layer can give")
    print("  them any: edge-inference runs on the reconciled candidates, upstream of the claim")
    print("  files. Until a layer asks that question of the claim set, these are provisional.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
