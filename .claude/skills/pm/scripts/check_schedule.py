"""Schedule checks an auditor otherwise makes by hand, over a form 2.18 Project Schedule.

The audit of the generated 2.18 (iteration 2 of the skill's evaluation) found
most of its errors by reading: a review, sign-off or acceptance that finishes
before the work it checks, work booked into a break the charter rules out, and
levelled hours per person that no longer match the hours the cost estimate
prices. These three checks find the same things mechanically. The schedule is
read from its Gantt table (columns WBS, Task Name, Start, Finish) and, for the
hours, from a table headed Resource with a hours column.

    check_schedule.py docs/forms/2-18-project-schedule.en.md \\
        --charter docs/charter-package.en.md --scope docs/scope-package.en.md

sequence (warning): an activity whose name says it checks something (review,
    approval, acceptance, sign-off, walkthrough, verification) finishes before
    an activity that comes before it in the same work package or control
    account and is not itself a check; a closeout activity finishes before any
    other activity of its phase. Code order stands for "produces the input",
    so read both rows before reporting: a finding is a lead.
break (warning): rows dated inside a break. Breaks come from --break, and from
    the charter: a sentence naming a holiday, break, freeze or New Year that
    says it begins (and, if stated, ends) on a date. Where the charter gives
    only the first day, every row on or after it is reported, since nothing
    says when the break ends.
hours (error): booked hours per person in the schedule differ from the scope
    package's 'Labor hours by resource' line, so the schedule and the cost
    baseline describe different assignments.

Exit code 1 when an error is found, 0 otherwise, 2 for a usage error.
"""

import argparse
import datetime
import re
import sys
from collections import namedtuple
from pathlib import Path

MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December")
DATE = re.compile(r"\b(\d{1,2}) (%s) (\d{4})\b" % "|".join(MONTHS))
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ACTIVITY = re.compile(r"^(\d+(?:\.\d+)+)-A(\d+)$")
CHECK_WORDS = re.compile(r"\b(?:review|approv\w*|accept\w*|sign(?:ed)?[- ]off|walkthrough|verif\w*)\b", re.I)
CLOSE_WORDS = re.compile(r"\b(?:closeout|close-out|lessons learned|final acceptance)\b", re.I)
BREAK_WORDS = re.compile(r"\b(?:holiday|break|freeze|closure|New Year|Tết)\b", re.I)
BEGINS = re.compile(r"\b(?:begins|starts|runs from|from)\s+(?:on\s+)?(\d{1,2} (?:%s) \d{4})" % "|".join(MONTHS))
ENDS = re.compile(r"\b(?:ends|until|to|through)\s+(?:on\s+)?(\d{1,2} (?:%s) \d{4})" % "|".join(MONTHS))
LABOR_LINE = re.compile(r"Labor hours by resource:\s*([^.]+(?:\.\d[^.]*)*)")
PAIR = re.compile(r"\b([A-Z][A-Z0-9]*)\s+([\d,]+(?:\.\d+)?)\b")

Finding = namedtuple("Finding", "level check path line message")
Row = namedtuple("Row", "line code activity name start finish")


def fmt_finding(f):
    return "%s %s:%d [%s] %s" % (f.level.upper(), f.path, f.line, f.check, f.message)


def plain(text):
    return re.sub(r"</?mark>|\*\*|\*", "", text).strip()


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_date(text):
    text = plain(text)
    if ISO.match(text):
        return datetime.date.fromisoformat(text)
    m = DATE.search(text)
    if not m:
        return None
    return datetime.date(int(m.group(3)), MONTHS.index(m.group(2)) + 1, int(m.group(1)))


def fmt(day):
    return "%s %d %s %d" % (day.strftime("%a"), day.day, MONTHS[day.month - 1], day.year)


