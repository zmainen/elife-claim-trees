"""A whole claim tree, read by a person, recorded as data.

The gap-claim surface (#78) decides one drafted claim at a time. This is the other reading the
plan in #82 asks for: a person goes through a *whole* tree — every claim, every part, every
edge — and records a verdict on each, bound to the version they read. The verdicts are a file,
one line per decision, append-only like the run ledger, so a reader who changes their mind
writes a second line and the latest one for a key wins.

    runs/<paper>/claim-tree.v<N>.verdicts.jsonl

A claim verdict says whether the claim is true to the paper, and if not what to do with it:

    {"kind": "claim", "slug": "...", "verdict": "keep"|"strike"|"merge-into"|"part-of",
     "target"?: "...", "role"?: "...", "panel"?: "...", "why"?: "...", "by": "...", "when": "..."}

An edge verdict says whether one relation is right, and if not, what it should have been:

    {"kind": "edge", "source": "...", "target": "...", "relation": "...",
     "verdict": "ok"|"wrong-direction"|"wrong-relation"|"strike"|"missing",
     "corrected"?: "...", "by": "...", "when": "..."}

A ruling answers one of the disputes the tree cannot settle claim-by-claim:

    {"kind": "ruling", "question": "...", "answer": "...", "why"?: "...", "by": "...", "when": "..."}

The reading is *editing*, not authoring: `skeleton` writes a `keep` for every claim and an `ok`
for every edge before the reader starts, so a claim they never look at stays `keep` and a claim
they consider carries `considered: true` — the one flag that tells a decision apart from a
default. `validate` refuses the four things a verdict file must never say. `evaluate score
--gold` reads the resolved verdicts as a corrected reference; `scripts/verdicts.py` is the CLI.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

# ── the vocabulary ────────────────────────────────────────────────────────────

CLAIM_VERDICTS = ("keep", "strike", "merge-into", "part-of")
EDGE_VERDICTS = ("ok", "wrong-direction", "wrong-relation", "strike", "missing")

# `verdict` values that name another claim as their `target`. A `strike` names nothing; a `keep`
# names nothing. `merge-into` and `part-of` are meaningless without one.
CLAIM_VERDICTS_WITH_TARGET = ("merge-into", "part-of")

# The three disputes the issue names, plus any free question a reader wants to settle. The named
# three are validated against this set only for a typo's sake — a free question is allowed.
RULING_QUESTIONS = ("sts-mentalising-role", "partner-algorithm-role", "procedure-under-scope")


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── the file ────────────────────────────────────────────────────────────────

def verdicts_path(root: Path, paper: str, version: int) -> Path:
    return Path(root) / "runs" / paper / f"claim-tree.v{version}.verdicts.jsonl"


def load(path: str | Path) -> list[dict]:
    """Every verdict line, in the order written. A half-written line is not a verdict."""
    p = Path(path)
    if not p.is_file():
        return []
    out: list[dict] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict):
            out.append(rec)
    return out


def append(path: str | Path, record: dict) -> None:
    """Append one verdict. The file is a sequence of decisions, never rewritten."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


def key_of(rec: dict) -> tuple | None:
    """The key a later line supersedes. One per claim, one per (source,target,relation) edge,
    one per ruling question."""
    kind = rec.get("kind")
    if kind == "claim":
        return ("claim", rec.get("slug"))
    if kind == "edge":
        return ("edge", rec.get("source"), rec.get("target"), rec.get("relation"))
    if kind == "ruling":
        return ("ruling", rec.get("question"))
    return None


