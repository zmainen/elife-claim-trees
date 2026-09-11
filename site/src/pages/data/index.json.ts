// The catalogue: every addressable cell, and the declaration behind it.
//
//     /data/index.json
//
// The matrix is the query with both paper and layer unbound, so this is that query as data.
// A consumer asking "what is stale" or "which papers have no coverage" reads this rather than
// crawling ten pages.

import type { APIRoute } from 'astro';
import {
  layers, groups, papers, cells, titleOf, fill_of, inState,
} from '../../lib/pipeline';

export const GET: APIRoute = () => {
  const body = {
    generated_from: 'pipeline/layers.yaml + runs/<paper>/ledger.jsonl',
    groups,
    layers: layers.map(l => ({
      id: l.id, title: l.title, question: l.question, kind: l.kind, scope: l.scope,
      group: l.group ?? null, needs: l.needs ?? [], views: l.views ?? [],
      issue: l.issue ?? null, open: l.open ?? false,
      requires_human: l.requires_human ?? false, reviews: l.reviews ?? null,
    })),
    papers: papers.map(p => ({
      slug: p,
      title: titleOf(p),
      fill: fill_of(p),
      cells: cells(p).map(c => ({
        layer: c.layer.id, state: c.state, version: c.v ?? null,
        ran: c.ran ?? null, data: c.dataHref,
      })),
    })),
    // The two queries worth having ready: what is wrong, and what is missing.
    stale: inState('stale', 'blocked').map(c => ({
      paper: c.paper, layer: c.layer.id, state: c.state,
      moved: c.moved ?? null, blocked_by: c.blockedBy ?? null,
    })),
    absent: inState('absent').map(c => ({
      paper: c.paper, layer: c.layer.id, command: c.command ?? null,
    })),
  };
  return new Response(JSON.stringify(body, null, 2) + '\n', {
    headers: { 'content-type': 'application/json; charset=utf-8' },
  });
};