def tables(text):
    """(header, [(line, cells)]) for each pipe table."""
    block = []
    for n, line in list(enumerate(text.splitlines(), 1)) + [(0, "")]:
        if line.lstrip().startswith("|"):
            block.append((n, line))
            continue
        if len(block) >= 2 and re.match(r"^\|?\s*:?-{3,}", block[1][1].strip()):
            yield [plain(c) for c in cells(block[0][1])], [(n2, cells(l2)) for n2, l2 in block[2:]]
        block = []


def schedule_rows(text):
    """Dated rows of every table headed with Task Name, Start and Finish."""
    rows = []
    for header, body in tables(text):
        names = [h.lower() for h in header]
        if not {"task name", "start", "finish"} <= set(names):
            continue
        code_col = names.index("wbs") if "wbs" in names else None
        for n, row in body:
            get = lambda name: row[names.index(name)] if names.index(name) < len(row) else ""
            start, finish = parse_date(get("start")), parse_date(get("finish"))
            if not start or not finish:
                continue
            code = plain(row[code_col]) if code_col is not None and code_col < len(row) else ""
            rows.append(Row(n, code, bool(ACTIVITY.match(code)), plain(get("task name")), start, finish))
    return rows


def check_sequence(path, rows, out):
    acts = [r for r in rows if r.activity]
    for r in acts:
        closing = CLOSE_WORDS.search(r.name)
        if not closing and not CHECK_WORDS.search(r.name):
            continue
        pkg, num = ACTIVITY.match(r.code).groups()
        parts = pkg.split(".")
        inputs = []
        for x in acts:
            if x is r or CHECK_WORDS.search(x.name) or CLOSE_WORDS.search(x.name):
                continue
            xpkg, xnum = ACTIVITY.match(x.code).groups()
            xparts = xpkg.split(".")
            if closing:
                related = xparts[:2] == parts[:2] and xpkg != pkg
            else:
                related = ((xpkg == pkg and int(xnum) < int(num))
                           or (xparts[:3] == parts[:3] and len(xparts) == len(parts)
                               and [int(p) for p in xparts] < [int(p) for p in parts]))
            if related and x.finish > r.finish:
                inputs.append(x)
        if inputs:
            last = max(inputs, key=lambda x: x.finish)
            scope = "phase" if closing else ("work package" if last.code.split("-")[0] == pkg
                                             else "control account")
            out.append(Finding("warning", "sequence", path, r.line,
                               "%s '%s' finishes %s, before %s '%s' (line %d) of the same %s finishes %s; "
                               "if that is its input, the check comes before the thing it checks"
                               % (r.code, r.name, fmt(r.finish), last.code, last.name, last.line, scope,
                                  fmt(last.finish))))


def charter_breaks(charter_path):
    """(start, end or None, line, sentence) for each break the charter dates."""
    found = []
    text = Path(charter_path).read_text(encoding="utf-8")
    for n, line in enumerate(text.splitlines(), 1):
        pieces = cells(line) if line.lstrip().startswith("|") else [line]
        for sentence in (x for piece in pieces for x in re.split(r"(?<=[.;])\s+", plain(piece))):
            if not BREAK_WORDS.search(sentence):
                continue
            b = BEGINS.search(sentence)
            if b:
                e = ENDS.search(sentence, b.end())
                found.append((parse_date(b.group(1)), parse_date(e.group(1)) if e else None, n,
                              sentence.strip()))
    return found


def check_breaks(path, rows, breaks, out):
    for start, end, where, sentence in breaks:
        hit = [r for r in rows if r.finish >= start and (end is None or r.start <= end)]
        if not hit:
            continue
        milestones = [r for r in hit if not r.code and re.match(r"M\d+\b", r.name)]
        acts = [r for r in hit if r.activity]
        window = "from %s to %s" % (fmt(start), fmt(end)) if end else \
            "on or after %s, when the break begins; no end date is given, so any of them may fall inside it" % fmt(start)
        # Milestones first, then the activities that start in the window, earliest first; one that
        # merely runs across it (level of effort) is counted but not quoted.
        inside = sorted((r for r in acts if r.start >= start), key=lambda r: (r.start, r.line))
        sample = ", ".join("%s (line %d, %s)" % (r.code or r.name.split()[0], r.line, fmt(r.start)) for r in
                           (milestones + inside)[:8])
        source = "charter line %d: '%s'" % (where, sentence[:90]) if where else "--break"
        out.append(Finding("warning", "break", path, hit[0].line,
                           "%d activities and %d milestones are dated %s (%s): %s"
                           % (len(acts), len(milestones), window, source, sample)))


