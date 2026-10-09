---
name: pm
description: Generate, fill or audit project management documents from A Project Manager's Book of Forms (3rd edition), keeping printed fields in printed order. Use it whenever the user asks for any form in the book, filled or blank, such as a project charter, assumption log, stakeholder register or analysis, scope statement, WBS or WBS dictionary, requirements or traceability matrix, activity or milestone list, schedule, duration or cost estimates, cost baseline, quality, resource, communications, risk or procurement plan, risk register, report or data sheet, RACI, team charter, change request, issue, decision or change log, status, variance or earned value report, quality, risk or procurement audit, lessons learned, closeout, product vision, backlog, release plan or retrospective; also when they cite a form number such as 1.1, 2.32 or 6.4 or "the form from the book", and when they ask to check, audit or review PM documents in docs/ or answer comments on the team's Google Doc, even without naming the book.
version: 2.0.0
user-invocable: true
argument-hint: "[form number or name] [--blank] | audit <files>"
---

# Project management documents from the Book of Forms

This repo documents a project using *A Project Manager's Book of Forms*, 3rd
edition (Wiley 2017), the companion to the PMBOK Guide 6th edition. The PDF is
`A_Project_Managers_Book_of_Forms.pdf` at the repo root, and it holds 66 forms
across Initiating, Planning, Executing, Monitoring and Controlling, Closing and
Agile.

Three things make a generated form useful rather than plausible-looking:

1. **The printed form decides the fields.** Not memory. A charter with the right
   fields in the wrong order, or with an invented "Risk Appetite" box, is worse
   than useless because a reviewer has to check it against the book anyway. The
   printed labels of all 66 forms are transcribed in `references/fields/`, and
   the scripts build and check forms from that, so you never recall a field
   list.
2. **Unknown stays visibly unknown.** `CLAUDE.md` forbids guessed values. A form
   where assumptions are marked is reviewable; a form where they are hidden
   costs the team a meeting.
3. **The document agrees with itself and with its siblings.** Two review rounds
   on this project (60 findings) were almost all about this: a sponsor described
   as the owner, "R1 to R10" after R12 existed, a Cost criterion saying
   "management reserve" beside a budget line that is a contingency reserve,
   `<br>` arriving in the Doc as text. `references/review-lessons.md` is the
   list of what the team's reviewers catch.

All commands below run from the repo root. The scripts are plain Python 3;
only `md_to_docx.py` needs a package (`uv run --with python-docx`).

## Workflow for a new or filled form

### 1. Resolve which form

Look the request up in `references/forms-index.md`. It carries all 66 forms with
their PDF page ranges, the `kind` that decides the Markdown shape, and the forms
whose printed title differs from their name (2.34, 4.8, 4.9).

Requests are often broader than one form ("help me with the risk side of this").
`extract_form.py` lists candidates when a name is ambiguous. Offer the
candidates rather than picking one silently, since generating the wrong form
wastes more of the user's time than one question does.

### 2. Read the printed form

```bash
python3 .claude/skills/pm/scripts/extract_form.py 2.32 --fields                  # the transcribed spec
python3 .claude/skills/pm/scripts/extract_form.py 2.32 --alignment --tailoring   # elements, blank text, plus both sections
```

`--fields` prints the spec from `references/fields/<form>.json`: title block,
blocks per page, grouped headers, banks, row labels, side-by-side pairs, legend
and notes. It needs no PDF. Read the notes line; it records what the JSON cannot
hold (a box that prints numbered lines, a label that prints twice, sample
content that must not be copied).

The default output is the book's Document Element table (what each field is
for) plus the blank form as text. `--alignment` and `--tailoring` add those
sections; `--prose` prints the whole description.

**No Alignment section.** 2.17, 2.21 and 2.32 have none; the script prints
"(not present for this form)". Use the description instead: run `--prose` and
take the documents it says the form receives information from and provides
information to. Those are the documents to compare in step 5, and the reading
paragraph says that is where the list came from, so nobody looks for an
Alignment section that is not there.

**Pictures.** If the kind is `chart` or `diagram` (2.3, 2.15, 2.18, 2.22, 6.3),
also look at the blank pages with the Read tool (`pages` takes PDF pages).
`pdftotext` flattens a Gantt chart into unreadable columns, and seeing the page
tells you what the table behind the picture has to carry.

### 3. Gather project facts

Read `references/house-style.md` (marking rules, where facts live) and, in
`references/rendering.md`, the section for this form's kind. From
`references/review-lessons.md` read sections 1, 2, 7, 8 and 9 for every form,
and sections 3 to 6 when the form carries numbers, scope boundaries, money or
success criteria. Reading all of it for a one-page register costs time and adds
nothing.

