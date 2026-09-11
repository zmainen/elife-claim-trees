// The standards section: one source format, four targets.
//
// A claim tree is written in one format — ours — and can be expressed in several others.
// This declares which, in the order a reader should meet them, so the tab strip and the
// index cannot disagree about what the section contains.
//
// Every format page answers the same six questions in the same order. That regularity is
// what makes this a reference rather than five essays, and it is the same discipline the
// layer pages follow:
//
//   what it is · what it requires · how a claim tree maps onto it ·
//   does it validate · what it cannot carry · what we would ask its authors
//
// Where a format has no answer to one of them, the page says so. Discourse Graphs has no
// mapping document and CiTO's is forty-four lines; padding those to match MIRA would make
// the section look even and be less true.

export interface Standard {
  id: string;
  name: string;
  full?: string;
  /** One line, for the tab strip and the index card. */
  blurb: string;
  /** Where the prose behind this page lives, if anywhere. */
  source?: string;
  /** How thoroughly this one is worked out. Shown, not hidden. */
  depth: 'reference' | 'proposal' | 'sketch';
}

export const STANDARDS: Standard[] = [
  {
    id: 'ours',
    name: 'Ours',
    full: 'The claim format',
    blurb: 'What a claim is, and what may be said about one. The format the other four map from.',
    source: 'docs/claim-format.md',
    depth: 'reference',
  },
  {
    id: 'mira',
    name: 'MIRA',
    full: 'Modular Interoperable Research Attribution',
    blurb: 'The discourse-graph schema eLife’s article platform reads.',
    source: 'docs/schema-mapping/mira-guide.md',
    depth: 'reference',
  },
  {
    id: 'oxa',
    name: 'OXA',
    full: 'Open Exchange Architecture',
    blurb: 'The document format behind Curvenote, Stencila and eLife. Our Claim node is a proposal to it.',
    source: 'docs/schema-mapping/oxa-claim-schema.md',
    depth: 'proposal',
  },
  {
    id: 'cito',
    name: 'CiTO',
    full: 'Citation Typing Ontology',
    blurb: 'Forty typed relations between documents. Six of ours map directly; eight need extensions.',
    source: 'docs/schema-mapping/cito-mapping.md',
    depth: 'sketch',
  },
  {
    id: 'dg',
    name: 'Discourse Graphs',
    blurb: 'Questions, Claims, Evidence and Sources. We emit it; the mapping lives only in code.',
    depth: 'sketch',
  },
];

export const byId: Record<string, Standard> =
  Object.fromEntries(STANDARDS.map(s => [s.id, s]));

export const DEPTH_NOTE: Record<Standard['depth'], string> = {
  reference: 'Worked out: the schema read, the mapping generated from the exporter, exports validated.',
  proposal: 'A proposal we are making, rather than a schema we are reading.',
  sketch: 'Thin. The mapping exists in code and has not been written up or validated.',
};

/** The six rubrics, in order. A page may answer a rubric with "nothing yet", but it may not
 *  reorder them or leave one out — that is what makes the tabs comparable. */
export const RUBRICS = [
  'What it is',
  'What it requires',
  'How a claim tree maps onto it',
  'Does it validate',
  'What it cannot carry',
  'What we would ask its authors',
] as const;
