"""Step 1 — Prepare: locate paper, fetch text, map figure structure.

Two input paths:
  1. JATS-XML (primary for eLife): structured XML from eLife CDN
  2. PDF (fallback): pdfplumber text extraction with regex section detection

JATS gives us labeled sections, typed figures with captions, structured
references with DOIs, and explicit metadata. PDF works for any journal
but requires heuristic parsing.

The path used is recorded in PreparedPaper.extraction_path because it
constrains what the three agents in Step 3 can extract.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import httpx
from lxml import etree

logger = logging.getLogger(__name__)


# ── eLife CDN URL patterns ───────────────────────────────────────────────
ELIFE_CDN_PDF_URL = "https://cdn.elifesciences.org/articles/{article_id}/elife-{article_id}-v1.pdf"
ELIFE_CDN_XML_URL = "https://cdn.elifesciences.org/articles/{article_id}/elife-{article_id}-v1.xml"

# Cache directory — survives across CLI runs
DEFAULT_CACHE_DIR = Path.home() / ".cache" / "elife-extract"


# ── Section headings ─────────────────────────────────────────────────────
# eLife PDFs sometimes inline section headings with following content (the
# Abstract/Assessment-box layout collapses to "...equally to this work
# Abstract Pyramidal neurons..."). The patterns below allow a heading to
# be followed by content on the same line — what we actually want is the
# *position* of the heading so we can slice from there. The regex demands
# the word is preceded by whitespace and followed by whitespace + a capital
# letter (the start of section content), which excludes mid-sentence
# mentions like "abstract from prior work."
#
# We also tolerate variants like "Materials and methods" (eLife) vs
# "Methods" (other journals).
SECTION_PATTERNS = {
    "abstract": re.compile(r"(?:^|\s)Abstract\s+(?=[A-Z])", re.MULTILINE),
    "introduction": re.compile(r"(?:^|\s)Introduction\s+(?=[A-Z])", re.MULTILINE),
    "results": re.compile(r"(?:^|\s)Results\s+(?=[A-Z])", re.MULTILINE),
    "discussion": re.compile(r"(?:^|\s)Discussion\s+(?=[A-Z])", re.MULTILINE),
    "methods": re.compile(
        r"(?:^|\s)(?:Materials?\s+and\s+[Mm]ethods|Methods)\s+(?=[A-Z])",
        re.MULTILINE,
    ),
    "references": re.compile(r"(?:^|\s)References\s+(?=[A-Z\d])", re.MULTILINE),
    "acknowledgements": re.compile(
        r"(?:^|\s)Acknowled?ge?ments?\s+(?=[A-Z])",
        re.MULTILINE | re.IGNORECASE,
    ),
}

# Figure caption start — eLife uses "Figure N." or "Figure N | " patterns.
# Allow Fig. abbreviation, supplementary figures (S prefix), and mixed casing.
FIG_CAPTION_START = re.compile(
    r"^(Figure|Fig\.?)\s+(?P<num>S?\d+(?:[-–]\d+)?)\.?\s*[|\.\s]",
    re.MULTILINE,
)

# Panel labels within a caption: "(A)", "(a)", letters in parentheses.
# Must NOT use \b before \( since \b is between word/non-word — and there
# is no word char before the paren in caption usage. Use a non-letter or
# start-of-string lookbehind instead.
PANEL_LABEL_RE = re.compile(r"(?:^|[^A-Za-z])\(\s*([A-Za-z])\s*\)", re.MULTILINE)


# ── Data class ───────────────────────────────────────────────────────────


@dataclass
class PreparedPaper:
    """Output of Step 1 — what the three agents in Step 3 read from."""

    doi: str
    article_id: str
    paper_slug: str
    title: str | None
    authors: list[str]
    abstract: str
    results_text: str
    captions_text: str
    methods_text: str
    extraction_path: Literal["jats", "pdf"]
    extraction_path_note: str | None = None
    figure_captions: list["FigureCaption"] = field(default_factory=list)

    @property
    def panel_ids(self) -> list[str]:
        """All panel IDs across all figures (e.g. ['fig1a', 'fig1b', 'fig2', ...])."""
        ids = []
        for fc in self.figure_captions:
            ids.extend(fc.panel_ids())
        return ids


@dataclass
class FigureCaption:
    """One figure's caption with extracted panel labels."""

    figure_num: str  # "1", "2", "S1", "3-5" etc.
    text: str
    panels: list[str]  # e.g. ["a", "b", "c"]; empty if no panel labels found

    def panel_ids(self) -> list[str]:
        """e.g. fig1a, fig1b, ... or just fig1 if no panels detected."""
        prefix = f"fig{self.figure_num.lower()}"
        if not self.panels:
            return [prefix]
        return [f"{prefix}{p.lower()}" for p in self.panels]


