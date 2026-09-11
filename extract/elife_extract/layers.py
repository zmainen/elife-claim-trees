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
from .write import _read_frontmatter, _write_key


# ── where a layer's files live ───────────────────────────────────────────


def answer_file(answer: str, cfg: Config) -> tuple[Path, str]:
    """A supplied answer: the file to read, and how the output should name it.

    A relative path resolves against the corpus root, not the working directory — the
    runner keeps the raw reply at `runs/<paper>/<layer>.answer.v<N>.json` and hands that
    path to a command that has already `cd extract`. The label is root-relative where it
    can be, so `model: supplied:runs/...` in the output means the same thing on any
    checkout; an absolute path outside the root is kept as it is.
    """
    p = Path(answer).expanduser()
    if not p.is_absolute():
        p = cfg.root / p
    p = p.resolve()
    try:
        label = str(p.relative_to(cfg.root))
    except ValueError:
        label = str(p)
    return p, f"supplied:{label}"


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

    prepared = read_prepared(paper, cfg)
    if answer is not None:
        p, label = answer_file(answer, cfg)
        extraction = reader_from_raw(agent, paper, label, p.read_text(encoding="utf-8"), prepared)
    else:
        extraction = run_agent(agent, prepared, cfg)
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
        p, label = answer_file(answer, cfg)
        draft = draft_from_raw(p.read_text(encoding="utf-8"), r, c, st, cfg,
                               prepared.doi, prepared.title,
                               prepared.extraction_path, prepared.extraction_path_note,
                               prepared)
        draft.model = label
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
        paper=prepared,
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
        p, label = answer_file(answer, cfg)
        revised = review_from_raw(p.read_text(encoding="utf-8"), draft)
        revised.model = label
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


# ── questions ────────────────────────────────────────────────────────────
# A retrofit for papers that already have trees: read the paper's questions off the abstract
# (and the Introduction, once prepare carries it) and the hypotheses and rejected alternatives
# it already holds, and record them on the paper. `write.py` does the same at extraction time
# for a fresh tree; this layer is how the nine papers extracted before questions existed catch
# up without a re-run — a `feature`, like `stance`, that revises an artifact rather than
# producing a new kind of thing.


def _hypotheses_and_alternatives(paper: str, cfg: Config) -> list[tuple[str, str]]:
    """(slug, sentence) for the claims a question answers: hypotheses and rejected alternatives.

    A question's answers are the paper's committed bet (`role: hypothesis`) and the rivals it
    turned down (the `alt-` files, `stance: rejects`). Those are the claims the layer shows the
    model and the only ones it may attach `addresses` to.
    """
    d = cfg.corpus_dir / paper
    out = []
    for f in sorted(d.glob("*.md")):
        if f.name == "index.md":
            continue
        fm = _read_frontmatter(f)
        slug = fm.get("slug") or f.stem
        if fm.get("role") == "hypothesis" or f.name.startswith("alt-"):
            out.append((slug, " ".join(str(fm.get("claim") or "").split())))
    return out


def questions_request(paper: str, cfg: Config) -> tuple[str, str]:
    """The exact (system, user) the questions layer would send.

    Separated from the call, as every model-answered layer is, so an analyst or another model
    can answer the same question through `--dump-prompt` / `--answer`.
    """
    from .prompts import prompt

    prepared = read_prepared(paper, cfg)
    lines = [f"# Abstract\n\n{prepared.abstract}\n"]
    # prepared.json carries no Introduction today; the prompt says it is used when available.
    intro = getattr(prepared, "introduction_text", None)
    if intro:
        lines.append(f"# Introduction\n\n{intro}\n")
    lines.append("# Hypotheses and rejected alternatives\n")
    for slug, sentence in _hypotheses_and_alternatives(paper, cfg):
        lines.append(f"- `{slug}`: {sentence}")
    return prompt("questions", cfg), "\n".join(lines) + "\n"


def _validate_questions(raw: dict, paper: str, cfg: Config) -> dict:
    """Coerce a model answer into `{questions, addresses}`, dropping what does not resolve.

    A question needs an id and text; an `addresses` entry needs a slug this paper actually
    holds and a target that is one of the returned question ids. An invented slug or a dangling
    target is dropped rather than written — the same rule the other layers apply to their
    answers.
    """
    if not isinstance(raw, dict):
        raise ValueError("questions answer must be a JSON object with `questions` and `addresses`")
    questions = [{"id": q["id"], "text": " ".join(str(q["text"]).split())}
                 for q in (raw.get("questions") or [])
                 if isinstance(q, dict) and q.get("id") and q.get("text")]
    ids = {q["id"] for q in questions}
    have = {slug for slug, _ in _hypotheses_and_alternatives(paper, cfg)}
    addresses = {slug: qid for slug, qid in (raw.get("addresses") or {}).items()
                 if slug in have and qid in ids}
    return {"questions": questions, "addresses": addresses}


