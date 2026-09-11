#!/usr/bin/env python3
"""Layer `adjudication` — of the spans the matcher could not resolve, which are real gaps?

`coverage` asks of every sentence in the paper whether a claim accounts for it, and answers
mechanically: a claim accounts for a span when it restates a statistic the span carries or
names the same figure panel. That test is wrong in both directions, and the residue it leaves
is a mixture — claims that state an effect without repeating its numbers, sentences that
assert nothing at all, and real holes in the corpus. Sorting them is a judgement about
meaning, which is why the verdicts are stored rather than recomputed: running this twice
produces two different answers, and the second one silently replaces the first.

The layer had a prompt and no runner, so its one existing mapping was produced by hand. This
is the runner, with the pair every model-answered layer carries:

    python3 scripts/adjudicate.py wengert-2026-kcnc1 --dump-prompt /tmp/q.txt
    # answer it anywhere — another model, another provider, a person
    python3 scripts/adjudicate.py wengert-2026-kcnc1 --answer /tmp/a.json

A verdict is written with the fingerprint of the sentence it was made about, because a span id
is positional: insert one sentence earlier in the section and every id after it shifts, and a
verdict would reattach to different text with nothing to notice. `coverage` discards a verdict
whose fingerprint no longer matches, and that is only possible if this writes one.
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

from elife_extract.coverage import claim_fingerprint, tree_fingerprint  # noqa: E402
from elife_extract.segment import span_sha  # noqa: E402
from corpus_facts import frontmatter  # noqa: E402

PROMPT = ROOT / "extract" / "prompts" / "coverage-adjudicator.md"
COVERAGE = ROOT / "coverage"
OUT_DIR = ROOT / "mappings"

# What the corpus stores. The prompt used to ask for `no-assertion`, which the reader in
# coverage.py does not recognise — a verdict spelled that way fell through to the `else` and
# was counted as the gap it had just been judged not to be. Both spellings are accepted here
# and normalised to the one the corpus reads.
VERDICTS = ("covered", "gap", "not-an-assertion")
ALIASES = {"no-assertion": "not-an-assertion", "not an assertion": "not-an-assertion"}

NOTE = ("Verdicts for spans the mechanical match could not resolve. covered = a claim does "
        "account for it; gap = a real hole; not-an-assertion = the span states no result of "
        "its own. Every verdict carries `sha`, the fingerprint of the sentence it judged. A "
        "`gap` also carries `tree`, the fingerprint of which claims existed when it was "
        "judged, and a `covered` carries `claim_sha`, the wording of the claim it named — "
        "because a gap is a statement about the tree, and closing one is exactly the edit "
        "that used to leave the verdict standing over nothing. `coverage` discards a verdict "
        "whose fingerprints no longer match rather than applying a judgement nobody made "
        "about what is there now.")


def orphans(paper: str) -> list[dict]:
    """The spans coverage could not resolve, in document order."""
    p = COVERAGE / f"{paper}.json"
    if not p.is_file():
        raise SystemExit(f"no coverage report for {paper!r} — run the coverage layer first")
    return json.loads(p.read_text(encoding="utf-8"))["spans"]["orphans"]


def claims(paper: str) -> list[dict]:
    """The claim tree the spans are judged against — slug and sentence, nothing else."""
    out = []
    for f in sorted((ROOT / "claims" / paper).glob("*.md")):
        if f.name == "index.md":
            continue
        fm = frontmatter(f) or {}
        assertion = next((a for a in (fm.get("assertions") or [])
                          if a.get("paper-slug") == paper), {})
        out.append({
            "slug": fm.get("slug") or f.stem,
            "role": fm.get("role") or "",
            "panel": assertion.get("panel") or "",
            "claim": re.sub(r"\s+", " ", (fm.get("claim") or "")).strip(),
        })
    return out


def build_prompt(paper: str) -> tuple[str, str]:
    sp, cl = orphans(paper), claims(paper)
    lines = [f"Paper: {paper}", "",
             f"## The claim tree ({len(cl)} claims)", ""]
    for c in cl:
        panel = f" · {c['panel']}" if c["panel"] else ""
        lines += [f"### {c['slug']}", f"role: {c['role']}{panel}", c["claim"], ""]
    lines += [f"## The spans to judge ({len(sp)})", ""]
    for s in sp:
        bits = []
        if s.get("stats"):
            bits.append("stats: " + ", ".join(s["stats"]))
        if s.get("panels"):
            bits.append("panels: " + ", ".join(s["panels"]))
        lines += [f"### {s['uid']}  [{s['section']}]" + (f"  ({' · '.join(bits)})" if bits else ""),
                  s["text"], ""]
    return PROMPT.read_text(encoding="utf-8"), "\n".join(lines)


def parse(raw: str) -> list[dict]:
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.S)
    if fence:
        text = fence.group(1).strip()
    start = min([i for i in (text.find("["), text.find("{")) if i >= 0], default=0)
    data = json.loads(text[start:])
    return data["spans"] if isinstance(data, dict) else data


def validate(answer: list[dict], paper: str) -> tuple[list[dict], list[str]]:
    """Normalise and check. Returns the verdicts to write and what is wrong with them."""
    want = {s["uid"]: s for s in orphans(paper)}
    tree_claims = claims(paper)
    by_slug_claims = {c["slug"]: c for c in tree_claims}
    slugs = set(by_slug_claims)
    problems, out, seen = [], [], set()

    for v in answer:
        uid = v.get("uid")
        if uid not in want:
            problems.append(f"{uid}: not a span this paper left unresolved")
            continue
        if uid in seen:
            problems.append(f"{uid}: judged twice")
            continue
        seen.add(uid)
        verdict = ALIASES.get(str(v.get("verdict", "")).strip(), str(v.get("verdict", "")).strip())
        if verdict not in VERDICTS:
            problems.append(f"{uid}: verdict {v.get('verdict')!r} is not one of {VERDICTS}")
            continue
        claim = v.get("claim") or None
        if verdict == "covered" and not claim:
            problems.append(f"{uid}: covered, but names no claim")
        elif verdict == "covered" and claim not in slugs:
            problems.append(f"{uid}: covered by {claim!r}, which is not a claim of this paper")
        elif verdict != "covered" and claim:
            problems.append(f"{uid}: {verdict} cannot name a claim")
        why = (v.get("why") or "").strip()
        if not why:
            problems.append(f"{uid}: no reason given, and the reason becomes the mark's body")
        rec = {"uid": uid, "verdict": verdict, "claim": claim if verdict == "covered" else None,
               "why": why, "sha": span_sha(want[uid]["text"])}
        # The second fingerprint, and which one depends on what the verdict rests on.
        # `not-an-assertion` rests on the sentence alone — it says the span states no result,
        # which no claim anywhere can make false — so it carries neither and never goes stale
        # for a reason outside itself.
        if verdict == "gap":
            rec["tree"] = tree_fingerprint(tree_claims)
        elif verdict == "covered" and claim in by_slug_claims:
            rec["claim_sha"] = claim_fingerprint(by_slug_claims[claim])
        out.append(rec)

    for uid in want:
        if uid not in seen:
            problems.append(f"{uid}: not judged")
    order = list(want)
    out.sort(key=lambda v: order.index(v["uid"]))
    return out, problems


def write(paper: str, verdicts: list[dict], *, by: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{paper}.json"
    out.write_text(json.dumps({
        "paper": paper,
        "adjudicated": date.today().isoformat(),
        "by": by,
        "note": NOTE,
        "spans": verdicts,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper")
    ap.add_argument("--dump-prompt", metavar="PATH",
                    help="write the exact prompt this layer would send to PATH and exit")
    ap.add_argument("--answer", metavar="PATH",
                    help="verdicts produced elsewhere; validated before anything is written")
    args = ap.parse_args()

    system, user = build_prompt(args.paper)
    if args.dump_prompt:
        out = Path(args.dump_prompt).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(system + "\n\n---\n\n" + user, encoding="utf-8")
        print(f"  adjudication: prompt written to {out}  "
              f"({len(system)}c system + {len(user)}c user)")
        print("  answer it, then: --answer <file>")
        return 0
    if not args.answer:
        ap.error("this layer is a judgement and has no backend call: "
                 "use --dump-prompt, then --answer")

    src = Path(args.answer).expanduser().resolve()
    verdicts, problems = validate(parse(src.read_text(encoding="utf-8")), args.paper)
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
    out = write(args.paper, verdicts, by=f"supplied:{where}")
    counts = {v: sum(1 for x in verdicts if x["verdict"] == v) for v in VERDICTS}
    print(f"  {args.paper:38} {len(verdicts)} verdicts · "
          + " · ".join(f"{k} {v}" for k, v in counts.items())
          + f" · {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
