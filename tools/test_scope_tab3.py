"""Unit tests for the Doc payload transform and the unit split."""

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc_edit
import gdoc_tab3
import scope_tab3

SOURCE = pathlib.Path(__file__).resolve().parent.parent / "docs" / "scope-package.en.md"

OUTLINE = """1.        Learning Center Management Software

1.1       Project Management                                          (major deliverable)
1.1.1       Project Governance                                        CA
1.1.1.1       Kickoff and team mobilisation

1.2       Requirements                                                (major deliverable, D1, M1)
1.2.1       Elicitation                                               CA
1.2.1.1       Stakeholder workshops
"""


class TestClassify(unittest.TestCase):
    def test_project(self):
        self.assertEqual(scope_tab3.classify("1", "Learning Center Management Software"),
                         ("Learning Center Management Software", "Project", ""))

    def test_major_deliverable_keeps_only_what_it_delivers(self):
        self.assertEqual(scope_tab3.classify("1.2", "Requirements (major deliverable, D1, M1)"),
                         ("Requirements", "Major deliverable", "D1, M1"))

    def test_control_account_flag_is_stripped_from_the_name(self):
        self.assertEqual(scope_tab3.classify("1.1.1", "Project Governance CA"),
                         ("Project Governance", "Control account", ""))

    def test_work_package(self):
        self.assertEqual(scope_tab3.classify("1.1.1.1", "Kickoff and team mobilisation"),
                         ("Kickoff and team mobilisation", "Work package", ""))


class TestOutlineToTable(unittest.TestCase):
    def setUp(self):
        self.rows = scope_tab3.outline_to_table(OUTLINE).splitlines()

    def test_header_and_row_count(self):
        self.assertEqual(self.rows[0], "| Code | Element | Type | Delivers |")
        self.assertEqual(len(self.rows), 2 + 7)

    def test_every_row_has_four_columns(self):
        for row in self.rows[2:]:
            self.assertEqual(len(gdoc_edit._split_row(row)), 4, row)

    def test_blank_lines_are_dropped(self):
        self.assertNotIn("|  |  |  |  |", self.rows)


class TestSplitFieldLines(unittest.TestCase):
    def test_separates_the_two_form_fields(self):
        out = scope_tab3.split_field_lines("**Project Title:** X\n**Date Prepared:** Y\n")
        self.assertEqual(out, "**Project Title:** X\n\n**Date Prepared:** Y\n")

    def test_survives_the_doc_parser_as_two_paragraphs(self):
        md = scope_tab3.split_field_lines("**Project Title:** X\n**Date Prepared:** Y\n")
        blocks = gdoc_edit.parse_blocks(md)
        self.assertEqual([b["type"] for b in blocks], ["para", "para"])


class TestRenumber(unittest.TestCase):
    def test_sheet_headings_drop_a_level(self):
        self.assertEqual(scope_tab3.renumber("#### 1.1.1.1 Kickoff"), "##### 1.1.1.1 Kickoff")

    def test_phase_headings_are_numbered_in_order(self):
        out = scope_tab3.renumber("### Phase 1.1 A\n### Phase 1.2 B")
        self.assertEqual(out.splitlines(), ["#### 3.3.1 Phase 1.1 A", "#### 3.3.2 Phase 1.2 B"])

    def test_section_headings_are_not_treated_as_sheets(self):
        out = scope_tab3.renumber("#### 3.1.1 Requirement information")
        self.assertEqual(out, "#### 3.1.1 Requirement information")


class TestBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = scope_tab3.build(SOURCE.read_text(encoding="utf-8"))

    def test_front_matter_is_gone(self):
        for dropped in ("How this document is organised", "Reading convention", "Decomposition method"):
            self.assertNotIn(dropped, self.payload)

    def test_starts_at_the_doc_section_heading(self):
        self.assertTrue(self.payload.startswith("## 3: Scope Baseline"))

    def test_method_is_folded_into_the_wbs_section(self):
        self.assertIn("#### 3.2.1 Inputs and method", self.payload)
        self.assertLess(self.payload.index("### 3.2 Work Breakdown Structure"),
                        self.payload.index("#### 3.2.1 Inputs and method"))

    def test_no_repo_paths_or_part_references_survive(self):
        for leaked in ("charter-package.en.md", "docs/", "Part 1", "Part 2", "Part 3"):
            self.assertNotIn(leaked, self.payload)

    def test_every_sheet_is_present(self):
        self.assertEqual(len(gdoc_tab3.SHEET_HEADING.findall(self.payload)), 71)

    def test_parses_cleanly_for_the_doc_writer(self):
        blocks = gdoc_edit.parse_blocks(self.payload)
        tables = [b for b in blocks if b["type"] == "table"]
        self.assertEqual(len(tables), 218)
        for b in tables:
            self.assertEqual(len({len(r) for r in b["rows"]}), 1, b["rows"][0][:2])

    def test_highlight_spans_are_balanced(self):
        self.assertEqual(self.payload.count("<mark>"), self.payload.count("</mark>"))


class TestSplitUnits(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.units = gdoc_tab3.split_units(scope_tab3.build(SOURCE.read_text(encoding="utf-8")))

    def test_one_opening_unit_plus_one_per_sheet(self):
        self.assertEqual(len(self.units), 72)

    def test_opening_unit_holds_the_matrix_and_the_structure(self):
        name, anchor, chunk = self.units[0]
        self.assertEqual(anchor, "3: Scope Baseline")
        self.assertIn("### 3.1 Requirements Traceability Matrix", chunk)
        self.assertIn("#### 3.2.2 The structure", chunk)
        self.assertNotIn("##### 1.1.1.1", chunk)

    def test_each_phase_heading_is_carried_by_its_first_sheet(self):
        carried = [c for _n, _a, c in self.units if c.startswith("#### 3.3.")]
        self.assertEqual(len(carried), 10)

    def test_anchors_are_whole_headings_not_bare_codes(self):
        _name, anchor, _chunk = self.units[1]
        self.assertEqual(anchor, "1.1.1.1 Kickoff and team mobilisation")

    def test_units_reassemble_into_the_payload(self):
        joined = "".join(c for _n, _a, c in self.units)
        payload = scope_tab3.build(SOURCE.read_text(encoding="utf-8"))
        self.assertEqual(joined.split(), payload.split())


if __name__ == "__main__":
    unittest.main()
