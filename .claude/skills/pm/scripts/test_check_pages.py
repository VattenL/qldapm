"""Tests for check_pages.py. Run: uv run --with pytest pytest -q .claude/skills/pm/scripts"""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import check_pages as cp


def levels(text):
    return [(f.level, f.line) for f in cp.check(text)]


class Pairs(unittest.TestCase):
    def test_both_numbers_are_clean(self):
        for text in ("PMBOK 6 section 6.5.2.6, printed page 215 (PDF page 254) says so.",
                     "Form 2.32, PDF page 141 (printed page 130).",
                     "PM 5.6 p168 (PDF 207) and BoF 3.3 p170 to 171 (PDF 181 to 182).",
                     "Agile Practice Guide p51 (PDF 861)."):
            self.assertEqual(levels(text), [], text)

    def test_a_bare_printed_page_is_an_error(self):
        self.assertEqual(levels("Early action beats repair (p443)."), [("error", 1)])

    def test_a_bare_pdf_page_is_an_error(self):
        self.assertEqual(levels("BoF 3.3 prose PDF 181 to 182."), [("error", 1)])

    def test_each_bare_number_is_reported_on_its_own_line(self):
        found = levels("- fine: p215 (PDF 254)\n- bad: PDF page 183\n- bad: page 12")
        self.assertEqual(found, [("error", 2), ("error", 3)])

    def test_a_pair_with_a_wrong_difference_warns_once(self):
        self.assertEqual(levels("PM p169 (PDF 999)."), [("warning", 1)])

    def test_section_and_form_numbers_are_not_pages(self):
        self.assertEqual([f for f in levels("PMBOK section 11.5.2.4 and form 2.32 and R5, D14.") if f[0] == "error"], [])

    def test_a_form_page_number_is_not_a_book_page(self):
        self.assertEqual(levels("The Disposition sits on page 3 of the form."), [])
        self.assertEqual(levels("Wrapped printed page 215\n(PDF page 254) pair."), [])

    def test_the_other_kind_must_be_in_the_same_sentence(self):
        self.assertEqual(levels("See p215. Then PDF 254 elsewhere."), [("error", 1), ("error", 1)])


class Citations(unittest.TestCase):
    def test_a_section_without_a_page_warns(self):
        self.assertEqual(levels("Crashing (PMBOK 6 section 6.5.2.6)."), [("warning", 1)])
        self.assertEqual(levels("CPI and SPI together (PM 7.4.2.2)."), [("warning", 1)])
        self.assertEqual(levels("Book of Forms form 2.32 lists it."), [("warning", 1)])

    def test_a_section_with_both_pages_is_clean(self):
        self.assertEqual(levels("PMBOK 6 section 6.5.2.6, printed page 215 (PDF page 254)."), [])

    def test_a_table_row_may_carry_the_page_in_another_cell(self):
        self.assertEqual(levels("| PM 6.5.2.6 | p215 (PDF 254) |"), [])
        self.assertEqual(levels("| PM 6.5.2.6 | crashing |"), [("warning", 1)])

    def test_a_bare_form_number_is_a_pointer(self):
        self.assertEqual(levels("Write form 2.32 and 3.3."), [])

    def test_sending_the_reader_to_a_note_is_named(self):
        found = cp.check("See pmbok-schedule.md for PM 6.5.2.6.")
        self.assertEqual([f.level for f in found], ["warning"])
        self.assertIn("note", found[0].message)

    def test_a_negative_claim_needs_a_page(self):
        self.assertEqual(levels("The book prints no weighted formula."), [("warning", 1)])
        self.assertEqual(levels("The book prints no formula (PM 7.4.2.2 p262 (PDF 301))."), [])
        self.assertEqual(levels("Not stated in the book."), [])


class Vietnamese(unittest.TestCase):
    def test_trang_in_and_trang_pdf_are_pages(self):
        self.assertEqual(levels("Theo PMBOK 6 muc 6.5.2.6, trang in 215 (trang PDF 254)."), [])
        self.assertEqual(levels("Theo PMBOK 6 muc 6.5.2.6, trang in 215 (PDF 254)."), [])

    def test_a_bare_vietnamese_page_is_an_error(self):
        self.assertEqual(levels("Xem trang in 215."), [("error", 1)])
        self.assertEqual(levels("Xem trang PDF 254."), [("error", 1)])


class QuotesAndPositions(unittest.TestCase):
    def test_a_quoted_page_number_is_the_document_s_own_text(self):
        self.assertEqual(levels('See "printed page 130" in the quotation.'), [])

    def test_a_quote_line_is_skipped(self):
        self.assertEqual(levels("> printed page 130 of the draft\n\nPlain text."), [])
        self.assertEqual(levels("quote: p130"), [])

    def test_a_position_in_a_document_is_not_a_book_page(self):
        self.assertEqual(levels("Section on printed page 1 of the Doc."), [])
        self.assertEqual(levels("Footer reads page 3 of 4."), [])

    def test_a_resource_code_with_hours_is_not_a_section_reference(self):
        self.assertEqual(levels("Resource PM 99.8 hours are booked in the week."), [])
        self.assertEqual(levels("Staff PM 40.5 h in the week of 5 October."), [])
        self.assertEqual(levels("PM 6.5.2.6 describes crashing."), [("warning", 1)])
        self.assertEqual(levels("PM 6.5 p215 describes it."), [("error", 1)])


class CommandLine(unittest.TestCase):
    def test_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            good, bad = Path(tmp) / "good.md", Path(tmp) / "bad.md"
            good.write_text("p215 (PDF 254)\n", encoding="utf-8")
            bad.write_text("p215\n", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cp.main([str(good)]), 0)
                self.assertEqual(cp.main([str(bad)]), 1)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(cp.main([str(good) + ".missing"]), 2)


if __name__ == "__main__":
    unittest.main()
