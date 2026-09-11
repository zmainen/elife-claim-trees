"""Layer runners — one function per runnable node in `pipeline/layers.yaml`.

A layer reads the paths its declaration names and writes the path it declares. That is the
whole contract, and it is what lets `scripts/pipeline.py run` hash what a run read and
produced.

Before this the CLI wrote `out/draft-<slug>.json` and `out/agents-<slug>.json` — paths no
layer declares — and did five layers' work in one process. So the graph described a pipeline
it could not execute (`pipeline.py run <paper> results-reader` answered "no runner declared"),
the provenance that mattered lived in a hand-kept `runs/<paper>/manifest.json` beside the
ledger, and `scripts/agents_report.py` read an `extract/out/` that is not in the repository,
so the data behind the site's agents page could not be regenerated.

Each runner writes one JSON object with `model` at the top level where a model answered it,
which is what a layer's `by_from: model` reads. A bare list cannot say who wrote it.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict
from pathlib import Path

from .config import Config
from .prepare import FigureCaption, PreparedPaper, TableCaption, prepare
from .schema import AgentExtraction, DraftClaimTable


# ── where a layer's files live ───────────────────────────────────────────


def run_dir(paper: str, cfg: Config) -> Path:
    d = cfg.root / "runs" / paper
    d.mkdir(parents=True, exist_ok=True)
    return d


def run_file(paper: str, name: str, cfg: Config) -> Path:
    return cfg.root / "runs" / paper / name


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def _require(path: Path, layer: str, produced_by: str) -> dict:
    """Read a declared input, or say which layer has not run rather than failing on a path."""
    if not path.is_file():
        raise SystemExit(
            f"error: {layer} needs {path.name}, which {produced_by} has not produced.\n"
            f"  expected: {path}\n"
            f"  run it:   python3 scripts/pipeline.py run <paper> {produced_by}"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def doi_of(paper: str, cfg: Config) -> str | None:
    """The paper's DOI from its claim-tree index — the same place the runner looks."""
    p = cfg.root / "claims" / paper / "index.md"
    if not p.is_file():
        return None
    m = re.search(r"^doi:\s*(\S+)", p.read_text(encoding="utf-8"), re.M)
    return m.group(1).strip("'\"") if m else None


# ── prepare ──────────────────────────────────────────────────────────────


def prepare_layer(paper: str, cfg: Config, *, doi: str | None = None,
                  pdf_path: Path | None = None, input_format: str = "auto") -> Path:
    """What the readers read, on disk and hashable.

    A layer because otherwise the three readers' only declared input is their prompt, and the
    paper — which eLife revises — would be hashed by nothing. A run would record which prompt
    read a paper without recording which paper.
    """
    doi = doi or doi_of(paper, cfg)
    if not doi and pdf_path is None:
        raise SystemExit(
            f"error: no DOI for {paper}. It is read from claims/{paper}/index.md, which does "
            f"not exist yet for a new paper — pass --doi, or --pdf-path for a paper that is "
            f"not on the eLife CDN.")
    prepared = prepare(doi=doi, paper_slug_override=paper,
                       input_format=input_format, pdf_path=pdf_path)
    return _write_json(run_file(paper, "prepared.json", cfg), asdict(prepared))


def read_prepared(paper: str, cfg: Config) -> PreparedPaper:
    data = _require(run_file(paper, "prepared.json", cfg), "this layer", "prepare")
    figures = [FigureCaption(**f) for f in data.pop("figure_captions", [])]
    tables = [TableCaption(**t) for t in data.pop("tables", [])]
    return PreparedPaper(**data, figure_captions=figures, tables=tables)


# ── the three readers ────────────────────────────────────────────────────

READER_OUTPUT = {"results": "results-reader.output.json",
                 "caption": "caption-reader.output.json",
                 "structure": "structure-reader.output.json"}


def reader_layer(agent: str, paper: str, cfg: Config, *,
                 answer: str | None = None) -> tuple[Path, AgentExtraction]:
    """One reader against its slice. The three stay apart because agreement is the signal.

    `answer` is a raw reply from somewhere other than the configured backend. It goes through
    the same validation, and records who produced it, so the ledger's `by` distinguishes a
    backend call from an agent answering the same prompt.
    """
    from .agents import model_for, reader_from_raw, run_agent

    if answer is not None:
        extraction = reader_from_raw(agent, paper, f"supplied:{answer}",
                                     Path(answer).read_text(encoding="utf-8"))
    else:
        extraction = run_agent(agent, read_prepared(paper, cfg), cfg)
    path = _write_json(run_file(paper, READER_OUTPUT[agent], cfg),
                       json.loads(extraction.model_dump_json()))
    return path, extraction


def reader_request(agent: str, paper: str, cfg: Config) -> tuple[str, str]:
    from .agents import build_reader_request
    return build_reader_request(agent, read_prepared(paper, cfg), cfg)


