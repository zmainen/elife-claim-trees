// Serve an artifact the pipeline produced.
//
//     /artifacts/<repo path>
//
// Most of what the layers produce was never served: the exports are copied into public/ and
// the rest — coverage, provenance, the abstract mappings, the syntheses, the reader runs —
// existed only in the repository, so the tab could offer a GitHub link and nothing else. A
// file the site does not hold cannot be copied to the clipboard or read in place, which is
// most of what a reader wants to do with one.
//
// Emitted at build from the repository file itself rather than copied into public/, so there
// is one copy of each artifact and git carries no duplicate to drift. The list comes from
// artifacts.json, which build-data.js writes by resolving every declared path — so what this
// route emits and what the pages offer are the same measurement.

import type { APIRoute, GetStaticPaths } from 'astro';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import index from '../../data/artifacts.json';

const served = Object.entries(index as Record<string, { at: string }>)
  .filter(([, e]) => e.at === 'artifacts')
  .map(([path]) => path);

const TYPE: Array<[RegExp, string]> = [
  [/\.jsonld$/, 'application/ld+json'],
  [/\.json$/, 'application/json'],
  [/\.md$/, 'text/markdown'],
  [/\.ttl$/, 'text/turtle'],
  [/\.csv$/, 'text/csv'],
];

export const getStaticPaths: GetStaticPaths = () => served.map(path => ({ params: { path } }));

export const GET: APIRoute = ({ params }) => {
  const path = params.path!;
  const type = TYPE.find(([re]) => re.test(path))?.[1] ?? 'text/plain';
  return new Response(readFileSync(join(process.cwd(), '..', path)), {
    headers: { 'content-type': `${type}; charset=utf-8` },
  });
};
