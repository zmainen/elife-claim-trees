"""Steps 6-7 — Dependency mapping and claim file emission.

Step 6 — Dependency mapping: typed edges between claims (the edge inventory
in `docs/method.md` § 4.3). This used to be left to the analyst, with the
writer emitting `belongings: []` and a TODO. It is now inferred by a model
call — see `edges.py`, which carries the vocabulary mapping and the rule for
where each relation type is stored. Pass --no-infer-edges to skip it.

Step 7 — Write claim files: generate UUID4 per claim, derive a slug, and
write each claim as <corpus_dir>/<paper_slug>/<claim_slug>.md per the
schema in § 4. Also write a paper index.md with title, DOI, authors,
abstract, and any deposit URLs (best-effort — these come from prepare,
which has heuristic-quality metadata).
"""

from __future__ import annotations

import logging
import re
import uuid
from datetime import date
from pathlib import Path

import yaml

from .config import Config
from .prepare import _ascii_fold
from .edges import edges_for_slug
from .schema import DraftClaimTable, ReconciledClaim
from .oxa import (
    Claim, ClaimGraph, ClaimRelation, ClaimMetadata, SourceSpan,
    Document, text_node, claim_from_reconciled, build_document, EDGE_MAP,
)

logger = logging.getLogger(__name__)


# ── Slug derivation for individual claims ────────────────────────────────


def derive_claim_slug(claim_text: str, panel: str | None = None) -> str:
    """Produce a 3-6 word hyphenated slug from a claim's text.

    Drop stopwords; take the first 3-5 content words; lowercase + hyphenate.
    Append a panel suffix if the slug would otherwise be ambiguous.
    """
    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did",
        "of", "to", "in", "on", "at", "by", "for", "with", "from", "as",
        "and", "or", "but", "if", "then", "than", "that", "this", "these",
        "these", "those", "their", "its", "it", "they", "there",
        "approximately", "approximately,", "almost", "nearly",
    }
    words = re.findall(r"\b[A-Za-z][A-Za-z\-]+\b", _ascii_fold(claim_text))
    keep = []
    for w in words:
        wl = w.lower()
        if wl in stopwords:
            continue
        keep.append(re.sub(r"[^a-z0-9]+", "-", wl).strip("-"))
        if len(keep) >= 5:
            break
    if not keep:
        keep = ["claim"]
    slug = "-".join(keep)[:60].rstrip("-")
    return slug


def _unique_slugs(claims: list[ReconciledClaim]) -> list[str]:
    """Generate per-claim slugs; disambiguate with counter on collision."""
    raw = [derive_claim_slug(c.claim, c.panel) for c in claims]
    seen: dict[str, int] = {}
    out: list[str] = []
    for s in raw:
        if s in seen:
            seen[s] += 1
            out.append(f"{s}-{seen[s]}")
        else:
            seen[s] = 1
            out.append(s)
    return out


# ── Schema mapping: ReconciledClaim → claim file frontmatter ────────────


# Map our claim_type vocabulary to the elife-claim-trees schema (§ 4.1).
# Same vocabulary; pass through directly for now.
_CLAIM_TYPE_PASSTHROUGH = {
    "empirical", "interpretive", "existence", "synthesis", "assessment"
}


