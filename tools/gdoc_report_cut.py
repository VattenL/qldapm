#!/usr/bin/env python3
"""Rebuild the combined report tab ("Báo cáo tổng hợp") as a new tab whose body, cover included, stays
under 90 pages, with every text in Arial and no text below 12 pt. The source tab is not changed.

The lecturer counts the pages before the appendices and marks by tracing a cell of a table up to where
its number comes from. So nothing is deleted: detail tables move to new appendices E to M, each place
they leave keeps its heading and a line naming the appendix, and every ID and figure stays. What is
cut is wording that repeats a defined scale (risk impacts written as H, M, L), and page breaks that
leave a page holding a heading only.

The new tab is written by the Writer of gdoc_merge_tabs.py from a read of the Doc changed in memory,
so the plan file has the same format and runs the same way:
    python tools/gdoc.py get --doc DOC_ID --out src.json
    python tools/gdoc_report_cut.py plan --source src.json --out cut.json
    python tools/gdoc_merge_tabs.py run --doc DOC_ID --plan cut.json --title "Báo cáo tổng hợp (rút gọn)"
    python tools/gdoc_report_cut.py pages --doc DOC_ID --tab NEW_TAB_ID
    python tools/gdoc_report_cut.py check --doc DOC_ID --tab NEW_TAB_ID --fix
`pages` needs pypdf (pip install pypdf). Image URIs in a read expire, so plan and run follow the read
closely. `delete-tab` removes a tab this script wrote, to run again.
"""

from __future__ import annotations

import argparse
import copy
import io
import json
import os
import pathlib
import re
import socket
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc
import gdoc_merge_tabs as merge

TAB = "Báo cáo tổng hợp"
APPENDICES = "Appendices"
FONT = "Arial"
MIN_PT = 12
PAD = {"magnitude": 2, "unit": "PT"}
DEFAULT_DIR = os.path.expanduser("~/.config/qldapm")
socket.setdefaulttimeout(900)

LEVEL = {"High": "H", "Medium": "M", "Low": "L"}
OWNER = re.compile(r"^.*\(([A-Z]+[0-9]*)\)$")


# ------------------------------------------------------------------ elements


def ptext(e) -> str:
    return "".join(x.get("textRun", {}).get("content", "") for x in e["paragraph"]["elements"])


def ctext(cell) -> str:
    return "".join(ptext(x) for x in cell["content"] if "paragraph" in x).strip()


def para(text: str, style: str = "NORMAL_TEXT", like=None) -> dict:
    """A new paragraph; like is a paragraph whose first run style it takes."""
    ts = {}
    if like is not None:
        runs = [x for x in like["paragraph"]["elements"] if "textRun" in x]
        ts = copy.deepcopy(runs[0]["textRun"].get("textStyle", {})) if runs else {}
        ts.pop("bold", None)
        ts.pop("backgroundColor", None)
    return {"paragraph": {"elements": [{"textRun": {"content": text + "\n", "textStyle": ts}}],
                          "paragraphStyle": {"namedStyleType": style}}}


def set_cell(cell, text: str):
    """Replace the cell's text, keeping its first paragraph's style and first run's style."""
    first = next(x for x in cell["content"] if "paragraph" in x)
    runs = [x for x in first["paragraph"]["elements"] if "textRun" in x]
    ts = copy.deepcopy(runs[0]["textRun"].get("textStyle", {})) if runs else {}
    first = copy.deepcopy(first)
    first["paragraph"]["elements"] = [{"textRun": {"content": text + "\n", "textStyle": ts}}]
    first["paragraph"].pop("bullet", None)
    cell["content"] = [first]


def heading_at(content, text: str, start: int = 0) -> int:
    for i in range(start, len(content)):
        e = content[i]
        if "paragraph" in e and ptext(e).strip() == text \
                and e["paragraph"]["paragraphStyle"].get("namedStyleType", "").startswith("HEADING"):
            return i
    raise SystemExit(f"heading {text!r} not found")


def table_at(content, first_cell: str, start: int = 0) -> int:
    for i in range(start, len(content)):
        e = content[i]
        if "table" in e and ctext(e["table"]["tableRows"][0]["tableCells"][0]).startswith(first_cell):
            return i
    raise SystemExit(f"table starting {first_cell!r} not found after element {start}")


