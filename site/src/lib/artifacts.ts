// What a layer produced, as something a reader can open.
//
// `produces` in layers.yaml is a repo-relative path with {paper} unsubstituted. It says what
// a layer *would* write, which is not the same as a file that exists: most declared paths in
// this corpus name output of a layer that has never run for that paper. So a path is resolved
// against what build-data.js measured rather than assumed — artifacts.json records, for every
// declared path, whether the site serves it, whether the repository holds it, or whether it
// was never produced at all. An honest "not produced" is worth more than a link that 404s.
//
// Three ways to open one, and a reader wants different ones at different times:
//   view      the site's own rendering of it — a claim list, a graph, the cell that made it
//   raw       the bytes, downloaded or copied
//   source    the file in the repository, when the site does not serve it

import index from '../data/artifacts.json';

type Entry = { at: 'public' | 'artifacts' | 'repo' | 'absent' | 'set';
                bytes?: number; n?: number; claims?: boolean };
const INDEX = index as Record<string, Entry>;
const REPO = 'https://github.com/zmainen/elife-claim-trees/blob/main';

export type ArtifactKind = 'jsonld' | 'json' | 'markdown' | 'image' | 'code' | 'other';

/** Where the artifact is, which decides what can be offered for it.
 *  served — the site has the bytes: download, copy and preview all work.
 *  repo   — it exists, but only in the repository: a link out, nothing more.
 *  absent — declared and never written. Not a link.
 *  set    — a glob, matching some number of files. A count, not a download. */
export type ArtifactState = 'served' | 'repo' | 'absent' | 'set';

export interface View { label: string; href: string }

export interface Artifact {
  /** The declared repo-relative path, with {paper} already substituted. */
  path: string;
  /** Filename alone — what the reader sees on the link. */
  name: string;
  state: ArtifactState;
  /** Where to open the file itself. Absent when nothing was produced. */
  href?: string;
  /** The file in the repository. Absent when it is not there either. */
  source?: string;
  /** True when the site serves the bytes; what copy and preview need. */
  downloadable: boolean;
  bytes?: number;
  /** For a glob: how many files match it. */
  count?: number;
  kind: ArtifactKind;
  /** What this format is, for a reader who has not met it. Absent when the name says it. */
  note?: string;
  /** The site's own renderings of this artifact, where it has any. */
  views: View[];
}

const KIND: Array<[RegExp, ArtifactKind]> = [
  [/\.jsonld$/, 'jsonld'],
  [/\.json$/, 'json'],
  [/\.(md|markdown)$/, 'markdown'],
  [/\.(png|jpg|jpeg|svg|webp)$/, 'image'],
  [/\.(py|js|ts|sh)$/, 'code'],
];

// Named formats the reader may not know by extension. Keyed on the distinctive part of the
// filename rather than the whole thing, so a new paper needs no entry.
const NOTE: Array<[RegExp, string]> = [
  [/\.mira-extended\.jsonld$/, 'MIRA, with the extensions this corpus needed'],
  [/\.mira\.jsonld$/, 'MIRA — the schema eLife reads'],
  [/\.oxa\.json$/, 'Open Exchange Architecture'],
  [/\.dg\.jsonld$/, 'Discourse Graphs — the Q/C/E/S ontology'],
  [/\.gap-report\.md$/, 'what the conversion dropped'],
  [/\.formats\.(md|json)$/, 'what each conversion cost, measured'],
  [/provenance\.json$/, 'what was re-run, and what came back'],
  [/\.marked\.md$/, 'the paper itself, with every claim and gap located in it'],
  [/\/prepared\.json$/, 'the text the readers were given'],
  [/\.output\.json$/, 'what the model returned, claim by claim'],
];

// Outputs the site already renders. A JSON-LD file is a download; the same content as a claim
// list or a graph is something a reader can actually read, and for several of these formats
// that view already exists and was reachable only by knowing where to look.
const VIEWS: Array<[RegExp, Array<[string, string]>]> = [
  [/^claims\/[^/]+\/alt-/, [['in the claim list', '/papers/{paper}/?view=claims']]],
  [/^claims\//, [['as a claim list', '/papers/{paper}/?view=claims'],
                 ['as a graph', '/papers/{paper}/?view=graph']]],

  [/abstract-mapping\//, [['against the abstract', '/papers/{paper}/abstract-map/']]],
  [/synthesis-v3\//, [['as the restated argument', '/papers/{paper}/synthesis/']]],
  [/\.formats\.md$/, [['as the format comparison', '/papers/{paper}/formats-report/']]],
];

const kindOf = (p: string): ArtifactKind =>
  KIND.find(([re]) => re.test(p))?.[1] ?? 'other';

/** Where an artifact is addressable, per state. `public` keeps its own path — those URLs are
 *  published and linked elsewhere; everything else the site serves comes from the endpoint. */
const hrefOf = (path: string, at: Entry['at'], base: string) =>
  at === 'public' ? `${base}/${path}`
  : at === 'artifacts' ? `${base}/artifacts/${path}`
  : undefined;

export interface Where { paper: string; layer: string }

/** Resolve one declared path. `base` is the site's BASE_URL without a trailing slash. */
export function artifact(path: string, base: string, where?: Where): Artifact {
  const e = INDEX[path] ?? { at: 'absent' as const };
  const href = hrefOf(path, e.at, base);
  // A view of a file that was never written renders nothing. Offered only where there is
  // something to look at.
  const views = where && e.at !== 'absent'
    ? [...(VIEWS.find(([re]) => re.test(path))?.[1] ?? []),
       // A run the cell page can render as claims, which build-data.js checked by reading it.
       ...(e.claims ? [['claim by claim', '/papers/{paper}/{layer}/'] as [string, string]] : []),
      ].map(([label, tpl]) => ({
        label,
        href: base + tpl.replace('{paper}', where.paper).replace('{layer}', where.layer),
      }))
    : [];
  return {
    path,
    name: path.split('/').pop() ?? path,
    state: e.at === 'set' ? 'set'
         : e.at === 'absent' ? 'absent'
         : href ? 'served' : 'repo',
    href,
    source: e.at === 'absent' ? undefined : `${REPO}/${path}`,
    downloadable: Boolean(href),
    bytes: e.bytes,
    count: e.n,
    kind: kindOf(path),
    note: NOTE.find(([re]) => re.test(path))?.[1],
    views,
  };
}

export const artifacts = (paths: string[] | undefined, base: string, where?: Where): Artifact[] =>
  (paths ?? []).map(p => artifact(p, base, where));

/** A directory of claim files is a tree, not a download. Declared paths that name one are
 *  reported as a location so the drawer can say so rather than offering a broken file.
 *
 *  A glob is a third thing, and not this one: `claims/{paper}/*.md` used to pass the extension
 *  test and be offered as a link to a GitHub blob with a literal asterisk in it, a 404 on the
 *  one layer — the claim tree — whose output matters most. It is resolved as a `set` instead,
 *  counted and sent to the views that render those files as pages. */
export const isDirectory = (path: string) => !path.includes('*') && !/\.[a-z0-9]+$/i.test(path);

export const SIZE = (n?: number) =>
  n === undefined ? '' : n < 1024 ? `${n} B`
  : n < 1024 * 1024 ? `${Math.round(n / 1024)} KB`
  : `${(n / 1024 / 1024).toFixed(1)} MB`;
