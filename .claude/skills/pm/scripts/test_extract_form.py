"""Tests for extract_form.py --knowledge. Run: python3 -m unittest discover -s .claude/skills/pm/scripts"""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import extract_form

SCRIPT = Path(extract_form.__file__)


class KnowledgeText(unittest.TestCase):
    def setUp(self):
        self.forms = extract_form.load_index()

    def test_every_form_has_a_knowledge_file(self):
        for num in self.forms:
            self.assertTrue((extract_form.KNOWLEDGE_DIR / f"{num}.json").exists(), num)

    def test_every_form_renders_without_dashes(self):
        for num in self.forms:
            text = extract_form.describe_knowledge(extract_form.load_knowledge(num))
            self.assertIn("Fields, printed label", text, num)
            self.assertIn("Decisions recorded here", text, num)
            self.assertIsNone(re.search("[\\u2013\\u2014]", text), num)

    def test_every_guidance_text_is_printed(self):
        # Wrapping must not drop words: compare with whitespace squeezed.
        for num in ("1.1", "2.32", "4.4", "6.4"):
            know = extract_form.load_knowledge(num)
            text = " ".join(extract_form.describe_knowledge(know).split())
            for el in know["elements"]:
                self.assertIn(" ".join(el["guidance"].split()), text, (num, el["element"]))
            for dec in know["decisions"]:
                self.assertIn(" ".join(dec["decision"].split()), text, (num, dec["decision"]))

    def test_blank_only_labels_say_not_stated_and_cite_both_pages(self):
        for num in self.forms:
            for item in extract_form.load_knowledge(num).get("blank_only", []):
                self.assertTrue(item["note"].startswith("Not stated in the book"), (num, item))
                self.assertRegex(item["cite"], r"PDF page \d+ \(printed page \d+\)")
        text = extract_form.describe_knowledge(extract_form.load_knowledge("3.3"))
        self.assertIn("Printed on the blank form but not described by the book (3):", text)
        for label in ("Stakeholder Impact", "Disposition", "Justification"):
            self.assertIn("  - " + label + "\n", text)

    def test_blank_only_labels_are_printed_labels_of_the_form_and_not_elements(self):
        import check_fidelity
        for num in self.forms:
            know = extract_form.load_knowledge(num)
            if not know.get("blank_only"):
                continue
            printed = {check_fidelity.loose(label) for label in check_fidelity.all_labels(check_fidelity.load_spec(num))}
            elements = {check_fidelity.loose(e["printed_label"] or "") for e in know["elements"]}
            for item in know["blank_only"]:
                key = check_fidelity.loose(item["printed_label"])
                self.assertIn(key, printed, (num, item["printed_label"]))
                self.assertNotIn(key, elements, (num, item["printed_label"]))

    def test_label_sits_beside_its_guidance(self):
        know = extract_form.load_knowledge("2.32")
        text = extract_form.describe_knowledge(know)
        self.assertIn("  - Risk Statement [book element: Risk statement]\n", text)
        lines = text.splitlines()
        i = lines.index("  - Risk Statement [book element: Risk statement]")
        self.assertIn("The risk event or condition", lines[i + 1])

    def test_sources_consumers_and_citation(self):
        text = extract_form.describe_knowledge(extract_form.load_knowledge("2.32"))
        self.assertIn("Sources, information this form receives from (19):", text)
        self.assertIn("Consumers, information this form provides to", text)
        self.assertIn("PDF pages 139 to 140 (printed pages 128 to 129)", text)

    def test_empty_sections_are_named(self):
        text = extract_form.describe_knowledge(extract_form.load_knowledge("2.32"))
        self.assertIn("Alignment, must agree with: none listed in the book", text)
        self.assertIn("Tailoring tips: none printed for this form", text)

    def test_tailoring_and_alignment_print_when_present(self):
        text = extract_form.describe_knowledge(extract_form.load_knowledge("2.31"))
        self.assertIn("Tailoring tips (3):", text)
        self.assertIn("Alignment, must agree with (", text)
        self.assertIn("Agile or adaptive:", text)

    def test_missing_form_exits(self):
        with self.assertRaises(SystemExit):
            extract_form.load_knowledge("9.9")


class KnowledgeCli(unittest.TestCase):
    def run_cli(self, *args):
        # A scratch working directory with no PDF in it or above it proves no PDF is read.
        with tempfile.TemporaryDirectory() as tmp:
            return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=tmp,
                                  capture_output=True, text=True)

    def test_knowledge_alone_needs_no_pdf(self):
        out = self.run_cli("2.32", "--knowledge")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("## Knowledge, references/knowledge/2.32.json", out.stdout)
        self.assertNotIn("## Printed form", out.stdout)

    def test_knowledge_by_name(self):
        out = self.run_cli("risk register", "--knowledge")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("# 2.32 Risk Register", out.stdout)

    def test_knowledge_combines_with_fields(self):
        out = self.run_cli("4.4", "--knowledge", "--fields")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("## Field spec", out.stdout)
        self.assertIn("## Knowledge", out.stdout)
        self.assertIn("Selected EAC, Justification, and Explanation", out.stdout)


if __name__ == "__main__":
    unittest.main()
