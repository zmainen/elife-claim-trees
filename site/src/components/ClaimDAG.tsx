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
  useReactFlow,
  ReactFlowProvider,
  Panel,
} from 'reactflow';
import 'reactflow/dist/style.css';
import dagre from '@dagrejs/dagre';
import { nodeColor, outcomeOf, OUTCOME_LABEL, OUTCOME_COLOR } from '../lib/status';
import { readableInCoreMira, MIRA_PARENT, MIRA_INVERSE_OF } from '../lib/mira';
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
// shrank it to 20%. With all fourteen the same claims are a single connected component.
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

// In the MIRA view an edge keeps only what a core-MIRA consumer can read off it: support or
// opposition. Both colours are the ones this graph already spends on those meanings, so the
// view changes what is said, not the vocabulary it is said in.
const MIRA_STROKE: Record<string, string> = {
  'mira:supports': 'var(--dag-edge-support)',
  'mira:opposes': 'var(--dag-edge-test)',
};

// ── Role bands ───────────────────────────────────────────────────────────────
// dagre ranks a node by its distance along the edges, which is a fact about the drawing and
// not about the paper: a control that happens to sit two edges from a hypothesis was drawn
// level with the predictions, and the picture had no shape a reader could name. The bands
// below are the paper's own division of labour, and the deductive spine — hypothesis, the
// prediction it entails, the result that tests the prediction — reads straight down them.
//
// The ten roles are corpus-facts.roles_used; every one has a home here, and a role that
// appears later without one lands in Findings rather than vanishing.
const BANDS: { id: string; label: string; roles: string[] }[] = [
  { id: 'hypothesis',     label: 'Hypotheses',           roles: ['hypothesis'] },
  { id: 'prediction',     label: 'Predictions',          roles: ['prediction'] },
  { id: 'empirical',      label: 'Findings',             roles: ['empirical'] },
  { id: 'interpretation', label: 'Interpretation',       roles: ['interpretation', 'synthesis', 'assessment'] },
  { id: 'control',        label: 'Controls and methods', roles: ['control', 'methodological'] },
  { id: 'context',        label: 'Scope and prior work', roles: ['scope', 'literature-context'] },
];
const BAND_OF_ROLE: Record<string, string> = {};
for (const b of BANDS) for (const r of b.roles) BAND_OF_ROLE[r] = b.id;

const NODE_WIDTH = 150;
const NODE_HEIGHT = 50;
const COL_GAP = 22;
const ROW_GAP = 16;
const BAND_GAP = 52;
const LABEL_GUTTER = 148;
// A band wider than this wraps onto a second row. Gädeke's Findings band is 23 claims: on one
// row that is 4000px against six bands of 600px, and fitView answers a 7:1 canvas with a zoom
// at which no label is legible. Wrapped, the bands stay bands and the page stays readable.
const MAX_PER_ROW = 8;

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

/** A band's name, in the gutter to the left of its rows. It sits outside the span the claims
 *  occupy so no edge ever crosses it, and carries a rule down the band's height so the band
 *  has a visible extent without a fill competing with the nodes. */
function BandNode({ data }: { data: any }) {
  return (
    <div
      style={{
        width: LABEL_GUTTER - 22,
        height: data.height,
        borderRight: '1px solid var(--dag-panel-border)',
        paddingRight: 10,
        boxSizing: 'border-box',
        display: 'flex',
        justifyContent: 'flex-end',
        pointerEvents: 'none',
      }}
    >
      <span
        style={{
          fontSize: 11,
          fontWeight: 600,
          letterSpacing: '0.07em',
          textTransform: 'uppercase',
          color: 'var(--dag-panel-fg)',
          opacity: 0.55,
          whiteSpace: 'nowrap',
          lineHeight: `${NODE_HEIGHT}px`,
        }}
      >
        {data.label}
      </span>
    </div>
  );
}

const nodeTypes: NodeTypes = { claimNode: ClaimNode as any, bandNode: BandNode as any };

interface Built {
  nodes: Node[];
  edges: Edge[];
}

