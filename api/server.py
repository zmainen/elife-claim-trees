"""FastAPI backend for the web-based paper ingester.

Receives a DOI + Anthropic API key, runs the full extraction pipeline,
and streams progress via SSE. Returns OXA-native claim graph JSON.

The API key is held in memory for the duration of the request and
discarded immediately after. Never logged, never stored.

Usage:
  uvicorn server:app --host 0.0.0.0 --port 8080
"""

from __future__ import annotations

import json
import logging
import os
import queue
import re
import sys
import threading
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Add the extract package to the path — works from HAAK repo or standalone
API_DIR = Path(__file__).resolve().parent
for candidate in [
    API_DIR.parent / "extract",                                         # published repo (extract/ at root)
    API_DIR / "elife_extract",                                          # standalone deploy
    API_DIR.parent / "home/collabs/elife/claim-trees/extract",         # HAAK repo
]:
    if (candidate / "elife_extract").is_dir() or candidate.name == "elife_extract":
        sys.path.insert(0, str(candidate if candidate.name != "elife_extract" else candidate.parent))
        break
else:
    # Last resort: assume elife_extract is importable from current PYTHONPATH
    pass

# Prompts directory — configurable via env var
PROMPTS_DIR = Path(os.environ.get("ELIFE_PROMPTS_DIR", "")).resolve() if os.environ.get("ELIFE_PROMPTS_DIR") else None

# Lazy imports — these pull in anthropic SDK etc.
_pipeline_ready = False


def _ensure_pipeline():
    global _pipeline_ready
    if not _pipeline_ready:
        global prepare, run_agent, reconcile_step, external_review
        global Config, reset_client, get_client
        from elife_extract.prepare import prepare
        from elife_extract.agents import run_agent, reset_client, get_client
        from elife_extract.reconcile import reconcile as reconcile_step
        from elife_extract.external_review import external_review
        from elife_extract.config import Config
        _pipeline_ready = True


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Vertex access control — token whitelist + IP whitelist
DEMO_TOKENS = set(
    t.strip() for t in os.environ.get("ELIFE_EXTRACT_DEMO_TOKENS", "").split(",")
    if t.strip()
)
# IPs that don't need a token (comma-separated in env var)
WHITELISTED_IPS = set(
    ip.strip() for ip in os.environ.get("ELIFE_EXTRACT_WHITELIST_IPS", "").split(",")
    if ip.strip()
)


def _is_authorized(api_key: str, demo_token: str, request) -> bool:
    """Check if the request is authorized for Vertex access."""
    if api_key:
        return True  # Using their own key
    if demo_token and demo_token in DEMO_TOKENS:
        return True
    # Check IP whitelist
    client_ip = request.headers.get("x-real-ip", request.headers.get("x-forwarded-for", "")).split(",")[0].strip()
    if client_ip and client_ip in WHITELISTED_IPS:
        return True
    return False

