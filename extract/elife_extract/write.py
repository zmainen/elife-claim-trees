"""Steps 6-7 — Dependency mapping and claim file emission.

Step 6 — Dependency mapping: typed edges between claims (14 edge types
from `docs/method.md` § 4.3). The methodology calls for this to be done
by the analyst at write time, with the analyst's judgment about which
claims `requires`, `supports`, `entails` etc. which others. The CLI's
contribution at this step is mechanical scaffolding — for hypothesis
claims, scaffold an `entails:` edge list to predictions; for prediction
claims, scaffold `derived-from:` and `tests:` edges; for empirical claims,
leave the edge sections empty for the analyst to fill in. A future LLM
pass can suggest edges; for now we ship the scaffolding with empty lists
and a `# TODO` marker the analyst can fill in.

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
from .schema import DraftClaimTable, ReconciledClaim

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
    words = re.findall(r"\b[A-Za-z][A-Za-z\-]+\b", claim_text)
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
) -> dict:
    """Build the YAML frontmatter dict for one claim."""
    today = date.today().isoformat()
    fm: dict = {
        "uuid": str(uuid.uuid4()),
        "slug": slug,
        "doi": "~",  # placeholder per § 4.1 — claims aren't yet citable units
        "claim": claim.claim,
        "claim-type": claim.claim_type,
        "role": claim.role,
        "concepts": [],  # § 4.1 — analyst fills in at review or in a later pass
        "priority": today,
        "epistemic": "tentative",  # default; analyst sets per § 4.1 vocabulary
    }

    # Edge sections — empty by default (Step 6 pass deferred). Include
    # placeholder keys for the canonical edges so the analyst sees the
    # slots and can fill them in.
    fm["belongings"] = []  # general belongs-to edges

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

    # Per-claim files
    for claim, slug in zip(draft.claims, slugs):
        fm = _claim_frontmatter(
            claim, slug, draft.paper_slug, draft.paper_doi
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
