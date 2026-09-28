"""Build form 2.18 Project Schedule from the scope baseline and the charter.

The schedule is derived, not typed: every work package start, finish and resource comes from the
WBS dictionary in docs/scope-package.en.md, and every milestone date from the summary milestone
schedule in docs/charter-package.en.md. Change those documents, then rerun this script; never edit
the generated form by hand.

Usage:
    uv run --with matplotlib tools/schedule.py            write the form and the two charts
    uv run --with matplotlib tools/schedule.py --check    only print the loading report

Outputs:
    docs/forms/2-18-project-schedule.en.md
    docs/assets/2-18-gantt-chart.png
    docs/assets/2-18-milestone-chart.png
"""

import argparse
import collections
import datetime
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from check_scope import DATE, MONTHS, cells, parse_dates, parse_sheets  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCOPE = ROOT / "docs" / "scope-package.en.md"
CHARTER = ROOT / "docs" / "charter-package.en.md"
FORM = ROOT / "docs" / "forms" / "2-18-project-schedule.en.md"
GANTT_PNG = ROOT / "docs" / "assets" / "2-18-gantt-chart.png"
MILESTONE_PNG = ROOT / "docs" / "assets" / "2-18-milestone-chart.png"

SHORT_MONTH = {m[:3]: m for m in MONTHS}
CHARTER_DATE = re.compile(r"\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (\d{1,2}) ([A-Z][a-z]{2}) (\d{4})\b")
WORK_HOURS_PER_WEEK = 40


def parse_outline(text):
    """Return (code, name, level, is_control_account) for every line of the Part 2 outline."""
    block = re.search(r"## Part 2: Work Breakdown Structure.*?```\n(.*?)```", text, re.S).group(1)
    rows = []
    for raw in block.splitlines():
        m = re.match(r"^\s*(\d+(?:\.\d+)*)\.?\s+(.+?)(?:\s{2,}(.*))?$", raw)
        if not m:
            continue
        code, name, note = m.group(1), m.group(2).strip(), (m.group(3) or "").strip()
        rows.append((code, name, code.count(".") + 1, note == "CA"))
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


def workdays(start, finish):
    days, d = [], start
    while d <= finish:
        if d.weekday() < 5:
            days.append(d)
        d += datetime.timedelta(days=1)
    return days


def build_rows(scope):
    """One row per outline line, with summary dates rolled up from the work packages below."""
    outline = parse_outline(scope)
    dates = parse_due_dates(scope)
    sheets = {s["code"]: s for s in parse_sheets(scope)}
    rows = []
    for code, name, level, _ in outline:
        if code in sheets:
            s = sheets[code]
            others = sorted({a[0] for a in s["acts"]} - {s["owner"]})
            start, finish = dates[code]
            rows.append(dict(code=code, name=name, level=level, summary=False, start=start,
                             finish=finish, resource=", ".join([s["owner"]] + others),
                             sheet=s))
        else:
            below = [dates[c] for c in dates if c.startswith(code + ".")]
            rows.append(dict(code=code, name=name, level=level, summary=True,
                             start=min(b[0] for b in below), finish=max(b[1] for b in below),
                             resource="", sheet=None))
    missing = set(dates) - {r["code"] for r in rows}
    if missing:
        raise SystemExit("dictionary sheets not in the outline: %s" % sorted(missing))
    return rows


def loading(rows):
    """Spread each activity's hours evenly over its package's working days; sum by resource and week."""
    load = collections.defaultdict(float)
    for r in rows:
        if r["summary"]:
            continue
        days = workdays(r["start"], r["finish"])
        for res, hours, _, _ in r["sheet"]["acts"]:
            for d in days:
                load[(res, d - datetime.timedelta(days=d.weekday()))] += hours / len(days)
    return load


