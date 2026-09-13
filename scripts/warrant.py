#!/usr/bin/env python3
"""How well does the tree support a claim — the dossier, the rule floor, and the comparison.

`warrant` is what the tree gives a reader grounds to believe, as distinct from what the paper
says (`confidence`) and from how many readers agreed (`READER_CONFIDENCE`). Issue #126, and the
design note docs/design/2026-09-13-warrant.md, ask for three mechanical pieces here, and one
model judgement that lives in the `warrant` layer (extract/prompts/warrant.md):

  dossier(paper)        Per claim, what the tree holds about its support — role, stance, the
                        outcomes on its predictions, the controls that validate it, the
                        alternatives it rules out, its reproduction records and their
                        verification provenance, what it requires and is part of, the claims
                        that support or extend it, and the assertion's confidence. Plain data,
                        no judgement in it.

  warrant_rule(d)       The note's version-1 rule, by role, over one claim's dossier. Returns
                        the level and the inputs that fired. It is the floor the model's reading
                        is scored against — and, per the ruling, it is shown to the model only
                        *after* it judges, never before.

  resolve(paper)        Runs the rule over the whole tree, in dependency order, so propagation
                        (a claim is bounded above by the weakest claim it requires) and the
                        minimum a synthesis takes over what it interprets can read their
                        neighbours' resolved levels.

  report(paper)         The comparison the note's §"How the rule is evaluated" asks for: the
                        model's level beside the rule's floor for every claim, agreement by
                        role, and every disagreement with the model's `why` beside the rule's
                        inputs. Reads the recorded `warrant.v<N>.json` and writes
                        `runs/<paper>/warrant.v<N>.report.md`.

The rule is deliberately coarse (four levels, one a flag), because a fine rule with no
adjudicated readings behind it is a guess with more digits. It is scored against the model's
reading, not the other way round.

Usage:
  python3 scripts/warrant.py <paper>            # dossier + rule floor, one line per claim
  python3 scripts/warrant.py <paper> --report   # write the model-vs-floor comparison
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prediction_outcome  # noqa: E402
from export_mira import CLAIMS_DIR, first_assertion, load_paper, relations  # noqa: E402

RULE_VERSION = 1

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The graded levels, weakest first, so `min` is the weakest and a cap is a slice. Predictions
# (confirmed/refuted/untested) and alternatives (ruled-out/open) carry their own vocabularies
# and never enter this ordering.
GRADED = ("contested", "weak", "moderate", "strong")
_RANK = {lv: i for i, lv in enumerate(GRADED)}

# The roles whose warrant is graded from the paper's assertion and the evidence on it. A role
# outside every branch of the rule (literature-context is the one in the corpus) is graded here
# too: it is an asserted claim with a confidence and, usually, nothing that checks it.
GRADED_ROLES = {"empirical", "control", "methodological", "scope", "literature-context"}
INTERPRETIVE_ROLES = {"synthesis", "interpretation"}

VOCABULARY = {
    "prediction": ("confirmed", "refuted", "untested"),
    "alternative": ("ruled-out", "open"),
    "graded": GRADED,
}


def vocabulary_for(role: str, stance: str) -> tuple[str, ...]:
    """The warrant words a claim of this role and stance may take — what the prompt offers it."""
    if role == "prediction":
        return VOCABULARY["prediction"]
    if _is_alternative(role, stance):
        return VOCABULARY["alternative"]
    return VOCABULARY["graded"]


def _is_alternative(role: str, stance: str) -> bool:
    """An alternative is a hypothesis the paper raises to reject or merely entertains (§rule)."""
    return role == "hypothesis" and stance in ("rejects", "entertains")


# ── the dossier: what the tree holds about a claim's support ──────────────────────────────


def _incoming(claims: list[dict]) -> dict[str, list[tuple[str, str]]]:
    """target slug → [(relation, source slug)] across the tree, both storage shapes."""
    inc: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
    for c in claims:
        for rel, tgt in relations(c):
            inc[tgt].append((rel, c["slug"]))
    return inc


def _verification(paper: str) -> dict[str, list[dict]]:
    """claim slug → the provenance entries that observed a run against it, where any exist.

    The record's `claim` field carries a bracketed qualifier for the several values checked
    against one claim (`… [fMRI β]`); the slug is what precedes it. A `verified` reproduction
    checks a number, and this is where the number was actually re-run and what it came to.
    """
    p = os.path.join(ROOT, "verification", paper, "provenance.json")
    if not os.path.isfile(p):
        return {}
    data = json.load(open(p, encoding="utf-8"))
    out: dict[str, list[dict]] = collections.defaultdict(list)
    for r in data.get("results", []):
        slug = (r.get("claim") or "").split(" [", 1)[0].strip()
        if slug:
            out[slug].append({"status": r.get("status"), "paper_value": r.get("paper_value"),
                              "reproduced_value": r.get("reproduced_value")})
    return out


def dossier(paper: str) -> dict[str, dict]:
    """Per claim, what the tree holds about its support. Plain data — no judgement in it.

    One dict per claim, keyed by slug. The identity keys (slug, role, stance, confidence,
    sentence) say what the claim is; the evidence keys say what stands behind it, and it is the
    non-empty ones the layer records as `warrant_from`.
    """
    claims = load_paper(paper)
    by_slug = {c["slug"]: c for c in claims}
    inc = _incoming(claims)
    prov = _verification(paper)
    outcomes = {it["prediction"]: it for it in prediction_outcome.scan([paper])}

    def prediction_outcome_of(slug: str) -> dict | None:
        it = outcomes.get(slug)
        if not it:
            return None
        outcome = ("refuted" if it["refutes"] else "confirmed" if it["confirms"]
                   else "untested")
        return {"outcome": outcome, "confirms": it["confirms"], "refutes": it["refutes"],
                "tests": it["tests"], "bucket": it["bucket"]}

    doss: dict[str, dict] = {}
    for c in claims:
        slug = c["slug"]
        a = first_assertion(c) or {}
        stance = a.get("stance") or "asserts"
        role = c.get("role")
        outgoing = list(relations(c))
        incoming = inc.get(slug, [])

        # The predictions this claim (a hypothesis) commits to: the targets it `entails`, plus
        # any claim that names it in `derived-from`. Each with the outcome the graph records.
        preds = {t for r, t in outgoing if r == "entails"}
        preds |= {src for r, src in incoming if r == "derived-from"}
        predictions = [{"slug": s, **(prediction_outcome_of(s) or {"outcome": "untested"})}
                       for s in sorted(preds) if by_slug.get(s, {}).get("role") == "prediction"]

        d = {
            "slug": slug,
            "role": role,
            "stance": stance,
            "confidence": a.get("confidence"),
            "sentence": " ".join((c.get("claim") or "").split()),
            # Evidence keys — the ones that "fire".
            "outcome": prediction_outcome_of(slug) if role == "prediction" else None,
            "predictions": predictions,
            "validated_by": sorted(src for r, src in incoming if r == "validates"),
            "rules_out": sorted(t for r, t in outgoing if r == "rules-out"),
            "reproductions": [{"status": r.get("status"),
                               "paper_value": r.get("paper_value"),
                               "reproduced_value": r.get("reproduced_value")}
                              for r in (c.get("reproductions") or [])],
            "verification": prov.get(slug, []),
            "requires": sorted(t for r, t in outgoing if r == "requires"),
            "part_of": sorted(t for r, t in outgoing if r == "part-of"),
            "interprets": sorted(t for r, t in outgoing if r == "interprets"),
            "supported_by": sorted(src for r, src in incoming if r == "supports"),
            "extended_by": sorted(src for r, src in incoming if r == "extends"),
            # The control or result that rules this claim out — the evidence behind an
            # alternative's ruled-out/open, and empty for a claim the paper asserts.
            "ruled_out_by": sorted(src for r, src in incoming if r == "rules-out"),
            # A cross-paper result that refutes this claim moves it to contested; within a
            # single tree this is always empty, and its emptiness is itself a finding (§inputs).
            "refuted_by_other_paper": sorted(
                src for r, src in incoming
                if r in ("refutes", "contradicts") and by_slug.get(src) is None),
        }
        doss[slug] = d
    return doss


# ── the rule floor: the note's version 1, by role ─────────────────────────────────────────


def _repro_statuses(d: dict) -> set[str]:
    return {r.get("status") for r in d.get("reproductions", [])}


def warrant_rule(d: dict, resolved: dict[str, str] | None = None) -> tuple[str, list[str]]:
    """The version-1 rule over one claim's dossier: the level, and the inputs that fired.

    `resolved` carries the levels the rest of the tree has already resolved to, which the two
    non-local branches read: propagation caps a graded claim at the weakest claim it requires,
    and a synthesis or interpretation takes the minimum over the claims it interprets. Every
    other branch is a function of the dossier alone, so a synthetic claim tests it without one.
    """
    resolved = resolved or {}
    role, stance = d["role"], d.get("stance") or "asserts"
    fired: list[str] = []

    # A prediction has an outcome, not a warrant (§rule, #28).
    if role == "prediction":
        o = d.get("outcome") or {}
        if o.get("confirms"):
            return "confirmed", [f"confirms:{s}" for s in o["confirms"]]
        if o.get("refutes"):
            return "refuted", [f"refutes:{s}" for s in o["refutes"]]
        return "untested", ([f"tests:{s}" for s in o.get("tests", [])] or ["no-test"])

    # An alternative is ruled-out when a rules-out edge reaches it, else open.
    if _is_alternative(role, stance):
        if d.get("ruled_out_by"):
            return "ruled-out", [f"ruled-out-by:{s}" for s in d["ruled_out_by"]]
        return "open", ["no-rules-out"]

    # A synthesis or interpretation takes the minimum over the claims it interprets.
    if role in INTERPRETIVE_ROLES:
        interpreted = [resolved[t] for t in d.get("interprets", [])
                       if resolved.get(t) in _RANK]
        if interpreted:
            lvl = min(interpreted, key=lambda x: _RANK[x])
            return lvl, [f"interprets:{t}={resolved[t]}" for t in d["interprets"]
                         if resolved.get(t) in _RANK]
        # Nothing graded to interpret: fall through to the graded branch on its own assertion.

    # A hypothesis is warranted by its predictions and its rivals.
    if role == "hypothesis":
        preds = d.get("predictions", [])
        confirmed = [p["slug"] for p in preds if p.get("outcome") == "confirmed"]
        refuted = [p["slug"] for p in preds if p.get("outcome") == "refuted"]
        if refuted:
            return "contested", [f"prediction-refuted:{s}" for s in refuted]
        if confirmed:
            fired = [f"prediction-confirmed:{s}" for s in confirmed]
            standing = _standing_rivals(d, resolved)
            if standing:
                return "moderate", fired + [f"rival-stands:{s}" for s in standing]
            return "strong", fired + (["rivals-ruled-out"] if _rivals(d, resolved) else [])
        return "weak", ["no-prediction-outcome"]

    # Empirical, control, methodological, scope (and any other asserted, graded claim).
    lvl, fired = _graded_rule(d)
    return _propagate(lvl, fired, d, resolved)


def _rivals(d: dict, resolved: dict[str, str]) -> list[str]:
    """Alternatives that address the same question as this hypothesis (§rule)."""
    # Matching is by the `addresses` question id the stance layer wrote on each side; a
    # hypothesis that carries none has no rivals to weigh here, which the report can note.
    return d.get("rivals", [])


def _standing_rivals(d: dict, resolved: dict[str, str]) -> list[str]:
    """Rivals to this hypothesis that were not ruled out — an alternative that still stands."""
    return [s for s in _rivals(d, resolved) if resolved.get(s) == "open"]


def _graded_rule(d: dict) -> tuple[str, list[str]]:
    """The graded branch: start from the assertion, move on the evidence on it (§rule)."""
    statuses = _repro_statuses(d)
    if "mismatch" in statuses or d.get("refuted_by_other_paper"):
        why = (["reproduction:mismatch"] if "mismatch" in statuses else [])
        why += [f"refuted-by:{s}" for s in d.get("refuted_by_other_paper", [])]
        return "contested", why
    if "verified" in statuses:
        return "strong", ["reproduction:verified"]
    if d.get("validated_by") and "partial" not in statuses:
        return "strong", [f"validated-by:{s}" for s in d["validated_by"]]
    if statuses == {"partial"} or (statuses and statuses <= {"partial"}):
        return "weak", ["reproduction:partial"]
    if d.get("confidence") in ("weak", "tentative") and not _has_check(d):
        return "weak", [f"confidence:{d['confidence']}", "unchecked"]
    checks = sorted(s for s in statuses if s) or ["asserted"]
    return "moderate", [f"reproduction:{s}" for s in checks] if statuses else ["asserted"]


def _has_check(d: dict) -> bool:
    """Whether anything in the tree checks this claim: a reproduction, a control, or a test."""
    return bool(d.get("reproductions") or d.get("validated_by") or d.get("verification"))


def _propagate(lvl: str, fired: list[str], d: dict, resolved: dict[str, str]) -> tuple[str, list[str]]:
    """Cap a graded claim's warrant at the weakest graded claim it requires (§propagation)."""
    caps = [(t, resolved[t]) for t in d.get("requires", []) if resolved.get(t) in _RANK]
    for t, req in caps:
        if _RANK[req] < _RANK[lvl]:
            lvl = req
            fired = fired + [f"bounded-by-requires:{t}={req}"]
    return lvl, fired


