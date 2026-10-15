# PM skill guide

How to use the `pm` skill in Claude Code to produce, check and audit forms from *A Project Manager's
Book of Forms*, 3rd edition, for this project. Written for teammates who know the course and the book
but have not read the skill's internals.

Vietnamese version: [`pm-skill-guide.vi.md`](pm-skill-guide.vi.md).

Every command below was run in this repo from the repo root, except the `gdoc` commands that need the team's Google credentials: the form commands on 1 October 2026, and the decision commands (`--knowledge`, `pm_calc.py`, `form_graph.py`, section 8) on 15 October 2026.

## Contents

1. What the skill does and does not do
2. Before you start
3. Asking for a form
4. From request to deliverable
5. The three marking states
6. House rules the reviewers enforce
7. Audits and Google Doc comments
8. Deciding: asking what to do
9. All 66 forms
10. Command cheat sheet
11. Troubleshooting
12. Improving the skill

## 1. What the skill does and does not do

The skill lives in `.claude/skills/pm/`. Claude Code loads it on its own when you ask for a form, cite
a form number, ask for an audit of the documents in `docs/`, or ask what to do about a project situation
(a slip, an overrun, a risk that happened, a change request).

| It does | It does not |
| --- | --- |
| Find the right form among the 66, by number or by name, and ask when a name matches several | Recall field lists from memory; every label comes from `references/fields/<form>.json`, transcribed from the blank pages |
| Scaffold the form in Markdown with the printed title block, labels, page headings, grouped headers and banks, in printed order | Add fields, columns or notes the printed form does not carry |
| Fill it from `docs/charter-package.en.md`, `docs/scope-package.en.md` and the forms in `docs/forms/` | Invent project values; anything assumed is highlighted, anything unknown stays empty or `[TBD]` |
| Run the fidelity and consistency checks and report what they find | Pick a winner silently when two project documents disagree; it reports the conflict for the team to decide |
| Render a form to `.docx` that looks like the book | Push to the team's Google Doc unless you ask, and never without the Doc ID you give it |
| Audit the package and draft replies to reviewer comments | Fix files while auditing, unless you ask for the fixes |
| Answer "what should we do" with options that are PMBOK 6 or Book of Forms techniques, each with the book's trade-off, then compute the derived numbers and list the forms that must change (section 8) | Shorten an estimate to fit a date, invent an owner, a threshold or a score, or decide for the sponsor; when scope, schedule, cost and quality cannot all hold it routes to a change request (3.3) to the sponsor |

The Markdown in `docs/` is the source of truth. The `.docx` and the Google Doc are built from it.

## 2. Before you start

| Need | Why | Check |
| --- | --- | --- |
| Claude Code, opened at the repo root | The skill is project-scoped and the scripts use repo paths | `/pm` appears when you type `/` |
| Python 3 | All scripts are plain Python (checked on 3.9 and 3.14) | `python3 --version` |
| `pdftotext` (poppler) | Reads the book's text for `extract_form.py` | `pdftotext -v` |
| `uv` | Runs `md_to_docx.py`, the tests and the Google tools with their packages | `uv --version` |
| `A_Project_Managers_Book_of_Forms.pdf` at the repo root | The authority for every form | `ls A_Project_Managers_Book_of_Forms.pdf` |
| `~/.config/qldapm/client_secret.json` | Only for reading or writing the Google Doc | see README, section Google Doc |

Page numbers: the skill and the scripts use **PDF pages**. PDF page = printed page + 11. Cite both, as
in "form 2.32, PDF page 141 (printed page 130)".

## 3. Asking for a form

Ask in plain English or Vietnamese. Naming the form number is the fastest way to get the right one.

| You want | Example prompt |
| --- | --- |
| A filled form | `Make the 2.32 Risk Register from the risks in the charter. Keep the R numbers; we have not scored probability or impact yet.` |
| A filled form, in Vietnamese | `Tạo cho nhóm form 1.3 Stakeholder Register từ charter, đúng form trong sách nhé. Nội dung tiếng Anh.` |
| A blank template | `Give me a blank 4.2 Project Status Report for the team, we'll fill it in every week.` |
| A blank template, in Vietnamese | `Cho mình form 2.14 Milestone List để trống, nhóm sẽ tự điền.` |
| An audit | `Audit docs/charter-package.en.md and docs/scope-package.en.md before we push them. Errors and warnings with locations. Don't fix anything.` |
| An audit, in Vietnamese | `Kiểm tra docs/forms/2-18-project-schedule.en.md so với charter và scope package, liệt kê lỗi và cảnh báo, đừng sửa file.` |
| A Word file | `Render docs/forms/2-32-risk-register.en.md to .docx for submission.` |
| A decision | `The mobile work is two weeks late against its milestone. What are my options and what do I update?` (section 8) |
| A decision, in Vietnamese | `khach hang muon them chuc nang moi thi ghi vao dau?` (section 8) |

You can also call the skill directly with a slash command:

```text
/pm 2.32                      fill form 2.32 from the project documents
/pm risk register             same, by name
/pm 4.2 blank                 the empty form, no project values
/pm audit docs/charter-package.en.md docs/scope-package.en.md
```

Tips:

- **Content language.** Deliverables are written in English even when you ask in Vietnamese. Say so
  if you want otherwise.
- **Ambiguous names.** "risk" matches six forms (2.31, 2.32, 2.33, 2.34, 2.36, 4.5). The skill lists
  them and asks rather than guessing.
- **Missing facts.** If the documents do not hold a value the form needs, the skill asks you or leaves
  it empty. Answer the question; do not tell it to "just fill something in".
- **Where it writes.** A new form goes to `docs/forms/<number>-<slug>.en.md`, for example
  `docs/forms/2-32-risk-register.en.md`. It never overwrites an existing file unless told to.

## 4. From request to deliverable

```text
request
  1. resolve the form          references/forms-index.md, extract_form.py
  2. read the printed form     extract_form.py --fields and --knowledge, plus the PDF page for charts
  3. gather project facts      docs/charter-package.en.md, docs/scope-package.en.md, docs/forms/
  4. scaffold, then fill       new_form.py, then Markdown edits
  5. check                     check_fidelity.py, check_consistency.py, tools/check_scope.py, form_graph.py --impact, reading
  6. render (if asked)         md_to_docx.py
  7. push (if asked)           tools/gdoc*.py, after auditing the payload
```

Claude runs these for you. You can run any of them yourself to see what it saw.

### Step 1 and 2: which form, and what it prints

```bash
python3 .claude/skills/pm/scripts/extract_form.py 2.32 --fields                 # printed labels, no PDF needed
python3 .claude/skills/pm/scripts/extract_form.py 2.32                          # Document Element table and blank form text
python3 .claude/skills/pm/scripts/extract_form.py 2.32 --alignment --tailoring  # plus Alignment and Tailoring Tips
python3 .claude/skills/pm/scripts/extract_form.py 2.32 --prose                  # the whole description
python3 .claude/skills/pm/scripts/extract_form.py 2.32 --knowledge              # what goes in each field, sources, consumers, decisions; no PDF needed
python3 .claude/skills/pm/scripts/extract_form.py risk                          # lists the six matching forms, exits 1
```

`--fields` output for 2.32, shortened:

```text
Title block: Project Title | Date Prepared
Page 1 of 1 (PDF page 141)
  table, bank 1: ID | Risk Statement | Owner | Probability | Impact: Scope | ... | Score | Response
  table, bank 2: Revised Probability | Impact: Scope | ... | Responsible Party | Actions | Status | Comments
Notes: ... Bank 2 prints no ID column. ...
```

Read the Notes line: it says what the labels alone cannot (banks, sample content not to copy, a label
printed twice).

`--knowledge` prints `references/knowledge/<form>.json`: the purpose, then each printed label with what
the book says goes in it, the documents the form receives from and provides to, the documents it must
agree with, the tailoring tips, and the decisions the form records. For 2.32, shortened:

