# Working on layers

`layers.yaml` is the only account of how this corpus is produced. Everything downstream trusts
it: `state` computes staleness from `needs`, the site renders cells from it, and a reader is
told a cell is current on its authority. A layer that is wired wrongly does not merely
misdocument itself — it reports `current` over output that is no longer true, which is the one
thing the ledger exists to prevent.

This is how to add one, change one, and review what one produced, and what to check afterwards.

---

## 1. Adding a layer

A layer is a question with an answer that lands in a file. Write the question down first; if it
cannot be put as a question about one paper, it is probably not a layer.

**Declare it.**

```yaml
  - id: gap-claim
    kind: candidate            # step · candidate · judgement · question · feature
    question: What claim would close each gap?
    needs: [adjudication, claim-tree, claim-format]
    reads: [extract/prompts/gap-claim.md, scripts/gap_claims.py]
    produces: ["runs/{paper}/gap-claim.output.json"]
    by_from: model
    command: "python3 scripts/gap_claims.py {paper} --answer runs/{paper}/gap-claim.answer.json"
```

`needs` is what makes it stale and what orders it. `reads` is everything else it opens —
prompts, its own script, a vocabulary file. **Both are load-bearing.** A path the command
touches and neither field names is an input whose change nothing will notice.

**If a model answers it, give it the pair.** Every model-answered layer carries
`--dump-prompt PATH` and `--answer PATH`: the first writes the exact request, the second takes
an answer back through the same validation a backend reply would get. A supplied answer records
`model: supplied:<path>` rather than naming a model that never ran. Keep the answer in
`runs/{paper}/<layer>.answer.json` so the recorded path is repo-relative and auditable.

**Validate before writing.** The validator is the layer's contract with whatever answered it.
Refuse the whole answer rather than write a partial one: every item answered, nothing invented,
every reference resolving to something this paper actually has.

**If it writes into `site/src/data/`, add it to `make data`** — or accept that the published
site will serve whatever was last committed. See §4; this is not hypothetical.

**Run it and record it.** `python3 scripts/pipeline.py run <paper> <layer>` runs the unmet
dependencies first and writes the ledger entry. Running the command by hand records nothing,
and an artifact with no entry reads `unrecorded` forever.

---

## 2. Changing a layer

Editing a script or a prompt named in `reads` moves that layer's hash, so its cells go stale
and everything downstream goes blocked. That is the system working. The work is to re-run them
in dependency order, and `pipeline.py run` already does that.

What it cannot do for you: a layer that a model answers cannot be re-run without an answer.
`--answer` replays a stored one, which is honest only while the question has not changed. If
the prompt changed, the stored answer is an answer to a different question — re-ask it.

**Rewriting a claim tree is the expensive case.** New slugs and new UUIDs orphan every derived
text layer at once: the plain wordings no longer match a slug, the marks no longer resolve to a
claim, the adjudicated verdicts were judged against a tree that no longer exists. All of it is
reported as stale and none of it is fixed by reporting. Budget the re-runs with the rewrite.

---

## 3. Reviewing what a layer produced

Two gates, and they are different.

**A claim decision** happens in the paper view. A drafted claim marks the sentence it came from
and its card opens in the margin: add it, reword it, change its type, or say it is not a claim.
Decisions append to `review/gap-claim-decisions.jsonl` through `/dev-review.json`, which exists
only under `npm run dev` — the published site is static and says so rather than offering a
button it does not have. `scripts/promote.py --write` then writes the accepted claims and
records the approval.

**A layer version** is approved with `pipeline.py approve <paper> <layer> --by "name"`. An
approval names a version: approving v2 says nothing about v3, and when the layer runs again the
approval does not follow.

Keep rejections. What a reviewer turned down is the only evidence there is about how good the
drafting was, and keeping only the accepted drafts destroys the measurement.

---

## 4. What to check, and what is still wrong

```bash
python3 scripts/audit_layers.py      # the graph against the commands
python3 scripts/pipeline.py state    # every paper against every layer
```

The audit answers five questions. The first has no findings and is worth keeping that way. The
rest are open and are listed here so they are not rediscovered:

**A layer that reads what it does not declare.** None, now. `verification` ran
`verification/audit_run.py` without declaring it, so editing the runner left every verification
cell reading `current`.

**Site data no build step regenerates.** `article`, `abstract-map`, `synthesis`, `summaries`
and `plain-claim` all write into `site/src/data/` and `make data` runs none of them. `make
build` regenerates what it can and publishes whatever else is committed, so a stale artifact
reaches the site with nothing in the way. This is not theoretical: rewriting Gädeke's tree to
v2 left 68 of 74 claims with no wording, and the published site showed 68 blank lines where its
claims had been. The staleness was computed, reported, and never consulted by the thing that
deploys.

**`edge-inference` runs before the claim files exist.** It needs only `reconcile`, so it
decides relations from the reconciled candidates and `claim-tree` writes what it inferred.
Nothing downstream of `claim-tree` decides a relation, so a claim added later — every claim a
reviewer promotes — can never be connected to anything. 34 claims currently have no outgoing
relation; 12 relations point at a claim that does not exist in their paper, 9 of them
`rules-out`.

**`external-review` asks a question `coverage` answers.** "What structure did the three readers
systematically miss?" is asked at `reconcile`, before the tree exists, and measured after it by
`coverage`. The question is asked where it can only be guessed at and not asked where it has
been measured.

**No layer version has ever been approved.** Zero, across the corpus, in a project whose README
says no human has checked any of it.

---

## 5. The invariants

- A path the command touches is named in `needs` or `reads`.
- A layer that a model answers carries `--dump-prompt` and `--answer`, and validates.
- An answer is kept where the artifact can point at it.
- A run goes through `pipeline.py run`, or it did not happen.
- An output under `site/src/data/` is regenerated by `make data`, or the site can publish a
  stale copy of it.
- An approval names a version, and does not follow the layer when it runs again.
