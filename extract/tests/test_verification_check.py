"""The verification-check layer: the verdict rule, and the runner that writes it beside warrant.

The check is mechanical — precedence over the reproduction records a claim carries and the
provenance the audited run wrote — so it is tested without a model and without the corpus: the
rule on synthetic evidence, and the runner on a claim tree built under a temporary root. What is
pinned is that each verdict follows from its evidence, that `mismatch` wins over a blocked record
on the same claim (the dopamine case), and that the runner lands on its declared path and writes
`check_verification:` while leaving `warrant:` untouched.

Runs under pytest (``pytest tests/test_verification_check.py``) or standalone
(``python tests/test_verification_check.py``).
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

# Standalone puts tests/ on the path and not the package beside it; test the tree you stand in.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import yaml

from elife_extract import cli, layers, verification_check as vc
from elife_extract.config import Config

SLUG = "p"
DECL = Path(__file__).resolve().parents[2] / "pipeline" / "layers.yaml"


def _cfg(root: Path) -> Config:
    return Config.from_args(cli.build_parser().parse_args(
        ["verification-check", "--paper", SLUG, "--root", str(root)]))


def _declaration() -> dict:
    return {l["id"]: l for l in yaml.safe_load(DECL.read_text())["layers"]}


# ── the verdict rule ──────────────────────────────────────────────────────


def test_reproduced_needs_a_verified_record_and_a_measured_run():
    """`reproduced` is a verified record whose provenance shows the script ran and measured it."""
    prov = {"claim": "x", "status": "PASS", "measured": True}
    assert vc.verdict([{"status": "verified"}], prov)[0] == "reproduced"


def test_a_verified_record_without_a_measured_run_is_only_partial():
    """Verified but not observed running (no provenance, or a recalled value) is `partial`, not
    `reproduced` — the ruling ties `reproduced` to provenance that shows the script ran."""
    assert vc.verdict([{"status": "verified"}], None)[0] == "partial"
    recalled = {"claim": "x", "status": "PASS", "measured": False}
    assert vc.verdict([{"status": "verified"}], recalled)[0] == "partial"


def test_mismatch_from_a_record_and_from_a_failed_run():
    assert vc.verdict([{"status": "mismatch"}], None)[0] == "mismatch"
    assert vc.verdict([], {"claim": "x", "status": "FAIL", "measured": True})[0] == "mismatch"


def test_mismatch_wins_over_blocked_on_the_same_claim():
    """The dopamine dSTORM claim carries a blocked record and a mismatch record; the reader must
    see the mismatch, so the more adverse verdict wins."""
    records = [{"status": "blocked"}, {"status": "mismatch"}]
    assert vc.verdict(records, None)[0] == "mismatch"


def test_blocked_unattempted_and_unrecorded():
    assert vc.verdict([{"status": "blocked"}], None)[0] == "blocked"
    assert vc.verdict([{"status": "unattempted"}], None)[0] == "unattempted"
    assert vc.verdict([], None)[0] == "unrecorded"
    assert vc.verdict(None, None)[0] == "unrecorded"


def test_partial_record_and_a_ran_but_unmeasured_provenance():
    assert vc.verdict([{"status": "partial"}], None)[0] == "partial"
    assert vc.verdict([], {"claim": "x", "status": "WARN", "measured": False})[0] == "partial"


def test_from_lists_every_record_status_and_the_provenance_read():
    _, fired = vc.verdict([{"status": "blocked"}, {"status": "mismatch"}],
                          {"claim": "x", "status": "PASS", "measured": True})
    assert "record:blocked" in fired and "record:mismatch" in fired
    assert "provenance:PASS measured" in fired


# ── the runner, under a temporary root ────────────────────────────────────


def _seed(cfg: Config, claims: dict[str, list[dict]], prov: dict | None = None) -> Path:
    """A claim tree of `{slug: reproductions}` and an optional provenance file, under the root."""
    d = cfg.corpus_dir / SLUG
    d.mkdir(parents=True, exist_ok=True)
    for slug, reps in claims.items():
        block = yaml.safe_dump({"reproductions": reps or []}, sort_keys=False,
                               allow_unicode=True).rstrip("\n")
        (d / f"{slug}.md").write_text(
            f"---\nslug: {slug}\nrole: empirical\nepistemic: moderate\nclaim: {slug}\n"
            f"{block}\n---\n\nBody.\n", encoding="utf-8")
    if prov is not None:
        pv = cfg.root / "verification" / SLUG
        pv.mkdir(parents=True, exist_ok=True)
        (pv / "provenance.json").write_text(json.dumps(prov), encoding="utf-8")
    return d


def test_runner_writes_its_declared_path():
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        _seed(cfg, {"a": [{"status": "verified"}]})
        path, payload = layers.verification_check_layer(SLUG, cfg)
        declared = _declaration()["verification-check"]["produces"][0].replace("{paper}", SLUG)
        assert path == cfg.root / declared
        assert json.loads(path.read_text())["checks"][0]["slug"] == "a"


def test_runner_writes_check_verification_and_leaves_warrant_untouched():
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        d = _seed(cfg, {
            "reproduced-claim": [{"status": "verified"}],
            "dstorm": [{"status": "blocked"}, {"status": "mismatch"}],
            "untried": [],
        }, prov={"paper": SLUG, "results": [
            {"claim": "reproduced-claim", "status": "PASS", "measured": True}]})
        # A claim already carrying a warrant: the check must sit beside it, not replace it.
        (d / "reproduced-claim.md").write_text(
            (d / "reproduced-claim.md").read_text().replace(
                "epistemic: moderate\n", "epistemic: moderate\nwarrant: strong\n"))

        layers.verification_check_layer(SLUG, cfg)

        got = {p.stem: layers._read_frontmatter(p) for p in d.glob("*.md")}
        assert got["reproduced-claim"]["check_verification"] == "reproduced"
        assert got["reproduced-claim"]["warrant"] == "strong", "the check overwrote the warrant"
        assert got["dstorm"]["check_verification"] == "mismatch"
        assert got["untried"]["check_verification"] == "unrecorded"
        assert "record:verified" in got["reproduced-claim"]["check_verification_from"]


def test_runner_is_idempotent():
    """A second run produces the same frontmatter — the write replaces, it does not accumulate."""
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        d = _seed(cfg, {"a": [{"status": "partial"}]})
        layers.verification_check_layer(SLUG, cfg)
        once = (d / "a.md").read_text()
        layers.verification_check_layer(SLUG, cfg)
        assert (d / "a.md").read_text() == once


def test_declared_command_names_a_real_subcommand():
    choices = set(cli.build_parser()._subparsers._group_actions[0].choices)
    assert "verification-check" in choices
    decl = _declaration()["verification-check"]
    assert decl.get("title") and "elife_extract.cli verification-check" in decl["command"]


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
