#!/usr/bin/env python3
"""Compact the combined report tab ("Báo cáo tổng hợp") of the Doc to the page budget: at most 90
pages with the body text at 12 pt, the tables in their own smaller face, the margins as they are, and
the WBS dictionary and the prompt log left to an appendix outside the count.

The tab was assembled by hand from tabs 1 to 10, while the Product Charter tab was being rewritten, so
its Parts 1 and 2 carry unfilled table placeholders, and a draft block from the second tab follows them
under the team's own note that it is not part of the submission. The steps, each run on its own flag:

  --charter   Parts 1 and 2 written again from docs/charter-package.en.md, with 2.1 Charter Elements
              cut to the elements the boxes of form 1.1 have no room for, and the draft block deleted
              up to the section break before "3: Scope Baseline".
  --prose     Reading conventions and method notes of sections 1 and 3 to 9 shortened, and the parts the
              submission does not need deleted: What this section is not, the risk revision history, and
              section 10 Assumption Log, with the references to it.
              Every shortened text is condensed from the paragraph it replaces; none adds a fact.
  --schedule  The table under the Gantt chart cut to the milestones, the phases, and the control
              accounts; the work packages and activities stay in the Gantt chart itself.
  --font      Body text below the cover at 12 pt. Tables, headings, and the cover keep their faces.

Run with:
    python3 tools/gdoc_report_tab.py --doc DOC_ID --dry-run --charter --prose --schedule --font
    python3 tools/gdoc_report_tab.py --doc DOC_ID --charter --prose --schedule --font
"""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import socket
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc_charter_tab as charter
import gdoc_cost_tab as layout
import gdoc_edit as ge

DEFAULT_DIR = os.path.expanduser("~/.config/qldapm")
TAB = "Báo cáo tổng hợp"
NEXT_PART = "3: Scope Baseline"
BODY_PT = 12

# 2.1 keeps the elements whose detail the boxes of form 1.1 have no room for.
KEEP_21 = ("Project purpose", "Overall project risk", "Summary milestone schedule",
           "Project approval requirements")

READING_21 = (
    "Table 1.1 Elements of a Project Charter, A Project Manager's Book of Forms, 3rd edition, PDF pages "
    "13 to 15 (printed pages 2 to 4). Together with the form in section 2.2 it is the project charter of "
    "PMBOK 6 section 4.1.3.1, printed page 81 (PDF page 120), as committed on 16 September 2026 and "
    "amended on 14 November 2026. The boxes of the form carry all fourteen elements; this section keeps "
    "only the detail they have no room for: the quantified business case, the risks identified at "
    "chartering, the notes behind the summary milestones, and the approval requirements. The change "
    "requests pending against the charter, among them the scope and cost request of section 5.7, change "
    "nothing here until the sponsor decides them. Form 2.32 Risk Register of section 8 keeps the numbers "
    "R1 to R12 and adds R13 to R18."
)

# The report carries no assumption log, so Part 1 no longer points to one.
READING_1 = charter.READING_1.rsplit(" Assumptions 1 to 19 are kept", 1)[0]

