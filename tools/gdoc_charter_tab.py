#!/usr/bin/env python3
"""Write the requirement specification and the project charter into the Product Charter tab of the Doc.

The content is derived from Parts 1 and 2 of docs/charter-package.en.md; nothing is authored here but
the three reading conventions, which say where each part comes from in the book and how it joins the
other tabs. What the Doc needs and the repo file does not, so that this tab reads like tabs 5 to 10:

  - the parts are headed "1: Requirement Specification" and "2: Project Charter", and 2A and 2B of the
    source become 2.1 Charter Elements and 2.2 Project Charter, with the references to them renamed;
  - each part opens with a "Reading convention" paragraph naming the form, its PDF and printed pages,
    and the PMBOK 6 section it is the output of, in place of the source's italic lines;
  - form 1.1 is laid out as the book prints it: one table per printed page under the dark PROJECT
    CHARTER bar, each label on a line of its own above its box, Project Sponsor beside Date Prepared
    and Project Manager beside Project Customer, the objectives and the milestones under their printed
    column heads, the Approvals block of two columns, and "Page N of 4" under each page;
  - the notes the source prints under the milestones and the Approvals move into the reading
    convention, since the form prints no such text;
  - headings are in Arial, tables in the 10 pt face with their header rows repeated, and each part
    and each printed page opens a new page.

The cover page above "1: Requirement Specification" is the team's and is never touched.

Run with:
    python3 tools/gdoc_charter_tab.py --doc DOC_ID --dry-run
    python3 tools/gdoc_charter_tab.py --doc DOC_ID --preview FILE   # write the tab text and stop
    python3 tools/gdoc_charter_tab.py --doc DOC_ID --clear          # rewrite everything below the cover
    python3 tools/gdoc_charter_tab.py --doc DOC_ID --finish         # rerun only the layout pass
"""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc_cost_tab as layout
import gdoc_edit as ge
import gdoc_form

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs" / "charter-package.en.md"
DEFAULT_DIR = os.path.expanduser("~/.config/qldapm")
TAB = "Product Charter"
H_PART1 = "1: Requirement Specification"
H_PART2 = "2: Project Charter"
H_ELEMENTS = "2.1 Charter Elements"
H_FORM = "2.2 Project Charter"
TITLE = "PROJECT CHARTER"
PAGE = "@@PAGE {}@@"
PAGES = 4

REWRITES = [
    ("Signature on the charter form in section 2B", "Signature on the charter form in section 2.2"),
    ("Quantified business case in section 2A", "Quantified business case in section 2.1"),
]

READING_1 = (
    "Form 2.8 Project Scope Statement, A Project Manager's Book of Forms, 3rd edition, PDF pages 58 to "
    "59 (printed pages 47 to 48), filled as the project scope statement of PMBOK 6 section 5.3.3.1, "
    "printed page 154 (PDF page 193). The book's tailoring tips combine it with the charter on a small "
    "project (PDF page 14, printed page 3). The functions F01 to F12 sit in the Project Scope "
    "Description and the measurable targets in the Product Acceptance Criteria. The brief fixes only the budget, the duration, and the team size; "
    "<mark>highlighted</mark> content is assumed rather than given, for the team to confirm, and each "
    "assumed figure is listed in section 1.6. Design choices such as the function set are not "
    "highlighted. Assumptions 1 to 19 are kept, with an owner, a due date, and a status, in form 1.2 "
    "Assumption Log of section 10 under the same numbers."
)

READING_21 = (
    "Table 1.1 Elements of a Project Charter, A Project Manager's Book of Forms, 3rd edition, PDF pages "
    "13 to 15 (printed pages 2 to 4): the fourteen elements in the book's order, with the detail the "
    "boxes of the form in section 2.2 have no room for. Together they are the project charter of "
    "PMBOK 6 section 4.1.3.1, printed page 81 (PDF page 120), as committed on 16 September 2026 and "
    "amended on 14 November 2026. The change requests pending against it, among them the scope and "
    "cost request of section 5.7, change nothing here until the sponsor decides them. Risks R1 to R12 "
    "are those identified at chartering; form 2.32 Risk Register of section 8 keeps their numbers and "
    "adds R13 to R18. The Key stakeholder list holds the twenty rows of form 1.3 Stakeholder Register "
    "of section 9.1, S01 to S20, in the same order."
)

