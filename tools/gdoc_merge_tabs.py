#!/usr/bin/env python3
"""Merge the tabs of a Google Doc into one new tab, in tab order, leaving out the tabs named with --skip.

The Docs API has no request that copies content, so every element is written again from a saved
documents.get read (tools/gdoc.py get): paragraph text, paragraph and text styles, bullets, inline
images, page breaks, tables with their column widths, row heights, header rows, cell styles and
merged cells, and section breaks with their page orientation. Each source tab starts on a new page
in a section that keeps the tab's orientation. The source tabs are not changed.

What the API cannot write is reported by `plan` and left out: floating (positioned) images, and
the glyph of a bulleted list that no bullet preset offers, which gets the closest preset.

Positions are computed from the read instead of read back after every write, because a full read
of a large Doc takes half a minute: the new tab holds the same elements as the sources, so every
element keeps its length. `run` checks the tab's end index before each batch against the computed
one and stops on the first difference. `verify` compares the written tab with the sources.

Run with:
    python tools/gdoc.py get --doc DOC_ID --out src.json
    python tools/gdoc_merge_tabs.py plan --source src.json --skip nhap --out plan.json
    python tools/gdoc_merge_tabs.py run --doc DOC_ID --plan plan.json --title "Merged"
    python tools/gdoc.py get --doc DOC_ID --out after.json
    python tools/gdoc_merge_tabs.py verify --source src.json --after after.json --plan plan.json

Image URIs in a read expire after a while, so `plan` and `run` follow the read closely.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import socket
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc

TAB = "@TAB@"
TEXT_FIELDS = ["bold", "italic", "underline", "strikethrough", "smallCaps", "backgroundColor",
               "foregroundColor", "fontSize", "weightedFontFamily", "baselineOffset", "link"]
PARA_FIELDS = ["alignment", "lineSpacing", "direction", "spacingMode", "spaceAbove", "spaceBelow",
               "borderBetween", "borderTop", "borderBottom", "borderLeft", "borderRight",
               "indentFirstLine", "indentStart", "indentEnd", "keepLinesTogether", "keepWithNext",
               "avoidWidowAndOrphan", "shading", "pageBreakBefore"]
CELL_FIELDS = ["backgroundColor", "borderLeft", "borderRight", "borderTop", "borderBottom",
               "paddingLeft", "paddingRight", "paddingTop", "paddingBottom", "contentAlignment"]
ROW_FIELDS = ["minRowHeight", "preventOverflow"]
CHUNK = 1500
DEFAULT_DIR = os.path.expanduser("~/.config/qldapm")
# The client library waits 60 s by default; a read of a Doc this size can take longer.
socket.setdefaulttimeout(600)


def u16(s: str) -> int:
    return len(s.encode("utf-16-le")) // 2


def rng(a: int, b: int) -> dict:
    return {"startIndex": a, "endIndex": b, "tabId": TAB}


def loc(i: int) -> dict:
    return {"index": i, "tabId": TAB}


def length(e) -> int:
    return e["endIndex"] - e.get("startIndex", 0)


def preset_for(level: dict) -> tuple[str, bool]:
    """Bullet preset for a list's first nesting level, and whether it draws the source glyph."""
    glyph_type, symbol = level.get("glyphType"), level.get("glyphSymbol")
    if glyph_type == "DECIMAL":
        return "NUMBERED_DECIMAL_ALPHA_ROMAN", level.get("glyphFormat") == "%0."
    if glyph_type == "UPPER_ALPHA":
        return "NUMBERED_UPPERALPHA_ALPHA_ROMAN", level.get("glyphFormat") == "%0."
    if symbol == "●":
        return "BULLET_DISC_CIRCLE_SQUARE", True
    return "BULLET_DISC_CIRCLE_SQUARE", False


def tab_list(doc):
    out, stack = [], list(doc["tabs"])
    while stack:
        t = stack.pop(0)
        out.append(t)
        stack = list(t.get("childTabs", [])) + stack
    return out


def para_text(e) -> str:
    return "".join(x.get("textRun", {}).get("content", "") for x in e["paragraph"]["elements"]).strip()