def booked_hours(text):
    """{person: (hours, line)} from a table headed Resource with a booked hours column."""
    for header, body in tables(text):
        names = [h.lower() for h in header]
        if not names or names[0] != "resource":
            continue
        col = next((i for i, h in enumerate(names) if "hours" in h and "peak" not in h), None)
        if col is None:
            continue
        out = {}
        for n, row in body:
            try:
                out[plain(row[0])] = (float(plain(row[col]).replace(",", "")), n)
            except (ValueError, IndexError):
                continue
        if out:
            return out
    return {}


def priced_hours(scope_path):
    text = Path(scope_path).read_text(encoding="utf-8")
    for n, line in enumerate(text.splitlines(), 1):
        m = LABOR_LINE.search(line)
        if m:
            return {k: float(v.replace(",", "")) for k, v in PAIR.findall(m.group(1))}, n
    return {}, 0


def check_hours(path, text, scope_path, out):
    booked = booked_hours(text)
    priced, where = priced_hours(scope_path)
    if not booked or not priced:
        return
    diff = [(p, booked[p], priced[p]) for p in priced if p in booked and abs(booked[p][0] - priced[p]) > 0.05]
    if not diff:
        return
    total_b = sum(h for h, _n in booked.values())
    total_p = sum(priced.values())
    line = min(b[1] for _p, b, _h in diff)
    detail = ", ".join("%s %g against %g" % (p, b[0], h) for p, b, h in diff)
    out.append(Finding("error", "hours", path, line,
                       "booked hours per person differ from the hours the cost estimate prices (%s:%d): %s; "
                       "totals %g against %g. The schedule and the labor baseline describe different "
                       "assignments; re-price, re-level, or record the change" % (scope_path, where, detail,
                                                                                   total_b, total_p)))


def run(path, charter=None, scope=None, breaks=()):
    text = Path(path).read_text(encoding="utf-8")
    rows = schedule_rows(text)
    out = []
    check_sequence(path, rows, out)
    windows = list(breaks) + (charter_breaks(charter) if charter else [])
    check_breaks(path, rows, windows, out)
    if scope:
        check_hours(path, text, scope, out)
    return out, len(rows)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("schedule", help="the 2.18 Markdown file")
    ap.add_argument("--charter", help="charter Markdown, for the breaks it dates")
    ap.add_argument("--scope", help="scope package Markdown, for the hours the cost estimate prices")
    ap.add_argument("--break", dest="breaks", nargs="+", action="append", default=[], metavar="DATE",
                    help="a break as a first day and, optionally, a last day (YYYY-MM-DD or 6 February 2027)")
    args = ap.parse_args(argv)
    for p in [args.schedule, args.charter, args.scope]:
        if p and not Path(p).is_file():
            ap.error("no such file: %s" % p)
    breaks = []
    for given in args.breaks:
        days = [parse_date(d) for d in given]
        if len(days) > 2 or not all(days):
            ap.error("--break takes one or two dates")
        breaks.append((days[0], days[1] if len(days) > 1 else None, 0, ""))
    out, count = run(args.schedule, args.charter, args.scope, breaks)
    for f in sorted(out, key=lambda f: (f.line, f.check)):
        print(fmt_finding(f))
    errors = sum(f.level == "error" for f in out)
    print("%d error(s), %d warning(s) over %d dated rows of %s" % (errors, len(out) - errors, count, args.schedule))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
