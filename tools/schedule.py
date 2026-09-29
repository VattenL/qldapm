"""Build form 2.18 Project Schedule, resource-levelled, from the scope baseline and the charter.

The schedule is derived, not typed. tools/level.py places every activity of the WBS dictionary in
docs/scope-package.en.md into its people's working hours; this script draws the result as the
printed form's Gantt chart (page 1, down to activities) and milestone chart (page 2), and adds the
resource histogram that shows the levelling holds. Change the source documents, then rerun; never
edit the generated form by hand.

Usage:
    uv run --with matplotlib tools/schedule.py [--prepared YYYY-MM-DD]

Outputs:
    docs/forms/2-18-project-schedule.en.md
    docs/assets/2-18-gantt-chart-<n>.png, one per Gantt page
    docs/assets/2-18-milestone-chart.png
    docs/assets/2-18-resource-histogram.png
"""

import argparse
import collections
import datetime
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from check_scope import MONTHS, cells, parse_dates, parse_sheets  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCOPE = ROOT / "docs" / "scope-package.en.md"
CHARTER = ROOT / "docs" / "charter-package.en.md"
FORM = ROOT / "docs" / "forms" / "2-18-project-schedule.en.md"
ASSETS = ROOT / "docs" / "assets"
MILESTONE_PNG = ASSETS / "2-18-milestone-chart.png"
HISTOGRAM_PNG = ASSETS / "2-18-resource-histogram.png"

SHORT_MONTH = {m[:3]: m for m in MONTHS}
CHARTER_DATE = re.compile(r"\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (\d{1,2}) ([A-Z][a-z]{2}) (\d{4})\b")
PEOPLE = ("PM", "DEV1", "DEV2", "DEV3", "QA1", "MOB1")
ROWS_PER_PAGE = 60
INCHES_PER_DAY = 0.06   # width of one calendar day on the timescale


def parse_outline(text):
    """Return (code, name, level) for every line of the Part 2 outline."""
    block = re.search(r"## Part 2: Work Breakdown Structure.*?```\n(.*?)```", text, re.S).group(1)
    rows = []
    for raw in block.splitlines():
        m = re.match(r"^\s*(\d+(?:\.\d+)*)\.?\s+(.+?)(?:\s{2,}(.*))?$", raw)
        if m:
            rows.append((m.group(1), m.group(2).strip(), m.group(1).count(".") + 1))
    return rows


def parse_due_dates(text):
    """Return {work package code: (start, finish)} from each dictionary sheet's Due Dates field."""
    out, code = {}, None
    for raw in text.splitlines():
        m = re.match(r"^#### (\d+(?:\.\d+)+) ", raw)
        if m:
            code = m.group(1)
        elif code and raw.startswith("| Due Dates |"):
            days = [d for _, _, d in parse_dates(cells(raw)[1])]
            out[code] = (min(days), max(days))
    return out


def parse_milestones(text):
    """Return [(id, name, date)] from the charter's summary milestone schedule table."""
    block = re.search(r"#### Summary milestone schedule\n(.*?)\n\n", text, re.S).group(1)
    out = []
    for raw in block.splitlines():
        row = cells(raw)
        if len(row) != 3 or not re.match(r"^M\d+$", row[0]):
            continue
        m = CHARTER_DATE.search(row[2])
        day = datetime.date(int(m.group(4)), MONTHS.index(SHORT_MONTH[m.group(3)]) + 1,
                            int(m.group(2)))
        out.append((row[0], row[1], day))
    return out


def fmt(day):
    return "%s %d %s %d" % (day.strftime("%a"), day.day, MONTHS[day.month - 1], day.year)


def short_date(day):
    return "%s %d %s %d" % (day.strftime("%a"), day.day, MONTHS[day.month - 1][:3], day.year)


def hours(h):
    return ("%.1f" % h).rstrip("0").rstrip(".")


def short_name(name):
    return name.split(";")[0]


def duration(start, finish, milestone=False):
    import level
    n = 0 if milestone else len(level.working_days(start, finish))
    return "%d day%s" % (n, "" if n == 1 else "s")


