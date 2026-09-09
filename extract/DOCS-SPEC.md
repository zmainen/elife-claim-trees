# Documentation site spec — elife-claim-trees extraction pipeline

**Audience:** eLife technical staff (Damian Pattinson, Andy Collings, and their engineers). Quality bar: Anthropic-style developer documentation — narrative voice, conceptually grounded, progressive disclosure, code-level when needed, diagrams where they earn their keep.

**Where it lives:** As a new section in the existing Astro site at `~/Projects/mainenlab/elife-claim-trees/site/src/pages/docs/`. The site is already built (Astro 6 + React + Tailwind); adding `/docs/` as a sibling of `/papers/` and `/method/` is a localized addition, not a redesign.

**Two artifacts in scope:**

1. **The presentation** — a single overview document the presenter walks through in 30–45 minutes tomorrow. Lives at `/docs/overview/` as a top-of-funnel page; doubles as the post-talk landing page.
2. **The docs site** — the deeper pages (architecture, reference, validation, contributor guide). Audience-after-the-talk: someone who watched the demo and wants to dig in.

---

## Site structure (top-level navigation)

Seven sections, ~22 pages total. Each page is a coherent unit; cross-references are kept tight (no link-soup).

### 1. **Overview** (entry point — also the talk script)

| Page | What it covers | Length | Diagram? |
|:-----|:---------------|:-------|:---------|
| `1.1 What this system is` | One-paragraph elevator + the problem it solves (manual claim extraction is the bottleneck of the methodology) + the system's bet (three-agent partition + Opus review) | 1 page | architecture-at-a-glance |
| `1.2 Quick demo — one paper end to end` | Headley walked through: DOI in, claim files out. Each step shown with what happens, what gets written. The presentation's spine. | 2 pages | per-step screenshots/output blocks |
| `1.3 When to use it` | Use cases: extracting a new paper, validating prompt changes, batch operation; non-use cases (Step 8 verification, cross-paper graph). | 1 page | — |

### 2. **Methodology** (situating the system in eLife's framework)

| Page | What it covers | Length | Diagram? |
|:-----|:---------------|:-------|:---------|
| `2.1 The 8-step process` | The methodology the system implements (already in `docs/method.md` § 3 — link out, summarize the 8 steps in 1 page with system mapping) | 1 page | flowchart |
| `2.2 The claim schema` | What a claim is — slug, claim, panel, role, claim-type, edges. One real example walked through. | 2 pages | annotated example |
| `2.3 What the curator does, what the system does` | The division of labor: prose extraction, role classification, the review gate. Where human judgment is load-bearing vs where it's cheap to automate. | 1 page | — |

### 3. **Architecture** (the system itself)

| Page | What it covers | Length | Diagram? |
|:-----|:---------------|:-------|:---------|
| `3.1 The pipeline at a glance` | Full pipeline diagram: PDF → prepare → 3-agent extract → reconcile → external review → write → verify-refs. Each box clickable to its detailed page. | 1 page | **central architecture diagram** |
| `3.2 The three-agent partition` | Why three readers and not one; the Results / Caption / Structure split; what each sees; why partitions reduce certain failure modes (quantitative hallucination, panel mis-assignment). | 2 pages | partition diagram |
| `3.3 Reconciliation` | How three lists of claims become one draft table; semantic matching across agents; the high/contested/single-source confidence taxonomy. | 1 page | — |
| `3.4 The external reviewer (Step 4.5)` | The "make Opus do what the curator would do" step. Why this exists (Phase F finding: prose extraction misses the deductive layer). The four-then-seven biases the prompt addresses. **The most novel part of the architecture.** | 2 pages | before/after on Headley |
| `3.5 The review gate` | The four review modes (interactive, external, auto-approve, dry-run); when each is right; the methodology's Step 5 framing. | 1 page | decision flowchart |

### 4. **Using the CLI**

