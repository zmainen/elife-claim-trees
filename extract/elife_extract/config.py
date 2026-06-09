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

# ── Vertex AI defaults (HAAK canonical: cr-mainen / europe-west1) ────────
DEFAULT_VERTEX_PROJECT = "cr-mainen"
DEFAULT_VERTEX_REGION = "europe-west1"

# ── Prompt variant directory ─────────────────────────────────────────────
# CLI flag --prompt-variant selects a subdirectory. The default variant
# lives at prompts/ root (results-reader.md, caption-reader.md,
# structure-reader.md). Variants live at prompts/<variant>/<role>.md.

DEFAULT_PROMPT_VARIANT = "default"


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
    backend: str = "vertex"  # "vertex" or "anthropic"

    # Paths (resolved at runtime, not import-time)
    corpus_dir: Path | None = None
    prompts_dir: Path | None = None
    output_dir: Path | None = None

    # Variant selection
    prompt_variant: str = DEFAULT_PROMPT_VARIANT
    reconcile_strategy: str = "confidence-tagged"
    review_mode: str = "interactive"

    # Behavioral knobs
    max_claims: int | None = None
    retry_on_thin: bool = True

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

        # Paths
        corpus = getattr(args, "corpus_dir", None) or os.environ.get("ELIFE_CORPUS_DIR")
        if corpus:
            cfg.corpus_dir = Path(corpus).expanduser().resolve()

        # Default prompts dir is the package's sibling prompts/ directory
        cfg.prompts_dir = Path(__file__).resolve().parent.parent / "prompts"

        output = getattr(args, "output_dir", None) or os.environ.get("ELIFE_EXTRACT_OUTPUT")
        cfg.output_dir = Path(output).expanduser().resolve() if output else Path.cwd() / "out"

        # Variants
        cfg.prompt_variant = getattr(args, "prompt_variant", None) or DEFAULT_PROMPT_VARIANT
        cfg.reconcile_strategy = getattr(args, "reconcile_strategy", None) or "confidence-tagged"
        cfg.review_mode = getattr(args, "review_mode", None) or "interactive"

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
        if self.corpus_dir is None:
            errors.append(
                "corpus_dir not set. Pass --corpus-dir or set ELIFE_CORPUS_DIR environment variable."
            )
        if self.prompts_dir is None or not self.prompts_dir.is_dir():
            errors.append(
                f"prompts_dir invalid or missing: {self.prompts_dir}"
            )
        return errors