class Resolved:
    """The verdicts that stand, after the latest line per key wins.

    A file is a history; this is the state it currently asserts. `claims`, `edges` and `rulings`
    are keyed so a caller can ask "what stands on this claim" without walking the whole file.
    """

    def __init__(self, records: list[dict]):
        self.claims: dict[str, dict] = {}
        self.edges: dict[tuple[str, str, str], dict] = {}
        self.rulings: dict[str, dict] = {}
        for rec in records:
            key = key_of(rec)
            if key is None:
                continue
            if key[0] == "claim" and key[1]:
                self.claims[key[1]] = rec
            elif key[0] == "edge" and all(key[1:]):
                self.edges[(key[1], key[2], key[3])] = rec
            elif key[0] == "ruling" and key[1]:
                self.rulings[key[1]] = rec

    # The verdicts a reader actually made, told apart from the skeleton's defaults by
    # `considered`. A `keep` with `considered: false` is a claim nobody looked at.
    def claims_considered(self) -> list[dict]:
        return [r for r in self.claims.values() if r.get("considered")]

    def edges_considered(self) -> list[dict]:
        return [r for r in self.edges.values() if r.get("considered")]

    @property
    def struck(self) -> set[str]:
        return {s for s, r in self.claims.items() if r.get("verdict") == "strike"}

    @property
    def merged(self) -> dict[str, str]:
        """slug → the claim it merges into."""
        return {s: r["target"] for s, r in self.claims.items()
                if r.get("verdict") == "merge-into" and r.get("target")}

    @property
    def part_of(self) -> dict[str, str]:
        """slug → the claim it is a part of, as ruled by a verdict."""
        return {s: r["target"] for s, r in self.claims.items()
                if r.get("verdict") == "part-of" and r.get("target")}


def resolve(records: list[dict]) -> Resolved:
    return Resolved(records)


# ── validation ──────────────────────────────────────────────────────────────

def validate(records: list[dict], *, claim_slugs, edge_triples=None) -> list[str]:
    """What is wrong with a verdict file, given the tree it was made against.

    Four refusals the plan (#82) names, and the kind/verdict typos that would make a line mean
    nothing:

      1. an unknown slug — a claim, target, or edge endpoint the tree does not carry;
      2. a cycle in `part-of` — a claim that is, transitively, a part of itself;
      3. a `merge-into` whose target is itself struck — merging into something that is not there;
      4. an edge naming an absent claim.

    Returns the problems as sentences; an empty list is a clean file.
    """
    slugs = set(claim_slugs)
    known_edges = set(edge_triples or [])
    problems: list[str] = []
    res = resolve(records)

    for rec in records:
        kind = rec.get("kind")
        if kind == "claim":
            slug = rec.get("slug")
            verdict = rec.get("verdict")
            if slug not in slugs:
                problems.append(f"claim verdict names {slug!r}, which is not a claim in the tree")
            if verdict not in CLAIM_VERDICTS:
                problems.append(f"{slug}: verdict {verdict!r} is not one of {CLAIM_VERDICTS}")
            target = rec.get("target")
            if verdict in CLAIM_VERDICTS_WITH_TARGET:
                if not target:
                    problems.append(f"{slug}: {verdict} needs a target")
                elif target not in slugs:
                    problems.append(f"{slug}: {verdict} target {target!r} is not a claim in the tree")
            elif target:
                problems.append(f"{slug}: a {verdict} verdict cannot name a target")
        elif kind == "edge":
            src, tgt, rel = rec.get("source"), rec.get("target"), rec.get("relation")
            verdict = rec.get("verdict")
            if verdict not in EDGE_VERDICTS:
                problems.append(f"edge {src}->{tgt} ({rel}): verdict {verdict!r} is not one of {EDGE_VERDICTS}")
            for end, label in ((src, "source"), (tgt, "target")):
                if end not in slugs:
                    problems.append(f"edge {src}->{tgt} ({rel}): {label} {end!r} is not a claim in the tree")
        elif kind == "ruling":
            if not rec.get("question"):
                problems.append("a ruling needs a question")
            if not rec.get("answer"):
                problems.append(f"ruling {rec.get('question')!r} has no answer")
        else:
            problems.append(f"a verdict line has kind {kind!r}, which is not claim, edge or ruling")

    # A merge-into whose target is itself struck: the duplicate would fold into nothing.
    for slug, target in res.merged.items():
        if target in res.struck:
            problems.append(f"{slug}: merge-into {target!r}, which is itself struck")

    # A cycle in part-of, over the verdicts' own part-of relations. A claim reachable from
    # itself by following part-of would have no whole to fold beneath.
    part_of = res.part_of
    for start in part_of:
        seen, cur = {start}, part_of.get(start)
        while cur is not None:
            if cur == start:
                problems.append(f"part-of forms a cycle through {start!r}")
                break
            if cur in seen:
                break
            seen.add(cur)
            cur = part_of.get(cur)

    return problems


