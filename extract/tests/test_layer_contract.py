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


def _read_paper() -> PreparedPaper:
    """A paper with real sentences in every reader section and one figure, so the slice the
    results reader gets can be inspected — the inventory line, the Introduction, the Discussion,
    and the span id in front of each sentence."""
    from elife_extract.prepare import FigureCaption
    return PreparedPaper(
        doi=DOI, article_id="105391", paper_slug=SLUG, title="A paper", authors=["G"],
        abstract="Guilt tracks insula activity. We show it here.",
        introduction_text="We asked whether responsibility drives guilt. Prior work found a link.",
        results_text="Participants chose the safe option. Insula activity rose in the guilt condition.",
        discussion_text="These findings suggest a guilt signal. This extends earlier reports.",
        captions_text="Figure 2. Choices. (A) safe choices.",
        methods_text="We recruited forty participants for the task.",
        extraction_path="jats",
        figure_captions=[FigureCaption(figure_num="2", text="Figure 2. Behavioural choices. Panel A shows safe choices.",
                                       panels=["a", "b"], element_id="fig2")],
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
                "external-review", "edge-inference", "questions", "parts",
                "summaries", "synthesis", "abstract-map"):
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


def test_write_replace_archives_the_current_tree_then_writes():
    """--replace moves the current tree to runs/<paper>/claim-tree.v<N>/ before writing anew.

    Without it a non-empty directory is refused: the version being replaced must stay
    addressable as files, since the ledger keeps only its content hash.
    """
    from elife_extract import write as write_mod
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        paper_dir = cfg.corpus_dir / SLUG

        write_mod.write_claim_files(_draft(2), cfg, edges=[])
        first = sorted(p.name for p in paper_dir.glob("*.md"))
        assert "index.md" in first

        # A plain second write is refused rather than clobbering unrecorded work.
        try:
            write_mod.write_claim_files(_draft(3), cfg, edges=[])
        except FileExistsError:
            pass
        else:
            assert False, "a non-empty directory was overwritten without --replace"

        # --replace archives the current tree (v1, no ledger) and writes the new one.
        write_mod.write_claim_files(_draft(3), cfg, edges=[], replace=True)
        archive = cfg.root / "runs" / SLUG / "claim-tree.v1"
        assert archive.is_dir(), "the replaced version was not archived"
        assert sorted(p.name for p in archive.glob("*.md")) == first
        claims_now = [p for p in paper_dir.glob("*.md") if p.name != "index.md"]
        assert len(claims_now) == 3 and (paper_dir / "index.md").is_file()


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
                 "reconcile", "external-review", "edge-inference", "questions", "parts",
                 "summaries", "synthesis", "abstract-map"):
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


# ── Evidence verification ─────────────────────────────────────────────────


def test_evidence_found_normalises_curly_quotes_and_en_dash():
    """Curly quotes and an en dash in the quote match ASCII text."""
    from elife_extract.agents import evidence_found
    quote = "“firing rate decreased from 5.5–0.2 Hz”"
    text  = 'The "firing rate decreased from 5.5-0.2 Hz" after stimulation.'
    assert evidence_found(quote, text)
    assert not evidence_found("completely made up sentence", text)


def test_reader_from_raw_sets_evidence_verified_when_paper_given():
    """One verbatim and one invented quote yield [True, False]; None when no paper."""
    from elife_extract.agents import reader_from_raw

    text_slice = "Insula activity increased during guilt induction."
    raw = json.dumps([
        {"claim": "The insula responds to guilt.", "panel": "fig1a",
         "claim_type": "empirical", "role": "empirical",
         "evidence": "Insula activity increased during guilt induction.",
         "confidence": "high", "notes": None},
        {"claim": "Amygdala showed no change.", "panel": None,
         "claim_type": "empirical", "role": "empirical",
         "evidence": "Amygdala activity was completely unchanged in all conditions.",
         "confidence": "tentative", "notes": None},
    ])
    paper = _paper()  # results_text is "r" * 400 — won't contain either quote

    # With paper supplied: first quote is not in the stub text, second also not
    ex_with = reader_from_raw("results", SLUG, "m", raw, paper)
    assert [c.evidence_verified for c in ex_with.claims] == [False, False]

    # With a paper whose results_text contains the first quote verbatim
    import dataclasses
    rich_paper = dataclasses.replace(paper, results_text=text_slice * 3)
    ex_rich = reader_from_raw("results", SLUG, "m", raw, rich_paper)
    assert ex_rich.claims[0].evidence_verified is True
    assert ex_rich.claims[1].evidence_verified is False

    # Without paper: both None
    ex_none = reader_from_raw("results", SLUG, "m", raw)
    assert all(c.evidence_verified is None for c in ex_none.claims)


