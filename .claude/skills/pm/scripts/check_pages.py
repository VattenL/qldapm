"""Page citations in a reply or a note: every page number needs its partner.

A book page is cited as the printed number and the PDF number together, for
example "PMBOK 6 section 6.5.2.6, printed page 215 (PDF page 254)". A bare
"p443" or "PDF 181" is ambiguous because the two numberings differ by 11 pages
in the Book of Forms, 39 in PMBOK 6 and 810 in the Agile Practice Guide.

    check_pages.py reply.md
    check_pages.py - < reply.md

page (error): a page number with no number of the other kind within 45
    characters, in the same sentence.
pair (warning): a printed and a PDF number side by side whose difference is
    not 11, 39 or 810, so one of them may be mistyped.
cite (warning): a book reference by section ("PMBOK 6 section 6.5.2.6", "PM
    6.5.2.6", "APG 5.2.1", "BoF 3.3", "Book of Forms form 2.32") in a sentence
    or table row that carries no page at all, or that sends the reader to a
    note instead of giving the pages.
negative (warning): "the book prints no X" with no page. Write "not stated in
    the book" and name the section searched with its two page numbers.

Vietnamese replies use "trang in 215 (trang PDF 254)"; "trang" alone is a
printed page. Not read as citations: text inside double quotation marks, a line
that starts with "> " or "quote:", and "page 3 of 4" or "page 1 of the Doc"
(a position in a document). Section numbers such as 6.5.2.6 and a bare form
number are not page numbers. "PM" is read as PMBOK only with a section of two or more dots (PM 6.5.2.6) or a
page cue after it (PM 6.5 p215); a resource code with hours (PM 99.8 hours) is not a reference. Exit code 1 when an error is found, 0 otherwise, 2
for a usage error.
"""

import argparse
import re
import sys
from collections import namedtuple

OFFSETS = (11, 39, 810)
REF = re.compile(
    r"(?P<kind>trang\s+PDF\s+|trang\s+in\s+|PDF\s+pages?\s+|PDF\s+|printed\s+pages?\s+|printed\s+|"
    r"\btrang\s+|\bpages?\s+|\bpp?\.?\s*)(?P<first>\d{1,4})(?!\.\d)"
    r"(?:\s+(?:to|and|den|va)\s+(?P<last>\d{1,4})(?!\.\d))?", re.I)
QUOTED = re.compile(r'"[^"\n]*"|\u201c[^\u201d\n]*\u201d')
POSITION = re.compile(r"(?:(?:printed|PDF)\s+)?\bpages?\s+\d{1,4}\s+of\s+(?:\d+\b|the\s+(?:Google\s+)?"
                      r"(?:Doc|form|document|tab|file|package|report))", re.I)
SECTION_REF = re.compile(
    r"\bPMBOK\s*6?\s+(?:section\s+|muc\s+)?\d+\.\d|\bPM\s+\d{1,2}(?:\.\d+){2,}|\bPM\s+\d{1,2}\.\d+\s*(?:p\d|printed|PDF)|\bPMBOK\s+6\s+(?:section\s+)?\d"
    r"|\bAPG\s+X?\d|\bBoF\s+\d|Agile Practice Guide\s+(?:section\s+)?\d|Book of Forms\s+(?:form\s+)?\d\.\d", re.I)
DEFERRAL = re.compile(r"\b(?:see|read|in|per|from)\s+(?:the\s+)?(?:note\s+)?`?(?:references/)?"
                      r"(?:pmbok-\w+|decisions|forms-index|book-structure)(?:\.md)?`?"
                      r"|before quoting it|read the (?:file|note) (?:first|before)", re.I)
NEGATIVE = re.compile(r"\b(?:the\s+)?(?:book|books|PMBOK|Guide)\s+(?:prints|gives|states|names|defines)\s+no\b", re.I)
SENTENCE = re.compile(r"(?<=[.;:!?])\s+(?=[A-Z(])|\n\n")
Finding = namedtuple("Finding", "level line message")


def kind_of(text):
    return "pdf" if "pdf" in text.lower() else "printed"


def references(sentence):
    found = []
    for m in REF.finditer(sentence):
        text = m.group("kind")
        # "p" glued to a section number or an ID (p53 inside a word) is not a page
        if m.start() > 0 and (sentence[m.start() - 1].isalnum() or sentence[m.start() - 1] == "."):
            continue
        kind = kind_of(text)
        number = int(m.group("first"))
        # "page 3 of a form" is a form page, not a book page: it needs no partner, but may be one
        weak = kind == "printed" and not text.lower().startswith(("printed", "trang in")) and number < 12
        found.append((m.start(), m.end(), kind, number, weak))
    return found


NEW_UNIT = re.compile(r"^\s*(?:\||#|>|quote:|[-*] |\d+\. )", re.I)


def units(text):
    """(first line number, text) of each paragraph, list item or table row: wrapped lines are joined, so a
    page pair that a line break splits is still one pair."""
    out, current, start = [], [], 0
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            if current:
                out.append((start, " ".join(current)))
            current = []
            continue
        if current and NEW_UNIT.match(line):
            out.append((start, " ".join(current)))
            current = []
        if not current:
            start = n
        current.append(line.strip())
    if current:
        out.append((start, " ".join(current)))
    return out


def cite_findings(n, sentence, refs):
    """Warnings for a book reference by section, or a negative claim, in a sentence with no page at all."""
    if refs:
        return []
    if NEGATIVE.search(sentence):
        return [Finding("warning", n, "negative claim about the book with no page: write 'not stated in the book' "
                        "and name the section searched with its printed and PDF pages")]
    if SECTION_REF.search(sentence):
        why = "sends the reader to a note" if DEFERRAL.search(sentence) else "gives a section but no page"
        return [Finding("warning", n, "book reference %s: add 'printed page N (PDF page M)' in the same sentence "
                        "or table row" % why)]
    return []


def check(text):
    out = []
    for n, line in units(text):
        if re.match(r"\s*(?:>|quote:)", line, re.I):
            continue
        line = POSITION.sub(" ", QUOTED.sub(" ", line))
        # a table row is one unit: the page may sit in another cell of the row
        for sentence in ([line] if line.lstrip().startswith("|") else SENTENCE.split(line)):
            refs = references(sentence)
            out.extend(cite_findings(n, sentence, refs))
            for start, end, kind, number, weak in refs:
                if weak:
                    continue
                partner = [r for r in refs if r[2] != kind and (abs(r[0] - end) <= 45 or abs(start - r[1]) <= 45)]
                if not partner:
                    other = "printed" if kind == "pdf" else "PDF"
                    out.append(Finding("error", n, "%s page %d has no %s number beside it; write both, for example "
                                       "'printed page 215 (PDF page 254)'" % (kind.upper() if kind == "pdf" else kind,
                                                                              number, other)))
                    continue
                if kind != "printed":
                    continue
                if not any(p[3] - number in OFFSETS for p in partner):
                    near = min(partner, key=lambda r: min(abs(r[0] - end), abs(start - r[1])))
                    out.append(Finding("warning", n, "printed page %d beside PDF page %d: the difference %d is not "
                                       "11, 39 or 810" % (number, near[3], near[3] - number)))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="the reply or note as a file, or - for standard input")
    args = ap.parse_args(argv)
    try:
        text = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
    except OSError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    found = check(text)
    for f in found:
        print("%s %s:%d %s" % (f.level.upper(), args.path, f.line, f.message))
    errors = sum(f.level == "error" for f in found)
    print("%d error(s), %d warning(s)" % (errors, len(found) - errors))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
