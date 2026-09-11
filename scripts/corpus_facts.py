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


def mira_facts(site):
    """What the MIRA export actually does, read from the generated files.

    The standards page carried "57% of typed relations have no MIRA predicate" for weeks. That
    number described an exporter that emitted only supports/opposes; it was never a fact about
    MIRA, whose relation vocabulary is extensible. It stayed live because it was typed into a
    page. So it is computed here instead, and the page reads it.
    """
    lost = inverse = rels = questions = records = 0
    for s in site:
        fj = os.path.join(ROOT, "exports", f"{s}.formats.json")
        if os.path.exists(fj):
            with open(fj, encoding="utf-8") as fh:
                d = json.load(fh)
            rels += d["relations"]
            lost += d["mira"]["lost"]
            inverse += sum(d["mira"]["inverse_only"].values())
        gr = os.path.join(ROOT, "exports", f"{s}.gap-report.md")
        if os.path.exists(gr):
            txt = open(gr, encoding="utf-8").read()
            m = re.search(r"\*\*(\d+) questions were derived", txt)
            if m:
                questions += int(m.group(1))
            m = re.search(r"\*\*(\d+) verification records", txt)
            if m:
                records += int(m.group(1))
    out = {"relations": rels, "lost": lost, "inverse_only": inverse,
           "carried": rels - lost,
           "synthesised_questions": questions, "verification_records": records}
    v = os.path.join(ROOT, "site", "src", "data", "mira-validation.json")
    if os.path.exists(v):
        with open(v, encoding="utf-8") as fh:
            val = json.load(fh)
        out["our_violations"] = val.get("our_violations")
        out["upstream_violations"] = val.get("upstream_violations")
        out["pinned_schema_commit"] = val.get("pinned_schema_commit")
    return out


def dangling_eliminations(site):
    """`rules-out` edges whose target names no claim in the paper.

    Each is an alternative the paper eliminates that has no node to be eliminated — the
    gap the stance layer exists to close, counted rather than asserted. scripts/
    check_relations.py reports the same set individually.
    """
    n = 0
    for s in site:
        d = os.path.join(CLAIMS, s)
        if not os.path.isdir(d):
            continue
        fms = [frontmatter(os.path.join(d, fn)) or {}
               for fn in sorted(os.listdir(d))
               if fn.endswith(".md") and fn != "index.md"]
        known = {fm.get("slug") for fm in fms if fm.get("slug")}
        for fm in fms:
            targets = fm.get("rules-out") or []
            if isinstance(targets, str):
                targets = [targets]
            n += sum(1 for x in targets
                     if isinstance(x, str) and x.strip() not in known and x.strip() != "*")
    return n


def stances(slug):
    """Claims in this paper the paper does not assert, counted by stance.

    A paper's tree can only record what a result rules out if the rival has a node to be,
    and the rival is marked by the stance on its assertion, not by its role or its slug —
    an alternative is functionally a hypothesis, and what makes it a rival is the posture.
    """
    out = {}
    d = os.path.join(CLAIMS, slug)
    if not os.path.isdir(d):
        return out
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md") or fn == "index.md":
            continue
        fm = frontmatter(os.path.join(d, fn)) or {}
        a = (fm.get("assertions") or [{}])[0]
        st = a.get("stance") if isinstance(a, dict) else None
        if st and st != "asserts":
            out[st] = out.get(st, 0) + 1
    return out


def _review_counts():
    """Queue items per paper, from review/*.json — empty when no queue has been generated."""
    total, pending = {}, {}
    d = os.path.join(ROOT, "review")
    if not os.path.isdir(d):
        return total, pending
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".json"):
            continue
        try:
            with open(os.path.join(d, fn), encoding="utf-8") as fh:
                doc = json.load(fh)
        except Exception:                                             # noqa: BLE001
            continue
        for i in doc.get("items", []):
            total[i["paper"]] = total.get(i["paper"], 0) + 1
            if i.get("decision") == "pending":
                pending[i["paper"]] = pending.get(i["paper"], 0) + 1
    return total, pending


