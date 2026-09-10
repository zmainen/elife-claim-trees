---
uuid: 1b98cdbc-4ab1-41f6-932c-7efd46909363
slug: wt-controls-rule-out-light-artifact
doi: ~
claim: >
  Wild-type control mice (n=6), which received the same surgical procedure, optical fiber
  implantation, and optogenetic stimulation protocol but lack Cre-dependent ChR2 expression
  in DRN serotonergic neurons, show baseline-level DRN/control fluorescence ratio (Fig. 1c)
  and chance-level (~5%) significantly modulated neurons (Fig. 2f) — ruling out light
  delivery, optical-fiber heating, viral injection, surgical artifact, or other non-specific
  effects of the procedure as drivers of the observed pupil, ripple, and neural
  modulation effects.
displayClaim: >
  WT controls (n=6) lacking ChR2 show baseline fluorescence and only chance-level (~5%)
  modulated neurons — ruling out light, heat, surgical, or viral artifacts.
claim-type: empirical
role: control
concepts:
  - wild-type control
  - light artifact
  - optogenetic specificity
  - false-positive rate
priority: 2026-04-20
epistemic: strong

rules-out:
  - light-or-heat-mediated-modulation
validates:
  - 5ht-stim-dilates-pupil
  - 5ht-stim-suppresses-sharp-wave-ripples
  - 5ht-stim-increases-exploratory-behaviors
  - 5ht-modulates-all-recorded-regions-bidirectionally

belongings: []

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: fig1c, fig2f
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: SERT-Cre vs WT comparison; matched surgical, viral, and stimulation procedure
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-20
    status: unverified
    notes: ~
---

The WT control is the standard for this class of optogenetic experiment and is implemented at the right scale (n=6 WT vs n=11 SERT-Cre, comparable enough for a meaningful contrast). The fact that the SERT-vs-WT contrast is the basis for the pupil and ripple statistics (Fig. 1h, l) and that the WT modulated-neuron fraction lands at the chance-level expectation (5%) gives this a strong epistemic standing. The control rules out the most common confounds for fiber-implanted optogenetic experiments — light leak, fiber-tip heating, surgical inflammation — but does not rule out 5-HT-independent effects of strong glutamatergic drive at the DRN, or downstream consequences of glutamate co-release from SERT-Cre+ neurons. Those are addressed in the discussion as caveats rather than tested experimentally.
