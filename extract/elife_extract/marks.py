"""Claim assignments as marks in the document itself.

A coverage verdict has to live somewhere. It lived in a sidecar keyed on span
ids like `results-026`, which is a position, so a sentence inserted earlier in
the section silently reattached every verdict after it to different text. A
fingerprint made that failure loud, but a fingerprint is a check, not an
identity: fix a typo in the paper and the hash changes, the span looks new, and
its assignment is lost even though it is obviously the same claim about the same
result.

The identity that survives both is the one tika already implements. A tika mark
anchors to a *quoted span* and relocates the quote when the text moves, so an
assignment written as a mark survives edits that a position or a hash cannot:

    ⟦^zach: @{the pattern was consistent with the Yu & Koban signature} <uuid>⟧

The payload is the claim's UUID, not its slug. A slug is derived from the claim's
text, so rewording a claim changes it, and a mark carrying one rots silently. All
341 claims in this corpus already carry a UUID, and `export_mira.py` already uses
it as the node identity, so the mark, the claim file and the MIRA node then name
the same thing.

Every span that carries a result gets a mark saying what became of it:

    assigned        ⟦^author: @{quote} <claim-uuid>⟧
    no assertion    ⟦^author: @{quote} no-assertion⟧
    unclaimed       ⟦^author: @{quote} gap⟧

An unmarked sentence therefore means one thing only: it carries no result and was
never an obligation.

The first version recorded a gap by *absence*, which read well as a principle and
failed on the page. 152 of this paper's 245 spans are ordinary prose, so absence
was dominated by sentences that were never obligations, and a bare line could mean
either "no claim accounts for this result" or "there is no result here" — the
distinction the whole exercise exists to draw. Rendering it is what showed this;
the argument for absence had sounded fine.
"""

from __future__ import annotations

import logging
import re

from .prepare import PreparedPaper
from .segment import segment

logger = logging.getLogger(__name__)

NO_ASSERTION = "no-assertion"
GAP = "gap"

# tika SPEC § 3: ⟦<sign><author>: <payload>⟧, and for an anchored kind the
# payload opens with @{the quoted span}. The `^` sign is the claim assignment.
MARK_RE = re.compile(r"⟦\^([A-Za-z0-9_.-]+):\s*@\{(.*?)\}\s*(\S+)⟧", re.DOTALL)

_SECTION_ORDER = ("abstract", "results", "captions", "tables")


def _quote_for(text: str, limit: int = 120) -> str:
    """The anchor quote: the span, trimmed, with the brace delimiter kept safe."""
    q = re.sub(r"\s+", " ", text).strip()
    if len(q) > limit:
        q = q[: limit - 1] + "…"
    # A literal } would close the anchor early. Nothing in this corpus needs one.
    return q.replace("}", ")")


def render_marked(paper: PreparedPaper, assignments: dict[str, str],
                  *, author: str = "zach", include_methods: bool = False) -> str:
    """Render the paper's text with a claim mark on every assigned span.

    `assignments` maps span uid -> payload (a claim UUID, or NO_ASSERTION).
    Spans with no entry are left bare, which is how a gap is recorded.

    The text is rebuilt from the same slices the segmenter reads, so a mark's
    anchor is exactly the span it was computed for — marking a separately
    produced Markdown file would let the two drift apart.
    """
    spans = segment(paper, include_methods=include_methods)
    out: list[str] = [f"# {paper.title}", "",
                      f"<!-- {paper.paper_slug} · claim assignments as tika ^ marks · "
                      f"payload is the claim UUID; `{NO_ASSERTION}` means the span states "
                      f"no result; an unmarked result sentence is a gap -->", ""]
    current = None
    for s in spans:
        if s.section != current:
            current = s.section
            out += ["", f"## {current}", ""]
        payload = assignments.get(s.uid)
        line = s.text
        if payload:
            line = f"{line}⟦^{author}: @{{{_quote_for(s.text)}}} {payload}⟧"
        out.append(line)
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def read_marks(text: str) -> list[dict]:
    """Every claim mark in a marked document, in order."""
    return [{"author": m.group(1), "quote": m.group(2).strip(), "payload": m.group(3)}
            for m in MARK_RE.finditer(text)]


def assignments_from_marked(text: str, paper: PreparedPaper,
                            *, include_methods: bool = False) -> dict[str, str]:
    """Recover span -> payload from a marked document.

    Resolution is by quote *in document order*, not by a quote lookup. Quotes
    are not unique: this paper has 401 spans but only 325 distinct sentences,
    because caption text is repeated in the results. A quote->span dictionary
    silently collapses those 70 duplicates, and the first attempt at this lost
    six assignments that way — it wrote 79 marks and read back 73.

    So a mark's quote establishes *what* it is anchored to and its position
    establishes *which* occurrence. Reading forward from a cursor gives both,
    and tolerates the text around a mark moving, which is the property a
    positional id lacked and a content hash cannot provide.
    """
    spans = segment(paper, include_methods=include_methods)
    quotes = [_quote_for(s.text) for s in spans]
    found: dict[str, str] = {}
    unresolved: list[str] = []
    cursor = 0
    for mk in read_marks(text):
        q = mk["quote"]
        try:                                   # the next occurrence at or after the cursor
            i = quotes.index(q, cursor)
        except ValueError:
            try:                               # the text moved: fall back to any occurrence
                i = quotes.index(q)
            except ValueError:
                unresolved.append(q)
                continue
        found[spans[i].uid] = mk["payload"]
        cursor = i + 1
    if unresolved:
        logger.warning("%d mark(s) whose anchor matches no span — the text moved past what "
                       "the quote can relocate; first: %r", len(unresolved), unresolved[0][:70])
    return found
