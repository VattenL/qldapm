"""Consistency checks a reviewer would otherwise make by hand.

Each check here comes from a finding in review/2026-09-16-doc-review.md or
review/2026-09-24-doc-audit.md; references/review-lessons.md explains why each
one matters. The checks read Markdown only and never edit it.

Usage:
    python3 check_consistency.py docs/charter-package.en.md docs/scope-package.en.md
    python3 check_consistency.py docs/forms/<file>.md docs/charter-package.en.md \\
        docs/scope-package.en.md --report docs/forms/<file>.md

The words charter and scope stand for docs/charter-package.en.md and docs/scope-package.en.md when no file of
that name exists.

Pass every document of a deliverable together: ID families defined in one file
(risks in the charter) are referenced from another (the RTM), a range is only
stale relative to the definitions pooled across all files given, and a section
reference may point at a heading in another file.

--report PATH judges PATH against the other files but prints and counts only
what PATH contributes: findings located in PATH, and findings in the other files
that appear only because PATH was added (a range PATH made stale, an ID whose
text PATH changes). Findings already present in the context files are counted
in one line and not shown, so a clean new form exits 0 even when its sources
still carry errors. --report may be repeated; given without a value it reports
on the first path. A report path that is not among the paths is added to them.

--audit also reports a uniform column that the text above its table explains (a reason does not make a
constant column informative); use it when reviewing documents.

--group prints one line per check and level (count, files, first location and message, the next lines) instead of
one line per finding, since one defect often shows as a finding for every date or citation it touches.
--show-context, with --report, also lists the findings left out as already in the context files, each with
the heading it sits under, so they can be checked for any that touch the table under review.
--today YYYY-MM-DD checks every Date Prepared against that day: one dated after it is an error, one before it a
warning to confirm the content was last checked on that date (off unless the day is given).

A stated count ("all fourteen elements of Table 1.1") is compared with the table or list printed straight
after it, and the same count elsewhere in the file is reported with it.

Exit code 1 when any shown error is found, 0 when only warnings or nothing,
2 for a usage error such as a missing file.
"""

import argparse
import datetime
import json
import os
import re
import sys
from collections import defaultdict, namedtuple
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December")
SHORT_MONTHS = ("Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sept", "Sep", "Oct", "Nov", "Dec")
WEEKDAY = r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)"

FULL_DATE = re.compile(r"\b(%s )?(\d{1,2}) (%s) (\d{4})\b" % (WEEKDAY, "|".join(MONTHS)))
# "5 Jan 2027", "5 Jan. 2027", "Mon 14 Sep" with no year, and "5 May. 2027". "5 May." without a
# year is the full month at the end of a sentence, so May needs both the dot and the year.
SHORT_DATE = re.compile(r"\b(?:%s )?\d{1,2} (?:(?:%s)\.?(?: \d{4})?|May\. \d{4})(?!\w)"
                        % (WEEKDAY, "|".join(SHORT_MONTHS)))
# ISO, month first, and numeric dates: none is the house format.
OTHER_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b(?:%s)\.? \d{1,2}, \d{4}\b|\b\d{1,2}/\d{1,2}/\d{4}\b"
                        % "|".join(MONTHS + SHORT_MONTHS))

# ID families: a letter prefix and a number, as in F01, D4, R12, M0, A03, BR05, NFR02.
ID = re.compile(r"\b([A-Z]{1,3})(\d{1,3})\b")
RANGE = re.compile(r"\b([A-Z]{1,3})(\d{1,3})(?: to | through |-|\u2013)\1?(\d{1,3})\b")
SECTION_REF = re.compile(r"(?:\b(?:[Ss]ections?|Parts?) +|\u00a7 *)(\d+(?:\.\d+)*[A-Z]?)\b")
# Words just before a reference that send it to another document: the book, PMBOK, a file name
# or a code span (file names are written in backticks), or the charter.
EXTERNAL_REF = re.compile(r"(?:PMBOK|Guide|\.md|the book|book's|`)\W*(?:[\w-]+\W+){0,3}$", re.I)
# The same, when a page citation sits between the document and the section ("PMBOK 6, printed page 442,
# section 11.5.2.1"): any clause that names the book, PMBOK or the Guide before the reference.
EXTERNAL_CLAUSE = re.compile(r"\b(?:PMBOK|the Guide|Book of Forms|Agile Practice Guide|the book)\b", re.I)
CLAUSE_START = re.compile(r"(?<=[.;:!?])\s+(?=\S)")
CHARTER_REF = re.compile(r"\bcharter(?:'s)?\W+(?:[\w-]+\W+){0,3}$", re.I)
# The same, written after the reference: "Part 2 of `docs/scope-package.en.md`", "section 1.6 of the
# charter", "section 4.1.3.1 of the PMBOK Guide". File names in code spans are blanked to spaces
# between their backticks, so a backtick is enough.
EXTERNAL_AFTER = re.compile(r"^\W{0,2}\s*(?:of|in)\s+(?:the\s+)?(?:`|[\w-]+\.md\b|book\b|PMBOK|Guide\b)", re.I)
CHARTER_AFTER = re.compile(r"^\W{0,2}\s*(?:of|in)\s+(?:the\s+)?(?:project\s+)?charter\b", re.I)
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
HEADING_NUMBER = re.compile(r"^(?:(?:Part|Section)\s+)?(\d+(?:\.\d+)*[A-Z]?)[.:]?(?:\s|$)")
HTML_TAG = re.compile(r"</?([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>")
ENTITY = re.compile(r"&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);")
EM_DASH = re.compile(r"\u2014|&mdash;|&#8212;|&#x2014;", re.I)
# Pictographs and the miscellaneous symbol and dingbat blocks, except the three text symbols a
# checklist may use: ballot box U+2610, ballot box with X U+2612 and check mark U+2713. None of
# the three has an emoji presentation.
EMOJI = re.compile("[\\U0001F300-\\U0001FAFF\\u2600-\\u260F\\u2611\\u2613-\\u2712\\u2714-\\u27BF]")
NUMBER = re.compile(r"^(-?\d[\d,]*(?:\.\d+)?)\s*(%|VND|h|hours?)?$")
TOTAL_LABEL = re.compile(r"^(?:\S+ )?(?:sub-?|grand )?totals?\b(?: \S+){0,2}$", re.I)
ID_HEADERS = ("id", "#", "code", "risk id", "req id", "req. id", "requirement id")
# Columns that say what an ID is. Status, dates, actions and comments change over time and differ
# between a register and its history by design, so they are not compared.
IDENTITY = {"source", "name", "requirement", "risk statement", "description", "deliverable",
            "business requirement", "technical requirement", "priority"}
