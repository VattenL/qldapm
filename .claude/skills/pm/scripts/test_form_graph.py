"""Tests for form_graph.py. Run: uv run -q --with pytest --with python-docx pytest -q .claude/skills/pm/scripts

The small cases build a three-to-six form knowledge directory in a temporary
folder; the last group runs against the real references/knowledge files.
"""

import contextlib
import io
import json
import re
from pathlib import Path

import pytest

import form_graph as fg


def write_form(folder, number, name="X", group="Planning", receives=(), provides=(), align=(), processes=(),
               starts=None):
    data = {
        "form": number, "name": name, "process_group": group, "pmbok_processes": list(processes),
        "receives_from": [{"source": s, "what": f"{s} into {number}"} for s in receives],
        "provides_to": [{"target": t, "what": f"{number} into {t}"} for t in provides],
        "alignment": [{"form": a, "what_must_agree": f"{number} agrees with {a}"} for a in align],
        "citation": f"Book of Forms form {number}, PDF page 20 (printed page 9)",
    }
    if starts:
        data["starts"] = {"when": starts, "cite": "Book of Forms form X, PDF page 20 (printed page 9)"}
    (Path(folder) / f"{number}.json").write_text(json.dumps(data), encoding="utf-8")


def graph(tmp_path, forms):
    folder = tmp_path / "knowledge"
    folder.mkdir(exist_ok=True)
    for number, kw in forms.items():
        write_form(folder, number, **kw)
    return fg.load_graph(folder, tmp_path / "no-index.md")


def run(*argv):
    buf = io.StringIO()
    err = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
        try:
            code = fg.main([str(a) for a in argv])
        except SystemExit as stop:
            code = stop.code
    return code, buf.getvalue()


CHAIN = {
    "1.1": dict(name="Charter", group="Initiating", provides=["2.8"], align=["2.8"]),
    "2.8": dict(name="Scope", receives=["1.1", "Business case"], provides=["2.9"]),
    "2.9": dict(name="WBS", receives=["2.8"], provides=["2.12"]),
    "2.12": dict(name="Activity List", receives=["2.9"], provides=["Scope baseline"], align=["2.9"]),
    "2.14": dict(name="Milestones", align=["2.12"]),
}


def test_flow_declared_by_either_side_is_one_edge(tmp_path):
    g = graph(tmp_path, CHAIN)
    assert g.upstream("2.9") == ["2.8"]
    assert g.downstream("2.8") == ["2.9", "Scope baseline"] or g.downstream("2.8") == ["2.9"]
    assert set(g.flow[("2.8", "2.9")]) == {"2.8", "2.9"}
    assert set(g.flow[("1.1", "2.8")]) == {"2.8", "1.1"}


def test_external_names_are_nodes_and_aliases_merge(tmp_path):
    g = graph(tmp_path, {
        "2.8": dict(receives=["Project budget (no form of this name in the book)"]),
        "2.9": dict(receives=["Project budget"]),
    })
    assert g.upstream("2.8") == ["Project budget"] == g.upstream("2.9")
    assert not g.is_form("Project budget")


def test_self_reference_is_reported_not_an_edge(tmp_path):
    g = graph(tmp_path, {"2.1": dict(provides=["2.1"])})
    assert not g.flow
    lines = []
    fg.check(g, lines.append)
    assert any("2.1 lists itself" in l for l in lines)


def test_check_groups_one_sided_links(tmp_path):
    g = graph(tmp_path, {
        "1.1": dict(group="Initiating", provides=["2.8"]),
        "2.8": dict(receives=[]),
        "2.9": dict(receives=["2.8"]),
        "2.12": dict(align=["2.9"]),
    })
    lines = []
    found = fg.check(g, lines.append)
    text = "\n".join(lines)
    assert "2.8 does not list under receives_from, though these list it under provides_to: 1.1" in text
    assert "2.8 does not list under provides_to, though these list it under receives_from: 2.9" in text
    assert "2.9 does not list under alignment, though these list it: 2.12" in text
    assert len(found) == 3
    assert run("--check", "--knowledge", tmp_path / "knowledge", "--index", tmp_path / "x")[0] == 1


