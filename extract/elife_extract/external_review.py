"""External review pass — Step 4.5, between reconciliation and write.

A single Opus call that takes the reconciled draft and the paper's context,
and returns a revised draft addressing the structural-inference biases the
three Sonnet extraction agents systematically miss:

  Bias 1: prediction-role under-coverage
  Bias 2: hypothesis-role under-coverage
  Bias 3: multi-panel claims collapsed
  Bias 4: synthesis vs interpretation confusion

Substitutes for the human analyst at Step 5 when `--review-mode=external`
is set. The methodology was written assuming a curator-in-the-loop; this
module is what makes the CLI usable in environments without one.

Cost: ~$1-2 per paper (one Opus call with paper context + draft).
Latency: 1-2 minutes.
"""

from __future__ import annotations

import json
import logging

from .agents import parse_json_response, stream_text
from .config import Config
from .prepare import PreparedPaper
from .schema import DraftClaimTable

logger = logging.getLogger(__name__)


def load_reviewer_prompt(cfg: Config) -> str:
    """The reviewer's system prompt: its task, then the contract. See prompts.py."""
    from .prompts import prompt
    return prompt("external-reviewer", cfg)


def _format_paper_context(paper: PreparedPaper, max_results_chars: int = 60000) -> str:
    """Format the paper context for the reviewer's user message.

    Truncate the results section if it's exceptionally long (eLife papers
    are typically 30-100KB; the reviewer can handle plenty but we don't
    need to send the whole 200KB if a paper happens to be huge).
    """
    results = paper.results_text
    truncated_note = ""
    if len(results) > max_results_chars:
        results = results[:max_results_chars]
        truncated_note = f"\n\n[results section truncated at {max_results_chars} chars; full length was {len(paper.results_text)}]"

    parts = [
        f"# Paper",
        f"DOI: {paper.doi}",
        f"Slug: {paper.paper_slug}",
        f"Title: {paper.title}",
        "",
        f"## Abstract",
        "",
        paper.abstract,
        "",
        f"## Results section",
        "",
        results + truncated_note,
    ]
    return "\n".join(parts)


def build_review_request(paper: PreparedPaper, draft: DraftClaimTable,
                         cfg: Config) -> tuple[str, str]:
    """The exact (system, user) the reviewer would send."""
    return load_reviewer_prompt(cfg), (
        f"{_format_paper_context(paper)}\n\n"
        f"## Reconciled draft claim table (your input to revise)\n\n"
        f"```json\n{draft.model_dump_json(indent=2)}\n```\n\n"
        f"Return the revised JSON claim table per your instructions. "
        f"JSON only — no surrounding prose."
    )


def review_from_raw(raw: str, draft: DraftClaimTable) -> DraftClaimTable:
    """Validate a raw reviewer answer into a revised DraftClaimTable.

    Every route in goes through here, so the fields the draft owns — how the paper was read,
    the per-agent counts — survive whoever answered.
    """
    parsed = parse_json_response(raw)
    if not isinstance(parsed, dict):
        raise ValueError(
            f"external reviewer returned non-dict JSON: {type(parsed).__name__}"
        )

    # Preserve fields the reviewer may have dropped
    parsed.setdefault("paper_doi", draft.paper_doi)
    parsed.setdefault("paper_title", draft.paper_title)
    parsed.setdefault("paper_slug", draft.paper_slug)
    # Assigned, not setdefault: how the paper was read is the draft's to state, and a
    # reviewer that invented a value would overwrite it. The prompt no longer shows one,
    # but the guarantee should not depend on the prompt.
    parsed["extraction_path"] = draft.extraction_path
    parsed["extraction_path_note"] = draft.extraction_path_note
    parsed.setdefault("per_agent_counts", dict(draft.per_agent_counts))
    parsed.setdefault("config_snapshot", dict(draft.config_snapshot))

    # Stamp the snapshot with the review pass
    parsed["config_snapshot"]["external_review"] = True

    return DraftClaimTable(**parsed)

def external_review(
    paper: PreparedPaper,
    draft: DraftClaimTable,
    cfg: Config,
) -> DraftClaimTable:
    """Run the external Opus reviewer pass on a reconciled draft.

    Returns a revised DraftClaimTable. Preserves the original draft on
    the caller side (caller is responsible for saving the original
    separately if it wants both).
    """
    system_prompt, user_message = build_review_request(paper, draft, cfg)

    logger.info(
        "external review: paper=%s claims=%d via %s",
        paper.paper_slug, len(draft.claims), cfg.model_reconcile,
    )
    raw = stream_text(
        cfg,
        model=cfg.model_reconcile,  # same model class as reconciliation
        system=system_prompt,
        user=user_message,
        max_tokens=32768,
        label="external-reviewer",
    )

    return review_from_raw(raw, draft)
