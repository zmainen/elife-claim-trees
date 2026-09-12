"""elife-extract — 8-step claim induction pipeline for eLife papers.

Methodology authority: ~/Projects/mainenlab/elife-claim-trees/docs/method.md
HaaK job: home/collabs/elife/claim-trees/jobs/extract-cli.md
"""

__version__ = "0.1.0"

# One call path: every model call in the package and in the API goes through
# `stream_text`.  The API imports `call` (thin alias) and `prompt` so the
# duplicate in api/llm.py and api/server.py can be removed.
from .agents import stream_text as call  # noqa: F401
from .prompts import prompt              # noqa: F401
