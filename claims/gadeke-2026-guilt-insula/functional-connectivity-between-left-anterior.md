---
uuid: bd115e8c-ec7a-4e6f-8b10-9ee16c17f4b1
slug: functional-connectivity-between-left-anterior
doi: null
claim: Functional connectivity between the left anterior insula (seed) and a cluster in the right inferior
  frontal gyrus varied with condition and choice, being highest when participants made Risky choices for
  themselves and Safe choices for both players (pFWE = 0.020, T = 4.34, d = 0.80, 115 voxels, peak MNI
  [46 16 22]).
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-13'
epistemic: tentative
warrant: weak
warrant_why: the tree records no reproduction, control or test bearing on this PPI result
tests:
- connectivity-between-guilt-responsibility-related-outcome-ph
confirms:
- connectivity-between-guilt-responsibility-related-outcome-ph
belongings:
- relation: supports
  target: functional-connectivity-between-guilt-responsibility-related
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig5
  confidence: tentative
reproductions: []
---

**Notes from extraction:** The caption reader (tentative) stated the analysis but not the direction; the results reader supplied the direction and statistics.

**Relations.** Why each outgoing edge was inferred:

- `tests` → `connectivity-between-guilt-responsibility-related-outcome-ph`: the insula-seed PPI tests the prefrontal Condition-by-Choice interaction prediction (results-142)
- `confirms` → `connectivity-between-guilt-responsibility-related-outcome-ph`: a right-IFG cluster's insula connectivity varied with condition and choice and survived FWE correction
- `supports` → `functional-connectivity-between-guilt-responsibility-related`: condition/choice-dependent insula connectivity supports the connectivity hypothesis

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> The first analysis revealed a cluster in the right IFG whose connectivity to the insula (the seed region) was highest when participants made Risky choices for themselves and Safe choices for both players (pFWE = 0.020, T = 4.34, d = 0.80, Z = 4.21, 115 voxels, peak at MNI [46 16 22]; Figure 5).

**caption-reader evidence:**
> Changes in functional connectivity between the left anterior insula (seed) and a cluster in the right inferior frontal gyrus at the time of the choice as a function of condition (Social vs. Solo) and choice (Risky or Safe).
