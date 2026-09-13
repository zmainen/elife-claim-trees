---
uuid: 4f75bdf1-62f6-4027-a3f4-b3ef47129364
slug: hypothesis-d1-d2-temporal-distinction
doi: ~
claim: >
  D1 and D2 receptors encode dopamine signals on distinct temporal scales due to their
  different binding kinetics: D1 receptors (high EC50, fast on-rate) follow extracellular
  DA with millisecond delay and act as detectors of transient burst events, while D2
  receptors (low EC50, slow off-rate) integrate the dopamine signal over seconds and
  cannot resolve brief pauses or closely spaced bursts.
displayClaim: >
  D1 and D2 receptors operate on distinct temporal scales — D1 tracks burst DA with
  millisecond delay; D2 integrates over seconds and cannot resolve brief pauses.
shortClaim: "D1 tracks burst dopamine on milliseconds — D2 integrates tonic dopamine over seconds."
claim-type: hypothesis
role: hypothesis
concepts:
  - D1 receptor
  - D2 receptor
  - receptor kinetics
  - temporal coding
priority: 2026-04-19
epistemic: hypothesis
check_verification: unrecorded
status: N/A
panel: hypothesis

entails:
  - d1r-tracks-da-50ms-delay
  - d2r-integrates-over-seconds
  - d2r-insensitive-to-brief-pauses

belongings: []

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: hypothesis
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: hypothesis stated in abstract and operationalised in Figure 1H–J receptor binding simulations
    confidence: N/A

reproductions: []
---

The D1/D2 temporal-distinction hypothesis is stated almost verbatim in the abstract: "D1 receptor occupancy follows extracellular DA concentration with milliseconds delay, while D2 receptors do not respond to brief pauses in firing but rather integrate DA signal over seconds." The hypothesis is operationalised by the receptor-binding simulations in Figure 1H–J, which compute occupancy under burst and pause stimuli using Hill kinetics. The hypothesis is logically downstream of the regional dynamics work (it requires the model's tonic vs phasic DA fields as input) but conceptually independent: the temporal-scale distinction is a property of the receptor binding kinetics themselves, not of the regional Vmax difference. The empirical findings (50 ms D1R delay, ≥5 s D2R recovery, insensitivity to 1 s pauses) all directly entail from the hypothesis.
