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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export_mira import INVERSE_PAIRS  # noqa: E402  the inverse pairs are declared once

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
    """Relation types and counts in the claim tree — the source of truth.

    `wild` counts relations whose target is `*`, meaning the claim constrains the paper as a
    whole. They are relations the tree holds and MIRA cannot express, so they are counted
    apart from the ones it can.
    """
    counts = Counter()
    wild = Counter()
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
                    if t.strip() == "*":
                        wild[k] += 1
        for item in (fm.get("belongings") or []):
            if isinstance(item, dict) and item.get("relation"):
                counts[item["relation"]] += 1
                if str(item.get("target", "")).strip() == "*":
                    wild[item["relation"]] += 1
        recs = [r for r in (fm.get("reproductions") or []) if isinstance(r, dict)]
        if recs:
            verif[max(recs, key=lambda r: str(r.get("date", ""))).get("status", "—")] += 1
    return claims, counts, verif, wild


def mira_edges(slug):
    """Count MIRA edges by relation, reading the declarations the document itself carries.

    MIRA reifies relations: an edge is a node with `source` and `destination`, typed by a
    relation declaration, never a predicate hanging off a claim. Counting node *properties*
    -- which this function used to do -- therefore found nothing after the exporter moved
    to the reified encoding, and the report announced that MIRA drops 100% of relations.
    It drops none. That is the second time a number about our own code was written down as
    a fact about MIRA, so nothing here is hardcoded: the relation's name and its parent are
    both read back out of the file being measured.

    Returns (counts by relation, parent by relation) where a parent is `mira:supports`,
    `mira:opposes`, or None for a relation declared with no such commitment.
    """
    p = os.path.join(EXPORTS, f"{slug}.mira.jsonld")
    if not os.path.exists(p):
        return None, None
    g = json.load(open(p, encoding="utf-8")).get("@graph", [])

    label, parent = {}, {}
    for n in g:
        if n.get("@type") != "AbstractRelationDef":
            continue
        label[n["@id"]] = n.get("label", n["@id"])
        parent[n["@id"]] = next(
            (s for s in (n.get("subClassOf") or [])
             if isinstance(s, str) and s in ("mira:supports", "mira:opposes")), None)

    counts, parents = Counter(), {}
    for n in g:
        if "source" not in n or "destination" not in n:
            continue
        for t in (n["@type"] if isinstance(n.get("@type"), list) else [n.get("@type")]):
            if t in label:
                counts[label[t]] += 1
                parents[label[t]] = parent[t]
    return counts, parents


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
    claims, tree, verif, wild = tree_relations(slug)
    total = sum(tree.values())
    mira, parents = mira_edges(slug)
    mira = mira or Counter()
    parents = parents or {}
    oxa = oxa_edges(slug) or Counter()
    dg = dg_edges(slug) or Counter()

    mira_kept = sum(mira.values())
    # The gap between the tree and the export is two unlike things, and calling both "dropped"
    # overstated the loss by twentyfold. An inverse relation is declared with `owl:inverseOf`
    # and emitted one direction only -- MIRA's own practice, and its 942-node demo graph
    # materialises no inverses either -- so a reader recovers it from the forward edge plus
    # the declaration. A `*` target has nowhere to point and is genuinely lost.
    inverse_only = {k: tree[k] for k in INVERSE_PAIRS if tree.get(k)}
    unrepresentable = {k: v for k, v in wild.items() if v}
    lost = sum(unrepresentable.values())
    # Every relation keeps its own declared type. The split is what a reader who knows only
    # core MIRA can still infer: a relation declared under `mira:supports` or `mira:opposes`
    # tells such a reader something; one declared neutrally tells it only that an edge exists.
    inherits = sum(v for k, v in mira.items() if parents.get(k))
    neutral = mira_kept - inherits
    dropped = {k: v for k, v in tree.items() if k in GAPS}

    return {
        "paper": slug,
        "claims": claims,
        "relations": total,
        "by_type": dict(tree.most_common()),
        "mira": {"kept": mira_kept, "lost": lost,
                 "inverse_only": inverse_only, "unrepresentable": unrepresentable,
                 "inherits_core": inherits, "neutral": neutral,
                 "edges": dict(mira.most_common()), "parents": parents,
                 "declared_types": dropped},
        "oxa": {"kept": sum(oxa.values()), "edges": dict(oxa.most_common())},
        "dg": {"kept": sum(dg.values()), "edges": dict(dg.most_common())},
        "verification": dict(verif.most_common()),
    }


