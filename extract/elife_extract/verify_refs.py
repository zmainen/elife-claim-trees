"""CrossRef DOI resolution for literature-context claims.

Per `panel-claim-unification.md` Phase 5: every literature-context claim
that cites prior work must have its citation resolved via CrossRef. This
is the primary defense against LLM hallucination of references and the
linking infrastructure for cross-paper claim graphs.

Pipeline:
  1. Scan <corpus_dir>/<paper_slug>/*.md for `role: literature-context` claims.
  2. For each claim:
     a. If the claim's assertions[0].doi is already a real DOI, just confirm it
        resolves via CrossRef (anti-hallucination check). No write-back needed.
     b. Else, extract reference hints from the slug + claim + body and query
        CrossRef. Use the highest-scoring match (above a confidence threshold)
        as the resolution.
     c. Write the verified DOI back to the claim's frontmatter (unless --dry-run).
  3. Return a results list summarizing per-claim status: confirmed / found /
     not-found / no-hint / unresolvable.

Resolution rate measured at panel-claim-unification.md Phase 5: ~97% on
bibliographies extracted from PDFs; ~25% with slug-derived hints alone.
The bibliography extraction step is the prerequisite for reliable
verification at scale; for now we use the slug+claim+body hints, which
are good enough for an analyst-reviewed first pass.

Mirrors the canonical script at
~/Projects/mainenlab/elife-claim-trees/scripts/verify-references.py.
Adapted to use httpx (vs urllib), corpus-dir + paper-slug conventions
(vs hardcoded paths), and the elife_extract config plumbing.
"""

from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import httpx
import yaml

from .config import Config

logger = logging.getLogger(__name__)


# ── CrossRef API ─────────────────────────────────────────────────────────


CROSSREF_BASE = "https://api.crossref.org"
CROSSREF_MAILTO = "zmainen@neuro.fchampalimaud.org"
CROSSREF_USER_AGENT = (
    f"elife-extract/0.1.0 (mailto:{CROSSREF_MAILTO})"
)

# Polite delay between queries — CrossRef's request that anonymous callers
# rate-limit themselves to ~50 rps. We're 1-2 rps.
QUERY_DELAY_S = 0.5

# Score threshold above which a CrossRef match is high-confidence enough to
# write back without manual review. Per the canonical script, score > 15
# indicates a precise hit; below that the queries are too noisy to commit.
CONFIDENCE_THRESHOLD = 15.0


@dataclass
class CrossrefMatch:
    """One result from CrossRef lookup."""
    doi: str
    title: str
    authors: str
    score: float
    raw: dict = field(default_factory=dict, repr=False)


def _client() -> httpx.Client:
    return httpx.Client(
        timeout=15.0,
        headers={"User-Agent": CROSSREF_USER_AGENT},
        follow_redirects=True,
    )


def crossref_lookup(query: str, rows: int = 3) -> list[CrossrefMatch]:
    """Query CrossRef /works for matches to a search string."""
    url = f"{CROSSREF_BASE}/works"
    params = {"query": query, "rows": rows, "mailto": CROSSREF_MAILTO}
    try:
        with _client() as c:
            resp = c.get(url, params=params)
            resp.raise_for_status()
        items = resp.json().get("message", {}).get("items", [])
    except Exception as e:
        logger.warning("CrossRef lookup failed for query=%r: %s", query, e)
        return []
    return [_format_match(it) for it in items]


def crossref_resolve_doi(doi: str) -> CrossrefMatch | None:
    """Resolve a DOI to its CrossRef metadata."""
    url = f"{CROSSREF_BASE}/works/{doi}"
    try:
        with _client() as c:
            resp = c.get(url, params={"mailto": CROSSREF_MAILTO})
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
        msg = resp.json().get("message", {})
    except Exception as e:
        logger.warning("CrossRef DOI resolve failed for %r: %s", doi, e)
        return None
    return _format_match(msg)


def _format_match(item: dict) -> CrossrefMatch:
    return CrossrefMatch(
        doi=item.get("DOI", ""),
        title=_format_title(item),
        authors=_format_authors(item),
        score=float(item.get("score") or 0),
        raw=item,
    )


def _format_authors(item: dict) -> str:
    authors = item.get("author", []) or []
    if not authors:
        return "(unknown authors)"
    if len(authors) <= 3:
        return ", ".join(_author_name(a) for a in authors)
    return f"{_author_name(authors[0])} et al."


def _author_name(a: dict) -> str:
    family = a.get("family", "")
    given = a.get("given", "")
    return f"{given} {family}".strip() or "(unknown)"


def _format_title(item: dict) -> str:
    titles = item.get("title", []) or []
    return titles[0] if titles else "(untitled)"


# ── Reference-hint extraction ───────────────────────────────────────────


