#!/usr/bin/env python3
"""Write the assumption log into its own tab of the Doc.

The content is derived from docs/forms/1-2-assumption-log.en.md; nothing is authored here. What the Doc
needs and the repo file does not:

  - the scope package and the stakeholder forms are named by their sections of the Doc;
  - the italic reading convention becomes a headed paragraph, as in the other tabs;
  - the tab is landscape, as the book prints form 1.2, and the log is laid out as printed: the dark title
    bar and the Project Title and Date Prepared line over the table, the grid in the small face, the
    header repeated on a page the table runs onto, and "Page 1 of 1" under it;
  - headings are in Arial, and the tab ends on its last line rather than on an empty paragraph.

Run with:
    python3 tools/gdoc_assumption_tab.py --doc DOC_ID --dry-run
    python3 tools/gdoc_assumption_tab.py --doc DOC_ID --preview FILE   # write the tab text and stop
    python3 tools/gdoc_assumption_tab.py --doc DOC_ID --create         # add the tab, then write it
    python3 tools/gdoc_assumption_tab.py --doc DOC_ID --clear          # rewrite a tab written before
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
from gdoc_stakeholder_tab import FORMS, PAGE, FOOTER, PROJECT, body_of, date_of, notes_of, read, with_footer

LOG = FORMS / "1-2-assumption-log.en.md"
DEFAULT_DIR = os.path.expanduser("~/.config/qldapm")
TAB = "10: Assumption Log"
# Points across the 648pt of a landscape page: ID, Category, Assumption/Constraint, Responsible Party,
# Due Date, Actions, Status, Comments.
WIDTHS = [24, 62, 190, 62, 58, 130, 36, 86]
# The title bar, the Project Title line and the column header repeat on a page the log runs onto.
PINNED = 3

REWRITES = [
    ("Assumption 20 holds the stakeholder readings of forms 1.3 and 1.4,",
     "Assumption 20 holds the stakeholder readings of forms 1.3 and 1.4 of section 9,"),
    ("The highlighted readings of the scope package and of forms 2.23, 2.28, and 2.32",
     "The highlighted readings of the scope baseline of section 3 and of forms 2.23, 2.28, and 2.32"),
]


def build() -> tuple[str, str]:
    """(date prepared, tab text)."""
    md = read(LOG, REWRITES)
    body = with_footer(body_of(md), "| ID | Category |")
    text = "## %s\n\n#### Reading convention\n\n%s\n\n%s" % (TAB, notes_of(md), body)
    text = re.sub(r"\n{3,}", "\n\n", text)
    if "`" in text or "<br" in text or "<ins>" in text or ".md" in text or "scope package" in text:
        raise SystemExit("a repo reference, an ins tag, or a <br> is left in the tab text")
    return date_of(md), text


def lay_out(doc, tab_n, date):
    tables = ge.top_tables(doc.content(tab_n))
    if len(tables) != 1:
        raise SystemExit("expected 1 table in the tab, found %d" % len(tables))
    start = tables[0]["startIndex"]
    tab_id, table_el = layout._table(doc, tab_n, start)
    doc.batch(gdoc_form.column_widths(tab_id, table_el, WIDTHS))
    layout.small_text(doc, tab_n, start, 1, layout.SMALL)
    layout.full_row(doc, tab_n, start, 0, "**Project Title:** %s          **Date Prepared:** %s" % (PROJECT, date))
    layout.full_row(doc, tab_n, start, 0, "**ASSUMPTION LOG**", background=gdoc_form.DARK, center=True)
    layout.whiten_title(doc, tab_n, start)
    layout.keep_rows(doc, tab_n, start, PINNED)
    layout.footer_line(doc, tab_n, FOOTER)
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
    print("  wrote the form (%d API calls)" % doc.calls)
    lay_out(doc, tab_n, date)
    print("done, %d API calls" % doc.calls)
    return 0


if __name__ == "__main__":
    sys.exit(main())
