The synthesis pipeline asks a different question from the paper summary: not "what does this paper argue?" (the summary's question) but "if you give an agent only the claim graph, with no abstract, no PDF, no published prose, can it reconstruct the paper's argument?" The comparator then asks: when the reconstruction is set against the published abstract, what is preserved, what is lost, what is added?

## Strict isolation

The synthesis agent reads only `site/src/data/claims.json` filtered by `paperSlug`. It does not see the paper's title, abstract, authors, or prose. It does not see the paper-summary. It sees only the claim sentences, panel attributions, role labels, epistemic markers, and the typed edges between claims.

Isolation matters: any contamination by the abstract would let the agent recover the paper's framing without the graph having to carry it. The diagnostic value of the synthesis is precisely the comparison against the abstract — what the agent recovers from the graph alone is what the graph is doing the work of carrying; what the agent fails to recover is what the abstract adds beyond the graph.

## Synthesizer prompt

The prompt explicitly enumerates argumentative moves and reasoning forms. The v3 prompt (representative excerpt):

> The claim graph carries multiple kinds of relation, each representing a different argumentative move:
> - `requires` — A depends on B being true. Mechanistic / hierarchical chain.
> - `entails` / `derived-from` — Hypothesis → prediction. Deductive entailment.
> - `tests` — Empirical claim → prediction it tests.
> - `supports` / `refutes` — Empirical claim → hypothesis it supports or refutes. Abductive inference.
> - `rules-out` — A's evidence eliminates an alternative. Argument by elimination.
> - `dissociates-with` — A and B jointly establish a dissociation. Argument by contrast.
> - `validates` — A is a control or sign-flip that strengthens B. Argument by disconfirmation.
> - `predicts` / `confirms` — predictive validation across model and experiment.
> - `scopes` — A is a boundary condition on B. Argument by qualified scope.
> - `interprets` — A reframes empirical B through theoretical / literature lens.
> - `enables-method` — A is the methodological capability that warrants B's interpretability.
>
> Scientific argument typically combines three reasoning forms:
> - Deduction — `entails`/`derived-from` edges.
> - Induction — `requires`/`supports` edges.
> - Abduction — `supports`/`refutes` from observation back to hypothesis.
>
> Use the right rhetorical move for the right structural relation. When `refutes:` edges are present, articulate the refutation explicitly. When a hypothesis is `derived-from:` another, articulate it as a logical consequence rather than as an independent finding. When `rules-out:` is present, surface the eliminated alternative.

The prompt's job is to license the right rhetorical move for the right edge type. Without explicit guidance, the agent tends to flatten `refutes` into `is consistent with` and to omit `rules-out` entirely; the prompt has been iterated to push back on these defaults.

The agent emits two outputs: a synthesis paragraph (200–400 words) and a per-sentence traceback that names the claims and edges each sentence draws on. The traceback is the audit trail.

## The comparator

The comparator is run separately, with both texts available — the synthesised reconstruction and the published abstract. It produces a sentence-by-sentence mapping (`site/src/data/abstract-mapping/<paper-slug>.json`) that records, for each abstract sentence: its type (`background` / `claim`), the claim slugs it maps onto, the kind of mapping (`direct` / `combined` / `compressed` / `flattened`), and a free-text note about what is preserved or lost.

The comparator also lists `orphanClaims` (claims present in the graph but not surfaced in the abstract) and `orphanSentences` (abstract content with no graph counterpart). These are the divergence inventory.

## What the comparator finds

Two diagnostic patterns recur across the {{papers}} papers:

1. **`rules-out` and `refutes` edges are scrubbed by abstracts.** The eliminative move is consistently flattened. The Meijer R1 abstract states the additivity finding; the synthesis surfaces both the additivity finding and the explicit refutation of the multiplicative-gain prediction. The abstract's "5-HT modulates spiking additively" carries the same proposition as the synthesis's "additive prediction confirmed and multiplicative prediction refuted, eliminating gain control as the dominant brain-wide mode," but the rhetorical move from refutation to elimination is absent. The abstract reader cannot tell that the paper is engaging an explicit alternative.

2. **`validates` edges (controls) are absorbed.** The Meijer R1 abstract names the 7,478-neuron / 13-region scope but does not mention that wild-type controls rule out the light artefact, that narrow-spike interneurons rule out an FSI-driven mechanism, or that layer-stratified analysis rules out a layer-specific cortical mechanism. The synthesis surfaces all three; the abstract presents the empirical findings as if the controls had not needed to be run.

These findings are robust to LLM stylistic variation — they describe structural properties of the abstract relative to the graph (which edges are absent as rhetorical moves), not surface features. The magnitude of the gap is less robust (Section 9).

## Iteration history

The synthesis pipeline went through three iterations.

**v1 — hierarchical-only synthesis** (`site/src/data/synthesis/`). The first prompt used only `requires` edges (read as a directed acyclic graph) and asked for a paragraph in the style of an abstract. The output read as a flattened restatement of the empirical findings, organised hierarchically. Hypotheses were not surfaced because v1 did not use the role labels; the hypothetico-deductive structure was invisible.

**v2 — enriched edges** (deprecated; not preserved as a separate directory). The second iteration added `supports`, `tests`, `entails`, `derived-from`, `dissociates-with`, and `interprets` to the prompt, and organised the synthesis around the `role: hypothesis` claims. The output recovered the deductive structure but underplayed the abductive loop — empirical claims supported hypotheses without explicitly closing the prediction-test loop.

**v3 — explicit hypothetico-deductive surfacing with refutation arc** (`site/src/data/synthesis-v3/`). The third iteration is the current production prompt. It enumerates the eleven edge types explicitly, names the three reasoning forms (deduction / induction / abduction) with edge-form mappings, instructs the agent to articulate refutations explicitly when `refutes:` edges are present and to surface eliminated alternatives explicitly when `rules-out:` is present, and to mark `derived-from:` between hypotheses (as in the Meijer R1 case where `hypothesis-orthogonal-neuromodulatory-subspace` is `derived-from: hypothesis-additive-modulation`) as logical consequence rather than independent finding.

The v3 outputs are the basis for the comparator findings above. v1 outputs are preserved for the five papers where they were generated, as a rough lineage of how the pipeline's diagnostic resolution improved.

[↑ Contents](#contents)

---
