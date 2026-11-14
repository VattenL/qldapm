#!/usr/bin/env python3
"""Write the stakeholder register and the stakeholder analysis into one tab of the Doc.

The content is derived from docs/forms/1-3-stakeholder-register.en.md and
1-4-stakeholder-analysis.en.md; nothing is authored here. What the Doc needs and the repo files do not:

  - the scope change request is named by its section 5.7, and the sibling forms by their sections;
  - each italic reading convention becomes a headed paragraph, as in the other tabs, and the levels
    and the interest and influence grid of form 1.4 sit under their own headings;
  - the tab is landscape, as the book prints both forms, and each form is laid out as printed: the dark
    title bar and the Project Title and Date Prepared line over the table, the grid in the small face,
    the header repeated on a page the table runs onto, and "Page 1 of 1" under it;
  - form 1.4 starts on a new page;
  - headings are in Arial, and the tab ends on its last line rather than on an empty paragraph.

Run with:
    python3 tools/gdoc_stakeholder_tab.py --doc DOC_ID --dry-run
    python3 tools/gdoc_stakeholder_tab.py --doc DOC_ID --preview FILE   # write the tab text and stop
    python3 tools/gdoc_stakeholder_tab.py --doc DOC_ID --create         # add the tab, then write it
    python3 tools/gdoc_stakeholder_tab.py --doc DOC_ID --clear          # rewrite a tab written before
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
FORMS = ROOT / "docs" / "forms"
REGISTER = FORMS / "1-3-stakeholder-register.en.md"
ANALYSIS = FORMS / "1-4-stakeholder-analysis.en.md"
DEFAULT_DIR = os.path.expanduser("~/.config/qldapm")
TAB = "9: Stakeholders"
H_REGISTER = "9.1 Stakeholder Register"
H_ANALYSIS = "9.2 Stakeholder Analysis"
PROJECT = "Development and Deployment of a Learning Center Management Software"
PAGE = "@@PAGE {}@@"
FOOTER = "Page 1 of 1"
# Points across the 648pt of a landscape page, one list per table in the order the tab prints them:
# the register, the levels of form 1.4, the analysis, the grid.
WIDTHS = [[30, 72, 112, 72, 126, 136, 100],
          [60, 294, 294],
          [30, 130, 160, 178, 150],
          [110, 269, 269]]
# The printed forms among those tables, with their title bars.
FORM_TABLES = {0: "STAKEHOLDER REGISTER", 2: "STAKEHOLDER ANALYSIS"}
# Rows each table repeats on a page it runs onto: for a form, the title bar, the Project Title line and
# the column header; otherwise the column header.
PINNED = [3, 1, 3, 1]

REGISTER_REWRITES = [
    ("form 2.28 Resource Requirements, and form 2.32 Risk Register version 1.1.",
     "form 2.28 Resource Requirements of section 7.2, and form 2.32 Risk Register version 1.1 of section 8."),
    ("form 1.4 Stakeholder Analysis can be matched", "form 1.4 Stakeholder Analysis of section 9.2 can be matched"),
    ("The scope change request of 8 October 2026 (form 3.3) is pending",
     "The scope change request of 8 October 2026, section 5.7, is pending"),
]
ANALYSIS_REWRITES = [
    ("stakeholders of form 1.3 Stakeholder Register, with",
     "stakeholders of form 1.3 Stakeholder Register of section 9.1, with"),
]
TITLE_LINES = re.compile(r"^\*\*(Project Title|Date Prepared):\*\* .*\n", re.M)
NOTE = re.compile(r"^\*([^*].*)\*$", re.M)


def read(path: pathlib.Path, rewrites) -> str:
    md = path.read_text(encoding="utf-8")
    for old, new in rewrites:
        if old not in md:
            raise SystemExit("expected text not found in %s, the source has changed: %r" % (path.name, old[:60]))
        md = md.replace(old, new)
    return md


def date_of(md: str) -> str:
    return re.search(r"^\*\*Date Prepared:\*\* (.+)$", md, re.M).group(1).strip()


def notes_of(md: str) -> str:
    notes = NOTE.findall(md)
    if not notes:
        raise SystemExit("no reading convention found")
    return "\n\n".join(notes)


def body_of(md: str) -> str:
    """The form without its title, its reading convention and its title block; its own second-level
    headings become the tab's fourth level, under the form's third-level heading."""
    md = re.sub(r"^# .*\n", "", md, count=1, flags=re.M)
    md = TITLE_LINES.sub("", NOTE.sub("", md))
    md = re.sub(r"^## ", "#### ", md, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", md).strip("\n") + "\n"


def with_footer(body: str, form_header: str) -> str:
    """The page marker straight after the printed table, so that "Page 1 of 1" closes the form and not
    the grid or notes that follow it."""
    lines = body.splitlines()
    at = next(k for k, line in enumerate(lines) if line.startswith(form_header))
    end = at
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    lines[end:end] = ["", PAGE.format(FOOTER)]
    return "\n".join(lines) + "\n"


def build() -> tuple[str, str]:
    """(date prepared, tab text)."""
    register = read(REGISTER, REGISTER_REWRITES)
    analysis = read(ANALYSIS, ANALYSIS_REWRITES)
    dates = {date_of(register), date_of(analysis)}
    if len(dates) != 1:
        raise SystemExit("the two forms carry different Date Prepared values: %s" % sorted(dates))
    date = dates.pop()

    def part(heading, md, form_header):
        return "### %s\n\n#### Reading convention\n\n%s\n\n%s" % (
            heading, notes_of(md), with_footer(body_of(md), form_header))

    text = "## %s\n\n%s\n%s" % (TAB, part(H_REGISTER, register, "| ID | Name |"),
                                part(H_ANALYSIS, analysis, "| ID | Name or Role |"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    if "`" in text or "<br" in text or "<ins>" in text or ".md" in text or "form 3.3" in text:
        raise SystemExit("a repo reference, an ins tag, or a <br> is left in the tab text")
    return date, text


def lay_out(doc, tab_n, date):
    """Each table from the last up, so that the start index of the ones above stays valid: widths and
    face, then for a printed form the Project Title line and the title bar over it; last the footers and
    the page break before form 1.4."""
    def starts():
        return [el["startIndex"] for el in ge.top_tables(doc.content(tab_n))]

    if len(starts()) != len(WIDTHS):
        raise SystemExit("expected %d tables in the tab, found %d" % (len(WIDTHS), len(starts())))
    project = "**Project Title:** %s          **Date Prepared:** %s" % (PROJECT, date)
    for k in range(len(WIDTHS) - 1, -1, -1):
        start = starts()[k]
        tab_id, table_el = layout._table(doc, tab_n, start)
        doc.batch(gdoc_form.column_widths(tab_id, table_el, WIDTHS[k]))
        if k in FORM_TABLES:
            layout.small_text(doc, tab_n, start, 1, layout.SMALL)
            layout.full_row(doc, tab_n, start, 0, project)
            layout.full_row(doc, tab_n, start, 0, "**%s**" % FORM_TABLES[k], background=gdoc_form.DARK,
                            center=True)
            layout.whiten_title(doc, tab_n, start)
        else:
            layout.small_text(doc, tab_n, start, 1, layout.TEXT)
        layout.keep_rows(doc, tab_n, start, PINNED[k])
    for _form in FORM_TABLES:
        layout.footer_line(doc, tab_n, FOOTER)
    tab_id, content = doc.tab(tab_n)
    el = ge.find_para(content, lambda t: t.strip() == H_ANALYSIS)
    doc.batch([{"updateParagraphStyle": {
        "range": {"startIndex": el["startIndex"], "endIndex": el["endIndex"], "tabId": tab_id},
        "paragraphStyle": {"pageBreakBefore": True}, "fields": "pageBreakBefore"}}])
    layout.finish(doc, tab_n)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--doc", required=True)
    p.add_argument("--tab", default=TAB)
    p.add_argument("--token", default=os.path.join(DEFAULT_DIR, "token.json"))
    p.add_argument("--create", action="store_true", help="add the tab if the Doc has none by this name")
    p.add_argument("--clear", action="store_true", help="empty this tab first; only this tab is touched")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--preview", default="", help="write the tab text to this file and stop")
    a = p.parse_args(argv)

    date, text = build()
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
        if not a.create:
            raise SystemExit("no tab %r in this Doc; tabs present: %s; pass --create" % (a.tab, names))
        doc.batch([{"addDocumentTab": {"tabProperties": {"title": a.tab}}}])
        doc.refresh()
        names = [t[0].strip() for t in doc.tabs()]
        print("  created tab %r" % a.tab)
    tab_n = names.index(a.tab)
    tab_id, content = doc.tab(tab_n)
    if a.clear and content[-1]["endIndex"] > 2:
        doc.delete_range(tab_id, 1, content[-1]["endIndex"] - 1)
        tab_id, content = doc.tab(tab_n)
    if content[-1]["endIndex"] > 2:
        raise SystemExit("tab %r is not empty; run with --clear to rewrite it" % a.tab)
    doc.batch([{"updateDocumentStyle": {"tabId": tab_id,
                                        "documentStyle": {"flipPageOrientation": True},
                                        "fields": "flipPageOrientation"}}])
    doc.insert_markdown(tab_n, doc.content(tab_n)[-1]["endIndex"] - 1, text)
    print("  wrote the forms (%d API calls)" % doc.calls)
    lay_out(doc, tab_n, date)
    print("done, %d API calls" % doc.calls)
    return 0


if __name__ == "__main__":
    sys.exit(main())
