"""Review endpoints — persona-grounded peer review of claim graphs.

Three endpoints:
  POST /review/suggest-panel  — editor suggests reviewers for a paper
  POST /review/run            — run the full review (panel → reviews → synthesis)
  POST /review/chat           — chat with a reviewer or editor (streaming)

The review operates on OXA claim nodes, uses HAAK personas, and produces
structured output (individual reviews, synthesis with claim-concern mapping).
"""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from typing import Optional

from anthropic import Anthropic, AnthropicVertex
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/review")

# Persona directory — HAAK repo on this server
PERSONA_DIR = Path(os.environ.get(
    "HAAK_PERSONA_DIR",
    os.path.expanduser("~/projects/haak/home/projects/scientopia/personas")
))

# Demo token whitelist (shared with extract endpoint)
DEMO_TOKENS = set(
    t.strip() for t in os.environ.get("ELIFE_EXTRACT_DEMO_TOKENS", "").split(",")
    if t.strip()
)

# Review instruction sets
INSTRUCTION_SETS = {
    "elife": {
        "reviewer": (
            "You are reviewing under eLife's publish-review-curate model. "
            "There is no accept/reject decision. Your job is to provide a public review "
            "that assesses the paper's strengths and weaknesses. Focus on: "
            "significance of the claims, strength of evidence, clarity of presentation, "
            "and reproducibility. Be constructive and specific. Address individual claims "
            "where possible."
        ),
        "editor": (
            "You are the editor under eLife's publish-review-curate model. "
            "You do not make accept/reject decisions. You synthesize reviewer assessments, "
            "identify convergent concerns, map concerns to specific claims, and produce "
            "an editorial assessment. Your assessment is public."
        ),
    },
    "standard": {
        "reviewer": (
            "You are reviewing this manuscript for a peer-reviewed journal. "
            "Assess: novelty, rigor, significance, clarity, reproducibility. "
            "Provide major and minor concerns. Be specific about which claims "
            "or results each concern addresses."
        ),
        "editor": (
            "You are the editor. Synthesize reviewer opinions, identify consensus "
            "and disagreements, map concerns to specific claims, and provide "
            "an overall assessment with a recommendation."
        ),
    },
    "methods-focused": {
        "reviewer": (
            "You are reviewing with a focus on methodological rigor. "
            "Assess: statistical validity, experimental design, power analysis, "
            "control conditions, reproducibility of computational methods. "
            "Identify which specific claims are affected by any methodological concerns."
        ),
        "editor": (
            "You are the editor with a methods focus. Prioritize methodological "
            "concerns in your synthesis. Map each concern to the claims it undermines."
        ),
    },
}


# ── Models ──────────────────────────────────────────────────────────────


class AuthInfo(BaseModel):
    api_key: str = ""
    demo_token: str = ""


class SuggestPanelRequest(AuthInfo):
    claims: list[dict]  # OXA claim nodes
    abstract: str = ""
    n_reviewers: int = 3


class RunReviewRequest(AuthInfo):
    claims: list[dict]
    abstract: str = ""
    paper_title: str = ""
    reviewers: list[dict]  # each: {slug, type: "personified"|"generic", name, ...}
    instructions: str = "elife"  # key into INSTRUCTION_SETS or raw text
    model: str = "claude-sonnet-4-6"
    editor_model: str = "claude-opus-4-8"


class ChatRequest(AuthInfo):
    role: str  # reviewer slug or "editor"
    messages: list[dict]  # [{role, content}, ...]
    context: dict  # persona, review text, focus concerns, instructions
    model: str = "claude-sonnet-4-6"


# ── Helpers ─────────────────────────────────────────────────────────────


def _get_client(auth: AuthInfo) -> Anthropic | AnthropicVertex:
    if auth.api_key:
        return Anthropic(api_key=auth.api_key)
    if not DEMO_TOKENS:
        raise ValueError("Vertex backend not configured")
    if auth.demo_token not in DEMO_TOKENS:
        raise ValueError("Invalid demo token")
    return AnthropicVertex(
        region=os.environ.get("VERTEX_REGION", "europe-west1"),
        project_id=os.environ.get("VERTEX_PROJECT_ID", "cr-mainen"),
    )


