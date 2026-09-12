# Scientopia: the scientific ecosystem as one loop

**Status:** proposed, for discussion
**Companion:** `02-implementation-guide.md` (what to build, in what order, and how to review it)
**Core:** `chain/` (the running prototype) · `chain/examples/scientopia/board.html` (two teams, a funder, a journal, a library, one round)

## 1. The idea in one paragraph

Scientopia writes the whole cycle of science — asking, proposing, funding, doing, writing,
reviewing, publishing, reading, and asking again — as one loop of artifacts that players
produce. Every artifact is a set of claims. A paper is claims composed; a review is claims
about claims; a funding decision is a claim with a verdict. Research teams write papers,
funders choose what to support, journals decide what to publish, and every team reads what
the journals published to design its next study. The loop closes through the library. It runs
in the open, as a fishbowl anyone can watch, and what it produces is citable. The processes it
runs begin as imitations of the institutions we have, and are themselves artifacts that can be
revised. The first instantiation is fully agentic; every role can be played by a person
instead, or by a team of people and agents.

## 2. Why

The thesis behind HAAK is that intelligence scales through institutions rather than
individuals: the unit that learns is not a mind but a process with roles, records and rules
for revising itself. Science is the best-documented instance. Its institutions — the proposal,
the grant, the paper, peer review, the journal, the citation — are a technology for turning
many partial, fallible readings into a public, cumulative, correctable record.

Two things follow. First, if that technology is what makes science work, then agents should
be organised by it, not merely made to imitate its outputs: a swarm of agents that each writes
papers is not science, but agents that propose, fund, review, publish and cite under declared
processes might be. Second, the technology is itself an object of study. Once the whole cycle
is written down as processes that players run, every convention in it — three reviewers,
blind review, one funder per grant, publication as the unit of credit — becomes a declaration
that can be varied and its effect on the record measured. The point of building the system
is as much to test the institutions as to produce the science.

The second thesis is **claims and modularity**. The unit of scientific content is not the
paper; it is the claim — a proposition with its evidence, its provenance and its relations to
other claims. Papers, proposals and reviews are compositions over claims. If the record is
kept at the level of claims, then reuse, citation, replication and disagreement all become
operations on a graph rather than on prose, and the same graph serves a reader, a reviewer, a
funder and a team designing the next study. The claim-tree work on the eLife corpus showed
that papers can be decomposed to that level. Scientopia inverts it: claims come first, and
documents are made from them.

## 3. What it is

A **game** with three kinds of player, a library, and a referee.

- **Research teams** run projects: a question, hypotheses and predictions, a design, a
  proposal, a study, a paper.
- **Funders** issue calls, read every team's proposal, and decide what to fund.
- **Journals** receive every team's paper, review, decide, and publish.
- **The library** holds what was imported from outside and everything the journals publish.
  Every team and every funder reads it; every publication lands in it; that is the loop.
- **The referee** is the core (`chain/`): it stages each step's request, runs the steps that
  are mechanical, records every answer with what it was made from, and computes what is
  current. It decides nothing.

A **player** is a persona file plus whatever answers its requests. That can be a person, a
model, or a team of people and agents. Inside a player, members coordinate however they like —
a chat, a lab meeting, a subagent tree; the system neither sees nor constrains it. Between
players there is exactly one channel: the artifacts in the store. A team never messages a
funder; it writes a proposal, and the funder reads it. This is what makes the system
observable, reproducible and open: the whole interface to any player is a request directory,
so any player — a script, a model, a person, a stranger's bot — can join.

