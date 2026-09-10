---
uuid: 711a9296-c951-4455-b0bb-99e3d48ab36e
slug: context-specificity-predicts-reversal-reinstatement-dmpfc
doi: ~
claim: >
  Higher reversal context specificity (PFC) predicts greater item reinstatement of CS-+ than
  CS+- reversal memory traces in dmPFC during test_old (t(22)=5.56, p<0.05), favoring
  reinstatement of threatening reversal memories in the same region that generalizes acquisition
  traces.
claim-type: empirical
role: empirical
concepts:
  - context specificity
  - reversal memory traces
  - dmPFC
  - item reinstatement
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
  - relation: extends
    target: dmpfc-reinstates-acquisition-traces-generalized

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig5Dii
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig5-v1.tif/full/1500,/0/default.jpg
    analysis: roi_lme_analysis.R, master_stats.R
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: LME with context specificity × CS type interaction predicting item reinstatement; FDR correction within ROI pairs
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: ~
---

dmPFC appears in both fig4B (generalized acquisition reinstatement) and fig5Dii (item reversal reinstatement predicted by context specificity). These are two different dependent variables, so the same region can host both effects — but the co-occurrence raises a question about whether these are truly independent measurements or correlated across participants. The paper does not report this correlation.
