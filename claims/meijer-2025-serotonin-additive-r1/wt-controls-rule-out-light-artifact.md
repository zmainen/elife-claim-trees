---
uuid: daf9cbad-8a15-458b-ab7f-30b397330a18
slug: wt-controls-rule-out-light-artifact
doi: ~
claim: >
  Wild-type control mice (n = 6) show baseline relative DRN/control fluorescence
  (no significant elevation over the in-slice control region) and chance-level (~5%)
  significant 5-HT-stimulation modulation, against the 10–60% in SERT-Cre mice. The light
  delivery and behavioral handling are otherwise identical between WT and SERT-Cre cohorts.
  This rules out direct optogenetic-light-driven artifacts (heat, retinal stimulation,
  electrical artifacts on probe channels), non-specific viral effects, and behavioral
  artifacts of fiber implantation as the explanation of the modulation findings.
displayClaim: >
  Wild-type controls (n = 6) show no DRN expression and chance-level (~5%) modulation —
  ruling out light artifact, non-specific viral effects, and implantation-related
  artifacts.
claim-type: empirical
role: control
concepts:
  - control experiment
  - wild-type controls
  - construct validity
  - light artifact
priority: 2026-04-20
epistemic: strong

belongings: []

scopes:
  - 5ht-modulates-all-recorded-regions-bidirectionally
  - 5ht-stim-dilates-pupil
  - 5ht-stim-increases-exploratory-behaviors

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig1c, fig2f
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: identical optogenetic protocol applied to non-SERT-Cre wild-type mice (n=6) with histological confirmation of absent ChR2 expression and per-neuron ZETA-test modulation analysis
    confidence: strong
    
reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

Carries over from v1 unchanged. The WT control cohort is essential for every claim that rests on the optogenetic-modulation effect being 5-HT-mediated rather than artifactual.
