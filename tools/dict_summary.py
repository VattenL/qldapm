#!/usr/bin/env python3
"""Form 2.10 at control account level, written into a tab of the team's Google Doc.

Page 52 of the book: the WBS dictionary "can provide detailed information about each work package or
summary information at the control account level". Section 3.3 of the Doc does the first, one sheet
per work package. This builds the second, one sheet per control account, from those same sheets and
nothing else: every sentence is quoted from a work package sheet, every number is a sum of its rows.

What a control account sheet carries, field by printed field:

  - Work Package Name and Code of Accounts: the control account, labels kept as printed;
  - Description of Work: the first sentence of each work package's description, under its code;
  - Assumptions and Constraints: each work package's assumptions, repeats dropped, and the
    first-pass estimate tag once;
  - Milestones and Due Dates: the work packages' milestones, each due at the finish of its work
    package, or on the charter gate date when the milestone is a gate;
  - the table: one row per work package and resource, the hours and money of that resource's
    activities in the package summed, and each material row as it stands;
  - Quality Requirements, Acceptance Criteria, Technical Information, Agreement Information: each
    work package's text under its code.

Responsible Person is not on the printed form and is left out; the Resource column names the people.

Usage:
    python tools/dict_summary.py --md docs/scope-package.en.md --preview out.md
    python tools/dict_summary.py --md docs/scope-package.en.md --doc DOC_ID --tab "dict rút gọn"
"""

from __future__ import annotations

import argparse
import collections
import os
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc_edit as ge  # noqa: E402
import scope_tab3  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_DIR = os.path.expanduser("~/.config/qldapm")
TITLE = "Development and Deployment of a Learning Center Management Software"
TAG = "<mark>First-pass estimate, re-baselined at M1.</mark>"
DATE = r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) \d{1,2} [A-Z][a-z]+ \d{4}"
NCOLS = 10
# Points, filling the 648pt text width of a landscape Letter page with one-inch margins: ID,
# Activity, Resource, then Labor and Material three each, Total Cost.
WIDTHS = [48, 180, 52, 42, 52, 62, 38, 52, 58, 64]
LEFT = 3   # the printed form's left block spans ID, Activity and Resource
FONT_PT = 9

# ------------------------------------------------------------------ reading the scope package


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def num(text):
    text = text.replace(",", "").replace("*", "").strip()
    return float(text) if text else 0.0


def parse(md):
    """The WBS outline as (code, name, note) and the dictionary sheets by code."""
    block = re.search(r"## Part 2: Work Breakdown Structure.*?```\n(.*?)```", md, re.S).group(1)
    outline = []
    for raw in block.splitlines():
        m = re.match(r"^\s*(\d+(?:\.\d+)*)\.?\s+(.+?)(?:\s{2,}(.*))?$", raw)
        if m:
            outline.append((m.group(1), m.group(2).strip(), (m.group(3) or "").strip()))
    sheets, cur = collections.OrderedDict(), None
    # Quoted text must read as the Doc reads it: section numbers, not the repository's Part headings.
    for raw in scope_tab3.doc_references(md[md.index("## Part 3"):]).splitlines():
        h = re.match(r"^#### (1(?:\.\d+){3}) (.+)$", raw)
        if h:
            cur = dict(code=h.group(1), name=h.group(2), fields={}, labour=[], material=[], stated=None)
            sheets[cur["code"]] = cur
            continue
        if cur is None or not raw.startswith("|") or raw.startswith("| ---"):
            continue
        c = cells(raw)
        if len(c) == 2 and c[0] != "Field":
            cur["fields"][c[0]] = c[1]
        elif len(c) == NCOLS and c[0] != "ID":
            if "Work package total" in c[1]:
                cur["stated"] = (num(c[3]), num(c[5]), num(c[8]), num(c[9]))
            elif c[2]:
                cur["labour"].append(dict(res=c[2], hours=num(c[3]), rate=num(c[4]), total=num(c[5])))
            elif c[6]:
                cur["material"].append(dict(name=c[1], units=num(c[6]), cost=num(c[7]), total=num(c[8])))
    return outline, sheets


def plain(text):
    return re.sub(r"</?mark>|\*\*", "", text)


