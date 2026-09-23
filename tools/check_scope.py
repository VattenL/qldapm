"""Consistency checks for docs/scope-package.en.md.

The scope package carries a 70-sheet WBS dictionary whose hours and money must roll up to the figures
the project charter already fixed. That arithmetic cannot be held by hand across 70 sheets, so it is
checked here instead. The Markdown is the source of truth; this script only reads it.

Usage:
    python tools/check_scope.py [path]

Exit code 0 when every check passes, 1 otherwise.
"""

import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT = ROOT / "docs" / "scope-package.en.md"

RATES = {"PM": 162500, "DEV1": 118750, "DEV2": 118750, "DEV3": 118750, "QA1": 93750, "MOB1": 122500}
ROLE = {"PM": "PM", "DEV1": "DEV", "DEV2": "DEV", "DEV3": "DEV", "QA1": "QA", "MOB1": "MOB"}

EXPECTED_HOURS = 4400
EXPECTED_ROLE_HOURS = {"PM": 800, "DEV": 2400, "QA": 800, "MOB": 400}
EXPECTED_LABOR = 539_000_000
EXPECTED_MATERIAL = 161_000_000
EXPECTED_TOTAL = 700_000_000
EXPECTED_PACKAGES = 70

CODE = re.compile(r"^\d+(?:\.\d+)*$")
NUM = re.compile(r"^[\d,]+$")


class Report:
    def __init__(self):
        self.failures = []

    def check(self, ok, message):
        if not ok:
            self.failures.append(message)
        return ok

    def done(self, checked):
        for line in self.failures:
            print("FAIL %s" % line)
        if self.failures:
            print("\n%d check(s) failed out of %d" % (len(self.failures), checked))
            return 1
        print("all %d checks passed" % checked)
        return 0


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def money(text):
    return int(text.replace(",", "").replace("*", "").strip() or 0)


def parse_outline(text):
    """Return the WBS codes of the Part 2 outline, with the control account flag."""
    block = re.search(r"## Part 2: Work Breakdown Structure.*?```\n(.*?)```", text, re.S)
    if not block:
        return {}
    out = collections.OrderedDict()
    for raw in block.group(1).splitlines():
        line = raw.strip()
        if not line:
            continue
        token = line.split()[0].rstrip(".")
        if not CODE.match(token):
            continue
        out[token] = "CA" in line.split()
    return out


def parse_sheets(text):
    """Return one record per WBS dictionary sheet."""
    sheets = []
    current = None
    in_acts = False
    for raw in text.splitlines():
        heading = re.match(r"^#### (\d+(?:\.\d+)+) (.+)$", raw)
        if heading:
            current = dict(code=heading.group(1), name=heading.group(2), acts=[], mats=[],
                           owner=None, stated=None)
            sheets.append(current)
            in_acts = False
            continue
        if current is None:
            continue
        if raw.startswith("| Responsible Person |"):
            current["owner"] = cells(raw)[1]
        elif raw.startswith("| ID | Activity | Resource |"):
            in_acts = True
        elif in_acts and raw.startswith("| | **Work package total**"):
            row = cells(raw)
            current["stated"] = (money(row[3]), money(row[5]), money(row[8]), money(row[9]))
            in_acts = False
        elif in_acts and raw.startswith("|") and not raw.startswith("| ---"):
            row = cells(raw)
            if len(row) < 10:
                continue
            res = row[2]
            if res:
                current["acts"].append((res, money(row[3]), money(row[4]), money(row[5])))
            elif row[6]:
                current["mats"].append((money(row[6]), money(row[7]), money(row[8])))
    return sheets


def parse_rtm_deliverables(text):
    block = re.search(r"### Requirement Information and Relationship Traceability\n(.*?)\n\n", text, re.S)
    if not block:
        return []
    found = []
    for raw in block.group(1).splitlines():
        if not raw.startswith("|") or raw.startswith("| ---") or raw.startswith("| ID |"):
            continue
        row = cells(raw)
        if len(row) < 7:
            continue
        found.extend((row[0], code) for code in re.findall(r"\d+(?:\.\d+){2,}", row[6]))
    return found


