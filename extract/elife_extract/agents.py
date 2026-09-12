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

import copy
import json
import logging
import re
import time
from typing import TYPE_CHECKING

from .config import Config, LITELLM_PREFIX, token_budget
from .prepare import PreparedPaper
from .schema import AgentExtraction, AgentName, CandidateClaim

if TYPE_CHECKING:                      # for the annotations only; never imported at runtime
    from anthropic import Anthropic, AnthropicVertex

logger = logging.getLogger(__name__)


# ── Evidence verification ────────────────────────────────────────────────

_CURLY_QUOTES = str.maketrans({"'": "‘", "’": "'", "“": '"', "”": '"'})
_DASHES = str.maketrans({"–": "-", "—": "-", "―": "-"})


def evidence_found(quote: str, text: str) -> bool:
    """True when the normalised quote appears verbatim in the normalised text.

    Normalises both sides: collapse whitespace, lowercase, map curly quotes and
    the three Unicode dash characters to their ASCII forms, strip a trailing
    ellipsis or full stop from the quote. A quote longer than 300 characters is
    matched on its first 300 — long quotes are almost certainly paraphrases.
    """
    def normalise(s: str) -> str:
        s = s.translate(_CURLY_QUOTES).translate(_DASHES)
        s = " ".join(s.split()).lower()
        return s

    q = normalise(quote).rstrip(".")
    if q.endswith("…") or q.endswith("..."):
        q = q.rstrip(".").rstrip("…").rstrip()
    q = q[:300]
    return q in normalise(text)


def _spans_by_uid(paper: PreparedPaper) -> dict[str, str]:
    """Every span's text keyed by its uid — the ids a reader cites in `span`."""
    from .segment import segment
    return {s.uid: s.text for s in segment(paper, include_methods=True)}


def verify_evidence(quote: str, span: str | None, spans: dict[str, str],
                    slice_text: str) -> tuple[bool, str | None]:
    """Check a quote against its cited span first, then the whole slice; say which matched.

    A quote checked against the one sentence it names is a real hallucination test: the span
    is a single sentence with no bracketed id, so a verbatim quote either is in it or is not.
    The slice fallback keeps the earlier meaning for a reader that cited no span (its slice
    carries no ids) and for a quote of two sentences that no single span holds.
    """
    if span and span in spans and evidence_found(quote, spans[span]):
        return True, "span"
    if evidence_found(quote, slice_text):
        return True, "slice"
    return False, None


# ── Slice mapping: which slice each agent reads ─────────────────────────

# The four prose sections the results reader reads, in reading order. Its slice is these
# sections cut into the numbered spans coverage uses, each sentence shown with its id in front
# so the reader can cite the span its evidence came from.
_RESULTS_SECTIONS = ("abstract", "introduction", "results", "discussion")


def _render_spans(paper: PreparedPaper, sections: tuple[str, ...]) -> str:
    """The given sections as `[uid] sentence` lines, in the segmenter's order."""
    from .segment import segment
    keep = set(sections)
    lines = [f"[{s.uid}] {s.text}" for s in segment(paper, include_methods=True)
             if s.section in keep]
    return "\n".join(lines)


def slice_for_agent(agent: AgentName, paper: PreparedPaper) -> str:
    """Return the paper slice this agent reads.

    The results-reader now gets the abstract, the Introduction, the Results and the Discussion —
    where the hypothesis, the questions and the literature-context premises are stated — with a
    panel inventory in front of it and every sentence numbered by its span id. The caption-reader
    gets figures and tables as before, plus the inventory: a table is a float that reports
    results panel-by-panel and its numbers appear nowhere else. The structure-reader is
    unchanged — methods, appendices and the supplementary inventory, which are structural claims
    about how the work was done.
    """
    if agent == "results":
        inventory = paper.panel_inventory()
        body = _render_spans(paper, _RESULTS_SECTIONS)
        parts = []
        if inventory:
            parts.append(f"# Panel inventory\n\n{inventory}")
        parts.append(f"# Paper (abstract, introduction, results, discussion)\n\n{body}")
        return "\n\n".join(parts)
    if agent == "caption":
        inventory = paper.panel_inventory()
        parts = []
        if inventory:
            parts.append(f"# Panel inventory\n\n{inventory}")
        parts.append(f"# Figure captions\n\n{paper.captions_text}")
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


