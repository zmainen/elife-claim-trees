---
uuid: 5d2ef557-c6ec-4052-82c2-0b8e4c297e01
slug: functional-connectivity-between-left-anterior
doi: null
claim: Functional connectivity between the left anterior insula (seed) and a cluster in the right inferior
  frontal gyrus varied with condition and choice, being highest when participants made Risky choices for
  themselves and Safe choices for both players (pFWE = 0.020, T = 4.34, d = 0.80, 115 voxels, peak MNI
  [46 16 22]).
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-12'
epistemic: tentative
tests:
- connectivity-between-guilt-responsibility-related-outcome-ph
belongings:
- relation: supports
  target: functional-connectivity-between-guilt-responsibility-related
- relation: requires
  target: prior-functional-connectivity-work-shown
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig5
  confidence: tentative
reproductions: []
---

**Notes from extraction:** The caption reader (tentative) stated the analysis but not the direction; the results reader supplied the direction and statistics.

**Relations.** Why each outgoing edge was inferred:

- `tests` → `connectivity-between-guilt-responsibility-related-outcome-ph`: The insula-IFG connectivity varying with condition and choice tests the connectivity prediction (evidence at span results-142).
- `supports` → `functional-connectivity-between-guilt-responsibility-related`: The condition- and choice-dependent insula-IFG connectivity supports the connectivity hypothesis (evidence at span results-142).
- `requires` → `prior-functional-connectivity-work-shown`: The connectivity analysis inherits prior functional-connectivity findings as background (evidence at span results-142).

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> The first analysis revealed a cluster in the right IFG whose connectivity to the insula (the seed region) was highest when participants made Risky choices for themselves and Safe choices for both players (pFWE = 0.020, T = 4.34, d = 0.80, Z = 4.21, 115 voxels, peak at MNI [46 16 22]; Figure 5).

**caption-reader evidence:**
> Changes in functional connectivity between the left anterior insula (seed) and a cluster in the right inferior frontal gyrus at the time of the choice as a function of condition (Social vs. Solo) and choice (Risky or Safe).
