---
uuid: a68ebd2f-95bf-43a9-b0e0-f9ce7a3fa5bd
slug: blue-light-dilations-exceed-green-control
doi: ~
claim: >
  Capillary dilations following 458 nm ChR2 stimulation (0.90±0.93 µm at 1.1 mW/mm²;
  0.90±0.78 µm at 4.3 mW/mm²) are significantly larger than those following 552 nm control
  illumination (0.58±0.92 µm; p<1e-4), confirming that the vascular responses are
  ChR2-mediated rather than photothermal artifacts.
claim-type: empirical
role: control
concepts:
  - ChR2 specificity
  - optogenetic control
  - capillary dilation
  - photothermal artifact
  - neurovascular coupling
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-pipeline-reveals-network-coordination
validates:
  - dilations-nearer-neurons-than-constrictions
  - constrictions-deeper-than-dilations
  - vessel-radius-heterogeneity-stimulation
  - network-assortativity-increases-stimulation
  - capillary-efficiency-increases-4pct

belongings:
  - relation: requires
    target: wt-controls-no-blue-green-difference
  - relation: supports
    target: dilations-nearer-neurons-than-constrictions

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    panel: fig8A
    figureUri: https://iiif.elifesciences.org/lax/95525%2Felife-95525-fig8-v1.tif/full/1500,/0/default.jpg
    analysis: Tutorial.ipynb
    dataset: https://doi.org/10.20383/103.01588
    dataset-doi: 10.20383/103.01588
    method: mixed-effects model on responder vessel radius changes; Wilcoxon signed-rank
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      Constriction responses: 458 nm at 1.1 mW/mm² produced –1.39±1.51 µm, at 4.3 mW/mm²
      produced –1.20±1.13 µm; 552 nm control produced –0.37±0.30 µm (smaller, p=0.02).
      The stimulation power comparison (1.1 vs 4.3 mW/mm² at 458 nm) was not significant
      for dilations; constrictions were significantly different (p=4.4e-3). Note: dilation
      magnitude did not increase with power, suggesting response saturation.
---

This claim is important for attributing the vascular responses to neuronal activation rather
than direct photothermal effects of the laser. The 552 nm control should not activate ChR2
(absorption peak ~470 nm) but does generate the same photon flux and thermal load. The
supplementary wild-type C57BL/6J comparison (Appendix 1—figure 9) strengthens this further:
WT mice show no statistically distinguishable radius distributions between blue and green
illumination, consistent with the responses being ChR2-specific.
