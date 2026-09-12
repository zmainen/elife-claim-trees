#!/usr/bin/env python3
"""Gather the scorecards into one manifest — the evaluation layer's output.

`evaluate score` writes a scorecard per (paper, profile) under `runs/<paper>/evaluation/`, in
the scorer's own format: how a candidate claim tree, produced under one model profile, scored
against the best reference available for that paper. This script reads every one of them into
`review/evaluation.json`, the corpus-scope `evaluation` layer's produced file — profile × paper
× metric, with the reference it was scored against and whether that reference was approved.

Read rather than recomputed downstream: `corpus_facts.py` reads this manifest into
`evaluation_*` tokens, and `/pipeline/evaluation/` renders it. A scorecard that lives on the
site is one nobody has to remember to regenerate, and a second implementation of the metrics
here would be a second answer to the question `evaluate` already answers.

WHAT A ROW IS

One row is one (paper, profile) cell. A cell with a scorecard is `scored` and carries its
metrics; a canonical profile with no scorecard for a paper that was swept is `not run` and
says why — so the table shows what is missing rather than omitting it. The model sweep (#85)
has four profiles, and only the zero-cost ones (`subagent`, and the experiments) can run until
a paid backend has credit; the rest appear as `not run: no backend credit`.

Usage:
  python3 scripts/evaluation_report.py            # summary across the corpus
  python3 scripts/evaluation_report.py --write     # regenerate review/evaluation.json
  python3 scripts/evaluation_report.py <paper>     # one paper's rows
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "runs")
MANIFEST = os.path.join(ROOT, "review", "evaluation.json")

# The profiles the sweep varies (config.PROFILES). A canonical profile with no scorecard for a
# swept paper is a row that says "not run", so the table names what a paid backend would fill.
CANONICAL_PROFILES = ["frontier", "standard", "open", "subagent"]

# Only these need a paid backend today; `subagent` is the zero-cost path and stays runnable.
NEEDS_BACKEND = {"frontier", "standard", "open"}

# The metrics a row carries, in display order. Percent metrics are integers 0-100; counts are
# raw. Absent values are null, not zero — a metric that was not measured is not a score of 0.
PERCENT_METRICS = ["recovery", "precision", "role", "panel", "edge_recovery"]


def _pct(num: int, den: int) -> int | None:
    return round(num / den * 100) if den else None


def _row_from_card(card: dict) -> dict:
    """One scored row, computed from a PaperScorecard-format dict."""
    n_ref = card.get("n_ref", 0)
    n_cli = card.get("n_cli", 0)
    n_rec = card.get("n_recovered", 0)
    n_ref_edges = card.get("n_ref_edges_on_matched", 0)
    ev = card.get("evidence_verified") or {}
    return {
        "status": "scored",
        "reference": card.get("reference", "unapproved"),
        "approved": str(card.get("reference", "")).startswith("approved"),
        "n_ref": n_ref,
        "n_cli": n_cli,
        "recovery": _pct(n_rec, n_ref),
        "precision": _pct(card.get("n_cli_matched", 0), n_cli),
        "role": _pct(card.get("n_role_match", 0), n_rec),
        "panel": _pct(card.get("n_panel_match", 0), n_rec),
        "edge_recovery": _pct(card.get("n_edge_recovered", 0), n_ref_edges),
        "n_ref_edges": n_ref_edges,
        "parts": card.get("n_cli_parts", 0),
        # Cost and tokens are recorded when the run made real calls; a subagent-answered run
        # cost nothing, which is a fact worth carrying rather than a blank.
        "cost_usd": card.get("cost_usd"),
        "tokens": card.get("tokens"),
        "evidence_quotes": ev.get("quotes"),
        "evidence_verified": ev.get("verified"),
        "note": card.get("note") or "",
        "error": card.get("error"),
    }


def _load_cards(paper: str) -> dict[str, dict]:
    """Every scorecard under runs/<paper>/evaluation/, keyed by its profile.

    A scorecard names its profile in the `profile` field; the filename is a convenience only.
    An experiment (the fourth reading, scaffolding-versus-model) names itself there too and so
    gets its own row alongside the canonical profiles.
    """
    out: dict[str, dict] = {}
    for path in sorted(glob.glob(os.path.join(RUNS, paper, "evaluation", "*.scorecard.json"))):
        try:
            with open(path, encoding="utf-8") as fh:
                card = json.load(fh)
        except (json.JSONDecodeError, OSError):
            continue
        prof = card.get("profile") or os.path.basename(path).split(".scorecard.json")[0]
        out[prof] = card
    return out


def _swept_papers() -> list[str]:
    """Papers with at least one scorecard — the ones the sweep has touched."""
    papers = []
    if not os.path.isdir(RUNS):
        return papers
    for paper in sorted(os.listdir(RUNS)):
        if glob.glob(os.path.join(RUNS, paper, "evaluation", "*.scorecard.json")):
            papers.append(paper)
    return papers


def build(slugs: list[str] | None = None) -> dict:
    papers = slugs if slugs is not None else _swept_papers()
    rows: list[dict] = []
    for paper in papers:
        cards = _load_cards(paper)
        # Canonical profiles first, in a stable order; a missing one is a `not run` row.
        for prof in CANONICAL_PROFILES:
            if prof in cards:
                rows.append({"paper": paper, "profile": prof, **_row_from_card(cards[prof])})
            else:
                rows.append({
                    "paper": paper, "profile": prof, "status": "not run",
                    "note": "no backend credit" if prof in NEEDS_BACKEND else "not scored yet",
                })
        # Experiments and any non-canonical profile: whatever scorecards remain.
        for prof in sorted(cards):
            if prof in CANONICAL_PROFILES:
                continue
            rows.append({"paper": paper, "profile": prof, **_row_from_card(cards[prof])})

    scored = [r for r in rows if r["status"] == "scored"]
    return {
        "layer": "evaluation",
        "papers": papers,
        "profiles": CANONICAL_PROFILES,
        "percent_metrics": PERCENT_METRICS,
        "rows": rows,
        # Flat scalars the site's one-level {{token}} resolver can reach from `found` prose.
        "n_papers": len(papers),
        "n_rows": len(rows),
        "n_scored": len(scored),
        "n_not_run": sum(1 for r in rows if r["status"] == "not run"),
        "best_recovery": max((r["recovery"] for r in scored
                              if r.get("recovery") is not None), default=0),
    }


def write(data: dict) -> bool:
    """Write the manifest, returning whether anything changed (a no-op run stays a no-op)."""
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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper", nargs="?")
    ap.add_argument("--write", action="store_true", help="regenerate review/evaluation.json")
    a = ap.parse_args()

    slugs = [a.paper] if a.paper else None
    data = build(slugs)

    if a.write:
        changed = write(data)
        print(f"{MANIFEST}: {'updated' if changed else 'unchanged'} "
              f"({data['n_scored']} scored, {data['n_not_run']} not run, "
              f"{data['n_papers']} paper(s))")

    print(f"\nevaluation — {data['n_scored']} scored row(s) across {data['n_papers']} paper(s)\n")
    for r in data["rows"]:
        if r["status"] == "scored":
            print(f"  {r['paper']:28s} {r['profile']:16s} "
                  f"recovery={r['recovery']}% precision={r['precision']}% "
                  f"role={r['role']}% panel={r['panel']}%  vs {r['reference']}")
        else:
            print(f"  {r['paper']:28s} {r['profile']:16s} not run: {r['note']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