def raw_slice_for_agent(agent: AgentName, paper: PreparedPaper) -> str:
    """The raw text of an agent's sections, without span ids or the inventory.

    Evidence is quoted verbatim from the prose, not from the id-prefixed rendering the model
    reads, so the slice a quote is checked against must be the raw text — a quote spanning two
    sentences would otherwise fail on the `[uid]` sitting between them.
    """
    if agent == "results":
        blocks = [paper.abstract, paper.introduction_text, paper.results_text,
                  paper.discussion_text]
    elif agent == "caption":
        blocks = [paper.captions_text, paper.tables_text]
    elif agent == "structure":
        blocks = [paper.methods_text, paper.appendix_text, paper.supplementary_text]
    else:
        raise ValueError(f"unknown agent: {agent!r}")
    return "\n\n".join(b for b in blocks if b)


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

    Used for --answer (free text) paths and as a fallback when structured output
    is unavailable or returns unexpected content. The structured output path
    bypasses the need for the salvage logic because the provider enforces valid JSON.

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


# ── Schema helpers for provider-enforced structured outputs ─────────────


def _filter_schema(schema: dict) -> dict:
    """Remove 'Filled by the runner' fields from a JSON schema (root + all $defs).

    The provider enforces the schema the model sees; fields the runner fills must
    not appear in it, or the model will invent values for them that the runner
    then overwrites anyway.
    """
    schema = copy.deepcopy(schema)
    for container in [schema] + list(schema.get("$defs", {}).values()):
        bad = {k for k, v in container.get("properties", {}).items()
               if isinstance(v, dict) and v.get("description", "").startswith("Filled by the runner")}
        if bad:
            for k in bad:
                container.get("properties", {}).pop(k, None)
            if "required" in container:
                container["required"] = [r for r in container["required"] if r not in bad]
    return schema


def _reader_output_schema() -> dict:
    """JSON schema for a reader agent's output: {claims: [CandidateClaim, ...]}.

    The object wrapper is required because most structured-output providers
    (Anthropic, OpenAI) expect a top-level object. _as_claim_list already
    handles the 'claims' key unwrap, so the rest of the parse path is unchanged.
    """
    claim_schema = _filter_schema(CandidateClaim.model_json_schema())
    defs = claim_schema.pop("$defs", {})
    claim_schema.pop("title", None)
    result: dict = {
        "type": "object",
        "properties": {"claims": {"type": "array", "items": claim_schema}},
        "required": ["claims"],
    }
    if defs:
        result["$defs"] = defs
    return result


def _draft_table_schema() -> dict:
    """JSON schema for the reconciler/reviewer output: filtered DraftClaimTable."""
    from .schema import DraftClaimTable
    return _filter_schema(DraftClaimTable.model_json_schema())


def _edge_output_schema() -> dict:
    """JSON schema for the edge-inference output: {edges: [{source, target, relation, why}]}.

    _parse_edges already extracts the inner array from an object wrapper by locating the first
    '[' and the last ']', so this wrapper does not require changes to the parsing path.
    """
    return {
        "type": "object",
        "properties": {
            "edges": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string",
                                   "description": "The source claim's 1-based index number."},
                        "target": {"type": "string",
                                   "description": "The target claim's 1-based index number."},
                        "relation": {"type": "string",
                                     "description": "The relation name from the vocabulary."},
                        "why": {"type": "string",
                                "description": "One sentence explaining the edge."},
                    },
                    "required": ["source", "target", "relation", "why"],
                },
            }
        },
        "required": ["edges"],
    }


# ── Anthropic client (cached per session) ───────────────────────────────


_client_cache: "Anthropic | AnthropicVertex | None" = None


def get_client(cfg: Config) -> "Anthropic | AnthropicVertex":
    """The SDK is imported here rather than at module scope.

    `__init__.py` imports this module to export `call`, so a module-scope
    `from anthropic import ...` made the SDK a hard dependency of importing the package at
    all — including for `elife-extract contract`, which renders a prompt from the vocabulary
    and calls no model. CI installs requirements.txt, which does not carry the SDK, so every
    check that shells into the package has failed since the call paths were merged into one.

    A backend client is needed when a call is made, and only then.
    """
    global _client_cache
    from anthropic import Anthropic, AnthropicVertex      # noqa: PLC0415
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


