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
already in the sources not shown"; what was read by hand; what was recomputed;
whether the live Doc and its comments were audited, or "not audited: no Doc ID
or credentials given">.

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

## Scans that found nothing

<One line per scan run with zero hits, with the count, so the reader knows it was
run: "literal `<br>` in the WBS dictionary cells: 0 hits", "sponsor and customer
merged in one cell: 0 hits", "RTM Part 1 against Part 1B for Source and Priority
(`id-conflict`): the IDs agree, for example BR03 Source in both". A scan that is
not reported here was not run. The mandatory scans of an audit of the charter and
scope package are listed under "Mandatory scans" below.>

## What passed

<The other checks that found nothing: totals that add up, labels in printed order,
ranges current, dates in one style.>
```

## Mandatory scans for the charter and the scope package

Each is reported as a finding with its location, or on a line of "Scans that found nothing" with its count. A scan that a defect is absent from is a pass; a scan that is not mentioned is a fail.

1. Mixed or abbreviated date formats (`check_consistency.py`, `date` and `date-style`).
2. Literal `<br>` or any HTML other than `<mark>` in the WBS dictionary cells (`grep -c '<br>'` on the scope package, and on the charter).
3. A sponsor and a customer merged in one cell or phrase, such as an RTM Source of "Center Director, sponsor" (`check_consistency.py` `role`).
4. The Cost success criterion's reserve wording against the budget line (`term`): report both wordings and say it is a charter source error for the sponsor to resolve.
5. **RTM Priority uniform.** Count the Priority cells of RTM Part 1 and Part 1B; when every row reads "Must have" (31 rows in Part 1 and 26 in Part 1B on the day this was written; recount), the column carries no
   information. Report one warning even when a sentence above the table explains it: quote the sentence and say what would close the warning (the form's own rule makes the value constant, or the team grades the rows).
   `check_consistency.py --audit` prints it as `uniform-column` and names the column and the value; the audit still has to list it.
6. The same requirement ID across RTM Part 1 and the Inter-RTM Part 1B for Source and Priority (`id-conflict`): every difference with both locations, or "the IDs agree" with an example.
7. Notes placed inside a printed form (`form-note`; each hit is its own finding, see Rules for findings), stated counts against their lists (`count`), ID ranges against the families (`range`), contents lines such as "V1 to V11" against the prompt log.
8. Derived figures recomputed from the assumption as written (the business-case activation share, the part-time person's load against the allocation: `load_check.py`).
9. **Stated effort against its window.** For every person the charter or the scope package gives an effort in person-months or hours and a window (joins after one milestone, leaves after another; a pilot of so many hours), run
   `load_check.py --effort NAME=QTY:UNIT:FROM:TO --hours-per-pm <the source's figure> --effort-source "NAME=<file:line>, <file:line>"` and report the implied FTE. It is a finding when it is above full time, or above the part-time
   fraction or weekly limit the documents state; the dictionary spread (scan 8) cannot see it, and an aside in another finding does not count. The finding cites **each source line**: every sentence that states the effort, the join and leave points
   (with the milestone dates and the line of the charter table that dates them), the sheet that places the work, and the line that gives the length of a person-month; it quotes them and shows the arithmetic (hours, working days, weeks, hours a
   week, FTE). The length of a person-month is the source's or the caller's, never silent: name the line it came from, or say it is assumed and ask the sponsor. When the documents state no weekly limit, the finding is a warning that asks for it
   (the effort above full time is an error: it contradicts itself without any limit). A scan with no person-month effort in the sources is listed under "Scans that found nothing" as such.
10. `check_pages.py` on the report itself.

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
  the heading the text sits under. Every finding, errors and warnings alike, has a
  `file:line` and quoted text: a finding without both is a lead, not a finding. A
  finding about a count or a pattern lists every location, each with its line.
- **A generated picture.** For a defect seen in a Gantt page, the milestone chart or the
  histogram, the picture has no line to cite, so give: the generator and its function
  (`tools/schedule.py`, `tools/gdoc_schedule_tab.py` `build()`), the payload heading the image sits
  under (`4.1 Project Schedule`), the `@@IMAGE` or `![...]` line in the source or payload with
  its line number, and the source rows the bar or the label was drawn from (`file:line`, quoted:
  the dates, the task name). Say which image you viewed (its file name or page) and what is wrong
  in it in words (a bar starting after its finish, a label cut off); the Needs line names the
  generator or the source row, never the image.
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
  (`references/push-audit.md`) and compare.
