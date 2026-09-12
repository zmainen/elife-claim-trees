"""The board: one static page that reads the store and the process and says, in plain English,
what this project is, what happened, and what every artifact holds. Generated entirely from the
store; nothing on it is typed by hand. No scripts and no external resources — the page is an
artifact like the rest and should open anywhere, fully readable with JavaScript disabled."""

from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

import yaml

from . import claims as C
from .process import Process
from .status import status
from .store import Store

# ── palettes (kept from the original board) ─────────────────────────────────
TONE = {"current": "#2f855a", "stale": "#b7791f", "blocked": "#c05621",
        "pending": "#2b6cb0", "absent": "#a0aec0"}
TYPE_ORDER = ("question", "scope", "hypothesis", "prediction", "method", "result",
              "interpretation", "assessment", "decision", "step")
TYPE_TONE = {"question": "#805ad5", "scope": "#718096", "hypothesis": "#3182ce",
             "prediction": "#4299e1", "method": "#38a169", "result": "#dd6b20",
             "interpretation": "#d69e2e", "assessment": "#e53e3e", "decision": "#c53030",
             "step": "#4a5568"}
WORKER_TONE = {"code": "#718096", "player": "#3182ce"}

# ── plain words for a system with none of its own ───────────────────────────
STATE_WORD = {"current": "up to date", "stale": "out of date", "blocked": "waiting",
              "pending": "open", "absent": "not started"}
STATE_MEANING = {
    "current": "Answered, every input still as it was, and everything it depends on is current.",
    "stale": "An input changed after this was answered, so it may no longer be right.",
    "blocked": "Answered and unchanged, but something it depends on is no longer current.",
    "pending": "A request is open and waiting for someone to answer it.",
    "absent": "Never answered."}
WORKER_WORD = {"code": "the referee (a script)", "player": "a player"}
# What each step asks, in plain words. Falls back to the step's own question.
STEP_NAME = {"question": "Ask the question", "hypotheses": "Propose hypotheses",
             "design": "Design the study", "proposal": "Compose the proposal",
             "proposal-review": "Review the proposal", "funding": "Decide funding",
             "study": "Run the study", "paper": "Compose the paper",
             "peer-review": "Peer review", "editorial": "Editorial decision",
             "publish": "Publish", "scheme": "Review the process itself"}
# The noun for an artifact of each step, as it reads in a sentence.
NOUN = {"question": "the question", "hypotheses": "the hypotheses", "design": "the design",
        "proposal": "the proposal", "proposal-review": "the proposal review",
        "funding": "the funding decision", "study": "the study results", "paper": "the paper",
        "peer-review": "the peer review", "editorial": "the editorial decision",
        "publish": "the published record", "scheme": "the ruling on the process"}
# The title on an artifact card.
TITLE = {"question": "The question", "hypotheses": "Hypotheses", "design": "The study design",
         "proposal": "The proposal", "proposal-review": "Proposal review",
         "funding": "Funding decision", "study": "Study results", "paper": "The paper",
         "peer-review": "Peer review", "editorial": "Editorial decision",
         "publish": "The published record", "scheme": "Ruling on the process"}
# The short label a judgement carries when shown beside a claim.
JUDGE = {"proposal-review": "Proposal review", "funding": "Funding", "peer-review": "Peer review",
         "editorial": "Editorial", "scheme": "Process ruling"}


def esc(s) -> str:
    return html.escape(str(s if s is not None else ""))


def step_name(step) -> str:
    return STEP_NAME.get(step.id) or step.question or step.id


def noun(step_id: str) -> str:
    return NOUN.get(step_id, f"the {step_id}")


def title(step_id: str) -> str:
    return TITLE.get(step_id, step_id)


def chip(state: str, text: str | None = None) -> str:
    return (f'<span class="chip" style="background:{TONE.get(state, "#718096")}">'
            f'{esc(text if text is not None else STATE_WORD.get(state, state))}</span>')


def tag(t: str) -> str:
    return f'<span class="tag" style="background:{TYPE_TONE.get(t, "#718096")}">{esc(t)}</span>'


def kind_of(x) -> str:
    """Who answers: the referee runs a command, or a player answers. Steps and records alike."""
    auto = x.automatic if hasattr(x, "automatic") else bool(x.get("automatic"))
    return "code" if auto else "player"