def layers(site):
    """Which analytic layer each paper has, detected from the artifacts on disk.

    The corpus is not one flat thing: it is a stack of layers built over the same papers, each
    answering a different question, and they were added at different times and cover different
    subsets. A reader who cannot see which layers a given paper has reads a missing layer as an
    oversight. Presence is detected from files rather than declared, so a paper cannot claim a
    layer it does not have.
    """
    out = {}
    review_counts, pending_counts = _review_counts()
    for s in site:
        has_tree = os.path.isdir(os.path.join(CLAIMS, s))
        prov = os.path.join(ROOT, "verification", s, "provenance.json")
        verified = 0
        if os.path.isfile(prov):
            try:
                with open(prov, encoding="utf-8") as fh:
                    verified = sum(1 for r in json.load(fh).get("results", [])
                                   if r.get("status") == "PASS")
            except Exception:                                         # noqa: BLE001
                verified = 0
        st = stances(s)
        out[s] = {
            "tree": has_tree,
            "verification": os.path.isfile(
                os.path.join(ROOT, "verification", s, "verify.py")),
            "verification_observed": os.path.isfile(prov),
            "verified_results": verified,
            "formats": os.path.isfile(os.path.join(ROOT, "exports", f"{s}.mira.jsonld")),
            "coverage": os.path.isfile(os.path.join(ROOT, "mappings", f"{s}.json")),
            "marked": os.path.isfile(os.path.join(ROOT, "marked", f"{s}.marked.md")),
            "agent_trace": os.path.isfile(os.path.join(ROOT, "mappings", f"{s}.json")),
            "alternatives": bool(st),
            "alternatives_n": sum(st.values()),
            "review": s in review_counts,
            "review_n": review_counts.get(s, 0),
            "review_pending": pending_counts.get(s, 0),
        }
    return out


def mira_mapping():
    """The role and relation mapping, read from the exporter's own tables.

    The site states how each claim role and each relation type is expressed in MIRA. Typing
    that into a page is how it goes stale, so it is read from ROLE_TO_TYPE and RELATION_DEFS
    and shipped as data.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from export_mira import ROLE_TO_TYPE, RELATION_DEFS, INVERSE_PAIRS
    rels = []
    for key, spec in sorted(RELATION_DEFS.items()):
        parent, domain, rng = spec[0], spec[1], spec[2]
        rels.append({
            "relation": key,
            "declared_under": parent,
            "domain": domain,
            "range": rng,
            "description": spec[3] if len(spec) > 3 else "",
            "inverse_of": INVERSE_PAIRS.get(key),
        })
    return {"roles": dict(sorted(ROLE_TO_TYPE.items())), "relations": rels}


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
        "mira": mira_facts(site),
        "mira_mapping": mira_mapping(),
        "layers": layers(site),
        "dangling_rules_out": dangling_eliminations(site),
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(facts, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print(f"corpus facts → {os.path.relpath(OUT, ROOT)}")
    print(f"  {facts['papers']} papers · {facts['claims']} claims · "
          f"{facts['relations']} typed relations "
          f"({facts['relation_types_used']} of {facts['relation_types_defined']} types used)")
    # "133/133 have a record" is true and reads as success. A record can say `blocked` or
    # `unattempted`, and most of them do, so the outcome is printed alongside the coverage --
    # never the coverage alone.
    print(f"  {facts['eligible_with_record']}/{facts['eligible_claims']} claims a re-run "
          f"could settle have a record — "
          + ", ".join(f"{v} {k}" for k, v in facts["reproduction_status"].items()))
    m = facts["mira"]
    print(f"  MIRA: {m['carried']}/{m['relations']} relations carried, {m['lost']} lost, "
          f"{m['our_violations']} violations of ours")
    print(f"  {facts['method_example_papers']} method-example paper(s), "
          f"{facts['method_example_claims']} claims — counted separately, never in the total")
    if a.show:
        print(json.dumps(facts, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