A management plan form (2.1, 2.2, 2.4, 2.5, 2.11, 2.19, 2.23, 2.26, 2.30,
2.31, 2.37, 2.40) is the output of a PMBOK 6 planning process, and the PMBOK section
lists what the plan carries, which can be more than the form prints. Read that
chapter in `PMBOK6_and_Agile_Practice_Guide.pdf` (PDF page = printed page +
39). For quality (2.23, 2.24, 3.6), `references/pmbok-quality.md` already maps
chapter 8 onto the forms and lists where the project's quality facts live; for
another knowledge area, write the same kind of note after reading the chapter.

The facts live in `docs/charter-package.en.md` (form 1.1 in Part 2B, the ID
families, budget, risks, milestones, assumptions 1 to 19) and
`docs/scope-package.en.md` (2.7, 2.9, 2.10). Read the Markdown directly; the
helpers in `tools/gdoc_edit.py` (`section`, `first_table`,
`table_by_first_cell`, `field_map`) are optional and only cover table-shaped
parts. Ask the user for what is genuinely missing rather than filling it in;
one round of questions beats a document nobody can trust.

### 4. Scaffold, then write

Start from the scaffold rather than a blank file. It already has the printed
title block, page headings, grouped headers (`Impact: Scope`), both banks,
row labels and checkbox groups in the shapes `rendering.md` prescribes:

```bash
python3 .claude/skills/pm/scripts/new_form.py 2.32 --out -        # print it
python3 .claude/skills/pm/scripts/new_form.py 2.32                # write docs/forms/2-32-risk-register.en.md
python3 .claude/skills/pm/scripts/new_form.py 2.32 --rows 12      # register with 12 empty rows
```

Without `--out` it writes `docs/forms/<number>-<slug>.en.md` and refuses to
overwrite without `--force`, so pass `--out` for a trial run.

Then fill it, keeping to these rules (`rendering.md` has the reasons):

- Labels, headers and their order stay exactly as scaffolded. Do not rename a
  label, add a column the form does not print (no ID column on 1.3, 1.4, 2.14,
  6.4, or on bank 2 of 2.32, 2.36, 3.1), or flatten `Impact: Scope` into
  `Impact Scope`.
- The title block uses the printed labels (`**Project Title:**`, `**Date
  Prepared:**`, or `**Date:**` where that is printed); 2.3 and 2.18 print
  none. `**Project:**`, `**Date prepared:**` and `**Source:**` are not printed
  labels.
- The citation and any reading convention go in the italic paragraph above
  the form, never inside it. Nothing goes inside the form that it does not
  print: no notes under a table, no explanation under Approvals.
- Copied project text (a risk statement, a response, a milestone name) is
  copied as written, not paraphrased, so the two documents stay one ID, one
  text.
- Assumed or derived values are inside `<mark>`; unknown values are an empty
  cell (the course brief says to leave a box empty when unknown) or `[TBD]`
  where an empty cell would read as an oversight.

**A blank template** is the scaffold with nothing added: every value empty,
the italic citation paragraph kept, no project names, dates, amounts or IDs.
Keep the scaffold's empty register rows so the shape is obvious. If the user
wants the team to fill it, say where it was written and that
`check_fidelity.py` passes on it.

### 5. Check

Run the mechanical checks, then read what they cannot see.

```bash
python3 .claude/skills/pm/scripts/check_fidelity.py docs/forms/<file>.md <form>
python3 .claude/skills/pm/scripts/check_consistency.py docs/forms/<file>.md \
    docs/charter-package.en.md docs/scope-package.en.md --report docs/forms/<file>.md
python3 tools/check_scope.py        # when the scope package or anything it rolls up to changed
```

`check_fidelity.py` compares the form with `references/fields/<form>.json`:
every printed label present, spelled as printed, in printed order, and it lists
labels the form does not print. Missing or out-of-order labels exit 1; fix them.
Unprinted labels are reported only; remove each one or name it as a tailoring
in the reading paragraph. `--list <form>` prints the expected labels. For a form
inside a package, `--section "<heading text>"` checks only that part
(`--section "Part 1:"` for the 2.7 matrix in the scope package).

`check_consistency.py` judges the new form against the whole package, because
ID ranges, people and section references span files. `--report` prints only
what the new form contributes, so errors already in the sources (they have
some) do not hide whether your form is clean. It catches markup, dates, stale
ranges, dangling section references, totals, uniform columns, one ID with two
texts, sponsor and customer merged, forbidden terms and the Approvals block.
Every `range` warning is fixed or explained in your reply: it is the check that
found "R1 to R10" and "V1 to V11", and it is a warning only because a deliberate
subset that stops one or two short of the end ("F01 to F10" for a pilot, or
"F01 to F11" in a historical prompt-log entry) looks the same.

