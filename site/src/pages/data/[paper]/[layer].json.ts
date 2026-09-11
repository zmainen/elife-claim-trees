// Fetch one cell.
//
//     /data/<paper>/<layer>.json
//
// The same resolver the pages use, served as data. This is what makes a version exportable
// rather than merely visible: a candidate — a second prompt variant on one paper — is
// reachable at its own address and can be diffed against the one that shipped without
// anyone screen-scraping a page.
//
// Pre-rendered in the static build, so the published site carries every cell as a file.

import type { APIRoute, GetStaticPaths } from 'astro';
import { papers, paperLayers, cell } from '../../../lib/pipeline';

export const getStaticPaths: GetStaticPaths = () =>
  papers.flatMap(paper =>
    paperLayers.map(layer => ({ params: { paper, layer: layer.id } })));

export const GET: APIRoute = ({ params }) => {
  const c = cell(params.paper!, params.layer!);
  if (!c) {
    return new Response(JSON.stringify({ error: 'no such cell' }), {
      status: 404, headers: { 'content-type': 'application/json' },
    });
  }
  return new Response(JSON.stringify({
    paper: c.paper,
    layer: {
      id: c.layer.id, title: c.layer.title, question: c.layer.question,
      kind: c.layer.kind, group: c.layer.group, needs: c.layer.needs ?? [],
      views: c.layer.views ?? [], reviews: c.layer.reviews,
      requires_human: c.layer.requires_human, issue: c.layer.issue,
    },
    version: c.v ?? null,
    versions: c.versions,
    state: c.state,
    ran: c.ran ?? null,
    by: c.by ?? null,
    note: c.note ?? null,
    // Present only when they explain the state, so a consumer can act on their presence.
    moved: c.moved ?? null,
    lost: c.lost ?? null,
    blocked_by: c.blockedBy ?? null,
    unrecorded_upstream: c.unrecordedUpstream ?? null,
    produces: c.produces,
    command: c.command ?? null,
    href: c.href,
  }, null, 2) + '\n', {
    headers: { 'content-type': 'application/json; charset=utf-8' },
  });
};
