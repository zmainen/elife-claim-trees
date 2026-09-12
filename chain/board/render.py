"""The renderer: reads the store and the process and returns one static HTML page — masthead,
the loop drawn as a loop, the players with their records, the artifacts as documents and reports,
the process, the standards and the ledger. Generated entirely from the store; same store in,
identical file out."""

from __future__ import annotations

import json
import math
from pathlib import Path

import yaml

from .. import claims as C
from ..process import Process
from ..status import status
from ..store import Store
from .read import Facts, Refs, review_lines, verdicts_by_claim
from .theme import (CSS, GROUPS, NOUN, ROLE_TONE, ROLE_WASH, SET_PHRASE, STATE_MEANING,
                    STATE_WORD, STEP_SHORT, TONE, _abs, _join, art_id, chip, claim_id, esc,
                    long_date, noun, player_anchor, step_anchor, step_name, tag, title)


SECTIONS = [("loop", "The loop"), ("players", "The players"),
            ("artifacts", "The artifacts"), ("open", "Open requests"),
            ("process", "The process"), ("standards", "Standards"), ("ledger", "The ledger")]



def board(proc: Process, store: Store, root: Path) -> str:
    st = status(proc, store, root)
    refs = Refs(proc, store)
    facts = Facts(proc, store)
    verdicts = verdicts_by_claim(proc, store, st)
    nav = "".join(f'<a href="#{sid}">{esc(name)}</a>' for sid, name in SECTIONS)
    parts = [
        '<!doctype html><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{esc(proc.name)} · board</title><style>{CSS}</style>",
        "<main>",
        _mast(proc, store, facts),
        f"<nav>{nav}</nav>",
        _loop(proc, store, st, facts),
        _players(proc, store, st, facts, refs),
        _artifacts(proc, store, root, st, refs, facts, verdicts),
        _open(proc, store, st, facts),
        _process(proc),
        _standards(),
        _ledger(proc, store, facts),
        "</main>"]
    return "\n".join(parts)


# ── masthead ────────────────────────────────────────────────────────────────
def _mast(proc: Process, store: Store, facts: Facts) -> str:
    nplayers = sum(len(proc.subject_ids(t)) for t, _ in GROUPS)
    nsteps = len(proc.steps)
    return (
        "<header class='mast'>"
        "<p class='eyebrow'>Scientopia · the scientific loop as one game</p>"
        f"<h1>{esc(proc.name.title())}</h1>"
        "<p class='standfirst'>Two research teams, a funder, a journal and a library carry one "
        "question through the whole cycle of science — asking, proposing, funding, studying, "
        "reviewing, publishing — and round again. Every artifact is a set of plain claims; nothing "
        "on this page was written by hand.</p>"
        "<p class='note'>This is one worked round. Every answer in it came from a stand-in — a "
        "fixture standing in for the player named — so the shape of the loop can be seen whole "
        "before any single judgement is made well.</p>"
        f"<div class='meta'><span><b>{nplayers}</b> players</span><span><b>{nsteps}</b> steps</span>"
        "<span><b>one</b> round</span><span>players answer their steps; the referee runs the rest</span>"
        "</div></header>")


# ── the loop ────────────────────────────────────────────────────────────────
def _now(proc, store, st, facts: Facts, sid: str, stype: str) -> str:
    """A single plain phrase for what this player is doing now."""
    cells = st.get(sid, {})
    if any(c.get("state") == "pending" for c in cells.values()):
        step = next(s for s, c in cells.items() if c.get("state") == "pending")
        return f"a request is open: {STEP_SHORT.get(step, step).lower()}"
    if stype == "team":
        f = facts.funded(sid)
        if f and f["verdict"] == "reject":
            return "declined; no study" if not facts.study_run(sid) else "declined"
        if not facts.study_run(sid) and not f:
            return "no study yet"
        if cells.get("question", {}).get("state") == "stale":
            return "out of date: the library grew"
        return "up to date"
    if stype == "funder":
        d = facts.cs(sid, "select").get("claims") or []
        funded = sum(1 for c in d if c.get("type") == "decision" and c.get("verdict") == "accept")
        total = sum(1 for c in d if c.get("type") == "decision")
        return f"funded {funded} of {total}" if total else "no call decided"
    if stype == "journal":
        n = sum(1 for p in facts.pubs if p["journal"] == sid)
        return f"published {n} article" + ("s" if n != 1 else "")
    if stype == "library":
        n = len(facts.pubs)
        return f"grew: {n} article" + ("s" if n != 1 else "") + " added"
    return STATE_WORD.get(next(iter(cells.values()), {}).get("state", ""), "")


