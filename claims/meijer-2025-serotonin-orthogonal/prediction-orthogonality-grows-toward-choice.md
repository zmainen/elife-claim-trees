---
uuid: 4f28c881-0692-4fcf-8595-2f4bcd0716af
slug: prediction-orthogonality-grows-toward-choice
doi: ~
claim: >
  If the 5-HT modulation specifically avoids the choice readout dimension as that dimension
  becomes informative, then the orthogonality between the 5-HT axis and the choice axis
  should not be constant — it should grow over the trial timecourse, becoming maximal in the
  hundreds of milliseconds leading up to the choice moment, when the choice axis has
  separated maximally and the readout demand is greatest.
displayClaim: >
  Orthogonality between 5-HT and choice axes should grow as the choice moment approaches —
  the modulation should clear out of the readout dimension when the readout is needed.
claim-type: prediction
role: prediction
concepts:
  - dynamic subspace geometry
  - choice readout
  - temporal evolution
  - peri-choice neural dynamics
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
    confidence: moderate

reproductions: []
---

This is a stronger and more specific prediction than the static one. A trivially-orthogonal modulation would just live in some random direction in the population manifold; what the hypothesis predicts is that orthogonality is *organized in time* — it tracks the emergence of the choice axis itself. Empirically, Fig. 5h shows the orthogonality measure rising over the seconds leading up to the choice moment. The paper does not provide a formal statistical test of the *increase* itself (only that the value at each timepoint exceeds shuffle), so the temporal-growth aspect is supported descriptively rather than tested as a slope. This is the load-bearing single-source aspect of the orthogonality finding most worth flagging.
