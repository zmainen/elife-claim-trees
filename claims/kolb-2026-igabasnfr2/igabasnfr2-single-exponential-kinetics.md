---
uuid: 837eae22-f6f6-4d29-9696-c998ee633b7f
slug: igabasnfr2-single-exponential-kinetics
doi: ~
claim: >
  iGABASnFR2 and iGABASnFR2n display single-exponential stopped-flow kinetics, whereas iGABASnFR1 exhibits biphasic kinetics; the observed reaction rate constants (Kobs) are far greater for both v2 sensors than for iGABASnFR1.
claim-type: empirical
role: empirical
concepts:
  - iGABASnFR2
  - stopped-flow kinetics
  - kon
  - binding kinetics
  - iGABASnFR1 comparison
priority: 2026-03-30
epistemic: strong

confirms:
  - hypothesis-saturation-mutagenesis-yields-improved-sensor
dissociates-with:
  - igabasnfr2-kinetics-rise-decay

belongings:
  - relation: supports
    target: igabasnfr2-fourfold-sensitivity-gain

assertions:
  - paper-slug: kolb-2026-igabasnfr2
    doi: 10.7554/eLife.108319
    panel: fig4c, fig4d
    figureUri: https://iiif.elifesciences.org/lax/108319%2Felife-108319-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: Zenodo analysis code
    dataset: https://doi.org/10.5281/zenodo.17971101
    dataset-doi: 10.5281/zenodo.17971101
    method: stopped-flow fluorescence spectroscopy; monoexponential fits in MATLAB
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    notes: >
      Stopped-flow measurements require purified protein (expressed in E. coli) and an Applied Photophysics SX20 stopped-flow spectrometer. n=3 replicates from three separate protein batches. Source data on Zenodo. Wet lab not feasible without purified protein and instrument.
---

The transition from biphasic to single-exponential kinetics in the v2 sensors suggests a simplification of the ligand-binding mechanism — the paper interprets this as "a less complex relationship between ligand binding and changes in fluorescence." The paper notes that iGABASnFR2 kinetics remain slower than iGluSnFR3, identifying kinetics as a remaining engineering target.