def _loop(proc, store, st, facts: Facts) -> str:
    teams, funders = proc.subject_ids("team"), proc.subject_ids("funder")
    journals = proc.subject_ids("journal")
    cx, cy, R = 380, 250, 190

    def spread(lo, hi, n):
        return [(lo + hi) / 2] if n == 1 else [lo + (hi - lo) * i / (n - 1) for i in range(n)]

    ring = [("library", "library", 90)]
    ring += [(s, "team", a) for s, a in zip(teams, spread(150, 210, len(teams)))]
    ring += [(s, "funder", a) for s, a in zip(funders, spread(255, 285, len(funders)))]
    ring += [(s, "journal", a) for s, a in zip(journals, spread(345, 375, len(journals)))]

    def pt(a, r):
        return (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))

    svg = ['<svg class="loop" viewBox="0 0 760 500" role="img" '
           'aria-label="The loop the players turn, drawn as a ring.">',
           '<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="6.5" refY="3" '
           'orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#94908c"/></marker></defs>',
           f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#e2ded9" stroke-width="1.5"/>']
    # flow arrows between consecutive stations, in loop order
    gap = 20
    for i in range(len(ring)):
        a1, a2 = ring[i][2], ring[(i + 1) % len(ring)][2]
        if a2 <= a1:
            a2 += 360
        x1, y1 = pt(a1 + gap, R)
        x2, y2 = pt(a2 - gap, R)
        svg.append(f'<path d="M{x1:.1f},{y1:.1f} A{R},{R} 0 0 1 {x2:.1f},{y2:.1f}" fill="none" '
                   f'stroke="#94908c" stroke-width="1.6" marker-end="url(#ah)"/>')
    # centre label
    svg.append(f'<text x="{cx}" y="{cy-6}" text-anchor="middle" font-size="13" fill="#94908c" '
               'letter-spacing="2" font-weight="600">THE LOOP</text>'
               f'<text x="{cx}" y="{cy+14}" text-anchor="middle" font-size="11.5" fill="#a8a49f">'
               'claims go round</text>')
    # nodes
    for sid, stype, a in ring:
        x, y = pt(a, R)
        left = math.cos(math.radians(a)) < -0.2
        top = math.sin(math.radians(a)) < -0.4
        bottom = math.sin(math.radians(a)) > 0.4
        w, h = 140, 46
        rx = x - w - 10 if left else (x + 10 if not (top or bottom) else x - w / 2)
        ry = y - h / 2 + (-34 if top else (34 if bottom else 0))
        rx = max(4, min(rx, 760 - w - 4))
        ry = max(4, min(ry, 500 - h - 4))
        # connector from ring point to card
        ccx = rx + (w if rx + w < x else (0 if rx > x else w / 2))
        ccy = ry + h / 2
        col, wash = ROLE_TONE[stype], ROLE_WASH[stype]
        now = _now(proc, store, st, facts, sid, stype)
        svg.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{ccx:.1f}" y2="{ccy:.1f}" '
                   f'stroke="{col}" stroke-width="1.2" opacity=".5"/>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{col}"/>')
        svg.append(
            f'<a href="#{player_anchor(sid)}"><g>'
            f'<rect class="node" x="{rx:.1f}" y="{ry:.1f}" width="{w}" height="{h}" rx="8" '
            f'fill="{wash}" stroke="{col}" stroke-width="1.4"/>'
            f'<text x="{rx + w/2:.1f}" y="{ry + 19:.1f}" text-anchor="middle" font-size="12.5" '
            f'font-weight="600" fill="#1a202c">{esc(facts.name(sid))}</text>'
            f'<text x="{rx + w/2:.1f}" y="{ry + 35:.1f}" text-anchor="middle" font-size="10.5" '
            f'fill="{col}">{esc(now)}</text></g></a>')
    svg.append("</svg>")
    jn = _join([facts.name(j) for j in journals]) or "a journal"
    legend = "<div class='legend'>" + "".join(
        f"<div class='it'>{chip(s)} {esc(STATE_MEANING[s])}</div>" for s in TONE) + "</div>"
    return ("<section><h2 id='loop'>The loop</h2>"
            "<p class='sec-note'>A directed cycle, not a line — claims go round</p>"
            "<div class='loopwrap'>" + "".join(svg) + "</div>"
            "<p class='small muted'>Each player sits on the ring at its place — teams on the left, "
            "funders at the top, journals on the right, the library at the bottom — showing what it "
            "is doing now. Click a player to jump to its card.</p>"
            f"<p>When {jn} publishes an article it lands in the library, which every team and every "
            "funder reads. That makes each team's earlier reading of the library out of date, so the "
            "loop comes round again: the teams re-ask their questions and the funder re-issues its "
            "call. Nothing here is broken — the arrows are the point.</p>"
            "<h3>The five states</h3>" + legend + "</section>")


