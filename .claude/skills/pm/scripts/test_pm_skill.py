"""Tests for the pm skill helpers. Run: python3 -m unittest discover -s .claude/skills/pm/scripts"""

import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

import extract_form

SKILL = Path(__file__).resolve().parent.parent
REPO = SKILL.parent.parent.parent
DASHES = re.compile("[\u2013\u2014]")


class Index(unittest.TestCase):
    def setUp(self):
        self.forms = extract_form.load_index()

    def test_every_form_is_listed(self):
        self.assertEqual(len(self.forms), 66)
        for group, last in (("1", 4), ("2", 40), ("3", 7), ("4", 9), ("5", 2), ("6", 4)):
            for n in range(1, last + 1):
                self.assertIn(f"{group}.{n}", self.forms)

    def test_page_ranges_are_sane(self):
        for form in self.forms.values():
            prose, blank = form["prose"], form["blank"]
            self.assertLessEqual(prose[0], prose[1], form["num"])
            self.assertLessEqual(blank[0], blank[1], form["num"])
            self.assertLess(prose[1], blank[0], form["num"])

    def test_kinds_are_known(self):
        known = {"fields", "log", "matrix", "chart", "diagram", "outline", "narrative"}
        self.assertEqual({f["kind"] for f in self.forms.values()} - known, set())

    def test_lookup_by_name(self):
        self.assertEqual(extract_form.resolve(self.forms, "retrospective")["num"], "6.4")
        self.assertEqual(extract_form.resolve(self.forms, "2.32")["num"], "2.32")


class SliceSection(unittest.TestCase):
    PROSE = "\n".join([
        "2.9 WORK BREAKDOWN STRUCTURE", "Some purpose text.",
        "tailoring tips", "  - Roll up to deliverables.",
        "Alignment", "  - Scope statement",
        "Description", "Document element   Description", "Level   The WBS level",
    ])

    def test_picks_the_named_section(self):
        self.assertIn("Roll up", extract_form.slice_section(self.PROSE, "tailoring tips"))
        self.assertIn("Scope statement", extract_form.slice_section(self.PROSE, "alignment"))
        self.assertIn("The WBS level", extract_form.slice_section(self.PROSE, "description"))

    def test_sections_do_not_bleed_into_each_other(self):
        self.assertNotIn("Scope statement", extract_form.slice_section(self.PROSE, "tailoring tips"))

    def test_absent_section_is_empty(self):
        self.assertEqual(extract_form.slice_section("nothing here", "alignment"), "")


class KeyValues(unittest.TestCase):
    def test_header_block_splits_into_lines(self):
        import md_to_docx
        text = "**Project:** Learning Center **Date prepared:** 24 September 2026"
        self.assertEqual(len(md_to_docx.split_key_values(text)), 2)

    def test_plain_paragraph_is_left_alone(self):
        import md_to_docx
        text = "This paragraph mentions **bold** words but is not a header block."
        self.assertEqual(md_to_docx.split_key_values(text), [text])