# Paragraphs of sections 1 and 3 to 9, found by the start of their text. None deletes the paragraph.
PROSE = [
    ("Form 2.8 Project Scope Statement, A Project Manager's Book of Forms", READING_1),
    ("In section 3.3, the split of hours and money across work packages",
     "The hours and money of each work package in the WBS dictionary (Appendix A) are a first-pass "
     "estimate, tagged once per sheet. The totals they roll up to are given by the charter and are not "
     "highlighted: 4,400 labor hours, 539,000,000 VND of labor, 161,000,000 VND of other cost, "
     "700,000,000 VND in all."),
    ("Per PMBOK 6 Figure 5-10, Create WBS takes",
     "Per PMBOK 6 Figure 5-10, Create WBS takes the scope management plan, the project scope statement, "
     "and the requirements documentation. The charter is not a direct input to 5.4; it reaches the WBS "
     "through the scope statement. The requirements traceability matrix is an output of 5.2, so this "
     "section builds it first from the charter and the requirement specification, and then builds the "
     "WBS from the scope statement."),
    ("The date prepared, 23 September 2026, falls inside the requirements phase", None),
    ("Work package sizing. Every work package holds between 8 and 80 hours",
     "Work package sizing. Every work package holds between 8 and 80 hours of effort and is controlled "
     "inside a single milestone gate. Three packages sit outside that rule: 1.1.1.2 weekly status "
     "reporting at 120 hours and 1.10.1.1 first warranty month support at 400 hours are level-of-effort "
     "packages, and 1.9.1.1 store accounts and signing keys, at 22 hours, crosses the M2 gate because "
     "Apple's enrolment of a legal entity takes up to four weeks."),
    ("The hours are effort, not calendar loading", None),
    ("Phase 1.2 carries a Technical Preparation control account", None),
    ("The schedule of PMBOK 6 section 6.5 Develop Schedule, reproduced from form 2.18",
     "The schedule of PMBOK 6 section 6.5 Develop Schedule, form 2.18 of A Project Manager's Book of "
     "Forms, 3rd edition, levelled from the work packages of section 3 and the milestones of section 2."),
    ("This schedule is the output of PMBOK 6 section 6.5 Develop Schedule. It is resource-levelled",
     "Form 2.18, resource-levelled (PMBOK 6 section 6.5.2.3): every activity of the WBS dictionary "
     "(Appendix A) keeps its hours and is placed into its people's working time, at most 8 hours a "
     "working day, weekends and New Year's Day excluded. 93 activities are divided between two people, "
     "and work may start up to 5 working days before the gate that releases it, which is fast tracking "
     "(6.5.2.6). Page 1 is the Gantt chart in 7 parts, which shows every work package and activity; the "
     "table under it keeps the milestones, the phases, and the control accounts. Page 2 is the milestone "
     "chart, each milestone at its levelled forecast beside its charter date. <mark>Highlighted</mark> "
     "dates are the levelled forecast, which moves M6 and M7 past the charter dates, so the milestones "
     "are not baselined until the sponsor decides the schedule change request of 30 September 2026. The "
     "Lunar New Year break of 2027 is not in the calendar (assumption 8). The levelled project runs from "
     "Mon 14 September 2026 to Fri 19 March 2027."),
    ("The cost estimate of PMBOK 6 section 7.2 Estimate Costs [1]",
     "The cost estimate of PMBOK 6 section 7.2 Estimate Costs [1]: what each control account of the WBS "
     "costs in people, in physical resources, and in software, with the basis of every figure. Its inputs "
     "are the ones the book lists for form 2.20 [2]: the WBS and the dictionary hours less the work the "
     "scope change request defers, the levelling of section 4.1 run on that reduced work, the resource on "
     "each dictionary activity, and the charter's contingency reserve. There is no separate cost or "
     "quality management plan and no lessons learned register yet. The updates this estimate proposes "
     "to other documents are carried by the scope change request of section 5.7."),
    ("Form 2.20 is filled at control account level",
     "Form 2.20 is filled at control account level, one row for each of the 21 control accounts the "
     "reduced scope keeps and one project-level row for the reserve, as the book permits [2]; form 2.21 "
     "shows the work behind each row. An hour costs the gross monthly salary plus the employer's "
     "contributions, 21.5% insurance [4] and 2% union fee [5], divided by 160 hours; the salary is the "
     "ITviec median for 1 to 2 years of experience [3], "
     "<mark>the seniority every role is costed at</mark>, and developers are priced as full-stack. The "
     "uncertainty sits in the hours: the optimistic and pessimistic values are 0.67 and 1.5 times the most "
     "likely, the cone of uncertainty at requirements complete [14], weighted (O + 4M + P) / 6 as PMBOK 6 "
     "section 7.2.2.5 gives, which is 1.0283 times the hours; the warranty support desk is an allocation "
     "and is not weighted. The total's range is 449,726,000 to 905,316,000; one standard deviation is "
     "75,932,000, so the estimate plus one standard deviation, 721,941,000, is about the 84th percentile. "
     "Amounts exclude VAT [16]. Confidence Level is Medium where the rates are survey medians and the "
     "prices are published, and Low for an allowance carried from the charter and for the reserve. "
     "<mark>Highlighted</mark> content is a choice or a quantity that no source confirms. Every figure is "
     "generated by the team's costing script from the WBS dictionary, the levelled schedule of section "
     "4.1, and the prices of section 5.6."),
    ("Had the five been paid by the month over that window instead", None),
    ("This request carries the cost estimate of form 2.20 in sections 5.1 to 5.6",
     "This request carries the cost estimate of sections 5.1 to 5.6 to the sponsor through Perform "
     "Integrated Change Control, PMBOK 6 section 4.6, as the funding limit reconciliation of section "
     "7.3.2.5: the full scope does not fit the 700,000,000 VND the charter makes available, so the request "
     "reduces the scope and changes how the work is staffed until the estimate meets the team's target of "
     "650,000,000. It follows the schedule change request of 30 September 2026. The submitted charter, "
     "scope package, and schedule are not edited until the sponsor decides. <mark>Highlighted</mark> "
     "figures are estimates, not quotations. The disposition is the sponsor's and is left empty; a ticked "
     "box, ☒, marks what applies."),
    ("Form 2.23, A Project Manager's Book of Forms, 3rd edition, PDF pages 108 to 109",
     "Form 2.23, A Project Manager's Book of Forms, 3rd edition, PDF pages 108 to 109 (printed pages 97 "
     "to 98), the output of PMBOK 6 section 8.1 Plan Quality Management with the components of section "
     "8.1.3.1; the quality tools are named inside the two approach boxes. It is built from the charter and "
     "the scope baseline of section 3, and follows the baselined charter, not the pending scope change "
     "request of section 5.7; if the sponsor approves it, the rows for A01, A02, A09, and A12 and the "
     "deliverables D4 and D11 change with it. Quality Objectives holds one row for each acceptance "
     "criterion of charter section 1.3, its text copied as written, and two rows for the warranty "
     "response targets and the review rule. A WBS code such as 1.6.1.4 names the work package that does "
     "the work. <mark>Highlighted</mark> content is a proposal or an assumption that no project document "
     "confirms yet."),
    ("Form 2.27, A Project Manager's Book of Forms, 3rd edition, PDF pages 122 to 123",
     "Form 2.27, A Project Manager's Book of Forms, 3rd edition, PDF pages 122 to 123 (printed pages 111 "
     "to 112); PMBOK 6 section 9.1.3.2. Built from the charter, the scope baseline of section 3, and the "
     "cost estimate of section 5, whose company rules and reduced scope it follows. Plain text is copied "
     "from the charter or from the company rules; highlighted text is a working rule "
     "proposed for the team to confirm at kickoff. The signature lines are empty."),
    ("Form 2.28, A Project Manager's Book of Forms, 3rd edition, PDF page 126",
     "Form 2.28, A Project Manager's Book of Forms, 3rd edition, PDF page 126 (printed page 115); PMBOK 6 "
     "section 9.2.3.1. It follows the cost estimate of section 5, form 2.20, row for row. Team rows give "
     "the role, the skills, the experience and degree, and the hours booked; physical rows give the item, "
     "its minimum specification, the quantity, and the amount. Software, accounts, and services are "
     "written as supplies, since the form has no software kind. Highlighted content is a "
     "choice or a specification that no source confirms."),
    ("Form 2.29, A Project Manager's Book of Forms, 3rd edition, PDF page 128",
     "Form 2.29, A Project Manager's Book of Forms, 3rd edition, PDF page 128 (printed page 117); PMBOK 6 "
     "section 9.2.3.3. It is kept in step with form 2.28, which holds the skills, the specifications, the "
     "hours, the amounts, and the basis, and applies the same reduced scope. The five printed branches "
     "are kept; software, accounts, and services sit under Supplies, and Materials has no entry because no "
     "document names a material. A highlighted quantity is an assumption."),
    ("Form 2.32, A Project Manager's Book of Forms, 3rd edition, PDF page 141",
     "Form 2.32, A Project Manager's Book of Forms, 3rd edition, PDF page 141 (printed page 130), the "
     "output of PMBOK 6 section 11.2.3.1. The form prints in two banks; row N of the second continues row "
     "N of the first, and the ID column of the second bank is added so that each can be read on its own. "
     "Each risk is written \"If CONDITION exists, EVENT may occur, leading to EFFECT\", the structure of "
     "Table 2.29 of the book. R1 to R12 restate the risks identified at chartering in section 2.1; R13 to "
     "R16 come from assumption and constraint analysis and document analysis (PMBOK 6 section 11.2.2), "
     "and R17 and R18 are the two risks the pending scope change request of section 5.7 adds."),
    ("Highlighted cells are the preparer's reading and are to be confirmed by the team",
     "<mark>Highlighted</mark> cells are the preparer's reading, to be confirmed by the team. Probability "
     "and Impact use the three levels of the scales above the form; Score is Probability-Impact, taking "
     "the highest of the four Impact levels. Owner names one role per risk (PMBOK 6 section 11.3.2.7). "
     "Response begins with the strategy for threats of PMBOK 6 section 11.5.2.4, and Actions name the "
     "work packages that carry it out."),
    ("Revised Probability, Impact, and Score forecast the risk expected to remain",
     "Revised Probability, Impact, and Score forecast the residual risk of PMBOK 6 section 11.5.3.3, so "
     "each of them is highlighted. Status is Open for every risk because no document records a response "
     "as complete. Every risk follows the charter until the sponsor decides the pending change requests; "
     "Comments say what each request would change. Cells changed in version 1.1 are shaded green."),
    ("Form 1.3, A Project Manager's Book of Forms, 3rd edition, PDF page 25",
     "Form 1.3, A Project Manager's Book of Forms, 3rd edition, PDF page 25 (printed page 14), the output "
     "of PMBOK 6 section 13.1.3.1. Built from the charter as amended on 14 November 2026, form 2.28 "
     "Resource Requirements of section 7.2, and form 2.32 Risk Register of section 8. Eight of the twenty "
     "rows were added to the charter's stakeholder list on 14 November 2026, each from a named place in "
     "the project's documents: S03 from the sponsor's authority and assumption 2, S08 from Users and "
     "roles and risk R15, S13 from the project manager's staffing authority, S14 from exit criterion 7, "
     "S17 and S18 from risk R12 and budget line 2, S19 from budget line 2 and acceptance criterion A12, "
     "and S20 from acceptance criterion A04 and risk R13."),
    ("The ID column is not printed on the form; it is added so that each row of this register",
     "The ID column is not printed on the form; it matches each row to form 1.4 of section 9.2. Contact "
     "Information is empty where no project document holds it. Requirements are the stakeholder's needs "
     "of the project or the product, and Expectations what the stakeholder expects of the way it runs. "
     "Classification uses three models of PMBOK 6 section 13.1.3.1: internal or external, the direction "
     "of influence (13.1.2.4), and the quadrant of the grid of form 1.4; the last two are the preparer's "
     "reading and are highlighted."),
    ("Form 1.4, A Project Manager's Book of Forms, 3rd edition, PDF page 27",
     "Form 1.4, A Project Manager's Book of Forms, 3rd edition, PDF page 27 (printed page 16), the "
     "stakeholder analysis of PMBOK 6 section 13.1.2.3, mapped as a grid (13.1.2.4). The rows are the "
     "twenty stakeholders of form 1.3, with the same IDs and names."),
    ("The stakeholders of this project are few and their relationships simple",
     "The analysis uses the two-by-two grid of the book's first tailoring tip, with two levels each for "
     "Interest and Influence, defined below, and the book's three Attitude classes, friend, neutral, and "
     "foe. No stakeholder has yet been interviewed, so every level is the preparer's reading and is "
     "highlighted."),
]

