import React, { useCallback, useMemo } from 'react';
import ReactFlow, {
  Background, Controls, Handle, Position, MarkerType,
  ReactFlowProvider, type Edge, type Node, type NodeTypes,
} from 'reactflow';
import 'reactflow/dist/style.css';
import dagre from '@dagrejs/dagre';
import { useFitOnReveal } from './useFitOnReveal';
import type { ExplorerData, LayerView } from '../lib/explorer';

// The pipeline, drawn as the graph it is.
//
// The page this replaces laid the layers out in columns headed "depth 0..7" and drew no
// edges at all — so the one thing the section promised, how a layer depends on its inputs,
// was the one thing a reader could not see. Depth is still the horizontal axis, because
// reading left to right is how the pipeline runs; the difference is that the dependencies
// are now lines you can follow.
//
// Hovering a node lights its whole ancestry and everything downstream of it. That is not
// decoration: staleness propagates along exactly those edges, so "what does a change here
// disturb" is a question the picture should answer without being read.

const NODE_W = 162;
const NODE_H = 58;

type Props = {
  data: ExplorerData;
  selected: string | null;
  lit: string | null;
  onSelect: (id: string | null) => void;
  onHover: (id: string | null) => void;
};

function LayerNode({ data }: { data: any }) {
  const l: LayerView = data.layer;
  const dim = data.dimmed;
  return (
    <>
      <Handle type="target" position={Position.Left} style={{ visibility: 'hidden' }} />
      <div
        className="map-node rounded-md px-2 py-1.5 cursor-pointer transition-opacity"
        data-scope={l.scope}
        data-group={l.group ?? ''}
        data-lit={data.lit ? 'on' : 'off'}
        data-selected={data.selected ? 'on' : 'off'}
        style={{ width: NODE_W, height: NODE_H, opacity: dim ? 0.28 : 1, boxSizing: 'border-box' }}
        title={l.question}
      >
        <div className="font-mono text-[12px] leading-tight truncate">{l.id}</div>
        <div className="map-node-muted text-[10px] leading-tight truncate">
          {l.kind}
          {l.status === 'proposed' ? ' · provisional' : ''}
          {l.open ? ' · undecided' : ''}
          {l.requiresHuman ? ' · needs a person' : ''}
        </div>
        {data.badge}
      </div>
      <Handle type="source" position={Position.Right} style={{ visibility: 'hidden' }} />
    </>
  );
}

const nodeTypes: NodeTypes = { layer: LayerNode };

/** Everything reachable from `id` along `edges`, in the given direction. */
function reach(id: string, adj: Map<string, string[]>): Set<string> {
  const seen = new Set<string>();
  const queue = [id];
  while (queue.length) {
    const cur = queue.pop()!;
    for (const next of adj.get(cur) ?? []) {
      if (seen.has(next)) continue;
      seen.add(next);
      queue.push(next);
    }
  }
  return seen;
}

