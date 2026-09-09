"""Unit tests for review_metrics — the four review-quality metrics.

Pure tests over hand-built ReviewAnnotationSet fixtures: no LLM, no I/O.
Runs under pytest (``pytest tests/test_review_metrics.py``) or standalone
(``python tests/test_review_metrics.py``) for environments without pytest.

The fixtures mirror the spec's worked example (the Niv stress-test review):
a "good" review with full coverage / anchoring / actionability, and a
"degraded" review with an unanchored complaint and an exit-less weakness, so
each metric is exercised both at ceiling and below it.
"""

from __future__ import annotations

from elife_extract.oxa import (
    Claim,
    ClaimGraph,
    ClaimVerdict,
    ReviewAnchor,
    ReviewAnnotationSet,
    ReviewComment,
    ReviewSuggestion,
    ReviewVerdict,
    Reviewer,
    SourceSpan,
    text_node,
)
from elife_extract.review_metrics import (
    actionability,
    agreement,
    anchoring,
    coverage,
    panel_quality,
)

TOL = 1e-9


def approx(a: float, b: float) -> bool:
    return abs(a - b) <= TOL


# ── Fixtures ──────────────────────────────────────────────────────────────

def claimgraph() -> ClaimGraph:
    """Three claims: an empirical result, an interpretation, a hypothesis."""
    return ClaimGraph(children=[
        Claim(identifier="c1-empirical", role="empirical", children=[text_node("X reduces Y.")]),
        Claim(identifier="c2-interp", role="interpretation", children=[text_node("X builds a model.")]),
        Claim(identifier="c3-hyp", role="hypothesis", children=[text_node("X and Y dissociate.")]),
    ])


def _grounded_span(quote: str) -> SourceSpan:
    return SourceSpan(quote=quote, grounding="verified")


def good_review(reviewer: str = "niv-y") -> ReviewAnnotationSet:
    """Every comment anchored; every weakness has an exit; all claims covered."""
    w1 = ReviewComment(
        identifier="w1", polarity="weakness", severity="critical",
        category="statistics", diagnosis="underpowered-null",
        anchor=ReviewAnchor(claimXref="c1-empirical", sourceSpan=_grounded_span("p=0.12, d=0.17")),
        children=[text_node("Null with n=9, no equivalence test.")],
        suggestion=ReviewSuggestion(
            priority="essential", action="add-analysis",
            children=[text_node("Run a TOST equivalence test.")],
            decisiveOutcome=[text_node("If equivalent to zero the claim stands; else soften it.")],
        ),
    )
    w2 = ReviewComment(
        identifier="w2", polarity="weakness", severity="major",
        category="interpretation", diagnosis="interpretive-overreach",
        anchor=ReviewAnchor(claimXref="c2-interp", sourceSpan=_grounded_span("builds predictive models")),
        children=[text_node("Correlation does not establish model-building.")],
        suggestion=ReviewSuggestion(
            priority="important", action="qualify",
            children=[text_node("Soften to 'correlates with contingency'.")],
        ),
    )
    s1 = ReviewComment(
        identifier="s1", polarity="strength", category="significance",
        anchor=ReviewAnchor(claimXref="c3-hyp"),
        children=[text_node("Clean associative-vs-random control.")],
    )
    verdict = ReviewVerdict(
        significance="important", strengthOfEvidence="solid", recommendation="major-revision",
        children=[text_node("Real blind spot, but the central claim outruns a small-n null.")],
        perClaim=[
            ClaimVerdict(claimXref="c1-empirical", justified="not-supported", commentXrefs=["w1"]),
            ClaimVerdict(claimXref="c2-interp", justified="overstated", commentXrefs=["w2"]),
            ClaimVerdict(claimXref="c3-hyp", justified="well-supported"),
        ],
    )
    return ReviewAnnotationSet(
        identifier=f"sautory-2026-{reviewer}", reviewer=Reviewer(identifier=reviewer),
        manuscript="sautory-2026-5ht-vr", verdict=verdict, comments=[w1, w2, s1],
    )


def degraded_review() -> ReviewAnnotationSet:
    """An unanchored complaint + an exit-less weakness; only one claim covered."""
    u1 = ReviewComment(
        identifier="u1", polarity="weakness", severity="major", category="clarity",
        anchor=ReviewAnchor(claimXref="ghost-claim"),  # not in the graph, no span
        children=[text_node("The paper is confusing somewhere.")],
    )
    w3 = ReviewComment(
        identifier="w3", polarity="weakness", severity="minor", category="methodology",
        anchor=ReviewAnchor(claimXref="c1-empirical", sourceSpan=_grounded_span("two-tailed t-test")),
        children=[text_node("Nested design violates independence.")],
        suggestion=ReviewSuggestion(
            priority="important", action="add-analysis",
            children=[text_node("Re-fit with a mixed-effects model.")],
        ),  # has an exit but no decisive-outcome framing
    )
    verdict = ReviewVerdict(
        children=[text_node("Some concerns.")],
        perClaim=[ClaimVerdict(claimXref="c1-empirical", justified="partially-supported")],
    )
    return ReviewAnnotationSet(
        identifier="sautory-2026-weak", reviewer=Reviewer(identifier="weak-r"),
        verdict=verdict, comments=[u1, w3],
    )


