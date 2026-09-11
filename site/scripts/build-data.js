#!/usr/bin/env node
// Reads claim markdown files from ../claims/ and outputs src/data/claims.json.
// Filters by corpus when CORPUS env var is set (reads ../corpus.yaml).
//   CORPUS=elife  → only eLife papers (default for public site)
//   CORPUS=all    → all papers (private/lab site)
//   unset         → defaults to 'elife'
import fs, { readFileSync, readdirSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import matter from 'gray-matter';
import { parse as parseYaml } from 'yaml';

const __dirname = dirname(fileURLToPath(import.meta.url));
const claimsRoot = join(__dirname, '../../claims');
const projectRoot = join(__dirname, '../../');
const outDir = join(__dirname, '../src/data');
const outFile = join(outDir, 'claims.json');

mkdirSync(outDir, { recursive: true });

// --- Verification level taxonomy ---
// How far we got re-running a paper. Every rung is a fact about our effort against the
// authors' *deposited* material — none of it is replication, which would mean an independent
// study finding the same thing, and which this corpus has never attempted.
//
// L1: we checked the deposit exists (a PDB record, a repository)
// L2: we read the deposited intermediates and compared them to the paper
// L3: we ran the authors' own scripts on their own data
// L4: we wrote our own analysis and ran it on their deposited data
// L5: we ran the whole pipeline from raw data — never reached
const VERIFICATION_LEVELS = {
  'artiushin-2026-spider-atlas': {
    level: 'unverified',
    label: 'We have not attempted it',
    detail: 'Atlas paper — data on Brain Image Library, verification is image inspection. Not attempted in this prototype.',
  },
  'bouyeure-2026-fear-rsa': {
    level: 'L4',
    label: 'We re-analysed their deposited data',
    detail: 'Downloaded NeuroVault NIfTI maps, independently counted significant voxels and found MNI peaks. Full MVPA pipeline not re-run.',
  },
  'ejdrup-2026-dopamine': {
    level: 'L3',
    label: 'We ran their deposited scripts',
    detail: 'Ran deposited figure-generation scripts with matplotlib patch. Vmax parameter sweep timed out (600s) — 3 simulation claims unverified.',
  },
  'gadeke-2026-guilt-insula': {
    level: 'L4',
    label: 'We re-analysed their deposited data',
    detail: 'Downloaded OpenNeuro CSVs, fit logistic regression independently, confirmed MNI peak coordinates. Full fMRI preprocessing not re-run.',
  },
  'headley-2026-inhibitory-rhythms': {
    level: 'L2',
    label: 'We compared their deposited CSVs',
    detail: 'Read deposited CSVs from GitHub, confirmed firing-rate values and STA timings. NEURON simulation not re-run (6 hrs + 1.88 GB Dryad).',
  },
  'kammer-2026-foveal-feedback': {
    level: 'unverified',
    label: 'We could not re-run it — specialist compute',
    detail: 'Per-subject fMRI MVPA pipeline requires specialist compute. Data on OpenNeuro but pipeline not re-run.',
  },
  'kolb-2026-igabasnfr2': {
    level: 'L1',
    label: 'We checked the deposit exists',
    detail: 'Parsed PDB 9D57 record from RCSB, confirmed structure metadata. Wet-lab experiments not computationally reproducible.',
  },
  'meijer-2025-serotonin-additive-r1': {
    level: 'L2',
    label: 'We compared their deposited CSVs',
    detail: 'Read deposited CSVs from GitHub repo, confirmed GLM interaction, modulation counts, and receptor expression results. 14/14 PASS. Full GLM refit requires iblatlas.',
  },
  'meijer-2025-serotonin-orthogonal': {
    level: 'L2',
    label: 'We compared their deposited CSVs',
    detail: 'Read deposited CSVs from GitHub repo, confirmed neuron counts, modulation fractions, and orthogonality measures. 9/12 PASS, 2 FAIL (ripple suppression direction, region count), 1 WARN (latency correlation).',
  },
  'rozak-2026-neurovascular-dl': {
    level: 'unverified',
    label: 'We could not re-run it — training data is proprietary',
    detail: 'Deep learning pipeline trained on proprietary microscopy data. Pre-trained model available but training set not redistributable.',
  },
  'sautory-2026-serotonin-novelty': {
    level: 'L2',
    label: 'We compared their CSVs and audited the repo',
    detail: 'All statistical values verified against deposited CSVs. Analysis scripts and data paths confirmed on disk. Full R analysis pipeline not re-run.',
  },
  'scheller-2026-self-prioritization': {
    level: 'L2',
    label: 'We compared their deposited CSVs',
    detail: 'Downloaded Stan posterior CSVs from OSF (live, not from-notes). Computed TVA statistics from posterior samples. 8/8 PASS. Full Stan model not re-run (12 hrs).',
  },
  'wengert-2026-kcnc1': {
    level: 'L4',
    label: 'We re-analysed their deposited data',
    detail: 'Downloaded G-Node Excel data, computed independent statistical tests. Direction confirmed for all claims; one magnitude mismatch (maximal firing).',
  },
};

// --- Corpus filtering ---
const corpusName = process.env.CORPUS || 'elife';
let allowedPapers = null; // null = no filter (all papers)

if (corpusName !== 'all') {
  const manifestPath = join(projectRoot, 'corpus.yaml');
  if (existsSync(manifestPath)) {
    const manifest = parseYaml(readFileSync(manifestPath, 'utf8'));
    const corpus = manifest?.corpora?.[corpusName];
    if (corpus?.papers) {
      allowedPapers = new Set(corpus.papers);
      console.log(`Corpus filter: ${corpusName} (${allowedPapers.size} papers)`);
    } else {
      console.warn(`Corpus '${corpusName}' not found in corpus.yaml; building all papers`);
    }
  } else {
    console.warn('No corpus.yaml found; building all papers');
  }
}

const ASSESSMENT_SUFFIXES = ['-scope', '-assumed', '-unjustified', '-constraint', '-only', '-parameterization', '-initialization'];

function isAssessment(slug, fm) {
  if (fm['claim-type'] === 'assessment') return true;
  return ASSESSMENT_SUFFIXES.some(s => slug.endsWith(s));
}

// Figure resolution: panel "fig3B" → fig3.jpg.
// Supplements: "fig3-figure-supplement-1" or "fig3-figsupp1" → fig3-figsupp1.jpg.
// Searches two locations: public/figures/{paper}/ and public/verification/originals/{paper}/

function panelToFigureFile(panel) {
  if (!panel) return null;
  const first = panel.split(',')[0].trim().toLowerCase();
  const suppMatch = first.match(/^fig(\d+)[-\s]*(?:figure[-\s]*supplement[-\s]*|figsupp)(\d+)/);
  if (suppMatch) return `fig${suppMatch[1]}-figsupp${suppMatch[2]}.jpg`;
  const figMatch = first.match(/^fig(\d+)/);
  if (figMatch) return `fig${figMatch[1]}.jpg`;
  return null;
}

function computeFigureUrl(paperSlug, panel) {
  const file = panelToFigureFile(panel);
  if (!file) return null;
  // Check public/figures/{paper}/ first (curated full-resolution figures)
  const figPath = join(__dirname, '../public/figures', paperSlug, file);
  if (fs.existsSync(figPath)) return `/elife-claim-trees/figures/${paperSlug}/${file}`;
  // Fall back to verification/originals/{paper}/ (original figure panels from papers)
  const origPath = join(__dirname, '../public/verification/originals', paperSlug, file);
  if (fs.existsSync(origPath)) return `/elife-claim-trees/verification/originals/${paperSlug}/${file}`;
  return null;
}

function normalizeStatus(reproductions) {
  if (!reproductions || reproductions.length === 0) return 'unknown';
  // Take the most recent reproduction
  // The current record is the newest by date, not the last in the array. Every other
  // consumer (corpus_facts.py, check_reproductions.py, audit_verifications.py) picks by
  // date; this picked by position, so a record prepended to the list was ignored and the
  // site kept showing superseded statuses while the corpus had moved on.
  // Compare the date's value, not its printed form. YAML parses `date: 2026-09-11` into a
  // Date, and String(Date) begins with the weekday — so "Fri Sep 11" sorted before
  // "Mon Mar 30" alphabetically and the older record won.
  const when = r => { const t = new Date(r?.date ?? 0).getTime(); return Number.isNaN(t) ? 0 : t; };
  const last = [...reproductions].sort((a, b) => when(a) - when(b)).at(-1);
  return last.status || 'unknown';
}

const papers = [];

for (const paperSlug of readdirSync(claimsRoot).sort()) {
  // Corpus filter: skip papers not in the selected corpus
  if (allowedPapers && !allowedPapers.has(paperSlug)) continue;

  const paperDir = join(claimsRoot, paperSlug);
  const indexPath = join(paperDir, 'index.md');

  let paperMeta = {};
  try {
    const { data } = matter(readFileSync(indexPath, 'utf8'));
    paperMeta = data;
  } catch {
    continue;
  }

  const claims = [];

  for (const file of readdirSync(paperDir).sort()) {
    if (file === 'index.md' || !file.endsWith('.md')) continue;
    const slug = file.replace('.md', '');
    const raw = readFileSync(join(paperDir, file), 'utf8');
    // Fix a YAML quirk: `belongings:\n[]` must be `belongings: []`
    const fixed = raw.replace(/^(belongings|reproductions|assertions|concepts):\n\[\]/gm, '$1: []');
    let fm, content;
    try {
      ({ data: fm, content } = matter(fixed));
    } catch (e) {
      console.warn(`YAML parse error in ${file}:`, e.message);
      fm = {}; content = '';
    }

    const requires = (fm.belongings || [])
      .filter(b => b.relation === 'requires')
      .map(b => b.target);
    const supports = (fm.belongings || [])
      .filter(b => b.relation === 'supports')
      .map(b => b.target);

    const status = normalizeStatus(fm.reproductions);
    const notes = (fm.reproductions || []).map(r => r.notes).filter(Boolean).join('\n\n');

    const logPath = join(projectRoot,
      `verification/${paperSlug}/verify.log`);
    const log_output = fs.existsSync(logPath)
      ? fs.readFileSync(logPath, 'utf8').slice(0, 3000)
      : null;

    // Extract per-claim verification row from log: "slug | PAPER VALUE | REPRODUCED | STATUS"
    let verifyRow = null;
    if (log_output) {
      for (const line of log_output.split('\n')) {
        // Match lines like: "perceptual-salience-6hz-advantage  | 6 Hz  | 6.05 Hz ... | PASS"
        if (line.includes(slug) && line.includes('|')) {
          const parts = line.split('|').map(s => s.trim());
          if (parts.length >= 4) {
            verifyRow = { paperValue: parts[1], reproduced: parts[2], result: parts[3] };
          }
          break;
        }
      }
    }

    // Read verify.py source code (truncated to keep JSON manageable)
    const scriptPath = fm.reproductions?.[0]?.script;
    let scriptSource = null;
    if (scriptPath) {
      const fullScriptPath = join(projectRoot, scriptPath);
      if (fs.existsSync(fullScriptPath)) {
        scriptSource = fs.readFileSync(fullScriptPath, 'utf8').slice(0, 8000);
      }
    }

    const panel = fm.assertions?.[0]?.panel || '';
    const figureUri = fm.assertions?.[0]?.figureUri || null;
    claims.push({
      uuid: fm.uuid || null,
      slug,
      paper: paperSlug,
      panel,
      figureUrl: figureUri || computeFigureUrl(paperSlug, panel),
      claim: (fm.claim || '').trim(),
      displayClaim: (fm.displayClaim || '').trim() || null,
      shortClaim: (fm.shortClaim || '').trim() || null,
      epistemic: fm.epistemic || 'unknown',
      status,
      discrepancy: fm.discrepancy || null,
      'claim-type': fm['claim-type'] || 'empirical',
      isAssessment: isAssessment(slug, fm),
      requires,
      supports,
      role: fm.role || null,
      // The paper's position toward the proposition, not the analyst's confidence in it.
      // Absent means `asserts` (docs/claim-format.md §2). This must reach the page: a claim
      // the paper *rejects* rendered like any other says the paper asserts what it denies,
      // which is the same over-reading the MIRA export warns about in its gap report.
      stance: fm.assertions?.[0]?.stance || 'asserts',
      entails: fm.entails || [],
      'derived-from': fm['derived-from'] || [],
      tests: fm.tests || [],
      refutes: fm.refutes || [],
      'rules-out': fm['rules-out'] || [],
      'dissociates-with': fm['dissociates-with'] || [],
      validates: fm.validates || [],
      predicts: fm.predicts || [],
      confirms: fm.confirms || [],
      interprets: fm.interprets || [],
      'enables-method': fm['enables-method'] || [],
      scopes: fm.scopes || [],
      notes: notes.trim(),
      figure: fm.reproductions?.[0]?.figure || null,
      reproFigureUrl: fm.reproductions?.[0]?.figure
        ? `/elife-claim-trees/${fm.reproductions[0].figure}`
        : null,
      original_figure: fm.reproductions?.[0]?.original_figure || null,
      originalFigureUrl: fm.reproductions?.[0]?.original_figure
        ? `/elife-claim-trees/${fm.reproductions[0].original_figure}`
        : null,
      dataset: fm.assertions?.[0]?.dataset || null,
      analysis: fm.assertions?.[0]?.analysis || null,
      method: fm.assertions?.[0]?.method || null,
      script: fm.reproductions?.[0]?.script || null,
      original_script: fm.reproductions?.[0]?.original_script || null,
      script_execution: fm.reproductions?.[0]?.script_execution || null,
      script_execution_note: fm.reproductions?.[0]?.script_execution_note || null,
      time_fast: fm.reproductions?.[0]?.time_fast || null,
      time_full: fm.reproductions?.[0]?.time_full || null,
      verifyRow,
      scriptSource,
      log_output,
    });
  }

  // ---------- Hierarchical claim numbering ----------
  // Precedence: Hypothesis → H#; Prediction (derived-from) → H#.P#;
  // Empirical tested by pred/hyp → H#.P#.# or H#.#;
  // Interpretation → I#; Synthesis → S#; Control → C#;
  // Dissociation-pair → D# (mutual dissociates-with); Standalone empirical → E#;
  // Methodological → M#; Scope targeted → Sc#; Global scope (*) → no number.
  {
    const bySlug = Object.fromEntries(claims.map(c => [c.slug, c]));
    const numberOf = {};      // slug -> string like "H1.P2.1"
    const partsOf = {};       // slug -> array like ['H',1,'P',2,1]
    const assign = (slug, str, parts) => {
      if (numberOf[slug]) return;
      numberOf[slug] = str;
      partsOf[slug] = parts;
    };

    // Claims the paper does not assert are numbered separately, at the end. They are
    // functionally hypotheses, so without this they join the H-series -- and because their
    // slugs sort first, Gaedeke's six rejected alternatives became H1-H6 and the paper's own
    // hypotheses were pushed to H7-H9. A reader then meets the paper's argument as six
    // propositions it denies. Stance decides membership of every role series below.
    const asserted = c => (c.stance || 'asserts') === 'asserts';

    // 1. Hypotheses (file-read order, which is sorted alphabetical)
    const hypotheses = claims.filter(c => c.role === 'hypothesis' && asserted(c));
    hypotheses.forEach((h, hi) => {
      const hNum = hi + 1;
      assign(h.slug, `H${hNum}`, ['H', hNum]);

      // Predictions that derive-from this hypothesis
      const preds = claims.filter(c =>
        c.role === 'prediction' && (c['derived-from'] || []).includes(h.slug)
      );
      preds.forEach((p, pi) => {
        const pNum = pi + 1;
        assign(p.slug, `H${hNum}.P${pNum}`, ['H', hNum, 'P', pNum]);

        // Empirical claims that test this prediction
        const tests = claims.filter(c =>
          (c.tests || []).includes(p.slug)
        );
        tests.forEach((t, ti) => {
          assign(t.slug, `H${hNum}.P${pNum}.${ti + 1}`, ['H', hNum, 'P', pNum, ti + 1]);
        });
      });

      // Empirical claims that test the hypothesis directly (no prediction layer)
      const directTests = claims.filter(c =>
        (c.tests || []).includes(h.slug) && !numberOf[c.slug]
      );
      directTests.forEach((t, ti) => {
        assign(t.slug, `H${hNum}.${ti + 1}`, ['H', hNum, ti + 1]);
      });
    });

    // 2. Interpretations
    let iCount = 0;
    claims.filter(c => c.role === 'interpretation' && asserted(c) && !numberOf[c.slug]).forEach(c => {
      iCount += 1;
      assign(c.slug, `I${iCount}`, ['I', iCount]);
    });

    // 2b. Literature-context (distinct role in Meijer paper) — L-series
    let lCount = 0;
    claims.filter(c => c.role === 'literature-context' && asserted(c) && !numberOf[c.slug]).forEach(c => {
      lCount += 1;
      assign(c.slug, `L${lCount}`, ['L', lCount]);
    });

    // 3. Synthesis
    let sCount = 0;
    claims.filter(c => c.role === 'synthesis' && asserted(c) && !numberOf[c.slug]).forEach(c => {
      sCount += 1;
      assign(c.slug, `S${sCount}`, ['S', sCount]);
    });

    // 4. Controls
    let cCount = 0;
    claims.filter(c => c.role === 'control' && asserted(c) && !numberOf[c.slug]).forEach(c => {
      cCount += 1;
      assign(c.slug, `C${cCount}`, ['C', cCount]);
    });

    // 5. Dissociation pairs (mutual dissociates-with). Assign D# per pair;
    // both members display the same number. Skip claims already numbered.
    const pairs = [];
    const pairIndex = {}; // slug -> pair index
    const seenPair = new Set();
    for (const c of claims) {
      for (const other of (c['dissociates-with'] || [])) {
        if (!bySlug[other]) continue;
        const key = [c.slug, other].sort().join('|');
        if (seenPair.has(key)) continue;
        seenPair.add(key);
        pairs.push([c.slug, other]);
      }
    }
    pairs.forEach(([a, b], pi) => {
      const dNum = pi + 1;
      for (const slug of [a, b]) {
        if (!numberOf[slug] && pairIndex[slug] === undefined) {
          pairIndex[slug] = dNum;
        }
      }
    });
    for (const [slug, dNum] of Object.entries(pairIndex)) {
      assign(slug, `D${dNum}`, ['D', dNum]);
    }

    // 6. Standalone empirical (role:empirical, no number yet)
    let eCount = 0;
    claims.filter(c => c.role === 'empirical' && asserted(c) && !numberOf[c.slug]).forEach(c => {
      eCount += 1;
      assign(c.slug, `E${eCount}`, ['E', eCount]);
    });

    // 7. Methodological
    let mCount = 0;
    claims.filter(c => c.role === 'methodological' && asserted(c) && !numberOf[c.slug]).forEach(c => {
      mCount += 1;
      assign(c.slug, `M${mCount}`, ['M', mCount]);
    });

    // 8. Targeted scope (not scopes: ["*"]). Includes empty-scopes lists
    // (treated as targeted-by-implication) — only global-* is truly unnumbered.
    let scCount = 0;
    claims.filter(c => {
      if (c.role !== 'scope' || !asserted(c) || numberOf[c.slug]) return false;
      const s = c.scopes || [];
      return !s.includes('*');
    }).forEach(c => {
      scCount += 1;
      assign(c.slug, `Sc${scCount}`, ['Sc', scCount]);
    });

    // 9. Orphan predictions (role:prediction with no derived-from) — P-series
    let pCount = 0;
    claims.filter(c => c.role === 'prediction' && asserted(c) && !numberOf[c.slug]).forEach(c => {
      pCount += 1;
      assign(c.slug, `P${pCount}`, ['P', pCount]);
    });

    // 10. Alternatives the paper does not assert — A-series, last, so they read as what
    // they are: rivals the paper eliminated, not steps in its own argument.
    let aCount = 0;
    claims.filter(c => !asserted(c) && !numberOf[c.slug]).forEach(c => {
      aCount += 1;
      assign(c.slug, `A${aCount}`, ['A', aCount]);
    });

    // Attach to claim objects
    for (const c of claims) {
      c.number = numberOf[c.slug] ?? null;
      c.numberParts = partsOf[c.slug] ?? null;
    }
  }

  // Count statuses
  const statusCounts = {};
  for (const c of claims) {
    statusCounts[c.status] = (statusCounts[c.status] || 0) + 1;
  }

  const verLevel = VERIFICATION_LEVELS[paperSlug] || {
    level: 'unknown', label: 'Unknown', detail: 'No verification metadata available.',
  };

  papers.push({
    slug: paperSlug,
    title: paperMeta.title || paperSlug,
    authors: paperMeta.authors || [],
    doi: paperMeta.doi || null,
    url: paperMeta.url || null,
    github: paperMeta.github || null,
    journal: paperMeta.journal || 'eLife',
    stage: paperMeta.stage || 'published',
    added: paperMeta.added || null,
    claimCount: claims.length,
    statusCounts,
    verificationLevel: verLevel.level,
    verificationLabel: verLevel.label,
    verificationDetail: verLevel.detail,
    claims,
  });
}

const totalClaims = papers.reduce((sum, p) => sum + p.claims.length, 0);
const allStatuses = {};
for (const p of papers) {
  for (const [k, v] of Object.entries(p.statusCounts)) {
    allStatuses[k] = (allStatuses[k] || 0) + v;
  }
}

const out = { papers, totalClaims, statusCounts: allStatuses };
writeFileSync(outFile, JSON.stringify(out, null, 2));
console.log(`Written ${outFile}: ${papers.length} papers, ${totalClaims} claims`);

// ── Publish the design notes ──────────────────────────────────────────────
// The pipeline's design note documents the structure the site has. It is self-contained HTML
// with its own styles, so it is served as an asset rather than re-rendered through the layout
// — one file, linked from /pipeline, with no second copy to drift.
const designSrc = join(projectRoot, 'docs', 'design');
const designDst = join(__dirname, '../public/design');
if (existsSync(designSrc)) {
  mkdirSync(designDst, { recursive: true });
  let d = 0;
  for (const f of readdirSync(designSrc)) {
    if (!f.endsWith('.html')) continue;
    fs.copyFileSync(join(designSrc, f), join(designDst, f));
    d++;
  }
  console.log(`Copied ${d} design note(s) to public/design/`);
}

// ── Publish the MIRA exports ──────────────────────────────────────────────
// The download links on the standards page point at /exports/, which is served from
// site/public/exports/. Copying here rather than by hand means a regenerated export cannot
// silently disagree with the file the site offers — which is the whole claim being made
// about them ("run the exporter and diff").
const exportsSrc = join(projectRoot, 'exports');
const exportsDst = join(__dirname, '../public/exports');
if (existsSync(exportsSrc)) {
  mkdirSync(exportsDst, { recursive: true });
  const published = new Set(papers.map(p => p.slug));
  let n = 0;
  for (const f of readdirSync(exportsSrc)) {
    // Only papers the site publishes: the corpus filter is the authority on that, and
    // shipping an export for a paper with no page would be a dangling download.
    const slug = f.replace(
      /\.(mira|mira-extended|dg)\.jsonld$|\.(gap-report|formats)\.md$|\.(oxa|formats)\.json$/, '');
    if (!published.has(slug)) continue;
    fs.copyFileSync(join(exportsSrc, f), join(exportsDst, f));
    n++;
  }
  console.log(`Copied ${n} export files to public/exports/`);
}

// ── Record which produced artifacts are actually downloadable ──────────────
// `produces` in layers.yaml is a repo path, and only some of those families are copied into
// public/ — exports and the verification figures are, claims/ coverage/ mappings/ marked/
// runs/ are not. The drawer offers a download for a file the site really serves and a source
// link for one it does not, and that distinction has to be measured rather than assumed: a
// download that 404s is worse than an honest "in the repository" link.
//
// Walks public/ once and writes the set of paths it found. A file that stops being copied
// stops being offered, with no second list to keep in step.
const artifactRoots = ['exports', 'verification', 'figures', 'design'];
const publishedPaths = [];
const walk = (abs, rel) => {
  if (!existsSync(abs)) return;
  for (const e of readdirSync(abs, { withFileTypes: true })) {
    const r = `${rel}/${e.name}`;
    if (e.isDirectory()) walk(join(abs, e.name), r);
    else publishedPaths.push(r);
  }
};
for (const root of artifactRoots) walk(join(__dirname, '../public', root), root);
publishedPaths.sort();
const artifactsOut = join(__dirname, '../src/data/published-artifacts.json');
writeFileSync(artifactsOut, JSON.stringify(publishedPaths, null, 0) + '\n');
console.log(`Written ${artifactsOut}: ${publishedPaths.length} published artifact paths`);
