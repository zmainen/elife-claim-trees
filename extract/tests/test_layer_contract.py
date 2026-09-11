"""The contract between this CLI and pipeline/layers.yaml.

A layer runner is only useful if it reads and writes the paths its declaration names: that is
what lets `scripts/pipeline.py run` hash what a run read and produced, and it is exactly what
the old shape got wrong. `extract` did five layers' work in one process and wrote
`out/draft-<slug>.json`, which no layer declares — so the ledger recorded hashes of files the
runner had never produced, and the graph described a chain it could not execute.

These tests pin the contract rather than the computation. No LLM and no network: the model
calls are stubbed, and what is checked is that each runner lands on its declared path, that
the declaration's commands name subcommands that exist, and that a layer reads its
predecessor's output instead of recomputing it.

Runs under pytest (``pytest tests/test_layer_contract.py``) or standalone
(``python tests/test_layer_contract.py``).
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
from dataclasses import asdict
from pathlib import Path
from unittest import mock

# Standalone (`python tests/test_layer_contract.py`) puts tests/ on the path and not the
# package beside it, so an `elife_extract` installed from some other checkout wins. Test the
# tree you are standing in. pytest already does this via rootdir.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import yaml

from elife_extract import agents as agents_mod
from elife_extract import cli, layers
from elife_extract import reconcile as reconcile_mod
from elife_extract.config import Config
from elife_extract.prepare import PreparedPaper
from elife_extract.schema import AgentExtraction, CandidateClaim, DraftClaimTable

SLUG = "gadeke-2026-guilt-insula"
DOI = "10.7554/eLife.105391"
DECL = Path(__file__).resolve().parents[2] / "pipeline" / "layers.yaml"


def _declaration() -> dict:
    return {l["id"]: l for l in yaml.safe_load(DECL.read_text())["layers"]}


def _cfg(root: Path) -> Config:
    return Config.from_args(cli.build_parser().parse_args(
        ["prepare", "--paper", SLUG, "--root", str(root)]))


def _paper() -> PreparedPaper:
    return PreparedPaper(
        doi=DOI, article_id="105391", paper_slug=SLUG, title="A paper", authors=["G"],
        abstract="a" * 400, results_text="r" * 400, captions_text="c" * 400,
        methods_text="m" * 400, extraction_path="jats",
    )


def _candidate() -> CandidateClaim:
    return CandidateClaim(claim="The insula responds to guilt.", panel="fig1a",
                          claim_type="empirical", role="empirical",
                          evidence="Insula activity increased.", confidence="high")


def _extraction(agent: str) -> AgentExtraction:
    return AgentExtraction(agent=agent, paper_slug=SLUG, model="stub-model",
                           claims=[_candidate()])


def _draft(n: int = 1) -> DraftClaimTable:
    return DraftClaimTable(
        paper_slug=SLUG, paper_doi=DOI, paper_title="A paper",
        per_agent_counts={"results": n},
        claims=[{"claim": f"Claim {i}.", "panel": "fig1a", "claim_type": "empirical",
                 "role": "empirical", "confidence": "high", "sources": ["results"]}
                for i in range(n)],
    )


def _seed_prepared(root: Path, cfg: Config) -> None:
    layers._write_json(layers.run_file(SLUG, "prepared.json", cfg), asdict(_paper()))


# ── the declaration and the CLI agree ────────────────────────────────────


def test_every_declared_command_names_a_real_subcommand():
    """A layer whose command names a subcommand this CLI does not have cannot run.

    `pipeline.py run` shells out to the string in `command:`; nothing checks it first, so a
    renamed subcommand would surface as a layer that fails at the moment someone needs it.
    """
    choices = set(cli.build_parser()._subparsers._group_actions[0].choices)
    for lid, layer in _declaration().items():
        cmd = layer.get("command") or ""
        m = re.search(r"elife_extract\.cli\s+([a-z-]+)", cmd)
        if m:
            assert m.group(1) in choices, f"{lid}: command names missing subcommand {m.group(1)!r}"


def test_induction_layers_all_have_runners():
    """The five layers `pipeline.py run` used to refuse, and the two added with them.

    Every one of these answered "no runner declared — skipping" and returned 3, which is the
    whole reason the graph could describe induction but never execute it.
    """
    decl = _declaration()
    for lid in ("prepare", "results-reader", "caption-reader", "structure-reader",
                "reconcile", "external-review", "edge-inference"):
        assert decl[lid].get("command"), f"{lid} still has no runner"


def test_model_answered_layers_declare_where_to_find_the_model():
    """`by_from` is how the ledger stops recording `scripts/pipeline.py run` as the author.

    Every layer a model answers must say where in its output the model is named, or the run
    record credits the runner for work a model did.
    """
    decl = _declaration()
    for lid in ("results-reader", "caption-reader", "structure-reader", "reconcile",
                "external-review", "edge-inference", "questions"):
        assert decl[lid].get("by_from") == "model", f"{lid} does not declare by_from"


# ── each runner lands on its declared path ───────────────────────────────


def test_prepare_writes_its_declared_path_and_reads_back():
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        root = cfg.root
        # `layers` binds prepare at import, so the patch has to land there rather than on
        # the module it came from — otherwise the real fetcher runs off its cache.
        with mock.patch.object(layers, "prepare", return_value=_paper()):
            path = layers.prepare_layer(SLUG, cfg, doi=DOI)

        declared = _declaration()["prepare"]["produces"][0].replace("{paper}", SLUG)
        assert path == root / declared, f"prepare wrote {path}, declaration says {declared}"

        back = layers.read_prepared(SLUG, cfg)
        assert back.doi == DOI and back.paper_slug == SLUG
        assert len(back.results_text) == 400, "the slice the readers get did not survive"


def test_each_reader_writes_its_declared_path():
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        root = cfg.root
        _seed_prepared(root, cfg)
        decl = _declaration()
        for agent in ("results", "caption", "structure"):
            with mock.patch.object(agents_mod, "run_agent", return_value=_extraction(agent)):
                path, extraction = layers.reader_layer(agent, SLUG, cfg)
            declared = decl[f"{agent}-reader"]["produces"][0].replace("{paper}", SLUG)
            assert path == root / declared
            assert json.loads(path.read_text())["model"] == "stub-model", \
                "the reader's output does not name the model, so by_from reads nothing"


def test_reconcile_reads_the_three_readers_from_disk():
    """Reconciliation's inputs are files now, not values passed inside one process."""
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        root = cfg.root
        _seed_prepared(root, cfg)
        for agent in ("results", "caption", "structure"):
            layers._write_json(layers.run_file(SLUG, layers.READER_OUTPUT[agent], cfg),
                               json.loads(_extraction(agent).model_dump_json()))

        seen = {}

        def fake_reconcile(results, caption, structure, cfg, **kw):
            seen["agents"] = [results.agent, caption.agent, structure.agent]
            return _draft()

        with mock.patch.object(reconcile_mod, "reconcile", fake_reconcile):
            path, draft = layers.reconcile_layer(SLUG, cfg)

        assert seen["agents"] == ["results", "caption", "structure"]
        declared = _declaration()["reconcile"]["produces"][0].replace("{paper}", SLUG)
        assert path == root / declared
        assert json.loads(path.read_text())["model"], "the draft does not name the model"