class SkillFile(unittest.TestCase):
    """SKILL.md is read on every use, so its size, trigger text and pointers are checked."""

    def setUp(self):
        self.text = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    def test_stays_under_450_lines(self):
        self.assertLess(len(self.text.splitlines()), 450)

    def test_description_fits_and_triggers_on_decisions(self):
        desc = re.search(r"^description: (.*)$", self.text, re.M).group(1)
        self.assertLessEqual(len(desc), 1024)
        for word in ("schedule slip", "cost overrun", "risk response", "change request",
                     "earned value", "which form"):
            self.assertIn(word, desc)

    def test_version_and_no_dashes(self):
        self.assertIn("version: 2.5.0", self.text)
        self.assertIsNone(DASHES.search(self.text))

    def test_decision_path_names_its_tools_and_catalog(self):
        self.assertIn("## Deciding, not just documenting", self.text)
        for needle in ("references/decisions.md", "pm_calc.py", "form_graph.py --impact",
                       "extract_form.py 2.32 --knowledge", "3.2", "3.3", "change request"):
            self.assertIn(needle, self.text)

    def test_every_referenced_file_exists(self):
        for rel in re.findall(r"`((?:references|scripts|evals)/[A-Za-z0-9_./-]+)`", self.text):
            if "<" in rel or rel.endswith("/"):
                continue
            self.assertTrue((SKILL / rel).exists(), rel)

    def test_files_table_lists_every_script_and_reference(self):
        files = self.text[self.text.index("## Files"):]
        for script in ("extract_form.py", "new_form.py", "check_fidelity.py", "check_consistency.py",
                       "md_to_docx.py", "pm_calc.py", "form_graph.py", "check_schedule.py"):
            self.assertIn(script, files)
        for ref in ("decisions.md", "book-structure.md", "form-graph.md", "pmbok-quality.md",
                    "knowledge/<form>.json", "load-check.md", "push-audit.md", "book-counts.json"):
            self.assertIn(ref, files)

    def test_every_pmbok_note_is_in_the_form_to_note_table(self):
        for note in SKILL.glob("references/pmbok-*.md"):
            self.assertIn(note.name, self.text, note.name)


class Evals(unittest.TestCase):
    def setUp(self):
        self.evals = json.loads((SKILL / "evals" / "evals.json").read_text(encoding="utf-8"))["evals"]

    def test_ids_are_one_to_nine_and_complete(self):
        self.assertEqual([e["id"] for e in self.evals], list(range(1, 10)))
        for e in self.evals:
            for key in ("eval_name", "prompt", "expected_output", "files", "assertions"):
                self.assertTrue(e[key] or key == "files", (e["id"], key))
            self.assertGreaterEqual(len(e["assertions"]), 8, e["id"])

    def test_no_dashes_and_listed_files_exist(self):
        for e in self.evals:
            self.assertIsNone(DASHES.search(json.dumps(e, ensure_ascii=False)), e["id"])
            for f in e["files"]:
                self.assertTrue((REPO / f).exists(), (e["id"], f))

    def test_new_evals_cite_both_page_numbers_for_book_claims(self):
        for e in self.evals[5:]:
            joined = " ".join(e["assertions"])
            self.assertRegex(joined, r"printed pages? \d+", e["id"])
            self.assertRegex(joined, r"PDF pages? \d+", e["id"])

    def test_evm_eval_figures_match_pm_calc(self):
        out = subprocess.run(
            [sys.executable, str(SKILL / "scripts" / "pm_calc.py"), "evm", "--bac", "700000000",
             "--pv", "280000000", "--ev", "252000000", "--ac", "294000000", "--json"],
            capture_output=True, text=True, check=True)
        rows = {}
        for section in json.loads(out.stdout)["sections"]:
            for row in section["rows"]:
                rows.setdefault(row["label"], []).append(row["value"])
        text = " ".join(next(e for e in self.evals if e["id"] == 7)["assertions"])
        self.assertEqual(rows["CV"][0], -42000000)
        self.assertEqual(rows["SV"][0], -28000000)
        self.assertAlmostEqual(rows["CPI"][0], 0.857, places=3)
        self.assertAlmostEqual(rows["SPI"][0], 0.9, places=6)
        eacs = sorted(v for k, vs in rows.items() if k == "EAC" for v in vs)
        self.assertEqual([round(v) for v in eacs], [742000000, 816666667, 874740741])
        for figure in ("-42,000,000", "-28,000,000", "0.857", "816,666,667", "742,000,000",
                       "874,740,741", "1.1034"):
            self.assertIn(figure, text)

    def test_vietnamese_eval_prompt_is_vietnamese(self):
        prompt = next(e for e in self.evals if e["id"] == 9)["prompt"]
        self.assertIn("khach hang muon them chuc nang moi", prompt)


