// What the reader needs, assembled once at build time.
//
// The paper page shows one paper three ways — the article itself, its findings figure by
// figure, its argument — and the same claim card from all three. Each view needs the same
// four things joined: the article the `article` layer parsed, the claims `claim-tree` wrote,
// the plain wordings `plain-claim` produced, and the sentence marks `marks` wrote into the
// document. Joining them in the component would mean doing it in the browser, three times,
// from data shipped three times; joining them here means the page ships one object.
//
// Everything below is translation, and the translations are the design: a role and a stance
// become a noun a reader knows, a verification record becomes a sentence, fourteen relation
// names become the phrases the claim card prints. See docs/design/2026-09-11-the-reader.html.

import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import corpus from '../data/claims.json';
import paperSummaries from '../data/paper-summaries.json';

const articles = import.meta.glob('../data/article/*.json', { eager: true }) as Record<string, { default: any }>;
const plainClaims = import.meta.glob('../data/plain-claims/*.json', { eager: true }) as Record<string, { default: any }>;
const abstractMaps = import.meta.glob('../data/abstract-mapping/*.json', { eager: true }) as Record<string, { default: any }>;

const bySlug = (m: Record<string, { default: any }>, slug: string) => {
  const k = Object.keys(m).find(x => x.endsWith(`/${slug}.json`));
  return k ? m[k].default : null;
};

// ── the vocabulary, in the reader's words ────────────────────────────────────

/** A claim's kind: what role × stance means, said as a noun a reader already has.
 *  `rejects` is the load-bearing one — six of Gädeke's claims are alternatives the paper
 *  argues against, and rendering them as hypotheses made the page open with propositions the
 *  paper denies. */
export function kindOf(role: string, stance: string): string {
  if (stance === 'rejects') return 'Alternative ruled out';
  if (stance === 'attributes') return 'Attributed to others';
  switch (role) {
    case 'hypothesis': return 'Hypothesis';
    case 'prediction': return 'Prediction';
    case 'empirical': return 'Finding';
    case 'control': return 'Check';
    case 'interpretation': return 'Interpretation';
    case 'synthesis': return 'Conclusion';
    case 'scope': return 'Caveat';
    case 'methodological': return 'Method';
    case 'literature-context': return 'From the literature';
    default: return 'Claim';
  }
}

export type CheckState = 'matches' | 'partly' | 'differs' | 'blocked' | 'none' | 'na';

const CHECK: Record<string, [CheckState, string]> = {
  verified: ['matches', 'Re-run matches'],
  partial: ['partly', 'Re-run partly matches'],
  differs: ['differs', 'Re-run differs'],
  blocked: ['blocked', 'Could not re-run'],
  unattempted: ['none', 'Not re-run'],
  unknown: ['na', ''],
};

/** Roles with nothing to re-run. A hypothesis is not a measurement, and the old drawer's
 *  `Not yet assessed` banner on one implied a re-run was owed that never could be. */
const NOT_RERUNNABLE = new Set(['hypothesis', 'prediction', 'scope', 'literature-context', 'methodological']);

/** The re-run, as a sentence and a pair of values.
 *  `notes` is prose written by whoever recorded the reproduction, and the pair we want is
 *  stated in it in one shape — `Paper: … Reproduced: …` — for every claim the audit re-checked.
 *  `verifyRow` carries the same pair for the older records. Neither is reformatted here: the
 *  point of showing both numbers is that a reader can see they are the same number. */
function checkOf(c: any): { paper?: string; reproduced?: string; date?: string; how?: string } | null {
  if (c.status === 'unknown') return null;
  const notes: string = c.notes ?? '';
  const m = notes.match(/Paper:\s*([\s\S]+?)\.?\s+Reproduced:\s*([\s\S]+?)(?:\s+[—-]\s+|\.\s|$)/);
  const row = c.verifyRow;
  const out: any = {};
  if (m) { out.paper = m[1].trim(); out.reproduced = m[2].trim(); }
  else if (row?.paperValue) { out.paper = row.paperValue; out.reproduced = row.reproduced; }
  const date = notes.match(/Re-checked (\d{4}-\d{2}-\d{2})/);
  if (date) out.date = date[1];
  if (notes.includes('deposited per-trial data')) out.how = "the authors' deposited per-trial data";
  else if (notes.includes('deposited group statistical map')) out.how = "the authors' deposited group statistical map";
  else if (notes.includes('deposited')) out.how = "the authors' deposited data";
  else if (/Methods|code inspection/.test(notes)) out.how = 'reading the Methods section';
  return out;
}

/** The fourteen relations, outward and inward, in the phrases the card prints.
 *  Ordered: what the claim rests on and answers to first, what rests on it second. */
