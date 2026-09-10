---
uuid: 70f673a2-d528-4d47-ae37-df7cd4e26044
slug: interprets-paquelet-correlated-ensembles
doi: 10.1016/j.neuron.2022.05.015
claim: >
  Paquelet et al. (2022, Neuron) used calcium imaging in awake behaving mice to characterize
  population activity in DRN serotonergic neurons. Sucrose consumption activated correlated
  ensembles comprising up to 59% of recorded serotonergic neurons; footshock activated
  correlated ensembles comprising up to 45%. During exploratory behaviors and social
  interaction, serotonergic neurons were recruited in coordinated ensembles with mixed
  selectivity. The activation pattern is correlated and ensemble-structured, not a uniform
  population-wide synchronous burst.
displayClaim: >
  Sucrose and footshock activate correlated DRN serotonergic ensembles (up to 59% and 45%
  of neurons respectively) with mixed selectivity — not uniform population synchrony
  (Paquelet 2022).
claim-type: interpretive
role: literature-context
concepts:
  - DRN ensemble structure
  - calcium imaging
  - correlated activation
  - mixed selectivity
priority: 2026-04-19
epistemic: moderate

belongings: []

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: discussion (D2 optogenetics limitation paragraph, D7 co-release paragraph)
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: literature interpretation; cited in D2 to characterize endogenous DRN activation patterns and in D7 on subpopulation organization
    confidence: moderate

reproductions: []
---

This claim registers the corrected characterization of endogenous DRN serotonergic activation patterns that R1 introduces in the discussion (D2 per revision notes). The v1 manuscript described "synchronized burst-like firing of 50–60% of serotonergic neurons" in response to sucrose and footshock, citing Paquelet et al. (2022). The R1 revision corrects this on three counts:

1. *Method.* Paquelet et al. used calcium imaging, which has temporal resolution insufficient to resolve spike bursts. The "burst-like firing" characterization was wrong on the underlying measurement; the actual finding is correlated calcium transients in ensembles, which Cohen et al. (2015, electrophysiology) and Li et al. (2016, fiber photometry) supplement with more direct evidence for phasic firing responses (registered separately as `interprets-cohen-li-matias-phasic-5ht-responses`).

2. *Numbers.* The 50–60% in v1 conflated sucrose (59%) and footshock (45%), reporting both as a single uniform range. The R1 revision separates the two stimuli with their actual fractions.

3. *Population structure.* The v1 framing ("synchronized burst-like firing of 50–60%") suggested uniform population synchrony. Paquelet et al.'s actual finding is correlated *ensemble* structure with mixed selectivity — different stimuli engage overlapping but distinguishable subpopulations. The R1 revision uses "correlated ensembles" rather than "synchronized firing."

This corrected characterization matters for the optogenetic-scope claim `optogenetic-activation-not-physiological-pattern`: optogenetic SERT-Cre + ChR2 stimulation drives a much broader and less ensemble-structured response than endogenous DRN activation. The v1 framing's overstatement of endogenous synchrony minimized this gap; the R1 framing acknowledges it more accurately. The graph encodes this through `optogenetic-activation-not-physiological-pattern` requiring both this claim and `interprets-cohen-li-matias-phasic-5ht-responses` as part of its scope-bounding context.
