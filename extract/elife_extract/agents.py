"""Steps 2-3 — Abstract scan and three-agent extraction.

Step 2 — Abstract scan: a single Claude call that reads the abstract
and identifies 2-4 top-level claims (the paper's main bets). Currently
folded into the Results-reader run (the Results-reader sees the abstract
already and surfaces these as hypothesis/synthesis claims). The dedicated
Step 2 call is reserved for future iterations that want the slugs ahead
of the full extraction pass.

Step 3 — Three independent extractions:
  Agent A — Results reader   → reads abstract + results prose
  Agent B — Caption reader   → reads figure captions panel-by-panel
  Agent C — Structure reader → reads methods + supplements + code

Each agent's prompt is loaded from prompts/{role}-reader.md (or from
prompts/<variant>/{role}-reader.md when --prompt-variant is set). The
agent receives its slice of the paper as the user message; the prompt
serves as the system message. Output is a JSON list parsed via the
schema.AgentExtraction model.

Agents currently run sequentially — Phase D's acceptance is "produces a
draft table"; speed is a Phase H/I optimization. Three Sonnet calls in
sequence at ~20-30s each is acceptable. A future async refactor can run
them concurrently when cost/latency budgets demand it.
"""

from __future__ import annotations

import json
import logging
import re
import time

from anthropic import Anthropic, AnthropicVertex

from .config import Config
from .prepare import PreparedPaper
from .schema import AgentExtraction, AgentName, CandidateClaim

logger = logging.getLogger(__name__)


# ── Slice mapping: which slice each agent reads ─────────────────────────


def slice_for_agent(agent: AgentName, paper: PreparedPaper) -> str:
    """Return the paper slice this agent reads."""
    if agent == "results":
        return f"# Abstract\n\n{paper.abstract}\n\n# Results\n\n{paper.results_text}"
    if agent == "caption":
        return f"# Figure captions\n\n{paper.captions_text}"
    if agent == "structure":
        return f"# Methods\n\n{paper.methods_text}"
    raise ValueError(f"unknown agent: {agent!r}")


# ── Prompt loading ──────────────────────────────────────────────────────


def load_prompt(agent: AgentName, cfg: Config) -> str:
    """Load the system prompt for an agent from disk."""
    path = cfg.prompt_path(f"{agent}-reader")
    if not path.is_file():
        raise FileNotFoundError(
            f"Prompt file not found for agent {agent!r} (variant {cfg.prompt_variant!r}): {path}"
        )
    return path.read_text()


# ── JSON parsing with code-fence tolerance ──────────────────────────────


_JSON_FENCE_OPEN = re.compile(r"^```(?:json)?\s*\n?", re.IGNORECASE)
_JSON_FENCE_CLOSE = re.compile(r"\n?```\s*$")


def parse_json_response(raw: str) -> list[dict] | dict:
    """Parse a JSON response from the model, tolerating markdown fences.

    Models sometimes wrap JSON output in ```json ... ``` despite explicit
    instructions not to. Strip leading and trailing fences independently
    (some models close with ``` while others get truncated before they
    can; handling both bounds independently means we don't choke when
    only one is present).
    """
    raw = raw.strip()
    raw = _JSON_FENCE_OPEN.sub("", raw, count=1)
    raw = _JSON_FENCE_CLOSE.sub("", raw, count=1).rstrip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try to extract just the JSON array or object
        for start_char, end_char in [('[', ']'), ('{', '}')]:
            start = raw.find(start_char)
            if start == -1:
                continue
            # Find the last valid closing bracket
            depth = 0
            last_valid = start
            in_string = False
            escape = False
            for i in range(start, len(raw)):
                c = raw[i]
                if escape:
                    escape = False
                    continue
                if c == '\\':
                    escape = True
                    continue
                if c == '"' and not escape:
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if c == start_char:
                    depth += 1
                elif c == end_char:
                    depth -= 1
                    if depth == 0:
                        last_valid = i
                        break
            if last_valid > start:
                try:
                    return json.loads(raw[start:last_valid+1])
                except json.JSONDecodeError:
                    pass
        # Last resort: try to salvage truncated JSON by closing brackets
        if '[' in raw:
            truncated = raw[raw.find('['):]
            # Close any open strings, objects, arrays
            truncated = truncated.rstrip(', \n\t')
            if not truncated.endswith(']'):
                # Remove the last incomplete item
                last_brace = truncated.rfind('}')
                if last_brace > 0:
                    truncated = truncated[:last_brace+1] + ']'
                    try:
                        return json.loads(truncated)
                    except json.JSONDecodeError:
                        pass
        raise


