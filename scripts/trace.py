#!/usr/bin/env python3
"""Trace a paper's claims: span → claim → code → data, and why the rest stopped.

The corpus can already say a claim was verified. It could not, until now, let a
reader *follow* that: which sentence of the paper the claim covers, which
function re-ran the analysis, which deposited file it read, and what came out
beside what the paper printed. Nor could it say, for the claims with no such
record, what stopped at which step.

Every link this emits is constructed from fields and checked, because a
provenance link that 404s is worse than none — it looks like evidence. On the
first run, four of five data links did not resolve: `data_file` held a path
followed by prose ("Code/csv/ — single-trial happiness tables, both cohorts…"),
so the field read as structured and was not.

Usage:
  python3 scripts/trace.py gadeke-2026-guilt-insula
  python3 scripts/trace.py <slug> --marked <file.marked.md>   # include spans
  python3 scripts/trace.py <slug> --check-links               # resolve every URL
  python3 scripts/trace.py <slug> --json out.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
from collections import Counter

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required:  pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAIMS_DIR = os.path.join(ROOT, "claims")

MARK_RE = re.compile(r"⟦>[a-z0-9_-]*(?:\.[0-9a-z]{4,6})?[^:⟧]*claim=([^\s:⟧]+):\s*@\{(.*?)\}",
                     re.DOTALL)
FUNC_RE = re.compile(r"^\s*(\w+)\(\).*?line\s+(\d+)", re.I)


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


def load_paper(slug):
    d = os.path.join(CLAIMS_DIR, slug)
    out = []
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".md") and fn != "index.md":
            fm = load_frontmatter(os.path.join(d, fn))
            if fm and fm.get("slug"):
                out.append(fm)
    return out


def data_links(rec):
    """Deep links into the deposited data, one per file the record names.

    A repository plus a commit plus a path is a permanent address; without the
    commit it is a moving target, which is why `data_commit` is recommended and
    its absence is reported rather than papered over.
    """
    src = (rec.get("data_source") or "").rstrip("/")
    if not src or "github.com" not in src:
        return []
    commit = rec.get("data_commit")
    files = rec.get("data_file")
    files = files if isinstance(files, list) else ([files] if files else [])
    out = []
    for f in files:
        f = str(f).strip()
        if not f:
            continue
        ref = commit or "HEAD"
        out.append({
            "file": f,
            "commit_pinned": bool(commit),
            "url": f"{src}/blob/{ref}/" + urllib.parse.quote(f.rstrip('/')) + ("/" if f.endswith("/") else ""),
        })
    return out


def code_link(rec, repo_url=None):
    """Link to our own verification script, at the line if the record says one."""
    script = rec.get("script")
    if not script:
        return None
    line = None
    m = FUNC_RE.match(str(rec.get("function") or ""))
    if m:
        line = int(m.group(2))
    base = repo_url or "https://github.com/zmainen/elife-claim-trees/blob/main"
    return {"path": script, "line": line,
            "url": f"{base}/{script}" + (f"#L{line}" if line else "")}


def spans_for(marked_text, uuid):
    return [q.strip() for u, q in MARK_RE.findall(marked_text or "") if u == uuid]


def check(url):
    r = subprocess.run(["curl", "-sIL", "-o", "/dev/null", "-w", "%{http_code}", url],
                       capture_output=True, text=True, timeout=30)
    return r.stdout.strip()


def build(slug, marked_text=None):
    rows = []
    for c in load_paper(slug):
        recs = [r for r in (c.get("reproductions") or []) if isinstance(r, dict)]
        cur = max(recs, key=lambda r: str(r.get("date", "")), default=None)
        row = {
            "claim": c["slug"],
            "uuid": c.get("uuid"),
            "role": c.get("role"),
            "text": (c.get("claim") or "").strip(),
            "spans": spans_for(marked_text, c.get("uuid")) if marked_text else [],
            "status": (cur or {}).get("status", "no-record"),
            "blocked_by": (cur or {}).get("blocked_by"),
            "attempts": len(recs),
            "code": code_link(cur) if cur else None,
            "data": data_links(cur) if cur else [],
            "paper_value": (cur or {}).get("paper_value"),
            "reproduced_value": (cur or {}).get("reproduced_value"),
            "why": (cur or {}).get("notes"),
        }
        rows.append(row)
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper")
    ap.add_argument("--marked", help="the paper's .marked.md, to include the spans")
    ap.add_argument("--check-links", action="store_true",
                    help="resolve every constructed URL and report the status code")
    ap.add_argument("--json", help="write the trace as JSON")
    a = ap.parse_args()

    marked = open(a.marked, encoding="utf-8").read() if a.marked else None
    rows = build(a.paper, marked)

    st = Counter(r["status"] for r in rows)
    print(f"=== Trace — {a.paper} ===\n")
    print(f"  {len(rows)} claims · " + " · ".join(f"{v} {k}" for k, v in st.most_common()))
    if marked:
        anchored = sum(1 for r in rows if r["spans"])
        print(f"  {anchored} anchored to at least one span in the paper")
    print()

    for r in sorted(rows, key=lambda r: (r["status"] != "verified", r["claim"])):
        mark = {"verified": "✓", "partial": "~", "mismatch": "!",
                "blocked": "·", "unattempted": "·", "no-record": " "}.get(r["status"], " ")
        print(f"  {mark} {r['claim']}")
        print(f"      {r['status']}" + (f" ({r['blocked_by']})" if r["blocked_by"] else "")
              + (f" · {r['attempts']} attempt(s)" if r["attempts"] > 1 else ""))
        if r["spans"]:
            print(f"      span: \"{r['spans'][0][:88]}\"" +
                  (f"  (+{len(r['spans'])-1} more)" if len(r["spans"]) > 1 else ""))
        if r["code"]:
            print(f"      code: {r['code']['url']}")
        for d in r["data"]:
            pin = "" if d["commit_pinned"] else "   ← not pinned to a commit"
            print(f"      data: {d['url']}{pin}")
        if r["paper_value"]:
            print(f"      paper {r['paper_value']}  ·  reproduced {r['reproduced_value']}")
        print()

    if a.check_links:
        print("  resolving every constructed link:")
        bad = 0
        for r in rows:
            for d in r["data"]:
                code = check(d["url"])
                ok = code.startswith("2")
                bad += 0 if ok else 1
                print(f"    {code}  {r['claim'][:34]:36} {d['file'][:52]}")
        print(f"\n  {bad} link(s) did not resolve.")
        if bad:
            return 1

    if a.json:
        open(a.json, "w", encoding="utf-8").write(json.dumps(rows, indent=2, ensure_ascii=False))
        print(f"  written: {a.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
