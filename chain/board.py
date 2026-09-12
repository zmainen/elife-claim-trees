"""The board: one static page that shows the process, every artifact, every request, and the
standards mapping. Generated from the store; nothing on it is typed by hand. No scripts, no
external resources — the page is an artifact like the rest and should open anywhere."""

from __future__ import annotations

import html
import json
from pathlib import Path

import yaml

from . import claims as C
from .process import Process, is_ref
from .status import status
from .store import Store

TONE = {"current": "#2f855a", "stale": "#b7791f", "blocked": "#c05621", "pending": "#2b6cb0", "absent": "#a0aec0"}
TYPE_ORDER = ("question", "scope", "hypothesis", "prediction", "method", "result", "interpretation",
              "assessment", "decision", "step")
TYPE_TONE = {"question": "#805ad5", "scope": "#718096", "hypothesis": "#3182ce", "prediction": "#4299e1",
             "method": "#38a169", "result": "#dd6b20", "interpretation": "#d69e2e", "assessment": "#e53e3e",
             "decision": "#c53030", "step": "#4a5568"}
CSS = """
body{font:14px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#1a202c;background:#f7fafc;margin:0;padding:0 0 4rem}
main{max-width:1180px;margin:0 auto;padding:1.5rem}
h1{font-size:1.6rem;margin:.2rem 0}h2{font-size:1.2rem;margin:2.2rem 0 .6rem;border-bottom:1px solid #e2e8f0;padding-bottom:.3rem}
h3{font-size:1rem;margin:1.4rem 0 .4rem}p.lead{color:#4a5568;max-width:70ch}
.wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;vertical-align:top;padding:.35rem .5rem;border-bottom:1px solid #edf2f7}
th{font-weight:600;color:#4a5568;font-size:11px;text-transform:uppercase;letter-spacing:.04em}
code,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px}
.chip{display:inline-block;padding:0 .5em;border-radius:1em;color:#fff;font-size:11px;line-height:1.7;vertical-align:middle}
.cell{white-space:nowrap}.muted{color:#718096}.small{font-size:12px}
details{margin:.3rem 0}summary{cursor:pointer;color:#2b6cb0}pre{background:#edf2f7;padding:.6rem;border-radius:4px;overflow-x:auto;font-size:12px;white-space:pre-wrap}
.art{background:#fff;border:1px solid #e2e8f0;border-radius:6px;padding:.8rem 1rem;margin:.8rem 0}
.tag{display:inline-block;padding:0 .4em;border-radius:3px;color:#fff;font-size:10px;text-transform:uppercase;letter-spacing:.05em;line-height:1.7}
.legend span{margin-right:1rem}svg text{font:11px -apple-system,Segoe UI,sans-serif}
"""


def esc(s) -> str:
    return html.escape(str(s if s is not None else ""))


def chip(state: str, text: str | None = None) -> str:
    return f'<span class="chip" style="background:{TONE.get(state, "#718096")}">{esc(text or state)}</span>'


def tag(t: str) -> str:
    return f'<span class="tag" style="background:{TYPE_TONE.get(t, "#718096")}">{esc(t)}</span>'


def board(proc: Process, store: Store, root: Path) -> str:
    st = status(proc, store, root)
    parts = [f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
             f"<title>{esc(proc.name)} · board</title><style>{CSS}</style><main>",
             f"<h1>{esc(proc.name)}</h1>",
             f'<p class="lead">The process, every artifact it has produced, every request waiting for an answer, '
             f'and where each fact came from. Generated from <code>store/</code>; process <code>{proc.hash}</code>. '
             f'{len(proc.steps)} steps over {", ".join(proc.subjects)}.</p>',
             _process(proc), _matrix(proc, st), _pending(proc, store, root, st)]
    for stype in proc.subjects:
        for sid in proc.subject_ids(stype):
            parts.append(_subject(proc, store, root, sid, st[sid]))
    parts += [_standards(), _ledger(proc, store), "</main>"]
    return "\n".join(parts).replace("<table>", '<div class="wrap"><table>').replace("</table>", "</table></div>")