MERGED_ROLE = re.compile(
    r"Director,?\s+(?:and\s+)?sponsor|sponsor,?\s+(?:and\s+)?(?:owner|(?:Center\s+)?Director)"
    r"|sponsor of the (?:learning )?center", re.I)
# A role word in apposition to a name: "Name, owner and Center Director", "Name (sponsor)".
APPOSITION = r"%s\s*[,(:]\s*(?:the\s+)?(?:[\w-]+\s+){0,3}?(?:%s)\b"
FORM_PAGE = re.compile(r"^#### .+, page \d+ of \d+\s*$")
# A page citation: "page 14", "pages 78 to 81". "page 2 of 4" is a page of a form, not of the book.
PAGE_CITE = re.compile(r"\b[Pp]ages?\s+(\d+)(?:\s*(?:to|and|-|\u2013)\s*(\d+))?\b(?!\s+of\s+\d)")
# First cells that head a stakeholder list: 1.3 Name, 1.4 Name or Role, the charter's Stakeholder.
STAKEHOLDER_KEYS = ("name", "name or role", "stakeholder", "stakeholder(s)")

# A range that stops one or two short of the last defined ID is usually a range that was not
# moved when the family grew (R1 to R10 after R12 was added). Further short than that, it is
# usually a deliberate subset such as an iteration.
NEAR_END = 2
# Below three members a family is too small to tell a subset from a stale range.
MIN_FAMILY = 3
NUMBER_WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
    "seventeen eighteen nineteen twenty".split())}
NUMBER_WORDS.update({"twenty-one": 21, "twenty-two": 22, "twenty-three": 23, "twenty-four": 24,
                     "twenty-five": 25, "thirty": 30})
COUNT_NOUNS = ("elements|risks|milestones|rows|functions|deliverables|requirements|criteria|assumptions|"
               "stakeholders|work packages|activities|phases|columns|fields|constraints|exclusions|roles|"
               "forms|steps|items|sections|findings|cases")
# "all fourteen elements", "13 rows", "twelve functions F01 to F12": a number, up to two words, a noun
# that names things a list holds.
COUNT_CLAIM = re.compile(r"\b(?:all|the|these|those|every one of the)\s+(\d{1,3}|%s)\s+(?:[\w'-]+\s+){0,2}?(%s)\b"
                         % ("|".join(NUMBER_WORDS), COUNT_NOUNS), re.I)
LIST_ITEM = re.compile(r"^(\s*)(?:[-*+]|\d+[.)])\s+\S")
# A short table often has one value throughout for a good reason; from eight rows on, a column
# with one value is more likely a default nobody revisited.
MIN_ROWS_FOR_UNIFORM = 8


class Finding(namedtuple("Finding", "level check path line message")):
    __slots__ = ()

    def __str__(self):
        return "%s %s:%d [%s] %s" % (self.level.upper(), self.path, self.line, self.check, self.message)


def lines_outside_code(text):
    """Yield (line_number, line) for lines outside fenced code blocks.

    Inline code is blanked to spaces between its backticks, so nothing written as
    code is checked and column positions stay the same.
    """
    fenced = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            yield n, re.sub(r"`[^`]*`", lambda m: "`" + " " * (len(m.group(0)) - 2) + "`", line)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def plain(text):
    return re.sub(r"</?mark>|\*\*|\*", "", text).strip()


def tables(numbered_lines):
    """Group consecutive pipe-table lines into (start_line, header, rows) with row line numbers."""
    block = []
    for n, line in list(numbered_lines) + [(0, "")]:
        if line.lstrip().startswith("|"):
            block.append((n, line))
            continue
        if len(block) >= 2 and re.match(r"^\|?\s*:?-{3,}", block[1][1].strip()):
            header = cells(block[0][1])
            rows = [(n2, cells(l2)) for n2, l2 in block[2:]]
            yield block[0][0], header, rows
        block = []


def printed_labels():
    """Every printed label in references/fields/*.json, lower case: field labels, column and row
    labels, check box labels and options, and printed text blocks."""
    labels = set()

    def walk(node, key=None):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, k)
        elif isinstance(node, list):
            for v in node:
                walk(v, key)
        elif isinstance(node, str) and key in ("title_block", "labels", "columns", "row_labels",
                                                           "label", "options", "text"):
            labels.add(node.lower())

    for p in sorted((SKILL_DIR / "references" / "fields").glob("*.json")):
        try:
            walk(json.loads(p.read_text(encoding="utf-8")))
        except ValueError:
            continue
    return labels


def load_terms():
    """(never, instead, why) rows of every 'Never write | Write instead | Why' table in references/."""
    terms = []
    for p in sorted((SKILL_DIR / "references").glob("*.md")):
        lines = list(enumerate(p.read_text(encoding="utf-8").splitlines(), 1))
        for _start, header, rows in tables(lines):
            if [plain(h).lower() for h in header[:2]] != ["never write", "write instead"]:
                continue
            for _n, row in rows:
                if len(row) >= 2 and plain(row[0]):
                    terms.append((plain(row[0]), plain(row[1]), plain(row[2]) if len(row) > 2 else ""))
    return terms


def load_parties():
    """(party, [names], why) rows of every 'External party | Written as | Why' table in references/."""
    parties = []
    for p in sorted((SKILL_DIR / "references").glob("*.md")):
        lines = list(enumerate(p.read_text(encoding="utf-8").splitlines(), 1))
        for _start, header, rows in tables(lines):
            if [plain(h).lower() for h in header[:2]] != ["external party", "written as"]:
                continue
            for _n, row in rows:
                if len(row) >= 2 and plain(row[0]):
                    names = [x.strip() for x in plain(row[1]).split(";") if x.strip()]
                    parties.append((plain(row[0]), names, plain(row[2]) if len(row) > 2 else ""))
    return parties


def longest_form():
    """The most pages any printed form has; a page number above it cannot be a form's own page."""
    most = 1
    for p in (SKILL_DIR / "references" / "fields").glob("*.json"):
        try:
            most = max(most, int(json.loads(p.read_text(encoding="utf-8")).get("page_count", 1)))
        except (ValueError, TypeError):
            continue
    return most


