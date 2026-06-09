"""Pydantic schema for candidate claims and the draft claim table.

The agent prompts (prompts/{results,caption,structure}-reader.md) instruct
agents to emit a JSON list of candidate-claim objects. This module models
that wire format and validates parsed responses.

The full claim-file schema (with UUIDs, edges, reproductions, prose body)
lives in elife-claim-trees § 4. This module covers only the extraction
phase's draft format; the writer (Phase E) maps draft claims onto the
full schema.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


ClaimType = Literal[
    "empirical", "interpretive", "existence", "synthesis", "assessment",
    "hypothesis", "prediction", "control", "scope", "methodological",
    "interpretation", "literature-context",
]
Role = Literal[
    "hypothesis",
    "prediction",
    "empirical",
    "control",
    "scope",
    "methodological",
    "synthesis",
    "interpretation",
    "literature-context",
]
AgentName = Literal["results", "caption", "structure", "reviewer"]
AgentConfidence = Literal["high", "tentative"]
ReconciledConfidence = Literal["high", "contested", "single-source"]


class CandidateClaim(BaseModel):
    """One claim as emitted by a single extraction agent."""

    claim: str = Field(..., min_length=8, description="Declarative sentence in active voice.")
    panel: str | None = Field(
        None, description="Panel ID like fig3a; null for synthesis-level claims."
    )
    claim_type: ClaimType
    role: Role
    evidence: str = Field(..., min_length=1, description="Verbatim quote grounding the claim.")
    confidence: AgentConfidence
    notes: str | None = None


class AgentExtraction(BaseModel):
    """The output of one extraction agent on one paper."""

    agent: AgentName
    paper_slug: str
    model: str
    claims: list[CandidateClaim]


class ReconciledClaim(BaseModel):
    """A candidate claim after the reconciliation step."""

    claim: str
    panel: str | None
    claim_type: ClaimType
    role: Role
    confidence: ReconciledConfidence
    sources: list[AgentName] = Field(
        ..., description="Which agents surfaced this claim (1-3)."
    )
    evidence_by_agent: dict[AgentName, str] = Field(
        default_factory=dict,
        description="Per-agent evidence quotes when surfaced.",
    )
    notes: str | None = None


class DraftClaimTable(BaseModel):
    """The output of Step 4 — what goes to the human review gate."""

    paper_slug: str
    paper_doi: str
    paper_title: str | None = None
    extraction_path: Literal["pdf", "github-readme", "elife-api", "web-fetch"] = "pdf"
    extraction_path_note: str | None = None
    per_agent_counts: dict[AgentName, int] = Field(default_factory=dict)
    claims: list[ReconciledClaim]
    config_snapshot: dict = Field(
        default_factory=dict,
        description="Models used, prompt variant, etc. — for reproducibility.",
    )