def who(worker: str) -> str:
    return (f'<span class="who"><span class="dot" style="background:{WORKER_TONE[worker]}"></span>'
            f'{esc(WORKER_WORD.get(worker, worker))}</span>')


# ── dates ───────────────────────────────────────────────────────────────────
def _dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def short_date(s: str) -> str:
    d = _dt(s)
    return f"{d.day} {d:%b}, {d:%H:%M}"


def long_date(s: str) -> str:
    d = _dt(s)
    return f"{d.day} {d:%b %Y} at {d:%H:%M}"


# ── anchors and links ───────────────────────────────────────────────────────
def _slug(s: str) -> str:
    return s.replace(":", "-").replace("/", "-").replace(".", "-")


def art_id(sid: str, step_id: str, v: int) -> str:
    return f"art-{_slug(sid)}-{_slug(step_id)}-v{v}"


def claim_id(gid: str) -> str:
    return "claim-" + _slug(gid)


def step_anchor(step_id: str) -> str:
    return "step-" + _slug(step_id)


class Refs:
    """Resolves a reference to a link and, for a claim, to its text and type — from the store."""

    def __init__(self, proc: Process, store: Store):
        self.proc, self.store = proc, store
        self.claims: dict[str, dict] = {}          # gid → claim, latest version wins
        for stype in proc.subjects:
            for sid in proc.subject_ids(stype):
                for step in proc.steps_for(stype):
                    for v in store.versions(sid, step.id):     # ascending: latest overwrites
                        cs = C.load(store.version_dir(sid, step.id, v)) or {}
                        for c in cs.get("claims") or []:
                            self.claims[C.gid(sid, step.id, c["id"])] = c

    def artifact_link(self, ref: str, label: str | None = None) -> str:
        sub, step = ref.split(":", 1)
        v = self.store.latest(sub, step)
        text = esc(label or title(step))
        return f'<a href="#{art_id(sub, step, v)}">{text}</a>' if v else text

    def link(self, ref: str, label: str | None = None) -> str:
        """A claim (`a:b:c`), an artifact (`a:b`), a step (`step:x`) or the process."""
        if ref == "process":
            return "the process"
        if ref.startswith("step:"):
            sid = ref.split(":", 1)[1]
            return f'<a href="#{step_anchor(sid)}">{esc(label or step_name(self.proc.steps[sid]))}</a>'
        if ref.count(":") >= 2:
            return f'<a href="#{claim_id(ref)}">{esc(label or ref.split(":")[-1])}</a>'
        return self.artifact_link(ref, label)

    def text_of(self, ref: str) -> str:
        c = self.claims.get(ref)
        return c.get("text", "") if c else ""

    def type_of(self, ref: str) -> str | None:
        c = self.claims.get(ref)
        return c.get("type") if c else None


# ── what every review or decision said about each claim ─────────────────────
def verdicts_by_claim(proc: Process, store: Store, st: dict) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for step in (proc.steps[s] for s in proc.order()):
        if not step.judges:
            continue
        for sid in proc.subject_ids(step.subject):
            v = store.latest(sid, step.id)
            if v is None:
                continue
            applies = st.get(sid, {}).get(step.id, {}).get("state") == "current"
            for c in (C.load(store.version_dir(sid, step.id, v)) or {}).get("claims") or []:
                if c.get("type") == "assessment" and c.get("about"):
                    out.setdefault(c["about"][0], []).append(
                        {"step": step.id, "verdict": c.get("verdict"), "text": c.get("text", ""),
                         "applies": applies})
    return out


def review_lines(gid: str, verdicts: dict) -> str:
    rows = []
    for d in verdicts.get(gid, []):
        stale = "" if d["applies"] else " <span class='muted'>(on an earlier version)</span>"
        rows.append(f"<div class='rev'><b>{esc(JUDGE.get(d['step'], d['step']))}:</b> "
                    f"{esc(d['verdict'])} — {esc(d['text'])}{stale}</div>")
    return f"<div class='revs'>{''.join(rows)}</div>" if rows else ""


# ── page ────────────────────────────────────────────────────────────────────
SECTIONS = [("what", "What this is"), ("story", "The story so far"),
            ("artifacts", "The artifacts"), ("open", "Open requests"),
            ("stand", "Where things stand"), ("process", "The process"),
            ("standards", "Standards"), ("ledger", "The ledger")]