def body_of(tab, drops):
    """The tab's body after its first section break. drops maps a tab title to the heading text from
    which the rest of that tab is left out, with the section break right before the heading."""
    content = tab["documentTab"]["body"]["content"]
    if "sectionBreak" not in content[0]:
        raise ValueError(f"tab {tab['tabProperties']['title']!r} does not start with a section break")
    body = content[1:]
    heading = drops.get(tab["tabProperties"]["title"])
    if heading is None:
        return body
    cut = next((i for i, e in enumerate(body) if "paragraph" in e and para_text(e) == heading), None)
    if cut is None:
        raise ValueError(f"heading {heading!r} not found in tab {tab['tabProperties']['title']!r}")
    if cut and "sectionBreak" in body[cut - 1]:
        cut -= 1
    return body[:cut]


def flip_of(tab) -> bool:
    return tab["documentTab"].get("documentStyle", {}).get("flipPageOrientation", False)


# -------------------------------------------------------------------- planning


class Writer:
    """Builds the requests. Positions in the new tab come from the caller; lengths from the read."""

    def __init__(self):
        self.out: list = []
        self.notes: list = []
        self.lists: dict = {}
        self.inline: dict = {}
        self.title = ""
        self.flip = False
        self.in_cell = False

    def use_tab(self, tab, flip):
        dt = tab["documentTab"]
        self.title = tab["tabProperties"]["title"]
        self.lists = dt.get("lists", {})
        self.inline = dt.get("inlineObjects", {})
        self.flip = flip

    # --- styles

    def para_style(self, p, a, b, only_present=False):
        ps = p.get("paragraphStyle", {})
        out = []
        if not only_present:
            out.append({"updateParagraphStyle": {"range": rng(a, b), "paragraphStyle": {
                "namedStyleType": ps.get("namedStyleType", "NORMAL_TEXT")}, "fields": "namedStyleType"}})
        fields = [f for f in PARA_FIELDS if f in ps] if only_present else PARA_FIELDS
        if self.in_cell:
            # Docs refuses page-break-before on a paragraph in a table
            fields = [f for f in fields if f != "pageBreakBefore"]
        if fields:
            out.append({"updateParagraphStyle": {"range": rng(a, b), "paragraphStyle": {
                f: ps[f] for f in fields if f in ps}, "fields": ",".join(fields)}})
        return out

    def run_style(self, el, d):
        ts = el["textRun"].get("textStyle", {})
        return {"updateTextStyle": {"range": rng(el["startIndex"] + d, el["endIndex"] + d),
                                    "textStyle": {f: ts[f] for f in TEXT_FIELDS if f in ts},
                                    "fields": ",".join(TEXT_FIELDS)}}

    # --- paragraphs

    def paragraph(self, e, start, newline):
        """Write paragraph e at start. Without newline, its newline is the empty paragraph already
        at start: the last paragraph of a cell or of the body."""
        p = e["paragraph"]
        els = p["elements"]
        pos, text = start, ""

        def flush():
            nonlocal pos, text
            if text:
                self.out.append({"insertText": {"location": loc(pos), "text": text}})
                pos += u16(text)
                text = ""

        for k, el in enumerate(els):
            if "textRun" in el:
                content = el["textRun"]["content"]
                if k == len(els) - 1:
                    if not content.endswith("\n"):
                        raise ValueError(f"{self.title}: paragraph at {e['startIndex']} does not end in a newline")
                    if not newline:
                        content = content[:-1]
                text += content
            elif "inlineObjectElement" in el:
                flush()
                obj = self.inline[el["inlineObjectElement"]["inlineObjectId"]]["inlineObjectProperties"]["embeddedObject"]
                self.out.append({"insertInlineImage": {"location": loc(pos), "uri": obj["imageProperties"]["contentUri"],
                                                       "objectSize": obj["size"]}})
                pos += 1
            elif "pageBreak" in el:
                rest = els[k + 1:]
                if not newline or len(rest) != 1 or rest[0].get("textRun", {}).get("content") != "\n":
                    raise ValueError(f"{self.title}: page break at {el['startIndex']} is not at the end of its paragraph")
                flush()
                # insertPageBreak writes the paragraph's newline as well
                self.out.append({"insertPageBreak": {"location": loc(pos)}})
                pos += 2
                break
            else:
                raise ValueError(f"{self.title}: unsupported element {sorted(el)} at {el.get('startIndex')}")
        flush()
        n = length(e)
        if pos - start != n - (0 if newline else 1):
            raise AssertionError(f"{self.title}: paragraph at {e['startIndex']} writes {pos - start}, expected {n}")
        self.out += self.para_style(p, start, start + n)
        d = start - e["startIndex"]
        self.out += [self.run_style(el, d) for el in els if "textRun" in el]
        return n

    def bullets(self, group):
        first_e, first_at = group[0]
        last_e, last_at = group[-1]
        level = self.lists[first_e["paragraph"]["bullet"]["listId"]]["listProperties"]["nestingLevels"][0]
        preset, exact = preset_for(level)
        if not exact:
            self.notes.append(f"{self.title}: list glyph {level.get('glyphSymbol') or level.get('glyphType')!r} "
                              f"written as {preset}, {len(group)} item(s)")
        self.out.append({"createParagraphBullets": {"range": rng(first_at, last_at + length(last_e)),
                                                    "bulletPreset": preset}})
        # the preset sets its own indents; put back the ones the source paragraphs carry
        for e, at in group:
            self.out += self.para_style(e["paragraph"], at, at + length(e), only_present=True)

    def restyle_prev(self, prev):
        """A table or section break goes in at the newline of the paragraph before it, which then ends
        in a new newline: give that paragraph back its style and its last run's style."""
        e, at = prev
        p = e["paragraph"]
        out = self.para_style(p, at, at + length(e), only_present=bool(p.get("bullet")))
        # Every run, not only the last: a run before the old newline can lose its size and emphasis too.
        out += [self.run_style(el, at - e["startIndex"]) for el in p["elements"] if "textRun" in el]
        return out

    # --- containers

    def container(self, content, pos, prev=None, last_in_place=False, boundary=None):
        """Write a sequence of paragraphs, tables and section breaks from pos. Returns (pos, prev).
        boundary(pos) is called between elements where a batch may be cut (never inside a list)."""
        group: list = []
        for i, e in enumerate(content):
            if "paragraph" in e:
                bullet = e["paragraph"].get("bullet")
                if bullet and bullet.get("nestingLevel", 0):
                    raise ValueError(f"{self.title}: nested list item at {e['startIndex']} is not supported")
                if group and (not bullet or group[-1][0]["paragraph"]["bullet"]["listId"] != bullet["listId"]):
                    self.bullets(group)
                    group = []
                if boundary and not group:
                    boundary(pos)
                n = self.paragraph(e, pos, newline=not (last_in_place and i == len(content) - 1))
                if bullet:
                    group.append((e, pos))
                prev = (e, pos)
                pos += n
                continue
            if group:
                self.bullets(group)
                group = []
            if boundary:
                boundary(pos)
            if prev is None:
                raise ValueError(f"{self.title}: {sorted(e)} at {e.get('startIndex')} has no paragraph before it")
            if "table" in e:
                self.table(e, pos, prev)
                pos += length(e)
            elif "sectionBreak" in e:
                flip = e["sectionBreak"].get("sectionStyle", {}).get("flipPageOrientation", False)
                self.section_break(pos, prev, flip ^ self.flip)
                pos += 1
            else:
                raise ValueError(f"{self.title}: unsupported element {sorted(e)}")
            prev = None
        if group:
            self.bullets(group)
        return pos, prev

    def section_break(self, pos, prev, flip):
        # At the previous paragraph's newline: the break lands at pos and the old newline becomes an
        # empty paragraph at pos + 1, which is removed.
        self.out += [{"insertSectionBreak": {"sectionType": "NEXT_PAGE", "location": loc(pos - 1)}},
                     {"deleteContentRange": {"range": rng(pos + 1, pos + 2)}},
                     *self.restyle_prev(prev),
                     {"updateSectionStyle": {"range": rng(pos + 1, pos + 2),
                                             "sectionStyle": {"flipPageOrientation": flip},
                                             "fields": "flipPageOrientation"}}]

    def table(self, e, T, prev):
        t = e["table"]
        rows, cols = t["rows"], t["columns"]
        size = rows * (2 * cols + 1)
        where = {"tableStartLocation": loc(T)}
        # Same trick as the section break: the table starts at T, the old newline after it is removed.
        self.out += [{"insertTable": {"rows": rows, "columns": cols, "location": loc(T - 1)}},
                     {"deleteContentRange": {"range": rng(T + 2 + size, T + 3 + size)}}]
        self.out += self.restyle_prev(prev)
        for c, cp in enumerate(t.get("tableStyle", {}).get("tableColumnProperties", [])):
            fields = [f for f in ("widthType", "width") if f in cp]
            if fields:
                self.out.append({"updateTableColumnProperties": {"tableStartLocation": loc(T), "columnIndices": [c],
                                                                 "tableColumnProperties": cp, "fields": ",".join(fields)}})
        header = 0
        for r, row in enumerate(t["tableRows"]):
            rs = row.get("tableRowStyle", {})
            fields = [f for f in ROW_FIELDS if f in rs]
            if fields:
                self.out.append({"updateTableRowStyle": {"tableStartLocation": loc(T), "rowIndices": [r],
                                                         "tableRowStyle": {f: rs[f] for f in fields},
                                                         "fields": ",".join(fields)}})
            if rs.get("tableHeader") and header == r:
                header = r + 1
        if header:
            self.out.append({"pinTableHeaderRows": {"tableStartLocation": loc(T), "pinnedHeaderRowsCount": header}})
        merges = []
        for r, row in enumerate(t["tableRows"]):
            if len(row["tableCells"]) != cols:
                raise ValueError(f"{self.title}: table at {e['startIndex']} row {r} has {len(row['tableCells'])} cells")
            for c, cell in enumerate(row["tableCells"]):
                cs = cell.get("tableCellStyle", {})
                fields = [f for f in CELL_FIELDS if f in cs]
                if fields:
                    self.out.append({"updateTableCellStyle": {
                        "tableRange": {"tableCellLocation": {**where, "rowIndex": r, "columnIndex": c},
                                       "rowSpan": 1, "columnSpan": 1},
                        "tableCellStyle": {f: cs[f] for f in fields}, "fields": ",".join(fields)}})
                if cs.get("rowSpan", 1) > 1 or cs.get("columnSpan", 1) > 1:
                    merges.append({"mergeTableCells": {"tableRange": {
                        "tableCellLocation": {**where, "rowIndex": r, "columnIndex": c},
                        "rowSpan": cs.get("rowSpan", 1), "columnSpan": cs.get("columnSpan", 1)}}})
        self.out += merges
        # Merging empty cells moves nothing. Fill from the last cell so each fill shifts only cells
        # already filled.
        for r in range(rows - 1, -1, -1):
            for c in range(cols - 1, -1, -1):
                cell = t["tableRows"][r]["tableCells"][c]
                at = T + 3 + r * (2 * cols + 1) + 2 * c
                self.in_cell = True
                end, _ = self.container(cell["content"], at, last_in_place=True)
                self.in_cell = False
                if end - at != length(cell) - 1:
                    raise AssertionError(f"{self.title}: cell ({r},{c}) of table at {e['startIndex']} writes a wrong length")


