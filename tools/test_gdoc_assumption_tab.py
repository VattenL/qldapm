"""The assumption tab payload keeps the log's content and loses only what the Doc lays out itself."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc_edit as ge
import gdoc_assumption_tab as a


def tables(text):
    return [b for b in ge.parse_blocks(text) if b["type"] == "table"]


def test_payload_has_the_printed_columns():
    _date, text = a.build()
    found = tables(text)
    assert len(found) == 1
    assert found[0]["rows"][0] == ["ID", "Category", "Assumption/Constraint", "Responsible Party", "Due Date",
                                   "Actions", "Status", "Comments"]
    assert sum(a.WIDTHS) == 648 and len(a.WIDTHS) == len(found[0]["rows"][0])


def test_assumptions_keep_the_charter_numbers():
    _date, text = a.build()
    ids = [row[0] for row in tables(text)[0]["rows"][1:]]
    assert ids == [str(n) for n in range(1, 21)] + ["C%d" % n for n in range(1, 7)]


def test_charter_assumptions_are_copied_word_for_word():
    charter = (a.FORMS.parent / "charter-package.en.md").read_text(encoding="utf-8")
    section = charter[charter.index("### 1.6 Project Assumptions"):charter.index("## Part 2")]
    source = dict(re.findall(r"^\| (\d+) \| (.+) \|$", section, re.M))
    _date, text = a.build()
    logged = {row[0]: row[2] for row in tables(text)[0]["rows"][1:]}
    assert all(logged[n] == source[n] for n in source)


def test_every_highlight_and_row_reaches_the_tab():
    _date, text = a.build()
    source = a.LOG.read_text(encoding="utf-8")
    assert text.count("<mark>") == source.count("<mark>")
    assert all(row in text for row in source.splitlines() if row.startswith("| "))


def test_page_marker_and_no_repo_references():
    _date, text = a.build()
    assert text.count("@@PAGE ") == 1
    assert ".md" not in text and "scope package" not in text and "<br" not in text


def test_date_is_the_forms_date_prepared():
    date, _text = a.build()
    assert re.fullmatch(r"\d{1,2} [A-Z][a-z]+ \d{4}", date)