# Headings deleted with everything under them up to the next heading.
DROP_HEADINGS = ("What this section is not", "Revision history")

# Parts the submission leaves out, deleted from the section break before them to the end of the tab.
DROP_TO_END = "10: Assumption Log"


# ------------------------------------------------------------------ content

def compact_charter() -> str:
    """Parts 1 and 2 as the Product Charter tab has them, with 2.1 cut to KEEP_21."""
    text = charter.build().replace(charter.READING_21, READING_21)
    start = text.index("### " + charter.H_ELEMENTS)
    end = text.index("### " + charter.H_FORM)
    parts = re.split(r"(?m)^(?=#### )", text[start:end])
    kept = [parts[0]]
    for part in parts[1:]:
        name = part.split("\n", 1)[0][5:].strip()
        if name == "Reading convention" or name in KEEP_21:
            kept.append(part)
    missing = [k for k in KEEP_21 if not any(p.startswith("#### " + k) for p in kept)]
    if missing:
        raise SystemExit("2.1 subsections not found: %s" % missing)
    text = text[:start] + "".join(kept) + text[end:]
    text = text.replace("The five objectives above", "The five objectives of the form in section 2.2")
    return text


def check_texts():
    for prefix, new in PROSE:
        if new is None:
            continue
        for bad in ("\u2014", "\u2013", "`", "section 3.3", "section 4.2"):
            if bad in new:
                raise SystemExit("%r in the text replacing %r" % (bad, prefix))