def test_reconcile_says_which_layer_has_not_run():
    """A missing input names the layer that produces it, not just a path that is not there."""
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        _seed_prepared(Path(tmp), cfg)
        try:
            layers.reconcile_layer(SLUG, cfg)
        except SystemExit as e:
            assert "results-reader" in str(e)
        else:
            assert False, "reconcile did not complain about the missing reader"


# ── what a downstream layer builds on ────────────────────────────────────


def test_best_draft_prefers_external_review_and_falls_back():
    """claim-tree declares both; external review is absent for nine of the ten papers."""
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        layers._write_json(layers.run_file(SLUG, "reconciler.output.json", cfg),
                           json.loads(_draft(2).model_dump_json()))
        draft, source = layers.best_draft(SLUG, cfg)
        assert source == "reconcile" and len(draft.claims) == 2

        layers._write_json(layers.run_file(SLUG, "external-review.output.json", cfg),
                           json.loads(_draft(5).model_dump_json()))
        draft, source = layers.best_draft(SLUG, cfg)
        assert source == "external-review" and len(draft.claims) == 5


def test_claim_tree_reads_edges_rather_than_re_inferring_them():
    """write_claim_files used to call infer_edges itself — a second paid call for an answer
    the edge-inference layer had already written to disk."""
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        layers._write_json(layers.run_file(SLUG, "edge-inference.output.json", cfg),
                           {"paper_slug": SLUG, "model": "stub", "edges": [{"a": 1}]})
        assert layers.read_edges(SLUG, cfg) == [{"a": 1}]

        from elife_extract import write as write_mod
        with mock.patch.object(write_mod, "resolve_edges") as resolver:
            write_mod.write_claim_files(_draft(2), cfg, edges=[])
            resolver.assert_not_called()


