import React, { useCallback, useEffect, useMemo, useState } from 'react';
import LayerBands from './LayerBands';
import LayerDrawer from './LayerDrawer';
import type { ExplorerData } from '../lib/explorer';

// One island: the view and the drawer share a selection, which is the whole point of the
// drawer. Selection is mirrored into the URL fragment (#layer=mira-export) so a link can
// open on a particular layer — the thing a walkthrough needs and a page-per-layer site got
// for free.
//
// There used to be two views and a toggle between them: columns, which overflowed to 1680px
// and left two fifths of the map off-screen, and a pan-and-zoom graph, which fitted by
// zooming out past the point of being able to read a node. Both spent the width on depth.
// LayerBands spends the height on it instead, which is the axis a page has to spare, and one
// view that works is worth more than a choice between two that do not — the toggle, the
// remembered preference and the canvas all went with it.

type Props = { data: ExplorerData; base: string };

const STATES: Array<[string, string]> = [
  ['current', 'current'], ['stale', 'stale'], ['blocked', 'blocked upstream'],
  ['absent', 'not run'], ['open', 'undecided'],
];

export default function PipelineExplorer({ data, base }: Props) {
  const [selected, setSelected] = useState<string | null>(null);
  const [lit, setLit] = useState<string | null>(null);

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

  const select = useCallback((id: string | null) => {
    setSelected(id);
    const url = new URL(window.location.href);
    url.hash = id ? `layer=${id}` : '';
    history.replaceState(null, '', url.toString());
  }, []);

  const layer = selected ? byId.get(selected) ?? null : null;

  return (
    <div>
      <LayerBands data={data} selected={selected} lit={lit}
                  onSelect={select} onHover={setLit} />

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

      </div>

      <LayerDrawer data={data} layer={layer} onSelect={select} base={base} />
    </div>
  );
}