def main(argv):
    path = pathlib.Path(argv[1]) if len(argv) > 1 else DEFAULT
    text = path.read_text(encoding="utf-8")
    rep = Report()
    checked = 0

    # 1. Outline structure.
    outline = parse_outline(text)
    rep.check(outline, "Part 2 outline not found")
    packages = [c for c, is_ca in outline.items() if not is_ca and c.count(".") == 3]
    accounts = [c for c, is_ca in outline.items() if is_ca]
    checked += 1
    rep.check(len(packages) == EXPECTED_PACKAGES,
              "expected %d work packages in the outline, found %d" % (EXPECTED_PACKAGES, len(packages)))
    checked += 1
    rep.check(len(outline) == len(set(outline)), "duplicate code in the outline")
    checked += 1
    for code in outline:
        parent = code.rsplit(".", 1)[0]
        if "." in code:
            rep.check(parent in outline, "%s has no parent %s in the outline" % (code, parent))
    checked += 1
    for code in packages:
        parent = code.rsplit(".", 1)[0]
        rep.check(outline.get(parent) is True,
                  "work package %s does not roll up to a control account" % code)
    checked += 1

    # 2. One dictionary sheet per work package, and nothing else.
    sheets = parse_sheets(text)
    sheet_codes = [s["code"] for s in sheets]
    rep.check(len(sheet_codes) == len(set(sheet_codes)), "duplicate dictionary sheet")
    checked += 1
    rep.check(set(sheet_codes) == set(packages),
              "dictionary sheets and work packages differ: %s" %
              sorted(set(sheet_codes) ^ set(packages)))
    checked += 1

    # 3. Each sheet is internally consistent and each owner is a known resource.
    total_hours = 0
    total_labor = 0
    total_material = 0
    role_hours = collections.Counter()
    for s in sheets:
        hours = sum(a[1] for a in s["acts"])
        labor = sum(a[3] for a in s["acts"])
        material = sum(m[2] for m in s["mats"])
        for res, hrs, rate, line_total in s["acts"]:
            rep.check(res in RATES, "%s: unknown resource %s" % (s["code"], res))
            if res in RATES:
                rep.check(rate == RATES[res], "%s: %s rate %s is not the charter rate %s"
                          % (s["code"], res, rate, RATES[res]))
                rep.check(hrs * rate == line_total,
                          "%s: %s line does not multiply out" % (s["code"], res))
                role_hours[ROLE[res]] += hrs
        for units, unit_cost, line_total in s["mats"]:
            rep.check(units * unit_cost == line_total,
                      "%s: material line does not multiply out" % s["code"])
        rep.check(s["stated"] is not None, "%s: no work package total row" % s["code"])
        if s["stated"]:
            st_hours, st_labor, st_material, st_total = s["stated"]
            rep.check(st_hours == hours, "%s: total row says %s hours, rows give %s"
                      % (s["code"], st_hours, hours))
            rep.check(st_labor == labor, "%s: total row says %s labor, rows give %s"
                      % (s["code"], st_labor, labor))
            rep.check(st_material == material, "%s: total row says %s material, rows give %s"
                      % (s["code"], st_material, material))
            rep.check(st_total == labor + material, "%s: total row does not add up" % s["code"])
        rep.check(s["owner"] in RATES, "%s: owner %r is not a known resource" % (s["code"], s["owner"]))
        total_hours += hours
        total_labor += labor
        total_material += material
    checked += 6

    # 4. Roll-up to the charter figures.
    rep.check(total_hours == EXPECTED_HOURS,
              "labor hours total %s, charter basis is %s" % (total_hours, EXPECTED_HOURS))
    rep.check(dict(role_hours) == EXPECTED_ROLE_HOURS,
              "hours by role %s, expected %s" % (dict(role_hours), EXPECTED_ROLE_HOURS))
    rep.check(total_labor == EXPECTED_LABOR,
              "labor cost %s, charter budget line 1 is %s" % (total_labor, EXPECTED_LABOR))
    rep.check(total_material == EXPECTED_MATERIAL,
              "other cost %s, charter budget lines 2 to 6 are %s" % (total_material, EXPECTED_MATERIAL))
    rep.check(total_labor + total_material == EXPECTED_TOTAL,
              "grand total %s, charter budget is %s" % (total_labor + total_material, EXPECTED_TOTAL))
    checked += 5

    # 5. Every WBS code cited by the traceability matrix exists.
    for rid, code in parse_rtm_deliverables(text):
        rep.check(code in outline, "RTM row %s cites %s, which is not in the WBS" % (rid, code))
    checked += 1

    # 6. Identifier coverage against the charter.
    for family, count, width in (("F", 12, 2), ("A", 12, 2), ("D", 11, 0), ("M", 7, 0)):
        for n in range(0 if family == "M" else 1, count + 1):
            ident = "%s%0*d" % (family, width, n)
            rep.check(ident in text, "charter identifier %s is not referenced anywhere" % ident)
    for family, count in (("BR", 6), ("FR", 12), ("NFR", 12)):
        for n in range(1, count + 1):
            ident = "%s%02d" % (family, n)
            rep.check(ident in text, "requirement identifier %s is missing" % ident)
    checked += 2

    # 7. Project writing rules.
    rep.check("—" not in text, "em dash found; the project writing rules forbid it")
    emoji = re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", text)
    rep.check(not emoji, "emoji found: %s" % sorted(set(emoji)))
    checked += 2

    print("%s: %d work packages, %d control accounts, %d hours, %s VND"
          % (path.name, len(packages), len(accounts), total_hours,
             "{:,}".format(total_labor + total_material)))
    return rep.done(checked)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
