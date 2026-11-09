#!/usr/bin/env python3
"""Write the risk register into its own tab of the Doc.

The content is derived from docs/forms/2-32-risk-register.en.md; nothing is authored here. What the
Doc needs and the repo file does not:

  - the scope change request is named by its section 5.7;
  - the italic reading convention becomes a headed paragraph, as in the other tabs, and the revision
    history and the probability and impact scales follow it under their own headings;
  - the tab is landscape, as the book prints form 2.32, and the two banks are laid out as printed: the
    dark title bar and the Project Title and Date Prepared line over the first bank, the Impact label
    spanning its four columns over a second header row, the other labels spanning both header rows,
    the grids in the small face, each bank repeating its header on a page it runs onto, and
    "Page 1 of 1" under it;
  - a cell the source wraps in <ins> changed in the current version and is shaded green; the tag
    itself never reaches the Doc;
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
# Points across the 648pt of a landscape page, one list per table in the order the tab prints them:
# revision history, scales, matrix, then the two banks of the form.
WIDTHS = [[50, 80, 380, 138],
          [50, 70, 132, 132, 132, 132],
          [160, 120, 120, 120],
          [24, 130, 44, 42, 58, 58, 58, 58, 46, 130],
          [24, 42, 50, 50, 50, 50, 46, 56, 160, 30, 90]]
BANKS = 2
# First column of the four Impact columns in each bank; every other column's label spans both header rows.
IMPACT = [4, 2]
# Rows each bank repeats on a page it runs onto: the title bar, the Project Title line and the two
# header rows over the first bank, the two header rows over the second.
PINNED = [4, 2]
FACE = 7
GREEN = {"color": {"rgbColor": {"red": 0.85, "green": 0.94, "blue": 0.83}}}
INS = re.compile(r"</?ins>")
GROUP = "Impact: "

REWRITES = [
    ("the scope change request of 8 October 2026 raises", "the scope change request of 8 October 2026, section 5.7, raises"),
    ("Cells changed in version 1.1 are wrapped in an ins tag.", "Cells changed in version 1.1 are shaded green."),
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


def two_tier(md):
    """The source writes each spanned column as "Impact: Scope" in one header row, the repo's rule for a
    grouped header. The Doc prints the form's two rows: Impact over the four columns, their labels
    under it, and every other label alone in the first row, to be merged down both rows."""
    out = []
    for line in md.splitlines():
        if line.startswith("| ID |") and GROUP in line:
            cells = ge._split_row(line)
            top = ["Impact" if c.startswith(GROUP) and not cells[k - 1].startswith(GROUP) else
                   ("" if c.startswith(GROUP) else c) for k, c in enumerate(cells)]
            under = ["**%s**" % c[len(GROUP):] if c.startswith(GROUP) else "" for c in cells]
            out.append("| " + " | ".join(top) + " |")
            out.append("| " + " | ".join(["---"] * len(cells)) + " |")
            out.append("| " + " | ".join(under) + " |")
            continue
        if out and out[-1].startswith("| ---") and line.startswith("| ---"):
            continue
        out.append(line)
    return "\n".join(out) + "\n"


def changed_cells(text):
    """(row, column) of every cell wrapped in <ins>, one list per bank, counted as the Doc table counts
    them: the header row is row 0."""
    tables = [b for b in ge.parse_blocks(text) if b["type"] == "table"][-BANKS:]
    return [[(r, c) for r, row in enumerate(t["rows"]) for c, cell in enumerate(row)
             if cell.strip().startswith("<ins>")] for t in tables]


def build() -> tuple[str, str, list]:
    """(date prepared, tab text, changed cells of each bank)."""
    md = read()
    date = re.search(r"^\*\*Date Prepared:\*\* (.+)$", md, re.M).group(1).strip()
    notes = "\n\n".join(NOTE.findall(md))
    if not notes:
        raise SystemExit("no reading convention found")
    body = re.sub(r"^# .*\n", "", md, count=1, flags=re.M)
    body = TITLE_LINES.sub("", NOTE.sub("", body)).strip("\n")
    body = two_tier(re.sub(r"^## ", "#### ", body, flags=re.M))
    text = "## %s\n\n#### Reading convention\n\n%s\n\n%s\n\n%s\n" % (TAB, notes, body, PAGE.format(FOOTER))
    changed = changed_cells(text)
    text = INS.sub("", text)
    if "`" in text or "<br" in text or "scope package" in text or ".md" in text:
        raise SystemExit("a repo reference or a <br> is left in the tab text")
    return date, text, changed


def header(doc, tab_n, start, impact):
    """The printed two-tier header: Impact across its four columns, every other label down both rows.
    The second row is empty under a label that spans it, so the merge leaves an empty paragraph in the
    head cell, which is removed afterwards."""
    tab_id, table_el = layout._table(doc, tab_n, start)
    ncols = len(ge.table_cells(table_el)[0])
    reqs = [gdoc_form.merge(tab_id, table_el, 0, impact, 1, 4)]
    reqs += [gdoc_form.merge(tab_id, table_el, 0, c, 2, 1)
             for c in range(ncols) if not impact <= c < impact + 4]
    doc.batch(reqs)
    tab_id, table_el = layout._table(doc, tab_n, start)
    reqs = []
    for cell in ge.table_cells(table_el)[0]:
        paras = cell["content"]
        while len(paras) > 1 and not ge.para_text(paras[-1]).strip():
            reqs.append({"deleteContentRange": {"range": {"startIndex": paras[-2]["endIndex"] - 1,
                                                          "endIndex": paras[-1]["endIndex"] - 1,
                                                          "tabId": tab_id}}})
            paras = paras[:-1]
    reqs.sort(key=lambda r: -r["deleteContentRange"]["range"]["startIndex"])
    reqs.append(gdoc_form.style(tab_id, table_el, 0, 0, 2, ncols))
    doc.batch(reqs)
    tab_id, table_el = layout._table(doc, tab_n, start)
    s, e = ge.cell_range(ge.table_cells(table_el)[0][0])
    s2, e2 = ge.cell_range(ge.table_cells(table_el)[1][-1])
    doc.batch([{"updateParagraphStyle": {"range": {"startIndex": s, "endIndex": e2, "tabId": tab_id},
                                         "paragraphStyle": {"alignment": "CENTER"}, "fields": "alignment"}}])


def shade(doc, tab_n, start, cells):
    tab_id, table_el = layout._table(doc, tab_n, start)
    reqs = [gdoc_form.style(tab_id, table_el, r, c, background=GREEN, align=None) for r, c in cells]
    if reqs:
        doc.batch(reqs)


def lay_out(doc, tab_n, date, changed):
    """Each table from the last up, so that the start index of the ones above stays valid: widths and
    face, then for the banks the two-tier header and the green cells, which use the source's row
    numbers, and only then the title bar and Project Title line over the first bank; last the footer."""
    def starts():
        return [el["startIndex"] for el in ge.top_tables(doc.content(tab_n))]

    if len(starts()) != len(WIDTHS):
        raise SystemExit("expected %d tables in the tab, found %d" % (len(WIDTHS), len(starts())))
    project = "**Project Title:** %s          **Date Prepared:** %s" % (PROJECT, date)
    first_bank = len(WIDTHS) - BANKS
    for k in range(len(WIDTHS) - 1, -1, -1):
        start = starts()[k]
        tab_id, table_el = layout._table(doc, tab_n, start)
        doc.batch(gdoc_form.column_widths(tab_id, table_el, WIDTHS[k]))
        if k < first_bank:
            layout.small_text(doc, tab_n, start, 1, FACE)
            layout.keep_rows(doc, tab_n, start, 1)
            continue
        b = k - first_bank
        layout.small_text(doc, tab_n, start, 2, FACE)
        header(doc, tab_n, start, IMPACT[b])
        shade(doc, tab_n, start, changed[b])
        if b == 0:
            layout.full_row(doc, tab_n, start, 0, project)
            layout.full_row(doc, tab_n, start, 0, "**RISK REGISTER**", background=gdoc_form.DARK, center=True)
            layout.whiten_title(doc, tab_n, start)
        layout.keep_rows(doc, tab_n, start, PINNED[b])
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

    date, text, changed = build()
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
    lay_out(doc, tab_n, date, changed)
    print("done, %d API calls" % doc.calls)
    return 0


if __name__ == "__main__":
    sys.exit(main())
