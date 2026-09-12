"""Reading the record: resolve references to links and text (Refs), read each player's facts
from the store (Facts), and gather what every review or decision said about each claim."""

from __future__ import annotations

from .. import claims as C
from ..process import Process
from ..store import Store
from .theme import (JUDGE, art_id, claim_id, esc, step_anchor, step_name, title)


class Refs:
    """Resolves a reference to a link and, for a claim, to its text and type — from the store."""

    def __init__(self, proc: Process, store: Store):
        self.proc, self.store = proc, store
        self.claims: dict[str, dict] = {}          # gid → claim, latest version wins
        for stype in proc.subjects:
            for sid in proc.subject_ids(stype):
                for step in proc.steps_for(stype):
                    for v in store.versions(sid, step.id):     # ascending: latest overwrites
                        for c in (C.load(store.version_dir(sid, step.id, v)) or {}).get("claims") or []:
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


# ── reading the record ──────────────────────────────────────────────────────
class Facts:
    """Everything the cards say about a player, read once from the store."""

    def __init__(self, proc: Process, store: Store):
        self.proc, self.store = proc, store
        self.cited: dict[str, int] = {}            # player → cites edges landing in its claims
        self.pubs: list[dict] = []                 # {id, article, team, journal}
        for stype in proc.subjects:
            for sid in proc.subject_ids(stype):
                for step in proc.steps_for(stype):
                    v = store.latest(sid, step.id)
                    if v is None:
                        continue
                    cs = C.load(store.version_dir(sid, step.id, v)) or {}
                    for e in cs.get("edges") or []:
                        if e.get("rel") != "cites":
                            continue
                        to = e["to"] if ":" in e["to"] else C.gid(sid, step.id, e["to"])
                        owner = to.split(":")[0]
                        self.cited[owner] = self.cited.get(owner, 0) + 1
                    if step.id == "published":
                        for sec in cs.get("sections") or []:
                            pid = sec.get("id", "")
                            if pid.startswith("pub:"):
                                art = next((r for r in sec.get("claims") or [] if r.endswith(":paper")), None)
                                self.pubs.append({"id": pid, "article": art,
                                                  "team": art.split(":")[0] if art else None, "journal": sid})

    def cs(self, sid: str, step: str) -> dict:
        v = self.store.latest(sid, step)
        return (C.load(self.store.version_dir(sid, step, v)) or {}) if v else {}

    def name(self, sid: str) -> str:
        m = self.proc.meta(sid).get("name")
        if m:
            return m
        return {"library": "the library", "process": "the process"}.get(sid, sid)

    def by_phrase(self, by: str | None) -> str:
        if not by or by == "referee":
            return "the referee"
        if by.startswith("stub:"):
            return f"a stand-in for {self.name(by.split(':', 1)[1])}"
        return by

    def decisions_about(self, judge_step: str, target: str) -> list[dict]:
        """Every decision a judging step made about `target` (an artifact ref)."""
        out = []
        for sid in self.proc.subject_ids(self.proc.steps[judge_step].subject):
            for c in self.cs(sid, judge_step).get("claims") or []:
                if c.get("type") == "decision" and target in (c.get("about") or []):
                    out.append({"player": sid, "verdict": c.get("verdict"), "text": c.get("text", "")})
        return out

    def tally_of(self, judge_step: str, target: str) -> dict:
        out = {}
        for sid in self.proc.subject_ids(self.proc.steps[judge_step].subject):
            for c in self.cs(sid, judge_step).get("claims") or []:
                if c.get("type") == "assessment" and c.get("of") == target and c.get("verdict") != "unconsidered":
                    out[c["verdict"]] = out.get(c["verdict"], 0) + 1
        return out

    def study_run(self, sid: str) -> bool:
        return any(c.get("type") in ("result", "interpretation") for c in self.cs(sid, "study").get("claims") or [])

    def funded(self, sid: str) -> dict | None:
        d = self.decisions_about("select", f"{sid}:proposal")
        return d[0] if d else None


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


