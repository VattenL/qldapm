#!/usr/bin/env python3
"""Write the quality management plan, form 2.23, into its own tab of the Doc.

The content is derived from docs/forms/2-23-quality-management-plan.en.md; nothing is authored here.
What the Doc needs and the repo file does not:

  - references to the scope package and to the scope change request become references to the Doc's
    sections 3 and 5.7;
  - the italic reading convention becomes a headed paragraph, as in the other tabs;
  - each printed page is laid out as the book prints it: the dark title bar, the Project Title and
    Date Prepared line on page 1 only, each printed heading as a grey row over its box, labelled
    boxes without the Field | Content header, and "Page N of 2" under the page;
  - page 2 starts on a new page.

Run with:
    python3 tools/gdoc_quality_tab.py --doc DOC_ID --dry-run
    python3 tools/gdoc_quality_tab.py --doc DOC_ID --create     # add the tab, then write it
    python3 tools/gdoc_quality_tab.py --doc DOC_ID --clear      # rewrite a tab written before
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
SOURCE = ROOT / "docs" / "forms" / "2-23-quality-management-plan.en.md"
DEFAULT_DIR = os.path.expanduser("~/.config/qldapm")
TAB = "6: Quality Management Plan"
TITLE = "QUALITY MANAGEMENT PLAN"
PROJECT = "Development and Deployment of a Learning Center Management Software"
PAGE = "@@PAGE {}@@"
# Printed headings that sit over a box of their own, in printed order.
CAPTIONS = ["Quality Objectives", "Quality Roles and Responsibilities",
            "Deliverables and Processes Subject to Quality Review"]
# Points, for a portrait page with the Doc's one-inch margins, about 468pt of usable width; one entry
# per table of the form, in printed order.
WIDTHS = [[130, 338], [150, 318], [150, 318], [234, 234], [130, 338]]

REWRITES = [
    ("the charter and the scope package as committed on 30 September 2026",
     "the charter and the scope baseline of section 3 as committed on 30 September 2026"),
    ("the scope change request of 8 October 2026, which has no disposition yet",
     "the scope change request of section 5.7, which has no disposition yet"),
    ("names the work package of the scope package that does the work",
     "names the work package of section 3 that does the work"),
    ("no work package of the scope package funds it", "no work package of section 3 funds it"),
]


def build() -> tuple[str, str]:
    """(date prepared, tab text)."""
    md = SOURCE.read_text(encoding="utf-8")
    for old, new in REWRITES:
        if old not in md:
            raise SystemExit("expected text not found, the source has changed: %r" % old[:60])
        md = md.replace(old, new)
    date = re.search(r"^\*\*Date Prepared:\*\* (.+)$", md, re.M).group(1).strip()

    m = re.search(r"^\*(Form 2\.23, .*?)\*$", md, re.M | re.S)
    note = m.group(1)
    body = md[m.end():]
    body = re.sub(r"^\*\*Project Title:\*\* .*\n\*\*Date Prepared:\*\* .*\n", "", body, flags=re.M)
    body = body.replace("| Field | Content |\n| --- | --- |\n", "")
    for caption in CAPTIONS:
        if body.count("**%s**\n\n" % caption) != 1:
            raise SystemExit("expected the printed heading %r once" % caption)
        body = body.replace("**%s**\n\n" % caption, "")
    body = body.replace("#### QUALITY MANAGEMENT PLAN, page 1 of 2\n", "### 6.1 Quality Management Plan\n")
    body = body.replace("#### QUALITY MANAGEMENT PLAN, page 2 of 2\n",
                        PAGE.format("Page 1 of 2") + "\n")
    body = body.rstrip() + "\n\n" + PAGE.format("Page 2 of 2") + "\n"

    text = "## %s\n\n#### Reading convention\n\n%s\n%s" % (TAB, note, body)
    if "`" in text or "<br" in text:
        raise SystemExit("a repo reference or a <br> is left in the tab text")
    return date, text


def lay_out(doc, tab_n, date):
    """Captions, title bars, widths, footers, and the page break, from the last table up so that the
    start index of every table above stays valid."""
    def starts():
        return [el["startIndex"] for el in ge.top_tables(doc.content(tab_n))]

    if len(starts()) != len(WIDTHS):
        raise SystemExit("expected %d tables in the tab, found %d" % (len(WIDTHS), len(starts())))
    for k in range(len(WIDTHS) - 1, -1, -1):
        start = starts()[k]
        tab_id, table_el = layout._table(doc, tab_n, start)
        doc.batch(gdoc_form.column_widths(tab_id, table_el, WIDTHS[k]))
        if 1 <= k <= 3:
            layout.full_row(doc, tab_n, start, 0, "**%s**" % CAPTIONS[k - 1], background=gdoc_form.GREY)
        if k == 0:
            layout.full_row(doc, tab_n, start, 0,
                            "**Project Title:** %s          **Date Prepared:** %s" % (PROJECT, date))
        if k in (0, 3):
            layout.full_row(doc, tab_n, start, 0, "**%s**" % TITLE, background=gdoc_form.DARK, center=True)
            layout.whiten_title(doc, tab_n, start)
    for footer in ("Page 1 of 2", "Page 2 of 2"):
        layout.footer_line(doc, tab_n, footer)
    tab_id, content = doc.tab(tab_n)
    el = ge.find_para(content, lambda t: t.strip() == "Page 1 of 2")
    doc.batch([{"insertPageBreak": {"location": {"index": el["endIndex"] - 1, "tabId": tab_id}}}])


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
    doc.insert_markdown(tab_n, doc.content(tab_n)[-1]["endIndex"] - 1, text)
    print("  wrote the form (%d API calls)" % doc.calls)
    lay_out(doc, tab_n, date)
    print("done, %d API calls" % doc.calls)
    return 0


if __name__ == "__main__":
    sys.exit(main())
