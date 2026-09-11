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

from .config import Config, LITELLM_PREFIX
from .prepare import PreparedPaper
from .schema import AgentExtraction, AgentName, CandidateClaim

logger = logging.getLogger(__name__)


# ── Slice mapping: which slice each agent reads ─────────────────────────


def slice_for_agent(agent: AgentName, paper: PreparedPaper) -> str:
    """Return the paper slice this agent reads.

    The caption-reader gets tables as well as figures: a table is a float that
    reports results panel-by-panel, and its numbers appear nowhere else in the
    text. The structure-reader gets appendices and the supplementary inventory,
    since supplementary methods and materials are structural claims about how
    the work was done.
    """
    if agent == "results":
        return f"# Abstract\n\n{paper.abstract}\n\n# Results\n\n{paper.results_text}"
    if agent == "caption":
        parts = [f"# Figure captions\n\n{paper.captions_text}"]
        if paper.tables_text:
            parts.append(f"# Tables\n\n{paper.tables_text}")
        return "\n\n".join(parts)
    if agent == "structure":
        parts = [f"# Methods\n\n{paper.methods_text}"]
        if paper.appendix_text:
            parts.append(f"# Appendices\n\n{paper.appendix_text}")
        if paper.supplementary_text:
            parts.append(f"# Supplementary material\n\n{paper.supplementary_text}")
        return "\n\n".join(parts)
    raise ValueError(f"unknown agent: {agent!r}")


# ── Prompt loading ──────────────────────────────────────────────────────


def load_prompt(agent: AgentName, cfg: Config) -> str:
    """The reader's system prompt: its task, then the contract. See prompts.py."""
    from .prompts import prompt
    return prompt(f"{agent}-reader", cfg)


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


def _as_claim_list(parsed, agent: str) -> list:
    """Coerce an agent response to the list of claims the prompt asked for.

    The prompts specify a bare JSON array. Claude models comply; others
    routinely wrap it — {"claims": [...]}, {"results": [...]}, or a lone
    unnamed list value. Since the pipeline is now multi-model, tolerate the
    wrapper rather than failing the run, in the same spirit as the code-fence
    tolerance above. Anything genuinely unusable still raises.
    """
    if isinstance(parsed, list):
        return parsed
    if isinstance(parsed, dict):
        # A single list-valued key is unambiguous whatever it is called.
        lists = {k: v for k, v in parsed.items() if isinstance(v, list)}
        if len(lists) == 1:
            key, value = next(iter(lists.items()))
            logger.warning(
                "agent=%s wrapped its array in an object; unwrapping key %r",
                agent, key,
            )
            return value
        for key in ("claims", "candidate_claims", "candidates", "results", "items"):
            if isinstance(parsed.get(key), list):
                logger.warning(
                    "agent=%s wrapped its array in an object; unwrapping key %r",
                    agent, key,
                )
                return parsed[key]
        # A single claim returned bare, rather than a list of one.
        if "claim" in parsed:
            logger.warning("agent=%s returned a single claim object; wrapping", agent)
            return [parsed]
    raise ValueError(
        f"agent={agent} returned JSON that is not a claim list: "
        f"{type(parsed).__name__}"
        + (f" with keys {sorted(parsed)[:8]}" if isinstance(parsed, dict) else "")
    )


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


def stream_text(
    cfg: Config,
    *,
    model: str,
    system: str,
    user: str,
    max_tokens: int = 32768,
    label: str | None = None,
) -> str:
    """One model call on whichever backend is configured; returns the text.

    Every model call in the package goes through here, so adding a provider
    is a config entry rather than a new code path. "vertex" and "anthropic"
    use the Anthropic SDK (streaming, because long claim lists can exceed the
    non-streaming limit); everything else goes through litellm.
    """
    t0 = time.time()
    tag = label or model
    chunks: list[str] = []
    progress = _Progress(tag, t0)

    if cfg.backend in ("vertex", "anthropic"):
        client = get_client(cfg)
        with client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        ) as stream:
            for text in stream.text_stream:
                chunks.append(text)
                progress.tick(len(text))
    else:
        import litellm

        # litellm logs a banner per call at INFO, which drowns our heartbeat.
        logging.getLogger("LiteLLM").setLevel(logging.WARNING)

        prefix = LITELLM_PREFIX.get(cfg.backend, cfg.backend)
        kwargs: dict = {
            "model": f"{prefix}/{model}",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_tokens": max_tokens,
            "stream": True,
        }
        if cfg.api_key:
            kwargs["api_key"] = cfg.api_key
        logger.info("  %s: sending %dc to %s (%s), awaiting first byte…",
                    tag, len(system) + len(user), kwargs["model"], cfg.backend)
        for chunk in litellm.completion(**kwargs):
            try:
                delta = chunk.choices[0].delta.content
            except (AttributeError, IndexError):
                continue
            if delta:
                chunks.append(delta)
                progress.tick(len(delta))

        # Not every provider honours stream=True for every model. Rather than
        # return an empty string and fail later in JSON parsing, retry once
        # without streaming and say so.
        if not chunks:
            logger.warning("  %s: stream returned nothing; retrying unstreamed",
                           tag)
            kwargs["stream"] = False
            resp = litellm.completion(**kwargs)
            chunks.append(resp.choices[0].message.content or "")

    raw = "".join(chunks)
    progress.done(len(raw))
    return raw


