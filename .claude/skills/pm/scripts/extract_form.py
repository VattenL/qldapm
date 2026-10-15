"""Extract the printed text of a form from A Project Manager's Book of Forms.

The point of this script is fidelity. Field labels and their order come from the
PDF every time, never from memory, so a generated document cannot drift from the
printed form.
"""

import argparse
import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
INDEX = SKILL_DIR / "references" / "forms-index.md"
FIELDS_DIR = SKILL_DIR / "references" / "fields"
KNOWLEDGE_DIR = SKILL_DIR / "references" / "knowledge"
PDF_NAME = "A_Project_Managers_Book_of_Forms.pdf"

SECTION_HEADS = ("tailoring tips", "alignment", "description")


def find_pdf(explicit=None):
    if explicit:
        p = Path(explicit)
        if not p.exists():
            sys.exit(f"pdf not found: {p}")
        return p
    here = Path.cwd().resolve()
    for d in [here, *here.parents]:
        p = d / PDF_NAME
        if p.exists():
            return p
    sys.exit(f"{PDF_NAME} not found in the working directory or any parent; pass --pdf")


def load_index():
    forms = {}
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| ") or line.startswith("| ---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 7 or not re.match(r"^[0-9]\.[0-9]+$", cells[0]):
            continue
        num, name, printed, group, kind, prose, blank = cells[:7]
        forms[num] = {
            "num": num,
            "name": name,
            "printed": name if printed == "(same)" else printed,
            "group": group,
            "kind": kind,
            "prose": [int(x) for x in prose.split("-")],
            "blank": [int(x) for x in blank.split("-")],
        }
    return forms


def resolve(forms, query):
    if query in forms:
        return forms[query]
    q = query.lower().strip()
    hits = [f for f in forms.values() if q in f["name"].lower() or q in f["printed"].lower()]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        sys.exit(f"no form matches {query!r}; see references/forms-index.md")
    sys.exit(
        "several forms match {!r}:\n".format(query)
        + "\n".join(f"  {f['num']}  {f['name']}" for f in hits)
    )


def page_text(pdf, first, last):
    out = subprocess.run(
        ["pdftotext", "-f", str(first), "-l", str(last), "-layout", str(pdf), "-"],
        capture_output=True,
        text=True,
    )
    if out.returncode != 0:
        sys.exit(out.stderr.strip() or "pdftotext failed")
    return out.stdout


def slice_section(prose, wanted):
    """Return one of the prose subsections. Headings vary in case in the source."""
    lines = prose.splitlines()
    starts = {}
    for i, line in enumerate(lines):
        s = line.strip().lower()
        if s in SECTION_HEADS and s not in starts:
            starts[s] = i
    if wanted not in starts:
        return ""
    begin = starts[wanted] + 1
    later = [i for h, i in starts.items() if i > starts[wanted]]
    end = min(later) if later else len(lines)
    return "\n".join(lines[begin:end]).strip("\n")


def load_spec(num):
    """The transcribed field spec of a form, references/fields/<num>.json."""
    path = FIELDS_DIR / f"{num}.json"
    if not path.exists():
        sys.exit(f"no field spec for form {num}: {path} is missing")
    return json.loads(path.read_text(encoding="utf-8"))


def load_knowledge(num):
    """The form's knowledge file, references/knowledge/<num>.json."""
    path = KNOWLEDGE_DIR / f"{num}.json"
    if not path.exists():
        sys.exit(f"no knowledge file for form {num}: {path} is missing")
    return json.loads(path.read_text(encoding="utf-8"))


def wrap(text, indent, first=None, width=100):
    return textwrap.fill(text, width=width, initial_indent=first or indent,
                         subsequent_indent=indent, break_long_words=False,
                         break_on_hyphens=False)


