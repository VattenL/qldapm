"""Deterministic calculators for the derived numbers a reviewer recomputes.

Every formula is one the books print, and every result carries the page where
the book prints it (PDF page and printed page). Where a book prints no formula
the tool says "not stated in the book" and does not supply one. Inputs are
never defaulted to project values; the only optional input with a default is
the performance factor, whose neutral value 1.0 is the book's "average
resource".

    pm_calc.py evm --bac 1000 --pv 400 --ev 350 --ac 450
    pm_calc.py pert --o 20 --m 25 --p 36
    pm_calc.py effort-to-duration --effort-hours 150 --resources 2 --availability 0.75 --performance 0.8
    pm_calc.py analogous --previous-value 10 --previous-size 160 --current-size 200
    pm_calc.py bottom-up --labor-hours 40 --labor-rate 50 --material 300
    pm_calc.py risk-score --probability high --impact very-high
    pm_calc.py risk-score --matrix
    pm_calc.py emv --outcome 0.6:80 0.4:-30
    pm_calc.py emv --option Build 120 0.6:200 0.4:90 --option Upgrade 50 0.6:120 0.4:60
    pm_calc.py weighted-score --weights 30 20 50 --scores 4 3 5 --scores 3 5 4 --names A B
    pm_calc.py comms-channels --people 5
    pm_calc.py earned-schedule --es 6 --at 8
    pm_calc.py cpm --activity A=5 --activity B=5 --activity C=10 --activity D=15 --link A,B --link A,C --link B,D --link C,D
    pm_calc.py cpm --activity A=5 --activity B=3 --link A,B,SS,2 --deadline 12 --slip A=2
    pm_calc.py velocity --completed 21 18 24 --remaining 120
    pm_calc.py cd3 --item "Pay online" 9000 3 --item "Reports" 4000 4
    pm_calc.py payback --investment 360 --net 50 120 150 160
    pm_calc.py evm --bac 700 --pv 280 --ev 252 --ac 294 --threshold 5 --base bac pv
    pm_calc.py cpm --activity A=5 --activity B=3 --link A,B --slip A=4 --start 2027-01-25 --holiday 2027-02-06:2027-02-14
    pm_calc.py cpm --activity A=5 --activity B=3 --link A,B --start 2027-01-25 --deadline 2027-02-05
    pm_calc.py evm --bac 700 --threshold 5
    pm_calc.py crash --option A 10 7 30 --option B 8 6 12 --needed 4
    pm_calc.py reserve --contingency 28 --used 5 --risk R5=0.3:12 --risk R7=20%:8
    pm_calc.py funding --tranche M0=140 --tranche M3=175 --through M3 --spent 300
    pm_calc.py response-effectiveness --option "Second provider" 10 4 3

Add --json to any subcommand for machine-readable output. Exit code 2 for an
input the book's formula cannot take.

Outside arithmetic aids. Seven computations are of this kind what a book names or draws
but does not give as an equation, and each says so in its output: comms-channels
(pair counting), payback (the first period in which the cumulative net benefit
reaches the investment; PMBOK 6 names payback in section 1.2.6.4, printed page
34, PDF page 73, and section 12.1.2.3, printed page 473, PDF page 512, and
prints no formula), and cpm (the forward and backward pass that PMBOK 6 section
6.5.2.2, printed page 210, PDF page 249, describes and Figure 6-16 shows
without equations), reserve (remaining contingency against the expected value of the open risks, after PMBOK 6
section 11.7.2.1), funding (tranches against cost to date, after section 7.3.3.2), and the overrun percent of evm
(no book prints a percent variance). response-effectiveness computes the ratio PMBOK 6 section 11.5.2.8 prints in
words. velocity and cd3 compute the definitions the Agile
Practice Guide prints in words. Beta standard deviation: neither book prints
one, so pert reports it as not stated.

Rounding is not stated in either book. Results print up to four decimals,
unrounded. Report an index as printed, so a CPI of 0.8621 is not shown as a
flattering 0.86; money goes in whole currency units, and a threshold is
compared in the unrounded form.
"""

import argparse
import datetime
import json
import math
import sys
import textwrap
from decimal import ROUND_HALF_UP, Decimal

EPS = 1e-9

LEVEL_NAMES = ("Very Low", "Low", "Medium", "High", "Very High")
LEVEL_CODES = ("VL", "L", "M", "H", "VH")
LEVEL_ALIASES = {
    "vl": 0, "very low": 0, "very-low": 0, "verylow": 0,
    "l": 1, "low": 1,
    "m": 2, "medium": 2, "moderate": 2,
    "h": 3, "high": 3,
    "vh": 4, "very high": 4, "very-high": 4, "veryhigh": 4,
}

# Probability and impact numbers of PMBOK 6 Figure 11-5; the book calls them an example.
FIG_PROBABILITY = ("0.10", "0.30", "0.50", "0.70", "0.90")
FIG_IMPACT = ("0.05", "0.10", "0.20", "0.40", "0.80")
# Impact numbers of Book of Forms form 2.35 tailoring tip, one doubling per level.
DOUBLING_IMPACT = ("0.5", "1", "2", "4", "8")
# Probability bands of Book of Forms Table 2.31 as (low, high) whole percents.
PROB_BANDS = ((1, 20), (21, 40), (41, 60), (61, 80))

C_EVA = "PMBOK 6 section 7.4.2.2, printed page 262 (PDF page 301)"
C_EVA_IDX = "PMBOK 6 section 7.4.2.2, printed page 263 (PDF page 302)"
C_EAC = "PMBOK 6 section 7.4.2.2, printed page 265 (PDF page 304)"
C_EAC_BU = "PMBOK 6 section 7.4.2.2, printed page 264 (PDF page 303)"
C_TCPI = "PMBOK 6 section 7.4.2.3, printed page 266 (PDF page 305)"
C_T71 = "PMBOK 6 Table 7-1, printed page 267 (PDF page 306)"
C_EVBASE = "PMBOK 6 section 7.4.2.2, printed page 261 (PDF page 300)"
C_44 = "Book of Forms form 4.4, Table 4.4, PDF page 218 (printed page 207)"
C_43 = "Book of Forms form 4.3, Table 4.3, PDF page 214 (printed page 203)"
C_BETA_DUR = ("Book of Forms form 2.17, PDF page 84 (printed page 73) and Table 2.16, "
              "PDF page 87 (printed page 76)")
C_BETA_COST = ("Book of Forms form 2.21, PDF page 99 (printed page 88) and Table 2.19, "
               "PDF page 100 (printed page 89)")
C_BETA_PM = "PMBOK 6 section 7.2.2.5, printed page 245 (PDF page 284)"
C_TRI_DUR = "PMBOK 6 section 6.4.2.4, printed page 201 (PDF page 240)"
C_217 = "Book of Forms form 2.17, Table 2.16, PDF page 86 (printed page 75)"
C_217_NOTE = "Book of Forms form 2.17, PDF page 84 (printed page 73)"
C_221_AN = "Book of Forms form 2.21, Table 2.19, PDF page 100 (printed page 89)"
C_221_BU = "Book of Forms form 2.21, Table 2.20, PDF page 101 (printed page 90)"
C_BU_PM = "PMBOK 6 section 7.2.2.4, printed page 244 (PDF page 283)"
C_231 = "Book of Forms form 2.34, Table 2.31, PDF pages 149 to 150 (printed pages 138 to 139)"
C_231_P = "Book of Forms form 2.34, Table 2.31, PDF page 149 (printed page 138)"
C_235 = "Book of Forms form 2.35, PDF page 154 (printed page 143)"
C_235_TIP = "Book of Forms form 2.35 tailoring tips, PDF page 153 (printed page 142)"
C_FIG115 = "PMBOK 6 Figure 11-5, printed page 408 (PDF page 447)"
C_MATRIX_PM = "PMBOK 6 section 11.1.3.1, printed page 408 (PDF page 447)"
C_TREE = "PMBOK 6 section 11.4.2.5 and Figure 11-15, printed page 435 (PDF page 474)"
C_239 = "Book of Forms form 2.39, PDF page 166 (printed page 155) and Table 2.35, PDF page 167 (printed page 156)"
C_CHAN = "PMBOK 6 section 10.1.2.2, printed page 370 (PDF page 409)"

C_ES = "PMBOK 6 Trends and Emerging Practices in Project Cost Management, printed page 233 (PDF page 272)"
C_CPM = "PMBOK 6 section 6.5.2.2 and Figure 6-16, printed pages 210 to 211 (PDF pages 249 to 250)"
C_VEL = "Agile Practice Guide section 5.4.1, printed page 64 (PDF page 874)"
C_VEL_EX = "Agile Practice Guide, printed page 61 (PDF page 871)"
C_CD3 = "Agile Practice Guide Table 5-1, printed page 59 (PDF page 869)"
C_RESERVE = "PMBOK 6 section 11.7.2.1, printed page 456 (PDF page 495)"
C_FUNDING = "PMBOK 6 section 7.3.3.2, printed page 256 (PDF page 295) and Figure 7-9, printed page 255 (PDF page 294)"
C_RESPONSE = "PMBOK 6 section 11.5.2.8, printed page 446 (PDF page 485)"
C_PAYBACK = ("PMBOK 6 section 1.2.6.4, printed page 34 (PDF page 73) and section 12.1.2.3, printed page 473 "
             "(PDF page 512)")

NOT_STATED = "not stated in the book"


class CalcError(Exception):
    """An input a book formula cannot take, or one the book does not define."""


def row(label, value, formula, cite, status=None, assumption=None, why=None, unit=""):
    return {"label": label, "value": value, "unit": unit, "formula": formula, "status": status,
            "assumption": assumption, "why": why, "cite": cite}


def section(title, rows):
    return {"title": title, "rows": rows}


def ratio(num, den):
    return None if den is None or abs(den) < EPS or num is None else num / den


def sign_word(v, positive, zero, negative):
    if v is None:
        return None
    if abs(v) < EPS:
        return zero
    return positive if v > 0 else negative


def need(name, value, positive=False, nonneg=False):
    if not math.isfinite(value):
        raise CalcError("%s must be a finite number" % name)
    if positive and not value > 0:
        raise CalcError("%s must be greater than zero" % name)
    if nonneg and value < 0:
        raise CalcError("%s must not be negative" % name)


def parse_number(text, name):
    try:
        value = float(str(text).replace(",", ""))
    except ValueError:
        raise CalcError("%s: %r is not a number" % (name, text))
    if not math.isfinite(value):
        raise CalcError("%s: %r is not a finite number" % (name, text))
    return value


def parse_share(text, name):
    """A probability or availability as a fraction (0.75) or with a percent sign (75%)."""
    raw = str(text).strip()
    if raw.endswith("%"):
        value = parse_number(raw[:-1], name) / 100
    else:
        value = parse_number(raw, name)
    if value < 0:
        raise CalcError("%s must not be negative, got %r" % (name, text))
    if value > 1 + EPS:
        raise CalcError("%s: write %s as a fraction up to 1 (0.75) or with a percent sign up to 100%% (75%%), "
                        "got %r" % (name, name, text))
    return value


BASE_NAMES = ("bac", "pv", "ev", "ac")
OUTSIDE_PERCENT = ("outside arithmetic aid, not stated in the book: " + C_43.replace("Table 4.3, ", "") +
                   " gives no percent variance")