def build_items(scope, milestones, result, forecast):
    """Page 1 rows: the milestones at their forecast, then the WBS down to activities."""
    owners = {s["code"]: s["owner"] for s in parse_sheets(scope)}
    items = [dict(kind="milestone", code="", name="%s %s" % (mid, short_name(name)), level=1,
                  start=forecast[mid], finish=forecast[mid], resource="",
                  label="%s %s" % (mid, short_name(name)))
             for mid, name, _ in milestones]
    for code, name, level in parse_outline(scope):
        if code in result:
            r = result[code]
            people = [owners[code]] + sorted({x["res"] for x in r["parts"]} - {owners[code]})
            items.append(dict(kind="summary", code=code, name=name, level=level, start=r["start"],
                              finish=r["finish"], resource=", ".join(people), label=name))
            by_id = collections.OrderedDict()
            for x in r["parts"]:
                by_id.setdefault(x["id"], []).append(x)
            for aid, parts in by_id.items():
                split = len(parts) > 1
                who = ", ".join("%s %s h" % (x["res"], hours(x["hours"])) if split else x["res"]
                                for x in parts)
                items.append(dict(kind="activity", code=aid, name=parts[0]["name"],
                                  level=level + 1, start=min(x["start"] for x in parts),
                                  finish=max(x["finish"] for x in parts), resource=who,
                                  label=", ".join(x["res"] for x in parts)))
        else:
            below = [result[c] for c in result if c.startswith(code + ".")]
            items.append(dict(kind="summary", code=code, name=name, level=level,
                              start=min(b["start"] for b in below),
                              finish=max(b["finish"] for b in below), resource="", label=name))
    return items


def pages_of(items):
    """Split the Gantt rows into pages, breaking only before a major deliverable."""
    pages, current = [], []
    for item in items:
        if item["kind"] == "summary" and item["level"] == 2 and len(current) > 0:
            block_len = next((j for j, other in enumerate(items[items.index(item) + 1:])
                              if other["kind"] == "summary" and other["level"] <= 2),
                             len(items) - items.index(item) - 1) + 1
            if len(current) + block_len > ROWS_PER_PAGE:
                pages.append(current)
                current = []
        current.append(item)
    pages.append(current)
    return pages


