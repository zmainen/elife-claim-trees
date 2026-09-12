// The paper page: the paper first, and the claims reached from it.
//
// Three depths of one paper — the article itself, its findings figure by figure, its argument
// — and one claim card reachable from all three. The card is the old ClaimDrawer's job, done
// in the reader's vocabulary: what the claim says in plain words, where in the paper it is
// said, whether our re-run matched, and what it connects to.
//
// Design note: docs/design/2026-09-11-the-reader.html. The data is assembled in lib/reader.ts.

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

type Claim = {
  slug: string; number: string | null; kind: string; role: string; stance: string;
  partOf: string | null; parts: string[];
  status: 'matches' | 'partly' | 'differs' | 'blocked' | 'none' | 'na';
  statusLabel: string; plain: string; hasPlain: boolean; full: string;
  panel: string | null; panels: [string, string][]; method: string | null; dataset: string | null;
  check: { paper?: string; reproduced?: string; date?: string; how?: string } | null;
  script: string | null; scriptSource: string | null;
  out: { rel: string; label: string; slug: string }[];
  in: { rel: string; label: string; slug: string }[];
};

type Props = { data: any; base: string };

/** The claims a reader means by "what this paper found". A hypothesis is not a finding, and a
 *  paper's rail should not open with six propositions it argues against. */
const RESULT_KINDS = new Set(['Finding', 'Check', 'Interpretation', 'Conclusion']);

const REL_ORDER = [
  'Tests', 'Confirms', 'Supports', 'Validates', 'Rules out', 'Refutes', 'Relies on',
  'Follows from', 'Leads to the prediction', 'Predicts', 'Interprets', 'Contrasts with',
  'Applies to', 'Makes possible',
  'Tested by', 'Confirmed by', 'Supported by', 'Validated by', 'Ruled out by', 'Refuted by',
  'Relied on by', 'Basis for', 'Predicted from', 'Interpreted by', 'Qualified by', 'Made possible by',
];

const trimDot = (s: string) => s.replace(/\s*[.]\s*$/, '');
const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** "Figure 3D, H" inside a sentence becomes a link to the figure.
 *  The marked sentences arrive as plain text — the marks were written onto the segmenter's
 *  prose, not onto the JATS — so the cross-references the article carries are put back here. */
const linkFigures = (text: string) =>
  esc(text).replace(/\bFigure\s+(\d+)([A-Z](?:\s*[,–-]\s*[A-Z])*)?/g,
    (m, n) => `<a class="rd-xref" href="#fig${n}">${m}</a>`);

function Dot({ c }: { c: Claim }) {
  if (c.status === 'na') return null;
  return <span className={`rd-dot rd-${c.status}`} title={c.statusLabel} aria-label={c.statusLabel} />;
}

// ── drafts: a proposed claim, and the decision it is waiting for ──────────────

type Decision = {
  decision: string; claim: string; note: string; by: string; role?: string; decided_at: string;
};
type Draft = {
  uid: string; span: string; slug: string; claim: string; role: string; panel: string;
  why: string; whyGap: string; inText: boolean; decision: Decision | null;
};

/** A decision, once it is one. */
const DECIDED: Record<string, string> = {
  accept: 'Added as drafted', edit: 'Added, reworded', reject: 'Not a claim',
};

/** The write side of the reader. It exists only under `npm run dev` — the published site is
 *  static and answers 404 — so every caller must be able to carry on without it. */
async function postReview(base: string, record: Record<string, unknown>) {
  const res = await fetch(`${base}/dev-review.json`, {
    method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify(record),
  });
  const body = await res.json().catch(() => null);
  if (!res.ok) {
    throw new Error(res.status === 404
      ? 'This page is the published build, which cannot write anything.'
      : (body?.error ?? `the endpoint answered ${res.status}`));
  }
  return body;
}

/** Who is deciding. The five decisions already on file are signed `unnamed`, because the page
 *  that took them asked for a name in a corner of a header nobody read. */
function Who({ id, who, setWho }: { id: string; who: string; setWho: (s: string) => void }) {
  return (
    <p className="rd-who">
      <label htmlFor={id}>Reviewing as</label>
      <input id={id} value={who} placeholder="your name" autoComplete="name"
        onChange={e => setWho(e.target.value)} />
    </p>
  );
}

/** A reader saying one of the graph's edges is wrong.
 *  It writes down the dispute and nothing else: the relation stays in the graph, because an
 *  edge is an assertion the extraction made and removing it silently from one reader's click
 *  would leave no record that anybody disagreed. */
function EdgeFlag({ base, paper, claim, rel, label, target, who }:
  { base: string; paper: string; claim: string; rel: string; label: string; target: string; who: string }) {
  const [open, setOpen] = useState(false);
  const [note, setNote] = useState('');
  const [sent, setSent] = useState(false);
  const [err, setErr] = useState('');

  if (sent) return <span className="rd-flagged">Flagged as wrong</span>;
  if (!open) {
    return (
      <button className="rd-flag" onClick={() => setOpen(true)}
        title={`Say that "${label}" is the wrong relation here`}>Wrong?</button>
    );
  }
  const send = async () => {
    if (!who.trim()) { setErr('Add your name in the rail first — the record says who disputed it.'); return; }
    try {
      await postReview(base, {
        type: 'edge', paper, claim, relation: rel, target, note: note.trim(),
        by: who.trim(), decided_at: new Date().toISOString(),
      });
      setSent(true);
    } catch (e: any) {
      setErr(`${e.message} Decisions need the dev server: run npm run dev and flag it there.`);
    }
  };
  return (
    <div className="rd-flagbox">
      <p>“{label}” is wrong here. This records that you disagree; it does not change the graph.</p>
      <input value={note} placeholder="What is wrong with it?" autoFocus
        onChange={e => setNote(e.target.value)}
        onKeyDown={e => { if (e.key === 'Enter') send(); }} />
      <div className="rd-flagact">
        <button className="rd-btn" onClick={send}>Flag it</button>
        <button className="rd-btn rd-btn-q" onClick={() => { setOpen(false); setErr(''); }}>Cancel</button>
      </div>
      {err && <p className="rd-warn">{err}</p>}
    </div>
  );
}

/** The draft card: a claim nobody has agreed to yet, beside the sentence that prompted it.
 *
 *  Defined at module scope rather than inside `Reader`, unlike the claim card. A component
 *  declared in a render body is a new type on every render, so React tears it down and builds
 *  it again — which costs nothing for a card of static text and would empty this one's textarea
 *  of focus, and of the caret's position, on every keystroke typed into it. */
function DraftCard({ d, paper, base, roles, who, setWho, onDecided, onBack, onClose, onShow }: {
  d: Draft; paper: string; base: string; roles: [string, string][];
  who: string; setWho: (s: string) => void;
  onDecided: (uid: string, rec: Decision) => void;
  onBack: () => void; onClose: () => void; onShow: (uid: string) => void;
}) {
  const [text, setText] = useState(d.decision?.claim?.trim() || d.claim);
  const [role, setRole] = useState(d.decision?.role || d.role);
  const [note, setNote] = useState(d.decision?.note ?? '');
  const [busy, setBusy] = useState(false);
  const [failed, setFailed] = useState<{ why: string; record: any } | null>(null);
  const box = useRef<HTMLTextAreaElement>(null);

  const reworded = text.trim() !== d.claim.trim();
  const meaning = roles.find(([r]) => r === role)?.[1] ?? '';

  // `accept` or `edit` is not the reviewer's choice to make: an accepted draft whose wording
  // they changed is an edit, and `promote.py` keeps both wordings so the two can be compared.
  const decide = async (add: boolean) => {
    if (!who.trim()) {
      setFailed(null);
      document.getElementById('rd-who-draft')?.focus();
      return;
    }
    const record = {
      paper, uid: d.uid, slug: d.slug,
      decision: !add ? 'reject' : reworded ? 'edit' : 'accept',
      claim: add ? text.trim() : '',
      role, note: note.trim(), by: who.trim(), decided_at: new Date().toISOString(),
    };
    setBusy(true);
    try {
      await postReview(base, record);
      setFailed(null);
      onDecided(d.uid, record as Decision);
    } catch (e: any) {
      setFailed({ why: e.message, record });
    } finally {
      setBusy(false);
    }
  };

  const standing = d.decision;
  return (
    <div className="rd-card">
      <div className="rd-cardnav">
        <button onClick={onBack}>← All results</button>
        <button onClick={onClose}>Close</button>
      </div>
      <p className="rd-kind rd-kind-draft">
        Proposed claim
        {standing && <span className="rd-settled">{DECIDED[standing.decision] ?? standing.decision}</span>}
      </p>

      {standing && (
        <p className="rd-standing">
          {standing.by} decided this on {(standing.decided_at || '').slice(0, 10)}
          {standing.note ? ` — “${standing.note}”` : ''}. Deciding again supersedes it; both are kept.
        </p>
      )}

      <div className="rd-blk rd-blk-top">
        <p className="rd-k">The paper says</p>
        <p className="rd-dspan">{d.span}</p>
        {d.inText && <p className="rd-cwhere"><button onClick={() => onShow(d.uid)}>Find it in the paper</button></p>}
        {!d.inText && <p className="rd-dnote">This sentence is in a table or a caption, so it is not underlined in the text above.</p>}
      </div>

      <div className="rd-blk">
        <p className="rd-k rd-k-draft">The claim that would be added</p>
        <textarea ref={box} className="rd-dedit" value={text} rows={5}
          onChange={e => setText(e.target.value)} aria-label="The claim, as it would be written" />
        <p className="rd-dslug">{d.slug}{d.panel ? ` · ${d.panel}` : ''}</p>
      </div>

      <div className="rd-blk">
        <p className="rd-k">What kind of claim it is</p>
        <select className="rd-dsel" value={role} onChange={e => setRole(e.target.value)}
          aria-label="The claim's role">
          {roles.map(([r, m]) => <option key={r} value={r} title={m}>{r}</option>)}
        </select>
        <p className="rd-dmeaning">{meaning}</p>
        {role !== d.role && <p className="rd-dnote">Drafted as <b>{d.role}</b>. Your choice is what gets written.</p>}
      </div>

      {d.why && (
        <div className="rd-blk">
          <p className="rd-k">Why it was proposed</p>
          <p>{d.why}</p>
        </div>
      )}
      {d.whyGap && (
        <div className="rd-blk">
          <p className="rd-k">Why nothing covers it</p>
          <p>{d.whyGap}</p>
        </div>
      )}

      <div className="rd-blk">
        <Who id="rd-who-draft" who={who} setWho={setWho} />
        <input className="rd-dnoteinput" value={note} placeholder="A note on your decision, if it needs one"
          onChange={e => setNote(e.target.value)} aria-label="A note on your decision" />
        <div className="rd-dact">
          <button className="rd-btn rd-btn-go" disabled={busy} onClick={() => decide(true)}>
            {reworded ? 'Add it, reworded' : 'Add it'}
          </button>
          {!reworded && (
            <button className="rd-btn" disabled={busy} onClick={() => box.current?.focus()}>Reword it</button>
          )}
          <button className="rd-btn" disabled={busy} onClick={() => decide(false)}>Not a claim</button>
        </div>
        {!who.trim() && <p className="rd-dnote">Your name goes on the record, so it is asked for before the decision is.</p>}
      </div>

      {failed && (
        <div className="rd-blk rd-offline">
          <p className="rd-k">Not recorded</p>
          <p>{failed.why} Decisions are appended by the dev server: run <code>npm run dev</code> and
            decide there, or add this line to <code>review/gap-claim-decisions.jsonl</code> yourself.</p>
          <pre className="rd-copy">{JSON.stringify(failed.record)}</pre>
        </div>
      )}

      <div className="rd-cfoot">
        <span>Drafted by a language model from a span no claim covered</span>
        <a href={`${base}/papers/${paper}/coverage/`}>Coverage ↗</a>
      </div>
    </div>
  );
}

