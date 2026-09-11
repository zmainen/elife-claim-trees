import React, { useEffect, useRef } from 'react';
import type { ExplorerData, LayerView, CellView } from '../lib/explorer';
import type { Artifact } from '../lib/artifacts';

// A layer, without leaving the map.
//
// Every node on this page used to be a link to its own page, which meant reading three
// layers cost three page loads and three trips back — and the matrix, the thing you were
// reading them against, was gone the moment you clicked. The drawer keeps the graph on
// screen and puts the layer beside it. `rests on` and `feeds` move the drawer rather than
// navigating, so following a dependency chain is now a chain of clicks in one place.
//
// The full page still exists at /pipeline/<id>, is still what a deep link resolves to, and
// is still where a layer with more to say than the declaration holds says it.

type Props = {
  data: ExplorerData;
  layer: LayerView | null;
  onSelect: (id: string | null) => void;
  base: string;
};

const Label = ({ children }: { children: React.ReactNode }) => (
  <h3 className="text-[10px] font-mono uppercase tracking-wider text-gray-400 dark:text-gray-500 m-0 mb-2">{children}</h3>
);

function Dot({ state }: { state: string | null }) {
  const key = state === 'n/a' ? 'na' : state;
  return <i className="inline-block w-2.5 h-2.5 rounded-sm flex-shrink-0"
            style={{ background: state ? `var(--st-${key})` : 'var(--st-na)' }} />;
}

const EXT_LABEL: Record<string, string> = {
  jsonld: 'JSON-LD', json: 'JSON', markdown: 'Markdown', image: 'image', code: 'source', other: 'file',
};

function ArtifactRow({ a }: { a: Artifact }) {
  return (
    <li className="py-1">
      {/* The filename gets its own line. These names are long and hyphenated, and sharing a
          flex row with the description broke them mid-word. */}
      <a href={a.href}
         {...(a.downloadable ? { download: '' } : { target: '_blank', rel: 'noopener' })}
         className="block font-mono text-[11.5px] text-amber-700 dark:text-amber-400 no-underline hover:underline leading-snug"
         style={{ overflowWrap: 'anywhere' }}>
        {a.name}
      </a>
      <div className="text-[10.5px] text-gray-500 dark:text-gray-400 leading-snug">
        {EXT_LABEL[a.kind]}
        {a.note ? ` — ${a.note}` : ''}
        {a.downloadable ? '' : ' · in the repository'}
      </div>
    </li>
  );
}

function CellBlock({ c, showPaper }: { c: CellView; showPaper: boolean }) {
  const has = c.artifacts.length > 0 || c.directories.length > 0;
  return (
    <div className="py-2.5 border-b border-gray-100 dark:border-gray-800 last:border-0">
      <div className="flex items-center gap-2 mb-0.5">
        <Dot state={c.state} />
        {showPaper
          ? <a href={c.href} className="text-[13px] text-gray-800 dark:text-gray-200 no-underline hover:text-amber-700 dark:hover:text-amber-400 font-medium">{c.short}</a>
          : <span className="text-[13px] text-gray-800 dark:text-gray-200 font-medium">{c.stateLabel}</span>}
        <span className="text-[11px] text-gray-500 dark:text-gray-400 font-mono tabular-nums">
          {showPaper ? c.stateLabel : ''}{c.v ? ` · v${c.v}` : ''}{c.ran ? ` · ${c.ran}` : ''}
        </span>
      </div>
      {c.note && <p className="text-[11.5px] text-gray-500 dark:text-gray-400 m-0 mb-1 leading-snug">{c.note}</p>}
      {has && (
        <ul className="list-none p-0 m-0 mt-1">
          {c.artifacts.map(a => <ArtifactRow key={a.path} a={a} />)}
          {c.directories.map(d => (
            <li key={d} className="py-1 text-[11.5px] text-gray-500 dark:text-gray-400">
              <code className="text-[11px]">{d}</code> — a directory of files, not a download
            </li>
          ))}
        </ul>
      )}
      {!has && c.command && (
        <p className="text-[11.5px] text-gray-500 dark:text-gray-400 m-0 leading-snug">
          Declares no file of its own.
        </p>
      )}
      <a href={c.dataHref} className="text-[10.5px] font-mono text-gray-400 dark:text-gray-500 no-underline hover:text-amber-700 dark:hover:text-amber-400">
        cell as JSON ↗
      </a>
    </div>
  );
}