# ── resolving the whole tree, in dependency order ─────────────────────────────────────────


def _order(doss: dict[str, dict]) -> list[str]:
    """Slugs in an order where a claim's requires/interprets/part-of targets come first.

    A depth-first walk down those edges, tolerant of the cycles the tree should not contain but
    a checker cannot assume away: a slug already on the stack is left where it is.
    """
    order: list[str] = []
    seen: set[str] = set()
    stack: set[str] = set()

    def visit(slug: str) -> None:
        if slug in seen:
            return
        stack.add(slug)
        for t in (doss[slug].get("requires", []) + doss[slug].get("interprets", [])
                  + doss[slug].get("part_of", [])):
            if t in doss and t not in stack:
                visit(t)
        stack.discard(slug)
        seen.add(slug)
        order.append(slug)

    for slug in doss:
        visit(slug)
    return order


def resolve(paper: str) -> dict[str, dict]:
    """Every claim's floor: {slug: {level, fired, dossier}}, propagation and minima applied."""
    doss = dossier(paper)
    _wire_rivals(paper, doss)
    resolved: dict[str, str] = {}
    out: dict[str, dict] = {}
    for slug in _order(doss):
        lvl, fired = warrant_rule(doss[slug], resolved)
        resolved[slug] = lvl
        out[slug] = {"level": lvl, "fired": fired, "dossier": doss[slug]}
    return out


