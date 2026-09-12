"""chain — a versioned processing graph with people in it, where every artifact is a claim set.

Five nouns:  subject · step · claim · version · run
Five verbs:  ask · answer · status · board · export

A step is a question asked of a subject. Asking stages a request: one directory holding the
step's instructions, copies of everything it may read, and a contract for what may come back.
Whoever answers — a script, a model, a person — reads that directory and nothing else. The
answer is a claim set, validated and written as the next version with a run record naming
what it was made from. A person's verdict is a claim set too: assessments about claims.

Nothing here calls a model or knows what a paper is.
"""

from .process import Process, Step, load
from .store import Store
from .status import status, STATES
from .run import ask, answer, stage

__all__ = ["Process", "Step", "load", "Store", "status", "STATES", "ask", "answer", "stage"]