def para_at(content, prefix: str, start: int = 0) -> int:
    for i in range(start, len(content)):
        if "paragraph" in content[i] and ptext(content[i]).startswith(prefix):
            return i
    raise SystemExit(f"paragraph starting {prefix!r} not found after element {start}")


# ------------------------------------------------------------------ indexes


def reindex(content, pos: int) -> int:
    """Give every element the indexes Docs would, from pos; return the end."""
    for e in content:
        if "sectionBreak" in e:
            if pos:
                e["startIndex"] = pos
            e["endIndex"] = pos + 1
            pos += 1
        elif "paragraph" in e:
            e["startIndex"] = pos
            for el in e["paragraph"]["elements"]:
                n = merge.u16(el["textRun"]["content"]) if "textRun" in el else 1
                el["startIndex"], el["endIndex"] = pos, pos + n
                pos += n
            e["endIndex"] = pos
        else:
            e["startIndex"] = pos
            pos += 1
            for row in e["table"]["tableRows"]:
                row["startIndex"] = pos
                pos += 1
                for cell in row["tableCells"]:
                    cell["startIndex"] = pos
                    pos = reindex(cell["content"], pos + 1)
                    cell["endIndex"] = pos
                row["endIndex"] = pos
            pos += 1
            e["endIndex"] = pos
    return pos


# ------------------------------------------------------------------ moves


class Appendix:
    """Collects the elements moved out of the body, each group under its own heading."""

    def __init__(self, first_letter: str = "E"):
        self.letter = first_letter
        self.out: list = []

    def move(self, content, i: int, j: int, title: str, pointer: str, style_like) -> str:
        """Move content[i:j] to a new appendix and leave the pointer paragraph in its place."""
        name = f"Appendix {self.letter}"
        self.letter = chr(ord(self.letter) + 1)
        moved = content[i:j]
        if any("sectionBreak" in e for e in moved):
            raise SystemExit(f"{name}: the moved range holds a section break")
        while moved and "paragraph" in moved[-1] and not ptext(moved[-1]).strip():
            moved.pop()
        self.out.append(para(f"{name}: {title}", "HEADING_3"))
        self.out += moved
        if "table" in moved[-1]:
            self.out.append(para("", like=style_like))
        content[i:j] = [para(pointer.format(name=name), like=style_like)]
        return name


# ------------------------------------------------------------------ style


def walk_paragraphs(content):
    for e in content:
        if "paragraph" in e:
            yield e
        elif "table" in e:
            for row in e["table"]["tableRows"]:
                for cell in row["tableCells"]:
                    yield from walk_paragraphs(cell["content"])


def walk_tables(content):
    for e in content:
        if "table" in e:
            yield e
            for row in e["table"]["tableRows"]:
                for cell in row["tableCells"]:
                    yield from walk_tables(cell["content"])


def restyle(content, named):
    """Arial everywhere, nothing under 12 pt, cell padding 2 pt. A new tab gets the default named
    styles, so each heading run carries the size, font, and colour its source named style gave it."""
    black = {"color": {"rgbColor": {}}}
    for e in walk_paragraphs(content):
        ps = e["paragraph"]["paragraphStyle"]
        kind = ps.get("namedStyleType", "NORMAL_TEXT")
        base = named.get(kind, {})
        if kind.startswith("HEADING"):
            for f in ("spaceAbove", "spaceBelow"):
                if f not in ps and f in base.get("paragraphStyle", {}):
                    ps[f] = base["paragraphStyle"][f]
        for el in e["paragraph"]["elements"]:
            if "textRun" not in el:
                continue
            ts = el["textRun"].setdefault("textStyle", {})
            weight = ts.get("weightedFontFamily", {}).get("weight", 400)
            ts["weightedFontFamily"] = {"fontFamily": FONT, "weight": weight}
            size = ts.get("fontSize", {}).get("magnitude") or base.get("textStyle", {}).get("fontSize", {}).get("magnitude")
            ts["fontSize"] = {"magnitude": max(MIN_PT, size or MIN_PT), "unit": "PT"}
            if kind.startswith("HEADING"):
                ts.setdefault("foregroundColor", black)
                ts.setdefault("bold", base.get("textStyle", {}).get("bold", False))
    for t in walk_tables(content):
        for row in t["table"]["tableRows"]:
            # A row that may not break across pages leaves the rest of a page empty when it does not fit.
            row.setdefault("tableRowStyle", {})["preventOverflow"] = False
            for cell in row["tableCells"]:
                cs = cell.setdefault("tableCellStyle", {})
                for side in ("paddingTop", "paddingBottom", "paddingLeft", "paddingRight"):
                    cs[side] = dict(PAD)


