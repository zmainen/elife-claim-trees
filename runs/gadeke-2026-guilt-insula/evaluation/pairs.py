#!/usr/bin/env python3
"""Emit two claim sets for a matcher to align, and score a returned alignment.

The textual matcher in compare.py returned 0/33 while its own near-miss list showed the same
findings in different words — `precuneus-tpj-mpfc-social-decisions` against
`precuneus-left-temporo-parietal-junction-medial`. Two claim sets about one paper do not share
wording, which is why `evaluate` makes the matcher a model call rather than a string compare.

  emit <tree-dir> <out.json>      the two lists, for a matcher to read
  score <tree-dir> <pairs.json>   recovery, role and panel agreement from its answer
"""

import json
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = Path(__import__('os').environ.get('CLAIM_TREES_ROOT', '/Users/zach/Projects/mainenlab/elife-claim-trees/.claude/worktrees/elife-claims-trees-issues-01d4ef'))
PAPER = "gadeke-2026-guilt-insula"
COMMITTED = REPO / "claims" / PAPER


def load(d: Path):
    out = []
    for f in sorted(d.glob("*.md")):
        if f.name == "index.md":
            continue
        m = re.match(r"^---\n(.*?)\n---", f.read_text(encoding="utf-8"), re.S)
        if not m:
            continue
        body = re.sub(r"^([A-Za-z0-9_-]+):\n(\[\]|\{\})\s*$", r"\1: \2", m.group(1), flags=re.M)
        try:
            fm = yaml.safe_load(body) or {}
        except yaml.YAMLError:
            continue
        if fm.get("slug"):
            # The writer records the panel on the assertion, not at top level; the
            # committed tree carries it in both places. Reading only the top-level field
            # made every written claim look panel-less and scored null-vs-null as agreement.
            a = fm.get("assertions") or []
            panel = fm.get("panel") or (a[0].get("panel") if a and isinstance(a[0], dict) else None)
            out.append({"slug": fm["slug"], "claim": (fm.get("claim") or "").strip(),
                        "role": fm.get("role"), "panel": panel})
    return out


def main():
    cmd = sys.argv[1]
    tree = Path(sys.argv[2])
    ref, new = load(COMMITTED), load(tree)

    if cmd == "emit":
        Path(sys.argv[3]).write_text(json.dumps({
            "committed": [{"slug": c["slug"], "claim": c["claim"]} for c in ref],
            "rerun": [{"slug": c["slug"], "claim": c["claim"]} for c in new],
        }, indent=1), encoding="utf-8")
        print(f"  {len(ref)} committed, {len(new)} re-run → {sys.argv[3]}")

    elif cmd == "score":
        pairs = json.loads(Path(sys.argv[3]).read_text())
        if isinstance(pairs, dict):
            pairs = pairs.get("pairs") or pairs.get("matches") or []
        R = {c["slug"]: c for c in ref}
        N = {c["slug"]: c for c in new}
        ok = [p for p in pairs if p.get("committed") in R and p.get("rerun") in N]
        bad = [p for p in pairs if p not in ok]

        print(f"  committed {len(ref)}   re-run {len(new)}")
        if bad:
            print(f"  {len(bad)} pair(s) named a slug that does not exist — ignored")
        print(f"\n  RECOVERY  {len(ok)}/{len(ref)} = {100*len(ok)/len(ref):.0f}%")

        role = sum(1 for p in ok if R[p["committed"]]["role"] == N[p["rerun"]]["role"])
        panel = sum(1 for p in ok
                    if (R[p["committed"]]["panel"] or "") == (N[p["rerun"]]["panel"] or ""))
        if ok:
            print(f"  ROLE      {role}/{len(ok)} = {100*role/len(ok):.0f}% of matched pairs")
            print(f"  PANEL     {panel}/{len(ok)} = {100*panel/len(ok):.0f}% of matched pairs")

        matched = {p["committed"] for p in ok}
        missed = [c for c in ref if c["slug"] not in matched]
        print(f"\n  committed claims the re-run did not recover ({len(missed)}):")
        for c in missed:
            print(f"    {c['role'] or '?':<18} {c['slug']}")

        extra = len(new) - len({p["rerun"] for p in ok})
        print(f"\n  re-run claims with no committed counterpart: {extra}")

        # Where the two disagree on role, on claims they agree are the same claim.
        diff = [(p, R[p["committed"]]["role"], N[p["rerun"]]["role"]) for p in ok
                if R[p["committed"]]["role"] != N[p["rerun"]]["role"]]
        if diff:
            print(f"\n  role disagreements on matched pairs ({len(diff)}):")
            for p, a, b in diff[:15]:
                print(f"    {a:<18} → {b:<18} {p['committed'][:44]}")


if __name__ == "__main__":
    main()
