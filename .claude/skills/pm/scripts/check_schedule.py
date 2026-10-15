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
    so read both rows before reporting: a finding is a lead. The activity it
    names is the one that shares the most words with the check, or for a closeout
    the warranty activity, else the latest finisher; the others are counted.
go-live (warning): an activity named go-live, production deployment,
    switchover or cutover finishes before an activity that executes or signs off
    the UAT (a UAT or user acceptance activity of execution, testing or
    sign-off, or an "acceptance decision"). Any package, not only the same one.
break (warning, or error when the charter says the break can absorb no overrun or cannot be crossed): rows dated inside a break. Breaks come from --break, and from
    the charter: a sentence naming a holiday, break, freeze or New Year that
    says it begins (and, if stated, ends) on a date. Where the charter gives
    only the first day, every row on or after it is reported, since nothing
    says when the break ends.
hours (error): booked hours per person in the schedule differ from the scope
    package's 'Labor hours by resource' line, so the schedule and the cost
    baseline describe different assignments. The finding also prices both
    sets of hours at each person's rate from the WBS dictionary activity
    tables (the Labor Rate column), so the cost of the difference is stated.

closeout (warning): a closeout activity finishes before a milestone whose name says warranty or closeout
    (M7 in this project), so the project is closed before the period it closes; this holds when no activity
    is named warranty, where the sequence check can only name the latest finisher.
test-order (warning): an activity that executes or retests names functions (F01 to F03) and finishes before
    the package named for one of them is built; read both rows, and the dictionary, which may ask for the order.
review-order (warning): a review, approval or walkthrough finishes before an activity of ANOTHER package or
    control account that it shares two or more content words with and that is not itself a check; the sequence
    check only compares inside one package or control account.
stated-count (warning): a task name states a number of weeks or days ("Weekly status report, 21 weeks") that
    differs from the row's own window (more than one week, or a different number of working days), and, with
    --scope, a dictionary sentence that states a duration ("pilot ... for the two weeks before go-live") for an
    activity of that sheet whose row is shorter than the stated working days. Compare with the sheet before reporting.

milestone-name (warning): the milestone names on page 1 of the 2.18 differ from the names on page 2 or from
    the charter's summary milestone table (read from --charter), or a milestone is dated differently on the two
    pages. The names are copied project text, so a shortened name is one ID with two texts.

--explained CHECK (repeatable; hours or milestone-name bare; break, sequence, go-live and the other order checks
only as CHECK=REASON; see below) reports that check's findings as warnings
tagged "explained, awaiting decision". Use it only when a document states the reason (a pending change
request 3.3 with an empty disposition) and name that document in the audit; the mismatch stays a finding
until the request is decided (references/audit-template.md). A pending 3.3 explains a forecast date or an
hour total; it never explains an order defect (a review before the thing it reviews, a go-live before the
UAT). So sequence and go-live are accepted only as --explained sequence="REASON" with the reason the order
changed, quoted from the document; a break needs its reason too (--explained break="REASON", the document
that dates the forecast); without a reason the option is refused with exit code 2.

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
GO_LIVE_WORDS = re.compile(r"\b(?:go-live|go live|switchover|cut-?over|production deployment)\b", re.I)
UAT_RUN_WORDS = re.compile(r"\b(?:UAT|user acceptance)\b.*\b(?:execution|executing|testing|sign(?:ed)?[- ]?off)\b"
                           r"|\bacceptance decision\b", re.I)
GENERIC = {"with", "against", "from", "that", "this", "their", "after", "before", "report", "the", "and", "for",
           "plan", "review", "approval", "walkthrough", "verification", "acceptance", "written", "check"}
BREAK_WORDS = re.compile(r"\b(?:holiday|break|freeze|closure|New Year|Tết)\b", re.I)
BEGINS = re.compile(r"\b(?:begins|starts|runs from|from)\s+(?:on\s+)?(\d{1,2} (?:%s) \d{4})" % "|".join(MONTHS))
ENDS = re.compile(r"\b(?:ends|until|to|through)\s+(?:on\s+)?(\d{1,2} (?:%s) \d{4})" % "|".join(MONTHS))
LABOR_LINE = re.compile(r"Labor hours by resource:\s*([^.]+(?:\.\d[^.]*)*)")
PAIR = re.compile(r"\b([A-Z][A-Z0-9]*)\s+([\d,]+(?:\.\d+)?)\b")