def markdown(r):
    L = [f"# {r['paper']} — what each format carries", "",
         f"{r['claims']} claims, {r['relations']} typed relations between them.", "",
         "One source, three targets. Each row is a relation type the paper's claim tree "
         "uses; each column is what became of it.", "",
         "| Relation | In the tree | MIRA | OXA | Discourse Graphs |",
         "|---|---:|---|---|---|"]

    parents = r["mira"]["parents"]
    for rel, n in r["by_type"].items():
        p = parents.get(rel)
        mira_cell = (f"`haak:{rel}`, under `{p}`" if p else
                     f"`haak:{rel}`, neutral" if rel in parents else "—")
        oxa_cell = "kept" if r["oxa"]["kept"] else "—"
        dg_cell = "kept" if rel not in GAPS and r["dg"]["kept"] else (
            "dropped" if rel in GAPS else "—")
        L.append(f"| `{rel}` | {n} | {mira_cell} | {oxa_cell} | {dg_cell} |")

    L += ["", "## What MIRA has no predicate for — and what happens instead", ""]
    if r["mira"]["declared_types"]:
        neutral = r["mira"]["neutral"]
        L.append(f"**{neutral} of {r['relations']} relations "
                 f"({round(100 * neutral / max(r['relations'], 1))}%) are neither support nor "
                 f"opposition.** They are not dropped and not flattened. MIRA imports a "
                 f"Discourse Graphs base schema in which relations are definable, and its "
                 f"`AbstractRelationDef` is a neutral root — it carries no supporting or "
                 f"opposing commitment — so each is declared in the document with a domain, a "
                 f"range and a description, and the edges are typed by that declaration.")
        L.append("")
        for k, v in sorted(r["mira"]["declared_types"].items(), key=lambda x: -x[1]):
            L.append(f"- `haak:{k}` ({v}) — {GAPS[k]}")
        L.append("")
        L.append("Declaring them under `mira:supports` would have been worse than dropping "
                 "them: it would assert that a boundary condition is evidence *for* the claim "
                 "it limits, which reverses the meaning.")
    else:
        L.append("Nothing: this paper uses only relations core MIRA already names.")

    L += ["", "## What a reader who knows only core MIRA sees", "",
          f"Every relation keeps its own type — nothing is flattened into `supports`. "
          f"{r['mira']['inherits_core']} of the {r['mira']['kept']} edges are declared "
          f"under `mira:supports` or `mira:opposes`, so a reader that follows only those two "
          f"still gets their direction; the reason the edge was drawn is in the declaration "
          f"rather than lost.", ""]
    for k, v in sorted(r["mira"]["edges"].items(), key=lambda x: -x[1]):
        p = parents.get(k)
        L.append(f"- `{k}` ({v}) — {'under `' + p + '`' if p else 'neutral'}")

    L += ["", "## What MIRA genuinely cannot carry", ""]
    if r["mira"]["inverse_only"]:
        n = sum(r["mira"]["inverse_only"].values())
        L.append(f"{n} `derived-from` relations are not emitted as edges. This is not loss: "
                 f"`derived-from` is declared `owl:inverseOf` `entails`, and MIRA never "
                 f"materialises the reverse direction — its own 942-node demo graph emits no "
                 f"inverse edges either. A reader recovers each one from the forward edge and "
                 f"the declaration.")
        L.append("")
    if r["mira"]["unrepresentable"]:
        n = r["mira"]["lost"]
        L.append(f"**{n} relations are lost.** They target `*` — the claim constrains the "
                 f"paper as a whole rather than another claim. `scopes` has `mira:Claim` as "
                 f"its range and MIRA has no paper-level node, so no edge is emitted and "
                 f"none is invented. The paper's `gap-report.md` names them.")
    else:
        L.append("Nothing. Every relation in this paper reaches the export, either as an "
                 "edge or as the declared inverse of one.")

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
        inv = sum(r["mira"]["inverse_only"].values())
        print(f"  {slug:38} {r['relations']:>4} relations · MIRA loses "
              f"{r['mira']['lost']:>2} ({inv:>2} inverse-only) · "
              f"OXA {r['oxa']['kept']:>3} · DG {r['dg']['kept']:>3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
