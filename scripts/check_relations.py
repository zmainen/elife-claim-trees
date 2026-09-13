#!/usr/bin/env python3
"""Check that relations mean what they say.

A claim graph's relations are only worth having if they are true, and three kinds of false
relation have already been found in this corpus. Each is invisible to a schema check --
every one is well-formed YAML naming a real slug -- so they need a rule that knows what the
relation types mean.

  1. Opposing a claim the same paper asserts.
     A paper does not rule out what it claims. When the thing actually being ruled out has
     no node, the edge gets aimed at the nearest claim that does. Four such relations
     existed; one of them made two compatible Gaedeke findings contradict each other, so the
     graph asserted an internal contradiction the paper does not make.

  2. Supporting and opposing the same target.
     A source that both supports a target and asserts it false (`contradicts`, `rules-out`,
     `refutes`) is incoherent. The rule is sound now that issue #19/#125 has ruled: the old
     `dissociates-with` was two relations — a neutral contrast (kept as `dissociates-with`) and
     a tension (`in-tension-with`) — and neither is an opposition in this sense, so the pairs
     that once sat in review (a support beside a `dissociates-with`) are fine and close.

  3. Attributing a claim to someone without saying to whom.
     `stance: attributes` without a `source` is indistinguishable from an invented rival.

Two more come from the issue #28 ruling that every tested prediction carries an outcome:

  4. A tested prediction with no outcome.
     A `tests` edge points at the prediction and no `confirms` or `refutes` does, so the graph
     records that the prediction was tested and never how the test came out.

  5. An outcome aimed at a hypothesis.
     `confirms`/`refutes` are outcomes of a stated prediction and aim at predictions only. Aimed
     at a hypothesis they are the shortcut the ruling retires -- the fix is to write the
     prediction the hypothesis entails and aim the outcome there.

Rules 4 and 5 need to know which papers' edge-inference is current under the post-ruling
contract, which is a fact about the ledger this script cannot see -- it reads claim files, not
run state. So it follows the ruling's stated fallback: they are errors for Gaedeke, whose
edge-inference is re-answered under the new contract in the same change, and warnings for every
other paper, whose trees the ruling does not re-run. `--warnings` lists the warnings.

A dangling target -- a relation naming something that is not a claim in the paper -- is
reported the same way, as a warning, not a failure. Some are genuine gaps awaiting the
alternative claims of issue #3; `scopes: '*'` is deliberate and means the whole paper.

Usage:
  python3 scripts/check_relations.py                 # every public paper
  python3 scripts/check_relations.py <paper-slug>
  python3 scripts/check_relations.py --warnings      # include dangling targets
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export_mira import (CLAIMS_DIR, load_paper, public_papers,  # noqa: E402
                         relations)

from relations import (CONTRARY, NEUTRAL_TEST,  # noqa: E402
                       OUTCOME, STANCES)

# The support-plus-oppose rule (issue #19), now sound under the #125 ruling. A source may not
# both *support* a target and assert it *false*. The support side is narrow on purpose: `tests`
# is neutral (a test says nothing about the outcome), and `predicts`/`replicates` do not bear on
# the same-target incoherence — so they are not support here. The oppose side is the moves that
# say the target is false: `contradicts`, `rules-out`, and `refutes` (an outcome aimed at a
# prediction). `in-tension-with` and `dissociates-with` are deliberately *not* in the oppose
# set — a result can support a hypothesis and be in tension with another result, and a
# dissociation is a neutral contrast — which is what closes the 72 cases the checker once held.
LINT_SUPPORT = {"supports", "extends", "validates", "confirms"}
LINT_OPPOSE = {"contradicts", "rules-out", "refutes"}

# The paper whose edge-inference is re-answered under the post-#28 contract in this change, so
# its outcome rules fail rather than warn. See the module docstring.
CURRENT_UNDER_CONTRACT = {"gadeke-2026-guilt-insula"}


def stance(claim, paper_slug):
    """This paper's stance toward this claim. Absent means `asserts` (claim-format.md §2)."""
    for a in (claim.get("assertions") or []):
        if not isinstance(a, dict):
            continue
        if a.get("paper-slug") in (paper_slug, None):
            return a.get("stance") or "asserts"
    return "asserts"


