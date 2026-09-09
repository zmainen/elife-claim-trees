#!/usr/bin/env python3
"""Ingest OXA claim documents into haak.db's claims table.

Usage:
  python3 ingest_oxa_claims.py <oxa-json-file> [--db <haak.db>] [--dry-run]

Reads an OXA Document JSON file containing a ClaimGraph, and inserts
each Claim into the claims table. The full OXA Claim node is stored
in the `data` column as JSON. The `text` column holds the plain claim
text for search. No schema migration needed — uses existing columns.

Idempotent: skips claims whose identifier already exists for the same
entity_id (paper).
"""

import argparse
import json
import sqlite3
import sys
import uuid
from pathlib import Path


DEFAULT_DB = Path.home() / "Projects/haak/infra/var/haak.db"


def extract_claim_text(claim: dict) -> str:
    """Extract plain text from a Claim's inline children."""
    parts = []
    for child in claim.get("children", []):
        if child.get("type") == "Text":
            parts.append(child["value"])
        elif "value" in child:
            parts.append(child["value"])
        elif "children" in child:
            parts.append(extract_claim_text(child))
    return " ".join(parts)


def normalize_claim(text: str) -> str:
    """Produce a normalized form for deduplication."""
    import re
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text[:500]


def ingest_document(doc: dict, conn: sqlite3.Connection, dry_run: bool = False) -> int:
    """Insert claims from an OXA Document into the claims table."""
    paper_doi = doc.get("metadata", {}).get("doi", "")
    paper_title = doc.get("metadata", {}).get("title", "")
    paper_slug = doc.get("metadata", {}).get("slug", "")

    # Build entity_id from DOI or slug
    entity_id = f"paper:{paper_slug}" if paper_slug else f"doi:{paper_doi}"

    # Find the ClaimGraph(s)
    claims_to_insert = []
    for block in doc.get("children", []):
        if block.get("type") == "ClaimGraph":
            for claim in block.get("children", []):
                if claim.get("type") == "Claim":
                    claims_to_insert.append(claim)
        elif block.get("type") == "Claim":
            claims_to_insert.append(block)

    if not claims_to_insert:
        print(f"  No claims found in document", file=sys.stderr)
        return 0

    # Check existing claims for this entity
    existing = set()
    try:
        cursor = conn.execute(
            "SELECT json_extract(data, '$.identifier') FROM claims WHERE entity_id = ?",
            (entity_id,),
        )
        existing = {row[0] for row in cursor if row[0]}
    except sqlite3.OperationalError:
        pass  # json_extract not available or data column absent

    inserted = 0
    for claim in claims_to_insert:
        identifier = claim.get("identifier", "")
        if identifier in existing:
            continue

        text = extract_claim_text(claim)
        normalized = normalize_claim(text)
        role = claim.get("role", "")
        meta = claim.get("metadata", {})
        confidence = meta.get("confidence", "")
        strength = claim.get("epistemicStrength", "")

        # Map role to evidence_type for backward compatibility
        evidence_type_map = {
            "empirical": "experimental",
            "control": "experimental",
            "hypothesis": "theoretical",
            "prediction": "theoretical",
            "interpretation": "theoretical",
            "synthesis": "review-synthesis",
            "methodological": "computational",
            "scope": "theoretical",
            "literature-context": "review-synthesis",
        }
        evidence_type = evidence_type_map.get(role, "")

        # Entities: extract concepts if available
        concepts = meta.get("concepts", [])
        entities_str = ", ".join(concepts) if concepts else ""

        claim_id = meta.get("uuid", str(uuid.uuid4()))

        if dry_run:
            print(f"  [dry-run] {identifier} ({role}): {text[:80]}...")
            inserted += 1
            continue

        conn.execute(
            """INSERT OR IGNORE INTO claims
               (id, entity_id, text, normalized, evidence_type, confidence, entities, data)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                claim_id,
                entity_id,
                text,
                normalized,
                evidence_type,
                confidence or strength,
                entities_str,
                json.dumps(claim, ensure_ascii=False),
            ),
        )
        inserted += 1

    if not dry_run:
        conn.commit()

    return inserted


def main():
    parser = argparse.ArgumentParser(description="Ingest OXA claims into haak.db")
    parser.add_argument("oxa_file", type=Path, help="OXA Document JSON file")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help=f"haak.db path (default: {DEFAULT_DB})")
    parser.add_argument("--dry-run", action="store_true", help="Print without inserting")
    args = parser.parse_args()

    if not args.oxa_file.is_file():
        print(f"error: file not found: {args.oxa_file}", file=sys.stderr)
        return 1

    doc = json.loads(args.oxa_file.read_text())
    if doc.get("type") != "Document":
        print(f"error: not an OXA Document (type={doc.get('type')})", file=sys.stderr)
        return 2

    title = doc.get("metadata", {}).get("title", "(untitled)")
    doi = doc.get("metadata", {}).get("doi", "(no DOI)")
    print(f"Ingesting: {title}")
    print(f"  DOI: {doi}")
    print(f"  DB:  {args.db}")

    conn = sqlite3.connect(str(args.db))
    try:
        n = ingest_document(doc, conn, dry_run=args.dry_run)
        print(f"  Inserted: {n} claim(s)")
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
