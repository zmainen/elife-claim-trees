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

DEFAULT_MODEL_RESULTS = "claude-sonnet-4-6"
DEFAULT_MODEL_CAPTION = "claude-sonnet-4-6"
DEFAULT_MODEL_STRUCTURE = "claude-sonnet-4-6"
DEFAULT_MODEL_RECONCILE = "claude-opus-4-6"

# ── Vertex AI defaults (HaaK canonical: cr-mainen / europe-west1) ────────
DEFAULT_VERTEX_PROJECT = "cr-mainen"
DEFAULT_VERTEX_REGION = "europe-west1"

# ── Prompt variant directory ─────────────────────────────────────────────
# CLI flag --prompt-variant selects a subdirectory. The default variant
# lives at prompts/ root (results-reader.md, caption-reader.md,
# structure-reader.md). Variants live at prompts/<variant>/<role>.md.

DEFAULT_PROMPT_VARIANT = "default"

# ── Backend routing ──────────────────────────────────────────────────────
# "vertex" and "anthropic" call the Anthropic SDK directly. Any other value
# is passed to litellm, whose provider prefix is looked up below — so
# OpenRouter, OpenAI and Gemini need no code of their own.

DEFAULT_BACKEND = "vertex"

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

    # Behavioral knobs
    max_claims: int | None = None
    retry_on_thin: bool = True
    infer_edges: bool = True
    edges_json: str | None = None

    # Provided fields, populated by from_args()
    extras: dict = field(default_factory=dict)

    @classmethod
    def from_args(cls, args) -> "Config":
        """Build a Config from argparse Namespace, falling back to env then defaults."""
        cfg = cls()

        # Models (CLI > env > default)
        cfg.model_results = (
            getattr(args, "model_results", None)
            or os.environ.get("ELIFE_EXTRACT_MODEL_RESULTS")
            or DEFAULT_MODEL_RESULTS
        )
        cfg.model_caption = (
            getattr(args, "model_caption", None)
            or os.environ.get("ELIFE_EXTRACT_MODEL_CAPTION")
            or DEFAULT_MODEL_CAPTION
        )
        cfg.model_structure = (
            getattr(args, "model_structure", None)
            or os.environ.get("ELIFE_EXTRACT_MODEL_STRUCTURE")
            or DEFAULT_MODEL_STRUCTURE
        )
        cfg.model_reconcile = (
            getattr(args, "model_reconcile", None)
            or os.environ.get("ELIFE_EXTRACT_MODEL_RECONCILE")
            or DEFAULT_MODEL_RECONCILE
        )

        # Backend selection. Anything other than "vertex"/"anthropic" is routed
        # through litellm, so openrouter/openai/google work without new code.
        cfg.backend = (
            getattr(args, "backend", None)
            or os.environ.get("ELIFE_EXTRACT_BACKEND")
            or DEFAULT_BACKEND
        )
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

        # Variants
        cfg.prompt_variant = getattr(args, "prompt_variant", None) or DEFAULT_PROMPT_VARIANT
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

    def validate(self) -> list[str]:
        """Return a list of error strings, or empty if valid."""
        errors = []
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
