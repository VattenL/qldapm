#!/usr/bin/env python3
"""Apply the version 3.1 content of the Markdown source to the team's Google Doc copy, in place.

Every step checks a precondition on the live document and is skipped when it has
already been applied, so the script can be re-run after a failure. Tab 0 is the
report (Part 1 and the charter form), tab 1 becomes the prompt log.

Usage:
    python3 tools/apply_review_2026-09-16.py --doc ID --md docs/charter-package.en.md [--steps 1,4-6] [--dry-run]
"""

from __future__ import annotations

import argparse
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gdoc  # noqa: E402
import gdoc_edit as ge  # noqa: E402

COVER_LINE = "MÔN QUẢN LÝ DỰ ÁN PHẦN MỀM"
COVER_TITLE = "BÁO CÁO BÀI TẬP LỚN"


class Source:
    """Slices of the Markdown source, by heading."""

    def __init__(self, md: str):
        self.md = md
        s = ge.section
        self.p1 = s(md, "## Part 1", "## Part 2")
        self.p2a = s(md, "### 2A.", "### 2B.")
        self.p2b = s(md, "### 2B.", "## Part 3")
        self.p3 = s(md, "## Part 3")
        self.roles = ge.first_table(s(self.p1, "#### 1.1.3", "#### 1.1.4"))
        self.functions = ge.first_table(s(self.p1, "#### 1.1.4", "#### 1.1.5"))
        self.exceptions = ge.first_table(s(self.p1, "#### 1.1.5", "### 1.2"))
        deliv = [b for b in ge.parse_blocks(s(self.p1, "### 1.2", "### 1.3")) if b["type"] == "table"]
        self.deliverables, self.internal = deliv[0], deliv[1]
        self.internal_intro = next(b["text"] for b in ge.parse_blocks(s(self.p1, "### 1.2", "### 1.3")) if b["type"] == "para" and b["text"].startswith("The deliverables marked"))
        self.acceptance = ge.first_table(s(self.p1, "### 1.3", "### 1.4"))
        self.exclusions_md = "\n".join(l for l in s(self.p1, "### 1.4", "### 1.5").splitlines() if l.startswith("- "))
        self.constraints_md = "\n".join(l for l in s(self.p1, "### 1.5", "### 1.6").splitlines() if l.startswith("- "))
        self.assumptions = ge.first_table(s(self.p1, "### 1.6"))
        b111 = [b for b in ge.parse_blocks(s(self.p1, "#### 1.1.1", "#### 1.1.2")) if b["type"] == "para"]
        self.scope_sentence = " " + b111[0]["text"].split("sessions</mark>.", 1)[1].strip()
        self.product_paras = [b["text"] for b in ge.parse_blocks(s(self.p1, "#### 1.1.2", "#### 1.1.3")) if b["type"] == "para"]
        pg = lambda n, m: s(self.p2b, f"#### PROJECT CHARTER, page {n} of 4", f"#### PROJECT CHARTER, page {m} of 4") if m else s(self.p2b, f"#### PROJECT CHARTER, page {n} of 4")
        p1t = [b for b in ge.parse_blocks(pg(1, 2)) if b["type"] == "table"]
        self.header_fields = ge.field_map(p1t[0])
        self.page1_boxes = ge.field_map(p1t[1])
        p2 = ge.parse_blocks(pg(2, 3))
        p2t = [b for b in p2 if b["type"] == "table"]
        self.objectives, self.milestones = p2t[0], p2t[1]
        self.milestone_note = next(b["text"] for b in p2 if b["type"] == "para")
        p3t = [b for b in ge.parse_blocks(pg(3, 4)) if b["type"] == "table"]
        self.financial = ge.field_map(p3t[0])["Preapproved Financial Resources"]
        self.stakeholders = p3t[1]
        self.exit_criteria = ge.field_map(p3t[2])["Project Exit Criteria"]
        self.authority = ge.field_map(p3t[3])
        p4 = ge.parse_blocks(pg(4, None))
        p4t = [b for b in p4 if b["type"] == "table"]
        self.page4_boxes = ge.field_map(p4t[0])
        self.approvals = p4t[1]
        self.approvals_note = [b["text"] for b in p4 if b["type"] == "para" and b["text"].startswith("The printed form")]
        self.intro_2b = next(b["text"] for b in ge.parse_blocks(self.p2b) if b["type"] == "para")


def row_by_key(table_block, key):
    return next(r for r in table_block["rows"] if r[0] == key)


