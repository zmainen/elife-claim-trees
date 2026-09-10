---
uuid: 4a9fe28d-cf62-4539-98f9-0f0e00126047
slug: prediction-5ht-axis-orthogonal-to-choice
doi: ~
claim: >
  If brain-wide 5-HT modulation is structurally separable from the choice computation, then
  in a low-dimensional projection of the population response (here, the first three
  principal components), the vector that separates 5-HT-stimulated from unstimulated trials
  should be near-orthogonal to the vector that separates left-choice from right-choice
  trials, with orthogonality measured as 1 - |dot product| of unit-normalized direction
  vectors.
displayClaim: >
  The orthogonal-subspace hypothesis predicts that the 5-HT effect direction in PCA space
  should be near-orthogonal to the choice direction.
claim-type: prediction
role: prediction
concepts:
  - principal components analysis
  - subspace geometry
  - choice axis
  - 5-HT effect axis
  - orthogonality measure
priority: 2026-04-19
epistemic: prediction
status: confirmed
panel: prediction

derived-from:
  - hypothesis-orthogonal-neuromodulatory-subspace

belongings: []

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: prediction
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: derived prediction
    confidence: strong

reproductions: []
---

The prediction is mathematically specific: the choice axis is defined in 3-D PCA space as the displacement between mean-left and mean-right trajectories (averaged over stimulation condition); the 5-HT axis is defined as the displacement between mean-stimulated and mean-unstimulated trajectories (averaged over choice). The hypothesis predicts these two unit-normalized directions should have a near-zero dot product. The orthogonality measure (1 - |dot product|) ranges 0 to 1 with 1 being fully orthogonal. The prediction is confirmed empirically by `5ht-axis-orthogonal-to-choice-axis` (Fig. 5h shows the measure significantly above shuffle null; the regional analysis in Fig. 5i shows it significant in mPFC, VIS, M2). This confirmation is what licenses the paper's central interpretive claim about state-dependent representations.
