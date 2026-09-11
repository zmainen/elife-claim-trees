# The prompts

Seven prompts in `extract/prompts/`, one per layer that calls a model. Each is a self-contained
markdown document loaded as the system message; the user message is the slice of the paper, or
the upstream layer's output.

They are **declared inputs**. Each layer names its prompt under `reads:`, so a run records the
hash of the prompt that produced it, and editing one makes every run that used it stale. That is
the difference between a prompt being in version control and a prompt being accounted for: you
could always see that a prompt had changed, but nothing could tell you which claim files had
been built with the old one.

| File | Layer | Reads |
|:-----|:------|:------|
| `results-reader.md` | [`results-reader`](/elife-claim-trees/pipeline/results-reader/) | The abstract and results prose |
| `caption-reader.md` | [`caption-reader`](/elife-claim-trees/pipeline/caption-reader/) | The figure and table captions |
| `structure-reader.md` | [`structure-reader`](/elife-claim-trees/pipeline/structure-reader/) | The methods, supplements and section structure |
| `reconciler.md` | [`reconcile`](/elife-claim-trees/pipeline/reconcile/) | The three readers' outputs |
| `external-reviewer.md` | [`external-review`](/elife-claim-trees/pipeline/external-review/) | The paper plus the reconciled draft |
| `edge-inference.md` | [`edge-inference`](/elife-claim-trees/pipeline/edge-inference/) | The draft's claims, numbered |
| `coverage-adjudicator.md` | [`adjudication`](/elife-claim-trees/pipeline/adjudication/) | Unresolved coverage spans against the claim tree |

Each layer's own page renders the prompt it runs under, in full, read from the committed file
at build — so what a reader sees on
[`results-reader`](/elife-claim-trees/pipeline/results-reader/) is the prompt that produced the
claims below it on the same page. The [agents page](/elife-claim-trees/pipeline/induction/)
shows all seven side by side, for reading them against each other.

## Shared structure

1. **Identity** — who the agent is and which layer it serves
2. **Input contract** — what the user message will contain
3. **Role** — what this agent is positioned to see that the others cannot
4. **Failure modes** — the specific errors it is most prone to, drawn from `docs/method.md`
   § 3.3
5. **Output schema** — the JSON shape it must produce
6. **Field guidance** — what each field should contain
7. **Quantity expectation** — roughly how many claims it typically surfaces
8. **What good looks like** — the qualities of correct output
9. **Worked examples**, where the guidance is otherwise abstract

The reconciler adds the confidence taxonomy — `high`, `contested`, `single-source`. The external
reviewer adds its bias rules, of which there are seven; the last three were added in the
iteration that lifted corpus role agreement from 78% to 83%.

The failure-mode sections are the load-bearing part, and they are specific rather than generic.
A single agent reading a whole paper invents numbers where the prose summarises ("a large
fraction" becomes "63 of 100 cells"), attaches claims to whichever panel it read last, and
extracts speculation from the discussion as though it were a result. Each reader's prompt names
the errors that reader in particular makes.

## Authoring a variant

To test a change without touching the defaults:

```bash
mkdir extract/prompts/my-variant
cp extract/prompts/caption-reader.md extract/prompts/my-variant/
# edit extract/prompts/my-variant/caption-reader.md
```

A variant directory need not be complete — prompts it does not contain fall back to the default,
so a variant can be a single-file change and the diff is the experiment.

Measure it before keeping it:

```bash
elife-extract evaluate --reference-dir ../claims/ --work-dir /tmp/eval \
  --all --prompt-variant my-variant
```

Diff the aggregate against the baseline. See
[measuring a prompt change](/elife-claim-trees/docs/evaluate/) for the discipline, and for the
worked example where one addition to the reviewer prompt moved a paper from 57% to 71% role
agreement.

Two failure modes to avoid, both of which produce a better number and a worse system:

**Editing until the aggregate rises.** That fits the prompt to the ten-paper reference corpus
rather than to the task. Change what a scorecard diagnosed, not what an aggregate rewards.

**Keeping a change measured on one paper.** A revision that lifts one paper and costs three is
common and only visible corpus-wide.

## Where they are loaded

`agents.py:load_prompt()` reads them at run time; `config.py:Config.prompt_path()` resolves the
variant. Nothing caches them across a run, so a prompt is read from disk exactly when it is
used — which is what makes the hash the ledger records the hash of the file that was actually
sent.
