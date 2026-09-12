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

from .config import Config, token_budget
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
        raw = stream_text(cfg, model=model, system=system, user=user, label="questions", max_tokens=token_budget("questions"))

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
                    "epistemic": fm.get("epistemic"),
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
        # Following the new whole's chain of wholes must not lead back to the part.
        node, cyclic = whole, False
        while True:
            if node == part:
                cyclic = True
                break
            if node not in whole_of:
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
        raw = stream_text(cfg, model=model, system=system, user=user, label="parts", max_tokens=token_budget("parts"))

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


# ── stance ───────────────────────────────────────────────────────────────
# The alternatives a paper rejects, raised from its controls. A control exists to eliminate a
# rival explanation, and states its target in prose; before this layer that rival lived only
# inside the control's sentence, so the `rules-out` edge that should have named it had nothing
# to point at — and on the contract (#83) an edge aimed at a claim the paper asserts is refused,
# so on a fresh draft the eliminative move had no target at all. This layer gives each rival a
# node — an `alt-` claim whose assertion carries `stance: rejects` — and writes the `rules-out`
# edge from the named control through `edges.edges_from_raw`, so the direction check applies: a
# `rules-out` whose target is asserted, or whose source is not a control or empirical claim, is
# dropped with a logged reason. A `feature`, like `questions` and `parts`: it revises a tree
# rather than making a new kind of thing, and is idempotent — an alternative already present by
# slug is updated, not duplicated.


def _claim_stance(fm: dict) -> str:
    """This paper's stance toward a claim file, read from its assertions; absent means `asserts`.

    The same rule `scripts/check_relations.py` applies (claim-format.md §2): a claim with no
    stance is asserted. The edge validator needs it to refuse a `rules-out` aimed at an asserted
    claim, so an `alt-` file's `rejects`/`entertains` has to reach it.
    """
    for a in (fm.get("assertions") or []):
        if isinstance(a, dict) and a.get("stance"):
            return a["stance"]
    return "asserts"


def _controls_and_empirical(paper: str, cfg: Config) -> list[dict]:
    """The claims that can do the eliminating — role `control` or `empirical` — for the prompt."""
    return [c for c in _tree_claims(paper, cfg) if c["role"] in ("control", "empirical")]


def _existing_alternatives(paper: str, cfg: Config) -> list[tuple[str, str]]:
    """(slug, sentence) for the `alt-` claims already in the tree, so a re-run can reuse a slug."""
    d = cfg.corpus_dir / paper
    out = []
    for f in sorted(d.glob("alt-*.md")):
        fm = _read_frontmatter(f)
        out.append((fm.get("slug") or f.stem, " ".join(str(fm.get("claim") or "").split())))
    return out


def _paper_questions(paper: str, cfg: Config) -> list[dict]:
    """The paper's questions from index.md — id and text — the only ids `addresses` may name."""
    fm = _read_frontmatter(cfg.corpus_dir / paper / "index.md")
    return [q for q in (fm.get("questions") or []) if isinstance(q, dict) and q.get("id")]


def _results_spans(paper: str, cfg: Config) -> list[tuple[str, str]]:
    """(uid, text) for the Results section of the prepared paper — the span ids the model cites.

    A prepared.json written before spans were recorded carries none, so the spans are segmented
    from the prepared paper on the fly — the same function prepare uses — rather than leaving the
    layer with no Results prose to reason over on the older papers.
    """
    from .prepare import _build_spans

    prepared = read_prepared(paper, cfg)
    spans = prepared.spans or [s for s in _build_spans(prepared)]
    return [(s["uid"], " ".join(str(s.get("text") or "").split()))
            for s in spans if s.get("section") == "results"]


