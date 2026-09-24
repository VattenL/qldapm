"""Unit tests for the Doc payload transform and the unit split."""

import pathlib
import re
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


class TestOutlineBlock(unittest.TestCase):
    def setUp(self):
        self.block = scope_tab3.outline_block(OUTLINE)
        self.items = gdoc_edit.parse_blocks(self.block)[0]["items"]

    def test_is_one_outline_block_for_the_doc_writer(self):
        blocks = gdoc_edit.parse_blocks(self.block)
        self.assertEqual([b["type"] for b in blocks], ["outline"])

    def test_one_line_per_element_and_blank_lines_dropped(self):
        self.assertEqual(len(self.items), 7)

    def test_depth_follows_the_code(self):
        self.assertEqual([d for d, _ in self.items], [0, 1, 2, 3, 1, 2, 3])

    def test_padding_is_collapsed_and_annotation_kept(self):
        self.assertEqual(self.items[4][1], "1.2  Requirements (major deliverable, D1, M1)")

    def test_control_account_marker_is_spelled_out(self):
        self.assertEqual(self.items[2][1], "1.1.1  Project Governance (control account)")


class TestFrontSection(unittest.TestCase):
    MD = "### Keep\n\nBody line one\nline two.\n\n- item one\n  continued\n- item two\n\n### Next\n\nNo."

    def test_stops_at_the_next_heading(self):
        body = scope_tab3.front_section(self.MD, "### Keep")
        self.assertIn("line two.", body)
        self.assertNotIn("No.", body)

    def test_list_continuations_join_their_item(self):
        body = scope_tab3.front_section(self.MD, "### Keep")
        self.assertIn("- item one continued", body)
        items = [b for b in gdoc_edit.parse_blocks(body) if b["type"] == "bullets"][0]["items"]
        self.assertEqual(items, ["item one continued", "item two"])


class TestSplitFieldLines(unittest.TestCase):
    def test_separates_the_two_form_fields(self):
        out = scope_tab3.split_field_lines("**Project Title:** X\n**Date Prepared:** Y\n")
        self.assertEqual(out, "**Project Title:** X\n\n**Date Prepared:** Y\n")

    def test_survives_the_doc_parser_as_two_paragraphs(self):
        md = scope_tab3.split_field_lines("**Project Title:** X\n**Date Prepared:** Y\n")
        blocks = gdoc_edit.parse_blocks(md)
        self.assertEqual([b["type"] for b in blocks], ["para", "para"])


class TestStripItalicNotes(unittest.TestCase):
    def test_drops_a_wholly_italic_paragraph(self):
        md = "keep me\n\n*Form 2.7, page 1 of 2.*\n\nkeep me too"
        out = scope_tab3.strip_italic_notes(md)
        self.assertNotIn("Form 2.7", out)
        self.assertIn("keep me", out)
        self.assertIn("keep me too", out)

    def test_drops_one_wrapped_across_lines(self):
        md = "*Form 2.10, one sheet per work package.\nAll fourteen printed fields appear.*\n\nbody"
        self.assertEqual(scope_tab3.strip_italic_notes(md).strip(), "body")

    def test_drops_page_marker_glued_to_the_next_heading(self):
        md = "| a | b |\n\n*Page 1 of 1*\n#### 1.1.1.2 Next sheet\n"
        out = scope_tab3.strip_italic_notes(md)
        self.assertNotIn("Page 1 of 1", out)
        self.assertIn("#### 1.1.1.2 Next sheet", out)

    def test_keeps_prose_that_merely_contains_emphasis(self):
        md = "The structure is decomposed **top-down**, not bottom-up."
        self.assertEqual(scope_tab3.strip_italic_notes(md).strip(), md)

    def test_keeps_a_bold_only_paragraph(self):
        md = "**What the hours mean.** The column is an estimate."
        self.assertEqual(scope_tab3.strip_italic_notes(md).strip(), md)

    def test_leaves_table_rows_alone(self):
        md = "| *a* | b |\n| --- | --- |\n| c | d |"
        self.assertEqual(scope_tab3.strip_italic_notes(md).strip(), md)

    def test_payload_has_no_italic_paragraph_left(self):
        payload = scope_tab3.build(SOURCE.read_text(encoding="utf-8"))
        paras = [b["text"] for b in gdoc_edit.parse_blocks(payload) if b["type"] == "para"]
        italic = [s for s in paras if s.startswith("*") and not s.startswith("**")]
        self.assertEqual(italic, [])
        self.assertNotIn("Page 1 of 1", payload)


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

    def test_repository_front_matter_is_gone(self):
        for dropped in ("How this document is organised", "second deliverable of the coursework"):
            self.assertNotIn(dropped, self.payload)

    def test_report_front_matter_is_kept(self):
        # Audit E9: the Doc lacked the legend, the Validate Scope note, and the method with its
        # sizing rule, which the dictionary sheets cite.
        for kept in ("#### Reading convention", "#### What this section is not", "Validate Scope (5.5)",
                     "**Top-down.**", "**Work package sizing.**", "between 8 and 80 hours"):
            self.assertIn(kept, self.payload)

    def test_method_states_the_level_the_outline_uses(self):
        self.assertIn("level 2 holds here: the ten major deliverables", self.payload)
        self.assertNotIn("Level 2 is the phase", self.payload)

    def test_wbs_is_an_outline_not_a_table(self):
        # Audit E8: form 2.9 prints an indented numbered outline.
        blocks = gdoc_edit.parse_blocks(self.payload)
        outlines = [b for b in blocks if b["type"] == "outline"]
        self.assertEqual(len(outlines), 1)
        self.assertEqual(outlines[0]["items"][0][0], 0)
        self.assertNotIn("| Code | Element | Type | Delivers |", self.payload)

    def test_structure_heading_precedes_its_form_fields(self):
        at = self.payload.index("#### 3.2.2 The structure")
        self.assertLess(at, self.payload.index("**Project Title:**", at))
        self.assertLess(self.payload.index("**Project Title:**", at), self.payload.index("```outline"))

    def test_starts_at_the_doc_section_heading(self):
        self.assertTrue(self.payload.startswith("## 3: Scope Baseline"))

    def test_method_is_folded_into_the_wbs_section(self):
        self.assertIn("#### 3.2.1 Inputs and method", self.payload)
        self.assertLess(self.payload.index("### 3.2 Work Breakdown Structure"),
                        self.payload.index("#### 3.2.1 Inputs and method"))

    def test_no_repo_paths_or_part_references_survive(self):
        for leaked in ("charter-package.en.md", "docs/", "Part 1", "Part 2", "Part 3"):
            self.assertNotIn(leaked, self.payload)

    def test_every_sheet_of_the_source_is_present(self):
        source = SOURCE.read_text(encoding="utf-8")
        in_source = len(re.findall(r"^#### 1(?:\.\d+){3} ", source, re.M))
        self.assertGreater(in_source, 0)
        self.assertEqual(len(gdoc_tab3.SHEET_HEADING.findall(self.payload)), in_source)

    def test_parses_cleanly_for_the_doc_writer(self):
        blocks = gdoc_edit.parse_blocks(self.payload)
        tables = [b for b in blocks if b["type"] == "table"]
        source = SOURCE.read_text(encoding="utf-8")
        body = source[source.index(scope_tab3.START):]
        body_tables = sum(1 for b in gdoc_edit.parse_blocks(body) if b["type"] == "table")
        # The transform adds the inputs table from the front matter, renders the WBS as an outline
        # rather than a table, and loses none of the body's own tables.
        self.assertEqual(len(tables), body_tables + 1)
        for b in tables:
            self.assertEqual(len({len(r) for r in b["rows"]}), 1, b["rows"][0][:2])

    def test_highlight_spans_are_balanced(self):
        self.assertEqual(self.payload.count("<mark>"), self.payload.count("</mark>"))