def widths(table_el, points):
    props = table_el["table"]["tableStyle"]["tableColumnProperties"]
    if len(points) != len(props):
        raise SystemExit("width list does not match the columns")
    for p, w in zip(props, points):
        p["widthType"] = "FIXED_WIDTH"
        p["width"] = {"magnitude": round(w, 1), "unit": "PT"}


# Advance widths of Arial in thousandths of an em; a glyph not listed counts as 556.
ARIAL = {**dict.fromkeys("0123456789abdeghnopqu", 556), **dict.fromkeys("ckvxyzJ", 500),
         **dict.fromkeys("ijl", 222), **dict.fromkeys("ft ,.;:/[]!|", 278), "r": 333, "-": 333, "(": 333,
         ")": 333, "m": 833, "w": 722, "%": 889, "&": 667, **dict.fromkeys("ABEKPSVXY", 667),
         **dict.fromkeys("CDHNRUw", 722), **dict.fromkeys("GOQ", 778), "F": 611, "T": 611, "Z": 611,
         "I": 278, "L": 556, "M": 833, "W": 944}
BOLD = 1.1
TEXT_WIDTH = 648  # landscape Letter less two 1-inch margins


def word_width(word: str, size: float, bold: bool) -> float:
    w = sum(ARIAL.get(ch, 556) for ch in word) * size / 1000
    return w * BOLD if bold else w


def tokens(text: str):
    """The pieces a line cannot break inside: words, split after a slash or a hyphen as Docs does."""
    for word in text.split():
        yield from (p for p in re.split(r"(?<=[/-])(?=[^\d])", word) if p)


def fit_widths(table_el, total=TEXT_WIDTH):
    """Column widths for 12 pt text. When every column can be as wide as its longest word or number,
    nothing breaks inside a word and the width left over is shared by the amount of text each column
    holds. When the table is too wide for that, the number columns keep their numbers whole, since a
    reader traces the figures, and the text columns share the rest with at least 60% of their longest
    word each. A last row headed Total is left out of the longest number. Returns whether everything fits."""
    t = table_el["table"]
    n = t["columns"]
    need, chars, digits, words = [0.0] * n, [0] * n, [0] * n, [0] * n
    rows = t["tableRows"]
    for r, row in enumerate(rows):
        total_row = r == len(rows) - 1 and ctext(row["tableCells"][0]) == "Total"
        for c, cell in enumerate(row["tableCells"]):
            if cell.get("tableCellStyle", {}).get("columnSpan", 1) > 1:
                continue
            for e in walk_paragraphs(cell["content"]):
                for el in e["paragraph"]["elements"]:
                    if "textRun" not in el:
                        continue
                    ts = el["textRun"].get("textStyle", {})
                    size = ts.get("fontSize", {}).get("magnitude", MIN_PT)
                    for tok in tokens(el["textRun"]["content"]):
                        words[c] += 1
                        digits[c] += any(ch.isdigit() for ch in tok)
                        if not total_row:
                            need[c] = max(need[c], word_width(tok, size, ts.get("bold", False)))
                    chars[c] += len(el["textRun"]["content"].strip())
    pad = 2 * PAD["magnitude"] + 3
    fits = sum(x + pad for x in need) <= total
    need = [min(x + pad, total * 0.4) for x in need]
    base = list(need)
    if sum(need) > total:
        numeric = [words[c] and digits[c] / words[c] > 0.5 for c in range(n)]
        avail = total - sum(need[c] for c in range(n) if numeric[c])
        others = [c for c in range(n) if not numeric[c]]
        floor = {c: 0.6 * need[c] for c in others}
        if avail <= 0 or sum(floor.values()) > avail:
            base = [x * total / sum(need) for x in need]
        else:
            share = sum(chars[c] for c in others) or 1
            for c in others:
                base[c] = floor[c] + (avail - sum(floor.values())) * chars[c] / share
    spare = total - sum(base)
    points = [b + spare * ch / (sum(chars) or 1) for b, ch in zip(base, chars)]
    t.setdefault("tableStyle", {})["tableColumnProperties"] = [{} for _ in range(n)]
    widths(table_el, points)
    return fits