def _process(proc: Process) -> str:
    rows = []
    for sid in proc.order():
        s = proc.steps[sid]
        ins = ", ".join(f"<code>{esc(t)}</code>" for t in s.inputs) or "—"
        what = (f"judges <code>{esc(s.judges)}</code> · verdicts {esc(', '.join(s.verdicts))}" if s.judges
                else (f"emits {' '.join(tag(t) for t in s.emits)}" if s.emits else "composes"))
        instr = ""
        if s.instructions and (proc.path.parent / s.instructions).is_file():
            instr = (f"<details><summary>instructions</summary><pre>"
                     f"{esc((proc.path.parent / s.instructions).read_text(encoding='utf-8'))}</pre></details>")
        cmd = f"<div class='mono muted small'>{esc(s.command)}</div>" if s.command else ""
        rows.append(f"<tr><td class='mono'>{esc(s.id)}</td><td>{esc(s.subject)}</td><td>{esc(s.worker)}</td>"
                    f"<td>{esc(s.question)}{cmd}{instr}</td><td>{ins}</td><td>{what}</td></tr>")
    return ("<h2>The process</h2><p class='lead'>A step is a question asked of a subject. It reads only what is "
            "staged into its request and writes one claim set. <em>code</em> answers itself; <em>model</em> and "
            "<em>human</em> steps wait for an answer.</p><table><tr><th>step</th><th>subject</th><th>worker</th>"
            "<th>question · instructions</th><th>inputs</th><th>answer</th></tr>" + "".join(rows) + "</table>")


def _matrix(proc: Process, st: dict) -> str:
    out = ["<h2>Where things stand</h2><p class='lead'>Computed from hashes, never stored. A judgement is shown "
           "beside the version it judged and says whether it still applies; the scheme column is the newest "
           "current ruling on the process.</p>",
           '<p class="legend small">' + " ".join(chip(s) for s in TONE) + "</p>"]
    for stype in proc.subjects:
        steps = proc.steps_for(stype)
        out.append(f"<h3>{esc(stype)}</h3><table><tr><th>subject</th>" +
                   "".join(f"<th class='mono'>{esc(s.id)}</th>" for s in steps) + "</tr>")
        for sid in proc.subject_ids(stype):
            cells = []
            for s in steps:
                c = st[sid][s.id]
                bits = [chip(c["state"])]
                if c.get("v"):
                    bits.append(f"<div class='small'>v{c['v']} · {esc(c.get('by'))}</div>")
                for d in c.get("assessed") or []:
                    tally = ", ".join(f"{k} {v}" for k, v in sorted(d["tally"].items())) or "no items"
                    bits.append(f"<div class='small'><span class='mono'>{esc(d['step'])}</span> by {esc(d['by'])}: "
                                f"<b>{esc(d['verdict'])}</b> ({d['considered']}/{d['of']}; {esc(tally)})"
                                + ("" if d["applies"] else " <span class='muted'>— judged an earlier version</span>") + "</div>")
                if c.get("moved"):
                    bits.append(f"<div class='small muted'>moved: {esc(', '.join(c['moved'][:3]))}</div>")
                if c.get("blocked_by"):
                    bits.append(f"<div class='small muted'>upstream: {esc(', '.join(c['blocked_by']))}</div>")
                bits.append(f"<div class='small muted'>scheme: {esc(c['scheme'])}</div>")
                cells.append("<td class='cell'>" + "".join(bits) + "</td>")
            out.append(f"<tr><td class='mono'>{esc(sid)}</td>{''.join(cells)}</tr>")
        out.append("</table>")
    return "\n".join(out)


def _pending(proc, store, root, st) -> str:
    rows = []
    for sid, cells in st.items():
        for step_id, c in cells.items():
            if c.get("state") == "pending" or c.get("request_open"):
                q = store.request_dir(sid, step_id) / "QUESTION.md"
                rows.append(f"<div class='art'><b class='mono'>{esc(sid)} · {esc(step_id)}</b> · "
                            f"waiting for {esc(proc.steps[step_id].worker)}<pre>"
                            f"{esc(q.read_text(encoding='utf-8') if q.is_file() else '')}</pre></div>")
    return ("<h2>Open requests</h2><p class='lead'>What a person or an agent could answer now. Each is a "
            "directory: the question, the instructions, everything it may read, and a skeleton.</p>"
            + ("".join(rows) or "<p class='muted'>None.</p>"))