def stance_request(paper: str, cfg: Config) -> tuple[str, str]:
    """The exact (system, user) the stance layer would send.

    Separated from the call, as every model-answered layer is, so an analyst or another model
    can answer the same question through `--dump-prompt` / `--answer`.
    """
    from .prompts import prompt

    lines = ["# Controls and empirical claims\n"]
    for c in _controls_and_empirical(paper, cfg):
        head = f"- `{c['slug']}` ({c['role']}"
        head += f", {c['panel']}" if c["panel"] else ""
        lines.append(f"{head}): {c['claim']}")
    questions = _paper_questions(paper, cfg)
    if questions:
        lines.append("\n# Research questions\n")
        for q in questions:
            lines.append(f"- `{q['id']}`: {' '.join(str(q.get('text') or '').split())}")
    existing = _existing_alternatives(paper, cfg)
    if existing:
        lines.append("\n# Alternatives already recorded\n")
        for slug, sentence in existing:
            lines.append(f"- `{slug}`: {sentence}")
    lines.append("\n# Results, by span\n")
    for uid, text in _results_spans(paper, cfg):
        lines.append(f"[{uid}] {text}")
    return prompt("stance", cfg), "\n".join(lines) + "\n"


def _alt_slug(raw_slug, claim: str) -> str:
    """The `alt-` slug for one alternative: an explicit slug when given, else derived from claim.

    An explicit slug lets a re-run land on the file it already wrote (idempotency is keyed on the
    slug), and lets a supplied answer reuse the hand-authored slug of an alternative the paper
    already carries. Either way the `alt-` prefix is enforced, so a rejected rival is never
    confused with a claim the paper asserts.
    """
    from .write import derive_claim_slug

    if raw_slug and str(raw_slug).strip():
        base = re.sub(r"^alt-", "", str(raw_slug).strip())
        base = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    else:
        base = ""
    if not base:
        base = derive_claim_slug(claim)
    return f"alt-{base}"


def _validate_stance(raw: dict, paper: str, cfg: Config) -> dict:
    """Coerce a model answer into `{alternatives: [...]}`, dropping what does not resolve.

    The same rule the other retrofits apply to their answers: what does not resolve is dropped,
    not guessed. An alternative needs a claim sentence; its stance is `rejects` or `entertains`
    (never `asserts` — a rival the paper commits to is not a rival); `ruled_out_by` keeps only
    the tree's own slugs; `addresses` keeps only a question id the paper states; `span` keeps only
    a real span id. Slugs are made unique within the run so two new alternatives cannot collide,
    while an `alt-` file already on disk is matched, not renamed.
    """
    import logging as _logging
    log = _logging.getLogger(__name__)

    if not isinstance(raw, dict):
        raise ValueError("stance answer must be a JSON object with `alternatives`")
    in_tree = {c["slug"] for c in _tree_claims(paper, cfg)}
    qids = {q["id"] for q in _paper_questions(paper, cfg)}
    span_ids = {uid for uid, _ in _results_spans(paper, cfg)}
    on_disk = {slug for slug, _ in _existing_alternatives(paper, cfg)}

    assigned: set[str] = set()
    out: list[dict] = []
    for e in (raw.get("alternatives") or []):
        if not isinstance(e, dict):
            continue
        claim = " ".join(str(e.get("claim") or "").split())
        if not claim:
            log.warning("stance: an alternative with no claim text; dropped")
            continue
        slug = _alt_slug(e.get("slug"), claim)
        if slug in assigned:                            # two new alternatives, one slug
            if slug in on_disk:
                log.warning("stance: %r seen twice in this answer; second dropped", slug)
                continue
            n = 2
            while f"{slug}-{n}" in assigned or f"{slug}-{n}" in on_disk:
                n += 1
            slug = f"{slug}-{n}"
        assigned.add(slug)

        stance = e.get("stance") if e.get("stance") in ("rejects", "entertains") else "rejects"
        ruled = [s for s in (e.get("ruled_out_by") or []) if isinstance(s, str) and s in in_tree]
        dropped = [s for s in (e.get("ruled_out_by") or [])
                   if isinstance(s, str) and s not in in_tree]
        if dropped:
            log.warning("stance: %s names %r as ruling it out, not in this tree; dropped",
                        slug, dropped)
        addresses = e.get("addresses") if e.get("addresses") in qids else None
        span = e.get("span") if e.get("span") in span_ids else None
        out.append({"slug": slug, "claim": claim, "role": e.get("role") or "hypothesis",
                    "stance": stance, "addresses": addresses, "ruled_out_by": ruled,
                    "span": span, "why": " ".join(str(e.get("why") or "").split()),
                    "existing": slug in on_disk})
    return {"alternatives": out}