class Guides(unittest.TestCase):
    """The two team guides in docs/ describe the decision path and the new scripts."""

    GUIDES = ("pm-skill-guide.md", "pm-skill-guide.vi.md")

    def test_guides_cover_the_decision_path(self):
        for name in self.GUIDES:
            text = (REPO / "docs" / name).read_text(encoding="utf-8")
            for needle in ("pm_calc.py", "form_graph.py", "--knowledge", "decisions.md",
                           "khach hang muon them chuc nang moi", "## 8. ", "## 12. "):
                self.assertIn(needle, text, (name, needle))
            self.assertIsNone(DASHES.search(text), name)
            self.assertNotIn("PASSED_COUNT", text, name)

    def test_guides_have_the_same_numbered_sections(self):
        heads = [re.findall(r"^## (\d+)\. ", (REPO / "docs" / n).read_text(encoding="utf-8"), re.M)
                 for n in self.GUIDES]
        self.assertEqual(heads[0], heads[1])
        self.assertEqual(heads[0], [str(i) for i in range(1, 13)])

    def test_guides_list_every_pm_calc_subcommand(self):
        out = subprocess.run([sys.executable, str(SKILL / "scripts" / "pm_calc.py"), "--help"],
                             capture_output=True, text=True, check=True).stdout
        subs = ("evm", "pert", "effort-to-duration", "analogous", "bottom-up", "risk-score", "emv",
                "weighted-score", "earned-schedule", "cpm", "crash", "velocity", "cd3", "payback", "comms-channels",
                "reserve", "funding", "response-effectiveness")
        for sub in subs:
            self.assertIn(sub, out, sub)
            for name in self.GUIDES:
                text = (REPO / "docs" / name).read_text(encoding="utf-8")
                self.assertIn(f"| `{sub}` |", text, (name, sub))


