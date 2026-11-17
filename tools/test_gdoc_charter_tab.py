"""The charter tab payload keeps Parts 1 and 2 of the source and lays form 1.1 out as printed."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc_edit as ge
import gdoc_charter_tab as c

SOURCE = c.SOURCE.read_text(encoding="utf-8")
PARTS = SOURCE[SOURCE.index("## Part 1"):SOURCE.index("## Part 3")]
TEXT = c.build()


def tables(text):
    return [b for b in ge.parse_blocks(text) if b["type"] == "table"]


def form_tables():
    return tables(TEXT[TEXT.index("### " + c.H_FORM):])


def test_headings_follow_the_other_tabs():
    heads = re.findall(r"^(#{2,3}) (.+)$", TEXT, re.M)
    assert heads[0] == ("##", c.H_PART1)
    assert ("##", c.H_PART2) in heads and ("###", c.H_ELEMENTS) in heads and ("###", c.H_FORM) in heads
    assert TEXT.count("#### Reading convention") == 3
    assert "2A." not in TEXT and "2B." not in TEXT and "page 1 of 4" not in TEXT


def test_every_highlight_of_parts_1_and_2_reaches_the_tab():
    # Two highlights come with the reading conventions ("highlighted" explained twice and 5 July 2027
    # moved from the note under the milestones), and the Approvals note with its one highlight goes.
    moved_out = SOURCE[SOURCE.index("The printed form carries a signature"):].split("\n", 1)[0]
    milestone_note = re.search(r"^M6 to M7 is the first month of the six-month warranty.*$", PARTS, re.M).group(0)
    expected = PARTS.count("<mark>") - moved_out.count("<mark>") - milestone_note.count("<mark>") + 3
    assert TEXT.count("<mark>") == expected


def test_every_table_row_outside_the_form_is_copied():
    outside = PARTS[:PARTS.index("### 2B.")]
    for old, new in c.REWRITES:
        outside = outside.replace(old, new)
    rows = [r for r in outside.splitlines() if r.startswith("| ") and not set(r) <= set("|- ")]
    assert all(r in TEXT for r in rows)


def test_form_is_four_printed_pages_of_two_columns():
    found = form_tables()
    assert len(found) == c.PAGES
    assert all(len(row) == 2 for t in found for row in t["rows"])
    assert [TEXT.count("@@PAGE Page %d of 4@@" % n) for n in range(1, 5)] == [1, 1, 1, 1]


def test_form_labels_in_printed_order():
    labels = ["Project Title:", "Project Sponsor:", "Date Prepared:", "Project Manager:", "Project Customer:",
              "Project Purpose:", "High-Level Project Description:", "Project Boundaries:", "Key Deliverables:",
              "High-Level Requirements:", "Overall Project Risk", "Project Objectives", "Success Criteria",
              "Scope:", "Time:", "Cost:", "Other:", "Summary Milestones", "Due Date",
              "Preapproved Financial Resources:", "Stakeholder(s)", "Role", "Project Exit Criteria:",
              "Project Manager Authority Level:", "Staffing Decisions:", "Budget Management and Variance:",
              "Technical Decisions:", "Conflict Resolution:", "Sponsor Authority:", "Approvals:",
              "Project Manager Signature", "Sponsor or Originator Signature", "Project Manager Name",
              "Sponsor or Originator Name", "Date**"]
    form = TEXT[TEXT.index("### " + c.H_FORM):]
    at = [form.index("**%s" % label) for label in labels]
    assert at == sorted(at)


def test_pairing_and_empty_boxes():
    page1 = form_tables()[0]["rows"]
    assert page1[1][0].startswith("**Project Sponsor:**") and page1[1][1].startswith("**Date Prepared:**")
    assert page1[2][0] == "**Project Manager:**" and page1[2][1].startswith("**Project Customer:**")
    approvals = form_tables()[3]["rows"][-6:]
    assert approvals[0] == ["", ""] and approvals[4] == ["", ""]
    assert approvals[2][0] == "" and "Nguyễn Mạnh Hùng" in approvals[2][1]


def test_known_drift_is_gone():
    assert "Iteration 2 release, F06 to F12" in TEXT and "F06 to F11" not in TEXT
    assert "Owner and project sponsor" not in TEXT
    assert "management reserve" not in TEXT


def test_reading_conventions_are_short():
    for para in (c.READING_1, c.READING_21, c.READING_22):
        assert len(para.split()) <= 150


def test_widths_fit_a_portrait_page():
    assert all(sum(w) == 468 for w in c.WIDTHS.values())
    assert sum(c.FORM_WIDTHS) == 468
    heads = {tuple(ge.parse_inline(cell)[0] for cell in t["rows"][0]) for t in tables(TEXT[:TEXT.index("### " + c.H_FORM)])}
    assert heads <= set(c.WIDTHS)
