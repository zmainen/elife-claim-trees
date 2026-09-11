"""Command-line entry point.

One subcommand per runnable layer in `pipeline/layers.yaml`. Each reads the paths its layer
declares and writes the path it declares, and nothing here walks the graph or records a run —
`scripts/pipeline.py` does both, and does them once.

That division is the point. This CLI used to be a pipeline of its own: `extract` did five
layers' work in one process, `run` chained extract → write → verify-refs, and both wrote to
`out/`, which no layer declares. So the graph described a shape it could not execute
(`pipeline.py run <paper> results-reader` answered "no runner declared"), a run left artifacts
the ledger could not hash, and the provenance that mattered — which model wrote these claims —
lived in a hand-kept manifest beside the ledger meant to replace it.

`--review-mode` is gone with them. It bundled two different things: `external`, which revises
the draft and is now the `external-review` layer, and `interactive`, a gate before the write,
where the architecture puts approval on a version after it exists —
`scripts/pipeline.py approve <paper> <layer>`.

`evaluate` is the one subcommand that is not a layer. It scores a re-extraction against the
committed corpus, so it asks about the prompts rather than about a paper, produces nothing any
layer consumes, and deliberately runs outside the graph.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .config import (
    Config,
    DEFAULT_MODEL_CAPTION,
    DEFAULT_MODEL_RECONCILE,
    DEFAULT_MODEL_RESULTS,
    DEFAULT_MODEL_STRUCTURE,
    DEFAULT_PROMPT_VARIANT,
)


def _logging(verbose: bool = False) -> None:
    import logging
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def _dump(args: argparse.Namespace, request, label: str) -> bool:
    """Write the exact prompt this layer would send, and stop.

    Whatever answers it then answers the question the layer would have asked, rather than a
    paraphrase of it written from memory. The answer comes back through `--answer` and gets
    the same validation a backend reply would.
    """
    if not getattr(args, "dump_prompt", None):
        return False
    system, user = request()
    out = Path(args.dump_prompt).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(system + "\n\n---\n\n" + user, encoding="utf-8")
    print(f"  {label}: prompt written to {out}  ({len(system)}c system + {len(user)}c user)")
    print(f"  answer it, then: --answer <file>")
    return True


def _cfg(args: argparse.Namespace) -> Config:
    cfg = Config.from_args(args)
    errors = cfg.validate()
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        raise SystemExit(2)
    _logging(getattr(args, "verbose", False))
    return cfg


# ── layer runners ────────────────────────────────────────────────────────


def cmd_prepare(args: argparse.Namespace) -> int:
    """Layer `prepare` — fetch and slice the paper the readers will read."""
    from .layers import prepare_layer

    cfg = _cfg(args)
    path = prepare_layer(args.paper, cfg, doi=args.doi,
                         pdf_path=Path(args.pdf_path) if args.pdf_path else None,
                         input_format=args.input_format)
    import json
    data = json.loads(path.read_text(encoding="utf-8"))
    print(f"=== prepare — {args.paper} ===")
    print(f"  doi    = {data['doi']}")
    print(f"  title  = {data['title']}")
    print(f"  path   = {data['extraction_path']}")
    print(f"  slices = abstract:{len(data['abstract'])}c results:{len(data['results_text'])}c "
          f"captions:{len(data['captions_text'])}c methods:{len(data['methods_text'])}c")
    print(f"  figures= {len(data['figure_captions'])}  tables={len(data['tables'])}")
    print(f"  written: {path}")
    return 0


def _reader(agent: str):
    def run(args: argparse.Namespace) -> int:
        from .layers import reader_layer, reader_request

        cfg = _cfg(args)
        if _dump(args, lambda: reader_request(agent, args.paper, cfg), f"{agent}-reader"):
            return 0
        path, extraction = reader_layer(agent, args.paper, cfg, answer=args.answer)
        verified = sum(1 for c in extraction.claims if c.evidence_verified)
        total = len(extraction.claims)
        ev_str = (f"  evidence verified {verified}/{total} quotes"
                  if any(c.evidence_verified is not None for c in extraction.claims) else "")
        print(f"=== {agent}-reader — {args.paper} ===")
        print(f"  model    = {extraction.model}")
        print(f"  proposed = {total} candidate claim(s)")
        if ev_str:
            print(ev_str)
        print(f"  written: {path}")
        return 0
    return run


def cmd_reconcile(args: argparse.Namespace) -> int:
    """Layer `reconcile` — which candidates survive, and which readers agreed."""
    from .layers import reconcile_layer, reconcile_request

    cfg = _cfg(args)
    if _dump(args, lambda: reconcile_request(args.paper, cfg), "reconcile"):
        return 0
    path, draft = reconcile_layer(args.paper, cfg, answer=args.answer)
    by_conf: dict[str, int] = {}
    for c in draft.claims:
        by_conf[c.confidence] = by_conf.get(c.confidence, 0) + 1
    ev_total = sum(len(c.evidence_verified) for c in draft.claims)
    ev_ok = sum(sum(v for v in c.evidence_verified.values()) for c in draft.claims)
    print(f"=== reconcile — {args.paper} ===")
    print(f"  model  = {draft.model}")
    print(f"  claims = {len(draft.claims)}  (per-agent: {dict(draft.per_agent_counts)})")
    for k in ("high", "contested", "single-source"):
        if k in by_conf:
            print(f"    {k:14s} {by_conf[k]:3d}")
    if ev_total:
        print(f"  evidence verified {ev_ok}/{ev_total} quotes")
    print(f"  written: {path}")
    return 0


def cmd_external_review(args: argparse.Namespace) -> int:
    """Layer `external-review` — recover the structure the three readers miss."""
    from .layers import external_review_layer, external_review_request, run_file
    import json

    cfg = _cfg(args)
    if _dump(args, lambda: external_review_request(args.paper, cfg), "external-review"):
        return 0
    before = len(json.loads(run_file(args.paper, "reconciler.output.json", cfg)
                            .read_text(encoding="utf-8"))["claims"]) \
        if run_file(args.paper, "reconciler.output.json", cfg).is_file() else 0
    path, revised = external_review_layer(args.paper, cfg, answer=args.answer)
    print(f"=== external-review — {args.paper} ===")
    print(f"  model  = {revised.model}")
    print(f"  claims = {before} → {len(revised.claims)}")
    print(f"  written: {path}")
    return 0


def cmd_edge_inference(args: argparse.Namespace) -> int:
    """Layer `edge-inference` — which claims depend on which."""
    from .layers import best_draft, edge_inference_layer, run_file
    from .edges import build_edge_request
    from .write import _unique_slugs

    cfg = _cfg(args)

    # Emit the prompt and stop. Whatever answers it — an analyst, a reasoning agent — then
    # answers the same question the layer would have asked, rather than a paraphrase of it
    # written from memory.
    if args.dump_prompt:
        draft, source = best_draft(args.paper, cfg)
        system, user = build_edge_request(draft, _unique_slugs(draft.claims))
        out = Path(args.dump_prompt).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(system + "\n\n---\n\n" + user, encoding="utf-8")
        print(f"  prompt written: {out}  (from {source})")
        print(f"  answer it with a JSON array, then re-run with --edges-json <answer.json>")
        return 0

    supplied = args.answer or args.edges_json
    if supplied:
        from .edges import edges_from_raw
        from .layers import _write_json, answer_file
        draft, _ = best_draft(args.paper, cfg)
        p, label = answer_file(supplied, cfg)
        edges = edges_from_raw(p.read_text(encoding="utf-8"), _unique_slugs(draft.claims),
                               source=label)
        path = _write_json(run_file(args.paper, "edge-inference.output.json", cfg), {
            "paper_slug": args.paper, "model": label, "edges": edges,
        })
    else:
        path, edges = edge_inference_layer(args.paper, cfg)

    kinds: dict[str, int] = {}
    for e in edges:
        # `relation` is the key edges.py emits; reading `relationType` counted every
        # edge as one unknown kind and reported "1 relation type" for any answer.
        k = e.get("relation", "?")
        kinds[k] = kinds.get(k, 0) + 1
    print(f"=== edge-inference — {args.paper} ===")
    print(f"  edges = {len(edges)} across {len(kinds)} relation type(s)")
    for k, n in sorted(kinds.items(), key=lambda kv: -kv[1]):
        print(f"    {k:28s} {n:3d}")
    print(f"  written: {path}")
    return 0


def cmd_write(args: argparse.Namespace) -> int:
    """Layer `claim-tree` — the claim files, from the best draft and the inferred edges."""
    from .layers import best_draft, read_edges
    from .write import archive_dir, carry_over, write_claim_files, write_oxa_document

    cfg = _cfg(args)
    draft, source = best_draft(args.paper, cfg)
    edges = read_edges(args.paper, cfg)

    print(f"=== claim-tree — {args.paper} ===")
    print(f"  draft  = {source} ({len(draft.claims)} claims)")
    print(f"  edges  = {len(edges)} from the edge-inference layer"
          if edges else "  edges  = none — the edge-inference layer has not run")

    # A replacement archives the current tree before it writes, so know now whether there was
    # one to archive: the carry-over below runs only when a version was actually set aside.
    paper_dir = cfg.corpus_dir / draft.paper_slug
    replacing = args.replace and paper_dir.exists() and any(paper_dir.iterdir())

    try:
        if args.format == "oxa":
            path = write_oxa_document(draft, cfg)
            print(f"  written: {path}")
            return 0
        written = write_claim_files(draft, cfg, edges=edges, replace=args.replace)
    except FileExistsError as e:
        print(f"error: {e}", file=sys.stderr)
        return 7
    except Exception as e:                                       # noqa: BLE001
        print(f"error: write failed: {e}", file=sys.stderr)
        return 8

    print(f"  wrote {len(written)} file(s) into {cfg.corpus_dir / draft.paper_slug}")

    # Carry forward what the induction chain does not produce and the replaced version held:
    # the `alt-` claims, the `rules-out` edges that named them, and the reproduction records.
    # Done here so a single `write --replace` leaves the final tree — and the ledger entry the
    # runner takes afterwards hashes it whole, carry-over included.
    if replacing:
        arch = archive_dir(cfg, draft.paper_slug)
        s = carry_over(cfg, draft.paper_slug, arch)
        print(f"  archived previous version to {arch.relative_to(cfg.root)}")
        print(f"  carried: {len(s['alt_claims'])} alt- claim(s), {len(s['rules_out'])} "
              f"rules-out edge(s), {len(s['reproductions'])} reproduction record(s)"
              + (f"; {len(s['unplaced'])} unplaced" if s["unplaced"] else ""))
    return 0


def cmd_questions(args: argparse.Namespace) -> int:
    """Layer `questions` — the research questions the paper's hypotheses answer."""
    from .layers import questions_layer, questions_request

    cfg = _cfg(args)
    if _dump(args, lambda: questions_request(args.paper, cfg), "questions"):
        return 0
    path, payload = questions_layer(args.paper, cfg, answer=args.answer)
    print(f"=== questions — {args.paper} ===")
    print(f"  model     = {payload['model']}")
    print(f"  questions = {len(payload['questions'])}")
    for q in payload["questions"]:
        addressed = [s for s, qid in payload["addresses"].items() if qid == q["id"]]
        print(f"    {q['id']}: {q['text']}")
        print(f"       ← {', '.join(addressed) if addressed else '(no claim addresses it)'}")
    print(f"  written: {path}")
    return 0