# ── Anchoring ─────────────────────────────────────────────────────────────

def test_anchoring_good_is_ceiling():
    a = anchoring(good_review(), claimgraph())
    assert a.n_comments == 3 and a.n_weaknesses == 2
    assert approx(a.rate, 1.0)
    assert approx(a.claim_rate, 1.0)
    assert approx(a.span_rate, 2 / 3)      # only the two weaknesses carry spans
    assert approx(a.weakness_rate, 1.0)


def test_anchoring_degraded_catches_unanchored():
    a = anchoring(degraded_review(), claimgraph())
    # u1 anchors to a non-existent claim with no span -> unanchored; w3 anchored
    assert approx(a.rate, 0.5)
    assert approx(a.claim_rate, 0.5)       # only w3's claimXref resolves
    assert approx(a.weakness_rate, 0.5)


# ── Coverage ──────────────────────────────────────────────────────────────

def test_coverage_good_is_full_with_role_breakdown():
    c = coverage(good_review(), claimgraph())
    assert c.total == 3 and c.covered == 3
    assert approx(c.rate, 1.0)
    assert c.uncovered == []
    assert approx(c.by_role["interpretation"], 1.0)


def test_coverage_degraded_is_partial():
    c = coverage(degraded_review(), claimgraph())
    assert c.covered == 1 and c.total == 3
    assert approx(c.rate, 1 / 3)
    assert c.uncovered == ["c2-interp", "c3-hyp"]
    assert approx(c.by_role["empirical"], 1.0)      # c1 covered
    assert approx(c.by_role["interpretation"], 0.0) # c2 not


# ── Actionability ─────────────────────────────────────────────────────────

def test_actionability_good_all_weaknesses_have_exits():
    act = actionability(good_review())
    assert act.n_weaknesses == 2
    assert approx(act.rate, 1.0)
    assert approx(act.decisive_rate, 0.5)   # only w1 frames a decisive outcome


def test_actionability_degraded_exit_missing():
    act = actionability(degraded_review())
    assert act.n_weaknesses == 2
    assert approx(act.rate, 0.5)            # only w3 has a suggestion
    assert approx(act.decisive_rate, 0.0)


# ── Agreement (panel) ─────────────────────────────────────────────────────

def test_agreement_concordant_vs_discordant():
    # Reviewer A: c1 not-supported(1), c2 overstated(0). Reviewer B: c1 well-supported(4), c2 overstated(0).
    ra = good_review("niv-y")
    rb = good_review("dayan-p")
    rb.verdict.perClaim[0].justified = "well-supported"   # B disagrees on c1
    ag = agreement([ra, rb])
    assert ag.n_assessed["c1-empirical"] == 2
    assert approx(ag.by_claim["c1-empirical"], 0.25)      # spread 3/4 -> 1 - 0.75
    assert approx(ag.by_claim["c2-interp"], 1.0)          # both 'overstated'
    # c3 assessed by both, both well-supported -> full agreement
    assert approx(ag.by_claim["c3-hyp"], 1.0)
    assert approx(ag.mean, (0.25 + 1.0 + 1.0) / 3)


def test_agreement_diagnosis_convergence():
    # Both reviewers raise underpowered-null on c1 -> convergent discovery.
    ag = agreement([good_review("niv-y"), good_review("dayan-p")])
    assert approx(ag.diagnosis_convergence["c1-empirical"], 1.0)
    assert approx(ag.diagnosis_convergence["c2-interp"], 1.0)


def test_agreement_single_reviewer_no_pairwise_claims():
    ag = agreement([good_review()])
    assert ag.by_claim == {}            # nothing assessed by >=2 reviewers
    assert ag.mean == 0.0


# ── Aggregate ─────────────────────────────────────────────────────────────

def test_panel_quality_bundles_everything():
    pq = panel_quality([good_review("niv-y"), good_review("dayan-p")], claimgraph())
    assert len(pq.reviews) == 2
    assert approx(pq.reviews[0].coverage.rate, 1.0)
    assert approx(pq.reviews[0].actionability.rate, 1.0)
    assert approx(pq.agreement.by_claim["c2-interp"], 1.0)


# ── Standalone runner (no pytest required) ────────────────────────────────

if __name__ == "__main__":
    import traceback

    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except Exception:
            print(f"FAIL  {t.__name__}")
            traceback.print_exc()
    print(f"\n{passed}/{len(tests)} passed")
    raise SystemExit(0 if passed == len(tests) else 1)