- **Evidence is quoted.** Copy the words, figures and dates as written, inside quotation
  marks or on a line that starts with `> `: `check_pages.py` skips both, so a page number in
  the audited text is not read as a citation. A derived figure shows the arithmetic from
  the assumption as written (for example "80% x 70% = 56%, not 70%"), so the reader can redo it.
- **Needs.** Say what the fix is when there is one right answer. When the
  sources disagree and either could be right, give the options and name who
  decides (the team, the sponsor, the PM); do not pick a winner. The audit is
  what the team decides from.
- **Citing the book.** Cite the PDF page, which is what `pdftotext` and the
  Read tool take, with the printed page in brackets: "form 2.32, PDF page 141
  (printed page 130)". PDF page = printed page + 11. A bare "page 130" is
  ambiguous and draws a question, and a section number alone is no citation:
  run `check_pages.py` on the report.
- **A form note is its own finding.** `check_consistency.py` `form-note` prints the quoted text of each
  note. Report every hit separately, never as "n form-notes at lines a, b, c": quote the note, give
  `file:line` and the printed page heading it sits under, and state the severity and why. A note that
  changes what the form says (a tailoring, a condition, a figure the form has no field for) is a
  warning that names what would close it (move it above the form into the italic reading paragraph,
  or print it in a field the form has); one that contradicts a printed field or another document is
  an error with both quotations; one that only repeats the source below the form is a warning of
  low weight, and still listed. A hit dropped as a false positive (a label the script does not know)
  is counted in Method with its quoted text. `--group` still prints every note on its own line.
- **Script output is a lead, not a finding.** Read the line each script points
  at before reporting it, and say in Method how many script findings you
  dropped as false positives and why. Every `range` warning is either reported
  or explained: it is the check that found "R1 to R10" and "V1 to V11".
- **A defect the source explains is still accounted for.** Where the source
  states its reason (a uniform Priority column with the sentence above the
  table saying why), a reason does not make a constant column informative:
  report it as a warning (`check_consistency.py --audit` does) that quotes the
  reason's line and says what would close it. Only a value the printed form
  itself makes constant is listed under What passed.
- **An overload, stated once.** `load_check.py` reports a week above the person's limit as an error until a document explains it (`--explained overload=REASON`, the reason naming the document);
  then it is a warning that names the decision it waits for, as with the other `--explained` checks. The limit itself is an assumption when the charter gives none: `load_check.py` says "limit assumed",
  and the report repeats it.
- **Script severity is not report severity.** `check_schedule.py` reports the hours mismatch as an
  error. When a document states the reason (a pending 3.3 with an empty disposition), run it with
  `--explained hours` so the line reads as a warning, and name that document; without such a document it
  stays an error. The same flag exists for `break` and `milestone-name`. A pending 3.3 explains a
  forecast date or an hour total, never an order defect (a review before the thing it reviews, a go-live
  before the UAT): `sequence` and `go-live` are accepted only as `--explained sequence=REASON` with the
  reason the order changed, quoted from the document; without one the finding stays a finding.
- **A break of unknown length.** When the charter dates the start of a break and not its end (the
  `break` check counts everything on or after the first day), report one warning that says no end date
  is given and asks the sponsor for it; list the dated rows as examples, not as a count of defects.
  When the charter also says the break can absorb no overrun (`check_schedule.py` reads that sentence), work booked inside it is an error, not a warning: it contradicts the charter,
  and the end date is still the sponsor's to give. `--explained break=REASON` needs the reason and names the document that dates the forecast.
- **Explained but undecided is a warning.** A change request with an empty
  disposition, a forecast awaiting the sponsor, a deliberate tailoring not yet
  approved: a warning that names the decision and who makes it. It becomes an
  error when a document relies on it as if it were settled.
- **An unprinted label.** One the document names as a tailoring in its reading
  paragraph (SKILL.md step 5) is a warning; one it does not name is an error.
  `check_fidelity.py` reports both the same way, so read the paragraph.
- **A file that predates a rule.** The first forms in `docs/forms/` carry
  `**Project:**`, `**Date prepared:**` and `**Source:**` (`house-style.md`,
  File layout): a warning naming the rule, once per file.
- **Expected warnings are listed, not counted.** A Doc payload gives
  `section-ref` warnings that only point at another document or tab
  (`push-audit.md`, step 3). List them as expected in Method.
- **Look at every generated image.** The Gantt pages, the milestone chart and
  the histogram are checked with the Read tool, one by one; say how many you
  viewed. The form table prints hours only on divided rows, so a chart can
  disagree with a table it was drawn from.
