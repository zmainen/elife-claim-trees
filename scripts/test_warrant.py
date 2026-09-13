#!/usr/bin/env python3
"""The warrant dossier and the version-2 rule floor.

What these pin is the two mechanical pieces of #126 as the 2026-09-13 rulings reframe them: the
dossier assembles the tree's *argument* about a claim — no reproduction, no verification, no
confidence — and `warrant_rule` grades that argument by role. The synthetic cases exercise one
claim per role: predictions and alternatives unchanged, the graded branch on the argument alone,
the cap on an interpretation, the agreement rule for a synthesis, same-kind propagation, and an
empty dossier coming out weak and flagged `unassessed`. The version-3 clauses are pinned too: a
graded claim that rules out a rival is moderate (strong with a validating control), and a
synthesis or interpretation reads the incoming supports it draws on. The corpus case checks the dossier reads
a real tree without judgement in it, and that resolving the whole tree stays inside each role's
vocabulary.

No network. Runs under pytest or standalone.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import warrant  # noqa: E402

PAPER = "gadeke-2026-guilt-insula"


def _d(role, **kw):
    """A dossier dict for one claim, evidence keys empty unless overridden."""
    base = {"slug": kw.get("slug", "x"), "role": role, "stance": kw.get("stance", "asserts"),
            "sentence": "s", "outcome": None, "predictions": [], "validated_by": [],
            "confirms": [], "confirmed_by": [], "rules_out": [], "ruled_out_by": [],
            "supported_by": [], "extended_by": [], "refuted_by": [], "requires": [],
            "part_of": [], "interprets": [], "require_roles": {}, "part_of_roles": {},
            "rivals": []}
    base.update({k: v for k, v in kw.items() if k in base})
    return base


def _lvl(d, resolved=None, unassessed=None):
    return warrant.warrant_rule(d, resolved, unassessed)[0]


# ── predictions: an outcome, not a warrant ────────────────────────────────


def test_prediction_takes_its_outcome():
    assert _lvl(_d("prediction", outcome={"confirms": ["r"], "refutes": [], "tests": ["r"]})) == "confirmed"
    assert _lvl(_d("prediction", outcome={"confirms": [], "refutes": ["r"], "tests": ["r"]})) == "refuted"
    assert _lvl(_d("prediction", outcome={"confirms": [], "refutes": [], "tests": ["r"]})) == "untested"
    assert _lvl(_d("prediction", outcome=None)) == "untested"


# ── alternatives: ruled-out or open ───────────────────────────────────────


def test_alternative_is_ruled_out_when_an_edge_reaches_it():
    assert _lvl(_d("hypothesis", stance="rejects", ruled_out_by=["a-control"])) == "ruled-out"
    assert _lvl(_d("hypothesis", stance="rejects", ruled_out_by=[])) == "open"
    assert _lvl(_d("hypothesis", stance="entertains", ruled_out_by=[])) == "open"


# ── the graded branch: the argument alone ─────────────────────────────────


def test_strong_needs_a_confirmed_prediction_and_a_control():
    for role in ("empirical", "control", "methodological", "scope"):
        lvl, fired = warrant.warrant_rule(_d(role, confirms=["p"], validated_by=["c"]))
        assert lvl == "strong", f"{role} that confirms and is validated should be strong, got {lvl}"
        assert "confirms:p" in fired and "validated-by:c" in fired


def test_exactly_one_of_confirms_or_control_is_moderate():
    assert _lvl(_d("empirical", confirms=["p"])) == "moderate"
    assert _lvl(_d("empirical", validated_by=["c"])) == "moderate"


def test_two_or_more_supporters_is_moderate():
    assert _lvl(_d("empirical", supported_by=["a", "b"])) == "moderate"
    # A single supporter is not enough.
    assert _lvl(_d("empirical", supported_by=["a"])) == "weak"


def test_a_result_refuted_in_the_tree_is_contested():
    lvl, fired = warrant.warrant_rule(_d("empirical", refuted_by=["a-result"]))
    assert lvl == "contested" and "refuted-by:a-result" in fired


def test_a_graded_claim_that_rules_out_a_rival_is_at_least_moderate():
    """§rule v3, A: a control that rules out an alternative is moderate on that alone; with a
    validating control (or a confirmed prediction) it is strong."""
    lvl, fired = warrant.warrant_rule(_d("control", rules_out=["alt-a"]))
    assert lvl == "moderate" and "rules-out:alt-a" in fired
    lvl, fired = warrant.warrant_rule(_d("control", rules_out=["alt-a"], validated_by=["c"]))
    assert lvl == "strong" and "rules-out:alt-a" in fired and "validated-by:c" in fired
    # A confirmed prediction lifts it to strong just as a control does.
    assert _lvl(_d("empirical", rules_out=["alt-a"], confirms=["p"])) == "strong"


def test_an_empty_dossier_is_weak_and_unassessed():
    for role in ("empirical", "control", "methodological", "scope"):
        lvl, fired = warrant.warrant_rule(_d(role))
        assert lvl == "weak" and "unassessed" in fired, f"{role}: {lvl}, {fired}"


def test_no_clause_reads_confidence_or_reproductions():
    """The reframe: warrant reasons from the argument, never from what the paper said or a
    reproduction re-ran. A dossier carrying those keys grades the same as one without them."""
    plain = _d("empirical", confirms=["p"], validated_by=["c"])
    noisy = dict(plain, confidence="weak", reproductions=[{"status": "mismatch"}],
                 verification=[{"status": "verified"}])
    assert warrant.warrant_rule(noisy) == warrant.warrant_rule(plain) == ("strong",
                                                                          ["confirms:p", "validated-by:c"])


# ── hypotheses: their predictions and their rivals ────────────────────────


def test_hypothesis_is_contested_when_a_prediction_is_refuted():
    d = _d("hypothesis", predictions=[{"slug": "p1", "outcome": "confirmed"},
                                      {"slug": "p2", "outcome": "refuted"}])
    assert _lvl(d) == "contested"


def test_hypothesis_is_strong_when_a_prediction_is_confirmed_and_rivals_ruled_out():
    d = _d("hypothesis", predictions=[{"slug": "p1", "outcome": "confirmed"}],
           rivals=["alt-a"])
    assert _lvl(d, {"alt-a": "ruled-out"}) == "strong"


def test_hypothesis_is_moderate_when_a_rival_still_stands():
    d = _d("hypothesis", predictions=[{"slug": "p1", "outcome": "confirmed"}],
           rivals=["alt-a"])
    assert _lvl(d, {"alt-a": "open"}) == "moderate"


def test_hypothesis_is_weak_with_no_prediction_outcome():
    d = _d("hypothesis", predictions=[{"slug": "p1", "outcome": "untested"}])
    assert _lvl(d) == "weak"


# ── interpretation: one step below the strongest it interprets, capped at moderate ──


def test_interpretation_steps_below_the_strongest_and_caps_at_moderate():
    # A strong parent yields moderate — argument alone never reaches strong.
    assert _lvl(_d("interpretation", interprets=["a"]), {"a": "strong"}) == "moderate"
    # A moderate parent yields weak.
    assert _lvl(_d("interpretation", interprets=["a"]), {"a": "moderate"}) == "weak"
    # The strongest of several sets the step.
    assert _lvl(_d("interpretation", interprets=["a", "b"]),
                {"a": "strong", "b": "weak"}) == "moderate"
    # Interpreting nothing is weak.
    assert _lvl(_d("interpretation", interprets=[])) == "weak"


# ── synthesis: agreement among what it interprets ─────────────────────────


def test_synthesis_is_moderate_when_it_interprets_two_or_more_none_weak():
    assert _lvl(_d("synthesis", interprets=["a", "b"]),
                {"a": "moderate", "b": "strong"}) == "moderate"
    # A weak member pulls it to weak.
    assert _lvl(_d("synthesis", interprets=["a", "b"]),
                {"a": "moderate", "b": "weak"}) == "weak"
    # Fewer than two is weak.
    assert _lvl(_d("synthesis", interprets=["a"]), {"a": "moderate"}) == "weak"


def test_synthesis_reads_incoming_supports_as_well_as_interprets():
    """§rule v3, B: a synthesis wired with two graded supporters, none weak, is moderate; with a
    single weak supporter it is weak."""
    lvl, fired = warrant.warrant_rule(_d("synthesis", supported_by=["a", "b"]),
                                      {"a": "moderate", "b": "strong"})
    assert lvl == "moderate" and "supported-by:a=moderate" in fired
    # extends counts as a support input too.
    assert _lvl(_d("synthesis", supported_by=["a"], extended_by=["b"]),
                {"a": "moderate", "b": "moderate"}) == "moderate"
    # One weak supporter: both too few and weak.
    assert _lvl(_d("synthesis", supported_by=["a"]), {"a": "weak"}) == "weak"


def test_interpretation_reads_incoming_supports_when_it_interprets_nothing_graded():
    """§rule v3, B: an interpretation that interprets nothing graded falls back to what supports
    it — two graded supporters none weak is moderate, otherwise weak."""
    assert _lvl(_d("interpretation", supported_by=["a", "b"]),
                {"a": "moderate", "b": "strong"}) == "moderate"
    assert _lvl(_d("interpretation", supported_by=["a"]), {"a": "moderate"}) == "weak"


# ── propagation: bounded by the weakest same-kind claim required ──────────


def test_a_claim_is_capped_by_the_weakest_same_kind_claim_it_requires():
    d = _d("empirical", confirms=["p"], validated_by=["c"], requires=["dep"],
           require_roles={"dep": "control"})
    lvl, fired = warrant.warrant_rule(d, {"dep": "weak"})
    assert lvl == "weak" and any("bounded-by-requires:dep" in f for f in fired)
    # A stronger prerequisite does not lower it.
    assert _lvl(d, {"dep": "strong"}) == "strong"


def test_a_prerequisite_of_another_kind_does_not_bound_but_is_noted_when_unassessed():
    d = _d("empirical", confirms=["p"], validated_by=["c"], requires=["m"],
           require_roles={"m": "methodological"})
    lvl, fired = warrant.warrant_rule(d, {"m": "weak"}, {"m"})
    assert lvl == "strong", "a methodological prerequisite must not bound a result"
    assert "prerequisite-unassessed:m" in fired


def test_methodological_and_scope_are_never_bounded():
    for role in ("methodological", "scope"):
        d = _d(role, confirms=["p"], validated_by=["c"], requires=["dep"],
               require_roles={"dep": "empirical"})
        assert _lvl(d, {"dep": "weak"}) == "strong", f"{role} must not be bounded"


# ── the dossier over a real tree: plain data, and resolution stays in vocab ──


def test_dossier_reads_the_tree_as_argument_only():
    doss = warrant.dossier(PAPER)
    assert len(doss) > 40, "the Gädeke tree should have many claims"
    alt = doss.get("alt-agency-aversion-not-guilt")
    assert alt and alt["ruled_out_by"], "an alternative should record what rules it out"
    # A result that both confirms a prediction and is validated should carry both, unjudged.
    ins = doss.get("insula-rois-responded-more-low")
    assert ins and "validated_by" in warrant.fired_keys(ins) and "confirms" in warrant.fired_keys(ins)
    # No checking record, no confidence, no judgement lives in the dossier.
    for key in ("reproductions", "verification", "confidence", "warrant", "level"):
        assert key not in alt and key not in ins, f"{key} must not be in a v2 dossier"


def test_resolving_the_tree_stays_inside_each_role_s_vocabulary():
    floor = warrant.resolve(PAPER)
    assert floor, "resolve returned nothing"
    for slug, f in floor.items():
        role, stance = f["dossier"]["role"], f["dossier"]["stance"]
        assert f["level"] in warrant.vocabulary_for(role, stance), \
            f"{slug} ({role}) resolved to {f['level']}, outside its vocabulary"


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