def loading_report(rows):
    load = loading(rows)
    over = sorted((week, res, h) for (res, week), h in load.items() if h > WORK_HOURS_PER_WEEK + 0.5)
    lines = ["Resource loading, hours spread evenly over each package's working days:"]
    for res in ("PM", "DEV1", "DEV2", "DEV3", "QA1", "MOB1"):
        weeks = {w: h for (r, w), h in load.items() if r == res}
        peak = max(weeks.items(), key=lambda kv: kv[1])
        lines.append("  %-4s %4d h over %2d weeks, peak %5.1f h in week of %s"
                     % (res, round(sum(weeks.values())), len(weeks), peak[1], fmt(peak[0])))
    lines.append("Weeks above %d h: %d" % (WORK_HOURS_PER_WEEK, len(over)))
    for week, res, h in over:
        lines.append("  %s  %-4s %5.1f h" % (fmt(week), res, h))
    return "\n".join(lines)


def mermaid_gantt(rows, milestones):
    out = ["```mermaid", "gantt", "    title Gantt Chart", "    dateFormat YYYY-MM-DD",
           "    axisFormat %d %b", "    excludes weekends"]
    for r in rows:
        if r["level"] == 2:
            out.append("    section %s %s" % (r["code"], r["name"]))
        elif not r["summary"]:
            end = r["finish"] + datetime.timedelta(days=1)
            out.append("    %s %s, %s :%s, %s" % (r["code"], r["name"].replace(":", ""),
                                                  r["resource"], r["start"], end))
    out.append("    section Milestones")
    for mid, name, day in milestones:
        out.append("    %s :milestone, %s, 0d" % (mid, day))
    out.append("```")
    return "\n".join(out)


def mermaid_milestones(milestones):
    out = ["```mermaid", "gantt", "    title Milestone Chart", "    dateFormat YYYY-MM-DD",
           "    axisFormat %b %Y"]
    for mid, name, day in milestones:
        out.append("    %s %s :milestone, %s, 0d" % (mid, name.split(";")[0], day))
    out.append("```")
    return "\n".join(out)


def duration(start, finish, milestone=False):
    n = 0 if milestone else len(workdays(start, finish))
    return "%d day%s" % (n, "" if n == 1 else "s")


def short_name(name):
    return name.split(";")[0]


def page1_rows(rows, milestones):
    """The Gantt view: the charter milestones as 0-day rows first, then the WBS."""
    out = [dict(kind="milestone", code="", name="%s %s" % (mid, short_name(name)), level=1,
                start=day, finish=day, label="%s %s" % (mid, short_name(name)))
           for mid, name, day in milestones]
    for r in rows:
        out.append(dict(kind="summary" if r["summary"] else "task", code=r["code"], name=r["name"],
                        level=r["level"], start=r["start"], finish=r["finish"],
                        label=r["name"] if r["summary"] else r["resource"]))
    return out


def gantt_table(rows, milestones):
    out = ["| ID | WBS | Task Name | Duration | Start | Finish | Resource Name |",
           "| --- | --- | --- | --- | --- | --- | --- |"]
    resource = {r["code"]: r["resource"] for r in rows}
    for i, r in enumerate(page1_rows(rows, milestones), 1):
        bold = "**%s**" if r["kind"] == "summary" else "%s"
        out.append("| %d | %s | %s | %s | <mark>%s</mark> | <mark>%s</mark> | %s |"
                   % (i, bold % r["code"] if r["code"] else "", bold % r["name"],
                      duration(r["start"], r["finish"], r["kind"] == "milestone"),
                      fmt(r["start"]), fmt(r["finish"]), resource.get(r["code"], "")))
    return "\n".join(out)


def milestone_table(milestones):
    out = ["| ID | Indicator | Task Name | Finish |", "| --- | --- | --- | --- |"]
    for i, (mid, name, day) in enumerate(milestones, 1):
        out.append("| %d | Fixed date | %s %s | <mark>%s</mark> |" % (i, mid, name, fmt(day)))
    return "\n".join(out)