app = FastAPI(
    title="eLife Claim Trees — Extraction API",
    description="Extract structured claim graphs from eLife papers",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# Mount review endpoints
from review import router as review_router
from llm import PROVIDER_MODELS
app.include_router(review_router)


class ExtractRequest(BaseModel):
    doi: str
    api_key: str = ""
    demo_token: str = ""
    provider: str = "anthropic"  # anthropic, openai, google, openrouter, vertex
    model_extract: str = "claude-sonnet-4-6"
    model_reconcile: str = "claude-opus-4-6"


@app.get("/providers")
def list_providers():
    """List available providers and their models."""
    return PROVIDER_MODELS


def _build_oxa_claim(claim: dict) -> dict:
    """Convert a reconciled claim dict to an OXA Claim node."""
    EDGE_MAP = {
        "supports": "cito:supports",
        "extends": "cito:extends",
        "qualifies": "cito:qualifies",
        "derived-from": "cito:citesAsSourceDocument",
        "enables-method": "cito:usesMethodIn",
        "dissociates-with": "cito:disagreesWith",
        "requires": "claimrel:requires",
        "tests": "claimrel:tests",
        "entails": "claimrel:entails",
        "interprets": "claimrel:interprets",
        "scopes": "claimrel:scopes",
        "rules-out": "claimrel:rulesOut",
        "replicates": "claimrel:replicates",
        "contradicts": "claimrel:contradicts",
    }
    slug = claim.get("slug", str(uuid.uuid4())[:8])
    role = claim.get("role", "empirical")
    panel = claim.get("panel")
    if isinstance(panel, str):
        panel = [p.strip() for p in panel.split(",")]

    relations = []
    for edge_key, cito in EDGE_MAP.items():
        targets = claim.get(edge_key, [])
        if isinstance(targets, str):
            targets = [targets]
        for t in (targets or []):
            if t:
                relations.append({"xref": t, "relationType": cito})

    node = {
        "type": "Claim",
        "identifier": slug,
        "role": role,
        "children": [{"type": "Text", "value": claim.get("claim", "")}],
    }
    if panel:
        node["panel"] = panel
    if claim.get("epistemic"):
        node["epistemicStrength"] = claim["epistemic"]
    if relations:
        node["relations"] = relations
    if claim.get("confidence"):
        node["metadata"] = {"confidence": claim["confidence"]}
    return node


def _run_agent_litellm(agent_name, paper, cfg, provider, api_key, model):
    """Run an extraction agent via litellm (for non-Anthropic providers)."""
    from elife_extract.agents import slice_for_agent, load_prompt, parse_json_response
    from elife_extract.schema import AgentExtraction, CandidateClaim
    from llm import call_llm

    system_prompt = load_prompt(agent_name, cfg)
    paper_slice = slice_for_agent(agent_name, paper)

    if not paper_slice.strip() or len(paper_slice) < 200:
        return AgentExtraction(agent=agent_name, paper_slug=paper.paper_slug, model=model, claims=[])

    raw = call_llm(
        provider=provider, api_key=api_key, model=model,
        system=system_prompt, user_message=paper_slice, max_tokens=32768,
    )
    parsed = parse_json_response(raw)
    if not isinstance(parsed, list):
        raise ValueError(f"agent={agent_name} returned non-list JSON")
    claims = [CandidateClaim(**c) for c in parsed]
    return AgentExtraction(agent=agent_name, paper_slug=paper.paper_slug, model=model, claims=claims)


def _reconcile_litellm(results_ext, caption_ext, structure_ext, cfg, provider, api_key, model, paper_doi, paper_title):
    """Run reconciliation via litellm."""
    from elife_extract.reconcile import load_reconciler_prompt, _format_agent_input
    from elife_extract.agents import parse_json_response
    from elife_extract.schema import DraftClaimTable, ReconciledClaim
    from llm import call_llm

    system_prompt = load_reconciler_prompt(cfg)
    user_message = (
        f"# Paper: {paper_title or 'unknown'}\nDOI: {paper_doi}\n"
        f"Slug: {results_ext.paper_slug}\n\n"
        f"{_format_agent_input(results_ext)}\n\n"
        f"{_format_agent_input(caption_ext)}\n\n"
        f"{_format_agent_input(structure_ext)}\n\n"
        f"Reconcile these three agent outputs into a single confidence-tagged "
        f"draft claim table per the schema in your instructions. Return JSON only."
    )

    raw = call_llm(
        provider=provider, api_key=api_key, model=model,
        system=system_prompt, user_message=user_message, max_tokens=32768,
    )
    parsed = parse_json_response(raw)
    if isinstance(parsed, dict):
        claims_list = parsed.get("claims", [])
    elif isinstance(parsed, list):
        claims_list = parsed
    else:
        raise ValueError(f"Reconciler returned unexpected type: {type(parsed)}")
    claims = [ReconciledClaim(**c) for c in claims_list]
    return DraftClaimTable(paper_slug=results_ext.paper_slug, paper_doi=paper_doi, paper_title=paper_title, claims=claims)


def _external_review_litellm(paper, draft, cfg, provider, api_key, model):
    """Run external review via litellm."""
    from elife_extract.external_review import load_reviewer_prompt, _format_paper_context
    from elife_extract.agents import parse_json_response
    from elife_extract.schema import DraftClaimTable, ReconciledClaim
    from llm import call_llm

    system_prompt = load_reviewer_prompt(cfg)
    paper_context = _format_paper_context(paper)
    draft_json = draft.model_dump_json()
    user_message = f"{paper_context}\n\n---\n\nDraft claim table:\n{draft_json}\n\nReview and revise. Return the full revised claim table as JSON."

    raw = call_llm(
        provider=provider, api_key=api_key, model=model,
        system=system_prompt, user_message=user_message, max_tokens=32768,
    )
    parsed = parse_json_response(raw)
    if isinstance(parsed, dict):
        claims_list = parsed.get("claims", [])
    elif isinstance(parsed, list):
        claims_list = parsed
    else:
        claims_list = draft.claims
    claims = [ReconciledClaim(**c) for c in claims_list]
    return DraftClaimTable(paper_slug=draft.paper_slug, paper_doi=draft.paper_doi or "uploaded", paper_title=draft.paper_title, claims=claims, config_snapshot=draft.config_snapshot)


def _run_agent_streaming(agent_name, paper, cfg, yield_fn):
    """Run an extraction agent with streaming progress via yield_fn.

    yield_fn(msg) emits an SSE event. Called every ~500 tokens with
    a snippet of the output so far.
    """
    from elife_extract.agents import slice_for_agent, load_prompt, parse_json_response, get_client
    from elife_extract.schema import AgentExtraction, CandidateClaim

    model = {"results": cfg.model_results, "caption": cfg.model_caption, "structure": cfg.model_structure}[agent_name]
    system_prompt = load_prompt(agent_name, cfg)
    paper_slice = slice_for_agent(agent_name, paper)

    if not paper_slice.strip() or len(paper_slice) < 200:
        yield_fn(f"  skipped (slice too short: {len(paper_slice)} chars)")
        return AgentExtraction(agent=agent_name, paper_slug=paper.paper_slug, model=model, claims=[])

    client = get_client(cfg)
    text_chunks = []
    token_count = 0
    last_report = 0
    last_heartbeat = time.time()
    full_text_so_far = ""

    with client.messages.stream(
        model=model, max_tokens=32768, system=system_prompt,
        messages=[{"role": "user", "content": paper_slice}],
    ) as stream:
        for text in stream.text_stream:
            text_chunks.append(text)
            full_text_so_far += text
            token_count += len(text.split())
            now = time.time()
            if token_count - last_report >= 100:
                last_report = token_count
                # Show the latest claim being generated
                claim_matches = list(re.finditer(r'"claim":\s*"([^"]{10,})', full_text_so_far))
                n_claims = len(claim_matches)
                if claim_matches:
                    latest = claim_matches[-1].group(1)[:70]
                    yield_fn(f"  claim {n_claims}: {latest}...")
                else:
                    yield_fn(f"  generating... ({token_count} tokens)")
                last_heartbeat = now
            elif now - last_heartbeat >= 10:
                yield_fn(f"  [{token_count} tokens, {int(now - last_heartbeat)}s since last update...]")
                last_heartbeat = now

    raw = full_text_so_far
    yield_fn(f"  complete ({len(raw)} chars, ~{token_count} tokens)")

    parsed = parse_json_response(raw)
    if not isinstance(parsed, list):
        raise ValueError(f"agent={agent_name} returned non-list JSON")
    claims = [CandidateClaim(**c) for c in parsed]
    return AgentExtraction(agent=agent_name, paper_slug=paper.paper_slug, model=model, claims=claims)


def _reconcile_streaming(results_ext, caption_ext, structure_ext, cfg, paper_doi, paper_title, yield_fn):
    """Reconcile with streaming progress."""
    from elife_extract.reconcile import load_reconciler_prompt, _format_agent_input
    from elife_extract.agents import parse_json_response, get_client
    from elife_extract.schema import DraftClaimTable, ReconciledClaim

    system_prompt = load_reconciler_prompt(cfg)
    user_message = (
        f"# Paper: {paper_title or 'unknown'}\nDOI: {paper_doi}\n"
        f"Slug: {results_ext.paper_slug}\n\n"
        f"{_format_agent_input(results_ext)}\n\n"
        f"{_format_agent_input(caption_ext)}\n\n"
        f"{_format_agent_input(structure_ext)}\n\n"
        f"Reconcile these three agent outputs into a single confidence-tagged draft claim table. Return JSON only."
    )

    client = get_client(cfg)
    text_chunks = []
    token_count = 0
    last_report = 0
    full_text_so_far = ""

    with client.messages.stream(
        model=cfg.model_reconcile, max_tokens=32768, system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            text_chunks.append(text)
            full_text_so_far += text
            token_count += len(text.split())
            if token_count - last_report >= 150:
                last_report = token_count
                claim_matches = list(re.finditer(r'"claim":\s*"([^"]{10,})', full_text_so_far))
                if claim_matches:
                    yield_fn(f"  merging claim {len(claim_matches)}: {claim_matches[-1].group(1)[:50]}...")
                else:
                    yield_fn(f"  processing... ({token_count} tokens)")

    raw = full_text_so_far
    yield_fn(f"  reconciliation complete (~{token_count} tokens)")

    parsed = parse_json_response(raw)
    if isinstance(parsed, dict):
        claims_list = parsed.get("claims", [])
    elif isinstance(parsed, list):
        claims_list = parsed
    else:
        raise ValueError(f"Reconciler returned unexpected type: {type(parsed)}")
    claims = [ReconciledClaim(**c) for c in claims_list]
    return DraftClaimTable(paper_slug=results_ext.paper_slug, paper_doi=paper_doi, paper_title=paper_title, claims=claims)


def _external_review_streaming(paper, draft, cfg, yield_fn):
    """External review with streaming progress."""
    from elife_extract.external_review import load_reviewer_prompt, _format_paper_context
    from elife_extract.agents import parse_json_response, get_client
    from elife_extract.schema import DraftClaimTable, ReconciledClaim

    system_prompt = load_reviewer_prompt(cfg)
    paper_context = _format_paper_context(paper)
    draft_json = draft.model_dump_json()
    user_message = f"{paper_context}\n\n---\n\nDraft claim table:\n{draft_json}\n\nReview and revise. Return the full revised claim table as JSON."

    client = get_client(cfg)
    text_chunks = []
    token_count = 0
    last_report = 0
    full_text_so_far = ""

    with client.messages.stream(
        model=cfg.model_reconcile, max_tokens=32768, system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for text in stream.text_stream:
            text_chunks.append(text)
            full_text_so_far += text
            token_count += len(text.split())
            if token_count - last_report >= 150:
                last_report = token_count
                claim_matches = list(re.finditer(r'"claim":\s*"([^"]{10,})', full_text_so_far))
                if claim_matches:
                    yield_fn(f"  merging claim {len(claim_matches)}: {claim_matches[-1].group(1)[:50]}...")
                else:
                    yield_fn(f"  processing... ({token_count} tokens)")

    raw = full_text_so_far
    yield_fn(f"  review complete (~{token_count} tokens)")

    parsed = parse_json_response(raw)
    if isinstance(parsed, dict):
        claims_list = parsed.get("claims", [])
    elif isinstance(parsed, list):
        claims_list = parsed
    else:
        claims_list = [c.model_dump() for c in draft.claims]
    claims = [ReconciledClaim(**c) for c in claims_list]
    return DraftClaimTable(paper_slug=draft.paper_slug, paper_doi=draft.paper_doi, paper_title=draft.paper_title, claims=claims, config_snapshot=draft.config_snapshot)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract")
async def extract(req: ExtractRequest, request: "Request"):
    """Run the full pipeline and stream progress via SSE."""
    _ensure_pipeline()

    def generate():
        try:
            # Build config — check auth
            cfg = Config()
            if req.api_key:
                cfg.anthropic_api_key = req.api_key
                cfg.backend = "anthropic"
            else:
                if not _is_authorized(req.api_key, req.demo_token, request):
                    raise ValueError("Not authorized — provide an API key, demo token, or connect from a whitelisted IP")
                cfg.backend = "vertex"
            cfg.model_results = req.model_extract
            cfg.model_caption = req.model_extract
            cfg.model_structure = req.model_extract
            cfg.model_reconcile = req.model_reconcile
            cfg.review_mode = "external"
            # Find prompts dir
            if PROMPTS_DIR and PROMPTS_DIR.is_dir():
                cfg.prompts_dir = PROMPTS_DIR
            else:
                # Try relative to this file in HAAK repo layout
                for p in [
                    API_DIR.parent / "extract/prompts",
                    API_DIR / "prompts",
                    API_DIR.parent / "home/collabs/elife/claim-trees/extract/prompts",
                ]:
                    if p.is_dir():
                        cfg.prompts_dir = p
                        break
            cfg.output_dir = Path("/tmp/elife-extract-api")
            cfg.output_dir.mkdir(parents=True, exist_ok=True)

            # Reset client cache so we use the new API key
            reset_client()

            # Step 1: Prepare
            yield f"data: {json.dumps({'step': 'prepare', 'message': 'Fetching and parsing JATS-XML...'})}\n\n"
            paper = prepare(req.doi, input_format="jats")
            yield f"data: {json.dumps({'step': 'prepare', 'message': f'Parsed: {paper.title}', 'slug': paper.paper_slug, 'figures': len(paper.figure_captions), 'panels': len(paper.panel_ids)})}\n\n"

            # Use litellm for non-Anthropic models (including Gemini on Vertex)
            is_gemini = req.model_extract.startswith("gemini")
            use_litellm = req.provider not in ("anthropic", "vertex") or is_gemini
            provider = "vertex" if (req.provider == "vertex" and is_gemini) else req.provider

            # Steps 2-3: Three-agent extraction (one at a time with progress)
            for i, (agent_name, agent_desc) in enumerate([
                ("results", "Results-reader (reads abstract + results prose)"),
                ("caption", "Caption-reader (reads figure captions panel by panel)"),
                ("structure", "Structure-reader (reads methods + supplements)"),
            ], 1):
                yield f"data: {json.dumps({'step': 'extract', 'message': f'Agent {i}/3: {agent_desc}...'})}\n\n"
                if use_litellm:
                    ext = _run_agent_litellm(agent_name, paper, cfg, provider, req.api_key, req.model_extract)
                else:
                    ext = run_agent(agent_name, paper, cfg)
                agent_short = agent_desc.split(" (")[0]
                yield f"data: {json.dumps({'step': 'extract', 'message': f'Agent {i}/3: {agent_short} → {len(ext.claims)} claims'})}\n\n"
                if i == 1: results_ext = ext
                elif i == 2: caption_ext = ext
                else: structure_ext = ext

            n_candidates = len(results_ext.claims) + len(caption_ext.claims) + len(structure_ext.claims)
            yield f"data: {json.dumps({'step': 'extract', 'message': f'Total: {n_candidates} candidate claims from 3 agents'})}\n\n"

            # Step 4: Reconciliation
            yield f"data: {json.dumps({'step': 'reconcile', 'message': f'Reconciling — merging 3 agent outputs ({provider})...'})}\n\n"
            if use_litellm:
                draft = _reconcile_litellm(results_ext, caption_ext, structure_ext, cfg, provider, req.api_key, req.model_reconcile, paper.doi, paper.title)
            else:
                draft = reconcile_step(results_ext, caption_ext, structure_ext, cfg, paper_doi=paper.doi, paper_title=paper.title)
            yield f"data: {json.dumps({'step': 'reconcile', 'message': f'Reconciled to {len(draft.claims)} claims'})}\n\n"

            # Step 4.5: External review
            yield f"data: {json.dumps({'step': 'review', 'message': 'Running external reviewer...'})}\n\n"
            if use_litellm:
                reviewed = _external_review_litellm(paper, draft, cfg, provider, req.api_key, req.model_reconcile)
            else:
                reviewed = external_review(paper, draft, cfg)
            yield f"data: {json.dumps({'step': 'review', 'message': f'Reviewed: {len(reviewed.claims)} claims after revision'})}\n\n"

            # Build OXA output
            oxa_claims = [_build_oxa_claim(c.model_dump()) for c in reviewed.claims]

            # Step 6: Infer edges between claims
            yield f"data: {json.dumps({'step': 'edges', 'message': f'Inferring relationships between {len(oxa_claims)} claims...'})}\n\n"
            from infer_edges import infer_edges, apply_edges
            if use_litellm:
                from llm import call_llm as _call
                def llm_fn(sys, usr, mdl):
                    return _call(provider=provider, api_key=req.api_key, model=mdl, system=sys, user_message=usr)
            else:
                def llm_fn(sys, usr, mdl):
                    client = get_client(cfg)
                    resp = client.messages.create(model=mdl, max_tokens=8192, system=sys, messages=[{"role": "user", "content": usr}])
                    return resp.content[0].text
            edges = infer_edges(oxa_claims, call_llm_fn=llm_fn, model=cfg.model_reconcile)
            oxa_claims = apply_edges(oxa_claims, edges)
            yield f"data: {json.dumps({'step': 'edges', 'message': f'Found {len(edges)} relationships between claims'})}\n\n"

            article = {
                "type": "Article",
                "identifier": paper.paper_slug,
                "metadata": {
                    "doi": paper.doi,
                    "title": paper.title,
                    "authors": paper.authors,
                },
                "children": oxa_claims,
            }

            yield f"data: {json.dumps({'step': 'done', 'message': f'Complete: {len(oxa_claims)} claims, {len(edges)} relationships', 'article': article})}\n\n"

        except Exception as e:
            logger.exception("Extraction failed")
            yield f"data: {json.dumps({'step': 'error', 'message': str(e)})}\n\n"

        finally:
            # Discard the API key by resetting the client
            reset_client()

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.post("/extract-file")
async def extract_file(
    request: Request,
    file: UploadFile = File(...),
    api_key: str = Form(""),
    demo_token: str = Form(""),
    provider: str = Form("anthropic"),
    model_extract: str = Form("claude-sonnet-4-6"),
    model_reconcile: str = Form("claude-opus-4-6"),
):
    """Extract claims from an uploaded PDF or DOCX file."""
    _ensure_pipeline()

    # Save uploaded file
    upload_dir = Path("/tmp/elife-extract-api/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    filename = file.filename or "upload"
    save_path = upload_dir / filename
    content = await file.read()
    save_path.write_bytes(content)

    def generate():
        try:
            # Build config
            cfg = Config()
            if api_key:
                cfg.anthropic_api_key = api_key
                cfg.backend = "anthropic"
            else:
                if not _is_authorized(api_key, demo_token, request):
                    raise ValueError("Not authorized — provide an API key, demo token, or connect from a whitelisted IP")
                cfg.backend = "vertex"
            cfg.model_results = model_extract
            cfg.model_caption = model_extract
            cfg.model_structure = model_extract
            cfg.model_reconcile = model_reconcile
            cfg.review_mode = "external"
            if PROMPTS_DIR and PROMPTS_DIR.is_dir():
                cfg.prompts_dir = PROMPTS_DIR
            else:
                for p in [
                    API_DIR.parent / "extract/prompts",
                    API_DIR / "prompts",
                    API_DIR.parent / "home/collabs/elife/claim-trees/extract/prompts",
                ]:
                    if p.is_dir():
                        cfg.prompts_dir = p
                        break
            cfg.output_dir = Path("/tmp/elife-extract-api")
            cfg.output_dir.mkdir(parents=True, exist_ok=True)
            reset_client()

            # Parse the file
            yield f"data: {json.dumps({'step': 'prepare', 'message': f'Parsing {filename}...'})}\n\n"

            suffix = save_path.suffix.lower()
            if suffix == ".pdf":
                from elife_extract.prepare import extract_text, slice_sections, extract_figure_captions
                from elife_extract.prepare import captions_text_block, guess_metadata, derive_slug
                from elife_extract.prepare import PreparedPaper

                full_text = extract_text(save_path)
                sections = slice_sections(full_text)
                captions = extract_figure_captions(full_text)
                title, authors, year = guess_metadata(full_text)
                slug = derive_slug(authors, year, title)

                paper = PreparedPaper(
                    doi="uploaded",
                    article_id="0",
                    paper_slug=slug,
                    title=title,
                    authors=authors,
                    abstract=sections.get("abstract", ""),
                    results_text=sections.get("results", full_text[:50000]),
                    captions_text=captions_text_block(captions),
                    methods_text=sections.get("methods", ""),
                    extraction_path="pdf",
                    extraction_path_note=f"Uploaded: {filename}",
                    figure_captions=captions,
                )
            elif suffix in (".docx", ".doc"):
                # Extract text from DOCX via python-docx
                try:
                    import docx
                    doc = docx.Document(str(save_path))
                    full_text = "\n".join(p.text for p in doc.paragraphs)
                except ImportError:
                    # Fallback: try pandoc
                    import subprocess
                    result = subprocess.run(
                        ["pandoc", str(save_path), "-t", "plain"],
                        capture_output=True, text=True, timeout=30,
                    )
                    full_text = result.stdout

                from elife_extract.prepare import slice_sections, extract_figure_captions
                from elife_extract.prepare import captions_text_block, guess_metadata, derive_slug
                from elife_extract.prepare import PreparedPaper

                sections = slice_sections(full_text)
                captions = extract_figure_captions(full_text)
                title, authors, year = guess_metadata(full_text)
                slug = derive_slug(authors, year, title)

                paper = PreparedPaper(
                    doi="uploaded",
                    article_id="0",
                    paper_slug=slug,
                    title=title,
                    authors=authors,
                    abstract=sections.get("abstract", ""),
                    results_text=sections.get("results", full_text[:50000]),
                    captions_text=captions_text_block(captions),
                    methods_text=sections.get("methods", ""),
                    extraction_path="pdf",
                    extraction_path_note=f"Uploaded DOCX: {filename}",
                    figure_captions=captions,
                )
            else:
                raise ValueError(f"Unsupported file type: {suffix}. Upload PDF or DOCX.")

            yield f"data: {json.dumps({'step': 'prepare', 'message': f'Parsed: {paper.title or filename}', 'slug': paper.paper_slug, 'figures': len(paper.figure_captions), 'panels': len(paper.panel_ids)})}\n\n"

            # Use litellm for non-Anthropic models (including Gemini on Vertex)
            is_gemini = model_extract.startswith("gemini")
            active_provider = provider  # capture from outer scope
            use_litellm = active_provider not in ("anthropic", "vertex") or is_gemini
            q = queue.Queue()

            def emit(step, msg):
                q.put(f"data: {json.dumps({'step': step, 'message': msg})}\n\n")

            # Steps 2-3: Streaming extraction
            agents_data = [
                ("results", "Results-reader"),
                ("caption", "Caption-reader"),
                ("structure", "Structure-reader"),
            ]
            extractions = []
            for i, (agent_name, agent_short) in enumerate(agents_data, 1):
                yield f"data: {json.dumps({'step': 'extract', 'message': f'Agent {i}/3: {agent_short}...'})}\n\n"
                if use_litellm:
                    ext = _run_agent_litellm(agent_name, paper, cfg, active_provider, api_key, model_extract)
                else:
                    # Run in thread with streaming callbacks via queue
                    result_holder = [None]
                    error_holder = [None]
                    def run_in_thread(an=agent_name):
                        try:
                            result_holder[0] = _run_agent_streaming(an, paper, cfg, lambda msg: emit('extract', msg))
                        except Exception as e:
                            error_holder[0] = e
                    t = threading.Thread(target=run_in_thread)
                    t.start()
                    last_hb = time.time()
                    while t.is_alive():
                        t.join(timeout=1.0)
                        got_msg = False
                        while not q.empty():
                            yield q.get()
                            got_msg = True
                            last_hb = time.time()
                        if not got_msg and time.time() - last_hb >= 10:
                            yield f"data: {json.dumps({'step': 'heartbeat', 'message': 'still working...'})}\n\n"
                            last_hb = time.time()
                    while not q.empty():
                        yield q.get()
                    if error_holder[0]:
                        raise error_holder[0]
                    ext = result_holder[0]
                yield f"data: {json.dumps({'step': 'extract', 'message': f'Agent {i}/3: {agent_short} → {len(ext.claims)} claims'})}\n\n"
                extractions.append(ext)

            results_ext, caption_ext, structure_ext = extractions
            n_candidates = sum(len(e.claims) for e in extractions)
            yield f"data: {json.dumps({'step': 'extract', 'message': f'Total: {n_candidates} candidate claims from 3 agents'})}\n\n"

            # Step 4: Streaming reconciliation
            yield f"data: {json.dumps({'step': 'reconcile', 'message': 'Reconciling — merging 3 agent outputs...'})}\n\n"
            if use_litellm:
                draft = _reconcile_litellm(results_ext, caption_ext, structure_ext, cfg, active_provider, api_key, model_reconcile, paper.doi, paper.title)
            else:
                result_holder = [None]
                error_holder = [None]
                def run_reconcile():
                    try:
                        result_holder[0] = _reconcile_streaming(results_ext, caption_ext, structure_ext, cfg, paper.doi, paper.title, lambda msg: emit('reconcile', msg))
                    except Exception as e:
                        error_holder[0] = e
                t = threading.Thread(target=run_reconcile)
                t.start()
                while t.is_alive():
                    t.join(timeout=0.5)
                    while not q.empty():
                        yield q.get()
                while not q.empty():
                    yield q.get()
                if error_holder[0]:
                    raise error_holder[0]
                draft = result_holder[0]
            yield f"data: {json.dumps({'step': 'reconcile', 'message': f'Reconciled to {len(draft.claims)} claims'})}\n\n"

            # Step 4.5: Streaming external review
            yield f"data: {json.dumps({'step': 'review', 'message': 'Running external reviewer...'})}\n\n"
            if use_litellm:
                reviewed = _external_review_litellm(paper, draft, cfg, active_provider, api_key, model_reconcile)
            else:
                result_holder = [None]
                error_holder = [None]
                def run_review():
                    try:
                        result_holder[0] = _external_review_streaming(paper, draft, cfg, lambda msg: emit('review', msg))
                    except Exception as e:
                        error_holder[0] = e
                t = threading.Thread(target=run_review)
                t.start()
                while t.is_alive():
                    t.join(timeout=0.5)
                    while not q.empty():
                        yield q.get()
                while not q.empty():
                    yield q.get()
                if error_holder[0]:
                    raise error_holder[0]
                reviewed = result_holder[0]
            yield f"data: {json.dumps({'step': 'review', 'message': f'Reviewed: {len(reviewed.claims)} claims'})}\n\n"

            # Build OXA output
            oxa_claims = [_build_oxa_claim(c.model_dump()) for c in reviewed.claims]

            # Step 6: Infer edges
            yield f"data: {json.dumps({'step': 'edges', 'message': f'Inferring relationships between {len(oxa_claims)} claims...'})}\n\n"
            from infer_edges import infer_edges, apply_edges
            if use_litellm:
                from llm import call_llm as _call
                def llm_fn(sys, usr, mdl):
                    return _call(provider=active_provider, api_key=api_key, model=mdl, system=sys, user_message=usr)
            else:
                def llm_fn(sys, usr, mdl):
                    c = get_client(cfg)
                    resp = c.messages.create(model=mdl, max_tokens=8192, system=sys, messages=[{"role": "user", "content": usr}])
                    return resp.content[0].text
            edges = infer_edges(oxa_claims, call_llm_fn=llm_fn, model=cfg.model_reconcile)
            oxa_claims = apply_edges(oxa_claims, edges)
            yield f"data: {json.dumps({'step': 'edges', 'message': f'Found {len(edges)} relationships'})}\n\n"

            article = {
                "type": "Article",
                "identifier": paper.paper_slug,
                "metadata": {
                    "title": paper.title,
                    "authors": paper.authors,
                    "source": filename,
                },
                "children": oxa_claims,
            }

            yield f"data: {json.dumps({'step': 'done', 'message': f'Complete: {len(oxa_claims)} claims, {len(edges)} relationships', 'article': article})}\n\n"

        except Exception as e:
            logger.exception("File extraction failed")
            yield f"data: {json.dumps({'step': 'error', 'message': str(e)})}\n\n"
        finally:
            reset_client()
            # Clean up uploaded file
            try:
                save_path.unlink(missing_ok=True)
            except Exception:
                pass

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
