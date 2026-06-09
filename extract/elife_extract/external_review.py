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

from .agents import get_client, parse_json_response
from .config import Config
from .prepare import PreparedPaper
from .schema import DraftClaimTable

logger = logging.getLogger(__name__)


def load_reviewer_prompt(cfg: Config) -> str:
    """Load the external-reviewer prompt from disk (variant-aware)."""
    if cfg.prompt_variant == "default":
        path = cfg.prompts_dir / "external-reviewer.md"
    else:
        path = cfg.prompts_dir / cfg.prompt_variant / "external-reviewer.md"
    if not path.is_file():
        raise FileNotFoundError(f"External reviewer prompt not found: {path}")
    return path.read_text()


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
    system_prompt = load_reviewer_prompt(cfg)
    paper_context = _format_paper_context(paper)
    draft_json = draft.model_dump_json(indent=2)

    user_message = (
        f"{paper_context}\n\n"
        f"## Reconciled draft claim table (your input to revise)\n\n"
        f"```json\n{draft_json}\n```\n\n"
        f"Return the revised JSON claim table per your instructions. "
        f"JSON only — no surrounding prose."
    )

    client = get_client(cfg)
    logger.info(
        "external review: paper=%s claims=%d via %s",
        paper.paper_slug, len(draft.claims), cfg.model_reconcile,
    )
    text_chunks: list[str] = []
    with client.messages.stream(
        model=cfg.model_reconcile,  # use the same Opus model as reconciliation
        max_tokens=32768,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for chunk in stream.text_stream:
            text_chunks.append(chunk)
    raw = "".join(text_chunks)

    parsed = parse_json_response(raw)
    if not isinstance(parsed, dict):
        raise ValueError(
            f"external reviewer returned non-dict JSON: {type(parsed).__name__}"
        )

    # Preserve fields the reviewer may have dropped
    parsed.setdefault("paper_doi", draft.paper_doi)
    parsed.setdefault("paper_title", draft.paper_title)
    parsed.setdefault("paper_slug", draft.paper_slug)
    parsed.setdefault("extraction_path", draft.extraction_path)
    parsed.setdefault("per_agent_counts", dict(draft.per_agent_counts))
    parsed.setdefault("config_snapshot", dict(draft.config_snapshot))

    # Stamp the snapshot with the review pass
    parsed["config_snapshot"]["external_review"] = True

    return DraftClaimTable(**parsed)
