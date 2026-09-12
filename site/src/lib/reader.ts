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
import corpusFacts from '../data/corpus-facts.json';

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

/** A sentence the reader should treat as carrying something: the claims it states, whether it
 *  was judged a gap, and — for a drafted claim awaiting a decision — the span's uid. `uid` is
 *  carried through the matcher so that a draft and a mark can be located by the same code. */
type Mark = { text: string; claims: string[]; gap: boolean; uid?: string };

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

/** Place the marked sentences into the article's paragraphs.
 *
 *  The two texts are the same prose reached by different routes — one through the segmenter,
 *  one through the JATS — so they differ in whitespace, in the section heading the segmenter
 *  glues onto a section's first sentence, and in what each includes: the segmenter's `results`
 *  section carries the figure captions embedded in the results text, which the JATS keeps as
 *  figures instead. So some marks belong to no paragraph at all, and that is normal.
 *
 *  Matching is therefore done once against the whole Results text rather than paragraph by
 *  paragraph. The first attempt walked marks and paragraphs together and stopped a paragraph
 *  at the first mark it could not place — which meant one caption mark early in Wengert's
 *  results blocked the 124 after it, and the page underlined five sentences out of 125.
 *  A mark that matches nowhere is dropped here and the next one is still tried.
 *
 *  Positions are found in whitespace-stripped text and mapped back through an index, so what
 *  the page underlines is the paragraph's own characters and nothing between two marks is lost.
 */
type Ranged = { start: number; end: number; claims: string[]; gap: boolean; uid?: string };

function normIndex(text: string): { norm: string; map: number[] } {
  let out = '';
  const map: number[] = [];
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (/\s/.test(ch)) continue;
    out += (ch === '\u2019' || ch === '\u2018' ? "'" : ch).toLowerCase();
    map.push(i);
  }
  return { norm: out, map };
}

/** Marks placed into each paragraph, as character ranges into that paragraph's own text. */
function placeMarks(paragraphs: { text: string }[], marks: Mark[], titles: string[]): Ranged[][] {
  const indexed = paragraphs.map(p => normIndex(p.text));
  const starts: number[] = [];
  let concat = '';
  for (const p of indexed) { starts.push(concat.length); concat += p.norm; }

  const out: Ranged[][] = paragraphs.map(() => []);
  let cursor = 0;
  for (const m of marks) {
    let ns = norm(m.text);
    let idx = concat.indexOf(ns, cursor);
    if (idx < 0) {
      // The segmenter glues a subsection heading onto the first sentence under it.
      const title = titles.find(t => t && ns.startsWith(t) && ns.length > t.length + 20);
      if (title) {
        const stripped = ns.slice(title.length);
        const j = concat.indexOf(stripped, cursor);
        if (j >= 0) { ns = stripped; idx = j; }
      }
    }
    if (idx < 0) continue;          // a caption or table mark: it belongs to no paragraph
    cursor = idx + ns.length;
    if (!m.claims.length && !m.gap && !m.uid) continue;  // nothing to show for an unmarked sentence

    // Which paragraph holds it. A mark never spans two, because a paragraph break is a
    // sentence break in both texts.
    let pi = starts.length - 1;
    while (pi > 0 && starts[pi] > idx) pi--;
    const local = idx - starts[pi];
    const map = indexed[pi].map;
    if (local + ns.length > map.length) continue;
    out[pi].push({
      start: map[local],
      end: map[local + ns.length - 1] + 1,
      claims: m.claims,
      gap: m.gap,
      uid: m.uid,
    });
  }
  return out;
}

type Piece = { text: string; claims: string[]; gap: boolean; draft: string | null };

/** One paragraph as alternating plain and marked pieces, covering all of its text. */
function pieces(text: string, ranges: Ranged[]): Piece[] {
  const out: Piece[] = [];
  const plain = (t: string): Piece => ({ text: t, claims: [], gap: false, draft: null });
  let at = 0;
  for (const r of ranges.sort((a, b) => a.start - b.start)) {
    if (r.start < at) continue;
    if (r.start > at) out.push(plain(text.slice(at, r.start)));
    out.push({ text: text.slice(r.start, r.end), claims: r.claims, gap: r.gap, draft: r.uid ?? null });
    at = r.end;
  }
  if (at < text.length) out.push(plain(text.slice(at)));
  return out;
}

// ── the drafts awaiting a person ─────────────────────────────────────────────

/** The five roles `gap-claim` may assign, in its own words (extract/prompts/gap-claim.md).
 *  A reviewer may disagree with the role the drafter chose, and choosing between five names
 *  is only a real choice if what they mean travels with them to the card. The tree's other
 *  roles — hypothesis, prediction, synthesis — are not here because they describe a paper's
 *  argument and are assigned when the tree is built, not when a missing result is written down. */