def threshold_only(bac, threshold, bases):
    """The amount a percent threshold stands for when only the BAC is known. Outside arithmetic aid."""
    need("bac", bac, positive=True)
    need("threshold", threshold, nonneg=True)
    if [b for b in bases if b != "bac"]:
        raise CalcError("a threshold on %s needs --pv, --ev and --ac as well; only the bac base can be computed "
                        "from the BAC alone" % ", ".join(b for b in bases if b != "bac"))
    return {"title": "Variance threshold amount",
            "inputs": {"BAC": bac, "threshold_percent": threshold},
            "sections": [section("Threshold as an amount of the BAC (outside arithmetic aid, not stated in the book)", [
                row("Threshold amount", threshold / 100 * bac, "percent / 100 x BAC", NOT_STATED,
                    assumption="Base BAC = %s. %s." % (num(bac), OUTSIDE_PERCENT))])],
            "notes": ["Pass --pv, --ev and --ac as well to compare the cost overrun and each forecast with this "
                      "threshold. When the charter does not say which baseline the percent is taken of, test every "
                      "candidate base (bac pv) rather than choosing one."]}


def evm(bac, pv, ev, ac, bottom_up_etc=None, approved_eac=None, threshold=None, bases=None):
    given = [v is not None for v in (pv, ev, ac)]
    if not all(given):
        if threshold is not None and not any(given):
            return threshold_only(bac, threshold, bases or ["bac"])
        raise CalcError("give --pv, --ev and --ac with --bac (SV and SPI need EV and PV, CV and CPI need EV and "
                        "AC); with only --bac, --threshold prints the amount the percent stands for")
    for name, value in (("bac", bac), ("pv", pv), ("ev", ev), ("ac", ac)):
        need(name, value, nonneg=True)
    if not bac > 0:
        raise CalcError("bac must be greater than zero: every percent and every forecast is measured against the "
                        "budget at completion (%s)" % C_EVBASE)
    cv = ev - ac
    sv = ev - pv
    cpi = ratio(ev, ac)
    spi = ratio(ev, pv)
    # The words of the Interpretation column of PMBOK 6 Table 7-1, printed page 267 (PDF page 306).
    cost_state = ("under planned cost", "on planned cost", "over planned cost")
    sched_state = ("ahead of schedule", "on schedule", "behind schedule")

    def index_state(v, words):
        return None if v is None else sign_word(v - 1, words[0], words[1], words[2])

    notes = []
    if ev > bac + EPS:
        notes.append("EV is above BAC. EV cannot be greater than the authorized planned value budget "
                     "(%s); check the inputs." % C_EVBASE)
    if pv > bac + EPS:
        notes.append("PV is above BAC. The total of the planned value is the BAC (%s); check the inputs."
                     % C_EVBASE)
    if abs(pv) < EPS and abs(ev) < EPS and abs(ac) < EPS:
        notes.append("PV, EV and AC are all zero: nothing was planned or done yet, so there is no status to "
                     "report. The forecasts and the TCPI below only restate the BAC.")
    if abs(ac) < EPS:
        notes.append("AC is zero, so CPI and every forecast that divides by it are not computable.")
    if abs(pv) < EPS:
        notes.append("PV is zero, so SPI is not computable.")

    status = section("Variances and indexes (no assumption beyond the inputs)", [
        row("CV", cv, "CV = EV - AC", C_EVA + "; " + C_T71 + "; " + C_44,
            sign_word(cv, *cost_state)),
        row("SV", sv, "SV = EV - PV", C_EVA + "; " + C_T71 + "; " + C_44,
            sign_word(sv, *sched_state)),
        row("CPI", cpi, "CPI = EV / AC", C_EVA_IDX + "; " + C_T71 + "; " + C_44,
            index_state(cpi, cost_state), why=None if cpi is not None else "AC is zero"),
        row("SPI", spi, "SPI = EV / PV", C_EVA_IDX + "; " + C_T71 + "; " + C_44,
            index_state(spi, sched_state), why=None if spi is not None else "PV is zero"),
        row("Percent planned", None if ratio(pv, bac) is None else 100 * pv / bac, "PV / BAC", C_44,
            unit="%", why=None if ratio(pv, bac) is not None else "BAC is zero"),
        row("Percent earned (percent complete)", None if ratio(ev, bac) is None else 100 * ev / bac,
            "EV / BAC", C_44 + "; PMBOK 6 says EV is often used to calculate percent complete but prints "
            "no formula (" + C_EVBASE + ")", unit="%", why=None if ratio(ev, bac) is not None else "BAC is zero"),
        row("Percent spent", None if ratio(ac, bac) is None else 100 * ac / bac, "AC / BAC", C_44,
            unit="%", why=None if ratio(ac, bac) is not None else "BAC is zero"),
    ])

    cpi_why = None if cpi else ("CPI is not computable because AC is zero" if cpi is None
                                else "CPI is zero because EV is zero, so BAC / CPI has no value")
    spi_why = None if spi else ("SPI is not computable because PV is zero" if spi is None
                                else "SPI is zero because EV is zero, so the divisor has no value")
    forecasts = [("EAC at the present CPI", "EAC = BAC / CPI", bac / cpi if cpi else None,
                  C_EAC + "; " + C_T71 + "; " + C_44,
                  "The cumulative CPI to date continues for all remaining work.", cpi_why)]
    forecasts.append(("EAC at the budgeted rate", "EAC = AC + (BAC - EV)", ac + (bac - ev),
                      C_EAC + "; " + C_T71,
                      "All remaining work is done at the budgeted rate, so the variance to date is accepted and "
                      "not repeated. PMBOK 6 says that when performance so far is unfavorable, assuming it will "
                      "improve should be accepted only when supported by project risk analysis.", None))
    both = None if not cpi or not spi else ac + (bac - ev) / (cpi * spi)
    forecasts.append(("EAC with CPI and SPI", "EAC = AC + [(BAC - EV) / (CPI x SPI)]", both,
                      C_EAC + "; " + C_T71 + "; " + C_44,
                      "Remaining work runs at an efficiency set by both indexes; most useful when the schedule "
                      "drives the remaining effort. PMBOK 6 says variants weight CPI and SPI by judgment (for "
                      "example 80/20 or 50/50); the book prints no weighted formula, so none is computed.",
                      cpi_why or spi_why))
    if bottom_up_etc is not None:
        need("bottom-up ETC", bottom_up_etc, nonneg=True)
        forecasts.append(("EAC bottom-up", "EAC = AC + bottom-up ETC", ac + bottom_up_etc,
                          C_EAC_BU + "; " + C_T71,
                          "The original plan is no longer valid and the remaining work was re-estimated from "
                          "the bottom up (the ETC you supplied).", None))
    if approved_eac is not None:
        need("approved EAC", approved_eac, nonneg=True)
        forecasts.append(("EAC approved", "EAC supplied by you", approved_eac, C_TCPI,
                          "An approved EAC may replace the BAC in the TCPI calculation (" + C_TCPI + ").", None))

    fc_rows = []
    for name, formula, eac, cite, assumption, why in forecasts:
        etc = None if eac is None else eac - ac
        vac = None if eac is None else bac - eac
        tcpi = None
        tcpi_why = None
        if eac is not None:
            tcpi, tcpi_why = tcpi_value(bac - ev, eac - ac, "EAC - AC")
        circular = TCPI_CIRCULAR.get(name)
        fc_rows.append(section(name, [
            row("EAC", eac, formula, cite, assumption=assumption, why=why),
            row("ETC", etc, "ETC = EAC - AC", C_T71, why=why),
            row("VAC", vac, "VAC = BAC - EAC", C_EVA + "; " + C_T71,
                None if vac is None else sign_word(vac, *cost_state), why=why),
            row("TCPI to this EAC", tcpi, "TCPI = (BAC - EV) / (EAC - AC)", C_TCPI + "; " + C_T71 + "; " + C_44,
                None if circular else tcpi_state(tcpi), assumption=circular, why=tcpi_why or why),
        ]))

    tcpi_bac, tcpi_bac_why = tcpi_value(bac - ev, bac - ac, "BAC - AC")
    to_bac = section("TCPI to complete on plan", [
        row("TCPI to BAC", tcpi_bac, "TCPI = (BAC - EV) / (BAC - AC)", C_TCPI + "; " + C_T71 + "; " + C_44,
            tcpi_state(tcpi_bac), "Work remaining divided by funds remaining against the BAC.", why=tcpi_bac_why)])

    overrun = overrun_section(bac, pv, ev, ac, forecasts, threshold, bases or ["bac"])
    notes.append("Rounding is not stated in either book. Report an index as printed here (four decimals) and money "
                 "to whole currency units. A two-decimal figure may sit beside the printed one but never replaces "
                 "it, and a threshold is compared with the unrounded figure.")
    notes.append("Quote the Table 7-1 words printed beside each result (over planned cost, behind schedule, harder "
                 "to complete); do not turn them into 'over budget'. With cumulative figures only, fill the "
                 "cumulative column of form 4.4 and leave the period columns empty (" + C_44 + ").")
    notes.append("Choosing among the EACs is the project manager's call and has to be justified "
                 "(Book of Forms form 4.4, Table 4.4, PDF page 218 (printed page 207)). The blank form prints two "
                 "EAC rows, EAC w/CPI and EAC w/ CPI*SPI, then Selected EAC, Justification, and Explanation "
                 "(PDF page 219 (printed page 208)); the budgeted-rate or bottom-up figure has no printed row, so "
                 "write it and the reason in Selected EAC, Justification, and Explanation.")
    notes.append("Form 4.3 variance analysis gives no variance formula beyond 'calculate the variance' for "
                 "cost; percent variance is not stated in the book (" + C_43 + ").")
    return {"title": "Earned value analysis",
            "inputs": {"BAC": bac, "PV": pv, "EV": ev, "AC": ac, "bottom_up_etc": bottom_up_etc,
                       "approved_eac": approved_eac},
            "sections": [status, to_bac] + fc_rows + overrun, "notes": notes}


def overrun_section(bac, pv, ev, ac, forecasts, threshold, bases):
    """Overrun as a percent of a base the team names. No book prints a percent variance, so every row is
    labelled an outside arithmetic aid; the charter or the sponsor decides the base and the threshold."""
    if threshold is not None:
        need("threshold", threshold, nonneg=True)
    values = {"bac": bac, "pv": pv, "ev": ev, "ac": ac}
    items = [("Cost overrun to date (AC - EV)", ac - ev)]
    items += [("Forecast overrun, %s (EAC - BAC)" % name, None if eac is None else eac - bac)
              for name, _f, eac, _c, _a, _w in forecasts]
    sections = []
    for base in bases:
        denominator = values[base]
        rows_ = []
        for label, amount in items:
            if amount is None:
                rows_.append(row(label, None, "overrun / %s x 100" % base.upper(), NOT_STATED,
                                 why="the forecast is not computable"))
                continue
            pct = None if abs(denominator) < EPS else 100 * amount / denominator
            state = None
            if pct is not None and threshold is not None:
                state = ("beyond the %s%% threshold" % num(threshold) if pct > threshold + EPS
                         else "within the %s%% threshold" % num(threshold))
            rows_.append(row(label, pct, "overrun / %s x 100" % base.upper(), NOT_STATED, state,
                             assumption="Base %s = %s. %s." % (base.upper(), num(denominator), OUTSIDE_PERCENT)
                             if label.startswith("Cost") else None,
                             why=None if pct is not None else "%s is zero" % base.upper(), unit="%"))
        if threshold is not None:
            rows_.append(row("Threshold amount", threshold / 100 * denominator, "percent / 100 x %s" % base.upper(),
                             NOT_STATED, assumption="Base %s = %s. %s." % (base.upper(), num(denominator),
                                                                           OUTSIDE_PERCENT)))
        sections.append(section("Overrun as a percent of %s (outside arithmetic aid, not stated in the book)"
                                % base.upper(), rows_))
    return sections


