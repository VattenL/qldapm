#!/usr/bin/env python3
"""Write the risk register into its own tab of the Doc.

The content is derived from docs/forms/2-32-risk-register.en.md; nothing is authored here. What the
Doc needs and the repo file does not:

  - the reference to the scope package becomes a reference to the Doc's section 3.2.4, and the scope
    change request is named by its section 5.7;
  - the italic reading convention becomes a headed paragraph, as in the other tabs;
  - the tab is landscape, as the book prints form 2.32, and the two banks are laid out as printed: the
    dark title bar and the Project Title and Date Prepared line over the first bank, the grids in the
    small face, each bank repeating its header on a page it runs onto, and "Page 1 of 1" under it;
  - headings are in Arial, and the tab ends on its last line rather than on an empty paragraph.

Run with:
    python3 tools/gdoc_risk_tab.py --doc DOC_ID --dry-run
    python3 tools/gdoc_risk_tab.py --doc DOC_ID --preview FILE   # write the tab text and stop
    python3 tools/gdoc_risk_tab.py --doc DOC_ID --create         # add the tab, then write it
    python3 tools/gdoc_risk_tab.py --doc DOC_ID --clear          # rewrite a tab written before
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
REGISTER = ROOT / "docs" / "forms" / "2-32-risk-register.en.md"
DEFAULT_DIR = os.path.expanduser("~/.config/qldapm")
TAB = "8: Risk Register"
PROJECT = "Development and Deployment of a Learning Center Management Software"
PAGE = "@@PAGE {}@@"
FOOTER = "Page 1 of 1"
# Points across the 648pt of a landscape page, one list per bank in printed order.
WIDTHS = [[30, 150, 50, 46, 44, 44, 48, 40, 60, 136],
          [46, 40, 44, 48, 40, 46, 54, 150, 36, 144]]
# Rows each bank repeats on a page it runs onto: the title bar, the Project Title line and the column
# header over the first bank, the column header over the second.
PINNED = [3, 1]
FACE = 7

REWRITES = [
    ("the coverage check in Part 2 of `docs/scope-package.en.md`", "the coverage check in section 3.2.4"),
    ("the scope change request of 8 October 2026 raises", "the scope change request of 8 October 2026, section 5.7, raises"),
]
TITLE_LINES = re.compile(r"^\*\*(Project Title|Date Prepared):\*\* .*\n", re.M)
NOTE = re.compile(r"^\*([^*].*)\*$", re.M)


def read() -> str:
    md = REGISTER.read_text(encoding="utf-8")
    for old, new in REWRITES:
        if old not in md:
            raise SystemExit("expected text not found in %s, the source has changed: %r" % (REGISTER.name, old[:60]))
        md = md.replace(old, new)
    return md


def build() -> tuple[str, str]:
    """(date prepared, tab text)."""
    md = read()
    date = re.search(r"^\*\*Date Prepared:\*\* (.+)$", md, re.M).group(1).strip()
    notes = "\n\n".join(NOTE.findall(md))
    if not notes:
        raise SystemExit("no reading convention found")
    body = re.sub(r"^# .*\n", "", md, count=1, flags=re.M)
    body = TITLE_LINES.sub("", NOTE.sub("", body)).strip("\n")
    text = "## %s\n\n#### Reading convention\n\n%s\n\n%s\n\n%s\n" % (TAB, notes, body, PAGE.format(FOOTER))
    if "`" in text or "<br" in text or "scope package" in text or ".md" in text:
        raise SystemExit("a repo reference or a <br> is left in the tab text")
    return date, text


def lay_out(doc, tab_n, date):
    """Widths, face and pinned rows from the second bank up, so that the start index of the first
    stays valid; then the title bar and Project Title line over the first bank, and the footer."""
    def starts():
        return [el["startIndex"] for el in ge.top_tables(doc.content(tab_n))]

    if len(starts()) != len(WIDTHS):
        raise SystemExit("expected %d tables in the tab, found %d" % (len(WIDTHS), len(starts())))
    project = "**Project Title:** %s          **Date Prepared:** %s" % (PROJECT, date)
    for k in range(len(WIDTHS) - 1, -1, -1):
        start = starts()[k]
        tab_id, table_el = layout._table(doc, tab_n, start)
        doc.batch(gdoc_form.column_widths(tab_id, table_el, WIDTHS[k]))
        layout.small_text(doc, tab_n, start, 1, FACE)
        if k == 0:
            layout.full_row(doc, tab_n, start, 0, project)
            layout.full_row(doc, tab_n, start, 0, "**RISK REGISTER**", background=gdoc_form.DARK, center=True)
            layout.whiten_title(doc, tab_n, start)
        layout.keep_rows(doc, tab_n, start, PINNED[k])
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