class _Progress:
    """Heartbeat for a long model call.

    A silent multi-minute call is indistinguishable from a hung one. The
    heartbeat is time-based rather than size-based on purpose: a size
    threshold stays silent exactly when the model is slow, which is when you
    most need to know it is alive. Time to first byte is reported separately,
    because that is the number that distinguishes "thinking" from "hung".
    """

    EVERY = 3.0  # seconds between heartbeats

    def __init__(self, tag: str, t0: float):
        self.tag, self.t0, self.n = tag, t0, 0
        self.first = True
        self.t_first = 0.0
        self.last = t0

    def tick(self, n: int) -> None:
        self.n += n
        now = time.time()
        if self.first:
            self.first = False
            self.t_first = now
            logger.info("  %s: first byte at %.1fs", self.tag, now - self.t0)
            self.last = now
            return
        if now - self.last >= self.EVERY:
            # Rate measured from first byte, not from send: including the
            # time-to-first-byte in the denominator makes throughput look
            # like it is accelerating when it is merely averaging away a
            # long prefill.
            gen = now - self.t_first
            rate = self.n / gen if gen > 0 else 0
            logger.info("  %s … %dc, %.0f c/s, %.0fs elapsed",
                        self.tag, self.n, rate, now - self.t0)
            self.last = now

    def done(self, total: int) -> None:
        now = time.time()
        wall = now - self.t0
        gen = now - self.t_first if self.t_first else wall
        rate = total / gen if gen > 0 else 0
        logger.info("  %s done: %dc in %.1fs wall (%.1fs to first byte, "
                    "%.0f c/s generating)", self.tag, total, wall,
                    self.t_first - self.t0 if self.t_first else 0.0, rate)


# ── Single-agent invocation ─────────────────────────────────────────────


def model_for(agent: AgentName, cfg: Config) -> str:
    return {"results": cfg.model_results, "caption": cfg.model_caption,
            "structure": cfg.model_structure}[agent]


def build_reader_request(agent: AgentName, paper: PreparedPaper,
                         cfg: Config) -> tuple[str, str]:
    """The exact (system, user) this reader would send.

    Separated from the call so the question can be asked of something other than the
    configured backend — an analyst, a reasoning agent, another provider — and the answer
    still goes through the same validation. `edge-inference` has had this seam since the run
    where a provider outage took the edges while every other stage succeeded; every layer a
    model answers has the same failure mode and now the same escape.
    """
    return load_prompt(agent, cfg), slice_for_agent(agent, paper)


def reader_from_raw(agent: AgentName, paper_slug: str, model: str,
                    raw: str) -> AgentExtraction:
    """Validate a raw reader answer into an AgentExtraction.

    Every route in goes through here: the backend, a supplied file, an agent's reply. The
    route differs; the checks do not.
    """
    claims = [CandidateClaim(**c) for c in _as_claim_list(parse_json_response(raw), agent)]
    return AgentExtraction(agent=agent, paper_slug=paper_slug, model=model, claims=claims)


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
    model = model_for(agent, cfg)
    system_prompt, paper_slice = build_reader_request(agent, paper, cfg)

    if not paper_slice.strip() or len(paper_slice) < 200:
        logger.warning(
            "agent=%s slice is short (%d chars); skipping invocation",
            agent,
            len(paper_slice),
        )
        return AgentExtraction(
            agent=agent, paper_slug=paper.paper_slug, model=model, claims=[]
        )

    raw = None
    for attempt in range(max_retries + 1):
        try:
            logger.info("agent=%s model=%s slice=%dc (streaming)", agent, model, len(paper_slice))
            # Streaming is required by the SDK for max_tokens that may run
            # >10 minutes; we use it unconditionally for safety. The result
            # is identical to a non-streaming call once collected.
            raw = stream_text(
                cfg,
                model=model,
                system=system_prompt,
                user=paper_slice,
                max_tokens=32768,  # 30+ claims with verbatim quotes routinely
                                   # exceed 10k tokens; budget for headroom
                label=f"{agent}-reader",
            )
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
        return reader_from_raw(agent, paper.paper_slug, model, raw)
    except Exception as parse_err:
        # Keep the raw reply before re-raising: a reply that failed to parse is the only
        # evidence of what went wrong, and it is gone the moment this returns.
        from pathlib import Path
        debug_path = Path(f"/tmp/elife-extract-debug-{agent}-{paper.paper_slug}.txt")
        debug_path.write_text(raw)
        logger.error(
            "agent=%s answer unusable: %s. Raw reply saved to %s (%d chars)",
            agent, parse_err, debug_path, len(raw),
        )
        logger.error("first 500 chars: %r", raw[:500])
        logger.error("last 500 chars: %r", raw[-500:])
        raise


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
