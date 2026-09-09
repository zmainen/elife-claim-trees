"""Step 6 — Dependency mapping: infer typed edges between reconciled claims.

`docs/method.md` § 3 Step 6 describes this step as the analyst's, and until
now the writer emitted `belongings: []` with a TODO. But the corpus's ~1,100
edges are the deductive layer — the hypothesis→prediction→evidence spine, the
scope constraints, the `requires` chains that propagate invalidity — and a
pipeline that reproduces claims without edges reproduces the nodes of the
graph and none of its structure.

This module closes that gap. It is adapted from `api/infer_edges.py`, which
has been serving the web demo; moving it into the package lets the CLI use
the same inference the API already does.

Two conventions matter and are not obvious:

1. **Where an edge is stored depends on its type.** The site's build step
   (`site/scripts/build-data.js`) reads `requires` and `supports` from the
   `belongings:` list, and every other relation from a top-level key. That
   split is undocumented but consistent across the corpus (requires: 148 in
   belongings vs 30 top-level; supports: 126 vs 25). We follow what the site
   reads, so generated files render like curated ones.

2. **Deduction is reciprocal.** A hypothesis carries `entails:` to its
   prediction and the prediction carries `derived-from:` back. The model is
   asked for one direction; we synthesise the other, because the site's
   hierarchical numbering (H1, H1.P1, H1.P1.E1) walks `derived-from`.
"""

from __future__ import annotations

import json
import logging
import re

from .agents import stream_text
from .config import Config
from .schema import DraftClaimTable, ReconciledClaim

logger = logging.getLogger(__name__)


# ── Vocabulary ───────────────────────────────────────────────────────────
# The prompt speaks CiTO/claimrel; the corpus uses bare relation names.

CITO_TO_CORPUS = {
    "cito:supports": "supports",
    "claimrel:tests": "tests",
    "claimrel:entails": "entails",
    "claimrel:requires": "requires",
    "claimrel:scopes": "scopes",
    "cito:usesMethodIn": "enables-method",
    "cito:disagreesWith": "dissociates-with",
    "claimrel:interprets": "interprets",
    "claimrel:rulesOut": "rules-out",
}

# Stored as {relation, target} entries under `belongings:`; everything else
# becomes a top-level list key. See module docstring.
BELONGINGS_RELATIONS = {"requires", "supports"}

# Deduction is recorded from both ends.
RECIPROCAL = {"entails": "derived-from"}


EDGE_PROMPT = """You are analyzing the argument structure of a scientific paper.
You have a list of claims extracted from the paper. Your job is to identify the logical
relationships between them.

Each claim is numbered. Refer to claims ONLY by their number.

For each relationship you find, specify:
- source: the NUMBER of the claim that carries the relationship
- target: the NUMBER of the claim it relates to
- relationType: one of these typed edges:

RELATIONSHIP TYPES:
- cito:supports — provides factual or intellectual support
- claimrel:tests — submits to empirical test (an empirical claim testing a prediction)
- claimrel:entails — logically entails (a hypothesis entailing its predictions)
- claimrel:requires — logically depends on as a prerequisite
- claimrel:scopes — delimits the domain of applicability
- cito:usesMethodIn — uses a method from this claim
- cito:disagreesWith — dissociates with (results that separate variables)
- claimrel:interprets — offers a theoretical reading
- claimrel:rulesOut — eliminates as a viable hypothesis (control results)

RULES:
- hypothesis claims typically ENTAIL prediction claims
- prediction claims are typically TESTED BY empirical claims
- scope claims typically SCOPE many other claims
- methodological claims are typically REQUIRED BY empirical claims
- control claims typically RULE OUT alternatives
- synthesis/interpretation claims typically aggregate multiple empirical claims

Return a JSON array of edges, using claim numbers:
[{"source": 12, "target": 3, "relationType": "claimrel:tests"}, ...]

Only include relationships you are confident about. It's better to miss an edge than to invent one.
"""


def _claim_digest(claims: list[ReconciledClaim], slugs: list[str]) -> str:
    """Render the claim list for the prompt, numbered.

    Claims are identified by number, not slug. Slugs invite paraphrase: given
    `[hypothesis] social-decisions-under-risk-engage`, the model reads the
    bracketed role as part of the name and returns invented identifiers — the
    bare word "hypothesis" as a source, or "prediction-" prefixed onto a
    target. Every edge then fails validation. An integer cannot be paraphrased.
    """
    lines = []
    for i, c in enumerate(claims, 1):
        panel = f", panel {c.panel}" if c.panel else ""
        lines.append(f"{i}. ({c.role}{panel}) {c.claim[:220]}")
    return "\n".join(lines)


