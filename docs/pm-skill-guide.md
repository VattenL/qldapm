# PM skill guide

How to use the `pm` skill in Claude Code to produce, check and audit forms from *A Project Manager's
Book of Forms*, 3rd edition, for this project. Written for teammates who know the course and the book
but have not read the skill's internals.

Vietnamese version: [`pm-skill-guide.vi.md`](pm-skill-guide.vi.md).

Every command below was run in this repo on 1 October 2026 from the repo root, except the `gdoc` commands that need the team's Google credentials.

## Contents

1. What the skill does and does not do
2. Before you start
3. Asking for a form
4. From request to deliverable
5. The three marking states
6. House rules the reviewers enforce
7. Audits and Google Doc comments
8. All 66 forms
9. Command cheat sheet
10. Troubleshooting
11. Improving the skill

## 1. What the skill does and does not do

The skill lives in `.claude/skills/pm/`. Claude Code loads it on its own when you ask for a form, cite
a form number, or ask for an audit of the documents in `docs/`.

| It does | It does not |
| --- | --- |
| Find the right form among the 66, by number or by name, and ask when a name matches several | Recall field lists from memory; every label comes from `references/fields/<form>.json`, transcribed from the blank pages |
| Scaffold the form in Markdown with the printed title block, labels, page headings, grouped headers and banks, in printed order | Add fields, columns or notes the printed form does not carry |
| Fill it from `docs/charter-package.en.md`, `docs/scope-package.en.md` and the forms in `docs/forms/` | Invent project values; anything assumed is highlighted, anything unknown stays empty or `[TBD]` |
| Run the fidelity and consistency checks and report what they find | Pick a winner silently when two project documents disagree; it reports the conflict for the team to decide |
| Render a form to `.docx` that looks like the book | Push to the team's Google Doc unless you ask, and never without the Doc ID you give it |
| Audit the package and draft replies to reviewer comments | Fix files while auditing, unless you ask for the fixes |

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

You can also call the skill directly with a slash command:

```text
/pm 2.32                      fill form 2.32 from the project documents
/pm risk register             same, by name
/pm 4.2 --blank               the empty form, no project values
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
  2. read the printed form     extract_form.py --fields, plus the PDF page for charts
  3. gather project facts      docs/charter-package.en.md, docs/scope-package.en.md, docs/forms/
  4. scaffold, then fill       new_form.py, then Markdown edits
  5. check                     check_fidelity.py, check_consistency.py, tools/check_scope.py, reading
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
python3 .claude/skills/pm/scripts/new_form.py 2.32 --out -        # print the blank form
python3 .claude/skills/pm/scripts/new_form.py 2.32                # write docs/forms/2-32-risk-register.en.md
python3 .claude/skills/pm/scripts/new_form.py 2.32 --rows 12      # 12 empty rows per register table
python3 .claude/skills/pm/scripts/new_form.py 2.32 --force        # overwrite an existing file
```

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

A blank template (`--blank`) is this scaffold with nothing added: no names, dates, amounts or IDs.

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
| `check_fidelity.py` | Does the Markdown carry every printed label, spelled as printed, in printed order? | Missing or out-of-order labels. Unprinted labels are listed but do not fail |
| `check_consistency.py --report <form>` | Does the new form agree with the charter and scope package? | Any error the new form contributes. Old errors in the sources are counted, not shown |
| `tools/check_scope.py` | Does the scope package still roll up to 4,400 hours and 700,000,000 VND? | Any of its checks |

A clean form prints, for example:

```text
2.32 Risk Register, 2-32-risk-register.en.md lines 1 to 18
22/22 printed labels present in printed order
```

After the scripts, the skill reads the documents the book says this form must agree with (its
Alignment section) and reports contradictions. Section 10 explains how to read a failing check.

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
python3 -c "import sys; sys.path.insert(0, 'tools'); import gdoc_schedule_tab as g; print(g.build())" > /tmp/schedule-tab.md
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

1. The scripts over the whole package: `check_consistency.py` on every file together,
   `check_fidelity.py` on each form (with `--section` for a form inside a package),
   `tools/check_scope.py`.
2. Every lesson in `review-lessons.md`, recomputing derived figures from their assumptions.
3. Sequence: nothing used, accepted or signed before it exists; no dates inside a period the charter
   rules out.
4. Load per person per week against the charter's allocation (`python3 tools/level.py` for the
   levelled schedule).
5. The push payload, when the Doc is involved.

The report follows `.claude/skills/pm/references/audit-template.md`:

```text
## Errors        E1, E2, ...   a contradiction someone can show with two quotations
## Warnings      W1, W2, ...   a weak point a grader may raise
## What passed                 the checks that found nothing
```

Each finding has a location (`file:line` and the section or form page), the quoted evidence, and the
fix or the decision it needs and who makes it.

Useful audit commands:

```bash
python3 .claude/skills/pm/scripts/check_consistency.py docs/charter-package.en.md docs/scope-package.en.md
python3 .claude/skills/pm/scripts/check_consistency.py docs/charter-package.en.md docs/scope-package.en.md --errors-only
python3 .claude/skills/pm/scripts/check_fidelity.py docs/scope-package.en.md 2.7 --section "Part 1:"
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

## 8. All 66 forms

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

## 9. Command cheat sheet

Run from the repo root. `S=.claude/skills/pm/scripts` shortens the lines below.

```bash
S=.claude/skills/pm/scripts