# ── DOI / article-ID handling ────────────────────────────────────────────


_ELIFE_DOI_RE = re.compile(r"10\.7554/eLife\.(\d+)", re.IGNORECASE)


def article_id_from_doi(doi: str) -> str:
    """Extract the article ID from an eLife DOI like 10.7554/eLife.95562."""
    m = _ELIFE_DOI_RE.match(doi.strip())
    if not m:
        raise ValueError(
            f"Not a recognized eLife DOI: {doi!r}. "
            "Expected format: 10.7554/eLife.<article-id>"
        )
    return m.group(1)


# ── PDF fetch ────────────────────────────────────────────────────────────


def fetch_pdf(article_id: str, cache_dir: Path | None = None) -> Path:
    """Fetch the eLife PDF for a given article ID. Cache locally.

    Raises httpx.HTTPStatusError on 4xx/5xx; re-uses cached file if present.
    """
    cache_dir = cache_dir or DEFAULT_CACHE_DIR
    cache_dir.mkdir(parents=True, exist_ok=True)
    cached = cache_dir / f"elife-{article_id}-v1.pdf"
    if cached.is_file() and cached.stat().st_size > 0:
        logger.info("using cached PDF: %s", cached)
        return cached

    url = ELIFE_CDN_PDF_URL.format(article_id=article_id)
    logger.info("fetching %s", url)
    with httpx.Client(timeout=60.0, follow_redirects=True) as client:
        resp = client.get(url)
        resp.raise_for_status()
        cached.write_bytes(resp.content)
    return cached


# ── JATS-XML fetch ──────────────────────────────────────────────────────


def fetch_jats(article_id: str, cache_dir: Path | None = None) -> Path:
    """Fetch JATS-XML from eLife CDN. Cache locally."""
    cache_dir = cache_dir or DEFAULT_CACHE_DIR
    cache_dir.mkdir(parents=True, exist_ok=True)
    cached = cache_dir / f"elife-{article_id}-v1.xml"
    if cached.is_file() and cached.stat().st_size > 0:
        logger.info("using cached JATS: %s", cached)
        return cached
    url = ELIFE_CDN_XML_URL.format(article_id=article_id)
    logger.info("fetching %s", url)
    with httpx.Client(timeout=60.0, follow_redirects=True) as client:
        resp = client.get(url)
        resp.raise_for_status()
        cached.write_bytes(resp.content)
    return cached


# ── JATS-XML parsing ────────────────────────────────────────────────────


def _strip_ns(root: etree._Element) -> None:
    """Strip XML namespaces for simpler XPath queries."""
    for el in root.iter():
        if isinstance(el.tag, str) and "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]


def _text(el: etree._Element | None) -> str:
    """Get all text content of an element, joined."""
    if el is None:
        return ""
    return " ".join(el.itertext()).strip()


