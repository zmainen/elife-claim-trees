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
import sys
import threading
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

# Provider → model catalog (what shows up in the /providers dropdown).
# Model IDs reflect the generation deployed at the time of writing; the
# extraction pipeline accepts whatever the provider's API accepts.
PROVIDER_MODELS = {
    "anthropic": [
        {"id": "claude-sonnet-4-6", "name": "Claude Sonnet 4.6 (balanced)", "tier": "fast"},
        {"id": "claude-opus-4-8", "name": "Claude Opus 4.8 (best)", "tier": "best"},
        {"id": "claude-haiku-4-5", "name": "Claude Haiku 4.5 (fast/cheap)", "tier": "cheap"},
    ],
    "openai": [
        {"id": "gpt-4o", "name": "GPT-4o", "tier": "fast"},
        {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "tier": "cheap"},
        {"id": "o3", "name": "o3", "tier": "best"},
    ],
    "google": [
        {"id": "gemini-2.5-pro", "name": "Gemini 2.5 Pro (best)", "tier": "best"},
        {"id": "gemini-2.5-flash", "name": "Gemini 2.5 Flash (fast)", "tier": "fast"},
    ],
    "openrouter": [
        {"id": "anthropic/claude-sonnet-4", "name": "Claude Sonnet 4 (via OpenRouter)", "tier": "fast"},
        {"id": "openai/gpt-4o", "name": "GPT-4o (via OpenRouter)", "tier": "fast"},
        {"id": "google/gemini-2.5-pro", "name": "Gemini 2.5 Pro (via OpenRouter)", "tier": "best"},
    ],
    # Hosted demo path (server-paid Vertex). cr-mainen pins opus at 4-6 —
    # 4-7/4-8 time out on that region. Requires a demo token / passkey auth.
    "vertex": [
        {"id": "gemini-2.5-flash", "name": "Gemini 2.5 Flash (fastest)", "tier": "fast"},
        {"id": "gemini-2.5-pro", "name": "Gemini 2.5 Pro", "tier": "best"},
        {"id": "claude-sonnet-4-6", "name": "Claude Sonnet 4.6 (Vertex)", "tier": "fast"},
        {"id": "claude-opus-4-6", "name": "Claude Opus 4.6 (Vertex)", "tier": "best"},
    ],
}

# Lazy imports — these pull in anthropic SDK etc.
_pipeline_ready = False


def _ensure_pipeline():
    global _pipeline_ready
    if not _pipeline_ready:
        global prepare, run_agent, reconcile_step, external_review
        global infer_edges, apply_oxa_edges
        global Config, reset_client
        from elife_extract.prepare import prepare
        from elife_extract.agents import run_agent, reset_client
        from elife_extract.reconcile import reconcile as reconcile_step
        from elife_extract.external_review import external_review
        from elife_extract.edges import infer_edges, apply_oxa_edges
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
app.include_router(review_router)


class ExtractRequest(BaseModel):
    doi: str
    api_key: str = ""
    demo_token: str = ""
    provider: str = "anthropic"  # anthropic, openai, google, openrouter, vertex
    model_extract: str = "claude-sonnet-4-6"
    model_reconcile: str = "claude-opus-4-8"


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


def _backend_for(provider: str, model: str) -> str:
    """Map (provider, model) to the package's backend string.

    "vertex" carries both Anthropic Claude models (handled by AnthropicVertex
    via the SDK) and Gemini models (handled by litellm's vertex_ai/ prefix).
    Every other provider maps to itself.
    """
    if provider == "vertex" and model.startswith("gemini"):
        return "vertex_ai"
    return provider  # "vertex", "anthropic", "openai", "google", "openrouter", …


def _make_cfg(provider: str, api_key: str, model_extract: str, model_reconcile: str) -> "Config":
    """Build a Config from per-request parameters.

    The backend is chosen from (provider, model) so Gemini on Vertex goes
    through litellm's vertex_ai/ path while Claude on Vertex goes through the
    Anthropic SDK. For non-Vertex providers the extract and reconcile models
    are always on the same backend, so one backend field covers both.
    """
    cfg = Config()
    # Use the extract model to pick the backend (reconcile is usually same provider)
    cfg.backend = _backend_for(provider, model_extract)
    if provider == "anthropic":
        cfg.anthropic_api_key = api_key or None
        cfg.backend = "anthropic"
    elif api_key:
        cfg.api_key = api_key
    cfg.model_results = model_extract
    cfg.model_caption = model_extract
    cfg.model_structure = model_extract
    cfg.model_reconcile = model_reconcile
    cfg.review_mode = "external"
    # Prompts dir
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
    return cfg


