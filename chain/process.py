"""The process: one YAML file declaring a DAG of steps over subject types.

A step is a question asked of a subject, answered by code, a model or a person. Its inputs are
other steps' latest artifacts and files; its instructions are a file; its answer is a claim set.
The process file, each step's own entry, and the instructions are all hashed into every run:
the process specification, the agent's instructions and the harness are artifacts like the rest.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

WORKERS = ("code", "model", "human")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:12]


@dataclass
class Step:
    id: str
    subject: str
    question: str = ""
    worker: str = "code"
    inputs: list[str] = field(default_factory=list)   # step ids, "subject:step", or file paths
    instructions: str | None = None                  # a markdown file, staged as INSTRUCTIONS.md
    command: str | None = None                       # code: reads $CHAIN_IN, writes $CHAIN_OUT
    emits: list[str] = field(default_factory=list)   # claim types this step may add
    judges: str | None = None                        # emits assessments about that step's claims
    verdicts: list[str] = field(default_factory=lambda: ["accept", "reject"])
    raw: dict = field(default_factory=dict, repr=False)

    @property
    def hash(self) -> str:
        return sha(json.dumps(self.raw, sort_keys=True).encode())


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

    def resolve(self, token: str, subject: str | None = None) -> tuple[str | None, str]:
        if ":" in token:
            sub, step = token.split(":", 1)
            return sub, step
        return subject, token

    def order(self) -> list[str]:
        seen, out, stack = set(), [], []

        def visit(sid):
            if sid in seen:
                return
            if sid in stack:
                raise ValueError(f"cycle at {sid!r}")
            stack.append(sid)
            for tok in self.steps[sid].inputs:
                if is_ref(tok):
                    visit(self.resolve(tok)[1])
            stack.pop()
            seen.add(sid)
            out.append(sid)

        for sid in self.steps:
            visit(sid)
        return out

    def subject_ids(self, stype: str) -> list[str]:
        spec = self.subjects.get(stype) or {}
        return [stype] if spec.get("singleton") else list(spec.get("ids") or [])

    def steps_for(self, stype: str) -> list[Step]:
        return [self.steps[s] for s in self.order() if self.steps[s].subject == stype]

    def as_judged(self) -> dict:
        """The declaration as a claim set a ruling can judge: one claim per step."""
        return {"claims": [{"id": s.id, "type": "step", "text": s.question or s.id,
                            "sha": s.hash, "worker": s.worker} for s in self.steps.values()]}


def load(path: str | Path) -> Process:
    path = Path(path)
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    subjects = doc.get("subjects") or {}
    steps: dict[str, Step] = {}
    for raw in doc.get("steps") or []:
        s = Step(**{k: v for k, v in raw.items() if k in Step.__dataclass_fields__}, raw=raw)
        if s.worker not in WORKERS:
            raise ValueError(f"{s.id}: worker must be one of {WORKERS}")
        if s.subject not in subjects:
            raise ValueError(f"{s.id}: unknown subject type {s.subject!r}")
        if s.judges:
            if s.worker == "code":
                raise ValueError(f"{s.id}: a judging step is answered by a model or a person")
            s.emits = s.emits or ["assessment", "decision"]
            if s.judges != "process" and s.judges not in s.inputs:
                s.inputs = [s.judges] + s.inputs          # what you judge, you read
        steps[s.id] = s
    p = Process(name=doc.get("name") or path.stem, path=path, subjects=subjects, steps=steps)
    for s in steps.values():
        for tok in s.inputs:
            if not is_ref(tok):
                continue
            sub, dep = p.resolve(tok)
            if dep not in steps:
                raise ValueError(f"{s.id}: input {dep!r} is not a step")
            if sub is None and steps[dep].subject != s.subject:
                raise ValueError(f"{s.id}: {dep} runs on {steps[dep].subject!r}; write "
                                 f"{steps[dep].subject}:{dep}")
    p.order()
    return p
