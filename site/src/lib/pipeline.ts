// Resolving a cell.
//
// A cell is (paper, layer, version). Everything the site does with the pipeline is one of
// four verbs on one: render it, fetch it, compare two, or run the layer that fills it. This
// module is the resolver they share, so a page and an endpoint cannot disagree about what a
// cell is or what state it is in.
//
// The data comes from corpus-facts.json, which scripts/corpus_facts.py fills from
// pipeline/layers.yaml and the run ledgers. Nothing here recomputes state — recomputing it in
// the browser's build and in Python would be two answers to one question, which is the whole
// failure mode the pipeline exists to close.

import facts from '../data/corpus-facts.json';
import corpus from '../data/claims.json';

export type CellState =
  | 'current' | 'stale' | 'absent' | 'blocked' | 'n/a' | 'open' | 'unrecorded';

export interface LayerDecl {
  id: string;
  title: string;
  question: string;
  kind: 'step' | 'candidate' | 'judgement' | 'feature' | 'question';
  scope: 'paper' | 'corpus';
  group?: string;
  needs?: string[];
  reads?: string[];
  produces?: string[];
  views?: string[];
  command?: string;
  issue?: number;
  open?: boolean;
  requires_human?: boolean;
  added?: string;
  found?: string;
}

export interface Cell {
  paper: string;
  layer: LayerDecl;
  state: CellState;
  /** Version number from the ledger; absent cells have none. */
  v?: number;
  ran?: string;
  note?: string;
  by?: string;
  /** Inputs whose content changed since the run — why a cell is stale. */
  moved?: string[];
  lost?: string[];
  blockedBy?: string[];
  /** Upstream layers with no ledger entry. Not a fault in this cell; a gap in its account. */
  unrecordedUpstream?: string[];
  /** Artifact paths for this cell, resolved for this paper. */
  produces: string[];
  /** The command that would fill it, with {paper} and {doi} substituted. */
  command?: string;
  /** Every recorded run of this layer for this paper, newest first. */
  versions: Version[];
  /** Approval is an operation on a version, not a layer. `applies` is false when the layer
   *  has run again since — the approval was granted to output that no longer exists. */
  approved?: { v: number; by?: string; when?: string; note?: string; applies: boolean };
  /** Addresses. */
  href: string;
  dataHref: string;
}

export interface Version {
  v: number;
  ran: string;
  note?: string;
  by?: string;
  kind?: string;
  cmd?: string;
  backfilled?: boolean;
}

const P: any = (facts as any).pipeline;

export const available = Boolean(P);
export const layers: LayerDecl[] = P?.layers ?? [];
export const groups: Record<string, { title: string; question: string }> = P?.groups ?? {};
export const byId: Record<string, LayerDecl> =
  Object.fromEntries(layers.map(l => [l.id, l]));

export const paperLayers = layers.filter(l => l.scope !== 'corpus');
export const corpusLayers = layers.filter(l => l.scope === 'corpus');

export const papers: string[] = Object.keys(P?.state ?? {}).sort();
const LEDGER: Record<string, any[]> = P?.ledger ?? {};

/** A paper's version history: every run, newest first. This is the changelog — there is no
 *  second one to keep in step with it. */
export function history(paper: string, layerId?: string): Version[] {
  return (LEDGER[paper] ?? [])
    .filter(e => !layerId || e.layer === layerId)
    .map(e => ({ v: e.v, ran: e.ran, note: e.note, by: e.by, kind: e.kind,
                 cmd: e.cmd, backfilled: e.backfilled, layer: e.layer } as any))
    .sort((a: any, b: any) => (b.ran ?? '').localeCompare(a.ran ?? '') || b.v - a.v);
}

const base = import.meta.env.BASE_URL.replace(/\/$/, '');
const doiOf = (paper: string) =>
  (corpus as any).papers.find((p: any) => p.slug === paper)?.doi ?? '';
export const titleOf = (paper: string) =>
  (corpus as any).papers.find((p: any) => p.slug === paper)?.title ?? paper;

const fill = (s: string, paper: string) =>
  s.replace(/\{paper\}/g, paper).replace(/\{doi\}/g, doiOf(paper));

