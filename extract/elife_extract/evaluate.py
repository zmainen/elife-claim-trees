"""Round-trip evaluation — score CLI output against a curated reference corpus.

Wraps the per-paper round-trip workflow into a reusable module that the
CLI's `evaluate` subcommand exposes. For each paper:
  1. Read the reference paper's index.md to get the DOI.
  2. Run extract -> reconcile -> (optional external_review) -> write
     into a temp corpus directory.
  3. Run the CrossRef-style matcher (Opus) to align CLI claims with
     reference claims.
  4. Score: claim recovery, panel agreement, role agreement, match quality.
  5. Save per-paper scorecard.

After all papers complete, render an aggregate scorecard with mean / median
per-paper scores plus a comparison table.

The matcher logic mirrors tests/headley_roundtrip.py (which now imports
from this module). Promoted to a first-class CLI capability so future
prompt iterations can be validated the same way without bespoke scripts.
"""

from __future__ import annotations

import json
import logging
import re
import statistics
from dataclasses import dataclass, field, asdict
from datetime import date
from pathlib import Path
from typing import Iterable

import yaml

from .agents import get_client
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


def run_matcher(
    ref_claims: list[Claim],
    cli_claims: list[Claim],
    cfg: Config,
) -> dict:
    """Call Opus to align reference and CLI claims; return parsed mapping."""
    user = (
        _format_claim_list(ref_claims, "REFERENCE")
        + "\n\n"
        + _format_claim_list(cli_claims, "CLI")
        + "\n\nReturn the JSON object as instructed."
    )
    client = get_client(cfg)
    text_chunks: list[str] = []
    with client.messages.stream(
        model=cfg.model_reconcile,  # Opus matcher (same model class)
        max_tokens=32768,
        system=MATCHER_PROMPT,
        messages=[{"role": "user", "content": user}],
    ) as stream:
        for chunk in stream.text_stream:
            text_chunks.append(chunk)
    raw = "".join(text_chunks).strip()
    raw = re.sub(r"^```(?:json)?\s*\n?", "", raw, count=1, flags=re.IGNORECASE)
    raw = re.sub(r"\n?```\s*$", "", raw, count=1)
    return json.loads(raw)


# ── Per-paper scorecard ─────────────────────────────────────────────────


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

    @property
    def recovery_pct(self) -> float:
        return self.n_recovered / self.n_ref * 100 if self.n_ref else 0.0

    @property
    def panel_pct(self) -> float:
        return self.n_panel_match / self.n_recovered * 100 if self.n_recovered else 0.0

    @property
    def role_pct(self) -> float:
        return self.n_role_match / self.n_recovered * 100 if self.n_recovered else 0.0


def score_against_reference(
    ref_dir: Path,
    cli_dir: Path,
    paper_slug: str,
    paper_doi: str,
    review_mode: str,
    cfg: Config,
) -> PaperScorecard:
    """Score a CLI output directory against a reference paper directory."""
    ref_claims = load_claims(ref_dir, "ref")
    cli_claims = load_claims(cli_dir, "cli")
    if not ref_claims:
        raise ValueError(f"no reference claims found in {ref_dir}")
    if not cli_claims:
        raise ValueError(f"no CLI claims found in {cli_dir}")

    matcher_out = run_matcher(ref_claims, cli_claims, cfg)
    matches = matcher_out.get("matches", [])

    n_recovered = sum(
        1 for m in matches
        if m.get("match_quality") in ("exact", "partial") and m.get("cli_slug")
    )
    n_exact = sum(1 for m in matches if m.get("match_quality") == "exact")
    n_partial = sum(1 for m in matches if m.get("match_quality") == "partial")
    n_panel = sum(1 for m in matches if m.get("panel_match") is True)
    n_role = sum(1 for m in matches if m.get("role_match") is True)

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
        cli_dir=str(cli_dir),
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


