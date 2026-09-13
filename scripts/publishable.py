#!/usr/bin/env python3
"""What the site is about to publish that the ledger says is out of date.

`state` has always been able to answer this and nothing asked it at the moment it mattered.
`make build` regenerates what it can and publishes whatever else is committed, so an artifact
that went stale weeks ago reaches the site with nothing in the way.

That is not hypothetical. Gädeke's tree went to claim-tree v2 and every layer that turns a
claim into text went stale with it. The ledger said so. The build did not ask, and the site
served the new tree through the old text: 68 of 74 claims with no wording, 3 of 93 marks still
resolving, blank lines where the claims had been.

    python3 scripts/publishable.py            # report, exit 0
    python3 scripts/publishable.py --fail     # exit 1 if anything is stale

Only the layers whose output the site renders are checked, and only for the papers the site
publishes. A stale export or a stale coverage report is a real thing to fix and not a reason to
block a deploy; a stale wording is on the page.

It reports by default and fails only when asked, because four of the five layers it watches are
model calls. A hard gate in the deploy would mean a page cannot be published until somebody
pays to regenerate it, and a gate that stops honest work gets removed rather than satisfied.
The deploy should pass `--fail` when the corpus is current enough to keep it that way.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline  # noqa: E402

SITE_DATA = "site/src/data"


def rendered_layers(decl: dict) -> list[dict]:
    """The layers whose output a page reads."""
    return [l for l in decl["layers"]
            if any(str(p).startswith(SITE_DATA) for p in (l.get("produces") or []))]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fail", action="store_true",
                    help="exit non-zero if any layer the site renders is out of date")
    args = ap.parse_args()

    decl = pipeline.load()
    layers = rendered_layers(decl)
    state = pipeline.state(decl)

    # `stale` and `blocked` are not the same risk and this gate must not conflate them.
    # Stale means this output is older than the claims it describes: the page renders the
    # current corpus through text that predates it, which is the failure that put 68 blank
    # lines on Gädeke's page. Blocked means an ancestor's provenance cannot be vouched for
    # while this output may be perfectly current — a gap in the account, not on the page.
    # Failing on blocked would mean a paper cannot be published until its whole induction
    # chain is re-run, which costs model calls and would make this gate the first thing
    # anybody switched off.
    stale: list[tuple[str, str, str]] = []
    unvouched: list[tuple[str, str, str]] = []
    for paper in sorted(state):
        for layer in layers:
            cell = state[paper].get(layer["id"], {})
            st = cell.get("state")
            if st == "stale":
                why = (cell.get("moved") or cell.get("appeared") or [""])[0]
                stale.append((paper, layer["id"], why))
            elif st == "blocked":
                unvouched.append((paper, layer["id"], ", ".join(cell.get("blocked_by") or [])))

    model = {l["id"] for l in layers if l.get("by_from") == "model"}
    print(f"Layers the site renders: {', '.join(l['id'] for l in layers)}")

    if stale:
        print(f"\n{len(stale)} out of date — the page renders the current corpus through "
              f"older text:\n")
        print(f"  {'paper':36}{'layer':14}what moved")
        for paper, lid, why in stale:
            print(f"  {paper:36}{lid:14}{why[:44]}")
        costly = sum(1 for s in stale if s[1] in model)
        if costly:
            print(f"\n  {costly} of these are model calls; regenerating them costs money.")
        print("  python3 scripts/pipeline.py run <paper> <layer>")
    else:
        print(f"\nNothing out of date: every layer the site renders is current against the "
              f"claims it describes, for all {len(state)} papers.")

    if unvouched:
        print(f"\n{len(unvouched)} current but unvouched — the output is not older than the "
              f"claims;\nan ancestor's provenance cannot be checked, which is a gap in the "
              f"account rather than on the page:\n")
        for paper, lid, why in unvouched:
            print(f"  {paper:36}{lid:14}behind {why[:36]}")

    if args.fail and stale:
        print("\nRefusing to call this publishable.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
