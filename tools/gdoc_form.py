"""Printed-form layout for tables already written into a Google Doc.

gdoc_edit.py renders a Markdown table as a plain grid, because Markdown carries nothing else: no
merged cells, no column spans, no cell shading, no column widths, no page orientation. The forms in
A Project Manager's Book of Forms carry all of those. So the content still comes from the Markdown,
and the layout is applied here afterwards, against the Doc.

What this reproduces from the printed form:

  - the dark title bar across the full width, white bold text;
  - the two-tier header whose group labels span several columns, as in form 2.7 where Requirement
    Information spans five columns and Relationship Traceability spans four;
  - fixed column widths in the printed proportions;
  - landscape pages for the tables too wide to read in portrait.

Every function returns requests or drives a Doc from tools/gdoc_edit.py. Nothing here authors content.
"""

from __future__ import annotations

import gdoc_edit as ge

DARK = {"color": {"rgbColor": {"red": 0.25, "green": 0.25, "blue": 0.27}}}
GREY = {"color": {"rgbColor": {"red": 0.89, "green": 0.89, "blue": 0.89}}}
WHITE = {"color": {"rgbColor": {"red": 1.0, "green": 1.0, "blue": 1.0}}}


def _start(tab_id, table_el):
    return {"index": table_el["startIndex"], "tabId": tab_id}


def _cell(tab_id, table_el, row, col):
    return {"tableStartLocation": _start(tab_id, table_el), "rowIndex": row, "columnIndex": col}


def _range(tab_id, table_el, row, col, rows=1, cols=1):
    return {"tableCellLocation": _cell(tab_id, table_el, row, col),
            "rowSpan": rows, "columnSpan": cols}


def merge(tab_id, table_el, row, col, rows=1, cols=1):
    return {"mergeTableCells": {"tableRange": _range(tab_id, table_el, row, col, rows, cols)}}


def style(tab_id, table_el, row, col, rows=1, cols=1, background=None, align="MIDDLE"):
    cell_style, fields = {}, []
    if background is not None:
        cell_style["backgroundColor"] = background
        fields.append("backgroundColor")
    if align:
        cell_style["contentAlignment"] = align
        fields.append("contentAlignment")
    return {"updateTableCellStyle": {
        "tableRange": _range(tab_id, table_el, row, col, rows, cols),
        "tableCellStyle": cell_style,
        "fields": ",".join(fields)}}


def column_widths(tab_id, table_el, widths):
    """widths is a list of points, one per column. Columns with a width of 0 are left alone."""
    reqs = []
    for col, pt in enumerate(widths):
        if not pt:
            continue
        reqs.append({"updateTableColumnProperties": {
            "tableStartLocation": _start(tab_id, table_el),
            "columnIndices": [col],
            "tableColumnProperties": {"widthType": "FIXED_WIDTH",
                                      "width": {"magnitude": pt, "unit": "PT"}},
            "fields": "widthType,width"}})
    return reqs


def insert_row_above(tab_id, table_el, row=0):
    return {"insertTableRow": {"tableCellLocation": _cell(tab_id, table_el, row, 0),
                               "insertBelow": False}}


def section_break(tab_id, index, landscape):
    """Start a new page-level section at index. Orientation is set afterwards, by flip()."""
    return {"insertSectionBreak": {"location": {"index": index, "tabId": tab_id},
                                   "sectionType": "NEXT_PAGE"}}


def flip(tab_id, start, end, landscape):
    return {"updateSectionStyle": {
        "range": {"startIndex": start, "endIndex": end, "tabId": tab_id},
        "sectionStyle": {"flipPageOrientation": bool(landscape)},
        "fields": "flipPageOrientation"}}


def find_table(content, first_cell, ncols=None, last=False):
    """The first top-level table whose top-left cell reads first_cell, or the last one with last=True.

    The tab holds one activity table per dictionary sheet, all of them starting with the same cell,
    so a caller styling the sheet it has just written must ask for the last.
    """
    tables = ge.top_tables(content)
    for el in (reversed(tables) if last else tables):
        rows = ge.table_cells(el)
        if not rows or not rows[0]:
            continue
        if ge.cell_text(rows[0][0]).strip() != first_cell:
            continue
        if ncols is not None and len(rows[0]) != ncols:
            continue
        return el
    return None


def apply_form(doc, tab_n, first_cell, title, groups=(), widths=(), ncols=None):
    """Give a table the printed-form look: title bar, optional group header, column widths.

    groups is a sequence of (label, start_column, span). The table is read back between batches
    because inserting a row and merging cells both move every index after them.
    """
    tab_id, content = doc.tab(tab_n)
    table_el = find_table(content, first_cell, ncols)
    if table_el is None:
        raise KeyError("no table starting with %r" % first_cell)
    ncols = len(ge.table_cells(table_el)[0])
    start_index = table_el["startIndex"]

    rows_to_add = 2 if groups else 1
    for _ in range(rows_to_add):
        doc.batch([insert_row_above(tab_id, table_el, 0)])
        tab_id, content = doc.tab(tab_n)
        table_el = next(el for el in ge.top_tables(content) if el["startIndex"] == start_index)

    # Text first, then merges: a merge keeps only the content of its top-left cell.
    cells = ge.table_cells(table_el)
    reqs = []
    if groups:
        for label, col, _span in reversed(groups):
            reqs += doc.set_cell(tab_id, cells[1][col], "**%s**" % label)
    reqs += doc.set_cell(tab_id, cells[0][0], "**%s**" % title)
    doc.batch(reqs)

    tab_id, content = doc.tab(tab_n)
    table_el = next(el for el in ge.top_tables(content) if el["startIndex"] == start_index)
    reqs = [merge(tab_id, table_el, 0, 0, 1, ncols)]
    for _label, col, span in groups:
        if span > 1:
            reqs.append(merge(tab_id, table_el, 1, col, 1, span))
    doc.batch(reqs)

    tab_id, content = doc.tab(tab_n)
    table_el = next(el for el in ge.top_tables(content) if el["startIndex"] == start_index)
    reqs = [style(tab_id, table_el, 0, 0, 1, 1, background=DARK)]
    if groups:
        reqs.append(style(tab_id, table_el, 1, 0, 1, ncols, background=GREY))
    reqs += column_widths(tab_id, table_el, widths)
    doc.batch(reqs)

    # The title bar reads white on dark; the Doc writer left it black.
    tab_id, content = doc.tab(tab_n)
    table_el = next(el for el in ge.top_tables(content) if el["startIndex"] == start_index)
    title_cell = ge.table_cells(table_el)[0][0]
    start, end = ge.cell_range(title_cell)
    doc.batch([{"updateTextStyle": {
        "range": {"startIndex": start, "endIndex": end, "tabId": tab_id},
        "textStyle": {"foregroundColor": WHITE, "bold": True},
        "fields": "foregroundColor,bold"}},
        {"updateParagraphStyle": {
            "range": {"startIndex": start, "endIndex": end, "tabId": tab_id},
            "paragraphStyle": {"alignment": "CENTER"},
            "fields": "alignment"}}])
    return table_el