const OUT: Record<string, string> = {
  tests: 'Tests', confirms: 'Confirms', supports: 'Supports', validates: 'Validates',
  'rules-out': 'Rules out', refutes: 'Refutes', requires: 'Relies on', 'derived-from': 'Follows from',
  entails: 'Leads to the prediction', predicts: 'Predicts', interprets: 'Interprets',
  'dissociates-with': 'Contrasts with', scopes: 'Applies to', 'enables-method': 'Makes possible',
};
const IN: Record<string, string> = {
  tests: 'Tested by', confirms: 'Confirmed by', supports: 'Supported by', validates: 'Validated by',
  'rules-out': 'Ruled out by', refutes: 'Refuted by', requires: 'Relied on by', 'derived-from': 'Basis for',
  entails: 'Predicted from', interprets: 'Interpreted by', scopes: 'Qualified by',
  'dissociates-with': 'Contrasts with', 'enables-method': 'Made possible by',
};
export const REL_ORDER = [
  ...Object.values(OUT).slice(0, 10), ...Object.values(IN),
];

/** `fig4e, fig4f` → [['4','E'],['4','F']]; `fig3 (text, no dedicated panel)` → [['3','']]. */
export function panelRefs(panel?: string | null): [string, string][] {
  if (!panel) return [];
  const out: [string, string][] = [];
  const seen = new Set<string>();
  for (const m of panel.toLowerCase().matchAll(/fig(?:ure)?\s*0*(\d+)([a-z])?/g)) {
    const key = `${m[1]}${m[2] ?? ''}`;
    if (seen.has(key)) continue;
    seen.add(key);
    out.push([m[1], (m[2] ?? '').toUpperCase()]);
  }
  return out;
}

// ── the marked paper ─────────────────────────────────────────────────────────

const norm = (s: string) => s.replace(/\s+/g, '').replace(/[’‘]/g, "'").toLowerCase();

type Mark = { text: string; claims: string[]; gap: boolean };

/** The results section of `marked/<paper>.marked.md`, as sentences carrying claim slugs.
 *
 *  The marks name claims by UUID; a `gap` key means the span states a result no claim
 *  accounts for, and `no-assertion` that it states no result at all. One sentence can carry
 *  several marks — a prediction and the finding that tests it are often one sentence.
 *
 *  Nine of the ten papers have no marked file yet, and that is the honest state of the
 *  corpus rather than a failure here: the paper renders, and its sentences are silent. */
function marksOf(paper: string, uuidToSlug: Record<string, string>): Mark[] {
  const path = join(process.cwd(), '..', 'marked', `${paper}.marked.md`);
  if (!existsSync(path)) return [];
  const text = readFileSync(path, 'utf8');
  const results = text.split('\n## results')[1]?.split('\n## captions')[0];
  if (!results) return [];

  const out: Mark[] = [];
  for (const line of results.split('\n')) {
    const raw = line.trim();
    if (!raw) continue;
    const claims = new Set<string>();
    let gap = false;
    for (const m of raw.matchAll(/⟦>\w+ claim=([^:]+):/g)) {
      if (m[1] === 'gap') gap = true;
      else if (uuidToSlug[m[1]]) claims.add(uuidToSlug[m[1]]);
    }
    const bare = raw.replace(/⟦[\s\S]*?⟧/g, '').trim();
    if (bare) out.push({ text: bare, claims: [...claims], gap });
  }
  return out;
}

/** Walk the marked sentences through one paragraph, in order.
 *
 *  The two texts are the same prose reached by different routes — one through the segmenter,
 *  one through the JATS — so they differ in whitespace and in the section heading the
 *  segmenter glues onto the first sentence of a section. Matching on whitespace-stripped text,
 *  and stripping a known heading from the front, recovers the rest. A sentence that still does
 *  not match is skipped rather than guessed at: a mark on the wrong sentence is worse than a
 *  sentence with no mark. */
function splitParagraph(text: string, marks: Mark[], cursor: { i: number }, titles: string[]): Mark[] | null {
  const target = norm(text);
  const recs: Mark[] = [];
  let at = 0;
  while (cursor.i < marks.length) {
    const m = marks[cursor.i];
    let ns = norm(m.text);
    let display = m.text;
    let idx = target.indexOf(ns, at);
    if (idx < 0) {
      const title = titles.find(t => t && ns.startsWith(t) && ns.length > t.length + 20);
      if (title) {
        const stripped = ns.slice(title.length);
        const j = target.indexOf(stripped, at);
        if (j >= 0) {
          // Drop the same number of visible characters from the display text.
          let seen = 0, k = 0;
          while (k < display.length && seen < title.length) { if (!/\s/.test(display[k])) seen++; k++; }
          display = display.slice(k).trim();
          ns = stripped; idx = j;
        }
      }
    }
    if (idx < 0) break;
    recs.push({ text: display, claims: m.claims, gap: m.gap });
    at = idx + ns.length;
    cursor.i++;
  }
  return recs.length ? recs : null;
}

// ── assembly ─────────────────────────────────────────────────────────────────