Then compare by reading. The book names, for most forms, the documents this one
must agree with (step 2). Read those that exist in `docs/` and compare the
overlapping fields. Report contradictions to the user; do not quietly pick a
winner, because a disagreement between two project documents is usually a real
decision someone has to make. The scripts cannot catch a derived number
computed from the wrong reading of an assumption, a count that disagrees with
its list, or scope that belongs to the project rather than the product; those
are in `review-lessons.md` sections 3 to 6.

### 6. Render to .docx when asked

```bash
uv run --with python-docx .claude/skills/pm/scripts/md_to_docx.py docs/forms/2-32-risk-register.en.md
```

Do this when the user asks for Word, or says the document is for submission or
printing. It draws the title bar, the printed side-by-side pairs from the spec
and the page footer. Otherwise the Markdown is the deliverable: it diffs, it
reviews, and the Doc is built from it.

### 7. Push to the Google Doc only when asked

The team's Doc is built from the Markdown and never hand-edited. Pushing needs
the user's Doc ID (an argument every time; never write it into a file) and the
OAuth client in `~/.config/qldapm/`. Audit the payload before any push
(see "Auditing the push pipeline" below), because what reaches the Doc is what
the generator emits, not what the source says.

## Citing the book

Cite the PDF page of the blank form, with the printed page in brackets: "form
2.32, PDF page 141 (printed page 130)". `forms-index.md`, `pdftotext` and the
Read tool all use PDF pages, while the book's own page numbers and the team's
older documents use printed pages; PDF page = printed page + 11. A bare "page
130" is ambiguous, because both numberings are in use and they differ by 11
pages, which is a different form. For a prose fact, cite
the prose page the same way ("section 1.1 list, PDF page 13 (printed page
2)").

## Auditing or answering a review

When the user asks to check, audit or review documents, or to answer comments
on the team's Google Doc, the job is the reviewer's, not the author's. Do not
fix while auditing unless asked: the audit is what the team decides from.

1. **Scripts first, over the whole package.** Run `check_consistency.py` over
   every file of the deliverable together, `check_fidelity.py` on each form
   (with `--section` per form inside a package), and `tools/check_scope.py` when
   the scope package is in scope. Read the line behind each finding before
   reporting it; a script finding is a lead.
2. **Walk `review-lessons.md`** section by section against the documents, all
   of it this time. Recompute every derived figure from its assumption as
   written, and count every list a number describes.
3. **Check sequence.** In a schedule, a WBS dictionary or a milestone list,
   read each work package's activities in date order and each milestone
   against the work it names. Look for anything used, reviewed, accepted or
   signed before the thing exists or finishes; a phase closed before the
   period it closes; and a date inside a period the charter rules out (a
   holiday, a freeze). These are invisible to the scripts and obvious to a
   grader.
4. **Check load per person per week** (below). A plan whose people are booked
   above their allocation is not a plan.
5. **Audit the push pipeline** when the documents are about to go to the Doc,
   or the user mentions the Doc (below).
6. **Report** in the shape of `references/audit-template.md`: Errors numbered
   E1..., then Warnings W1..., each with the location (`file:line` and the
   section or form page), the evidence quoted, and the fix or the decision it
   needs and who makes it. Write it as a Markdown file only where the user
   asks; otherwise give it in the reply.
7. **Replies to reviewer threads** follow `review-lessons.md` section 11 and go
   in the reviewer's language. `tools/gdoc.py comments --doc <id>` lists the
   threads with the text each is anchored to; `tools/gdoc.py post --doc <id>
   --review <file> --dry-run` shows what would be posted.

### Load per person per week

The charter claims an allocation per person (full time, or part time for a
window such as "joins after M2 and leaves after M5"). Spread each person's
hours over the working days of each package's window, sum by week, and compare
with that allocation. For the WBS dictionary as written:

```python
import collections, datetime, sys
sys.path.insert(0, "tools")
import check_scope, schedule
text = open("docs/scope-package.en.md", encoding="utf-8").read()
windows = schedule.parse_due_dates(text)          # {package: (start, finish)} from Due Dates
load = collections.defaultdict(float)
for sheet in check_scope.parse_sheets(text):      # activities as (resource, hours, rate, cost)
    start, finish = windows[sheet["code"]]
    days = [start + datetime.timedelta(n) for n in range((finish - start).days + 1)]
    days = [d for d in days if d.weekday() < 5]
    for res, hours, _rate, _cost in sheet["acts"]:
        for d in days:
            load[(res, d - datetime.timedelta(d.weekday()))] += hours / len(days)
for (res, week), h in sorted(load.items()):
    if h > 40:
        print(res, week, round(h, 1))
```

