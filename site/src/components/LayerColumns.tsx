import React from 'react';
import type { ExplorerData, LayerView } from '../lib/explorer';

// The pipeline as columns — the reading this page had before the graph, kept.
//
// It answers a different question, and answers it faster: *what are the layers, and roughly
// in what order*. Nothing overlaps, nothing needs panning, and the whole set is on screen at
// a glance. What it cannot show is which layer feeds which, which is why the graph exists
// beside it rather than instead of it.
//
// Both views are the same selection and the same drawer, so switching does not lose your place.

type Props = {
  data: ExplorerData;
  selected: string | null;
  onSelect: (id: string | null) => void;
};

function Card({ l, mode, selected, onSelect }: {
  l: LayerView; mode: 'corpus' | 'paper'; selected: boolean; onSelect: () => void;
}) {
  const c = l.cells[0];
  const pct = l.fill && l.fill.total ? Math.round((l.fill.done / l.fill.total) * 100) : 0;
  return (
    <button
      onClick={onSelect}
      title={l.question}
      data-scope={l.scope}
      data-selected={selected ? 'on' : 'off'}
      className="map-node block w-full text-left rounded px-2.5 py-2 cursor-pointer"
    >
      <span className="block font-mono text-[11.5px] leading-tight truncate">{l.id}</span>
      <span className="map-node-muted block text-[10px] leading-tight truncate">
        {l.kind}{l.group ? ` · ${l.group}` : ''}
        {l.status === 'proposed' ? ' · provisional' : ''}
        {l.open ? ' · undecided' : ''}
        {l.requiresHuman ? ' · needs a person' : ''}
      </span>
      {l.scope === 'corpus' ? (
        <span className="map-node-muted block text-[9.5px] mt-1">every paper</span>
      ) : mode === 'paper' ? (
        <span className="flex items-center gap-1.5 mt-1">
          <i className="inline-block w-2 h-2 rounded-sm flex-shrink-0"
             style={{ background: `var(--st-${c?.state === 'n/a' ? 'na' : c?.state ?? 'absent'})` }} />
          <span className="map-node-muted text-[9.5px] truncate">
            {c?.stateLabel}{c?.v ? ` · v${c.v}` : ''}
          </span>
        </span>
      ) : (
        <span className="flex items-center gap-1.5 mt-1">
          <span className="flex-1 h-1 rounded-full overflow-hidden" style={{ background: 'var(--st-absent)' }}>
            <span className="block h-full" style={{ width: `${pct}%`, background: 'var(--st-current)' }} />
          </span>
          <span className="map-node-muted text-[9.5px] tabular-nums">{l.fill?.done}/{l.fill?.total}</span>
        </span>
      )}
    </button>
  );
}

export default function LayerColumns({ data, selected, onSelect }: Props) {
  const maxDepth = Math.max(0, ...data.layers.map(l => l.depth));
  const cols = Array.from({ length: maxDepth + 1 }, (_, d) =>
    data.layers.filter(l => l.depth === d));

  return (
    <div className="map-shell overflow-x-auto border border-gray-200 dark:border-gray-700 rounded-lg">
      <div className="flex gap-4 p-5 min-w-max">
        {cols.map((col, i) => (
          <div key={i} className="flex flex-col gap-2.5 w-[168px]">
            <div className="text-[10px] font-mono uppercase tracking-wider text-gray-400 dark:text-gray-500 pb-1.5 border-b border-gray-200 dark:border-gray-700">
              depth {i}
            </div>
            {col.map(l => (
              <Card key={l.id} l={l} mode={data.mode}
                    selected={selected === l.id}
                    onSelect={() => onSelect(selected === l.id ? null : l.id)} />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