# ------------------------------------------------------------------ the cuts


def risk_register(content, note_like, appendix):
    """Form 2.32, first bank: probability, impact, and score cells hold the level the scales above
    define, written H, M, or L, and an owner named with a role code keeps the code. The reason after
    each impact level goes to the appendix (reasons_table); the responses stay whole."""
    i = table_at(content, "RISK REGISTER")
    t = content[i]
    rows = t["table"]["tableRows"]
    header = [ctext(c) for c in rows[2]["tableCells"]]
    if header[:4] != ["ID", "Risk Statement", "Owner", "Probability"] or header[8:] != ["Score", "Response"]:
        raise SystemExit(f"risk register header not as expected: {header}")
    set_cell(rows[2]["tableCells"][3], "Prob.")
    sub = [ctext(c) for c in rows[3]["tableCells"]]
    if sub[4:8] != ["Scope", "Quality", "Schedule", "Cost"]:
        raise SystemExit(f"risk register impact row not as expected: {sub}")
    set_cell(rows[3]["tableCells"][5], "Qual.")
    set_cell(rows[3]["tableCells"][6], "Sched.")
    for row in rows[4:]:
        cells = row["tableCells"]
        if not re.fullmatch(r"R\d+", ctext(cells[0])):
            raise SystemExit(f"risk register row {ctext(cells[0])!r} is not a risk")
        m = OWNER.match(ctext(cells[2]))
        if m:
            set_cell(cells[2], m.group(1))
        set_cell(cells[3], LEVEL[ctext(cells[3])])
        for c in range(4, 8):
            set_cell(cells[c], LEVEL[ctext(cells[c]).split(":", 1)[0].strip()])
        a, b = ctext(cells[8]).split("-")
        set_cell(cells[8], f"{LEVEL[a]}-{LEVEL[b]}")
    content.insert(i, para("In the register, H, M, and L are the levels High, Medium, and Low of the "
                           "scales above, and Prob., Qual., and Sched. stand for Probability, Quality, "
                           "and Schedule. The reason behind each impact level is in %s with the "
                           "second bank of the form." % appendix, like=note_like))


def risk_reasons(table_el):
    """Rows of (ID, Scope, Quality, Schedule, Cost) impact texts of the first bank, before the cut."""
    out = []
    for row in table_el["table"]["tableRows"][4:]:
        cells = [ctext(c) for c in row["tableCells"]]
        out.append([cells[0]] + cells[4:8])
    return out


def reasons_table(rows, like_table):
    """A five-column table holding the impact reasons, built on the style of an existing table."""
    t = copy.deepcopy(like_table)
    proto_row = t["table"]["tableRows"][4]
    proto_cell = proto_row["tableCells"][1]
    head_cell = t["table"]["tableRows"][3]["tableCells"][4]
    new_rows = []
    for r, values in enumerate([["ID", "Scope", "Quality", "Schedule", "Cost"]] + rows):
        row = copy.deepcopy(proto_row)
        row["tableCells"] = []
        for v in values:
            cell = copy.deepcopy(head_cell if r == 0 else proto_cell)
            cell["tableCellStyle"].pop("columnSpan", None)
            cell["tableCellStyle"].pop("rowSpan", None)
            set_cell(cell, v)
            row["tableCells"].append(cell)
        row.pop("tableRowStyle", None)
        new_rows.append(row)
    new_rows[0]["tableRowStyle"] = {"tableHeader": True}
    t["table"]["tableRows"] = new_rows
    t["table"]["rows"], t["table"]["columns"] = len(new_rows), 5
    t["table"]["tableStyle"] = {"tableColumnProperties": [{} for _ in range(5)]}
    widths(t, [40, 152, 152, 152, 152])
    return t


METHOD = {"Bottom-up": "BU", "parametric rate": "PR", "three-point hours": "3P", "parametric prices": "PP",
          "allowance": "AL", "Reserve analysis [1]": "RA [1]"}