def test_check_clean_graph_exits_zero(tmp_path):
    graph(tmp_path, {
        "2.8": dict(provides=["2.9"], align=["2.9"]),
        "2.9": dict(receives=["2.8"], align=["2.8"]),
    })
    code, out = run("--check", "--knowledge", tmp_path / "knowledge", "--index", tmp_path / "x")
    assert code == 0 and "0 inconsistencies" in out


def test_check_reports_unknown_form_number(tmp_path):
    g = graph(tmp_path, {"2.8": dict(provides=["9.9"])})
    lines = []
    fg.check(g, lines.append)
    assert any("9.9 is named in the knowledge files but has no knowledge file" in l for l in lines)


def test_impact_orders_by_distance_and_follows_alignment_once(tmp_path):
    g = graph(tmp_path, CHAIN)
    rows = fg.impact(g, "2.8")
    assert rows["2.9"][0] == 1 and rows["2.12"][0] == 2
    assert rows["1.1"][0] == 1 and "agree" in rows["1.1"][1]
    # 2.14 aligns with 2.12, which is downstream at distance 2, so it is rechecked at 3
    assert rows["2.14"][0] == 3
    assert "2.8" not in rows


def test_alignment_partner_is_not_followed_downstream(tmp_path):
    g = graph(tmp_path, {
        "1.1": dict(group="Initiating", provides=["2.3"], align=["2.8"]),
        "2.3": dict(receives=["1.1"]),
        "2.8": dict(),
    })
    rows = fg.impact(g, "2.8")
    assert set(rows) - {"Scope baseline"} == {"1.1"}


def test_depth_limits_the_search(tmp_path):
    g = graph(tmp_path, CHAIN)
    assert "2.12" not in fg.impact(g, "2.8", depth=1)
    assert "2.12" in fg.impact(g, "2.8", depth=2)


def test_scope_baseline_composite(tmp_path):
    g = graph(tmp_path, {
        "2.8": dict(),
        "2.9": dict(),
        "2.10": dict(),
        "2.12": dict(receives=["Scope baseline"]),
        "2.37": dict(align=["Scope baseline"]),
    })
    rows = fg.impact(g, "2.9")
    assert rows["2.12"][0] == 2 and rows["Scope baseline"][0] == 1
    assert rows["2.37"][0] == 1 and "through Scope baseline" in rows["2.37"][1]
    assert fg.impact(g, "2.10").keys() == rows.keys()


def test_docs_matching(tmp_path):
    docs = tmp_path / "docs"
    (docs / "forms").mkdir(parents=True)
    (docs / "forms" / "2-18-project-schedule.en.md").write_text("x")
    (docs / "forms" / "2.1-plan.en.md").write_text("x")
    (docs / "charter-package.en.md").write_text("x")
    (docs / "scope-package.en.md").write_text("x")
    assert fg.docs_for("2.18", docs) == ["forms/2-18-project-schedule.en.md"]
    assert fg.docs_for("2.1", docs) == ["forms/2.1-plan.en.md"]
    assert fg.docs_for("1.1", docs) == ["charter-package.en.md"]
    assert fg.docs_for("2.9", docs) == ["scope-package.en.md"]
    assert fg.docs_for("2.8", docs) == ["charter-package.en.md"]
    assert fg.docs_for("2.10", docs) == ["scope-package.en.md"]
    assert fg.docs_for("2.7", docs) == ["scope-package.en.md"]


def test_impact_marks_forms_in_docs(tmp_path):
    graph(tmp_path, CHAIN)
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "scope-package.en.md").write_text("x")
    code, out = run("--impact", "2.8", "--knowledge", tmp_path / "knowledge", "--docs", docs)
    assert code == 0
    assert "2.9 WBS  [in docs: scope-package.en.md]" in out
    assert "2.12 Activity List  [not in docs]" in out


