#!/usr/bin/env python3
"""Apply decided review items to the claim files.

The queue holds judgements; this carries them out. It is deliberately unwilling:

  * dry run by default — `--write` is required to touch a file
  * refuses while any item in the topic is `pending`, so a half-reviewed queue cannot
    half-apply and leave the corpus in a state nobody chose
  * reciprocity-aware — removing a pair removes both declared directions, which is why 18
    pairs are 30 edges
  * idempotent — an item already applied is detected and skipped, so a re-run after a partial
    failure does not double-edit
  * records why — every touched claim gets a line saying which review changed it, so the edit
    is explicable later without archaeology through commit messages

  python3 scripts/apply_review.py dissociates-with            # show what would change
  python3 scripts/apply_review.py dissociates-with --write
  python3 scripts/apply_review.py dissociates-with --paper gadeke-2026-guilt-insula --write
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE_DIR = os.path.join(ROOT, "review")
CLAIMS = os.path.join(ROOT, "claims")

# What each decided type does to the edge. `keep` types change nothing per-edge; only the
# declaration in export_mira.py changes, and that is a one-line edit made by hand.
EFFECT = {
    "parallel": ("remove", None),
    "tension": ("retype", "qualifies"),
    "selective": ("keep", None),
    "property": ("keep", None),
}


def claim_path(paper, slug):
    return os.path.join(CLAIMS, paper, f"{slug}.md")


def strip_relation(text, key, target):
    """Remove `target` from a top-level `key:` list or a belongings entry. Returns (text, n)."""
    n = 0

    # Top-level list form:  key:\n  - target
    def drop_from_list(m):
        nonlocal n
        body = m.group(2)
        kept = [ln for ln in body.splitlines()
                if ln.strip() not in (f"- {target}", f"- '{target}'", f'- "{target}"')]
        if len(kept) == len(body.splitlines()):
            return m.group(0)
        n += 1
        if not [k for k in kept if k.strip()]:
            return ""                      # the key had only this target; drop the key too
        return m.group(1) + "\n".join(kept) + "\n"

    text = re.sub(rf"^({re.escape(key)}:\n)((?:[ \t]+- .*\n)+)", drop_from_list, text,
                  flags=re.M)

    # belongings form:  - relation: key\n    target: target
    pat = re.compile(rf"^[ \t]*- relation: {re.escape(key)}\n[ \t]*target: {re.escape(target)}\n",
                     flags=re.M)
    text, k = pat.subn("", text)
    n += k
    return text, n


def add_relation(text, key, target):
    """Add `target` under a top-level `key:` list, creating the key if absent."""
    if re.search(rf"^{re.escape(key)}:\n(?:[ \t]+- .*\n)*[ \t]+- {re.escape(target)}\s*$",
                 text, flags=re.M):
        return text, 0
    m = re.search(rf"^({re.escape(key)}:\n)", text, flags=re.M)
    if m:
        return text[:m.end()] + f"  - {target}\n" + text[m.end():], 1
    # Insert before `assertions:`, which every claim file has.
    m = re.search(r"^assertions:", text, flags=re.M)
    ins = f"{key}:\n  - {target}\n\n"
    if m:
        return text[:m.start()] + ins + text[m.start():], 1
    return text, 0


def note_line(item, action):
    return (f"\nReview {item['id']}: relation `dissociates-with` → {action} "
            f"({item['decision']}), decided by {item.get('decided_by') or 'unrecorded'}"
            f"{'. ' + item['note'] if item.get('note') else ''}\n")


def apply_item(item, write, changed):
    kind, newkey = EFFECT[item["decision"]]
    if kind == "keep":
        return 0

    edits = 0
    # A reciprocal pair declares the relation in both directions; both go.
    directions = [(item["a"], item["b"])]
    if item["reciprocal"]:
        directions.append((item["b"], item["a"]))

    for src, dst in directions:
        p = claim_path(item["paper"], src)
        if not os.path.isfile(p):
            print(f"    ! missing {os.path.relpath(p, ROOT)}")
            continue
        text = changed.get(p) or io.open(p, encoding="utf-8").read()
        text2, n = strip_relation(text, "dissociates-with", dst)
        if n == 0:
            continue                        # already applied, or never present
        if kind == "retype":
            text2, _ = add_relation(text2, newkey, dst)
        text2 = text2.rstrip("\n") + "\n" + note_line(item, kind)
        changed[p] = text2
        edits += 1
        arrow = "removed" if kind == "remove" else f"→ {newkey}"
        print(f"    {os.path.relpath(p, ROOT)}  {src} -dissociates-with-> {dst}  {arrow}")
    return edits


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("topic")
    ap.add_argument("--paper")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    path = os.path.join(QUEUE_DIR, f"{a.topic}.json")
    if not os.path.isfile(path):
        sys.exit(f"no queue at {os.path.relpath(path, ROOT)} — run scripts/review_queue.py")
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)

    items = [i for i in doc["items"] if not a.paper or i["paper"] == a.paper]
    pending = [i for i in items if i["decision"] == "pending"]
    if pending:
        scope = f"for {a.paper}" if a.paper else "in this topic"
        print(f"{len(pending)} of {len(items)} item(s) {scope} are still pending.")
        print("Nothing is applied while a decision is outstanding: a half-reviewed queue would "
              "leave the corpus in a state nobody chose.")
        for i in pending[:5]:
            print(f"    pending  {i['a']} ↔ {i['b']}"
                  + (f"   (proposed: {i['proposed']})" if i.get("proposed") else ""))
        if len(pending) > 5:
            print(f"    … and {len(pending) - 5} more")
        return 1

    bad = [i for i in items if i["decision"] not in EFFECT]
    if bad:
        sys.exit(f"unknown decision {bad[0]['decision']!r} on {bad[0]['id']} — "
                 f"expected one of {', '.join(EFFECT)}")

    changed, edits = {}, 0
    for i in items:
        edits += apply_item(i, a.write, changed)

    kept = sum(1 for i in items if EFFECT[i["decision"]][0] == "keep")
    print(f"\n{len(items)} decided item(s): {edits} edge edit(s) across {len(changed)} file(s), "
          f"{kept} needing no per-edge change")

    if not a.write:
        print("dry run — nothing written. Re-run with --write to apply.")
        return 0
    for p, text in changed.items():
        io.open(p, "w", encoding="utf-8").write(text)
    print(f"wrote {len(changed)} file(s). Re-run export_mira.py, formats_report.py and "
          f"corpus_facts.py, then scripts/check_relations.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
