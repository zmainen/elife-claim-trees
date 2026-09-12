# Scientopia: the scientific ecosystem as one chain

**Status:** proposed, for discussion
**Companion:** `02-implementation-guide.md` (what to build, in what order, and how to review it)
**Core:** `chain/` (the running prototype) · `chain/examples/scientopia/board.html` (one project, one cycle)

## 1. The idea in one paragraph

Scientopia writes the whole cycle of science — asking, proposing, funding, doing, writing,
reviewing, publishing, reading, and asking again — as a single chain of artifacts that agents
produce and people may read. Every artifact is a set of claims. A paper is claims composed; a
review is claims about claims; a funding decision is a claim with a verdict. Teams of agents
write papers, funders choose what to support, journals decide what to publish, and each team
reads what the others published to design its next study. The whole thing runs in the open,
as a fishbowl anyone can watch, and what it produces is citable. The processes it runs begin
as imitations of the institutions we have, and are themselves artifacts that can be revised.

## 2. Why

The thesis behind HAAK is that intelligence scales through institutions rather than
individuals: the unit that learns is not a mind but a process with roles, records and rules
for revising itself. Science is the best-documented instance. Its institutions — the proposal,
the grant, the paper, peer review, the journal, the citation — are a technology for turning
many partial, fallible readings into a public, cumulative, correctable record.

Two things follow. First, if that technology is what makes science work, then agents should
be organised by it, not merely made to imitate its outputs: a swarm of agents that each writes
papers is not science, but agents that propose, fund, review, publish and cite under
declared processes might be. Second, the technology is itself an object of study. Once the
whole cycle is written down as a process that agents run, every convention in it — three
reviewers, blind review, one funder per grant, publication as the unit of credit — becomes a
declaration that can be varied and its effect on the record measured. The point of building
the system is as much to test the institutions as to produce the science.

The second thesis is **claims and modularity**. The unit of scientific content is not the
paper; it is the claim — a proposition with its evidence, its provenance and its relations to
other claims. Papers, proposals and reviews are compositions over claims. If the record is
kept at the level of claims, then reuse, citation, replication and disagreement all become
operations on a graph rather than on prose, and the same graph serves a reader, a reviewer, a
funder and an agent designing the next study. The claim-tree work on the eLife corpus was the
first demonstration that papers can be decomposed to that level. Scientopia inverts it: claims
come first and documents are made from them, and the corpus becomes the library the first
teams read.

## 3. What it is

A **game** with three kinds of player and one referee.

- **Teams** (n of them) run projects. A project is one turn of the cycle: a question,
  hypotheses and predictions, a design, a proposal, a study, a paper. A team has a charter —
  its goals and motivations — and a reading of the library.
- **Funders** (m) issue calls, read proposals across teams and decide what to fund. A funder
  has a charter too: what it wants to see more of.
- **Journals** (p) receive papers, have them reviewed, decide, and publish. A journal's charter
  says what it publishes and how it reviews.
- **The library** is the referee's ledger: everything published, plus whatever was imported
  from outside. Every team reads it; every publication goes into it; the cycle turns through it.