class DecisionCatalog(unittest.TestCase):
    TEXT = (SKILL / "references" / "decisions.md").read_text(encoding="utf-8")
    FORM = re.compile(r"(?<![\d.])([1-6]\.\d{1,2})(?![\d])")

    def forms(self, cell):
        previous = None
        while previous != cell:
            previous, cell = cell, re.sub(r"\([^()]*\)", "", cell)
        return set(self.FORM.findall(cell))

    def test_also_record_column_equals_the_record_lines_of_the_row(self):
        record = {}
        for m in re.finditer(r"^### (D\d+) .*?\n(.*?)(?=^### |^## |\Z)", self.TEXT, re.S | re.M):
            r = re.search(r"^- Record: (.*)$", m.group(2), re.M)
            record[m.group(1)] = self.forms(r.group(1)) if r else set()
        rows = 0
        for line in self.TEXT.splitlines():
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) == 9 and c[0].isdigit():
                rows += 1
                needed = set().union(*[record.get(d, set()) for d in re.findall(r"D\d+", c[2])])
                listed = self.forms(c[4]) | self.forms(c[7])
                self.assertEqual(needed - listed, set(), "row " + c[0])
        self.assertEqual(rows, 40)

    def test_every_routed_decision_exists(self):
        defined = set(re.findall(r"^### (D\d+) ", self.TEXT, re.M))
        for line in self.TEXT.splitlines():
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) == 9 and c[0].isdigit():
                self.assertLessEqual(set(re.findall(r"D\d+", c[2])), defined, "row " + c[0])

    def test_late_schedule_row_reaches_resource_optimization(self):
        row = next(line for line in self.TEXT.splitlines() if line.startswith("| 6 |"))
        self.assertIn("D13", row)
        self.assertIn("6.5.2.3 p211 (PDF 250)", self.TEXT)

    def routing_rows(self):
        rows = []
        for line in self.TEXT.splitlines():
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) == 9 and c[0].isdigit():
                rows.append(c)
        return rows

    def test_every_row_names_an_impact_anchor_that_is_a_real_form(self):
        index = (SKILL / "references" / "forms-index.md").read_text(encoding="utf-8")
        real = set(re.findall(r"^\| (\d\.\d+) \|", index, re.M))
        for c in self.routing_rows():
            if c[8].startswith("none:"):
                self.assertEqual(c[2], "none", "only a pointer row has no anchor: row " + c[0])
                continue
            anchors = self.forms(c[8])
            self.assertTrue(anchors, "row " + c[0])
            self.assertLessEqual(anchors, real, "row " + c[0])
        self.assertIn("Impact anchor = the form", self.TEXT)

    def test_a_row_that_moves_a_baseline_names_3_3_as_an_anchor(self):
        for c in self.routing_rows():
            if "3.3" in c[3] or "3.3" in c[4]:
                if c[0] in ("9", "11", "35"):
                    self.assertIn("3.3", self.forms(c[8]), "row " + c[0])

    def test_imposed_date_and_favourable_variance_have_routes(self):
        rows = {c[0]: c for c in self.routing_rows()}
        self.assertIn("imposed", rows["37"][1])
        self.assertIn("D14", rows["37"][2])
        self.assertIn("6.5.2.6 p215 (PDF 254)", rows["37"][6])
        self.assertIn("favourable", rows["38"][1].lower())
        self.assertIn("D15", rows["38"][2])
        self.assertIn("4.6.3.2 p120 (PDF 159)", rows["38"][6])

    def test_the_calculator_list_equals_pm_calc_help(self):
        out = subprocess.run([sys.executable, str(SKILL / "scripts" / "pm_calc.py"), "--help"],
                             capture_output=True, text=True, check=True).stdout
        subs = set(re.sub(r"\s+", "", re.search(r"\{([^}]+)\}", out).group(1)).split(","))
        self.assertGreaterEqual(len(subs), 17)
        section1 = self.TEXT[self.TEXT.index("## 1. How to use it"):self.TEXT.index("## 2. Routing table")]
        listed = set(re.findall(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)*)`", section1.split("3. **Run the calculator**")[1].split("4. **Check")[0]))
        self.assertLessEqual(subs, listed, sorted(subs - listed))
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        listed_skill = set(re.findall(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)*)`", skill))
        self.assertLessEqual(subs, listed_skill, sorted(subs - listed_skill))

    def test_every_option_line_states_a_trade_off_or_says_it_is_not_stated(self):
        marker = re.compile(r"trade-off|not stated|no trade|stated (?:fit|condition|benefit|trade)|none stated|"
                            r"each with a stated|no (?:cost comparison|rule|criterion|threshold)|no weights|"
                            r"no scale or response time|differ", re.I)
        missing = []
        for m in re.finditer(r"^### (D\d+) .*?\n(.*?)(?=^### |^## )", self.TEXT, re.S | re.M):
            options = re.search(r"^- Options.*?(?=^- (?:Inputs and calc|Step 0)|\Z)", m.group(2), re.S | re.M)
            if options and not marker.search(options.group(0)):
                missing.append(m.group(1))
        self.assertEqual(missing, [], "add the book's stated trade-off or 'not stated in the book'")

    def test_change_path_does_not_give_a_false_reason_for_the_3_4_order(self):
        self.assertNotIn("because 3.4 carries Status and Disposition", self.TEXT)
        self.assertNotIn("Do not put the 3.4 record before the decision", self.TEXT)
        self.assertIn("from the change request through the", self.TEXT)
        self.assertIn("team's convention", self.TEXT)

    def test_risk_response_table_has_five_strategies_and_isolation_is_avoid(self):
        body = re.search(r"^### D36 .*?(?=^### |^## )", self.TEXT, re.S | re.M).group(0)
        self.assertIn("is avoid by the book", body)
        self.assertIn("Who pays", body)
        self.assertIn("exactly the five threat", self.TEXT)

    def test_new_routing_rows_exist_for_a_deviation_and_for_which_form(self):
        rows = {c[0]: c for c in self.routing_rows()}
        self.assertIn("revised baseline", rows["39"][1])
        self.assertIn("D05", rows["39"][2])
        self.assertIn("Which form", rows["40"][1])
        self.assertIn("1.2", self.forms(rows["1"][3]))
        self.assertIn("D02", rows["1"][2])

    def test_decisions_name_the_calculator_where_one_exists(self):
        for d, sub in (("D17", "reserve"), ("D18", "reserve"), ("D19", "funding"), ("D19", "payback"),
                       ("D36", "response-effectiveness")):
            body = re.search(r"^### %s .*?(?=^### |^## )" % d, self.TEXT, re.S | re.M).group(0)
            self.assertIn("pm_calc.py " + sub, body, (d, sub))
        for stale in ("Calc: no subcommand", "no subcommand.", "work it by hand"):
            self.assertNotIn(stale, self.TEXT)

    def test_late_schedule_entry_tests_the_allowance_and_the_network(self):
        body = re.search(r"^### D14 .*?(?=^### |^## )", self.TEXT, re.S | re.M).group(0)
        for needle in ("same cause and the same milestone", "assumed", "no network", "imposed",
                       "PV and EV of the item", "PM 6.5.2.6 p215 (PDF 254)"):
            self.assertIn(needle, body, needle)

    def test_new_function_entry_says_who_pays(self):
        body = re.search(r"^### D07 .*?(?=^### |^## )", self.TEXT, re.S | re.M).group(0)
        self.assertIn("Who pays", body)
        self.assertIn("additional funding or an approved reserve draw", body)

    def test_change_path_states_the_eight_steps_in_order(self):
        section = self.TEXT[self.TEXT.index("## 4. Integrated change control path"):self.TEXT.index("## 5. Recommendation format")]
        order = section[section.index("**Order to state"):].split("\n\n")[0]
        positions = [order.index(w) for w in ("trigger", "the request on 3.3", "impact analysis of time, cost, resources and risk",
                                              "the decision", "the record in 3.4", "tell the requester", "implement",
                                              "update the affected documents")]
        self.assertEqual(positions, sorted(positions))

    def test_authority_limits_block_is_named_and_referenced(self):
        self.assertIn("**Authority limits to read from 1.1.**", self.TEXT)
        for d in ("D14", "D15", "D16", "D17", "D18", "D26"):
            body = re.search(r"^### %s .*?(?=^### |^## )" % d, self.TEXT, re.S | re.M).group(0)
            self.assertIn("Authority limits", body, d)