def first_sentence(text):
    """The first sentence, or the whole text when a cut would split a highlight."""
    m = re.search(r"(?<=[a-z0-9)%])\.\s+(?=[A-Z])", text)
    if not m:
        return text
    head = text[: m.start() + 1]
    return head if head.count("<mark>") == head.count("</mark>") else text


def split_milestones(text):
    return [re.sub(r"^\d+\.\s*", "", p).strip() for p in re.split(r";\s*(?=\d+\.\s)", text) if p.strip()]


def gate_dates(sheets):
    """{gate: date} from the "M1 on <date>" entries the owning sheets carry in Due Dates."""
    out = {}
    for s in sheets.values():
        for g, d in re.findall(r"\b(M\d) on (%s)" % DATE, plain(s["fields"].get("Due Dates", ""))):
            out.setdefault(g, d)
    return out


def due_of(milestone, due_field, gates):
    """The date a milestone of a work package is due.

    A milestone that is a gate, or is set at or by one ("Risk register baselined at M1"), is due on
    that gate's date. Any other is due by the finish of its work package.
    """
    gate = re.match(r"^(M\d)\b", milestone) or re.search(r"\b(?:at|by) (M\d)\b", milestone)
    if gate and gate.group(1) in gates:
        return gates[gate.group(1)]
    text = plain(due_field)
    m = re.search(r"to (%s)" % DATE, text) or re.search(r"(%s)" % DATE, text)
    return m.group(1) if m else ""


def fmt(x):
    return "{:,.0f}".format(x) if float(x).is_integer() else "{:,.1f}".format(x)


def build(md):
    """One record per control account, in outline order."""
    outline, sheets = parse(md)
    gates = gate_dates(sheets)
    cas = [(c, n) for c, n, note in outline if note == "CA"]
    phases = {c: n for c, n, note in outline if c.count(".") == 1}
    records = []
    for ca, name in cas:
        wps = [s for code, s in sheets.items() if code.rsplit(".", 1)[0] == ca]
        if not wps:
            raise SystemExit("control account %s has no work package sheet" % ca)
        rec = dict(code=ca, name=name, phase=(ca.rsplit(".", 1)[0], phases[ca.rsplit(".", 1)[0]]),
                   wps=[s["code"] for s in wps], desc=[], assume=[], milestones=[], rows=[],
                   quality=[], accept=[], tech=[], agree=[])
        seen_assume = {}
        for s in wps:
            f = s["fields"]
            rec["desc"].append((s["code"], s["name"], first_sentence(f.get("Description of Work", ""))))
            a = f.get("Assumptions and Constraints", "").replace(TAG, "").strip()
            if a:
                if a in seen_assume:
                    seen_assume[a].append(s["code"])
                else:
                    seen_assume[a] = [s["code"]]
                    rec["assume"].append((seen_assume[a], a))
            for ms in split_milestones(f.get("Milestones", "")):
                rec["milestones"].append((s["code"], ms, due_of(ms, f.get("Due Dates", ""), gates)))
            for key, out in (("Quality Requirements", "quality"), ("Acceptance Criteria", "accept"),
                             ("Technical Information", "tech")):
                if f.get(key, "").strip():
                    rec[out].append((s["code"], f[key].strip()))
            ag = f.get("Agreement Information", "").strip()
            if ag:
                hit = next((x for x in rec["agree"] if x[1] == ag), None)
                if hit:
                    hit[0].append(s["code"])
                else:
                    rec["agree"].append(([s["code"]], ag))
            # One row per resource, in the order the activities name them.
            by_res = collections.OrderedDict()
            for a_ in s["labour"]:
                r = by_res.setdefault(a_["res"], dict(hours=0.0, rate=a_["rate"], total=0.0))
                if r["rate"] != a_["rate"]:
                    raise SystemExit("%s: %s at two rates" % (s["code"], a_["res"]))
                r["hours"] += a_["hours"]
                r["total"] += a_["total"]
            first = True
            for res, r in by_res.items():
                rec["rows"].append([s["code"] if first else "", s["name"] if first else "", res,
                                    fmt(r["hours"]), fmt(r["rate"]), fmt(r["total"]), "", "", "",
                                    fmt(r["total"])])
                first = False
            for m_ in s["material"]:
                rec["rows"].append([s["code"] if first else "", m_["name"], "", "", "", "",
                                    fmt(m_["units"]), fmt(m_["cost"]), fmt(m_["total"]), fmt(m_["total"])])
                first = False
            hours = sum(a_["hours"] for a_ in s["labour"])
            labour = sum(a_["total"] for a_ in s["labour"])
            mat = sum(m_["total"] for m_ in s["material"])
            if s["stated"] and s["stated"] != (hours, labour, mat, labour + mat):
                raise SystemExit("%s: rows do not add up to the stated work package total" % s["code"])
        hours = sum(num(r[3]) for r in rec["rows"])
        labour = sum(num(r[5]) for r in rec["rows"])
        mat = sum(num(r[8]) for r in rec["rows"])
        rec["total"] = (hours, labour, mat, labour + mat)
        records.append(rec)
    return records


