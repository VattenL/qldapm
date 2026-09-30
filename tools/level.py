"""Resource-level the schedule at activity level, PMBOK 6 section 6.5 Develop Schedule.

The techniques are the book's: resource leveling (6.5.2.3), with activities divided between two
people where that finishes them earlier, and fast tracking (6.5.2.6), which lets work start a few days before the gate that
releases it. No estimate is changed: every activity keeps the hours its WBS dictionary sheet gives
it, and only its dates and who helps with it change.

Calendar:
    At most HOURS_PER_DAY on a working day, weekends and HOLIDAYS excluded. The Lunar New Year break
    of 2027 is not in HOLIDAYS: the charter dates its first day (assumption 8) but not its length,
    so the report flags any forecast that reaches it.

Gates:
    M0 is fixed. Every later gate falls on the day the last work due at it finishes, so leveling
    may move it; that is the forecast the change request puts to the sponsor. M7 is M6 plus the
    charter's full warranty month, or later if closeout work runs past it.

Kept from the current dictionary dates, as relations rather than dates:
    the gate a package may start after, the gate it must finish by, and, inside one control
    account, the order of two packages when one finished before the other started. An acceptance
    package is placed last and finishes with the last work due at its gate.

Level of effort:
    1.1.1.2 and 1.1.1.3 run from M0 to M7 and are spread evenly over every working day. Warranty
    support, 1.10.1.1, is spread evenly over the warranty month and     keeps its estimated hours.

Usage:
    python3 tools/level.py           print the gates, the loading check, and the divided activities
"""

import collections
import datetime
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import schedule as S  # noqa: E402
from check_scope import cells, money  # noqa: E402

HOURS_PER_DAY = 8
HOLIDAYS = {datetime.date(2027, 1, 1)}   # New Year's Day, a statutory public holiday in Viet Nam
FAST_TRACK_DAYS = 5   # working days a package may start before the gate that releases it
HELPER_SHARE = 0.5    # the most of one activity a helper may take
DEVELOPERS = ("DEV1", "DEV2", "DEV3")
RATES = {"PM": 162500, "DEV1": 118750, "DEV2": 118750, "DEV3": 118750, "QA1": 93750,
         "MOB1": 122500}   # the charter's rate mix per hour, as the scope package states it
WARRANTY = "1.10.1.1"
WARRANTY_DAYS = 31    # charter: the first warranty month runs its full 31 days before closeout
HORIZON = 240         # calendar days past the charter's M7 the model may run into
ONE = datetime.timedelta(days=1)


def working(day):
    return day.weekday() < 5 and day not in HOLIDAYS


def next_working(day):
    day += ONE
    while not working(day):
        day += ONE
    return day


def previous_working(day):
    day -= ONE
    while not working(day):
        day -= ONE
    return day


def on_or_after(day):
    while not working(day):
        day += ONE
    return day


def working_days(start, finish):
    days, d = [], start
    while d <= finish:
        if working(d):
            days.append(d)
        d += ONE
    return days


def parse_activities(scope):
    """{work package code: [(activity id, activity name, resource, hours)]} for labour rows."""
    out, code = collections.OrderedDict(), None
    for raw in scope.splitlines():
        m = re.match(r"^#### (\d+(?:\.\d+)+) ", raw)
        if m:
            code = m.group(1)
            out[code] = []
            continue
        if code and re.match(r"^\| %s-A\d+ \|" % re.escape(code), raw):
            row = cells(raw)
            if row[2]:
                out[code].append((row[0], row[1], row[2], money(row[3])))
    return out


