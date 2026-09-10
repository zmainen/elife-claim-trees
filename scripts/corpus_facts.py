#!/usr/bin/env python3
"""Count the corpus, so no page has to.

Every stale figure on this site was a number somebody typed into a page: "12
papers", "310 claims", "231 claims · 503 typed relations", "the eight-step
process". The counts that stayed correct were the ones generated at build time
from `claims.json`. So the fix is not to correct them again — it is to stop
writing them down.

This emits `site/src/data/corpus-facts.json`, and the methodology page
substitutes `{{token}}` from it while rendering `docs/method.md`. A number in
prose then cannot drift from the corpus, because it is not in the prose.

Scope is the site corpus — the ten eLife papers — because that is what the site
publishes. The two bioRxiv method examples are counted separately and named as
such, never folded into a corpus total.

Usage:
  python3 scripts/corpus_facts.py            # write the file
  python3 scripts/corpus_facts.py --print    # show what it computed
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required:  pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAIMS = os.path.join(ROOT, "claims")
OUT = os.path.join(ROOT, "site", "src", "data", "corpus-facts.json")

SUPPORTS = {"tests", "confirms", "validates", "supports", "extends", "replicates"}
OPPOSES = {"contradicts", "opposes", "dissociates-with", "rules-out"}
GAPS = {"entails", "derived-from", "interprets", "enables-method", "scopes",
        "requires", "qualifies"}
EDGE_KEYS = SUPPORTS | OPPOSES | GAPS

ELIGIBLE_ROLES = {"empirical", "control"}


def frontmatter(path):
    t = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", t, re.S)
    if not m:
        return None
    body = re.sub(r"^([A-Za-z0-9_-]+):\n(\[\]|\{\})\s*$", r"\1: \2", m.group(1), flags=re.M)
    try:
        return yaml.safe_load(body)
    except yaml.YAMLError:
        return None


def corpora():
    data = yaml.safe_load(open(os.path.join(ROOT, "corpus.yaml"), encoding="utf-8")) or {}
    site, examples = [], []
    for name, c in (data.get("corpora") or {}).items():
        if not c.get("public"):
            continue
        (site if c.get("in_site_corpus", True) else examples).extend(c.get("papers") or [])
    return sorted(site), sorted(examples)


def relations(c):
    for k in sorted(EDGE_KEYS):
        for t in (c.get(k) or []):
            if isinstance(t, str):
                yield k
    for item in (c.get("belongings") or []):
        if isinstance(item, dict) and item.get("relation"):
            yield item["relation"]


def scan(slugs):
    claims = 0
    rels = Counter()
    roles = Counter()
    repro = Counter()
    eligible = with_record = 0
    for s in slugs:
        d = os.path.join(CLAIMS, s)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md") or fn == "index.md":
                continue
            fm = frontmatter(os.path.join(d, fn))
            if not fm or not fm.get("slug"):
                continue
            claims += 1
            role = fm.get("role") or fm.get("claim-type") or "empirical"
            roles[role] += 1
            for r in relations(fm):
                rels[r] += 1
            recs = [r for r in (fm.get("reproductions") or []) if isinstance(r, dict)]
            if role in ELIGIBLE_ROLES:
                eligible += 1
                if recs:
                    with_record += 1
            cur = max(recs, key=lambda r: str(r.get("date", "")), default=None)
            if cur:
                repro[cur.get("status", "—")] += 1
    return claims, rels, roles, repro, eligible, with_record


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--print", dest="show", action="store_true")
    a = ap.parse_args()

    site, examples = corpora()
    claims, rels, roles, repro, eligible, with_record = scan(site)
    ex_claims, _, _, _, _, _ = scan(examples)

    verify_scripts = sum(
        1 for s in site if os.path.isfile(os.path.join(ROOT, "verification", s, "verify.py")))

    facts = {
        "papers": len(site),
        "claims": claims,
        "relations": sum(rels.values()),
        "relation_types_used": len(rels),
        "relation_types_defined": len(EDGE_KEYS),
        "roles_used": len(roles),
        "role_counts": dict(roles.most_common()),
        "relation_counts": dict(rels.most_common()),
        "largest_role": roles.most_common(1)[0][0] if roles else None,
        "largest_role_n": roles.most_common(1)[0][1] if roles else 0,
        "verify_scripts": verify_scripts,
        "papers_without_verify": len(site) - verify_scripts,
        # scripts that have been instrumented to emit provenance: Gädeke only
        "papers_without_verify_audit": verify_scripts - 1,
        "eligible_claims": eligible,
        "eligible_with_record": with_record,
        "reproduction_status": dict(repro.most_common()),
        "method_example_papers": len(examples),
        "method_example_claims": ex_claims,
        "site_corpus": site,
        "method_examples": examples,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(facts, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print(f"corpus facts → {os.path.relpath(OUT, ROOT)}")
    print(f"  {facts['papers']} papers · {facts['claims']} claims · "
          f"{facts['relations']} typed relations "
          f"({facts['relation_types_used']} of {facts['relation_types_defined']} types used)")
    print(f"  {facts['eligible_with_record']}/{facts['eligible_claims']} claims a re-run "
          f"could settle have a record")
    print(f"  {facts['method_example_papers']} method-example paper(s), "
          f"{facts['method_example_claims']} claims — counted separately, never in the total")
    if a.show:
        print(json.dumps(facts, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