CSS = """
:root{--ink:#1a202c;--muted:#718096;--line:#e2e8f0;--bg:#f7fafc;--card:#fff;--accent:#2b6cb0}
*{box-sizing:border-box}
body{font:15px/1.6 -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);margin:0}
main{max-width:1100px;margin:0 auto;padding:1.5rem 1.25rem 5rem}
h1{font-size:1.7rem;margin:.2rem 0 .4rem}
h2{font-size:1.3rem;margin:2.6rem 0 .7rem;padding-bottom:.35rem;border-bottom:2px solid var(--line);scroll-margin-top:3.4rem}
h3{font-size:1.05rem;margin:1.6rem 0 .5rem}
h4{font-size:.95rem;margin:1rem 0 .3rem;color:#2d3748}
p{max-width:74ch}p.lead{color:#4a5568}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.muted{color:var(--muted)}.small{font-size:.86rem}
code,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.82em}
nav{position:sticky;top:0;z-index:5;background:rgba(247,250,252,.94);backdrop-filter:blur(6px);border-bottom:1px solid var(--line);margin:0 -1.25rem 1rem;padding:.5rem 1.25rem}
nav a{display:inline-block;margin:.1rem .8rem .1rem 0;font-size:.85rem}
.chip{display:inline-block;padding:.05em .6em;border-radius:1em;color:#fff;font-size:.75rem;font-weight:600;line-height:1.6;vertical-align:middle;white-space:nowrap}
.tag{display:inline-block;padding:0 .45em;border-radius:3px;color:#fff;font-size:.66rem;text-transform:uppercase;letter-spacing:.05em;line-height:1.7;vertical-align:middle}
.who{display:inline-flex;align-items:center;gap:.3em;white-space:nowrap}
.dot{width:.6em;height:.6em;border-radius:50%;display:inline-block}
/* cycle strip */
.strip{display:flex;flex-wrap:wrap;gap:.4rem;align-items:stretch;margin:1rem 0}
.stepbox{flex:1 1 8.5rem;min-width:8.5rem;background:var(--card);border:1px solid var(--line);border-radius:7px;padding:.5rem .6rem;position:relative}
.stepbox .n{font-size:.66rem;color:var(--muted)}
.stepbox .nm{font-weight:600;font-size:.9rem;display:block;margin:.1rem 0 .35rem}
.stepbox .row{display:flex;justify-content:space-between;align-items:center;gap:.3rem;font-size:.78rem}
/* legend */
.legend{display:flex;flex-wrap:wrap;gap:.4rem 1.2rem;margin:.6rem 0}
.legend .it{font-size:.85rem;max-width:34ch}
/* timeline */
.tl{list-style:none;padding:0;margin:.6rem 0}
.tl li{padding:.35rem 0 .35rem .9rem;border-left:2px solid var(--line);margin-left:.3rem}
.tl .eff{color:var(--muted);font-size:.88rem}
/* cards */
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:.9rem 1.1rem;margin:1rem 0;scroll-margin-top:3.4rem}
.card>.hd{display:flex;flex-wrap:wrap;align-items:baseline;gap:.5rem;margin-bottom:.2rem}
.card>.hd .t{font-size:1.05rem;font-weight:600}
.prov{color:#4a5568;font-size:.9rem;margin:.25rem 0}
.stat{font-size:.9rem;margin:.2rem 0 .5rem;font-weight:500}
/* claims within a card */
.claim{border-top:1px solid var(--line);padding:.55rem 0}
.claim:first-of-type{border-top:none}
.claim .txt{margin:.1rem 0}
.claim .id{font-size:.72rem;color:var(--muted)}
.edges{font-size:.82rem;color:#4a5568;margin-top:.15rem}
.revs{margin:.35rem 0 .1rem .9rem;padding-left:.7rem;border-left:2px solid #edf2f7}
.rev{font-size:.85rem;color:#4a5568;padding:.05rem 0}
.report .line{border-top:1px solid var(--line);padding:.45rem 0;display:flex;gap:.6rem;align-items:baseline;flex-wrap:wrap}
.report .line .rz{color:#4a5568;font-size:.9rem}
.decision{background:#f7fafc;border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:5px;padding:.5rem .7rem;margin:.3rem 0 .6rem}
.sec-claim{border-top:1px solid #edf2f7;padding:.45rem 0}
details{margin:.5rem 0}summary{cursor:pointer;color:var(--accent);font-size:.9rem}
pre{background:#f1f5f9;padding:.7rem;border-radius:5px;overflow-x:auto;font-size:.8rem;white-space:pre-wrap;line-height:1.5}
.wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;font-size:.85rem}
th,td{text-align:left;vertical-align:top;padding:.4rem .55rem;border-bottom:1px solid #edf2f7}
th{font-weight:600;color:#4a5568;font-size:.7rem;text-transform:uppercase;letter-spacing:.04em}
.grid td{white-space:nowrap}.grid .why{color:var(--muted);font-size:.78rem;white-space:normal;max-width:16ch}
.pill{display:inline-block;background:#edf2f7;border-radius:4px;padding:0 .4em;font-size:.72rem;color:#4a5568;margin-right:.3rem}
"""


