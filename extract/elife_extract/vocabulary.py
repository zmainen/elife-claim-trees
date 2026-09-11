"""The claim vocabulary, declared once: roles, claim types, confidence.

Relations live in `scripts/relations.py`, one level up, where four scripts already read them.
This module is the same idea for the other three vocabularies the prompts use, which until now
were written into each prompt by hand and disagreed: the results-reader prompt named
`claim_type: hypothesis` in one section and listed five types without it in another; the
reconciler defined `high` as all three readers when the partition means most claims are
visible to at most two; and `schema.py` had been widened to twelve claim types to accept
whatever any prompt happened to say.

`contract.py` renders this into `extract/prompts/contract/vocabulary.md`, which every model
call receives. Examples name a corpus claim by (paper, slug), and the renderer quotes it from
the claim file, so an example is a real claim or generation fails.
"""

from __future__ import annotations

# ── Questions ────────────────────────────────────────────────────────────
# A question is not a claim — a claim is a declarative sentence — so it lives on the paper, not
# in the claim graph. It is what the paper set out to answer, and the paper states it, in the
# abstract or in the Introduction. Each hypothesis and each rejected alternative addresses one:
# the hypothesis is the answer the paper commits to, the alternatives are the answers it turns
# down. A question is never a hypothesis with a question mark: do not manufacture one by
# hollowing a hypothesis into "X involves neural mechanisms" — return the question the paper
# actually asked, or none.

QUESTIONS = (
    "A **question** is what the paper set out to answer. It is not a claim — a claim is a "
    "declarative sentence — so it is recorded on the paper rather than as a node in the graph. "
    "The paper states it, in the abstract or in the opening of the Introduction. Each "
    "`hypothesis` and each rejected alternative addresses one: the hypothesis is the answer the "
    "paper commits to, and the alternatives it rules out are the other answers to the same "
    "question. Never turn a question into a hollow hypothesis such as \"X involves neural "
    "mechanisms\" — return the question the paper actually asked, or return none."
)

# ── Roles ────────────────────────────────────────────────────────────────
# The rhetorical function a claim serves in the paper's argument. Nine values; the corpus uses
# all nine. `example` is (paper, slug). `signals` are phrases in the prose that mark the role.