READING_22 = (
    "Form 1.1 Project Charter, A Project Manager's Book of Forms, 3rd edition, PDF pages 16 to 19 "
    "(printed pages 5 to 8), filled from section 2.1. Field names and field order are as printed; each "
    "printed page is one table under the PROJECT CHARTER bar, and Page N of 4 counts printed pages, "
    "one of which may run over two pages of this Doc. The Project Manager box, the signatures, and the "
    "dates are empty: the sponsor appoints the project manager at M0 (assumption 15), and the rest is "
    "completed on signing. <mark>Highlighted</mark> content is assumed rather than given. M6 to M7 is "
    "the first month of the six-month warranty; months 2 to 6 run after closeout to <mark>5 July "
    "2027</mark> under budget line 5. The pilot, the parallel run, and the store dates behind the "
    "Summary Milestones are under Summary milestone schedule in section 2.1."
)

# Points across the 468pt of a portrait page, keyed by the header row of each table outside the form.
WIDTHS = {
    ("Role", "Who they are", "What they do with the system"): [96, 112, 260],
    ("ID", "Function", "Primary actor", "Description"): [30, 96, 80, 262],
    ("Situation", "Required behaviour"): [150, 318],
    ("#", "Deliverable", "For", "Due at"): [32, 300, 64, 72],
    ("Internal deliverable", "Produced"): [268, 200],
    ("ID", "Category", "Criterion"): [34, 96, 338],
    ("#", "Assumption"): [28, 440],
    ("Loss today", "Value today", "What the project changes"): [110, 170, 188],
    ("", "Amount"): [140, 328],
    ("Severity", "Meaning", "Response", "Workaround or fix"): [80, 180, 90, 118],
    ("#", "Type", "Risk", "Response"): [30, 54, 180, 204],
    ("Objective area", "Objective", "Success criteria"): [80, 150, 238],
    ("ID", "Milestone", "Due date"): [30, 338, 100],
    ("#", "Category", "Amount (VND)", "Share", "Basis"): [22, 150, 82, 40, 174],
    ("Stakeholder", "Role in the project"): [170, 298],
    ("To be approved", "Approved by", "Evidence"): [120, 170, 178],
}
FORM_WIDTHS = [234, 234]


# ------------------------------------------------------------------ content

def _plain(md: str) -> str:
    return ge.parse_inline(md)[0].strip()


def _drop_notes(md: str) -> str:
    """The source's italic lines and rules: the reading conventions take their place."""
    md = re.sub(r"^\*[^*].*\*\s*$\n?", "", md, flags=re.M)
    md = re.sub(r"^---\s*$\n?", "", md, flags=re.M)
    return md


def _row(*cells) -> str:
    return "| " + " | ".join(cells) + " |"


def _label(text: str, colon: bool = True) -> str:
    return "**%s%s**" % (text, ":" if colon else "")


def _fields(p2b: str) -> dict:
    """Every Field | Content row of the form, keyed by its plain label. The Project Manager Authority
    Level table is one of them; the stakeholder table is not, though it also has two columns and a
    Project Manager row."""
    out = {}
    for block in ge.parse_blocks(p2b):
        if (block["type"] == "table" and block["rows"]
                and _plain(block["rows"][0][0]) in ("Field", "Project Manager Authority Level")):
            for row in block["rows"]:
                out[_plain(row[0])] = row[1]
    return out


def _table_starting(p2b: str, first: str):
    for block in ge.parse_blocks(p2b):
        if block["type"] == "table" and _plain(block["rows"][0][0]) == first:
            return block
    raise SystemExit("form table starting %r not found in the source" % first)


def _box(rows, label, value, colon=True):
    rows.append(_row(_label(label, colon), ""))
    rows.append(_row(value, ""))