def board(proc: Process, store: Store, root: Path) -> str:
    st = status(proc, store, root)
    refs = Refs(proc, store)
    verdicts = verdicts_by_claim(proc, store, st)
    nav = "".join(f'<a href="#{sid}">{esc(name)}</a>' for sid, name in SECTIONS)
    parts = [
        '<!doctype html><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{esc(proc.name)} · board</title><style>{CSS}</style>",
        f"<main><h1>{esc(proc.name)}</h1>", f"<nav>{nav}</nav>",
        _what(proc, store, st),
        _story(proc, store, st),
        _artifacts(proc, store, root, st, refs, verdicts),
        _open(proc, store, st),
        _stand(proc, st, refs),
        _process(proc),
        _standards(),
        _ledger(proc, store),
        "</main>"]
    return "\n".join(parts)


# ── 1. what this is ─────────────────────────────────────────────────────────
def _what(proc: Process, store: Store, st: dict) -> str:
    subs = ", ".join(sorted(set(sid for stype in proc.subjects for sid in proc.subject_ids(stype)
                                if stype != "process")))
    lead = (
        "<section><h2 id='what'>What this is</h2>"
        f"<p class='lead'>This is one research project — <b>{esc(subs)}</b> — carried through the whole "
        "research &rarr; publishing &rarr; funding cycle by a mix of people, models and scripts. "
        "Every step is a question put to the project, and every answer is a set of plain claims — a "
        "hypothesis, a method, a result, a verdict. Nothing on this page was written by hand: it is all "
        "read back from the record of what was asked and answered.</p>")
    # the cycle, as a strip of the project's steps in order
    boxes = []
    project_steps = [s for stype in proc.subjects if stype != "process" for s in proc.steps_for(stype)]
    the_subject = next((sid for stype in proc.subjects if stype != "process"
                        for sid in proc.subject_ids(stype)), None)
    for i, s in enumerate(project_steps, 1):
        cell = st.get(the_subject, {}).get(s.id, {})
        v = cell.get("v")
        target = f"#{art_id(the_subject, s.id, v)}" if v else f"#{step_anchor(s.id)}"
        boxes.append(
            f"<a class='stepbox' href='{target}'><span class='n'>{i}</span>"
            f"<span class='nm'>{esc(step_name(s))}</span>"
            f"<span class='row'>{who(kind_of(s))} {chip(cell.get('state', 'absent'))}</span></a>")
    strip = f"<div class='strip'>{''.join(boxes)}</div>"
    note = ("<p class='small muted'>A twelfth step stands apart: the process reviews itself, asking "
            "whether each step above should exist. Its ruling is the last card under The artifacts.</p>")
    legend = "<div class='legend'>" + "".join(
        f"<div class='it'>{chip(s)} {esc(STATE_MEANING[s])}</div>" for s in TONE) + "</div>"
    return lead + strip + note + "<h3>What the colours mean</h3>" + legend + "</section>"


# ── 2. the story so far ─────────────────────────────────────────────────────
def answer_summary(cs: dict, step) -> str:
    if step.judges:
        n = sum(1 for c in cs.get("claims") or [] if c.get("type") == "assessment")
        return f"{n} assessments and a decision"
    if cs.get("sections") and not cs.get("claims"):
        n = len(cs["sections"])
        return f"a document of {n} section" + ("s" if n != 1 else "")
    n = len(cs.get("claims") or [])
    return f"{n} claim" + ("s" if n != 1 else "")


