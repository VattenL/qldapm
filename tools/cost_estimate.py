#!/usr/bin/env python3
"""Cost estimates, forms 2.20 and 2.21, and the scope change request, generated from the WBS dictionary.

The hours come from the activity tables of docs/scope-package.en.md, less the work the change request
defers and scaled where it makes work leaner; the calendar comes from tools/level.py, the levelling
that draws form 2.18, run on the same reduced work. The prices are the ones listed in REFS below,
each with the page it was read from on the date prepared. Everything the two forms print is computed
here, so a changed price, sheet, or scope decision is a rerun, not an edit:

    python tools/cost_estimate.py                 # writes docs/forms/2-20-cost-estimates.en.md
                                                  # and docs/forms/3-3-change-request-scope.en.md
    python tools/cost_estimate.py --out -         # prints the estimate instead

Rules the numbers follow (they are restated in the form's own rules table):

  - the team's target is 650,000,000 VND, under the charter's 700,000,000 funding limit;
  - F07, F08, and F12 are deferred to a second project, and the packages that test, fix, specify,
    or design them shrink with the build hours kept;
  - one seniority for every role, the ITviec median for 1 to 2 years;
  - an hour costs gross salary plus the employer's statutory contributions over 160 hours a month;
  - the hours are three-point, beta weighted, over the cone of uncertainty at requirements complete;
  - the project is charged by timesheet for booked hours; the supplier's company rules decide what
    else is not a project cost;
  - US dollar prices are converted at one Vietcombank selling rate;
  - every amount is rounded to the nearest 1,000 VND.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import math
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCOPE = ROOT / "docs" / "scope-package.en.md"
OUT = ROOT / "docs" / "forms" / "2-20-cost-estimates.en.md"
CR_OUT = ROOT / "docs" / "forms" / "3-3-change-request-scope.en.md"

TITLE = "Development and Deployment of a Learning Center Management Software"
DATE = "8 October 2026"
SCHEDULE_CR_DATE = "30 September 2026"
TARGET = 650_000_000
CHARTER_TOTAL = 700_000_000
CHARTER_LABOR = 539_000_000
CHARTER_WARRANTY = 35_000_000
CHARTER_LINES = [   # charter budget lines 1 to 6
    ("Personnel", 539_000_000), ("Infrastructure, licences, store accounts", 42_000_000),
    ("Facilities, equipment, travel", 14_000_000),
    ("Deployment, migration, training, documentation", 42_000_000),
    ("Warranty and support, months 2 to 6", 35_000_000), ("Contingency reserve", 28_000_000)]
CHARTER_RATE = {"PM": 162_500, "DEV": 118_750, "QA": 93_750, "MOB": 122_500}   # assumption 17, per hour
RESERVE = 28_000_000
# Form 2.20 of 7 October 2026 (commit 6056c43), salary beta weighted over 1 to 8 years: the estimate,
# and the estimate with the five paid through the levelled window.
OCT7_ESTIMATE, OCT7_WITH_IDLE = 1_450_419_000, 1_735_946_000
HOURS_PER_MONTH = 160
FX = 26_170                      # VND per USD, Vietcombank selling rate [fx]
CAP = 50_600_000                 # contribution ceiling from 1 July 2026 [bhxh]
EMPLOYER_CAPPED = 0.225          # social 17.5% + health 3% [bhxh], union fee 2% [union], on the capped base
EMPLOYER_UNCAPPED = 0.01         # unemployment insurance 1% [bhxh], its own ceiling is far above these salaries
DESK_HOURS = 160                 # 0.2 FTE for warranty months 2 to 6, web system only
CHARTER_DESK_HOURS = 280         # the charter's 0.35 FTE, web and app
CONE = (0.67, 1.0, 1.5)          # requirements complete, Figure 1 of [cone]
M0 = dt.date(2026, 9, 14)
CHARTER_M7 = dt.date(2027, 2, 5)
FULL_TIME = ("PM", "DEV1", "DEV2", "DEV3", "QA1")

F12_PACKAGES = ("1.2.3.4", "1.3.1.5", "1.4.4.1", "1.5.4.1", "1.5.4.2", "1.5.4.3", "1.5.4.4",
                "1.6.1.2", "1.9.1.1", "1.9.1.2")
DEFERRED = F12_PACKAGES + ("1.5.1.3", "1.5.2.1")          # with F07 and F08
DEFERRED_FUNCTIONS = "F07 teacher payroll, F08 assessment and progress reports, and F12 the mobile app"
LEAN = {   # work package: share of its dictionary hours kept, and why
    "1.1.1.2": (0.5, "status reports fortnightly instead of weekly"),
    "1.10.1.1": (0.4, "a support rota in the first warranty month instead of the whole team on call"),
}
BUILD_PREFIXES = ("1.4.1.", "1.4.2.", "1.4.4.", "1.5.1.", "1.5.2.", "1.5.3.", "1.5.4.")
WEB_ONLY = ("1.4.4.", "1.5.4.")
# Packages that specify, design, test, or fix named build work, and the build packages they cover;
# None means every build package, "web" every build package of the web system.
COVERS = {
    "1.2.1.2": None,
    "1.3.1.2": "web",
    "1.3.1.3": None,
    "1.3.1.4": "web",
    "1.5.5.1": ("1.5.1.1", "1.5.1.2", "1.5.1.3", "1.5.3.1", "1.5.3.2", "1.5.3.3"),
    "1.5.5.2": ("1.5.2.1", "1.5.2.2", "1.5.4.1", "1.5.4.2", "1.5.4.3", "1.5.4.4"),
    "1.5.5.3": ("1.5.",),
    "1.6.1.6": ("1.4.2.1", "1.4.2.2", "1.4.2.3", "1.5.3.1", "1.5.3.2", "1.5.3.3"),
    "1.6.1.7": ("1.4.1.2", "1.4.1.3", "1.5.1.1", "1.5.1.2", "1.5.1.3"),
    "1.6.1.8": ("1.4.1.1", "1.4.1.4", "1.5.2.1", "1.5.2.2"),
}
# Charter business case, section 2A: one-off release of overdue tuition, recurring net benefit with
# and without the app's push channel, and hosting and store accounts a year (assumption 19).
RELEASE = 360_000_000
RECURRING_APP, RECURRING_SMS = 90_600_000, 58_300_000
RUNNING_APP, RUNNING_WEB = 27_600_000, 25_000_000

REFS = [
    ("PMI", "A Guide to the Project Management Body of Knowledge, 6th edition, chapter 7 Project Cost "
     "Management: 7.2 Estimate Costs, 7.2.2.5 three-point estimating, 7.2.2.6 reserve analysis, 7.2.3.2 "
     "basis of estimates, and 7.3.2.5 funding limit reconciliation",
     "PMBOK6_and_Agile_Practice_Guide.pdf in the team repository",
     "Process, inputs and outputs, techniques, beta formula, contents of the basis of estimates, "
     "accuracy ranges, reconciliation of the estimate with a funding limit"),
    ("C. S. Dionisio", "A Project Manager's Book of Forms, 3rd edition, forms 2.19 Cost Management Plan, "
     "2.20 Cost Estimates, 2.21 Cost Estimating Worksheet, 3.3 Change Request", "PDF pages 93 to 103 and 181 to 185 (printed pages 82 to 92 and 170 to 174)",
     "Printed fields of the forms; the rules table takes three fields of form 2.19"),
    ("ITviec", "Vietnam IT Salary and Recruitment Market Report 2025-2026, 1,839 respondents surveyed in "
     "2025, monthly median salary by position and years of experience",
     "https://itviec.com/report/vietnam-it-salary-and-recruitment-market",
     "Medians for 1 to 2 years: Project Leader/Manager 29.85, Full-stack Developer 20.35, QA-QC 18, "
     "Mobile Developer 28.8 million VND a month; for 3 to 4 years, priced only as an alternative in the "
     "change request: 48.4, 34.5, 24.4, 29.05"),
    ("MISA AMIS", "Ty le dong BHXH 2026, published 18 September 2026, citing the Law on Social Insurance "
     "2024 and Decree 158/2025/ND-CP", "https://amis.misa.vn/?p=292831",
     "Employer share 21.5%: retirement 14, sickness 3, accident 0.5, health 3, unemployment 1; "
     "contribution ceiling 50,600,000 VND a month from 1 July 2026"),
    ("Thu Vien Phap Luat", "Quy dinh ve kinh phi cong doan 2%, Law on Trade Unions 2024, article 29, "
     "point b of clause 1",
     "https://thuvienphapluat.vn/ma-so-thue/phap-luat-thue/quy-dinh-ve-kinh-phi-cong-doan-2-o-van-ban-nao-49584-225246.html",
     "Union fee 2% of the payroll on which social insurance is paid, due whether or not a union exists"),
    ("Vietnam.vn", "Ti gia USD hom nay 5.10: Vietcombank ban ra 26.170 dong/USD",
     "https://www.vietnam.vn/ti-gia-usd-hom-nay-5-10-vietcombank-ban-ra-26-170-dong-usd",
     "26,170 VND per USD, the rate every dollar price here is converted at"),
    ("GitHub", "Pricing", "https://github.com/pricing",
     "Free plan for organizations: unlimited private repositories and collaborators, 2,000 Actions "
     "minutes a month, 0 USD"),
    ("Figma", "Pricing", "https://www.figma.com/pricing/",
     "Professional plan, full seat"),
    ("CostBench", "Figma pricing 2026", "https://costbench.com/software/design/figma/",
     "Professional full seat 16 USD a month billed annually, 20 USD billed monthly"),
    ("WHTop", "Viettel IDC plans T2.Gen 02 and T1.Base 05, updated 20 April 2026",
     "https://www.whtop.com/plans/viettelidc.com.vn/147281 and https://www.whtop.com/plans/viettelidc.com.vn/147277",
     "T1.Base 05 at 799,000 VND a month for staging; T2.Gen 02 at 1,200,000 VND a month for "
     "production, which the center provides; VAT not included"),
    ("VnEconomy", "Ten mien .vn cap 2 mot ky tu co phi duy tri len toi 40 trieu dong/nam, on Circular "
     "20/2023/TT-BTC",
     "https://vneconomy.vn/ten-mien-vn-cap-2-mot-ky-tu-co-phi-duy-tri-len-toi-40-trieu-dong-nam.htm",
     ".vn second-level domain: registration 100,000 VND once, maintenance 350,000 VND a year"),
    ("Let's Encrypt", "About Let's Encrypt", "https://letsencrypt.org/about/",
     "TLS certificates free of charge, renewed automatically"),
    ("Advertising Vietnam", "5 sai lam pho bien khi trien khai SMS brandname cho chuoi ban le",
     "https://advertisingvietnam.com/article/5-sai-lam-pho-bien-khi-trien-khai-sms-brandname-cho-chuoi-ban-le",
     "SMS brandname 600 to 800 VND a message"),
    ("S. McConnell", "Software Development's Cone of Uncertainty, Construx best practices white paper, "
     "version 1, January 2010",
     "https://www.construx.com/wp-content/uploads/2019/02/CxWhitePaper_ConeOfUncertainty.pdf",
     "Figure 1: estimates by skilled estimators fall within 0.67x to 1.5x of the outcome at "
     "Requirements Complete, 0.5x to 2x at Approved Product Definition"),
    ("VnExpress", "Nganh IT am tham thuong Tet",
     "https://vnexpress.net/nganh-it-am-tham-thuong-tet-3529076.html",
     "A 13th-month salary is common practice at IT employers in Viet Nam"),
    ("MISA", "Khau tru thue GTGT la gi? Dieu kien khau tru thue GTGT dau vao moi nhat, on the Law on "
     "VAT 48/2024/QH15, article 14", "https://sme.misa.vn/345365/khau-tru-thue-gtgt/",
     "A business on the deduction method deducts the input VAT on goods and services it uses for "
     "taxable business"),
]
R = {key: i + 1 for i, key in enumerate([
    "pmbok", "forms", "itviec", "bhxh", "union", "fx", "github", "figma", "figma2", "viettel", "domain",
    "letsencrypt", "sms", "cone", "tet", "vat"])}
assert len(R) == len(REFS)

COMPANY_RULES = [
    "Remote-first: the team works from home and meets at the center's branches for workshops, demos, "
    "and acceptance, so no desk is rented.",
    "Staff bring their own laptops, with no allowance for wear.",
    "Free tiers wherever they are enough: GitHub Free {github}; a paid seat only for the months it is used.",
    "Paperless: manuals and guides are delivered in the application and as files, not printed.",
    "Timesheets: the project is charged for the hours its people book on it. In weeks without project "
    "work they work on the supplier's other projects or training, and the supplier pays them in full "
    "either way; no one's pay depends on this project's hours.",
    "Every statutory contribution is charged with the hour. The 13th-month salary, the market's "
    "practice {tet}, is paid in full by the supplier from its own revenue and is not charged to projects.",
    "No overtime is planned; the levelled schedule keeps every person inside a 40-hour week.",
    "The supplier's shared costs (management, human resources, accounting) and its margin are not "
    "charged to the project.",
]


def ref(*keys):
    return "".join("[%d]" % R[k] for k in keys)


def r1000(x):
    return int(round(x / 1000.0)) * 1000


def vnd(x):
    return "{:,}".format(int(x))


def hrs(x):
    """Hours to one decimal, without a trailing .0."""
    s = "{:,.1f}".format(x)
    return s[:-2] if s.endswith(".0") else s


def pct(x):
    return "%+.0f%%" % (100 * x)


def beta(o, m, p):
    return (o + 4 * m + p) / 6


CONE_E = beta(*CONE)


def factor(k):
    """Hours multiplier: k 0, 1, 2 for the optimistic, most likely, pessimistic case; None expected."""
    return CONE_E if k is None else CONE[k]


# ---------------------------------------------------------------- labor

ROLES = {
    # code: (resource codes, ITviec position, gross medians for 1 to 2 and for 3 to 4 years in
    # million VND a month)
    "PM": (("PM",), "Project Leader/Manager", 29.85, 48.4),
    "DEV": (("DEV1", "DEV2", "DEV3"), "Full-stack Developer", 20.35, 34.5),
    "QA": (("QA1",), "QA-QC", 18.0, 24.4),
    "MOB": (("MOB1",), "Mobile Developer", 28.8, 29.05),
}
ROLE_LABEL = {"PM": "project manager and business analyst", "DEV": "developer",
              "QA": "QA engineer", "MOB": "mobile developer, part time"}
ROLE_OF = {res: k for k, v in ROLES.items() for res in v[0]}


def loaded(gross):
    return gross + EMPLOYER_CAPPED * min(gross, CAP) + EMPLOYER_UNCAPPED * gross


class Role:
    def __init__(self, code, senior=False):
        self.code = code
        _res, self.position, low, mid = ROLES[code]
        self.gross = (mid if senior else low) * 1_000_000
        self.monthly = loaded(self.gross)
        self.rate = r1000(self.monthly / HOURS_PER_MONTH)
        self.gross_hour = self.gross / HOURS_PER_MONTH


RATES = {k: Role(k) for k in ROLES}
SENIOR_RATES = {k: Role(k, senior=True) for k in ROLES}


# ---------------------------------------------------------------- calendar

def weekdays(a, b):
    n, d = 0, a
    while d <= b:
        n += d.weekday() < 5
        d += dt.timedelta(1)
    return n


def payroll_months(a, b):
    """Calendar months on payroll, part months pro rata by working days."""
    total, d = 0.0, a.replace(day=1)
    while d <= b:
        nxt = (d.replace(day=28) + dt.timedelta(4)).replace(day=1)
        last = nxt - dt.timedelta(1)
        total += weekdays(max(a, d), min(b, last)) / weekdays(d, last)
        d = nxt
    return total


def billed_months(a, b):
    """Calendar months a monthly subscription is billed for, from the month of a to the month of b."""
    return (b.year - a.year) * 12 + b.month - a.month + 1


def levelled(drop=(), scale=None):
    """Gate dates of the levelled schedule with the dropped work packages left out and the scaled ones
    shortened, and the start of the development environment, 1.2.3.2."""
    import level as L
    import schedule as S
    scale = scale or {}
    packages, gates = L.load_model(S.SCOPE.read_text(encoding="utf-8"),
                                   S.CHARTER.read_text(encoding="utf-8"))
    for code in drop:
        packages.pop(code, None)
    for code, f in scale.items():
        p = packages.get(code)
        if p is None or f == 1:
            continue
        busiest = collections.Counter()
        for a in p["acts"]:
            a["hours"] *= f
            busiest[a["res"]] += a["hours"]
        p["span"] = max(1, math.ceil(max(busiest.values(), default=0) / L.HOURS_PER_DAY))
    end = None
    for _ in range(6):
        result, new_gate, _cal = L.level(packages, gates, end)
        if new_gate[list(gates)[-1]] == end:
            break
        end = new_gate[list(gates)[-1]]
    return dict(new_gate), result["1.2.3.2"]["start"]


# ---------------------------------------------------------------- physical and software

class Item:
    """One priced resource that is not labor.

    unit costs are (optimistic, most likely, pessimistic); qty is a number or the same triple when the
    quantity is what is uncertain. Allowances carry no unit and no price source: they are the charter's
    figures, kept and flagged rather than replaced by a guess. line is the charter budget line the
    amount belongs to.
    """

    def __init__(self, act, ca, kind, column, line, name, variable, unit, qty, refs, note="",
                 allowance=False):
        self.act, self.ca, self.kind, self.column, self.line = act, ca, kind, column, line
        self.name, self.variable, self.unit, self.qty, self.refs = name, variable, unit, qty, refs
        self.note, self.allowance = note, allowance
        self.wp = act.split("-")[0]

    def amounts(self):
        q = self.qty if isinstance(self.qty, tuple) else (self.qty,) * 3
        return tuple(r1000(u * n) for u, n in zip(self.unit, q))

    def amount(self, k):
        return self.expected if k is None else self.amounts()[k]

    @property
    def three_point(self):
        o, _m, p = self.amounts()
        return o != p

    @property
    def expected(self):
        """Either the price or the quantity is three-point, never both."""
        if not self.three_point:
            return self.amounts()[1]
        if isinstance(self.qty, tuple):
            return r1000(self.unit[1] * beta(*self.qty))
        return r1000(beta(*self.unit) * self.qty)

    @property
    def likely_qty(self):
        return self.qty[1] if isinstance(self.qty, tuple) else self.qty


FIGMA_MONTHS = 2
STAGING = 799_000                # Viettel IDC T1.Base 05 [viettel]
PRINTING = "Documentation production and printing"
DATA_ENTRY = "External data-entry support"


def make_items(staging_months):
    return [
        Item("1.1.1.1-A4", "1.1.1", "Software", "Other Direct Costs", 2, "Figma Professional, one full seat",
             "Seat-month of Figma Professional, billed monthly", (20 * FX,) * 3, FIGMA_MONTHS,
             ("figma", "figma2", "fx"), "the two design months only"),
        Item("1.2.3.2", "1.2.3", "Software", "Other Direct Costs", 2, "Staging server",
             "Month of a T1.Base 05 staging server", (STAGING,) * 3, staging_months, ("viettel",),
             "from the development environment to closeout"),
        Item("1.5.4.3", "1.5.4", "Software", "Other Direct Costs", 2, "Codemagic macOS build minutes",
             "Codemagic macOS build minute", (0.095 * FX,) * 3, (750, 1500, 3000), ("fx",),
             "iOS builds need macOS"),
        Item("1.6.1.2-A3", "1.6.1", "Physical", "Equipment", 3, "Test phones, Android and iPhone",
             "Pair of test phones", (11_339_000, 11_339_000, 12_039_000), 1, (), "bought outright"),
        Item("1.7.1.2-A4", "1.7.1", "Human", "Total Labor", 4, DATA_ENTRY,
             "", (12_000_000,) * 3, 1, (), "", allowance=True),
        Item("1.8.1.1-A4", "1.8.1", "Software", "Other Direct Costs", 2,
             "Domain .vn first year and TLS certificate",
             "Domain .vn and TLS certificate, first year", (450_000, 450_000, 2_000_000), 1,
             ("domain", "letsencrypt"), "free certificate; the charter's 2,000,000 of budget line 2 as the "
             "pessimistic case for a paid one"),
        Item("1.8.1.3-A4", "1.8.1", "Physical", "Travel", 4, "Go-live support and on-site presence",
             "", (8_000_000,) * 3, 1, (), "", allowance=True),
        Item("1.8.2.1-A5", "1.8.2", "Physical", "Supplies", 4, PRINTING,
             "", (10_000_000,) * 3, 1, (), "", allowance=True),
        Item("1.8.2.2-A4", "1.8.2", "Physical", "Supplies", 4, "Training delivery, venue, and materials",
             "", (12_000_000,) * 3, 1, (), "", allowance=True),
        Item("1.8.2.2-A5", "1.8.2", "Physical", "Travel", 3, "Travel to the three branches",
             "", (3_000_000,) * 3, 1, (), "", allowance=True),
    ]


# What the charter's budget funded that this estimate does not, and why; amounts at the published
# price or, where marked, the charter's own figure.
NOT_PROJECT = [
    ("Production server, 12 months", r1000(12 * 1_200_000), "viettel",
     "the center provides the cloud virtual server (charter, Resources preassigned)"),
    ("Development and test gateway credits", 4_000_000, "sms",
     "the center provides and pays its gateway account (same place, and assumption 12); the charter's "
     "own figure"),
    ("Documentation printing", 10_000_000, None, "company rule 4, paperless; the charter's allowance"),
    ("External data entry", 12_000_000, None,
     "the center enters and cleans its own source data, as risk R6 and the project exclusions say; "
     "the charter's allowance"),
    ("Workspace", 0, None, "company rule 1, remote-first"),
    ("Laptops", 0, None, "company rule 2, staff bring their own"),
    ("GitHub Team", 0, None, "company rule 3, GitHub Free"),
    ("Weeks without project work", 0, None, "company rule 5, timesheets"),
    ("13th-month salary", 0, None, "company rule 6, paid by the supplier"),
]
EXCLUDED = (PRINTING, DATA_ENTRY)


# ---------------------------------------------------------------- scope package

ROW = re.compile(r"^\| (\d+(?:\.\d+)+)-A(\d+) \| ([^|]+?) \| ([A-Z0-9]*) *\| *([\d,]*) *\|", re.M)
CA_NAMES = {}
WP_NAMES = {}


def read_scope(path):
    """{work package: Counter(resource: hours)}, with the names into CA_NAMES and WP_NAMES."""
    md = path.read_text(encoding="utf-8")
    for m in re.finditer(r"^ +(\d+\.\d+\.\d+) +(.+?) +CA$", md, re.M):
        CA_NAMES[m.group(1)] = m.group(2).strip()
    for m in re.finditer(r"^#### (\d+\.\d+\.\d+\.\d+) (.+)$", md, re.M):
        WP_NAMES[m.group(1)] = m.group(2).strip()
    hours = collections.defaultdict(collections.Counter)
    for m in ROW.finditer(md):
        wp, _a, _act, res, h = m.groups()
        if res:
            hours[wp][res] += int(h.replace(",", ""))
    return hours


def code_key(code):
    return [int(x) for x in code.split(".")]


def ca_of(wp):
    return ".".join(wp.split(".")[:3])


def build_packages(wp_hours, web=False):
    return [w for w in wp_hours if w.startswith(BUILD_PREFIXES) and not (web and w.startswith(WEB_ONLY))]


def scope_scale(wp_hours, drop, lean=True, proportional=True):
    """{work package: share of its dictionary hours kept} for the packages that are not kept whole."""
    scale = {}
    if proportional and drop:
        for wp, cover in COVERS.items():
            if wp in drop:
                continue
            if cover is None or cover == "web":
                covered = build_packages(wp_hours, web=cover == "web")
            else:
                covered = [w for w in build_packages(wp_hours)
                           if w in cover or any(w.startswith(c) for c in cover if c.endswith("."))]
            every = sum(sum(wp_hours[w].values()) for w in covered)
            kept = sum(sum(wp_hours[w].values()) for w in covered if w not in drop)
            if kept < every:
                scale[wp] = kept / every
    if lean:
        for wp, (f, _why) in LEAN.items():
            scale[wp] = scale.get(wp, 1.0) * f
    return scale


# ---------------------------------------------------------------- the estimate

class Account:
    def __init__(self, ca, res_hours, items, rates, desk):
        self.ca, self.rates = ca, rates
        self.name = CA_NAMES[ca]
        self.lines = []   # (role, resources label, most likely hours, cone weighted)
        by_role = collections.defaultdict(list)
        for res, h in sorted(res_hours.items()):
            by_role[ROLE_OF[res]].append((res, h))
        for role in ("PM", "DEV", "QA", "MOB"):
            if role in by_role:
                h = sum(x for _r, x in by_role[role])
                label = ", ".join("%s %s h" % (r, hrs(x)) for r, x in by_role[role])
                self.lines.append((role, label, h, True))
        if ca == "1.10.1" and desk:
            self.lines.append(("DEV", "support desk %d h" % desk, desk, False))
        self.items = [i for i in items if i.ca == ca]

    @property
    def hours(self):
        return sum(h for _r, _l, h, _w in self.lines)

    @staticmethod
    def line_hours(h, weighted, k):
        return h * factor(k) if weighted else h

    def line_cost(self, role, h, weighted, k=None):
        return r1000(self.line_hours(h, weighted, k) * self.rates[role].rate)

    def labor(self, k=None):
        team = sum(self.line_cost(r, h, w, k) for r, _l, h, w in self.lines)
        return team + sum(i.amount(k) for i in self.items if i.kind == "Human")

    def physical(self, k=None):
        return sum(i.amount(k) for i in self.items if i.kind != "Human")

    def total(self, k=None):
        return self.labor(k) + self.physical(k)


class Estimate:
    """One estimate: the dictionary less the dropped packages and with the scaled ones shortened,
    priced under one set of rules.

    monthly True pays the five full-time staff for the whole levelled window instead of by timesheet;
    thirteenth True charges the 13th-month salary to the project; exclude names items not charged."""

    def __init__(self, wp_hours, drop=DEFERRED, lean=True, proportional=True, rates=RATES,
                 desk=DESK_HOURS, monthly=False, thirteenth=False, exclude=EXCLUDED):
        self.wp_hours = wp_hours
        self.drop, self.rates, self.desk_hours = set(drop), rates, desk
        self.monthly, self.charge_13th = monthly, thirteenth
        self.scale = scope_scale(wp_hours, self.drop, lean, proportional)
        self.dictionary_hours = sum(sum(c.values()) for c in wp_hours.values())
        self.gates, dev_start = levelled(tuple(sorted(self.drop)), self.scale)
        self.m7 = self.gates["M7"]
        self.months = payroll_months(M0, self.m7)
        self.capacity = self.months * HOURS_PER_MONTH
        self.staging_months = billed_months(dev_start, self.m7)
        self.items = [i for i in make_items(self.staging_months)
                      if i.wp not in self.drop and i.name not in exclude]
        by_ca = collections.defaultdict(collections.Counter)
        self.person = collections.Counter()
        for wp, c in wp_hours.items():
            if wp in self.drop:
                continue
            f = self.scale.get(wp, 1.0)
            kept = collections.Counter({res: h * f for res, h in c.items()})
            by_ca[ca_of(wp)].update(kept)
            self.person.update(kept)
        self.accounts = [Account(ca, by_ca[ca], self.items, rates, desk)
                         for ca in sorted(by_ca, key=code_key)]
        self.hours = sum(self.person.values())

    def booked(self, p, k):
        return self.person[p] * factor(k)

    def idle_hours(self, p, k=None):
        if not self.monthly:
            return 0.0
        return max(0.0, self.capacity - self.booked(p, k))

    def bench_hours(self, p, k=None):
        """Hours in the levelled window a full-time person spends off the project."""
        return max(0.0, self.capacity - self.booked(p, k))

    def idle(self, k=None):
        return r1000(sum(self.idle_hours(p, k) * self.rates[ROLE_OF[p]].rate for p in FULL_TIME))

    def thirteenth(self, k=None):
        if not self.charge_13th:
            return 0
        paid = (max(self.capacity, self.booked(p, k)) if self.monthly else self.booked(p, k)
                for p in FULL_TIME)
        gross = sum(h * self.rates[ROLE_OF[p]].gross_hour for h, p in zip(paid, FULL_TIME))
        gross += self.booked("MOB1", k) * self.rates["MOB"].gross_hour
        gross += self.desk_hours * self.rates["DEV"].gross_hour
        return r1000(gross / 12)

    def labor(self, k=None):
        return sum(a.labor(k) for a in self.accounts) + self.idle(k) + self.thirteenth(k)

    def physical(self, k=None):
        return sum(a.physical(k) for a in self.accounts)

    def total(self, k=None):
        return self.labor(k) + self.physical(k) + RESERVE

    @property
    def low(self):
        return self.total(0)

    @property
    def high(self):
        return self.total(2)

    @property
    def sigma(self):
        return r1000((self.high - self.low) / 6)

    def desk(self):
        return r1000(self.desk_hours * self.rates["DEV"].rate)

    def budget_lines(self):
        """The expected estimate in the six lines of the charter's budget table."""
        lines = [0] * 6
        for i in self.items:
            lines[i.line - 1] += i.expected
        team = sum(a.labor() for a in self.accounts) - sum(
            i.expected for i in self.items if i.kind == "Human") - self.desk()
        lines[0] = team + self.idle() + self.thirteenth()
        lines[4] = self.desk()
        lines[5] = RESERVE
        return lines


