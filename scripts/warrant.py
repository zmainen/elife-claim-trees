#!/usr/bin/env python3
"""How well does the tree support a claim — the dossier, the rule floor, and the comparison.

`warrant` is what the tree's *argument* gives a reader grounds to believe, as distinct from what
the paper says (`confidence`) and from how many readers agreed (`READER_CONFIDENCE`). Version 2
(the 2026-09-13 rulings, docs/design/2026-09-13-warrant.md) reframes it: warrant reasons only
from what the paper reports and how its argument hangs together, as the tree records it —
predictions and their outcomes, the controls that validate a result, the rivals it rules out,
what supports and requires what. *Checking* is not part of it. A reproduction, a methods
assessment, a statistics check, a citation check are each a separate later layer that writes a
modifier beside the warrant; none of them enters here. There are three mechanical pieces, and
one model judgement that lives in the `warrant` layer (extract/prompts/warrant.md):

  dossier(paper)        Per claim, what the tree's argument holds — role, stance, the outcomes
                        on its predictions, the controls that validate it, the rivals it rules
                        out, the incoming supports/extends/confirms/refutes, what it requires
                        and is part of (with their roles), and what it interprets. No checking
                        record, no confidence, no reproduction. Plain data, no judgement in it.

  warrant_rule(d)       The note's version-2 rule, by role, over one claim's dossier. Returns
                        the level and the inputs that fired. It is the floor the model's reading
                        is scored against — kept for scoring only, and shown to the model only
                        *after* it judges, never before.

  resolve(paper)        Runs the rule over the whole tree, in dependency order, so propagation
                        (a claim is bounded above by the weakest same-kind claim it requires)
                        and the interpretation/synthesis rules can read their neighbours'
                        resolved levels.

  report(paper)         The comparison: the model's level beside the rule's floor for every
                        claim, agreement overall and by role, and every disagreement with the
                        model's `why` beside the rule's fired keys. Reads the recorded
                        `warrant.v<N>.json`, writes `runs/<paper>/warrant.v<N>.report.md`, and
                        writes `runs/<paper>/warrant.v<N>.annotated.json` beside it.

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

RULE_VERSION = 2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The graded levels, weakest first, so `min` is the weakest and a cap is a slice. Predictions
# (confirmed/refuted/untested) and alternatives (ruled-out/open) carry their own vocabularies
# and never enter this ordering.
GRADED = ("contested", "weak", "moderate", "strong")
_RANK = {lv: i for i, lv in enumerate(GRADED)}

# The roles whose warrant is graded from the tree's argument on the claim. A role outside every
# branch of the rule (literature-context is the one in the corpus) is graded here too.
GRADED_ROLES = {"empirical", "control", "methodological", "scope", "literature-context"}
INTERPRETIVE_ROLES = {"synthesis", "interpretation"}

# The role groups propagation runs within: a claim is bounded only by a required claim of its own
# group. Methodological and scope are in no group, so they never bound anything and are never
# bounded (§rule v2). An unassessed prerequisite of another kind is noted, not counted.
_ROLE_GROUP = {"empirical": "result", "control": "result",
               "hypothesis": "claim", "prediction": "claim"}

# One step below, for an interpretation over the strongest claim it interprets. `contested` and
# `weak` floor at `weak` — an interpretation is not itself refuted by interpreting refuted work.
_STEP_DOWN = {"strong": "moderate", "moderate": "weak", "weak": "weak", "contested": "weak"}

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


# ── the dossier: what the tree's argument holds about a claim ──────────────────────────────


def _incoming(claims: list[dict]) -> dict[str, list[tuple[str, str]]]:
    """target slug → [(relation, source slug)] across the tree, both storage shapes."""
    inc: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
    for c in claims:
        for rel, tgt in relations(c):
            inc[tgt].append((rel, c["slug"]))
    return inc


def dossier(paper: str) -> dict[str, dict]:
    """Per claim, what the tree's argument holds about its support. Plain data — no judgement.

    One dict per claim, keyed by slug. The identity keys (slug, role, stance, sentence) say what
    the claim is; the evidence keys say how the paper's argument stands behind it, and it is the
    non-empty ones the layer records as `warrant_from`. No checking record enters here: a
    reproduction, a methods or statistics check, a citation check is a later layer's word
    (§"Checks are separate layers").
    """
    claims = load_paper(paper)
    by_slug = {c["slug"]: c for c in claims}
    inc = _incoming(claims)
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

        requires = sorted(t for r, t in outgoing if r == "requires")
        part_of = sorted(t for r, t in outgoing if r == "part-of")
        d = {
            "slug": slug,
            "role": role,
            "stance": stance,
            "sentence": " ".join((c.get("claim") or "").split()),
            # Evidence keys — the argument that "fires".
            "outcome": prediction_outcome_of(slug) if role == "prediction" else None,
            "predictions": predictions,
            "validated_by": sorted(src for r, src in incoming if r == "validates"),
            # This claim tests a prediction that came out as predicted — it is the source of a
            # `confirms` (§rule v2, the empirical `strong` clause). And the predictions others
            # confirm about it, shown as argument.
            "confirms": sorted(t for r, t in outgoing if r == "confirms"),
            "confirmed_by": sorted(src for r, src in incoming if r == "confirms"),
            "rules_out": sorted(t for r, t in outgoing if r == "rules-out"),
            "ruled_out_by": sorted(src for r, src in incoming if r == "rules-out"),
            "supported_by": sorted(src for r, src in incoming if r == "supports"),
            "extended_by": sorted(src for r, src in incoming if r == "extends"),
            # A result in the tree that refutes this claim moves it to contested (§rule v2).
            "refuted_by": sorted(src for r, src in incoming
                                 if r in ("refutes", "contradicts") and src in by_slug),
            "requires": requires,
            "part_of": part_of,
            "interprets": sorted(t for r, t in outgoing if r == "interprets"),
            # The roles of what it requires and is part of, for the rendered dossier and for
            # propagation's same-group test.
            "require_roles": {t: by_slug.get(t, {}).get("role") for t in requires},
            "part_of_roles": {t: by_slug.get(t, {}).get("role") for t in part_of},
        }
        doss[slug] = d
    return doss


# ── the rule floor: the note's version 2, by role ─────────────────────────────────────────


def warrant_rule(d: dict, resolved: dict[str, str] | None = None,
                 unassessed: set[str] | None = None) -> tuple[str, list[str]]:
    """The version-2 rule over one claim's dossier: the level, and the inputs that fired.

    `resolved` carries the levels the rest of the tree has already resolved to, which the
    non-local branches read: propagation caps a claim at the weakest same-kind claim it
    requires, and interpretation/synthesis read the levels of what they interpret. `unassessed`
    is the slugs the rule found empty, so a prerequisite of another kind can be flagged. Every
    other branch is a function of the dossier alone, so a synthetic claim tests it without one.
    """
    resolved = resolved or {}
    unassessed = unassessed or set()
    role, stance = d["role"], d.get("stance") or "asserts"

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

    # An interpretation sits one step below the strongest claim it interprets, capped at
    # moderate — argument alone never reaches strong.
    if role == "interpretation":
        levels = [(t, resolved[t]) for t in d.get("interprets", []) if resolved.get(t) in _RANK]
        if not levels:
            return "weak", ["interprets-nothing"]
        top = max((lv for _, lv in levels), key=lambda x: _RANK[x])
        lvl = _cap(_STEP_DOWN[top], "moderate")
        return lvl, [f"interprets:{t}={lv}" for t, lv in levels]

    # A synthesis reads agreement among what it interprets: moderate if two or more, none weak.
    if role == "synthesis":
        levels = [(t, resolved[t]) for t in d.get("interprets", []) if resolved.get(t) in _RANK]
        fired = [f"interprets:{t}={lv}" for t, lv in levels]
        if len(levels) >= 2 and all(lv != "weak" for _, lv in levels):
            return "moderate", fired
        return "weak", (fired or ["interprets-nothing"])

    # A hypothesis is warranted by its predictions and its rivals.
    if role == "hypothesis":
        preds = d.get("predictions", [])
        confirmed = [p["slug"] for p in preds if p.get("outcome") == "confirmed"]
        refuted = [p["slug"] for p in preds if p.get("outcome") == "refuted"]
        if refuted:
            lvl, fired = "contested", [f"prediction-refuted:{s}" for s in refuted]
        elif confirmed:
            fired = [f"prediction-confirmed:{s}" for s in confirmed]
            standing = _standing_rivals(d, resolved)
            if standing:
                lvl, fired = "moderate", fired + [f"rival-stands:{s}" for s in standing]
            else:
                lvl = "strong"
                fired = fired + (["rivals-ruled-out"] if _rivals(d, resolved) else [])
        else:
            lvl, fired = "weak", ["no-prediction-outcome"]
        return _propagate(lvl, fired, role, d, resolved, unassessed)

    # Empirical, control, methodological, scope (and any other asserted, graded claim).
    lvl, fired = _graded_rule(d)
    return _propagate(lvl, fired, role, d, resolved, unassessed)


def _cap(lvl: str, ceiling: str) -> str:
    return lvl if _RANK[lvl] <= _RANK[ceiling] else ceiling


def _rivals(d: dict, resolved: dict[str, str]) -> list[str]:
    """Alternatives that address the same question as this hypothesis (§rule)."""
    return d.get("rivals", [])


def _standing_rivals(d: dict, resolved: dict[str, str]) -> list[str]:
    """Rivals to this hypothesis that were not ruled out — an alternative that still stands."""
    return [s for s in _rivals(d, resolved) if resolved.get(s) == "open"]


def _graded_rule(d: dict) -> tuple[str, list[str]]:
    """The graded branch: the tree's argument alone (§rule v2). No confidence, no reproduction.

    `strong` when the claim both tests a prediction that came out as predicted (it is the source
    of a `confirms`) and is validated by a control; `moderate` when exactly one of those holds,
    or when two or more distinct claims support it; `weak` otherwise; `contested` when a result
    in the tree refutes it. An empty dossier is `weak`, flagged `unassessed`.
    """
    if d.get("refuted_by"):
        return "contested", [f"refuted-by:{s}" for s in d["refuted_by"]]
    confirms = d.get("confirms", [])
    validated = d.get("validated_by", [])
    supports = d.get("supported_by", [])
    tests = bool(confirms)
    ctrl = bool(validated)
    if tests and ctrl:
        return "strong", ([f"confirms:{s}" for s in confirms]
                          + [f"validated-by:{s}" for s in validated])
    if (tests != ctrl) or len(supports) >= 2:
        fired = [f"confirms:{s}" for s in confirms] + [f"validated-by:{s}" for s in validated]
        if len(supports) >= 2:
            fired += [f"supported-by:{s}" for s in supports]
        return "moderate", fired
    if not fired_keys(d):
        return "weak", ["unassessed"]
    return "weak", ([f"supported-by:{s}" for s in supports] or ["asserted"])


def _propagate(lvl: str, fired: list[str], role: str, d: dict,
               resolved: dict[str, str], unassessed: set[str]) -> tuple[str, list[str]]:
    """Bound a claim's warrant at the weakest same-kind claim it requires (§propagation, v2).

    Only a required claim of the same role group bounds it (empirical/control together;
    hypothesis/prediction together). Methodological and scope are in no group, so they neither
    bound nor are bounded. An unassessed prerequisite of another kind is listed and left to
    change nothing.
    """
    grp = _ROLE_GROUP.get(role)
    rroles = d.get("require_roles", {})
    for t in d.get("requires", []):
        t_lvl = resolved.get(t)
        same = grp is not None and grp == _ROLE_GROUP.get(rroles.get(t))
        if same and t_lvl in _RANK and _RANK[t_lvl] < _RANK[lvl]:
            lvl = t_lvl
            fired = fired + [f"bounded-by-requires:{t}={t_lvl}"]
        elif not same and t in unassessed:
            fired = fired + [f"prerequisite-unassessed:{t}"]
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
    """Every claim's floor: {slug: {level, fired, dossier}}, propagation and interpretation applied."""
    doss = dossier(paper)
    _wire_rivals(paper, doss)
    resolved: dict[str, str] = {}
    unassessed: set[str] = set()
    out: dict[str, dict] = {}
    for slug in _order(doss):
        lvl, fired = warrant_rule(doss[slug], resolved, unassessed)
        resolved[slug] = lvl
        if "unassessed" in fired:
            unassessed.add(slug)
        out[slug] = {"level": lvl, "fired": fired, "dossier": doss[slug]}
    return out