def _tree_claims_for_edges(paper: str, cfg: Config) -> tuple[list[dict], list[str]]:
    """(claims, slugs) parallel lists for `edges.edges_from_raw`, with each claim's stance.

    Read after the `alt-` files are written, so a freshly raised alternative reads its own
    `rejects`/`entertains` — which is what lets the direction check keep the `rules-out` aimed at
    it and refuse one aimed at a claim the paper asserts.
    """
    d = cfg.corpus_dir / paper
    claims, slugs = [], []
    for f in sorted(d.glob("*.md")):
        if f.name == "index.md":
            continue
        fm = _read_frontmatter(f)
        slugs.append(fm.get("slug") or f.stem)
        claims.append({"role": fm.get("role"), "stance": _claim_stance(fm),
                       "claim": " ".join(str(fm.get("claim") or "").split())})
    return claims, slugs


def stance_layer(paper: str, cfg: Config, *,
                 answer: str | None = None) -> tuple[Path, dict]:
    """Raise the alternatives a paper rejects, write their `alt-` files, and the `rules-out` edges.

    The model (or a supplied answer) returns the rivals and the controls that kill them; the
    runner writes an `alt-` claim file per rival (creating a new one, or updating one already
    present by slug rather than duplicating it), then adds the `rules-out` edges from the named
    controls through `edges.edges_from_raw` so the direction check applies, and records the run.
    """
    from .agents import parse_json_response, stream_text

    system, user = stance_request(paper, cfg)
    if answer is not None:
        p, model = answer_file(answer, cfg)
        raw = p.read_text(encoding="utf-8")
    else:
        model = cfg.model_reconcile
        raw = stream_text(cfg, model=model, system=system, user=user, label="stance", max_tokens=token_budget("stance"))

    data = _validate_stance(parse_json_response(raw), paper, cfg)
    edges = _apply_stance(paper, data, cfg)
    payload = {"paper_slug": paper, "model": model, **data, "edges": edges}
    path = _write_json(run_file(paper, "stance.output.json", cfg), payload)
    return path, payload


def _write_alt_file(f: Path, alt: dict, paper: str, doi: str | None) -> None:
    """Write a new `alt-` claim file — the assertion carries the stance, the body carries the why.

    Built in the shape the hand-authored `alt-` files use (claim-format.md §2, "Alternative
    explanations are claims"): the role is whatever the rival functionally is, and it is the
    stance on the assertion, not the role, that marks it as a rival.
    """
    import uuid
    from datetime import date

    from .write import _format_claim_file

    fm: dict = {
        "uuid": str(uuid.uuid4()),
        "slug": alt["slug"],
        "doi": None,
        "claim": alt["claim"],
        "claim-type": "interpretive",
        "role": alt["role"],
        **({"addresses": alt["addresses"]} if alt["addresses"] else {}),
        "concepts": [],
        "priority": date.today().isoformat(),
        "epistemic": "weak",
        "assertions": [{
            "paper-slug": paper,
            "doi": doi,
            "stance": alt["stance"],
            "method": "agent extraction of the alternative the paper argues against",
            "confidence": "weak",
        }],
        "reproductions": [],
    }
    body = ["An alternative explanation the paper argues against, not a proposition it asserts.", ""]
    if alt["why"]:
        body += [alt["why"], ""]
    if alt["span"]:
        body += [f"Raised in the Results at `{alt['span']}`.", ""]
    f.write_text(_format_claim_file(fm, "\n".join(body).rstrip() + "\n"), encoding="utf-8")


