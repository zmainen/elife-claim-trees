# Kinds of decision

**Status:** proposed
**Frames:** [#31](https://github.com/zmainen/elife-claim-trees/issues/31) · [#56](https://github.com/zmainen/elife-claim-trees/issues/56) · [#82](https://github.com/zmainen/elife-claim-trees/issues/82)
**Depends on:** `docs/design/2026-09-11-layers-as-pipeline.html` (approval as an operation on a version; a layer as a proposal)

Four different things have been called "review" in this repository, and a badge on the site
that does not say which one it means says nothing. This note names the kinds, says what a
person does in each, what record each leaves in git, how the site shows them, and how the
issue tracker is typed so that a title tells you which kind you are looking at.

## The four kinds

| Kind | Question it answers | Who decides | Record | Effect |
|:--|:--|:--|:--|:--|
| **Code** | Does the mechanism do what its declaration says? | Tests and gates; a reviewer of the diff | A PR; the ledger marks runs stale where inputs moved | Mechanical. No meaning changes. |
| **Scheme** (general) | What does this mean, for every paper? | A person, once | A design note; the declaration (`layers.yaml`, `relations.py`, `vocabulary.py`) with `status: accepted`; an entry in `runs/approvals.jsonl` naming the declaration's version | Propagation: every run under the old scheme is stale. |
| **Adjudication** (specific) | Is this version of this layer's output right, for this paper? | A person, per version | A verdict file beside the output; an entry in `runs/<paper>/approvals.jsonl` naming the version and the verdict file | That version is approved; the next is not until read. |
| **Run** | Produce the next version under the current scheme. | Nobody; the runner | A ledger entry | A new version, unread. |

The first three are decisions; the fourth is not, and calling it one is how "carry the nine
papers through the layers" became an issue rather than a command. A run is what happens after
a scheme is accepted and before an adjudication; it needs an issue only when it needs money.

Two things that look like a fifth kind are not. Deciding a drafted gap claim in the margin
(#78) is an adjudication of some claims of a version rather than all of them: the same
verdict record, marked partial. Auditing a verification record against the run that produced
it (#36) is an adjudication of the `verification` layer's output: a verdict per record. Both
use the specific kind's machinery.

## What a person does

**A scheme ruling.** The question is stated as a question, in a design note, with the
corpus evidence and a recommendation, and declared with `status: proposed` and `issue: N`. The
discussion is the issue. The ruling is written into the declaration — the definition in
`relations.py` or `vocabulary.py`, the row in `docs/method.md`, `status: accepted` in
`layers.yaml` — by a PR that closes the issue, and the person's approval of that declaration
version is appended to `runs/approvals.jsonl` by `pipeline.py approve --declaration <layer>`.
The ledger then reports every dependent run stale, and the re-runs are runs. #19, #20 and #28
are rulings waiting to be made; the parts and questions changes were rulings made by
proposal and acceptance in a day, and should have left the same record.

**A layer acceptance** is a scheme ruling whose question is "should this step exist, and is
this what it should do", and whose evidence includes adjudicated outputs of the layer on real
papers. That is #31, and it is why per-paper adjudications accumulate into a general
acceptance rather than standing beside it.

**An adjudication.** Four steps, and the surface supports each:

1. *Prepare.* A verdict skeleton for the version (`verdicts.py skeleton`, every claim `keep`
   and every edge `ok`, each marked not yet considered), or the same in the margin of the
   paper.
2. *Read.* A verdict per claim (`keep`, `strike`, `merge-into`, `part-of`, a corrected role
   or panel) and per edge (`ok`, `wrong-direction`, `wrong-relation`, `strike`, `missing`),
   and answers to the paper's own open questions. A partial reading is a legitimate state
   and is shown as one.
3. *Approve.* `pipeline.py approve <paper> <layer> --v <N>` naming the verdict file. The
   approval is bound to the version; when the layer runs again it does not follow.
4. *Apply.* The verdicts become the next version through the writer's carry machinery, and
   that version is approved by construction, because it is the reader's own reading. Its
   successors are not, but the verdicts travel to them through the matcher pairs as
   evidence, and the badge says how many carried.

## The procedure is itself a scheme

The four steps above, the verdict vocabulary (`keep`, `strike`, `merge-into`, `part-of`, a
corrected role or panel; `ok`, `wrong-direction`, `wrong-relation`, `strike`, `missing`) and the
rule that a partial reading is a state are not given. They are a proposal, and the right way to
treat them is the way this note treats every other general question: as a declaration with a
version, ruled on once, and scored on real papers before it is accepted. A verdict file names
the procedure version it was read under, the way a run names the prompt hash it ran under, so
a reading made under an earlier procedure stays a valid record rather than becoming an
undocumented one.

What makes the procedure evaluable is that its output is structured. Four measurements need
nothing the repository does not already have:

- **Agreement.** Two readings of the same version, by two people or by a person and a model,
  scored with the matcher that `evaluate score` already uses: the fraction of claims and edges
  on which the verdicts coincide, by verdict kind. A procedure whose readers disagree about
  what `part-of` means has a vocabulary problem, not a reader problem.
- **Yield.** How long a reading takes, and what fraction of verdicts are anything other than
  `keep` and `ok`. A procedure under which every verdict is `keep` is cheap and blind; one
  under which half are corrections is measuring the pipeline, not the reader.
- **Persistence.** How many verdicts carry to the next version through the matcher pairs.
  This is the badge's "k carried" counter, read as a property of the procedure rather than of
  one paper.
- **Effect.** Whether applying the verdicts moves the evaluation scores against the reference
  in the direction the reader intended, and whether an adjudicated version used as the
  reference ranks candidate runs differently from the unadjudicated one.

Changing the procedure is a scheme ruling and goes through #31 like any other. This
separates three things that #82 has been carrying together: the surface is code, the
procedure is scheme, and the reading of Gädeke v3 is the adjudication.

## What the site shows

A cell has three facts, and today's badge folds them into one word. It should show three:

- **Mechanism**: current, stale, blocked, absent, not applicable, or run not observed —
  what the ledger computes from hashes. Unchanged.
- **Scheme**: accepted, proposed, or open — the status of this layer's declaration and of
  every corpus-scope declaration it needs. A tree built while `relation-vocab` is open is
  *provisional*, and the site should say so on the cell rather than only on the vocabulary
  page.
- **Adjudication**: approved v<N> by <person>; partial, k of n; superseded (an earlier
  version was approved); or unread. From `approvals.jsonl` and the verdict file.

A layer page carries the scheme badge for the declaration itself, with who accepted it and
when, beside the counter of papers adjudicated under it. The pipeline matrix keeps mechanism
as the cell's colour and adds a mark for adjudication, so "which papers has a person read"
is visible at corpus altitude, which it never has been.

## What the tracker looks like

Issues carry a kind, as a label: `kind:code`, `kind:scheme`, `kind:adjudication`, `kind:run`.
Titles follow the kind. A scheme issue is the question it asks ("Is `dissociates-with` an
opposition?"). An adjudication issue is the paper and the version ("Adjudicate Gädeke
claim-tree v3"). A run issue is the command ("Run the chain on the nine papers under the
standard profile"), exists only if it costs money, and closes when the ledger shows the
runs. Parents group by kind: #56 for the pipeline's code, #31 for the scheme rulings and
layer acceptances, one per paper for its adjudications.

Consequences for the current tracker, applied with this note:

- #18 closes. It is a run, and what it needed — a runner for every layer, versioned trees, a
  profile — is either done or is #85. The command is `pipeline.py run <paper> claim-tree`
  per paper.
- #31 becomes the parent of #19, #20 and #28, which are its first three rulings, and of a
  code sub-issue for `approve --declaration` and the scheme badge.
- #82 is renamed to the paper and the version it adjudicates; its tooling half (the surface
  and gold scoring, in flight) is a code sub-issue of #56.
- #36 is an adjudication of the verification layer and is labelled so.
- The adjudication procedure gets its own scheme issue under #31, so that a change to the
  verdict vocabulary or the steps is ruled on and versioned rather than edited in passing.

## What this does not decide

Whether a scheme ruling needs one person or two. The record can hold several approvals of a
declaration version; whether acceptance requires more than one is a governance question the
corpus is too small to have needed yet.

Whether adjudication verdicts should be public on the site or only their counts. The
verdict file is committed, so they are public in the repository; the note recommends the site
show counts and the corrected values, and link the file.
