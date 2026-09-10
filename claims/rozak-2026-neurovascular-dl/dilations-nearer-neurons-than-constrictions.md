---
uuid: c1381a0c-47be-4721-9022-ddec7d45b3fd
slug: dilations-nearer-neurons-than-constrictions
doi: ~
claim: >
  Following ChR2 optogenetic activation at 458 nm, capillary dilations occur on average
  16.1±14.3 µm from the nearest labeled pyramidal neuron while constrictions occur 21.9±14.6 µm
  away (4.3 mW/mm²; p<1e-4), and this spatial segregation is absent under control 552 nm
  illumination.
claim-type: empirical
role: empirical
concepts:
  - neurovascular coupling
  - spatial gradient
  - capillary dilation
  - capillary constriction
  - distance to neuron
  - ChR2 optogenetics
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-pipeline-reveals-network-coordination
confirms:
  - hypothesis-network-level-nvc-coordination
  - synthesis-individual-vessel-measurements-insufficient
dissociates-with:
  - constrictions-deeper-than-dilations

belongings:
  - relation: requires
    target: responder-threshold-2sd-untested
  - relation: supports
    target: network-assortativity-increases-stimulation

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    panel: fig8D
    figureUri: https://iiif.elifesciences.org/lax/95525%2Felife-95525-fig8-v1.tif/full/1500,/0/default.jpg
    analysis: Tutorial.ipynb
    dataset: https://doi.org/10.20383/103.01588
    dataset-doi: 10.20383/103.01588
    method: vertex-wise distance to YFP-labeled neuron; mixed-effects model; Wilcoxon test
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      The spatial gradient (dilations closer, constrictions farther) was significant at
      4.3 mW/mm² (p<1e-4) and 1.1 mW/mm² (p=1.5e-3). The 16.8±13.5 µm / 22.7±16.3 µm
      values apply to 1.1 mW/mm²; the 16.1±14.3 / 21.9±14.6 values apply to 4.3 mW/mm².
      No significant power-dependent shift in the distances themselves was detected between
      the two stimulation levels. Control condition (552 nm) showed no significant difference
      in dilator vs. constrictor distance to neuron.
---

This is the paper's primary biological claim about spatial organization of neurovascular coupling.
The interpretation is that vasodilatory signals (e.g., prostanoids, NO) diffuse from activated neurons
outward, and vessels close to the source dilate while the drain effect or vessel tone mechanisms
cause more distant vessels to constrict. This is consistent with a propagating vasoactive wave
but the paper does not demonstrate the mechanism, only the spatial pattern. The claim requires the
responder threshold (2×SD) because vessels below that threshold are excluded from the analysis.