/** One cell, resolved. Returns null for a layer this paper does not have in scope. */
export function cell(paper: string, layerId: string): Cell | null {
  const layer = byId[layerId];
  const raw = P?.state?.[paper]?.[layerId];
  if (!layer || !raw) return null;
  return {
    paper,
    layer,
    state: raw.state,
    v: raw.v,
    ran: raw.ran,
    note: raw.note,
    by: raw.by,
    moved: raw.moved?.length ? raw.moved : undefined,
    lost: raw.lost?.length ? raw.lost : undefined,
    blockedBy: raw.blocked_by,
    unrecordedUpstream: raw.unrecorded_upstream,
    versions: history(paper, layerId),
    approved: raw.approved,
    produces: (layer.produces ?? []).map(p => fill(p, paper)),
    command: layer.command ? fill(layer.command, paper) : undefined,
    href: `${base}/papers/${paper}/${layerId}/`,
    dataHref: `${base}/data/${paper}/${layerId}.json`,
  };
}

/** Every addressable cell, in dependency order within each paper. */
export function cells(paper: string): Cell[] {
  return paperLayers.map(l => cell(paper, l.id)).filter((c): c is Cell => c !== null);
}

/** The matrix: the query with both paper and layer unbound. */
export function matrix(): Record<string, Cell[]> {
  return Object.fromEntries(papers.map(p => [p, cells(p)]));
}

/** Cells in one state, across the corpus — "what is stale", "what is missing". */
export function inState(...states: CellState[]): Cell[] {
  return papers.flatMap(p => cells(p).filter(c => states.includes(c.state)));
}

/** How full a paper is: the jagged edge, as a fraction. */
export function fill_of(paper: string): { done: number; total: number } {
  const cs = cells(paper);
  return {
    done: cs.filter(c => c.state === 'current' || c.state === 'n/a').length,
    total: cs.length,
  };
}

/** Layers that need this one. The graph runs both ways: a layer page wants to say what it
 *  feeds as well as what it rests on, since that is what a change here would disturb. */
export function dependents(layerId: string): LayerDecl[] {
  return layers.filter(l => (l.needs ?? []).includes(layerId));
}

/** Longest path from a root, which is the column a node belongs in when the graph is drawn.
 *  Longest rather than shortest: a node must sit to the right of everything it needs, and
 *  the shortest path would place it left of a longer dependency. */
export function depth(layerId: string, seen = new Set<string>()): number {
  const l = byId[layerId];
  if (!l || seen.has(layerId)) return 0;
  seen.add(layerId);
  const needs = l.needs ?? [];
  return needs.length ? 1 + Math.max(...needs.map(n => depth(n, new Set(seen)))) : 0;
}

/** The graph as columns, for drawing. */
export function columns(scope?: 'paper' | 'corpus'): LayerDecl[][] {
  const ls = scope ? layers.filter(l => l.scope === scope) : layers;
  const out: LayerDecl[][] = [];
  for (const l of ls) {
    const d = depth(l.id);
    (out[d] ??= []).push(l);
  }
  return out.map(c => c ?? []);
}

/** Every recorded run across the corpus, newest first — the site-wide changelog. */
export function allHistory(): (Version & { paper: string; layer: string })[] {
  return papers
    .flatMap(p => (LEDGER[p] ?? []).map(e => ({ ...e, paper: p })))
    .sort((a, b) => (b.ran ?? '').localeCompare(a.ran ?? ''));
}

/** Fill {{token}} from corpus-facts, flattening one level so `mira.carried` is `mira_carried`.
 *
 *  An unknown token throws rather than rendering as {{...}}: a build that fails is a problem
 *  someone fixes, and a page that quietly shows its own placeholder is one nobody notices.
 *  Same convention, and same reasoning, as docs/method.md. */
const FLAT: Record<string, unknown> = (() => {
  const out: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(facts as Record<string, unknown>)) {
    out[k] = v;
    if (v && typeof v === 'object' && !Array.isArray(v)) {
      for (const [k2, v2] of Object.entries(v as Record<string, unknown>)) {
        if (typeof v2 !== 'object') out[`${k}_${k2}`] = v2;
      }
    }
  }
  return out;
})();

export function resolve(text: string): string {
  return text.replace(/\{\{(\w+)\}\}/g, (_m, key) => {
    if (!(key in FLAT)) {
      throw new Error(
        `pipeline/layers.yaml uses {{${key}}}, which corpus-facts.json does not define. ` +
        `Add it to scripts/corpus_facts.py or fix the token.`);
    }
    return String(FLAT[key]);
  });
}

/** Cells a person has approved, and whose approval still applies to what is there now. */
export function approvedCells(): Cell[] {
  return papers.flatMap(p => cells(p).filter(c => c.approved?.applies));
}

export const STATE_LABEL: Record<CellState, string> = {
  current: 'current',
  stale: 'stale',
  absent: 'not run',
  blocked: 'blocked upstream',
  'n/a': 'not applicable',
  open: 'undecided',
  unrecorded: 'unrecorded',
};