def _wire_rivals(paper: str, doss: dict[str, dict]) -> None:
    """Attach same-question rivals to each hypothesis, matched on `addresses`.

    The alternatives carry `addresses: q<n>`; a hypothesis that answers the same question is its
    rival. Hypotheses in the corpus rarely carry `addresses`, so this usually attaches nothing —
    which, with every Gädeke alternative already ruled out, changes no hypothesis's level.
    """
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
    keys = ("outcome", "predictions", "validated_by", "confirms", "confirmed_by", "rules_out",
            "ruled_out_by", "supported_by", "extended_by", "refuted_by", "requires", "part_of",
            "interprets")
    return [k for k in keys if d.get(k)]


# ── the comparison: the model's reading beside the rule's floor ───────────────────────────


def _latest_version(paper: str) -> int | None:
    """The highest N for which runs/<paper>/warrant.v<N>.json exists."""
    d = os.path.join(ROOT, "runs", paper)
    if not os.path.isdir(d):
        return None
    vs = []
    for fn in os.listdir(d):
        if fn.startswith("warrant.v") and fn.endswith(".json") and "report" not in fn \
                and "annotated" not in fn:
            try:
                vs.append(int(fn[len("warrant.v"):-len(".json")]))
            except ValueError:
                pass
    return max(vs) if vs else None