def cmd_parts(args: argparse.Namespace) -> int:
    """Layer `parts` — which claims are components of other claims."""
    from .layers import parts_layer, parts_request

    cfg = _cfg(args)
    if _dump(args, lambda: parts_request(args.paper, cfg), "parts"):
        return 0
    path, payload = parts_layer(args.paper, cfg, answer=args.answer)
    print(f"=== parts — {args.paper} ===")
    print(f"  model = {payload['model']}")
    print(f"  parts = {len(payload['parts'])}")
    for e in payload["parts"]:
        print(f"    {e['part']} → {e['whole']}")
    print(f"  written: {path}")
    return 0


def cmd_summaries(args: argparse.Namespace) -> int:
    """Layer `summaries` — the paper in three paragraphs, written from its claim graph."""
    from .layers import summaries_layer, summaries_request

    cfg = _cfg(args)
    if _dump(args, lambda: summaries_request(args.paper, cfg), "summaries"):
        return 0
    path, payload = summaries_layer(args.paper, cfg, answer=args.answer)
    print(f"=== summaries — {args.paper} ===")
    print(f"  model = {payload['model']}")
    for k in ("hypotheses", "subject", "claims", "inferences"):
        if payload.get(k):
            print(f"  {k}: {payload[k][:90]}{'…' if len(payload[k]) > 90 else ''}")
    print(f"  written: {path}")
    return 0