RULE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")


def check_markup(path, lines, labels, out):
    for i, (n, line) in enumerate(lines):
        if RULE.match(line) and i and lines[i - 1][1].lstrip().startswith("|") and lines[i - 1][0] == n - 1:
            out.append(Finding("error", "table-rule", path, n,
                               "a horizontal rule directly under a table row is read as a table row by the Doc "
                               "generator and arrives as a stray '---' cell; leave a blank line between the "
                               "table and the rule"))
        for m in HTML_TAG.finditer(line):
            if m.group(1).lower() != "mark":
                out.append(Finding("error", "html", path, n,
                                   "<%s> will reach the Google Doc as literal text; only <mark> is converted"
                                   % m.group(1)))
        if EM_DASH.search(line):
            out.append(Finding("error", "em-dash", path, n, "em dash; use a comma, semicolon or full stop"))
        for m in ENTITY.finditer(line):
            if not EM_DASH.fullmatch(m.group(0)):
                out.append(Finding("error", "html", path, n,
                                   "%s will reach the Google Doc as literal text; write the character"
                                   % m.group(0)))
        if EMOJI.search(line):
            out.append(Finding("error", "emoji", path, n, "emoji in a project document"))
        first_cell = cells(line)[0] if line.lstrip().startswith("|") else ""
        whole_mark = re.fullmatch(r"<mark>([^<]*)</mark>", first_cell)
        if (any(re.fullmatch(r"\s*<mark>[^<]*</mark>\s*:?\s*", b) for b in re.findall(r"\*\*(.+?)\*\*", line))
                or re.match(r"^\s*<mark>\s*\*\*[^*]+\*\*\s*</mark>", line)
                or re.fullmatch(r"<mark>\s*\*\*[^*]+\*\*\s*</mark>", first_cell)
                or (whole_mark and plain(whole_mark.group(1)).rstrip(":").lower() in labels)):
            out.append(Finding("error", "mark-on-label", path, n,
                               "a label is highlighted; highlight marks uncertain content, never a label"))
            continue
        h = HEADING.match(line)
        if h and "<mark>" in h.group(2):
            out.append(Finding("error", "mark-on-label", path, n, "a heading is highlighted"))


def check_terms(path, lines, terms, out):
    """Words house-style.md forbids, from its 'Never write' table. A denial ('no X') is allowed."""
    for never, instead, why in terms:
        pattern = re.compile(r"\b%s\b" % re.escape(never), re.I)
        for n, line in lines:
            for m in pattern.finditer(line):
                if re.search(r"\b(?:no|not|never|nor)\b(?:\s+\w+)?\s*$", line[:m.start()], re.I):
                    continue
                out.append(Finding("error", "term", path, n, "'%s': write '%s'%s"
                                   % (m.group(0), instead, "; " + why if why else "")))


def date_blocks(lines):
    """Map each table line to the block its dates must agree within, and (line, text) pairs to scan.

    The house rule is one date style per table, read as per column: the Due Dates
    column of a dictionary sheet may carry weekdays while Date Prepared does not.
    In a field table (headed Field, or with every first cell bold) each field is
    its own block. Prose lines are one block, keyed 0.
    """
    blocks = {}
    for start, header, rows in tables(lines):
        fields = (plain(header[0]).lower() in ("field", "")
                  or all(re.fullmatch(r"\*\*[^*]+\*\*:?", row[0]) for _n, row in rows if row and row[0]))
        for n, row in rows:
            for col, cell in enumerate(row):
                if fields:
                    blocks[(n, col)] = (start, plain(row[0]).lower()) if col else (start, "#label", n)
                else:
                    blocks[(n, col)] = (start, col)
    return blocks


def check_dates(path, lines, out):
    """House format is '2 September 2026'; a weekday prefix only if every date beside it has one."""
    blocks = date_blocks(lines)
    styles = defaultdict(lambda: defaultdict(list))
    for n, line in lines:
        pieces = list(enumerate(cells(line))) if (n, 0) in blocks else [(None, line)]
        for col, text in pieces:
            block = blocks.get((n, col), 0)
            for m in OTHER_DATE.finditer(text):
                out.append(Finding("error", "date", path, n,
                                   "'%s' is not in the house format; write it as 2 September 2026" % m.group(0)))
            for m in FULL_DATE.finditer(text):
                if m.group(2).startswith("0"):
                    out.append(Finding("error", "date", path, n,
                                       "leading zero in '%s'; write the day without it" % m.group(0)))
                styles[block]["weekday" if m.group(1) else "plain"].append(n)
            for m in SHORT_DATE.finditer(text):
                out.append(Finding("error", "date", path, n,
                                   "abbreviated month in '%s'; write the month in full" % m.group(0).rstrip(".")))
    for block, found in styles.items():
        if len(found) > 1:
            first = min(v[0] for v in found.values())
            summary = ", ".join("%s %d (first line %d)" % (k, len(v), v[0]) for k, v in sorted(found.items()))
            where = "this table column" if block else "the prose of this file"
            out.append(Finding("warning", "date-style", path, first,
                               "%s mixes date styles: %s" % (where, summary)))


def definitions(files):
    """Highest number defined per ID family.

    An ID counts as defined where it opens a table row, a list item or a heading,
    which is how every register in this repo introduces its entries.
    """
    defined = defaultdict(set)
    for _path, lines in files:
        for _n, line in lines:
            first = None
            if line.lstrip().startswith("|"):
                row = cells(line)
                first = plain(row[0]) if row else None
                if not first and len(row) > 1:
                    first = plain(row[1])
            else:
                m = re.match(r"^\s*(?:[-*]|\d+\.|#{1,6})\s+\**([A-Z]{1,3}\d{1,3})\b", line)
                first = m.group(1) if m else None
            if first:
                m = re.match(r"^([A-Z]{1,3})(\d{1,3})\b", first)
                if m:
                    defined[m.group(1)].add(int(m.group(2)))
    return defined


def check_ranges(path, lines, defined, out):
    """A range past the last defined ID is an error; one that starts at the first ID and stops
    NEAR_END or fewer short of the last is a warning, because it may be a subset on purpose."""
    for n, line in lines:
        for m in RANGE.finditer(line):
            family, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
            have = defined.get(family)
            if not have or hi <= lo or len(have) < MIN_FAMILY:
                continue
            top = max(have)
            if hi > top:
                out.append(Finding("error", "range", path, n,
                                   "'%s' runs past the last defined %s, which is %s%d"
                                   % (m.group(0), family, family, top)))
            elif top - NEAR_END <= hi < top and lo == min(have):
                out.append(Finding("warning", "range", path, n,
                                   "'%s' stops short of %s%d; stale if it means the whole family"
                                   % (m.group(0), family, top)))


