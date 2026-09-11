import React, { useCallback, useEffect, useMemo, useState } from 'react';

type Claim = {
  slug: string;
  claim: string;
  displayClaim?: string | null;
  panel?: string;
  status: string;
  epistemic: string;
  role?: string | null;
  stance?: string | null;
  'claim-type'?: string | null;
  isAssessment?: boolean;
  figureUrl?: string | null;
  reproFigureUrl?: string | null;
  originalFigureUrl?: string | null;
  number?: string | null;
  requires?: string[];
  supports?: string[];
  tests?: string[];
  entails?: string[];
  'derived-from'?: string[];
  refutes?: string[];
  'rules-out'?: string[];
  'dissociates-with'?: string[];
  validates?: string[];
  predicts?: string[];
  confirms?: string[];
  interprets?: string[];
  'enables-method'?: string[];
  scopes?: string[];
  script?: string | null;
  original_script?: string | null;
  script_execution?: string | null;
  script_execution_note?: string | null;
  notes?: string | null;
  time_fast?: string | null;
  time_full?: string | null;
  dataset?: string | null;
  method?: string | null;
  analysis?: string | null;
  verifyRow?: { paperValue: string; reproduced: string; result: string } | null;
  scriptSource?: string | null;
  log_output?: string | null;
  discrepancy?: { type: string; explanation: string } | null;
};

type Props = {
  allClaims: Claim[];
  paperSlug: string;
  baseUrl: string;
};

// What we did, in the first person — the same vocabulary as lib/status.ts. A drawer that
// said "Verified" in green was the site's most direct claim that a proposition is true, on
// the strength of having re-run a script.
const STATUS_LABEL: Record<string, string> = {
  'verified': 're-ran: numbers match',
  'verified:partial': 're-ran: partly matches',
  'verified:with-nuance': 're-ran: matches, with nuance',
  'verified:direction-and-trend': 're-ran: direction and trend match',
  'verified:interpretive': 'checked by reading, not by running',
  'failed': 're-ran: differs',
  'failed:mismatch': 're-ran: differs',
  'unverified:no-data': 'couldn\u2019t re-run — no data deposited',
  'unverified:no-code': 'couldn\u2019t re-run — no code deposited',
  'unverified:code-error': 'couldn\u2019t re-run — the deposited code errored',
  'unverified:compute-infeasible': 'couldn\u2019t re-run — needs specialist compute',
  'unverified:partial': 'not re-run yet',
  'unverified': 'not re-run yet',
  'unknown': 'not re-run yet',
};

function statusDotColor(status: string): string {
  // Slate, not green. The dot says we re-ran something; green would say the claim is true.
  if (status === 'verified') return '#475569';
  if (
    status === 'failed' ||
    status === 'unverified:code-error' ||
    status === 'unverified:compute-infeasible'
  )
    return '#f59e0b';
  return 'var(--card-faint)';
}

const roleChipStyle: Record<string, string> = {
  hypothesis: 'bg-violet-50 text-violet-700 border-violet-200 dark:bg-violet-950/40 dark:text-violet-300 dark:border-violet-900',
  prediction: 'bg-indigo-50 text-indigo-700 border-indigo-200 dark:bg-indigo-950/40 dark:text-indigo-300 dark:border-indigo-900',
  empirical: 'bg-sky-50 text-sky-700 border-sky-200 dark:bg-sky-950/40 dark:text-sky-300 dark:border-sky-900',
  control: 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-900',
  interpretation: 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-900',
  synthesis: 'bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-900',
  methodological: 'bg-teal-50 text-teal-700 border-teal-200 dark:bg-teal-950/40 dark:text-teal-300 dark:border-teal-900',
  scope: 'bg-slate-50 text-slate-600 border-slate-200 dark:bg-slate-800/60 dark:text-slate-300 dark:border-slate-700',
};

const EDGES: { key: keyof Claim; label: string; desc: string }[] = [
  { key: 'requires', label: 'Requires', desc: 'this claim depends on:' },
  { key: 'supports', label: 'Supports', desc: 'this claim supports:' },
  { key: 'tests', label: 'Tests', desc: 'tests the prediction:' },
  { key: 'entails', label: 'Entails', desc: 'this claim entails:' },
  { key: 'derived-from', label: 'Derived from', desc: 'derived from:' },
  { key: 'refutes', label: 'Refutes', desc: 'refutes:' },
  { key: 'rules-out', label: 'Rules out', desc: 'rules out:' },
  { key: 'dissociates-with', label: 'Dissociates with', desc: 'forms a dissociation pair with:' },
  { key: 'validates', label: 'Validates', desc: 'validates:' },
  { key: 'predicts', label: 'Predicts', desc: 'predicts:' },
  { key: 'confirms', label: 'Confirms', desc: 'confirms:' },
  { key: 'interprets', label: 'Interprets', desc: 'reframes:' },
  { key: 'enables-method', label: 'Enables method', desc: 'enables:' },
  { key: 'scopes', label: 'Scopes', desc: 'qualifies:' },
];

