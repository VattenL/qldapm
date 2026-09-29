#!/usr/bin/env python3
"""Bring the scope tab of the team's Google Doc up to its source, in place.

The tab carries reviewers' comment threads, all anchored on headings and header cells, so it is
never cleared. Three steps, each safe to repeat:

  dictionary  Rebuild each WBS dictionary sheet under its existing heading in the layout form 2.10
              prints: the WBS DICTIONARY title bar, Work Package Name beside Code of Accounts,
              Description of Work beside Assumptions and Constraints, Milestones beside Due Dates,
              the two-tier Labor and Material header, the four full-width boxes below, and
              "Page 1 of 1". Responsible Person, which the book lists on page 52 but does not print,
              takes a row of its own under the printed boxes. A sheet already in this layout is
              skipped. Each sheet starts a new page.
  rtm         Rewrite the cells of the inter-requirements matrix that differ from the source.
  text        Replace the prose whose wording changed in the source, and only the changed words, so
              the formatting around them is kept.

Content comes from docs/scope-package.en.md through tools/scope_tab3.py, the same payload the tab
was written from; nothing is authored here.

Run with:
    python3 tools/gdoc_scope_sync.py --doc DOC_ID --tab "3: Scope Baseline" --step dictionary --limit 2
    python3 tools/gdoc_scope_sync.py --doc DOC_ID --tab "3: Scope Baseline" --step all
"""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc_edit as ge
import gdoc_form
import scope_tab3

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_DIR = os.path.expanduser("~/.config/qldapm")
SHEET_HEADING = re.compile(r"^##### (1(?:\.\d+){3} .+)$", re.M)
# Points, for the Doc's 648pt of usable width on a landscape Letter page.
TOP_WIDTHS = [324, 324]
ACTIVITY_WIDTHS = [72, 104, 62, 42, 50, 68, 38, 62, 72, 78]
PAIRS = [("Project Title", "Date Prepared"), ("Work Package Name", "Code of Accounts"),
         ("Description of Work", "Assumptions and Constraints"), ("Milestones", "Due Dates")]
BOTTOM = ["Quality Requirements", "Acceptance Criteria", "Technical Information",
          "Agreement Information"]
TITLE = "WBS DICTIONARY"
PAGE_FOOTER = "Page 1 of 1"


# ------------------------------------------------------------------ payload

def payload(md_path):
    return scope_tab3.build(pathlib.Path(md_path).read_text(encoding="utf-8"))


def sheets_of(text):
    """{heading text: (fields, activity rows, bottom fields)} for every dictionary sheet."""
    starts = [(m.start(), m.group(1)) for m in SHEET_HEADING.finditer(text)]
    out = {}
    for k, (pos, heading) in enumerate(starts):
        end = starts[k + 1][0] if k + 1 < len(starts) else len(text)
        tables = [b for b in ge.parse_blocks(text[pos:end]) if b["type"] == "table"]
        top, acts, bottom = tables[0], tables[1], tables[2]
        out[heading] = (dict((r[0], r[1]) for r in top["rows"][1:]), acts["rows"][1:],
                        dict((r[0], r[1]) for r in bottom["rows"][1:]))
    return out


def boxed(label, value):
    return ("**%s:** %s" % (label, value)).strip() if value else "**%s:**" % label


def rows_md(rows):
    return "\n".join("| " + " | ".join(r) + " |" for r in rows)


def sheet_markdown(fields, acts, bottom):
    """The sheet in form 2.10's layout. No header separator: every label is bold inline."""
    top = [["**%s**" % TITLE, ""]]
    top += [[boxed(a, fields.get(a, "")), boxed(b, fields.get(b, ""))] for a, b in PAIRS]
    top.append([boxed("Responsible Person", fields.get("Responsible Person", "")), ""])
    head = [["**ID**", "**Activity**", "**Resource**", "**Labor**", "", "", "**Material**", "", "",
             "**Total Cost**"],
            ["", "", "", "**Hours**", "**Rate**", "**Total**", "**Units**", "**Cost**", "**Total**", ""]]
    low = [[boxed(k, bottom.get(k, ""))] for k in BOTTOM]
    return "\n\n".join([rows_md(top), rows_md(head + acts), rows_md(low), PAGE_FOOTER]) + "\n"


# ------------------------------------------------------------------ reading the tab

