"""Segmentation — cut the paper into spans that must each be accounted for.

This is the base pass. Everything else measures itself against it.

The problem it replaces: coverage was computed by finding statistics with a
regex and checking whether their exact text appeared in some claim. That fails
constantly and in both directions. A paper reporting `p = 0.0004` and a claim
saying "p < 0.001" is the same result stated two ways, and scores as a miss. A
claim that states an effect without restating its number scores as a miss. A
statistic the regex does not match is invisible on both sides, so it cannot
even be missed.

The fix is to stop inventing the denominator and take it from the document. Cut
the text into spans, mechanically and exhaustively; every span is then either
accounted for by some claim or it is not, and "not" is a fact about the text
rather than about a pattern.

Spans are sentences, because a sentence is the smallest span that reliably
carries one assertion in scientific prose, and because sentence boundaries can
be found without a model. Splitting scientific prose is not naive, though:
"Fig. 2", "et al.", "e.g.", "p = 0.03.", "0.5 mm", and author initials all put
a period where no sentence ends. Those cases are enumerated below rather than
hidden in a general-purpose splitter, so a failure is visible and fixable.

Each span carries features — the statistics in it, the panels it names, whether
it cites — which downstream passes use for routing and reporting. The features
are *derived from* the span; the span is never derived from the features.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field

from .prepare import PreparedPaper

logger = logging.getLogger(__name__)


# ── Sentence segmentation ────────────────────────────────────────────────

# Abbreviations that end in a period without ending a sentence. Kept explicit:
# a general splitter fails silently on domain text, and this list is the thing
# to extend when it does.
_ABBREV = {
    # bibliographic
    "et al", "cf", "e.g", "i.e", "vs", "viz", "ibid", "resp",
    # structural references
    "fig", "figs", "eq", "eqs", "ref", "refs", "sec", "ch", "tab", "suppl",
    "no", "vol", "pp", "p",
    # units and measures
    "approx", "ca", "min", "max", "sd", "sem", "ms", "sec", "hr", "mm", "cm",
    "ml", "mg", "kg", "mol", "temp",
    # titles
    "dr", "prof", "mr", "mrs", "ms", "st",
}

# A boundary is a terminator, then space, then something that can start a
# sentence. Excluded before the terminator: an abbreviation, a single capital
# (an initial), or a digit (a decimal, or "Study 1.").
_BOUNDARY_RE = re.compile(
    r"""(?<=[.!?])          # a terminator
        ["')\]]?            # optionally closed by a quote or bracket
        \s+                 # whitespace
        (?=               # followed by a plausible sentence opening:
            [A-Z(\[]        #   capital, or an opening bracket
            | [“"']    #   or an opening quote
        )
    """,
    re.VERBOSE,
)

_ENDS_ABBREV_RE = re.compile(
    r"(?:^|[\s(\[])(" + "|".join(sorted(_ABBREV, key=len, reverse=True)) + r")\.$",
    re.IGNORECASE,
)
_ENDS_INITIAL_RE = re.compile(r"(?:^|\s)[A-Z]\.$")
_ENDS_NUMBER_RE = re.compile(r"\d\.$")


def split_sentences(text: str) -> list[str]:
    """Split scientific prose into sentences, tolerating domain abbreviations."""
    if not text or not text.strip():
        return []
    text = re.sub(r"\s+", " ", text).strip()
    out: list[str] = []
    buf = ""
    for piece in _BOUNDARY_RE.split(text):
        candidate = (buf + " " + piece).strip() if buf else piece.strip()
        # If the accumulated text ends on an abbreviation, an initial, or a
        # decimal, the boundary was spurious — keep accumulating.
        tail = candidate
        if (_ENDS_ABBREV_RE.search(tail) or _ENDS_INITIAL_RE.search(tail)
                or _ENDS_NUMBER_RE.search(tail)):
            buf = candidate
            continue
        out.append(candidate)
        buf = ""
    if buf:
        out.append(buf.strip())
    return [s for s in out if s]


_MD_NOISE_RE = re.compile(r"[*_`]|\\(?=[<>~^&%$#\[\]])")
_SUPSUB_RE = re.compile(r"\^([^^\s]{1,4})\^|~([^~\s]{1,4})~")


def plain(text: str) -> str:
    """Strip Markdown emphasis and escapes for feature detection.

    Pandoc renders a statistic as `*t*(1180) = 3.52` and an exponent as
    `*R*^2^`; a pattern written for plain prose matches neither. Detection runs
    on this flattened form while marks are anchored to the original text, so
    the document is never rewritten — only read differently.
    """
    text = _SUPSUB_RE.sub(lambda m: m.group(1) or m.group(2) or "", text)
    return _MD_NOISE_RE.sub("", text)


# ── Span features ─────────────────────────────────────────────────────

# A reported statistic: a named quantity with a value. Broad on purpose — this
# is a feature of a span, not the denominator, so a false positive costs a
# label rather than a phantom obligation.
STAT_RE = re.compile(
    r"""(?<![A-Za-z])
    (?: p | t | F | Z | z | r | R\^?2 | rho | ρ | d | BF\s*_?1?0? | β | beta
      | χ2 | chi2 | HDI | CI | AIC | BIC | loo | n | N | df )
    \s*(?:\([^)]{0,12}\))?\s*
    [=<>≤≥]\s*
    [-−–]?\d*\.?\d+(?:\s*[eE]\s*[-−–]?\s*\d+)?
    """,
    re.VERBOSE,
)

# Panel references, resolved to the same ids `prepare` builds the inventory from
# ("fig2c", "fig3s1", "table1", "tableapp1-4"). Getting this right is the whole
# job: a reference the reader cannot resolve is a panel nothing can account for,
# and it shows up as a coverage gap that is really a parsing gap.
#
# Five shapes occur in this corpus, and the earlier single regex mishandled all
# but the first:
#
#   Figure 2C                     one panel
#   Figure 3A, B, E, F            a list — four panels, not one blob
#   Figure 2C-F                   a range — four panels
#   Appendix 1—table 4            one id ("tableapp1-4"), not "Appendix 1" + "table 4"
#   ( A, E )                      bare letters in a caption, meaning the figure being captioned
#
# The list form is also where the old pattern broke worst: `[A-Za-z]` let it run
# on past the reference into the statistic that followed, so "Figure 2C , t (39)
# = 2.27" parsed as the panel "Figure 2C , t". Panel letters are single and
# upper-case; requiring that is what stops the bleed.

_FIG_ANCHOR_RE = re.compile(
    r"\b(?P<kind>Fig(?:ure)?s?|Tables?|Appendix)\.?\s*"
    r"(?P<num>\d+)"
    r"(?P<supp>\s*[-–—]?\s*(?:figure\s+)?supplement\s*\d+)?"
    r"(?P<apptab>\s*[-–—]\s*table\s*\d+)?"
    r"(?P<letters>(?:\s*[A-H](?:\s*[,&]\s*|\s*[-–—]\s*|\s+and\s+))*\s*[A-H])?"
    r"(?![A-Za-z])",
    re.IGNORECASE,
)

# A bare "( A, E )" or "( A–D )" — panel letters with no figure named, which is how
# a figure caption refers to its own panels.
_BARE_LETTERS_RE = re.compile(r"\(\s*([A-H](?:\s*[,&-–—]\s*|\s+and\s+|\s*)){0,7}[A-H]\s*\)")
_LETTER_RE = re.compile(r"[A-H]")


def _expand_letters(chunk: str) -> list[str]:
    """Turn "A, B, E, F" or "C-F" into individual lower-case panel letters."""
    if not chunk:
        return []
    letters = _LETTER_RE.findall(chunk.upper())
    if not letters:
        return []
    # A range is written with a dash between exactly two letters: C-F -> C,D,E,F.
    if re.search(r"[A-H]\s*[-–—]\s*[A-H]", chunk.upper()) and len(letters) == 2:
        a, b = ord(letters[0]), ord(letters[1])
        if b > a:
            return [chr(c).lower() for c in range(a, b + 1)]
    return [c.lower() for c in letters]


def panel_refs(text: str, current_figure: str | None = None) -> list[str]:
    """Every panel id a piece of text refers to, in inventory form.

    `current_figure` is the figure a caption is captioning ("fig3"), which is
    what lets "( A, E )" resolve. Without it those bare letters are ambiguous
    and are left alone rather than guessed at.
    """
    out: list[str] = []

    def add(pid: str) -> None:
        if pid not in out:
            out.append(pid)

    for m in _FIG_ANCHOR_RE.finditer(text):
        kind = m.group("kind").lower()
        num = m.group("num")
        base = "table" if kind.startswith("table") else (
            "app" if kind.startswith("appendix") else "fig")

        if base == "app":
            # "Appendix 1—table 4" is one id; a bare "Appendix 1" names no panel.
            # The id is the document's own — eLife's JATS calls this `app1table4`.
            if m.group("apptab"):
                n = re.search(r"\d+", m.group("apptab")).group(0)
                add(f"app{num}table{n}")
            continue

        if m.group("supp"):
            n = re.search(r"\d+", m.group("supp")).group(0)
            add(f"{base}{num}s{n}")
            continue

        letters = _expand_letters(m.group("letters") or "")
        if letters:
            for L in letters:
                add(f"{base}{num}{L}")
        else:
            add(f"{base}{num}")

    # The key resources table has a name rather than a number, and JATS calls it
    # `keyresource`. Nothing else in the reference grammar reaches it.
    if re.search(r"\bkey\s+resources?\s+table\b", text, re.I):
        add("keyresource")

    if current_figure:
        for m in _BARE_LETTERS_RE.finditer(text):
            for L in _expand_letters(m.group(0)):
                add(f"{current_figure}{L}")
    return out


# Kept for callers that want the raw spans rather than resolved ids.
PANEL_REF_RE = _FIG_ANCHOR_RE

CITATION_RE = re.compile(r"\([A-Z][A-Za-z’'\-]+(?:\s+et\s+al\.?)?,?\s*\d{4}[a-z]?\)")

COORD_RE = re.compile(r"\[\s*[-−–]?\d+\s*,\s*[-−–]?\d+\s*,\s*[-−–]?\d+\s*\]")


def span_sha(text: str) -> str:
    """A content fingerprint for a span: the first 8 hex of sha256 over its
    normalised text.

    Span ids are positional (`results-026`), which makes them readable and
    useless as identity: insert one sentence earlier in the section and every
    id after it shifts, silently. Anything that stores a judgement about a span
    — an adjudicated coverage verdict, a claim assignment — must be able to
    tell that the sentence it judged is still the sentence it is looking at.
    The id says where to look; the fingerprint says whether it is the same text.

    JATS cannot help here. It gives ids to sections (43 in this paper) and to
    figures and tables, but to none of its 225 paragraphs, and it has no
    sentence element at all. Below section level there is nothing to inherit.
    """
    import hashlib
    return hashlib.sha256(re.sub(r"\s+", " ", text).strip().encode("utf-8")).hexdigest()[:8]


@dataclass
class Span:
    """One span of the paper's text that must be accounted for."""

    uid: str
    section: str
    index: int
    text: str
    stats: list[str] = field(default_factory=list)
    panels: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
    coords: list[str] = field(default_factory=list)

    @property
    def sha(self) -> str:
        """Content fingerprint — see `span_sha`."""
        return span_sha(self.text)

    @property
    def has_result(self) -> bool:
        """Carries a number that a claim would have to account for."""
        return bool(self.stats or self.coords)

    @property
    def kind(self) -> str:
        """Coarse label, for reporting only — never used to skip a span."""
        if self.stats or self.coords:
            return "statistical"
        if self.panels:
            return "panel"
        if self.citations:
            return "citational"
        return "textual"


def _features(text: str, current_figure: str | None = None) -> dict:
    text = plain(text)
    return {
        "stats": [m.group(0).strip() for m in STAT_RE.finditer(text)],
        "panels": panel_refs(text, current_figure),
        "citations": [m.group(0).strip() for m in CITATION_RE.finditer(text)],
        "coords": [m.group(0).strip() for m in COORD_RE.finditer(text)],
    }


_CAPTION_START_RE = re.compile(r"^\s*(Figure|Table)\s*(\d+)"
                               r"(?:\s*[-–—]?\s*(?:figure\s+)?supplement\s*(\d+))?",
                               re.IGNORECASE)


def _figure_context(sentence: str, current: str | None) -> str | None:
    """Track which figure a caption is captioning.

    A caption opens with "Figure 3." and its following sentences then refer to
    "( A, E )" with no figure named. Those bare letters are the densest panel
    references in the paper and resolving them needs this state — without it,
    every panel mentioned only inside its own caption is invisible.
    """
    m = _CAPTION_START_RE.match(sentence)
    if not m:
        return current
    base = "table" if m.group(1).lower() == "table" else "fig"
    return f"{base}{m.group(2)}" + (f"s{m.group(3)}" if m.group(3) else "")


def segment(paper: PreparedPaper, *, include_methods: bool = True) -> list[Span]:
    """Cut the whole paper into spans.

    Sections are kept distinct so a downstream pass can weight them — a
    methods sentence and a results sentence carry different obligations — but
    nothing is dropped here. Deciding what need not be claimed is a policy
    question, and policy does not belong in the measurement.
    """
    sections: list[tuple[str, str]] = [
        ("abstract", paper.abstract),
        ("results", paper.results_text),
        ("captions", paper.captions_text),
        ("tables", paper.tables_text),
    ]
    if include_methods:
        sections += [("methods", paper.methods_text),
                     ("appendix", paper.appendix_text)]

    spans: list[Span] = []
    for section, text in sections:
        if not text or not text.strip():
            continue
        current_figure: str | None = None
        for i, sent in enumerate(split_sentences(text), 1):
            current_figure = _figure_context(sent, current_figure)
            spans.append(Span(uid=f"{section}-{i:03d}", section=section,
                              index=i, text=sent,
                              **_features(sent, current_figure)))
    return spans


def summarise(spans: list[Span]) -> str:
    """A short report of what the segmentation found."""
    from collections import Counter
    by_section = Counter(u.section for u in spans)
    by_kind = Counter(u.kind for u in spans)
    n_stats = sum(len(u.stats) for u in spans)
    L = [f"Segmentation — {len(spans)} spans",
         "  by section: " + ", ".join(f"{k}={v}" for k, v in by_section.items()),
         "  by kind   : " + ", ".join(f"{k}={v}" for k, v in by_kind.items()),
         f"  spans carrying a result: {sum(1 for u in spans if u.has_result)}",
         f"  statistic mentions     : {n_stats}"]
    return "\n".join(L)
