---
uuid: cf85076a-1b1f-462c-ac7a-e6bd64306681
slug: orthogonality-significant-in-mpfc-vis-m2
doi: ~
claim: >
  When the manifold orthogonality analysis is repeated separately for each brain region, at
  the last time point before the choice moment, the orthogonality between the 5-HT effect
  axis and the choice axis significantly exceeds the shuffle null distribution in three
  regions: medial prefrontal cortex, visual cortex, and supplementary motor area (M2). Other
  regions either lack significant choice or 5-HT separation (and so cannot be tested) or
  show non-significant orthogonality.
displayClaim: >
  Per-region, orthogonality between 5-HT and choice axes is significant in medial prefrontal
  cortex, visual cortex, and supplementary motor area at the pre-choice timepoint.
claim-type: empirical
role: empirical
concepts:
  - regional dissociation
  - medial prefrontal cortex
  - supplementary motor area
  - visual cortex
  - per-region manifold
priority: 2026-04-20
epistemic: moderate

belongings:
  - relation: requires
    target: 5ht-axis-orthogonal-to-choice-axis
  - relation: requires
    target: manifold-from-pooled-super-session
  - relation: supports
    target: hypothesis-orthogonal-neuromodulatory-subspace

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: fig5i
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: per-region manifold analysis at last pre-choice timepoint, permutation test against block-aware null
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-04-20
    status: unverified
    notes: ~
---

The regional decomposition of the orthogonality result is informative. mPFC is the most striking case: it shows simultaneously the strongest choice separation (Fig. 5c) and a significant 5-HT separation (Fig. 5f), and it shows significant orthogonality between the two — making it the clearest single-region demonstration of the central hypothesis. M2 and VIS provide independent confirmation in regions with different functional roles. Notably, regions like the hippocampus (which show strong 5-HT effects in passive condition) or the striatum do not show significant orthogonality in this per-region test — either because they don't show clear choice-axis structure (hippocampus during a perceptual task) or because their effective dimensionality is different. The non-uniform distribution of significance is consistent with the orthogonality property being a feature of cortical task-coding regions specifically, rather than a universal property of the brain-wide response.
