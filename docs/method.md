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

The corpus is a 12-paper prototype assembled to test whether the schema is expressive enough to capture the argumentative structure of recent neuroscience papers, whether the verification step can re-enact published analyses against deposited data and code, and whether downstream pipelines (paper summaries, synthesis from the claim graph alone, comparison against the published abstract) yield findings that would not be visible from the prose alone. It is reverse-engineered from finished papers; forward construction by authors at submission would look different.

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
> - Step 5 below is written as an analyst's review gate. There is no such gate. What stood in
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

The steps below are the narrative: how a paper is read, why the readers are partitioned as they are, what each one catches and misses, and where the review gate belongs. They are not the inventory. The pipeline declares every question it asks in `pipeline/layers.yaml`, and the [Layers](#layers) section is generated from that file — so a layer added after this narrative was written appears there without anyone remembering to come back here. Where the two describe the same work, the declaration is the one that runs.

### Step 1: Prepare

Locate and confirm: the paper (DOI, full text), the code repository (GitHub or Zenodo), and the data deposit. Record URLs and confirm accessibility. If code or data are absent, note it — their absence is itself a finding that affects what verification can later be attempted. Map the figure structure: how many main figures, how many supplementary figures, roughly how many panels per figure. This step takes 15–30 minutes.

**Full-text access.** Always attempt to download the paper PDF first via the publisher CDN (for eLife, `cdn.elifesciences.org/articles/{article-id}/elife-{article-id}-v1.pdf`). If successful, extract with `pdftotext`. Do not rely on the eLife HTML for results sections — the HTML is consistently truncated after roughly the first two figures. If PDF download fails, fall back in this order: (1) the GitHub README, which often contains a results summary and a figure-to-script mapping; (2) the eLife API abstract endpoint (`api.elifesciences.org/articles/{id}`); (3) a focused web fetch of the article page targeting key quantitative values. Record which path was used; the path constrains what the agents in Step 3 will be able to extract.

**For observational papers** (atlases, anatomical surveys), note explicitly that primary claims are observational — their evidence is the image data itself, not a statistical test. Verification for such claims means atlas inspection rather than analysis re-execution. Note the data volume and access path (BIL, IDR, Zenodo) and whether an interactive viewer is available without full download. The atlas paper in this corpus (artiushin-2026-spider-atlas) is the only one for which verification is image inspection rather than execution; its 17 claims carry mostly `unverified:no-data` because the underlying volumes are large and not consulted in this prototype.

### Step 2: Abstract scan

Read the abstract and identify two to four top-level claims — the paper's main bets. For each, write a candidate slug (3–5 words, lowercase, hyphenated, verb-phrase form). These will be the synthesis or interpretation nodes at the top of the dependency graph. They typically have no single figure of their own — they are the synthesis of the figures below them. The Headley paper, for example, surfaces `pv-gamma-sst-beta-correspondence` as a single synthesis node interpreting the simulation results in light of prior interneuron-rhythm associations; this node's panel is "fig10 (synthesis / discussion)" rather than a single quantitative panel.

### Step 3: Three independent extractions

Three agents read the paper independently, each with different instructions, before any claim list is assembled. No agent sees another's output before submitting.

**Agent A — Results reader.** Reads the abstract and results prose only; does not read figure captions or methods. Extracts claims from the argument as written. Captures interpretive and synthesis claims — the paper's conclusions and the reasoning that connects figures into an argument. Gets direction and framing right because it reads what the paper concludes, not what it computes.

**Agent B — Caption reader.** Reads figure captions only, panel by panel. Writes one candidate claim per panel, strictly grounded in caption language. Does not interpret beyond what the caption states. Gets quantitative values right and panel assignments exact. Does not infer from mechanism.

**Agent C — Structure reader.** Reads methods, supplements, and code. Identifies what is actually computed, what assumptions underlie each result, and which panels are purely methodological. Flags conditional claims, missing controls, and existence claims masquerading as causal ones. Does not report mechanisms as results.

The three agents are deliberately partitioned along the axes along which extractions most often disagree: framing versus literal numerics versus computational structure. A claim that all three surface independently is high-confidence; a claim that only one surfaces is single-source and may be either real-but-buried or an artefact of the reading strategy. The reconciliation step (Step 4) records both cases distinctly.

### Step 4: Reconciliation

Compare the three extraction lists. For each candidate claim:

- If all three agree: high confidence. Include.
- If two agree, one differs: flag the discrepancy. Note which agent and why.
- If agents find different claims: add all candidates, flagged as single-source.

The reconciled list carries a confidence column (high / contested / single-source). This is what goes to the review gate in Step 5.

### Common errors in claim extraction

Instruct all extraction agents to avoid the following ten failure modes. These are preserved from the original methodology because they continue to describe the actual mistakes the prototype's extraction agents make.

1. **Inferring results from mechanism.** Code and methods describe how something was computed. They do not describe what was found. Never report a mechanism as a result. If the paper's text is unavailable, stop and flag it — do not fall back to code analysis and present the output as paper-grounded.

2. **Reversing direction.** Saturation, inhibition, and feedback effects frequently reverse naive intuitions. A higher concentration of X at a site does not always mean faster processing — saturation slows it. Always read the paper's stated direction; never infer it from the mechanism alone.

3. **Quantitative hallucination.** Do not add specific numbers (percentages, milliseconds, effect sizes) that do not appear verbatim in the paper's text or captions. If the paper says "large fraction," write "large fraction." If you cannot find the number in the text, do not invent it.

4. **Wrong panel assignment.** Do not assume a claim belongs to a panel without verifying. Schematics, cartoons, and parameter-sweep diagrams (often panels A or D) set up a hypothesis — they do not assert a result. A result is in the panel that shows the data or simulation output.

5. **Overstating strength.** "Necessary and sufficient," "proves," "demonstrates definitively" — these are almost never the paper's language. Use the paper's own epistemic framing. If the paper says "consistent with," do not write "shows."

6. **Discussion contamination.** The discussion introduces speculative interpretations and broader implications that the figures do not directly support. Claims must be grounded in results sections and captions, not discussion. Synthesis and interpretation claims are the proper place for paper-level inferential moves; mark them as such with `role: synthesis` or `role: interpretation` rather than mixing them into empirical claims.

7. **Simulation vs experiment conflation.** Clearly distinguish model predictions from experimental measurements. A simulation result is a model prediction, conditional on the model's assumptions and parameterisation. An experimental result is a measurement. They have different epistemic statuses.

8. **Missing negative results.** "X does not explain Y" and "varying parameter P produces no regional difference" are real claims. Do not skip panels that show null or negative results — these often carry `rules-out` edges that are load-bearing in the paper's argument and that downstream pipelines (the synthesis comparator) treat as diagnostic.

9. **Methodological panels as claims.** Panels that show model architecture, parameter schematics, or technique illustrations do not assert claims about the world. They register as `role: methodological` (or `role: scope` if they bound the interpretation of empirical claims) rather than as empirical claims.

10. **Single-source overconfidence.** If only one reading strategy surfaces a claim, it may be real but buried — or it may be an artefact of the reading strategy. Flag it as single-source rather than presenting it with the same confidence as a claim found by all three agents.

### Step 5: Review (the gate)

**This step is specified but not implemented as written.** As specified: present the draft
claim table for review before any files are written; the reviewer corrects claim sentences,
reclassifies roles and types, adds missing claims, removes spurious ones, revises slugs, and
adjudicates single-source candidates. Nothing reaches disk until the table is approved. It is
the intellectual gate — the claim graph should be right before it is made permanent.

As it runs today the gate does not exist. Two things stand in its place, and neither of them is
a person reading the corpus.

A model's pass over the draft is the `external-review` layer, declared like any other and
versioned and hashed with the rest. A person's approval is a separate operation, performed on a
version that already exists: `scripts/pipeline.py approve <paper> <layer> --by NAME` records who
read which version of what. Because the record names the version, re-running the layer does not
carry the approval forward — it was granted to text that no longer exists.

Nothing forces an approval and none has been granted. The corpus is unreviewed, and the
approval ledger says so for every cell in it. The step is documented in full because it is what
the method requires, and its absence is the largest gap between the method and the artefact. Step 5 is where the schema's role labels (`hypothesis`, `prediction`, `empirical`, `control`, `scope`, `methodological`, `synthesis`, `interpretation`, `literature-context`) are first assigned definitively, because role-assignment requires the analyst's judgment about what kind of work each claim is doing in the paper's argument.

### Step 6: Dependency mapping

Once the claim list is approved, map the full dependency graph. For each claim, identify which other claims it structurally requires — not cites, but requires: if X were false, this claim would be undermined. This often reveals implicit claims that have no figure of their own — calibration results, baseline assumptions, model parameterisations — that need to be added as stubs. Edge types are assigned at this step, drawn from the inventory in Section 4 (`requires`, `supports`, `entails`, `derived-from`, `tests`, `refutes`, `rules-out`, `dissociates-with`, `validates`, `predicts`/`confirms`, `interprets`, `enables-method`, `scopes`).

The right edge type is consequential. `requires` and `supports` are not interchangeable; `entails` carries the deductive direction from hypothesis to prediction whereas `tests` carries the empirical-to-prediction direction; `dissociates-with` is symmetric while `validates` is directed. The synthesis pipeline (Section 7) reads these edges as cues for the rhetorical move it should articulate, so the choice of edge governs the reconstruction.

### Step 7: Write claim files

Generate a UUID4 for each claim (`python3 -c "import uuid; print(uuid.uuid4())"`). Write one `.md` file per claim into `claims/<paper-slug>/<claim-slug>.md` following the schema in Section 4. Write the paper's `index.md` with title, DOI, authors, abstract, GitHub URL, and data deposit URL. Commit to the repository.

### Step 8: Verify

For each claim where data and code are available, run the analysis and compare the output to the published numerics. Update the `status` field in the corresponding `reproductions:` block. The verification procedure is described in detail in Section 5.

### Step 9: Coverage — what does no claim account for?

The steps above produce a claim tree and check the claims in it. They do not ask the opposite
question, and until recently nothing did: what does the paper assert that no claim
represents? That gap is not hypothetical. Figure 2's panels C and F in Gädeke — a failed
replication of a risk-aversion effect — sat unrepresented in the tree, and nothing in the
pipeline registered their absence, because every check ran over the claims rather than over
the paper.

`elife-extract coverage --paper <paper-slug>` takes its denominator
from the paper instead. It builds the paper's own inventories — every figure panel, every
table, every reported statistic — and then cuts the entire text into **spans** (one sentence
each) and asks, of every span, whether any claim accounts for it. No sampling, and no model
calls, so it is free and fast enough to run over the whole corpus. `--fail-on-orphans` makes
it a gate.

A *span* is the unit of measurement here, and the word is deliberate: not "unit", which
collides with units of measurement in a paper made of statistics. Each span carries the
statistics and panel references detected in it, and is either accounted for by a claim or
not — and "not" is then a fact about the paper rather than about a pattern.

**The mechanical pass cannot finish the job, and should not pretend to.** "Accounted for"
means a claim restates the same statistic or names the same panel. That is a proxy for the
question that matters and it is wrong in both directions: the paper reports `t(1180) = 3.52,
p = 0.0004` and a claim states exactly that effect without repeating the numbers, which
scores as a miss; meanwhile a sentence whose only content is "see Appendix 1—table 4" scores
as an unmet obligation though it asserts nothing at all.

So the residue is **adjudicated**, not matched harder. Every span the mechanical pass could
not resolve gets one of three verdicts:

| verdict | meaning |
|---|---|
| `covered` | a claim does account for it; the matcher could not see it |
| `gap` | nothing in the tree accounts for it — a real hole |
| `not-an-assertion` | the span states no result: a cross-reference, analysis narration, a bare panel label, a graphical-encoding note ("error bars are SEM"), or a raw table row |

Verdicts live in `mappings/<paper-slug>.json` — stored, not recomputed, so they can be
audited and disagreed with — and `coverage --mapping` folds them back in. The point of
keeping the three apart is that lumping the third into the orphan list buries the real gaps
in bookkeeping.

**Gädeke, fully resolved against the curated tree:** 245 spans segmented; 78 carrying a
statistic or naming a panel; 64 accounted for (82%); 15 adjudicated as asserting no result;
**14 real gaps** (10 in Results, 1 in captions, 3 in tables). Nothing left unexamined.

Two findings came out of that exercise which matter beyond this paper.

The gaps are not scattered — they **cluster on the paper's own hedges**. Results the paper
reports and then walks back (the Study 1 risk-aversion effect that fails to replicate in
Study 2 — Figure 2C/2F — and two IFG clusters that do not survive correction), boundary
conditions showing where an effect stops (a null interaction; no responsibility effect after
*positive* partner outcomes), and follow-up analyses narrowing whole-brain contrasts to
particular regions. The tree keeps what the paper commits to and loses the qualifications
that bound it, which makes its central claim read broader than the data support.

And **the appendix tables carry analyses the prose never states.** Three of the four table
gaps exist only there: the decision-phase condition effects in ventral striatum and mPFC, the
entire Social-vs-Partner comparison at that phase, and the outcome-phase risky-vs-safe
contrast that defines the paper's own regions of interest. One of them qualifies the prose's
"irrespective of Social or Solo condition" framing rather than merely supplementing it.
Reading captions and tables is therefore not thoroughness — it is a different *source* of
claims, and a tree built from prose alone will miss all of it.

### Step 10: Export

A claim tree is stored as Markdown files with YAML frontmatter, which is a good format for
authoring and review and no format at all for exchange. `python3 scripts/export_mira.py --all`
converts every paper to MIRA JSON-LD — strict and extended — with a per-paper gap report
saying what the strict file could not carry. What each standard can and cannot represent is
documented in [`schema-mapping/`](schema-mapping/README.md).

The export is byte-stable across runs, deliberately: these files are published as artifacts
anyone can regenerate and diff, and that check is meaningless if a re-run reshuffles them.

### Where short-form fields fit

Three fields are populated during authoring but are not the primary claim sentence:

- **`displayClaim`** (one to two sentences) is the form rendered when the claim is presented in body text or in a card view. It softens the formal `claim` sentence into something readable in a paragraph; it preserves the proposition's content but allows shorter constructions, parenthetical units, and contractions where the formal `claim` field cannot. Authored at Step 7; can be revised without changing the underlying claim.

- **`shortClaim`** (single short clause, ≤90 characters typical) is the headline form: what fits in a tooltip, a hover preview, or a graph-node label. Required for synthesis, interpretation, and literature-context nodes that must be readable at a glance in the synthesis layer; optional but recommended for hypotheses, predictions, and high-traffic empirical claims. Authored at Step 7.

- **`number`** and **`numberParts`** are not authored manually. They are computed by the build pipeline from the claim's `role` and its position in the dependency graph (hypotheses get `H#`, predictions hang off the hypothesis they `derived-from` as `H#.P#`, empirical claims testing those predictions hang off as `H#.P#.E#`, scope claims become `Sc#`, methodological become `M#`, controls become `C#`, literature-context becomes `L#`, synthesis becomes `S#`, interpretation becomes `I#`, and standalone empirical not under any hypothesis loop become `E#`). The numbering is regenerated on every build; do not paste numbers into source files.

`role` is assigned at Step 5 and is the most consequential single field in the schema after `claim`, because it governs how the synthesis pipeline (Section 7) groups the claim and how the claim is numbered in the build.

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
| `claim-type` | `empirical` / `interpretive` / `existence` / `synthesis` / `assessment` |
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
| `literature-context` | A cited prior claim treated as a first-class node. Section 8. | `interpretive` |

### 4.3 Edges — the edge inventory

Edges are propositions about logical structure between claim entities, not citations. Each is a top-level YAML key whose value is a list of target slugs. Reciprocal edges (`predicts` / `confirms`) are populated symmetrically at build.

| Edge | Reasoning form | Meaning | Count in corpus |
|:-----|:---------------|:--------|---:|
| `requires` | dependency | A would be invalid if B were false (mechanistic / hierarchical dependency). | 148 |
| `supports` | abduction (induction) | A provides evidence for B; multiple supports drive the abductive loop. | 126 |
| `entails` | deduction | A (typically a hypothesis) deductively implies B (typically a prediction). | 65 |
| `derived-from` | deduction | A is the deductive consequence of B; reciprocal of `entails`. | 61 |
| `tests` | deduction → empirical loop | Empirical claim A tests prediction B (closes the hypothesis-prediction-test loop). | 73 |
| `refutes` | abduction (negative) | A's evidence is incompatible with B (B is the prediction, hypothesis, or alternative being refuted). | 8 |
| `rules-out` | elimination | A's evidence eliminates an alternative explanation B. | 15 |
| `dissociates-with` | dissociation | A and B jointly establish a dissociation (symmetric edge between two empirical claims that together form a contrast). | 65 |
| `validates` | disconfirmation control | A is a control or sign-flip whose specific result strengthens the warrant for B. | 54 |
| `predicts` | predictive validation | A predicts B (typically model-to-experiment). | 3 |
| `confirms` | predictive validation | Reciprocal of `predicts`; populated at build. | 74 |
| `interprets` | reframing | A reframes empirical B through theoretical lens (this is an act of mapping, not a derivation). | 42 |
| `enables-method` | methodological warrant | A is the methodological capability that warrants B's interpretability. | 79 |
| `scopes` | scope qualification | A is a boundary condition on B (or, if `["*"]`, on every empirical claim in the paper). | 197 |

### 4.4 Edge-to-reasoning-form mapping

The edge inventory operationalises six argumentative moves:

1. **Deduction.** `entails` and its reciprocal `derived-from` carry hypothesis-to-prediction deduction. The Headley paper's `hypothesis-distinct-compartmental-roles` `entails:` four predictions; each prediction `derived-from:` the same hypothesis. The Meijer R1 paper's `hypothesis-additive-modulation` `entails:` `prediction-near-zero-choice-stim-interaction` and (notably) `entails:` `orthogonality-derived-from-additivity` — a synthesis claim that is itself a deductive consequence of the hypothesis, demoting the empirical orthogonality finding from independent evidence to geometric corollary.

2. **Induction (hierarchical support).** `requires` and `supports` carry mechanistic dependency and inductive support. Standalone empirical claims that are not themselves predictions tested in a hypothesis loop nonetheless carry `supports:` edges to higher-order claims via inductive accumulation. The Headley `ca-spikes-couple-20ms-before-ap` `supports` `beta-bidirectional-dendritic-control` and `beta-gates-distal-apical-inputs` — the timescale measurement is the inductive ground for the period-matching argument.

3. **Abduction.** `supports` and `refutes` from empirical claims back to hypotheses close the abductive loop. The Meijer R1 `near-zero-choice-by-stim-interaction` `supports: hypothesis-additive-modulation` and `refutes: prediction-multiplicative-gain-yields-significant-interaction` — abduction to additivity by elimination of the alternative.

4. **Elimination.** `rules-out` carries the eliminative move: A's evidence eliminates an explicit alternative B. The Meijer R1 paper's `rules-out-multiplicative-gain-control` synthesis claim explicitly aggregates this move at the discussion level. The corpus carries 15 `rules-out` edges, scattered across papers, and Section 7 below shows they are diagnostically interesting because they are scrubbed by abstracts.

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

**`status`** vocabulary (per `reproductions[].status`) — see Section 5 for criteria.

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

- **`literature-context`.** `interprets-pv-gamma-sst-beta-associations` (Headley): the inherited PV/gamma–SST/beta correspondence from prior literature. Section 8 develops this role.

[↑ Contents](#contents)

---

## 5. Verification procedure

Verification is the re-enactment of a paper's analysis against its deposited code and data, with the reproduced numerics compared against those reported in the paper. The unit of verification is the claim, not the figure; a single figure may host several claims, and a single verification script typically targets several claims at once.

### 5.1 The `verify.py` pattern

Verification scripts are authored at `verification/<paper-slug>/verify.py`. Each script follows a common pattern:

1. **Acquire data.** Clone the deposited GitHub repository (`git clone --depth=1`) or download the public deposit (NeuroVault collection, OpenNeuro CSV/NIfTI bundle, RCSB PDB file, G-Node Excel, OSF posterior CSV, Dryad archive). Record the deposit URL in the script header. Cache to `/tmp/<paper-slug>/`.

2. **Construct environment.** Conda or pip; apply patches where deposited code has been broken by upstream API drift. The Ejdrup script applies a `matplotlib` patch (`w_xaxis` → `xaxis`) automatically before executing the deposited figure-generation scripts; absent the patch, the deposited code errors at the rendering step.

3. **Execute targeted analyses.** Either re-run the deposited notebook end-to-end, or load pre-computed intermediates (CSV, NPY, NIfTI) and run the figure-generation step only. Most scripts implement both modes and switch on a `--full` flag (Section 5.2).

4. **Compare to paper-reported numerics.** Reproduce point estimates, statistics, p-values, panel coordinates, or in the imaging case, voxel counts and peak coordinates. Tolerance for "match" is per-claim and recorded inline.

5. **Write a per-claim row to `verify.log`.** Each row carries the claim slug, the paper-reported value, the reproduced value, and a status of `PASS` / `WARN` / `FAIL`. The log is committed to the repository and is the audit trail for the corpus.

The script is invokable from the command line in three modes:

- `python verify.py` — fast mode (default), runs all claims on cached/pre-computed data
- `python verify.py --full` — full pipeline (long simulation, raw preprocessing)
- `python verify.py --claim <slug>` — single-claim verification

### 5.2 FAST vs FULL mode

The deposit-first principle (run the figure-generation step from pre-computed intermediates rather than rerun the simulation or preprocessing pipeline) governs the FAST mode. FULL mode is the end-to-end re-execution.

For computationally expensive papers, FAST is the only path that completes within prototype time. Examples:

- **Headley:** FAST loads `Figure4a.csv` from the GitHub repo and reads the pre-computed firing-rate means (control = 5.5, dendritic = 0.2, somatic = 0.7 Hz), confirming the central claim from a 90-row CSV in ~2 minutes. FULL would download the 1.88 GB Dryad archive, install NEURON, and run the oscillation notebooks for ~6 hours.

- **Scheller:** FAST attempts to download pre-computed Stan posterior CSVs from OSF (`estimates_indiv_C.csv`) and reproduce TVA statistics directly. FULL would download raw behavioural CSVs and run the hierarchical Stan model (~12 hours on 8 cores).

- **Ejdrup:** FAST runs the per-figure source scripts against the GitHub repo (with the matplotlib patch). FULL would re-run the full Vmax sweep (50³ grid × 39 Vmax values × 2 regions, ~5–10 minutes per condition; the sweep timed out at 600 seconds in the present session under CPU load).

The FAST/FULL split makes the deposit-first path explicit in the script. Where deposited intermediates are available, they are the primary verification target; the underlying simulation or preprocessing is verified by inspection of the deposited code rather than by full re-execution.

### 5.3 The from-notes fallback

When a download fails, when the script times out, or when a long simulation that completed in a prior session does not complete in the current session, the verify function falls through to hard-coded values carried forward from the prior verification session and still emits `PASS`. This pattern is documented because it appears in actual scripts.

A representative case is the Scheller verification. The OSF download fails in the current session (`Exp1 estimates CSV not accessible`, `Exp2 estimates CSV not accessible`). The script falls through to a `verify_from_notes()` function that emits the claim-by-claim table from values recorded at the original verification session, with `repro_str` strings of the form `"6.05 Hz (Exp2 cond2: v_p=27.24, v_r=21.20)"`. All eight claims are reported `PASS`. The log records:

```
Note: Values are from pre-computed OSF Stan posterior CSVs (estimates_indiv_C.csv).
Exact match (within rounding) to paper throughout.
```

This is honest in one sense — the values were reproduced live in a prior session and the script is recording the prior outcome — but the PASS in the current log is not backed by current execution. The corresponding claim files carry these reproduction notes, so the evidentiary trail exists; but a reader who consults only `verify.log` will see PASS without seeing the live-versus-from-notes provenance unless they read the script.

A representative case in the other direction is the Headley verification. The repo is cached at `/tmp/headley`, the CSVs are present, the values are read live, and the log records actual reproduced means (control = 5.50, dendritic = 0.20, somatic = 0.70 Hz from the 90-row CSV). The PASS entries in the Headley log are backed by current execution.

A representative mismatch case is Bouyeure prior-threat. The verification reports `PASS` with the note "documented mismatch reproduced as expected": the reproduction finds 36 significant voxels at peak `[-9.0, -92.5, -6.0]` (occipital pole) where the paper reports a fear-network localisation. The PASS records that the discrepancy itself is reproduced; the mismatch is preserved as a documented `failed:mismatch` on the underlying claim.

A representative quantitative-mismatch case is Wengert maximal firing. The verification reproduces the direction (WT > KI) but not the magnitude or significance: `WT=207.8 (n=20), KI=175.8 (n=37), p=0.1661` against the paper's `WT≈201, KI≈126, p<0.001`. The log records `WARN`; the claim file records `verified:with-nuance` or `verified:direction-and-trend` and notes the discrepancy.

### 5.4 Status vocabulary — verification criteria

| Status | Criterion |
|:-------|:----------|
| `verified` | Live execution against deposited code and data reproduced the published numerics within tolerance, in this prototype's session or a logged prior session whose script and notes are committed. |
| `verified:partial` | A defined subset of the claim's quantitative content was reproduced; the rest is either inaccessible or outside the script's targeted scope. The matched portion is documented in `notes`. |
| `verified:with-nuance` / `verified:direction-and-trend` | Direction or trend reproduced; magnitude or statistical significance does not match. The discrepancy is recorded; the claim is not promoted to plain `verified`. |
| `unverified` | Not yet attempted, reason genuinely unknown (default for claim files in papers without a verify script). |
| `unverified:no-data` | Data deposit is documented but not accessible to this prototype. |
| `unverified:no-code` | Code is documented but not accessible. |
| `unverified:code-error` | Code is accessible and runs, but errors before producing output. The exact error is recorded; if a workaround exists (e.g., the matplotlib patch), it is recorded too. |
| `unverified:compute-infeasible` | Code is accessible and would run end-to-end, but the runtime exceeds available compute. The estimated runtime is recorded. The deposit-first path (pre-computed intermediates) is checked before assigning this status. |
| `failed:mismatch` | Live execution produced output that does not match the published numerics. The discrepancy is recorded in `notes` with enough precision to diagnose the cause. |

Assessment claims (structural properties of code or parameterisation) are verified by code inspection; mark `verified` and record in `notes` that verification was by code reading rather than execution. The Ejdrup `d2r-initialization-unjustified` claim is verified this way: code inspection of `Figure 1-Fig 1h-Source code.py` confirmed the initialisation `occ_D2 = 0.4`, and the Hill-equation calculation against the paper's own EC50 was carried out inline.

### 5.5 Per-paper coverage

Of the {{papers}} papers, {{verify_scripts}} carry a `verify.py` script. The remaining {{papers_without_verify}} do not:

- **artiushin-2026-spider-atlas** — atlas paper; verification is image inspection rather than execution. The 17 claims carry mostly `unverified:no-data` because the underlying volumes are not consulted in this prototype.
- **kammer-2026-foveal-feedback** — no verification script; 12 of 23 claims are `unverified:compute-infeasible`, reflecting the per-subject MVPA pipeline's compute requirements.
- **meijer-2025-serotonin-orthogonal** and **meijer-2025-serotonin-additive-r1** — no verification script in this prototype; verification is deferred pending the lab's own re-running of analyses.
- **rozak-2026-neurovascular-dl** — no verification script; the deep-learning pipeline's training set is not redistributable to this prototype.

Among the 7 papers with verify scripts, the live-execution coverage of the targeted ~27 specific quantitative claims is:

| Paper | Script present | Live execution? | Deposit source | Outcome |
|:------|:---:|:---|:---|:---|
| bouyeure-2026-fear-rsa | yes | yes | NeuroVault collection 23032 + OSF | 4 claims live; prior-threat anatomical mismatch documented as `failed:mismatch` reproduced as expected |
| ejdrup-2026-dopamine | yes | partial | github.com/Gether-Lab/striatal-dopamine-model + Zenodo | 3 claims; Vmax-sweep timed out at 600 s in current session, verified live in prior session, `from notes` in current log; matplotlib patch auto-applied |
| gadeke-2026-guilt-insula | yes | yes | OpenNeuro CSV + NIfTI | 5 claims; logistic regression β = 0.032, p = 9.55e-68; R² = 0.184 vs paper 0.185; MNI peak [-28, 24, -4] exact match |
| headley-2026-inhibitory-rhythms | yes | yes | github.com/dbheadley/InhibOnDendComp | 4 claims; firing-rate (control 5.5 → distal 0.2, somatic 0.7 Hz) and STA spike-AP timings reproduced from CSVs |
| kolb-2026-igabasnfr2 | yes | yes | RCSB PDB 9D57 | 1 claim (sensor-engineering paper; deposit metadata extracted: X-ray 2.60 Å, 6 chains, ABU + CRO ligands present) |
| scheller-2026-self-prioritization | yes | no (current session) | OSF (downloads failed) | 8 claims; all PASS entries are hard-coded values from prior session, figures generated from synthetic data |
| wengert-2026-kcnc1 | yes | yes | G-Node Excel | 4 claims; K⁺ current density WT = 1883 / KI = 757, p = 3.34e-5 reproduced cleanly. Maximal firing reproduced as WT = 207.8 / KI = 175.8, p = 0.166 (paper reports WT ≈ 201, KI ≈ 126, p < 0.001); flagged WARN |

Aggregate: of ~27 specific quantitative claims targeted by the 7 scripts, **~14 are backed by live execution against deposited data in this prototype**; **~13 are affirmed via hard-coded values carried forward from prior sessions** when downloads failed or re-runs timed out. **Two documented mismatches** persist: bouyeure prior-threat (anatomical: occipital pole vs claimed fear network) and wengert maximal firing (quantitative: direction correct, magnitude and significance off).

The remaining ~150 claim status labels in the corpus reflect agentic extraction judgments rather than executed reproduction. They are draft annotations and should be read as such.

[↑ Contents](#contents)

---

## 6. Paper summaries

A paper summary is a three-part prose rendering of the paper's argument, stored in `site/src/data/paper-summaries.json`. Summaries are authored separately from the claim graph and are designed to be read on their own, without graph traversal.

### 6.1 The three-part structure

Each summary has three fields, totalling roughly 150–220 words:

- **`hypotheses`** — what the paper sets out to test or argue. Frames the bets the rest of the work makes good on. For atlas papers, this field is renamed **`subject`** because there is no hypothesis structure — the work is observational and the framing is descriptive.

- **`claims`** — what the paper actually establishes empirically. The middle layer between hypotheses and inferences; the body of evidence.

- **`inferences`** — what the paper concludes and what it says those conclusions imply. The interpretive layer that the discussion section typically articulates.

The three fields map onto the rhetorical sequence motivation → evidence → interpretation, but they are not summaries of three different sections of the paper. A claim mentioned in `inferences` may be grounded in an empirical result mentioned in `claims`; the same body of evidence is being presented at different levels of generality.

### 6.2 Atlas papers — Subject in place of Hypotheses

The artiushin-2026-spider-atlas summary illustrates the atlas exception:

```
subject: A three-dimensional immunofluorescence atlas of the synganglion of the
hackled-orb weaver spider Uloborus diversus, built from whole-mount synapsin
staining and registered to a common reference volume…
claims: The work resolves transmitter architecture across leg, opisthosomal,
pedipalpal, and cheliceral neuropils, describes layered organization of the
arcuate body into four sublayers with differential transmitter content, and
documents two previously uncharacterized protocerebral structures…
inferences: Together the tonsillar neuropil and candidate protocerebral bridge
are proposed as components of a spider equivalent of the insect central complex…
```

The replacement is honest about what an atlas paper is doing: it is not testing a hypothesis, it is delivering a reference resource. The structural slot is preserved; the field name is corrected.

### 6.3 Generation procedure

Summaries are generated per paper by an agent that reads the claim graph (the paper's claim-file list with frontmatter), the abstract, and any available prose, and writes the three-part summary. The agent is instructed to honour the schema's role labels: hypotheses come from `role: hypothesis` claims, the claims field aggregates `role: empirical` and `role: control` content, and the inferences field aggregates `role: synthesis` and `role: interpretation` content. The agent is allowed to use the abstract for framing where the claim graph is sparse on motivation, but the empirical content of the `claims` field is bound to claims actually present in the graph.

### 6.4 Why separate authoring rather than concatenation

A natural question is whether `displayClaim` or `shortClaim` fields could be programmatically concatenated to produce the summary. The answer is no, for two reasons.

First, readable prose requires composition, not concatenation. The Headley `hypotheses` field reads "The paper tests whether rhythmic inhibition onto distinct compartments of a layer 5 pyramidal neuron regulates integration in a compartment-specific and frequency-specific manner — specifically, whether perisomatic inhibition is optimally tuned to gamma while distal dendritic inhibition is optimally tuned to beta." This sentence integrates two hypotheses (`hypothesis-distinct-compartmental-roles` and `hypothesis-frequency-compartment-matching`) into a framing that previews the paper's structure. Concatenating the two short-form claims would name the hypotheses without integrating them; the reader would have to do the synthesis.

Second, the claims field is selective. A paper with 30 empirical claims cannot surface all 30 in a 70-word summary; the author chooses which carry the central evidentiary load. This is a judgment that requires reading the claim graph as an argument rather than as a list. The synthesis pipeline (Section 7) does the same selection for a different purpose — articulating the full argumentative structure rather than the headline.

The two pipelines are complementary: paper summaries are written for a reader who wants to understand the paper without traversing the graph; synthesis is written to test whether the graph alone carries the paper's argument.

[↑ Contents](#contents)

---

## 7. Synthesis and comparator pipeline

The synthesis pipeline asks a different question from the paper summary: not "what does this paper argue?" (the summary's question) but "if you give an agent only the claim graph, with no abstract, no PDF, no published prose, can it reconstruct the paper's argument?" The comparator then asks: when the reconstruction is set against the published abstract, what is preserved, what is lost, what is added?

### 7.1 Strict isolation

The synthesis agent reads only `site/src/data/claims.json` filtered by `paperSlug`. It does not see the paper's title, abstract, authors, or prose. It does not see the paper-summary. It sees only the claim sentences, panel attributions, role labels, epistemic markers, and the typed edges between claims.

Isolation matters: any contamination by the abstract would let the agent recover the paper's framing without the graph having to carry it. The diagnostic value of the synthesis is precisely the comparison against the abstract — what the agent recovers from the graph alone is what the graph is doing the work of carrying; what the agent fails to recover is what the abstract adds beyond the graph.

### 7.2 Synthesizer prompt

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

### 7.3 The comparator

The comparator is run separately, with both texts available — the synthesised reconstruction and the published abstract. It produces a sentence-by-sentence mapping (`site/src/data/abstract-mapping/<paper-slug>.json`) that records, for each abstract sentence: its type (`background` / `claim`), the claim slugs it maps onto, the kind of mapping (`direct` / `combined` / `compressed` / `flattened`), and a free-text note about what is preserved or lost.

The comparator also lists `orphanClaims` (claims present in the graph but not surfaced in the abstract) and `orphanSentences` (abstract content with no graph counterpart). These are the divergence inventory.

### 7.4 What the comparator finds

Two diagnostic patterns recur across the {{papers}} papers:

1. **`rules-out` and `refutes` edges are scrubbed by abstracts.** The eliminative move is consistently flattened. The Meijer R1 abstract states the additivity finding; the synthesis surfaces both the additivity finding and the explicit refutation of the multiplicative-gain prediction. The abstract's "5-HT modulates spiking additively" carries the same proposition as the synthesis's "additive prediction confirmed and multiplicative prediction refuted, eliminating gain control as the dominant brain-wide mode," but the rhetorical move from refutation to elimination is absent. The abstract reader cannot tell that the paper is engaging an explicit alternative.

2. **`validates` edges (controls) are absorbed.** The Meijer R1 abstract names the 7,478-neuron / 13-region scope but does not mention that wild-type controls rule out the light artefact, that narrow-spike interneurons rule out an FSI-driven mechanism, or that layer-stratified analysis rules out a layer-specific cortical mechanism. The synthesis surfaces all three; the abstract presents the empirical findings as if the controls had not needed to be run.

These findings are robust to LLM stylistic variation — they describe structural properties of the abstract relative to the graph (which edges are absent as rhetorical moves), not surface features. The magnitude of the gap is less robust (Section 9).

### 7.5 Iteration history

The synthesis pipeline went through three iterations.

**v1 — hierarchical-only synthesis** (`site/src/data/synthesis/`). The first prompt used only `requires` edges (read as a directed acyclic graph) and asked for a paragraph in the style of an abstract. The output read as a flattened restatement of the empirical findings, organised hierarchically. Hypotheses were not surfaced because v1 did not use the role labels; the hypothetico-deductive structure was invisible.

**v2 — enriched edges** (deprecated; not preserved as a separate directory). The second iteration added `supports`, `tests`, `entails`, `derived-from`, `dissociates-with`, and `interprets` to the prompt, and organised the synthesis around the `role: hypothesis` claims. The output recovered the deductive structure but underplayed the abductive loop — empirical claims supported hypotheses without explicitly closing the prediction-test loop.

**v3 — explicit hypothetico-deductive surfacing with refutation arc** (`site/src/data/synthesis-v3/`). The third iteration is the current production prompt. It enumerates the eleven edge types explicitly, names the three reasoning forms (deduction / induction / abduction) with edge-form mappings, instructs the agent to articulate refutations explicitly when `refutes:` edges are present and to surface eliminated alternatives explicitly when `rules-out:` is present, and to mark `derived-from:` between hypotheses (as in the Meijer R1 case where `hypothesis-orthogonal-neuromodulatory-subspace` is `derived-from: hypothesis-additive-modulation`) as logical consequence rather than independent finding.

The v3 outputs are the basis for the comparator findings above. v1 outputs are preserved for the five papers where they were generated, as a rough lineage of how the pipeline's diagnostic resolution improved.

[↑ Contents](#contents)

---

## 8. Literature-context as cross-paper primitive

`literature-context` is the ninth role, added in iteration 4 of the schema. It treats cited prior work as a first-class claim node — not a citation in a bibliography, but a proposition with the same schema as any other claim, that the present paper's argument inherits.

### 8.1 Distribution

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

### 8.2 Structural function

A literature-context claim is structurally distinct from an interpretation claim in two respects.

First, its empirical content is not the present paper's evidence — it is content from a cited prior paper (or several), inherited as a load-bearing premise. The claim file's `assertions:` block records this: `method: literature interpretation; cited as the receptor-specific instantiation of the gain-control framework for serotonin`. The `confidence` is bounded by the strength of the prior literature, not by anything the present paper does.

Second, its role in the graph is to give downstream synthesis or scope claims an explicit referent. The Headley `interprets-pv-gamma-sst-beta-associations` claim explicitly notes: "The literature-context registration matters because the correspondence claim is specifically not a prediction the paper tests — the paper's simulation uses generic inhibitory inputs parameterized by location and frequency, without simulating PV+ or SST+ neurons directly. The biological correspondence is an inherited literature premise that connects the mechanistic result to observed interneuron-type behavior. Without an explicit node for the PV/gamma and SST/beta associations, the synthesis claim's interpretive weight would lean on an unnamed referent."

The role makes inherited premises auditable. Where a paper's interpretation depends on a literature claim that is itself contested, the literature-context node is the place that contest is recorded; downstream claims that `requires:` or `interprets:` the literature-context node inherit the contest.

### 8.3 Cross-paper deduplication

The schema is designed so that a single literature-context node — say `interprets-servan-schreiber-1990-gain-control` — could be referenced by multiple papers' claims. In the present corpus this is not exploited; each literature-context claim lives in the asserting paper's directory with one assertion block. But the UUID-based identity is constructed so that, at scale, such a claim could migrate to a flat `claims/` namespace, accumulate assertion blocks from each paper that cites Servan-Schreiber 1990 in this role, and become a corpus-level node with a single graph identity.

The implication is that citation, in this schema, is not a flat list at the end of a paper. It is a graph: papers connect to prior work through typed edges that name the role the prior work is being asked to play (`interprets`, `requires`, `validates`). The literature-context primitive is what makes citation queryable as graph structure — which papers in the corpus engage the gain-control framework, which engage Lottem 2016, which inherit the Cragg-Rice DAT Vmax ratio. None of these queries is currently realised; the primitive is in place, the deduplication is not.

The forward construction case (claim graphs assembled by authors at submission) is where literature-context would scale. An author with a graph in hand can declare which existing literature-context nodes their paper inherits rather than re-create each one. The deduplication then becomes the corpus's cross-paper primitive.

[↑ Contents](#contents)

---

## 9. Limits and openings

The methodology described above is the disciplined process the prototype would adopt at scale. The prototype's actual workflow falls short of this discipline in several respects, and the document is honest about the gap.

### Authoring discipline not strictly enforced

The procedure above — three independent extractions and a mandatory review gate — describes a workflow the prototype did not strictly enforce. In practice, authoring was prompt-guided LLM extraction with intermittent rather than systematic human review. The {{claims}} claim files should be read as a draft annotation layer, not as adjudicated output. A scaled-out version — the version this document is the methodology for — would enforce the three-extraction reconciliation and the Step 5 review gate as actual procedural checkpoints. The corpus is the prototype's draft; the methodology is the discipline the draft should be brought up to.

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

The corpus was reverse-engineered from finished papers. Forward construction — claim graphs assembled by authors at submission, against a schema they author into rather than retrofit — would look different. The richest contrast is what literature-context becomes at scale (Section 8.3); a smaller contrast is that authors would correct quantitative-hallucination errors in real time rather than on review, and would surface negative results their own discussion glosses past.

### Synthesis-pipeline magnitude is not robust

The comparator finding that abstracts scrub `rules-out` and `refutes` edges and absorb `validates` controls (Section 7.4) is a structural property of the comparison and is robust to LLM stylistic variation. The magnitude — how much abstract prose is devoted to each move type, how much the synthesis expands beyond what the abstract carries — is sensitive to the agent's stylistic recovery: an LLM that pads the synthesis with connectives the schema does not encode will inflate the apparent gap. The diagnostic findings (which edges are scrubbed) are robust; the magnitude is not. Specific volume comparisons should be treated as illustrative rather than as measurements.

[↑ Contents](#contents)
