---
uuid: 6cdf645a-3865-433f-ac5f-308630199916
slug: individual-grbs-dot-product-values-not
doi: null
claim: Individual GRBS dot-product values did not correlate with the behavioural guilt responses (Spearman's
  Rho = –0.058, p = 0.725), indicating the neural signature does not track individual differences in behavioural
  guilt sensitivity.
claim-type: empirical
role: control
concepts: []
priority: '2026-09-13'
belongings: []
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: null
  readers: single-source
reproductions:
- carried_from: guilt-signature-no-individual-difference
  agent: mainen-z
  date: 2026-09-11
  status: partial
  script: verification/gadeke-2026-guilt-insula/verify.py
  script_execution: executed
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_file: fMRIresults/outcome/guiltEffectEachPartic.nii
  paper_value: Spearman rho=-0.058, p=0.725
  reproduced_value: 'rho=0.088, p=0.588, n=40 — null reproduces, coefficient differs from the reported
    -0.058. Volume i is assumed to be row i: the deposit ships no participant order for the 4D map, so'
  notes: 'Re-checked 2026-09-11 against the deposited group statistical map, observed by verification/audit_run.py.
    Paper: Spearman rho=-0.058, p=0.725. Reproduced: rho=0.088, p=0.588, n=40 — null reproduces, coefficient
    differs from the reported -0.058. Volume i is assumed to be row i: the deposit ships no participant
    order for the 4D map, so the pairing cannot be confirmed from it.. The substantive claim — no correlation
    between the neural signature and individual behavioural guilt — reproduces; the coefficient does not
    match the reported value, and the deposit ships no participant order for the 4D map, so volume-to-row
    pairing is assumed rather than confirmed.

    '
- carried_from: guilt-signature-no-individual-difference
  agent: mainen-z
  date: 2026-03-30
  status: unattempted
  notes: null
warrant: weak
warrant_why: the tree records nothing bearing on this null control
---

**Notes from extraction:** Null result: the neural signature does not track individual differences in behavioural guilt sensitivity.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We assessed whether inter-individual differences in these dot product values correlated with the behavioural guilt responses, but did not find a significant association [Spearman’s Rho = –0.058, p = 0.725].