| Page | What it covers | Length | Diagram? |
|:-----|:---------------|:-------|:---------|
| `4.1 Install & configure` | Mostly mirrors `INTEGRATION.md` § 1-2 (already written) | 1 page | — |
| `4.2 First paper walkthrough` | The "first 10 minutes" experience. From DOI to claim files with explanations. | 2 pages | terminal screenshots |
| `4.3 The five subcommands` | Reference for `extract`, `write`, `verify-refs`, `run`, `evaluate` — what each does, when to use it, common flags. | 2 pages | — |
| `4.4 Review modes — when to use each` | Deeper than § 3.5: cost / quality / human-time tradeoffs per mode. Worked examples for the three operational shapes (single-paper curated, batch unattended, batch-then-review). | 2 pages | comparison table |
| `4.5 Batch operation` | Running on many papers; using `evaluate` for validation; cost projection; rate-limit handling; the `--skip-existing` resumability story. | 1 page | — |
| `4.6 Cost & performance` | Per-paper / per-step / per-model breakdown; how to reduce cost (model overrides, --max-claims, prompt variants); measured numbers from the 10-paper sweep. | 1 page | cost table per phase |

### 5. **Validation**

| Page | What it covers | Length | Diagram? |
|:-----|:---------------|:-------|:---------|
| `5.1 How we measure quality` | The round-trip methodology: extract on a paper that has a curated reference, score the CLI's output via Opus matcher on (recovery, panel, role) | 1 page | round-trip diagram |
| `5.2 10-paper sweep results` | The aggregate scorecard with mean/median per metric. What passed, what didn't. Per-paper breakdown table. | 2 pages | per-paper bar chart, aggregate table |
| `5.3 Known limitations` | Panel agreement at 55% — the multi-panel collapse problem; role on certain paper structures (kammer, rozak); methodology fallback chain not implemented; the canonical-script DOI bug. | 1 page | — |
| `5.4 The iteration discipline` | How prompt changes get validated before they ship: change → re-run `evaluate` → diff aggregate → decide. The kammer iteration as the worked example (57% → 71% role on one targeted prompt change). | 1 page | — |

### 6. **Reference**

| Page | What it covers | Length | Diagram? |
|:-----|:---------------|:-------|:---------|
| `6.1 Configuration reference` | Every env var, every CLI flag, with defaults and meaning | 2 pages (table-heavy) | — |
| `6.2 The 9 roles` | Each role with definition, signal phrases, claim-type pairing, edge patterns it carries, an example from the corpus | 3 pages | role-relationship diagram (entails / derived-from / tests / supports) |
| `6.3 The 14 edge types` | From `docs/method.md` § 4.3 — `requires`, `supports`, `entails`, `derived-from`, `tests`, `refutes`, `rules-out`, `dissociates-with`, `validates`, `predicts/confirms`, `interprets`, `enables-method`, `scopes` | 2 pages | argument-pattern diagrams |
| `6.4 The prompts` | The five prompt files (results-reader, caption-reader, structure-reader, reconciler, external-reviewer) — full text, why each design decision, how to write a variant | 3 pages | — |
| `6.5 API reference` | Python module reference: prepare / agents / reconcile / external_review / review / write / verify_refs / evaluate / config / schema. One section per module. | 4 pages (the longest section) | — |
| `6.6 Glossary` | Key terms: claim, panel, role, claim-type, edge, draft table, review gate, deductive layer, structural inference | 1 page | — |

### 7. **For contributors**

| Page | What it covers | Length | Diagram? |
|:-----|:---------------|:-------|:---------|
| `7.1 Code structure` | Where things live (extract/, prompts/, tests/), how to find what you need | 1 page | dir tree |
| `7.2 Adding a prompt variant` | The `--prompt-variant` flag's design; how to fork and test a prompt change without touching the default | 1 page | — |
| `7.3 Running the validation sweep` | How to use `evaluate` to measure your changes; the kammer iteration as worked example | 1 page | — |
| `7.4 Design decisions` | The `architecture/decisions/` ADR-style record. Why three agents not one, why streaming, why the schema deviates from method.md, etc. | 2 pages | — |

---

## Tomorrow's presentation — what we ship first

Not all 22 pages need to exist by tomorrow. The presentation is the spine; the rest is the path the audience walks afterward. Pages required for tomorrow:

**Must ship (the presentation walks through these):**
- 1.1, 1.2, 1.3 (overview + demo + use cases)
- 2.1, 2.3 (methodology recap, division of labor)
- 3.1, 3.2, 3.4, 3.5 (architecture overview, agent partition, the external reviewer, review modes)
- 5.2 (the 10-paper sweep results)
- 4.1, 4.2 (install + first paper)

