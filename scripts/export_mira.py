#!/usr/bin/env python3
"""
Export a paper's claim tree to MIRA JSON-LD.

MIRA (Modular Interoperable Research Attribution) is the discourse-graph schema
eLife's article platform ingests. This writes two files:

  <slug>.mira.jsonld           strict MIRA core — safe to hand to any MIRA reader
  <slug>.mira-extended.jsonld  the same graph plus a `haak:` namespace carrying
                               the structure MIRA has no vocabulary for

and a gap report saying exactly what the strict export dropped and why.

The split matters. MIRA can express roughly half of what a claim tree holds; a
single "converted" file either silently loses the rest or emits something a
strict reader chokes on. Two files keeps both promises.

Usage:
  python scripts/export_mira.py gadeke-2026-guilt-insula
  python scripts/export_mira.py --all
  python scripts/export_mira.py <slug> --out-dir exports
"""

import argparse
import json
import os
import re
import sys
from datetime import date

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required:  pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAIMS_DIR = os.path.join(ROOT, "claims")

# The schema's own id. The context URL previously used here — /schema/context.jsonld —
# returns 404; the published identifier is this PURL.
MIRA_CONTEXT = "http://purl.org/mira-science/mira#"
DGB = "https://mira.science/schema/discoursegraphs_base#"
HAAK = "https://haak.world/schema/claim#"

# ── Declaring the relations MIRA does not ship ───────────────────────────────
# MIRA is not limited to `supports` and `opposes`. It imports a Discourse Graphs base
# schema defining `AbstractRelationDef`, `RelationDef` (carrying `rdfs:domain` and
# `rdfs:range`) and `RelationInstance` — relations are first-class definable things, and
# supports/opposes are simply the two MIRA ships with.
#
# So a relation with no MIRA predicate need not be dropped, and need not be flattened into
# `supports` either. Flattening would be worse than dropping for several of these: mapping
# `scopes` to `supports` would assert that a boundary condition is evidence *for* the claim
# it limits, which is not a compression of the meaning but a reversal of it.
#
# Instead each is declared, once per document, as a RelationDef with a domain, a range and a
# description, and then used as a predicate. A reader that knows only core MIRA still reads
# every node and every supports/opposes edge; a reader that follows the RelationDefs gets
# the rest with stated semantics. Nothing is lost and nothing is misstated.
RELATION_DEFS = {
    "entails":        ("mira:Claim", "mira:Claim",
                       "The subject claim logically entails the object claim — the deductive "
                       "step from a hypothesis to a prediction it commits to."),
    "derived-from":   ("mira:Claim", "mira:Claim",
                       "The subject claim was derived from the object claim; the inverse of "
                       "entails."),
    "requires":       ("mira:Claim", "mira:Claim",
                       "The subject claim depends on the object holding. If the object fails, "
                       "the subject is undermined."),
    "scopes":         ("mira:Claim", "mira:Claim",
                       "The subject states a boundary condition governing where the object "
                       "claim is valid. Not support: a scope constraint narrows a claim."),
    "interprets":     ("mira:Claim", "mira:Evidence",
                       "The subject offers a theoretical reading of the object result."),
    "enables-method": ("mira:Evidence", "mira:Protocol",
                       "The subject result makes the object method possible downstream."),
    "qualifies":      ("mira:Claim", "mira:Claim",
                       "The subject narrows the object claim's applicability."),
}

# ── Mapping tables ────────────────────────────────────────────────────────────
# Every entry here is a decision that a human should be able to disagree with,
# which is why they are data rather than buried in code.

ROLE_TO_TYPE = {
    "hypothesis":         "mira:Claim",
    "prediction":         "mira:Claim",
    "empirical":          "mira:Evidence",
    "control":            "mira:Evidence",
    "interpretation":     "mira:Claim",
    "synthesis":          "mira:Claim",
    "assessment":         "mira:Claim",
    "scope":              "mira:Claim",
    "methodological":     "mira:Protocol",
    "literature-context": "dg:SourceDocument",
}