class TestSplitUnits(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = scope_tab3.build(SOURCE.read_text(encoding="utf-8"))
        cls.units = gdoc_tab3.split_units(cls.payload)

    def test_one_unit_per_opening_section_plus_one_per_sheet(self):
        sheets = len(gdoc_tab3.SHEET_HEADING.findall(self.payload))
        self.assertEqual(len(self.units), len(gdoc_tab3.OPENING) + sheets)

    def test_opening_units_follow_the_declared_order_and_orientation(self):
        opening = self.units[:len(gdoc_tab3.OPENING)]
        self.assertEqual([u[0] for u in opening], [o[0] for o in gdoc_tab3.OPENING])
        self.assertEqual([u[3] for u in opening], [o[2] for o in gdoc_tab3.OPENING])

    def test_the_lead_carries_no_table(self):
        _name, anchor, chunk, landscape = self.units[0]
        self.assertEqual(anchor, "3: Scope Baseline")
        self.assertFalse(landscape)
        self.assertNotIn("|", chunk)

    def test_the_wide_matrices_are_landscape_and_hold_both_tables(self):
        name, _anchor, chunk, landscape = self.units[1]
        self.assertEqual(name, "3.1 matrices")
        self.assertTrue(landscape)
        self.assertIn("| ID | Requirement | Source |", chunk)
        self.assertIn("Inter-requirements traceability matrix", chunk)

    def test_the_outline_section_is_landscape(self):
        name, _anchor, _chunk, landscape = self.units[2]
        self.assertEqual(name, "3.2 method and structure")
        self.assertTrue(landscape)

    def test_only_the_narrow_sections_stay_portrait(self):
        portrait = [o[0] for o in gdoc_tab3.OPENING if not o[2]]
        self.assertEqual(portrait, ["lead", "3.2.4 coverage"])

    def test_every_sheet_unit_is_landscape(self):
        for name, _anchor, _chunk, landscape in self.units[len(gdoc_tab3.OPENING):]:
            self.assertTrue(landscape, name)

    def test_each_phase_heading_is_carried_by_its_first_sheet(self):
        carried = [c for _n, _a, c, _l in self.units if c.startswith("#### 3.3.")]
        self.assertEqual(len(carried), 10)

    def test_anchors_are_whole_headings_not_bare_codes(self):
        _name, anchor, _chunk, _l = self.units[len(gdoc_tab3.OPENING)]
        self.assertRegex(anchor, r"^1(\.\d+){3} \S")

    def test_units_reassemble_into_the_payload(self):
        joined = "".join(c for _n, _a, c, _l in self.units)
        self.assertEqual(joined.split(), self.payload.split())


class TestApplyLayoutRouting(unittest.TestCase):
    def test_widths_match_the_column_counts_they_are_for(self):
        self.assertEqual(len(gdoc_tab3.RTM_WIDTHS), 9)
        self.assertEqual(len(gdoc_tab3.INTER_WIDTHS), 8)
        self.assertEqual(len(gdoc_tab3.ACTIVITY_WIDTHS), 10)

    def test_widths_fit_a_landscape_page(self):
        for widths in (gdoc_tab3.RTM_WIDTHS, gdoc_tab3.INTER_WIDTHS,
                       gdoc_tab3.ACTIVITY_WIDTHS):
            self.assertLessEqual(sum(widths), 698, widths)

    def test_rtm_groups_cover_every_column_exactly_once(self):
        covered = []
        for _label, start, span in gdoc_tab3.RTM_GROUPS:
            covered.extend(range(start, start + span))
        self.assertEqual(covered, list(range(9)))


if __name__ == "__main__":
    unittest.main()
