#!/usr/bin/env python3
"""The article, as the site renders it: JATS-XML into one JSON file per paper.

`prepare` already fetches the JATS and keeps four flattened strings from it — abstract,
results, captions, methods — which is everything the three readers need and nothing a page
needs. `results_text` is one string with the section headings glued to the sentences that
follow them, so a site that wants to show the paper cannot recover where the sections were.

This keeps the structure instead: the section tree, each paragraph with its inline markup,
the figures with their captions, the tables with their rows. It calls no model and reads the
same cached XML `prepare` fetched, so it is free to re-run and its output is byte-stable —
nothing here stamps a date, which is what stops a rebuild from marking every paper stale.

    python3 scripts/article_json.py gadeke-2026-guilt-insula
    python3 scripts/article_json.py --all
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "extract"))

from lxml import etree  # noqa: E402
from elife_extract.prepare import article_id_from_doi, fetch_jats  # noqa: E402

OUT_DIR = ROOT / "site" / "src" / "data" / "article"
FIGURE_DIR = ROOT / "site" / "public" / "figures"
IIIF = ("https://iiif.elifesciences.org/lax/"
        "{aid}%2Felife-{aid}-{fig}-v1.tif/full/1500,/0/default.jpg")


# ── the paper's own record ────────────────────────────────────────────────────

def index_frontmatter(paper: str) -> dict:
    """The paper's index.md frontmatter — where the DOI lives."""
    p = ROOT / "claims" / paper / "index.md"
    text = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, flags=re.S)
    if not m:
        raise SystemExit(f"{p}: no frontmatter")
    import yaml
    return yaml.safe_load(m.group(1))


# ── JATS ──────────────────────────────────────────────────────────────────────

def strip_ns(root) -> None:
    for el in root.iter():
        if isinstance(el.tag, str) and "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]


def plain(el) -> str:
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def inline(el, *, drop=()) -> str:
    """One JATS element as the minimal HTML the reader needs.

    Six tags, and each earns its place: italic and bold because a paper's variables and panel
    letters are set in them, sup/sub because an exponent that loses its markup becomes a
    different number, `xref` because a reference to Figure 3 should reach Figure 3, and
    `disp-formula` because an equation dropped silently is a sentence that no longer parses.
    Everything else is unwrapped rather than kept, so nothing arrives in a class this page
    has no style for.
    """
    def esc(s: str) -> str:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    parts = [esc(el.text or "")]
    for ch in el:
        if ch.tag in drop:
            parts.append(esc(ch.tail or ""))
            continue
        inner = inline(ch, drop=drop)
        if ch.tag == "italic":
            parts.append(f"<i>{inner}</i>")
        elif ch.tag in ("bold", "sc"):
            parts.append(f"<b>{inner}</b>")
        elif ch.tag == "sup":
            parts.append(f"<sup>{inner}</sup>")
        elif ch.tag == "sub":
            parts.append(f"<sub>{inner}</sub>")
        elif ch.tag == "xref":
            rid, rt = ch.get("rid", ""), ch.get("ref-type")
            if rt == "fig":
                parts.append(f'<a class="xref" href="#{rid}">{inner}</a>')
            elif rt == "table":
                parts.append(f'<a class="xref" href="#{rid}">{inner}</a>')
            elif rt == "bibr":
                parts.append(f'<span class="cite">{inner}</span>')
            else:
                parts.append(inner)
        elif ch.tag in ("inline-formula", "disp-formula", "mml:math"):
            parts.append(f'<span class="math">{plain(ch)}</span>')
        else:
            parts.append(inner)
        parts.append(esc(ch.tail or ""))
    return re.sub(r"[ \t]+", " ", "".join(parts)).strip()


def figure_record(fig, aid: str, paper: str) -> dict:
    """One <fig>. `fig3s1` is eLife's id for a supplement; its image is `fig3-figsupp1`."""
    fid = fig.get("id") or ""
    supp = re.match(r"^fig(\d+)s(\d+)$", fid)
    num = re.sub(r"\D", "", fid.split("s")[0]) if fid.startswith("fig") else ""
    image_id = f"fig{supp.group(1)}-figsupp{supp.group(2)}" if supp else fid
    cap = fig.find("caption")
    label = plain(fig.find("label")) if fig.find("label") is not None else ""
    title = plain(cap.find("title")) if cap is not None and cap.find("title") is not None else ""
    body = "".join(f"<p>{inline(p)}</p>" for p in cap.findall("p")) if cap is not None else ""
    local = FIGURE_DIR / paper / f"fig{num}.jpg"
    return {
        "id": fid,
        "num": num,
        "label": label.rstrip(". ") or (f"Figure {num}" if num else fid),
        "title": title,
        "caption": body,
        "supplement": bool(supp),
        "src": (f"/figures/{paper}/fig{num}.jpg" if (local.is_file() and not supp)
                else IIIF.format(aid=aid, fig=image_id)),
    }


def table_record(tw) -> dict:
    """One <table-wrap>, kept as a table.

    A paper's table is where a model comparison or a parameter set lives, and Gädeke's Table 1
    carries ten claim marks on its own. Flattening it to text loses the column that says which
    model won.
    """
    cap = tw.find("caption")
    label = plain(tw.find("label")) if tw.find("label") is not None else ""
    title = plain(cap.find("title")) if cap is not None and cap.find("title") is not None else ""
    body = "".join(f"<p>{inline(p)}</p>" for p in cap.findall("p")) if cap is not None else ""
    rows = []
    table = tw.find("table")
    if table is not None:
        for tr in table.iter("tr"):
            cells = [{"tag": "th" if td.tag == "th" else "td",
                      "html": inline(td),
                      "colspan": td.get("colspan")} for td in tr if td.tag in ("td", "th")]
            if cells:
                rows.append(cells)
    return {"id": tw.get("id") or "", "label": label.rstrip(". ") or title,
            "title": title, "caption": body, "rows": rows}