def _story(proc: Process, store: Store, st: dict) -> str:
    events = []
    for stype in proc.subjects:
        for sid in proc.subject_ids(stype):
            for idx, r in enumerate(store.ledger(sid)):
                events.append((r["answered"], idx, sid, r))
    events.sort(key=lambda e: (e[0], e[1]))
    out_of_date = {sid: sum(1 for c in cells.values() if c.get("state") in ("stale", "blocked"))
                   for sid, cells in st.items()}
    rows = []
    for when, _, sid, r in events:
        step = proc.steps[r["step"]]
        cs = C.load(store.version_dir(sid, r["step"], r["v"])) or {}
        summ = answer_summary(cs, step)
        link = f"<a href='#{art_id(sid, r['step'], r['v'])}'><em>{esc(step_name(step))}</em></a>"
        if r["v"] > 1:
            k = out_of_date.get(sid, 0)
            eff = f" <span class='eff'>This made {k} later step" + ("s" if k != 1 else "") + " out of date.</span>"
            line = f"{esc(r['by'])} answered {link} again (v{r['v']}): {esc(summ)}.{eff}"
        else:
            line = f"{esc(r['by'])} answered {link} for {esc(sid)} (v{r['v']}): {esc(summ)}."
        rows.append(f"<li><span class='muted small'>{esc(short_date(when))}</span> — {line}</li>")
    return ("<section><h2 id='story'>The story so far</h2>"
            "<p class='lead'>Every answer that has been recorded, oldest first. Each links to the "
            "artifact it produced.</p><ul class='tl'>" + "".join(rows) + "</ul></section>")


# ── 3. the artifacts ────────────────────────────────────────────────────────
def _artifacts(proc, store, root, st, refs: Refs, verdicts) -> str:
    cards = []
    for stype in proc.subjects:
        for sid in proc.subject_ids(stype):
            for step in proc.steps_for(stype):
                vs = store.versions(sid, step.id)
                for v in reversed(vs):                       # newest version first
                    cards.append(_card(proc, store, root, st, refs, verdicts, sid, step, v))
    return ("<section><h2 id='artifacts'>The artifacts</h2>"
            "<p class='lead'>One card per version, in the order the steps run. Each says who made it, "
            "from what, whether it is still current, and what it holds. Every claim links to where it "
            "is defined.</p>" + "".join(cards) + "</section>")


def _provenance(store, sid, step, v, rec, refs: Refs) -> str:
    who_made = "a script" if kind_of(step) == "code" else esc(rec.get("by"))
    ins = [refs.artifact_link(i["ref"], f"{noun(i['ref'].split(':', 1)[1])} (v{i['v']})")
           for i in rec.get("in", []) if i["kind"] == "step"]
    tail = []
    if any(i["kind"] == "instructions" for i in rec.get("in", [])):
        tail.append("its instructions")
    tail.append("the process definition")
    made_from = _join(ins + tail)
    frm = f", from {made_from}" if made_from else ""
    return f"<div class='prov'>Made by {who_made} on {esc(long_date(rec.get('answered')))}{frm}.</div>"


def _status_sentence(cell, store, refs: Refs) -> str:
    s = cell.get("state")
    if s == "current":
        return "<div class='stat' style='color:#2f855a'>Up to date.</div>"
    if s == "stale":
        names = [_moved_name(m, store) for m in cell.get("moved", [])]
        return f"<div class='stat' style='color:#b7791f'>Out of date: {_join(names)} changed after this was made.</div>"
    if s == "blocked":
        names = [f"{noun(b.split(':', 1)[1])}" for b in cell.get("blocked_by", [])]
        return f"<div class='stat' style='color:#c05621'>Waiting: {_join(names)} must be brought up to date first.</div>"
    if s == "pending":
        return f"<div class='stat' style='color:#2b6cb0'>A request is open, waiting for {esc(WORKER_WORD.get(kind_of(cell), 'an answer'))}.</div>"
    return "<div class='stat muted'>Not started.</div>"