def headings(content):
    return [el for el in content if "paragraph" in el and el["paragraph"].get(
        "paragraphStyle", {}).get("namedStyleType", "").startswith("HEADING")]


def heading_el(content, text):
    for el in headings(content):
        if ge.para_text(el).strip() == text:
            return el
    return None


def tables_after(content, index, n):
    return [el for el in ge.top_tables(content) if el["startIndex"] > index][:n]


def sheet_done(content, head):
    t = tables_after(content, head["startIndex"], 1)
    return bool(t) and ge.cell_text(ge.table_cells(t[0])[0][0]).strip() == TITLE


def sheet_end(content, head):
    """Start of the heading after this sheet, or the end of the tab."""
    later = [el for el in headings(content) if el["startIndex"] > head["startIndex"]]
    return later[0]["startIndex"] if later else content[-1]["endIndex"] - 1


# ------------------------------------------------------------------ bulk writing

# A read of this Doc takes about 20 seconds whatever is asked for, so the sheets are written in
# phases, each phase one read and a few batches for every sheet at once. Sheets are edited from the
# last to the first, so an edit never moves the indexes of the sheets still to be edited.
CHUNK = 400


def send(doc, reqs):
    for k in range(0, len(reqs), CHUNK):
        doc.svc.documents().batchUpdate(documentId=doc.id,
                                        body={"requests": reqs[k:k + CHUNK]}).execute()
        doc.calls += 1


def read(doc, tab_n):
    doc.refresh()
    return doc.tab(tab_n)


def sheet_tables(fields, acts, bottom):
    """The three tables of a sheet as rows of Markdown cells."""
    lines = sheet_markdown(fields, acts, bottom).split("\n\n")
    return [ge.parse_blocks(chunk)[0]["rows"] for chunk in lines[:3]]


def placeholder(n, k):
    return "@@D%03d%s@@" % (n, "ABC"[k])


def white_bold_centre(tab_id, cell):
    start, end = ge.cell_range(cell)
    return [{"updateTextStyle": {"range": {"startIndex": start, "endIndex": end, "tabId": tab_id},
                                 "textStyle": {"foregroundColor": gdoc_form.WHITE, "bold": True},
                                 "fields": "foregroundColor,bold"}},
            {"updateParagraphStyle": {"range": {"startIndex": start, "endIndex": end + 1,
                                                "tabId": tab_id},
                                      "paragraphStyle": {"alignment": "CENTER"}, "fields": "alignment"}}]


def centre(tab_id, start, end):
    return {"updateParagraphStyle": {"range": {"startIndex": start, "endIndex": end, "tabId": tab_id},
                                     "paragraphStyle": {"alignment": "CENTER"}, "fields": "alignment"}}


