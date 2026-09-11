"""Tests for the precision, edge recovery, approved-reference lookup and pairs-format
tolerance added by feat/evaluate-precision-and-edges.

No LLM and no network. Runs under pytest or standalone.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

# Standalone puts tests/ on the path — test the tree we are standing in.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from elife_extract.evaluate import (
    Claim,
    _build_scorecard,
    _normalize_pairs,
    _score_edges,
    find_approved_tree,
    load_claims,
    load_edges,
    score_from_precomputed_pairs,
)


# ── helpers ───────────────────────────────────────────────────────────────


def _write_claim(d: Path, slug: str, role: str = "empirical",
                 panel: str | None = None, edges: dict | None = None,
                 part_of: list[str] | None = None) -> Path:
    """Write a minimal claim file."""
    lines = ["---", f"slug: {slug}", f"role: {role}",
             f"claim: The {slug} result."]
    if panel:
        lines += [f"panel: {panel}", "assertions:",
                  f"  - paper-slug: test", f"    panel: {panel}"]
    if edges:
        for rel, targets in edges.items():
            lines.append(f"{rel}:")
            for t in targets:
                lines.append(f"  - {t}")
    if part_of:
        lines.append("part-of:")
        for w in part_of:
            lines.append(f"  - {w}")
    lines.append("---")
    p = d / f"{slug}.md"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


# ── precision ─────────────────────────────────────────────────────────────


def test_precision_counts_unique_cli_matches():
    """n_cli_matched is the number of distinct CLI claims matched to any ref claim."""
    ref_claims = [
        Claim("r1", "ref one", None, "empirical"),
        Claim("r2", "ref two", None, "empirical"),
        Claim("r3", "ref three", None, "empirical"),
    ]
    # c1 matches r1, c2 matches r2; c3 and c4 are unmatched extras.
    cli_claims = [
        Claim("c1", "cli one", None, "empirical"),
        Claim("c2", "cli two", None, "empirical"),
        Claim("c3", "cli extra", None, "empirical"),
        Claim("c4", "cli extra2", None, "empirical"),
    ]
    matches = [
        {"ref_slug": "r1", "cli_slug": "c1", "match_quality": "exact",
         "panel_match": True, "role_match": True},
        {"ref_slug": "r2", "cli_slug": "c2", "match_quality": "partial",
         "panel_match": "n/a", "role_match": True},
        {"ref_slug": "r3", "cli_slug": None, "match_quality": "none",
         "panel_match": "n/a", "role_match": "n/a"},
    ]

    with tempfile.TemporaryDirectory() as tmp:
        ref_dir = Path(tmp) / "ref"
        cli_dir = Path(tmp) / "cli"
        ref_dir.mkdir(); cli_dir.mkdir()
        for c in ref_claims:
            _write_claim(ref_dir, c.slug, c.role)
        for c in cli_claims:
            _write_claim(cli_dir, c.slug, c.role)

        sc = _build_scorecard(
            paper_slug="test", paper_doi="", review_mode="test",
            reference="unapproved", cli_dir=str(cli_dir),
            ref_claims=ref_claims, cli_claims=cli_claims, matches=matches,
            ref_dir=ref_dir, cli_dir_path=cli_dir,
        )

    assert sc.n_recovered == 2
    assert sc.n_cli_matched == 2   # c1 and c2
    assert sc.n_cli == 4
    assert abs(sc.precision_pct - 50.0) < 0.1


def test_precision_parts_tally():
    """n_cli_parts counts CLI claims that carry a part-of relation."""
    with tempfile.TemporaryDirectory() as tmp:
        ref_dir = Path(tmp) / "ref"
        cli_dir = Path(tmp) / "cli"
        ref_dir.mkdir(); cli_dir.mkdir()

        _write_claim(ref_dir, "r1", "empirical")
        _write_claim(cli_dir, "c1", "empirical")
        _write_claim(cli_dir, "c2", "empirical", part_of=["c1"])  # a part

        ref_claims = load_claims(ref_dir, "ref")
        cli_claims = load_claims(cli_dir, "cli")
        matches = [{"ref_slug": "r1", "cli_slug": "c1", "match_quality": "exact",
                    "panel_match": "n/a", "role_match": True}]

        sc = _build_scorecard(
            paper_slug="test", paper_doi="", review_mode="test",
            reference="unapproved", cli_dir=str(cli_dir),
            ref_claims=ref_claims, cli_claims=cli_claims, matches=matches,
            ref_dir=ref_dir, cli_dir_path=cli_dir,
        )

    assert sc.n_cli_parts == 1
    assert sc.n_cli == 2
    assert sc.n_cli_matched == 1


# ── edge recovery ─────────────────────────────────────────────────────────


def test_edge_recovery_basic():
    """_score_edges returns correct counts for a small synthetic graph.

    ref graph:  r1 -tests-> r2  (both in matched pairs → 1 ref edge on matched)
                r1 -supports-> r3  (r3 not in pairs → edge not counted)
    cli graph:  c1 -tests-> c2  (recovers r1→r2 via the pair r1↔c1, r2↔c2)
                c1 -supports-> c2  (extra CLI edge on matched pair)
    """
    ref_claims = [Claim("r1", "h", None, "hypothesis"),
                  Claim("r2", "e", None, "empirical"),
                  Claim("r3", "s", None, "scope")]
    cli_claims = [Claim("c1", "h", None, "hypothesis"),
                  Claim("c2", "e", None, "empirical"),
                  Claim("c3", "x", None, "empirical")]

    matches = [
        {"ref_slug": "r1", "cli_slug": "c1", "match_quality": "exact",
         "panel_match": "n/a", "role_match": True},
        {"ref_slug": "r2", "cli_slug": "c2", "match_quality": "exact",
         "panel_match": "n/a", "role_match": True},
        {"ref_slug": "r3", "cli_slug": None, "match_quality": "none",
         "panel_match": "n/a", "role_match": "n/a"},
    ]

    with tempfile.TemporaryDirectory() as tmp:
        ref_dir = Path(tmp) / "ref"
        cli_dir = Path(tmp) / "cli"
        ref_dir.mkdir(); cli_dir.mkdir()

        # ref: r1 tests r2; r1 supports r3
        _write_claim(ref_dir, "r1", "hypothesis", edges={"tests": ["r2"], "supports": ["r3"]})
        _write_claim(ref_dir, "r2", "empirical")
        _write_claim(ref_dir, "r3", "scope")

        # cli: c1 tests c2 (recovered); c1 supports c2 (extra)
        _write_claim(cli_dir, "c1", "hypothesis", edges={"tests": ["c2"], "supports": ["c2"]})
        _write_claim(cli_dir, "c2", "empirical")
        _write_claim(cli_dir, "c3", "empirical")

        n_ref, n_rec, n_extra = _score_edges(matches, ref_claims, cli_claims, ref_dir, cli_dir)

    assert n_ref == 1      # r1-tests->r2 is the only ref edge between matched pairs
    assert n_rec == 1      # c1-tests->c2 recovers it
    assert n_extra == 1    # c1-supports->c2 is an extra CLI edge


def test_edge_recovery_no_matched_pairs():
    """When nothing is matched, all edge counts are zero."""
    with tempfile.TemporaryDirectory() as tmp:
        ref_dir = Path(tmp) / "ref"
        cli_dir = Path(tmp) / "cli"
        ref_dir.mkdir(); cli_dir.mkdir()
        _write_claim(ref_dir, "r1", edges={"tests": ["r2"]})
        _write_claim(ref_dir, "r2")
        _write_claim(cli_dir, "c1")
        matches: list[dict] = []
        ref_claims = load_claims(ref_dir, "ref")
        cli_claims = load_claims(cli_dir, "cli")
        n_ref, n_rec, n_extra = _score_edges(matches, ref_claims, cli_claims, ref_dir, cli_dir)
    assert n_ref == 0 and n_rec == 0 and n_extra == 0


# ── approved reference lookup ─────────────────────────────────────────────


def test_find_approved_tree_no_approvals_file():
    """With no approvals.jsonl the committed dir and 'unapproved' are returned."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "runs" / "p").mkdir(parents=True)
        committed = root / "claims" / "p"
        committed.mkdir(parents=True)
        got_dir, status = find_approved_tree("p", root, committed)
    assert got_dir == committed
    assert status == "unapproved"