def heading_numbers(lines):
    numbers = set()
    for _n, line in lines:
        h = HEADING.match(line)
        m = HEADING_NUMBER.match(plain(h.group(2))) if h else None
        if m:
            numbers.add(m.group(1))
    return numbers


def check_section_refs(path, lines, numbers_by_path, charters, out):
    """A 'section N' or 'Part N' must be a heading here, or in the charter when the words just
    before or after it name the charter ("charter section 1.6", "section 1.6 of the charter").
    One named after another document ("Part 2 of `scope-package.en.md`") is not checked. One found
    only in other files given is a warning to name the document; every such file is listed."""
    own = numbers_by_path[path]
    in_charter = set().union(*(numbers_by_path[p] for p in charters)) if charters else set()
    for n, line in lines:
        for m in SECTION_REF.finditer(line):
            ref, before, after = m.group(1), line[max(0, m.start() - 30):m.start()], line[m.end():m.end() + 40]
            clause = CLAUSE_START.split(line[:m.start()])[-1]
            if EXTERNAL_REF.search(before) or EXTERNAL_AFTER.search(after) or EXTERNAL_CLAUSE.search(clause):
                continue
            if CHARTER_REF.search(before) or CHARTER_AFTER.search(after):
                if charters and ref not in in_charter:
                    out.append(Finding("error", "section-ref", path, n,
                                       "refers to the charter's section %s, which is not a heading in %s"
                                       % (ref, ", ".join(charters))))
                continue
            if ref in own:
                continue
            elsewhere = [p for p, numbers in numbers_by_path.items() if p != path and ref in numbers]
            if elsewhere:
                out.append(Finding("warning", "section-ref", path, n,
                                   "section %s is not here but in %s; name the document it means, for example "
                                   "'section %s of the charter' or 'section %s of `scope-package.en.md`'"
                                   % (ref, " and ".join(elsewhere), ref, ref)))
            else:
                out.append(Finding("error", "section-ref", path, n,
                                   "refers to section %s, which is not a heading in any file given" % ref))


def check_citations(path, lines, longest, out):
    """A book page cited without saying which numbering: PDF and printed pages differ by 11.

    A page number no higher than the longest form's page count is read as a page of a form
    ("form 1.1 page 3") and left alone; so is a citation with PDF or printed beside it.
    """
    for n, line in lines:
        for m in PAGE_CITE.finditer(line):
            if int(m.group(1)) <= longest:
                continue
            near = line[max(0, m.start() - 12):m.end() + 25]
            if re.search(r"\b(?:PDF|printed)\b", near, re.I):
                continue
            out.append(Finding("warning", "citation", path, n,
                               "'%s' does not say whether it is a PDF or a printed page; write 'PDF page "
                               "N (printed page N-11)'" % m.group(0)))


def check_stakeholders(files, parties, out):
    """A stakeholder list names every external party the project documents depend on.

    The parties come from the 'External party' table in house-style.md. A party counts as a
    dependency when any line outside the list names it (a risk, a budget line, an assumption),
    and as listed when a first cell of the list names it.
    """
    for path, lines in files:
        for start, header, rows in tables(lines):
            if plain(header[0]).lower() not in STAKEHOLDER_KEYS or len(rows) < 3:
                continue
            listed = " | ".join(plain(r[0]) for _n, r in rows if r)
            inside = {start} | {n for n, _r in rows}
            for party, names, why in parties:
                pattern = re.compile(r"(?<!\w)(?:%s)(?!\w)" % "|".join(re.escape(x) for x in names), re.I)
                if pattern.search(listed):
                    continue
                # The list's own file first, so the evidence quoted does not change when a new
                # file is given before it (check_consistency --report compares the messages).
                ordered = sorted(files, key=lambda f: f[0] != path)
                where = next(((p2, n2, m.group(0)) for p2, lines2 in ordered for n2, l2 in lines2
                              if not (p2 == path and n2 in inside) for m in [pattern.search(l2)] if m), None)
                if where:
                    out.append(Finding("warning", "stakeholder", path, start,
                                       "the stakeholder list has no row for %s, which %s:%d names ('%s')%s"
                                       % (party, where[0], where[1], where[2], "; " + why if why else "")))


def check_form_notes(path, lines, labels, out):
    """Prose between a printed page heading and the end of the form is a note the form does not print.

    Tables, headings, bold labels, check boxes, images and a line that is wholly a
    printed label (an impact area of 3.3, say) are the form's own content. An @@IMAGE line is
    the placeholder a Doc payload (tools/gdoc_schedule_tab.py) uses for the printed picture.
    """
    inside = False
    for n, line in lines:
        text = line.strip()
        if FORM_PAGE.match(line):
            inside = True
        elif re.match(r"^(#{1,3} |---\s*$)", line):
            inside = False
        elif (inside and text and not text.startswith(("|", "#", "![", "<!--", "@@IMAGE"))
              and not re.match(r"\*\*[^*]+\*\*:?", text)
              and not re.match(r"[-*] \[[ xX]\]", text)
              and plain(text).rstrip(":").lower() not in labels):
            out.append(Finding("warning", "form-note", path, n,
                               "text inside the printed form that the form does not print; move it before the form"))


NOTE_WORDS = 150


def check_note_length(path, lines, out):
    """The italic paragraphs above a form carry the citation and what a reader needs (the copy used, differences,
    added rows, empty cells, the PM mark). A long one is a note nobody reads (review-lessons.md, One person,
    one name: a few sentences, not 280 words). A paragraph is the run of consecutive non-blank lines, so a
    note wrapped over many lines counts as one. The limit is the skill's, not the book's."""
    first = next((i for i, (_n, line) in enumerate(lines) if FORM_PAGE.match(line)), None)
    if first is None:
        return
    paragraph = []
    for n, line in lines[:first] + [(0, "")]:
        text = line.strip()
        if text:
            paragraph.append((n, text))
            continue
        if paragraph:
            joined = " ".join(t for _n, t in paragraph)
            if len(joined) > 2 and joined.startswith("*") and not joined.startswith("**") and joined.endswith("*"):
                count = len(joined.split())
                if count > NOTE_WORDS:
                    out.append(Finding("warning", "note-length", path, paragraph[0][0],
                                       "the italic note above the form is %d words; keep it to the citation, the copy "
                                       "used, differences, added rows, empty cells and the PM mark (about %d words at "
                                       "most) and put questions in the reply" % (count, NOTE_WORDS)))
        paragraph = []


