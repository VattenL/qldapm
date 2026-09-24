# Turning a printed form into Markdown

The printed forms are boxes on paper. Markdown has no boxes, so each `kind` in
`forms-index.md` has a settled shape. Follow it so that every document in
`docs/forms/` reads the same way and so `md_to_docx.py` can render it back into
something that looks like the book.

Every form, whatever its kind, opens the same way, because every printed form
carries the title bar and the Project Title / Date Prepared line:

```markdown
# 2.32 Risk Register

**Project:** Development and Deployment of a Learning Center Management Software
**Date prepared:** 24 September 2026
**Source:** A Project Manager's Book of Forms, 3rd edition, form 2.32, page 128

<body>
```

Multi-page forms keep the page boundary, because the book's page count is part
of the form's identity and `tools/gdoc.py` inserts a Google Doc page break on
exactly this heading shape:

```markdown
#### RISK REPORT, page 2 of 4
```

## `fields`

Labelled boxes become a two-column table. The label goes in bold in the left
column, exactly as printed, in printed order.

```markdown
| Field | Content |
| --- | --- |
| **Project Purpose** | Replace the paper enrolment process ... |
| **High-Level Project Description** | |
```

The vertical table keeps printed reading order even where the printed form sets
two fields side by side (1.1 page 1 pairs Project Sponsor with Date Prepared and
Project Manager with Project Customer; 2.10 pairs Work Package Name with Code of
Accounts, Description of Work with Assumptions and Constraints, Milestones with
Due Dates). The pairing is layout, and it is applied at render time by
`tools/gdoc_form.py` and `md_to_docx.py`. Reading order for a pair is left then
right.

A cell holds one paragraph. `<br>` does not survive the push to the Google Doc
(it arrived as literal text 23 times), and Markdown cannot put a list in a
cell, so a list inside a cell is written inline: `(1) ... (2) ... (3) ...`.

Only content is highlighted. `<mark>` never wraps a bold label or a heading.

An empty right cell means the value is genuinely not known yet. That is a real
state in this repo, not an oversight, and the charter uses it for the project
manager's name because the sponsor appoints the PM at M0.

Where the printed form pairs two labelled columns under one heading, keep the
printed header row rather than flattening it:

```markdown
| | Project Objectives | Success Criteria |
| --- | --- | --- |
| **Scope** | | |
```

Checkbox lists (form 3.6 Quality Audit, 3.3 Change Request) become task list
items, one per printed box, in printed order:

```markdown
- [ ] Project processes
- [x] Project documents
```

Nothing goes inside the form that the printed form does not print: no note
under the milestone table, no explanation under Approvals, no extra title
heading. Put the explanation in a short italic paragraph before the form's
first page heading. Signature blocks copy the printed columns exactly; for 1.1
that is two, Project Manager and Sponsor or Originator.

## `log`

A register. One column per printed column, one row per record. Give every row a
stable ID in the first column and reuse the repo's ID schemes where one already
exists (`R1`-`R12` for risks, `A01`-`A12` for assumptions, `F01`-`F12` for
functions, `D1`-`D11` for deliverables, `M0`-`M7` for milestones).

Wide registers such as 2.32 Risk Register print their columns across two banks
on one page. Keep both banks, as two tables under one heading, in printed order,
sharing the ID column. Splitting them is better than a 14-column table nobody
can read, and it matches how the page is actually printed.

## `matrix`

A grid. First column carries the row labels, header row carries the column
labels, both copied from the printed form.

```markdown
| | Person 1 | Person 2 | Person 3 |
| --- | --- | --- | --- |
| **Work package 1** | R | C | A |
```

Keep the printed legend below the grid (for 2.25 that is the R / C / A / I
definitions) because the grid is meaningless without it.

## `outline`

A numbered decomposition (2.9 WBS, 2.29 RBS). Use a nested ordered list, not a
table: the printed form is an indented outline, and a Code | Element | Type
table was rejected as a different form. Number in the order the work happens,
and never append a late package at the end of a branch out of sequence:

```markdown
1. Learning Center Management Software
   1. Requirements
      1. Stakeholder interviews
      2. Requirement specification
```

## `chart` and `diagram`

These four forms are pictures: 2.3 Project Roadmap, 2.18 Project Schedule,
2.22 Cost Baseline, 6.3 Release Plan, plus 2.15 Network Diagram. A picture is
not the deliverable, the information behind it is, so emit **both**:

1. The underlying table, which is what anyone will actually read and edit:
   phases with start and finish dates; activities with predecessors and
   relationship types; periods with cumulative planned value.
2. A Mermaid block rendering it (`gantt` for roadmaps and schedules, `flowchart
   LR` for the network diagram, `xychart-beta` for the cost baseline S-curve).

`md_to_docx.py` renders the table and skips the Mermaid block, which is the
right trade: a Word file with the real numbers beats a Word file with a broken
picture.

For 2.15, name the relationship type on each edge (`FS`, `SS`, `FF`, `SF`) and
any lead or lag (`FS-2d`, `FS+3d`), because those are the whole point of the
form.

## `narrative`

Form 6.1 Product Vision is a sentence template. Reproduce the printed sentence
stems verbatim as body text and fill the blanks; do not restructure it into a
table, because the phrasing is the form.
