---
uuid: 0cdf69ab-ffa6-4e8b-a87b-e681ec8c2526
slug: screening-scope-wet-lab-only
doi: ~
claim: >
  The primary claims of iGABASnFR2 performance (sensitivity, kinetics, SNR) are established through wet-lab measurements (fluorescence imaging in cultured neurons, stopped-flow kinetics, two-photon excitation spectroscopy) that cannot be reproduced from deposited code and data alone; computational analysis of deposited source data covers only figure generation, not the underlying measurements.
claim-type: assessment
role: scope
concepts:
  - wet lab
  - stopped-flow kinetics
  - two-photon spectroscopy
  - reproduction barrier
priority: 2026-03-30
epistemic: strong

scopes:
  - mutagenesis-3947-variants-screened
  - igabasnfr2-fourfold-sensitivity-gain
  - igabasnfr2-13fold-expression-increase
  - igabasnfr2n-negative-going-variant
  - igabasnfr2-kinetics-rise-decay
  - igabasnfr2-cpgfp-rigid-on-gaba-binding
  - igabasnfr2-oncell-affinity-sevenfold
  - igabasnfr2-single-exponential-kinetics
  - igabasnfr2-2p-compatible
  - igabasnfr2-gaba-selective-specificity
  - igabasnfr2-retina-direction-selectivity
  - igabasnfr2-single-bouton-hippocampus
  - igabasnfr2-invivo-barrel-cortex

belongings: []

assertions:
  - paper-slug: kolb-2026-igabasnfr2
    doi: ~
    panel: all figures (assessment)
    analysis: code inspection
    dataset: ~
    dataset-doi: ~
    method: code inspection + corpus-assessment
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: verified
    notes: >
      Confirmed by corpus-assessment.md: reproduction difficulty rated Hard. Primary claims require sensor constructs and specialized equipment. Analysis code covers figure generation from pre-measured source data.
---
