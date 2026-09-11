"""The relation vocabulary, declared once.

A relation is a proposition about logical structure between two claims. Which relations exist,
and which of them are oppositions, is the question the `relation-vocab` layer asks and has not
answered — issue #19, and the reason everything downstream of it is provisional.

That question was undecided in four places at once. `corpus_facts.py`, `export_mira.py`,
`formats_report.py` and `check_relations.py` each wrote the vocabulary down, and the four lists
disagreed:

  - `refutes` and `predicts` are defined in docs/method.md § 4.3 and were in none of them. The
    corpus holds one `refutes:` edge — the single instance of that eliminative move — and no
    generated figure on this site has ever counted it, nor did any export carry it.
  - `opposes` had a slot in three of the sets and no MIRA definition, so a paper using it would
    have had the relation silently dropped.
  - The same seven `GAPS` descriptions existed twice, in wording that had drifted apart.

This is the shape of problem the run ledger was built for one level up: four mechanisms, one
question. So the same answer applies — one definition, imported.

Deciding *which* relations are oppositions is still open. This file does not close it; it makes
the question askable in one place instead of four.
"""

from __future__ import annotations

# A relation that asserts the target is strengthened by the source.
_SUPPORTS = {
    "supports": "the source provides evidence for the target",
    "tests": "an empirical result tests the target prediction, closing the loop",
    "validates": "a control whose specific result strengthens the target's warrant",
    "confirms": "the source confirms the target; reciprocal of predicts",
    "predicts": "the source predicts the target, typically model to experiment",
    "extends": "the source extends the target beyond its original conditions",
    "replicates": "an independent finding of the same result as the target",
}

# A relation that asserts the target is weakened, eliminated, or separated from something.
#
# `dissociates-with` sits here uneasily and is held apart by check_relations for that reason:
# it is used more than the rest of this group combined, and many of its uses sit alongside a
# supporting relation on the same pair — coherent only if it means "these two come apart"
# rather than "the target is wrong". Whether it is an opposition at all is the open question.
_OPPOSES = {
    "contradicts": "the source and target cannot both hold",
    "opposes": "the source stands against the target",
    "refutes": "the source's evidence is incompatible with the target",
    "rules-out": "the source's evidence eliminates the target as an explanation",
    "dissociates-with": "the source and target jointly establish a dissociation (symmetric)",
}

# A relation with no supporting or opposing sense, and — for the MIRA export — no predicate at
# all. These are what a conversion to a support/oppose vocabulary costs.
GAPS = {
    "entails": "a hypothesis entails its prediction — the deductive step",
    "derived-from": "a prediction derived from its hypothesis (inverse of entails)",
    "interprets": "one claim interprets another",
    "enables-method": "a result makes a downstream method possible",
    "scopes": "a scope constraint governs another claim's validity",
    "requires": "a claim depends on another holding",
    "qualifies": "a claim narrows another's applicability",
}

# SUPPORTS and OPPOSES are sets and GAPS is a description map, which is the shape the four
# call sites already used. The descriptions for all three live in DESCRIPTIONS, so nothing has
# to choose between knowing what a relation means and being able to test membership.
SUPPORTS = set(_SUPPORTS)
OPPOSES = set(_OPPOSES)
EDGE_KEYS = SUPPORTS | OPPOSES | set(GAPS)

DESCRIPTIONS = {**_SUPPORTS, **_OPPOSES, **GAPS}

# A finer cut of OPPOSES, for the one check that needs it: which relations may not be aimed at
# a claim the same paper asserts.
#
# `rules-out`, `contradicts` and `opposes` assert the target is false, so aiming one at a claim
# the paper holds is an error under any reading — the thing actually being eliminated has no
# node, and the edge found the nearest claim that does.
#
# `refutes` is not in that group, and the distinction is the substance rather than a detail.
# docs/method.md § 4.3 defines its target as "the prediction, hypothesis, or alternative being
# refuted": a paper refuting its own prediction is the hypothetico-deductive loop closing, not
# a mis-aimed edge. Scheller's `self-salience-reduces-perceptual-benefit` refutes that paper's
# own independence hypothesis, which is what the experiment was for. Grouping `refutes` with
# `rules-out` reported eight such cases as errors.
#
# `dissociates-with` is excluded for a different reason: whether it opposes anything at all is
# the open question, and a checker that assumed it does would report it as an error 65 times
# and close issue #19 by attrition.
CONTRARY = {"contradicts", "opposes", "rules-out"}
REFUTES_OWN = {"refutes"}
DISTINGUISHES = {"dissociates-with"}

# What a paper may do with a proposition, per docs/claim-format.md § 2.
STANCES = {"asserts", "entertains", "rejects", "attributes"}


def relations(claim):
    """Every relation this claim declares, as relation names, one per target.

    Two shapes carry them: a top-level YAML key whose value is a list of target slugs, and the
    `belongings` list of `{relation, target}` objects. Both are the schema; a count that reads
    only one of them is wrong by however much the other holds.
    """
    for key in sorted(EDGE_KEYS):
        for target in (claim.get(key) or []):
            if isinstance(target, str):
                yield key
    for item in (claim.get("belongings") or []):
        if isinstance(item, dict) and item.get("relation"):
            yield item["relation"]
