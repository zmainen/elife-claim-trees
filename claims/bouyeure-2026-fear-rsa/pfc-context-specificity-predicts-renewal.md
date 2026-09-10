---
uuid: 2ff7f5ea-efaf-408e-9ef3-ab46fe395e74
slug: pfc-context-specificity-predicts-renewal
doi: ~
claim: >
  Prefrontal cortex context-specificity during reversal learning predicts subsequent fear renewal at test, linking context-specific neural coding to behavioral expression of fear.
claim-type: empirical
role: empirical
concepts:
  - prefrontal cortex
  - context specificity
  - fear renewal
  - prediction
  - individual differences
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-pfc-context-specificity-tracks-renewal

belongings:
  - relation: requires
    target: context-specificity-increases-reversal
  - relation: supports
    target: hypothesis-context-specificity-supports-renewal

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: ~
    panel: fig5
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig5-v1.tif/full/1500,/0/default.jpg
    analysis: roi_lme_analysis.R, master_stats.R
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: "correlation: RSA context specificity × behavioral fear renewal"
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      R analysis scripts. Not yet executed.
---