```text
Fields, printed label then what goes in it (13):
  - ID [book element: Risk ID]
      A unique identifier for the risk. The blank form prints the column as ID.
  - Risk Statement [book element: Risk statement]
      The risk event or condition. Usually phrased 'EVENT may occur, causing IMPACT' or ...
Sources, information this form receives from (19):
  - 1.2
      Assumption log: reviewed as a source of risks ...; the book does not say which fields are used
Alignment, must agree with: none listed in the book
Tailoring tips: none printed for this form
Decisions recorded here (6):
  - Which response strategy a risk gets now
      Recorded in: Response
```

"The book does not say" means the book is silent and the team decides. Where the knowledge label and the
blank form differ (2.32 prints `ID` where the element table says `Risk ID`), the blank form wins; copy
labels from `--fields`.

### Step 3: where the facts live

| Facts | File and place |
| --- | --- |
| Problem, product, users, functions F01 to F12, exceptions | `docs/charter-package.en.md`, Part 1, 1.1 |
| Deliverables D1 to D11 | same, 1.2 |
| Acceptance criteria A01 to A12 | same, 1.3 |
| Exclusions, constraints, assumptions 1 to 19 | same, 1.4 to 1.6 |
| Charter elements: risks R1 to R12, milestones M0 to M7, budget, stakeholders | `docs/charter-package.en.md`, Part 2A |
| The filled 1.1 form | `docs/charter-package.en.md`, Part 2B |
| Requirements BR, FR, NFR and the RTM (2.7) | `docs/scope-package.en.md`, Part 1 and 1B |
| WBS (2.9) and WBS dictionary (2.10), resource codes PM, DEV1 to DEV3, QA1, MOB1 | same, Parts 2 and 3 |
| Schedule (2.18) and the change request for moved milestones (3.3) | `docs/forms/2-18-project-schedule.en.md`, `docs/forms/3-3-change-request.en.md` |

### Step 4: scaffold, then fill

```bash
python3 .claude/skills/pm/scripts/new_form.py 2.32                    # print the blank form, writes nothing
python3 .claude/skills/pm/scripts/new_form.py 2.32 --out <path>       # write it where you choose (a scratch path in an audit)
python3 .claude/skills/pm/scripts/new_form.py 2.32 --docs --rows 12   # docs/forms/2-32-risk-register.en.md, 12 empty rows
python3 .claude/skills/pm/scripts/new_form.py 2.32 --docs --force     # overwrite an existing file
python3 .claude/skills/pm/scripts/new_form.py 4.2 --out <dir>/ --dated 2026-10-19   # a dated copy of a recurring report, written into a directory outside docs/
python3 .claude/skills/pm/scripts/risk_actions.py docs/scope-package.en.md          # the Actions cell of 2.32 for each risk, from the coverage check
```

Only `--docs` (and `--dated` without `--out`) write into `docs/`. `Project Title` is left empty: copy it from the charter's title block when you fill the form.

The scaffold for 2.32 starts like this:

```markdown
# 2.32 Risk Register

*Form 2.32, A Project Manager's Book of Forms, 3rd edition, PDF page 141 (printed page 130). The table
prints in two banks, one above the other; row N of the second table continues row N of the first.*

**Project Title:**
**Date Prepared:**

| ID | Risk Statement | Owner | Probability | Impact: Scope | Impact: Quality | Impact: Schedule | Impact: Cost | Score | Response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

A blank template is this scaffold with nothing added: no names, dates, amounts or IDs.

How each kind of form becomes Markdown:

| Kind | Markdown shape |
| --- | --- |
| `fields` | `Field \| Content` table, bold label on the left, printed order |
| `log` | One table, one column per printed column; wide registers (2.32, 2.36, 3.1) as two tables, one per printed bank |
| `matrix` | Grid with row labels in the first column, printed legend kept below |
| `outline` | Nested numbered list (2.9, 2.29), never a Code / Element table |
| `chart`, `diagram` | The table behind the picture, plus a Mermaid block |
| `narrative` | The printed sentence stems, filled (6.1) |

A column under a printed group header is written `Group: Label`, for example `Impact: Scope`. Not
`Impact Scope`, not `Scope (Impact)`.

### Step 5: check

```bash
python3 .claude/skills/pm/scripts/check_fidelity.py docs/forms/2-32-risk-register.en.md 2.32
python3 .claude/skills/pm/scripts/check_consistency.py docs/forms/2-32-risk-register.en.md \
    docs/charter-package.en.md docs/scope-package.en.md --report docs/forms/2-32-risk-register.en.md