// ── adjudicating a whole tree: the verdict controls (#82) ─────────────────────
//
// This extends the gap-claim surface above rather than adding a third one. The same rail, the
// same claim card, the same dev-only write endpoint and the same "reviewing as" name — but a
// mode in which every claim card carries a verdict (keep / strike / merge / part-of, a role and
// a panel), every relation carries one (ok / wrong direction / wrong relation / strike), and the
// three rulings the tree cannot settle claim-by-claim sit at the top. Decisions land in
// runs/<paper>/claim-tree.v<N>.verdicts.jsonl, bound to the version the page is showing.

type Verdict = Record<string, any>;
type Verdicts = { claims: Record<string, Verdict>; edges: Record<string, Verdict>; rulings: Record<string, Verdict> };

const ekey = (s: string, t: string, r: string) => `${s}|${t}|${r}`;

function resolveVerdicts(records: any[]): Verdicts {
  const claims: Record<string, Verdict> = {};
  const edges: Record<string, Verdict> = {};
  const rulings: Record<string, Verdict> = {};
  for (const r of records || []) {
    if (r?.kind === 'claim' && r.slug) claims[r.slug] = r;                       // latest line wins
    else if (r?.kind === 'edge' && r.source && r.target && r.relation) edges[ekey(r.source, r.target, r.relation)] = r;
    else if (r?.kind === 'ruling' && r.question) rulings[r.question] = r;
  }
  return { claims, edges, rulings };
}

const CLAIM_VERDICTS: [string, string][] = [
  ['keep', 'Keep'], ['strike', 'Strike'], ['merge-into', 'Merge into…'], ['part-of', 'Part of…'],
];
const EDGE_VERDICTS: [string, string][] = [
  ['ok', 'OK'], ['wrong-direction', 'Wrong direction'], ['wrong-relation', 'Wrong relation…'], ['strike', 'Strike'],
];
// The relation vocabulary, raw key → the phrase the card prints (mirrors reader.ts OUT). Used by
// the "wrong relation" and "missing relation" controls.
const REL_VOCAB: [string, string][] = [
  ['tests', 'Tests'], ['confirms', 'Confirms'], ['supports', 'Supports'], ['validates', 'Validates'],
  ['rules-out', 'Rules out'], ['refutes', 'Refutes'], ['requires', 'Relies on'], ['derived-from', 'Follows from'],
  ['entails', 'Leads to the prediction'], ['predicts', 'Predicts'], ['interprets', 'Interprets'],
  ['dissociates-with', 'Contrasts with'], ['scopes', 'Applies to'], ['enables-method', 'Makes possible'],
];

/** Post one verdict line through the dev endpoint and return the record it stored (with
 *  `considered: true` and its timestamp), or throw if the endpoint is not there. */
async function postVerdict(base: string, paper: string, version: number, who: string, fields: Record<string, unknown>) {
  const body = await postReview(base, { file: 'verdicts', paper, version, by: who, ...fields });
  return (body as any)?.record ?? null;
}

/** The verdict standing on a claim, told apart from the skeleton's default by `considered`. */
function claimBadge(v: Verdict | undefined): { label: string; considered: boolean } | null {
  if (!v) return null;
  let label = v.verdict as string;
  if ((v.verdict === 'merge-into' || v.verdict === 'part-of') && v.target) label = `${v.verdict} ${v.target}`;
  return { label, considered: !!v.considered };
}

/** The claim card's verdict controls: is this claim true to the paper, and if not, what to do
 *  with it — plus the role and panel a reader may correct. */
function ClaimVerdict({ base, paper, version, claim, roles, slugs, who, focusWho, standing, onPosted }: {
  base: string; paper: string; version: number; claim: Claim;
  roles: [string, string][]; slugs: { slug: string; plain: string }[];
  who: string; focusWho: () => void; standing: Verdict | undefined;
  onPosted: (rec: Verdict) => void;
}) {
  const [verdict, setVerdict] = useState<string>(standing?.verdict || 'keep');
  const [target, setTarget] = useState<string>(standing?.target || '');
  const [role, setRole] = useState<string>(standing?.role || claim.role);
  const [panel, setPanel] = useState<string>(standing?.panel ?? (claim.panel || ''));
  const [why, setWhy] = useState<string>(standing?.why ?? '');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');

  const needsTarget = verdict === 'merge-into' || verdict === 'part-of';
  const meaning = roles.find(([r]) => r === role)?.[1] ?? '';
  const badge = claimBadge(standing);

  const save = async () => {
    if (!who.trim()) { setErr('Add your name in the rail first.'); focusWho(); return; }
    if (needsTarget && !target) { setErr('Choose the claim to point at.'); return; }
    setBusy(true); setErr('');
    try {
      const rec = await postVerdict(base, paper, version, who, {
        kind: 'claim', slug: claim.slug, verdict,
        ...(needsTarget ? { target } : {}),
        role, panel: panel.trim(), why: why.trim(),
      });
      if (rec) onPosted(rec);
    } catch (e: any) {
      setErr(`${e.message} Run npm run dev to record verdicts.`);
    } finally { setBusy(false); }
  };

  return (
    <div className="rd-blk rd-adj">
      <p className="rd-k rd-k-adj">Your verdict{badge && <span className={`rd-vbadge${badge.considered ? ' on' : ''}`}>{badge.considered ? badge.label : `default: ${badge.label}`}</span>}</p>
      <div className="rd-vrow">
        {CLAIM_VERDICTS.map(([v, lbl]) => (
          <button key={v} className={`rd-vbtn${verdict === v ? ' on' : ''}`} onClick={() => setVerdict(v)}>{lbl}</button>
        ))}
      </div>
      {needsTarget && (
        <select className="rd-dsel" value={target} onChange={e => setTarget(e.target.value)} aria-label="Target claim">
          <option value="">— choose a claim —</option>
          {slugs.filter(s => s.slug !== claim.slug).map(s => (
            <option key={s.slug} value={s.slug}>{s.slug}</option>
          ))}
        </select>
      )}
      <div className="rd-vgrid">
        <label>Role
          <select className="rd-dsel" value={role} onChange={e => setRole(e.target.value)}>
            {roles.map(([r]) => <option key={r} value={r}>{r}</option>)}
          </select>
        </label>
        <label>Panel
          <input className="rd-dnoteinput" value={panel} placeholder="e.g. fig4e, or blank"
            onChange={e => setPanel(e.target.value)} />
        </label>
      </div>
      {meaning && <p className="rd-dmeaning">{meaning}</p>}
      <input className="rd-dnoteinput" value={why} placeholder="Why, if it needs saying"
        onChange={e => setWhy(e.target.value)} aria-label="Why" />
      <div className="rd-dact">
        <button className="rd-btn rd-btn-go" disabled={busy} onClick={save}>Record verdict</button>
      </div>
      {err && <p className="rd-warn">{err}</p>}
    </div>
  );
}

/** One relation's verdict: ok / wrong direction / wrong relation / strike. Replaces the
 *  gap-claim `EdgeFlag` while adjudicating — the same quiet dispute, now a recorded verdict. */
function EdgeVerdict({ base, paper, version, source, target, relation, label, who, focusWho, standing, onPosted }: {
  base: string; paper: string; version: number; source: string; target: string; relation: string;
  label: string; who: string; focusWho: () => void; standing: Verdict | undefined; onPosted: (rec: Verdict) => void;
}) {
  const [open, setOpen] = useState(false);
  const [corrected, setCorrected] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const current = standing?.considered ? (standing.verdict as string) : null;

  const send = async (verdict: string, corr?: string) => {
    if (!who.trim()) { setErr('Add your name in the rail first.'); focusWho(); return; }
    setBusy(true); setErr('');
    try {
      const rec = await postVerdict(base, paper, version, who, {
        kind: 'edge', source, target, relation, verdict, ...(corr ? { corrected: corr } : {}),
      });
      if (rec) onPosted(rec);
      setOpen(false);
    } catch (e: any) {
      setErr(`${e.message} Run npm run dev to record verdicts.`);
    } finally { setBusy(false); }
  };

  if (open) {
    return (
      <div className="rd-flagbox">
        <p>What should “{label}” be? Choose the corrected relation, or leave it and just mark it wrong.</p>
        <select className="rd-dsel" value={corrected} onChange={e => setCorrected(e.target.value)}>
          <option value="">— corrected relation —</option>
          {REL_VOCAB.filter(([k]) => k !== relation).map(([k, l]) => <option key={k} value={k}>{l} ({k})</option>)}
        </select>
        <div className="rd-flagact">
          <button className="rd-btn" disabled={busy} onClick={() => send('wrong-relation', corrected)}>Record</button>
          <button className="rd-btn rd-btn-q" onClick={() => { setOpen(false); setErr(''); }}>Cancel</button>
        </div>
        {err && <p className="rd-warn">{err}</p>}
      </div>
    );
  }
  return (
    <span className="rd-evrow">
      {EDGE_VERDICTS.map(([v, lbl]) => (
        <button key={v} disabled={busy}
          className={`rd-vbtn rd-vbtn-sm${current === v ? ' on' : ''}`}
          onClick={() => (v === 'wrong-relation' ? setOpen(true) : send(v))}>{lbl}</button>
      ))}
      {current && <span className="rd-evstanding">{current}</span>}
      {err && <span className="rd-warn">{err}</span>}
    </span>
  );
}

/** Add a relation the tree is missing: a person saying the graph should carry an edge it does
 *  not. Recorded as a `missing` edge verdict. */
function MissingRelation({ base, paper, version, source, slugs, who, focusWho, onPosted }: {
  base: string; paper: string; version: number; source: string;
  slugs: { slug: string; plain: string }[]; who: string; focusWho: () => void; onPosted: (rec: Verdict) => void;
}) {
  const [open, setOpen] = useState(false);
  const [relation, setRelation] = useState('supports');
  const [target, setTarget] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');

  const send = async () => {
    if (!who.trim()) { setErr('Add your name in the rail first.'); focusWho(); return; }
    if (!target) { setErr('Choose the claim it should point at.'); return; }
    setBusy(true); setErr('');
    try {
      const rec = await postVerdict(base, paper, version, who, {
        kind: 'edge', source, target, relation, verdict: 'missing', corrected: relation,
      });
      if (rec) onPosted(rec);
      setOpen(false); setTarget('');
    } catch (e: any) {
      setErr(`${e.message} Run npm run dev to record verdicts.`);
    } finally { setBusy(false); }
  };

  if (!open) return <button className="rd-flag" onClick={() => setOpen(true)}>+ Missing relation</button>;
  return (
    <div className="rd-flagbox">
      <p>A relation the graph should carry but does not.</p>
      <div className="rd-vgrid">
        <select className="rd-dsel" value={relation} onChange={e => setRelation(e.target.value)}>
          {REL_VOCAB.map(([k, l]) => <option key={k} value={k}>{l} ({k})</option>)}
        </select>
        <select className="rd-dsel" value={target} onChange={e => setTarget(e.target.value)}>
          <option value="">— target claim —</option>
          {slugs.filter(s => s.slug !== source).map(s => <option key={s.slug} value={s.slug}>{s.slug}</option>)}
        </select>
      </div>
      <div className="rd-flagact">
        <button className="rd-btn" disabled={busy} onClick={send}>Add it</button>
        <button className="rd-btn rd-btn-q" onClick={() => { setOpen(false); setErr(''); }}>Cancel</button>
      </div>
      {err && <p className="rd-warn">{err}</p>}
    </div>
  );
}

