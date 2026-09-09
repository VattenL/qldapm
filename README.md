# Learning Center Management Software: charter package

Coursework deliverable. Covers all four points of `requirement.md`. Document version 3.0.

The deliverable is Markdown. No PDF is produced any more.

## Layout

```
docs/charter-package.en.md    English deliverable, the document to submit
docs/charter-package.vi.md    Vietnamese version, version 2.0, no longer maintained
docs/requirements.md          General (course-wide) requirement, 3 points
requirement.md                Team requirement, the same 3 points plus the prompt log
docs/assets/style.css         Print stylesheet, only used by the retired PDF pipeline
build/                        Old HTML and PDF output, retired
build.py                      Old Markdown to HTML to PDF pipeline, retired
```

The English file is the source of truth.

## How the document answers the assignment

| Assignment point | Answered by | Source in the book |
| --- | --- | --- |
| 1. Requirement specification (short) | Part 1 | Form 2.8 Project Scope Statement, pages 58 to 59 |
| 2. Charter using the book's template | Part 2A and 2B | Table 1.1, pages 13 to 15; the form, pages 16 to 19 |
| 3. Fill in the form, empty or yellow where unknown | Part 2B | The form, pages 16 to 19 |
| 4. Prompt log with quality notes per version | Part 3 | Not from the book |

## Document structure

1. **Part 1, requirement specification.** Problem, product, seven users and roles, eleven functions
   F01 to F11 each with a description, ten exception cases in 1.1.5, ten deliverables D1 to D10,
   eleven acceptance criteria A01 to A11, exclusions, constraints, and fifteen assumptions.
2. **Part 2A, charter elements.** All fourteen elements of Table 1.1 in the book's order, including
   the quantified business case and the risk register R1 to R10.
3. **Part 2B, the PROJECT CHARTER form.** The printed four-page form reproduced field for field and
   filled in, one section per printed page.
4. **Part 3, prompt log.** Eleven prompt versions with a quality assessment of each and the reason it
   was replaced, plus the lessons the sequence shows.

## Conventions

- All customer details and figures are assumptions, listed in section 1.6 and highlighted in place.
- `<mark>` is the only HTML in the file. It renders as a yellow highlight in GitHub, IDE previews, and
  most Markdown viewers, and is used per point 3 of the assignment: it marks content whose correctness
  cannot be confirmed from the brief. The file carries 64 markers. Content given by the brief (budget,
  duration, team size) and deliberate design decisions (F01 to F11, A01 to A11) are deliberately not
  marked, because they are choices rather than guesses.
- An empty box in the Part 2B form means the field cannot be completed until signing, per the same
  instruction. Only the project manager name and the signature and date fields are empty.
- Section 2B follows the printed form field for field and in the printed order. Keep the four page
  sections and their field order if the section is edited.
- Section 1.1.5 is not decoration. A requirement list that describes only success is the normal failure
  mode of this kind of document; if a function is added to 1.1.4, add what it does when it goes wrong.
- Project writing rules from `CLAUDE.md` apply: no em dashes, no emoji.

## Verified against the book

Text was extracted directly from `A_Project_Managers_Book_of_Forms.pdf` rather than recalled.

- **Table 1.1 element list (Part 2A).** All fourteen elements of section 1.1 are present in the book's
  order: project purpose, high-level project description, project boundaries, key deliverables,
  high-level requirements, overall project risk, project objectives and related success criteria,
  summary milestone schedule, preapproved financial resources, key stakeholder list, project approval
  requirements, project exit criteria, assigned project manager with responsibility and authority
  level, name and authority of the sponsor.
- **Four-page form (Part 2B).** All 27 printed field names are present, in the printed order. Note the
  page 1 pairing: Project Sponsor with Date Prepared, and Project Manager with Project Customer.
- **Second charter template (cross-check, not a target format).** The document was also checked against
  the worked charter example in Rita Mulcahy's *PMP Exam Prep*, which is not in this repository. Part 2B
  was deliberately not rewritten into that template: the assignment names the Book of Forms form, and
  PMBOK 6 section 4.1.3.1 lists the same fourteen elements Part 2A already follows.

## Internal consistency

Checked and holding as of version 3.0:

- Budget lines 490 + 70 + 70 + 70 = 700,000,000 VND; 490,000,000 over 25 person-months = 19,600,000 each.
- Milestone payments 20 + 25 + 30 + 25 = 100%.
- 14 Sep 2026 to 5 Feb 2027 = 144 days; M6 to M7 = 31 days; every milestone falls on the weekday stated.
- Staff base 35 teachers + 17 administrative = 52; the 80% training target reconciles with the 90% and
  75% sub-targets.
- Business case: recurring benefit 104.4M a year, one-off release 360M, cumulative net by year
  -235.6, -156.2, -76.8, +2.6, so payback falls in year 4. The overdue balance is treated as a stock,
  not a flow.

## History

Version 3.0 restored two sections that version 2.1 had deleted: the filled four-page form and the
prompt log. Graded against `docs/requirements.md`, version 2.1 scored 49 out of 100, because it had
substituted the Table 1.1 element list for the prescribed form and dropped the fill-in requirement
entirely. Part 3, V10 and V11 record what happened and why.

## Vietnamese file

`docs/charter-package.vi.md` is the version 2.0 print-format translation. It still contains the `<div>`
and HTML-table constructs the English file has dropped, and it carries none of the changes from V7
onward: the form field order, the business case and its correction, the exception cases, the warranty
matrix, the customer obligations, R9 and R10, the restored form, and the V7 to V11 prompt-log entries.
It is kept for reference only. If a Vietnamese deliverable is needed, retranslate from the current
English file rather than patching it.
