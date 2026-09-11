#!/usr/bin/env python3
"""Assemble the review queue: every gap-claim draft awaiting a person's decision.

The drafting layer produces candidates and the corpus takes none of them until somebody
decides. This builds the surface that decision is made on: one card per draft, carrying the
paper's own sentence that prompted it, the sentences either side, the figure panel it points
at, and the reason it was proposed. Publish the result as an Artifact and the decisions come
back through `scripts/promote.py`.

    python3 scripts/build_review_queue.py     # writes site/public/review-queue.html
"""
import json, re, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HERE = REPO / 'site' / 'public'
sys.path.insert(0, str(REPO / 'scripts'))
sys.path.insert(0, str(REPO / 'extract'))
import os
os.chdir(REPO)
from gap_claims import neighbours                                  # noqa: E402

corpus = json.load(open(REPO / 'site/src/data/claims.json'))
titles = {p['slug']: p['title'] for p in corpus['papers']}
# One figure URL per figure number, taken from whichever claim of that paper cites it.
figs = {}
for p in corpus['papers']:
    for c in p['claims']:
        u = c.get('figureUrl')
        if not u:
            continue
        m = re.search(r'fig(?:ure)?\s*0*(\d+)', (c.get('panel') or '').lower())
        if m:
            figs.setdefault((p['slug'], m.group(1)), u)

items = []
for out in sorted(REPO.glob('runs/*/gap-claim.output.json')):
    paper = out.parent.name
    d = json.loads(out.read_text())
    around = neighbours(paper)
    why_gap = {s['uid']: s.get('why', '')
               for s in json.loads((REPO / f'mappings/{paper}.json').read_text())['spans']}
    for c in d['candidates']:
        before, after = around.get(c['uid'], ('', ''))
        fnum = re.search(r'fig(?:ure)?\s*0*(\d+)', (c.get('panel') or '').lower())
        fig = figs.get((paper, fnum.group(1))) if fnum else None
        items.append({
            'paper': paper,
            'paperTitle': titles.get(paper, paper),
            'paperGaps': len(d['candidates']) + len(d['declined']),
            'uid': c['uid'],
            'span': c['span'],
            'before': before[:400],
            'after': after[:400],
            'slug': c['slug'],
            'claim': c['claim'],
            'role': c['role'],
            'panel': c.get('panel') or '',
            'why': c['why'],
            'whyGap': why_gap.get(c['uid'], ''),
            'figure': fig,
            'figureLabel': f"Figure {fnum.group(1)}" if fnum and fig else '',
        })

# Gädeke first: it is the paper the reviewer knows best, and its drafts are the harder calls.
items.sort(key=lambda i: (i['paper'] != 'gadeke-2026-guilt-insula', i['paper'], i['uid']))
tpl = (HERE / 'review-queue.template.html').read_text()
page = tpl.replace('{{DATA}}', json.dumps(items, ensure_ascii=False).replace('</', '<\\/'))
(HERE / 'review-queue.html').write_text(page)
print(f"{len(items)} items, {len(page)} bytes")
for i in items:
    print(f"  {i['paper'][:22]:24} {i['uid']:14} {i['slug'][:44]:46} fig={'y' if i['figure'] else '-'} ctx={'y' if i['before'] else '-'}")
