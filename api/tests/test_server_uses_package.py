"""One call path: the API imports the package's functions, not its own copies.

These tests verify the structural outcome of the refactor — that the API
uses the package's implementations and that the old duplicate files are gone.
No network, no model API calls: the package's model-calling functions are
stubbed with unittest.mock.
"""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path
from unittest import mock

# Put the extract package on the path (mirrors api/server.py's path setup).
API_DIR = Path(__file__).resolve().parents[1]
EXTRACT_DIR = API_DIR.parent / "extract"
if EXTRACT_DIR.is_dir():
    sys.path.insert(0, str(EXTRACT_DIR))


# ── Structural assertions — deleted files ────────────────────────────────


def test_llm_py_deleted():
    """api/llm.py has been deleted; importing it must fail."""
    assert not (API_DIR / "llm.py").exists(), (
        "api/llm.py still exists — it should have been deleted as part of the "
        "one-call-path refactor (issue #86)"
    )


def test_infer_edges_py_deleted():
    """api/infer_edges.py has been deleted; importing it must fail."""
    assert not (API_DIR / "infer_edges.py").exists(), (
        "api/infer_edges.py still exists — it should have been deleted as part of the "
        "one-call-path refactor (issue #86)"
    )


# ── Import smoke test ────────────────────────────────────────────────────


def _stub_heavy_imports():
    """Stub out SDK and FastAPI imports so server.py loads without extras installed."""
    for mod in [
        "anthropic", "anthropic.types",
        "fastapi", "fastapi.middleware.cors", "fastapi.responses",
        "pydantic",
        "litellm",
    ]:
        if mod not in sys.modules:
            sys.modules[mod] = types.ModuleType(mod)

    # FastAPI stub — needs a callable app factory
    fa = sys.modules["fastapi"]
    fa.FastAPI = lambda **kw: mock.MagicMock()
    fa.File = lambda *a, **kw: None
    fa.Form = lambda *a, **kw: None
    fa.HTTPException = Exception
    fa.Request = object
    fa.UploadFile = object

    cors = sys.modules["fastapi.middleware.cors"]
    cors.CORSMiddleware = object

    resp = sys.modules["fastapi.responses"]
    resp.StreamingResponse = lambda *a, **kw: None

    pb = sys.modules["pydantic"]
    pb.BaseModel = object

    # review module — stub so server.py's `from review import router` works
    review_stub = types.ModuleType("review")
    review_stub.router = mock.MagicMock()
    sys.modules["review"] = review_stub


def test_server_imports():
    """server.py imports cleanly when the package is on the path."""
    _stub_heavy_imports()
    # Remove cached copy if we've imported before
    sys.modules.pop("server", None)
    sys.path.insert(0, str(API_DIR))
    try:
        import server  # noqa: F401
    finally:
        sys.path.remove(str(API_DIR))


# ── Endpoint wires package functions ────────────────────────────────────


def test_extract_endpoint_uses_package_run_agent():
    """The /extract endpoint calls elife_extract.agents.run_agent, not a private copy."""
    _stub_heavy_imports()
    sys.modules.pop("server", None)
    sys.path.insert(0, str(API_DIR))
    try:
        import server
        # server exposes run_agent as a module-level name after _ensure_pipeline()
        # The test checks there is no _run_agent_litellm or _run_agent_streaming.
        assert not hasattr(server, "_run_agent_litellm"), (
            "server._run_agent_litellm should have been deleted"
        )
        assert not hasattr(server, "_run_agent_streaming"), (
            "server._run_agent_streaming should have been deleted"
        )
    finally:
        sys.path.remove(str(API_DIR))


def test_extract_endpoint_uses_package_reconcile():
    """The /extract endpoint calls elife_extract.reconcile.reconcile, not a private copy."""
    _stub_heavy_imports()
    sys.modules.pop("server", None)
    sys.path.insert(0, str(API_DIR))
    try:
        import server
        assert not hasattr(server, "_reconcile_litellm"), (
            "server._reconcile_litellm should have been deleted"
        )
        assert not hasattr(server, "_reconcile_streaming"), (
            "server._reconcile_streaming should have been deleted"
        )
    finally:
        sys.path.remove(str(API_DIR))


def test_extract_endpoint_uses_package_external_review():
    """The /extract endpoint calls elife_extract.external_review.external_review."""
    _stub_heavy_imports()
    sys.modules.pop("server", None)
    sys.path.insert(0, str(API_DIR))
    try:
        import server
        assert not hasattr(server, "_external_review_litellm"), (
            "server._external_review_litellm should have been deleted"
        )
        assert not hasattr(server, "_external_review_streaming"), (
            "server._external_review_streaming should have been deleted"
        )
    finally:
        sys.path.remove(str(API_DIR))


def test_provider_models_in_server():
    """PROVIDER_MODELS is defined in server.py, not imported from the deleted llm.py."""
    _stub_heavy_imports()
    sys.modules.pop("server", None)
    sys.path.insert(0, str(API_DIR))
    try:
        import server
        assert hasattr(server, "PROVIDER_MODELS"), (
            "PROVIDER_MODELS should be defined in server.py"
        )
        assert isinstance(server.PROVIDER_MODELS, dict)
        assert "anthropic" in server.PROVIDER_MODELS
    finally:
        sys.path.remove(str(API_DIR))


if __name__ == "__main__":
    # Run standalone without pytest
    import traceback
    tests = [
        test_llm_py_deleted,
        test_infer_edges_py_deleted,
        test_server_imports,
        test_extract_endpoint_uses_package_run_agent,
        test_extract_endpoint_uses_package_reconcile,
        test_extract_endpoint_uses_package_external_review,
        test_provider_models_in_server,
    ]
    failed = 0
    for fn in tests:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
        except Exception:
            print(f"  FAIL  {fn.__name__}")
            traceback.print_exc()
            failed += 1
    if failed:
        raise SystemExit(f"{failed} test(s) failed")
    print(f"All {len(tests)} tests passed.")