def _wire_rivals(paper: str, doss: dict[str, dict]) -> None:
    """Attach same-question rivals to each hypothesis, matched on `addresses`.

    The alternatives carry `addresses: q<n>`; a hypothesis that answers the same question is its
    rival. Hypotheses in the corpus rarely carry `addresses`, so this usually attaches nothing —
    which, with every Gädeke alternative already ruled out, changes no hypothesis's level.
    """
    d = os.path.join(CLAIMS_DIR, paper)
    addresses: dict[str, str] = {}
    alt_stance: dict[str, str] = {}
    for c in load_paper(paper):
        slug = c["slug"]
        a = first_assertion(c) or {}
        if c.get("addresses"):
            addresses[slug] = c["addresses"]
        alt_stance[slug] = a.get("stance") or "asserts"
    by_q: dict[str, list[str]] = collections.defaultdict(list)
    for slug, q in addresses.items():
        if _is_alternative(doss.get(slug, {}).get("role"), alt_stance.get(slug, "asserts")):
            by_q[q].append(slug)
    for slug, dd in doss.items():
        if dd["role"] == "hypothesis" and not _is_alternative(dd["role"], dd["stance"]):
            q = addresses.get(slug)
            dd["rivals"] = sorted(by_q.get(q, [])) if q else []


