"""Tests for check_fidelity.py. Run: python3 -m unittest discover -s .claude/skills/pm/scripts

fixtures/fidelity/broken-2-32.md is the risk register from the iteration-1
review that flattened the Impact group, swapped Owner and Probability and lost
the Status column. The documents under docs/ are checked when present.
"""

import contextlib
import io
import json
import unittest
from pathlib import Path

import check_fidelity as cf

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures" / "fidelity"
DOCS = HERE.parents[3] / "docs"


def spec(form):
    return cf.load_spec(form)


def run_main(*argv):
    """Exit code and printed lines of the command line."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            code = cf.main([str(a) for a in argv])
        except SystemExit as stop:
            code = stop.code
    return code, buf.getvalue().splitlines()


def table(header, rows=()):
    lines = ["| " + " | ".join(header) + " |", "|" + " --- |" * len(header)]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines) + "\n\n"


def render(form):
    """A blank form written by the shapes of references/rendering.md."""
    out = ["# %s %s\n" % (form["form"], form["name"])]
    for where, slots in cf.blocks(form):
        header = [s.text for s in slots if s.shape == "header"]
        rows = [s.text for s in slots if s.shape == "row"]
        fields = [s.text for s in slots if s.shape == "field"]
        for s in slots:
            if s.shape == "title":
                out.append("**%s:** \n" % s.text)
            elif s.shape in ("bold", "caption"):
                out.append("\n**%s**\n\n" % s.text)
            elif s.shape == "checklabel":
                out.append("\n**%s:**\n\n" % s.text)
            elif s.shape == "option":
                out.append("- [ ] %s\n" % s.text)
        if fields:
            out.append("\n" + table(["Field", "Content"], [["**%s**" % f, ""] for f in fields]))
        if header or rows:
            corner = [""] if rows else []
            out.append("\n" + table(corner + header, [["**%s**" % r] + [""] * len(header) for r in rows]))
    return "".join(out)


class Expected(unittest.TestCase):
    def test_grouped_columns_carry_the_group(self):
        labels = [s.text for s in cf.expected(spec("2.32"))]
        self.assertEqual(labels.count("Impact: Scope"), 2)
        self.assertNotIn("Impact", labels)

    def test_both_banks_are_expected(self):
        labels = [s.text for s in cf.expected(spec("2.32"))]
        self.assertIn("Revised Probability", labels)
        self.assertEqual(labels[-1], "Comments")

    def test_repeated_labels_are_kept(self):
        labels = [s.text for s in cf.expected(spec("3.3"))]
        self.assertEqual(labels.count("Description"), 6)
        self.assertEqual(labels.count("Increase"), 5)
        page2 = [s.text for s in cf.expected(spec("2.7")) if s.where.startswith("page 2")]
        self.assertEqual(page2.count("ID"), 2)

    def test_full_width_group_is_a_caption(self):
        slots = cf.expected(spec("2.17"))
        self.assertEqual(slots[2].shape, "caption")
        self.assertEqual(slots[2].text, "Parametric Estimates")
        self.assertEqual(slots[3].text, "ID")

    def test_placeholders_and_sentences_are_not_expected(self):
        labels = [s.text for s in cf.expected(spec("2.25"))]
        self.assertEqual(labels, ["Project Title", "Date Prepared"])
        self.assertEqual([s.text for s in cf.expected(spec("6.1"))], ["Project Title", "Date Prepared"])

    def test_title_block_expected_again_where_a_page_repeats_it(self):
        where = [s.where for s in cf.expected(spec("2.31")) if s.text == "Project Title"]
        self.assertEqual(where, ["title block", "page 2, title block"])
        self.assertEqual([s.text for s in cf.expected(spec("2.33"))].count("Project Title"), 1)

    def test_boxless_headings_are_bold_lines(self):
        slots = {s.text: s.shape for s in cf.expected(spec("1.1"))}
        self.assertEqual(slots["Approvals"], "bold")
        self.assertEqual(slots["Project Manager Authority Level"], "bold")

    def test_form_without_title_block(self):
        self.assertEqual([s.text for s in cf.expected(spec("2.18"))][:2], ["ID", "WBS"])

    def test_every_spec_loads_and_has_labels(self):
        for path in sorted(cf.FIELDS.glob("*.json")):
            form = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(cf.blocks(form), path.name)


class RenderedByTheRules(unittest.TestCase):
    def test_every_form_passes_when_written_as_rendering_md_says(self):
        for path in sorted(cf.FIELDS.glob("*.json")):
            form = json.loads(path.read_text(encoding="utf-8"))
            result = cf.check(render(form), form)
            self.assertFalse(result.failed, (form["form"], result.missing, result.disorder))
            self.assertEqual(result.extra, [], form["form"])


class Broken232(unittest.TestCase):
    def setUp(self):
        self.text = (FIXTURES / "broken-2-32.md").read_text(encoding="utf-8")

    def test_fails_from_the_command_line(self):
        code, out = run_main(FIXTURES / "broken-2-32.md", "2.32")
        self.assertEqual(code, 1)
        self.assertIn("missing (9):", out)

    def test_findings(self):
        result = cf.check(self.text, spec("2.32"))
        missing = [(s.where, s.text) for s, _ in result.missing]
        self.assertIn(("page 1, table, bank 1", "Impact: Scope"), missing)
        self.assertIn(("page 1, table, bank 2", "Impact: Cost"), missing)
        self.assertIn(("page 1, table, bank 2", "Status"), missing)
        self.assertEqual([s.text for s, _ in result.disorder], ["Probability"])
        extra = [c.text for c, _ in result.extra]
        self.assertIn("Source", extra)
        self.assertEqual(extra.count("Impact Scope"), 2)

    def test_near_miss_is_named(self):
        result = cf.check(self.text, spec("2.32"))
        notes = dict(((s.where, s.text), n) for s, n in result.missing)
        self.assertEqual(notes[("page 1, table, bank 1", "Impact: Scope")], "written as 'Impact Scope' on line 9")
        self.assertEqual(notes[("page 1, table, bank 2", "Impact: Scope")], "written as 'Impact Scope' on line 24")

    def test_fixed_copy_passes(self):
        text = self.text.replace("| Probability | Owner |", "| Owner | Probability |")
        for area in ("Scope", "Quality", "Schedule", "Cost"):
            text = text.replace("Impact %s" % area, "Impact: %s" % area)
        text = text.replace("| Actions | Comments |", "| Actions | Status | Comments |")
        text = "\n".join(l for l in text.splitlines() if not l.startswith("**Source:**"))
        result = cf.check(text, spec("2.32"))
        self.assertFalse(result.failed, (result.missing, result.disorder))
        self.assertEqual(result.extra, [])


class Positions(unittest.TestCase):
    FORM = {"form": "9.1", "name": "Test", "printed_title": "TEST", "kind": "fields", "page_count": 1,
            "title_block": [], "pages": [{"page": 1, "blocks": [
                {"type": "fields", "labels": ["Cost", "Risk Owner"]}]}]}

    def test_prose_is_never_matched(self):
        md = "# 9.1 Test\n\nThe cost of delay matters and the risk owner signs.\n"
        result = cf.check(md, self.FORM)
        self.assertEqual([s.text for s, _ in result.missing], ["Cost", "Risk Owner"])

    def test_bold_inside_a_content_cell_is_not_a_label(self):
        md = "# 9.1 Test\n\n" + table(["Field", "Content"], [["**Risk Owner**", "**Cost** is high"]])
        result = cf.check(md, self.FORM)
        self.assertEqual([s.text for s, _ in result.missing], ["Cost"])

    def test_order_is_checked(self):
        md = "# 9.1 Test\n\n" + table(["Field", "Content"], [["**Risk Owner**", ""], ["**Cost**", ""]])
        result = cf.check(md, self.FORM)
        self.assertTrue(result.failed)
        self.assertEqual(len(result.disorder), 1)
        self.assertEqual(result.missing, [])

    def test_bold_line_label_and_mark_and_colon(self):
        md = "# 9.1 Test\n\n**Cost:** <mark>12</mark>\n**<mark>Risk Owner</mark>:** x\n"
        self.assertFalse(cf.check(md, self.FORM).failed)

    def test_case_differs_is_missing_with_a_note(self):
        md = "# 9.1 Test\n\n**Cost:** 1\n**Risk owner:** x\n"
        result = cf.check(md, self.FORM)
        self.assertEqual(result.missing[0][1], "written as 'Risk owner' on line 4")

    def test_code_fence_and_italic_paragraph_are_skipped(self):
        md = "# 9.1 Test\n\n*Reading convention.\n**Cost** is explained here.*\n\n```\n**Risk Owner**\n```\n"
        self.assertEqual(len(cf.check(md, self.FORM).missing), 2)

    def test_extra_label_does_not_fail(self):
        md = "# 9.1 Test\n\n**Source:** book\n**Cost:** 1\n**Risk Owner:** x\n"
        result = cf.check(md, self.FORM)
        self.assertFalse(result.failed)
        self.assertEqual([c.text for c, _ in result.extra], ["Source"])

    def test_one_label_cannot_satisfy_two(self):
        form = dict(self.FORM, pages=[{"page": 1, "blocks": [
            {"type": "fields", "labels": ["Description"]}, {"type": "fields", "labels": ["Description"]}]}])
        result = cf.check("# 9.1 Test\n\n**Description:** a\n", form)
        self.assertEqual(len(result.missing), 1)
        self.assertEqual(result.disorder, [])


class Region(unittest.TestCase):
    def test_embedded_form_starts_at_page_one_and_ends_at_shallower_heading(self):
        md = ("# Package\n\n**Cost:** not the form\n\n### 2B form\n\n#### TEST, page 1 of 2\n\n**Cost:** 1\n\n"
              "#### TEST, page 2 of 2\n\n**Risk Owner:** x\n\n## Part 3\n\n**Source:** after the form\n")
        result = cf.check(md, Positions.FORM)
        self.assertFalse(result.failed)
        self.assertEqual(result.extra, [])
        self.assertEqual(result.start, 6)

    def test_section_option(self):
        md = "# Notes\n\n## Draft\n\n**Cost:** 1\n\n## Final\n\n**Cost:** 1\n**Risk Owner:** 2\n"
        self.assertTrue(cf.check(md, Positions.FORM, section="Draft").failed)
        self.assertFalse(cf.check(md, Positions.FORM, section="Final").failed)

    def test_end_option_stops_the_section(self):
        md = "# Notes\n\n## Final\n\n**Cost:** 1\n**Risk Owner:** 2\n\n### Roll-up\n\n| Hours | Amount |\n| --- | --- |\n"
        whole = cf.check(md, Positions.FORM, section="Final")
        self.assertEqual([c.text for c, _ in whole.extra], ["Hours", "Amount"])
        cut = cf.check(md, Positions.FORM, section="Final", until="Roll-up")
        self.assertEqual(cut.extra, [])
        self.assertFalse(cut.failed)

    def test_heading_labels_with_a_section_number(self):
        md = "# Package\n\n## Part 1: Scope\n\n### 1.1 Cost\n\ntext\n\n### 1.2 Risk Owner\n\ntext\n\n### 1.3 Notes\n"
        result = cf.check(md, Positions.FORM, section="Part 1:")
        self.assertFalse(result.failed)
        self.assertEqual(result.extra, [])  # a heading that is not a printed label is not reported

    def test_plain_first_cell_of_a_field_table_is_a_label(self):
        md = "# 9.1 Test\n\n" + table(["Field", "Content"], [["Cost", "1"], ["Owner", "x"], ["Risk Owner", "2"]])
        result = cf.check(md, Positions.FORM)
        self.assertFalse(result.failed)
        self.assertEqual([c.text for c, _ in result.extra], ["Owner"])


    def test_page_with_its_own_title_bar_stays_in_the_form(self):
        md = ("# Package\n\n**ID** before the form\n\n### 2.7\n\n"
              "#### REQUIREMENTS TRACEABILITY MATRIX, page 1 of 2\n\n**Project Title:** x\n\n"
              "#### INTER-REQUIREMENTS TRACEABILITY MATRIX, page 2 of 2\n\n**Project Title:** x\n")
        self.assertEqual(cf.region(md.splitlines(), spec("2.7")), (6, len(md.splitlines())))

    def test_underlying_picture_table_is_not_unprinted(self):
        md = "# 2.22 Cost Baseline\n\n" + table(["Period", "Cumulative Planned Value"]) + "**Owner:** x\n"
        self.assertEqual([c.text for c, _ in cf.check(md, spec("2.22")).extra], ["Owner"])


class CommandLine(unittest.TestCase):
    def test_list_prints_the_header_rows(self):
        code, out = run_main("--list", "2.32")
        self.assertEqual(code, 0)
        self.assertIn("  **Project Title:** value", out)
        bank2 = out[out.index("page 1, table, bank 2") + 1]
        self.assertTrue(bank2.startswith("  | Revised Probability | Impact: Scope |"))

    def test_list_puts_row_labels_in_their_printed_column(self):
        out = run_main("--list", "2.1")[1]
        i = out.index("  **Subsidiary Management Plans**")
        self.assertEqual(out[i + 2], "  | Name | Comment |")
        out = run_main("--list", "1.1")[1]
        self.assertIn("  | | Project Objectives | Success Criteria |", out)

    def test_list_accepts_a_hyphenated_number(self):
        self.assertEqual(run_main("--list", "2-10")[0], 0)

    def test_unknown_form(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(run_main("x.md", "9.99")[0], 2)

    def test_markdown_required_without_list(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(run_main("2.32")[0], 2)


@unittest.skipUnless(DOCS.is_dir(), "docs/ not present")
class RepoDocuments(unittest.TestCase):
    """The team's documents. A failure here is either a checker bug or a document defect."""

    def test_charter_form(self):
        result = cf.check((DOCS / "charter-package.en.md").read_text(encoding="utf-8"), spec("1.1"))
        self.assertFalse(result.failed, (result.missing, result.disorder))
        self.assertEqual(result.extra, [])

    def test_schedule_form(self):
        result = cf.check((DOCS / "forms" / "2-18-project-schedule.en.md").read_text(encoding="utf-8"), spec("2.18"))
        self.assertFalse(result.failed, (result.missing, result.disorder))

    def test_change_request_gaps_are_only_unbolded_impact_areas(self):
        """3.3 writes the impact areas as plain lines; the checker must say so, not lose them."""
        result = cf.check((DOCS / "forms" / "3-3-change-request.en.md").read_text(encoding="utf-8"), spec("3.3"))
        self.assertEqual(result.disorder, [])
        for slot, note in result.missing:
            self.assertEqual(slot.shape, "checklabel", slot.text)
            self.assertIn("plain line", note)


