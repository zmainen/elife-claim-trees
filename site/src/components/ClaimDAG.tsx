import React, { useCallback, useMemo, useState } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  Handle,
  Position,
  type Node,
  type Edge,
  type NodeTypes,
  useNodesState,
  useEdgesState,
  useReactFlow,
  ReactFlowProvider,
  Panel,
} from 'reactflow';
import 'reactflow/dist/style.css';
import dagre from '@dagrejs/dagre';
import { nodeColor, REPLICATION_COLOR, REPLICATION_LABEL, ROLE_COLOR, hasReplication }
  from '../lib/replication';

interface Claim {
  slug: string;
  paper: string;
  claim: string;
  panel: string;
  epistemic: string;
  status: string;
  isAssessment: boolean;
  requires: string[];
  supports: string[];
  notes: string;
}

interface Props {
  claims: Claim[];
  paperSlug: string;
}

// Render the slug as a readable label (full, no truncation).
function shortLabel(slug: string): string {
  return slug.replace(/-/g, ' ');
}

// Custom node renderer
function ClaimNode({ data }: { data: any }) {
  // The node's colour is what the claim *is* — its role. It used to be our re-run result, so
  // a green box meant "we reproduced it" and a blue box meant "this is a prediction", in one
  // undifferentiated colour key. Our result is now a separate marker on the right edge.
  const color = nodeColor(data.status, data.role);
  const isAssessment = data.isAssessment;
  const showRepl = hasReplication(data.status);

  return (
    <>
      <Handle type="target" position={Position.Bottom} style={{ visibility: 'hidden' }} />
      <div
        title={data.claim}
        style={{
          width: 160,
          border: `1.5px ${isAssessment ? 'dashed' : 'solid'} ${color}`,
          borderRadius: 6,
          background: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          gap: 6,
          padding: '8px 10px',
          cursor: 'pointer',
          boxSizing: 'border-box',
          opacity: data.dimmed ? 0.35 : 1,
          transition: 'opacity 0.15s',
        }}
      >
        <span
          style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: color,
            flexShrink: 0,
          }}
        />
        <span
          style={{
            fontSize: 11,
            fontWeight: 500,
            color: '#111827',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            flex: 1,
            minWidth: 0,
          }}
        >
          {shortLabel(data.slug)}
        </span>
        {/* Our re-run, as a marker clipped to the edge — attached to the node, not part of
            it. Monochrome, so it cannot be read as a grade on the claim. */}
        {showRepl && (
          <span
            title={REPLICATION_LABEL[data.status]}
            style={{
              marginLeft: 'auto',
              width: 6,
              height: 6,
              flexShrink: 0,
              borderRadius: 1,
              background: data.status === 'unattempted' || data.status === 'blocked'
                ? 'transparent' : REPLICATION_COLOR[data.status],
              border: `1px solid ${REPLICATION_COLOR[data.status]}`,
            }}
          />
        )}
      </div>
      <Handle type="source" position={Position.Top} style={{ visibility: 'hidden' }} />
    </>
  );
}

const nodeTypes: NodeTypes = { claimNode: ClaimNode as any };

const NODE_WIDTH = 180;
const NODE_HEIGHT = 60;

function layoutGraph(claims: Claim[]): { nodes: Node[]; edges: Edge[] } {
  const g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: 'BT', ranksep: 80, nodesep: 40, edgesep: 20, marginx: 20, marginy: 20 });

  for (const c of claims) {
    g.setNode(c.slug, { width: NODE_WIDTH, height: NODE_HEIGHT });
  }

  const edges: Edge[] = [];

  for (const c of claims) {
    for (const req of c.requires) {
      if (claims.find(x => x.slug === req)) {
        g.setEdge(req, c.slug);
        edges.push({
          id: `req-${req}-${c.slug}`,
          source: req,
          target: c.slug,
          type: 'smoothstep',
          style: { stroke: '#d1d5db', strokeWidth: 1.5 },
          markerEnd: { type: 'arrowclosed' as any, width: 12, height: 12, color: '#d1d5db' },
        });
      }
    }
    for (const sup of c.supports) {
      if (claims.find(x => x.slug === sup)) {
        edges.push({
          id: `sup-${c.slug}-${sup}`,
          source: c.slug,
          target: sup,
          type: 'smoothstep',
          style: { stroke: '#86efac', strokeWidth: 1.5, strokeDasharray: '5 3' },
          markerEnd: { type: 'arrowclosed' as any, width: 12, height: 12, color: '#86efac' },
        });
      }
    }
  }

  dagre.layout(g);

  const nodes: Node[] = claims.map(c => {
    const pos = g.node(c.slug);
    return {
      id: c.slug,
      type: 'claimNode',
      position: { x: pos.x - NODE_WIDTH / 2, y: pos.y - NODE_HEIGHT / 2 },
      data: { ...c, dimmed: false },
    };
  });

  return { nodes, edges };
}