def check(paper_slug):
    claims = load_paper(paper_slug)
    by_slug = {c["slug"]: c for c in claims}
    errors, warnings = [], []

    for c in claims:
        st = stance(c, paper_slug)
        if st not in STANCES:
            errors.append(f"{c['slug']}: unknown stance {st!r} "
                          f"(expected one of {', '.join(sorted(STANCES))})")
        if st == "attributes" and not any(
                (a.get("source") or a.get("citation"))
                for a in (c.get("assertions") or []) if isinstance(a, dict)):
            errors.append(f"{c['slug']}: stance 'attributes' with no source — an attributed "
                          f"claim must say who asserts it")

        seen = {}
        for key, target in relations(c):
            seen.setdefault(target, set()).add(key)

            t = by_slug.get(target)
            if t is None:
                if target.strip() != "*":
                    warnings.append(f"{c['slug']} -{key}-> {target!r} names no claim in "
                                    f"this paper")
                continue

            if stance(t, paper_slug) == "asserts" and key in CONTRARY:
                errors.append(
                    f"{c['slug']} -{key}-> {t['slug']}: cannot oppose a claim this paper "
                    f"asserts. Either the target is the wrong claim, or the thing being "
                    f"opposed needs its own claim with stance 'entertains'.")

        for target, keys in seen.items():
            if keys & LINT_SUPPORT and keys & LINT_OPPOSE:
                errors.append(f"{c['slug']} -> {target}: both supports and opposes "
                              f"({', '.join(sorted(keys))})")

    # Rules 4 and 5, from the issue #28 ruling. Errors for the paper re-answered under the new
    # contract, warnings for the rest -- the script cannot see which trees are current, so it
    # follows the ruling's fallback (see the module docstring).
    bucket = errors if paper_slug in CURRENT_UNDER_CONTRACT else warnings
    incoming: dict[str, set] = {}
    for c in claims:
        for key, target in relations(c):
            if key in OUTCOME or key in NEUTRAL_TEST:
                incoming.setdefault(target, set()).add(key)
        for key, target in relations(c):        # 5. an outcome aimed at a hypothesis
            if key in OUTCOME and by_slug.get(target, {}).get("role") == "hypothesis":
                bucket.append(f"{c['slug']} -{key}-> {target}: outcome aimed at a hypothesis; "
                              f"write the prediction the hypothesis entails and aim it there")
    for c in claims:                            # 4. a tested prediction with no outcome
        if c.get("role") != "prediction":
            continue
        keys = incoming.get(c["slug"], set())
        if keys & NEUTRAL_TEST and not keys & OUTCOME:
            bucket.append(f"{c['slug']}: tested prediction with no outcome edge "
                          f"(a `tests` points at it, no `confirms`/`refutes` does)")

    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper", nargs="?")
    ap.add_argument("--warnings", action="store_true", help="also list dangling targets")
    a = ap.parse_args()

    slugs = [a.paper] if a.paper else public_papers()
    total_e = total_w = 0
    for s in slugs:
        if not os.path.isdir(os.path.join(CLAIMS_DIR, s)):
            print(f"  {s}: no claim directory", file=sys.stderr)
            continue
        errors, warnings = check(s)
        total_e += len(errors)
        total_w += len(warnings)
        if errors or (warnings and a.warnings):
            print(f"\n{s}")
            for e in errors:
                print(f"  ERROR   {e}")
            if a.warnings:
                for w in warnings:
                    print(f"  warn    {w}")

    print(f"\n{total_e} error(s) across {len(slugs)} paper(s)")
    print(f"{total_w} warning(s) — dangling targets and issue #28 outcome gaps"
          + ("" if a.warnings else " — --warnings to list"))
    return 1 if total_e else 0


if __name__ == "__main__":
    raise SystemExit(main())
