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

# The published JSON-LD context. Two wrong values preceded it:
#   /schema/context.jsonld           404s
#   http://purl.org/mira-science/mira#   the ontology NAMESPACE, not a context document —
#                                        a JSON-LD parser fetches it, gets RDF, and dies
# before validating anything. Use the PURL, never the github.io copy, which is served from a
# stale branch and contains `"Study": "mira:Protocol"` — silently retyping every Study.
MIRA_CONTEXT = "https://purl.org/mira-science/mira.jsonld"
DGB = "https://discoursegraphs.com/schema/dg_base#"
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
# Every relation we emit, with the MIRA parent it genuinely descends from.
#
# `parent` is the crux. A relation that really is a kind of support or opposition says so,
# and a MIRA reader that knows only the core vocabulary still understands it. The other six
# are neither: `scopes` states where a claim holds, `requires` a prerequisite, `entails` and
# `derived-from` a deductive step, `interprets` a reading, `enables-method` an affordance.
# Declaring any of them `subClassOf mira:supports` would assert that a boundary condition is
# evidence *for* the claim it limits — a reversal of the meaning, not a compression of it.
# `AbstractRelationDef` is the neutral root and carries no such commitment, so they hang
# there and the document says what they mean instead of pretending they are support.
RELATION_DEFS = {
    "supports":         ("mira:supports", "mira:Claim", "mira:Claim",
                         "The source claim provides support for the destination claim."),
    "tests":            ("mira:supports", "mira:Evidence", "mira:Claim",
                         "The source evidence was gathered to test the destination claim."),
    "validates":        ("mira:supports", "mira:Evidence", "mira:Claim",
                         "The source evidence validates the destination claim."),
    "confirms":         ("mira:supports", "mira:Evidence", "mira:Claim",
                         "The source evidence confirms the destination claim."),
    "extends":          ("mira:supports", "mira:Claim", "mira:Claim",
                         "The source claim extends the destination claim to new conditions."),
    "replicates":       ("mira:supports", "mira:Evidence", "mira:Claim",
                         "The source evidence independently replicates the destination claim."),
    "contradicts":      ("mira:opposes", "mira:Claim", "mira:Claim",
                         "The source claim contradicts the destination claim."),
    "rules-out":        ("mira:opposes", "mira:Evidence", "mira:Claim",
                         "The source evidence eliminates the destination claim as viable."),
    "dissociates-with": ("mira:opposes", "mira:Evidence", "mira:Claim",
                         "The source result separates two things the destination claim joins."),
    # Neither supporting nor opposing — rooted at AbstractRelationDef and nothing else.
    "entails":          (None, "mira:Claim", "mira:Claim",
                         "The source claim logically entails the destination claim: the "
                         "deductive step from a hypothesis to a prediction it commits to."),
    "derived-from":     (None, "mira:Claim", "mira:Claim",
                         "The source claim was derived from the destination claim; the "
                         "inverse of entails."),
    "requires":         (None, "mira:Claim", "mira:Claim",
                         "The source claim depends on the destination holding. If the "
                         "destination fails, the source is undermined."),
    "scopes":           (None, "mira:Claim", "mira:Claim",
                         "The source states a boundary condition governing where the "
                         "destination claim is valid. Neither supports nor opposes."),
    "interprets":       (None, "mira:Claim", "mira:Evidence",
                         "The source claim offers a theoretical reading of the destination "
                         "result."),
    "enables-method":   (None, "mira:Evidence", "mira:Protocol",
                         "The source result makes the destination method possible."),
    "qualifies":        (None, "mira:Claim", "mira:Claim",
                         "The source narrows the destination claim's applicability."),
}

# Declared as an inverse pair rather than as two unrelated relations, and emitted in one
# direction only: MIRA declares inverses on the definition (`owl:inverseOf` in mira.ttl) and
# nothing in its demo graph materialises the reverse edge.
INVERSE_PAIRS = {"derived-from": "entails"}



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

