#!/usr/bin/env python3
"""A result row must be readable without knowing how many fields it has.

Rows grew a fifth field, `measured`, and nine scripts broke in the same place: each ended with

    n_pass = sum(1 for _, _, _, s in ROWS if s == "PASS")

which asserts the row has exactly four fields. The first observed run raised `ValueError: too
many values to unpack (expected 4)` and wrote no results, so the paper read as a failed
verification — the same shape of fault #141 had just fixed in the observer.

Unpacking a record into a fixed number of names is a readable habit and the wrong one for a
record meant to grow. These checks are static: they run in milliseconds and would have caught
all nine before any script was launched.
"""

import ast
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def scripts():
    return sorted(glob.glob(os.path.join(ROOT, "verification", "*", "verify.py")))


def fixed_arity_unpacks(tree):
    """Every place that unpacks ROWS into a tuple of names instead of indexing it."""
    bad = []
    for node in ast.walk(tree):
        target = iter_ = None
        if isinstance(node, ast.For):
            target, iter_ = node.target, node.iter
        elif isinstance(node, ast.comprehension):
            target, iter_ = node.target, node.iter
        if isinstance(iter_, ast.Name) and iter_.id == "ROWS" \
                and isinstance(target, ast.Tuple):
            bad.append((node.lineno if hasattr(node, "lineno") else iter_.lineno,
                        len(target.elts)))
    return bad


def row_declares_measured(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "row":
            names = [a.arg for a in node.args.args]
            return "measured" in names
    return False


def main():
    failures = []
    for path in scripts():
        rel = os.path.relpath(path, ROOT)
        tree = ast.parse(open(path, encoding="utf-8").read())

        for lineno, n in fixed_arity_unpacks(tree):
            failures.append(f"{rel}:{lineno} unpacks ROWS into {n} names; index the row instead")

        if not row_declares_measured(tree):
            failures.append(f"{rel} defines row() without `measured` — its results cannot say "
                            f"whether the value came from this run")

    # The observer must pass the flag on when a script sets it, and must not invent one when
    # the script says nothing: absent and false are different facts about a row.
    sys.path.insert(0, os.path.join(ROOT, "verification"))
    import audit_run  # noqa: E402

    emit = audit_run.result_row
    if "measured" in emit(("s", "p", "v", "PASS")):
        failures.append("a four-field row must not acquire a `measured` key")
    if emit(("s", "p", "v", "PASS", False)).get("measured") is not False:
        failures.append("a row marked unmeasured must reach provenance as measured=false")
    if emit(("s", "p", "v", "PASS", True)).get("measured") is not True:
        failures.append("a row marked measured must reach provenance as measured=true")

    for f in failures:
        print(f"FAIL {f}")
    n = len(scripts())
    print(f"{'FAILED' if failures else 'ok'}: {n} verification script(s), "
          f"{len(failures)} problem(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
