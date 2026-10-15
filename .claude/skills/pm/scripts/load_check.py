"""Load per person per week from the WBS dictionary of the scope package.

Each activity's hours are spread evenly over the Monday to Friday days of its
work package's Due Dates window, summed by person and week, and compared with
the person's weekly limit. The hours are spread evenly, so a week is a lead,
not a finding: read the package windows behind it. The check reads the
dictionary's due dates, not the levelled dates of a 2.18 (tools/level.py and
check_schedule.py cover those).

    load_check.py docs/scope-package.en.md
    load_check.py docs/scope-package.en.md --limit MOB1=20 --leaves MOB1=2026-12-18
    load_check.py docs/scope-package.en.md --only-leaf --exclude 1.1.1.3
    load_check.py docs/scope-package.en.md --charter docs/charter-package.en.md --holiday 2027-02-06:2027-02-14
    load_check.py docs/scope-package.en.md --daily-limit 8
    load_check.py docs/scope-package.en.md --schedule docs/forms/2-18-project-schedule.en.md --limit MOB1=20
    load_check.py docs/scope-package.en.md --limit MOB1=20 --explained overload="pending 3.3 moves the window"

The default limit is 40 hours a week for everyone; a part-time person's limit
and a leaving date come from the charter and are passed by the caller, never
assumed here. When the charter states no weekly figure for a part-time person
(it gives person-months), the 40 default judges that person as full time and hides
an overload: report the person-months against the window, ask the sponsor for the
weekly limit, and run with an assumed limit labelled as assumed (references/load-check.md).
--leaves reports a person's dated work after the given date (write the date as YYYY-MM-DD).
A person with no --limit is judged against the default 40, and each such finding says the limit is assumed.
--schedule FILE spreads each activity's hours over the Start to Finish of its row in a levelled 2.18 instead of the
dictionary window: the hours come from the dictionary (or from the "NAME 21 h" shares a divided row prints), the
dates from the 2.18. Still an even spread, so a week is a lead.
--explained overload=REASON turns the week and day overload findings into warnings that carry the reason (the
reason must name the document that gives it, such as a pending change request); a work-after-leaving finding is
never explained away. Severity: an overload is an error until a document explains it, then a warning naming the
decision it waits for (references/audit-template.md).
--only-leaf skips a sheet whose code is the prefix of another sheet's code
(a control account that repeats its package's hours); --exclude skips named
sheets.

--holiday START[:END] (repeatable, YYYY-MM-DD) takes those days out of every window
before the hours are spread; --charter reads the breaks the charter dates with an end
(a break with only a first day cannot be applied and is listed, since nothing says when it ends).
A window that falls wholly inside a break has no working day and is listed as skipped.
Three more findings, each a lead to read behind: a day that holds more than 24 hours of
one person (always reported, since no day holds more), a day above --daily-limit when
one is given (the limit is the caller's, from the charter or the team; none is assumed),
and, with --charter, a package whose window ends after the date of a milestone its sheet
lists under Milestones (it feeds a gate it crosses; the scope package's roll-up states
the deliberate cases). Exit code 1 when a week or a day is over its limit or work follows a
leaving date, 0 otherwise (a gate crossing is reported and does not change the code), 2 for
a usage error.
"""

import argparse
import collections
import datetime
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[4] / "tools"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_schedule  # noqa: E402
import check_scope  # noqa: E402
import schedule  # noqa: E402

DEFAULT_LIMIT = 40.0
HOURS_IN_A_DAY = 24.0


def weekdays(start, finish, holidays=()):
    days = [start + datetime.timedelta(n) for n in range((finish - start).days + 1)]
    return [d for d in days if d.weekday() < 5 and not any(a <= d <= b for a, b in holidays)]