DATE_PREPARED = re.compile(r"\bDate prepared\b", re.I)


def check_date_prepared(path, lines, today, out):
    """Date Prepared against today. After today is impossible; before today is a lead to confirm."""
    if today is None:
        return
    for n, line in lines:
        if not DATE_PREPARED.search(line):
            continue
        m = FULL_DATE.search(line[DATE_PREPARED.search(line).end():])
        if not m:
            continue
        day = datetime.date(int(m.group(4)), MONTHS.index(m.group(3)) + 1, int(m.group(2)))
        if day > today:
            out.append(Finding("error", "date-prepared", path, n,
                               "Date Prepared %s is after today (%s)" % (m.group(0), today.isoformat())))
        elif day < today:
            out.append(Finding("warning", "date-prepared", path, n,
                               "Date Prepared %s is %d day(s) before today (%s); confirm the content was last checked "
                               "on that date, or update it" % (m.group(0), (today - day).days, today.isoformat())))


def check_tables(path, lines, out, id_values, audit=False):
    for start, header, rows in tables(lines):
        names = [plain(h) for h in header]
        check_totals(path, names, rows, out)
        check_uniform(path, start, names, rows, out, prose_above(lines, start), audit)
        collect_id_values(path, names, rows, id_values)


def prose_above(lines, start):
    """The text a reader sees before the table at line start: every line that is not a table row
    or a heading, back to the nearest heading of level 1 or 2 (the part the table belongs to)."""
    text = []
    for n, line in reversed(lines):
        if n >= start:
            continue
        h = HEADING.match(line)
        if h and len(h.group(1)) <= 2:
            break
        if not h and not line.lstrip().startswith("|"):
            text.append(line.strip())
    return plain(" ".join(reversed(text)))


def number(cell):
    """(value, unit) of a numeric cell, ignoring bold and highlight; None for text."""
    m = NUMBER.match(plain(cell))
    if not m:
        return None
    return float(m.group(1).replace(",", "")), m.group(2) or ""


def total_column(row):
    """Column of the Total label among the first three text cells, or None for an ordinary row."""
    for col, cell in enumerate(row[:3]):
        if number(cell) is None and TOTAL_LABEL.match(plain(cell)):
            return col
    return None


def check_totals(path, names, rows, out):
    """A Total row must equal the lines above it.

    Subtotals are allowed: a total passes if it equals the rows since the last
    total, the earlier totals plus the rows since, or every non-total row. Only
    columns right of the label are summed; those left of it are row numbers or
    codes. A percentage column may be off by half a point per line, for rounding.
    """
    loose, totals, everything = [], [], []
    for n, row in rows:
        label = total_column(row)
        if label is None:
            loose.append(row)
            everything.append(row)
            continue
        for col in range(label + 1, len(row)):
            got = number(row[col])
            if got is None:
                continue
            candidates = []
            for group in (loose, totals + loose, everything):
                parts = [number(r[col]) for r in group if col < len(r) and plain(r[col])]
                if parts and all(p is not None for p in parts):
                    candidates.append((sum(p[0] for p in parts), len(parts)))
            if candidates and all(abs(c - got[0]) > (0.5 * k if got[1] == "%" else 0.5) for c, k in candidates):
                name = names[col] if col < len(names) and names[col] else "column %d" % (col + 1)
                out.append(Finding("error", "total", path, n,
                                   "%s total is %s but its lines sum to %s"
                                   % (name, fmt(got[0]), fmt(candidates[0][0]))))
        totals.append(row)
        loose = []


def fmt(x):
    return "{:,.0f}".format(x) if x == int(x) else "{:,}".format(x)


def explains(prose, name, value):
    """Whether one sentence of prose names the value together with the column or with a word
    that says it holds throughout ('Every requirement is Must have', 'Status is Open because')."""
    for s in sentences(prose):
        if re.search(r"(?<!\w)%s(?!\w)" % re.escape(value), s, re.I) and (
                (name and re.search(r"(?<!\w)%s(?!\w)" % re.escape(name), s, re.I))
                or re.search(r"\b(?:every|all|each|uniform|throughout)\b", s, re.I)):
            return True
    return False


def check_uniform(path, start, names, rows, out, prose="", audit=False):
    """A text column with one value in every row of a long table carries no information, unless
    the text above the table says why (rendering.md: say it once, above the table). With audit,
    an explained column is still reported: a reason does not make a constant column informative,
    so the reviewer decides whether the form's own rule makes it constant."""
    data = [r for _, r in rows if total_column(r) is None]
    if len(data) < MIN_ROWS_FOR_UNIFORM:
        return
    for col, name in enumerate(names[1:], 1):
        values = {plain(r[col]) for r in data if col < len(r)}
        value = next(iter(values)) if len(values) == 1 else ""
        if not value or number(value) is not None:
            continue
        if explains(prose, name, value):
            if audit:
                out.append(Finding("warning", "uniform-column", path, start,
                                   "column '%s' (column %d) holds '%s' in every one of %d rows; the text above the "
                                   "table gives a reason, but the column still separates nothing; confirm that the "
                                   "form's own rule makes it constant, or grade the values"
                                   % (name, col + 1, value, len(data))))
            continue
        out.append(Finding("warning", "uniform-column", path, start,
                           "column '%s' (column %d) holds '%s' in every one of %d rows; grade the values, or say "
                           "once in the text above the table why every row has it"
                           % (name, col + 1, value, len(data))))


def count_of(token):
    return int(token) if token.isdigit() else NUMBER_WORDS.get(token.lower())