def draw_sheet(items, columns, title, path, x_range, gates=(), baseline=None):
    """A scheduling-tool view: a task grid on the left, the timescale and bars on the right.

    items: dicts with kind (summary, activity, milestone), level, start, finish, label.
    columns: (header, width in inches, align, function of (index, item) returning the cell text).
    baseline: optional {row index: date} drawn as a hollow diamond, the charter date.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon, Rectangle

    ink, muted, rule, head = "#1f1f1f", "#5a5a5a", "#d4d4d4", "#ececec"
    bar, summary, diamond, gate = "#8db4e2", "#3c3c3c", "#1f1f1f", "#b0b0b0"
    row_h, head_rows, fs = 0.24, 2, 7.5
    one = datetime.timedelta(days=1)

    first, last = x_range
    chart_w = max(8.0, (last - first).days * INCHES_PER_DAY)
    table_w = sum(c[1] for c in columns)
    n = len(items)
    height = (n + head_rows) * row_h + 0.6
    W = table_w + chart_w + 0.4
    fig = plt.figure(figsize=(W, height), dpi=130)
    fig.patch.set_facecolor("white")

    def axes(x0, w):
        ax = fig.add_axes([x0 / W, 0.2 / height, w / W, (height - 0.6) / height])
        ax.set_ylim(n - 0.5, -head_rows - 0.5)
        for side in ax.spines.values():
            side.set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        return ax

    fig.text(0.5, 1 - 0.28 / height, title, ha="center", va="center", fontsize=13, color=ink)

    grid = axes(0.2, table_w)
    grid.set_xlim(0, table_w)
    grid.add_patch(Rectangle((0, -head_rows - 0.5), table_w, head_rows, color=head, zorder=0))
    x = 0.0
    for header, width, align, cell in columns:
        grid.text(x + 0.06, -head_rows / 2 - 0.5, header, va="center", fontsize=fs, color=ink,
                  weight="bold")
        for i, item in enumerate(items):
            text = cell(i, item)
            weight = "bold" if item["kind"] == "summary" else "normal"
            if header == "Task Name":
                text = "   " * (item["level"] - 1) + text
            tx = x + width - 0.06 if align == "right" else x + 0.06
            grid.text(tx, i, text, va="center", ha=align, fontsize=fs, color=ink, weight=weight)
        grid.plot([x, x], [-head_rows - 0.5, n - 0.5], color=rule, linewidth=0.6)
        x += width
    grid.plot([x, x], [-head_rows - 0.5, n - 0.5], color=muted, linewidth=0.9)
    for i in range(-head_rows, n + 1):
        grid.plot([0, table_w], [i - 0.5, i - 0.5], color=rule, linewidth=0.5)

    chart = axes(0.2 + table_w, chart_w)
    x0, x1 = mdates.date2num(first), mdates.date2num(last)
    chart.set_xlim(x0, x1)
    chart.add_patch(Rectangle((x0, -head_rows - 0.5), x1 - x0, head_rows, color=head, zorder=0))
    chart.plot([x0, x1], [-1.5, -1.5], color=rule, linewidth=0.6)
    chart.plot([x0, x1], [-0.5, -0.5], color=muted, linewidth=0.9)
    week = first
    while week <= last:
        wx = mdates.date2num(week)
        chart.plot([wx, wx], [-1.5, n - 0.5], color=rule, linewidth=0.5, linestyle=(0, (1, 2)),
                   zorder=0)
        chart.text(wx + 0.4, -1.0, "%d/%d" % (week.day, week.month), va="center", fontsize=6.5,
                   color=muted)
        week += datetime.timedelta(days=7)
    month = first.replace(day=1)
    while month <= last:
        mx = max(mdates.date2num(month), x0)
        chart.plot([mx, mx], [-2.5, -1.5], color=rule, linewidth=0.6)
        if x1 - mx > 14:
            chart.text(mx + 0.5, -2.0, "%s %d" % (MONTHS[month.month - 1], month.year),
                       va="center", fontsize=7, color=ink)
        month = (month + datetime.timedelta(days=32)).replace(day=1)
    for day in gates:
        gx = mdates.date2num(day) + 0.5
        chart.plot([gx, gx], [-0.5, n - 0.5], color=gate, linewidth=0.8, zorder=0)

    def side_label(right, left, i, text, size, weight):
        """Label right of a mark; left of it when that would run past the timescale; inside
        the bar's end, on a white backing, when neither side has room."""
        per_char = 0.0085 if weight == "bold" else 0.0075
        width_days = len(text) * size * per_char / INCHES_PER_DAY
        if right + width_days < x1:
            chart.text(right, i, text, va="center", ha="left", fontsize=size, color=ink,
                       weight=weight)
        elif left - width_days > x0:
            chart.text(left, i, text, va="center", ha="right", fontsize=size, color=ink,
                       weight=weight)
        else:
            chart.text(right - 3.0, i, text, va="center",
                       ha="right", fontsize=size, color=ink, weight=weight, zorder=4,
                       bbox=dict(facecolor="white", edgecolor="none", pad=0.6))

    def diamond_at(m, i, filled):
        chart.add_patch(Polygon([(m - 1.3, i), (m, i - 0.3), (m + 1.3, i), (m, i + 0.3)],
                                facecolor=diamond if filled else "white", edgecolor=diamond,
                                linewidth=1.0, zorder=3))

    for i, item in enumerate(items):
        s = mdates.date2num(item["start"])
        e = mdates.date2num(item["finish"] + one)
        if item["kind"] == "milestone":
            m = s + 0.5
            if baseline and i in baseline:
                b = mdates.date2num(baseline[i]) + 0.5
                if b != m:
                    chart.plot([b, m], [i, i], color=gate, linewidth=0.8, zorder=2)
                diamond_at(b, i, False)
            diamond_at(m, i, True)
            side_label(m + 2.0, m - 2.0, i, item["label"], fs, "bold")
        elif item["kind"] == "summary":
            chart.add_patch(Rectangle((s, i - 0.22), e - s, 0.14, color=summary, zorder=3))
            for ex in (s, e):
                chart.plot([ex, ex], [i - 0.22, i + 0.12], color=summary, linewidth=1.2, zorder=3)
            side_label(e + 1.2, s - 1.2, i, item["label"], fs, "bold")
        else:
            chart.add_patch(Rectangle((s, i - 0.25), e - s, 0.5, color=bar, zorder=3))
            side_label(e + 1.0, s - 1.0, i, item["label"], fs - 0.5, "normal")

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