def allocations(text, only_leaf=False, exclude=(), holidays=()):
    """Return ([(code, person, hours, days)], skipped codes): each activity's hours with the working days of
    its package's Due Dates window, less the holidays. A sheet with no working day is skipped."""
    windows = schedule.parse_due_dates(text)
    sheets = check_scope.parse_sheets(text)
    codes = [s["code"] for s in sheets]
    found, skipped = [], []
    for sheet in sheets:
        code = sheet["code"]
        parent = only_leaf and any(c != code and c.startswith(code + ".") for c in codes)
        if code in exclude or parent or code not in windows:
            skipped.append(code)
            continue
        days = weekdays(*windows[code], holidays=holidays)
        if not days:
            skipped.append(code)
            continue
        for person, hours, _rate, _cost in sheet["acts"]:
            found.append((code, person, hours, days))
    return found, skipped


def schedule_allocations(scope_text, schedule_text, holidays=()):
    """Return ([(code, person, hours, days)], unmatched): the dictionary's hours placed in the Start to Finish of
    each activity row of a levelled 2.18. A row that prints "NAME 21 h" shares uses those hours; a plain name takes
    the dictionary hours of that activity. A row the dictionary does not know is listed in unmatched."""
    dictionary = {}
    for raw in scope_text.splitlines():
        row = check_scope.cells(raw) if raw.startswith("|") else []
        if len(row) >= 4 and re.match(r"^\d+(?:\.\d+)+-A\d+$", row[0]) and row[2]:
            dictionary.setdefault(row[0], {})[row[2]] = check_scope.money(row[3])
    found, unmatched = [], []
    for header, body in check_schedule.tables(schedule_text):
        names = [h.lower() for h in header]
        if not {"wbs", "start", "finish", "resource name"} <= set(names):
            continue
        for _n, row in body:
            cell = lambda name: row[names.index(name)] if names.index(name) < len(row) else ""
            code = check_schedule.plain(cell("wbs"))
            start, finish = check_schedule.parse_date(cell("start")), check_schedule.parse_date(cell("finish"))
            if not re.match(r"^\d+(?:\.\d+)+-A\d+$", code) or not start or not finish:
                continue
            days = weekdays(start, finish, holidays)
            if not days:
                unmatched.append(code)
                continue
            for token in check_schedule.plain(cell("resource name")).split(","):
                m = re.match(r"^\s*(\S+?)(?:\s+([\d.]+)\s*h)?\s*$", token)
                if not m:
                    continue
                person = m.group(1)
                hours = float(m.group(2)) if m.group(2) else dictionary.get(code, {}).get(person)
                if hours is None:
                    unmatched.append(code)
                    continue
                found.append((code, person, hours, days))
    return found, unmatched


def schedule_peaks(schedule_text):
    """{person: peak hours} from the Resource table of a levelled 2.18 (a column headed Peak hours)."""
    for header, body in check_schedule.tables(schedule_text):
        names = [h.lower() for h in header]
        if not names or names[0] != "resource" or "peak hours" not in names:
            continue
        col, out = names.index("peak hours"), {}
        for _n, row in body:
            try:
                out[check_schedule.plain(row[0])] = float(check_schedule.plain(row[col]).replace(",", ""))
            except (ValueError, IndexError):
                continue
        return out
    return {}


def spread(text, only_leaf=False, exclude=(), holidays=(), found_skipped=None):
    """Return ({(person, week start): hours}, {person: latest date with work}, skipped codes)."""
    found, skipped = found_skipped or allocations(text, only_leaf, exclude, holidays)
    load = collections.defaultdict(float)
    last = {}
    for _code, person, hours, days in found:
        for d in days:
            load[(person, d - datetime.timedelta(d.weekday()))] += hours / len(days)
        if hours:
            last[person] = max(last.get(person, days[-1]), days[-1])
    return load, last, skipped


def daily(text, only_leaf=False, exclude=(), holidays=(), found_skipped=None):
    """{(person, day): hours} with each activity's hours spread evenly over its window's working days."""
    found, _skipped = found_skipped or allocations(text, only_leaf, exclude, holidays)
    load = collections.defaultdict(float)
    for _code, person, hours, days in found:
        for d in days:
            load[(person, d)] += hours / len(days)
    return load


