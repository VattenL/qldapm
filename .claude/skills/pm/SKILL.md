---
name: pm
description: Generate, fill or audit project management documents from A Project Manager's Book of Forms (3rd edition), keeping printed fields in printed order, and answer project management decisions with PMBOK 6 techniques. Use it for any form in the book, filled or blank (charter, assumption log, stakeholder register, scope statement, WBS, schedule, cost, quality, resource, communications, risk and procurement plans, risk register, RACI, change request, issue, decision and change logs, status, variance and earned value reports, audits, closeout, agile forms), for a form number such as 1.1, 2.32 or 6.4, and to check, audit or review PM documents in docs/ or answer comments on the team's Google Doc. Also use it for decisions: a schedule slip, a cost overrun, a risk that occurred or a risk response, evaluating a change request, earned value status, reserves, estimates, or which form to use, in English or Vietnamese, even without naming the book.
version: 2.5.0
user-invocable: true
argument-hint: "[form number or name] | audit <files> | decide <situation>"
---

# Project management documents from the Book of Forms

This repo documents a project using *A Project Manager's Book of Forms*, 3rd
edition (Wiley 2017), the companion to the PMBOK Guide 6th edition. The PDF is
`A_Project_Managers_Book_of_Forms.pdf` at the repo root, and it holds 66 forms
across Initiating, Planning, Executing, Monitoring and Controlling, Closing and
Agile.

Three things make a generated form useful rather than plausible-looking:

1. **The printed form decides the fields.** Not memory: a charter with the right
   fields in the wrong order, or an invented "Risk Appetite" box, has to be
   checked against the book anyway. The printed labels of all 66 forms are
   transcribed in `references/fields/`, and the scripts build and check forms
   from that.
2. **Unknown stays visibly unknown.** `CLAUDE.md` forbids guessed values; marked
   assumptions are reviewable, hidden ones cost the team a meeting.
3. **The document agrees with itself and with its siblings.** Two review rounds
   (60 findings) were almost all about this: a sponsor described as the owner,
   "R1 to R10" after R12 existed, "management reserve" beside a contingency
   reserve. `references/review-lessons.md` lists what the reviewers catch.

All commands below run from the repo root. The scripts are plain Python 3;
only `md_to_docx.py` needs a package (`uv run --with python-docx`).

