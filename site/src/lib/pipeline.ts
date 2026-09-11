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
  /** The layer this one passes judgement on. Set only on `judgement` layers. */
  reviews?: string;
  /** How it works, in prose: what it is given, what it returns, and what it gets wrong.
   *  The declaration's `question` says why the layer exists; this says how it answers. A
   *  layer whose prompt or script carries that account already leaves it unset rather than
   *  restating it — see /docs/layers for the narrative the `doc` link points at. */
  how?: string;
  /** A site path to the narrative documentation for this layer, deep-linked to its section. */
  doc?: string;
  /** Lifecycle of the declaration itself (#31). A layer's declaration is a proposal: it says
   *  a step should exist and what it does, and at some point that is accepted. Absent means
   *  unstated — not accepted. Only `proposed` is rendered, so an undeclared status never
   *  claims an approval nobody granted. */
  status?: 'proposed' | 'accepted' | 'superseded';
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

/** The name a reader recognises the paper by: the first author's surname.
 *
 * Taken from the author list rather than the slug. Slugs are ASCII by necessity, so deriving
 * the label from one silently drops diacritics — Gädeke and Kämmer both lost theirs, on the
 * pages that name them most often. Falls back to the slug where no author list exists. */
export const shortOf = (paper: string) => {
  const first = (corpus as any).papers.find((p: any) => p.slug === paper)?.authors?.[0];
  const surname = typeof first === 'string'
    ? first.replace(/\s+et al\.?.*$/i, '').trim().split(/\s+/).filter(w => !/^[A-Z]{1,3}$/.test(w)).pop()
    : null;
  return surname || paper.split('-')[0].replace(/^./, c => c.toUpperCase());
};

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

/** How full a paper is: the jagged edge, as a fraction.
 *
 *  Filled means the cell holds an answer, which is a fact about the corpus. Whether that
 *  answer's inputs can still be checked is a fact about the ledger, and the two were being
 *  conflated: counting only `current` meant a cell whose output exists but predates the
 *  ledger read as not done. Gädeke reported 4 of 21 while holding 18 answers, and the number
 *  moved when runs were re-recorded without a single claim changing.
 *
 *  `absent` is the only state that is genuinely empty. What is checkable is counted
 *  separately, on /pipeline, where the distinction is the subject rather than a side effect. */
export function fill_of(paper: string): { done: number; total: number } {
  const cs = cells(paper);
  return {
    done: cs.filter(c => c.state !== 'absent').length,
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

/** What each declared view is, and where it is rendered.
 *
 *  `views` was a list of words printed on the page and implemented nowhere, which reads as a
 *  feature to anyone who has not tried to use one. Every view named here says which component
 *  draws it; a view with no entry is declared and not built, and the page says so rather than
 *  printing the word and leaving the reader to find out.
 */
export const VIEWS: Record<string, { label: string; where: string }> = {
  document:   { label: 'document', where: 'rendered above, where the layer writes prose' },
  graph:      { label: 'graph', where: 'on the paper page, as the claim graph' },
  comparison: { label: 'comparison', where: 'on the cell page, for the layers that have one' },
  overlap:    { label: 'overlap', where: 'on the induction page, as reader agreement' },
};

export const STATE_LABEL: Record<CellState, string> = {
  current: 'current',
  stale: 'stale',
  absent: 'not run',
  blocked: 'blocked upstream',
  'n/a': 'not applicable',
  open: 'undecided',
  unrecorded: 'unrecorded',
};
