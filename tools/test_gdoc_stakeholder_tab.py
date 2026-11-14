"""The stakeholder tab payload keeps both forms' content and loses only what the Doc lays out itself."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc_edit as ge
import gdoc_stakeholder_tab as s


def tables(text):
    return [b for b in ge.parse_blocks(text) if b["type"] == "table"]


def test_payload_has_its_tables_with_the_printed_columns():
    _date, text = s.build()
    found = tables(text)
    assert len(found) == len(s.WIDTHS)
    assert [len(t["rows"][0]) for t in found] == [len(w) for w in s.WIDTHS]
    assert found[0]["rows"][0][1:] == ["Name", "Position/Role", "Contact Information", "Requirements",
                                       "Expectations", "Classification"]
    assert found[2]["rows"][0][1:] == ["Name or Role", "Interest", "Influence", "Attitude"]


def test_widths_fill_the_landscape_page():
    assert all(sum(w) == 648 for w in s.WIDTHS)


def test_register_and_analysis_carry_the_same_ids():
    _date, text = s.build()
    found = tables(text)
    ids = [re.sub(r"</?mark>", "", row[0]) for row in found[0]["rows"][1:]]
    assert ids == [re.sub(r"</?mark>", "", row[0]) for row in found[2]["rows"][1:]]
    assert ids == ["S%02d" % n for n in range(1, len(ids) + 1)]


def test_every_highlight_and_row_reaches_the_tab():
    _date, text = s.build()
    sources = [p.read_text(encoding="utf-8") for p in (s.REGISTER, s.ANALYSIS)]
    assert text.count("<mark>") == sum(src.count("<mark>") for src in sources)
    rows = [line for src in sources for line in src.splitlines() if line.startswith("| ")]
    assert all(row in text for row in rows)


def test_page_markers_close_the_forms_and_no_repo_references():
    _date, text = s.build()
    assert text.count("@@PAGE ") == 2
    grid = text.index("#### Interest and influence grid")
    assert text.rindex("@@PAGE ") < grid
    assert ".md" not in text and "<br" not in text and "form 3.3" not in text


def test_date_is_the_forms_date_prepared():
    date, _text = s.build()
    assert re.fullmatch(r"\d{1,2} [A-Z][a-z]+ \d{4}", date)
