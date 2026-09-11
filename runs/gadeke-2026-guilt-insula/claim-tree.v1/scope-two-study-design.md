---
uuid: aa8d444f-2f3c-4558-8074-f6347d962523
slug: scope-two-study-design
doi: ~
claim: >
  All findings are scoped to a two-study design: Study 1 is an fMRI study of N=40
  young adults run on a 3T scanner using a within-subject lottery paradigm with three
  conditions (Solo, Social, Partner) over two scanning sessions; Study 2 is a
  behavioural-only replication with N=44 independent participants using the same task
  outside the scanner. Both studies use the same EV-maximising algorithmic partner
  (the participants are not told the partner is an algorithm). All neural claims
  derive from Study 1; all behavioural claims are tested in both studies. Conclusions
  about interpersonal guilt are conditional on this paradigm — repeated lottery
  decisions in a constrained risk-taking design with monetary stakes — and on the
  specific population sampled.
displayClaim: >
  Two-study design (fMRI N=40, behavioural N=44) using a within-subject lottery
  paradigm with an EV-maximising algorithmic partner. All neural claims are
  conditional on Study 1; all behavioural claims are tested in both studies.
claim-type: assessment
role: scope
concepts:
  - sample
  - paradigm scope
  - replication
  - within-subject design
  - lottery paradigm
priority: 2026-04-20
epistemic: weak
status: N/A
panel: scope

scopes:
  - lottery-choice-increases-with-ev
  - solo-vs-social-choice-difference
  - risk-premiums-null-social-solo
  - happiness-correlates-partner-reward
  - responsibility-modulates-guilt-computational
  - social-prpe-weight-positive
  - guilt-reduces-happiness-after-partner-loss
  - guilt-effect-independent-of-own-outcome
  - agency-reduces-happiness
  - ventral-striatum-tracks-risky-choices
  - precuneus-tpj-mpfc-social-decisions
  - insula-tracks-guilt-effect
  - ventral-striatum-tracks-computational-reward
  - sts-tracks-partner-reward-prediction-errors
  - insula-ifg-connectivity-guilt
  - insula-guilt-replicates-yu-koban-signature
  - guilt-signature-no-individual-difference

belongings: []

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: scope
    analysis: ~
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: design summary from Methods
    confidence: weak

reproductions:
  - agent: mainen-z
    date: 2026-04-20
    status: blocked
    blocked_by: not-applicable
    # The two-study design: established by reading the Methods, not by running code. A design or scope claim is settled by the paper's own
    # description, so there is no analysis to re-run and no value to compare.
    notes: >
      Confirmed by Methods inspection: Study 1 (N=40, fMRI, two sessions of ~50
      decision trials per condition); Study 2 (N=44, behavioural replication with
      identical task structure outside scanner). Algorithmic partner confirmed via
      `partner-algorithm-deception-assumption`. The two-study structure is the
      paper's principal robustness check against single-sample false positives.
---

This scope claim makes explicit what every empirical claim in the paper inherits about its generalisability. The two-study design is the paper's main internal-replication mechanism: behavioural claims that fail to replicate in Study 2 (notably `solo-vs-social-choice-difference`) are appropriately weakened, while those that replicate (the guilt effect, the social_pRPE positive weight, the EV sensitivity) gain confidence. The neural claims have no internal replication — they are all Study 1 only — and are therefore more dependent on the convergent-validity check via the Yu/Koban signature (`insula-guilt-replicates-yu-koban-signature`) and on prior-literature replication of the risk-and-social-cognition manipulation checks. The constrained lottery paradigm scopes the affective claims: the "guilt" tested here is the affect arising from monetary risk decisions affecting an absent abstract partner, not necessarily the same construct as guilt in face-to-face interaction or moral transgression contexts.
