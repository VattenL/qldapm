"""Render a generated form's Markdown into a .docx styled like the printed book.

The look comes from the book: a dark title bar with the form name in white
capitals, the Project Title and Date Prepared line under it, bordered tables,
and a "Page N of M" footer. Markdown parsing is delegated to tools/gdoc_edit.py
so there is only one Markdown subset in this repo.

The form number comes from the H1 ("# 2.10 WBS Dictionary") or from --form.
With it, references/fields/<form>.json supplies the printed title bar and the
"pairs" the printed form sets side by side: two or three labelled boxes on one
line render as one row of label and content cells, as on the page. Mermaid
blocks are skipped (the table above them carries the numbers), nested ordered
lists keep their printed outline codes, and task-list items render as boxes.
"""

import argparse
import json
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

SKILL_DIR = Path(__file__).resolve().parent.parent
FIELDS_DIR = SKILL_DIR / "references" / "fields"
BAR = "3F3F3F"
PAGE_HEADING = re.compile(r"^(.+?),\s*page\s+(\d+)\s+of\s+(\d+)$", re.I)
FORM_H1 = re.compile(r"^#\s+(\d+\.\d+)\s", re.M)
MERMAID = re.compile(r"^```mermaid[^\n]*\n.*?^```[ \t]*(?:\n|$)", re.M | re.S)
LIST_ITEM = re.compile(r"^( *)\d+\.\s+(.*)$")
TASK = re.compile(r"^\[([ xX])\]\s+(.*)$")
KEY_LINE = re.compile(r"^\*\*([^*]+?):\*\*\s*(.*)$")
# Escaped characters survive the inline parser as private-use stand-ins.
ESCAPES = {"\\*": "\ue000", "\\|": "\ue001"}
UNESCAPE = {"\ue000": "*", "\ue001": "|"}


def find_repo_root(start: Path) -> Path:
    """The skill lives at <repo>/.claude/skills/pm, so the repo is four levels up.

    Fall back to the working directory and the document's own path, which keeps
    the script usable when the skill is installed elsewhere.
    """
    candidates = [SKILL_DIR.parents[2], Path.cwd().resolve(), start]
    for base in candidates:
        for d in [base, *base.parents]:
            if (d / "tools" / "gdoc_edit.py").exists():
                return d
    sys.exit("tools/gdoc_edit.py not found; run this from inside the repo")


def shade(cell_or_para, hex_colour):
    el = OxmlElement("w:shd")
    el.set(qn("w:val"), "clear")
    el.set(qn("w:fill"), hex_colour)
    cell_or_para.append(el)


def title_bar(doc, text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.rows[0].cells[0]
    shade(cell._tc.get_or_add_tcPr(), BAR)
    para = cell.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(text.upper())
    run.bold = True
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)


def unescape(text):
    for k, v in UNESCAPE.items():
        text = text.replace(k, v)
    return text


def write_runs(para, text, parse_inline):
    plain, styles = parse_inline(text)
    plain = unescape(plain)
    if not styles:
        para.add_run(plain)
        return
    marks = [(s, e, k) for s, e, k in sorted(styles)]
    cut = sorted({0, len(plain)} | {p for s, e, _ in marks for p in (s, e)})
    for a, b in zip(cut, cut[1:]):
        if a == b:
            continue
        run = para.add_run(plain[a:b])
        active = {k for s, e, k in marks if s <= a and b <= e}
        run.bold = "bold" in active
        run.italic = "italic" in active
        if "code" in active:
            run.font.name = "Consolas"
        if "mark" in active:
            shade(run._r.get_or_add_rPr(), "FFFF00")


KEY_VALUE = re.compile(r"(?=\*\*[A-Z][^*]{0,40}:\*\*)")


def split_key_values(text):
    """The header block is a run of "**Key:** value" lines with no blank line
    between them, so the Markdown parser hands it over as one paragraph. Put the
    lines back, otherwise the .docx opens with a wall of text."""
    parts = [p.strip() for p in KEY_VALUE.split(text) if p.strip()]
    return parts if len(parts) > 1 else [text]


def form_number(md):
    m = FORM_H1.search(md)
    return m.group(1) if m else None