# MIRA carries the hypothesis/established distinction on EpistemicStatus rather
# than in the node type, so role and epistemic strength both feed this.
def epistemic_status(role, epistemic):
    if role in ("hypothesis", "prediction"):
        return "mira:Hypothesis"
    if epistemic == "weak" or role == "scope":
        return "mira:Assumption"
    if epistemic in ("strong", "moderate"):
        return "mira:Claim"
    return "mira:Claim"

SUPPORTS = {"tests", "confirms", "validates", "supports", "extends", "replicates"}
OPPOSES  = {"contradicts", "opposes", "dissociates-with", "rules-out"}

# Relations with no MIRA predicate at all. These are the export's real cost.
GAPS = {
    "entails":        "hypothesis entails its prediction — the deductive step",
    "derived-from":   "prediction derived from its hypothesis (inverse of entails)",
    "interprets":     "one claim interprets another",
    "enables-method": "a result makes a downstream method possible",
    "scopes":         "a scope constraint governs another claim's validity",
    "requires":       "a claim depends on another holding",
    "qualifies":      "a claim narrows another's applicability",
}

EDGE_KEYS = SUPPORTS | OPPOSES | set(GAPS)


# ── Reading ───────────────────────────────────────────────────────────────────

def load_frontmatter(path):
    """Parse a claim file's YAML frontmatter, tolerating a known formatting quirk."""
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        raise ValueError(f"no YAML frontmatter in {path}")
    body = m.group(1)
    # Several committed files write an empty list on the line *after* its key,
    # at column 0, which strict YAML rejects. Normalise rather than edit the
    # source files — see issue about `belongings:` formatting.
    body = re.sub(r"^([A-Za-z0-9_-]+):\n(\[\]|\{\})\s*$", r"\1: \2", body, flags=re.M)
    return yaml.safe_load(body)


def load_paper(paper_slug):
    d = os.path.join(CLAIMS_DIR, paper_slug)
    if not os.path.isdir(d):
        sys.exit(f"no such paper: {paper_slug}")
    claims = []
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md") or fn == "index.md":
            continue
        fm = load_frontmatter(os.path.join(d, fn))
        if fm and fm.get("slug"):
            claims.append(fm)
    return claims


# ── Conversion ────────────────────────────────────────────────────────────────

def node_id(claim):
    return f"urn:uuid:{claim['uuid']}"


def relations(claim):
    """Yield (relation, target) pairs from BOTH places the corpus stores them.

    Claims carry relations two ways: as top-level list keys (`tests:`, `scopes:`)
    and as `belongings:` entries of the form {relation, target}. Roughly 300
    relations corpus-wide live only in `belongings`, so reading one form and not
    the other silently truncates the graph. See docs/claim-format.md §5, which
    documents the `belongings` form; the top-level form is undocumented practice.
    """
    # sorted(): EDGE_KEYS is a set, and Python randomises string hashing per process, so an
    # unsorted iteration emits relations in a different order on every run — which showed up
    # as the published exports changing bytes without changing content.
    for key in sorted(EDGE_KEYS):
        for target in (claim.get(key) or []):
            if isinstance(target, str):
                yield key, target
    for item in (claim.get("belongings") or []):
        if isinstance(item, dict) and item.get("relation") and item.get("target"):
            yield item["relation"], item["target"]


def first_assertion(claim):
    a = claim.get("assertions") or []
    return a[0] if a else {}


