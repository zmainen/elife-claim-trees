---
uuid: d5cc37f8-3738-4acf-95de-3c10a177aa69
slug: self-salience-reduces-perceptual-benefit
doi: ~
claim: >
  Perceptual salience benefit is substantially reduced for self-associated stimuli (2.5 Hz
  [HDI95: 0.86 to 4.1 Hz]) compared to other-associated (5.2 Hz [HDI95: 3.6 to 6.9 Hz])
  or non-socially-associated perceptually salient stimuli (6 Hz [HDI95: 4.6 to 7.3 Hz]),
  indicating a sub-additive interaction when social self-relevance and perceptual salience
  co-occur.
claim-type: empirical
role: empirical
concepts:
  - sub-additive interaction
  - self-salience
  - perceptual salience
  - attentional competition
  - obligatory self-prioritization
priority: 2026-03-30
epistemic: moderate

refutes:
  - hypothesis-social-perceptual-independent-mechanisms
dissociates-with:
  - self-social-additive-perceptual

belongings:
  - relation: requires
    target: perceptual-salience-6hz-advantage
  - relation: supports
    target: self-salience-dominates-other-associated

assertions:
  - paper-slug: scheller-2026-self-prioritization
    doi: 10.7554/eLife.100932
    panel: fig6, fig7
    figureUri: https://iiif.elifesciences.org/lax/100932%2Felife-100932-fig6-v1.tif/full/1500,/0/default.jpg
    analysis: OSF analysis notebooks (https://osf.io/a62df)
    dataset: https://osf.io/a62df
    dataset-doi: ~
    method: hierarchical Bayesian TVA, condition comparison, Experiment 2 (N=71)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-09-13
    status: verified
    script: verification/scheller-2026-self-prioritization/verify.py
    original_script: https://osf.io/a62df
    script_execution: executed
    script_execution_note: >
      Automated as verify_self_salience_subadditive(): recomputes mean(v_p - v_r) per
      condition from the deposited posterior summary CSV and checks the sub-additive
      ordering (self-salient < other-salient < pure perceptual).
    data_source: https://osf.io/a62df
    data_file: estimates_indiv_C_Exp2.csv
    notes: >
      Verified from estimates_indiv_C.csv (Exp2, OSF https://osf.io/a62df). Self-salient
      cond (4): diff = 2.58 Hz (claim: 2.5 Hz). Other-salient cond (5): diff = 5.32 Hz
      (claim: 5.2 Hz). Non-social perceptual cond (2): diff = 6.05 Hz (claim: 6 Hz).
      Sub-additivity pattern confirmed: self-associated salience benefit (2.58) < other-
      associated salience benefit (5.32) < pure perceptual benefit (6.05).
---

The sub-additivity for self-associated stimuli is the paper's most theoretically interesting interaction: self-relevance actively reduces the processing benefit that perceptual salience would otherwise confer. The paper interprets this as "obligatory" self-prioritization — self-relevance so dominates the attentional allocation that it competes with rather than adds to physical salience. The effect is driven by a smaller salient rate increase for self-associated stimuli (0.78 Hz vs 2.5 Hz for other-associated) and less suppression of the non-salient stimulus.