# ---------------------------------------------------------------- what each row says

SAME = "Hours as the dictionary sheets give them."
ASSUME = {
    "1.1.1": "Remote-first, staff on their own laptops, GitHub Free: company rules 1 to 3. "
             "<mark>Figma paid for the two design months only</mark>.",
    "1.2.3": "The gateway proof uses a free tier. A staging server <mark>from the development "
             "environment to closeout</mark>; production runs on the center's server.",
    "1.3.1": "Design work runs on the Figma seat of 1.1.1.",
    "1.5.2": "Test messages go through the center's own gateway account, which the charter says the "
             "center provides.",
    "1.6.1": "Web system test only.",
    "1.7.1": "The center enters and cleans its own source data, as risk R6 and the project exclusions "
             "say; <mark>the migration scripts keep their dictionary hours</mark>.",
    "1.8.1": "The certificate is free; production runs on the center's server. Go-live support kept at "
             "the charter's allowance, <mark>not checked against a published price</mark>.",
    "1.8.2": "Manuals delivered in the application and as files (company rule 4). Training and travel kept "
             "at the charter's allowances, <mark>not checked against a published price</mark>, since venues "
             "and distances are not known.",
    "1.10.1": "Warranty months 2 to 6 at <mark>0.2 FTE for the web system</mark>, costed as developer "
              "hours rather than as the charter's lump sum; an allocation, so not weighted.",
}


