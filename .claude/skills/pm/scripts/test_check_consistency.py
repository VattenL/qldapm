"""Tests for check_consistency.py. Run: python3 -m unittest discover -s .claude/skills/pm/scripts

The fixtures in fixtures/consistency/ come from the iteration-1 review of the
skill: fn* should be flagged, fp* and x* should not be, except where a test below
records the review's verdict that a finding is correct or a miss is by design.
"""

import contextlib
import datetime
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import check_consistency as cc

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "consistency"
SPONSOR, CUSTOMER = "Dr. Nguyen Manh Hung", "Do Thi Bich Ngoc"


def fixture(name):
    return (FIXTURES / (name + ".md")).read_text(encoding="utf-8")


def findings(*names, **kwargs):
    return cc.run({name + ".md": fixture(name) for name in names}, **kwargs)


def pairs(found):
    return {(f.check, f.level) for f in found}


def run_main(*argv):
    """Exit code and printed lines of the command line."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = cc.main([str(a) for a in argv])
    return code, buf.getvalue().splitlines()


class Flagged(unittest.TestCase):
    """Every fn fixture gives the finding it was written for, at the level stated."""

    EXPECTED = {
        "fn01-range-hyphen": ("range", "warning"),
        "fn03-range-through": ("range", "warning"),
        "fn04-range-to-no-prefix": ("range", "warning"),
        "fn06-sponsor-of-center": ("role-merge", "error"),
        "fn07-sponsor-of-the-center": ("role-merge", "error"),
        "fn08-approvals-three-col": ("approvals", "error"),
        "fn09-approvals-heading-level4": ("approvals", "error"),
        "fn10-approvals-bold-colon-inline": ("approvals", "error"),
        "fn11-approvals-title-case": ("approvals", "error"),
        "fn12-date-short-dot": ("date", "error"),
        "fn13-date-iso": ("date", "error"),
        "fn14-date-month-first": ("date", "error"),
        "fn15-date-short-no-year": ("date", "error"),
        "fn16-date-numeric": ("date", "error"),
        "fn17-date-may": ("date", "error"),
        "fn18-total-percent-wrong": ("total", "error"),
        "fn19-total-label-third-col": ("total", "error"),
        "fn20-total-with-currency": ("total", "error"),
        "fn21-total-with-mark": ("total", "error"),
        "fn22-management-reserve": ("term", "error"),
        "fn23-br-self-closing": ("html", "error"),
        "fn24-br-uppercase-space": ("html", "error"),
        "fn25-emdash-entity": ("em-dash", "error"),
        "fn26-mark-on-label-plain": ("mark-on-label", "error"),
        "fn27-mark-bold-both": ("mark-on-label", "error"),
        "fn28-heading-mark-bold": ("mark-on-label", "error"),
        "fn29-id-conflict-two-bank": ("id-conflict", "warning"),
        "fn30-id-conflict-req-id-header": ("id-conflict", "warning"),
        "fn32-sponsor-bold-colon-header": ("role-merge", "error"),
        "fn34-uniform-marked": ("uniform-column", "warning"),
        "fn35-section-ref-capital": ("section-ref", "error"),
        "fn36-section-ref-sign": ("section-ref", "error"),
        "fn37-range-v-family-list-item": ("range", "warning"),
        "fn38-range-heading-defined": ("range", "warning"),
        "fn39-charter-word-hides-ref": ("section-ref", "error"),
    }

    def test_each_fixture(self):
        for name, expected in self.EXPECTED.items():
            with self.subTest(name):
                self.assertIn(expected, pairs(findings(name)))

    def test_en_dash_range(self):
        text = fixture("fn01-range-hyphen").replace("R1-R10", "R1\u2013R10")
        self.assertIn(("range", "warning"), pairs(cc.run({"doc.md": text})))

    def test_sponsor_merge_needs_the_names(self):
        """Without the charter the names are unknown; --sponsor and --customer supply them."""
        self.assertNotIn("role-merge", {f.check for f in findings("fn31-sponsor-merge-no-charter")})
        found = findings("fn31-sponsor-merge-no-charter", sponsor=SPONSOR, customer=CUSTOMER)
        self.assertIn(("role-merge", "error"), pairs(found))

    def test_one_finding_per_highlighted_heading(self):
        found = [f for f in findings("fn28-heading-mark-bold") if f.check == "mark-on-label"]
        self.assertEqual(len(found), 1)

    def test_all_three_non_house_date_shapes(self):
        for name, text in (("fn13-date-iso", "2026-09-02"), ("fn14-date-month-first", "September 2, 2026"),
                           ("fn16-date-numeric", "02/09/2026")):
            with self.subTest(name):
                self.assertTrue(any(text in f.message for f in findings(name)))

    def test_two_bank_rtm_source_conflicts(self):
        """The Inter-RTM rows the review found in the scope package before commit bfd9df8."""
        found = [f for f in findings("rtm-source-conflicts") if f.check == "id-conflict"]
        conflicted = {f.message.split()[0] for f in found}
        self.assertEqual(conflicted, {"FR06", "FR12", "NFR01", "NFR08"})
        self.assertTrue(all("source" in f.message for f in found))


class Clean(unittest.TestCase):
    """Each fp and x fixture is clean of the check it probes."""

    PROBES = {
        "fp01-iteration-range": "range",
        "fp03-weekday-table-full": "date-style",
        "fp05-pmbok-ref": "section-ref",
        "fp06-mark-after-bold-label": "mark-on-label",
        "fp07-mark-bold-content": "mark-on-label",
        "fp08-total-with-percent": "total",
        "fp09-total-rounded-percent": "total",
        "fp10-subtotal-then-grand": "total",
        "fp11-wbs-code-ids": "id-conflict",
        "fp12-id-repeats-by-design": "id-conflict",
        "fp13-total-in-text-column": "total",
        "fp14-dates-iso-in-code": "date",
        "fp15-short-range-hyphen-in-wbs": "range",
        "fp16-emoji-arrow-dingbat": "emoji",
        "fp17-section-ref-heading-with-mark": "section-ref",
        "fp19-sponsor-with-word-owner-of-risk": "role-merge",
        "fp20-customer-sponsored-event": "role-merge",
        "x02-rounded-percent": "total",
        "x03-section-heading-word": "section-ref",
        "x04-subtotal-hyphen": "total",
        "x05-one-line-header": "mark-on-label",
        "x06-total-first-col-numbered": "total",
    }

    def test_each_fixture(self):
        for name, check in self.PROBES.items():
            with self.subTest(name):
                self.assertNotIn(check, {f.check for f in findings(name)})

    def test_no_errors_at_all(self):
        for name in self.PROBES:
            if name == "fp17-section-ref-heading-with-mark":
                continue
            with self.subTest(name):
                self.assertEqual([str(f) for f in findings(name) if f.level == "error"], [])

    def test_cross_document_section_reference(self):
        """'section 1.1.5' in a form resolves against the charter given with it."""
        alone = findings("fp04-cross-doc-ref")
        self.assertIn(("section-ref", "error"), pairs(alone))
        pooled = [f for f in findings("fp04-cross-doc-ref", "charter-context") if f.check == "section-ref"]
        self.assertEqual([f.level for f in pooled], ["warning"])
        self.assertIn("charter-context.md", pooled[0].message)


class Verdicts(unittest.TestCase):
    """Findings and misses the review judged correct or by design. A change here is deliberate."""

    def test_iteration_from_the_first_id_stays_a_warning(self):
        # F01 to F10 for an iteration cannot be told from a stale range mechanically (review A8).
        self.assertIn(("range", "warning"), pairs(findings("fp02-iteration-range-from-1")))

    def test_highlighted_heading_is_an_error(self):
        self.assertIn(("mark-on-label", "error"), pairs(findings("fp17-section-ref-heading-with-mark")))

    def test_constant_unit_column_is_reported(self):
        self.assertIn(("uniform-column", "warning"), pairs(findings("fp18-uniform-numeric-vs-text")))

    def test_range_three_short_of_the_end_is_silent(self):
        # NEAR_END is 2: R1 to R9 after R12 reads as a subset (review A8).
        self.assertNotIn("range", {f.check for f in findings("x01-r1-r9")})
        self.assertNotIn("range", {f.check for f in findings("fn05-range-and")})

    def test_short_table_is_not_judged_uniform(self):
        self.assertNotIn("uniform-column", {f.check for f in findings("fn33-uniform-7rows")})


class Consistency(unittest.TestCase):
    """Each case is a finding the reviewers actually made on this project."""

    def run_on(self, text, **names):
        return {f.check for f in cc.run({"doc.md": text}, **names)}

    CHARTER = "\n".join([
        "| Field | Content |", "| --- | --- |",
        "| **Project Sponsor** | <mark>Dr. Nguyễn Mạnh Hùng</mark> |",
        "| **Project Customer** | <mark>Đỗ Thị Bích Ngọc, owner and Director of "
        "the learning center</mark> |",
        "",
    ])

    def test_leading_zero_and_short_month(self):
        self.assertIn("date", self.run_on("Prepared 02 September 2026."))
        self.assertIn("date", self.run_on("Go-live 5 Jan 2027."))
        self.assertNotIn("date", self.run_on("Go-live 5 January 2027."))
        self.assertNotIn("date", self.run_on("It goes live on 5 May."))

    def test_br_is_not_converted(self):
        self.assertIn("html", self.run_on("| 1.1 | first<br>second |"))
        self.assertNotIn("html", self.run_on("| 1.1 | <mark>assumed</mark> |"))
        self.assertNotIn("html", self.run_on("It dropped the `<div>` wrappers."))
        self.assertIn("html", self.run_on("Fees &amp; charges"))

    def test_highlighted_label(self):
        self.assertIn("mark-on-label", self.run_on("| **<mark>Project Customer</mark>** | x |"))
        self.assertNotIn("mark-on-label", self.run_on("**Sponsor:** <mark>Dr. Nguyễn Mạnh Hùng</mark>"))

    def test_stale_range(self):
        register = "\n".join("| R%d | risk |" % i for i in range(1, 13))
        text = "| ID | Risk |\n| --- | --- |\n" + register + "\n\nRisks R1 to R10 carry responses."
        found = cc.run({"doc.md": text})
        self.assertIn(("range", "warning"), pairs(found))
        self.assertNotIn("range", self.run_on(text.replace("R1 to R10", "R1 to R12")))
        self.assertIn(("range", "error"), pairs(cc.run({"doc.md": text.replace("R1 to R10", "R1 to R14")})))

    def test_iteration_subrange_is_not_stale(self):
        register = "\n".join("| F%02d | f |" % i for i in range(1, 13))
        text = "| ID | Function |\n| --- | --- |\n" + register + "\n\nIteration 1 builds F01 to F05."
        self.assertNotIn("range", self.run_on(text))

    def test_dangling_section(self):
        self.assertIn("section-ref", self.run_on("## 1.1 Scope\n\nBusiness case in section 2A."))
        self.assertNotIn("section-ref", self.run_on("### 2A. Charter elements\n\nSee section 2A."))
        self.assertNotIn("section-ref", self.run_on("As PMBOK 6 section 4.1.3.1 says."))
        self.assertNotIn("section-ref", self.run_on("## Part 1: Scope\n\nSee Part 1."))
        self.assertIn("section-ref", self.run_on("## Part 1: Scope\n\nSee Part 4."))

    def test_charter_reference_is_checked_against_the_charter(self):
        charter = "# PROJECT CHARTER\n\n### 2A. Charter elements\n"
        form = "The charter section 2C has the budget."
        found = cc.run({"form.md": form, "charter.md": charter})
        self.assertIn(("section-ref", "error"), pairs(found))
        found = cc.run({"form.md": form.replace("2C", "2A"), "charter.md": charter})
        self.assertNotIn("section-ref", {f.check for f in found})

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

    M0_TABLE = "| ID | Milestone | Due date |\n| --- | --- | --- |\n| M0 | Kickoff | Mon 14 Sep 2026 |\n\n"

    def test_m0_phrase_after_m0_is_stale(self):
        text = self.M0_TABLE + ("**Date Prepared:** 15 October 2026\n\n"
                                "| Name |\n| --- |\n| <mark>name to be assigned by the sponsor at M0</mark> |\n")
        self.assertIn("stale-m0", self.run_on(text))

    def test_m0_phrase_on_or_before_m0_is_fine(self):
        text = self.M0_TABLE + ("**Date Prepared:** 14 September 2026\n\n"
                                "| Name |\n| --- |\n| <mark>name to be assigned by the sponsor at M0</mark> |\n")
        self.assertNotIn("stale-m0", self.run_on(text))

    def test_other_wordings_of_the_m0_appointment_are_stale_too(self):
        for sentence in ("The sponsor names the project manager on or before 14 September 2026.",
                         "The project manager is to be assigned by the sponsor.",
                         "The sponsor will appoint the project manager at M0.",
                         "| Assumptions | The sponsor names the project manager by Mon 14 Sep 2026, and others. |"):
            text = self.M0_TABLE + "**Date Prepared:** 23 September 2026\n\n%s\n" % sentence
            self.assertIn("stale-m0", self.run_on(text), sentence)

    def test_an_appointment_after_m0_or_no_appointment_is_not_flagged(self):
        for sentence in ("The sponsor names the project manager by 30 September 2026.",
                         "Kickoff minutes are signed by the project manager named in writing.",
                         "The sponsor assigns the reviewer at M0."):
            text = self.M0_TABLE + "**Date Prepared:** 23 September 2026\n\n%s\n" % sentence
            self.assertNotIn("stale-m0", self.run_on(text), sentence)

    def test_a_rule_directly_under_a_table_row_is_an_error(self):
        table = "| A | B |\n| --- | --- |\n| 1 | 2 |\n"
        self.assertIn("table-rule", self.run_on(table + "---\n\nNext\n"))
        self.assertNotIn("table-rule", self.run_on(table + "\n---\n\nNext\n"))
        self.assertNotIn("table-rule", self.run_on("Text\n\n---\n\nNext\n"))

    def test_a_long_italic_note_above_a_form_warns(self):
        page = "#### RISK REPORT, page 1 of 1\n\n| A |\n| --- |\n| x |\n"
        short = "*" + " ".join(["word"] * 40) + "*\n\n" + page
        long = "*" + " ".join(["word"] * 200) + "*\n\n" + page
        self.assertNotIn("note-length", self.run_on(short))
        self.assertIn("note-length", self.run_on(long))
        self.assertNotIn("note-length", self.run_on("*" + " ".join(["word"] * 200) + "*\n\nNo form page here.\n"))

    def test_a_wrapped_italic_note_is_counted_as_one_paragraph(self):
        page = "#### RISK REPORT, page 1 of 1\n\n| A |\n| --- |\n| x |\n"
        words = ["word"] * 200
        wrapped = "*" + "\n".join(" ".join(words[i:i + 10]) for i in range(0, 200, 10)) + "*\n\n" + page
        self.assertIn("note-length", self.run_on(wrapped))
        two = "*" + " ".join(["a"] * 40) + "*\n\n*" + "\n".join(" ".join(words[i:i + 10]) for i in range(0, 200, 10)) \
            + "*\n\n" + page
        found = [f for f in cc.run({"doc.md": two}) if f.check == "note-length"]
        self.assertEqual(len(found), 1)
        self.assertGreater(found[0].line, 1)

    def test_date_prepared_against_today_is_off_unless_given(self):
        text = "**Date Prepared:** 2 September 2026\n"
        self.assertNotIn("date-prepared", {f.check for f in cc.run({"a.md": text})})
        late = [f for f in cc.run({"a.md": text}, today=datetime.date(2026, 10, 15)) if f.check == "date-prepared"]
        self.assertEqual([f.level for f in late], ["warning"])
        self.assertIn("43 day(s)", late[0].message)
        early = [f for f in cc.run({"a.md": text}, today=datetime.date(2026, 9, 1)) if f.check == "date-prepared"]
        self.assertEqual([f.level for f in early], ["error"])
        same = cc.run({"a.md": text}, today=datetime.date(2026, 9, 2))
        self.assertNotIn("date-prepared", {f.check for f in same})

    def test_uniform_column_message_names_the_column_and_the_value(self):
        rows = "\n".join("| FR%02d | Must have |" % i for i in range(1, 10))
        found = [f for f in cc.run({"a.md": "| ID | Priority |\n| --- | --- |\n" + rows}) if f.check == "uniform-column"]
        self.assertIn("column 'Priority'", found[0].message)
        self.assertIn("'Must have' in every one of 9 rows", found[0].message)

    def test_m0_rule_needs_the_charter_date(self):
        text = "**Date Prepared:** 15 October 2026\n\nname to be assigned by the sponsor at M0\n"
        self.assertNotIn("stale-m0", self.run_on(text))

    def test_uniform_priority(self):
        rows = "\n".join("| FR%02d | Must have |" % i for i in range(1, 10))
        self.assertIn("uniform-column", self.run_on("| ID | Priority |\n| --- | --- |\n" + rows))

    def test_uniform_column_explained_above_the_table(self):
        rows = "\n".join("| FR%02d | Must have |" % i for i in range(1, 10))
        table = "| ID | Priority |\n| --- | --- |\n" + rows
        said = "## Part 1: RTM\n\nEvery requirement is Must have: nothing in the baseline is optional.\n\n"
        self.assertNotIn("uniform-column", self.run_on(said + table))
        # The reason must be in the same part: a sentence above a level-2 heading does not count.
        self.assertIn("uniform-column", self.run_on(said.replace("## Part 1", "# Doc") + "## Part 2\n\n" + table))
        # Naming the value without the column or an every/all word is not an explanation.
        self.assertIn("uniform-column", self.run_on("Must have is a MoSCoW grade.\n\n" + table))

    def test_status_open_explained_in_the_reading_paragraph(self):
        rows = "\n".join("| R%d | Open |" % i for i in range(1, 13))
        text = ("# 2.32 Risk Register\n\n*Status is Open because no response has been completed.*\n\n"
                "| ID | Status |\n| --- | --- |\n" + rows)
        self.assertNotIn("uniform-column", self.run_on(text))

    def test_audit_reports_an_explained_uniform_column_too(self):
        rows = "\n".join("| FR%02d | Must have |" % i for i in range(1, 10))
        text = ("## Part 1: RTM\n\nEvery requirement is Must have: nothing in the baseline is optional.\n\n"
                "| ID | Priority |\n| --- | --- |\n" + rows)
        self.assertNotIn("uniform-column", {f.check for f in cc.run({"a.md": text})})
        audited = [f for f in cc.run({"a.md": text}, audit=True) if f.check == "uniform-column"]
        self.assertEqual(len(audited), 1)
        self.assertIn("still separates nothing", audited[0].message)

    def test_priority_of_one_id_differs_between_tables(self):
        text = "\n".join([
            "| ID | Priority |", "| --- | --- |", "| BR03 | Must have |", "",
            "| ID | Priority |", "| --- | --- |", "| BR03 | Should have |"])
        self.assertIn("id-conflict", self.run_on(text))

    def test_section_after_a_page_citation_is_the_books(self):
        text = "Per PMBOK 6, printed page 442, section 11.5.2.1 says so. See also section 7.4.2.2 of the Guide."
        self.assertNotIn("section-ref", self.run_on(text))
        # a section of this document is still checked
        self.assertIn("section-ref", self.run_on("The plan is in section 9.9 here."))
        # another sentence about the book does not excuse the next sentence
        self.assertIn("section-ref", self.run_on("PMBOK 6 is the source. The plan is in section 9.9 here."))

    def test_count_that_disagrees_with_the_list_after_it(self):
        text = "All fourteen items of the plan:\n\n- one\n- two\n- three\n"
        found = [f for f in cc.run({"a.md": text}) if f.check == "count"]
        self.assertEqual(len(found), 1)
        self.assertIn("says 14 items, but the list starting at line 3 has 3", found[0].message)
        ok = "All three items of the plan:\n\n- one\n- two\n- three\n"
        self.assertEqual([f for f in cc.run({"a.md": ok}) if f.check == "count"], [])

    def test_count_against_a_table_and_a_run_of_headings(self):
        table = "The two risks are:\n\n| ID | Risk |\n| --- | --- |\n| R1 | a |\n| R2 | b |\n| R3 | c |\n"
        self.assertEqual(len([f for f in cc.run({"a.md": table}) if f.check == "count"]), 1)
        heads = "### Charter\n\nAll four elements, in order.\n\n#### One\n\ntext\n\n#### Two\n\ntext\n\n### Next\n"
        found = [f for f in cc.run({"a.md": heads}) if f.check == "count"]
        self.assertEqual(len(found), 1)
        self.assertIn("has 2", found[0].message)

    def test_count_repeated_elsewhere_is_reported_with_the_wrong_one(self):
        text = ("Covers all fourteen elements.\n\n### Charter\n\n*All fourteen elements of Table 1.1, listed*\n\n"
                "#### One\n\ntext\n")
        found = [f for f in cc.run({"a.md": text}) if f.check == "count"]
        self.assertEqual(sorted(f.line for f in found), [1, 5])

    def test_count_of_a_book_table_comes_from_the_registry(self):
        found = [f for f in cc.run({"a.md": "The thirteen elements of Table 1.1 are used."}) if f.check == "count"]
        self.assertEqual(found, [])
        found = [f for f in cc.run({"a.md": "The fourteen elements of Table 1.1 are used."}) if f.check == "count"]
        self.assertEqual(len(found), 1)
        self.assertIn("Table 1.1 as the book prints it", found[0].message)
        self.assertIn("PDF pages 14 to 15 (printed pages 3 to 4)", found[0].message)

    def test_count_claims_that_look_backwards_or_sit_in_a_list_are_left_alone(self):
        above = "The two functions above are in scope.\n\n| a | b |\n| --- | --- |\n| 1 | 2 |\n| 3 | 4 |\n| 5 | 6 |\n"
        self.assertEqual([f for f in cc.run({"a.md": above}) if f.check == "count"], [])
        inside = "- Each of the seven roles sees data\n- other\n- another\n"
        self.assertEqual([f for f in cc.run({"a.md": inside}) if f.check == "count"], [])

    def test_reference_named_after_the_number(self):
        self.assertNotIn("section-ref", self.run_on("Carried by Part 2 of `docs/scope-package.en.md`."))
        charter = "# PROJECT CHARTER\n\n### 1.6 Project Assumptions\n"
        found = cc.run({"form.md": "See section 1.6 of the charter.", "charter.md": charter})
        self.assertNotIn("section-ref", {f.check for f in found})
        found = cc.run({"form.md": "See section 1.9 of the charter.", "charter.md": charter})
        self.assertIn(("section-ref", "error"), pairs(found))

    def test_reference_found_in_two_files_names_both(self):
        found = cc.run({"form.md": "See Part 2.", "a.md": "## Part 2: One\n", "b.md": "## Part 2: Two\n"})
        message = [f.message for f in found if f.check == "section-ref"][0]
        self.assertIn("a.md", message)
        self.assertIn("b.md", message)

    def test_image_placeholder_is_not_a_note(self):
        form = "#### PROJECT SCHEDULE, page 1 of 2\n\n@@IMAGE 2-18-gantt-chart-1.png@@\n"
        self.assertNotIn("form-note", self.run_on(form))

    def test_book_page_without_its_numbering(self):
        self.assertIn("citation", self.run_on("Form 2.18, pages 78 to 81."))
        self.assertIn("citation", self.run_on("Page 14 of the book supports it."))
        self.assertNotIn("citation", self.run_on("Form 2.18, PDF pages 91 to 92 (printed pages 80 to 81)."))
        self.assertNotIn("citation", self.run_on("Form 1.1 page 3 holds the milestones."))
        self.assertNotIn("citation", self.run_on("#### PROJECT CHARTER, page 2 of 4"))

    def test_stakeholder_list_misses_a_party_a_risk_depends_on(self):
        charter = ("| # | Type | Risk | Response |\n| --- | --- | --- | --- |\n"
                   "| R12 | Project | A store rejects the app | Open the Apple and Google Play accounts at M1 |\n")
        register = ("| Name | Position/Role |\n| --- | --- |\n| Sponsor | Sponsor |\n| Customer | Customer |\n"
                    "| Students and parents | Users of the app on Google Play |\n")
        found = [f for f in cc.run({"1-3.md": register, "charter.md": charter}) if f.check == "stakeholder"]
        self.assertEqual(len(found), 2)
        self.assertTrue(all(f.path == "1-3.md" and f.level == "warning" for f in found))
        listed = register + "| Apple | App Store operator |\n| Google | Google Play operator |\n"
        self.assertEqual([f for f in cc.run({"1-3.md": listed, "charter.md": charter})
                          if f.check == "stakeholder"], [])

    def test_party_table_is_read_from_the_references(self):
        self.assertIn("Cloud hosting provider", [party for party, _, _ in cc.load_parties()])

    def test_date_style_is_judged_per_column(self):
        sheet = "\n".join([
            "| Field | Content |", "| --- | --- |",
            "| Date Prepared | 23 September 2026 |",
            "| Due Dates | Mon 14 September 2026 to Fri 18 September 2026 |"])
        self.assertNotIn("date-style", self.run_on(sheet))
        mixed = "\n".join([
            "| Milestone | Date |", "| --- | --- |",
            "| M0 | Mon 14 September 2026 |", "| M1 | 2 October 2026 |"])
        self.assertIn("date-style", self.run_on(mixed))

    def test_note_inside_a_printed_form(self):
        form = "\n".join([
            "#### PROJECT CHARTER, page 4 of 4", "",
            "| Field | Content |", "| --- | --- |", "| **Approvals** | |", "",
            "- [ ] Approve", "",
            "The project manager is not yet named."])
        found = [f for f in cc.run({"doc.md": form}) if f.check == "form-note"]
        self.assertEqual([f.line for f in found], [9])
        self.assertIn('"The project manager is not yet named."', found[0].message)

    def test_every_form_note_is_listed_with_its_text_when_grouped(self):
        form = "\n".join([
            "#### PROJECT CHARTER, page 4 of 4", "",
            "| Field | Content |", "| --- | --- |", "| **Approvals** | |", "",
            "The project manager is not yet named.", "",
            "A second note that is not printed."])
        found = [f for f in cc.run({"doc.md": form}) if f.check == "form-note"]
        lines = cc.grouped(found, {"doc.md": 0})
        self.assertEqual(len(found), 2)
        self.assertIn('"The project manager is not yet named."', lines[0])
        self.assertTrue(any('"A second note that is not printed."' in l and "doc.md:9" in l for l in lines[1:]))

    def test_a_long_form_note_is_quoted_and_marked_cut(self):
        text = "word " * (cc.NOTE_QUOTE // 5 + 20)
        quoted = cc.quoted(text)
        self.assertIn("(cut at %d of" % cc.NOTE_QUOTE, quoted)
        self.assertEqual(cc.quoted("short note"), '"short note"')

    def test_denied_term_is_allowed(self):
        self.assertNotIn("term", self.run_on("The project has no management reserve."))

    def test_term_table_is_read_from_the_references(self):
        self.assertIn("management reserve", [never for never, _, _ in cc.load_terms()])


class CommandLine(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        register = "\n".join("| R%d | risk %d |" % (i, i) for i in range(1, 11))
        self.source = self.tmp / "source.md"
        self.source.write_text("| ID | Risk |\n| --- | --- |\n" + register
                               + "\n\nRisks R1 to R10 carry responses. Prepared 02 September 2026.\n",
                               encoding="utf-8")
        self.form = self.tmp / "form.md"
        self.form.write_text("Responses for R1 to R10 are in the register.\n", encoding="utf-8")

    def test_exit_codes(self):
        self.assertEqual(run_main(self.form)[0], 0)
        self.assertEqual(run_main(self.source)[0], 1)
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                cc.main([str(self.tmp / "nope.md")])
        self.assertEqual(raised.exception.code, 2)

    def test_report_hides_errors_already_in_the_context(self):
        code, lines = run_main(self.form, self.source, "--report", self.form)
        self.assertEqual(code, 0)
        self.assertFalse(any("source.md" in line for line in lines[:-1]))
        self.assertIn("not shown", lines[-1])

    def test_report_without_a_value_means_the_first_path(self):
        self.assertEqual(run_main(self.form, self.source, "--report")[0], 0)

    def test_report_path_is_added_to_the_paths(self):
        code, lines = run_main("--report", self.form, self.source)
        self.assertEqual(code, 0)
        self.assertIn("in 2 file(s)", lines[-1])

    def test_report_shows_what_the_new_form_breaks_in_the_context(self):
        """A form that adds R11 and R12 makes the source's 'R1 to R10' stale."""
        self.form.write_text("| ID | Risk |\n| --- | --- |\n| R11 | new |\n| R12 | new |\n", encoding="utf-8")
        code, lines = run_main(self.form, self.source, "--report", self.form)
        self.assertTrue(any("source.md" in line and "[range]" in line for line in lines))

    def test_report_still_fails_on_errors_in_the_form(self):
        self.form.write_text("Prepared 2026-09-02.\n", encoding="utf-8")
        self.assertEqual(run_main(self.form, self.source, "--report", self.form)[0], 1)

    def test_paths_are_deduplicated(self):
        _code, once = run_main(self.source)
        _code, twice = run_main(self.source, self.source)
        self.assertEqual(once, twice)

    def test_group_prints_one_line_per_check_with_a_count(self):
        self.source.write_text("Dates 02 September 2026 and 03 September 2026 and 2026-09-04.\n", encoding="utf-8")
        _code, lines = run_main(self.source, "--group")
        date_lines = [line for line in lines if "[date]" in line]
        self.assertEqual(len(date_lines), 1)
        self.assertIn("x3", date_lines[0])

    def test_show_context_lists_the_hidden_findings_with_their_heading(self):
        self.source.write_text("## Register\n\n" + self.source.read_text(encoding="utf-8"), encoding="utf-8")
        _code, plain_lines = run_main(self.form, self.source, "--report", self.form)
        _code, lines = run_main(self.form, self.source, "--report", self.form, "--show-context")
        self.assertGreater(len(lines), len(plain_lines))
        context = [line for line in lines if line.lstrip().startswith("CONTEXT")]
        self.assertTrue(context)
        self.assertTrue(all("(under: Register)" in line for line in context))

    def test_charter_and_scope_are_shorthand_for_the_package_files(self):
        code, lines = run_main("charter", "scope", "--errors-only")
        self.assertIn("2 file(s)", lines[-1])
        self.assertNotIn("no such file", "\n".join(lines))

    def test_today_must_be_a_date(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                cc.main([str(self.form), "--today", "15 October"])

    def test_errors_only_hides_warnings(self):
        _code, lines = run_main(self.source, "--errors-only")
        self.assertFalse(any(line.startswith("WARNING") for line in lines))


if __name__ == "__main__":
    unittest.main()
