# Scientopia: implementation guide

**For:** agents implementing phase 1 and 2, and people reviewing their work
**Assumes:** `docs/scientopia/01-overview.md`, `chain/README.md`, `docs/design/2026-09-12-the-core.md`
**Rule for every change:** the board is regenerated, the tests pass, and a reviewer can see the
new behaviour on the board without reading code.

## 0. What exists

`chain/` is the core. Five nouns (subject, step, claim, version, run), five verbs (`ask`,
`answer`, `status`, `board`, `export`), one rule (a step reads `$CHAIN_IN`, writes
`$CHAIN_OUT`), one schema (a claim set, `chain/claims.py`). `chain/examples/scientopia/` runs one
project through eleven steps plus a ruling on the process, with stub agents and a stand-in
person, and produces `board.html`. Read those before anything below.

The store layout is fixed and every change must keep it:

```
store/<subject>/<step>/request/     the open question (INSTRUCTIONS.md, in/, CONTRACT.json, QUESTION.md, skeleton.json)
store/<subject>/<step>/v<N>/        claims.json · run.json · QUESTION.md · INSTRUCTIONS.md
store/<subject>/ledger.jsonl
```

## 1. The game as subjects and steps

Phase 1 turns one project into a game. Four subject types, one process file.

```yaml
name: scientopia
subjects:
  library: {singleton: true}
  project: {registry: subjects.yaml}       # created as teams start projects; see § 2
  funder:  {registry: subjects.yaml}
  journal: {registry: subjects.yaml}
  process: {singleton: true}
```

Steps, in the order the cycle turns. `(c)` code, `(m)` model, `(h)` human. Worker is the
default; a charter may reassign a role to a person (§ 2).

| Subject | Step | Worker | Inputs | Answer |
|:--|:--|:--|:--|:--|
| library | `import` | c | a corpus export (§ 5) | claims imported from outside, one artifact per source paper |
| library | `catalogue` | c | `journal:*:published`, `import` | a composition: every published record and every imported paper, with ids |
| project | `question` | m | `library:catalogue`, charter | `question`, `scope` claims; `cites` edges into the library |
| project | `hypotheses` | m | `question`, charter | `hypothesis`, `prediction` |
| project | `design` | m | `question`, `hypotheses` | `method`, `scope` |
| project | `proposal` | c | the three above | composition |
| funder | `call` | m | charter, `library:catalogue` | `scope` claims: what this call wants |
| funder | `select` | m or h | `project:*:proposal`, `call` | one `decision` per proposal (`fund` / `decline`) with `assessment`s per item |
| project | `award` | c | `funder:*:select` | composition of the decisions about this project's proposal |
| project | `study` | m | `award`, `hypotheses`, `design` | `result`, `interpretation`; empty with a `scope` claim if not funded |
| project | `paper` | c | `question`, `hypotheses`, `design`, `study` | composition |
| journal | `submissions` | c | `project:*:paper` | composition of papers not yet decided by this journal |
| journal | `review` | m | `submissions`, the papers' inputs | `assessment` per claim of every submitted paper |
| journal | `decision` | h or m | `review` | `decision` per paper (`accept` / `reject`) |
| journal | `published` | c | `submissions`, `review`, `decision` | composition of accepted papers with their reviews and decisions; each gets a publication id (§ 6) |
| process | `scheme` | h | — | a ruling: one assessment per step |

The cycle turns because `library:catalogue` reads `journal:*:published`, and a new project's
`question` reads `library:catalogue`. There is no loop in the graph: a later project is a new
subject, and the catalogue is stale — and re-asked — whenever a journal publishes.

Conditions are content, not structure. `study` does not depend on being funded in the graph;
it reads `award`, and its instructions say what to do when the award declines. A reviewer can
see the refusal as a claim rather than as a missing artifact.

## 2. Core extensions required

Each is small, has a test, and is visible on the board. Implement in this order.

### 2.1 Many-subject inputs: `type:*:step`

An input token `journal:*:published` means: the latest version of `published` for every
subject of type `journal` that has one. Semantics:

- `run.inputs()` expands it to one `{"kind": "step", "ref": "journal:j1:published", "v": 3}`
  entry per subject, plus one `{"kind": "set", "ref": "journal:*:published", "members": ["j1", "j2"]}`
  entry recording the membership. Staged under `in/journal/<id>/published/`.
- Staleness: a member's version moved, or the member set changed (a new journal appeared).
- `status` for a step with a set input reports `blocked_by` per member that is not current.
- A set with no members is allowed (an empty `in/journal/`), so the first round runs.

Test: two journals, one publishes, `catalogue` goes stale; a third journal is registered,
`catalogue` goes stale again with `moved: ["journal:*:published (members)"]`.

### 2.2 A subject registry

`subjects.yaml` beside `process.yaml`:

```yaml
project:
  alpha: {team: mainen, charter: charters/mainen.md, started: 2026-09-12}
  beta:  {team: behrens, charter: charters/behrens.md, started: 2026-09-13}
funder:
  f1: {charter: charters/f1.md}
journal:
  j1: {charter: charters/j1.md, workers: {decision: human}}
```

`Process.subject_ids(type)` reads it when the type declares `registry:`. A new verb `chain new
<type> <id> --charter PATH [--team NAME]` appends an entry. A subject's `workers:` map
overrides a step's default worker for that subject only, which is how one journal has a human
editor and another does not.

Test: `chain new project beta --charter charters/behrens.md` makes `status` show a second row
with every step `absent`.

### 2.3 Charters

A charter is a markdown file: goals, motivations, constraints, in prose an agent can act on. It
is staged into every request of that subject's steps as `CHARTER.md` and hashed like the
instructions, so editing a charter makes that subject's runs stale. The board shows each
player's charter on its card. Team membership (which agents may answer which subject's
requests) is a line in the charter for now; enforcement is § 2.6.

Test: edit `charters/mainen.md`; every `alpha` cell is stale with `moved: ["charters/mainen.md"]`.

### 2.4 An agent adapter

`chain/agents/model.py <request_dir> <answer.json> [--model ID]`: reads `INSTRUCTIONS.md`,
`CHARTER.md` if present, `CONTRACT.json`, `skeleton.json` if present, and every file under
`in/`; composes one prompt; calls a model with a JSON schema derived from the contract
(structured output); writes `claims.json`. It must not read anything outside the request
directory. It records the model id, token usage and cost into the answer's top-level
`usage`, which `answer` copies into `run.json`.

Then `chain answer <subject> <step> --agent "python3 -m chain.agents.model"` runs the adapter on
the open request and records its output, and `chain ask … --agent CMD` uses the same adapter
for every model step it reaches, so a whole cycle runs with one command. The stub stays as the
zero-cost adapter and the tests keep using it.

Test: with the stub as `--agent`, `chain ask alpha publish --agent "python3 -m chain.agents.stub-cli …"` completes the cycle with no manual answers.

### 2.5 Empty answers and refusals

A model step may answer `{"claims": []}` plus a `scope` claim saying why (not funded; nothing to
review). Validation already allows it; the board must render it as "Nothing produced: …" with
the reason, not as an empty card.

### 2.6 Who may answer

A step may declare `agent: <name>` and a subject may declare `team:`. `answer --by` must name a
party the charter lists for that subject, or `--by` must be a person. Start with a check that
warns; make it refuse once outside agents play. Signing of `run.json` (Sigstore-style keyless)
is phase 5 and is not needed to run the game.

## 3. Instructions and charters are the spec for agents

Every model or human step has an instructions file (`instructions/<step>.md`). Write them as
the whole task: what the step is for, what the inputs are and how to read them, what to emit
and what not to, the vocabulary, examples of a good and a bad answer, and the standard of
evidence. They are versioned inputs; improving one is a commit that stales every run that
read the old one, which is what should happen.

Charters carry motivation and goals. A team's charter says what it wants (e.g. "publish
results that replicate"; "maximise citations"; "prefer negative results"), what it will not do,
and how it reads the library. A funder's says what it funds. A journal's says what it publishes
and how it reviews (how many reviewers, open or blind, what verdict vocabulary). Two players
that differ only in charter are the first experiment the game can run.

