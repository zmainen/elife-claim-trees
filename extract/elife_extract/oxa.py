"""OXA Claim schema — Pydantic models for structured scientific claims.

Extends the upstream oxa-types package with Claim, ClaimGraph, and
supporting types. These models are the local definition used until the
Claim RFC is accepted into the OXA specification, at which point they
are replaced by the generated models from oxa-types.

See: home/collabs/elife/claim-trees/reference/oxa-rfc-claim/
See: home/collabs/mira/oxa-adoption/spec.md
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# Re-export upstream types we build on.
from oxa_types import Heading, Paragraph, Strong, Text
from oxa_types import Document as _UpstreamDocument


# ── Additional OXA inline types ──────────────────────────────────────────

class Emphasis(BaseModel):
    """Emphasized content (typically italic)."""
    model_config = ConfigDict(strict=True)
    type: Literal["Emphasis"] = "Emphasis"
    id: str | None = None
    children: list[Inline] = Field(description="Inline content to emphasize.")


class InlineMath(BaseModel):
    """Inline LaTeX math."""
    model_config = ConfigDict(strict=True)
    type: Literal["InlineMath"] = "InlineMath"
    id: str | None = None
    value: str = Field(description="LaTeX math expression.")


class InlineCode(BaseModel):
    """Inline code span."""
    model_config = ConfigDict(strict=True)
    type: Literal["InlineCode"] = "InlineCode"
    id: str | None = None
    value: str
    language: str | None = None


class Cite(BaseModel):
    """Citation to a Reference node."""
    model_config = ConfigDict(strict=True)
    type: Literal["Cite"] = "Cite"
    id: str | None = None
    xref: str = Field(description="Identifier of the target Reference.")
    intent: str | None = Field(default=None, description="CiTO intent IRI.")
    display: Literal["author", "date", "full"] | None = None
    children: list[Inline] | None = None


# Extended inline union (superset of oxa-types Inline).
Inline = Text | Strong | Emphasis | InlineMath | InlineCode | Cite


# ── Additional OXA block types ───────────────────────────────────────────

class Reference(BaseModel):
    """Bibliographic record (CSL-JSON)."""
    model_config = ConfigDict(strict=True)
    type: Literal["Reference"] = "Reference"
    id: str = Field(description="Citation key (must be unique in document).")
    csl: dict[str, Any] = Field(description="CSL-JSON item object.")
    children: list[Inline] | None = None


class Code(BaseModel):
    """Code block."""
    model_config = ConfigDict(strict=True)
    type: Literal["Code"] = "Code"
    id: str | None = None
    value: str
    language: str | None = None


# ── Source span (from Mira's mirax overlay) ──────────────────────────────

class SourceSpan(BaseModel):
    """Tracks where a claim was extracted from in the source document.

    Follows Mira's SourceSpan model with OXA-compatible naming.
    """
    quote: str = Field(description="Verbatim text from the source document.")
    docId: str | None = Field(default=None, description="Source document identifier.")
    charStart: int | None = Field(default=None, description="Character offset (start).")
    charEnd: int | None = Field(default=None, description="Character offset (end).")
    page: int | None = Field(default=None, description="Page number in source PDF.")
    bbox: list[float] | None = Field(
        default=None, description="Bounding box [left, top, right, bottom]."
    )
    grounding: Literal["verified", "fuzzy", "unverified"] = "unverified"


# ── Claim types (OXA RFC) ────────────────────────────────────────────────

ClaimRole = Literal[
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

EpistemicStrength = Literal["strong", "moderate", "suggestive", "speculative"]


class ClaimRelation(BaseModel):
    """Typed edge to another claim, using CiTO vocabulary."""
    xref: str = Field(description="Target claim identifier.")
    relationType: str = Field(description="CiTO IRI or claimrel extension IRI.")


class ClaimMetadata(BaseModel):
    """Claim-level metadata: provenance, source span, auxiliary fields."""
    model_config = ConfigDict(extra="allow")

    # Provenance
    lifecycle: Literal[
        "designed", "pilot", "supported", "refuted",
        "inconclusive", "extracted", "published",
    ] | None = None
    confidence: Literal["high", "contested", "single-source"] | None = None
    sources: list[str] | None = Field(
        default=None, description="Extraction agents that surfaced this claim."
    )
    extractionPath: str | None = None

    # Source grounding
    sourceSpan: SourceSpan | None = None

    # Display variants
    displayClaim: str | None = Field(
        default=None, description="Human-friendly rendering (one sentence)."
    )
    shortClaim: str | None = Field(
        default=None, description="Ultra-short rendering (< 80 chars)."
    )

    # Identity
    uuid: str | None = None
    doi: str | None = None
    concepts: list[str] | None = None


class Claim(BaseModel):
    """A scientific claim — an independently addressable proposition.

    Part of a paper's argument structure. Carries a role (hypothesis,
    empirical result, prediction, etc.), optional figure-panel anchors,
    epistemic strength, and typed relations to other claims.

    OXA RFC: home/collabs/elife/claim-trees/reference/oxa-rfc-claim/
    """
    model_config = ConfigDict(strict=True)

    type: Literal["Claim"] = "Claim"
    id: str | None = None
    classes: list[str] | None = None
    data: dict[str, Any] | None = None

    # Claim-specific
    identifier: str = Field(description="Unique slug for cross-referencing.")
    role: ClaimRole
    panel: list[str] | None = Field(
        default=None, description="Figure panel IDs this claim is grounded in."
    )
    epistemicStrength: EpistemicStrength | None = None
    relations: list[ClaimRelation] | None = None
    metadata: ClaimMetadata | None = None

    # Content — the proposition text as inline nodes.
    children: list[Inline] = Field(
        description="The claim text as OXA inline content."
    )


class ClaimGraph(BaseModel):
    """Container for a document's claim structure.

    Groups all claims in one navigable unit. Optional — claims can also
    appear inline within the document body.
    """
    model_config = ConfigDict(strict=True)

    type: Literal["ClaimGraph"] = "ClaimGraph"
    id: str | None = None
    identifier: str | None = None
    metadata: dict[str, Any] | None = None
    children: list[Claim] = Field(description="The claims in this graph.")


# ── Review annotation types (structured peer review) ─────────────────────
#
# Vocabulary for claims-anchored peer review. A reviewer's assessment becomes
# typed, addressable annotations: each observation is a ReviewComment anchored
# to the Claim it evaluates (claimXref) and the manuscript passage it cites
# (SourceSpan — reusing the extraction-grounding machinery) and/or a figure
# panel. The eLife two-axis assessment is a ReviewVerdict (with optional
# per-claim verdicts); concrete fixes are ReviewSuggestions. One reviewer's
# complete review is a ReviewAnnotationSet.
#
# Spec:        home/collabs/mira/oxa-adoption/review-annotations-spec.md  (hetu)
# Consumed by: home/collabs/mira/oxa-adoption/structured-review-spec.md   (mimamsa)

# eLife assessment axes (platform/styles/formal-review.md, reviewer mandate).
Significance = Literal[
    "landmark", "fundamental", "important", "valuable", "useful",
]
StrengthOfEvidence = Literal[
    "exceptional", "compelling", "convincing", "solid", "incomplete", "inadequate",
]

# Editorial recommendation. Distinct from the assessment axes: the axes
# describe the work, the recommendation prescribes an action. (Design-review
# support / support-with-reservations / oppose map to accept / minor / major.)
ReviewRecommendation = Literal[
    "accept", "minor-revision", "major-revision", "reject",
]

# Polarity and severity are orthogonal: a strength carries no severity, a
# weakness does, a neutral comment is a question or a remark.
ReviewPolarity = Literal["strength", "weakness", "neutral"]
ReviewSeverity = Literal["critical", "major", "minor"]

# Coarse concern dimension — what KIND of concern (aligned with the eLife axes
# and the standard dimensions of methodological critique).
ReviewCategory = Literal[
    "significance", "evidence", "methodology", "statistics", "controls",
    "interpretation", "scope", "reproducibility", "clarity", "literature",
    "ethics",
]

# Fine-grained failure mode — names the specific inferential breakdown and
# predicts what resolves it. Optional refinement of category; absent unless
# the reviewer diagnoses a specific failure (the argument-failure modes).
ReviewDiagnosis = Literal[
    "interpretive-overreach",     # conclusion outruns the evidence
    "underpowered-null",          # absence of evidence read as evidence of absence
    "confound",                   # alternative cause not excluded
    "not-uniquely-diagnostic",    # result consistent with rival hypotheses
    "missing-control",            # decisive control absent
    "missing-analysis",           # decisive analysis not run
    "scope-overreach",            # conclusion exceeds the tested domain
    "statistical-artifact",       # multiplicity / power / inference error
    "circular-reasoning",         # assumes what it sets out to show
    "unsupported-mechanism",      # mechanistic claim without mechanistic evidence
]

# Per-claim verdict values — exactly the verdicts the prose reviews already use.
ClaimJustification = Literal[
    "well-supported", "supported-with-caveats",
    "partially-supported", "not-supported", "overstated",
]

# Lifecycle of a review annotation — orthogonal to the claim lifecycle.
ReviewStatus = Literal["draft", "submitted", "addressed", "withdrawn"]

# Kind of fix a suggestion proposes.
ReviewActionType = Literal[
    "revise-text",      # concrete wording change (originalText -> proposedText)
    "add-analysis",     # run a specific analysis
    "add-experiment",   # run a follow-up experiment (maps to Mira Request)
    "add-control",      # add a missing control
    "reframe",          # restructure the argument or claim
    "qualify",          # add a scope condition or caveat
    "remove",           # cut an overclaim
]


class Reviewer(BaseModel):
    """The authoring party. Persona-grounded in HaaK; an Agent (ORCID/DID) in Mira."""
    model_config = ConfigDict(strict=True)
    identifier: str = Field(description="Persona slug or agent id.")
    did: str | None = Field(default=None, description="AT Protocol DID (PDS owner).")
    orcid: str | None = None
    persona: str | None = Field(default=None, description="Grounding persona file.")
    role: Literal["reviewer", "editor"] = "reviewer"


class ReviewProvenance(BaseModel):
    """How an AI-generated review annotation was produced (mirrors Mira Provenance)."""
    model_config = ConfigDict(extra="allow")
    runId: str | None = None
    model: str | None = None
    promptId: str | None = None
    backend: str | None = None
    confidence: Literal["high", "moderate", "low"] | None = None


class ReviewAnchor(BaseModel):
    """Where a comment attaches — what makes it addressable.

    Reuses SourceSpan (quote + char offsets + grounding), so review anchors get
    the same exact / fuzzy / unverified grounding verification the extraction
    pipeline implements. The AT Protocol byte-range facet (byteStart / byteEnd)
    and strong-ref (uri / cid to the immutable Claim record) are DERIVED from
    this at publication time, not stored — char offsets ground review->source,
    byte offsets are the wire format. An anchor is well-formed if at least one
    of claimXref / sourceSpan / panel is present.
    """
    model_config = ConfigDict(strict=True)
    claimXref: str | None = Field(default=None, description="Identifier of the Claim evaluated.")
    sourceSpan: SourceSpan | None = Field(default=None, description="Manuscript passage cited.")
    panel: list[str] | None = Field(default=None, description="Figure panel(s), e.g. ['fig4i'].")


class ReviewSuggestion(BaseModel):
    """The 'exit': a structured, actionable fix for a weakness.

    A weakness without an exit is a complaint; a weakness with an exit is a
    recommendation. Carries a priority, an action type, the recommendation prose
    (children), and — for the gold standard — a decisive-outcome framing. For
    concrete wording edits, originalText / proposedText hold the replacement.
    Usually nested in its ReviewComment; may stand alone via addressesComment.
    """
    model_config = ConfigDict(strict=True)
    type: Literal["ReviewSuggestion"] = "ReviewSuggestion"
    id: str | None = None
    identifier: str | None = None
    priority: Literal["essential", "important", "optional"]
    action: ReviewActionType
    children: list[Inline] = Field(description="What to do — the recommendation.")
    decisiveOutcome: list[Inline] | None = Field(
        default=None, description="'If X then Y; if Z then W' framing."
    )
    originalText: str | None = Field(default=None, description="For action=revise-text.")
    proposedText: str | None = Field(default=None, description="For action=revise-text.")
    rationale: list[Inline] | None = None
    addressesComment: str | None = Field(
        default=None, description="xref to the ReviewComment this resolves (if standalone)."
    )


class ReviewCommentMetadata(BaseModel):
    """Annotation-level metadata: status, provenance, auxiliary fields."""
    model_config = ConfigDict(extra="allow")
    status: ReviewStatus = "submitted"
    provenance: ReviewProvenance | None = None


class ReviewComment(BaseModel):
    """A single evaluative observation about one claim (or the manuscript).

    The atomic unit of review. polarity and severity are orthogonal (a strength
    has no severity). category is the coarse concern dimension; diagnosis names
    the specific failure mode (optional). The anchor makes it addressable. The
    body (children) is the argument; grounds optionally separates the Toulmin
    warrant. relations let a critique participate in the claim graph as a
    second-order edge (e.g. cito:disagreesWith). suggestion carries the exit.
    """
    model_config = ConfigDict(strict=True)
    type: Literal["ReviewComment"] = "ReviewComment"
    id: str | None = None
    identifier: str = Field(description="Unique within the review.")
    polarity: ReviewPolarity
    severity: ReviewSeverity | None = Field(
        default=None, description="Weaknesses only; null for strengths / neutral."
    )
    category: ReviewCategory
    diagnosis: ReviewDiagnosis | None = Field(
        default=None, description="Specific failure mode (refinement of category)."
    )
    anchor: ReviewAnchor
    children: list[Inline] = Field(description="The critique — diagnosis + argument.")
    grounds: list[Inline] | None = Field(
        default=None, description="Why the reviewer holds it — the Toulmin warrant."
    )
    relations: list[ClaimRelation] | None = Field(
        default=None, description="Typed edges into the claim graph (e.g. cito:disagreesWith)."
    )
    suggestion: ReviewSuggestion | None = Field(default=None, description="The exit.")
    metadata: ReviewCommentMetadata | None = None


class ClaimVerdict(BaseModel):
    """Per-claim assessment — the structured 'Are the Conclusions Justified?' line."""
    model_config = ConfigDict(strict=True)
    claimXref: str
    justified: ClaimJustification
    commentXrefs: list[str] = Field(
        default_factory=list, description="ReviewComments backing this verdict."
    )


class ReviewVerdict(BaseModel):
    """The review's top-level assessment, with optional per-claim verdicts.

    The eLife two-axis assessment (significance x strengthOfEvidence), each of
    which must be justified in the prose (children), plus an editorial
    recommendation and the per-claim breakdown that makes coverage measurable.
    """
    model_config = ConfigDict(strict=True)
    type: Literal["ReviewVerdict"] = "ReviewVerdict"
    id: str | None = None
    identifier: str | None = None
    significance: Significance | None = None
    strengthOfEvidence: StrengthOfEvidence | None = None
    recommendation: ReviewRecommendation | None = None
    perClaim: list[ClaimVerdict] | None = None
    children: list[Inline] = Field(description="The assessment prose (2-4 sentences).")
    commentXrefs: list[str] | None = Field(
        default=None, description="Top-level constituent comments (manuscript-wide)."
    )
    metadata: ReviewCommentMetadata | None = None


class ReviewAnnotationSet(BaseModel):
    """One reviewer's complete review of one manuscript.

    The review analogue of ClaimGraph: a verdict plus the flat list of comments
    (each optionally nesting its suggestion). The editor's synthesis is itself a
    ReviewAnnotationSet with reviewer.role='editor'. Emitted as
    {lastname}_review.oxa.json beside the manuscript; the prose review markdown
    is a regenerable view of it.
    """
    model_config = ConfigDict(strict=True)
    type: Literal["ReviewAnnotationSet"] = "ReviewAnnotationSet"
    id: str | None = None
    identifier: str = Field(description="Unique review id, e.g. 'sautory-2026-niv'.")
    reviewer: Reviewer
    manuscript: str | None = Field(
        default=None, description="Identifier of the reviewed Document / manuscript."
    )
    verdict: ReviewVerdict
    comments: list[ReviewComment] = Field(
        default_factory=list, description="The review's comments (each may nest a suggestion)."
    )
    metadata: dict[str, Any] | None = None


# Extended block union (superset of oxa-types Block).
Block = Heading | Paragraph | Code | Reference | ClaimGraph | Claim | ReviewAnnotationSet


class Document(BaseModel):
    """OXA Document with extended Block union supporting Claim types.

    Mirrors oxa_types.Document but accepts ClaimGraph and Claim as children.
    When the Claim RFC lands upstream, this is replaced by the generated
    Document from oxa-types.
    """
    model_config = ConfigDict(strict=True)

    type: Literal["Document"] = "Document"
    id: str | None = Field(default=None, description="Unique identifier.")
    classes: list[str] | None = None
    data: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = Field(
        default=None, description="Arbitrary document metadata."
    )
    title: list[Inline] | None = Field(
        default=None, description="Document title as inline content."
    )
    children: list[Block] = Field(description="Block content of the document.")


# ── Edge vocabulary ──────────────────────────────────────────────────────

EDGE_MAP: dict[str, str] = {
    # CiTO exact matches
    "supports": "cito:supports",
    "extends": "cito:extends",
    "qualifies": "cito:qualifies",
    # CiTO close matches
    "derived-from": "cito:citesAsSourceDocument",
    "enables-method": "cito:usesMethodIn",
    "dissociates-with": "cito:disagreesWith",
    # Claim-relations extensions (CiTO subproperties)
    "requires": "claimrel:requires",
    "tests": "claimrel:tests",
    "entails": "claimrel:entails",
    "interprets": "claimrel:interprets",
    "scopes": "claimrel:scopes",
    "rules-out": "claimrel:rulesOut",
    "replicates": "claimrel:replicates",
    "contradicts": "claimrel:contradicts",
}


# ── Builder helpers ──────────────────────────────────────────────────────

def text_node(value: str) -> Text:
    """Convenience: create an OXA Text node."""
    return Text(type="Text", value=value)


def claim_from_reconciled(
    claim_text: str,
    slug: str,
    role: str,
    panel: str | None = None,
    epistemic: str | None = None,
    confidence: str | None = None,
    sources: list[str] | None = None,
    evidence_by_agent: dict[str, str] | None = None,
    uuid_str: str | None = None,
) -> Claim:
    """Build a Claim node from extraction-pipeline fields.

    Maps the elife-extract vocabulary to OXA types.
    """
    panels = None
    if panel:
        panels = [p.strip() for p in panel.split(",")]

    meta = ClaimMetadata(
        lifecycle="extracted",
        confidence=confidence,
        sources=sources,
        uuid=uuid_str,
    )

    # Build source span from the best available evidence quote
    if evidence_by_agent:
        best_quote = next(iter(evidence_by_agent.values()), None)
        if best_quote:
            meta.sourceSpan = SourceSpan(quote=best_quote)

    return Claim(
        identifier=slug,
        role=role,
        panel=panels,
        epistemicStrength=epistemic if epistemic in (
            "strong", "moderate", "suggestive", "speculative"
        ) else None,
        children=[text_node(claim_text)],
        metadata=meta,
    )


def build_document(
    paper_slug: str,
    paper_doi: str,
    paper_title: str | None,
    claims: list[Claim],
    authors: list[str] | None = None,
) -> Document:
    """Build an OXA Document containing a ClaimGraph."""
    meta: dict[str, Any] = {"doi": paper_doi}
    if paper_title:
        meta["title"] = paper_title
    if authors:
        meta["authors"] = authors

    title_nodes = None
    if paper_title:
        title_nodes = [text_node(paper_title)]

    graph = ClaimGraph(
        identifier=f"{paper_slug}-claims",
        children=claims,
    )

    return Document(
        metadata=meta,
        title=title_nodes,
        children=[graph],  # type: ignore[arg-type]  # extended Block union
    )


# ── Source-span grounding ─────────────────────────────────────────────────


def ground_source_span(
    span: SourceSpan,
    source_text: str,
    fuzzy_threshold: float = 0.92,
) -> SourceSpan:
    """Verify a source span's quote against the source text.

    Exact substring match → verified (with char offsets).
    Fuzzy match ≥ threshold → fuzzy (with approximate offsets).
    No match → unverified (offsets left as None).
    """
    import re as _re

    quote = span.quote
    if not quote or not source_text:
        return span

    # Normalize whitespace for matching (sources have newlines mid-sentence)
    norm_source = _re.sub(r"\s+", " ", source_text)
    norm_quote = _re.sub(r"\s+", " ", quote)

    # Exact match (on whitespace-normalized text)
    idx = norm_source.find(norm_quote)
    if idx >= 0:
        span.grounding = "verified"
        span.charStart = idx
        span.charEnd = idx + len(norm_quote)
        return span

    # Fuzzy match — slide a window of quote length across the normalized source
    try:
        from rapidfuzz import fuzz
    except ImportError:
        return span

    best_score = 0.0
    best_start = 0
    window = len(norm_quote)
    step = max(1, window // 4)

    for start in range(0, len(norm_source) - window + 1, step):
        candidate = norm_source[start : start + window]
        score = fuzz.ratio(norm_quote, candidate) / 100.0
        if score > best_score:
            best_score = score
            best_start = start

    if best_score >= fuzzy_threshold:
        span.grounding = "fuzzy"
        span.charStart = best_start
        span.charEnd = best_start + window

    return span


def ground_claims_in_document(
    claims: list[Claim],
    source_text: str,
    fuzzy_threshold: float = 0.92,
) -> list[Claim]:
    """Ground all claims' source spans against the source text."""
    for claim in claims:
        if claim.metadata and claim.metadata.sourceSpan:
            claim.metadata.sourceSpan = ground_source_span(
                claim.metadata.sourceSpan, source_text, fuzzy_threshold
            )
    return claims