def test_order_is_topological(tmp_path):
    g = graph(tmp_path, CHAIN)
    steps, cycles, dropped = fg.creation_order(g)
    position = {f: i for i, (_, f, _) in enumerate(steps)}
    assert not cycles and not dropped
    assert position["1.1"] < position["2.8"] < position["2.9"] < position["2.12"]
    assert dict((f, s) for s, f, _ in steps)["1.1"] == 1


def test_order_drops_the_link_from_the_later_form_and_every_other_back_link(tmp_path):
    g = graph(tmp_path, {
        "2.1": dict(provides=["2.2"], receives=["2.2"]),
        "2.2": dict(provides=["2.1"], receives=["2.1"]),
        "2.3": dict(receives=["2.2"]),
        "2.4": dict(provides=["2.1"]),
    })
    g.flow[("2.2", "2.1")].pop("2.1")
    steps, cycles, dropped = fg.creation_order(g)
    assert [c for c, _ in cycles] == [["2.1", "2.2"]]
    assert dropped == [("2.2", "2.1"), ("2.4", "2.1")]
    position = {f: i for i, (_, f, _) in enumerate(steps)}
    assert position["2.1"] < position["2.2"] < position["2.3"]


def test_order_cut_is_deterministic(tmp_path):
    forms = {
        "2.1": dict(provides=["2.2"]),
        "2.2": dict(provides=["2.3"]),
        "2.3": dict(provides=["2.1"]),
    }
    first = fg.creation_order(graph(tmp_path, forms))
    second = fg.creation_order(graph(tmp_path, forms))
    assert first == second and len(first[2]) == 1


def test_order_cuts_a_loop_by_process_sequence_not_by_position(tmp_path):
    # 2.23 (8.1) says it provides to 2.4 (5.1); the earlier process is drafted first
    g = graph(tmp_path, {
        "2.4": dict(processes=["5.1 Plan Scope Management"], receives=["2.23"]),
        "2.6": dict(processes=["5.2 Collect Requirements"], receives=["2.4"]),
        "2.23": dict(processes=["8.1 Plan Quality Management"], receives=["2.6"], provides=["2.4"]),
    })
    steps, cycles, dropped = fg.creation_order(g)
    step = {f: s for s, f, _ in steps}
    assert dropped == [("2.23", "2.4")]
    assert step["2.4"] < step["2.6"] < step["2.23"]


def test_a_form_without_a_process_takes_the_rank_of_the_form_before_it(tmp_path):
    g = graph(tmp_path, {
        "2.2": dict(processes=["4.2 Develop Project Management Plan"]),
        "2.3": dict(),
        "2.4": dict(processes=["5.1 Plan Scope Management"]),
    })
    ranks = fg.process_ranks(g)
    assert ranks["2.2"] < ranks["2.3"] < ranks["2.4"]
    assert ranks["2.3"][:3] == ranks["2.2"][:3]


def test_links_into_a_form_created_at_the_start_are_revision_inputs(tmp_path):
    g = graph(tmp_path, {
        "2.8": dict(processes=["5.3 Define Scope"], provides=["2.32"]),
        "2.32": dict(processes=["11.2 Identify Risks"], receives=["2.8"], starts="the start of the project"),
        "4.1": dict(group="Monitoring and Controlling", processes=["4.5 Monitor and Control Project Work"],
                    provides=["2.32"]),
    })
    steps, cycles, dropped = fg.creation_order(g)
    step = {f: (s, pre) for s, f, pre in steps}
    assert step["2.32"] == (1, [])
    assert set(dropped) == {("2.8", "2.32"), ("4.1", "2.32")}
    code, out = run("--order", "--knowledge", tmp_path / "knowledge")
    assert "created at the start of the project" in out and "revised as these exist: 2.8, 4.1" in out


