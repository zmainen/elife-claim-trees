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

// ── whole-tree adjudication (#82) ─────────────────────────────────────────────
//
// A second reading the gap-claim surface does not cover: a person going through a whole claim
// tree and recording a verdict on every claim and every edge, bound to the version they read.
// It lands in its own append-only file, one per version, beside the tree:
//
//     runs/<paper>/claim-tree.v<N>.verdicts.jsonl
//
// The vocabulary mirrors extract/elife_extract/verdicts.py; a value outside it is refused here,
// where the caller can still be told why, rather than written and read back as a typo.

const CLAIM_VERDICTS = ['keep', 'strike', 'merge-into', 'part-of'];
const CLAIM_VERDICTS_WITH_TARGET = ['merge-into', 'part-of'];
const EDGE_VERDICTS = ['ok', 'wrong-direction', 'wrong-relation', 'strike', 'missing'];
// The nine roles a claim tree assigns (vocabulary.py). A reader may correct one to any of them.
const TREE_ROLES = ['hypothesis', 'prediction', 'empirical', 'control', 'methodological',
  'scope', 'synthesis', 'interpretation', 'literature-context'];
const PAPER_RE = /^[a-z0-9][a-z0-9-]*$/;

const verdictFile = async (paper: string, version: number) => {
  const path = await import('node:path');
  return path.resolve(process.cwd(), '..', 'runs', paper, `claim-tree.v${version}.verdicts.jsonl`);
};

async function handleVerdict(body: Record<string, any>, by: string, when: string): Promise<Response> {
  const paper = str(body.paper);
  const version = Number(body.version);
  if (!paper || !PAPER_RE.test(paper)) return DENIED('a verdict needs a valid paper slug');
  if (!Number.isInteger(version) || version < 1) return DENIED('a verdict is bound to a tree version');

  const { appendFile, writeFile, mkdir, access } = await import('node:fs/promises');
  const path = await import('node:path');
  const file = await verdictFile(paper, version);
  await mkdir(path.dirname(file), { recursive: true });

  const op = str(body.op) || 'append';

  // Pre-fill every claim `keep` and every edge `ok`, all `considered: false`, so the reading is
  // editing rather than authoring. Refuses to clobber a file that already has verdicts unless
  // asked, because that file may already be a reading.
  if (op === 'skeleton') {
    const claims: string[] = Array.isArray(body.claims) ? body.claims.map(str).filter(Boolean) : [];
    const edges: any[] = Array.isArray(body.edges) ? body.edges : [];
    let exists = true;
    try { await access(file); } catch { exists = false; }
    if (exists && !body.force) {
      return DENIED('a verdict file already exists for this version; pass force to replace it');
    }
    const lines = [
      ...claims.map(slug => ({ kind: 'claim', slug, verdict: 'keep', considered: false, by, when })),
      ...edges.map((e: any) => ({
        kind: 'edge', source: str(e[0]), target: str(e[1]), relation: str(e[2]),
        verdict: 'ok', considered: false, by, when,
      })),
    ];
    await writeFile(file, lines.map(l => JSON.stringify(l)).join('\n') + '\n', 'utf8');
    return new Response(JSON.stringify({ ok: true, wrote: lines.length }, null, 2) + '\n',
      { headers: { 'content-type': 'application/json' } });
  }

  // Mark the reading finished: record the approval through the same code path as
  // `pipeline.py approve` — scripts/verdicts.py, which validates the file first.
  if (op === 'approve') {
    const { execFile } = await import('node:child_process');
    const { promisify } = await import('node:util');
    const run = promisify(execFile);
    try {
      const { stdout } = await run('python3',
        ['scripts/verdicts.py', 'approve', paper, '--by', by],
        { cwd: path.resolve(process.cwd(), '..') });
      return new Response(JSON.stringify({ ok: true, approved: true, output: stdout }, null, 2) + '\n',
        { headers: { 'content-type': 'application/json' } });
    } catch (e: any) {
      return DENIED(`approve failed: ${e?.stderr || e?.message || e}`, 500);
    }
  }

  // A single verdict line. `considered: true` is what tells a reader's decision apart from the
  // skeleton's default; the surface sends it on every posted verdict.
  const kind = str(body.kind);
  let record: Record<string, unknown>;
  if (kind === 'claim') {
    const slug = str(body.slug), verdict = str(body.verdict);
    if (!slug) return DENIED('a claim verdict needs a slug');
    if (!CLAIM_VERDICTS.includes(verdict)) return DENIED(`verdict is one of ${CLAIM_VERDICTS.join(', ')}`);
    const target = str(body.target);
    if (CLAIM_VERDICTS_WITH_TARGET.includes(verdict) && !target) {
      return DENIED(`a ${verdict} verdict needs a target claim`);
    }
    const role = str(body.role);
    if (role && !TREE_ROLES.includes(role)) return DENIED(`role is one of ${TREE_ROLES.join(', ')}`);
    record = {
      kind: 'claim', slug, verdict,
      ...(target ? { target } : {}), ...(role ? { role } : {}),
      ...(str(body.panel) ? { panel: str(body.panel) } : {}),
      ...(str(body.why) ? { why: str(body.why) } : {}),
      considered: true, by, when,
    };
  } else if (kind === 'edge') {
    const source = str(body.source), target = str(body.target), relation = str(body.relation);
    const verdict = str(body.verdict);
    if (!source || !target || !relation) return DENIED('an edge verdict needs source, target and relation');
    if (!EDGE_VERDICTS.includes(verdict)) return DENIED(`verdict is one of ${EDGE_VERDICTS.join(', ')}`);
    record = {
      kind: 'edge', source, target, relation, verdict,
      ...(str(body.corrected) ? { corrected: str(body.corrected) } : {}),
      considered: true, by, when,
    };
  } else if (kind === 'ruling') {
    const question = str(body.question), answer = str(body.answer);
    if (!question || !answer) return DENIED('a ruling needs a question and an answer');
    record = {
      kind: 'ruling', question, answer,
      ...(str(body.why) ? { why: str(body.why) } : {}),
      considered: true, by, when,
    };
  } else {
    return DENIED('a verdict is one of kind claim, edge or ruling');
  }

  try {
    await appendFile(file, JSON.stringify(record) + '\n', 'utf8');
  } catch (e: any) {
    return DENIED(`could not append to the verdict file: ${e?.message ?? e}`, 500);
  }
  return new Response(JSON.stringify({ ok: true, record }, null, 2) + '\n',
    { headers: { 'content-type': 'application/json' } });
}

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

  // Whole-tree adjudication (#82) lands in its own per-version verdict file; the gap-claim
  // decision path below is unchanged.
  if (body.file === 'verdicts') {
    return handleVerdict(body, by, decided_at);
  }

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
