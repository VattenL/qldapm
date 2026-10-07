#!/usr/bin/env python3
"""Cost estimates, forms 2.20 and 2.21, generated from the WBS dictionary and published prices.

The hours come from the activity tables of docs/scope-package.en.md and nothing else. The prices are
the ones listed in REFS below, each with the page it was read from on the date prepared. Everything
the form prints is computed here, so a changed price or a changed sheet is a rerun, not an edit:

    python tools/cost_estimate.py                 # writes docs/forms/2-20-cost-estimates.en.md
    python tools/cost_estimate.py --out -         # prints it instead

Rules the numbers follow (they are restated in the form's own rules table):

  - labor is costed per hour as gross monthly salary plus the employer's statutory contributions,
    divided by the charter's 160 hours a person-month, rounded to the nearest 1,000 VND an hour;
  - the salary is a three-point estimate, beta weighted, over the ITviec medians for 1 to 2, 3 to 4,
    and 5 to 8 years of experience;
  - US dollar prices are converted at one Vietcombank selling rate;
  - every amount is rounded to the nearest 1,000 VND.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCOPE = ROOT / "docs" / "scope-package.en.md"
OUT = ROOT / "docs" / "forms" / "2-20-cost-estimates.en.md"

TITLE = "Development and Deployment of a Learning Center Management Software"
DATE = "7 October 2026"
CHARTER_TOTAL = 700_000_000
CHARTER_LABOR = 539_000_000
RESERVE = 28_000_000
HOURS_PER_MONTH = 160
FX = 26_170                      # VND per USD, Vietcombank selling rate [6]
CAP = 50_600_000                 # contribution ceiling from 1 July 2026 [4]
EMPLOYER_CAPPED = 0.225          # social 17.5% + health 3% [4], union fee 2% [5], on the capped base
EMPLOYER_UNCAPPED = 0.01         # unemployment insurance 1% [4], its own ceiling is far above these salaries
WARRANTY_HOURS = 280             # 0.35 FTE for months 2 to 6 after go-live, charter budget line 5

REFS = [
    ("PMI", "A Guide to the Project Management Body of Knowledge, 6th edition, chapter 7 Project Cost "
     "Management: 7.2 Estimate Costs, 7.2.2.5 three-point estimating, 7.2.2.6 reserve analysis, 7.2.3.2 "
     "basis of estimates", "PMBOK6_and_Agile_Practice_Guide.pdf in the team repository, pages 240 to 247",
     "Process, techniques, beta formula, contents of the basis of estimates"),
    ("C. S. Dionisio", "A Project Manager's Book of Forms, 3rd edition, forms 2.19 Cost Management Plan, "
     "2.20 Cost Estimates, 2.21 Cost Estimating Worksheet", "pages 82 to 92",
     "Printed fields of both forms; the rules table takes three fields of form 2.19"),
    ("ITviec", "Vietnam IT Salary and Recruitment Market Report 2025-2026, 1,839 respondents surveyed in "
     "2025, monthly median salary by position and years of experience",
     "https://itviec.com/report/vietnam-it-salary-and-recruitment-market",
     "Project Leader/Manager 29.85, 48.4, 58.45; Full-stack Developer 20.35, 34.5, 41.8; QA-QC 18, 24.4, "
     "29.75; Mobile Developer 28.8, 29.05, 37.35 million VND for 1 to 2, 3 to 4, 5 to 8 years"),
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
    ("Apple", "Apple Developer Program enrollment", "https://developer.apple.com/programs/enroll/",
     "99 USD per membership year"),
    ("Google", "Play Console Help, register for a developer account",
     "https://support.google.com/googleplay/android-developer/answer/6112435",
     "25 USD one-time registration fee"),
    ("GitHub", "Pricing", "https://github.com/pricing",
     "Team 4 USD per user a month for the first 12 months; Free 0 USD"),
    ("Figma", "Pricing", "https://www.figma.com/pricing/",
     "Professional plan, full seat 16 USD a month"),
    ("CostBench", "Figma pricing 2026", "https://costbench.com/software/design/figma/",
     "Professional full seat 16 USD a month billed annually, 20 USD billed monthly"),
    ("Codemagic", "Billing and pricing documentation", "https://docs.codemagic.io/billing/pricing/",
     "Pay as you go, macOS M2 virtual machine 0.095 USD a build minute"),
    ("WHTop", "Viettel IDC plans T2.Gen 02 and T1.Base 05, updated 20 April 2026",
     "https://www.whtop.com/plans/viettelidc.com.vn/147281 and https://www.whtop.com/plans/viettelidc.com.vn/147277",
     "4 vCPU, 8 GB: T2.Gen 02 at 1,200,000 VND a month, 80 GB SSD; T1.Base 05 at 799,000 VND a month, "
     "40 GB SSD; VAT not included"),
    ("VnEconomy", "Ten mien .vn cap 2 mot ky tu co phi duy tri len toi 40 trieu dong/nam, on Circular "
     "20/2023/TT-BTC",
     "https://vneconomy.vn/ten-mien-vn-cap-2-mot-ky-tu-co-phi-duy-tri-len-toi-40-trieu-dong-nam.htm",
     ".vn second-level domain: registration 100,000 VND once, maintenance 350,000 VND a year"),
    ("Let's Encrypt", "About Let's Encrypt", "https://letsencrypt.org/about/",
     "TLS certificates free of charge, renewed automatically"),
    ("Advertising Vietnam", "5 sai lam pho bien khi trien khai SMS brandname cho chuoi ban le",
     "https://advertisingvietnam.com/article/5-sai-lam-pho-bien-khi-trien-khai-sms-brandname-cho-chuoi-ban-le",
     "SMS brandname 600 to 800 VND a message"),
    ("Replus", "Gia thue coworking space 2026, published 13 May 2026",
     "https://replus.com.vn/gia-thue-coworking-space/",
     "Fixed desk 1,750,000 to 5,000,000 VND a month"),
    ("ICAD Vietnam", "Top 13 coworking space Ha Noi, published 31 October 2024",
     "https://icadvietnam.vn/coworking-space-ha-noi/",
     "Fixed desk per person a month at ten spaces, from 1,000,000 to 5,000,000 VND, median 2,975,000"),
    ("FPT Shop", "HP 250 G10 i5-1334U, 16 GB, 512 GB SSD",
     "https://fptshop.com.vn/may-tinh-xach-tay/hp-250-g10-i5-1334u-b3wa8at",
     "18,390,000 VND, VAT included"),
    ("Mytour", "Top 6 reliable PC and laptop rental services in Hanoi",
     "https://mytour.vn/en/blog/bai-viet/top-6-reliable-pc-and-laptop-rental-services-in-hanoi.html",
     "Laptop rental 600,000 to 1,000,000 VND a machine a month"),
    ("Viettablet", "Samsung Galaxy A06 4 GB, 64 GB", "https://www.viettablet.com/samsung-galaxy-a06",
     "2,249,000 VND, official, VAT included"),
    ("Dien Thoai Vui", "iPhone 13 cu", "https://dienthoaivui.com.vn/may-doi-tra/dien-thoai-cu/iphone-13-cu/",
     "iPhone 13 128 GB used: 9,090,000 VND scratched, 9,790,000 VND good condition, VAT included"),
    ("Thu Vien Phap Luat", "Nghi dinh luong toi thieu vung 2026 la Nghi dinh nao, on Decree 293/2025/ND-CP",
     "https://thuvienphapluat.vn/hoi-dap-phap-luat/nghi-dinh-luong-toi-thieu-vung-2026-la-nghi-dinh-nao-138076681.html",
     "Region I minimum wage 5,310,000 VND a month, 25,500 VND an hour, from 1 January 2026"),
]
R = {key: i + 1 for i, key in enumerate([
    "pmbok", "forms", "itviec", "bhxh", "union", "fx", "apple", "google", "github", "figma", "figma2",
    "codemagic", "viettel", "domain", "letsencrypt", "sms", "replus", "icad", "fptshop", "rental",
    "a06", "iphone", "minwage"])}
assert len(R) == len(REFS)


def ref(*keys):
    return "".join("[%d]" % R[k] for k in keys)


def r1000(x):
    return int(round(x / 1000.0)) * 1000


def vnd(x):
    return "{:,}".format(int(x))


def beta(o, m, p):
    return (o + 4 * m + p) / 6


# ---------------------------------------------------------------- labor

ROLES = {
    # code: (resource codes, ITviec position, gross O, M, P in million VND a month)
    "PM": (("PM",), "Project Leader/Manager", 29.85, 48.4, 58.45),
    "DEV": (("DEV1", "DEV2", "DEV3"), "Full-stack Developer", 20.35, 34.5, 41.8),
    "QA": (("QA1",), "QA-QC", 18.0, 24.4, 29.75),
    "MOB": (("MOB1",), "Mobile Developer", 28.8, 29.05, 37.35),
}
ROLE_LABEL = {"PM": "project manager and business analyst", "DEV": "developer",
              "QA": "QA engineer", "MOB": "mobile developer, part time"}
ROLE_OF = {res: k for k, v in ROLES.items() for res in v[0]}


def loaded(gross):
    return gross + EMPLOYER_CAPPED * min(gross, CAP) + EMPLOYER_UNCAPPED * gross


class Role:
    def __init__(self, code):
        self.code = code
        _res, self.position, *gross = ROLES[code]
        self.gross = [g * 1_000_000 for g in gross]
        self.monthly = [loaded(g) for g in self.gross]
        self.expected_monthly = beta(*self.monthly)
        self.hourly = [r1000(m / HOURS_PER_MONTH) for m in self.monthly]
        self.rate = r1000(self.expected_monthly / HOURS_PER_MONTH)


RATES = {k: Role(k) for k in ROLES}


# ---------------------------------------------------------------- physical and software

class Item:
    """One priced resource that is not labor.

    unit costs are (optimistic, most likely, pessimistic); qty is a number or the same triple when the
    quantity is what is uncertain. Allowances carry no unit and no price source: they are the charter's
    figures, kept and flagged rather than replaced by a guess.
    """

    def __init__(self, act, ca, kind, column, name, variable, unit, qty, refs, note="", allowance=False):
        self.act, self.ca, self.kind, self.column, self.name = act, ca, kind, column, name
        self.variable, self.unit, self.qty, self.refs = variable, unit, qty, refs
        self.note, self.allowance = note, allowance

    def amounts(self):
        q = self.qty if isinstance(self.qty, tuple) else (self.qty,) * 3
        return tuple(r1000(u * n) for u, n in zip(self.unit, q))

    @property
    def three_point(self):
        o, m, p = self.amounts()
        return o != p

    @property
    def expected(self):
        if not self.three_point:
            return self.amounts()[1]
        return r1000(self.expected_unit * self.expected_qty)

    @property
    def expected_unit(self):
        if isinstance(self.qty, tuple):
            return self.unit[1]
        return beta(*self.unit)

    @property
    def expected_qty(self):
        return beta(*self.qty) if isinstance(self.qty, tuple) else self.qty


PERSON_MONTHS = 27.5             # 25 core and 2.5 mobile, charter budget line 1
LAPTOP_MONTH = 18_390_000 / 36
GITHUB_MONTH = 4 * FX
ITEMS = [
    Item("1.1.1.1-A5", "1.1.1", "Physical", "Indirect Costs", "Workspace, fixed coworking desks",
         "Seat-month of a fixed coworking desk", (1_750_000, 3_000_000, 5_000_000), PERSON_MONTHS, ("replus", "icad"),
         "one desk for each person-month booked"),
    Item("1.1.1.1-A5", "1.1.1", "Physical", "Equipment", "Laptops, six",
         "Machine-month of a laptop", (LAPTOP_MONTH, LAPTOP_MONTH, 1_000_000), PERSON_MONTHS, ("fptshop", "rental"),
         "purchase price over 36 months, rental at the top of the range as the pessimistic case"),
    Item("1.1.1.1-A4", "1.1.1", "Software", "Other Direct Costs", "GitHub Team, repository and build",
         "User-month of GitHub Team", (0, GITHUB_MONTH, GITHUB_MONTH), PERSON_MONTHS, ("github", "fx"),
         "the Free plan as the optimistic case"),
    Item("1.1.1.1-A4", "1.1.1", "Software", "Other Direct Costs", "Figma Professional, one full seat",
         "Figma seat, annual plan, or two months as the optimistic case", (2 * 20 * FX, 192 * FX, 192 * FX), 1, ("figma", "figma2", "fx"),
         "annual plan; two months billed monthly as the optimistic case"),
    Item("1.5.2.2-A4", "1.5.2", "Software", "Other Direct Costs", "SMS test messages",
         "SMS message", (600, 800, 800), 5000, ("sms",),
         "development and test only; production messages are the center's (charter assumption 12)"),
    Item("1.5.4.3", "1.5.4", "Software", "Other Direct Costs", "Codemagic macOS build minutes",
         "Codemagic macOS build minute", (0.095 * FX,) * 3, (750, 1500, 3000), ("codemagic", "fx"),
         "iOS builds need macOS and no team machine is a Mac"),
    Item("1.6.1.2-A3", "1.6.1", "Physical", "Equipment", "Test phones, Galaxy A06 new and iPhone 13 used",
         "Pair of test phones", (2_249_000 + 9_090_000, 2_249_000 + 9_090_000, 2_249_000 + 9_790_000), 1,
         ("a06", "iphone"), "bought outright for the project"),
    Item("1.7.1.2-A4", "1.7.1", "Human", "Total Labor", "External data-entry support",
         "", (12_000_000,) * 3, 1, ("minwage",),
         "at the Region I minimum wage of 25,500 VND an hour it buys about 470 hours", allowance=True),
    Item("1.8.1.1-A3", "1.8.1", "Software", "Other Direct Costs", "Cloud server and staging, 12 months",
         "Month of a production and a staging server", (1_999_000,) * 3, 12, ("viettel",),
         "Viettel IDC T2.Gen 02 for production and T1.Base 05 for staging, VAT excluded"),
    Item("1.8.1.1-A4", "1.8.1", "Software", "Other Direct Costs", "Domain .vn first year and TLS certificate",
         "Domain .vn and TLS certificate, first year", (450_000, 450_000, 2_000_000), 1, ("domain", "letsencrypt"),
         "free certificate; the charter's 2,000,000 as the pessimistic case for a paid one"),
    Item("1.8.1.3-A4", "1.8.1", "Physical", "Travel", "Go-live support and on-site presence",
         "", (8_000_000,) * 3, 1, (), "", allowance=True),
    Item("1.8.2.1-A5", "1.8.2", "Physical", "Supplies", "Documentation production and printing",
         "", (10_000_000,) * 3, 1, (), "", allowance=True),
    Item("1.8.2.2-A4", "1.8.2", "Physical", "Supplies", "Training delivery, venue, and materials",
         "", (12_000_000,) * 3, 1, (), "", allowance=True),
    Item("1.8.2.2-A5", "1.8.2", "Physical", "Travel", "Travel to the three branches",
         "", (3_000_000,) * 3, 1, (), "", allowance=True),
    Item("1.9.1.1-A4", "1.9.1", "Software", "Other Direct Costs", "Apple Developer Program and Google Play",
         "US dollar of store fees", (FX,) * 3, 124, ("apple", "google", "fx"), "99 USD a year and 25 USD once"),
]

CA_NAMES = {}


# ---------------------------------------------------------------- scope package

ROW = re.compile(r"^\| (\d+(?:\.\d+)+)-A(\d+) \| ([^|]+?) \| ([A-Z0-9]*) *\| *([\d,]*) *\|", re.M)


def read_scope(path):
    md = path.read_text(encoding="utf-8")
    for m in re.finditer(r"^ +(\d+\.\d+\.\d+) +(.+?) +CA$", md, re.M):
        CA_NAMES[m.group(1)] = m.group(2).strip()
    hours = collections.defaultdict(collections.Counter)
    for m in ROW.finditer(md):
        wp, _a, _act, res, h = m.groups()
        if res:
            hours[".".join(wp.split(".")[:3])][res] += int(h.replace(",", ""))
    return hours


def code_key(code):
    return [int(x) for x in code.split(".")]


# ---------------------------------------------------------------- the estimate

class Account:
    def __init__(self, ca, res_hours):
        self.ca = ca
        self.name = CA_NAMES[ca]
        self.lines = []   # (role, resources label, hours)
        by_role = collections.defaultdict(list)
        for res, h in sorted(res_hours.items()):
            by_role[ROLE_OF[res]].append((res, h))
        for role in ("PM", "DEV", "QA", "MOB"):
            if role in by_role:
                hrs = sum(h for _r, h in by_role[role])
                label = ", ".join("%s %d h" % (r, h) for r, h in by_role[role])
                self.lines.append((role, label, hrs))
        if ca == "1.10.1":
            self.lines.append(("DEV", "support desk %d h" % WARRANTY_HOURS, WARRANTY_HOURS))
        self.items = [i for i in ITEMS if i.ca == ca]

    @property
    def hours(self):
        return sum(h for _r, _l, h in self.lines)

    def _items(self, human, k):
        its = [i for i in self.items if (i.kind == "Human") == human]
        if k is None:
            return sum(i.expected for i in its)
        return sum(i.amounts()[k] for i in its)

    def labor(self, k=None):
        """Team hours at the rate, plus outsourced people, which the book counts as labor."""
        if k is None:
            team = sum(h * RATES[r].rate for r, _l, h in self.lines)
        else:
            team = sum(h * RATES[r].hourly[k] for r, _l, h in self.lines)
        return team + self._items(True, k)

    def physical(self, k=None):
        return self._items(False, k)

    @property
    def estimate(self):
        return self.labor() + self.physical()

    @property
    def low(self):
        return self.labor(0) + self.physical(0)

    @property
    def high(self):
        return self.labor(2) + self.physical(2)

    @property
    def sigma(self):
        lab = sum(h * (RATES[r].hourly[2] - RATES[r].hourly[0]) for r, _l, h in self.lines) / 6
        return lab + sum((i.amounts()[2] - i.amounts()[0]) / 6 for i in self.items)


# ---------------------------------------------------------------- what each row says

ASSUME = {
    "1.1.1": "A desk, a laptop, and a GitHub seat for every person-month booked, 27.5 in all, at a "
             "<mark>coworking space the supplier rents</mark>. <mark>Figma bought as an annual plan "
             "although the design work needs about two months</mark>.",
    "1.2.1": "Hours as the dictionary sheets give them.",
    "1.2.2": "Hours as the dictionary sheets give them.",
    "1.2.3": "Hours as the dictionary sheets give them; the gateway and framework proofs use free "
             "tiers.",
    "1.3.1": "Hours as the dictionary sheets give them; design work runs on the Figma seat of 1.1.1.",
    "1.3.2": "Hours as the dictionary sheets give them.",
    "1.4.1": "Hours as the dictionary sheets give them.",
    "1.4.2": "Hours as the dictionary sheets give them.",
    "1.4.3": "Hours as the dictionary sheets give them.",
    "1.4.4": "The mobile developer is on a labor contract for the hours booked, not for idle weeks.",
    "1.5.1": "Hours as the dictionary sheets give them.",
    "1.5.2": "<mark>5,000 test messages</mark> through the gateway; production messages are paid by the "
             "center under charter assumption 12.",
    "1.5.3": "Hours as the dictionary sheets give them.",
    "1.5.4": "<mark>1,500 macOS build minutes</mark>, since iOS builds need macOS and no team laptop is "
             "a Mac.",
    "1.5.5": "Hours as the dictionary sheets give them.",
    "1.6.1": "Both phones bought outright for the project at retail price, VAT included.",
    "1.6.2": "Hours as the dictionary sheets give them.",
    "1.7.1": "Data-entry support kept at the charter's allowance; <mark>no published price was used, "
             "and the quantity of hours is not known</mark>.",
    "1.8.1": "Cloud prices exclude VAT; the certificate is free. Go-live support kept at the charter's "
             "allowance, <mark>not checked against a published price</mark>.",
    "1.8.2": "Printing, training, and travel kept at the charter's allowances; <mark>not checked "
             "against a published price</mark>, since page counts, venues, and distances are not known.",
    "1.8.3": "Hours as the dictionary sheets give them.",
    "1.9.1": "Store accounts in the center's name, paid by the project for the first year.",
    "1.10.1": "Warranty months 2 to 6 at <mark>0.35 FTE</mark>, charter budget line 5, costed as "
              "developer hours rather than as the charter's lump sum.",
    "1.10.2": "Hours as the dictionary sheets give them.",
}


def resources_cell(acc):
    human = [label for _r, label, _h in acc.lines] + [i.name for i in acc.items if i.kind == "Human"]
    parts = ["Human: " + "; ".join(human) + "."]
    phys = [i.name for i in acc.items if i.kind == "Physical"]
    soft = [i.name for i in acc.items if i.kind == "Software"]
    if phys:
        parts.append("Physical: " + "; ".join(phys) + ".")
    if soft:
        parts.append("Software: " + "; ".join(soft) + ".")
    return " ".join(parts)


def method_cell(acc):
    m = ["Bottom-up; three-point rate"]
    if any(not i.allowance for i in acc.items):
        m.append("parametric prices")
    if any(i.allowance for i in acc.items):
        m.append("allowance")
    return "; ".join(m) + "."


def basis_cell(acc):
    parts = []
    for role, _label, h in acc.lines:
        parts.append("%s %s h at %s VND/h" % (role, vnd(h), vnd(RATES[role].rate)))
    text = "; ".join(parts) + " %s." % ref("itviec", "bhxh", "union")
    for i in acc.items:
        if i.allowance:
            text += " %s %s, allowance%s." % (
                i.name, vnd(i.expected), "; %s %s" % (i.note, ref(*i.refs)) if i.refs else "")
        else:
            text += " %s %s %s." % (i.name, vnd(i.expected), ref(*i.refs))
    return text


def confidence_cell(acc):
    if any(i.allowance for i in acc.items):
        return "Medium; low for the allowances"
    return "Medium"


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


# ---------------------------------------------------------------- Markdown

def table(head, rows, right=()):
    out = ["| " + " | ".join(head) + " |",
           "| " + " | ".join("---:" if i in right else "---" for i in range(len(head))) + " |"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def header_table():
    return table(["Field", "Content"], [["**Project Title**", TITLE], ["**Date Prepared**", DATE]])


def build(hours):
    accounts = [Account(ca, hours[ca]) for ca in sorted(hours, key=code_key)]
    lab = sum(a.labor() for a in accounts)
    phys = sum(a.physical() for a in accounts)
    total = lab + phys + RESERVE
    low = sum(a.low for a in accounts) + RESERVE
    high = sum(a.high for a in accounts) + RESERVE
    sigma = sum(a.sigma for a in accounts)
    total_hours = sum(a.hours for a in accounts)
    sigma = r1000(sigma)
    p84 = total + sigma
    z700 = (CHARTER_TOTAL - total) / sigma

    charter_months = payroll_months(dt.date(2026, 9, 14), dt.date(2027, 2, 5))
    levelled_months = payroll_months(dt.date(2026, 9, 14), dt.date(2027, 3, 19))
    extra = round(levelled_months, 2) - 5
    core = [("PM", 1), ("DEV", 3), ("QA", 1)]
    idle_labor = sum(n * r1000(extra * RATES[r].expected_monthly) for r, n in core)
    seat, laptop, github = ITEMS[0], ITEMS[1], ITEMS[2]
    idle_other = sum(r1000(5 * extra * i.expected_unit) for i in (seat, laptop, github))
    idle = idle_labor + idle_other

    L = []
    w = L.append
    w("# 2.20 Activity Cost Estimates")
    w("")
    w("**Project:** %s" % TITLE)
    w("**Date prepared:** %s" % DATE)
    w("**Source:** A Project Manager's Book of Forms, 3rd edition, form 2.20, pages 85 to 87, and "
      "form 2.21, pages 88 to 92")
    w("")
    w("The cost estimate of PMBOK 6 section 7.2 Estimate Costs %s: what each control account of the WBS "
      "costs in people, in physical resources, and in software, with the basis of every figure. Its "
      "inputs are the ones Figure 7-4 names: the scope baseline (the WBS and the hours of the WBS "
      "dictionary), the project schedule (the levelled calendar of form 2.18), the resource "
      "requirements (the resource on each dictionary activity), and the risk register of the charter, "
      "through its contingency reserve. Its outputs are this form, its basis of estimates in form "
      "2.21 and in the references at the end, and the updates it proposes to the assumption log and "
      "the risk register." % ref("pmbok"))
    w("")
    w("This is an estimate, not a budget. Determine Budget, PMBOK 6 process 7.3, adds the estimates up period "
      "by period into the cost baseline of form 2.22, and is done once the sponsor has decided on the "
      "figures below; the earned value formulas of Table 7-1 belong to Control Costs, process 7.4, "
      "and need that baseline first. Neither is in this document.")
    w("")
    w("### Rules of the estimate")
    w("")
    w("*Three fields of form 2.19 Cost Management Plan %s govern how every figure below is written. "
      "The project has no separate cost management plan, so they are stated here.*" % ref("forms"))
    w("")
    w(table(["Field", "Content"], [
        ["**Units of Measure**",
         "Labor in hours of effort, and in person-months of %d hours where people are paid by the "
         "month, the charter's own conversion. Physical and software resources in their selling unit: "
         "seat-month, machine-month, user-month, message, build minute, server-month, or the item. "
         "Money in VND; prices in US dollars converted at %s VND per USD, the Vietcombank selling rate "
         "of October 2026 %s." % (HOURS_PER_MONTH, vnd(FX), ref("fx"))],
        ["**Level of Precision**",
         "Hourly rates rounded to the nearest 1,000 VND, and every amount to the nearest 1,000 VND. "
         "Unit prices are kept as published."],
        ["**Level of Accuracy**",
         "At initiation the charter's figure was a rough order of magnitude, -25%% to +75%% in PMBOK 6 "
         "terms %s. This estimate is bottom-up over the 78 work packages with published prices, but "
         "the people are not yet hired and their seniority is not known, so its accuracy is stated per "
         "row as a range from the optimistic to the pessimistic inputs rather than as one percentage, "
         "and it is re-estimated when the team is hired." % ref("pmbok")],
    ]))
    w("")
    w("*Reading convention. Form 2.20 is filled at control account level, one row for each of the 24 "
      "control accounts of the WBS and one for the project, which the book permits, since its ID is "
      "\"the WBS ID or activity ID\" %s; form 2.21 shows the work behind each row. The Resource "
      "column names the three kinds of resource the estimate covers: human, physical, and software. "
      "Labor is costed from the hours of the WBS dictionary and nothing else, %s hours in all: the "
      "dictionary's 4,400 and %d hours of support desk for warranty months 2 to 6, which the "
      "dictionary carries as a lump sum. An hour costs the monthly gross salary plus the employer's "
      "contributions, 21.5%% for social, health, and unemployment insurance %s and 2%% union fee %s, "
      "divided by %d hours. The salary is not one figure but three, the ITviec medians for 1 to 2, "
      "3 to 4, and 5 to 8 years of experience %s, weighted (O + 4M + P) / 6 as PMBOK 6 section "
      "7.2.2.5 gives, with <mark>3 to 4 years as the most likely seniority</mark>; every three-point row of form 2.21 uses "
      "that one weighting, which is why its Weighting Equation column repeats; developers are "
      "priced as full-stack, since the team has no separate front-end or back-end developer. The "
      "estimate is that expected value, and the Range is what the row costs at "
      "the optimistic and the pessimistic inputs. Prices are taken as published: goods bought at retail "
      "include VAT, cloud and software services exclude it; the difference is under 3,000,000 VND and is "
      "left in. Confidence Level reads Medium where the rates are survey medians "
      "for a team not yet hired at a known seniority and the prices are published, and Low for an "
      "allowance carried from the charter or a reserve that is a percentage rather than a risk "
      "analysis. Reference numbers in square brackets point to the list at the end. <mark>Highlighted</mark> content is a choice or a quantity that no source "
      "confirms. The analogous section of form 2.21 is empty, because the supplier has no record of "
      "a previous similar project to scale from. Every figure is generated by "
      "`tools/cost_estimate.py` from `scope-package.en.md` and the prices it lists; change those and "
      "rerun it rather than editing this file.*" % (
          ref("forms"), vnd(total_hours), WARRANTY_HOURS, ref("bhxh"), ref("union"),
          HOURS_PER_MONTH, ref("itviec")))
    w("")

    # ---- form 2.20
    w("#### ACTIVITY COST ESTIMATES, page 1 of 1")
    w("")
    w(header_table())
    w("")
    rows = []
    for a in accounts:
        rows.append([
            "%s %s" % (a.ca, a.name), resources_cell(a), vnd(a.labor()), vnd(a.physical()), "",
            vnd(a.estimate), method_cell(a), ASSUME[a.ca], basis_cell(a),
            "%s to %s" % (vnd(a.low), vnd(a.high)), confidence_cell(a)])
    rows.append([
        "1 Project", "Contingency reserve, charter budget line 6", "", "", vnd(RESERVE), vnd(RESERVE),
        "Reserve analysis %s." % ref("pmbok"),
        "Held at project level and drawn only through change control against risks R1 to R12. "
        "<mark>Not re-derived</mark>: the register carries no probability or impact to derive it from. "
        "At the charter's 4%% of the new estimate it would be %s." % vnd(r1000(0.04 * (lab + phys))),
        "Charter budget line 6.", vnd(RESERVE), "Low"])
    rows.append([
        "**Total**", "", "**%s**" % vnd(lab), "**%s**" % vnd(phys), "**%s**" % vnd(RESERVE),
        "**%s**" % vnd(total), "", "", "%s labor hours." % vnd(total_hours),
        "**%s to %s**" % (vnd(low), vnd(high)),
        "About 50%% at the estimate and about 84%% at %s, one standard deviation of %s above it, the rows taken to move together. "
        "%s is %.1f standard deviations below the estimate." % (
            vnd(p84), vnd(sigma), vnd(CHARTER_TOTAL), -z700)])
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
    for code, role in RATES.items():
        hrs = sum(h for a in accounts for r, l, h in a.lines if r == code and "support desk" not in l)
        res = " ".join(ROLES[code][0])
        prow.append([res, "Labor hour, %s" % ROLE_LABEL[code], vnd(role.rate), vnd(hrs),
                     vnd(hrs * role.rate)])
        if code == "DEV":
            prow.append(["1.10.1.2", "Labor hour, warranty support desk, developer", vnd(role.rate),
                         vnd(WARRANTY_HOURS), vnd(WARRANTY_HOURS * role.rate)])
    for i in ITEMS:
        if i.allowance:
            continue
        unit = i.expected_unit
        qty = i.expected_qty
        prow.append([i.act, i.variable, vnd(round(unit)), "{:,.1f}".format(qty).replace(".0", ""),
                     vnd(i.expected)])
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
    for code, role in RATES.items():
        o, m, p = (r1000(x) for x in role.monthly)
        trow.append(["%s, person-month" % " ".join(ROLES[code][0]), vnd(o), vnd(m), vnd(p),
                     "(O + 4M + P) / 6", vnd(r1000(role.expected_monthly))])
    for i in ITEMS:
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
        for role, label, h in a.lines:
            t = h * RATES[role].rate
            brow.append(["%s %s" % (a.ca, label), vnd(h), vnd(RATES[role].rate), vnd(t)] + [""] * 7
                        + [vnd(t)])
            sums["hours"] += h
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
    brow.append(["**Total**", "**%s**" % vnd(sums["hours"]), "", "**%s**" % vnd(sums["labor"])]
                + ["**%s**" % vnd(sums[c]) if sums[c] else "" for c in cols]
                + ["**%s**" % vnd(RESERVE), "**%s**" % vnd(total)])
    w(table(["ID", "Labor Hours", "Labor Rate", "Total Labor"] + cols + ["Reserve", "Estimate"], brow,
            right=tuple(range(1, 12))))
    w("")
    w("---")
    w("")

    # ---- paid time without booked work
    w("### Paid time without booked work")
    w("")
    w("The estimate above pays for the hours the WBS needs. The people who work them are paid by the "
      "month, and a month in which someone has little booked work costs the same as a full one. "
      "Whether that idle time is a project cost depends on whether the person can be released when "
      "there is no work, and the charter answers that for most of the team: the five full-time staff "
      "are \"committed before planning starts and are not renegotiable\", so they stay on the payroll "
      "for the whole schedule. The part-time mobile developer is the exception and is paid for the "
      "hours booked, which the estimate already does.")
    w("")
    w("Each of the five has 800 hours in the dictionary, 5 person-months at %d hours. How long they "
      "are paid depends on which calendar holds:" % HOURS_PER_MONTH)
    w("")
    w(table(["Calendar", "Window", "Months on payroll", "Booked months", "Paid without booked work",
             "Cost"], [
        ["Charter", "14 September 2026 to 5 February 2027", "%.2f" % charter_months, "5.00",
         "None; %.2f months short" % (5 - charter_months), "0"],
        ["Levelled schedule, form 2.18", "14 September 2026 to 19 March 2027",
         "%.2f" % levelled_months, "5.00", "<mark>%.2f months each</mark>" % extra, vnd(idle)],
    ], right=(2, 3, 5)))
    w("")
    w("Months on payroll count part months by working days. The charter's window holds %.2f months, "
      "so 800 hours a person do not fit in it, which is the same finding the levelled schedule "
      "reached. If the sponsor accepts the levelled dates of change request 3.3, each of the five is "
      "paid %.2f months for which the WBS books no work: %s of labor at their expected monthly cost, "
      "and %s for their desks, laptops, and GitHub seats over the same months, %s in all. That figure "
      "is not in the form, because it belongs to a schedule decision rather than to the work of any "
      "control account. There are three ways to avoid paying it: lend the five to other work of the "
      "supplier in the weeks they are not booked, which the charter's commitment rules out unless the "
      "sponsor waives it; keep the charter's dates, which the levelling showed the hours do not fit; "
      "or accept it as the cost of the later end date." % (
          charter_months, extra, vnd(idle_labor), vnd(idle_other), vnd(idle)))
    w("")

    # ---- variance
    w("### Estimate against the charter: for the team to decide")
    w("")
    w("This estimate does not change the charter, the scope package, or their checker, which still "
      "hold the 700,000,000 VND baseline. The difference is reported here for the team and the "
      "sponsor, because choosing between the options below is their decision.")
    w("")
    ch_lab = CHARTER_LABOR + 35_000_000 + 12_000_000   # with warranty line 5 and the data-entry allowance
    w(table(["Line", "Charter (VND)", "This estimate (VND)", "Difference (VND)"], [
        ["Labor, with warranty months 2 to 6 and outsourced data entry", vnd(ch_lab), vnd(lab), vnd(lab - ch_lab)],
        ["Physical and software", vnd(CHARTER_TOTAL - ch_lab - RESERVE), vnd(phys),
         vnd(phys - (CHARTER_TOTAL - ch_lab - RESERVE))],
        ["Contingency reserve", vnd(RESERVE), vnd(RESERVE), "0"],
        ["**Total**", "**%s**" % vnd(CHARTER_TOTAL), "**%s**" % vnd(total),
         "**%s**" % vnd(total - CHARTER_TOTAL)],
    ], right=(1, 2, 3)))
    w("")
    w("With the idle months of the levelled schedule the estimate is %s, %s above the charter." % (
        vnd(total + idle), vnd(total + idle - CHARTER_TOTAL)))
    w("")
    junior = sum(a.labor(0) for a in accounts)
    w("Where the difference comes from:")
    w("")
    w("1. **The charter's rate mix is a junior team.** Assumption 17 costs a developer at 19,000,000 "
      "VND a month fully loaded, which is about %s gross once the employer's 23.5%% is taken out. "
      "ITviec puts a full-stack developer with 1 to 2 years at 20,350,000 and with 3 to 4 years at "
      "34,500,000 %s. The same holds for the other roles: a project manager at 26,000,000 loaded is "
      "below the median for 1 to 2 years. Even with every role at the 1 to 2 year median, labor "
      "comes to %s, against %s in the charter." % (
          vnd(r1000(19_000_000 / 1.235)), ref("itviec"), vnd(junior), vnd(ch_lab)))
    w("2. **Workspace was nearly free in the charter.** %s for 27.5 seat-months is %s a seat-month; "
      "coworking desks cost %s to %s %s." % (
          "9,000,000 for workspace and laptops together", vnd(r1000(9_000_000 / PERSON_MONTHS)),
          "1,750,000", "5,000,000", ref("replus", "icad")))
    w("3. **Warranty months 2 to 6** were a lump sum of 35,000,000 for 0.35 FTE over five months; at "
      "a developer's rate that is %s." % vnd(WARRANTY_HOURS * RATES["DEV"].rate))
    w("")
    w("What the team can do, each with what it costs:")
    w("")
    w("1. Raise the budget through a change request to the sponsor, at the estimate, or at %s if the "
      "levelled schedule is accepted with the team kept on." % vnd(total + idle))
    w("2. Hire at the 1 to 2 year level and keep the hours, which brings labor to %s; the hours of the "
      "dictionary were not estimated for a junior team, so this moves the risk from cost to schedule "
      "and quality." % vnd(junior))
    w("3. Reduce the scope through a change request, for example the mobile app F12, which carries "
      "%s of mobile developer hours and its own build, store, and test costs." % vnd(
          sum(h * RATES["MOB"].rate for a in accounts for r, _l, h in a.lines if r == "MOB")))
    w("4. Put the team in the supplier's own office, so that the workspace becomes the supplier's "
      "overhead rather than a project cost; that removes %s from the estimate but not from the "
      "supplier's books." % vnd(ITEMS[0].expected))
    w("")
    w("Proposed updates to other documents, not made here: assumption 17 replaced by the rates of "
      "form 2.21 page 1 and their source; a new project risk in the register, that the budget does not "
      "cover the team at market rates, with this estimate as its evidence; and charter assumption 12, "
      "that the center pays for its gateway account, confirmed for test messages as well.")
    w("")

    # ---- references
    w("### References")
    w("")
    w("All web pages read on %s. Prices are as the page showed them that day." % DATE)
    w("")
    for n, (who, what, where, used) in enumerate(REFS, 1):
        w("%d. %s. *%s*. %s. Used: %s." % (n, who, what, where, used))
    w("")
    return "\n".join(L), dict(total=total, labor=lab, physical=phys, low=low, high=high, sigma=sigma,
                              idle=idle, hours=total_hours)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--scope", default=str(SCOPE))
    ap.add_argument("--out", default=str(OUT), help="output path, or - for standard output")
    a = ap.parse_args(argv)
    hours = read_scope(pathlib.Path(a.scope))
    md, figures = build(hours)
    if a.out == "-":
        sys.stdout.write(md)
    else:
        pathlib.Path(a.out).write_text(md, encoding="utf-8")
        print("wrote %s" % a.out)
    print("; ".join("%s %s" % (k, vnd(v)) for k, v in figures.items()), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