function verificationBanner(status: string, role?: string | null, stance?: string | null): { bg: string; border: string; text: string; icon: string; label: string; detail: string } {
  // A claim the paper does not assert is not a claim awaiting verification -- there is
  // nothing to verify, because the paper is arguing the proposition is false. This has to
  // come first: the role-based banners below all say the paper *states* the claim, which on
  // a ruled-out alternative is the exact inversion of its meaning.
  if (stance === 'rejects') return {
    bg: '#fffbeb', border: '#fcd34d', text: '#92400e', hue: 'amber', icon: '\u2298',
    label: 'Ruled out by this paper',
    detail: 'The paper does not assert this. It is an alternative explanation the paper argues against — recorded so the evidence that eliminated it has something to point at. Follow the incoming rules-out relation to see which result did the work.',
  };
  if (stance === 'entertains') return {
    bg: '#fffbeb', border: '#fcd34d', text: '#92400e', hue: 'amber', icon: '?',
    label: 'Raised, not asserted',
    detail: 'The paper raises this as a candidate and does not commit to it. No result in this tree settles it either way.',
  };
  if (stance === 'attributes') return {
    bg: '#f5f3ff', border: '#ddd6fe', text: '#5b21b6', hue: 'violet', icon: '\u201C',
    label: 'Attributed to others',
    detail: 'This paper reports that someone else asserts this. It is not a claim of this paper.',
  };
  // --- Role-based defaults for claims that don't get code verification ---
  // Hypotheses, predictions, literature-context, and synthesis claims are
  // assessed by their argumentative role, not by running code.
  if (status === 'unknown' || !status) {
    if (role === 'hypothesis') return {
      bg: '#eff6ff', border: '#bfdbfe', text: '#1e40af', hue: 'blue', icon: 'H',
      label: 'Manuscript hypothesis',
      detail: 'This is an organizing hypothesis stated by the paper. It is assessed by whether its predictions are supported, not by running code.',
    };
    if (role === 'prediction') return {
      bg: '#eff6ff', border: '#bfdbfe', text: '#1e40af', hue: 'blue', icon: 'P',
      label: 'Derived prediction',
      detail: 'This prediction is deductively derived from a hypothesis. It is tested by the empirical claims linked via "tests" edges.',
    };
    if (role === 'literature-context') return {
      bg: '#faf5ff', border: '#e9d5ff', text: '#6b21a8', hue: 'purple', icon: '↗',
      label: 'Cited claim',
      detail: 'This claim is inherited from prior literature. Its status depends on the cited paper\'s own evidence, not on this paper\'s data.',
    };
    if (role === 'synthesis' || role === 'interpretation') return {
      bg: '#eff6ff', border: '#bfdbfe', text: '#1e40af', hue: 'blue', icon: 'S',
      label: 'Interpretive claim',
      detail: 'This synthesis or interpretation integrates multiple empirical findings. Its warrant comes from the claims it draws on, not from a single verification.',
    };
    if (role === 'scope') return {
      bg: 'var(--card-sunk)', border: 'var(--card-border)', text: 'var(--card-muted)', icon: '◻',
      label: 'Scope declaration',
      detail: 'This claim declares a boundary condition on the paper\'s findings. It is confirmed by reading the methods, not by running code.',
    };
    // Default for unknown empirical/control/methodological
    return {
      bg: 'var(--card-sunk)', border: 'var(--card-border)', text: 'var(--card-muted)', icon: '?',
      label: 'Not yet assessed',
      detail: 'This claim has not been through the verification process.',
    };
  }

  // --- Code-executed verification statuses ---
  if (status === 'verified') return {
    bg: '#f8fafc', border: '#cbd5e1', text: '#334155', hue: 'slate', icon: '=',
    label: (role === 'scope' || role === 'methodological')
      ? 'we checked this by reading'
      : 're-ran: numbers match',
    detail: (role === 'scope' || role === 'methodological')
      ? 'Someone read the deposited code, methods text or data records and found this to hold. Not a judgement of whether the claim is correct.'
      : 'We ran a script against the authors\u2019 deposited data and the number that came out matched the number in the paper. That is a fact about the re-run, not about whether the claim is true.',
  };
  if (status === 'verified:partial') return {
    bg: '#f8fafc', border: '#cbd5e1', text: '#334155', hue: 'slate', icon: '~',
    label: 're-ran: partly matches',
    detail: 'Part of this claim came back matching against the deposited data. What we could not re-run is in the notes.',
  };
  if (status === 'verified:with-nuance') return {
    bg: '#fffbeb', border: '#fde68a', text: '#92400e', hue: 'amber', icon: '~',
    label: 're-ran: matches, with a discrepancy',
    detail: 'Direction or trend came back matching; magnitude or significance differs from the paper. The discrepancy is documented below.',
  };
  if (status === 'verified:interpretive') return {
    bg: '#f8fafc', border: '#cbd5e1', text: '#334155', hue: 'slate', icon: '=',
    label: 'checked by reading, not by running',
    detail: 'An interpretive claim with no code to run. Someone examined the evidence structure behind it — which is weaker evidence than a re-run, and is recorded separately for that reason.',
  };
  if (status === 'verified:direction-and-trend') return {
    bg: '#f8fafc', border: '#cbd5e1', text: '#334155', hue: 'slate', icon: '~',
    label: 're-ran: direction and trend match',
    detail: 'The direction and trend came back matching the paper; exact values differ.',
  };

  // --- Failure ---
  if (status === 'failed' || status === 'failed:mismatch') return {
    bg: '#fffbeb', border: '#fde68a', text: '#92400e', hue: 'amber', icon: '≠',
    label: 're-ran: differs',
    detail: 'We ran the authors\u2019 deposited code on their deposited data and got a different number than the paper reports. That is a disagreement worth looking at, not a verdict: it can be our error as easily as theirs.',
  };

  // --- Unverified with reason ---
  if (status === 'unverified:code-error') return {
    bg: '#fffbeb', border: '#fde68a', text: '#92400e', hue: 'amber', icon: '!',
    label: 'couldn\u2019t re-run — the code errored',
    detail: 'A script exists and we tried to run it, but it failed. Nothing follows about the claim.',
  };
  if (status === 'unverified:compute-infeasible') return {
    bg: 'var(--card-sunk)', border: 'var(--card-border)', text: 'var(--card-muted)', icon: '⏱',
    label: 'couldn\u2019t re-run — needs specialist compute',
    detail: 'Re-running this needs hardware or compute time we do not have. Not attempted, rather than attempted and failed.',
  };
  if (status === 'unverified:no-data') return {
    bg: 'var(--card-sunk)', border: 'var(--card-border)', text: 'var(--card-muted)', icon: '—',
    label: 'couldn\u2019t re-run — no data deposited',
    detail: 'The data this claim rests on is not publicly available, so there is nothing to re-run it against.',
  };
  if (status === 'unverified:no-code') return {
    bg: 'var(--card-sunk)', border: 'var(--card-border)', text: 'var(--card-muted)', icon: '—',
    label: 'not re-run yet — no script written',
    detail: 'Nobody has written a script to re-run this one. A gap in our effort, not in the paper.',
  };
  if (status === 'unverified' || status === 'unverified:partial' || status.startsWith('partial')) return {
    bg: 'var(--card-sunk)', border: 'var(--card-border)', text: 'var(--card-muted)', icon: '○',
    label: 'not re-run yet',
    detail: 'Nobody has attempted to re-run this claim against the deposited data. It says nothing about whether the claim holds.',
  };
  if (status === 'N/A') return {
    bg: 'var(--card-sunk)', border: 'var(--card-border)', text: 'var(--card-muted)', icon: '—',
    label: 'nothing to re-run',
    detail: 'This is not the kind of claim a script can check \u2014 a scope condition, or an interpretation.',
  };

  // --- Fallback ---
  return {
    bg: 'var(--card-sunk)', border: 'var(--card-border)', text: 'var(--card-muted)', icon: '?',
    label: status,
    detail: 'We do not recognise this status \u2014 see the notes.',
  };
}

