// What a layer is made of, read from the repository at build.
//
// A layer page could say everything about a layer except the two things that define it: the
// prompt or script it runs under, and what that produced. Both were rendered as bare paths —
// `extract/prompts/results-reader.md`, `runs/{paper}/results-reader.output.json`, the second
// still carrying its placeholder — so the page named its own definition and its own output
// and showed neither.
//
// This reads both off disk during the build. Nothing is copied into src/data first, and there
// is no generator to run: a prompt edited in the repository is a prompt changed on the site,
// with no committed intermediate to go stale between them. The build's working directory is
// site/, so the repository root is one level up — the same resolution lib/markdown.ts uses.

import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join, basename, extname } from 'node:path';
import matter from 'gray-matter';
import type { LayerDecl } from './pipeline';
import type { ClaimLite } from './compare';

const ROOT = join(process.cwd(), '..');
const REPO = 'https://github.com/zmainen/elife-claim-trees/blob/main';

/** What kind of thing a declared input is, which decides how it can be shown. */
export type SourceKind = 'prompt' | 'code' | 'data' | 'prose';

export interface Source {
  /** The declared path, with {paper} substituted where one was given. */
  path: string;
  kind: SourceKind;
  /** False for a path the declaration names and the repository does not have. */
  exists: boolean;
  lines: number;
  /** Full text — prompts and prose are shown whole; code is not. */
  text?: string;
  /** A code file's leading docstring or comment block: what it says it does. */
  summary?: string;
  href: string;
}

const kindOf = (p: string): SourceKind =>
  /^extract\/prompts\//.test(p) ? 'prompt'
    : /\.(py|js|ts|sh)$/.test(p) ? 'code'
    : /\.(md|markdown|txt)$/.test(p) ? 'prose'
    : 'data';

/** A Python module docstring or a leading `#`/`//` comment block — the file's own account of
 *  itself. Preferred over an excerpt of the code, which explains nothing to a reader who came
 *  to find out what the layer does. */
