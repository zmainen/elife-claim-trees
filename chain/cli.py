"""python3 -m chain <verb>

    ask     <subject> <step> [--again]         stage the question (and answer it, if code) — walks unmet inputs first
    answer  <subject> <step> <path> --by WHO   validate a claims.json (or a directory holding one) and record it
    status  [subject] [--json]                 subject × step, with judgements and the scheme
    board   [--out board.html]                 one page showing the process, every artifact and every request
    export  <subject> <step> [--v N]           the version as JSON-LD with its standards mapping
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from . import process as P
from .board import board
from .export import export
from .run import answer, ask
from .status import status
from .store import Store

GLYPH = {"current": "✓", "stale": "~", "absent": "·", "blocked": "!", "pending": "?"}


def _ctx(a):
    root = Path(a.root).resolve()
    return P.load(root / a.process), Store(root / a.store), root


def cmd_ask(a):
    proc, store, root = _ctx(a)
    done = ask(proc, store, root, a.subject, a.step, by=a.by, note=a.note or "", again=a.again)
    for step, outcome, where in done:
        print(f"  {step:18} {outcome:9} {where}")
    if not done:
        print("  nothing to ask: it is current (use --again for a fresh version)")


def cmd_answer(a):
    proc, store, root = _ctx(a)
    vd = answer(proc, store, root, a.subject, a.step, Path(a.path), by=a.by, note=a.note or "")
    print(f"  recorded {vd.relative_to(root)}/")


def cmd_status(a):
    proc, store, root = _ctx(a)
    st = status(proc, store, root, [a.subject] if a.subject else None)
    if a.json:
        print(json.dumps(st, indent=2, sort_keys=True))
        return
    for sid, cells in st.items():
        print(sid)
        for step_id, c in cells.items():
            line = f"  {GLYPH[c['state']]} {step_id:18} {c['state']:8} {c['worker']:6}"
            if c.get("v"):
                line += f" v{c['v']} · {c.get('by')}"
            for d in c.get("assessed") or []:
                line += f"   · {d['step']}: {d['verdict']} by {d['by']} ({d['considered']}/{d['of']})" + \
                        ("" if d["applies"] else " [an earlier version]")
            line += f"   · scheme: {c['scheme']}"
            if c.get("moved"):
                line += f"   ← moved: {', '.join(c['moved'][:3])}"
            if c.get("blocked_by"):
                line += f"   ← {', '.join(c['blocked_by'])}"
            print(line)


def cmd_board(a):
    proc, store, root = _ctx(a)
    out = Path(a.out) if a.out else root / "board.html"
    out.write_text(board(proc, store, root), encoding="utf-8")
    print(f"  wrote {out}")


def cmd_export(a):
    proc, store, root = _ctx(a)
    print(json.dumps(export(proc, store, root, a.subject, a.step, a.v), indent=2, ensure_ascii=False))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="chain", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=os.environ.get("CHAIN_ROOT", "."))
    ap.add_argument("--process", default=os.environ.get("CHAIN_PROCESS", "process.yaml"))
    ap.add_argument("--store", default=os.environ.get("CHAIN_STORE", "store"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("ask"); s.add_argument("subject"); s.add_argument("step"); s.add_argument("--by"); s.add_argument("--note")
    s.add_argument("--again", action="store_true", help="ask even if current: a fresh version"); s.set_defaults(fn=cmd_ask)
    s = sub.add_parser("answer"); s.add_argument("subject"); s.add_argument("step"); s.add_argument("path")
    s.add_argument("--by", required=True); s.add_argument("--note"); s.set_defaults(fn=cmd_answer)
    s = sub.add_parser("status"); s.add_argument("subject", nargs="?"); s.add_argument("--json", action="store_true"); s.set_defaults(fn=cmd_status)
    s = sub.add_parser("board"); s.add_argument("--out"); s.set_defaults(fn=cmd_board)
    s = sub.add_parser("export"); s.add_argument("subject"); s.add_argument("step"); s.add_argument("--v", type=int); s.set_defaults(fn=cmd_export)
    a = ap.parse_args(argv)
    a.fn(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
