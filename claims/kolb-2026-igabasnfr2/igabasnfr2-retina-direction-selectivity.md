---
uuid: 808a0591-b637-4f1a-9ff9-e05e779644bf
slug: igabasnfr2-retina-direction-selectivity
doi: ~
claim: >
  iGABASnFR2 directly demonstrates direction-selective GABA release from starburst amacrine cells in the intact retina, with significantly higher SNR and response reliability than iGABASnFR1; iGABASnFR1 signals were insufficient to detect direction selectivity even after trial-averaging.
claim-type: empirical
role: empirical
concepts:
  - iGABASnFR2
  - retina
  - direction selectivity
  - starburst amacrine cell
  - GABA release
  - two-photon imaging
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-improved-sensor-enables-new-measurements
confirms:
  - hypothesis-improved-sensor-enables-new-biology
dissociates-with:
  - igabasnfr2-single-bouton-hippocampus

belongings:
  - relation: supports
    target: igabasnfr2-fourfold-sensitivity-gain
  - relation: requires
    target: igabasnfr2-2p-compatible

assertions:
  - paper-slug: kolb-2026-igabasnfr2
    doi: 10.7554/eLife.108319
    panel: fig5
    figureUri: https://iiif.elifesciences.org/lax/108319%2Felife-108319-fig5-v1.tif/full/1500,/0/default.jpg
    analysis: Zenodo analysis code
    dataset: https://doi.org/10.5281/zenodo.17971101
    dataset-doi: 10.5281/zenodo.17971101
    method: two-photon imaging in excised retina; Cre-Lox AAV delivery in ChAT-IRES-Cre mice; moving spot and full-field flash stimuli
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    notes: >
      n=147 ROIs from five retinae (iGABASnFR1), n=346 ROIs from three retinae (iGABASnFR2). SNR comparison: p=0 (Mann-Whitney-Wilcoxon). Direction selectivity (CV): p=7.812×10⁻⁶. Mean response reliability iGABASnFR2: 0.66±0.14 vs iGABASnFR1: 0.41±0.11. Requires retinal preparation, 2P microscope, and AAV-injected mice.
---

This is the primary biological demonstration of Fig 5 and serves as the key scientific advance claim in the paper: the improvement is not merely a fold-change in a screening assay but enables a measurement — direction-selective GABA release — that was previously inaccessible. iGABASnFR1 produced signals too weak for single-trial detection; iGABASnFR2 enabled single-trial detection of both static flash and motion responses. The direction selectivity result (lower circular variance with iGABASnFR2) provides direct evidence for the long-hypothesized but unconfirmed centrifugal GABA release hypothesis in starburst cells.