def _resolve(ref, slugs: list[str]) -> str | None:
    """Resolve a model-supplied claim reference to a slug.

    Accepts the 1-based index the prompt asks for, and falls back to matching
    a slug string — exact, then after stripping a role prefix the model may
    have prepended.
    """
    if isinstance(ref, bool):
        return None
    if isinstance(ref, int):
        return slugs[ref - 1] if 1 <= ref <= len(slugs) else None
    if not isinstance(ref, str):
        return None
    s = ref.strip()
    if s.isdigit():
        n = int(s)
        return slugs[n - 1] if 1 <= n <= len(slugs) else None
    if s in slugs:
        return s
    for prefix in ("hypothesis-", "prediction-", "empirical-", "control-",
                   "scope-", "claim-", "synthesis-", "interpretation-"):
        if s.startswith(prefix) and s[len(prefix):] in slugs:
            return s[len(prefix):]
    return None


def infer_edges(
    draft: DraftClaimTable, slugs: list[str], cfg: Config
) -> list[dict]:
    """Ask the model for typed relations between the draft's claims.

    Returns [{source, target, relation}] in corpus vocabulary. Edges naming
    an unknown slug, or pointing at themselves, are dropped rather than
    written — an invented target is worse than a missing edge.
    """
    user = (
        f"Here are {len(draft.claims)} claims from the paper:\n\n"
        f"{_claim_digest(draft.claims, slugs)}\n\n"
        "Identify the relationships between these numbered claims. "
        "Refer to claims by number. Return JSON array only."
    )

    raw = stream_text(
        cfg,
        model=cfg.model_reconcile,
        system=EDGE_PROMPT,
        user=user,
        label="edge-inference",
    )

    match = re.search(r"\[.*\]", raw, re.DOTALL)
    if not match:
        logger.warning("edge inference returned no JSON array; no edges written")
        return []
    try:
        parsed = json.loads(match.group(0))
    except json.JSONDecodeError:
        logger.warning("edge inference JSON parse failed; no edges written")
        return []

    edges: list[dict] = []
    seen: set[tuple[str, str, str]] = set()
    unknown = 0
    for e in parsed:
        if not isinstance(e, dict):
            continue
        src = _resolve(e.get("source"), slugs)
        tgt = _resolve(e.get("target"), slugs)
        rel = CITO_TO_CORPUS.get(e.get("relationType", ""), e.get("relationType", ""))
        if not src or not tgt or src == tgt or not rel:
            unknown += 1
            continue
        if rel not in set(CITO_TO_CORPUS.values()):
            unknown += 1
            continue
        key = (src, tgt, rel)
        if key not in seen:
            seen.add(key)
            edges.append({"source": src, "target": tgt, "relation": rel})

    # Synthesise the reciprocal of each deductive edge.
    for e in list(edges):
        inverse = RECIPROCAL.get(e["relation"])
        if not inverse:
            continue
        key = (e["target"], e["source"], inverse)
        if key not in seen:
            seen.add(key)
            edges.append(
                {"source": e["target"], "target": e["source"], "relation": inverse}
            )

    by_type: dict[str, int] = {}
    for e in edges:
        by_type[e["relation"]] = by_type.get(e["relation"], 0) + 1
    logger.info(
        "edge inference: %d edges across %d types (%d dropped as invalid): %s",
        len(edges), len(by_type), unknown,
        ", ".join(f"{k}={v}" for k, v in sorted(by_type.items(), key=lambda x: -x[1])),
    )
    return edges


def edges_for_slug(edges: list[dict], slug: str) -> tuple[dict, list[dict]]:
    """Split one claim's outgoing edges into (top-level keys, belongings).

    Returns ({relation: [targets]}, [{relation, target}]) ready to merge into
    the claim's frontmatter.
    """
    top: dict[str, list[str]] = {}
    belongings: list[dict] = []
    for e in edges:
        if e["source"] != slug:
            continue
        if e["relation"] in BELONGINGS_RELATIONS:
            belongings.append({"relation": e["relation"], "target": e["target"]})
        else:
            top.setdefault(e["relation"], []).append(e["target"])
    return top, belongings
