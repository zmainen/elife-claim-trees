// What a layer produced, as something a reader can open.
//
// `produces` in layers.yaml is a repo-relative path. Some of those families are copied into
// public/ at build and are therefore real URLs on the published site; the rest exist only in
// the repository. The difference is not cosmetic — offering a download that 404s is worse
// than saying plainly that the file is in the repo — so it is measured rather than assumed:
// published-artifacts.json is the set of paths build-data.js actually found under public/.

import published from '../data/published-artifacts.json';

const PUBLISHED = new Set(published as string[]);
const REPO = 'https://github.com/zmainen/elife-claim-trees/blob/main';

export type ArtifactKind = 'jsonld' | 'json' | 'markdown' | 'image' | 'code' | 'other';

export interface Artifact {
  /** The declared repo-relative path, with {paper} already substituted. */
  path: string;
  /** Filename alone — what the reader sees on the link. */
  name: string;
  /** Where to open it: a site URL when published, a GitHub blob otherwise. */
  href: string;
  /** True when the site serves the bytes; false when the link leaves for GitHub. */
  downloadable: boolean;
  kind: ArtifactKind;
  /** What this format is, for a reader who has not met it. Absent when the name says it. */
  note?: string;
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
];

const kindOf = (p: string): ArtifactKind =>
  KIND.find(([re]) => re.test(p))?.[1] ?? 'other';

/** Resolve one declared path. `base` is the site's BASE_URL without a trailing slash. */
export function artifact(path: string, base: string): Artifact {
  const downloadable = PUBLISHED.has(path);
  return {
    path,
    name: path.split('/').pop() ?? path,
    href: downloadable ? `${base}/${path}` : `${REPO}/${path}`,
    downloadable,
    kind: kindOf(path),
    note: NOTE.find(([re]) => re.test(path))?.[1],
  };
}

export const artifacts = (paths: string[] | undefined, base: string): Artifact[] =>
  (paths ?? []).map(p => artifact(p, base));

/** A directory of claim files is a tree, not a download. Declared paths that name one are
 *  reported as a location so the drawer can say so rather than offering a broken file. */
export const isDirectory = (path: string) => !/\.[a-z0-9]+$/i.test(path);