def cost_estimates(content, note_like):
    """Form 2.20: Method written as codes, Confidence Level as M or L, and the hours left out of the
    Resource cell, since Basis of Estimates gives each of them with its weighting. The width this
    frees goes to Assumptions and Basis through fit_widths."""
    i = table_at(content, "ACTIVITY COST ESTIMATES")
    t = content[i]
    rows = t["table"]["tableRows"]
    header = [ctext(c) for c in rows[2]["tableCells"]]
    if header[3:7] != ["Physical Costs", "Reserve", "Estimate", "Method"] or header[10] != "Confidence Level":
        raise SystemExit(f"activity cost estimates header not as expected: {header}")
    for c, short in ((3, "Phys. Costs"), (4, "Res."), (6, "Meth."), (10, "Conf.")):
        set_cell(rows[2]["tableCells"][c], short)
    for row in rows[3:]:
        cells = row["tableCells"]
        method = ctext(cells[6]).rstrip(".")
        if method:
            parts = [p.strip() for p in method.split(";")]
            if any(p not in METHOD for p in parts):
                raise SystemExit(f"method {method!r} has no code")
            set_cell(cells[6], "; ".join(METHOD[p] for p in parts) + ".")
        conf = ctext(cells[10])
        if conf:
            set_cell(cells[10], re.sub(r"\b(Medium|Low|High)\b", lambda m: LEVEL[m.group(1)],
                                       re.sub(r"\blow\b", "L", conf)))
        res = ctext(cells[1])
        if res.startswith("Human:"):
            set_cell(cells[1], re.sub(r" \d+(\.\d+)? h\b", "", res))
    # Eleven columns do not hold every word at 12 pt; the labor, estimate, and range figures stay
    # whole, and two physical costs and the reserve wrap.
    widths(t, [68, 62, 66, 44, 38, 66, 40, 80, 80, 68, 36])
    t["fixed_widths"] = True
    content.insert(i, para("In the form, Phys. Costs is Physical Costs, Res. is Reserve, and Meth. is "
                           "the Method, written BU bottom-up, PR parametric rate, 3P three-point hours, "
                           "PP parametric prices, AL allowance, and RA reserve analysis; Conf. is the "
                           "Confidence Level, H, M, or L for High, Medium, or Low. The hours of each "
                           "person are in Basis of Estimates.", like=note_like))


def one_section(content):
    """Keep the cover's section and the first landscape one; every later section break starts a new
    page in the same orientation, often leaving most of a page empty, so the parts run on."""
    breaks = [k for k, e in enumerate(content) if k and "sectionBreak" in e]
    flips = {bool(content[k]["sectionBreak"].get("sectionStyle", {}).get("flipPageOrientation")) for k in breaks}
    if flips != {True}:
        raise SystemExit("a later section is not landscape; section breaks kept")
    keep = breaks[0]
    content[:] = [e for k, e in enumerate(content) if not (k in breaks and k != keep)]


