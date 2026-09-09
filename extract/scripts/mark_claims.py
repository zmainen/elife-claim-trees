#!/usr/bin/env python3
"""Mark a paper's Markdown with claim assignments, as tika ⟦^⟧ marks.

The broad pass of coverage-by-marking. Every sentence carrying a reported
statistic is looked up against the claim set; where a claim accounts for it, a
mark is written anchored to the sentence; where none does, the sentence is left
bare and is therefore visible as an orphan.

Mark grammar follows tika SPEC § 3 — the same anchoring the citation and
bibliography kinds use, because a claim assignment is the same shape of thing:
many instances scattered through a text, each pointing at one element.

    ⟦@zach: @{Smith et al. (2014)} smith2014entropy⟧    citation → bib key
    ⟦^zach: @{t(39) = 2.27, p = 0.03} risk-aversion⟧    claim instance → claim

Recall is what matters here, not precision: duplicates and false positives are
resolved in the mapping pass, and a missed span cannot be resolved at all.

NOTE: tika does not yet know the `^` sign. Its parser falls through unknown
signs to a substitution with an empty replacement, which on accept would delete
the marked span. Marked files must not be opened in tika for disposition until
that PR lands. Written to a separate .marked.md for exactly that reason.

Usage:
  python scripts/mark_claims.py <paper.md> <claims-dir> [-o out.md]
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml  # noqa: E402

from elife_extract.segment import STAT_RE, plain, split_sentences  # noqa: E402

AUTHOR = "zach"


def norm(s: str) -> str:
    """Compare statistics ignoring spacing, dash flavour and case."""
    return re.sub(r"\s+", "", s).replace("−", "-").replace("–", "-").lower()


def load_claims(d: Path) -> list[dict]:
    out = []
    for f in sorted(d.glob("*.md")):
        if f.name == "index.md":
            continue
        m = re.match(r"^---\n(.*?)\n---", f.read_text(), re.S)
        if not m:
            continue
        body = re.sub(r"^([A-Za-z0-9_-]+):\n(\[\]|\{\})\s*$", r"\1: \2",
                      m.group(1), flags=re.M)
        try:
            fm = yaml.safe_load(body) or {}
        except yaml.YAMLError:
            continue
        if fm.get("slug"):
            out.append(fm)
    return out


def claim_stat_index(claims: list[dict]) -> dict[str, list[str]]:
    """statistic → slugs of every claim that states it."""
    idx: dict[str, list[str]] = {}
    for c in claims:
        text = c.get("claim") or ""
        for m in STAT_RE.finditer(plain(text)):
            idx.setdefault(norm(m.group(0)), []).append(c["slug"])
    return idx


def mark_document(md: str, claims: list[dict]) -> tuple[str, dict]:
    idx = claim_stat_index(claims)
    lines_out, n_marked, n_orphan, orphans = [], 0, 0, []

    for line in md.split("\n"):
        # Leave structure, code and reference lists alone.
        if not line.strip() or line.lstrip().startswith(("#", "|", ">", "    ", ":::")):
            lines_out.append(line)
            continue

        pieces = []
        for sent in split_sentences(line):
            stats = [m.group(0) for m in STAT_RE.finditer(plain(sent))]
            if not stats:
                pieces.append(sent)
                continue
            hits: list[str] = []
            for s in stats:
                for slug in idx.get(norm(s), []):
                    if slug not in hits:
                        hits.append(slug)
            if hits:
                quote = sent if len(sent) <= 120 else sent[:117] + "…"
                quote = quote.replace("}", ")")  # keep the @{...} delimiter safe
                pieces.append(
                    sent + "".join(f"⟦^{AUTHOR}: @{{{quote}}} {slug}⟧" for slug in hits)
                )
                n_marked += 1
            else:
                pieces.append(sent)
                n_orphan += 1
                orphans.append(sent)
        lines_out.append(" ".join(pieces))

    stats = {"marked": n_marked, "orphan": n_orphan, "orphans": orphans}
    return "\n".join(lines_out), stats


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markdown", type=Path)
    ap.add_argument("claims_dir", type=Path)
    ap.add_argument("-o", "--out", type=Path)
    a = ap.parse_args()

    claims = load_claims(a.claims_dir)
    marked, st = mark_document(a.markdown.read_text(), claims)
    out = a.out or a.markdown.with_suffix(".marked.md")
    out.write_text(marked)

    total = st["marked"] + st["orphan"]
    pct = 100.0 * st["marked"] / total if total else 100.0
    print(f"claims loaded          : {len(claims)}")
    print(f"result sentences       : {total}")
    print(f"  marked               : {st['marked']}  ({pct:.0f}%)")
    print(f"  orphaned             : {st['orphan']}")
    print(f"written                : {out}")
    if st["orphans"]:
        print("\nfirst unmarked result sentences:")
        for s in st["orphans"][:6]:
            print(f"  · {s[:110]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
