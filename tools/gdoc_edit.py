"""Index-safe editing of a Google Doc from a Markdown subset.

Parser: headings (#..####), paragraphs, "- " bullets, "1. " numbered items, "> " quotes,
pipe tables (a "| --- |" separator marks a header row), "---" rules, and the inline
marks **bold**, *italic*, `code`, <mark>yellow</mark>.

Doc operations re-read the document after every batch and process cells from the
last one backwards, so the indexes computed from one read stay valid inside a batch.
"""

from __future__ import annotations

import re

YELLOW = {"color": {"rgbColor": {"red": 1.0, "green": 1.0, "blue": 0.0}}}
NAMED_HEADING = {1: "HEADING_1", 2: "HEADING_2", 3: "HEADING_3", 4: "HEADING_4", 5: "HEADING_5"}
PLACEHOLDER = "@@TABLE{}@@"
# Points of left indent per outline level; the printed WBS steps each level in by about a quarter inch.
OUTLINE_INDENT = 18

# ------------------------------------------------------------------ inline markdown

_TOKEN = re.compile(r"(\*\*|\*|<mark>|</mark>|`)")


def parse_inline(text: str):
    """Return (plain, styles); styles is a list of (start, end, key) with key in bold/italic/mark/code."""
    plain, styles, opened = [], [], {}
    pos = 0
    for part in _TOKEN.split(text):
        if part == "**":
            key = "bold"
        elif part == "*":
            key = "italic"
        elif part == "`":
            key = "code"
        elif part == "<mark>":
            opened["mark"] = pos
            continue
        elif part == "</mark>":
            if "mark" in opened:
                styles.append((opened.pop("mark"), pos, "mark"))
            continue
        else:
            plain.append(part)
            pos += len(part)
            continue
        if key in opened:
            styles.append((opened.pop(key), pos, key))
        else:
            opened[key] = pos
    for key, start in opened.items():
        styles.append((start, pos, key))
    return "".join(plain), [s for s in styles if s[0] < s[1]]


# ------------------------------------------------------------------ block markdown

_SEP_ROW = re.compile(r"^\|(\s*:?-{3,}:?\s*\|)+\s*$")


def _split_row(line: str):
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [c.strip() for c in inner.split("|")]