function layoutGraph(claims: Claim[]): Built {
  const present = new Set(claims.map(c => c.slug));

  // ── the edges the reader can see ──
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
        edges.push({
          id,
          source: t,
          target: c.slug,
          type: 'smoothstep',
          data: { rel },
        });
      }
    }
  }

  // ── horizontal order, seeded by dagre ──
  // The bands fix y, so dagre is asked for one thing only: an ordering across the page that
  // does not cross more edges than it must. Its ranks are discarded.
  const g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: 'BT', ranksep: 58, nodesep: 16, edgesep: 10, marginx: 14, marginy: 14 });
  for (const c of claims) g.setNode(c.slug, { width: NODE_WIDTH, height: NODE_HEIGHT });
  for (const e of edges) {
    // Framing relations are drawn but do not order the layout. `scopes` alone is a large
    // share of Gädeke's edges and ties one boundary-condition claim to most of the paper;
    // letting it pull the ordering splays a band across the page for no gain.
    if (REL_FAMILY[(e.data as any).rel] !== 'framing') g.setEdge(e.source, e.target);
  }
  dagre.layout(g);
  const seedX: Record<string, number> = {};
  for (const c of claims) seedX[c.slug] = g.node(c.slug)?.x ?? 0;

  // ── assign to bands, drop the empty ones ──
  const members: Record<string, Claim[]> = {};
  for (const c of claims) {
    const band = BAND_OF_ROLE[(c as any).role] ?? 'empirical';
    (members[band] ||= []).push(c);
  }
  const live = BANDS.filter(b => (members[b.id] ?? []).length > 0);

  // Two barycentre sweeps over the dagre seed. A node wants to sit above or below the things
  // it is joined to, and the seed's ordering was computed for ranks these bands do not use.
  const neighbours: Record<string, string[]> = {};
  for (const e of edges) {
    if (REL_FAMILY[(e.data as any).rel] === 'framing') continue;
    (neighbours[e.source] ||= []).push(e.target);
    (neighbours[e.target] ||= []).push(e.source);
  }
  const order: Record<string, number> = { ...seedX };
  for (let sweep = 0; sweep < 2; sweep++) {
    const next: Record<string, number> = {};
    for (const c of claims) {
      const ns = neighbours[c.slug] ?? [];
      next[c.slug] = ns.length
        ? ns.reduce((s, n) => s + (order[n] ?? 0), 0) / ns.length
        : order[c.slug];
    }
    // Ties are broken by the previous order, so a band of unconnected claims keeps a stable
    // arrangement rather than reshuffling on every render.
    for (const c of claims) order[c.slug] = (next[c.slug] + order[c.slug]) / 2;
  }

  // ── rows within each band ──
  const laid = live.map(band => {
    const list = [...(members[band.id] ?? [])].sort(
      (a, b) => (order[a.slug] - order[b.slug]) || a.slug.localeCompare(b.slug));
    const rowCount = Math.ceil(list.length / MAX_PER_ROW);
    // Spread evenly rather than filling the first row and leaving a stub on the second.
    const even = Math.ceil(list.length / rowCount);
    const rows: Claim[][] = [];
    for (let i = 0; i < list.length; i += even) rows.push(list.slice(i, i + even));
    return { band, rows };
  });

  // ── place, every band centred on one axis ──
  // Centring each band inside its own width would step the narrow bands off the wide ones and
  // the spine would zigzag. The page has one centre line and all six bands sit on it.
  const rowWidth = (n: number) => n * NODE_WIDTH + (n - 1) * COL_GAP;
  const canvasWidth = Math.max(...laid.flatMap(l => l.rows.map(r => rowWidth(r.length))));

  const nodes: Node[] = [];
  let y = 0;
  for (const { band, rows } of laid) {
    const bandHeight = rows.length * NODE_HEIGHT + (rows.length - 1) * ROW_GAP;

    nodes.push({
      id: `band-${band.id}`,
      type: 'bandNode',
      position: { x: -LABEL_GUTTER, y },
      data: { label: band.label, height: bandHeight },
      draggable: false,
      selectable: false,
      connectable: false,
      focusable: false,
      zIndex: -1,
    });

    rows.forEach((row, ri) => {
      const x0 = (canvasWidth - rowWidth(row.length)) / 2;
      row.forEach((c, ci) => {
        nodes.push({
          id: c.slug,
          type: 'claimNode',
          position: { x: x0 + ci * (NODE_WIDTH + COL_GAP), y: y + ri * (NODE_HEIGHT + ROW_GAP) },
          data: { ...c, dimmed: false },
        });
      });
    });

    y += bandHeight + BAND_GAP;
  }

  return { nodes, edges };
}