def extract_reference_hints(slug: str, claim_text: str, body_text: str) -> list[str]:
    """Pull author/year/journal hints from a literature-context claim.

    Mirrors the heuristic in scripts/verify-references.py. Returns hints
    in decreasing order of expected CrossRef precision.
    """
    hints: list[str] = []
    combined = (claim_text or "") + " " + (body_text or "")

    # Best signal: full citation with journal — "Author (YYYY, *Journal* vol:page)"
    journal_refs = re.findall(
        r"([\w'\-]+(?:\s+(?:et\s+al\.?|[\w'\-]+))*?)\s*\((\d{4}),?\s*\*?([^)]+?)\*?\s*(\d+)?[:/]?(\d+)?\)",
        combined,
    )
    for author_block, year, journal, _, _ in journal_refs:
        first_author = re.split(r"[,;&]", author_block)[0].strip()
        if first_author.lower() in {"the", "this", "that", "from", "with", "and", "for"}:
            continue
        query = f"{first_author} {year} {journal.strip('* ')}"
        hints.append(query)

    # Next: simple "Author et al. (YYYY)" or "Author (YYYY)"
    simple_refs = re.findall(
        r"([\w'\-]+)\s+(?:et\s+al\.?,?\s*)?\((\d{4})\)",
        combined,
    )
    skip = {"the", "this", "that", "from", "with", "and", "for", "fig", "figure", "section"}
    for author, year in simple_refs:
        if author.lower() in skip:
            continue
        hints.append(f"{author} {year}")

    # Fallback: "interprets-author-year-..." slug
    m = re.match(r"interprets-([\w'\-]+)-(\d{4})", slug)
    if m:
        hints.append(f"{m.group(1).title()} {m.group(2)}")

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for h in hints:
        norm = h.lower().strip()
        if norm and norm not in seen:
            seen.add(norm)
            unique.append(h)
    return unique


# ── Claim file IO ────────────────────────────────────────────────────────


def _read_claim_file(path: Path) -> tuple[dict, str, str]:
    """Read a claim .md file and return (frontmatter, body, full_text)."""
    full = path.read_text()
    if not full.startswith("---"):
        return {}, full, full
    parts = full.split("---", 2)
    if len(parts) < 3:
        return {}, full, full
    fm_text = parts[1]
    body = parts[2].strip()
    # Tolerate the canonical script's "[]" quirk: bare [] on next line after a key
    fm_fixed = re.sub(r"^(\w[\w-]*):\n\[\]", r"\1: []", fm_text, flags=re.MULTILINE)
    try:
        fm = yaml.safe_load(fm_fixed) or {}
    except yaml.YAMLError as e:
        logger.warning("YAML parse failed for %s: %s", path, e)
        return {}, body, full
    return fm, body, full


def _write_claim_file(path: Path, fm: dict, body: str) -> None:
    """Write a claim .md file with new frontmatter, preserving body."""
    fm_yaml = yaml.safe_dump(
        fm, sort_keys=False, allow_unicode=True, default_flow_style=False, width=100
    )
    text = f"---\n{fm_yaml}---\n"
    if body:
        text += "\n" + body
        if not text.endswith("\n"):
            text += "\n"
    path.write_text(text)


# ── Per-claim verification ──────────────────────────────────────────────


@dataclass
class VerifyResult:
    """Outcome of verifying one literature-context claim."""

    paper_slug: str
    claim_slug: str
    status: Literal[
        "confirmed",      # had a DOI, CrossRef confirmed it resolves
        "found",          # no DOI, CrossRef matched at high confidence
        "low-confidence", # CrossRef matched but below threshold
        "not-found",      # CrossRef didn't return a useful match
        "no-hint",        # couldn't extract any reference hint from the claim
        "unresolvable",   # had a DOI, CrossRef said it doesn't exist
        "skipped",        # not a literature-context claim
    ]
    doi: str | None = None
    title: str = ""
    authors: str = ""
    score: float | None = None
    note: str = ""


