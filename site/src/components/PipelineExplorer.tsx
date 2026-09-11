import React, { useCallback, useEffect, useMemo, useState } from 'react';
import LayerMap from './LayerMap';
import LayerColumns from './LayerColumns';
import LayerDrawer from './LayerDrawer';
import type { ExplorerData } from '../lib/explorer';

// One island: the view and the drawer share a selection, which is the whole point of the
// drawer. Selection is mirrored into the URL fragment (#layer=mira-export) so a link can
// open on a particular layer — the thing a walkthrough needs and a page-per-layer site got
// for free.
//
// Two views of one set. Columns are faster to scan and never overlap; the graph is the only
// one that shows what feeds what. Neither is a strict improvement on the other, so the
// reader picks, and the pick is remembered — a walkthrough that starts in columns should not
// be thrown back into the graph on the next page.

type Props = { data: ExplorerData; base: string; height?: number };

type View = 'graph' | 'columns';
const VIEW_KEY = 'pipeline-view';

const STATES: Array<[string, string]> = [
  ['current', 'current'], ['stale', 'stale'], ['blocked', 'blocked upstream'],
  ['absent', 'not run'], ['open', 'undecided'],
];

export default function PipelineExplorer({ data, base, height = 460 }: Props) {
  const [selected, setSelected] = useState<string | null>(null);
  const [lit, setLit] = useState<string | null>(null);
  // Columns first. It is the view that needs no explaining, and a reader who wants the
  // dependencies drawn can ask for them.
  const [view, setView] = useState<View>('columns');

  const byId = useMemo(() => new Map(data.layers.map(l => [l.id, l])), [data]);

  // Read the fragment on arrival, and again whenever it changes. The second half is not
  // belt-and-braces: a link to #layer=coverage from somewhere else on this same page is a
  // same-document navigation, so nothing remounts and mount-time reading alone would leave
  // the drawer shut on exactly the links most likely to be followed.
  useEffect(() => {
    const fromHash = () => {
      const m = /(?:^|[#&])layer=([a-z0-9-]+)/.exec(window.location.hash);
      setSelected(m && byId.has(m[1]) ? m[1] : null);
    };
    fromHash();
    window.addEventListener('hashchange', fromHash);
    return () => window.removeEventListener('hashchange', fromHash);
  }, [byId]);

  useEffect(() => {
    try {
      const v = localStorage.getItem(VIEW_KEY);
      if (v === 'graph' || v === 'columns') setView(v);
    } catch { /* private browsing, or storage refused: the default stands */ }
  }, []);

  const pickView = useCallback((v: View) => {
    setView(v);
    try { localStorage.setItem(VIEW_KEY, v); } catch { /* not worth failing over */ }
  }, []);

  const select = useCallback((id: string | null) => {
    setSelected(id);
    const url = new URL(window.location.href);
    url.hash = id ? `layer=${id}` : '';
    history.replaceState(null, '', url.toString());
  }, []);

  const layer = selected ? byId.get(selected) ?? null : null;

  return (
    <div>
      <div className="flex items-center justify-end mb-2">
        <div role="group" aria-label="Layer view"
             className="inline-flex rounded border border-gray-200 dark:border-gray-700 overflow-hidden">
          {(['columns', 'graph'] as View[]).map(v => (
            <button key={v} onClick={() => pickView(v)} aria-pressed={view === v}
                    className={`text-[11px] font-mono px-2.5 py-1 cursor-pointer border-0 ${
                      view === v
                        ? 'bg-gray-900 text-white dark:bg-gray-100 dark:text-gray-900'
                        : 'bg-transparent text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'}`}>
              {v === 'columns' ? 'columns' : 'graph'}
            </button>
          ))}
        </div>
      </div>

      {view === 'graph' ? (
        <div className="map-shell border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"
             style={{ height }}>
          <LayerMap data={data} selected={selected} lit={lit}
                    onSelect={select} onHover={setLit} />
        </div>
      ) : (
        <LayerColumns data={data} selected={selected} onSelect={select} />
      )}

      <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 mt-2.5 text-[11px] text-gray-500 dark:text-gray-400">
        {data.mode === 'paper'
          ? STATES.map(([s, label]) => (
              <span key={s} className="flex items-center gap-1.5">
                <i className="inline-block w-2.5 h-2.5 rounded-sm"
                   style={{ background: `var(--st-${s})` }} />{label}
              </span>
            ))
          : <span className="flex items-center gap-1.5">
              <span className="inline-block w-6 h-1 rounded-full" style={{ background: 'var(--st-current)' }} />
              how many papers have been through it
            </span>}
        <span className="flex items-center gap-1.5">
          <i className="inline-block w-2.5 h-2.5 rounded-sm border border-dashed"
             style={{ borderColor: 'var(--map-corpus-border)' }} />corpus-scope
        </span>
        <span className="ml-auto">
          Click a layer for detail{view === 'graph' ? ' · hover to light its dependencies' : ''}
        </span>
      </div>

      <LayerDrawer data={data} layer={layer} onSelect={select} base={base} />
    </div>
  );
}
