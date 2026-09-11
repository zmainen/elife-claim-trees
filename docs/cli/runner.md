# The runner

`scripts/pipeline.py` is the pipeline. Five subcommands and one job: run a layer after
running whatever it still needs, and record that it happened.

It needs only PyYAML, holds no credentials and calls no model — so reading the graph, the
state matrix and the whole run history costs nothing and works offline.

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

`stale` and `unrecorded` are easy to confuse and mean different things. **Stale**: an input
changed since the run, so the output is probably wrong — rebuild it. **Unrecorded**: the
output exists but no run accounts for it, which is the normal state for anything produced
before the ledger existed. An unrecorded artifact may be perfectly good; `backfill` gives it
a record.

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
own output at the key its declaration names in `by_from`; otherwise it is the runner.

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

Approvals live in `runs/<paper>/approvals.jsonl` and apply to any layer. They are **empty for
every cell in this corpus** — nothing here has been checked by a person, and the site reports
that from this file rather than from a disclaimer.

**Looking for `--review-mode interactive`?** It is gone, and this is its replacement. The
difference is when it happens: that flag opened the draft in an editor *before* the claim
files were written, so what you approved was not the version that reached the corpus. You now
approve a version that exists and can be read.

**To correct a claim, edit the file.** That makes the layer `stale` against its own ledger
entry, which is accurate — the files are no longer what the layer produced. Re-run the layer
to rebuild from source, or leave the edit and let the state say so.

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