def _section_text(root: etree._Element, sec_type: str) -> str:
    """Extract full text of a body section by sec-type attribute."""
    for sec in root.findall(f".//body/sec[@sec-type='{sec_type}']"):
        return _text(sec)
    # Fallback: match by title text (some papers use non-standard sec-type)
    for sec in root.findall(".//body/sec"):
        title_el = sec.find("title")
        if title_el is not None and title_el.text:
            t = title_el.text.lower().strip()
            if sec_type == "methods" and ("method" in t or "material" in t):
                return _text(sec)
            if sec_type == "results" and "result" in t:
                return _text(sec)
            if sec_type == "intro" and "intro" in t:
                return _text(sec)
            if sec_type == "discussion" and "discuss" in t:
                return _text(sec)
    return ""


def _extract_jats_figures(root: etree._Element) -> list[FigureCaption]:
    """Extract figure captions from JATS <fig> elements."""
    captions: list[FigureCaption] = []
    for fig in root.findall(".//fig"):
        fig_id = fig.get("id", "")
        label_el = fig.find("label")
        caption_el = fig.find("caption")
        if caption_el is None:
            continue
        # Figure number from label or id
        fig_num = ""
        if label_el is not None and label_el.text:
            m = re.search(r"(S?\d+(?:[-–]\d+)?)", label_el.text)
            fig_num = m.group(1) if m else fig_id.replace("fig", "")
        elif fig_id:
            fig_num = fig_id.replace("fig", "").replace("s", "S")
        caption_text = _text(caption_el)
        # Prefix with label for context
        if label_el is not None and label_el.text:
            caption_text = f"{label_el.text.strip()} {caption_text}"
        # Extract panel labels from caption text
        panels: list[str] = []
        seen: set[str] = set()
        for pm in PANEL_LABEL_RE.finditer(caption_text):
            letter = (pm.group(1) or "").lower()
            if letter and letter not in seen and letter.isalpha() and len(letter) == 1:
                panels.append(letter)
                seen.add(letter)
        captions.append(FigureCaption(figure_num=fig_num, text=caption_text, panels=panels))
    return captions


def _extract_jats_metadata(root: etree._Element) -> tuple[str | None, list[str], str | None]:
    """Extract title, authors, year from JATS front matter."""
    meta = root.find(".//article-meta")
    if meta is None:
        return None, [], None
    # Title
    title_el = meta.find(".//title-group/article-title")
    title = _text(title_el) if title_el is not None else None
    # Authors
    authors: list[str] = []
    for contrib in meta.findall(".//contrib-group/contrib[@contrib-type='author']"):
        gn = contrib.find(".//given-names")
        sn = contrib.find(".//surname")
        if sn is not None:
            name = f"{_text(gn)} {_text(sn)}".strip()
            authors.append(name)
    # Year
    year: str | None = None
    pub_date = meta.find(".//pub-date[@date-type='publication']")
    if pub_date is None:
        pub_date = meta.find(".//pub-date")
    if pub_date is not None:
        year_el = pub_date.find("year")
        if year_el is not None and year_el.text:
            year = year_el.text.strip()
    return title, authors, year


def parse_jats(xml_path: Path, doi: str, paper_slug_override: str | None = None) -> PreparedPaper:
    """Parse a JATS-XML file into PreparedPaper."""
    tree = etree.parse(str(xml_path))
    root = tree.getroot()
    _strip_ns(root)

    article_id = article_id_from_doi(doi)
    title, authors, year = _extract_jats_metadata(root)
    slug = paper_slug_override or derive_slug(authors, year, title)

    abstract_el = root.find(".//article-meta/abstract")
    abstract = _text(abstract_el)
    results_text = _section_text(root, "results")
    methods_text = _section_text(root, "methods")
    captions = _extract_jats_figures(root)

    return PreparedPaper(
        doi=doi,
        article_id=article_id,
        paper_slug=slug,
        title=title,
        authors=authors,
        abstract=abstract,
        results_text=results_text,
        captions_text=captions_text_block(captions),
        methods_text=methods_text,
        extraction_path="jats",
        extraction_path_note=f"JATS-XML from {ELIFE_CDN_XML_URL.format(article_id=article_id)}",
        figure_captions=captions,
    )


