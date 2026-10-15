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


    def test_a_break_that_can_absorb_no_overrun_makes_work_inside_it_an_error(self):
        strict = self.CHARTER + "- **The Lunar New Year break** begins immediately after closeout and can absorb no overrun.\n"
        found = [f for f in self.checks(self.schedule(), charter=self.write("charter.md", strict))
                 if f.check == "break"]
        self.assertEqual([f.level for f in found], ["error"])
        self.assertIn("can absorb no overrun", found[0].message)
        mild = [f for f in self.checks(self.schedule(), charter=self.write("c2.md", self.CHARTER)) if f.check == "break"]
        self.assertEqual([f.level for f in mild], ["warning"])

    def test_explained_break_needs_a_reason(self):
        with self.assertRaises(ValueError):
            cs.explained_checks(["break"])
        self.assertIn("3.3", cs.explained_checks(["break=the pending 3.3 dates M5 in the break"])["break"])


class NewOrderChecks(Base):
    def test_closeout_before_the_warranty_milestone_with_no_warranty_activity(self):
        text = HEAD + row(1, "1.10.2.1-A1", "Closeout report and lessons learned", "Mon 15 February 2027",
                          "Tue 16 February 2027") \
            + "| 2 |  | M7 First warranty month complete, project closeout | 0 days | <mark>Mon 22 March 2027</mark> | " \
              "<mark>Mon 22 March 2027</mark> |  |\n"
        found = [f for f in self.checks(text) if f.check == "closeout"]
        self.assertEqual(len(found), 1)
        self.assertIn("M7", found[0].message)

    def test_execution_before_the_function_package_is_built(self):
        text = HEAD + row(1, "1.4.1.3", "F03 Course catalog", "Thu 12 November 2026", "Thu 19 November 2026") \
            + row(2, "1.4.3.2-A1", "Test case authoring for F01 to F03", "Fri 6 November 2026", "Mon 9 November 2026") \
            + row(3, "1.4.3.2-A2", "Unit and integration execution", "Mon 9 November 2026", "Fri 13 November 2026")
        found = [f for f in self.checks(text) if f.check == "test-order"]
        self.assertEqual([f.line for f in found], [5])
        self.assertIn("F03", found[0].message)
        after = text.replace("Fri 13 November 2026", "Mon 23 November 2026")
        self.assertEqual([f for f in self.checks(after) if f.check == "test-order"], [])

    def test_review_before_the_thing_it_reviews_in_another_package(self):
        text = HEAD + row(1, "1.2.2.2-A2", "Technical review of the data model", "Mon 28 September 2026",
                          "Thu 1 October 2026") \
            + row(2, "1.3.1.2-A1", "Data model sketch for the twelve functions", "Mon 26 October 2026",
                  "Thu 29 October 2026")
        found = [f for f in self.checks(text) if f.check == "review-order"]
        self.assertEqual(len(found), 1)
        self.assertIn("data, model", found[0].message)

    def test_a_count_in_a_task_name_against_its_window(self):
        text = HEAD + row(1, "1.1.1.3-A1", "Weekly status report, 21 weeks", "Mon 14 September 2026",
                          "Mon 22 March 2027") \
            + row(2, "1.1.1.3-A2", "Weekly status report, 27 weeks", "Mon 14 September 2026", "Mon 22 March 2027")
        found = [f for f in self.checks(text) if f.check == "stated-count"]
        self.assertEqual([f.line for f in found], [3])

    def test_a_pilot_shorter_than_the_dictionary_states(self):
        scope = self.write("scope.md", "#### 1.8.1.3 Production deployment\n\n| Description of Work | Deploy the release, "
                           "pilot F01 to F06 at one branch for the two weeks before go-live, then switch over. |\n")
        text = HEAD + row(1, "1.8.1.3-A1", "Pilot deployment and support at one branch", "Wed 10 February 2027",
                          "Fri 12 February 2027")
        found = [f for f in self.checks(text, scope=scope) if f.check == "stated-count"]
        self.assertEqual(len(found), 1)
        self.assertIn("10 working days", found[0].message)
        long = text.replace("Fri 12 February 2027", "Tue 23 February 2027")
        self.assertEqual([f for f in self.checks(long, scope=scope) if f.check == "stated-count"], [])


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

    def test_the_difference_is_priced_at_the_dictionary_rates(self):
        scope = self.write("scope.md", self.SCOPE + (
            "| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total |\n"
            "| --- | --- | --- | ---: | ---: | ---: |\n"
            "| 1.1.1.1-A1 | Kickoff | PM | 8 | 100 | 800 |\n"
            "| 1.1.1.1-A2 | Build | DEV1 | 8 | 50 | 400 |\n"
            "| 1.1.1.1-A3 | App | MOB1 | 8 | 200 | 1,600 |\n"))
        found = self.checks(self.schedule("700", "800", "400"), scope=scope)
        self.assertIn("cost 190,000 against 200,000 priced, a difference of -10,000", found[0].message)

    def test_matching_hours_are_clean(self):
        scope = self.write("scope.md", self.SCOPE)
        self.assertEqual(self.checks(self.schedule("800", "800", "400"), scope=scope), [])