function Flow({ data, selected, lit, onSelect, onHover }: Props) {
  const focus = lit ?? selected;
  // On a paper page this map lives in a tab panel, which is display:none until chosen.
  const shell = useFitOnReveal<HTMLDivElement>(0.06);

  const { nodes, edges } = useMemo(() => {
    const ls = data.layers;
    const byId = new Map(ls.map(l => [l.id, l]));
    const present = (id: string) => byId.has(id);

    // Both directions, so one hover can light the full ancestry and the full fan-out.
    const up = new Map<string, string[]>();
    const down = new Map<string, string[]>();
    const pairs: Array<[string, string]> = [];
    for (const l of ls) {
      for (const n of l.needs) {
        if (!present(n)) continue;
        pairs.push([n, l.id]);
        up.set(l.id, [...(up.get(l.id) ?? []), n]);
        down.set(n, [...(down.get(n) ?? []), l.id]);
      }
    }

    const family = focus
      ? new Set<string>([focus, ...reach(focus, up), ...reach(focus, down)])
      : null;

    const g = new dagre.graphlib.Graph();
    g.setDefaultEdgeLabel(() => ({}));
    g.setGraph({ rankdir: 'LR', nodesep: 13, ranksep: 54, marginx: 10, marginy: 10 });
    for (const l of ls) g.setNode(l.id, { width: NODE_W, height: NODE_H });
    for (const [s, t] of pairs) g.setEdge(s, t);
    dagre.layout(g);

    const nodes: Node[] = ls.map(l => {
      const p = g.node(l.id);
      return {
        id: l.id,
        type: 'layer',
        position: { x: p.x - NODE_W / 2, y: p.y - NODE_H / 2 },
        data: {
          layer: l,
          dimmed: family ? !family.has(l.id) : false,
          lit: focus === l.id,
          selected: selected === l.id,
          badge: data.mode === 'paper'
            ? <StateChip state={l.scope === 'corpus' ? null : l.cells[0]?.state ?? null}
                         label={l.scope === 'corpus' ? 'corpus-wide' : l.cells[0]?.stateLabel ?? ''}
                         v={l.cells[0]?.v ?? null} />
            : <FillBar fill={l.fill} />,
        },
        draggable: false,
        connectable: false,
      };
    });

    const edges: Edge[] = pairs.map(([s, t]) => {
      const on = family ? family.has(s) && family.has(t) : false;
      return {
        id: `${s}->${t}`,
        source: s,
        target: t,
        type: 'smoothstep',
        animated: false,
        style: {
          stroke: on ? 'var(--map-edge-lit)' : 'var(--map-edge)',
          strokeWidth: on ? 1.9 : 1.1,
          opacity: family && !on ? 0.18 : 1,
        },
        markerEnd: {
          type: MarkerType.ArrowClosed, width: 13, height: 13,
          color: on ? 'var(--map-edge-lit)' : 'var(--map-edge)',
        },
      };
    });

    return { nodes, edges };
  }, [data, focus, selected]);

  const onNodeClick = useCallback(
    (_: React.MouseEvent, n: Node) => onSelect(n.id === selected ? null : n.id),
    [onSelect, selected]);

  return (
    <div ref={shell} className="h-full w-full">
    <ReactFlow
      nodes={nodes}
      edges={edges}
      nodeTypes={nodeTypes}
      onNodeClick={onNodeClick}
      onNodeMouseEnter={(_, n) => onHover(n.id)}
      onNodeMouseLeave={() => onHover(null)}
      onPaneClick={() => onSelect(null)}
      fitView
      fitViewOptions={{ padding: 0.06 }}
      minZoom={0.3}
      maxZoom={1.8}
      proOptions={{ hideAttribution: true }}
      nodesDraggable={false}
      nodesConnectable={false}
      elementsSelectable
      /* The map sits inside a scrolling page. React Flow's default is to swallow the wheel
         and zoom, which turns scrolling past the graph into a trap — the reader's page stops
         moving and the picture silently rescales. The wheel is the page's; zoom is on the
         controls, on pinch, and on ctrl+wheel. */
      preventScrolling={false}
      zoomOnScroll={false}
      panOnScroll={false}
      zoomOnDoubleClick={false}
      panOnDrag
    >
      <Background gap={18} size={1} color="var(--map-grid)" />
      <Controls showInteractive={false} position="bottom-right" />
    </ReactFlow>
    </div>
  );
}

function FillBar({ fill }: { fill: LayerView['fill'] }) {
  if (!fill) return <div className="map-node-muted text-[9px] mt-1">every paper</div>;
  const pct = fill.total ? Math.round((fill.done / fill.total) * 100) : 0;
  return (
    <div className="flex items-center gap-1.5 mt-1">
      <div className="flex-1 h-1 rounded-full overflow-hidden" style={{ background: 'var(--st-absent)' }}>
        <div style={{ width: `${pct}%`, height: '100%', background: 'var(--st-current)' }} />
      </div>
      <span className="map-node-muted text-[9px] tabular-nums">{fill.done}/{fill.total}</span>
    </div>
  );
}

function StateChip({ state, label, v }: { state: string | null; label: string; v: number | null }) {
  return (
    <div className="flex items-center gap-1.5 mt-1">
      <i className="inline-block w-2 h-2 rounded-sm flex-shrink-0"
         style={{ background: state ? `var(--st-${state === 'n/a' ? 'na' : state})` : 'var(--st-na)' }} />
      <span className="map-node-muted text-[9px] truncate">
        {label}{v ? ` · v${v}` : ''}
      </span>
    </div>
  );
}

export default function LayerMap(props: Props) {
  return (
    <ReactFlowProvider>
      <Flow {...props} />
    </ReactFlowProvider>
  );
}