class TablesInsideBoxes(unittest.TestCase):
    FORM = {"form": "9.4", "name": "Boxes", "printed_title": "BOXES", "kind": "fields", "page_count": 1,
            "title_block": [], "pages": [{"page": 1, "blocks": [
                {"type": "fields", "labels": ["Problem", "Users"]}]}]}
    MD = ("# 9.4 Boxes\n\n| Field | Content |\n| --- | --- |\n| **Problem** | text |\n| **Users** | see below |\n\n"
          + table(["Role", "Who they are"], [["Teacher", "staff"]]))

    def test_a_table_header_inside_a_box_is_reported_by_default(self):
        result = cf.check(self.MD, self.FORM)
        self.assertEqual({c.text for c, _ in result.extra}, {"Role", "Who they are"})

    def test_ignore_tables_skips_it_and_counts_it(self):
        result = cf.check(self.MD, self.FORM, ignore_tables=True)
        self.assertEqual(result.extra, [])
        self.assertEqual(result.ignored, 1)

    def test_a_table_that_carries_a_printed_label_is_still_the_forms(self):
        md = "# 9.4 Boxes\n\n" + table(["Problem", "Extra column"], [["a", "b"]])
        result = cf.check(md, self.FORM, ignore_tables=True)
        self.assertEqual([c.text for c, _ in result.extra], ["Extra column"])
        self.assertEqual(result.ignored, 0)

    @unittest.skipUnless((DOCS / "charter-package.en.md").exists(), "needs docs/charter-package.en.md")
    def test_the_charter_scope_statement_with_the_option(self):
        code, lines = run_main(DOCS / "charter-package.en.md", "2.8", "--section", "Part 1: Requirement Specification",
                               "--end", "Part 2:", "--ignore-tables")
        self.assertEqual(code, 0, lines)
        self.assertFalse([x for x in lines if x.startswith("unprinted labels") and "(0" not in x], lines)


