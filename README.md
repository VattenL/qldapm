# Learning Center Management Software — charter package

Covers all four requirements of `requirement.md`. Document version 2.0.

The deliverable is Markdown. No PDF is produced any more.

## Layout

```
docs/charter-package.en.md    English deliverable — the document to submit
docs/charter-package.vi.md    Vietnamese version, legacy print format, no longer maintained
docs/assets/style.css         Print stylesheet, only used by the retired PDF pipeline
build/                        Old HTML/PDF output, retired
build.py                      Old Markdown -> HTML -> PDF pipeline, retired
```

The English file is the source of truth. It is plain Markdown: no `<div>` wrappers, no page-break
elements, no HTML tables, no stylesheet dependency. It renders identically in GitHub, an IDE preview,
and any Markdown viewer.

## Document structure

1. **Requirement specification (short)** — product description, scope in/out, users and roles, 11 functions
   F01–F11, **14 exception requirements E01–E14**, non-functional requirements N01–N10, technical approach,
   assumptions, constraints, and **customer obligations**.
2. **Project charter** — first all fourteen elements listed in section 1.1 of *A Project Manager's Book of Forms*
   (3rd ed.), then the four-page PROJECT CHARTER form itself, filled in, one section per printed page.
3. **Prompt log** — nine prompt versions with a quality assessment of each and the reason it was replaced.

## Conventions

- All customer details and figures are assumptions, listed in section 1.8.
- `<mark>` is the only HTML kept. It renders as a yellow highlight and is used per requirement 3: it marks
  content whose correctness cannot be confirmed from the brief. Content given by the brief (budget, duration,
  team size) and deliberate design decisions (F01–F11, E01–E14, N01–N10) are deliberately *not* marked. The
  English file carries 71 markers. The convention is explained to the reader at the top of the document.
- Section 2B follows the printed form field for field and in the printed order, checked against pages 16–19 of
  `A_Project_Managers_Book_of_Forms.pdf`. Keep the four page sections and their field order if the section is edited.
- Section 1.5 (E01–E14) is not decoration. A requirement list that describes only success is the normal failure
  mode of this kind of document; if a function is added to 1.4, add what it does when it goes wrong.

## Verified against the book

- **Table 1.1 element list (section 2A).** All fourteen elements of section 1.1 of the book are present, in the
  book's order: project purpose, high-level project description, project boundaries, key deliverables,
  high-level requirements, overall project risk, project objectives and related success criteria, summary
  milestone schedule, preapproved financial resources, key stakeholder list, project approval requirements,
  project exit criteria, assigned project manager with responsibility and authority level, name and authority
  of the sponsor.
- **Four-page form (section 2B).** Compared field by field against pages 16–19. The field set matches. One
  layout error was found and fixed: the printed page 1 pairs Project Sponsor with Date Prepared and Project
  Manager with Project Customer; the document had paired Title with Date Prepared and Sponsor with Customer.
- **Second charter template (cross-check, not a target format).** The document was also checked against the
  worked charter example in Rita Mulcahy's *PMP Exam Prep* ("Customer Satisfaction Fix-It Project"), which is
  not in this repository and uses a different section list. Section 2B was deliberately **not** rewritten into
  that template: the assignment names the Book of Forms form, and PMBOK 6 §4.1.3.1 lists the same fourteen
  elements section 2A already follows. The comparison exposed two content gaps, both filled — a quantified
  **business case** and an explicit **resources preassigned** statement. Recorded as V8 of the prompt log.

## Customer review (V9)

The document was then read as the paying customer rather than as a marker. One correction and seven additions
came out of it, all recorded as V9 of the prompt log.

- **The business case arithmetic was wrong.** V8 counted the release of overdue tuition (360 million VND) as a
  *recurring annual* benefit and claimed payback in under two years. It is a stock, not a flow: cutting overdue
  tuition from 8% to 3% releases the money **once**, and only the carrying cost and the avoided write-off
  recur. Corrected: recurring benefit ≈ 104.4 million VND per year, one-off release 360 million VND, payback in
  the **fourth year** — close to nine years on recurring benefit alone. The document states the error rather
  than quietly swapping the number.
- **Section 1.5 added (E01–E14).** F01–F11 described only the happy path. The exception requirements cover
  missing, late, and wrong attendance; teacher absence; class cancellation after payment; mid-course
  withdrawal; unmatched bank transfers; overpayment and reversal; gateway failure; missing consent; disputed
  teaching-hour sheets; report disagreements; system outage; duplicate students; unreconciled migration.
- **N09 degraded operation** — paper fallback and catch-up, trained and rehearsed before go-live.
- **N10 data ownership and exit** — full export in an open format, runnable by the center itself at any time.
- **Warranty response matrix** — Critical / High / Medium with response and fix targets; an open Critical or
  High defect at the end of the warranty month blocks closeout.
- **R9 go-live failure** — branch pilot, two-week parallel run, trained paper fallback, and written rollback
  criteria the center can invoke itself. **R10 benefit not realised** — a named benefit owner, because an aged
  debt list does not collect money on its own.
- **UAT failure path** — three named options, a 2-working-day deadline, and "silence is not acceptance".
- **Customer obligations table (section 1.8)** — what the center must provide, by when, and what happens if it
  does not.
- **Scope contradiction fixed** — the exclusions previously read as if a fourth branch were out of scope, while
  the fourth branch was the stated reason for buying the system. Branches are configuration in F11; what is
  excluded is serving other companies.

## Vietnamese file

`docs/charter-package.vi.md` is the version 2.0 print-format translation. It still contains the `<div>` and
HTML-table constructs that the English file has dropped, and it carries none of the fixes made since: the form
field order, the closed audit item, the business case and its correction, E01–E14, N09–N10, the customer
obligations, R9–R10, and the V7–V9 prompt-log entries. It is kept for reference only. If a Vietnamese
deliverable is needed, retranslate from the current English file rather than patching it.