**That's 12 pages.** Ship-ready by tomorrow.

**Should ship within a week (deep dives the curious will want):**
- 2.2 (claim schema)
- 3.3 (reconciliation detail)
- 4.3, 4.4, 4.5, 4.6 (CLI reference, modes, batch, cost)
- 5.1, 5.3, 5.4 (round-trip methodology, limitations, iteration discipline)

**That's 9 more pages.** A week of writing.

**Can ship over the following weeks (the long tail):**
- 6.1–6.6 (full reference)
- 7.1–7.4 (contributor guide)

---

## Format and stack

**Astro pages.** Each documentation page is `.mdx` (Markdown + JSX components for diagrams, code blocks, callouts). The site already has a config; adding `pages/docs/<section>/<page>.mdx` works without infra changes.

**Diagrams.** Three options:
1. Mermaid (rendered client-side; works in Astro with `astro-mermaid` integration)
2. Hand-drawn SVG (more control, more work)
3. Tikz/LaTeX (overkill)

I'd recommend **Mermaid for the architecture diagrams** (pipeline flow, three-agent partition, role relationships) and **inline SVG / image for the cost-per-step bar charts and validation results**.

**Code examples.** Astro has built-in syntax highlighting via Shiki. Use it.

**Cross-page navigation.** Sidebar with the 7-section structure; collapsible per section. Astro's `@astrojs/starlight` would be the right choice if we want to skip building this; alternative is rolling our own using Astro layouts (~1 day's work).

**Decision needed:** do we adopt Starlight as a sub-site under `/docs/` (clean, pre-built TOC + sidebar + search), or do we build the docs in the existing Astro layout (consistent visual identity with the rest of the site)?

I'd lean **Starlight**. Time-to-presentation > visual consistency, and we can theme Starlight to match later.

---

## Effort estimate

| Phase | Pages | Estimated effort | Cost (LLM-assisted writing) |
|:------|------:|:-----------------|:----------------------------|
| Tomorrow's presentation pages | 12 | 4-6 hours | ~$10 in LLM-assisted drafting |
| Week-1 deep dives | 9 | 6-8 hours | ~$10 |
| Long tail (reference + contributor) | 13 | 10-15 hours | ~$15 |
| **Total** | **34** | **~25 hours** | **~$35** |

Most of the writing can be drafted from existing inscriptions (`README.md`, `INTEGRATION.md`, `.haak/method.md`, the job's worklog, the prompts themselves). The drafts get refined for narrative flow + diagrams added.

---

## What I need to confirm with you before starting

1. **Site location.** Docs go in the external `~/Projects/mainenlab/elife-claim-trees/site/` (the Astro site eLife will see), not in the haak repo. Confirm? Or do you want a separate doc site?

2. **Starlight vs custom Astro.** Trade speed-to-presentation for visual consistency, or invest in matching the existing site? I lean Starlight.

3. **Diagrams.** Mermaid for architecture, hand-drawn for results charts? Confirm, or do you want a different approach?

4. **Tomorrow's presentation format.** Is this a slide deck (Keynote / PPTX), a guided web tour (presenter walks through the docs site live), or a PDF document? My spec assumes "guided web tour" — the docs site itself is the presentation.

5. **Audience composition.** Just Damian + Andy, or their engineering team too? The depth I assume depends on whether non-technical decision-makers will be in the room.

6. **Start now or wait for the v2 sweep to land?** The v2 sweep is mid-flight; results will inform Section 5.2. I can start writing the non-validation pages in parallel and fold the new aggregate in when it lands.

Once those are confirmed, I'll start producing the 12 must-ship pages tonight in priority order:

1. **3.1** — pipeline-at-a-glance (the central diagram everyone references)
2. **1.1, 1.2** — overview + demo (the talk's opening)
3. **3.4** — the external reviewer (the most novel architectural decision)
4. **5.2** — sweep results (the credibility)
5. **2.1, 2.3** — methodology recap
6. **3.2, 3.5** — agent partition + review modes
7. **4.1, 4.2** — install + first paper
8. **1.3** — when to use it (the close)

Ordering reflects: get the load-bearing diagram done first, then the spine, then the differentiator (reviewer pass), then the receipts.