def build_form(p2b: str) -> str:
    """The four printed pages, each one two-column table. A row whose second cell is empty is merged
    across the table by the layout pass: that is a label line or the box under it."""
    f = _fields(p2b)
    need = ["Project Title", "Project Sponsor", "Date Prepared", "Project Manager", "Project Customer",
            "Project Purpose", "High-Level Project Description", "Project Boundaries", "Key Deliverables",
            "High-Level Requirements", "Overall Project Risk", "Preapproved Financial Resources",
            "Project Exit Criteria", "Staffing Decisions", "Budget Management and Variance",
            "Technical Decisions", "Conflict Resolution", "Sponsor Authority"]
    missing = [k for k in need if k not in f]
    if missing:
        raise SystemExit("form fields missing from the source: %s" % missing)

    def inline(label, value):
        return ("%s %s" % (_label(label), value)).strip()

    p1 = [_row(inline("Project Title", f["Project Title"]), ""),
          _row(inline("Project Sponsor", f["Project Sponsor"]), inline("Date Prepared", f["Date Prepared"])),
          _row(inline("Project Manager", f["Project Manager"]), inline("Project Customer", f["Project Customer"]))]
    for k in need[5:10]:
        _box(p1, k, f[k])
    _box(p1, "Overall Project Risk", f["Overall Project Risk"], colon=False)

    objectives = _table_starting(p2b, "")
    milestones = _table_starting(p2b, "Summary Milestones")
    p2 = [_row("**Project Objectives**", "**Success Criteria**")]
    for row in objectives["rows"][1:]:
        p2.append(_row(_label(_plain(row[0])), ""))
        p2.append(_row(row[1], row[2]))
    p2.append(_row("**Summary Milestones**", "**Due Date**"))
    p2 += [_row(*row) for row in milestones["rows"][1:]]

    stakeholders = _table_starting(p2b, "Stakeholder(s)")
    p3 = []
    _box(p3, "Preapproved Financial Resources", f["Preapproved Financial Resources"])
    p3.append(_row("**Stakeholder(s)**", "**Role**"))
    p3 += [_row(*row) for row in stakeholders["rows"][1:]]
    _box(p3, "Project Exit Criteria", f["Project Exit Criteria"])
    p3.append(_row(_label("Project Manager Authority Level"), ""))
    _box(p3, "Staffing Decisions", f["Staffing Decisions"])
    _box(p3, "Budget Management and Variance", f["Budget Management and Variance"])

    approvals = [b for b in ge.parse_blocks(p2b) if b["type"] == "table" and
                 [_plain(c) for c in b["rows"][0]] == ["", "Project Manager", "Sponsor or Originator"]]
    if len(approvals) != 1:
        raise SystemExit("the Approvals table was not found once in the source")
    signed = {_plain(r[0]): r[1:] for r in approvals[0]["rows"][1:]}
    p4 = []
    for k in ("Technical Decisions", "Conflict Resolution", "Sponsor Authority"):
        _box(p4, k, f[k])
    p4.append(_row(_label("Approvals"), ""))
    for what, pm_label, sp_label in (("Signature", "Project Manager Signature", "Sponsor or Originator Signature"),
                                     ("Name", "Project Manager Name", "Sponsor or Originator Name"),
                                     ("Date", "Date", "Date")):
        pm, sp = signed[what]
        p4.append(_row(pm or " ", sp or " "))
        p4.append(_row("**%s**" % pm_label, "**%s**" % sp_label))

    pages = []
    for n, rows in enumerate((p1, p2, p3, p4), start=1):
        pages.append("\n".join(rows) + "\n\n" + PAGE.format("Page %d of %d" % (n, PAGES)))
    return "\n\n".join(pages) + "\n"


def build() -> str:
    md = SOURCE.read_text(encoding="utf-8")
    for old, new in REWRITES:
        if md.count(old) != 1:
            raise SystemExit("expected text not found once in the charter source: %r" % old[:60])
        md = md.replace(old, new)
    p1 = ge.section(md, "## Part 1", "## Part 2")
    p2a = ge.section(md, "### 2A.", "### 2B.")
    p2b = ge.section(md, "### 2B.", "## Part 3")

    p1 = _drop_notes(p1.split("\n", 1)[1])
    title = re.search(r"^\*\*Project Title:\*\*.*$", p1, re.M).group(0)
    date = re.search(r"^\*\*Date Prepared:\*\*.*$", p1, re.M).group(0)
    p1 = p1.replace(title + "\n", "").replace(date + "\n", "")
    p2a = _drop_notes(p2a.split("\n", 1)[1])

    text = "\n\n".join([
        "## " + H_PART1, "#### Reading convention", READING_1, title, date, p1.strip(),
        "## " + H_PART2, "### " + H_ELEMENTS, "#### Reading convention", READING_21, p2a.strip(),
        "### " + H_FORM, "#### Reading convention", READING_22, build_form(p2b).strip(),
    ]) + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    for bad in ("`", "<br", "<ins>", ".md", "section 2A", "section 2B", "Part 2A", "Part 2B", "\u2014", "\u2013"):
        if bad in text:
            raise SystemExit("%r is left in the tab text" % bad)
    return text


# ------------------------------------------------------------------ layout

def _header(el):
    return tuple(_plain(ge.cell_text(c)) for c in ge.table_cells(el)[0])


def _find(content, heading):
    try:
        return ge.find_para(content, lambda t: t.strip() == heading)
    except KeyError:
        return None


def _below(content, heading):
    el = _find(content, heading)
    if el is None:
        raise SystemExit("heading %r not found in the tab" % heading)
    return el["startIndex"]