def load_model(scope, charter):
    """Packages with their activities and their gate relations, and the charter gates."""
    dates = S.parse_due_dates(scope)
    acts = parse_activities(scope)
    gates = collections.OrderedDict((m, d) for m, _, d in S.parse_milestones(charter))
    names = list(gates)
    owned, code = {}, None
    for raw in scope.splitlines():
        m = re.match(r"^#### (\d+(?:\.\d+)+) ", raw)
        if m:
            code = m.group(1)
        elif code and raw.startswith("| Due Dates |"):
            for gate in re.findall(r"\b(M\d) on ", cells(raw)[1]):
                owned.setdefault(code, []).append(gate)
    first, last = gates[names[0]], gates[names[-1]]
    packages = collections.OrderedDict()
    for code, (start, finish) in dates.items():
        kickoff = names[0] in owned.get(code, [])
        owns = [g for g in owned.get(code, []) if g != names[0]]
        due = min(i for i, g in enumerate(names) if gates[g] >= finish)
        release = max([i for i, g in enumerate(names)
                       if gates[g] < start or (gates[g] == start and not owns)] or [0])
        # A package dated on the gate day it is due at (the accountant's sign-off on go-live day)
        # belongs to the window that gate closes.
        release = min(release, max(due - 1, 0))
        busiest = collections.Counter()
        for _, _, res, hours in acts[code]:
            busiest[res] += hours
        packages[code] = dict(
            code=code, start=start, finish=finish, release=release, due=due, owns=owns,
            kickoff=kickoff,
            loe=(start == first and finish == last),
            span=-(-max(busiest.values(), default=0) // HOURS_PER_DAY),
            acts=[dict(id=i, name=n, res=r, hours=h) for i, n, r, h in acts[code]])
    return packages, gates


def predecessors(packages):
    """Inside one control account and one gate window, the order the current dates give."""
    pred = {c: set() for c in packages}
    for a in packages.values():
        for b in packages.values():
            if a is b or a["loe"] or b["loe"] or WARRANTY in (a["code"], b["code"]):
                continue
            if (a["release"], a["due"]) != (b["release"], b["due"]):
                continue
            if a["code"].rsplit(".", 1)[0] != b["code"].rsplit(".", 1)[0]:
                continue
            if a["finish"] < b["start"]:
                pred[b["code"]].add(a["code"])
    return pred


def helpers(package, person):
    """Who may take part of an activity when that finishes it earlier.

    Developers help each other. A developer may help with QA1's test work, and DEV3, who built the
    cross-platform proof, with MOB1's mobile work. QA1 and DEV3 may help the project manager with
    requirements and analysis work: the charter's response to risk R9 already makes QA1 the second
    reader of the requirements, and DEV3 writes the nonfunctional requirements. Governance (1.1)
    and acceptance packages, where the owner signs, are never divided. Where a helper's rate
    differs from the owner's, the labour cost changes, and the change request carries it.
    """
    if package["owns"] or package["code"].startswith("1.1."):
        return []
    if person in DEVELOPERS:
        return [d for d in DEVELOPERS if d != person]
    return {"QA1": list(DEVELOPERS), "PM": ["QA1", "DEV3"], "MOB1": ["DEV3"]}.get(person, [])


class Calendar:
    def __init__(self, start, finish, people):
        self.days = working_days(start, finish)
        self.free = {p: {d: float(HOURS_PER_DAY) for d in self.days} for p in people}

    def spread(self, person, hours, start, finish):
        days = [d for d in self.days if start <= d <= finish]
        for d in days:
            self.free[person][d] -= hours / len(days)
        return {d: hours / len(days) for d in days}

    def place(self, people, hours, earliest, commit=True):
        """Fill free hours from the earliest day, the owner first each day.

        A helper takes at most HELPER_SHARE of the activity. Returns
        (start, finish, {person: hours}); with commit False nothing is booked.
        """
        limit = {p: hours if i == 0 else hours * HELPER_SHARE for i, p in enumerate(people)}
        left, first, last, share = hours, None, None, collections.Counter()
        self.last_booking = collections.defaultdict(dict)
        for d in self.days:
            if d < earliest:
                continue
            if left <= 1e-9:
                break
            for person in people:
                take = min(left, self.free[person][d], limit[person] - share[person])
                if take <= 1e-9:
                    continue
                if commit:
                    self.free[person][d] -= take
                    self.last_booking[person][d] = take
                left -= take
                share[person] += take
                first = first or d
                last = d
        if left > 1e-9:
            raise SystemExit("%s cannot place %.1f h inside the model horizon" % (people, left))
        return first, last, share


def level(packages, gates, project_end=None):
    """Level once, with level-of-effort work spread from M0 to project_end."""
    names = list(gates)
    start = gates[names[0]]
    project_end = project_end or gates[names[-1]]
    people = sorted({a["res"] for p in packages.values() for a in p["acts"]})
    cal = Calendar(start, gates[names[-1]] + datetime.timedelta(days=HORIZON), people)
    result = {}
    for p in packages.values():
        if p["loe"]:
            parts = []
            for a in p["acts"]:
                days = cal.spread(a["res"], a["hours"], start, project_end)
                parts.append(dict(id=a["id"], name=a["name"], owner=a["res"], res=a["res"],
                                  hours=a["hours"], start=start, finish=project_end, days=days))
            result[p["code"]] = dict(start=start, finish=project_end, parts=parts)
    pred = predecessors(packages)
    new_gate = {names[0]: start}
    todo = [p for p in packages.values() if not p["loe"] and p["code"] != WARRANTY]
    # Warranty support is booked when go-live is known; see below.
    # The package that holds M0 (kickoff) goes first; other governance work has float and
    # follows the work that sets a gate.
    todo.sort(key=lambda p: (not p["kickoff"], p["release"],
                             p["code"].startswith("1.1.") and not p["owns"],
                             bool(p["owns"]), p["due"], p["start"],
                             [int(x) for x in p["code"].split(".")]))

    def due_at(k):
        return [q for q in packages.values() if q["due"] == k and not q["loe"]
                and q["code"] != WARRANTY]

    while todo:
        placed = False
        for p in list(todo):
            gate = names[p["release"]]
            if gate not in new_gate or any(q not in result for q in pred[p["code"]]):
                continue
            k = p["due"]
            if p["owns"] and any(q["code"] not in result for q in due_at(k) if not q["owns"]):
                continue
            earliest = new_gate[gate] if p["release"] == 0 else next_working(new_gate[gate])
            if not p["owns"] and p["release"] > 0:
                for _ in range(FAST_TRACK_DAYS):
                    earliest = previous_working(earliest)
            earliest = max([earliest] + [next_working(result[q]["finish"]) for q in pred[p["code"]]])
            if p["owns"]:
                others = [result[q["code"]]["finish"] for q in due_at(k) if not q["owns"]]
                if others:
                    end = max(others)
                    for _ in range(p["span"] - 1):
                        end = previous_working(end)
                    earliest = max(earliest, end)
            parts = []
            for a in p["acts"]:
                options = [[a["res"]]] + [[a["res"], h] for h in helpers(p, a["res"])]
                best = min(options, key=lambda who: (cal.place(who, a["hours"], earliest,
                                                               commit=False)[1], len(who)))
                s, f, share = cal.place(best, a["hours"], earliest)
                for person in best:
                    if share[person] > 1e-9:
                        days = cal.last_booking[person]
                        parts.append(dict(id=a["id"], name=a["name"], owner=a["res"], res=person,
                                          hours=share[person], start=min(days), finish=max(days),
                                          days=dict(days)))
            result[p["code"]] = dict(start=min(x["start"] for x in parts),
                                     finish=max(x["finish"] for x in parts), parts=parts)
            todo.remove(p)
            placed = True
            for g in p["owns"]:
                if g not in new_gate and all(q["code"] in result for q in due_at(names.index(g))):
                    new_gate[g] = max(result[q["code"]]["finish"] for q in due_at(names.index(g)))
            go_live = names[-2]
            if go_live in new_gate and WARRANTY not in result:
                # The warranty month is booked as soon as go-live is known, before closeout work.
                w_start = next_working(new_gate[go_live])
                w_end = on_or_after(new_gate[go_live] + datetime.timedelta(days=WARRANTY_DAYS))
                parts = []
                for a in packages[WARRANTY]["acts"]:
                    days = cal.spread(a["res"], a["hours"], w_start, w_end)
                    parts.append(dict(id=a["id"], name=a["name"], owner=a["res"], res=a["res"],
                                      hours=a["hours"], start=w_start, finish=w_end, days=days))
                result[WARRANTY] = dict(start=w_start, finish=w_end, parts=parts)
            # A gate no package owns (closeout) closes when everything due at it is placed.
            for i, g in enumerate(names):
                if g not in new_gate and names[i - 1] in new_gate and due_at(i) and \
                        not any(q["owns"] for q in due_at(i)) and \
                        all(q["code"] in result for q in due_at(i)):
                    new_gate[g] = max(result[q["code"]]["finish"] for q in due_at(i))
        if not placed:
            raise SystemExit("no package can be placed; check the gate relations")

    # Closeout cannot come before the warranty month ends.
    new_gate[names[-1]] = max(new_gate.get(names[-1], result[WARRANTY]["finish"]),
                              result[WARRANTY]["finish"])
    return result, new_gate, cal


def weekly_load(result):
    """Booked hours by (person, Monday of the week), from the day-by-day bookings."""
    load = collections.defaultdict(float)
    for r in result.values():
        for x in r["parts"]:
            for d, h in x["days"].items():
                load[(x["res"], d - datetime.timedelta(days=d.weekday()))] += h
    return load


def run():
    scope = S.SCOPE.read_text(encoding="utf-8")
    charter = S.CHARTER.read_text(encoding="utf-8")
    packages, gates = load_model(scope, charter)
    end = None
    for _ in range(6):
        result, new_gate, cal = level(packages, gates, end)
        if new_gate[list(gates)[-1]] == end:
            break
        end = new_gate[list(gates)[-1]]
    else:
        raise SystemExit("the project end does not settle")
    return packages, gates, result, new_gate, cal


def main():
    packages, gates, result, new_gate, cal = run()
    print("Gate  charter                  levelled forecast")
    for g in gates:
        print("%-4s  %-24s %s" % (g, S.fmt(gates[g]), S.fmt(new_gate[g])))
    over = [(p, d, cal.free[p][d]) for p in cal.free for d in cal.days if cal.free[p][d] < -1e-6]
    print("Days any person is booked above %d hours: %d" % (HOURS_PER_DAY, len(over)))
    peak = max(weekly_load(result).items(), key=lambda kv: kv[1])
    print("Peak week: %s %.1f h in the week of %s" % (peak[0][0], peak[1], S.fmt(peak[0][1])))
    hours = collections.Counter()
    for r in result.values():
        for x in r["parts"]:
            hours[x["res"]] += x["hours"]
    print("Hours by person:", {k: round(v, 1) for k, v in sorted(hours.items())})
    divided = [(c, a) for c, r in result.items() for a in {x["id"] for x in r["parts"]}
               if len([x for x in r["parts"] if x["id"] == a]) > 1]
    print("Activities divided between two people: %d" % len(divided))
    return 0


if __name__ == "__main__":
    sys.exit(main())