def list_size(lines, at, above=None):
    """(items, description) of the table, list or run of headings that starts at index `at` of lines:
    data rows of a table (total rows left out), the top-level items of a bullet or numbered list, or the
    headings one level below the heading level `above` when the claim sits right under such a heading.
    None when none starts there."""
    n, text = lines[at]
    h = HEADING.match(text)
    if h and above is not None and len(h.group(1)) == above + 1:
        count = 0
        for _n, t in lines[at:]:
            m = HEADING.match(t)
            if m and len(m.group(1)) <= above:
                break
            count += bool(m and len(m.group(1)) == above + 1)
        return count, "the run of headings starting at line %d" % n
    if text.lstrip().startswith("|"):
        block = []
        for _n, t in lines[at:]:
            if not t.lstrip().startswith("|"):
                break
            block.append(t)
        if len(block) >= 3 and re.match(r"^\|?\s*:?-{3,}", block[1].strip()):
            return len([1 for t in block[2:] if total_column(cells(t)) is None]), \
                "the table starting at line %d" % n
        return None
    m = LIST_ITEM.match(text)
    if not m:
        return None
    indent, count = len(m.group(1)), 0
    for _n, t in lines[at:]:
        item = LIST_ITEM.match(t)
        if not t.strip():
            continue
        if item and len(item.group(1)) == indent:
            count += 1
        elif item and len(item.group(1)) > indent or t.startswith(" ") and not item:
            continue
        else:
            break
    return count, "the list starting at line %d" % n