# Labels that warrant high inference effort (complex synthesis or graph tasks).
_HIGH_EFFORT_LABELS: frozenset[str] = frozenset(
    {"reconciler", "external-reviewer", "parts"}
)


def _effort_for(label: str | None) -> str:
    """Map a call label to an effort level for output_config.

    High: reconciler, external-reviewer, edge-inference*, parts.
    Medium: readers and everything else.
    """
    if label and (label in _HIGH_EFFORT_LABELS or label.startswith("edge-inference")):
        return "high"
    return "medium"


def _supports_adaptive_thinking(model: str) -> bool:
    """True for Claude 4.6+ and 5+ models that use thinking: {type: adaptive}.

    budget_tokens is rejected with HTTP 400 on these models; adaptive is the
    correct form. Pre-4.6 models still use budget_tokens.
    """
    import re
    m = re.search(r"(\d+)-(\d+)", model)
    if m:
        return (int(m.group(1)), int(m.group(2))) >= (4, 6)
    # bare major version, e.g. "claude-opus-5"
    m = re.search(r"-(\d+)$", model)
    return bool(m and int(m.group(1)) >= 5)


def stream_text(
    cfg: Config,
    *,
    model: str,
    system: str,
    user: str,
    max_tokens: int = 32768,
    label: str | None = None,
    output_schema: dict | None = None,
) -> tuple[str, dict]:
    """One model call on whichever backend is configured; returns (text, usage).

    When `output_schema` is given the provider enforces the reply is valid JSON
    matching that schema (Anthropic: output_config.format; litellm: response_format).
    Without it the free-text salvage parser in parse_json_response handles fences
    and bracket mismatches. The log line names which path each reply took.

    The second return value is a usage dict with keys input_tokens, output_tokens,
    cache_read_input_tokens, cache_creation_input_tokens (all int, zero when unknown).

    Every model call in the package goes through here, so adding a provider
    is a config entry rather than a new code path. "vertex" and "anthropic"
    use the Anthropic SDK (streaming, because long claim lists can exceed the
    non-streaming limit); everything else goes through litellm.
    """
    t0 = time.time()
    tag = label or model
    chunks: list[str] = []
    progress = _Progress(tag, t0)
    usage: dict = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0,
    }

    if cfg.backend in ("vertex", "anthropic"):
        client = get_client(cfg)
        # Prompt caching: wrap the system prompt in a content block so the provider
        # can cache it across calls with the same system prompt.
        system_blocks = [{"type": "text", "text": system,
                          "cache_control": {"type": "ephemeral"}}]
        stream_kwargs: dict = dict(
            model=model,
            max_tokens=max_tokens,
            system=system_blocks,
            messages=[{"role": "user", "content": user}],
        )
        # Adaptive thinking for 4.6+ models. budget_tokens is rejected on these.
        if _supports_adaptive_thinking(model):
            stream_kwargs["thinking"] = {"type": "adaptive"}
        # Effort and structured output live in output_config.
        out_cfg: dict = {"effort": _effort_for(label)}
        if output_schema is not None:
            out_cfg["format"] = {
                "type": "json",
                "json_schema": {"name": label or "output", "schema": output_schema},
            }
            logger.info("  %s: sending %dc to %s (%s), structured output active",
                        tag, len(system) + len(user), model, cfg.backend)
        else:
            logger.info("  %s: sending %dc to %s (%s), free-text (salvage parser active)",
                        tag, len(system) + len(user), model, cfg.backend)
        stream_kwargs["output_config"] = out_cfg
        with client.messages.stream(**stream_kwargs) as stream:
            for text in stream.text_stream:
                chunks.append(text)
                progress.tick(len(text))
            final = stream.get_final_message()
        u = final.usage
        usage = {
            "input_tokens": getattr(u, "input_tokens", 0) or 0,
            "output_tokens": getattr(u, "output_tokens", 0) or 0,
            "cache_read_input_tokens": getattr(u, "cache_read_input_tokens", 0) or 0,
            "cache_creation_input_tokens": getattr(u, "cache_creation_input_tokens", 0) or 0,
        }
        logger.info("  %s: usage in=%d out=%d cache_read=%d cache_create=%d",
                    tag, usage["input_tokens"], usage["output_tokens"],
                    usage["cache_read_input_tokens"], usage["cache_creation_input_tokens"])
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
        if output_schema is not None:
            # json_schema is supported by OpenAI-compatible and Gemini backends.
            # Providers that don't support it fall back to json_object (best effort).
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": label or "output",
                    "schema": output_schema,
                    "strict": True,
                },
            }
            logger.info("  %s: sending %dc to %s (%s), structured output active",
                        tag, len(system) + len(user), kwargs["model"], cfg.backend)
        else:
            logger.info("  %s: sending %dc to %s (%s), free-text (salvage parser active)",
                        tag, len(system) + len(user), kwargs["model"], cfg.backend)
        if cfg.backend == "vertex_ai":
            # Gemini on Vertex AI: credentials from environment, project/location explicit.
            kwargs["vertex_project"] = cfg.vertex_project
            kwargs["vertex_location"] = cfg.vertex_region
        elif cfg.api_key:
            kwargs["api_key"] = cfg.api_key
        last_chunk_usage = None
        for chunk in litellm.completion(**kwargs):
            try:
                delta = chunk.choices[0].delta.content
            except (AttributeError, IndexError):
                delta = None
            if delta:
                chunks.append(delta)
                progress.tick(len(delta))
            # Some providers include usage in the final streaming chunk.
            if getattr(chunk, "usage", None):
                last_chunk_usage = chunk.usage

        # Not every provider honours stream=True for every model. Rather than
        # return an empty string and fail later in JSON parsing, retry once
        # without streaming and say so.
        if not chunks:
            logger.warning("  %s: stream returned nothing; retrying unstreamed",
                           tag)
            kwargs["stream"] = False
            resp = litellm.completion(**kwargs)
            chunks.append(resp.choices[0].message.content or "")
            if getattr(resp, "usage", None):
                last_chunk_usage = resp.usage

        if last_chunk_usage is not None:
            usage = {
                "input_tokens": getattr(last_chunk_usage, "prompt_tokens", 0) or 0,
                "output_tokens": getattr(last_chunk_usage, "completion_tokens", 0) or 0,
                "cache_read_input_tokens": 0,
                "cache_creation_input_tokens": 0,
            }

    raw = "".join(chunks)
    progress.done(len(raw))
    return raw, usage


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
                    raw: str, paper: PreparedPaper | None = None) -> AgentExtraction:
    """Validate a raw reader answer into an AgentExtraction.

    Every route in goes through here: the backend, a supplied file, an agent's reply. The
    route differs; the checks do not. When `paper` is given, each claim's `evidence_verified`
    is set by checking the quote against the agent's slice.
    """
    claims = [CandidateClaim(**c) for c in _as_claim_list(parse_json_response(raw), agent)]
    if paper is not None:
        spans = _spans_by_uid(paper)
        text = raw_slice_for_agent(agent, paper)
        for c in claims:
            c.evidence_verified, c.evidence_verified_against = verify_evidence(
                c.evidence, c.span, spans, text)
        verified = sum(1 for c in claims if c.evidence_verified)
        by_span = sum(1 for c in claims if c.evidence_verified_against == "span")
        logger.info("agent=%s evidence verified %d/%d (%d against the cited span)",
                    agent, verified, len(claims), by_span)
    return AgentExtraction(agent=agent, paper_slug=paper_slug, model=model, claims=claims)


def run_agent(
    agent: AgentName,
    paper: PreparedPaper,
    cfg: Config,
    *,
    max_retries: int = 2,
) -> tuple[AgentExtraction, dict]:
    """Run one extraction agent against the paper's slice for that role.

    Returns (AgentExtraction, usage_dict). Raises on unrecoverable error.
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
        ), {}

    schema = _reader_output_schema()
    raw = None
    usage: dict = {}
    for attempt in range(max_retries + 1):
        try:
            logger.info("agent=%s model=%s slice=%dc (streaming)", agent, model, len(paper_slice))
            # Streaming is required by the SDK for max_tokens that may run
            # >10 minutes; we use it unconditionally for safety. The result
            # is identical to a non-streaming call once collected.
            raw, usage = stream_text(
                cfg,
                model=model,
                system=system_prompt,
                user=paper_slice,
                max_tokens=token_budget("reader", cfg.max_claims or 30),
                label=f"{agent}-reader",
                output_schema=schema,
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
        return reader_from_raw(agent, paper.paper_slug, model, raw, paper), usage
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
