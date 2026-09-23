"""Turn docs/scope-package.en.md into the payload for the third tab of the team's Doc.

The Doc is a copy of the Markdown, not a second version of it, so this module derives the tab
content rather than holding its own. It does four things the Doc needs and the repo file does not:

  - drops everything before Part 1, which is guidance for a reader of the repo, not report content;
  - renumbers the headings to continue the Doc's own scheme, where Thẻ 1 carries "1: Requirement
    Specification" and "2: Project Charter";
  - turns the WBS outline into a table, because the Doc writer in gdoc_edit.py has no fenced code
    block and would merge the outline into a single paragraph;
  - folds the inputs and the decomposition method into the WBS section, since the WBS arrives
    otherwise with no stated method.

Pure functions only. Nothing here talks to Google; tools/gdoc_tab3.py does that.

Usage:
    python tools/scope_tab3.py [--md docs/scope-package.en.md] [--out PATH]
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_MD = ROOT / "docs" / "scope-package.en.md"
START = "## Part 1: Requirements Traceability Matrix"

LEAD = """## 3: Scope Baseline

**Project Title:** Development and Deployment of a Learning Center Management Software

**Date Prepared:** 23 September 2026

The scope baseline of PMBOK 6 section 5.4, being the requirements traceability matrix, the work
breakdown structure, and the WBS dictionary. Each is reproduced from the form in A Project Manager's
Book of Forms, 3rd edition, field for field and in the printed field order: form 2.7 for the matrix,
form 2.9 for the structure, form 2.10 for the dictionary. It continues sections 1 and 2 and takes its
content from them: the requirement specification of section 1 and the charter of section 2.
"""

METHOD = """#### 3.2.1 Inputs and method

The inputs to Create WBS are the scope management plan, the project scope statement, and the
requirements documentation, per PMBOK 6 Figure 5-10. The project charter is not a direct input: it is
an input to Plan Scope Management, Collect Requirements, and Define Scope, and it reaches the structure
below through the scope statement those processes produce. The traceability matrix of section 3.1 is an
output of Collect Requirements, not an input here; it is updated later by Validate Scope and Control
Scope. The scope statement used is section 1 of this report, and the requirements documentation is
sections 1.1.4, 1.1.5, and 1.3 of it.