def _claim_frontmatter(
    claim: ReconciledClaim,
    slug: str,
    paper_slug: str,
    paper_doi: str,
    edges: list[dict] | None = None,
) -> dict:
    """Build the YAML frontmatter dict for one claim."""
    today = date.today().isoformat()
    fm: dict = {
        "uuid": str(uuid.uuid4()),
        "slug": slug,
        # None serialises as YAML null, matching curated files. Writing the
        # string "~" produced a quoted '~' that parsers read as text.
        "doi": None,  # per § 4.1 — claims aren't yet citable units
        "claim": claim.claim,
        "claim-type": claim.claim_type,
        "role": claim.role,
        "concepts": [],  # § 4.1 — analyst fills in at review or in a later pass
        "priority": today,
        # Roles that are not empirical carry their role as the epistemic
        # value in the curated corpus; the rest start unassessed.
        "epistemic": (
            claim.role if claim.role in ("hypothesis", "prediction") else "tentative"
        ),
    }

    # Step 6 — dependency mapping. `requires`/`supports` live under
    # `belongings:`; every other relation is a top-level key. See
    # edges.BELONGINGS_RELATIONS for why.
    top, belongings = edges_for_slug(edges or [], slug)
    fm.update(top)
    fm["belongings"] = belongings

    # Assertions block — link the claim to its panel and source paper
    if claim.panel:
        fm["assertions"] = [
            {
                "paper-slug": paper_slug,
                "doi": paper_doi,
                "panel": claim.panel,
                "confidence": "tentative",
            }
        ]
    else:
        fm["assertions"] = [
            {
                "paper-slug": paper_slug,
                "doi": paper_doi,
                "panel": None,
                "confidence": "tentative",
            }
        ]

    # Reproductions — empty list; verification is per-paper and not
    # something extract produces. Analyst or verify.py downstream fills.
    fm["reproductions"] = []

    return fm


def _claim_body(claim: ReconciledClaim) -> str:
    """Build the prose body of a claim file.

    The body is for caveats, alternative interpretations, and reasoning
    that doesn't compress into frontmatter. We seed it with the agent
    evidence quotes and the reconciler's notes — the analyst can revise.
    """
    parts = []
    if claim.notes:
        parts.append(f"**Notes from extraction:** {claim.notes}")
        parts.append("")

    if claim.evidence_by_agent:
        parts.append(
            "<!-- Evidence quotes from the extraction agents — preserved for "
            "audit. Edit or remove as appropriate. -->"
        )
        parts.append("")
        for agent, quote in claim.evidence_by_agent.items():
            parts.append(f"**{agent}-reader evidence:**")
            parts.append(f"> {quote}")
            parts.append("")

    if not parts:
        return ""
    return "\n".join(parts).rstrip() + "\n"


def _format_claim_file(fm: dict, body: str) -> str:
    """Render frontmatter + body to a claim .md file."""
    fm_yaml = yaml.safe_dump(
        fm,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=100,
    )
    text = f"---\n{fm_yaml}---\n"
    if body:
        text += "\n" + body
    return text


# ── Paper-level index.md ─────────────────────────────────────────────────


def _format_paper_index(
    draft: DraftClaimTable,
    claim_slugs: list[str],
) -> str:
    """Render <paper_slug>/index.md with title, DOI, authors, summary."""
    fm = {
        "paper-slug": draft.paper_slug,
        "title": draft.paper_title or "(title not detected)",
        "doi": draft.paper_doi,
        "url": f"https://doi.org/{draft.paper_doi}",
        "added": date.today().isoformat(),
        "claim-count": len(draft.claims),
        "extraction-path": draft.extraction_path,
    }
    fm_yaml = yaml.safe_dump(
        fm, sort_keys=False, allow_unicode=True, default_flow_style=False
    )

    body = ["## Claims", ""]
    for c, slug in zip(draft.claims, claim_slugs):
        body.append(f"- [{slug}]({slug}.md) ({c.confidence}) — {c.claim[:120]}")
    body.append("")
    body.append("## Extraction provenance")
    body.append("")
    body.append(f"- per-agent counts: {draft.per_agent_counts}")
    body.append(f"- reconciliation strategy: {draft.config_snapshot.get('reconcile_strategy', '?')}")
    body.append(f"- prompt variant: {draft.config_snapshot.get('prompt_variant', '?')}")
    body.append("")
    return f"---\n{fm_yaml}---\n\n" + "\n".join(body)


# ── OXA write path ───────────────────────────────────────────────────────


def _reconciled_to_oxa_claim(
    claim: ReconciledClaim,
    slug: str,
) -> Claim:
    """Convert a ReconciledClaim to an OXA Claim node."""
    return claim_from_reconciled(
        claim_text=claim.claim,
        slug=slug,
        role=claim.role,
        panel=claim.panel,
        epistemic=None,  # ReconciledClaim doesn't carry epistemic strength
        confidence=claim.confidence,
        sources=[str(s) for s in claim.sources],
        evidence_by_agent={str(k): v for k, v in claim.evidence_by_agent.items()},
    )