def _load_persona(slug: str) -> dict:
    """Load a persona from the HAAK persona library."""
    persona_path = PERSONA_DIR / slug / "persona.md"
    if not persona_path.exists():
        # Try fuzzy match
        candidates = list(PERSONA_DIR.glob(f"*{slug}*"))
        if candidates:
            persona_path = candidates[0] / "persona.md"
    if not persona_path.exists():
        return {"name": slug, "text": "", "field": "", "seniority": "", "gender": "", "location": ""}

    text = persona_path.read_text()
    # Parse frontmatter
    meta = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip("'\"")
            text = parts[2].strip()

    # Extract table row for seniority/gender/location
    career = ""
    m = re.search(r"Career stage\s*\|\s*(.+?)(?:\s*\||\s*$)", text, re.MULTILINE)
    if m:
        career = m.group(1).strip()

    return {
        "name": meta.get("name", slug),
        "field": meta.get("field", ""),
        "seniority": career.split("(")[0].strip() if career else "",
        "institution": meta.get("institution", ""),
        "text": text,
    }


def _list_personas() -> list[dict]:
    """List all available personas with metadata.

    Handles two formats:
      - Directory with persona.md inside (newer format)
      - Standalone .md file (older format)
    """
    personas = []
    if not PERSONA_DIR.exists():
        return personas
    for entry in sorted(PERSONA_DIR.iterdir()):
        if entry.name.startswith("."):
            continue
        if entry.is_dir() and (entry / "persona.md").exists():
            p = _load_persona(entry.name)
        elif entry.is_file() and entry.suffix == ".md":
            p = _load_persona_from_file(entry)
        else:
            continue
        if p.get("name"):
            p["type"] = "personified"
            p.pop("text", None)
            personas.append(p)
    return personas


def _load_persona_from_file(path: Path) -> dict:
    """Load a persona from a standalone .md file (older format)."""
    text = path.read_text()
    meta = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip("'\"")
            body = parts[2].strip()

    name = meta.get("name", path.stem.split("-", 3)[-1].replace("-", " ").title() if "-" in path.stem else path.stem)
    return {
        "slug": path.stem,
        "name": name,
        "field": meta.get("field", ""),
        "seniority": meta.get("career_stage", ""),
        "institution": meta.get("institution", ""),
        "text": body,
    }


def _get_instructions(key: str) -> dict:
    """Get reviewer and editor instructions by key or as raw text."""
    if key in INSTRUCTION_SETS:
        return INSTRUCTION_SETS[key]
    # Treat as custom raw text — use same text for both
    return {"reviewer": key, "editor": key}


def _claims_context(claims: list[dict], abstract: str = "") -> str:
    """Format claims as context for reviewers."""
    parts = []
    if abstract:
        parts.append(f"ABSTRACT:\n{abstract}\n")
    parts.append("CLAIMS:")
    for c in claims:
        role = c.get("role", "?")
        text = ""
        for child in c.get("children", []):
            if child.get("type") == "Text":
                text = child.get("value", "")
        panel = ", ".join(c.get("panel", []))
        rels = len(c.get("relations", []))
        parts.append(f"\n[{role}] {c.get('identifier', '?')}")
        if panel:
            parts.append(f"  panel: {panel}")
        parts.append(f"  {text}")
        if rels:
            parts.append(f"  ({rels} relations)")
    return "\n".join(parts)


# ── Endpoints ───────────────────────────────────────────────────────────


@router.get("/personas")
def list_personas(demo_token: str = ""):
    """List available reviewer personas. Personified only with valid demo token."""
    show_personified = demo_token and demo_token in DEMO_TOKENS
    personas = _list_personas() if show_personified else []
    return {
        "personified": [p for p in personas if p.get("type") == "personified"],
        "generic": [
            {"slug": "stats-reviewer", "name": "Statistical methods reviewer",
             "type": "generic", "field": "Experimental design, power analysis, multiple comparisons",
             "focus": "Does the analysis support the claims?"},
            {"slug": "replication-skeptic", "name": "Replication skeptic",
             "type": "generic", "field": "Reproducibility, effect sizes, pre-registration",
             "focus": "Would this replicate?"},
            {"slug": "domain-newcomer", "name": "Domain newcomer",
             "type": "generic", "field": "Accessibility, clarity, jargon",
             "focus": "Can a non-specialist follow the argument?"},
            {"slug": "theoretical-integrator", "name": "Theoretical integrator",
             "type": "generic", "field": "Cross-field connections, broader significance",
             "focus": "How does this change the field?"},
            {"slug": "methods-specialist", "name": "Computational methods specialist",
             "type": "generic", "field": "Code quality, numerical methods, model validation",
             "focus": "Are the computational methods sound?"},
        ],
        "total": len(personas) + 5,
    }


