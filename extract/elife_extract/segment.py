"""Segmentation — cut the paper into units that must each be accounted for.

This is the base pass. Everything else measures itself against it.

The problem it replaces: coverage was computed by finding statistics with a
regex and checking whether their exact text appeared in some claim. That fails
constantly and in both directions. A paper reporting `p = 0.0004` and a claim
saying "p < 0.001" is the same result stated two ways, and scores as a miss. A
claim that states an effect without restating its number scores as a miss. A
statistic the regex does not match is invisible on both sides, so it cannot
even be missed.

The fix is to stop inventing the denominator and take it from the document. Cut
the text into units, mechanically and exhaustively; every unit is then either
accounted for by some claim or it is not, and "not" is a fact about the text
rather than about a pattern.

Units are sentences, because a sentence is the smallest span that reliably
carries one assertion in scientific prose, and because sentence boundaries can
be found without a model. Splitting scientific prose is not naive, though:
"Fig. 2", "et al.", "e.g.", "p = 0.03.", "0.5 mm", and author initials all put
a period where no sentence ends. Those cases are enumerated below rather than
hidden in a general-purpose splitter, so a failure is visible and fixable.

Each unit carries features — the statistics in it, the panels it names, whether
it cites — which downstream passes use for routing and reporting. The features
are *derived from* the unit; the unit is never derived from the features.
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


# ── Unit features ─────────────────────────────────────────────────────

# A reported statistic: a named quantity with a value. Broad on purpose — this
# is a feature of a unit, not the denominator, so a false positive costs a
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

PANEL_REF_RE = re.compile(
    r"\b(?:Fig(?:ure)?s?|Table|Appendix)\.?\s*"
    r"\d+[A-Za-z]?(?:\s*[-–—]\s*(?:figure\s+)?supplement\s*\d+)?"
    r"(?:\s*[,–—-]\s*[A-Za-z]\b)*",
    re.IGNORECASE,
)

CITATION_RE = re.compile(r"\([A-Z][A-Za-z’'\-]+(?:\s+et\s+al\.?)?,?\s*\d{4}[a-z]?\)")

COORD_RE = re.compile(r"\[\s*[-−–]?\d+\s*,\s*[-−–]?\d+\s*,\s*[-−–]?\d+\s*\]")


@dataclass
class Unit:
    """One segment of the paper that must be accounted for."""

    uid: str
    section: str
    index: int
    text: str
    stats: list[str] = field(default_factory=list)
    panels: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
    coords: list[str] = field(default_factory=list)

    @property
    def has_result(self) -> bool:
        """Carries a number that a claim would have to account for."""
        return bool(self.stats or self.coords)

    @property
    def kind(self) -> str:
        """Coarse label, for reporting only — never used to skip a unit."""
        if self.stats or self.coords:
            return "statistical"
        if self.panels:
            return "panel"
        if self.citations:
            return "citational"
        return "textual"


def _features(text: str) -> dict:
    text = plain(text)
    return {
        "stats": [m.group(0).strip() for m in STAT_RE.finditer(text)],
        "panels": [m.group(0).strip() for m in PANEL_REF_RE.finditer(text)],
        "citations": [m.group(0).strip() for m in CITATION_RE.finditer(text)],
        "coords": [m.group(0).strip() for m in COORD_RE.finditer(text)],
    }


def segment(paper: PreparedPaper, *, include_methods: bool = True) -> list[Unit]:
    """Cut the whole paper into units.

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

    units: list[Unit] = []
    for section, text in sections:
        if not text or not text.strip():
            continue
        for i, sent in enumerate(split_sentences(text), 1):
            units.append(Unit(uid=f"{section}-{i:03d}", section=section,
                              index=i, text=sent, **_features(sent)))
    return units


def summarise(units: list[Unit]) -> str:
    """A short report of what the segmentation found."""
    from collections import Counter
    by_section = Counter(u.section for u in units)
    by_kind = Counter(u.kind for u in units)
    n_stats = sum(len(u.stats) for u in units)
    L = [f"Segmentation — {len(units)} units",
         "  by section: " + ", ".join(f"{k}={v}" for k, v in by_section.items()),
         "  by kind   : " + ", ".join(f"{k}={v}" for k, v in by_kind.items()),
         f"  units carrying a result: {sum(1 for u in units if u.has_result)}",
         f"  statistic mentions     : {n_stats}"]
    return "\n".join(L)
