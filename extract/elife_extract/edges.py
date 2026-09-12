"""Step 6 — Dependency mapping: infer typed edges between reconciled claims.

`docs/method.md` § 3 Step 6 describes this step as the analyst's, and until
now the writer emitted `belongings: []` with a TODO. But the corpus's ~1,100
edges are the deductive layer — the hypothesis→prediction→evidence spine, the
scope constraints, the `requires` chains that propagate invalidity — and a
pipeline that reproduces claims without edges reproduces the nodes of the
graph and none of its structure.

This module closes that gap. The prompt is rebuilt on the contract (#83): it
speaks the corpus's own relation vocabulary, is given each claim's role, panel,
stance, sentence, cited spans and the readers' evidence quotes rather than a
220-character stub, and asks for a one-sentence `why` per edge. Validation is
where the direction rules bite — the same rules `scripts/relations.py` states
beside each relation and `scripts/check_relations.py` enforces on the corpus.

Four conventions matter and are not obvious:

1. **The vocabulary is loaded, not copied.** `scripts/relations.py` is the one
   place the relations, their directions and the confusable pairs are declared;
   this module loads it the way `contract.py` does, so the prompt, the checker
   and this validator cannot drift. There is no CiTO map any more — five corpus
   relations (`validates`, `confirms`, `extends`, `refutes`, `qualifies`) could
   not be emitted through it, and `part-of` post-dates it.

2. **Direction is checked, not trusted.** A relation name says two claims are
   related, not which is which. `tests` runs empirical/control → prediction;
   `entails` from a hypothesis; `scopes` from a scope claim; `rules-out` and the
   other contrary relations only at a claim the paper does not assert; `part-of`
   only where it forms no cycle and no second whole. An edge that breaks its
   rule is dropped with a logged reason, never silently kept.

3. **Deduction is reciprocal.** A hypothesis carries `entails:` to its
   prediction and the prediction carries `derived-from:` back; a hypothesis or
   result `predicts` an observation and the observation `confirms` it. The model
   is asked for one direction and forbidden the other; we synthesise it, because
   the site's hierarchical numbering (H1, H1.P1, H1.P1.E1) walks `derived-from`.

4. **Where an edge is stored depends on its type.** The site's build step
   (`site/scripts/build-data.js`) reads `requires` and `supports` from the
   `belongings:` list, and every other relation from a top-level key. We follow
   what the site reads, so generated files render like curated ones.
"""

from __future__ import annotations

import importlib.util
import json
import logging
import re
from pathlib import Path

from .agents import _edge_output_schema, stream_text
from .config import Config
from .schema import DraftClaimTable, ReconciledClaim

logger = logging.getLogger(__name__)


# ── Vocabulary, loaded from the one place it is declared ───────────────────