# ------------------------------------------------------------------ the sheet as cell paragraphs


def listed(pairs, name_first=False):
    out = []
    for p in pairs:
        codes, text = p[0], p[-1]
        code = ", ".join(codes) if isinstance(codes, list) else codes
        out.append("%s: %s" % (code, text))
    return out


def sheet_cells(rec, prepared):
    """{(row, col): [markdown paragraph, ...]} for the head cell of every block of the form."""
    ms = rec["milestones"]
    body = {
        (0, 0): ["WBS DICTIONARY"],
        (1, 0): ["**Project Title:** %s      **Date Prepared:** %s" % (TITLE, prepared)],
        (2, 0): ["**Work Package Name:** %s (control account)" % rec["name"]],
        (2, LEFT): ["**Code of Accounts:** %s" % rec["code"]],
        (3, 0): ["**Description of Work:**"] + ["%s %s: %s" % (c, n, d) for c, n, d in rec["desc"]],
        (3, LEFT): ["**Assumptions and Constraints:**"] + listed(rec["assume"]) + [TAG],
        (4, 0): ["**Milestones:**"] + ["%d. %s (%s)" % (i, m, c) for i, (c, m, _d) in enumerate(ms, 1)],
        (4, LEFT): ["**Due Dates:**"] + ["%d. <mark>%s</mark>" % (i, d) if d else "%d." % i
                                        for i, (_c, _m, d) in enumerate(ms, 1)],
    }
    header = ["ID", "Activity", "Resource", "Labor", "", "", "Material", "", "", "Total Cost"]
    sub = ["", "", "", "Hours", "Rate", "Total", "Units", "Cost", "Total", ""]
    for c, t in enumerate(header):
        if t:
            body[(5, c)] = ["**%s**" % t]
    for c, t in enumerate(sub):
        if t:
            body[(6, c)] = ["**%s**" % t]
    r = 7
    for row in rec["rows"]:
        for c, t in enumerate(row):
            if t:
                body[(r, c)] = [t]
        r += 1
    h, lab, mat, tot = rec["total"]
    for c, t in ((1, "**Control account total**"), (3, "**%s**" % fmt(h)), (5, "**%s**" % fmt(lab)),
                 (8, "**%s**" % fmt(mat)), (9, "**%s**" % fmt(tot))):
        body[(r, c)] = [t]
    r += 1
    for key, label in (("quality", "Quality Requirements"), ("accept", "Acceptance Criteria"),
                       ("tech", "Technical Information"), ("agree", "Agreement Information")):
        body[(r, 0)] = ["**%s:**" % label] + listed(rec[key])
        r += 1
    return body, r


def merges(rec):
    """(row, col, rows, cols) of every merged block, the printed form's layout."""
    n_rows = len(rec["rows"])
    out = [(0, 0, 1, NCOLS), (1, 0, 1, NCOLS)]
    for r in (2, 3, 4):
        out += [(r, 0, 1, LEFT), (r, LEFT, 1, NCOLS - LEFT)]
    out += [(5, 0, 2, 1), (5, 1, 2, 1), (5, 2, 2, 1), (5, 3, 1, 3), (5, 6, 1, 3), (5, 9, 2, 1)]
    first_field = 7 + n_rows + 1
    out += [(first_field + k, 0, 1, NCOLS) for k in range(4)]
    return out


