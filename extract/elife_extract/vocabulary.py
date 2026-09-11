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
        "example": ("gadeke-2026-guilt-insula", "risk-premiums-not-differ-between"),
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
     ("gadeke-2026-guilt-insula", "risk-premiums-not-differ-between"),
     ("gadeke-2026-guilt-insula", "when-partner-received-low-lottery")),
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

# ── What is not a claim ──────────────────────────────────────────────────
# The `methodological` definition drew the line — procedure is a claim only when a result turns
# on it — but the recorded Opus structure reader returned procedure anyway, because the line had
# no examples (docs/design/2026-09-11-parts.md). `WARRANTS` are the positive side: procedure a
# result does turn on, quoted through `_quote` so each resolves to a real methodological claim.
# `NOT_CLAIMS` are the negative side: sentences the reader returned (the six from Gädeke's v3
# structure output, plus one from the earlier DeepSeek run) that no result turns on, each with
# the one thing it merely records.
WARRANTS = [
    ("kammer-2026-foveal-feedback", "preregistered-design-validates-mvpa"),
    ("gadeke-2026-guilt-insula", "model-based-glm-entered-best-fitting-computational"),
    ("gadeke-2026-guilt-insula", "momentary-happiness-modelled-five-computational"),
    ("gadeke-2026-guilt-insula", "parameter-recovery-procedure-synthetic-data-generated"),
]

NOT_CLAIMS = [
    ("Happiness ratings were Z-scored per participant to remove the influence of differing "
     "rating variability across participants.",
     "a normalisation — no result reads differently for it"),
    ("Risk attitude was quantified as a risk premium — the EVdiff value yielding 50% risky "
     "choices from a fitted logistic regression — and compared between Solo and Social "
     "conditions with paired t-tests in both studies.",
     "a definition of a measure — the finding is that the premium did not differ, not that it "
     "was defined this way"),
    ("Two gPPI seed-to-voxel connectivity analyses used functionally defined seeds: the left "
     "insula cluster more sensitive to Risky versus Safe outcomes (GLM3) and the left STS "
     "cluster responding more to social_pRPE than partner_pRPE (GLM4), with identical seeds "
     "across participants.",
     "a seed choice — the connectivity result is the claim, not which seeds produced it"),
    ("All reported clusters survive a whole-brain family-wise-error-corrected threshold of "
     "p < 0.05 with a cluster-forming voxel-wise threshold of p < 0.001 (or a smaller volume "
     "where explicitly mentioned).",
     "a threshold applied to every result alike — a scope condition folded into the paper's "
     "scope claim, not a finding"),
    ("The fMRI data of four Study 2 participants were excluded from the fMRI analysis for "
     "excessive head motion (>3 mm or >3°).",
     "an exclusion count — a component of the paper's scope claim, not a claim of its own"),
    ("The Study 2 sample size of 44 was fixed a priori by a G*Power analysis based on Study 1's "
     "effect size (Cohen's d = 0.56), with alpha = 0.05 and power = 0.95.",
     "a power analysis fixing the sample — a component of the paper's scope claim"),
    ("The experiment was implemented in MATLAB using Psychtoolbox.",
     "a software choice — no result would mean anything different in another toolbox"),
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

# ── Same, part, or different ─────────────────────────────────────────────
# The reconciler's three-way test, shown on real pairs. Each triple is two candidate sentences
# and the verdict, with one line of why. All are drawn from the Gädeke pairs the recorded Opus
# run wrongly kept apart (docs/design/2026-09-11-parts.md); the sentences are quoted literally
# from the claim files, so a triple is an example of what the reconciler actually receives.
# `contract.py` renders these; they are strings, not slugs, because the reconciler compares
# sentences, not files.
SAME_CLAIM = [
    ("same",
     "In both studies, participants felt worse after low lottery outcomes for the partner when "
     "those outcomes followed their own choice rather than the partner's, which the authors "
     "interpret as interpersonal guilt.",
     "When the partner received the low lottery outcome, participant happiness was lower when "
     "the participant rather than the partner had chosen the lottery — a significant "
     "partner-outcome × decision-maker interaction (Study 1: t(1180) = 3.52, p = 0.0004, "
     "β = 0.37; Study 2: t(937) = 2.85, p = 0.0045, β = 0.33) — operationalizing interpersonal "
     "guilt.",
     "The same partner-outcome × decision-maker interaction on the same happiness data, cited "
     "once as a cross-study synthesis and once as the result that computes it: merge, keep the "
     "wording with the coefficients."),
    ("part",
     "One cluster in the left STS responded more to partner reward prediction errors resulting "
     "from participant rather than partner choices (pFWE = 0.022, T = 4.70, d = 0.53, "
     "100 voxels, peak MNI [−52 –32 0]).",
     "The left superior temporal sulcus cluster responded to model-based regressors coding "
     "participant reward prediction resulting from participant and partner choices across both "
     "sessions of the experiment.",
     "The first states one directional contrast — participant-caused above partner-caused — of "
     "the broader responsiveness the second states as a whole: keep both, the first `part_of` "
     "the second."),
    ("different",
     "During receipt of lottery versus safe outcomes (across all conditions), clusters were "
     "more active in the bilateral anterior insula, dmPFC, right STS, bilateral ventral "
     "striatum, right dorsolateral prefrontal cortex, and bilateral inferior parietal lobe.",
     "The bilateral ventral striatum was more active when participants chose the risky rather "
     "than the safe option (Cohen's d = 0.72 left, 0.85 right), irrespective of Social or Solo "
     "condition, replicating previous findings.",
     "Both light up the ventral striatum, but by different computations — one the "
     "lottery-versus-safe outcome-receipt contrast, the other the risky-versus-safe choice "
     "contrast: keep both, no relation between them here."),
]
