"""Turn docs/scope-package.en.md into the payload for the third tab of the team's Doc.

The Doc is a copy of the Markdown, not a second version of it, so this module derives the tab
content rather than holding its own. It does four things the Doc needs and the repo file does not:

  - keeps the source's own front sections that are report content (the Validate Scope note, the
    reading convention, the inputs, and the decomposition method with its sizing rule) and drops the
    rest, which is guidance for a reader of the repo;
  - renumbers the headings to continue the Doc's own scheme, where Thẻ 1 carries "1: Requirement
    Specification" and "2: Project Charter";
  - rewrites the fenced WBS outline as an ```outline block, which gdoc_edit.py renders as one
    indented paragraph per line, the shape form 2.9 prints;
  - folds the inputs and the decomposition method into the WBS section, so the structure arrives
    with its method stated.

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

# Front sections of the source kept in the Doc, as (source heading, where it goes, Doc heading).
# The rest of the front matter describes the repository and is dropped.
FRONT = [
    ("### What this document is not", "lead", "#### What this section is not"),
    ("### Reading convention", "lead", "#### Reading convention"),
    ("### Inputs actually used", "method", None),
    ("### Decomposition method", "method", None),
]
METHOD_HEADING = "#### 3.2.1 Inputs and method"

STRUCTURE_HEADING = "#### 3.2.2 The structure"
WBS_PART = "## Part 2: Work Breakdown Structure"

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


def front_section(md: str, heading: str) -> str:
    """Body of one front section of the source, up to the next heading or rule."""
    m = re.search(r"^%s$" % re.escape(heading), md, re.M)
    if not m:
        raise SystemExit("front section %r not found; the source file has changed shape" % heading)
    body = md[m.end():]
    stop = re.search(r"^(#{2,3} |---$)", body, re.M)
    return unwrap_items(body[: stop.start()] if stop else body).strip()


def unwrap_items(text: str) -> str:
    """Join the hard-wrapped continuation lines of list items onto their item.

    The Doc writer reads a list item as one line; an indented continuation would otherwise become a
    separate paragraph after the list.
    """
    out = []
    for line in text.splitlines():
        if out and line.startswith("  ") and line.strip() and out[-1].lstrip().startswith("- "):
            out[-1] = out[-1].rstrip() + " " + line.strip()
        else:
            out.append(line)
    return "\n".join(out)


def outline_line(code: str, rest: str) -> str:
    """One line of the printed outline: code, element, and what it delivers, single-spaced."""
    rest = re.sub(r"\s{2,}", " ", rest).strip()
    if rest.endswith(" CA"):
        rest = rest[:-3] + " (control account)"
    return "%s%s  %s" % ("  " * code.count("."), code, rest)


def outline_block(block: str) -> str:
    """Rewrite the fenced WBS outline as an outline block for the Doc writer."""
    rows = ["```outline"]
    for raw in block.splitlines():
        m = OUTLINE_LINE.match(raw.strip())
        if m:
            rows.append(outline_line(m.group(1), m.group(2)))
    rows.append("```")
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
    body = body[: fence.start()] + outline_block(fence.group(1)) + "\n\n" + body[fence.end():]
    # The structure heading goes above the form's own header fields, which sit before the fence.
    body = body.replace(WBS_PART, WBS_PART + "\n\n" + STRUCTURE_HEADING, 1)

    body = strip_italic_notes(body)
    body = renumber(body)
    body = body.replace("### 3.2 Work Breakdown Structure",
                        "### 3.2 Work Breakdown Structure\n\n@@METHOD@@", 1)
    body = split_field_lines(body)
    lead, method = [LEAD.strip()], [METHOD_HEADING]
    for heading, where, doc_heading in FRONT:
        text = front_section(md, heading)
        (lead if where == "lead" else method).extend(([doc_heading] if doc_heading else []) + [text])
    out = "\n\n".join(lead) + "\n\n" + body
    out = out.replace("@@METHOD@@", "\n\n".join(method))
    # The report refers to its own sections, not to the repository layout.
    for old, new in (
        ("`charter-package.en.md` Part 2A and 2B", "section 2"),
        ("This document therefore", "This section therefore"),
        ("`charter-package.en.md` sections", "sections"),
        ("charter-package.en.md", "sections 1 and 2 of this report"),
        ("not in this document", "not in this report"),
        ("which is what this document covers", "which is what this section covers"),
        ("which are what this document covers", "which are what this section covers"),
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