def load_spec(form):
    """The field spec for a form number, or None when there is none."""
    path = FIELDS_DIR / f"{form}.json" if form else None
    if path is None or not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def label_of(cell_md, parse_inline):
    return unescape(parse_inline(cell_md)[0]).strip().rstrip(":").strip()


def pair_rows(rows, pairs, parse_inline):
    """Group consecutive two-column rows whose labels are a printed pair, in order."""
    labels = [label_of(r[0], parse_inline) if r else "" for r in rows]
    groups, i = [], 0
    while i < len(rows):
        for pair in pairs:
            if len(rows[i]) == 2 and labels[i:i + len(pair)] == list(pair) \
                    and all(len(r) == 2 for r in rows[i:i + len(pair)]):
                groups.append(rows[i:i + len(pair)])
                i += len(pair)
                break
        else:
            groups.append([rows[i]])
            i += 1
    return groups


def add_paired_table(doc, groups, header, parse_inline):
    """One table row per group: label and content cells side by side.

    A row that is not part of a pair keeps its label cell and spans the rest
    of the width with its content cell.
    """
    width = 2 * max(len(g) for g in groups)
    table = doc.add_table(rows=len(groups), cols=width)
    table.style = "Table Grid"
    for r, group in enumerate(groups):
        cells = []
        for k, (label, content) in enumerate(group):
            left = table.cell(r, 2 * k)
            right = table.cell(r, 2 * k + 1)
            if k == len(group) - 1 and 2 * k + 1 < width - 1:
                right = right.merge(table.cell(r, width - 1))
            cells += [(left, label), (right, content)]
        for cell, text in cells:
            cell.text = ""
            write_runs(cell.paragraphs[0], text, parse_inline)
            if r == 0 and header:
                shade(cell._tc.get_or_add_tcPr(), "E8E8E8")
    doc.add_paragraph()


def add_table(doc, block, parse_inline, pairs=None):
    rows = block["rows"]
    if block.get("header") and rows and [label_of(c, parse_inline) for c in rows[0]] == ["Field", "Content"]:
        # rendering.md's Field | Content header is Markdown structure; the book prints none.
        rows = rows[1:]
        block = dict(block, header=False)
    if not rows:
        return
    if pairs:
        groups = pair_rows(rows, pairs, parse_inline)
        if any(len(g) > 1 for g in groups):
            add_paired_table(doc, groups, block.get("header"), parse_inline)
            return
    width = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=width)
    table.style = "Table Grid"
    for r, cells in enumerate(rows):
        for c in range(width):
            cell = table.cell(r, c)
            cell.text = ""
            text = cells[c] if c < len(cells) else ""
            write_runs(cell.paragraphs[0], text, parse_inline)
            if r == 0 and block.get("header"):
                shade(cell._tc.get_or_add_tcPr(), "E8E8E8")
    doc.add_paragraph()


def field(para, instruction):
    begin, instr, end = (OxmlElement(f"w:fld{x}") for x in ("Char", "Char", "Char"))
    begin.set(qn("w:fldCharType"), "begin")
    end.set(qn("w:fldCharType"), "end")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    run = para.add_run()._r
    for el in (begin, instr, end):
        run.append(el)


def footer(doc):
    """Word computes the page numbers, so a reflow cannot make the footer lie."""
    para = doc.sections[0].footer.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.add_run("Page ")
    field(para, " PAGE ")
    para.add_run(" of ")
    field(para, " NUMPAGES ")


def nest_ordered_lists(md):
    """Turn a nested ordered list into the fenced outline the parser keeps.

    tools/gdoc_edit.py flattens numbered items, which would lose the depth of
    an outline form (2.9 WBS, 2.29 RBS). A list with any indented item becomes
    a fenced block of printed codes ("1.1.2. Work Package"), two spaces per
    level, which the parser hands back as an outline. Flat lists are left alone.
    """
    lines, out, i, fenced = md.splitlines(), [], 0, False
    while i < len(lines):
        if lines[i].strip().startswith("```"):
            fenced = not fenced
        if fenced or not LIST_ITEM.match(lines[i]):
            out.append(lines[i])
            i += 1
            continue
        run = []
        while i < len(lines) and LIST_ITEM.match(lines[i]):
            run.append(LIST_ITEM.match(lines[i]))
            i += 1
        if not any(m.group(1) for m in run):
            out += [m.group(0) for m in run]
            continue
        out.append("```")
        indents, counters = [], []
        for m in run:
            indent = len(m.group(1))
            while indents and indent < indents[-1]:
                indents.pop()
            if not indents or indent > indents[-1]:
                indents.append(indent)
            depth = len(indents) - 1
            counters = counters[:depth + 1]
            counters += [0] * (depth + 1 - len(counters))
            counters[depth] += 1
            code = ".".join(str(n) for n in counters) + "."
            out.append("  " * depth + f"{code} {m.group(2)}")
        out.append("```")
    return "\n".join(out)