def text_item(content, fmt="text/plain"):
    """A description as MIRA carries it.

    `dct:description` is shaped `sh:class sioc:Item` — a node, not a literal. A plain string
    fails validation, which is how we found this. `sampleData.json` writes the same shape:
    `"description": {"@type": "Item", "format": "text/html", "content": "…"}`.
    """
    return {"@type": "Item", "format": fmt, "content": content}


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
    extra_nodes = []

    node = {
        "@id": node_id(claim),
        "@type": ROLE_TO_TYPE.get(role, "mira:Claim"),
        # `title` and `description` are MIRA's own terms; `schema:name` and
        # `schema:description` were ours and are not in its vocabulary.
        "title": claim["slug"],
        "description": text_item((claim.get("claim") or "").strip()),

    }

    doi = a.get("doi") or claim.get("doi")
    if doi and doi != "~":
        # Only Evidence carries sourceDocument: `mira.yaml` gives Claim the single slot
        # `addresses`, and the shape is closed, so a Claim with a sourceDocument is rejected.
        if node["@type"] == "mira:Evidence":
            node["sourceDocument"] = {"@id": f"https://doi.org/{doi}",
                                      "@type": "SourceDocument"}

    # An Evidence node's observation base is the study that produced it.
    if node["@type"] == "mira:Evidence" and a.get("dataset"):
        # observationBase is "the data on which the observation is based", and its range is
        # `prov:Entity` — the dataset itself, not the study that used it. Pointing it at a
        # Study was our error and failed on class.
        #
        # The Entity node carries an @id and a type and nothing else, deliberately.
        # `prov:Entity` and `prov:Activity` are generated as closed shapes with zero allowed
        # properties, so any node of those types that carries a title, a description or an
        # identifier is rejected — a MIRA bug, reported upstream as demo-MIRA-graph-data#1.
        # An empty node is the only form that validates today, and the dataset URL is
        # already the identifier, so nothing is lost by saying it once.
        ds = str(a["dataset"]).strip()
        if ds.startswith("http"):
            node["observationBase"] = {"@id": ds}
            # `prov:Entity` in full: the context defines the `prov` prefix but no bare
            # `Entity` term, so an unqualified "Entity" resolves nowhere and the class
            # constraint fails without saying why.
            extra_nodes.append({"@id": ds, "@type": "prov:Entity"})

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

    # No relation is emitted as a property of this node. MIRA's node shapes are closed
    # (`mira.shacl`: `mira:Claim a sh:NodeShape ; … sh:closed true`) and `supports`/`opposes`
    # live on an `Argument` mixin that `Claim` and `Evidence` do not mix in, so an inline
    # edge is rejected outright. Relations are reified into their own nodes by `export`.

    # `epistemicStatus` is not a MIRA property — it is not among the 30 the context defines,
    # and we had been emitting `mira:epistemicStatus` as though it were. It cannot go in the
    # strict file either: every node shape is `sh:closed`, so MIRA admits no extension
    # property at all, ours included. It is a real thing the corpus knows and MIRA has no
    # term for, so it lives in the extended file and the gap report names it.
    if not extended:
        return node, dropped, extra_nodes
    node["haakx:epistemicStatus"] = epistemic_status(role, claim.get("epistemic"))

    # ── haak: extension — everything MIRA cannot express ──────────────────
    ext = {"haak:role": role}
    # MIRA has no way to say a paper considered a proposition and rejected it. A rejected
    # alternative emitted as a plain mira:Claim reads as something this paper asserts -- the
    # inversion of its meaning. The strict file still carries the `rules-out` edge, declared
    # under mira:opposes, so a MIRA-only reader gets the direction; it does not get the
    # posture. The gap report says so per paper.
    st = a.get("stance") or "asserts"
    if st != "asserts":
        ext["haak:stance"] = st
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
    return node, dropped, extra_nodes


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
            "description": text_item(text),
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


def _rel_ids(key):
    """Stable ids for a relation's declaration pair and its edges."""
    safe = key.replace("-", "_")
    return f"haak:reldef/{safe}", f"haak:reldef/{safe}/def"


# `domain` and `range` are `sh:class dgb:NodeSchema`, and MIRA's sample satisfies that by
# declaring its own NodeSchema nodes and pointing at those — not at `mira:Claim` directly.
# So the document declares the node types it uses before it declares its relations.
NODE_TYPES = {"mira:Claim": "haak:type/Claim",
              "mira:Evidence": "haak:type/Evidence",
              "mira:Protocol": "haak:type/Protocol"}


def node_type_nodes(author_id, stamp):
    return [{"@id": local, "@type": "NodeSchema", "subClassOf": [mira],
             "label": mira.split(":")[1], "creator": author_id,
             "created": stamp, "modified": stamp}
            for mira, local in NODE_TYPES.items()]