# ------------------------------------------------------------------ helpers

def _tab(doc):
    names = [t[0].strip() for t in doc.tabs()]
    if TAB not in names:
        raise SystemExit("no tab %r; tabs present: %s" % (TAB, names))
    return names.index(TAB)


def _para(content, prefix):
    hits = [el for el in ge.top_paragraphs(content) if ge.para_text(el).strip().startswith(prefix)]
    if len(hits) > 1:
        raise SystemExit("%d paragraphs start with %r" % (len(hits), prefix))
    return hits[0] if hits else None


def _marked(el):
    return [r["textRun"]["content"] for r in el["paragraph"]["elements"]
            if "textRun" in r and r["textRun"].get("textStyle", {}).get("backgroundColor")]


# ------------------------------------------------------------------ steps

def step_charter(doc, tab_n, dry):
    tab_id, content = doc.tab(tab_n)
    head = charter._find(content, charter.H_PART1)
    nxt = charter._find(content, NEXT_PART)
    if head is None or nxt is None:
        raise SystemExit("the tab must hold %r and %r" % (charter.H_PART1, NEXT_PART))
    k = next(i for i, el in enumerate(content) if el.get("startIndex") == nxt["startIndex"])
    brk = content[k - 1]
    if "sectionBreak" not in brk:
        raise SystemExit("no section break before %r" % NEXT_PART)
    text = compact_charter()
    print("charter: delete %d to %d, insert %d characters" % (head["startIndex"], brk["startIndex"] - 1, len(text)))
    if dry:
        return
    doc.delete_range(tab_id, head["startIndex"], brk["startIndex"] - 1)
    doc.insert_markdown(tab_n, head["startIndex"], text)
    charter.lay_out(doc, tab_n)


def step_prose(doc, tab_n, dry):
    tab_id, content = doc.tab(tab_n)
    reqs = []
    for prefix, new in PROSE:
        el = _para(content, prefix)
        if el is None:
            print("prose: not found, skipped: %r" % prefix[:60])
            continue
        old = ge.para_text(el).strip()
        print("prose: %s %r (%d -> %d chars)%s" % ("delete" if new is None else "shorten", prefix[:50],
                                                   len(old), 0 if new is None else len(ge.parse_inline(new)[0]),
                                                   "  marked: %s" % _marked(el) if _marked(el) else ""))
        if new is None:
            reqs.append((el["startIndex"], [{"deleteContentRange": {"range": {
                "startIndex": el["startIndex"], "endIndex": el["endIndex"], "tabId": tab_id}}}]))
        else:
            s, e = el["startIndex"], el["endIndex"] - 1
            reqs.append((s, [{"deleteContentRange": {"range": {"startIndex": s, "endIndex": e, "tabId": tab_id}}}]
                         + ge.insert_inline(tab_id, s, new)[0]))
    tops = content
    for name in DROP_HEADINGS:
        k = next((i for i, el in enumerate(tops) if "paragraph" in el and ge.para_text(el).strip() == name), None)
        if k is None:
            print("prose: heading not found, skipped: %r" % name)
            continue
        j = k + 1
        while j < len(tops) and not (
                "paragraph" in tops[j]
                and tops[j]["paragraph"]["paragraphStyle"].get("namedStyleType", "").startswith("HEADING")):
            j += 1
        s, e = tops[k]["startIndex"], tops[j]["startIndex"]
        print("prose: drop %r with what follows it, %d characters" % (name, e - s))
        reqs.append((s, [{"deleteContentRange": {"range": {"startIndex": s, "endIndex": e, "tabId": tab_id}}}]))
    if not dry and reqs:
        flat = []
        for _, r in sorted(reqs, key=lambda x: x[0], reverse=True):
            flat += r
        doc.batch(flat)
    drop_to_end(doc, tab_n, dry)


def drop_to_end(doc, tab_n, dry):
    """DROP_TO_END and everything after it. The content goes first; the section break before it, which
    turns the page to landscape, goes in a request of its own, and the paragraph before the break is
    removed instead when the API will not remove the break itself, so no empty page is left."""
    tab_id, tops = doc.tab(tab_n)
    k = next((i for i, el in enumerate(tops) if "paragraph" in el and ge.para_text(el).strip() == DROP_TO_END), None)
    if k is None:
        print("prose: %r not found, skipped" % DROP_TO_END)
        return
    s, e = tops[k]["startIndex"], tops[-1]["endIndex"] - 1
    print("prose: drop %r to the end of the tab, %d characters" % (DROP_TO_END, e - s))
    if dry:
        return
    doc.batch([{"deleteContentRange": {"range": {"startIndex": s, "endIndex": e, "tabId": tab_id}}}])
    tab_id, tops = doc.tab(tab_n)
    brk = tops[-2] if "sectionBreak" in tops[-2] else None
    if brk is None:
        return
    for start, end in ((brk["startIndex"], brk["endIndex"]), (brk["startIndex"] - 1, brk["endIndex"])):
        try:
            doc.batch([{"deleteContentRange": {"range": {"startIndex": start, "endIndex": end, "tabId": tab_id}}}])
            print("prose: section break removed (%d to %d)" % (start, end))
            return
        except Exception as exc:
            print("prose: section break not removed (%d to %d): %s" % (start, end, str(exc)[:120]))


def step_schedule(doc, tab_n, dry):
    tab_id, content = doc.tab(tab_n)
    table = next((el for el in ge.top_tables(content)
                  if [ge.cell_text(c).strip() for c in ge.table_cells(el)[0]][:3] == ["ID", "WBS", "Task Name"]),
                 None)
    if table is None:
        raise SystemExit("schedule table not found")
    rows = ge.table_cells(table)
    drop = [n for n, row in enumerate(rows) if n and ge.cell_text(row[1]).strip().count(".") >= 3]
    print("schedule: %d rows, keep %d" % (len(rows), len(rows) - len(drop)))
    if dry or not drop:
        return
    where = {"index": table["startIndex"], "tabId": tab_id}
    doc.batch([{"deleteTableRow": {"tableCellLocation": {"tableStartLocation": where, "rowIndex": n, "columnIndex": 0}}}
               for n in reversed(drop)])