/** The three rulings the tree cannot settle claim-by-claim, written out, each with an answer. */
function Rulings({ base, paper, version, questions, standing, who, focusWho, onPosted }: {
  base: string; paper: string; version: number;
  questions: { id: string; question: string }[]; standing: Record<string, Verdict>;
  who: string; focusWho: () => void; onPosted: (rec: Verdict) => void;
}) {
  return (
    <div className="rd-rulings">
      {questions.map(q => (
        <Ruling key={q.id} base={base} paper={paper} version={version} q={q}
          standing={standing[q.id]} who={who} focusWho={focusWho} onPosted={onPosted} />
      ))}
    </div>
  );
}

function Ruling({ base, paper, version, q, standing, who, focusWho, onPosted }: {
  base: string; paper: string; version: number; q: { id: string; question: string };
  standing: Verdict | undefined; who: string; focusWho: () => void; onPosted: (rec: Verdict) => void;
}) {
  const [answer, setAnswer] = useState(standing?.answer ?? '');
  const [why, setWhy] = useState(standing?.why ?? '');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const save = async () => {
    if (!who.trim()) { setErr('Add your name in the rail first.'); focusWho(); return; }
    if (!answer.trim()) { setErr('Answer the question first.'); return; }
    setBusy(true); setErr('');
    try {
      const rec = await postVerdict(base, paper, version, who, {
        kind: 'ruling', question: q.id, answer: answer.trim(), why: why.trim(),
      });
      if (rec) onPosted(rec);
    } catch (e: any) {
      setErr(`${e.message} Run npm run dev to record verdicts.`);
    } finally { setBusy(false); }
  };
  return (
    <div className="rd-ruling">
      <p className="rd-rq">{q.question}</p>
      <input className="rd-dnoteinput" value={answer} placeholder="Your answer"
        onChange={e => setAnswer(e.target.value)} />
      <input className="rd-dnoteinput" value={why} placeholder="Why, if it needs saying"
        onChange={e => setWhy(e.target.value)} />
      <div className="rd-dact">
        <button className="rd-btn" disabled={busy} onClick={save}>{standing?.considered ? 'Update' : 'Record'}</button>
        {standing?.considered && <span className="rd-evstanding">recorded</span>}
      </div>
      {err && <p className="rd-warn">{err}</p>}
    </div>
  );
}