@router.post("/suggest-panel")
def suggest_panel(req: SuggestPanelRequest):
    """Editor suggests a reviewer panel based on the paper's claims."""
    client = _get_client(req)
    claims_text = _claims_context(req.claims, req.abstract)
    personas = _list_personas()
    persona_list = "\n".join(
        f"- {p['slug']}: {p['name']} — {p['field']}"
        for p in personas[:50]  # cap to avoid token overflow
    )

    prompt = f"""You are an editor assembling a reviewer panel for a scientific paper.

The paper has {len(req.claims)} claims. Here they are:

{claims_text}

Available reviewers (first 50 of {len(personas)}):
{persona_list}

Select {req.n_reviewers} reviewers whose expertise best covers this paper's claims. For each:
1. Name the reviewer (by slug)
2. Explain why their expertise is relevant to specific claims
3. Note any potential biases

Also suggest 1-2 generic reviewer roles that would complement the panel.

Return JSON:
{{
  "panel": [
    {{"slug": "...", "reason": "...", "claims_covered": ["claim-id-1", "..."]}},
    ...
  ],
  "generic_suggestions": [
    {{"role": "...", "reason": "..."}},
    ...
  ],
  "coverage_gaps": ["..."]
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    # Parse JSON from response
    text = response.content[0].text
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    return {"raw": text}


@router.post("/run")
async def run_review(req: RunReviewRequest):
    """Run the full review pipeline — returns SSE stream."""

    def generate():
        try:
            client = _get_client(req)
            instructions = _get_instructions(req.instructions)
            claims_text = _claims_context(req.claims, req.abstract)

            reviews = []

            # Phase 1: Individual reviews
            for i, reviewer in enumerate(req.reviewers):
                slug = reviewer.get("slug", f"reviewer-{i}")
                name = reviewer.get("name", slug)
                rtype = reviewer.get("type", "generic")

                yield f"data: {json.dumps({'step': 'review', 'message': f'Reviewer {i+1}/{len(req.reviewers)}: {name} reading claims and writing review...'})}\n\n"

                # Build system prompt
                if rtype == "personified":
                    persona = _load_persona(slug)
                    system = (
                        f"You are {persona['name']}, reviewing a scientific manuscript. "
                        f"Stay in character. Draw on your expertise and perspective.\n\n"
                        f"REVIEW INSTRUCTIONS:\n{instructions['reviewer']}\n\n"
                        f"YOUR PERSONA:\n{persona['text'][:3000]}"
                    )
                else:
                    focus = reviewer.get("focus", reviewer.get("field", ""))
                    system = (
                        f"You are a {name}. {focus}\n\n"
                        f"REVIEW INSTRUCTIONS:\n{instructions['reviewer']}"
                    )

                user_msg = (
                    f"Please review this paper. Title: {req.paper_title}\n\n"
                    f"{claims_text}\n\n"
                    f"Provide your review with:\n"
                    f"1. Overall assessment\n"
                    f"2. Major concerns (reference specific claim identifiers)\n"
                    f"3. Minor concerns\n"
                    f"4. Strengths\n"
                    f"5. Private recommendation to editor"
                )

                response = client.messages.create(
                    model=req.model,
                    max_tokens=8192,
                    system=system,
                    messages=[{"role": "user", "content": user_msg}],
                )
                review_text = response.content[0].text

                reviews.append({
                    "slug": slug,
                    "name": name,
                    "type": rtype,
                    "review": review_text,
                })

                # Count words as a rough quality indicator
                word_count = len(review_text.split())
                yield f"data: {json.dumps({'step': 'review', 'message': f'Reviewer {i+1}/{len(req.reviewers)}: {name} — done ({word_count} words)'})}\n\n"

            # Phase 2: Editor synthesis
            yield f"data: {json.dumps({'step': 'synthesis', 'message': f'Editor reading {len(reviews)} reviews and synthesizing...'})}\n\n"

            all_reviews = "\n\n---\n\n".join(
                f"REVIEWER: {r['name']}\n\n{r['review']}" for r in reviews
            )

            editor_system = (
                f"You are the editor. {instructions['editor']}\n\n"
                f"You have received {len(reviews)} reviews for this paper."
            )

            editor_msg = (
                f"Paper: {req.paper_title}\n\n"
                f"CLAIMS:\n{claims_text}\n\n"
                f"REVIEWS:\n{all_reviews}\n\n"
                f"Produce an editorial synthesis with:\n"
                f"1. Assessment summary (significance, evidence strength)\n"
                f"2. Concern inventory — for each concern:\n"
                f"   - Title\n"
                f"   - Severity (critical/major/minor)\n"
                f"   - Which reviewers raised it\n"
                f"   - Which claim identifiers it affects\n"
                f"   - Description\n"
                f"3. Strengths consensus\n"
                f"4. Overall editorial assessment\n\n"
                f"Return as JSON:\n"
                f'{{"assessment": "...", "concerns": [{{"id": 1, "title": "...", '
                f'"severity": "major", "reviewers": ["name"], '
                f'"claims_affected": ["claim-id"], "description": "..."}}], '
                f'"strengths": ["..."], "editorial_assessment": "..."}}'
            )

            response = client.messages.create(
                model=req.editor_model,
                max_tokens=8192,
                system=editor_system,
                messages=[{"role": "user", "content": editor_msg}],
            )
            synthesis_text = response.content[0].text

            yield f"data: {json.dumps({'step': 'synthesis', 'message': 'Editor synthesis complete — parsing concerns...'})}\n\n"

            # Try to parse JSON
            synthesis = {}
            m = re.search(r"\{.*\}", synthesis_text, re.DOTALL)
            if m:
                try:
                    synthesis = json.loads(m.group(0))
                except json.JSONDecodeError:
                    synthesis = {"raw": synthesis_text}
            else:
                synthesis = {"raw": synthesis_text}

            result = {
                "reviews": reviews,
                "synthesis": synthesis,
                "paper_title": req.paper_title,
                "n_claims": len(req.claims),
                "instructions": req.instructions,
            }

            n_concerns = len(synthesis.get("concerns", []))
            msg = f"Review complete: {len(reviews)} reviewers, {n_concerns} concerns"
            yield f"data: {json.dumps({'step': 'done', 'message': msg, 'result': result})}\n\n"

        except Exception as e:
            logger.exception("Review failed")
            yield f"data: {json.dumps({'step': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/chat")
async def chat(req: ChatRequest):
    """Chat with a reviewer or editor — streaming response."""

    def generate():
        try:
            client = _get_client(req)

            # Build system prompt from context
            ctx = req.context
            if req.role == "editor":
                system = (
                    f"You are the editor. Be direct, fair, constructive. "
                    f"Help the author understand priorities and craft responses.\n\n"
                    f"{ctx.get('instructions', '')}\n\n"
                    f"YOUR SYNTHESIS:\n{ctx.get('synthesis', '')}\n\n"
                    f"YOUR ASSESSMENT:\n{ctx.get('assessment', '')}"
                )
            else:
                persona_text = ctx.get("persona", "")
                review_text = ctx.get("review", "")
                system = (
                    f"You are {ctx.get('name', req.role)}, reviewing a manuscript. "
                    f"Stay in character. Be direct, defend your positions, "
                    f"acknowledge good points, reconsider if persuaded.\n\n"
                    f"{ctx.get('instructions', '')}\n\n"
                    f"YOUR PERSONA:\n{persona_text[:2000]}\n\n"
                    f"YOUR REVIEW:\n{review_text}"
                )

            # Focus concerns if provided
            if ctx.get("focus_concerns"):
                concerns_text = "\n".join(
                    f"- {c.get('title', '?')}: {c.get('description', '')}"
                    for c in ctx["focus_concerns"]
                )
                system += f"\n\nFOCUS ON THESE CONCERNS:\n{concerns_text}"

            with client.messages.stream(
                model=req.model,
                max_tokens=2048,
                system=system,
                messages=[{"role": m["role"], "content": m["content"]}
                          for m in req.messages],
            ) as stream:
                for text in stream.text_stream:
                    yield f"data: {json.dumps({'token': text})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            logger.exception("Chat failed")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