def fired_keys(d: dict) -> list[str]:
    """The non-empty evidence keys of a dossier — what the layer records as `warrant_from`."""
    keys = ("outcome", "predictions", "validated_by", "rules_out", "ruled_out_by",
            "reproductions", "verification", "requires", "part_of", "interprets",
            "supported_by", "extended_by")
    return [k for k in keys if d.get(k)]


# ── the comparison: the model's reading beside the rule's floor ───────────────────────────


def _latest_version(paper: str) -> int | None:
    """The highest N for which runs/<paper>/warrant.v<N>.json exists."""
    d = os.path.join(ROOT, "runs", paper)
    if not os.path.isdir(d):
        return None
    vs = []
    for fn in os.listdir(d):
        if fn.startswith("warrant.v") and fn.endswith(".json") and "report" not in fn:
            try:
                vs.append(int(fn[len("warrant.v"):-len(".json")]))
            except ValueError:
                pass
    return max(vs) if vs else None


def render_dossier(d: dict) -> str:
    """A claim's dossier as the prompt shows it to the reader — readable, not JSON."""
    lines = []
    o = d.get("outcome")
    if o:
        parts = []
        if o.get("confirms"):
            parts.append("confirmed by " + ", ".join(o["confirms"]))
        if o.get("refutes"):
            parts.append("refuted by " + ", ".join(o["refutes"]))
        if not parts and o.get("tests"):
            parts.append("tested by " + ", ".join(o["tests"]) + ", outcome not recorded")
        lines.append("  outcome: " + ("; ".join(parts) if parts else "no test points at it"))
    for p in d.get("predictions", []):
        lines.append(f"  prediction {p['slug']}: {p.get('outcome', 'untested')}")
    if d.get("validated_by"):
        lines.append("  validated by control(s): " + ", ".join(d["validated_by"]))
    if d.get("ruled_out_by"):
        lines.append("  ruled out by: " + ", ".join(d["ruled_out_by"]))
    if d.get("rules_out"):
        lines.append("  rules out: " + ", ".join(d["rules_out"]))
    if d.get("rivals"):
        lines.append("  same-question rivals: " + ", ".join(d["rivals"]))
    for r in d.get("reproductions", []):
        lines.append(f"  reproduction [{r.get('status')}]: "
                     f"paper {r.get('paper_value')} → reproduced {r.get('reproduced_value')}")
    for v in d.get("verification", []):
        lines.append(f"  verification [{v.get('status')}]: "
                     f"paper {v.get('paper_value')} → observed {v.get('reproduced_value')}")
    if d.get("requires"):
        lines.append("  requires: " + ", ".join(d["requires"]))
    if d.get("part_of"):
        lines.append("  part of: " + ", ".join(d["part_of"]))
    if d.get("interprets"):
        lines.append("  interprets: " + ", ".join(d["interprets"]))
    if d.get("supported_by"):
        lines.append("  supported by: " + ", ".join(d["supported_by"]))
    if d.get("extended_by"):
        lines.append("  extended by: " + ", ".join(d["extended_by"]))
    if not lines:
        lines.append("  (the tree records nothing that bears on this claim)")
    return "\n".join(lines)


