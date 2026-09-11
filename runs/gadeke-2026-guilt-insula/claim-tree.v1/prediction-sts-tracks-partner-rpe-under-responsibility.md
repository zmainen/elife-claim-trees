---
uuid: 52a693d9-fa42-4b84-8e27-7c77ef16022f
slug: prediction-sts-tracks-partner-rpe-under-responsibility
doi: ~
claim: >
  If superior temporal sulcus represents the partner's affective experience selectively
  under responsibility, then in a model-based GLM with trial-by-trial partner RPE
  regressors split by who-chose, the parametric modulator for partner RPE in Social
  trials (subject-decided) should yield a significant cluster in left STS, while the
  parametric modulator for partner RPE in Partner trials (partner-decided) should not.
  This conditional engagement, rather than a main effect of partner RPE, is the
  diagnostic prediction.
displayClaim: >
  The mentalizing-under-responsibility hypothesis predicts that left STS tracks
  partner reward prediction errors specifically when the participant is responsible
  for the choice — a parametric modulator that is significant in Social but not in
  Partner trials.
claim-type: prediction
role: prediction
concepts:
  - superior temporal sulcus
  - partner RPE
  - responsibility
  - model-based fMRI
  - parametric modulator
priority: 2026-04-20
epistemic: prediction
status: N/A
panel: prediction

derived-from:
  - hypothesis-sts-mentalizes-partner-state-under-responsibility

belongings: []

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: prediction
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: derived prediction
    confidence: moderate

reproductions: []
---

This prediction is structurally dependent on the responsibility model fitting (`prediction-responsibility-model-wins-comparison`), since it requires trial-by-trial partner RPE regressors derived from that model. It is also dependent on the manipulation check provided by `ventral-striatum-tracks-computational-reward` — if GLM2 fails to recover the canonical ventral-striatum reward signal, the absence of an STS effect would be uninterpretable. The conditional-engagement form of the prediction (Social-yes, Partner-no) is what distinguishes a mentalizing-under-responsibility account from a generic "STS tracks others' outcomes" account; a main-effect finding would not adjudicate. Tested by `sts-tracks-partner-reward-prediction-errors` (fig4H).
