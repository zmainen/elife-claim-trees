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
import unicodedata
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
# Captions label panels three ways, and all three must be read:
#   singles  "( A )"
#   lists    "( A, D )"   "(A and B)"
#   ranges   "( A-D )"    meaning A, B, C, D
# Reading only singles lost B, C, E and F of Figure 2; reading a range as a
# two-item list lost C, D, F and G of Figure 3. Parenthesised letters are also
# used for abbreviations — "low outcomes (L)", "(L-H)" — so a descending or
# implausible range is rejected, and a letter outside the panel run is dropped.
PANEL_GROUP_RE = re.compile(r"(?:^|[^A-Za-z])\(\s*([A-Za-z][^()]{0,24}?)\s*\)")


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
    tables: list["TableCaption"] = field(default_factory=list)
    appendix_text: str = ""
    supplementary_text: str = ""
    # The Introduction states the organising hypothesis and the questions; the Discussion states
    # the interpretation and the literature-context premises. Both were parsed and thrown away
    # until now, so no reader saw them. Defaults keep every committed prepared.json loadable.
    introduction_text: str = ""
    discussion_text: str = ""
    # The paper cut into the numbered spans coverage segments, so a reader can cite the id in
    # front of a sentence and coverage can match a claim to a span rather than re-finding it by
    # string. One dict per span: {uid, section, text}. Filled by prepare via the segmenter.
    spans: list[dict] = field(default_factory=list)

    @property
    def tables_text(self) -> str:
        return "\n\n".join(t.text for t in self.tables)

    @property
    def panel_ids(self) -> list[str]:
        """All panel IDs across all figures (e.g. ['fig1a', 'fig1b', 'fig2', ...])."""
        ids = []
        for fc in self.figure_captions:
            ids.extend(fc.panel_ids())
        ids.extend(t.panel_id() for t in self.tables)
        return ids

    def panel_inventory(self) -> str:
        """One line per figure and table: its id, its panel ids, and the caption's first sentence.

        The results reader reads the sentences that say what each panel is for but was given no
        list of the panels that exist, so it left most claims unanchored and could not tell a
        real panel from one it imagined. This is that list, in the ids the paper already carries.
        """
        lines: list[str] = []
        for fc in self.figure_captions:
            lines.append(f"{fc.base_id()}: {', '.join(fc.panel_ids())} — {_caption_head(fc.text)}")
        for t in self.tables:
            lines.append(f"{t.panel_id()}: {t.panel_id()} — {_caption_head(t.text)}")
        return "\n".join(lines)


@dataclass
class FigureCaption:
    """One figure's caption with extracted panel labels."""

    figure_num: str  # display label: "1", "2", "S1", "3-5" etc.
    text: str
    panels: list[str]  # e.g. ["a", "b", "c"]; empty if no panel labels found
    element_id: str = ""   # the JATS <fig id> verbatim, when the source has one

    def base_id(self) -> str:
        """The figure's identifier — the document's own, wherever it has one.

        eLife's JATS assigns every figure and table an id (`fig2`, `fig3s1`,
        `app1table4`, `keyresource`). Parsing the human-readable label and
        rebuilding an id from it was inventing a second name for something
        already named, and the two disagreed: "Appendix 1—table 4" became
        `tableapp1-4` where the document itself says `app1table4`. Inherit the
        identifier; derive one only from a source that has none, which is the
        PDF path.
        """
        return self.element_id or f"fig{self.figure_num.lower()}"

    def panel_ids(self) -> list[str]:
        """e.g. fig1a, fig1b, ... or just fig1 if no panels detected.

        Panels are the one thing genuinely not inherited: JATS marks figures,
        not panels. So the panel id extends the figure's own id with the letter
        the article itself prints ("Figure 2C" -> fig2 + c).
        """
        base = self.base_id()
        if not self.panels:
            return [base]
        return [f"{base}{p.lower()}" for p in self.panels]


@dataclass
class TableCaption:
    """One table: label, caption and tabulated values as flat text."""

    table_num: str
    text: str
    element_id: str = ""   # the JATS <table-wrap id> verbatim

    def panel_id(self) -> str:
        """The table's identifier — the document's own where it has one."""
        return self.element_id or f"table{self.table_num.lower()}"