TCPI_CIRCULAR = {
    "EAC at the present CPI": "By construction this equals the CPI (the EAC assumes the CPI continues), so it "
                              "measures the forecast, not the effort left against the BAC; the Table 7-1 words "
                              "are left off. Read the TCPI to BAC for that.",
    "EAC at the budgeted rate": "By construction this is 1 (the EAC assumes the remaining work costs what it "
                                "was budgeted), so it says nothing about the effort left; the Table 7-1 words "
                                "are left off. Read the TCPI to BAC for that.",
}


def tcpi_value(work, funds, funds_name):
    if funds <= EPS:
        return None, ("%s is zero or negative, so no funds remain; the book does not say how to read TCPI "
                      "then" % funds_name)
    return work / funds, None


def tcpi_state(v):
    if v is None:
        return None
    return sign_word(v - 1, "harder to complete", "same to complete", "easier to complete")


def pert(o, m, p):
    for name, value in (("o", o), ("m", m), ("p", p)):
        need(name, value, nonneg=True)
    notes = []
    if not o <= m <= p:
        notes.append("The inputs are not in the order optimistic <= most likely <= pessimistic; the books "
                     "define optimistic as the best case and pessimistic as the worst case.")
    cite_beta = "; ".join((C_BETA_DUR, C_BETA_COST, C_BETA_PM))
    notes.append("The Book of Forms says the project's needs decide the equation and calls beta the common "
                 "one (form 2.17, PDF page 84 (printed page 73)). PMBOK 6 uses the triangular equation when "
                 "there is insufficient historical data or the data is judgmental (" + C_TRI_DUR + ").")
    return {"title": "Three-point estimate",
            "inputs": {"optimistic": o, "most_likely": m, "pessimistic": p},
            "sections": [section("Expected value", [
                row("Beta mean", (o + 4 * m + p) / 6, "tE = (tO + 4 tM + tP) / 6", cite_beta,
                    assumption="Beta distribution weighting; most likely counts four times."),
                row("Triangular mean", (o + m + p) / 3, "tE = (tO + tM + tP) / 3",
                    C_TRI_DUR + "; " + C_BETA_PM,
                    assumption="Triangular distribution; the three estimates count equally."),
                row("Standard deviation", None, NOT_STATED, "no formula printed in PMBOK 6 or the Book of Forms",
                    why=NOT_STATED + " (neither book prints a formula for it)"),
            ])], "notes": notes}


def effort_to_duration(effort, resources, availability, performance=None):
    performance_given = performance is not None
    if not performance_given:
        performance = 1.0
    need("effort hours", effort, positive=True)
    need("resources", resources, positive=True)
    need("availability", availability, positive=True)
    if availability > 1 + EPS:
        raise CalcError("availability is above 100 percent")
    need("performance factor", performance, positive=True)
    divisor = resources * availability * performance
    notes = [
        "Performance factor: an average resource is 1.0, a highly skilled one 0.8, a less skilled one 1.2; "
        "the more skilled the resource, the lower the factor (" + C_217 + ").",
        "The book also says most people are productive on project work only about 75 percent of the time "
        "(" + C_217_NOTE + "). The equation has no separate term for it; the book does not say to fold it "
        "into percent available, and its worked example uses 75 percent as availability.",
        "The duration is in the unit of the effort (hours if hours were entered); converting to calendar "
        "time is not stated in the book.",
        "The printed equation divides by the performance factor, so a factor below 1.0 gives a longer duration "
        "than 1.0 (the book's own example: 150 / (2 x .75 x .8) = 125 hours, where 1.0 would give 100), while "
        "its prose says a highly skilled resource gets the work done faster and tells you to multiply the "
        "effort hours by the factor (" + C_217 + "). The two readings disagree; this tool follows the printed "
        "equation and example, and the book does not say which reading is meant.",
    ]
    if not performance_given:
        notes.insert(0, "No performance factor given: 1.0 was used, the book's average resource (" + C_217 + ").")
    return {"title": "Parametric duration from effort",
            "inputs": {"effort": effort, "resources": resources, "availability": availability,
                       "performance_factor": performance},
            "sections": [section("Duration", [
                row("Resource capacity factor", divisor, "quantity x percent available x performance factor",
                    C_217),
                row("Duration estimate", effort / divisor,
                    "Effort / (quantity x percent available x performance factor) = duration", C_217),
            ])], "notes": notes}


def analogous(previous_value, previous_size, current_size):
    need("previous value", previous_value, nonneg=True)
    need("previous size", previous_size, positive=True)
    need("current size", current_size, nonneg=True)
    mult = current_size / previous_size
    return {"title": "Analogous estimate",
            "inputs": {"previous_value": previous_value, "previous_size": previous_size,
                       "current_size": current_size},
            "sections": [section("Estimate", [
                row("Multiplier", mult, "current activity / previous activity", C_217 + "; " + C_221_AN),
                row("Estimate", previous_value * mult, "previous duration or cost x multiplier",
                    C_217 + "; " + C_221_AN,
                    assumption="The previous work is similar in fact; the book calls this a high-level "
                               "estimate for when detailed information is not available, and says factors such "
                               "as complexity or price increases can be added (not quantified in the book)."),
            ])], "notes": []}


def bottom_up(labor_hours, labor_rate, material=None, supplies=None, equipment=None, travel=None,
              other_direct=None, indirect=None, reserve=None):
    need("labor hours", labor_hours, nonneg=True)
    need("labor rate", labor_rate, nonneg=True)
    parts = [("Material", material), ("Supplies", supplies), ("Equipment", equipment), ("Travel", travel),
             ("Other direct costs", other_direct), ("Indirect costs", indirect), ("Reserve", reserve)]
    for name, value in parts:
        if value is not None:
            need(name.lower(), value, nonneg=True)
    labor = labor_hours * labor_rate
    total = labor + sum(v for _n, v in parts if v is not None)
    omitted = [n for n, v in parts if v is None]
    notes = ["Reserve is the contingency reserve cost for the work package (" + C_221_BU + ")."]
    if omitted:
        notes.append("Not supplied and counted as zero: %s." % ", ".join(omitted))
    return {"title": "Bottom-up cost estimate",
            "inputs": {"labor_hours": labor_hours, "labor_rate": labor_rate,
                       **{n.lower().replace(" ", "_"): v for n, v in parts}},
            "sections": [section("Estimate", [
                row("Total labor", labor, "labor hours x labor rate", C_221_BU),
                row("Estimate", total,
                    "labor + material + supplies + equipment + travel + other direct + indirect + reserve",
                    C_221_BU + "; " + C_BU_PM),
            ])], "notes": notes}


def parse_level(text, name):
    key = str(text).strip().lower()
    if key in LEVEL_ALIASES:
        return LEVEL_ALIASES[key]
    raise CalcError("%s: %r is not a level; use very low, low, medium, high, very high (or VL, L, M, H, VH)"
                    % (name, text))


def probability_level(text):
    """A probability as a level word, or as a whole percent (35%) placed in a Table 2.31 band."""
    raw = str(text).strip()
    if not raw.endswith("%"):
        return parse_level(raw, "probability")
    pct = parse_number(raw[:-1], "probability")
    if pct != int(pct):
        raise CalcError("probability: the book's bands are whole percents (1 to 20, 21 to 40, and so on), "
                        "got %s%%; %s (%s)" % (raw[:-1], NOT_STATED, C_231_P))
    pct = int(pct)
    if pct == 80:
        raise CalcError("probability: 80 percent is printed in two bands, 'High: 61 to 80' and 'Very High: "
                        "80 percent or greater' (%s); give the level word" % C_231_P)
    if pct > 80:
        return 4 if pct <= 100 else _outside(raw)
    for index, (low, high) in enumerate(PROB_BANDS):
        if low <= pct <= high:
            return index
    return _outside(raw)


def _outside(raw):
    raise CalcError("probability: %s is outside the bands Table 2.31 prints (1 percent up to 100 percent) (%s)"
                    % (raw, C_231_P))


def rating(p, i):
    """Overall rating of one probability and one impact on a single objective, from Table 2.31.

    p and i are 0 (very low) to 4 (very high). Table 2.31's rules about a medium
    score on more than two objectives need several objectives and are not used.
    """
    if (p >= 2 and i == 4) or (p >= 3 and i >= 3) or (p == 4 and i >= 2):
        return "High"
    if ((p == 0 and i >= 3) or (p == 1 and i >= 2) or (p == 2 and 1 <= i <= 3)
            or (p == 3 and i <= 2) or (p == 4 and i <= 1)):
        return "Medium"
    return "Low"


def rating_grid():
    """Rows probability very high down to very low, columns impact very low to very high."""
    return [[rating(p, i) for i in range(5)] for p in range(4, -1, -1)]


def score_product(p_text, i_text):
    return Decimal(str(p_text)) * Decimal(str(i_text))


def figure_round(value):
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def figure_grid():
    return [[figure_round(score_product(FIG_PROBABILITY[p], FIG_IMPACT[i])) for i in range(5)]
            for p in range(4, -1, -1)]


def risk_score(probability, impact, scale):
    cite_axes = ("The printed form 2.35 prints no axis titles and no legend for its three grey tones (%s). "
                 "Probability down the side and impact along the bottom is a convention; the grid is the same "
                 "either way round, and its tones match the High, Medium and Low rules of Table 2.31 "
                 "(%s)." % (C_235, C_231))
    if scale == "rating":
        p = probability_level(probability)
        i = parse_level(impact, "impact")
        result = rating(p, i)
        notes = [cite_axes,
                 "Rules about a medium impact on more than two objectives need several objectives and are not "
                 "applied to one probability and one impact. Impact definitions differ by objective "
                 "(" + C_231_P + ")."]
        if str(probability).strip().endswith("%"):
            notes.append("Percent placed in the Table 2.31 band: 1 to 20 very low, 21 to 40 low, 41 to 60 "
                         "medium, 61 to 80 high, 80 or greater very high (" + C_231_P + ").")
        return {"title": "Risk rating (Book of Forms 2.34 and 2.35)",
                "inputs": {"probability": probability, "impact": impact, "scale": scale},
                "sections": [section("Rating", [
                    row("Probability level", LEVEL_NAMES[p], "level word, or Table 2.31 percent band", C_231_P),
                    row("Impact level", LEVEL_NAMES[i], "level word", C_231_P),
                    row("Risk rating", result, "High, Medium or Low by the Table 2.31 rules", C_231,
                        assumption="One objective at a time; the book rates each objective's impact."),
                ])], "notes": notes}
    if scale == "pmbok":
        p_text = FIG_PROBABILITY[parse_level(probability, "probability")] if _is_level(probability) else \
            _probability_text(probability)
        i_text = FIG_IMPACT[parse_level(impact, "impact")] if _is_level(impact) else \
            _numeric_text(impact, "impact")
        score = score_product(p_text, i_text)
        return {"title": "Probability-impact score (PMBOK 6 Figure 11-5)",
                "inputs": {"probability": probability, "impact": impact, "scale": scale},
                "sections": [section("Score", [
                    row("Probability value", float(Decimal(p_text)), "level word mapped by Figure 11-5, or your number",
                        C_FIG115),
                    row("Impact value", float(Decimal(i_text)), "level word mapped by Figure 11-5, or your number",
                        C_FIG115),
                    row("Score", float(score), "probability x impact", C_MATRIX_PM + "; " + C_FIG115,
                        assumption="Where numeric values are used they can be multiplied to give a "
                                   "probability-impact score. The figure prints two decimals (%s)."
                                   % figure_round(score)),
                ])],
                "notes": ["The Figure 11-5 values are the book's example scale (very low to very high "
                          "probability 0.10, 0.30, 0.50, 0.70, 0.90; negative impact 0.05, 0.10, 0.20, 0.40, "
                          "0.80). The book prints no score cut-off between its shaded bands (" + C_FIG115 + ")."]}
    p_text = _probability_text(probability)
    i = parse_level(impact, "impact")
    score = score_product(p_text, DOUBLING_IMPACT[i])
    return {"title": "Probability-impact score, doubling impact scale (Book of Forms 2.35 tailoring tip)",
            "inputs": {"probability": probability, "impact": impact, "scale": scale},
            "sections": [section("Score", [
                row("Impact value", float(Decimal(DOUBLING_IMPACT[i])),
                    "Very Low .5, Low 1, Medium 2, High 4, Very High 8", C_235_TIP),
                row("Score", float(score), "probability x impact value", C_235_TIP + "; " + C_MATRIX_PM,
                    assumption="The form 2.35 tip gives the doubling impact values only; multiplying by a "
                               "probability number is the PMBOK 6 convention, and the Book of Forms prints no "
                               "probability numbers for this scheme."),
            ])], "notes": ["Objective weights (for example schedule 40 percent, the others 20 percent each, "
                           "totalling 100 percent) are mentioned in the same tip, but the book gives no formula "
                           "for combining them, so none is computed (" + C_235_TIP + ")."]}