# ── the skeleton ──────────────────────────────────────────────────────────────

def skeleton(claim_slugs, edge_triples, *, by: str = "skeleton",
             when: str | None = None) -> list[dict]:
    """Every claim pre-filled `keep`, every edge pre-filled `ok`, all `considered: false`.

    So the reading is editing a file rather than authoring one: a claim the reader never opens
    stays `keep`, and `considered` tells the two apart. Edges are the tree's relations; `part-of`
    is a claim verdict, not an edge, so it is not enumerated here.
    """
    when = when or now()
    out: list[dict] = []
    for slug in sorted(set(claim_slugs)):
        out.append({"kind": "claim", "slug": slug, "verdict": "keep",
                    "considered": False, "by": by, "when": when})
    for src, tgt, rel in sorted(set(edge_triples)):
        out.append({"kind": "edge", "source": src, "target": tgt, "relation": rel,
                    "verdict": "ok", "considered": False, "by": by, "when": when})
    return out


def is_complete(records: list[dict], *, claim_slugs, edge_triples) -> bool:
    """Every claim and every edge carries at least one verdict line."""
    res = resolve(records)
    return (set(claim_slugs) <= set(res.claims)
            and set(edge_triples) <= set(res.edges))


# ── reading a tree off disk (for the CLI and tests) ─────────────────────────────
#
# A frontmatter reader kept here rather than borrowed from evaluate.py so this module carries no
# dependency on the model-call chain: a validator must import without a backend.

_FM = re.compile(r"^---\n(.*?)\n---", re.S)

# The relation vocabulary, from scripts/relations.py; `part-of` is a claim verdict, not an edge.
def _edge_relations() -> set[str]:
    import importlib.util
    p = Path(__file__).resolve().parents[2] / "scripts" / "relations.py"
    if not p.is_file():
        return set()
    spec = importlib.util.spec_from_file_location("relations", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return set(mod.EDGE_KEYS) - {"part-of"}


def read_frontmatter(path: Path) -> dict:
    import yaml
    text = Path(path).read_text(encoding="utf-8")
    m = _FM.match(text)
    if not m:
        return {}
    fixed = re.sub(r"^(\w[\w-]*):\n\[\]", r"\1: []", m.group(1), flags=re.MULTILINE)
    try:
        return yaml.safe_load(fixed) or {}
    except yaml.YAMLError:
        return {}


def load_tree(claim_dir: str | Path) -> tuple[list[str], list[tuple[str, str, str]]]:
    """A paper's claim slugs and its (source, target, relation) edges, from the claim files.

    Edges are read from the top-level relation keys and the `belongings` list, the two places the
    schema puts them — the same two `evaluate.load_edges` reads. `part-of` is excluded: it is a
    claim verdict, not an edge.
    """
    claim_dir = Path(claim_dir)
    rels = _edge_relations()
    slugs: list[str] = []
    triples: list[tuple[str, str, str]] = []
    for path in sorted(claim_dir.glob("*.md")):
        if path.name == "index.md":
            continue
        fm = read_frontmatter(path)
        if not fm:
            continue
        slug = fm.get("slug") or path.stem
        slugs.append(slug)
        seen: set[tuple[str, str, str]] = set()

        def _add(tgt, rel):
            t = (slug, tgt, rel)
            if rel in rels and isinstance(tgt, str) and t not in seen:
                seen.add(t)
                triples.append(t)

        for rel in sorted(rels):
            for tgt in (fm.get(rel) or []):
                _add(tgt, rel)
        for item in (fm.get("belongings") or []):
            if isinstance(item, dict):
                _add(item.get("target"), item.get("relation"))
    return slugs, triples
