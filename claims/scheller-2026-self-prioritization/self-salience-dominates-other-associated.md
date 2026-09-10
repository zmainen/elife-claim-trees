---
uuid: fcc24782-2506-4c9e-908a-baa03bb791fb
slug: self-salience-dominates-other-associated
doi: ~
claim: >
  For perceptually salient self-associated stimuli, social salience effects are the stronger
  predictor (BFinclusion = 2458.52) while perceptual salience also contributes; for
  perceptually salient other-associated stimuli, perceptual salience dominates
  (BFinclusion = 4638.74), with social salience having a weaker role.
shortClaim: "Social salience dominates for self-associated stimuli — perceptual salience dominates for other."
claim-type: empirical
role: synthesis
concepts:
  - Bayesian model selection
  - self vs other association
  - salience dominance
  - individual differences
  - attentional prediction
priority: 2026-03-30
epistemic: moderate

interprets:
  - self-salience-reduces-perceptual-benefit
  - self-social-additive-perceptual

belongings:
  - relation: requires
    target: self-salience-reduces-perceptual-benefit

assertions:
  - paper-slug: scheller-2026-self-prioritization
    doi: 10.7554/eLife.100932
    panel: fig9 (Tables 1, 2)
    figureUri: https://iiif.elifesciences.org/lax/100932%2Felife-100932-fig9-v1.tif/full/1500,/0/default.jpg
    analysis: OSF analysis notebooks (https://osf.io/a62df)
    dataset: https://osf.io/a62df
    dataset-doi: ~
    method: Bayesian regression model comparison, Experiment 2 (N=71)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      Data accessible on OSF (Correlation_Results.xlsx contains Δw and ΔΔv per participant).
      The BFinclusion values (2458.52, 4638.74) require running Bayesian regression model
      comparison using the BayesFactor R package or equivalent. The qualitative pattern is
      confirmed from point estimates: self-salient condition has smaller perceptual benefit
      (2.58 Hz) than other-salient (5.32 Hz), suggesting social salience dominates for
      self. BFinclusion computation not yet executed.
---

The regression analysis establishes an asymmetry in how social and perceptual salience compete for attention: for self-associated stimuli, who the object belongs to trumps how salient it looks; for other-associated stimuli, physical appearance dominates. This asymmetry is consistent with a hierarchical processing account where self-relevance engages a high-priority attentional channel that overrides bottom-up salience cues.
