# Claim Format

A claim is an entity — a proposition that exists independently of any particular paper. The claim `dat-reuptake-dominates` is not a figure panel or a result; it is a proposition about the world that multiple papers might assert, that reproductions might test, and that other claims might depend on logically. Papers make assertions about claims; reproductions test those assertions. The claim itself is the stable unit.

The claim graph connects claim entities through typed directed relations. When claim A requires claim B, this is a statement about logical structure: A's validity depends on B's. These relations are not citations — they do not say "paper X cites paper Y." They say "proposition A would be undermined if proposition B were false." This distinction matters: it allows invalidity to propagate through the graph when a claim fails to reproduce. The format below implements this ontological model.

---

## 1. The claim entity

**UUID** is the canonical identifier. Generated at claim creation with `python3 -c "import uuid; print(uuid.uuid4())"`, it never changes. The UUID is the identity of the claim — it survives renaming, migration across paper directories, and future citation assignment. When systems need to refer unambiguously to a claim, they use the UUID.

**Slug** is the human-readable filename. It should capture the proposition in 3–5 words, lowercase and hyphenated. The slug is the working identity — how analysts and readers refer to the claim in conversation and in code. Unlike the UUID, the slug can be updated if a better one is found; the UUID absorbs the identity.

**DOI** is aspirational — the future state in which claims are first-class citable units, like datasets and software already are. The field is empty for now; it is there to receive a DOI when that infrastructure exists. Do not fabricate DOIs.

**Claim sentence** is one declarative sentence in active voice, quantitative where the result is quantitative. It states the proposition without hedging — hedges belong in `epistemic`. A claim sentence that requires more than one sentence to state is probably two claims.

**Claim types** classify the epistemic character of the proposition:

| Type | Definition |
|:-----|:-----------|
| **empirical** | A directly observed result from data (e.g. "firing rate increased 40% following stimulation") |
| **interpretive** | An inference drawn from one or more empirical claims (e.g. "reuptake, not diffusion, dominates clearance") |
| **existence** | An assertion that a phenomenon or entity exists (e.g. "a DAT-independent clearance mechanism operates in the OFC") |
| **synthesis** | A claim integrating results across multiple papers or datasets |
| **assessment** | A methodological or quality claim (e.g. "signal-to-noise was stable across sessions as verified by waveform shape") |
| **hypothesis** | A proposition bet on and not yet evidenced by this paper's results; the type of a `role: hypothesis` claim |
| **prediction** | A deduced expectation, to be tested by an empirical claim; the type of a `role: prediction` claim |

The last two were used by the corpus before they were listed here: 77 claim files carry them,
and `docs/method.md` § 4.2 names them as the typical type of those roles. The pipeline's schema
accepts these seven and nothing else.

Type is a property of the claim entity — it describes the nature of the proposition, not the figure that instantiates it in any given paper.

**Epistemic** is the analyst's assessment of how strongly the claim is supported across its assertion(s): `strong`, `moderate`, `weak`, or `contested`. This should be updated when new assertions or reproductions come in. A claim that was `strong` from one paper and `failed:mismatch` in a reproduction should be moved to `contested`.

---

## 2. Assertions

An assertion is a situation: a paper asserting a claim at a moment in time, in a specific way. The assertion records the relationship between a claim entity and a paper entity — when a paper instantiates a claim in a particular figure, with a particular analysis, using a particular dataset.

The figure panel is a quality of the assertion, not a property of the claim. This is the key structural shift from the prior format. Panel `fig2a` tells you how paper `ejdrup-2026-dopamine` chose to present the claim — but the claim `dat-reuptake-dominates` could also be asserted in a different paper's supplementary figure, or in a table, or without a figure at all. The claim exists independently; the panel is how one paper chose to show it.

A claim can carry multiple assertion blocks, one per paper that asserts it. Each block records:

- `paper-slug` — the slug of the asserting paper, matching its directory name
- `doi` — the paper's DOI
- `panel` — the figure panel (or table, or analysis block) instantiating the claim in this paper
- `analysis` — the notebook or script that generates the result from data
- `dataset` / `dataset-doi` — the data deposit used
- `method` — the computational or experimental method
- `confidence` — the paper's own confidence level (strong / moderate / weak)
- `stance` — the paper's epistemic position toward the proposition (below)

### Stance

A paper does not only assert propositions. It also raises candidates it does not commit to,
argues that some are false, and reports what others have claimed. `stance` records which:

| Value | Meaning |
|:------|:--------|
| `asserts` | The paper claims the proposition is true. **Default** when the field is absent. |
| `entertains` | The paper raises it as a candidate and does not assert it. |
| `rejects` | The paper argues it is false. |
| `attributes` | Someone else asserts it; this paper reports that. Requires a citation in `source`. |

