---
uuid: 2952075b-80ca-4849-9ddd-6582a1967dac
slug: participants-chose-risky-option-lottery
doi: null
claim: Participants chose the risky option (lottery) more often in the Solo than the Social condition
  in Study 1 (t(4796) = 2.54, p = 0.011, β = 0.164) but not in Study 2 (t(3829) = 0.23, p = 0.82, β =
  0.015).
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-12'
epistemic: tentative
part-of:
- participants-showed-very-similar-risk
belongings: []
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig2a,fig2d
  confidence: tentative
reproductions:
- carried_from: solo-vs-social-choice-difference
  agent: mainen-z
  date: 2026-09-11
  status: partial
  script: verification/gadeke-2026-guilt-insula/verify.py
  script_execution: executed
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_file: Code/csv/Behav - Choices_singleTrialData.csv
  paper_value: t(4796)=2.54, p=0.011 (weak, not replicated in Study 2)
  reproduced_value: cond0=0.518 vs cond1=0.536, t(39)=-1.06 p=0.297 per participant — the deposit does
    not document which level is Solo, and a per-participant test has far less power than the paper's trial-level
    model
  notes: 'Re-checked 2026-09-11 against the deposited per-trial data, observed by verification/audit_run.py.
    Paper: t(4796)=2.54, p=0.011 (weak, not replicated in Study 2). Reproduced: cond0=0.518 vs cond1=0.536,
    t(39)=-1.06 p=0.297 per participant — the deposit does not document which level is Solo, and a per-participant
    test has far less power than the paper''s trial-level model. Recorded `unattempted` until this run,
    while the CSV that settles it was already being downloaded by the same script.

    '
- carried_from: solo-vs-social-choice-difference
  agent: mainen-z
  date: 2026-03-30
  status: unattempted
  notes: Behavioral result from Study 1. Not yet executed.
---

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Participants chose the lottery more often in the Solo condition than in the Social condition in Study 1 (t(4796) = 2.54, p = 0.011, β = 0.164, 95% CI = [0.038 0.291]), but this difference was not found in Study 2 (t(3829) = 0.23, p = 0.82, β = 0.015, 95% CI = [–0.109 0.138]).

**caption-reader evidence:**
> Participants chose the risky option slightly more often in the Solo condition than in the Social condition in Study 1 ( A ) but not in Study 2 ( D ).
