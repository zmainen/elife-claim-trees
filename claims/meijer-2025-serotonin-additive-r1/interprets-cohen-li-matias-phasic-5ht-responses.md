---
uuid: 7ebb813f-b228-40bc-ab80-af31a6d7eb3c
slug: interprets-cohen-li-matias-phasic-5ht-responses
doi: 10.1038/ncomms10503
claim: >
  Phasic activation of dorsal raphe serotonergic neurons in response to appetitive and
  aversive stimuli has been documented across complementary recording modalities: single-unit
  electrophysiology (Cohen, Amoroso & Uchida, 2015, eLife 4:e06346), fiber photometry
  (Li et al., 2016, Nat. Commun. 7), and population calcium imaging plus photometry
  (Matias, Lottem, Dugué & Mainen, 2017, eLife 6:e20552). Together these studies establish
  that DRN 5-HT neurons exhibit phasic firing responses time-locked to behaviorally salient
  events, on timescales of hundreds of milliseconds to seconds.
displayClaim: >
  Phasic 5-HT responses to appetitive and aversive stimuli are documented
  electrophysiologically (Cohen 2015), photometrically (Li 2016), and in population
  recording (Matias 2017).
claim-type: interpretive
role: literature-context
concepts:
  - phasic firing
  - DRN serotonergic
  - electrophysiology
  - fiber photometry
  - reward and punishment
priority: 2026-04-19
epistemic: moderate

belongings: []

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: discussion (D2 optogenetics limitation paragraph)
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: literature interpretation; cited in R1 D2 to establish that phasic 5-HT activation is a documented physiological phenomenon, addressing the v1 omission of these direct-recording references
    confidence: moderate

reproductions: []
---

This claim registers the direct-recording evidence base for phasic DRN serotonergic activation that the R1 discussion adds. The v1 manuscript discussed phasic 5-HT activation in response to appetitive/aversive stimuli but cited only Paquelet et al. (2022, calcium imaging) for the population characterization, omitting the spike-resolved evidence from Cohen et al. (2015) and the photometry evidence from Li et al. (2016). The R1 revision adds both, giving the discussion an honest evidence base for the claim that phasic 5-HT activation is a real physiological phenomenon, not an optogenetic artifact.

This is consequential for the scope-bounding of the paper's optogenetic findings (`optogenetic-activation-not-physiological-pattern`). The relevant question is not "does endogenous DRN activation ever occur?" — Cohen, Li, Matias, and Paquelet collectively establish that it does. The relevant question is "does endogenous DRN activation occur in the same temporal and ensemble pattern as ChR2 optogenetic drive?" — and the answer there is more nuanced: phasic activation is real but its ensemble structure (per Paquelet 2022) differs from the broad coordinated drive of ChR2 stimulation, and its temporal kinetics (per Cohen 2015 single-unit data and Li 2016 photometry) are slower than the 25-Hz pulse train used in the present paper.

The R1 D2 paragraph also adds the Kauvar et al. (2025) brain-wide modulation finding for airpuffs, which (when combined with airpuffs activating 5-HT neurons per Matias 2017) raises the inferential possibility that some of those brain-wide effects are 5-HT-mediated. The Kauvar reference is mentioned but not registered as a separate interpretation claim because its function is to support the same scope point rather than to introduce new theoretical content.