Use the person's own limit, not 40, for a part-time role, and check the last
dated work against the date the person is said to leave. This spreads hours
evenly, so report a week as overloaded only when it is clearly over, and say
the method in the finding. For the resource-levelled schedule, `python3
tools/level.py` prints the days anyone is booked above 8 hours and the hours by
person; compare each person's total with the hours the cost estimate prices for
that person, since the budget is hours times that person's rate.

### Auditing the push pipeline

What reaches the Doc is what the generator emits. Tab 3 of the Doc once fell
108 paragraphs behind its source because the generator dropped them, not
because anyone edited the Doc (`review-lessons.md` section 10). So audit the
payload as well as the source:

| Part of the Doc | Payload built by | Written by |
| --- | --- | --- |
| Whole document (one tab only) | `tools/gdoc.py` (Markdown to HTML) | `gdoc.py replace` or `import-html` |
| Scope baseline tab | `python3 tools/scope_tab3.py --out <scratch>/tab3.md` | `tools/gdoc_tab3.py`, `tools/gdoc_scope_sync.py` |
| Schedule tab (2.18, 3.3) | `gdoc_schedule_tab.build()` | `tools/gdoc_schedule_tab.py` |

1. Build the payload into the scratchpad without credentials:
   `python3 tools/scope_tab3.py --out <scratch>/tab3.md`;
   `python3 -c "import sys; sys.path.insert(0, 'tools'); import gdoc_schedule_tab as g; print(g.build())" > <scratch>/schedule-tab.md`;
   `python3 tools/gdoc_tab3.py --doc <id> --dry-run` or
   `python3 tools/gdoc_schedule_tab.py --doc <id> --dry-run` for the units.
2. Compare the payload's headings with the source's, and list what the
   generator drops, renames or adds. A rule, reading note or label that the
   source states and the payload drops is an error if the Doc relies on it.
3. Run `check_fidelity.py` and `check_consistency.py` on the payload too: a
   generator can add a label the printed form does not carry.
4. Check the markup against the subset `tools/gdoc_edit.py` parses (headings
   `#` to `####`, paragraphs, `- ` and `1. ` items, `> ` quotes, pipe tables,
   `---`, `**bold**`, `*italic*`, `` `code` ``, `<mark>`). Anything else
   arrives in the Doc as literal text, as `<br>` did 23 times. `gdoc.py
   replace` re-imports the whole file and collapses a multi-tab Doc to one
   tab, so it is never the way to update the team's Doc.
5. After a push, `tools/gdoc.py get --doc <id> --out <scratch>/doc.json
   --marks` lists the highlighted runs; their count should match the `<mark>`
   spans in the payload.

The Google tools need `uv run --with
google-api-python-client,google-auth-oauthlib,markdown`.

## Checks before you hand it over

- `check_fidelity.py` passes: every printed label, spelled as printed, in
  printed order, and every unprinted label it lists removed or named as a
  tailoring.
- `check_consistency.py ... --report <form>` shows no errors, and every warning
  left is one you can explain.
- No em dashes, no emoji (`CLAUDE.md`).
- Every assumed value is inside `<mark>`, every unknown is empty or `[TBD]`,
  and nothing is invented.
- Nothing appears inside the form that the printed form does not carry;
  explanations go in the italic paragraph before it, with the citation in PDF
  and printed pages.

## Files

| Path | What it is |
| --- | --- |
| `references/forms-index.md` | All 66 forms: PDF page ranges, kind, printed titles, title-block, bank and group quirks |
| `references/fields/<form>.json` | Printed labels per blank page: title block, blocks, groups, banks, row labels, pairs, legend, notes |
| `references/rendering.md` | How each kind becomes Markdown, and why |
| `references/house-style.md` | Marking rules, dates, forbidden terms, where the project's facts live |
| `references/review-lessons.md` | What the team's reviewers caught, and how to check for it |
| `references/pmbok-quality.md` | PMBOK 6 chapter 8 mapped onto forms 2.23, 2.24 and 3.6: page map, terms, where the quality facts live, traps |
| `references/audit-template.md` | Shape and rules of an audit report: errors, warnings, location, evidence, decision |
| `scripts/extract_form.py` | Form text from the PDF; `--fields` prints the spec, `--alignment`, `--tailoring`, `--prose` |
| `scripts/new_form.py` | Blank Markdown form from the spec in the rendering.md shapes; `--out`, `--rows`, `--force` |
| `scripts/check_fidelity.py` | Printed labels present and in order; `--list`, `--section` |
| `scripts/check_consistency.py` | Cross-document checks from the review findings; `--report`, `--errors-only` |
| `scripts/md_to_docx.py` | Form Markdown to a .docx that looks like the book |
| `scripts/test_*.py` | Tests: `uv run --with pytest --with python-docx pytest -q .claude/skills/pm/scripts` |
| `evals/evals.json` | Test prompts with gradable assertions |
