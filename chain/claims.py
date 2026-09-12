"""The one schema every artifact shares: a claim set.

    {"claims":   [{"id", "type", "text", "by", "about"?, "verdict"?, "evidence"?}],
     "edges":    [{"from", "to", "rel"}],
     "sections": [{"title", "claims": [refs]}]}          # compositions only

A claim's global id is `player:step:id`; inside its own artifact the local id suffices. A
reference is a claim (`juniper:study:r1`) or a whole artifact (`juniper:paper`). An answer may
only refer to what its request staged, so a player cannot cite what it was not shown.

A paper, a proposal, a review, a funding decision and a person's verdict are all claim sets.
A review is assessments about claims; a decision is a claim with a verdict about an artifact.
The vocabulary is small on purpose and mapped to standards in standards.yaml.
"""

from __future__ import annotations

import json
from pathlib import Path

from .process import Step, sha

TYPES = ("question", "hypothesis", "prediction", "method", "result", "interpretation", "scope",
         "assessment", "decision", "step")
RELATIONS = ("answers", "derived-from", "tests", "supports", "contradicts", "part-of",
             "replicates", "cites", "assesses", "decides")
JUDGING = ("assessment", "decision")
OVERALL = ("accept", "reject", "partial")


def gid(subject: str, step: str, local: str) -> str:
    return f"{subject}:{step}:{local}"


def load(vdir: Path) -> dict | None:
    p = Path(vdir) / "claims.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def staged(request_dir: Path) -> dict[str, dict]:
    """Every artifact the request staged: {player:step: claim set}."""
    out = {}
    for cj in (request_dir / "in").rglob("claims.json"):
        parts = cj.parent.relative_to(request_dir / "in").parts
        if len(parts) >= 2:
            out[f"{parts[0]}:{parts[1]}"] = json.loads(cj.read_text(encoding="utf-8"))
    return out


def refs_in(request_dir: Path) -> set[str]:
    """Every reference an answer to this request may make: staged claims and artifacts."""
    out = set()
    for ref, cs in staged(request_dir).items():
        out.add(ref)
        sub, step = ref.split(":", 1)
        for c in cs.get("claims") or []:
            out.add(gid(sub, step, c["id"]))
    return out


def validate(step: Step, subject: str, ans, known: set[str], manifest: dict) -> list[str]:
    if not isinstance(ans, dict) or not isinstance(ans.get("claims"), list):
        return ["an answer is {claims: [...]} (edges and sections optional)"]
    out, local = [], set()
    for c in ans["claims"]:
        cid = c.get("id")
        if not cid or cid in local:
            out.append(f"claim {cid!r}: missing or duplicate id")
        local.add(cid)
        if c.get("type") not in TYPES:
            out.append(f"{cid}: type {c.get('type')!r} not one of {TYPES}")
        elif step.emits and c["type"] not in step.emits:
            out.append(f"{cid}: this step emits {step.emits}, not {c['type']!r}")
        if not (c.get("text") or "").strip():
            out.append(f"{cid}: no text")
        if c.get("type") in JUDGING:
            if not c.get("about"):
                out.append(f"{cid}: an {c['type']} says what it is about")
            allowed = set(step.verdicts) | {"unconsidered"} | set(OVERALL)
            if c.get("verdict") not in allowed:
                out.append(f"{cid}: verdict {c.get('verdict')!r} not one of {sorted(allowed)}")
    mine = {gid(subject, step.id, l) for l in local} | {f"{subject}:{step.id}"}
    ok = known | mine | ({"process"} | {f"step:{s}" for s in manifest.get("steps", [])}
                          if step.judges == "process" else set())

    def ref_ok(r):
        return r in ok or (r.count(":") == 0 and gid(subject, step.id, r) in ok)

    for c in ans["claims"]:
        for r in c.get("about") or []:
            if not ref_ok(r):
                out.append(f"{c.get('id')}: about {r!r}, which this request did not stage")
    for e in ans.get("edges") or []:
        if e.get("rel") not in RELATIONS:
            out.append(f"edge {e}: rel not one of {RELATIONS}")
        for end in ("from", "to"):
            if not ref_ok(e.get(end, "")):
                out.append(f"edge {e}: {end} {e.get(end)!r} not staged")
    for s in ans.get("sections") or []:
        for r in s.get("claims") or []:
            if not ref_ok(r):
                out.append(f"section {s.get('title')!r}: {r!r} not staged")
    if step.judges:
        items = manifest.get("items") or {}
        targets = manifest.get("targets") or []
        judged = [c for c in ans["claims"] if c.get("type") == "assessment"]
        considered = sum(1 for c in judged if c.get("verdict") != "unconsidered")
        decisions = {a: c for c in ans["claims"] if c.get("type") == "decision" for a in c.get("about") or []}
        for t in targets:
            if t not in decisions:
                out.append(f"a judging answer carries one decision about {t}")
            elif decisions[t].get("verdict") not in OVERALL:
                out.append(f"the decision about {t}: verdict is one of {OVERALL}")
            elif items and considered < len(items) and decisions[t]["verdict"] != "partial":
                out.append(f"{considered} of {len(items)} items considered: the decisions are `partial`")
    return out


