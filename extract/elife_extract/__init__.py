"""elife-extract — 8-step claim induction pipeline for eLife papers.

Methodology authority: ~/Projects/mainenlab/elife-claim-trees/docs/method.md
HaaK job: home/collabs/elife/claim-trees/jobs/extract-cli.md
"""

__version__ = "0.1.0"

# One call path: every model call in the package and in the API goes through `stream_text`.
# The API imports `call` (a thin alias) and `prompt`, so the duplicates in api/llm.py and
# api/server.py could be removed.
#
# Resolved on first use rather than at import. Exporting them eagerly made importing the
# package import `agents`, which imports `prepare`, which imports httpx and lxml — so
# `elife-extract contract`, which renders a prompt from the vocabulary and calls no model,
# could not start without the Anthropic SDK and an HTTP client installed. CI installs
# requirements.txt, which carries neither, and every check that shells into the package has
# failed since the call paths were merged into one. What a call needs is loaded when a call
# is made.
_LAZY = {"call": (".agents", "stream_text"), "prompt": (".prompts", "prompt")}


def __getattr__(name: str):
    if name in _LAZY:
        from importlib import import_module
        module, attr = _LAZY[name]
        return getattr(import_module(module, __name__), attr)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted([*globals(), *_LAZY])