A request for a document ("give me the 2.32 risk register") follows the form
workflow. A request for a decision ("we are two weeks late", "R5 happened")
follows "Deciding, not just documenting" after it and ends in the forms that
record it. A request can need both: decide first, then update the forms.

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
python3 .claude/skills/pm/scripts/extract_form.py 2.32 --knowledge               # what goes in each field, sources, consumers, decisions
```

`--knowledge` prints `references/knowledge/<form>.json` and needs no PDF. Use
it to decide what goes in each box: each printed label with what the book says
belongs there (labels the blank form prints that the book does not describe are
listed apart, "not stated in the book"), then the documents the form receives
from, provides to and must agree with, the tailoring tips, the agile note and the
decisions it records. "The book does not say" means the book is silent and the
team decides; do not turn it into a rule. Its labels can differ from the blank
form's (2.32 prints ID where the element table says Risk ID); the blank form
wins, and `--fields` is the spelling to copy. `--fields` prints the spec (title
block, blocks per page, grouped headers, banks, row labels, pairs, legend, notes)
and needs no PDF; read its notes line, which records what the JSON cannot hold (a
box that prints numbered lines, sample content that must not be copied). The default
output is the book's Document Element table plus the blank form as text; `--alignment`,
`--tailoring` and `--prose` add sections.

**No Alignment section.** 2.17, 2.21 and 2.32 have none ("not present for this
form"). Run `--prose` and take the documents the form receives information from
and provides information to; those are the documents to compare in step 5, and
the reading paragraph says that is where the list came from.

**Pictures.** For a `chart` or `diagram` kind (2.3, 2.15, 2.18, 2.22, 6.3) also
look at the blank pages with the Read tool (`pages` takes PDF pages): `pdftotext`
flattens a Gantt chart, and the page shows what the table behind it must carry.

### 3. Gather project facts

A blank template carries no project facts: skip the project documents for it (see step 4), keep the printed form, and read the area note
for the form's purpose only. Otherwise read `references/house-style.md` (marking rules, where facts live) and, in
`references/rendering.md`, the section for this form's kind. From
`references/review-lessons.md` read sections 1, 2, 7, 8 and 9 for every form (section 1
holds the PM-name rule for 1.3 and 1.4), and sections 3 to 6 when the form carries
numbers, scope boundaries, money or success criteria. Reading all of it for a
one-page register costs time and adds nothing.

Read the PMBOK 6 note for the form's knowledge area. Each note maps the
chapter onto the forms, gives the page map (printed and PDF page), lists the
terms with the book's meaning, says where this project's facts live, and ends
with the decisions in that area. The area is the chapter of the process in the
form's `pmbok_processes` (`--knowledge` prints it); a form that lists processes of several chapters (4.3, 4.4, the reports 4.1 and 4.2) takes
the note of every chapter it lists:

| Note in `references/` | Forms |
| --- | --- |
| `pmbok-integration.md` (chapter 4) | 1.1, 1.2, 2.1, 2.2, 2.3, 3.2, 3.3, 3.4, 3.5, 4.2, 5.1, 5.2 |
| `pmbok-scope.md` (5) | 2.4 to 2.10, 4.9 |
| `pmbok-schedule.md` (6) | 2.11 to 2.18 |
| `pmbok-cost.md` (7) | 2.19 to 2.22; 4.3 and 4.4 with the schedule, scope, procurement and integration notes they list |
| `pmbok-quality.md` (8) | 2.23, 2.24, 3.6 |
| `pmbok-resource.md` (9) | 2.25 to 2.29, 3.7, 4.1 |
| `pmbok-communications.md` (10) | 2.30, 4.1, 4.2, 4.6 |
| `pmbok-risk.md` (11) | 2.31 to 2.36, 4.5 |
| `pmbok-procurement.md` (12) | 2.37 to 2.39, 4.6, 4.7, 4.8 |
| `pmbok-stakeholder.md` (13) | 1.3, 1.4, 2.40, 3.1 |
| `pmbok-agile.md` (Agile Practice Guide) | 6.1 to 6.4, and any "agile", "iteration" or "release" claim in another form |

A management plan form (2.1, 2.2, 2.4, 2.5, 2.11, 2.19, 2.23, 2.26, 2.30,
2.31, 2.37, 2.40) is the output of a PMBOK 6 planning process, and the PMBOK
section lists what the plan carries, which can be more than the form prints;
the note says which. Read the chapter in `PMBOK6_and_Agile_Practice_Guide.pdf`
(PDF page = printed page + 39) only for what the note does not settle. The
book's process-to-form map and its wording rules are in
`references/book-structure.md`.

The facts live in `docs/charter-package.en.md` (form 1.1 in Part 2B, the ID
families, budget, risks, milestones, assumptions 1 to 19) and
`docs/scope-package.en.md` (2.7, 2.9, 2.10). Read the Markdown directly; the
helpers in `tools/gdoc_edit.py` (`section`, `first_table`, `table_by_first_cell`,
`field_map`) are optional. List `docs/forms/` and read every file in it, not only
the graph neighbours: a pending 3.3 can change a risk or a date you are about to
copy, and a note's sentence about what `docs/` holds can be stale. Ask the user
for what is genuinely missing rather than filling it in; one round of questions
beats a document nobody can trust.

### 4. Scaffold, then write

Start from the scaffold rather than a blank file. It already has the printed
title block, page headings, grouped headers (`Impact: Scope`), both banks,
row labels and checkbox groups in the shapes `rendering.md` prescribes:

```bash
python3 .claude/skills/pm/scripts/new_form.py 2.32                    # print it, writes nothing
python3 .claude/skills/pm/scripts/new_form.py 2.32 --out <path>       # write it where you choose
python3 .claude/skills/pm/scripts/new_form.py 2.32 --docs --rows 12   # docs/forms/2-32-risk-register.en.md, 12 empty rows
```

Only `--docs` (or `--dated`) writes into `docs/`, and never over a file without
`--force`; use it when the user asked for a file there. In a sandbox or an audit
write to the outputs folder or a scratch path with `--out`. `Project Title` is
left empty: copy it from the charter's title block when filling the form.

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
  the form, never inside it, in the fixed order of `rendering.md` (The italic
  note). Nothing goes inside the form that it does not print: no notes under a
  table, no explanation under Approvals.
- Copied project text (a risk statement, a response, a milestone name) is
  copied as written, not paraphrased, so the two documents stay one ID, one
  text (a 2.32 from the charter: `rendering.md`, Filling 2.32 from the charter).
- Assumed or derived values are inside `<mark>`; unknown values are an empty
  cell (the course brief says to leave a box empty when unknown) or `[TBD]`
  where an empty cell would read as an oversight.

**A blank template** is the scaffold with nothing added: every value empty,
the italic citation paragraph kept, no project names, dates, amounts or IDs.
Keep the scaffold's empty register rows so the shape is obvious, and leave Date Prepared empty. If the user
wants the team to fill it, say where it was written and that
`check_fidelity.py` passes on it. `check_consistency.py` on it is safe and optional (it only
proves no project fact leaked); `check_fidelity.py` is the required check. Never
copy a project fact, such as a work package or a date, into the reply.

**A recurring report** (4.1 to 4.4, 6.3, 6.4) keeps the blank as the master
`<number>-<slug>.en.md` and each filled copy is its own dated file,
`<number>-<slug>-YYYY-MM-DD.en.md` (the team's convention; the book prints one
form per report), written with `new_form.py <form> --out <dir>/ --dated YYYY-MM-DD` (`--dated` alone writes into `docs/forms/`).

### 5. Check

Run the mechanical checks, then read what they cannot see. Run each command
on its own and give its exit code in the reply: chained with `&&`, one failure
skips the rest unseen. Edit a source with the Edit tool, not `sed -i`, whose
flags differ on macOS.

```bash
python3 .claude/skills/pm/scripts/check_fidelity.py docs/forms/<file>.md <form>
python3 .claude/skills/pm/scripts/check_consistency.py docs/forms/<file>.md \
    docs/charter-package.en.md docs/scope-package.en.md --report docs/forms/<file>.md
