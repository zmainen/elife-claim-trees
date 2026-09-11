// Record a review decision, in dev.
//
//     POST /dev-review.json   {"paper": "…", "uid": "results-143", "decision": "accept", …}
//     POST /dev-review.json   {"type": "edge", "paper": "…", "claim": "…", "relation": "…", …}
//
// Injected by the same dev-only integration as /dev-run.json, for the same reason and in the
// same shape: a published static site has nothing to append to, and shipping a server adapter
// for one endpoint would make the whole site dynamic to serve a file write. Outside dev this
// refuses with 404 and the draft card says so, rather than offering a button that quietly
// does nothing.
//
// It appends and never rewrites. A reviewer who changes their mind writes a second record for
// the same uid: the file is the sequence of decisions rather than the current state of them,
// the reader and `scripts/promote.py` both take the last record for a uid, and the earlier one
// survives as evidence of what a person thought before they thought again.
//
// An edge record is not a decision about a draft at all. It says that a person reading the
// claim card disputes a relation the graph asserts — a report, not an edit, which is why it
// lands in the same append-only file and changes nothing.

import type { APIRoute } from 'astro';

export const prerender = false;

const DENIED = (msg: string, status = 400) =>
  new Response(JSON.stringify({ ok: false, error: msg }, null, 2) + '\n',
    { status, headers: { 'content-type': 'application/json' } });

const DECISIONS = ['accept', 'edit', 'reject'];

// The five roles `gap-claim` may assign. A reviewer may change a draft's role, and a role
// outside this set would reach `promote.py`'s CLAIM_TYPE table as a silent fall-through to
// `empirical` — so it is refused here, where the caller can still be told why.
const ROLES = ['empirical', 'control', 'interpretation', 'scope', 'literature-context'];

const str = (v: unknown) => (typeof v === 'string' ? v.trim() : '');

export const POST: APIRoute = async ({ request }) => {
  if (!import.meta.env.DEV) {
    return DENIED('recording a decision is a dev-mode capability; the published site is static', 404);
  }

  let body: Record<string, any>;
  try {
    body = await request.json();
  } catch {
    return DENIED('expected a JSON body');
  }

  // Five decisions are already recorded as `unnamed` because the surface that took them never
  // asked hard enough. An unsigned record is worth much less than a signed one, so it is the
  // one field with no default.
  const by = str(body.by);
  if (!by) return DENIED('a decision needs a name: the record says who made it');
  const decided_at = str(body.decided_at) || new Date().toISOString().replace(/\.\d+Z$/, 'Z');

  let record: Record<string, unknown>;
  if (body.type === 'edge') {
    const paper = str(body.paper), claim = str(body.claim);
    const relation = str(body.relation), target = str(body.target);
    if (!paper || !claim || !relation || !target) {
      return DENIED('an edge flag needs paper, claim, relation and target');
    }
    record = { type: 'edge', paper, claim, relation, target, note: str(body.note), by, decided_at };
  } else {
    const paper = str(body.paper), uid = str(body.uid), decision = str(body.decision);
    if (!paper || !uid) return DENIED('paper and uid are both required');
    if (!DECISIONS.includes(decision)) {
      return DENIED(`decision is one of ${DECISIONS.join(', ')}`);
    }
    const role = str(body.role);
    if (role && !ROLES.includes(role)) return DENIED(`role is one of ${ROLES.join(', ')}`);
    record = {
      paper, uid, slug: str(body.slug), decision,
      claim: str(body.claim), role, note: str(body.note), by, decided_at,
    };
  }

  // Imported here rather than at module scope: these are Node built-ins, and the static build
  // must be able to parse this file without pulling them into a browser bundle.
  const { appendFile, mkdir } = await import('node:fs/promises');
  const path = await import('node:path');
  const file = path.resolve(process.cwd(), '..', 'review', 'gap-claim-decisions.jsonl');

  try {
    await mkdir(path.dirname(file), { recursive: true });
    await appendFile(file, JSON.stringify(record) + '\n', 'utf8');
  } catch (e: any) {
    return DENIED(`could not append to review/gap-claim-decisions.jsonl: ${e?.message ?? e}`, 500);
  }

  return new Response(JSON.stringify({ ok: true, record }, null, 2) + '\n',
    { headers: { 'content-type': 'application/json' } });
};
