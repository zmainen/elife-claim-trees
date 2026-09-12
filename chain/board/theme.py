"""Board theme: the palettes, the plain-word maps, the stylesheet, and the small pure
helpers (escaping, chips, tags, dates, anchors) that the renderer builds pages from."""

from __future__ import annotations

import html
from datetime import datetime

from .. import claims as C


TONE = {"current": "#2f855a", "stale": "#b7791f", "blocked": "#c05621",
        "pending": "#2b6cb0", "absent": "#a0aec0"}
TYPE_TONE = {"question": "#805ad5", "scope": "#718096", "hypothesis": "#3182ce",
             "prediction": "#4299e1", "method": "#38a169", "result": "#dd6b20",
             "interpretation": "#d69e2e", "assessment": "#e53e3e", "decision": "#c53030",
             "step": "#4a5568"}
# One tone per kind of player, for the loop and the cards.
ROLE_TONE = {"team": "#3182ce", "funder": "#805ad5", "journal": "#c05621",
             "library": "#2f855a", "process": "#4a5568"}
ROLE_WASH = {"team": "#ebf3fb", "funder": "#f0ebfa", "journal": "#fbeee6",
             "library": "#e9f5ee", "process": "#edf0f4"}

# ── plain words for a system with none of its own ───────────────────────────
STATE_WORD = {"current": "up to date", "stale": "out of date", "blocked": "waiting",
              "pending": "open", "absent": "not started"}
STATE_MEANING = {
    "current": "Answered, every input still as it was, and everything it depends on is current.",
    "stale": "An input changed after this was answered, so it may no longer be right.",
    "blocked": "Answered and unchanged, but something it depends on is no longer current.",
    "pending": "A request is open and waiting to be answered.",
    "absent": "Never answered."}

# Real step ids of the scientopia process, in plain words.
STEP_NAME = {"import": "Import the corpus", "catalogue": "Catalogue the library",
             "question": "Ask the question", "hypotheses": "Propose hypotheses",
             "design": "Design the study", "proposal": "Compose the proposal",
             "award": "Record the award", "study": "Run the study", "paper": "Compose the paper",
             "call": "Issue the call", "select": "Select proposals to fund",
             "submissions": "Collect submissions", "review": "Review the papers",
             "decision": "Decide what to publish", "published": "Publish",
             "scheme": "Review the process itself"}
STEP_SHORT = {"import": "Import", "catalogue": "Catalogue", "question": "Question",
              "hypotheses": "Hypotheses", "design": "Design", "proposal": "Proposal",
              "award": "Award", "study": "Study", "paper": "Paper", "call": "Call",
              "select": "Selection", "submissions": "Submissions", "review": "Review",
              "decision": "Decision", "published": "Publications", "scheme": "Scheme"}
NOUN = {"import": "the imported corpus", "catalogue": "the catalogue", "question": "the question",
        "hypotheses": "the hypotheses", "design": "the design", "proposal": "the proposal",
        "award": "the award", "study": "the study", "paper": "the paper", "call": "the call",
        "select": "the funding decision", "submissions": "the submissions",
        "review": "the review", "decision": "the editorial decision",
        "published": "the published record", "scheme": "the ruling on the process"}
TITLE = {"import": "Imported corpus", "catalogue": "Library catalogue", "question": "The question",
         "hypotheses": "Hypotheses", "design": "Study design", "proposal": "Proposal",
         "award": "Award", "study": "Study results", "paper": "The paper", "call": "Funding call",
         "select": "Funding decision", "submissions": "Submissions", "review": "Peer review",
         "decision": "Editorial decision", "published": "Published record",
         "scheme": "Ruling on the process"}
# The short label a judgement carries when shown beside a claim.
JUDGE = {"select": "Funder", "review": "Reviewer", "decision": "Editor", "scheme": "Process"}
# A set reference, in words.
SET_PHRASE = {"journal:*:published": "every journal's publications",
              "funder:*:select": "every funder's decision", "team:*:paper": "every team's paper",
              "team:*:proposal": "every team's proposal", "team:*:question": "every team's question",
              "team:*:hypotheses": "every team's hypotheses", "team:*:design": "every team's design",
              "team:*:study": "every team's study"}
GROUPS = [("team", "Research teams"), ("funder", "Funders"),
          ("journal", "Journals"), ("library", "The library")]


def esc(s) -> str:
    return html.escape(str(s if s is not None else ""))


