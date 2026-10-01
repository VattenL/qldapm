"""Consistency checks a reviewer would otherwise make by hand.

Each check here comes from a finding in review/2026-09-16-doc-review.md or
review/2026-09-24-doc-audit.md; references/review-lessons.md explains why each
one matters. The checks read Markdown only and never edit it.

Usage:
    python3 check_consistency.py docs/charter-package.en.md docs/scope-package.en.md
    python3 check_consistency.py docs/forms/<file>.md docs/charter-package.en.md \\
        docs/scope-package.en.md --report docs/forms/<file>.md

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

Exit code 1 when any shown error is found, 0 when only warnings or nothing,
2 for a usage error such as a missing file.
"""

import argparse
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
            "business requirement", "technical requirement"}
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


def check_markup(path, lines, labels, out):
    for n, line in lines:
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
            if EXTERNAL_REF.search(before) or EXTERNAL_AFTER.search(after):
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
                                   "section %s is not here but in %s; name the document it means"
                                   % (ref, " and ".join(elsewhere))))
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


def check_tables(path, lines, out, id_values):
    for start, header, rows in tables(lines):
        names = [plain(h) for h in header]
        check_totals(path, names, rows, out)
        check_uniform(path, start, names, rows, out, prose_above(lines, start))
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


def check_uniform(path, start, names, rows, out, prose=""):
    """A text column with one value in every row of a long table carries no information, unless
    the text above the table says why (rendering.md: say it once, above the table)."""
    data = [r for _, r in rows if total_column(r) is None]
    if len(data) < MIN_ROWS_FOR_UNIFORM:
        return
    for col, name in enumerate(names[1:], 1):
        values = {plain(r[col]) for r in data if col < len(r)}
        value = next(iter(values)) if len(values) == 1 else ""
        if not value or number(value) is not None or explains(prose, name, value):
            continue
        out.append(Finding("warning", "uniform-column", path, start,
                           "every one of %d rows has %s (column %d) '%s'; grade the values, or say "
                           "once in the text above the table why every row has it"
                           % (len(data), name, col + 1, value)))


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


def run(texts, sponsor=None, customer=None, terms=None, labels=None):
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
    for path, lines in files:
        check_markup(path, lines, labels, out)
        check_terms(path, lines, terms, out)
        check_dates(path, lines, out)
        check_ranges(path, lines, defined, out)
        check_section_refs(path, lines, numbers_by_path, charters, out)
        check_citations(path, lines, longest, out)
        check_form_notes(path, lines, labels, out)
        check_tables(path, lines, out, id_values)
        check_roles(path, lines, sponsor, customer, out)
        check_approvals(path, texts[path], lines, out)
    report_id_conflicts(id_values, out)
    check_stakeholders(files, parties, out)
    return out


def contributed(texts, report, sponsor=None, customer=None):
    """Findings that the report paths contribute, and the number of context findings left out.

    A finding is the report paths' when it sits in one of them, or when it is absent
    from a run over the other files alone.
    """
    everything = run(texts, sponsor, customer)
    context = {p: t for p, t in texts.items() if p not in report}
    before = set(run(context, sponsor, customer)) if context else set()
    shown = [f for f in everything if f.path in report or f not in before]
    return shown, len(everything) - len(shown)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--report", action="append", nargs="?", const="", default=[], metavar="PATH",
                    help="print and count only what PATH contributes; the other paths are context "
                         "(without a value: the first path)")
    ap.add_argument("--sponsor", help="sponsor's name, if the charter is not among the paths")
    ap.add_argument("--customer", help="customer's name, if the charter is not among the paths")
    ap.add_argument("--errors-only", action="store_true")
    args = ap.parse_args(argv)

    paths = [os.path.normpath(p) for p in args.paths]
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
    if report:
        report = set(report)
        out, hidden = contributed(texts, report, sponsor, customer)
    else:
        out, hidden = run(texts, sponsor, customer), 0

    order = {p: i for i, p in enumerate(paths)}
    shown = [f for f in out if f.level == "error" or not args.errors_only]
    for f in sorted(shown, key=lambda f: (order.get(f.path, len(order)), f.line, f.check)):
        print(f)
    errors = sum(f.level == "error" for f in out)
    summary = "%d error(s), %d warning(s) in %d file(s)" % (errors, len(out) - errors, len(paths))
    if report:
        summary += "; reporting on %s, %d finding(s) already in the context files not shown" % (
            ", ".join(p for p in paths if p in report), hidden)
    print(summary)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
