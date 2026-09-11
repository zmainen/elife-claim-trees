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
import { nodeColor, outcomeOf, OUTCOME_LABEL, OUTCOME_COLOR } from '../lib/status';
import { useFitOnReveal } from './useFitOnReveal';

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
  [rel: string]: any;
}

// The corpus defines fourteen relation types and this component drew two of them. On Gädeke
// that was 9 edges out of 89, so the graph arrived as a field of unconnected dots and fitView
// shrank it to 20%. With all fourteen the same 33 claims are a single connected component.
//
// Four families rather than fourteen colours: a reader can hold four. The reasoning form of
// each edge is in docs/reference/edges.
const REL_FAMILY: Record<string, 'dependency' | 'support' | 'test' | 'framing'> = {
  'requires': 'dependency', 'derived-from': 'dependency', 'enables-method': 'dependency',
  'supports': 'support', 'validates': 'support', 'confirms': 'support',
  'entails': 'support', 'predicts': 'support',
  'tests': 'test', 'refutes': 'test', 'rules-out': 'test', 'dissociates-with': 'test',
  'interprets': 'framing', 'scopes': 'framing',
};
const RELATIONS = Object.keys(REL_FAMILY);

const FAMILY: Record<string, { stroke: string; dash?: string; label: string }> = {
  dependency: { stroke: 'var(--dag-edge)', label: 'depends on' },
  support:    { stroke: 'var(--dag-edge-support)', dash: '5 3', label: 'supports · validates' },
  test:       { stroke: 'var(--dag-edge-test)', dash: '2 3', label: 'tests · rules out' },
  framing:    { stroke: 'var(--dag-edge-framing)', dash: '1 4', label: 'interprets · scopes' },
};

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
  // `repro` is the layer switch, handed down from the graph. Off — the default — the node
  // is coloured by what the claim does in the paper, and the tree carries no verdict of ours.
  const color = nodeColor(data.status, data.role, Boolean((data as any).repro));
  const isAssessment = data.isAssessment;

  return (
    <>
      <Handle type="target" position={Position.Bottom} style={{ visibility: 'hidden' }} />
      <div
        title={data.claim}
        style={{
          width: NODE_WIDTH,
          border: `1.5px ${isAssessment ? 'dashed' : 'solid'} ${color}`,
          borderRadius: 6,
          background: 'var(--dag-node-bg)',
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
            color: 'var(--dag-node-fg)',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            flex: 1,
            minWidth: 0,
          }}
        >
          {shortLabel(data.slug)}
        </span>
      </div>
      <Handle type="source" position={Position.Top} style={{ visibility: 'hidden' }} />
    </>
  );
}

const nodeTypes: NodeTypes = { claimNode: ClaimNode as any };

const NODE_WIDTH = 150;
const NODE_HEIGHT = 50;