/** The nine roles a claim tree assigns, each with its meaning inline — the vocabulary a reader
 *  chooses from when they correct a claim's role in the adjudication surface. The definitions
 *  are extract/elife_extract/vocabulary.py's, trimmed to a sentence a reader can weigh at the
 *  card. Kept beside DRAFT_ROLES because both answer the same question: a role select is a real
 *  choice only if what each name means travels with it. */
export const TREE_ROLES: [string, string][] = [
  ['hypothesis', 'The proposition the paper sets out to test — the answer it commits to for one research question. Carries no measurement of its own.'],
  ['prediction', 'What should be observed if the hypothesis holds. Deduced, not measured; an empirical claim tests it.'],
  ['empirical', 'A result the paper measured.'],
  ['control', 'A measurement whose work is to eliminate an alternative or show a method works — validation, manipulation checks, most null results.'],
  ['methodological', 'A statement about how the analysis was done, holding for the results that rest on it.'],
  ['scope', 'A condition or limitation every other claim inherits — the sample, the design, what the study does and does not cover.'],
  ['synthesis', 'A conclusion drawn across several of the paper\'s own results.'],
  ['interpretation', 'A claim about what a result means, beyond what was measured.'],
  ['literature-context', 'A claim the paper attributes to other work rather than showing itself.'],
];

/** The three disputes the whole-tree reading must settle (issue #82 § Verdicts), written out so
 *  the surface can put the questions at the top of the tree rather than leaving them implicit. */
export const RULING_QUESTIONS: { id: string; question: string }[] = [
  { id: 'sts-mentalising-role',
    question: 'Is the STS mentalising claim a hypothesis the paper tests, or an interpretation it offers of a result?' },
  { id: 'partner-algorithm-role',
    question: 'Is the partner-algorithm claim about the scope of the deception (what the partner actually did), or a methodological statement about how the task was run?' },
  { id: 'procedure-under-scope',
    question: 'Do the exclusions, the fixed sample size and the design belong under the scope claim as parts of it?' },
];

export const DRAFT_ROLES: [string, string][] = [
  ['empirical', 'A result the paper measured.'],
  ['control', 'A result whose purpose is to eliminate an alternative explanation or to show a method works. Most validation, manipulation checks and negative controls are this.'],
  ['interpretation', 'A claim about what a result means, beyond what was measured.'],
  ['scope', 'A condition or limitation every other claim inherits.'],
  ['literature-context', 'A claim this paper attributes to other work rather than showing.'],
];

/** The decision standing for each of this paper's drafts.
 *  The file is append-only, so a reviewer who changed their mind wrote a second record for the
 *  same uid: the last one is the decision and the earlier ones are the history. Edge flags
 *  share the file and are not decisions about a draft, so they are skipped. */
function decisionsOf(paper: string): Record<string, any> {
  const path = join(process.cwd(), '..', 'review', 'gap-claim-decisions.jsonl');
  if (!existsSync(path)) return {};
  const out: Record<string, any> = {};
  for (const line of readFileSync(path, 'utf8').split('\n')) {
    if (!line.trim()) continue;
    let rec: any;
    try { rec = JSON.parse(line); } catch { continue; }   // a half-written line is not a decision
    if (rec?.type === 'edge' || rec?.paper !== paper || !rec?.uid) continue;
    out[rec.uid] = rec;
  }
  return out;
}

/** The claims `gap-claim` drafted for this paper, each with the decision standing on it.
 *
 *  A draft carries two reasons and they answer different questions: `why` is the drafter's
 *  argument for adding this claim, and the gap verdict's own `why` is the reason the span was
 *  judged to need one at all. A reviewer needs both — the second is what they are being asked
 *  to agree with, and the first is only the proposal.
 *
 *  Most papers have no drafts: `gap-claim` has been run on two of the ten. */
function draftsOf(paper: string) {
  const at = (...p: string[]) => join(process.cwd(), '..', ...p);
  const run = at('runs', paper, 'gap-claim.output.json');
  if (!existsSync(run)) return [];
  const cands: any[] = JSON.parse(readFileSync(run, 'utf8')).candidates ?? [];

  const whyGap: Record<string, string> = {};
  const mapping = at('mappings', `${paper}.json`);
  if (existsSync(mapping)) {
    for (const s of JSON.parse(readFileSync(mapping, 'utf8')).spans ?? []) whyGap[s.uid] = s.why ?? '';
  }
  const decided = decisionsOf(paper);

  return cands.map(c => ({
    uid: c.uid,
    span: (c.span ?? '').trim(),
    slug: c.slug,
    claim: (c.claim ?? '').trim(),
    role: c.role ?? 'empirical',
    panel: c.panel ?? '',
    why: c.why ?? '',
    whyGap: whyGap[c.uid] ?? '',
    decision: decided[c.uid] ?? null,
  }));
}

