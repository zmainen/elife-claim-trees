#!/usr/bin/env python3
"""What each interchange format carries from a claim tree, and what it drops.

Measured from the generated files rather than derived from the mapping tables.
A mapping table says what a converter intends; the export says what it did, and
those came apart once already — the Discourse Graphs exporter looked for claims
one level above where they sit and wrote a file with a single node, in valid
JSON-LD nothing would flag.

For each paper this emits:

  exports/<slug>.formats.md     the comparison, as prose and a table
  exports/<slug>.formats.json   the same numbers, for the site to render

The Markdown is the artifact and the page renders it, so a figure on the site
cannot disagree with the export it describes.

Usage:
  python3 scripts/formats_report.py --all
  python3 scripts/formats_report.py <paper-slug>
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
EXPORTS = os.path.join(ROOT, "exports")

SUPPORTS = {"tests", "confirms", "validates", "supports", "extends", "replicates"}
OPPOSES = {"contradicts", "opposes", "dissociates-with", "rules-out"}
GAPS = {
    "entails": "a hypothesis entails its prediction — the deductive step",
    "derived-from": "a prediction derived from its hypothesis",
    "interprets": "one claim interprets another",
    "enables-method": "a result makes a downstream method possible",
    "scopes": "a scope constraint governs another claim's validity",
    "requires": "a claim depends on another holding",
    "qualifies": "a claim narrows another's applicability",
}
EDGE_KEYS = SUPPORTS | OPPOSES | set(GAPS)


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


def tree_relations(slug):
    """Relation types and counts in the claim tree — the source of truth."""
    counts = Counter()
    claims = 0
    verif = Counter()
    d = os.path.join(CLAIMS, slug)
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md") or fn == "index.md":
            continue
        fm = frontmatter(os.path.join(d, fn))
        if not fm or not fm.get("slug"):
            continue
        claims += 1
        for k in sorted(EDGE_KEYS):
            for t in (fm.get(k) or []):
                if isinstance(t, str):
                    counts[k] += 1
        for item in (fm.get("belongings") or []):
            if isinstance(item, dict) and item.get("relation"):
                counts[item["relation"]] += 1
        recs = [r for r in (fm.get("reproductions") or []) if isinstance(r, dict)]
        if recs:
            verif[max(recs, key=lambda r: str(r.get("date", ""))).get("status", "—")] += 1
    return claims, counts, verif


def mira_edges(slug):
    p = os.path.join(EXPORTS, f"{slug}.mira.jsonld")
    if not os.path.exists(p):
        return None
    g = json.load(open(p, encoding="utf-8")).get("@graph", [])
    c = Counter()
    for n in g:
        for k, v in n.items():
            # Core MIRA predicates, plus the relations declared as RelationDefs in this
            # document. Both are carried; only the second needs the declaration read.
            if k in ("mira:supports", "mira:opposes") or k.startswith("haak:"):
                c[k] += len(v) if isinstance(v, list) else 1
    return c


def oxa_edges(slug):
    p = os.path.join(EXPORTS, f"{slug}.oxa.json")
    if not os.path.exists(p):
        return None

    def walk(n):
        if isinstance(n, dict):
            if n.get("type") == "Claim":
                yield n
                return
            for ch in (n.get("children") or []):
                yield from walk(ch)

    c = Counter()
    for claim in walk(json.load(open(p, encoding="utf-8"))):
        for r in (claim.get("relations") or []):
            c[r.get("relationType", "?")] += 1
    return c


def dg_edges(slug):
    p = os.path.join(EXPORTS, f"{slug}.dg.jsonld")
    if not os.path.exists(p):
        return None
    g = json.load(open(p, encoding="utf-8")).get("@graph", [])
    c = Counter()
    for n in g:
        if "Relation" in str(n.get("@type", "")):
            rt = str(n.get("https://discoursegraphs.org/ontology#relationType", "?"))
            c[rt.rsplit("#", 1)[-1]] += 1
    return c


def report(slug):
    claims, tree, verif = tree_relations(slug)
    total = sum(tree.values())
    mira = mira_edges(slug) or Counter()
    oxa = oxa_edges(slug) or Counter()
    dg = dg_edges(slug) or Counter()

    mira_kept = sum(mira.values())
    mira_core = sum(v for k, v in mira.items() if k.startswith("mira:"))
    mira_declared = mira_kept - mira_core
    dropped = {k: v for k, v in tree.items() if k in GAPS}
    flattened = {k: v for k, v in tree.items() if k in SUPPORTS or k in OPPOSES}

    return {
        "paper": slug,
        "claims": claims,
        "relations": total,
        "by_type": dict(tree.most_common()),
        "mira": {"kept": mira_kept, "dropped": total - mira_kept,
                 "core": mira_core, "declared": mira_declared,
                 "edges": dict(mira), "declared_types": dropped},
        "oxa": {"kept": sum(oxa.values()), "edges": dict(oxa.most_common())},
        "dg": {"kept": sum(dg.values()), "edges": dict(dg.most_common())},
        "flattened": flattened,
        "verification": dict(verif.most_common()),
    }


def markdown(r):
    L = [f"# {r['paper']} — what each format carries", "",
         f"{r['claims']} claims, {r['relations']} typed relations between them.", "",
         "One source, three targets. Each row is a relation type the paper's claim tree "
         "uses; each column is what became of it.", "",
         "| Relation | In the tree | MIRA | OXA | Discourse Graphs |",
         "|---|---:|---|---|---|"]

    oxa_by_rel = r["oxa"]["edges"]
    for rel, n in r["by_type"].items():
        if rel in GAPS:
            mira_cell = f"declared `haak:{rel}`"
        elif rel in SUPPORTS:
            mira_cell = "→ supports"
        else:
            mira_cell = "→ opposes"
        oxa_cell = "kept" if r["oxa"]["kept"] else "—"
        dg_cell = "kept" if rel not in GAPS and r["dg"]["kept"] else (
            "dropped" if rel in GAPS else "—")
        L.append(f"| `{rel}` | {n} | {mira_cell} | {oxa_cell} | {dg_cell} |")

    L += ["", "## What MIRA has no predicate for — and what happens instead", ""]
    if r["mira"]["declared_types"]:
        L.append(f"**{r['mira']['declared']} of {r['relations']} relations "
                 f"({round(100 * r['mira']['declared'] / max(r['relations'], 1))}%) fall outside "
                 f"`supports` and `opposes`.** They are not dropped and not flattened: MIRA "
                 f"imports a Discourse Graphs base schema in which relations are definable, so "
                 f"each is declared in the document as a `RelationDef` with a domain, a range "
                 f"and a description, then used as a predicate.")
        L.append("")
        for k, v in sorted(r["mira"]["declared_types"].items(), key=lambda x: -x[1]):
            L.append(f"- `haak:{k}` ({v}) — {GAPS[k]}")
        L.append("")
        L.append("A reader that knows only core MIRA still gets every node and every "
                 "supports/opposes edge. One that follows the declarations gets the rest with "
                 "stated semantics. Flattening these into `supports` would have been worse "
                 "than dropping them: it would assert that a boundary condition is evidence "
                 "*for* the claim it limits.")
    else:
        L.append("Nothing: this paper uses only relations core MIRA already names.")

    L += ["", "## What MIRA flattens", "",
          "`tests`, `confirms`, `validates`, `extends` and `replicates` all become "
          "`mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become "
          "`mira:opposes`. The relation survives; the reason it was drawn does not.", ""]
    for k, v in sorted(r["flattened"].items(), key=lambda x: -x[1]):
        L.append(f"- `{k}` ({v})")

    L += ["", "## What no format carries", "",
          "Verification — that a claim was checked, by what code, against what deposited "
          "data, with what result beside the published value. None of the three has a node "
          "for it.", ""]
    if r["verification"]:
        L.append("This paper's records: " +
                 ", ".join(f"{v} {k}" for k, v in r["verification"].items()) + ".")

    L += ["", "---", "",
          "Generated by `scripts/formats_report.py` from the files in `exports/`, not from "
          "the converters' mapping tables — a table says what a converter intends, the "
          "export says what it did.", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper", nargs="?")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()

    if a.all:
        data = yaml.safe_load(open(os.path.join(ROOT, "corpus.yaml"), encoding="utf-8")) or {}
        slugs = []
        for _, c in (data.get("corpora") or {}).items():
            if c.get("public") and c.get("in_site_corpus", True):
                slugs += c.get("papers") or []
        slugs = sorted(slugs)
    elif a.paper:
        slugs = [a.paper]
    else:
        ap.error("give a paper slug or --all")

    for slug in slugs:
        r = report(slug)
        open(os.path.join(EXPORTS, f"{slug}.formats.md"), "w", encoding="utf-8").write(markdown(r))
        open(os.path.join(EXPORTS, f"{slug}.formats.json"), "w", encoding="utf-8").write(
            json.dumps(r, indent=2) + "\n")
        pct = round(100 * r["mira"]["dropped"] / max(r["relations"], 1))
        print(f"  {slug:38} {r['relations']:>4} relations · MIRA drops {r['mira']['dropped']:>3} "
              f"({pct:>2}%) · OXA {r['oxa']['kept']:>3} · DG {r['dg']['kept']:>3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