def _apply_stance(paper: str, data: dict, cfg: Config) -> list[dict]:
    """Write the `alt-` files and the `rules-out` edges, and return the edges written.

    An alternative already present by slug is updated in place — its `addresses` refreshed —
    rather than rewritten, so the hand-authored body and assertions survive; a new one is written
    whole. The `rules-out` edges then go through `edges.edges_from_raw` against the tree as it now
    stands, so a `rules-out` whose source is not a control or empirical claim, or whose target is
    a claim the paper asserts, is dropped with a logged reason before it is written.
    """
    import yaml

    from .edges import edges_from_raw

    d = cfg.corpus_dir / paper
    doi = doi_of(paper, cfg)

    for alt in data["alternatives"]:
        f = d / f"{alt['slug']}.md"
        if f.is_file():
            if alt["addresses"]:
                _write_key(f, "addresses", f"addresses: {alt['addresses']}", after="role")
        else:
            _write_alt_file(f, alt, paper, doi)

    raw_edges = [{"source": src, "target": alt["slug"], "relation": "rules-out", "why": alt["why"]}
                 for alt in data["alternatives"] for src in alt["ruled_out_by"]]
    claims, slugs = _tree_claims_for_edges(paper, cfg)
    edges = edges_from_raw(json.dumps(raw_edges), claims, slugs, source="stance")

    by_source: dict[str, list[str]] = {}
    for e in edges:
        if e["relation"] == "rules-out":
            by_source.setdefault(e["source"], []).append(e["target"])
    for src, targets in by_source.items():
        f = d / f"{src}.md"
        if not f.is_file():
            continue
        have = [t for t in (_read_frontmatter(f).get("rules-out") or []) if isinstance(t, str)]
        merged = have + [t for t in targets if t not in have]
        block = yaml.safe_dump({"rules-out": merged}, sort_keys=False, allow_unicode=True,
                               default_flow_style=False, width=100).rstrip("\n")
        _write_key(f, "rules-out", block, after="epistemic")
    return edges


# ── the measures: prose written from the graph, on disk under site/src/data ──
# summaries, synthesis and abstract-map were declared with outputs the site renders and no
# runner or committed prompt, so their artifacts could not be regenerated and no version could
# be recorded. Each is model-written prose over the same claim graph; each carries the
# `--dump-prompt` / `--answer` seam every model-answered layer has, so a model with no backend
# here can answer it and the ledger records who did.


def site_data_file(cfg: Config, *parts: str) -> Path:
    """A path under the site's committed data. The measures write here, not into runs/."""
    return cfg.root / "site" / "src" / "data" / Path(*parts)


def _known_slugs(paper: str, cfg: Config) -> set[str]:
    return {c["slug"] for c in _tree_claims(paper, cfg)}


def _graph_for_prose(paper: str, cfg: Config) -> str:
    """The claim tree rendered for a layer that restates it: every claim, then every edge.

    Slug, role (and the epistemic marker where it says more than the role), the panel and the
    sentence, then the typed edges written `source --relation--> target` — the graph and nothing
    from the paper, which is what lets the summary and the synthesis be a test of the graph.
    """
    claims = _tree_claims(paper, cfg)
    lines = ["# Claims\n"]
    for c in claims:
        head = f"- `{c['slug']}` ({c['role'] or 'claim'}"
        if c["epistemic"] and c["epistemic"] != c["role"]:
            head += f", {c['epistemic']}"
        if c["panel"]:
            head += f", {c['panel']}"
        lines.append(f"{head}): {c['claim']}")
    edges = [(c["slug"], k, t) for c in claims for k, t in c["edges"]]
    if edges:
        lines.append("\n# Edges\n")
        for s, k, t in edges:
            lines.append(f"- {s} --{k}--> {t}")
    return "\n".join(lines) + "\n"


# ── summaries ────────────────────────────────────────────────────────────
# The paper in three paragraphs, the block at the top of every paper page. `produces` names one
# file for all papers, so the runner reads it, replaces the paper's entry, and writes it back:
# editing one paper's summary restates the artifact every paper's cell reads, which is why they
# go stale together. The model is recorded inside the paper's entry rather than at the top level
# the shared file has no room for; `pipeline.py`'s by_from reader falls back to the per-paper
# entry, so `by_from: model` still finds it.

SUMMARIES_FILE = "paper-summaries.json"


def summaries_request(paper: str, cfg: Config) -> tuple[str, str]:
    from .prompts import prompt
    return prompt("summaries", cfg), _graph_for_prose(paper, cfg)


def _validate_summary(raw: dict) -> dict:
    """Coerce a model answer into the three-paragraph entry, one of hypotheses/subject.

    An atlas or descriptive paper returns `subject` in place of `hypotheses`; every other paper
    returns `hypotheses`. Exactly one is kept, and `claims` and `inferences` must both be present
    — a summary missing a paragraph is not written.
    """
    if not isinstance(raw, dict):
        raise ValueError("summary answer must be a JSON object with hypotheses/subject, claims, inferences")
    out: dict = {}
    if raw.get("subject"):
        out["subject"] = " ".join(str(raw["subject"]).split())
    elif raw.get("hypotheses"):
        out["hypotheses"] = " ".join(str(raw["hypotheses"]).split())
    else:
        raise ValueError("summary needs one of `hypotheses` or `subject`")
    for k in ("claims", "inferences"):
        if not raw.get(k):
            raise ValueError(f"summary needs a non-empty `{k}` paragraph")
        out[k] = " ".join(str(raw[k]).split())
    return out