def book_counts():
    """[(table, noun, count, cite)] from references/book-counts.json."""
    try:
        data = json.loads((SKILL_DIR / "references" / "book-counts.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return [(t["table"], t["noun"].lower(), int(t["count"]), t["cite"]) for t in data.get("tables", [])]


def check_counts(path, lines, out):
    """A count in prose ("all fourteen elements of Table 1.1") that disagrees with the table or list
    printed straight after it, or with the rows the book prints in that table (book-counts.json). The
    same count in the same words elsewhere in the file is reported too, since the wrong number is
    usually copied (the charter said fourteen in three places)."""
    claims, wrong, level, current = [], {}, {}, None
    registry = book_counts()
    for k, (n, line) in enumerate(lines):
        h = HEADING.match(line)
        if h:
            current = len(h.group(1))
        level[k] = current
        if line.lstrip().startswith("|") or not line.strip() or h or LIST_ITEM.match(line):
            continue
        for m in COUNT_CLAIM.finditer(plain(line)):
            if re.match(r"\W*(?:above|earlier|before|previous|so far)\b", plain(line)[m.end():], re.I):
                continue
            claims.append((n, count_of(m.group(1)), m.group(2).lower(), k))
        for table, noun, count, cite in registry:
            for m in re.finditer(r"\b(\d{1,3}|%s)\s+(?:[\w'-]+\s+){0,2}?%s\s+of\s+Table\s+%s\b"
                                 % ("|".join(NUMBER_WORDS), noun, re.escape(table)), plain(line), re.I):
                said = count_of(m.group(1))
                if said != count:
                    wrong[(said, noun)] = (n, count, "Table %s as the book prints it (%s)" % (table, cite))
                    claims.append((n, said, noun, k))
    for n, said, noun, k in claims:
        j = k + 1
        while j < len(lines) and not lines[j][1].strip():
            j += 1
        if j >= len(lines) or lines[j][0] - n > 3 or (said, noun) in wrong:
            continue
        got = list_size(lines, j, level[k])
        if got and got[0] != said and said is not None:
            wrong[(said, noun)] = (n, got[0], got[1])
    shown = set()
    for n, said, noun, k in claims:
        hit = wrong.get((said, noun))
        if not hit or (n, said, noun) in shown:
            continue
        shown.add((n, said, noun))
        at, size, where = hit
        if n == at:
            out.append(Finding("warning", "count", path, n, "says %s %s, but %s has %s" % (said, noun, where, size)))
        else:
            out.append(Finding("warning", "count", path, n,
                               "says %s %s, the same count that line %d gets wrong (%s has %s)"
                               % (said, noun, at, where, size)))


def collect_id_values(path, names, rows, id_values):
    """Record, per ID, the text of each identity column.

    A table that repeats its ID header (the Inter-RTM of 2.7, or the two banks of
    2.32 written as one table) holds one register per bank, each keyed on its own
    ID column. Columns are compared by header name only: a label column under a
    different name ("Requirement" against "Technical Requirement") is paraphrased
    by design and is not compared.
    """
    key = plain(names[0]).lower() if names else ""
    if key not in ID_HEADERS:
        return
    banks = [i for i, name in enumerate(names) if plain(name).lower() == key] + [len(names)]
    for lo, hi in zip(banks, banks[1:]):
        columns = {}
        for col in range(lo + 1, hi):
            name = plain(names[col]).lower()
            if name in IDENTITY and name not in columns:
                columns[name] = col
        seen = set()
        for n, row in rows:
            ident = plain(row[lo]) if lo < len(row) else ""
            if not ID.fullmatch(ident) or ident in seen:
                continue
            seen.add(ident)
            for name, col in columns.items():
                if col < len(row) and plain(row[col]):
                    id_values[(ident, name)].append((path, n, plain(row[col])))


def report_id_conflicts(id_values, out):
    for (key, name), seen in sorted(id_values.items()):
        distinct = {v for _, _, v in seen}
        if len(distinct) > 1:
            path, n, _ = seen[0]
            where = "; ".join("%s:%d '%s'" % (p, ln, v[:60]) for p, ln, v in seen[:4])
            if len(seen) > 4:
                where += "; and %d more" % (len(seen) - 4)
            out.append(Finding("warning", "id-conflict", path, n,
                               "%s has different %s text in different tables: %s" % (key, name, where)))


M0_PHRASE = re.compile(r"assigned by the sponsor at M0", re.I)
M0_ROW = re.compile(r"^\|\s*M0\s*\|")
ANY_DATE = re.compile(r"\b(\d{1,2}) (%s)[a-z]* (\d{4})\b" % "|".join(m[:3] for m in MONTHS))
# The family of wordings that tie the project manager's appointment to M0: a verb of appointing, the
# project manager, and either M0 itself or a date on or before M0, or a future "to be assigned".
APPOINT = re.compile(r"\b(?:assign|name|appoint|designat|select|nominat)\w*", re.I)
PM_WORDS = re.compile(r"\bproject manager\b", re.I)
M0_ANCHOR = re.compile(r"\b(?:at|by|before|on or before|until)\s+M0\b|\bto be (?:assigned|named|appointed|designated)\b"
                       r"|\bwill (?:assign|name|appoint|designate)\b", re.I)
BEFORE_DATE = re.compile(r"\b(?:on or before|by|before)\s+(?:%s )?(\d{1,2}) (%s)[a-z]* (\d{4})\b"
                         % (WEEKDAY, "|".join(m[:3] for m in MONTHS)), re.I)


def charter_m0(files):
    """The M0 date from the milestone table of a charter among files, or None."""
    for path, lines in files:
        for _n, line in lines:
            if M0_ROW.match(line.strip()):
                m = ANY_DATE.search(plain(line))
                if m:
                    return datetime.date(int(m.group(3)), [x[:3] for x in MONTHS].index(m.group(2)) + 1,
                                         int(m.group(1)))
    return None


def appointment_before_m0(sentence, m0):
    """True when a sentence ties the project manager's appointment to M0: 'assigned by the sponsor at M0',
    'to be named', or 'names the project manager on or before <a date not after M0>'."""
    if M0_PHRASE.search(sentence):
        return True
    if not (PM_WORDS.search(sentence) and APPOINT.search(sentence)):
        return False
    if M0_ANCHOR.search(sentence):
        return True
    for m in BEFORE_DATE.finditer(sentence):
        month = [x[:3].lower() for x in MONTHS].index(m.group(2)[:3].lower()) + 1
        if datetime.date(int(m.group(3)), month, int(m.group(1))) <= m0:
            return True
    return False


def check_stale_m0(path, lines, m0, out):
    """'name to be assigned by the sponsor at M0' fits a document prepared on or before M0 (review-lessons.md,
    One person, one name). After M0 it reads as stale: the appointment is either recorded or a question. The
    check reads the family of wordings (appointment verb, project manager, M0 or a date on or before it), not
    one phrase."""
    if m0 is None:
        return
    prepared = None
    for _n, line in lines:
        if re.match(r"\*\*Date Prepared:\*\*", line.strip()):
            m = ANY_DATE.search(plain(line))
            if m:
                prepared = datetime.date(int(m.group(3)), [x[:3] for x in MONTHS].index(m.group(2)) + 1,
                                         int(m.group(1)))
            break
    if prepared is None or prepared <= m0:
        return
    for n, line in lines:
        text = plain(line)
        if text.lstrip().startswith("|"):
            text = " ; ".join(cells(text))
        hit = next((x for x in sentences(text) if appointment_before_m0(x, m0)), None)
        if hit:
            out.append(Finding("warning", "stale-m0", path, n,
                               "the appointment of the project manager is tied to M0 or to a date on or before it "
                               "(%r) in a document prepared on %s, after M0 on %s; no project document records the "
                               "appointment, so write that, mark it, and list it as a question to the sponsor"
                               % (hit.strip()[:90], prepared.isoformat(), m0.isoformat())))


def people(files):
    """Sponsor and customer names from the charter's page 1 fields, in a table or as bold lines."""
    found = {}
    for _path, lines in files:
        for _n, line in lines:
            for field in ("Project Sponsor", "Project Customer"):
                m = (re.match(r"^\|\s*\*\*%s:?\*\*:?\s*\|\s*(.+?)\s*\|\s*$" % field, line)
                     or re.match(r"^\*\*%s:?\*\*:?\s*([^*]+?)\s*(?:\*\*|$)" % field, line))
                if m and field not in found:
                    name = plain(m.group(1)).split(",")[0].strip()
                    if name:
                        found[field] = name
    return found.get("Project Sponsor"), found.get("Project Customer")


def sentences(text):
    return re.split(r"(?<!\bDr)(?<!\bMr)(?<!\bMs)(?<!\bMrs)\.\s+|;\s+", text)


def check_roles(path, lines, sponsor, customer, out):
    """Sponsor and customer are separate people and never share a role word.

    A merge is a role word in apposition to the other person's name ("Name, owner
    and Center Director"), a merged phrase such as "Director and sponsor", or a
    table row that gives the sponsor the customer's role. A role word elsewhere in
    the sentence ("the risk owner", "asked the sponsor") is not a merge.
    """
    distinct = sponsor and customer and sponsor != customer
    for n, line in lines:
        pieces = cells(line) if line.lstrip().startswith("|") else [line]
        for piece in pieces:
            for s in sentences(plain(piece)):
                if MERGED_ROLE.search(s):
                    out.append(Finding("error", "role-merge", path, n,
                                       "sponsor and customer roles merged: '%s'" % s.strip()[:90]))
                    continue
                if not distinct:
                    continue
                if re.search(APPOSITION % (re.escape(sponsor), r"owner|Director|Customer"), s, re.I):
                    out.append(Finding("error", "role-merge", path, n,
                                       "the sponsor, %s, is described as owner, Director or Customer" % sponsor))
                if re.search(APPOSITION % (re.escape(customer), r"sponsor"), s, re.I):
                    out.append(Finding("error", "role-merge", path, n,
                                       "the customer, %s, is described as sponsor" % customer))
        if distinct and line.lstrip().startswith("|"):
            row = [plain(c) for c in cells(line)]
            if len(row) >= 2 and sponsor in row[0] and re.match(r"(?:Customer|owner|(?:Center )?Director)\b",
                                                                 row[1], re.I):
                out.append(Finding("error", "role-merge", path, n,
                                   "the sponsor, %s, is listed with the role '%s'" % (sponsor, row[1][:40])))


def is_charter(text):
    return "PROJECT CHARTER" in text or re.search(r"^\s*(?:#+\s*)?project charter\s*$", text, re.I | re.M)


def check_approvals(path, text, lines, out):
    """Form 1.1 prints two signature columns: Project Manager and Sponsor or Originator."""
    if not is_charter(text):
        return
    after = False
    for n, line in lines:
        if re.match(r"^\s*(?:\*\*|#)", line) and re.match(r"^(?:#+\s*)?Approvals\s*:?(?:\s|$)", plain(line)):
            after = True
            continue
        if after and line.lstrip().startswith("|"):
            head = [plain(c) for c in cells(line)]
            roles = [h for h in head if h]
            if roles != ["Project Manager", "Sponsor or Originator"]:
                out.append(Finding("error", "approvals", path, n,
                                   "form 1.1 prints two signature columns, Project Manager and Sponsor or "
                                   "Originator; this block has: %s" % ", ".join(roles)))
            return


def run(texts, sponsor=None, customer=None, terms=None, labels=None, audit=False, today=None):
    """Every check over texts, a {path: markdown} mapping in the order given; returns the findings.

    Sponsor and customer default to the names in the charter fields among texts;
    terms and labels default to the tables in references/.
    """
    files = [(path, list(lines_outside_code(text))) for path, text in texts.items()]
    found_sponsor, found_customer = people(files)
    sponsor, customer = sponsor or found_sponsor, customer or found_customer
    terms = load_terms() if terms is None else terms
    labels = printed_labels() if labels is None else labels
    parties, longest = load_parties(), longest_form()
    defined = definitions(files)
    numbers_by_path = {path: heading_numbers(lines) for path, lines in files}
    charters = [path for path, _ in files if is_charter(texts[path])]

    out, id_values = [], defaultdict(list)
    m0 = charter_m0(files)
    for path, lines in files:
        check_stale_m0(path, lines, m0, out)
        check_markup(path, lines, labels, out)
        check_terms(path, lines, terms, out)
        check_dates(path, lines, out)
        check_ranges(path, lines, defined, out)
        check_section_refs(path, lines, numbers_by_path, charters, out)
        check_citations(path, lines, longest, out)
        check_form_notes(path, lines, labels, out)
        check_note_length(path, lines, out)
        check_date_prepared(path, lines, today, out)
        check_tables(path, lines, out, id_values, audit)
        check_counts(path, lines, out)
        check_roles(path, lines, sponsor, customer, out)
        check_approvals(path, texts[path], lines, out)
    report_id_conflicts(id_values, out)
    check_stakeholders(files, parties, out)
    return out


def contributed(texts, report, sponsor=None, customer=None, audit=False, today=None, with_context=False):
    """Findings that the report paths contribute, and the number of context findings left out.

    A finding is the report paths' when it sits in one of them, or when it is absent
    from a run over the other files alone. With with_context the left-out findings are returned too, as a
    third value.
    """
    everything = run(texts, sponsor, customer, audit=audit, today=today)
    context = {p: t for p, t in texts.items() if p not in report}
    before = set(run(context, sponsor, customer, audit=audit, today=today)) if context else set()
    shown = [f for f in everything if f.path in report or f not in before]
    left = [f for f in everything if f not in shown]
    if with_context:
        return shown, len(left), left
    return shown, len(left)


def heading_at(text, line):
    """The nearest heading at or above a line of text, for the context listing."""
    found = ""
    for n, raw in enumerate(text.splitlines(), 1):
        if n > line:
            break
        m = HEADING.match(raw)
        if m:
            found = m.group(2).strip()
    return found


def grouped(findings, order):
    """One line per (level, check): the count, the files, the first location and message, the next lines."""
    groups = {}
    for f in sorted(findings, key=lambda f: (order.get(f.path, len(order)), f.line, f.check)):
        groups.setdefault((f.level, f.check), []).append(f)
    lines = []
    for (level, check), items in sorted(groups.items(), key=lambda kv: (kv[0][0] != "error", -len(kv[1]), kv[0][1])):
        first = items[0]
        files = sorted({i.path for i in items})
        lines.append("%s [%s] x%d in %s; first %s:%d: %s" % (level.upper(), check, len(items), ", ".join(files),
                                                          first.path, first.line, first.message))
        if len(items) > 1:
            lines.append("    more at: " + ", ".join("%s:%d" % (i.path, i.line) for i in items[1:6])
                         + (" ..." if len(items) > 6 else ""))
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--report", action="append", nargs="?", const="", default=[], metavar="PATH",
                    help="print and count only what PATH contributes; the other paths are context "
                         "(without a value: the first path)")
    ap.add_argument("--sponsor", help="sponsor's name, if the charter is not among the paths")
    ap.add_argument("--customer", help="customer's name, if the charter is not among the paths")
    ap.add_argument("--errors-only", action="store_true")
    ap.add_argument("--group", action="store_true",
                    help="one line per check and level (count, files, first location, the next lines) instead of "
                         "one line per finding")
    ap.add_argument("--show-context", action="store_true",
                    help="with --report, also list the findings left out as already in the context files, with "
                         "the heading each sits under")
    ap.add_argument("--today", metavar="YYYY-MM-DD",
                    help="check each Date Prepared against this day (after it: error; before it: warning)")
    ap.add_argument("--audit", action="store_true",
                    help="also report a uniform column the text above the table explains; use when reviewing "
                         "documents, not when generating a form")
    args = ap.parse_args(argv)

    shorthand = {"charter": "docs/charter-package.en.md", "scope": "docs/scope-package.en.md"}
    repo = SKILL_DIR.parents[2]
    paths = [os.path.normpath(os.path.relpath(repo / shorthand[p]) if p in shorthand and not Path(p).is_file() else p)
             for p in args.paths]
    report = [os.path.normpath(p) for p in args.report if p]
    if "" in args.report:
        if not paths:
            ap.error("--report without a value needs at least one path")
        report.append(paths[0])
    paths = list(dict.fromkeys(report + paths if report else paths))
    if not paths:
        ap.error("give at least one Markdown file")
    texts = {}
    for p in paths:
        if not Path(p).is_file():
            ap.error("no such file: %s" % p)
        texts[p] = Path(p).read_text(encoding="utf-8")

    sponsor, customer = args.sponsor, args.customer
    today = None
    if args.today:
        try:
            today = datetime.date.fromisoformat(args.today)
        except ValueError:
            ap.error("--today %r: write the date as YYYY-MM-DD" % args.today)
    left = []
    if report:
        report = set(report)
        out, hidden, left = contributed(texts, report, sponsor, customer, args.audit, today, with_context=True)
    else:
        out, hidden = run(texts, sponsor, customer, audit=args.audit, today=today), 0

    order = {p: i for i, p in enumerate(paths)}
    shown = [f for f in out if f.level == "error" or not args.errors_only]
    if args.group:
        for line in grouped(shown, order):
            print(line)
    else:
        for f in sorted(shown, key=lambda f: (order.get(f.path, len(order)), f.line, f.check)):
            print(f)
    if args.show_context and left:
        print("Findings already in the context files (not part of the report):")
        for f in sorted(left, key=lambda f: (order.get(f.path, len(order)), f.line, f.check)):
            print("  CONTEXT %s  (under: %s)" % (f, heading_at(texts[f.path], f.line) or "no heading"))
    errors = sum(f.level == "error" for f in out)
    summary = "%d error(s), %d warning(s) in %d file(s)" % (errors, len(out) - errors, len(paths))
    if report:
        summary += "; reporting on %s, %d finding(s) already in the context files not shown" % (
            ", ".join(p for p in paths if p in report), hidden)
    print(summary)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
