#!/usr/bin/env python3
"""Emit what the extraction agents did, for the site to render.

The corpus is produced by language models end to end and checked by no human. A site that
says so in a sentence and shows nothing is asking to be taken on trust. This emits the actual
record: which agent role read which part of the paper, under which prompt, using which model,
what each proposed, the verbatim sentence it based each claim on, and where the agents
disagreed.

Only one paper has this record. The other nine were extracted before agent runs were saved,
so `extract/out/` holds a draft and an agent file for Gaedeke alone. The generated data says
which papers have a trace so the pages can state that rather than render empty templates.

Writes `site/src/data/agents.json`:

  roles       the seven roles, each with its prompt text read from extract/prompts/
  papers      per paper: per-agent counts, the model used, and every drafted claim with the
              agents that proposed it and the evidence each quoted
  agreement   how many claims more than one reader found

Usage:
  python3 scripts/agents_report.py
  python3 scripts/agents_report.py --print
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS = os.path.join(ROOT, "extract", "prompts")
# The extraction record is read from runs/, which is tracked, rather than extract/out/, which
# extract/.gitignore excludes. Both hold the same thing — runs/<paper>/<role>-reader.output.json
# is byte-for-byte the block that extract/out/agents-<paper>.json keys by role, and
# reconciler.output.json is the draft. Reading the ignored copy made this page unreproducible:
# the data existed on one machine, in a directory git was told to forget, and regenerating
# anywhere else silently emptied the page it feeds. extract/out/ is still read as a fallback so
# a fresh extraction run works before its outputs are filed into runs/.
RUNS_DIR = os.path.join(ROOT, "runs")
OUT_DIR = os.path.join(ROOT, "extract", "out")
READER_FILE = {"results": "results-reader", "caption": "caption-reader",
               "structure": "structure-reader"}
OUT = os.path.join(ROOT, "site", "src", "data", "agents.json")

# The pipeline in order. `stage` groups them: three readers work in parallel on different
# slices of the paper, then the rest run in sequence over their output.
ROLES = [
    {"id": "results-reader", "stage": "read", "reads": "the Results section",
     "returns": "candidate claims, each with a panel, a role and the sentence it rests on",
     "agent_key": "results"},
    {"id": "caption-reader", "stage": "read", "reads": "figure and table captions",
     "returns": "candidate claims anchored to the panel they describe",
     "agent_key": "caption"},
    {"id": "structure-reader", "stage": "read", "reads": "the abstract and section structure",
     "returns": "candidate claims the paper frames as its own conclusions",
     "agent_key": "structure"},
    {"id": "reconciler", "stage": "reconcile",
     "reads": "all three readers' output",
     "returns": "one draft table, each claim tagged by how many readers proposed it",
     "agent_key": None},
    {"id": "external-reviewer", "stage": "reconcile",
     "reads": "the draft table and the paper",
     "returns": "a revised table — this is what stands in for a human review step",
     "agent_key": None},
    {"id": "edge-inference", "stage": "relate", "reads": "the reconciled claims",
     "returns": "typed relations between them — the deductive spine",
     "agent_key": None},
    {"id": "coverage-adjudicator", "stage": "cover",
     "reads": "unmatched spans of the paper and the claim tree",
     "returns": "a covered / gap / no-assertion verdict for each span",
     "agent_key": None},
]


def prompt_text(role_id):
    p = os.path.join(PROMPTS, f"{role_id}.md")
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def _load(*candidates):
    """First of these paths that exists, parsed. None if none do."""
    for p in candidates:
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as fh:
                return json.load(fh)
    return None


def paper_trace(slug):
    draft = _load(os.path.join(RUNS_DIR, slug, "reconciler.output.json"),
                  os.path.join(OUT_DIR, f"draft-{slug}.json"))
    if draft is None:
        return None

    models = {}
    for key, fname in READER_FILE.items():
        block = _load(os.path.join(RUNS_DIR, slug, f"{fname}.output.json"))
        if block:
            models[key] = block.get("model")
    if not models:
        agents = _load(os.path.join(OUT_DIR, f"agents-{slug}.json")) or {}
        models = {k: b.get("model") for k, b in agents.items() if isinstance(b, dict)}

    claims = []
    for c in draft.get("claims", []):
        claims.append({
            "claim": c.get("claim"),
            "panel": c.get("panel"),
            "role": c.get("role"),
            "confidence": c.get("confidence"),
            "sources": sorted(c.get("sources") or []),
            "evidence_by_agent": c.get("evidence_by_agent") or {},
        })

    by_n = Counter(len(c["sources"]) for c in claims)
    return {
        "paper_slug": slug,
        "paper_title": draft.get("paper_title"),
        "paper_doi": draft.get("paper_doi"),
        "extraction_path": draft.get("extraction_path"),
        "per_agent_counts": draft.get("per_agent_counts") or {},
        "models": models,
        "config": draft.get("config_snapshot") or {},
        "claims": claims,
        "drafted": len(claims),
        "found_by_one": by_n.get(1, 0),
        "found_by_more": sum(v for n, v in by_n.items() if n > 1),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--print", dest="show", action="store_true")
    a = ap.parse_args()

    roles = []
    for r in ROLES:
        text = prompt_text(r["id"])
        roles.append({**r, "prompt": text,
                      "prompt_lines": len(text.splitlines()) if text else 0,
                      "prompt_path": f"extract/prompts/{r['id']}.md" if text else None})

    slugs = sorted(
        {d for d in os.listdir(RUNS_DIR)
         if os.path.isfile(os.path.join(RUNS_DIR, d, "reconciler.output.json"))}
        if os.path.isdir(RUNS_DIR) else set()
        | ({f[len("draft-"):-len(".json")]
            for f in os.listdir(OUT_DIR) if f.startswith("draft-")}
           if os.path.isdir(OUT_DIR) else set()))
    papers = {s: paper_trace(s) for s in slugs}
    papers = {k: v for k, v in papers.items() if v}

    data = {"roles": roles, "papers": papers, "papers_with_trace": sorted(papers)}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
        fh.write("\n")

    missing = [r["id"] for r in roles if not r["prompt"]]
    print(f"agents → {os.path.relpath(OUT, ROOT)}")
    print(f"  {len(roles)} roles, {len(roles) - len(missing)} with a committed prompt"
          + (f" — missing: {', '.join(missing)}" if missing else ""))
    for s, p in papers.items():
        print(f"  {s}: {p['drafted']} drafted claims · "
              f"{p['found_by_more']} found by more than one reader · "
              f"{', '.join(f'{k} {v}' for k, v in p['per_agent_counts'].items())}")
    if not papers:
        print("  no paper has a saved agent trace")
    if a.show:
        print(json.dumps({k: v for k, v in data.items() if k != "roles"}, indent=2)[:2000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