def _write_summary(paper: str, entry: dict, cfg: Config) -> Path:
    """Replace one paper's entry in the shared summaries file, leaving the others byte-for-byte.

    Read, replace the key in place (assignment to an existing key keeps its position), write
    back with the file's own formatting — indent 2, unicode kept, no trailing newline.
    """
    path = site_data_file(cfg, SUMMARIES_FILE)
    data = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    data[paper] = entry
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def summaries_layer(paper: str, cfg: Config, *,
                    answer: str | None = None) -> tuple[Path, dict]:
    """Write the paper's three-paragraph summary into the shared paper-summaries.json."""
    from .agents import parse_json_response, stream_text

    system, user = summaries_request(paper, cfg)
    if answer is not None:
        p, model = answer_file(answer, cfg)
        raw = p.read_text(encoding="utf-8")
    else:
        model = cfg.model_reconcile
        raw = stream_text(cfg, model=model, system=system, user=user, label="summaries", max_tokens=token_budget("summaries"))

    entry = {**_validate_summary(parse_json_response(raw)), "model": model}
    path = _write_summary(paper, entry, cfg)
    return path, {"paper_slug": paper, **entry}


# ── synthesis ──────────────────────────────────────────────────────────────
# The paper's argument, restated from the claim graph alone and traced back to the nodes it was
# built from. Given the graph and nothing else, so a restatement that reads as the same paper is
# evidence the graph carries it. The output is the flat v3 shape the site reads.


def synthesis_request(paper: str, cfg: Config) -> tuple[str, str]:
    from .prompts import prompt
    return prompt("synthesis", cfg), _graph_for_prose(paper, cfg)


def _validate_synthesis(raw: dict, paper: str, cfg: Config) -> dict:
    """Coerce a model answer into `{synthesis, traceback}`, dropping unresolvable references.

    The synthesis prose is kept as written (its paragraph breaks matter). Each traceback entry
    keeps only the claim slugs this paper actually holds; an edge is kept as the string it came
    as. An entry with no sentence is dropped.
    """
    if not isinstance(raw, dict):
        raise ValueError("synthesis answer must be a JSON object with `synthesis` and `traceback`")
    synthesis = str(raw.get("synthesis") or "").strip()
    if not synthesis:
        raise ValueError("synthesis needs a non-empty `synthesis`")
    known = _known_slugs(paper, cfg)
    traceback = []
    for e in (raw.get("traceback") or []):
        if not isinstance(e, dict) or not e.get("sentence"):
            continue
        traceback.append({
            "sentence": " ".join(str(e["sentence"]).split()),
            "claims": [s for s in (e.get("claims") or []) if s in known],
            "edges": [x for x in (e.get("edges") or []) if isinstance(x, str)],
        })
    return {"synthesis": synthesis, "traceback": traceback}


def synthesis_layer(paper: str, cfg: Config, *,
                    answer: str | None = None) -> tuple[Path, dict]:
    """Write the restatement and its traceback to site/src/data/synthesis-v3/<paper>.json."""
    from .agents import parse_json_response, stream_text

    system, user = synthesis_request(paper, cfg)
    if answer is not None:
        p, model = answer_file(answer, cfg)
        raw = p.read_text(encoding="utf-8")
    else:
        model = cfg.model_reconcile
        raw = stream_text(cfg, model=model, system=system, user=user, label="synthesis", max_tokens=token_budget("synthesis"))

    data = _validate_synthesis(parse_json_response(raw), paper, cfg)
    payload = {"paperSlug": paper, "version": 3, **data, "model": model}
    path = _write_json(site_data_file(cfg, "synthesis-v3", f"{paper}.json"), payload)
    return path, payload


