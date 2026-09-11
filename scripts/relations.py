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
    "part-of": "a component of another claim — one comparison, condition, measure or study "
               "of a proposition the target states whole; the target is weakened but not "
               "falsified by the source alone",
}

# SUPPORTS and OPPOSES are sets and GAPS is a description map, which is the shape the four
# call sites already used. The descriptions for all three live in DESCRIPTIONS, so nothing has
# to choose between knowing what a relation means and being able to test membership.
SUPPORTS = set(_SUPPORTS)
OPPOSES = set(_OPPOSES)
EDGE_KEYS = SUPPORTS | OPPOSES | set(GAPS)

DESCRIPTIONS = {**_SUPPORTS, **_OPPOSES, **GAPS}

# Which way an edge points, as a sentence about its two ends. A relation name says that two
# claims are related and not which is which, and the prompt that asks a model for edges gave it
# only the name — so `tests` came back from prediction to result as often as from result to
# prediction. The direction lives here, beside the definition, so the prompt contract and the
# checker read one rule.
DIRECTION = {
    "supports": "from the evidence to the claim it is evidence for",
    "tests": "from the empirical result to the prediction it tests",
    "validates": "from the control to the claim whose warrant it strengthens",
    "confirms": "from the result to the prediction or hypothesis it confirms; the reciprocal of predicts",
    "predicts": "from the model or hypothesis to the observation it predicts",
    "extends": "from the later or broader result to the claim it extends",
    "replicates": "from the independent finding to the claim it reproduces",
    "contradicts": "from either claim to the other; they cannot both hold",
    "opposes": "from the claim that stands against to the one it stands against",
    "refutes": "from the evidence to the prediction, hypothesis or alternative it is incompatible with",
    "rules-out": "from the control or evidence to the alternative explanation it eliminates — a claim "
                 "the paper entertains or rejects, never one it asserts",
    "dissociates-with": "symmetric: between the two empirical claims that together establish the contrast",
    "entails": "from the hypothesis to the prediction it deductively implies",
    "derived-from": "from the prediction back to its hypothesis; written mechanically as the reciprocal of entails",
    "interprets": "from the interpretation to the empirical claim it reframes",
    "enables-method": "from the methodological claim to the result whose interpretability it warrants",
    "scopes": "from the scope claim to the claims it bounds, or to `*` for every empirical claim in the paper",
    "requires": "from the dependent claim to its prerequisite: the source would be invalid if the target were false",
    "qualifies": "from the qualifying result to the claim whose applicability it narrows",
    "part-of": "from the component to the claim it is a part of: the source states one "
               "comparison, condition, measure or study of what the target states as a whole",
}

# One edge from the corpus per relation, as (paper, source slug, target slug). The prompt
# contract quotes both claims, so an example that names a slug the corpus no longer has fails
# generation rather than quietly describing an edge that does not exist. Relations with no use
# in the corpus have no example, and the contract says so.
EXAMPLE = {
    "supports": ("headley-2026-inhibitory-rhythms", "distal-inhib-drops-firing-02hz",
                 "hypothesis-distinct-compartmental-roles"),
    "requires": ("headley-2026-inhibitory-rhythms", "distal-inhib-drops-firing-02hz",
                 "l5-model-single-cell-scope"),
    "entails": ("headley-2026-inhibitory-rhythms", "hypothesis-distinct-compartmental-roles",
                "prediction-distal-dendritic-spike-mechanism"),
    "derived-from": ("headley-2026-inhibitory-rhythms", "prediction-distal-dendritic-spike-mechanism",
                     "hypothesis-distinct-compartmental-roles"),
    "tests": ("headley-2026-inhibitory-rhythms", "distal-inhib-drops-firing-02hz",
              "prediction-distal-dendritic-spike-mechanism"),
    "refutes": ("meijer-2025-serotonin-additive-r1", "5ht-stim-leaves-decision-behavior-intact",
                "prediction-5ht-shifts-psychometric"),
    # Gädeke's claim-tree v2 renamed the claim that carries this eliminative edge; the alt- node
    # is the one carried across from v1. `qualifies` left the corpus with the v1 tree — no claim
    # of any paper uses it now — so it has no example, which the contract renders as such.
    "rules-out": ("gadeke-2026-guilt-insula", "participant-happiness-lower-when-participant",
                  "alt-agency-aversion-not-guilt"),
    "dissociates-with": ("headley-2026-inhibitory-rhythms", "distal-inhib-drops-firing-02hz",
                         "perisomatic-inhib-drops-firing-07hz"),
    "validates": ("meijer-2025-serotonin-orthogonal", "wt-controls-rule-out-light-artifact",
                  "5ht-stim-dilates-pupil"),
    "predicts": ("meijer-2025-serotonin-orthogonal", "hypothesis-state-switch-by-5ht",
                 "5ht-stim-dilates-pupil"),
    "confirms": ("meijer-2025-serotonin-orthogonal", "5ht-axis-orthogonal-to-choice-axis",
                 "prediction-5ht-axis-orthogonal-to-choice"),
    "interprets": ("headley-2026-inhibitory-rhythms", "pv-gamma-sst-beta-correspondence",
                   "beta-optimal-distal-dendritic-entrainment"),
    "enables-method": ("kammer-2026-foveal-feedback", "preregistered-design-validates-mvpa",
                       "foveal-v1-decodes-peripheral-saccade-target"),
    "scopes": ("headley-2026-inhibitory-rhythms", "l5-model-single-cell-scope", "*"),
    "extends": ("kammer-2026-foveal-feedback", "v2-v3-generalize-shape-not-category",
                "decoding-shape-sensitive-not-semantic"),
    # The low-minus-high difference is one measure of the insula ROI guilt result, which states
    # the same contrast "even after subtracting responses to high outcomes". Retrofitted onto
    # Gädeke's claim-tree v2 by the `parts` layer (#75).
    "part-of": ("gadeke-2026-guilt-insula", "difference-response-between-low-high",
                "insula-rois-responded-more-low"),
}