# ── the players ─────────────────────────────────────────────────────────────
def _players(proc, store, st, facts: Facts, refs: Refs) -> str:
    out = ["<section><h2 id='players'>The players</h2>",
           "<p class='sec-note'>Who they are · what they have done · what they are doing now</p>",
           "<p>The institutions come first: each team, funder, journal and the library, with the "
           "record read back from what it produced. Its current activity and its artifacts are the "
           "drill-down beneath.</p>"]
    for stype, heading in GROUPS:
        ids = proc.subject_ids(stype)
        if not ids:
            continue
        out.append(f"<h3>{esc(heading)}</h3>")
        for sid in ids:
            out.append(_pcard(proc, store, st, facts, refs, sid, stype))
    return "\n".join(out) + "</section>"


def _persona_html(proc, sid: str) -> tuple[str, str]:
    """First paragraph, and the full persona for a collapsible."""
    rel = proc.meta(sid).get("persona")
    if not rel:
        return "", ""
    p = proc.path.parent / rel
    if not p.is_file():
        return "", ""
    text = p.read_text(encoding="utf-8").strip()
    body = "\n".join(l for l in text.splitlines() if not l.startswith("#")).strip()
    first = body.split("\n\n")[0].replace("\n", " ").strip()
    return first, text


def _pcard(proc, store, st, facts: Facts, refs: Refs, sid: str, stype: str) -> str:
    col = ROLE_TONE[stype]
    first, full = _persona_html(proc, sid)
    persona = f"<p class='persona'>{esc(first)}</p>" if first else ""
    full_block = (f"<details><summary>Full persona</summary><pre>{esc(full)}</pre></details>"
                  if full and full.strip() != ("# " + first).strip() else "")
    record = _record(proc, store, st, facts, refs, sid, stype)
    now = _now_block(proc, store, st, facts, sid, stype)
    links = _player_links(proc, store, sid, refs)
    role = {"team": "research team", "funder": "funder", "journal": "journal",
            "library": "library"}.get(stype, stype)
    return (f"<article class='pcard' id='{player_anchor(sid)}' style='--rail:{col}'>"
            f"<div class='hd'><span class='nm'>{esc(facts.name(sid))}</span>"
            f"<span class='role'>{esc(role)}</span>"
            f"<span class='chip ghost' style='--c:{col}'>{esc(_now(proc, store, st, facts, sid, stype))}</span></div>"
            f"{persona}{full_block}"
            f"<div class='block'><div class='lbl'>Record</div><div class='record'>{record}</div></div>"
            f"<div class='block'><div class='lbl'>Now</div>{now}</div>{links}</article>")