def plan(src, skip, drops):
    tabs = [t for t in tab_list(src) if t["tabProperties"]["title"] not in skip]
    w = Writer()
    cuts = []  # (request count, end index of the tab body at that point)
    first_flip = flip_of(tabs[0])
    pos, prev = 1, None

    def boundary(at):
        if not cuts or len(w.out) - cuts[-1][0] >= CHUNK:
            cuts.append((len(w.out), at + 1))

    for n, tab in enumerate(tabs):
        body = body_of(tab, drops)
        if n:
            boundary(pos)
            w.section_break(pos, prev, flip_of(tab) ^ first_flip)
            pos += 1
        w.use_tab(tab, flip_of(tab) ^ first_flip)
        objs = tab["documentTab"].get("positionedObjects", {})
        if objs:
            w.notes.append(f"{w.title}: {len(objs)} floating image(s) left out, the API cannot write them")
        pos, prev = w.container(body, pos, prev=None, last_in_place=n == len(tabs) - 1, boundary=boundary)
        if prev is None:
            raise ValueError(f"tab {w.title!r} does not end with a paragraph")
    cuts.append((len(w.out), pos))
    chunks = [{"requests": w.out[a:b], "end_before": e0, "end_after": e1}
              for (a, e0), (b, e1) in zip(cuts, cuts[1:]) if b > a]
    return {"first_flip": first_flip, "end": pos, "notes": w.notes, "drops": drops,
            "sources": [t["tabProperties"]["title"] for t in tabs], "chunks": chunks}