def gate_crossings(text, milestones, only_leaf=False, exclude=()):
    """[(code, milestone id, window finish, milestone date)] for each sheet whose window ends after the date of
    a milestone its Milestones row lists. milestones is {id: date} from the charter's summary table."""
    windows = schedule.parse_due_dates(text)
    sheets = check_scope.parse_sheets(text)
    codes = [s["code"] for s in sheets]
    found, code = [], None
    for raw in text.splitlines():
        m = re.match(r"^#### (\d+(?:\.\d+)+) ", raw)
        if m:
            code = m.group(1)
        elif code and raw.startswith("| Milestones |") and code in windows and code not in exclude:
            if only_leaf and any(c != code and c.startswith(code + ".") for c in codes):
                continue
            for mid in dict.fromkeys(re.findall(r"\bM\d+\b", raw)):
                if mid in milestones and windows[code][1] > milestones[mid]:
                    found.append((code, mid, windows[code][1], milestones[mid]))
    return found


def parse_pairs(items, kind):
    out = {}
    for text in items:
        name, sep, value = text.partition("=")
        if not sep or not name.strip():
            raise ValueError("%s %r: write NAME=VALUE" % (kind, text))
        out[name.strip()] = value.strip()
    return out


def check(text, limits, leaves, default_limit=DEFAULT_LIMIT, only_leaf=False, exclude=(), holidays=(),
          daily_limit=None, found_skipped=None, kinds=None):
    """Findings as strings. Pass a list as kinds to receive one word per finding: "overload" or "leaving"."""
    load, last, skipped = spread(text, only_leaf, exclude, holidays, found_skipped)
    findings = []
    kinds = [] if kinds is None else kinds

    def add(kind, line):
        findings.append(line)
        kinds.append(kind)

    for (person, day), hours in sorted(daily(text, only_leaf, exclude, holidays, found_skipped).items(),
                                       key=lambda kv: (kv[0][0], kv[0][1])):
        if hours > HOURS_IN_A_DAY + 1e-9:
            add("overload", "%s on %s: %.1f hours in one day, more than a day holds (%g); the package window is "
                "shorter than its hours" % (person, day.isoformat(), hours, HOURS_IN_A_DAY))
        elif daily_limit is not None and hours > daily_limit + 1e-9:
            add("overload", "%s on %s: %.1f hours in one day against a daily limit of %g" % (
                person, day.isoformat(), hours, daily_limit))
    for (person, week), hours in sorted(load.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        limit = limits.get(person, default_limit)
        if hours > limit + 1e-9:
            assumed = "" if person in limits else " (limit assumed: the default, no --limit given for %s)" % person
            add("overload", "%s week of %s: %.1f hours against a limit of %g%s" % (
                person, week.isoformat(), hours, limit, assumed))
    for person, date in sorted(leaves.items()):
        if last.get(person) and last[person] > date:
            add("leaving", "%s has dated work until %s, after the leaving date %s" % (
                person, last[person].isoformat(), date.isoformat()))
    return findings, skipped


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("scope", help="the scope package Markdown (docs/scope-package.en.md)")
    parser.add_argument("--limit", action="append", default=[], metavar="NAME=HOURS",
                        help="a person's weekly limit; everyone else gets %g" % DEFAULT_LIMIT)
    parser.add_argument("--leaves", action="append", default=[], metavar="NAME=YYYY-MM-DD",
                        help="the last date a person is available")
    parser.add_argument("--only-leaf", action="store_true", help="skip a sheet that is the prefix of another sheet")
    parser.add_argument("--exclude", action="append", default=[], metavar="CODE", help="skip this sheet")
    parser.add_argument("--holiday", action="append", default=[], metavar="START[:END]",
                        help="a day or range (YYYY-MM-DD) with no work; repeatable")
    parser.add_argument("--daily-limit", type=float, metavar="HOURS",
                        help="also report a person-day above this many hours (the caller's figure, none assumed)")
    parser.add_argument("--charter", help="charter Markdown: its dated breaks and its milestone dates")
    parser.add_argument("--schedule", metavar="FILE", help="a levelled 2.18: place the hours in its rows instead of "
                        "the dictionary windows")
    parser.add_argument("--explained", action="append", default=[], metavar="overload=REASON",
                        help="report the overload findings as warnings with this reason (name the document)")
    args = parser.parse_args(argv)
    try:
        limits = {k: float(v) for k, v in parse_pairs(args.limit, "--limit").items()}
        leaves = {}
        for k, v in parse_pairs(args.leaves, "--leaves").items():
            try:
                leaves[k] = datetime.date.fromisoformat(v)
            except ValueError:
                raise ValueError("--leaves %s=%r: write the date as YYYY-MM-DD (for example 2026-12-18)" % (k, v))
        explained = parse_pairs(args.explained, "--explained")
        if set(explained) - {"overload"} or any(not r for r in explained.values()):
            raise ValueError("--explained takes overload=REASON with a reason that names the document giving it")
        holidays = [tuple(datetime.date.fromisoformat(x) for x in (h.split(":") + [h])[:2]) if ":" not in h
                    else tuple(datetime.date.fromisoformat(x) for x in h.split(":", 1)) for h in args.holiday]
        text = Path(args.scope).read_text(encoding="utf-8")
        charter = Path(args.charter).read_text(encoding="utf-8") if args.charter else None
    except (ValueError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    notes = []
    if charter:
        for first, last, line, sentence in check_schedule.charter_breaks(args.charter):
            if last:
                holidays.append((first, last))
            else:
                notes.append("charter line %d dates a break from %s with no end date, so it is not applied; pass "
                             "--holiday %s:<last day> once the end is known" % (line, first.isoformat(),
                                                                                first.isoformat()))
    found_skipped = None
    if args.schedule:
        try:
            found, unmatched = schedule_allocations(text, Path(args.schedule).read_text(encoding="utf-8"), holidays)
        except OSError as exc:
            print("error: %s" % exc, file=sys.stderr)
            return 2
        found_skipped = (found, unmatched)
        for person, peak in sorted(schedule_peaks(Path(args.schedule).read_text(encoding="utf-8")).items()):
            if peak > limits.get(person, DEFAULT_LIMIT) + 1e-9:
                notes.append("%s: the schedule's own Resource table prints a peak week of %g hours, above the limit "
                             "of %g%s" % (person, peak, limits.get(person, DEFAULT_LIMIT),
                                          "" if person in limits else " (assumed default)"))
        if unmatched:
            notes.append("%d schedule row(s) matched no dictionary hours or have no working day (%s)" % (
                len(unmatched), ", ".join(dict.fromkeys(unmatched[:6]))))
    kinds = []
    findings, skipped = check(text, limits, leaves, only_leaf=args.only_leaf, exclude=set(args.exclude),
                              holidays=holidays, daily_limit=args.daily_limit, found_skipped=found_skipped,
                              kinds=kinds)
    blocking = 0
    for line, kind in zip(findings, kinds):
        if kind == "overload" and "overload" in explained:
            print("warning (explained, awaiting decision: %s): %s" % (explained["overload"], line))
        else:
            blocking += 1
            print(line)
    crossings = []
    if charter:
        miles = {mid: day for mid, _name, day in schedule.parse_milestones(charter)}
        crossings = gate_crossings(text, miles, args.only_leaf, set(args.exclude))
        for code, mid, finish, gate in crossings:
            print("gate: %s ends %s, after %s on %s, a milestone its sheet lists; read the sheet and the roll-up "
                  "for a stated reason" % (code, finish.isoformat(), mid, gate.isoformat()))
    for note in notes:
        print("note: " + note)
    print("%d finding(s), %d gate crossing(s); hours spread evenly over each package's Monday to Friday window "
          "less %d holiday range(s); %d sheet(s) skipped. Report a week as overloaded only when it is clearly "
          "over." % (len(findings), len(crossings), len(holidays), len(skipped)))
    if args.schedule:
        print("source of the windows: the Start and Finish of the rows in %s. A levelled form places hours day by "
              "day, so an even spread over overlapping rows can show a week the form does not have: when the "
              "form's own Resource table says no week is above the limit, read the rows of the week before "
              "reporting it." % args.schedule)
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