def _record(proc, store, st, facts: Facts, refs: Refs, sid: str, stype: str) -> str:
    n = facts.name(sid)
    if stype == "team":
        return _team_record(proc, store, facts, refs, sid, n)
    if stype == "funder":
        return _funder_record(proc, store, facts, refs, sid, n)
    if stype == "journal":
        return _journal_record(proc, store, facts, refs, sid, n)
    return _library_record(proc, store, facts, refs, sid, n)


def _team_record(proc, store, facts: Facts, refs: Refs, sid: str, n: str) -> str:
    props = len(store.versions(sid, "proposal"))
    f = facts.funded(sid)
    lines = [f"Made {props} proposal" + ("s" if props != 1 else "") + "."]
    if f:
        funder = facts.name([x["player"] for x in facts.decisions_about("select", f"{sid}:proposal")][0])
        why = f["text"].split(":", 1)[1].strip() if f["text"][:9].lower().startswith(("funded:", "declined:")) else f["text"]
        word = "Funded" if f["verdict"] == "accept" else "Declined"
        lines.append(f"{word} by {esc(funder)} — {esc(why)}")
    if facts.study_run(sid):
        lines.append("Ran the study and reported results.")
    else:
        lines.append("No study was run.")
    pub = [p for p in facts.pubs if p["team"] == sid]
    if pub:
        jn = facts.name(pub[0]["journal"])
        link = refs.artifact_link(pub[0]["journal"] + ":published", pub[0]["id"])
        lines.append(f"Published 1 article in {esc(jn)} ({link}).")
    else:
        lines.append("Nothing published.")
    tally = facts.tally_of("review", f"{sid}:paper")
    if tally:
        lines.append("Reviewers found " + _tally_phrase(tally) + ".")
    cited = facts.cited.get(sid, 0)
    lines.append(f"Cited {cited} time" + ("s" if cited != 1 else "") + " by others.")
    return "".join(f"<p class='line'>{x}</p>" for x in lines)


def _funder_record(proc, store, facts: Facts, refs: Refs, sid: str, n: str) -> str:
    calls = len(store.versions(sid, "call"))
    dec = [c for c in facts.cs(sid, "select").get("claims") or [] if c.get("type") == "decision"]
    lines = [f"Issued {calls} call" + ("s" if calls != 1 else "") + ".",
             f"Read {len(dec)} proposal" + ("s" if len(dec) != 1 else "") + "."]
    for c in dec:
        team = facts.name((c.get("about") or [""])[0].split(":")[0])
        word = "Funded" if c.get("verdict") == "accept" else "Declined"
        lines.append(f"{word} {esc(team)} — {esc(c.get('text'))}")
    return "".join(f"<p class='line'>{x}</p>" for x in lines)


def _journal_record(proc, store, facts: Facts, refs: Refs, sid: str, n: str) -> str:
    sub = facts.cs(sid, "submissions").get("sections") or []
    nsub = sum(len(s.get("claims") or []) for s in sub)
    nrev = sum(1 for c in facts.cs(sid, "review").get("claims") or [] if c.get("type") == "assessment")
    dec = [c for c in facts.cs(sid, "decision").get("claims") or [] if c.get("type") == "decision"]
    lines = [f"Received {nsub} submission" + ("s" if nsub != 1 else "") + ".",
             f"Delivered {nrev} review" + ("s" if nrev != 1 else "") + " (one per claim)."]
    for c in dec:
        team = facts.name((c.get("about") or [""])[0].split(":")[0])
        word = "Accepted" if c.get("verdict") == "accept" else "Rejected"
        lines.append(f"{word} {esc(team)}'s paper — {esc(c.get('text'))}")
    pubs = [p for p in facts.pubs if p["journal"] == sid]
    if pubs:
        arts = _join([f"{esc(p['id'])} ({facts.name(p['team'])})" for p in pubs])
        lines.append(f"Published {len(pubs)}: {arts}.")
    return "".join(f"<p class='line'>{x}</p>" for x in lines)


