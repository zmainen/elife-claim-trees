# Method

This document describes the procedure by which a published paper is translated into a claim graph, the schema in which that graph is stored, the verification step that re-enacts the paper's analysis against deposited code and data, the paper-summary and synthesis-comparator pipelines layered on top, and the limits of what the present prototype actually executes versus what it documents. It is a methodology reference for the corpus described in `site/src/data/claims.json`, not a prospectus.

The document covers the scientific methodology: schema, claim authoring, verification, the synthesis and comparator pipeline, and the literature-context primitive. It does not cover the web rendering of the corpus.

---

## Contents

1. [Overview](#1-overview)
2. [Corpus](#2-corpus)
3. [Claim induction](#3-claim-induction)
4. [Schema](#4-schema)
5. [Verification procedure](#5-verification-procedure)
6. [Paper summaries](#6-paper-summaries)
7. [Synthesis and comparator pipeline](#7-synthesis-and-comparator-pipeline)
8. [Literature-context as cross-paper primitive](#8-literature-context-as-cross-paper-primitive)
9. [Limits and openings](#9-limits-and-openings)

---

## 1. Overview

A claim graph is a decomposition of a scientific paper into typed propositions and the typed logical relations between them. Each proposition is one declarative sentence in active voice, recorded with provenance (which paper asserts it, in which panel, using which analysis and dataset), an epistemic marker, and a reproduction status. Relations are not citations; they are statements about logical structure — `A requires B` means A's validity depends on B's, so invalidity propagates through the graph when a claim fails to reproduce.

The unit of work is the claim, not the figure. A figure panel records where a paper instantiates a claim; the claim is the stable entity. The same proposition could be asserted by different papers in different panels — the UUID identifies the claim while one or more `assertions` blocks attach it to specific paper-panel-analysis tuples.

The method has two distinct phases. **Claim induction** is the process of reading a paper and extracting its claim structure — the propositions, their roles, their logical dependencies, and their provenance (which figure panel, which analysis, which dataset). Claim induction is a reading act: it requires comprehension of the paper's argument and judgment about what constitutes a claim. It produces a claim graph. **Claim verification** is the process of running code against deposited data to check whether an induced claim reproduces. Verification is an execution act: it requires data, code, and compute. It produces a pass/fail/warn verdict per claim, optionally with reproduced figures that can be compared to the published originals.

The two phases are separable. A claim graph is valuable before any verification runs — it makes the paper's argument structure explicit and navigable. Verification adds an empirical layer: did the computation actually produce the reported result? But induction comes first, and induction is where provenance should be captured — figure URIs, panel assignments, dataset links — because the agent performing induction has the paper's structured source (JATS XML, PDF) in front of it. Deferring provenance capture to a later build step (e.g. guessing figure filenames from panel labels) is fragile and loses information that was available at induction time.

The corpus is a {{papers}}-paper prototype assembled to test whether the schema is expressive enough to capture the argumentative structure of recent neuroscience papers, whether the verification step can re-enact published analyses against deposited data and code, and whether downstream pipelines (paper summaries, synthesis from the claim graph alone, comparison against the published abstract) yield findings that would not be visible from the prose alone. It is reverse-engineered from finished papers; forward construction by authors at submission would look different.

What this document is not: a specification of how the schema should evolve at scale, a proposal for editorial workflow, or a comparison with related schemes (Wikidata, Semantic Web claim representations, micropublications). Those discussions belong elsewhere.

[↑ Contents](#contents)

---

## 2. Corpus

The published corpus is **{{papers}} papers** from eLife, spanning the journal's neuroscience subfield mix. Two further papers — the two bioRxiv versions of one preprint — are carried as method examples rather than corpus members: they are the only pair here that shows how a claim tree changes between a preprint and its revision, and they are counted separately everywhere ({{method_example_claims}} claims across {{method_example_papers}} versions), never folded into a corpus total.

Total: **{{claims}} claims** across {{papers}} papers, carrying **{{relations}} typed relations** — {{relation_types_used}} of the {{relation_types_defined}} relation types the vocabulary defines, and all {{roles_used}} roles.

**Distribution by `role`:**

| Role | Count |
|:-----|---:|
| empirical | 139 |
| prediction | 46 |
| hypothesis | 31 |
| control | 27 |
| scope | 23 |
| methodological | 16 |
| literature-context | 12 |
| synthesis | 9 |
| interpretation | 7 |
| **Total** | **{{claims}}** |

**Per-paper claim counts:** artiushin 17, bouyeure 30, ejdrup 25, gadeke 27, headley 26, kammer 23, kolb 20, meijer-orthogonal 24, meijer-additive-r1 41, rozak 23, scheller 23, wengert 31.

The R1 revision of the Meijer paper carries 41 claims against 24 in the v1 preprint — the inflation reflects new hypotheses (additivity, orthogonality-as-derivation), new empirical claims (per-neuron GLM coefficients, receptor-expression GLM), and new literature-context nodes added to anchor the receptor-pharmacological reframing.

[↑ Contents](#contents)

---

## 3. Claim induction

> ## No human checks this corpus
>
> **Every claim in this repository was produced by a language model, and no person has
> verified any of it.** That is true of the whole pipeline, not one step of it:
>
> - The claims are **found** by three model calls reading the paper independently, and
>   **reconciled** by a fourth.
> - The relations between claims — the deductive spine — are **inferred** by a model call.
> - The method requires an analyst's review gate. There is no such gate. What stood in
>   for one was a flag — `--review-mode external`, which is **another model** revising the
>   draft, or `--review-mode auto-approve`, which wrote the files unread — and both are gone.
>   The model's revision is now a declared layer, `external-review`, so changing the prompt
>   behind it makes every claim tree built on it stale. Approval is what it should always have
>   been: an operation on a version that already exists, recorded in
>   `runs/<paper>/approvals.jsonl` by `scripts/pipeline.py approve`. That file is empty for
>   every cell in this corpus — the same fact as before, now stated where it can be checked
>   rather than inferred from a default.
> - The `agent:` field on a verification record names **the agent identity that ran the
>   script**, not a person who checked the result. All 225 records read `agent: mainen-z`;
>   none of them means Zach Mainen read that claim.
> - The coverage verdicts in `mappings/` — `covered`, `gap`, `no-assertion` — are **model
>   judgements**, made from the paper and the claim text.
>
> Read the corpus as **a draft annotation layer**, not as adjudicated output. Where this
> document says "curated", it means "assembled by this pipeline", not "checked by a person".
>
> A human-review step is compatible with the format — claim files carry provenance fields,
> and the tooling can already write anchored comments and claim assignments into the paper
> for a person to disposition. **It is not implemented, and it has not been run.** Adding it
> would be a change to the method, and would be recorded here as one.

Claim induction is the translation of a paper from argument format into claim-graph format. It demands reading comprehension, domain judgment, and decisions about what constitutes a claim — and in this version a model makes all of them.

Induction is not one act but a sequence of them, and each is a declared layer with its own
question, its own inputs and its own record of having run. What each does, and how, is
documented beside its declaration in `pipeline/layers/` and gathered in the
[Layers](#layers) section. What follows here is what holds across all of them.

### Reading the abstract first

Read the abstract and identify two to four top-level claims — the paper's main bets. For each, write a candidate slug (3–5 words, lowercase, hyphenated, verb-phrase form). These will be the synthesis or interpretation nodes at the top of the dependency graph. They typically have no single figure of their own — they are the synthesis of the figures below them. The Headley paper, for example, surfaces `pv-gamma-sst-beta-correspondence` as a single synthesis node interpreting the simulation results in light of prior interneuron-rhythm associations; this node's panel is "fig10 (synthesis / discussion)" rather than a single quantitative panel.

### Why three readers

The three agents are deliberately partitioned along the axes along which extractions most often disagree: framing versus literal numerics versus computational structure. A claim that all three surface independently is high-confidence; a claim that only one surfaces is single-source and may be either real-but-buried or an artefact of the reading strategy. The `reconcile` layer records both cases distinctly.

### Where short-form fields fit

Three fields are populated during authoring but are not the primary claim sentence:

- **`displayClaim`** (one to two sentences) is the form rendered when the claim is presented in body text or in a card view. It softens the formal `claim` sentence into something readable in a paragraph; it preserves the proposition's content but allows shorter constructions, parenthetical units, and contractions where the formal `claim` field cannot. Authored with the claim files; can be revised without changing the underlying claim.

- **`shortClaim`** (single short clause, ≤90 characters typical) is the headline form: what fits in a tooltip, a hover preview, or a graph-node label. Required for synthesis, interpretation, and literature-context nodes that must be readable at a glance in the synthesis layer; optional but recommended for hypotheses, predictions, and high-traffic empirical claims. Authored with the claim files.

- **`number`** and **`numberParts`** are not authored manually. They are computed by the build pipeline from the claim's `role` and its position in the dependency graph (hypotheses get `H#`, predictions hang off the hypothesis they `derived-from` as `H#.P#`, empirical claims testing those predictions hang off as `H#.P#.E#`, scope claims become `Sc#`, methodological become `M#`, controls become `C#`, literature-context becomes `L#`, synthesis becomes `S#`, interpretation becomes `I#`, and standalone empirical not under any hypothesis loop become `E#`). The numbering is regenerated on every build; do not paste numbers into source files.

`role` is assigned at the review gate and is the most consequential single field in the schema after `claim`, because it governs how the `synthesis` layer groups the claim and how the claim is numbered in the build.

[↑ Contents](#contents)

---

## 4. Schema

One markdown file per claim, stored at `claims/<paper-slug>/<claim-slug>.md`. The file has YAML frontmatter and an optional markdown body for prose elaboration. The body is for caveats, alternative interpretations, pointers to contradicting claims in other papers, and reasoning that does not compress into frontmatter; it is rendered as prose where the claim is displayed in detail.

### 4.1 Required frontmatter

| Field | Value |
|:------|:------|
| `uuid` | UUID4, generated once at creation, immutable |
| `slug` | filename slug, lowercase, hyphenated, 3–6 words, verb phrase |
| `doi` | placeholder `~` for now (claims are not yet citable units) |
| `claim` | one declarative sentence, active voice, quantitative where the result is quantitative |
| `claim-type` | `empirical` / `interpretive` / `existence` / `synthesis` / `assessment` / `hypothesis` / `prediction` |
| `role` | one of nine values (Section 4.2) |
| `concepts` | controlled list of domain terms |
| `priority` | date the claim was first registered |
| `epistemic` | `strong` / `moderate` / `weak` / `contested` (analyst's overall assessment of support across all assertions) |
| `assertions` | list of blocks linking the claim to specific paper-panel-analysis tuples |
| `reproductions` | list of blocks recording verification attempts |

`claim-type` and `role` are orthogonal axes: `claim-type` is the epistemic character of the proposition (is it observed, inferred, asserted to exist, synthesised, or methodological?); `role` is the rhetorical function the claim serves in this paper's argument. A `claim-type: empirical` claim can carry `role: empirical`, `role: control`, or `role: scope` depending on whether it is the primary observation, a check that rules out an alternative, or a boundary condition.

### 4.2 Roles — the role inventory

Role is the rhetorical function the claim plays in the paper's argument. The synthesis pipeline reads this field directly to organise reconstruction.

| Role | What it marks | Typical claim-type |
|:-----|:--------------|:-------------------|
| `hypothesis` | The paper's organising hypothesis or framing question. Anchors deductive chains via `entails:` to predictions. | `hypothesis` |
| `prediction` | A specific empirical prediction derivable from a hypothesis. Carries `derived-from:` back to its hypothesis and is `tests:`-targeted by empirical claims. | `prediction` |
| `empirical` | A measured or computed result, panel-grounded. The largest role bucket ({{largest_role_n}} of {{claims}}). | `empirical` |
| `control` | A check ruling out an artefactual or alternative explanation. Carries `scopes:` or `rules-out:` edges. | `empirical` |
| `scope` | A boundary condition that qualifies a set of claims (single-cell scope, dataset boundary, optogenetic-vs-physiological scope). Often global (`scopes: ["*"]`). | `assessment` |
| `methodological` | A procedural or analytical capability that warrants a downstream interpretation (manifold-from-pooled-super-session, particular sorting pipeline). Carries `enables-method:`. | `assessment` |
| `synthesis` | A claim integrating across multiple empirical claims into a higher-order proposition (the dissociation, the receptor-reconciliation). Top of the within-paper graph. | `synthesis` / `interpretive` |
| `interpretation` | A reframing of an empirical result through theoretical lens, marked separately from synthesis. Carries `interprets:` edges. | `interpretive` |
| `literature-context` | A cited prior claim treated as a first-class node. Section 5. | `interpretive` |

### 4.3 Edges — the edge inventory

Edges are propositions about logical structure between claim entities, not citations. Each is a top-level YAML key whose value is a list of target slugs. Reciprocal edges (`predicts` / `confirms`) are populated symmetrically at build.

| Edge | Reasoning form | Meaning | Count in corpus |
|:-----|:---------------|:--------|---:|
| `requires` | dependency | A would be invalid if B were false (mechanistic / hierarchical dependency). | {{relation_counts.requires}} |
| `supports` | abduction (induction) | A provides evidence for B; multiple supports drive the abductive loop. | {{relation_counts.supports}} |
| `entails` | deduction | A (typically a hypothesis) deductively implies B (typically a prediction). | {{relation_counts.entails}} |
| `derived-from` | deduction | A is the deductive consequence of B; reciprocal of `entails`. | {{relation_counts.derived-from}} |
| `tests` | deduction → empirical loop | Empirical claim A tests prediction B (closes the hypothesis-prediction-test loop). | {{relation_counts.tests}} |
| `refutes` | abduction (negative) | A's evidence is incompatible with B (B is the prediction, hypothesis, or alternative being refuted). | {{relation_counts.refutes}} |
| `rules-out` | elimination | A's evidence eliminates an alternative explanation B. | {{relation_counts.rules-out}} |
| `dissociates-with` | dissociation | A and B jointly establish a dissociation (symmetric edge between two empirical claims that together form a contrast). | {{relation_counts.dissociates-with}} |
| `validates` | disconfirmation control | A is a control or sign-flip whose specific result strengthens the warrant for B. | {{relation_counts.validates}} |
| `predicts` | predictive validation | A predicts B (typically model-to-experiment). | {{relation_counts.predicts}} |
| `confirms` | predictive validation | Reciprocal of `predicts`; populated at build. | {{relation_counts.confirms}} |
| `interprets` | reframing | A reframes empirical B through theoretical lens (this is an act of mapping, not a derivation). | {{relation_counts.interprets}} |
| `enables-method` | methodological warrant | A is the methodological capability that warrants B's interpretability. | {{relation_counts.enables-method}} |
| `scopes` | scope qualification | A is a boundary condition on B (or, if `["*"]`, on every empirical claim in the paper). | {{relation_counts.scopes}} |

### 4.4 Edge-to-reasoning-form mapping

The edge inventory operationalises six argumentative moves:

1. **Deduction.** `entails` and its reciprocal `derived-from` carry hypothesis-to-prediction deduction. The Headley paper's `hypothesis-distinct-compartmental-roles` `entails:` four predictions; each prediction `derived-from:` the same hypothesis. The Meijer R1 paper's `hypothesis-additive-modulation` `entails:` `prediction-near-zero-choice-stim-interaction` and (notably) `entails:` `orthogonality-derived-from-additivity` — a synthesis claim that is itself a deductive consequence of the hypothesis, demoting the empirical orthogonality finding from independent evidence to geometric corollary.

2. **Induction (hierarchical support).** `requires` and `supports` carry mechanistic dependency and inductive support. Standalone empirical claims that are not themselves predictions tested in a hypothesis loop nonetheless carry `supports:` edges to higher-order claims via inductive accumulation. The Headley `ca-spikes-couple-20ms-before-ap` `supports` `beta-bidirectional-dendritic-control` and `beta-gates-distal-apical-inputs` — the timescale measurement is the inductive ground for the period-matching argument.

3. **Abduction.** `supports` and `refutes` from empirical claims back to hypotheses close the abductive loop. The Meijer R1 `near-zero-choice-by-stim-interaction` `supports: hypothesis-additive-modulation` and `refutes: prediction-multiplicative-gain-yields-significant-interaction` — abduction to additivity by elimination of the alternative.

4. **Elimination.** `rules-out` carries the eliminative move: A's evidence eliminates an explicit alternative B. The Meijer R1 paper's `rules-out-multiplicative-gain-control` synthesis claim explicitly aggregates this move at the discussion level. The corpus carries 15 `rules-out` edges, scattered across papers, and the `synthesis` layer shows they are diagnostically interesting because they are scrubbed by abstracts.

5. **Dissociation.** `dissociates-with` is a symmetric edge between two empirical claims that together establish a contrast. The Headley `distal-inhib-drops-firing-02hz` `dissociates-with` `perisomatic-inhib-drops-firing-07hz` — neither claim alone establishes the compartmental dissociation; the contrast does. The corpus carries 65 such pairings, often joined to the shared hypothesis they jointly support.

6. **Scope qualification.** `scopes` carries the boundary condition. A scope claim with `scopes: ["*"]` qualifies every empirical claim in the paper. The Headley paper's two global-scope claims (`l5-model-single-cell-scope`, `naturalistic-drive-parameterization`) qualify all empirical results — no network dynamics, no sensitivity analysis over synaptic parameters. The Meijer R1 paper's `optogenetic-activation-not-physiological-pattern` scopes the brain-wide additivity claim to optogenetic stimulation, leaving open whether endogenous, mixed-selectivity DRN release would yield the same signature.

### 4.5 Auxiliary fields

**`displayClaim`** — one to two sentences, used in body text and card views; preserves the proposition while allowing readable phrasing.

**`shortClaim`** — single short clause for graph nodes and tooltips; required for synthesis / interpretation / literature-context nodes, recommended for high-traffic claims.

**`number` / `numberParts`** — computed at build from role + graph position; do not author manually. The numbering convention is hierarchical: `H1.P2.E1` reads as "first hypothesis, second prediction, first empirical test." Standalone empirical (no hypothesis loop) become `E#`; controls `C#`; scope `Sc#`; methodological `M#`; literature-context `L#`; synthesis `S#`; interpretation `I#`. 242 of the 245 published claims carry computed numbers.

**`reproductions:`** — list of blocks. Each block records a verification attempt:

```yaml
reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: verified
    script: verification/<paper-slug>/verify.py
    original_figure: verification/originals/<paper-slug>/fig4.jpg
    figure: verification/<paper-slug>/fig4a-firing-rates.png
    original_script: <URL to deposited notebook>
    script_execution: unmodified | patched | from-notes
    script_execution_note: short string describing any patch
    time_fast: "~2 min"
    time_full: "~6 hrs (NEURON + 1.88 GB Dryad)"
    notes: |
      Free prose recording reproduced numerics, comparison with paper,
      and any caveats. The notes field is the primary place where the
      reproduction's evidentiary basis is recorded.
```

**`status`** vocabulary (per `reproductions[].status`) — see the `verification` layer for criteria.

| Status | Meaning |
|:-------|:--------|
| `verified` | Ran the analysis end-to-end (or read the deposited intermediate); output matches the assertion within tolerance |
| `verified:partial` | Ran a defined subset; matched portion documented in `notes` |
| `unverified` | Not yet attempted (default; reason genuinely unknown) |
| `unverified:no-data` | Data deposit not accessible |
| `unverified:no-code` | Code not accessible |
| `unverified:code-error` | Code runs but errors before producing output; record the exact error and any known fix |
| `unverified:compute-infeasible` | Code runs but would require compute beyond available resources; record estimated runtime and any deposit-first workaround |
| `failed:mismatch` | Ran; output does not match — discrepancy logged in `notes` |

`unknown` appears in 95 claims of the rendered `claims.json`; this reflects either the absence of a `reproductions:` block on the source claim file (default `unknown`) or a non-empty block whose `status` was never set. It should be read as "not yet adjudicated" rather than as a verification outcome.

### 4.6 Examples per role and edge

A single example per role, drawn from the corpus:

- **`hypothesis`.** `hypothesis-distinct-compartmental-roles` (Headley): "Perisomatic and distal dendritic inhibition serve distinct computational roles… `entails:` four predictions." A hypothesis carries `entails` edges to its predictions; it does not itself carry empirical content.

- **`prediction`.** `prediction-beta-optimal-distal` (Headley): "If the optimal frequency of rhythmic inhibition at a compartment is set by matching the rhythm period to the local spike timescale, then distal inhibition should be maximally effective at beta (~20 Hz)." Carries `derived-from: hypothesis-frequency-compartment-matching`.

- **`empirical`.** `distal-inhib-drops-firing-02hz` (Headley): "Doubling distal dendritic inhibition reduces somatic firing rate from approximately 5.5 Hz to approximately 0.2 Hz, primarily by suppressing dendritic Ca²⁺ and NMDA spikes." Carries `tests`, `dissociates-with`, `requires`, and `supports` edges — the typical density for a load-bearing empirical claim.

- **`control`.** `cortical-layers-show-no-differential-modulation` (Meijer R1): "Splitting cortical recordings by layer reveals no differences in modulation fraction, sign, or latency. This rules out a layer-specific cortical mechanism." Empirically computed but functions to eliminate an alternative.

- **`scope`.** `l5-model-single-cell-scope` (Headley): "All results come from a single-cell compartmental model… no network dynamics, no recurrent excitation, no population effects." Carries `scopes: ["*"]`, qualifying every empirical claim.

- **`methodological`.** `manifold-from-pooled-super-session` (Meijer R1): "Manifold analysis is on a pooled super-session… nulls are block-aware shuffles." Carries `enables-method:` and `scopes:` edges to the manifold-derived empirical claims.

- **`synthesis`.** `orthogonality-derived-from-additivity` (Meijer R1): "Under a linear readout, additive modulation entails orthogonality of the stim and choice axes." Carries `derived-from: hypothesis-additive-modulation` — a deductive synthesis that demotes orthogonality from independent finding to geometric corollary.

- **`interpretation`.** `pv-gamma-sst-beta-correspondence` (Headley): "Layer 5 inhibitory streams are functionally matched to interneuron type." Carries `interprets:` edges to the four empirical claims that ground the mapping.

- **`literature-context`.** `interprets-pv-gamma-sst-beta-associations` (Headley): the inherited PV/gamma–SST/beta correspondence from prior literature. Section 5 develops this role.

[↑ Contents](#contents)

---

## 5. Literature-context as cross-paper primitive

`literature-context` is the ninth role, added in iteration 4 of the schema. It treats cited prior work as a first-class claim node — not a citation in a bibliography, but a proposition with the same schema as any other claim, that the present paper's argument inherits.

### 5.1 Distribution

Twelve `literature-context` claims appear across eight papers in the present corpus:

| Paper | Count | Examples |
|:------|---:|:---|
| meijer-2025-serotonin-additive-r1 | 5 | `interprets-gain-control-default-framework`, `interprets-5ht2a-gain-control-visual-cortex`, `interprets-lottem-2016-additive-piriform`, `interprets-cohen-li-matias-phasic-5ht-responses`, `interprets-paquelet-correlated-ensembles` |
| ejdrup-2026-dopamine | 2 | `interprets-cragg-rice-vmax-ratio`, `interprets-may-wightman-1989-fscv` |
| gadeke-2026-guilt-insula | 1 | (single literature-context anchor) |
| headley-2026-inhibitory-rhythms | 1 | `interprets-pv-gamma-sst-beta-associations` |
| kammer-2026-foveal-feedback | 1 | (single literature-context anchor) |
| meijer-2025-serotonin-orthogonal | 1 | (single literature-context anchor) |
| scheller-2026-self-prioritization | 1 | (single literature-context anchor) |
| **Total** | **12** | |

The Meijer R1 paper is the densest case because its central reframing (additivity rather than gain control) requires explicit engagement with the prior-literature gain-control framework. Without literature-context nodes, the `rules-out: multiplicative-gain-control` synthesis claim would have no explicit referent for "multiplicative gain control" — the move would be eliminative against an unnamed alternative. The literature-context node `interprets-gain-control-default-framework` makes the Servan-Schreiber lineage explicit, so that the eliminative move has something specific to engage.

### 5.2 Structural function

A literature-context claim is structurally distinct from an interpretation claim in two respects.

First, its empirical content is not the present paper's evidence — it is content from a cited prior paper (or several), inherited as a load-bearing premise. The claim file's `assertions:` block records this: `method: literature interpretation; cited as the receptor-specific instantiation of the gain-control framework for serotonin`. The `confidence` is bounded by the strength of the prior literature, not by anything the present paper does.

Second, its role in the graph is to give downstream synthesis or scope claims an explicit referent. The Headley `interprets-pv-gamma-sst-beta-associations` claim explicitly notes: "The literature-context registration matters because the correspondence claim is specifically not a prediction the paper tests — the paper's simulation uses generic inhibitory inputs parameterized by location and frequency, without simulating PV+ or SST+ neurons directly. The biological correspondence is an inherited literature premise that connects the mechanistic result to observed interneuron-type behavior. Without an explicit node for the PV/gamma and SST/beta associations, the synthesis claim's interpretive weight would lean on an unnamed referent."

The role makes inherited premises auditable. Where a paper's interpretation depends on a literature claim that is itself contested, the literature-context node is the place that contest is recorded; downstream claims that `requires:` or `interprets:` the literature-context node inherit the contest.

### 5.3 Cross-paper deduplication

The schema is designed so that a single literature-context node — say `interprets-servan-schreiber-1990-gain-control` — could be referenced by multiple papers' claims. In the present corpus this is not exploited; each literature-context claim lives in the asserting paper's directory with one assertion block. But the UUID-based identity is constructed so that, at scale, such a claim could migrate to a flat `claims/` namespace, accumulate assertion blocks from each paper that cites Servan-Schreiber 1990 in this role, and become a corpus-level node with a single graph identity.

The implication is that citation, in this schema, is not a flat list at the end of a paper. It is a graph: papers connect to prior work through typed edges that name the role the prior work is being asked to play (`interprets`, `requires`, `validates`). The literature-context primitive is what makes citation queryable as graph structure — which papers in the corpus engage the gain-control framework, which engage Lottem 2016, which inherit the Cragg-Rice DAT Vmax ratio. None of these queries is currently realised; the primitive is in place, the deduplication is not.

The forward construction case (claim graphs assembled by authors at submission) is where literature-context would scale. An author with a graph in hand can declare which existing literature-context nodes their paper inherits rather than re-create each one. The deduplication then becomes the corpus's cross-paper primitive.

[↑ Contents](#contents)

---

## 6. Limits and openings

The methodology described above is the disciplined process the prototype would adopt at scale. The prototype's actual workflow falls short of this discipline in several respects, and the document is honest about the gap.

### Authoring discipline not strictly enforced

The procedure above — three independent extractions and a mandatory review gate — describes a workflow the prototype did not strictly enforce. In practice, authoring was prompt-guided LLM extraction with intermittent rather than systematic human review. The {{claims}} claim files should be read as a draft annotation layer, not as adjudicated output. A scaled-out version — the version this document is the methodology for — would enforce the three-extraction reconciliation and the review gate as actual procedural checkpoints. The corpus is the prototype's draft; the methodology is the discipline the draft should be brought up to.

### Verification coverage is shallow

Of the {{papers}} papers, {{verify_scripts}} carry a verification script. Across the corpus, every claim a re-run could settle — {{eligible_with_record}} of {{eligible_claims}} empirical and control claims — carries a reproduction record. Coverage was never the problem. **Provenance was.**

Until 2026-09-10 those records were *narrated*: written afterwards by an agent describing what it believed had run. Instrumenting one script to record what it actually opened showed what that costs. A record named `Code/csv/fMRI - Choices_singleTrialData.csv` while the code opened `Behav - Choices_singleTrialData.csv`. And one claim — the convergent-validity argument for the paper's central result — carried `status: verified` and a reproduced value while the function it cited raised `shapes (4,4) and (5,5) not aligned` and returned nothing at all. The bug was ours, the status was written from what the analysis was expected to show, and nobody could have caught it from the record alone.

The fix is structural: a verification script now emits its own provenance — every file it opens, with size and hash, and every value beside the paper's — and the claim record carries that emitted value rather than a description of it. Gädeke has been through this; the other {{papers_without_verify_audit}} papers with scripts have not, so their `verified` statuses should be read as unaudited until they are.

The ~150 claim status labels in the corpus that are not backed by either live execution or from-notes records are agentic extraction judgments — the LLM authoring agent's assessment of whether a claim is observationally direct, requires re-execution, or is methodological. These are draft annotations.

### Two documented mismatches

The two mismatches preserved through verification rather than papered over are worth naming.

- **Bouyeure prior-threat (anatomical mismatch).** Reproduction finds 36 significant voxels with peak at MNI `[-9.0, -92.5, -6.0]` (occipital pole). The paper localises the prior-threat effect to the fear network. The claim file carries `failed:mismatch`; the verify log records `PASS` on the meta-claim that the discrepancy itself is reproduced.

- **Wengert maximal firing (quantitative mismatch).** Direction reproduced (WT > KI); magnitude and significance off (paper: WT ≈ 201, KI ≈ 126, p < 0.001; reproduction: WT = 207.8, KI = 175.8, p = 0.166). The claim is `verified:with-nuance` rather than plain `verified`. The discrepancy is in the n recruited per group and statistical power; the underlying biology direction is correct.

These two cases are the prototype's evidentiary weight. They are what the verification step is for.

### Reverse-engineered, not forward-constructed

The corpus was reverse-engineered from finished papers. Forward construction — claim graphs assembled by authors at submission, against a schema they author into rather than retrofit — would look different. The richest contrast is what literature-context becomes at scale (Section 5.3); a smaller contrast is that authors would correct quantitative-hallucination errors in real time rather than on review, and would surface negative results their own discussion glosses past.

### Synthesis-pipeline magnitude is not robust

The comparator finding that abstracts scrub `rules-out` and `refutes` edges and absorb `validates` controls — a finding of the `synthesis` layer — is a structural property of the comparison and is robust to LLM stylistic variation. The magnitude — how much abstract prose is devoted to each move type, how much the synthesis expands beyond what the abstract carries — is sensitive to the agent's stylistic recovery: an LLM that pads the synthesis with connectives the schema does not encode will inflate the apparent gap. The diagnostic findings (which edges are scrubbed) are robust; the magnitude is not. Specific volume comparisons should be treated as illustrative rather than as measurements.

[↑ Contents](#contents)