# ── abstract-map ─────────────────────────────────────────────────────────
# The abstract cut into sentences, each mapped to the claims it carries, and every claim the
# abstract drops. The runner owns the sentence split, so the model annotates numbered sentences
# and the text is re-attached by number; and it derives `orphanClaims` and `orphanSentences`
# from the per-sentence mapping, so the two directions cannot disagree.


def _abstract_sentences(paper: str, cfg: Config) -> tuple[str, list[str]]:
    """The abstract as one whitespace-normalised string and the same string split into sentences."""
    from .segment import split_sentences

    text = " ".join(read_prepared(paper, cfg).abstract.split())
    return text, split_sentences(text)


def abstract_map_request(paper: str, cfg: Config) -> tuple[str, str]:
    from .prompts import prompt

    _text, sentences = _abstract_sentences(paper, cfg)
    lines = ["# Abstract, by sentence\n"]
    for i, s in enumerate(sentences, 1):
        lines.append(f"[{i}] {s}")
    lines.append("\n# Claims\n")
    for c in _tree_claims(paper, cfg):
        lines.append(f"- `{c['slug']}` ({c['role'] or 'claim'}): {c['claim']}")
    return prompt("abstract-map", cfg), "\n".join(lines) + "\n"


def _validate_abstract_map(raw: dict, paper: str, cfg: Config) -> dict:
    """Coerce a model answer into the mapping, both directions enforced from one source.

    The runner's own split is authoritative: each returned sentence is matched to its number and
    its text re-attached, an unknown `type` becomes `background`, a `claim` sentence resolving to
    no known slug becomes `unmappable`, and `kind` is confined to the three the site labels.
    `orphanClaims` is every claim no sentence carried and `orphanSentences` every unmappable
    sentence — derived here rather than trusted, so assigning a claim and calling it an orphan
    cannot both happen.
    """
    if not isinstance(raw, dict):
        raise ValueError("abstract-map answer must be a JSON object with `sentences`")
    _text, sentences = _abstract_sentences(paper, cfg)
    text_of = {i + 1: s for i, s in enumerate(sentences)}
    known = _known_slugs(paper, cfg)

    annotated: dict[int, dict] = {}
    for e in (raw.get("sentences") or []):
        if not isinstance(e, dict):
            continue
        try:
            n = int(e.get("n"))
        except (TypeError, ValueError):
            continue
        if n in text_of:
            annotated[n] = e

    out_sentences = []
    for n in sorted(text_of):
        e = annotated.get(n, {})
        typ = e.get("type") if e.get("type") in ("claim", "background", "unmappable") else "background"
        claims = [s for s in (e.get("claims") or []) if s in known] if typ == "claim" else []
        if typ == "claim" and not claims:
            typ = "unmappable"                          # named claims, none in this tree
        item = {"n": n, "text": text_of[n], "type": typ, "claims": claims}
        if typ == "claim":
            item["kind"] = e.get("kind") if e.get("kind") in ("direct", "combined", "synthesis") else "direct"
        note = " ".join(str(e.get("note") or "").split())
        if note:
            item["note"] = note
        out_sentences.append(item)

    used = {s for it in out_sentences for s in it["claims"]}
    return {
        "abstract": _text,
        "sentences": out_sentences,
        "orphanClaims": [c["slug"] for c in _tree_claims(paper, cfg) if c["slug"] not in used],
        "orphanSentences": [it["n"] for it in out_sentences if it["type"] == "unmappable"],
    }


def abstract_map_layer(paper: str, cfg: Config, *,
                       answer: str | None = None) -> tuple[Path, dict]:
    """Write the abstract-to-claims mapping to site/src/data/abstract-mapping/<paper>.json."""
    from .agents import parse_json_response, stream_text

    system, user = abstract_map_request(paper, cfg)
    if answer is not None:
        p, model = answer_file(answer, cfg)
        raw = p.read_text(encoding="utf-8")
    else:
        model = cfg.model_reconcile
        raw = stream_text(cfg, model=model, system=system, user=user, label="abstract-map", max_tokens=token_budget("abstract-map"))

    data = _validate_abstract_map(parse_json_response(raw), paper, cfg)
    payload = {"paperSlug": paper, **data, "model": model}
    path = _write_json(site_data_file(cfg, "abstract-mapping", f"{paper}.json"), payload)
    return path, payload
