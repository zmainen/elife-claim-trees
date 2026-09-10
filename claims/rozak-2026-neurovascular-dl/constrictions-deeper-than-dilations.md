---
uuid: a3ca491f-f3b6-456f-b69c-6f9449183c4a
slug: constrictions-deeper-than-dilations
doi: ~
claim: >
  Constricting capillaries are located on average 37±179 µm deeper in cortex than dilating
  capillaries following 458 nm optogenetic stimulation at 4.3 mW/mm² (p<1e-4), with dilators
  tending toward the cortical surface across all stimulation conditions.
claim-type: empirical
role: empirical
concepts:
  - cortical depth
  - capillary dilation
  - capillary constriction
  - optogenetics
  - neurovascular coupling
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-pipeline-reveals-network-coordination
confirms:
  - hypothesis-network-level-nvc-coordination
dissociates-with:
  - dilations-nearer-neurons-than-constrictions

belongings:
  - relation: requires
    target: responder-threshold-2sd-untested
  - relation: supports
    target: dilations-nearer-neurons-than-constrictions

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    panel: fig8E
    figureUri: https://iiif.elifesciences.org/lax/95525%2Felife-95525-fig8-v1.tif/full/1500,/0/default.jpg
    analysis: Tutorial.ipynb
    dataset: https://doi.org/10.20383/103.01588
    dataset-doi: 10.20383/103.01588
    method: vertex-wise cortical depth from cortical surface; mixed-effects model
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      The 37±179 µm depth difference applies to 4.3 mW/mm² (p<1e-4). For 1.1 mW/mm², the
      difference was 58±187 µm deeper (p=0.02). There was no significant change in the mean
      depth of constricting or dilating vessels between the two stimulation power levels.
      The SD (179 µm) is very large relative to the mean (37 µm) — indicating this is a
      weak central tendency with substantial scatter, not a sharp laminar boundary.
---

The large SD relative to the effect size (37±179 µm) means this claim describes a statistical
tendency rather than a clean laminar dissociation. Layer 5 pyramidal neurons (Thy1-ChR2)
have somata in deep cortex and apical dendrites toward the surface — the depth gradient of
dilation/constriction may reflect proximity to either dendrites (surface) or somata (deep),
but the paper does not resolve which anatomical compartment drives the response.