def report(paper: str) -> str:
    """Write runs/<paper>/warrant.v<N>.report.md: the model's reading beside the rule's floor."""
    v = _latest_version(paper)
    if v is None:
        sys.exit(f"no recorded warrant version for {paper} — run the warrant layer first")
    answer = json.load(open(os.path.join(ROOT, "runs", paper, f"warrant.v{v}.json"),
                             encoding="utf-8"))
    model = {c["slug"]: c for c in answer.get("claims", [])}
    floor = resolve(paper)

    agree_by_role: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0])  # [agree, total]
    disagreements = []
    rows = []
    for slug in sorted(floor):
        f = floor[slug]
        m = model.get(slug, {})
        role = f["dossier"]["role"]
        m_level = m.get("warrant")
        r_level = f["level"]
        same = m_level == r_level
        agree_by_role[role][1] += 1
        agree_by_role[role][0] += int(same)
        rows.append((slug, role, m_level, r_level, same))
        if not same:
            disagreements.append({
                "slug": slug, "role": role, "model": m_level, "rule": r_level,
                "why": m.get("why", ""), "unsupported": m.get("unsupported", False),
                "fired": f["fired"],
            })

    total_agree = sum(a for a, _ in agree_by_role.values())
    total = sum(t for _, t in agree_by_role.values())

    out = [f"# Warrant: the model's reading beside the rule's floor — {paper}", ""]
    out.append(f"Rule v{RULE_VERSION}, shown here *after* the model judged, never before. "
               f"The model read {total} claims; it and the rule agree on "
               f"{total_agree}/{total}.")
    out += ["", "## Agreement by role", "",
            "| role | agree | total |", "|:--|--:|--:|"]
    for role in sorted(agree_by_role):
        a, t = agree_by_role[role]
        out.append(f"| {role} | {a} | {t} |")
    out.append(f"| **all** | **{total_agree}** | **{total}** |")

    out += ["", "## Every claim", "",
            "| claim | role | model | rule | |", "|:--|:--|:--|:--|:--|"]
    for slug, role, m_level, r_level, same in rows:
        out.append(f"| {slug} | {role} | {m_level} | {r_level} | {'' if same else '≠'} |")

    out += ["", "## Disagreements", ""]
    if not disagreements:
        out.append("None — the model's reading and the rule's floor coincide on every claim.")
    for dd in disagreements:
        out.append(f"### {dd['slug']} ({dd['role']})")
        out.append(f"- **model:** {dd['model']}"
                   + ("  ·  flagged unsupported" if dd["unsupported"] else ""))
        out.append(f"  - why: {dd['why']}")
        out.append(f"- **rule:** {dd['rule']}  ·  fired: {', '.join(dd['fired']) or '—'}")
        out.append("")

    out += _mismatch_note(paper, floor, model)
    text = "\n".join(out).rstrip() + "\n"
    path = os.path.join(ROOT, "runs", paper, f"warrant.v{v}.report.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"{path}: written ({total_agree}/{total} agree)")
    return path


def _mismatch_note(paper: str, floor: dict, model: dict) -> list[str]:
    """The single fact the note asks the comparison to assert (§How the rule is evaluated).

    The corpus holds exactly one `mismatch` reproduction, and it must come out `contested`. It
    is not Gädeke's, so the note's contingency applies: say so, and show what the rule and the
    model did on Gädeke's `partial` records instead.
    """
    out = ["## The one assertion the note asks for", ""]
    here = [s for s, f in floor.items()
            if any(r.get("status") == "mismatch" for r in f["dossier"].get("reproductions", []))]
    if here:
        s = here[0]
        out.append(f"`{s}` carries the corpus's `mismatch` reproduction, and the rule reads it "
                   f"`{floor[s]['level']}` — the note's requirement that a `mismatch` come out "
                   f"`contested` holds.")
        return out
    out.append("The corpus's one `mismatch` reproduction is **not** in this paper — it is "
               "`ejdrup-2026-dopamine/dat-clustering-greater-in-vs`, which this tree cannot "
               "exercise. The rule's `mismatch → contested` step is covered by the synthetic "
               "test instead. What this paper has is `partial` records, and the note asks what "
               "the rule and the model did on those:")
    out.append("")
    out.append("| claim | reproductions | model | rule |")
    out.append("|:--|:--|:--|:--|")
    for s in sorted(floor):
        f = floor[s]
        statuses = [r.get("status") for r in f["dossier"].get("reproductions", [])]
        if "partial" in statuses:
            m = model.get(s, {})
            out.append(f"| {s} | {', '.join(statuses)} | {m.get('warrant')} | {f['level']} |")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper")
    ap.add_argument("--report", action="store_true",
                    help="write runs/<paper>/warrant.v<N>.report.md from the recorded answer")
    a = ap.parse_args()
    if a.report:
        report(a.paper)
        return 0
    floor = resolve(a.paper)
    print(f"warrant rule v{RULE_VERSION} · {a.paper} · {len(floor)} claims\n")
    for slug in sorted(floor):
        f = floor[slug]
        print(f"  {f['level']:9s} {f['dossier']['role']:16s} {slug}")
        if f["fired"]:
            print(f"            ← {', '.join(f['fired'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