def parse_blocks(md: str):
    """Return a list of blocks: dicts with 'type' and fields."""
    lines = md.splitlines()
    blocks, i = [], 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        m = re.match(r"^(#{1,5})\s+(.*)$", line)
        if m:
            blocks.append({"type": "heading", "level": len(m.group(1)), "text": m.group(2).strip()})
            i += 1
            continue
        if s == "---":
            blocks.append({"type": "hr"})
            i += 1
            continue
        if s.startswith("```"):
            # A fenced block, used for the numbered outline printed on forms 2.9 and 2.29: one
            # paragraph per line, indented by its depth. Depth is the leading spaces divided by two.
            items = []
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                if lines[i].strip():
                    depth = (len(lines[i]) - len(lines[i].lstrip(" "))) // 2
                    items.append((depth, lines[i].strip()))
                i += 1
            i += 1
            blocks.append({"type": "outline", "items": items})
            continue
        if s.startswith("|"):
            rows, header = [], False
            while i < len(lines) and lines[i].strip().startswith("|"):
                if _SEP_ROW.match(lines[i].strip()):
                    header = len(rows) == 1
                else:
                    rows.append(_split_row(lines[i]))
                i += 1
            blocks.append({"type": "table", "rows": rows, "header": header})
            continue
        if s.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:].strip())
                i += 1
            blocks.append({"type": "bullets", "items": items})
            continue
        if re.match(r"^\d+\.\s", s):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            blocks.append({"type": "numbered", "items": items})
            continue
        if s.startswith("> "):
            parts = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                parts.append(lines[i].strip()[2:])
                i += 1
            blocks.append({"type": "quote", "text": " ".join(parts)})
            continue
        parts = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,5}\s|\||- |\d+\.\s|> |---$|```)", lines[i].strip()):
            parts.append(lines[i].strip())
            i += 1
        blocks.append({"type": "para", "text": " ".join(parts)})
    return blocks


def section(md: str, start: str, end: str | None = None) -> str:
    """Lines from the line starting with `start` (inclusive) up to the line starting with `end` (exclusive)."""
    lines = md.splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith(start))
    if end is None:
        return "\n".join(lines[i:])
    j = next(k for k in range(i + 1, len(lines)) if lines[k].startswith(end))
    return "\n".join(lines[i:j])


def first_table(md: str):
    return next(b for b in parse_blocks(md) if b["type"] == "table")


def table_by_first_cell(md: str, key: str):
    """Row (list of cell strings) whose first cell equals key, searched over every table in md."""
    for b in parse_blocks(md):
        if b["type"] == "table":
            for row in b["rows"]:
                if row and row[0] == key:
                    return row
    raise KeyError(key)


def field_map(table_block):
    """For 'Field | Content' tables: {plain field name: content markdown}."""
    out = {}
    for row in table_block["rows"]:
        if len(row) >= 2:
            out[parse_inline(row[0])[0]] = row[1]
    return out


# ------------------------------------------------------------------ requests from inline text

def style_requests(tab_id: str, base: int, styles, reset_len: int | None = None):
    reqs = []
    if reset_len:
        reqs.append({"updateTextStyle": {
            "range": {"startIndex": base, "endIndex": base + reset_len, "tabId": tab_id},
            "textStyle": {"bold": False, "italic": False, "backgroundColor": {}},
            "fields": "bold,italic,backgroundColor"}})
    for start, end, key in styles:
        rng = {"startIndex": base + start, "endIndex": base + end, "tabId": tab_id}
        if key == "bold":
            reqs.append({"updateTextStyle": {"range": rng, "textStyle": {"bold": True}, "fields": "bold"}})
        elif key == "italic":
            reqs.append({"updateTextStyle": {"range": rng, "textStyle": {"italic": True}, "fields": "italic"}})
        elif key == "mark":
            reqs.append({"updateTextStyle": {"range": rng, "textStyle": {"backgroundColor": YELLOW}, "fields": "backgroundColor"}})
    return reqs


def insert_inline(tab_id: str, index: int, md_text: str, bold_all: bool = False):
    """Requests that insert one paragraph's worth of text (no trailing newline) at index."""
    plain, styles = parse_inline(md_text)
    if not plain:
        return [], 0
    reqs = [{"insertText": {"location": {"index": index, "tabId": tab_id}, "text": plain}}]
    reqs += style_requests(tab_id, index, styles, reset_len=len(plain))
    if bold_all:
        reqs.append({"updateTextStyle": {"range": {"startIndex": index, "endIndex": index + len(plain), "tabId": tab_id},
                                         "textStyle": {"bold": True}, "fields": "bold"}})
    return reqs, len(plain)


def compose_blocks(blocks):
    """Turn blocks into (text, paragraph_specs, tables). Text ends with a newline per paragraph.

    paragraph_specs: list of dicts {start, end, kind, level, styles} with offsets into text.
    tables: list of table blocks in order; each is represented by a placeholder paragraph.
    """
    text, specs, tables = [], [], []
    pos = 0

    def add(plain, styles, kind, level=0):
        nonlocal pos
        line = plain + "\n"
        text.append(line)
        specs.append({"start": pos, "end": pos + len(line), "kind": kind, "level": level, "styles": styles})
        pos += len(line)

    for b in blocks:
        t = b["type"]
        if t == "heading":
            plain, styles = parse_inline(b["text"])
            add(plain, styles, "heading", b["level"])
        elif t == "para":
            plain, styles = parse_inline(b["text"])
            add(plain, styles, "para")
        elif t == "quote":
            plain, styles = parse_inline(b["text"])
            add(plain, styles, "quote")
        elif t in ("bullets", "numbered"):
            for k, item in enumerate(b["items"]):
                plain, styles = parse_inline(item)
                add(plain, styles, t, level=k)  # level marks position in the group
            specs[-1]["group_end"] = True
        elif t == "outline":
            for depth, item in b["items"]:
                plain, styles = parse_inline(item)
                add(plain, styles, "outline", level=depth)
        elif t == "table":
            tables.append(b)
            add(PLACEHOLDER.format(len(tables) - 1), [], "placeholder")
        elif t == "hr":
            continue
    return "".join(text), specs, tables


def block_requests(tab_id: str, index: int, text: str, specs):
    """Requests inserting composed text at index and styling its paragraphs."""
    reqs = [{"insertText": {"location": {"index": index, "tabId": tab_id}, "text": text}}]
    reqs.append({"updateTextStyle": {
        "range": {"startIndex": index, "endIndex": index + len(text), "tabId": tab_id},
        "textStyle": {"bold": False, "italic": False, "backgroundColor": {}},
        "fields": "bold,italic,backgroundColor"}})
    reqs.append({"updateParagraphStyle": {
        "range": {"startIndex": index, "endIndex": index + len(text), "tabId": tab_id},
        "paragraphStyle": {"namedStyleType": "NORMAL_TEXT", "alignment": "START", "indentStart": {"magnitude": 0, "unit": "PT"}},
        "fields": "namedStyleType,alignment,indentStart"}})
    group_start = None
    for sp in specs:
        rng = {"startIndex": index + sp["start"], "endIndex": index + sp["end"], "tabId": tab_id}
        reqs += style_requests(tab_id, index + sp["start"], sp["styles"])
        if sp["kind"] == "heading":
            reqs.append({"updateParagraphStyle": {"range": rng, "paragraphStyle": {"namedStyleType": NAMED_HEADING[sp["level"]]}, "fields": "namedStyleType"}})
        elif sp["kind"] == "quote":
            reqs.append({"updateParagraphStyle": {"range": rng, "paragraphStyle": {"indentStart": {"magnitude": 36, "unit": "PT"}}, "fields": "indentStart"}})
            reqs.append({"updateTextStyle": {"range": rng, "textStyle": {"italic": True}, "fields": "italic"}})
        elif sp["kind"] == "outline":
            reqs.append({"updateParagraphStyle": {"range": rng, "paragraphStyle": {
                "indentStart": {"magnitude": OUTLINE_INDENT * sp["level"], "unit": "PT"},
                "spaceAbove": {"magnitude": 6 if sp["level"] <= 1 else 0, "unit": "PT"}},
                "fields": "indentStart,spaceAbove"}})
        elif sp["kind"] in ("bullets", "numbered"):
            if group_start is None:
                group_start = sp["start"]
            if sp.get("group_end"):
                preset = "BULLET_DISC_CIRCLE_SQUARE" if sp["kind"] == "bullets" else "NUMBERED_DECIMAL_ALPHA_ROMAN"
                reqs.append({"createParagraphBullets": {
                    "range": {"startIndex": index + group_start, "endIndex": index + sp["end"], "tabId": tab_id},
                    "bulletPreset": preset}})
                group_start = None
    return reqs


# ------------------------------------------------------------------ reading structure

def para_text(el) -> str:
    return "".join(pe.get("textRun", {}).get("content", "") for pe in el["paragraph"].get("elements", []))


def top_paragraphs(content):
    return [el for el in content if "paragraph" in el]


def top_tables(content):
    return [el for el in content if "table" in el]


def find_para(content, pred, start_after: int = -1):
    for el in content:
        if "paragraph" in el and el["startIndex"] > start_after and pred(para_text(el).rstrip("\n")):
            return el
    raise KeyError("paragraph not found")


def table_after(content, para_el):
    for el in content:
        if "table" in el and el["startIndex"] >= para_el["endIndex"]:
            return el
    raise KeyError("no table after paragraph")


def cell_text(cell) -> str:
    return "".join(para_text(e) for e in cell["content"] if "paragraph" in e).rstrip("\n")


def cell_range(cell):
    """(start, end) of the cell's text excluding the final newline; equal when empty."""
    return cell["content"][0]["startIndex"], cell["endIndex"] - 1


def table_cells(table_el):
    return [[c for c in row["tableCells"]] for row in table_el["table"]["tableRows"]]


# ------------------------------------------------------------------ Doc wrapper

class Doc:
    def __init__(self, service, doc_id: str, log=print):
        self.svc = service
        self.id = doc_id
        self.log = log
        self.doc = None
        self.calls = 0
        self.refresh()

    def refresh(self):
        self.doc = self.svc.documents().get(documentId=self.id, includeTabsContent=True).execute()
        return self.doc

    def batch(self, requests):
        if not requests:
            return
        self.svc.documents().batchUpdate(documentId=self.id, body={"requests": requests}).execute()
        self.calls += 1
        self.refresh()

    def tabs(self):
        return [(t["tabProperties"]["title"], t["tabProperties"]["tabId"], t["documentTab"]["body"]["content"])
                for t in self.doc.get("tabs", [])]

    def tab(self, n: int):
        title, tab_id, content = self.tabs()[n]
        return tab_id, content

    def content(self, n: int):
        return self.tabs()[n][2]

    # --- cells

    def set_cell(self, tab_id, cell, md_text: str, bold_all: bool = False):
        """Requests replacing a cell's text (single paragraph). Apply cells from the last to the first."""
        start, end = cell_range(cell)
        reqs = []
        if end > start:
            reqs.append({"deleteContentRange": {"range": {"startIndex": start, "endIndex": end, "tabId": tab_id}}})
        ins, _ = insert_inline(tab_id, start, md_text, bold_all=bold_all)
        return reqs + ins

    def append_cell(self, tab_id, cell, md_text: str):
        _start, end = cell_range(cell)
        ins, _ = insert_inline(tab_id, end, md_text)
        return ins

    def fill_table(self, tab_id, table_el, rows, header: bool):
        """Requests filling an (empty or not) table from rows of markdown cells, last cell first."""
        cells = table_cells(table_el)
        reqs = []
        for r in range(len(cells) - 1, -1, -1):
            for c in range(len(cells[r]) - 1, -1, -1):
                md_text = rows[r][c] if r < len(rows) and c < len(rows[r]) else ""
                reqs += self.set_cell(tab_id, cells[r][c], md_text, bold_all=(header and r == 0))
        return reqs

    # --- rows and columns

    def insert_row_below(self, tab_n: int, table_el, row_idx: int, row_md):
        tab_id, _ = self.tab(tab_n)
        loc = {"tableStartLocation": {"index": table_el["startIndex"], "tabId": tab_id}, "rowIndex": row_idx, "columnIndex": 0}
        self.batch([{"insertTableRow": {"tableCellLocation": loc, "insertBelow": True}}])
        table_el = self._table_at(tab_n, table_el["startIndex"])
        cells = table_cells(table_el)[row_idx + 1]
        reqs = []
        for c in range(len(cells) - 1, -1, -1):
            reqs += self.set_cell(tab_id, cells[c], row_md[c] if c < len(row_md) else "")
        self.batch(reqs)
        return self._table_at(tab_n, table_el["startIndex"])

    def insert_column_before(self, tab_n: int, table_el, col_idx: int, values_md, header_bold=True):
        tab_id, _ = self.tab(tab_n)
        loc = {"tableStartLocation": {"index": table_el["startIndex"], "tabId": tab_id}, "rowIndex": 0, "columnIndex": col_idx}
        self.batch([{"insertTableColumn": {"tableCellLocation": loc, "insertRight": False}}])
        table_el = self._table_at(tab_n, table_el["startIndex"])
        cells = table_cells(table_el)
        reqs = []
        for r in range(len(cells) - 1, -1, -1):
            reqs += self.set_cell(tab_id, cells[r][col_idx], values_md[r] if r < len(values_md) else "", bold_all=(header_bold and r == 0))
        self.batch(reqs)
        return self._table_at(tab_n, table_el["startIndex"])

    def delete_column(self, tab_n: int, table_el, col_idx: int):
        tab_id, _ = self.tab(tab_n)
        loc = {"tableStartLocation": {"index": table_el["startIndex"], "tabId": tab_id}, "rowIndex": 0, "columnIndex": col_idx}
        self.batch([{"deleteTableColumn": {"tableCellLocation": loc}}])
        return self._table_at(tab_n, table_el["startIndex"])

    def _table_at(self, tab_n: int, start_index: int):
        for el in top_tables(self.content(tab_n)):
            if el["startIndex"] == start_index:
                return el
        raise KeyError(f"table at {start_index} not found")

    # --- blocks

    def delete_range(self, tab_id, start, end):
        if end > start:
            self.batch([{"deleteContentRange": {"range": {"startIndex": start, "endIndex": end, "tabId": tab_id}}}])

    def insert_markdown(self, tab_n: int, index: int, md: str):
        """Insert a Markdown block sequence so that it starts at index (which must be a paragraph start)."""
        tab_id, _ = self.tab(tab_n)
        blocks = parse_blocks(md)
        text, specs, tables = compose_blocks(blocks)
        if not text:
            return index
        self.batch(block_requests(tab_id, index, text, specs))
        end_index = index + len(text)
        for k in range(len(tables) - 1, -1, -1):
            end_index += self._materialise_table(tab_n, PLACEHOLDER.format(k), tables[k])
        return end_index

    def _materialise_table(self, tab_n: int, placeholder: str, table_block) -> int:
        """Replace the placeholder paragraph with a filled table. Returns the index growth."""
        tab_id, content = self.tab(tab_n)
        ph = find_para(content, lambda t: t == placeholder)
        rows = table_block["rows"]
        ncols = max(len(r) for r in rows)
        before_len = content[-1]["endIndex"]
        self.batch([{"insertTable": {"rows": len(rows), "columns": ncols,
                                     "location": {"index": ph["startIndex"], "tabId": tab_id}}}])
        tab_id, content = self.tab(tab_n)
        ph = find_para(content, lambda t: t == placeholder)
        table_el = next(el for el in reversed(top_tables(content)) if el["endIndex"] <= ph["startIndex"])
        reqs = [{"deleteContentRange": {"range": {"startIndex": ph["startIndex"], "endIndex": ph["endIndex"], "tabId": tab_id}}}]
        reqs += self.fill_table(tab_id, table_el, rows, table_block["header"])
        self.batch(reqs)
        # an empty paragraph the API put in front of the table is kept as spacing
        after_len = self.content(tab_n)[-1]["endIndex"]
        return after_len - before_len
