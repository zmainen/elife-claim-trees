---
uuid: f2fccd5f-8ee8-4138-9e97-055ebda75cd8
slug: igabasnfr2-invivo-barrel-cortex
doi: ~
claim: >
  iGABASnFR2 detects volume-transmitted extracellular GABA signals in vivo in mouse barrel cortex (layers L2–L3, ~300 μm depth) evoked by rhythmic whisker stimulation, corresponding to a transient GABA concentration increase of approximately 2–2.5 μM at peak.
claim-type: empirical
role: empirical
concepts:
  - iGABASnFR2
  - in vivo imaging
  - barrel cortex
  - whisker stimulation
  - volume transmission
  - GABA
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-improved-sensor-enables-new-measurements
confirms:
  - hypothesis-improved-sensor-enables-new-biology
dissociates-with:
  - igabasnfr2-retina-direction-selectivity
  - igabasnfr2-single-bouton-hippocampus

belongings:
  - relation: supports
    target: igabasnfr2-fourfold-sensitivity-gain
  - relation: requires
    target: igabasnfr2-2p-compatible

assertions:
  - paper-slug: kolb-2026-igabasnfr2
    doi: 10.7554/eLife.108319
    panel: fig6c, fig6-video1
    figureUri: https://iiif.elifesciences.org/lax/108319%2Felife-108319-fig6-v1.tif/full/1500,/0/default.jpg
    analysis: Zenodo analysis code
    dataset: https://doi.org/10.5281/zenodo.17971101
    dataset-doi: 10.5281/zenodo.17971101
    method: in vivo 2P Tornado scanning (1 kHz resonant scan); AAV9-hSyn-iGABASnFR2 cortical injection; rhythmic whisker stimulation (4 air puffs at 20 Hz, 200 ms)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    notes: >
      Single-trial ΔF/F₀ shown in Fig 6c (no group statistics reported beyond prior slice calibration). GABA concentration estimate (~2–2.5 μM) is derived from prior calibration by Magloire et al. (2023), not directly measured in this experiment. Requires in vivo 2P setup and cranial window surgery. Epistemic rated moderate because the concentration estimate is calibration-derived, not directly measured.
---

The GABA concentration estimate rests on a calibration from Magloire et al. (2023), making it an inferential rather than direct measurement — hence moderate epistemic strength. The physiological interpretation (volume-transmitted signal from interneuron bursts diffusing tens of microns from release sites) is consistent with the spatial extent observed (~150 μm-wide area). This is the only in vivo neural circuit measurement in the paper; all other in vivo claims refer to purified protein or cultured neuron assays.