def cut(tab):
    dt = tab["documentTab"]
    content = dt["body"]["content"]
    named = {s["namedStyleType"]: s for s in dt.get("namedStyles", {}).get("styles", [])}
    like = content[para_at(content, "The customer owns a private")]
    app = Appendix("E")

    # The cover ends at its date line; the empty heading after it opens a blank page 2.
    first_break = next(k for k, e in enumerate(content) if k and "sectionBreak" in e)
    date = para_at(content, "Hà Nội")
    if first_break < date or any(ptext(e).strip() for e in content[date + 1:first_break]):
        raise SystemExit("the cover does not end as expected")
    del content[date + 1:first_break]

    # 1.1.5: the intro and the table of situations.
    h = heading_at(content, "1.1.5 Exception and failure behaviour")
    end = heading_at(content, "1.2 Project Deliverables", h)
    app.move(content, h + 1, end, "Exception and failure behaviour (section 1.1.5)",
             "The twelve functions above describe the system working normally. What the system must do "
             "when it does not is in {name}, in scope on the same terms as the functions.", like)

    # 1.4: the product and project exclusions.
    h = heading_at(content, "1.4 Project Exclusions")
    end = heading_at(content, "1.5 Project Constraints", h)
    app.move(content, h + 1, end, "Project exclusions (section 1.4)",
             "What the product and the project do not include is listed in {name}.", like)

    # 1.6: the assumption table.
    h = heading_at(content, "1.6 Project Assumptions")
    end = heading_at(content, "2: Project Charter", h)
    app.move(content, h + 1, end, "Project assumptions (section 1.6)",
             "Every assumed figure in this document is listed in {name}, assumptions 1 to 19. None of "
             "them is given by the assignment brief, which supplies only the budget, the duration, and "
             "the team size.", like)

    # 2.1: the charter elements the boxes of form 1.1 have no room for.
    h = heading_at(content, "2.1 Charter Elements")
    end = heading_at(content, "2.2 Project Charter", h)
    app.move(content, h + 1, end, "Charter elements (section 2.1)",
             "The charter is the form in section 2.2. The detail its boxes have no room for, the "
             "business case, the overall project risk with the risks R1 to R12 identified at "
             "chartering, the notes on the summary milestones, and the approval requirements, is in "
             "{name}.", like)

    # 3.1.1 and 3.1.2: the requirements traceability matrix; the ID families above it stay.
    h = heading_at(content, "3.1.1 Requirement information and relationship traceability")
    end = heading_at(content, "3.2 Work Breakdown Structure", h)
    app.move(content, h, end, "Requirements traceability matrix (section 3.1)",
             "The matrix, with the information and relationship traceability of every requirement, is "
             "in {name}; the inter-requirements matrix is in Appendix B.", like)

    # 3.2.1: the inputs of Create WBS and the rules the WBS is built by.
    h = heading_at(content, "3.2.1 Inputs and method")
    end = heading_at(content, "3.2.2 The structure", h)
    app.move(content, h + 1, end, "WBS inputs and method (section 3.2.1)",
             "The inputs of the WBS and the rules it is built by, top-down by major deliverable, one owner "
             "per work package, and 8 to 80 hours per work package, are in {name}.", like)

    # 3.2.4: the coverage table.
    h = heading_at(content, "3.2.4 Coverage")
    t = table_at(content, "Charter item", h)
    app.move(content, h + 1, t + 1, "Coverage of the charter by the WBS (section 3.2.4)",
             "Where the WBS delivers each function, deliverable, and milestone of the charter is in {name}.",
             like)

    # 4.1: the table under the Gantt chart.
    h = heading_at(content, "PROJECT SCHEDULE, page 1 of 2")
    t = table_at(content, "ID", h)
    app.move(content, t, t + 1, "Project schedule table, form 2.18 page 1 (section 4.1)",
             "The table of milestones, phases, and control accounts that goes with the chart below is in "
             "{name}.", like)
    # Put the line above the chart: under it, the line alone spills onto a page of its own.
    content.insert(h + 1, content.pop(t))

    # 5.1: the table of work packages the scope change request changes; its total line stays.
    h = heading_at(content, "5.1 Rules of the estimate")
    t = table_at(content, "Work package", h)
    app.move(content, t, t + 1, "Work packages deferred or made leaner (section 5.1)",
             "The hours each of these work packages keeps are in {name}.", like)

    # 5.3: page 1 of form 2.21; page 2 is already Appendix C.
    h = heading_at(content, "5.3 Cost Estimating Worksheet")
    end = para_at(content, "Page 2 of form 2.21", h)
    app.move(content, h + 1, end, "Cost estimating worksheet, form 2.21 page 1 (section 5.3)",
             "Page 1 of form 2.21, the cost estimating worksheet with its analogous and three-point "
             "estimates, is in {name}.", like)

    # 5.4 and the derivation half of 5.5.
    h = heading_at(content, "5.4 Paid time without booked work")
    end = heading_at(content, "5.5 Estimate against the charter: for the team to decide", h)
    app.move(content, h + 1, end, "Paid time without booked work (section 5.4)",
             "None is charged; the hours of each person outside booked work, and why, are in {name}.", like)
    h = heading_at(content, "5.5 Estimate against the charter: for the team to decide")
    s = para_at(content, "Where the difference comes from", h)
    end = heading_at(content, "5.6 References", h)
    app.move(content, s, end, "Estimate against the charter, the derivation (section 5.5)",
             "Where the difference comes from, what the charter funded that this estimate does not "
             "charge, and the updates proposed to other documents are in {name}.", like)

    # 5.7: the change request form.
    h = heading_at(content, "5.7 Change Request")
    end = next(k for k in range(h + 1, len(content)) if "sectionBreak" in content[k])
    app.move(content, h + 1, end, "Change request for scope and cost, form 3.3 (section 5.7)",
             "The change request that carries this estimate to the sponsor, deferring F07, F08, and F12, "
             "is in {name}.", like)

    # 7.1: the team charter.
    h = heading_at(content, "7.1 Team Charter")
    end = heading_at(content, "7.2 Resource Requirements", h)
    app.move(content, h + 1, end, "Team charter, form 2.27 (section 7.1)",
             "The team charter, with its values, meeting guidelines, communication, decision, and "
             "conflict rules, is in {name}.", like)

    # 7.3: form 2.29.
    h = heading_at(content, "7.3 Resource Breakdown Structure")
    end = next(k for k in range(h + 1, len(content)) if "sectionBreak" in content[k])
    app.move(content, h + 1, end, "Resource breakdown structure, form 2.29 (section 7.3)",
             "Form 2.29, the resource breakdown structure, is in {name}.", like)

    # 8: the second bank of the risk register, with the impact reasons of the first bank.
    first = content[table_at(content, "RISK REGISTER")]
    reasons = reasons_table(risk_reasons(first), first)
    t = table_at(content, "ID", table_at(content, "RISK REGISTER") + 1)
    name = app.move(content, t, t + 1, "Risk register, second bank, and the reasons behind the impact "
                    "levels (section 8)",
                    "The second bank of the form, with the revised probability, impact, and score, the "
                    "responsible party, the actions, and the status of each risk, is in {name}.", like)
    app.out += [para("Impact levels of the first bank, with the reason for each.", like=like), reasons,
                para("", like=like)]
    risk_register(content, like, name)

    # 9.2: form 1.4; the level definitions and the grid stay.
    t = table_at(content, "STAKEHOLDER ANALYSIS")
    end = heading_at(content, "Interest and influence grid", t)
    app.move(content, t, end, "Stakeholder analysis, form 1.4 (section 9.2)",
             "Form 1.4, with the interest, influence, and attitude of each of the twenty stakeholders, "
             "is in {name}; the grid below places them.", like)

    cost_estimates(content, like)
    one_section(content)

    # Appendices start on a new page, so the page count before them is the body.
    h = heading_at(content, APPENDICES)
    content[h]["paragraph"]["paragraphStyle"]["pageBreakBefore"] = True
    if "paragraph" not in content[-1]:
        content.append(para("", like=like))
    content += app.out
    if "paragraph" not in content[-1] or ptext(content[-1]).strip():
        content.append(para("", like=like))

    restyle(content, named)
    for e in content:
        if "table" not in e or e.pop("fixed_widths", False) or e["table"]["columns"] < 4:
            continue
        if not fit_widths(e):
            print(f"note: a table of {e['table']['columns']} columns is too narrow for its longest words")
    reindex(content, 0)
    return tab


