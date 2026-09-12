#!/usr/bin/env python3
"""Check that the layer graph says what the layers actually do.

`pipeline/layers.yaml` is the only account of how this corpus is produced: what each layer
reads, what it writes, and what it therefore goes stale against. Everything downstream trusts
it — `state` computes staleness from `needs`, the site renders cells from it, and a reader is
told a cell is current on its authority.

Nothing checked it against the commands it declares. A layer whose command reads a file its
`needs` does not cover is not merely undocumented: its cell reads `current` while the input it
actually used moves underneath it, which is the one thing the ledger exists to prevent.

    python3 scripts/audit_layers.py            # the findings
    python3 scripts/audit_layers.py --strict   # exit non-zero if any are found

Each check answers one question and prints what it found, never a score.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline  # noqa: E402

# Paths a command mentions that are not a layer's business to declare: its own outputs, the
# runner, and the interpreter.
IGNORE = re.compile(r"^(python3?|node|cd|&&|--?\w|scripts/pipeline\.py)$")
PATHY = re.compile(r"(?:\.\./)?((?:[a-z_][a-z0-9_.-]*/)+[a-zA-Z0-9_{}.*-]+\.[a-z]+)")


def declared_paths(layer: dict, by_id: dict) -> set[str]:
    """Every path this layer is entitled to read, by its own declaration."""
    out: set[str] = set()
    for dep in layer.get("needs") or []:
        out |= set(by_id[dep].get("produces") or [])
    out |= set(layer.get("reads") or [])
    return {p.lstrip("./") for p in out}


def command_paths(layer: dict) -> set[str]:
    """Every path its command mentions, resolved to repo-relative.

    A command may change directory first — half of them are `cd extract && python3 …` — and a
    path written after that is relative to there, not to the root the declaration uses. The
    first version of this check did not know that and reported two correctly-declared layers
    as undeclared, which is the failure mode an audit can least afford: it spends the reader's
    trust on nothing and teaches them to skim the output.
    """
    cmd = layer.get("command") or ""
    base = ""
    m = re.match(r"\s*cd\s+([^\s&;]+)", cmd)
    if m:
        base = m.group(1).rstrip("/") + "/"
    out = set()
    for m in PATHY.finditer(cmd):
        raw = m.group(1)
        if IGNORE.match(raw):
            continue
        # `../` sits outside the capture group, so ask the whole match whether it was there.
        if m.group(0).startswith("../"):
            out.add(raw)                # up out of the cd, already repo-relative
        elif base and not raw.startswith(base):
            out.add(base + raw)
        else:
            out.add(raw)
    return out


def covers(declared: set[str], path: str) -> bool:
    """Does any declared path cover this one? A glob covers what it matches."""
    if path in declared:
        return True
    for d in declared:
        if "*" in d:
            pat = re.escape(d).replace(r"\*", "[^/]*")
            if re.fullmatch(pat, path):
                return True
        # A directory covers what is under it.
        if not d.endswith("/") and "." not in Path(d).name and path.startswith(d + "/"):
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strict", action="store_true", help="exit non-zero if anything is found")
    args = ap.parse_args()

    decl = pipeline.load()
    layers, by_id = decl["layers"], decl["by_id"]
    findings: list[tuple[str, str]] = []

    # ── 1. a command that reads what its needs do not cover ──────────────────────────────
    print("── Inputs a layer reads and does not declare ─────────────────────────────")
    print("   Its cell reads `current` while this input moves underneath it.\n")
    n = 0
    for l in layers:
        declared = declared_paths(l, by_id)
        produced = {p.lstrip("./") for p in (l.get("produces") or [])}
        for p in sorted(command_paths(l)):
            if covers(produced, p) or covers(declared, p):
                continue
            print(f"   {l['id']:18} reads {p}")
            findings.append((l["id"], f"undeclared input {p}"))
            n += 1
    if not n:
        print("   none")

    # ── 2. an output nothing consumes ────────────────────────────────────────────────────
    print("\n── Outputs no other layer needs ──────────────────────────────────────────")
    print("   Not wrong on its own — a leaf can be the point — but a layer meant to feed")
    print("   another and reaching nothing is how a measurement becomes a dead end.\n")
    consumed: set[str] = set()
    for l in layers:
        for dep in l.get("needs") or []:
            consumed |= {p.lstrip("./") for p in (by_id[dep].get("produces") or [])}
        consumed |= {p.lstrip("./") for p in (l.get("reads") or [])}
    n = 0
    for l in layers:
        outs = {p.lstrip("./") for p in (l.get("produces") or [])}
        if not outs or (outs & consumed):
            continue
        # An output the site renders is consumed — by a page rather than by a layer. Saying so
        # is the difference between "nothing reads this" and "no layer does", and only the
        # first is a dead end.
        site = [o for o in outs if o.startswith("site/src/data")]
        where = "read by the site" if site else "terminal"
        print(f"   {l['id']:18} {where}")
        if not site:
            findings.append((l["id"], "output consumed by no layer and not rendered"))
        n += 1
    if not n:
        print("   none")

    # ── 3. a layer that answers a question another layer measures ────────────────────────
    print("\n── Ordering: a layer placed before the evidence it needs ─────────────────")
    print("   `needs` is the only ordering there is, so a layer that asks a question")
    print("   answered downstream of it can only guess.\n")
    order = {l["id"]: i for i, l in enumerate(pipeline.order(decl) if hasattr(pipeline, "order")
                                              else [x["id"] for x in layers])} if False else {}
    # Reachability: which layers can a layer see, transitively?
    def upstream(lid: str, seen: set[str] | None = None) -> set[str]:
        seen = seen or set()
        for d in by_id[lid].get("needs") or []:
            if d not in seen:
                seen.add(d)
                upstream(d, seen)
        return seen

    # `answered_by` names a layer that asks the same question in the right place. Where one
    # exists the ordering is still odd and no longer costs anything, so the audit says so and
    # stops counting it: a finding that cannot be cleared is one people learn to scroll past.
    pairs = [("external-review", "coverage", None,
              "asks what the readers missed; coverage measures it, downstream"),
             ("edge-inference", "claim-tree", "edge-review",
              "decides relations from the candidates; a claim written later can never get one")]
    n = 0
    for asker, measurer, answered_by, why in pairs:
        if asker not in by_id or measurer not in by_id or measurer in upstream(asker):
            continue
        if answered_by and answered_by in by_id and measurer in upstream(answered_by):
            print(f"   {asker:18} {why}")
            print(f"   {'':18} answered downstream by `{answered_by}`")
            continue
        print(f"   {asker:18} {why}")
        findings.append((asker, f"ordered before {measurer}"))
        n += 1
    if not n:
        print("   none outstanding")

    # ── 4. what the site publishes that `make data` cannot regenerate ────────────────────
    print("\n── Site data no build step regenerates ───────────────────────────────────")
    print("   `make build` regenerates what it can and publishes whatever else is")
    print("   committed, so a stale artifact reaches the site with nothing in the way.\n")
    mk = (ROOT / "Makefile").read_text(encoding="utf-8")
    data_step = mk.split("data:", 1)[1].split("\n\n", 1)[0] if "data:" in mk else ""
    n = 0
    for l in layers:
        for p in (l.get("produces") or []):
            if not p.startswith("site/src/data"):
                continue
            script = (l.get("command") or "").split()
            named = any(s.split("/")[-1] in data_step for s in script if s.endswith(".py"))
            if not named:
                print(f"   {l['id']:18} {p}")
                findings.append((l["id"], f"site data not in `make data`: {p}"))
                n += 1
    if not n:
        print("   none")

    # ── 5. layers with output and no approval, anywhere ──────────────────────────────────
    print("\n── The human gate ───────────────────────────────────────────────────────")
    approvals = 0
    for p in pipeline.papers():
        approvals += len(pipeline.read_approvals(p))
    print(f"   approvals recorded across the whole corpus: {approvals}")
    if approvals == 0:
        findings.append(("corpus", "no layer version has ever been approved by a person"))

    print(f"\n{len(findings)} finding(s)")
    return 1 if (args.strict and findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
