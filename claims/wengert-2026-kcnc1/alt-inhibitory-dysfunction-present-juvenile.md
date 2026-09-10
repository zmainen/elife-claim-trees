---
uuid: 8f0f1866-b184-4166-8ed7-97af70a45e88
slug: alt-inhibitory-dysfunction-present-juvenile
doi: ~
claim: >
  Inhibitory dysfunction in Kcnc1-A421V/+ mice is already established at the juvenile stage
  (P16-21) rather than emerging with age, so the phenotype is developmentally static rather
  than progressive.
claim-type: interpretive
role: hypothesis
concepts:
  - developmental progression
  - inhibitory dysfunction
  - alternative explanation
priority: 2026-09-10
epistemic: weak

assertions:
  - paper-slug: wengert-2026-kcnc1
    doi: 10.7554/eLife.103784
    stance: rejects
    method: agent extraction of the reading the paper's own claim notes named and excluded
    confidence: weak

reproductions: []
---

An alternative the paper argues against, not a proposition it asserts.

This claim exists because the corpus had already written it down in prose. The note on
`pv-in-inhibitory-synapse-intact-juvenile` read: *"this claim both supports and contradicts
the developmental progression claim depending on the angle. It supports the temporal framing
(juvenile normal, adult altered) but contradicts a naive reading of 'inhibitory dysfunction
present at juvenile.'"* The naive reading is the thing being contradicted — and it had no
node, so the `contradicts` edge was aimed at the progression claim the same result supports.

The resolution the note gives is the real content: firing-frequency impairment **is** present
in juveniles, while synaptic-per-spike function is not. So the phenotype is neither wholly
present nor wholly absent at P16-21, which is what makes the static reading wrong.