def _moved_name(m: str, store: Store) -> str:
    if "/" in m or m.endswith(".yaml") or m.endswith(".md"):
        return "the instructions" if m.endswith(".md") else "the process definition"
    sub, step = m.split(":", 1)
    latest = store.latest(sub, step)
    return f"{noun(step)} (now v{latest})" if latest else noun(step)


def _card(proc, store, root, st, refs: Refs, verdicts, sid, step, v) -> str:
    vd = store.version_dir(sid, step.id, v)
    rec = store.run_record(sid, step.id, v) or {}
    cs = C.load(vd) or {}
    cell = st.get(sid, {}).get(step.id, {})
    is_latest = v == store.latest(sid, step.id)
    head = (f"<div class='hd'><span class='t'>{esc(title(step.id))} (version {v})</span> "
            f"{who(kind_of(step))} {chip(cell.get('state', 'absent'))}</div>")
    body = [head, _provenance(store, sid, step, v, rec, refs), _status_sentence(cell, store, refs)]
    if step.judges:
        body.append(_report(cs, step, sid, refs, is_latest))
    elif cs.get("sections") and not cs.get("claims"):
        body.append(_composition(cs, refs, verdicts))
    else:
        body.append(_claim_list(cs, sid, step, refs, verdicts, is_latest))
    body.append(_asked(vd))
    body.append(_files(root, vd, rec))
    return f"<article class='card' id='{art_id(sid, step.id, v)}'>" + "".join(body) + "</article>"


def _claim_list(cs, sid, step, refs: Refs, verdicts, anchor: bool) -> str:
    by_from: dict[str, list] = {}
    for e in cs.get("edges") or []:
        by_from.setdefault(e["from"], []).append(e)
    rows = []
    for c in cs.get("claims") or []:
        gid = C.gid(sid, step.id, c["id"])
        idattr = f" id='{claim_id(gid)}'" if anchor else ""
        edges = by_from.get(c["id"], []) + by_from.get(gid, [])
        esent = " · ".join(f"{esc(e['rel'])} {refs.link(_abs(sid, step.id, e['to']))}" for e in edges)
        estr = f"<div class='edges'>{esent}</div>" if esent else ""
        rows.append(
            f"<div class='claim'{idattr}>{tag(c.get('type'))} "
            f"<span class='id mono'>{esc(c['id'])}</span>"
            f"<div class='txt'>{esc(c.get('text'))}</div>{estr}{review_lines(gid, verdicts)}</div>")
    return "".join(rows)


def _composition(cs, refs: Refs, verdicts) -> str:
    out = []
    for sec in cs.get("sections") or []:
        out.append(f"<h4>{esc(sec['title'])}</h4>")
        for ref in sec.get("claims") or []:
            if ref.count(":") < 2:                            # a whole artifact, not a claim
                out.append(f"<div class='sec-claim'>{refs.artifact_link(ref)} "
                           f"<span class='muted small'>— see its own card</span></div>")
                continue
            t = refs.type_of(ref)
            label = tag(t) + " " if t else ""
            out.append(f"<div class='sec-claim'>{label}{refs.link(ref)} <div class='txt'>"
                       f"{esc(refs.text_of(ref))}</div>{review_lines(ref, verdicts)}</div>")
    return "<div class='doc'>" + "".join(out) + "</div>"


def _report(cs, step, sid, refs: Refs, anchor: bool) -> str:
    claims = cs.get("claims") or []
    decision = next((c for c in claims if c.get("type") == "decision"), None)
    assessments = [c for c in claims if c.get("type") == "assessment"]
    considered = [a for a in assessments if a.get("verdict") != "unconsidered"]
    out = []
    if decision:
        did = f" id='{claim_id(C.gid(sid, step.id, decision['id']))}'" if anchor else ""
        out.append(f"<div class='decision'{did}><b>Decision: {esc(decision.get('verdict'))}</b> — "
                   f"{esc(decision.get('text'))}</div>")
    for a in assessments:
        gid = C.gid(sid, step.id, a["id"])
        idattr = f" id='{claim_id(gid)}'" if anchor else ""
        about = (a.get("about") or [None])[0]
        item = a.get("judged") or (refs.text_of(about) if about else "")
        target = refs.link(about) if about else ""
        rz = f"<span class='rz'>{esc(a.get('text'))}</span>" if a.get("text") else ""
        out.append(f"<div class='line'{idattr}>"
                   f"<span class='pill'>{esc(a.get('verdict'))}</span>"
                   f"<span>{esc(item)} {('· ' + target) if target else ''}</span>{rz}</div>")
    count = (f"<p class='small muted'>{len(considered)} of {len(assessments)} items considered.</p>"
             if assessments else "")
    return f"<div class='report'>{''.join(out)}</div>{count}"


