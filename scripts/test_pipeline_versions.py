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


def _decl(root: Path):
    """A tiny two-layer declaration under `root`, with its reads on disk, loaded with
    pipeline pointed at `root` so digests and the corpus ledger resolve there."""
    _touch(root, "scripts/relations.py", "EDGE_KEYS = ['supports']\n")
    (root / "pipeline").mkdir(parents=True, exist_ok=True)
    (root / "pipeline" / "layers.yaml").write_text(
        "version: 1\n"
        "layers:\n"
        "  - id: claim-format\n"
        "    kind: feature\n"
        "    scope: corpus\n"
        "    reads: []\n"
        "  - id: relation-vocab\n"
        "    kind: question\n"
        "    scope: corpus\n"
        "    needs: [claim-format]\n"
        "    reads: [scripts/relations.py]\n"
        "  - id: claim-tree\n"
        "    kind: step\n"
        "    scope: paper\n"
        "    needs: [relation-vocab]\n"
        "    produces: ['claims/{paper}/*.md']\n",
        encoding="utf-8")
    pipeline.ROOT = str(root)
    return pipeline.load(str(root / "pipeline" / "layers.yaml"))


def test_declaration_version_is_a_function_of_entry_and_reads():
    old = pipeline.ROOT
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            decl = _decl(root)
            rv = decl["by_id"]["relation-vocab"]
            v1 = pipeline.declaration_version(rv)
            assert v1 == pipeline.declaration_version(rv)          # deterministic
            # A read file it names moves the version — the same machinery staleness uses.
            _touch(root, "scripts/relations.py", "EDGE_KEYS = ['supports', 'tests']\n")
            assert pipeline.declaration_version(rv) != v1
    finally:
        pipeline.ROOT = old


def test_declaration_state_open_accepted_superseded():
    old = pipeline.ROOT
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            decl = _decl(root)
            rv = decl["by_id"]["relation-vocab"]

            # Never approved → open, and claim-tree is provisional on the corpus decisions.
            ds = pipeline.declaration_state(decl)
            assert ds["relation-vocab"]["scheme"] == "open"
            assert ds["claim-tree"].get("provisional_on") == ["claim-format", "relation-vocab"]

            # Approve claim-format and the current relation-vocab version → accepted.
            pipeline.approve_declaration("claim-format",
                                         pipeline.declaration_version(decl["by_id"]["claim-format"]),
                                         by="curator")
            ver = pipeline.declaration_version(rv)
            pipeline.approve_declaration("relation-vocab", ver, by="curator", note="ruled")
            ds = pipeline.declaration_state(decl)
            assert ds["relation-vocab"]["scheme"] == "accepted"
            assert ds["relation-vocab"]["approved"]["by"] == "curator"
            # claim-tree now waits on nothing — both corpus deps are accepted.
            assert "provisional_on" not in ds["claim-tree"]

            # Move the declaration past what was accepted → proposed, marked superseded.
            _touch(root, "scripts/relations.py", "EDGE_KEYS = ['supports', 'opposes']\n")
            ds = pipeline.declaration_state(decl)
            assert ds["relation-vocab"]["scheme"] == "proposed"
            assert ds["relation-vocab"]["approved"]["superseded"] is True
            # And claim-tree is provisional again, on relation-vocab alone.
            assert ds["claim-tree"].get("provisional_on") == ["relation-vocab"]

            # The ruling is one line in the corpus-level ledger, in the approval shape.
            recs = pipeline.read_corpus_approvals()
            assert [r["declaration"] for r in recs] == ["claim-format", "relation-vocab"]
            assert recs[1]["version"] == ver and recs[1]["note"] == "ruled"
    finally:
        pipeline.ROOT = old


def test_status_proposed_reads_as_proposed_until_accepted():
    old = pipeline.ROOT
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            decl = _decl(root)
            decl["by_id"]["relation-vocab"]["status"] = "proposed"
            ds = pipeline.declaration_state(decl)
            assert ds["relation-vocab"]["scheme"] == "proposed"
            pipeline.approve_declaration("relation-vocab",
                                         pipeline.declaration_version(decl["by_id"]["relation-vocab"]),
                                         by="curator")
            assert pipeline.declaration_state(decl)["relation-vocab"]["scheme"] == "accepted"
    finally:
        pipeline.ROOT = old


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
