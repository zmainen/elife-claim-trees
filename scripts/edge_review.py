#!/usr/bin/env python3
"""Layer `edge-review` — what does a claim added after induction depend on and support?

`edge-inference` needs only `reconcile`. It runs on the reconciled candidates, upstream of the
claim files, and `claim-tree` writes the edges it inferred. Nothing downstream of `claim-tree`
decides a relation, so a claim written afterwards has no path to one — not later, not ever.

Which would be an abstract complaint if the corpus did not now produce such claims. A reviewer
promoting a `gap-claim` draft adds a claim to a finished tree, and it lands with no relation in
a graph whose entire purpose is typed relations. This layer is the missing edge back: it asks
the relation question of the claim set as it stands rather than of the candidates that produced
it.

Corpus-wide that is six claims today, not the thirty-four a first count gave. The difference is
the definition, and the smaller number is the right one: counting claims with no *outgoing*
relation swept in every rejected alternative, which asserts nothing by design and is connected
by the control that rules it out.

    python3 scripts/edge_review.py gadeke-2026-guilt-insula --dump-prompt /tmp/q.txt
    # answer it anywhere — another model, another provider, a person
    python3 scripts/edge_review.py gadeke-2026-guilt-insula --answer /tmp/a.json
    python3 scripts/edge_review.py gadeke-2026-guilt-insula --answer /tmp/a.json --write

It is deliberately the same question `edge-inference` asks, under the same contract: the system
prompt is that layer's prompt, composed through `prompts.prompt`, and every answer goes through
`edges.edges_from_raw`, which drops an edge that names an unknown slug, points at itself, names
no relation, breaks a direction rule, or writes a reciprocal the corpus synthesises. An invented
or mis-aimed edge is worse than a missing one, and that has to hold whichever layer asked.

What differs is the input and the scope of the answer. The digest is the whole tree, because a
relation is only judgeable against the claims it could hold with; the edges kept are the ones
touching a claim that has none, in either direction, since being unreferenced is the same
defect seen from the other side.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "extract"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from elife_extract import edges as E  # noqa: E402
from corpus_facts import frontmatter, loadable  # noqa: E402

OUT = ROOT / "runs"

# Every relation a claim file can carry, from the same declaration `edges.py` reads.
REL_KEYS = sorted(E.EDGE_KEYS | E.BELONGINGS_RELATIONS | set(E.RECIPROCAL.values()))


def claims_of(paper: str) -> list[dict]:
    """Every claim of this paper, as the dicts `edges.py` already knows how to read.

    `_role`, `_stance` and `_sentence` take a claim through `_get`, which handles a mapping as
    readily as an object, so the frontmatter goes straight in and the direction checks work on
    it unchanged. Ordered by slug so the numbering in the digest is stable between a dumped
    prompt and the answer that comes back to it.
    """
    out = []
    for f in sorted((ROOT / "claims" / paper).glob("*.md")):
        if f.name == "index.md":
            continue
        fm = frontmatter(f) or {}
        fm.setdefault("slug", f.stem)
        out.append(fm)
    return out


def outgoing(claim: dict) -> list[str]:
    """The relations this claim asserts, wherever the format keeps them."""
    rels = [k for k in REL_KEYS if claim.get(k)]
    if claim.get("belongings"):
        rels += [b.get("relation") for b in claim["belongings"] if isinstance(b, dict)]
    return [r for r in rels if r]


def targets_of(claim: dict) -> set[str]:
    """Every slug this claim points at, wherever the format keeps the relation."""
    out: set[str] = set()
    for k in REL_KEYS:
        v = claim.get(k)
        if isinstance(v, list):
            out |= {x for x in v if isinstance(x, str)}
    for b in (claim.get("belongings") or []):
        if isinstance(b, dict) and b.get("target"):
            out.add(b["target"])
    return out


def unconnected(claims: list[dict]) -> list[dict]:
    """Claims with no relation in either direction.

    Not "asserts none": a rejected alternative asserts nothing by design, and is connected by
    the control that rules it out. Counting only outgoing edges would put all six of Gädeke's
    alternatives on this list and invite a model to wire them to something, which would be the
    graph asserting what the paper denies. A claim nothing points at and that points at nothing
    is the orphan this layer is for.
    """
    pointed_at: set[str] = set()
    for c in claims:
        pointed_at |= targets_of(c)
    return [c for c in claims
            if not outgoing(c) and c.get("slug") not in pointed_at]


def build_prompt(paper: str) -> tuple[str, str]:
    import argparse as _a

    from elife_extract.config import Config
    from elife_extract.prompts import prompt as compose

    claims = claims_of(paper)
    slugs = [c["slug"] for c in claims]
    loose = unconnected(claims)
    if not loose:
        raise SystemExit(f"{paper}: every claim already asserts a relation")

    cfg = Config.from_args(_a.Namespace())
    system = compose("edge-inference", cfg)

    numbered = {c["slug"]: i + 1 for i, c in enumerate(claims)}
    which = ", ".join(str(numbered[c["slug"]]) for c in loose)
    user = (
        f"Here are {len(claims)} claims from one paper, as its claim tree stands today:\n\n"
        f"{E._claim_digest(claims, slugs)}\n\n"
        f"Claims {which} assert no relation to anything. Every other claim in this list is "
        "already wired into the tree.\n\n"
        "Identify the relationships those claims have to the rest. An edge may run in either "
        "direction: one of them may depend on, support, test or qualify a claim that is "
        "already connected, and an already-connected claim may depend on or be supported by "
        "one of them. Do not restate relations that already hold between two connected "
        "claims — they are shown so that the loose claims can be judged against them.\n\n"
        "A claim that genuinely stands alone is a real answer: emit nothing for it rather "
        "than reaching for the nearest plausible neighbour. A wrong edge is worse than a "
        "missing one, because it will be read as the paper's own reasoning.\n\n"
        "Refer to claims by number. Return one edge per line as a JSON object; no prose, no "
        "code fence."
    )
    return system, user


def review(raw: str, paper: str) -> tuple[list[dict], list[str]]:
    """Validate an answer and keep the edges that touch a claim which had none."""
    claims = claims_of(paper)
    slugs = [c["slug"] for c in claims]
    loose = {c["slug"] for c in unconnected(claims)}

    edges = E.edges_from_raw(raw, claims, slugs, source="edge-review")
    kept, dropped = [], []
    for e in edges:
        if e["source"] in loose or e["target"] in loose:
            kept.append(e)
        else:
            dropped.append(f"{e['source']} {e['relation']} {e['target']}")
    return kept, dropped


def write_output(paper: str, edges: list[dict], dropped: list[str], *, by: str) -> Path:
    out = OUT / paper / "edge-review.output.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "paper": paper,
        "reviewed_on": date.today().isoformat(),
        "model": by,
        "note": ("Relations for claims that had none, asked of the claim set as it stands. "
                 "Validated by edges.edges_from_raw, so the direction rules and the corpus "
                 "vocabulary hold exactly as they do for edge-inference."),
        "edges": edges,
        "dropped_already_connected": dropped,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return out


def apply(paper: str, edges: list[dict]) -> list[Path]:
    """Merge the edges into the claim files, where the format keeps each relation.

    `edges_for_slug` holds the rule for which relation is a top-level key and which belongs in
    `belongings:`, and it is the rule `claim-tree` writes by. Using it here is what stops a
    claim written by this layer from looking different to one written by induction.

    The frontmatter is read through `corpus_facts.loadable`, because the claims this layer
    exists for are the ones a promoted `gap-claim` draft wrote, and that template emits
    `belongings:` with `[]` on the next line — which `yaml.safe_load` refuses outright. Reading
    a claim file strictly and writing it back is how the first run of this layer crashed
    halfway through a paper.
    """
    import yaml

    from elife_extract.write import _format_claim_file

    touched = []
    for slug in sorted({e["source"] for e in edges}):
        path = ROOT / "claims" / paper / f"{slug}.md"
        if not path.is_file():
            print(f"  ! no claim file for {slug}", file=sys.stderr)
            continue
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, flags=re.S)
        if not m:
            print(f"  ! {slug} has no frontmatter", file=sys.stderr)
            continue
        fm = yaml.safe_load(loadable(m.group(1))) or {}
        top, belongings = E.edges_for_slug(edges, slug)
        for rel, targets in top.items():
            fm[rel] = sorted(set((fm.get(rel) or []) + targets))
        if belongings:
            have = {(b.get("relation"), b.get("target")) for b in (fm.get("belongings") or [])
                    if isinstance(b, dict)}
            fm["belongings"] = (fm.get("belongings") or []) + [
                b for b in belongings if (b["relation"], b["target"]) not in have]
        # Rendered by the same function `claim-tree` renders with, down to the dump width: a
        # claim this layer touches should differ from its committed self by the edge it gained
        # and nothing else, and a private 80-column re-wrap of every sentence in the file is
        # not nothing — it is the diff a reviewer has to read past to find the edge.
        path.write_text(_format_claim_file(fm, m.group(2).lstrip("\n")), encoding="utf-8")
        touched.append(path)
    return touched


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper")
    ap.add_argument("--dump-prompt", metavar="PATH",
                    help="write the exact prompt this layer would send to PATH and exit")
    ap.add_argument("--answer", metavar="PATH",
                    help="edges produced elsewhere; validated exactly as edge-inference's are")
    ap.add_argument("--write", action="store_true",
                    help="merge the validated edges into the claim files")
    args = ap.parse_args()

    if args.dump_prompt:
        system, user = build_prompt(args.paper)
        out = Path(args.dump_prompt).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(system + "\n\n---\n\n" + user, encoding="utf-8")
        print(f"  edge-review: prompt written to {out}  "
              f"({len(system)}c system + {len(user)}c user)")
        print("  answer it, then: --answer <file>")
        return 0
    if not args.answer:
        ap.error("this layer has no backend call of its own: use --dump-prompt, then --answer")

    src = Path(args.answer).expanduser().resolve()
    edges, dropped = review(src.read_text(encoding="utf-8"), args.paper)
    if not edges:
        # An answer whose every edge is already in the corpus is this layer having run before,
        # not a failure: `--write` connects the claims it was asked about, so a second run sees
        # no unconnected claim and keeps nothing. `pipeline.py run` records a step by executing
        # its command, which is exactly that second run, so failing here would mean the layer
        # could never record the run that succeeded. The output file is left alone — it holds
        # the edges of the run that wrote them.
        if dropped:
            print(f"  {args.paper}: the corpus already holds all {len(dropped)} edge(s) in "
                  "this answer; nothing to write")
            return 0
        print(f"{args.paper}: no valid edge for any unconnected claim", file=sys.stderr)
        return 1

    try:
        where = src.relative_to(ROOT)
    except ValueError:
        where = src
    out = write_output(args.paper, edges, dropped, by=f"supplied:{where}")

    loose = {c["slug"] for c in unconnected(claims_of(args.paper))}
    print(f"  {args.paper}")
    for e in edges:
        mark = "→" if e["source"] in loose else "←"
        print(f"    {mark} {e['source']}  {e['relation']}  {e['target']}")
    print(f"  {len(edges)} edge(s) for {len(loose)} unconnected claim(s)"
          + (f", {len(dropped)} dropped as already connected" if dropped else "")
          + f" · {out.relative_to(ROOT)}")

    if not args.write:
        print("\n  nothing written to the corpus — pass --write to merge them into the claims")
        return 0
    touched = apply(args.paper, edges)
    print(f"\n  {len(touched)} claim file(s) updated")
    print("  every layer downstream of claim-tree is now stale for this paper, by design")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