def prepare(md):
    """Markdown as the parser should see it: no Mermaid, outlines kept, escapes held."""
    md = MERMAID.sub("", md)
    md = nest_ordered_lists(md)
    for k, v in ESCAPES.items():
        md = md.replace(k, v)
    return md


def title_block_rows(text, spec):
    """The title block lines as [label, value] rows, or None if it is not one."""
    if not spec or not spec["title_block"]:
        return None
    rows = []
    for part in split_key_values(text):
        m = KEY_LINE.match(part)
        if not m or m.group(1).strip() not in spec["title_block"]:
            return None
        rows.append([f"**{m.group(1).strip()}:**", m.group(2).strip()])
    return rows


def render(md_path: Path, out_path: Path, form=None):
    root = find_repo_root(md_path.resolve().parent)
    sys.path.insert(0, str(root / "tools"))
    from gdoc_edit import parse_blocks, parse_inline

    md = md_path.read_text(encoding="utf-8")
    spec = load_spec(form or form_number(md))
    pairs = spec["pairs"] if spec else []
    blocks = parse_blocks(prepare(md))
    has_pages = any(b["type"] == "heading" and PAGE_HEADING.match(b["text"]) for b in blocks)
    doc = Document()
    pages = None
    titled = False

    for block in blocks:
        kind = block["type"]
        if kind == "heading":
            text = block["text"]
            m = PAGE_HEADING.match(text)
            if m:
                pages = m.group(3)
                if titled:
                    doc.add_page_break()
                title_bar(doc, m.group(1))
                titled = True
                continue
            if block["level"] == 1 and not titled and not has_pages:
                # A generated form opens with "# 2.32 Risk Register"; the bar
                # carries the printed title, which can differ from the name.
                title_bar(doc, spec["printed_title"] if spec
                          else re.sub(r"^[0-9]+\.[0-9]+\s+", "", text))
                titled = True
                continue
            para = doc.add_paragraph()
            run = para.add_run(text)
            run.bold = True
            run.font.size = Pt(13 if block["level"] <= 2 else 11)
        elif kind == "table":
            add_table(doc, block, parse_inline, pairs)
        elif kind == "bullets":
            for item in block["items"]:
                task = TASK.match(item)
                if task:
                    box = "\u2612 " if task.group(1) in "xX" else "\u2610 "
                    write_runs(doc.add_paragraph(), box + task.group(2), parse_inline)
                else:
                    write_runs(doc.add_paragraph(style="List Bullet"), item, parse_inline)
        elif kind == "outline":
            for depth, item in block["items"]:
                para = doc.add_paragraph()
                para.paragraph_format.left_indent = Pt(18 * depth)
                write_runs(para, item, parse_inline)
        elif kind == "numbered":
            for item in block["items"]:
                write_runs(doc.add_paragraph(style="List Number"), item, parse_inline)
        elif kind == "quote":
            write_runs(doc.add_paragraph(style="Intense Quote"), block["text"], parse_inline)
        elif kind == "hr":
            doc.add_paragraph("_" * 60)
        else:
            rows = title_block_rows(block["text"], spec)
            if rows and any(len(g) > 1 for g in pair_rows(rows, pairs, parse_inline)):
                add_table(doc, {"rows": rows, "header": False}, parse_inline, pairs)
                continue
            for line in split_key_values(block["text"]):
                write_runs(doc.add_paragraph(), line, parse_inline)

    footer(doc)
    doc.save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("markdown", type=Path)
    ap.add_argument("-o", "--out", type=Path, help="defaults to the input path with .docx")
    ap.add_argument("--form", help="form number when the H1 does not start with one, for example 1.1")
    args = ap.parse_args()
    out = args.out or args.markdown.with_suffix(".docx")
    print(render(args.markdown, out, args.form))


if __name__ == "__main__":
    main()
