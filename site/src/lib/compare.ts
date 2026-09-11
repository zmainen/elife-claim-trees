// Aligning two versions of a claims-shaped output.
//
// A prompt change, a model swap or a re-run produces a second version of a reader, a
// reconciliation or a claim tree, and the only useful question about it is what changed. Two
// claim sets about one paper do not share slugs and rarely share wording — `evaluate` learned
// this when its string matcher scored 0/33 on a re-run of Gädeke — so the alignment is by the
// claim text, exact first and then by a cheap token overlap, not by any identifier.
//
// The matcher here is deliberately mechanical and local: no model call, no network, run at
// build over files the site already has. It will miss a pairing a reader would make from
// meaning alone, and it says so by leaving both claims in the only-in-old and only-in-new
// lists rather than forcing a match. That is the honest failure for a diff: a missed pair
// reads as one claim dropped and one added, which is visible, where a wrong pair reads as a
// role or panel change that never happened.

export interface ClaimLite {
  /** The claim sentence — what the alignment is on. */
  text: string;
  role?: string | null;
  panel?: string | null;
  slug?: string | null;
}

export interface Pair {
  old: ClaimLite;
  new: ClaimLite;
  /** 1 for an exact text match, otherwise the token-overlap score that paired them. */
  score: number;
  exact: boolean;
  /** True where the two carry different roles / panels — what the diff is for. */
  roleChanged: boolean;
  panelChanged: boolean;
}

export interface Alignment {
  matched: Pair[];
  onlyOld: ClaimLite[];
  onlyNew: ClaimLite[];
}

/** Content tokens of a claim: lowercased, punctuation dropped, split on whitespace. Numbers
 *  are kept — they are often the whole of what distinguishes two empirical claims. */
export function tokens(text: string): Set<string> {
  return new Set(
    (text ?? '')
      .toLowerCase()
      .replace(/[^\p{L}\p{N}\s]/gu, ' ')
      .split(/\s+/)
      .filter(Boolean),
  );
}

/** Normalised token overlap — the Jaccard index of the two token sets, in [0, 1]. Cheap, and
 *  symmetric, which a diff wants: the pairing must not depend on which version is "old". */
export function similarity(a: string, b: string): number {
  const ta = tokens(a);
  const tb = tokens(b);
  if (ta.size === 0 || tb.size === 0) return 0;
  let inter = 0;
  for (const t of ta) if (tb.has(t)) inter++;
  return inter / (ta.size + tb.size - inter);
}

const norm = (s: string) => s.toLowerCase().replace(/\s+/g, ' ').trim();
const same = (a?: string | null, b?: string | null) => (a ?? '') !== (b ?? '');

/** Align two claim lists: exact claim text first, then a token overlap above the threshold,
 *  greedily by descending score so the closest surviving pair wins. Whatever is left over is
 *  only-in-old (dropped) or only-in-new (added). */
export function align(oldList: ClaimLite[], newList: ClaimLite[], threshold = 0.5): Alignment {
  const oldLeft = oldList.map((c, i) => ({ c, i }));
  const newLeft = newList.map((c, i) => ({ c, i }));
  const usedOld = new Set<number>();
  const usedNew = new Set<number>();
  const matched: Pair[] = [];

  const pair = (o: ClaimLite, n: ClaimLite, score: number, exact: boolean) =>
    matched.push({
      old: o, new: n, score, exact,
      roleChanged: same(o.role, n.role),
      panelChanged: same(o.panel, n.panel),
    });

  // Pass 1: exact normalised text. An unchanged claim should never be reported as a
  // near-match with a score, and two claims with identical text are the same claim.
  const byText = new Map<string, number[]>();
  for (const { c, i } of newLeft) {
    const k = norm(c.text);
    (byText.get(k) ?? byText.set(k, []).get(k)!).push(i);
  }
  for (const { c, i } of oldLeft) {
    const hits = byText.get(norm(c.text));
    const j = hits?.find(x => !usedNew.has(x));
    if (j !== undefined) {
      usedOld.add(i); usedNew.add(j);
      pair(c, newList[j], 1, true);
    }
  }

  // Pass 2: best token overlap above the threshold, strongest pairs first.
  const cands: { i: number; j: number; s: number }[] = [];
  for (const { c: o, i } of oldLeft) {
    if (usedOld.has(i)) continue;
    for (const { c: n, j } of newLeft.map(x => ({ c: x.c, j: x.i }))) {
      if (usedNew.has(j)) continue;
      const s = similarity(o.text, n.text);
      if (s >= threshold) cands.push({ i, j, s });
    }
  }
  cands.sort((a, b) => b.s - a.s);
  for (const { i, j, s } of cands) {
    if (usedOld.has(i) || usedNew.has(j)) continue;
    usedOld.add(i); usedNew.add(j);
    pair(oldList[i], newList[j], s, false);
  }

  return {
    matched,
    onlyOld: oldList.filter((_, i) => !usedOld.has(i)),
    onlyNew: newList.filter((_, i) => !usedNew.has(i)),
  };
}