def test_find_approved_tree_with_approval_no_archive():
    """An approval whose archive dir does not exist falls back to the committed dir."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        runs_p = root / "runs" / "p"
        runs_p.mkdir(parents=True)
        committed = root / "claims" / "p"
        committed.mkdir(parents=True)
        _write_claim(committed, "c1")

        approval = {"layer": "claim-tree", "v": 1, "by": "alice",
                    "when": "2026-09-01T00:00:00Z", "note": ""}
        (runs_p / "approvals.jsonl").write_text(json.dumps(approval) + "\n")

        # No archive dir at runs/p/claim-tree.v1/ — falls back to committed.
        got_dir, status = find_approved_tree("p", root, committed)
    assert got_dir == committed
    assert status == "approved v1"


def test_find_approved_tree_with_archive():
    """When the archive dir exists and has claim files, it is returned."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        runs_p = root / "runs" / "p"
        runs_p.mkdir(parents=True)
        committed = root / "claims" / "p"
        committed.mkdir(parents=True)

        # Build the archive dir (claim-tree.v1/).
        archive = runs_p / "claim-tree.v1"
        archive.mkdir()
        _write_claim(archive, "archived-claim")

        approval = {"layer": "claim-tree", "v": 1, "by": "bob",
                    "when": "2026-09-02T00:00:00Z", "note": ""}
        (runs_p / "approvals.jsonl").write_text(json.dumps(approval) + "\n")

        got_dir, status = find_approved_tree("p", root, committed)
    assert got_dir == archive
    assert status == "approved v1"


