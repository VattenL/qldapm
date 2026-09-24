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


class Consistency(unittest.TestCase):
    """Each case is a finding the reviewers actually made on this project."""

    def run_on(self, text, **names):
        import check_consistency as cc
        lines = list(cc.lines_outside_code(text))
        files = [("doc.md", lines)]
        sponsor, customer = cc.people(files)
        sponsor, customer = names.get("sponsor", sponsor), names.get("customer", customer)
        out, id_values = [], __import__("collections").defaultdict(list)
        cc.check_markup("doc.md", lines, out)
        cc.check_dates("doc.md", lines, out)
        cc.check_ranges("doc.md", lines, cc.definitions(files), out)
        cc.check_section_refs("doc.md", lines, out)
        cc.check_tables("doc.md", lines, out, id_values)
        cc.check_roles("doc.md", lines, sponsor, customer, out)
        cc.check_approvals("doc.md", text, lines, out)
        cc.report_id_conflicts(id_values, out)
        return {f.check for f in out}

    CHARTER = "\n".join([
        "| Field | Content |", "| --- | --- |",
        "| **Project Sponsor** | <mark>Dr. Nguyễn Mạnh Hùng</mark> |",
        "| **Project Customer** | <mark>Đỗ Thị Bích Ngọc, owner and Director of the learning center</mark> |",
        "",
    ])

    def test_leading_zero_and_short_month(self):
        self.assertIn("date", self.run_on("Prepared 02 September 2026."))
        self.assertIn("date", self.run_on("Go-live 5 Jan 2027."))
        self.assertNotIn("date", self.run_on("Go-live 5 January 2027."))

    def test_br_is_not_converted(self):
        self.assertIn("html", self.run_on("| 1.1 | first<br>second |"))
        self.assertNotIn("html", self.run_on("| 1.1 | <mark>assumed</mark> |"))
        self.assertNotIn("html", self.run_on("It dropped the `<div>` wrappers."))

    def test_highlighted_label(self):
        self.assertIn("mark-on-label", self.run_on("| **<mark>Project Customer</mark>** | x |"))
        self.assertNotIn("mark-on-label", self.run_on("**Sponsor:** <mark>Dr. Nguyễn Mạnh Hùng</mark>"))

    def test_stale_range(self):
        register = "\n".join("| R%d | risk |" % i for i in range(1, 13))
        text = "| ID | Risk |\n| --- | --- |\n" + register + "\n\nRisks R1 to R10 carry responses."
        self.assertIn("range", self.run_on(text))
        self.assertNotIn("range", self.run_on(text.replace("R1 to R10", "R1 to R12")))

    def test_iteration_subrange_is_not_stale(self):
        register = "\n".join("| F%02d | f |" % i for i in range(1, 13))
        text = "| ID | Function |\n| --- | --- |\n" + register + "\n\nIteration 1 builds F01 to F05."
        self.assertNotIn("range", self.run_on(text))

    def test_dangling_section(self):
        self.assertIn("section-ref", self.run_on("## 1.1 Scope\n\nBusiness case in section 2A."))
        self.assertNotIn("section-ref", self.run_on("### 2A. Charter elements\n\nSee section 2A."))
        self.assertNotIn("section-ref", self.run_on("As PMBOK 6 section 4.1.3.1 says."))

    def test_totals_with_subtotal(self):
        table = "\n".join([
            "| | Amount |", "| --- | ---: |",
            "| PM | 130 |", "| Devs | 285 |", "| **Labor total** | **415** |",
            "| Other | 85 |", "| **Total** | **500** |"])
        self.assertNotIn("total", self.run_on(table))
        self.assertIn("total", self.run_on(table.replace("**500**", "**700**")))

    def test_sponsor_described_as_owner(self):
        bad = self.CHARTER + "\n| Dr. Nguyễn Mạnh Hùng, owner and Center Director | Customer |"
        self.assertIn("role-merge", self.run_on(bad))
        self.assertIn("role-merge", self.run_on("| NFR01 | Center Director, sponsor |"))
        good = self.CHARTER + "\n| Dr. Nguyễn Mạnh Hùng | Sponsor: releases the funding |"
        self.assertNotIn("role-merge", self.run_on(good))

    def test_approvals_has_two_columns(self):
        three = "PROJECT CHARTER\n\n**Approvals**\n\n| | Sponsor | Project Manager | Customer |\n| --- | --- | --- | --- |"
        self.assertIn("approvals", self.run_on(three))
        two = "PROJECT CHARTER\n\n**Approvals**\n\n| | Project Manager | Sponsor or Originator |\n| --- | --- | --- |"
        self.assertNotIn("approvals", self.run_on(two))

    def test_same_id_different_source(self):
        text = "\n".join([
            "| ID | Source |", "| --- | --- |", "| BR03 | Accountant, Center Director |", "",
            "| ID | Source |", "| --- | --- |", "| BR03 | Accountant |"])
        self.assertIn("id-conflict", self.run_on(text))

    def test_uniform_priority(self):
        rows = "\n".join("| FR%02d | Must have |" % i for i in range(1, 10))
        self.assertIn("uniform-column", self.run_on("| ID | Priority |\n| --- | --- |\n" + rows))


if __name__ == "__main__":
    unittest.main()