def describe_knowledge(know):
    """The knowledge file as readable text: what goes in each printed field and
    what the form is connected to. Empty sections say so rather than vanish."""
    out = [wrap(f"Purpose: {know['purpose']}", "  ", first="")]
    if know["pmbok_processes"]:
        out.append("PMBOK 6 processes: " + "; ".join(know["pmbok_processes"]))
    out.append("")
    out.append(f"Fields, printed label then what goes in it ({len(know['elements'])}):")
    for el in know["elements"]:
        label = el["printed_label"] or "(not printed on the blank form)"
        named = f" [book element: {el['element']}]" if el["element"] != el["printed_label"] else ""
        out.append(f"  - {label}{named}")
        out.append(wrap(el["guidance"], "      "))
    blank_only = know.get("blank_only", [])
    if blank_only:
        out.append("")
        out.append(f"Printed on the blank form but not described by the book ({len(blank_only)}):")
        for item in blank_only:
            out.append(f"  - {item['printed_label']}")
            out.append(wrap(item["note"] + " (" + item["cite"] + ")", "      "))
    for key, title, name_key in (
        ("receives_from", "Sources, information this form receives from", "source"),
        ("provides_to", "Consumers, information this form provides to", "target"),
        ("alignment", "Alignment, must agree with", "form"),
    ):
        items = know[key]
        out.append("")
        if not items:
            out.append(f"{title}: none listed in the book")
            continue
        out.append(f"{title} ({len(items)}):")
        for item in items:
            what = item.get("what", item.get("what_must_agree", ""))
            out.append(f"  - {item[name_key]}")
            out.append(wrap(what, "      "))
    out.append("")
    if know["tailoring"]:
        out.append(f"Tailoring tips ({len(know['tailoring'])}):")
        for tip in know["tailoring"]:
            out.append(wrap(tip, "    ", first="  - "))
    else:
        out.append("Tailoring tips: none printed for this form")
    if know["agile_or_adaptive"]:
        out.append("")
        out.append("Agile or adaptive:")
        out.append(wrap(know["agile_or_adaptive"], "  "))
    out.append("")
    out.append(f"Decisions recorded here ({len(know['decisions'])}):")
    for dec in know["decisions"]:
        out.append(f"  - {dec['decision']}")
        out.append(wrap("Recorded in: " + dec["recorded_in"], "      "))
        if dec["notes"]:
            out.append(wrap(dec["notes"], "      "))
    out.append("")
    out.append(wrap("Source: " + know["citation"], "  ", first=""))
    if know["notes"]:
        out.append(wrap("Notes: " + know["notes"], "  ", first=""))
    return "\n".join(out)


def flat_columns(columns):
    """Column labels as a pipe table writes them.

    A printed group header spanning some columns becomes a "Group: Label"
    prefix on each spanned column (rendering.md, Grouped header rows). A single
    group spanning every column is the table's caption instead, so it is
    returned separately and the labels stay plain.
    """
    if len(columns) == 1 and isinstance(columns[0], dict):
        return list(columns[0]["columns"]), columns[0]["group"]
    labels = []
    for col in columns:
        if isinstance(col, dict):
            labels += [f"{col['group']}: {c}" for c in col["columns"]]
        else:
            labels.append(col)
    return labels, ""