def render_dossier(d: dict) -> str:
    """A claim's dossier as the prompt shows it to the reader — readable, not JSON.

    The tree's argument only: predictions and their outcomes, the controls that validate it, the
    rivals it rules out, what supports/extends/confirms/refutes it, what it requires and is part
    of (with their roles), what it interprets. No reproduction, no confidence — a later layer's
    business, not warrant's.
    """
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
    if d.get("confirms"):
        lines.append("  confirms prediction(s): " + ", ".join(d["confirms"]))
    if d.get("validated_by"):
        lines.append("  validated by control(s): " + ", ".join(d["validated_by"]))
    if d.get("ruled_out_by"):
        lines.append("  ruled out by: " + ", ".join(d["ruled_out_by"]))
    if d.get("rules_out"):
        lines.append("  rules out: " + ", ".join(d["rules_out"]))
    if d.get("rivals"):
        lines.append("  same-question rivals: " + ", ".join(d["rivals"]))
    if d.get("refuted_by"):
        lines.append("  refuted by: " + ", ".join(d["refuted_by"]))
    if d.get("supported_by"):
        lines.append("  supported by: " + ", ".join(d["supported_by"]))
    if d.get("extended_by"):
        lines.append("  extended by: " + ", ".join(d["extended_by"]))
    if d.get("confirmed_by"):
        lines.append("  confirmed by: " + ", ".join(d["confirmed_by"]))
    if d.get("requires"):
        lines.append("  requires: " + ", ".join(_with_roles(d["requires"], d.get("require_roles", {}))))
    if d.get("part_of"):
        lines.append("  part of: " + ", ".join(_with_roles(d["part_of"], d.get("part_of_roles", {}))))
    if d.get("interprets"):
        lines.append("  interprets: " + ", ".join(d["interprets"]))
    if not lines:
        lines.append("  (the tree records nothing that bears on this claim)")
    return "\n".join(lines)


