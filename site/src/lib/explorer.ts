// The payload the pipeline explorer renders.
//
// The map and the drawer are one island sharing one selection, so the data they need is
// computed here — at build, from the same resolver the pages and the /data/ endpoint use —
// and handed over whole. Two reasons it is not fetched:
//
//   * the drawer opens on click, and a fetch per node would put a spinner between the reader
//     and a fact the build already knew;
//   * `cell()` reads corpus-facts.json, which must not reach the browser bundle.
//
// /data/<paper>/<layer>.json remains the public address of a cell. This is the same content,
// pre-joined for one page.

import {
  layers, byId, groups, papers, cells, cell, dependents, depth, resolve, shortOf, titleOf,
  paperLayers, STATE_LABEL, type CellState, type LayerDecl,
} from './pipeline';
import { artifacts, isDirectory, type Artifact } from './artifacts';

export const KIND_NOTE: Record<string, string> = {
  step: 'Mechanical: re-runnable from its declared inputs.',
  candidate: 'One of several parallel outputs, kept rather than collapsed — agreement between them is the informative case.',
  judgement: 'A decision, stored rather than recomputed, because recomputing it destroys the record of who decided.',
  feature: 'A capability that revises existing artifacts. It runs once, and then it is part of the schema.',
  question: 'A decision about meaning, and then the propagation of it through everything downstream.',
};

export interface CellView {
  paper: string;
  short: string;
  title: string;
  state: CellState;
  stateLabel: string;
  v: number | null;
  ran: string | null;
  note: string | null;
  href: string;
  dataHref: string;
  artifacts: Artifact[];
  /** Declared outputs that name a directory rather than a file. */
  directories: string[];
  command: string | null;
}

export interface LayerView {
  id: string;
  title: string;
  question: string;
  kind: LayerDecl['kind'];
  kindNote: string;
  scope: LayerDecl['scope'];
  group: string | null;
  groupTitle: string | null;
  groupQuestion: string | null;
  status: string | null;
  open: boolean;
  requiresHuman: boolean;
  issue: number | null;
  added: string | null;
  found: string | null;
  needs: string[];
  feeds: string[];
  /** Longest path from a root. The column view is this; the graph view uses it as rank. */
  depth: number;
  href: string;
  /** Corpus altitude: how many papers have been through it. */
  fill: { done: number; total: number } | null;
  /** One entry per paper, in corpus mode; one entry (this paper) in paper mode. */
  cells: CellView[];
}

export interface ExplorerData {
  mode: 'corpus' | 'paper';
  paper: { slug: string; short: string; title: string } | null;
  layers: LayerView[];
  stateLabels: Record<string, string>;
}

const cellView = (paper: string, layer: LayerDecl, base: string): CellView | null => {
  const c = cell(paper, layer.id);
  if (!c) return null;
  const produced = c.produces ?? [];
  return {
    paper,
    short: shortOf(paper),
    title: titleOf(paper),
    state: c.state,
    stateLabel: STATE_LABEL[c.state],
    v: c.v ?? null,
    ran: c.ran?.slice(0, 10) ?? null,
    note: c.note ?? null,
    href: c.href,
    dataHref: c.dataHref,
    artifacts: artifacts(produced.filter(p => !isDirectory(p)), base),
    directories: produced.filter(isDirectory),
    command: c.command ?? null,
  };
};

const layerView = (l: LayerDecl, base: string, only: string | null): LayerView => {
  const scoped = l.scope === 'corpus' ? [] : (only ? [only] : papers);
  const views = scoped.map(p => cellView(p, l, base)).filter((c): c is CellView => c !== null);
  const done = views.filter(c => c.state === 'current' || c.state === 'stale').length;
  return {
    id: l.id,
    title: l.title,
    question: l.question,
    kind: l.kind,
    kindNote: KIND_NOTE[l.kind] ?? '',
    scope: l.scope,
    group: l.group ?? null,
    groupTitle: l.group ? groups[l.group]?.title ?? null : null,
    groupQuestion: l.group ? groups[l.group]?.question ?? null : null,
    status: (l as any).status ?? null,
    open: Boolean(l.open),
    requiresHuman: Boolean(l.requires_human),
    issue: l.issue ?? null,
    added: l.added ?? null,
    // Resolved here: {{token}} substitution reads corpus-facts, which stays out of the bundle.
    found: l.found ? resolve(l.found) : null,
    needs: l.needs ?? [],
    feeds: dependents(l.id).map(d => d.id),
    depth: depth(l.id),
    href: `${base}/pipeline/${l.id}/`,
    fill: l.scope === 'corpus' ? null : { done, total: views.length },
    cells: views,
  };
};

/** Every layer, at corpus altitude. */
export function corpusExplorer(base: string): ExplorerData {
  return {
    mode: 'corpus',
    paper: null,
    layers: layers.map(l => layerView(l, base, null)),
    stateLabels: STATE_LABEL,
  };
}

/** One paper's instance of every layer it has in scope. Corpus-scope layers are carried too:
 *  they are what the paper's cells rest on, and a map that hid them would show roots with no
 *  cause. They simply have no cell of their own. */
export function paperExplorer(paper: string, base: string): ExplorerData {
  const inScope = new Set(paperLayers.map(l => l.id));
  return {
    mode: 'paper',
    paper: { slug: paper, short: shortOf(paper), title: titleOf(paper) },
    layers: layers
      .filter(l => inScope.has(l.id) || l.scope === 'corpus')
      .map(l => layerView(l, base, paper)),
    stateLabels: STATE_LABEL,
  };
}