def test_reconciled_claim_evidence_verified_has_one_entry_per_reader():
    """draft_from_raw populates evidence_verified from evidence_by_agent."""
    from elife_extract.reconcile import draft_from_raw

    cfg = _cfg(Path(tempfile.mkdtemp()))
    r, c, st = _extraction("results"), _extraction("caption"), _extraction("structure")
    raw = json.dumps({
        "paper_slug": SLUG, "paper_doi": DOI,
        "claims": [{
            "claim": "Insula responds to guilt.", "panel": "fig1a",
            "claim_type": "empirical", "role": "empirical",
            "confidence": "high", "sources": ["results", "caption"],
            "evidence_by_agent": {
                "results": "Insula activity increased during guilt induction.",
                "caption": "completely fabricated caption evidence xyz",
            },
        }],
    })
    import dataclasses
    paper = dataclasses.replace(_paper(),
                                results_text="Insula activity increased during guilt induction." * 5,
                                captions_text="c" * 400)
    draft = draft_from_raw(raw, r, c, st, cfg, DOI, paper=paper)
    ev = draft.claims[0].evidence_verified
    assert set(ev.keys()) == {"results", "caption"}
    assert ev["results"] is True
    assert ev["caption"] is False


# ── Prepare reads the whole paper: spans, inventory, span-cited evidence ──


def test_spans_are_numbered_per_section_in_coverage_uid_format():
    """prepared.json spans match the ids coverage's segmenter produces (`results-026`)."""
    from elife_extract.prepare import _build_spans
    from elife_extract.segment import segment

    paper = _read_paper()
    spans = _build_spans(paper)
    # Every uid is `<section>-<3 digits>`, numbered from 001 within its section.
    for s in spans:
        assert re.fullmatch(r"[a-z]+-\d{3}", s["uid"]), s["uid"]
    intro = [s["uid"] for s in spans if s["section"] == "introduction"]
    assert intro[:2] == ["introduction-001", "introduction-002"]
    # The spans prepare records and the ones coverage segments are the same function's output.
    assert [(s["uid"], s["section"], s["text"]) for s in spans] == \
        [(s.uid, s.section, s.text) for s in segment(paper, include_methods=True)]


def test_results_reader_slice_carries_introduction_discussion_and_the_inventory():
    """The results reader now reads all four prose sections and sees the panels that exist."""
    from elife_extract.agents import slice_for_agent

    sliced = slice_for_agent("results", _read_paper())
    assert "We asked whether responsibility drives guilt." in sliced   # Introduction
    assert "These findings suggest a guilt signal." in sliced          # Discussion
    # One inventory line for the figure, its panel ids and the caption head.
    assert "fig2: fig2a, fig2b — Behavioural choices." in sliced


def test_a_rendered_slice_line_begins_with_its_span_id():
    """Each sentence is prefixed with the id the reader cites in `span`."""
    from elife_extract.agents import slice_for_agent

    sliced = slice_for_agent("results", _read_paper())
    body = [ln for ln in sliced.splitlines() if ln.startswith("[")]
    assert body, "no span-prefixed lines rendered"
    assert re.match(r"^\[[a-z]+-\d{3}\] \S", body[0]), body[0]