NUMBER_WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve".split())}
STATED_SPAN = re.compile(r"\b(\d{1,3}|%s)[- ](weeks?|days?)\b" % "|".join(NUMBER_WORDS), re.I)
DICT_DURATION = re.compile(r"\b(?:for|over|during)\s+(?:the\s+)?(\d{1,3}|%s)\s+(weeks?|working days|days)\b"
                           % "|".join(NUMBER_WORDS), re.I)
EXECUTE_WORDS = re.compile(r"\b(?:execut\w*|retest\w*|test run)\b", re.I)
FUNCTION_ID = re.compile(r"\b([A-Z])(\d{2})\b")
NO_OVERRUN = re.compile(r"\b(?:break|holiday|freeze)\b.*\b(?:absorb(?:s)? no|cannot absorb|no overrun)\b"
                        r"|\b(?:absorb(?:s)? no|cannot absorb|no overrun)\b.*\b(?:break|holiday|freeze)\b", re.I)

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
            last = pick_input(r, inputs, closing)
            scope = "phase" if closing else ("work package" if last.code.split("-")[0] == pkg
                                             else "control account")
            more = "" if len(inputs) == 1 else " (%d activities of it finish later in all)" % len(inputs)
            out.append(Finding("warning", "sequence", path, r.line,
                               "%s '%s' finishes %s, before %s '%s' (line %d) of the same %s finishes %s%s; "
                               "if that is its input, the check comes before the thing it checks"
                               % (r.code, r.name, fmt(r.finish), last.code, last.name, last.line, scope,
                                  fmt(last.finish), more)))


def words(name):
    return {w for w in re.findall(r"[a-z]{4,}", name.lower())} - GENERIC


def pick_input(r, inputs, closing):
    """The activity to name as the thing a check or closeout comes before: for a closeout the warranty
    activity, for a check the activity that shares the most words with it, else the latest finisher."""
    latest = lambda xs: max(xs, key=lambda x: x.finish)
    if closing:
        warranty = [x for x in inputs if re.search(r"warrant", x.name, re.I)]
        return latest(warranty) if warranty else latest(inputs)
    shared = [(len(words(r.name) & words(x.name)), x) for x in inputs]
    best = max(n for n, _x in shared)
    return latest([x for n, x in shared if n == best]) if best else latest(inputs)


def check_go_live(path, rows, out):
    """A go-live, switchover or production deployment that finishes before a UAT execution or sign-off."""
    acts = [r for r in rows if r.activity]
    uat = [x for x in acts if UAT_RUN_WORDS.search(x.name)]
    for r in acts:
        if not GO_LIVE_WORDS.search(r.name) or UAT_RUN_WORDS.search(r.name):
            continue
        later = [x for x in uat if x.finish > r.finish]
        if later:
            last = max(later, key=lambda x: x.finish)
            out.append(Finding("warning", "go-live", path, r.line,
                               "%s '%s' finishes %s, before %s '%s' (line %d) finishes %s; go-live depends on the "
                               "UAT result, so read both rows and the charter's UAT rule before reporting"
                               % (r.code, r.name, fmt(r.finish), last.code, last.name, last.line,
                                  fmt(last.finish))))


def function_ids(name):
    """The function IDs a row name lists: "F01 to F03" gives F01, F02, F03; "F04 and F05" gives both."""
    found = []
    for m in re.finditer(r"\b([A-Z])(\d{2})(?:\s+to\s+\1(\d{2}))?\b", name):
        first, last = int(m.group(2)), int(m.group(3) or m.group(2))
        found.extend("%s%02d" % (m.group(1), n) for n in range(first, last + 1))
    return found


def check_test_order(path, rows, out):
    """An execution or retest row finishes before the package named for a function its own package tests. The
    functions are the IDs named by the row or by any row of its package ("Test case authoring for F01 to F03")."""
    for r in (x for x in rows if x.activity and EXECUTE_WORDS.search(x.name)):
        pkg = ACTIVITY.match(r.code).group(1)
        ids = sorted({i for x in rows if x.code.split("-")[0] == pkg for i in function_ids(x.name)})
        if not ids:
            continue
        built = [x for x in rows if x is not r and not CHECK_WORDS.search(x.name) and not EXECUTE_WORDS.search(x.name)
                 and not re.search(r"\btest", x.name, re.I) and FUNCTION_ID.match(x.name)
                 and FUNCTION_ID.match(x.name).group(0) in ids and x.finish > r.finish]
        if built:
            last = max(built, key=lambda x: x.finish)
            out.append(Finding("warning", "test-order", path, r.line,
                               "%s '%s' finishes %s, before %s '%s' (line %d) finishes %s%s; if the test runs against "
                               "what was built, it comes before the build; the dictionary may ask for this order, so "
                               "read the sheet" % (r.code, r.name, fmt(r.finish), last.code or "the package",
                                                   last.name, last.line, fmt(last.finish),
                                                   "" if len(built) == 1 else " (%d rows of it finish later)"
                                                   % len(built))))