class Runner:
    def __init__(self, d: ge.Doc, src: Source, dry: bool):
        self.d, self.src, self.dry = d, src, dry
        self.steps = []

    def step(self, n, name):
        def deco(fn):
            self.steps.append((n, name, fn))
            return fn
        return deco

    # helpers ------------------------------------------------------------
    def para(self, tab_n, text, prefix=False, after=-1):
        content = self.d.content(tab_n)
        pred = (lambda t: t.startswith(text)) if prefix else (lambda t: t == text)
        return ge.find_para(content, pred, start_after=after)

    def table_after_heading(self, tab_n, heading):
        content = self.d.content(tab_n)
        return ge.table_after(content, self.para(tab_n, heading))

    def replace_para(self, tab_id, para_el, md_text):
        start, end = para_el["startIndex"], para_el["endIndex"] - 1
        reqs = [{"deleteContentRange": {"range": {"startIndex": start, "endIndex": end, "tabId": tab_id}}}] if end > start else []
        ins, _ = ge.insert_inline(tab_id, start, md_text)
        return reqs + ins

    def label_cell(self, tab_n, label):
        """The single cell of the 1x1 table that follows the bold label paragraph."""
        t = self.table_after_heading(tab_n, label)
        return t, ge.table_cells(t)[0][0]

    def run(self, only):
        for n, name, fn in self.steps:
            if only and n not in only:
                continue
            needed, apply = fn()
            if not needed:
                print(f"step {n:2} skip  {name}")
                continue
            if self.dry:
                print(f"step {n:2} would {name}")
                continue
            before = self.d.calls
            apply()
            print(f"step {n:2} done  {name} ({self.d.calls - before} calls)")