def test_impact_takes_several_forms_and_counts_files(tmp_path):
    graph(tmp_path, CHAIN)
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "scope-package.en.md").write_text("x")
    code, out = run("--impact", "2.8", "2.12", "--knowledge", tmp_path / "knowledge", "--docs", docs)
    assert code == 0
    assert "Recheck when 2.8 Scope and 2.12 Activity List change" in out
    assert "1 of 3 forms exist in docs/, in 1 file." in out
    assert "scope-package.en.md holds 2.9" in out
    rows = fg.impact(fg.load_graph(tmp_path / "knowledge", tmp_path / "x"), ["2.8", "2.12"])
    assert "2.8" not in rows and "2.12" not in rows


def test_impact_of_3_3_adds_the_category_forms_and_labels_them(tmp_path):
    g = graph(tmp_path, {
        "3.3": dict(group="Executing", provides=["3.4"]),
        "3.4": dict(group="Executing"),
        "2.9": dict(), "2.22": dict(), "2.32": dict(),
    })
    rows = fg.impact(g, "3.3", depth=1)
    assert rows["2.9"][0] == 1 and "Impacts of Change: Scope" in rows["2.9"][1] and fg.SKILL_TAG in rows["2.9"][1]
    assert "Impacts of Change: Cost" in rows["2.22"][1]
    assert "3.4" in rows and fg.SKILL_TAG not in rows["3.4"][1]
    only = fg.impact(g, "3.3", depth=1, categories=["Cost"])
    assert "2.22" in only and "2.9" not in only


def test_a_risk_register_provides_to_a_change_request(tmp_path):
    g = graph(tmp_path, {"2.32": dict(), "3.3": dict(group="Executing")})
    rows = fg.impact(g, "2.32", depth=1)
    assert rows["3.3"][0] == 1 and "11.5.3.1" in rows["3.3"][1]


def test_impact_cli_rejects_an_unknown_category(tmp_path):
    graph(tmp_path, CHAIN)
    assert run("--impact", "2.8", "--category", "Nonsense", "--knowledge", tmp_path / "knowledge")[0] == 2
    assert run("2.8", "--category", "Cost", "--knowledge", tmp_path / "knowledge")[0] == 2


def test_order_group_filter(tmp_path):
    graph(tmp_path, CHAIN)
    code, out = run("--order", "--group", "init", "--knowledge", tmp_path / "knowledge")
    assert code == 0 and "1.1 Charter" in out and "2.8 Scope" not in out
    assert run("--order", "--group", "nonsense", "--knowledge", tmp_path / "knowledge")[0] == 2


def test_single_form_view(tmp_path):
    graph(tmp_path, CHAIN)
    code, out = run("2-9", "--knowledge", tmp_path / "knowledge")
    assert code == 0
    assert "2.8 Scope [declared by both]" in out
    assert "2.12 Activity List [declared by both]" in out
    assert "Business case" in run("2.8", "--knowledge", tmp_path / "knowledge")[1]
    assert run("9.9", "--knowledge", tmp_path / "knowledge")[0] == 2


def test_markdown_has_group_tables_and_mermaid(tmp_path):
    graph(tmp_path, CHAIN)
    target = tmp_path / "out.md"
    code, _ = run("--markdown", "--out", target, "--knowledge", tmp_path / "knowledge")
    text = target.read_text(encoding="utf-8")
    assert code == 0
    assert "## Initiating" in text and "## Planning" in text
    assert "```mermaid" in text and 'n2_8["2.8 Scope"]' in text and "n2_8 --> n2_9" in text
    assert "n1_1" not in text.split("```mermaid")[1]
    assert "## Documents named without a form number" in text and "| Business case |" in text