export default function LayerDrawer({ data, layer, onSelect, base }: Props) {
  const panel = useRef<HTMLDivElement>(null);
  const open = layer !== null;

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onSelect(null); };
    window.addEventListener('keydown', onKey);
    panel.current?.focus();
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onSelect]);

  if (!layer) return null;
  const l = layer;
  const byId = new Map(data.layers.map(x => [x.id, x]));
  const chip = (id: string) => {
    const t = byId.get(id);
    return (
      <button key={id} onClick={() => onSelect(id)}
              className="font-mono text-[11.5px] px-1.5 py-0.5 rounded border border-gray-200 dark:border-gray-700 text-amber-700 dark:text-amber-400 bg-transparent cursor-pointer hover:border-amber-600 dark:hover:border-amber-500">
        {id}{t ? '' : ' ↗'}
      </button>
    );
  };

  const isCorpus = l.scope === 'corpus';
  const ran = l.cells.filter(c => c.state === 'current' || c.state === 'stale');

  return (
    <>
      <div onClick={() => onSelect(null)}
           className="fixed inset-0 bg-black/25 dark:bg-black/50 z-40" aria-hidden="true" />
      <div ref={panel} tabIndex={-1} role="dialog" aria-label={`${l.title} — layer`}
           className="fixed right-0 top-0 h-full w-full sm:w-[440px] z-50 overflow-y-auto bg-white dark:bg-[#15191e] border-l border-gray-200 dark:border-gray-700 shadow-2xl outline-none">
        <div className="p-5">

          <div className="flex items-start justify-between gap-3 mb-3">
            <div>
              <div className="font-mono text-[12px] text-gray-500 dark:text-gray-400">{l.id}</div>
              <h2 className="text-[19px] font-semibold text-gray-900 dark:text-gray-100 m-0 leading-tight">{l.title}</h2>
            </div>
            <button onClick={() => onSelect(null)} aria-label="Close"
                    className="text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 bg-transparent border-0 cursor-pointer text-xl leading-none p-1">×</button>
          </div>

          <div className="flex flex-wrap gap-1.5 mb-3 text-[10px] font-mono uppercase tracking-wider">
            <span className="text-gray-500 dark:text-gray-400">{l.kind} · {l.scope}</span>
            {l.status === 'proposed' && (
              <span className="px-1.5 rounded border border-dashed border-amber-500 text-amber-700 dark:text-amber-400">provisional</span>
            )}
            {l.open && <span className="text-blue-700 dark:text-blue-400">undecided</span>}
            {l.requiresHuman && <span className="text-amber-700 dark:text-amber-400">needs a person</span>}
          </div>

          <p className="text-[15px] italic text-gray-700 dark:text-gray-300 m-0 mb-2 leading-snug">{l.question}</p>
          <p className="text-[12.5px] text-gray-600 dark:text-gray-400 m-0 mb-4 leading-relaxed">{l.kindNote}</p>

          {l.groupTitle && (
            <p className="text-[12px] text-gray-500 dark:text-gray-400 m-0 mb-4 leading-snug">
              Part of <strong className="text-gray-700 dark:text-gray-300">{l.groupTitle}</strong> — {l.groupQuestion}
            </p>
          )}

          {l.found && (
            <section className="mb-5 border-l-2 border-emerald-500 dark:border-emerald-600 pl-3">
              <Label>What it found{l.added ? ` · added ${l.added}` : ''}</Label>
              <p className="text-[12.5px] text-gray-700 dark:text-gray-300 m-0 leading-relaxed"
                 dangerouslySetInnerHTML={{ __html: l.found.replace(/`([^`]+)`/g, '<code class="text-[11.5px]">$1</code>') }} />
            </section>
          )}

          <section className="mb-5">
            <Label>Rests on</Label>
            {l.needs.length === 0
              ? <p className="text-[12.5px] text-gray-500 dark:text-gray-400 m-0">Nothing — this is a root.</p>
              : <div className="flex flex-wrap gap-1.5">{l.needs.map(chip)}</div>}
          </section>

          <section className="mb-5">
            <Label>Feeds{l.feeds.length > 0 ? ' — a change here disturbs these' : ''}</Label>
            {l.feeds.length === 0
              ? <p className="text-[12.5px] text-gray-500 dark:text-gray-400 m-0">Nothing — this is a leaf.</p>
              : <div className="flex flex-wrap gap-1.5">{l.feeds.map(chip)}</div>}
          </section>

          {isCorpus ? (
            <section className="mb-5">
              <Label>Scope</Label>
              <p className="text-[12.5px] text-gray-600 dark:text-gray-400 m-0 leading-relaxed">
                A decision about the corpus, not a run against one paper. It has no cell of its
                own; when it changes, every cell that rests on it goes stale.
              </p>
              {l.issue && (
                <p className="text-[12.5px] m-0 mt-2">
                  <a href={`https://github.com/zmainen/elife-claim-trees/issues/${l.issue}`}
                     target="_blank" rel="noopener"
                     className="text-amber-700 dark:text-amber-400 no-underline hover:underline">Issue #{l.issue}</a>
                  <span className="text-gray-500 dark:text-gray-400"> — the decision is taken there.</span>
                </p>
              )}
            </section>
          ) : (
            <section className="mb-5">
              <Label>
                {data.mode === 'paper'
                  ? 'This paper'
                  : `Across the corpus — ${ran.length} of ${l.cells.length} papers`}
              </Label>
              {l.cells.length === 0
                ? <p className="text-[12.5px] text-gray-500 dark:text-gray-400 m-0">No cell for this layer.</p>
                : <div>{l.cells.map(c => (
                    <CellBlock key={c.paper} c={c} showPaper={data.mode === 'corpus'} />
                  ))}</div>}
            </section>
          )}

          {l.cells[0]?.command && (
            <section className="mb-5">
              <Label>How it runs</Label>
              <pre className="text-[10.5px] font-mono bg-gray-50 dark:bg-gray-900/60 border border-gray-200 dark:border-gray-700 rounded p-2.5 m-0 overflow-x-auto whitespace-pre-wrap break-all text-gray-700 dark:text-gray-300">{l.cells[0].command}</pre>
            </section>
          )}

          <footer className="pt-3 border-t border-gray-100 dark:border-gray-800">
            <a href={l.href} className="text-[12.5px] text-amber-700 dark:text-amber-400 no-underline hover:underline">
              Full page for this layer →
            </a>
          </footer>
        </div>
      </div>
    </>
  );
}