def step_dictionary(doc, tab_n, text, limit, pause):
    sheets = sheets_of(text)
    order = list(sheets)
    tab_id, content = read(doc, tab_n)
    todo = []
    for n, heading in enumerate(order):
        head = heading_el(content, heading)
        if head is None:
            raise SystemExit("sheet heading %r not found in the tab" % heading)
        if not sheet_done(content, head):
            todo.append((n, heading))
    if limit:
        todo = todo[:limit]
    print("dictionary: %d of %d sheets to rebuild" % (len(todo), len(order)))

    # 1. Replace each sheet's old tables with the new text: placeholders and the page footer.
    reqs = []
    for n, heading in reversed(todo):
        head = heading_el(content, heading)
        end = sheet_end(content, head)
        if end > head["endIndex"]:
            reqs.append({"deleteContentRange": {"range": {"startIndex": head["endIndex"],
                                                          "endIndex": end, "tabId": tab_id}}})
        md = "\n\n".join([placeholder(n, 0), placeholder(n, 1), placeholder(n, 2), PAGE_FOOTER])
        plain, specs, _ = ge.compose_blocks(ge.parse_blocks(md))
        reqs += ge.block_requests(tab_id, head["endIndex"], plain, specs)
    send(doc, reqs)
    print("  1 text written (%d API calls)" % doc.calls)

    # 2. An empty table in front of each placeholder, whose text is removed.
    tab_id, content = read(doc, tab_n)
    shapes = {}
    for n, heading in todo:
        for k, rows in enumerate(sheet_tables(*sheets[heading])):
            shapes[placeholder(n, k)] = (len(rows), max(len(r) for r in rows))
    reqs = []
    for el in reversed([el for el in content if "paragraph" in el]):
        key = ge.para_text(el).strip()
        if key in shapes:
            rows, cols = shapes[key]
            reqs.append({"deleteContentRange": {"range": {"startIndex": el["startIndex"],
                                                          "endIndex": el["endIndex"] - 1,
                                                          "tabId": tab_id}}})
            reqs.append({"insertTable": {"rows": rows, "columns": cols,
                                         "location": {"index": el["startIndex"], "tabId": tab_id}}})
    send(doc, reqs)
    print("  2 tables inserted (%d API calls)" % doc.calls)

    # 3. Fill every cell, the last cell of the last sheet first.
    tab_id, content = read(doc, tab_n)
    reqs = []
    for n, heading in reversed(todo):
        head = heading_el(content, heading)
        tables = tables_after(content, head["startIndex"], 3)
        for el, rows in reversed(list(zip(tables, sheet_tables(*sheets[heading])))):
            reqs += doc.fill_table(tab_id, el, rows, header=False)
    send(doc, reqs)
    print("  3 cells filled (%d API calls)" % doc.calls)

    # 4. Merges: the title bar, the Responsible Person row, and the two-tier activity header.
    tab_id, content = read(doc, tab_n)
    reqs = []
    for n, heading in reversed(todo):
        head = heading_el(content, heading)
        top, acts, _low = tables_after(content, head["startIndex"], 3)
        reqs += [gdoc_form.merge(tab_id, acts, 0, 9, 2, 1), gdoc_form.merge(tab_id, acts, 0, 6, 1, 3),
                 gdoc_form.merge(tab_id, acts, 0, 3, 1, 3), gdoc_form.merge(tab_id, acts, 0, 2, 2, 1),
                 gdoc_form.merge(tab_id, acts, 0, 1, 2, 1), gdoc_form.merge(tab_id, acts, 0, 0, 2, 1),
                 gdoc_form.merge(tab_id, top, 5, 0, 1, 2), gdoc_form.merge(tab_id, top, 0, 0, 1, 2)]
    send(doc, reqs)
    print("  4 cells merged (%d API calls)" % doc.calls)
    step_style(doc, tab_n, order)


def step_style(doc, tab_n, order):
    """Shading, widths, the white title, centred headers and footer, and a page per sheet. None of
    these moves an index, so every sheet in the new layout is styled in one pass."""
    tab_id, content = read(doc, tab_n)
    reqs = []
    for heading in order:
        head = heading_el(content, heading)
        if not sheet_done(content, head):
            continue
        top, acts, low = tables_after(content, head["startIndex"], 3)
        reqs += [gdoc_form.style(tab_id, top, 0, 0, 1, 2, background=gdoc_form.DARK),
                 gdoc_form.style(tab_id, acts, 0, 0, 2, 10, background=gdoc_form.GREY)]
        reqs += gdoc_form.column_widths(tab_id, top, TOP_WIDTHS)
        reqs += gdoc_form.column_widths(tab_id, acts, ACTIVITY_WIDTHS)
        reqs += gdoc_form.column_widths(tab_id, low, [sum(TOP_WIDTHS)])
        reqs += white_bold_centre(tab_id, ge.table_cells(top)[0][0])
        for row in ge.table_cells(acts)[:2]:
            for cell in row:
                start, end = ge.cell_range(cell)
                reqs.append(centre(tab_id, start, end + 1))
        footer = next(el for el in content if "paragraph" in el and el["startIndex"] > low["startIndex"]
                      and ge.para_text(el).strip() == PAGE_FOOTER)
        reqs.append(centre(tab_id, footer["startIndex"], footer["endIndex"]))
        # Each sheet starts a page, as form 2.10 prints it; a phase heading right above moves with it.
        before = [el for el in content if "paragraph" in el and el["endIndex"] <= head["startIndex"]
                  and ge.para_text(el).strip()]
        lead = before[-1] if before and before[-1]["paragraph"].get("paragraphStyle", {}).get(
            "namedStyleType") == "HEADING_4" else head
        reqs.append({"updateParagraphStyle": {
            "range": {"startIndex": lead["startIndex"], "endIndex": lead["endIndex"], "tabId": tab_id},
            "paragraphStyle": {"pageBreakBefore": True}, "fields": "pageBreakBefore"}})
    send(doc, reqs)
    print("  5 styled (%d API calls)" % doc.calls)


