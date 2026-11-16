"""The risk tab payload keeps the register's content and loses only what the Doc lays out itself."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc_edit as ge
import gdoc_risk_tab as r


def tables(text):
    return [b for b in ge.parse_blocks(text) if b["type"] == "table"]


def test_payload_has_its_tables_and_both_banks():
    _date, text, _changed = r.build()
    assert len(tables(text)) == len(r.WIDTHS)
    banks = tables(text)[-r.BANKS:]
    assert [len(t["rows"][0]) for t in banks] == [len(w) for w in r.WIDTHS[-r.BANKS:]]
    assert len(banks[0]["rows"]) == len(banks[1]["rows"])


def test_widths_fill_the_landscape_page():
    assert all(sum(w) <= 648 for w in r.WIDTHS)
    assert [sum(w) for w in r.WIDTHS[-r.BANKS:]] == [648, 648]


def test_every_highlight_and_row_reaches_the_tab():
    _date, text, _changed = r.build()
    source = r.REGISTER.read_text(encoding="utf-8")
    assert text.count("<mark>") == source.count("<mark>")
    rows = [r.INS.sub("", line) for line in source.splitlines()
            if line.startswith("| ") and r.GROUP not in line]
    assert all(row in text for row in rows)


def test_banks_print_the_two_tier_header():
    _date, text, _changed = r.build()
    for bank, first in zip(tables(text)[-r.BANKS:], r.IMPACT):
        top, under = bank["rows"][0], bank["rows"][1]
        assert top[first:first + 4] == ["Impact", "", "", ""]
        assert under[first:first + 4] == ["**Scope**", "**Quality**", "**Schedule**", "**Cost**"]
        assert all(not c for k, c in enumerate(under) if not first <= k < first + 4)


def test_changed_cells_are_shaded_not_printed():
    _date, text, changed = r.build()
    source = r.REGISTER.read_text(encoding="utf-8")
    assert "<ins>" not in text
    banks = source.split("**Date Prepared:**", 1)[1]
    assert sum(len(c) for c in changed) == banks.count("<ins>")
    assert all(row >= 2 for bank in changed for row, _col in bank)


def test_page_marker_and_no_repo_references():
    _date, text, _changed = r.build()
    assert text.count("@@PAGE ") == 1
    assert "scope package" not in text and ".md" not in text
    assert "<br" not in text


def test_date_is_the_forms_date_prepared():
    date, _text, _changed = r.build()
    assert re.fullmatch(r"\d{1,2} [A-Z][a-z]+ \d{4}", date)
