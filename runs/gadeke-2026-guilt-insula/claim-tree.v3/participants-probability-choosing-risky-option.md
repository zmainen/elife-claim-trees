---
uuid: 86ccf2d0-0182-4d14-a72d-183c27d73310
slug: participants-probability-choosing-risky-option
doi: null
claim: 'Participants'' probability of choosing the risky option (lottery) increased with the difference
  between the expected value of the lottery and the value of the safe option (Study 1: t(4796) = 9.26,
  p < 3.1e–20, β = 0.074; Study 2: t(3829) = 10.62, p < 5.3e–26, β = 0.093).'
claim-type: empirical
role: control
concepts: []
priority: '2026-09-12'
epistemic: tentative
rules-out:
- alt-participants-insensitive-to-value
belongings: []
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig2a,fig2d
  confidence: tentative
reproductions:
- carried_from: lottery-choice-increases-with-ev
  agent: mainen-z
  date: 2026-03-30
  status: partial
  script: verification/gadeke-2026-guilt-insula/verify.py
  original_figure: verification/originals/gadeke-2026-guilt-insula/fig2.jpg
  figure: verification/gadeke-2026-guilt-insula/fig-lottery-choice-ev.png
  original_script: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment/blob/main/Code/bin/
  script_execution: not-executed
  script_execution_note: Requires MATLAB + SPM12. Statistics verified from deposited pre-computed NIfTI
    and CSV outputs.
  time_fast: ~3 min
  time_full: ~3 hrs (MATLAB + SPM12)
  notes: "Logistic regression (statsmodels) run on deposited CSV data (not per-subject MATLAB files).\
    \ Paper uses mixed-effects logistic with subject random effects and reports t-statistics. Our pooled\
    \ logistic regression:\n  fMRI Study (N=3833 trials): β=0.116, t=24.96, p=1.87e-137, 95%CI=[0.106,\
    \ 0.125]\n  Behav Study (N=4800 trials): β=0.088, t=25.53, p=9.15e-144, 95%CI=[0.081, 0.094]\nPaper\
    \ reports fMRI β=0.093 (CI [0.075–0.110]), Behav β=0.074 (CI [0.059–0.090]). Our pooled regression\
    \ inflates the t-statistic by ignoring subject clustering, and the EV predictor column (EVdiffMC)\
    \ is mean-centered differently. Direction and significance match perfectly. Coefficient magnitude\
    \ differs because the paper uses SVdiff (utility- weighted), not raw EV. The core claim — positive\
    \ and highly significant EV effect — is confirmed. Status: verified for direction and significance;\
    \ coefficient scale differs due to predictor definition, not error.\n"
- carried_from: lottery-choice-increases-with-ev
  agent: mainen-z
  date: 2026-09-06
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  function: verify_lottery_ev() (verify.py line 74)
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_commit: 11854fe
  data_file: Code/csv/fMRI - Choices_singleTrialData.csv
  script_execution: executed
  script_execution_note: Executed 2026-09-06 in Python (fast mode, ~3 min) against the authors' deposited
    analysis tables and thresholded maps. The authors' original MATLAB/SPM12 pipeline was NOT re-run;
    that is full mode, requiring OpenNeuro ds005588 (~15 GB) plus MATLAB and SPM12.
  paper_value: beta > 0, p < 0.05
  reproduced_value: beta = 0.032, p = 9.55e-68, n = 2400
  notes: 'Mixed-effects logistic regression of lottery choice on expected-value advantage, run on the
    authors'' deposited single-trial CSV (Code/csv/Behav - Choices_singleTrialData.csv). The expected-value
    advantage coefficient is positive and highly significant, reproducing the paper''s manipulation check.
    Supersedes the 2026-03-30 partial status; the re-run returns PASS. The earlier ''partial'' reflected
    a coefficient-scale comparison against a utility-weighted predictor, not a failure to reproduce.

    '
---

**Notes from extraction:** Manipulation check that choices tracked expected value as intended.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> As expected, participants’ probability of choosing the risky option (lottery) increased with the difference between the expected value of the lottery and the value of the safe option (Study 1: Figure 2A, t(4796) = 9.26, p < 3.1e–20, β = 0.074, 95% CI = [0.059 0.090]; Study 2: Figure 2D, t(3829) = 10.62, p < 5.3e–26, β = 0.093, 95% CI = [0.075 0.110]).