python3 tools/check_scope.py         # only when the scope package or what it rolls up to changed
```

| Check | Question it answers | Fails (exit 1) on |
| --- | --- | --- |
| `check_fidelity.py` | Does the Markdown carry every printed label, spelled as printed, in printed order? | Missing or out-of-order labels. Unprinted labels are listed but do not fail. `--flattened` accepts the scope package's RTM and WBS dictionary, which write a printed group header as its child label or as group and child, and lists them; `--ignore-tables` skips a table inside a free-text box; `--page N` checks one printed page of a form the document writes apart |
| `check_consistency.py --report <form>` | Does the new form agree with the charter and scope package? | Any error the new form contributes. Old errors in the sources are counted, not shown (`--show-context` lists them with the heading each sits under; `--group` prints one line per check, except that each `form-note` keeps its own line with its quoted text; `--today YYYY-MM-DD` compares each Date Prepared with that day; the words `charter` and `scope` stand for the two package files) |
| `tools/check_scope.py` | Does the scope package still roll up to 4,400 hours and 700,000,000 VND? | Any of its checks |

A clean form prints, for example:

```text
2.32 Risk Register, 2-32-risk-register.en.md lines 1 to 18
22/22 printed labels present in printed order
```

After the scripts, the skill lists the documents the book says this form must agree with and reports
contradictions:

```bash
python3 .claude/skills/pm/scripts/form_graph.py 2.32                      # sources, consumers, alignment partners
python3 .claude/skills/pm/scripts/form_graph.py --impact 2.9 2.10 --depth 1   # documents to recheck when forms change together
```

`--impact` marks each document as present in `docs/` or not, counts the files (2.9 and 2.10 share one) and says "Nothing to compare" when none exists, so the skill reads only what exists. A link
counts when either form declares it, and the tag says which. Section 11 explains how to read a failing
check.

### Step 6: Word file

```bash
uv run --with python-docx .claude/skills/pm/scripts/md_to_docx.py docs/forms/2-32-risk-register.en.md
uv run --with python-docx .claude/skills/pm/scripts/md_to_docx.py docs/forms/2-32-risk-register.en.md -o /tmp/risk.docx
```

The `.docx` has the book's dark title bar, bordered tables, the side-by-side field pairs the printed
form uses, and a "Page N of M" footer. Mermaid blocks are skipped; the table above them carries the
numbers. Only render when the document is for submission or printing.

### Step 7: the team Google Doc

The Doc is a copy of the Markdown. Change the Markdown, then rebuild the Doc; never hand-edit the Doc.

- Only on request, and only with the Doc ID passed on the command line (the ID is in `README.md`,
  section Google Doc). Nobody writes it into a file.
- Setup once per machine: `README.md`, section Google Doc.
- The Doc has several tabs, each with its own generator. Use the matching one:

| Part of the Doc | Payload built by | Written by |
| --- | --- | --- |
| Scope baseline tab | `python3 tools/scope_tab3.py --out <scratch>/tab3.md` | `tools/gdoc_tab3.py`, `tools/gdoc_scope_sync.py` |
| Schedule tab (2.18, 3.3) | `gdoc_schedule_tab.build()` | `tools/gdoc_schedule_tab.py` |
| Whole document, one tab only | `tools/gdoc.py` | `gdoc.py import-html` (new Doc) |

- **Never run `gdoc.py replace` on the team's Doc.** It re-imports the whole file and collapses a
  multi-tab Doc into one tab.
- Build and check the payload before pushing, because what reaches the Doc is what the generator
  emits. These need no credentials:

```bash
python3 tools/scope_tab3.py --out /tmp/tab3.md
PYTHONDONTWRITEBYTECODE=1 python3 -c "import sys; sys.path.insert(0, 'tools'); import gdoc_schedule_tab as g; print(g.build())" > /tmp/schedule-tab.md
python3 .claude/skills/pm/scripts/check_consistency.py /tmp/tab3.md
```

## 5. The three marking states

Every value in a form is in one of three states, and the Markdown shows which.

| State | How it is written | Example |
| --- | --- | --- |
| Known: from a project document or from you | Plain text | `700,000,000 VND` |
| Assumed, inferred or not yet confirmed | `<mark>...</mark>`, with the reason in the same cell if it fits | `courses of <mark>24 to 48 sessions</mark>` (charter 1.1.1) |
| Not known and not inferable | Empty cell, or `[TBD]` where an empty cell would look like an oversight | `[TBD]` |

Why:

- The course brief says to fill the form and leave unknown boxes empty or yellow. `<mark>` becomes the
  yellow highlight in the Google Doc.
- `CLAUDE.md` forbids guessed values. A form with hidden guesses costs the team a meeting to untangle;
  a form with marked guesses can be confirmed in one pass.
- `<mark>` is the only HTML allowed. It marks content, never a label or a heading.

An empty box is a real state, not a mistake: the project manager's name is empty in the charter on
purpose, because the sponsor appoints the PM at M0 (assumption 15).

## 6. House rules the reviewers enforce

These come from two review rounds on the team's Doc (60 findings). The consistency check catches the
ones marked "script".

| Rule | Write | Not | Caught by |
| --- | --- | --- | --- |
| One date style per document | `2 September 2026` | `02 September 2026`, `2 Sep 2026`, `2026-09-02` | script |
| Weekdays only if the whole table has them | `Mon 14 September 2026` in every row | a mix of weekday and plain dates | script (warning) |
| The 28,000,000 VND budget line is a contingency reserve | contingency reserve | `management reserve`, which is the sponsor's reserve outside the baseline; this project has none | script |
| Sponsor and customer are two people | Dr. Nguyễn Mạnh Hùng with sponsor wording; Đỗ Thị Bích Ngọc with customer or Director wording | "sponsor" beside the customer's name, or "owner" beside the sponsor's | script |
| No line breaks inside cells | `(1) ... (2) ... (3) ...` inline | `<br>`, which arrives in the Doc as literal text | script |
| Only `<mark>` as HTML | `<mark>` | any other tag or HTML entity | script |
| Nothing extra inside the printed form | explanations in the italic paragraph above the form | notes under a table, text under Approvals, an extra heading | partly (warning) |
| Printed title block labels | `**Project Title:**`, `**Date Prepared:**` (or `**Date:**` where printed) | `**Project:**`, `**Date prepared:**`, `**Source:**` | fidelity |
| No column the form does not print | 1.3 starts with Name | an added ID column on 1.3, 1.4, 2.14, 6.4 or bank 2 of 2.32, 2.36, 3.1 | fidelity |
| Ranges match the family's current end | `R1 to R12`, `F01 to F12` | `R1 to R10` after R12 exists | script (warning) |
| One ID, one text | the same wording for NFR02 everywhere | two meanings for one ID | script (warning) |
| `A` means acceptance criterion | `A01`, `assumption 18` | `A18` for an assumption | reading |
| Totals add up | lines sum to the Total row | a total typed by hand | script |
| Copied text stays copied | the charter's risk statement, word for word | a paraphrase | reading |
| No em dashes, no emoji | comma, semicolon, colon or full stop | em dash, en dash, emoji | script |
| Cite both page numbers | PDF page 141 (printed page 130) | "page 130" | reading |

The full list, with the reviewer threads behind each rule, is
`.claude/skills/pm/references/review-lessons.md`.

## 7. Audits and Google Doc comments

### Auditing

Ask for an audit when the documents are about to go to the Doc, or before a grading deadline. The skill
works as a reviewer and does not edit files unless you ask.

It runs, in order:

1. The scripts over the whole package: `check_consistency.py --audit` on every file together (`--audit`
   also reports a constant column that the text above it explains), `check_fidelity.py` on each form (with
   `--section` for a form inside a package, `--flattened` for the RTM), `check_schedule.py` on a 2.18 (it also compares the
   milestone names with the charter; `--explained hours` reports a mismatch that a pending 3.3 explains as a warning; a pending 3.3 never explains an order
   defect, so `--explained sequence=REASON` needs the reason quoted, and `break=REASON` too), `tools/check_scope.py`. Add `--report <file>` when one file is the deliverable. The mandatory scans of `audit-template.md` are each reported, a hit or a line under "Scans that found nothing": dates, `<br>`, a merged sponsor and customer, the reserve wording, an RTM whose Priority is one value throughout (a warning even when a sentence explains it), the same ID across Parts 1 and 1B.
2. Every lesson in `review-lessons.md`, recomputing derived figures from their assumptions.
3. Sequence: nothing used, accepted or signed before it exists; no dates inside a period the charter
   rules out. `check_schedule.py` finds a check before its subject, a closeout before its warranty or its milestone, a go-live
   before the UAT, a test before the build, a review before another package's work, a count in a task name or a dictionary sentence against its window,
   and work inside a break (an error when the charter says the break can absorb no overrun); the rest is read, by the recipe in `audit-template.md` (Used before it exists).
4. Load per person per week against the charter's allocation (`load_check.py docs/scope-package.en.md --limit
   MOB1=<hours> --leaves MOB1=YYYY-MM-DD`, plus `--charter`, `--holiday` and `--daily-limit`; `--schedule <2.18 file>` spreads the hours over a levelled schedule's rows;
   `--explained overload=REASON` makes an overload a warning that names its document; a finding under the default 40 hours says "limit assumed", and when the charter gives a part-time
   person no weekly figure the default hides an overload, so ask the sponsor; `python3 tools/level.py` for the levelled schedule).
5. A generated form or the push payload, when the Doc is involved (`references/push-audit.md`).

The report follows `.claude/skills/pm/references/audit-template.md`:

```text
## Errors        E1, E2, ...   a contradiction someone can show with two quotations
## Warnings      W1, W2, ...   a weak point a grader may raise
## Scans that found nothing    each scan run with zero hits, so the reader knows it was run
## What passed                 the other checks that found nothing
```

Each finding has a location (`file:line` and the section or form page), the quoted evidence, and the
fix or the decision it needs and who makes it.

Useful audit commands:

```bash
python3 .claude/skills/pm/scripts/check_consistency.py docs/charter-package.en.md docs/scope-package.en.md
python3 .claude/skills/pm/scripts/check_consistency.py docs/charter-package.en.md docs/scope-package.en.md --errors-only
python3 .claude/skills/pm/scripts/check_consistency.py docs/charter-package.en.md docs/scope-package.en.md --audit
python3 .claude/skills/pm/scripts/check_schedule.py docs/forms/2-18-project-schedule.en.md --charter docs/charter-package.en.md --scope docs/scope-package.en.md
python3 .claude/skills/pm/scripts/check_fidelity.py docs/scope-package.en.md 2.7 --section "Part 1:" --flattened
python3 .claude/skills/pm/scripts/load_check.py docs/scope-package.en.md --limit MOB1=20 --leaves MOB1=2026-12-18
python3 tools/check_scope.py
python3 tools/level.py
```

### Answering Doc comments

Ask, for example, `Answer the open comments on the team Doc` and give the Doc ID. The skill lists the
threads with the text each is anchored to, drafts replies, and shows you what would be posted before
anything is posted.

```bash
gdoc() { uv run --with google-api-python-client,google-auth-oauthlib,markdown tools/gdoc.py "$@"; }
gdoc comments --doc DOC_ID                                         # threads and anchored text
gdoc post --doc DOC_ID --review review/<date>-doc-review.json --dry-run
gdoc post --doc DOC_ID --review review/<date>-doc-review.json
```

How replies are written (`review-lessons.md` section 11):

1. Agree or disagree in the first word ("Đồng ý", "Đã bỏ", "Đã thêm").
2. Say what changed and where: section, cell, version.
3. Quote the new sentence in English when the source is English.
4. List the knock-on edits in other places.
5. When the request conflicts with a fixed constraint (budget, duration), name the constraint and the
   cost of the trade-off, and leave the decision to the team.
6. Reply in the reviewer's language.

`post` is idempotent: a reply whose first line is already on the Doc is skipped.

## 8. Deciding: asking what to do

The forms record decisions; they do not make them. When you ask what to do ("we are two weeks late",
"R5 happened", "the client wants a new function", "which form do I fill for this?"), the skill takes the
decision path and ends in the forms that record the decision.

```text
situation
  1. route it                  references/decisions.md (40 routing rows, 43 decisions), references/pmbok-<area>.md
  2. compute derived numbers   scripts/pm_calc.py
  3. list what else changes    scripts/form_graph.py --impact
  4. present                   the recommendation format of decisions.md section 5
  5. record (after you agree)  3.2 Decision Log; 3.3 Change Request then 3.4 Change Log when a baseline moves