def _stop(content):
    """Where Part 2 ends in a tab that goes on after it, as the report tab does: the first section
    break or part heading below the form. None in the Product Charter tab, where Part 2 runs to the end."""
    form_at = _below(content, H_FORM)
    for el in content:
        if el.get("startIndex", 0) <= form_at:
            continue
        style = el.get("paragraph", {}).get("paragraphStyle", {}).get("namedStyleType", "")
        if "sectionBreak" in el or style in ("HEADING_1", "HEADING_2"):
            return el["startIndex"]
    return None


def lay_out(doc, tab_n):
    """Tables from the last up, so that the start index of the ones above stays valid. A form table that
    already has its title bar and a footer already written are left alone, so an interrupted pass can be
    run again with --finish."""
    tab_id, content = doc.tab(tab_n)
    top, form_at, stop = _below(content, H_PART1), _below(content, H_FORM), _stop(content)
    starts = [el["startIndex"] for el in ge.top_tables(content)
              if el["startIndex"] > top and (stop is None or el["startIndex"] < stop)]
    form = [s for s in starts if s > form_at]
    if len(form) != PAGES:
        raise SystemExit("expected %d form tables, found %d" % (PAGES, len(form)))
    for start in reversed(starts):
        tab_id, table_el = layout._table(doc, tab_n, start)
        if start in form:
            rows = ge.table_cells(table_el)
            if ge.cell_text(rows[0][0]).strip() == TITLE:
                continue
            merges = [gdoc_form.merge(tab_id, table_el, r, 0, 1, 2)
                      for r in range(len(rows) - 1, -1, -1)
                      if ge.cell_text(rows[r][0]).strip() and not ge.cell_text(rows[r][1]).strip()]
            doc.batch(merges + gdoc_form.column_widths(tab_id, table_el, FORM_WIDTHS))
            layout.small_text(doc, tab_n, start, 0, layout.TEXT)
            layout.full_row(doc, tab_n, start, 0, "**%s**" % TITLE, background=gdoc_form.DARK, center=True)
            layout.whiten_title(doc, tab_n, start)
            layout.keep_rows(doc, tab_n, start, 1)
        else:
            head = _header(table_el)
            if head not in WIDTHS:
                raise SystemExit("no column widths for the table headed %r" % (head,))
            doc.batch(gdoc_form.column_widths(tab_id, table_el, WIDTHS[head]))
            layout.small_text(doc, tab_n, start, 1, layout.TEXT)
            layout.keep_rows(doc, tab_n, start, 1)
    for n in range(1, PAGES + 1):
        try:
            layout.footer_line(doc, tab_n, "Page %d of %d" % (n, PAGES))
        except KeyError:
            pass
    breaks(doc, tab_n)
    finish(doc, tab_n)


def finish(doc, tab_n):
    """The closing pass of the other tabs (layout.finish) restricted to what lies below the cover: the
    numbered items of a box on lines of their own, paragraph spacing, headings in Arial, the line over
    each table kept with it, and no empty paragraph at the end of the tab. The cover keeps the spacing
    the team gave it."""
    tab_id, content = doc.tab(tab_n)
    top, stop = _below(content, H_PART1), _stop(content)
    end = stop if stop is not None else content[-1]["endIndex"]
    layout.number_lines(doc, tab_n, within=(top, end))
    tab_id, content = doc.tab(tab_n)
    top, stop = _below(content, H_PART1), _stop(content)
    end = stop if stop is not None else content[-1]["endIndex"]

    def ours(req):
        body = next(iter(req.values()))
        return top <= body["range"]["startIndex"] < end

    reqs = [r for r in layout.spacing(content, tab_id) if ours(r)]
    kept = set()
    for k, el in enumerate(content):
        if not top <= el.get("startIndex", 0) < end:
            continue
        style = el.get("paragraph", {}).get("paragraphStyle", {})
        if style.get("namedStyleType", "").startswith("HEADING"):
            reqs.append({"updateTextStyle": {
                "range": {"startIndex": el["startIndex"], "endIndex": el["endIndex"] - 1, "tabId": tab_id},
                "textStyle": {"weightedFontFamily": {"fontFamily": "Arial"}}, "fields": "weightedFontFamily"}})
        if "table" not in el:
            continue
        for prev in reversed(content[max(0, k - 3):k]):
            text = ge.para_text(prev).strip() if "paragraph" in prev else None
            if text is None or re.match(r"^Page \d+ of \d+$", text):
                break
            kept.add(prev["startIndex"])
            if text:
                break
    for el in content:
        style = el.get("paragraph", {}).get("paragraphStyle", {})
        if ("paragraph" in el and top <= el["startIndex"] < end
                and style.get("namedStyleType", "NORMAL_TEXT") == "NORMAL_TEXT"):
            reqs.append({"updateParagraphStyle": {
                "range": {"startIndex": el["startIndex"], "endIndex": el["endIndex"], "tabId": tab_id},
                "paragraphStyle": {"keepWithNext": el["startIndex"] in kept}, "fields": "keepWithNext"}})
    doc.batch(reqs)
    if stop is not None:
        return
    tab_id, content = doc.tab(tab_n)
    last, before = content[-1], content[-2]
    if ge.para_text(last).strip() or "paragraph" in before:
        if "paragraph" in before and not ge.para_text(last).strip():
            align = before["paragraph"].get("paragraphStyle", {}).get("alignment", "START")
            doc.batch([{"deleteContentRange": {"range": {"startIndex": before["endIndex"] - 1,
                                                         "endIndex": before["endIndex"], "tabId": tab_id}}}])
            tab_id, content = doc.tab(tab_n)
            el = content[-1]
            doc.batch([{"updateParagraphStyle": {
                "range": {"startIndex": el["startIndex"], "endIndex": el["endIndex"], "tabId": tab_id},
                "paragraphStyle": {"alignment": align}, "fields": "alignment"}}])