def test_evidence_check_accepts_a_quote_against_the_cited_span():
    """A quote verbatim from the cited span verifies, and records that it matched the span."""
    from elife_extract.agents import _spans_by_uid, raw_slice_for_agent, verify_evidence

    paper = _read_paper()
    spans = _spans_by_uid(paper)
    # results-002 is the second Results sentence.
    quote = "Insula activity rose in the guilt condition."
    ok, against = verify_evidence(quote, "results-002", spans,
                                  raw_slice_for_agent("results", paper))
    assert ok and against == "span"
    # No span cited, but the quote is still in the raw slice: verified against the slice.
    ok2, against2 = verify_evidence(quote, None, spans, raw_slice_for_agent("results", paper))
    assert ok2 and against2 == "slice"
    # A fabricated quote verifies against neither.
    ok3, against3 = verify_evidence("totally invented sentence", "results-002", spans,
                                    raw_slice_for_agent("results", paper))
    assert not ok3 and against3 is None


def test_prepared_json_round_trips_spans_introduction_and_discussion():
    """asdict → prepared.json → read_prepared keeps the new fields; old files still load."""
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        paper = _read_paper()
        from elife_extract.prepare import _build_spans
        paper.spans = _build_spans(paper)
        layers._write_json(layers.run_file(SLUG, "prepared.json", cfg), asdict(paper))
        back = layers.read_prepared(SLUG, cfg)
        assert back.introduction_text == paper.introduction_text
        assert back.discussion_text == paper.discussion_text
        assert back.spans and back.spans[0]["uid"].startswith("abstract-")

        # A prepared.json written before this change — no spans/introduction/discussion — loads.
        layers._write_json(layers.run_file(SLUG, "prepared.json", cfg), asdict(_paper()))
        old = layers.read_prepared(SLUG, cfg)
        assert old.introduction_text == "" and old.discussion_text == "" and old.spans == []


# ── parts: the writer resolves it, and the validator refuses the impossible ──


def test_writer_resolves_part_of_to_a_slug_and_drops_unresolvable_text():
    """The reconciler names the whole by sentence; the writer resolves it to the whole's slug
    once every claim has one, and text that resolves to no claim is dropped, not guessed."""
    from elife_extract import write as write_mod
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        draft = DraftClaimTable(
            paper_slug=SLUG, paper_doi=DOI, paper_title="A paper",
            claims=[
                {"claim": "The insula tracks the guilt effect.", "panel": "fig4e",
                 "claim_type": "empirical", "role": "empirical", "confidence": "high",
                 "sources": ["results"]},
                {"claim": "The low-minus-high difference was larger in Social.", "panel": "fig4e",
                 "claim_type": "empirical", "role": "empirical", "confidence": "high",
                 "sources": ["results"],
                 "part_of": "the insula tracks the guilt effect"},      # case/period differ
                {"claim": "An orphan part.", "panel": None,
                 "claim_type": "empirical", "role": "empirical", "confidence": "high",
                 "sources": ["results"], "part_of": "a whole that does not exist"},
            ],
        )
        write_mod.write_claim_files(draft, cfg, edges=[])
        d = cfg.corpus_dir / SLUG
        whole, part, orphan = write_mod._unique_slugs(draft.claims)
        part_fm = yaml.safe_load((d / f"{part}.md").read_text().split("---", 2)[1])
        assert part_fm.get("part-of") == [whole], "resolvable part not linked to the whole's slug"
        orphan_fm = yaml.safe_load((d / f"{orphan}.md").read_text().split("---", 2)[1])
        assert not orphan_fm.get("part-of"), "unresolvable part_of should be dropped, not guessed"


def _seed_tree(cfg: Config, slugs: list[str]) -> None:
    d = cfg.corpus_dir / SLUG
    d.mkdir(parents=True, exist_ok=True)
    for s in slugs:
        (d / f"{s}.md").write_text(f"---\nslug: {s}\nrole: empirical\nclaim: {s}\n---\n")