```

### Example prompts

| Situation | Example prompt | What comes back |
| --- | --- | --- |
| Schedule slip | `The mobile application work (WBS 1.5.4, due for M5) is two weeks late. What are my options, which are allowed, and what do I update? I do not want an answer that just says the estimate was wrong.` | Crashing and fast tracking (PMBOK 6 section 6.5.2.6) with their trade-offs, what 2.18 already used, the reserve and authority limits from the charter, a change request to the sponsor, the forms to update |
| Earned value status | `BAC 700,000,000; PV 280,000,000; EV 252,000,000; AC 294,000,000 VND. Give me the status, a forecast at completion and what goes in form 4.4.` | CV, SV, CPI, SPI, three EACs and TCPI from `pm_calc.py evm`, the status words of PMBOK 6 Table 7-1, the 4.4 fields, the 5% escalation limit |
| A risk happened | `R5 has happened: the notification gateway is unstable and the price went up. What do we do, and what do I write in the register and the decision log? I do not know who owns it.` | The 11.5 strategies, contingency reserve within the charter limits, proposed 2.32 and 3.2 text, owner and scores left empty |
| Which form | `khach hang muon them chuc nang moi thi ghi vao dau?` | 3.3 then 3.4, the sponsor decides, 2.7 and the scope baseline 2.8 to 2.10 change only after approval, in Vietnamese |
| Where to record | `Where do I write down why we chose a second provider?` | 3.2 Decision Log, Comments carries the alternatives and the reason |

The same questions work in Vietnamese; the answer comes back in the language you asked in.

### What the answer contains

The recommendation format (`decisions.md` section 5) has eight parts: the situation with the document and
section each fact came from; the constraint check (which of scope, schedule, cost, quality, resources and
risk binds, which baselines an option touches, whether the project manager's authority covers it); an
options table (technique with citation, the book's trade-off or "not stated in the book", baseline effect);
one recommendation; the calculator output; what the team must decide and who decides; the forms to update
with the printed field; and the citations with both page numbers. Facts such as the 20,000,000 VND reserve
limit, the 5% variance limit or a milestone date are read from the charter and the packages each time; the
catalog does not store them. It keeps one list of the authority limits to read (per transaction, per reserve
use, forecast overrun percent and its base, a change in funding, which reserve and which risks may draw on
it) that the late-schedule, variance, forecast and reserve decisions all point to. A question such as "what do
I write" or "what do I tell the sponsor" is answered with the draft in the reply, not a file.

### The rules it keeps

These are the team's rules, repeated in `SKILL.md` and `decisions.md`.

- Every remedy is a technique PMBOK 6 or the Book of Forms names, with the trade-off the book states. If the
  book states none, the answer says "not stated in the book" and marks the choice as judgment.
- An estimate is never cut to fit a date or a fund.
- When scope, schedule, cost and quality cannot all hold, the route is a change request (3.3) to the sponsor.
- Contingency reserve (inside the cost baseline, for identified risks) is not management reserve (outside it). When the charter words the reserve otherwise than its budget line, the answer reports both wordings as a source error for the sponsor.
- A narrow question (one status figure, which form) gets a short answer with the three forms to write first; the full seven-part format is for a decision that moves a baseline or asks for options.
- An owner, a threshold, a score, a rate or a date is never invented; it is asked for or left empty.
- Nothing is written under `docs/` unless you ask.

### pm_calc.py: the numbers

Plain Python, no packages. Every result prints the page where the book prints its formula, PDF page and
printed page. `--json` gives machine-readable output.

| Subcommand | Computes | Where the book prints it |
| --- | --- | --- |
| `evm` | CV, SV, CPI, SPI, percent planned, earned and spent, three EACs, ETC, VAC, TCPI (toward the present-CPI EAC it equals the CPI and toward the budgeted-rate EAC it is 1, so those two carry no Table 7-1 words); `--threshold` and `--base` add the overrun as a percent of BAC, PV, EV or AC with the threshold's amount, and mark it within or beyond; `--bac` with `--threshold` alone prints the amount | PMBOK 6 section 7.4.2.2 and Table 7-1; Book of Forms 4.4. The percent is an outside aid: no book prints a percent variance |
| `pert` | Beta and triangular mean of three estimates | Book of Forms 2.17, 2.21; PMBOK 6 sections 6.4.2.4, 7.2.2.5 |
| `effort-to-duration` | Duration from effort, quantity, percent available and performance factor | Book of Forms 2.17, Table 2.16 |
| `analogous` | Estimate from a previous value and the ratio of sizes | Book of Forms 2.17, 2.21 |
| `bottom-up` | Cost as hours x rate plus material and the other parts | Book of Forms 2.21, Table 2.20 |
| `risk-score` | High, Medium or Low from probability and impact; `--matrix` prints the 2.35 grid | Book of Forms 2.34 Table 2.31, 2.35; PMBOK 6 Figure 11-5 |
| `emv` | Expected monetary value and a decision tree with `--option` | PMBOK 6 section 11.4.2.5, Figure 11-15 |
| `weighted-score` | Weighted criteria score and the winner | Book of Forms 2.39, Table 2.35 |
| `earned-schedule` | SV(t) = ES - AT, SPI(t) = ES / AT | PMBOK 6, Trends and Emerging Practices in Project Cost Management, printed page 233 (PDF page 272) |
| `crash` | Crashing options ranked by extra cost per day saved, and the cheapest ones that reach `--needed` days; critical activities only, with the team's own crashed durations and costs | PMBOK 6 section 6.5.2.6, printed page 215 (PDF page 254) defines crashing as the least incremental cost and prints no equation; labelled an outside arithmetic aid |
| `cpm` | Early and late dates, total and free float, the critical path, a `--deadline` (working days from day 1, or a date with `--start`), a `--slip` what-if; `--start` and `--holiday` turn working days into calendar dates and say whether a slip crosses a break | PMBOK 6 section 6.5.2.2 and Figure 6-16 describe the passes and print no equation; labelled an outside arithmetic aid |
| `velocity` | Velocity per iteration, the average, the iterations remaining | Agile Practice Guide section 5.4.1, printed page 64 (PDF page 874); the average and the forecast are outside aids |
| `cd3` | Items ranked by cost of delay divided by duration | Agile Practice Guide Table 5-1, printed page 59 (PDF page 869); the Guide prints the words and no units |
| `payback` | The first period in which the cumulative net benefit reaches the investment | PMBOK 6 names payback and prints no formula; labelled an outside arithmetic aid |
| `comms-channels` | n(n-1)/2 | Neither book prints it; labelled an outside arithmetic aid |
| `reserve` | Contingency remaining against the expected value of the open risks | PMBOK 6 section 11.7.2.1, printed page 456 (PDF page 495) names the comparison and prints no equation; labelled an outside arithmetic aid |
| `funding` | Funds released by tranche against cost to date | PMBOK 6 section 7.3.3.2, printed page 256 (PDF page 295), and Figure 7-9; labelled an outside arithmetic aid |
| `response-effectiveness` | (change in impact level) / (implementation cost) per response | PMBOK 6 section 11.5.2.8, printed page 446 (PDF page 485) |

```bash
python3 .claude/skills/pm/scripts/pm_calc.py evm --bac 700000000 --pv 280000000 --ev 252000000 --ac 294000000
```

```text
Variances and indexes (no assumption beyond the inputs)
  CV                                 -42000000  (over planned cost)  [1]
  SV                                 -28000000  (behind schedule)  [1]
  CPI                                0.8571  (over planned cost)  [2]
  SPI                                0.9  (behind schedule)  [2]