def cmd_verify_refs(args: argparse.Namespace) -> int:
    """Layer `reference-check` — do the cited references resolve, and to what?"""
    import json
    from dataclasses import asdict
    from .layers import _write_json, run_file
    from .verify_refs import verify_refs

    cfg = _cfg(args)
    print(f"=== reference-check — {args.paper or 'whole corpus'} ===")
    print(f"  corpus_dir = {cfg.corpus_dir}")
    try:
        results = verify_refs(args.paper, cfg, dry_run=args.dry_run)
    except Exception as e:                                       # noqa: BLE001
        print(f"error: reference check failed: {e}", file=sys.stderr)
        return 3

    by_status: dict[str, int] = {}
    for r in results:
        by_status[r.status] = by_status.get(r.status, 0) + 1
    print(f"\n=== Summary ({len(results)} literature-context claim(s)) ===")
    for status in ("confirmed", "found", "low-confidence", "not-found",
                   "no-hint", "unresolvable"):
        if status in by_status:
            print(f"  {status:18s} {by_status[status]}")
    n_resolved = by_status.get("confirmed", 0) + by_status.get("found", 0)
    rate = (n_resolved / len(results) * 100) if results else 0
    print(f"  {'=' * 30}")
    print(f"  resolution rate    {rate:.1f}% ({n_resolved}/{len(results)})")

    # The report is what the layer produces. Two implementations of this check existed and
    # neither kept one: scripts/verify-references.py wrote a corpus-wide JSON that nothing
    # regenerated, and this path printed to the terminal and kept nothing at all.
    if args.dry_run:
        print("\n  --dry-run: no DOIs written and no report kept.")
        return 0
    if not args.paper:
        print("\n  no report written — a version belongs to one paper. "
              "Re-run with --paper <slug> to record one.")
        return 0
    path = _write_json(run_file(args.paper, "reference-check.output.json", cfg), {
        "paper_slug": args.paper,
        "resolution_pct": round(rate, 1),
        "by_status": by_status,
        "results": [asdict(r) for r in results],
    })
    print(f"  written: {path}")
    return 0


# ── layers that read the paper as well as the tree ───────────────────────


def _load_claim_frontmatter(d: Path) -> list:
    """Read every claim file's YAML frontmatter from a claim-tree directory."""
    import re
    import yaml
    out = []
    for f in sorted(d.glob("*.md")):
        if f.name == "index.md":
            continue
        m = re.match(r"^---\n(.*?)\n---", f.read_text(encoding="utf-8"), re.S)
        if not m:
            continue
        # Some committed files put an empty list at column 0 on the line after
        # its key, which strict YAML rejects. Normalise rather than edit source.
        body = re.sub(r"^([A-Za-z0-9_-]+):\n(\[\]|\{\})\s*$", r"\1: \2",
                      m.group(1), flags=re.M)
        try:
            fm = yaml.safe_load(body) or {}
        except yaml.YAMLError:
            continue
        if fm.get("slug"):
            out.append(fm)
    return out


def _claims_of(args: argparse.Namespace, cfg: Config) -> tuple[Path, list]:
    d = (Path(args.claims_dir).expanduser().resolve() if args.claims_dir
         else cfg.corpus_dir / args.paper)
    if not d.is_dir():
        print(f"error: claims dir not found: {d}", file=sys.stderr)
        raise SystemExit(2)
    claims = _load_claim_frontmatter(d)
    if not claims:
        print(f"error: no claim files under {d}", file=sys.stderr)
        raise SystemExit(2)
    return d, claims