def test_parts_validator_rejects_cycle_self_edge_and_two_wholes():
    """The parts validator drops a self-edge, a second whole for one part, an edge that would
    close a cycle, and an unknown slug — the four ways a `part-of` answer can be impossible."""
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        _seed_tree(cfg, ["a", "b", "c"])
        raw = {"parts": [
            {"part": "a", "whole": "a"},        # self-edge → dropped
            {"part": "b", "whole": "a"},        # kept: b is part of a
            {"part": "b", "whole": "c"},        # b already has a whole → dropped
            {"part": "a", "whole": "b"},        # a→b would close a→b→a → dropped
            {"part": "c", "whole": "nope"},     # unknown slug → dropped
        ]}
        data = layers._validate_parts(raw, SLUG, cfg)
        assert data["parts"] == [{"part": "b", "whole": "a", "why": ""}]


def test_parts_is_answerable_and_its_declared_command_exists():
    """`parts` can be dumped and answered, and the command its declaration names is a real
    subcommand — the seam every model-answered layer has, on the newest one."""
    choices = cli.build_parser()._subparsers._group_actions[0].choices
    opts = {o for a in choices["parts"]._actions for o in a.option_strings}
    assert "--dump-prompt" in opts and "--answer" in opts
    cmd = _declaration()["parts"]["command"]
    m = re.search(r"elife_extract\.cli\s+([a-z-]+)", cmd)
    assert m and m.group(1) in choices, "parts' command names a subcommand the CLI does not have"


# ── the measures: each lands on its declared site path and records who answered ──


def test_the_measures_write_their_declared_paths_and_record_the_model():
    """summaries, synthesis and abstract-map each land on the site path they declare and each
    records who answered — summaries inside the paper's entry, since the file is one for the
    whole corpus; the other two at the top level. A supplied answer goes through the same
    validation the backend reply would, so an invented slug is dropped rather than written."""
    decl = _declaration()
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        root = cfg.root
        _seed_tree(cfg, ["a", "b"])
        _seed_prepared(root, cfg)
        (root / "site" / "src" / "data").mkdir(parents=True, exist_ok=True)
        (root / "site" / "src" / "data" / "paper-summaries.json").write_text("{}")

        sum_ans = Path(tmp) / "sum.json"
        sum_ans.write_text(json.dumps({"hypotheses": "H.", "claims": "C.", "inferences": "I."}))
        path, _ = layers.summaries_layer(SLUG, cfg, answer=str(sum_ans))
        assert path == root / decl["summaries"]["produces"][0].replace("{paper}", SLUG)
        entry = json.loads(path.read_text())[SLUG]
        assert entry["model"].startswith("supplied:"), "summaries did not record the model in the entry"
        assert entry.get("hypotheses") and not entry.get("subject")

        syn_ans = Path(tmp) / "syn.json"
        syn_ans.write_text(json.dumps({"synthesis": "S.", "traceback": [
            {"sentence": "S.", "claims": ["a", "ghost"], "edges": ["a --supports--> b"]}]}))
        path, _ = layers.synthesis_layer(SLUG, cfg, answer=str(syn_ans))
        assert path == root / decl["synthesis"]["produces"][0].replace("{paper}", SLUG)
        out = json.loads(path.read_text())
        assert out["model"].startswith("supplied:") and out["version"] == 3
        assert out["traceback"][0]["claims"] == ["a"], "an invented traceback slug survived"

        am_ans = Path(tmp) / "am.json"
        am_ans.write_text(json.dumps({
            "sentences": [{"n": 1, "type": "claim", "claims": ["a", "ghost"], "kind": "direct"}],
            "orphanClaims": ["whatever"], "orphanSentences": [9]}))
        path, _ = layers.abstract_map_layer(SLUG, cfg, answer=str(am_ans))
        assert path == root / decl["abstract-map"]["produces"][0].replace("{paper}", SLUG)
        out = json.loads(path.read_text())
        assert out["model"].startswith("supplied:")
        assert out["sentences"][0]["claims"] == ["a"], "an invented mapped slug survived"
        # orphanClaims and orphanSentences are derived from the per-sentence mapping, not trusted.
        assert out["orphanClaims"] == ["b"] and out["orphanSentences"] == []
