#!/usr/bin/env python3
"""Find claims that need a human judgement, and put them in a queue with the evidence.

Every claim, relation and verdict in this corpus was produced by a language model and checked
by nobody. That is stated on the site, but until now there was no mechanism for a human to
check anything even if they wanted to. This is that mechanism: a detector finds candidates, an
agent proposes a reading, and the decision waits for a person.

WHAT IS AUTOMATIC AND WHAT IS NOT

Detection is automatic, and so is the evidence: reciprocity, co-occurring relations, shared
neighbours, whether either claim reports a null result, the roles involved. Refreshing the
queue is automatic and idempotent -- decisions already recorded survive regeneration.

The judgement is not, and a measurement says why. A heuristic built from the structural
features above reproduces an agent's reading of the 45 `dissociates-with` pairs 42% of the
time, against 25% for guessing among four types. The distinction cannot be computed from the
shape of the graph; it requires reading what the claims say. So the queue carries a *proposal*
attributed to the agent that made it, and `decision: pending` until a person rules.

  python3 scripts/review_queue.py                 # refresh every queue
  python3 scripts/review_queue.py --paper <slug>  # one paper
  python3 scripts/review_queue.py --status        # what is pending, by paper
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export_mira import load_paper, relations  # noqa: E402
import corpus_facts as CF  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE_DIR = os.path.join(ROOT, "review")
SITE_OUT = os.path.join(ROOT, "site", "src", "data", "review.json")

SUPPORTING = {"supports", "tests", "validates", "confirms", "extends", "replicates"}

# A claim that reports an absence. Recorded as evidence, not used to decide anything: the
# heuristic that leaned on it was right 42% of the time.
NULL_RESULT = re.compile(
    r"\bno\b.{0,20}\b(significant|difference|detectable|effect|correlat)|"
    r"\bdo(es)? not (differ|correlate|change)|not significantly|"
    r"\bnegligible\b|\bnull\b|\bunaffected\b|\bintact\b|\bunchanged\b", re.I)

# Definitions are self-contained on purpose. An earlier draft illustrated each type with a
# result from a specific paper -- "PV interneurons impaired while excitatory neurons are not" --
# which is unreadable to anyone who has not read that paper, and the reviewer needs the
# definition before the examples, not instead of them. The concrete cases are the queue itself,
# each carrying both claims in full.
TYPES = {
    "parallel": ("Two findings about different objects, neither bearing on the other. The "
                 "relation asserts a connection the claims do not have."),
    "selective": ("The same measure applied in two places, present in one and absent in the "
                  "other. This is the technical sense of a dissociation, and how specificity "
                  "is established."),
    "property": ("One object, two attributes that did not move together: a gain on one "
                 "dimension without the corresponding change on another."),
    "tension": ("Both findings are asserted, and together they constrain a shared "
                "explanation — if one account of them were right, the other result should "
                "have come out differently."),
}
ACTIONS = {
    "parallel": "remove the relation",
    "selective": "keep as dissociates-with, declared with no parent",
    "property": "keep as dissociates-with, declared with no parent",
    "tension": "retype as qualifies",
}


def short(text, n=240):
    return re.sub(r"\s+", " ", (text or "").strip())[:n]


def dissociates_with(paper):
    """Every dissociates-with pair in a paper, with the evidence a reader needs.

    Reciprocal pairs are one item, not two: the relation is declared in both directions in 62%
    of cases, and asking someone the same question twice is how a review queue gets abandoned.
    """
    claims = {c["slug"]: c for c in load_paper(paper)}
    out = collections.defaultdict(set)
    for c in claims.values():
        for k, t in relations(c):
            out[c["slug"]].add((k, t))

    # Both loops iterate in sorted order, and a reciprocal pair is emitted under the
    # alphabetically smaller slug. Neither is cosmetic.
    #
    # `rels` is a set, and Python randomises string hashing per process, so iterating it
    # directly visited a claim's relations in a different order on every run. For a reciprocal
    # pair — 62% of them here — whichever direction was reached first won the dedup below and
    # decided which slug became `a`. The item's `id` is f"{paper}:{a}|{b}", so the same pair
    # was published as `paper:x|y` one run and `paper:y|x` the next.
    #
    # That is not a cosmetic diff. `apply_review.py` matches decisions to items by `id`, so a
    # judgement recorded against one run's identifier silently found no item in the next. A
    # queue whose membership is stable and whose names are not is worse than one that changes
    # visibly.
    items, seen = [], set()
    for a, rels in sorted(out.items()):
        for k, b in sorted(rels):
            if k != "dissociates-with" or b not in claims:
                continue
            recip = ("dissociates-with", a) in out.get(b, set())
            key = tuple(sorted((a, b)))
            if recip and key in seen:
                continue
            seen.add(key)
            if recip:
                # Direction carries no meaning when the relation is declared both ways, so
                # the identifier must not depend on which way we happened to walk it.
                a, b = key

            ta = {t for _, t in out.get(a, set())}
            tb = {t for _, t in out.get(b, set())}
            co = sorted({kk for kk, tt in out[a] if tt == b and kk != "dissociates-with"})
            items.append({
                "id": f"{paper}:{a}|{b}",
                "paper": paper,
                "a": a, "b": b,
                "a_text": short(claims[a].get("claim")),
                "b_text": short(claims[b].get("claim")),
                "a_role": claims[a].get("role"),
                "b_role": claims[b].get("role"),
                "reciprocal": recip,
                "also_carries": co,
                "shared_neighbours": sorted((ta & tb) - {a, b})[:4],
                "a_reports_null": bool(NULL_RESULT.search(claims[a].get("claim") or "")),
                "b_reports_null": bool(NULL_RESULT.search(claims[b].get("claim") or "")),
            })
    return items


DETECTORS = {
    "dissociates-with": {
        "question": "Is this an opposition, a distinction, or no relation at all?",
        "why": ("`dissociates-with` is declared under `mira:opposes` in every MIRA export. "
                "If it is not an opposition, that misstates these relations to every consumer "
                "of the export, including eLife."),
        "types": TYPES,
        "actions": ACTIONS,
        "find": dissociates_with,
    },
}


def load_existing(path):
    """Decisions already recorded, keyed by item id, so a refresh never discards one."""
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return {i["id"]: i for i in data.get("items", [])}


def refresh(topic, papers, seeds):
    spec = DETECTORS[topic]
    path = os.path.join(QUEUE_DIR, f"{topic}.json")
    prior = load_existing(path)

    items = []
    for p in papers:
        for it in spec["find"](p):
            old = prior.get(it["id"], {})
            it["proposed"] = old.get("proposed") or seeds.get(it["id"])
            it["proposed_by"] = old.get("proposed_by") or (
                "agent reading, unverified" if seeds.get(it["id"]) else None)
            # A decision already made is never overwritten by a refresh.
            it["decision"] = old.get("decision", "pending")
            it["decided_by"] = old.get("decided_by")
            it["note"] = old.get("note")
            items.append(it)

    items.sort(key=lambda i: (i["paper"], i["a"]))
    doc = {
        "topic": topic,
        "question": spec["question"],
        "why": spec["why"],
        "types": spec["types"],
        "actions": spec["actions"],
        "items": items,
    }
    os.makedirs(QUEUE_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, sort_keys=False)
        fh.write("\n")
    return doc


def summarise(docs):
    rows = []
    for doc in docs:
        by_paper = collections.Counter()
        pend = collections.Counter()
        for i in doc["items"]:
            by_paper[i["paper"]] += 1
            if i["decision"] == "pending":
                pend[i["paper"]] += 1
        rows.append((doc["topic"], by_paper, pend))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--paper")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--seeds", help="JSON of {item id: proposed type} to seed proposals with")
    a = ap.parse_args()

    site, examples = CF.corpora()
    papers = [a.paper] if a.paper else site + examples

    seeds = {}
    if a.seeds and os.path.isfile(a.seeds):
        with open(a.seeds, encoding="utf-8") as fh:
            seeds = json.load(fh)

    docs = [refresh(t, papers, seeds) for t in DETECTORS]

    # One file the site reads, so the review layer cannot drift from the queue.
    os.makedirs(os.path.dirname(SITE_OUT), exist_ok=True)
    with open(SITE_OUT, "w", encoding="utf-8") as fh:
        json.dump({"topics": docs}, fh, indent=2)
        fh.write("\n")

    for topic, total, pend in summarise(docs):
        n, p = sum(total.values()), sum(pend.values())
        print(f"{topic}: {n} item(s), {p} pending, {n - p} decided")
        if a.status:
            for paper in sorted(total):
                print(f"    {paper:38} {total[paper]:3} · {pend[paper]:3} pending")
    print(f"\nqueue → review/ · site data → {os.path.relpath(SITE_OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