def _is_level(text):
    return str(text).strip().lower() in LEVEL_ALIASES


def _probability_text(text):
    """A numeric probability as exact decimal text: 0.3 or 30%, between 0 and 1."""
    raw = str(text).replace(",", "").strip()
    parse_share(raw, "probability")
    if raw.endswith("%"):
        return str(Decimal(raw[:-1].strip()) / 100)
    return str(Decimal(raw))


def _numeric_text(text, name):
    value = parse_number(text, name)
    if value < 0:
        raise CalcError("%s must not be negative" % name)
    return str(text).replace(",", "").strip()


def matrix(scale):
    if scale == "pmbok":
        grid = figure_grid()
        header = ["Probability"] + ["%s %s" % (LEVEL_NAMES[i] if i != 2 else "Moderate", FIG_IMPACT[i])
                                    for i in range(5)]
        body = [["%s %s" % (LEVEL_NAMES[p], FIG_PROBABILITY[p])] + [str(c) for c in grid[4 - p]]
                for p in range(4, -1, -1)]
        notes = ["Threats half of the figure; the opportunities half repeats the same numbers with the impact "
                 "scale reversed (" + C_FIG115 + ")."]
        title = "PMBOK 6 Figure 11-5 scores, threats side"
    else:
        grid = rating_grid()
        header = ["Probability"] + list(LEVEL_NAMES)
        body = [[LEVEL_NAMES[p]] + grid[4 - p] for p in range(4, -1, -1)]
        notes = ["Cell text H, M, L is High, Medium, Low. The printed form shades the cells in three grey tones, "
                 "dark where this grid says High, mid for Medium, and the two lightest tones for Low (%s). "
                 "The printed form has no axis titles and no legend; probability down the side and impact "
                 "along the bottom is a convention that matches Table 2.31 (%s)." % (C_235, C_231)]
        body = [[r[0]] + [c[0] for c in r[1:]] for r in body]
        title = "Probability and impact matrix as the book shows it (form 2.35)"
    return {"title": title, "inputs": {"scale": scale}, "matrix": {"header": header, "rows": body},
            "sections": [], "notes": notes,
            "cite": C_235 + "; " + C_231 if scale == "rating" else C_FIG115}


def parse_probability(text):
    return parse_share(text, "probability")


def parse_outcome(token):
    prob, sep, value = str(token).partition(":")
    if not sep:
        raise CalcError("outcome %r must look like probability:value, for example 0.6:80 or 60%%:80" % token)
    return parse_probability(prob), parse_number(value, "outcome value")


def emv(outcomes, options):
    if not outcomes and not options:
        raise CalcError("give --outcome probability:value, or --option NAME COST probability:payoff ...")
    sections = []
    notes = ["EMV of a branch is each outcome's probability times its value, added up; the book prints it as "
             "'$36M = .60 ($80M) + .40 (-$30M)' with net path value equal to payoffs minus costs along the "
             "path (" + C_TREE + ")."]

    def check(probs, label):
        total = sum(probs)
        if abs(total - 1) > 1e-6:
            notes.append("%s: probabilities add to %s, not 1; the book's example chance nodes add to 100 "
                         "percent and it states no rule for other cases." % (label, total))

    if outcomes:
        probs = [p for p, _v in outcomes]
        check(probs, "Outcomes")
        sections.append(section("Expected monetary value", [
            row("EMV", sum(p * v for p, v in outcomes), "EMV = sum of probability x value", C_TREE)]))
    if options:
        results = []
        for name, cost, outs in options:
            check([p for p, _v in outs], name)
            paths = [(p, v - cost) for p, v in outs]
            results.append((name, sum(p * n for p, n in paths), paths))
            sections.append(section("Option %s (investment %s)" % (name, num(cost)), [
                row("Net path value %d" % (k + 1), n, "payoff - investment", C_TREE)
                for k, (_p, n) in enumerate(paths)] + [
                row("EMV of %s" % name, results[-1][1], "sum of probability x net path value", C_TREE)]))
        best = max(r[1] for r in results)
        winners = [r[0] for r in results if abs(r[1] - best) < EPS]
        decision = ("Decision EMV = %s, the larger EMV, option %s." % (num(best), winners[0]) if len(winners) == 1
                    else "Options %s tie on EMV %s; the book states no tie rule." % (", ".join(winners), num(best)))
        sections.append(section("Decision", [row("Decision EMV", best, "the larger of the option EMVs", C_TREE,
                                                  status=decision)]))
        notes.append("The book's example takes the larger EMV as the decision and remarks that this choice is "
                     "also the lower-risk one, since it avoids the worst-case loss (" + C_TREE + ").")
    return {"title": "Expected monetary value", "inputs": {"outcomes": outcomes, "options": [
        {"name": n, "investment": c, "outcomes": o} for n, c, o in options]},
            "sections": sections, "notes": notes}


def weighted_score(weights, candidates, names, scale_max):
    if not weights:
        raise CalcError("give --weights")
    if not candidates:
        raise CalcError("give --scores at least once")
    total_weight = sum(weights)
    if abs(total_weight - 100) > 1e-6:
        raise CalcError("weights add to %s percent; the book says the sum of all the criteria must equal "
                        "100 percent (%s)" % (num(total_weight), C_239))
    if any(w < 0 for w in weights):
        raise CalcError("weights must not be negative")
    if names and len(names) != len(candidates):
        raise CalcError("--names has %d names for %d --scores lists" % (len(names), len(candidates)))
    labels = names or ["Candidate %d" % (k + 1) for k in range(len(candidates))]
    sections = []
    totals = []
    for label, scores in zip(labels, candidates):
        if len(scores) != len(weights):
            raise CalcError("%s has %d ratings for %d weights" % (label, len(scores), len(weights)))
        for s in scores:
            need("rating", s, nonneg=True)
        if scale_max is not None:
            for s in scores:
                if not 1 <= s <= scale_max:
                    raise CalcError("%s: rating %s is outside the 1 to %s range chosen for the criteria (%s)"
                                    % (label, num(s), num(scale_max), C_239))
        parts = [w / 100 * s for w, s in zip(weights, scores)]
        totals.append(sum(parts))
        sections.append(section(label, [
            row("Score for criterion %d" % (k + 1), part, "weight x rating", C_239)
            for k, part in enumerate(parts)] + [row("Total", totals[-1], "sum of the scores", C_239)]))
    notes = ["The weight is used as a fraction of 1 (30 percent is 0.30), so a total sits on the rating scale; "
             "the book says only 'multiply the weight times the rating' and does not print the unit (" + C_239 + ")."]
    if len(totals) > 1:
        best = max(totals)
        winners = [l for l, t in zip(labels, totals) if abs(t - best) < EPS]
        if len(winners) == 1:
            notes.append("Highest total score wins the bid: %s with %s (%s)." % (winners[0], num(best), C_239))
        else:
            notes.append("%s tie on %s; the book states no tie rule." % (", ".join(winners), num(best)))
    return {"title": "Source selection weighted score",
            "inputs": {"weights_percent": weights, "ratings": candidates, "names": labels,
                       "rating_scale_max": scale_max},
            "sections": sections, "notes": notes}


def comms_channels(people):
    if people != int(people) or people < 1:
        raise CalcError("people must be a whole number of at least 1")
    n = int(people)
    channels = n * (n - 1) // 2
    return {"title": "Communication channels",
            "inputs": {"people": n},
            "sections": [section("Channels", [
                row("Channels", channels, "n x (n - 1) / 2", NOT_STATED + "; PMBOK 6 section 10.1.2.2 lists "
                    "the number of potential channels as a source for communication requirements but prints "
                    "no formula (" + C_CHAN + ")",
                    assumption="Counts one-to-one paths between n people, each pair once. The book names "
                               "one-to-many and many-to-many paths as well and prints no count for them.")])],
            "notes": ["This is plain pair counting, not a formula either book prints (searched PMBOK 6 and "
                      "the Book of Forms); cite it as such."]}


def earned_schedule(es, at):
    need("es", es, nonneg=True)
    need("at", at, positive=True)
    sv_t = es - at
    spi_t = es / at
    state = ("ahead of schedule", "on schedule", "behind schedule")
    return {"title": "Earned schedule",
            "inputs": {"ES": es, "AT": at},
            "sections": [section("Time-based schedule measures (same time unit for ES and AT)", [
                row("SV(t)", sv_t, "SV(t) = ES - AT", C_ES,
                    sign_word(sv_t, *state), unit="time units"),
                row("SPI(t)", spi_t, "SPI(t) = ES / AT", C_ES,
                    sign_word(spi_t - 1, *state))])],
            "notes": ["Earned schedule is a trend the book names; PMBOK 6 gives these two equations and says the "
                      "theory also forecasts the completion date from earned schedule, actual time and estimated "
                      "duration, but prints no such formula, so none is computed (" + C_ES + ").",
                      "ES is an input. The book as printed on that page does not say how to read it off the planned "
                      "value curve; the team states its reading.",
                      "Earned schedule is a trend, not a PMBOK 6 requirement; use it beside SV and SPI of the evm "
                      "subcommand, not instead of them."]}