# ── Anthropic client (cached per session) ───────────────────────────────


_client_cache: Anthropic | AnthropicVertex | None = None


def get_client(cfg: Config) -> Anthropic | AnthropicVertex:
    global _client_cache
    if _client_cache is None:
        if cfg.backend == "anthropic" and cfg.anthropic_api_key:
            _client_cache = Anthropic(api_key=cfg.anthropic_api_key)
        else:
            _client_cache = AnthropicVertex(
                region=cfg.vertex_region, project_id=cfg.vertex_project
            )
    return _client_cache


def reset_client():
    """Clear cached client — call when API key changes between requests."""
    global _client_cache
    _client_cache = None


# ── Single-agent invocation ─────────────────────────────────────────────


def run_agent(
    agent: AgentName,
    paper: PreparedPaper,
    cfg: Config,
    *,
    max_retries: int = 2,
) -> AgentExtraction:
    """Run one extraction agent against the paper's slice for that role.

    Returns the validated AgentExtraction. Raises on unrecoverable error.
    Retries with exponential backoff on rate limits (429).
    """
    model = {
        "results": cfg.model_results,
        "caption": cfg.model_caption,
        "structure": cfg.model_structure,
    }[agent]

    system_prompt = load_prompt(agent, cfg)
    paper_slice = slice_for_agent(agent, paper)

    if not paper_slice.strip() or len(paper_slice) < 200:
        logger.warning(
            "agent=%s slice is short (%d chars); skipping invocation",
            agent,
            len(paper_slice),
        )
        return AgentExtraction(
            agent=agent, paper_slug=paper.paper_slug, model=model, claims=[]
        )

    client = get_client(cfg)

    raw = None
    for attempt in range(max_retries + 1):
        try:
            logger.info("agent=%s model=%s slice=%dc (streaming)", agent, model, len(paper_slice))
            # Streaming is required by the SDK for max_tokens that may run
            # >10 minutes; we use it unconditionally for safety. The result
            # is identical to a non-streaming call once collected.
            text_chunks: list[str] = []
            with client.messages.stream(
                model=model,
                max_tokens=32768,  # 30+ claims with verbatim quotes routinely
                                   # exceed 10k tokens; budget for headroom
                system=system_prompt,
                messages=[{"role": "user", "content": paper_slice}],
            ) as stream:
                for text in stream.text_stream:
                    text_chunks.append(text)
            raw = "".join(text_chunks)
            break
        except Exception as e:
            status = getattr(e, "status_code", None)
            if status == 429 and attempt < max_retries:
                wait = 2 ** (attempt + 1)
                logger.warning("agent=%s rate limited; sleeping %ds", agent, wait)
                time.sleep(wait)
                continue
            raise

    assert raw is not None
    try:
        parsed = parse_json_response(raw)
    except Exception as parse_err:
        # Save raw response for debugging then re-raise with context
        from pathlib import Path
        debug_path = Path(f"/tmp/elife-extract-debug-{agent}-{paper.paper_slug}.txt")
        debug_path.write_text(raw)
        logger.error(
            "agent=%s JSON parse failed: %s. Raw response saved to %s (%d chars)",
            agent, parse_err, debug_path, len(raw),
        )
        logger.error("first 500 chars: %r", raw[:500])
        logger.error("last 500 chars: %r", raw[-500:])
        raise

    if not isinstance(parsed, list):
        raise ValueError(
            f"agent={agent} returned non-list JSON: {type(parsed).__name__}"
        )

    claims = [CandidateClaim(**c) for c in parsed]
    return AgentExtraction(
        agent=agent, paper_slug=paper.paper_slug, model=model, claims=claims
    )


def run_all_agents(
    paper: PreparedPaper, cfg: Config
) -> tuple[AgentExtraction, AgentExtraction, AgentExtraction]:
    """Run Results, Caption, Structure agents in sequence.

    The three agents are independent — none of them sees another's output
    before submitting. Returns a tuple in (results, caption, structure)
    order. Sequential rather than concurrent for now; Phase H/I optimization.
    """
    results = run_agent("results", paper, cfg)
    logger.info("results-reader produced %d claims", len(results.claims))

    caption = run_agent("caption", paper, cfg)
    logger.info("caption-reader produced %d claims", len(caption.claims))

    structure = run_agent("structure", paper, cfg)
    logger.info("structure-reader produced %d claims", len(structure.claims))

    return results, caption, structure