python3 tools/check_scope.py        # when the scope package or anything it rolls up to changed
```

`check_fidelity.py` compares the form with `references/fields/<form>.json`: every printed label present, spelled and ordered as
printed. Missing or out-of-order labels exit 1; unprinted labels are reported only (remove each, or name it as a tailoring in the
reading paragraph). Options: `--flattened` (the scope package's 2.7 and 2.10 write a group header as its child label), `--ignore-tables`
(a table inside a free-text box, the roles table in 2.8), `--section "<heading>" --end "<next heading>"` for a form inside a package
(the text must match one heading; `audit-template.md` has the headings of 1.1, 2.7, 2.9 and 2.10), `--page N`, `--list <form>`.

`check_consistency.py` judges the new form against the whole package, because ID ranges, people and section references span files (`charter`
and `scope` stand for the two package files). `--report` prints only what the new form contributes; `--show-context` also lists the findings
left out as already in the sources. It catches markup (`table-rule`), dates, stale ranges, dangling section references, totals, uniform
columns, one ID with two texts, sponsor and customer merged, forbidden terms, `stale-m0`, an italic paragraph over about 150 words
(`note-length`) and the Approvals block. Every `range` warning is fixed or explained in your reply: it is the check that found "R1 to R10",
and a warning only because a deliberate subset ("F01 to F10" for a pilot) looks the same. When the form carries or cites a reserve, say
in one line which reserve the budget line names and, if the charter words it otherwise, report both wordings as a source error for the sponsor.

Then compare by reading. List what must agree with the form, rather than
recalling it:

```bash
python3 .claude/skills/pm/scripts/form_graph.py 2.32            # sources, consumers, alignment partners, with what flows
python3 .claude/skills/pm/scripts/form_graph.py --impact 2.9 2.10 --depth 1   # documents to recheck when forms change together
```

`--impact` lists the documents downstream of the forms, then the forms they must agree with, says which exist
in `docs/` ("N of M forms exist"), and marks a stand-in section (the charter holds the content of 1.2, 1.3, 2.6,
2.14 and 2.32 without reproducing those forms; recheck that section, it is counted apart). It adds links tagged
"skill mapping, not book text": the Impacts of Change areas of 3.3 to forms, and the forms whose results may
become a 3.3. Use `--depth 1` or `2`; without it the list runs to most of the planning forms. Read what exists
in `docs/` and compare the overlapping fields. Report contradictions to the user; do not quietly pick a winner,
because a disagreement between two project documents is usually a decision someone has to make. A "declared
only by" tag means the other form's section is silent, a gap in the book's lists and not a finding against the
project; treat it as weak when ordering forms. The scripts cannot catch a derived number computed from the wrong
reading of an assumption, a count that disagrees with its list, or scope that belongs to the project rather than
the product; those are in `review-lessons.md` sections 3 to 6, and `pm_calc.py` recomputes a derived figure.

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
(`references/push-audit.md`), because what reaches the Doc is what
the generator emits, not what the source says.

## Deciding, not just documenting

Use this path when the user asks what to do, not which form to fill. The forms
are where a decision is recorded; the decision itself comes from PMBOK 6 and
the Book of Forms. Do not answer a decision from memory and do not write a form
first.

1. **Route the situation.** Read `references/decisions.md` in parts (offset and limit), find the row of section 2 that fits
   ("R5 happened", "two weeks late", "client wants a new function", "work differs from the scope baseline", "which form
   do I fill for X"), then read the entry it names in section 3 and the same decision in the `pmbok-<area>.md` note (the
   table in step 3 of the form workflow). A 3.3 already in `docs/forms/`: read section 4, "While a 3.3 is pending", first.
   In Vietnamese, keep form titles in English and the diacritics (`house-style.md`, Vietnamese terms). If no row fits,
   take the closest decision and say so. Restate each fact the user gives (a date, a milestone, an owner, an
   amount) and check it against the documents before building options; a
   mismatch is the first open question. Ask for each missing input before
   recommending. When you cannot ask, list the questions first, then give a
   conditional answer ("if EV is X, then Y") and never one number built on an
   assumed input; label every assumed value. A status measure with no PV, EV
   or AC given is answered by naming what is needed ("PV and EV for the package
   are needed to state SV and SPI") and showing no figure. Project facts (every limit of the PM's authority, the
   reserve, thresholds, risk responses, milestone dates) are read from `docs/charter-package.en.md`, `docs/scope-package.en.md`
   and `docs/forms/` at the time, never from the catalog and never guessed; a form with no file
   there is read where the project keeps it (`decisions.md`, "Where this project keeps a form").
2. **Compute any derived number** with `pm_calc.py`, which prints each result
   with the page where the book prints its formula:

   ```bash
   python3 .claude/skills/pm/scripts/pm_calc.py evm --bac <BAC> --pv <PV> --ev <EV> --ac <AC>
   python3 .claude/skills/pm/scripts/pm_calc.py --help   # pert, effort-to-duration, analogous, bottom-up, risk-score, emv, weighted-score, earned-schedule, cpm, crash, velocity, cd3, payback, comms-channels, reserve, funding, response-effectiveness
   ```

   Report the inputs, the formula name and the result. Where the tool says "not
   stated in the book" (the beta standard deviation, payback, the critical path
   passes, the channel count n(n-1)/2, a percent overrun, the crashing cost per day), say so and label the
   figure an outside arithmetic aid; give a percent with its base and its amount (`evm --bac <BAC> --threshold <percent>`
   prints the amount; add `--pv --ev --ac` and `--base bac pv` to test an overrun). `cpm --start <date> --holiday <range>`
   turns a slip into calendar dates, and `--deadline` takes working days from day 1 or a date with `--start`;
   `crash --option NAME NORMAL CRASHED EXTRA` ranks crashing options by extra cost per day saved. When it cannot compute a figure (zero AC gives no CPI, zero
   PV no SPI) or refuses an input (a zero BAC), say why instead of substituting
   a value. Report an index as printed (four decimals, so 0.8621 is not shown as
   0.86) with the Table 7-1 words, money in whole currency units; no book states a
   rounding rule.
3. **List what else changes.** Run `form_graph.py --impact <anchor> --depth 1` on the row's impact
   anchor (`decisions.md` section 2, none for a which-form row; 3.3 as well only when a baseline move is the recommendation) and quote
   the count line of each anchor's run, never another form's. Paste the forms that exist in `docs/` and the
   stand-in sections it marks; name every other form the run prints as a form to create later, none dropped
   and none added, each form once across runs; with nothing in `docs/`, say "nothing to compare". For 3.3
   state its provides-to and recipient edges (2.2, 3.4, the change control board) even when they are not
   in `docs/`, and what it receives from. A decision that moves a baseline (scope 2.8 to 2.10, schedule 2.18,
   cost 2.22) also follows the change path in `decisions.md` section 4: the eight steps, stated in order as
   a numbered list. Answer the question first; a narrow question stays short (section 5, item 10).
4. **Present in the recommendation format** of `decisions.md` section 5:
   situation with sources, constraint check, options table (technique, the
   book's trade-off or "not stated in the book", baseline effect), one
   recommendation, calculator output, what the team must decide and who,
   forms to update, citations with both page numbers.
5. **Record it, after the user agrees.** 3.2 Decision Log for the decision, its
   alternatives and reason; 3.1 for an issue; 3.3 then 3.4 when a baseline, a
   plan or a constraint changes (the sponsor approves what is beyond the PM's
   authority in the charter); then the forms named by step 3. Offer to draft
   them. "What do I write" or "what do I tell the sponsor" is answered with the
   draft in the reply (`decisions.md` section 5, Drafts); write a file only when
   asked, and nothing under `docs/` unless told.

**Rules for every recommendation.** These are the team's, and the catalog
repeats them:

- Every remedy is a technique PMBOK 6 or the Book of Forms names (crashing,
  fast tracking, resource leveling, reserve analysis, avoid, transfer,
  mitigate, accept, and so on), with the trade-off the book states. If the book
  states none, write "not stated in the book" and mark the choice as judgment.
- Never shorten an estimate to fit a date or a fund. No chapter names that
  technique. When scope, schedule, cost and quality cannot all hold, the route
  is a change request (3.3) to the sponsor, with the options and their effects.
- Contingency reserve (inside the cost baseline, for identified risks) and
  management reserve (outside it) are different; check which one the project
  has before using either word. When the charter words the reserve otherwise than its
  budget line, report both wordings in one line as a source error for the sponsor
  (`decisions.md` section 5, item 11).
- Do not invent an owner, a threshold, a score, a rate or a date. Ask, or leave
  it empty and say it is for the team.

Worked routes ("two weeks late", "R5 happened", "a new function") are in
`decisions.md` sections 1 and 2.

## Citing the book

Cite the PDF page of the blank form, with the printed page in brackets: "form
2.32, PDF page 141 (printed page 130)". `forms-index.md`, `pdftotext` and the
Read tool all use PDF pages, while the book's own page numbers and the team's
older documents use printed pages; PDF page = printed page + 11. A bare "page
130" is ambiguous, because both numberings are in use and they differ by 11
pages, which is a different form. For a prose fact, cite
the prose page the same way ("section 1.1 list, PDF page 13 (printed page
2)"). Every page mention in a reply, a table cell and a pointer included, carries
both numbers, and every claim about a book carries them too: a section number
alone ("PMBOK 6 section 6.5.2.6") or a pointer to a note is not a citation, and
"the book prints no X" becomes "not stated in the book" with the section searched
and its pages. A note's `p215/254` is printed 215, PDF 254: write both words. In Vietnamese
write "trang in 215 (trang PDF 254)".
`scripts/check_pages.py <reply file>` flags a bare page (error) and a section
with no page or a negative claim with none (warning); text inside quotation
marks or after `> ` is the audited document's own and is skipped.

## Auditing or answering a review

When the user asks to check, audit or review documents, or to answer comments
on the team's Google Doc, the job is the reviewer's, not the author's. Do not
fix while auditing unless asked: the audit is what the team decides from.

1. **Scripts first, over the whole package.** Run `check_consistency.py --audit` over every file of the
   deliverable together (`--audit` also reports a constant column that the text above it explains; add
   `--report <file>` when one file is the deliverable, so the errors the sources already carry are not mixed
   in), `check_fidelity.py` on each form (`--section` per form inside a package), `check_schedule.py` on a
   2.18, and `tools/check_scope.py` when the scope package is in scope. Read the line behind each finding
   before reporting it; a script finding is a lead (`check_consistency.py --group` collapses one defect that shows as many
   findings). A pending 3.3 explains a date or an hour total (`--explained hours`), never an order defect: `--explained
   sequence=REASON` and `break=REASON` need the reason quoted. Before a push ask for the Doc ID; without it, or without
   credentials, say in Method that the live Doc and its comments were not audited.
2. **Walk `review-lessons.md`** section by section against the documents, all of it this time. Recompute
   every derived figure from its assumption as written, and count every list a number describes: grep each
   stated count ("fourteen", "V1 to V11") and compare it with its source list (the `count` check reads
   `references/book-counts.json`). Compare each Date Prepared with today (`check_consistency.py --today YYYY-MM-DD`) and
   each stated duration with its window (`audit-template.md`, Stated durations and staleness).
3. **Check sequence.** In a schedule, a WBS dictionary or a milestone list, read each work package's activities in
   date order and each milestone against the work it names. Look for anything used, reviewed, accepted or signed
   before the thing exists or finishes; a phase closed before the period it closes; a date inside a period the
   charter rules out (a holiday, a freeze). `check_schedule.py` finds a check dated before its subject, a closeout
   before its warranty or its milestone, a go-live before the UAT, a test before the build, a review before another
   package's work, a stated count against its window, and work in a break; the rest is read, by the recipe in
   `audit-template.md` (Used before it exists). Run every mandatory scan of `audit-template.md` and list each one that
   found nothing (`<br>`, a merged sponsor and customer, RTM Source and Priority across Parts 1 and 1B) under "Scans that
   found nothing"; an RTM whose Priority is one value throughout is a warning even when a sentence explains it.
4. **Check load per person per week** (below). `check_schedule.py` also compares booked with priced hours. A
   plan whose people are booked above their allocation is not a plan.
5. **Audit a generated form, or the push pipeline,** when a file is generated (2.18) or the documents are about to
   go to the Doc: `references/push-audit.md`.
6. **Report** in the shape of `references/audit-template.md`: Errors numbered E1..., then Warnings W1..., each
   with the location (`file:line` and the section or form page), the evidence quoted, and the fix or the
   decision it needs and who makes it. A defect that is explained but undecided is a warning naming the
   decision. Write it as a Markdown file only where the user asks; otherwise give it in the reply.
7. **Replies to reviewer threads** follow `review-lessons.md` section 11 and go in the reviewer's language.
   `tools/gdoc.py comments --doc <id>` lists the threads; `tools/gdoc.py post --doc <id> --review <file>
   --dry-run` shows what would be posted.

### Load per person per week

`python3 .claude/skills/pm/scripts/load_check.py docs/scope-package.en.md --charter docs/charter-package.en.md
--limit MOB1=<hours> --leaves MOB1=YYYY-MM-DD` spreads each person's hours over the working days of each package's window
(less the breaks the charter dates with an end, or `--holiday`), sums by week and compares with the person's limit and
leaving date; `--schedule <2.18 file>` uses the rows of a levelled 2.18 instead. It also reports a day above 24 hours and a
package ending after a milestone it feeds. The default limit is 40 and each finding under it says "limit assumed"; when the
charter gives a part-time person no weekly figure (only person-months), 40 hides an overload: report the person-months against
the window, ask the sponsor for the weekly limit, and list it as an open question. An overload is an error until a document
explains it (`--explained overload=REASON`), then a warning. Report a week as overloaded only when it is clearly over.
Method: `references/load-check.md`.

## Checks before you hand it over

- `check_fidelity.py` passes (every printed label spelled and ordered as printed;
  each unprinted label removed or named as a tailoring) and `check_consistency.py
  ... --report <form>` shows no errors, with every warning left explained.
- No em dashes, no emoji (`CLAUDE.md`). Every assumed value is inside `<mark>`,
  every unknown is empty or `[TBD]`, nothing is invented.
- Nothing inside the form that the printed form does not carry; explanations go
  in the italic paragraph before it, with the citation in PDF and printed pages.

## Files

| Path | What it is |
| --- | --- |
| `references/forms-index.md` | All 66 forms: PDF page ranges, kind, printed titles, title-block, bank and group quirks |
| `references/fields/<form>.json` | Printed labels per blank page: title block, blocks, groups, banks, row labels, pairs, legend, notes |
| `references/rendering.md` | How each kind becomes Markdown, and why; filling 2.32 step by step |
| `references/house-style.md` | Marking rules, dates, forbidden terms, Vietnamese terms, 1.3 fill rules, where the project's facts live |
| `references/review-lessons.md` | What the team's reviewers caught, and how to check for it |
| `references/decisions.md` | Decision catalog: 40 routing rows with impact anchors, 43 decisions with the book's trade-offs, calculator, forms to record in and escalation; the authority limits, the change control path, the recommendation format and drafts |
| `references/pmbok-<area>.md` | One note per knowledge area and `pmbok-agile.md` (`pmbok-quality.md` is the model): page map, terms, where the project's facts live (pointers, no copied figures), decisions. Form-to-note table in step 3 |
| `references/knowledge/<form>.json` | Per form: purpose, what goes in each field, sources, consumers, alignment, tailoring, decisions, citation; read through `extract_form.py --knowledge` |
| `references/book-structure.md` | How the Book of Forms is organised, which process each form comes from, its wording rules |
| `references/form-graph.md` | Generated map of the 66 forms; regenerate with `form_graph.py --markdown --out references/form-graph.md` (it prints without `--out`) |
| `references/audit-template.md` | Shape and rules of an audit report, the mandatory scans, and the used-before-it-exists recipe |
| `references/push-audit.md` | Auditing a generated form (regenerate into a scratch copy) and the payload pushed to the Doc |
| `references/book-counts.json` | Rows the books print in a named table, for the `count` check |
| `references/load-check.md` | Load per person per week: the method, `--schedule` and the level.py comparison |
| `scripts/extract_form.py` | Form text from the PDF; `--fields` the spec, `--knowledge` the field guidance and links (no PDF needed), `--alignment`, `--tailoring`, `--prose` |
| `scripts/pm_calc.py` | Derived numbers with the page that prints each formula (`evm`, `pert`, `effort-to-duration`, `analogous`, `bottom-up`, `risk-score`, `emv`, `weighted-score`, `earned-schedule`, `cpm`, `crash`, `velocity`, `cd3`, `payback`, `comms-channels`, `reserve`, `funding`, `response-effectiveness`); the outside arithmetic aids say so in their output; `--json` |
| `scripts/load_check.py` | Hours per person per week and per day against a limit and a leaving date, from the dictionary or a levelled 2.18; `--limit`, `--leaves`, `--schedule`, `--explained`, `--holiday`, `--charter` |
| `scripts/check_pages.py` | A reply or note: every page number needs its printed or PDF partner (English or Vietnamese); a section or a negative claim with no page warns |
| `scripts/form_graph.py` | The forms as a dependency graph: `<form>`, `--impact <forms> [--depth N] [--category C]`, `--order`, `--check`, `--markdown [--out F]` |
| `scripts/new_form.py` | Blank Markdown form from the spec; prints by default; `--out` (file or directory), `--docs`, `--dated`, `--rows`, `--force` |
| `scripts/risk_actions.py` | The Actions cell of 2.32 for each risk from the scope package's coverage check |
| `scripts/check_fidelity.py` | Printed labels present and in order; `--list`, `--section`, `--end`, `--page`, `--flattened`, `--ignore-tables` |
| `scripts/check_consistency.py` | Cross-document checks from the review findings; `--report`, `--show-context`, `--group`, `--today`, `--errors-only`, `--audit` |
| `scripts/check_schedule.py` | A 2.18 against the charter and the cost estimate: order checks, breaks, milestone names, stated counts, booked against priced hours; `--explained` |
| `scripts/md_to_docx.py` | Form Markdown to a .docx that looks like the book |
| `scripts/test_*.py` | Tests: `uv run --with pytest --with python-docx pytest -q .claude/skills/pm/scripts` |
| `evals/evals.json` | Test prompts with gradable assertions |
