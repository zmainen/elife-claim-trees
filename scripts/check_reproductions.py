#!/usr/bin/env python3
"""Check every claim's reproduction record against the gate.

A reproduction record is supposed to answer one question: *can a reader get from
this claim to the code and data that would settle it?* Most records in this
corpus do not. They record that a script exists and roughly how long it takes to
run — effort — without recording what data it ran on or what number came out.

Two schemas grew side by side. The corpus-wide one (187 records, all ten papers)
carries `script`, `original_script`, `script_execution`, `time_fast`,
`time_full`. Five records, all in one paper, additionally carry `function`,
`data_source`, `data_commit`, `data_file`, `paper_value` and `reproduced_value`
— the fields that make a record evidence rather than a status. This script makes
that difference visible and countable instead of leaving it to be discovered.

The gate is deliberately simple:

  a record that claims the analysis RAN     must say what it ran on and what came out
  a record that says it could NOT run       must say what blocked it
  a record that was never attempted         must say only that

Usage:
  python3 scripts/check_reproductions.py                 # every published paper
  python3 scripts/check_reproductions.py <paper-slug>
  python3 scripts/check_reproductions.py --strict        # exit 1 if any record fails
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter, defaultdict

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required:  pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAIMS_DIR = os.path.join(ROOT, "claims")

# ── The vocabulary ───────────────────────────────────────────────────────────
# Fourteen distinct status strings had accreted across 187 records, several of
# them used once (`N/A`, `verified:with-nuance`, `partial:zenodo-data-downloaded`).
# That is not a vocabulary, it is a history of individual decisions. Five states
# cover every case, and the distinctions the long tail was reaching for belong in
# `notes` or in `blocked_by`, where they can be counted.

STATUS = {
    "verified":    "the analysis was run and the reproduced value matches the paper",
    "partial":     "the analysis was run and reproduces part of the claim",
    "mismatch":    "the analysis was run and the values disagree",
    "blocked":     "the analysis could not be run; `blocked_by` says why",
    "unattempted": "nobody has tried",
}

BLOCKED_BY = {
    "no-data":            "the data is not deposited, or not reachable",
    "no-code":            "the analysis code is not published",
    "code-error":         "the published code does not run",
    "compute-infeasible": "running it needs resources we do not have",
    "not-applicable":     "the claim is not the kind of thing code can settle",
}

# What a record must carry to count as evidence rather than an assertion.
RAN = ("verified", "partial", "mismatch")
CHAIN = {
    "script":           "our script that re-runs the analysis",
    "data_source":      "where the data came from — repository, archive or DOI",
    "data_file":        "the specific file the value was read from",
    "paper_value":      "what the paper reports",
    "reproduced_value": "what the re-run produced",
}
RECOMMENDED = {
    "function":    "the function and line that produces the value",
    "data_commit": "the commit or version of the data source",
}

# ── Who is expected to have a record ─────────────────────────────────────────
# "19 of 27 claims have a reproduction record" is not a finding, because the
# denominator is wrong. A hypothesis is not the kind of thing a script settles —
# it is the proposition the paper's evidence bears on, and asking for its
# reproduced value is a category error, not a gap. Reporting one number over all
# claims makes a complete corpus look incomplete and hides which absences matter.
#
# Eligible: roles that assert something a re-run could confirm or contradict.
# Not eligible: roles that frame, scope, interpret or cite.

ELIGIBLE = {"empirical", "control"}
NOT_ELIGIBLE = {
    "hypothesis":         "a proposition the evidence bears on, not a measurement",
    "prediction":         "what the hypothesis entails; its test is the empirical claim",
    "scope":              "a boundary condition, settled by the paper's own description",
    "methodological":     "a procedure, not a result",
    "interpretation":     "a reading of results, not a result",
    "synthesis":          "an aggregation across claims",
    "assessment":         "a judgement about the work",
    "literature-context": "an assertion about another paper",
}


LEGACY_STATUS = {
    "verified": "verified",
    "verified:partial": "partial",
    "verified:interpretive": "partial",
    "verified:with-nuance": "partial",
    "verified:direction-and-trend": "partial",
    "partial:zenodo-data-downloaded": "partial",
    "unverified:partial": "partial",
    "failed:mismatch": "mismatch",
    "unverified:no-data": "blocked",
    "unverified:no-code": "blocked",
    "unverified:code-error": "blocked",
    "unverified:compute-infeasible": "blocked",
    "unverified": "unattempted",
    "N/A": "unattempted",
}
LEGACY_BLOCKED = {
    "unverified:no-data": "no-data",
    "unverified:no-code": "no-code",
    "unverified:code-error": "code-error",
    "unverified:compute-infeasible": "compute-infeasible",
    "N/A": "not-applicable",
}


def load_frontmatter(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    body = re.sub(r"^([A-Za-z0-9_-]+):\n(\[\]|\{\})\s*$", r"\1: \2", m.group(1), flags=re.M)
    try:
        return yaml.safe_load(body)
    except yaml.YAMLError:
        return None


def papers():
    man = os.path.join(ROOT, "corpus.yaml")
    data = yaml.safe_load(open(man, encoding="utf-8")) or {}
    for name, c in (data.get("corpora") or {}).items():
        if c.get("public") and c.get("in_site_corpus", True):
            return sorted(c.get("papers") or [])
    return []


def check_record(rec: dict, *, history: bool = False) -> list[str]:
    """Everything wrong with one record, in plain language.

    `history=True` for a superseded attempt: it must use the vocabulary, but is
    not required to carry the evidence chain, because it is a record of what was
    tried rather than a claim standing today.
    """
    problems = []
    status = rec.get("status")

    if status in LEGACY_STATUS and status not in STATUS:
        problems.append(f"legacy status {status!r} — now {LEGACY_STATUS[status]!r}")
        status = LEGACY_STATUS[status]
    elif status not in STATUS:
        problems.append(f"unknown status {status!r}")
        return problems

    if status == "blocked":
        by = rec.get("blocked_by")
        if not by:
            problems.append("blocked, but does not say what blocked it")
        elif by not in BLOCKED_BY:
            problems.append(f"unknown blocked_by {by!r}")

    if status in RAN and not history:
        missing = [f for f in CHAIN if not rec.get(f)]
        if missing:
            problems.append("claims the analysis ran but does not record "
                            + ", ".join(missing))
        thin = [f for f in RECOMMENDED if not rec.get(f)]
        if thin and not missing:
            problems.append("no " + ", ".join(thin) + " (recommended)")

    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper", nargs="?",
                    help="paper slug (default: the paper the current layer covers)")
    ap.add_argument("--corpus", action="store_true",
                    help="every published paper. These records are the March-April pass, "
                         "written against the older schema — the totals describe that layer, "
                         "not this one.")
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero if any record fails the gate")
    ap.add_argument("--verbose", "-v", action="store_true",
                    help="list every failing record, not just the counts")
    a = ap.parse_args()

    CURRENT_LAYER = "gadeke-2026-guilt-insula"
    if a.paper:
        slugs = [a.paper]
    elif a.corpus:
        slugs = papers()
    else:
        slugs = [CURRENT_LAYER]
    status_counts = Counter()
    gate = Counter()
    eligible = Counter(); extra_records = Counter()
    elig_total = 0; elig_with = 0
    per_paper = defaultdict(lambda: Counter())
    failures = []

    for slug in slugs:
        d = os.path.join(CLAIMS_DIR, slug)
        if not os.path.isdir(d):
            print(f"no such paper: {slug}", file=sys.stderr)
            return 2
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md") or fn == "index.md":
                continue
            fm = load_frontmatter(os.path.join(d, fn)) or {}
            role = fm.get("role") or fm.get("claim-type") or "empirical"
            eligible[role if role in ELIGIBLE else "—not eligible—"] += 1
            recs = [r for r in (fm.get("reproductions") or []) if isinstance(r, dict)]
            if role in ELIGIBLE:
                elig_total += 1
                if recs:
                    elig_with += 1
            elif recs:
                extra_records[role] += 1
            # A claim accumulates verification attempts. The gate judges the CURRENT one —
            # the most recent by date — and treats the rest as history: an earlier attempt
            # that reached a weaker conclusion is a record of what was tried, not a claim
            # standing today, and holding it to the same bar would punish keeping the trail.
            # History still has to use the vocabulary; it just need not carry the chain.
            current = max(recs, key=lambda r: str(r.get("date", "")), default=None)
            for rec in recs:
                raw = rec.get("status")
                status_counts[raw] += 1
                probs = check_record(rec) if rec is current else check_record(rec, history=True)
                ok = not probs
                gate["passes" if ok else "fails"] += 1
                per_paper[slug]["passes" if ok else "fails"] += 1
                if not ok:
                    failures.append((slug, fm.get("slug", fn), raw, probs))

    total = sum(gate.values())
    print(f"=== Reproduction records — {len(slugs)} paper(s), {total} record(s) ===")
    if len(slugs) > 1:
        print("    (the March–April pass, written against the older schema —\n"
              "     these totals describe that layer, not the current one)")
    print()
    print(f"  meet the gate : {gate['passes']}")
    print(f"  do not        : {gate['fails']}\n")

    print(f"  claims a re-run could settle (empirical, control): {elig_total}")
    print(f"    with a record : {elig_with}")
    print(f"    without       : {elig_total - elig_with}")
    if extra_records:
        print("  records on roles a re-run cannot settle "
              "(fine — usually 'blocked / not-applicable'):")
        for r, n in extra_records.most_common():
            print(f"    {r:22} {n}")
    print()
    print("  by paper:")
    for slug in slugs:
        c = per_paper[slug]
        n = c["passes"] + c["fails"]
        if n:
            print(f"    {slug:38} {c['passes']:>3}/{n:<3} pass")

    print("\n  status values in use:")
    for s, n in status_counts.most_common():
        note = "" if s in STATUS else "   ← legacy"
        print(f"    {str(s):32} {n:>4}{note}")

    if a.verbose and failures:
        print(f"\n  failing records ({len(failures)}):")
        for slug, claim, raw, probs in failures[:60]:
            print(f"    [{slug}] {claim}")
            for p in probs:
                print(f"        · {p}")
        if len(failures) > 60:
            print(f"    … and {len(failures) - 60} more")

    if a.strict and gate["fails"]:
        print(f"\nFAIL: {gate['fails']} record(s) do not meet the gate.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