# -------------------------------------------------------------------- running


def tab_end(svc, doc_id, tab_id):
    doc = svc.documents().get(documentId=doc_id, includeTabsContent=True,
                              fields="revisionId,tabs(tabProperties(tabId),documentTab(body(content(endIndex))))").execute()
    for t in tab_list(doc):
        if t["tabProperties"]["tabId"] == tab_id:
            return doc["revisionId"], t["documentTab"]["body"]["content"][-1]["endIndex"]
    raise KeyError(f"tab {tab_id} not found")


def send(svc, doc_id, requests, revision):
    from googleapiclient.errors import HttpError

    for attempt in range(6):
        try:
            return svc.documents().batchUpdate(documentId=doc_id, body={
                "requests": requests, "writeControl": {"targetRevisionId": revision}}).execute()
        except HttpError as ex:
            if ex.resp.status in (429, 500, 502, 503) and attempt < 5:
                time.sleep(15 * (attempt + 1))
                continue
            raise


def cmd_run(a, svc):
    pl = json.load(open(a.plan, encoding="utf-8"))
    state_path = pathlib.Path(a.plan + ".state.json")
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"next": 0}
    if "tabId" not in state:
        doc = svc.documents().get(documentId=a.doc, fields="revisionId").execute()
        reply = send(svc, a.doc, [{"addDocumentTab": {"tabProperties": {"title": a.title}}}], doc["revisionId"])
        state["tabId"] = reply["replies"][0]["addDocumentTab"]["tabProperties"]["tabId"]
        state_path.write_text(json.dumps(state), encoding="utf-8")
        print("created tab", state["tabId"], flush=True)
        if pl["first_flip"]:
            send(svc, a.doc, [{"updateDocumentStyle": {"tabId": state["tabId"], "documentStyle": {
                "flipPageOrientation": True}, "fields": "flipPageOrientation"}}], reply["writeControl"]["requiredRevisionId"])
    tab_id = state["tabId"]
    chunks = pl["chunks"]
    for k in range(state["next"], len(chunks)):
        ch = chunks[k]
        revision, end = tab_end(svc, a.doc, tab_id)
        if end != ch["end_before"]:
            sys.exit(f"batch {k}: tab ends at {end}, expected {ch['end_before']}; stopped")
        body = json.loads(json.dumps(ch["requests"]).replace(json.dumps(TAB), json.dumps(tab_id)))
        t0 = time.time()
        send(svc, a.doc, body, revision)
        state["next"] = k + 1
        state_path.write_text(json.dumps(state), encoding="utf-8")
        print(f"batch {k + 1}/{len(chunks)}: {len(body)} requests, {time.time() - t0:.0f}s", flush=True)
    _revision, end = tab_end(svc, a.doc, tab_id)
    print("tab", tab_id, "ends at", end, "expected", pl["end"], "ok" if end == pl["end"] else "MISMATCH")


