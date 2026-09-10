---
uuid: ec7c50b1-ca2a-4704-ab2d-c17def3b6de1
slug: prediction-5ht-axis-orthogonal-to-choice
doi: ~
claim: >
  If brain-wide 5-HT modulation is structurally separable from the choice computation
  (under additive modulation), then in a low-dimensional projection of the population
  response (here, the first three principal components), the vector that separates
  5-HT-stimulated from unstimulated trials should be near-orthogonal to the vector that
  separates left-choice from right-choice trials, with orthogonality measured as
  1 - |dot product| of unit-normalized direction vectors.
displayClaim: >
  Under additive modulation, the 5-HT effect direction in PCA space should be near-orthogonal
  to the choice direction.
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
  - orthogonality-derived-from-additivity

belongings: []

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: prediction
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: derived prediction
    confidence: strong

reproductions: []
---

Carries over from v1 with one structural change: the prediction now derives from both the orthogonal-subspace hypothesis directly (as in v1) *and* from the additivity hypothesis via the geometric corollary `orthogonality-derived-from-additivity`. The two derivations are not independent — under R1's reframing, the orthogonal-subspace hypothesis is itself derived from additivity, so the orthogonality prediction is mathematically a consequence of additivity in any case. The dual `derived-from` link encodes the fact that the prediction follows from either framing equivalently.

The prediction is confirmed empirically by `5ht-axis-orthogonal-to-choice-axis` (Fig. 5h shows the orthogonality measure significantly above shuffle null; the regional analysis in Fig. 5i shows it significant in mPFC, VIS, M2). Note that under R1's additivity framing, this confirmation is geometrically the same fact as the GLM near-zero interaction result (`near-zero-choice-by-stim-interaction`) — see `orthogonality-derived-from-additivity` for the derivation.
