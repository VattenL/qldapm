"""Write a blank Markdown form from its transcribed field spec.

Labels, their order, grouped headers, banks, row labels and checkboxes come
from references/fields/<form>.json; the Markdown shapes follow
references/rendering.md and house-style.md. Every value is left empty, because
a blank form holds no project facts: fill it from the project documents, and
mark anything assumed with <mark>.

The default output is docs/forms/<number>-<slug>.en.md in the repo, and an
existing file is never overwritten without --force. A form the team fills again
and again (a weekly status report) gets one dated copy per use with --dated:
docs/forms/<number>-<slug>-YYYY-MM-DD.en.md.

A register table gets as many empty rows as the printed form draws, read from
the spec's notes ("The table prints 6 blank rows"), or 3 where the notes give no
count; --rows overrides it.
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

from extract_form import flat_columns, load_index, load_spec, resolve

SKILL_DIR = Path(__file__).resolve().parent.parent
PRINTED_OFFSET = 11
DEFAULT_ROWS = 3
COUNTS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
          "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15}
# "prints 6 blank rows", "eight blank rows each", "two banks of seven blank rows", "6 tall blank rows".
BLANK_ROWS = re.compile(r"\b(\d+|%s)\s+(?:tall\s+)?blank\s+rows\b" % "|".join(COUNTS), re.I)
# rendering.md, Boxes with numbered lines.
NUMBERED_LINES = ("A box printed with numbered lines holds its entries in one cell, written inline as"
                  " (1) ... (2) ...; a table keeps one row per entry.")

# rendering.md, Opening a form: 1.1 carries its title block as the first
# Field | Content table, to match docs/charter-package.en.md Part 2B.
TITLE_BLOCK_AS_TABLE = {"1.1"}

# rendering.md, chart and diagram: the Mermaid type per picture form and the
# underlying table that goes with it where the page prints no table of its own.
MERMAID = {"2.3": "gantt", "2.18": "gantt", "6.3": "gantt",
           "2.15": "flowchart LR", "2.22": "xychart-beta"}
UNDERLYING = {
    "gantt": ["Phase", "Start", "Finish"],
    "flowchart LR": ["Activity", "Predecessor", "Relationship", "Lead or Lag"],
    "xychart-beta": ["Period", "Cumulative Planned Value"],
}
MERMAID_HINT = {
    "gantt": "Draw this from the table above once the table holds real values.",
    "flowchart LR": "One node per activity in the table above; label each edge with its "
                    "relationship and any lead or lag, for example FS-2d.",
    "xychart-beta": "x-axis from the Period column, line from the Cumulative Planned Value column.",
}


def find_repo_root():
    """The skill lives at <repo>/.claude/skills/pm; fall back to the working directory."""
    for base in (SKILL_DIR.parents[2], Path.cwd().resolve()):
        for d in [base, *base.parents]:
            if (d / ".git").exists() or (d / "tools" / "gdoc_edit.py").exists():
                return d
    return Path.cwd().resolve()


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def default_path(spec, root, dated=None):
    """docs/forms/<number>-<slug>.en.md, or with -YYYY-MM-DD before .en.md for a dated copy."""
    suffix = f"-{dated.isoformat()}" if dated else ""
    return root / "docs" / "forms" / f"{spec['form'].replace('.', '-')}-{slug(spec['name'])}{suffix}.en.md"


def cell(text):
    """Escape what would break a pipe table cell or the inline parser."""
    return text.replace("|", r"\|").replace("*", r"\*")


def bold(text):
    return f"**{cell(text)}**" if text else ""


def row(cells):
    return "|" + "|".join(f" {c} " if c else " " for c in cells) + "|"


def table(header, rows):
    lines = [row(header), "| " + " | ".join("---" for _ in header) + " |"]
    return lines + [row(r) for r in rows]


def title_block_pages(spec):
    """Pages that print the title block: page 1, plus any page marked "title_block": true."""
    return {1} | {p["page"] for p in spec["pages"] if p.get("title_block")}


def page_title(spec, page):
    """The title bar a page prints; 2.7 and 2.21 page 2 print one of their own."""
    return page.get("printed_title", spec["printed_title"])


def row_label_column_printed(block):
    """Whether the first entry of columns heads the column the row labels print in.

    It does when its header is printed blank, or when the spec says so with
    "row_label_column": true (2.1 Name, 2.37 Area, 4.5 and 4.7 Process).
    Otherwise the row labels get a column of their own with a blank header, as
    rendering.md shows for 1.1 page 2.
    """
    cols = block["columns"]
    if not block["row_labels"] or not cols or not isinstance(cols[0], str):
        return False
    return cols[0] == "" or bool(block.get("row_label_column"))


def printed_rows(spec):
    """The number of blank rows the printed form draws, from its notes, or DEFAULT_ROWS.

    Where the notes give different counts for different tables (1.1 prints 7 and
    6), the largest is used, so no printed table gets fewer rows than it has.
    """
    counts = [int(c) if c.isdigit() else COUNTS[c.lower()] for c in BLANK_ROWS.findall(spec.get("notes", ""))]
    return max(counts) if counts else DEFAULT_ROWS


def title_lines(spec):
    return [f"**{label}:**" for label in spec["title_block"]]


def fields_table(labels):
    return table(["Field", "Content"], [[bold(label), ""] for label in labels])


def table_block(spec, block, rows):
    labels, caption = flat_columns(block["columns"])
    out = [bold(caption), ""] if caption else []
    if block["row_labels"]:
        if not labels:
            # 2.2 Change Control Process: printed row labels beside blank boxes, no header.
            header = ["Field", "Content"]
        elif row_label_column_printed(block):
            header = [cell(c) for c in labels]
        else:
            header = [""] + [cell(c) for c in labels]
        width = max(len(header), 2)
        header += [""] * (width - len(header))
        body = [[bold(r)] + [""] * (width - 1) for r in block["row_labels"]]
    else:
        header = [cell(c) for c in labels]
        body = [[""] * len(header) for _ in range(rows)]
    return out + table(header, body)


def signatures_block(block, rows):
    if block["rows"]:
        header = [""] + [cell(c) for c in block["columns"]]
        body = [[bold(r)] + [""] * len(block["columns"]) for r in block["rows"]]
    else:
        header = [cell(c) for c in block["columns"]]
        body = [[""] * len(header) for _ in range(rows)]
    return table(header, body)


def checkbox_block(block):
    return [bold(block["label"]), ""] + [f"- [ ] {o}" for o in block["options"]]


def outline_block(text):
    """A nested ordered list from the printed outline; depth comes from the code."""
    out = []
    for line in text.splitlines():
        m = re.match(r"^\s*((?:\d+\.)+)\s*(.*)$", line)
        if not m:
            continue
        numbers = m.group(1).rstrip(".").split(".")
        out.append("   " * (len(numbers) - 1) + f"{numbers[-1]}. {m.group(2)}")
    return out


def picture_kind(spec):
    """The Mermaid type rendering.md gives this picture form."""
    return MERMAID.get(spec["form"], "flowchart LR" if spec["kind"] == "diagram" else "gantt")


def underlying_header(spec):
    """Columns of the table rendering.md puts behind a picture on a page that prints none."""
    if any(b["type"] == "picture" for p in spec["pages"] for b in p["blocks"]
           if not any(x["type"] == "table" for x in p["blocks"])):
        return UNDERLYING[picture_kind(spec)]
    return []


def picture_block(spec, page, rows):
    kind = picture_kind(spec)
    out = []
    if not any(b["type"] == "table" for b in page["blocks"]):
        header = UNDERLYING[kind]
        out += table(header, [[""] * len(header) for _ in range(rows)]) + [""]
    out += ["```mermaid", kind]
    if kind != "flowchart LR":
        out.append(f'    title "{spec["name"]}"' if kind == "xychart-beta" else f"    title {spec['name']}")
    if kind == "gantt":
        out.append("    dateFormat YYYY-MM-DD")
    out += [f"    %% {MERMAID_HINT[kind]}", "```"]
    return out


def text_block(spec, block):
    if spec["kind"] == "outline":
        return outline_block(block["text"])
    text = block["text"]
    if spec["kind"] == "narrative" or text.rstrip().endswith("."):
        return [text]
    return [bold(text)]


def citation(spec):
    first, last = spec["pages"][0]["pdf_page"], spec["pages"][-1]["pdf_page"]
    if first == last:
        where = f"PDF page {first} (printed page {first - PRINTED_OFFSET})"
    else:
        where = (f"PDF pages {first} to {last} "
                 f"(printed pages {first - PRINTED_OFFSET} to {last - PRINTED_OFFSET})")
    text = f"Form {spec['form']}, A Project Manager's Book of Forms, 3rd edition, {where}."
    banks = max((b.get("bank", 1) for p in spec["pages"] for b in p["blocks"]), default=1)
    if banks > 1:
        text += (" The table prints in two banks, one above the other; row N of the"
                 " second table continues row N of the first.")
    if "numbered lines" in spec.get("notes", ""):
        text += " " + NUMBERED_LINES
    return f"*{text}*"


def render(spec, rows=None):
    """The blank form as Markdown text; rows defaults to the printed count."""
    rows = printed_rows(spec) if rows is None else rows
    out = [f"# {spec['form']} {spec['name']}", "", citation(spec), ""]
    multi = spec["page_count"] > 1
    with_title = title_block_pages(spec)
    for page in spec["pages"]:
        n = page["page"]
        if multi:
            out += [f"#### {page_title(spec, page)}, page {n} of {spec['page_count']}", ""]
        if n in with_title and spec["title_block"]:
            if spec["form"] in TITLE_BLOCK_AS_TABLE:
                out += fields_table(spec["title_block"]) + [""]
            else:
                out += title_lines(spec) + [""]
        for block in page["blocks"]:
            kind = block["type"]
            if kind == "fields":
                lines = fields_table(block["labels"])
            elif kind == "table":
                lines = table_block(spec, block, rows)
            elif kind == "signatures":
                lines = signatures_block(block, rows)
            elif kind == "checkboxes":
                lines = checkbox_block(block)
            elif kind == "picture":
                lines = picture_block(spec, page, rows)
            elif kind == "text":
                lines = text_block(spec, block)
            else:
                sys.exit(f"form {spec['form']}: unknown block type {kind!r}")
            out += lines + [""]
    # 2.15 prints a legend that explains the book's own sample diagram, not a key.
    if spec["legend"] and not spec.get("legend_sample"):
        for para in spec["legend"].splitlines():
            if para.strip():
                out += [para.strip(), ""]
    return "\n".join(out).rstrip("\n") + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("form", help="form number (2.32) or part of its name (risk register)")
    ap.add_argument("--out", help="output path, or - for standard output; "
                                  "default docs/forms/<number>-<slug>.en.md")
    ap.add_argument("--rows", type=int, help="empty rows per register table "
                                             "(default: the printed count, or 3 where the spec gives none)")
    ap.add_argument("--dated", nargs="?", const="today", metavar="YYYY-MM-DD",
                    help="a dated copy for a form filled repeatedly: <number>-<slug>-YYYY-MM-DD.en.md "
                         "(default today); ignored with --out")
    ap.add_argument("--force", action="store_true", help="overwrite an existing file")
    args = ap.parse_args()
    if args.rows is not None and args.rows < 1:
        sys.exit("--rows must be at least 1")
    dated = None
    if args.dated:
        try:
            dated = (datetime.date.today() if args.dated == "today"
                     else datetime.date.fromisoformat(args.dated))
        except ValueError:
            sys.exit(f"--dated takes a date as YYYY-MM-DD, not {args.dated!r}")

    form = resolve(load_index(), args.form)
    text = render(load_spec(form["num"]), args.rows)

    if args.out == "-":
        sys.stdout.write(text)
        return
    out = Path(args.out) if args.out else default_path(load_spec(form["num"]), find_repo_root(), dated)
    if out.exists() and not args.force:
        sys.exit(f"{out} exists; pass --force to overwrite it")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
