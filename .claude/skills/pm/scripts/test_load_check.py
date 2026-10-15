"""Tests for load_check.py. Run: uv run --with pytest pytest -q .claude/skills/pm/scripts"""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import load_check as lc

SHEET = """#### {code} {name}

| Responsible Person | PM |
| Due Dates | <mark>{window}</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {code}-A1 | Work | {res} | {hours} | 100 | {total} | | | | {total} |
| | **Work package total** | | {hours} | | {total} | | | | {total} |

"""


def scope(*sheets):
    return "\n".join(SHEET.format(code=c, name="Package", window=w, res=r, hours=h, total=h * 100)
                     for c, w, r, h in sheets)


MON_FRI = "Mon 5 October 2026 to Fri 9 October 2026"
NEXT_WEEK = "Mon 12 October 2026 to Fri 16 October 2026"


class Load(unittest.TestCase):
    def test_a_week_over_the_limit_is_reported_and_one_at_the_limit_is_not(self):
        findings, _ = lc.check(scope(("1.1.1.1", MON_FRI, "DEV1", 60), ("1.1.1.2", NEXT_WEEK, "DEV1", 40)), {}, {})
        self.assertEqual(len(findings), 1)
        self.assertIn("2026-10-05", findings[0])
        self.assertIn("60.0 hours", findings[0])

    def test_a_part_time_limit_comes_from_the_caller(self):
        text = scope(("1.1.1.1", MON_FRI, "MOB1", 30))
        self.assertEqual(lc.check(text, {}, {})[0], [])
        findings, _ = lc.check(text, {"MOB1": 20.0}, {})
        self.assertEqual(len(findings), 1)
        self.assertIn("limit of 20", findings[0])

    def test_work_after_a_leaving_date(self):
        text = scope(("1.1.1.1", MON_FRI, "MOB1", 10), ("1.1.1.2", NEXT_WEEK, "MOB1", 10))
        findings, _ = lc.check(text, {}, {"MOB1": lc.datetime.date(2026, 10, 9)})
        self.assertEqual(len(findings), 1)
        self.assertIn("2026-10-16", findings[0])

    def test_exclude_and_only_leaf_skip_sheets(self):
        text = scope(("1.1", MON_FRI, "DEV1", 100), ("1.1.1", MON_FRI, "DEV1", 10))
        self.assertEqual(len(lc.check(text, {}, {})[0]), 1)
        findings, skipped = lc.check(text, {}, {}, only_leaf=True)
        self.assertEqual(findings, [])
        self.assertEqual(skipped, ["1.1"])
        findings, skipped = lc.check(text, {}, {}, exclude={"1.1"})
        self.assertEqual(skipped, ["1.1"])

    def test_a_day_holding_more_than_24_hours_is_always_reported(self):
        text = scope(("1.1.1.1", "Mon 5 October 2026 to Mon 5 October 2026", "DEV1", 30))
        findings, _ = lc.check(text, {"DEV1": 80.0}, {})
        self.assertEqual(len(findings), 1)
        self.assertIn("more than a day holds", findings[0])

    def test_a_daily_limit_is_the_callers_and_off_by_default(self):
        text = scope(("1.1.1.1", MON_FRI, "DEV1", 50))
        self.assertEqual([f for f in lc.check(text, {"DEV1": 60.0}, {})[0]], [])
        findings, _ = lc.check(text, {"DEV1": 60.0}, {}, daily_limit=8.0)
        self.assertEqual(len(findings), 5)
        self.assertIn("daily limit of 8", findings[0])

    def test_holidays_leave_the_window_and_the_hours_move_to_the_other_days(self):
        text = scope(("1.1.1.1", MON_FRI, "DEV1", 40))
        day = lc.datetime.date
        findings, _ = lc.check(text, {}, {}, holidays=[(day(2026, 10, 7), day(2026, 10, 9))], daily_limit=8.0)
        self.assertEqual(len(findings), 2)
        self.assertIn("20.0 hours in one day", findings[0])

    def test_a_window_inside_a_holiday_is_skipped(self):
        text = scope(("1.1.1.1", MON_FRI, "DEV1", 40))
        day = lc.datetime.date
        findings, skipped = lc.check(text, {}, {}, holidays=[(day(2026, 10, 5), day(2026, 10, 9))])
        self.assertEqual((findings, skipped), ([], ["1.1.1.1"]))

    def test_a_window_that_ends_after_the_gate_it_feeds(self):
        text = scope(("1.1.1.1", MON_FRI, "DEV1", 10)).replace(
            "| Due Dates |", "| Milestones | 1. M1 requirements baselined |\n| Due Dates |", 1)
        day = lc.datetime.date
        self.assertEqual(lc.gate_crossings(text, {"M1": day(2026, 10, 8)}), [("1.1.1.1", "M1", day(2026, 10, 9),
                                                                              day(2026, 10, 8))])
        self.assertEqual(lc.gate_crossings(text, {"M1": day(2026, 10, 9)}), [])

    def test_a_default_limit_is_labelled_assumed(self):
        text = scope(("1.1.1.1", MON_FRI, "DEV1", 60))
        self.assertIn("limit assumed", lc.check(text, {}, {})[0][0])
        self.assertNotIn("assumed", lc.check(text, {"DEV1": 50.0}, {})[0][0])

    def test_explained_overload_is_a_warning_with_the_reason_and_exit_code_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scope.md"
            path.write_text(scope(("1.1.1.1", MON_FRI, "DEV1", 60)), encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = lc.main([str(path), "--explained", "overload=pending 3.3 in docs/forms"])
            self.assertEqual(code, 0)
            self.assertIn("warning (explained, awaiting decision: pending 3.3 in docs/forms)", out.getvalue())
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                self.assertEqual(lc.main([str(path), "--explained", "overload="]), 2)
                self.assertEqual(lc.main([str(path), "--explained", "leaving=x"]), 2)

    def test_a_prose_leaving_date_names_the_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scope.md"
            path.write_text(scope(("1.1.1.1", MON_FRI, "DEV1", 10)), encoding="utf-8")
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                self.assertEqual(lc.main([str(path), "--leaves", "DEV1=18 December"]), 2)
            self.assertIn("YYYY-MM-DD", err.getvalue())

    def test_a_levelled_schedule_places_the_hours_in_its_own_rows(self):
        text = scope(("1.1.1.1", MON_FRI, "DEV1", 40))
        sched = ("| ID | WBS | Task Name | Duration | Start | Finish | Resource Name |\n"
                 "| --- | --- | --- | --- | --- | --- | --- |\n"
                 "| 1 | 1.1.1.1-A1 | Work | 1 day | Mon 5 October 2026 | Mon 5 October 2026 | DEV1 |\n")
        found, unmatched = lc.schedule_allocations(text, sched)
        self.assertEqual([(c, p, h, len(d)) for c, p, h, d in found], [("1.1.1.1-A1", "DEV1", 40.0, 1)])
        self.assertEqual(unmatched, [])
        findings, _ = lc.check(text, {}, {}, found_skipped=(found, unmatched), daily_limit=8.0)
        self.assertTrue(any("40.0 hours in one day" in f for f in findings))
        divided = sched.replace("| DEV1 |", "| DEV1 10 h, DEV2 30 h |")
        hours = sorted((p, h) for _c, p, h, _d in lc.schedule_allocations(text, divided)[0])
        self.assertEqual(hours, [("DEV1", 10.0), ("DEV2", 30.0)])

    def test_command_line_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scope.md"
            path.write_text(scope(("1.1.1.1", MON_FRI, "DEV1", 60)), encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(lc.main([str(path)]), 1)
                self.assertEqual(lc.main([str(path), "--limit", "DEV1=80"]), 0)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                self.assertEqual(lc.main([str(path), "--holiday", "not-a-date"]), 2)
                self.assertEqual(lc.main([str(path), "--limit", "DEV1"]), 2)
                self.assertEqual(lc.main([str(path) + ".missing"]), 2)


class Effort(unittest.TestCase):
    D = staticmethod(lc.datetime.date)

    def test_a_part_time_effort_above_full_time_in_its_window(self):
        # 2.5 person-months of 160 hours in the 46 working days from 16 October to 18 December 2026
        findings, lines = lc.effort_check("MOB1", 2.5, "pm", self.D(2026, 10, 16), self.D(2026, 12, 18),
                                          hours_per_pm=160)
        self.assertEqual(len(findings), 1)
        self.assertIn("43.5 hours a week", findings[0])
        self.assertIn("above full time", findings[0])
        text = "\n".join(lines)
        self.assertIn("400 hours", text)
        self.assertIn("full-time week assumed", text)
        self.assertIn("1.19 person-months per calendar month", text)

    def test_an_effort_within_full_time_but_above_the_part_time_limit(self):
        args = ("MOB1", 200, "h", self.D(2026, 10, 5), self.D(2026, 11, 13))
        self.assertEqual(lc.effort_check(*args)[0], [])
        findings, _ = lc.effort_check(*args, limit=20.0, week_hours=40.0)
        self.assertEqual(len(findings), 1)
        self.assertIn("above the stated limit of 20", findings[0])
        lines = lc.effort_check(*args, week_hours=40.0)[1]
        self.assertNotIn("assumed", "\n".join(lines))

    def test_a_person_month_length_is_never_assumed(self):
        with self.assertRaises(ValueError) as caught:
            lc.effort_check("MOB1", 2.5, "pm", self.D(2026, 10, 16), self.D(2026, 12, 18))
        self.assertIn("--hours-per-pm", str(caught.exception))

    def test_a_window_with_no_working_day_is_refused(self):
        with self.assertRaises(ValueError):
            lc.effort_check("MOB1", 8, "h", self.D(2026, 10, 10), self.D(2026, 10, 11))

    def test_holidays_shorten_the_window(self):
        plain = lc.effort_check("A", 80, "h", self.D(2026, 10, 5), self.D(2026, 10, 16))[1][-1]
        held = lc.effort_check("A", 80, "h", self.D(2026, 10, 5), self.D(2026, 10, 16),
                               holidays=[(self.D(2026, 10, 12), self.D(2026, 10, 16))])[1][-1]
        self.assertIn("40.0 hours a week", plain)
        self.assertIn("80.0 hours a week", held)

    def test_parse_effort_reads_milestone_ids_and_dates(self):
        miles = {"M2": self.D(2026, 10, 16), "M5": self.D(2026, 12, 18)}
        self.assertEqual(lc.parse_effort("MOB1=2.5:pm:M2:M5", miles),
                         ("MOB1", 2.5, "pm", self.D(2026, 10, 16), self.D(2026, 12, 18)))
        self.assertEqual(lc.parse_effort("A=8:h:2026-10-05:2026-10-06", {})[3], self.D(2026, 10, 5))
        for bad in ("A=8:h:M2:M5", "A=8:x:2026-10-05:2026-10-06", "A=8:h:2026-10-06:2026-10-05",
                    "A=8:h:5 October:6 October", "A=8h"):
            with self.assertRaises(ValueError, msg=bad):
                lc.parse_effort(bad, {})

    def test_command_line_effort(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scope.md"
            path.write_text(scope(("1.1.1.1", MON_FRI, "DEV1", 10)), encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = lc.main([str(path), "--effort", "MOB1=2.5:pm:2026-10-16:2026-12-18", "--hours-per-pm", "160",
                                "--effort-source", "MOB1=charter.md:337 and charter.md:353"])
            self.assertEqual(code, 1)
            self.assertIn("charter.md:337 and charter.md:353", out.getvalue())
            self.assertIn("1 effort finding(s)", out.getvalue())
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(lc.main([str(path), "--effort", "MOB1=300:h:2026-10-16:2026-12-18"]), 0)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                self.assertEqual(lc.main([str(path), "--effort", "MOB1=2.5:pm:2026-10-16:2026-12-18"]), 2)
            self.assertIn("--hours-per-pm", err.getvalue())


if __name__ == "__main__":
    unittest.main()
