---
uuid: 7ca6bb4e-6e66-47c1-bf7c-52c64d17d80d
slug: context-specificity-predicts-acquisition-reinstatement-regional-dissociation
doi: ~
claim: >
  Higher reversal context specificity (PFC) interacts with CS type to predict generalized
  reinstatement of acquisition memory traces in ACC/SFG (favoring initially threatening CS+-,
  t(22)=6.25, p<0.05) and precuneus (favoring initially safe CS-+, t(22)=4.89, p<0.01),
  with opposite directions across regions.
claim-type: empirical
role: empirical
concepts:
  - context specificity
  - acquisition memory traces
  - ACC
  - precuneus
  - generalized reinstatement
  - individual differences
priority: 2026-03-30
epistemic: moderate

validates:
  - hypothesis-context-specificity-supports-renewal

belongings:
  - relation: requires
    target: context-specificity-increases-reversal
  - relation: supports
    target: pfc-context-specificity-predicts-renewal

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig5Di
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig5-v1.tif/full/1500,/0/default.jpg
    analysis: roi_lme_analysis.R, master_stats.R
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: LME with context specificity × CS type interaction predicting generalized reinstatement; FDR correction within ROI pairs
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: n=22-24; small sample for an individual-differences LME with interaction; effect sizes not reported
---

The opposite directions in ACC/SFG vs precuneus are noteworthy: context specificity predicts more reinstatement of originally-threatening (CS+-) traces in ACC/SFG but more reinstatement of originally-safe (CS-+) traces in precuneus. The paper reports this as a regional dissociation in how context specificity routes memory competition, but with n~22 the interaction is vulnerable to noise. The t-statistics (6.25 and 4.89) are large for this sample size, which may reflect LME degree-of-freedom estimation (Satterthwaite) yielding df=22 rather than a conventional t-test.
