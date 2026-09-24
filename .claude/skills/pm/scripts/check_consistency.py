"""Consistency checks a reviewer would otherwise make by hand.

Each check here comes from a finding in review/2026-09-16-doc-review.md or
review/2026-09-24-doc-audit.md; references/review-lessons.md explains why each
one matters. The checks read Markdown only and never edit it.

Usage:
    python3 check_consistency.py docs/charter-package.en.md docs/scope-package.en.md

Pass every document of a deliverable together: ID families defined in one file
(risks in the charter) are referenced from another (the RTM), and a range is only
stale relative to the definitions pooled across all files given.

Exit code 1 when any error is found, 0 when only warnings or nothing.
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December")
SHORT_MONTHS = ("Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Sept", "Oct", "Nov", "Dec")
WEEKDAY = r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)"

FULL_DATE = re.compile(r"\b(%s )?(\d{1,2}) (%s) (\d{4})\b" % (WEEKDAY, "|".join(MONTHS)))
SHORT_DATE = re.compile(r"\b(?:%s )?\d{1,2} (%s) \d{4}\b" % (WEEKDAY, "|".join(SHORT_MONTHS)))

# ID families: a letter prefix and a number, as in F01, D4, R12, M0, A03, BR05, NFR02.
ID = re.compile(r"\b([A-Z]{1,3})(\d{1,3})\b")
RANGE = re.compile(r"\b([A-Z]{1,3})(\d{1,3})(?: to |-|\u2013)\1?(\d{1,3})\b")
SECTION_REF = re.compile(r"\bsections? (\d+(?:\.\d+)*[A-Z]?)\b")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
HEADING_NUMBER = re.compile(r"^(?:Part\s+)?(\d+(?:\.\d+)*[A-Z]?)[.:]?(?:\s|$)")
HTML_TAG = re.compile(r"</?([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>")
EM_DASH = "\u2014"
EMOJI = re.compile("[\\U0001F300-\\U0001FAFF\\u2600-\\u27BF]")
NUMBER = re.compile(r"^\**\s*(-?[\d,]+(?:\.\d+)?)\s*(%?)\s*\**$")
MERGED_ROLE = re.compile(
    r"Director,?\s+(?:and\s+)?sponsor|sponsor,?\s+(?:and\s+)?(?:owner|(?:Center\s+)?Director)"
    r"|sponsor of the (?:learning )?center", re.I)


class Finding:
    def __init__(self, level, check, path, line, message):
        self.level, self.check, self.path, self.line, self.message = level, check, path, line, message

    def __str__(self):
        return "%s %s:%d [%s] %s" % (self.level.upper(), self.path, self.line, self.check, self.message)


def lines_outside_code(text):
    """Yield (line_number, line) for lines that are not inside a fenced code block."""
    fenced = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            yield n, re.sub(r"`[^`]*`", lambda m: m.group(0).replace("<", "(").replace(">", ")"), line)


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


def check_markup(path, lines, out):
    for n, line in lines:
        for m in HTML_TAG.finditer(line):
            if m.group(1).lower() != "mark":
                out.append(Finding("error", "html", path, n,
                                   "<%s> will reach the Google Doc as literal text; only <mark> is converted"
                                   % m.group(1)))
        if EM_DASH in line:
            out.append(Finding("error", "em-dash", path, n, "em dash; use a comma, semicolon or full stop"))
        if EMOJI.search(line):
            out.append(Finding("error", "emoji", path, n, "emoji in a project document"))
        first_cell = cells(line)[0] if line.lstrip().startswith("|") else ""
        if (re.search(r"\*\*\s*<mark>[^<]*</mark>\s*:?\s*\*\*", line)
                or re.match(r"^\s*<mark>\s*\*\*[^*]+\*\*\s*</mark>", line)
                or re.fullmatch(r"<mark>\s*\*\*[^*]+\*\*\s*</mark>", first_cell)):
            out.append(Finding("error", "mark-on-label", path, n,
                               "a bold label is highlighted; highlight marks uncertain content, never a label"))
        h = HEADING.match(line)
        if h and "<mark>" in h.group(2):
            out.append(Finding("error", "mark-on-label", path, n, "a heading is highlighted"))


def check_dates(path, lines, out):
    styles = defaultdict(list)
    for n, line in lines:
        for m in FULL_DATE.finditer(line):
            if m.group(2).startswith("0"):
                out.append(Finding("error", "date", path, n,
                                   "leading zero in '%s'; write the day without it" % m.group(0)))
            styles["weekday" if m.group(1) else "plain"].append(n)
        for m in SHORT_DATE.finditer(line):
            out.append(Finding("error", "date", path, n,
                               "abbreviated month in '%s'; write the month in full" % m.group(0)))
            styles["abbreviated"].append(n)
    if len(styles) > 1:
        summary = ", ".join("%s %d (first line %d)" % (k, len(v), v[0]) for k, v in sorted(styles.items()))
        out.append(Finding("warning", "date-style", path, min(v[0] for v in styles.values()),
                           "more than one date style in this file: %s" % summary))


def definitions(files):
    """Highest number defined per ID family, with the zero-padding width it uses.

    An ID counts as defined where it opens a table row or a list item, which is how
    every register in this repo introduces its entries.
    """
    defined = defaultdict(set)
    for path, lines in files:
        for _n, line in lines:
            first = None
            if line.lstrip().startswith("|"):
                row = cells(line)
                first = plain(row[0]) if row else None
                if not first and len(row) > 1:
                    first = plain(row[1])
            else:
                m = re.match(r"^\s*(?:[-*]|\d+\.)\s+\**([A-Z]{1,3}\d{1,3})\b", line)
                first = m.group(1) if m else None
            if first:
                m = re.match(r"^([A-Z]{1,3})(\d{1,3})\b", first)
                if m:
                    defined[m.group(1)].add(int(m.group(2)))
    return defined


def check_ranges(path, lines, defined, out):
    for n, line in lines:
        for m in RANGE.finditer(line):
            family, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
            have = defined.get(family)
            if not have or hi <= lo or len(have) < 3:
                continue
            top = max(have)
            if hi > top:
                out.append(Finding("error", "range", path, n,
                                   "'%s' runs past the last defined %s, which is %s%d"
                                   % (m.group(0), family, family, top)))
            elif top - 2 <= hi < top and lo == min(have):
                out.append(Finding("warning", "range", path, n,
                                   "'%s' stops short of %s%d; stale if it means the whole family"
                                   % (m.group(0), family, top)))


def check_section_refs(path, lines, out):
    numbers = set()
    for _n, line in lines:
        h = HEADING.match(line)
        if h:
            m = HEADING_NUMBER.match(plain(h.group(2)))
            if m:
                numbers.add(m.group(1).rstrip("."))
    for n, line in lines:
        for m in SECTION_REF.finditer(line):
            ref = m.group(1)
            before = line[max(0, m.start() - 25):m.start()]
            if re.search(r"PMBOK|Guide", before) or re.search(r"\.md\b|\bcharter\b|\bthe book\b", line, re.I):
                continue
            if ref not in numbers:
                out.append(Finding("error", "section-ref", path, n,
                                   "refers to section %s, which is not a heading in this document" % ref))


def check_tables(path, lines, out, id_values):
    for start, header, rows in tables(lines):
        names = [plain(h) for h in header]
        check_totals(path, names, rows, out)
        check_uniform(path, start, names, rows, out)
        collect_id_values(path, names, rows, id_values)


def number(cell):
    m = NUMBER.match(plain(cell) if "<mark>" in cell else cell)
    if not m:
        return None
    return float(m.group(1).replace(",", "")), m.group(2)


def check_totals(path, names, rows, out):
    """A Total row must equal the lines above it.

    Subtotals are allowed: a total passes if it equals the rows since the last
    total, the earlier totals plus the rows since, or every non-total row.
    """
    loose, totals, everything = [], [], []
    for n, row in rows:
        label = " ".join(plain(c) for c in row[:2]).lower()
        if not re.search(r"\btotal\b", label):
            loose.append(row)
            everything.append(row)
            continue
        for col in range(len(row)):
            got = number(row[col])
            if got is None:
                continue
            candidates = []
            for group in (loose, totals + loose, everything):
                parts = [number(r[col]) for r in group if col < len(r) and plain(r[col])]
                if parts and all(p is not None for p in parts):
                    candidates.append(sum(p[0] for p in parts))
            if candidates and all(abs(c - got[0]) > 0.5 for c in candidates):
                name = names[col] if col < len(names) and names[col] else "column %d" % (col + 1)
                out.append(Finding("error", "total", path, n,
                                   "%s total is %s but its lines sum to %s"
                                   % (name, fmt(got[0]), fmt(candidates[0]))))
        totals.append(row)
        loose = []


def fmt(x):
    return "{:,.0f}".format(x) if x == int(x) else "{:,}".format(x)


def check_uniform(path, start, names, rows, out):
    data = [r for _, r in rows if not re.search(r"\btotal\b", " ".join(plain(c) for c in r[:2]).lower())]
    if len(data) < 8:
        return
    for col, name in enumerate(names[1:], 1):
        values = {plain(r[col]) for r in data if col < len(r)}
        if len(values) == 1 and next(iter(values)) and number(next(iter(values))) is None:
            out.append(Finding("warning", "uniform-column", path, start,
                               "every one of %d rows has %s '%s'; the column carries no information "
                               "unless the text above the table says why" % (len(data), name, values.pop())))


def collect_id_values(path, names, rows, id_values):
    if not names or plain(names[0]).lower() not in ("id", "#", "code", "risk id", "req id"):
        return
    columns = {}
    for col, name in enumerate(names[1:], 1):
        if name and name.lower() not in columns and name.lower() != plain(names[0]).lower():
            columns[name.lower()] = col
    seen = set()
    for n, row in rows:
        key = plain(row[0]) if row else ""
        if not ID.fullmatch(key) or key in seen:
            continue
        seen.add(key)
        for name, col in columns.items():
            if col < len(row) and plain(row[col]):
                id_values[(key, name)].append((path, n, plain(row[col])))


def report_id_conflicts(id_values, out):
    for (key, name), seen in sorted(id_values.items()):
        distinct = {v for _, _, v in seen}
        if len(distinct) > 1:
            path, n, _ = seen[0]
            where = "; ".join("%s:%d '%s'" % (p, ln, v[:60]) for p, ln, v in seen[:3])
            out.append(Finding("warning", "id-conflict", path, n,
                               "%s has different %s text in different tables: %s" % (key, name, where)))


def people(files):
    """Sponsor and customer names from the charter's page 1 fields, if present."""
    found = {}
    for _path, lines in files:
        for _n, line in lines:
            for field in ("Project Sponsor", "Project Customer"):
                m = re.match(r"^\|\s*\*\*%s\*\*\s*\|\s*(.+?)\s*\|\s*$" % field, line)
                if m and field not in found:
                    name = plain(m.group(1)).split(",")[0].strip()
                    if name:
                        found[field] = name
    return found.get("Project Sponsor"), found.get("Project Customer")


