"""Tests for risk_actions.py. Run: uv run --with pytest pytest -q .claude/skills/pm/scripts"""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import risk_actions as ra

PACKAGE = """#### 1.2.3.2 Notification gateway proof of concept

#### 1.2.3.3 Cross-platform framework proof

### Coverage check

| Charter item | Where the WBS delivers it |
| --- | --- |
| R1 to R2 responses | Owned by 1.1.1.4. R1 1.2.3.2 and 1.2.3.3; R2 1.2.3.2. |
"""


class Actions(unittest.TestCase):
    def test_a_work_package_is_written_with_its_title_and_several_are_joined_by_a_semicolon(self):
        titles = ra.sheet_titles(PACKAGE)
        found, missing = ra.actions(ra.coverage_row(PACKAGE)[1], titles)
        self.assertEqual(found, {"R1": ["1.2.3.2", "1.2.3.3"], "R2": ["1.2.3.2"]})
        self.assertEqual(missing, [])
        self.assertEqual(ra.render(found["R1"], titles),
                         "Work package 1.2.3.2, Notification gateway proof of concept; "
                         "Work package 1.2.3.3, Cross-platform framework proof")

    def test_a_code_with_no_sheet_is_reported_and_the_exit_code_is_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scope.md"
            path.write_text(PACKAGE.replace("#### 1.2.3.3 Cross-platform framework proof\n", ""), encoding="utf-8")
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                self.assertEqual(ra.main([str(path)]), 1)
            self.assertIn("no sheet for 1.2.3.3", err.getvalue())

    def test_no_coverage_row_and_a_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scope.md"
            path.write_text("# nothing\n", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(ra.main([str(path)]), 1)
                self.assertEqual(ra.main([str(path) + ".missing"]), 2)

    def test_one_risk_and_the_source_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "scope.md"
            path.write_text(PACKAGE, encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(ra.main([str(path), "--risk", "R2"]), 0)
            lines = out.getvalue().splitlines()
            self.assertTrue(lines[0].startswith("R2\t"))
            self.assertEqual(len(lines), 2)
            self.assertTrue(lines[1].startswith("source: "))


if __name__ == "__main__":
    unittest.main()
