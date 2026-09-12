"""Model profiles and the evaluation report (#85).

Two contracts are pinned here. First, that `--profile` resolves to exactly the models, prompt
variant, chunking, output enforcement and effort the issue's table says — and that an unknown
profile fails rather than silently falling back to a default. Second, that the evaluation
report aggregates the scorecards under runs/<paper>/evaluation/ into one row per (paper,
profile), so the layer's output is a function of the scorecards it reads.

No LLM and no network. Runs under pytest or standalone.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from elife_extract import cli
from elife_extract.config import (
    Config, PROFILES, PROFILE_NAMES, resolve_profile, _backend_model,
)

REPO = Path(__file__).resolve().parents[2]


def _cfg(*args) -> Config:
    return Config.from_args(cli.build_parser().parse_args(list(args)))


# ── profile resolution ────────────────────────────────────────────────────


def test_each_profile_yields_the_models_the_table_says():
    """On a backend with no override (anthropic), each profile resolves to its logical ids."""
    expect = {
        "frontier": ("claude-opus-5", "claude-opus-5"),
        "standard": ("claude-sonnet-5", "claude-opus-5"),
        "open":     ("deepseek-chat", "deepseek-chat"),
        "subagent": ("claude-sonnet-5", "claude-opus-5"),
    }
    for name, (readers, reasoner) in expect.items():
        c = _cfg("results-reader", "--paper", "x", "--profile", name, "--backend", "anthropic")
        assert c.model_results == readers, f"{name} readers"
        assert c.model_caption == readers, f"{name} caption"
        assert c.model_structure == readers, f"{name} structure"
        assert c.model_reconcile == reasoner, f"{name} reconcile"


def test_each_profile_yields_the_flags_the_table_says():
    """Variant, chunking, output enforcement, effort and thinking follow the profile."""
    c = _cfg("results-reader", "--paper", "x", "--profile", "frontier", "--backend", "anthropic")
    assert c.prompt_variant == "frontier"
    assert c.output_format == "json_schema"
    assert (c.reader_effort, c.reasoner_effort) == ("high", "xhigh")
    assert c.thinking is True and c.per_arc is False

    o = _cfg("results-reader", "--paper", "x", "--profile", "open", "--backend", "anthropic")
    assert o.prompt_variant == "open"
    assert o.per_arc is True and o.per_figure_captions is True
    assert o.output_format == "json_object" and o.thinking is False

    s = _cfg("results-reader", "--paper", "x", "--profile", "subagent", "--backend", "anthropic")
    assert s.prompt_variant == "default"
    assert s.output_format == "none"          # answered elsewhere; nothing to enforce


def test_effort_follows_the_reader_reasoner_split():
    c = _cfg("results-reader", "--paper", "x", "--profile", "frontier", "--backend", "anthropic")
    assert c.effort_for("results-reader") == "high"           # a reader
    assert c.effort_for("reconciler") == "xhigh"              # a synthesis step
    assert c.effort_for("edge-inference.arc2") == "xhigh"     # edge labels are reasoner


def test_the_vertex_backend_pins_the_older_generation():
    """The Vertex project serves 4.6, not 5, so the current-generation ids map to 4.6 there."""
    assert _backend_model("vertex", "claude-opus-5") == "claude-opus-4-6"
    assert _backend_model("vertex", "claude-sonnet-5") == "claude-sonnet-4-6"
    assert _backend_model("anthropic", "claude-opus-5") == "claude-opus-5"
    c = _cfg("results-reader", "--paper", "x", "--profile", "standard", "--backend", "vertex")
    assert c.model_results == "claude-sonnet-4-6"
    assert c.model_reconcile == "claude-opus-4-6"


def test_an_explicit_model_overrides_the_profile():
    c = _cfg("results-reader", "--paper", "x", "--profile", "frontier",
             "--backend", "anthropic", "--model-results", "my-model")
    assert c.model_results == "my-model"          # CLI arg beats the profile
    assert c.model_reconcile == "claude-opus-5"   # the rest still from the profile


def test_no_profile_uses_the_current_generation_defaults():
    c = _cfg("results-reader", "--paper", "x", "--backend", "anthropic")
    assert c.model_results == "claude-sonnet-5"
    assert c.model_reconcile == "claude-opus-5"
    assert c.prompt_variant == "default"


def test_an_unknown_profile_fails():
    """resolve_profile raises, and a Config carrying an unknown profile reports it."""
    try:
        resolve_profile("bogus")
        raise AssertionError("resolve_profile should have raised on an unknown profile")
    except ValueError as e:
        assert "bogus" in str(e)
    # argparse rejects it at parse time for a model-answered subcommand …
    try:
        _cfg("results-reader", "--paper", "x", "--profile", "bogus")
        raise AssertionError("argparse should reject an unknown --profile choice")
    except SystemExit:
        pass
    # … and validate() catches it when the field is set another way.
    ns = cli.build_parser().parse_args(["results-reader", "--paper", "x", "--backend", "anthropic"])
    ns.profile = "bogus"
    errs = Config.from_args(ns).validate()
    assert any("profile" in e and "bogus" in e for e in errs)


def test_the_committed_variant_dirs_exist_for_the_profiles_that_declare_them():
    """frontier overrides the three reader tasks; open overrides the caption task. The loader
    inherits the contract, so the variant dirs need only the task files that differ."""
    fr = REPO / "extract" / "prompts" / "frontier"
    assert (fr / "results-reader.md").is_file()
    assert (fr / "caption-reader.md").is_file()
    assert (fr / "structure-reader.md").is_file()
    op = REPO / "extract" / "prompts" / "open"
    assert (op / "caption-reader.md").is_file()


# ── the evaluation report ──────────────────────────────────────────────────


def _load_report():
    p = REPO / "scripts" / "evaluation_report.py"
    spec = importlib.util.spec_from_file_location("evaluation_report", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _card(profile: str, n_ref: int, n_cli: int, n_recovered: int) -> dict:
    return {
        "profile": profile, "paper_slug": "p", "reference": "claim-tree v1 (committed)",
        "n_ref": n_ref, "n_cli": n_cli, "n_recovered": n_recovered,
        "n_cli_matched": n_recovered, "n_role_match": n_recovered, "n_panel_match": 0,
        "n_ref_edges_on_matched": 0, "n_edge_recovered": 0, "n_cli_parts": 0,
    }


def test_the_report_aggregates_two_scorecards_into_one_row_each():
    mod = _load_report()
    with tempfile.TemporaryDirectory() as tmp:
        runs = Path(tmp) / "runs" / "p" / "evaluation"
        runs.mkdir(parents=True)
        (runs / "subagent.scorecard.json").write_text(json.dumps(_card("subagent", 33, 63, 25)))
        (runs / "fourth-reading.scorecard.json").write_text(
            json.dumps(_card("fourth-reading", 33, 34, 27)))
        mod.RUNS = str(Path(tmp) / "runs")

        data = mod.build(["p"])
        by = {r["profile"]: r for r in data["rows"]}

        # One row per scorecard, with recovery computed from the counts.
        assert by["subagent"]["status"] == "scored"
        assert by["subagent"]["recovery"] == round(25 / 33 * 100)
        assert by["fourth-reading"]["recovery"] == round(27 / 33 * 100)
        assert by["subagent"]["reference"] == "claim-tree v1 (committed)"

        # The canonical profiles with no scorecard are shown as not-run, so the table names
        # what a paid backend would fill rather than omitting it.
        assert by["frontier"]["status"] == "not run"
        assert by["frontier"]["note"] == "no backend credit"
        assert data["n_scored"] == 2


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