# -------------------------------------------------------------------- verifying


def flat_style(p):
    """Per-character text style of a paragraph as (length, style) runs, equal neighbours joined."""
    out = []
    for el in p["elements"]:
        if "textRun" in el:
            key = json.dumps({f: el["textRun"].get("textStyle", {}).get(f) for f in TEXT_FIELDS
                              if el["textRun"].get("textStyle", {}).get(f) not in (None, {})}, sort_keys=True)
            n = u16(el["textRun"]["content"])
        else:
            key, n = sorted(set(el) - {"startIndex", "endIndex", "textStyle"})[0], 1
        if out and out[-1][1] == key:
            out[-1][0] += n
        else:
            out.append([n, key])
    return out


def compare(want, got, where, diffs, in_cell=False):
    kinds = lambda e: sorted(set(e) & {"paragraph", "table", "sectionBreak"})
    if len(want) != len(got):
        diffs.append((where, f"{len(want)} elements expected, {len(got)} found"))
    for i, (a, b) in enumerate(zip(want, got)):
        at = f"{where}[{i}]"
        if kinds(a) != kinds(b):
            diffs.append((at, f"{kinds(a)} expected, {kinds(b)} found"))
            return
        if "paragraph" in a:
            pa, pb = a["paragraph"], b["paragraph"]
            sa, sb = pa.get("paragraphStyle", {}), pb.get("paragraphStyle", {})
            if flat_style(pa) != flat_style(pb):
                diffs.append((at, "text or text style differs"))
            fields = ["namedStyleType"] + [f for f in PARA_FIELDS if (not pa.get("bullet") or f in sa)
                                           and not (in_cell and f == "pageBreakBefore")]
            bad = [f for f in fields if sa.get(f) != sb.get(f)]
            if bad:
                diffs.append((at, f"paragraph style differs: {bad}"))
            if bool(pa.get("bullet")) != bool(pb.get("bullet")):
                diffs.append((at, "bullet differs"))
        elif "table" in a:
            ta, tb = a["table"], b["table"]
            if (ta["rows"], ta["columns"]) != (tb["rows"], tb["columns"]):
                diffs.append((at, "table size differs"))
                continue
            if ta.get("tableStyle") != tb.get("tableStyle"):
                diffs.append((at, "column widths differ"))
            for r, (ra, rb) in enumerate(zip(ta["tableRows"], tb["tableRows"])):
                if ra.get("tableRowStyle", {}) != rb.get("tableRowStyle", {}):
                    diffs.append((f"{at} row {r}", "row style differs"))
                for c, (ca, cb) in enumerate(zip(ra["tableCells"], rb["tableCells"])):
                    if ca.get("tableCellStyle", {}) != cb.get("tableCellStyle", {}):
                        diffs.append((f"{at} cell {r},{c}", "cell style differs"))
                    compare(ca["content"], cb["content"], f"{at} cell {r},{c}", diffs, in_cell=True)
        elif "sectionBreak" in a:
            fa = a["sectionBreak"].get("sectionStyle", {}).get("flipPageOrientation", False)
            fb = b["sectionBreak"].get("sectionStyle", {}).get("flipPageOrientation", False)
            if fa != fb:
                diffs.append((at, f"orientation flip {fa} expected, {fb} found"))


