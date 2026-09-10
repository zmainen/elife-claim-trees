"""Unit tests for how `run` composes extract → write → verify-refs.

No LLM and no network: the three pipeline steps `extract` calls are stubbed,
and what is checked is the wiring between subcommands rather than what any of
them computes.

`run` used to null out `args.draft` before calling `cmd_write`, which then did
`Path(None)` and raised — so the subcommand the README and the walkthrough both
name as the end-to-end path could not complete. The extraction stage now hands
the next two stages the draft it wrote and the slug it derived, and that is what
these tests pin down.

Runs under pytest (``pytest tests/test_cli_composition.py``) or standalone
(``python tests/test_cli_composition.py``).
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest import mock

from elife_extract import agents as agents_mod
from elife_extract import cli
from elife_extract import prepare as prepare_mod
from elife_extract import reconcile as reconcile_mod

SLUG = "gadeke-2026-guilt-insula"
DOI = "10.7554/eLife.105391"


def _stub_paper():
    return mock.MagicMock(
        paper_slug=SLUG, title="Contributions of insula and superior temporal sulcus",
        doi=DOI, extraction_path="jats", abstract="a", results_text="r",
        captions_text="c", methods_text="m", panel_ids=["fig1"],
    )


def _stub_json_model(**attrs):
    m = mock.MagicMock(**attrs)
    m.model_dump_json.return_value = "{}"
    return m


def _run(argv, on_write, on_verify=lambda args: 0):
    """Run `cli.cmd_run` with the model-calling stages stubbed out."""
    agent = _stub_json_model(claims=[])
    draft = _stub_json_model(claims=[], paper_slug=SLUG, paper_doi=DOI)
    with mock.patch.object(prepare_mod, "prepare", return_value=_stub_paper()), \
         mock.patch.object(agents_mod, "run_all_agents", return_value=(agent, agent, agent)), \
         mock.patch.object(reconcile_mod, "reconcile", return_value=draft), \
         mock.patch.object(cli, "cmd_write", on_write), \
         mock.patch.object(cli, "cmd_verify_refs", on_verify):
        return cli.cmd_run(cli.build_parser().parse_args(argv))


def _argv(tmp: Path):
    return ["run", "--doi", DOI, "--corpus-dir", str(tmp), "--output-dir", str(tmp / "out")]


def test_run_hands_write_an_existing_draft():
    """The draft `write` receives is the file `extract` just wrote, not None."""
    seen = {}

    def on_write(args):
        seen["draft"] = args.draft
        return 0

    with tempfile.TemporaryDirectory() as tmp:
        rc = _run(_argv(Path(tmp)), on_write)
        # Inside the block: the temporary directory is gone once it closes.
        assert seen["draft"] is not None, "write was handed no draft"
        assert Path(seen["draft"]).is_file(), "the draft path does not name a file"
        assert Path(seen["draft"]).name == f"draft-{SLUG}.json"

    assert rc == 0


def test_run_hands_verify_refs_the_slug():
    """`verify-refs` needs the slug `prepare` derived; nothing else knows it."""
    seen = {}

    with tempfile.TemporaryDirectory() as tmp:
        rc = _run(_argv(Path(tmp)),
                  on_write=lambda args: 0,
                  on_verify=lambda args: seen.__setitem__("paper", args.paper) or 0)

    assert rc == 0
    assert seen["paper"] == SLUG


def test_run_bypasses_the_review_gate():
    """`run` is the unattended path: Step 5 is auto-approve, never interactive."""
    seen = {}

    with tempfile.TemporaryDirectory() as tmp:
        _run(_argv(Path(tmp)), on_write=lambda args: seen.__setitem__("mode", args.review_mode) or 0)

    assert seen["mode"] == "auto-approve"


def test_run_stops_when_write_fails():
    """A failing stage ends the run; verify-refs must not run on a bad write."""
    ran = {"verify": False}

    with tempfile.TemporaryDirectory() as tmp:
        rc = _run(_argv(Path(tmp)),
                  on_write=lambda args: 7,
                  on_verify=lambda args: ran.__setitem__("verify", True) or 0)

    assert rc == 7
    assert not ran["verify"]


def test_output_dir_flag_places_the_draft():
    """--output-dir is a real flag on extract and run, not just an env var."""
    seen = {}

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "elsewhere"
        _run(["run", "--doi", DOI, "--corpus-dir", tmp, "--output-dir", str(out)],
             on_write=lambda args: seen.__setitem__("draft", args.draft) or 0)
        assert Path(seen["draft"]).parent == out.resolve()


def test_prompts_dir_flag_is_honored():
    """--prompts-dir was accepted and then ignored; Config must respect it."""
    from elife_extract.config import Config

    with tempfile.TemporaryDirectory() as tmp:
        args = cli.build_parser().parse_args(
            ["extract", "--doi", DOI, "--corpus-dir", tmp, "--prompts-dir", tmp])
        assert Config.from_args(args).prompts_dir == Path(tmp).resolve()


# ── Standalone runner (no pytest required) ────────────────────────────────

if __name__ == "__main__":
    import traceback

    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except Exception:
            print(f"FAIL  {t.__name__}")
            traceback.print_exc()
    print(f"\n{passed}/{len(tests)} passed")
    raise SystemExit(0 if passed == len(tests) else 1)