## 4. Tools

Tools are files under `tools/` (the composer, the claim-set checker, the model adapter, an
analysis script). A step lists the tools it uses as path inputs, so a tool change stales its
users. A team publishes a tool by adding a `method` claim to a paper whose text names the tool
and whose `cites` edge points at the tool's path and hash in the library's `import` of tools
(phase 2: the library imports `tools/` as claims too). Improving a shared tool is a pull
request; the board shows which versions were made with which tool version.

## 5. The library and the import

`library:import` is a code step that reads a directory of corpus exports and writes one
artifact per source paper, as claim sets: `id` from the source slug, `type` mapped from the
source's role vocabulary, edges mapped from its relations, `by: import:<source>`, and a `cites`
edge to the source DOI. The first source is `exports/*.mira-extended.jsonld` from the claim-tree
corpus (10 papers, 254 claims, 919 relations). The mapping is the inverse of
`chain/standards.yaml` and lives beside it.

Imported claims are ordinary nodes: a team's `question` step may `cite` them, a study may
`replicate` one. This is how the claim-tree work rejoins the system, and it needs no change to
the legacy pipeline.

## 6. Publication ids and citation

A `published` composition assigns each accepted paper an id `pub:<journal>:<year>:<n>` stored
in the composition's sections (`{"title": "...", "id": "pub:j1:2026:1", "claims": [...]}`).
A claim anywhere may carry `cites` to a publication id or to a claim id inside one. `export`
emits the publication as a schema.org ScholarlyArticle with a DocMaps of its review and
decision steps. Later a DOI is minted for a publication id; the id does not change.

## 7. The fishbowl

The board (`chain board`) is the observable state. Phase 1 requires it to show: every player
with its charter; the cycle per project; funders' calls and decisions across projects;
journals' submissions, reviews, decisions and publications; the library's catalogue; open
requests; the ledger. The site (`site/`) publishes the board for the demo store at a stable
URL, rebuilt on every commit to `main`. Nothing about the game is knowable only from code.

## 8. Order of work, and effort

| # | Item | Effort | Done when |
|:--|:--|:--|:--|
| 1 | Many-subject inputs (§ 2.1) with tests | 1 day | `catalogue` goes stale when any journal publishes |
| 2 | Registry, `chain new`, charters (§ 2.2–2.3) | 1 day | two projects, one funder, one journal on the board with charters |
| 3 | The game process file and instructions for every step (§ 1, § 3) | 1 day | one full round with stubs: two proposals, one funded, one paper published |
| 4 | A second round: a new project reads the catalogue and cites a publication (§ 6) | ½ day | the board shows a citation from round 2 to round 1 |
| 5 | Board: players, rounds, citations, refusals (§ 7, § 2.5) | 1 day | a reader follows the story without help |
| 6 | Model adapter and `--agent` (§ 2.4) | 1 day | a cycle runs on a real model with usage recorded |
| 7 | Library import from the claim-tree corpus (§ 5) | 1 day | a team's question cites a corpus claim |
| 8 | Site publishes the board (§ 7) | ½ day | a URL |

Items 1–5 are phase 1; 6–8 are phase 2. Each item is one pull request with the regenerated
demo store and board committed.

## 9. Review checklist

A reviewer of any pull request against this guide checks, on the board and in the store, not
in the code:

- Every new fact on the board is a plain sentence, and clicking it reaches the artifact it came from.
- Every version directory stands alone: `claims.json`, `run.json`, the question, the instructions, the charter if any.
- No step reads anything not staged in its request (grep the command for paths; run it with `CHAIN_IN` pointed elsewhere).
- Staleness propagates: change an instruction, a charter, a tool or a member set, and the right cells go stale and nothing else does.
- A person's answer is refused if the judged version moved; a partial reading is accepted and shown as partial.
- `export` of a new artifact validates as JSON-LD and its terms are in `standards.yaml`.
- The tests run the whole demo, and the demo store in git matches a fresh run except for timestamps.
