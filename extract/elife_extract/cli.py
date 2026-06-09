"""Command-line entry point.

Subcommands implement the 8-step methodology in two phases:
    extract     — Steps 1-4 (no disk writes to corpus)
    write       — Steps 5-7 (claim files emitted)
    verify-refs — CrossRef DOI resolution for literature-context claims
    run         — Composed shorthand (extract + write + verify-refs)

The two-phase shape is required by the methodology's Step 5 review gate
(`docs/method.md` § 3.3): "Nothing is written to disk until the table is
approved." Bypass for tests/automation: `--auto-approve`.
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


# ── Subcommand handlers (Phase B: stubs that print intent) ───────────────


def cmd_extract(args: argparse.Namespace) -> int:
    """Steps 1-4: fetch paper, abstract scan, three-agent extraction, reconciliation."""
    cfg = Config.from_args(args)
    errors = cfg.validate()
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        return 2

    import json
    import logging
    from .prepare import prepare
    from .agents import run_all_agents
    from .reconcile import reconcile as reconcile_step

    # Honor a --verbose flag if present; default to INFO logging
    log_level = logging.DEBUG if getattr(args, "verbose", False) else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # ── Step 1: prepare ──────────────────────────────────────────────────
    print(f"=== Step 1 — Prepare ===")
    print(f"  doi    = {args.doi}")
    try:
        paper = prepare(
            args.doi,
            paper_slug_override=getattr(args, "paper_slug", None),
            input_format=getattr(args, "input_format", "auto"),
        )
    except Exception as e:
        print(f"error: prepare failed: {e}", file=sys.stderr)
        return 3

    print(f"  slug   = {paper.paper_slug}")
    print(f"  title  = {paper.title}")
    print(f"  path   = {paper.extraction_path}")
    print(
        f"  slices = abstract:{len(paper.abstract)}c results:{len(paper.results_text)}c "
        f"captions:{len(paper.captions_text)}c methods:{len(paper.methods_text)}c"
    )
    print(f"  panels = {len(paper.panel_ids)} detected")
    print()

    # ── Steps 2-3: three-agent extraction ────────────────────────────────
    print(f"=== Steps 2-3 — Three-agent extraction ===")
    print(f"  Results-reader   ({cfg.model_results})")
    print(f"  Caption-reader   ({cfg.model_caption})")
    print(f"  Structure-reader ({cfg.model_structure})")
    print(f"  vertex: project={cfg.vertex_project} region={cfg.vertex_region}")
    print()
    try:
        results, caption, structure = run_all_agents(paper, cfg)
    except Exception as e:
        print(f"error: extraction failed: {e}", file=sys.stderr)
        return 4

    print(f"  results-reader   → {len(results.claims):3d} candidate claim(s)")
    print(f"  caption-reader   → {len(caption.claims):3d} candidate claim(s)")
    print(f"  structure-reader → {len(structure.claims):3d} candidate claim(s)")
    print()

    # ── Step 4: reconciliation ───────────────────────────────────────────
    print(f"=== Step 4 — Reconciliation ({cfg.model_reconcile}) ===")
    try:
        draft = reconcile_step(
            results, caption, structure, cfg,
            paper_doi=paper.doi,
            paper_title=paper.title,
        )
    except Exception as e:
        print(f"error: reconciliation failed: {e}", file=sys.stderr)
        return 5

    by_conf: dict[str, int] = {}
    for c in draft.claims:
        by_conf[c.confidence] = by_conf.get(c.confidence, 0) + 1
    print(f"  draft has {len(draft.claims)} claim(s):")
    for k in ("high", "contested", "single-source"):
        if k in by_conf:
            print(f"    {k:14s}  {by_conf[k]:3d}")
    print()

    # ── Write draft to disk ──────────────────────────────────────────────
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    draft_path = cfg.output_dir / f"draft-{paper.paper_slug}.json"
    draft_path.write_text(draft.model_dump_json(indent=2))
    # Also save raw agent outputs for debugging / future tooling
    (cfg.output_dir / f"agents-{paper.paper_slug}.json").write_text(
        json.dumps(
            {
                "results": json.loads(results.model_dump_json()),
                "caption": json.loads(caption.model_dump_json()),
                "structure": json.loads(structure.model_dump_json()),
            },
            indent=2,
        )
    )
    print(f"=== Output ===")
    print(f"  draft  → {draft_path}")
    print(f"  agents → {cfg.output_dir}/agents-{paper.paper_slug}.json")
    print(f"  Next: elife-extract write --draft {draft_path} --corpus-dir {cfg.corpus_dir}")
    return 0


def cmd_write(args: argparse.Namespace) -> int:
    """Steps 5-7: review + dependency mapping + write claim files."""
    cfg = Config.from_args(args)
    errors = cfg.validate()
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        return 2

    import json
    import logging
    from .review import review as review_step
    from .write import write_claim_files
    from .schema import DraftClaimTable

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Load the draft
    draft_path = Path(args.draft).expanduser().resolve()
    if not draft_path.is_file():
        print(f"error: draft not found: {draft_path}", file=sys.stderr)
        return 3

    print(f"=== Step 5 — Review gate ({cfg.review_mode}) ===")
    print(f"  draft = {draft_path}")
    try:
        draft_data = json.loads(draft_path.read_text())
        draft = DraftClaimTable(**draft_data)
    except Exception as e:
        print(f"error: failed to parse draft: {e}", file=sys.stderr)
        return 4

    print(f"  paper = {draft.paper_slug} ({draft.paper_doi})")
    print(f"  claims = {len(draft.claims)} (per-agent: {dict(draft.per_agent_counts)})")
    print()

    # external mode: run Opus reviewer pass before write; substitutes for
    # the human review at Step 5.
    if cfg.review_mode == "external":
        from .prepare import prepare
        from .external_review import external_review
        print(f"  external reviewer: re-fetching paper context for {draft.paper_doi}...")
        try:
            paper = prepare(draft.paper_doi)
        except Exception as e:
            print(f"error: failed to fetch paper for external review: {e}", file=sys.stderr)
            return 5
        print(f"  external reviewer: calling {cfg.model_reconcile}...")
        try:
            revised = external_review(paper, draft, cfg)
        except Exception as e:
            print(f"error: external review failed: {e}", file=sys.stderr)
            return 6
        print(f"  external review: {len(draft.claims)} -> {len(revised.claims)} claims after revision")
        # Save the revised draft alongside the original for audit
        revised_path = draft_path.with_name(draft_path.stem + ".reviewed.json")
        revised_path.write_text(revised.model_dump_json(indent=2))
        print(f"  revised draft saved: {revised_path}")
        approved = revised
    else:
        approved = review_step(draft, cfg)
        if approved is None:
            print("review aborted; no claim files written.", file=sys.stderr)
            return 6
        if cfg.review_mode == "interactive" and len(approved.claims) != len(draft.claims):
            print(
                f"  review: {len(draft.claims)} -> {len(approved.claims)} claims after edit"
            )

    # Step 7: write claim files
    print()
    print(f"=== Steps 6-7 — Write claim files ===")
    print(f"  corpus_dir = {cfg.corpus_dir}")
    print(f"  paper_dir  = {cfg.corpus_dir / approved.paper_slug}")
    try:
        written = write_claim_files(approved, cfg)
    except FileExistsError as e:
        print(f"error: {e}", file=sys.stderr)
        return 7
    except Exception as e:
        print(f"error: write failed: {e}", file=sys.stderr)
        return 8

    print(f"  wrote {len(written)} files:")
    for p in written[:5]:
        print(f"    {p.relative_to(cfg.corpus_dir)}")
    if len(written) > 5:
        print(f"    ... and {len(written) - 5} more")
    print()
    print(f"  Step 6 (dependency mapping) is scaffolded — claim files have empty")
    print(f"  edge sections. Analyst fills in or runs a future edge-inference pass.")
    print(f"  Next: elife-extract verify-refs --paper {approved.paper_slug} --corpus-dir {cfg.corpus_dir}")
    return 0


def cmd_verify_refs(args: argparse.Namespace) -> int:
    """CrossRef DOI resolution for literature-context claims."""
    cfg = Config.from_args(args)
    errors = cfg.validate()
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        return 2

    import logging
    from .verify_refs import verify_refs

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    paper = getattr(args, "paper", None)
    dry_run = getattr(args, "dry_run", False)

    print(f"=== verify-refs (paper={paper}, dry_run={dry_run}) ===")
    print(f"  corpus_dir = {cfg.corpus_dir}")
    print()

    try:
        results = verify_refs(paper, cfg, dry_run=dry_run)
    except Exception as e:
        print(f"error: verify-refs failed: {e}", file=sys.stderr)
        return 3

    # Summarize
    by_status: dict[str, int] = {}
    for r in results:
        by_status[r.status] = by_status.get(r.status, 0) + 1
    print()
    print(f"=== Summary ({len(results)} literature-context claim(s)) ===")
    for status in (
        "confirmed", "found", "low-confidence", "not-found",
        "no-hint", "unresolvable",
    ):
        if status in by_status:
            print(f"  {status:18s} {by_status[status]}")

    n_resolved = by_status.get("confirmed", 0) + by_status.get("found", 0)
    n_total = len(results)
    rate = (n_resolved / n_total * 100) if n_total else 0
    print(f"  {'=' * 30}")
    print(f"  resolution rate    {rate:.1f}% ({n_resolved}/{n_total})")
    if dry_run and "found" in by_status:
        print()
        print(f"  --dry-run: {by_status['found']} new DOI(s) NOT written. Re-run without --dry-run to commit.")
    return 0


def cmd_evaluate(args: argparse.Namespace) -> int:
    """Round-trip evaluation against a curated reference corpus.

    For each named (or all) paper in the reference corpus, run the full
    pipeline (extract -> reconcile -> optional external review -> write)
    and score the CLI's output against the reference. Aggregate per-paper
    scorecards into a multi-paper report.
    """
    import logging
    from .evaluate import evaluate_paper, aggregate_report
    from .config import Config

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    cfg = Config.from_args(args)
    # corpus_dir is not needed for evaluate — we use --reference-dir instead.
    # Minimum required: reference dir exists and prompts dir is reachable.
    if cfg.prompts_dir is None or not cfg.prompts_dir.is_dir():
        print(f"error: prompts dir invalid: {cfg.prompts_dir}", file=sys.stderr)
        return 2

    reference_dir = Path(args.reference_dir).expanduser().resolve()
    if not reference_dir.is_dir():
        print(f"error: reference dir not found: {reference_dir}", file=sys.stderr)
        return 2

    work_root = Path(args.work_dir).expanduser().resolve()
    work_root.mkdir(parents=True, exist_ok=True)

    # Resolve which papers to evaluate
    if args.papers:
        slugs = [s.strip() for s in args.papers.split(",") if s.strip()]
    elif args.all:
        slugs = sorted(p.name for p in reference_dir.iterdir() if p.is_dir())
    else:
        print("error: pass --paper(s), or --all to evaluate the whole corpus", file=sys.stderr)
        return 2

    print(f"=== evaluate ===")
    print(f"  reference_dir = {reference_dir}")
    print(f"  work_dir      = {work_root}")
    print(f"  review_mode   = {args.review_mode}")
    print(f"  papers        = {len(slugs)} ({', '.join(slugs[:6])}{'...' if len(slugs) > 6 else ''})")
    print()

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
        card = evaluate_paper(
            ref_paper_dir=ref_paper_dir,
            work_dir=paper_work_dir,
            cfg=cfg,
            review_mode=args.review_mode,
        )
        cards.append(card)
        if card.error:
            print(f"[{i}/{len(slugs)}] {slug}: FAILED ({card.error})")
        else:
            print(
                f"[{i}/{len(slugs)}] {slug}: "
                f"recovery={card.recovery_pct:.0f}%, "
                f"panel={card.panel_pct:.0f}%, "
                f"role={card.role_pct:.0f}% "
                f"({card.n_cli} CLI vs {card.n_ref} ref)"
            )

    # Aggregate report
    out_path = work_root / "aggregate-scorecard.md"
    aggregate_report(
        cards=cards,
        out_path=out_path,
        reference_dir=reference_dir,
        work_root=work_root,
        review_mode=args.review_mode,
    )
    print()
    print(f"aggregate scorecard: {out_path}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    """Composed shorthand: extract + write + verify-refs in sequence.

    Implies --auto-approve (the human review gate is bypassed). For
    interactive use, run the three subcommands separately.
    """
    print(f"[stub] run (composed):")
    print(f"  doi          = {args.doi}")
    print(f"  --auto-approve implied (review gate bypassed)")
    print()
    print("Sequencing extract → write → verify-refs (each currently a stub).")
    print()

    # Stub: just call them in sequence with the auto-approve flag set.
    args.review_mode = "auto-approve"
    args.draft = None  # to be filled by extract's output
    args.paper = None  # to be filled by write's output
    rc = cmd_extract(args)
    if rc != 0:
        return rc
    rc = cmd_write(args)
    if rc != 0:
        return rc
    rc = cmd_verify_refs(args)
    return rc


# ── Argument parser construction ──────────────────────────────────────────


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    """Args shared across all subcommands."""
    parser.add_argument(
        "--corpus-dir",
        type=Path,
        help="Where claim files are read/written. Required (or set ELIFE_CORPUS_DIR).",
    )
    parser.add_argument(
        "--prompts-dir",
        type=Path,
        help="Override the prompts directory (default: package-local prompts/).",
    )
    parser.add_argument(
        "--prompt-variant",
        default=DEFAULT_PROMPT_VARIANT,
        help=f"Named prompt variant under prompts/<variant>/ (default: {DEFAULT_PROMPT_VARIANT}).",
    )


def _add_model_args(parser: argparse.ArgumentParser) -> None:
    """Model-routing knobs for the extraction subcommands."""
    parser.add_argument(
        "--model-results",
        default=None,
        help=f"Model for the Results-reader agent (default: {DEFAULT_MODEL_RESULTS}).",
    )
    parser.add_argument(
        "--model-caption",
        default=None,
        help=f"Model for the Caption-reader agent (default: {DEFAULT_MODEL_CAPTION}).",
    )
    parser.add_argument(
        "--model-structure",
        default=None,
        help=f"Model for the Structure-reader agent (default: {DEFAULT_MODEL_STRUCTURE}).",
    )
    parser.add_argument(
        "--model-reconcile",
        default=None,
        help=f"Model for the reconciliation step (default: {DEFAULT_MODEL_RECONCILE}).",
    )
    parser.add_argument(
        "--vertex-project",
        default=None,
        help="Vertex AI project ID (default: VERTEX_PROJECT_ID env or cr-mainen).",
    )
    parser.add_argument(
        "--vertex-region",
        default=None,
        help="Vertex AI region (default: VERTEX_REGION env or europe-west1).",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="elife-extract",
        description=(
            "8-step claim induction pipeline for eLife papers. "
            "Three-agent extraction → reconciliation → review → write. "
            "See: ~/Projects/mainenlab/elife-claim-trees/docs/method.md § 3."
        ),
    )
    parser.add_argument("--version", action="version", version=f"elife-extract {__version__}")

    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    # ── extract ──────────────────────────────────────────────────────────
    p_extract = sub.add_parser(
        "extract",
        help="Steps 1-4: fetch paper, run three-agent extraction, reconcile.",
        description=(
            "Fetch paper, do abstract scan, run the three-agent extraction "
            "(Results / Caption / Structure), and reconcile into a draft "
            "claim table. No claim files are written; the draft is emitted "
            "as JSON for the write subcommand to consume after review."
        ),
    )
    p_extract.add_argument("--doi", required=True, help="eLife paper DOI (e.g., 10.7554/eLife.95562).")
    p_extract.add_argument(
        "--input-format",
        choices=["auto", "jats", "pdf"],
        default="auto",
        help="Input source: jats (structured XML, default for eLife), pdf (fallback), auto (jats for eLife DOIs).",
    )
    p_extract.add_argument(
        "--paper-slug",
        help="Override the slug derived from DOI/title (e.g., headley-2026-inhibitory-rhythms).",
    )
    p_extract.add_argument(
        "--max-claims",
        type=int,
        default=None,
        help="Hard cap on per-paper claim count (cost control for batches).",
    )
    p_extract.add_argument(
        "--no-retry-on-thin",
        dest="retry_on_thin",
        action="store_false",
        default=True,
        help="Disable retrying an agent if its output looks thin.",
    )
    p_extract.add_argument(
        "--reconcile-strategy",
        choices=["confidence-tagged", "union", "intersection-only", "majority-vote"],
        default="confidence-tagged",
        help="How to handle disagreements between agents (default: confidence-tagged).",
    )
    _add_common_args(p_extract)
    _add_model_args(p_extract)
    p_extract.set_defaults(func=cmd_extract)

    # ── write ────────────────────────────────────────────────────────────
    p_write = sub.add_parser(
        "write",
        help="Steps 5-7: review + dependency mapping + write claim files.",
        description=(
            "Take a draft claim table from extract, present it for human "
            "review (or skip review with --review-mode=auto-approve), map "
            "dependency edges, generate UUIDs, and write claim .md files "
            "into the corpus."
        ),
    )
    p_write.add_argument("--draft", required=True, type=Path, help="Path to draft claim JSON from extract.")
    p_write.add_argument(
        "--review-mode",
        choices=["interactive", "auto-approve", "external", "dry-run"],
        default="interactive",
        help=(
            "Step 5 review gate handling: interactive (open $EDITOR), "
            "auto-approve (skip review for tests/demos), external (run Opus "
            "reviewer pass before write — substitutes for human review), "
            "or dry-run (print only)."
        ),
    )
    _add_common_args(p_write)
    p_write.set_defaults(func=cmd_write)

    # ── verify-refs ──────────────────────────────────────────────────────
    p_refs = sub.add_parser(
        "verify-refs",
        help="CrossRef DOI resolution for literature-context claims.",
        description=(
            "For each literature-context claim in the named paper, resolve "
            "the cited reference via CrossRef and write the verified DOI "
            "back to the claim's frontmatter. Flags unresolvable references."
        ),
    )
    p_refs.add_argument(
        "--paper",
        default=None,
        help="Paper slug under corpus-dir/. Omit to sweep the whole corpus.",
    )
    p_refs.add_argument(
        "--dry-run",
        action="store_true",
        help="Print resolutions without writing back to claim files.",
    )
    _add_common_args(p_refs)
    p_refs.set_defaults(func=cmd_verify_refs)

    # ── evaluate (multi-paper round-trip) ────────────────────────────────
    p_eval = sub.add_parser(
        "evaluate",
        help="Round-trip score CLI output against a curated reference corpus.",
        description=(
            "For each paper in the reference corpus (or a named subset), "
            "run extract -> reconcile -> optional external review -> write, "
            "score against the reference, and aggregate per-paper scorecards "
            "into a multi-paper report. Use to validate prompt iterations "
            "before deploying."
        ),
    )
    p_eval.add_argument(
        "--reference-dir", required=True,
        help="Path to the curated reference corpus (e.g., elife-claim-trees/claims/).",
    )
    p_eval.add_argument(
        "--work-dir", required=True,
        help="Where per-paper extraction artifacts and scorecards go.",
    )
    grp = p_eval.add_mutually_exclusive_group()
    grp.add_argument(
        "--paper", dest="papers",
        help="Single paper slug (in reference dir) to evaluate.",
    )
    grp.add_argument(
        "--papers",
        help="Comma-separated list of paper slugs to evaluate.",
    )
    grp.add_argument(
        "--all", action="store_true",
        help="Evaluate every paper directory under reference-dir.",
    )
    p_eval.add_argument(
        "--review-mode",
        choices=["auto-approve", "external"],
        default="external",
        help="How the write step is run for each paper (default: external).",
    )
    p_eval.add_argument(
        "--skip-existing", action="store_true",
        help="Skip papers that already have a scorecard.json under work-dir.",
    )
    _add_model_args(p_eval)
    p_eval.add_argument(
        "--prompts-dir", type=Path,
        help="Override the prompts directory (default: package-local prompts/).",
    )
    p_eval.add_argument(
        "--prompt-variant", default="default",
        help="Named prompt variant under prompts/<variant>/.",
    )
    p_eval.set_defaults(func=cmd_evaluate)

    # ── run (composed shorthand) ─────────────────────────────────────────
    p_run = sub.add_parser(
        "run",
        help="Composed shorthand: extract + write + verify-refs (--auto-approve implied).",
        description=(
            "End-to-end run for tests, demos, and batch extraction. The "
            "human review gate is bypassed (review-mode=auto-approve). "
            "For interactive runs that go through human review, invoke "
            "extract / write / verify-refs separately."
        ),
    )
    p_run.add_argument("--doi", required=True, help="eLife paper DOI.")
    p_run.add_argument(
        "--input-format", choices=["auto", "jats", "pdf"], default="auto",
        help="Input source (default: auto = jats for eLife DOIs).",
    )
    p_run.add_argument("--paper-slug", help="Override slug.")
    p_run.add_argument("--max-claims", type=int, default=None)
    p_run.add_argument(
        "--reconcile-strategy",
        choices=["confidence-tagged", "union", "intersection-only", "majority-vote"],
        default="confidence-tagged",
    )
    _add_common_args(p_run)
    _add_model_args(p_run)
    p_run.set_defaults(func=cmd_run)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
