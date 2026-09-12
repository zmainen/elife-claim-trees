#!/usr/bin/env python3
"""The printable review document, regenerated from the current tree.

A whole claim tree is adjudicated two ways, and they must show the same state: in the site's
Reader, claim by claim in the margin of the paper; and on paper, this markdown document a reader
marks up away from a screen. This regenerates the second from the claim files, in the shape of
the hand-written `runs/gadeke-2026-guilt-insula/claim-tree.v2.review.md`, and adds a column
showing any verdict already recorded in the verdict file — so a reading begun in one surface is
visible in the other.

    python3 scripts/review_document.py gadeke-2026-guilt-insula            # to stdout
    python3 scripts/review_document.py gadeke-2026-guilt-insula --write    # to runs/<paper>/...

Nothing is written without `--write`; printing keeps the committed document a reference the
generator mirrors rather than one it silently rewrites.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "extract"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline  # noqa: E402
from elife_extract import verdicts as vd  # noqa: E402

# The order the review document walks the tree — by the work each claim does in the argument,
# with a paper's rejected alternatives (hypotheses that argue against) before its own. Within a
# group, alphabetical by slug. This reproduces the numbering of the v2 document.
ROLE_ORDER = ["hypothesis", "prediction", "empirical", "control", "methodological",
              "scope", "synthesis", "interpretation", "literature-context"]

# Relations read off a claim, in a stable order; `part-of` shows too, since a part names its
# whole here even though it is a claim verdict, not an edge, when scored.
REL_KEYS = ["entails", "derived-from", "tests", "confirms", "validates", "supports", "requires",
            "predicts", "interprets", "rules-out", "refutes", "contradicts", "opposes",
            "dissociates-with", "enables-method", "scopes", "extends", "replicates",
            "qualifies", "part-of"]


def _relations(fm: dict) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()

    def add(rel, tgt):
        if isinstance(tgt, str) and (rel, tgt) not in seen:
            seen.add((rel, tgt))
            out.append((rel, tgt))

    for rel in REL_KEYS:
        for tgt in (fm.get(rel) or []):
            add(rel, tgt)
    for item in (fm.get("belongings") or []):
        if isinstance(item, dict):
            add(item.get("relation"), item.get("target"))
    return out


def _body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip("\n")
    return ""


def _verdict_cell(rec: dict | None) -> str:
    """The verdict standing on a claim, for the summary table."""
    if not rec:
        return "—"
    v = rec.get("verdict", "")
    if v in ("merge-into", "part-of") and rec.get("target"):
        v = f"{v} `{rec['target']}`"
    considered = "" if rec.get("considered") else " *(default)*"
    return f"{v}{considered}"


def build(paper: str, v: int, cdir: Path) -> str:
    claims = []
    for p in sorted(cdir.glob("*.md")):
        if p.name == "index.md":
            continue
        fm = vd.read_frontmatter(p)
        if not fm:
            continue
        assertions = fm.get("assertions") or []
        a0 = assertions[0] if assertions and isinstance(assertions[0], dict) else {}
        claims.append({
            "slug": fm.get("slug") or p.stem,
            "role": fm.get("role") or "",
            "type": fm.get("claim-type") or "",
            "panel": a0.get("panel") or "—",
            "epistemic": fm.get("epistemic") or "",
            "stance": a0.get("stance") or "asserts",
            "method": a0.get("method"),
            "claim": " ".join(str(fm.get("claim", "")).split()),
            "relations": _relations(fm),
            "body": _body(p),
        })

    def key(c):
        try:
            ri = ROLE_ORDER.index(c["role"])
        except ValueError:
            ri = len(ROLE_ORDER)
        return (ri, 0 if c["stance"] == "rejects" else 1, c["slug"])

    claims.sort(key=key)

    # Any verdicts recorded so far, so the two surfaces show the same state.
    res = vd.resolve(vd.load(vd.verdicts_path(ROOT, paper, v)))

    lines: list[str] = []
    lines.append(f"# {paper} — claim-tree v{v} for adjudication")
    lines.append("")
    lines.append(f"This is the document a person reads to approve **claim-tree v{v}** of "
                 f"`{paper}` — and, having read it, records that approval with:")
    lines.append("")
    lines.append(f"    python3 scripts/verdicts.py approve {paper} --by \"<name>\"")
    lines.append("")
    lines.append(f"{len(claims)} claims in `claims/{paper}/`. For each: is the claim true to the "
                 f"paper, is the role right, is the panel right, and is each relation right in type "
                 f"and direction? Mark each line ✓ / ✗ / ? and note why; the vocabulary is "
                 f"`extract/prompts/contract/vocabulary.md`. The **Verdict** column shows what has "
                 f"already been recorded in `{vd.verdicts_path(ROOT, paper, v).relative_to(ROOT)}`.")
    lines.append("")
    lines.append("| # | Slug | Role | Type | Panel | Stance | Verdict |")
    lines.append("|--:|:--|:--|:--|:--|:--|:--|")
    for i, c in enumerate(claims, 1):
        lines.append(f"| {i} | `{c['slug']}` | {c['role']} | {c['type']} | {c['panel']} | "
                     f"{c['stance']} | {_verdict_cell(res.claims.get(c['slug']))} |")
    lines.append("")

    for i, c in enumerate(claims, 1):
        lines.append(f"## {i}. `{c['slug']}`")
        lines.append("")
        lines.append(f"**{c['role']}** · type `{c['type']}` · panel `{c['panel']}` · "
                     f"epistemic `{c['epistemic']}` · stance `{c['stance']}`")
        lines.append("")
        lines.append(f"> {c['claim']}")
        lines.append("")
        if c["relations"]:
            rels = "; ".join(f"`{rel}` → `{tgt}`" for rel, tgt in c["relations"])
            lines.append(f"Relations: {rels}")
        else:
            lines.append("Relations: none")
        lines.append("")
        if c["method"]:
            lines.append(f"Method: {c['method']}  ")
            lines.append("")
        vrec = res.claims.get(c["slug"])
        if vrec and vrec.get("considered"):
            note = f" — {vrec['why']}" if vrec.get("why") else ""
            lines.append(f"Recorded verdict: **{_verdict_cell(vrec)}**{note} "
                         f"(by {vrec.get('by', '?')})")
            lines.append("")
        if c["body"]:
            lines.append(c["body"])
            lines.append("")
        lines.append("- [ ] claim ✓/✗/?  ")
        lines.append("- [ ] role ✓/✗/?  ")
        lines.append("- [ ] panel ✓/✗/?  ")
        lines.append("- [ ] relations ✓/✗/?  ")
        lines.append("- notes: ")
        lines.append("")

    return "\n".join(lines).rstrip("\n") + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper")
    ap.add_argument("--v", type=int, help="which version (default: the one on the ledger)")
    ap.add_argument("--write", action="store_true",
                    help="write to runs/<paper>/claim-tree.v<N>.review.md (default: stdout)")
    args = ap.parse_args()

    run = pipeline._latest(pipeline.read_ledger(args.paper), "claim-tree")
    if not run:
        print(f"error: claim-tree has never run for {args.paper!r}", file=sys.stderr)
        return 2
    v = args.v if args.v is not None else run["v"]
    cdir = (ROOT / "claims" / args.paper) if v == run["v"] else (ROOT / "runs" / args.paper / f"claim-tree.v{v}")
    if not cdir.is_dir():
        print(f"error: no tree at {cdir}", file=sys.stderr)
        return 2

    doc = build(args.paper, v, cdir)
    if args.write:
        out = ROOT / "runs" / args.paper / f"claim-tree.v{v}.review.md"
        out.write_text(doc, encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)} ({doc.count(chr(10))} lines)")
    else:
        sys.stdout.write(doc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
