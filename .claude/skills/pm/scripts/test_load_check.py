"""Tests for load_check.py. Run: uv run --with pytest pytest -q .claude/skills/pm/scripts"""

import contextlib
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import load_check as lc

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "load"


def fixture(name):
    return (FIXTURES / (name + ".md")).read_text(encoding="utf-8")


def run_main(*argv):
    """(exit code, stdout, stderr) of the command line."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = lc.main([str(a) for a in argv])
    return code, out.getvalue(), err.getvalue()

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


class Fixtures(unittest.TestCase):
    """The fp fixtures come from the 14 November 2026 run over the team's documents (tool-run.md FP13, FP14); the
    x fixtures are charters that crashed the run instead of giving a usage error."""

    def test_fp01_schedule_rows_are_judged_by_the_hours_a_week_must_hold(self):
        # Write 40 h in week 1 and Review 40 h over weeks 1 and 2: the form places Review in week 2, peak 40 h.
        code, out, _err = run_main(FIXTURES / "fp01-schedule-even-spread-scope.md", "--schedule",
                                   FIXTURES / "fp01-schedule-even-spread-schedule.md")
        self.assertEqual(code, 0, out)
        self.assertIn("0 finding(s)", out)

    def test_fp01_a_week_the_rows_must_overfill_is_still_reported(self):
        sched = fixture("fp01-schedule-even-spread-schedule").replace(
            "| 10 days | Mon 14 September 2026 | Fri 25 September 2026 |",
            "| 6 days | Mon 14 September 2026 | Mon 21 September 2026 |")
        found, unmatched = lc.schedule_allocations(fixture("fp01-schedule-even-spread-scope"), sched)
        findings, _ = lc.check("", {}, {}, found_skipped=(found, unmatched), forced=True)
        self.assertEqual(len(findings), 1)
        self.assertIn("at least 72.0 hours", findings[0])

    def test_fp02_a_milestone_named_as_a_start_is_not_a_gate(self):
        text, charter = fixture("fp02-gate-from-milestone-scope"), fixture("fp02-gate-from-milestone-charter")
        self.assertEqual(lc.gate_crossings(text, lc.charter_milestones(charter)), [])
        gates = text.replace("issued every week from M0 |", "issued every week from M0; 2. Gate review at each of "
                                                            "M0 to M1 |")
        self.assertEqual([c[:2] for c in lc.gate_crossings(gates, lc.charter_milestones(charter))],
                         [("1.1.1.2", "M1")])

    def test_fp03_a_window_is_judged_against_the_latest_milestone_its_sheet_lists(self):
        text, charter = fixture("fp03-gate-latest-milestone-scope"), fixture("fp03-gate-latest-milestone-charter")
        self.assertEqual(lc.gate_crossings(text, lc.charter_milestones(charter)), [])
        late = text.replace("Tue 5 January 2027", "Fri 8 January 2027")
        self.assertEqual([c[:2] for c in lc.gate_crossings(late, lc.charter_milestones(charter))],
                         [("1.9.1.2", "M6")])

    def test_x01_a_charter_with_the_months_in_full_is_read(self):
        miles = lc.charter_milestones(fixture("x01-charter-full-months"))
        self.assertEqual(miles, {"M0": lc.datetime.date(2026, 9, 14), "M1": lc.datetime.date(2026, 10, 2),
                                 "M6": lc.datetime.date(2027, 1, 5)})
        code, out, err = run_main(FIXTURES / "fp03-gate-latest-milestone-scope.md", "--charter",
                                  FIXTURES / "x01-charter-full-months.md")
        self.assertEqual(code, 0, err)

    def test_x02_a_charter_without_the_milestone_block_is_a_usage_error(self):
        code, _out, err = run_main(FIXTURES / "fp03-gate-latest-milestone-scope.md", "--charter",
                                   FIXTURES / "x02-charter-no-milestone-block.md")
        self.assertEqual(code, 2)
        self.assertIn("#### Summary milestone schedule", err)

    def test_x03_a_missing_tools_folder_is_a_usage_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            scripts = Path(tmp) / "repo" / ".claude" / "skills" / "pm" / "scripts"
            scripts.mkdir(parents=True)
            here = Path(__file__).resolve().parent
            for name in ("load_check.py", "check_schedule.py"):
                shutil.copy(here / name, scripts / name)
            done = subprocess.run([sys.executable, str(scripts / "load_check.py"), str(FIXTURES / "x01-charter-full-"
                                   "months.md")], capture_output=True, text=True, cwd=tmp)
            self.assertEqual(done.returncode, 2, done.stderr)
            self.assertIn("tools", done.stderr)
            self.assertNotIn("Traceback", done.stderr)


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
