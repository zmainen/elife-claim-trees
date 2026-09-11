# The runner

`scripts/pipeline.py` is the pipeline. Five subcommands, no dependencies beyond PyYAML, and
one job: run a layer after running whatever it still needs, and record that it happened.

Until recently none of this was documented anywhere. The layer model — the ledger, staleness,
propagation, approval — was assumed by every page under `/pipeline` and described in
`pipeline/layers.yaml`'s own header, and the thirty-three pages that used to be here mentioned
`ledger` zero times and `approval` zero times. This page is the gap being closed.

## `graph` — the declaration, as a shape

```bash
python3 scripts/pipeline.py graph
```

Prints every layer in dependency order with its kind, scope, what it needs and what it
produces. It reads `pipeline/layers.yaml` and nothing else, so it is the fastest way to check
that an edit to the declaration is well formed: an unknown dependency or a cycle is a hard
error here rather than a confusing state later.

## `state` — the paper × layer matrix

```bash
python3 scripts/pipeline.py state
python3 scripts/pipeline.py state --json           # what the site reads
python3 scripts/pipeline.py state --fail-on-stale  # as a CI gate
```

A cell is one layer asked of one paper, and it is in exactly one state:

| State | Meaning |
|:------|:--------|
| `current` | It ran, and every input still hashes to what that run recorded |
| `stale` | An input changed since the run, or an output is gone |
| `blocked` | Something it needs is stale or blocked, so its own result cannot be trusted |
| `absent` | It has never run, and produced nothing |
| `unrecorded` | Its outputs exist but no run records them — it ran before the ledger did |
| `n/a` | Declared impossible for this paper, with a reason |
| `open` | An undecided question; everything downstream of it is provisional |

The distinction between `stale` and `unrecorded` is the one that matters and the one that is
easiest to collapse. An input that *changed* since a run makes the output wrong. An input that
was never *recorded* is a different complaint: most of these papers were extracted before the
ledger existed, and their exports are perfectly consistent with the claim files they were built
from. Conflating the two would paint the whole corpus red and say nothing.

A jagged edge in the matrix is the normal condition. A blank means the layer has not been run
for that paper — not that it was run and found nothing.

## `run` — run a layer, and what it needs

```bash
python3 scripts/pipeline.py run <paper> <layer>
python3 scripts/pipeline.py run <paper> <layer> --dry-run   # print the commands, run nothing
python3 scripts/pipeline.py run <paper> <layer> --no-deps   # only the layer named
python3 scripts/pipeline.py run <paper> <layer> --note "…"  # the changelog line for the ledger
```

The command it runs comes from the layer's `command:` field, so there is one definition of how
a layer is produced and the copy-and-run text on the site cannot drift from what actually runs.

**It prunes at satisfied ancestors.** Asking for `coverage` on a paper whose claim tree is
already current runs `coverage` and nothing else — it does not walk through the tree into the
induction layers beneath it. Rebuilding a subtree nothing is waiting for would mean three
reader calls, a reconciliation and an Opus review to regenerate inputs to a file that is
already correct. Satisfied means `current` or `unrecorded`; `stale` and `blocked` are rebuilt.

Start `--dry-run`. It prints the chain in dependency order without running any of it, and on a
paper that has been through the pipeline it usually prints one line.

After each layer succeeds, `run` appends a record naming every input by path and content hash:

```json
{
  "layer": "prepare",
  "v": 1,
  "ran": "2026-09-11T11:00:39Z",
  "kind": "step",
  "note": "the paper the readers read, recorded",
  "by": "scripts/pipeline.py run",
  "cmd": "cd extract && python3 -m elife_extract.cli prepare --paper … --doi …",
  "in":  [{"path": "extract/elife_extract/prepare.py", "sha": "8ee35979be8f"}],
  "out": [{"path": "runs/…/prepared.json", "sha": "5512285faceb"}]
}
```

`by` names who answered. For a layer a model answers it is the model, read out of the layer's
own output at the key its declaration names in `by_from` — because from outside the command,
the runner can only record that it invoked something. Every entry used to say
`scripts/pipeline.py run` while the fact worth recording lived in a hand-kept manifest beside
the ledger meant to replace it.

## `approve` — record that a person read a version

```bash
python3 scripts/pipeline.py approve <paper> <layer> --by "your name" \
  --note "roles checked against figures 2-4"
python3 scripts/pipeline.py approve <paper> <layer> --by "…" --v 2   # a specific version
```

Approval is not a layer and not a gate. It is an operation on a version: a person reads what a
layer produced and approves *that output*, and the record names the version it was granted to.
When the layer runs again the approval does not follow — it was given to text that no longer
exists, and `state` reports it as no longer applying rather than carrying it forward.

It defaults to the version currently on the ledger, because approving a version that is not the
one on disk is almost always a mistake. `--v` names one explicitly, since reading v2 and
recording it after v3 has run is a coherent thing to have done.

Approvals live in `runs/<paper>/approvals.jsonl`, apply to any layer, and are **empty for every
cell in this corpus**. That is what "no human has checked this" is when it is a fact about the
data rather than a sentence in a preface.

There is no way to approve during a run, and that is deliberate. The CLI used to have a
`--review-mode interactive` gate that opened the draft claim table in an editor before anything
was written. It reviewed the wrong object: what a curator edited was a draft, while the version
that reached the corpus was whatever the write step then made of it, which nobody saw — and an
editor session that deleted three claims left no record that it had happened.

To correct a claim now, edit the file. That makes the layer stale against its own ledger entry,
which is true: the files are no longer what the layer produced. Staleness you can see beats an
edit nobody recorded.

## `backfill` — ledgers from what already exists

```bash
python3 scripts/pipeline.py backfill
python3 scripts/pipeline.py backfill --force   # rewrite ledgers that already exist
```

Writes run records for artifacts that predate the ledger, marked `backfilled: true` so they are
never mistaken for observed runs. Nine of these papers were extracted before any of this
existed; backfill is what makes their cells `current` rather than permanently `unrecorded`,
without claiming to know more about them than the files support.

## Using it as a library

`load()` returns the indexed declaration; `state()` returns the matrix. The site's
`src/lib/pipeline.ts` reads the JSON that `state --json` emits, which is why the pipeline pages
and this tool can never disagree about what has been run.
