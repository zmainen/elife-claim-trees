"""Round-trip evaluation — score CLI output against a curated reference corpus.

What this module does
─────────────────────
For each paper:
  1. Read the reference paper's index.md to get the DOI.
  2. Run prepare → readers → reconcile → (external-review) → edges → write
     through the same layer runners that `pipeline.py run` uses, into a
     temporary root (`work_dir`), so the chain scored is the declared one and
     the temp root gets its own artifacts.
  3. Find the approved reference: if `runs/<paper>/approvals.jsonl` records an
     approval of the `claim-tree` layer, use that version's archived directory
     (`runs/<paper>/claim-tree.v<N>/`); if no approval exists, use the
     committed tree and say so in `reference`.
  4. Run the CrossRef-style matcher to align CLI claims with reference claims.
     The matcher call is factorable: `--dump-prompts` writes the prompt to a
     file and exits; `--answers` replays a directory of answers; `--matcher-
     answer` supplies the alignment directly.
  5. Score: claim recovery, precision, panel, role, edge recovery, role
     confusion.
  6. Save a per-paper scorecard.

After all papers complete, render an aggregate scorecard.

Offline / no-backend workflow
──────────────────────────────
  evaluate --dump-prompts <dir>   write every prompt for each paper to <dir>/
                                  named by layer; also writes matcher.json.
                                  Exits without calling any model.
  evaluate --answers <dir>        replay a directory of layer answers (one JSON
                                  file per layer, named by layer id, e.g.
                                  results-reader.json, reconcile.json).
  --matcher-answer <file>         supply a pre-computed alignment instead of
                                  calling the matcher model.

The score subcommand
─────────────────────
  evaluate score --reference <dir> --candidate <dir> --pairs <file>

  Score two claim directories against each other using pre-computed pairs,
  with no model call. Accepts the pairs format from `match.v3.pairs.json`
  (`[{committed, rerun, note}]`) as well as the matcher's own format
  (`{matches: [{ref_slug, cli_slug, ...}]}`). Reports recovery, precision,
  panel, role, edges and role confusion in the same style as pairs.py.
"""

from __future__ import annotations

import json
import logging
import re
import shutil
import statistics
from collections import defaultdict
from dataclasses import dataclass, field, asdict, replace
from datetime import date
from pathlib import Path

import yaml

from . import verdicts as vd
from .agents import stream_text
from .config import Config

logger = logging.getLogger(__name__)


# ── Per-claim representation for the matcher ────────────────────────────


@dataclass
class Claim:
    slug: str
    claim: str
    panel: str | None
    role: str
    claim_type: str | None = None
    source: str = ""  # "ref" or "cli"


def _read_frontmatter(path: Path) -> dict:
    text = path.read_text()
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm_text = parts[1]
    # Tolerate the canonical script's quirk: bare `[]` on next line after a key
    fm_fixed = re.sub(r"^(\w[\w-]*):\n\[\]", r"\1: []", fm_text, flags=re.MULTILINE)
    try:
        return yaml.safe_load(fm_fixed) or {}
    except yaml.YAMLError:
        return {}


def load_claims(claim_dir: Path, source: str) -> list[Claim]:
    """Load all claim files from a paper directory (skip index.md)."""
    claims = []
    for path in sorted(claim_dir.glob("*.md")):
        if path.name == "index.md":
            continue
        fm = _read_frontmatter(path)
        if not fm:
            continue
        slug = fm.get("slug") or path.stem
        panel = None
        assertions = fm.get("assertions") or []
        if assertions and isinstance(assertions[0], dict):
            panel = assertions[0].get("panel")
        claims.append(Claim(
            slug=slug,
            claim=(fm.get("claim", "") or "").strip().replace("\n", " "),
            panel=panel,
            role=fm.get("role", ""),
            claim_type=fm.get("claim-type"),
            source=source,
        ))
    return claims


# ── Edge loading ─────────────────────────────────────────────────────────