class Milestones(Base):
    GANTT = ("| ID | WBS | Task Name | Duration | Start | Finish | Resource Name |\n| --- | --- | --- | --- | --- | --- | --- |\n"
             "| 1 |  | M5 System test complete | 0 days | <mark>Mon 8 February 2027</mark> | <mark>Mon 8 February 2027</mark> |  |\n")
    PAGE2 = ("\n| ID | Indicator | Task Name | Finish |\n| --- | --- | --- | --- |\n"
             "| 1 | Charter date | M5 System test complete; app submitted | <mark>Mon 8 February 2027</mark> |\n")
    CHARTER = ("| ID | Milestone | Due date |\n| --- | --- | --- |\n"
               "| M5 | System test complete; app submitted | <mark>Fri 18 Dec 2026</mark> |\n")

    def test_a_shortened_milestone_name_is_one_id_with_two_texts(self):
        charter = self.write("charter.md", self.CHARTER)
        found = self.checks(self.GANTT + self.PAGE2, charter=charter)
        names = [f for f in found if f.check == "milestone-name"]
        self.assertEqual(len(names), 2)
        self.assertIn("page 2", names[0].message)
        self.assertIn("charter", names[1].message)

    def test_matching_names_and_dates_are_clean(self):
        page2 = self.PAGE2.replace("; app submitted", "")
        self.assertEqual([f for f in self.checks(self.GANTT + page2) if f.check == "milestone-name"], [])

    def test_a_date_that_differs_between_the_pages(self):
        page2 = self.PAGE2.replace("; app submitted", "").replace("8 February", "9 February")
        found = [f for f in self.checks(self.GANTT + page2) if f.check == "milestone-name"]
        self.assertEqual(len(found), 1)
        self.assertIn("dated", found[0].message)


class GoLive(Base):
    def test_go_live_before_the_uat_it_depends_on(self):
        text = HEAD + row(1, "1.8.1.3-A2", "Production deployment and switchover", "Wed 10 February 2027",
                          "Mon 15 February 2027") \
            + row(2, "1.8.3.2-A1", "UAT execution with the business owners", "Fri 12 February 2027",
                  "Wed 17 February 2027")
        found = [f for f in self.checks(text) if f.check == "go-live"]
        self.assertEqual([f.line for f in found], [3])
        self.assertIn("1.8.3.2-A1", found[0].message)

    def test_go_live_after_the_uat_is_clean(self):
        text = HEAD + row(1, "1.8.1.3-A2", "Production deployment and switchover", "Thu 18 February 2027",
                          "Fri 19 February 2027") \
            + row(2, "1.8.3.2-A1", "UAT execution with the business owners", "Fri 12 February 2027",
                  "Wed 17 February 2027")
        self.assertEqual([f for f in self.checks(text) if f.check == "go-live"], [])

    def test_uat_preparation_does_not_count_as_the_uat(self):
        text = HEAD + row(1, "1.8.1.3-A2", "Production deployment and switchover", "Wed 10 February 2027",
                          "Mon 15 February 2027") \
            + row(2, "1.6.2.2-A1", "UAT entry criteria review", "Wed 10 February 2027", "Tue 16 February 2027")
        self.assertEqual([f for f in self.checks(text) if f.check == "go-live"], [])


class NamedInput(Base):
    def test_a_review_names_the_activity_it_shares_words_with(self):
        text = HEAD + row(1, "1.7.1.3-A1", "Data extraction", "Mon 15 February 2027", "Wed 24 February 2027") \
            + row(2, "1.7.1.3-A2", "Reconciliation report production", "Fri 12 February 2027",
                  "Fri 19 February 2027") \
            + row(3, "1.7.1.3-A3", "Reconciliation verification", "Mon 8 February 2027", "Tue 9 February 2027")
        found = [f for f in self.checks(text) if f.check == "sequence"]
        self.assertEqual(len(found), 1)
        self.assertIn("1.7.1.3-A2", found[0].message)
        self.assertIn("2 activities", found[0].message)

    def test_a_closeout_names_the_warranty_activity(self):
        text = HEAD + row(1, "1.10.1.1-A1", "First warranty month support", "Thu 18 February 2027",
                          "Mon 22 March 2027") \
            + row(2, "1.10.1.3-A1", "Support desk handover", "Mon 15 February 2027", "Tue 23 March 2027") \
            + row(3, "1.10.2.1-A1", "Closeout report and lessons learned", "Mon 15 February 2027",
                  "Wed 17 February 2027")
        found = [f for f in self.checks(text) if f.check == "sequence"]
        self.assertIn("1.10.1.1-A1", found[0].message)


class Explained(Base):
    def test_a_pending_change_request_does_not_explain_an_order_defect(self):
        schedule = HEAD + row(1, "1.8.3.2-A1", "UAT execution", "Fri 12 February 2027", "Wed 17 February 2027") \
            + row(2, "1.8.3.2-A2", "Acceptance decision and sign-off", "Fri 12 February 2027",
                  "Mon 15 February 2027")
        path = self.write("s.md", schedule)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            cs.main([path, "--explained", "sequence"])
        self.assertEqual(raised.exception.code, 2)
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = cs.main([path, "--explained", "sequence=the sponsor moved sign-off ahead of UAT in 3.3"])
        self.assertEqual(code, 0)
        self.assertIn("explained: the sponsor moved sign-off ahead of UAT in 3.3, awaiting decision", out.getvalue())

    def test_an_unknown_check_is_refused(self):
        with self.assertRaises(ValueError):
            cs.explained_checks(["colour"])

    def test_explained_downgrades_the_named_check_only(self):
        scope = self.write("scope.md", Hours.SCOPE)
        schedule = Hours("schedule").schedule("1", "800", "400")
        plain = self.checks(schedule, scope=scope)
        soft = self.checks(schedule, scope=scope, explained=("hours",))
        self.assertEqual([f.level for f in plain if f.check == "hours"], ["error"])
        self.assertEqual([f.level for f in soft if f.check == "hours"], ["warning"])
        self.assertIn("explained, awaiting decision", soft[0].message)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cs.main([self.write("s.md", schedule), "--scope", scope, "--explained", "hours"]), 0)


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