function DAGInner({ claims, paperSlug }: Props) {
  const { nodes: baseNodes, edges: baseEdges } = useMemo(() => layoutGraph(claims), [claims]);
  // Off by default: a reader arriving at a claim tree should see the paper's argument, not a
  // scorecard of what we managed to re-run.
  const [showRepro, setShowRepro] = useState(false);
  // Which interchange format the graph is read through. `corpus` is this project's own
  // vocabulary; `mira` is what survives into the schema eLife reads.
  const [mode, setMode] = useState<'corpus' | 'mira'>('corpus');
  const [active, setActive] = useState<Set<string> | null>(null);
  // The graph lives in a <details> inside a column the rail resizes, so its box keeps moving
  // for a while after it appears. Fit until it stops, then leave the reader alone.
  const shell = useFitOnReveal<HTMLDivElement>(0.15, { refitOnResize: true });

  const claimBySlug = useMemo(() => {
    const m: Record<string, Claim> = {};
    for (const c of claims) m[c.slug] = c;
    return m;
  }, [claims]);

  // What the MIRA view costs, counted off the edges actually drawn rather than off a table —
  // so the number in the banner is the number of lines that left the picture.
  const loss = useMemo(() => {
    const dropped = baseEdges.filter(e => !readableInCoreMira((e.data as any).rel));
    const byType: Record<string, number> = {};
    for (const e of dropped) {
      const rel = (e.data as any).rel as string;
      byType[rel] = (byType[rel] ?? 0) + 1;
    }
    const types = Object.keys(byType).sort((a, b) => byType[b] - byType[a]);
    return { count: dropped.length, total: baseEdges.length, types, byType };
  }, [baseEdges]);

  const edges = useMemo(() => baseEdges.flatMap(e => {
    const rel = (e.data as any).rel as string;
    const dim = active && !(active.has(e.source) && active.has(e.target));
    let stroke: string;
    let dash: string | undefined;
    if (mode === 'mira') {
      const parent = MIRA_PARENT[rel];
      if (!parent) return [];
      stroke = MIRA_STROKE[parent];
      dash = undefined;
    } else {
      const fam = FAMILY[REL_FAMILY[rel]];
      stroke = fam.stroke;
      dash = fam.dash;
    }
    return [{
      ...e,
      style: { stroke, strokeWidth: 1.4, strokeDasharray: dash, opacity: dim ? 0.15 : 1 },
      markerEnd: { type: 'arrowclosed' as any, width: 11, height: 11, color: stroke },
    }];
  }), [baseEdges, mode, active]);

  const nodes = useMemo(() => baseNodes.map(n => (
    n.type === 'bandNode'
      ? n
      : { ...n, data: { ...n.data, repro: showRepro, dimmed: Boolean(active && !active.has(n.id)) } }
  )), [baseNodes, showRepro, active]);

  const onNodeClick = useCallback((_: any, node: Node) => {
    const claim = claimBySlug[node.id];
    if (!claim) return;
    // The same event the claim cards and summary bullets dispatch. The graph used to carry
    // its own sidebar, which made three panels on one page saying the same thing in three
    // different shapes — and is why the verification record went into the rail's card rather
    // than into a second panel here.
    window.dispatchEvent(new CustomEvent('open-claim', { detail: { slug: claim.slug } }));

    // Follow the edges the reader can see, not just `requires`. In the MIRA view that means
    // the edges MIRA can still read: the neighbourhood shrinks with the picture, which is
    // the thing the view is there to show.
    const visible = baseEdges.filter(e =>
      mode === 'corpus' || readableInCoreMira((e.data as any).rel));
    const up: Record<string, string[]> = {};
    const down: Record<string, string[]> = {};
    for (const e of visible) {
      (up[e.target] ||= []).push(e.source);
      (down[e.source] ||= []).push(e.target);
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
    const reached = new Set<string>([node.id]);
    walk(node.id, up, reached);
    walk(node.id, down, reached);
    setActive(reached);
  }, [claimBySlug, baseEdges, mode]);

  const onPaneClick = useCallback(() => setActive(null), []);

  // Only a real gesture stops the auto-fit. fitView moves the viewport itself and fires
  // onMoveStart with no event, which otherwise locks the graph at the first fit it was given.
  const onMoveStart = useCallback((e: any) => { if (e) shell.settle(); }, [shell]);

  return (
    <div ref={shell} className="dag-shell flex h-full w-full flex-col">
      {/* The format switch. The site reports elsewhere, in a table, that MIRA carries almost
          every relation in the corpus; that is true of the triples and says nothing about
          whether they can be read. One click is the argument. */}
      <div className="dag-formatbar">
        <div className="dag-formatrow">
          <div className="dag-seg" role="group" aria-label="Interchange format">
            {([['corpus', 'This corpus'], ['mira', 'MIRA']] as const).map(([id, label]) => (
              <button key={id} type="button" aria-pressed={mode === id}
                      onClick={() => setMode(id)}>{label}</button>
            ))}
          </div>
          <p className="dag-formatnote">
            {mode === 'corpus'
              ? <>All {loss.total} relations between these claims, in the fourteen types the corpus defines.</>
              : <>The same graph as a reader of core MIRA sees it: <strong>{loss.count} of {loss.total} relations
                  gone</strong>, and the rest flattened to support or opposition.</>}
          </p>
        </div>
        {mode === 'mira' && loss.count > 0 && (
          <p className="dag-formatloss">
            Hidden: {loss.types.map(t => `${t} (${loss.byType[t]})`).join(', ')}.
            {' '}These types declare no core MIRA predicate, so they are exported as bare
            {' '}<code>haak:reldef</code> terms with no parent: the triples are in the file, but
            {' '}nothing tells a consumer that knows only <code>mira:supports</code> and
            {' '}<code>mira:opposes</code> what they assert.
            {loss.types.some(t => MIRA_INVERSE_OF[t]) && (
              <> <code>derived-from</code> reaches MIRA only as its inverse, <code>entails</code>,
                {' '}which declares no parent either.</>
            )}
          </p>
        )}
      </div>

      <div className="min-h-0 flex-1">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          nodeTypes={nodeTypes}
          onNodeClick={onNodeClick}
          onPaneClick={onPaneClick}
          onMoveStart={onMoveStart}
          nodesDraggable={false}
          nodesConnectable={false}
          elementsSelectable={true}
          fitView
          fitViewOptions={{ padding: 0.15 }}
          minZoom={0.1}
          maxZoom={3}
          proOptions={{ hideAttribution: true }}
        >
          <Background color="var(--dag-grid)" gap={20} />
          <Controls />
          <MiniMap
            nodeColor={(n) => (n.type === 'bandNode'
              ? 'transparent'
              : nodeColor((n.data as any)?.status ?? 'unknown', (n.data as any)?.role, showRepro))}
            style={{ background: 'var(--dag-minimap)' }}
          />
          <Panel position="top-left">
            {/* Folded by default. The key is a fixed block in the one corner the band labels
                have to pass through, and at the zoom a seventy-claim graph fits at it covered
                the thing the bands were added to show. The bar above the canvas now says what
                the view is; this is the detail behind it. */}
            <details className="dag-key">
              <summary className="dag-panel">Key</summary>
            <div className="dag-panel dag-keybody rounded-lg p-3 text-xs shadow-sm space-y-1.5">
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
                {(mode === 'corpus'
                  ? (Object.keys(FAMILY) as Array<keyof typeof FAMILY>).map(k => [FAMILY[k].stroke, FAMILY[k].dash, FAMILY[k].label] as const)
                  : ([
                      [MIRA_STROKE['mira:supports'], undefined, 'mira:supports'],
                      [MIRA_STROKE['mira:opposes'], undefined, 'mira:opposes'],
                    ] as const)
                ).map(([stroke, dash, label]) => (
                  <div key={label} className="flex items-center gap-1.5">
                    <svg width="22" height="8" style={{ display: 'inline-block', flexShrink: 0 }}>
                      <line x1="0" y1="4" x2="22" y2="4"
                            stroke={stroke} strokeWidth="1.6" strokeDasharray={dash} />
                    </svg>
                    <span>{label}</span>
                  </div>
                ))}
              </div>
            </div>
            </details>
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