function layoutGraph(claims: Claim[]): { nodes: Node[]; edges: Edge[] } {
  const g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: 'BT', ranksep: 58, nodesep: 16, edgesep: 10, marginx: 14, marginy: 14 });

  const present = new Set(claims.map(c => c.slug));
  for (const c of claims) g.setNode(c.slug, { width: NODE_WIDTH, height: NODE_HEIGHT });

  const edges: Edge[] = [];
  const seen = new Set<string>();

  for (const c of claims) {
    for (const rel of RELATIONS) {
      const targets: string[] = Array.isArray(c[rel]) ? c[rel] : [];
      for (const t of targets) {
        // `scopes: ["*"]` means every empirical claim in the paper. Drawing it would add a
        // fan from one node to thirty and say less than the sentence does.
        if (t === '*' || !present.has(t)) continue;
        const id = `${rel}-${c.slug}-${t}`;
        if (seen.has(id)) continue;
        seen.add(id);
        const family = REL_FAMILY[rel];
        const fam = FAMILY[family];
        // Framing relations are drawn but do not rank the layout. `scopes` alone is 29 of
        // Gädeke's 89 edges and ties one boundary-condition claim to most of the paper; letting
        // it constrain the ranking splayed a single row across 2700px and fitView answered with
        // 30% zoom. The argument's spine is dependency, support and test.
        if (family !== 'framing') g.setEdge(t, c.slug);
        edges.push({
          id,
          source: t,
          target: c.slug,
          type: 'smoothstep',
          data: { rel },
          style: { stroke: fam.stroke, strokeWidth: 1.4, strokeDasharray: fam.dash },
          markerEnd: { type: 'arrowclosed' as any, width: 11, height: 11, color: fam.stroke },
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
  // Off by default: a reader arriving at a claim tree should see the paper's argument, not a
  // scorecard of what we managed to re-run.
  const [showRepro, setShowRepro] = useState(false);
  const shell = useFitOnReveal<HTMLDivElement>(0.15);

  // Repainting the whole graph when the layer is switched, rather than reading the flag from
  // a context in each node — the node count here is small and this keeps the node dumb.
  React.useEffect(() => {
    setNodes(nds => nds.map(n => ({ ...n, data: { ...n.data, repro: showRepro } })));
  }, [showRepro, setNodes]);

  // Build adjacency for highlighting
  const claimBySlug = useMemo(() => {
    const m: Record<string, Claim> = {};
    for (const c of claims) m[c.slug] = c;
    return m;
  }, [claims]);

  const onNodeClick = useCallback((_: any, node: Node) => {
    const claim = claimBySlug[node.id];
    if (!claim) return;
    // The same event the claim cards and summary bullets dispatch. The graph used to carry
    // its own sidebar, which made three panels on one page saying the same thing in three
    // different shapes.
    window.dispatchEvent(new CustomEvent('open-claim', { detail: { slug: claim.slug } }));

    // Follow the edges the reader can see, not just `requires`. Adjacency is built once
    // from the same relation set the layout used.
    const ancestors = new Set<string>();
    const descendants = new Set<string>();
    const up: Record<string, string[]> = {};
    const down: Record<string, string[]> = {};
    for (const c of claims) {
      for (const rel of RELATIONS) {
        const targets: string[] = Array.isArray(c[rel]) ? c[rel] : [];
        for (const t of targets) {
          if (t === '*' || !claimBySlug[t]) continue;
          (up[c.slug] ||= []).push(t);
          (down[t] ||= []).push(c.slug);
        }
      }
    }
    const walk = (from: string, adj: Record<string, string[]>, into: Set<string>) => {
      const stack = [from];
      while (stack.length) {
        for (const n of adj[stack.pop()!] ?? []) {
          if (into.has(n)) continue;
          into.add(n);
          stack.push(n);
        }
      }
    };
    walk(node.id, up, ancestors);
    walk(node.id, down, descendants);

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
    setNodes(nds => nds.map(n => ({ ...n, data: { ...n.data, dimmed: false } })));
    setEdges(eds => eds.map(e => ({ ...e, style: { ...e.style, opacity: 1 } })));
  }, []);

  const base = import.meta.env.BASE_URL.replace(/\/$/, '');

  return (
    <div ref={shell} className="dag-shell h-full w-full">
      <div className="h-full w-full">
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
          <Background color="var(--dag-grid)" gap={20} />
          <Controls />
          <MiniMap
            nodeColor={(n) => nodeColor((n.data as any)?.status ?? 'unknown', (n.data as any)?.role, showRepro)}
            style={{ background: 'var(--dag-minimap)' }}
          />
          <Panel position="top-left">
            <div className="dag-panel rounded-lg p-3 text-xs shadow-sm space-y-1.5">
              {/* The reproduction layer is a switch, and off by default. With it off the graph
                  shows what the paper argues and nothing about what we ran — which is the test
                  that the separation is real rather than described. */}
              <label className="flex items-center gap-1.5 cursor-pointer select-none pb-1.5 mb-1 border-b border-gray-200 dark:border-gray-700">
                <input type="checkbox" checked={showRepro}
                       onChange={(e) => setShowRepro(e.target.checked)} className="accent-slate-600" />
                <span className="font-semibold">Colour by our re-runs</span>
              </label>
              <div className="font-semibold mb-1">
                {showRepro ? 'What we re-ran' : "The paper's argument"}
              </div>
              {(showRepro
                ? ([
                    [OUTCOME_COLOR.match, OUTCOME_LABEL.match],
                    [OUTCOME_COLOR.partial, OUTCOME_LABEL.partial],
                    [OUTCOME_COLOR.differs, OUTCOME_LABEL.differs],
                    [OUTCOME_COLOR.blocked, OUTCOME_LABEL.blocked],
                    [OUTCOME_COLOR['not-attempted'], OUTCOME_LABEL['not-attempted']],
                  ] as [string, string][])
                : ([
                    ['#60a5fa', 'Hypothesis / prediction / synthesis'],
                    ['#a78bfa', 'Cited claim (literature)'],
                    ['#64748b', 'Empirical result / control'],
                    ['#94a3b8', 'Scope / methodological'],
                  ] as [string, string][])
              ).map(([color, label]) => (
                <div key={label} className="flex items-center gap-1.5">
                  <span style={{ width: 10, height: 10, borderRadius: 2, background: color, display: 'inline-block' }} />
                  <span>{label}</span>
                </div>
              ))}
              <div className="border-t border-gray-200 dark:border-gray-700 pt-1.5 mt-1 space-y-1">
                <div className="flex items-center gap-1.5">
                  <span style={{ width: 22, height: 8, border: '1.5px solid currentColor', display: 'inline-block', borderRadius: 1 }} />
                  <span>Result claim</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span style={{ width: 22, height: 8, border: '1.5px dashed currentColor', display: 'inline-block', borderRadius: 1 }} />
                  <span>Assessment claim</span>
                </div>
              </div>
              {/* The edges carry as much of the argument as the nodes do, and had no key. */}
              <div className="border-t border-gray-200 dark:border-gray-700 pt-1.5 mt-1 space-y-1">
                {(Object.keys(FAMILY) as Array<keyof typeof FAMILY>).map(k => (
                  <div key={k} className="flex items-center gap-1.5">
                    <svg width="22" height="8" style={{ display: 'inline-block', flexShrink: 0 }}>
                      <line x1="0" y1="4" x2="22" y2="4"
                            stroke={FAMILY[k].stroke} strokeWidth="1.6"
                            strokeDasharray={FAMILY[k].dash} />
                    </svg>
                    <span>{FAMILY[k].label}</span>
                  </div>
                ))}
              </div>
            </div>
          </Panel>
        </ReactFlow>
      </div>

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
