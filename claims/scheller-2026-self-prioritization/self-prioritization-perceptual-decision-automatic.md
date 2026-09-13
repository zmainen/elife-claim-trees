---
uuid: 0b72064e-d0fc-43e9-a2d0-2d5044cde51e
slug: self-prioritization-perceptual-decision-automatic
doi: ~
claim: >
  In the perceptual decision dimension (report which shape flickered first), self-associated
  stimuli were processed 1.5 Hz faster than other-associated stimuli [HDI95: −0.16 to 3.2 Hz],
  driven by a capacity increase of 2.6 Hz and a self-associated rate increase of 2.1 Hz
  [HDI95: 0.13 to 4.1 Hz]; other-associated stimulus rate showed no consistent increase
  (0.53 Hz [HDI95: −1.4 to 2.5 Hz]).
claim-type: empirical
role: empirical
concepts:
  - self-prioritization
  - attentional selection
  - automatic processing
  - perceptual decision
  - TVA processing rates
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-self-advantage-perceptual-decision
confirms:
  - hypothesis-self-association-alters-attentional-selection

belongings:
  - relation: requires
    target: tva-capacity-model-wins
  - relation: supports
    target: self-prioritization-automatic-early

assertions:
  - paper-slug: scheller-2026-self-prioritization
    doi: 10.7554/eLife.100932
    panel: fig5
    figureUri: https://iiif.elifesciences.org/lax/100932%2Felife-100932-fig5-v1.tif/full/1500,/0/default.jpg
    analysis: OSF analysis notebooks (https://osf.io/a62df)
    dataset: https://osf.io/a62df
    dataset-doi: ~
    method: hierarchical Bayesian TVA estimation, Experiment 1 (N=69)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-09-13
    status: verified
    script: verification/scheller-2026-self-prioritization/verify.py
    original_script: https://osf.io/a62df
    script_execution: executed
    script_execution_note: >
      Automated as verify_perceptual_automatic(): recomputes mean(v_p - v_r) from the
      deposited posterior summary CSV for Exp1's baseline and perceptual conditions.
    data_source: https://osf.io/a62df
    data_file: estimates_indiv_C_Exp1.csv
    notes: >
      Verified from estimates_indiv_C.csv (Exp1, OSF https://osf.io/a62df). The 1.5 Hz
      self-advantage is the change in (v_p - v_r) from baseline to perceptual condition:
      baseline diff = -0.91 Hz, perceptual diff = +0.64 Hz, change = +1.55 Hz (claim: 1.5 Hz).
      Group-level computation from ΔC_µ and Δw_µ gives 1.45 Hz. ΔC_perceptual = 2.60 Hz
      (exact match); self rate Δ = 2.07 Hz (claim: 2.1 Hz); other rate Δ = 0.53 Hz (claim: 0.53 Hz).
      HDI bounds not independently verified (require posterior samples from .nc trace) but
      group-level summary confirms ΔC HDI = [-1.4, 6.7] Hz as claimed.
---

The 1.5 Hz self-advantage in the perceptual decision condition is the central finding for the automaticity claim: when participants merely report which shape flickered first (without decoding the social identity), self-associated stimuli still receive enhanced processing. The HDI barely crossing zero (lower bound −0.16 Hz) means this specific effect is not conclusive in isolation — the strength of the claim rests on the convergence across experiments and conditions. The capacity increase of 2.6 Hz is notable but similarly uncertain (HDI95: −1.7 to 6.8 Hz in the results text).
