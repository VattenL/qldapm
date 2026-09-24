"""Render a generated form's Markdown into a .docx styled like the printed book.

The look comes from the book: a dark title bar with the form name in white
capitals, the Project Title and Date Prepared line under it, bordered tables,
and a "Page N of M" footer. Markdown parsing is delegated to tools/gdoc_edit.py
so there is only one Markdown subset in this repo.
"""

import argparse
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
BAR = "3F3F3F"
PAGE_HEADING = re.compile(r"^(.+?),\s*page\s+(\d+)\s+of\s+(\d+)$", re.I)


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


def write_runs(para, text, parse_inline):
    plain, styles = parse_inline(text)
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


def add_table(doc, block, parse_inline):
    rows = block["rows"]
    if not rows:
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


def render(md_path: Path, out_path: Path):
    root = find_repo_root(md_path.resolve().parent)
    sys.path.insert(0, str(root / "tools"))
    from gdoc_edit import parse_blocks, parse_inline

    blocks = parse_blocks(md_path.read_text(encoding="utf-8"))
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
            if block["level"] == 1 and not titled:
                # A generated form opens with "# 2.32 Risk Register".
                title_bar(doc, re.sub(r"^[0-9]+\.[0-9]+\s+", "", text))
                titled = True
                continue
            para = doc.add_paragraph()
            run = para.add_run(text)
            run.bold = True
            run.font.size = Pt(13 if block["level"] <= 2 else 11)
        elif kind == "table":
            add_table(doc, block, parse_inline)
        elif kind == "bullets":
            for item in block["items"]:
                write_runs(doc.add_paragraph(style="List Bullet"), item, parse_inline)
        elif kind == "numbered":
            for item in block["items"]:
                write_runs(doc.add_paragraph(style="List Number"), item, parse_inline)
        elif kind == "quote":
            write_runs(doc.add_paragraph(style="Intense Quote"), block["text"], parse_inline)
        elif kind == "hr":
            doc.add_paragraph("_" * 60)
        else:
            for line in split_key_values(block["text"]):
                write_runs(doc.add_paragraph(), line, parse_inline)

    footer(doc)
    doc.save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("markdown", type=Path)
    ap.add_argument("-o", "--out", type=Path, help="defaults to the input path with .docx")
    args = ap.parse_args()
    out = args.out or args.markdown.with_suffix(".docx")
    print(render(args.markdown, out))


if __name__ == "__main__":
    main()