def section(sec, depth: int, aid: str, paper: str, figs: dict, tables: dict) -> dict:
    """One <sec>, with its paragraphs, floats and children in document order."""
    blocks = []
    for ch in sec:
        if ch.tag == "p":
            html = inline(ch, drop=("fig", "table-wrap", "disp-formula"))
            if html:
                blocks.append({"type": "p", "html": html, "text": plain(ch)})
            for f in ch.iter("fig"):
                figs[f.get("id")] = figure_record(f, aid, paper)
                blocks.append({"type": "fig", "id": f.get("id")})
        elif ch.tag == "fig":
            figs[ch.get("id")] = figure_record(ch, aid, paper)
            blocks.append({"type": "fig", "id": ch.get("id")})
        elif ch.tag == "fig-group":
            for f in ch.findall("fig"):
                figs[f.get("id")] = figure_record(f, aid, paper)
                blocks.append({"type": "fig", "id": f.get("id")})
        elif ch.tag == "table-wrap":
            tables[ch.get("id")] = table_record(ch)
            blocks.append({"type": "table", "id": ch.get("id")})
        elif ch.tag == "disp-formula":
            blocks.append({"type": "formula", "text": plain(ch)})
        elif ch.tag == "sec":
            blocks.append({"type": "sec", "sec": section(ch, depth + 1, aid, paper, figs, tables)})
    title_el = sec.find("title")
    return {
        "id": sec.get("id") or "",
        "type": sec.get("sec-type") or "",
        "title": plain(title_el) if title_el is not None else "",
        "depth": depth,
        "blocks": blocks,
    }


# Sentence split for the abstract only. The body's sentences come from the marked paper, which
# is where the claim assignments are; splitting them twice, by two rules, would give the site
# two different sentences to reconcile.
_ABBR = r"(?<!\be\.g)(?<!\bi\.e)(?<!\bcf)(?<!\bvs)(?<!\bFig)(?<!\bet al)"


def sentences(text: str) -> list[str]:
    parts = re.split(rf"{_ABBR}(?<=[.!?])\s+(?=[A-Z(])", text)
    return [p.strip() for p in parts if p.strip()]


def build(paper: str) -> dict:
    fm = index_frontmatter(paper)
    doi = fm.get("doi")
    if not doi:
        raise SystemExit(f"{paper}: no doi in claims/{paper}/index.md")
    aid = article_id_from_doi(doi)
    root = etree.parse(str(fetch_jats(aid))).getroot()
    strip_ns(root)

    # `root.find` takes the article's own children, so the editor assessment, the referee
    # reports and the author response — each a <sub-article> with a <body> of its own — stay
    # out. A `.//body` search reaches into all of them.
    front = root.find("front/article-meta")
    body = root.find("body")
    if body is None:
        raise SystemExit(f"{paper}: no <body> in the JATS")

    authors = []
    for grp in front.findall("contrib-group"):
        for c in grp.findall("contrib"):
            if c.get("contrib-type") != "author":
                continue
            n = c.find("name")
            if n is None:
                continue
            given = plain(n.find("given-names")) if n.find("given-names") is not None else ""
            surname = plain(n.find("surname")) if n.find("surname") is not None else ""
            full = f"{given} {surname}".strip()
            if full and full not in authors:
                authors.append(full)

    pub = front.find("pub-date")
    year = plain(pub.find("year")) if pub is not None and pub.find("year") is not None else ""
    kwds = []
    for g in front.findall("kwd-group"):
        if g.get("kwd-group-type") == "author-keywords":
            kwds = [plain(k) for k in g.findall("kwd")]

    abs_el = front.find("abstract")
    abstract_text = " ".join(plain(p) for p in abs_el.findall("p")) if abs_el is not None else ""

    figs: dict = {}
    tables: dict = {}
    secs = [section(s, 1, aid, paper, figs, tables) for s in body.findall("sec")]

    return {
        "slug": paper,
        "doi": doi,
        "articleId": aid,
        "source": f"https://cdn.elifesciences.org/articles/{aid}/elife-{aid}-v1.xml",
        "title": plain(front.find("title-group/article-title")),
        "authors": authors,
        "year": year,
        "keywords": kwds,
        "abstract": [{"text": s} for s in sentences(abstract_text)],
        "sections": secs,
        "figures": list(figs.values()),
        "tables": list(tables.values()),
    }


def write(paper: str) -> None:
    data = build(paper)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{paper}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    def count(secs):
        n = 0
        for s in secs:
            for b in s["blocks"]:
                n += 1 if b["type"] == "p" else 0
                if b["type"] == "sec":
                    n += count([b["sec"]])
        return n

    print(f"  {paper:38} {len(data['sections'])} sections · {count(data['sections'])} paragraphs · "
          f"{len(data['figures'])} figures · {len(data['tables'])} tables")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper", nargs="?", help="paper slug")
    ap.add_argument("--all", action="store_true", help="every paper in the corpus")
    args = ap.parse_args()
    if args.all:
        import yaml
        manifest = yaml.safe_load((ROOT / "corpus.yaml").read_text())
        slugs = manifest["corpora"]["elife"]["papers"]
    elif args.paper:
        slugs = [args.paper]
    else:
        ap.error("give a paper slug or --all")
    for s in slugs:
        write(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