def relation_nodes(used, author_id, stamp):
    """The declaration ladder MIRA uses for relation types.

    Three nodes per relation, following `sampleData.json`: an `AbstractRelationDef` naming
    the relation, a `RelationDef` binding its domain and range, and then one edge node per
    instance. The `owl:Restriction` on `rdf:predicate` is reproduced from the sample for
    fidelity; no shape checks it and no prose explains it, so it is carried rather than
    relied on.
    """
    out = []
    for key in used:
        parent, domain, rng, desc = RELATION_DEFS[key]
        abstract, defn = _rel_ids(key)
        sub = [{"@type": "owl:Restriction", "onProperty": "rdf:predicate",
                "hasValue": abstract}]
        if parent:
            sub.insert(0, parent)
        node = {"@id": abstract, "@type": "AbstractRelationDef", "subClassOf": sub,
                "label": key, "creator": author_id,
                "created": stamp, "modified": stamp}
        # An inverse is a property of the declaration, not of the edges.
        if key in INVERSE_PAIRS and INVERSE_PAIRS[key] in used:
            node["inverseOf"] = _rel_ids(INVERSE_PAIRS[key])[0]
        out.append(node)
        out.append({"@id": defn, "@type": "RelationDef",
                    "domain": NODE_TYPES.get(domain, domain),
                    "range": NODE_TYPES.get(rng, rng),
                    "subClassOf": [abstract, "dgb:RelationInstance"],
                    "label": key, "description": text_item(desc),
                    "creator": author_id, "created": stamp, "modified": stamp})
    return out


def export(paper_slug, extended):
    claims = load_paper(paper_slug)
    by_slug = {c["slug"]: c for c in claims}
    author_id = "haak:agent/elife-claim-trees"
    stamp = f"{date.today().isoformat()}T00:00:00.000Z"

    nodes, all_dropped = [], []
    for c in claims:
        node, dropped, extra = build_node(c, by_slug, extended)
        nodes.append(node)
        nodes.extend(extra)
        for key, target in dropped:
            all_dropped.append((c["slug"], key, target))

    questions, qlinks = synthesize_questions(claims, by_slug, extended)
    for node in nodes:
        for slug, qid in qlinks.items():
            if node.get("title") == slug:
                node["mira:addresses"] = {"@id": qid}
    emitted = [{k: v for k, v in q.items() if k != "_derived"} for q in questions]
    nodes = emitted + nodes

    # ── Reify every relation ────────────────────────────────────────────────
    # One edge node per relation, carrying source and destination. `derived-from` is not
    # emitted at all: it is declared as the inverse of `entails`, and MIRA never
    # materialises the reverse direction.
    #
    # A target that names no claim in this paper is one of two things, and they are not the
    # same. Both used to be dropped without a word, which is how 15 relations went missing
    # from the corpus-wide count without anything saying so.
    #
    #   A prose target is an *eliminated alternative* -- "differential release probability
    #   as the explanation for the DS/VS DA difference". A `rules-out` edge pointing at one
    #   is among the most informative things a paper does, and it has no claim node only
    #   because nobody asserted the thing being excluded. So the node is materialised: it is
    #   a Claim in exactly MIRA's sense, and the extended file flags that the pipeline minted
    #   it from a relation target rather than reading it off a claim file.
    #
    #   A `*` target means the claim scopes the whole paper. There is no paper-level node
    #   for `scopes` to point at -- its range is Claim -- so no edge is invented. It goes to
    #   the gap report by name.
    edges, used, minted, wildcards, n = [], set(), {}, [], 0
    for c in claims:
        for key, target in relations(c):
            if key not in RELATION_DEFS or key in INVERSE_PAIRS:
                continue
            t = by_slug.get(target)
            if t:
                dest, dest_label = node_id(t), t["slug"]
            elif target.strip() == "*":
                wildcards.append((c["slug"], key))
                continue
            else:
                if target not in minted:
                    minted[target] = f"haak:claim/{paper_slug}/alternative/{len(minted) + 1}"
                dest, dest_label = minted[target], target
            used.add(key)
            n += 1
            abstract, _ = _rel_ids(key)
            edges.append({
                "@id": f"haak:edge/{paper_slug}/{n}",
                "@type": [abstract],
                "source": node_id(c),
                "destination": dest,
                "title": f"[[{c['slug']}]] -{key}-> [[{dest_label}]]",
                "creator": author_id, "created": stamp, "modified": stamp,
            })

    for text, mid in minted.items():
        alt = {"@id": mid, "@type": "mira:Claim",
               "title": text, "description": text_item(text)}
        if extended:
            alt["haak:materialisedFrom"] = "relation-target"
            alt["haak:reviewNote"] = (
                "No claim file asserts this. It is an alternative explanation named as the "
                "target of a relation -- usually one the paper rules out -- and is minted as "
                "a Claim so the edge has somewhere to land. Not an authored claim.")
        nodes.append(alt)
    # An inverse is declared whenever its forward relation is used, so the pair is legible
    # even though only one direction is emitted.
    for inv, fwd in INVERSE_PAIRS.items():
        if fwd in used:
            used.add(inv)

    nodes = (node_type_nodes(author_id, stamp)
             + relation_nodes(sorted(used), author_id, stamp) + nodes + edges)
    nodes.insert(0, {"@id": author_id, "@type": "UserAccount",
                     "accountName": "elife-claim-trees pipeline"})

    ctx = {"@context": [MIRA_CONTEXT,
                        {"haak": HAAK, "dgb": DGB,
                         "owl": "http://www.w3.org/2002/07/owl#",
                         "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                         "dct": "http://purl.org/dc/terms/",
                         "prov": "http://www.w3.org/ns/prov#",
                         "onProperty": {"@id": "owl:onProperty", "@type": "@id"},
                         "hasValue": {"@id": "owl:hasValue", "@type": "@id"}}]}
    if extended:
        ctx["@context"].append({"haakx": "https://haak.world/schema/claim-extended#"})

    doc = dict(ctx)
    doc["@graph"] = nodes
    return doc, claims, all_dropped, questions, sorted(minted), wildcards