class ProjectFactsAreCurrent(unittest.TestCase):
    """The reference files point at where a project fact lives and never copy a money figure: a copy goes stale
    silently and an answer can quote it instead of reading docs/. A date a note quotes must still occur in the
    project documents."""

    AMOUNT = re.compile(r"\b\d{1,3}(?:,\d{3}){2,}\b|\b\d[\d,.]*\s*(?:VND|USD|dong)\b")
    DATE = re.compile(r"\b\d{1,2} (?:%s) \d{4}\b" % "|".join(
        "January February March April May June July August September October November December".split()))
    CHECKED = ("pmbok-*.md", "decisions.md", "house-style.md", "load-check.md", "push-audit.md", "rendering.md")

    def files(self):
        out = []
        for pattern in self.CHECKED:
            out += sorted((SKILL / "references").glob(pattern))
        return out

    def test_no_reference_file_copies_a_currency_amount(self):
        for path in self.files():
            found = sorted({m.group(0) for m in self.AMOUNT.finditer(path.read_text(encoding="utf-8"))})
            self.assertEqual(found, [], "%s copies a figure; point at the file and heading instead" % path.name)

    def test_dates_in_the_notes_occur_in_docs(self):
        docs = REPO / "docs"
        sources = [docs / "charter-package.en.md", docs / "scope-package.en.md"] + sorted((docs / "forms").glob("*.md"))
        if not all(p.exists() for p in sources[:2]):
            self.skipTest("needs the charter and scope packages")
        corpus = "\n".join(p.read_text(encoding="utf-8") for p in sources)
        for path in sorted((SKILL / "references").glob("pmbok-*.md")) + [SKILL / "references" / "decisions.md"]:
            stale = sorted({m for m in self.DATE.findall(path.read_text(encoding="utf-8")) if m not in corpus})
            self.assertEqual(stale, [], path.name)