ROLES = [
    {
        "role": "hypothesis",
        "definition": "An answer the paper commits to, to a question it states: the proposition "
                      "it bets on, phrased as a claim about the world rather than as the "
                      "question. It carries no empirical content of its own; it is what the "
                      "predictions are deduced from and what the results are gathered for, and "
                      "the alternatives the paper rules out are the other answers to the same "
                      "question. Each hypothesis carries `addresses`, the question it answers. "
                      "Most papers have one to three.",
        "typical_claim_type": "hypothesis",
        "signals": ["we hypothesize", "we propose that", "we asked whether", "we sought to test",
                    "the central question is whether"],
        "carries": "`entails` to each of its predictions; usually `panel: null`",
        "example": ("headley-2026-inhibitory-rhythms", "hypothesis-distinct-compartmental-roles"),
    },
    {
        "role": "prediction",
        "definition": "What should be observed if the hypothesis holds, under stated conditions. "
                      "A prediction is deduced, not measured: it is anchored in the model or in "
                      "principled reasoning, and an empirical claim then tests it. Write it as a "
                      "conditional when the paper does not.",
        "typical_claim_type": "prediction",
        "signals": ["if X, then we should observe Y", "this predicts that", "the model predicts",
                    "should be maximally effective at", "is predicted to"],
        "carries": "`derived-from` back to its hypothesis (written mechanically); is the target of `tests`",
        "example": ("headley-2026-inhibitory-rhythms", "prediction-beta-optimal-distal"),
    },
    {
        "role": "empirical",
        "definition": "A measured or computed result, anchored to the panel that shows it, "
                      "carrying the paper's own numbers and the paper's own epistemic verb. The "
                      "largest role.",
        "typical_claim_type": "empirical",
        "signals": ["we found that", "we observed", "we measured", "increased", "did not differ"],
        "carries": "`tests` to the prediction it checks; `supports` and `requires` as the argument needs",
        "example": ("headley-2026-inhibitory-rhythms", "distal-inhib-drops-firing-02hz"),
    },
    {
        "role": "control",
        "definition": "An empirical result whose work in the argument is to eliminate an "
                      "alternative explanation or to show a manipulation did what it should. "
                      "Its content is a measurement; what makes it a control is what it rules "
                      "out. A null result is usually a control.",
        "typical_claim_type": "empirical",
        "signals": ["rules out", "excludes", "is not due to", "no significant effect of",
                    "control condition", "manipulation check", "regardless of"],
        "carries": "`rules-out` to the alternative it eliminates; `validates` to the claim it defends",
        "example": ("gadeke-2026-guilt-insula", "risk-premiums-null-social-solo"),
    },
    {
        "role": "scope",
        "definition": "A boundary condition on what the results can mean: the model class, the "
                      "preparation, the population, the design. Often global. It asserts nothing "
                      "about the world; it says where the paper's assertions apply.",
        "typical_claim_type": "assessment",
        "signals": ["all results come from", "restricted to", "in this preparation",
                    "was not a physiological pattern", "N = "],
        "carries": "`scopes` to the claims it bounds, or `scopes: [\"*\"]`",
        "example": ("headley-2026-inhibitory-rhythms", "l5-model-single-cell-scope"),
    },
    {
        "role": "methodological",
        "definition": "A capability or analytical commitment that a downstream result depends on "
                      "for its interpretation: the sorting pipeline, the null distribution, the "
                      "model fit that licenses a model-based analysis. Not procedure for its own "
                      "sake — which software ran the task is not a claim unless a result turns on "
                      "it.",
        "typical_claim_type": "assessment",
        "signals": ["analysis is on", "nulls are", "fit better than", "validated against"],
        "carries": "`enables-method` to the results it warrants",
        "example": ("kammer-2026-foveal-feedback", "preregistered-design-validates-mvpa"),
    },
    {
        "role": "synthesis",
        "definition": "A higher-order proposition that integrates several of the paper's own "
                      "results into one claim, staying inside the paper's evidence: the "
                      "dissociation, the reconciliation, the summary that several panels jointly "
                      "establish.",
        "typical_claim_type": "synthesis",
        "signals": ["taken together", "these results show", "this dissociation establishes",
                    "in summary"],
        "carries": "is the target of `supports` from the results it integrates",
        "example": ("meijer-2025-serotonin-additive-r1", "orthogonality-derived-from-additivity"),
    },
    {
        "role": "interpretation",
        "definition": "A reading of the results through a theoretical lens from outside the "
                      "paper's own evidence: a mapping onto a framework, a proposed mechanism, a "
                      "functional meaning. It is an act of mapping, not a derivation.",
        "typical_claim_type": "interpretive",
        "signals": ["may provide a functional interpretation", "suggests a role for",
                    "points to a mechanism whereby", "is consistent with the view that"],
        "carries": "`interprets` to the empirical claims it reframes",
        "example": ("headley-2026-inhibitory-rhythms", "pv-gamma-sst-beta-correspondence"),
    },
    {
        "role": "literature-context",
        "definition": "A finding from cited prior work that the paper's argument inherits as a "
                      "premise, recorded as a claim of its own so the inheritance is auditable. "
                      "The citation may be implicit: prose that paraphrases a prior empirical "
                      "pattern as background is literature-context whether or not it names the "
                      "paper.",
        "typical_claim_type": "interpretive",
        "signals": ["as shown by", "previous work has established", "the reported association of",
                    "(Author, Year) found"],
        "carries": "is the target of `requires` or `interprets` from the claims that lean on it",
        "example": ("headley-2026-inhibitory-rhythms", "interprets-pv-gamma-sst-beta-associations"),
    },
]