def step_font(doc, tab_n, dry):
    tab_id, content = doc.tab(tab_n)
    top = charter._below(content, charter.H_PART1)
    reqs = []
    for el in ge.top_paragraphs(content):
        style = el["paragraph"]["paragraphStyle"].get("namedStyleType", "NORMAL_TEXT")
        if el["startIndex"] < top or style != "NORMAL_TEXT" or el["endIndex"] - el["startIndex"] < 2:
            continue
        reqs.append({"updateTextStyle": {
            "range": {"startIndex": el["startIndex"], "endIndex": el["endIndex"] - 1, "tabId": tab_id},
            "textStyle": {"fontSize": {"magnitude": BODY_PT, "unit": "PT"}}, "fields": "fontSize"}})
    print("font: %d body paragraphs to %d pt" % (len(reqs), BODY_PT))
    if not dry and reqs:
        doc.batch(reqs)


# ------------------------------------------------------------------ appendix

APPENDIX = "Appendices"

# Each part moved: the heading it stays under, the first element moved after it (None: the one after the
# heading), the heading or text where the move stops, the appendix title, and the line left in its place.
MOVES = [
    ("3.1.2 Inter-requirements traceability matrix", None, "3.2 Work Breakdown Structure",
     "Appendix B: Inter-requirements traceability matrix",
     "The inter-requirements traceability matrix is in Appendix B."),
    ("5.3 Cost Estimating Worksheet", "Page 1 of 2", "5.4 Paid time without booked work",
     "Appendix C: Bottom-up cost estimating worksheet, form 2.21 page 2",
     "Page 2 of form 2.21, the bottom-up cost estimating worksheet, is in Appendix C."),
    ("5.6 References", None, "5.7 Change Request",
     "Appendix D: References of section 5",
     "The references cited in section 5 as [1] to [16] are listed in Appendix D."),
]

TEXT_FIELDS = ("bold", "italic", "underline", "strikethrough", "fontSize", "weightedFontFamily",
               "backgroundColor", "foregroundColor", "link", "baselineOffset")
PARA_FIELDS = ("namedStyleType", "alignment", "lineSpacing", "spaceAbove", "spaceBelow", "indentStart",
               "indentFirstLine", "indentEnd", "keepWithNext", "keepLinesTogether")
CELL_FIELDS = ("backgroundColor", "contentAlignment", "paddingLeft", "paddingRight", "paddingTop",
               "paddingBottom", "borderLeft", "borderRight", "borderTop", "borderBottom")


def _runs(paragraph):
    """(text, textStyle) of each run of a paragraph, the closing newline left out."""
    out = []
    for e in paragraph["elements"]:
        if "textRun" in e:
            out.append((e["textRun"]["content"], e["textRun"].get("textStyle", {})))
    if out and out[-1][0].endswith("\n"):
        out[-1] = (out[-1][0][:-1], out[-1][1])
    return [r for r in out if r[0]]


def _text_reqs(tab_id, base, runs):
    reqs, at = [], base
    for text, style in runs:
        fields = [f for f in TEXT_FIELDS if f in style]
        if fields:
            reqs.append({"updateTextStyle": {"range": {"startIndex": at, "endIndex": at + len(text), "tabId": tab_id},
                                             "textStyle": {f: style[f] for f in fields}, "fields": ",".join(fields)}})
        at += len(text)
    return reqs


def _para_req(tab_id, start, end, pstyle):
    fields = [f for f in PARA_FIELDS if f in pstyle]
    return {"updateParagraphStyle": {"range": {"startIndex": start, "endIndex": end, "tabId": tab_id},
                                     "paragraphStyle": {f: pstyle[f] for f in fields}, "fields": ",".join(fields)}}


def _append_paragraphs(doc, tab_n, paras):
    """paras: (runs, paragraphStyle). One insert at the end of the tab and one batch of styles."""
    tab_id, content = doc.tab(tab_n)
    end = content[-1]["endIndex"] - 1
    text = "".join("\n" + "".join(t for t, _ in runs) for runs, _ in paras)
    reqs = [{"insertText": {"location": {"index": end, "tabId": tab_id}, "text": text}},
            {"updateTextStyle": {"range": {"startIndex": end, "endIndex": end + len(text), "tabId": tab_id},
                                 "textStyle": {"bold": False, "italic": False, "backgroundColor": {}},
                                 "fields": "bold,italic,backgroundColor"}}]
    at = end + 1
    for runs, pstyle in paras:
        n = sum(len(t) for t, _ in runs)
        reqs.append(_para_req(tab_id, at, at + n + 1, pstyle))
        reqs += _text_reqs(tab_id, at, runs)
        at += n + 1
    doc.batch(reqs)