QUOTE = re.compile(r'"([^"()]{12,200})"')
CITE = re.compile(r"(?:^|[\s(,;])(PM|APG|BoF)\s[^()]*\(PDF (\d+)")
# Note style: "(printed 354, PDF 393)", "(p426/465)", "(X3.6 p138 (948))". The book is not named, so either PDF may hold it.
ALT_CITE = re.compile(r"^\s*\((?:printed \d+, PDF (\d+)|p\d+(?:\s+to\s+\d+)?/(\d+)|(?:APG |PM |BoF )?[A-Z0-9.]+ p\d+ \((\d+)\))")
NOTE_CITE = re.compile(r"^[^.]{0,120}?(PMBOK|Book of Forms|Agile Practice Guide)[^.]{0,120}?PDF pages? (\d+)")


def squeeze(text):
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    return re.sub(r"[^a-z0-9]+", " ", re.sub(r"-\s*\n\s*", "", text.lower())).strip()


@unittest.skipUnless(shutil.which("pdftotext") and (REPO / "PMBOK6_and_Agile_Practice_Guide.pdf").exists()
                     and (REPO / "A_Project_Managers_Book_of_Forms.pdf").exists(), "needs pdftotext and both PDFs")
class QuotesAreOnTheCitedPage(unittest.TestCase):
    """A short quotation followed by its citation must occur on the cited PDF page or the page after it
    (a quotation can straddle a page break; the PMBOK text is interleaved with a watermark, so a quotation
    also passes when the three words after its first and the three before its last are found)."""

    PDF = {"PM": "PMBOK6_and_Agile_Practice_Guide.pdf", "APG": "PMBOK6_and_Agile_Practice_Guide.pdf",
           "BoF": "A_Project_Managers_Book_of_Forms.pdf", "PMBOK": "PMBOK6_and_Agile_Practice_Guide.pdf",
           "Agile Practice Guide": "PMBOK6_and_Agile_Practice_Guide.pdf",
           "Book of Forms": "A_Project_Managers_Book_of_Forms.pdf"}
    cache = {}

    def page(self, book, n):
        key = (book, n)
        if key not in self.cache:
            out = subprocess.run(["pdftotext", "-layout", "-f", str(n), "-l", str(n), str(REPO / self.PDF[book]), "-"],
                                 capture_output=True, text=True).stdout
            self.cache[key] = squeeze(out)
        return self.cache[key]

    def found(self, book, n, quote):
        words = squeeze(quote).split()
        for page in (n - 1, n, n + 1):
            text = self.page(book, page)
            if " ".join(words) in text:
                return True
            # the watermark lines of the PMBOK pages can fall inside a quotation: match its inner words in pieces
            core = words[1:-1] if len(words) >= 5 else []
            if core and " ".join(core[:3]) in text and " ".join(core[-3:]) in text:
                return True
        return False

    def check(self, path):
        checked, missing = 0, []
        for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
            for m in QUOTE.finditer(line):
                tail = line[m.end():m.end() + 160]
                c = CITE.search(tail)
                if c:
                    book, page = c.group(1), int(c.group(2))
                else:
                    c = NOTE_CITE.match(tail)
                    if c:
                        book, page = c.group(1), int(c.group(2))
                    else:
                        c = ALT_CITE.match(tail)
                        if not c:
                            continue
                        book, page = None, int(next(g for g in c.groups() if g))
                checked += 1
                books = (book,) if book else ("PM", "BoF")
                if not any(self.found(b, page, m.group(1)) for b in books):
                    missing.append((n, book, page, m.group(1)))
        return checked, missing

    def test_decisions_quotations(self):
        checked, missing = self.check(SKILL / "references" / "decisions.md")
        self.assertGreater(checked, 10)
        self.assertEqual(missing, [])

    def test_note_quotations(self):
        for path in sorted((SKILL / "references").glob("pmbok-*.md")):
            _checked, missing = self.check(path)
            self.assertEqual(missing, [], path.name)


if __name__ == "__main__":
    unittest.main()