def _library_record(proc, store, facts: Facts, refs: Refs, sid: str, n: str) -> str:
    imp = facts.cs(sid, "import")
    sources = sorted({(c.get("by") or "").split(":", 1)[-1] for c in imp.get("claims") or [] if c.get("by")})
    nseed = len(imp.get("claims") or [])
    lines = [f"Holds {nseed} imported claim" + ("s" if nseed != 1 else "") +
             (f" from {len(sources)} seed source" + ("s" if len(sources) != 1 else "") + "." if sources else "."),
             f"Holds {len(facts.pubs)} publication" + ("s" if len(facts.pubs) != 1 else "") +
             " added by the journals."]
    cited = facts.cited.get(sid, 0)
    lines.append(f"Its claims were cited {cited} time" + ("s" if cited != 1 else "") + " by the teams.")
    return "".join(f"<p class='line'>{x}</p>" for x in lines)


def _tally_phrase(tally: dict) -> str:
    return _join([f"{v} {k}" for k, v in tally.items()])


def _now_block(proc, store, st, facts: Facts, sid: str, stype: str) -> str:
    cells = st.get(sid, {})
    steps = proc.steps_for(stype)
    strip = []
    notes = []
    for s in steps:
        c = cells.get(s.id, {})
        state = c.get("state", "absent")
        v = c.get("v")
        vt = f" <span class='muted'>v{v}</span>" if v else ""
        strip.append(f"<span class='stepcell'><span class='s'>{esc(STEP_SHORT.get(s.id, s.id))}</span>"
                     f"{chip(state)}{vt}</span>")
        sent = _cell_sentence(proc, store, st, facts, sid, s.id, c)
        if sent:
            notes.append(f"<div class='n'>{sent}</div>")
    return (f"<div class='strip'>{''.join(strip)}</div>"
            + (f"<div class='notes'>{''.join(notes)}</div>" if notes else
               "<div class='notes'><div class='n muted'>Every step is up to date.</div></div>"))


def _cell_sentence(proc, store, st, facts: Facts, sid: str, step_id: str, c: dict) -> str:
    state = c.get("state")
    if state == "current" or state == "absent":
        return ""
    short = STEP_SHORT.get(step_id, step_id)
    if state == "stale":
        for m in c.get("moved", []):
            if ":*:" in m:
                jn = _join([facts.name(j) for j in proc.subject_ids(m.split(":")[0])])
                return (f"Its {esc(short.lower())} is out of date: {esc(jn)} published since it "
                        "read the library.")
        return f"Its {esc(short.lower())} is out of date: an input changed."
    if state == "blocked":
        ups = _join([noun(b.split(":", 1)[1]) for b in c.get("blocked_by", [])])
        return f"Its {esc(short.lower())} is waiting on {ups} to be brought up to date."
    if state == "pending":
        return f"A request is open for its {esc(short.lower())}."
    return ""


def _player_links(proc, store, sid: str, refs: Refs) -> str:
    links = []
    for step in proc.steps_for(proc.type_of(sid)):
        if store.latest(sid, step.id) is not None:
            links.append(refs.artifact_link(f"{sid}:{step.id}", title(step.id)))
    if not links:
        return ""
    return ("<div class='linkrow'><span class='lbl'>Artifacts</span>" + " ".join(links) + "</div>")


# ── the artifacts (drill-down, by player) ───────────────────────────────────
def _artifacts(proc, store, root, st, refs: Refs, facts: Facts, verdicts) -> str:
    out = ["<section><h2 id='artifacts'>The artifacts</h2>",
           "<p class='sec-note'>Everything each player made, in the order the steps run</p>",
           "<p>The drill-down. A proposal or a paper reads like a document; a review or a decision "
           "reads like a report, the decision first and then one line per item. Every reference is a "
           "link to where the claim is defined.</p>"]
    for stype, heading in GROUPS + [("process", "The process itself")]:
        for sid in proc.subject_ids(stype):
            cards = []
            for step in proc.steps_for(stype):
                for v in reversed(store.versions(sid, step.id)):
                    cards.append(_card(proc, store, root, st, refs, facts, verdicts, sid, step, v))
            if cards:
                out.append(f"<div class='pgroup'><h3>{esc(facts.name(sid))}</h3>" + "".join(cards) + "</div>")
    return "\n".join(out) + "</section>"


