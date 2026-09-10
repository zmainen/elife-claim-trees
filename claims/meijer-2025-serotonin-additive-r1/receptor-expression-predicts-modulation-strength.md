---
uuid: 8382db52-dd38-45c6-ba10-0bbe54a1960c
slug: receptor-expression-predicts-modulation-strength
doi: ~
claim: >
  A generalized linear model predicting per-region 5-HT modulation strength (the absolute
  modulation index, computed at the brain-region level after coarse-graining the Allen atlas
  into Beryl-atlas regions) from z-scored expression density of six serotonergic receptors
  (5-HT1a, 1b, 2a, 2c, 3a, 5a) and DRN projection density yields a high explained-variance
  fit (pseudo R² = 0.50, Binomial family with Logit link). The 5-HT1 receptor expression
  is a significant positive predictor of modulation strength: regions expressing more 5-HT1
  receptors contain a larger fraction of 5-HT-modulated neurons. DRN projection density and
  5-HT2a receptor expression are negative predictors. Variance inflation factors are < 5,
  indicating acceptable multicollinearity, and leave-one-region-out cross-validation
  produces tightly clustered coefficients indicating no single region drives the result.
displayClaim: >
  A receptor-expression + projection-density GLM (per-region) explains 50% of the variance
  in 5-HT modulation strength; 5-HT1 receptor expression is the leading positive predictor.
claim-type: empirical
role: empirical
concepts:
  - generalized linear model
  - 5-HT1 receptors
  - receptor expression
  - DRN projection density
  - cross-validation
priority: 2026-04-20
epistemic: strong

belongings:
  - relation: requires
    target: seven-target-trajectories-13-regions-7478-neurons
  - relation: requires
    target: 5ht-modulates-all-recorded-regions-bidirectionally

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig3a, fig3b
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation; statsmodels GLM
    dataset: Allen Brain Atlas ISH (receptor expression IDs in methods); Allen Mouse Connectivity Atlas (DRN projection IDs in methods); plus IBL ONE protocol for spiking data
    dataset-doi: ~
    method: per-Beryl-region GLM (Binomial family, Logit link) with seven z-scored predictors (six receptors + DRN projection density); leave-one-region-out cross-validation; VIF check
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

This is one of four new R1 empirical claims that came directly from Reviewer 2's request (R2.1.2.a) for a quantitative analysis of how receptor expression and projection density predict regional modulation patterns. Figure 3 (entirely new in R1; no v1 equivalent) is the result. The structural function of these four claims in the graph is to give the brain-wide bidirectional-modulation finding (`5ht-modulates-all-recorded-regions-bidirectionally`) a mechanistic substrate: the regional heterogeneity is not arbitrary but is partially explained by receptor distributions, with different receptor classes contributing in different ways.

Three details bound the strength claim. First, the GLM is fit at the per-region level on the Beryl atlas (~308 regions in the full atlas, but only the regions with ≥ 10 recorded neurons are included), so the unit of analysis is region-level not neuron-level. The pseudo R² of 0.50 is therefore at the regional aggregate level. Second, the predictors are z-scored receptor expression densities from public Allen Brain Atlas in situ hybridization data — they characterize the average density per region, not cell-type-specific expression patterns or activation-dependent receptor function. Third, the directionality of the 5-HT1 / 5-HT2a coefficients in the strength model differs from their directionality in the directionality model (`receptor-expression-predicts-modulation-direction`); see that claim for the picture of how the same receptors play different roles in predicting how-much vs. which-way modulation goes.

The Mainen-lab interpretation explicitly proposed by R1: 5-HT1 receptors are fast-acting inhibitory receptors with strong serotonin affinity; brain regions with more 5-HT1 are more reliably modulated because these receptors respond well to short phasic optogenetic pulses of serotonin. 5-HT2 receptors are slower and may be better suited to slow tonic serotonin levels than to phasic optogenetic drive — explaining their negative correlation with modulation strength under this stimulation protocol.