# ------------------------------------------------------------------ commands


def cmd_plan(a):
    src = json.load(open(a.source, encoding="utf-8"))
    tab = next((t for t in merge.tab_list(src) if t["tabProperties"]["title"] == TAB), None)
    if tab is None:
        raise SystemExit(f"no tab {TAB!r} in {a.source}")
    tab = cut(copy.deepcopy(tab))
    result = merge.plan({"tabs": [tab]}, set(), {})
    pathlib.Path(a.out).write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    n = sum(len(c["requests"]) for c in result["chunks"])
    print(f"{n} requests in {len(result['chunks'])} batches; the new tab will end at {result['end']}")
    for note in result["notes"]:
        print("note:", note)


def cmd_pages(a, creds):
    from google.auth.transport.requests import AuthorizedSession
    from pypdf import PdfReader

    r = AuthorizedSession(creds).get(f"https://docs.google.com/document/d/{a.doc}/export",
                                     params={"format": "pdf", "tab": a.tab}, timeout=900)
    r.raise_for_status()
    if a.out:
        pathlib.Path(a.out).write_bytes(r.content)
    pages = PdfReader(io.BytesIO(r.content)).pages
    first = next((k for k, p in enumerate(pages) if (p.extract_text() or "").lstrip().startswith(APPENDICES)), None)
    body = first if first is not None else len(pages)
    print(f"{len(pages)} pages; body {body} (cover included), appendices {len(pages) - body}")