# Pairs a reader most often confuses, with what separates them and two claims that sit either
# side of the line. Each example is (paper, slug).
ROLE_CONFUSABLE = [
    ("hypothesis", "prediction",
     "A hypothesis says what is the case; a prediction says what will be observed if it is. "
     "\"Compartments serve distinct roles\" is the bet; \"if so, doubling distal inhibition "
     "should suppress dendritic spikes more than doubling perisomatic inhibition\" is what it "
     "commits the paper to seeing. Surface both, and keep them apart: adding predictions never "
     "reduces the number of hypotheses.",
     ("headley-2026-inhibitory-rhythms", "hypothesis-distinct-compartmental-roles"),
     ("headley-2026-inhibitory-rhythms", "prediction-distal-dendritic-spike-mechanism")),
    ("control", "empirical",
     "Both are measurements. Ask what the result is *for*: if it demonstrates the effect the "
     "paper is about, it is empirical; if it shows that something else does not explain that "
     "effect, or that the manipulation worked, it is a control.",
     ("gadeke-2026-guilt-insula", "risk-premiums-null-social-solo"),
     ("gadeke-2026-guilt-insula", "guilt-reduces-happiness-after-partner-loss")),
    ("synthesis", "interpretation",
     "Synthesis stays inside the paper's own evidence and says what several results jointly "
     "establish. Interpretation reaches outside it, to a framework, a mechanism or a literature, "
     "and says what the results mean there.",
     ("meijer-2025-serotonin-additive-r1", "orthogonality-derived-from-additivity"),
     ("headley-2026-inhibitory-rhythms", "pv-gamma-sst-beta-correspondence")),
    ("scope", "methodological",
     "Scope bounds where the results apply and usually qualifies every empirical claim at once. "
     "A methodological claim is a specific capability that specific results depend on for their "
     "meaning. \"All results come from a single-cell model\" is scope; \"the preregistered plan "
     "fixed the decoding pipeline, the ROIs and the tests in advance\" is methodological, "
     "because the decoding results count as confirmatory only if it did.",
     ("headley-2026-inhibitory-rhythms", "l5-model-single-cell-scope"),
     ("kammer-2026-foveal-feedback", "preregistered-design-validates-mvpa")),
    ("literature-context", "interpretation",
     "Literature-context restates what a cited paper found; it is someone else's result, "
     "inherited. Interpretation is this paper's reading of its own results, even when that "
     "reading leans on the literature. The inherited premise and the reading that uses it are "
     "two claims.",
     ("headley-2026-inhibitory-rhythms", "interprets-pv-gamma-sst-beta-associations"),
     ("headley-2026-inhibitory-rhythms", "pv-gamma-sst-beta-correspondence")),
]

# ── Claim types ──────────────────────────────────────────────────────────
# The epistemic character of the proposition, independent of the role it plays. Seven values:
# the five in docs/claim-format.md and the two the corpus uses for its deductive layer, which
# method.md § 4.2 names as the typical type of those roles and 77 claim files carry.

CLAIM_TYPES = [
    ("empirical", "a directly observed or computed result"),
    ("interpretive", "an inference drawn from one or more empirical claims"),
    ("existence", "an assertion that a phenomenon, entity or resource exists"),
    ("synthesis", "a claim integrating results across several analyses or papers"),
    ("assessment", "a methodological, scope or quality claim about how the work was done"),
    ("hypothesis", "a proposition bet on, not yet evidenced by this paper's results"),
    ("prediction", "a deduced expectation, to be tested by an empirical claim"),
]

# ── Confidence, after reconciliation ─────────────────────────────────────
# A fact about agreement between the readers, not about the world. The partition means most
# claims are visible to at most two readers, so "all three" is not the bar for `high`.

CONFIDENCE = [
    ("high", "more than one reader surfaced the same proposition and they agree on its panel "
             "and its direction"),
    ("contested", "more than one reader surfaced it and they disagree — about the panel, the "
                  "direction, or whether it is a hypothesis, a prediction or a result. Record "
                  "what each said in `notes`"),
    ("single-source", "one reader surfaced it. Expected for panel-level numerics (caption reader "
                      "only), scope and methodological claims (structure reader only) and "
                      "synthesis (results reader only); not a mark against the claim"),
]

# What a reader may say about its own claim, before reconciliation.
READER_CONFIDENCE = [
    ("high", "asserted directly in the text the reader was given, with a quotable sentence"),
    ("tentative", "read between the lines, summarised across sentences, or ambiguous in the "
                  "source; say why in `notes`"),
]
