import json
from pathlib import Path

import pytest

from chain import load, Store, status, ask, answer
from chain.examples.scientopia import demo

EX = Path(__file__).resolve().parent.parent / "examples" / "scientopia"


@pytest.fixture
def cycle(tmp_path):
    r = demo.run(tmp_path)
    return load(tmp_path / "process.yaml"), Store(tmp_path / "store"), tmp_path, r


def test_the_whole_cycle_runs_and_is_current_before_the_revision(cycle):
    proc, store, root, r = cycle
    before = r["before"]["alpha"]
    assert all(c["state"] == "current" for c in before.values()), {k: v["state"] for k, v in before.items()}
    assert before["publish"]["v"] == 1 and before["question"]["by"] == "demo-human"
    judged = {d["step"]: d for d in before["paper"]["assessed"]}
    assert set(judged) == {"peer-review", "editorial"}
    assert judged["peer-review"]["by"] == "stub-agent" and judged["peer-review"]["applies"]
    assert judged["peer-review"]["tally"] == {"supported": 9, "weak": 2, "unsupported": 2}
    assert judged["editorial"]["by"] == "demo-human" and judged["editorial"]["of"] == 0
    funding = next(d for d in before["proposal"]["assessed"] if d["step"] == "funding")
    assert funding["verdict"] == "accept"                              # funding's decision stands
    assert all(c["scheme"] == "accept" for c in before.values())
    assert (root / "board.html").stat().st_size > 20000


def test_a_revision_makes_downstream_stale_and_judgements_stop_applying(cycle):
    proc, store, root, r = cycle
    after = r["after"]["alpha"]
    assert after["hypotheses"]["state"] == "current" and after["hypotheses"]["v"] == 2
    assert after["design"]["state"] == "stale" and after["proposal"]["state"] == "stale"
    assert after["study"]["state"] == "blocked" or after["study"]["state"] == "stale"
    assert after["publish"]["state"] == "blocked"
    assert not any(d["applies"] for d in after["proposal"]["assessed"])
    assert after["question"]["state"] == "current"                       # upstream is untouched


def test_answers_may_only_refer_to_what_was_staged(cycle, tmp_path):
    proc, store, root, _ = cycle
    ask(proc, store, root, "alpha", "design")          # design is stale: re-ask stages a request
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"claims": [{"id": "m9", "type": "method", "text": "x"}],
                               "edges": [{"from": "m9", "to": "alpha:study:r1", "rel": "tests"}]}))
    with pytest.raises(SystemExit, match="not staged"):
        answer(proc, store, root, "alpha", "design", bad, by="t")
    wrong = tmp_path / "wrong.json"
    wrong.write_text(json.dumps({"claims": [{"id": "r1", "type": "result", "text": "x"}]}))
    with pytest.raises(SystemExit, match="emits"):
        answer(proc, store, root, "alpha", "design", wrong, by="t")


def test_partial_readings_must_say_so(cycle, tmp_path):
    proc, store, root, _ = cycle
    # bring the chain to a fresh proposal, then review it partially
    for step in ("design", "proposal"):
        ask(proc, store, root, "alpha", step)
        if proc.steps[step].worker != "code":
            demo.answer_pending(proc, store, root, "alpha", step, EX / "answers" / f"{step}.json", "stub-agent")
    ask(proc, store, root, "alpha", "proposal-review")
    skel = json.loads((store.request_dir("alpha", "proposal-review") / "skeleton.json").read_text())
    assert any(c["about"] == ["alpha:hypotheses:p3"] for c in skel["claims"])   # the new prediction is an item
    assert any(c.get("carried") for c in skel["claims"])                       # unchanged items carried
    for c in skel["claims"]:
        if c["type"] == "decision":
            c["verdict"] = "accept"
    f = tmp_path / "p.json"; f.write_text(json.dumps(skel))
    with pytest.raises(SystemExit, match="partial"):
        answer(proc, store, root, "alpha", "proposal-review", f, by="t")


def test_a_ruling_binds_to_the_declaration_and_carries_forward(cycle, tmp_path):
    proc, store, root, _ = cycle
    y = (root / "process.yaml").read_text().replace("Publish, revise, or decline?", "Publish or decline?")
    (root / "process.yaml").write_text(y)
    proc2 = load(root / "process.yaml")
    st = status(proc2, store, root)
    assert st["process"]["scheme"]["state"] == "stale"
    assert st["alpha"]["editorial"]["scheme"] == "proposed"
    ask(proc2, store, root, "process", "scheme")
    skel = json.loads((store.request_dir("process", "scheme") / "skeleton.json").read_text())
    by_about = {c["about"][0]: c for c in skel["claims"] if c["type"] == "assessment"}
    assert by_about["step:editorial"]["verdict"] == "unconsidered"
    assert by_about["step:question"].get("carried") and by_about["step:question"]["verdict"] == "accept"


def test_answer_refused_when_the_request_went_stale(cycle, tmp_path):
    proc, store, root, _ = cycle
    ask(proc, store, root, "alpha", "design")
    (root / "instructions" / "design.md").write_text("# changed\n")
    f = tmp_path / "d.json"; f.write_text(json.dumps({"claims": []}))
    with pytest.raises(SystemExit, match="ask again"):
        answer(proc, store, root, "alpha", "design", f, by="t")


def test_export_carries_standards(cycle):
    proc, store, root, _ = cycle
    from chain.export import export
    doc = export(proc, store, root, "alpha", "study")
    types = {t for n in doc["@graph"] for t in (n.get("@type") or [])}
    assert "prov:Activity" in types and "dg:Evidence" in types and "mira:Result" in types
    assert any("cito:disputes" in n for n in doc["@graph"])