def velocity(completed, remaining=None):
    if not completed:
        raise CalcError("give the story points completed in at least one iteration")
    for v in completed:
        need("completed points", v, nonneg=True)
    rows_ = [row("Iteration %d" % (k + 1), v, "velocity = sum of the story point sizes of the features actually "
                 "completed in the iteration", C_VEL, unit="points") for k, v in enumerate(completed)]
    mean = sum(completed) / len(completed)
    sections = [section("Velocity per iteration", rows_),
                section("Plan from history (outside arithmetic aid)", [
                    row("Average velocity", mean, "sum of the velocities / number of iterations", NOT_STATED +
                        "; the Guide says a team plans its next capacity by looking at its historical performance "
                        "(" + C_VEL + ")", unit="points per iteration")])]
    notes = []
    if len(completed) < 4:
        notes.append("Only %d iteration%s given. The Guide says it can take four to eight iterations to achieve a "
                     "stable velocity (%s); treat the average as a rough guide." %
                     (len(completed), "" if len(completed) == 1 else "s", C_VEL))
    if remaining is not None:
        need("remaining points", remaining, nonneg=True)
        if mean > EPS:
            sections[1]["rows"].append(row(
                "Iterations remaining", remaining / mean, "remaining points / average velocity",
                NOT_STATED + "; worked example, not an equation: about 500 points left at 50 points an iteration is "
                "about 10 iterations (" + C_VEL_EX + ")", unit="iterations",
                assumption="Scope and velocity stay as they are; a burnup shows scope change."))
        else:
            sections[1]["rows"].append(row("Iterations remaining", None, "remaining points / average velocity",
                                           NOT_STATED, why="average velocity is zero"))
    notes.append("Velocity is the team's own capacity measure. Relative estimates cannot be compared across teams "
                 "or added across teams (Agile Practice Guide, printed page 67 (PDF page 877)).")
    return {"title": "Velocity", "inputs": {"completed": completed, "remaining": remaining},
            "sections": sections, "notes": notes}


def cd3(items):
    if not items:
        raise CalcError("give at least one --item NAME COST_OF_DELAY DURATION")
    scored = []
    for name, delay, duration in items:
        need("cost of delay for %s" % name, delay, nonneg=True)
        need("duration of %s" % name, duration, positive=True)
        scored.append((name, delay, duration, delay / duration))
    ranked = sorted(scored, key=lambda t: -t[3])
    rows_ = [row("%d. %s" % (k + 1, n), v, "CD3 = cost of delay / duration", C_CD3 +
                 "; the Guide prints the words and no units or scale",
                 assumption="cost of delay %s over duration %s, both as the product owner supplied them" %
                            (num(d), num(t))) for k, (n, d, t, v) in enumerate(ranked)]
    notes = ["The Guide names ranking by cost of delay divided by duration (CD3) 'and other value models'; the "
             "cost of delay and the duration come from the product owner and team, in one unit each, and the "
             "book does not say how to estimate them (" + C_CD3 + ")."]
    ties = [n for n, _d, _t, v in ranked if abs(v - ranked[0][3]) < EPS]
    if len(ties) > 1:
        notes.append("%s tie on %s; the book states no tie rule." % (", ".join(ties), num(ranked[0][3])))
    return {"title": "Cost of delay divided by duration (CD3)",
            "inputs": {"items": [(n, d, t) for n, d, t in items]},
            "sections": [section("Highest first", rows_)], "notes": notes}


def payback(investment, nets):
    need("investment", investment, positive=True)
    if not nets:
        raise CalcError("give the net benefit of each period with --net")
    cumulative, running, first = [], 0.0, None
    for k, v in enumerate(nets):
        if not math.isfinite(v):
            raise CalcError("net benefit must be a finite number")
        running += v
        cumulative.append(running)
        if first is None and running + EPS >= investment:
            first = k + 1
    rows_ = [row("Period %d" % (k + 1), "net %s, cumulative %s" % (num(v), num(c)),
                 "cumulative net benefit = sum of the net benefits so far", NOT_STATED + "; " + C_PAYBACK)
             for k, (v, c) in enumerate(zip(nets, cumulative))]
    summary = row("Payback period", first if first is not None else "not reached in the periods given",
                  "first period in which the cumulative net benefit reaches the investment",
                  NOT_STATED + "; " + C_PAYBACK, unit="periods" if first is not None else "",
                  assumption="Whole periods only; interpolating inside a period is a convention neither book states, "
                             "so it is not computed. Net benefits are undiscounted.")
    return {"title": "Payback period",
            "inputs": {"investment": investment, "net_benefits": nets},
            "sections": [section("Cumulative net benefit", rows_), section("Result", [summary])],
            "notes": ["PMBOK 6 names payback analysis (" + C_PAYBACK + ") and prints no equation, and the Book of "
                      "Forms does not mention it. This is an outside arithmetic aid: label it so, and list the "
                      "inputs and where each came from."]}


def reserve(contingency, used, risks):
    need("contingency reserve", contingency, nonneg=True)
    need("used to date", used, nonneg=True)
    if used > contingency + EPS:
        raise CalcError("used to date is above the contingency reserve: check the inputs or the draws made")
    remaining = contingency - used
    rows_, expected, worst = [], 0.0, 0.0
    for name, prob, impact in risks:
        need("impact of %s" % name, impact, nonneg=True)
        expected += prob * impact
        worst += impact
        rows_.append(row(name, prob * impact, "probability x impact = %s x %s" % (num(prob), num(impact)),
                         "PMBOK 6 section 11.4.2.5, printed page 435 (PDF page 474)"))
    result = [
        row("Contingency reserve remaining", remaining, "reserve - used to date", C_RESERVE),
        row("Expected value of the open risks", expected, "sum of probability x impact", NOT_STATED + "; " + C_RESERVE,
            assumption="Probability and impact come from the team's own register; the book names no way to size a "
                       "reserve from the sum."),
        row("Remaining minus expected value", remaining - expected, "remaining reserve - expected value",
            NOT_STATED + "; " + C_RESERVE,
            sign_word(remaining - expected, "reserve above the expected value", "reserve equals the expected value",
                      "reserve below the expected value")),
        row("Remaining minus the full impact of every open risk", remaining - worst,
            "remaining reserve - sum of impacts", NOT_STATED + "; " + C_RESERVE,
            assumption="Every open risk occurring at full impact; a bound, not a forecast."),
    ]
    return {"title": "Reserve analysis, remaining contingency against remaining risk",
            "inputs": {"contingency": contingency, "used": used, "open_risks": len(risks)},
            "sections": [section("Open risks", rows_), section("Remaining reserve against remaining risk", result)],
            "notes": ["PMBOK 6 says reserve analysis compares the contingency reserve remaining with the risk "
                      "remaining at any time to decide whether the remaining reserve is adequate, and that it may "
                      "be shown as a burndown chart (" + C_RESERVE + "). It prints no rule for adequate, no ratio "
                      "and no equation, so this is an outside arithmetic aid and the judgment is the team's.",
                      "Closed or avoided risks leave the open list; a risk that occurred is an issue and its cost "
                      "is a draw on the reserve (used to date), not an open risk."]}


def funding(tranches, spent, through, total=None):
    if not tranches:
        raise CalcError("give the funding tranches with --tranche NAME=AMOUNT, in release order")
    need("spent", spent, nonneg=True)
    names = [n for n, _v in tranches]
    if len(set(names)) != len(names):
        raise CalcError("a tranche name is given twice")
    if through not in names:
        raise CalcError("--through %r is not one of the tranches: %s" % (through, ", ".join(names)))
    cumulative, running, rows_, released = {}, 0.0, [], None
    for name, amount in tranches:
        need("tranche %s" % name, amount, nonneg=True)
        running += amount
        cumulative[name] = running
        rows_.append(row(name, running, "cumulative funds released = sum of the tranches so far", C_FUNDING,
                         assumption=None))
        if name == through:
            released = running
    result = [
        row("Funds released through %s" % through, released, "cumulative tranches", C_FUNDING),
        row("Actual cost to date", spent, "as supplied", C_FUNDING),
        row("Released minus spent", released - spent, "funds released - actual cost", NOT_STATED + "; " + C_FUNDING,
            sign_word(released - spent, "funds released exceed cost to date", "funds exactly used",
                      "cost to date exceeds the funds released")),
    ]
    notes = ["PMBOK 6 says funding often occurs in incremental amounts that may not be evenly distributed and shows "
             "them as steps against the cost baseline (" + C_FUNDING + "). Comparing the steps with actual cost is "
             "an outside arithmetic aid; the book prints no equation."]
    if total is not None:
        need("total funding", total, positive=True)
        if abs(running - total) > 0.5:
            notes.append("The tranches add to %s, not the stated total %s; check them against the charter." % (
                num(running), num(total)))
    return {"title": "Funding released against cost to date",
            "inputs": {"through": through, "spent": spent, "total": total},
            "sections": [section("Tranches in release order", rows_), section("Comparison", result)], "notes": notes}


def response_effectiveness(options):
    if not options:
        raise CalcError("give at least one --option NAME IMPACT_BEFORE IMPACT_AFTER COST")
    rows_ = []
    for name, before, after, cost in options:
        need("impact before of %s" % name, before, nonneg=True)
        need("impact after of %s" % name, after, nonneg=True)
        need("cost of %s" % name, cost, positive=True)
        rows_.append(row(name, (before - after) / cost,
                         "(impact before - impact after) / implementation cost = (%s - %s) / %s" % (
                             num(before), num(after), num(cost)), C_RESPONSE,
                         assumption="Impact before and after are the team's own levels or amounts, in one unit."))
    return {"title": "Cost effectiveness of risk responses",
            "inputs": {"options": len(options)}, "sections": [section("Change in impact level per unit of cost", rows_)],
            "notes": ["The ratio of (change in impact level) divided by (implementation cost) gives the cost "
                      "effectiveness of a response, a higher ratio being more effective, when the impact can be "
                      "quantified in money (" + C_RESPONSE + "). The book gives no threshold and no weighting "
                      "against timing or secondary risks, so choosing among the options is judgment."]}


C_CRASH = "PMBOK 6 section 6.5.2.6, printed page 215 (PDF page 254)"


def crash(options, needed=None):
    """Rank crashing options by extra cost per day saved. Outside arithmetic aid."""
    if not options:
        raise CalcError("give at least one --option NAME NORMAL_DAYS CRASHED_DAYS EXTRA_COST")
    rows_, ranked = [], []
    for name, normal, crashed, extra in options:
        need("normal days of %s" % name, normal, positive=True)
        need("crashed days of %s" % name, crashed, nonneg=True)
        need("extra cost of %s" % name, extra, nonneg=True)
        saved = normal - crashed
        if saved <= EPS:
            raise CalcError("%s: crashed days must be fewer than normal days" % name)
        ranked.append((extra / saved, name, saved, extra))
    ranked.sort()
    total_days, total_cost = 0.0, 0.0
    for per_day, name, saved, extra in ranked:
        rows_.append(row(name, per_day, "extra cost / days saved", NOT_STATED,
                         assumption="Saves %s days for %s extra." % (num(saved), num(extra)),
                         unit="per day saved"))
    plan_rows = []
    if needed is not None:
        need("days needed", needed, positive=True)
        for per_day, name, saved, extra in ranked:
            if total_days >= needed - EPS:
                break
            total_days += saved
            total_cost += extra
            plan_rows.append(row(name, total_days, "cumulative days saved, cheapest first", NOT_STATED,
                                 assumption="Cumulative extra cost %s." % num(total_cost), unit="days"))
        reached = total_days >= needed - EPS
        plan_rows.append(row("Days needed" + ("" if reached else " (not reached)"), needed,
                             "taken from the cheapest option up", NOT_STATED,
                             assumption=None if reached else "Every option together saves %s days." % num(total_days),
                             unit="days"))
    sections = [section("Options ranked by extra cost per day saved (outside arithmetic aid)", rows_)]
    if plan_rows:
        sections.append(section("Cheapest first until the days needed are saved", plan_rows))
    return {"title": "Crashing options",
            "inputs": {"options": [o[0] for o in options], "days_needed": needed},
            "sections": sections,
            "notes": ["Outside arithmetic aid: " + C_CRASH + " defines crashing as shortening the schedule for the "
                      "least incremental cost by adding resources, and prints no equation. Only activities on the "
                      "critical path shorten the project (crashing works only for those); the tool does not know "
                      "which activities are critical, so give it only critical ones, found with cpm.",
                      "The book says crashing does not always produce a viable alternative and may increase risk "
                      "or cost; the tool has no risk term. The crashed duration and the extra cost are the team's "
                      "figures from a quote or a resource plan (more resources on the same work), never an estimate "
                      "cut to fit. If no option closes the gap, the route is a change request (3.3) to the sponsor (team rule)."]}


