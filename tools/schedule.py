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


def gantt_table(rows):
    out = ["| ID | WBS | Task Name | Start | Finish | Resource Name |",
           "| --- | --- | --- | --- | --- | --- |"]
    for i, r in enumerate(rows, 1):
        name = "**%s**" % r["name"] if r["summary"] else r["name"]
        wbs = "**%s**" % r["code"] if r["summary"] else r["code"]
        out.append("| %d | %s | %s | <mark>%s</mark> | <mark>%s</mark> | %s |"
                   % (i, wbs, name, fmt(r["start"]), fmt(r["finish"]), r["resource"]))
    return "\n".join(out)


def milestone_table(milestones):
    out = ["| ID | Indicator | Task Name | Finish |", "| --- | --- | --- | --- |"]
    for i, (mid, name, day) in enumerate(milestones, 1):
        out.append("| %d | Fixed date | %s %s | <mark>%s</mark> |" % (i, mid, name, fmt(day)))
    return "\n".join(out)


def draw_gantt(rows, milestones, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    ink, muted, grid = "#0b0b0b", "#52514e", "#e4e3de"
    bar, summary = "#2a78d6", "#3a3935"
    one = datetime.timedelta(days=1)
    start = min(r["start"] for r in rows) - datetime.timedelta(days=3)
    finish = max(r["finish"] for r in rows) + datetime.timedelta(days=14)

    fig, ax = plt.subplots(figsize=(16, 0.19 * len(rows) + 1.6), dpi=150)
    for i, r in enumerate(rows):
        x0, width = mdates.date2num(r["start"]), (r["finish"] - r["start"] + one).days
        if r["summary"]:
            ax.barh(i, width, left=x0, height=0.28, color=summary)
            for x in (x0, x0 + width):
                ax.plot([x], [i + 0.08], marker="v", color=summary, markersize=4)
        else:
            ax.barh(i, width, left=x0, height=0.56, color=bar, edgecolor="white", linewidth=0.5)
            ax.text(x0 + width + 0.6, i, r["resource"], va="center", fontsize=6, color=muted)
    for mid, _, day in milestones:
        x = mdates.date2num(day) + 0.5
        ax.axvline(x, color=muted, linewidth=0.8, linestyle=(0, (3, 3)), zorder=0)
        ax.text(x, -1.3, mid, ha="center", va="bottom", fontsize=7, color=ink, weight="bold")

    labels = ["%s%s  %s" % ("   " * (r["level"] - 1), r["code"], r["name"]) for r in rows]
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(labels, fontsize=6.5, color=ink)
    for tick, r in zip(ax.get_yticklabels(), rows):
        if r["summary"]:
            tick.set_fontweight("bold")
    ax.set_ylim(len(rows) - 0.4, -1.8)
    ax.set_xlim(mdates.date2num(start), mdates.date2num(finish))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.xaxis.tick_top()
    ax.tick_params(axis="x", labelsize=6.5, colors=muted, rotation=90)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=grid, linewidth=0.5)
    ax.set_axisbelow(True)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.set_title("Gantt Chart", fontsize=12, color=ink, pad=34)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="white")
    plt.close(fig)


def draw_milestones(milestones, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    ink, muted, grid, mark = "#0b0b0b", "#52514e", "#e4e3de", "#3a3935"
    fig, ax = plt.subplots(figsize=(12, 0.42 * len(milestones) + 1.4), dpi=150)
    for i, (mid, name, day) in enumerate(milestones):
        x = mdates.date2num(day)
        ax.plot([x], [i], marker="D", markersize=8, color=mark)
        ax.text(x + 2, i, "%d/%d" % (day.day, day.month), va="center", fontsize=8, color=muted)
    ax.set_yticks(range(len(milestones)))
    ax.set_yticklabels(["%s  %s" % (mid, name.split(";")[0])
                        for mid, name, _ in milestones], fontsize=8, color=ink)
    ax.set_ylim(len(milestones) - 0.5, -0.7)
    days = [d for _, _, d in milestones]
    ax.set_xlim(mdates.date2num(min(days)) - 7, mdates.date2num(max(days)) + 14)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.tick_top()
    ax.tick_params(axis="x", labelsize=8, colors=muted)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=grid, linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.set_title("Milestone Chart", fontsize=12, color=ink, pad=24)
    fig.tight_layout()
    fig.savefig(path, facecolor="white")
    plt.close(fig)


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
accounts run from the earliest start to the latest finish below them. Page 2 carries the charter's
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

{gantt_table(rows)}

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
