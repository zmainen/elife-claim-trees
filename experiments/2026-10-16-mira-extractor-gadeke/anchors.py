"""Counts, anchor check, and node dump for the extractor's Gädeke answer."""
import json, re, sys, unicodedata
from collections import Counter

RUN = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
paper = open(f"{RUN}/gadeke-2026-guilt-insula.md", encoding="utf-8").read()
ans = json.load(open(f"{RUN}/answer.json", encoding="utf-8"))

def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    return re.sub(r"\s+", " ", s).strip().lower()
npaper = norm(paper)

print("== answer.json ==")
print("nodes by type:", Counter(n["type"] for n in ans["nodes"]))
print("edges by relation:", Counter(e["relation"] for e in ans["edges"]))
print("paper:", json.dumps(ans.get("paper"), ensure_ascii=False)[:400])

exact = loose = missing = 0; bad = []
items = [("node", n["id"], n.get("anchor")) for n in ans["nodes"]] + \
        [("edge", f'{e["subject"]}-{e["relation"]}-{e["object"]}', e.get("anchor")) for e in ans["edges"]]
for kind, ident, a in items:
    if not a: continue
    if a in paper: exact += 1
    elif norm(a) in npaper: loose += 1; bad.append((kind, ident, "loose", a))
    else: missing += 1; bad.append((kind, ident, "MISSING", a))
print(f"anchors: {exact} verbatim, {loose} only after normalising quotes/dashes/space, {missing} not in text; "
      f"{sum(1 for n in ans['nodes'] if not n.get('anchor'))} nodes without anchor")
for b in bad: print("  ", *b)

print("\n== nodes ==")
for n in ans["nodes"]:
    print(f'[{n["id"]}] {n["type"]}: {n["text"]}')
    if n.get("description"): print(f'     desc: {n["description"][:300]}')
    if n.get("anchor"): print(f'     anchor: {n["anchor"]}')
print("\n== edges ==")
txt = {n["id"]: n["text"][:70] for n in ans["nodes"]}
for e in ans["edges"]:
    print(f'{e["subject"]} -{e["relation"]}-> {e["object"]}   | {txt.get(e["subject"],"?")}  =>  {txt.get(e["object"],"?")}')