class FlattenedGroups(unittest.TestCase):
    """--flattened: the scope package writes the RTM group header as its child labels (rendering.md)."""

    FORM = {"form": "9.2", "name": "Test", "printed_title": "TEST", "kind": "matrix", "page_count": 1,
            "title_block": [], "pages": [{"page": 1, "blocks": [
                {"type": "table", "bank": 1, "columns": [
                    {"group": "Requirement Information", "columns": ["ID", "Source"]}, "Notes"]}]}]}
    FLAT = "# 9.2 Test\n\n" + table(["ID", "Source", "Notes"], [["R1", "A", "x"]])

    def test_a_flattened_group_fails_by_default(self):
        result = cf.check(self.FLAT, self.FORM)
        self.assertTrue(result.failed)
        self.assertEqual([s.text for s, _ in result.missing],
                         ["Requirement Information: ID", "Requirement Information: Source"])

    def test_flattened_option_accepts_the_child_label_and_lists_it(self):
        result = cf.check(self.FLAT, self.FORM, flat_groups=True)
        self.assertFalse(result.failed)
        self.assertEqual([s.text for s in result.flattened],
                         ["Requirement Information: ID", "Requirement Information: Source"])

    @unittest.skipUnless((DOCS / "scope-package.en.md").exists(), "needs docs/scope-package.en.md")
    def test_the_scope_package_rtm_passes_only_with_the_option(self):
        package = DOCS / "scope-package.en.md"
        self.assertEqual(run_main(package, "2.7", "--section", "Part 1:")[0], 1)
        code, lines = run_main(package, "2.7", "--section", "Part 1:", "--flattened")
        self.assertEqual(code, 0)
        self.assertTrue([x for x in lines if x.startswith("grouped headers written without the colon")])

    COST = {"form": "9.3", "name": "Cost", "printed_title": "COST", "kind": "fields", "page_count": 1,
            "title_block": [], "pages": [{"page": 1, "blocks": [
                {"type": "table", "bank": 1, "columns": [
                    "ID", {"group": "Labor", "columns": ["Hours", "Total"]},
                    {"group": "Material", "columns": ["Units", "Total"]}, "Total Cost"]}]}]}

    def test_group_and_child_joined_by_a_space_is_accepted(self):
        md = "# 9.3 Cost\n\n" + table(["ID", "Labor Hours", "Labor Total", "Material Units", "Material Total",
                                         "Total Cost"], [["1", "2", "3", "4", "5", "6"]])
        result = cf.check(md, self.COST, flat_groups=True)
        self.assertFalse(result.failed, result.missing)
        self.assertEqual(len(result.flattened), 4)
        self.assertEqual(result.extra, [])

    def test_a_child_shared_by_two_groups_is_not_accepted_alone(self):
        md = "# 9.3 Cost\n\n" + table(["ID", "Hours", "Total", "Units", "Total Cost"], [["1", "2", "3", "4", "5"]])
        result = cf.check(md, self.COST, flat_groups=True)
        self.assertEqual([s.text for s, _ in result.missing], ["Labor: Total", "Material: Total"])

    def test_the_other_spelling_of_an_accepted_label_stays_reported(self):
        md = "# 9.3 Cost\n\n" + table(["ID", "Labor Hours", "Labor Total", "Material Units", "Material Total",
                                         "Total Cost"], [["1"] * 6]) + table(["Hours", "Rate"], [["1", "2"]])
        result = cf.check(md, self.COST, flat_groups=True)
        self.assertEqual([c.text for c, _ in result.extra], ["Hours", "Rate"])

    @unittest.skipUnless((DOCS / "scope-package.en.md").exists(), "needs docs/scope-package.en.md")
    def test_the_wbs_dictionary_sheets_pass_with_the_option(self):
        package = DOCS / "scope-package.en.md"
        code, lines = run_main(package, "2.10", "--section", "Part 3: WBS Dictionary", "--flattened")
        self.assertEqual(code, 0, lines)
        self.assertIn("22/22 printed labels present in printed order", lines)
        self.assertFalse([x for x in lines if "Labor Rate" in x or "Material Cost" in x])

    @unittest.skipUnless((DOCS / "scope-package.en.md").exists(), "needs docs/scope-package.en.md")
    def test_the_second_rtm_page_is_checked_alone_with_page_two(self):
        package = DOCS / "scope-package.en.md"
        code, lines = run_main(package, "2.7", "--section", "Part 1B", "--page", "2", "--flattened")
        self.assertEqual(code, 0, lines)
        self.assertFalse([x for x in lines if x.startswith("missing")], lines)

    def test_page_must_exist(self):
        self.assertEqual(run_main("x.md", "2.7", "--page", "3")[0], 2)

    def test_flattened_option_does_not_excuse_a_label_that_is_absent(self):
        md = "# 9.2 Test\n\n" + table(["ID", "Notes"], [["R1", "x"]])
        result = cf.check(md, self.FORM, flat_groups=True)
        self.assertEqual([s.text for s, _ in result.missing], ["Requirement Information: Source"])


if __name__ == "__main__":
    unittest.main()