def assume_cell(est, acc):
    parts = [ASSUME.get(acc.ca, SAME)]
    gone = sorted((w for w in est.drop if ca_of(w) == acc.ca), key=code_key)
    if gone:
        parts.append("Deferred: %s." % ", ".join("%s %s" % (w, WP_NAMES[w]) for w in gone))
    scaled = sorted((w for w in est.scale if ca_of(w) == acc.ca and w not in est.drop), key=code_key)
    if scaled:
        parts.append("<mark>Scaled</mark>: %s." % "; ".join(
            "%s to %.0f%%%s" % (w, 100 * est.scale[w], ", " + LEAN[w][1] if w in LEAN else
                                ", with the build work it covers") for w in scaled))
    return " ".join(parts)


def resources_cell(acc):
    human = [label for _r, label, _h, _w in acc.lines] + [i.name for i in acc.items if i.kind == "Human"]
    parts = ["Human: " + "; ".join(human) + "."]
    phys = [i.name for i in acc.items if i.kind == "Physical"]
    soft = [i.name for i in acc.items if i.kind == "Software"]
    if acc.ca == "1.1.1":
        soft = ["GitHub Free, 0"] + soft
    if phys:
        parts.append("Physical: " + "; ".join(phys) + ".")
    if soft:
        parts.append("Software: " + "; ".join(soft) + ".")
    return " ".join(parts)


