"""Convert the authoring form (claims/<doc>/*.md) to the v0 interchange form.

    python3 schema/to_claim_set.py                      # validate every paper, report
    python3 schema/to_claim_set.py --out exports/v0     # write <doc>.claims.json
    python3 schema/to_claim_set.py --paper headley-2026-inhibitory-rhythms

Normalisation happens here, not in the claim files: `claim-type`/`role`/`epistemic` are three
fields encoding two axes, and the declared vocabularies in vocabulary.py do not match what the
corpus holds (docs/design/2026-09-13-the-split.md § 3.2). The exporter resolves them into
`type`, `function` and `confidence` so the authoring form can migrate on its own schedule.
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "claim-set-v0.schema.json"

# The relation names a claim file may carry as a top-level key. Taken from
# scripts/relations.py EDGE_KEYS, which is normative: when the vocabulary changes there — as it
# did when #125's ruling split `dissociates-with` into a neutral contrast and `in-tension-with` —
# this list and the schema's enum follow it rather than drifting from it.
PREDICATES = tuple(sorted(['confirms', 'contradicts', 'derived-from', 'dissociates-with', 'enables-method', 'entails', 'extends', 'in-tension-with', 'interprets', 'opposes', 'part-of', 'predicts', 'qualifies', 'refutes', 'replicates', 'requires', 'rules-out', 'scopes', 'supports', 'tests', 'validates']))
RELATION_ALIAS: dict[str, str] = {}
TYPE_ALIAS = {"methodological": ("assessment", "methodological"), "scope": ("scope", None)}
ROLE_FUNCTION = {"control": "control", "literature-context": "literature-context",
                 "methodological": "methodological"}
STRENGTH = {"strong", "moderate", "tentative", "weak"}
REPRO_STATUS = {"verified", "partial", "mismatch", "blocked", "unattempted", "unverified"}
DISCREPANCY_KIND = {"methodological-gap", "numeric", "direction", "data-mismatch", "unexplained"}


def frontmatter(path: Path) -> dict | None:
    """Parse YAML frontmatter, repairing write.py's zero-indent `belongings:\\n[]`."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    raw = re.sub(r"^\[\]$", "  []", text.split("---", 2)[1], flags=re.M)
    try:
        return yaml.safe_load(raw) or {}
    except yaml.YAMLError as e:
        print(f"  ! unparseable frontmatter: {path.relative_to(ROOT)}: {e.args[0]}", file=sys.stderr)
        return None


def one_line(v) -> str:
    return " ".join(str(v).split())


def claim_of(d: dict) -> dict:
    slug = d["slug"]
    ctype, function = TYPE_ALIAS.get(d.get("claim-type"), (d.get("claim-type"), None))
    function = function or ROLE_FUNCTION.get(d.get("role"))
    if slug.startswith("alt-"):
        function = "alternative"

    c = {"id": slug, "uuid": str(d["uuid"]), "text": one_line(d["claim"]), "type": ctype}
    if function:
        c["function"] = function
    if d.get("epistemic") in STRENGTH:
        c["confidence"] = d["epistemic"]
    if d.get("displayClaim"):
        c["plain"] = one_line(d["displayClaim"])
    if d.get("shortClaim"):
        c["short"] = str(d["shortClaim"])[:90]
    if d.get("concepts"):
        c["concepts"] = [str(x) for x in d["concepts"]]
    if d.get("addresses"):
        a = d["addresses"]
        c["addresses"] = [a] if isinstance(a, str) else list(a)
    return c


def assertions_of(d: dict, doc: str) -> list[dict]:
    out = []
    for a in d.get("assertions") or []:
        if not isinstance(a, dict):
            continue
        e = {"document": a.get("paper-slug", doc), "stance": a.get("stance") or "asserts"}
        if a.get("doi"):
            e["doi"] = a["doi"]
        locator = {k: str(a[k]) for k in ("panel", "figureUri") if a.get(k)}
        if locator:
            e["locator"] = locator
        grounds = {}
        for src, dst in (("method", "method"), ("analysis", "analysis"),
                         ("dataset", "dataset"), ("dataset-doi", "datasetDoi")):
            if a.get(src):
                grounds[dst] = str(a[src])
        if not str(grounds.get("dataset", "")).startswith("http"):
            grounds.pop("dataset", None)
        if grounds:
            e["grounds"] = grounds
        if a.get("confidence") in STRENGTH:
            e["confidence"] = a["confidence"]
        out.append(e)
    return out or [{"document": doc, "stance": "asserts"}]


