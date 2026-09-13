# The verification check sits beside the warrant, never over it

**Status:** proposed
**Issue:** [#126](https://github.com/zmainen/elife-claim-trees/issues/126)
**Frames:** [#36](https://github.com/zmainen/elife-claim-trees/issues/36) · [#20](https://github.com/zmainen/elife-claim-trees/issues/20)
**Depends on:** the `warrant` layer, the `verification` layer, `docs/claim-format.md`, `extract/elife_extract/verification_check.py`

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
