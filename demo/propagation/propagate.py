#!/usr/bin/env python3
"""
propagate.py — Change propagation through a claim dependency graph.

Usage:
    python propagate.py --paper <paper-slug> --claim <claim-id> --output text|html|json
"""

import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path

# Repo root relative to this script
REPO_ROOT = Path(__file__).resolve().parents[2]
CLAIMS_DIR = REPO_ROOT / "claims"


def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from a markdown file. Minimal parser — no external deps."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm = text[4:end]
    result = {}
    # Slug, uuid, claim, claim-type, epistemic
    for key in ("uuid", "slug", "doi", "claim-type", "epistemic"):
        m = re.search(rf"^{key}:\s*(.+)$", fm, re.MULTILINE)
        if m:
            result[key] = m.group(1).strip().strip("\"'")
    # Multi-line claim (block scalar >)
    m = re.search(r"^claim:\s*>\s*\n((?:  .+\n?)+)", fm, re.MULTILINE)
    if m:
        result["claim"] = re.sub(r"\s+", " ", m.group(1)).strip()
    else:
        m = re.search(r"^claim:\s*(.+)$", fm, re.MULTILINE)
        if m:
            result["claim"] = m.group(1).strip().strip("\"'")

    # Belongings — parse relation/target pairs
    belongings = []
    in_belongings = False
    rel = None
    for line in fm.splitlines():
        if line.strip() == "belongings:":
            in_belongings = True
            continue
        if in_belongings:
            if line and not line.startswith(" ") and not line.startswith("-"):
                in_belongings = False
                continue
            rm = re.match(r"\s+-?\s*relation:\s*(\w+)", line)
            if rm:
                rel = rm.group(1)
            tm = re.match(r"\s+target:\s*(\S+)", line)
            if tm and rel:
                belongings.append({"relation": rel, "target": tm.group(1)})
                rel = None
    result["belongings"] = belongings

    # Panel from first assertion
    m = re.search(r"^\s+panel:\s*(.+)$", fm, re.MULTILINE)
    if m:
        result["panel"] = m.group(1).strip()

    return result


def load_paper_claims(paper_slug: str) -> dict[str, dict]:
    """Load all claim files for a paper. Returns {slug: metadata}."""
    paper_dir = CLAIMS_DIR / paper_slug
    if not paper_dir.exists():
        available = [d.name for d in CLAIMS_DIR.iterdir() if d.is_dir()]
        print(f"Error: paper '{paper_slug}' not found.\nAvailable: {', '.join(sorted(available))}", file=sys.stderr)
        sys.exit(1)

    claims = {}
    for path in paper_dir.glob("*.md"):
        if path.name == "index.md":
            continue
        text = path.read_text()
        meta = parse_frontmatter(text)
        if not meta.get("slug"):
            meta["slug"] = path.stem
        slug = meta["slug"]
        meta["_file"] = path.name
        claims[slug] = meta

    return claims


def build_forward_dag(claims: dict[str, dict]) -> dict[str, set[str]]:
    """
    Build forward dependency graph: for each claim, which claims depend on it.
    A claim B that has `requires A` or `extends A` means A → B in the forward graph
    (if A changes, B is affected). `supports` is directional the other way: A supports B
    means A provides evidence for B — if A is undermined, B loses support.
    We propagate through ALL relation types except `contradicts`.
    """
    forward: dict[str, set[str]] = {slug: set() for slug in claims}
    for slug, meta in claims.items():
        for b in meta.get("belongings", []):
            rel = b.get("relation", "")
            target = b.get("target", "")
            if rel in ("requires", "extends") and target in claims:
                # slug requires/extends target → target's change affects slug
                forward[target].add(slug)
            elif rel == "supports" and target in claims:
                # slug supports target → slug's change affects target (loses a support)
                forward[slug].add(target)
    return forward


