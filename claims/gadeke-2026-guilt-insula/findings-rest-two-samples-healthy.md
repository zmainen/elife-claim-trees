---
uuid: 2005532f-b003-46be-827f-5597a232f385
slug: findings-rest-two-samples-healthy
doi: null
claim: The findings rest on two samples of healthy adults — Study 1 (behaviour only, N = 40) and Study
  2 (fMRI, N = 44); all BOLD/fMRI results derive from Study 2, while the behavioural results come from
  both studies.
claim-type: assessment
role: scope
concepts: []
priority: '2026-09-13'
scopes:
- when-partner-received-low-lottery
belongings: []
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: null
  readers: high
reproductions:
- carried_from: scope-two-study-design
  agent: mainen-z
  date: 2026-04-20
  status: blocked
  blocked_by: not-applicable
  notes: 'Confirmed by Methods inspection: Study 1 (N=40, fMRI, two sessions of ~50 decision trials per
    condition); Study 2 (N=44, behavioural replication with identical task structure outside scanner).
    Algorithmic partner confirmed via `partner-algorithm-deception-assumption`. The two-study structure
    is the paper''s principal robustness check against single-sample false positives.'
warrant: weak
warrant_why: a scope statement the tree records nothing bearing on
---

**Notes from extraction:** Global scope condition bounding the empirical claims; distinguishes the behavioural study from the fMRI study. The results reader emphasised that BOLD results come only from Study 2; the structure reader gave the two sample sizes.

**Relations.** Why each outgoing edge was inferred:

- `scopes` → `when-partner-received-low-lottery`: the guilt effect is bounded to two samples of healthy adults

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We analysed the BOLD responses of brain regions engaged during decision-making and at the time of receiving the outcomes of the choice using conventional as well as computational model-based analyses, using the fMRI data collected in Study 2.

**structure-reader evidence:**
> Forty healthy participants (14 male, mean age 26.1, range 22–31) participated in Study 1 (behaviour only study), and 44 healthy participants (19 male, mean (SD) age = 30.6 (6.5), range 23–50) participated in Study 2 (fMRI study).