def breaks(doc, tab_n):
    """Each part and the form open a page; each printed page of the form ends with a hard break."""
    tab_id, content = doc.tab(tab_n)
    reqs = []
    for el in ge.top_paragraphs(content):
        if ge.para_text(el).strip() in (H_PART1, H_PART2, H_FORM):
            reqs.append({"updateParagraphStyle": {
                "range": {"startIndex": el["startIndex"], "endIndex": el["endIndex"], "tabId": tab_id},
                "paragraphStyle": {"pageBreakBefore": True}, "fields": "pageBreakBefore"}})
    doc.batch(reqs)
    for n in range(PAGES - 1, 0, -1):
        tab_id, content = doc.tab(tab_n)
        el = ge.find_para(content, lambda t, n=n: t.strip() == "Page %d of %d" % (n, PAGES))
        if any("pageBreak" in e for e in el["paragraph"]["elements"]):
            continue
        doc.batch([{"insertPageBreak": {"location": {"index": el["endIndex"] - 1, "tabId": tab_id}}}])


# ------------------------------------------------------------------ main

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--doc", required=True)
    p.add_argument("--tab", default=TAB)
    p.add_argument("--token", default=os.path.join(DEFAULT_DIR, "token.json"))
    p.add_argument("--clear", action="store_true", help="delete everything below the cover page first")
    p.add_argument("--finish", action="store_true", help="rerun only the layout pass")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--preview", default="", help="write the tab text to this file and stop")
    a = p.parse_args(argv)

    text = build()
    tables = sum(1 for b in ge.parse_blocks(text) if b["type"] == "table")
    print("payload: %d characters, %d tables" % (len(text), tables))
    if a.preview:
        pathlib.Path(a.preview).write_text(text, encoding="utf-8")
        print("preview written to %s" % a.preview)
        return 0
    if a.dry_run:
        return 0

    import gdoc

    creds = gdoc.load_creds(pathlib.Path(a.token))
    doc = layout.Doc(layout.docs_service(creds), a.doc)
    names = [t[0].strip() for t in doc.tabs()]
    if a.tab not in names:
        raise SystemExit("no tab %r in this Doc; tabs present: %s" % (a.tab, names))
    tab_n = names.index(a.tab)
    if a.finish:
        lay_out(doc, tab_n)
        print("done, %d API calls" % doc.calls)
        return 0

    tab_id, content = doc.tab(tab_n)
    head = _find(content, H_PART1)
    if head is None:
        raise SystemExit("no %r heading in the tab: the cover page cannot be told apart" % H_PART1)
    end = content[-1]["endIndex"] - 1
    if end > head["startIndex"] + 1:
        if not a.clear:
            raise SystemExit("the tab already holds content below the cover; run with --clear to rewrite it")
        doc.delete_range(tab_id, head["startIndex"], end)
    doc.insert_markdown(tab_n, doc.content(tab_n)[-1]["endIndex"] - 1, text)
    print("  wrote parts 1 and 2 (%d API calls)" % doc.calls)
    lay_out(doc, tab_n)
    print("done, %d API calls" % doc.calls)
    return 0


if __name__ == "__main__":
    sys.exit(main())
