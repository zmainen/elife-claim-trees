#!/usr/bin/env python3
"""Did the paper's predictions come out, and does the tree say so?

A prediction is a commitment made in advance. A claim tree that records which result *tested*
a prediction, and never whether the test came out for or against it, has recorded the setup
and dropped the result.

`tests` is neutral on purpose -- `X tests P` says X bears on P, not which way it went. The
vocabulary has a positive counterpart, `confirms`, used 74 times corpus-wide. What it has no
counterpart for is failure: nothing in the vocabulary says "the result came out against this
prediction". `contradicts` and `rules-out` do not fill the gap, because both assert the target
is *false*, and a refuted prediction is not a false statement -- it was a correct derivation
from its hypothesis, and what the failure damages is the hypothesis, one edge upstream.

So the corpus can record that a prediction succeeded and cannot record that one failed. Every
tree we publish will look like a paper whose predictions all worked out.

WHAT THIS DOES, AND WHAT IT DELIBERATELY DOES NOT

It classifies each prediction by the *shape of the graph around it* -- which edges point at it,
and whether the prediction's own text enumerates more commitments than it has edges. That is
mechanical and checkable.

It does NOT judge whether a testing result actually matches the prediction it is wired to.
That is a semantic reading, it needs an agent or a person, and a rule that guessed at it would
launder a judgement as a measurement. Where the reading is what matters, this abstains and
says so.

THE RULE, v2

  recorded            a `confirms` edge exists, and if the prediction enumerates conjuncts,
                      there are at least as many outcome edges as conjuncts.
  unrecorded          `tests` edges exist, no `confirms`. The outcome is not in the graph.
  untested            nothing points at it at all.
  abstain:conjunction the prediction enumerates more commitments than it has edges, so no
                      single verdict can be right about all of them.
  abstain:convention  `confirms` without `tests`. Two conventions are in use in this corpus
                      and this prediction follows the other one; which is correct is the
                      question this layer asks, so the rule must not assume an answer.

v1 of the rule matched enumerated conjuncts by roman numeral only and found 4. v2 adds
`(a)(b)(c)` and finds 6 -- the two it had missed include the largest conjunction in the
corpus, a four-part prediction with nine testing results. The version is recorded in the
manifest because an approval is granted to a rule version, not to a rule.

Usage:
  python3 scripts/prediction_outcome.py                 # summary across the corpus
  python3 scripts/prediction_outcome.py --write         # regenerate the manifest
  python3 scripts/prediction_outcome.py --bucket unrecorded   # list one bucket
  python3 scripts/prediction_outcome.py <paper-slug>
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export_mira import CLAIMS_DIR, load_paper, public_papers, relations  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "review", "prediction-outcome.json")

RULE_VERSION = 2

# An outcome edge says how a test came out. `confirms` is the only one that exists; the
# absence of a negative counterpart is the finding, not an oversight in this list.
OUTCOME = {"confirms"}
NEUTRAL = {"tests"}

# Predictions enumerate their commitments two ways. v1 knew only the first.
ENUMERATORS = (
    re.compile(r"\((i{1,3}|iv|v)\)"),
    re.compile(r"\(([a-e])\)"),
)

BUCKETS = {
    "recorded": (
        "The graph says how the test came out. A `confirms` edge points at the prediction "
        "from the result that settled it."),
    "unrecorded": (
        "A result is wired to the prediction with `tests`, which is neutral, and nothing "
        "records the outcome. The paper asserts the result, so a reader would infer the "
        "prediction was met -- but that inference is the reader's, not the graph's."),
    "untested": (
        "Nothing points at this prediction at all. It was derived from a hypothesis and then "
        "left unconnected to any result."),
    "abstain:conjunction": (
        "The prediction states more commitments than it has edges -- \"should show (i)... "
        "(ii)... (iii)...\" with fewer results wired than parts. One verdict cannot be right "
        "about all of them, so the rule declines rather than picking the majority."),
    "abstain:convention": (
        "`confirms` without `tests`. Two conventions for wiring outcomes are in use across "
        "this corpus, and this prediction follows the one that omits the neutral edge. Which "
        "is correct is the question this layer asks, so the rule must not assume an answer."),
}


def conjuncts(text: str) -> list[str]:
    """Enumerated commitments in a prediction's own words, by whichever scheme it used."""
    for pat in ENUMERATORS:
        found = sorted(set(m.lower() for m in pat.findall(text)))
        if len(found) >= 2:
            return found
    return []