def step_name(step) -> str:
    sid = step if isinstance(step, str) else step.id
    return STEP_NAME.get(sid) or (step.question if hasattr(step, "question") else sid) or sid


def noun(step_id: str) -> str:
    return NOUN.get(step_id, f"the {step_id}")


def title(step_id: str) -> str:
    return TITLE.get(step_id, step_id)


def chip(state: str, text: str | None = None) -> str:
    return (f'<span class="chip" style="--c:{TONE.get(state, "#718096")}">'
            f'{esc(text if text is not None else STATE_WORD.get(state, state))}</span>')


def tag(t: str) -> str:
    return f'<span class="tag" style="background:{TYPE_TONE.get(t, "#718096")}">{esc(t)}</span>'


# ── dates ───────────────────────────────────────────────────────────────────
def _dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def short_date(s: str) -> str:
    d = _dt(s)
    return f"{d.day} {d:%b}, {d:%H:%M}"


def long_date(s: str) -> str:
    d = _dt(s)
    return f"{d.day} {d:%b} at {d:%H:%M}"


# ── anchors and links ───────────────────────────────────────────────────────
def _slug(s: str) -> str:
    return s.replace(":", "-").replace("/", "-").replace(".", "-")


def art_id(sid: str, step_id: str, v: int) -> str:
    return f"art-{_slug(sid)}-{_slug(step_id)}-v{v}"


def claim_id(gid: str) -> str:
    return "claim-" + _slug(gid)


def player_anchor(sid: str) -> str:
    return "player-" + _slug(sid)


def step_anchor(step_id: str) -> str:
    return "step-" + _slug(step_id)