def test_markdown_prints_by_default_and_never_writes_into_the_skill(tmp_path):
    graph(tmp_path, CHAIN)
    before = fg.OUTPUT.read_bytes() if fg.OUTPUT.exists() else None
    code, out = run("--markdown", "--knowledge", tmp_path / "knowledge")
    assert code == 0 and out.startswith("# Form graph") and "wrote" not in out
    assert (fg.OUTPUT.read_bytes() if fg.OUTPUT.exists() else None) == before
    assert run("--out", tmp_path / "x.md", "--knowledge", tmp_path / "knowledge")[0] == 2


def test_a_package_section_stands_in_for_a_form_and_is_counted_apart(tmp_path):
    graph(tmp_path, CHAIN)
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "scope-package.en.md").write_text("x")
    (docs / "charter-package.en.md").write_text("x")
    code, out = run("--impact", "2.12", "--knowledge", tmp_path / "knowledge", "--docs", docs)
    assert "2.14 Milestones  [stand-in section in docs: charter-package.en.md, Part 2A, Summary milestone schedule" in out
    assert "1 of 2 forms exist in docs/" in out
    assert "1 more has a stand-in section" in out and "2.14 is held as charter-package.en.md" in out
    assert "Nothing to compare" not in out
    assert "none dropped and none added" in out
    assert fg.stand_in_for("2.14", tmp_path / "no-docs") is None


def test_modes_are_exclusive(tmp_path):
    assert run("2.8", "--order")[0] == 2
    assert run()[0] == 2
    assert run("--group", "Planning", "2.8")[0] == 2


REAL_FORMS = sorted(fg.KNOWLEDGE.glob("*.json"))


@pytest.fixture(scope="module")
def real_graph():
    return fg.load_graph()



@pytest.mark.skipif(not REAL_FORMS, reason="knowledge files not present")
class TestRealData:
    @pytest.fixture
    def g(self, real_graph):
        return real_graph

    def test_all_66_forms_load_and_match_the_index(self, g):
        assert len(g.forms) == 66 and set(g.forms) == set(g.index)

    def test_every_form_number_named_is_a_form(self, g):
        assert {n for n in g.nodes() if fg.FORM_RE.match(n)} <= set(g.forms)

    def test_scope_baseline_is_the_book_composite(self, g):
        assert g.upstream("Scope baseline")[-3:] == ["2.8", "2.9", "2.10"]
        assert "2.12" in g.downstream("Scope baseline")

    def test_order_respects_every_kept_edge(self, g):
        steps, cycles, dropped = fg.creation_order(g)
        assert len(steps) == 66
        step = {f: s for s, f, _ in steps}
        cut = set(dropped)
        for (a, b) in fg.order_edges(g):
            if (a, b) not in cut:
                assert step[a] < step[b], (a, b)
        assert all(e in fg.order_edges(g) for e in dropped)

    def test_order_follows_the_process_sequence(self, g):
        steps, _, _ = fg.creation_order(g)
        step = {f: s for s, f, _ in steps}
        for a, b in (("1.1", "2.1"), ("1.3", "2.4"), ("2.4", "2.6"), ("2.16", "2.18"), ("2.17", "2.18"),
                     ("2.21", "2.22"), ("2.20", "2.22"), ("2.2", "3.3"), ("2.1", "2.2")):
            assert step[a] < step[b], (a, b)
        assert step["1.1"] == 1 and step["1.3"] <= 2

    def test_logs_created_at_the_start_have_no_prerequisites(self, g):
        steps, _, _ = fg.creation_order(g)
        step = {f: (s, pre) for s, f, pre in steps}
        for f in ("2.32", "2.33", "3.1", "3.2"):
            assert g.forms[f]["starts"]["when"] == "the start of the project"
            assert step[f] == (1, [])

    def test_3_3_impact_reaches_every_category_form(self, g):
        rows = fg.impact(g, "3.3", depth=1)
        for f in ("2.2", "3.4", "2.8", "2.9", "2.10", "2.6", "2.7", "2.20", "2.22", "2.23", "2.14", "2.18", "2.32"):
            assert f in rows, f

    def test_charter_comes_first_and_is_in_step_one(self, g):
        steps, _, _ = fg.creation_order(g)
        assert dict((f, s) for s, f, _ in steps)["1.1"] == 1

    def test_impact_of_every_form_is_computed(self, g):
        for f in g.forms:
            assert f not in fg.impact(g, f)

    def test_wbs_impact_includes_the_schedule_and_the_charter(self, g):
        rows = fg.impact(g, "2.9")
        assert rows["2.18"][0] == 1 and rows["1.1"][0] == 1

    def test_markdown_covers_every_form(self, g):
        text = fg.markdown(g)
        for f in g.forms:
            assert f"| {f} | {g.name(f)} |" in text
        assert not any(ord(c) in (0x2013, 0x2014) for c in text)