def write_oxa_document(draft: DraftClaimTable, cfg: Config) -> Path:
    """Emit an OXA Document JSON file for a paper's claims.

    Produces <corpus_dir>/<paper_slug>.oxa.json containing a Document
    with a ClaimGraph of Claim nodes. This is the OXA-native output
    path — the source of truth for downstream tools.

    Also writes per-claim YAML markdown files for human browsing
    (backward compatibility with the existing corpus format).
    """
    if cfg.corpus_dir is None:
        raise ValueError("corpus_dir not set; cannot write OXA document")

    slugs = _unique_slugs(draft.claims)

    # Convert each reconciled claim to an OXA Claim node
    oxa_claims = []
    for claim, slug in zip(draft.claims, slugs):
        oxa_claims.append(_reconciled_to_oxa_claim(claim, slug))

    # Build the OXA Document
    doc = build_document(
        paper_slug=draft.paper_slug,
        paper_doi=draft.paper_doi,
        paper_title=draft.paper_title,
        claims=oxa_claims,
    )

    # Write the OXA JSON
    cfg.corpus_dir.mkdir(parents=True, exist_ok=True)
    oxa_path = cfg.corpus_dir / f"{draft.paper_slug}.oxa.json"

    import json
    out = doc.model_dump(mode="json", exclude_none=True)
    oxa_path.write_text(json.dumps(out, indent=2, ensure_ascii=False))

    logger.info("OXA document: %s (%d claims)", oxa_path, len(oxa_claims))
    return oxa_path


# ── Top-level write ──────────────────────────────────────────────────────


def write_claim_files(draft: DraftClaimTable, cfg: Config) -> list[Path]:
    """Emit claim files into <corpus_dir>/<paper_slug>/.

    Returns the list of paths written (the index plus one per claim).
    Refuses to overwrite existing files; use --force in a future pass
    to allow reruns. For now, the analyst can rm the directory first.
    """
    if cfg.corpus_dir is None:
        raise ValueError("corpus_dir not set; cannot write claim files")

    paper_dir = cfg.corpus_dir / draft.paper_slug
    if paper_dir.exists() and any(paper_dir.iterdir()):
        raise FileExistsError(
            f"refusing to overwrite non-empty {paper_dir}. "
            "Move or delete it before re-running write."
        )
    paper_dir.mkdir(parents=True, exist_ok=True)

    slugs = _unique_slugs(draft.claims)
    written: list[Path] = []

    # Step 6 — infer the edges between claims before writing any of them,
    # since an edge names two slugs and both must already be assigned.
    edges: list[dict] = []
    # A supplied edge answer wins over calling a backend, and goes through exactly the same
    # validation — unknown slugs dropped, self-edges dropped, reciprocals synthesised. The
    # route in differs; the checks do not. This exists because the deductive spine is the
    # part of a claim tree that matters most and the part most easily lost to a provider
    # outage: on a live Gädeke run every other stage succeeded and the edges were gone.
    supplied = getattr(cfg, "edges_json", None)
    if supplied:
        from .edges import edges_from_raw
        try:
            edges = edges_from_raw(Path(supplied).read_text(encoding="utf-8"),
                                   slugs, source=f"supplied:{supplied}")
        except Exception as e:                                   # noqa: BLE001
            logger.warning("supplied edge file unusable (%s); writing claims without edges", e)
    elif getattr(cfg, "infer_edges", True):
        from .edges import infer_edges
        try:
            edges = infer_edges(draft, slugs, cfg)
        except Exception as e:                                   # noqa: BLE001
            logger.warning("edge inference failed (%s); writing claims without edges", e)

    # Per-claim files
    for claim, slug in zip(draft.claims, slugs):
        fm = _claim_frontmatter(
            claim, slug, draft.paper_slug, draft.paper_doi, edges
        )
        body = _claim_body(claim)
        text = _format_claim_file(fm, body)
        path = paper_dir / f"{slug}.md"
        path.write_text(text)
        written.append(path)

    # Paper index.md
    index_path = paper_dir / "index.md"
    index_path.write_text(_format_paper_index(draft, slugs))
    written.append(index_path)

    return written
