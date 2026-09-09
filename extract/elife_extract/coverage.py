"""Coverage — is every assertion in the paper represented by a claim?

`evaluate` scores *agreement*: when the CLI and the curated corpus both name a
claim, do they agree about its panel and role. That says nothing about what
neither of them mentioned. You can score 100% agreement on a third of a paper.

This module supplies the missing denominator. It builds an inventory of the
paper's assertion sites directly from the source — every figure panel, every
table, every reported statistic — independently of what any model produced,
then reports what no claim accounts for.

The distinction that makes it useful: an *orphan* is not a disagreement, it is
a silence. Nothing in the pipeline previously reported silence, which is how
Figure 2's panels C and F — a failed replication of a risk-aversion effect —
sat unrepresented without anything registering their absence.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field

from .prepare import PreparedPaper

logger = logging.getLogger(__name__)


# ── Statistic detection ──────────────────────────────────────────────────
# Deliberately conservative: a reported statistic carries a value. Bare
# mentions of "a t-test" are prose, not results, and matching them would
# inflate the denominator with things no claim should have to cite.

STAT_PATTERNS = [
    # p = 0.03, p < .001, p = 3.1e-20
    ("p", re.compile(r"\bp\s*[=<>≤≥]\s*0?\.\d+(?:\s*[eE]\s*[-−]\s*\d+)?|"
                     r"\bp\s*[=<>≤≥]\s*\d+(?:\.\d+)?[eE][-−]\d+", re.I)),
    # t(39) = 2.27
    ("t", re.compile(r"\bt\s*\(\s*\d+(?:\.\d+)?\s*\)\s*[=]\s*[-−]?\d+\.?\d*", re.I)),
    # F(1,39) = 6.28
    ("F", re.compile(r"\bF\s*\(\s*\d+\s*,\s*\d+\s*\)\s*[=]\s*[-−]?\d+\.?\d*")),
    # Z = 2.85
    ("Z", re.compile(r"\bZ\s*[=]\s*[-−]?\d+\.?\d*")),
    # d = 0.36  (Cohen's d)
    ("d", re.compile(r"\bd\s*[=]\s*[-−]?\d+\.?\d*")),
    # r = 0.89, R2 = 0.185, rho = -0.058
    ("r", re.compile(r"\b(?:r|R2|R\^?2|rho|ρ|Rho)\s*[=]\s*[-−]?\d*\.?\d+", re.I)),
    # BF10 = 0.49
    ("BF", re.compile(r"\bBF\s*_?10\s*[=]\s*[-−]?\d*\.?\d+", re.I)),
    # beta = 0.33
    ("beta", re.compile(r"\b(?:β|beta)\s*[=]\s*[-−]?\d*\.?\d+", re.I)),
]

# MNI / stereotactic coordinates are assertions too — a peak location is a
# result, and this corpus verifies one of them against the deposited map.
COORD_RE = re.compile(r"\[\s*[-−]?\d+\s*,\s*[-−]?\d+\s*,\s*[-−]?\d+\s*\]")


def _norm(s: str) -> str:
    """Normalise a statistic for comparison: no spaces, ASCII minus, lowercase."""
    return re.sub(r"\s+", "", s).replace("−", "-").replace("–", "-").lower()


@dataclass(frozen=True)
class Statistic:
    kind: str
    text: str
    where: str          # which slice it was found in
    context: str = ""   # surrounding prose, for the orphan report

    @property
    def key(self) -> str:
        return _norm(self.text)


def extract_statistics(paper: PreparedPaper) -> list[Statistic]:
    """Every reported statistic in the paper, by slice."""
    slices = {
        "results": paper.results_text,
        "captions": paper.captions_text,
        "tables": paper.tables_text,
        "methods": paper.methods_text,
        "appendix": paper.appendix_text,
        "abstract": paper.abstract,
    }
    seen: set[str] = set()
    out: list[Statistic] = []
    for where, text in slices.items():
        if not text:
            continue
        for kind, rx in STAT_PATTERNS + [("coord", COORD_RE)]:
            for m in rx.finditer(text):
                stat = Statistic(
                    kind=kind,
                    text=m.group(0).strip(),
                    where=where,
                    context=re.sub(r"\s+", " ",
                                   text[max(0, m.start() - 90):m.end() + 40]).strip(),
                )
                if stat.key not in seen:
                    seen.add(stat.key)
                    out.append(stat)
    return out


# ── Coverage report ──────────────────────────────────────────────────────


@dataclass
class CoverageReport:
    paper_slug: str
    panels_total: list[str] = field(default_factory=list)
    panels_claimed: list[str] = field(default_factory=list)
    panels_orphan: list[str] = field(default_factory=list)
    panels_phantom: list[str] = field(default_factory=list)
    panels_figure_level: list[str] = field(default_factory=list)
    stats_total: list[Statistic] = field(default_factory=list)
    stats_orphan: list[Statistic] = field(default_factory=list)

    @property
    def panel_pct(self) -> float:
        n = len(self.panels_total)
        return 100.0 * (n - len(self.panels_orphan)) / n if n else 100.0

    @property
    def stat_pct(self) -> float:
        n = len(self.stats_total)
        return 100.0 * (n - len(self.stats_orphan)) / n if n else 100.0

    @property
    def complete(self) -> bool:
        return not self.panels_orphan and not self.stats_orphan


_PANEL_TOKEN_RE = re.compile(r"(?:fig(?:ure)?|table)\s*\.?\s*"
                             r"(?:s?\d+)(?:\s*[-–—]?\s*(?:figure\s*)?supplement\s*\d+)?"
                             r"\s*[a-z]?", re.I)


def _claim_panel_ids(panel_field: str | None) -> set[str]:
    """Normalise a claim's panel field into inventory-shaped ids.

    Deliberately the same resolver the paper side uses. Two normalisers meant
    two vocabularies: a claim saying "Figure 4E" and a paper saying "fig4e"
    only match if one function decides what both mean.
    """
    if not panel_field:
        return set()
    from .segment import panel_refs
    return set(panel_refs(str(panel_field)))


def _claim_panels(claim: dict):
    """Every panel a claim names, from both places the corpus stores them.

    The curated corpus keeps panels on the assertion — `assertions: [{panel: "fig4e, fig4f"}]`
    — while the CLI writes a top-level `panel`. Reading only the top level scored the whole
    curated corpus at 0/40 panels, which looked like a devastating finding and was a bug in
    the measurement. Same shape as the `belongings` relations the MIRA export used to miss:
    when a corpus stores one fact two ways, a reader that knows one way reports confident
    zeroes.
    """
    vals = []
    top = claim.get("panel")
    if top:
        vals.append(top)
    for a in (claim.get("assertions") or []):
        if isinstance(a, dict) and a.get("panel"):
            vals.append(a["panel"])
    ids = set()
    for v in vals:
        ids |= _claim_panel_ids(v)
    return ids


def assess(
    paper: PreparedPaper,
    claims: list[dict],
) -> CoverageReport:
    """Compare the paper's assertion inventory against a set of claims.

    `claims` are dicts with at least `panel` and `claim` (the claim sentence);
    both the draft table and parsed claim files can supply that shape.
    """
    rep = CoverageReport(paper_slug=paper.paper_slug)
    rep.panels_total = list(dict.fromkeys(paper.panel_ids))

    claimed: set[str] = set()
    for c in claims:
        claimed |= _claim_panels(c)
    rep.panels_claimed = sorted(claimed)

    inventory = set(rep.panels_total)
    rep.panels_orphan = [p for p in rep.panels_total if p not in claimed]

    # A claim may cite a whole figure ("fig3") where the paper has panels
    # ("fig3a".."fig3h"). That is not a phantom — the figure exists — but it
    # is imprecise, and it discharges none of its panels, so it stays in the
    # orphan list while being reported separately.
    prefixes = {re.match(r"((?:fig|table)[a-z]*\d+(?:s\d+)?)", p).group(1)
                for p in inventory if re.match(r"((?:fig|table)[a-z]*\d+(?:s\d+)?)", p)}
    rep.panels_figure_level = sorted(
        c for c in claimed if c not in inventory and c in prefixes)
    rep.panels_phantom = sorted(
        c for c in claimed if c not in inventory and c not in prefixes)

    rep.stats_total = extract_statistics(paper)
    blob = _norm(" ".join((c.get("claim") or "") for c in claims))
    rep.stats_orphan = [s for s in rep.stats_total if s.key not in blob]
    return rep


# ── Span-level coverage ──────────────────────────────────────────────────
# The section above takes its denominator from two inventories the paper
# publishes about itself: its figure panels and the statistics a regex can find.
# Both are useful and neither is exhaustive — a statistic the pattern misses is
# invisible on both sides, so it cannot even be counted as missed.
#
# This section takes the denominator from the text instead. `segment` cuts the
# whole paper into sentences, mechanically; every sentence is then either
# accounted for by some claim or it is not, and "not" is a fact about the paper
# rather than about a pattern.
#
# What counts as "accounted for" is deliberately narrow and mechanical: a claim
# states the same statistic, or names the same panel. Nothing here tries to
# judge whether a claim means the same thing as a sentence — that is the human's
# job, and a model that guessed would hide exactly the sentences worth looking
# at. So an unaccounted sentence is a *candidate* orphan, not a verdict.


@dataclass
class SpanCoverage:
    paper_slug: str
    spans: list = field(default_factory=list)          # every span, in order
    excluded: list = field(default_factory=list)       # adjudicated as asserting no result
    adjudicated: int = 0
    accounted: list = field(default_factory=list)      # (span, [slugs])
    orphans: list = field(default_factory=list)        # spans carrying a result, unmatched
    textual: list = field(default_factory=list)        # spans carrying no result at all

    @property
    def obligations(self) -> int:
        """Spans carrying something a claim could be expected to account for.

        Excludes spans adjudicated as asserting no result: a cross-reference is
        not an obligation, and counting it as one understates the corpus.
        """
        return len(self.accounted) + len(self.orphans)

    @property
    def pct(self) -> float:
        n = self.obligations
        return 100.0 * len(self.accounted) / n if n else 100.0


def _claim_index(claims: list[dict]) -> tuple[dict, dict]:
    """statistic → slugs, and panel-id → slugs, over the whole claim set."""
    from .segment import STAT_RE, plain
    by_stat: dict[str, list[str]] = {}
    by_panel: dict[str, list[str]] = {}
    for c in claims:
        slug = c.get("slug") or ""
        for m in STAT_RE.finditer(plain(c.get("claim") or "")):
            by_stat.setdefault(_norm(m.group(0)), []).append(slug)
        for pid in _claim_panels(c):
            by_panel.setdefault(pid, []).append(slug)
    return by_stat, by_panel


def assess_spans(paper: PreparedPaper, claims: list[dict],
                 *, include_methods: bool = False) -> SpanCoverage:
    """Cut the paper into sentences and ask which ones a claim accounts for.

    Methods are excluded by default: a methods sentence describes procedure, and
    the corpus does not claim procedure. Pass include_methods=True to see them
    counted — the measurement does not decide the policy, it just reports it.
    """
    from .segment import segment

    rep = SpanCoverage(paper_slug=paper.paper_slug)
    by_stat, by_panel = _claim_index(claims)
    rep.spans = segment(paper, include_methods=include_methods)

    for u in rep.spans:
        hits: list[str] = []
        for s in u.stats:
            for slug in by_stat.get(_norm(s), []):
                if slug not in hits:
                    hits.append(slug)
        for p in u.panels:
            for pid in _claim_panel_ids(p):
                for slug in by_panel.get(pid, []):
                    if slug not in hits:
                        hits.append(slug)
        if not (u.has_result or u.panels):
            rep.textual.append(u)
        elif hits:
            rep.accounted.append((u, hits))
        else:
            rep.orphans.append(u)
    return rep


VERDICTS = ("covered", "gap", "not-an-assertion")


def apply_mapping(rep: SpanCoverage, mapping: dict) -> SpanCoverage:
    """Fold adjudicated verdicts into a report.

    The mechanical match answers "does a claim restate this statistic or name
    this panel", which is a proxy for the question that matters and a poor one
    in both directions. Adjudication resolves the remainder into three states:

      covered           a claim does account for it; the matcher could not see
                        it, typically because the claim states the effect
                        without repeating its numbers
      gap               nothing in the tree accounts for it — a real hole
      not-an-assertion  the span states no result of its own: a cross-reference
                        ("see Appendix 1—table 4"), analysis narration, or a
                        bare panel label

    Keeping the three apart is the point. Lumping the third into the orphan
    list buries the real gaps in bookkeeping — in the Gädeke Results section,
    9 of 24 unmatched spans assert nothing, and reporting them as unmet
    obligations made the 10 that matter harder to see, not easier.

    A verdict is a judgement and is stored, not recomputed, so it can be
    audited, disagreed with, and re-used when the corpus changes.
    """
    # Accept either a bare array of verdicts or {"spans": [...]}, because both are
    # natural things for an adjudicator to hand back.
    rows = mapping.get("spans", []) if isinstance(mapping, dict) else mapping
    by_uid = {m["uid"]: m for m in rows if isinstance(m, dict) and m.get("uid")}
    still_orphan, covered_late, excluded = [], [], []
    for u in rep.orphans:
        v = by_uid.get(u.uid)
        if not v:
            still_orphan.append(u)
        elif v.get("verdict") == "covered":
            covered_late.append((u, [v["claim"]] if v.get("claim") else []))
        elif v.get("verdict") == "not-an-assertion":
            excluded.append((u, v.get("why", "")))
        else:
            still_orphan.append(u)
    rep.accounted = rep.accounted + covered_late
    rep.orphans = still_orphan
    rep.excluded = excluded
    rep.adjudicated = len(by_uid)
    return rep


def render_spans(rep: SpanCoverage, *, limit: int = 20) -> str:
    from collections import Counter
    by_section = Counter(u.section for u in rep.spans)
    L = [f"Span coverage — {rep.paper_slug}",
         f"  {len(rep.spans)} spans segmented from the paper "
         f"({', '.join(f'{k}={v}' for k, v in by_section.items())})",
         f"  {rep.obligations} carry a statistic or name a panel; "
         f"{len(rep.textual)} are prose that asserts no result",
         f"  accounted for by a claim: {len(rep.accounted)}/{rep.obligations} "
         f"({rep.pct:.0f}%)"]
    if rep.excluded:
        L.append(f"  adjudicated as asserting no result: {len(rep.excluded)} "
                 f"(cross-references, analysis narration, bare panel labels)")
    if rep.orphans:
        label = ("GAPS" if rep.adjudicated else "NOT ACCOUNTED FOR")
        L.append(f"\n  {label} ({len(rep.orphans)}) — each carries a result that no "
                 f"claim states:")
        for u in rep.orphans[:limit]:
            L.append(f"    [{u.uid}] {u.text[:110]}")
            if u.stats:
                L.append(f"           stats: {', '.join(u.stats[:6])}")
        if len(rep.orphans) > limit:
            L.append(f"    … and {len(rep.orphans) - limit} more")
    else:
        L.append("\n  every span carrying a result is accounted for")
    return "\n".join(L)


def render(rep: CoverageReport, *, limit: int = 12) -> str:
    """A human-readable orphan report."""
    L = [f"Coverage — {rep.paper_slug}",
         f"  panels     {len(rep.panels_total) - len(rep.panels_orphan)}/"
         f"{len(rep.panels_total)}  ({rep.panel_pct:.0f}%)",
         f"  statistics {len(rep.stats_total) - len(rep.stats_orphan)}/"
         f"{len(rep.stats_total)}  ({rep.stat_pct:.0f}%)"]
    if rep.panels_orphan:
        L.append(f"\n  UNCLAIMED PANELS ({len(rep.panels_orphan)}):")
        L.append("    " + ", ".join(rep.panels_orphan))
    if rep.panels_figure_level:
        L.append(f"\n  CITED AT FIGURE LEVEL, NOT PANEL ({len(rep.panels_figure_level)}):")
        L.append("    " + ", ".join(rep.panels_figure_level))
    if rep.panels_phantom:
        L.append(f"\n  CITED BUT NOT IN THE PAPER ({len(rep.panels_phantom)}):")
        L.append("    " + ", ".join(rep.panels_phantom))
    if rep.stats_orphan:
        L.append(f"\n  UNCLAIMED STATISTICS ({len(rep.stats_orphan)}):")
        for s in rep.stats_orphan[:limit]:
            L.append(f"    {s.text:<22} [{s.where}]  …{s.context[-72:]}")
        if len(rep.stats_orphan) > limit:
            L.append(f"    … and {len(rep.stats_orphan) - limit} more")
    if rep.complete:
        L.append("\n  complete — every panel and statistic is claimed")
    return "\n".join(L)