def declared(g, form):
    """What the form's own knowledge file declares: (receives, provides, alignment) as sets."""
    receives = {s for (s, d), by in g.flow.items() if d == form and form in by}
    provides = {d for (s, d), by in g.flow.items() if s == form and form in by}
    align = {b if a == form else a for (a, b), by in g.align.items() if form in by}
    return receives, provides, align


@pytest.mark.skipif(not REAL_FORMS, reason="knowledge files not present")
class TestAgainstThePrintedPages:
    """Lists read off the book and compared by hand with the knowledge files."""

    @pytest.fixture
    def g(self, real_graph):
        return real_graph

    def test_2_32_risk_register_lists_on_pdf_pages_139_to_140(self, g):
        # Book of Forms form 2.32, PDF page 139 (printed page 128): "can receive information from" 19 documents
        receives, provides, align = declared(g, "2.32")
        assert receives == {"1.2", "3.1", "3.5", "2.5", "2.6", "Scope baseline", "2.11", "2.16", "Schedule baseline",
                            "2.19", "2.20", "2.22", "2.23", "2.26", "2.28", "2.31", "Procurement documents",
                            "Agreements", "1.3"}
        # PDF pages 139 to 140 (printed pages 128 to 129): "provides information to" 10 documents
        assert provides == {"2.8", "2.16", "2.20", "2.23", "2.28", "2.33", "2.37", "2.40", "3.5", "5.2"}
        # the book prints no Alignment section for 2.32
        assert align == set()

    def test_2_32_partners_are_exactly_the_forms_whose_alignment_names_the_register(self, g):
        # Alignment sections naming the risk register: 1.1, 1.2, 2.22 (PDF page 104), 2.33, 2.34, 2.35
        # (PDF page 153), 2.36, 3.1, 4.1, 4.2, 4.5, 5.1
        assert set(g.partners("2.32")) == {"1.1", "1.2", "2.22", "2.33", "2.34", "2.35", "2.36", "3.1", "4.1",
                                            "4.2", "4.5", "5.1"}

    def test_form_without_alignment_section_says_so(self, g):
        lines = []
        fg.show_form(g, "2.32", lines.append)
        assert any("no Alignment section" in line for line in lines)
        lines = []
        fg.show_form(g, "2.10", lines.append)
        assert not any("no Alignment section" in line for line in lines)

    def test_2_10_wbs_dictionary_lists_on_pdf_pages_63_to_64(self, g):
        # Book of Forms form 2.10, PDF page 63 (printed page 52): receives from 9, provides to 12, aligned with 5
        receives, provides, align = declared(g, "2.10")
        assert receives == {"2.6", "2.8", "1.2", "2.12", "2.14", "2.28", "2.20", "2.24", "Contracts"}
        assert provides == {"2.12", "2.15", "2.16", "2.18", "2.20", "Project budget", "2.23", "2.26", "2.28",
                            "2.32", "2.37", "Accepted deliverables"}
        assert set(g.flow[("2.10", "Scope baseline")]) == {"(book)"}
        assert {"1.1", "2.6", "2.8", "2.9", "2.12"} <= align

    def test_2_10_alignment_through_the_scope_baseline(self, g):
        # 2.18 (PDF page 89), 2.37 and 2.39 name "Scope baseline" in their Alignment sections
        partners = g.partners("2.10")
        for form in ("2.18", "2.37", "2.39"):
            assert [via for via, _by in partners[form]] == ["Scope baseline"]

    def test_scope_baseline_cites_the_forms_that_define_it(self, g):
        # printed page 49 is form 2.9 (PDF page 60), printed page 52 is form 2.10 (PDF page 63)
        cite = fg.COMPOSITES["Scope baseline"]["cite"]
        assert "form 2.9, PDF page 60 (printed page 49)" in cite
        assert "form 2.10, PDF page 63 (printed page 52)" in cite
        assert "form 2.8" not in cite

    def test_3_3_change_request_lists_on_pdf_pages_181_to_182(self, g):
        # Book of Forms form 3.3, PDF page 181 (printed page 170): Alignment lists the change management plan
        # and the change log; the prose names the change control board and any executing process
        receives, provides, align = declared(g, "3.3")
        assert align == {"2.2", "3.4"}
        # 3.4 is a reading from the 3.4 prose and Table 3.4 (the 3.3 pages name only the board)
        assert provides == {"Change control board", "3.4"}
        assert receives == {"Executing, monitoring and controlling processes"}

    def test_3_3_links_declared_by_other_forms(self, g):
        # 2.7 (PDF page 51) and 2.14 (PDF page 76) list "Change requests"; 2.2 (PDF page 36) and
        # 3.4 (PDF page 186) list the change request as related
        assert set(g.upstream("3.3")) >= {"2.7", "2.14"}
        assert set(g.downstream("3.3")) >= {"2.2", "3.4"}
        assert set(g.flow[("2.7", "3.3")]) == {"2.7"}

    def test_resource_forms_come_before_the_estimates_that_use_them(self, g):
        steps, _, _ = fg.creation_order(g)
        step = {f: s for s, f, _ in steps}
        # 9.1 and 9.2 rank with 6.3: PMBOK 6 section 6.4, printed page 195 (PDF page 234), takes the resource
        # requirements and breakdown structure of 9.2 as inputs
        assert step["2.26"] < step["2.28"] < step["2.17"] < step["2.18"] < step["2.20"]
        assert step["2.28"] < step["2.16"] and step["2.29"] < step["2.17"]

    def test_monitoring_forms_need_the_plans_and_baselines_they_measure_against(self, g):
        steps, _, _ = fg.creation_order(g)
        by = {f: (s, pre) for s, f, pre in steps}
        for f, (sources, _cite) in fg.ORDER_INPUTS.items():
            assert set(sources) <= set(by[f][1]), f
            assert all(by[f][0] > by[x][0] for x in sources), f
        assert by["4.3"][0] > by["2.22"][0] and by["4.4"][0] > by["4.3"][0]

    def test_order_text_says_what_needs_nothing_means(self, g):
        code, out = run("--order")
        assert code == 0
        assert "means the book lists no source for the form" in out
        assert "Prerequisites added by the skill (skill mapping, not book text)" in out

    def test_the_committed_form_graph_is_the_generated_one(self, g):
        committed = fg.OUTPUT.read_text(encoding="utf-8")
        assert committed == fg.markdown(g), "regenerate: form_graph.py --markdown --out references/form-graph.md"

    def test_forms_the_book_only_aligns_are_drafted_after_the_plan_they_align_with(self, g):
        steps, _, _ = fg.creation_order(g)
        by = {f: (s, pre) for s, f, pre in steps}
        assert by["2.27"][0] > by["2.26"][0]
        assert by["2.39"][0] > max(by["2.37"][0], by["2.38"][0])
        assert by["4.8"][0] > max(by["2.37"][0], by["4.7"][0])
        for f in ("2.27", "2.39", "4.8"):
            assert "Alignment" in fg.ORDER_INPUTS[f][1], f
            assert "printed page" in fg.ORDER_INPUTS[f][1], f

    def test_a_form_with_no_listed_source_is_told_to_check_its_alignment_partners(self, g):
        code, out = run("--order")
        line = next(x for x in out.splitlines() if "1.1 Project Charter" in x and "step" in x)
        assert "the book lists no source; it must agree with" in line

    def test_stand_in_sections_exist_in_the_charter_package(self):
        charter = (fg.DOCS / "charter-package.en.md")
        if not charter.is_file():
            pytest.skip("needs the charter package")
        text = charter.read_text(encoding="utf-8")
        for form, (name, section) in fg.STAND_INS.items():
            assert name == charter.name
            for part in section.replace("Part 2A, ", "").split(", "):
                heading = re.sub(r"^\d[.\d]* ", "", part)
                assert heading.lower() in text.lower(), (form, part)

    def test_impact_of_the_schedule_keeps_the_form_count_and_adds_stand_ins(self, g):
        code, out = run("--impact", "2.18", "--depth", "1")
        assert "5 of 29 forms exist in docs/" in out
        for form in ("1.2", "2.14", "2.32"):
            assert f"{form} is held as charter-package.en.md" in out
        assert "2.22 Cost Baseline  [not in docs]" in out

    def test_every_change_source_reaches_3_3_with_a_citation(self, g):
        for f, text in fg.CHANGE_SOURCES.items():
            assert "PMBOK 6 section" in text and "(PDF page" in text and "printed page" in text, f
            assert "3.3" in fg.impact(g, f), f

    def test_3_3_impact_reaches_stakeholder_and_document_boxes(self, g):
        rows = fg.impact(g, "3.3", depth=1)
        for f in ("1.3", "1.4", "2.30", "2.40", "1.2", "2.31", "3.6"):
            assert f in rows, f
        assert set(fg.IMPACT_CATEGORIES) >= {"Stakeholder Impact", "Project Documents"}
        only = fg.impact(g, "3.3", depth=1, categories=["Stakeholder Impact"])
        assert "1.3" in only and "2.8" not in only