Stance belongs on the assertion rather than on the claim because the claim is
paper-independent (§1). The same proposition can be asserted by one paper and rejected by
another; when both papers' trees are read together, the claim entity carries two assertion
blocks with opposing stances and the disagreement becomes queryable. Were stance a property of
the claim, that case could not be represented at all.

Stance says what the paper concluded. The relations say *why*: a rejected alternative normally
carries an incoming `rules-out` edge from the evidence that eliminated it. Keep both — a paper
can reject something by dismissal with no evidence offered, and conversely the edge names which
control did the work, which stance cannot.

There is no separate value for "rejected". A claim asserted with `entertains` and an incoming
`rules-out` **is** a rejected alternative; one with `entertains` and no such edge is an *open*
alternative, a rival the paper raised and did not settle.

### Alternative explanations are claims

When a paper rules something out — a confound, a rival mechanism, a competing account — the
thing being ruled out is a proposition, and it gets a claim file like any other. Its role is
whatever it functionally is (usually `hypothesis`); what marks it as a rival is its stance, not
its role.

```yaml
---
uuid: [uuid4]
slug: alt-social-context-shifts-risk-attitude
claim: >
  The happiness difference between Social and Partner conditions reflects a
  social-context-driven shift in risk attitude rather than responsibility-contingent guilt.
role: hypothesis
epistemic: weak
assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.104323
    stance: rejects
    method: agent extraction from the paper's control analyses
---
```

and the control that kills it carries the edge:

```yaml
rules-out:
  - alt-social-context-shifts-risk-attitude
```

**Never point `rules-out` or `contradicts` at a claim the same paper asserts.** A paper does
not rule out what it claims. Where an alternative has no node, the temptation is to aim the
edge at the nearest claim that does — which produces a relation that is structurally valid and
factually false. Four such edges existed in this corpus, and one produced a contradiction
between two compatible findings. `scripts/check_relations.py` now rejects them.

---

## 3. Reproductions

A reproduction is a situation: an agent re-enacting an assertion to test whether it holds. It records who ran it, when, and what happened. A claim moves from `unverified` to `verified` (or `failed`) through reproductions.

**Status vocabulary:**

| Status | Meaning |
|:-------|:--------|
| `verified` | Ran the analysis; output matches the assertion |
| `failed:mismatch` | Ran the analysis; output does not match — discrepancy logged in `notes` |
| `unverified:no-data` | Data deposit not accessible; reproduction not attempted |
| `unverified:no-code` | Code not accessible; reproduction not attempted |
| `unverified` | Not yet attempted |

When a reproduction fails with `failed:mismatch`, the discrepancy should be described in `notes` with enough precision that a future agent can diagnose the cause. "Numbers differ" is not sufficient. "Clearance rate constant is 0.31 s⁻¹ in reproduction vs 0.18 s⁻¹ in paper; suspect different initial conditions used" is.

---

## 4. Belongings

Belongings are typed directed edges between claim entities. They express logical dependencies between propositions:

| Relation | Meaning |
|:---------|:--------|
| `supports` | This claim provides evidence for the target claim |
| `requires` | This claim would be invalid if the target claim were wrong — a structural dependency |
| `contradicts` | This claim is in direct tension with the target claim |
| `extends` | This claim builds on or refines the target claim |

These are not citations. They are statements about the logical structure of a claim graph. When you mark claim A as requiring claim B, you assert that A's validity depends on B's validity. Invalidity propagates: if B fails to reproduce, that failure has downstream consequences for every claim that requires B. The graph makes these dependencies explicit and auditable.

The `target` field takes the slug of the target claim. If the target claim lives in a different paper directory, use its slug — slugs are globally unique across the claim graph.

---

## 5. Conditionality as graph structure

Conditionalities are not annotations — they are claims. When a result claim depends on a model parameter, a methodological choice, or an assumption that carries uncertainty, that dependency is represented as a formal `requires` relation pointing at an **assessment claim** that is itself a node in the graph.

An assessment claim registers a parameter or assumption as an explicit entity: its value, its source, its uncertainty, and whether it has been sensitivity-tested. Example:

```yaml
---
uuid: [uuid4]
slug: d2r-initialization-unjustified
claim: >
  D2 receptor occupancy is initialized at 0.4 in the simulation without derivation
  from steady state; at EC50 = 7 nM and tonic [DA] ~10 nM, equilibrium occupancy
  would be approximately 0.59. No sensitivity analysis over this parameter is reported.
claim-type: assessment
concepts:
  - D2 receptor
  - initial conditions
  - model assumption
priority: 2026-03-29
epistemic: weak
assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: 1H
    method: code inspection
    confidence: weak
reproductions: []
---
```