def _subject(proc, store, root, sid, cells) -> str:
    out = [f"<h2>{esc(sid)}</h2>", _graph(proc, store, sid)]
    for step in proc.steps_for(proc.steps[next(iter(cells))].subject):
        v = store.latest(sid, step.id)
        if v is None:
            continue
        vd = store.version_dir(sid, step.id, v)
        rec = store.run_record(sid, step.id, v) or {}
        cs = C.load(vd) or {}
        ins = "".join(f"<li><code>{esc(i.get('ref') or i['path'])}</code> {esc(i['kind'])} "
                      f"<span class='mono muted'>{esc('v%d' % i['v'] if i.get('v') else i['sha'])}</span></li>"
                      for i in rec.get("in", []))
        out.append(f"<div class='art'><b class='mono'>{esc(step.id)}</b> v{v} · {esc(step.worker)} · "
                   f"{esc(rec.get('by'))} · {esc(rec.get('answered'))} {chip(cells[step.id]['state'])}"
                   f"<div class='small muted'>{esc(step.question)} · <code>{esc(rec.get('out', {}).get('path'))}</code></div>"
                   f"<details><summary>read from ({len(rec.get('in', []))})</summary><ul class='small'>{ins}</ul></details>"
                   + _claims(sid, step.id, cs) + "</div>")
    return "\n".join(out)


def _claims(sid, step_id, cs) -> str:
    out = []
    if cs.get("claims"):
        rows = []
        for c in cs["claims"]:
            extra = ""
            if c.get("about"):
                extra += f"<div class='small muted'>about {esc(', '.join(c['about']))}</div>"
            if c.get("verdict"):
                extra += f"<div class='small'><b>{esc(c['verdict'])}</b></div>"
            if c.get("carried"):
                extra += "<div class='small muted'>carried from the previous version</div>"
            rows.append(f"<tr><td class='mono'>{esc(C.gid(sid, step_id, c['id']))}</td><td>{tag(c.get('type'))}</td>"
                        f"<td>{esc(c.get('text'))}{extra}</td><td class='small muted'>{esc(c.get('by'))}</td></tr>")
        out.append("<table><tr><th>claim</th><th>type</th><th>text</th><th>by</th></tr>" + "".join(rows) + "</table>")
    if cs.get("edges"):
        out.append("<p class='small'>" + " · ".join(
            f"<code>{esc(e['from'])}</code> <b>{esc(e['rel'])}</b> <code>{esc(e['to'])}</code>" for e in cs["edges"]) + "</p>")
    if cs.get("sections"):
        out.append("<ul class='small'>" + "".join(
            f"<li><b>{esc(s['title'])}</b>: {', '.join(f'<code>{esc(r)}</code>' for r in s['claims'])}</li>"
            for s in cs["sections"]) + "</ul>")
    return "".join(out)