def _edge_keys() -> set[str]:
    """The relation vocabulary, loaded from scripts/relations.py once."""
    import importlib.util
    p = Path(__file__).resolve().parents[2] / "scripts" / "relations.py"
    if not p.is_file():
        # Fallback to a minimal set so the module is importable without the scripts dir.
        return {"supports", "tests", "validates", "confirms", "predicts", "extends",
                "replicates", "contradicts", "opposes", "refutes", "rules-out",
                "dissociates-with", "entails", "derived-from", "interprets",
                "enables-method", "scopes", "requires", "qualifies", "part-of"}
    spec = importlib.util.spec_from_file_location("relations", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod.EDGE_KEYS


def load_edges(claim_dir: Path) -> list[tuple[str, str, str]]:
    """Load (source, target, relation) triples from a paper's claim files.

    Reads every top-level relation key (EDGE_KEYS) and the `belongings` list.
    Returns a list of unique triples (de-duplicated within each file).
    """
    keys = _edge_keys()
    triples: list[tuple[str, str, str]] = []
    for path in sorted(claim_dir.glob("*.md")):
        if path.name == "index.md":
            continue
        fm = _read_frontmatter(path)
        if not fm:
            continue
        slug = fm.get("slug") or path.stem
        seen: set[tuple[str, str, str]] = set()

        def _add(src: str, tgt: str, rel: str) -> None:
            t = (src, tgt, rel)
            if t not in seen:
                seen.add(t)
                triples.append(t)

        for key in sorted(keys):
            for tgt in (fm.get(key) or []):
                if isinstance(tgt, str):
                    _add(slug, tgt, key)
        for item in (fm.get("belongings") or []):
            if isinstance(item, dict):
                rel = item.get("relation")
                tgt = item.get("target")
                if rel and tgt:
                    _add(slug, tgt, rel)
    return triples


# ── Approved reference lookup ─────────────────────────────────────────────


def find_approved_tree(
    paper_slug: str,
    root: Path,
    committed_dir: Path,
) -> tuple[Path, str]:
    """Find the most recently approved claim-tree version for a paper.

    Returns (ref_dir, reference_status) where reference_status is
    "approved v<N>" or "unapproved". Uses the approvals pipeline.py
    writes to runs/<paper>/approvals.jsonl.

    If an approved version exists and its archived directory is present at
    runs/<paper>/claim-tree.v<N>/, that directory is returned. Otherwise
    the committed_dir is returned with the approval status still noted.
    """
    approvals_path = root / "runs" / paper_slug / "approvals.jsonl"
    if not approvals_path.is_file():
        return committed_dir, "unapproved"

    approvals: list[dict] = []
    with approvals_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    approvals.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    ct_approvals = [a for a in approvals if a.get("layer") == "claim-tree"]
    if not ct_approvals:
        return committed_dir, "unapproved"

    latest = max(ct_approvals, key=lambda a: (a.get("v", 0), a.get("when", "")))
    v = latest.get("v", 1)
    status = f"approved v{v}"

    # The approved version is archived at runs/<paper>/claim-tree.v<N>/ when
    # the layer was subsequently replaced. If the archive dir is absent, the
    # approved version is the current committed tree (it has not been replaced
    # since the approval).
    archived = root / "runs" / paper_slug / f"claim-tree.v{v}"
    if archived.is_dir() and any(archived.glob("*.md")):
        return archived, status

    # No archive — check if the committed dir looks like the approved version.
    return committed_dir, status


# ── Matcher prompt ───────────────────────────────────────────────────────


MATCHER_PROMPT = """You are scoring a claim-extraction CLI against a human-curated reference corpus.

# Inputs

You receive two lists of claims about the same paper:
- REFERENCE: human-curated, the gold standard.
- CLI: produced by an automated 8-step extraction pipeline.

# Task

For each REFERENCE claim, identify the best matching CLI claim (or null if no match).

Two claims match if they assert the same proposition about the paper's content, even when phrased differently. They do NOT need to share the same panel ID, role classification, or quantitative phrasing — those are scored separately. The match is at the level of "this is the same finding."

Indicators of a match:
- Same direction of relationship (X increases Y, not X decreases Y)
- Same entities or compatible synonyms
- Same outcome
- One is a strict refinement of the other

A reference claim may match multiple CLI claims (the CLI may have split it). Pick the single best — the most specific CLI claim that captures the reference's full proposition. If multiple CLI claims jointly capture one reference claim but no single one captures the whole, pick the one that captures the most.

# Output

A JSON object:

```json
{
  "matches": [
    {
      "ref_slug": "<reference claim slug>",
      "cli_slug": "<best matching CLI claim slug or null>",
      "match_quality": "exact | partial | none",
      "panel_match": true | false | "n/a",
      "role_match": true | false | "n/a",
      "notes": "<short note when relevant>"
    }
  ]
}
```

Field guidance:
- `match_quality`:
  - `exact` — the CLI claim asserts the same proposition with the same direction and entities; phrasing may differ.
  - `partial` — the CLI claim captures a strict subset or superset of the reference proposition.
  - `none` — no CLI claim captures the reference proposition.
- `panel_match`: true if both claims have the same panel ID (or both are null/synthesis-level); false if they differ; "n/a" if no match.
- `role_match`: true if both have the same role; false if they differ; "n/a" if no match.
- `notes`: short context for ambiguous matches or systematic CLI failures (e.g., "CLI split this into 3 narrower claims; chose the closest").

Return only the JSON object, no surrounding prose.
"""


def _format_claim_list(claims: list[Claim], label: str) -> str:
    lines = [f"## {label} ({len(claims)} claims)\n"]
    for c in claims:
        lines.append(f"- **{c.slug}** [panel={c.panel}, role={c.role}]: {c.claim}")
    return "\n".join(lines)


def matcher_prompt_inputs(
    ref_claims: list[Claim],
    cli_claims: list[Claim],
) -> tuple[str, str]:
    """Return (system, user) for the matcher, without calling any model."""
    user = (
        _format_claim_list(ref_claims, "REFERENCE")
        + "\n\n"
        + _format_claim_list(cli_claims, "CLI")
        + "\n\nReturn the JSON object as instructed."
    )
    return MATCHER_PROMPT, user


def run_matcher(
    ref_claims: list[Claim],
    cli_claims: list[Claim],
    cfg: Config,
    *,
    dump_prompt: Path | None = None,
    answer: Path | None = None,
) -> dict:
    """Align reference and CLI claims. Return parsed mapping.

    dump_prompt — if set, write {system, user} JSON there and raise
        _DumpedPrompt so the caller can skip the model call.
    answer — if set, read the raw model reply from this file instead of
        calling the backend.
    """
    system, user = matcher_prompt_inputs(ref_claims, cli_claims)

    if dump_prompt is not None:
        dump_prompt.parent.mkdir(parents=True, exist_ok=True)
        dump_prompt.write_text(json.dumps({"system": system, "user": user}, indent=2,
                                          ensure_ascii=False))
        raise _DumpedPrompt(str(dump_prompt))

    if answer is not None:
        raw = answer.read_text(encoding="utf-8").strip()
    else:
        raw = stream_text(
            cfg,
            model=cfg.model_reconcile,
            system=system,
            user=user,
            max_tokens=32768,
            label="matcher",
        ).strip()

    raw = re.sub(r"^```(?:json)?\s*\n?", "", raw, count=1, flags=re.IGNORECASE)
    raw = re.sub(r"\n?```\s*$", "", raw, count=1)
    return json.loads(raw)


class _DumpedPrompt(Exception):
    """Raised when a prompt has been dumped and the caller should not proceed."""


# ── Pairs format normalisation ────────────────────────────────────────────


def _normalize_pairs(pairs_data: object) -> list[dict]:
    """Accept either pairs format and return a canonical matches list.

    Format A (matcher output): {"matches": [{ref_slug, cli_slug, match_quality, ...}]}
    Format B (match.v*.pairs.json): [{committed, rerun, note}]

    Format B is treated as if every entry is an exact match with no panel/role info,
    so the caller can score recovery and role agreement without re-querying a model.
    """
    if isinstance(pairs_data, dict):
        return pairs_data.get("matches", [])
    if isinstance(pairs_data, list):
        out = []
        for p in pairs_data:
            if not isinstance(p, dict):
                continue
            ref_slug = p.get("committed") or p.get("ref_slug")
            cli_slug = p.get("rerun") or p.get("cli_slug")
            if not ref_slug or not cli_slug:
                continue
            out.append({
                "ref_slug": ref_slug,
                "cli_slug": cli_slug,
                "match_quality": p.get("match_quality", "exact"),
                "panel_match": p.get("panel_match", "n/a"),
                "role_match": p.get("role_match", "n/a"),
                "notes": p.get("note") or p.get("notes", ""),
            })
        return out
    return []


# ── Scoring ───────────────────────────────────────────────────────────────


@dataclass
class PaperScorecard:
    """Per-paper round-trip scoring result."""

    paper_slug: str
    paper_doi: str
    n_ref: int
    n_cli: int
    n_recovered: int
    n_exact: int
    n_partial: int
    n_panel_match: int
    n_role_match: int
    matches: list[dict] = field(default_factory=list)
    review_mode: str = "auto-approve"
    cli_dir: str = ""
    error: str | None = None

    # ── new fields ──────────────────────────────────────────────────────
    # Precision: how many of the CLI claims are matched to any ref claim.
    # n_cli_parts counts CLI claims that carry a part-of relation, as a
    # separate informational tally (they inflate n_cli without necessarily
    # inflating n_cli_matched).
    n_cli_matched: int = 0
    n_cli_parts: int = 0

    # Edge recovery: of the reference edges between matched claim pairs, how
    # many does the CLI tree reproduce with the same relation on the same pair.
    # n_cli_extra_edges: CLI edges on matched pairs that have no ref counterpart.
    n_ref_edges_on_matched: int = 0
    n_edge_recovered: int = 0
    n_cli_extra_edges: int = 0

    # Per-role confusion over matched pairs: {(ref_role, cli_role): count}.
    role_confusion: dict = field(default_factory=dict)

    # Reference status: "approved v<N>", "approved v<N> (committed)", or "unapproved".
    reference: str = "unapproved"

    # Which model profile produced the candidate this was scored against (#85). Empty when the
    # candidate was not produced under a named profile.
    profile: str = ""

    # A free note the evaluation layer surfaces beside the row — what the candidate is, or a
    # caveat about the reference. Empty by default.
    note: str = ""

    @property
    def recovery_pct(self) -> float:
        return self.n_recovered / self.n_ref * 100 if self.n_ref else 0.0

    @property
    def panel_pct(self) -> float:
        return self.n_panel_match / self.n_recovered * 100 if self.n_recovered else 0.0

    @property
    def role_pct(self) -> float:
        return self.n_role_match / self.n_recovered * 100 if self.n_recovered else 0.0

    @property
    def precision_pct(self) -> float:
        return self.n_cli_matched / self.n_cli * 100 if self.n_cli else 0.0

    @property
    def edge_recovery_pct(self) -> float:
        return (self.n_edge_recovered / self.n_ref_edges_on_matched * 100
                if self.n_ref_edges_on_matched else 0.0)


def _score_edges(
    matches: list[dict],
    ref_claims: list[Claim],
    cli_claims: list[Claim],
    ref_dir: Path,
    cli_dir: Path,
) -> tuple[int, int, int]:
    """Count reference edges on matched pairs that are recovered in the CLI tree.

    Returns (n_ref_edges_on_matched, n_recovered, n_cli_extra).
    """
    # Build ref→cli and cli→ref maps over matched pairs.
    ref_to_cli: dict[str, str] = {}
    cli_to_ref: dict[str, str] = {}
    ref_slugs = {c.slug for c in ref_claims}
    cli_slugs = {c.slug for c in cli_claims}

    for m in matches:
        rs = m.get("ref_slug")
        cs = m.get("cli_slug")
        if (m.get("match_quality") in ("exact", "partial")
                and rs in ref_slugs and cs and cs in cli_slugs):
            ref_to_cli[rs] = cs
            cli_to_ref[cs] = rs

    if not ref_to_cli:
        return 0, 0, 0

    ref_edges = load_edges(ref_dir)
    cli_edges = load_edges(cli_dir)

    # Reference edges where both endpoints are in the matched set.
    ref_edge_set: set[tuple[str, str, str]] = set()
    for src, tgt, rel in ref_edges:
        if src in ref_to_cli and tgt in ref_to_cli:
            ref_edge_set.add((src, tgt, rel))

    # Map to CLI slugs for recovery check.
    ref_mapped: set[tuple[str, str, str]] = {
        (ref_to_cli[src], ref_to_cli[tgt], rel)
        for src, tgt, rel in ref_edge_set
    }

    # CLI edges where both endpoints are in matched CLI slugs.
    cli_edge_set: set[tuple[str, str, str]] = set()
    for src, tgt, rel in cli_edges:
        if src in cli_to_ref and tgt in cli_to_ref:
            cli_edge_set.add((src, tgt, rel))

    n_ref_on_matched = len(ref_edge_set)
    n_recovered = len(ref_mapped & cli_edge_set)
    n_extra = len(cli_edge_set - ref_mapped)
    return n_ref_on_matched, n_recovered, n_extra


def _score_role_confusion(
    matches: list[dict],
    ref_claims: list[Claim],
    cli_claims: list[Claim],
) -> dict[str, int]:
    """Build a {(ref_role, cli_role): count} table over matched pairs.

    Serialized as a flat dict with "<ref_role>→<cli_role>" keys so it is
    JSON-serialisable without a custom encoder.
    """
    ref_by_slug = {c.slug: c for c in ref_claims}
    cli_by_slug = {c.slug: c for c in cli_claims}
    confusion: dict[str, int] = defaultdict(int)
    for m in matches:
        rs = m.get("ref_slug")
        cs = m.get("cli_slug")
        if m.get("match_quality") not in ("exact", "partial") or not cs:
            continue
        ref_c = ref_by_slug.get(rs)
        cli_c = cli_by_slug.get(cs)
        if ref_c and cli_c:
            key = f"{ref_c.role or '?'}→{cli_c.role or '?'}"
            confusion[key] += 1
    return dict(confusion)


def score_against_reference(
    ref_dir: Path,
    cli_dir: Path,
    paper_slug: str,
    paper_doi: str,
    review_mode: str,
    cfg: Config,
    *,
    reference: str = "unapproved",
    dump_prompt: Path | None = None,
    matcher_answer: Path | None = None,
) -> PaperScorecard:
    """Score a CLI output directory against a reference paper directory.

    Calls the matcher model unless dump_prompt or matcher_answer is set.
    """
    ref_claims = load_claims(ref_dir, "ref")
    cli_claims = load_claims(cli_dir, "cli")
    if not ref_claims:
        raise ValueError(f"no reference claims found in {ref_dir}")
    if not cli_claims:
        raise ValueError(f"no CLI claims found in {cli_dir}")

    matcher_out = run_matcher(ref_claims, cli_claims, cfg,
                              dump_prompt=dump_prompt, answer=matcher_answer)
    matches = matcher_out.get("matches", [])

    return _build_scorecard(
        paper_slug=paper_slug, paper_doi=paper_doi, review_mode=review_mode,
        reference=reference, cli_dir=str(cli_dir),
        ref_claims=ref_claims, cli_claims=cli_claims, matches=matches,
        ref_dir=ref_dir, cli_dir_path=cli_dir,
    )


def score_from_precomputed_pairs(
    ref_dir: Path,
    cli_dir: Path,
    pairs_path: Path,
    paper_slug: str | None = None,
    paper_doi: str = "",
    review_mode: str = "precomputed",
    reference: str = "unapproved",
) -> PaperScorecard:
    """Score using pre-computed pairs (no model call).

    Accepts both `[{committed, rerun, note}]` and `{matches: [...]}` formats.
    """
    ref_claims = load_claims(ref_dir, "ref")
    cli_claims = load_claims(cli_dir, "cli")
    if not ref_claims:
        raise ValueError(f"no reference claims found in {ref_dir}")
    if not cli_claims:
        raise ValueError(f"no CLI claims found in {cli_dir}")

    raw_pairs = json.loads(pairs_path.read_text(encoding="utf-8"))
    matches = _normalize_pairs(raw_pairs)

    slug = paper_slug or ref_dir.name
    # Augment matches with panel_match and role_match if they are "n/a" (from format B).
    matches = _fill_panel_role(matches, ref_claims, cli_claims)

    return _build_scorecard(
        paper_slug=slug, paper_doi=paper_doi, review_mode=review_mode,
        reference=reference, cli_dir=str(cli_dir),
        ref_claims=ref_claims, cli_claims=cli_claims, matches=matches,
        ref_dir=ref_dir, cli_dir_path=cli_dir,
    )


def _fill_panel_role(
    matches: list[dict],
    ref_claims: list[Claim],
    cli_claims: list[Claim],
) -> list[dict]:
    """Fill panel_match and role_match for pairs that arrived with "n/a".

    Format B pairs don't carry panel/role, so we compute them from the loaded claims.
    """
    ref_by_slug = {c.slug: c for c in ref_claims}
    cli_by_slug = {c.slug: c for c in cli_claims}
    out = []
    for m in matches:
        m = dict(m)
        rs = m.get("ref_slug")
        cs = m.get("cli_slug")
        if m.get("panel_match") == "n/a" and rs and cs:
            ref_c = ref_by_slug.get(rs)
            cli_c = cli_by_slug.get(cs)
            if ref_c and cli_c:
                m["panel_match"] = (
                    (ref_c.panel or "") == (cli_c.panel or "")
                )
                m["role_match"] = ref_c.role == cli_c.role
        out.append(m)
    return out


def _build_scorecard(
    *,
    paper_slug: str,
    paper_doi: str,
    review_mode: str,
    reference: str,
    cli_dir: str,
    ref_claims: list[Claim],
    cli_claims: list[Claim],
    matches: list[dict],
    ref_dir: Path,
    cli_dir_path: Path,
) -> PaperScorecard:
    """Compute all scores from a resolved matches list and return a PaperScorecard."""
    n_recovered = sum(
        1 for m in matches
        if m.get("match_quality") in ("exact", "partial") and m.get("cli_slug")
    )
    n_exact = sum(1 for m in matches if m.get("match_quality") == "exact")
    n_partial = sum(1 for m in matches if m.get("match_quality") == "partial")
    n_panel = sum(1 for m in matches if m.get("panel_match") is True)
    n_role = sum(1 for m in matches if m.get("role_match") is True)

    # Precision: unique CLI claims matched to any ref claim.
    matched_cli_slugs = {
        m["cli_slug"] for m in matches
        if m.get("match_quality") in ("exact", "partial") and m.get("cli_slug")
    }
    n_cli_matched = len(matched_cli_slugs)

    # Parts tally (informational).
    try:
        keys = _edge_keys()
    except Exception:
        keys = set()
    part_key = "part-of" if "part-of" in keys else None

    def _has_part_of(path: Path) -> bool:
        if not part_key:
            return False
        fm = _read_frontmatter(path)
        return bool(fm.get(part_key))

    n_cli_parts = sum(
        1 for p in sorted(cli_dir_path.glob("*.md"))
        if p.name != "index.md" and _has_part_of(p)
    )

    # Edge scoring.
    try:
        n_ref_edges, n_edge_rec, n_extra = _score_edges(
            matches, ref_claims, cli_claims, ref_dir, cli_dir_path)
    except Exception as e:
        logger.warning("edge scoring failed: %s", e)
        n_ref_edges = n_edge_rec = n_extra = 0

    # Role confusion.
    try:
        role_confusion = _score_role_confusion(matches, ref_claims, cli_claims)
    except Exception as e:
        logger.warning("role confusion scoring failed: %s", e)
        role_confusion = {}

    return PaperScorecard(
        paper_slug=paper_slug,
        paper_doi=paper_doi,
        n_ref=len(ref_claims),
        n_cli=len(cli_claims),
        n_recovered=n_recovered,
        n_exact=n_exact,
        n_partial=n_partial,
        n_panel_match=n_panel,
        n_role_match=n_role,
        matches=matches,
        review_mode=review_mode,
        cli_dir=cli_dir,
        n_cli_matched=n_cli_matched,
        n_cli_parts=n_cli_parts,
        n_ref_edges_on_matched=n_ref_edges,
        n_edge_recovered=n_edge_rec,
        n_cli_extra_edges=n_extra,
        role_confusion=role_confusion,
        reference=reference,
    )


# ── End-to-end per-paper evaluation ─────────────────────────────────────


def doi_from_reference_index(ref_paper_dir: Path) -> str:
    """Read the DOI from a reference paper's index.md frontmatter."""
    idx = ref_paper_dir / "index.md"
    if not idx.is_file():
        raise FileNotFoundError(f"reference index not found: {idx}")
    fm = _read_frontmatter(idx)
    doi = fm.get("doi")
    if not doi or not isinstance(doi, str) or not doi.startswith("10."):
        raise ValueError(f"reference index has no valid DOI: {idx} (doi={doi!r})")
    return doi


# Layer names for --dump-prompts / --answers files.
LAYER_ANSWER_NAMES = {
    "results-reader":   "results-reader.json",
    "caption-reader":   "caption-reader.json",
    "structure-reader": "structure-reader.json",
    "reconcile":        "reconcile.json",
    "external-review":  "external-review.json",
    "edge-inference":   "edge-inference.json",
    "matcher":          "matcher.json",
}


def evaluate_paper(
    ref_paper_dir: Path,
    work_dir: Path,
    cfg: Config,
    review_mode: str = "external",
    *,
    dump_prompts_dir: Path | None = None,
    answers_dir: Path | None = None,
    matcher_answer: Path | None = None,
) -> PaperScorecard:
    """Run the full layer chain → score one paper.

    The chain runs through the layer runner functions in layers.py against a
    temporary root (`work_dir`), so the same code path as `pipeline.py run`
    is exercised and the temp root holds a per-run record of what was read.

    If the reference paper has an approved claim-tree version
    (runs/<paper>/approvals.jsonl), that version is used as the reference
    rather than the committed tree, and the scorecard records which.

    Offline workflow
    ────────────────
    dump_prompts_dir — write each model prompt to a file in this directory
        (named by LAYER_ANSWER_NAMES) and return early with a scorecard whose
        error says "prompts dumped".
    answers_dir — read each model answer from the correspondingly named file
        in this directory instead of calling the backend.
    matcher_answer — read the pre-computed matcher alignment from this file
        instead of calling the matcher model.
    """
    from .layers import (
        reader_layer, reader_request,
        reconcile_layer, reconcile_request,
        external_review_layer, external_review_request,
        edge_inference_layer,
        best_draft, read_edges,
    )
    from .write import write_claim_files

    paper_slug = ref_paper_dir.name

    # ── 1. Approved reference ─────────────────────────────────────────────
    ref_dir, reference_status = find_approved_tree(paper_slug, cfg.root, ref_paper_dir)

    # ── 2. DOI ────────────────────────────────────────────────────────────
    try:
        doi = doi_from_reference_index(ref_paper_dir)
    except Exception as e:
        return _err(paper_slug, "?", review_mode, reference_status, f"DOI lookup failed: {e}")

    # ── 3. Temp root setup ────────────────────────────────────────────────
    work_dir.mkdir(parents=True, exist_ok=True)
    tmp_cfg = replace(cfg, root=work_dir, corpus_dir=work_dir / "claims",
                      output_dir=work_dir / "out")

    # Copy prepared.json from the main runs dir if it exists (avoids a network
    # fetch and ensures the same paper text is scored).
    main_prepared = cfg.root / "runs" / paper_slug / "prepared.json"
    tmp_runs = work_dir / "runs" / paper_slug
    tmp_runs.mkdir(parents=True, exist_ok=True)
    tmp_prepared = tmp_runs / "prepared.json"

    if main_prepared.is_file() and not tmp_prepared.is_file():
        shutil.copy2(main_prepared, tmp_prepared)

    if not tmp_prepared.is_file():
        # Fall through to prepare_layer (fetches from eLife CDN).
        try:
            from .layers import prepare_layer
            prepare_layer(paper_slug, tmp_cfg, doi=doi)
        except Exception as e:
            return _err(paper_slug, doi, review_mode, reference_status, f"prepare failed: {e}")

    # ── 4. Readers ────────────────────────────────────────────────────────
    dumping = dump_prompts_dir is not None
    for agent in ("results", "caption", "structure"):
        layer_key = f"{agent}-reader"
        answer_path = (answers_dir / LAYER_ANSWER_NAMES[layer_key]
                       if answers_dir else None)
        dump_path = (dump_prompts_dir / LAYER_ANSWER_NAMES[layer_key]
                     if dumping else None)

        if dump_path is not None:
            try:
                system, user = reader_request(agent, paper_slug, tmp_cfg)
            except Exception as e:
                return _err(paper_slug, doi, review_mode, reference_status,
                            f"{layer_key} prompt build failed: {e}")
            dump_path.parent.mkdir(parents=True, exist_ok=True)
            dump_path.write_text(json.dumps({"system": system, "user": user}, indent=2,
                                            ensure_ascii=False))
            continue

        try:
            reader_layer(agent, paper_slug, tmp_cfg,
                         answer=str(answer_path) if answer_path and answer_path.is_file()
                         else None)
        except Exception as e:
            return _err(paper_slug, doi, review_mode, reference_status,
                        f"{layer_key} failed: {e}")

    # ── 5. Reconcile ──────────────────────────────────────────────────────
    answer_path = (answers_dir / LAYER_ANSWER_NAMES["reconcile"]
                   if answers_dir else None)
    dump_path = (dump_prompts_dir / LAYER_ANSWER_NAMES["reconcile"] if dumping else None)

    if dump_path is not None:
        try:
            system, user = reconcile_request(paper_slug, tmp_cfg)
        except Exception as e:
            return _err(paper_slug, doi, review_mode, reference_status,
                        f"reconcile prompt build failed: {e}")
        dump_path.parent.mkdir(parents=True, exist_ok=True)
        dump_path.write_text(json.dumps({"system": system, "user": user}, indent=2,
                                        ensure_ascii=False))
    else:
        try:
            reconcile_layer(paper_slug, tmp_cfg,
                            answer=str(answer_path) if answer_path and answer_path.is_file()
                            else None)
        except Exception as e:
            return _err(paper_slug, doi, review_mode, reference_status,
                        f"reconcile failed: {e}")

    # ── 6. External review (optional) ─────────────────────────────────────
    if review_mode == "external":
        answer_path = (answers_dir / LAYER_ANSWER_NAMES["external-review"]
                       if answers_dir else None)
        dump_path = (dump_prompts_dir / LAYER_ANSWER_NAMES["external-review"]
                     if dumping else None)

        if dump_path is not None:
            try:
                system, user = external_review_request(paper_slug, tmp_cfg)
            except Exception as e:
                return _err(paper_slug, doi, review_mode, reference_status,
                            f"external-review prompt build failed: {e}")
            dump_path.parent.mkdir(parents=True, exist_ok=True)
            dump_path.write_text(json.dumps({"system": system, "user": user}, indent=2,
                                            ensure_ascii=False))
        else:
            try:
                external_review_layer(paper_slug, tmp_cfg,
                                      answer=str(answer_path)
                                      if answer_path and answer_path.is_file() else None)
            except Exception as e:
                return _err(paper_slug, doi, review_mode, reference_status,
                            f"external-review failed: {e}")

    # ── 7. Edge inference ─────────────────────────────────────────────────
    if not dumping:
        try:
            edge_inference_layer(paper_slug, tmp_cfg)
        except Exception as e:
            logger.warning("edge inference failed (scoring without edges): %s", e)

    # If we were just dumping prompts, write the matcher prompt and return early.
    if dumping:
        try:
            ref_claims = load_claims(ref_dir, "ref")
            # We can't run the chain to get CLI claims yet, so we skip the matcher prompt.
            dump_path = dump_prompts_dir / LAYER_ANSWER_NAMES["matcher"]
            dump_path.write_text(
                json.dumps({"note": "matcher prompt requires chain output; run --answers first"},
                           indent=2))
        except Exception:
            pass
        return _err(paper_slug, doi, review_mode, reference_status,
                    f"prompts dumped to {dump_prompts_dir}")

    # ── 8. Write claim files ──────────────────────────────────────────────
    try:
        draft, _ = best_draft(paper_slug, tmp_cfg)
        edges = read_edges(paper_slug, tmp_cfg)
        cli_paper_dir = tmp_cfg.corpus_dir / paper_slug
        if cli_paper_dir.exists():
            shutil.rmtree(cli_paper_dir)
        write_claim_files(draft, tmp_cfg, edges=edges)
    except Exception as e:
        return _err(paper_slug, doi, review_mode, reference_status, f"write failed: {e}")

    # ── 9. Score ──────────────────────────────────────────────────────────
    try:
        _matcher_answer = matcher_answer
        if answers_dir and not _matcher_answer:
            candidate = answers_dir / LAYER_ANSWER_NAMES["matcher"]
            if candidate.is_file():
                _matcher_answer = candidate

        scorecard = score_against_reference(
            ref_dir=ref_dir,
            cli_dir=cli_paper_dir,
            paper_slug=paper_slug,
            paper_doi=doi,
            review_mode=review_mode,
            cfg=cfg,
            reference=reference_status,
            matcher_answer=_matcher_answer,
        )
    except Exception as e:
        return _err(paper_slug, doi, review_mode, reference_status, f"scoring failed: {e}")

    # Persist per-paper scorecard.
    sc_path = work_dir / "scorecard.json"
    sc_path.write_text(json.dumps(asdict(scorecard), indent=2, default=str))
    return scorecard


def _err(paper_slug: str, doi: str, review_mode: str, reference: str, msg: str) -> PaperScorecard:
    return PaperScorecard(
        paper_slug=paper_slug, paper_doi=doi,
        n_ref=0, n_cli=0, n_recovered=0, n_exact=0, n_partial=0,
        n_panel_match=0, n_role_match=0,
        review_mode=review_mode, reference=reference, error=msg,
    )


# ── score subcommand (no model required) ─────────────────────────────────


def print_score_report(card: PaperScorecard, ref_dir: Path | None = None) -> None:
    """Print a scorecard in the style of pairs.py, with precision and edges."""
    p = card
    print(f"\n  reference   {p.reference}")
    print(f"  committed {p.n_ref}   re-run {p.n_cli}")
    print()
    if p.n_ref:
        print(f"  RECOVERY  {p.n_recovered}/{p.n_ref} = {p.recovery_pct:.0f}%")
        print(f"  PRECISION {p.n_cli_matched}/{p.n_cli} = {p.precision_pct:.0f}%"
              + (f"  ({p.n_cli_parts} part-of)" if p.n_cli_parts else ""))
    if p.n_recovered:
        print(f"  ROLE      {p.n_role_match}/{p.n_recovered} = {p.role_pct:.0f}% of matched pairs")
        print(f"  PANEL     {p.n_panel_match}/{p.n_recovered} = {p.panel_pct:.0f}% of matched pairs")
    if p.n_ref_edges_on_matched > 0 or p.n_cli_extra_edges > 0:
        print(f"  EDGES     {p.n_edge_recovered}/{p.n_ref_edges_on_matched} ref edges recovered"
              f"  ({p.edge_recovery_pct:.0f}%)  |"
              f"  {p.n_cli_extra_edges} extra CLI edge(s)")
    print()

    # Missed reference claims: ref slugs that appear in no matched pair.
    matched_ref = {m.get("ref_slug") for m in p.matches
                   if m.get("match_quality") in ("exact", "partial") and m.get("cli_slug")}
    # Try to get ref claim details (slug + role) for a richer report.
    ref_claims: list[Claim] = []
    if ref_dir and ref_dir.is_dir():
        try:
            ref_claims = load_claims(ref_dir, "ref")
        except Exception:
            pass
    ref_by_slug = {c.slug: c for c in ref_claims}

    # Unmatched entries from the matches list (match_quality "none" or null cli_slug).
    matched_none = [m.get("ref_slug") for m in p.matches
                    if not m.get("cli_slug") or m.get("match_quality") == "none"]
    # Ref slugs that appeared in no match entry at all (format B pairs omit unmatched).
    all_match_ref_slugs = {m.get("ref_slug") for m in p.matches if m.get("ref_slug")}
    missing_from_pairs = [c.slug for c in ref_claims if c.slug not in all_match_ref_slugs]

    all_missed = list(dict.fromkeys(matched_none + missing_from_pairs))
    if all_missed:
        print(f"  committed claims the re-run did not recover ({len(all_missed)}):")
        for slug in all_missed[:20]:
            role = ref_by_slug.get(slug, None)
            role_str = f"{role.role:<18} " if role else ""
            print(f"    {role_str}{slug}")

    extra_cli = p.n_cli - p.n_cli_matched
    print(f"\n  re-run claims with no committed counterpart: {extra_cli}")

    # Role confusion.
    if p.role_confusion:
        disagreements = {k: v for k, v in p.role_confusion.items() if "→" in k
                         and k.split("→")[0] != k.split("→")[1]}
        if disagreements:
            print(f"\n  role disagreements on matched pairs ({sum(disagreements.values())}):")
            for key, count in sorted(disagreements.items(), key=lambda x: -x[1]):
                ref_role, cli_role = key.split("→", 1)
                print(f"    {ref_role:<18} → {cli_role:<18} ({count})")


# ── Scoring against an adjudicated gold (verdict file) ────────────────────
#
# The matcher-based scorecard above measures agreement between two model drafts: how much of
# a reference tree a candidate recovers, how many of its claims land on a reference claim.
# It has no notion of a *wrong* reference claim, because until a person read one no claim was
# wrong. A verdict file is that reading. Scored against it:
#
#   - recovery counts only KEPT claims as the reference; a struck claim is not something a
#     candidate should reproduce, so it leaves the denominator;
#   - a struck claim the candidate DOES reproduce counts against precision, as the false
#     positive it now is;
#   - a merge-into pair is one reference claim, not two;
#   - role accuracy is against the corrected role, panel against the corrected panel;
#   - edge recovery is against the corrected edge set, with `missing` edges included.
#
# Reported beside the matcher numbers, so the two can be read together the first time a tree
# is scored against something a person actually adjudicated.


@dataclass
class GoldScorecard:
    paper_slug: str
    n_ref_all: int          # every claim in the tree the verdicts were made on
    n_kept: int             # kept reference claims (struck removed, merges folded)
    n_struck: int
    n_merges: int
    n_parts: int            # part-of verdicts, informational
    n_recovered: int
    n_cli: int
    n_cli_matched: int      # candidate claims landing on a KEPT reference claim
    n_struck_reproduced: int  # candidate claims that only match struck reference claims
    n_role_match: int
    n_panel_match: int
    n_ref_edges_on_matched: int
    n_edge_recovered: int
    n_missing_edges: int    # edges the reading added that the tree did not carry

    @property
    def recovery_pct(self) -> float:
        return self.n_recovered / self.n_kept * 100 if self.n_kept else 0.0

    @property
    def precision_pct(self) -> float:
        return self.n_cli_matched / self.n_cli * 100 if self.n_cli else 0.0

    @property
    def role_pct(self) -> float:
        return self.n_role_match / self.n_recovered * 100 if self.n_recovered else 0.0

    @property
    def panel_pct(self) -> float:
        return self.n_panel_match / self.n_recovered * 100 if self.n_recovered else 0.0

    @property
    def edge_recovery_pct(self) -> float:
        return (self.n_edge_recovered / self.n_ref_edges_on_matched * 100
                if self.n_ref_edges_on_matched else 0.0)


def _canonicalize(slug: str, merged: dict[str, str]) -> str:
    """Follow merge-into to the claim that stands, guarding a mistaken cycle."""
    seen = {slug}
    while slug in merged:
        slug = merged[slug]
        if slug in seen:
            break
        seen.add(slug)
    return slug


def _corrected_edges(
    ref_edges: list[tuple[str, str, str]],
    edge_verdicts: dict[tuple[str, str, str], dict],
) -> tuple[set[tuple[str, str, str]], int]:
    """The reference edge set after the reading, and how many edges it added.

    An edge with no verdict is kept (the skeleton marks every edge `ok`, so an unmarked one is
    a reader who never disagreed). `strike` drops it, `wrong-relation` and `wrong-direction`
    rewrite it, `missing` adds an edge the tree did not carry.
    """
    # part-of is a claim verdict, not a relation edge; keep it out of the edge tally.
    corrected: set[tuple[str, str, str]] = set()
    added = 0
    ref_set = {(s, t, r) for s, t, r in ref_edges if r != "part-of"}
    for s, t, r in ref_set:
        v = edge_verdicts.get((s, t, r))
        verdict = v.get("verdict") if v else "ok"
        if verdict == "strike":
            continue
        if verdict == "wrong-relation":
            corrected.add((s, t, (v.get("corrected") or r)))
        elif verdict == "wrong-direction":
            corrected.add((t, s, (v.get("corrected") or r)))
        else:  # ok, missing-on-existing, or anything unrecognised: keep the edge
            corrected.add((s, t, r))
    for (s, t, r), v in edge_verdicts.items():
        if v.get("verdict") == "missing" and (s, t, r) not in ref_set:
            corrected.add((s, t, (v.get("corrected") or r)))
            added += 1
    return corrected, added


def score_against_gold(
    ref_dir: Path,
    cli_dir: Path,
    pairs_path: Path,
    verdicts_path: Path,
    paper_slug: str | None = None,
) -> GoldScorecard:
    """Score a candidate tree against an adjudicated reference (a verdict file)."""
    ref_claims = load_claims(ref_dir, "ref")
    cli_claims = load_claims(cli_dir, "cli")
    if not ref_claims:
        raise ValueError(f"no reference claims found in {ref_dir}")
    if not cli_claims:
        raise ValueError(f"no CLI claims found in {cli_dir}")

    res = vd.resolve(vd.load(verdicts_path))
    ref_by_slug = {c.slug: c for c in ref_claims}
    cli_by_slug = {c.slug: c for c in cli_claims}
    ref_slugs = set(ref_by_slug)

    struck = res.struck & ref_slugs
    merged = {s: t for s, t in res.merged.items() if s in ref_slugs and t in ref_slugs}
    parts = {s for s in res.part_of if s in ref_slugs}

    def corrected_role(slug: str) -> str:
        r = res.claims.get(slug, {})
        return (r.get("role") or (ref_by_slug[slug].role if slug in ref_by_slug else "")) or ""

    def corrected_panel(slug: str) -> str:
        r = res.claims.get(slug, {})
        return (r.get("panel") or (ref_by_slug[slug].panel if slug in ref_by_slug else "")) or ""

    # The kept reference claims: struck removed, merged folded into their target.
    canon = {s: _canonicalize(s, merged) for s in ref_slugs}
    kept = {canon[s] for s in ref_slugs if s not in struck and canon[s] not in struck}

    # Matches, ref slug → cli slug over the pairs the matcher (or a pairs file) produced.
    matches = _normalize_pairs(json.loads(pairs_path.read_text(encoding="utf-8")))
    ref_to_cli: dict[str, str] = {}
    for m in matches:
        rs, cs = m.get("ref_slug"), m.get("cli_slug")
        if m.get("match_quality") in ("exact", "partial") and rs in ref_slugs and cs in cli_by_slug:
            ref_to_cli[rs] = cs

    # Recovery: a kept (canonical) claim is recovered when itself or a slug merged into it has a
    # matched candidate.
    recovered_cli: dict[str, str] = {}   # canonical kept slug → the cli claim that recovered it
    for rs, cs in ref_to_cli.items():
        c = canon[rs]
        if c in kept and c not in recovered_cli:
            recovered_cli[c] = cs
    n_recovered = len(recovered_cli)

    # Precision: candidate claims landing on a kept reference claim count; those landing only on
    # struck claims are the false positives the reading exposes.
    cli_matched_kept: set[str] = set()
    cli_matched_struck: set[str] = set()
    for rs, cs in ref_to_cli.items():
        (cli_matched_kept if canon[rs] in kept else cli_matched_struck).add(cs)
    n_struck_reproduced = len(cli_matched_struck - cli_matched_kept)

    # Role and panel accuracy, over recovered pairs, against the corrected values.
    n_role = n_panel = 0
    for c, cs in recovered_cli.items():
        cli_c = cli_by_slug.get(cs)
        if not cli_c:
            continue
        if (cli_c.role or "") == corrected_role(c):
            n_role += 1
        if (cli_c.panel or "") == corrected_panel(c):
            n_panel += 1

    # Edges: the corrected reference edge set, restricted to matched pairs, remapped to cli.
    corrected, n_missing = _corrected_edges(load_edges(ref_dir), res.edges)
    # A ref endpoint reaches a cli slug through its canonical claim's recovering match.
    ref_endpoint_to_cli = {c: cs for c, cs in recovered_cli.items()}
    ref_edges_on_matched = {
        (s, t, r) for s, t, r in corrected
        if canon.get(s, s) in ref_endpoint_to_cli and canon.get(t, t) in ref_endpoint_to_cli
    }
    ref_mapped = {
        (ref_endpoint_to_cli[canon.get(s, s)], ref_endpoint_to_cli[canon.get(t, t)], r)
        for s, t, r in ref_edges_on_matched
    }
    cli_edges = {(s, t, r) for s, t, r in load_edges(cli_dir) if r != "part-of"}
    n_edge_rec = len(ref_mapped & cli_edges)

    return GoldScorecard(
        paper_slug=paper_slug or ref_dir.name,
        n_ref_all=len(ref_claims),
        n_kept=len(kept),
        n_struck=len(struck),
        n_merges=len(merged),
        n_parts=len(parts),
        n_recovered=n_recovered,
        n_cli=len(cli_claims),
        n_cli_matched=len(cli_matched_kept),
        n_struck_reproduced=n_struck_reproduced,
        n_role_match=n_role,
        n_panel_match=n_panel,
        n_ref_edges_on_matched=len(ref_edges_on_matched),
        n_edge_recovered=n_edge_rec,
        n_missing_edges=n_missing,
    )


def print_gold_report(card: GoldScorecard) -> None:
    """Print the gold scorecard, in the same shape as the matcher report beside it."""
    p = card
    print("\n  ── against the adjudicated gold ─────────────────────────────")
    print(f"  reference   verdicts: {p.n_kept} kept  ({p.n_struck} struck, "
          f"{p.n_merges} merged, {p.n_parts} parts) of {p.n_ref_all}")
    print(f"  candidate   {p.n_cli} claims")
    print()
    if p.n_kept:
        print(f"  RECOVERY  {p.n_recovered}/{p.n_kept} = {p.recovery_pct:.0f}%  (kept claims only)")
    if p.n_cli:
        print(f"  PRECISION {p.n_cli_matched}/{p.n_cli} = {p.precision_pct:.0f}%"
              + (f"  ({p.n_struck_reproduced} reproduced a struck claim)"
                 if p.n_struck_reproduced else ""))
    if p.n_recovered:
        print(f"  ROLE      {p.n_role_match}/{p.n_recovered} = {p.role_pct:.0f}%  (vs corrected role)")
        print(f"  PANEL     {p.n_panel_match}/{p.n_recovered} = {p.panel_pct:.0f}%  (vs corrected panel)")
    if p.n_ref_edges_on_matched:
        print(f"  EDGES     {p.n_edge_recovered}/{p.n_ref_edges_on_matched} corrected edges recovered"
              f"  ({p.edge_recovery_pct:.0f}%)"
              + (f"  |  {p.n_missing_edges} edge(s) the reading added" if p.n_missing_edges else ""))
    print()


# ── Aggregate report ────────────────────────────────────────────────────


def aggregate_report(
    cards: list[PaperScorecard],
    out_path: Path,
    reference_dir: Path,
    work_root: Path,
    review_mode: str,
) -> None:
    """Render a multi-paper aggregate scorecard."""
    successes = [c for c in cards if c.error is None and c.n_ref > 0]
    failures = [c for c in cards if c.error is not None]

    def _stats(values: list[float]) -> tuple[float, float]:
        if not values:
            return 0.0, 0.0
        return statistics.mean(values), statistics.median(values)

    rec_pct = [c.recovery_pct for c in successes]
    prec_pct = [c.precision_pct for c in successes]
    panel_pct = [c.panel_pct for c in successes]
    role_pct = [c.role_pct for c in successes]
    edge_pct = [c.edge_recovery_pct for c in successes if c.n_ref_edges_on_matched > 0]
    rec_mean, rec_med = _stats(rec_pct)
    prec_mean, prec_med = _stats(prec_pct)
    panel_mean, panel_med = _stats(panel_pct)
    role_mean, role_med = _stats(role_pct)
    edge_mean, edge_med = _stats(edge_pct)

    n_papers = len(cards)
    n_success = len(successes)

    lines = [
        "# Aggregate round-trip scorecard",
        "",
        f"**Generated:** {date.today().isoformat()}",
        f"**Reference corpus:** `{reference_dir}`",
        f"**Work directory:** `{work_root}`",
        f"**Review mode:** `{review_mode}`",
        f"**Papers attempted:** {n_papers} ({n_success} succeeded, {len(failures)} failed)",
        "",
        "## Aggregate metrics (across successful papers)",
        "",
        "| Metric | Mean | Median | n |",
        "|:-------|-----:|-------:|--:|",
        f"| Claim recovery (% of reference recovered) | {rec_mean:.1f}% | {rec_med:.1f}% | {n_success} |",
        f"| Precision (% of CLI claims matched) | {prec_mean:.1f}% | {prec_med:.1f}% | {n_success} |",
        f"| Panel agreement (% of recovered) | {panel_mean:.1f}% | {panel_med:.1f}% | {n_success} |",
        f"| Role agreement (% of recovered) | {role_mean:.1f}% | {role_med:.1f}% | {n_success} |",
        f"| Edge recovery (% of ref edges on matched pairs) | {edge_mean:.1f}% | {edge_med:.1f}% | {len(edge_pct)} |",
        "",
        "## Per-paper detail",
        "",
        "| Paper | ref | cli | rec | prec | panel | role | ref-edges | edge-rec | extra-edges | reference |",
        "|:------|----:|----:|----:|-----:|------:|-----:|----------:|---------:|------------:|:----------|",
    ]
    for c in cards:
        if c.error:
            lines.append(
                f"| `{c.paper_slug}` | — | — | — | — | — | — | — | — | — | (error: {c.error[:60]}) |"
            )
            continue
        lines.append(
            f"| `{c.paper_slug}` | {c.n_ref} | {c.n_cli} | {c.recovery_pct:.0f}% | "
            f"{c.precision_pct:.0f}% | {c.panel_pct:.0f}% | {c.role_pct:.0f}% | "
            f"{c.n_ref_edges_on_matched} | {c.edge_recovery_pct:.0f}% | "
            f"{c.n_cli_extra_edges} | {c.reference} |"
        )

    if failures:
        lines.append("")
        lines.append("## Failures")
        lines.append("")
        for c in failures:
            lines.append(f"- `{c.paper_slug}`: {c.error}")

    out_path.write_text("\n".join(lines) + "\n")