def cmd_check(a, creds):
    """Every text run of the written tab is Arial and at least 12 pt, counting the size and font a run
    takes from its named style."""
    doc = gdoc.docs(creds).documents().get(documentId=a.doc, includeTabsContent=True).execute()
    tab = next((t for t in merge.tab_list(doc) if t["tabProperties"]["tabId"] == a.tab), None)
    if tab is None:
        raise SystemExit(f"no tab {a.tab}")
    dt = tab["documentTab"]
    named = {s["namedStyleType"]: s.get("textStyle", {}) for s in dt.get("namedStyles", {}).get("styles", [])}
    bad, runs = [], 0
    for e in walk_paragraphs(dt["body"]["content"]):
        base = named.get(e["paragraph"]["paragraphStyle"].get("namedStyleType", "NORMAL_TEXT"), {})
        for el in e["paragraph"]["elements"]:
            if "textRun" not in el or not el["textRun"]["content"].strip():
                continue
            runs += 1
            ts = el["textRun"].get("textStyle", {})
            font = (ts.get("weightedFontFamily") or base.get("weightedFontFamily") or named["NORMAL_TEXT"].get("weightedFontFamily", {})).get("fontFamily")
            size = (ts.get("fontSize") or base.get("fontSize") or named["NORMAL_TEXT"].get("fontSize", {})).get("magnitude")
            if font != FONT or (size or 0) < MIN_PT:
                bad.append((el["startIndex"], el["endIndex"], font, size, el["textRun"]["content"][:40]))
    print(f"{runs} text runs; {len(bad)} not {FONT} at {MIN_PT} pt or more")
    for b in bad[:20]:
        print(" ", b)
    if a.fix and bad:
        # A run next to an inserted table or section break can lose the style the plan gave it.
        reqs = [{"updateTextStyle": {"range": {"startIndex": s0, "endIndex": e0, "tabId": a.tab},
                                     "textStyle": {"weightedFontFamily": {"fontFamily": FONT, "weight": 400},
                                                   "fontSize": {"magnitude": max(MIN_PT, size or 0), "unit": "PT"}},
                                     "fields": "weightedFontFamily,fontSize"}}
                for s0, e0, _font, size, _text in bad]
        gdoc.docs(creds).documents().batchUpdate(documentId=a.doc, body={"requests": reqs}).execute()
        print(f"fixed {len(reqs)} run(s)")


def cmd_delete_tab(a, creds):
    svc = gdoc.docs(creds)
    doc = svc.documents().get(documentId=a.doc, fields="tabs(tabProperties)").execute()
    titles = {t["tabProperties"]["tabId"]: t["tabProperties"]["title"] for t in merge.tab_list(doc)}
    if a.tab not in titles:
        raise SystemExit(f"no tab {a.tab}")
    if titles[a.tab] == TAB or "rút gọn" not in titles[a.tab]:
        raise SystemExit(f"tab {titles[a.tab]!r} was not written by this script; not deleted")
    svc.documents().batchUpdate(documentId=a.doc, body={"requests": [{"deleteTab": {"tabId": a.tab}}]}).execute()
    print("deleted", titles[a.tab])


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--token", default=os.path.join(DEFAULT_DIR, "token.json"))
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("plan")
    s.add_argument("--source", required=True)
    s.add_argument("--out", required=True)
    s = sub.add_parser("pages")
    s.add_argument("--doc", required=True)
    s.add_argument("--tab", required=True)
    s.add_argument("--out")
    s = sub.add_parser("check")
    s.add_argument("--doc", required=True)
    s.add_argument("--tab", required=True)
    s.add_argument("--fix", action="store_true", help="set the runs it reports to Arial at 12 pt or more")
    s = sub.add_parser("delete-tab")
    s.add_argument("--doc", required=True)
    s.add_argument("--tab", required=True)
    a = p.parse_args(argv)
    if a.cmd == "plan":
        cmd_plan(a)
        return
    creds = gdoc.load_creds(pathlib.Path(a.token))
    if a.cmd == "pages":
        cmd_pages(a, creds)
    elif a.cmd == "check":
        cmd_check(a, creds)
    else:
        cmd_delete_tab(a, creds)


if __name__ == "__main__":
    main()