def build_node(claim, by_slug, extended):
    role = claim.get("role") or claim.get("claim-type") or "empirical"
    a = first_assertion(claim)

    node = {
        "@id": node_id(claim),
        "@type": ROLE_TO_TYPE.get(role, "mira:Claim"),
        "schema:name": claim["slug"],
        "schema:description": (claim.get("claim") or "").strip(),
        "mira:epistemicStatus": epistemic_status(role, claim.get("epistemic")),
    }

    doi = a.get("doi") or claim.get("doi")
    if doi and doi != "~":
        node["dg:sourceDocument"] = {"schema:identifier": f"doi:{doi}"}

    # An Evidence node's observation base is the study that produced it.
    if node["@type"] == "mira:Evidence" and a.get("dataset"):
        study = {
            "@type": "mira:Study",
            "schema:identifier": a["dataset"],
        }
        if a.get("method"):
            study["mira:follows"] = {"@type": "mira:Protocol",
                                     "schema:name": a["method"]}
        node["mira:observationBase"] = study

    supports, opposes, dropped = [], [], []
    for key, target in relations(claim):
        t = by_slug.get(target)
        ref = {"@id": node_id(t)} if t else {"schema:name": target}
        if key in SUPPORTS:
            supports.append(ref)
        elif key in OPPOSES:
            opposes.append(ref)
        else:
            dropped.append((key, target))

    if supports:
        node["mira:supports"] = supports if len(supports) > 1 else supports[0]
    if opposes:
        node["mira:opposes"] = opposes if len(opposes) > 1 else opposes[0]

    # The relations core MIRA has no predicate for are emitted under their declared
    # RelationDef rather than discarded. This is what makes the strict file lossless.
    declared = {}
    for key, target in dropped:
        if key not in RELATION_DEFS:
            continue
        t = by_slug.get(target)
        declared.setdefault(f"haak:{key}", []).append(
            {"@id": node_id(t)} if t else {"schema:name": target})
    for k, v in declared.items():
        node[k] = v if len(v) > 1 else v[0]

    if not extended:
        return node, dropped

    # ── haak: extension — everything MIRA cannot express ──────────────────
    ext = {"haak:role": role}
    if claim.get("epistemic"):
        ext["haak:epistemicStrength"] = claim["epistemic"]

    typed = {}
    for key, target in relations(claim):
        t = by_slug.get(target)
        typed.setdefault(key, []).append(
            {"@id": node_id(t)} if t else {"schema:name": target})
    if typed:
        # Sorted, because this file is published as a reproducible artifact: re-running the
        # export must produce the same bytes, not the same content in dict-insertion order.
        ext["haak:relations"] = {k: typed[k] for k in sorted(typed)}

    reps = []
    for r in (claim.get("reproductions") or []):
        rec = {
            "@type": "haak:VerificationRecord",
            "haak:agent": r.get("agent"),
            "schema:date": str(r.get("date")) if r.get("date") else None,
            "haak:status": r.get("status"),
            "haak:executed": r.get("script_execution") == "executed",
        }
        for src, dst in (("script", "haak:script"),
                         ("function", "haak:function"),
                         ("data_source", "haak:dataSource"),
                         ("data_commit", "haak:dataCommit"),
                         ("data_file", "haak:dataFile"),
                         ("paper_value", "haak:publishedValue"),
                         ("reproduced_value", "haak:reproducedValue")):
            if r.get(src):
                rec[dst] = r[src]
        reps.append({k: v for k, v in rec.items() if v is not None})
    if reps:
        ext["haak:verification"] = reps

    if a.get("panel"):
        ext["haak:panel"] = a["panel"]
    if a.get("analysis"):
        ext["haak:analysis"] = a["analysis"]

    node.update(ext)
    return node, dropped


def synthesize_questions(claims, by_slug, extended):
    """MIRA requires each Claim to address a Question. Claim trees have none.

    A question is derived mechanically from each hypothesis so the export is
    schema-valid, and flagged so nobody mistakes it for something the authors
    wrote. Override by adding `question:` to the hypothesis's frontmatter.
    """
    questions, links = [], {}
    for c in claims:
        if (c.get("role") or c.get("claim-type")) != "hypothesis":
            continue
        qid = f"urn:uuid:{c['uuid']}#question"
        text = c.get("question")
        derived = text is None
        if derived:
            first = (c.get("claim") or "").strip().split(". ")[0].rstrip(".")
            text = f"Is it the case that {first[0].lower() + first[1:]}?" if first else None
        if not text:
            continue
        q = {
            "@id": qid,
            "@type": "mira:Question",
            "schema:description": text,
        }
        # Flag the derivation only in the extended file — in the strict file the
        # `haak:` prefix is undeclared, so these keys would be undefined terms.
        # The gap report lists every derived question for review either way.
        if derived and extended:
            q["haak:autoDerived"] = True
            q["haak:reviewNote"] = ("Derived mechanically from the hypothesis text; "
                                    "MIRA requires a Question node and the claim tree "
                                    "has none. Needs human review before publication.")
        q["_derived"] = derived
        questions.append(q)
        links[c["slug"]] = qid
    return questions, links


