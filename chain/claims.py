"""The one schema every artifact shares: a claim set.

    {"claims":   [{"id", "type", "text", "by", "about"?, "verdict"?, "evidence"?}],
     "edges":    [{"from", "to", "rel"}],
     "sections": [{"title", "claims": [refs]}]}          # compositions only

A claim's global id is `subject:step:id`; inside its own artifact the local id suffices. A
reference is a claim (`alpha:study:r1`) or a whole artifact (`alpha:paper`). An answer may
only refer to what its request staged, so an agent cannot cite what it was not shown.

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


def refs_in(request_dir: Path) -> set[str]:
    """Every reference an answer to this request may make: staged claims and artifacts."""
    out = set()
    for cj in (request_dir / "in").rglob("claims.json"):
        sub, step = cj.parent.relative_to(request_dir / "in").parts[:2]
        out.add(f"{sub}:{step}")
        for c in (json.loads(cj.read_text(encoding="utf-8")).get("claims") or []):
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
        judged = [c for c in ans["claims"] if c.get("type") == "assessment"]
        considered = sum(1 for c in judged if c.get("verdict") != "unconsidered")
        overall = [c for c in ans["claims"] if c.get("type") == "decision"]
        if not overall:
            out.append("a judging answer carries one decision claim about the whole artifact")
        elif overall[0].get("verdict") not in OVERALL:
            out.append(f"the decision's verdict is one of {OVERALL}")
        elif items and considered < len(items) and overall[0]["verdict"] != "partial":
            out.append(f"{considered} of {len(items)} items considered: the decision is `partial`")
    return out


def _sha(c: dict) -> str:
    return c.get("sha") or sha(json.dumps(c, sort_keys=True).encode())


def items(judged: dict, target: str, request_dir: Path | None) -> dict[str, dict]:
    """What a judging step judges, as {ref: {sha, text}}.

    A step's own claims are the items. A composition (a proposal, a paper) has none of its
    own: its items are the claims its sections reference, read from the request's staged
    inputs — so a reviewer judges the hypotheses a proposal is made of, not the wrapper.
    The process, judged by a ruling, has one item per step."""
    out = {}
    if target == "process":
        return {f"step:{c['id']}": {"sha": c["sha"], "text": c["text"]} for c in judged["claims"]}
    for c in judged.get("claims") or []:
        out[f"{target}:{c['id']}"] = {"sha": _sha(c), "text": c.get("text", "")}
    if not out and judged.get("sections") and request_dir:
        staged = {}
        for cj in (request_dir / "in").rglob("claims.json"):
            sub, step = cj.parent.relative_to(request_dir / "in").parts[:2]
            for c in json.loads(cj.read_text(encoding="utf-8")).get("claims") or []:
                staged[gid(sub, step, c["id"])] = c
        for s in judged["sections"]:
            for ref in s.get("claims") or []:
                if ref in staged:
                    out[ref] = {"sha": _sha(staged[ref]), "text": staged[ref].get("text", "")}
    return out


def skeleton(step: Step, target: str, its: dict[str, dict], prior: dict | None) -> dict:
    """Assessments pre-filled for a person: `unconsidered`, or carried from the prior answer
    where the judged claim is unchanged."""
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
                           "verdict": "unconsidered", "text": "", "judged": it["text"][:160]})
    claims.append({"id": "overall", "type": "decision", "about": [target], "verdict": "partial", "text": ""})
    return {"claims": claims, "item_hashes": {r: it["sha"] for r, it in its.items()},
            "_per_item": step.verdicts + ["unconsidered"], "_overall": list(OVERALL)}