def method_cell(acc):
    m = ["Bottom-up; parametric rate; three-point hours"]
    if any(not i.allowance for i in acc.items):
        m.append("parametric prices")
    if any(i.allowance for i in acc.items):
        m.append("allowance")
    return "; ".join(m) + "."


def basis_cell(acc):
    parts = []
    for role, _label, h, w in acc.lines:
        parts.append("%s %s h%s at %s VND/h" % (role, hrs(h), ", %s weighted" % hrs(h * CONE_E) if w else "",
                                                vnd(acc.rates[role].rate)))
    text = "; ".join(parts) + " %s." % ref("itviec", "bhxh", "union", "cone")
    for i in acc.items:
        if i.allowance:
            text += " %s %s, allowance." % (i.name, vnd(i.expected))
        else:
            text += " %s %s %s." % (i.name, vnd(i.expected), ref(*i.refs))
    return text


def confidence_cell(acc):
    if any(i.allowance for i in acc.items):
        return "Medium; low for the allowances"
    return "Medium"


# ---------------------------------------------------------------- Markdown

def table(head, rows, right=()):
    out = ["| " + " | ".join(head) + " |",
           "| " + " | ".join("---:" if i in right else "---" for i in range(len(head))) + " |"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def header_table():
    return table(["Field", "Content"], [["**Project Title**", TITLE], ["**Date Prepared**", DATE]])


def long_date(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def payback_year(cost, recurring, running):
    """First year in which the cumulative net turns positive, on the charter's own model, with the
    running cost the center carries from the first year."""
    return math.ceil((cost - RELEASE) / (recurring - running))


def _bridge(total, steps):
    rows, run = [], 0
    for name, amount in steps:
        run += amount
        rows.append([name, vnd(amount), vnd(run)])
    assert run == total, (run, total)
    return rows


def build(est, full):
    accounts = est.accounts
    lab, phys, total = est.labor(), est.physical(), est.total()
    low, high, sigma = est.low, est.high, est.sigma
    rules = [r.format(github=ref("github"), tet=ref("tet")) for r in COMPANY_RULES]

    L = []
    w = L.append
    w("# 2.20 Activity Cost Estimates")
    w("")
    w("**Project:** %s" % TITLE)
    w("**Date prepared:** %s" % DATE)
    w("**Source:** A Project Manager's Book of Forms, 3rd edition, form 2.20, PDF pages 96 to 98 "
      "(printed pages 85 to 87), and form 2.21, PDF pages 99 to 103 (printed pages 88 to 92)")
    w("")
    w("The cost estimate of PMBOK 6 section 7.2 Estimate Costs %s: what each control account of the WBS "
      "costs in people, in physical resources, and in software, with the basis of every figure. Its "
      "inputs are the ones the book lists for form 2.20 %s. The scope baseline gives the WBS and the "
      "hours of the WBS dictionary, less the work the scope change request defers; the project schedule "
      "is the levelling of form 2.18 run on that reduced work; the resource requirements are the resource "
      "on each dictionary activity; the risk register of the charter is carried through its contingency "
      "reserve. There is no separate cost or quality management plan: the rules below stand in for the "
      "first, and the test plan of 1.3.2.1 and the criteria A01 to A12 set the test hours the dictionary "
      "already carries. There is no lessons learned register yet, which is also why the analogous section "
      "of form 2.21 is empty. Its outputs are this form, its basis of estimates in form 2.21 and the "
      "references, and the updates it proposes to the scope baseline, the resource requirements, the "
      "assumption log, and the risk register, which the scope change request "
      "`3-3-change-request-scope.en.md` carries." % (ref("pmbok"), ref("forms")))
    w("")
    w("This is an estimate, not a budget. Determine Budget, PMBOK 6 process 7.3, adds the estimates up "
      "period by period into the cost baseline of form 2.22, and its funding limit reconciliation, "
      "section 7.3.2.5, is where an estimate is compared with the money available %s. The charter makes "
      "700,000,000 VND available, and the team set a target of %s to keep a margin under it. The full "
      "scope cannot meet it, %s VND under the same rules, so the scope and the way the work is staffed "
      "were reduced until it could; the change request puts that reduction to the sponsor. The earned "
      "value formulas of PMBOK 6 Table 7-1 belong to Control Costs, process 7.4, and need the baseline "
      "first. Neither is in this document." % (ref("pmbok"), vnd(TARGET), vnd(full.total())))
    w("")
    w("### Rules of the estimate")
    w("")
    w("*Three fields of form 2.19 Cost Management Plan %s govern how every figure below is written. "
      "The project has no separate cost management plan, so they are stated here, followed by the "
      "supplier's company rules, which decide what is and is not a project cost, and the scope this "
      "estimate covers.*" % ref("forms"))
    w("")
    acc_lo, acc_hi = low / total - 1, high / total - 1
    w(table(["Field", "Content"], [
        ["**Units of Measure**",
         "Labor in hours of effort, and in person-months of %d hours, the charter's own conversion. "
         "Physical and software resources in their selling unit: seat-month, server-month, or the item. "
         "Money in VND; prices in US dollars converted at %s VND per USD, the Vietcombank selling rate of "
         "October 2026 %s." % (HOURS_PER_MONTH, vnd(FX), ref("fx"))],
        ["**Level of Precision**",
         "Hourly rates and every amount to the nearest 1,000 VND; hours to one decimal. Unit prices are "
         "kept as published, and the parametric worksheet multiplies them by the most likely quantity."],
        ["**Level of Accuracy**",
         "%s to %s around the estimate, the range from the optimistic to the pessimistic inputs. That is "
         "inside the -25%% to +75%% PMBOK 6 gives for a rough order of magnitude and wider than the -5%% to "
         "+10%% of a definitive estimate %s. The hours carry the cone of uncertainty at requirements "
         "complete %s; the estimate is redone at M1, when the requirements are baselined." % (
             pct(acc_lo), pct(acc_hi), ref("pmbok"), ref("cone"))],
    ]))
    w("")
    w("**Company rules.** The supplier keeps its own costs low without passing them to its staff:")
    w("")
    for n, r in enumerate(rules, 1):
        w("%d. %s" % (n, r))
    w("")
    gone = sorted(est.drop, key=code_key)
    gone_hours = sum(sum(c.values()) for wp, c in est.wp_hours.items() if wp in est.drop)
    w("**Scope of this estimate.** %s are deferred to a second project: the %d work packages %s, %s "
      "dictionary hours. The packages that specify, design, test, or fix named build work keep the share "
      "of their hours that the build work kept bears to all of it, and two packages are made leaner:" % (
          DEFERRED_FUNCTIONS[0].upper() + DEFERRED_FUNCTIONS[1:], len(gone), ", ".join(gone), vnd(gone_hours)))
    w("")
    srows = []
    for wp in sorted((x for x in est.scale if x not in est.drop), key=code_key):
        base = sum(est.wp_hours[wp].values())
        srows.append(["%s %s" % (wp, WP_NAMES[wp]), vnd(base), hrs(base * est.scale[wp]),
                      "%.0f%%" % (100 * est.scale[wp]),
                      LEAN[wp][1] if wp in LEAN else "with the build work it covers"])
    w(table(["Work package", "Dictionary hours", "Hours kept", "Share", "Why"], srows, right=(1, 2, 3)))
    w("")
    w("That leaves %s of the %s dictionary hours, %.0f%%." % (
        hrs(est.hours), vnd(est.dictionary_hours), 100 * est.hours / est.dictionary_hours))
    w("")
    w("*Reading convention. Form 2.20 is filled at control account level, one row for each of the %d "
      "control accounts the reduced scope keeps and one project-level row for the reserve, which the book "
      "permits, since its ID is \"the WBS ID or activity ID\" %s; form 2.21 shows the work behind each row. "
      "The Resource column names the three kinds of resource the estimate covers: human, physical, and "
      "software. An hour costs the gross monthly salary plus the employer's contributions, 21.5%% for "
      "social, health, and unemployment insurance %s and 2%% union fee %s, divided by %d hours; the salary "
      "is the ITviec median for 1 to 2 years of experience %s, <mark>the seniority every role is costed "
      "at</mark>, and developers are priced as full-stack, since the team has no separate front-end or "
      "back-end developer. The rates are single figures, and the uncertainty sits in the hours: each "
      "control account's hours are the most likely value, 0.67 and 1.5 times them the optimistic and "
      "pessimistic, the cone of uncertainty at requirements complete %s, weighted (O + 4M + P) / 6 as "
      "PMBOK 6 section 7.2.2.5 gives, which is %.4f times the hours; every three-point row of form 2.21 "
      "uses that one weighting, which is why its Weighting Equation column repeats. The warranty support "
      "desk is an allocation and is not weighted. The project is charged by timesheet (company rule 5), "
      "so a row is the cost of its effort and there is no row for paid time without project work. Range "
      "is what a row costs at the optimistic and the pessimistic inputs, and the total's range is %s to "
      "%s, taken with every row moving together; one standard deviation, (P - O) / 6, is %s, so the "
      "estimate plus one standard deviation, %s, is about the 84th percentile. Every amount excludes "
      "VAT, which the supplier deducts as input tax %s. Confidence Level reads Medium where the rates are "
      "survey medians and the prices are published, and Low for an allowance carried from the charter "
      "and for a reserve that is a percentage rather than a risk analysis. Reference numbers in square "
      "brackets point to the list at the end. <mark>Highlighted</mark> content is a choice or a quantity "
      "that no source confirms. Every figure is generated by `tools/cost_estimate.py` from "
      "`scope-package.en.md`, the levelling of `tools/level.py`, and the prices it lists; change those "
      "and rerun it rather than editing this file.*" % (
          len(accounts), ref("forms"), ref("bhxh"), ref("union"), HOURS_PER_MONTH, ref("itviec"),
          ref("cone"), CONE_E, vnd(low), vnd(high), vnd(sigma), vnd(total + sigma), ref("vat")))
    w("")

    # ---- form 2.20
    w("#### ACTIVITY COST ESTIMATES, page 1 of 1")
    w("")
    w(header_table())
    w("")

    def rng(lo, hi):
        return "%s to %s" % (vnd(min(lo, hi)), vnd(max(lo, hi)))

    rows = []
    for a in accounts:
        rows.append([
            "%s %s" % (a.ca, a.name), resources_cell(a), vnd(a.labor()), vnd(a.physical()), "",
            vnd(a.total()), method_cell(a), assume_cell(est, a), basis_cell(a),
            rng(a.total(0), a.total(2)), confidence_cell(a)])
    rows.append([
        "1 Project, contingency reserve", "Contingency reserve, charter budget line 6", "", "",
        vnd(RESERVE), vnd(RESERVE), "Reserve analysis %s." % ref("pmbok"),
        "Held at project level and drawn only through change control against risks R1 to R12. "
        "<mark>Not re-derived</mark>: the register carries no probability or impact to derive it from. "
        "At the charter's 4%% of the new estimate it would be %s." % vnd(r1000(0.04 * (lab + phys))),
        "Charter budget line 6.", vnd(RESERVE), "Low"])
    rows.append([
        "**Total**", "", "**%s**" % vnd(lab), "**%s**" % vnd(phys), "**%s**" % vnd(RESERVE),
        "**%s**" % vnd(total), "", "", "%s hours of work and %d support desk hours." % (
            hrs(est.hours), est.desk_hours),
        "**%s to %s**" % (vnd(low), vnd(high)), "Medium"])
    w(table(["WBS ID", "Resource", "Labor Costs", "Physical Costs", "Reserve", "Estimate", "Method",
             "Assumptions/Constraints", "Basis of Estimates", "Range", "Confidence Level"], rows,
            right=(2, 3, 4, 5)))
    w("")

    # ---- form 2.21 page 1
    w("#### COST ESTIMATING WORKSHEET, page 1 of 2")
    w("")
    w(header_table())
    w("")
    w("**Parametric Estimates**")
    w("")
    prow = []
    role_hours = collections.Counter()
    for a in accounts:
        for r, _l, h, wtd in a.lines:
            if wtd:
                role_hours[r] += h
    for code, role in est.rates.items():
        if not role_hours[code]:
            continue
        prow.append([" ".join(ROLES[code][0]), "Labor hour, %s" % ROLE_LABEL[code], vnd(role.rate),
                     hrs(role_hours[code]), vnd(r1000(role_hours[code] * role.rate))])
        if code == "DEV":
            prow.append(["1.10.1.2", "Labor hour, warranty support desk, developer", vnd(role.rate),
                         vnd(est.desk_hours), vnd(est.desk())])
    for i in est.items:
        if i.allowance:
            continue
        prow.append([i.act, i.variable, vnd(round(i.unit[1])), vnd(i.likely_qty), vnd(i.amounts()[1])])
    w(table(["ID", "Cost Variable", "Cost per Unit", "Number of Units", "Cost Estimate"], prow,
            right=(2, 3, 4)))
    w("")
    w("**Analogous Estimates**")
    w("")
    w(table(["ID", "Previous Activity", "Previous Cost", "Current Activity", "Multiplier", "Cost Estimate"],
            [[""] * 6, [""] * 6]))
    w("")
    w("**Three-Point Estimates**")
    w("")
    trow = []
    for code, role in est.rates.items():
        h = role_hours[code]
        if not h:
            continue
        o, m, p = (r1000(h * f * role.rate) for f in CONE)
        trow.append(["%s, labor hours, %s h" % (" ".join(ROLES[code][0]), hrs(h)), vnd(o), vnd(m), vnd(p),
                     "(O + 4M + P) / 6", vnd(r1000(h * CONE_E * role.rate))])
    for i in est.items:
        if not i.three_point:
            continue
        o, m, p = i.amounts()
        trow.append(["%s, %s" % (i.act, i.name), vnd(o), vnd(m), vnd(p), "(O + 4M + P) / 6",
                     vnd(i.expected)])
    w(table(["ID", "Optimistic Cost", "Most Likely Cost", "Pessimistic Cost", "Weighting Equation",
             "Expected Cost Estimate"], trow, right=(1, 2, 3, 5)))
    w("")

    # ---- form 2.21 page 2
    w("#### BOTTOM-UP COST ESTIMATING WORKSHEET, page 2 of 2")
    w("")
    w(header_table())
    w("")
    cols = ["Material", "Supplies", "Equipment", "Travel", "Other Direct Costs", "Indirect Costs"]
    brow = []
    sums = collections.Counter()
    for a in accounts:
        for role, label, h, wtd in a.lines:
            eh = a.line_hours(h, wtd, None)
            t = a.line_cost(role, h, wtd)
            brow.append(["%s %s" % (a.ca, label), hrs(eh), vnd(a.rates[role].rate), vnd(t)] + [""] * 7
                        + [vnd(t)])
            sums["hours"] += eh
            sums["labor"] += t
        for i in a.items:
            if i.kind == "Human":
                sums["labor"] += i.expected
                brow.append(["%s %s" % (i.act, i.name), "", "", vnd(i.expected)] + [""] * 7
                            + [vnd(i.expected)])
                continue
            cells = [""] * 6
            cells[cols.index(i.column)] = vnd(i.expected)
            sums[i.column] += i.expected
            brow.append(["%s %s" % (i.act, i.name), "", "", ""] + cells + ["", vnd(i.expected)])
    brow.append(["1 Contingency reserve", "", "", ""] + [""] * 6 + [vnd(RESERVE), vnd(RESERVE)])
    brow.append(["**Total**", "**%s**" % hrs(sums["hours"]), "", "**%s**" % vnd(sums["labor"])]
                + ["**%s**" % vnd(sums[c]) if sums[c] else "" for c in cols]
                + ["**%s**" % vnd(RESERVE), "**%s**" % vnd(total)])
    assert sums["labor"] == lab, (sums["labor"], lab)
    w(table(["ID", "Labor Hours", "Labor Rate", "Total Labor"] + cols + ["Reserve", "Estimate"], brow,
            right=tuple(range(1, 12))))
    w("")
    w("---")
    w("")

    # ---- paid time without booked work
    w("### Paid time without booked work")
    w("")
    w("None is charged. The charter commits the five full-time staff to the project \"before planning "
      "starts\" and makes them \"not renegotiable\"; company rule 5 keeps that commitment, since each of "
      "them is available to the project whenever its schedule needs them, and charges the project only "
      "for the hours they book. The levelled schedule of the reduced work runs %.2f months, %s to %s, "
      "%s hours a person; the rest of each person's time is the supplier's, spent on its other projects "
      "or training and paid by it:" % (est.months, long_date(M0), long_date(est.m7), hrs(est.capacity)))
    w("")
    w(table(["Person", "Hours booked, weighted", "Hours in the levelled window", "Hours the supplier carries"],
            [[p, hrs(est.booked(p, None)), hrs(est.capacity), hrs(est.bench_hours(p))] for p in FULL_TIME],
            right=(1, 2, 3)))
    w("")
    w("Had the five been paid by the month over that window instead, the option the estimate of 7 October 2026 "
      "priced separately, the project would carry those hours too.")
    w("")

    # ---- variance
    w("### Estimate against the charter: for the team to decide")
    w("")
    w("This estimate does not change the charter, the scope package, or their checker, which still hold "
      "the full scope and the 700,000,000 VND baseline. The reduction goes to the sponsor in "
      "`3-3-change-request-scope.en.md`, because deferring functions is the sponsor's decision.")
    w("")
    bl = est.budget_lines()
    vrows = [[name, vnd(amount), vnd(new), vnd(new - amount)] for (name, amount), new in zip(CHARTER_LINES, bl)]
    vrows.append(["**Total**", "**%s**" % vnd(CHARTER_TOTAL), "**%s**" % vnd(sum(bl)),
                  "**%s**" % vnd(sum(bl) - CHARTER_TOTAL)])
    assert sum(bl) == total, (sum(bl), total)
    w(table(["Charter budget line", "Charter (VND)", "This estimate (VND)", "Difference (VND)"], vrows,
            right=(1, 2, 3)))
    w("")
    charter_kept = r1000(sum(est.person[p] * CHARTER_RATE[ROLE_OF[p]] for p in est.person))
    plain = sum(a.line_cost(r, h, False) for a in accounts for r, _l, h, wtd in a.lines if wtd)
    weighted = sum(a.line_cost(r, h, True) for a in accounts for r, _l, h, wtd in a.lines if wtd)
    w("Where the difference comes from, in the order it arises:")
    w("")
    w(table(["Step", "Amount (VND)", "Running total (VND)"], _bridge(total, [
        ("Charter total", CHARTER_TOTAL),
        ("Work deferred or made leaner, %s of the %s dictionary hours kept, at the charter's rate mix" % (
            hrs(est.hours), vnd(est.dictionary_hours)), charter_kept - CHARTER_LABOR),
        ("The hours kept at the market median for 1 to 2 years instead of the charter's rate mix "
         "(assumption 17)", plain - charter_kept),
        ("The same hours weighted for the cone of uncertainty", weighted - plain),
        ("Warranty months 2 to 6, %d hours at a developer's rate instead of the lump sum" % est.desk_hours,
         est.desk() - CHARTER_WARRANTY),
        ("Physical and software: the charter's lines 2 to 4 less what is deferred, what moves to the "
         "center, and what the company rules remove", sum(bl[1:4]) - sum(a for _n, a in CHARTER_LINES[1:4])),
    ]), right=(1, 2)))
    w("")
    w("What the charter funded that this estimate does not charge:")
    w("")
    w(table(["Item", "Amount (VND)", "Why it is not a project cost"],
            [[n, vnd(a) if a else "", "%s%s" % (why, " %s" % ref(k) if k else "")] for n, a, k, why in NOT_PROJECT],
            right=(1,)))
    w("")
    w("The production server and the gateway credits are costs the charter itself places on the center, "
      "and the change request asks the sponsor to confirm that and correct budget line 2, which also funds "
      "them. The store accounts leave with F12.")
    w("")
    w("Proposed updates to other documents, carried by the change request and not made here: the scope "
      "reduction in the charter, the WBS, the dictionary, and the traceability matrix; assumption 17 "
      "replaced by the rates of form 2.21 page 1 and their source; the company rules added to the "
      "assumptions; new project risks, that a team costed at 1 to 2 years needs more hours than the "
      "dictionary gives, and that the weighted hours overrun the levelled window; budget line 2 and the "
      "Resources preassigned paragraph made to agree on hosting and the gateway account.")
    w("")

    # ---- references
    w("### References")
    w("")
    w("All web pages read on 7 October 2026. Prices are as the page showed them that day.")
    w("")
    for n, (who, what, where, used) in enumerate(REFS, 1):
        w("%d. %s. *%s*. %s. Used: %s." % (n, who, what, where, used))
    w("")
    return "\n".join(L)


# ---------------------------------------------------------------- change request

def boxes(w, title, checked):
    w("**%s**" % title)
    w("")
    for name in ("Increase", "Decrease", "Modify"):
        w("- [%s] %s" % ("x" if name == checked else " ", name))
    w("")


def build_cr(est, full, senior):
    total = est.total()
    pay_now = payback_year(total, RECURRING_SMS, RUNNING_WEB)
    bl = est.budget_lines()
    lines = "; ".join("line %d %s <mark>%s</mark>" % (n, name.lower(), vnd(v))
                      for n, ((name, _a), v) in enumerate(zip(CHARTER_LINES, bl), 1))
    L = []
    w = L.append
    w("# 3.3 Change Request, scope and cost")
    w("")
    w("**Project:** %s" % TITLE)
    w("**Date prepared:** %s" % DATE)
    w("**Source:** A Project Manager's Book of Forms, 3rd edition, form 3.3, PDF pages 181 to 185 (printed pages 170 to 174)")
    w("")
    w("*Reading convention. This request carries the cost estimate of form 2.20, "
      "`2-20-cost-estimates.en.md`, to the sponsor through Perform Integrated Change Control, PMBOK 6 "
      "section 4.6, as the funding limit reconciliation of section 7.3.2.5: the full scope does not fit "
      "the 700,000,000 VND the charter makes available, so the request reduces the scope and changes how "
      "the work is staffed until the estimate meets the team's target of %s. It follows the schedule "
      "change request of %s. Every figure is generated by `tools/cost_estimate.py` together with the "
      "estimate. The submitted charter, scope package, and schedule are not edited; the changes listed "
      "below are made in a new version of each once the sponsor decides. <mark>Highlighted</mark> figures "
      "are estimates, not quotations. The disposition on page 3 is the sponsor's and is left empty. Check "
      "boxes are marked `[x]` where they apply.*" % (vnd(TARGET), SCHEDULE_CR_DATE))
    w("")
    w("#### CHANGE REQUEST, page 1 of 3")
    w("")
    w(table(["Field", "Content"], [["**Project Title**", TITLE], ["**Date Prepared**", DATE],
                                   ["**Requestor**", "Project Manager"]]))
    w("")
    w("**Category**")
    w("")
    for name, on in (("Scope", True), ("Quality", True), ("Requirements", True), ("Cost", True),
                     ("Schedule", True), ("Documents", True)):
        w("- [%s] %s" % ("x" if on else " ", name))
    w("")
    lean = "; ".join("%s at %.0f%%, %s" % (wp, 100 * f, why) for wp, (f, why) in LEAN.items())
    w(table(["Field", "Content"], [
        ["**Detailed Description of Proposed Change**",
         "(1) Defer %s to a second project. Deliverable D11 and acceptance criterion A12 leave this "
         "project; D4 becomes the release of F06 and F09 to F11; A01 covers nine functions; the app parts "
         "of A02 and A09 leave. (2) Make the project work leaner: %s; warranty months 2 to 6 at 0.2 FTE "
         "for the web system, %d hours; the packages that specify, design, test, or fix named build work "
         "shrink with it. (3) Staff and charge the work differently: every role costed at the ITviec "
         "median for 1 to 2 years plus the employer's contributions, %s VND an hour for the project "
         "manager, %s for a developer, %s for the QA engineer, replacing assumption 17; the project charged "
         "by timesheet for booked hours. (4) Add the supplier's company rules to the assumptions: "
         "remote-first, staff on their own laptops, free tiers, paperless manuals, timesheets, the "
         "13th-month salary paid by the supplier, no planned overtime, no shared cost or margin charged. "
         "(5) The center provides the production server and the gateway account with its test messages, "
         "as the Resources preassigned paragraph says, and enters and cleans its own source data, as risk "
         "R6 says; budget line 2 and the data-entry allowance no longer fund them. (6) Re-cut the budget to "
         "the estimate, <mark>%s VND</mark>: %s. The %s VND left under the 700,000,000 funding limit is not "
         "requested for the cost baseline; the sponsor may hold it as a management reserve." % (
             DEFERRED_FUNCTIONS, lean, est.desk_hours, vnd(est.rates["PM"].rate), vnd(est.rates["DEV"].rate),
             vnd(est.rates["QA"].rate), vnd(total), lines, vnd(CHARTER_TOTAL - total))],
        ["**Justification for Proposed Change**",
         "Estimated bottom-up from the WBS dictionary at market rates, the full scope costs %s VND under the "
         "same company rules and the same 1 to 2 year team, and %s VND with the team at 3 to 4 years, "
         "paid by the month through the levelled window; the estimate of 7 October 2026, with the salary "
         "weighted over 1 to 8 years, was %s VND, and %s with the months paid without booked work. All "
         "exceed the funding limit, and the 28,000,000 "
         "VND contingency reserve cannot absorb any of them. Funding limit reconciliation leaves two courses: more "
         "money or less work. This request takes the second. The functions deferred are the ones the "
         "center can run without for a term: teacher payroll stays on its current spreadsheet, progress "
         "reports stay manual, and guardians keep SMS and the web portal. F10, the Director's view of "
         "revenue and fill rate, is kept, because it is the charter's main reason for the project. The "
         "reduced work costs %s VND, %s to %s at the optimistic and pessimistic inputs, %s hours instead of "
         "%s." % (vnd(full.total()), vnd(senior.total()), vnd(OCT7_ESTIMATE), vnd(OCT7_WITH_IDLE), vnd(total), vnd(est.low), vnd(est.high),
                  hrs(est.hours), vnd(est.dictionary_hours))],
    ]))
    w("")
    w("**Impacts of Change**")
    w("")
    boxes(w, "Scope", "Decrease")
    w(table(["Field", "Content"], [["**Description**",
        "%s deferred, %d work packages; deliverable D11 removed and D4 reduced. The %d remaining packages "
        "keep their deliverables; %d of them are scaled, listed in the scope paragraph of form 2.20." % (
            DEFERRED_FUNCTIONS[0].upper() + DEFERRED_FUNCTIONS[1:], len(est.drop),
            len(est.wp_hours) - len(est.drop), len([x for x in est.scale if x not in est.drop]))]]))
    w("")
    boxes(w, "Quality", "Modify")
    w(table(["Field", "Content"], [["**Description**",
        "A01 covers nine functions; A12 and the app parts of A02 and A09 leave. Iteration 2 code review "
        "and defect fixing shrink with the build work they cover. The team is costed at 1 to 2 years, so "
        "the same hours may yield more defects; the 99% UAT threshold of A01 is unchanged."]]))
    w("")
    w("#### CHANGE REQUEST, page 2 of 3")
    w("")
    boxes(w, "Requirements", "Decrease")
    w(table(["Field", "Content"], [["**Description**",
        "The requirements traced to F07, F08, and F12 move to the second project. The functional "
        "specification covers nine functions."]]))
    w("")
    boxes(w, "Cost", "Modify")
    w(table(["Field", "Content"], [["**Description**",
        "The cost baseline becomes <mark>%s VND</mark>, %s under the funding limit and %s under the team's "
        "target. Personnel is %s instead of 539,000,000; warranty months 2 to 6 are %s instead of "
        "35,000,000. The center takes on the production server, %s a year at the published price, and the "
        "test messages on its gateway account, both already its own under the charter, and its own data "
        "entry." % (vnd(total), vnd(CHARTER_TOTAL - total), vnd(TARGET - total), vnd(bl[0]), vnd(bl[4]),
                    vnd(NOT_PROJECT[0][1]))]]))
    w("")
    boxes(w, "Schedule", "Decrease")
    w(table(["Field", "Content"], [["**Description**",
        "Levelled on the reduced work, closeout falls on %s, against %s for the full scope in the schedule "
        "change request of %s; the gates are re-baselined in form 2.18." % (
            long_date(est.m7), long_date(full.m7), SCHEDULE_CR_DATE)]]))
    w("")
    w("**Stakeholder Impact**")
    w("")
    w("- [x] High risk")
    w("- [ ] Low risk")
    w("- [ ] Medium risk")
    w("")
    w(table(["Field", "Content"], [["**Description**",
        "Guardians and teachers get no mobile app in this project; guardians keep SMS and the web portal. "
        "The accountant keeps the teacher payroll spreadsheet, and teachers keep writing progress reports by "
        "hand. On the charter's cash model, SMS as the only channel brings the recurring benefit to %s VND a "
        "year and, with %s a year of hosting the center pays from the first year, payback to about year %d "
        "on this cost; the charter already names that as the reason F12 was in scope. The second project "
        "brings F12 and the push channel back. The center takes on its own data entry, with the accountant "
        "available 4 hours a week (assumption 10), which raises risk R6." % (
            vnd(RECURRING_SMS), vnd(RUNNING_WEB), pay_now)]]))
    w("")
    w(table(["Field", "Content"], [
        ["**Project Documents**",
         "Charter: functions and deliverables (F07, F08, F12; D4, D11), acceptance criteria A01, A02, A09, "
         "A12, the budget table and its total, assumption 17, the company rules added to the assumptions, "
         "the Resources preassigned paragraph and budget line 2 made to agree, the business case and "
         "payback, the payment amounts of the tranches. Risk register: R6 raised, and two new project "
         "risks, that a team costed at 1 to 2 years needs more hours than the dictionary gives, and that "
         "the weighted hours overrun the levelled window. Scope package: the deferred rows of the "
         "traceability matrix, the WBS, the dictionary sheets deferred or scaled, and the 700,000,000 VND "
         "check of `tools/check_scope.py`. Form 2.18 re-levelled; form 2.20 becomes the basis of the cost "
         "baseline, form 2.22."],
        ["**Comments**",
         "Alternatives weighed, each priced the same way. (1) The full scope under these rules: %s VND, "
         "over the funding limit. (2) The full scope at 3 to 4 years, paid by the month: %s VND, which "
         "would need the budget raised. (3) Keeping the team at 3 to 4 "
         "years on the reduced scope: %s VND, over the target. (4) Deferring F10 as well: rejected, because "
         "it is the charter's main reason for the project. The main risk of this request is the team's "
         "seniority: the dictionary hours were not estimated for a team at 1 to 2 years, and if their hours "
         "run at the pessimistic end of the cone the total reaches %s VND, above the funding limit. It is "
         "re-estimated at M1." % (
             vnd(full.total()), vnd(senior.total()),
             vnd(Estimate(est.wp_hours, rates=SENIOR_RATES).total()), vnd(est.high))],
    ]))
    w("")
    w("#### CHANGE REQUEST, page 3 of 3")
    w("")
    w("**Disposition:**")
    w("")
    w("- [ ] Approve")
    w("- [ ] Defer")
    w("- [ ] Reject")
    w("")
    w(table(["Field", "Content"], [["**Justification**", ""]]))
    w("")
    return "\n".join(L)


def estimates(hours):
    """The estimate, the full scope under the same rules, and the full scope at 3 to 4 years paid by the month."""
    est = Estimate(hours)
    full = Estimate(hours, drop=(), lean=False, desk=CHARTER_DESK_HOURS)
    senior = Estimate(hours, drop=(), lean=False, rates=SENIOR_RATES, desk=CHARTER_DESK_HOURS,
                      monthly=True, thirteenth=True, exclude=())
    return est, full, senior


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--scope", default=str(SCOPE))
    ap.add_argument("--out", default=str(OUT), help="output path, or - for standard output")
    ap.add_argument("--cr-out", default=str(CR_OUT), help="change request path, or - to skip it")
    a = ap.parse_args(argv)
    est, full, senior = estimates(read_scope(pathlib.Path(a.scope)))
    md = build(est, full)
    if a.out == "-":
        sys.stdout.write(md)
    else:
        pathlib.Path(a.out).write_text(md, encoding="utf-8")
        print("wrote %s" % a.out)
    if a.cr_out != "-":
        pathlib.Path(a.cr_out).write_text(build_cr(est, full, senior), encoding="utf-8")
        print("wrote %s" % a.cr_out)
    print("total %s (%s to %s), %s hours, full scope same rules %s, full scope at 3 to 4 years %s, M7 %s" % (
        vnd(est.total()), vnd(est.low), vnd(est.high), hrs(est.hours), vnd(full.total()),
        vnd(senior.total()), est.m7), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