def _append_table(doc, tab_n, src):
    """A copy of the table element src at the end of the tab: text, run and paragraph styles, cell
    styles, column widths, merges, and the pinned header rows."""
    t = src["table"]
    tab_id, content = doc.tab(tab_n)
    doc.batch([{"insertTable": {"rows": t["rows"], "columns": t["columns"],
                                "endOfSegmentLocation": {"segmentId": "", "tabId": tab_id}}}])
    tab_id, content = doc.tab(tab_n)
    new = ge.top_tables(content)[-1]
    cells = ge.table_cells(new)
    texts = []
    for r, row in enumerate(t["tableRows"]):
        for c, cell in enumerate(row["tableCells"]):
            paras = [p["paragraph"] for p in cell["content"] if "paragraph" in p]
            text = "\n".join("".join(x for x, _ in _runs(p)) for p in paras)
            if text:
                texts.append((cells[r][c]["content"][0]["startIndex"], text))
    reqs = [{"insertText": {"location": {"index": i, "tabId": tab_id}, "text": x}}
            for i, x in sorted(texts, reverse=True)]
    for k in range(0, len(reqs), layout.CHUNK):
        doc.batch(reqs[k:k + layout.CHUNK])
    tab_id, content = doc.tab(tab_n)
    new = ge.top_tables(content)[-1]
    cells = ge.table_cells(new)
    where = {"index": new["startIndex"], "tabId": tab_id}
    reqs = []
    for r, row in enumerate(t["tableRows"]):
        for c, cell in enumerate(row["tableCells"]):
            dst = [p for p in cells[r][c]["content"] if "paragraph" in p]
            srcp = [p["paragraph"] for p in cell["content"] if "paragraph" in p]
            for sp, dp in zip(srcp, dst):
                reqs.append(_para_req(tab_id, dp["startIndex"], dp["endIndex"], sp.get("paragraphStyle", {})))
                reqs += _text_reqs(tab_id, dp["startIndex"], _runs(sp))
            cs = cell.get("tableCellStyle", {})
            fields = [f for f in CELL_FIELDS if f in cs]
            if fields:
                reqs.append({"updateTableCellStyle": {
                    "tableRange": {"tableCellLocation": {"tableStartLocation": where, "rowIndex": r, "columnIndex": c},
                                   "rowSpan": 1, "columnSpan": 1},
                    "tableCellStyle": {f: cs[f] for f in fields}, "fields": ",".join(fields)}})
    for c, prop in enumerate(t.get("tableStyle", {}).get("tableColumnProperties", [])):
        if prop.get("widthType") == "FIXED_WIDTH" and "width" in prop:
            reqs.append({"updateTableColumnProperties": {"tableStartLocation": where, "columnIndices": [c],
                                                         "tableColumnProperties": prop,
                                                         "fields": "widthType,width"}})
    for r, row in enumerate(t["tableRows"]):
        for c, cell in enumerate(row["tableCells"]):
            cs = cell.get("tableCellStyle", {})
            if cs.get("rowSpan", 1) > 1 or cs.get("columnSpan", 1) > 1:
                reqs.append({"mergeTableCells": {"tableRange": {
                    "tableCellLocation": {"tableStartLocation": where, "rowIndex": r, "columnIndex": c},
                    "rowSpan": cs.get("rowSpan", 1), "columnSpan": cs.get("columnSpan", 1)}}})
    pinned = 0
    for row in t["tableRows"]:
        if row.get("tableRowStyle", {}).get("tableHeader"):
            pinned += 1
        else:
            break
    if pinned:
        reqs.append({"pinTableHeaderRows": {"tableStartLocation": where, "pinnedHeaderRowsCount": pinned}})
    heights = [(r, row["tableRowStyle"]["minRowHeight"]) for r, row in enumerate(t["tableRows"])
               if row.get("tableRowStyle", {}).get("minRowHeight", {}).get("magnitude")]
    for r, h in heights:
        reqs.append({"updateTableRowStyle": {"tableStartLocation": where, "rowIndices": [r],
                                             "tableRowStyle": {"minRowHeight": h}, "fields": "minRowHeight"}})
    for k in range(0, len(reqs), layout.CHUNK):
        doc.batch(reqs[k:k + layout.CHUNK])


def _span(content, move):
    """Indexes in content of the first and last element a move takes."""
    heading, first, stop = move[0], move[1], move[2]
    names = [ge.para_text(el).strip() if "paragraph" in el else None for el in content]
    h = names.index(heading)
    a = names.index(first, h) + 1 if first else h + 1
    b = names.index(stop, a)
    return a, b - 1


def step_appendix(doc, tab_n, dry):
    tab_id, content = doc.tab(tab_n)
    names = [ge.para_text(el).strip() if "paragraph" in el else None for el in content]
    if APPENDIX in names:
        raise SystemExit("the tab already has %r; the move has been made" % APPENDIX)
    spans = [_span(content, m) for m in MOVES]
    for m, (a, b) in zip(MOVES, spans):
        kinds = ["T" if "table" in content[k] else "p" for k in range(a, b + 1)]
        print("appendix: %r takes %d elements (%s)" % (m[3], b - a + 1, "".join(kinds)))
        if any("sectionBreak" in content[k] for k in range(a, b + 1)):
            raise SystemExit("a section break lies inside %r" % m[3])
    if dry:
        return
    _append_paragraphs(doc, tab_n, [([(APPENDIX, {})], {"namedStyleType": "HEADING_2"})])
    for m, (a, b) in zip(MOVES, spans):
        _append_paragraphs(doc, tab_n, [([(m[3], {})], {"namedStyleType": "HEADING_3"})])
        group, number = [], 0
        for k in range(a, b + 1):
            el = content[k]
            if "table" in el:
                if group:
                    _append_paragraphs(doc, tab_n, group)
                    group = []
                _append_table(doc, tab_n, el)
                continue
            para = el["paragraph"]
            runs = _runs(para)
            if not runs:
                continue
            if para.get("bullet"):
                number += 1
                runs = [("[%d] " % number, runs[0][1])] + runs
            group.append((runs, para.get("paragraphStyle", {})))
        if group:
            _append_paragraphs(doc, tab_n, group)
    tab_id, content = doc.tab(tab_n)
    names = [ge.para_text(el).strip() if "paragraph" in el else None for el in content]
    k = names.index(APPENDIX)
    doc.batch([{"updateParagraphStyle": {
        "range": {"startIndex": content[k]["startIndex"], "endIndex": content[k]["endIndex"], "tabId": tab_id},
        "paragraphStyle": {"pageBreakBefore": True}, "fields": "pageBreakBefore"}}])
    # The originals go from the last up, each replaced by the line that points to the appendix.
    for m in reversed(MOVES):
        tab_id, content = doc.tab(tab_n)
        a, b = _span(content, m)
        s, e = content[a]["startIndex"], content[b]["endIndex"]
        reqs = [{"deleteContentRange": {"range": {"startIndex": s, "endIndex": e, "tabId": tab_id}}},
                {"insertText": {"location": {"index": s, "tabId": tab_id}, "text": m[4] + "\n"}},
                {"updateTextStyle": {"range": {"startIndex": s, "endIndex": s + len(m[4]), "tabId": tab_id},
                                     "textStyle": {"bold": False, "italic": False, "backgroundColor": {},
                                                   "fontSize": {"magnitude": BODY_PT, "unit": "PT"}},
                                     "fields": "bold,italic,backgroundColor,fontSize"}},
                {"updateParagraphStyle": {"range": {"startIndex": s, "endIndex": s + len(m[4]) + 1, "tabId": tab_id},
                                          "paragraphStyle": {"namedStyleType": "NORMAL_TEXT", "alignment": "START",
                                                             "indentStart": {"magnitude": 0, "unit": "PT"},
                                                             "indentFirstLine": {"magnitude": 0, "unit": "PT"}},
                                          "fields": "namedStyleType,alignment,indentStart,indentFirstLine"}}]
        doc.batch(reqs)
        print("appendix: moved %r" % m[3])