def export(paper_slug, extended):
    claims = load_paper(paper_slug)
    by_slug = {c["slug"]: c for c in claims}

    nodes, all_dropped = [], []
    for c in claims:
        node, dropped = build_node(c, by_slug, extended)
        nodes.append(node)
        for key, target in dropped:
            all_dropped.append((c["slug"], key, target))

    questions, qlinks = synthesize_questions(claims, by_slug, extended)
    for node in nodes:
        for slug, qid in qlinks.items():
            if node["schema:name"] == slug:
                node["mira:addresses"] = {"@id": qid}
    # `_derived` is bookkeeping for the report, never part of the graph.
    emitted = [{k: v for k, v in q.items() if k != "_derived"} for q in questions]
    nodes = emitted + nodes

    # Declare every relation this document actually uses, so its predicates are defined
    # rather than merely emitted.
    used = sorted({k for _, k, _ in all_dropped})
    defs = [{
        "@id": f"haak:{k}",
        "@type": "dgb:RelationDef",
        "rdfs:domain": RELATION_DEFS[k][0],
        "rdfs:range": RELATION_DEFS[k][1],
        "dct:description": RELATION_DEFS[k][2],
    } for k in used if k in RELATION_DEFS]
    nodes = defs + nodes

    ctx = {"@context": [MIRA_CONTEXT,
                        {"dgb": DGB, "haak": HAAK,
                         "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                         "dct": "http://purl.org/dc/terms/"}]}
    if extended:
        ctx["@context"].append({"haak": "https://haak.world/schema/claim#"})

    doc = dict(ctx)
    doc["@graph"] = nodes
    return doc, claims, all_dropped, questions


# ── Reporting ─────────────────────────────────────────────────────────────────

def gap_report(paper_slug, claims, dropped, questions):
    roles = {}
    for c in claims:
        roles[c.get("role") or c.get("claim-type")] = \
            roles.get(c.get("role") or c.get("claim-type"), 0) + 1

    total_edges = sum(1 for c in claims for _ in relations(c))

    by_type = {}
    for _, key, _ in dropped:
        by_type[key] = by_type.get(key, 0) + 1

    reps = sum(len(c.get("reproductions") or []) for c in claims)
    verified = sum(1 for c in claims if c.get("reproductions"))

    L = []
    L.append(f"# MIRA export — what the strict file cannot carry\n")
    L.append(f"**Paper:** `{paper_slug}` · **Generated:** {date.today().isoformat()}\n")
    L.append(f"{len(claims)} claims, {total_edges} typed relations between them.\n")

    L.append("## Claims by role\n")
    for r, n in sorted(roles.items(), key=lambda x: (-x[1], x[0])):
        L.append(f"- **{r}** — {n}")
    L.append("")

    L.append("## Relations dropped\n")
    if not dropped:
        L.append("None.\n")
    else:
        pct = round(100 * len(dropped) / total_edges) if total_edges else 0
        L.append(f"**{len(dropped)} of {total_edges} relations ({pct}%) have no MIRA "
                 f"predicate and are absent from the strict export.**\n")
        L.append("| Relation | Dropped | What is lost |")
        L.append("|---|---:|---|")
        for k, n in sorted(by_type.items(), key=lambda x: (-x[1], x[0])):
            L.append(f"| `{k}` | {n} | {GAPS.get(k, '')} |")
        L.append("")
        L.append("The `entails` / `derived-from` pair is the most consequential: together "
                 "they are the paper's deductive spine. Without them a reader cannot tell "
                 "which prediction belongs to which hypothesis.\n")

    L.append("## Relations flattened\n")
    L.append("`tests`, `confirms`, `validates`, `extends` and `replicates` all become "
             "`mira:supports`; `contradicts`, `rules-out` and `dissociates-with` all become "
             "`mira:opposes`. Both directions of collapse lose real distinctions — most "
             "sharply, evidence *designed* to test a prediction becomes indistinguishable "
             "from evidence that merely agrees with it after the fact.\n")

    L.append("## Verification records dropped\n")
    L.append(f"**{reps} verification records across {verified} claims are absent from the "
             f"strict export.** MIRA has no node type for the fact that a claim was "
             f"independently checked, by what code, against what data, with what result. "
             f"They are carried in the extended file as `haak:VerificationRecord`.\n")

    L.append("## Questions synthesized\n")
    auto = [q for q in questions if q.get("_derived")]
    L.append(f"MIRA requires every Claim to address a `mira:Question`; a claim tree has no "
             f"such node. **{len(auto)} questions were derived mechanically from hypothesis "
             f"text and need human review.**\n")
    for q in auto:
        L.append(f"- {q['schema:description']}")
    L.append("")
    L.append("Override any of these by adding a `question:` field to the hypothesis's "
             "frontmatter and re-running the export.\n")
    return "\n".join(L)


def public_papers():
    """The papers a public export may include, from `corpus.yaml`.

    `--all` used to mean every directory under `claims/`, which is not the same
    thing. The repository's `.gitignore` keeps private papers' claim trees and
    verification scripts out of git, but `exports/` was never covered — so
    exporting "the whole corpus" wrote MIRA files and gap reports for three lab
    papers, two of them unpublished, into a directory that was then committed.
    The manifest already records which corpora are public; the exporter now asks
    it instead of trusting the filesystem.
    """
    manifest = os.path.join(ROOT, "corpus.yaml")
    if not os.path.exists(manifest):
        return None                      # no manifest: caller decides
    data = yaml.safe_load(open(manifest, encoding="utf-8")) or {}
    out = []
    for name, c in (data.get("corpora") or {}).items():
        if c.get("public"):
            out += list(c.get("papers") or [])
    return sorted(set(out))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("paper", nargs="?", help="paper slug under claims/")
    p.add_argument("--all", action="store_true", help="export every paper")
    p.add_argument("--out-dir", default="exports")
    p.add_argument("--include-private", action="store_true",
                   help="also export papers corpus.yaml marks non-public. Off by default: "
                        "`exports/` is committed, so a private paper exported here becomes "
                        "a public file.")
    args = p.parse_args()

    if args.all:
        on_disk = sorted(d for d in os.listdir(CLAIMS_DIR)
                         if os.path.isdir(os.path.join(CLAIMS_DIR, d)))
        allowed = public_papers()
        if allowed is None or args.include_private:
            papers = on_disk
        else:
            papers = [d for d in on_disk if d in allowed]
            held = [d for d in on_disk if d not in allowed]
            if held:
                print(f"  skipping {len(held)} non-public paper(s): {', '.join(held)}\n"
                      f"  (corpus.yaml marks them private; --include-private overrides)")
    elif args.paper:
        papers = [args.paper]
    else:
        p.error("give a paper slug or --all")

    out_dir = args.out_dir if os.path.isabs(args.out_dir) \
        else os.path.join(ROOT, args.out_dir)
    os.makedirs(out_dir, exist_ok=True)

    for slug in papers:
        try:
            strict, claims, dropped, questions = export(slug, extended=False)
            ext, _, _, _ = export(slug, extended=True)
        except Exception as e:                                   # noqa: BLE001
            print(f"  {slug}: FAILED — {e}", file=sys.stderr)
            continue

        for name, doc in ((f"{slug}.mira.jsonld", strict),
                          (f"{slug}.mira-extended.jsonld", ext)):
            with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
                json.dump(doc, f, indent=2, ensure_ascii=False)
                f.write("\n")

        with open(os.path.join(out_dir, f"{slug}.gap-report.md"), "w",
                  encoding="utf-8") as f:
            f.write(gap_report(slug, claims, dropped, questions))

        total = sum(1 for c in claims for _ in relations(c))
        print(f"  {slug}: {len(claims)} claims, {len(strict['@graph'])} nodes, "
              f"{len(dropped)}/{total} relations declared as RelationDefs")

    print(f"\nWritten to {out_dir}/")


if __name__ == "__main__":
    main()