def _graph(proc, store, sid) -> str:
    """Every claim of this subject's latest versions, laid out by type, with its edges."""
    nodes, edges, said = {}, [], {}          # said: what assessments say about each claim
    for step in proc.steps_for(_stype(proc, sid)):
        v = store.latest(sid, step.id)
        if v is None:
            continue
        cs = C.load(store.version_dir(sid, step.id, v)) or {}
        for c in cs.get("claims") or []:
            if c.get("type") in C.JUDGING:
                for a in c.get("about") or []:
                    said.setdefault(a, []).append((step.id, c.get("verdict"), c.get("text", "")))
            else:
                nodes[C.gid(sid, step.id, c["id"])] = c
        for e in cs.get("edges") or []:
            edges.append((_g(sid, step.id, e["from"]), _g(sid, step.id, e["to"]), e["rel"]))
    if not nodes:
        return ""
    cols = [t for t in TYPE_ORDER if any(c.get("type") == t for c in nodes.values())]
    pos, ys = {}, {t: 0 for t in cols}
    W, H, colw, rowh = 1140, 0, 1140 / max(len(cols), 1), 40
    for g, c in nodes.items():
        t = c.get("type")
        pos[g] = (cols.index(t) * colw + 6, 30 + ys[t] * rowh)
        ys[t] += 1
        H = max(H, 30 + ys[t] * rowh)
    svg = [f'<svg viewBox="0 0 {W} {H + 10}" width="100%" style="background:#fff;border:1px solid #e2e8f0;border-radius:6px">']
    for i, t in enumerate(cols):
        svg.append(f'<text x="{i * colw + 6}" y="16" fill="{TYPE_TONE[t]}" font-weight="600">{esc(t)}</text>')
    for a, b, rel in edges:
        if a in pos and b in pos:
            (x1, y1), (x2, y2) = pos[a], pos[b]
            color = "#e53e3e" if rel == "contradicts" else ("#2f855a" if rel == "supports" else "#a0aec0")
            svg.append(f'<line x1="{x1 + colw - 14}" y1="{y1 + 12}" x2="{x2}" y2="{y2 + 12}" stroke="{color}" '
                       f'stroke-width="1.2" opacity=".7"><title>{esc(a)} {esc(rel)} {esc(b)}</title></line>')
    for g, (x, y) in pos.items():
        c = nodes[g]
        verdicts = " · ".join(f"{s.split('-')[0]}: {v}" for s, v, _ in said.get(g, []))
        title = c.get("text", "") + "".join(f"\n— {s}: {v}. {t}" for s, v, t in said.get(g, []))
        svg.append(f'<rect x="{x}" y="{y}" width="{colw - 16}" height="32" rx="3" fill="{TYPE_TONE[c.get("type")]}" opacity=".12"/>'
                   f'<text x="{x + 4}" y="{y + 13}" font-weight="600"><title>{esc(title)}</title>{esc(g.split(":", 2)[2])}'
                   f'  <tspan font-weight="400" fill="#4a5568">{esc(c.get("text", "")[:int(colw / 7) - len(c["id"]) - 2])}</tspan></text>'
                   f'<text x="{x + 4}" y="{y + 26}" fill="#718096"><title>{esc(title)}</title>{esc(verdicts[:int(colw / 5.5)])}</text>')
    svg.append("</svg>")
    return ("<p class='small muted'>Every claim of this subject's latest versions, by type, with what each review "
            "and decision said about it beneath. Lines are edges: green supports, red contradicts, grey the rest. "
            "Hover a claim for its text and every verdict on it.</p>" + "".join(svg))


def _stype(proc, sid):
    return next(t for t in proc.subjects if sid in proc.subject_ids(t))


def _g(sid, step, ref):
    return ref if ":" in ref else C.gid(sid, step, ref)


def _standards() -> str:
    std = yaml.safe_load((Path(__file__).resolve().parent / "standards.yaml").read_text(encoding="utf-8"))
    rows = "".join(f"<tr><td>{tag(t)}</td><td>{esc('; '.join(f'{k}: {v}' for k, v in m.items()))}</td></tr>"
                   for t, m in std["types"].items())
    rels = "".join(f"<tr><td><code>{esc(r)}</code></td><td>{esc('; '.join(f'{k}: {v}' for k, v in m.items()))}</td></tr>"
                   for r, m in std["relations"].items())
    recs = "".join(f"<tr><td><code>{esc(k)}</code></td><td>{esc('; '.join(f'{a}: {b}' for a, b in m.items()))}</td></tr>"
                   for k, m in std.items() if k in ("process", "step", "run", "version", "worker"))
    return ("<h2>Standards</h2><p class='lead'>Kept as a mapping from step zero (<code>chain/standards.yaml</code>) and "
            "exported with every version. Where a standard does not fit, the note says so.</p>"
            f"<h3>records</h3><table>{recs}</table><h3>claim types</h3><table>{rows}</table>"
            f"<h3>relations</h3><table>{rels}</table>")


def _ledger(proc, store) -> str:
    rows = []
    for stype in proc.subjects:
        for sid in proc.subject_ids(stype):
            for r in store.ledger(sid):
                rows.append((r["answered"], f"<tr><td class='mono'>{esc(r['answered'])}</td><td class='mono'>{esc(sid)}</td>"
                             f"<td class='mono'>{esc(r['step'])} v{r['v']}</td><td>{esc(r['worker'])}</td><td>{esc(r['by'])}</td>"
                             f"<td class='small muted'>{esc(r.get('note'))}</td></tr>"))
    rows.sort(reverse=True)
    return ("<h2>Ledger</h2><table><tr><th>answered</th><th>subject</th><th>version</th><th>worker</th><th>by</th><th>note</th></tr>"
            + "".join(r for _, r in rows) + "</table>")