def _asked(vd: Path) -> str:
    q = (vd / "QUESTION.md")
    ins = (vd / "INSTRUCTIONS.md")
    blocks = []
    if q.is_file():
        blocks.append(f"<h4>The question, as posed</h4><pre>{esc(q.read_text(encoding='utf-8'))}</pre>")
    if ins.is_file():
        blocks.append(f"<h4>Instructions</h4><pre>{esc(ins.read_text(encoding='utf-8'))}</pre>")
    if not blocks:
        return ""
    return "<details><summary>What the agent was asked</summary>" + "".join(blocks) + "</details>"


def _files(root: Path, vd: Path, rec: dict) -> str:
    rel = vd.relative_to(root)
    return ("<details><summary>Files &amp; provenance</summary>"
            f"<p class='small'>Directory: <code>{esc(rel)}</code></p>"
            f"<pre>{esc(json.dumps(rec, indent=2, sort_keys=True))}</pre></details>")


# ── 4. open requests ────────────────────────────────────────────────────────
def _open(proc, store, st) -> str:
    cards = []
    for sid, cells in st.items():
        for step_id, c in cells.items():
            if c.get("state") != "pending" and not c.get("request_open"):
                continue
            step = proc.steps[step_id]
            rd = store.request_dir(sid, step_id)
            man = rd / "manifest.json"
            items = ""
            if man.is_file():
                n = len((json.loads(man.read_text(encoding="utf-8")).get("items") or {}))
                if n:
                    items = f" {n} items to judge."
            cards.append(
                f"<article class='card'><div class='hd'><span class='t'>Waiting for "
                f"{esc(WORKER_WORD.get(kind_of(step), 'an answer'))}: {esc(step_name(step))} for {esc(sid)}.</span></div>"
                f"<p class='prov'>{esc(step.question)}{items}</p></article>")
    inner = "".join(cards) or "<p class='muted'>Nothing is open right now — every question has been answered.</p>"
    return ("<section><h2 id='open'>Open requests</h2>"
            "<p class='lead'>Questions a person or an agent could answer now.</p>" + inner + "</section>")


# ── 5. where things stand ───────────────────────────────────────────────────
def _stand(proc, st, refs: Refs) -> str:
    out = ["<section><h2 id='stand'>Where things stand</h2>",
           "<p class='lead'>Every subject against every step. Worked out from the record each time the "
           "page is built, never stored. A cell that is not up to date says why.</p>"]
    for stype in proc.subjects:
        steps = proc.steps_for(stype)
        out.append(f"<h3>{esc(stype)}</h3><div class='wrap'><table class='grid'><tr><th>subject</th>"
                   + "".join(f"<th>{esc(step_name(s))}</th>" for s in steps) + "</tr>")
        for sid in proc.subject_ids(stype):
            cells = ["<td><span class='mono'>" + esc(sid) + "</span></td>"]
            for s in steps:
                c = st[sid][s.id]
                why = ""
                if c["state"] == "stale" and c.get("moved"):
                    why = "changed input"
                elif c["state"] == "blocked" and c.get("blocked_by"):
                    why = "waiting on " + noun(c["blocked_by"][0].split(":", 1)[1]).replace("the ", "")
                elif c["state"] == "pending":
                    why = "open request"
                elif c["state"] == "absent":
                    why = "not started"
                v = f"<div class='small muted'>v{c['v']}</div>" if c.get("v") else ""
                w = f"<div class='why'>{esc(why)}</div>" if why else ""
                cells.append(f"<td>{chip(c['state'])}{v}{w}</td>")
            out.append("<tr>" + "".join(cells) + "</tr>")
        out.append("</table></div>")
    return "\n".join(out) + "</section>"