# Look up a form
python3 $S/extract_form.py 2.32 --fields                 # printed labels, no PDF needed
python3 $S/extract_form.py 2.32                          # element table and blank form text from the PDF
python3 $S/extract_form.py 2.32 --alignment --tailoring  # what it must agree with, how to tailor it
python3 $S/extract_form.py 2.32 --prose                  # the whole description
python3 $S/check_fidelity.py --list 2.32                 # expected labels in Markdown shape

# Scaffold
python3 $S/new_form.py 2.32 --out -                      # print
python3 $S/new_form.py 2.32                              # write docs/forms/2-32-risk-register.en.md
python3 $S/new_form.py 2.32 --rows 12 --out /tmp/r.md    # more rows, other path
python3 $S/new_form.py 2.32 --force                      # overwrite

# Check
python3 $S/check_fidelity.py docs/forms/<file>.md <form>
python3 $S/check_fidelity.py docs/scope-package.en.md 2.7 --section "Part 1:"
python3 $S/check_consistency.py docs/forms/<file>.md docs/charter-package.en.md docs/scope-package.en.md --report docs/forms/<file>.md
python3 $S/check_consistency.py docs/charter-package.en.md docs/scope-package.en.md --errors-only
python3 tools/check_scope.py
python3 tools/level.py

# Render
uv run --with python-docx $S/md_to_docx.py docs/forms/<file>.md
uv run --with python-docx $S/md_to_docx.py docs/forms/<file>.md -o <out>.docx

# Google Doc payloads (no credentials needed)
python3 tools/scope_tab3.py --out /tmp/tab3.md
python3 -c "import sys; sys.path.insert(0, 'tools'); import gdoc_schedule_tab as g; print(g.build())" > /tmp/schedule-tab.md

# Tests
uv run --with pytest --with python-docx pytest -q .claude/skills/pm/scripts
python3 -m unittest discover -s .claude/skills/pm/scripts    # without uv, needs python-docx installed
python3 -m unittest tools.test_check_scope
```

Exit codes: `0` clean, `1` a failing finding, `2` a usage error (for example a missing file).

## 10. Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `uv: command not found` | uv is not installed | `brew install uv`, or `curl -LsSf https://astral.sh/uv/install.sh \| sh`. Without uv: `python3 -m venv .venv && .venv/bin/pip install python-docx pytest`, then use `.venv/bin/python` (`.venv/` is git-ignored) |
| `FileNotFoundError: ... 'pdftotext'` | poppler is not installed | macOS `brew install poppler`; Ubuntu or WSL `sudo apt install poppler-utils`. Meanwhile `--fields` works without it |
| `A_Project_Managers_Book_of_Forms.pdf not found ...; pass --pdf` | Run outside the repo, or the PDF is missing | `cd` to the repo root, or add `--pdf <path>` |
| `several forms match 'risk'` | The name matches more than one form | Use the number, for example `2.32` |
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

- Errors fail the run; warnings do not. Every `range` warning must be fixed or explained, since it is
  the check that found `R1 to R10`.
- With `--report`, findings that were already in the charter or scope package are counted at the end
  and not shown. The sources do carry some (abbreviated dates in the charter, for example); they are a
  separate job, not a reason your form fails.
- A script finding is a lead. Open the line before acting on it.

## 11. Improving the skill

### Layout

| Path | What to change there |
| --- | --- |
| `.claude/skills/pm/SKILL.md` | The workflow Claude follows |
| `references/review-lessons.md` | What reviewers catch, and how to check for it |
| `references/house-style.md` | Marking rules, dates, the "Never write" table, where facts live |
| `references/rendering.md` | How each kind of form becomes Markdown |
| `references/forms-index.md` | The 66 forms, pages, kinds, printed titles |
| `references/fields/<form>.json` | Printed labels per form; fix here if a label is wrong |
| `references/audit-template.md` | Shape of an audit report |
| `scripts/*.py`, `scripts/test_*.py`, `scripts/fixtures/` | Scripts, tests and test inputs |
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

Expected today: `142 passed`. Run them after any change under `.claude/skills/pm/`.

### Run the evals

`evals/evals.json` holds five prompts with assertions: an audit of the charter and scope package, a
1.3 Stakeholder Register from a Vietnamese prompt, a 2.32 Risk Register, a held-out audit of the 2.18
schedule, and a blank 4.2 template. To run them, ask Claude Code:

```text
Use the skill-creator skill to run the pm evals in .claude/skills/pm/evals/evals.json
and write the results to .claude/skills/pm-workspace/iteration-<N>/.
```

Earlier runs are in `.claude/skills/pm-workspace/iteration-1/` and `iteration-2/`: one folder per eval
with the outputs, and `benchmark.md` with the pass rate against the previous skill. When you add an
eval, give it an `id`, `eval_name`, `prompt`, `expected_output`, `files` and `assertions`, and write
each assertion so someone can check it from the output alone.

### Before you commit

- Tests pass.
- No em dashes, en dashes or emoji (`CLAUDE.md`).
- No AI attribution in commit messages.
- No Doc IDs or other hardcoded values in files.
