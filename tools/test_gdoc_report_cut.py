"""The cut report keeps the index arithmetic of Docs, moves without losing elements, and sets every
text to Arial at 12 pt or more."""

import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc_report_cut as rc


def cell(text):
    return {"content": [rc.para(text)], "tableCellStyle": {}}


def table(rows):
    return {"table": {"rows": len(rows), "columns": len(rows[0]),
                      "tableRows": [{"tableCells": [cell(t) for t in r]} for r in rows],
                      "tableStyle": {"tableColumnProperties": [{} for _ in rows[0]]}}}


def test_reindex_counts_a_table_as_docs_does():
    # A 1x1 table with an empty cell takes 5 indexes: table, row, cell, the cell's newline, table end;
    # gdoc_merge_tabs.Writer.table relies on the same layout.
    content = [{"sectionBreak": {}}, rc.para("ab"), table([[""]]), rc.para("")]
    end = rc.reindex(content, 0)
    t = content[2]
    assert content[1]["startIndex"] == 1 and content[1]["endIndex"] == 4
    assert t["startIndex"] == 4 and t["endIndex"] == 9
    assert t["table"]["tableRows"][0]["tableCells"][0]["content"][0]["startIndex"] == 7
    assert end == 10


def test_reindex_counts_utf16_units():
    content = [{"sectionBreak": {}}, rc.para("\U0001F600")]
    assert rc.reindex(content, 0) == 4


def test_move_leaves_a_pointer_and_keeps_every_element():
    content = [rc.para("1.1 Heading", "HEADING_3"), rc.para("intro"), table([["a", "b"]]), rc.para("next")]
    app = rc.Appendix("E")
    name = app.move(content, 1, 3, "Detail", "See {name}.", content[1])
    assert name == "Appendix E" and app.letter == "F"
    assert [rc.ptext(e).strip() for e in content if "paragraph" in e] == ["1.1 Heading", "See Appendix E.", "next"]
    assert rc.ptext(app.out[0]).strip() == "Appendix E: Detail"
    assert "table" in app.out[2] and "paragraph" in app.out[3]


def test_move_refuses_a_section_break():
    content = [rc.para("x"), {"sectionBreak": {}}, rc.para("y")]
    with pytest.raises(SystemExit):
        rc.Appendix().move(content, 0, 2, "t", "{name}", content[0])


def test_restyle_sets_arial_and_lifts_small_text():
    small = rc.para("small")
    small["paragraph"]["elements"][0]["textRun"]["textStyle"] = {"fontSize": {"magnitude": 10, "unit": "PT"}}
    head = rc.para("Head", "HEADING_3")
    content = [small, head, table([["c"]])]
    named = {"NORMAL_TEXT": {"textStyle": {"fontSize": {"magnitude": 11, "unit": "PT"}}},
             "HEADING_3": {"textStyle": {"fontSize": {"magnitude": 14, "unit": "PT"}},
                           "paragraphStyle": {"spaceAbove": {"magnitude": 16, "unit": "PT"}}}}
    rc.restyle(content, named)
    for e in rc.walk_paragraphs(content):
        ts = e["paragraph"]["elements"][0]["textRun"]["textStyle"]
        assert ts["weightedFontFamily"]["fontFamily"] == "Arial"
        assert ts["fontSize"]["magnitude"] >= 12
    assert head["paragraph"]["elements"][0]["textRun"]["textStyle"]["fontSize"]["magnitude"] == 14
    assert head["paragraph"]["paragraphStyle"]["spaceAbove"]["magnitude"] == 16
    pad = content[2]["table"]["tableRows"][0]["tableCells"][0]["tableCellStyle"]
    assert pad["paddingTop"]["magnitude"] == 2 and pad["paddingLeft"]["magnitude"] == 2


def test_fit_widths_keeps_numbers_whole_and_fills_the_page():
    t = table([["Labor Costs", "Assumptions"], ["587,661,000", "word " * 80]])
    assert rc.fit_widths(t, total=300)
    w = [p["width"]["magnitude"] for p in t["table"]["tableStyle"]["tableColumnProperties"]]
    assert w[0] >= rc.word_width("587,661,000", 12, False) + 4
    assert abs(sum(w) - 300) < 0.5


def test_fit_widths_reports_a_table_too_narrow():
    t = table([["Supercalifragilistic", "Antidisestablishment"]])
    assert not rc.fit_widths(t, total=100)
