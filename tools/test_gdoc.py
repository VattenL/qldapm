"""Unit tests for the pure parts of tools/gdoc.py. Run: python3 -m unittest tools/test_gdoc.py"""

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gdoc  # noqa: E402

THREADS = {
    "T1": {"id": "T1", "content": "Cao quá", "replies": [{"content": "99 thôi"}]},
    "T2": {"id": "T2", "content": "Bỏ", "replies": []},
    "N0": {"id": "N0", "content": "[Approvals] already there\nmore", "replies": []},
}


class PlanPosts(unittest.TestCase):
    def test_reply_and_new_comment(self):
        review = [
            {"thread": "T2", "location": "x", "reviewer": "V", "reply": "Đã bỏ.\nchi tiết"},
            {"new": True, "location": "Cover", "quote": "q", "content": "missing prompt log"},
        ]
        actions, skipped = gdoc.plan_posts(review, THREADS)
        self.assertEqual(skipped, [])
        self.assertEqual(actions[0][:2], ("reply", "T2"))
        self.assertEqual(actions[1][0], "comment")
        self.assertEqual(actions[1][2], "[Cover] missing prompt log")
        self.assertEqual(actions[1][3], "q")

    def test_idempotent(self):
        review = [
            {"thread": "T1", "location": "x", "reviewer": "V", "reply": "99 thôi\nsecond run"},
            {"new": True, "location": "Approvals", "quote": "q", "content": "already there\nmore"},
        ]
        actions, skipped = gdoc.plan_posts(review, THREADS)
        self.assertEqual(actions, [])
        self.assertEqual([s[0] for s in skipped], ["reply", "comment"])

    def test_unknown_thread(self):
        with self.assertRaises(KeyError):
            gdoc.plan_posts([{"thread": "nope", "location": "x", "reviewer": "V", "reply": "r"}], THREADS)


class Validate(unittest.TestCase):
    def test_rejects_bad_items(self):
        with self.assertRaises(ValueError):
            gdoc.validate_review([{"location": "x"}])
        with self.assertRaises(ValueError):
            gdoc.validate_review([{"thread": "T", "location": "x", "reviewer": "V"}])
        with self.assertRaises(ValueError):
            gdoc.validate_review([])


class Html(unittest.TestCase):
    def test_marks_and_page_breaks(self):
        html = gdoc.md_to_html("#### PROJECT CHARTER, page 2 of 4\n\nA <mark>B</mark>\n\n| a | b |\n| --- | --- |\n| 1 | 2 |", "T")
        self.assertIn('<span style="background-color:#ffff00">B</span>', html)
        self.assertIn('<div style="page-break-before:always"></div><h4>PROJECT CHARTER, page 2 of 4</h4>', html)
        self.assertIn("<table>", html)

    def test_marks_walker(self):
        content = [
            {"paragraph": {"elements": [{"textRun": {"content": "plain"}}, {"textRun": {"content": "yellow", "textStyle": {"backgroundColor": {"color": {}}}}}]}},
            {"table": {"tableRows": [{"tableCells": [{"tableCellStyle": {"backgroundColor": {"color": {"rgbColor": {}}}}, "content": [{"paragraph": {"elements": [{"textRun": {"content": "cell text"}}]}}]}]}]}},
        ]
        self.assertEqual(list(gdoc.iter_marks(content)), [("run", "yellow"), ("cell", "cell text")])


if __name__ == "__main__":
    unittest.main()
