# Turning a printed form into Markdown

The printed forms are boxes on paper. Markdown has no boxes, so each `kind` in
`forms-index.md` has a settled shape. Follow it so that every document in
`docs/forms/` reads the same way and so `md_to_docx.py` can render it back into
something that looks like the book.

## Where the labels come from

`references/fields/<form>.json` is the authority for what a form prints. It was
transcribed once from the blank pages and holds, per form:

- `title_block`: the labels printed under the title bar, in printed reading
  order (left then right, top to bottom). Empty for 2.3 and 2.18.
- `pages[]`: one entry per printed page. `"title_block": true` marks a later
  page that prints the title block again (2.7, 2.21 and 2.31 page 2), and
  `printed_title` a page whose title bar differs from the form's (2.7 page 2
  INTER-REQUIREMENTS TRACEABILITY MATRIX, 2.21 page 2 BOTTOM-UP COST
  ESTIMATING WORKSHEET).
- `pages[].blocks`: each printed block in order. A `fields` block lists box
  labels; a `table` block lists its `columns`, where an entry
  `{"group": "Impact", "columns": [...]}` is a printed header spanning those
  columns, and `bank` numbers the strips of one register printed one above the
  other; `row_labels` are printed row headings, and `"row_label_column": true`
  says they print inside the first listed column (2.1 Name, 2.37 Area, 4.5 and
  4.7 Process) rather than in an unheaded column of their own; a `text` block is
  either a printed heading with no box of its own (1.1 Approvals, 2.2
  Definitions of Change) or a printed sentence (it ends with a full stop);
  `signatures` and `picture` blocks speak for themselves.
- `pairs`: labels the printed form sets side by side on one line, the title
  block included.
- `legend`: printed text under the form; `"legend_sample": true` marks one that
  explains the book's own sample (2.15) and is not copied.
- `notes`: what the JSON cannot hold (a bank with no ID column, sample content
  that must not be copied, how a box is drawn).

Copy labels, grouped headers, banks and pairs from that file, never from memory
or from the prose pages. Where the prose table (Table 2.29 and the like) words
an element differently from the blank form, the blank form wins.
`scripts/new_form.py <form>` scaffolds a blank Markdown form from it following
this file, and `scripts/check_fidelity.py` checks a finished form against it.

## Opening a form

```markdown
# 2.32 Risk Register

*Form 2.32, A Project Manager's Book of Forms, 3rd edition, PDF page 141
(printed page 130). <reading convention, if the form needs one>*

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 24 September 2026

<body>
```

The title block is the form's own first line, so it uses the printed labels,
exactly as `title_block` gives them, one `**Label:** value` line each, with no
blank line between them. The labels vary and are not interchangeable:

- most forms print `Project Title` and `Date Prepared`;
- 2.4, 2.5, 2.11, 2.33, 2.37 and 2.38 print `Date`, so write `**Date:**`;
- 6.3 prints `Project Name` and no date, so write `**Project Name:**` only;
- 2.3 and 2.18 print no title block at all (`title_block` is empty), so write
  none;
- some forms print more on the same lines (1.1 adds Project Sponsor, Project
  Manager and Project Customer; 3.6, 4.5 and 4.7 add Project Auditor and Audit
  Date). Write every one, in `title_block` order. 1.1 is the exception in
  shape: `docs/charter-package.en.md` Part 2B carries its five title-block
  labels as the first `Field | Content` table, and a regenerated 1.1 matches
  that.

Do not write `**Project:**`, `**Date prepared:**` or `**Source:**` in a form;
those are not printed labels. The bold key/value block under the H1 of
`docs/charter-package.en.md` (`**Project:**`, `**Budget:**`, `**Date
prepared:**` and so on) is that package's own metadata, not a form, which is
why its labels differ; `house-style.md` (File layout) gives the same rule. A
generated form follows it too: the three bold lines `tools/schedule.py` writes
at the top of 2.18, which prints no title block, are a finding against the
generator.

The citation is not part of the form. It goes in the italic paragraph above the
title block, together with any reading convention, and cites the PDF page of
the blank form with the printed page in brackets. Do not write it as a bold
`**Source:**` line: it would sit among the printed labels and read as one.

Multi-page forms keep the page boundary, because the book's page count is part
of the form's identity and `tools/gdoc.py` inserts a Google Doc page break on
exactly this heading shape:

```markdown
#### RISK REPORT, page 2 of 4
```

On a multi-page form the title block goes under the `page 1 of N` heading, and
again under any later page heading whose printed page repeats it (2.7, 2.21
and 2.31 page 2 do; the spec marks them `"title_block": true`). A page with its
own title bar uses it in the heading:
`#### INTER-REQUIREMENTS TRACEABILITY MATRIX, page 2 of 2`.

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
Due Dates). Reading order for a pair is left then right. The pairing is layout:
`md_to_docx.py` applies it when it renders the .docx, from the `pairs` list in
`references/fields/<form>.json`. Do not write a pair as a two-column row in the
Markdown, and do not invent a pair the form does not print.
`tools/gdoc_form.py` does not pair fields; it draws title bars, group header
rows passed to it explicitly, column widths and landscape pages in the Google
Doc.

