/**
 * The replication layer.
 *
 * A claim carries two different kinds of standing and they must never be rendered as one:
 *
 *   1. What the paper argues — its role, its confidence, its relations to other claims.
 *      That is the tree, and it is the paper's own voice.
 *   2. What happened when *we* re-ran the deposited analysis. That is this file, and it is
 *      our voice, about our work, and it says nothing about whether the paper is right.
 *
 * The site used to call (2) "verified", in green, with a checkmark, up to and including an
 * "All claims verified" badge in a paper header. A reader has no way to take that as anything
 * but a verdict on the paper. It is not one: 61 of 254 claims carried that badge, and all it
 * meant was that a script re-ran the authors' own numbers and got them back.
 *
 * So the vocabulary here follows three rules.
 *
 *   - Every label's subject is us. "Re-ran it — numbers match", never "verified".
 *   - No truth colours. Green and red are the universal true/false signal and this layer is
 *     not about truth; it is monochrome, with a single amber flag reserved for a divergence
 *     the reader genuinely needs to notice.
 *   - Absence beats a grey verdict. A claim nobody has re-run yet, and a claim with nothing
 *     to re-run, get no mark — not a "Unverified" chip that reads as a failing grade.
 */

/** The states a re-run can actually be in. `unknown` means the claim has nothing to re-run. */
export type Replication =
  | 'verified' | 'partial' | 'mismatch' | 'blocked' | 'unattempted' | 'unknown';

/** Full sentence, for a drawer or a tooltip. The subject is always us. */
export const REPLICATION_LABEL: Record<string, string> = {
  verified: 'We re-ran it — the numbers match',
  partial: 'We re-ran it — it partly matches',
  mismatch: 'We re-ran it — the numbers differ',
  blocked: 'We could not re-run it',
  unattempted: 'We have not re-run it yet',
  unknown: 'Nothing here to re-run',
};

/** Chip text, for a card. Keeps "re-ran" in front so the chip cannot be read as a verdict. */
export const REPLICATION_SHORT: Record<string, string> = {
  verified: 're-ran · matches',
  partial: 're-ran · partly matches',
  mismatch: 're-ran · differs',
  blocked: 're-run blocked',
  unattempted: 'not re-run',
  unknown: '',
};

/**
 * Why the claim could not be re-run. Rendered next to `blocked`, because "blocked" on its own
 * invites the reader to supply the worst explanation.
 */
export const BLOCKED_HINT = 'no deposited data, or the analysis needs software we cannot run';

/**
 * Monochrome slate, one amber flag. Deliberately no green and no red: this layer does not
 * grade the paper, and a colour that says "correct" or "wrong" would claim that it does.
 */
export const REPLICATION_COLOR: Record<string, string> = {
  verified: '#475569',
  partial: '#94a3b8',
  mismatch: '#d97706',
  blocked: '#cbd5e1',
  unattempted: '#e2e8f0',
  unknown: '#e2e8f0',
};

/** Tailwind chip classes. Literal strings — Tailwind scans source text, so no interpolation. */
export const REPLICATION_TAILWIND: Record<string, string> = {
  verified: 'bg-slate-100 text-slate-700 border border-slate-300 ' +
    'dark:bg-slate-800 dark:text-slate-200 dark:border-slate-600',
  partial: 'bg-slate-50 text-slate-600 border border-slate-200 ' +
    'dark:bg-slate-800/60 dark:text-slate-300 dark:border-slate-700',
  mismatch: 'bg-amber-50 text-amber-800 border border-amber-300 ' +
    'dark:bg-amber-950 dark:text-amber-200 dark:border-amber-800',
  blocked: 'bg-transparent text-slate-500 border border-dashed border-slate-300 ' +
    'dark:text-slate-400 dark:border-slate-600',
  unattempted: 'bg-transparent text-slate-400 border border-dashed border-slate-200 ' +
    'dark:text-slate-500 dark:border-slate-700',
  unknown: '',
};

/**
 * Whether to draw a replication mark at all.
 *
 * `unknown` is not uncertainty — it is 36 predictions, 33 hypotheses and 6 literature-context
 * claims that have no number to reproduce in the first place. Marking those "Unverified" told
 * the reader a re-run had failed when none was ever possible.
 */
export function hasReplication(status?: string | null): boolean {
  return !!status && status !== 'unknown' && status in REPLICATION_LABEL;
}

/** Whether the claim is re-runnable in principle, i.e. whether "not re-run yet" is a real gap. */
export function isReplicable(status?: string | null): boolean {
  return !!status && status !== 'unknown';
}

/**
 * The paper's own layer. Role decides a node's colour in the graph, because role is a property
 * of the claim; a re-run result is not, and no longer recolours the node.
 */
export const ROLE_COLOR: Record<string, string> = {
  empirical: '#2563eb',
  control: '#3b82f6',
  hypothesis: '#60a5fa',
  prediction: '#60a5fa',
  synthesis: '#60a5fa',
  interpretation: '#60a5fa',
  'literature-context': '#a78bfa',
  scope: '#94a3b8',
  methodological: '#94a3b8',
};

/** The paper's stated confidence in its own claim. Separate scale, separate hues. */
export const EPISTEMIC_TAILWIND: Record<string, string> = {
  strong: 'bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-200',
  moderate: 'bg-sky-100 text-sky-800 dark:bg-sky-950 dark:text-sky-200',
  weak: 'bg-indigo-50 text-indigo-700 dark:bg-indigo-950 dark:text-indigo-300',
  contested: 'bg-violet-100 text-violet-800 dark:bg-violet-950 dark:text-violet-200',
  hypothesis: 'bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300',
  unknown: 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400',
};

/** A graph node takes its colour from what the claim *is*, never from how our re-run went. */
export function nodeColor(_status: string, role?: string | null): string {
  return (role && ROLE_COLOR[role]) || '#94a3b8';
}