function header(text: string): string | undefined {
  const doc = text.match(/^(?:#![^\n]*\n)?\s*(?:"""|''')([\s\S]*?)(?:"""|''')/);
  if (doc) return doc[1].trim();
  const lines: string[] = [];
  for (const line of text.split('\n')) {
    if (/^#!/.test(line)) continue;
    const m = line.match(/^\s*(?:#|\/\/)\s?(.*)$/);
    if (!m) break;
    lines.push(m[1]);
  }
  const block = lines.join('\n').trim();
  return block || undefined;
}

/** One declared path, resolved. */
export function source(declared: string, paper?: string): Source {
  const path = declared.replace(/\{paper\}/g, paper ?? '{paper}');
  const abs = join(ROOT, path);
  const exists = !paper && path.includes('{paper}') ? false : existsSync(abs);
  const base: Source = {
    path, kind: kindOf(path), exists, lines: 0, href: `${REPO}/${path}`,
  };
  if (!exists) return base;
  const text = readFileSync(abs, 'utf8');
  const lines = text.split('\n').length;
  return base.kind === 'code'
    ? { ...base, lines, summary: header(text) }
    : { ...base, lines, text };
}

/** Everything a layer declares it reads besides its dependencies' outputs. */
export const sources = (layer: LayerDecl, paper?: string): Source[] =>
  (layer.reads ?? []).map(r => source(r, paper));

// ── what a run produced ───────────────────────────────────────────────────────

export interface Records {
  /** The artifact these came out of. */
  path: string;
  /** The key holding them, when the file is an object; absent when it is a bare list. */
  key?: string;
  records: Record<string, unknown>[];
  /** Field names in first-appearance order — the output's shape, read off the output. */
  fields: string[];
  /** The scalars beside the records: model, paper, counts. */
  meta: Record<string, unknown>;
}

/** A markdown artifact, for the layers whose output is a document rather than a table. */
export interface Document { path: string; text: string; truncated: boolean }

/** The long text inside a JSON artifact — `prepare` writes the abstract, the results prose,
 *  the captions and the methods as four fields of one file, and the only useful view of that
 *  is the text itself. A field is a section when it is long enough to be prose rather than a
 *  label. */
export interface Section { key: string; text: string; chars: number }

const DOC_CAP = 80_000;

/** The records in a parsed artifact, if it has any.
 *
 * A bare list is the records. An object's records are its first array-of-objects value:
 * `claims` for a reader, `spans` for an adjudication, `results` for a verification run,
 * `items` for the prediction rule. Everything scalar beside them is the meta. A file with no
 * such array — coverage's nested counts, the formats report's measurements — returns null,
 * and the caller shows the meta alone rather than an empty table. */
function parse(path: string, raw: string): Records | null {
  let data: unknown;
  try { data = JSON.parse(raw); } catch { return null; }

  const isTable = (v: unknown): v is unknown[] =>
    Array.isArray(v) && v.length > 0 && typeof v[0] === 'object' && v[0] !== null;

  let records: unknown[] | null = null;
  let key: string | undefined;
  const meta: Record<string, unknown> = {};
  const nested: [string, Record<string, unknown>][] = [];
  if (Array.isArray(data)) {
    records = data;
  } else if (data && typeof data === 'object') {
    for (const [k, v] of Object.entries(data as Record<string, unknown>)) {
      if (!records && isTable(v)) { records = v; key = k; }
      else if (v === null || typeof v !== 'object') meta[k] = v;
      else if (!Array.isArray(v)) nested.push([k, v as Record<string, unknown>]);
    }
    // One level down, when the top holds only counts. `coverage` writes its totals at the top
    // and the spans nobody accounted for under `spans.orphans`, and those spans are the whole
    // finding — a page that showed the counts and not the list showed the summary of a report
    // instead of the report.
    if (!records) {
      for (const [k, obj] of nested) {
        for (const [k2, v] of Object.entries(obj)) {
          if (isTable(v)) { records = v; key = `${k}.${k2}`; break; }
          if (v === null || typeof v !== 'object') meta[`${k}.${k2}`] = v;
        }
        if (records) break;
      }
    }
  }
  // Two is the threshold for calling an array a table. A one-element array is structure — the
  // OXA export's single `children` entry, whose value is the whole document — and rendering it
  // as a table of one row with a JSON blob in a cell tells a reader nothing the file would not
  // have told them better.
  if (!records || records.length < 2) {
    return Object.keys(meta).length ? { path, records: [], fields: [], meta } : null;
  }

  const rows = records.filter(r => r && typeof r === 'object') as Record<string, unknown>[];
  const fields: string[] = [];
  for (const r of rows) for (const f of Object.keys(r)) if (!fields.includes(f)) fields.push(f);
  return { path, key, records: rows, fields, meta };
}

/** Read one produced path as records, or null when it is not a JSON table. */
export function records(path: string): Records | null {
  const abs = join(ROOT, path);
  if (!/\.json$/.test(path) || !existsSync(abs)) return null;
  return parse(path, readFileSync(abs, 'utf8'));
}

/** Read one produced path as a document. */
export function document(path: string): Document | null {
  const abs = join(ROOT, path);
  if (!/\.(md|markdown|txt)$/.test(path) || !existsSync(abs)) return null;
  const text = readFileSync(abs, 'utf8');
  return { path, text: text.slice(0, DOC_CAP), truncated: text.length > DOC_CAP };
}

const SECTION_MIN = 400;

/** The prose fields of a JSON artifact, longest first. */
export function sections(path: string): Section[] {
  const abs = join(ROOT, path);
  if (!/\.json$/.test(path) || !existsSync(abs)) return [];
  let data: unknown;
  try { data = JSON.parse(readFileSync(abs, 'utf8')); } catch { return []; }
  if (!data || typeof data !== 'object' || Array.isArray(data)) return [];
  return Object.entries(data as Record<string, unknown>)
    .filter(([, v]) => typeof v === 'string' && v.length >= SECTION_MIN)
    .map(([key, v]) => ({ key, text: v as string, chars: (v as string).length }));
}

/** Whatever this cell produced that can be shown, and the path it came from.
 *
 * The path is returned even when nothing in the file can be rendered, because the link is
 * worth having on its own: the previous version of this page showed neither the output nor a
 * way to reach it. */
export function output(produces: string[]):
    { path?: string; records?: Records; document?: Document; sections?: Section[] } {
  for (const p of produces) {
    const d = document(p);
    if (d) return { path: p, document: d };
    const r = records(p);
    if (r) return { path: p, records: r, sections: sections(p) };
    if (existsSync(join(ROOT, p))) return { path: p };
  }
  return {};
}

// ── versions, for the two-version comparison ────────────────────────────────────
//
// A cell's earlier versions are addressable on disk, and this reads them into claim lists the
// aligner can diff. Two shapes, because two mechanisms keep them:
//
//   claim-tree  archives the whole tree into runs/<paper>/claim-tree.v<N>/ on each --replace,
//               so an earlier version is a directory of claim files.
//   the reader, reconcile, review and edge layers each overwrite one output file per run, so
//               scripts/pipeline.py keeps a copy beside it as <name>.v<N>.<ext>. Nothing is
//               backfilled, so a version is offered only where its bytes were actually kept.
//
// The current version is the live output — claims/<paper>/ or the layer's own output file —
// and carries the ledger's latest version number.

/** A version of a cell, reduced to the claim list a diff needs. */
export interface LayerVersion {
  v: number;
  /** Where its bytes are: the live output, or a kept copy. */
  source: 'current' | 'kept';
  claims: ClaimLite[];
  /** The file or directory the claims were read from, repo-relative. */
  path: string;
}

/** The claims in a reader/reconciler/edge output file: the first array-of-objects value,
 *  reduced to text, role and panel. Reuses the same `parse` the table view reads through. */
function claimsFromOutput(rel: string): ClaimLite[] {
  const r = records(rel);
  if (!r) return [];
  const textField = ['claim', 'text', 'sentence', 'from'].find(f => r.fields.includes(f));
  return r.records.map(rec => ({
    text: String(rec[textField ?? 'claim'] ?? ''),
    role: (rec.role ?? rec.claim_type ?? null) as string | null,
    panel: (rec.panel ?? null) as string | null,
    slug: (rec.slug ?? null) as string | null,
  })).filter(c => c.text);
}

/** The claims in a claim-tree directory: one markdown file per claim, panel read off the
 *  first assertion where the writer records it. index.md is the paper, not a claim. */
function claimsFromTree(absDir: string): ClaimLite[] {
  let names: string[];
  try { names = readdirSync(absDir); } catch { return []; }
  const out: ClaimLite[] = [];
  for (const name of names.sort()) {
    if (name === 'index.md' || !name.endsWith('.md')) continue;
    let fm: Record<string, any>;
    try { fm = matter(readFileSync(join(absDir, name), 'utf8')).data; } catch { continue; }
    const claim = typeof fm.claim === 'string' ? fm.claim.trim() : '';
    if (!claim) continue;
    const assertion = Array.isArray(fm.assertions) ? fm.assertions[0] : undefined;
    out.push({
      text: claim,
      role: fm.role ?? null,
      panel: assertion?.panel ?? fm.panel ?? null,
      slug: fm.slug ?? name.replace(/\.md$/, ''),
    });
  }
  return out;
}

const KEPT_RE = /\.v(\d+)(\.[a-z0-9]+)$/i;

/** Every version of this cell whose bytes are on disk, newest first, with the current output
 *  as the highest version. `latest` is the ledger's current version number for this cell; the
 *  live output is stamped with it so the comparison can label the sides by version.
 *
 *  Returns fewer than two versions when only the current one is addressable — most cells, and
 *  the honest state until a layer has run twice with the copy-keeping in place. */
export function layerVersions(paper: string, layerId: string, produces: string[],
                              latest: number): LayerVersion[] {
  const out: LayerVersion[] = [];

  if (layerId === 'claim-tree') {
    const currentDir = `claims/${paper}`;
    out.push({ v: latest, source: 'current', path: currentDir,
               claims: claimsFromTree(join(ROOT, currentDir)) });
    const runsDir = join(ROOT, 'runs', paper);
    let names: string[] = [];
    try { names = readdirSync(runsDir); } catch { /* no runs dir */ }
    for (const name of names) {
      const m = name.match(/^claim-tree\.v(\d+)$/);
      if (!m) continue;
      const rel = `runs/${paper}/${name}`;
      out.push({ v: Number(m[1]), source: 'kept', path: rel,
                 claims: claimsFromTree(join(ROOT, rel)) });
    }
  } else {
    const rel = produces.find(p => /\.json$/.test(p)) ?? produces[0];
    if (rel) {
      out.push({ v: latest, source: 'current', path: rel, claims: claimsFromOutput(rel) });
      const dir = rel.slice(0, rel.lastIndexOf('/'));
      const stem = basename(rel, extname(rel));               // reconciler.output
      const ext = extname(rel);                               // .json
      let names: string[] = [];
      try { names = readdirSync(join(ROOT, dir)); } catch { /* no dir */ }
      for (const name of names) {
        const m = name.match(KEPT_RE);
        if (!m || !name.startsWith(`${stem}.v`) || m[2] !== ext) continue;
        const krel = `${dir}/${name}`;
        out.push({ v: Number(m[1]), source: 'kept', path: krel,
                   claims: claimsFromOutput(krel) });
      }
    }
  }

  // Newest first, current before a kept copy of the same number, and only versions that
  // actually yielded claims — an empty side is nothing to diff against.
  return out
    .filter(ver => ver.claims.length > 0)
    .sort((a, b) => b.v - a.v || (a.source === 'current' ? -1 : 1));
}

// ── evaluation ──────────────────────────────────────────────────────────────────
//
// The evaluation layer (#85) writes review/evaluation.json: one row per (paper, profile) with
// the metrics and the reference. The claim-tree cell reads that same file, filtered to this
// paper, so the scorecard a reader sees here is the one the /pipeline/evaluation/ page renders
// and nobody has to remember to regenerate a second copy. The matcher's per-re-run alignments
// still live beside the paper (runs/<paper>/evaluation/match.v<N>.pairs.json) and are shown as
// the detail behind the numbers.

export interface MatchPair { committed: string; rerun: string; note?: string }
export interface EvalRow {
  profile: string;
  status: string;
  reference?: string;
  n_cli?: number;
  recovery?: number | null;
  precision?: number | null;
  role?: number | null;
  panel?: number | null;
  edge_recovery?: number | null;
  note?: string;
}
export interface Evaluation {
  /** The rows for this paper from review/evaluation.json, canonical profiles first. */
  rows: EvalRow[];
  /** The matcher's alignments, one entry per scored re-run, newest first. */
  pairs: { v: number; rows: MatchPair[] }[];
  dir: string;
}

/** The evaluation for a paper, or null when nothing has been scored for it. */
export function evaluation(paper: string): Evaluation | null {
  // The scores come from the layer's output file, read once for the whole corpus.
  let rows: EvalRow[] = [];
  try {
    const manifest = JSON.parse(
      readFileSync(join(ROOT, 'review', 'evaluation.json'), 'utf8'));
    rows = (manifest.rows as EvalRow[]).filter((r: any) => r.paper === paper);
  } catch { /* no manifest, or unreadable */ }

  // The alignments still come from disk, as the detail behind the numbers.
  const dir = `runs/${paper}/evaluation`;
  const abs = join(ROOT, dir);
  const pairs: { v: number; rows: MatchPair[] }[] = [];
  let names: string[] = [];
  try { names = readdirSync(abs); } catch { /* none */ }
  for (const name of names) {
    const m = name.match(/^match\.v(\d+)\.pairs\.json$/);
    if (!m) continue;
    try {
      const prs = JSON.parse(readFileSync(join(abs, name), 'utf8'));
      if (Array.isArray(prs)) pairs.push({ v: Number(m[1]), rows: prs });
    } catch { /* skip an unparseable alignment */ }
  }
  pairs.sort((a, b) => b.v - a.v);
  if (rows.length === 0 && pairs.length === 0) return null;
  return { rows, pairs, dir };
}
