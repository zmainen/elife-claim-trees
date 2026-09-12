"""The verdict model: the four refusals, latest-line-wins, a complete skeleton, and
`evaluate score --gold` on a synthetic tree with one strike, one merge and one corrected role.

No LLM and no network. Runs under pytest or standalone (`python tests/test_verdicts.py`).
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

# Standalone puts tests/ on the path — test the tree we are standing in.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from elife_extract import verdicts as vd
from elife_extract.evaluate import score_against_gold


# ── the four refusals ─────────────────────────────────────────────────────

SLUGS = ["a", "b", "c"]
EDGES = [("a", "b", "supports")]


def test_refuses_unknown_slug():
    problems = vd.validate([{"kind": "claim", "slug": "zzz", "verdict": "keep"}],
                           claim_slugs=SLUGS, edge_triples=EDGES)
    assert any("zzz" in p and "not a claim" in p for p in problems)


def test_refuses_part_of_cycle():
    records = [
        {"kind": "claim", "slug": "a", "verdict": "part-of", "target": "b"},
        {"kind": "claim", "slug": "b", "verdict": "part-of", "target": "a"},
    ]
    problems = vd.validate(records, claim_slugs=SLUGS, edge_triples=EDGES)
    assert any("cycle" in p for p in problems)


def test_refuses_merge_into_struck_target():
    records = [
        {"kind": "claim", "slug": "a", "verdict": "merge-into", "target": "b"},
        {"kind": "claim", "slug": "b", "verdict": "strike"},
    ]
    problems = vd.validate(records, claim_slugs=SLUGS, edge_triples=EDGES)
    assert any("merge-into" in p and "struck" in p for p in problems)


def test_refuses_edge_naming_absent_claim():
    records = [{"kind": "edge", "source": "a", "target": "zzz",
                "relation": "supports", "verdict": "ok"}]
    problems = vd.validate(records, claim_slugs=SLUGS, edge_triples=EDGES)
    assert any("zzz" in p and "not a claim" in p for p in problems)


def test_clean_skeleton_has_no_problems():
    records = vd.skeleton(SLUGS, EDGES)
    assert vd.validate(records, claim_slugs=SLUGS, edge_triples=EDGES) == []


# ── latest line wins ───────────────────────────────────────────────────────

def test_latest_line_wins_per_key():
    records = [
        {"kind": "claim", "slug": "a", "verdict": "keep"},
        {"kind": "claim", "slug": "a", "verdict": "strike"},
        {"kind": "edge", "source": "a", "target": "b", "relation": "supports", "verdict": "ok"},
        {"kind": "edge", "source": "a", "target": "b", "relation": "supports", "verdict": "strike"},
        {"kind": "ruling", "question": "q", "answer": "first"},
        {"kind": "ruling", "question": "q", "answer": "second"},
    ]
    res = vd.resolve(records)
    assert res.claims["a"]["verdict"] == "strike"
    assert res.edges[("a", "b", "supports")]["verdict"] == "strike"
    assert res.rulings["q"]["answer"] == "second"


# ── the skeleton is complete ────────────────────────────────────────────────

def test_skeleton_covers_every_claim_and_edge():
    slugs = ["x", "y", "z"]
    edges = [("x", "y", "tests"), ("y", "z", "requires")]
    records = vd.skeleton(slugs, edges)
    # one keep per claim, one ok per edge, all considered: false
    assert sum(1 for r in records if r["kind"] == "claim") == 3
    assert sum(1 for r in records if r["kind"] == "edge") == 2
    assert all(r["considered"] is False for r in records)
    assert all(r["verdict"] in ("keep", "ok") for r in records)
    assert vd.is_complete(records, claim_slugs=slugs, edge_triples=edges)
    # dropping a line makes it incomplete
    assert not vd.is_complete(records[:-1], claim_slugs=slugs, edge_triples=edges)


# ── evaluate score --gold ───────────────────────────────────────────────────

def _write_claim(d: Path, slug: str, role: str, panel: str | None = None,
                 edges: dict | None = None) -> None:
    lines = ["---", f"slug: {slug}", f"role: {role}", f"claim: The {slug} finding."]
    if edges:
        for rel, targets in edges.items():
            lines.append(f"{rel}:")
            for t in targets:
                lines.append(f"  - {t}")
    if panel:
        lines += ["assertions:", "  - paper-slug: synthetic", f"    panel: {panel}"]
    lines.append("---")
    (d / f"{slug}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_score_against_gold_strike_merge_and_role():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        ref = root / "ref"; ref.mkdir()
        cli = root / "cli"; cli.mkdir()

        # Reference tree: r1, r2 (a duplicate of r1), r3 (control), r4 (a bogus claim).
        _write_claim(ref, "r1", "empirical")
        _write_claim(ref, "r2", "empirical")
        _write_claim(ref, "r3", "control")
        _write_claim(ref, "r4", "empirical")
        # Candidate reproduces all four, one-to-one.
        _write_claim(cli, "c1", "empirical")
        _write_claim(cli, "c2", "empirical")
        _write_claim(cli, "c3", "control")
        _write_claim(cli, "c4", "empirical")

        pairs = root / "pairs.json"
        pairs.write_text(
            '{"matches": ['
            '{"ref_slug":"r1","cli_slug":"c1","match_quality":"exact"},'
            '{"ref_slug":"r2","cli_slug":"c2","match_quality":"exact"},'
            '{"ref_slug":"r3","cli_slug":"c3","match_quality":"exact"},'
            '{"ref_slug":"r4","cli_slug":"c4","match_quality":"exact"}]}',
            encoding="utf-8")

        # The reading: r4 is not a claim (strike); r2 is a duplicate of r1 (merge);
        # r3's role is really interpretation, not control (corrected role).
        verdicts = root / "verdicts.jsonl"
        verdicts.write_text("\n".join([
            '{"kind":"claim","slug":"r1","verdict":"keep","considered":true}',
            '{"kind":"claim","slug":"r2","verdict":"merge-into","target":"r1","considered":true}',
            '{"kind":"claim","slug":"r3","verdict":"keep","role":"interpretation","considered":true}',
            '{"kind":"claim","slug":"r4","verdict":"strike","considered":true}',
        ]) + "\n", encoding="utf-8")

        card = score_against_gold(ref, cli, pairs, verdicts, paper_slug="synthetic")

        assert card.n_ref_all == 4
        assert card.n_struck == 1
        assert card.n_merges == 1
        # kept reference claims: r1 (r2 folds in) and r3 → two.
        assert card.n_kept == 2
        assert card.n_recovered == 2
        # precision: c4 reproduced a struck claim, so it does not count as matched.
        assert card.n_cli == 4
        assert card.n_cli_matched == 3
        assert card.n_struck_reproduced == 1
        # role: r1 keeps empirical (c1 matches), r3 corrected to interpretation (c3 is control → miss).
        assert card.n_role_match == 1
        assert card.role_pct == 50.0


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