def _provenance(store, facts: Facts, sid, step, v, rec, refs: Refs) -> str:
    made_by = facts.by_phrase(rec.get("by"))
    verb = "Assembled by" if step.automatic else "Made by"
    # A judging step records the set input and each of its expanded members; name the set once.
    set_steps = {i["ref"].split(":")[-1] for i in rec.get("in", []) if i.get("kind") == "set"}
    ins = []
    for i in rec.get("in", []):
        if i.get("kind") == "step":
            if i["ref"].split(":", 1)[1] in set_steps:
                continue
            ins.append(refs.artifact_link(i["ref"], f"{noun(i['ref'].split(':', 1)[1])} (v{i['v']})"))
        elif i.get("kind") == "set":
            ins.append(SET_PHRASE.get(i.get("ref"), i.get("ref")))
        elif i.get("kind") not in ("instructions", "persona", "declaration"):
            p = i.get("path", "")
            ins.append("the seed corpus" if "seed" in p else esc(p))
    frm = f" from {_join(ins)}" if ins else ""
    when = long_date(rec.get("answered")) if rec.get("answered") else ""
    return f"<div class='prov'>{verb} {esc(made_by)} on {esc(when)}{frm}.</div>"


def _status_sentence(cell, store, facts: Facts) -> str:
    s = cell.get("state")
    if s == "current":
        return "<div class='stat' style='color:#2f855a'>Up to date.</div>"
    if s == "stale":
        names = []
        for m in cell.get("moved", []):
            if ":*:" in m:
                names.append("the library (it grew)")
            elif m.endswith(".yaml"):
                names.append("the process")
            else:
                sub, step = m.split(":", 1)
                names.append(noun(step))
        return (f"<div class='stat' style='color:#b7791f'>Out of date: {_join(names)} changed after "
                "this was made.</div>")
    if s == "blocked":
        names = [noun(b.split(":", 1)[1]) for b in cell.get("blocked_by", [])]
        return (f"<div class='stat' style='color:#c05621'>Waiting: {_join(names)} must be brought up "
                "to date first.</div>")
    if s == "pending":
        return "<div class='stat' style='color:#2b6cb0'>A request is open, waiting to be answered.</div>"
    return "<div class='stat muted'>Not started.</div>"


def _card(proc, store, root, st, refs: Refs, facts: Facts, verdicts, sid, step, v) -> str:
    vd = store.version_dir(sid, step.id, v)
    rec = store.run_record(sid, step.id, v) or {}
    cs = C.load(vd) or {}
    cell = st.get(sid, {}).get(step.id, {})
    is_latest = v == store.latest(sid, step.id)
    col = TONE.get(cell.get("state", "absent"), "#a0aec0")
    vlabel = f" (version {v})" if len(store.versions(sid, step.id)) > 1 else ""
    head = (f"<div class='hd'><span class='t'>{esc(title(step.id))}{vlabel}</span> "
            f"{chip(cell.get('state', 'absent'))}</div>")
    body = [head, _provenance(store, facts, sid, step, v, rec, refs), _status_sentence(cell, store, facts)]
    if step.judges:
        body.append(_report(cs, step, sid, refs, facts, is_latest))
    elif cs.get("sections") and not cs.get("claims"):
        body.append(_composition(cs, refs, verdicts))
    elif not cs.get("claims"):
        body.append("<p class='muted small'>Empty.</p>")
    else:
        body.append(_claim_list(cs, sid, step, refs, verdicts, is_latest))
    body.append(_asked(vd))
    body.append(_files(root, vd, rec))
    return (f"<article class='card' id='{art_id(sid, step.id, v)}' style='--rail:{col}'>"
            + "".join(body) + "</article>")


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
        head = esc(sec["title"])
        if sec.get("id"):
            head += f" <span class='muted mono small'>{esc(sec['id'])}</span>"
        out.append(f"<h4>{head}</h4>")
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