def month_end(day):
    """The timescale stops at the end of the month the last bar ends in."""
    return (day.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)


def x_range_of(items):
    first = min(i["start"] for i in items)
    first -= datetime.timedelta(days=first.weekday() + 7)
    return first, month_end(max(i["finish"] for i in items))


def draw_gantt(pages, forecast, x_range):
    paths = []
    number = 0
    for page_no, page in enumerate(pages, 1):
        columns = [
            ("ID", 0.4, "right", lambda i, it, base=number: str(base + i + 1)),
            ("WBS", 0.95, "left", lambda i, it: it["code"]),
            ("Task Name", 4.9, "left", lambda i, it: it["name"]),
            ("Duration", 0.8, "left",
             lambda i, it: duration(it["start"], it["finish"], it["kind"] == "milestone")),
            ("Start", 1.3, "left", lambda i, it: short_date(it["start"])),
            ("Finish", 1.3, "left", lambda i, it: short_date(it["finish"])),
        ]
        path = ASSETS / ("2-18-gantt-chart-%d.png" % page_no)
        title = "Gantt Chart, part %d of %d" % (page_no, len(pages))
        draw_sheet(page, columns, title, path, x_range, gates=list(forecast.values()))
        paths.append(path)
        number += len(page)
    return paths


def draw_milestones(milestones, forecast, path):
    items = [dict(kind="milestone", level=1, start=forecast[mid], finish=forecast[mid],
                  name="%s %s" % (mid, short_name(name)),
                  label="%d/%d" % (forecast[mid].day, forecast[mid].month))
             for mid, name, _ in milestones]
    baseline = {i: day for i, (_, _, day) in enumerate(milestones)}
    columns = [
        ("ID", 0.4, "right", lambda i, it: str(i + 1)),
        ("Task Name", 5.4, "left", lambda i, it: it["name"]),
        ("Charter", 1.3, "left", lambda i, it: short_date(baseline[i])),
        ("Finish", 1.3, "left", lambda i, it: short_date(it["finish"])),
    ]
    first = min(list(baseline.values()) + [i["start"] for i in items])
    x_range = (first - datetime.timedelta(days=first.weekday() + 7),
               month_end(max(i["finish"] for i in items)))
    draw_sheet(items, columns, "Milestone Chart: hollow diamond at the charter date, filled at "
               "the levelled forecast", path, x_range, baseline=baseline)