- **What the load check cannot see.** `load-check.md` spreads dictionary hours
  over the package windows and `tools/level.py` checks the levelled days; neither
  checks a person's hours in the week of a named milestone or a part-time limit
  unless you pass the person's own limit, and neither compares a stated person-months
  with the window it is placed in (that is `load_check.py --effort`, mandatory scan 9).
  Say so in Method when it matters.
- **Known findings are listed, not hidden.** `check_fidelity.py` on the scope package's 2.7 and on 2.10
  exits 1 without the option because the package writes a printed group header as its child labels; run it with `--flattened`
  (it accepts the child alone, `Category`, and group and child, `Labor Rate`), report the flattened labels as one warning
  that names `rendering.md`, and do not count it as a second defect. For the 2.7 pages together use `--section "Part 1:"
  --end "Part 2:" --flattened`; for the second page alone `--section "Part 1B" --page 2 --flattened` (a plain `--section
  "Part 1B"` expects the repeated title block, which the package writes once). A table inside a free-text box (the roles and
  functions tables of 2.8) lists its headers as unprinted labels: run `--ignore-tables` and name the tables in Method. For the
  charter use `--section "2B. PROJECT CHARTER form" --end "Part 3: Prompt Log"`. For the scope package's 2.10 use `--section "Part 3" --flattened`. For its 2.9 use `--section "Part 2" --end "Roll-up"`: ending at "Part 3" takes in the Roll-up table and lists 12 labels that
  are not 2.9's. Findings already in the sources are separated with
  `check_consistency.py --report <file>`; a second pass over the whole package lists the context
  errors apart, so a new form's findings are not mixed with them, and `--show-context` lists them with the heading each sits under. `--group` prints one line per check and level (one defect often shows
  as a finding for every date or citation it touches), and `--today YYYY-MM-DD` compares each Date Prepared with that day.
- **Scope of an audit.** A linked form beside the packages (2.18, 3.3) is audited when it is in the
  deliverable list, and is evidence only otherwise; say which in Method. A fact from outside the documents
  (a public holiday, a vendor's lead time) is marked as outside knowledge and written as the question it
  raises, never as a defect of the documents.
- **Used before it exists.** The scripts catch a check dated before its subject, a closeout before its
  warranty and a go-live before the UAT; the rest is read. Recipe for a WBS dictionary or a 2.18: (1) list the
  things the plan consumes that a sheet must first create: each deliverable and function ID (D1 to D11, F01 to F12; the
  scope package's Coverage check names the sheet that delivers each D), and the nouns that need setting up (an
  environment, test devices, accounts and licences, migrated or sample data, a reviewer's time); (2) for each,
  `grep -n -i "<noun>" docs/scope-package.en.md docs/forms/2-18-project-schedule.en.md` and note the sheet or row that
  creates it and the rows that use it, with the Due Dates or Start and Finish of each; (3) report a use whose window ends
  before the creating row finishes, quoting both rows with their dates, as a warning (an error when the later row is
  the only creator). Authoring a test or a plan for a function before it is built is not a use; running, reviewing,
  accepting, demonstrating, training on or deploying it is. Count what you checked under "What passed". Three more cases of the recipe: (a) compare the dictionary's activities with the 2.18 rows: a dictionary
  activity with no 2.18 row (the material-only purchase rows are an example) is itself a finding, because the thing it creates (a device, an account, a licence) then has no dated creating row; (b) an order that the
  source dictionary itself asks for (a sentence such as "testing is against the requirement baseline of M1, not against what was built") is a warning that quotes the dictionary line, because the order follows the
  source, and an error when it contradicts the charter or the printed form; (c) `check_schedule.py` also reads `closeout`, `test-order`, `review-order` and `stated-count` leads: read both rows before reporting.
  Text inside a printed form that the form does not print is `check_consistency.py` `form-note`; a product name in the Project Title box or a note under a heading that script does not know is layout
  no script sees: read the form page against the blank.
- **Stated durations and staleness.** Compare each duration the documents state (a pilot, an account
  enrolment, a warranty month) with the window the schedule gives it, and Date Prepared
  with today's date: a form prepared before a milestone that it describes as future is stale.
- **No fixes.** Do not edit the audited files unless asked; the report is the
  deliverable.
- **Language.** Write the report in English unless asked otherwise. Replies to
  reviewer threads go in the reviewer's language (see `review-lessons.md`
  section 11).