def questions_layer(paper: str, cfg: Config, *,
                    answer: str | None = None) -> tuple[Path, dict]:
    """Record the paper's questions, and write them onto the paper and its claims.

    The model (or a supplied answer) returns the questions and which claim answers which; the
    runner writes the output JSON, then edits `index.md` and the named claim files in place —
    inserting `questions:` and `addresses:` without disturbing the keys already there.
    """
    from .agents import parse_json_response, stream_text

    system, user = questions_request(paper, cfg)
    if answer is not None:
        p, model = answer_file(answer, cfg)
        raw = p.read_text(encoding="utf-8")
    else:
        model = cfg.model_reconcile
        raw = stream_text(cfg, model=model, system=system, user=user, label="questions")

    data = _validate_questions(parse_json_response(raw), paper, cfg)
    payload = {"paper_slug": paper, "model": model, **data}
    path = _write_json(run_file(paper, "questions.output.json", cfg), payload)
    _apply_questions(paper, data, cfg)
    return path, payload


# ── writing questions and addresses back into the tree, in place ─────────
# The frontmatter text-editors (`_write_key` and friends) live in write.py, which both this
# layer and the claim-tree carry-over write keys back through — one copy, since layers already
# imports write.


def _apply_questions(paper: str, data: dict, cfg: Config) -> None:
    """Write `questions:` into index.md and `addresses:` into each named claim file."""
    import yaml

    d = cfg.corpus_dir / paper
    if data["questions"]:
        block = yaml.safe_dump({"questions": data["questions"]}, sort_keys=False,
                               allow_unicode=True, default_flow_style=False,
                               width=100).rstrip("\n")
        _write_key(d / "index.md", "questions", block)
    for slug, qid in data["addresses"].items():
        f = d / f"{slug}.md"
        if f.is_file():
            _write_key(f, "addresses", f"addresses: {qid}", after="role")


# ── parts ────────────────────────────────────────────────────────────────
# The second grain of a claim tree: a claim can be a component of another — one comparison,
# condition, measure or study of a proposition the whole states once. `write.py` records this
# at reconciliation for a fresh tree, from the reconciler's `part_of`; this layer is the
# retrofit for the trees induced before `part-of` existed. It reads the tree, not the paper —
# the claims and their edges — so it is cheap, and writes `part-of:` into each part's claim
# file in place. A `feature`, like `questions` and `stance`: it revises a tree rather than
# making a new kind of thing.


