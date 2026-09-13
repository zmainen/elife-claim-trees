#!/usr/bin/env python3
"""Adjudicate a whole claim tree: the skeleton, the validator, the approval, the apply.

The reading itself is a person's — claim by claim, part by part, edge by edge — and it is
recorded in a verdict file beside the tree it was made against:

    runs/<paper>/claim-tree.v<N>.verdicts.jsonl

This is the tooling around that file. The surface in the site's Reader writes the same file
through a dev endpoint (#78's pattern); this script is the same four operations from the
command line, for a reader who would rather edit the file, and for the maintainer who applies
what a reading decided.

    python3 scripts/verdicts.py skeleton <paper>          # pre-fill keep/ok, so reading is editing
    python3 scripts/verdicts.py validate <paper>          # refuse the four things it must not say
    python3 scripts/verdicts.py approve  <paper> --by NAME # record the reading as an approval
    python3 scripts/verdicts.py apply    <paper> --write   # corrected tree → the next version

`skeleton` writes a `keep` for every claim and an `ok` for every edge, each `considered: false`,
so a claim the reader never opens stays `keep` and the surface flips `considered` on the ones
they weigh. `approve` names the verdict file in the approval, so `pipeline.py state` shows the
`claim-tree` cell approved for the version the reading was made on. `apply` is the maintainer's
call — it writes the corrected roles, panels and edges into a new claim-tree version through
`write --replace`'s carry machinery, and it does nothing without `--write`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "extract"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline  # noqa: E402
from elife_extract import verdicts as vd  # noqa: E402


# ── locating a paper's current tree and version ────────────────────────────────

def current_version(paper: str) -> int | None:
    """The claim-tree version on the ledger — the version the committed tree is."""
    run = pipeline._latest(pipeline.read_ledger(paper), "claim-tree")
    return run["v"] if run else None


def claim_dir(paper: str) -> Path:
    return ROOT / "claims" / paper


def resolve_paper_version(paper: str, v: int | None) -> tuple[int, Path]:
    """The version to act on and the claim directory that holds it.

    Defaults to the version on the ledger, which is the committed tree in `claims/<paper>/`. A
    named older version reads from its archive under `runs/`.
    """
    latest = current_version(paper)
    if latest is None:
        raise SystemExit(f"error: claim-tree has never run for {paper!r}")
    v = v if v is not None else latest
    if v == latest:
        return v, claim_dir(paper)
    archived = ROOT / "runs" / paper / f"claim-tree.v{v}"
    if not archived.is_dir():
        raise SystemExit(f"error: no archived tree for {paper} v{v} at {archived}")
    return v, archived


def _tree(paper: str, v: int | None):
    v, cdir = resolve_paper_version(paper, v)
    slugs, edges = vd.load_tree(cdir)
    return v, cdir, slugs, edges


# ── skeleton ────────────────────────────────────────────────────────────────

def cmd_skeleton(args) -> int:
    v, cdir, slugs, edges = _tree(args.paper, args.v)
    path = vd.verdicts_path(ROOT, args.paper, v)
    if path.exists() and not args.force:
        print(f"error: {path.relative_to(ROOT)} already exists — reading it would overwrite a "
              f"reading. Pass --force to replace it.", file=sys.stderr)
        return 1
    records = vd.skeleton(slugs, edges, by=args.by)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        import json
        for rec in records:
            fh.write(json.dumps(rec) + "\n")
    print(f"{args.paper} claim-tree v{v}: wrote {len(slugs)} claim + {len(edges)} edge "
          f"verdicts (all keep/ok, considered: false)")
    print(f"  {path.relative_to(ROOT)}")
    print("  The reading is now editing this file — in the site's Reader, or by hand.")
    return 0


# ── validate ────────────────────────────────────────────────────────────────

def cmd_validate(args) -> int:
    v, cdir, slugs, edges = _tree(args.paper, args.v)
    path = vd.verdicts_path(ROOT, args.paper, v)
    if not path.is_file():
        print(f"error: no verdict file at {path.relative_to(ROOT)} — run `skeleton` first",
              file=sys.stderr)
        return 2
    records = vd.load(path)
    problems = vd.validate(records, claim_slugs=slugs, edge_triples=edges)
    res = vd.resolve(records)
    complete = vd.is_complete(records, claim_slugs=slugs, edge_triples=edges)
    print(f"{args.paper} claim-tree v{v}: {len(records)} verdict line(s), "
          f"{len(res.claims)}/{len(slugs)} claims and {len(res.edges)}/{len(edges)} edges decided "
          f"({len(res.claims_considered())} claims, {len(res.edges_considered())} edges considered)")
    if not complete:
        print("  incomplete: some claims or edges carry no verdict "
              "(run `skeleton` to pre-fill them)")
    if problems:
        print(f"\n  {len(problems)} problem(s):")
        for p in problems:
            print(f"    - {p}")
        return 1
    print("  valid.")
    return 0


# ── approve ─────────────────────────────────────────────────────────────────

def cmd_approve(args) -> int:
    v, cdir, slugs, edges = _tree(args.paper, args.v)
    path = vd.verdicts_path(ROOT, args.paper, v)
    if not path.is_file():
        print(f"error: no verdict file at {path.relative_to(ROOT)} — nothing to approve",
              file=sys.stderr)
        return 2
    records = vd.load(path)
    problems = vd.validate(records, claim_slugs=slugs, edge_triples=edges)
    if problems:
        print(f"error: the verdict file is invalid; fix it before approving:", file=sys.stderr)
        for p in problems:
            print(f"    - {p}", file=sys.stderr)
        return 1
    if not vd.is_complete(records, claim_slugs=slugs, edge_triples=edges):
        print("warning: some claims or edges carry no verdict — approving a partial reading")

    # The same code path as `pipeline.py approve <paper> claim-tree --v <N> --by NAME --note`.
    # The note names the verdict file, so the approval records what was read.
    run = pipeline._latest(pipeline.read_ledger(args.paper), "claim-tree")
    note = args.note or str(path.relative_to(ROOT))
    rec = pipeline.approve(args.paper, "claim-tree", v, by=args.by, note=note)
    current = " (the current version)" if run and v == run.get("v") else \
              f" (superseded — the ledger is at v{run.get('v')})" if run else ""
    print(f"{args.paper}/claim-tree v{v} approved by {rec['by']}{current}")
    print(f"  note: {note}")
    print("  `python3 scripts/pipeline.py state` now shows the cell approved.")
    return 0


# ── apply ─────────────────────────────────────────────────────────────────────

def _draft_from_tree(paper: str, cdir: Path, res: "vd.Resolved"):
    """Rebuild the writer's input from a committed tree, with the verdicts applied.

    There is no reader in the package that reconstructs a `DraftClaimTable` from claim files —
    every other caller feeds it from the reconciler's JSON — so it is assembled here from the
    frontmatter, dropping struck and merged-away claims, correcting role and panel, and setting
    `part_of` where a verdict ruled one. The edges are the tree's relations with the edge
    verdicts applied. Returns (draft, edges) for `write_claim_files`.
    """
    from elife_extract.schema import DraftClaimTable, ReconciledClaim

    struck = res.struck
    merged = res.merged            # slug → the claim it folds into
    part_of_v = res.part_of        # slug → the whole a verdict makes it a part of

    # slug → claim sentence, for resolving part_of back to the sentence the writer expects.
    sentence: dict[str, str] = {}
    fm_by_slug: dict[str, dict] = {}
    for p in sorted(cdir.glob("*.md")):
        if p.name == "index.md":
            continue
        fm = vd.read_frontmatter(p)
        if fm:
            slug = fm.get("slug") or p.stem
            fm_by_slug[slug] = fm
            sentence[slug] = " ".join(str(fm.get("claim", "")).split())

    doi = pipeline._doi_of(paper) or ""
    claims: list[ReconciledClaim] = []
    kept_slugs: set[str] = set()
    for slug, fm in fm_by_slug.items():
        if slug in struck or slug in merged:
            continue                                  # struck, or folded into its duplicate
        cv = res.claims.get(slug, {})
        role = cv.get("role") or fm.get("role") or "empirical"
        panel = cv.get("panel")
        if panel is None:
            assertions = fm.get("assertions") or []
            panel = assertions[0].get("panel") if assertions and isinstance(assertions[0], dict) else None
        # part_of: a verdict's ruling wins; otherwise the tree's own part-of, if any.
        whole = part_of_v.get(slug) or (fm.get("part-of") or [None])[0]
        claims.append(ReconciledClaim(
            claim=fm.get("claim", "").strip(),
            panel=panel,
            claim_type=fm.get("claim-type") or "empirical",
            role=role,
            addresses=None,          # the questions layer re-runs against the new tree
            confidence="single-source",
            sources=[],
            notes=None,
            part_of=sentence.get(whole) if whole else None,
        ))
        kept_slugs.add(slug)

    # Edges: the tree's relations, folded through merges, with the verdicts applied. `part-of`
    # is not here — the writer rebuilds it from each claim's `part_of`.
    _, triples = vd.load_tree(cdir)

    def fold(s: str) -> str:
        seen = {s}
        while s in merged:
            s = merged[s]
            if s in seen:
                break
            seen.add(s)
        return s

    edges: list[dict] = []
    seen_e: set[tuple[str, str, str]] = set()

    def add(s: str, t: str, rel: str):
        s, t = fold(s), fold(t)
        if s in struck or t in struck or s == t or s not in kept_slugs or t not in kept_slugs:
            return
        key = (s, t, rel)
        if key not in seen_e:
            seen_e.add(key)
            edges.append({"source": s, "target": t, "relation": rel})

    for s, t, rel in triples:
        v = res.edges.get((s, t, rel))
        verdict = v.get("verdict") if v else "ok"
        if verdict == "strike":
            continue
        if verdict == "wrong-relation":
            add(s, t, v.get("corrected") or rel)
        elif verdict == "wrong-direction":
            add(t, s, v.get("corrected") or rel)
        else:
            add(s, t, rel)
    for (s, t, rel), v in res.edges.items():
        if v.get("verdict") == "missing" and (s, t, rel) not in seen_e:
            add(s, t, v.get("corrected") or rel)

    draft = DraftClaimTable(
        paper_slug=paper, paper_doi=doi,
        paper_title=None, claims=claims,
        model="adjudication",
    )
    return draft, edges


def cmd_apply(args) -> int:
    v, cdir, slugs, edges_tree = _tree(args.paper, args.v)
    latest = current_version(args.paper)
    if v != latest:
        print(f"error: can only apply the current version (v{latest}); v{v} is archived",
              file=sys.stderr)
        return 2
    path = vd.verdicts_path(ROOT, args.paper, v)
    if not path.is_file():
        print(f"error: no verdict file at {path.relative_to(ROOT)}", file=sys.stderr)
        return 2
    records = vd.load(path)
    problems = vd.validate(records, claim_slugs=slugs, edge_triples=edges_tree)
    if problems:
        print("error: the verdict file is invalid; fix it before applying:", file=sys.stderr)
        for p in problems:
            print(f"    - {p}", file=sys.stderr)
        return 1
    res = vd.resolve(records)

    from elife_extract.config import Config
    from elife_extract.write import archive_dir, carry_over, write_claim_files
    cfg = Config()
    cfg.root = ROOT
    cfg.corpus_dir = ROOT / "claims"

    draft, edges = _draft_from_tree(args.paper, cdir, res)
    print(f"=== apply {args.paper} claim-tree v{v} → v{v + 1} ===")
    print(f"  {len(res.struck)} struck, {len(res.merged)} merged, {len(res.part_of)} part-of; "
          f"{len(draft.claims)} claims and {len(edges)} edges in the corrected tree")
    if not args.write:
        print("\nnothing written — pass --write to archive the current tree and write the "
              "corrected one as the next version")
        return 0

    paper_dir = cfg.corpus_dir / args.paper
    replacing = paper_dir.exists() and any(paper_dir.iterdir())
    written = write_claim_files(draft, cfg, edges=edges, replace=True)
    print(f"  wrote {len(written)} file(s) into {paper_dir.relative_to(ROOT)}")
    if replacing:
        arch = archive_dir(cfg, args.paper)
        s = carry_over(cfg, args.paper, arch)
        print(f"  archived previous version to {arch.relative_to(ROOT)}")
        print(f"  carried: {len(s['alt_claims'])} alt- claim(s), {len(s['rules_out'])} "
              f"rules-out edge(s), {len(s['reproductions'])} reproduction record(s)"
              + (f"; {len(s['unplaced'])} unplaced" if s["unplaced"] else ""))
    print("\n  Record the new version on the ledger with:")
    print(f"    python3 scripts/pipeline.py run {args.paper} claim-tree --no-deps "
          f"--note 'adjudicated tree from {path.relative_to(ROOT)}'")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("skeleton", help="pre-fill keep/ok for every claim and edge")
    s.add_argument("paper")
    s.add_argument("--v", type=int, help="which version (default: the one on the ledger)")
    s.add_argument("--by", default="skeleton", help="who the pre-fill is attributed to")
    s.add_argument("--force", action="store_true", help="overwrite an existing verdict file")
    s.set_defaults(fn=cmd_skeleton)

    val = sub.add_parser("validate", help="refuse the four things a verdict file must not say")
    val.add_argument("paper")
    val.add_argument("--v", type=int, help="which version (default: the one on the ledger)")
    val.set_defaults(fn=cmd_validate)

    a = sub.add_parser("approve", help="record the reading as a version-bound approval")
    a.add_argument("paper")
    a.add_argument("--by", required=True, help="who read it")
    a.add_argument("--v", type=int, help="which version (default: the one on the ledger)")
    a.add_argument("--note", help="what they checked (default: the verdict file path)")
    a.set_defaults(fn=cmd_approve)

    ap_ = sub.add_parser("apply", help="write the corrected tree as the next version")
    ap_.add_argument("paper")
    ap_.add_argument("--v", type=int, help="which version (default: the one on the ledger)")
    ap_.add_argument("--write", action="store_true", help="actually write (default: dry-run)")
    ap_.set_defaults(fn=cmd_apply)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
