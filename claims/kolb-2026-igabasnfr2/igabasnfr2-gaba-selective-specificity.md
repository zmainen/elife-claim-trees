---
uuid: 669554c3-7a4d-453b-b9bd-893e935e630c
slug: igabasnfr2-gaba-selective-specificity
doi: ~
claim: >
  iGABASnFR2 displays high selectivity for GABA over structurally related compounds, none of which interfere with GABA binding as competitive or non-competitive antagonists at 1 mM concentrations.
claim-type: empirical
role: control
concepts:
  - iGABASnFR2
  - GABA selectivity
  - neurotransmitter specificity
  - off-target binding
priority: 2026-03-30
epistemic: strong

validates:
  - igabasnfr2-retina-direction-selectivity
  - igabasnfr2-single-bouton-hippocampus
  - igabasnfr2-invivo-barrel-cortex
rules-out:
  - igabasnfr2-fourfold-sensitivity-gain

belongings: []

assertions:
  - paper-slug: kolb-2026-igabasnfr2
    doi: 10.7554/eLife.108319
    panel: fig4-supplement1, fig4-supplement2
    figureUri: https://iiif.elifesciences.org/lax/108319%2Felife-108319-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: Zenodo analysis code
    dataset: https://doi.org/10.5281/zenodo.17971101
    dataset-doi: 10.5281/zenodo.17971101
    method: fluorescence titration with GABA-related compounds; competition assay with 1 mM competitor + increasing GABA
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    notes: >
      Specificity data from purified protein titrations (n≥3 replicates per compound). Compounds tested include structurally related amino acids and histamine. Source data on Zenodo. Wet lab not feasible without purified protein.
---

The specificity assessment covers compounds tested by titration up to concentrations far exceeding physiological levels. The competition assay (Fig 4—supplement 2) confirms that none of the tested compounds act as strong non-competitive allosteric antagonists or inhibitors of GABA binding, even at 1 mM. The paper notes that the apparent EC50 in competition conditions was similar to other assay conditions despite a different dose-response curve shape — a discrepancy flagged as unresolved.
