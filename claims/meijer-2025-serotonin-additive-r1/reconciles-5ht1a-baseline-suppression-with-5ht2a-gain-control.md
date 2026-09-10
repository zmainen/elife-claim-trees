---
uuid: f2b05632-4058-416f-8b38-211dc0ee00bd
slug: reconciles-5ht1a-baseline-suppression-with-5ht2a-gain-control
doi: ~
claim: >
  The brain-wide additive signature of 5-HT modulation is consistent with — and may reflect
  the dominance of — a 5-HT1A-mediated stimulus-independent baseline-suppression component,
  while the previously demonstrated 5-HT2A-mediated multiplicative gain modulation of evoked
  sensory responses in visual cortex (Azimi 2020, Barzan 2024) operates as a separable,
  receptor-specific component. Azimi et al. (2020) explicitly dissociated the two
  components: 5-HT1A mediates an additive baseline suppression independent of stimulus
  drive, and 5-HT2A mediates a multiplicative gain on evoked responses. The brain-wide
  additive mode observed here likely reflects dominance of the 5-HT1A component across most
  regions, with 5-HT2A gain control persisting locally where 5-HT2A density is high.
displayClaim: >
  The brain-wide additive mode reflects dominance of a 5-HT1A baseline-suppression
  component over the 5-HT2A gain-modulation component shown in visual cortex —
  reconciling the two prior receptor-specific pictures.
shortClaim: "The additive mode reflects 5-HT1A baseline suppression dominating 5-HT2A gain control."
claim-type: interpretive
role: synthesis
concepts:
  - 5-HT1A
  - 5-HT2A
  - receptor-specific computation
  - baseline suppression
  - gain modulation
  - reconciliation
priority: 2026-04-19
epistemic: moderate
panel: discussion

belongings:
  - relation: requires
    target: hypothesis-additive-modulation
  - relation: requires
    target: 5ht-modulates-all-recorded-regions-bidirectionally

interprets:
  - interprets-5ht2a-gain-control-visual-cortex
  - interprets-lottem-2016-additive-piriform

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: discussion (D9, final paragraph)
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: discussion-level synthesis hypothesis introduced to reconcile the brain-wide additive finding with prior 5-HT2A gain-control literature
    confidence: moderate

reproductions: []
---

This is a new R1 discussion-level synthesis claim that addresses the apparent discrepancy between the brain-wide additive mode reported here and the well-established 5-HT2A-mediated gain control of visual-cortex evoked responses (Azimi 2020, Barzan 2024). The R1 discussion (D9 in the revision notes) introduces the receptor-dependent reconciliation explicitly, citing Azimi et al. (2020) for the 5-HT1A / 5-HT2A dissociation: their visual-cortex recordings dissociated a 5-HT1A-mediated stimulus-independent baseline-suppression component from a 5-HT2A-mediated multiplicative gain modulation of stimulus-evoked responses. The two are separable in their data; they are not two interpretations of the same observation but two distinct receptor-mediated effects with different computational signatures.

The reconciliation hypothesis is that the brain-wide additive mode reported in this paper reflects dominance of the 5-HT1A component across most regions — consistent with `5ht-modulates-all-recorded-regions-bidirectionally` showing widespread modulation that is well-described by an additive shift, with the largest effects in regions with high 5-HT1A density (mPFC, hippocampus). The 5-HT2A gain modulation persists locally where 5-HT2A density is high (visual cortex), but is not the dominant signature when averaged across the recorded regions. This is testable in principle by per-region GLM analysis with regional 5-HT2A density as a moderator, but the paper does not perform this test; the receptor-density predictor analysis (Fig. 3) is on modulation magnitude and direction, not on the choice × stim interaction.

The claim is moderate-epistemic for two reasons. First, it is a discussion synthesis, not directly tested in the data. Second, it relies on the Azimi et al. dissociation being correct; if the 5-HT1A / 5-HT2A separation is itself receptor-pharmacology-confounded the reconciliation rests on shifting ground. Nevertheless it is the conceptually cleanest available reconciliation of the brain-wide additive finding with the prior visual-cortex gain-control finding, and the R1 discussion adopts it explicitly.
