"""The risk tab payload keeps the register's content and loses only what the Doc lays out itself."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc_edit as ge
import gdoc_risk_tab as r


def test_payload_has_both_banks():
    _date, text = r.build()
    blocks = ge.parse_blocks(text)
    assert [b["type"] for b in blocks if b["type"] in ("table", "box")] == ["table"] * 2


def test_every_highlight_and_row_reaches_the_tab():
    _date, text = r.build()
    source = r.REGISTER.read_text(encoding="utf-8")
    assert text.count("<mark>") == source.count("<mark>")
    rows = [line for line in source.splitlines() if line.startswith("| ")]
    assert all(row in text for row in rows)


def test_page_marker_and_no_repo_references():
    _date, text = r.build()
    assert text.count("@@PAGE ") == 1
    assert "scope package" not in text and ".md" not in text
    assert "<br" not in text


def test_date_is_the_forms_date_prepared():
    date, _text = r.build()
    assert re.fullmatch(r"\d{1,2} [A-Z][a-z]+ \d{4}", date)