function updateUrlClaim(slug: string | null) {
  const url = new URL(window.location.href);
  if (slug) url.searchParams.set('claim', slug);
  else url.searchParams.delete('claim');
  window.history.pushState({}, '', url.toString());
}

export default function ClaimDrawer({ allClaims, paperSlug, baseUrl }: Props) {
  const bySlug = useMemo(() => {
    const m: Record<string, Claim> = {};
    for (const c of allClaims) m[c.slug] = c;
    return m;
  }, [allClaims]);

  const [openSlug, setOpenSlug] = useState<string | null>(null);
  const [history, setHistory] = useState<string[]>([]);
  const [codeOpen, setCodeOpen] = useState(false);

  useEffect(() => {
    const sp = new URLSearchParams(window.location.search);
    const s = sp.get('claim');
    if (s && bySlug[s]) setOpenSlug(s);
  }, [bySlug]);

  useEffect(() => {
    const handler = (e: Event) => {
      const ev = e as CustomEvent<{ slug: string }>;
      const s = ev.detail?.slug;
      if (!s || !bySlug[s]) return;
      setOpenSlug(prev => {
        if (prev && prev !== s) {
          setHistory(h => [...h, prev]);
        }
        return s;
      });
      setCodeOpen(false);
    };
    window.addEventListener('open-claim', handler as EventListener);
    return () => window.removeEventListener('open-claim', handler as EventListener);
  }, [bySlug]);

  useEffect(() => {
    updateUrlClaim(openSlug);
  }, [openSlug]);

  useEffect(() => {
    const onPop = () => {
      const sp = new URLSearchParams(window.location.search);
      const s = sp.get('claim');
      setOpenSlug(s && bySlug[s] ? s : null);
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, [bySlug]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && openSlug) close();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [openSlug]);

  const close = useCallback(() => {
    setOpenSlug(null);
    setHistory([]);
    setCodeOpen(false);
  }, []);

  const goTo = useCallback(
    (slug: string) => {
      if (!bySlug[slug]) return;
      setOpenSlug(prev => {
        if (prev && prev !== slug) setHistory(h => [...h, prev]);
        return slug;
      });
      setCodeOpen(false);
    },
    [bySlug]
  );

  const goBack = useCallback(() => {
    setHistory(h => {
      if (h.length === 0) return h;
      const prev = h[h.length - 1];
      setOpenSlug(prev);
      setCodeOpen(false);
      return h.slice(0, -1);
    });
  }, []);

  if (!openSlug) return null;
  const claim = bySlug[openSlug];
  if (!claim) return null;

  const claimText = (claim.displayClaim?.trim()) || claim.claim;
  const original = claim.displayClaim && claim.displayClaim.trim() !== claim.claim ? claim.claim : null;
  const dotColor = statusDotColor(claim.status);
  const banner = verificationBanner(claim.status, claim.role, claim.stance);

  const hasCode = !!claim.script;
  const hasOrigFigure = !!(claim.originalFigureUrl || claim.figureUrl);
  const hasReproFigure = !!claim.reproFigureUrl;
  const hasFigurePair = hasOrigFigure && hasReproFigure;
  const origFigSrc = claim.originalFigureUrl || claim.figureUrl;
  const hasVerifyRow = !!claim.verifyRow;
  const hasScriptSource = !!claim.scriptSource;
  const hasDiscrepancy = !!claim.discrepancy;

  return (
    <>
      <div className="claim-drawer-backdrop" onClick={close} aria-hidden="true" />
      <aside
        className="claim-drawer"
        role="dialog"
        aria-label={`Claim details: ${claim.slug}`}
      >
        {/* Header */}
        <div className="drawer-header">
          <div className="drawer-header-left">
            {history.length > 0 && (
              <button className="drawer-back" onClick={goBack} aria-label="Back">
                ←
              </button>
            )}
            {claim.number && (
              <span className="drawer-number">{claim.number}</span>
            )}
            {claim.role && (
              <span
                className={`drawer-role-chip ${roleChipStyle[claim.role] ?? roleChipStyle.empirical}`}
              >
                {claim.role.toUpperCase()}
              </span>
            )}
            {claim.stance && claim.stance !== 'asserts' && (
              <span className="drawer-stance-chip" title="This paper does not assert this claim">
                {claim.stance === 'rejects' ? 'RULED OUT' : claim.stance.toUpperCase()}
              </span>
            )}
            {claim.panel && <span className="drawer-panel">{claim.panel}</span>}
          </div>
          <button className="drawer-close" onClick={close} aria-label="Close">
            ×
          </button>
        </div>

        <div className="drawer-body">
          {/* Full claim text */}
          <p className="drawer-claim-main">{claimText}</p>

          {/* VERIFICATION BANNER — the headline */}
          <div className={`drawer-verification hue-${(banner as any).hue ?? 'amber'}`}>
            <div className="drawer-verify-header">
              <span className="drawer-verify-icon">{banner.icon}</span>
              <span className="drawer-verify-label">{banner.label}</span>
            </div>
            <p className="drawer-verify-detail">{banner.detail}</p>

            {/* Timing */}
            {(claim.time_fast || claim.time_full) && (
              <div className="drawer-verify-timing">
                {claim.time_fast && <span>Fast: {claim.time_fast}</span>}
                {claim.time_fast && claim.time_full && <span className="drawer-verify-timing-sep">/</span>}
                {claim.time_full && <span>Full: {claim.time_full}</span>}
              </div>
            )}

            {/* Per-claim comparison: paper value vs reproduced */}
            {hasVerifyRow && (
              <div className="drawer-verify-compare">
                <div className="drawer-verify-compare-row">
                  <span className="drawer-verify-compare-label">Paper reports</span>
                  <span className="drawer-verify-compare-val">{claim.verifyRow!.paperValue}</span>
                </div>
                <div className="drawer-verify-compare-row">
                  <span className="drawer-verify-compare-label">We reproduced</span>
                  <span className="drawer-verify-compare-val">{claim.verifyRow!.reproduced}</span>
                </div>
                <div className="drawer-verify-compare-row">
                  <span className="drawer-verify-compare-label">Result</span>
                  <span className={`drawer-verify-compare-result ${claim.verifyRow!.result === 'PASS' ? 'result-pass' : 'result-other'}`}>
                    {claim.verifyRow!.result}
                  </span>
                </div>
              </div>
            )}

            {claim.script_execution_note && (
              <p className="drawer-verify-note">{claim.script_execution_note}</p>
            )}

            {claim.method && (
              <div className="drawer-verify-method">
                <span className="drawer-verify-method-label">Method:</span> {claim.method}
              </div>
            )}
          </div>

          {/* DISCREPANCY — when verification found a gap */}
          {hasDiscrepancy && (
            <div className={`drawer-discrepancy ${
              claim.discrepancy!.type === 'genuine-mismatch' ? 'discrepancy-mismatch' :
              claim.discrepancy!.type === 'data-gap' ? 'discrepancy-data' :
              'discrepancy-method'
            }`}>
              <div className="drawer-discrepancy-header">
                <span className="drawer-discrepancy-type">
                  {claim.discrepancy!.type === 'genuine-mismatch' ? 'Result mismatch' :
                   claim.discrepancy!.type === 'data-gap' ? 'Data not available' :
                   'Analysis pipeline differs'}
                </span>
              </div>
              <p className="drawer-discrepancy-text">{claim.discrepancy!.explanation}</p>
            </div>
          )}

          {/* FIGURE COMPARISON — original vs reproduced */}
          {hasFigurePair && (
            <div className="drawer-figures">
              <div className="drawer-figure-pair">
                <div className="drawer-figure-col">
                  <div className="drawer-figure-col-label">Published figure</div>
                  <img src={origFigSrc!} alt={`Original ${claim.panel ?? 'figure'}`} />
                  {claim.panel && <div className="drawer-figure-panel-ref">{claim.panel}</div>}
                </div>
                <div className="drawer-figure-col">
                  <div className="drawer-figure-col-label">Reproduced from data</div>
                  <img src={claim.reproFigureUrl!} alt="Reproduced figure" />
                </div>
              </div>
            </div>
          )}

          {/* Single figure (original only, no reproduction) */}
          {hasOrigFigure && !hasReproFigure && (
            <div className="drawer-figures">
              <div className="drawer-figure-single">
                <div className="drawer-figure-col-label">Published figure</div>
                <img src={origFigSrc!} alt={`Figure ${claim.panel ?? ''}`} />
                {claim.panel && <div className="drawer-figure-panel-ref">{claim.panel}</div>}
              </div>
            </div>
          )}

          {/* Single figure (reproduced only, no original) */}
          {!hasOrigFigure && hasReproFigure && (
            <div className="drawer-figures">
              <div className="drawer-figure-single">
                <div className="drawer-figure-col-label">Reproduced from data</div>
                <img src={claim.reproFigureUrl!} alt="Reproduced figure" />
              </div>
            </div>
          )}

          {original && (
            <div className="drawer-original">
              <div className="drawer-original-label">Original claim text</div>
              <p className="drawer-original-text">{original}</p>
            </div>
          )}

          {/* CODE — inline, expandable */}
          {hasCode && (
            <div className="drawer-code-section">
              <button
                className="drawer-code-toggle"
                onClick={() => setCodeOpen(o => !o)}
                aria-expanded={codeOpen}
              >
                <span className="drawer-code-toggle-icon">{codeOpen ? '▾' : '▸'}</span>
                <span className="drawer-code-toggle-label">View verification code</span>
                <span className="drawer-code-toggle-path">{claim.script}</span>
              </button>

              {codeOpen && (
                <div className="drawer-code-body">
                  {claim.dataset && (
                    <div className="drawer-code-row">
                      <span className="drawer-code-key">Data source</span>
                      <span className="drawer-code-val">{claim.dataset}</span>
                    </div>
                  )}
                  {claim.original_script && (
                    <div className="drawer-code-row">
                      <span className="drawer-code-key">Original analysis</span>
                      <span className="drawer-code-val">{claim.original_script}</span>
                    </div>
                  )}
                  {claim.notes && (
                    <div className="drawer-code-notes">{claim.notes}</div>
                  )}
                  {hasScriptSource && (
                    <div className="drawer-code-log">
                      <div className="drawer-code-log-header">verify.py</div>
                      <pre className="drawer-code-log-pre">{claim.scriptSource}</pre>
                    </div>
                  )}
                  {claim.log_output && (
                    <div className="drawer-code-log">
                      <div className="drawer-code-log-header">verify.log — output</div>
                      <pre className="drawer-code-log-pre">{claim.log_output}</pre>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Metadata row */}
          <div className="drawer-meta">
            <span className="drawer-meta-item">
              <span className="drawer-dot" style={{ background: dotColor }} />
              {STATUS_LABEL[claim.status] ?? claim.status}
            </span>
            <span className="drawer-meta-item">{claim.epistemic}</span>
            {claim['claim-type'] && (
              <span className="drawer-meta-item">{claim['claim-type']}</span>
            )}
            {claim.isAssessment && (
              <span className="drawer-meta-item drawer-meta-assessment">assessment</span>
            )}
          </div>

          {/* Relations */}
          {EDGES.map(({ key, label, desc }) => {
            const targets = ((claim[key] as string[] | undefined) ?? []).filter(Boolean);
            if (targets.length === 0) return null;
            return (
              <div key={key as string} className="drawer-edge-block">
                <div className="drawer-edge-label">{label}</div>
                <div className="drawer-edge-desc">{desc}</div>
                <div className="drawer-edge-targets">
                  {targets.map(t => {
                    const tc = bySlug[t];
                    return (
                      <button
                        key={t}
                        className="drawer-target-card"
                        onClick={() => tc && goTo(t)}
                        disabled={!tc}
                      >
                        <span className="drawer-target-meta">
                          {tc?.number && (
                            <span className="drawer-target-number">{tc.number}</span>
                          )}
                          <span className="drawer-target-slug">{t}</span>
                        </span>
                        {tc && (
                          <span className="drawer-target-text">
                            {(tc.displayClaim?.trim()) || tc.claim}
                          </span>
                        )}
                        {!tc && <span className="drawer-target-missing">(not in graph)</span>}
                      </button>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </aside>

      <style>{`
        .claim-drawer-backdrop {
          position: fixed;
          inset: 0;
          background: rgba(17, 24, 39, 0.35);
          z-index: 80;
          animation: fadeIn 0.15s ease;
        }
        .claim-drawer {
          position: fixed;
          top: 0;
          right: 0;
          bottom: 0;
          width: 40vw;
          min-width: 420px;
          max-width: 640px;
          background: var(--card-bg);
          box-shadow: -8px 0 24px rgba(17, 24, 39, 0.08);
          z-index: 90;
          display: flex;
          flex-direction: column;
          animation: slideIn 0.18s ease;
        }
        @media (max-width: 640px) {
          .claim-drawer {
            width: 100vw;
            min-width: 0;
            max-width: none;
          }
        }
        @keyframes fadeIn {
          from { opacity: 0; } to { opacity: 1; }
        }
        @keyframes slideIn {
          from { transform: translateX(30px); opacity: 0.4; }
          to { transform: translateX(0); opacity: 1; }
        }

        .drawer-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0.9rem 1.1rem;
          border-bottom: 1px solid var(--card-border);
          flex-shrink: 0;
        }
        .drawer-header-left {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          flex-wrap: wrap;
          min-width: 0;
        }
        .drawer-back, .drawer-close {
          background: transparent;
          border: 1px solid var(--card-border);
          color: var(--card-muted);
          width: 28px;
          height: 28px;
          border-radius: 4px;
          cursor: pointer;
          font-size: 16px;
          line-height: 1;
          display: inline-flex;
          align-items: center;
          justify-content: center;
        }
        .drawer-back:hover, .drawer-close:hover {
          border-color: var(--card-faint);
          color: var(--card-head);
        }
        .drawer-number {
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
          font-size: 13px;
          font-weight: 600;
          color: var(--card-body);
          letter-spacing: 0.02em;
        }
        .drawer-stance-chip {
          display: inline-block;
          font-size: 10px;
          font-weight: 700;
          letter-spacing: 0.05em;
          padding: 2px 7px;
          border-radius: 3px;
          border: 1px dashed #b45309;
          color: #b45309;
          background: rgba(180, 83, 9, 0.08);
        }
        .drawer-role-chip {
          display: inline-block;
          font-size: 9.5px;
          font-weight: 600;
          letter-spacing: 0.05em;
          padding: 1px 6px;
          border-radius: 3px;
          border: 1px solid;
          text-transform: uppercase;
        }
        .drawer-panel {
          color: var(--card-faint);
          text-transform: uppercase;
          letter-spacing: 0.08em;
          font-size: 10px;
          font-variant: small-caps;
        }

        .drawer-body {
          overflow-y: auto;
          padding: 1.1rem 1.1rem 2rem;
          flex: 1 1 auto;
        }
        .drawer-claim-main {
          font-size: 1.05rem;
          line-height: 1.55;
          color: var(--card-head);
          margin: 0 0 0.9rem;
          font-weight: 500;
        }

        /* ── Verification banner ── */
        .drawer-verification {
          border: 1px solid;
          border-radius: 6px;
          padding: 0.75rem 0.9rem;
          margin: 0 0 1rem;
        }
        .drawer-verify-header {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-bottom: 0.3rem;
        }
        .drawer-verify-icon {
          width: 22px;
          height: 22px;
          border-radius: 999px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          font-size: 12px;
          font-weight: 700;
          flex-shrink: 0;
        }
        .drawer-verify-label {
          font-size: 0.88rem;
          font-weight: 600;
        }
        .drawer-verify-detail {
          font-size: 0.78rem;
          line-height: 1.5;
          margin: 0;
          opacity: 0.85;
        }
        .drawer-verify-timing {
          margin-top: 0.4rem;
          font-size: 0.72rem;
          opacity: 0.7;
          display: flex;
          gap: 0.3rem;
        }
        .drawer-verify-timing-sep { opacity: 0.5; }
        .drawer-verify-note {
          margin: 0.4rem 0 0;
          font-size: 0.75rem;
          font-style: italic;
          opacity: 0.8;
          line-height: 1.45;
        }
        .drawer-verify-method {
          margin-top: 0.4rem;
          font-size: 0.75rem;
          opacity: 0.8;
        }
        .drawer-verify-method-label {
          font-weight: 600;
          text-transform: uppercase;
          font-size: 0.65rem;
          letter-spacing: 0.05em;
        }
        .drawer-verify-compare {
          margin-top: 0.6rem;
          border-top: 1px solid currentColor;
          border-top-color: inherit;
          opacity: 0.9;
          padding-top: 0.5rem;
        }
        .drawer-verify-compare-row {
          display: flex;
          justify-content: space-between;
          align-items: baseline;
          padding: 0.15rem 0;
          font-size: 0.78rem;
        }
        .drawer-verify-compare-label {
          font-size: 0.68rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          opacity: 0.7;
        }
        .drawer-verify-compare-val {
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
          font-size: 0.82rem;
          font-weight: 500;
        }
        .drawer-verify-compare-result {
          font-weight: 700;
          font-size: 0.78rem;
          letter-spacing: 0.03em;
        }
        .result-pass { }
        .result-other { opacity: 0.8; }

        /* ── Discrepancy block ── */
        .drawer-discrepancy {
          border-radius: 6px;
          padding: 0.7rem 0.85rem;
          margin: 0 0 1rem;
          border-left: 3px solid;
        }
        .discrepancy-mismatch {
          background: #fef2f2;
          border-left-color: #ef4444;
        }
        .discrepancy-data {
          background: var(--card-sunk);
          border-left-color: var(--card-faint);
        }
        .discrepancy-method {
          background: #fffbeb;
          border-left-color: #f59e0b;
        }
        .drawer-discrepancy-header {
          margin-bottom: 0.3rem;
        }
        .drawer-discrepancy-type {
          font-size: 0.75rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.04em;
        }
        .discrepancy-mismatch .drawer-discrepancy-type { color: #991b1b; }
        .discrepancy-data .drawer-discrepancy-type { color: var(--card-muted); }
        .discrepancy-method .drawer-discrepancy-type { color: #92400e; }
        .drawer-discrepancy-text {
          font-size: 0.78rem;
          line-height: 1.55;
          color: var(--card-body);
          margin: 0;
        }

        /* ── Figure comparison ── */
        .drawer-figures {
          margin: 0 0 1rem;
        }
        .drawer-figure-pair {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 0.6rem;
        }
        @media (max-width: 500px) {
          .drawer-figure-pair {
            grid-template-columns: 1fr;
          }
        }
        .drawer-figure-col {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }
        .drawer-figure-col-label {
          font-size: 9.5px;
          font-weight: 600;
          letter-spacing: 0.06em;
          text-transform: uppercase;
          color: var(--card-muted);
        }
        .drawer-figure-col img, .drawer-figure-single img {
          max-width: 100%;
          border: 1px solid var(--card-border);
          border-radius: 4px;
          display: block;
        }
        .drawer-figure-panel-ref {
          font-size: 0.68rem;
          color: var(--card-faint);
          text-transform: uppercase;
          letter-spacing: 0.06em;
        }
        .drawer-figure-single {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }

        /* ── Original claim text ── */
        .drawer-original {
          margin: 0 0 1rem;
          padding: 0.55rem 0.7rem;
          background: var(--card-sunk);
          border-left: 3px solid var(--card-border-hover);
          border-radius: 3px;
        }
        .drawer-original-label {
          font-size: 9.5px;
          font-weight: 600;
          letter-spacing: 0.08em;
          color: var(--card-faint);
          text-transform: uppercase;
          font-variant: small-caps;
          margin-bottom: 0.25rem;
        }
        .drawer-original-text {
          font-size: 0.85rem;
          color: var(--card-muted);
          line-height: 1.5;
          margin: 0;
        }

        /* ── Code section (expandable) ── */
        .drawer-code-section {
          margin: 0 0 1rem;
          border: 1px solid var(--card-border);
          border-radius: 6px;
          overflow: hidden;
        }
        .drawer-code-toggle {
          display: flex;
          align-items: center;
          gap: 0.4rem;
          width: 100%;
          padding: 0.6rem 0.75rem;
          background: var(--card-sunk);
          border: none;
          cursor: pointer;
          font: inherit;
          text-align: left;
          transition: background 0.1s ease;
        }
        .drawer-code-toggle:hover {
          background: var(--card-border);
        }
        .drawer-code-toggle-icon {
          font-size: 10px;
          color: var(--card-muted);
          width: 12px;
          flex-shrink: 0;
        }
        .drawer-code-toggle-label {
          font-size: 0.78rem;
          font-weight: 600;
          color: var(--card-body);
        }
        .drawer-code-toggle-path {
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
          font-size: 0.68rem;
          color: var(--card-faint);
          margin-left: auto;
          flex-shrink: 0;
        }
        .drawer-code-body {
          padding: 0.7rem 0.75rem;
          border-top: 1px solid var(--card-border);
        }
        .drawer-code-row {
          display: flex;
          gap: 0.5rem;
          font-size: 0.75rem;
          padding: 0.15rem 0;
          align-items: baseline;
        }
        .drawer-code-key {
          min-width: 6.5rem;
          font-size: 9px;
          font-weight: 600;
          letter-spacing: 0.06em;
          text-transform: uppercase;
          color: var(--card-faint);
          flex-shrink: 0;
        }
        .drawer-code-val {
          color: var(--card-body);
          word-break: break-all;
        }
        .drawer-code-notes {
          margin-top: 0.5rem;
          font-size: 0.75rem;
          color: var(--card-muted);
          line-height: 1.55;
          white-space: pre-wrap;
          padding: 0.5rem 0.6rem;
          background: var(--card-bg);
          border: 1px solid var(--card-border);
          border-radius: 3px;
        }
        .drawer-code-log {
          margin-top: 0.5rem;
          border-radius: 4px;
          overflow: hidden;
          border: 1px solid #1e293b;
        }
        .drawer-code-log-header {
          background: #1e293b;
          color: var(--card-faint);
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
          font-size: 10px;
          font-weight: 600;
          letter-spacing: 0.06em;
          padding: 0.35rem 0.6rem;
        }
        .drawer-code-log-pre {
          background: #0f172a;
          color: var(--card-strong);
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
          font-size: 10.5px;
          line-height: 1.55;
          padding: 0.6rem;
          margin: 0;
          overflow-x: auto;
          white-space: pre;
          max-height: 300px;
          overflow-y: auto;
        }

        /* ── Metadata ── */
        .drawer-meta {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          margin-bottom: 1.2rem;
          padding-bottom: 1rem;
          border-bottom: 1px solid var(--card-border);
        }
        .drawer-meta-item {
          font-size: 11px;
          color: var(--card-muted);
          background: var(--card-sunk);
          padding: 2px 8px;
          border-radius: 3px;
          display: inline-flex;
          align-items: center;
          gap: 0.3rem;
        }
        .drawer-meta-assessment {
          background: #fdf4ff;
          color: #86198f;
        }
        .drawer-dot {
          width: 8px;
          height: 8px;
          border-radius: 999px;
          display: inline-block;
        }

        /* ── Relations ── */
        .drawer-edge-block {
          margin-bottom: 1rem;
        }
        .drawer-edge-label {
          font-size: 10.5px;
          font-weight: 600;
          letter-spacing: 0.08em;
          color: var(--card-body);
          text-transform: uppercase;
          font-variant: small-caps;
        }
        .drawer-edge-desc {
          font-size: 0.72rem;
          color: var(--card-faint);
          font-style: italic;
          margin: 0.1rem 0 0.4rem;
        }
        .drawer-edge-targets {
          display: flex;
          flex-direction: column;
          gap: 0.35rem;
        }
        .drawer-target-card {
          text-align: left;
          background: var(--card-bg);
          border: 1px solid var(--card-border);
          border-radius: 4px;
          padding: 0.5rem 0.65rem;
          cursor: pointer;
          transition: border-color 0.12s ease, background 0.12s ease;
          display: flex;
          flex-direction: column;
          gap: 0.2rem;
          font: inherit;
          width: 100%;
        }
        .drawer-target-card:hover:not(:disabled) {
          border-color: var(--card-faint);
          background: #fafafa;
        }
        .drawer-target-card:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }
        .drawer-target-meta {
          display: inline-flex;
          align-items: baseline;
          gap: 0.4rem;
        }
        .drawer-target-number {
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
          font-size: 11.5px;
          color: var(--card-muted);
          font-weight: 500;
        }
        .drawer-target-slug {
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
          font-size: 10.5px;
          color: var(--card-faint);
        }
        .drawer-target-text {
          font-size: 0.85rem;
          color: var(--card-head);
          line-height: 1.4;
        }
        .drawer-target-missing {
          font-size: 0.7rem;
          color: var(--card-faint);
          font-style: italic;
        }

        .font-mono {
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        }
      `}</style>
    </>
  );
}