The result claim then carries a `requires` relation:

```yaml
belongings:
  - relation: requires
    target: d2r-initialization-unjustified
```

This is how the graph carries conditionality structurally. The epistemic status of a claim is bounded by the weakest claim it requires. If `d2r-initialization-unjustified` is `weak`, every claim that requires it inherits that weakness — not by annotation, but by graph traversal.

**Three types of conditionality that should always be ontologized this way:**

1. **Model parameter assumptions** — when a simulation result depends on a parameter assumed from literature rather than measured in the paper. Register the parameter as an assessment claim: its value, citation, and whether uncertainty was tested.

2. **Model scope** — when a simulation operates at a different scale or architecture from the paper's primary model. Register the scope separation as an assessment claim that simulation-derived claims require. Add a `scope` field to the assertion block (e.g., `scope: varicosity-scale`, `scope: tissue-scale`, `scope: in-vivo`, `scope: ex-vivo`).

3. **Methodological assumptions** — when a key result depends on a choice (initialization, boundary condition, cluster detection threshold) that is not sensitivity-tested. Register the choice as an assessment claim with epistemic: weak.

**What this means for verification:** the reproduction step (Step 8) must also run assessment claims. Verifying an assessment claim means checking whether the paper acknowledges, justifies, or sensitivity-tests the assumption. If it does, the assessment claim's epistemic status rises. If not, it stays weak — and propagates weakness to every claim that requires it.

---

## 6. Naming conventions

Slugs should be:
- Lowercase, hyphenated
- 3–6 words
- A verb phrase that captures the proposition

Good examples: `dat-reuptake-dominates`, `d2-autoreceptors-suppress-tonic`, `phasic-release-saturates-clearance`, `novelty-drives-drn-firing`.

Avoid:
- Figure references: `fig2a-result` (the panel is an assertion quality, not the claim identity)
- Paper-specific language: `ejdrup-main-finding` (claims are independent of papers)
- Vague terms: `dopamine-result-1` (not meaningful to a domain expert without context)

The slug should be meaningful to a domain expert who has not read any specific paper. It should summarize the proposition in terms of the underlying phenomenon.

---

## 7. Directory structure

```
claims/
  <paper-slug>/
    index.md              # paper metadata: title, DOI, authors, abstract, GitHub, data deposit
    <claim-slug>.md       # one file per claim registered from this paper
    ...
```

Claims are registered into a paper-slug directory as the ingest point. For the prototype, this organization is fine and allows claims to be discovered alongside their primary paper. As the claim graph grows and claims are asserted by multiple papers, individual claim files can migrate to a flat `claims/` namespace — the UUID ensures identity survives migration, and the slug provides continuity.

---

## 8. Generating UUIDs

At claim creation, generate a UUID4:

```bash
python3 -c "import uuid; print(uuid.uuid4())"
```

Paste the output directly into the `uuid` frontmatter field. This happens once, at creation. It never changes after that.

---

## 9. Full example

```yaml
---
uuid: 3f7a2b1c-8e4d-4f9a-b2c1-7d3e5f8a9b0c
slug: dat-reuptake-dominates
doi: ~        # assigned when claims become formally citable; empty for now
claim: >
  DAT-mediated reuptake is the dominant mechanism of dopamine clearance
  in the dorsal striatum under physiological stimulation conditions.
claim-type: interpretive
concepts:
  - dopamine transporter
  - dopamine clearance
  - dorsal striatum
priority: 2026-03-29   # date this claim was first registered
epistemic: strong       # strong | moderate | weak | contested

belongings:
  - relation: supports       # supports | requires | contradicts | extends
    target: tonic-dopamine-sets-baseline
  - relation: requires
    target: dat-expression-confirmed

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig2a               # quality of the assertion, not the claim identity
    scope: tissue-scale        # varicosity-scale | tissue-scale | in-vivo | ex-vivo | in-vitro
    analysis: notebooks/fig2_dat_kinetics.ipynb
    dataset: https://zenodo.org/record/XXXXXXX
    dataset-doi: 10.5281/zenodo.XXXXXXX
    method: mathematical modelling
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-29
    status: unverified    # verified | failed:mismatch | unverified:no-data | unverified:no-code | unverified
    notes: ~
---

Optional prose body — caveats, alternative interpretations, pointers to contradicting claims in other papers. Use this for any reasoning that cannot be compressed into frontmatter: e.g., a known boundary condition where the claim may not hold, or a note that an earlier preprint version reported a different value.
```