The structure is decomposed **top-down**, not assembled bottom-up: the charter fixes the deliverables D1
to D11 and the milestones M0 to M7 before any work package exists. It is organised **by life-cycle
phase**, which is one of the four arrangements the book allows on page 49, because the life cycle is
predictive with two build iterations. Level 2 is the phase, level 3 the control account, level 4 the
work package, and each work package rolls up to one and only one control account, per page 50. Every
work package names **one accountable owner**, and review and testing are work packages in their own
right rather than activities hidden inside the packages they check; no review is owned by the author of
the thing reviewed.
"""

STRUCTURE_HEADING = "#### 3.2.2 The structure"

HEADINGS = [
    ("## Part 1: Requirements Traceability Matrix", "### 3.1 Requirements Traceability Matrix"),
    ("### Requirement Information and Relationship Traceability",
     "#### 3.1.1 Requirement information and relationship traceability"),
    ("### Part 1B: Inter-Requirements Traceability Matrix",
     "#### 3.1.2 Inter-requirements traceability matrix"),
    ("## Part 2: Work Breakdown Structure", "### 3.2 Work Breakdown Structure"),
    ("### Roll-up", "#### 3.2.3 Roll-up"),
    ("### Coverage check", "#### 3.2.4 Coverage"),
    ("## Part 3: WBS Dictionary", "### 3.3 WBS Dictionary"),
]

PHASE = re.compile(r"^### (Phase 1\.\d+ .+)$")
# Work package codes are exactly four levels and always start at the project, "1". Anchoring on that
# keeps the renumbered section headings, which start at "3", out of the sheet shift.
SHEET = re.compile(r"^#### (1(?:\.\d+){3} .+)$")
OUTLINE_LINE = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.+)$")


def classify(code, rest):
    """Return (element, kind, delivers) for one line of the printed WBS outline."""
    delivers = ""
    m = re.search(r"\((.+)\)\s*$", rest)
    if m:
        delivers = m.group(1)
        rest = rest[: m.start()].rstrip()
    if rest.endswith("CA"):
        return rest[:-2].rstrip(), "Control account", delivers
    if code.count(".") == 0:
        return rest, "Project", delivers
    if "major deliverable" in delivers:
        return rest, "Major deliverable", delivers.replace("major deliverable", "").strip(" ,")
    return rest, "Work package", delivers


def outline_to_table(block: str) -> str:
    """Turn the fenced WBS outline into a pipe table the Doc writer can render."""
    rows = ["| Code | Element | Type | Delivers |", "| --- | --- | --- | --- |"]
    for raw in block.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = OUTLINE_LINE.match(line)
        if not m:
            continue
        code, rest = m.group(1), m.group(2).strip()
        element, kind, delivers = classify(code, rest)
        rows.append("| %s | %s | %s | %s |" % (code, element, kind, delivers))
    return "\n".join(rows)


def split_field_lines(text: str) -> str:
    """Put a blank line between the two form header fields.

    The Doc writer joins consecutive non-blank lines into one paragraph, which would run the Project
    Title and the Date Prepared of every sheet together.
    """
    return re.sub(r"(\*\*Project Title:\*\*[^\n]*)\n(\*\*Date Prepared:\*\*)", r"\1\n\n\2", text)


def strip_italic_notes(text: str) -> str:
    """Drop the wholly italic paragraphs.

    These are the notes naming the form and its printed page, and the Page 1 of 1 markers. They
    explain the source document to a reader of the repository; the Doc carries the form itself, so
    they are noise there. Only a paragraph that is italic from its first character to its last is
    removed, which leaves prose containing **bold** or a mid-sentence emphasis untouched.
    """
    out, buf = [], []

    def flush():
        if not buf:
            return
        joined = " ".join(line.strip() for line in buf)
        italic = (joined.startswith("*") and not joined.startswith("**")
                  and joined.endswith("*") and not joined.endswith("**"))
        if not italic:
            out.extend(buf)
        buf.clear()

    for line in text.splitlines():
        s = line.strip()
        # A heading or a table row ends the paragraph before it. The source puts "*Page 1 of 1*"
        # directly above the next heading with no blank line, so splitting on blank lines alone
        # would keep it, or take the heading with it.
        if not s or s.startswith("#") or s.startswith("|") or s.startswith("```"):
            flush()
            out.append(line)
            continue
        buf.append(line)
    flush()
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out))


def renumber(text: str) -> str:
    for old, new in HEADINGS:
        text = text.replace(old, new, 1)
    out, phase_n = [], 0
    for line in text.splitlines():
        m = PHASE.match(line)
        if m:
            phase_n += 1
            out.append("#### 3.3.%d %s" % (phase_n, m.group(1)))
            continue
        m = SHEET.match(line)
        if m:
            out.append("##### %s" % m.group(1))
            continue
        out.append(line)
    return "\n".join(out)


def build(md: str) -> str:
    if START not in md:
        raise SystemExit("%r not found; the source file has changed shape" % START)
    body = md[md.index(START):]

    fence = re.search(r"```\n(.*?)```\n", body, re.S)
    if not fence:
        raise SystemExit("WBS outline fence not found")
    body = body[: fence.start()] + STRUCTURE_HEADING + "\n\n" + outline_to_table(fence.group(1)) \
        + "\n" + body[fence.end():]

    body = strip_italic_notes(body)
    body = renumber(body)
    body = body.replace("### 3.2 Work Breakdown Structure",
                        "### 3.2 Work Breakdown Structure\n\n@@METHOD@@", 1)
    body = split_field_lines(body)
    out = LEAD + "\n" + body
    out = out.replace("@@METHOD@@", METHOD.strip())
    # The report refers to its own sections, not to the repository layout.
    for old, new in (
        ("`charter-package.en.md` sections", "sections"),
        ("charter-package.en.md", "sections 1 and 2 of this report"),
        ("is not in this document", "is not in this report"),
        ("which is what this document covers", "which is what this section covers"),
    ):
        out = out.replace(old, new)
    # Headings were renumbered above, so any "Part N" left is a cross-reference in body text.
    # It is matched across a line break because the source is hard-wrapped.
    out = re.sub(r"\bPart 1B\b", "section 3.1.2", out)
    out = re.sub(r"\bPart(\s+)([123])\b", lambda m: "section%s3.%s" % (m.group(1), m.group(2)), out)
    if re.search(r"\bPart [123]", out):
        raise SystemExit("unconverted cross-reference to a repo Part heading")
    return out.rstrip() + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--md", default=str(DEFAULT_MD))
    p.add_argument("--out", default="")
    a = p.parse_args(argv)
    payload = build(pathlib.Path(a.md).read_text(encoding="utf-8"))
    if a.out:
        pathlib.Path(a.out).write_text(payload, encoding="utf-8")
        print("%s: %d lines, %d characters" % (a.out, payload.count("\n"), len(payload)))
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