def cmd_coverage(args: argparse.Namespace) -> int:
    """Layer `coverage` — what in the paper does no claim account for?

    No model calls, so it is fast and free, and it can be run on every paper in the corpus
    as a gate. It answers a different question from `evaluate`: evaluate scores agreement
    between two claim sets, which says nothing about what neither of them mentioned. You can
    score 100% agreement on a third of a paper. This takes its denominator from the paper.
    """
    import json
    from .coverage import assess, render, assess_spans, render_spans
    from .layers import read_prepared

    cfg = _cfg(args)
    paper = read_prepared(args.paper, cfg)
    claims_dir, claims = _claims_of(args, cfg)

    inv = assess(paper, claims)
    spans = assess_spans(paper, claims, include_methods=args.include_methods)
    if args.mapping:
        from .coverage import apply_mapping
        spans = apply_mapping(spans, json.loads(Path(args.mapping).read_text(encoding="utf-8")),
                              claims)

    print(f"=== Coverage — {paper.paper_slug} ===")
    print(f"  claims read: {len(claims)}  from {claims_dir}\n")
    print(render(inv))
    print()
    print(render_spans(spans))

    if args.json:
        out = Path(args.json).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({
            "paper": paper.paper_slug,
            "claims": len(claims),
            "panels": {"total": inv.panels_total, "orphan": inv.panels_orphan,
                       "figure_level": inv.panels_figure_level,
                       "phantom": inv.panels_phantom, "pct": round(inv.panel_pct, 1)},
            "statistics": {"total": len(inv.stats_total),
                           "orphan": [s.text for s in inv.stats_orphan],
                           "pct": round(inv.stat_pct, 1)},
            "spans": {
                "segmented": len(spans.spans),
                "obligations": spans.obligations,
                "textual": len(spans.textual),
                "accounted": len(spans.accounted),
                "pct": round(spans.pct, 1),
                "orphans": [{"uid": u.uid, "section": u.section, "text": u.text,
                             "stats": u.stats, "panels": u.panels}
                            for u in spans.orphans],
            },
        }, indent=2), encoding="utf-8")
        print(f"\nwritten: {out}")

    # A gate, when asked to be one.
    if args.fail_on_orphans and (inv.panels_orphan or spans.orphans):
        print("\nFAIL: the paper contains panels or results no claim accounts for.",
              file=sys.stderr)
        return 1
    return 0


def cmd_mark(args: argparse.Namespace) -> int:
    """Layer `marks` — write the paper's claim assignments into the document.

    The marked document is the record: an assigned span carries the claim's UUID, a span
    that states no result says so, and a span carrying a result with no mark is a gap you
    can see by looking.
    """
    import json
    from .coverage import assess_spans, apply_mapping
    from .marks import render_marked, assignments_from_marked, NO_ASSERTION, GAP
    from .layers import read_prepared

    cfg = _cfg(args)
    paper = read_prepared(args.paper, cfg)
    _, claims = _claims_of(args, cfg)

    uuid_of = {c["slug"]: c.get("uuid") for c in claims}
    # A card in the margin shows the note's body. With the UUID alone in the payload every
    # card read `49d08c4f-7b31-4967-9ab7-06aa50a006b4`, which is correct, durable and
    # unreadable — visible the moment the document was opened rather than reasoned about.
    # The key stays the identity; the body says what it means.
    label_of = {c["slug"]: (c.get("shortClaim") or c.get("slug") or "") for c in claims}

    rep = assess_spans(paper, claims, include_methods=args.include_methods)
    mapping = {}
    if args.mapping and Path(args.mapping).is_file():
        mapping = json.loads(Path(args.mapping).read_text(encoding="utf-8"))
        rep = apply_mapping(rep, mapping, claims)

    # A span is assigned the UUID of a claim that accounts for it. Where several do, the
    # first is written — the mark records that the span is covered, and which claim leads;
    # a span belonging to several claims is a curation question rather than something to
    # guess at here.
    assignments: dict[str, str] = {}
    labels: dict[str, str] = {}
    for span, slugs in rep.accounted:
        sl = next((sl for sl in slugs if uuid_of.get(sl)), None)
        if sl:
            assignments[span.uid] = uuid_of[sl]
            labels[span.uid] = label_of.get(sl, sl)
    reasons: dict[str, str] = {}
    for v in (mapping.get("spans", []) if isinstance(mapping, dict) else mapping) or []:
        if isinstance(v, dict) and v.get("uid") and v.get("why"):
            reasons[v["uid"]] = v["why"]
    for span, why in rep.excluded:
        assignments[span.uid] = NO_ASSERTION
        if why:
            reasons.setdefault(span.uid, why)
    # The body reads: what the claim says, then why — whichever we have.
    for uid, lab in labels.items():
        reasons[uid] = f"{lab} — {reasons[uid]}" if reasons.get(uid) else lab
    # A span carrying a result that no claim accounts for is marked as such. Leaving it bare
    # would make it indistinguishable from the ordinary prose around it, which is most of the
    # paper — and telling those two apart is the entire point.
    for span in rep.orphans:
        assignments[span.uid] = GAP

    text = render_marked(paper, assignments, author=args.author,
                         include_methods=args.include_methods, reasons=reasons)
    out = Path(args.out).expanduser() if args.out else cfg.root / "marked" / f"{paper.paper_slug}.marked.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")

    # Read the marks straight back. If the document cannot reproduce the assignments it was
    # just written from, it is not a record of anything.
    back = assignments_from_marked(text, paper, include_methods=args.include_methods)
    n = lambda p: sum(1 for v in assignments.values() if v == p)
    print(f"=== Marked — {paper.paper_slug} ===")
    print(f"  assigned to a claim : {len(assignments) - n(NO_ASSERTION) - n(GAP)}")
    print(f"  states no result    : {n(NO_ASSERTION)}")
    print(f"  unclaimed (gap)     : {n(GAP)}")
    print(f"  unmarked prose      : (carries no result — never an obligation)")
    print(f"  written             : {out}")
    if back == assignments:
        print(f"  round-trip          : OK — {len(back)} marks read back identically")
        return 0
    print(f"  round-trip          : MISMATCH — wrote {len(assignments)}, read {len(back)}",
          file=sys.stderr)
    return 1