LINK_TYPES = ("FS", "SS", "FF", "SF")


def parse_link(text):
    """'A,B' or 'A,B,SS' or 'A,B,SS,2' as (pred, succ, type, lag)."""
    parts = [t.strip() for t in str(text).split(",")]
    if len(parts) < 2 or len(parts) > 4 or not parts[0] or not parts[1]:
        raise CalcError("link %r: write PRED,SUCC or PRED,SUCC,TYPE or PRED,SUCC,TYPE,LAG (TYPE is one of %s)"
                        % (text, ", ".join(LINK_TYPES)))
    kind = (parts[2] if len(parts) > 2 and parts[2] else "FS").upper()
    if kind not in LINK_TYPES:
        raise CalcError("link %r: type %r is not one of %s" % (text, parts[2], ", ".join(LINK_TYPES)))
    lag = parse_number(parts[3], "lag") if len(parts) > 3 else 0.0
    return parts[0], parts[1], kind, lag


def parse_pair(text, name):
    left, sep, right = str(text).partition("=")
    if not sep or not left.strip():
        raise CalcError("%s %r: write NAME=VALUE" % (name, text))
    return left.strip(), parse_number(right, name)


def network_pass(durations, links, deadline=None):
    """Forward and backward pass. Times run from 0 as the start of day 1, so a result of f means the end of
    day f, which is the day-1 convention of PMBOK 6 Figure 6-16."""
    order, pending = [], {a: 0 for a in durations}
    out_links, in_links = {a: [] for a in durations}, {a: [] for a in durations}
    for p_, s_, kind, lag in links:
        for a in (p_, s_):
            if a not in durations:
                raise CalcError("link refers to %r, which is not an activity" % a)
        if p_ == s_:
            raise CalcError("activity %r is linked to itself" % p_)
        out_links[p_].append((s_, kind, lag))
        in_links[s_].append((p_, kind, lag))
        pending[s_] += 1
    ready = [a for a in durations if pending[a] == 0]
    while ready:
        a = ready.pop(0)
        order.append(a)
        for s_, _k, _l in out_links[a]:
            pending[s_] -= 1
            if pending[s_] == 0:
                ready.append(s_)
    if len(order) != len(durations):
        raise CalcError("the links form a loop among: %s" %
                        ", ".join(a for a in durations if a not in order))
    start, finish = {}, {}
    for a in order:
        d = durations[a]
        s_ = 0.0
        for p_, kind, lag in in_links[a]:
            if kind == "FS":
                s_ = max(s_, finish[p_] + lag)
            elif kind == "SS":
                s_ = max(s_, start[p_] + lag)
            elif kind == "FF":
                s_ = max(s_, finish[p_] + lag - d)
            else:
                s_ = max(s_, start[p_] + lag - d)
        start[a], finish[a] = s_, s_ + d
    end = max(finish.values())
    limit = end if deadline is None else deadline
    late_start, late_finish = {}, {}
    for a in reversed(order):
        d = durations[a]
        lf = limit
        for s_, kind, lag in out_links[a]:
            if kind == "FS":
                lf = min(lf, late_start[s_] - lag)
            elif kind == "SS":
                lf = min(lf, late_start[s_] - lag + d)
            elif kind == "FF":
                lf = min(lf, late_finish[s_] - lag)
            else:
                lf = min(lf, late_finish[s_] - lag + d)
        late_finish[a], late_start[a] = lf, lf - d
    free = {}
    for a in order:
        slacks = []
        for s_, kind, lag in out_links[a]:
            if kind == "FS":
                slacks.append(start[s_] - (finish[a] + lag))
            elif kind == "SS":
                slacks.append(start[s_] - (start[a] + lag))
            elif kind == "FF":
                slacks.append(finish[s_] - (finish[a] + lag))
            else:
                slacks.append(finish[s_] - (start[a] + lag))
        free[a] = min(slacks) if slacks else end - finish[a]
    return {"order": order, "es": start, "ef": finish, "ls": late_start, "lf": late_finish,
            "free": free, "end": end}


def parse_date(text, name):
    try:
        return datetime.date.fromisoformat(str(text).strip())
    except ValueError:
        raise CalcError("%s %r: write the date as YYYY-MM-DD" % (name, text))


def parse_breaks(items):
    """Each item is DATE or START:END (YYYY-MM-DD), a closed range of calendar days with no work."""
    spans = []
    for text in items:
        first, sep, last = str(text).partition(":")
        a = parse_date(first, "--holiday")
        b = parse_date(last, "--holiday") if sep else a
        if b < a:
            raise CalcError("--holiday %r ends before it starts" % text)
        spans.append((a, b))
    return spans


class WorkCalendar:
    """Working days are Monday to Friday outside the given breaks; day 1 is the first working day on or after
    the start date. An outside aid: neither book defines a calendar convention."""

    def __init__(self, start, spans):
        self.spans = spans
        self.days = []
        self.day = start

    def working(self, d):
        return d.weekday() < 5 and not any(a <= d <= b for a, b in self.spans)

    def date(self, number):
        number = max(1, int(round(number)))
        while len(self.days) < number:
            while not self.working(self.day):
                self.day += datetime.timedelta(1)
            self.days.append(self.day)
            self.day += datetime.timedelta(1)
        return self.days[number - 1]

    def number(self, d):
        """Working day number of the last working day on or before d, counted from day 1."""
        first = self.date(1)
        if d < first:
            raise CalcError("the deadline %s is before day 1 (%s)" % (d.isoformat(), first.isoformat()))
        count, day = 0, first
        while day <= d:
            if self.working(day):
                count += 1
            day += datetime.timedelta(1)
        return count

    def breaks_between(self, first, last):
        """Weekday break days that fall between two dates, as a list of (start, end) spans."""
        hit = []
        for a, b in self.spans:
            lo, hi = max(a, first), min(b, last)
            if lo <= hi and any((lo + datetime.timedelta(n)).weekday() < 5 for n in range((hi - lo).days + 1)):
                hit.append((lo, hi))
        return hit


def parse_deadline(text, start, spans):
    """A deadline as working days from day 1, or as a date converted with the start date and the breaks."""
    if text is None:
        return None
    try:
        return float(str(text).replace(",", ""))
    except ValueError:
        pass
    when = parse_date(text, "--deadline")
    if start is None:
        raise CalcError("--deadline %r is a date: give --start (the date of day 1), or write the deadline as "
                        "working days counted from day 1" % text)
    return float(WorkCalendar(start, spans).number(when))


def span_text(spans):
    return ", ".join(a.isoformat() if a == b else "%s to %s" % (a.isoformat(), b.isoformat()) for a, b in spans)


def cpm(activities, links, deadline=None, slip=None, start=None, holidays=None):
    if not activities:
        raise CalcError("give at least one --activity NAME=DURATION")
    durations = {}
    for name, d in activities:
        if name in durations:
            raise CalcError("activity %r is given twice" % name)
        need("duration of %s" % name, d, nonneg=True)
        durations[name] = d
    if deadline is not None:
        need("deadline", deadline, positive=True)
    base = network_pass(durations, links, deadline)
    slipped = None
    if slip:
        name, days = slip
        if name not in durations:
            raise CalcError("--slip refers to %r, which is not an activity" % name)
        need("slip", days, nonneg=True)
        changed = dict(durations)
        changed[name] += days
        slipped = network_pass(changed, links, deadline)

    def day(v):
        return v + 1

    table, rows_ = [], []
    least = min(base["lf"][a] - base["ef"][a] for a in durations)
    for a in sorted(durations, key=lambda x: (base["es"][x], base["order"].index(x))):
        total = base["lf"][a] - base["ef"][a]
        item = {"activity": a, "duration": durations[a], "ES": day(base["es"][a]), "EF": base["ef"][a],
                "LS": day(base["ls"][a]), "LF": base["lf"][a], "total_float": total,
                "free_float": base["free"][a], "critical": abs(total - least) < EPS}
        table.append(item)
        rows_.append(row(a, "ES %s  EF %s  LS %s  LF %s  total float %s  free float %s%s" % (
            num(item["ES"]), num(item["EF"]), num(item["LS"]), num(item["LF"]), num(total),
            num(base["free"][a]),
            ("  (critical)" if least <= EPS else "  (least total float)") if item["critical"] else ""),
            NOT_STATED, C_CPM + "; the book describes the passes and prints no equations"))
    path = [t["activity"] for t in table if t["critical"]]
    result_rows = [row("Project duration (early finish of the last activity)", base["end"],
                       "longest path through the network", C_CPM, unit="days"),
                   row("Critical path" if least <= EPS else "Path with the least total float", " - ".join(path),
                       "the longest path has the least total float, usually zero", C_CPM)]
    notes_head = ["Reading the rows: ES and EF come from the forward pass, LS and LF from the backward pass, "
                  "total float = LF - EF, free float = how far the activity can slip without moving any "
                  "successor's early date (PMBOK 6 section 6.5.2.2: total float is the delay from early start "
                  "that does not delay the project finish; free float is the delay that does not delay the early "
                  "start of any successor)."]
    notes = notes_head + ["This is an outside arithmetic aid: PMBOK 6 describes the forward and backward pass and shows "
             "Figure 6-16 (project starts on day 1, activity A of 5 days finishes on day 5, the critical path is "
             "A-C-D of 30 days) but prints no equations (" + C_CPM + "). Early and late dates are the periods in "
             "which an activity could run, with no resource limit, not the schedule itself.",
             "Link types FS, SS, FF, SF come from PMBOK 6 section 6.3.2.1, printed page 190 (PDF page 229); a "
             "positive lag delays the successor, a negative one is a lead. Times are working days; calendars are "
             "not modelled unless --start is given."]
    if deadline is not None:
        neg = [t["activity"] for t in table if t["total_float"] < -EPS]
        notes.append("A constraint of day %s on the finish was applied to the backward pass. Positive total float "
                     "comes from a constraint later than the early finish; negative total float means the "
                     "constraint is violated by duration and logic, and negative float analysis is the book's "
                     "technique for finding ways to bring the schedule back (PMBOK 6 section 6.5.2.2, printed page "
                     "210 (PDF page 249))." % num(deadline))
        if neg:
            notes.append("Negative total float on: %s." % ", ".join(neg))
    sections = [section("Dates in days, day 1 is the first working day", rows_), section("Result", result_rows)]
    calendar = None
    if start is not None:
        calendar = WorkCalendar(start, holidays or [])
        cal_rows = []
        for t in table:
            first = calendar.date(t["ES"])
            last = calendar.date(max(t["EF"], t["ES"]))
            cal_rows.append(row(t["activity"], "%s to %s" % (first.isoformat(), last.isoformat()),
                                "working day number mapped to a calendar date", NOT_STATED, assumption=None))
        end_date = calendar.date(base["end"])
        cal_rows.append(row("Project finish", end_date.isoformat(), "date of the last working day of the path",
                            NOT_STATED))
        sections.append(section("Calendar dates (outside arithmetic aid: Monday to Friday, breaks %s)" % (
            span_text(holidays) if holidays else "none given"), cal_rows))
        notes.append("Calendar dates map working-day numbers onto Monday to Friday outside the breaks you pass with "
                     "--holiday; day 1 is the first working day on or after %s. Public holidays, the length of a "
                     "break and a part-time person's own calendar are not known to the tool, so give each break "
                     "from the charter or the schedule and never from memory." % start.isoformat())
    if slipped:
        name, days = slip
        before = base["lf"][name] - base["ef"][name]
        after = slipped["lf"][name] - slipped["ef"][name]
        sections.append(section("What if %s runs %s days longer" % (name, num(days)), [
            row("Project finish moves by", slipped["end"] - base["end"], "new longest path - old longest path",
                C_CPM, unit="days",
                assumption="Only the duration of %s changes; the links, calendars and constraint stay." % name),
            row("Total float of %s before and after" % name, "%s then %s" % (num(before), num(after)),
                "LF - EF", C_CPM)]))
        if after < -EPS and deadline is None:
            notes.append("The slip uses up the float of %s and moves the project finish." % name)
        if calendar is not None:
            old_end, new_end = calendar.date(base["end"]), calendar.date(slipped["end"])
            crossed = calendar.breaks_between(old_end, new_end) if new_end > old_end else []
            sections[-1]["rows"].append(row(
                "Project finish date before and after", "%s then %s" % (old_end.isoformat(), new_end.isoformat()),
                "working day number mapped to a calendar date", NOT_STATED))
            sections[-1]["rows"].append(row(
                "Break between the old and the new finish", span_text(crossed) if crossed else "none",
                "breaks given with --holiday that lie between the two dates", NOT_STATED,
                assumption=None if holidays else "No break was given, so none can be reported."))
            if crossed:
                notes.append("The slipped finish moves past %s. Work that cannot run in a break pushes the dates "
                             "further, and a charter rule on that break (read it from the charter) can turn a slip "
                             "of a few days into a slip over the break." % span_text(crossed))
    return {"title": "Critical path method", "inputs": {"activities": dict(durations), "start": start,
            "holidays": span_text(holidays) if holidays else None,
            "links": ["%s>%s %s%+g" % (p_, s_, k, l) if l else "%s>%s %s" % (p_, s_, k) for p_, s_, k, l in links],
            "deadline": deadline, "slip": None if not slip else "%s+%s" % slip},
            "sections": sections, "notes": notes, "table": table}