# ── PDF text extraction ──────────────────────────────────────────────────


def extract_text(pdf_path: Path) -> str:
    """Extract full text from PDF using pdfplumber, preserving line breaks."""
    import pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        pages = [p.extract_text() or "" for p in pdf.pages]
    return "\n".join(pages)


# ── Section slicing ──────────────────────────────────────────────────────


def find_section_offsets(text: str) -> dict[str, int]:
    """Return char-offset of each detected section heading."""
    offsets: dict[str, int] = {}
    for name, pattern in SECTION_PATTERNS.items():
        m = pattern.search(text)
        if m:
            offsets[name] = m.start()
    return offsets


def slice_sections(text: str) -> dict[str, str]:
    """Slice the full text into named sections.

    Returns a dict with keys: abstract, introduction, results, discussion,
    methods, references, acknowledgements (when found). Each value is the
    text BETWEEN that heading and the next heading (or end of doc). The
    heading itself is consumed.
    """
    offsets = find_section_offsets(text)
    if not offsets:
        return {}

    # Sort sections by position so we can slice between them
    ordered = sorted(offsets.items(), key=lambda kv: kv[1])
    sections: dict[str, str] = {}

    for i, (name, start) in enumerate(ordered):
        # Skip the heading line itself
        m = SECTION_PATTERNS[name].search(text, start)
        section_start = m.end() if m else start
        section_end = ordered[i + 1][1] if i + 1 < len(ordered) else len(text)
        sections[name] = text[section_start:section_end].strip()

    return sections


# ── Figure caption extraction ────────────────────────────────────────────


def extract_figure_captions(text: str) -> list[FigureCaption]:
    """Find figure captions and extract their panel labels.

    Captions in eLife PDFs typically appear:
      - In the body text near where the figure is referenced (some journals)
      - Listed together at the end of the paper (eLife convention varies)

    Heuristic: match "Figure N." or "Fig. N." at line-start and consume
    until the next caption start or a clear stop pattern (next section
    heading, end of document).
    """
    captions: list[FigureCaption] = []
    matches = list(FIG_CAPTION_START.finditer(text))
    if not matches:
        return captions

    for i, m in enumerate(matches):
        fig_num = m.group("num")
        start = m.start()
        # End at the next caption's start, or at the next section heading,
        # whichever comes first. Cap at 4000 chars to avoid runaway.
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = min(start + 4000, len(text))
        # Also stop at any new major section heading
        for section_re in SECTION_PATTERNS.values():
            sm = section_re.search(text, start + 1, end)
            if sm and sm.start() < end:
                end = sm.start()
        caption_text = text[start:end].strip()

        # Extract panel labels
        panel_letters: list[str] = []
        seen = set()
        for pm in PANEL_LABEL_RE.finditer(caption_text):
            letter = (pm.group(1) or "").lower()
            if letter and letter not in seen and letter.isalpha() and len(letter) == 1:
                panel_letters.append(letter)
                seen.add(letter)

        captions.append(
            FigureCaption(figure_num=fig_num, text=caption_text, panels=panel_letters)
        )

    return captions


def captions_text_block(captions: list[FigureCaption]) -> str:
    """Format the figure captions as a single text block for the Caption-reader agent."""
    parts = []
    for fc in captions:
        parts.append(f"=== Figure {fc.figure_num} ===")
        parts.append(fc.text)
        if fc.panels:
            parts.append(f"[panels detected: {', '.join(fc.panels)}]")
        parts.append("")
    return "\n".join(parts)


# ── Slug derivation ──────────────────────────────────────────────────────