def sentences(text):
    return re.split(r"(?<!\bDr)(?<!\bMr)(?<!\bMs)(?<!\bMrs)\.\s+|;\s+", text)


def check_roles(path, lines, sponsor, customer, out):
    for n, line in lines:
        pieces = cells(line) if line.lstrip().startswith("|") else [line]
        for piece in pieces:
            for s in sentences(plain(piece)):
                if MERGED_ROLE.search(s):
                    out.append(Finding("error", "role-merge", path, n,
                                       "sponsor and customer roles merged: '%s'" % s.strip()[:90]))
                    continue
                if sponsor and customer and sponsor != customer:
                    if sponsor in s and customer not in s and re.search(r"\b(owner|Director|Customer)\b", s):
                        out.append(Finding("error", "role-merge", path, n,
                                           "the sponsor, %s, is described as owner, Director or Customer" % sponsor))
                    if customer in s and sponsor not in s and re.search(r"\bsponsor\b", s, re.I):
                        out.append(Finding("error", "role-merge", path, n,
                                           "the customer, %s, is described as sponsor" % customer))
        if sponsor and customer and line.lstrip().startswith("|"):
            row = [plain(c) for c in cells(line)]
            if len(row) >= 2 and sponsor in row[0] and re.search(r"^Customer\b", row[1]):
                out.append(Finding("error", "role-merge", path, n,
                                   "the sponsor, %s, is listed with the Customer role" % sponsor))


