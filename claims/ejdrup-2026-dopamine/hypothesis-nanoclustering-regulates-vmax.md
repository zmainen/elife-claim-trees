---
uuid: 08b37324-70f4-4ff9-bf37-c73d2b8a43c4
slug: hypothesis-nanoclustering-regulates-vmax
doi: ~
claim: >
  DAT nanoclustering acts as a possible regulator of effective DAT activity in striatum: when
  transporters are concentrated into dense nanoclusters rather than uniformly distributed,
  local depletion at the cluster surface creates a diffusion-limited bottleneck that lowers
  the effective Vmax even at constant total DAT expression — proposing nanoclustering as one
  candidate mechanism for the lower effective Vmax in VS than DS.
displayClaim: >
  DAT nanoclustering is a possible regulator of effective transporter activity, with denser
  clusters lowering effective Vmax via diffusion-limited substrate access — proposed as one
  contributor to the regional Vmax difference.
shortClaim: "DAT nanoclustering lowers effective Vmax and helps set regional dopamine dynamics."
claim-type: hypothesis
role: hypothesis
concepts:
  - DAT nanoclustering
  - effective Vmax
  - diffusion limitation
  - regional regulation
priority: 2026-04-19
epistemic: hypothesis
check_verification: unrecorded
status: N/A
panel: hypothesis

entails:
  - dat-nanoclustering-slows-clearance
  - dat-clustering-greater-in-vs

belongings: []

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: hypothesis
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: hypothesis stated in abstract ("our simulations posit DAT nanoclustering as a possible regulator") and developed in Figure 4
    confidence: N/A

reproductions: []
---

The nanoclustering hypothesis is the paper's secondary contribution. It bridges a varicosity-scale simulation result (denser DAT clusters slow DA clearance via diffusion limitation, even at constant total Vmax) with a super-resolution dSTORM observation (DAT is more nanoclustered in VS than DS). The two findings are presented as compatible with — but not as proof of — a causal pathway from nanoclustering to the regional Vmax difference. The paper is careful to call this a "possible" regulator rather than an established cause; the architectural separation between the varicosity-scale and tissue-scale models (`nanoclustering-model-varicosity-scale`) and the constant-Vmax constraint (`nanoclustering-constant-vmax-constraint`) limit how strongly the empirical results can corroborate the hypothesis.
