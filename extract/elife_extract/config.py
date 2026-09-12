"""Configuration — paths, models, env-var contracts.

The CLI is configured via a combination of CLI args (highest priority),
environment variables, and defaults. This module centralizes the contract
so every subcommand resolves the same way.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

# ── Default model selection ──────────────────────────────────────────────
# Three extraction agents on Sonnet (each reading their slice).
# Reconciliation on Opus (the harder synthesis step).
# Mixed-model pattern matches panel-claim-unification.md Phase 1's
# measured ~$4.48/paper cost.
#
# These are the `standard` profile's models, and they name the current generation:
# `claude-sonnet-5` for the readers, `claude-opus-5` for the synthesis steps. The generation
# is a logical id; BACKEND_MODEL_OVERRIDES below maps it to whatever a given backend actually
# serves. `--profile` picks a different set (see PROFILES); an explicit `--model-*` overrides
# either.

DEFAULT_MODEL_RESULTS = "claude-sonnet-5"
DEFAULT_MODEL_CAPTION = "claude-sonnet-5"
DEFAULT_MODEL_STRUCTURE = "claude-sonnet-5"
DEFAULT_MODEL_RECONCILE = "claude-opus-5"

# ── Per-backend model id overrides ───────────────────────────────────────
# A profile names a generation as a logical id (`claude-opus-5`), but not every backend serves
# every generation. The Vertex project this repo uses (cr-mainen / europe-west1) has the 4.6
# generation enabled and not the 5 generation, so a run routed through Vertex must ask for the
# ids Vertex actually serves or the call 404s. The 4.6 ids are therefore the Vertex entries
# here — the last generation Vertex has — and stay until the project enables 5. The Anthropic
# direct path and the litellm backends receive the logical id unchanged.

BACKEND_MODEL_OVERRIDES: dict[str, dict[str, str]] = {
    "vertex": {
        "claude-sonnet-5": "claude-sonnet-4-6",
        "claude-opus-5": "claude-opus-4-6",
    },
}


def _backend_model(backend: str, model: str) -> str:
    """Map a logical model id to what *backend* actually serves (identity when no override)."""
    return BACKEND_MODEL_OVERRIDES.get(backend, {}).get(model, model)

# ── Vertex AI defaults (HaaK canonical: cr-mainen / europe-west1) ────────
DEFAULT_VERTEX_PROJECT = "cr-mainen"
DEFAULT_VERTEX_REGION = "europe-west1"

# ── Prompt variant directory ─────────────────────────────────────────────
# CLI flag --prompt-variant selects a subdirectory. The default variant
# lives at prompts/ root (results-reader.md, caption-reader.md,
# structure-reader.md). Variants live at prompts/<variant>/<role>.md.

DEFAULT_PROMPT_VARIANT = "default"

# ── Model profiles ────────────────────────────────────────────────────────
# A profile is one coherent choice of models, prompt variant, chunking, output enforcement and
# effort — the axes the model sweep (issue #85) varies. `--profile` selects one on every
# model-answered subcommand and on `evaluate`; the fields it resolves to are read by config,
# the CLI and the layer runners, so a run's whole shape follows from one word.
#
#   readers / reasoner   the logical model id for the three readers, and for the synthesis
#                        steps (reconcile, external-review, edge-inference, parts, questions).
#                        A backend override (above) maps the id to what the backend serves.
#   variant              the prompt-variant directory; task files there override, the contract
#                        is inherited. `default` is today's tasks.
#   per_arc              edge inference runs one call per hypothesis arc rather than over the
#                        whole table — a weaker model does better with one job per call.
#   per_figure_captions  the caption reader runs once per figure with its panels enumerated.
#   output_format        provider-enforced output: json_schema (strict), json_object (json
#                        mode, best-effort), or none (the prompt is dumped and answered
#                        elsewhere — the subagent path, where no provider enforces anything).
#   reader_effort /      inference effort for the readers, and for the synthesis steps.
#   reasoner_effort
#   thinking             adaptive thinking on (Claude 4.6+/5); ignored where unsupported.
#   backend              a fallback backend when none is given — `open` implies litellm.
#
# The table follows issue #85. `subagent` is the zero-cost path: every step is a dumped prompt
# answered by a Claude Code subagent, so it enforces nothing and names the answering model in
# the ledger's `by`.


@dataclass(frozen=True)
class Profile:
    readers: str
    reasoner: str
    variant: str = DEFAULT_PROMPT_VARIANT
    per_arc: bool = False
    per_figure_captions: bool = False
    output_format: str = "json_schema"
    reader_effort: str = "medium"
    reasoner_effort: str = "high"
    thinking: bool = True
    backend: str | None = None


PROFILES: dict[str, Profile] = {
    # Frontier: one model, lean tasks, whole slices, high/xhigh effort. Over-prescriptive
    # prompts measurably cost accuracy on this tier, so the scaffolding is stripped to the
    # contract plus a one-page task.
    "frontier": Profile(
        readers="claude-opus-5", reasoner="claude-opus-5", variant="frontier",
        reader_effort="high", reasoner_effort="xhigh",
    ),
    # Standard (default): the current generation with today's tasks — the signal-phrase tables
    # and the quantity ceiling the standard tier needs because it over-splits.
    "standard": Profile(
        readers="claude-sonnet-5", reasoner="claude-opus-5", variant="default",
        reader_effort="medium", reasoner_effort="high",
    ),
    # Open: local/hosted open-weight models via litellm, with the work chunked so each call has
    # one job, the full example set, and json mode enforced by the provider.
    "open": Profile(
        readers="deepseek-chat", reasoner="deepseek-chat", variant="open",
        per_arc=True, per_figure_captions=True, output_format="json_object",
        reader_effort="medium", reasoner_effort="medium", thinking=False,
        backend="deepseek",
    ),
    # Subagent: the zero-cost path. A Claude Code subagent answers each dumped prompt; nothing
    # is enforced by a provider, and the ledger's `by` names the model that actually answered.
    # Models mirror `standard` because that is what today's recorded runs stand in for.
    "subagent": Profile(
        readers="claude-sonnet-5", reasoner="claude-opus-5", variant="default",
        output_format="none",
    ),
}

PROFILE_NAMES = tuple(PROFILES)


def resolve_profile(name: str, backend: str | None = None) -> Profile:
    """The Profile named, or ValueError naming the ones that exist.

    `backend` is unused here — the backend override is applied to the resolved model ids by
    Config, which knows the backend in force — but is accepted so callers can pass it without
    caring whether the mapping happens here or there.
    """
    if name not in PROFILES:
        raise ValueError(
            f"unknown profile {name!r}; choose one of {', '.join(PROFILE_NAMES)}")
    return PROFILES[name]


# ── Backend routing ──────────────────────────────────────────────────────
# "vertex" and "anthropic" call the Anthropic SDK directly. Any other value
# is passed to litellm, whose provider prefix is looked up below — so
# OpenRouter, OpenAI and Gemini need no code of their own.

DEFAULT_BACKEND = "vertex"

# ── Per-layer output-token budgets ──────────────────────────────────────
# Budget = tokens_per_claim * n_claims, clamped to [min_tokens, max_tokens].
# Fixed-budget layers use tokens_per_claim = 0 and return max_tokens directly.
#
# Rationale for each row:
#   reader           450 t/claim — verbatim evidence quotes are long
#   reconciler       900 t/claim — richer format: sources, evidence_by_agent, span_by_agent
#   external-reviewer 900 t/claim — same format as reconciler (revises the draft in place)
#   edge-inference    60 t/claim — each edge is a short 4-field object
#   questions/parts/summaries/synthesis/abstract-map — prose outputs; small fixed ceiling
#   stance            fixed 4096 — a small set of ruled-out alternative claims

_BUDGET_TABLE: dict[str, tuple[int, int, int]] = {
    # (tokens_per_claim, min_tokens, max_tokens)
    "reader":             (450,     8_192, 32_768),
    "reconciler":         (900,     8_192, 32_768),
    "external-reviewer":  (900,     8_192, 32_768),
    "edge-inference":     ( 60,     4_096, 32_768),
    "questions":          (  0,       512,  2_048),
    "parts":              (  0,       512,  2_048),
    "summaries":          (  0,       512,  4_096),
    "synthesis":          (  0,       512,  4_096),
    "abstract-map":       (  0,       512,  2_048),
    "stance":             (  0,     1_024,  4_096),
}


def token_budget(label: str, n_claims: int = 25) -> int:
    """Return a max_tokens budget for *label* scaled to *n_claims*.

    For layers whose budget scales with output size, *n_claims* should be the
    expected number of output claims (reader) or the input draft's claim count
    (reconciler/reviewer/edges).  Fixed-budget layers ignore *n_claims*.

    The result is always within the [min_tokens, max_tokens] interval declared
    in _BUDGET_TABLE, which prevents both reservation errors (HTTP 402 when the
    provider reserves more than the account balance) and truncated output.
    """
    per, lo, hi = _BUDGET_TABLE.get(label, (450, 8_192, 32_768))
    raw = per * max(n_claims, 1) if per else hi
    return max(lo, min(hi, raw))


LITELLM_PREFIX = {
    "openrouter": "openrouter",
    "openai": "openai",
    "google": "gemini",
    "groq": "groq",
    "together": "together_ai",
    "deepseek": "deepseek",
    # Gemini models served via Google Vertex AI (as opposed to direct Google AI API).
    # Use backend="vertex_ai" when the model is Gemini but credentials are Vertex credentials.
    "vertex_ai": "vertex_ai",
}

BACKEND_ENV_KEY = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "openai": "OPENAI_API_KEY",
    "google": "GEMINI_API_KEY",
    "groq": "GROQ_API_KEY",
    "together": "TOGETHER_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
}


@dataclass
class Config:
    """Runtime configuration resolved from CLI args + env + defaults."""

    # Model routing
    model_results: str = DEFAULT_MODEL_RESULTS
    model_caption: str = DEFAULT_MODEL_CAPTION
    model_structure: str = DEFAULT_MODEL_STRUCTURE
    model_reconcile: str = DEFAULT_MODEL_RECONCILE

    # Vertex AI
    vertex_project: str = DEFAULT_VERTEX_PROJECT
    vertex_region: str = DEFAULT_VERTEX_REGION

    # Direct Anthropic API (alternative to Vertex)
    anthropic_api_key: str | None = None
    # "vertex" and "anthropic" use the Anthropic SDK directly; every other
    # value ("openrouter", "openai", "google", …) is routed through litellm.
    backend: str = DEFAULT_BACKEND
    api_key: str | None = None

    # Paths (resolved at runtime, not import-time)
    # `root` is the corpus repository — the directory `pipeline/layers.yaml` resolves its
    # declared paths against. Every layer runner writes under it, so the paths a run produces
    # are the paths the ledger hashes.
    root: Path | None = None
    corpus_dir: Path | None = None
    prompts_dir: Path | None = None
    output_dir: Path | None = None

    # Variant selection
    prompt_variant: str = DEFAULT_PROMPT_VARIANT
    reconcile_strategy: str = "confidence-tagged"

    # Profile: the one word that sets models, variant, chunking, enforcement and effort.
    # `None` means no profile was named and the per-field defaults above stand.
    profile: str | None = None
    per_arc: bool = False
    per_figure_captions: bool = False
    # Provider-enforced output mode: "json_schema", "json_object", or "none" (answered
    # elsewhere, so nothing to enforce).
    output_format: str = "json_schema"
    reader_effort: str = "medium"
    reasoner_effort: str = "high"
    thinking: bool = True

    # Behavioral knobs
    max_claims: int | None = None
    retry_on_thin: bool = True
    infer_edges: bool = True
    edges_json: str | None = None

    # Provided fields, populated by from_args()
    extras: dict = field(default_factory=dict)

    @classmethod
    def from_args(cls, args) -> "Config":
        """Build a Config from argparse Namespace, falling back to env then defaults.

        Precedence is CLI arg > env var > the named profile > the per-field default. A
        `--profile` sits between the environment and the defaults: it moves the whole set of
        fields at once, and an explicit `--model-*`, `--backend` or `--prompt-variant` still
        wins over what the profile would have chosen.
        """
        cfg = cls()

        # Profile: resolved first, so its fields can serve as the fallback for everything
        # below. An unknown name is left on cfg.profile and reported by validate(), rather
        # than raised here, so the CLI prints one clean error instead of a traceback.
        cfg.profile = getattr(args, "profile", None)
        prof: Profile | None = PROFILES.get(cfg.profile) if cfg.profile else None

        # Backend selection. Anything other than "vertex"/"anthropic" is routed
        # through litellm, so openrouter/openai/google work without new code. The `open`
        # profile implies a litellm backend, offered here only as a fallback.
        cfg.backend = (
            getattr(args, "backend", None)
            or os.environ.get("ELIFE_EXTRACT_BACKEND")
            or (prof.backend if prof else None)
            or DEFAULT_BACKEND
        )

        # Models (CLI > env > profile > default), then mapped to what the backend serves.
        cfg.model_results = _backend_model(cfg.backend,
            getattr(args, "model_results", None)
            or os.environ.get("ELIFE_EXTRACT_MODEL_RESULTS")
            or (prof.readers if prof else None)
            or DEFAULT_MODEL_RESULTS
        )
        cfg.model_caption = _backend_model(cfg.backend,
            getattr(args, "model_caption", None)
            or os.environ.get("ELIFE_EXTRACT_MODEL_CAPTION")
            or (prof.readers if prof else None)
            or DEFAULT_MODEL_CAPTION
        )
        cfg.model_structure = _backend_model(cfg.backend,
            getattr(args, "model_structure", None)
            or os.environ.get("ELIFE_EXTRACT_MODEL_STRUCTURE")
            or (prof.readers if prof else None)
            or DEFAULT_MODEL_STRUCTURE
        )
        cfg.model_reconcile = _backend_model(cfg.backend,
            getattr(args, "model_reconcile", None)
            or os.environ.get("ELIFE_EXTRACT_MODEL_RECONCILE")
            or (prof.reasoner if prof else None)
            or DEFAULT_MODEL_RECONCILE
        )

        # Chunking, enforcement and effort follow the profile when one is named.
        if prof:
            cfg.per_arc = prof.per_arc
            cfg.per_figure_captions = prof.per_figure_captions
            cfg.output_format = prof.output_format
            cfg.reader_effort = prof.reader_effort
            cfg.reasoner_effort = prof.reasoner_effort
            cfg.thinking = prof.thinking
        cfg.api_key = (
            getattr(args, "api_key", None)
            or os.environ.get(BACKEND_ENV_KEY.get(cfg.backend, ""))
            or None
        )
        # Kept for backwards compatibility with the anthropic-only path.
        cfg.anthropic_api_key = cfg.anthropic_api_key or (
            cfg.api_key if cfg.backend == "anthropic" else None
        )

        # Vertex AI
        cfg.vertex_project = (
            getattr(args, "vertex_project", None)
            or os.environ.get("VERTEX_PROJECT_ID")
            or DEFAULT_VERTEX_PROJECT
        )
        cfg.vertex_region = (
            getattr(args, "vertex_region", None)
            or os.environ.get("VERTEX_REGION")
            or DEFAULT_VERTEX_REGION
        )

        # Paths. The package ships inside the corpus repo as extract/elife_extract/, so the
        # repository root is two directories up — the same guess prompts_dir already makes.
        root = (getattr(args, "root", None)
                or os.environ.get("ELIFE_CLAIM_TREES_ROOT")
                or Path(__file__).resolve().parents[2])
        cfg.root = Path(root).expanduser().resolve()

        corpus = getattr(args, "corpus_dir", None) or os.environ.get("ELIFE_CORPUS_DIR")
        cfg.corpus_dir = (Path(corpus).expanduser().resolve() if corpus
                          else cfg.root / "claims")

        cfg.infer_edges = not getattr(args, "no_infer_edges", False)
        cfg.edges_json = getattr(args, "edges_json", None)

        # Default prompts dir is the package's sibling prompts/ directory
        prompts = getattr(args, "prompts_dir", None)
        cfg.prompts_dir = (Path(prompts).expanduser().resolve() if prompts
                           else Path(__file__).resolve().parent.parent / "prompts")

        output = getattr(args, "output_dir", None) or os.environ.get("ELIFE_EXTRACT_OUTPUT")
        cfg.output_dir = Path(output).expanduser().resolve() if output else Path.cwd() / "out"

        # Variants. An explicit --prompt-variant wins; otherwise the profile's variant; then
        # the default. (The CLI passes None when the flag is absent, so the profile is reached.)
        cfg.prompt_variant = (
            getattr(args, "prompt_variant", None)
            or (prof.variant if prof else None)
            or DEFAULT_PROMPT_VARIANT
        )
        cfg.reconcile_strategy = getattr(args, "reconcile_strategy", None) or "confidence-tagged"

        # Knobs
        cfg.max_claims = getattr(args, "max_claims", None)
        cfg.retry_on_thin = getattr(args, "retry_on_thin", True)

        return cfg

    def prompt_path(self, agent: str) -> Path:
        """Resolve the prompt file for a given agent in the active variant."""
        if self.prompt_variant == DEFAULT_PROMPT_VARIANT:
            return self.prompts_dir / f"{agent}.md"
        return self.prompts_dir / self.prompt_variant / f"{agent}.md"

    # Which call labels are synthesis steps rather than readers. Effort follows the profile's
    # reader_effort / reasoner_effort by this split, and the labels match those stream_text is
    # given (`{agent}-reader`, `reconciler`, `external-reviewer`, `edge-inference*`, …).
    _REASONER_LABELS = frozenset(
        {"reconciler", "external-reviewer", "parts"})

    def effort_for(self, label: str | None) -> str:
        """The inference effort for a call, from the profile's reader/reasoner split."""
        if label and (label in self._REASONER_LABELS or label.startswith("edge-inference")):
            return self.reasoner_effort
        return self.reader_effort

    def validate(self) -> list[str]:
        """Return a list of error strings, or empty if valid."""
        errors = []
        if self.profile is not None and self.profile not in PROFILES:
            errors.append(
                f"unknown profile {self.profile!r}; choose one of {', '.join(PROFILE_NAMES)}")
        if self.root is None or not self.root.is_dir():
            errors.append(
                f"root not found: {self.root}. Pass --root, or set ELIFE_CLAIM_TREES_ROOT, "
                f"to the corpus repository pipeline/layers.yaml resolves its paths against."
            )
        if self.prompts_dir is None or not self.prompts_dir.is_dir():
            errors.append(
                f"prompts_dir invalid or missing: {self.prompts_dir}"
            )
        return errors