# ------------------------------------------------------------------ flow and table face

def step_flow(doc, tab_n, dry):
    """No forced page inside a part: the hard breaks under "Page N of M" and the page-break-before of
    the subsection headings go. The parts keep theirs, and so do the section breaks. The cover loses
    the two empty lines that push "Hà Nội" onto a page of its own."""
    tab_id, content = doc.tab(tab_n)
    top = charter._below(content, charter.H_PART1)
    reqs = []
    for el in ge.top_paragraphs(content):
        if el["startIndex"] < top:
            continue
        style = el["paragraph"]["paragraphStyle"]
        for e in el["paragraph"]["elements"]:
            if "pageBreak" in e:
                reqs.append((e["startIndex"], {"deleteContentRange": {"range": {
                    "startIndex": e["startIndex"], "endIndex": e["endIndex"], "tabId": tab_id}}}))
        if style.get("pageBreakBefore") and style.get("namedStyleType") not in ("HEADING_1", "HEADING_2"):
            reqs.append((el["startIndex"], {"updateParagraphStyle": {
                "range": {"startIndex": el["startIndex"], "endIndex": el["endIndex"], "tabId": tab_id},
                "paragraphStyle": {"pageBreakBefore": False}, "fields": "pageBreakBefore"}}))
    cover = [el for el in ge.top_paragraphs(content) if el["startIndex"] < top]
    place = next(k for k, el in enumerate(cover) if ge.para_text(el).strip().startswith("Hà Nội"))
    blanks = [el for el in cover[max(0, place - 5):place] if not ge.para_text(el).strip()
              and not any("inlineObjectElement" in e for e in el["paragraph"]["elements"])][:2]
    for el in blanks:
        reqs.append((el["startIndex"], {"deleteContentRange": {"range": {
            "startIndex": el["startIndex"], "endIndex": el["endIndex"], "tabId": tab_id}}}))
    print("flow: %d forced breaks off, %d empty cover lines removed" % (len(reqs) - len(blanks), len(blanks)))
    if not dry and reqs:
        doc.batch([r for _, r in sorted(reqs, key=lambda x: x[0], reverse=True)])


def step_tables(doc, tab_n, dry, old=10, new=9):
    """Table text set in `old` pt goes to `new` pt; smaller faces are left as they are."""
    tab_id, content = doc.tab(tab_n)
    top = charter._below(content, charter.H_PART1)
    reqs = []

    def walk(elements):
        for el in elements:
            if "table" in el:
                for row in el["table"]["tableRows"]:
                    for cell in row["tableCells"]:
                        walk(cell["content"])
            elif "paragraph" in el:
                for e in el["paragraph"]["elements"]:
                    size = e.get("textRun", {}).get("textStyle", {}).get("fontSize", {}).get("magnitude")
                    if size == old:
                        reqs.append({"updateTextStyle": {
                            "range": {"startIndex": e["startIndex"], "endIndex": e["endIndex"], "tabId": tab_id},
                            "textStyle": {"fontSize": {"magnitude": new, "unit": "PT"}}, "fields": "fontSize"}})

    for el in content:
        if "table" in el and el["startIndex"] > top:
            walk([el])
    print("tables: %d runs from %d to %d pt" % (len(reqs), old, new))
    if not dry:
        for k in range(0, len(reqs), layout.CHUNK):
            doc.batch(reqs[k:k + layout.CHUNK])


# ------------------------------------------------------------------ reading conventions, table face, landscape

LANDSCAPE_WIDTH = 648  # points across a landscape Letter page inside 1-inch margins
PORTRAIT_WIDTH = 468


def step_no_reading(doc, tab_n, dry):
    """Every "Reading convention" heading with the paragraphs under it, up to the next heading, table,
    section break, or empty line (the empty line before a table cannot be deleted with it)."""
    tab_id, content = doc.tab(tab_n)
    spans = []
    for k, el in enumerate(content):
        if "paragraph" not in el or ge.para_text(el).strip() != "Reading convention":
            continue
        j = k + 1
        while j < len(content):
            nxt = content[j]
            if "paragraph" not in nxt or not ge.para_text(nxt).strip():
                break
            if nxt["paragraph"]["paragraphStyle"].get("namedStyleType", "").startswith("HEADING"):
                break
            j += 1
        spans.append((el["startIndex"], content[j - 1]["endIndex"]))
    print("reading conventions: %d to delete, %d characters" % (len(spans), sum(e - s for s, e in spans)))
    if not dry and spans:
        doc.batch([{"deleteContentRange": {"range": {"startIndex": s, "endIndex": e, "tabId": tab_id}}}
                   for s, e in sorted(spans, reverse=True)])


