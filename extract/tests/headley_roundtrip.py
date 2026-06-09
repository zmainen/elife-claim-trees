"""Round-trip test on Headley 2026 — Phase F's load-bearing acceptance.

Compares the CLI's extracted claims against the 26 human-curated reference
claims at ~/Projects/mainenlab/elife-claim-trees/claims/headley-2026-inhibitory-rhythms/.
Scores claim recovery, panel assignment, and role classification.

Usage:
    python tests/headley_roundtrip.py [--cli-dir <path>] [--ref-dir <path>] \
        [--scorecard <path>]

Defaults:
    --cli-dir   /tmp/elife-test/headley-2024-spatially-targeted-inhibitory/
                (the output of `elife-extract write` from the Phase D/E run)
    --ref-dir   ~/Projects/mainenlab/elife-claim-trees/claims/headley-2026-inhibitory-rhythms/
    --scorecard tests/headley-roundtrip.md

The matching uses Opus to do semantic alignment — comparing 26 × 76 claim
pairs by string similarity misses too many real matches. The model is
asked to produce a JSON mapping {ref_slug: cli_slug_or_null} where
cli_slug_or_null is the best CLI match for the reference claim, or null
if none matches.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml
from anthropic import AnthropicVertex


# ── Paths ────────────────────────────────────────────────────────────────


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLI_DIR = Path("/tmp/elife-test/headley-2024-spatially-targeted-inhibitory")
DEFAULT_REF_DIR = Path.home() / "Projects/mainenlab/elife-claim-trees/claims/headley-2026-inhibitory-rhythms"
DEFAULT_SCORECARD = REPO_ROOT / "tests/headley-roundtrip.md"

VERTEX_PROJECT = os.environ.get("VERTEX_PROJECT_ID", "cr-mainen")
VERTEX_REGION = os.environ.get("VERTEX_REGION", "europe-west1")
MATCHER_MODEL = "claude-opus-4-6"


# ── Claim loading ────────────────────────────────────────────────────────


@dataclass
class Claim:
    slug: str
    claim: str
    panel: str | None
    role: str
    claim_type: str | None = None
    source: str = ""  # "ref" or "cli"


def _read_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    text = path.read_text()
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def _load_claims(claim_dir: Path, source: str) -> list[Claim]:
    """Load all claim files from a paper directory."""
    claims = []
    for path in sorted(claim_dir.glob("*.md")):
        if path.name == "index.md":
            continue
        fm = _read_frontmatter(path)
        if not fm:
            continue
        slug = fm.get("slug") or path.stem
        # Reference uses 'panel' inside assertions[0]; CLI uses panel inside assertions[0] too.
        panel = None
        assertions = fm.get("assertions") or []
        if assertions and isinstance(assertions, list) and isinstance(assertions[0], dict):
            panel = assertions[0].get("panel")
        # CLI also exposes panel at frontmatter top-level via reconciled.panel; reference
        # keeps it inside assertions only. Normalize.
        claims.append(Claim(
            slug=slug,
            claim=fm.get("claim", "").strip().replace("\n", " "),
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


# ── Format inputs for the matcher ────────────────────────────────────────


def _format_claim_list(claims: list[Claim], label: str) -> str:
    lines = [f"## {label} ({len(claims)} claims)\n"]
    for c in claims:
        lines.append(f"- **{c.slug}** [panel={c.panel}, role={c.role}]: {c.claim}")
    return "\n".join(lines)


# ── Run the matcher ──────────────────────────────────────────────────────


def run_matcher(ref_claims: list[Claim], cli_claims: list[Claim]) -> dict:
    """Call Opus to align reference and CLI claims; return the parsed mapping."""
    user = (
        _format_claim_list(ref_claims, "REFERENCE")
        + "\n\n"
        + _format_claim_list(cli_claims, "CLI")
        + "\n\nReturn the JSON object as instructed."
    )
    client = AnthropicVertex(project_id=VERTEX_PROJECT, region=VERTEX_REGION)
    text_chunks: list[str] = []
    with client.messages.stream(
        model=MATCHER_MODEL,
        max_tokens=32768,
        system=MATCHER_PROMPT,
        messages=[{"role": "user", "content": user}],
    ) as stream:
        for chunk in stream.text_stream:
            text_chunks.append(chunk)
    raw = "".join(text_chunks).strip()
    # Strip ```json ... ``` fences if present (open/close independently)
    raw = re.sub(r"^```(?:json)?\s*\n?", "", raw, count=1, flags=re.IGNORECASE)
    raw = re.sub(r"\n?```\s*$", "", raw, count=1)
    return json.loads(raw)


# ── Scorecard ────────────────────────────────────────────────────────────


def build_scorecard(
    ref_claims: list[Claim],
    cli_claims: list[Claim],
    matches: list[dict],
) -> str:
    """Render the scorecard markdown, including per-claim table and summary."""
    by_ref = {m["ref_slug"]: m for m in matches}
    cli_by_slug = {c.slug: c for c in cli_claims}
    ref_by_slug = {c.slug: c for c in ref_claims}

    n_ref = len(ref_claims)
    n_cli = len(cli_claims)
    n_recovered = sum(
        1 for m in matches
        if m["match_quality"] in ("exact", "partial") and m.get("cli_slug")
    )
    n_exact = sum(1 for m in matches if m["match_quality"] == "exact")
    n_partial = sum(1 for m in matches if m["match_quality"] == "partial")
    n_none = sum(1 for m in matches if m["match_quality"] == "none")

    panel_match_count = sum(1 for m in matches if m.get("panel_match") is True)
    role_match_count = sum(1 for m in matches if m.get("role_match") is True)

    matched_count = n_recovered  # base for panel/role percentage
    panel_pct = (panel_match_count / matched_count * 100) if matched_count else 0
    role_pct = (role_match_count / matched_count * 100) if matched_count else 0
    recovery_pct = n_recovered / n_ref * 100 if n_ref else 0

    pass_recovery = recovery_pct >= 80
    pass_panel = panel_pct >= 90
    pass_role = role_pct >= 75

    lines = [
        "# Headley 2026 — Round-trip test scorecard",
        "",
        f"**Generated:** {__import__('datetime').date.today().isoformat()}",
        "",
        f"**Reference:** `{DEFAULT_REF_DIR}` ({n_ref} curated claims)",
        f"**CLI output:** `{DEFAULT_CLI_DIR}` ({n_cli} extracted claims)",
        f"**Matcher model:** {MATCHER_MODEL}",
        "",
        "## Acceptance criteria",
        "",
        f"| Metric | Threshold | Achieved | Status |",
        f"|:-------|:----------|:---------|:-------|",
        f"| Claim recovery | ≥ 80% | {recovery_pct:.1f}% ({n_recovered}/{n_ref}) | {'✅ PASS' if pass_recovery else '❌ FAIL'} |",
        f"| Panel assignment | ≥ 90% (of matched) | {panel_pct:.1f}% ({panel_match_count}/{matched_count}) | {'✅ PASS' if pass_panel else '❌ FAIL'} |",
        f"| Role classification | ≥ 75% (of matched) | {role_pct:.1f}% ({role_match_count}/{matched_count}) | {'✅ PASS' if pass_role else '❌ FAIL'} |",
        "",
        "## Match-quality breakdown",
        "",
        f"- Exact matches: {n_exact}",
        f"- Partial matches: {n_partial}",
        f"- No match: {n_none}",
        f"- Total recovered (exact + partial): {n_recovered} of {n_ref}",
        "",
        "## Per-reference detail",
        "",
        "| Reference slug | Match quality | CLI slug | Panel match | Role match | Notes |",
        "|:---------------|:--------------|:---------|:-----------:|:----------:|:------|",
    ]

    for ref in ref_claims:
        m = by_ref.get(ref.slug, {})
        cli_slug = m.get("cli_slug") or "—"
        quality = m.get("match_quality", "?")
        panel_m = m.get("panel_match", "?")
        role_m = m.get("role_match", "?")
        note = m.get("notes", "") or ""
        if note and len(note) > 80:
            note = note[:77] + "..."
        # Format booleans/n/a compactly
        def fmt(v):
            if v is True: return "✓"
            if v is False: return "✗"
            return "n/a"
        lines.append(
            f"| `{ref.slug}` | {quality} | "
            f"{cli_slug if cli_slug == '—' else f'`{cli_slug}`'} | "
            f"{fmt(panel_m)} | {fmt(role_m)} | {note} |"
        )

    lines.extend([
        "",
        "## Unmatched CLI claims",
        "",
        f"The CLI produced {n_cli} claims; {matched_count} of them aligned to a reference.",
        f"The remaining {n_cli - matched_count} did not. (The reference is curated tighter than the",
        "CLI's extraction; over-extraction is the CLI's expected failure mode at this stage.)",
        "",
        "Selected unmatched CLI claims (first 10) for prompt iteration:",
        "",
    ])
    matched_cli_slugs = {m.get("cli_slug") for m in matches if m.get("cli_slug")}
    unmatched = [c for c in cli_claims if c.slug not in matched_cli_slugs]
    for c in unmatched[:10]:
        lines.append(f"- `{c.slug}` [panel={c.panel}, role={c.role}]: {c.claim[:120]}")

    return "\n".join(lines) + "\n"


# ── Main ────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="Headley round-trip scoring (Phase F)")
    parser.add_argument("--ref-dir", type=Path, default=DEFAULT_REF_DIR)
    parser.add_argument("--cli-dir", type=Path, default=DEFAULT_CLI_DIR)
    parser.add_argument("--scorecard", type=Path, default=DEFAULT_SCORECARD)
    parser.add_argument(
        "--matches-json",
        type=Path,
        default=None,
        help="Save raw matcher JSON to this path (default: alongside scorecard).",
    )
    parser.add_argument(
        "--load-matches",
        type=Path,
        default=None,
        help="Load matcher JSON instead of calling Opus (for re-rendering scorecards).",
    )
    args = parser.parse_args()

    ref_claims = _load_claims(args.ref_dir, "ref")
    cli_claims = _load_claims(args.cli_dir, "cli")
    print(f"loaded {len(ref_claims)} reference + {len(cli_claims)} CLI claims")

    if args.load_matches:
        result = json.loads(args.load_matches.read_text())
    else:
        print(f"calling matcher ({MATCHER_MODEL})…", file=sys.stderr)
        result = run_matcher(ref_claims, cli_claims)
        out = args.matches_json or args.scorecard.with_suffix(".matches.json")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2))
        print(f"saved matcher output: {out}", file=sys.stderr)

    matches = result.get("matches", [])
    if len(matches) != len(ref_claims):
        print(
            f"warning: matcher returned {len(matches)} matches for {len(ref_claims)} ref claims",
            file=sys.stderr,
        )

    scorecard = build_scorecard(ref_claims, cli_claims, matches)
    args.scorecard.parent.mkdir(parents=True, exist_ok=True)
    args.scorecard.write_text(scorecard)
    print(f"scorecard: {args.scorecard}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
