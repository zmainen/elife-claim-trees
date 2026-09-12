# Scientopia: implementation guide

**For:** agents implementing phases 1 and 2, and people reviewing their work
**Assumes:** `docs/scientopia/01-overview.md`, `chain/README.md`, `docs/design/2026-09-12-the-core.md`
**Rule for every change:** the board is regenerated, the tests pass, and a reviewer can see the
new behaviour on the board without reading code.

## 0. What exists

`chain/` is the core, the referee. Five nouns (player, step, claim, version, run), five verbs
(`ask`, `answer`, `status`, `board`, `export`), one rule (a step reads `$CHAIN_IN`, writes
`$CHAIN_OUT`), one schema (a claim set, `chain/claims.py`). A step with a `command` is run by
the referee; any other step waits for its player. The core does not know whether a player is
a person or an agent; the run records who answered.

`chain/examples/scientopia/` runs one round: two teams (Juniper, Larch) read the library and
propose; a funder (Aurora) selects one; the funded team runs its study and both compose papers;
a journal (Meridian) reviews, decides and publishes; the library grows and every team's reading
of it is out of date. Stand-in players answer from fixtures under `answers/<player>/`.

The store layout is fixed and every change must keep it:

```
store/<player>/<step>/request/     the open question (INSTRUCTIONS.md, PERSONA.md, in/, CONTRACT.json, QUESTION.md, skeleton.json)
store/<player>/<step>/v<N>/        claims.json · run.json · QUESTION.md · INSTRUCTIONS.md · PERSONA.md
store/<player>/ledger.jsonl
```

Three semantics are settled and must be preserved:

- **Set inputs.** `team:*:proposal` means every team's latest proposal. A set input goes stale
  when a member's version moves or the membership changes; it never blocks, and it does not
  order the graph. This is how the loop closes without a cycle and without a wait.
- **Reference discipline.** An answer may refer only to claims its request staged. A team
  that is to cite the library must have the library's holdings as inputs, not an index of them.
- **Judging.** `judges: <ref>` stages the judged artifacts and a skeleton with one assessment
  per item and one decision per artifact. A composition's items are the claims its sections
  reference, followed through staged artifacts. Partial readings must say so.

## 1. Players and the loop, as declared

```yaml
subjects:
  library: {singleton: true}
  team:    {ids: {juniper: {name: Juniper Lab, persona: personas/juniper.md}, …}}
  funder:  {ids: {aurora: {…}}}
  journal: {ids: {meridian: {…}}}
  process: {singleton: true}
```

| Player | Step | Answered by | Inputs | Answer |
|:--|:--|:--|:--|:--|
| library | `import` | referee | `seed/` | the seed corpus as a claim set (§ 5) |
| library | `catalogue` | referee | `import`, `journal:*:published` | an index of everything readable |
| team | `question` | the team | `library:import`, `journal:*:published`, persona | `question`, `scope`; `cites` into the library |
| team | `hypotheses` | the team | `question` | `hypothesis`, `prediction` |
| team | `design` | the team | `question`, `hypotheses` | `method`, `scope` |
| team | `proposal` | referee | the three above | composition |
| team | `award` | referee | `funder:*:select` | the decisions about this team's proposal |
| team | `study` | the team | `award`, `hypotheses`, `design` | `result`, `interpretation`; or one `scope` claim saying it was not funded |
| team | `paper` | referee | `question`, `hypotheses`, `design`, `study` | composition |
| funder | `call` | the funder | the library, persona | `scope` claims: what this call wants |
| funder | `select` | the funder | judges `team:*:proposal`; `call`, the teams' claims | `fund`/`decline` per item, a decision per proposal |
| journal | `submissions` | referee | `team:*:paper` | composition |
| journal | `review` | the journal | judges `submissions`; the papers' claims | `supported`/`weak`/`unsupported` per claim |
| journal | `decision` | the journal | judges `team:*:paper`; `review` | `accept`/`reject` per paper |
| journal | `published` | referee | `decision`, `review`, `submissions` | accepted articles with reviews and decisions, each with a `pub:` id |
| process | `scheme` | anyone | — | a ruling: one assessment per step |

"The team", "the funder", "the journal" are players: a person, a model, or a group; the
process does not say. Conditions are content, not structure: `study` reads `award` and its
instructions say what to do when declined.

## 2. Core extensions required for phase 1

Each is small, has a test, and is visible on the board. In this order.

### 2.1 Reputation from the record

A code step `library:reputation` reading `journal:*:published`, `journal:*:review`,
`funder:*:select` and `team:*:paper`, emitting one claim set: per player, counts of
publications, citations received (`cites` edges into its claims), funded proposals, reviews
delivered, decisions made. The board shows these on each player's card. The formula lives in
`tools/reputation.py`, is an input to the step, and changing it is a commit that stales the
step. Phase 1 uses counts; weights are a ruling.

Test: after one round, Juniper has 1 publication and Larch 0; after a second round in which
a team cites Juniper, Juniper's citations are 1.

### 2.2 Budgets

A funder's `select` decision carries `budget: <tokens>` per funded proposal; `award` composes
it; `study` may not spend more than it (the model adapter reports usage into `run.json`, and
`answer` refuses an answer whose usage exceeds the award). Unfunded means budget 0 and the
study's instructions already say what to do. The board shows budgets granted and spent.

Test: a study whose `usage.tokens` exceeds its award is refused with a plain message.

### 2.3 Rounds

