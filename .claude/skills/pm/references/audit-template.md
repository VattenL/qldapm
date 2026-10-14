# Audit report template

Use this shape for any audit or review of the project documents: the source
Markdown in `docs/`, a generated form, or the payload about to be pushed to the
team's Google Doc. The team decides from the report, so every finding has to be
checkable by someone who did not do the audit: where it is, what the text says,
and what would settle it.

When the user wants the audit as a file, it goes in `review/` at the repo root
as `review/YYYY-MM-DD-<topic>.md` (for example
`review/2026-09-24-doc-audit.md`), which is where the earlier audits are and
what `review-lessons.md` cites. Otherwise it is the reply.

## Shape

```markdown
# Audit of <what was audited>, <date in full, 1 October 2026>

Audited: <files, with version or commit if known; the Doc and its tabs if the
payload was audited too>.

Standard: *A Project Manager's Book of Forms*, 3rd edition, form <n> <name>
(PDF pages <a> to <b>, printed pages <a-11> to <b-11>), ... Both ranges are in
`references/forms-index.md` (Blank pages and Printed blank). Field lists come
from `references/fields/<form>.json` and `check_fidelity.py`, not memory.

Method: <scripts run and their totals, for example "check_consistency.py over
the package with --report on the new form: 0 errors, 1 warning, 24 findings
already in the sources not shown"; what was read by hand; what was recomputed>.

## Errors

Each contradicts another part of the package, the brief, the charter, or the
printed form.

**E1. <One sentence that states the defect, not the topic.>**
- Where: `docs/charter-package.en.md:<line>` (Part 2A business case; form 1.1 page 1)
- Evidence: "<quoted text>" against "<quoted text>" at `<file>:<line>`
- Needs: <the fix>, or <the decision, the options, and who decides>

## Warnings

Weak points a grader or reviewer may raise. None contradicts another part.

**W1. ...**

## Comment threads

<Only when the Doc's threads were in scope: thread id, the reviewer's point,
whether the source now answers it, and the reply proposed.>

## What passed

<The checks that found nothing, so the reader knows they were run: totals that
add up, labels in printed order, ranges current, dates in one style.>
```

## Rules for findings

- **Error or warning.** An error is a contradiction a reader can show with two
  quotations, or a quotation against the printed form or the brief. A warning
  is a judgement: weak, ambiguous, unexplained, or likely to draw a comment.
  When in doubt, make it a warning and say what would make it an error.
- **One finding, one defect.** State the defect in the bold line ("The business
  case applies 70% activation to all guardians, not to the 80% with a
  smartphone"), not the area ("Business case"). Several occurrences of one
  defect are one finding with every location listed.
- **Location.** `file:line`, plus the section, sheet code or form page, so it
  can be found in both the Markdown and the Doc. For the Doc, name the tab and
  the heading the text sits under.
- **A payload has no file in the repo.** A payload exists only in memory or in
  the scratchpad, so cite what rebuilds it and where in it: the generator and
  its function, the payload heading, and the source line the text came from,
  for example "`tools/gdoc_schedule_tab.py` `build()`, payload heading
  `4.1 Project Schedule`, from `docs/forms/2-18-project-schedule.en.md:5`".
  Give a scratch line number only together with the command that rebuilds the
  file.
- **A generated form is fixed at its generator.** When the file says it is
  generated (2.18 by `tools/schedule.py`, the Doc tabs by the `tools/gdoc_*`
  writers), the Needs line names the generator or the source document to
  change, never the generated file, since a hand edit is lost on the next run.
  Say whether the committed file is current: regenerate it into the scratchpad
  (`SKILL.md`, Auditing a generated form) and compare.
- **Evidence is quoted.** Copy the words, figures and dates as written. A
  derived figure shows the arithmetic from the assumption as written (for
  example "80% x 70% = 56%, not 70%"), so the reader can redo it.
- **Needs.** Say what the fix is when there is one right answer. When the
  sources disagree and either could be right, give the options and name who
  decides (the team, the sponsor, the PM); do not pick a winner. The audit is
  what the team decides from.
- **Citing the book.** Cite the PDF page, which is what `pdftotext` and the
  Read tool take, with the printed page in brackets: "form 2.32, PDF page 141
  (printed page 130)". PDF page = printed page + 11. A bare "page 130" is
  ambiguous and draws a question.
- **Script output is a lead, not a finding.** Read the line each script points
  at before reporting it, and say in Method how many script findings you
  dropped as false positives and why. Every `range` warning is either reported
  or explained: it is the check that found "R1 to R10" and "V1 to V11".
- **A defect the source explains is still accounted for.** Where the source
  states its reason (a uniform Priority column with the sentence above the
  table saying why), list it under What passed with the line of the reason,
  and make it a warning only if the reason does not hold.
- **No fixes.** Do not edit the audited files unless asked; the report is the
  deliverable.
- **Language.** Write the report in English unless asked otherwise. Replies to
  reviewer threads go in the reviewer's language (see `review-lessons.md`
  section 11).
