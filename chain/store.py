"""The store: one directory per subject, one directory per artifact version, one ledger.

    store/<subject>/ledger.jsonl                 every run, append-only
    store/<subject>/<step>/v<N>/                 an artifact: the answer, plus run.json
    store/<subject>/<step>/request/              the open request, if one is pending

An artifact directory is complete on its own: `run.json` names every input by path and hash,
the process and step declaration hashes, who answered and when. Hand it to someone without
the repository and they can see what it is and what it was made from.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

VERSION = re.compile(r"^v(\d+)$")


def sha_path(p: Path) -> str | None:
    """Content hash of a file, or of a directory as the sorted concatenation of its files."""
    if not p.exists():
        return None
    h = hashlib.sha256()
    if p.is_dir():
        for f in sorted(x for x in p.rglob("*") if x.is_file()):
            h.update(str(f.relative_to(p)).encode())
            h.update(f.read_bytes())
    else:
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


def read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(p: Path, obj) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                 encoding="utf-8")
    return p


class Store:
    def __init__(self, root: Path):
        self.root = Path(root)

    def subject(self, sid: str) -> Path:
        return self.root / sid

    def step_dir(self, sid: str, step: str) -> Path:
        return self.subject(sid) / step

    def request_dir(self, sid: str, step: str) -> Path:
        return self.step_dir(sid, step) / "request"

    def versions(self, sid: str, step: str) -> list[int]:
        d = self.step_dir(sid, step)
        if not d.is_dir():
            return []
        return sorted(int(m.group(1)) for x in d.iterdir()
                      if x.is_dir() and (m := VERSION.match(x.name)))

    def latest(self, sid: str, step: str) -> int | None:
        vs = self.versions(sid, step)
        return vs[-1] if vs else None

    def version_dir(self, sid: str, step: str, v: int) -> Path:
        return self.step_dir(sid, step) / f"v{v}"

    def run_record(self, sid: str, step: str, v: int) -> dict | None:
        p = self.version_dir(sid, step, v) / "run.json"
        return read_json(p) if p.is_file() else None

    # ── ledger ──────────────────────────────────────────────────────────

    def ledger_path(self, sid: str) -> Path:
        return self.subject(sid) / "ledger.jsonl"

    def ledger(self, sid: str) -> list[dict]:
        p = self.ledger_path(sid)
        if not p.is_file():
            return []
        return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]

    def append(self, sid: str, record: dict) -> None:
        p = self.ledger_path(sid)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")

    def subjects(self) -> list[str]:
        return sorted(x.name for x in self.root.iterdir() if x.is_dir()) if self.root.is_dir() else []

    def wipe_request(self, sid: str, step: str) -> None:
        d = self.request_dir(sid, step)
        if d.exists():
            shutil.rmtree(d)
