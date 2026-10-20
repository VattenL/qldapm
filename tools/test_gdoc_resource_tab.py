"""The resource tab payload keeps the three forms' content and loses only what the Doc lays out itself."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc_edit as ge
import gdoc_resource_tab as r


def test_payload_has_the_printed_tables_without_their_markdown_headers():
    _date, text = r.build()
    blocks = ge.parse_blocks(text)
    assert [b["type"] for b in blocks if b["type"] in ("table", "box")] == ["table"] * 4 + ["box"]
    assert "| Field | Content |" not in text


def test_every_highlight_of_the_sources_reaches_the_tab():
    _date, text = r.build()
    sources = [p.read_text(encoding="utf-8") for p in (r.CHARTER, r.REQUIREMENTS, r.STRUCTURE)]
    assert text.count("<mark>") == sum(s.count("<mark>") for s in sources)


def test_every_register_row_and_outline_item_reaches_the_tab():
    _date, text = r.build()
    source = r.REQUIREMENTS.read_text(encoding="utf-8")
    rows = [line for line in source.splitlines() if line.startswith("| ")]
    assert all(row in text for row in rows if "Quantity" not in row)
    outline = r.outline_of(r.STRUCTURE.read_text(encoding="utf-8"))
    items = [m for m in re.findall(r"^ *\d+\. ", r.STRUCTURE.read_text(encoding="utf-8"), re.M)]
    assert len(outline) == len(items)
    assert outline[0].startswith("1.  ") and outline[1].startswith("  1.1.  ")


def test_page_markers_and_no_repo_references():
    _date, text = r.build()
    assert text.count("@@PAGE ") == 3
    assert "scope package" not in text and ".md" not in text
    assert "<br" not in text


def test_date_is_the_forms_date_prepared():
    date, _text = r.build()
    assert re.fullmatch(r"\d{1,2} [A-Z][a-z]+ \d{4}", date)
