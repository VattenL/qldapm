"""Unit tests for the Markdown subset parser in tools/gdoc_edit.py."""

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gdoc_edit as ge  # noqa: E402


class Inline(unittest.TestCase):
    def test_styles(self):
        plain, styles = ge.parse_inline("A **bold** and *it* with <mark>yellow</mark> and `c`.")
        self.assertEqual(plain, "A bold and it with yellow and c.")
        self.assertIn((2, 6, "bold"), styles)
        self.assertIn((11, 13, "italic"), styles)
        self.assertIn((19, 25, "mark"), styles)

    def test_nested_mark_in_bold(self):
        plain, styles = ge.parse_inline("**Team:** <mark>one</mark>")
        self.assertEqual(plain, "Team: one")
        self.assertEqual(sorted(styles), [(0, 5, "bold"), (6, 9, "mark")])


class Blocks(unittest.TestCase):
    MD = "### 1.2 Deliverables\n\nIntro line\ncontinues.\n\n| # | Name |\n| --- | --- |\n| D1 | One |\n\n- a\n- b\n\n1. x\n2. y\n\n> quoted\n\n| only |\n\n---\n"

    def test_types(self):
        kinds = [b["type"] for b in ge.parse_blocks(self.MD)]
        self.assertEqual(kinds, ["heading", "para", "table", "bullets", "numbered", "quote", "table", "hr"])

    def test_table_header_detection(self):
        tables = [b for b in ge.parse_blocks(self.MD) if b["type"] == "table"]
        self.assertTrue(tables[0]["header"])
        self.assertEqual(tables[0]["rows"], [["#", "Name"], ["D1", "One"]])
        self.assertFalse(tables[1]["header"])

    def test_para_joins_lines(self):
        para = ge.parse_blocks(self.MD)[1]
        self.assertEqual(para["text"], "Intro line continues.")

    def test_compose_and_requests(self):
        blocks = ge.parse_blocks("## H\n\nText <mark>y</mark>\n\n- a\n- b\n\n| c1 | c2 |\n| --- | --- |\n| v | w |\n")
        text, specs, tables = ge.compose_blocks(blocks)
        self.assertEqual(text, "H\nText y\na\nb\n@@TABLE0@@\n")
        self.assertEqual(len(tables), 1)
        reqs = ge.block_requests("t.0", 10, text, specs)
        kinds = [next(iter(r)) for r in reqs]
        self.assertEqual(kinds[0], "insertText")
        self.assertIn("createParagraphBullets", kinds)
        bullets = next(r for r in reqs if "createParagraphBullets" in r)["createParagraphBullets"]["range"]
        self.assertEqual((bullets["startIndex"], bullets["endIndex"]), (10 + 9, 10 + 13))
        heading = next(r for r in reqs if "updateParagraphStyle" in r and r["updateParagraphStyle"]["paragraphStyle"].get("namedStyleType") == "HEADING_2")
        self.assertEqual(heading["updateParagraphStyle"]["range"]["endIndex"], 12)


class Helpers(unittest.TestCase):
    MD = "## A\ntext\n### B\n| Field | Content |\n| --- | --- |\n| **X** | one |\n| F12 | Mobile | Actor | Desc |\n## C\n"

    def test_section_and_maps(self):
        sec = ge.section(self.MD, "### B", "## C")
        self.assertTrue(sec.startswith("### B"))
        self.assertEqual(ge.field_map(ge.first_table(sec))["X"], "one")
        self.assertEqual(ge.table_by_first_cell(self.MD, "F12")[1], "Mobile")


if __name__ == "__main__":
    unittest.main()