EAC at the present CPI
  EAC                                816666666.6667  [6]
      formula: EAC = BAC / CPI
      assumption: The cumulative CPI to date continues for all remaining work.
Sources
  [1] PMBOK 6 section 7.4.2.2, printed page 262 (PDF page 301); PMBOK 6 Table 7-1, printed page 267 (PDF page 306); ...
```

What the tool will not do:

- Where the books print no formula it says "not stated in the book": the beta standard deviation, a payback
  period, a percent variance. It does not supply one.
- It refuses inputs the formula cannot take (a zero BAC, a negative probability, `nan`) and says why; a zero
  AC or PV gives no CPI or SPI and the output says so. It does not substitute a value.
- It prints up to four decimals, unrounded. No book states a rounding rule; an index is reported as printed (a CPI of
  0.8621 is not shown as a flattering 0.86), with the Table 7-1 words, and money in whole VND, compared with a
  threshold in the unrounded form. A percent overrun is labelled an outside aid, with its base.
- Form 2.17's prose says a skilled resource is faster, while its printed equation divides by the factor.
  The tool follows the printed equation and example (150 hours of effort, 2 people, 75 percent, factor 0.8
  gives 125 hours) and prints a note about the disagreement. Tell the team which reading you use.
- Table 2.31 prints 80 percent in two probability bands; the tool refuses a bare 80% and asks for the level
  word.

### form_graph.py: what else changes

The 66 forms as a graph, built from the `receives_from`, `provides_to` and `alignment` lists in
`references/knowledge/`.

| Command | Prints |
| --- | --- |
| `form_graph.py 3.3` | Upstream, downstream and alignment partners of one form, what flows, and who declares each link |
| `form_graph.py --impact 2.9 2.10 --depth 1` | Documents to recheck when one or several forms change, ordered by distance, each marked in docs/ or not (or as a stand-in section: the charter holds the content of 1.2, 1.3, 2.6, 2.14 and 2.32, counted apart), with the number of files, and a line saying what the changed form receives from; the answer names every form listed, none dropped and none added; `--category` limits 3.3 to some Impacts of Change categories; without `--depth` it follows the links all the way down |
| `form_graph.py --order [--group Planning]` | A creation order in PMBOK process sequence (9.1 and 9.2 rank before 6.4, whose inputs they produce); the forms of the Executing, Monitoring and Controlling and Closing groups are listed apart, each tagged with the step of its first version and when it is final; a link from a later process to an earlier one is a revision input, and the cut edges are printed; 2.27, 2.39 and 4.8, which the book only aligns with a plan, and 4.3, 4.4, 4.6 and 4.7 take the plans and baselines they measure against as prerequisites, tagged as a skill mapping |
| `form_graph.py --check` | Links one form declares and the other does not |
| `form_graph.py --markdown [--out F]` | Prints the form graph; `--out` writes it (the committed copy is `references/form-graph.md`, and a test keeps it equal to the generated text) |

```text
$ python3 .claude/skills/pm/scripts/form_graph.py --impact 3.3 --depth 1 --category Cost
Recheck when 3.3 Change Request changes (6 documents, within 1 edge):
  1  2.2 Change Management Plan  [not in docs]  (3.3 provides to it)
  1  2.20 Cost Estimates  [not in docs]  (3.3 Impacts of Change: Cost; skill mapping, not book text)
  1  2.21 Cost Estimating Worksheet  [not in docs]  (3.3 Impacts of Change: Cost; skill mapping, not book text)
  1  2.22 Cost Baseline  [not in docs]  (3.3 Impacts of Change: Cost; skill mapping, not book text)
  1  3.4 Change Log  [not in docs]  (3.3 provides to it)
  1  Change control board (external)  [external, no form]  (3.3 provides to it)