# ── Reporting ─────────────────────────────────────────────────────────────────

def gap_report(paper_slug, claims, dropped, questions, minted=(), wildcards=()):
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
        L.append(f"- {q['description']['content']}")
    L.append("")
    L.append("Override any of these by adding a `question:` field to the hypothesis's "
             "frontmatter and re-running the export.\n")

    nonassert = [c for c in claims
                 if (first_assertion(c).get("stance") or "asserts") != "asserts"]
    L.append("## Stance: claims this paper does not assert\n")
    if nonassert:
        L.append(f"**{len(nonassert)} of this paper's claims are not asserted by it.** They "
                 f"are alternative explanations it entertains, rejects, or attributes to "
                 f"others. MIRA has no vocabulary for that distinction: it types a node as "
                 f"`Claim` and says nothing about who stands behind it.\n")
        L.append("The strict export still carries the `rules-out` edge that eliminated each "
                 "one, declared under `mira:opposes`, so a MIRA-only reader can see the "
                 "direction of the argument. What that reader cannot see is that the paper "
                 "**denies** these propositions — so it will over-read them as assertions. "
                 "The stance travels in the extended file as `haak:stance`.\n")
        for c in nonassert:
            st = first_assertion(c).get("stance")
            L.append(f"- `{c['slug']}` — {st}")
        L.append("")
    else:
        L.append("Every claim in this paper is asserted by it.\n")

    L.append("## Alternatives materialised as claims\n")
    if minted:
        L.append(f"**{len(minted)} relation targets name something no claim file asserts.** "
                 f"They are alternative explanations the paper argues against, so the target "
                 f"exists only as the thing being excluded. Each is minted as a "
                 f"`mira:Claim` so the edge has a destination, and flagged "
                 f"`haak:materialisedFrom: relation-target` in the extended file. **None of "
                 f"these is an authored claim.**\n")
        for t in minted:
            L.append(f"- {t}")
        L.append("")
    else:
        L.append("None: every relation in this paper points at a claim the tree asserts.\n")

    L.append("## Paper-level scopes with no MIRA target\n")
    if wildcards:
        L.append(f"**{len(wildcards)} `scopes` relations target `*`** — the claim constrains "
                 f"the paper as a whole rather than another claim. `mira:scopes` has "
                 f"`mira:Claim` as its range and MIRA has no paper-level node to point at, "
                 f"so no edge is emitted and no target is invented. The constraint is real "
                 f"and is not in the strict export.\n")
        for slug, key in wildcards:
            L.append(f"- `{slug}` — {key} the whole paper")
        L.append("")
    else:
        L.append("None.\n")
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
            strict, claims, dropped, questions, minted, wildcards = export(
                slug, extended=False)
            ext, *_ = export(slug, extended=True)
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
            f.write(gap_report(slug, claims, dropped, questions, minted, wildcards))

        total = sum(1 for c in claims for _ in relations(c))
        extra = ""
        if minted:
            extra += f", {len(minted)} alternatives materialised"
        if wildcards:
            extra += f", {len(wildcards)} paper-level scopes unrepresentable"
        print(f"  {slug}: {len(claims)} claims, {len(strict['@graph'])} nodes, "
              f"{len(dropped)}/{total} relations declared as RelationDefs{extra}")

    print(f"\nWritten to {out_dir}/")


if __name__ == "__main__":
    main()