def preview(records, prepared):
    """Markdown for reading the content before it is written; not the Doc's layout."""
    out = []
    for rec in records:
        body, n = sheet_cells(rec, prepared)
        out.append("#### %s %s\n" % (rec["code"], rec["name"]))
        for (r, c), paras in sorted(body.items()):
            if r in (5, 6) or 7 <= r < 7 + len(rec["rows"]) + 1:
                continue
            out.append("\n".join(paras) + "\n")
        out.append("| ID | Activity | Resource | Hours | Rate | Labor | Units | Cost | Material | Total |")
        out.append("| --- " * NCOLS + "|")
        for row in rec["rows"]:
            out.append("| " + " | ".join(row) + " |")
        h, lab, mat, tot = rec["total"]
        out.append("| | **Control account total** | | %s | | %s | | | %s | %s |\n" % (fmt(h), fmt(lab), fmt(mat), fmt(tot)))
    return "\n".join(out)


# ------------------------------------------------------------------ writing the Doc

SLIM = ("tabs(tabProperties(tabId,title),documentTab(body(content(startIndex,endIndex,sectionBreak,"
        "paragraph(elements(textRun(content))),table(rows,columns,tableRows(tableCells(startIndex,"
        "endIndex,content(startIndex,endIndex,paragraph(elements(textRun(content)))))))))))")
DARK = {"color": {"rgbColor": {"red": 0.25, "green": 0.25, "blue": 0.27}}}
GREY = {"color": {"rgbColor": {"red": 0.89, "green": 0.89, "blue": 0.89}}}
WHITE = {"color": {"rgbColor": {"red": 1.0, "green": 1.0, "blue": 1.0}}}
PH = "@@SHEET@@"


class Writer:
    def __init__(self, svc, doc_id, title, sleep=1.0):
        self.svc, self.id, self.title, self.sleep, self.calls = svc, doc_id, title, sleep, 0

    def read(self):
        d = self.svc.documents().get(documentId=self.id, includeTabsContent=True, fields=SLIM).execute()
        for t in d["tabs"]:
            if t["tabProperties"]["title"].strip() == self.title:
                return t["tabProperties"]["tabId"], t["documentTab"]["body"]["content"]
        raise SystemExit("no tab titled %r" % self.title)

    def batch(self, reqs):
        """One batchUpdate. The API answers a sound request with a 500 or 503 now and then, and a
        batch is atomic, so the same batch is sent again after a pause."""
        from googleapiclient.errors import HttpError
        if not reqs:
            return
        for attempt in range(4):
            try:
                self.svc.documents().batchUpdate(documentId=self.id, body={"requests": reqs}).execute()
                break
            except HttpError as e:
                if e.resp.status not in (500, 503) or attempt == 3:
                    raise
                print("    API %d, retrying in %ds" % (e.resp.status, 5 * (attempt + 1)))
                time.sleep(5 * (attempt + 1))
        self.calls += 1
        time.sleep(self.sleep)


def text_requests(tab_id, index, paragraphs, font_pt=None):
    """Insert paragraphs (markdown inline) at index as one run; return (requests, length)."""
    plains, styles, pos = [], [], 0
    for k, md in enumerate(paragraphs):
        p, st = ge.parse_inline(md)
        styles += [(pos + a, pos + b, key) for a, b, key in st]
        plains.append(p)
        pos += len(p) + (1 if k < len(paragraphs) - 1 else 0)
    text = "\n".join(plains)
    if not text:
        return [], 0
    reqs = [{"insertText": {"location": {"index": index, "tabId": tab_id}, "text": text}}]
    reqs += ge.style_requests(tab_id, index, styles, reset_len=len(text))
    if font_pt:
        reqs.append({"updateTextStyle": {"range": {"startIndex": index, "endIndex": index + len(text), "tabId": tab_id},
                                         "textStyle": {"fontSize": {"magnitude": font_pt, "unit": "PT"}},
                                         "fields": "fontSize"}})
    return reqs, len(text)


