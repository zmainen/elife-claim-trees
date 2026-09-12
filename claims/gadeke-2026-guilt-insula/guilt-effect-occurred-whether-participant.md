---
uuid: a699617e-d283-4bf0-9279-dc1006c0bb83
slug: guilt-effect-occurred-whether-participant
doi: null
claim: 'The guilt effect occurred whether the participant received the high lottery outcome (Study 1:
  t(39) = –3.58, p < 0.001, d = 0.56; Study 2: t(43) = –2.68, p = 0.01, d = 0.4) or the low outcome (Study
  1: t(39) = –3.39, p = 0.002, d = 0.54; Study 2: t(43) = –3.58, p < 0.001, d = 0.54).'
claim-type: empirical
role: control
concepts: []
priority: '2026-09-11'
epistemic: tentative
rules-out:
- alt-guilt-effect-driven-by-own-outcome
part-of:
- both-studies-participants-felt-worse
belongings:
- relation: supports
  target: both-studies-participants-felt-worse
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: null
  confidence: tentative
reproductions:
- carried_from: guilt-effect-independent-of-own-outcome
  agent: mainen-z
  date: 2026-09-11
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  script_execution: executed
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_file: Code/csv/Behav - Happiness_singleTrialData_socialRiskyChoicesOnly.csv
  paper_value: own-win t(39)=-3.58 p<0.001 · own-loss t(39)=-3.39 p=0.002
  reproduced_value: own-win t(39)=-3.57 p=0.0010 · own-loss t(36)=-3.59 p=0.0010
  notes: 'Re-checked 2026-09-11 against the deposited per-trial data, observed by verification/audit_run.py.
    Paper: own-win t(39)=-3.58 p<0.001 · own-loss t(39)=-3.39 p=0.002. Reproduced: own-win t(39)=-3.57
    p=0.0010 · own-loss t(36)=-3.59 p=0.0010. Recorded `unattempted` until this run, while the CSV that
    settles it was already being downloaded by the same script.

    '
- carried_from: guilt-effect-independent-of-own-outcome
  agent: mainen-z
  date: 2026-03-30
  status: unattempted
  notes: null
---

**Notes from extraction:** Shows the guilt effect does not depend on the participant's own outcome, strengthening (validating) the guilt interpretation.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> The ‘guilt effect’ occurred whether the participant received the high lottery outcome (Study 1: t(39) = –3.58, p < 0.001, d = 0.56, BF10 = 32; Study 2: t(43) = –2.68, p = 0.01, d = 0.4, BF10 = 3.8) or the low lottery outcome (Study 1: t(39) = –3.39, p = 0.002, d = 0.54, BF10 = 19; Study 2: t(43) = –3.58, p < 0.001, d = 0.54, BF10 = 33.5).