# ── edge inference: the direction checks, reciprocals, and the why ─────────
# The claims are a minimal arc plus one entertained alternative, so every direction rule has a
# claim that satisfies it and a claim that breaks it. Passed as dicts because a draft claim
# carries no stance today — `edges._stance` defaults to `asserts`, and only an alternative the
# reviewer raised reads `entertains`, which is exactly the one target a `rules-out` may have.

_EDGE_SLUGS = ["h", "p", "e", "c", "s", "e2", "alt"]


def _edge_claims() -> list[dict]:
    return [
        {"role": "hypothesis", "stance": "asserts", "claim": "the hypothesis"},        # 1 h
        {"role": "prediction", "stance": "asserts", "claim": "the prediction"},        # 2 p
        {"role": "empirical", "stance": "asserts", "claim": "the result"},             # 3 e
        {"role": "control", "stance": "asserts", "claim": "the control"},              # 4 c
        {"role": "scope", "stance": "asserts", "claim": "the scope bound"},            # 5 s
        {"role": "empirical", "stance": "asserts", "claim": "another result"},         # 6 e2
        {"role": "hypothesis", "stance": "entertains", "claim": "an alternative"},      # 7 alt
    ]


def _validate(parsed: list, claims: list | None = None) -> list[dict]:
    from elife_extract.edges import _validate_edges
    return _validate_edges(parsed, claims or _edge_claims(), _EDGE_SLUGS, source="test")


def _triples(edges: list[dict]) -> set[tuple[str, str, str]]:
    return {(e["source"], e["target"], e["relation"]) for e in edges}


def test_edge_rejects_unknown_relation_reference_and_self():
    """Three ways a reference or relation is unusable — each dropped, the one valid edge kept."""
    edges = _validate([
        {"source": 3, "target": 2, "relation": "not-a-relation"},   # unknown relation → drop
        {"source": 99, "target": 2, "relation": "tests"},           # index out of range → drop
        {"source": 3, "target": 3, "relation": "supports"},         # self reference → drop
        {"source": 3, "target": 2, "relation": "tests"},            # valid → kept
    ])
    assert _triples(edges) == {("e", "p", "tests")}


def test_edge_rejects_the_mechanically_written_reciprocals():
    """`derived-from` and `confirms` are synthesised, never emitted; emitting them is dropped."""
    edges = _validate([
        {"source": 2, "target": 1, "relation": "derived-from"},
        {"source": 3, "target": 2, "relation": "confirms"},
    ])
    assert edges == []


def test_edge_direction_tests_entails_scopes():
    """`tests` runs empirical/control → prediction; `entails` from a hypothesis; `scopes` from a
    scope claim. The wrong source or target is dropped, the right one kept."""
    edges = _validate([
        {"source": 1, "target": 2, "relation": "tests"},     # source hypothesis → drop
        {"source": 3, "target": 6, "relation": "tests"},     # target empirical → drop
        {"source": 3, "target": 2, "relation": "tests"},     # kept
        {"source": 3, "target": 2, "relation": "entails"},   # source empirical → drop
        {"source": 1, "target": 2, "relation": "entails"},   # kept (+ reciprocal derived-from)
        {"source": 3, "target": 6, "relation": "scopes"},    # source empirical → drop
        {"source": 5, "target": 6, "relation": "scopes"},    # kept
    ])
    t = _triples(edges)
    assert {("e", "p", "tests"), ("h", "p", "entails"), ("p", "h", "derived-from"),
            ("s", "e2", "scopes")} <= t
    assert ("h", "p", "tests") not in t and ("e", "e2", "tests") not in t
    assert ("e", "p", "entails") not in t and ("e", "e2", "scopes") not in t