def _load_relations():
    """`scripts/relations.py`, loaded by path — the single source of the edge vocabulary.

    The same load `contract.py` and the `parts` layer do: the package cannot import a script
    that sits beside it, and copying the vocabulary here is the drift this whole module exists
    to remove.
    """
    p = Path(__file__).resolve().parents[2] / "scripts" / "relations.py"
    spec = importlib.util.spec_from_file_location("relations", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


_REL = _load_relations()
EDGE_KEYS = set(_REL.EDGE_KEYS)
# The contrary relations — those that assert the target is false — may not be aimed at a claim
# the paper asserts. Imported so this validator and `check_relations.py` read one set.
CONTRARY = set(_REL.CONTRARY)

# Stored as {relation, target} entries under `belongings:`; everything else becomes a
# top-level list key. See module docstring.
BELONGINGS_RELATIONS = {"requires", "supports"}

# Deduction is recorded from both ends. The model is asked for the left key and forbidden the
# right one, which we write mechanically as its reciprocal.
RECIPROCAL = {"entails": "derived-from", "predicts": "confirms"}
NEVER_EMITTED = set(RECIPROCAL.values())          # {"derived-from", "confirms"}

# The role a relation's source must have, where the direction rule fixes it. `rules-out` runs
# from the control or evidence that eliminates a rival, so its source is a control or an
# empirical claim — the `stance` layer aims one from a named control at the alternative it kills,
# and a rules-out from anything else is dropped the way a mis-directed `tests` is.
_SOURCE_ROLE = {"entails": {"hypothesis"}, "scopes": {"scope"}, "tests": {"empirical", "control"},
                "rules-out": {"empirical", "control"}}


# The prompt is a file, not a string, so that a committed run can record which version of
# it produced a given set of edges. A prompt that lives only in code cannot be cited by a
# provenance record, and an output nobody can trace to its prompt is not reproducible. It is
# composed with the contract vocabulary through `prompts.prompt("edge-inference", cfg)`.


def _get(claim, key, default=None):
    """Read a field from a ReconciledClaim, a CandidateClaim or a plain dict."""
    if isinstance(claim, dict):
        return claim.get(key, default)
    return getattr(claim, key, default)


def _role(claim) -> str | None:
    return _get(claim, "role")


def _stance(claim) -> str:
    """The paper's stance toward this claim; absent means `asserts` (claim-format.md §2).

    A freshly drafted claim carries no stance, so it reads `asserts`: the induction chain does
    not raise the alternatives a `rules-out` would target — the `stance` layer does, later — so
    a contrary edge inferred here has no valid target, which the direction check enforces.
    """
    return _get(claim, "stance") or "asserts"


def _sentence(claim) -> str:
    return " ".join(str(_get(claim, "claim") or "").split())


def _spans(claim) -> list[str]:
    """The span ids this claim's evidence was drawn from, in reader order, de-duplicated.

    A ReconciledClaim carries `span_by_agent` (one per reader); a reader's CandidateClaim
    carries a single `span`. Either way the digest shows the model where a `why` can cite one.
    """
    out: list[str] = []
    for v in (_get(claim, "span_by_agent") or {}).values():
        if v and v not in out:
            out.append(v)
    single = _get(claim, "span")
    if single and single not in out:
        out.append(single)
    return out


def _evidence(claim) -> list[tuple[str | None, str]]:
    """The evidence quotes grounding this claim, whole — never truncated.

    `evidence_by_agent` (reconciled) is a quote per reader; a reader's own claim has one
    `evidence` string. The model reasons from what the readers actually saw, so the quotes go
    in in full rather than cut to 220 characters as the old stub did.
    """
    by_agent = _get(claim, "evidence_by_agent") or {}
    if by_agent:
        return [(a, q) for a, q in by_agent.items() if q]
    single = _get(claim, "evidence")
    return [(None, single)] if single else []


def _claim_digest(claims: list, slugs: list[str], *, include: set[int] | None = None) -> str:
    """Render the claim list for the prompt, numbered.

    Claims are identified by number, not slug. Slugs invite paraphrase: given
    `[hypothesis] social-decisions-under-risk-engage`, the model reads the bracketed role as
    part of the name and returns invented identifiers. An integer cannot be paraphrased.

    Per claim: its number, role, panel and stance; the full sentence; the span ids its evidence
    came from where the draft has any; and every evidence quote the readers gave, in full. When
    `include` is given (per-arc chunking) only those global numbers are rendered, but the
    numbering stays global so answers merge under one scheme.
    """
    lines: list[str] = []
    for i, c in enumerate(claims, 1):
        if include is not None and i not in include:
            continue
        role = _role(c) or "claim"
        panel = _get(c, "panel")
        head = f"{i}. ({role}"
        if panel:
            head += f", panel {panel}"
        head += f", {_stance(c)}) {_sentence(c)}"
        lines.append(head)
        spans = _spans(c)
        if spans:
            lines.append(f"    span: {', '.join(spans)}")
        for agent, quote in _evidence(c):
            q = " ".join(str(quote).split())
            lines.append(f"    evidence ({agent}): “{q}”" if agent else f"    evidence: “{q}”")
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


def _parse_edges(raw: str) -> list | None:
    """Read the model's edges, whether an array, JSON-lines, or a stream cut off mid-answer.

    The rebuilt prompt asks for one edge object per line, not a bracketed array, and a run that
    hits the token ceiling stops mid-object. Discarding every edge because the last one was
    truncated is the wrong trade: the objects before the cut are complete and exactly as good
    as they would have been had the model stopped one object earlier. This happened on a live
    Gädeke run — six minutes of streaming and zero edges written.

    So the whole reply is walked for complete top-level `{…}` objects, tracking brace depth
    outside strings. Array brackets and the commas or newlines between objects sit outside any
    brace and are ignored, so an array, JSON-lines and a truncated stream all read the same;
    a half-written trailing object is dropped rather than guessed at. A clean bracketed array
    is tried first for speed.
    """
    start = raw.find("[")
    end = raw.rfind("]")
    if start != -1 and end > start:
        try:
            parsed = json.loads(raw[start:end + 1])
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            pass    # fall through and walk for whole objects

    objs: list = []
    depth = 0
    obj_start = -1
    in_str = False
    esc = False
    for i, ch in enumerate(raw):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                obj_start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and obj_start != -1:
                    try:
                        objs.append(json.loads(raw[obj_start:i + 1]))
                    except json.JSONDecodeError:
                        pass
                    obj_start = -1

    if not objs:
        logger.warning("edge inference produced no parseable edges; none written")
        return None
    return objs


def arcs(claims: list) -> list[list[int]]:
    """One arc per hypothesis: the hypothesis, every prediction, and the claims that mention them.

    For `--per-arc` chunking: a weaker model does better with one hypothesis's arc per call than
    the whole table at once. The links that would define an arc precisely (`entails`, `tests`)
    are what this layer infers, so they are not available yet; the arc is approximated by role
    and by content-word overlap — the hypothesis, all predictions, and any claim sharing a
    salient word with them. Arcs overlap freely; the merge de-duplicates. With no hypothesis the
    only arc is the whole table.
    """
    stop = {"which", "these", "those", "their", "there", "where", "while", "about", "between",
            "during", "study", "studies", "paper", "results", "result", "effect", "condition"}
    words = lambda t: {w for w in re.findall(r"[a-z]{5,}", t.lower())} - stop
    hyps = [i for i, c in enumerate(claims, 1) if _role(c) == "hypothesis"]
    preds = [i for i, c in enumerate(claims, 1) if _role(c) == "prediction"]
    if not hyps:
        return [list(range(1, len(claims) + 1))]
    out: list[list[int]] = []
    for h in hyps:
        key = words(_sentence(claims[h - 1]))
        for p in preds:
            key |= words(_sentence(claims[p - 1]))
        members = {h, *preds}
        for i, c in enumerate(claims, 1):
            if i not in members and words(_sentence(c)) & key:
                members.add(i)
        out.append(sorted(members))
    return out


def build_edge_request(draft: DraftClaimTable, slugs: list[str], cfg: Config | None = None, *,
                       include: set[int] | None = None) -> tuple[str, str]:
    """The exact (system, user) prompt the edge step sends.

    Exposed so the same request can be answered by something other than a
    configured backend — an analyst, or a reasoning agent — without that
    answer being produced against a different question. If the prompt lived
    only inside the runner, any alternative route would be guessing at it.

    The system prompt is the task composed with the contract vocabulary, loaded through
    `prompts.prompt` so the file the layer declares is the file that is sent, honouring
    `--prompts-dir` and `--prompt-variant` in the passed `cfg`. `include` restricts the digest
    to one arc's claims for `--per-arc`, keeping the global numbering.
    """
    import argparse

    from .prompts import prompt as compose

    if cfg is None:
        cfg = Config.from_args(argparse.Namespace())
    system = compose("edge-inference", cfg)
    shown = len(include) if include is not None else len(draft.claims)
    user = (
        f"Here are {len(draft.claims)} claims from the paper"
        + (f" (this request covers {shown} of them; keep the numbering):\n\n"
           if include is not None else ":\n\n")
        + f"{_claim_digest(draft.claims, slugs, include=include)}\n\n"
        "Identify the relationships between these numbered claims. Refer to claims by number. "
        "Return one edge per line as a JSON object; no prose, no code fence."
    )
    return system, user


def edges_from_raw(raw: str, claims: list, slugs: list[str], *,
                   source: str = "model") -> list[dict]:
    """Validate a raw edge response into corpus-vocabulary edges.

    Every route into the corpus goes through here — the configured backend, a supplied file, an
    analyst's hand-written list. `claims` and `slugs` are parallel: the claim at index i-1 is
    the one the digest numbered i, and the validator needs its role and stance to check
    direction. Edges that name an unknown slug, point at themselves, name no relation, break a
    direction rule, or emit a mechanically-written reciprocal are dropped rather than written —
    an invented or mis-aimed edge is worse than a missing one, and that has to hold no matter
    who produced the answer.
    """
    parsed = _parse_edges(raw)
    if parsed is None:
        return []
    return _validate_edges(parsed, claims, slugs, source=source)


def infer_edges(draft: DraftClaimTable, slugs: list[str], cfg: Config, *,
                per_arc: bool = False) -> list[dict]:
    """Ask the configured backend for typed relations between the claims.

    `per_arc` splits the work into one call per hypothesis arc and merges the replies through
    the same validation — the merge is concatenation before validation, which de-duplicates.
    """
    # Budget the call to what the output can actually be. An edge is a small JSON object — two
    # claim numbers, a relation name and a one-sentence why, ~80 tokens — and a paper has at most
    # a few edges per claim. Taking the package default of 32768 asks for far more than this call
    # can emit, which buys nothing and costs real failures: providers that reserve the requested
    # budget against a credit balance reject the request outright. That is how edge inference once
    # died on a live Gädeke run — HTTP 402 — and lost the spine while every other stage succeeded.
    budget = max(8192, min(32768, 500 * max(len(slugs), 1)))

    edge_schema = _edge_output_schema()
    if per_arc:
        raws: list[str] = []
        for members in arcs(draft.claims):
            system, user = build_edge_request(draft, slugs, cfg, include=set(members))
            raws.append(stream_text(cfg, model=cfg.model_reconcile, system=system, user=user,
                                    max_tokens=budget, label="edge-inference[arc]",
                                    output_schema=edge_schema))
        return edges_from_raw("\n".join(raws), draft.claims, slugs, source="model:per-arc")

    system, user = build_edge_request(draft, slugs, cfg)
    raw = stream_text(cfg, model=cfg.model_reconcile, system=system, user=user,
                      max_tokens=budget, label="edge-inference", output_schema=edge_schema)
    return edges_from_raw(raw, draft.claims, slugs, source="model")


def _validate_edges(parsed: list, claims: list, slugs: list[str], *, source: str) -> list[dict]:
    """Apply the direction rules to a parsed edge list, then synthesise the reciprocals.

    Every rejection is counted by reason and logged, so a run says what it refused and why
    rather than silently thinning the graph.
    """
    role_of = {slug: _role(c) for slug, c in zip(slugs, claims)}
    stance_of = {slug: _stance(c) for slug, c in zip(slugs, claims)}

    edges: list[dict] = []
    seen: set[tuple[str, str, str]] = set()
    part_whole: dict[str, str] = {}                 # part slug → its whole, for cycle detection
    dissociate_pairs: set[frozenset] = set()        # symmetric: one edge per unordered pair
    rejected: dict[str, int] = {}

    def reject(reason: str) -> None:
        rejected[reason] = rejected.get(reason, 0) + 1

    for e in parsed:
        if not isinstance(e, dict):
            reject("not an object")
            continue
        src = _resolve(e.get("source"), slugs)
        tgt = _resolve(e.get("target"), slugs)
        # `relation` is the corpus key; tolerate the old `relationType` so a stale answer is
        # reported as an unknown relation rather than crashing.
        rel = (e.get("relation") or e.get("relationType") or "").strip()
        why = " ".join(str(e.get("why") or "").split())

        if not src or not tgt:
            reject("unknown or unresolvable reference")
            continue
        if src == tgt:
            reject("self reference")
            continue
        if rel not in EDGE_KEYS:
            reject(f"unknown relation {rel!r}" if rel else "no relation named")
            continue
        if rel in NEVER_EMITTED:
            reject(f"{rel} is written mechanically, never emitted")
            continue

        need = _SOURCE_ROLE.get(rel)
        if need and role_of.get(src) not in need:
            reject(f"{rel} source must be {'/'.join(sorted(need))}, not {role_of.get(src)}")
            continue
        if rel == "tests" and role_of.get(tgt) != "prediction":
            reject(f"tests target must be a prediction, not {role_of.get(tgt)}")
            continue
        if rel in CONTRARY and stance_of.get(tgt) == "asserts":
            reject(f"{rel} cannot target a claim the paper asserts")
            continue

        if rel == "part-of":
            if src in part_whole:
                reject("part-of: a part may have only one whole")
                continue
            node, cyclic = tgt, False
            while True:
                if node == src:
                    cyclic = True
                    break
                if node not in part_whole:
                    break
                node = part_whole[node]
            if cyclic:
                reject("part-of: would close a cycle")
                continue
            part_whole[src] = tgt

        if rel == "dissociates-with":
            pair = frozenset((src, tgt))
            if pair in dissociate_pairs:
                reject("dissociates-with: symmetric, already recorded for this pair")
                continue
            dissociate_pairs.add(pair)

        key = (src, tgt, rel)
        if key in seen:
            continue
        seen.add(key)
        edges.append({"source": src, "target": tgt, "relation": rel, "why": why})

    # Synthesise the reciprocal of each deductive edge — the direction the model was forbidden.
    for e in list(edges):
        inverse = RECIPROCAL.get(e["relation"])
        if not inverse:
            continue
        key = (e["target"], e["source"], inverse)
        if key not in seen:
            seen.add(key)
            edges.append({"source": e["target"], "target": e["source"], "relation": inverse,
                          "why": f"reciprocal of {e['relation']} ({e['source']} → {e['target']})"})

    by_type: dict[str, int] = {}
    for e in edges:
        by_type[e["relation"]] = by_type.get(e["relation"], 0) + 1
    dropped = sum(rejected.values())
    logger.info(
        "edges (%s): %d edges across %d types (%d dropped): %s",
        source, len(edges), len(by_type), dropped,
        ", ".join(f"{k}={v}" for k, v in sorted(by_type.items(), key=lambda x: -x[1])),
    )
    if rejected:
        logger.info("  rejected: %s",
                    "; ".join(f"{v}× {r}" for r, v in sorted(rejected.items(), key=lambda x: -x[1])))
    return edges


# Reverse mapping for OXA output — corpus relation names back to CiTO/claimrel IRIs. The CiTO
# map lives in `oxa.py` now (there is no `CITO_TO_CORPUS` in this module any more), and
# `oxa.EDGE_MAP` is already corpus-name → IRI, which is exactly what `apply_oxa_edges` needs.
from .oxa import EDGE_MAP as _CORPUS_TO_CITO


def apply_oxa_edges(oxa_claims: list[dict], edges: list[dict]) -> list[dict]:
    """Apply corpus-format edges from `infer_edges` to OXA claim nodes.

    `edges` is the list returned by `infer_edges` — each edge is
    {"source": slug, "target": slug, "relation": corpus_name}.  The OXA
    `relations` list uses CiTO/claimrel IRIs as `relationType`, so we
    convert back on the way in.

    Called by the API after `infer_edges`; the CLI's write step uses
    `edges_for_slug` instead (which produces YAML frontmatter, not OXA JSON).
    """
    idx: dict[str, list[dict]] = {}
    for e in edges:
        rel_cito = _CORPUS_TO_CITO.get(e["relation"], e["relation"])
        idx.setdefault(e["source"], []).append(
            {"xref": e["target"], "relationType": rel_cito}
        )
    for c in oxa_claims:
        cid = c.get("identifier", "")
        if cid in idx:
            c["relations"] = c.get("relations", []) + idx[cid]
    return oxa_claims


def edges_for_slug(edges: list[dict], slug: str) -> tuple[dict, list[dict]]:
    """Split one claim's outgoing edges into (top-level keys, belongings).

    Returns ({relation: [targets]}, [{relation, target}]) ready to merge into the claim's
    frontmatter. The `why` rides along in each edge dict but is not written into the frontmatter
    — the frontmatter shape is fixed; the `why` goes in the claim body's Relations note instead.
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