def _report(cs, step, sid, refs: Refs, facts: Facts, anchor: bool) -> str:
    claims = cs.get("claims") or []
    decisions = [c for c in claims if c.get("type") == "decision"]
    assessments = [c for c in claims if c.get("type") == "assessment"]
    considered = [a for a in assessments if a.get("verdict") != "unconsidered"]
    out = []
    for decision in decisions:
        did = f" id='{claim_id(C.gid(sid, step.id, decision['id']))}'" if anchor else ""
        about = (decision.get("about") or [None])[0]
        who = ""
        if about and ":" in about and about != "process":
            owner, wstep = about.split(":", 1)
            label = f"{facts.name(owner)}'s {noun(wstep).replace('the ', '')}"
            who = f" on {refs.link(about, label)}"
        elif about == "process":
            who = " on the process"
        out.append(f"<div class='decision'{did}><b>Decision: {esc(decision.get('verdict'))}</b>{who} — "
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
    blocks = []
    for fn, heading in (("QUESTION.md", "The question, as posed"), ("INSTRUCTIONS.md", "Instructions"),
                        ("PERSONA.md", "The persona given")):
        p = vd / fn
        if p.is_file():
            blocks.append(f"<h4>{heading}</h4><pre>{esc(p.read_text(encoding='utf-8'))}</pre>")
    if not blocks:
        return ""
    return "<details><summary>What was asked</summary>" + "".join(blocks) + "</details>"


def _files(root: Path, vd: Path, rec: dict) -> str:
    rel = vd.relative_to(root)
    return ("<details><summary>Files &amp; provenance</summary>"
            f"<p class='small'>Directory: <code>{esc(rel)}</code></p>"
            f"<pre>{esc(json.dumps(rec, indent=2, sort_keys=True))}</pre></details>")


# ── open requests ───────────────────────────────────────────────────────────
def _open(proc, store, st, facts: Facts) -> str:
    cards = []
    for sid, cells in st.items():
        for step_id, c in cells.items():
            if c.get("state") != "pending" and not c.get("request_open"):
                continue
            step = proc.steps[step_id]
            man = store.request_dir(sid, step_id) / "manifest.json"
            items = ""
            if man.is_file():
                n = len((json.loads(man.read_text(encoding="utf-8")).get("items") or {}))
                if n:
                    items = f" {n} items to judge."
            answerer = "the referee" if step.automatic else f"{facts.name(sid)}"
            cards.append(
                f"<article class='card'><div class='hd'><span class='t'>{esc(step_name(step))} — "
                f"{esc(facts.name(sid))}</span></div>"
                f"<p class='prov'>Waiting for {esc(answerer)}. {esc(step.question)}{items}</p></article>")
    inner = "".join(cards) or ("<p class='muted'>Nothing is open right now. The loop has come round: "
                               "every team's reading of the library is out of date, and the next round "
                               "would re-ask those questions.</p>")
    return ("<section><h2 id='open'>Open requests</h2>"
            "<p class='sec-note'>Questions that could be answered now</p>" + inner + "</section>")


# ── the process (the definition) ────────────────────────────────────────────
def _process(proc: Process) -> str:
    out = ["<section><h2 id='process'>The process</h2>",
           "<p class='sec-note'>The definition — the rules the round above followed</p>",
           "<p>This is the <b>definition</b>, not what happened: each step is a question put to a "
           "kind of player, what it reads, and what it must produce. A step with a command is run by "
           "the referee; every other waits for its player.</p>"]
    by_type = {}
    for sid in proc.order():
        by_type.setdefault(proc.steps[sid].subject, []).append(proc.steps[sid])
    labels = {"library": "The library", "team": "Research teams", "funder": "Funders",
              "journal": "Journals", "process": "The process itself"}
    for stype in proc.subjects:
        steps = by_type.get(stype, [])
        if not steps:
            continue
        out.append(f"<h3>{esc(labels.get(stype, stype))}</h3>")
        for s in steps:
            reads = _join([_input_phrase(t) for t in s.inputs]) or "only its instructions"
            if s.judges:
                produces = ("assessments and a decision about " +
                            ("the process itself" if s.judges == "process" else SET_PHRASE.get(s.judges, esc(noun(s.judges.split(':')[-1])))))
            elif s.emits:
                produces = "claims of type " + ", ".join(esc(e) for e in s.emits)
            elif s.command and "compose" in s.command:
                produces = "a composition — a document arranging other claims"
            else:
                produces = "a claim set"
            answered = "the referee runs it" if s.automatic else "answered by its player"
            instr = ""
            p = proc.path.parent / (s.instructions or "")
            if s.instructions and p.is_file():
                instr = (f"<details><summary>Instructions</summary><pre>"
                         f"{esc(p.read_text(encoding='utf-8'))}</pre></details>")
            cmd = (f" <span class='pill'>command</span> <code>{esc(s.command)}</code>" if s.command else "")
            out.append(
                f"<article class='card' id='{step_anchor(s.id)}' style='--rail:{ROLE_TONE.get(stype)}'>"
                f"<div class='hd'><span class='t'>{esc(step_name(s))}</span> "
                f"<span class='muted small'>{esc(answered)}</span></div>"
                f"<p class='prov'>{esc(s.question)}</p>"
                f"<p class='small'><b>Reads:</b> {reads}. <b>Produces:</b> {produces}.{cmd}</p>{instr}</article>")
    return "\n".join(out) + "</section>"


def _input_phrase(tok: str) -> str:
    if "/" in tok or "." in tok:
        return "the seed corpus" if "seed" in tok else esc(tok)
    if tok in SET_PHRASE:
        return SET_PHRASE[tok]
    if ":" in tok:
        sub, step = tok.split(":", 1)
        return f"<a href='#{step_anchor(step)}'>{esc(noun(step))}</a>"
    return f"<a href='#{step_anchor(tok)}'>{esc(noun(tok))}</a>"


# ── standards and the ledger ────────────────────────────────────────────────
def _standards() -> str:
    std = yaml.safe_load((Path(__file__).resolve().parent.parent / "standards.yaml").read_text(encoding="utf-8"))
    rows = "".join(f"<tr><td>{tag(t)}</td><td class='small'>{esc('; '.join(f'{k}: {v}' for k, v in m.items()))}</td></tr>"
                   for t, m in std["types"].items())
    rels = "".join(f"<tr><td><code>{esc(r)}</code></td><td class='small'>{esc('; '.join(f'{k}: {v}' for k, v in m.items()))}</td></tr>"
                   for r, m in std["relations"].items())
    recs = "".join(f"<tr><td><code>{esc(k)}</code></td><td class='small'>{esc('; '.join(f'{a}: {b}' for a, b in m.items()))}</td></tr>"
                   for k, m in std.items() if k in ("process", "step", "run", "version", "answerer"))
    return ("<section><h2 id='standards'>Standards</h2>"
            "<p class='sec-note'>How this vocabulary maps onto established ones</p>"
            "<p>Kept from the start and exported with every version. Where a standard does not fit, "
            "the note says so.</p>"
            f"<h3>Records</h3><div class='wrap'><table>{recs}</table></div>"
            f"<h3>Claim types</h3><div class='wrap'><table>{rows}</table></div>"
            f"<h3>Relations</h3><div class='wrap'><table>{rels}</table></div></section>")


def _ledger(proc, store, facts: Facts) -> str:
    rows = []
    for stype in proc.subjects:
        for sid in proc.subject_ids(stype):
            for r in store.ledger(sid):
                answerer = "the referee" if r.get("automatic") else facts.by_phrase(r.get("by"))
                rows.append((r["answered"], f"<tr><td class='mono'>{esc(r['answered'])}</td>"
                             f"<td>{esc(facts.name(sid))}</td>"
                             f"<td>{esc(step_name(proc.steps[r['step']]))} v{r['v']}</td>"
                             f"<td>{esc(answerer)}</td>"
                             f"<td class='small muted'>{esc(r.get('note'))}</td></tr>"))
    rows.sort(reverse=True)
    return ("<section><h2 id='ledger'>The ledger</h2>"
            "<p class='sec-note'>The raw append-only record, newest first — for audit</p>"
            "<div class='wrap'><table><tr><th>answered</th><th>player</th><th>step</th>"
            "<th>who answered</th><th>note</th></tr>" + "".join(r for _, r in rows) + "</table></div></section>")

