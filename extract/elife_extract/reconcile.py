"""Step 4 — Reconciliation: fold three agent extractions into a draft claim table.

Per `docs/method.md` § 3.3 Step 4 + the reconciler prompt at
prompts/reconciler.md. The reconciler is a single Opus call that takes
the three agent outputs and produces a confidence-tagged DraftClaimTable.

The hard part is semantic matching — agents will phrase the same claim
differently. We hand the three full lists to the reconciler model and let
it match. Programmatic alternatives (literal string match, embedding
similarity) miss too many semantic equivalences.
"""

from __future__ import annotations

import json
import logging

from .agents import get_client, load_prompt, parse_json_response
from .config import Config
from .schema import AgentExtraction, DraftClaimTable, ReconciledClaim

logger = logging.getLogger(__name__)


# ── Reconciler prompt loading ────────────────────────────────────────────


def load_reconciler_prompt(cfg: Config):
    """Load the reconciler prompt from disk (variant-aware)."""
    if cfg.prompt_variant == "default":
        path = cfg.prompts_dir / "reconciler.md"
    else:
        path = cfg.prompts_dir / cfg.prompt_variant / "reconciler.md"
    if not path.is_file():
        raise FileNotFoundError(f"Reconciler prompt not found: {path}")
    return path.read_text()


# ── Reconciler invocation ───────────────────────────────────────────────


def _format_agent_input(extraction: AgentExtraction) -> str:
    """Format an agent's extraction for the reconciler's user message."""
    lines = [f"## Agent {extraction.agent}-reader (model: {extraction.model})"]
    lines.append(f"Surfaced {len(extraction.claims)} candidate claim(s):")
    lines.append("")
    for i, c in enumerate(extraction.claims, 1):
        lines.append(f"### {extraction.agent}-{i}")
        lines.append(f"- claim: {c.claim}")
        lines.append(f"- panel: {c.panel}")
        lines.append(f"- claim_type: {c.claim_type}")
        lines.append(f"- role: {c.role}")
        lines.append(f"- evidence: {c.evidence}")
        lines.append(f"- agent_confidence: {c.confidence}")
        if c.notes:
            lines.append(f"- notes: {c.notes}")
        lines.append("")
    return "\n".join(lines)


def reconcile(
    results: AgentExtraction,
    caption: AgentExtraction,
    structure: AgentExtraction,
    cfg: Config,
    paper_doi: str,
    paper_title: str | None = None,
) -> DraftClaimTable:
    """Reconcile three extractions into a draft claim table via Opus.

    The reconciler sees all three lists at once. It returns a DraftClaimTable
    matching the schema in schema.py — with confidence (high / contested /
    single-source), the list of agent sources per claim, and per-agent
    evidence quotes preserved.
    """
    if cfg.reconcile_strategy != "confidence-tagged":
        raise NotImplementedError(
            f"reconcile_strategy={cfg.reconcile_strategy!r} not yet implemented "
            f"(only 'confidence-tagged' available in Phase D)"
        )

    system_prompt = load_reconciler_prompt(cfg)
    user_message = (
        f"# Paper: {paper_title or 'unknown'}\n"
        f"DOI: {paper_doi}\n"
        f"Slug: {results.paper_slug}\n\n"
        f"{_format_agent_input(results)}\n\n"
        f"{_format_agent_input(caption)}\n\n"
        f"{_format_agent_input(structure)}\n\n"
        f"Reconcile these three agent outputs into a single confidence-tagged "
        f"draft claim table per the schema in your instructions. Return JSON only."
    )

    client = get_client(cfg)
    logger.info(
        "reconciling %d (results) + %d (caption) + %d (structure) claims via %s",
        len(results.claims),
        len(caption.claims),
        len(structure.claims),
        cfg.model_reconcile,
    )
    text_chunks: list[str] = []
    with client.messages.stream(
        model=cfg.model_reconcile,
        max_tokens=32768,  # reconciliation output can be large; budget headroom
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            text_chunks.append(text)
    raw = "".join(text_chunks)
    parsed = parse_json_response(raw)
    if not isinstance(parsed, dict):
        raise ValueError(
            f"reconciler returned non-dict JSON: {type(parsed).__name__}"
        )

    # Build the DraftClaimTable, filling in fields the reconciler may have skipped
    parsed.setdefault("paper_doi", paper_doi)
    parsed.setdefault("paper_title", paper_title)
    parsed.setdefault("paper_slug", results.paper_slug)
    parsed.setdefault(
        "per_agent_counts",
        {
            "results": len(results.claims),
            "caption": len(caption.claims),
            "structure": len(structure.claims),
        },
    )
    parsed.setdefault(
        "config_snapshot",
        {
            "model_results": cfg.model_results,
            "model_caption": cfg.model_caption,
            "model_structure": cfg.model_structure,
            "model_reconcile": cfg.model_reconcile,
            "prompt_variant": cfg.prompt_variant,
            "reconcile_strategy": cfg.reconcile_strategy,
        },
    )
    return DraftClaimTable(**parsed)