def write_intro(w, prepared, n_ca, n_wp):
    tab_id, content = w.read()
    if len("".join(ge.para_text(e) for e in content if "paragraph" in e).strip()):
        return False
    md = "\n\n".join([
        "## WBS Dictionary, control account level",
        "**Project Title:** %s" % TITLE,
        "**Date Prepared:** %s" % prepared,
        "#### Reading convention",
        "- Form 2.10 filled at control account level. Page 52 of the book allows the dictionary to give "
        "\"detailed information about each work package or summary information at the control account "
        "level\"; section 3.3 does the first, with %d sheets, and this tab does the second, with one sheet "
        "for each of the %d control accounts of section 3.2." % (n_wp, n_ca),
        "- The printed labels are kept. Work Package Name and Code of Accounts carry the control account.",
        "- Nothing here is new. Each sentence is quoted from a work package sheet of section 3.3, under "
        "that work package's code; Description of Work quotes the first sentence of each description.",
        "- Each table row is one work package and one resource: the hours and money of that resource's "
        "activities in the package, summed. Material rows are as in section 3.3. The activity list itself "
        "stays in section 3.3.",
        "- A milestone is due by the finish of the work package that carries it, or on the charter gate "
        "date when the milestone is a gate or is set at one. Dates are highlighted as in section 3.3.",
        "- The highlighted tag means what it means in section 3.3: the hours, money and dates are a "
        "first-pass estimate, re-baselined at M1.",
        "- Responsible Person is not on the printed form and is not used; the Resource column names the "
        "people who do the work.",
    ]) + "\n"
    blocks = ge.parse_blocks(md)
    text, specs, _tables = ge.compose_blocks(blocks)
    end = content[-1]["endIndex"] - 1
    reqs = ge.block_requests(tab_id, end, text, specs)
    reqs.append({"updateSectionStyle": {"range": {"startIndex": end, "endIndex": end + len(text), "tabId": tab_id},
                                        "sectionStyle": {"flipPageOrientation": True},
                                        "fields": "flipPageOrientation"}})
    w.batch(reqs)
    return True


def sheet_state(content, heading):
    """'absent', 'unmerged' (placeholder still there), 'empty' (merged, not filled) or 'done'."""
    head = next((e for e in content if "paragraph" in e and ge.para_text(e).strip() == heading), None)
    if head is None:
        return "absent"
    after = [e for e in content if e.get("startIndex", -1) > head["startIndex"]]
    if any("paragraph" in e and ge.para_text(e).strip() == PH for e in after):
        return "unmerged"
    table = next(e for e in after if "table" in e)
    return "empty" if ge.cell_text(ge.table_cells(table)[0][0]) == "" else "done"


def page_label(page, pages):
    """The sheets are one form set, numbered through as the book numbers a form of several pages."""
    return "Page %d of %d" % (page, pages)