Every step is the same mechanism whether it imitates an institution ("review, then an
editorial decision") or judges a product ("which of these proposals deserves support"). The
core does not distinguish human from agent; the process says who plays a role (a player), and
the record says who answered.

The system has one **schema**: the claim set. Ten claim types, ten relations, all mapped to
existing standards. There is no second schema for reviews, decisions, proposals or grants;
each is a claim set of a particular shape. That is what makes the players interoperable and
the record queryable — and it is the thesis made concrete: claims are the atoms, everything
else is composition.

## 4. Inputs and outputs

**Input.** A pointer to a field. The planned seed is the International Brain Laboratory's
brain-wide map: its open dataset as the data teams may analyse, and its papers as the first
holdings of the library, imported as claim sets. (Reviewing the IBL infrastructure is a to-do;
the demo carries placeholders in the right shape.) Beyond that, the personas of the initial
players. No hypothesis is written by hand unless a persona says a person plays that role.

**Outputs.**

1. **The fishbowl.** The full state of the system as a web page anyone can read: the players
   and what each has done, the processes they run, every artifact, every open request, who
   answered what and from what. Nothing lives only in a codebase.
2. **Citable publications.** A journal's published record is an artifact with a stable id and
   a standards export (PROV, DocMaps, CiTO, MIRA, Discourse Graphs). It can be cited from
   inside the system and from outside it.
3. **Tools and processes.** The processes the players run, the instructions their agents
   read, and the tools they use are artifacts in the same store, versioned, public, and open to
   improvement by the players themselves.

## 5. Motivation: personas and the game's dynamics

A player has a **persona**, given by a file: who it is, what it values, how it reads and
writes. Personas are inputs to every request the player answers and are hashed like
everything else. But motivation is not scripted into personas. It comes from the game:
**reputation**, computed from the record — publications, citations, replications, funded
proposals, reviews delivered, and their alt-metric analogues — and visible to every player
on the board. A team that wants to be read writes what gets cited; a funder that wants
discoveries funds what gets replicated; a journal that wants to matter publishes what holds
up. Personas say who a player is; the rules say what pays.

The metrics are proxies, and honestly so. In the near term they are sub-proxies — counts on a
small closed record, before the ecosystem is joined to the real literature and its impact
measures. In the long run every one of them stands in for the thing all three kinds of player
actually want, which is discovery: knowledge that was not there before and survives being
checked. The first instantiations exist to define these rules and quality metrics, run under
them, and see what they select for. Changing a metric is a ruling on the process, recorded
like any other.

**Scarcity** is what makes funding a decision rather than a formality. In the first
instantiation the scarce resources are tokens and compute: a funder's award is a budget that
the study step spends, and a team that is not funded does not run. Money is a later proxy for
the same thing.

## 6. Principles

**Artifacts are the only channel between players.** Within a player, anything goes. Between
players, only the store. Teams of agents interact by reading and writing claim sets, never by
messaging.

**Every role can be played by a person or by an agent.** Reviewers, editors, funders,
investigators: the process names the role, the record names who filled it. The system can be
fully human, fully agentic, or any mixture, and the first instantiation is fully agentic.
Where a person does play, their answer is a claim set like any other, bound to the version
they read; the board says exactly where people looked. Human participation is neither assumed
nor assumed partial; it is a hook in every role.

**Standards from step zero.** Nothing in the schema is invented where a standard exists. The
mapping is a file, exported with every artifact, and honest about where nothing fits.

**Processes mimic institutions and are open to redesign.** The first processes copy the
institutions we know: a call, a grant, a peer-reviewed journal. Each is a declaration with a
version, and a ruling on a declaration is itself a step a player answers. Changing the number
of reviewers is a commit.

**Tools are shared and improvable.** The composer that turns claims into a paper, the checker
that validates a claim set, the adapter that answers a request with a model: all are files in
the store, all are inputs to the steps that use them, all can be improved by a team and
published for the others.

**Anyone can put a player in.** Because the interface is the request directory and the
contract, a participant registers a player with a persona and whatever answers its requests.
The system does not care what that is.

## 7. What it deliberately does not do yet

It does not implement the substance of research, review or funding judgement. The first
version runs the shape of the loop with stand-in players whose answers are fixtures, so that
the mechanism can be seen whole before any single judgement is made well. Real analysis of
the IBL data, real review, and real allocation of tokens come later, one role at a time, each
replacing a stub with a player under the same contract.

## 8. Roadmap

| Phase | Delivers | Visible as |
|:--|:--|:--|
| 0 (done) | The core; two teams, a funder, a journal and a library through one round with stubs; the loop closing through the library; the board. | `chain/examples/scientopia/board.html` |
| 1 | The game proper: reputation computed from the record; token budgets as the scarce resource; a second round in which teams read the first round's publications and cite them; a player registry so players are added without editing the process. Still stubs. | A board of players with reputations and two rounds |
| 2 | Real players: a model adapter that answers a request; the IBL papers imported as the library and the IBL dataset as the data; teams that analyse it. | Publications whose claims cite IBL |
| 3 | People in roles: a human editor, a human funder, a mixed team; the site publishes the board. | The fishbowl, public |
| 4 | Redesign: rulings on the processes; variants of review and funding run side by side and measured on the record. | Experiments about institutions |
| 5 | Open participation: a registered outside player. | — |

## 9. Open questions, for discussion

- **The reputation function.** Which counts, weighted how, over what window; and whether
  players see each other's reputations or only their own.
- **Budgets.** How a funder's token budget is set, whether it replenishes, and what a journal
  spends its budget on (review).
- **Rounds.** Whether the loop turns on a clock (every player asks again each round) or on
  events (a team asks again when the library changes).
- **Identity and signing.** When outside players join, a run record needs a signature.
- **Anonymity in review.** A process declaration; the first journal copies eLife's open model.
- **Where the library lives.** Git for text; Underlay or an object store for data.
- **Names.** `chain` is a placeholder for the core. The demo's players are trees and skies
  (Juniper, Larch, Aurora, Meridian) to avoid the AlphaFold echo of "alpha"; a naming scheme
  for real players is open.
