---
uuid: a95a99d0-5af2-4711-8941-be2d0713688c
slug: 5ht-axis-orthogonal-to-choice-axis
doi: ~
claim: >
  In the manifold analysis built from a pooled super-session of trial-averaged peri-event
  PETHs across all neurons, sessions, and mice, the 5-HT effect axis (the displacement
  vector between mean stimulated and mean unstimulated trajectories in 3-D PCA space,
  averaged across choice) is significantly more orthogonal to the choice axis (the
  displacement between mean left and mean right trajectories, averaged across stimulation)
  than expected from a block-aware shuffle null distribution. The orthogonality measure
  (1 - |dot product| of unit-normalized direction vectors) increases over the pre-choice
  timecourse and is significant in the time window approaching the choice moment.
displayClaim: >
  In the pooled super-session manifold, the 5-HT effect direction in PCA space is
  significantly more orthogonal to the choice direction than shuffle null, and orthogonality
  grows toward the choice moment.
claim-type: empirical
role: empirical
concepts:
  - principal components analysis
  - subspace geometry
  - choice axis
  - orthogonality
  - super-session manifold
priority: 2026-04-20
epistemic: strong

confirms:
  - prediction-5ht-axis-orthogonal-to-choice
  - prediction-orthogonality-grows-toward-choice
supports:
  - hypothesis-orthogonal-neuromodulatory-subspace
  - hypothesis-additive-modulation

belongings:
  - relation: requires
    target: manifold-from-pooled-super-session
  - relation: requires
    target: 5ht-modulates-all-recorded-regions-bidirectionally
  - relation: supports
    target: hypothesis-orthogonal-neuromodulatory-subspace

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig6d, fig6e
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: PCA on mean-subtracted PETH super-session, vector definitions of choice axis and 5-HT axis, orthogonality = 1 - |dot product|, null = block-aware pseudo-stimulation shuffles
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

Carries over from v1. Under R1's framing, this empirical result and the GLM near-zero interaction `near-zero-choice-by-stim-interaction` are not statistically independent — they are two operationalizations of the same underlying additivity property under linear (PCA) projection in the 2×2 factorial design. See `orthogonality-derived-from-additivity` for the mathematical equivalence. The two claims are kept as separate nodes because they are computed from different analyses with different statistical tests (manifold permutation vs. across-animal t-test), but they should not be combined as if they were independent confirmations.

The structural concerns from v1 still apply: the analysis is in 3 PCA dimensions only, and pools across mice and sessions into a super-session, so orthogonality is established at the population level rather than per-animal. The R1 reframing does not change these methodological characteristics. Note that the figure containing this analysis was renumbered in R1 from v1's Fig. 5 to R1's Fig. 6 (because R1 inserts a new Fig. 3 for the receptor-expression GLM analysis).