def read_reader(agent: str, paper: str, cfg: Config) -> AgentExtraction:
    return AgentExtraction(**_require(
        run_file(paper, READER_OUTPUT[agent], cfg), "reconcile", f"{agent}-reader"))


# ── reconcile, external review, edges ────────────────────────────────────


def _three_readers(paper: str, cfg: Config):
    return (read_reader("results", paper, cfg), read_reader("caption", paper, cfg),
            read_reader("structure", paper, cfg))


def reconcile_request(paper: str, cfg: Config) -> tuple[str, str]:
    from .reconcile import build_reconcile_request
    p = read_prepared(paper, cfg)
    r, c, st = _three_readers(paper, cfg)
    return build_reconcile_request(r, c, st, cfg, p.doi, p.title)


def reconcile_layer(paper: str, cfg: Config, *,
                    answer: str | None = None) -> tuple[Path, DraftClaimTable]:
    from .reconcile import draft_from_raw, reconcile

    prepared = read_prepared(paper, cfg)
    if answer is not None:
        r, c, st = _three_readers(paper, cfg)
        draft = draft_from_raw(Path(answer).read_text(encoding="utf-8"), r, c, st, cfg,
                               prepared.doi, prepared.title,
                               prepared.extraction_path, prepared.extraction_path_note)
        draft.model = f"supplied:{answer}"
        path = _write_json(run_file(paper, "reconciler.output.json", cfg),
                           json.loads(draft.model_dump_json()))
        return path, draft
    draft = reconcile(
        read_reader("results", paper, cfg),
        read_reader("caption", paper, cfg),
        read_reader("structure", paper, cfg),
        cfg, paper_doi=prepared.doi, paper_title=prepared.title,
        extraction_path=prepared.extraction_path,
        extraction_path_note=prepared.extraction_path_note,
    )
    draft.model = cfg.model_reconcile
    path = _write_json(run_file(paper, "reconciler.output.json", cfg),
                       json.loads(draft.model_dump_json()))
    return path, draft


def external_review_request(paper: str, cfg: Config) -> tuple[str, str]:
    from .external_review import build_review_request
    draft = DraftClaimTable(**_require(
        run_file(paper, "reconciler.output.json", cfg), "external-review", "reconcile"))
    return build_review_request(read_prepared(paper, cfg), draft, cfg)


def external_review_layer(paper: str, cfg: Config, *,
                          answer: str | None = None) -> tuple[Path, DraftClaimTable]:
    """The Opus pass that recovers structure the three readers systematically miss.

    Was `--review-mode external`. It is a step, not review: it changes the artifact, and it
    runs before the version it would have approved exists.
    """
    from .external_review import external_review, review_from_raw

    draft = DraftClaimTable(**_require(
        run_file(paper, "reconciler.output.json", cfg), "external-review", "reconcile"))
    if answer is not None:
        revised = review_from_raw(Path(answer).read_text(encoding="utf-8"), draft)
        revised.model = f"supplied:{answer}"
    else:
        revised = external_review(read_prepared(paper, cfg), draft, cfg)
        revised.model = cfg.model_reconcile
    path = _write_json(run_file(paper, "external-review.output.json", cfg),
                       json.loads(revised.model_dump_json()))
    return path, revised


def best_draft(paper: str, cfg: Config) -> tuple[DraftClaimTable, str]:
    """The draft a downstream layer should build on, and which layer produced it.

    `claim-tree` declares both `reconcile` and `external-review` as needs. External review is
    the better draft where it exists and is absent for nine of the ten papers, so an absent
    one is the normal condition rather than a failure — the graph reports it beside the cell
    as `unrecorded_upstream` and the state stays computed from what did run.
    """
    reviewed = run_file(paper, "external-review.output.json", cfg)
    if reviewed.is_file():
        return DraftClaimTable(**json.loads(reviewed.read_text(encoding="utf-8"))), "external-review"
    return DraftClaimTable(**_require(
        run_file(paper, "reconciler.output.json", cfg), "this layer", "reconcile")), "reconcile"


def edge_inference_layer(paper: str, cfg: Config) -> tuple[Path, list[dict]]:
    from .edges import infer_edges
    from .write import _unique_slugs

    draft, _ = best_draft(paper, cfg)
    edges = infer_edges(draft, _unique_slugs(draft.claims), cfg)
    path = _write_json(run_file(paper, "edge-inference.output.json", cfg), {
        "paper_slug": paper, "model": cfg.model_reconcile, "edges": edges,
    })
    return path, edges


def read_edges(paper: str, cfg: Config) -> list[dict]:
    """Edges from the layer's output, tolerating the bare array the first runs wrote."""
    p = run_file(paper, "edge-inference.output.json", cfg)
    if not p.is_file():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data.get("edges", [])