# ── 6. the process (the definition) ─────────────────────────────────────────
def _process(proc: Process) -> str:
    out = ["<section><h2 id='process'>The process</h2>",
           "<p class='lead'>This is the <b>definition</b> — the rules the run above followed, not what "
           "happened. Each step is a question, an answerer, what it reads, and what it must produce.</p>"]
    for sid in proc.order():
        s = proc.steps[sid]
        reads = _join([f"<a href='#{step_anchor(t)}'>{esc(noun(t))}</a>"
                       for t in s.inputs if "/" not in t and "." not in t]) or "nothing but its instructions"
        if s.judges:
            produces = ("assessments and a decision about " +
                        ("the process itself" if s.judges == "process" else esc(noun(s.judges.split(':')[-1]))))
        elif s.emits:
            produces = "claims of type " + ", ".join(esc(e) for e in s.emits)
        else:
            produces = "a composition — a document that arranges other claims"
        cmd = (f"<p class='small'><span class='pill'>command</span><code>{esc(s.command)}</code></p>"
               if s.command else "")
        instr = ""
        p = proc.path.parent / (s.instructions or "")
        if s.instructions and p.is_file():
            instr = (f"<details><summary>Instructions</summary><pre>"
                     f"{esc(p.read_text(encoding='utf-8'))}</pre></details>")
        out.append(
            f"<article class='card' id='{step_anchor(sid)}'><div class='hd'>"
            f"<span class='t'>{esc(step_name(s))}</span> {who(kind_of(s))}</div>"
            f"<p class='prov'>{esc(s.question)}</p>"
            f"<p class='small'><b>Reads:</b> {reads}. <b>Produces:</b> {produces}.</p>{cmd}{instr}</article>")
    return "\n".join(out) + "</section>"


# ── 7. standards and the ledger ─────────────────────────────────────────────
def _standards() -> str:
    std = yaml.safe_load((Path(__file__).resolve().parent / "standards.yaml").read_text(encoding="utf-8"))
    rows = "".join(f"<tr><td>{tag(t)}</td><td class='small'>{esc('; '.join(f'{k}: {v}' for k, v in m.items()))}</td></tr>"
                   for t, m in std["types"].items())
    rels = "".join(f"<tr><td><code>{esc(r)}</code></td><td class='small'>{esc('; '.join(f'{k}: {v}' for k, v in m.items()))}</td></tr>"
                   for r, m in std["relations"].items())
    recs = "".join(f"<tr><td><code>{esc(k)}</code></td><td class='small'>{esc('; '.join(f'{a}: {b}' for a, b in m.items()))}</td></tr>"
                   for k, m in std.items() if k in ("process", "step", "run", "version", "worker"))
    return ("<section><h2 id='standards'>Standards</h2>"
            "<p class='lead'>How this vocabulary maps onto established ones, kept from the start and "
            "exported with every version. Where a standard does not fit, the note says so.</p>"
            f"<h3>Records</h3><div class='wrap'><table>{recs}</table></div>"
            f"<h3>Claim types</h3><div class='wrap'><table>{rows}</table></div>"
            f"<h3>Relations</h3><div class='wrap'><table>{rels}</table></div></section>")


def _ledger(proc, store) -> str:
    rows = []
    for stype in proc.subjects:
        for sid in proc.subject_ids(stype):
            for r in store.ledger(sid):
                rows.append((r["answered"], f"<tr><td class='mono'>{esc(r['answered'])}</td>"
                             f"<td class='mono'>{esc(sid)}</td><td>{esc(step_name(proc.steps[r['step']]))} v{r['v']}</td>"
                             f"<td>{esc(kind_of(r))}</td><td>{esc(r['by'])}</td>"
                             f"<td class='small muted'>{esc(r.get('note'))}</td></tr>"))
    rows.sort(reverse=True)
    return ("<section><h2 id='ledger'>The ledger</h2>"
            "<p class='lead'>The raw append-only record, newest first — the source everything above is "
            "built from.</p><div class='wrap'><table><tr><th>answered</th><th>subject</th><th>step</th>"
            "<th>worker</th><th>by</th><th>note</th></tr>" + "".join(r for _, r in rows) + "</table></div></section>")


# ── small helpers ───────────────────────────────────────────────────────────
def _join(items: list[str]) -> str:
    items = [i for i in items if i]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def _abs(sid: str, step_id: str, ref: str) -> str:
    return ref if ":" in ref else C.gid(sid, step_id, ref)