class _SSELogHandler(logging.Handler):
    """Capture package heartbeat messages and forward them as SSE events.

    The package's `_Progress` class logs timing and throughput to the
    `elife_extract` logger.  Installing this handler on that logger during
    a request lets the SSE generator relay those messages to the client
    without re-implementing the progress logic.
    """

    def __init__(self, q: "queue.Queue[str]", step: str) -> None:
        super().__init__()
        self.q = q
        self.step = step

    def emit(self, record: logging.LogRecord) -> None:
        msg = record.getMessage()
        self.q.put(f"data: {json.dumps({'step': self.step, 'message': msg})}\n\n")


def _run_with_sse(fn, q: "queue.Queue[str]", step: str):
    """Generator: yields SSE strings while fn() runs in a thread; returns the result.

    Package heartbeat messages are captured via a logging handler on the
    `elife_extract` logger and forwarded to the SSE stream. The return value
    is available to the caller via `result = yield from _run_with_sse(...)`,
    which works because Python sub-generators surface their `return` value as
    the expression value of `yield from`.
    """
    pkg_logger = logging.getLogger("elife_extract")
    handler = _SSELogHandler(q, step)
    pkg_logger.addHandler(handler)
    result_holder: list = [None]
    error_holder: list = [None]

    def target():
        try:
            result_holder[0] = fn()
        except Exception as exc:
            error_holder[0] = exc
        finally:
            pkg_logger.removeHandler(handler)

    t = threading.Thread(target=target)
    t.start()
    while t.is_alive():
        t.join(timeout=0.5)
        while not q.empty():
            yield q.get()
    while not q.empty():
        yield q.get()
    if error_holder[0]:
        raise error_holder[0]
    return result_holder[0]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract")
