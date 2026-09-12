import json
from pathlib import Path

import pytest

from chain import load, Store, status, ask, answer, stage
from chain.examples.scientopia import demo


@pytest.fixture(scope="module")
def cycle(tmp_path_factory):
    root = tmp_path_factory.mktemp("sci")
    r = demo.run(root)
    return load(root / "process.yaml"), Store(root / "store"), root, r


def test_one_round_runs_and_the_loop_closes(cycle):
    proc, store, root, r = cycle
    st = r["status"]
    assert st["library"]["catalogue"]["v"] == 2                      # re-asked after publication
    assert st["library"]["catalogue"]["state"] == "current"
    # every team's reading of the library is now out of date: the loop
    assert st["juniper"]["question"]["state"] == "stale" and "journal:*:published" in st["juniper"]["question"]["moved"]
    assert st["aurora"]["select"]["state"] == "blocked"              # its inputs read the old catalogue
    assert (root / "board.html").stat().st_size > 20000


def test_the_funder_judged_every_proposal_and_the_journal_every_paper(cycle):
    proc, store, root, r = cycle
    st = r["status"]
    j = {d["player"]: d for d in st["juniper"]["proposal"]["assessed"]}
    l = {d["player"]: d for d in st["larch"]["proposal"]["assessed"]}
    assert j["aurora"]["verdict"] == "accept" and l["aurora"]["verdict"] == "reject"
    assert j["aurora"]["tally"]["fund"] >= 6 and l["aurora"]["tally"] == {"decline": 6}
    assert j["aurora"]["by"] == "stub:aurora"
    pub = {d["step"]: d for d in st["juniper"]["paper"]["assessed"]}
    assert pub["decision"]["verdict"] == "accept" and pub["decision"]["player"] == "meridian"
    assert pub["review"]["tally"] == {"supported": 9, "weak": 1, "unsupported": 1}   # per paper, not per wrapper
    larch_study = json.loads((store.version_dir("larch", "study", 1) / "claims.json").read_text())
    assert [c["type"] for c in larch_study["claims"]] == ["scope"]   # declined: no study, said so
    published = json.loads((store.version_dir("meridian", "published", 1) / "claims.json").read_text())
    assert published["sections"][0]["id"] == "pub:meridian:1" and published["sections"][0]["claims"] == ["juniper:paper"]


def test_a_set_input_is_stale_when_a_member_changes_or_appears(cycle):
    proc, store, root, r = cycle
    # a set input never blocks: the journal's record stands although the teams' reading of the
    # library is out of date — a loop cannot be a wait
    assert r["status"]["meridian"]["submissions"]["state"] == "current"
    assert r["status"]["juniper"]["paper"]["state"] == "blocked"
    # a new team appears: the funder's reading of `team:*:proposal` is stale on membership alone
    y = (root / "process.yaml").read_text().replace("      larch:   {name: Larch Group, persona: personas/larch.md}",
                                                   "      larch:   {name: Larch Group, persona: personas/larch.md}\n      rowan: {name: Rowan}")
    (root / "process.yaml").write_text(y)
    proc2 = load(root / "process.yaml")
    st = status(proc2, store, root)
    assert st["rowan"]["question"]["state"] == "absent"
    assert st["aurora"]["select"]["state"] in ("stale", "blocked")


def test_answers_may_only_refer_to_what_was_staged(cycle, tmp_path):
    proc, store, root, _ = cycle
    ask(proc, store, root, "juniper", "question")          # stale since the library grew: re-asked
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"claims": [{"id": "q9", "type": "question", "text": "x"}],
                               "edges": [{"from": "q9", "to": "larch:hypotheses:h1", "rel": "cites"}]}))
    with pytest.raises(SystemExit, match="not staged"):
        answer(proc, store, root, "juniper", "question", bad, by="t")
    wrong = tmp_path / "wrong.json"
    wrong.write_text(json.dumps({"claims": [{"id": "r1", "type": "result", "text": "x"}]}))
    with pytest.raises(SystemExit, match="emits"):
        answer(proc, store, root, "juniper", "question", wrong, by="t")
    store.wipe_request("juniper", "question")


def test_partial_readings_must_say_so_and_the_persona_is_staged(cycle, tmp_path):
    proc, store, root, _ = cycle
    rd = stage(proc, store, root, "aurora", "select")
    assert (rd / "PERSONA.md").read_text().startswith("# Aurora Foundation")
    skel = json.loads((rd / "skeleton.json").read_text())
    assert {c["about"][0] for c in skel["claims"] if c["type"] == "decision"} == {"juniper:proposal", "larch:proposal"}
    assert all(c.get("carried") for c in skel["claims"] if c["type"] == "assessment")   # nothing changed
    for c in skel["claims"]:
        if c["type"] == "decision":
            c["verdict"] = "accept"
    skel["claims"][0]["verdict"] = "unconsidered"
    f = tmp_path / "p.json"; f.write_text(json.dumps(skel))
    with pytest.raises(SystemExit, match="partial"):
        answer(proc, store, root, "aurora", "select", f, by="t")
    store.wipe_request("aurora", "select")


def test_a_ruling_binds_to_the_declaration_and_carries_forward(cycle, tmp_path):
    proc, store, root, _ = cycle
    y = (root / "process.yaml").read_text().replace("Which papers are published?", "Which papers go out?")
    (root / "process.yaml").write_text(y)
    proc2 = load(root / "process.yaml")
    st = status(proc2, store, root)
    assert st["process"]["scheme"]["state"] == "stale" and st["meridian"]["decision"]["scheme"] == "proposed"
    ask(proc2, store, root, "process", "scheme")
    skel = json.loads((store.request_dir("process", "scheme") / "skeleton.json").read_text())
    by_about = {c["about"][0]: c for c in skel["claims"] if c["type"] == "assessment"}
    assert by_about["step:decision"]["verdict"] == "unconsidered"
    assert by_about["step:question"].get("carried") and by_about["step:question"]["verdict"] == "accept"
    store.wipe_request("process", "scheme")


def test_answer_refused_when_the_request_went_stale(cycle, tmp_path):
    proc, store, root, _ = cycle
    ask(proc, store, root, "juniper", "question")
    (root / "personas" / "juniper.md").write_text("# changed\n")
    f = tmp_path / "d.json"; f.write_text(json.dumps({"claims": []}))
    with pytest.raises(SystemExit, match="ask again"):
        answer(proc, store, root, "juniper", "question", f, by="t")


def test_export_carries_standards(cycle):
    proc, store, root, _ = cycle
    from chain.export import export
    doc = export(proc, store, root, "juniper", "study")
    types = {t for n in doc["@graph"] for t in (n.get("@type") or [])}
    assert "prov:Activity" in types and "dg:Evidence" in types and "mira:Result" in types
    assert any("cito:disputes" in n for n in doc["@graph"])