# The label a caption opens with ("Figure 2.", "Table 1.", "Appendix 1—table 4.") is not part
# of the sentence that says what the float shows, so it is stripped before the first sentence.
_CAPTION_LABEL_RE = re.compile(r"^\s*(?:Figure|Fig\.?|Table|Appendix)[^.]*\.\s*", re.IGNORECASE)


def _caption_head(text: str, limit: int = 160) -> str:
    """The first sentence of a caption, minus its "Figure N." label — the inventory line."""
    t = _CAPTION_LABEL_RE.sub("", " ".join(text.split()), count=1)
    m = re.search(r"(.+?[.!?])(?:\s|$)", t)
    return (m.group(1) if m else t)[:limit].strip()


def _build_spans(paper: "PreparedPaper") -> list[dict]:
    """The paper's spans, in the shape prepared.json records — the segmenter coverage uses."""
    from .segment import segment  # deferred: segment imports PreparedPaper from here
    return [{"uid": s.uid, "section": s.section, "text": s.text}
            for s in segment(paper, include_methods=True)]


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


def _main_scopes(root: etree._Element) -> list[etree._Element]:
    """The article's own content, excluding <sub-article>.

    eLife JATS embeds the editor assessment, referee reports and author
    response as <sub-article> elements, each with its own <body>, <sec> and
    sometimes <fig>. A `.//body/sec` or `.//fig` search reaches into them, so
    referee prose could be extracted as the authors' claims. Scope to the
    article's own body and floats-group instead.
    """
    scopes = [el for el in (root.find("body"), root.find("floats-group"))
              if el is not None]
    return scopes or [root]


def _section_text(root: etree._Element, sec_type: str) -> str:
    """Extract full text of a body section by sec-type attribute."""
    body = root.find("body")
    if body is None:
        return ""
    for sec in body.findall(f"sec[@sec-type='{sec_type}']"):
        return _text(sec)
    # Fallback: match by title text (some papers use non-standard sec-type)
    for sec in body.findall("sec"):
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


def _panel_letters(caption: str) -> list[str]:
    """Panel letters named in a caption, expanding lists and ranges."""
    found: list[str] = []
    seen: set[str] = set()
    for m in PANEL_GROUP_RE.finditer(caption):
        body = m.group(1).strip()
        if not re.fullmatch(r"[A-Za-z](\s*(?:,|and|&|[-\u2013\u2014])\s*[A-Za-z])*",
                            body, re.IGNORECASE):
            continue
        rng = re.fullmatch(r"([A-Za-z])\s*[-\u2013\u2014]\s*([A-Za-z])", body)
        if rng:
            a, b = rng.group(1).lower(), rng.group(2).lower()
            # Descending or absurdly wide means it is not a panel range —
            # "(L-H)" is low-minus-high, not panels L through H.
            if not (0 < ord(b) - ord(a) <= 8):
                continue
            letters = [chr(c) for c in range(ord(a), ord(b) + 1)]
        else:
            letters = [t.lower() for t in re.split(r"[^A-Za-z]+", body)
                       if len(t) == 1]
        for letter in letters:
            if letter.isalpha() and letter not in seen:
                found.append(letter)
                seen.add(letter)
    return _contiguous_panels(found)


def _contiguous_panels(letters: list[str]) -> list[str]:
    """Keep the run of panel letters that starts at the lowest one present.

    Captions use parenthesised letters for two different jobs: panel labels
    and abbreviations. Figure 4 here labels panels ( A ) … ( I ) and also
    writes "low lottery outcomes (L)" and "(L–H)" — L is an abbreviation, not
    a tenth panel. Real panels are consecutive; a letter separated from the
    run by a gap is something else. Spacing distinguishes them in this
    publisher's typesetting, but sequence is the general rule.
    """
    if not letters:
        return []
    ordered = sorted(set(letters))
    keep = [ordered[0]]
    for prev, cur in zip(ordered, ordered[1:]):
        if ord(cur) - ord(prev) != 1:
            break
        keep.append(cur)
    return [c for c in letters if c in set(keep)]