def test_edge_contrary_only_targets_a_claim_the_paper_does_not_assert():
    """`rules-out`/`contradicts`/`opposes` at an asserted claim is dropped; at an entertained
    alternative it is kept. This is the CONTRARY set `check_relations.py` enforces on the
    corpus, imported from `relations.py` so the two agree."""
    edges = _validate([
        {"source": 4, "target": 2, "relation": "rules-out"},     # target asserts → drop
        {"source": 3, "target": 2, "relation": "contradicts"},   # target asserts → drop
        {"source": 3, "target": 2, "relation": "opposes"},       # target asserts → drop
        {"source": 4, "target": 7, "relation": "rules-out"},     # target entertains → kept
    ])
    assert _triples(edges) == {("c", "alt", "rules-out")}


def test_edge_part_of_rejects_a_cycle_and_a_second_whole():
    """A part points at one whole, and the chain of wholes may not close a cycle."""
    edges = _validate([
        {"source": 3, "target": 6, "relation": "part-of"},   # e is part of e2 → kept
        {"source": 6, "target": 3, "relation": "part-of"},   # e2 → e would close a cycle → drop
        {"source": 3, "target": 5, "relation": "part-of"},   # e already has a whole → drop
    ])
    assert _triples(edges) == {("e", "e2", "part-of")}


def test_edge_dissociates_with_is_symmetric_and_written_once():
    """`dissociates-with` is symmetric; the same pair written both ways keeps one edge."""
    edges = _validate([
        {"source": 3, "target": 6, "relation": "dissociates-with"},
        {"source": 6, "target": 3, "relation": "dissociates-with"},   # same pair → drop
    ])
    assert len([e for e in edges if e["relation"] == "dissociates-with"]) == 1


def test_edge_reciprocals_are_synthesised():
    """`entails` synthesises `derived-from`; `predicts` synthesises `confirms`. The site's
    hierarchical numbering walks the reciprocal, so it must be written."""
    edges = _validate([
        {"source": 1, "target": 2, "relation": "entails", "why": "h implies p"},
        {"source": 1, "target": 2, "relation": "predicts", "why": "h predicts p"},
    ])
    t = _triples(edges)
    assert {("h", "p", "entails"), ("p", "h", "derived-from"),
            ("h", "p", "predicts"), ("p", "h", "confirms")} <= t


def test_edge_why_is_carried_through_to_the_output():
    """The model's one-sentence `why` survives validation, and a synthesised reciprocal says so."""
    edges = _validate([{"source": 3, "target": 2, "relation": "tests",
                        "why": "the result tests the prediction, results-002"}])
    assert edges[0]["why"] == "the result tests the prediction, results-002"
    recip = [e for e in _validate([{"source": 1, "target": 2, "relation": "entails",
                                    "why": "h implies p"}])
             if e["relation"] == "derived-from"][0]
    assert "reciprocal of entails" in recip["why"]


def test_edge_why_lands_in_the_claim_body_not_the_frontmatter():
    """The writer records each edge's `why` under a Relations note in the body; the frontmatter
    shape is unchanged — `tests` is still a top-level key, no `why` beside it."""
    from elife_extract import write as write_mod
    with tempfile.TemporaryDirectory() as tmp:
        cfg = _cfg(Path(tmp))
        draft = DraftClaimTable(
            paper_slug=SLUG, paper_doi=DOI, paper_title="A paper",
            claims=[
                {"claim": "The result tests the prediction.", "panel": "fig1a",
                 "claim_type": "empirical", "role": "empirical", "confidence": "high",
                 "sources": ["results"]},
                {"claim": "The prediction.", "panel": None, "claim_type": "prediction",
                 "role": "prediction", "confidence": "high", "sources": ["results"]},
            ],
        )
        src, tgt = write_mod._unique_slugs(draft.claims)
        edges = [{"source": src, "target": tgt, "relation": "tests",
                  "why": "E tests P, results-002"}]
        write_mod.write_claim_files(draft, cfg, edges=edges)
        text = (cfg.corpus_dir / SLUG / f"{src}.md").read_text()
        fm, body = text.split("---", 2)[1], text.split("---", 2)[2]
        assert "results-002" not in fm, "the why leaked into the frontmatter"
        assert "**Relations.**" in body and "E tests P, results-002" in body


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