def check_review_order(path, rows, out):
    """A check that finishes before the activity of another package or control account it names most (two or
    more content words in common, the activity itself not a check). Inside one package or control account the
    sequence check already compares. A lead: read both rows."""
    acts = [r for r in rows if r.activity]
    for r in acts:
        if not CHECK_WORDS.search(r.name) or CLOSE_WORDS.search(r.name):
            continue
        pkg = ACTIVITY.match(r.code).group(1)
        best, shared = None, set()
        for x in acts:
            if x is r or CHECK_WORDS.search(x.name) or CLOSE_WORDS.search(x.name) or EXECUTE_WORDS.search(x.name):
                continue
            if ACTIVITY.match(x.code).group(1).split(".")[:3] == pkg.split(".")[:3]:
                continue
            common = words(r.name) & words(x.name)
            if len(common) >= 2 and (best is None or len(common) > len(shared)):
                best, shared = x, common
        if best is not None and best.finish > r.finish:
            out.append(Finding("warning", "review-order", path, r.line,
                               "%s '%s' finishes %s, before %s '%s' (line %d) of another package finishes %s "
                               "(words in common: %s); if that is the thing it reviews, the review comes first"
                               % (r.code, r.name, fmt(r.finish), best.code, best.name, best.line, fmt(best.finish),
                                  ", ".join(sorted(shared)))))


def check_closeout(path, rows, out):
    """A closeout activity that finishes before a milestone whose name says warranty or closeout."""
    marks = [r for r in rows if not r.code and re.match(r"M\d+\b", r.name) and re.search(r"warrant|closeout", r.name, re.I)]
    for r in (x for x in rows if x.activity and CLOSE_WORDS.search(x.name)):
        later = [m for m in marks if m.finish > r.finish]
        if later:
            m = max(later, key=lambda x: x.finish)
            out.append(Finding("warning", "closeout", path, r.line,
                               "%s '%s' finishes %s, before %s (line %d) on %s; the closeout comes before the period "
                               "the milestone names" % (r.code, r.name, fmt(r.finish), m.name.split(" ", 1)[0] + " '"
                                                        + m.name.split(" ", 1)[1] + "'", m.line, fmt(m.finish))))


def number_of(token):
    return int(token) if token.isdigit() else NUMBER_WORDS[token.lower()]


def working_days(start, finish):
    return sum(1 for n in range((finish - start).days + 1) if (start + datetime.timedelta(n)).weekday() < 5)


def check_stated_count(path, rows, scope, out):
    """A number of weeks or days in a task name against the row's window, and a duration the dictionary states."""
    for r in (x for x in rows if x.activity):
        for m in STATED_SPAN.finditer(r.name):
            stated, unit = number_of(m.group(1)), m.group(2).lower()
            if unit.startswith("week"):
                span = (r.finish - r.start).days / 7
                bad = abs(span - stated) > 1
                window = "%.0f weeks" % span
            else:
                span = working_days(r.start, r.finish)
                bad = span != stated
                window = "%d working days" % span
            if bad:
                out.append(Finding("warning", "stated-count", path, r.line,
                                   "%s '%s' states %d %s but its window %s to %s is %s"
                                   % (r.code, r.name, stated, unit, fmt(r.start), fmt(r.finish), window)))
    if not scope:
        return
    sheet = None
    for n, raw in enumerate(Path(scope).read_text(encoding="utf-8").splitlines(), 1):
        head = re.match(r"^#### (\d+(?:\.\d+)+) ", raw)
        if head:
            sheet = head.group(1)
            continue
        if not sheet or not raw.startswith("| Description of Work |"):
            continue
        for sentence in re.split(r"(?<=[.;])\s+", plain(cells(raw)[1])):
            for m in DICT_DURATION.finditer(sentence):
                clause = sentence[:m.end()].rsplit(",", 1)[-1]
                own = [x for x in rows if x.activity and ACTIVITY.match(x.code).group(1) == sheet]
                best = [x for x in own if len(words(clause) & words(x.name)) >= 2]
                if not best:
                    continue
                row = max(best, key=lambda x: len(words(clause) & words(x.name)))
                stated = number_of(m.group(1)) * (5 if m.group(2).lower().startswith("week") else 1)
                got = working_days(row.start, row.finish)
                if got < stated:
                    out.append(Finding("warning", "stated-count", path, row.line,
                                       "%s '%s' runs %d working days (%s to %s), but %s:%d says '%s' (%d working "
                                       "days)" % (row.code, row.name, got, fmt(row.start), fmt(row.finish), scope, n,
                                                  clause.strip() + m.group(0)[len(m.group(0)):], stated)))


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