def draw_histogram(load, cap, path):
    """Weekly booked hours per person as small multiples, with the weekly limit drawn."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    ink, muted, grid, bar = "#1f1f1f", "#5a5a5a", "#e4e3de", "#2a78d6"
    weeks = sorted({w for _, w in load})
    fig, axes = plt.subplots(len(PEOPLE), 1, figsize=(14, 1.35 * len(PEOPLE) + 0.9), dpi=130,
                             sharex=True)
    for ax, person in zip(axes, PEOPLE):
        values = [load.get((person, w), 0.0) for w in weeks]
        ax.bar([mdates.date2num(w) + 2.5 for w in weeks], values, width=5, color=bar,
               edgecolor="white", linewidth=0.8)
        ax.axhline(cap, color=ink, linewidth=0.9, linestyle=(0, (4, 3)))
        ax.set_ylim(0, cap * 1.25)
        ax.set_yticks([0, 20, cap])
        ax.tick_params(axis="y", labelsize=7, colors=muted)
        ax.grid(axis="y", color=grid, linewidth=0.6)
        ax.set_axisbelow(True)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(grid)
        peak = max(values)
        ax.text(0.0, 1.02, "%s  peak %s h, total %s h" % (person, hours(peak), hours(sum(values))),
                transform=ax.transAxes, fontsize=8, color=ink, weight="bold", va="bottom")
    axes[-1].xaxis.set_major_locator(mdates.MonthLocator())
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    axes[-1].tick_params(axis="x", labelsize=8, colors=muted)
    fig.suptitle("Resource histogram: booked hours per week after levelling, dashed line at %d h"
                 % cap, fontsize=11, color=ink)
    fig.tight_layout()
    fig.savefig(path, facecolor="white")
    plt.close(fig)


def gantt_table(items):
    out = ["| ID | WBS | Task Name | Duration | Start | Finish | Resource Name |",
           "| --- | --- | --- | --- | --- | --- | --- |"]
    for i, r in enumerate(items, 1):
        bold = "**%s**" if r["kind"] == "summary" else "%s"
        out.append("| %d | %s | %s | %s | <mark>%s</mark> | <mark>%s</mark> | %s |"
                   % (i, bold % r["code"] if r["code"] else "", bold % r["name"],
                      duration(r["start"], r["finish"], r["kind"] == "milestone"),
                      fmt(r["start"]), fmt(r["finish"]), r["resource"]))
    return "\n".join(out)


def milestone_table(milestones, forecast):
    out = ["| ID | Indicator | Task Name | Finish |", "| --- | --- | --- | --- |"]
    for i, (mid, name, day) in enumerate(milestones, 1):
        note = "Fixed date" if forecast[mid] == day else "Charter date %s" % fmt(day)
        out.append("| %d | %s | %s %s | <mark>%s</mark> |" % (i, note, mid, name, fmt(forecast[mid])))
    return "\n".join(out)


def loading_table(load, cap):
    out = ["| Resource | Booked hours | Weeks booked | Peak week | Peak hours |",
           "| --- | ---: | ---: | --- | ---: |"]
    for person in PEOPLE:
        weeks = {w: h for (p, w), h in load.items() if p == person and h > 1e-9}
        peak = max(weeks.items(), key=lambda kv: kv[1])
        out.append("| %s | %s | %d | %s | %s |" % (person, hours(sum(weeks.values())), len(weeks),
                                                  fmt(peak[0]), hours(peak[1])))
    return "\n".join(out)


def mermaid_gantt(items):
    out = ["```mermaid", "gantt", "    title Gantt Chart, work packages", "    dateFormat YYYY-MM-DD",
           "    axisFormat %d %b", "    excludes weekends"]
    for r in items:
        if r["kind"] == "summary" and r["level"] == 2:
            out.append("    section %s %s" % (r["code"], r["name"]))
        elif r["kind"] == "summary" and r["level"] == 4:
            end = r["finish"] + datetime.timedelta(days=1)
            out.append("    %s %s :%s, %s" % (r["code"], r["name"].replace(":", ""), r["start"], end))
    out.append("    section Milestones")
    for r in items:
        if r["kind"] == "milestone":
            out.append("    %s :milestone, %s, 0d" % (r["name"].split()[0], r["start"]))
    out.append("```")
    return "\n".join(out)


def render(items, pages, paths, milestones, forecast, load, prepared, divided):
    import level
    first, last = forecast[milestones[0][0]], forecast[milestones[-1][0]]
    go_live = milestones[-2][0]
    gantt_pages = []
    start = 0
    for page_no, (page, path) in enumerate(zip(pages, paths), 1):
        gantt_pages.append("![Gantt chart, part %d of %d](../assets/%s)"
                           % (page_no, len(pages), path.name))
        start += len(page)
    gantt_images = "\n\n".join(gantt_pages)
    return f"""# 2.18 Project Schedule

**Project:** Development and Deployment of a Learning Center Management Software
**Date prepared:** {prepared.day} {MONTHS[prepared.month - 1]} {prepared.year}
**Source:** A Project Manager's Book of Forms, 3rd edition, form 2.18, pages 78 to 81