def draw_sheet(items, columns, title, path, gates=()):
    """Draw a scheduling-tool style view: a task grid on the left, the timescale and bars on the right.

    items: dicts with kind (summary, task, milestone), level, start, finish, label.
    columns: (header, width in inches, align, function of (index, item) returning the cell text).
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

    first = min(i["start"] for i in items)
    first -= datetime.timedelta(days=first.weekday() + 7)
    last = max(i["finish"] for i in items) + datetime.timedelta(days=35)
    chart_w = max(10.0, (last - first).days * 0.085)
    table_w = sum(c[1] for c in columns)
    n = len(items)
    height = (n + head_rows) * row_h + 0.6
    fig = plt.figure(figsize=(table_w + chart_w + 0.4, height), dpi=130)
    fig.patch.set_facecolor("white")
    W, H = table_w + chart_w + 0.4, height

    def axes(x0, w):
        ax = fig.add_axes([x0 / W, 0.2 / H, w / W, (height - 0.6) / H])
        ax.set_ylim(n - 0.5, -head_rows - 0.5)
        for side in ax.spines.values():
            side.set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        return ax

    fig.text(0.5, 1 - 0.28 / H, title, ha="center", va="center", fontsize=13, color=ink)

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

    for i, item in enumerate(items):
        s = mdates.date2num(item["start"])
        e = mdates.date2num(item["finish"] + one)
        if item["kind"] == "milestone":
            m = s + 0.5
            chart.add_patch(Polygon([(m - 1.3, i), (m, i - 0.3), (m + 1.3, i), (m, i + 0.3)],
                                    color=diamond, zorder=3))
            # A label that would run past the timescale goes on the left of its diamond.
            fits = m + 2.0 + len(item["label"]) * 0.075 / 0.085 < x1
            chart.text(m + 2.0 if fits else m - 2.0, i, item["label"], va="center",
                       ha="left" if fits else "right", fontsize=fs, color=ink, weight="bold")
        elif item["kind"] == "summary":
            chart.add_patch(Rectangle((s, i - 0.22), e - s, 0.14, color=summary, zorder=3))
            for ex in (s, e):
                chart.plot([ex, ex], [i - 0.22, i + 0.12], color=summary, linewidth=1.2, zorder=3)
            chart.text(e + 1.2, i, item["label"], va="center", fontsize=fs, color=ink,
                       weight="bold")
        else:
            chart.add_patch(Rectangle((s, i - 0.25), e - s, 0.5, color=bar, zorder=3))
            chart.text(e + 1.0, i, item["label"], va="center", fontsize=fs - 0.5, color=ink)

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


def short_date(day):
    return "%s %d %s %d" % (day.strftime("%a"), day.day, MONTHS[day.month - 1][:3], day.year)


def draw_gantt(rows, milestones, path):
    items = page1_rows(rows, milestones)
    columns = [
        ("ID", 0.4, "right", lambda i, it: str(i + 1)),
        ("WBS", 0.7, "left", lambda i, it: it["code"]),
        ("Task Name", 4.9, "left", lambda i, it: it["name"]),
        ("Duration", 0.8, "left",
         lambda i, it: duration(it["start"], it["finish"], it["kind"] == "milestone")),
        ("Start", 1.3, "left", lambda i, it: short_date(it["start"])),
        ("Finish", 1.3, "left", lambda i, it: short_date(it["finish"])),
    ]
    draw_sheet(items, columns, "Gantt Chart", path, gates=[d for _, _, d in milestones])


def draw_milestones(milestones, path):
    items = [dict(kind="milestone", level=1, start=day, finish=day,
                  name="%s %s" % (mid, short_name(name)), label="%d/%d" % (day.day, day.month))
             for mid, name, day in milestones]
    columns = [
        ("ID", 0.4, "right", lambda i, it: str(i + 1)),
        ("Task Name", 4.6, "left", lambda i, it: it["name"]),
        ("Finish", 1.3, "left", lambda i, it: short_date(it["finish"])),
    ]
    draw_sheet(items, columns, "Milestone Chart", path)


def render(rows, milestones, prepared):
    first, last = rows[0]["start"], rows[0]["finish"]
    load = loading(rows)
    over = [(h, res, week) for (res, week), h in load.items() if h > WORK_HOURS_PER_WEEK + 0.5]
    worst_h, worst_res, worst_week = max(over) if over else (0, "", first)
    levelling = (
        "The dates are not yet resource-levelled: spreading each sheet's hours evenly over its "
        "package's working days puts a resource above %d hours in %d resource-weeks, the worst "
        "being %s at %d hours in the week of %s. Levelling may move package dates and, where a "
        "gate cannot hold the work, a milestone, which is a charter change for the sponsor."
        % (WORK_HOURS_PER_WEEK, len(over), worst_res, round(worst_h), fmt(worst_week))
        if over else "Spread evenly, no resource exceeds %d hours in any week." % WORK_HOURS_PER_WEEK)
    return f"""# 2.18 Project Schedule