def _sha(c: dict) -> str:
    return c.get("sha") or sha(json.dumps(c, sort_keys=True).encode())


def items(targets: list[tuple[str, dict]], request_dir: Path | None) -> dict[str, dict]:
    """What a judging step judges, as {ref: {sha, text, of: target}}.

    A step's own claims are its items. A composition (a proposal, a paper, a journal's
    submissions) has none of its own: its items are the claims its sections reference,
    followed through staged artifacts — so a reviewer judges the hypotheses a proposal is made
    of, and a journal judges the claims of every paper submitted, not the wrappers. The
    process, judged by a ruling, has one item per step."""
    out = {}
    st = staged(request_dir) if request_dir else {}

    def claims_of(ref):
        sub, step = ref.split(":", 1)
        return {gid(sub, step, c["id"]): c for c in (st.get(ref) or {}).get("claims") or []}

    def walk(target, cs, seen):
        for c in cs.get("claims") or []:
            out[f"{target}:{c['id']}"] = {"sha": _sha(c), "text": c.get("text", ""), "of": target}
        for s in cs.get("sections") or []:
            for ref in s.get("claims") or []:
                if ref.count(":") == 2:
                    c = claims_of(ref.rsplit(":", 1)[0]).get(ref)
                    if c:
                        out[ref] = {"sha": _sha(c), "text": c.get("text", ""), "of": target}
                elif ref in st and ref not in seen:
                    walk(ref, st[ref], seen | {ref})

    for target, judged in targets:
        if target == "process":
            for c in judged["claims"]:
                out[f"step:{c['id']}"] = {"sha": c["sha"], "text": c["text"], "of": "process"}
        else:
            walk(target, judged, {target})
    return out


def skeleton(step: Step, targets: list[str], its: dict[str, dict], prior: dict | None) -> dict:
    """Assessments pre-filled for a player: `unconsidered`, or carried from the prior answer
    where the judged claim is unchanged; one decision per judged artifact."""
    prior_by_about = {c["about"][0]: c for c in (prior or {}).get("claims") or []
                      if c.get("type") == "assessment" and c.get("about")}
    prior_hashes = (prior or {}).get("item_hashes") or {}
    claims = []
    for ref, it in its.items():
        p = prior_by_about.get(ref)
        if p and prior_hashes.get(ref) == it["sha"]:
            claims.append(dict(p, carried=True))
        else:
            claims.append({"id": "a-" + ref.replace(":", "-"), "type": "assessment", "about": [ref],
                           "of": it["of"], "verdict": "unconsidered", "text": "", "judged": it["text"][:160]})
    for t in targets:
        claims.append({"id": "overall" if len(targets) == 1 else "overall-" + t.replace(":", "-"),
                       "type": "decision", "about": [t], "verdict": "partial", "text": ""})
    return {"claims": claims, "item_hashes": {r: it["sha"] for r, it in its.items()},
            "_per_item": step.verdicts + ["unconsidered"], "_overall": list(OVERALL)}