def write_sheet(w, rec, prepared, page, pages):
    heading = "%s %s" % (rec["code"], rec["name"])
    tab_id, content = w.read()
    state = sheet_state(content, heading)
    if state == "done":
        return False
    if state == "unmerged":
        raise SystemExit("%s was left half written; delete it from its heading and run again" % heading)
    body, n_rows = sheet_cells(rec, prepared)
    if state == "empty":
        fill_sheet(w, rec, body, heading)
        return True
    end = content[-1]["endIndex"] - 1
    text = "%s\n%s\n%s\n" % (heading, PH, page_label(page, pages))
    h_end = end + len(heading) + 1
    ph_end = h_end + len(PH) + 1
    reqs = [{"insertText": {"location": {"index": end, "tabId": tab_id}, "text": text}},
            {"updateTextStyle": {"range": {"startIndex": end, "endIndex": end + len(text), "tabId": tab_id},
                                 "textStyle": {"bold": False, "italic": False, "backgroundColor": {}},
                                 "fields": "bold,italic,backgroundColor"}},
            {"updateParagraphStyle": {"range": {"startIndex": end, "endIndex": end + len(text), "tabId": tab_id},
                                      "paragraphStyle": {"namedStyleType": "NORMAL_TEXT", "alignment": "START"},
                                      "fields": "namedStyleType,alignment"}},
            {"updateParagraphStyle": {"range": {"startIndex": end, "endIndex": h_end, "tabId": tab_id},
                                      "paragraphStyle": {"namedStyleType": "HEADING_4", "pageBreakBefore": True},
                                      "fields": "namedStyleType,pageBreakBefore"}},
            {"updateParagraphStyle": {"range": {"startIndex": ph_end, "endIndex": end + len(text), "tabId": tab_id},
                                      "paragraphStyle": {"alignment": "CENTER"}, "fields": "alignment"}},
            {"updateTextStyle": {"range": {"startIndex": ph_end, "endIndex": end + len(text) - 1, "tabId": tab_id},
                                 "textStyle": {"bold": True}, "fields": "bold"}},
            {"insertTable": {"rows": n_rows, "columns": NCOLS, "location": {"index": h_end, "tabId": tab_id}}}]
    w.batch(reqs)

    # Delete the placeholder, then merge the empty table into the printed blocks.
    tab_id, content = w.read()
    ph = ge.find_para(content, lambda t: t == PH)
    table = next(el for el in reversed(ge.top_tables(content)) if el["endIndex"] <= ph["startIndex"])
    start = {"index": table["startIndex"], "tabId": tab_id}
    reqs = [{"deleteContentRange": {"range": {"startIndex": ph["startIndex"], "endIndex": ph["endIndex"], "tabId": tab_id}}}]
    for r, c, rs, cs in merges(rec):
        reqs.append({"mergeTableCells": {"tableRange": {
            "tableCellLocation": {"tableStartLocation": start, "rowIndex": r, "columnIndex": c},
            "rowSpan": rs, "columnSpan": cs}}})
    w.batch(reqs)
    fill_sheet(w, rec, body, heading)
    return True


def fill_sheet(w, rec, body, heading):
    """Fill the head cells from the last to the first, so earlier indexes stay valid, then style."""
    tab_id, content = w.read()
    head = next(e for e in content if "paragraph" in e and ge.para_text(e).strip() == heading)
    table = next(e for e in content if "table" in e and e["startIndex"] > head["startIndex"])
    grid = ge.table_cells(table)
    start = {"index": table["startIndex"], "tabId": tab_id}
    numeric = set(range(3, NCOLS))
    reqs = []
    for (r, c) in sorted(body, reverse=True):
        idx = grid[r][c]["content"][0]["startIndex"]
        ins, n = text_requests(tab_id, idx, body[(r, c)], font_pt=FONT_PT)
        reqs += ins
        if (r, c) == (0, 0):
            reqs.append({"updateTextStyle": {"range": {"startIndex": idx, "endIndex": idx + n, "tabId": tab_id},
                                             "textStyle": {"bold": True, "foregroundColor": WHITE,
                                                           "fontSize": {"magnitude": 14, "unit": "PT"}},
                                             "fields": "bold,foregroundColor,fontSize"}})
        align = None
        if (r, c) == (0, 0) or r in (5, 6):
            align = "CENTER"
        elif 7 <= r < 7 + len(rec["rows"]) + 1 and c in numeric:
            align = "END"
        if align:
            reqs.append({"updateParagraphStyle": {"range": {"startIndex": idx, "endIndex": idx + n + 1, "tabId": tab_id},
                                                  "paragraphStyle": {"alignment": align}, "fields": "alignment"}})
    def shade(r, c, rs, cs, colour):
        return {"updateTableCellStyle": {"tableRange": {
            "tableCellLocation": {"tableStartLocation": start, "rowIndex": r, "columnIndex": c},
            "rowSpan": rs, "columnSpan": cs},
            "tableCellStyle": {"backgroundColor": colour}, "fields": "backgroundColor"}}
    reqs.append(shade(0, 0, 1, NCOLS, DARK))
    reqs.append(shade(5, 0, 2, NCOLS, GREY))
    for col, pt in enumerate(WIDTHS):
        reqs.append({"updateTableColumnProperties": {"tableStartLocation": start, "columnIndices": [col],
                                                     "tableColumnProperties": {"widthType": "FIXED_WIDTH",
                                                                               "width": {"magnitude": pt, "unit": "PT"}},
                                                     "fields": "widthType,width"}})
    w.batch(reqs)
    return True


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--md", default=str(ROOT / "docs" / "scope-package.en.md"))
    p.add_argument("--prepared", default="30 September 2026")
    p.add_argument("--preview", default="")
    p.add_argument("--doc", default="")
    p.add_argument("--tab", default="dict rút gọn")
    p.add_argument("--token", default=os.path.join(DEFAULT_DIR, "token.json"))
    p.add_argument("--limit", type=int, default=0)
    a = p.parse_args(argv)

    md = pathlib.Path(a.md).read_text(encoding="utf-8")
    records = build(md)
    n_wp = sum(len(r["wps"]) for r in records)
    total = [sum(r["total"][k] for r in records) for k in range(4)]
    print("%d control accounts, %d work packages, %s hours, %s VND labour, %s VND other, %s VND"
          % (len(records), n_wp, fmt(total[0]), fmt(total[1]), fmt(total[2]), fmt(total[3])))
    if a.preview:
        pathlib.Path(a.preview).write_text(preview(records, a.prepared), encoding="utf-8")
        print("preview written to", a.preview)
    if not a.doc:
        return 0

    import gdoc

    w = Writer(gdoc.docs(gdoc.load_creds(pathlib.Path(a.token))), a.doc, a.tab)
    if write_intro(w, a.prepared, len(records), n_wp):
        print("  wrote the heading and the reading convention")
    written = 0
    for k, rec in enumerate(records, 1):
        if a.limit and written >= a.limit:
            print("  stopping at --limit %d" % a.limit)
            break
        if write_sheet(w, rec, a.prepared, k, len(records)):
            written += 1
            print("  wrote %s %s (%d rows)" % (rec["code"], rec["name"], len(rec["rows"])))
        else:
            print("  skip %s, already present" % rec["code"])
    fixed = fix_page_labels(w, records)
    if fixed:
        print("  renumbered %d page labels" % fixed)
    fix_widths(w)
    print("done: %d sheets, %d write calls" % (written, w.calls))
    return 0


