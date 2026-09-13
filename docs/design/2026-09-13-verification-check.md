# The verification check sits beside the warrant, never over it

**Status:** the ruling stands and the layer ran; its code is now in neither working tree
**Issue:** [claim-graphs#27](https://github.com/zmainen/claim-graphs/issues/27), the port. Filed
here as #126, which moved with the machinery.
**Frames:** [#36](https://github.com/zmainen/elife-claim-trees/issues/36) · [claim-graphs#20](https://github.com/zmainen/claim-graphs/issues/20)
**Depends on:** the `warrant` layer, the `verification` layer, `docs/claim-format.md`. The layer's
own code was `extract/elife_extract/verification_check.py`, which the split removed from this
repository without it arriving in the machinery — see *What this repository still holds*.

The v2 warrant rulings (`docs/design/2026-09-13-warrant.md`) drew a line this note builds on:
warrant reasons only from what the paper reports and how its argument hangs together, as the
tree records it. A reproduction is not part of that. Re-running the authors' code on the
authors' data answers a different question — did the deposited computation produce the reported
number? — and it answers it with a different kind of evidence. The two must not be folded
together, because a reader who sees one word cannot then tell which question it answered.

So a check is a separate field. This note states the rule that governs every check, and builds
the first of them.

## Warrant and each check are separate fields

A claim carries a `warrant` — how well the tree's argument supports it — and, beside it, one
field per check. The first is `check_verification`: did a re-run stand behind the claim? A
methods assessment, a statistics check, a citation check would each be another such field, added
by another layer, each writing beside the warrant and none of them into it.

The rule is that a check never overwrites the warrant. It sits beside it. On the claim the site
shows the pair — *warrant · verification* — as two chips, and the warrant keeps saying what the
edges say whatever the check found. The one thing that *does* overwrite a warrant is an
adjudication verdict: a person reading the claim and recording a judgement about its support.
That is a decision about meaning, stored because recomputing it would destroy it; a check is a
mechanical reading of records, and the two are not interchangeable.

The reason to keep them apart is the same reason the reproduction palette on this site is slate
and blue rather than green and red: a re-run that reproduces a number is not a claim that the
finding is true, and a re-run that fails to reproduce one is not a claim that it is false. It is
a fact about our run. Written into the warrant, it would read as a verdict on the science. Written
beside it, it reads as what it is.

## The verification-check layer

`verification-check` is a `feature` layer, like `warrant`, `stance` and `parts`: it revises the
tree rather than making a new kind of thing. It is mechanical — no model, no prompt — so it has
no `--dump-prompt`/`--answer` seam. For every claim it reads two sources and writes one verdict.

The two sources are the reproduction records the claim carries (`reproductions:`, with a status
of `verified`, `partial`, `mismatch`, `blocked` or `unattempted`) and the verification provenance
the audited run wrote (`verification/<paper>/provenance.json`, whose per-claim `results` carry a
PASS/WARN/FAIL status and whether the value was actually `measured` rather than recalled from a
deposit). The verdict is one of six words, and the rule is precedence over that evidence — the
most adverse *informative* verdict a claim's evidence supports wins:

| Verdict | What it reads |
|:--|:--|
| `reproduced` | a record marked verified whose provenance shows the script ran and measured the value |
| `partial` | recorded verified but not observed running, a `partial` record, or a run that executed without measuring the value |
| `mismatch` | a re-run that disagreed with the paper (a `mismatch` record or a FAIL run) — the site shows it as contested-by-verification |
| `blocked` | a record that could not be run — no data, no code, specialist compute |
| `unattempted` | a record not yet tried, or a recorded status this rule does not name |
| `unrecorded` | nothing — no record and no provenance for this claim |

Precedence is why a claim with both a `blocked` record and a `mismatch` record reads `mismatch`:
the reader must see the disagreement. The verdict lands in `check_verification:`, with
`check_verification_from:` naming the record statuses and provenance it read, so the reading is
auditable against the evidence. `warrant:` is never read or written here.

The MIRA and OXA exporters are left alone for now — no interchange format has a node for a check
any more than it has one for a warrant — and the export mapping follows in its own change.

## The first real case: the dopamine dSTORM claim

`ejdrup-2026-dopamine`'s `dat-clustering-greater-in-vs` is where this earns its keep. The paper
reports DAT more nanoclustered in VS than DS at *p* = 0.012 with *n* = 12 DS, *n* = 13 VS. The
deposited CSV (Zenodo record 18046987) has the sample sizes reversed — *n* = 13 DS, *n* = 12 VS —
and Welch's *t* on it gives *p* = 0.029 two-tailed; no standard test reproduces 0.012. The
direction (VS > DS) holds; the number and the *n*s do not. The claim carries a `mismatch`
reproduction record beside a later `blocked` one.

Under this ruling that claim reads: **warrant as its edges say** — the tree's argument still
supports the empirical result at whatever level its `confirms`/`validated-by`/`supported-by`
edges warrant, unchanged by the re-run — and, beside it, **verification: mismatch**, shown as
contested-by-verification. The two facts stand side by side. Neither is allowed to silence the
other, which is exactly what would have happened had the mismatch been written into the warrant,
or the warrant been left to imply the re-run agreed.

## What this repository still holds

The split moved the machinery to `zmainen/claim-graphs` and took everything under `extract/` with
it, but this layer's declaration never arrived there. So the layer exists in neither working tree,
and the corpus is left holding the evidence of runs that nothing can currently reproduce. Porting
it is machinery work ([claim-graphs#27](https://github.com/zmainen/claim-graphs/issues/27), which
names all six pieces); what follows is the corpus side a port has to satisfy.

**The code survives in history.** `extract/elife_extract/verification_check.py` — 77 lines, no
model and no prompt — is readable at `e8a2aa5^`:

```
git show e8a2aa5^:extract/elife_extract/verification_check.py
```

**Three runs are committed, on the two papers the rule was written for.**

| paper | committed output |
|:--|:--|
| `ejdrup-2026-dopamine` | `runs/ejdrup-2026-dopamine/verification-check.output{,.v1}.json` |
| `gadeke-2026-guilt-insula` | `runs/gadeke-2026-guilt-insula/verification-check.output{,.v1,.v2}.json` |

Within each paper every one of those files is byte-identical, which is not an accident worth
tidying away. Gädeke's v2 was a re-run on tree v7 after edge completion and warrant v3 — the
argument underneath the claims changed, and the check's verdicts did not move by a byte. That is
the ruling in this note holding: the check reads reproduction records and verification provenance,
never `warrant:` and never the edges, so a changed argument must leave it unchanged. A port that
reproduces the bytes has also reproduced that independence.

These outputs are therefore the correctness test, and a strict one: `make fresh` compares
regenerated artifacts against what is committed, so a reimplementation that changes one byte of a
verdict or of `check_verification_from:` fails the gate rather than quietly publishing a second
opinion.

**The ledger describes commands that no longer resolve.** `runs/ejdrup-2026-dopamine/ledger.jsonl`
and `runs/gadeke-2026-guilt-insula/ledger.jsonl` carry three `verification-check` records whose
`cmd` reads `cd extract && python3 -m elife_extract.cli verification-check --paper <paper>` and
whose declared input is `extract/elife_extract/verification_check.py`. Both were true of the runs
that happened and neither is true of this repository now. They are left as written, because a
ledger record is a statement about a past run, and editing it to match today's layout would make it
a worse record rather than a better one.

**No declaration accounts for any of it, so nothing flags it.** `verification-check` is absent from
the machinery's `pipeline/layers.yaml`, and therefore from `pipeline.layers`,
`pipeline.declarations` and `pipeline.state` in `site/src/data/corpus-facts.json`. Two consequences
a porter should know. `audit_layers.py` reports nothing here — it looks for inputs a layer reads
without declaring, and has no check for the converse, a committed output that no declaration claims
— so this orphan is silent rather than surfaced. And the site generates its layer pages from the
declarations, so there is no `/papers/<paper>/verification-check` page: the three ledger records,
dead `cmd` included, are rendered nowhere and reach a reader only inside the shipped
`corpus-facts.json`. Restoring the declaration is what makes the outputs legible again, and it
belongs with the code.