# ── the prompt contract ──────────────────────────────────────────────────


def cmd_contract(args: argparse.Namespace) -> int:
    """Render the prompt contract from its sources, or check that the committed one is current.

    Not a layer: it produces inputs to layers. The rendered files are declared in
    pipeline/layers.yaml as what the readers, the reconciler and the reviewer read, so
    regenerating them after a vocabulary change is what makes every run that read the old
    definitions stale.
    """
    from .contract import CONTRACT_DIR, check, write

    cfg = _cfg(args)
    if args.write:
        for p in write(cfg.prompts_dir, cfg.root):
            print(f"  wrote {p.relative_to(cfg.root)}")
    stale = check(cfg.prompts_dir, cfg.root)
    if stale:
        print(f"error: extract/prompts/{CONTRACT_DIR}/ is not what its sources generate: "
              f"{', '.join(stale)}\n  run: cd extract && python3 -m elife_extract.cli contract --write",
              file=sys.stderr)
        return 1
    print(f"  extract/prompts/{CONTRACT_DIR}/ is current")
    return 0


# ── the one subcommand that is not a layer ───────────────────────────────


def cmd_evaluate(args: argparse.Namespace) -> int:
    """Score a re-extraction against the committed corpus.

    Deliberately outside the graph. It asks about the prompts rather than about a paper,
    writes nothing any layer consumes, and runs the chain into a temp tree — so its answer
    is "if today's prompts re-read these papers, how close would they land", which is not a
    question about a version of anything.
    """
    from .evaluate import evaluate_paper, aggregate_report

    _logging(getattr(args, "verbose", False))
    cfg = Config.from_args(args)
    # corpus_dir is not used — evaluate reads --reference-dir and writes into --work-dir.
    if cfg.prompts_dir is None or not cfg.prompts_dir.is_dir():
        print(f"error: prompts dir invalid: {cfg.prompts_dir}", file=sys.stderr)
        return 2

    reference_dir = Path(args.reference_dir).expanduser().resolve()
    if not reference_dir.is_dir():
        print(f"error: reference dir not found: {reference_dir}", file=sys.stderr)
        return 2

    work_root = Path(args.work_dir).expanduser().resolve()
    work_root.mkdir(parents=True, exist_ok=True)

    if args.papers:
        slugs = [s.strip() for s in args.papers.split(",") if s.strip()]
    elif args.all:
        slugs = sorted(p.name for p in reference_dir.iterdir() if p.is_dir())
    else:
        print("error: pass --paper(s), or --all to evaluate the whole corpus", file=sys.stderr)
        return 2

    print(f"=== evaluate ===")
    print(f"  reference_dir  = {reference_dir}")
    print(f"  work_dir       = {work_root}")
    print(f"  external review= {'on' if args.external_review else 'off'}")
    print(f"  papers         = {len(slugs)} ({', '.join(slugs[:6])}{'...' if len(slugs) > 6 else ''})")
    print()

    review_mode = "external" if args.external_review else "auto-approve"
    cards = []
    for i, slug in enumerate(slugs, 1):
        ref_paper_dir = reference_dir / slug
        if not ref_paper_dir.is_dir():
            print(f"[{i}/{len(slugs)}] {slug}: SKIP (no reference dir)", file=sys.stderr)
            continue

        paper_work_dir = work_root / slug
        existing_card = paper_work_dir / "scorecard.json"
        if args.skip_existing and existing_card.is_file():
            import json as _j
            data = _j.loads(existing_card.read_text())
            from .evaluate import PaperScorecard
            card = PaperScorecard(**{k: v for k, v in data.items() if k != "matches"})
            card.matches = data.get("matches", [])
            cards.append(card)
            print(f"[{i}/{len(slugs)}] {slug}: SKIP (existing scorecard)")
            continue

        print(f"[{i}/{len(slugs)}] {slug}: starting...")
        card = evaluate_paper(ref_paper_dir=ref_paper_dir, work_dir=paper_work_dir,
                              cfg=cfg, review_mode=review_mode)
        cards.append(card)
        if card.error:
            print(f"[{i}/{len(slugs)}] {slug}: FAILED ({card.error})")
        else:
            print(f"[{i}/{len(slugs)}] {slug}: "
                  f"recovery={card.recovery_pct:.0f}%, panel={card.panel_pct:.0f}%, "
                  f"role={card.role_pct:.0f}% ({card.n_cli} CLI vs {card.n_ref} ref)")

    out_path = work_root / "aggregate-scorecard.md"
    aggregate_report(cards=cards, out_path=out_path, reference_dir=reference_dir,
                     work_root=work_root, review_mode=review_mode)
    print(f"\naggregate scorecard: {out_path}")
    return 0


# ── Argument parser construction ──────────────────────────────────────────


def _add_backend_args(parser: argparse.ArgumentParser) -> None:
    """Backend routing. Shared by every subcommand that calls a model."""
    parser.add_argument(
        "--backend", default=None,
        help=("Model backend: vertex (default), anthropic, openrouter, openai, "
              "google, groq, together, deepseek. Anything but vertex/anthropic "
              "is routed via litellm. Or set ELIFE_EXTRACT_BACKEND."),
    )
    parser.add_argument(
        "--api-key", default=None,
        help=("API key for the chosen backend. Defaults to that backend's "
              "environment variable (e.g. OPENROUTER_API_KEY). Not needed for vertex."),
    )


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    """Args shared across every layer runner."""
    parser.add_argument(
        "--root", type=Path,
        help="The corpus repository — what pipeline/layers.yaml resolves its paths against. "
             "Defaults to the directory this package ships in, or ELIFE_CLAIM_TREES_ROOT.",
    )
    parser.add_argument(
        "--corpus-dir", type=Path,
        help="Where claim files are read and written (default: <root>/claims).",
    )
    parser.add_argument(
        "--prompts-dir", type=Path,
        help="Override the prompts directory (default: package-local prompts/).",
    )
    parser.add_argument(
        "--prompt-variant", default=DEFAULT_PROMPT_VARIANT,
        help=f"Named prompt variant under prompts/<variant>/ (default: {DEFAULT_PROMPT_VARIANT}).",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Per-chunk DEBUG logging. Default is INFO, which reports each stage and a "
             "progress heartbeat.",
    )
    _add_backend_args(parser)