# ------------------------------------------------------------------ rtm and text

def step_rtm(doc, tab_n, text):
    block = text[text.index("#### 3.1.2"):]
    table = next(b for b in ge.parse_blocks(block) if b["type"] == "table")
    want = table["rows"][1:]
    tab_id, content = doc.tab(tab_n)
    el = gdoc_form.find_table(content, "INTER-REQUIREMENTS TRACEABILITY MATRIX")
    cells = ge.table_cells(el)
    data = cells[2:]
    if len(data) != len(want):
        raise SystemExit("inter-requirements matrix has %d rows in the Doc, %d in the source"
                         % (len(data), len(want)))
    reqs, n = [], 0
    for r in range(len(want) - 1, -1, -1):
        for c in range(len(want[r]) - 1, -1, -1):
            plain, _ = ge.parse_inline(want[r][c])
            if ge.cell_text(data[r][c]).strip() != plain:
                reqs += doc.set_cell(tab_id, data[r][c], want[r][c])
                n += 1
    doc.batch(reqs)
    print("rtm: %d cells rewritten" % n)


def plain_paragraphs(text):
    return [ge.parse_inline(b["text"])[0] for b in ge.parse_blocks(text) if b["type"] == "para"]


def step_text(doc, tab_n, text):
    """Replace the words that differ between a source paragraph and the tab paragraph that opens
    the same way. Paragraphs that already match, or have no counterpart, are left alone."""
    tab_id, content = doc.tab(tab_n)
    have = [ge.para_text(el).strip() for el in content if "paragraph" in el]
    reqs, n = [], 0
    for w in plain_paragraphs(text):
        if w in have or len(w) < 80:
            continue
        match = [o for o in have if o[:60] == w[:60]]
        if len(match) != 1:
            continue
        o = match[0]
        p = 0
        while p < min(len(o), len(w)) and o[p] == w[p]:
            p += 1
        s = 0
        while s < min(len(o), len(w)) - p and o[-1 - s] == w[-1 - s]:
            s += 1
        # Widen to whole words and some context so the match is unique in the tab.
        a = max(0, o.rfind(" ", 0, max(0, p - 30)))
        b_old = len(o) - s
        b_old = o.find(" ", b_old + 30) if o.find(" ", b_old + 30) > 0 else len(o)
        b_new = b_old + (len(w) - len(o))
        reqs.append({"replaceAllText": {"containsText": {"text": o[a:b_old], "matchCase": True},
                                        "replaceText": w[a:b_new],
                                        "tabsCriteria": {"tabIds": [tab_id]}}})
        n += 1
        print("  text: %r -> %r" % (o[a:b_old][:70], w[a:b_new][:70]))
    doc.batch(reqs)
    print("text: %d paragraphs updated" % n)


# ------------------------------------------------------------------ main

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--doc", required=True)
    p.add_argument("--tab", default="3: Scope Baseline")
    p.add_argument("--md", default=str(ROOT / "docs" / "scope-package.en.md"))
    p.add_argument("--step", choices=["dictionary", "rtm", "text", "all"], default="all")
    p.add_argument("--token", default=os.path.join(DEFAULT_DIR, "token.json"))
    p.add_argument("--limit", type=int, default=0, help="rebuild at most this many sheets")
    p.add_argument("--sleep", type=float, default=1.0)
    a = p.parse_args(argv)

    import gdoc

    text = payload(a.md)
    doc = ge.Doc(gdoc.docs(gdoc.load_creds(pathlib.Path(a.token))), a.doc)
    names = [t[0].strip() for t in doc.tabs()]
    if a.tab.strip() not in names:
        raise SystemExit("no tab %r; tabs present: %s" % (a.tab, names))
    tab_n = names.index(a.tab.strip())
    if a.step in ("text", "all"):
        step_text(doc, tab_n, text)
    if a.step in ("rtm", "all"):
        step_rtm(doc, tab_n, text)
    if a.step in ("dictionary", "all"):
        step_dictionary(doc, tab_n, text, a.limit, a.sleep)
    print("done, %d API calls" % doc.calls)
    return 0


if __name__ == "__main__":
    sys.exit(main())
