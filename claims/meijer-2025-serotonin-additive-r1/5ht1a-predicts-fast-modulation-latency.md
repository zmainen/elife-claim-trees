---
uuid: 4ddd99ac-4a0c-4be4-b736-964e4e896ce2
slug: 5ht1a-predicts-fast-modulation-latency
doi: ~
claim: >
  A generalized linear model predicting per-region mean 5-HT modulation latency from z-scored
  expression density of six serotonergic receptors and DRN projection density yields a fit
  with pseudo R² = 0.52 (Gamma family with log link). Among the predictors, only 5-HT1a
  receptor expression is a significant negative predictor of modulation latency: regions
  expressing more 5-HT1a are modulated by 5-HT stimulation at shorter latencies. Contrary
  to the original hypothesis, neither DRN projection density nor expression of the
  ionotropic 5-HT3 receptor is a significant predictor of latency.
displayClaim: >
  5-HT1a expression negatively predicts modulation latency (more 5-HT1a → faster); DRN
  projection density and ionotropic 5-HT3 are not significant predictors.
claim-type: empirical
role: empirical
concepts:
  - 5-HT1a
  - modulation latency
  - ionotropic 5-HT3
  - direct projections
priority: 2026-04-20
epistemic: moderate

belongings:
  - relation: requires
    target: receptor-expression-predicts-modulation-strength

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig3d
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation; statsmodels GLM
    dataset: Allen Brain Atlas ISH; Allen Mouse Connectivity Atlas; IBL ONE protocol
    dataset-doi: ~
    method: per-Beryl-region GLM (Gamma family, log link) on mean per-neuron modulation latency, latencies estimated via latenZy (ref. 27)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

The latency result has two notable null findings. First, ionotropic 5-HT3 receptor expression does not predict modulation latency, contrary to the prior expectation that ionotropic receptors (which are direct ligand-gated ion channels and therefore in principle the fastest) would mediate the shortest-latency responses. Second, DRN projection density does not predict latency either — regions receiving more direct DRN input are not modulated at shorter latencies than those receiving little. Both null results are consistent with the broader observation in the paper that the fastest 5-HT modulation effects are likely indirect or polysynaptic, not direct ionotropic transmission.

The positive result — 5-HT1a expression predicting fast modulation — is consistent with the Gi/o-coupled inhibitory mechanism of 5-HT1a being relatively fast among the metabotropic receptors. The result also dovetails with the per-neuron finding that putative inhibition is faster than excitation on average (per the broader finding in `latency-correlates-with-absolute-modulation`, although the directional fast-inhibition / slow-excitation claim from v1 was not replicated under the new latenZy method).

Moderate epistemic strength because the latency estimation is itself noisy (latenZy excludes neurons without a reliable peak, reducing per-region sample size), and the Gamma-link model is a particular choice for a positive-valued target.