A cell holds one paragraph. `<br>` does not survive the push to the Google Doc
(it arrived as literal text 23 times), and Markdown cannot put a list in a
cell, so a list inside a cell is written inline: `(1) ... (2) ... (3) ...`.

**Boxes with numbered lines.** Some boxes print numbered lines (4.2's three
accomplishment boxes print 1 to 6, 1 to 4 and 1 to 4; 4.1, 2.10 Milestones,
2.27 and 2.37 do the same; the spec's notes say which). The box stays one
cell and its entries are written inline, `(1) ... (2) ...`, as many as there
are entries, which may be more or fewer than the printed lines. A blank form
leaves the cell empty: no `(1) (2) (3)` placeholders, since a placeholder is a
value. `new_form.py` adds one sentence saying this to the italic paragraph of
every form whose notes mention numbered lines. Where the numbered lines are
the rows of a table (2.26), the table keeps one row per entry.

**A printed box with a one-word heading cell.** Where the form prints a box
whose top cell is a label and whose body is one blank cell (4.1 and 4.2 print
`Risk:` under New Risks Identified and `Issue:` under Issues), the box is a
one-column table headed with that label, and each entry is a row. A blank form
gives it the printed row count from the spec's notes, or 3 where the notes
give none, so the shape is visible; the bold line above it is the printed
heading.

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

The blank first header cell is the column the row labels sit in. Where the
printed form heads that column itself (`row_label_column` in the spec), use the
printed header instead of a blank one, so 2.1 is `| Name | Comment |` with
`| **Scope** | |` beneath it. Where it prints row labels beside blank boxes and
no header at all (2.2 Change Control Process), write the rows as a
`Field | Content` table.

A printed heading that has no box of its own is a bold line on its own, and
the boxes under it follow as usual; a printed instruction sentence is plain
text:

```markdown
**Definitions of Change**

| Field | Content |
| --- | --- |
| **Schedule change** | |

Attach relevant forms used in the change control process.
```

The `Field | Content` header row is Markdown structure, not a printed label:
`check_fidelity.py` ignores it and `md_to_docx.py` does not draw it.

Checkbox lists (form 3.6 Quality Audit, 3.3 Change Request) become task list
items, one per printed box, in printed order, under the group's printed label
as a bold line (the colon is optional). A plain-text label is not found by
`check_fidelity.py`:

```markdown
**Area Audited**

- [ ] Project processes
- [x] Project documents
```

Nothing goes inside the form that the printed form does not print: no note
under the milestone table, no explanation under Approvals, no extra title
heading. Put the explanation in a short italic paragraph before the form's
first page heading. Signature blocks copy the printed columns exactly; for 1.1
that is two, Project Manager and Sponsor or Originator.

## Grouped header rows

Some tables print a header that spans several columns above the column labels:
2.32 prints Impact over Scope, Quality, Schedule and Cost in both banks; 2.36
prints Impact in bank 1 and Revised Impact in bank 2; 2.7 page 1 prints
Requirement Information over ID to Category and Relationship Traceability over
Business Objective to Validation; 2.10 prints Labor over Hours, Rate, Total and
Material over Units, Cost, Total. A pipe table has exactly one header row, so
the two printed rows cannot both be header rows.

Write each spanned column as `Group: Label`, with the group exactly as printed,
a colon and one space, and the column label exactly as printed. Columns the
group does not span keep their plain label:

```markdown
| ID | Risk Statement | Owner | Probability | Impact: Scope | Impact: Quality | Impact: Schedule | Impact: Cost | Score | Response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

Why this and not a printed group row: a group row placed as the header with the
column labels as the first body row turns the labels into a record, so every
parser in this repo (`tools/gdoc_edit.py`, `check_consistency.py`, the ID
comparison) reads the wrong header; and plain child labels alone leave four
columns called `Scope`, `Quality`, `Schedule`, `Cost` whose meaning depends on
a row the Markdown does not have (in 2.10 the label `Total` would appear twice,
once under Labor and once under Material). The prefix keeps every column
self-describing, and it is a fixed string that `check_fidelity.py` builds from
the `group` entries in
`references/fields/<form>.json` and matches cell for cell. Do not write
`Impact Scope`, `Impact - Scope` or `Scope (Impact)`; and do not add a group the
form does not print.

A group that spans every column of its table is not a grouped header but the
table's caption (2.17 and 2.21 page 1: Parametric, Analogous and Three-Point
Estimates). The same holds for a `text` block printed directly above a table
(2.23 Quality Objectives and the two headings after it, 2.26). Write the caption as
a bold line directly above that table, `**Parametric Estimates**`, and keep the
column labels plain.

`docs/scope-package.en.md` Part 1 writes the 2.7 header with plain labels and
names the two groups in its italic caption, and `tools/gdoc_tab3.py` draws the
group row in the Google Doc through `gdoc_form.apply_form(..., groups=...)`.
That rendering predates this rule; a new form follows the rule.

## `log`

A register. One column per printed column, in printed order, one row per
record.

If the printed form has an ID column (`ID`, `Issue ID`, `WBS ID`), fill it
with the repo's scheme where one exists: `R1`-`R12` for risks, `A01`-`A12` for
acceptance criteria, `F01`-`F12` for functions, `D1`-`D11` for deliverables,
`M0`-`M7` for milestones, BR/FR/NFR for requirements. Assumptions are numbered
1 to 19 without a letter, so the ID column of 1.2 Assumption Log holds `1` to
`19`; `A01` is an acceptance criterion, never an assumption.

**Source data with no printed column.** A source sometimes carries a column
the form does not print, such as the charter's Type (Product or Project) on
its risk register. Do not add the column. Put the value in the nearest printed
free-text field of the same record (Comments on 2.32 and 3.1), written the same
way in every row (`Charter type: Product.`), and say once in the italic
paragraph where it went. If the form has no free-text field, name the source
column in the italic paragraph and leave the data in the source.

**One source column for two printed ones.** 2.32 prints Response in bank 1
and Actions in bank 2; the charter has one Response column. Copy the source's
response verbatim into Response and do not split it, because one ID, one text
matters more than the split. Actions takes only what a document states as
actions for that risk (the work packages the scope package's coverage check
assigns to the response, cited as such); otherwise it is empty. Status is
`Open`, plain, for every risk no document records as closed (see
`house-style.md`, Judgement columns), and the italic paragraph says why, which
also answers the uniform-column check.

If the printed form has no ID column, do not add one. 1.3 Stakeholder Register
starts with Name, 1.4 Stakeholder Analysis with Name or Role, 2.14 Milestone
List with Milestone, 6.4 Retrospective with Start. The first printed column is
the key, and an added ID column is a field the form does not print. Where a
record already has a repo ID, it may lead the text of the first printed column
(`M1 Requirement specification approved and baselined` in 2.14's Milestone
column).

Wide registers print their columns in two banks on one page, one strip above
the other: 2.32 Risk Register (ten columns in each bank), 2.36 Risk Data Sheet
(one risk, one row per bank) and 3.1 Issue Log. Keep both banks, as two tables
under one heading, in printed order. Bank 2 of these forms prints no ID column,
so do not add one there either: bank 2 holds the same records in the same order
and the same number of rows as bank 1, so row N of bank 2 continues row N of
bank 1, which is how the printed page reads. Splitting is better than a
20-column table nobody can read, and it matches how the page is printed. If a
reviewer asks for the ID repeated in bank 2, that is a tailoring: do it, and
say so once in the italic paragraph before the form.

## What the Doc pipeline parses

`tools/gdoc_edit.py` (`parse_blocks`, `parse_inline`), which every Doc writer
in `tools/` goes through, understands: headings `#` to `#####` (a `######`
heading is a paragraph of literal hashes); paragraphs; `- ` bullets and `1. `
numbered items, one level only, since indentation is dropped; `> ` quotes;
pipe tables; `---`; fenced blocks, each line a paragraph indented by its
leading spaces (the WBS outline goes through this); and inline `**bold**`,
`*italic*`, `` `code` `` and `<mark>`. Anything else, `<br>` and other HTML,
entities, images in Markdown syntax, nested list indentation, arrives as
literal text or loses its structure. `tools/gdoc_schedule_tab.py` replaces
each chart with an `@@IMAGE <file>@@` line that it later swaps for the image.

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
   relationship types; periods with cumulative planned value. Where the page
   prints a table of its own (2.18 ID, WBS, Task Name, Start, Finish; 6.3 the
   Sprint by Team grid), that table is the underlying one. Where it prints
   none, the columns are `Phase | Start | Finish` (2.3),
   `Activity | Predecessor | Relationship | Lead or Lag` (2.15) and
   `Period | Cumulative Planned Value` (2.22); `check_fidelity.py` does not
   report those as unprinted.
2. A Mermaid block rendering it (`gantt` for roadmaps and schedules, `flowchart
   LR` for the network diagram, `xychart-beta` for the cost baseline S-curve).

Printed headings over a picture stay as bold lines above its table (2.3
**Life Cycle Phases** and **Timeline**); a caption on the book's sample (2.18
Sample Gantt Chart) does not.

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
