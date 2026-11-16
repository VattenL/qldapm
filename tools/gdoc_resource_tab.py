#!/usr/bin/env python3
"""Write the team charter, resource requirements and resource breakdown structure into one tab of the Doc.

The content is derived from docs/forms/2-27-team-charter.en.md, 2-28-resource-requirements.en.md and
2-29-resource-breakdown-structure.en.md; nothing is authored here. What the Doc needs and the repo
files do not:

  - references to the scope package and to the scope change request become references to the Doc's
    sections 3 and 5.7;
  - each italic reading convention becomes a headed paragraph, as in the other tabs;
  - each printed page is laid out as the book prints it: the dark title bar, the Project Title and
    Date Prepared line on page 1 only, labelled boxes without the Field | Content header, and "Page N
    of M" under the page; form 2.29 is the framed outline box that tab 3 uses for form 2.9;
  - the tables are set in the 10pt face of the cost tab's prose tables, and the 21 row requirements
    register in its 8pt grid face; a table that runs over a page repeats its heading and column header;
  - headings are in Arial, and the tab ends on its last line rather than on an empty paragraph;
  - forms 2.28 and 2.29 start on a new page, and so does page 2 of form 2.27.

Run with:
    python3 tools/gdoc_resource_tab.py --doc DOC_ID --dry-run
    python3 tools/gdoc_resource_tab.py --doc DOC_ID --preview FILE   # write the tab text and stop
    python3 tools/gdoc_resource_tab.py --doc DOC_ID --create         # add the tab, then write it
    python3 tools/gdoc_resource_tab.py --doc DOC_ID --clear          # rewrite a tab written before
    python3 tools/gdoc_resource_tab.py --doc DOC_ID --tidy           # only the outline pass of form 2.29
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
CHARTER = FORMS / "2-27-team-charter.en.md"
REQUIREMENTS = FORMS / "2-28-resource-requirements.en.md"
STRUCTURE = FORMS / "2-29-resource-breakdown-structure.en.md"
DEFAULT_DIR = os.path.expanduser("~/.config/qldapm")
TAB = "7: Resource Plan"
H_CHARTER = "7.1 Team Charter"
H_REQUIREMENTS = "7.2 Resource Requirements"
H_STRUCTURE = "7.3 Resource Breakdown Structure"
PROJECT = "Development and Deployment of a Learning Center Management Software"
PAGE = "@@PAGE {}@@"
# Points, for a portrait page with the Doc's one-inch margins, about 468pt of usable width; one entry
# per table of the forms, in printed order: 2.27 page 1, 2.27 page 2, the 2.27 signature block, 2.28.
WIDTHS = [[130, 338], [130, 338], [234, 234], [58, 100, 76, 117, 117]]
# Rows each table repeats on a page it runs onto: the heading rows and the column header.
PINNED = [0, 0, 1, 3]
SIGNATURE_ROW_PT = 26
# The outline of form 2.29 is set in the small face, so that its 40 lines and the page number stay on
# one page under the reading convention, as the book prints the form.
OUTLINE_PT = 8
OUTLINE_SPACE_PT = 0
PAGE_LINE_SPACE_PT = 6

REWRITES = [
    ("the scope package as committed on 14 October 2026",
     "the scope baseline of section 3 as committed on 14 October 2026"),
]
REQUIREMENTS_REWRITES = [
    ("the scope change request that carries it", "the scope change request of section 5.7 that carries it"),
]
HEADER = "| Field | Content |\n| --- | --- |\n"
TITLE_LINES = re.compile(r"^\*\*(Project Title|Date Prepared):\*\* .*\n", re.M)
NOTE = re.compile(r"^\*([^*].*)\*$", re.M)
LIST_ITEM = re.compile(r"^( *)(\d+)\. (.*)$")


def read(path: pathlib.Path, rewrites) -> str:
    md = path.read_text(encoding="utf-8")
    for old, new in list(REWRITES) + list(rewrites):
        if old not in md:
            if (old, new) in REWRITES:
                continue
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
    """The form without its title, its reading convention and its title block."""
    md = re.sub(r"^# .*\n", "", md, count=1, flags=re.M)
    md = NOTE.sub("", md)
    md = TITLE_LINES.sub("", md)
    return md.strip("\n") + "\n"


def outline_of(md: str) -> list[str]:
    """The nested list of form 2.29 as the lines of the framed outline: the printed code with its
    closing dot at every level, indented two spaces a level."""
    counters, lines = [], []
    for raw in body_of(md).splitlines():
        m = LIST_ITEM.match(raw)
        if not m:
            continue
        depth = len(m.group(1)) // 3
        counters = counters[:depth]
        counters += [0] * (depth + 1 - len(counters))
        counters[depth] = int(m.group(2))
        code = ".".join(str(n) for n in counters)
        lines.append("%s%s.  %s" % ("  " * depth, code, m.group(3).strip()))
    if not lines:
        raise SystemExit("no outline found in form 2.29")
    return lines


def build() -> tuple[str, str]:
    """(date prepared, tab text)."""
    charter = read(CHARTER, [])
    requirements = read(REQUIREMENTS, REQUIREMENTS_REWRITES)
    structure = read(STRUCTURE, [])
    dates = {date_of(m) for m in (charter, requirements, structure)}
    if len(dates) != 1:
        raise SystemExit("the three forms carry different Date Prepared values: %s" % sorted(dates))
    date = dates.pop()

    page_one = body_of(charter).replace(HEADER, "")
    page_one = page_one.replace("#### TEAM CHARTER, page 1 of 2\n", "")
    page_one = page_one.replace("#### TEAM CHARTER, page 2 of 2\n", PAGE.format("Page 1 of 2") + "\n")
    page_one = page_one.rstrip() + "\n\n" + PAGE.format("Page 2 of 2") + "\n"

    register = body_of(requirements).rstrip() + "\n\n" + PAGE.format("Page 1 of 1") + "\n"

    fields = "**Project Title:** %s      **Date\u00a0Prepared:** %s" % (PROJECT, date)
    box = "\n".join(["```form", "!title RESOURCE BREAKDOWN STRUCTURE", "!fields " + fields]
                    + outline_of(structure) + ["!page Page 1 of 1", "```"])

    def part(heading, md, form):
        return "### %s\n\n#### Reading convention\n\n%s\n\n%s\n" % (heading, notes_of(md), form)

    text = "## %s\n\n%s\n%s\n%s" % (
        TAB, part(H_CHARTER, charter, page_one), part(H_REQUIREMENTS, requirements, register),
        part(H_STRUCTURE, structure, box))
    if "`" in text.replace("```form", "").replace("```", "") or "<br" in text \
            or "scope package" in text or ".md" in text:
        raise SystemExit("a repo reference or a <br> is left in the tab text")
    return date, text


def tidy_box(doc, tab_n):
    """The framed outline of form 2.29 in the small face with tight lines, and its Project Title
    line with spaces and a whole 'Date Prepared' where an earlier write left a tab. Safe to run again."""
    tab_id, content = doc.tab(tab_n)
    table_el = ge.top_tables(content)[-1]
    cell = ge.table_cells(table_el)[0][0]
    paras = [el for el in cell["content"] if "paragraph" in el]
    reqs = []
    last = paras[-1]
    reqs.append({"updateParagraphStyle": {
        "range": {"startIndex": last["startIndex"], "endIndex": last["endIndex"], "tabId": tab_id},
        "paragraphStyle": {"spaceAbove": {"magnitude": PAGE_LINE_SPACE_PT, "unit": "PT"}},
        "fields": "spaceAbove"}})
    for el in paras[1:-1]:
        text = ge.para_text(el)
        rng = {"startIndex": el["startIndex"], "endIndex": el["endIndex"], "tabId": tab_id}
        if text.startswith("Project Title:"):
            continue
        reqs.append({"updateTextStyle": {
            "range": {"startIndex": el["startIndex"], "endIndex": el["endIndex"] - 1, "tabId": tab_id},
            "textStyle": {"fontSize": {"magnitude": OUTLINE_PT, "unit": "PT"}}, "fields": "fontSize"}})
        reqs.append({"updateParagraphStyle": {
            "range": rng, "paragraphStyle": {"spaceAbove": {"magnitude": OUTLINE_SPACE_PT, "unit": "PT"}},
            "fields": "spaceAbove"}})
    doc.batch(reqs)
    tab_id, content = doc.tab(tab_n)
    cell = ge.table_cells(ge.top_tables(content)[-1])[0][0]
    line = next(el for el in cell["content"] if "paragraph" in el and ge.para_text(el).startswith("Project Title:"))
    text, start = ge.para_text(line), line["startIndex"]
    fixes = []
    at = text.find("\t")
    if at >= 0:
        fixes.append((start + at, 1, "      "))
    at = text.find("Date Prepared:")
    if at >= 0:
        fixes.append((start + at + 4, 1, "\u00a0"))
    for index, length, new_text in sorted(fixes, reverse=True):
        doc.batch([{"deleteContentRange": {"range": {"startIndex": index, "endIndex": index + length,
                                                     "tabId": tab_id}}},
                   {"insertText": {"location": {"index": index, "tabId": tab_id}, "text": new_text}}])


def lay_out(doc, tab_n, date):
    """Title bars, widths, footers and page breaks, from the last table up so that the start index
    of every table above stays valid. The framed outline of form 2.29 is the last table and is
    styled as it is written."""
    def starts():
        return [el["startIndex"] for el in ge.top_tables(doc.content(tab_n))]

    if len(starts()) != len(WIDTHS) + 1:
        raise SystemExit("expected %d tables in the tab, found %d" % (len(WIDTHS) + 1, len(starts())))
    project = ("**Project Title:** %s          **Date Prepared:** %s" % (PROJECT, date))
    bars = {0: "TEAM CHARTER", 1: "TEAM CHARTER", 3: "RESOURCE REQUIREMENTS"}
    for k in range(len(WIDTHS) - 1, -1, -1):
        start = starts()[k]
        tab_id, table_el = layout._table(doc, tab_n, start)
        doc.batch(gdoc_form.column_widths(tab_id, table_el, WIDTHS[k]))
        if k == 3:
            layout.small_text(doc, tab_n, start, 1, layout.SMALL)
        else:
            doc.batch([layout.font_size(tab_id, table_el, layout.TEXT)])
        if k == 2:
            tab_id, table_el = layout._table(doc, tab_n, start)
            rows = list(range(1, len(ge.table_cells(table_el))))
            doc.batch([{"updateTableRowStyle": {
                "tableStartLocation": {"index": table_el["startIndex"], "tabId": tab_id},
                "rowIndices": rows,
                "tableRowStyle": {"minRowHeight": {"magnitude": SIGNATURE_ROW_PT, "unit": "PT"}},
                "fields": "minRowHeight"}}])
        if k in (0, 3):
            layout.full_row(doc, tab_n, start, 0, project)
        if k in bars:
            layout.full_row(doc, tab_n, start, 0, "**%s**" % bars[k], background=gdoc_form.DARK, center=True)
            layout.whiten_title(doc, tab_n, start)
        layout.keep_rows(doc, tab_n, start, PINNED[k])
    for footer in ("Page 1 of 2", "Page 2 of 2", "Page 1 of 1"):
        layout.footer_line(doc, tab_n, footer)
    tab_id, content = doc.tab(tab_n)
    el = ge.find_para(content, lambda t: t.strip() == "Page 1 of 2")
    doc.batch([{"insertPageBreak": {"location": {"index": el["endIndex"] - 1, "tabId": tab_id}}}])
    tab_id, content = doc.tab(tab_n)
    reqs = []
    for heading in (H_REQUIREMENTS, H_STRUCTURE):
        el = ge.find_para(content, lambda t, h=heading: t.strip() == h)
        reqs.append({"updateParagraphStyle": {
            "range": {"startIndex": el["startIndex"], "endIndex": el["endIndex"], "tabId": tab_id},
            "paragraphStyle": {"pageBreakBefore": True}, "fields": "pageBreakBefore"}})
    doc.batch(reqs)
    tidy_box(doc, tab_n)
    layout.finish(doc, tab_n)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--doc", required=True)
    p.add_argument("--tab", default=TAB)
    p.add_argument("--token", default=os.path.join(DEFAULT_DIR, "token.json"))
    p.add_argument("--create", action="store_true", help="add the tab if the Doc has none by this name")
    p.add_argument("--clear", action="store_true", help="empty this tab first; only this tab is touched")
    p.add_argument("--tidy", action="store_true", help="only run the outline pass on the tab already written")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--preview", default="", help="write the tab text to this file and stop")
    a = p.parse_args(argv)

    date, text = build()
    blocks = ge.parse_blocks(text)
    tables = sum(1 for b in blocks if b["type"] in ("table", "box"))
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
    if a.tidy:
        tidy_box(doc, tab_n)
        print("done, %d API calls" % doc.calls)
        return 0
    tab_id, content = doc.tab(tab_n)
    if a.clear and content[-1]["endIndex"] > 2:
        doc.delete_range(tab_id, 1, content[-1]["endIndex"] - 1)
        tab_id, content = doc.tab(tab_n)
    if content[-1]["endIndex"] > 2:
        raise SystemExit("tab %r is not empty; run with --clear to rewrite it" % a.tab)
    doc.insert_markdown(tab_n, doc.content(tab_n)[-1]["endIndex"] - 1, text)
    print("  wrote the forms (%d API calls)" % doc.calls)
    lay_out(doc, tab_n, date)
    print("done, %d API calls" % doc.calls)
    return 0


if __name__ == "__main__":
    sys.exit(main())
