"""External review pass — Step 4.5, between reconciliation and write.

A single Opus call that takes the reconciled draft and the paper's context,
and returns a *patch* — targeted edits and new claims — that the runner applies
to produce the revised draft.

  Bias 1: prediction-role under-coverage
  Bias 2: hypothesis-role under-coverage
  Bias 3: multi-panel claims collapsed
  Bias 4: synthesis vs interpretation confusion

The patch format (edits + additions) is cheaper to emit and easier to audit
than a full replacement table: the reviewer names each change explicitly, so
a diff between the reconciled draft and the reviewed draft is meaningful.

Cost: ~$1-2 per paper (one Opus call with paper context + draft).
Latency: 1-2 minutes.
"""

from __future__ import annotations

import copy
import logging

from .agents import parse_json_response, stream_text
from .config import Config, token_budget
from .prepare import PreparedPaper
from .schema import DraftClaimTable, ReconciledClaim, ReviewPatch

logger = logging.getLogger(__name__)


def load_reviewer_prompt(cfg: Config) -> str:
    """The reviewer's system prompt: its task, then the contract. See prompts.py."""
    from .prompts import prompt
    return prompt("external-reviewer", cfg)


def _format_paper_context(paper: PreparedPaper, max_results_chars: int = 120000) -> str:
    """Format the paper context for the reviewer's user message.

    The reviewer now gets the abstract, the Introduction, the Results, the Discussion and the
    figure captions — the organising hypothesis and the literature-context premises it was
    previously asked to *infer* are stated in the Introduction and the Discussion. Methods stay
    out: the reviewer's job is the argument, not the procedure.

    The results section is truncated only if it is exceptionally long. The ceiling is set above
    a typical eLife paper — Gädeke's whole reviewer context is about 67k characters — so a normal
    paper is never cut, and only a pathologically large results section is bounded.
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
        f"## Introduction",
        "",
        paper.introduction_text,
        "",
        f"## Results section",
        "",
        results + truncated_note,
        "",
        f"## Discussion",
        "",
        paper.discussion_text,
        "",
        f"## Figure captions",
        "",
        paper.captions_text,
    ]
    return "\n".join(parts)


def build_review_request(paper: PreparedPaper, draft: DraftClaimTable,
                         cfg: Config) -> tuple[str, str]:
    """The exact (system, user) the reviewer would send."""
    return load_reviewer_prompt(cfg), (
        f"{_format_paper_context(paper)}\n\n"
        f"## Reconciled draft claim table (your input to patch)\n\n"
        f"```json\n{draft.model_dump_json(indent=2)}\n```\n\n"
        f"Return the patch JSON per your instructions. "
        f"JSON only — no surrounding prose."
    )


def _review_output_schema() -> dict:
    """JSON schema for ReviewPatch, filtered to exclude runner-filled fields."""
    from .agents import _filter_schema
    raw = ReviewPatch.model_json_schema()
    return _filter_schema(raw)


def patch_from_raw(raw: str) -> ReviewPatch:
    """Parse and validate a raw reviewer answer into a ReviewPatch."""
    parsed = parse_json_response(raw)
    if not isinstance(parsed, dict):
        raise ValueError(
            f"external reviewer returned non-dict JSON: {type(parsed).__name__}"
        )
    return ReviewPatch(**parsed)


def apply_patch(draft: DraftClaimTable, patch: ReviewPatch) -> DraftClaimTable:
    """Apply a ReviewPatch to a DraftClaimTable, returning a revised copy.

    - edits: update named fields of the matched claim (matched by `claim` sentence).
    - additions: append new claims to the end of the list.
    - Claims with no matching edit are returned unchanged.
    - A claim sentence in `edits` that does not match any draft claim is logged
      as a warning and skipped (the reviewer may have paraphrased).
    """
    # Index by claim sentence for O(1) lookup
    claim_index: dict[str, int] = {c.claim: i for i, c in enumerate(draft.claims)}

    # Deep copy so we don't mutate the caller's draft
    revised_claims = [copy.deepcopy(c) for c in draft.claims]

    for edit in patch.edits:
        idx = claim_index.get(edit.claim)
        if idx is None:
            logger.warning(
                "external reviewer edit: claim sentence not found in draft — skipped: %.80s",
                edit.claim,
            )
            continue
        claim = revised_claims[idx]
        if edit.role is not None:
            claim.role = edit.role
        if edit.claim_type is not None:
            claim.claim_type = edit.claim_type
        if edit.panel is not None:
            claim.panel = edit.panel
        if edit.notes is not None:
            claim.notes = edit.notes

    for addition in patch.additions:
        revised_claims.append(copy.deepcopy(addition))

    # Build revised DraftClaimTable preserving all provenance fields
    revised_data = draft.model_dump()
    revised_data["claims"] = [c.model_dump() for c in revised_claims]
    revised_data.setdefault("config_snapshot", {})
    revised_data["config_snapshot"]["external_review"] = True
    return DraftClaimTable(**revised_data)


def review_from_raw(raw: str, draft: DraftClaimTable) -> tuple[DraftClaimTable, ReviewPatch]:
    """Validate a raw reviewer answer and apply it to produce a revised DraftClaimTable.

    Returns both the revised table and the raw patch, so the caller can write both.
    """
    patch = patch_from_raw(raw)
    revised = apply_patch(draft, patch)
    return revised, patch


def external_review(
    paper: PreparedPaper,
    draft: DraftClaimTable,
    cfg: Config,
) -> tuple[DraftClaimTable, ReviewPatch, dict]:
    """Run the external Opus reviewer pass on a reconciled draft.

    Returns (revised DraftClaimTable, raw ReviewPatch, usage dict).
    Preserves the original draft on the caller side (caller is responsible for
    saving the original separately if it wants both).
    """
    system_prompt, user_message = build_review_request(paper, draft, cfg)

    logger.info(
        "external review: paper=%s claims=%d via %s",
        paper.paper_slug, len(draft.claims), cfg.model_reconcile,
    )
    raw, usage = stream_text(
        cfg,
        model=cfg.model_reconcile,  # same model class as reconciliation
        system=system_prompt,
        user=user_message,
        max_tokens=token_budget("external-reviewer", len(draft.claims)),
        label="external-reviewer",
        output_schema=_review_output_schema(),
    )

    revised, patch = review_from_raw(raw, draft)
    return revised, patch, usage