def _relations_module():
    """`scripts/relations.py`, loaded by path — the single source of the edge vocabulary.

    The same load `contract.py` does. The package cannot import a script beside it, and the
    parts prompt shows each claim's existing edges, so it needs to know which frontmatter keys
    are relations rather than guessing.
    """
    import importlib.util

    p = Path(__file__).resolve().parents[2] / "scripts" / "relations.py"
    spec = importlib.util.spec_from_file_location("relations", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def _tree_claims(paper: str, cfg: Config) -> list[dict]:
    """Every claim in the paper's tree — slug, role, panel, sentence, outgoing edges.

    The edges are what lets the prompt see that the graph half-says composition already: a part
    usually carries `supports` or `tests` into the claim it composes. Read from both places the
    schema stores a relation — the top-level list keys and `belongings` — like everything that
    counts the corpus's edges.
    """
    edge_keys = _relations_module().EDGE_KEYS
    d = cfg.corpus_dir / paper
    out = []
    for f in sorted(d.glob("*.md")):
        if f.name == "index.md":
            continue
        fm = _read_frontmatter(f)
        slug = fm.get("slug") or f.stem
        edges = []
        for key in sorted(edge_keys):
            for t in (fm.get(key) or []):
                if isinstance(t, str):
                    edges.append((key, t))
        for item in (fm.get("belongings") or []):
            if isinstance(item, dict) and item.get("relation") and item.get("target"):
                edges.append((item["relation"], item["target"]))
        out.append({"slug": slug, "role": fm.get("role"),
                    "panel": (fm.get("assertions") or [{}])[0].get("panel")
                    if fm.get("assertions") else None,
                    "claim": " ".join(str(fm.get("claim") or "").split()),
                    "edges": edges})
    return out


def parts_request(paper: str, cfg: Config) -> tuple[str, str]:
    """The exact (system, user) the parts layer would send.

    Separated from the call, as every model-answered layer is, so an analyst or another model
    can answer the same question through `--dump-prompt` / `--answer`.
    """
    from .prompts import prompt

    lines = ["# The claim tree\n"]
    for c in _tree_claims(paper, cfg):
        head = f"- `{c['slug']}` ({c['role'] or 'claim'}"
        head += f", {c['panel']}" if c["panel"] else ""
        lines.append(f"{head}): {c['claim']}")
        if c["edges"]:
            lines.append("  edges: " + ", ".join(f"{k} → {t}" for k, t in c["edges"]))
    return prompt("parts", cfg), "\n".join(lines) + "\n"


def _validate_parts(raw: dict, paper: str, cfg: Config) -> dict:
    """Coerce a model answer into `{parts: [{part, whole, why}]}`, dropping what does not hold.

    The same rule the other retrofits apply to their answers: what does not resolve is dropped,
    not guessed. A part and a whole must both be claims in this tree; a part is not its own
    whole; a part points at exactly one whole (a second is dropped); and the edges may not form
    a cycle — following a chain of wholes must terminate. A dropped edge is warned about, so the
    output is auditable against the tree the layer read.
    """
    import logging as _logging
    log = _logging.getLogger(__name__)

    if not isinstance(raw, dict):
        raise ValueError("parts answer must be a JSON object with `parts`")
    slugs = {c["slug"] for c in _tree_claims(paper, cfg)}
    whole_of: dict[str, str] = {}
    kept: list[dict] = []
    for e in (raw.get("parts") or []):
        if not isinstance(e, dict):
            continue
        part, whole = e.get("part"), e.get("whole")
        why = " ".join(str(e.get("why") or "").split())
        if part not in slugs or whole not in slugs:
            log.warning("parts: %r → %r names a claim not in this tree; dropped", part, whole)
            continue
        if part == whole:
            log.warning("parts: %r is its own whole; dropped", part)
            continue
        if part in whole_of:
            log.warning("parts: %r already has whole %r; second whole %r dropped",
                        part, whole_of[part], whole)
            continue
        node, cyclic = whole, False
        while node in whole_of:
            if node == part:
                cyclic = True
                break
            node = whole_of[node]
        if cyclic:
            log.warning("parts: %r → %r would close a cycle; dropped", part, whole)
            continue
        whole_of[part] = whole
        kept.append({"part": part, "whole": whole, "why": why})
    return {"parts": kept}


def parts_layer(paper: str, cfg: Config, *,
                answer: str | None = None) -> tuple[Path, dict]:
    """Record the paper's parts, and write `part-of:` onto each part's claim file.

    The model (or a supplied answer) returns the `part-of` edges it finds; the runner writes
    the output JSON, then edits each part's claim file in place — inserting `part-of:` without
    disturbing the keys already there.
    """
    from .agents import parse_json_response, stream_text

    system, user = parts_request(paper, cfg)
    if answer is not None:
        p, model = answer_file(answer, cfg)
        raw = p.read_text(encoding="utf-8")
    else:
        model = cfg.model_reconcile
        raw = stream_text(cfg, model=model, system=system, user=user, label="parts")

    data = _validate_parts(parse_json_response(raw), paper, cfg)
    payload = {"paper_slug": paper, "model": model, **data}
    path = _write_json(run_file(paper, "parts.output.json", cfg), payload)
    _apply_parts(paper, data, cfg)
    return path, payload


def _apply_parts(paper: str, data: dict, cfg: Config) -> None:
    """Write `part-of: [<whole>]` into each part's claim file, a top-level relation key.

    Placed after `epistemic`, where `write.py` and `stance`'s carry-over put the other
    top-level relations, so a retrofitted file and an induced one read the same.
    """
    import yaml

    d = cfg.corpus_dir / paper
    for e in data["parts"]:
        f = d / f"{e['part']}.md"
        if not f.is_file():
            continue
        block = yaml.safe_dump({"part-of": [e["whole"]]}, sort_keys=False,
                               allow_unicode=True, default_flow_style=False).rstrip("\n")
        _write_key(f, "part-of", block, after="epistemic")