# The pairs a reader most often confuses, each with what separates them. The contract renders
# these after the definitions, because a definition read alone is easy to agree with and hard
# to apply at the boundary.
CONFUSABLE = [
    ("requires", "supports",
     "`requires` is a dependency: if the target were false the source would be invalid. "
     "`supports` is evidence: the source makes the target more credible and would survive its "
     "falsity. One empirical claim commonly carries both — it *requires* the scope claim that "
     "bounds the model it was computed in, and *supports* the hypothesis it was run to test."),
    ("entails", "tests",
     "Both connect a hypothesis's arc, in opposite directions and from different roles. "
     "`entails` runs *down* from the hypothesis to a prediction and is deductive: the prediction "
     "follows if the hypothesis holds. `tests` runs *up* from an empirical result to the "
     "prediction it checks. A result never `entails` anything; a hypothesis never `tests`."),
    ("rules-out", "refutes",
     "`rules-out` eliminates an alternative explanation — a claim the paper raises in order to "
     "reject, which has a node of its own with stance `entertains` or `rejects`. `refutes` is "
     "aimed at one of the paper's own predictions or hypotheses that the evidence came out "
     "against; a paper refuting its own prediction is the hypothetico-deductive loop closing. "
     "Never aim `rules-out` at a claim the same paper asserts."),
    ("dissociates-with", "contradicts",
     "`dissociates-with` joins two results that are both true and *differ*: the contrast between "
     "them is the finding, and neither undermines the other. `contradicts` says two claims cannot "
     "both hold. Two conditions producing different effects is a dissociation, not a "
     "contradiction."),
    ("scopes", "requires",
     "A scope claim bounds what a result can mean and is written from the scope claim *to* the "
     "results it bounds (or to `*`). `requires` is written from the result *to* what it depends "
     "on. The same pair of claims can carry both, in opposite directions: the result requires "
     "the scope; the scope scopes the result."),
    ("validates", "supports",
     "`validates` is a control's edge: a check whose specific outcome (a null where a confound "
     "would have produced an effect, a sign-flip, a manipulation check) strengthens the warrant "
     "for a target. `supports` is ordinary evidence for a proposition. A control `validates`; a "
     "main result `supports`."),
    ("part-of", "supports",
     "`part-of` is composition: the source is one comparison, condition, measure or study *of* "
     "the proposition the target states whole, and dropping it weakens the target without "
     "falsifying it. `supports` is evidence: an independent finding that makes the target more "
     "credible and would survive being removed. The insula-ROI result stated beside the "
     "voxel-wise result is a *part of* the claim that the insula tracks the guilt effect; a "
     "distinct finding that happens to bear on that claim merely *supports* it. A filter on "
     "`supports` cannot tell a component from an independent finding, which is why composition "
     "needs its own relation."),
]

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
