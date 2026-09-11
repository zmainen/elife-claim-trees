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

import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import type { LayerDecl } from './pipeline';

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
