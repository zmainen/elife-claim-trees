---
uuid: 1ccdf7c0-20fe-448b-8173-e0dd6eabdb37
slug: drn-projection-density-not-significant-predictor
doi: ~
claim: >
  Contrary to the expectation that brain regions receiving stronger direct projections from
  the dorsal raphe nucleus would be more strongly modulated by 5-HT stimulation, DRN
  projection density (from the Allen Mouse Connectivity Atlas, averaged over the three
  experiments with the strongest projection results) is not a significant positive predictor
  of regional modulation strength in the GLM. In the strength model the DRN projection
  coefficient is in fact negative. This null result implies that most of the brain-wide
  serotonergic modulation observed is not mediated by direct DRN axonal projections to the
  recorded region — instead, the dominant effects are likely indirect (polysynaptic through
  intermediate regions, or via volume transmission of serotonin across region boundaries).
displayClaim: >
  DRN projection density is not a significant positive predictor of modulation strength —
  most modulation is likely indirect or polysynaptic, not via direct projections.
claim-type: empirical
role: empirical
concepts:
  - DRN projections
  - indirect pathways
  - volume transmission
  - polysynaptic modulation
  - null result
priority: 2026-04-20
epistemic: moderate

belongings:
  - relation: requires
    target: receptor-expression-predicts-modulation-strength

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig3b
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation; statsmodels GLM
    dataset: Allen Mouse Connectivity Atlas (experiment IDs 480074702, 114155190, 128055110)
    dataset-doi: ~
    method: per-Beryl-region GLM coefficient for DRN projection density (z-scored) as one of seven predictors of modulation strength (Binomial family)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

This is one of the most informative negative findings in the paper. The pre-registered expectation from the receptor-density GLM design was that direct DRN projections would correlate with the observed modulation pattern, on the standard reasoning that regions receiving more direct serotonergic axons should experience more direct modulation. The data refute this: DRN projection density does not significantly predict modulation strength as a positive coefficient. The R1 discussion (paragraph 4) takes this seriously and concludes that the dominant brain-wide effects are likely indirect — polysynaptic relays through intermediate regions or volume transmission of serotonin across region boundaries.

The hippocampus is the cleanest illustration. In the recordings, 5-HT stimulation produces strong and rapid suppression of hippocampal activity. But the dorsal raphe nucleus does not project strongly to the hippocampus directly — projections are dominated by the median raphe nucleus, which receives input from DRN and projects to hippocampus. The DRN→MR→hippocampus polysynaptic pathway is consistent with the rapid hippocampal effect being driven by indirect projections rather than direct DRN axons.

The implication for the brain-wide additivity finding is that the additive computational signature observed is the net result of mixed direct and indirect pathways, not exclusively direct serotonergic transmission. This is registered explicitly in the discussion and reinforces the scope claim `optogenetic-activation-not-physiological-pattern` — what is being measured is the brain-wide consequence of strong DRN serotonergic activation, including its indirect downstream effects, rather than direct serotonergic modulation per se.