def check_approvals(path, text, lines, out):
    if "PROJECT CHARTER" not in text:
        return
    after = False
    for n, line in lines:
        if re.match(r"^\s*(\*\*Approvals\*\*|#+\s*Approvals)\s*:?\s*$", line):
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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--sponsor", help="sponsor's name, if the charter is not among the paths")
    ap.add_argument("--customer", help="customer's name, if the charter is not among the paths")
    ap.add_argument("--errors-only", action="store_true")
    args = ap.parse_args(argv)

    files, texts = [], {}
    for p in args.paths:
        text = p.read_text(encoding="utf-8")
        texts[str(p)] = text
        files.append((str(p), list(lines_outside_code(text))))

    sponsor, customer = people(files)
    sponsor, customer = args.sponsor or sponsor, args.customer or customer
    defined = definitions(files)

    out, id_values = [], defaultdict(list)
    for path, lines in files:
        check_markup(path, lines, out)
        check_dates(path, lines, out)
        check_ranges(path, lines, defined, out)
        check_section_refs(path, lines, out)
        check_tables(path, lines, out, id_values)
        check_roles(path, lines, sponsor, customer, out)
        check_approvals(path, texts[path], lines, out)
    report_id_conflicts(id_values, out)

    shown = [f for f in out if f.level == "error" or not args.errors_only]
    for f in sorted(shown, key=lambda f: (f.path, f.line, f.check)):
        print(f)
    errors = sum(f.level == "error" for f in out)
    warnings = len(out) - errors
    print("%d error(s), %d warning(s) in %d file(s)" % (errors, warnings, len(files)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