def derive_slug(authors: list[str], year: str | None, title: str | None) -> str:
    """Derive a paper slug like 'headley-2026-inhibitory-rhythms' from metadata.

    First author surname + year + a short content phrase from the title.
    Best-effort; the analyst can override at write time via --paper-slug.
    """
    surname = (authors[0].split()[-1] if authors else "unknown").lower()
    surname = re.sub(r"[^a-z]", "", surname)
    year_part = year or "unknown"
    if title:
        # Take 2-3 content words, lowercased, hyphenated
        words = re.findall(r"\b[A-Za-z]{4,}\b", title)
        skip = {"with", "from", "into", "between", "during", "their", "that", "this",
                "these", "those", "have", "been", "were", "will", "should", "would",
                "while", "where", "when", "what", "such"}
        keep = [w.lower() for w in words if w.lower() not in skip][:3]
        content = "-".join(keep) if keep else "untitled"
    else:
        content = "untitled"
    return f"{surname}-{year_part}-{content}"


# ── Title / authors extraction ───────────────────────────────────────────
# These are heuristic. Phase C ships them as best-effort; the analyst can
# override via CLI flag.

_YEAR_RE = re.compile(r"\b(20\d{2})\b")


def guess_metadata(text: str) -> tuple[str | None, list[str], str | None]:
    """Pull title, authors, year from the first ~3000 chars of the PDF.

    Heuristic; may miss for atypical layouts. Returns (title, authors, year).
    """
    head = text[:3000]
    lines = [ln.strip() for ln in head.splitlines() if ln.strip()]
    title = None
    authors: list[str] = []
    year: str | None = None

    # Title is typically the first non-trivial line of the PDF
    for ln in lines[:20]:
        # Skip obvious non-title artifacts
        if any(s in ln.lower() for s in ("research article", "elife", "doi:", "https://")):
            continue
        if len(ln) > 20 and len(ln) < 300 and not ln.endswith("."):
            title = ln
            break

    # Authors: look for a line with multiple capitalized name-tokens after the title
    if title:
        try:
            ti = lines.index(title)
            for ln in lines[ti + 1 : ti + 8]:
                if "@" in ln or "elifesciences" in ln.lower():
                    continue
                # Heuristic: comma-separated names with capitalized words
                if "," in ln and len(re.findall(r"\b[A-Z][a-z]+", ln)) >= 4:
                    parts = [p.strip(" *†‡§¶") for p in ln.split(",")]
                    authors = [p for p in parts if len(p) > 3 and len(p) < 60]
                    break
        except ValueError:
            pass

    # Year — first 4-digit year in the head section
    ym = _YEAR_RE.search(head)
    if ym:
        year = ym.group(1)

    return title, authors, year


# ── Top-level prepare() ──────────────────────────────────────────────────


def prepare(
    doi: str,
    paper_slug_override: str | None = None,
    cache_dir: Path | None = None,
    input_format: Literal["auto", "jats", "pdf"] = "auto",
) -> PreparedPaper:
    """Fetch and slice a paper into the three agent inputs.

    input_format:
      - "auto" (default): use JATS for eLife DOIs, PDF otherwise
      - "jats": force JATS-XML input
      - "pdf": force PDF input
    """
    article_id = article_id_from_doi(doi)

    if input_format == "auto":
        input_format = "jats"  # eLife DOIs always have JATS

    if input_format == "jats":
        xml_path = fetch_jats(article_id, cache_dir=cache_dir)
        return parse_jats(xml_path, doi, paper_slug_override)

    # PDF fallback
    pdf_path = fetch_pdf(article_id, cache_dir=cache_dir)
    full_text = extract_text(pdf_path)

    sections = slice_sections(full_text)
    captions = extract_figure_captions(full_text)

    title, authors, year = guess_metadata(full_text)
    slug = paper_slug_override or derive_slug(authors, year, title)

    return PreparedPaper(
        doi=doi,
        article_id=article_id,
        paper_slug=slug,
        title=title,
        authors=authors,
        abstract=sections.get("abstract", ""),
        results_text=sections.get("results", ""),
        captions_text=captions_text_block(captions),
        methods_text=sections.get("methods", ""),
        extraction_path="pdf",
        extraction_path_note=f"PDF from {ELIFE_CDN_PDF_URL.format(article_id=article_id)}",
        figure_captions=captions,
    )
