---
uuid: e36646f0-ce3f-4223-acec-a4c490b38400
slug: happiness-correlates-partner-reward
doi: ~
claim: >
  Participant momentary happiness correlates with both participant reward (Study 1:
  F(1,3598)=691.5, R²=0.16; Study 2: F(1,2630)=650.8, R²=0.20) and partner reward
  (Study 1: F(1,2426)=128.6, R²=0.05; Study 2: F(1,1735)=111.8, R²=0.06), confirming
  that participants were emotionally responsive to partner outcomes throughout the task.
claim-type: empirical
role: empirical
concepts:
  - momentary happiness
  - partner reward
  - other-regarding preferences
  - social decision
priority: 2026-03-30
epistemic: strong

validates:
  - guilt-reduces-happiness-after-partner-loss
  - hypothesis-insula-tracks-interpersonal-guilt

belongings:
  - relation: supports
    target: guilt-reduces-happiness-after-partner-loss

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig3a, fig3b, fig3e, fig3f
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: master_behavAnalysis.m
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: mixed-effects linear regression (pooled across participants)
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: verified
    script: verification/gadeke-2026-guilt-insula/verify.py
    original_figure: verification/originals/gadeke-2026-guilt-insula/fig3.jpg
    figure: verification/gadeke-2026-guilt-insula/fig-happiness-partner-reward.png
    original_script: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment/blob/main/Code/bin/
    script_execution: not-executed
    script_execution_note: "Requires MATLAB + SPM12. Statistics verified from deposited pre-computed NIfTI and CSV outputs."
    time_fast: "~3 min"
    time_full: "~3 hrs (MATLAB + SPM12)"
    notes: >
      Pre-computed LMM tables in Code/csv/ confirm all values directly. Partner reward (rewardPart)
      is a significant positive predictor of happiness in both studies:
        fMRI Study: β=0.16* (SE=0.07), Model R²=0.185, N=1895 (matches paper R²=0.185)
        Behav Study: β=0.21*** (SE=0.06), Model R²=0.147, N=2428 (matches paper)
      The paper reports partner reward F-statistics from a different model decomposition;
      our confirmatory statsmodels LMM on trial-level data gives:
        fMRI: β=0.631, p=1.05e-14; Behav: β=0.575, p=1.88e-16
      Pearson r (pooled, no random effects): fMRI r=0.243, Behav r=0.230, both p<1e-13.
      Direction, significance, and approximate R² all match. Claim verified.
  - agent: mainen-z
    date: 2026-09-06
    status: verified
    script: verification/gadeke-2026-guilt-insula/verify.py
    function: verify_happiness_partner() (verify.py line 147)
    data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
    data_commit: 11854fe
    data_file: "Code/csv/ — happiness-by-model tables, both cohorts (auto-detected by column matching; see caveat below)"
    script_execution: executed
    script_execution_note: "Executed 2026-09-06 in Python (fast mode, ~3 min) against the authors' deposited analysis tables and thresholded maps. The authors' original MATLAB/SPM12 pipeline was NOT re-run; that is full mode, requiring OpenNeuro ds005588 (~15 GB) plus MATLAB and SPM12."
    paper_value: "R2 = 0.185 (fMRI cohort), 0.147 (behavioural cohort)"
    reproduced_value: "R2 = 0.184, 0.145"
    notes: >
      Model R² for the happiness model including partner reward, recomputed for both cohorts
      from the authors' deposited happiness-by-model tables. Both values land within 0.002 of
      the published figures.
      Caveat on auditability: the script currently locates its input by globbing the CSV
      directory and matching on column names rather than by a pinned filename, so this row of
      the chain is not yet independently auditable — a reader cannot confirm which file was
      read. Pinning the exact filename is an open task.
---

This is a prerequisite for the guilt-effect analysis. If partner reward did not influence happiness at all, the guilt contrast (partner low outcome × decision-maker identity) would be uninformative. The partner reward effect is weaker than the self-reward effect by a factor of roughly 3–4 in R², consistent with self-interest dominating but social information making a meaningful independent contribution. Note the algorithm-partner deception makes this result particularly informative: participants were emotionally responsive to algorithmic partner outcomes as if they were real.
