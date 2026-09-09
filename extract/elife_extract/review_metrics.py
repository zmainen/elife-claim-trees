"""Review-quality metrics over structured review annotations.

Pure, deterministic functions computing four orthogonal review-quality metrics
from a ``ReviewAnnotationSet`` (and the manuscript's ``ClaimGraph``). No LLM
calls, no I/O — every metric is a function of the annotations plus the claim
set, so it is unit-testable and cheap to run on every review.

The four metrics, each grounded in a formal-review convention
(``platform/styles/formal-review.md``):

================  ==========================================================
anchoring         fraction of comments that resolve to a claim or a grounded
                  span — *specificity* (conv. 3: figure references are
                  mandatory for weaknesses).
coverage          fraction of the manuscript's claims that received a comment
                  or a per-claim verdict — *completeness* (the "Are the
                  Conclusions Justified?" discipline).
agreement         panel concordance of per-claim verdicts — *reliability*
                  (the editor's consensus scoring + anti-groupthink; the
                  metric is bidirectional — uniform agreement is itself a
                  flag to check for conformity, not just a virtue).
actionability     fraction of weaknesses carrying an exit (a suggestion) —
                  *usefulness* (conv. 4: a weakness without an exit is a
                  complaint, not a critique).
================  ==========================================================

Spec: ``home/collabs/mira/oxa-adoption/structured-review-spec.md``.
Models: ``elife_extract.oxa`` (Hetu's review vocabulary).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from elife_extract.oxa import (
    ClaimGraph,
    ReviewAnnotationSet,
)

# Verdicts placed on an ordinal scale, "how justified is the claim", so the
# spread of a panel's verdicts measures (dis)agreement. ``overstated`` sits at
# the bottom: the assertion exceeds what its evidence supports.
_JUSTIFIED_ORDINAL: dict[str, int] = {
    "well-supported": 4,
    "supported-with-caveats": 3,
    "partially-supported": 2,
    "not-supported": 1,
    "overstated": 0,
}
_JUSTIFIED_RANGE = max(_JUSTIFIED_ORDINAL.values()) - min(_JUSTIFIED_ORDINAL.values())

# A source span counts as anchored only if it actually grounds against the text.
_GROUNDED = {"verified", "fuzzy"}


def _frac(num: int, den: int) -> float:
    """num/den, or 0.0 when den is 0. Callers guard on the reported counts."""
    return num / den if den else 0.0


def _claim_roles(claimgraph: ClaimGraph) -> dict[str, str]:
    return {c.identifier: c.role for c in claimgraph.children}


# ── 1. Anchoring ──────────────────────────────────────────────────────────

@dataclass
class AnchoringResult:
    rate: float          # any anchor resolves (claim OR grounded span)
    claim_rate: float    # anchor.claimXref resolves to a real claim
    span_rate: float     # anchor.sourceSpan grounds (verified/fuzzy)
    weakness_rate: float # anchoring among weaknesses only (the conv-3 target)
    n_comments: int
    n_weaknesses: int


def _claim_anchored(comment, claim_ids: set[str]) -> bool:
    x = comment.anchor.claimXref
    return x is not None and x in claim_ids


def _span_grounded(comment) -> bool:
    ss = comment.anchor.sourceSpan
    return ss is not None and ss.grounding in _GROUNDED


def anchoring(rset: ReviewAnnotationSet, claimgraph: ClaimGraph) -> AnchoringResult:
    """How many comments point, machine-resolvably, at a claim or a passage.

    ``claim_rate`` is the stronger condition (resolves to a real claim id);
    ``span_rate`` requires the cited quote to actually ground in the source.
    A comment with neither is an unanchored complaint.
    """
    ids = set(_claim_roles(claimgraph))
    comments = rset.comments
    weak = [c for c in comments if c.polarity == "weakness"]

    def anchored(c) -> bool:
        return _claim_anchored(c, ids) or _span_grounded(c)

    return AnchoringResult(
        rate=_frac(sum(anchored(c) for c in comments), len(comments)),
        claim_rate=_frac(sum(_claim_anchored(c, ids) for c in comments), len(comments)),
        span_rate=_frac(sum(_span_grounded(c) for c in comments), len(comments)),
        weakness_rate=_frac(sum(anchored(c) for c in weak), len(weak)),
        n_comments=len(comments),
        n_weaknesses=len(weak),
    )


# ── 2. Coverage ───────────────────────────────────────────────────────────

@dataclass
class CoverageResult:
    rate: float                 # claims touched / total claims
    covered: int
    total: int
    by_role: dict[str, float]   # role -> coverage within that role
    uncovered: list[str]        # claim ids with no comment and no verdict


def _touched_claims(rset: ReviewAnnotationSet, ids: set[str]) -> set[str]:
    touched: set[str] = set()
    for c in rset.comments:
        x = c.anchor.claimXref
        if x in ids:
            touched.add(x)
    if rset.verdict.perClaim:
        for cv in rset.verdict.perClaim:
            if cv.claimXref in ids:
                touched.add(cv.claimXref)
    return touched


def coverage(rset: ReviewAnnotationSet, claimgraph: ClaimGraph) -> CoverageResult:
    """Fraction of the manuscript's claims that drew any review attention.

    A claim is *covered* if it has at least one comment anchored to it or a
    per-claim verdict. ``by_role`` exposes the common failure mode of grading
    results (``empirical``) while ignoring the story (``interpretation``).
    """
    roles = _claim_roles(claimgraph)
    ids = set(roles)
    touched = _touched_claims(rset, ids)

    by_role: dict[str, float] = {}
    role_totals: Counter[str] = Counter(roles.values())
    role_hits: Counter[str] = Counter(roles[c] for c in touched)
    for role, total in role_totals.items():
        by_role[role] = _frac(role_hits.get(role, 0), total)

    return CoverageResult(
        rate=_frac(len(touched), len(ids)),
        covered=len(touched),
        total=len(ids),
        by_role=by_role,
        uncovered=sorted(ids - touched),
    )


# ── 3. Agreement (panel-level) ────────────────────────────────────────────

@dataclass
class AgreementResult:
    mean: float                              # mean per-claim agreement
    by_claim: dict[str, float]               # claim -> agreement in [0, 1]
    n_assessed: dict[str, int]               # claim -> #reviewers who issued a verdict
    diagnosis_convergence: dict[str, float]  # claim -> modal-diagnosis fraction


def agreement(panel: list[ReviewAnnotationSet]) -> AgreementResult:
    """Panel concordance on per-claim verdicts, plus convergent discovery.

    For each claim assessed by >=2 reviewers, ``by_claim`` = 1 - (verdict
    spread / range): all-equal verdicts -> 1.0, maximal split -> 0.0.
    ``diagnosis_convergence`` reports, per claim, the fraction of anchored
    weakness diagnoses that share the modal failure mode — independent
    reviewers naming the same ``diagnosis`` is the strongest signal a weakness
    is real. The metric is deliberately bidirectional: uniform agreement is a
    cue for the editor's echo-check, not an unalloyed good.

    Note: in-specialty weighting is not applied here — reviewer expertise is
    panel metadata the editor holds, not a field on the annotation. The editor
    layer weights ``by_claim`` by declared focus areas.
    """
    scores: dict[str, list[int]] = {}
    diagnoses: dict[str, list[str]] = {}
    for rset in panel:
        if rset.verdict.perClaim:
            for cv in rset.verdict.perClaim:
                scores.setdefault(cv.claimXref, []).append(_JUSTIFIED_ORDINAL[cv.justified])
        for c in rset.comments:
            if c.polarity == "weakness" and c.diagnosis and c.anchor.claimXref:
                diagnoses.setdefault(c.anchor.claimXref, []).append(c.diagnosis)

    by_claim: dict[str, float] = {}
    n_assessed: dict[str, int] = {}
    for cid, sc in scores.items():
        n_assessed[cid] = len(sc)
        if len(sc) >= 2:
            by_claim[cid] = 1.0 - (max(sc) - min(sc)) / _JUSTIFIED_RANGE

    convergence: dict[str, float] = {}
    for cid, ds in diagnoses.items():
        if len(ds) >= 2:
            convergence[cid] = _frac(Counter(ds).most_common(1)[0][1], len(ds))

    mean = sum(by_claim.values()) / len(by_claim) if by_claim else 0.0
    return AgreementResult(
        mean=mean,
        by_claim=by_claim,
        n_assessed=n_assessed,
        diagnosis_convergence=convergence,
    )


# ── 4. Actionability ──────────────────────────────────────────────────────

@dataclass
class ActionabilityResult:
    rate: float           # weaknesses with a suggestion (an exit)
    decisive_rate: float  # weaknesses whose suggestion frames a decisive outcome
    n_weaknesses: int


def actionability(rset: ReviewAnnotationSet) -> ActionabilityResult:
    """Fraction of weaknesses that carry an exit.

    A weakness with a ``suggestion`` is a recommendation; one without is a
    complaint. ``decisive_rate`` is the gold standard — the suggestion also
    states an "if X then Y; if Z then W" decisive outcome.
    """
    weak = [c for c in rset.comments if c.polarity == "weakness"]
    has_exit = [c for c in weak if c.suggestion is not None]
    decisive = [c for c in has_exit if c.suggestion.decisiveOutcome]
    return ActionabilityResult(
        rate=_frac(len(has_exit), len(weak)),
        decisive_rate=_frac(len(decisive), len(weak)),
        n_weaknesses=len(weak),
    )


# ── Aggregates ────────────────────────────────────────────────────────────

@dataclass
class ReviewQuality:
    """The single-review quality vector (agreement is panel-level, see below)."""
    review_id: str
    anchoring: AnchoringResult
    coverage: CoverageResult
    actionability: ActionabilityResult


def review_quality(rset: ReviewAnnotationSet, claimgraph: ClaimGraph) -> ReviewQuality:
    return ReviewQuality(
        review_id=rset.identifier,
        anchoring=anchoring(rset, claimgraph),
        coverage=coverage(rset, claimgraph),
        actionability=actionability(rset),
    )


@dataclass
class PanelQuality:
    """Quality across a panel: per-review vectors plus panel-level agreement."""
    reviews: list[ReviewQuality]
    agreement: AgreementResult


def panel_quality(panel: list[ReviewAnnotationSet], claimgraph: ClaimGraph) -> PanelQuality:
    return PanelQuality(
        reviews=[review_quality(r, claimgraph) for r in panel],
        agreement=agreement(panel),
    )
