---
uuid: e05b0913-66d9-4ac2-be33-40385aaf6181
slug: wt-controls-no-blue-green-difference
doi: ~
claim: >
  Wild-type C57BL/6J mice (n=4) show no statistically distinguishable capillary radius
  distributions following blue (458 nm) versus green (552 nm) photostimulation, confirming
  that vascular responses in Thy1-ChR2 mice are ChR2-specific and not attributable to
  photothermal or non-specific light effects.
claim-type: empirical
role: control
concepts:
  - wild-type control
  - ChR2 specificity
  - photothermal artifact
  - C57BL/6J
  - negative control
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-pipeline-reveals-network-coordination
confirms:
  - hypothesis-network-level-nvc-coordination
validates:
  - blue-light-dilations-exceed-green-control
  - dilations-nearer-neurons-than-constrictions
  - constrictions-deeper-than-dilations

belongings:
  - relation: supports
    target: blue-light-dilations-exceed-green-control
  - relation: supports
    target: dilations-nearer-neurons-than-constrictions

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    panel: app1fig9
    analysis: Tutorial.ipynb
    dataset: https://doi.org/10.20383/103.01588
    dataset-doi: 10.20383/103.01588
    method: Wilcoxon test on capillary radius distributions; n=4 C57BL/6J mice
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      n=4 wild-type mice is a small sample for a negative control, but the key result is
      the absence of a difference rather than presence, so the power concern is somewhat
      mitigated. The Wilcoxon test is appropriate for comparing distributions. The caption
      states the distributions "were not statistically distinguishable" — no p-value is
      reported in the main text or caption for the WT comparison itself.
---

This is the key negative control that distinguishes ChR2-mediated from light-mediated vascular
effects. The paper appropriately uses 552 nm (not absorbed by ChR2) as the within-Thy1-ChR2
control, and the WT comparison provides an additional cross-genotype check. The n=4 WT mice
is small but the result is directionally consistent: no response in mice lacking ChR2.
