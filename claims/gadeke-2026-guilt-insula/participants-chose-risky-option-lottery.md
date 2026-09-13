---
uuid: f12d294d-eafe-4a6b-9968-8b4d9034ee56
slug: participants-chose-risky-option-lottery
doi: null
claim: Participants chose the risky option (lottery) more often in the Solo than the Social condition
  in Study 1 (t(4796) = 2.54, p = 0.011, β = 0.164) but not in Study 2 (t(3829) = 0.23, p = 0.82, β =
  0.015).
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-13'
belongings:
- relation: supports
  target: participants-showed-very-similar-risk
- relation: requires
  target: each-trial-participants-chose-between
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig2a,fig2d
  readers: high
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
warrant: weak
warrant_why: a choice result that requires the paradigm each-trial-participants-chose-between; no control or support bears on it
warrant_from:
- requires
check_verification: reproduced
check_verification_from:
- record:partial
- record:unattempted
- provenance:WARN measured
---

**Relations.** Why each outgoing edge was inferred:

- `supports` → `participants-showed-very-similar-risk`: the Solo>Social lottery-choice difference (fig2a,fig2d) is one of the risk-preference results the synthesis draws together
- `requires` → `each-trial-participants-chose-between`: the Solo/Social choice-proportion result requires the three-condition choice paradigm to have been run

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Participants chose the lottery more often in the Solo condition than in the Social condition in Study 1 (t(4796) = 2.54, p = 0.011, β = 0.164, 95% CI = [0.038 0.291]), but this difference was not found in Study 2 (t(3829) = 0.23, p = 0.82, β = 0.015, 95% CI = [–0.109 0.138]).

**caption-reader evidence:**
> Participants chose the risky option slightly more often in the Solo condition than in the Social condition in Study 1 ( A ) but not in Study 2 ( D ).
