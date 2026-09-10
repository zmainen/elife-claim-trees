---
uuid: 9ac2766f-915b-4a39-822b-1c02e58bca31
slug: orthogonality-derived-from-additivity
doi: ~
claim: >
  In a 2 × 2 factorial choice × stimulation experimental design with linear (PCA)
  projection of the population response, additive 5-HT modulation entails geometric
  orthogonality between the stimulation-effect direction and the choice direction.
  Under additive modulation, every choice trajectory is displaced by the same vector
  (the stimulation effect), so the displacement that distinguishes the stimulated from
  the unstimulated trajectories — averaged across choice — is by definition orthogonal
  to the displacement that distinguishes the choice trajectories — averaged across
  stimulation. The orthogonality result in PCA space (`5ht-axis-orthogonal-to-choice-axis`)
  is therefore a geometric corollary of the GLM additivity finding, not an independent
  empirical claim.
displayClaim: >
  In a 2×2 factorial design under linear projection, additive modulation entails
  orthogonality of the stimulation and choice directions; orthogonality is the
  geometric consequence of the GLM additivity finding.
shortClaim: "Under a linear readout, additive modulation entails orthogonality of the stim and choice axes."
claim-type: interpretive
role: synthesis
concepts:
  - 2x2 factorial design
  - additive modulation
  - subspace geometry
  - linear projection
  - principal components analysis
priority: 2026-04-19
epistemic: strong
status: confirmed
panel: results+discussion

belongings:
  - relation: requires
    target: hypothesis-additive-modulation
  - relation: requires
    target: manifold-from-pooled-super-session

derived-from:
  - hypothesis-additive-modulation

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: results (R5 conclusion), discussion (D1, D9)
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: mathematical derivation under 2×2 factorial design with linear projection; explicit in R1 abstract ("As a geometric consequence of this additivity, 5-HT modulation was confined to a subspace orthogonal to the choice axis"), R5 conclusion ("As a geometric consequence of this additivity, the subspace in which serotonin exerts its effect is orthogonal to the subspace in which choice-related modulation occurs"), and D1 ("As a geometric consequence of this additivity, manifold analysis confirmed that the 5-HT effect axis is orthogonal to the choice axis")
    confidence: strong

reproductions: []
---

This is the second of the two new R1-only synthesis claims and the structural piece that demotes orthogonality from an independent finding to a derivation. Its function is to make explicit a fact about the experimental design and the analysis that v1 left implicit: under a 2×2 factorial choice × stimulation design with linear (PCA) projection, additive modulation and orthogonality of the stimulation and choice directions are mathematically equivalent properties — they are two views of the same underlying computational structure.

The derivation is straightforward. Define the four trial-averaged trajectories L (left choice, no stim), R (right choice, no stim), L_stim (left choice, stim), R_stim (right choice, stim). The choice axis is (L + L_stim)/2 - (R + R_stim)/2, the difference in mean trajectory between left and right choices, averaged across stimulation. The 5-HT axis is (L_stim + R_stim)/2 - (L + R)/2, the difference between stimulated and unstimulated, averaged across choice. Under additive modulation, L_stim = L + δ and R_stim = R + δ where δ is the stimulation displacement vector. Substituting, the choice axis becomes (L + L + δ)/2 - (R + R + δ)/2 = L - R (the δ terms cancel), and the 5-HT axis becomes (L + δ + R + δ)/2 - (L + R)/2 = δ. The two axes are L - R and δ; orthogonality holds whenever δ has no component along L - R, which under additivity is given (the additive offset is independent of choice). The PCA-space orthogonality result is therefore not independent evidence for the additivity hypothesis — it is a geometric restatement of it.

This has two consequences for how the R1 paper should be read. First, the orthogonality measurements (Fig. 5g–i) and the GLM interaction term (Fig. 6c) are not independent confirmations — they should not be combined as if they were two separate tests of the same hypothesis. They are two operationalizations of one underlying property. Second, the v1 framing of orthogonality as the central finding is now visible as a partial picture: it described the geometric signature of the underlying computation but not the computation itself. Naming the computation as additive modulation is the conceptual move that R1 makes.

The two claims (`5ht-axis-orthogonal-to-choice-axis` and `near-zero-choice-by-stim-interaction`) still appear as separate empirical claims in the graph because they are computed from different analyses with different statistical tests — the manifold permutation test and the across-animal t-test respectively. But this synthesis claim flags that they are structurally non-independent, and the reproduction graph should treat them as such (a failure to reproduce one would impugn the other in a way that two genuinely independent claims would not).
