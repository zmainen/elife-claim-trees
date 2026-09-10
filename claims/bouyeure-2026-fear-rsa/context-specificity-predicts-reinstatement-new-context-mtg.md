---
uuid: d0bcf69c-c791-4b94-9d82-92a43bccc4ed
slug: context-specificity-predicts-reinstatement-new-context-mtg
doi: ~
claim: >
  Higher reversal context specificity (PFC) predicts greater item reinstatement of CS-+ than
  CS+- acquisition memory traces in MTG during test_new (t(22)=2.51, p<0.05), the phase with
  entirely new contexts, suggesting context specificity generalizes beyond the training context.
claim-type: empirical
role: control
concepts:
  - context specificity
  - test new contexts
  - MTG
  - item reinstatement
  - generalization
priority: 2026-03-30
epistemic: weak

belongings:
  - relation: requires
    target: context-specificity-increases-reversal
  - relation: extends
    target: context-specificity-predicts-reversal-reinstatement-dmpfc

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig5Diii
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig5-v1.tif/full/1500,/0/default.jpg
    analysis: roi_lme_analysis.R, master_stats.R
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: LME with context specificity × CS type interaction predicting item reinstatement in MTG during test_new
    confidence: weak

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: ~
---

The paper labels this a control analysis ("as a control, we also analyzed reinstatement during the test_new phase") but then reports a significant effect that complicates interpretation. Context specificity during reversal predicting reinstatement in new contexts is somewhat paradoxical — new contexts should not benefit from reversal-phase context specificity. The paper's discussion does not fully resolve this. Weakest of the context-specificity claims (t=2.51, borderline significant, exploratory ROI).