def num(v, places=4):
    if v is None:
        return "not computable"
    text = ("%.*f" % (places, v)).rstrip("0").rstrip(".")
    return "0" if text in ("", "-0") else text


def render_text(res):
    sources = []

    def cite_id(text):
        if text not in sources:
            sources.append(text)
        return sources.index(text) + 1

    lines = [res["title"]]
    if res.get("inputs"):
        lines.append("Inputs: " + ", ".join("%s=%s" % (k, v) for k, v in res["inputs"].items() if v is not None))
    if "matrix" in res:
        grid = [res["matrix"]["header"]] + res["matrix"]["rows"]
        widths = [max(len(r[c]) for r in grid) for c in range(len(grid[0]))]
        lines.append("")
        for r in grid:
            lines.append("  " + "  ".join(cell.ljust(widths[c]) for c, cell in enumerate(r)).rstrip())
        lines.append("  Source: " + res["cite"])
    for sec in res["sections"]:
        lines.append("")
        lines.append(sec["title"])
        for r in sec["rows"]:
            if r["value"] is None:
                value = "not computable" if not r.get("why") else "not computable (%s)" % r["why"]
                if r["formula"] == NOT_STATED:
                    value = NOT_STATED
            elif isinstance(r["value"], str):
                value = r["value"]
            else:
                value = num(r["value"]) + (" " + r["unit"] if r["unit"] else "")
            tail = ("  (%s)" % r["status"]) if r["status"] else ""
            lines.append("  %-34s %s%s  [%d]" % (r["label"], value, tail, cite_id(r["cite"])))
            if r["formula"] != NOT_STATED:
                lines.append("      formula: " + r["formula"])
            if r["assumption"]:
                lines.extend(textwrap.wrap("assumption: " + r["assumption"], 100, initial_indent="      ",
                                           subsequent_indent="          "))
    if res.get("notes"):
        lines.append("")
        lines.append("Notes")
        for n in res["notes"]:
            lines.extend(textwrap.wrap(n, 100, initial_indent="  - ", subsequent_indent="    "))
    if sources:
        lines.append("")
        lines.append("Sources")
        for k, s in enumerate(sources):
            lines.extend(textwrap.wrap(s, 100, initial_indent="  [%d] " % (k + 1), subsequent_indent="      "))
    return "\n".join(lines)