def classify(pred: dict, incoming: dict[str, list[str]]) -> tuple[str, dict]:
    """Bucket one prediction, and return the evidence the bucket was chosen on."""
    tests = sorted(incoming.get("tests", []))
    confirms = sorted(incoming.get("confirms", []))
    parts = conjuncts(pred.get("claim", "") or "")
    ev = {"tests": tests, "confirms": confirms, "conjuncts": parts}

    if confirms and not tests:
        return "abstain:convention", ev
    if parts and max(len(tests), len(confirms)) < len(parts):
        return "abstain:conjunction", ev
    if confirms:
        return "recorded", ev
    if tests:
        return "unrecorded", ev
    return "untested", ev


def scan(slugs: list[str]) -> list[dict]:
    """Every prediction in these papers, bucketed. Order is stable so the manifest diffs."""
    items = []
    for paper in slugs:
        if not os.path.isdir(os.path.join(CLAIMS_DIR, paper)):
            continue
        claims = load_paper(paper)
        incoming: dict[str, dict[str, list[str]]] = collections.defaultdict(
            lambda: collections.defaultdict(list))
        for c in claims:
            for key, target in relations(c):
                if key in OUTCOME or key in NEUTRAL:
                    incoming[target][key].append(c["slug"])
        for c in sorted(claims, key=lambda x: x["slug"]):
            if c.get("role") != "prediction":
                continue
            bucket, ev = classify(c, incoming.get(c["slug"], {}))
            items.append({
                "paper": paper,
                "prediction": c["slug"],
                "bucket": bucket,
                "claim": " ".join((c.get("claim") or "").split()),
                **ev,
            })
    return items


def conventions(items: list[dict]) -> dict[str, dict[str, int]]:
    """Which wiring convention each paper used. The split is the finding."""
    out: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for it in items:
        t, c = bool(it["tests"]), bool(it["confirms"])
        name = ("tests+confirms" if t and c else "confirms only" if c
                else "tests only" if t else "neither")
        out[it["paper"]][name] += 1
    return {p: dict(v) for p, v in sorted(out.items())}


def build(slugs: list[str]) -> dict:
    items = scan(slugs)
    counts = collections.Counter(i["bucket"] for i in items)
    return {
        "layer": "prediction-outcome",
        "rule_version": RULE_VERSION,
        "papers": len(slugs),
        "predictions": len(items),
        "buckets": {b: counts.get(b, 0) for b in BUCKETS},
        "bucket_notes": BUCKETS,
        "conventions": conventions(items),
        "items": items,
    }


def write(data: dict) -> bool:
    """Write the manifest. Returns whether anything changed, so a no-op run is visibly a
    no-op rather than a fresh timestamp on identical content."""
    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    new = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    old = None
    if os.path.isfile(MANIFEST):
        with open(MANIFEST, encoding="utf-8") as fh:
            old = fh.read()
    if old == new:
        return False
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        fh.write(new)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper", nargs="?")
    ap.add_argument("--write", action="store_true", help="regenerate review/prediction-outcome.json")
    ap.add_argument("--bucket", help="list the items in one bucket")
    a = ap.parse_args()

    slugs = [a.paper] if a.paper else public_papers()
    data = build(slugs)

    if a.write:
        changed = write(data)
        print(f"{MANIFEST}: {'updated' if changed else 'unchanged'} "
              f"(rule v{RULE_VERSION}, {data['predictions']} predictions)")

    if a.bucket:
        for it in data["items"]:
            if it["bucket"] != a.bucket:
                continue
            print(f"\n{it['paper']} :: {it['prediction']}")
            print(f"  tests={it['tests'] or '—'}")
            print(f"  confirms={it['confirms'] or '—'}")
            if it["conjuncts"]:
                print(f"  conjuncts={it['conjuncts']}")
        return 0

    print(f"rule v{RULE_VERSION} · {data['predictions']} predictions "
          f"across {data['papers']} papers\n")
    for b in BUCKETS:
        n = data["buckets"][b]
        bar = "█" * n
        print(f"  {b:22s} {n:3d}  {bar}")
    print("\nwiring convention by paper")
    for p, d in data["conventions"].items():
        if d:
            print(f"  {p:34s} {d}")
    abst = sum(v for k, v in data["buckets"].items() if k.startswith("abstain"))
    print(f"\n{abst} abstention(s) — the rule declines these rather than guessing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