def reproductions_of(d: dict) -> list[dict]:
    """`discrepancy` is a paper-versus-rerun finding, not a relation: it belongs here."""
    disc = d.get("discrepancy")
    if isinstance(disc, dict) and disc.get("explanation"):
        kind = str(disc.get("type", "unexplained"))
        disc = {"kind": kind if kind in DISCREPANCY_KIND else "unexplained",
                "explanation": one_line(disc["explanation"])}
    else:
        disc = None

    out = []
    for r in d.get("reproductions") or []:
        if not isinstance(r, dict):
            continue
        status = str(r.get("status", "unattempted")).split(":")[0]
        e = {"status": status if status in REPRO_STATUS else "unverified"}
        if r.get("agent"):
            e["by"] = str(r["agent"])
        if r.get("date"):
            e["date"] = str(r["date"])
        if r.get("blocked_by"):
            e["blockedBy"] = str(r["blocked_by"])
        if r.get("script"):
            e["script"] = str(r["script"])
        if r.get("notes"):
            e["note"] = one_line(r["notes"])
        if disc and e["status"] in ("mismatch", "partial"):
            e["discrepancy"] = disc
            disc = None
        out.append(e)
    if disc:
        out.append({"status": "mismatch", "discrepancy": disc})
    return out


def edges_of(d: dict) -> list[dict]:
    """One `edges` array from `belongings` plus the nineteen top-level predicate keys."""
    slug, seen, out = d["slug"], set(), []
    pairs = [(b["relation"], b["target"]) for b in d.get("belongings") or []
             if isinstance(b, dict) and b.get("target")]
    pairs += [(p, t) for p in PREDICATES for t in (d.get(p) or []) if isinstance(t, str)]
    for rel, target in pairs:
        rel = RELATION_ALIAS.get(rel, rel)
        if (rel, target) not in seen:
            seen.add((rel, target))
            out.append({"from": slug, "rel": rel, "to": target})
    return out


def convert(doc: str) -> dict:
    index = frontmatter(ROOT / "claims" / doc / "index.md") or {}
    cs = {"schemaVersion": "0", "document": {"id": doc},
          "provenance": {"generator": "schema/to_claim_set.py", "reviewed": "none"},
          "claims": [], "edges": []}
    for key in ("doi", "title"):
        if index.get(key):
            cs["document"][key] = index[key]
    if index.get("questions"):
        cs["questions"] = [{"id": q["id"], "text": one_line(q["text"])} for q in index["questions"]]

    for path in sorted((ROOT / "claims" / doc).glob("*.md")):
        if path.name == "index.md":
            continue
        d = frontmatter(path)
        if not d:
            continue
        cs["claims"].append({**claim_of(d), "assertions": assertions_of(d, doc),
                             **({"reproductions": r} if (r := reproductions_of(d)) else {})})
        cs["edges"].extend(edges_of(d))
    return cs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--paper", help="one document slug; default every one in claims/")
    ap.add_argument("--out", type=Path, help="directory to write <doc>.claims.json into")
    args = ap.parse_args()

    try:
        import jsonschema
        validator = jsonschema.Draft202012Validator(json.loads(SCHEMA.read_text()))
    except ImportError:
        validator = None
        print("jsonschema not installed — converting without validating", file=sys.stderr)

    docs = [args.paper] if args.paper else sorted(
        Path(p).parent.name for p in glob.glob(str(ROOT / "claims" / "*" / "index.md")))
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)

    failed = 0
    for doc in docs:
        cs = convert(doc)
        ids = {c["id"] for c in cs["claims"]}
        dangling = [e for e in cs["edges"] if e["to"] != "*" and e["to"] not in ids]
        errors = list(validator.iter_errors(cs)) if validator else []
        failed += bool(errors or dangling)
        print(f"{doc:42s} claims={len(cs['claims']):3d} edges={len(cs['edges']):4d} "
              f"errors={len(errors):2d} dangling={len(dangling):2d}")
        for e in errors:
            print(f"     {'/'.join(map(str, e.absolute_path))}: {e.message[:120]}")
        for e in dangling:
            print(f"     dangling: {e['from']} --{e['rel']}--> {e['to']}")
        if args.out:
            (args.out / f"{doc}.claims.json").write_text(json.dumps(cs, indent=2) + "\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
