---
uuid: 476a1ca2-1ad8-4d72-833a-15f0af2528c0
slug: optogenetic-activation-not-physiological-pattern
doi: ~
claim: >
  SERT-Cre + ChR2-mediated optogenetic activation drives DRN serotonergic neurons more
  broadly and uniformly than endogenous serotonin release, which engages anatomically and
  functionally distinct subpopulations with distinct projection targets and behavioral
  correlates. Optogenetic drive itself is not spatially uniform either — light intensity
  falls off steeply from the fiber tip and ChR2-expressing neurons show frequency-dependent
  adaptation (Dugué et al. 2014) — but it nevertheless produces a coordinated phasic
  response unlike the correlated-ensemble patterns observed during natural behavior
  (Paquelet et al. 2022, calcium imaging).
displayClaim: >
  Optogenetic SERT-Cre activation drives a broader, more synchronized 5-HT response than
  endogenous release. Optogenetic drive itself is non-uniform (light fall-off, ChR2
  adaptation; Dugué 2014).
claim-type: assessment
role: scope
concepts:
  - optogenetic specificity
  - ChR2 adaptation
  - light penetration
  - DRN subpopulation organization
  - endogenous vs evoked
priority: 2026-04-20
epistemic: moderate

scopes:
  - 5ht-modulates-all-recorded-regions-bidirectionally
  - 5ht-stim-leaves-decision-behavior-intact
  - 5ht-axis-orthogonal-to-choice-axis
  - near-zero-choice-by-stim-interaction
  - hypothesis-additive-modulation

belongings:
  - relation: requires
    target: interprets-paquelet-correlated-ensembles
  - relation: requires
    target: interprets-cohen-li-matias-phasic-5ht-responses

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: discussion / scope
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: discussion / scope claim, supported by external literature (Dugué 2014 on light delivery and ChR2 adaptation; Paquelet 2022 on DRN ensemble structure; Cohen 2015, Li 2016, Matias 2017 on phasic 5-HT responses)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

Carries over from v1 with two material refinements that the R1 D2 rewrite makes explicit:

1. **Optogenetic drive is not uniform.** The v1 manuscript described stimulation as "recruiting all DRN serotonergic neurons simultaneously," which is wrong — light intensity falls off with distance from the fiber tip and ChR2 shows frequency-dependent adaptation at sustained 25-Hz stimulation. Dugué et al. (2014) characterized both effects. The R1 wording correctly says SERT-Cre stimulation drives DRN neurons "more broadly and uniformly than endogenous release" without claiming it is itself uniform.

2. **Endogenous activation is correlated-ensemble, not synchronous-burst.** The v1 manuscript characterized endogenous DRN activation in response to sucrose and footshock as "synchronized burst-like firing of 50–60% of neurons," citing Paquelet et al. (2022). The R1 D2 rewrite corrects this on three counts (see `interprets-paquelet-correlated-ensembles`): Paquelet used calcium imaging (cannot resolve bursts), the percentages should be separated by stimulus (sucrose 59%, footshock 45%), and the activation is correlated-ensemble with mixed selectivity rather than uniform synchrony.

The scope claim now scopes more findings than in v1: in addition to the brain-wide modulation, behavioral null, and orthogonality results, R1's central additivity hypothesis (`hypothesis-additive-modulation`) and the GLM result (`near-zero-choice-by-stim-interaction`) are also bounded by this claim. The reasoning is the same as v1's: results from optogenetic stimulation describe what brain-wide 5-HT activation can do, not what 5-HT in fact does in this task under endogenous activation patterns. The R1 refinement makes this scope more honest by characterizing both the optogenetic drive and the endogenous comparison correctly.
