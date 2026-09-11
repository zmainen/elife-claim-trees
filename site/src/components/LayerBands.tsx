import React from 'react';
import type { ExplorerData, LayerView } from '../lib/explorer';

// The layer graph as bands down the page.
//
// It replaced two views that both spent the screen's scarce axis on the pipeline's long one.
// Columns put nine depths across the width and overflowed to 1680px in a 974px shell, so two
// fifths of the map sat off-screen behind a drag. The graph fitted by zooming out, which
// bought the shape at the cost of being able to read any node in it, and then wanted pan and
// zoom to give that back.
//
// Depth is an order, and a page has an unbounded axis for orders: down. Bands turn the long
// axis into scroll-the-page, which is free, and spend the width on the layers within a depth
// — which have no order among themselves and can wrap. Nothing is off-screen, nothing needs
// fitting, and a phone and a desktop differ only in how many chips sit on a line.
//
// The edges went with the canvas. In a DAG drawn by depth every arrow points from a lower
// band to a higher one, so position carries direction and the lines were twenty-eight nodes'
// worth of crossings restating the layout. Hovering a layer marks what feeds it and
// everything downstream instead — the question the arrows only let you trace by eye.

type Props = {
  data: ExplorerData;
  selected: string | null;
  lit: string | null;
  onSelect: (id: string | null) => void;
  onHover: (id: string | null) => void;
};

type Mark = 'self' | 'needs' | 'downstream' | null;

function Chip({ l, mode, mark, dim, selected, onSelect, onHover }: {
  l: LayerView; mode: 'corpus' | 'paper'; mark: Mark; dim: boolean; selected: boolean;
  onSelect: () => void; onHover: (on: boolean) => void;
}) {
  const c = l.cells[0];
  const pct = l.fill && l.fill.total ? Math.round((l.fill.done / l.fill.total) * 100) : 0;
  return (
    <button
      onClick={onSelect}
      onMouseEnter={() => onHover(true)}
      onMouseLeave={() => onHover(false)}
      onFocus={() => onHover(true)}
      onBlur={() => onHover(false)}
      title={l.question}
      data-scope={l.scope}
      data-group={l.group ?? undefined}
      data-mark={mark ?? undefined}
      data-dim={dim ? 'on' : undefined}
      data-selected={selected ? 'on' : 'off'}
      aria-pressed={selected}
      className="chip map-node block w-full min-w-0 text-left rounded px-2.5 py-2 cursor-pointer"
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

export default function LayerBands({ data, selected, lit, onSelect, onHover }: Props) {
  const maxDepth = Math.max(0, ...data.layers.map(l => l.depth));
  const bands = Array.from({ length: maxDepth + 1 }, (_, d) => data.layers.filter(l => l.depth === d));

  // Hover marks, not selection: a selected layer opens the drawer, and the drawer covers the
  // page it would be marking. Hover and keyboard focus are the pointer already asking the
  // question — nothing to open, nothing to dismiss, and the marks are gone when you move off.
  const focus = lit ? data.layers.find(l => l.id === lit) ?? null : null;
  const needs = new Set(focus?.needs ?? []);
  const down = new Set(focus?.downstream ?? []);

  const markOf = (id: string): Mark =>
    !focus ? null
      : id === focus.id ? 'self'
      : needs.has(id) ? 'needs'
      : down.has(id) ? 'downstream'
      : null;

  return (
    <div className="bands">
      {bands.map((layers, d) => (
        <div key={d} className="flex gap-4 py-3 border-t border-gray-100 dark:border-gray-800">
          <div className="w-14 flex-shrink-0 pt-1">
            <span className="block text-[10px] font-mono uppercase tracking-wider text-gray-400 dark:text-gray-500">
              depth {d}
            </span>
            <span className="block text-[10px] font-mono text-gray-300 dark:text-gray-600 tabular-nums">
              {layers.length}
            </span>
          </div>
          {/* Auto-fill grid rather than wrapped flex: chips line up into columns instead of
              ragging, and the track count follows the width without a breakpoint anywhere. */}
          <div className="band-chips grid gap-2 min-w-0 flex-1">
            {layers.map(l => (
              <Chip key={l.id} l={l} mode={data.mode}
                    mark={markOf(l.id)}
                    dim={Boolean(focus) && markOf(l.id) === null}
                    selected={selected === l.id}
                    onSelect={() => onSelect(selected === l.id ? null : l.id)}
                    onHover={(on: boolean) => onHover(on ? l.id : null)} />
            ))}
          </div>
        </div>
      ))}

      <p className="text-[11px] text-gray-500 dark:text-gray-400 mt-3 mb-0">
        {focus
          ? <>
              <span className="font-mono text-gray-700 dark:text-gray-300">{focus.id}</span>
              {focus.needs.length ? <> rests on <span className="font-mono">{focus.needs.join(', ')}</span></> : <> is a root</>}
              {focus.downstream.length
                ? <> · {focus.downstream.length} layer{focus.downstream.length === 1 ? '' : 's'} fall out of date if it changes</>
                : <> · nothing downstream of it</>}
            </>
          : <>Every layer rests on a band above it. Point at one to see what feeds it and what it would unsettle; click for the rest.</>}
      </p>
    </div>
  );
}