def test_find_approved_tree_picks_latest_version():
    """When there are multiple approvals, the one with the highest version wins."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        runs_p = root / "runs" / "p"
        runs_p.mkdir(parents=True)
        committed = root / "claims" / "p"
        committed.mkdir(parents=True)

        # Two archived versions.
        for v in (1, 2):
            arch = runs_p / f"claim-tree.v{v}"
            arch.mkdir()
            _write_claim(arch, f"claim-v{v}")

        lines = [
            json.dumps({"layer": "claim-tree", "v": 1, "by": "x",
                        "when": "2026-09-01T00:00:00Z", "note": ""}),
            json.dumps({"layer": "claim-tree", "v": 2, "by": "y",
                        "when": "2026-09-02T00:00:00Z", "note": ""}),
        ]
        (runs_p / "approvals.jsonl").write_text("\n".join(lines) + "\n")

        got_dir, status = find_approved_tree("p", root, committed)
    assert status == "approved v2"
    assert got_dir == runs_p / "claim-tree.v2"


def test_find_approved_tree_ignores_other_layer_approvals():
    """An approval of a layer other than claim-tree does not count."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        runs_p = root / "runs" / "p"
        runs_p.mkdir(parents=True)
        committed = root / "claims" / "p"
        committed.mkdir(parents=True)

        approval = {"layer": "reconcile", "v": 3, "by": "z",
                    "when": "2026-09-01T00:00:00Z", "note": ""}
        (runs_p / "approvals.jsonl").write_text(json.dumps(approval) + "\n")

        got_dir, status = find_approved_tree("p", root, committed)
    assert got_dir == committed
    assert status == "unapproved"


# ── pairs format tolerance ────────────────────────────────────────────────


def test_normalize_pairs_format_b():
    """Format B [{committed, rerun, note}] is accepted and normalised."""
    pairs_b = [
        {"committed": "r1", "rerun": "c1", "note": "same finding"},
        {"committed": "r2", "rerun": "c2", "note": ""},
    ]
    out = _normalize_pairs(pairs_b)
    assert len(out) == 2
    assert out[0]["ref_slug"] == "r1"
    assert out[0]["cli_slug"] == "c1"
    assert out[0]["match_quality"] == "exact"


def test_normalize_pairs_format_a():
    """Format A {matches:[...]} is accepted unchanged."""
    pairs_a = {"matches": [
        {"ref_slug": "r1", "cli_slug": "c1", "match_quality": "exact",
         "panel_match": True, "role_match": True, "notes": ""},
    ]}
    out = _normalize_pairs(pairs_a)
    assert len(out) == 1
    assert out[0]["ref_slug"] == "r1"
    assert out[0]["match_quality"] == "exact"


def test_score_from_precomputed_pairs_end_to_end():
    """score_from_precomputed_pairs correctly computes recovery, precision and edges
    from a small synthetic dataset using the format-B pairs file."""
    with tempfile.TemporaryDirectory() as tmp:
        ref_dir = Path(tmp) / "ref"
        cli_dir = Path(tmp) / "cli"
        ref_dir.mkdir(); cli_dir.mkdir()

        # ref: r1 tests r2
        _write_claim(ref_dir, "r1", "hypothesis", edges={"tests": ["r2"]})
        _write_claim(ref_dir, "r2", "empirical")

        # cli: c1 tests c2 (recovers), plus c3 unmatched extra
        _write_claim(cli_dir, "c1", "interpretation")   # role mismatch: hypothesis vs interpretation
        _write_claim(cli_dir, "c2", "empirical")
        _write_claim(cli_dir, "c3", "empirical")
        _write_claim(cli_dir, "c1", "interpretation",   # overwrite with edge
                     edges={"tests": ["c2"]})

        pairs_path = Path(tmp) / "pairs.json"
        pairs_path.write_text(json.dumps([
            {"committed": "r1", "rerun": "c1"},   # matched; role will disagree
            {"committed": "r2", "rerun": "c2"},
        ]))

        card = score_from_precomputed_pairs(
            ref_dir=ref_dir, cli_dir=cli_dir, pairs_path=pairs_path,
            paper_slug="test", review_mode="test",
        )

    assert card.n_ref == 2
    assert card.n_cli == 3
    assert card.n_recovered == 2
    assert card.n_cli_matched == 2
    assert abs(card.precision_pct - 200 / 3) < 1   # 2/3 ≈ 66.7%
    assert card.n_ref_edges_on_matched == 1          # r1-tests->r2
    assert card.n_edge_recovered == 1                # c1-tests->c2
    assert card.n_cli_extra_edges == 0
    # r1 is hypothesis, c1 is interpretation — role disagrees
    assert card.n_role_match < 2
    assert "hypothesis→interpretation" in card.role_confusion


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