def strict_break(charter_path):
    """(line, sentence) of a charter sentence that says a break can absorb no overrun, or None."""
    text = Path(charter_path).read_text(encoding="utf-8")
    for n, line in enumerate(text.splitlines(), 1):
        for sentence in re.split(r"(?<=[.;])\s+", plain(line)):
            if NO_OVERRUN.search(sentence):
                return n, sentence.strip()
    return None


def check_breaks(path, rows, breaks, out, strict=None):
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
        why = ""
        if strict:
            why = ("; the charter says the break can absorb no overrun (charter line %d: '%s'), so work booked inside "
                   "it contradicts the charter" % (strict[0], strict[1][:90]))
        out.append(Finding("error" if strict else "warning", "break", path, hit[0].line,
                           "%d activities and %d milestones are dated %s (%s): %s%s"
                           % (len(acts), len(milestones), window, source, sample, why)))


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


def labor_rates(scope_path):
    """{resource: rate} from the Resource and Labor Rate columns of the activity tables."""
    text = Path(scope_path).read_text(encoding="utf-8")
    found = {}
    for header, body in tables(text):
        names = [h.lower() for h in header]
        if "resource" not in names or "labor rate" not in names:
            continue
        r_col, c_col = names.index("resource"), names.index("labor rate")
        for _n, row in body:
            try:
                found.setdefault(plain(row[r_col]), float(plain(row[c_col]).replace(",", "")))
            except (ValueError, IndexError):
                continue
    return found


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
    rates = labor_rates(scope_path)
    priced_note = ""
    if all(p in rates for p in priced):
        cost_b = sum(booked[p][0] * rates[p] for p in priced if p in booked)
        cost_p = sum(priced[p] * rates[p] for p in priced)
        priced_note = ("; at the rates of the WBS dictionary the booked hours cost {:,.0f} against {:,.0f} "
                       "priced, a difference of {:,.0f}").format(cost_b, cost_p, cost_b - cost_p)
    out.append(Finding("error", "hours", path, line,
                       "booked hours per person differ from the hours the cost estimate prices (%s:%d): %s; "
                       "totals %g against %g%s. The schedule and the labor baseline describe different "
                       "assignments; re-price, re-level, or record the change" % (scope_path, where, detail,
                                                                                   total_b, total_p, priced_note)))


MILESTONE_ID = re.compile(r"^(M\d+)\s+(.+)$")


def milestone_tables(text):
    """({id: (name, line, finish)} from the Gantt page, {id: (name, line, finish)} from the milestone page)."""
    page1, page2 = {}, {}
    for header, body in tables(text):
        names = [h.lower() for h in header]
        if "task name" not in names or "finish" not in names:
            continue
        name_col, finish_col = names.index("task name"), names.index("finish")
        target = page2 if "indicator" in names else page1
        for n, row in body:
            if max(name_col, finish_col) >= len(row):
                continue
            m = MILESTONE_ID.match(plain(row[name_col]))
            if m and (target is page2 or not plain(row[names.index("wbs")] if "wbs" in names else "")):
                target[m.group(1)] = (m.group(2).strip(), n, parse_date(row[finish_col]))
    return page1, page2


def charter_milestones(charter_path):
    """{id: (name, line)} from the charter's summary milestone table (ID, Milestone, Due date)."""
    found = {}
    text = Path(charter_path).read_text(encoding="utf-8")
    for header, body in tables(text):
        names = [h.lower() for h in header]
        if names[:2] != ["id", "milestone"]:
            continue
        for n, row in body:
            if len(row) >= 2 and re.match(r"^M\d+$", plain(row[0])):
                found[plain(row[0])] = (plain(row[1]), n)
    return found


