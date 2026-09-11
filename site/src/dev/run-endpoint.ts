// Run a layer, in dev.
//
//     POST /dev-run.json   {"paper": "...", "layer": "...", "deps": true}
//
// It lives outside `pages/` and is injected by a dev-only integration in astro.config.mjs,
// because the two obvious placements both fail: an underscore-prefixed file in `pages/` is
// silently excluded from routing, and a routed one carrying `prerender = false` makes the
// static build demand a server adapter it should not need.
//
// A published static site cannot run anything, so this exists only under `npm run dev` and
// refuses otherwise. The published build shows the same command as copy-and-run text: one
// declaration, two behaviours, and no page that promises a button it does not have.
//
// `deps: true` runs the unmet dependencies first, in dependency order — "generate the layer
// and the layers it rests on". Nothing is run that is already current.

import type { APIRoute } from 'astro';

export const prerender = false;

const DENIED = (msg: string, status = 400) =>
  new Response(JSON.stringify({ ok: false, error: msg }, null, 2) + '\n',
    { status, headers: { 'content-type': 'application/json' } });

export const POST: APIRoute = async ({ request }) => {
  if (!import.meta.env.DEV) {
    return DENIED('running layers is a dev-mode capability; the published site is static', 404);
  }

  let body: { paper?: string; layer?: string; deps?: boolean };
  try {
    body = await request.json();
  } catch {
    return DENIED('expected a JSON body');
  }
  const { paper, layer, deps = true } = body;
  if (!paper || !layer) return DENIED('paper and layer are both required');

  // Imported here rather than at module scope: these are Node built-ins, and the static
  // build must be able to parse this file without pulling them into a browser bundle.
  const { execFile } = await import('node:child_process');
  const { promisify } = await import('node:util');
  const path = await import('node:path');
  const run = promisify(execFile);

  const root = path.resolve(process.cwd(), '..');
  const args = ['scripts/pipeline.py', 'run', paper, layer];
  if (!deps) args.push('--no-deps');

  try {
    const { stdout, stderr } = await run('python3', args, {
      cwd: root, timeout: 15 * 60_000, maxBuffer: 8 * 1024 * 1024,
    });
    return new Response(JSON.stringify({ ok: true, paper, layer, stdout, stderr }, null, 2) + '\n',
      { headers: { 'content-type': 'application/json' } });
  } catch (e: any) {
    // A failed layer is an outcome, not a server error: the caller wants the output.
    return new Response(JSON.stringify({
      ok: false, paper, layer,
      code: e?.code ?? null, stdout: e?.stdout ?? '', stderr: e?.stderr ?? String(e),
    }, null, 2) + '\n', { status: 200, headers: { 'content-type': 'application/json' } });
  }
};
