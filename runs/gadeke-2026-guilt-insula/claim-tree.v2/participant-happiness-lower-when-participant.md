---
uuid: e5b37e08-ac87-426b-832d-1b97ba14923f
slug: participant-happiness-lower-when-participant
doi: null
claim: 'Participant happiness was lower when the participant was the decision-maker (Social + Solo vs.
  Partner), independent of outcome (Study 1: t(3600) = –3.92, p < 0.0001, β = –0.14; Study 2: t(2870)
  = –6.07, p < 0.0001, β = –0.24).'
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-11'
epistemic: tentative
rules-out:
- alt-agency-aversion-not-guilt
belongings: []
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: null
  confidence: tentative
reproductions:
- carried_from: agency-reduces-happiness
  agent: mainen-z
  date: 2026-09-11
  status: partial
  script: verification/gadeke-2026-guilt-insula/verify.py
  script_execution: executed
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_file: Code/csv/Behav - Happiness_singleTrialData_socialRiskyChoicesOnly.csv
  paper_value: t(3600)=-3.92, p<0.0001, beta=-0.14
  reproduced_value: decided=-0.048 vs not=0.122, t(39)=-2.60 p=0.0131 — direction reproduces on the deposited
    subset (social risky choices, 1216 trials); the paper's model covers ~3600
  notes: 'Re-checked 2026-09-11 against the deposited per-trial data, observed by verification/audit_run.py.
    Paper: t(3600)=-3.92, p<0.0001, beta=-0.14. Reproduced: decided=-0.048 vs not=0.122, t(39)=-2.60 p=0.0131
    — direction reproduces on the deposited subset (social risky choices, 1216 trials); the paper''s model
    covers ~3600. Recorded `unattempted` until this run, while the CSV that settles it was already being
    downloaded by the same script.

    '
- carried_from: agency-reduces-happiness
  agent: mainen-z
  date: 2026-03-30
  status: unattempted
  notes: null
---

**Notes from extraction:** The agency effect on happiness, distinct from the guilt (partner-outcome-contingent) effect.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> we assessed whether happiness varied depending on the participant’s agency (Social + Solo vs. Partner), and found happiness to be lower when the participant chose, independent of the outcome (Study 1: t(3600) = –3.92, p < 0.0001, β = –0.14, 95% CI = [−0.20 to 0.07]; Study 2: t(2870) = –6.07, p < 0.0001, β = –0.24, 95% CI = [−0.31 to 0.16]).
