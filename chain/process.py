"""The process: one YAML file declaring a DAG of steps over player types.

A step is a question asked of a player. Either the referee answers it by running a command,
or a player answers it — a person, a model, a team of both; the process does not say which,
the run records who did. A step's inputs are other steps' latest artifacts, every player of a
type's latest artifact (`team:*:proposal`), or files. Its instructions are a file, and the
player's persona is a file; both are hashed into every run like the process itself.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:12]


@dataclass
class Step:
    id: str
    subject: str                                     # player type this step runs against
    question: str = ""
    inputs: list[str] = field(default_factory=list)  # step | subject:step | type:*:step | path
    instructions: str | None = None
    command: str | None = None                       # present: the referee runs it, no player waits
    emits: list[str] = field(default_factory=list)   # claim types this step may add
    judges: str | None = None                        # step, type:*:step, or "process"
    verdicts: list[str] = field(default_factory=lambda: ["accept", "reject"])
    raw: dict = field(default_factory=dict, repr=False)

    @property
    def hash(self) -> str:
        return sha(json.dumps(self.raw, sort_keys=True).encode())

    @property
    def automatic(self) -> bool:
        return self.command is not None


def is_ref(token: str) -> bool:
    """A step reference has no slash and no dot; anything else is a path."""
    return "/" not in token and "." not in token


@dataclass
class Process:
    name: str
    path: Path
    subjects: dict[str, dict]
    steps: dict[str, Step]

    @property
    def hash(self) -> str:
        return sha(self.path.read_bytes())

    # ── players ─────────────────────────────────────────────────────────
    def subject_ids(self, stype: str) -> list[str]:
        spec = self.subjects.get(stype) or {}
        if spec.get("singleton"):
            return [stype]
        ids = spec.get("ids") or []
        return list(ids) if isinstance(ids, (list, dict)) else []

    def type_of(self, sid: str) -> str | None:
        return next((t for t in self.subjects if sid in self.subject_ids(t)), None)

    def meta(self, sid: str) -> dict:
        """A player's declared facts: persona file, display name, whatever the file says."""
        t = self.type_of(sid)
        ids = (self.subjects.get(t) or {}).get("ids")
        return dict(ids[sid]) if isinstance(ids, dict) and isinstance(ids.get(sid), dict) else {}

    # ── references ──────────────────────────────────────────────────────
    def step_of(self, token: str) -> str:
        return token.rsplit(":", 1)[1] if ":" in token else token

    def expand(self, token: str, subject: str | None) -> list[tuple[str, str]]:
        """A reference → the (player, step) pairs it names right now."""
        parts = token.split(":")
        if len(parts) == 1:
            return [(subject, token)]
        if len(parts) == 3 and parts[1] == "*":
            return [(sid, parts[2]) for sid in self.subject_ids(parts[0])]
        return [(parts[0], parts[1])]

    def is_set(self, token: str) -> bool:
        return token.count(":") == 2 and token.split(":")[1] == "*"

    # ── the graph ───────────────────────────────────────────────────────
    def order(self) -> list[str]:
        seen, out, stack = set(), [], []

        def visit(sid):
            if sid in seen:
                return
            if sid in stack:
                raise ValueError(f"cycle at {sid!r}")
            stack.append(sid)
            for tok in self.steps[sid].inputs:
                # A set input (`journal:*:published`) reads whatever exists and orders
                # nothing: it is how the loop closes without a cycle in the graph.
                if is_ref(tok) and not self.is_set(tok):
                    visit(self.step_of(tok))
            stack.pop()
            seen.add(sid)
            out.append(sid)

        for sid in self.steps:
            visit(sid)
        return out

    def steps_for(self, stype: str) -> list[Step]:
        return [self.steps[s] for s in self.order() if self.steps[s].subject == stype]

    def as_judged(self) -> dict:
        """The declaration as a claim set a ruling can judge: one claim per step."""
        return {"claims": [{"id": s.id, "type": "step", "text": s.question or s.id,
                            "sha": s.hash} for s in self.steps.values()]}


def load(path: str | Path) -> Process:
    path = Path(path)
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    subjects = doc.get("subjects") or {}
    steps: dict[str, Step] = {}
    for raw in doc.get("steps") or []:
        s = Step(**{k: v for k, v in raw.items() if k in Step.__dataclass_fields__}, raw=raw)
        if s.subject not in subjects:
            raise ValueError(f"{s.id}: unknown player type {s.subject!r}")
        if s.judges:
            if s.command:
                raise ValueError(f"{s.id}: a judging step is answered by a player, not a command")
            s.emits = s.emits or ["assessment", "decision"]
            if s.judges != "process" and s.judges not in s.inputs:
                s.inputs = [s.judges] + s.inputs          # what you judge, you read
        steps[s.id] = s
    p = Process(name=doc.get("name") or path.stem, path=path, subjects=subjects, steps=steps)
    for s in steps.values():
        for tok in s.inputs:
            if not is_ref(tok):
                continue
            dep = p.step_of(tok)
            if dep not in steps:
                raise ValueError(f"{s.id}: input {dep!r} is not a step")
            if ":" not in tok and steps[dep].subject != s.subject:
                raise ValueError(f"{s.id}: {dep} runs on {steps[dep].subject!r}; write "
                                 f"{steps[dep].subject}:<id>:{dep} or {steps[dep].subject}:*:{dep}")
            if p.is_set(tok) and tok.split(":")[0] not in subjects:
                raise ValueError(f"{s.id}: {tok} names no player type")
    p.order()
    return p