def describe_spec(spec):
    """The printed labels of a spec, block by block, in printed order."""
    out = [f"Title block: {' | '.join(spec['title_block']) or '(none printed)'}"]
    for page in spec["pages"]:
        line = f"Page {page['page']} of {spec['page_count']} (PDF page {page['pdf_page']})"
        if "printed_title" in page:
            line += f", title bar {page['printed_title']}"
        if page.get("title_block"):
            line += ", title block printed again"
        out.append(line)
        for block in page["blocks"]:
            kind = block["type"]
            if kind == "fields":
                out.append("  fields: " + " | ".join(block["labels"]))
            elif kind == "table":
                labels, caption = flat_columns(block["columns"])
                line = f"  table, bank {block['bank']}: " + " | ".join(labels or ["(no header)"])
                if caption:
                    line += f" (caption: {caption})"
                out.append(line)
                if block["row_labels"]:
                    where = f" (in the {labels[0]} column)" if block.get("row_label_column") else ""
                    out.append(f"    row labels{where}: " + " | ".join(block["row_labels"]))
            elif kind == "checkboxes":
                out.append(f"  checkboxes, {block['label']}: " + " | ".join(block["options"]))
            elif kind == "signatures":
                out.append("  signatures: " + " | ".join(block["columns"])
                           + (" ; rows: " + " | ".join(block["rows"]) if block["rows"] else ""))
            elif kind == "text":
                out.append("  text: " + block["text"].replace("\n", " / "))
            elif kind == "picture":
                out.append("  picture: " + block["description"])
    if spec["pairs"]:
        out.append("Pairs: " + "; ".join(" + ".join(p) for p in spec["pairs"]))
    if spec["legend"]:
        sample = " (explains the book's sample; not copied)" if spec.get("legend_sample") else ""
        out.append(f"Legend{sample}: " + spec["legend"].replace("\n", " / "))
    if spec["notes"]:
        out.append("Notes: " + spec["notes"])
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        epilog="--blank, --elements, --prose, --fields and --knowledge choose what to print; with none of "
               "them the output is --blank --elements. --alignment and --tailoring add their "
               "section to that output rather than replacing it.")
    ap.add_argument("form", help="form number (2.32) or part of its name (risk register)")
    ap.add_argument("--blank", action="store_true", help="the printed blank form pages")
    ap.add_argument("--elements", action="store_true", help="the Document Element table")
    ap.add_argument("--alignment", action="store_true", help="also print the forms this one must agree with")
    ap.add_argument("--tailoring", action="store_true", help="also print the Tailoring Tips")
    ap.add_argument("--prose", action="store_true", help="the whole descriptive section")
    ap.add_argument("--fields", action="store_true",
                    help="the printed labels from references/fields/<form>.json; needs no PDF")
    ap.add_argument("--knowledge", action="store_true",
                    help="purpose, what goes in each field, sources, consumers, alignment, tailoring and "
                         "decisions from references/knowledge/<form>.json; needs no PDF")
    ap.add_argument("--pdf", help="path to the book PDF")
    args = ap.parse_args()

    form = resolve(load_index(), args.form)

    if not (args.blank or args.elements or args.prose or args.fields or args.knowledge):
        args.blank = args.elements = True

    heading = form["name"]
    if form["printed"] != form["name"]:
        heading += f" (printed as {form['printed']})"
    print(f"# {form['num']} {heading} -- {form['group']}, kind: {form['kind']}")
    print(f"# blank pages {form['blank'][0]}-{form['blank'][1]}, prose pages "
          f"{form['prose'][0]}-{form['prose'][1]} (PDF page = book page + 11)")

    if args.fields:
        print(f"\n## Field spec, references/fields/{form['num']}.json\n")
        print(describe_spec(load_spec(form["num"])))

    if args.knowledge:
        print(f"\n## Knowledge, references/knowledge/{form['num']}.json\n")
        print(describe_knowledge(load_knowledge(form["num"])))

    needs_prose = args.elements or args.alignment or args.tailoring or args.prose
    if not (needs_prose or args.blank):
        return
    pdf = find_pdf(args.pdf)
    prose = page_text(pdf, *form["prose"]) if needs_prose else ""

    if args.prose:
        print("\n## Description section\n")
        print(prose)
    else:
        for flag, key, label in (
            (args.tailoring, "tailoring tips", "Tailoring tips"),
            (args.alignment, "alignment", "Alignment"),
            (args.elements, "description", "Document elements"),
        ):
            if flag:
                print(f"\n## {label}\n")
                print(slice_section(prose, key) or "(not present for this form)")

    if args.blank:
        print("\n## Printed form\n")
        print(page_text(pdf, *form["blank"]))


if __name__ == "__main__":
    main()
