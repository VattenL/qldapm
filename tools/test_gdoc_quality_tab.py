"""The quality tab payload keeps the form's content and loses only what the Doc lays out itself."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc_edit as ge
import gdoc_quality_tab as q


def test_payload_has_the_five_printed_boxes_without_their_markdown_headers():
    _date, text = q.build()
    tables = [b for b in ge.parse_blocks(text) if b["type"] == "table"]
    assert len(tables) == len(q.WIDTHS)
    assert "| Field | Content |" not in text
    for caption in q.CAPTIONS:
        assert "**%s**" % caption not in text


def test_every_highlight_of_the_source_reaches_the_tab():
    _date, text = q.build()
    source = q.SOURCE.read_text(encoding="utf-8")
    assert text.count("<mark>") == source.count("<mark>")


def test_page_markers_and_no_repo_references():
    _date, text = q.build()
    assert text.count("@@PAGE ") == 2
    assert "scope package" not in text
    assert "`" not in text


def test_date_is_the_forms_date_prepared():
    date, _text = q.build()
    assert re.fullmatch(r"\d{1,2} [A-Z][a-z]+ \d{4}", date)