The loop turns when players ask again. Phase 1 turns it on a clock: `chain round` asks every
team's `question` again (`--again`), then drives every player to its last step, in the same
order as the demo. A round is not a core concept — it is a script over `ask` — but it is the
unit the board narrates. Later, event-driven turning (a team asks again when its set inputs
go stale) replaces the clock.

Test: two rounds; a second-round question cites a first-round publication; reputation moves.

### 2.4 A player registry and `chain new`

Players are declared inline today. Move them to `players.yaml` beside `process.yaml`, same
shape (`type → id → {name, persona, …}`), read by `Process.subject_ids`, and add `chain new
<type> <id> --persona PATH` so a player is added without editing the process. A player's
entry may carry `answers: {step: <who>}` to record who plays which of its roles — a person's
name, an agent's id — for the board, not for enforcement.

### 2.5 Answers may say what they cost

`answer` accepts `--usage FILE` (or a top-level `usage` in the claim set) with tokens and
cost, copied into `run.json`. The board totals it per player and per round.

### 2.6 Empty answers and refusals

Already allowed by validation. The board must render `{"claims": [scope…]}` as "Not carried
out: …" rather than as an empty card.

## 3. Instructions and personas are the spec for players

Every non-mechanical step has an instructions file (`instructions/<step>.md`). Write it as the
whole task: what the step is for, what the inputs are and how to read them, what to emit and
what not to, the vocabulary, an example of a good and a bad answer, and the standard of
evidence. Improving one is a commit that stales every run that read the old one.

A persona (`personas/<player>.md`) says who the player is: its field, its taste, its
constraints, how it reads and writes, who its members are. It does not script motivation;
the reputation function does that. Two players that differ only in persona are the first
experiment the game can run; two journals that differ only in review process are the second.

## 4. Tools

Tools are files under `tools/`. A step lists the tools it uses as path inputs, so a tool
change stales its users. A team publishes a tool by adding a `method` claim to a paper whose
text names the tool and whose `cites` edge points at the tool's entry in the library's
`import` (phase 2: the library imports `tools/` as claims too). Improving a shared tool is a
pull request; the board shows which versions were made with which tool version.

## 5. The library and the IBL seed

`library:import` reads `seed/*.json`: claim sets in the store's own schema with a `source` and
a `citation`. The demo's seed is a placeholder in the shape of the IBL brain-wide map paper.
Phase 2 replaces it with claim sets extracted from the IBL papers (the claim-tree pipeline can
do this; its exports map onto the schema through the inverse of `standards.yaml`), and adds a
pointer to the IBL dataset that `study` steps may analyse under their budget. Reviewing the
IBL infrastructure (ONE, Alyx, the released datasets) is a to-do before phase 2.

Imported claims are ordinary nodes: a team's `question` may `cite` them, a study may
`replicate` one, and the reputation function counts citations into them like any other.

## 6. Publication ids and citation

`published` assigns each accepted paper an id `pub:<journal>:<n>` in its sections. A claim
anywhere may carry `cites` to a publication id or to a claim inside one. `export` emits the
publication as a schema.org ScholarlyArticle with a DocMaps of its review and decision.
Later a DOI is minted for a publication id; the id does not change.

## 7. The fishbowl

The board is the observable state and its top level is institutional: **players first**.
For each player: who it is (persona), its reputation, what it has done (proposals, awards,
papers, publications, reviews, decisions), and what it is doing now (open requests, steps in
progress). The loop is drawn as a loop — library → teams → funders → teams → journals →
library — with the players placed on it, not as a line of steps. Drill-down from a player
reaches its process and its artifacts, rendered as documents (a proposal, a paper) and
reports (a review, a decision), with every reference a link. The ledger is at the bottom, for
audit. The site publishes the board for the demo store at a stable URL.

## 8. Order of work, and effort

| # | Item | Effort | Done when |
|:--|:--|:--|:--|
| 1 | Reputation step and tool (§ 2.1) | 1 day | reputations on the board |
| 2 | Rounds script (§ 2.3); a second round in the demo | 1 day | a second-round citation of a first-round publication |
| 3 | Budgets and usage (§ 2.2, § 2.5) | 1 day | a refused over-budget study; totals on the board |
| 4 | Registry and `chain new` (§ 2.4) | ½ day | a third team added without editing the process |
| 5 | Board: players first, the loop, rounds, refusals (§ 7, § 2.6) | 1 day | a reader follows the game without help |
| 6 | Model adapter: `chain/agents/model.py` answering a request from its directory only, with usage | 1 day | a round on a real model |
| 7 | IBL seed: papers as claim sets, dataset pointer (§ 5) | 2 days | a team's question cites an IBL claim |
| 8 | Site publishes the board (§ 7) | ½ day | a URL |

Items 1–5 are phase 1; 6–8 are phase 2. Each item is one pull request with the regenerated
demo store and board committed.

## 9. Review checklist

A reviewer of any pull request against this guide checks, on the board and in the store, not
in the code:

- The board's top level is players, and every fact on it is a sentence that links to the artifact it came from.
- Every version directory stands alone: `claims.json`, `run.json`, the question, the instructions, the persona.
- No step reads anything not staged in its request (grep the command for paths; run it with `CHAIN_IN` pointed elsewhere).
- Staleness propagates: change an instruction, a persona, a tool or a member set, and the right cells go stale and nothing else does; nothing is blocked across a set input.
- A player's answer is refused if the judged version moved; a partial reading is accepted and shown as partial.
- `export` of a new artifact validates as JSON-LD and its terms are in `standards.yaml`.
- The tests run the whole demo, and the demo store in git matches a fresh run except for timestamps.
