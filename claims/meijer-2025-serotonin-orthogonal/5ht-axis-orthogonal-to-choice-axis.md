---
uuid: edaec7c9-e745-4a84-b73c-aea77cf4550b
slug: 5ht-axis-orthogonal-to-choice-axis
doi: ~
claim: >
  In the manifold analysis built from a pooled super-session of trial-averaged peri-event
  PETHs across all neurons, sessions, and mice, the 5-HT effect axis (defined as the
  displacement vector between mean stimulated and mean unstimulated trajectories in 3-D PCA
  space, averaged across choice) is significantly more orthogonal to the choice axis (the
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

belongings:
  - relation: requires
    target: manifold-from-pooled-super-session
  - relation: requires
    target: 5ht-modulates-all-recorded-regions-bidirectionally
  - relation: supports
    target: hypothesis-orthogonal-neuromodulatory-subspace

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: fig5g, fig5h
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: PCA on mean-subtracted PETH super-session, vector definitions of choice axis and 5-HT axis, orthogonality = 1 - |dot product|, null = block-aware pseudo-stimulation shuffles
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-20
    status: unverified
    notes: ~
---

This is the central empirical claim of the paper. Its strength rests on three structural choices: (1) the geometric definition of the choice and 5-HT axes is symmetric and pre-specified in the methods, not data-derived per timepoint; (2) the orthogonality measure is bounded [0, 1] and the test is a permutation against a block-aware null that preserves the temporal autocorrelation of stimulation blocks (a non-trivial methodological move that prevents spurious orthogonality from inflated effective N); (3) the temporal trajectory — orthogonality growing as the choice axis emerges — is descriptively consistent with the hypothesis but is not itself tested as a slope.

Two non-trivial concerns shape its epistemic boundary. First, the analysis is in only 3 PCA dimensions; high-dimensional populations may have additional structure that this projection misses. Second, the analysis pools across mice and sessions into a super-session — orthogonality is established at the population level, not per-animal, so within-animal variability is not characterized.