0 of 5 forms exist in docs/, in 0 files.
Nothing to compare: none of these 5 forms exists in docs/. Say so, list them as forms to create or update later, and do not paste the rows as if they were documents to recheck.
Changed form lives in: forms/3-3-change-request.en.md (3.3)
```

Without `--category`, 3.3 also lists the forms of the other categories (Scope, Quality, Requirements,
Schedule, Stakeholder Impact, Project Documents, and resources and risk), and the forms whose results may become
a 3.3 (2.18, 2.32, 2.40, 3.6, 4.3, 4.4, 4.6) point back to it. Those rows are tagged `skill mapping, not book text`: the
book lists the categories on 3.3 (Book of Forms form 3.3, PDF pages 181 to 182 (printed pages 170 to 171)),
and the mapping from a category to the forms of the matching knowledge area is the skill's.

Read it with care:

- The scope baseline is the one composite: 2.8, 2.9 and 2.10 together (Book of Forms form 2.9, PDF page 60
  (printed page 49)). A form that receives from or aligns with the scope baseline is listed against all
  three. The schedule baseline and the project budget are external names because the book names no form for
  them.
- The book usually says that a form provides to another, not which fields flow. The text on each link says
  so; do not turn it into a field mapping.
- `--check` reports 340 one-sided links (117 `provides_to`, 68 `receives_from`, 155 alignment). Most are a
  form that lists a consumer which does not list it back. That is the book being silent on one side, or a
  gap in the knowledge files, not an error in the project.
- `--order` cuts every link that runs from a form of a later PMBOK 6 process to a form of an earlier one
  (process group, then chapter and section, then form number), so 1.3 comes before 2.4 and 2.16 before
  2.18. The risk register 2.32, the risk report 2.33, the issue log 3.1 and the decision log 3.2 are
  created at the start of the project (Book of Forms form 2.32, PDF page 140 (printed page 129); 2.33, PDF
  page 142 (printed page 131); 3.1, PDF page 176 (printed page 165); 3.2, PDF page 179 (printed page
  168)), so their incoming links are revision inputs. The order is the skill's reading of the recorded
  links, not the book's.

### Limits

- The decision catalog and the PMBOK notes were written from the two books and checked in two passes.
  PMBOK page numbers in the decision sections were verified against the PDF. Claims that rest on the Book
  of Forms were checked for the page offset only, apart from the links of forms 2.10, 2.32 and 3.3 and the
  formulas of forms 2.16, 2.17, 2.21, 2.34, 2.35, 2.39, 4.3 and 4.4, which were read on their pages. Treat a
  citation as a pointer and open the page before you quote it to a reviewer.
- The catalog merges roughly 100 area decisions into 43 cross-area entries. A situation that fits no row is
  answered from the closest entry, and the answer says so.
- The skill recommends. The sponsor decides what is beyond the project manager's authority, and the charter
  names no change control board.

## 9. All 66 forms

Kind decides the Markdown shape (section 4). "In repo" names where a filled version already exists.

| Form | Name | Kind | Project data it needs | In repo |
| --- | --- | --- | --- | --- |
| 1.1 | Project Charter | fields | Purpose, description, boundaries, deliverables, requirements, overall risk, objectives and success criteria, milestones, preapproved budget, stakeholders, exit criteria, PM authority, sponsor | charter Part 2B |
| 1.2 | Assumption Log | log | Assumptions 1 to 19 and the constraints, with category, responsible party, due date, actions, status | |
| 1.3 | Stakeholder Register | log | Each stakeholder's name, position or role, contact, requirements, expectations, classification | |
| 1.4 | Stakeholder Analysis | log | Each stakeholder or role with interest, influence and attitude | |
| 2.1 | Project Management Plan | fields | Life cycle phases, activities and deliverables, phase reviews with entry and exit criteria, development approach per deliverable, subsidiary plans, variance thresholds, baseline management | |
| 2.2 | Change Management Plan | fields | Change approach, what counts as a schedule, budget, scope or document change, change control board, request process | |
| 2.3 | Project Roadmap | chart | Phases with start and finish dates, major milestones | |
| 2.4 | Scope Management Plan | fields | How the WBS and dictionary are built and maintained, deliverable acceptance, scope and requirements integration | |
| 2.5 | Requirements Management Plan | fields | How requirements are collected, analysed, categorised, prioritised, traced, tracked, reported, validated and placed under configuration management | |
| 2.6 | Requirements Documentation | log | Requirements with stakeholder, category, priority, acceptance criteria, test, phase or release | |
| 2.7 | Requirements Traceability Matrix | matrix | Requirement ID, text, source, priority, category; business objective, deliverable, verification, validation; business against technical requirements on page 2 | scope Part 1, 1B |
| 2.8 | Project Scope Statement | fields | Scope description, deliverables, acceptance criteria, exclusions, constraints, assumptions | charter Part 1 |
| 2.9 | Work Breakdown Structure | outline | Deliverables, control accounts and work packages with codes, in work order | scope Part 2 |
| 2.10 | WBS Dictionary | fields | Per work package: description, assumptions, milestones and due dates, activities with resource, hours, rate, material, cost, quality and acceptance criteria | scope Part 3 |
| 2.11 | Schedule Management Plan | fields | Method, tool, accuracy, units, variance thresholds, reporting, update rules | |
| 2.12 | Activity List | log | Activities per work package with ID and description of work | |
| 2.13 | Activity Attributes | fields | One activity: predecessors and successors with relationship and lead or lag, resources, skills, effort type, location, imposed dates, assumptions | |
| 2.14 | Milestone List | log | Milestones M0 to M7 with description and type | |
| 2.15 | Network Diagram | diagram | Activities with predecessors, relationship type (FS, SS, FF, SF), lead or lag | |
| 2.16 | Duration Estimates | log | Per activity: effort hours, duration estimate | |
| 2.17 | Duration Estimating Worksheet | log | Parametric, analogous and three-point inputs per activity | |
| 2.18 | Project Schedule | chart | Activities with ID, WBS code, name, start, finish; milestones | `docs/forms/2-18-project-schedule.en.md` |
| 2.19 | Cost Management Plan | fields | Units, precision, accuracy, control thresholds, performance measurement rules, reporting | |
| 2.20 | Cost Estimates (prints as Activity Cost Estimates) | log | Per WBS ID: resource, labor and physical cost, reserve, estimate, method, basis, range, confidence | |
| 2.21 | Cost Estimating Worksheet | log | Parametric, analogous, three-point and bottom-up cost inputs | |
| 2.22 | Cost Baseline | chart | Cumulative planned value per period, from the schedule and the cost estimates | |
| 2.23 | Quality Management Plan | fields | Standards, objectives with metrics, quality roles, deliverables and processes under review, QA and QC approach | |
| 2.24 | Quality Metrics | log | Item, metric, measurement method (from A01 to A12 and the NFRs) | |
| 2.25 | Responsibility Assignment Matrix | matrix | Work packages against people (PM, DEV1 to DEV3, QA1, MOB1) with R, A, C, I | |
| 2.26 | Resource Management Plan | fields | Roles with number, skill, acquisition and release; responsibilities and authority; structure; training; recognition; physical resources | |
| 2.27 | Team Charter | fields | Values, meeting, communication, decision and conflict rules, team signatures | |
| 2.28 | Resource Requirements | log | Per ID: resource, quantity, assumptions | |
| 2.29 | Resource Breakdown Structure | outline | Resources by category: people, equipment, materials, supplies | |
| 2.30 | Communications Management Plan | fields | Per stakeholder: information, method, timing, sender; assumptions, constraints, glossary | |
| 2.31 | Risk Management Plan | fields | Strategy, method, roles, categories, risk funding, contingency protocols, tolerances, probability and impact definitions | |
| 2.32 | Risk Register | log | Risks R1 to R12 with owner, probability, impact on scope, quality, schedule and cost, score, response, revised values | |
| 2.33 | Risk Report | fields | Executive summary, overall risk status and drivers, counts of risks by probability and impact, metrics | |
| 2.34 | Probability and Impact Assessment (prints as Probability and Impact Risk Rating) | matrix | Very High to Very Low definitions for each objective and for probability, rating thresholds | |
| 2.35 | Probability and Impact Matrix | matrix | Which probability and impact cells the team treats as high, medium, low | |
| 2.36 | Risk Data Sheet | log | One risk in depth: cause, scores, responses, secondary and residual risk, contingency plan, funds, time, fallback | |
| 2.37 | Procurement Management Plan | fields | Integration with scope, schedule and risk, procurement timing, metrics, roles, assumptions, jurisdiction and currency, independent estimates | |
| 2.38 | Procurement Strategy | fields | Delivery method, contract type, incentive criteria, procurement life cycle | |
| 2.39 | Source Selection Criteria | log | Criteria with weights and ratings per candidate | |
| 2.40 | Stakeholder Engagement Plan | fields | Current and desired engagement per stakeholder, pending changes, relationships, approach | |
| 3.1 | Issue Log | log | Issues with type, description, priority, impact, responsible party, status, resolution date and resolution | |
| 3.2 | Decision Log | log | Decisions with category, responsible party, date | |
| 3.3 | Change Request | fields | Requestor, category, description, justification, impact on scope, quality, requirements, cost, schedule and stakeholders, disposition | `docs/forms/3-3-change-request.en.md` |
| 3.4 | Change Log | log | Changes with category, requestor, submission date, status, disposition | |
| 3.5 | Lessons Learned Register | log | Lessons with category, trigger, responsible party | |
| 3.6 | Quality Audit | fields | Auditor, audit date, area audited, good practices, areas for improvement, defects with actions | |
| 3.7 | Team Performance Assessment | fields | Ratings and comments on technical performance and interpersonal competency | |
| 4.1 | Team Member Status Report | fields | One person's planned, done and missed activities, funds, variances, next period | |
| 4.2 | Project Status Report | fields | Period accomplishments, variances and their impact on milestones and budget, next period, risks, issues, changes | |
| 4.3 | Variance Analysis | fields | Planned against actual for schedule, cost and quality, root cause, response | |
| 4.4 | Earned Value Analysis (prints as Earned Value Analysis Report) | fields | BAC, PV, EV, AC per period; SV, CV, SPI, CPI; root causes and impact | |
| 4.5 | Risk Audit | fields | Risk events and responses that occurred, whether the risk process was followed | |
| 4.6 | Contractor Status Report | fields | Vendor's scope, quality, schedule and cost performance, forecast, claims, risks | |
| 4.7 | Procurement Audit | fields | Vendor performance, whether the procurement process was followed | |
| 4.8 | Contract Closeout Report (prints as Contract Closeout) | fields | Vendor performance, contract changes and disputes, completion and final payment dates | |
| 4.9 | Product Acceptance Form (prints as Formal Acceptance Form) | log | Requirements with acceptance criteria, validation method, status, sign-off | |
| 5.1 | Lessons Learned Summary | fields | What worked and what to improve, area by area, at project end | |
| 5.2 | Project or Phase Closeout (prints as Project Closeout) | fields | Objectives against results for scope, quality, time, cost; benefits; business needs; risks and issues | |
| 6.1 | Product Vision | narrative | Who the product is for, the needs, how it meets them, why customers buy it | |
| 6.2 | Product Backlog | log | Items with summary, priority, story, status | |
| 6.3 | Release Plan | chart | Release goal, sprints against teams | |
| 6.4 | Retrospective | log | Start, stop, keep, more, less | |

Page ranges for every form are in `.claude/skills/pm/references/forms-index.md`. The exact printed
labels of any form: `python3 .claude/skills/pm/scripts/check_fidelity.py --list <form>`.

## 10. Command cheat sheet

Run from the repo root. `S=.claude/skills/pm/scripts` shortens the lines below.

```bash
S=.claude/skills/pm/scripts