def json_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    raise TypeError(repr(obj))


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="print JSON instead of plain text")
    parser = argparse.ArgumentParser(
        description="Deterministic PM calculators; every formula is from PMBOK 6 or the Book of Forms and "
                    "is cited in the output. Page numbers give the PDF page and the printed page.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("evm", parents=[common], help="earned value analysis",
                       description="Earned value analysis. Formulas: CV = EV - AC, SV = EV - PV, VAC = BAC - EAC "
                                   "(PMBOK 6 section 7.4.2.2, printed page 262, PDF page 301); "
                                   "SPI = EV / PV, CPI = EV / AC (printed page 263, PDF page 302); EAC variants "
                                   "(printed pages 264 to 265, PDF pages 303 to 304); ETC = EAC - AC; TCPI "
                                   "(section 7.4.2.3, printed page 266, PDF page 305); status words from Table "
                                   "7-1 (printed page 267, PDF page 306), printed as under, on or over planned cost, ahead of, on or "
                                   "behind schedule, harder, same or easier to complete; percent planned, earned and spent "
                                   "(Book of Forms form 4.4, Table 4.4, PDF page 218, printed page 207).")
    p.add_argument("--bac", type=float, required=True, help="BAC")
    for name in ("pv", "ev", "ac"):
        p.add_argument("--" + name, type=float, help="%s; required unless only --bac and --threshold are given"
                       % name.upper())
    p.add_argument("--bottom-up-etc", type=float, help="your re-estimate of the remaining work; adds "
                   "EAC = AC + bottom-up ETC (PMBOK 6 section 7.4.2.2, printed page 264, PDF page 303)")
    p.add_argument("--approved-eac", type=float, help="an approved EAC to use as the TCPI goal (PMBOK 6 "
                   "section 7.4.2.3, printed page 266, PDF page 305)")
    p.add_argument("--threshold", type=float, metavar="PERCENT",
                   help="a variance threshold in percent from the charter; each overrun percent is marked within "
                        "or beyond it (the percent itself is an outside arithmetic aid)")
    p.add_argument("--base", nargs="+", choices=BASE_NAMES, default=["bac"],
                   help="what the percent is taken of, default bac; when the charter does not say, pass several "
                        "(for example bac pv) and report every one")

    p = sub.add_parser("pert", parents=[common], help="three-point estimate",
                       description="Beta mean (tO + 4 tM + tP) / 6: Book of Forms form 2.17, PDF page 84 (printed "
                                   "page 73) and Table 2.16, PDF page 87 (printed page 76); form 2.21, PDF page "
                                   "99 (printed page 88); PMBOK 6 section 7.2.2.5, printed page 245 (PDF page "
                                   "284). Triangular mean (tO + tM + tP) / 3: PMBOK 6 section 6.4.2.4, printed "
                                   "page 201 (PDF page 240). The standard deviation is not stated in either book.")
    for name in ("o", "m", "p"):
        p.add_argument("--" + name, type=float, required=True,
                       help={"o": "optimistic", "m": "most likely", "p": "pessimistic"}[name])

    p = sub.add_parser("effort-to-duration", parents=[common], help="parametric duration from effort hours",
                       description="Effort / (quantity x percent available x performance factor) = duration. "
                                   "Book of Forms form 2.17, Table 2.16, PDF page 86 (printed page 75). The "
                                   "book's example: 150 / (2 x .75 x .8) = 125 hours. The book's note that "
                                   "people are productive about 75 percent of the time is on PDF page 84 "
                                   "(printed page 73) and is printed in the output.")
    p.add_argument("--effort-hours", type=float, required=True, help="estimated effort")
    p.add_argument("--resources", type=float, required=True, help="resource quantity (people)")
    p.add_argument("--availability", required=True,
                   help="share of time the resources are available: 0.75 or 75%% (a bare number above 1 is refused)")
    p.add_argument("--performance", type=float,
                   help="performance factor; when left out 1.0 is used, which the book calls an average "
                        "resource (0.8 skilled, 1.2 less skilled) and the output says so")

    p = sub.add_parser("analogous", parents=[common], help="analogous duration or cost estimate",
                       description="Multiplier = current / previous; estimate = previous duration or cost x "
                                   "multiplier. Book of Forms form 2.17, Table 2.16, PDF page 86 (printed page 75) "
                                   "and form 2.21, Table 2.19, PDF page 100 (printed page 89).")
    p.add_argument("--previous-value", type=float, required=True, help="previous duration or cost")
    p.add_argument("--previous-size", type=float, required=True, help="size of the previous work")
    p.add_argument("--current-size", type=float, required=True, help="size of the current work")

    p = sub.add_parser("bottom-up", parents=[common], help="bottom-up cost estimate for a work package",
                       description="Labor = hours x rate; estimate = labor + material + supplies + equipment + "
                                   "travel + other direct + indirect + contingency reserve. Book of Forms form "
                                   "2.21, Table 2.20, PDF page 101 (printed page 90). Omitted parts count as zero "
                                   "and the output lists them.")
    p.add_argument("--labor-hours", type=float, required=True)
    p.add_argument("--labor-rate", type=float, required=True)
    for name in ("material", "supplies", "equipment", "travel", "other-direct", "indirect", "reserve"):
        p.add_argument("--" + name, type=float)

    p = sub.add_parser("risk-score", parents=[common], help="risk rating or probability-impact score",
                       description="Scale rating (default): Book of Forms Table 2.31, form 2.34, PDF pages 149 to "
                                   "150 (printed pages 138 to 139) gives High, Medium or Low from a probability "
                                   "level and an impact level; a probability may be a whole percent such as 35%% "
                                   "placed in the Table 2.31 bands. Scale pmbok: probability x impact with the "
                                   "Figure 11-5 values, PMBOK 6 printed page 408 (PDF page 447). Scale doubling: "
                                   "impact Very Low .5, Low 1, Medium 2, High 4, Very High 8 from the form 2.35 "
                                   "tailoring tip, PDF page 153 (printed page 142). --matrix prints the 5 by 5 "
                                   "grid of form 2.35, PDF page 154 (printed page 143), as ratings (or, with "
                                   "--scale pmbok, as the Figure 11-5 scores).")
    p.add_argument("--probability", help="level word, or a whole percent with a percent sign (rating scale); "
                                         "a level word or a number (pmbok); a number (doubling)")
    p.add_argument("--impact", help="level word (rating, doubling), or a level word or a number (pmbok)")
    p.add_argument("--scale", choices=("rating", "pmbok", "doubling"), default="rating")
    p.add_argument("--matrix", action="store_true", help="print the matrix instead of scoring one risk")

    p = sub.add_parser("emv", parents=[common], help="expected monetary value and a decision tree",
                       description="EMV = sum of probability x value; a decision tree takes the larger EMV of the "
                                   "options after payoff minus investment. PMBOK 6 section 11.4.2.5, Figure "
                                   "11-15, printed page 435 (PDF page 474). The book's example: Build New Plant, "
                                   "invest 120, 0.6:200 and 0.4:90 gives 36; Upgrade Plant, invest 50, 0.6:120 "
                                   "and 0.4:60 gives 46.")
    p.add_argument("--outcome", nargs="+", default=[], metavar="PROB:VALUE",
                   help="outcomes of one chance node, for example 0.6:80 0.4:-30 or 60%%:80")
    p.add_argument("--option", nargs="+", action="append", default=[], metavar="NAME COST PROB:PAYOFF",
                   help="a decision option: name, investment, then probability:payoff pairs; repeat per option")

    p = sub.add_parser("weighted-score", parents=[common], help="source selection weighted score",
                       description="Score = weight x rating per criterion, totalled per candidate, highest total "
                                   "wins; weights add to 100 percent. Book of Forms form 2.39, PDF page 166 "
                                   "(printed page 155) and Table 2.35, PDF page 167 (printed page 156).")
    p.add_argument("--weights", nargs="+", required=True, help="weights in percent, adding to 100")
    p.add_argument("--scores", nargs="+", action="append", required=True,
                   help="one candidate's ratings in the same order as the weights; repeat per candidate")
    p.add_argument("--names", nargs="+", help="candidate names in the order of the --scores lists")
    p.add_argument("--scale-max", type=float, help="top of the rating range the team chose (1 to N); when given, "
                   "ratings outside 1 to N are refused")

    p = sub.add_parser("comms-channels", parents=[common], help="communication channels",
                       description="n x (n - 1) / 2. Not printed in either book: PMBOK 6 section 10.1.2.2, printed "
                                   "page 370 (PDF page 409) lists the number of potential channels as a source "
                                   "but gives no formula. The output says so.")
    p.add_argument("--people", type=int, required=True, help="number of people")

    p = sub.add_parser("earned-schedule", parents=[common], help="time-based schedule variance and index",
                       description="SV(t) = ES - AT and SPI(t) = ES / AT: PMBOK 6, Trends and Emerging Practices in "
                                   "Project Cost Management, printed page 233 (PDF page 272). The book names the "
                                   "completion-date forecast but prints no formula for it.")
    p.add_argument("--es", type=float, required=True, help="earned schedule, in the same time unit as --at")
    p.add_argument("--at", type=float, required=True, help="actual time")

    p = sub.add_parser("cpm", parents=[common], help="critical path, dates and float of a small network",
                       description="Forward and backward pass with total and free float, day 1 convention of PMBOK 6 "
                                   "Figure 6-16 (section 6.5.2.2, printed pages 210 to 211, PDF pages 249 to 250). "
                                   "An outside arithmetic aid: the book prints no equations.")
    p.add_argument("--activity", action="append", default=[], metavar="NAME=DAYS", help="an activity and its duration")
    p.add_argument("--link", action="append", default=[], metavar="PRED,SUCC[,TYPE[,LAG]]",
                   help="a dependency; TYPE is FS (default), SS, FF or SF; LAG in days, negative for a lead")
    p.add_argument("--deadline", metavar="DAYS|YYYY-MM-DD",
                   help="the project must finish by the end of this working day, counted from day 1 (a number), "
                        "or by this calendar date (needs --start); gives positive or negative total float")
    p.add_argument("--slip", metavar="NAME=DAYS", help="what if this activity runs this many days longer")
    p.add_argument("--start", metavar="YYYY-MM-DD", help="calendar date of day 1 (the first working day on or "
                   "after it); adds calendar dates, Monday to Friday")
    p.add_argument("--holiday", action="append", default=[], metavar="DATE[:DATE]",
                   help="a break with no work, a date or a closed range YYYY-MM-DD:YYYY-MM-DD; repeat per break")

    p = sub.add_parser("crash", parents=[common], help="rank crashing options by extra cost per day saved",
                       description="Crashing shortens the schedule for the least incremental cost by adding "
                                   "resources, on critical path activities only (PMBOK 6 section 6.5.2.6, printed "
                                   "page 215, PDF page 254). An outside arithmetic aid: the book prints no equation.")
    p.add_argument("--option", nargs=4, action="append", default=[],
                   metavar=("NAME", "NORMAL_DAYS", "CRASHED_DAYS", "EXTRA_COST"),
                   help="a critical activity: duration as planned, duration when crashed, extra cost of crashing; "
                        "repeat per activity")
    p.add_argument("--needed", type=float, help="days to save, to list the cheapest options that reach it")

    p = sub.add_parser("velocity", parents=[common], help="velocity from completed story points",
                       description="Velocity is the sum of the story point sizes of the features actually completed in "
                                   "the iteration (Agile Practice Guide section 5.4.1, printed page 64, PDF page 874). "
                                   "The average and the iterations remaining are outside arithmetic aids.")
    p.add_argument("--completed", type=float, nargs="+", required=True, help="points completed in each iteration")
    p.add_argument("--remaining", type=float, help="story points still in the release")

    p = sub.add_parser("cd3", parents=[common], help="rank items by cost of delay divided by duration",
                       description="CD3 = cost of delay / duration, ranking highest first (Agile Practice Guide "
                                   "Table 5-1, printed page 59, PDF page 869). The Guide gives no units.")
    p.add_argument("--item", nargs=3, action="append", default=[], metavar=("NAME", "COST_OF_DELAY", "DURATION"),
                   help="a backlog item; repeat per item")

    p = sub.add_parser("reserve", parents=[common], help="remaining contingency against remaining risk",
                       description="Reserve analysis: contingency remaining compared with the risk remaining "
                                   "(PMBOK 6 section 11.7.2.1, printed page 456, PDF page 495). An outside "
                                   "arithmetic aid: the book prints no equation and no adequacy rule.")
    p.add_argument("--contingency", type=float, required=True, help="the contingency reserve in the cost baseline")
    p.add_argument("--used", type=float, default=0.0, help="contingency drawn so far, default 0")
    p.add_argument("--risk", action="append", default=[], metavar="ID=PROB:IMPACT",
                   help="an open risk, for example R5=0.3:12000000 or R5=30%%:12000000; repeat per risk")

    p = sub.add_parser("funding", parents=[common], help="funds released by tranche against cost to date",
                       description="Funding released in steps against actual cost (PMBOK 6 section 7.3.3.2, printed "
                                   "page 256, PDF page 295, and Figure 7-9, printed page 255, PDF page 294). An "
                                   "outside arithmetic aid: the book prints no equation.")
    p.add_argument("--tranche", action="append", default=[], metavar="NAME=AMOUNT",
                   help="a funding tranche in release order, for example M0=140000000; repeat per tranche")
    p.add_argument("--through", required=True, help="the last tranche already released")
    p.add_argument("--spent", type=float, required=True, help="cumulative actual cost to date")
    p.add_argument("--total", type=float, help="total funding stated by the sponsor, to check the tranches add up")

    p = sub.add_parser("response-effectiveness", parents=[common], help="cost effectiveness of risk responses",
                       description="(change in impact level) / (implementation cost), higher is more effective "
                                   "(PMBOK 6 section 11.5.2.8, printed page 446, PDF page 485).")
    p.add_argument("--option", nargs=4, action="append", default=[],
                   metavar=("NAME", "IMPACT_BEFORE", "IMPACT_AFTER", "COST"), help="a response; repeat per response")

    p = sub.add_parser("payback", parents=[common], help="payback period from net benefits",
                       description="First period in which the cumulative net benefit reaches the investment. An "
                                   "outside arithmetic aid: PMBOK 6 names payback analysis (section 1.2.6.4, printed "
                                   "page 34, PDF page 73; section 12.1.2.3, printed page 473, PDF page 512) and "
                                   "prints no formula.")
    p.add_argument("--investment", type=float, required=True)
    p.add_argument("--net", type=float, nargs="+", required=True, help="net benefit of each period, in order")
    return parser


def run(args):
    cmd = args.command
    if cmd == "evm":
        return evm(args.bac, args.pv, args.ev, args.ac, args.bottom_up_etc, args.approved_eac, args.threshold,
                   args.base)
    if cmd == "pert":
        return pert(args.o, args.m, args.p)
    if cmd == "effort-to-duration":
        return effort_to_duration(args.effort_hours, args.resources,
                                  parse_share(args.availability, "availability"), args.performance)
    if cmd == "analogous":
        return analogous(args.previous_value, args.previous_size, args.current_size)
    if cmd == "bottom-up":
        return bottom_up(args.labor_hours, args.labor_rate, args.material, args.supplies, args.equipment,
                         args.travel, args.other_direct, args.indirect, args.reserve)
    if cmd == "risk-score":
        if args.matrix:
            if args.scale == "doubling":
                raise CalcError("--matrix prints the rating grid or, with --scale pmbok, the Figure 11-5 scores; "
                                "the doubling scale has no printed grid and no probability numbers (%s)"
                                % C_235_TIP)
            return matrix("pmbok" if args.scale == "pmbok" else "rating")
        if args.probability is None or args.impact is None:
            raise CalcError("give --probability and --impact, or --matrix")
        return risk_score(args.probability, args.impact, args.scale)
    if cmd == "emv":
        outcomes = [parse_outcome(t) for t in args.outcome]
        options = []
        for tokens in args.option:
            if len(tokens) < 3:
                raise CalcError("--option needs a name, an investment and at least one probability:payoff")
            investment = parse_number(tokens[1], "investment")
            need("investment", investment, nonneg=True)
            options.append((tokens[0], investment,
                            [parse_outcome(t) for t in tokens[2:]]))
        return emv(outcomes, options)
    if cmd == "weighted-score":
        weights = [parse_number(str(w).rstrip("%"), "weight") for w in args.weights]
        candidates = [[parse_number(s, "rating") for s in group] for group in args.scores]
        return weighted_score(weights, candidates, args.names, args.scale_max)
    if cmd == "earned-schedule":
        return earned_schedule(args.es, args.at)
    if cmd == "cpm":
        if args.holiday and not args.start:
            raise CalcError("--holiday needs --start, the date of day 1")
        start = None if not args.start else parse_date(args.start, "--start")
        breaks = parse_breaks(args.holiday)
        return cpm([parse_pair(t, "activity") for t in args.activity], [parse_link(t) for t in args.link],
                   parse_deadline(args.deadline, start, breaks),
                   None if not args.slip else parse_pair(args.slip, "slip"), start, breaks)
    if cmd == "crash":
        return crash([(n, parse_number(a, "normal days"), parse_number(b, "crashed days"),
                       parse_number(c, "extra cost")) for n, a, b, c in args.option], args.needed)
    if cmd == "velocity":
        return velocity(args.completed, args.remaining)
    if cmd == "cd3":
        return cd3([(n, parse_number(d, "cost of delay"), parse_number(t, "duration")) for n, d, t in args.item])
    if cmd == "payback":
        return payback(args.investment, args.net)
    if cmd == "reserve":
        risks = []
        for token in args.risk:
            name, sep, rest = token.partition("=")
            if not sep or not name.strip():
                raise CalcError("risk %r: write ID=PROB:IMPACT" % token)
            prob, value = parse_outcome(rest)
            risks.append((name.strip(), prob, value))
        return reserve(args.contingency, args.used, risks)
    if cmd == "funding":
        return funding([parse_pair(t, "tranche") for t in args.tranche], args.spent, args.through, args.total)
    if cmd == "response-effectiveness":
        return response_effectiveness([(n, parse_number(b, "impact before"), parse_number(a, "impact after"),
                                        parse_number(c, "cost")) for n, b, a, c in args.option])
    return comms_channels(args.people)


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        result = run(args)
    except CalcError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2, default=json_default))
    else:
        print(render_text(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
