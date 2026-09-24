"""Tests for the pm skill helpers. Run: python3 -m unittest discover -s .claude/skills/pm/scripts"""

import unittest
from pathlib import Path

import check_fidelity
import extract_form


class Index(unittest.TestCase):
    def setUp(self):
        self.forms = extract_form.load_index()

    def test_every_form_is_listed(self):
        self.assertEqual(len(self.forms), 66)
        for group, last in (("1", 4), ("2", 40), ("3", 7), ("4", 9), ("5", 2), ("6", 4)):
            for n in range(1, last + 1):
                self.assertIn(f"{group}.{n}", self.forms)

    def test_page_ranges_are_sane(self):
        for form in self.forms.values():
            prose, blank = form["prose"], form["blank"]
            self.assertLessEqual(prose[0], prose[1], form["num"])
            self.assertLessEqual(blank[0], blank[1], form["num"])
            self.assertLess(prose[1], blank[0], form["num"])

    def test_kinds_are_known(self):
        known = {"fields", "log", "matrix", "chart", "diagram", "outline", "narrative"}
        self.assertEqual({f["kind"] for f in self.forms.values()} - known, set())

    def test_lookup_by_name(self):
        self.assertEqual(extract_form.resolve(self.forms, "retrospective")["num"], "6.4")
        self.assertEqual(extract_form.resolve(self.forms, "2.32")["num"], "2.32")


class SliceSection(unittest.TestCase):
    PROSE = "\n".join([
        "2.9 WORK BREAKDOWN STRUCTURE", "Some purpose text.",
        "tailoring tips", "  - Roll up to deliverables.",
        "Alignment", "  - Scope statement",
        "Description", "Document element   Description", "Level   The WBS level",
    ])

    def test_picks_the_named_section(self):
        self.assertIn("Roll up", extract_form.slice_section(self.PROSE, "tailoring tips"))
        self.assertIn("Scope statement", extract_form.slice_section(self.PROSE, "alignment"))
        self.assertIn("The WBS level", extract_form.slice_section(self.PROSE, "description"))

    def test_sections_do_not_bleed_into_each_other(self):
        self.assertNotIn("Scope statement", extract_form.slice_section(self.PROSE, "tailoring tips"))

    def test_absent_section_is_empty(self):
        self.assertEqual(extract_form.slice_section("nothing here", "alignment"), "")


class Locate(unittest.TestCase):
    def test_bold_label_wins_over_prose_mention(self):
        body = "the cost of delay matters. | **cost** | 700m |"
        self.assertGreater(check_fidelity.locate(body, "Cost"), 20)

    def test_word_boundary(self):
        self.assertEqual(check_fidelity.locate("classification scheme", "class"), -1)

    def test_absent(self):
        self.assertEqual(check_fidelity.locate("nothing", "Risk Owner"), -1)


class KeyValues(unittest.TestCase):
    def test_header_block_splits_into_lines(self):
        import md_to_docx
        text = "**Project:** Learning Center **Date prepared:** 24 September 2026"
        self.assertEqual(len(md_to_docx.split_key_values(text)), 2)

    def test_plain_paragraph_is_left_alone(self):
        import md_to_docx
        text = "This paragraph mentions **bold** words but is not a header block."
        self.assertEqual(md_to_docx.split_key_values(text), [text])


if __name__ == "__main__":
    unittest.main()