def _with_roles(slugs: list[str], roles: dict[str, str]) -> list[str]:
    return [f"{s} ({roles[s]})" if roles.get(s) else s for s in slugs]


def report(paper: str) -> str:
    """Write warrant.v<N>.report.md and warrant.v<N>.annotated.json from the recorded answer."""
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
    out.append(f"Rule v{RULE_VERSION}, the argument-only floor, shown here *after* the model "
               f"judged, never before. The model read {total} claims; it and the rule agree on "
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

    text = "\n".join(out).rstrip() + "\n"
    path = os.path.join(ROOT, "runs", paper, f"warrant.v{v}.report.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    ann = write_annotated(paper, v, floor, model)
    print(f"{path}: written ({total_agree}/{total} agree)")
    print(f"{ann}: written")
    return path


def write_annotated(paper: str, v: int, floor: dict, model: dict) -> str:
    """One object per claim, the maintainer's annotated page is built from — byte-stable.

    Sorted by slug, sorted keys, trailing newline: a function of the tree and the recorded
    answer alone, so it is not rewritten by `make data` (which does not touch runs/) and a
    re-run produces the same bytes.
    """
    records = []
    for slug in sorted(floor):
        f = floor[slug]
        d = f["dossier"]
        m = model.get(slug, {})
        records.append({
            "slug": slug,
            "role": d["role"],
            "stance": d["stance"],
            "sentence": d["sentence"],
            "rule": f["level"],
            "rule_fired": f["fired"],
            "model": m.get("warrant"),
            "why": m.get("why", ""),
            "model_from": m.get("warrant_from", []),
            "unsupported": bool(m.get("unsupported", False)),
            "dossier": render_dossier(d),
        })
    path = os.path.join(ROOT, "runs", paper, f"warrant.v{v}.annotated.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(records, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    return path


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