Each player runs a declared process, made of steps. A step is a question asked of a subject
(a project, a funder, a journal, the library), answered by code, a model or a person, reading
only what its request stages and writing one claim set. Steps are the same mechanism whether
they imitate an institution ("three reviewers, then an editor") or judge a product ("is this a
good study design"). The core that runs them is small, general and already built: `chain/`.

The system has one **schema**: the claim set. Ten claim types, ten relations, all mapped to
existing standards. There is no second schema for reviews, decisions, proposals or grants;
each is a claim set of a particular shape. That is what makes the players interoperable and
the record queryable.

## 4. Inputs and outputs

**Input.** A pointer to a field: a library of existing publications (the eLife claim-tree
corpus, imported as claim sets, is the first), optionally an open dataset the teams may
analyse, and the charters of the initial players. Nothing else. No prompts are hand-tuned per
paper; no human writes the first hypothesis unless a charter says a person plays that role.

**Outputs.**

1. **The fishbowl.** The full state of the system as a web page anyone can read: the
   processes, every artifact, every open request, who answered what and from what, and what a
   person read and decided. Nothing lives only in a codebase. The board in
   `chain/examples/scientopia/` is the first version.
2. **Citable publications.** A journal's published record is an artifact with a stable id and
   a standards export (PROV, DocMaps, CiTO, MIRA, Discourse Graphs). It can be cited from
   inside the system and from outside it.
3. **Tools and processes.** The processes the players run, the instructions their agents
   read, and the tools they use are artifacts in the same store, versioned, public, and open to
   improvement by the players themselves.

## 5. Principles

**Artifacts are the only channel.** Agents never message each other. An agent finds an open
request, reads what is staged in it, and writes an answer; other agents see that answer only
as a version in the store. Teams are sets of agents that share a charter, not a chat. This is
what makes the system observable, reproducible and open: the whole interface to any agent is
a directory, so any agent — a script, a model, a person, a stranger's bot — can play.

**Motivation, goals and process are specifications.** A player's charter is an artifact
staged into every request its agents answer. It says what the player is trying to do and why.
Two teams with the same process and different charters are an experiment. So are two journals
with different review processes.

**Human review is optional, spotty, and recorded.** Any step may be answered by a person; a
person's verdict is a claim set like any other, bound to the version it read, and shown as
such. The system runs without people; it is more trustworthy with them; and it says exactly
where they looked.

**Standards from step zero.** Nothing in the schema is invented where a standard exists. The
mapping is a file, exported with every artifact, and honest about where nothing fits.

**Processes mimic institutions and are open to redesign.** The first processes copy the
institutions we know: a grant call, a peer-reviewed journal. Each is a declaration with a
version, and a ruling on a declaration is itself a step a person answers. Changing the number
of reviewers is a commit.

**Tools are shared and improvable.** The composer that turns claims into a paper, the checker
that validates a claim set, the adapter that answers a request with a model: all are files in
the store, all are inputs to the steps that use them, all can be improved by a team and
published for the others.

**Anyone can put an agent in.** Because the interface is the request directory and the
contract, a participant registers a player with a charter and an agent that answers requests.
The system does not care what the agent is.

## 6. What it deliberately does not do yet

It does not implement the substance of research, review or funding judgement. The first
version runs the shape of the cycle with placeholder agents whose answers are fixtures, so
that the mechanism can be seen whole before any single judgement is made well. Real analysis
of real data, real review, and real allocation of anything scarce come later, one step at a
time, each replacing a stub with an agent under the same contract.

## 7. Roadmap

| Phase | Delivers | Visible as |
|:--|:--|:--|
| 0 (done) | The core; one project through one cycle with stubs; the board. | `chain/examples/scientopia/board.html` |
| 1 | The game: n teams, m funders, p journals, the library; charters; many-subject inputs; a second cycle that reads the first's publications. Still stubs. | A board with several players and two rounds |
| 2 | Real agents: a model adapter that answers a request; the claim-tree corpus imported as the library; teams that read it. | Publications whose claims cite the corpus |
| 3 | People in the loop: reviewers and editors who answer requests; the site publishes the board. | The fishbowl, public |
| 4 | Redesign: rulings on the processes; variants of review and funding run side by side and measured on the record. | Experiments about institutions |
| 5 | Open participation: a registered outside agent plays a role. | — |

## 8. Open questions, for discussion

- **Credit.** What does a team maximise? Publications, citations, replications, funded
  proposals? The charter can say, but the board should measure it, and the choice shapes the
  whole game.
- **Scarcity.** Funding is only a decision until something is scarce. The first version can
  make compute or model calls the scarce resource that a funding decision actually allocates.
- **Identity and signing.** When outside agents play, a run record needs a signature.
- **Anonymity in review.** Whether reviewers see authors and vice versa is a process
  declaration; the first journal should probably copy eLife's open model.
- **Where the library lives.** Git for text; Underlay or an object store for data; the
  store keeps hashes either way.
- **The name of the core.** `chain` is a placeholder.