def test_read_edges_tolerates_the_bare_array_the_first_runs_wrote():
    """Gädeke's committed edge output is a bare JSON list, written before the layer existed."""
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        p = layers.run_file(SLUG, "edge-inference.output.json", cfg)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps([{"source": 1, "target": 3}]))
        assert layers.read_edges(SLUG, cfg) == [{"source": 1, "target": 3}]


def test_root_is_what_the_paths_resolve_against():
    """--root, not the working directory, decides where a layer's output lands."""
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        assert cfg.root == Path(tmp).resolve()
        assert cfg.corpus_dir == Path(tmp).resolve() / "claims"
        assert layers.run_file(SLUG, "prepared.json", cfg) == \
            Path(tmp).resolve() / "runs" / SLUG / "prepared.json"


def test_prompts_dir_flag_is_honored():
    """--prompts-dir was accepted and then ignored once; Config must respect it."""
    with tempfile.TemporaryDirectory() as tmp:
        args = cli.build_parser().parse_args(
            ["reconcile", "--paper", SLUG, "--prompts-dir", tmp])
        assert Config.from_args(args).prompts_dir == Path(tmp).resolve()


def test_the_retired_subcommands_are_gone():
    """`extract` and `run` duplicated pipeline.py run without writing a ledger."""
    for gone in ("extract", "run"):
        try:
            cli.build_parser().parse_args([gone, "--doi", DOI])
        except SystemExit as e:
            assert e.code == 2
        else:
            assert False, f"{gone} still parses"


# ── any layer a model answers can be answered by something else ──────────


def test_every_model_answered_layer_can_be_dumped_and_answered():
    """The seam `edge-inference` has always had, on all six.

    A layer whose only route in is the configured backend is a layer that stops when the
    provider does — which is how one Gädeke run lost its edges while every other stage
    succeeded. `--dump-prompt` asks for the question; `--answer` supplies the reply, through
    the same validation a backend reply gets.
    """
    choices = cli.build_parser()._subparsers._group_actions[0].choices
    for name in ("results-reader", "caption-reader", "structure-reader",
                 "reconcile", "external-review", "edge-inference", "questions"):
        opts = {o for a in choices[name]._actions for o in a.option_strings}
        assert "--dump-prompt" in opts, f"{name} cannot be asked for its prompt"
        assert "--answer" in opts, f"{name} cannot be given an answer"


def test_a_supplied_reader_answer_is_validated_and_attributed():
    """A supplied answer goes through the same parse, and records where it came from."""
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        _seed_prepared(cfg.root, cfg)
        ans = Path(tmp) / "a.json"
        ans.write_text(json.dumps([{
            "claim": "The insula responds to guilt.", "panel": "fig1a",
            "claim_type": "empirical", "role": "empirical",
            "evidence": "Insula activity increased.", "confidence": "high"}]))

        path, ex = layers.reader_layer("results", SLUG, cfg, answer=str(ans))
        assert len(ex.claims) == 1
        # The ledger reads `model` out of this file; it must say an answer was supplied
        # rather than name a model that never ran.
        assert json.loads(path.read_text())["model"].startswith("supplied:")


def test_a_supplied_answer_that_is_not_valid_is_refused():
    """Validation is not skipped because the answer came from outside the backend."""
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        _seed_prepared(cfg.root, cfg)
        ans = Path(tmp) / "bad.json"
        ans.write_text(json.dumps([{"claim": "too short"}]))   # missing required fields
        try:
            layers.reader_layer("results", SLUG, cfg, answer=str(ans))
        except Exception:
            pass
        else:
            assert False, "an invalid supplied answer was accepted"


def test_the_dumped_prompt_is_the_one_the_layer_would_send():
    """Dumping must not build a different question from the one the backend gets."""
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        _seed_prepared(cfg.root, cfg)
        from elife_extract.agents import build_reader_request, slice_for_agent, load_prompt
        system, user = layers.reader_request("results", SLUG, cfg)
        paper = layers.read_prepared(SLUG, cfg)
        assert system == load_prompt("results", cfg)
        assert user == slice_for_agent("results", paper)


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