def _extract_jats_figures(root: etree._Element) -> list[FigureCaption]:
    """Extract figure captions from JATS <fig> elements."""
    captions: list[FigureCaption] = []
    figs = [f for scope in _main_scopes(root) for f in scope.iter("fig")]
    for fig in figs:
        fig_id = fig.get("id", "")
        label_el = fig.find("label")
        caption_el = fig.find("caption")
        if caption_el is None:
            continue
        # Figure number from label or id
        fig_num = ""
        label_txt = _text(label_el) if label_el is not None else ""
        if label_txt:
            # "Figure 3-figure supplement 1" must not collapse onto "Figure 3".
            sup = re.search(r"(\d+)\s*[—–-]\s*figure\s+supplement\s+(\d+)",
                            label_txt, re.IGNORECASE)
            if sup:
                fig_num = f"{sup.group(1)}s{sup.group(2)}"
            else:
                m = re.search(r"(S?\d+(?:[-–]\d+)?)", label_txt)
                fig_num = m.group(1) if m else fig_id.replace("fig", "")
        elif fig_id:
            fig_num = fig_id.replace("fig", "").replace("s", "S")
        caption_text = _text(caption_el)
        # Prefix with label for context
        if label_el is not None and label_el.text:
            caption_text = f"{label_el.text.strip()} {caption_text}"
        # Extract panel labels from caption text
        panels = _panel_letters(caption_text)
        captions.append(FigureCaption(figure_num=fig_num, text=caption_text, panels=panels,
                                      element_id=fig_id))
    return captions



def _extract_jats_tables(root: etree._Element) -> list["TableCaption"]:
    """Extract tables: label, caption, and the tabulated values themselves.

    Tables carry results that appear nowhere else — this corpus already cites
    `table1` as the panel for a claim about model weights — yet nothing in the
    pipeline read them. Caption alone is not enough: the numbers are in the
    cells.
    """
    tables: list[TableCaption] = []
    # Most tables in an eLife article sit in <back><app-group><app>, not the
    # body — 11 of 13 for this paper. Scoping to the body found two.
    scopes = _main_scopes(root) + [el for el in (root.find("back"),) if el is not None]
    wraps = [t for scope in scopes for t in scope.iter("table-wrap")]
    for tw in wraps:
        label_el = tw.find("label")
        label = _text(label_el) if label_el is not None else ""
        app = re.search(r"Appendix\s*(\d+)\s*[—–-]\s*table\s*(\d+)", label, re.I)
        if app:
            num = f"app{app.group(1)}-{app.group(2)}"
        else:
            m = re.search(r"(S?\d+)", label)
            num = m.group(1) if m else re.sub(r"[^a-z0-9]+", "", (tw.get("id") or label).lower())[:24]
        cap = tw.find("caption")
        body = tw.find(".//table")
        text = " ".join(x for x in (label, _text(cap), _text(body)) if x).strip()
        if text:
            tables.append(TableCaption(table_num=num, text=text,
                                       element_id=(tw.get("id") or "")))
    return tables


def _extract_appendices(root: etree._Element) -> str:
    """Appendix / supplementary prose from <app-group>."""
    parts = []
    for app in root.iter("app"):
        parts.append(_text(app))
    return "\n\n".join(p for p in parts if p)


def _extract_supplementary(root: etree._Element) -> str:
    """Titles and captions of supplementary-material blocks.

    The files themselves are not fetched; recording that they exist keeps them
    visible in the assertion inventory rather than silently absent.
    """
    parts = []
    for sm in root.iter("supplementary-material"):
        label = sm.find("label")
        cap = sm.find("caption")
        bits = [_text(label) if label is not None else "", _text(cap) if cap is not None else ""]
        line = " ".join(b for b in bits if b).strip()
        if line:
            parts.append(line)
    return "\n".join(parts)


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
    introduction_text = _section_text(root, "intro")
    results_text = _section_text(root, "results")
    discussion_text = _section_text(root, "discussion")
    methods_text = _section_text(root, "methods")
    captions = _extract_jats_figures(root)
    tables = _extract_jats_tables(root)
    appendix = _extract_appendices(root)
    supplementary = _extract_supplementary(root)

    paper = PreparedPaper(
        doi=doi,
        article_id=article_id,
        paper_slug=slug,
        title=title,
        authors=authors,
        abstract=abstract,
        results_text=results_text,
        captions_text=captions_text_block(captions),
        methods_text=methods_text,
        tables=tables,
        appendix_text=appendix,
        supplementary_text=supplementary,
        introduction_text=introduction_text,
        discussion_text=discussion_text,
        extraction_path="jats",
        extraction_path_note=f"JATS-XML from {ELIFE_CDN_XML_URL.format(article_id=article_id)}",
        figure_captions=captions,
    )
    paper.spans = _build_spans(paper)
    return paper


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


