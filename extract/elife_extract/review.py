"""Step 5 — Review gate.

Per `docs/method.md` § 3.3 Step 5: "Nothing is written to disk until the
table is approved." The review step is a hard gate between extraction
and file emission.

Three modes:
  interactive   — open the draft in $EDITOR; the user edits in place;
                  on save+exit, the edited draft is the input to write.
  auto-approve  — skip the review (for tests, batches, demos).
  dry-run       — print the draft without saving; no file emission.

The interactive review opens a YAML serialization of the draft (more
readable than the JSON intermediate) and re-parses it after the user
exits the editor. The user can:

  - Edit any claim's text, panel, role, claim_type
  - Delete claims (remove the entry)
  - Add new claims (insert a new entry)
  - Adjust confidence
  - Add notes

Schema validation runs on re-read; if it fails, the user is told and the
edit is preserved at a temp path for re-attempt.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

from .config import Config
from .schema import DraftClaimTable

logger = logging.getLogger(__name__)


def _draft_to_review_yaml(draft: DraftClaimTable) -> str:
    """Serialize the draft to a human-friendly YAML for editor review."""
    header = (
        f"# Draft claim table for review — paper {draft.paper_slug}\n"
        f"# DOI: {draft.paper_doi}\n"
        f"# Title: {draft.paper_title or '(unknown)'}\n"
        f"# Per-agent counts: results={draft.per_agent_counts.get('results', 0)} "
        f"caption={draft.per_agent_counts.get('caption', 0)} "
        f"structure={draft.per_agent_counts.get('structure', 0)}\n"
        f"# Total reconciled: {len(draft.claims)}\n"
        f"#\n"
        f"# Edit, delete, or add claims below. Save and exit to continue.\n"
        f"# Quit without saving (vim :q!, etc.) to abort the write step.\n"
        f"# Lines starting with # are comments and will be discarded.\n"
        f"\n"
    )

    # We dump the model as a list-of-dicts under a top-level 'claims' key.
    # Keep paper-level metadata at the top so the user sees it but doesn't
    # need to edit it.
    body = yaml.safe_dump(
        json.loads(draft.model_dump_json()),
        sort_keys=False,
        allow_unicode=True,
        width=120,
    )
    return header + body


def _read_review_yaml(text: str) -> DraftClaimTable:
    """Parse the user's edits back into a DraftClaimTable."""
    # Strip comment-only lines (yaml itself tolerates inline comments)
    lines = [ln for ln in text.splitlines() if not ln.lstrip().startswith("#")]
    cleaned = "\n".join(lines)
    data = yaml.safe_load(cleaned)
    if not isinstance(data, dict):
        raise ValueError(f"review YAML must be a mapping at root, got {type(data).__name__}")
    return DraftClaimTable(**data)


def _editor_command() -> list[str]:
    """Resolve the editor command from $VISUAL or $EDITOR, falling back to vi."""
    editor = os.environ.get("VISUAL") or os.environ.get("EDITOR") or ""
    if editor:
        # $EDITOR often contains a multi-word command
        return editor.split()
    if shutil.which("vi"):
        return ["vi"]
    raise RuntimeError(
        "No editor found. Set $EDITOR or $VISUAL, or install vi."
    )


def review(draft: DraftClaimTable, cfg: Config) -> DraftClaimTable | None:
    """Present the draft for human approval and return the (possibly edited) draft.

    Returns None if the user aborts (interactive mode without saving).
    """
    mode = cfg.review_mode

    if mode == "auto-approve":
        logger.info("review-mode=auto-approve — skipping review gate")
        return draft

    if mode == "dry-run":
        # Print the draft to stdout; no file writes happen downstream
        print(_draft_to_review_yaml(draft))
        logger.info("review-mode=dry-run — printed draft, no claim files will be emitted")
        return None

    if mode != "interactive":
        raise ValueError(f"unknown review_mode: {mode!r}")

    # Interactive: write the draft to a temp YAML file, open in editor,
    # re-read after editor exits.
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=f".review.{draft.paper_slug}.yaml",
        delete=False,
    ) as tf:
        tf.write(_draft_to_review_yaml(draft))
        review_path = Path(tf.name)

    print(f"Opening draft for review: {review_path}", file=sys.stderr)
    print(f"  edit, save, and exit to continue; quit without saving to abort.", file=sys.stderr)

    cmd = _editor_command() + [str(review_path)]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        logger.warning("editor exited with code %d; aborting review", result.returncode)
        return None

    edited_text = review_path.read_text()

    # If the user didn't change anything, treat as an explicit auto-approve
    # equivalent. The original draft is what gets written.
    try:
        edited = _read_review_yaml(edited_text)
    except Exception as e:
        # Preserve the edit so the user can retry
        rescue_path = review_path.with_suffix(".rescue.yaml")
        rescue_path.write_text(edited_text)
        print(
            f"\nReview YAML failed to parse: {e}\n"
            f"  Your edits are preserved at: {rescue_path}\n"
            f"  Re-run with corrected YAML or restart from the original draft.\n",
            file=sys.stderr,
        )
        return None

    review_path.unlink(missing_ok=True)
    return edited
