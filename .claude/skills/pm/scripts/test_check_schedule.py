"""Tests for check_schedule.py. Run: uv run --with pytest pytest -q .claude/skills/pm/scripts

Each case is a defect the iteration-2 audit of the generated form 2.18 found by
reading, cut down to the rows that show it.
"""

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

import check_schedule as cs

HEAD = "| ID | WBS | Task Name | Duration | Start | Finish | Resource Name |\n| --- | --- | --- | --- | --- | --- | --- |\n"


def row(n, code, name, start, finish):
    return "| %d | %s | %s | 1 day | <mark>%s</mark> | <mark>%s</mark> | PM |\n" % (n, code, name, start, finish)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)

    def write(self, name, text):
        path = self.tmp / name
        path.write_text(text, encoding="utf-8")
        return str(path)

    def checks(self, schedule, **kwargs):
        out, _count = cs.run(self.write("2-18.md", schedule), **kwargs)
        return out


class Sequence(Base):
    def test_sign_off_before_the_work_it_signs_off(self):
        text = HEAD + row(1, "1.8.3.2-A1", "UAT execution with the business owners",
                          "Fri 12 February 2027", "Wed 17 February 2027") \
            + row(2, "1.8.3.2-A2", "Acceptance decision and sign-off with sponsor",
                  "Fri 12 February 2027", "Mon 15 February 2027")
        found = [f for f in self.checks(text) if f.check == "sequence"]
        self.assertEqual(len(found), 1)
        self.assertIn("1.8.3.2-A1", found[0].message)
        self.assertIn("work package", found[0].message)

    def test_acceptance_before_the_report_of_an_earlier_package(self):
        text = HEAD + row(1, "1.7.1.3-A2", "Reconciliation report production",
                          "Fri 12 February 2027", "Fri 12 February 2027") \
            + row(2, "1.7.1.4-A1", "Reconciliation walkthrough and written acceptance",
                  "Wed 10 February 2027", "Wed 10 February 2027")
        found = [f for f in self.checks(text) if f.check == "sequence"]
        self.assertEqual([f.line for f in found], [4])
        self.assertIn("control account", found[0].message)

    def test_closeout_before_the_rest_of_its_phase(self):
        text = HEAD + row(1, "1.10.1.1-A1", "First warranty month support",
                          "Thu 18 February 2027", "Mon 22 March 2027") \
            + row(2, "1.10.2.1-A1", "Closeout report and lessons learned",
                  "Mon 15 February 2027", "Tue 16 February 2027")
        found = [f for f in self.checks(text) if f.check == "sequence"]
        self.assertEqual(len(found), 1)
        self.assertIn("phase", found[0].message)

    def test_review_after_its_input_is_clean(self):
        text = HEAD + row(1, "1.3.1.1-A1", "Architecture design", "Mon 5 October 2026", "Fri 9 October 2026") \
            + row(2, "1.3.1.1-A2", "Design review", "Mon 12 October 2026", "Tue 13 October 2026")
        self.assertEqual(self.checks(text), [])

    def test_a_later_package_is_not_an_input(self):
        text = HEAD + row(1, "1.3.1.1-A1", "Design review", "Mon 5 October 2026", "Fri 9 October 2026") \
            + row(2, "1.3.1.2-A1", "Database schema", "Mon 5 October 2026", "Fri 16 October 2026")
        self.assertEqual(self.checks(text), [])


class Breaks(Base):
    CHARTER = ("| # | Assumption |\n| --- | --- |\n"
               "| 8 | The Lunar New Year of 2027 begins on 6 February 2027. Closeout is baselined the day before. |\n")

    def schedule(self):
        return HEAD + "| 1 |  | M5 System test complete | 0 days | <mark>Mon 8 February 2027</mark> | " \
                      "<mark>Mon 8 February 2027</mark> |  |\n" \
            + row(2, "1.8.1.3-A2", "Production deployment", "Fri 12 February 2027", "Mon 15 February 2027") \
            + row(3, "1.2.1.1-A1", "Workshops", "Mon 5 October 2026", "Fri 9 October 2026")

    def test_break_dated_in_the_charter(self):
        charter = self.write("charter.md", self.CHARTER)
        found = [f for f in self.checks(self.schedule(), charter=charter) if f.check == "break"]
        self.assertEqual(len(found), 1)
        self.assertIn("1 activities and 1 milestones", found[0].message)
        self.assertIn("no end date", found[0].message)
        self.assertIn("charter line 3", found[0].message)

    def test_break_given_with_an_end(self):
        import datetime
        window = (datetime.date(2027, 2, 6), datetime.date(2027, 2, 10), 0, "")
        found = [f for f in self.checks(self.schedule(), breaks=[window]) if f.check == "break"]
        self.assertIn("0 activities and 1 milestones", found[0].message)

    def test_no_break_no_finding(self):
        self.assertEqual([f for f in self.checks(self.schedule()) if f.check == "break"], [])


class Hours(Base):
    SCOPE = "Labor hours by resource: PM 800, DEV1 800, MOB1 400. At the charter's rates.\n"

    def schedule(self, pm, dev, mob):
        return ("| Resource | Booked hours | Weeks booked | Peak week | Peak hours |\n"
                "| --- | ---: | ---: | --- | ---: |\n"
                "| PM | %s | 28 | Mon 14 September 2026 | 40 |\n"
                "| DEV1 | %s | 26 | Mon 14 September 2026 | 40 |\n"
                "| MOB1 | %s | 11 | Mon 9 November 2026 | 40 |\n" % (pm, dev, mob))

    def test_levelled_hours_differ_from_the_priced_hours(self):
        scope = self.write("scope.md", self.SCOPE)
        found = self.checks(self.schedule("655.1", "1,020.9", "324"), scope=scope)
        self.assertEqual([(f.check, f.level) for f in found], [("hours", "error")])
        self.assertIn("PM 655.1 against 800", found[0].message)
        self.assertIn("DEV1 1020.9 against 800", found[0].message)
        self.assertIn("MOB1 324 against 400", found[0].message)

    def test_matching_hours_are_clean(self):
        scope = self.write("scope.md", self.SCOPE)
        self.assertEqual(self.checks(self.schedule("800", "800", "400"), scope=scope), [])


class CommandLine(Base):
    def test_exit_codes(self):
        scope = self.write("scope.md", Hours.SCOPE)
        clean = self.write("clean.md", HEAD + row(1, "1.1.1.1-A1", "Kickoff", "Mon 14 September 2026",
                                                     "Mon 14 September 2026"))
        bad = self.write("bad.md", Hours("schedule").schedule("1", "800", "400"))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cs.main([clean, "--scope", scope]), 0)
            self.assertEqual(cs.main([bad, "--scope", scope]), 1)
            self.assertEqual(cs.main([clean, "--break", "2027-02-06", "6 March 2027"]), 0)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            cs.main([clean, "--break", "not a date"])
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