def _add_answerable_args(parser: argparse.ArgumentParser, what: str) -> None:
    """Let something other than the configured backend answer this layer.

    `edge-inference` has had this pair since a provider outage took the edges while every
    other stage succeeded. Every layer a model answers has that failure mode, and the same
    escape: ask for the prompt, answer it anywhere, hand back the reply.
    """
    parser.add_argument(
        "--dump-prompt", metavar="PATH",
        help=f"Write the exact prompt this layer would send to PATH and exit, so whatever "
             f"answers it answers the same question. Nothing is run.")
    parser.add_argument(
        "--answer", metavar="PATH",
        help=f"Record this file as the answer instead of calling a backend. It goes through "
             f"the same validation as a backend reply; {what}")


def _add_model_args(parser: argparse.ArgumentParser) -> None:
    """Model-routing knobs for the subcommands that call a model."""
    parser.add_argument("--model-results", default=None,
                        help=f"Model for the Results-reader (default: {DEFAULT_MODEL_RESULTS}).")
    parser.add_argument("--model-caption", default=None,
                        help=f"Model for the Caption-reader (default: {DEFAULT_MODEL_CAPTION}).")
    parser.add_argument("--model-structure", default=None,
                        help=f"Model for the Structure-reader (default: {DEFAULT_MODEL_STRUCTURE}).")
    parser.add_argument("--model-reconcile", default=None,
                        help=f"Model for reconciliation, external review and edge inference "
                             f"(default: {DEFAULT_MODEL_RECONCILE}).")
    parser.add_argument("--vertex-project", default=None,
                        help="Vertex AI project ID (default: VERTEX_PROJECT_ID env or cr-mainen).")
    parser.add_argument("--vertex-region", default=None,
                        help="Vertex AI region (default: VERTEX_REGION env or europe-west1).")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="elife-extract",
        description=(
            "Layer runners for the claim-trees pipeline. One subcommand per runnable layer "
            "in pipeline/layers.yaml; each reads and writes the paths its layer declares. "
            "To run a layer and its unmet dependencies, and to record the run, use "
            "`python3 scripts/pipeline.py run <paper> <layer>` rather than calling these "
            "in sequence."
        ),
        epilog=(
            "Layers, in dependency order: prepare, results-reader, caption-reader, "
            "structure-reader, reconcile, external-review, edge-inference, write "
            "(claim-tree), verify-refs (reference-check), coverage, mark (marks). "
            "`evaluate` is a tool, not a layer."
        ),
    )
    parser.add_argument("--version", action="version", version=f"elife-extract {__version__}")
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    # ── prepare ──────────────────────────────────────────────────────────
    p_prep = sub.add_parser(
        "prepare", help="Layer `prepare` — fetch and slice the paper.",
        description=(
            "Fetch the paper, slice it into the abstract / results / captions / methods the "
            "three readers each get, and write runs/<paper>/prepared.json. A layer so that "
            "the paper itself is hashed: without it a reader's only declared input is its "
            "prompt, and a run records which prompt read a paper but not which paper."
        ),
    )
    p_prep.add_argument("--paper", required=True, help="Paper slug.")
    p_prep.add_argument("--doi", default=None,
                        help="Paper DOI. Defaults to the one in claims/<paper>/index.md, "
                             "which a new paper does not have yet.")
    p_prep.add_argument("--pdf-path", default=None,
                        help="A local PDF, for a paper that is not on the eLife CDN.")
    p_prep.add_argument("--input-format", choices=["auto", "jats", "pdf"], default="auto",
                        help="Input source (default: auto = jats for eLife DOIs).")
    _add_common_args(p_prep)
    p_prep.set_defaults(func=cmd_prepare)

    # ── the three readers ────────────────────────────────────────────────
    for agent, reads in (("results", "the Results section"),
                         ("caption", "the figure and table captions"),
                         ("structure", "the methods, supplements and section structure")):
        p = sub.add_parser(
            f"{agent}-reader", help=f"Layer `{agent}-reader` — read {reads}.",
            description=(
                f"Run the {agent}-reader against {reads} of runs/<paper>/prepared.json and "
                f"write its candidate claims to runs/<paper>/{agent}-reader.output.json. "
                f"The three readers are kept apart because their agreement is the signal; "
                f"none sees another's output."
            ),
        )
        p.add_argument("--paper", required=True, help="Paper slug.")
        _add_answerable_args(p, "the model recorded is the file it came from.")
        _add_common_args(p)
        _add_model_args(p)
        p.set_defaults(func=_reader(agent))

    # ── reconcile ────────────────────────────────────────────────────────
    p_rec = sub.add_parser(
        "reconcile", help="Layer `reconcile` — which candidates survive.",
        description=(
            "Align the three readers' outputs into one draft claim table, tagged by "
            "confidence and carrying which readers surfaced each claim."
        ),
    )
    p_rec.add_argument("--paper", required=True, help="Paper slug.")
    p_rec.add_argument("--reconcile-strategy",
                       choices=["confidence-tagged", "union", "intersection-only",
                                "majority-vote"],
                       default="confidence-tagged")
    _add_answerable_args(p_rec, "the fields the pipeline owns are filled either way.")
    _add_common_args(p_rec)
    _add_model_args(p_rec)
    p_rec.set_defaults(func=cmd_reconcile)

    # ── external review ──────────────────────────────────────────────────
    p_ext = sub.add_parser(
        "external-review", help="Layer `external-review` — recover missed structure.",
        description=(
            "One Opus pass over the reconciled draft, recovering the prediction and "
            "hypothesis roles and the multi-panel claims the three readers systematically "
            "miss. Was --review-mode external; it is a step rather than review, because it "
            "changes the artifact and runs before the version it would approve exists."
        ),
    )
    p_ext.add_argument("--paper", required=True, help="Paper slug.")
    _add_answerable_args(p_ext, "the draft's own fields survive whoever answered.")
    _add_common_args(p_ext)
    _add_model_args(p_ext)
    p_ext.set_defaults(func=cmd_external_review)

    # ── edge inference ───────────────────────────────────────────────────
    p_edge = sub.add_parser(
        "edge-inference", help="Layer `edge-inference` — which claims depend on which.",
        description=(
            "Infer typed relations between the draft's claims and write them to "
            "runs/<paper>/edge-inference.output.json, which the claim-tree layer then reads "
            "rather than paying for the same answer twice."
        ),
    )
    p_edge.add_argument("--paper", required=True, help="Paper slug.")
    _add_answerable_args(p_edge, "unknown slugs and self-edges are dropped either way.")
    p_edge.add_argument("--edges-json", help=argparse.SUPPRESS)   # the older name for --answer
    _add_common_args(p_edge)
    _add_model_args(p_edge)
    p_edge.set_defaults(func=cmd_edge_inference)

    # ── questions ────────────────────────────────────────────────────────
    p_q = sub.add_parser(
        "questions", help="Layer `questions` — the research questions the paper answers.",
        description=(
            "A question is not a claim, so it lives on the paper. Given the abstract (and the "
            "Introduction when prepare carries it) and the paper's existing hypothesis and "
            "alt- claims, return the questions the paper states and which claim answers which, "
            "then write `questions:` into index.md and `addresses:` into the named claim files. "
            "A retrofit for papers whose trees were built before questions were first-class."
        ),
    )
    p_q.add_argument("--paper", required=True, help="Paper slug.")
    _add_answerable_args(p_q, "the questions and addresses are validated against this tree.")
    _add_common_args(p_q)
    _add_model_args(p_q)
    p_q.set_defaults(func=cmd_questions)

    # ── parts ──────────────────────────────────────────────────────────────
    p_parts = sub.add_parser(
        "parts", help="Layer `parts` — which claims are components of other claims.",
        description=(
            "A claim tree has two grains. Given the tree's claims — slug, role, panel, sentence "
            "and their edges — return the `part-of` edges it holds: each claim that is a "
            "component of another under the definition, and the whole it belongs to. It writes "
            "`part-of:` into each part's claim file. A retrofit for trees induced before "
            "`part-of` was first-class; `write.py` records it at reconciliation for fresh ones. "
            "`--dump-prompt` writes the exact request, `--answer` feeds a reply back through the "
            "same validation — an unknown slug, a self-edge, a cycle or a second whole is "
            "dropped, not written."
        ),
    )
    p_parts.add_argument("--paper", required=True, help="Paper slug.")
    _add_answerable_args(p_parts, "the parts are validated against this tree.")
    _add_common_args(p_parts)
    _add_model_args(p_parts)
    p_parts.set_defaults(func=cmd_parts)

    # ── summaries ──────────────────────────────────────────────────────────
    p_sum = sub.add_parser(
        "summaries", help="Layer `summaries` — the paper in three paragraphs.",
        description=(
            "The block at the top of every paper page, written from the claim graph alone. Given "
            "the tree's claims — slug, role, panel, sentence and edges — return three paragraphs: "
            "`hypotheses` (or `subject` for an atlas), `claims` and `inferences`. It writes the "
            "paper's entry into the shared site/src/data/paper-summaries.json. "
            "`--dump-prompt` writes the exact request, `--answer` feeds a reply back through the "
            "same validation."
        ),
    )
    p_sum.add_argument("--paper", required=True, help="Paper slug.")
    _add_answerable_args(p_sum, "the three paragraphs are checked, one of hypotheses/subject kept.")
    _add_common_args(p_sum)
    _add_model_args(p_sum)
    p_sum.set_defaults(func=cmd_summaries)

    # ── write (claim-tree) ───────────────────────────────────────────────
    p_write = sub.add_parser(
        "write", help="Layer `claim-tree` — write the claim files.",
        description=(
            "Assign slugs and UUIDs, attach the edges the edge-inference layer produced, "
            "and write one claim file per claim into <corpus-dir>/<paper>/. Builds on the "
            "external-review output where that layer has run, and on the reconciled draft "
            "where it has not."
        ),
    )
    p_write.add_argument("--paper", required=True, help="Paper slug.")
    p_write.add_argument("--format", choices=["yaml", "oxa"], default="yaml",
                         help="yaml (per-claim markdown, default) or oxa (one JSON Document).")
    p_write.add_argument("--replace", action="store_true",
                         help="Replace an existing tree: move it to runs/<paper>/claim-tree.v<N>/ "
                              "first, then write the new one and carry forward its alt- claims, "
                              "rules-out edges and reproduction records. Without this, a non-empty "
                              "directory is refused.")
    _add_common_args(p_write)
    p_write.set_defaults(func=cmd_write)

    # ── verify-refs (reference-check) ────────────────────────────────────
    p_refs = sub.add_parser(
        "verify-refs", help="Layer `reference-check` — do the cited references resolve?",
        description=(
            "For each literature-context claim, resolve the cited reference via CrossRef, "
            "write the confirmed DOI back to the claim's frontmatter, and record what was "
            "found in runs/<paper>/reference-check.output.json."
        ),
    )
    p_refs.add_argument("--paper", default=None,
                        help="Paper slug. Omit to sweep the corpus — which writes no report, "
                             "because a version belongs to one paper.")
    p_refs.add_argument("--dry-run", action="store_true",
                        help="Print resolutions without writing DOIs back or keeping a report.")
    _add_common_args(p_refs)
    p_refs.set_defaults(func=cmd_verify_refs)

    # ── coverage ─────────────────────────────────────────────────────────
    p_cov = sub.add_parser(
        "coverage", help="Layer `coverage` — what does no claim account for?",
        description=(
            "Take the denominator from the paper rather than from the claim set. Builds the "
            "panel and statistic inventories, segments the whole text into sentences, and "
            "reports which carry a result no claim states. Unlike `evaluate`, which scores "
            "agreement between two claim sets, this can see what both of them missed."
        ),
    )
    p_cov.add_argument("--paper", required=True, help="Paper slug.")
    p_cov.add_argument("--claims-dir", help="The claim tree to measure against "
                                            "(default: <corpus-dir>/<paper>).")
    p_cov.add_argument("--include-methods", action="store_true",
                       help="Count methods sentences as obligations too (off by default: "
                            "the corpus claims results, not procedure).")
    p_cov.add_argument("--mapping",
                       help="Adjudicated verdicts for spans the mechanical match could not "
                            "resolve, so the report shows real gaps rather than everything "
                            "the string match missed.")
    p_cov.add_argument("--json", help="Also write the full report as JSON here.")
    p_cov.add_argument("--fail-on-orphans", action="store_true",
                       help="Exit non-zero if any panel or result is unaccounted for.")
    _add_common_args(p_cov)
    p_cov.set_defaults(func=cmd_coverage)

    # ── mark (marks) ─────────────────────────────────────────────────────
    p_mark = sub.add_parser(
        "mark", help="Layer `marks` — write claim assignments into the document.",
        description=(
            "Render the paper with a tika claim mark on every span a claim accounts for, "
            "carrying that claim's UUID. Spans that state no result are marked as such; a "
            "span carrying a result that no claim states is marked as a gap, so it is "
            "visible by looking rather than only countable in a report."
        ),
    )
    p_mark.add_argument("--paper", required=True, help="Paper slug.")
    p_mark.add_argument("--claims-dir", help="Default: <corpus-dir>/<paper>.")
    p_mark.add_argument("--mapping", help="Adjudicated verdicts, as for `coverage`.")
    p_mark.add_argument("--include-methods", action="store_true")
    p_mark.add_argument("--author", default="zach", help="Mark author (default: zach).")
    p_mark.add_argument("-o", "--out", help="Output path (default: <root>/marked/<paper>.marked.md).")
    _add_common_args(p_mark)
    p_mark.set_defaults(func=cmd_mark)

    # ── contract (not a layer) ───────────────────────────────────────────
    p_con = sub.add_parser(
        "contract", help="Render the prompt contract, or check that the committed one is current.",
        description=(
            "The part of every prompt that is generated: the vocabulary of roles, claim types, "
            "relations and confidence, rendered from vocabulary.py and scripts/relations.py "
            "with examples quoted from the corpus, and the output schema rendered from "
            "schema.py. --write regenerates extract/prompts/contract/; without it the command "
            "only checks, and exits non-zero when the committed files are stale."
        ),
    )
    p_con.add_argument("--write", action="store_true", help="Regenerate the contract files.")
    _add_common_args(p_con)
    p_con.set_defaults(func=cmd_contract)

    # ── evaluate (not a layer) ───────────────────────────────────────────
    p_eval = sub.add_parser(
        "evaluate", help="Score a re-extraction against the committed corpus. Not a layer.",
        description=(
            "Re-run the chain into a temp tree for each paper and score the result against "
            "the committed claim files: recovery, panel agreement, role agreement. Use it to "
            "validate a prompt change before keeping it. Outside the graph deliberately — it "
            "asks about the prompts rather than about a paper, and produces nothing any "
            "layer consumes."
        ),
    )
    p_eval.add_argument("--reference-dir", required=True,
                        help="The curated reference corpus (e.g. claims/).")
    p_eval.add_argument("--work-dir", required=True,
                        help="Where per-paper extraction artifacts and scorecards go.")
    grp = p_eval.add_mutually_exclusive_group()
    grp.add_argument("--paper", dest="papers", help="Single paper slug to evaluate.")
    grp.add_argument("--papers", help="Comma-separated list of paper slugs.")
    grp.add_argument("--all", action="store_true",
                     help="Evaluate every paper directory under reference-dir.")
    p_eval.add_argument("--external-review", action="store_true", default=True,
                        help="Run the external-review step in the scored chain (default: on).")
    p_eval.add_argument("--no-external-review", dest="external_review", action="store_false",
                        help="Score the chain without external review.")
    p_eval.add_argument("--skip-existing", action="store_true",
                        help="Skip papers that already have a scorecard.json under work-dir.")
    p_eval.add_argument("-v", "--verbose", action="store_true")
    p_eval.add_argument("--prompts-dir", type=Path,
                        help="Override the prompts directory (default: package-local prompts/).")
    p_eval.add_argument("--prompt-variant", default=DEFAULT_PROMPT_VARIANT,
                        help="Named prompt variant under prompts/<variant>/.")
    _add_model_args(p_eval)
    _add_backend_args(p_eval)
    p_eval.set_defaults(func=cmd_evaluate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
