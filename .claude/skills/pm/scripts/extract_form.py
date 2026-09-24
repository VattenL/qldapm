"""Extract the printed text of a form from A Project Manager's Book of Forms.

The point of this script is fidelity. Field labels and their order come from the
PDF every time, never from memory, so a generated document cannot drift from the
printed form.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
INDEX = SKILL_DIR / "references" / "forms-index.md"
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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("form", help="form number (2.32) or part of its name (risk register)")
    ap.add_argument("--blank", action="store_true", help="the printed blank form pages")
    ap.add_argument("--elements", action="store_true", help="the Document Element table")
    ap.add_argument("--alignment", action="store_true", help="forms this one must agree with")
    ap.add_argument("--tailoring", action="store_true", help="the Tailoring Tips")
    ap.add_argument("--prose", action="store_true", help="the whole descriptive section")
    ap.add_argument("--pdf", help="path to the book PDF")
    args = ap.parse_args()

    pdf = find_pdf(args.pdf)
    form = resolve(load_index(), args.form)

    asked = args.blank or args.elements or args.alignment or args.tailoring or args.prose
    if not asked:
        args.blank = args.elements = True

    heading = form["name"]
    if form["printed"] != form["name"]:
        heading += f" (printed as {form['printed']})"
    print(f"# {form['num']} {heading} -- {form['group']}, kind: {form['kind']}")
    print(f"# blank pages {form['blank'][0]}-{form['blank'][1]}, prose pages "
          f"{form['prose'][0]}-{form['prose'][1]} (PDF page = book page + 11)")

    prose = page_text(pdf, *form["prose"]) if (
        args.elements or args.alignment or args.tailoring or args.prose) else ""

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
