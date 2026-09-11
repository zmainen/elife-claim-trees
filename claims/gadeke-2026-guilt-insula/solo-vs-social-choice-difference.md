---
uuid: 5198582f-237b-447c-810e-c9a4559f9cb6
slug: solo-vs-social-choice-difference
doi: ~
claim: >
  Participants chose lotteries more often in the Solo condition than in the Social condition in Study 1 (t(4796)=2.54, p=0.011, β=0.164, 95%CI=[0.038, 0.291]) but not in Study 2 (t(3829)=0.23, p=0.82, β=0.015), suggesting a weak and inconsistent effect of social context on risk-taking that does not replicate across studies.
claim-type: empirical
role: empirical
concepts:
  - solo condition
  - social condition
  - risk-taking
  - lottery choice
priority: 2026-03-30
epistemic: moderate

dissociates-with:
  - risk-premiums-null-social-solo

belongings: []

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig2a (Study 1 only; null in fig2d Study 2)
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: master_behavAnalysis.m
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: mixed-effects regression
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-09-11
    status: partial
    script: verification/gadeke-2026-guilt-insula/verify.py
    script_execution: executed
    data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
    data_file: Code/csv/Behav - Choices_singleTrialData.csv
    paper_value: "t(4796)=2.54, p=0.011 (weak, not replicated in Study 2)"
    reproduced_value: "cond0=0.518 vs cond1=0.536, t(39)=-1.06 p=0.297 per participant — the deposit does not document which level is Solo, and a per-participant test has far less power than the paper's trial-level model"
    notes: >
      Re-checked 2026-09-11 against the deposited per-trial data, observed by verification/audit_run.py. Paper: t(4796)=2.54, p=0.011 (weak, not replicated in Study 2). Reproduced: cond0=0.518 vs cond1=0.536, t(39)=-1.06 p=0.297 per participant — the deposit does not document which level is Solo, and a per-participant test has far less power than the paper's trial-level model. Recorded `unattempted` until this run, while the CSV that settles it was already being downloaded by the same script.
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      Behavioral result from Study 1. Not yet executed.
---


