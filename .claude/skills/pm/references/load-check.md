# Load per person per week

The charter claims an allocation per person (full time, or part time for a
window such as "joins after M2 and leaves after M5"). Spread each person's
hours over the working days of each package's window, sum by week, and compare
with that allocation. For the WBS dictionary as written:

```python
import collections, datetime, sys
sys.path.insert(0, "tools")
import check_scope, schedule
text = open("docs/scope-package.en.md", encoding="utf-8").read()
windows = schedule.parse_due_dates(text)          # {package: (start, finish)} from Due Dates
load = collections.defaultdict(float)
for sheet in check_scope.parse_sheets(text):      # activities as (resource, hours, rate, cost)
    start, finish = windows[sheet["code"]]
    days = [start + datetime.timedelta(n) for n in range((finish - start).days + 1)]
    days = [d for d in days if d.weekday() < 5]
    for res, hours, _rate, _cost in sheet["acts"]:
        for d in days:
            load[(res, d - datetime.timedelta(d.weekday()))] += hours / len(days)
for (res, week), h in sorted(load.items()):
    if h > 40:
        print(res, week, round(h, 1))
```

Use the person's own limit, not 40, for a part-time role, and check the last
dated work against the date the person is said to leave. This spreads hours
evenly, so report a week as overloaded only when it is clearly over, and say
the method in the finding. For the resource-levelled schedule, `python3
tools/level.py` prints the days anyone is booked above 8 hours and the hours by
person; compare each person's total with the hours the cost estimate prices for
that person, since the budget is hours times that person's rate.

**What this check cannot see.** It reads the dictionary's due dates, not the levelled
dates of the 2.18, so it says nothing about a person's load in the schedule the team
will follow; `tools/level.py` and `scripts/check_schedule.py` cover that (the second
compares booked with priced hours and prices the difference). The 2.18 form table
prints a person's hours only on divided activities, so the hours of the others have
to be read from the Resource loading table or the dictionary. Neither tool knows a
part-time limit or a leaving date unless you pass it, which is why the paragraph
above asks for them.

**The script.** `scripts/load_check.py` does the spread above and more:

```bash
python3 .claude/skills/pm/scripts/load_check.py docs/scope-package.en.md --charter docs/charter-package.en.md \
    --limit MOB1=<hours> --leaves MOB1=YYYY-MM-DD --holiday <first>:<last> --daily-limit <hours>
```

Every date is written YYYY-MM-DD (2026-12-18); a prose date stops the run with a message naming the format.

- `--holiday FIRST:LAST` (repeatable) and the breaks `--charter` reads (only those with an end date) are taken out of every window
  before the hours are spread, the way `check_schedule.py` reads them. A break the charter dates with a first day only cannot be
  applied and is printed as a note; ask the sponsor for its end.
- A person-day above 24 hours is always reported, since no day holds more: the window is shorter than the hours. `--daily-limit`
  adds a day above the caller's own figure; none is assumed.
- A person with no `--limit` is judged against the default 40, and each finding for that person says "limit assumed". Pass
  the person's own figure, or keep the label in the report.
- `--schedule FILE` replaces the dictionary windows with the Start and Finish of the activity rows of a levelled 2.18, with the
  hours from the dictionary (or from the "MOB1 21 h" shares a divided row prints). It is the check on the 40 hours per week the
  levelled form claims. A levelled form places hours day by day, so an even spread over overlapping rows can show a week the form
  does not have; read the rows of the week, and compare with the peak hours of the form's own Resource table (the script prints
  a note when a peak is above the limit).
- `--explained overload=REASON` turns the week and day overload findings into warnings that carry the reason; the reason names
  the document that gives it (a pending 3.3, a charter sentence). A work-after-leaving finding is never explained this way.
  Severity, stated once: an overload is an error until a document explains it, then a warning that names the decision it waits
  for (`audit-template.md`, severity).
- With `--charter`, a package whose window ends after the date of a milestone listed on its sheet is printed as a `gate:` line. Read the
  sheet and the roll-up first: the scope package states its deliberate cases (a package that crosses a gate for a stated reason).

- `--effort NAME=QTY:UNIT:FROM:TO` compares an effort the source states with the calendar window it is placed in. It needs no
  dictionary hours, so it catches what the spread cannot: a part-time role whose person-months do not fit between joining and
  leaving. UNIT is `pm` or `h`; FROM and TO are dates or milestone ids read from `--charter` (`MOB1=2.5:pm:M2:M5`).

**A part-time person the charter gives no weekly figure.** The charter states 2.5 person-months for the mobile developer and no
hours a week, and the dictionary spread alone judges that person against the default 40, as full time. Run the effort check
as well:

```bash
python3 .claude/skills/pm/scripts/load_check.py docs/scope-package.en.md --charter docs/charter-package.en.md \
    --effort MOB1=2.5:pm:M2:M5 --hours-per-pm <hours the source gives> --fraction MOB1=<stated fraction> \
    --effort-source "MOB1=docs/charter-package.en.md:<line>, docs/scope-package.en.md:<line>"
```

It prints the hours (quantity times the person-month), the working days of the window, the weekly hours, the implied FTE and
whether that is above the person's own limit (`--limit NAME=HOURS` or `--fraction NAME=0.5`) or above 1.0 (exit code 1), and it
echoes `--effort-source`. Three inputs are the caller's and none is assumed silently:

- **The length of a person-month** (`--hours-per-pm`) has no single value. Take it from the source (the hours the cost rates are
  worked out at, such as the 160 hours of the rate mix) and name that line in the finding. Without it a `pm` effort is a usage
  error. If the source states none, ask the sponsor and say the figure is assumed.
- **The full-time week** (`--week-hours`) defaults to 40 and the output says "full-time week assumed" until it is given.
- **The window** counts both end dates, Monday to Friday, less `--holiday` and the charter's breaks that have an end. "Joins
  after M2" and "leaves after M5" are read as the M2 and M5 dates themselves; say so in the finding if a day either way changes
  the answer. The output also prints person-months per calendar month (days over 30.4375, an approximation) as a cross-check.

Then ask the sponsor for the weekly limit, run with an assumed limit labelled as assumed, and list the missing limit as an open
question or a warning; never write the assumed limit as the charter's. The finding cites every line the effort rests on: each
charter sentence that states the person-months, the join and leave points, and the sheet that places the work.