CSS = """
:root{--ink:#1a202c;--ink2:#3b3748;--muted:#6b7280;--line:#e2e8f0;--line2:#cbd5e0;--bg:#f7f6f3;--card:#fff;--wash:#f0eef2;--accent:#2b6cb0}
*{box-sizing:border-box}
body{font:15px/1.6 -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);margin:0}
main{max-width:1100px;margin:0 auto;padding:0 1.25rem 5rem}
.mono,code,.eyebrow,.sec-note,.meta,.role,.block .lbl,.linkrow .lbl{font-family:ui-monospace,Menlo,Consolas,monospace}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:600;font-size:2.5rem;line-height:1.08;letter-spacing:-.01em;margin:0 0 .5rem}
h2{font-family:Georgia,serif;font-weight:600;font-size:1.6rem;margin:0 0 .2rem;letter-spacing:-.01em;scroll-margin-top:3.4rem}
h3{font-size:1.05rem;margin:1.5rem 0 .5rem}
h4{font-size:.9rem;margin:1rem 0 .3rem;color:#2d3748}
p{max-width:74ch}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.muted{color:var(--muted)}.small{font-size:.86rem}
code{font-size:.82em;background:var(--wash);border:1px solid var(--line);border-radius:3px;padding:.05em .35em}
section{margin:0 0 3.4rem}
.eyebrow,.sec-note{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.eyebrow{margin:0 0 1.1rem}.sec-note{margin:.1rem 0 1.2rem}
/* masthead */
.mast{padding:3rem 0 2rem;border-bottom:1px solid var(--line);margin-bottom:2.4rem}
.standfirst{font-family:Georgia,serif;font-size:1.18rem;line-height:1.5;color:var(--ink2);max-width:64ch;margin:0 0 1rem}
.mast .note{font-size:.92rem;color:var(--muted);max-width:64ch;margin:0 0 1.3rem}
.meta{display:flex;flex-wrap:wrap;gap:.4rem 1.6rem;font-size:.75rem;color:var(--muted)}
.meta b{color:var(--ink2);font-weight:600}
nav{position:sticky;top:0;z-index:5;background:rgba(247,246,243,.94);backdrop-filter:blur(6px);border-bottom:1px solid var(--line);margin:0 -1.25rem 2rem;padding:.5rem 1.25rem}
nav a{display:inline-block;margin:.1rem .9rem .1rem 0;font-size:.83rem}
/* chips + tags */
.chip{display:inline-block;padding:.05em .62em;border-radius:1em;color:#fff;background:var(--c,#718096);font-size:.72rem;font-weight:600;line-height:1.7;vertical-align:middle;white-space:nowrap}
.chip.ghost{background:transparent;color:var(--c);border:1px solid var(--c)}
.tag{display:inline-block;padding:0 .45em;border-radius:3px;color:#fff;font-size:.64rem;text-transform:uppercase;letter-spacing:.05em;line-height:1.8;vertical-align:middle}
.pill{display:inline-block;background:var(--wash);border-radius:4px;padding:0 .4em;font-size:.72rem;color:var(--ink2);margin-right:.3rem}
/* loop */
.loopwrap{margin:1rem 0 1.4rem}
.loop{width:100%;max-width:760px;height:auto;display:block;margin:0 auto}
.loop text{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif}
.loop a{cursor:pointer}.loop a:hover .node{stroke-width:2.4}
.legend{display:flex;flex-wrap:wrap;gap:.5rem 1.4rem;margin:.7rem 0}
.legend .it{font-size:.85rem;max-width:36ch}
/* cards (players + artifacts) */
.pcard,.card{background:var(--card);border:1px solid var(--line);border-left:5px solid var(--rail,var(--line2));border-radius:8px;scroll-margin-top:3.4rem}
.pcard{padding:1rem 1.2rem;margin:1.1rem 0}.card{padding:.9rem 1.1rem;margin:1rem 0}
.pcard .hd,.card>.hd{display:flex;flex-wrap:wrap;align-items:baseline;gap:.5rem .7rem;margin-bottom:.2rem}
.pcard .hd .nm{font-size:1.2rem;font-weight:600}
.role,.block .lbl,.linkrow .lbl{font-size:.7rem;text-transform:uppercase;letter-spacing:.09em;color:var(--muted)}
.persona{color:var(--ink2);margin:.35rem 0 .2rem}
.block{margin:.8rem 0 .2rem}.block .lbl{margin-bottom:.35rem}
.record{font-size:.94rem}.record .line{padding:.15rem 0}
.strip{display:flex;flex-wrap:wrap;gap:.35rem;margin:.3rem 0 .5rem}
.stepcell{border:1px solid var(--line);border-radius:6px;padding:.3rem .5rem;background:var(--bg);min-width:6rem;font-size:.78rem}
.stepcell .s{display:block;color:var(--muted);margin-bottom:.2rem;font-size:.72rem}
.notes .n{font-size:.9rem;color:var(--ink2);margin:.2rem 0}
.linkrow{margin-top:.7rem;padding-top:.55rem;border-top:1px dashed var(--line2);display:flex;flex-wrap:wrap;gap:.3rem .9rem;font-size:.82rem;align-items:baseline}
.pgroup{margin:1.8rem 0 0}.pgroup>h3{border-bottom:1px solid var(--line2);padding-bottom:.3rem}
.card>.hd .t{font-size:1.05rem;font-weight:600}
.prov{color:var(--ink2);font-size:.9rem;margin:.25rem 0}
.stat{font-size:.9rem;margin:.2rem 0 .5rem;font-weight:500}
.claim{border-top:1px solid var(--line);padding:.55rem 0}.claim:first-of-type{border-top:none}
.claim .txt{margin:.1rem 0}.claim .id{font-size:.72rem;color:var(--muted)}
.edges{font-size:.82rem;color:var(--ink2);margin-top:.15rem}
.revs{margin:.35rem 0 .1rem .9rem;padding-left:.7rem;border-left:2px solid var(--wash)}
.rev{font-size:.85rem;color:var(--ink2);padding:.05rem 0}
.report .line{border-top:1px solid var(--line);padding:.45rem 0;display:flex;gap:.6rem;align-items:baseline;flex-wrap:wrap}
.report .line .rz{color:var(--ink2);font-size:.9rem}
.decision{background:var(--wash);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:5px;padding:.5rem .7rem;margin:.3rem 0 .6rem}
.sec-claim{border-top:1px solid var(--wash);padding:.45rem 0}
details{margin:.5rem 0}summary{cursor:pointer;color:var(--accent);font-size:.9rem}
pre{background:#f1f2f4;padding:.7rem;border-radius:5px;overflow-x:auto;font-size:.8rem;white-space:pre-wrap;line-height:1.5}
.wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;font-size:.85rem}
th,td{text-align:left;vertical-align:top;padding:.4rem .55rem;border-bottom:1px solid var(--wash)}
th{font-weight:600;color:var(--ink2);font-size:.7rem;text-transform:uppercase;letter-spacing:.04em}
"""


def _join(items: list[str]) -> str:
    items = [i for i in items if i]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def _abs(sid: str, step_id: str, ref: str) -> str:
    return ref if ":" in ref else C.gid(sid, step_id, ref)