def fix_page_labels(w, records):
    """Set the label under each sheet to its place in the set; sheets written earlier said 1 of 1."""
    tab_id, content = w.read()
    edits = []
    for k, rec in enumerate(records, 1):
        heading = "%s %s" % (rec["code"], rec["name"])
        head = next((e for e in content if "paragraph" in e and ge.para_text(e).strip() == heading), None)
        if head is None:
            continue
        table = next(e for e in content if "table" in e and e["startIndex"] > head["startIndex"])
        label = next(e for e in content if "paragraph" in e and e["startIndex"] >= table["endIndex"]
                     and ge.para_text(e).strip())
        old = ge.para_text(label).rstrip("\n")
        if not old.startswith("Page "):
            raise SystemExit("no page label under %s" % heading)
        if old != page_label(k, len(records)):
            edits.append((label["startIndex"], len(old), page_label(k, len(records))))
    reqs = []
    for start, n, new in sorted(edits, reverse=True):
        reqs += [{"deleteContentRange": {"range": {"startIndex": start, "endIndex": start + n, "tabId": tab_id}}},
                 {"insertText": {"location": {"index": start, "tabId": tab_id}, "text": new}},
                 {"updateTextStyle": {"range": {"startIndex": start, "endIndex": start + len(new), "tabId": tab_id},
                                      "textStyle": {"bold": True}, "fields": "bold"}}]
    w.batch(reqs)
    return len(edits)


def fix_widths(w):
    """Give every sheet table of the tab the current column widths, in one call."""
    tab_id, content = w.read()
    reqs = []
    for table in ge.top_tables(content):
        if table["table"]["columns"] != NCOLS:
            continue
        start = {"index": table["startIndex"], "tabId": tab_id}
        for col, pt in enumerate(WIDTHS):
            reqs.append({"updateTableColumnProperties": {
                "tableStartLocation": start, "columnIndices": [col],
                "tableColumnProperties": {"widthType": "FIXED_WIDTH", "width": {"magnitude": pt, "unit": "PT"}},
                "fields": "widthType,width"}})
    w.batch(reqs)


if __name__ == "__main__":
    sys.exit(main())