def evaluate_paper(
    ref_paper_dir: Path,
    work_dir: Path,
    cfg: Config,
    review_mode: str = "external",
) -> PaperScorecard:
    """Run the full extract -> review -> write -> score pipeline on one paper.

    work_dir holds the per-paper extraction artifacts:
      <work_dir>/out/draft-<slug>.json
      <work_dir>/<slug>/<claim>.md  (the CLI's output corpus)
      <work_dir>/scorecard.json     (the per-paper PaperScorecard)

    Returns the PaperScorecard. On failure, returns a scorecard with
    error set; the caller can decide whether to abort or continue.
    """
    from .prepare import prepare
    from .agents import run_all_agents
    from .reconcile import reconcile as reconcile_step
    from .external_review import external_review
    from .write import write_claim_files

    paper_slug_ref = ref_paper_dir.name
    try:
        doi = doi_from_reference_index(ref_paper_dir)
    except Exception as e:
        return PaperScorecard(
            paper_slug=paper_slug_ref, paper_doi="?",
            n_ref=0, n_cli=0, n_recovered=0, n_exact=0, n_partial=0,
            n_panel_match=0, n_role_match=0,
            review_mode=review_mode, error=f"DOI lookup failed: {e}",
        )

    work_dir.mkdir(parents=True, exist_ok=True)
    (work_dir / "out").mkdir(parents=True, exist_ok=True)

    logger.info("evaluate paper=%s doi=%s mode=%s", paper_slug_ref, doi, review_mode)

    # 1. prepare
    try:
        paper = prepare(doi)
    except Exception as e:
        return PaperScorecard(
            paper_slug=paper_slug_ref, paper_doi=doi,
            n_ref=0, n_cli=0, n_recovered=0, n_exact=0, n_partial=0,
            n_panel_match=0, n_role_match=0,
            review_mode=review_mode, error=f"prepare failed: {e}",
        )

    cli_paper_slug = paper.paper_slug

    # 2-3. extract
    try:
        results, caption, structure = run_all_agents(paper, cfg)
    except Exception as e:
        return PaperScorecard(
            paper_slug=paper_slug_ref, paper_doi=doi,
            n_ref=0, n_cli=0, n_recovered=0, n_exact=0, n_partial=0,
            n_panel_match=0, n_role_match=0,
            review_mode=review_mode, error=f"extract failed: {e}",
        )

    # 4. reconcile
    try:
        draft = reconcile_step(
            results, caption, structure, cfg,
            paper_doi=doi, paper_title=paper.title,
        )
    except Exception as e:
        return PaperScorecard(
            paper_slug=paper_slug_ref, paper_doi=doi,
            n_ref=0, n_cli=0, n_recovered=0, n_exact=0, n_partial=0,
            n_panel_match=0, n_role_match=0,
            review_mode=review_mode, error=f"reconcile failed: {e}",
        )

    draft_path = work_dir / "out" / f"draft-{cli_paper_slug}.json"
    draft_path.write_text(draft.model_dump_json(indent=2))

    # 4.5 (optional). external review
    if review_mode == "external":
        try:
            draft = external_review(paper, draft, cfg)
            (work_dir / "out" / f"draft-{cli_paper_slug}.reviewed.json").write_text(
                draft.model_dump_json(indent=2)
            )
        except Exception as e:
            return PaperScorecard(
                paper_slug=paper_slug_ref, paper_doi=doi,
                n_ref=0, n_cli=0, n_recovered=0, n_exact=0, n_partial=0,
                n_panel_match=0, n_role_match=0,
                review_mode=review_mode,
                error=f"external review failed: {e}",
            )

    # 5-7. write (use a per-paper sub-directory under work_dir)
    write_cfg = Config.from_args(_NSpace(corpus_dir=work_dir, output_dir=work_dir / "out"))
    write_cfg.model_reconcile = cfg.model_reconcile
    write_cfg.model_results = cfg.model_results
    write_cfg.model_caption = cfg.model_caption
    write_cfg.model_structure = cfg.model_structure
    write_cfg.prompt_variant = cfg.prompt_variant
    try:
        # Wipe any prior CLI output for this paper to allow re-runs
        cli_paper_dir = work_dir / cli_paper_slug
        if cli_paper_dir.exists():
            import shutil
            shutil.rmtree(cli_paper_dir)
        write_claim_files(draft, write_cfg)
    except Exception as e:
        return PaperScorecard(
            paper_slug=paper_slug_ref, paper_doi=doi,
            n_ref=0, n_cli=0, n_recovered=0, n_exact=0, n_partial=0,
            n_panel_match=0, n_role_match=0,
            review_mode=review_mode, error=f"write failed: {e}",
        )

    # 8. score
    try:
        scorecard = score_against_reference(
            ref_dir=ref_paper_dir,
            cli_dir=work_dir / cli_paper_slug,
            paper_slug=paper_slug_ref,
            paper_doi=doi,
            review_mode=review_mode,
            cfg=cfg,
        )
    except Exception as e:
        return PaperScorecard(
            paper_slug=paper_slug_ref, paper_doi=doi,
            n_ref=0, n_cli=0, n_recovered=0, n_exact=0, n_partial=0,
            n_panel_match=0, n_role_match=0,
            review_mode=review_mode, error=f"scoring failed: {e}",
        )

    # Persist per-paper scorecard
    sc_path = work_dir / "scorecard.json"
    sc_path.write_text(json.dumps(asdict(scorecard), indent=2, default=str))
    return scorecard


class _NSpace:
    """Minimal argparse.Namespace stand-in for Config.from_args."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


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
    panel_pct = [c.panel_pct for c in successes]
    role_pct = [c.role_pct for c in successes]
    rec_mean, rec_med = _stats(rec_pct)
    panel_mean, panel_med = _stats(panel_pct)
    role_mean, role_med = _stats(role_pct)

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
        f"| Panel agreement (% of recovered) | {panel_mean:.1f}% | {panel_med:.1f}% | {n_success} |",
        f"| Role agreement (% of recovered) | {role_mean:.1f}% | {role_med:.1f}% | {n_success} |",
        "",
        "## Per-paper detail",
        "",
        "| Paper | n_ref | n_cli | recovered | exact | partial | recovery | panel | role |",
        "|:------|------:|------:|----------:|------:|--------:|---------:|------:|-----:|",
    ]
    for c in cards:
        if c.error:
            lines.append(
                f"| `{c.paper_slug}` | — | — | — | — | — | — | — | — | (error: {c.error[:60]}) |"
            )
            continue
        lines.append(
            f"| `{c.paper_slug}` | {c.n_ref} | {c.n_cli} | {c.n_recovered} | "
            f"{c.n_exact} | {c.n_partial} | {c.recovery_pct:.0f}% | "
            f"{c.panel_pct:.0f}% | {c.role_pct:.0f}% |"
        )

    if failures:
        lines.append("")
        lines.append("## Failures")
        lines.append("")
        for c in failures:
            lines.append(f"- `{c.paper_slug}`: {c.error}")

    out_path.write_text("\n".join(lines) + "\n")
