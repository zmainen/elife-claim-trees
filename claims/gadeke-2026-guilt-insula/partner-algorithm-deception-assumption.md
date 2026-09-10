---
uuid: cb673152-8776-46c8-8f13-c95262c2138b
slug: partner-algorithm-deception-assumption
doi: ~
claim: >
  The experiment partner's decisions were in fact made by an expected-value-maximizing
  algorithm (lottery chosen if EV_diff > 0), not by a real person, but participants were
  not informed of this; this deception is a structural assumption underlying all social
  comparison contrasts and the claim that participants felt interpersonal guilt toward
  a real partner.
displayClaim: >
  The "partner" was an EV-maximizing algorithm, not a real person. All
  social-comparison claims inherit this structural validity assumption.
claim-type: assessment
role: scope
concepts:
  - experimental design
  - deception
  - partner simulation
  - validity
  - interpersonal guilt
priority: 2026-03-30
epistemic: weak

scopes:
  - guilt-reduces-happiness-after-partner-loss
  - guilt-effect-independent-of-own-outcome
  - happiness-correlates-partner-reward
  - insula-tracks-guilt-effect
  - insula-ifg-connectivity-guilt
  - sts-tracks-partner-reward-prediction-errors
  - social-prpe-weight-positive
  - responsibility-modulates-guilt-computational
  - insula-guilt-replicates-yu-koban-signature
  - guilt-signature-no-individual-difference
  - precuneus-tpj-mpfc-social-decisions
  - agency-reduces-happiness

belongings:
  - relation: requires
    target: guilt-reduces-happiness-after-partner-loss
  - relation: requires
    target: insula-tracks-guilt-effect
  - relation: requires
    target: sts-tracks-partner-reward-prediction-errors

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: ~
    method: code inspection (Decision task section, Methods)
    confidence: weak

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: not-applicable
    # The partner was an algorithm: established by reading the Methods, not by running code. A design or scope claim is settled by the paper's own
    # description, so there is no analysis to re-run and no value to compare.
    notes: >
      Confirmed by code inspection of Methods section (Decision task, p.15): "the partner's
      decisions were simulated using a simple algorithm that always selected the option with
      the highest expected value". Authors acknowledge this in Discussion as a limitation and
      note that partner outcomes nonetheless influenced participant happiness, arguing the
      effects could be stronger with genuine interaction.
---

This is a structural validity assumption that every social comparison claim in the paper requires. The authors acknowledge it as a limitation in the Discussion. The counter-argument they offer — that partner outcomes still influenced happiness, showing participants were not emotionally detached — is behavioral evidence that the deception was partially effective. The EV-maximizing algorithm creates a predictable (though stochastic) partner that eliminates reciprocal strategic interactions, which the authors argue is analytically advantageous. Whether participants would show stronger guilt effects with a real partner is an open question. This assumption means all "interpersonal guilt" and "social responsibility" claims are strictly interpersonal in the phenomenological sense but have algorithmic structure in the operationalization.
