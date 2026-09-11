"""A run keeps a versioned copy of each single file it produced under runs/.

The site's two-version comparison reads an earlier version's bytes from `<name>.v<N>.<ext>`
beside the current output. `pipeline.keep_versions` is what writes those copies, and this pins
its contract: single files under `runs/` are copied to the version the run recorded, and
nothing else is — a path outside `runs/`, a glob, or a directory is left alone, and no version
is backfilled.

Runs under pytest (``pytest scripts/test_pipeline_versions.py``) or standalone
(``python3 scripts/test_pipeline_versions.py``).
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline


def _touch(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def test_keep_versions_copies_runs_single_files():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _touch(root, "runs/p/reconciler.output.json", '{"v": 2}')
        _touch(root, "runs/p/edge-inference.output.json", "[]")
        rec = {
            "v": 2,
            "out": [
                {"path": "runs/p/reconciler.output.json"},
                {"path": "runs/p/edge-inference.output.json"},
            ],
        }
        made = pipeline.keep_versions(rec, root=str(root))

        assert set(made) == {
            "runs/p/reconciler.output.v2.json",
            "runs/p/edge-inference.output.v2.json",
        }
        # The copy is beside the current output, carries the run's version, and is byte-equal.
        kept = root / "runs/p/reconciler.output.v2.json"
        assert kept.is_file()
        assert kept.read_text(encoding="utf-8") == '{"v": 2}'
        # The layer's own output path is untouched — everything downstream reads it.
        assert (root / "runs/p/reconciler.output.json").is_file()


def test_keep_versions_ignores_non_runs_globs_and_missing():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _touch(root, "claims/p/a-claim.md", "---\n---\n")          # not under runs/
        _touch(root, "runs/p/questions.output.json", "{}")          # a real runs/ file
        rec = {
            "v": 1,
            "out": [
                {"path": "claims/p/a-claim.md"},                    # outside runs/: skip
                {"path": "runs/p/claim-tree.v1/*.md"},              # a glob: skip
                {"path": "runs/p/never-written.output.json"},       # absent: skip
                {"path": "runs/p/questions.output.json"},           # kept
            ],
        }
        made = pipeline.keep_versions(rec, root=str(root))

        assert made == ["runs/p/questions.output.v1.json"]
        assert not (root / "claims/p/a-claim.v1.md").exists()
        assert not (root / "runs/p/never-written.output.v1.json").exists()


def _run():
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"ok   {name}")
            except AssertionError as e:                              # noqa: PERF203
                fails += 1
                print(f"FAIL {name}: {e}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(_run())
