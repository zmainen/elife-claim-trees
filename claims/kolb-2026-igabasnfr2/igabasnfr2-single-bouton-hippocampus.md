---
uuid: ff5506c7-eac9-42f7-8643-d38068feafd5
slug: igabasnfr2-single-bouton-hippocampus
doi: ~
claim: >
  iGABASnFR2 detects GABA release from individual hippocampal interneuron axonal boutons using Tornado scanning two-photon microscopy; iGABASnFR1 failed to produce any detectable spike-evoked fluorescence signal across 15 trials in five separate experiments.
claim-type: empirical
role: empirical
concepts:
  - iGABASnFR2
  - hippocampus
  - single bouton
  - Tornado scan
  - two-photon microscopy
  - interneuron
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-improved-sensor-enables-new-measurements
confirms:
  - hypothesis-improved-sensor-enables-new-biology
dissociates-with:
  - igabasnfr2-retina-direction-selectivity

belongings:
  - relation: supports
    target: igabasnfr2-fourfold-sensitivity-gain
  - relation: requires
    target: igabasnfr2-2p-compatible

assertions:
  - paper-slug: kolb-2026-igabasnfr2
    doi: 10.7554/eLife.108319
    panel: fig6a, fig6b
    figureUri: https://iiif.elifesciences.org/lax/108319%2Felife-108319-fig6-v1.tif/full/1500,/0/default.jpg
    analysis: Zenodo analysis code
    dataset: https://doi.org/10.5281/zenodo.17971101
    dataset-doi: 10.5281/zenodo.17971101
    method: simultaneous 2P Tornado scanning (1.5 μm scan path, 0.5–1 kHz) and whole-cell electrophysiology in acute hippocampal slices and organotypic cultures; biolistic transfection (CA3 interneurons) and viral delivery (CA1)
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    notes: >
      iGABASnFR1 result: 0 signals across 15 trials × 5 experiments. iGABASnFR2 result: consistent evoked signals; SNR>3 may require 5–10 trial averaging. Requires Femtonics 2P system, patch clamp rig, and AAV-injected mice or biolistically transfected organotypic cultures.
---

The negative iGABASnFR1 result (Fig 6a) is as important as the positive iGABASnFR2 result (Fig 6b): it documents a qualitative capability threshold crossed by the engineering. The method (Tornado scanning) was previously developed for glutamate sensors (Jensen et al., 2019) and is now applied to GABA imaging for the first time with a sensor sensitive enough to resolve individual bouton events.
