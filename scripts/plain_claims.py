#!/usr/bin/env python3
"""One plain sentence per claim — the wording a reader meets first.

A claim is recorded in the authors' words, which is right: the corpus has to be able to show
what the paper said, and a paraphrase is not evidence of anything. But the authors' words open
with the statistics — `Being the decision-maker (Social + Solo vs Partner condition) reduces
participant happiness independently of outcome (Study 1: t(3600)=-3.92, p<0.0001, …)` — and a
page that lists thirty of those has told a non-specialist nothing they can act on.

`shortClaim` was meant to be this and is filled for hypotheses and predictions only; every
empirical claim in the corpus falls back to the full sentence. This layer fills the gap for all
of them, and does it as a layer rather than as a field somebody edits, because it is model-
written prose that a reader will take for the paper's own. It therefore needs what every other
model output here has: a version, a recorded run, an input hash that goes stale when the claim
it restates changes, and a place for a person to approve it.

    python3 scripts/plain_claims.py gadeke-2026-guilt-insula                       # call the model
    python3 scripts/plain_claims.py gadeke-2026-guilt-insula --dump-prompt /tmp/q.txt
    python3 scripts/plain_claims.py gadeke-2026-guilt-insula --answer /tmp/a.json

`--dump-prompt` / `--answer` is the pair every layer a model answers carries, and it works
here the way it works there: the exact request is written out, whatever answers it answers the
question this layer would have asked rather than a paraphrase written from memory, and the
answer comes back through the same validation a backend reply would get. A supplied answer
records `model: supplied:<path>` rather than naming a model that never ran.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "extract"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402

# Six scripts here carry the same three-line fix for one quirk of the claim files — a key
# whose empty value is written on the next line, which PyYAML rejects and gray-matter accepts.
# This is the seventh caller and it imports the fix rather than copying it again.
from corpus_facts import frontmatter  # noqa: E402

PROMPT = ROOT / "extract" / "prompts" / "plain-claim.md"
OUT_DIR = ROOT / "site" / "src" / "data" / "plain-claims"
MAX_CHARS = 200

# What a statistic looks like. The rule the prompt states is "no statistics"; this is the part
# of it a machine can check. It is deliberately narrow — "two studies" and "three regions" are
# findings, not evidence, and a validator that rejected every digit would forbid them.
STATS = [
    (re.compile(r"\bp\s*[<=>]\s*\.?\d"), "a p-value"),
    (re.compile(r"\b[tFzZ]\s*\(\s*\d"), "a test statistic"),
    (re.compile(r"\b(?:95|99)\s*%\s*CI"), "a confidence interval"),
    (re.compile(r"[βρηΔ]\s*[=<>]"), "a coefficient"),
    (re.compile(r"\b(?:Cohen's\s*d|BF10|R\s*2|r\s*=)\b", re.I), "an effect size"),
    (re.compile(r"\bMNI\b|\[\s*-?\d+[,\s]+-?\d+[,\s]+-?\d+\s*\]"), "a coordinate"),
    (re.compile(r"\b[Nn]\s*=\s*\d"), "a sample size"),
    (re.compile(r"\bFWE\b|\bpFWE\b|\buncorrected\b", re.I), "a correction term"),
]


# ── the claims ────────────────────────────────────────────────────────────────

def load_claims(paper: str) -> list[dict]:
    """Every claim file of one paper, in slug order."""
    d = ROOT / "claims" / paper
    if not d.is_dir():
        raise SystemExit(f"no claim directory for {paper!r}")
    out = []
    for p in sorted(d.glob("*.md")):
        if p.name == "index.md":
            continue
        fm = frontmatter(p) or {}
        assertion = next((a for a in (fm.get("assertions") or [])
                          if a.get("paper-slug") == paper), {})
        out.append({
            "slug": fm.get("slug") or p.stem,
            "role": fm.get("role") or fm.get("claim-type") or "",
            "stance": assertion.get("stance", "asserts"),
            "panel": assertion.get("panel") or "",
            "claim": re.sub(r"\s+", " ", (fm.get("claim") or "")).strip(),
        })
    return out


def build_prompt(paper: str, claims: list[dict]) -> tuple[str, str]:
    system = PROMPT.read_text(encoding="utf-8")
    lines = [f"Paper: {paper}", f"{len(claims)} claims.", ""]
    for c in claims:
        stance = "" if c["stance"] == "asserts" else f" · stance: {c['stance']}"
        panel = f" · {c['panel']}" if c["panel"] else ""
        lines += [f"### {c['slug']}", f"role: {c['role']}{stance}{panel}", c["claim"], ""]
    return system, "\n".join(lines)


# ── validation ────────────────────────────────────────────────────────────────

def validate(answer: dict, claims: list[dict]) -> list[str]:
    """What is wrong with this answer. An empty list is the only thing that gets written."""
    problems = []
    want = {c["slug"] for c in claims}
    got = set(answer)
    for slug in sorted(want - got):
        problems.append(f"{slug}: missing")
    for slug in sorted(got - want):
        problems.append(f"{slug}: not a claim of this paper")
    for slug in sorted(want & got):
        s = (answer[slug] or "").strip()
        if not s:
            problems.append(f"{slug}: empty")
            continue
        if len(s) > MAX_CHARS:
            problems.append(f"{slug}: {len(s)} chars, over {MAX_CHARS}")
        if not s.endswith((".", "?")):
            problems.append(f"{slug}: does not end a sentence")
        if re.search(r"[.?!]\s+[A-Z]", s):
            problems.append(f"{slug}: more than one sentence")
        for rx, what in STATS:
            if rx.search(s):
                problems.append(f"{slug}: carries {what} — {rx.search(s).group(0)!r}")
                break
    return problems


def write(paper: str, answer: dict, claims: list[dict], *, model: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{paper}.json"
    # A list of records rather than a slug→sentence map, so the layer's own page renders it
    # with the generic table the other layers get. The role and the panel travel with each
    # wording because the page that reviews these needs to see what was being restated.
    payload = {
        "paper": paper,
        "model": model,
        "prompt": str(PROMPT.relative_to(ROOT)),
        "claims": [
            {"slug": c["slug"], "role": c["role"], "panel": c["panel"],
             "plain": answer[c["slug"]].strip()}
            for c in claims
        ],
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return out


# ── the model call ────────────────────────────────────────────────────────────

def ask_model(system: str, user: str) -> tuple[str, str]:
    from elife_extract.agents import stream_text
    from elife_extract.config import Config

    cfg = Config.load()
    model = getattr(cfg, "reconciler_model", None) or getattr(cfg, "model", None)
    if not model:
        raise SystemExit("no model configured — see extract/elife_extract/config.py")
    raw = stream_text(cfg, model=model, system=system, user=user, label="plain-claim")
    return raw, model


def parse(raw: str) -> dict:
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.S)
    if fence:
        text = fence.group(1).strip()
    start = text.find("{")
    if start > 0:
        text = text[start:]
    return json.loads(text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper")
    ap.add_argument("--dump-prompt", metavar="PATH",
                    help="write the exact prompt this layer would send to PATH and exit, so "
                         "whatever answers it answers this question rather than a paraphrase")
    ap.add_argument("--answer", metavar="PATH",
                    help="an answer produced elsewhere; validated exactly as a backend reply is")
    args = ap.parse_args()

    claims = load_claims(args.paper)
    system, user = build_prompt(args.paper, claims)

    if args.dump_prompt:
        out = Path(args.dump_prompt).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(system + "\n\n---\n\n" + user, encoding="utf-8")
        print(f"  plain-claim: prompt written to {out}  "
              f"({len(system)}c system + {len(user)}c user)")
        print("  answer it, then: --answer <file>")
        return 0

    if args.answer:
        src = Path(args.answer).expanduser().resolve()
        answer = parse(src.read_text(encoding="utf-8"))
        # Repo-relative where the answer was kept in the repo, which is where an answer worth
        # auditing belongs. An absolute path outside it is recorded as given and says,
        # correctly, that the artifact cannot be traced past this machine.
        try:
            where = src.relative_to(ROOT)
        except ValueError:
            where = src
        model = f"supplied:{where}"
    else:
        raw, model = ask_model(system, user)
        answer = parse(raw)

    problems = validate(answer, claims)
    if problems:
        print(f"{args.paper}: {len(problems)} problem(s), nothing written", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1

    out = write(args.paper, answer, claims, model=model)
    longest = max(len(answer[c["slug"]].strip()) for c in claims)
    print(f"  {args.paper:38} {len(claims)} claims · longest {longest} chars · "
          f"{out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
