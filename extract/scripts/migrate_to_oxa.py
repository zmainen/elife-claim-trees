#!/usr/bin/env python3
"""Migrate YAML-frontmatter claim files to OXA-native JSON.

Usage:
  python3 migrate_to_oxa.py <paper-dir> [--output-dir <dir>]

Reads all .md claim files in <paper-dir>, converts each to an OXA Claim
node, and writes the full paper as a single OXA Article JSON file.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


# Edge type → CiTO/claimrel mapping
EDGE_MAP = {
    # CiTO exact
    "supports": "cito:supports",
    "extends": "cito:extends",
    "qualifies": "cito:qualifies",
    # CiTO close
    "derived-from": "cito:citesAsSourceDocument",
    "enables-method": "cito:usesMethodIn",
    "dissociates-with": "cito:disagreesWith",
    # Extensions
    "requires": "claimrel:requires",
    "tests": "claimrel:tests",
    "entails": "claimrel:entails",
    "interprets": "claimrel:interprets",
    "scopes": "claimrel:scopes",
    "rules-out": "claimrel:rulesOut",
    "replicates": "claimrel:replicates",
    "contradicts": "claimrel:contradicts",
    # Were missing entirely, so every relation of these two types was silently dropped —
    # 19 of Gädeke's 89 alone. `validates` is the corpus's most-used positive relation.
    "validates": "cito:confirms",
    "confirms": "cito:confirms",
}

EDGE_KEYS = set(EDGE_MAP.keys())


def parse_claim_file(path: Path) -> dict | None:
    """Parse a YAML-frontmatter markdown claim file."""
    text = path.read_text()
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        # Several committed files write an empty list on the line *after* its key, at
        # column 0 (`belongings:\n[]`), which strict YAML rejects. Every other loader in
        # this repository normalises it; this one did not, so those files raised, returned
        # None, and were skipped — silently. Five of Gädeke's 27 claims were missing from
        # its OXA export, and they were the five carrying verification records.
        body = re.sub(r"^([A-Za-z0-9_-]+):\n(\[\]|\{\})\s*$", r"\1: \2",
                      parts[1], flags=re.M)
        fm = yaml.safe_load(body)
    except yaml.YAMLError as e:
        # Loud, not silent. A claim that cannot be parsed is a claim missing from the
        # export, and an export quietly short of five claims looks exactly like an export.
        print(f"[warn] {path}: unparseable frontmatter, claim EXCLUDED: {e}",
              file=sys.stderr)
        return None
    if not isinstance(fm, dict) or "claim" not in fm:
        return None
    fm["_body"] = parts[2].strip()
    fm["_path"] = str(path)
    return fm


# The four stances a paper can take toward a proposition (claim-format.md §2).
# Absent means `asserts`.
STANCES = {"asserts", "entertains", "rejects", "attributes"}


def stance_of(fm: dict) -> tuple[str, str | None]:
    """This paper's stance toward this claim, and the source it attributes it to.

    Stance lives on the assertion because a claim is paper-independent: two papers can
    hold opposite postures toward one proposition. OXA has no assertion object, and a
    paper's OXA document describes exactly one paper, so it lands on the claim node here.
    """
    a = (fm.get("assertions") or [{}])[0]
    if not isinstance(a, dict):
        return "asserts", None
    st = a.get("stance") or "asserts"
    return (st if st in STANCES else "asserts"), a.get("source")


def to_oxa_claim(fm: dict) -> dict:
    """Convert parsed frontmatter to an OXA Claim node."""
    claim_text = fm.get("claim", "").strip()
    identifier = fm.get("slug", fm.get("uuid", ""))
    role = fm.get("role", fm.get("claim-type", "empirical"))

    # Panel — normalize to list
    panel = fm.get("panel")
    if isinstance(panel, str):
        panel = [p.strip() for p in panel.split(",")]
    elif panel is None:
        panel = []

    # Epistemic strength — only valid values; role names are not strengths
    _VALID_STRENGTHS = {"strong", "moderate", "suggestive", "speculative"}
    raw_epistemic = fm.get("epistemic", "")
    epistemic = raw_epistemic if raw_epistemic in _VALID_STRENGTHS else None

    # Build relations from BOTH places the corpus stores them. Reading only the top-level
    # keys missed everything under `belongings:` — 14 of Gädeke's 89 relations, and all of
    # its `requires` and `supports`. This is the third exporter to have had this bug; the
    # corpus stores one fact two ways and every reader has to know both.
    relations = []
    pairs = []
    for edge_key in EDGE_MAP:
        targets = fm.get(edge_key, [])
        if isinstance(targets, str):
            targets = [targets]
        for target in (targets or []):
            if target:
                pairs.append((edge_key, target))
    for item in (fm.get("belongings") or []):
        if isinstance(item, dict) and item.get("relation") and item.get("target"):
            pairs.append((item["relation"], item["target"]))

    for edge_key, target in pairs:
        cito_type = EDGE_MAP.get(edge_key)
        if not cito_type:
            continue
        relations.append({"xref": target, "relationType": cito_type})

    # Build the OXA node
    node = {
        "type": "Claim",
        "identifier": identifier,
        "role": role,
        "children": [{"type": "Text", "value": claim_text}],
    }
    if panel:
        node["panel"] = panel
    if epistemic:
        node["epistemicStrength"] = epistemic
    if relations:
        node["relations"] = relations

    # Without this, the six alternatives Gädeke argues *against* exported as ordinary
    # Claim nodes — six propositions the paper denies, read by any consumer as six it
    # makes. The `rules-out` edge pointing at them gives the direction of the argument
    # and not the paper's posture, so the node has to carry it.
    stance, source = stance_of(fm)
    if stance != "asserts":
        node["stance"] = stance
        if source:
            node["stanceSource"] = source

    # Metadata — provenance and auxiliary fields
    meta = {}
    if fm.get("uuid"):
        meta["uuid"] = fm["uuid"]
    if fm.get("doi") and fm["doi"] != "~":
        meta["doi"] = fm["doi"]
    if fm.get("concepts"):
        meta["concepts"] = fm["concepts"]
    if fm.get("displayClaim"):
        meta["displayClaim"] = fm["displayClaim"].strip()
    if fm.get("shortClaim"):
        meta["shortClaim"] = fm["shortClaim"].strip()
    if fm.get("confidence"):
        meta["confidence"] = fm["confidence"]
    if meta:
        node["metadata"] = meta

    return node


def build_article(paper_dir: Path, claims: list[dict]) -> dict:
    """Build an OXA Article containing all claims."""
    index_path = paper_dir / "index.md"
    paper_meta = {}
    if index_path.exists():
        text = index_path.read_text()
        if text.startswith("---"):
            parts = text.split("---", 2)
            try:
                fm = yaml.safe_load(parts[1])
                if isinstance(fm, dict):
                    paper_meta = fm
            except yaml.YAMLError:
                pass

    slug = paper_meta.get("slug", paper_dir.name)

    # Wrap claims in a ClaimGraph
    claim_graph = {
        "type": "ClaimGraph",
        "identifier": f"{slug}-claims",
        "children": claims,
    }

    metadata: dict = {}
    if paper_meta.get("doi"):
        metadata["doi"] = paper_meta["doi"]
    if paper_meta.get("title"):
        metadata["title"] = paper_meta["title"]
    if paper_meta.get("authors"):
        metadata["authors"] = paper_meta["authors"]

    title_nodes = None
    if paper_meta.get("title"):
        title_nodes = [{"type": "Text", "value": paper_meta["title"]}]

    doc = {
        "type": "Document",
        "metadata": metadata,
        "children": [claim_graph],
    }
    if title_nodes:
        doc["title"] = title_nodes

    return doc


def main():
    parser = argparse.ArgumentParser(description="Migrate claim files to OXA JSON")
    parser.add_argument("paper_dir", type=Path, help="Directory with .md claim files")
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    paper_dir = args.paper_dir.resolve()
    out_dir = (args.output_dir or paper_dir).resolve()

    # Parse all claim files (skip index.md)
    claim_files = sorted(paper_dir.glob("*.md"))
    claim_files = [f for f in claim_files if f.name != "index.md"]

    claims = []
    skipped = 0
    for f in claim_files:
        fm = parse_claim_file(f)
        if fm is None:
            skipped += 1
            continue
        claims.append(to_oxa_claim(fm))

    article = build_article(paper_dir, claims)
    doc_slug = article["children"][0]["identifier"].replace("-claims", "")

    out_path = out_dir / f"{doc_slug}.oxa.json"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as fp:
        json.dump(article, fp, indent=2, ensure_ascii=False)

    print(f"Converted {len(claims)} claims ({skipped} skipped)")
    print(f"Output: {out_path}")

    # Summary stats
    roles = {}
    rel_types = {}
    for c in claims:
        r = c.get("role", "?")
        roles[r] = roles.get(r, 0) + 1
        for rel in c.get("relations", []):
            rt = rel["relationType"]
            rel_types[rt] = rel_types.get(rt, 0) + 1
    print(f"\nRoles: {dict(sorted(roles.items()))}")
    print(f"Relations: {dict(sorted(rel_types.items()))}")


if __name__ == "__main__":
    main()