*Reading convention. This schedule is the output of PMBOK 6 section 6.5 Develop Schedule. It is
resource-levelled (6.5.2.3): every activity of the WBS dictionary in `scope-package.en.md` keeps the
hours its sheet gives it, and is placed day by day into its people's working time, at most
{level.HOURS_PER_DAY} hours a working day, weekends and New Year's Day excluded. Where an activity finishes earlier
when divided, a second person takes up to half of it: developers help each other and QA1, DEV3
helps MOB1, and QA1 or DEV3 help the project manager with requirements work, as the charter's
response to risk R9 already provides; {divided} activities are divided, and their rows name both
people with their hours. Governance and acceptance packages are never divided. Work may start up to
{level.FAST_TRACK_DAYS} working days before the gate that releases it, which is fast tracking (6.5.2.6). Page 1 is the Gantt
chart in {len(pages)} parts: the milestones at their levelled forecast as 0-day rows, then the WBS, each work
package with its activities below it; Duration counts working days. Page 2 is the milestone chart,
each milestone at its levelled forecast beside its charter date. <mark>Highlighted</mark> dates are
the levelled forecast. The forecast moves {go_live} and M7 past the dates the charter imposes, so
the milestones are not baselined until the sponsor decides change request `3-3-change-request.en.md`;
until then the charter and the dictionary keep their dates. The Lunar New Year break of 2027 is not
in the calendar, because the charter dates its first day but not its length (assumption 8), and
the forecast crosses it. Dependency arrows are not drawn: the order kept is each package's gate and,
inside a control account, the order the dictionary dates give, since the activity list (2.12) and
the network diagram (2.15) have not been produced. The form is generated by `tools/schedule.py`;
change the source documents and rerun it rather than editing this file. The levelled project runs
from {fmt(first)} to {fmt(last)}.*

#### PROJECT SCHEDULE, page 1 of 2

{gantt_images}

{gantt_table(items)}

{mermaid_gantt(items)}

#### PROJECT SCHEDULE, page 2 of 2

![Milestone chart of M0 to M7, charter date and levelled forecast](../assets/{MILESTONE_PNG.name})

{milestone_table(milestones, forecast)}

---

### Resource loading after levelling

This check is not part of the printed form. It is the evidence that the levelling holds: booked
hours per person and week, from the day-by-day placement, never above
{level.HOURS_PER_DAY * 5} hours in a week.

![Resource histogram, booked hours per person and week](../assets/{HISTOGRAM_PNG.name})

{loading_table(load, level.HOURS_PER_DAY * 5)}
"""


def main(argv=None):
    import level
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--prepared", help="date prepared, YYYY-MM-DD, default today")
    args = ap.parse_args(argv)

    scope = SCOPE.read_text(encoding="utf-8")
    milestones = parse_milestones(CHARTER.read_text(encoding="utf-8"))
    packages, gates, result, forecast, cal = level.run()
    over = [(p, d) for p in cal.free for d in cal.days if cal.free[p][d] < -1e-6]
    if over:
        raise SystemExit("levelling left %d over-booked days" % len(over))
    load = level.weekly_load(result)
    divided = sum(1 for r in result.values()
                  for a in {x["id"] for x in r["parts"]}
                  if len([x for x in r["parts"] if x["id"] == a]) > 1)

    prepared = (datetime.date.fromisoformat(args.prepared) if args.prepared
                else datetime.date.today())
    items = build_items(scope, milestones, result, forecast)
    pages = pages_of(items)
    for old in ASSETS.glob("2-18-gantt-chart*.png"):
        old.unlink()
    paths = draw_gantt(pages, forecast, x_range_of(items))
    draw_milestones(milestones, forecast, MILESTONE_PNG)
    draw_histogram(load, level.HOURS_PER_DAY * 5, HISTOGRAM_PNG)
    FORM.parent.mkdir(parents=True, exist_ok=True)
    FORM.write_text(render(items, pages, paths, milestones, forecast, load, prepared, divided),
                    encoding="utf-8")
    print("wrote %s, %d Gantt pages, milestone chart, resource histogram"
          % (FORM.relative_to(ROOT), len(paths)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
