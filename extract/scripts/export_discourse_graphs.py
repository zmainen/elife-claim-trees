#!/usr/bin/env python3
"""Export OXA claim JSON to Discourse Graphs JSON-LD.

Usage:
  python3 export_discourse_graphs.py <oxa-json> [--output <path>]

Maps OXA Claim nodes to the Discourse Graphs Q/C/E/S ontology:
  - hypothesis, prediction, synthesis, interpretation → dg:Claim
  - empirical, control → dg:Evidence
  - literature-context → dg:Source
  - scope, methodological → dg:Evidence (with qualifier)

Relations map to dg:supports / dg:opposedBy where possible; others
carry the CiTO/claimrel IRI as a typed annotation.
"""

import argparse
import json
import sys
from pathlib import Path

# Discourse Graphs ontology namespace
DG_NS = "https://discoursegraphs.org/ontology#"
CITO_NS = "http://purl.org/spar/cito/"
CLAIMREL_NS = "http://elife-claim-trees.org/relations/"

# Role → DG node type mapping
ROLE_TO_DG_TYPE = {
    "hypothesis": "Claim",
    "prediction": "Claim",
    "synthesis": "Claim",
    "interpretation": "Claim",
    "empirical": "Evidence",
    "control": "Evidence",
    "scope": "Evidence",
    "methodological": "Evidence",
    "literature-context": "Source",
}

# Relation type → DG relation mapping
# DG has only: supports, opposedBy, addresses, interpretedAs
RELATION_TO_DG = {
    "cito:supports": "supports",
    "cito:extends": "supports",
    "cito:disagreesWith": "opposedBy",
    "claimrel:contradicts": "opposedBy",
    "claimrel:rulesOut": "opposedBy",
    "claimrel:interprets": "interpretedAs",
    "claimrel:tests": "supports",  # testing is a form of evidential support
    "claimrel:entails": "supports",
    "cito:citesAsSourceDocument": "supports",
    "cito:usesMethodIn": "supports",
    "claimrel:replicates": "supports",
    # These have no DG equivalent — carried as annotations
    "claimrel:requires": None,
    "claimrel:scopes": None,
    "cito:qualifies": None,
}


def oxa_to_jsonld(oxa_path: Path) -> dict:
    """Convert an OXA Article with Claims to JSON-LD."""
    with open(oxa_path) as f:
        doc = json.load(f)

    paper_id = doc.get("identifier", "unknown")
    paper_meta = doc.get("metadata", {})
    base_uri = f"https://elife-claim-trees.org/papers/{paper_id}/"

    nodes = []
    edges = []

    for claim in doc.get("children", []):
        if claim.get("type") != "Claim":
            continue

        claim_id = claim.get("identifier", "")
        claim_uri = f"{base_uri}{claim_id}"
        role = claim.get("role", "empirical")
        dg_type = ROLE_TO_DG_TYPE.get(role, "Evidence")

        # Proposition text
        text_parts = []
        for child in claim.get("children", []):
            if child.get("type") == "Text":
                text_parts.append(child.get("value", ""))
        text = " ".join(text_parts)

        # Build JSON-LD node
        node = {
            "@id": claim_uri,
            "@type": f"{DG_NS}{dg_type}",
            f"{DG_NS}content": text,
            f"{DG_NS}role": role,
        }
        if claim.get("panel"):
            node[f"{DG_NS}panel"] = claim["panel"]
        if claim.get("epistemicStrength"):
            node[f"{DG_NS}epistemicStrength"] = claim["epistemicStrength"]
        if claim.get("metadata", {}).get("doi"):
            node["http://purl.org/ontology/bibo/doi"] = claim["metadata"]["doi"]

        nodes.append(node)

        # Build edges
        for rel in claim.get("relations", []):
            target_id = rel.get("xref", "")
            if target_id == "*":
                continue  # Skip wildcard scopes
            target_uri = f"{base_uri}{target_id}"
            rel_type = rel.get("relationType", "")
            dg_rel = RELATION_TO_DG.get(rel_type)

            edge = {
                "@type": f"{DG_NS}Relation",
                f"{DG_NS}source": {"@id": claim_uri},
                f"{DG_NS}target": {"@id": target_uri},
            }
            if dg_rel:
                edge[f"{DG_NS}relationType"] = f"{DG_NS}{dg_rel}"
            else:
                # Carry the original CiTO/claimrel type
                edge[f"{DG_NS}relationType"] = rel_type
            edge[f"{DG_NS}originalRelationType"] = rel_type

            edges.append(edge)

    # Source node for the paper itself
    source_node = {
        "@id": base_uri,
        "@type": f"{DG_NS}Source",
        f"{DG_NS}content": paper_meta.get("title", paper_id),
    }
    if paper_meta.get("doi"):
        source_node["http://purl.org/ontology/bibo/doi"] = paper_meta["doi"]
    if paper_meta.get("authors"):
        source_node[f"{DG_NS}authors"] = paper_meta["authors"]

    # Assemble JSON-LD document
    jsonld = {
        "@context": {
            "dg": DG_NS,
            "cito": CITO_NS,
            "claimrel": CLAIMREL_NS,
            "bibo": "http://purl.org/ontology/bibo/",
        },
        "@graph": [source_node] + nodes + edges,
    }
    return jsonld


def main():
    parser = argparse.ArgumentParser(description="Export OXA claims to Discourse Graphs JSON-LD")
    parser.add_argument("oxa_json", type=Path, help="OXA Article JSON file")
    parser.add_argument("--output", type=Path, default=None, help="Output path (default: <input>.dg.jsonld)")
    args = parser.parse_args()

    jsonld = oxa_to_jsonld(args.oxa_json)

    out_path = args.output or args.oxa_json.with_suffix(".dg.jsonld")
    with open(out_path, "w") as f:
        json.dump(jsonld, f, indent=2, ensure_ascii=False)

    nodes = [n for n in jsonld["@graph"] if n["@type"] != f"{DG_NS}Relation"]
    edges = [n for n in jsonld["@graph"] if n["@type"] == f"{DG_NS}Relation"]
    print(f"Exported {len(nodes)} nodes, {len(edges)} relations")
    print(f"Output: {out_path}")

    # Summarize DG type distribution
    type_counts = {}
    for n in nodes:
        t = n["@type"].split("#")[-1]
        type_counts[t] = type_counts.get(t, 0) + 1
    print(f"Node types: {dict(sorted(type_counts.items()))}")

    # Summarize DG relation distribution
    rel_counts = {}
    for e in edges:
        rt = e.get(f"{DG_NS}relationType", "?").split("#")[-1]
        rel_counts[rt] = rel_counts.get(rt, 0) + 1
    print(f"Relation types: {dict(sorted(rel_counts.items()))}")


if __name__ == "__main__":
    main()
