// What a reproduction record says, and what it must not be mistaken for.
//
// A record here means one thing: somebody re-ran the authors' deposited code against their
// deposited data and compared the number that came out to the number in the paper. It is a
// fact about *our* run, not about whether the claim is true. The site said "✓ verified" in
// green and meant the first while reading as the second, on 61 of 254 claims — and said
// "Unverified" in grey on the 48 nobody had attempted, which reads as a failing grade for
// work not yet begun.
//
// Two rules follow, and they are why this file looks the way it does.
//
// THE SUBJECT IS US. Every label names what we did: "re-ran: numbers match", "not re-run
// yet", "couldn't re-run". None of them is an adjective describing the claim.
//
// GREEN DOES NOT MEAN TRUE. Green and red are the universal truth signal and we were spending
// them on provenance. Reproduction now uses the tooling palette — slate and blue — and nothing
// on this site is green for "correct". The paper's own argument keeps the role colours, which
// is where a reader's judgement of the science belongs.

/** The outcome of a re-run, as a fact about the run. */
export type ReproOutcome = 'match' | 'partial' | 'differs' | 'blocked' | 'not-attempted' | 'none';

/** Stored status values map onto five outcomes. The stored vocabulary is unchanged — renaming
 *  it is a corpus-wide migration and belongs in its own change — so the translation lives
 *  here, at the one place the site reads it. */
export function outcomeOf(status: string | null | undefined): ReproOutcome {
  const s = status ?? '';
  // Two vocabularies are stored. build-data.js derives a short one onto the claim —
  // verified / partial / blocked / unattempted / unknown — while individual reproduction
  // records use the longer `verified:*` and `unverified:*` forms. Both are read here, which
  // is the point of having one translation: getting this wrong silently hides every chip,
  // as it did until the built page was checked rather than the source.
  if (s === 'verified') return 'match';
  if (s === 'partial') return 'partial';
  if (s === 'blocked') return 'blocked';
  if (s === 'unattempted') return 'not-attempted';
  if (s === 'unknown' || s === '') return 'none';

  if (s.startsWith('failed')) return 'differs';
  if (s === 'verified:interpretive') return 'match';
  if (s.startsWith('verified')) return 'partial';
  if (s === 'unverified' || s === 'unverified:partial') return 'not-attempted';
  if (s.startsWith('unverified')) return 'blocked';
  return 'none';
}

/** What we did, in the first person. Never an adjective about the claim. */
export const OUTCOME_LABEL: Record<ReproOutcome, string> = {
  'match': 're-ran: numbers match',
  'partial': 're-ran: partly matches',
  'differs': 're-ran: differs',
  'blocked': 'couldn’t re-run',
  'not-attempted': 'not re-run yet',
  'none': '',
};

/** The short form, for a chip clipped to a card. Still first-person. */
export const OUTCOME_SHORT: Record<ReproOutcome, string> = {
  'match': 're-ran · matches',
  'partial': 're-ran · partly',
  'differs': 're-ran · differs',
  'blocked': 'couldn’t re-run',
  'not-attempted': 'not re-run',
  'none': '',
};

// Slate and blue: tooling, not verdict. `differs` is the one outcome that earns a warm colour,
// because a reproduction that disagrees with the paper is a finding rather than a status.
export const OUTCOME_TAILWIND: Record<ReproOutcome, string> = {
  'match': 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300',
  'partial': 'bg-slate-50 text-slate-600 dark:bg-slate-800/60 dark:text-slate-400',
  'differs': 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300',
  'blocked': 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
  'not-attempted': 'bg-transparent text-gray-400 dark:text-gray-600',
  'none': 'bg-transparent text-gray-400 dark:text-gray-600',
};

/** Graph node colours for the reproduction layer, when it is switched on. */
export const OUTCOME_COLOR: Record<ReproOutcome, string> = {
  'match': '#475569',        // slate-600
  'partial': '#94a3b8',      // slate-400
  'differs': '#d97706',      // amber-600 — a disagreement is worth seeing
  'blocked': '#cbd5e1',      // slate-300
  'not-attempted': '#e2e8f0',
  'none': '#e2e8f0',
};

/** Why we could not re-run it, where the stored status says. */
export const BLOCKED_REASON: Record<string, string> = {
  'unverified:no-data': 'no data deposited',
  'unverified:no-code': 'no code deposited',
  'unverified:code-error': 'the deposited code errored',
  'unverified:compute-infeasible': 'needs specialist compute',
};

// ── The paper's own argument ────────────────────────────────────────────────
// These colour the tree by what a claim *does* in the paper. They are the default, and with
// the reproduction layer switched off they are all a reader sees — which is the test that the
// separation is real: turn the layer off and the tree shows what the paper argues, carrying
// no verdicts of ours at all.

export const ROLE_COLOR: Record<string, string> = {
  'hypothesis': '#60a5fa',
  'prediction': '#60a5fa',
  'literature-context': '#a78bfa',
  'synthesis': '#60a5fa',
  'interpretation': '#60a5fa',
  'scope': '#94a3b8',
  'methodological': '#94a3b8',
  'empirical': '#64748b',
  'control': '#64748b',
};

export const EPISTEMIC_TAILWIND: Record<string, string> = {
  'strong': 'bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300',
  'moderate': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300',
  'weak': 'bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-300',
  'contested': 'bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-300',
  'hypothesis': 'bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300',
  'unknown': 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
};

/** A claim's colour in the graph.
 *
 *  `repro` is the layer switch. Off — the default — a node is coloured by its role, so the
 *  tree shows the paper's argument and none of our verdicts. On, a node carries the outcome
 *  of our re-run in the tooling palette.
 */
export function nodeColor(status: string, role?: string | null, repro = false): string {
  if (repro) {
    const o = outcomeOf(status);
    if (o !== 'none') return OUTCOME_COLOR[o];
  }
  if (role && ROLE_COLOR[role]) return ROLE_COLOR[role];
  return '#cbd5e1';
}

// ── Retired ─────────────────────────────────────────────────────────────────
// STATUS_COLOR, STATUS_LABEL and STATUS_TAILWIND keyed the green/red truth palette directly
// off the stored status and are gone. Anything that needs a label goes through `outcomeOf`,
// which is the only place the stored vocabulary is read.
