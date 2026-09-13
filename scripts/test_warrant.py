#!/usr/bin/env python3
"""The warrant dossier and the version-1 rule floor.

What these pin is the two mechanical pieces of #126: the dossier assembles what the tree holds
about a claim's support, and `warrant_rule` grades it by role. The synthetic cases exercise one
claim per role — including the single fact the note requires, that a `mismatch` reproduction
comes out `contested`. The corpus case checks the dossier reads a real tree without judgement in
it, and that resolving the whole tree stays inside each role's vocabulary.

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
            "confidence": kw.get("confidence"), "sentence": "s", "outcome": None,
            "predictions": [], "validated_by": [], "rules_out": [], "ruled_out_by": [],
            "reproductions": [], "verification": [], "requires": [], "part_of": [],
            "interprets": [], "supported_by": [], "extended_by": [], "rivals": [],
            "refuted_by_other_paper": []}
    base.update({k: v for k, v in kw.items() if k in base})
    return base


def _lvl(d, resolved=None):
    return warrant.warrant_rule(d, resolved)[0]


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


# ── the graded branch: empirical, control, methodological, scope ──────────


def test_a_mismatch_reproduction_is_contested():
    """The one fact the note's §evaluation requires the rule to get right."""
    for role in ("empirical", "control", "methodological", "scope"):
        lvl, fired = warrant.warrant_rule(_d(role, reproductions=[{"status": "mismatch"}]))
        assert lvl == "contested", f"{role} with a mismatch should be contested, got {lvl}"
        assert "reproduction:mismatch" in fired


def test_a_result_refuted_by_another_paper_is_contested():
    assert _lvl(_d("empirical", refuted_by_other_paper=["other/claim"])) == "contested"


def test_a_verified_reproduction_is_strong():
    assert _lvl(_d("empirical", reproductions=[{"status": "verified"}])) == "strong"


def test_a_control_that_validates_with_no_partial_is_strong():
    assert _lvl(_d("empirical", validated_by=["ctrl"])) == "strong"
    # A partial alongside pulls it off strong.
    assert _lvl(_d("empirical", validated_by=["ctrl"],
                   reproductions=[{"status": "partial"}])) == "weak"


def test_only_a_partial_reproduction_is_weak():
    assert _lvl(_d("empirical", reproductions=[{"status": "partial"}])) == "weak"


def test_tentative_and_unchecked_is_weak():
    assert _lvl(_d("empirical", confidence="tentative")) == "weak"
    assert _lvl(_d("scope", confidence="weak")) == "weak"


def test_asserted_with_only_a_blocked_or_unattempted_check_is_moderate():
    assert _lvl(_d("methodological", confidence="tentative",
                   reproductions=[{"status": "blocked"}])) == "moderate"
    assert _lvl(_d("control", confidence="tentative",
                   reproductions=[{"status": "unattempted"}])) == "moderate"


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


# ── synthesis and interpretation: the minimum over what they interpret ────


def test_interpretation_takes_the_minimum_over_what_it_interprets():
    d = _d("interpretation", interprets=["a", "b"])
    assert _lvl(d, {"a": "strong", "b": "weak"}) == "weak"
    assert _lvl(_d("synthesis", interprets=["a"]), {"a": "moderate"}) == "moderate"


# ── propagation: bounded by the weakest claim required ────────────────────


def test_a_graded_claim_is_capped_by_the_weakest_claim_it_requires():
    d = _d("empirical", reproductions=[{"status": "verified"}], requires=["dep"])
    lvl, fired = warrant.warrant_rule(d, {"dep": "weak"})
    assert lvl == "weak" and any("bounded-by-requires:dep" in f for f in fired)
    # A stronger prerequisite does not lower it.
    assert _lvl(d, {"dep": "strong"}) == "strong"


# ── the dossier over a real tree: plain data, and resolution stays in vocab ──


def test_dossier_reads_the_tree_as_plain_data():
    doss = warrant.dossier(PAPER)
    assert len(doss) > 40, "the Gädeke tree should have many claims"
    alt = doss.get("alt-agency-aversion-not-guilt")
    assert alt and alt["ruled_out_by"], "an alternative should record what rules it out"
    # A verified empirical result should carry its reproduction, unjudged.
    ins = doss.get("insula-rois-responded-more-low")
    assert ins and "validated_by" in warrant.fired_keys(ins)
    # No warrant/level is written into the dossier — it is data, not judgement.
    assert "warrant" not in alt and "level" not in alt


def test_resolving_the_tree_stays_inside_each_role_s_vocabulary():
    floor = warrant.resolve(PAPER)
    assert floor, "resolve returned nothing"
    for slug, f in floor.items():
        role, stance = f["dossier"]["role"], f["dossier"]["stance"]
        assert f["level"] in warrant.vocabulary_for(role, stance), \
            f"{slug} ({role}) resolved to {f['level']}, outside its vocabulary"


def test_the_corpus_mismatch_resolves_contested_where_the_tree_holds_it():
    """The note's single fact, checked where the corpus actually holds the `mismatch`."""
    paper = "ejdrup-2026-dopamine"
    if not os.path.isdir(os.path.join(warrant.CLAIMS_DIR, paper)):
        return  # a checkout without the private tree cannot exercise it
    floor = warrant.resolve(paper)
    hits = [s for s, f in floor.items()
            if any(r.get("status") == "mismatch" for r in f["dossier"]["reproductions"])]
    for s in hits:
        assert floor[s]["level"] == "contested", f"{s} holds a mismatch but resolved {floor[s]['level']}"


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