# Rebuild forward refs.
Emphasis.model_rebuild()
Cite.model_rebuild()
Claim.model_rebuild()
ClaimGraph.model_rebuild()
ReviewSuggestion.model_rebuild()
ReviewComment.model_rebuild()
ReviewVerdict.model_rebuild()
ReviewAnnotationSet.model_rebuild()


__all__ = [
    # OXA upstream re-exports
    "Document", "Heading", "Paragraph", "Strong", "Text",
    # Extended types
    "Emphasis", "InlineMath", "InlineCode", "Cite", "Reference", "Code",
    # Claim types (OXA RFC)
    "Claim", "ClaimGraph", "ClaimRelation", "ClaimMetadata",
    "ClaimRole", "EpistemicStrength",
    # Source grounding (Mira-derived)
    "SourceSpan",
    # Review annotation types (structured peer review)
    "Significance", "StrengthOfEvidence", "ReviewRecommendation",
    "ReviewPolarity", "ReviewSeverity", "ReviewCategory", "ReviewDiagnosis",
    "ClaimJustification", "ReviewStatus", "ReviewActionType",
    "Reviewer", "ReviewProvenance", "ReviewAnchor", "ReviewSuggestion",
    "ReviewComment", "ReviewCommentMetadata", "ClaimVerdict", "ReviewVerdict",
    "ReviewAnnotationSet",
    # Unions
    "Block", "Inline",
    # Vocabulary
    "EDGE_MAP",
    # Builders
    "text_node", "claim_from_reconciled", "build_document",
    # Grounding
    "ground_source_span", "ground_claims_in_document",
]