// ── the whole-tree adjudication (#82) ─────────────────────────────────────────

/** The claim-tree version the committed tree is, from corpus-facts' pipeline state — the same
 *  state the site already carries. A verdict file is bound to it, so the surface reads and writes
 *  the version it is showing rather than guessing. */
function claimTreeVersion(paper: string): number | null {
  const cell = (corpusFacts as any)?.pipeline?.state?.[paper]?.['claim-tree'];
  return cell && typeof cell.v === 'number' ? cell.v : null;
}

/** The verdict lines recorded for one version, raw and in file order. The client resolves the
 *  latest per key; passing the whole history keeps the two surfaces reading the same file.
 *  Under `astro dev` this is re-read on each request, so a verdict posted through the endpoint
 *  shows on reload — the same freshness the gap-claim decisions have. */
function verdictsOf(paper: string, version: number): any[] {
  const path = join(process.cwd(), '..', 'runs', paper, `claim-tree.v${version}.verdicts.jsonl`);
  if (!existsSync(path)) return [];
  const out: any[] = [];
  for (const line of readFileSync(path, 'utf8').split('\n')) {
    if (!line.trim()) continue;
    try { out.push(JSON.parse(line)); } catch { /* a half-written line is not a verdict */ }
  }
  return out;
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
    // The two grains: the whole this claim is a part of, and the parts that hang off it. A
    // part is shown folded beneath its whole, and the default list shows wholes alone, so the
    // page can carry both without opening on the fine grain. Parts sort by slug, the order the
    // numbering letters them in.
    const partOf: string | null = (c['part-of'] ?? [])[0] ?? null;
    const parts: string[] = paper.claims
      .filter((o: any) => (o['part-of'] ?? []).includes(c.slug))
      .map((o: any) => o.slug)
      .sort((a: string, b: string) => a.localeCompare(b));
    return {
      slug: c.slug,
      number: c.number ?? null,
      partOf,
      parts,
      kind: kindOf(c.role, c.stance ?? 'asserts'),
      role: c.role,
      stance: c.stance ?? 'asserts',
      status,
      statusLabel: status === 'na' ? '' : label,
      // The plain wording where the layer has run, the authors' short wording where it has
      // not, and the full claim as a last resort — so a paper without the layer still reads.
      // `||`, not `??`. `short` is a trimmed string, so a claim without one is '' — which
      // `??` accepts, because '' is neither null nor undefined. The row then renders empty.
      // It stayed invisible while every claim had either a plain wording or a short one, and
      // appeared the moment a tree was rewritten: Gädeke went to 74 claims on claim-tree v2,
      // 68 of them with no wording in either field, and the site showed 68 blank lines where
      // its claims had been. A missing wording should cost the reader the full sentence with
      // its statistics, never the claim itself.
      plain: (plain[c.slug] || short || full).trim(),
      hasPlain: Boolean(plain[c.slug]),
      full,
      panel: c.panel ?? null,
      panels,
      method: c.method ?? null,
      dataset: c.dataset ?? null,
      check: checkOf(c),
      // The re-run itself, where one was written. `script` is the path in the repo and
      // `scriptSource` the text of it — 37 claims across the corpus carry both. A verdict a
      // reader cannot audit is a verdict they have to take on trust, and this is the one
      // place the page can hand them the actual check.
      script: c.script ?? null,
      scriptSource: c.scriptSource ?? null,
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
  const titles: string[] = [];
  const collectTitles = (secs: any[]) => secs.forEach(s => {
    titles.push(norm(s.title ?? ''));
    s.blocks.filter((b: any) => b.type === 'sec').forEach((b: any) => collectTitles([b.sec]));
  });
  collectTitles(article?.sections ?? []);

  // The Results paragraphs, in document order — the text the marks were written against.
  const resultsParas: any[] = [];
  const collectParas = (sec: any, inResults: boolean) => {
    for (const b of sec.blocks) {
      if (b.type === 'sec') collectParas(b.sec, inResults || b.sec.type === 'results');
      else if (b.type === 'p' && inResults) resultsParas.push(b);
    }
  };
  (article?.sections ?? []).forEach((s: any) => collectParas(s, s.type === 'results'));

  const placed = marks.length ? placeMarks(resultsParas, marks, titles) : [];

  // ---- the drafts, on the sentences the gap verdicts named
  //
  // A draft's span is a sentence of the Results, so it is located by the matcher that locates
  // the marks — in uid order, because that matcher walks forward through the text and never
  // looks back. A draft written against a table row or a figure caption is in no Results
  // paragraph and places nowhere; the rail lists it instead of losing it.
  const drafts = draftsOf(paperSlug);
  const draftPlaced = drafts.length && resultsParas.length
    ? placeMarks(resultsParas, [...drafts]
        .sort((a, b) => a.uid.localeCompare(b.uid))
        .map(d => ({ text: d.span, claims: [], gap: true, uid: d.uid })), titles)
    : [];

  // A drafted span is usually already carrying a `gap` mark on exactly the same characters,
  // and `pieces` drops a range that overlaps the one before it. So the draft is folded onto
  // the range that is already there rather than pushed beside it: pushed beside it, one of the
  // two would be silently dropped, and which one depends on the order they were found in.
  const inText = new Set<string>();
  draftPlaced.forEach((rs, i) => {
    for (const r of rs) {
      const same = (placed[i] ??= []).find(x => x.start === r.start && x.end === r.end);
      if (same) same.uid = r.uid; else placed[i].push(r);
      inText.add(r.uid!);
    }
  });

  const byPara = new Map<any, Ranged[]>();
  resultsParas.forEach((p, i) => { if (placed[i]?.length) byPara.set(p, placed[i]); });

  const withMarks = (sec: any): any => ({
    ...sec,
    blocks: sec.blocks.map((b: any) => {
      if (b.type === 'sec') return { ...b, sec: withMarks(b.sec) };
      const ranges = byPara.get(b);
      return ranges ? { ...b, sentences: pieces(b.text, ranges) } : b;
    }),
  });
  const sections = (article?.sections ?? []).map((s: any) => withMarks(s));

  // ---- the abstract, with the claims each sentence carries
  const abstract = (amap?.sentences ?? article?.abstract ?? []).map((s: any) => ({
    text: s.text,
    claims: (s.type === 'claim' ? (s.claims ?? []) : []).filter((x: string) => byClaimSlug[x]),
  }));

  // What this paper can be taken away as. MIRA is the one eLife reads, so it is the one the
  // page offers at the top; the rest stay in the record section with their gap report.
  const exportsOf = (name: string) =>
    existsSync(join(process.cwd(), '..', 'exports', `${paperSlug}.${name}`))
      ? `/exports/${paperSlug}.${name}` : null;
  const downloads = {
    mira: exportsOf('mira.jsonld'),
    miraExtended: exportsOf('mira-extended.jsonld'),
    gapReport: exportsOf('gap-report.md'),
    oxa: exportsOf('oxa.json'),
    dg: exportsOf('dg.jsonld'),
  };

  // ---- the whole-tree adjudication payload (dev-only surface; #82)
  // The edge universe is the directed relations the cards show — one per (claim, target,
  // relation). It is what a reader can decide, and the denominator the progress count uses;
  // for a tree whose relations are all in the card vocabulary it equals the file's edge count.
  const adjVersion = claimTreeVersion(paperSlug);
  const treeEdges: [string, string, string][] = [];
  const edgeSeen = new Set<string>();
  for (const c of claims) {
    for (const o of c.out) {
      const k = `${c.slug}|${o.slug}|${o.rel}`;
      if (!edgeSeen.has(k)) { edgeSeen.add(k); treeEdges.push([c.slug, o.slug, o.rel]); }
    }
  }
  const adjudication = adjVersion != null ? {
    version: adjVersion,
    records: verdictsOf(paperSlug, adjVersion),
    edges: treeEdges,
    claimCount: claims.length,
    edgeCount: treeEdges.length,
    roles: TREE_ROLES,
    rulings: RULING_QUESTIONS,
  } : null;

  const marked = placed.reduce((n, rs) => n + rs.filter(r => r.claims.length).length, 0);
  const gaps = placed.reduce((n, rs) => n + rs.filter(r => r.gap).length, 0);
  const rerun = claims.filter((c: any) => c.status === 'matches' || c.status === 'partly').length;
  const undecided = drafts.filter(d => !d.decision).length;

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
    drafts: drafts.map(d => ({ ...d, inText: inText.has(d.uid) })),
    draftRoles: DRAFT_ROLES,
    adjudication,
    counts: { claims: claims.length, rerun, marked, gaps, drafts: drafts.length, undecided },
    downloads,
    hasArticle: Boolean(article),
    hasPlain: Object.keys(plain).length > 0,
  };
}

export type ReaderData = ReturnType<typeof readerData>;