function DAGInner({ claims, paperSlug }: Props) {
  const { nodes: initialNodes, edges: initialEdges } = useMemo(() => layoutGraph(claims), [claims]);
  const [nodes, setNodes] = useNodesState(initialNodes);
  const [edges, setEdges] = useEdgesState(initialEdges);
  const [selected, setSelected] = useState<Claim | null>(null);
  const { fitView } = useReactFlow();

  // Build adjacency for highlighting
  const claimBySlug = useMemo(() => {
    const m: Record<string, Claim> = {};
    for (const c of claims) m[c.slug] = c;
    return m;
  }, [claims]);

  const onNodeClick = useCallback((_: any, node: Node) => {
    const claim = claimBySlug[node.id];
    if (!claim) return;
    setSelected(claim);

    const ancestors = new Set<string>();
    const descendants = new Set<string>();

    function walkUp(slug: string) {
      const c = claimBySlug[slug];
      if (!c) return;
      for (const r of c.requires) {
        if (!ancestors.has(r)) { ancestors.add(r); walkUp(r); }
      }
    }
    function walkDown(slug: string) {
      for (const c of claims) {
        if (c.requires.includes(slug) && !descendants.has(c.slug)) {
          descendants.add(c.slug);
          walkDown(c.slug);
        }
      }
    }
    walkUp(node.id);
    walkDown(node.id);

    const active = new Set([node.id, ...ancestors, ...descendants]);

    setNodes(nds => nds.map(n => ({
      ...n,
      data: { ...n.data, dimmed: !active.has(n.id) },
    })));

    setEdges(eds => eds.map(e => ({
      ...e,
      style: {
        ...e.style,
        opacity: (active.has(e.source) && active.has(e.target)) ? 1 : 0.15,
      },
    })));
  }, [claimBySlug, claims]);

  const onPaneClick = useCallback(() => {
    setSelected(null);
    setNodes(nds => nds.map(n => ({ ...n, data: { ...n.data, dimmed: false } })));
    setEdges(eds => eds.map(e => ({ ...e, style: { ...e.style, opacity: 1 } })));
  }, []);

  const base = import.meta.env.BASE_URL.replace(/\/$/, '');

  return (
    <div className="flex h-full">
      {/* DAG canvas */}
      <div className="flex-1 h-full">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          nodeTypes={nodeTypes}
          onNodeClick={onNodeClick}
          onPaneClick={onPaneClick}
          nodesDraggable={false}
          nodesConnectable={false}
          elementsSelectable={true}
          fitView
          fitViewOptions={{ padding: 0.15 }}
          minZoom={0.2}
          maxZoom={3}
          proOptions={{ hideAttribution: true }}
        >
          <Background color="#f3f4f6" gap={20} />
          <Controls />
          <MiniMap
            nodeColor={(n) => nodeColor((n.data as any)?.status ?? 'unknown', (n.data as any)?.role)}
            style={{ background: '#f9fafb' }}
          />
          <Panel position="top-left">
            <div className="bg-white border border-gray-200 rounded-lg p-3 text-xs shadow-sm space-y-1.5">
              <div className="font-semibold text-gray-700 mb-1">What each claim is</div>
              {[
                [ROLE_COLOR.empirical, 'Empirical result'],
                [ROLE_COLOR.control, 'Control'],
                [ROLE_COLOR.hypothesis, 'Hypothesis / prediction / synthesis'],
                [ROLE_COLOR['literature-context'], 'Cited claim (literature)'],
                [ROLE_COLOR.scope, 'Scope / method'],
              ].map(([color, label]) => (
                <div key={label} className="flex items-center gap-1.5">
                  <span style={{ width: 10, height: 10, borderRadius: 2, background: color, display: 'inline-block' }} />
                  <span className="text-gray-600">{label}</span>
                </div>
              ))}
              <div className="border-t border-gray-100 pt-1.5 mt-1 space-y-1">
                <div className="font-semibold text-gray-700 mb-1">What our re-run found</div>
                {[
                  ['verified', 'matches'],
                  ['partial', 'partly matches'],
                  ['mismatch', 'differs'],
                  ['unattempted', 'not re-run / blocked'],
                ].map(([st, label]) => (
                  <div key={st} className="flex items-center gap-1.5">
                    <span style={{
                      width: 8, height: 8, borderRadius: 1, display: 'inline-block',
                      background: st === 'unattempted' ? 'transparent' : REPLICATION_COLOR[st],
                      border: `1px solid ${REPLICATION_COLOR[st]}`,
                    }} />
                    <span className="text-gray-600">{label}</span>
                  </div>
                ))}
              </div>
              <div className="border-t border-gray-100 pt-1.5 mt-1 space-y-1">
                <div className="flex items-center gap-1.5">
                  <span style={{ width: 22, height: 8, border: '1.5px solid #6b7280', display: 'inline-block', borderRadius: 1 }} />
                  <span className="text-gray-600">Result claim</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span style={{ width: 22, height: 8, border: '1.5px dashed #6b7280', display: 'inline-block', borderRadius: 1 }} />
                  <span className="text-gray-600">Assessment claim</span>
                </div>
              </div>
            </div>
          </Panel>
        </ReactFlow>
      </div>

      {/* Sidebar */}
      {selected && (
        <div className="w-80 border-l border-gray-200 bg-white overflow-y-auto flex-shrink-0">
          <div className="p-4 space-y-4">
            <div className="flex items-start justify-between gap-2">
              <h3 className="font-semibold text-sm text-gray-900 leading-snug">{selected.slug}</h3>
              <button
                onClick={onPaneClick}
                className="text-gray-400 hover:text-gray-600 text-xs flex-shrink-0"
              >✕</button>
            </div>

            <p className="text-sm text-gray-700 leading-relaxed">{selected.claim}</p>

            <div className="flex flex-wrap gap-1.5">
              <span
                className="inline-block px-2 py-0.5 rounded text-xs font-medium"
                style={{ background: nodeColor(selected.status, selected.role) + '22', color: '#111', border: `1px solid ${nodeColor(selected.status, selected.role)}` }}
              >{selected.status === 'unknown' ? selected.role : selected.status}</span>
              <span className="inline-block px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-700">
                {selected.epistemic}
              </span>
              {selected.isAssessment && (
                <span className="inline-block px-2 py-0.5 rounded text-xs font-medium bg-purple-50 text-purple-700 border border-purple-200">
                  assessment
                </span>
              )}
            </div>

            {selected.panel && (
              <div className="text-xs text-gray-500">Panel: {selected.panel}</div>
            )}

            {selected.requires.length > 0 && (
              <div>
                <div className="text-xs font-semibold text-gray-500 mb-1">Requires</div>
                <div className="flex flex-col gap-1">
                  {selected.requires.map(r => (
                    <a
                      key={r}
                      href={`${base}/papers/${paperSlug}/${r}/`}
                      className="text-xs text-blue-600 hover:underline break-words"
                    >{r}</a>
                  ))}
                </div>
              </div>
            )}

            {selected.supports.length > 0 && (
              <div>
                <div className="text-xs font-semibold text-gray-500 mb-1">Supports</div>
                <div className="flex flex-col gap-1">
                  {selected.supports.map(s => (
                    <a
                      key={s}
                      href={`${base}/papers/${paperSlug}/${s}/`}
                      className="text-xs text-green-700 hover:underline break-words"
                    >{s}</a>
                  ))}
                </div>
              </div>
            )}

            {selected.notes && (
              <div>
                <div className="text-xs font-semibold text-gray-500 mb-1">Notes</div>
                <p className="text-xs text-gray-600 leading-relaxed whitespace-pre-wrap">{selected.notes}</p>
              </div>
            )}

            <a
              href={`${base}/papers/${paperSlug}/${selected.slug}/`}
              className="block text-xs text-center py-1.5 px-3 border border-gray-200 rounded hover:bg-gray-50 text-gray-600 no-underline"
            >
              View full claim →
            </a>
          </div>
        </div>
      )}
    </div>
  );
}

export default function ClaimDAG(props: Props) {
  return (
    <ReactFlowProvider>
      <DAGInner {...props} />
    </ReactFlowProvider>
  );
}
