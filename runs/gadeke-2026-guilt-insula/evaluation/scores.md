The matcher was one Claude Opus 5 subagent per tree, unreviewed.
The baseline this compares to is experiments/2026-09-11-gadeke-subagent-rerun/ (old prompts, Opus everywhere: 97 claims, 173 edges, 27 of 33 recovered, role 85%, panel 30%, 70 extras).
Evaluation is not yet a declared layer (item 7 of docs/design/2026-09-11-reading-the-paper-better.md).

## v2 (Sonnet readers)

  committed 33   re-run 63

  RECOVERY  25/33 = 76%
  ROLE      19/25 = 76% of matched pairs
  PANEL     10/25 = 40% of matched pairs

  committed claims the re-run did not recover (8):
    hypothesis         alt-agency-aversion-not-guilt
    hypothesis         alt-guilt-effect-driven-by-own-outcome
    hypothesis         alt-imaging-contrast-invalid
    hypothesis         alt-model-based-glm-invalid
    hypothesis         alt-participants-insensitive-to-value
    hypothesis         alt-social-context-shifts-risk-attitude
    prediction         prediction-responsibility-model-wins-comparison
    scope              scope-two-study-design

  re-run claims with no committed counterpart: 38

  role disagreements on matched pairs (6):
    hypothesis         → interpretation     hypothesis-insula-tracks-interpersonal-guilt
    hypothesis         → interpretation     hypothesis-sts-mentalizes-partner-state-unde
    interpretation     → empirical          insula-guilt-replicates-yu-koban-signature
    control            → empirical          lottery-choice-increases-with-ev
    scope              → methodological     partner-algorithm-deception-assumption
    control            → empirical          ventral-striatum-tracks-risky-choices

## v3 (Opus everywhere)

  committed 33   re-run 68

  RECOVERY  26/33 = 79%
  ROLE      20/26 = 77% of matched pairs
  PANEL     6/26 = 23% of matched pairs

  committed claims the re-run did not recover (7):
    hypothesis         alt-guilt-effect-driven-by-own-outcome
    hypothesis         alt-imaging-contrast-invalid
    hypothesis         alt-model-based-glm-invalid
    hypothesis         alt-participants-insensitive-to-value
    hypothesis         alt-social-context-shifts-risk-attitude
    hypothesis         hypothesis-responsibility-weights-partner-rpes
    literature-context interprets-yu-koban-guilt-signature

  re-run claims with no committed counterpart: 42

  role disagreements on matched pairs (6):
    hypothesis         → interpretation     alt-agency-aversion-not-guilt
    empirical          → control            guilt-signature-no-individual-difference
    hypothesis         → interpretation     hypothesis-sts-mentalizes-partner-state-unde
    interpretation     → control            insula-guilt-replicates-yu-koban-signature
    empirical          → interpretation     insula-ifg-connectivity-guilt
    scope              → methodological     partner-algorithm-deception-assumption

## v3 — the whole chain re-induced under the current prompts (#96)

`claim-tree` v3 is the first Gädeke tree whose every layer is one recorded chain under the
current prompts: the three readers reading the Introduction, Results, Discussion and the
numbered spans (citing `span`); `reconcile` v6 carrying those spans into the draft;
`external-review` v4 over the full paper; `edge-inference` v6 whose `why`s cite the spans.
The six `alt-` claims, their `rules-out` edges and the nineteen reproduction records were
carried forward from v2 by the same `carry_over` code #73 used, through a fresh v2↔v3 matcher
alignment (`match.v3-v2.pairs.json`, also written as `match.v4.pairs.json` for the runner's
`_find_pairs`). v3 has **68 claims** (62 induced + 6 carried alternatives) against v2's 74;
the six it does not carry are exactly the sentences the current contract's vocabulary now
lists as *not a claim* — a normalisation, a measure definition, a seed choice, a whole-brain
threshold, an exclusion count and an a-priori sample size — the last two folded into the
two-study scope claim instead.

Matcher answers were produced by a Claude Opus 4.8 subagent (`match.v3-v2.pairs.json`,
`match.v3-v1.pairs.json`); no model backend had credit, so every model-answered layer was
answered against the exact dumped prompt.

### v3 vs v2 (reference = runs/…/claim-tree.v2, candidate = claims/)

  committed 74   re-run 68

  RECOVERY  68/74 = 92%
  PRECISION 68/68 = 100%  (13 part-of)
  ROLE      68/68 = 100% of matched pairs
  PANEL     68/68 = 100% of matched pairs
  EDGES     48/78 ref edges recovered  (62%)  |  36 extra CLI edge(s)

  committed claims the re-run did not recover (6) — the six the current prompt reclassifies as not a claim:
    methodological     all-reported-clusters-survive-whole-brain
    scope              fmri-data-four-study-participants
    methodological     happiness-ratings-z-scored-per-participant
    methodological     risk-attitude-quantified-risk-premium
    methodological     study-sample-size-fixed-priori
    methodological     two-gppi-seed-to-voxel-connectivity-analyses

  re-run claims with no committed counterpart: 0

The 100% role and panel agreement reflects that v3 keeps v2's wording for every claim it
carries; the difference between the trees is the six reclassified sentences and the recorded
provenance, not the readings.

### v3 vs v1 (reference = runs/…/claim-tree.v1, candidate = claims/)

  committed 33   re-run 68

  RECOVERY  32/33 = 97%
  PRECISION 32/68 = 47%  (13 part-of)
  ROLE      26/32 = 81% of matched pairs
  PANEL     12/32 = 38% of matched pairs
  EDGES     15/83 ref edges recovered  (18%)  |  9 extra CLI edge(s)

  committed claims the re-run did not recover (2):
    hypothesis         hypothesis-responsibility-weights-partner-rpes
    literature-context interprets-yu-koban-guilt-signature

  re-run claims with no committed counterpart: 36

v1 was 33 claims from an unrecorded March-2026 process; v3 recovers all but two of them and
adds 36 more, so precision against v1 is low by construction — v3 is a far denser tree than
the one it descends from, not a divergent reading of the same paper.
