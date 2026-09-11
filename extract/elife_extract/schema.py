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


# Seven, not twelve. The list had been widened to accept every word any prompt happened to use
# as a type — `control`, `scope`, `methodological` are roles — so the schema enforced nothing.
# These are the five in docs/claim-format.md plus the two the corpus uses for its deductive
# layer; the definitions are in vocabulary.py and the contract renders them.
ClaimType = Literal[
    "empirical", "interpretive", "existence", "synthesis", "assessment",
    "hypothesis", "prediction",
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

    claim: str = Field(..., min_length=8, description=(
        "One declarative sentence in active voice, with the paper's own numbers and the "
        "paper's own epistemic verb."))
    panel: str | None = Field(None, description=(
        "The panel that shows the result, lowercase, as the paper labels it: fig3a, fig5d-h, "
        "fig3s1c, table1. Several panels separated by commas when the claim spans them. null "
        "for a claim no panel shows."))
    claim_type: ClaimType = Field(..., description="The kind of proposition; see the vocabulary.")
    role: Role = Field(..., description="The work it does in the argument; see the vocabulary.")
    addresses: str | None = Field(None, description=(
        "For a hypothesis or an alternative explanation, the research question it answers, as "
        "the paper states it or in one sentence; null for every other role."))
    evidence: str = Field(..., min_length=1, description=(
        "A verbatim quote from the text you were given, at most two sentences, that grounds "
        "the claim. It is checked against the source."))
    confidence: AgentConfidence = Field(..., description="high or tentative; see the vocabulary.")
    span: str | None = Field(None, description=(
        "The id of the span the evidence quote comes from, exactly as it is bracketed before "
        "the sentence in your slice (results-026). null when the sentence shows no id."))
    notes: str | None = Field(None, description=(
        "Hedges, alternative readings, or what made this tentative. null when there is nothing "
        "to say."))
    evidence_verified: bool | None = Field(None, description=(
        "Filled by the runner. Leave null."))
    evidence_verified_against: Literal["span", "slice"] | None = Field(None, description=(
        "Filled by the runner: whether the quote matched the cited span or only the wider "
        "slice. Leave null."))


class AgentExtraction(BaseModel):
    """The output of one extraction agent on one paper."""

    agent: AgentName
    paper_slug: str
    model: str
    claims: list[CandidateClaim]


class ReconciledClaim(BaseModel):
    """A candidate claim after the reconciliation step."""

    claim: str = Field(..., description=(
        "The canonical sentence. Where readers phrased one proposition differently, the most "
        "precise phrasing, grounded in their evidence."))
    panel: str | None = Field(None, description=(
        "As for a reader. Where readers disagree, the caption reader's panel."))
    claim_type: ClaimType = Field(..., description="See the vocabulary.")
    role: Role = Field(..., description="See the vocabulary.")
    addresses: str | None = Field(None, description=(
        "For a hypothesis or an alternative explanation, the research question it answers, as "
        "the paper states it or in one sentence; null for every other role."))
    confidence: ReconciledConfidence = Field(..., description=(
        "A fact about agreement: single-source for one reader, high for several who agree, "
        "contested for several who disagree."))
    sources: list[AgentName] = Field(..., description=(
        "The readers that surfaced this claim: results, caption, structure; reviewer for a "
        "claim the review pass added."))
    evidence_by_agent: dict[AgentName, str] = Field(default_factory=dict, description=(
        "For each reader in sources, the verbatim quote it gave."))
    span_by_agent: dict[AgentName, str] = Field(default_factory=dict, description=(
        "For each reader in sources that cited one, the span id its evidence quote came from."))
    evidence_verified: dict[str, bool] = Field(default_factory=dict, description=(
        "Filled by the runner. Leave null."))
    evidence_verified_against: dict[str, str] = Field(default_factory=dict, description=(
        "Filled by the runner: per reader, `span` or `slice`. Leave null."))
    notes: str | None = Field(None, description=(
        "What the readers disagreed about, or why a single-source claim deserves a second "
        "look. A review pass prefixes its notes with [reviewer]."))


class DraftClaimTable(BaseModel):
    """The output of Step 4 — what goes to the human review gate."""

    paper_slug: str = Field(..., description="As given in the input.")
    paper_doi: str = Field(..., description="As given in the input.")
    paper_title: str | None = Field(None, description="As given in the input.")
    # How the paper was read. The vocabulary is prepare.py's, because prepare is what
    # decides: JATS XML for an eLife DOI, PDF only when forced or for a paper off the CDN.
    #
    # This used to read Literal["pdf", "github-readme", "elife-api", "web-fetch"] = "pdf" —
    # a set that omitted `jats` entirely and defaulted to the one value that was usually
    # wrong. The draft therefore could not record a JATS intake even when that is what
    # happened, and said "pdf" whether or not anything had checked.
    #
    # None means the draft does not know, which is a different and honest answer. The
    # reconcile layer fills it in from prepared.json, so a draft built through the pipeline
    # always carries the real value; a draft built some other way says so.
    extraction_path: Literal["jats", "pdf"] | None = Field(None, description=(
        "Filled by the runner from prepared.json. Leave null."))
    extraction_path_note: str | None = None
    per_agent_counts: dict[AgentName, int] = Field(default_factory=dict, description=(
        "How many candidates each reader proposed."))
    # Which model produced this draft, at the top level so the pipeline's `by_from: model`
    # can read it out of the file. Every ledger entry used to record `scripts/pipeline.py
    # run` as the author of a claim table an LLM wrote.
    model: str | None = None
    claims: list[ReconciledClaim] = Field(..., description="Every surviving claim.")
    config_snapshot: dict = Field(
        default_factory=dict,
        description="Filled by the runner: models and prompt variant. Leave empty.",
    )
