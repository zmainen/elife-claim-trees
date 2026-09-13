---
uuid: db461123-def3-48f9-b844-22dd93864d70
slug: partner-reward-prediction-errors-resulting
doi: null
claim: 'The partner''s reward prediction errors resulting from the participants'' own choices (social_pRPE)
  had weights greater than 0 (Responsibility model: Study 1: Z = 2.85, p = 0.004; Study 2: Z = 3.26, p
  = 0.001), contributing to explaining participants'' momentary happiness.'
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-11'
epistemic: tentative
tests:
- responsibility-partner-outcomes-influences-participant
belongings:
- relation: requires
  target: momentary-happiness-modelled-five-computational
- relation: supports
  target: both-studies-participants-felt-worse
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: null
  confidence: tentative
reproductions:
- carried_from: social-prpe-weight-positive
  agent: mainen-z
  date: 2026-09-11
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  script_execution: executed
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_file: Code/csv/Behav - Responsibility - fittedParameters.csv
  paper_value: Z=2.85, p=0.004 (social_pRPE > 0)
  reproduced_value: median=0.197, wilcoxon p=0.0037, 27/40 above zero
  notes: 'Re-checked 2026-09-11 against the deposited per-trial data, observed by verification/audit_run.py.
    Paper: Z=2.85, p=0.004 (social_pRPE > 0). Reproduced: median=0.197, wilcoxon p=0.0037, 27/40 above
    zero. Recorded `unattempted` until this run, while the CSV that settles it was already being downloaded
    by the same script.

    '
- carried_from: social-prpe-weight-positive
  agent: mainen-z
  date: 2026-03-30
  status: unattempted
  notes: null
---

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> weights for social_pRPE were greater than 0: Responsibility model: Study 1: Z = 2.85, p = 0.004, Study 2: Z = 3.26, p = 0.001; ResponsibilityRedux model: Study 1: Z = 2.93, p = 0.003, Study 2: Z = 3.30, p = 0.001.