def step_table_size(doc, tab_n, dry, size=BODY_PT):
    """Every run of every table below the cover at `size` pt."""
    tab_id, content = doc.tab(tab_n)
    top = charter._below(content, charter.H_PART1)
    reqs = []

    def walk(elements):
        for el in elements:
            if "table" in el:
                for row in el["table"]["tableRows"]:
                    for cell in row["tableCells"]:
                        walk(cell["content"])
            elif "paragraph" in el:
                for e in el["paragraph"]["elements"]:
                    run = e.get("textRun")
                    if run and run.get("textStyle", {}).get("fontSize", {}).get("magnitude") != size:
                        reqs.append({"updateTextStyle": {
                            "range": {"startIndex": e["startIndex"], "endIndex": e["endIndex"], "tabId": tab_id},
                            "textStyle": {"fontSize": {"magnitude": size, "unit": "PT"}}, "fields": "fontSize"}})

    walk([el for el in content if "table" in el and el["startIndex"] > top])
    print("table face: %d runs to %d pt" % (len(reqs), size))
    if not dry:
        for k in range(0, len(reqs), layout.CHUNK):
            doc.batch(reqs[k:k + layout.CHUNK])


def step_landscape(doc, tab_n, dry):
    """Everything below the cover on landscape pages: a section break before Part 1 (which no longer
    needs its own page break), every section after it turned, and the tables laid out for a portrait
    page widened in proportion to the landscape page."""
    tab_id, content = doc.tab(tab_n)
    head = charter._find(content, charter.H_PART1)
    k = next(i for i, el in enumerate(content) if el.get("startIndex") == head["startIndex"])
    has_break = any("sectionBreak" in el for el in content[max(0, k - 2):k])
    print("landscape: %s section break before Part 1" % ("keep the" if has_break else "insert a"))
    if dry:
        return
    if not has_break:
        doc.batch([{"insertSectionBreak": {"location": {"index": head["startIndex"], "tabId": tab_id},
                                           "sectionType": "NEXT_PAGE"}}])
    tab_id, content = doc.tab(tab_n)
    head = charter._find(content, charter.H_PART1)
    end = content[-1]["endIndex"] - 1
    doc.batch([
        {"updateParagraphStyle": {"range": {"startIndex": head["startIndex"], "endIndex": head["endIndex"], "tabId": tab_id},
                                  "paragraphStyle": {"pageBreakBefore": False}, "fields": "pageBreakBefore"}},
        {"updateSectionStyle": {"range": {"startIndex": head["startIndex"], "endIndex": end, "tabId": tab_id},
                                "sectionStyle": {"flipPageOrientation": True}, "fields": "flipPageOrientation"}}])
    tab_id, content = doc.tab(tab_n)
    head = charter._find(content, charter.H_PART1)
    reqs = []
    for el in ge.top_tables(content):
        if el["startIndex"] < head["startIndex"]:
            continue
        props = el["table"].get("tableStyle", {}).get("tableColumnProperties", [])
        widths = [p.get("width", {}).get("magnitude") for p in props]
        if not widths or None in widths or sum(widths) > PORTRAIT_WIDTH + 2:
            continue
        factor = LANDSCAPE_WIDTH / sum(widths)
        where = {"index": el["startIndex"], "tabId": tab_id}
        for c, w in enumerate(widths):
            reqs.append({"updateTableColumnProperties": {
                "tableStartLocation": where, "columnIndices": [c],
                "tableColumnProperties": {"widthType": "FIXED_WIDTH",
                                          "width": {"magnitude": round(w * factor, 1), "unit": "PT"}},
                "fields": "widthType,width"}})
    print("landscape: %d column widths scaled" % len(reqs))
    for k in range(0, len(reqs), layout.CHUNK):
        doc.batch(reqs[k:k + layout.CHUNK])


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--doc", required=True)
    p.add_argument("--token", default=os.path.join(DEFAULT_DIR, "token.json"))
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--layout", action="store_true", help="rerun only the layout pass of Parts 1 and 2")
    for flag in ("charter", "prose", "schedule", "font", "appendix", "flow", "tables",
                 "no_reading", "table_size", "landscape"):
        p.add_argument("--" + flag.replace("_", "-"), action="store_true")
    a = p.parse_args(argv)
    check_texts()
    # A read the API never answers otherwise holds the run for an hour; every step can be run again.
    socket.setdefaulttimeout(180)

    import gdoc

    doc = layout.Doc(layout.docs_service(gdoc.load_creds(pathlib.Path(a.token))), a.doc)
    tab_n = _tab(doc)
    if a.charter:
        step_charter(doc, tab_n, a.dry_run)
    if a.layout and not a.dry_run:
        charter.lay_out(doc, tab_n)
    if a.prose:
        step_prose(doc, tab_n, a.dry_run)
    if a.schedule:
        step_schedule(doc, tab_n, a.dry_run)
    if a.font:
        step_font(doc, tab_n, a.dry_run)
    if a.appendix:
        step_appendix(doc, tab_n, a.dry_run)
    if a.flow:
        step_flow(doc, tab_n, a.dry_run)
    if a.tables:
        step_tables(doc, tab_n, a.dry_run)
    if a.no_reading:
        step_no_reading(doc, tab_n, a.dry_run)
    if a.table_size:
        step_table_size(doc, tab_n, a.dry_run)
    if a.landscape:
        step_landscape(doc, tab_n, a.dry_run)
    print("done, %d API calls" % doc.calls)
    return 0


if __name__ == "__main__":
    sys.exit(main())