def build(runner: Runner):
    d, src = runner.d, runner.src
    T0 = 0

    @runner.step(1, "cover: course line below the report title")
    def s1():
        content = d.content(T0)
        mon = ge.find_para(content, lambda t: t == COVER_LINE)
        bao = ge.find_para(content, lambda t: t == COVER_TITLE)
        needed = mon["startIndex"] < bao["startIndex"]

        def apply():
            tab_id, _ = d.tab(T0)
            ins = bao["endIndex"] - 1
            d.batch([
                {"insertText": {"location": {"index": ins, "tabId": tab_id}, "text": "\n" + COVER_LINE}},
                {"updateTextStyle": {"range": {"startIndex": ins + 1, "endIndex": ins + 1 + len(COVER_LINE), "tabId": tab_id}, "textStyle": {"bold": True}, "fields": "bold"}},
                {"deleteContentRange": {"range": {"startIndex": mon["startIndex"], "endIndex": mon["endIndex"], "tabId": tab_id}}},
            ])
        return needed, apply

    @runner.step(2, "1.1.1: scope sentence")
    def s2():
        p = runner.para(T0, "The customer owns a private after-school learning center", prefix=True)
        needed = "aged 6 to 18" not in ge.para_text(p)

        def apply():
            tab_id, _ = d.tab(T0)
            ins, _n = ge.insert_inline(tab_id, p["endIndex"] - 1, src.scope_sentence)
            d.batch(ins)
        return needed, apply

    @runner.step(3, "1.1.2: product paragraphs")
    def s3():
        h = runner.para(T0, "1.1.2 The product")
        content = d.content(T0)
        paras = [el for el in ge.top_paragraphs(content) if el["startIndex"] >= h["endIndex"] and ge.para_text(el).strip()][:2]
        needed = "companion mobile app" not in ge.para_text(paras[0])

        def apply():
            tab_id, _ = d.tab(T0)
            reqs = runner.replace_para(tab_id, paras[1], src.product_paras[1]) + runner.replace_para(tab_id, paras[0], src.product_paras[0])
            d.batch(reqs)
        return needed, apply

    @runner.step(4, "1.1.3: roles table")
    def s4():
        t = runner.table_after_heading(T0, "1.1.3 Users and roles")
        cells = ge.table_cells(t)
        rows = {ge.cell_text(r[0]): r for r in cells}
        needed = "session notes" not in ge.cell_text(rows["Teacher"][2])

        def apply():
            tab_id, _ = d.tab(T0)
            reqs = []
            reqs += d.append_cell(tab_id, rows["Student / Parent"][2], "; also messages to the front desk, make-up session request, bank-transfer confirmation with reference, re-enrollment request, and the end-of-course evaluation of the course and the teacher, all from the mobile app (F12) or the web")
            reqs += d.set_cell(tab_id, rows["Accountant"][2], row_by_key(src.roles, "Accountant")[2])
            reqs += d.append_cell(tab_id, rows["Teacher"][2], "; also scores and progress comments, session notes and a per-class report, announcements and messages to parents, and the end-of-course evaluation of their classes, from the mobile app (F12) or the web")
            reqs += d.set_cell(tab_id, rows["Front-desk / Admissions staff"][2], row_by_key(src.roles, "Front-desk / Admissions staff")[2])
            reqs += d.set_cell(tab_id, rows["Academic Manager"][2], row_by_key(src.roles, "Academic Manager")[2])
            d.batch(reqs)
        return needed, apply

    @runner.step(5, "1.1.4: F08, F09, new F12")
    def s5():
        t = runner.table_after_heading(T0, "1.1.4 Functions")
        cells = ge.table_cells(t)
        needed = not any(ge.cell_text(r[0]) == "F12" for r in cells)

        def apply():
            tab_id, _ = d.tab(T0)
            rows = {ge.cell_text(r[0]): r for r in cells}
            f08, f09 = row_by_key(src.functions, "F08"), row_by_key(src.functions, "F09")
            reqs = []
            reqs += d.set_cell(tab_id, rows["F09"][3], f09[3]) + d.set_cell(tab_id, rows["F09"][1], f09[1])
            reqs += d.set_cell(tab_id, rows["F08"][3], f08[3]) + d.set_cell(tab_id, rows["F08"][1], f08[1])
            d.batch(reqs)
            t2 = runner.table_after_heading(T0, "1.1.4 Functions")
            d.insert_row_below(T0, t2, len(cells) - 1, row_by_key(src.functions, "F12"))
        return needed, apply

    @runner.step(6, "1.1.5: four exception rows")
    def s6():
        t = runner.table_after_heading(T0, "1.1.5 Exception and failure behaviour")
        needed = len(ge.table_cells(t)) == 11

        def apply():
            for row in src.exceptions["rows"][-4:]:
                t2 = runner.table_after_heading(T0, "1.1.5 Exception and failure behaviour")
                d.insert_row_below(T0, t2, len(ge.table_cells(t2)) - 1, row)
        return needed, apply

    @runner.step(7, "1.2: For column, D11, internal deliverables")
    def s7():
        t = runner.table_after_heading(T0, "1.2 Project Deliverables")
        cells = ge.table_cells(t)
        needed = ge.cell_text(cells[0][2]) != "For"

        def apply():
            tab_id, _ = d.tab(T0)
            rows = {ge.cell_text(r[0]): r for r in cells}
            reqs = d.set_cell(tab_id, rows["D10"][1], row_by_key(src.deliverables, "D10")[1]) + d.set_cell(tab_id, rows["D2"][1], row_by_key(src.deliverables, "D2")[1])
            d.batch(reqs)
            t2 = runner.table_after_heading(T0, "1.2 Project Deliverables")
            values = [r[2] for r in src.deliverables["rows"][:11]]  # header + D1..D10
            t2 = d.insert_column_before(T0, t2, 2, values)
            d.insert_row_below(T0, t2, 10, row_by_key(src.deliverables, "D11"))
            h = runner.para(T0, "1.3 Product Acceptance Criteria")
            md = src.internal_intro + "\n\n" + "\n".join("| " + " | ".join(r) + " |" if i != 1 else "| --- | --- |" for i, r in enumerate([src.internal["rows"][0], None] + src.internal["rows"][1:]))
            d.insert_markdown(T0, h["startIndex"], md + "\n")
        return needed, apply

    @runner.step(8, "1.3: A01, A02, A04, A09, new A12")
    def s8():
        t = runner.table_after_heading(T0, "1.3 Product Acceptance Criteria")
        cells = ge.table_cells(t)
        needed = not any(ge.cell_text(r[0]) == "A12" for r in cells)

        def apply():
            tab_id, _ = d.tab(T0)
            rows = {ge.cell_text(r[0]): r for r in cells}
            reqs = []
            for key in ("A09", "A04", "A02", "A01"):
                reqs += d.set_cell(tab_id, rows[key][2], row_by_key(src.acceptance, key)[2])
            d.batch(reqs)
            t2 = runner.table_after_heading(T0, "1.3 Product Acceptance Criteria")
            d.insert_row_below(T0, t2, len(cells) - 1, row_by_key(src.acceptance, "A12"))
        return needed, apply

    def bullets_between(h_start, h_end):
        content = d.content(T0)
        a, b = runner.para(T0, h_start), runner.para(T0, h_end)
        return [el for el in ge.top_paragraphs(content) if a["endIndex"] <= el["startIndex"] < b["startIndex"] and ge.para_text(el).strip()], b

    @runner.step(9, "1.4: exclusions rewritten")
    def s9():
        paras, _ = bullets_between("1.4 Project Exclusions", "1.5 Project Constraints")
        needed = not any(ge.para_text(p).startswith("Staff functions on mobile") for p in paras)

        def apply():
            tab_id, _ = d.tab(T0)
            paras2, nxt = bullets_between("1.4 Project Exclusions", "1.5 Project Constraints")
            d.delete_range(tab_id, paras2[0]["startIndex"], paras2[-1]["endIndex"])
            nxt = runner.para(T0, "1.5 Project Constraints")
            d.insert_markdown(T0, nxt["startIndex"], src.exclusions_md + "\n")
        return needed, apply

    @runner.step(10, "1.5: constraints rewritten")
    def s10():
        paras, _ = bullets_between("1.5 Project Constraints", "1.6 Project Assumptions")
        needed = not any("part-time mobile developer" in ge.para_text(p) for p in paras)

        def apply():
            tab_id, _ = d.tab(T0)
            paras2, _ = bullets_between("1.5 Project Constraints", "1.6 Project Assumptions")
            d.delete_range(tab_id, paras2[0]["startIndex"], paras2[-1]["endIndex"])
            nxt = runner.para(T0, "1.6 Project Assumptions")
            d.insert_markdown(T0, nxt["startIndex"], src.constraints_md + "\n")
        return needed, apply

    @runner.step(11, "1.6: assumption 1 and 16 to 19")
    def s11():
        t = runner.table_after_heading(T0, "1.6 Project Assumptions")
        needed = len(ge.table_cells(t)) == 16

        def apply():
            tab_id, _ = d.tab(T0)
            cells = ge.table_cells(t)
            d.batch(d.set_cell(tab_id, cells[1][1], row_by_key(src.assumptions, "1")[1]))
            for key in ("16", "17", "18", "19"):
                t2 = runner.table_after_heading(T0, "1.6 Project Assumptions")
                d.insert_row_below(T0, t2, len(ge.table_cells(t2)) - 1, row_by_key(src.assumptions, key))
        return needed, apply

    @runner.step(12, "form page 1: header fields in the printed order")
    def s12():
        date_lbl = runner.para(T0, "Date Prepared")
        sponsor_lbl = runner.para(T0, "Project Sponsor")
        needed = date_lbl["startIndex"] < sponsor_lbl["startIndex"]

        def apply():
            tab_id, _ = d.tab(T0)
            for label in ("Project Manager", "Date Prepared"):
                lbl = runner.para(T0, label)
                tbl = ge.table_after(d.content(T0), lbl)
                d.delete_range(tab_id, lbl["startIndex"], tbl["endIndex"])
            cust = runner.para(T0, "Project Customer")
            d.insert_markdown(T0, cust["startIndex"], "**Date Prepared**\n\n| 2 September 2026 |\n\n**Project Manager**\n\n| |\n")
            reqs = []
            for label, key in (("Project Customer", "Project Customer"), ("Project Sponsor", "Project Sponsor"), ("Project Title", "Project Title")):
                _t, cell = runner.label_cell(T0, label)
                reqs += d.set_cell(tab_id, cell, src.header_fields[key])
            d.batch(reqs)
        return needed, apply

    @runner.step(13, "form page 1: six boxes")
    def s13():
        _t, cell = runner.label_cell(T0, "Project Purpose")
        needed = "90,600,000" not in ge.cell_text(cell)

        def apply():
            tab_id, _ = d.tab(T0)
            reqs = []
            for label in ("Overall Project Risk", "High-Level Requirements", "Key Deliverables", "Project Boundaries", "High-Level Project Description", "Project Purpose"):
                _t, c = runner.label_cell(T0, label)
                reqs += d.set_cell(tab_id, c, src.page1_boxes[label])
            d.batch(reqs)
        return needed, apply

    @runner.step(14, "form page 2: objectives, milestones, note")
    def s14():
        h = runner.para(T0, "PROJECT CHARTER, page 2 of 4")
        content = d.content(T0)
        tables = [el for el in ge.top_tables(content) if el["startIndex"] >= h["endIndex"]][:2]
        note = next(el for el in ge.top_paragraphs(content) if el["startIndex"] >= tables[1]["endIndex"] and ge.para_text(el).strip())
        needed = "First warranty month" not in ge.cell_text(ge.table_cells(tables[1])[8][0])

        def apply():
            tab_id, _ = d.tab(T0)
            reqs = runner.replace_para(tab_id, note, src.milestone_note)
            reqs += d.fill_table(tab_id, tables[1], src.milestones["rows"], header=True)
            reqs += d.fill_table(tab_id, tables[0], src.objectives["rows"], header=True)
            d.batch(reqs)
        return needed, apply

    @runner.step(15, "form page 3: financial, stakeholders, exit criteria, authority")
    def s15():
        h = runner.para(T0, "PROJECT CHARTER, page 3 of 4")
        content = d.content(T0)
        stake = [el for el in ge.top_tables(content) if el["startIndex"] >= h["endIndex"]][1]
        needed = len(ge.table_cells(stake)) == 12

        def apply():
            tab_id, _ = d.tab(T0)
            reqs = []
            for label, key in (("Budget Management and Variance", "Budget Management and Variance"), ("Staffing Decisions", "Staffing Decisions")):
                _t, c = runner.label_cell(T0, label)
                reqs += d.set_cell(tab_id, c, src.authority[key])
            _t, c = runner.label_cell(T0, "Project Exit Criteria")
            reqs += d.set_cell(tab_id, c, src.exit_criteria)
            d.batch(reqs)
            h2 = runner.para(T0, "PROJECT CHARTER, page 3 of 4")
            stake2 = [el for el in ge.top_tables(d.content(T0)) if el["startIndex"] >= h2["endIndex"]][1]
            stake2 = d.insert_row_below(T0, stake2, 1, ["", ""])
            reqs = d.fill_table(tab_id, stake2, src.stakeholders["rows"], header=True)
            _t, c = runner.label_cell(T0, "Preapproved Financial Resources")
            reqs += d.set_cell(tab_id, c, src.financial)
            d.batch(reqs)
        return needed, apply

    @runner.step(16, "form page 4: boxes and two-column approvals")
    def s16():
        appr = ge.table_after(d.content(T0), runner.para(T0, "Approvals"))
        needed = len(ge.table_cells(appr)[0]) == 4

        def apply():
            tab_id, _ = d.tab(T0)
            reqs = []
            for label in ("Sponsor Authority", "Conflict Resolution", "Technical Decisions"):
                _t, c = runner.label_cell(T0, label)
                reqs += d.set_cell(tab_id, c, src.page4_boxes[label])
            d.batch(reqs)
            appr2 = ge.table_after(d.content(T0), runner.para(T0, "Approvals"))
            appr2 = d.delete_column(T0, appr2, 3)
            d.batch(d.fill_table(tab_id, appr2, src.approvals["rows"], header=True))
            appr3 = ge.table_after(d.content(T0), runner.para(T0, "Approvals"))
            if src.approvals_note:
                d.insert_markdown(T0, appr3["endIndex"], src.approvals_note[0] + "\n")
        return needed, apply

    @runner.step(17, "insert Part 2A before the form")
    def s17():
        content = d.content(T0)
        needed = not any(ge.para_text(el).startswith("2A. Charter elements") for el in ge.top_paragraphs(content))

        def apply():
            h = runner.para(T0, "PROJECT CHARTER")
            md = src.p2a.rstrip() + "\n\n### 2B. PROJECT CHARTER form\n\n" + src.intro_2b + "\n"
            d.insert_markdown(T0, h["startIndex"], md)
        return needed, apply

    @runner.step(18, "tab 2 becomes Part 3, the prompt log")
    def s18():
        title, tab_id, content = d.tabs()[1]
        needed = not any(ge.para_text(el).startswith("Part 3: Prompt Log") for el in ge.top_paragraphs(content))

        def apply():
            _title, tab_id2, content2 = d.tabs()[1]
            d.delete_range(tab_id2, 1, content2[-1]["endIndex"] - 1)
            d.insert_markdown(1, 1, src.p3.rstrip() + "\n")
            d.batch([{"updateDocumentTabProperties": {"tabProperties": {"tabId": tab_id2, "title": "Phần 3: Prompt Log"}, "fields": "title"}}])
        return needed, apply


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--doc", required=True)
    p.add_argument("--md", required=True)
    p.add_argument("--token", default=os.path.expanduser("~/.config/qldapm/token.json"))
    p.add_argument("--steps", help="e.g. 1,3,5-7")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    only = set()
    if a.steps:
        for part in a.steps.split(","):
            lo, _, hi = part.partition("-")
            only.update(range(int(lo), int(hi or lo) + 1))
    creds = gdoc.load_creds(pathlib.Path(a.token))
    src = Source(pathlib.Path(a.md).read_text(encoding="utf-8"))
    d = ge.Doc(gdoc.docs(creds), a.doc)
    runner = Runner(d, src, a.dry_run)
    build(runner)
    runner.run(only)
    print("total batch calls:", d.calls)


if __name__ == "__main__":
    main()