export function readerData(paperSlug: string) {
  const paper = (corpus as any).papers.find((p: any) => p.slug === paperSlug);
  const article = bySlug(articles, paperSlug);
  const plain: Record<string, string> = Object.fromEntries(
    (bySlug(plainClaims, paperSlug)?.claims ?? []).map((c: any) => [c.slug, c.plain]));
  const amap = bySlug(abstractMaps, paperSlug);
  const summary = (paperSummaries as Record<string, any>)[paperSlug] ?? null;

  const byClaimSlug: Record<string, any> = {};
  for (const c of paper.claims) byClaimSlug[c.slug] = c;
  const uuidToSlug: Record<string, string> = {};
  for (const c of paper.claims) uuidToSlug[c.uuid] = c.slug;

  // ---- claims
  const claims = paper.claims.map((c: any) => {
    const [state, label] = CHECK[c.status] ?? ['na', ''];
    const runnable = !NOT_RERUNNABLE.has(c.role) || state === 'matches' || state === 'partly';
    const status: CheckState = runnable ? state : 'na';
    const panels = panelRefs(c.panel);
    const out: { rel: string; label: string; slug: string }[] = [];
    for (const [rel, label] of Object.entries(OUT)) {
      for (const t of c[rel] ?? []) if (byClaimSlug[t]) out.push({ rel, label, slug: t });
    }
    const inward: { rel: string; label: string; slug: string }[] = [];
    for (const other of paper.claims) {
      for (const [rel, label] of Object.entries(IN)) {
        if ((other[rel] ?? []).includes(c.slug)) inward.push({ rel, label, slug: other.slug });
      }
    }
    const full = (c.claim ?? '').trim();
    const short = (c.shortClaim ?? c.displayClaim ?? '').trim();
    return {
      slug: c.slug,
      number: c.number ?? null,
      kind: kindOf(c.role, c.stance ?? 'asserts'),
      role: c.role,
      stance: c.stance ?? 'asserts',
      status,
      statusLabel: status === 'na' ? '' : label,
      // The plain wording where the layer has run, the authors' short wording where it has
      // not, and the full claim as a last resort — so a paper without the layer still reads.
      plain: (plain[c.slug] ?? short ?? full).trim(),
      hasPlain: Boolean(plain[c.slug]),
      full,
      panel: c.panel ?? null,
      panels,
      method: c.method ?? null,
      dataset: c.dataset ?? null,
      check: checkOf(c),
      out,
      in: inward,
    };
  });
  const claimBySlug: Record<string, any> = {};
  for (const c of claims) claimBySlug[c.slug] = c;

  // ---- figures, each with the claims its panels carry
  const figures = (article?.figures ?? [])
    .filter((f: any) => !f.supplement)
    .map((f: any) => ({
      ...f,
      claims: claims
        .filter((c: any) => c.panels.some(([n]: [string, string]) => n === f.num))
        .map((c: any) => ({
          slug: c.slug,
          letters: c.panels.filter(([n, l]: [string, string]) => n === f.num && l).map(([, l]: [string, string]) => l),
        }))
        .sort((a: any, b: any) => (a.letters[0] ?? 'ZZ').localeCompare(b.letters[0] ?? 'ZZ')),
    }));

  // ---- the article, with the marked sentences folded into the Results paragraphs
  const marks = marksOf(paperSlug, uuidToSlug);
  const cursor = { i: 0 };
  const titles: string[] = [];
  const collectTitles = (secs: any[]) => secs.forEach(s => {
    titles.push(norm(s.title ?? ''));
    s.blocks.filter((b: any) => b.type === 'sec').forEach((b: any) => collectTitles([b.sec]));
  });
  collectTitles(article?.sections ?? []);

  const withMarks = (sec: any, inResults: boolean): any => ({
    ...sec,
    blocks: sec.blocks.map((b: any) => {
      if (b.type === 'sec') return { ...b, sec: withMarks(b.sec, inResults || b.sec.type === 'results') };
      if (b.type !== 'p' || !inResults || !marks.length) return b;
      const sentences = splitParagraph(b.text, marks, cursor, titles);
      return sentences ? { ...b, sentences } : b;
    }),
  });
  const sections = (article?.sections ?? []).map((s: any) => withMarks(s, s.type === 'results'));

  // ---- the abstract, with the claims each sentence carries
  const abstract = (amap?.sentences ?? article?.abstract ?? []).map((s: any) => ({
    text: s.text,
    claims: (s.type === 'claim' ? (s.claims ?? []) : []).filter((x: string) => byClaimSlug[x]),
  }));

  const marked = marks.length;
  const gaps = marks.filter(m => m.gap).length;
  const rerun = claims.filter((c: any) => c.status === 'matches' || c.status === 'partly').length;

  return {
    slug: paperSlug,
    title: paper.title,
    authors: paper.authors,
    journal: paper.journal,
    year: article?.year ?? '',
    doi: paper.doi,
    url: paper.url,
    github: paper.github,
    keywords: article?.keywords ?? [],
    stage: paper.stage,
    summary,
    abstract,
    sections,
    figures,
    tables: article?.tables ?? [],
    claims,
    counts: { claims: claims.length, rerun, marked, gaps },
    hasArticle: Boolean(article),
    hasPlain: Object.keys(plain).length > 0,
  };
}

export type ReaderData = ReturnType<typeof readerData>;