**Project:** Development and Deployment of a Learning Center Management Software
**Date prepared:** {prepared.day} {MONTHS[prepared.month - 1]} {prepared.year}
**Source:** A Project Manager's Book of Forms, 3rd edition, form 2.18, pages 78 to 81

*Reading convention. This schedule is the output of PMBOK 6 section 6.5 Develop Schedule and is
built from the scope baseline: every row of page 1 is a line of the WBS in
`scope-package.en.md` Part 2, and every work package start and finish is the Due Dates field of its
WBS dictionary sheet in Part 3. Summary rows for the project, the major deliverables and the control
accounts run from the earliest start to the latest finish below them. Page 1 opens with the milestones as 0-day rows, and Duration counts working days, Monday to Friday, with no public holiday removed. Page 2 carries the charter's
summary milestones M0 to M7; its Indicator column is the printed chart's icon column, and every milestone reads Fixed date because the charter milestone dates are fixed and not renegotiated in planning (dictionary sheet 1.1.1.2). The Resource Name column is what the printed chart writes next to each
bar: the work package's Responsible Person first, then every other resource with hours on that
sheet. <mark>Highlighted</mark> dates are first-pass estimates that are re-baselined at M1, as the
dictionary and the charter state. Dependency arrows are not drawn: the activity list (2.12) and the
network diagram (2.15) that would supply them have not been produced, so the only sequencing shown is
the milestone gates, drawn as dashed lines M0 to M7. The form is generated by `tools/schedule.py`
from those two documents; change them and rerun the script rather than editing this file. The
project runs from {fmt(first)} to {fmt(last)}. {levelling}*

#### PROJECT SCHEDULE, page 1 of 2

![Gantt chart of the 78 work packages, with milestone gates M0 to M7](../assets/{GANTT_PNG.name})

{gantt_table(rows, milestones)}

{mermaid_gantt(rows, milestones)}

#### PROJECT SCHEDULE, page 2 of 2

![Milestone chart of M0 to M7](../assets/{MILESTONE_PNG.name})

{milestone_table(milestones)}

{mermaid_milestones(milestones)}
"""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--check", action="store_true", help="print the loading report only")
    ap.add_argument("--prepared", help="date prepared, YYYY-MM-DD, default today")
    args = ap.parse_args(argv)

    scope = SCOPE.read_text(encoding="utf-8")
    rows = build_rows(scope)
    milestones = parse_milestones(CHARTER.read_text(encoding="utf-8"))
    print(loading_report(rows))
    if args.check:
        return 0

    prepared = (datetime.date.fromisoformat(args.prepared) if args.prepared
                else datetime.date.today())
    draw_gantt(rows, milestones, GANTT_PNG)
    draw_milestones(milestones, MILESTONE_PNG)
    FORM.parent.mkdir(parents=True, exist_ok=True)
    FORM.write_text(render(rows, milestones, prepared), encoding="utf-8")
    print("wrote %s, %s, %s" % (FORM.relative_to(ROOT), GANTT_PNG.relative_to(ROOT),
                                MILESTONE_PNG.relative_to(ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
