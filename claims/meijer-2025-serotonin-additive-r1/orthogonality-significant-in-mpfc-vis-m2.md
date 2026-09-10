---
uuid: 47d9bcc6-5d0f-4f6b-826d-c6638e2069d8
slug: orthogonality-significant-in-mpfc-vis-m2
doi: ~
claim: >
  When the manifold orthogonality analysis is computed per region at the last time point
  before the choice moment, the orthogonality between the 5-HT effect axis and the choice
  axis is significantly above the shuffle null distribution in three regions: medial
  prefrontal cortex (mPFC), visual cortex (VIS), and supplementary motor area (M2). Other
  recorded regions did not reach per-region significance at this timepoint, although the
  pooled-super-session result holds at the population level.
displayClaim: >
  Per-region orthogonality at the last pre-choice timepoint reaches significance in mPFC,
  visual cortex, and supplementary motor area.
claim-type: empirical
role: empirical
concepts:
  - per-region analysis
  - mPFC
  - visual cortex
  - supplementary motor area
  - orthogonality
priority: 2026-04-20
epistemic: moderate

belongings:
  - relation: requires
    target: manifold-from-pooled-super-session
  - relation: requires
    target: 5ht-axis-orthogonal-to-choice-axis

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig6f
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: per-region manifold analysis at last pre-choice time bin, permutation testing against block-aware null
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

Carries over from v1 unchanged in substance; figure renumbered from v1 Fig. 5i to R1 Fig. 6f because R1 inserts a new Fig. 3 for the receptor-expression GLM. The three regions that reach per-region significance — mPFC, VIS, M2 — are also the regions with the strongest choice separation in the same analysis, which makes structural sense: orthogonality between two vectors is most cleanly measurable when both vectors have appreciable magnitude. The non-significant regions either lack a strong per-region choice axis or have low neuron counts after per-region splitting.

Under R1's additivity framing, this per-region result has a particular interpretive role: it shows that the additive-modulation signature (in its geometric form) holds in the regions where the task computation is most strongly represented. This is consistent with the additive mechanism being general rather than localized to non-task-encoding regions. The R1 reconciliation hypothesis `reconciles-5ht1a-baseline-suppression-with-5ht2a-gain-control` would predict that visual cortex specifically might show some 5-HT2A gain-modulation signature, which the orthogonality result here does not test directly — orthogonality holds in visual cortex within the limits of this 3-D PCA analysis, but a multiplicative gain component below the noise floor would not be ruled out.