def check_milestones(path, text, charter, out):
    page1, page2 = milestone_tables(text)
    if not page1 or not page2:
        return
    official = charter_milestones(charter) if charter else {}
    for mid in sorted(page1, key=lambda x: int(x[1:])):
        name1, line1, date1 = page1[mid]
        if mid in page2:
            name2, line2, date2 = page2[mid]
            if name1 != name2:
                out.append(Finding("warning", "milestone-name", path, line1,
                                   "%s is '%s' on page 1 (line %d) and '%s' on page 2 (line %d); one milestone, "
                                   "one text" % (mid, name1, line1, name2, line2)))
            if date1 != date2 and date1 and date2:
                out.append(Finding("warning", "milestone-name", path, line1,
                                   "%s is dated %s on page 1 (line %d) and %s on page 2 (line %d)"
                                   % (mid, fmt(date1), line1, fmt(date2), line2)))
        if mid in official and name1 != official[mid][0]:
            out.append(Finding("warning", "milestone-name", path, line1,
                               "%s is '%s' on page 1 (line %d) and '%s' in the charter (%s:%d)"
                               % (mid, name1, line1, official[mid][0], charter, official[mid][1])))


def run(path, charter=None, scope=None, breaks=(), explained=()):
    text = Path(path).read_text(encoding="utf-8")
    rows = schedule_rows(text)
    out = []
    check_sequence(path, rows, out)
    check_go_live(path, rows, out)
    check_closeout(path, rows, out)
    check_test_order(path, rows, out)
    check_review_order(path, rows, out)
    check_stated_count(path, rows, scope, out)
    windows = list(breaks) + (charter_breaks(charter) if charter else [])
    check_breaks(path, rows, windows, out, strict_break(charter) if charter else None)
    check_milestones(path, text, charter, out)
    if scope:
        check_hours(path, text, scope, out)
    soft = explained_checks(explained)
    out = [Finding("warning", f.check, f.path, f.line, f.message + " [explained%s, awaiting decision]" % soft[f.check])
           if f.check in soft else f for f in out]
    return out, len(rows)


ORDER_CHECKS = ("sequence", "go-live", "break", "closeout", "test-order", "review-order", "stated-count")


def explained_checks(given):
    """{check: ': reason' or ''} from --explained values. An order check needs a reason: 'sequence=REASON'."""
    soft = {}
    for item in given:
        check, _, reason = item.partition("=")
        if check not in ("hours", "milestone-name") + ORDER_CHECKS:
            raise ValueError("--explained takes hours or milestone-name, or %s as CHECK=REASON, not %r"
                             % (", ".join(ORDER_CHECKS), item))
        if check in ORDER_CHECKS and not reason.strip():
            raise ValueError("a pending change request explains a date or an hour total, not an order defect: "
                             "%s needs the reason (the document that gives it, or the reason the order changed), as "
                             "--explained %s=REASON" % (check, check))
        soft[check] = ": " + reason.strip() if reason.strip() else ""
    return soft


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("schedule", help="the 2.18 Markdown file")
    ap.add_argument("--charter", help="charter Markdown, for the breaks it dates")
    ap.add_argument("--scope", help="scope package Markdown, for the hours the cost estimate prices")
    ap.add_argument("--break", dest="breaks", nargs="+", action="append", default=[], metavar="DATE",
                    help="a break as a first day and, optionally, a last day (YYYY-MM-DD or 6 February 2027)")
    ap.add_argument("--explained", action="append", default=[], metavar="CHECK",
                    help="report this check's findings as warnings, because a document states the reason and "
                         "the decision is pending: hours or milestone-name; break, sequence, go-live, closeout, "
                         "test-order, review-order and stated-count only as CHECK=REASON with the reason quoted "
                         "from the document")
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
    try:
        explained_checks(args.explained)
    except ValueError as exc:
        ap.error(str(exc))
    out, count = run(args.schedule, args.charter, args.scope, breaks, args.explained)
    for f in sorted(out, key=lambda f: (f.line, f.check)):
        print(fmt_finding(f))
    errors = sum(f.level == "error" for f in out)
    print("%d error(s), %d warning(s) over %d dated rows of %s" % (errors, len(out) - errors, count, args.schedule))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