# Look up a form
python3 $S/extract_form.py 2.32 --fields                 # printed labels, no PDF needed
python3 $S/extract_form.py 2.32                          # element table and blank form text from the PDF
python3 $S/extract_form.py 2.32 --alignment --tailoring  # what it must agree with, how to tailor it
python3 $S/extract_form.py 2.32 --prose                  # the whole description
python3 $S/extract_form.py 2.32 --knowledge              # field guidance, sources, consumers, decisions; no PDF needed
python3 $S/check_fidelity.py --list 2.32                 # expected labels in Markdown shape

# Decide
python3 $S/pm_calc.py evm --bac <BAC> --pv <PV> --ev <EV> --ac <AC>      # add --json for machine output
python3 $S/pm_calc.py pert --o 20 --m 25 --p 36
python3 $S/pm_calc.py risk-score --probability high --impact very-high
python3 $S/pm_calc.py evm --bac 700 --pv 280 --ev 252 --ac 294 --threshold 5 --base bac pv   # overrun as a percent, within or beyond
python3 $S/pm_calc.py cpm --activity A=5 --activity B=3 --link A,B --slip A=4 --start 2027-01-25 --holiday 2027-02-06:2027-02-14
python3 $S/pm_calc.py reserve --contingency 28 --used 5 --risk R5=0.3:12
python3 $S/pm_calc.py evm --bac 700 --threshold 5                        # the amount a percent threshold stands for
python3 $S/pm_calc.py crash --option A 10 7 30 --option B 8 6 12 --needed 4   # crashing options by extra cost per day saved
python3 $S/pm_calc.py cpm --activity A=5 --activity B=3 --link A,B --start 2027-01-25 --deadline 2027-02-05   # a date deadline needs --start
python3 $S/pm_calc.py --help                                             # all eighteen subcommands
python3 $S/form_graph.py 3.3                             # sources, consumers, alignment partners
python3 $S/form_graph.py --impact 2.9 --depth 1          # what to recheck when 2.9 changes
python3 $S/form_graph.py --order --group Planning        # creation order from the recorded links
python3 $S/form_graph.py --check                         # one-sided links in the knowledge files
python3 $S/form_graph.py --markdown --out .claude/skills/pm/references/form-graph.md   # regenerate the committed copy

# Scaffold
python3 $S/new_form.py 2.32                              # print, writes nothing
python3 $S/new_form.py 2.32 --docs                       # write docs/forms/2-32-risk-register.en.md
python3 $S/new_form.py 2.32 --rows 12 --out /tmp/r.md    # more rows, other path
python3 $S/new_form.py 2.32 --docs --force               # overwrite
python3 $S/new_form.py 4.2 --out /tmp/reports/ --dated 2026-10-19   # a dated copy in a directory, never docs/
python3 $S/risk_actions.py docs/scope-package.en.md      # the Actions cell of 2.32 for each risk

# Check
python3 $S/check_fidelity.py docs/forms/<file>.md <form>
python3 $S/check_fidelity.py docs/scope-package.en.md 2.7 --section "Part 1:" --flattened
python3 $S/check_fidelity.py docs/scope-package.en.md 2.7 --section "Part 1B" --page 2 --flattened
python3 $S/check_pages.py <reply>.md                     # every page number has its printed or PDF partner; a section with no page warns
python3 $S/load_check.py docs/scope-package.en.md --limit MOB1=20 --leaves MOB1=2026-12-18
python3 $S/load_check.py docs/scope-package.en.md --charter docs/charter-package.en.md --daily-limit 8
python3 $S/load_check.py docs/scope-package.en.md --schedule docs/forms/2-18-project-schedule.en.md --limit MOB1=20   # the levelled 2.18's rows
python3 $S/check_consistency.py docs/forms/<file>.md docs/charter-package.en.md docs/scope-package.en.md --report docs/forms/<file>.md
python3 $S/check_consistency.py docs/charter-package.en.md docs/scope-package.en.md --errors-only
python3 $S/check_consistency.py charter scope --group --today 2026-10-15   # one line per check; Date Prepared against a day
python3 tools/check_scope.py
python3 tools/level.py

# Render
uv run --with python-docx $S/md_to_docx.py docs/forms/<file>.md
uv run --with python-docx $S/md_to_docx.py docs/forms/<file>.md -o <out>.docx

# Google Doc payloads (no credentials needed)
python3 tools/scope_tab3.py --out /tmp/tab3.md
PYTHONDONTWRITEBYTECODE=1 python3 -c "import sys; sys.path.insert(0, 'tools'); import gdoc_schedule_tab as g; print(g.build())" > /tmp/schedule-tab.md

# Tests
uv run --with pytest --with python-docx pytest -q .claude/skills/pm/scripts
python3 -m unittest discover -s .claude/skills/pm/scripts    # without uv, needs python-docx installed
python3 -m unittest tools.test_check_scope
```

Exit codes: `0` clean, `1` a failing finding, `2` a usage error (for example a missing file).

## 11. Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `uv: command not found` | uv is not installed | `brew install uv`, or `curl -LsSf https://astral.sh/uv/install.sh \| sh`. Without uv: `python3 -m venv .venv && .venv/bin/pip install python-docx pytest`, then use `.venv/bin/python` (`.venv/` is git-ignored) |
| `FileNotFoundError: ... 'pdftotext'` | poppler is not installed | macOS `brew install poppler`; Ubuntu or WSL `sudo apt install poppler-utils`. Meanwhile `--fields` works without it |
| `A_Project_Managers_Book_of_Forms.pdf not found ...; pass --pdf` | Run outside the repo, or the PDF is missing | `cd` to the repo root, or add `--pdf <path>` |
| `several forms match 'risk'` | The name matches more than one form | Use the number, for example `2.32` |
| `unknown form or document: 9.9` (exit 2) from `form_graph.py` | The argument is neither a form number nor a name in the graph | Use a number from section 9, or an external name as the book writes it, such as `"Scope baseline"` |
| `form_graph.py --impact 2.9` prints about a hundred documents | Without `--depth` it follows every link downstream, and the graph is dense | Add `--depth 1` or `--depth 2` |
| `pm_calc.py` exits 2 with `error:` | The formula cannot take the input: a zero BAC, a probability outside 0 to 100%, a bare `80%` in Table 2.31, `nan` | Read the message; it names the input and why. Give the missing figure or the level word |
| A figure shows `not stated in the book` | The books print no formula for it (beta standard deviation, percent variance; payback and the critical path passes are outside aids) | Decide the method with the team and record it in 3.2; do not cite the book for it |
| `no knowledge file for form ...` from `extract_form.py --knowledge` | The number is wrong or the file is missing | Use `references/knowledge/<number>.json`; all 66 forms have one |
| `... exists; pass --force to overwrite it` | `new_form.py` will not overwrite | `--out <other path>`, or `--force` if you mean it |
| `tools/gdoc_edit.py not found; run this from inside the repo` | `md_to_docx.py` run from elsewhere | Run from the repo root |
| The skill does not start | Claude Code opened outside the repo, or the request did not look like a PM task | Open Claude Code at the repo root, type `/pm <form>` |

### Reading a failing fidelity check

`check_fidelity.py` on `.claude/skills/pm/scripts/fixtures/fidelity/broken-2-32.md`, a real earlier
attempt, shortened:

```text
2.32 Risk Register, broken-2-32.md lines 1 to 37
12/22 printed labels present in printed order
missing (9):
  page 1, table, bank 1: Impact: Scope (written as 'Impact Scope' on line 9)
  page 1, table, bank 2: Status
out of printed order (1):
  page 1, table, bank 1: Probability (line 9)
unprinted labels (9), reported only:
  line 5: Source
  line 9: Impact Scope (printed as 'Impact: Scope')
```

- **missing**: a printed label is not there. "written as" means it is there with the wrong spelling;
  rename it. No hint means it is absent; add it in its printed place.
- **out of printed order**: present, but in the wrong position; move it.
- **unprinted labels**: something the form does not print, such as `**Source:**`. Remove it, or name it
  as a tailoring in the italic paragraph above the form. These do not fail the check.

### Reading a failing consistency check

Each line is `LEVEL file:line [check] message`. A real example:

```text
WARNING docs/forms/3-3-change-request.en.md:34 [date-style] this table column mixes date styles: plain 1 (first line 34), weekday 2 (first line 34)
0 error(s), 1 warning(s) in 3 file(s); reporting on docs/forms/3-3-change-request.en.md, 24 finding(s) already in the context files not shown
```

| Check name | Meaning |
| --- | --- |
| `date`, `date-style` | A date not in `2 September 2026` style, or mixed styles in one column |
| `range` | A range such as `R1 to R10` that stops short of the family's current end |
| `role-merge` | Sponsor and customer wording mixed |
| `term` | A word from the "Never write" table in `house-style.md` |
| `html`, `em-dash`, `emoji` | Markup or characters that do not survive the Doc or break the house rules |
| `mark-on-label` | A label or heading highlighted |
| `total` | A Total row that does not equal its lines |
| `uniform-column` | Every row holds the same value, so the column says nothing |
| `id-conflict` | One ID with two different texts |
| `section-ref` | A reference to a section that does not exist in the deliverable |
| `approvals` | A signature block that is not the printed one |
| `form-note` | Text inside the printed form that the form does not print |
| `note-length` | An italic paragraph above a form (wrapped lines count as one paragraph) runs past about 150 words |
| `date-prepared` | With `--today`: a Date Prepared after that day (error) or before it (warning to confirm the content was last checked then) |
| `stale-m0` | The project manager's appointment tied to M0 or an earlier date, in a document prepared after M0 |
| `table-rule` | A `---` line directly under a table row, which the Doc generator turns into a stray cell |

- Errors fail the run; warnings do not. Every `range` warning must be fixed or explained, since it is
  the check that found `R1 to R10`.
- With `--report`, findings that were already in the charter or scope package are counted at the end
  and not shown. The sources do carry some (abbreviated dates in the charter, for example); they are a
  separate job, not a reason your form fails.
- A script finding is a lead. Open the line before acting on it.

## 12. Improving the skill

### Layout

| Path | What to change there |
| --- | --- |
| `.claude/skills/pm/SKILL.md` | The form workflow and the decision path Claude follows (kept under 450 lines) |
| `references/decisions.md` | The decision catalog: routing table, 43 decisions, change control path, recommendation format |
| `references/pmbok-<area>.md` | One PMBOK 6 note per knowledge area, and `pmbok-agile.md`; the form-to-note table is in `SKILL.md` |
| `references/knowledge/<form>.json` | What goes in each field, sources, consumers, alignment, decisions; read through `extract_form.py --knowledge`. `form_graph.py` is built from it |
| `references/book-structure.md`, `references/form-graph.md` | How the book is organised; the generated form map (regenerate with `form_graph.py --markdown --out references/form-graph.md`) |
| `references/review-lessons.md` | What reviewers catch, and how to check for it |
| `references/house-style.md` | Marking rules, dates, the "Never write" table, where facts live |
| `references/rendering.md` | How each kind of form becomes Markdown |
| `references/forms-index.md` | The 66 forms, pages, kinds, printed titles |
| `references/fields/<form>.json` | Printed labels per form; fix here if a label is wrong |
| `references/audit-template.md`, `references/push-audit.md` | Shape of an audit report; auditing a generated form (regenerate into a scratch copy) and the payload pushed to the Doc |
| `references/book-counts.json` | Rows the books print in a named table, for the `count` check of `check_consistency.py` |
| `scripts/*.py`, `scripts/test_*.py`, `scripts/fixtures/` | Scripts, tests and test inputs, including `pm_calc.py`, `form_graph.py`, `check_schedule.py`, `load_check.py`, `check_pages.py` and `risk_actions.py` |
| `evals/evals.json` | Test prompts with gradable assertions |

### Add a review lesson

When a reviewer flags something new on the Doc:

1. Add it to the matching section of `references/review-lessons.md` (1 people and roles, 2 IDs and
   ranges, 3 numbers, 4 scope, 5 money, 6 success criteria, 7 layout, 8 markup, 9 dates, 10
   completeness, 11 replies). Say what went wrong, why a reviewer cares, how to check it, and cite the
   thread or audit ID.
2. A forbidden word: add a row to the "Never write | Write instead | Why" table in
   `references/house-style.md`. The consistency check reads that table, so no code change is needed.
3. A mechanical rule: add a check to `scripts/check_consistency.py`, mark the lesson **[script]**, and
   add fixtures in `scripts/fixtures/consistency/`: `fnNN-*.md` must be flagged, `fpNN-*.md` must not.
   Register them in `scripts/test_check_consistency.py`.
4. A wrong printed label: fix `references/fields/<form>.json` after looking at the blank page
   (`Read` the PDF page, or `pdftotext -layout -f N -l N A_Project_Managers_Book_of_Forms.pdf -`).

### Run the tests

```bash
uv run --with pytest --with python-docx pytest -q .claude/skills/pm/scripts
```

Expected today: `481 passed` and the subtests. `test_pm_skill.py` also checks that `SKILL.md` stays under 450 lines, that its description fits 1,024 characters, and that the evals are well formed; `test_pm_calc.py` reproduces the worked examples the books print. Run them after any change under `.claude/skills/pm/`.

### Run the evals

`evals/evals.json` holds nine prompts with assertions: an audit of the charter and scope package, a
1.3 Stakeholder Register from a Vietnamese prompt, a 2.32 Risk Register, a held-out audit of the 2.18
schedule, a blank 4.2 template, and four decision prompts (a schedule slip on the mobile work, an earned
value status with the figures given, a response to R5, and a Vietnamese question about where a new
function is recorded). To run them, ask Claude Code:

```text
Use the skill-creator skill to run the pm evals in .claude/skills/pm/evals/evals.json
and write the results to .claude/skills/pm-workspace/iteration-<N>/.
```

Earlier runs are in `.claude/skills/pm-workspace/iteration-1/` and `iteration-2/`: one folder per eval
with the outputs, and `benchmark.md` with the pass rate against the previous skill. When you add an
eval, give it an `id`, `eval_name`, `prompt`, `expected_output`, `files` and `assertions`, and write
each assertion so someone can check it from the output alone.

### Add or fix decision knowledge

- A PMBOK or Book of Forms fact in a decision: change the matching `references/pmbok-<area>.md` and
  `references/decisions.md`, with the page in both numberings, then open the page to check it.
- A form's links or field guidance: change `references/knowledge/<form>.json`. Run
  `form_graph.py --check` to see whether the other side lists the link, and `form_graph.py --markdown --out references/form-graph.md`
  to regenerate it (without `--out` it prints, and a test fails when the committed copy is stale).
- A formula: change `scripts/pm_calc.py` when a book prints it, and add a test with the book's worked example.
  Arithmetic the books only name or draw (payback, the critical path passes) may be added as an outside arithmetic
  aid, labelled so in its output and its docstring. Otherwise the tool must say "not stated in the book".

### Before you commit

- Tests pass.
- No em dashes, en dashes or emoji (`CLAUDE.md`).
- No AI attribution in commit messages.
- No Doc IDs or other hardcoded values in files.
