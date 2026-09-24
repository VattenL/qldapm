---
name: pm
description: Generate any project management document from A Project Manager's Book of Forms (3rd edition, the PMBOK Guide 6 companion) with the printed fields and field order intact. Use this whenever the user asks for a project charter, scope statement, WBS or WBS dictionary, requirements documentation or traceability matrix, stakeholder register or analysis, assumption log, issue or decision or change log, change request, risk management plan or risk register or risk report or risk data sheet, probability and impact matrix, schedule or cost or quality or resource or communications or procurement plan, activity list, milestone list, duration or cost estimates, RACI or responsibility assignment matrix, team charter, status report, variance or earned value analysis, quality or risk or procurement audit, lessons learned, project closeout, product vision, product backlog, release plan or retrospective, and whenever they mention a form number like 1.1, 2.32 or 6.4 or ask for "the form from the book". Also use it for filling, tailoring or checking the consistency of PM documents already in docs/, even when the user does not name the book.
version: 1.1.0
user-invocable: true
argument-hint: "[form number or name] [--blank]"
---

# Project management documents from the Book of Forms

This repo documents a project using *A Project Manager's Book of Forms*, 3rd
edition (Wiley 2017), the companion to the PMBOK Guide 6th edition. The PDF is
`A_Project_Managers_Book_of_Forms.pdf` at the repo root, and it holds 66 forms
across Initiating, Planning, Executing, Monitoring and Controlling, Closing and
Agile.

Two things make a generated form useful rather than plausible-looking:

1. **The printed form decides the fields.** Not memory. A charter with the right
   fields in the wrong order, or with an invented "Risk Appetite" box, is worse
   than useless because a reviewer has to check it against the book anyway.
   `scripts/extract_form.py` exists so you never have to recall a field list.
2. **Unknown stays visibly unknown.** `CLAUDE.md` forbids guessed values. A form
   where assumptions are marked is reviewable; a form where they are hidden
   costs the team a meeting.
3. **The document agrees with itself and with its siblings.** Two review rounds
   on this project (60 findings) were almost all about this: a sponsor described
   as the owner, "R1 to R10" after R12 existed, a Cost criterion saying
   "management reserve" beside a budget line that is a contingency reserve,
   `<br>` arriving in the Doc as text. `references/review-lessons.md` is the
   list of what the team's reviewers catch; read it before step 4.

## Workflow

### 1. Resolve which form

Look the request up in `references/forms-index.md`. It carries all 66 forms with
their PDF page ranges and a `kind` that decides the Markdown shape.

Requests are often broader than one form ("help me with the risk side of this").
The extractor lists candidates when a name is ambiguous. Offer the candidates
rather than picking one silently, since generating the wrong form wastes more of
the user's time than one question does.

### 2. Extract the printed form

```bash
uv run .claude/skills/pm/scripts/extract_form.py 2.32
uv run .claude/skills/pm/scripts/extract_form.py "risk register" --alignment --tailoring
```

Default output is the Document Element table (the book's own description of each
field) plus the printed blank form. Add `--alignment` for the list of other
forms this one must stay consistent with, `--tailoring` for the book's advice on
adapting it, `--prose` for the whole descriptive section.

Some forms have no Tailoring Tips or Alignment section; the script says so
rather than inventing one.

If a form is a picture (kind `chart` or `diagram`), also read the blank pages
with the Read tool. `pdftotext` flattens a Gantt chart into unreadable columns,
and seeing the page tells you what the table behind the picture has to carry.

### 3. Gather project facts

Read `references/house-style.md` and `references/review-lessons.md` before
writing anything. The first covers the marking rules and where the project's
facts live; the second covers what reviewers reject even when every field is
filled.

In short: prefer `docs/project.yaml` if it exists, otherwise parse
`docs/charter-package.en.md` with the helpers already in `tools/gdoc_edit.py`
(`section`, `first_table`, `table_by_first_cell`, `field_map`). Ask the user for
what is genuinely missing rather than filling it in; one round of questions
beats a document nobody can trust.