def verify_claim(
    fm: dict,
    body: str,
    paper_slug: str,
    claim_path: Path,
    dry_run: bool,
) -> VerifyResult:
    """Verify one claim's literature-context citation."""
    role = fm.get("role")
    slug = fm.get("slug") or claim_path.stem
    claim_text = fm.get("claim", "") or ""

    if role != "literature-context":
        return VerifyResult(
            paper_slug=paper_slug, claim_slug=slug, status="skipped",
            note=f"role={role}, not literature-context",
        )

    # Path 1: claim already has a DOI. For literature-context claims the
    # canonical location is the top-level `doi:` field (the *cited* paper's
    # DOI). For other roles the top-level doi is `~` per § 4.1 — we only
    # consult assertions[0].doi as a legacy fallback.
    existing_doi = fm.get("doi")
    if not (existing_doi and isinstance(existing_doi, str) and existing_doi.startswith("10.")):
        # Legacy fallback: check assertions[0].doi (some older claim files
        # may have the cited DOI there per the canonical verify-references.py)
        assertions = fm.get("assertions") or []
        if assertions and isinstance(assertions[0], dict):
            ass_doi = assertions[0].get("doi")
            if isinstance(ass_doi, str) and ass_doi.startswith("10."):
                existing_doi = ass_doi

    if existing_doi and existing_doi.startswith("10."):
        match = crossref_resolve_doi(existing_doi)
        time.sleep(QUERY_DELAY_S)
        if match:
            return VerifyResult(
                paper_slug=paper_slug, claim_slug=slug, status="confirmed",
                doi=existing_doi, title=match.title, authors=match.authors,
                note="existing DOI resolves via CrossRef",
            )
        return VerifyResult(
            paper_slug=paper_slug, claim_slug=slug, status="unresolvable",
            doi=existing_doi,
            note="existing DOI does not resolve via CrossRef — likely hallucinated",
        )

    # Path 2: no DOI yet — query CrossRef from extracted hints
    hints = extract_reference_hints(slug, claim_text, body)
    if not hints:
        return VerifyResult(
            paper_slug=paper_slug, claim_slug=slug, status="no-hint",
            note="no Author (Year) or interprets-* slug pattern found in claim",
        )

    best: CrossrefMatch | None = None
    for hint in hints[:3]:  # don't burn through CrossRef on one claim
        results = crossref_lookup(hint)
        time.sleep(QUERY_DELAY_S)
        if results and (best is None or results[0].score > best.score):
            best = results[0]

    if best is None:
        return VerifyResult(
            paper_slug=paper_slug, claim_slug=slug, status="not-found",
            note=f"queried {len(hints[:3])} hints, no CrossRef matches",
        )

    if best.score < CONFIDENCE_THRESHOLD:
        return VerifyResult(
            paper_slug=paper_slug, claim_slug=slug, status="low-confidence",
            doi=best.doi, title=best.title, authors=best.authors, score=best.score,
            note=f"top match scored {best.score:.1f}, below threshold {CONFIDENCE_THRESHOLD}",
        )

    # High-confidence match — write the DOI back to the top-level `doi:` field
    # (canonical location for the cited paper's DOI on literature-context claims)
    if not dry_run:
        fm["doi"] = best.doi
        _write_claim_file(claim_path, fm, body)

    return VerifyResult(
        paper_slug=paper_slug, claim_slug=slug, status="found",
        doi=best.doi, title=best.title, authors=best.authors, score=best.score,
        note="" if dry_run else "DOI written to frontmatter",
    )


# ── Top-level walk ──────────────────────────────────────────────────────


def verify_refs(
    paper_slug: str | None,
    cfg: Config,
    dry_run: bool = False,
) -> list[VerifyResult]:
    """Walk a corpus directory and verify all literature-context claims.

    If paper_slug is given, walk only that paper's directory. Otherwise
    walk every paper directory under cfg.corpus_dir.
    """
    if cfg.corpus_dir is None:
        raise ValueError("corpus_dir not set; cannot verify refs")

    if paper_slug:
        paper_dirs = [cfg.corpus_dir / paper_slug]
    else:
        paper_dirs = sorted(p for p in cfg.corpus_dir.iterdir() if p.is_dir())

    results: list[VerifyResult] = []
    for paper_dir in paper_dirs:
        if not paper_dir.is_dir():
            logger.warning("paper directory not found: %s", paper_dir)
            continue
        slug = paper_dir.name
        for claim_path in sorted(paper_dir.glob("*.md")):
            if claim_path.name == "index.md":
                continue
            fm, body, _ = _read_claim_file(claim_path)
            if not fm:
                continue
            r = verify_claim(fm, body, slug, claim_path, dry_run)
            if r.status != "skipped":
                results.append(r)
                _print_result(r, dry_run)

    return results


def _print_result(r: VerifyResult, dry_run: bool) -> None:
    """Pretty-print one result line for the operator."""
    icon = {
        "confirmed": "✓",
        "found": "→",
        "low-confidence": "?",
        "not-found": "·",
        "no-hint": "—",
        "unresolvable": "✗",
    }.get(r.status, "·")
    line = f"  [{icon} {r.status}] {r.paper_slug}/{r.claim_slug}"
    if r.doi:
        line += f"  doi={r.doi}"
    if r.score is not None:
        line += f"  score={r.score:.1f}"
    print(line)
    if r.title:
        print(f"      {r.authors} — {r.title[:90]}")
    if r.note and r.status in ("low-confidence", "not-found", "no-hint", "unresolvable"):
        print(f"      note: {r.note}")