def test_impact_says_when_there_is_nothing_to_compare(tmp_path):
    graph(tmp_path, CHAIN)
    docs = tmp_path / "docs"
    docs.mkdir()
    code, out = run("--impact", "2.8", "--knowledge", tmp_path / "knowledge", "--docs", docs)
    assert code == 0
    assert "Nothing to compare" in out
    (docs / "scope-package.en.md").write_text("x")
    code, out = run("--impact", "2.8", "--knowledge", tmp_path / "knowledge", "--docs", docs)
    assert "Nothing to compare" not in out and "Compare only the 1 that exist" in out

def test_forms_of_the_later_groups_are_tagged_first_version_and_final(tmp_path):
    graph(tmp_path, {
        "1.1": dict(name="Charter", group="Initiating", provides=["3.5"]),
        "3.5": dict(name="Lessons", group="Executing", receives=["1.1"], provides=["5.1"]),
        "5.1": dict(name="Summary", group="Closing", receives=["3.5"]),
    })
    code, out = run("--order", "--knowledge", tmp_path / "knowledge")
    assert code == 0
    planning, _, late = out.partition("not part of the planning sequence above")
    assert "1.1 Charter [Initiating]" in planning and "3.5" not in planning.split("Forms of the later groups")[0]
    assert "first version at step 2; final version: the last update before closeout" in late
    assert "first version at step 3; final version: closeout" in late


def test_impact_also_says_what_the_changed_form_receives_from(tmp_path):
    graph(tmp_path, CHAIN)
    code, out = run("--impact", "2.9", "--knowledge", tmp_path / "knowledge", "--docs", tmp_path / "docs")
    assert code == 0
    assert "2.9 WBS receives from (1): 2.8 Scope" in out