def cmd_verify(a):
    src = json.load(open(a.source, encoding="utf-8"))
    after = json.load(open(a.after, encoding="utf-8"))
    pl = json.load(open(a.plan, encoding="utf-8"))
    state = json.loads(pathlib.Path(a.plan + ".state.json").read_text(encoding="utf-8"))
    by_title = {t["tabProperties"]["title"]: t for t in tab_list(src)}
    want, first_flip = [], pl["first_flip"]
    for n, title in enumerate(pl["sources"]):
        tab = by_title[title]
        if n:
            want.append({"sectionBreak": {"sectionStyle": {"flipPageOrientation": flip_of(tab) ^ first_flip}}})
        for e in body_of(tab, pl["drops"]):
            if "sectionBreak" in e:
                flip = e["sectionBreak"].get("sectionStyle", {}).get("flipPageOrientation", False)
                e = {"sectionBreak": {"sectionStyle": {"flipPageOrientation": flip ^ flip_of(tab) ^ first_flip}}}
            want.append(e)
    got_tab = next(t for t in tab_list(after) if t["tabProperties"]["tabId"] == state["tabId"])
    got = got_tab["documentTab"]["body"]["content"][1:]
    diffs: list = []
    compare(want, got, "body", diffs)
    print(f"{len(want)} top-level elements expected, {len(got)} found; {len(diffs)} difference(s)")
    for where, what in diffs[: a.limit]:
        print(" ", where, what)
    for note in pl["notes"]:
        print("note:", note)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--token", default=os.path.join(DEFAULT_DIR, "token.json"))
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("plan")
    s.add_argument("--source", required=True)
    s.add_argument("--skip", action="append", default=[], help="title of a tab to leave out; repeatable")
    s.add_argument("--drop", action="append", default=[], metavar="TAB=HEADING",
                   help="leave out the tab TAB from the paragraph HEADING to its end; repeatable")
    s.add_argument("--out", required=True)
    s = sub.add_parser("run")
    s.add_argument("--doc", required=True)
    s.add_argument("--plan", required=True)
    s.add_argument("--title", required=True, help="title of the new tab")
    s = sub.add_parser("verify")
    s.add_argument("--source", required=True)
    s.add_argument("--after", required=True)
    s.add_argument("--plan", required=True)
    s.add_argument("--limit", type=int, default=40)
    a = p.parse_args(argv)
    if a.cmd == "plan":
        drops = dict(d.split("=", 1) for d in a.drop)
        result = plan(json.load(open(a.source, encoding="utf-8")), set(a.skip), drops)
        pathlib.Path(a.out).write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
        n = sum(len(c["requests"]) for c in result["chunks"])
        print(f"{len(result['sources'])} tabs: {', '.join(result['sources'])}")
        print(f"{n} requests in {len(result['chunks'])} batches; the new tab will end at {result['end']}")
        for note in result["notes"]:
            print("note:", note)
    elif a.cmd == "run":
        cmd_run(a, gdoc.docs(gdoc.load_creds(pathlib.Path(a.token))))
    else:
        cmd_verify(a)


if __name__ == "__main__":
    main()