def bfs_propagation(changed_slug: str, forward: dict[str, set[str]]) -> tuple[set[str], set[str]]:
    """
    BFS from changed_slug through forward DAG.
    Returns (direct_affected, transitive_affected) — mutually exclusive sets.
    """
    if changed_slug not in forward:
        return set(), set()

    direct = forward[changed_slug].copy()
    visited = {changed_slug} | direct
    queue = deque(direct)
    transitive = set()

    while queue:
        node = queue.popleft()
        for neighbor in forward[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                transitive.add(neighbor)
                queue.append(neighbor)

    return direct, transitive


def classify_claim(meta: dict) -> str:
    """Return a short label for claim role."""
    ctype = meta.get("claim-type", "empirical")
    slug = meta.get("slug", "")
    # Detect conclusion-like claims
    if ctype == "interpretive" or "correspondence" in slug or "pv-" in slug:
        return "interpretive"
    if ctype == "assessment":
        return "assessment"
    return ctype


def run(paper_slug: str, changed_slug: str, output_format: str):
    claims = load_paper_claims(paper_slug)

    if changed_slug not in claims:
        available = sorted(claims.keys())
        print(f"Error: claim '{changed_slug}' not found.\nAvailable claims:\n  " + "\n  ".join(available), file=sys.stderr)
        sys.exit(1)

    forward = build_forward_dag(claims)
    direct, transitive = bfs_propagation(changed_slug, forward)

    total = len(claims)
    affected = direct | transitive
    unaffected = set(claims.keys()) - {changed_slug} - affected

    # Check if synthesis/interpretive/conclusion claims are in blast radius
    high_level_affected = [
        slug for slug in affected
        if claims[slug].get("claim-type") in ("interpretive", "synthesis")
        or "correspondence" in slug
    ]

    result = {
        "paper": paper_slug,
        "changed_claim": changed_slug,
        "changed_proposition": claims[changed_slug].get("claim", ""),
        "changed_type": claims[changed_slug].get("claim-type", ""),
        "total_claims": total,
        "blast_radius": len(affected),
        "blast_fraction": f"{len(affected)}/{total}",
        "directly_affected": sorted(direct),
        "transitively_affected": sorted(transitive),
        "unaffected": sorted(unaffected),
        "high_level_in_blast": high_level_affected,
    }

    if output_format == "json":
        print(json.dumps(result, indent=2))
        return

    if output_format == "html":
        print_html(result, claims, forward)
        return

    # Default: text
    print_text(result, claims)


def print_text(result: dict, claims: dict):
    w = 72
    print("=" * w)
    print(f"  CHANGE PROPAGATION ANALYSIS")
    print(f"  Paper: {result['paper']}")
    print("=" * w)
    print(f"\nChanged claim:  {result['changed_claim']}")
    print(f"Type:           {result['changed_type']}")
    prop = result['changed_proposition']
    if len(prop) > 200:
        prop = prop[:197] + "..."
    print(f"Proposition:    {prop}")

    print(f"\n{'─' * w}")
    print(f"  BLAST RADIUS: {result['blast_radius']} of {result['total_claims']} claims affected")
    print(f"{'─' * w}")

    if result["directly_affected"]:
        print(f"\nDIRECTLY AFFECTED ({len(result['directly_affected'])}):")
        for slug in result["directly_affected"]:
            meta = claims[slug]
            ctype = meta.get("claim-type", "?")
            ep = meta.get("epistemic", "?")
            print(f"  [{ctype:12s}] [{ep:8s}] {slug}")

    if result["transitively_affected"]:
        print(f"\nTRANSITIVELY AFFECTED ({len(result['transitively_affected'])}):")
        for slug in result["transitively_affected"]:
            meta = claims[slug]
            ctype = meta.get("claim-type", "?")
            ep = meta.get("epistemic", "?")
            print(f"  [{ctype:12s}] [{ep:8s}] {slug}")

    if result["high_level_in_blast"]:
        print(f"\n⚑  HIGH-LEVEL CLAIMS IN BLAST RADIUS:")
        for slug in result["high_level_in_blast"]:
            meta = claims[slug]
            prop = meta.get("claim", "")[:120]
            print(f"  {slug}")
            print(f"    \"{prop}...\"")
    else:
        print(f"\n  No interpretive/synthesis claims in blast radius.")

    print(f"\n{'─' * w}")
    print(f"  Unaffected: {len(result['unaffected'])} claims")
    print(f"{'─' * w}\n")


def print_html(result: dict, claims: dict, forward: dict):
    """Minimal inline HTML for email/paste use — not the main demo.html."""
    lines = ["<html><body style='font-family:monospace'>"]
    lines.append(f"<h2>Change propagation: {result['changed_claim']}</h2>")
    lines.append(f"<p>Paper: {result['paper']}<br>")
    lines.append(f"Blast radius: <strong>{result['blast_radius']} / {result['total_claims']}</strong> claims affected</p>")
    if result["directly_affected"]:
        lines.append("<h3>Directly affected</h3><ul>")
        for s in result["directly_affected"]:
            lines.append(f"<li>{s}</li>")
        lines.append("</ul>")
    if result["transitively_affected"]:
        lines.append("<h3>Transitively affected</h3><ul>")
        for s in result["transitively_affected"]:
            lines.append(f"<li>{s}</li>")
        lines.append("</ul>")
    lines.append("</body></html>")
    print("\n".join(lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Propagate a claim change through the dependency graph.")
    parser.add_argument("--paper", required=True, help="Paper slug (directory name under claims/)")
    parser.add_argument("--claim", required=True, help="Changed claim slug")
    parser.add_argument("--output", choices=["text", "html", "json"], default="text")
    args = parser.parse_args()
    run(args.paper, args.claim, args.output)
