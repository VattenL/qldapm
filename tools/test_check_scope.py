"""Unit tests for the pure parts of check_scope.py."""

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import check_scope


SHEET = """#### 1.2.3.4 Example work package

**Project Title:** Example
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Example work package |
| Code of Accounts | 1.2.3.4 |
| Responsible Person | DEV2 |
| Description of Work | Something. |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.3.4-A1 | First activity | DEV2 | 28 | 118,750 | 3,325,000 | | | | 3,325,000 |
| 1.2.3.4-A2 | A purchase | | | | | 2 | 1,000,000 | 2,000,000 | 2,000,000 |
| | **Work package total** | | **28** | | **3,325,000** | | | **2,000,000** | **5,325,000** |

*Page 1 of 1*
"""

OUTLINE = """## Part 2: Work Breakdown Structure

```
1.        Project
1.1       Phase                                                       (major deliverable)
1.1.1       Account                                                   CA
1.1.1.1       Package one
1.1.1.2       Package two
```
"""

RTM = """### Requirement Information and Relationship Traceability

| ID | Requirement | Source | Priority | Category | Business Objective | Deliverable | Verification | Validation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR01 | Something | Director | Must have | Functional | Scope | 1.4.1.1 (D3) | Metric | Technique |
| FR02 | Something else | Director | Must have | Functional | Scope | 1.5.4.1, 1.9.1.3 (D4, D11) | Metric | Technique |

"""


class TestCells(unittest.TestCase):
    def test_splits_and_strips(self):
        self.assertEqual(check_scope.cells("| a | b |  c |"), ["a", "b", "c"])

    def test_money_handles_commas_bold_and_blank(self):
        self.assertEqual(check_scope.money("3,325,000"), 3325000)
        self.assertEqual(check_scope.money("**28**"), 28)
        self.assertEqual(check_scope.money(""), 0)


class TestParseOutline(unittest.TestCase):
    def setUp(self):
        self.outline = check_scope.parse_outline(OUTLINE)

    def test_finds_every_code(self):
        self.assertEqual(list(self.outline), ["1", "1.1", "1.1.1", "1.1.1.1", "1.1.1.2"])

    def test_marks_control_accounts_only(self):
        self.assertTrue(self.outline["1.1.1"])
        self.assertFalse(self.outline["1.1.1.1"])
        self.assertFalse(self.outline["1.1"])

    def test_missing_block_returns_empty(self):
        self.assertEqual(check_scope.parse_outline("no outline here"), {})


class TestParseSheets(unittest.TestCase):
    def setUp(self):
        self.sheet = check_scope.parse_sheets(SHEET)[0]

    def test_header_fields(self):
        self.assertEqual(self.sheet["code"], "1.2.3.4")
        self.assertEqual(self.sheet["name"], "Example work package")
        self.assertEqual(self.sheet["owner"], "DEV2")

    def test_labor_and_material_rows_are_separated(self):
        self.assertEqual(self.sheet["acts"], [("DEV2", 28, 118750, 3325000)])
        self.assertEqual(self.sheet["mats"], [(2, 1000000, 2000000)])

    def test_total_row(self):
        self.assertEqual(self.sheet["stated"], (28, 3325000, 2000000, 5325000))

    def test_field_table_rows_are_not_activities(self):
        self.assertEqual(len(self.sheet["acts"]) + len(self.sheet["mats"]), 2)


class TestParseRtmDeliverables(unittest.TestCase):
    def test_extracts_every_cited_code(self):
        self.assertEqual(
            check_scope.parse_rtm_deliverables(RTM),
            [("FR01", "1.4.1.1"), ("FR02", "1.5.4.1"), ("FR02", "1.9.1.3")],
        )

    def test_ignores_deliverable_ids_in_brackets(self):
        codes = [code for _, code in check_scope.parse_rtm_deliverables(RTM)]
        self.assertNotIn("D3", codes)


class TestReport(unittest.TestCase):
    def test_collects_failures(self):
        rep = check_scope.Report()
        rep.check(True, "fine")
        rep.check(False, "broken")
        self.assertEqual(rep.failures, ["broken"])


if __name__ == "__main__":
    unittest.main()