def _ascii_fold(text: str) -> str:
    """Fold accented Latin characters to ASCII so slugs stay readable.

    Slug derivation matched [A-Za-z] only, which silently *dropped* accented
    characters rather than transliterating them: Gadeke's surname became
    "gdeke", Muller "mller", Angstrom "ngstrm". For a European journal corpus
    that is not an edge case. NFKD splits a letter from its combining mark;
    dropping only the marks leaves the base letter behind.
    """
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    # Ligatures and letters with a stroke have no combining decomposition.
    for src, dst in (("ß", "ss"), ("Ø", "O"), ("ø", "o"), ("Æ", "AE"),
                     ("æ", "ae"), ("Œ", "OE"), ("œ", "oe"), ("Đ", "D"),
                     ("đ", "d"), ("Ł", "L"), ("ł", "l")):
        text = text.replace(src, dst)
    return text


def derive_slug(authors: list[str], year: str | None, title: str | None) -> str:
    """Derive a paper slug like 'headley-2026-inhibitory-rhythms' from metadata.

    First author surname + year + a short content phrase from the title.
    Best-effort; the analyst can override at write time via --paper-slug.
    """
    surname = _ascii_fold(authors[0].split()[-1] if authors else "unknown").lower()
    surname = re.sub(r"[^a-z]", "", surname)
    year_part = year or "unknown"
    if title:
        # Take 2-3 content words, lowercased, hyphenated
        words = re.findall(r"\b[A-Za-z]{4,}\b", _ascii_fold(title))
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
    doi: str | None = None,
    paper_slug_override: str | None = None,
    cache_dir: Path | None = None,
    input_format: Literal["auto", "jats", "pdf"] = "auto",
    pdf_path: Path | None = None,
) -> PreparedPaper:
    """Fetch and slice a paper into the three agent inputs.

    input_format:
      - "auto" (default): use JATS for eLife DOIs, PDF otherwise
      - "jats": force JATS-XML input
      - "pdf": force PDF input

    pdf_path supplies a local PDF for a paper that is not on the eLife CDN.
    It bypasses fetching, forces the PDF path, and makes `doi` optional.
    """
    if not doi and pdf_path is None:
        raise ValueError("prepare() requires a DOI or a local pdf_path")

    article_id = article_id_from_doi(doi) if doi else None

    if pdf_path is not None:
        input_format = "pdf"
    elif input_format == "auto":
        input_format = "jats"  # eLife DOIs always have JATS

    if input_format == "jats":
        if article_id is None:
            raise ValueError("JATS input requires a DOI")
        xml_path = fetch_jats(article_id, cache_dir=cache_dir)
        return parse_jats(xml_path, doi, paper_slug_override)

    # PDF path — a local file when given, otherwise fetched from the eLife CDN.
    if pdf_path is None:
        pdf_path = fetch_pdf(article_id, cache_dir=cache_dir)
        source_note = f"PDF from {ELIFE_CDN_PDF_URL.format(article_id=article_id)}"
    else:
        source_note = f"local PDF at {pdf_path}"
    full_text = extract_text(pdf_path)

    sections = slice_sections(full_text)
    captions = extract_figure_captions(full_text)

    title, authors, year = guess_metadata(full_text)
    slug = paper_slug_override or derive_slug(authors, year, title)

    # The section slicer already detects Introduction and Discussion; the two branches were
    # simply never read out.
    paper = PreparedPaper(
        doi=doi or "",
        article_id=article_id or "",
        paper_slug=slug,
        title=title,
        authors=authors,
        abstract=sections.get("abstract", ""),
        results_text=sections.get("results", ""),
        captions_text=captions_text_block(captions),
        methods_text=sections.get("methods", ""),
        introduction_text=sections.get("introduction", ""),
        discussion_text=sections.get("discussion", ""),
        extraction_path="pdf",
        extraction_path_note=source_note,
        figure_captions=captions,
    )
    paper.spans = _build_spans(paper)
    return paper
