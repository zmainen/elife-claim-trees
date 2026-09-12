"""One loader for every prompt: the role's task, then the contract it shares with the others.

Three loaders existed — `load_prompt`, `load_reconciler_prompt`, `load_reviewer_prompt` —
each resolving the variant directory its own way, and a fourth path read the edge prompt at
import time and ignored the variant altogether. This is the one place that knows what a role
is sent, and `files()` is what the declaration in `pipeline/layers.yaml` has to agree with:
the test in `tests/test_prompt_contract.py` checks that a layer's `reads` lists exactly the
files its runner composes, so a prompt file cannot be sent without being hashed into the run.
"""

from __future__ import annotations

from pathlib import Path

from .config import DEFAULT_PROMPT_VARIANT, Config
from .contract import CONTRACT_DIR

# role → (task file, contract files), all relative to the prompts directory.
_VOCAB = f"{CONTRACT_DIR}/vocabulary.md"
_CANDIDATE = f"{CONTRACT_DIR}/schema-candidate.md"
_DRAFT = f"{CONTRACT_DIR}/schema-draft.md"

ROLES: dict[str, tuple[str, list[str]]] = {
    "results-reader": ("results-reader.md", [_VOCAB, _CANDIDATE]),
    "caption-reader": ("caption-reader.md", [_VOCAB, _CANDIDATE]),
    "structure-reader": ("structure-reader.md", [_VOCAB, _CANDIDATE]),
    "reconciler": ("reconciler.md", [_VOCAB, _DRAFT]),
    "external-reviewer": ("external-reviewer.md", [_VOCAB, _DRAFT]),
    # Edge inference reads the vocabulary — where the relations, their directions and the
    # confusable pairs are defined — but not the claim schema: it returns edges, not claims.
    "edge-inference": ("edge-inference.md", [_VOCAB]),
    "coverage-adjudicator": ("coverage-adjudicator.md", []),
    # Questions gets the vocabulary — it needs the definition of a hypothesis and of a question
    # — but not the claim schema: it returns questions, not claims.
    "questions": ("questions.md", [_VOCAB]),
    # Parts gets the vocabulary — it needs the definition of `part-of` and how it differs from
    # `supports` — but not the claim schema: it returns `part-of` edges, not claims.
    "parts": ("parts.md", [_VOCAB]),
    # Summaries and synthesis reason about the claims by role — hypothesis, empirical, synthesis
    # — so they get the vocabulary that defines a role, but not the claim schema: they return
    # prose, not claims.
    "summaries": ("summaries.md", [_VOCAB]),
    "synthesis": ("synthesis.md", [_VOCAB]),
    # Abstract-map returns a mapping keyed by slug and sentence number, not a judgement about
    # roles, so it gets its task alone.
    "abstract-map": ("abstract-map.md", []),
}


def files(role: str) -> list[str]:
    """Every file the role's prompt is composed from, task first, relative to prompts/."""
    task, contract = ROLES[role]
    return [task, *contract]


def declared_reads(role: str) -> list[str]:
    """The same list as repository-relative paths — what `layers.yaml` must declare."""
    return [f"extract/prompts/{f}" for f in files(role)]


def _resolve(cfg: Config, rel: str) -> Path:
    """A variant may override any file; what it does not override comes from the default."""
    if cfg.prompt_variant != DEFAULT_PROMPT_VARIANT:
        p = cfg.prompts_dir / cfg.prompt_variant / rel
        if p.is_file():
            return p
    return cfg.prompts_dir / rel


def prompt(role: str, cfg: Config) -> str:
    """The system prompt for a role: its task, then the contract, separated by a rule."""
    if role not in ROLES:
        raise KeyError(f"unknown prompt role {role!r}; known: {', '.join(ROLES)}")
    parts = []
    for rel in files(role):
        p = _resolve(cfg, rel)
        if not p.is_file():
            hint = (f" — run `elife-extract contract --write`" if rel.startswith(CONTRACT_DIR)
                    else "")
            raise FileNotFoundError(f"prompt file for {role!r} not found: {p}{hint}")
        parts.append(p.read_text(encoding="utf-8").strip())
    return "\n\n---\n\n".join(parts) + "\n"