export default function Reader({ data, base }: Props) {
  const C: Record<string, Claim> = useMemo(
    () => Object.fromEntries(data.claims.map((c: Claim) => [c.slug, c])), [data]);
  const FIG: Record<string, any> = useMemo(
    () => Object.fromEntries(data.figures.map((f: any) => [f.id, f])), [data]);

  const [view, setView] = useState<'paper' | 'findings' | 'argument'>('paper');
  // The list shows the coarse grain — wholes — by default; a part is folded under its whole.
  // This reveals the fine grain in place, without opening the reader on it.
  const [showParts, setShowParts] = useState(false);
  const [stack, setStack] = useState<string[]>([]);
  const [near, setNear] = useState<Set<string>>(new Set());
  // The decisions on file at build time, and any made since without a reload.
  const [drafts, setDrafts] = useState<Draft[]>(data.drafts ?? []);
  const [draftUid, setDraftUid] = useState<string | null>(null);
  const [who, setWhoState] = useState('');
  const paperRef = useRef<HTMLDivElement>(null);
  const railRef = useRef<HTMLElement>(null);
  const active = stack.length ? stack[stack.length - 1] : null;
  const D: Record<string, Draft> = useMemo(
    () => Object.fromEntries(drafts.map(d => [d.uid, d])), [drafts]);
  const undecided = drafts.filter(d => !d.decision).length;

  // A card opening into a rail scrolled halfway down the results list starts the reader in
  // the middle of the card they just asked for.
  useEffect(() => { if (railRef.current) railRef.current.scrollTop = 0; }, [active, draftUid]);

  // The name is asked once and remembered, in the same place the old review page kept it.
  useEffect(() => {
    try { setWhoState(localStorage.getItem('reviewer') || ''); } catch { /* private browsing */ }
  }, []);
  const setWho = useCallback((s: string) => {
    setWhoState(s);
    try { localStorage.setItem('reviewer', s.trim()); } catch { /* private browsing */ }
  }, []);

  const decided = useCallback((uid: string, rec: Decision) => {
    setDrafts(ds => ds.map(d => (d.uid === uid ? { ...d, decision: rec } : d)));
  }, []);

  // ── whole-tree adjudication (#82), a dev-only mode over the same rail ────────
  const adjData = data.adjudication;
  const canAdjudicate = import.meta.env.DEV && !!adjData;
  const [adj, setAdj] = useState(false);
  const [verdicts, setVerdicts] = useState<Verdicts>(() => resolveVerdicts(adjData?.records ?? []));
  const slugList = useMemo(
    () => data.claims.map((c: Claim) => ({ slug: c.slug, plain: c.plain })), [data]);
  const focusWho = useCallback(() => document.getElementById('rd-who-rail')?.focus(), []);
  const putClaimVerdict = useCallback((rec: Verdict) =>
    setVerdicts(v => ({ ...v, claims: { ...v.claims, [rec.slug]: rec } })), []);
  const putEdgeVerdict = useCallback((rec: Verdict) =>
    setVerdicts(v => ({ ...v, edges: { ...v.edges, [ekey(rec.source, rec.target, rec.relation)]: rec } })), []);
  const putRulingVerdict = useCallback((rec: Verdict) =>
    setVerdicts(v => ({ ...v, rulings: { ...v.rulings, [rec.question]: rec } })), []);
  const claimsDecided = Object.values(verdicts.claims).filter(v => v.considered).length;
  const edgesDecided = Object.values(verdicts.edges).filter(v => v.considered).length;
  const [finishMsg, setFinishMsg] = useState('');
  const skeleton = useCallback(async () => {
    if (!adjData) return;
    if (!who.trim()) { setFinishMsg('Add your name in the rail first.'); focusWho(); return; }
    try {
      await postReview(base, { file: 'verdicts', op: 'skeleton', paper: data.slug,
        version: adjData.version, by: who.trim(), claims: data.claims.map((c: Claim) => c.slug),
        edges: adjData.edges });
      setFinishMsg('Skeleton written — reload to edit it. Every claim is keep, every edge ok, none considered yet.');
    } catch (e: any) { setFinishMsg(`${e.message} Run npm run dev to write the skeleton.`); }
  }, [adjData, who, base, data, focusWho]);
  const finish = useCallback(async () => {
    if (!adjData) return;
    if (!who.trim()) { setFinishMsg('Add your name in the rail first.'); focusWho(); return; }
    try {
      const body = await postReview(base, { file: 'verdicts', op: 'approve', paper: data.slug,
        version: adjData.version, by: who.trim() });
      setFinishMsg((body as any)?.output?.trim() || 'Recorded the approval.');
    } catch (e: any) { setFinishMsg(`${e.message}`); }
  }, [adjData, who, base, data.slug, focusWho]);

  // ── results, in the order the paper shows them ──────────────────────────────
  const results = useMemo(() => {
    // Wholes only: a part is a component of another claim and is shown folded beneath it, not
    // as a result of its own. The default list is therefore the coarse grain of the tree.
    const rs = data.claims.filter((c: Claim) => RESULT_KINDS.has(c.kind) && !c.partOf);
    const key = (c: Claim): [number, string] =>
      c.panels.length ? [Number(c.panels[0][0]), c.panels[0][1] || 'ZZ'] : [99, 'ZZ'];
    return [...rs].sort((a, b) => {
      const [an, al] = key(a), [bn, bl] = key(b);
      return an - bn || al.localeCompare(bl);
    });
  }, [data]);

  // ── the URL is the state a reader can share ─────────────────────────────────
  useEffect(() => {
    const sp = new URLSearchParams(window.location.search);
    const v = sp.get('view');
    if (v === 'findings' || v === 'argument' || v === 'paper') setView(v);
    // `?view=structure` and `?view=graph` are what the old tabs put in people's bookmarks.
    if (v === 'structure') setView('argument');
    const claim = sp.get('claim');
    if (claim && C[claim]) setStack([claim]);
    const draft = sp.get('draft');
    // Against the drafts the page was built with, not the ones in state: state changes every
    // time a decision is made, and re-running this then would put the reader back wherever the
    // URL last pointed.
    if (draft && (data.drafts ?? []).some((x: Draft) => x.uid === draft)) setDraftUid(draft);
  }, [C, data]);

  const sync = useCallback((v: string, claim: string | null, draft: string | null) => {
    const url = new URL(window.location.href);
    v === 'paper' ? url.searchParams.delete('view') : url.searchParams.set('view', v);
    claim ? url.searchParams.set('claim', claim) : url.searchParams.delete('claim');
    draft ? url.searchParams.set('draft', draft) : url.searchParams.delete('draft');
    window.history.replaceState({}, '', url.toString());
  }, []);

  // One rail, two kinds of card: opening either puts the other away.
  const open = useCallback((slug: string) => {
    if (!C[slug]) return;
    setDraftUid(null);
    setStack(s => (s[s.length - 1] === slug ? s : [...s, slug]));
  }, [C]);
  const openDraftCard = useCallback((uid: string) => {
    setStack([]);
    setDraftUid(uid);
  }, []);
  const back = useCallback(() => { setDraftUid(null); setStack(s => s.slice(0, -1)); }, []);
  const close = useCallback(() => { setDraftUid(null); setStack([]); }, []);

  useEffect(() => { sync(view, active, draftUid); }, [view, active, draftUid, sync]);

  // The graph and any other component on the page open a claim the way they always have.
  useEffect(() => {
    const h = (e: Event) => open((e as CustomEvent<{ slug: string }>).detail.slug);
    window.addEventListener('open-claim', h as EventListener);
    return () => window.removeEventListener('open-claim', h as EventListener);
  }, [open]);

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === 'Escape' && (stack.length || draftUid)) close(); };
    window.addEventListener('keydown', h);
    return () => window.removeEventListener('keydown', h);
  }, [stack.length, draftUid, close]);

  // ── which findings are on screen, so the rail can say where you are ─────────
  useEffect(() => {
    if (view !== 'paper' || !paperRef.current) return;
    const io = new IntersectionObserver(entries => {
      setNear(prev => {
        const next = new Set(prev);
        for (const e of entries) {
          const el = e.target as HTMLElement;
          const slugs = el.dataset.claims
            ? el.dataset.claims.split(',')
            : (FIG[el.dataset.fig ?? '']?.claims ?? []).map((x: any) => x.slug);
          for (const s of slugs) e.isIntersecting ? next.add(s) : next.delete(s);
        }
        return next;
      });
    }, { rootMargin: '-8% 0px -45% 0px' });
    paperRef.current.querySelectorAll('[data-claims], [data-fig]').forEach(el => io.observe(el));
    return () => io.disconnect();
  }, [view, FIG, data]);

  const goFigure = (id: string) => {
    setView('paper');
    requestAnimationFrame(() => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' }));
  };
  const goText = (slug: string) => {
    setView('paper');
    requestAnimationFrame(() => {
      const el = [...document.querySelectorAll<HTMLElement>('[data-claims]')]
        .find(e => (e.dataset.claims ?? '').split(',').includes(slug));
      el?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  };
  const goDraft = (uid: string) => {
    setView('paper');
    requestAnimationFrame(() =>
      document.querySelector(`[data-draft="${uid}"]`)?.scrollIntoView({ behavior: 'smooth', block: 'center' }));
  };

  const src = (s: string) => (s.startsWith('/') ? `${base}${s}` : s);

  // ── the rows that list claims under a figure ────────────────────────────────
  const FigureClaims = ({ f }: { f: any }) => (
    <div className="rd-figclaims">
      <p className="rd-k">What this figure shows</p>
      {f.claims.map((x: any) => {
        const c = C[x.slug];
        return (
          <button key={x.slug} className={`rd-row${active === x.slug ? ' on' : ''}`} onClick={() => open(x.slug)}>
            <span className={`rd-panel${x.letters.length ? '' : ' rd-panel-text'}`}>
              {x.letters.length ? x.letters.join(', ') : 'text'}
            </span>
            <span className="rd-rowtext">{trimDot(c.plain)}</span>
            <Dot c={c} />
          </button>
        );
      })}
    </div>
  );

  const Figure = ({ id }: { id: string }) => {
    const f = FIG[id];
    if (!f) return null;
    return (
      <figure className="rd-fig" id={f.id} data-fig={f.id}>
        <img src={src(f.src)} alt={`${f.label}. ${f.title}`} loading="lazy" />
        <figcaption>
          <span className="rd-figlabel">{f.label}.</span> {f.title}
          {f.caption && (
            <details className="rd-cap">
              <summary>Full caption</summary>
              <div dangerouslySetInnerHTML={{ __html: f.caption }} />
            </details>
          )}
        </figcaption>
        {f.claims.length > 0 && <FigureClaims f={f} />}
      </figure>
    );
  };

  const Table = ({ id }: { id: string }) => {
    const t = data.tables.find((x: any) => x.id === id);
    if (!t) return null;
    return (
      <figure className="rd-tablewrap" id={t.id}>
        <figcaption><span className="rd-figlabel">{t.label}.</span> {t.title}</figcaption>
        <div className="rd-tablescroll">
          <table className="rd-table">
            <tbody>
              {t.rows.map((row: any[], i: number) => (
                <tr key={i}>
                  {row.map((cell, j) => cell.tag === 'th'
                    ? <th key={j} colSpan={Number(cell.colspan) || undefined} dangerouslySetInnerHTML={{ __html: cell.html }} />
                    : <td key={j} colSpan={Number(cell.colspan) || undefined} dangerouslySetInnerHTML={{ __html: cell.html }} />)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </figure>
    );
  };

  const Blocks = ({ blocks }: { blocks: any[] }) => (
    <>
      {blocks.map((b, i) => {
        if (b.type === 'fig') return <Figure key={i} id={b.id} />;
        if (b.type === 'table') return <Table key={i} id={b.id} />;
        if (b.type === 'formula') return <p key={i} className="rd-formula">{b.text}</p>;
        if (b.type === 'sec') return <Section key={i} sec={b.sec} />;
        if (b.sentences) {
          return (
            <p key={i}>
              {b.sentences.map((s: any, j: number) => (
                <span key={j}>
                  {s.claims.length ? (
                    <span
                      className={`rd-mk${s.claims.includes(active) ? ' on' : ''}`}
                      data-claims={s.claims.join(',')}
                      role="button"
                      tabIndex={0}
                      onClick={() => open(pickClaim(s.claims))}
                      onKeyDown={e => { if (e.key === 'Enter') open(pickClaim(s.claims)); }}
                      dangerouslySetInnerHTML={{ __html: linkFigures(s.text) }}
                    />
                  ) : s.draft && D[s.draft] ? (
                    // A claim is asserted and a draft is proposed, so the two marks cannot look
                    // alike: dashed until somebody has decided, and quiet once they have.
                    <span
                      className={`rd-dk${D[s.draft].decision ? ' settled' : ''}${s.draft === draftUid ? ' on' : ''}`}
                      data-draft={s.draft}
                      role="button"
                      tabIndex={0}
                      title={D[s.draft].decision ? 'A claim was proposed here and decided' : 'A claim is proposed here, awaiting a decision'}
                      onClick={() => openDraftCard(s.draft)}
                      onKeyDown={e => { if (e.key === 'Enter') openDraftCard(s.draft); }}
                      dangerouslySetInnerHTML={{ __html: linkFigures(s.text) }}
                    />
                  ) : (
                    <span dangerouslySetInnerHTML={{ __html: linkFigures(s.text) }} />
                  )}{' '}
                </span>
              ))}
            </p>
          );
        }
        return <p key={i} dangerouslySetInnerHTML={{ __html: b.html }} />;
      })}
    </>
  );

  /** One sentence can carry a prediction and the finding that tests it. The finding is what a
   *  reader clicking that sentence is asking about. */
  const pickClaim = (slugs: string[]) =>
    [...slugs].sort((a, b) => Number(RESULT_KINDS.has(C[b]?.kind)) - Number(RESULT_KINDS.has(C[a]?.kind)))[0];

  const Section = ({ sec }: { sec: any }): any => {
    const H = (['h2', 'h2', 'h3', 'h4', 'h5', 'h5'][sec.depth] ?? 'h5') as any;
    return (
      <>
        {sec.title && <H id={sec.id} className={`rd-h${sec.depth}`}>{sec.title}</H>}
        <Blocks blocks={sec.blocks} />
      </>
    );
  };

  // ── views ───────────────────────────────────────────────────────────────────
  const main = data.sections.filter((s: any) => !/methods/.test(s.type));
  const methods = data.sections.filter((s: any) => /methods/.test(s.type));

  const PaperView = () => (
    <div className="rd-paper" ref={paperRef}>
      {data.summary && (
        <section className="rd-brief">
          <div className="rd-briefhead">
            <span className="rd-k rd-k-accent">In brief</span>
            <span className="rd-briefnote">
              {data.counts.claims} claims · {data.counts.rerun} re-run from the authors' data ·
              written by a model, not yet checked by a person
            </span>
          </div>
          <dl>
            {data.summary.hypotheses && <><dt>They asked</dt><dd>{data.summary.hypotheses}</dd></>}
            {data.summary.subject && <><dt>Studied</dt><dd>{data.summary.subject}</dd></>}
            {data.summary.claims && <><dt>They found</dt><dd>{data.summary.claims}</dd></>}
            {data.summary.inferences && <><dt>It means</dt><dd>{data.summary.inferences}</dd></>}
          </dl>
        </section>
      )}

      {data.abstract.length > 0 && (
        <>
          <p className="rd-k">Abstract</p>
          <p>
            {data.abstract.map((s: any, i: number) => (
              <span key={i}>
                {s.claims.length ? (
                  <span
                    className={`rd-mk${s.claims.includes(active) ? ' on' : ''}`}
                    data-claims={s.claims.join(',')}
                    role="button"
                    tabIndex={0}
                    onClick={() => open(pickClaim(s.claims))}
                    onKeyDown={e => { if (e.key === 'Enter') open(pickClaim(s.claims)); }}
                  >{s.text}</span>
                ) : s.text}{' '}
              </span>
            ))}
          </p>
        </>
      )}

      {main.map((s: any, i: number) => <Section key={i} sec={s} />)}

      {methods.length > 0 && (
        <details className="rd-fold">
          <summary>Materials and methods</summary>
          {methods.map((s: any, i: number) => <Section key={i} sec={s} />)}
        </details>
      )}
    </div>
  );

  const FindingsView = () => (
    <div className="rd-digest">
      <h1 className="rd-vtitle">What the paper found, figure by figure</h1>
      <p className="rd-lede">
        Each line is one result the paper claims, with the panel it comes from and whether we could
        reproduce it from the authors' deposited data. Click a line for the detail.
      </p>
      {data.figures.map((f: any) => (
        <div className="rd-dg" key={f.id}>
          <div>
            <button className="rd-thumb" onClick={() => goFigure(f.id)} aria-label={`Go to ${f.label} in the paper`}>
              <img src={src(f.src)} alt={f.label} loading="lazy" />
            </button>
            <p className="rd-dgk"><b>{f.label}</b>{f.title}</p>
          </div>
          <div>
            {f.claims.length === 0
              ? <p className="rd-empty">No result is claimed from this figure.</p>
              : f.claims.map((x: any) => {
                const c = C[x.slug];
                return (
                  <button key={x.slug} className="rd-row rd-row-lg" onClick={() => open(x.slug)}>
                    <span className={`rd-panel${x.letters.length ? '' : ' rd-panel-text'}`}>
                      {x.letters.length ? x.letters.join(', ') : 'text'}
                    </span>
                    <span className="rd-rowtext">{trimDot(c.plain)}</span>
                    <span className={`rd-verdict-inline rd-${c.status}`}>{c.statusLabel}</span>
                  </button>
                );
              })}
          </div>
        </div>
      ))}
    </div>
  );

  const ArgumentView = () => {
    const hyps = data.claims.filter((c: Claim) => c.kind === 'Hypothesis');
    const alts = data.claims.filter((c: Claim) => c.kind === 'Alternative ruled out');
    const caveats = data.claims.filter((c: Claim) => c.kind === 'Caveat');
    const conclusions = data.claims.filter((c: Claim) => c.kind === 'Conclusion');
    const standalone = results.filter((c: Claim) =>
      c.kind === 'Finding' && !c.in.some(r => r.rel === 'tests' || r.rel === 'entails') &&
      !c.out.some(r => r.rel === 'tests'));

    return (
      <div className="rd-arg">
        <h1 className="rd-vtitle">How the argument fits together</h1>
        <p className="rd-lede">
          {hyps.length > 0
            ? `The paper asks ${hyps.length} question${hyps.length === 1 ? '' : 's'}. Each makes a prediction, and each prediction is tested by one or more results.`
            : 'This paper tests no stated hypothesis. Its findings stand on their own, and what they rest on is below.'}
        </p>

        {hyps.map((h: Claim, i: number) => {
          const preds = h.out.filter(r => r.rel === 'entails').map(r => C[r.slug]).filter(Boolean);
          const conf = h.in.filter(r => r.rel === 'confirms' || r.rel === 'validates').map(r => C[r.slug]).filter(Boolean);
          return (
            <section className="rd-hyp" key={h.slug}>
              <p className="rd-k rd-k-accent">Question {i + 1} of {hyps.length}</p>
              <button className="rd-hypq" onClick={() => open(h.slug)}>{trimDot(h.plain)}</button>
              <ul className="rd-chain">
                {preds.map(p => {
                  const tests = p.in.filter(r => r.rel === 'tests').map(r => C[r.slug]).filter(Boolean);
                  return (
                    <li key={p.slug}>
                      <span className="rd-lab">Predicts</span>
                      <div>
                        <button onClick={() => open(p.slug)}>{trimDot(p.plain)}</button>
                        {tests.length > 0 && (
                          <ul className="rd-tests">
                            {tests.map(t => (
                              <li key={t.slug}>
                                <button onClick={() => open(t.slug)}>{trimDot(t.plain)}</button>
                                <span className={`rd-verdict-inline rd-${t.status}`}>{t.statusLabel}</span>
                              </li>
                            ))}
                          </ul>
                        )}
                      </div>
                    </li>
                  );
                })}
                {conf.length > 0 && (
                  <li>
                    <span className="rd-lab">Confirmed by</span>
                    <div>{conf.map(c => (
                      <button key={c.slug} onClick={() => open(c.slug)}>{trimDot(c.plain)}</button>
                    ))}</div>
                  </li>
                )}
              </ul>
            </section>
          );
        })}

        {conclusions.length > 0 && (
          <>
            <h2 className="rd-argh">What the paper concludes</h2>
            {conclusions.map((c: Claim) => (
              <div className="rd-alt" key={c.slug}>
                <button className="rd-a1" onClick={() => open(c.slug)}>{trimDot(c.plain)}</button>
              </div>
            ))}
          </>
        )}

        {alts.length > 0 && (
          <>
            <h2 className="rd-argh">Explanations the paper rules out</h2>
            <p className="rd-sub">
              A result means little until the obvious rival explanations are eliminated. The authors
              named {alts.length}.
            </p>
            {alts.map((a: Claim) => {
              const by = a.in.filter(r => r.rel === 'rules-out').map(r => C[r.slug]).filter(Boolean);
              return (
                <div className="rd-alt" key={a.slug}>
                  <button className="rd-a1" onClick={() => open(a.slug)}><s>{trimDot(a.plain)}</s></button>
                  <div className="rd-a2">
                    {by.length ? <>Ruled out by {by.map((c, i) => (
                      <span key={c.slug}>{i > 0 && ' and '}
                        <button onClick={() => open(c.slug)}>{trimDot(c.plain)}</button>
                      </span>
                    ))}</> : 'Named by the paper, not tested directly'}
                  </div>
                </div>
              );
            })}
          </>
        )}

        {standalone.length > 0 && (
          <>
            <h2 className="rd-argh">Findings that stand on their own</h2>
            <p className="rd-sub">Results no stated prediction called for.</p>
            {standalone.map((c: Claim) => (
              <div className="rd-alt" key={c.slug}>
                <button className="rd-a1" onClick={() => open(c.slug)}>{trimDot(c.plain)}</button>
              </div>
            ))}
          </>
        )}

        {caveats.length > 0 && (
          <>
            <h2 className="rd-argh">What every result assumes</h2>
            <p className="rd-sub">These qualify all of the findings above.</p>
            {caveats.map((c: Claim) => (
              <div className="rd-alt" key={c.slug}>
                <button className="rd-a1" onClick={() => open(c.slug)}>{trimDot(c.plain)}</button>
              </div>
            ))}
          </>
        )}

        <p className="rd-more">
          This is the plain reading of the claim graph. The graph itself, with all fourteen relation
          types and every claim's record, is under <a href="#record">About this record</a>.
        </p>
      </div>
    );
  };

  // ── the rail: the list at rest, the card when one is open ───────────────────
  const RailList = () => {
    const groups = new Map<string, Claim[]>();
    for (const c of results) {
      const k = c.panels.length ? `Figure ${c.panels[0][0]}` : 'In the text';
      if (!groups.has(k)) groups.set(k, []);
      groups.get(k)!.push(c);
    }
    const partCount = data.claims.filter((c: Claim) => c.partOf).length;
    return (
      <div className="rd-rest">
        <p className="rd-k rd-k-accent rd-railk">
          What this paper shows <span>{results.length} results</span>
        </p>
        <p className="rd-railnote">
          {data.counts.marked > 0
            ? 'Underlined sentences and figure panels carry a claim. Click one, or a line below.'
            : 'Figure panels carry a claim. Click one, or a line below.'}
        </p>
        {partCount > 0 && (
          // The list shows wholes; a whole's components fold beneath it on request. A part is
          // one comparison, condition or measure of a claim already listed — the fine grain.
          <button className="rd-partstoggle" aria-pressed={showParts}
                  onClick={() => setShowParts(s => !s)}>
            {showParts ? 'Hide' : 'Show'} the {partCount} part{partCount === 1 ? '' : 's'} folded beneath
          </button>
        )}
        {[...groups].map(([k, cs]) => (
          <div className="rd-rg" key={k}>
            <div className="rd-rgk">{k}</div>
            {cs.map(c => (
              <div key={c.slug} className="rd-rgroup">
                <button
                  className={`rd-rrow${near.has(c.slug) && view === 'paper' ? ' near' : ''}`}
                  onClick={() => open(c.slug)}
                >
                  <Dot c={c} />
                  <span className="rd-rt">{trimDot(c.plain)}</span>
                </button>
                {showParts && c.parts.map(p => C[p]).filter(Boolean).map(p => (
                  <button
                    key={p.slug}
                    className={`rd-rrow rd-rpart${near.has(p.slug) && view === 'paper' ? ' near' : ''}`}
                    onClick={() => open(p.slug)}
                  >
                    <Dot c={p} />
                    <span className="rd-rt">{trimDot(p.plain)}</span>
                  </button>
                ))}
              </div>
            ))}
          </div>
        ))}
        {drafts.length > 0 && (
          <div className="rd-drafts">
            <p className="rd-k rd-k-draft rd-railk">
              Proposed claims <span>{undecided} of {drafts.length} undecided</span>
            </p>
            <p className="rd-railnote">
              Drafted for results no claim covers. None of them is in the corpus until you say so.
            </p>
            {drafts.map(d => (
              <button key={d.uid} className={`rd-drow${d.decision ? ' settled' : ''}`}
                onClick={() => openDraftCard(d.uid)}>
                <span className="rd-dmark" aria-hidden="true" />
                <span className="rd-rt">{trimDot(d.decision?.claim || d.claim)}</span>
                {d.decision && <span className="rd-settled">{DECIDED[d.decision.decision] ?? d.decision.decision}</span>}
              </button>
            ))}
          </div>
        )}
        {data.counts.gaps > 0 && (
          <p className="rd-gaps">
            {data.counts.gaps} results in the text carry no claim yet —
            <a href={`${base}/papers/${data.slug}/coverage/`}> see coverage</a>.
          </p>
        )}
      </div>
    );
  };

  const Card = ({ c }: { c: Claim }) => {
    const fig = c.panels.length ? `fig${c.panels[0][0]}` : null;
    const letters = fig ? c.panels.filter(p => p[0] === c.panels[0][0]).map(p => p[1]).filter(Boolean) : [];
    const inText = data.counts.marked > 0 &&
      typeof document !== 'undefined' &&
      [...document.querySelectorAll<HTMLElement>('[data-claims]')]
        .some(e => (e.dataset.claims ?? '').split(',').includes(c.slug));

    // The relation name travels with the label: the label is what a reader is shown, and the
    // name is what a flag has to say was wrong, because `Relies on` is not what the graph
    // calls it.
    const seen = new Set<string>();
    const groups = new Map<string, { rel: string; claims: Claim[] }>();
    for (const r of [...c.out, ...c.in].sort((a, b) => REL_ORDER.indexOf(a.label) - REL_ORDER.indexOf(b.label))) {
      const t = C[r.slug];
      if (!t || seen.has(r.slug)) continue;
      seen.add(r.slug);
      if (!groups.has(r.label)) groups.set(r.label, { rel: r.rel, claims: [] });
      groups.get(r.label)!.claims.push(t);
    }

    const k = c.check ?? {};
    const lead =
      c.status === 'matches' ? `We re-ran this from ${k.how ?? "the authors' deposited data"}${k.date ? ` on ${k.date}` : ''} and got the same result.`
      : c.status === 'partly' ? `We re-ran this from ${k.how ?? "the authors' deposited data"}${k.date ? ` on ${k.date}` : ''}. The direction reproduces; the numbers differ.`
      : c.status === 'differs' ? 'We re-ran this and got a different result.'
      : c.status === 'blocked' ? (k.how === 'reading the Methods section'
          ? 'There is nothing to re-run. It was confirmed by reading the Methods section.'
          : 'We could not re-run this: the analysis needs software or data we do not have.')
      : 'We have not tried to re-run this yet.';

    return (
      <div className="rd-card">
        <div className="rd-cardnav">
          <button onClick={back}>← {stack.length > 1 ? 'Back' : 'All results'}</button>
          <button onClick={close}>Close</button>
        </div>
        <p className="rd-kind">
          {c.kind}
          {c.status !== 'na' && <span className={`rd-verdict-inline rd-${c.status}`}>{c.statusLabel}</span>}
        </p>
        <p className="rd-cshort">{c.plain}</p>
        {c.hasPlain && c.full && <p className="rd-cwords">{c.full}</p>}

        {(fig || inText) && (
          <p className="rd-cwhere">
            <span>Where:</span>
            {fig && FIG[fig] && (
              <button onClick={() => goFigure(fig)}>
                {FIG[fig].label}{letters.length ? ` ${letters.join(', ')}` : ''}
              </button>
            )}
            {inText && <button onClick={() => goText(c.slug)}>In the text</button>}
          </p>
        )}

        {adj && adjData && (
          <ClaimVerdict key={`v-${c.slug}`} base={base} paper={data.slug} version={adjData.version}
            claim={c} roles={adjData.roles} slugs={slugList} who={who} focusWho={focusWho}
            standing={verdicts.claims[c.slug]} onPosted={putClaimVerdict} />
        )}

        {c.status !== 'na' && (
          <div className="rd-blk">
            <p className="rd-k">Does it hold up?</p>
            <span className={`rd-verdict rd-${c.status}`}>{c.statusLabel}</span>
            <p>{lead}</p>
            {(k.paper || k.reproduced) && (
              <dl className="rd-cmp">
                <dt>Paper says</dt><dd>{k.paper ?? '—'}</dd>
                <dt>Our re-run</dt><dd>{k.reproduced ?? '—'}</dd>
                {c.dataset && (
                  <><dt>Data</dt><dd>{/^https?:/.test(c.dataset)
                    ? <a href={c.dataset} target="_blank" rel="noopener">{c.dataset}</a>
                    : c.dataset}</dd></>
                )}
              </dl>
            )}
            {/* The check itself. A verdict a reader cannot audit is one they have to take on
                trust; where a script was written, this is the script. Folded, because it is
                the deepest thing on the card and not what most readers came for. */}
            {c.scriptSource && (
              <details className="rd-script">
                <summary>The check we ran{c.script && <code>{c.script}</code>}</summary>
                <pre>{c.scriptSource}</pre>
              </details>
            )}
          </div>
        )}

        {c.method && (
          <div className="rd-blk">
            <p className="rd-k">How it was measured</p>
            <p>{c.method}</p>
          </div>
        )}

        {(groups.size > 0 || (adj && adjData)) && (
          <div className="rd-blk">
            <p className="rd-k">How it connects</p>
            <ul className="rd-rel">
              {[...groups].map(([label, g]) => (
                <li key={label}>
                  <span className="rd-rl">{label}</span>
                  <div>{g.claims.map(t => (
                    <div className="rd-relrow" key={t.slug}>
                      <button onClick={() => open(t.slug)}>{trimDot(t.plain)}<Dot c={t} /></button>
                      {adj && adjData
                        ? <EdgeVerdict key={`ev-${c.slug}-${t.slug}-${g.rel}`} base={base}
                            paper={data.slug} version={adjData.version} source={c.slug} target={t.slug}
                            relation={g.rel} label={label} who={who} focusWho={focusWho}
                            standing={verdicts.edges[ekey(c.slug, t.slug, g.rel)]} onPosted={putEdgeVerdict} />
                        : <EdgeFlag base={base} paper={data.slug} claim={c.slug}
                            rel={g.rel} label={label} target={t.slug} who={who} />}
                    </div>
                  ))}</div>
                </li>
              ))}
            </ul>
            {adj && adjData ? (
              <>
                <MissingRelation base={base} paper={data.slug} version={adjData.version}
                  source={c.slug} slugs={slugList} who={who} focusWho={focusWho} onPosted={putEdgeVerdict} />
                <p className="rd-dnote">
                  Mark each relation ok or wrong, and add one the graph is missing. A verdict is a
                  record; `apply` is what rewrites the graph, and that is the maintainer's call.
                </p>
              </>
            ) : groups.size > 0 && (
              <p className="rd-dnote">
                These relations were inferred, not written by the authors. Flagging one records that
                a person disputes it; it does not change the graph.
              </p>
            )}
          </div>
        )}

        {c.parts.length > 0 && (
          <div className="rd-blk">
            <p className="rd-k">Its parts</p>
            <p className="rd-railnote">Components of this claim — one comparison, condition or measure each.</p>
            <ul className="rd-rel">
              {c.parts.map(p => C[p]).filter(Boolean).map(p => (
                <li key={p.slug}>
                  <div><button onClick={() => open(p.slug)}>{trimDot(p.plain)}<Dot c={p} /></button></div>
                </li>
              ))}
            </ul>
          </div>
        )}
        {c.partOf && C[c.partOf] && (
          <div className="rd-blk">
            <p className="rd-k">Part of</p>
            <div><button className="rd-relback" onClick={() => open(c.partOf!)}>{trimDot(C[c.partOf].plain)}<Dot c={C[c.partOf]} /></button></div>
          </div>
        )}

        <div className="rd-cfoot">
          <span>Extracted by a language model, not yet checked by a person</span>
          <a href={`${base}/papers/${data.slug}/plain-claim/`}>The record ↗</a>
        </div>
      </div>
    );
  };

  return (
    <div className="rd">
      <nav className="rd-modes" aria-label="How to read this paper">
        {(['paper', 'findings', 'argument'] as const).map(v => (
          <button key={v} className="rd-mode" aria-pressed={view === v} onClick={() => setView(v)}>
            {v === 'paper' ? 'Paper' : v === 'findings' ? 'Findings' : 'Argument'}
          </button>
        ))}
        {/* Dev-only, like #78's write path: adjudicating a whole tree needs the endpoint that
            only `astro dev` serves. On the published site the button is not shown at all. */}
        {canAdjudicate && (
          <button className="rd-mode rd-mode-adj" aria-pressed={adj} onClick={() => setAdj(a => !a)}
            title="Record a verdict on every claim and edge (needs the dev server)">
            {adj ? 'Adjudicating' : 'Adjudicate'}
          </button>
        )}
      </nav>

      <div className="rd-grid">
        <div className="rd-col">
          {view === 'paper' && <PaperView />}
          {view === 'findings' && <FindingsView />}
          {view === 'argument' && <ArgumentView />}
        </div>
        <aside ref={railRef} className={`rd-rail${active || draftUid || adj ? ' open' : ''}`} aria-live="polite">
          {adj && adjData && (
            <div className="rd-adjbar">
              <p className="rd-k rd-k-adj">
                Adjudicating claim-tree v{adjData.version}
                <span>{claimsDecided}/{adjData.claimCount} claims · {edgesDecided}/{adjData.edgeCount} edges</span>
              </p>
              <p className="rd-railnote">
                Open a claim to record its verdict; every relation on the card carries one too.
                Nothing is in the corpus until you mark the reading finished. Verdicts land in
                <code> runs/{data.slug}/claim-tree.v{adjData.version}.verdicts.jsonl</code>.
              </p>
              <div className="rd-dact">
                {Object.keys(verdicts.claims).length === 0 && (
                  <button className="rd-btn" onClick={skeleton}>Generate skeleton</button>
                )}
                <button className="rd-btn rd-btn-go" onClick={finish}>Mark reading finished</button>
              </div>
              {finishMsg && <pre className="rd-adjmsg">{finishMsg}</pre>}
              <details className="rd-rulingswrap">
                <summary>The three rulings the tree cannot settle claim-by-claim</summary>
                <Rulings base={base} paper={data.slug} version={adjData.version}
                  questions={adjData.rulings} standing={verdicts.rulings}
                  who={who} focusWho={focusWho} onPosted={putRulingVerdict} />
              </details>
            </div>
          )}
          {draftUid && D[draftUid]
            ? <DraftCard
                key={draftUid} d={D[draftUid]} paper={data.slug} base={base}
                roles={data.draftRoles ?? []} who={who} setWho={setWho}
                onDecided={decided} onBack={back} onClose={close} onShow={goDraft} />
            // Called, not mounted: both are declared in this render body, so as elements they
            // would be a new component type on every render and React would rebuild the rail
            // from scratch — taking with it whatever an `EdgeFlag` had half-typed in it.
            : active ? Card({ c: C[active] }) : RailList()}
          {/* Outside the two cards, because both of them are rebuilt on every render of this
              component and an input inside a rebuilt subtree loses focus as you type it. */}
          {(drafts.length > 0 || adj) && !draftUid && <Who id="rd-who-rail" who={who} setWho={setWho} />}
        </aside>
      </div>

      <style>{`
        .rd { --rd-gap: 3.5rem; }
        /* :where() contributes no specificity, so every component rule below wins the font it
           sets. Written as .rd button, this reset beat .rd-row and the figure's claim list
           inherited the paper's serif — the one place the two voices must not merge. */
        .rd :where(button) { font: inherit; color: inherit; background: none; border: 0; padding: 0; cursor: pointer; text-align: left; }
        .rd button:focus-visible, .rd [tabindex]:focus-visible, .rd a:focus-visible {
          outline: 2px solid var(--claim); outline-offset: 2px; border-radius: 2px;
        }
        .rd-k {
          font-size: 11.5px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase;
          color: var(--card-muted); margin: 0 0 0.5rem;
        }
        .rd-k-accent { color: var(--claim); }

        /* ── the three depths ─────────────────────────────────────────── */
        .rd-modes { display: flex; gap: 1.75rem; border-bottom: 1px solid var(--card-border); margin-bottom: 0.5rem; }
        .rd-mode {
          padding: 0.55rem 0 0.75rem; font-size: 11.5px; font-weight: 600; letter-spacing: 0.11em;
          text-transform: uppercase; color: var(--card-border-hover);
          border-bottom: 2px solid transparent; margin-bottom: -1px; transition: color 0.12s, border-color 0.12s;
        }
        .rd-mode:hover { color: var(--card-strong); }
        .rd-mode[aria-pressed='true'] { color: var(--claim); border-bottom-color: var(--claim); }

        .rd-grid { display: grid; grid-template-columns: minmax(0, 1fr) 19.5rem; gap: 0 var(--rd-gap); align-items: start; }
        .rd-col { min-width: 0; }

        /* ── the paper ────────────────────────────────────────────────── */
        .rd-paper { font-family: var(--paper-serif); font-size: 17px; line-height: 1.62; color: var(--card-body); max-width: 68ch; }
        .rd-paper p { margin: 0 0 1.05em; }
        .rd-paper sup, .rd-paper sub { font-size: 0.72em; line-height: 0; }
        .rd-paper i { font-style: italic; }
        .rd-paper .cite, .rd-paper .rd-xref, .rd-paper .xref { color: var(--card-muted); }
        .rd-paper .xref, .rd-paper .rd-xref { text-decoration: none; border-bottom: 1px solid var(--card-border); }
        .rd-paper .xref:hover, .rd-paper .rd-xref:hover { color: var(--card-head); border-color: var(--card-border-hover); }
        .rd-paper .math { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; }
        .rd-formula { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.84em; color: var(--card-muted); overflow-x: auto; }

        .rd-brief, .rd-k, .rd-lede, .rd-railnote { font-family: Inter, system-ui, sans-serif; }
        .rd-brief {
          font-size: 14.5px; line-height: 1.55; border-top: 1px solid var(--card-border-hover);
          border-bottom: 1px solid var(--card-border); padding: 1.35rem 0 0.6rem; margin: 0.75rem 0 2.25rem;
        }
        .rd-briefhead { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: baseline; gap: 0.5rem 1rem; }
        .rd-briefnote { font-size: 12px; color: var(--card-muted); }
        .rd-brief dl { margin: 0; display: grid; grid-template-columns: 7em 1fr; gap: 0 1.1rem; }
        .rd-brief dt { color: var(--card-muted); font-size: 12.5px; font-weight: 500; padding-top: 2px; }
        .rd-brief dd { margin: 0 0 0.75rem; color: var(--card-body); }

        .rd-h1, .rd-paper h2 { font-size: 22px; font-weight: 600; color: var(--card-head); margin: 2.6rem 0 0.8rem; letter-spacing: -0.01em; }
        .rd-h2 { font-family: Inter, system-ui, sans-serif; font-size: 12px; font-weight: 600; letter-spacing: 0.13em; text-transform: uppercase; color: var(--card-muted); margin: 2rem 0 0.6rem; }
        .rd-h3 { font-size: 17.5px; font-weight: 600; color: var(--card-head); margin: 1.6rem 0 0.5rem; }
        .rd-h4, .rd-h5 { font-size: 16.5px; font-weight: 600; font-style: italic; color: var(--card-strong); margin: 1.2rem 0 0.4rem; }

        .rd-fold { margin-top: 2.5rem; border-top: 1px solid var(--card-border); padding-top: 0.5rem; }
        .rd-fold > summary, .rd-cap > summary {
          list-style: none; cursor: pointer; font-family: Inter, system-ui, sans-serif;
          font-size: 13px; color: var(--card-muted); padding: 0.4rem 0;
        }
        .rd-fold > summary::-webkit-details-marker, .rd-cap > summary::-webkit-details-marker { display: none; }
        .rd-fold > summary::before, .rd-cap > summary::before {
          content: ''; display: inline-block; width: 6px; height: 6px; margin-right: 0.5rem;
          border-right: 1.5px solid currentColor; border-bottom: 1.5px solid currentColor;
          transform: rotate(-45deg); transition: transform 0.15s;
        }
        .rd-fold[open] > summary::before, .rd-cap[open] > summary::before { transform: rotate(45deg); }
        .rd-fold > summary:hover, .rd-cap > summary:hover { color: var(--card-head); }

        /* a sentence that carries a claim */
        .rd-mk {
          text-decoration: underline; text-decoration-color: var(--claim-line);
          text-decoration-thickness: 1.5px; text-underline-offset: 4px;
          cursor: pointer; border-radius: 2px; transition: background 0.12s;
        }
        .rd-mk:hover { background: var(--claim-wash); }
        .rd-mk.on { background: var(--claim-wash-2); text-decoration-color: var(--claim); }

        /* a sentence somebody has proposed a claim for — dashed, because it is a proposal */
        .rd-dk {
          text-decoration: underline; text-decoration-style: dashed;
          text-decoration-color: var(--draft-line); text-decoration-thickness: 1.5px;
          text-underline-offset: 4px; cursor: pointer; border-radius: 2px; transition: background 0.12s;
        }
        .rd-dk:hover { background: var(--draft-wash); }
        .rd-dk.on { background: var(--draft-wash-2); text-decoration-color: var(--draft); }
        /* decided: the question is closed, so the sentence stops asking it */
        .rd-dk.settled { text-decoration-style: dotted; text-decoration-color: var(--card-border-hover); }
        .rd-dk.settled:hover { background: var(--card-sunk); }

        /* ── figures ──────────────────────────────────────────────────── */
        .rd-fig { margin: 1.9rem 0 2.1rem; scroll-margin-top: 4.5rem; }
        .rd-fig img { display: block; width: 100%; height: auto; border: 1px solid var(--card-border); background: #fff; }
        .rd-fig figcaption, .rd-tablewrap figcaption {
          font-family: Inter, system-ui, sans-serif; font-size: 13.5px; line-height: 1.5;
          color: var(--card-muted); margin-top: 0.7rem;
        }
        .rd-figlabel { font-weight: 600; color: var(--card-head); }
        .rd-cap { margin-top: 0.35rem; }
        .rd-cap p { margin: 0 0 0.5rem; }

        .rd-figclaims { margin-top: 0.9rem; border-top: 1px solid var(--card-border); }
        .rd-figclaims .rd-k { color: var(--claim); padding-top: 0.7rem; }
        .rd-row {
          display: grid; grid-template-columns: 3.2em 1fr auto; gap: 0 0.8rem; align-items: baseline;
          width: 100%; padding: 0.45rem 0; border-bottom: 1px solid var(--card-border);
          font-family: Inter, system-ui, sans-serif; font-size: 14px; line-height: 1.4; color: var(--card-body);
        }
        .rd-row:last-child { border-bottom: 0; }
        .rd-row:hover .rd-rowtext, .rd-row.on .rd-rowtext { color: var(--claim-strong); }
        .rd-row.on { background: var(--claim-wash); }
        .rd-row-lg { font-size: 14.5px; grid-template-columns: 3.2em 1fr auto; }
        .rd-panel {
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11.5px;
          letter-spacing: 0.04em; color: var(--card-muted);
        }
        .rd-panel-text { font-family: Inter, system-ui, sans-serif; font-style: italic; font-size: 12px; letter-spacing: 0; }

        /* ── tables ───────────────────────────────────────────────────── */
        .rd-tablewrap { margin: 1.9rem 0; }
        .rd-tablescroll { overflow-x: auto; border: 1px solid var(--card-border); margin-top: 0.6rem; }
        .rd-table { border-collapse: collapse; width: 100%; font-family: Inter, system-ui, sans-serif; font-size: 12.5px; }
        .rd-table th, .rd-table td { padding: 0.4rem 0.6rem; border-bottom: 1px solid var(--card-border); text-align: left; white-space: nowrap; }
        .rd-table th { font-weight: 600; color: var(--card-head); background: var(--card-sunk); }
        .rd-table td { color: var(--card-body); font-variant-numeric: tabular-nums; }

        /* ── the outcome of a re-run, and nothing else ────────────────── */
        .rd-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: var(--ran-none); flex: none; }
        .rd-dot.rd-matches { background: var(--ran-ok); }
        .rd-dot.rd-partly { background: var(--ran-part); }
        .rd-dot.rd-differs { background: var(--ran-differs); }
        .rd-dot.rd-blocked, .rd-dot.rd-none { background: transparent; border: 1.5px solid var(--ran-none); }
        .rd-verdict, .rd-verdict-inline { font-family: Inter, system-ui, sans-serif; white-space: nowrap; }
        .rd-verdict-inline { font-size: 12px; color: var(--card-muted); }
        .rd-verdict-inline.rd-matches { color: var(--ran-ok); }
        .rd-verdict-inline.rd-partly { color: var(--ran-part); }
        .rd-verdict-inline.rd-differs { color: var(--ran-differs); }
        .rd-verdict { display: inline-block; font-size: 12.5px; font-weight: 600; padding: 2px 8px; border-radius: 3px; margin-bottom: 0.5rem; }
        .rd-verdict.rd-matches { background: var(--ran-ok-bg); color: var(--ran-ok); }
        .rd-verdict.rd-partly { background: var(--ran-part-bg); color: var(--ran-part); }
        .rd-verdict.rd-differs { background: var(--ran-differs-bg); color: var(--ran-differs); }
        .rd-verdict.rd-blocked, .rd-verdict.rd-none { background: var(--ran-none-bg); color: var(--card-body); }

        /* ── findings ─────────────────────────────────────────────────── */
        .rd-digest, .rd-arg { padding-top: 2.25rem; max-width: 68ch; font-family: Inter, system-ui, sans-serif; }
        .rd-vtitle { font-family: var(--paper-serif); font-size: 28px; font-weight: 600; letter-spacing: -0.012em; margin: 0 0 0.4rem; color: var(--card-head); line-height: 1.15; text-wrap: balance; }
        .rd-lede { color: var(--card-body); font-size: 15px; max-width: 60ch; margin: 0 0 2rem; line-height: 1.55; }
        .rd-dg { display: grid; grid-template-columns: 9.5rem 1fr; gap: 0 1.6rem; padding: 1.3rem 0; border-top: 1px solid var(--card-border); }
        .rd-dg:last-of-type { border-bottom: 1px solid var(--card-border); }
        .rd-thumb { display: block; width: 100%; }
        .rd-thumb img { width: 100%; height: auto; display: block; border: 1px solid var(--card-border); background: #fff; }
        .rd-thumb:hover img { border-color: var(--claim); }
        .rd-dgk { font-size: 11.5px; color: var(--card-muted); margin: 0.5rem 0 0; line-height: 1.4; }
        .rd-dgk b { display: block; color: var(--card-head); font-size: 12.5px; font-weight: 600; }
        .rd-empty { font-size: 13.5px; color: var(--card-muted); font-style: italic; margin: 0.4rem 0; }

        /* ── argument ─────────────────────────────────────────────────── */
        .rd-hyp { border-top: 2px solid var(--card-head); padding: 1.1rem 0 1.3rem; }
        .rd-hypq { font-family: var(--paper-serif); font-size: 19px; font-weight: 600; line-height: 1.35; color: var(--card-head); margin: 0 0 0.8rem; display: block; text-wrap: pretty; }
        .rd-hypq:hover { color: var(--claim-strong); }
        .rd-chain { margin: 0; padding: 0; list-style: none; }
        .rd-chain > li { display: grid; grid-template-columns: 8em 1fr; gap: 0 0.9rem; padding: 0.55rem 0; border-top: 1px solid var(--card-border); font-size: 14.5px; line-height: 1.45; }
        .rd-lab { font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--card-muted); font-weight: 600; padding-top: 3px; }
        .rd-chain button { color: var(--card-body); display: block; width: 100%; padding: 0.1rem 0; }
        .rd-chain button:hover { color: var(--claim-strong); }
        .rd-tests { margin: 0.35rem 0 0; padding: 0; list-style: none; }
        .rd-tests li { display: flex; gap: 0.6rem; align-items: baseline; padding: 0.25rem 0; }
        .rd-tests li::before { content: '↳'; color: var(--card-muted); flex: none; }
        .rd-tests button { flex: 1; }
        .rd-argh { font-family: var(--paper-serif); font-size: 21px; font-weight: 600; color: var(--card-head); margin: 2.6rem 0 0.3rem; }
        .rd-sub { color: var(--card-body); font-size: 14px; margin: 0 0 0.8rem; max-width: 60ch; }
        .rd-alt { border-top: 1px solid var(--card-border); padding: 0.7rem 0; }
        .rd-a1 { color: var(--card-body); font-size: 14.5px; line-height: 1.45; display: block; width: 100%; }
        .rd-a1:hover { color: var(--card-head); }
        .rd-a1 s { text-decoration-color: var(--card-muted); }
        .rd-a2 { margin-top: 0.3rem; font-size: 13px; color: var(--card-muted); }
        .rd-a2 button { color: var(--claim-strong); border-bottom: 1px solid var(--claim-line); }
        .rd-more { margin-top: 2.5rem; border-top: 1px solid var(--card-border); padding-top: 0.9rem; font-size: 13px; color: var(--card-muted); }
        .rd-more a { color: var(--claim-strong); }

        /* ── rail ─────────────────────────────────────────────────────── */
        .rd-rail {
          position: sticky; top: 3.5rem; max-height: calc(100vh - 4rem); overflow: auto;
          padding: 2.25rem 0 2.5rem; font-family: Inter, system-ui, sans-serif;
          scrollbar-width: thin;
        }
        .rd-railk { display: flex; justify-content: space-between; align-items: baseline; }
        .rd-railk span { color: var(--card-muted); font-weight: 500; letter-spacing: 0; text-transform: none; font-size: 12px; }
        .rd-railnote { color: var(--card-muted); font-size: 12.5px; line-height: 1.45; margin: 0 0 1rem; }
        .rd-rg { margin-top: 0.9rem; }
        .rd-rgk { font-size: 11.5px; color: var(--card-muted); font-weight: 500; padding-bottom: 0.25rem; border-bottom: 1px solid var(--card-border); }
        .rd-rrow { display: grid; grid-template-columns: 8px 1fr; gap: 0 0.6rem; align-items: baseline; width: 100%; padding: 0.4rem 0.35rem 0.4rem 0; border-radius: 3px; color: var(--card-body); font-size: 13px; line-height: 1.4; }
        .rd-rrow:hover { color: var(--card-head); background: var(--claim-wash); }
        .rd-rrow.near { color: var(--card-head); box-shadow: inset 2px 0 0 var(--claim); padding-left: 0.5rem; }
        .rd-rrow .rd-dot { position: relative; top: -1px; }
        /* The text is placed, not flowed. Dot renders nothing for a claim a re-run cannot
           settle — a hypothesis, a prediction, a scope, and now every part — so that row has
           one child, and a single child in a two-track grid lands in the first track: the 8px
           one meant for the dot. The sentence then wrapped one word per line down a 288px
           column of empty space. It showed up the moment the parts retrofit put ten dotless
           claims in Gädeke's lane. */
        .rd-rrow .rd-rt { grid-column: 2; }
        /* A part folds beneath its whole: indented, quieter, and joined by a left rule so the
           two grains read as one claim and its components rather than two peers. */
        .rd-rgroup { display: contents; }
        .rd-rpart { padding-left: 1rem; margin-left: 0.4rem; border-left: 1px solid var(--card-border); font-size: 12.5px; color: var(--card-muted); }
        .rd-rpart:hover { color: var(--card-head); }
        .rd-partstoggle { font-size: 12px; color: var(--claim-strong); margin: 0 0 0.4rem; text-decoration: underline; text-underline-offset: 2px; }
        .rd-partstoggle:hover { color: var(--card-head); }
        .rd-gaps { font-size: 12px; color: var(--card-muted); margin-top: 1.2rem; border-top: 1px solid var(--card-border); padding-top: 0.6rem; }
        .rd-gaps a { color: var(--claim-strong); }

        /* ── the claim card ───────────────────────────────────────────── */
        .rd-card { animation: rd-in 0.16s ease-out; }
        @keyframes rd-in { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }
        @media (prefers-reduced-motion: reduce) { .rd-card { animation: none; } .rd * { transition: none !important; } }
        .rd-cardnav { display: flex; justify-content: space-between; font-size: 12.5px; color: var(--card-muted); margin-bottom: 0.9rem; }
        .rd-cardnav button:hover { color: var(--card-head); }
        .rd-kind { display: flex; align-items: baseline; gap: 0.6rem; font-size: 11.5px; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 600; color: var(--claim); margin: 0 0 0.6rem; }
        .rd-kind .rd-verdict-inline { letter-spacing: 0; text-transform: none; font-weight: 500; }
        .rd-cshort { font-family: var(--paper-serif); font-size: 17.5px; line-height: 1.4; font-weight: 600; color: var(--card-head); margin: 0 0 0.9rem; text-wrap: pretty; }
        .rd-cwords { font-family: var(--paper-serif); font-size: 13.5px; line-height: 1.5; color: var(--card-body); margin: 0 0 1rem; padding-left: 0.7rem; border-left: 2px solid var(--card-border); }
        .rd-cwhere { display: flex; flex-wrap: wrap; gap: 0.3rem 0.9rem; font-size: 13px; color: var(--card-muted); margin: 0 0 1rem; }
        .rd-cwhere button { color: var(--claim-strong); font-weight: 500; border-bottom: 1px solid var(--claim-line); }
        .rd-blk { border-top: 1px solid var(--card-border); padding: 0.75rem 0; }
        .rd-blk p { margin: 0 0 0.35rem; color: var(--card-body); font-size: 13px; line-height: 1.5; }
        .rd-blk p:last-child { margin-bottom: 0; }
        .rd-cmp { display: grid; grid-template-columns: 6em 1fr; gap: 0.15rem 0.7rem; font-size: 12.5px; margin: 0.4rem 0 0; }
        .rd-cmp dt { color: var(--card-muted); }
        .rd-cmp dd { margin: 0; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11.5px; color: var(--card-head); overflow-wrap: anywhere; }
        .rd-cmp dd a { color: var(--claim-strong); border-bottom: 1px solid var(--claim-line); }
        /* The verification script, folded. The deepest thing on a claim card and the only
           part of it a reader can check for themselves. */
        .rd-script { margin: 0.6rem 0 0; }
        .rd-script > summary {
          list-style: none; cursor: pointer; font-size: 12px; color: var(--card-muted);
          display: flex; align-items: baseline; gap: 0.45rem;
        }
        .rd-script > summary::-webkit-details-marker { display: none; }
        .rd-script > summary::before {
          content: ''; width: 5px; height: 5px; flex: none; transform: rotate(-45deg);
          border-right: 1.5px solid var(--card-faint); border-bottom: 1.5px solid var(--card-faint);
          transition: transform 0.15s;
        }
        .rd-script[open] > summary::before { transform: rotate(45deg); }
        .rd-script > summary:hover { color: var(--claim-strong); }
        .rd-script > summary code { font-size: 11px; color: var(--card-faint); }
        .rd-script pre {
          margin: 0.5rem 0 0; padding: 0.7rem 0.8rem; background: var(--card-sunk);
          border: 1px solid var(--card-border); border-radius: 5px;
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px;
          line-height: 1.6; color: var(--card-body); overflow-x: auto; white-space: pre;
          max-height: 22rem; overflow-y: auto;
        }
        .rd-rel { margin: 0.3rem 0 0; padding: 0; list-style: none; }
        .rd-rel li { display: grid; grid-template-columns: 7.5em 1fr; gap: 0 0.6rem; align-items: baseline; padding: 0.4rem 0; border-top: 1px solid var(--card-border); font-size: 13px; line-height: 1.4; }
        .rd-rel li:first-child { border-top: 0; }
        .rd-rl { font-size: 10.5px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--card-muted); font-weight: 600; padding-top: 2px; }
        .rd-rel button { color: var(--card-body); display: block; padding: 0.1rem 0; }
        .rd-rel button:hover { color: var(--claim-strong); }
        .rd-rel .rd-dot { margin-left: 0.4rem; }
        .rd-cfoot { border-top: 1px solid var(--card-border); padding-top: 0.7rem; margin-top: 0.5rem; font-size: 12px; color: var(--card-muted); display: flex; justify-content: space-between; gap: 0.8rem; }
        .rd-cfoot a { color: var(--card-muted); }
        .rd-cfoot a:hover { color: var(--card-head); }

        /* ── disputing an edge ────────────────────────────────────────── */
        .rd-relrow { display: flex; align-items: baseline; gap: 0.5rem; }
        .rd-relrow > button { flex: 1; }
        .rd-flag { font-size: 11px; color: var(--card-faint); flex: none; opacity: 0; transition: opacity 0.12s; }
        .rd-relrow:hover .rd-flag, .rd-flag:focus-visible { opacity: 1; }
        .rd-flag:hover { color: var(--draft-strong); }
        .rd-flagged { font-size: 11px; color: var(--draft); flex: none; white-space: nowrap; }
        .rd-flagbox { border: 1px solid var(--draft-line); border-radius: 5px; padding: 0.6rem 0.7rem; margin: 0.3rem 0; background: var(--draft-wash); }
        .rd-flagbox p { font-size: 12px; color: var(--card-body); margin: 0 0 0.45rem; line-height: 1.4; }
        .rd-flagbox input { width: 100%; }
        .rd-flagact { display: flex; gap: 0.4rem; margin-top: 0.45rem; }

        /* ── the draft card ───────────────────────────────────────────── */
        .rd-kind-draft { color: var(--draft); }
        .rd-k-draft { color: var(--draft); }
        .rd-settled {
          font-size: 11px; letter-spacing: 0; text-transform: none; font-weight: 500;
          color: var(--card-muted); border: 1px solid var(--card-border); border-radius: 3px;
          padding: 1px 6px; white-space: nowrap;
        }
        .rd-standing { font-size: 12.5px; color: var(--card-muted); line-height: 1.45; margin: 0 0 0.6rem; }
        .rd-blk-top { border-top: 0; padding-top: 0; }
        .rd-dspan { font-family: var(--paper-serif); font-size: 14.5px; line-height: 1.5; color: var(--card-body); margin: 0 0 0.5rem; padding-left: 0.7rem; border-left: 2px solid var(--card-border-hover); }
        .rd-dedit {
          width: 100%; resize: vertical; font-family: var(--paper-serif); font-size: 15px;
          line-height: 1.45; color: var(--card-head); background: var(--card-bg);
          border: 1px solid var(--draft-line); border-radius: 5px; padding: 0.55rem 0.65rem;
        }
        .rd-dedit:focus { outline: 2px solid var(--draft); outline-offset: 1px; }
        .rd-blk .rd-dslug { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; color: var(--card-muted); margin: 0.35rem 0 0; overflow-wrap: anywhere; }
        .rd-dsel {
          font: inherit; font-size: 13px; color: var(--card-head); background: var(--card-bg);
          border: 1px solid var(--card-border-hover); border-radius: 4px; padding: 0.3rem 0.45rem; width: 100%;
        }
        .rd-blk .rd-dmeaning { font-size: 12.5px; color: var(--card-muted); margin: 0.4rem 0 0; }
        .rd-blk .rd-dnote, .rd-dnote { font-size: 12px; color: var(--card-muted); line-height: 1.45; margin: 0.4rem 0 0; }
        .rd-dnote b { color: var(--card-head); font-weight: 600; }
        .rd-who { display: flex; align-items: baseline; gap: 0.5rem; font-size: 12.5px; color: var(--card-muted); margin: 0 0 0.6rem; }
        .rd-who input, .rd-dnoteinput, .rd-flagbox input {
          font: inherit; font-size: 13px; color: var(--card-head); background: var(--card-bg);
          border: 1px solid var(--card-border); border-radius: 4px; padding: 0.3rem 0.45rem;
        }
        .rd-who input { flex: 1; min-width: 0; }
        .rd-who input:focus, .rd-dnoteinput:focus, .rd-flagbox input:focus { border-color: var(--draft); }
        .rd-dnoteinput { width: 100%; margin-bottom: 0.6rem; }
        .rd-dact { display: flex; flex-wrap: wrap; gap: 0.4rem; }
        .rd-btn {
          font-size: 13px; font-weight: 500; color: var(--card-body); background: var(--card-bg);
          border: 1px solid var(--card-border-hover); border-radius: 5px; padding: 0.35rem 0.7rem;
          transition: border-color 0.12s, color 0.12s;
        }
        .rd-btn:hover:not(:disabled) { border-color: var(--draft); color: var(--draft-strong); }
        .rd-btn:disabled { opacity: 0.5; cursor: default; }
        .rd-btn-go { color: var(--draft-strong); border-color: var(--draft); background: var(--draft-wash); }
        .rd-btn-q { border-color: var(--card-border); color: var(--card-muted); }
        .rd-flagbox .rd-warn { font-size: 12px; color: var(--card-head); margin: 0.4rem 0 0; }
        .rd-offline { background: var(--card-sunk); border-radius: 5px; padding: 0.7rem; margin-top: 0.6rem; }
        .rd-offline code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11.5px; }
        .rd-copy {
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 10.5px; line-height: 1.45;
          color: var(--card-body); background: var(--card-bg); border: 1px solid var(--card-border);
          border-radius: 4px; padding: 0.5rem; margin: 0.5rem 0 0; overflow-x: auto; white-space: pre-wrap;
          overflow-wrap: anywhere; user-select: all;
        }

        /* ── whole-tree adjudication (#82) ────────────────────────────── */
        .rd-mode-adj { margin-left: auto; color: var(--draft-strong); }
        .rd-mode-adj[aria-pressed="true"] { color: var(--draft-strong); }
        .rd-adjbar { border: 1px solid var(--draft); background: var(--draft-wash); border-radius: 6px; padding: 0.8rem 0.9rem; margin-bottom: 1rem; }
        .rd-k-adj { color: var(--draft-strong); display: flex; justify-content: space-between; align-items: baseline; gap: 0.6rem; }
        .rd-k-adj span { font-weight: 500; font-size: 12px; color: var(--card-muted); letter-spacing: 0; text-transform: none; }
        .rd-adjbar code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; }
        .rd-adjmsg { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; line-height: 1.45; color: var(--card-body); background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 4px; padding: 0.5rem; margin: 0.6rem 0 0; overflow-x: auto; white-space: pre-wrap; overflow-wrap: anywhere; }
        .rd-rulingswrap { margin-top: 0.7rem; }
        .rd-rulingswrap > summary { font-size: 12.5px; color: var(--card-muted); cursor: pointer; }
        .rd-rulingswrap > summary:hover { color: var(--card-head); }
        .rd-ruling { margin-top: 0.7rem; padding-top: 0.6rem; border-top: 1px solid var(--card-border); }
        .rd-rq { font-size: 12.5px; color: var(--card-body); line-height: 1.4; margin: 0 0 0.45rem; }
        .rd-adj { border: 1px solid var(--draft); border-radius: 5px; padding: 0.7rem 0.75rem; background: var(--draft-wash); }
        .rd-vbadge { font-weight: 500; font-size: 11px; color: var(--card-muted); text-transform: none; letter-spacing: 0; margin-left: 0.5rem; }
        .rd-vbadge.on { color: var(--draft-strong); }
        .rd-vrow { display: flex; flex-wrap: wrap; gap: 0.35rem; margin: 0.2rem 0 0.55rem; }
        .rd-vbtn { font-size: 12px; color: var(--card-body); background: var(--card-bg); border: 1px solid var(--card-border-hover); border-radius: 5px; padding: 0.3rem 0.6rem; }
        .rd-vbtn:hover:not(:disabled) { border-color: var(--draft); color: var(--draft-strong); }
        .rd-vbtn.on { color: var(--draft-strong); border-color: var(--draft); background: var(--draft-wash); font-weight: 500; }
        .rd-vbtn-sm { font-size: 11px; padding: 0.15rem 0.4rem; }
        .rd-vgrid { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.4rem; }
        .rd-vgrid label { font-size: 11.5px; color: var(--card-muted); display: flex; flex-direction: column; gap: 0.2rem; flex: 1; min-width: 7rem; }
        .rd-evrow { display: inline-flex; flex-wrap: wrap; gap: 0.25rem; align-items: center; }
        .rd-evstanding { font-size: 11px; color: var(--draft-strong); margin-left: 0.35rem; }

        /* ── drafts in the rail list ──────────────────────────────────── */
        .rd-drafts { margin-top: 1.6rem; border-top: 1px solid var(--card-border); padding-top: 0.9rem; }
        .rd-drow {
          display: grid; grid-template-columns: 8px 1fr auto; gap: 0 0.6rem; align-items: baseline;
          width: 100%; padding: 0.4rem 0.35rem 0.4rem 0; border-radius: 3px;
          color: var(--card-body); font-size: 13px; line-height: 1.4;
        }
        .rd-drow:hover { color: var(--card-head); background: var(--draft-wash); }
        .rd-dmark { display: inline-block; width: 8px; height: 8px; border-radius: 50%; border: 1.5px dashed var(--draft); flex: none; position: relative; top: -1px; }
        .rd-drow.settled .rd-dmark { border-style: solid; border-color: var(--card-border-hover); }
        .rd-drow.settled .rd-rt { color: var(--card-muted); }

        /* ── narrow ───────────────────────────────────────────────────── */
        @media (max-width: 1000px) {
          .rd-grid { grid-template-columns: minmax(0, 1fr); }
          .rd-rail {
            position: fixed; inset: auto 0 0 0; max-height: 72vh; z-index: 40;
            background: var(--card-bg); border-top: 1px solid var(--card-border-hover);
            box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.12); padding: 1rem 1.25rem 2rem;
            transform: translateY(102%); transition: transform 0.2s ease-out;
          }
          .rd-rail.open { transform: none; }
          .rd-rest { display: none; }
          .rd-dg { grid-template-columns: minmax(0, 1fr); gap: 0.9rem; }
          .rd-thumb { max-width: 16rem; }
        }
      `}</style>
    </div>
  );
}
