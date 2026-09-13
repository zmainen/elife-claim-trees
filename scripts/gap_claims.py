#!/usr/bin/env python3
"""Layer `gap-claim` — what claim would close each gap?

`coverage` asks what the paper asserts that no claim represents, and `adjudication` sorts the
residue into the real holes. Until now the answer went into the marked document and stopped
there: nothing read a gap, and the graph ended at `marks`. So the pipeline asked what it had
missed twice — once at `external-review`, which runs before the claim tree exists and can only
guess from the candidates, and once at `coverage`, where the answer is evidence and had
nowhere to go.

This is the edge back. It drafts the claim each gap span needs, in the corpus's format, and
writes them as candidates:

    python3 scripts/gap_claims.py wengert-2026-kcnc1 --dump-prompt /tmp/q.txt
    # answer it anywhere — another model, another provider, a person
    python3 scripts/gap_claims.py wengert-2026-kcnc1 --answer /tmp/a.json

**Candidates, not claims.** It writes `runs/{paper}/gap-claim.output.json` and never touches
`claims/`. Promoting a draft into the tree is a decision about what a paper asserts, and this
corpus already carries the warning that no person has checked any of it; a layer that wrote
claim files directly would put a model's drafting inside the artifact the warning is about.
The candidates carry everything the promotion needs — slug, sentence, role, panel, and the
span each answers — so the step that remains is judgement rather than transcription.

Once a draft is promoted, the verdict that recorded the gap goes stale by itself: it carries
the fingerprint of which claims existed when it was judged, and the tree it named no longer
matches. That is the loop closing, and it is why the fingerprint is worth having.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "extract"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline  # noqa: E402

from adjudicate import claims, orphans  # noqa: E402

PROMPT = ROOT / "extract" / "prompts" / "gap-claim.md"
MAPPINGS = ROOT / "mappings"
OUT = ROOT / "runs"

ROLES = ("empirical", "control", "interpretation", "scope", "literature-context")

NOTE = ("Claims drafted for the spans `adjudication` judged a real gap. Candidates, not "
        "claims: nothing here is in the tree until a person promotes it, and promoting one "
        "makes the verdict that recorded the gap stale, which is how the loop closes.")


def gaps(paper: str) -> list[dict]:
    """The spans judged a gap, with the text each one is about."""
    m = MAPPINGS / f"{paper}.json"
    if not m.is_file():
        raise SystemExit(f"no adjudicated verdicts for {paper!r} — run the adjudication layer first")
    verdicts = json.loads(m.read_text(encoding="utf-8"))["spans"]
    by_uid = {s["uid"]: s for s in orphans(paper)}
    out = []
    for v in verdicts:
        if v.get("verdict") != "gap":
            continue
        span = by_uid.get(v["uid"])
        if not span:      # the span is no longer unresolved: a claim now matches it outright
            continue
        out.append({**span, "why_gap": v.get("why", "")})
    return out


def panel_ids(paper: str) -> list[str]:
    """Every panel id this paper actually has, in the notation the validator accepts.

    The first run of this layer had to read the validator to learn that the tree's
    `fig4-figure-supplement-1` is `fig4s1` here. The prompt said "the paper's own notation"
    and the paper has two; telling it which one costs a line.
    """
    prepared = ROOT / "runs" / paper / "prepared.json"
    if not prepared.is_file():
        return []
    p = json.loads(prepared.read_text(encoding="utf-8"))
    out = []
    for fc in p.get("figure_captions") or []:
        base = fc.get("element_id") or f"fig{str(fc.get('figure_num', '')).lower()}"
        out.append(base)
        out += [f"{base}{ltr}" for ltr in (fc.get("panels") or [])]
    for t in p.get("tables") or []:
        out.append(t.get("element_id") or f"table{t.get('table_num', '')}")
    return out


def neighbours(paper: str) -> dict[str, tuple[str, str]]:
    """The sentence before and after each span.

    A span is one sentence and its condition is often in the one before it: the first run of
    this layer had to open the marked document to find that a null result was in the control
    condition, because neither the span nor the verdict's reason said so. A drafter who has
    to leave the prompt to answer it has been given the wrong prompt.
    """
    from elife_extract.layers import read_prepared          # noqa: PLC0415
    from elife_extract.segment import segment               # noqa: PLC0415
    from elife_extract.config import Config                 # noqa: PLC0415
    try:
        prep = read_prepared(paper, Config(root=ROOT))
        spans = segment(prep, include_methods=False)
    except Exception:                                        # no prepared paper: no context
        return {}
    out = {}
    for i, sp in enumerate(spans):
        before = spans[i - 1].text if i else ""
        after = spans[i + 1].text if i + 1 < len(spans) else ""
        out[sp.uid] = (before, after)
    return out


def build_prompt(paper: str) -> tuple[str, str]:
    gs, cl = gaps(paper), claims(paper)
    around = neighbours(paper)
    pids = panel_ids(paper)
    lines = [f"Paper: {paper}", "",
             f"## The claim tree as it stands ({len(cl)} claims)",
             "", "Do not duplicate any of these.", ""]
    for c in cl:
        panel = f" · {c['panel']}" if c["panel"] else ""
        lines += [f"### {c['slug']}", f"role: {c['role']}{panel}", c["claim"], ""]
    if pids:
        lines += ["## The panels this paper has",
                  "",
                  "Use one of these in `panel`, exactly as spelled here, or leave it empty.",
                  "A supplement is `fig4s1`, never `fig4-figure-supplement-1`.",
                  "", ", ".join(pids), ""]
    lines += [f"## The gaps to close ({len(gs)})",
              "",
              "Each span is one sentence. The line before and after it are given because a "
              "span's condition is often stated in its neighbour rather than in itself.",
              ""]
    for g in gs:
        bits = []
        if g.get("stats"):
            bits.append("stats: " + ", ".join(g["stats"]))
        if g.get("panels"):
            bits.append("panels: " + ", ".join(g["panels"]))
        before, after = around.get(g["uid"], ("", ""))
        lines += [f"### {g['uid']}  [{g['section']}]" + (f"  ({' · '.join(bits)})" if bits else "")]
        if before:
            lines += [f"context before — {before}"]
        lines += [f"THE SPAN — {g['text']}"]
        if after:
            lines += [f"context after — {after}"]
        lines += [f"judged a gap because: {g['why_gap']}" if g.get("why_gap") else "", ""]
    return PROMPT.read_text(encoding="utf-8"), "\n".join(lines)


def parse(raw: str) -> dict:
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.S)
    if fence:
        text = fence.group(1).strip()
    start = text.find("{")
    data = json.loads(text[start if start >= 0 else 0:])
    if isinstance(data, list):          # a bare array of drafts is a natural thing to hand back
        data = {"drafted": data, "declined": []}
    return data


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _panel_id(raw: str) -> str:
    """`Figure 4—figure supplement 1`, `fig4-figure-supplement-1` and `fig4s1` are one panel.

    The claim tree writes supplements out in full, in more than one style, and
    `prepared.json` uses the JATS element id. Refusing the tree's own spelling taught this
    layer's first user to read the validator instead of the prompt, which is a fault in the
    validator rather than in the answer. Everything is reduced to one token first, so the
    separators stop mattering at all.
    """
    t = re.sub(r"[\s._\-\u2010-\u2015]", "", raw.strip().lower())
    t = t.replace("figure", "fig")
    t = re.sub(r"figsupplement", "s", t)
    return t


def validate(answer: dict, paper: str) -> tuple[dict, list[str]]:
    want = {g["uid"]: g for g in gaps(paper)}
    existing = {c["slug"] for c in claims(paper)}
    panels = set()
    prepared = ROOT / "runs" / paper / "prepared.json"
    if prepared.is_file():
        p = json.loads(prepared.read_text(encoding="utf-8"))
        for fc in p.get("figure_captions") or []:
            base = fc.get("element_id") or f"fig{fc.get('figure_num','').lower()}"
            panels.add(base)
            panels |= {f"{base}{ltr}" for ltr in (fc.get("panels") or [])}
        for t in p.get("tables") or []:
            panels.add(t.get("element_id") or f"table{t.get('table_num','')}")

    drafted = answer.get("drafted") or []
    declined = answer.get("declined") or []
    problems, seen, slugs, out = [], set(), set(), []

    for d in drafted:
        uid = d.get("uid")
        if uid not in want:
            problems.append(f"{uid}: not a span this paper left as a gap")
            continue
        if uid in seen:
            problems.append(f"{uid}: answered twice")
            continue
        seen.add(uid)
        slug = (d.get("slug") or "").strip()
        claim = re.sub(r"\s+", " ", (d.get("claim") or "")).strip()
        role = (d.get("role") or "").strip()
        panel = (d.get("panel") or "").strip()
        why = (d.get("why") or "").strip()
        if not SLUG_RE.match(slug):
            problems.append(f"{uid}: {slug!r} is not a kebab-case slug")
        if slug in existing:
            problems.append(f"{uid}: {slug!r} is already a claim of this paper")
        if slug in slugs:
            problems.append(f"{uid}: {slug!r} drafted twice in this answer")
        slugs.add(slug)
        if len(claim) < 20:
            problems.append(f"{uid}: the claim is too short to be one")
        if role not in ROLES:
            problems.append(f"{uid}: role {role!r} is not one of {ROLES}")
        if not why:
            problems.append(f"{uid}: no reason given, and the reason is what the promotion reads")
        # A panel the paper does not have is the failure mode that matters here: a claim
        # pointing at fig7 of a six-figure paper reads as evidence and resolves to nothing.
        for raw in [x.strip() for x in panel.split(",") if x.strip()]:
            pid = _panel_id(raw)
            if panels and pid not in panels:
                problems.append(f"{uid}: panel {raw!r} is not a panel of this paper")
        out.append({"uid": uid, "span": want[uid]["text"], "slug": slug, "claim": claim,
                    "role": role, "panel": panel, "why": why})

    for d in declined:
        uid = d.get("uid")
        if uid not in want:
            problems.append(f"{uid}: not a span this paper left as a gap")
            continue
        if uid in seen:
            problems.append(f"{uid}: both drafted and declined")
            continue
        seen.add(uid)
        if not (d.get("why") or "").strip():
            problems.append(f"{uid}: declined with no reason")

    for uid in want:
        if uid not in seen:
            problems.append(f"{uid}: neither drafted nor declined")

    order = list(want)
    out.sort(key=lambda d: order.index(d["uid"]))
    return {"drafted": out,
            "declined": [{"uid": d["uid"], "why": (d.get("why") or "").strip()}
                         for d in declined if d.get("uid") in want]}, problems


def write(paper: str, result: dict, *, by: str, tokens: int | None = None) -> Path:
    out = OUT / paper / "gap-claim.output.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "paper": paper,
        "drafted_on": date.today().isoformat(),
        "model": by,
        "note": NOTE,
        "candidates": result["drafted"],
        "declined": result["declined"],
        **({"usage": pipeline.answered_usage(tokens)} if tokens else {}),
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper")
    ap.add_argument("--dump-prompt", metavar="PATH",
                    help="write the exact prompt this layer would send to PATH and exit")
    ap.add_argument("--answer", metavar="PATH",
                    help="drafts produced elsewhere; validated before anything is written")
    ap.add_argument("--tokens", type=int, metavar="N",
                    help="what the session that answered this spent; the "
                         "ledger records how an answer arrived and, with "
                         "this, what it cost")
    args = ap.parse_args()

    system, user = build_prompt(args.paper)
    if args.dump_prompt:
        out = Path(args.dump_prompt).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(system + "\n\n---\n\n" + user, encoding="utf-8")
        print(f"  gap-claim: prompt written to {out}  "
              f"({len(system)}c system + {len(user)}c user)")
        print("  answer it, then: --answer <file>")
        return 0
    if not args.answer:
        ap.error("this layer has no backend call: use --dump-prompt, then --answer")

    src = Path(args.answer).expanduser().resolve()
    result, problems = validate(parse(src.read_text(encoding="utf-8")), args.paper)
    if problems:
        print(f"{args.paper}: {len(problems)} problem(s), nothing written", file=sys.stderr)
        for p in problems[:40]:
            print(f"  {p}", file=sys.stderr)
        if len(problems) > 40:
            print(f"  … and {len(problems) - 40} more", file=sys.stderr)
        return 1

    try:
        where = src.relative_to(ROOT)
    except ValueError:
        where = src
    out = write(args.paper, result, by=f"supplied:{where}",
                tokens=pipeline.answered_tokens(args.tokens))
    print(f"  {args.paper:38} {len(result['drafted'])} drafted · "
          f"{len(result['declined'])} declined · {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