### 4. Write the Markdown

Follow `references/rendering.md` for the shape that matches the form's `kind`,
and `references/house-style.md` for the marking and file conventions. Write to
`docs/forms/<number>-<slug>.en.md`.

For a blank template, same steps, empty cells, no invented rows: keep two or
three empty rows in a register so the shape is obvious.

### 5. Check alignment

The book names, for most forms, the other documents this one must agree with.
Read those that exist in `docs/` and compare the overlapping fields. Report
contradictions to the user; do not quietly pick a winner, because a disagreement
between two project documents is usually a real decision someone has to make.

Then run the mechanical checks over the new form together with every document
it draws from, so ID ranges and people are judged against the whole package:

```bash
python3 .claude/skills/pm/scripts/check_consistency.py docs/forms/<file>.md docs/charter-package.en.md docs/scope-package.en.md
python3 tools/check_scope.py        # when the scope package or anything it rolls up to changed
```

The script catches markup, dates, stale ranges, dangling section references,
totals, uniform columns, the same ID with two texts, sponsor and customer
merged, and the Approvals block. It cannot catch a derived number computed from
the wrong reading of an assumption, a count that disagrees with its list, or
scope that belongs to the project rather than the product; those are in
`review-lessons.md` sections 3 to 6 and need a read.

### 6. Render to .docx when asked

```bash
uv run --with python-docx .claude/skills/pm/scripts/md_to_docx.py docs/forms/2-32-risk-register.en.md
```

Do this when the user asks for Word, or says the document is for submission or
printing. Otherwise the Markdown is the deliverable: it diffs, it reviews, and
`tools/gdoc.py` can push it to the team's Google Doc.

## Auditing or answering a review

When the user asks to check, audit or review documents, or to answer comments
on the team's Google Doc, the job is the reviewer's, not the author's:

1. Run `check_consistency.py` over the whole package and `check_fidelity.py` on
   each form it contains, and read the output critically; a warning such as
   `F01 to F05` is fine when it names an iteration.
2. Walk `review-lessons.md` section by section against the documents. Recompute
   every derived figure from its assumption as written.
3. Report in the shape of `review/2026-09-24-doc-audit.md`: **Errors** (contradicts
   another part, the brief or the book) numbered E1..., then **Warnings**
   (weak points a grader may raise) numbered W1...; each with the location,
   the evidence quoted, and the decision it needs if it is the team's call.
4. Replies to reviewer threads follow `review-lessons.md` section 11 and go in
   the reviewer's language.

Do not fix while auditing unless asked: the audit is what the team decides from.

## Checks before you hand it over

- Every printed field label appears, spelled as printed, in printed order.
  `scripts/check_fidelity.py docs/forms/<file>.md <form-number>` does this.
- No em dashes, no emoji (`CLAUDE.md`).
- Every assumed value is inside `<mark>`, every unknown is `[TBD]` or an empty
  cell, and nothing is invented.
- `scripts/check_consistency.py` reports no errors on the form plus its sources,
  and every warning left is one you can explain.
- Nothing appears inside the form that the printed form does not carry;
  explanations go in a reading-convention paragraph before it.

## Files

| Path | What it is |
| --- | --- |
| `references/forms-index.md` | All 66 forms: page ranges, kind, naming quirks |
| `references/rendering.md` | How each kind becomes Markdown |
| `references/house-style.md` | Repo conventions and the no-invention rule |
| `references/review-lessons.md` | What the team's reviewers caught, and why |
| `scripts/extract_form.py` | Printed form text straight from the PDF |
| `scripts/md_to_docx.py` | Form Markdown to a .docx that looks like the book |
| `scripts/check_fidelity.py` | Field labels present, in printed order |
| `scripts/check_consistency.py` | Cross-document checks from the review findings |