async def extract(req: ExtractRequest, request: "Request"):
    """Run the full pipeline and stream progress via SSE."""
    _ensure_pipeline()

    def generate():
        try:
            if not req.api_key and not _is_authorized(req.api_key, req.demo_token, request):
                raise ValueError("Not authorized — provide an API key, demo token, or connect from a whitelisted IP")

            cfg = _make_cfg(req.provider, req.api_key, req.model_extract, req.model_reconcile)
            reset_client()

            # Step 1: Prepare
            yield f"data: {json.dumps({'step': 'prepare', 'message': 'Fetching and parsing JATS-XML...'})}\n\n"
            paper = prepare(req.doi, input_format="jats")
            yield f"data: {json.dumps({'step': 'prepare', 'message': f'Parsed: {paper.title}', 'slug': paper.paper_slug, 'figures': len(paper.figure_captions), 'panels': len(paper.panel_ids)})}\n\n"

            # Steps 2-3: Three-agent extraction
            q: queue.Queue = queue.Queue()
            extractions = []
            for i, (agent_name, agent_desc) in enumerate([
                ("results", "Results-reader (reads abstract + results prose)"),
                ("caption", "Caption-reader (reads figure captions panel by panel)"),
                ("structure", "Structure-reader (reads methods + supplements)"),
            ], 1):
                yield f"data: {json.dumps({'step': 'extract', 'message': f'Agent {i}/3: {agent_desc}...'})}\n\n"
                ext = yield from _run_with_sse(
                    lambda an=agent_name: run_agent(an, paper, cfg), q, "extract"
                )
                agent_short = agent_desc.split(" (")[0]
                yield f"data: {json.dumps({'step': 'extract', 'message': f'Agent {i}/3: {agent_short} → {len(ext.claims)} claims'})}\n\n"
                extractions.append(ext)

            results_ext, caption_ext, structure_ext = extractions
            n_candidates = sum(len(e.claims) for e in extractions)
            yield f"data: {json.dumps({'step': 'extract', 'message': f'Total: {n_candidates} candidate claims from 3 agents'})}\n\n"

            # Step 4: Reconciliation
            yield f"data: {json.dumps({'step': 'reconcile', 'message': f'Reconciling — merging 3 agent outputs ({req.provider})...'})}\n\n"
            draft = yield from _run_with_sse(
                lambda: reconcile_step(results_ext, caption_ext, structure_ext, cfg,
                                       paper_doi=paper.doi, paper_title=paper.title),
                q, "reconcile"
            )
            yield f"data: {json.dumps({'step': 'reconcile', 'message': f'Reconciled to {len(draft.claims)} claims'})}\n\n"

            # Step 4.5: External review
            yield f"data: {json.dumps({'step': 'review', 'message': 'Running external reviewer...'})}\n\n"
            reviewed = yield from _run_with_sse(
                lambda: external_review(paper, draft, cfg), q, "review"
            )
            yield f"data: {json.dumps({'step': 'review', 'message': f'Reviewed: {len(reviewed.claims)} claims after revision'})}\n\n"

            # Build OXA output
            oxa_claims = [_build_oxa_claim(c.model_dump()) for c in reviewed.claims]

            # Step 6: Infer edges between claims
            yield f"data: {json.dumps({'step': 'edges', 'message': f'Inferring relationships between {len(oxa_claims)} claims...'})}\n\n"
            slugs = [c.slug for c in reviewed.claims]
            # Reconcile backend for edge inference: if extract and reconcile models differ in
            # type (e.g. extract=gemini, reconcile=claude), clone cfg with reconcile backend.
            edge_cfg = cfg
            reconcile_backend = _backend_for(req.provider, req.model_reconcile)
            if reconcile_backend != cfg.backend:
                import dataclasses
                edge_cfg = dataclasses.replace(cfg, backend=reconcile_backend)
            edges = infer_edges(reviewed, slugs, edge_cfg)
            oxa_claims = apply_oxa_edges(oxa_claims, edges)
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
    model_reconcile: str = Form("claude-opus-4-8"),
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
            if not api_key and not _is_authorized(api_key, demo_token, request):
                raise ValueError("Not authorized — provide an API key, demo token, or connect from a whitelisted IP")

            cfg = _make_cfg(provider, api_key, model_extract, model_reconcile)
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
                try:
                    import docx
                    doc = docx.Document(str(save_path))
                    full_text = "\n".join(p.text for p in doc.paragraphs)
                except ImportError:
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

            q: queue.Queue = queue.Queue()
            extractions = []
            for i, (agent_name, agent_short) in enumerate([
                ("results", "Results-reader"),
                ("caption", "Caption-reader"),
                ("structure", "Structure-reader"),
            ], 1):
                yield f"data: {json.dumps({'step': 'extract', 'message': f'Agent {i}/3: {agent_short}...'})}\n\n"
                ext = yield from _run_with_sse(
                    lambda an=agent_name: run_agent(an, paper, cfg), q, "extract"
                )
                yield f"data: {json.dumps({'step': 'extract', 'message': f'Agent {i}/3: {agent_short} → {len(ext.claims)} claims'})}\n\n"
                extractions.append(ext)

            results_ext, caption_ext, structure_ext = extractions
            n_candidates = sum(len(e.claims) for e in extractions)
            yield f"data: {json.dumps({'step': 'extract', 'message': f'Total: {n_candidates} candidate claims from 3 agents'})}\n\n"

            # Step 4: Reconciliation
            yield f"data: {json.dumps({'step': 'reconcile', 'message': 'Reconciling — merging 3 agent outputs...'})}\n\n"
            draft = yield from _run_with_sse(
                lambda: reconcile_step(results_ext, caption_ext, structure_ext, cfg,
                                       paper_doi=paper.doi, paper_title=paper.title),
                q, "reconcile"
            )
            yield f"data: {json.dumps({'step': 'reconcile', 'message': f'Reconciled to {len(draft.claims)} claims'})}\n\n"

            # Step 4.5: External review
            yield f"data: {json.dumps({'step': 'review', 'message': 'Running external reviewer...'})}\n\n"
            reviewed = yield from _run_with_sse(
                lambda: external_review(paper, draft, cfg), q, "review"
            )
            yield f"data: {json.dumps({'step': 'review', 'message': f'Reviewed: {len(reviewed.claims)} claims'})}\n\n"

            # Build OXA output
            oxa_claims = [_build_oxa_claim(c.model_dump()) for c in reviewed.claims]

            # Step 6: Infer edges
            yield f"data: {json.dumps({'step': 'edges', 'message': f'Inferring relationships between {len(oxa_claims)} claims...'})}\n\n"
            slugs = [c.slug for c in reviewed.claims]
            edge_cfg = cfg
            reconcile_backend = _backend_for(provider, model_reconcile)
            if reconcile_backend != cfg.backend:
                import dataclasses
                edge_cfg = dataclasses.replace(cfg, backend=reconcile_backend)
            edges = infer_edges(reviewed, slugs, edge_cfg)
            oxa_claims = apply_oxa_edges(oxa_claims, edges)
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
