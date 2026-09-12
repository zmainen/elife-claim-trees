#!/usr/bin/env python3
"""Validate every MIRA export against MIRA's own pinned shapes, and say whose fault each
violation is.

"Validates against MIRA" is not a yes/no answer today, because MIRA's generated shapes
contain a constraint nothing can satisfy. Two of its properties -- `addresses` and
`sourceDocument` -- are rendered by `gen-shacl` with an `sh:in` list of slot *names*
alongside an `sh:class` and `sh:nodeKind sh:BlankNodeOrIRI`. The shape demands an IRI and
then demands that IRI be the string "RelationDef" or "observationBase".

`docs/schema-mapping/mira-sh-in-bug.jsonld` proves it in four nodes of MIRA's own terms.
This script runs that proof first, so the classification below is never taken on trust,
then validates each export and splits the violations two ways:

  upstream  the unsatisfiable sh:in constraint -- ours to report, not to fix
  ours      anything else -- a real failure of this exporter

Exit status is 0 only when every export's `ours` count is zero. The site reads the JSON
rather than quoting a number somebody typed.

Usage:
  python3 scripts/validate_mira.py              # all public exports
  python3 scripts/validate_mira.py <slug>       # one paper
  python3 scripts/validate_mira.py --json       # machine-readable, no table
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORTS = os.path.join(ROOT, "exports")
VENDOR = os.path.join(ROOT, "vendor")
PROOF = os.path.join(ROOT, "docs", "schema-mapping", "mira-sh-in-bug.jsonld")
OUT = os.path.join(ROOT, "site", "src", "data", "mira-validation.json")

PINNED = "483f0b21480c0f4ced9c1519fc0f6df2b8617cfe"

# The upstream bug's signature: an sh:in list whose members are the two slot *names*
# gen-shacl emitted instead of permitted values. Matched on the message rather than the
# property path, and order-independently, because the generator emits the two literals in
# either order depending on set iteration -- both orders occur across the corpus.
UPSTREAM = re.compile(
    r"not in list \[(?=[^]]*Literal\(\"observationBase\"\))"
    r"(?=[^]]*Literal\(\"RelationDef\"\))[^]]*\]")


MIRA_CONTEXT_URL = "https://purl.org/mira-science/mira.jsonld"


def offline(path, tmpdir):
    """The export with its remote @context replaced by the vendored copy.

    vendor/ exists so that validation is reproducible offline and gives the same answer next
    year as today. It holds the shapes, the ontology and the context — and the context was the
    one nobody used. Every export names the context by its canonical URL, correctly, because a
    consumer has to be able to resolve it; but the JSON-LD parser then dereferences that URL
    on every validation, twelve times a run, and purl.org rate-limited a local `make data`
    with a 429 that failed the whole target.

    The published file is not touched. This is a copy, made for the validator, with the one
    string swapped for the object vendor/mira.jsonld already holds. Nothing else about the
    graph changes: the same terms, from the same pinned commit, resolved from disk.
    """
    doc = json.loads(open(path, encoding="utf-8").read())
    vendored = json.loads(open(os.path.join(VENDOR, "mira.jsonld"), encoding="utf-8").read())
    local = vendored["@context"]

    ctx = doc.get("@context")
    if isinstance(ctx, str):
        doc["@context"] = local if ctx == MIRA_CONTEXT_URL else ctx
    elif isinstance(ctx, list):
        doc["@context"] = [local if c == MIRA_CONTEXT_URL else c for c in ctx]

    out = os.path.join(tmpdir, os.path.basename(path))
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh)
    return out


def shacl(path):
    """Returns (conforms, [violation blocks]). Raises if pyshacl cannot run."""
    if not os.path.isdir(VENDOR):
        sys.exit(f"vendor/ missing. Fetch MIRA's shapes at {PINNED} -- see "
                 f"docs/schema-mapping/mira-guide.md")
    with tempfile.TemporaryDirectory() as tmp:
        return _shacl(offline(path, tmp), path)


def _shacl(path, original):
    p = subprocess.run(
        ["pyshacl", "-s", os.path.join(VENDOR, "mira.shacl"), "-sf", "turtle",
         "-e", os.path.join(VENDOR, "mira.ttl"), "-df", "json-ld", path],
        capture_output=True, text=True)
    out = p.stdout + p.stderr
    if "Conforms:" not in out:
        sys.exit(f"pyshacl failed on {os.path.relpath(original, ROOT)}:\n{out.strip()}")
    return "Conforms: True" in out, out.split("Constraint Violation")[1:]


def classify(path):
    conforms, blocks = shacl(path)
    upstream = sum(1 for b in blocks if UPSTREAM.search(b))
    paths = sorted({m for b in blocks for m in re.findall(r"Result Path: (\S+)", b)})
    return {"conforms": conforms, "violations": len(blocks),
            "upstream": upstream, "ours": len(blocks) - upstream, "paths": paths}


def proof():
    """MIRA's shapes reject MIRA's own terms. Checked, not assumed."""
    r = classify(PROOF)
    if r["upstream"] != 2 or r["ours"]:
        sys.exit("The upstream-bug proof no longer behaves as documented "
                 f"({r}). MIRA's shapes may have been fixed -- re-read "
                 "docs/schema-mapping/mira-guide.md before trusting this script.")
    return r


def public_papers():
    import yaml
    data = yaml.safe_load(open(os.path.join(ROOT, "corpus.yaml"), encoding="utf-8")) or {}
    slugs = []
    for _, c in (data.get("corpora") or {}).items():
        if c.get("public"):
            slugs += c.get("papers") or []
    return sorted(set(slugs))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper", nargs="?")
    ap.add_argument("--json", action="store_true", help="emit JSON only")
    a = ap.parse_args()

    p = proof()
    slugs = [a.paper] if a.paper else public_papers()
    papers, missing = {}, []
    for s in slugs:
        f = os.path.join(EXPORTS, f"{s}.mira.jsonld")
        if not os.path.exists(f):
            missing.append(s)
            continue
        papers[s] = classify(f)

    ours = sum(r["ours"] for r in papers.values())
    result = {
        "pinned_schema_commit": PINNED,
        "papers": papers,
        "total_violations": sum(r["violations"] for r in papers.values()),
        "upstream_violations": sum(r["upstream"] for r in papers.values()),
        "our_violations": ours,
        "clean": ours == 0 and not missing,
        "missing_exports": missing,
        "upstream_bug": {
            "properties": ["mira:addresses", "mira:sourceDocument"],
            "proof": os.path.relpath(PROOF, ROOT),
            "proof_violations": p["violations"],
            "summary": "gen-shacl renders subproperty_of as an sh:in list of slot names, "
                       "so both properties demand an IRI that is also one of two strings. "
                       "No document can satisfy them.",
        },
    }

    if not a.paper:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2, sort_keys=True)
            fh.write("\n")

    if a.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"MIRA shapes pinned at {PINNED[:8]}")
        print(f"upstream bug reproduced on {result['upstream_bug']['proof']}: "
              f"{p['violations']} violations on {', '.join(p['paths'])}\n")
        for s, r in papers.items():
            flag = "ok" if not r["ours"] else f"{r['ours']} OURS"
            print(f"  {s:38} {r['violations']:>3} violations · "
                  f"{r['upstream']:>3} upstream · {flag}")
        for s in missing:
            print(f"  {s:38}   no export -- run scripts/export_mira.py")
        print(f"\n{result['total_violations']} violations across {len(papers)} papers; "
              f"{result['upstream_violations']} are MIRA's unsatisfiable sh:in constraint "
              f"and {ours} are ours.")
        if result["clean"]:
            print("Every export is conformant except where MIRA's own shapes reject "
                  "MIRA's own terms.")

    return 0 if result["clean"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
