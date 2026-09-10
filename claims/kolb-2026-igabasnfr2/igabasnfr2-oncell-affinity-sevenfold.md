---
uuid: 10eb034c-f5b4-422e-a43b-8375a917111d
slug: igabasnfr2-oncell-affinity-sevenfold
doi: ~
claim: >
  iGABASnFR2 expressed on the surface of cultured neurons has an on-cell EC50 of 6.4 ± 0.21 μM for GABA, representing a sevenfold higher affinity than iGABASnFR1 (EC50 ~45 μM on-cell) while remaining above the tonic extracellular GABA concentration range of 0.2–2.5 μM in the mammalian brain.
claim-type: empirical
role: empirical
concepts:
  - iGABASnFR2
  - GABA affinity
  - EC50
  - on-cell titration
  - tonic GABA
priority: 2026-03-30
epistemic: strong

confirms:
  - hypothesis-saturation-mutagenesis-yields-improved-sensor
dissociates-with:
  - igabasnfr2-fourfold-sensitivity-gain

belongings:
  - relation: supports
    target: igabasnfr2-fourfold-sensitivity-gain
  - relation: extends
    target: igabasnfr2-fourfold-sensitivity-gain

assertions:
  - paper-slug: kolb-2026-igabasnfr2
    doi: 10.7554/eLife.108319
    panel: fig4b
    figureUri: https://iiif.elifesciences.org/lax/108319%2Felife-108319-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: Zenodo analysis code
    dataset: https://doi.org/10.5281/zenodo.17971101
    dataset-doi: 10.5281/zenodo.17971101
    method: on-cell fluorescence titration; GABA perfusion onto cultured neurons
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    notes: >
      On-cell titration requires sensor-expressing neurons and perfusion system. Source data on Zenodo covers dose-response curves. Wet lab reconstruction not feasible without constructs. Analysis of deposited source data not yet executed.
---

The on-cell EC50 of 6.4 μM contrasts with the purified-protein EC50 of 1.1 μM (Fig 4a), a discrepancy the paper notes but does not resolve mechanistically. The paper cites a similar observation with iGluSnFR (Aggarwal et al., 2023) and treats the on-cell value as a better predictor of in vivo performance because it reflects the membrane-bound operating environment. The 22-fold improvement relative to iGABASnFR.F102PfG (the prior highest-sensitivity mutant) is a key quantitative landmark in the series.
