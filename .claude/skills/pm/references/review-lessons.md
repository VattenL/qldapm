# What the team's reviewers catch

Two review rounds on this project's documents produced 60 findings:
`review/2026-09-16-doc-review.md` (26 reviewer threads, 9 new findings) and
`review/2026-09-24-doc-audit.md` (11 errors, 14 warnings). Almost none of them
were about missing fields. They were about a document that disagrees with
itself, with its sibling documents, or with the printed form, in ways a
reader notices and a generator does not.

Later rounds added sections 12 to 20 and extended the others: the format audit
of 29 September (`review/2026-09-29-format-audit.md`), the schedule renumbering
review of 30 September (`review/2026-09-30-schedule-v2.md`), the reviewer
threads on the Doc up to 5 November (the risk register threads of Đại Dũng
Nguyễn and Vatten above all), the print layout audit of 14 October, and the
team's whole-Doc audit of 8 November (`review/2026-11-08-doc-audit.json`, 33
errors, 94 warnings, 57 notes that survived two skeptics; cited here by key,
V2.10 or G1.13). The 8 November audit is the team's own machine audit held to
the reviewers' standard, so where a human reviewer raised the same point the
human is named first. Who the reviewers are and what each checks: section 20.

Read this file before generating a form that reuses project facts, and before
any audit. Each lesson says what went wrong, why a reviewer cares, and how to
check it. `scripts/check_consistency.py` automates the ones marked **[script]**;
the rest need reading. The lessons are patterns to check for, not a record of
what has been fixed: several of the examples quoted here are still in the
sources, so an audit reports them again if it finds them.

## Contents

1. People and roles
2. IDs, ranges and cross-references
3. Numbers that must add up
4. Scope: product versus project
5. Money: reserves, tranches, bases
6. Measurable success criteria
7. Form layout fidelity
8. Markup that does not survive the Doc
9. Dates
10. Completeness of the package
11. How to answer a reviewer
12. Marking: yellow, empty, green
13. Versioning and visible change
14. Doc layout and print
15. Risk register writing and scoring (2.31, 2.32, 2.36)
16. Schedule logic (2.18 and the 3.3 that moves it)
17. WBS and dictionary structure (2.9, 2.10)
18. Pending change requests across the Doc
19. Length and audience
20. The reviewers and what each checks

## 1. People and roles, and the stakeholder registers (1.3, 1.4)

**Sponsor and customer are two different people.** Sponsor Dr. Nguyễn Mạnh Hùng
funds, approves and accepts; customer Đỗ Thị Bích Ngọc owns the center and the
business need (assumption 16). The old charter tab merged them four times:
"owner and Center Director" beside the sponsor's name, "sponsor of the learning
center" beside the customer's, a Customer column holding the sponsor's name in
Approvals, and an RTM Source of "Center Director, sponsor". Each one made a
reviewer stop, because authority to accept deliverables depends on who is who.
(Threads AAACG0ldth4, AAACG0ldth0; New 4, New 5; audit E10.)

- Every mention of the sponsor's name carries sponsor wording only; every
  mention of the customer's name carries customer or Director wording only.
  **[script]**
- A stakeholder table lists them on two rows with separate roles.

**Stakeholders include every party a risk, a budget line or an assumption
depends on.** R12 depends on Apple and Google, whose store review can reject
the app, and budget line 2 pays Apple Developer, Google Play and a push
service, yet neither of the charter's two key stakeholder lists names any of
them (audit W5). So a stakeholder register (1.3, 1.4) is built from the
charter's stakeholder list *plus* every external party named in the risk
register, the budget lines and the assumptions, each on its own row. Copying
the charter's list alone repeats the gap. **[script]** warns when a party in
the External party table of `house-style.md` is named elsewhere but has no row.

**One person, one name, everywhere.** The old tab named the PM "Ngô Hải Đăng" on
page 1 and "Nguyễn Văn A" in the stakeholder table. Now the PM is deliberately
unnamed (assumption 15: the sponsor appoints the PM at M0), so the name is
empty in all three places: the Project Manager box of 1.1, the signature
block, and the stakeholder row. The row itself stays. A register whose first
column is Name (1.3, 1.4) writes the position alone, `Project Manager`, in the
Name cell, since Table 1.3 lets a position stand in for a name; it never writes
a person's name and puts no description in the cell (the next rule: a field holds
the value). That rule wins over any "name to be assigned" wording in a cell. The
sentence "name to be assigned by the sponsor at M0" belongs in the italic paragraph
and the question list only, and only for a Date Prepared on or before M0 (14
September 2026); `check_consistency.py` warns (`stale-m0`) when it appears in a
document prepared after M0. After M0 write that no project document records the
appointment, mark it, and list it as a question to the sponsor; never invent a
name. The safe sentence, which `check_consistency.py` does not read as stale: "No project document records who the project
manager is, so the name is left empty and listed as a question to the sponsor." (it has no M0, no date and no "to be assigned"). (Thread AAACG0ldth8; New 1.) Keep the italic paragraph to what a reader needs
(the source copy, what is empty and why): a few sentences, not the 280 words of the
first runs; the questions to the user go in the reply.

**A field holds the value, not a description of it.** Reviewers struck
"- owner and Director of the learning center" after a sponsor's name and "- sponsor
of the learning center: 3 branches, 1,200 students, 35 teachers" after a
customer's. Facts about the center belong in 1.1.1, not repeated in a name box.
A role clause is acceptable only where it disambiguates (the Customer box keeps
"owner and Director" to tell her apart from the sponsor).

**A real person's name used for a fictional role is a question, not a fix.**
The customer carries the lecturer's name from the cover (New 8, audit W12).
Flag it to the team; do not rename on your own.

**Every deliverable and every gate has one approver, and every tab names the
same one.** The 8 November audit found three signatories across the
deliverables and none for D7 and D11 (V2.38; already 24 Sep W5), and three
readings of who decides UAT entry: the charter and tab 6 say the project
manager, the dictionary says the sponsor and the QA engineer agree it (V7.6).
Check: for D1 to D11 and each gate (UAT entry, go-live, closeout), collect
every "approves", "signs", "accepted by" in every tab; expect one role per
item, and that role present in the 2.23 roles table and in 2.28.

**A role is written in words with its code in brackets, one spelling per role,
taken from 2.28.** `Project manager (PM)`, `QA engineer (QA1)`, `Mobile
developer (MOB1)`. Vatten on the risk register, 5 November: "Viết chữ vào"
(write words, not codes); Đại Dũng Nguyễn, 4 November, item 6: "Thống nhất
cách gọi chức năng" (one way of naming each function). The center's IT person
was both "System Administrator" and "Center IT administrator" (V1.49). Check:
a bare resource code in a prose or register cell, or a second name for one
role, in any tab.

## 2. IDs, ranges and cross-references

The project runs on ID families: F01-F12 functions, D1-D11 deliverables,
A01-A12 acceptance criteria, R1-R12 risks, M0-M7 milestones, assumptions 1-19,
BR/FR/NFR requirements, WBS codes 1.x.y.z.

**A range must match the family's current extent.** The old tab said "Risks R1 to
R10" when the register ran to R12, and "F01 to F11" after F12 was added. When a
family grows, every range that names its end must move with it. **[script]**

**A reference must land on something that exists in the same deliverable.** The
form cited "section 2A" and "section 1.3" in a Doc that had no 2A (New 3). If
the target is not in the document being delivered, either bring it in or drop
the reference. **[script]** for `section N` references.

**One ID, one text.** The RTM gave NFR02 one meaning on page 1 and another on page
2, and BR03 two different Sources (audit W7). An ID repeated across tables must
carry the same label and source. **[script]**

**One ID, one scope.** D4 read "F06 to F11" in section 1.2 while M4, Key
Deliverables and the WBS said F06 to F12 (audit E4). When the definition of an
ID changes, grep for every place it is spelled out.

**Codes in work order.** WBS codes are read as a sequence; 1.4.1.4 after 1.4.1.3
is fine, but 1.4.1.4 holding F02 after 1.4.1.3 holding F03 reads as an append,
and so does a testing package numbered after its own acceptance (audit W8).
Number by the order the work happens, and put each package under the phase
that does it (UAT execution belongs to Quality Assurance and Test, owned by the
business owners who execute it, not to Handover under QA1). The rule the team
adopted on 30 September (`review/2026-09-30-schedule-v2.md`, lines 12 to 15):
inside a control account, order by start date, then finish date of Due Dates,
then F number, testing before defect fixing. Where every date of a sheet is
the same (14 of 24 control-account sheets, G1.30) the dates give no order, so
the rule must be stated another way.

**One code, one name, in every tab.** Six of the twelve function names in the
RTM differed from the charter's (V3.53); M6 had four names (V1.46) and M5 and
M6 differed between the two pages of 2.18 (V4.8). Check: map each F, D, M and
R code to the charter's wording and grep every tab for other wordings.

**When codes change, every tab moves in the same change.** On 15 October tabs
3, 4 and the dictionary summary still used the old WBS codes while tab 5 used
the 30 September renumbering. Build the code-to-title map from the WBS and
flag any tab whose code for a title differs. Only review records (`review/`,
this file) keep old codes, because they are records. A renumbering keeps the
same rows: compare the set of (title, hours, cost) before and after, and run
`tools/check_scope.py`.

**Every cited ID exists at the level cited.** Activity IDs cited in tabs 5 and
7 (1.1.1.1-A4) were not rows of the schedule, which stopped at A3 (V1.14); a
control account (1.8.1) was cited as a work package (V8.17); one ID column
held three naming systems (V8.22). Check each `x.y.z.w-An` against 2.18 and
each code against its level in 2.9.

**A reference into the draft tab is a dangling reference.** Thẻ 2 is marked
"bản nháp, không thuộc bài nộp" (draft, not part of the submission). Tab 4
pointed to "section 4.2", a 3.3 held only in Thẻ 2 (V1.10, V4.24, errors);
tab 5 cited a schedule of 1 March 2027 that is in no tab (V6.44). Every
"section N" or "form X" a submitted tab cites resolves to a heading in a
submitted tab.

**A reading note describes what the Doc holds.** Tab 3 said its section 3.3
was quoted from the 78 package sheets, which are not in the Doc, and section
3.3 was a byte-identical copy of the "dict rút gọn" tab (V1.17, V3.1, V5.1,
errors). Counts and sources a note claims must exist in the Doc, and no
section is a copy of another tab.

**A field another tab relies on is present.** Tab 3's method said every work
package names a single accountable owner, the dictionary said the owner field
is not used, and tabs 7 and 8 rest on that field (V3.30, V8.1, errors). For
each rule or column defined as "the X of form Y", find X in the Doc.

**Objectives carry codes the RTM can trace to.** Vatten, 24 September, on the
RTM's Business Objective: "Nên thêm bảng đánh mã vào charter" (add a coding
table to the charter), then "Cho ngắn" (keep it short). The RTM cites "Quality:
A04 met", an acceptance criterion, as its business objective (24 Sep W7; V3.7
still open on 8 November).

## 3. Numbers that must add up

**Totals equal the sum of their lines.** The budget table has six lines that must
total 700,000,000 VND and 100%. The dictionary's 78 sheets must roll up to 4,400
hours and 539,000,000 VND of labor. **[script]** checks every Markdown table
that has a Total row; `tools/check_scope.py` checks the scope package roll-up
and must pass after any change to it.

**A derived number is recomputed from its stated inputs.** The business case
applied a 70% app activation to all guardians, while assumption 18 says 80% own
a smartphone and 70% *of those* activate, which is 56%. That moved payback from
year 5 to year 6 (audit E1). When a figure depends on an assumption, redo the
arithmetic from the assumption as written, and quote the result in every place
it appears (2A, form page 1, RTM BR05).

**Load stays inside what the plan claims.** "Part-time" 2.5 person-months packed
into 9 weeks is 44 hours a week (audit E2); a developer said to leave after M5
still had hours to 5 January. Check hours per week against the claimed
allocation, and the last dated work against the stated end.

**Stated counts match the list.** "Fourteen elements of Table 1.1" when the table
lists 13 (audit E11); "one of the two exceptions" when the text said four
(E7). Count the thing before writing the number, and name which list you
counted. The book has two lists for the charter and they differ: the bullet
list at the start of section 1.1 (PDF page 13, printed page 2) has 14 items and
includes Project approval requirements, between Key stakeholder list and
Project exit criteria; Table 1.1 (PDF pages 14 to 15, printed pages 3 to 4) has 13 rows and the
printed form (PDF pages 16 to 19, printed pages 5 to 8) has no such field, only the Approvals
signature block. So the charter's 14th section in 2A does come from the book.
Audit E11 is half wrong for this reason: "Table 1.1 lists 13 elements" is
right, but "Project approval requirements ... comes from PMBOK 6 section
4.1.3.1, not from the book" is not. The correct wording is "13 elements in
Table 1.1; Project approval requirements is in the book's section 1.1 list
(printed page 2) but not in Table 1.1 or on the form".

**Business-case arithmetic is rechecked with a stated method.** `pm_calc.py
payback --investment I --net ...` gives the first period whose cumulative net
benefit reaches the investment (an outside arithmetic aid: PMBOK 6 names payback
and prints no equation). For anything else write a scratch script, list its
inputs and where each came from in the audit's Method line, and show the
arithmetic in the finding.

**A rule that is cited is stated.** "Exceptions to the sizing rule" in a Doc that
never states the 8 to 80 hour rule (audit E7). If a section relies on a rule,
the rule is in the same deliverable.

**Every row's arithmetic holds, not only the totals.** For 39 of 43 labor rows
of the cost estimate, printed hours times printed rate did not give the
printed total, up to 11,000 VND off (V6.11). Check hours x rate per row, and
say once whether amounts use rounded hours.

**A figure said to come from a document is in that document, and a figure
derived from a highlighted input is highlighted.** Tab 3 called 4,400 labor
hours "given by the charter"; the charter gives 27.5 person-months, and 4,400
rests on the tab's own highlighted 160 hours per person-month (V3.15).

**The project manager's cost authority fits inside the reserve, or the route
for the excess is stated.** A 5% variance on 700,000,000 VND is 35,000,000,
more than the 28,000,000 contingency reserve, with no further funding (V2.17).
`pm_calc.py reserve` and `evm --threshold` print both amounts.

**The dictionary's cost equals the cost of the levelled plan.** When the
leveller divides an activity between two people at different rates, the
package cost changes: PM 24 h x 162,500 plus QA1 24 h x 93,750 is 6,150,000,
1,650,000 less for the same 48 hours; 51 of 78 packages were divided (V5.4).

**Every figure of a change request can be reproduced from the Doc.** The 32
person-weeks and the PM's 124 hours of the schedule request could not be
reproduced (G3.2), nor the crashing figures (G3.7). A request once cited
1,723,938,000 VND as "the estimate of 7 October", which was 1,450,419,000 and
1,735,946,000, and printed a literal "99%%" (commit 9cd5f64). Recompute each
figure from tabs in the submission and grep for format-string debris.

## 4. Scope: product versus project

Reviewers separated the two twice (threads AAACG0ldtig, AAACG0ldtik):

- **Exclusions** come in two lists: what the product will not do (preschool,
  offline app, staff functions on mobile) and what the project will not do
  (pay subscriptions beyond 12 months, clean the source data, staff the
  center, operate after handover).
- **Deliverables** are marked by audience: for the customer (D1-D9, D11) or
  internal (D10 plus the PM plan, schedule, status reports, risk register,
  test plan).
- **Business reason versus project work.** Opening a fourth branch is why the
  center wants the system; it is not work this project does. Say both in one
  sentence rather than letting the reason read as scope (thread AAACG0ldtiE).
- **Boundaries are as detailed as possible**, both Included and Excluded, and
  name the user population (learners aged 6 to 18) so a reader can decide an
  edge case from the text (thread AAACG0ldtiI).
- **What the WBS tests is a requirement.** The RTM had no row for the
  fourteen exception and failure cases of charter section 1.1.5, though the
  WBS and the test packages treat them as requirements with their own tests
  (V3.11). Two acceptance criteria required behaviour no function described
  (V2.59). Check that each criterion A01 to A12 traces to a function that
  describes the behaviour, and each tested case to an RTM row.

## 5. Money: reserves, tranches, bases

**Contingency reserve and management reserve are different things.** A
contingency reserve sits inside the cost baseline, is drawn by the PM for
identified risks through change control, and here is 28,000,000 VND (budget line
6). A management reserve belongs to the sponsor, sits outside the baseline, and
this project has none. Using the wrong term in one cell (the Cost success
criterion still says "management reserve use reported monthly") contradicts the
budget. (Thread AAACG0ldtjM; audit W2.)

**Every budget line carries its basis.** "Infrastructure 70,000,000" drew "must be
proved later" (thread AAACG0ldtj4). Each line gets a unit price and quantity or
a stated rule, highlighted as assumed, and a re-estimate point (M1).

**A reserve is derived, not asserted.** 4% with no link to R1-R12 is a warning
(audit W2). If the risks carry no probability or impact, say the reserve is a
percentage allowance and when it will be derived.

**Payment tranches follow acceptance and should not leave closeout unfunded.**
20/25/30/25 paid by M6 leaves nothing held for M7 or warranty (audit W3). Tie
each tranche to a signed acceptance record and check what is still owed after
the last deliverable.

**Warranty is costed.** Six months after go-live, the first inside the project,
months 2 to 6 on budget line 5 (thread AAACG0ldtiY).

**What the customer supplies is not also costed.** The charter says the center
supplies the cloud server, the gateway and the store accounts, and that the
project budget pays for them (V1.3; V8.10 for the production server). For each
resource the center provides, confirm no budget line pays for it in the same
period, or that the split is stated.

**A unit price is the published price, with its source; an item with no
published price keeps the charter's allowance, highlighted** (Vatten's cost
estimate, commit 6056c43; V6.10 a domain price that is not the published one
and a pessimistic figure with no source). An allowance is removed only for a
reason a source states (V6.14).

**A gap between estimate and budget goes to the sponsor as a change request,
under the technique's book name.** The charter is not edited to match an
estimate, and estimates are not cut to fit (memory rule; `decisions.md`).
Funding limit reconciliation (PMBOK 6 section 7.3.2.5) levels spending by
period (printed page 253 (PDF page 292)); presenting a scope reduction under
that name is a misnamed technique (V6.5).

## 6. Measurable success criteria

- **A pass mark of 100% hands the customer a veto.** Reviewers settled on 99% of
  an agreed UAT test set, the remainder being defects that do not affect
  operation, with "acceptance cannot be withheld for scope outside the
  baseline" (threads AAACG0ldtjY, AAACG0ldtjo). When a threshold changes,
  change it everywhere it appears: A01, the Other row, exit criterion 2 and the
  UAT failure path.
- **Key deliverables signed off** is the headline scope criterion, not a count
  of functions.
- **The first risk is failing the objective itself** (R1: the system does not
  meet A01-A12 so the center cannot operate on it). Each risk is typed Product
  or Project (thread AAACG0ldti0).
- **Criterion and assumption say the same thing.** "70% of guardians with a
  smartphone by closeout" against "within the first term" (audit W4). Pick one
  window.
- **A column where every row holds the same value carries no information.**
  All 31 requirements "Must have" makes Priority useless (audit W7). Either
  grade them or say once, above the table, why they are uniform. **[script]**
  flags a uniform column unless a sentence in the text above the table, in
  the same part, names the value together with the column or with "every" or
  "all" ("Every requirement is Must have: ..."). An audit that finds the
  reason stated is still a warning when reviewing documents (`check_consistency.py
  --audit` reports it): a reason does not make a constant column informative.
  Name the reason's line in the warning and say what would close it (the form's
  own rule makes the value constant, or the team grades the rows). Only a
  column the printed form defines as constant passes quietly.
- **A criterion copied into another form keeps every clause.** The go-live rule
  of the quality plan left out A01's clause that no defect of any severity may
  be open in the tuition, payment or teaching-hour path (V7.15); the exit
  criterion and the UAT failure path left out the same clause (V2.62). Diff
  each copy against the charter, clause by clause.
- **Each quality objective says how it is measured and which deliverable row
  checks it.** Three of the 14 objectives of 2.23 (A05, A08, A11) had neither
  (V7.17).

### Open on 15 October 2026

The disagreements found on 14 November 2026 are in `project.md` section 7; the greps
below still apply and are rerun with it.

This list is a starting point, not a verdict: re-run each grep before reporting, and drop an item that no
longer matches, since the sources are edited between audits. Report the item, do not pick a winner (the
sponsor decides). A line that is not here is not thereby fixed: walk sections 1 to 6 as well.

Contradictions in the charter package (`docs/charter-package.en.md`):

- Reserve wording: `grep -n -i "management reserve" docs/charter-package.en.md` finds form 2B's Cost row
  (line 464, "management reserve use reported monthly"); 2A's Cost row says "reserve use reported monthly"
  and budget line 6 is a contingency reserve.
- R12 against the Time criterion: `grep -n "^| R12 \|no milestone more than" docs/charter-package.en.md`. R12
  says go-live does not depend on the app and an app slip of up to two weeks after M6 is absorbed without moving
  M6; the Time criterion says no milestone more than 1 week late and M6 is named "app live in both stores".
  Three statements, two readings.
- "All fourteen elements of Table 1.1": `grep -n -i "fourteen" docs/charter-package.en.md` (lines 28, 34, 227);
  Table 1.1 has 13 rows (see "Stated counts" above).
- Part-time load: the charter gives the mobile developer 2.5 person-months and no weekly figure
  (`grep -n -i "person-month" docs/charter-package.en.md`; `grep -n -i "a week" docs/charter-package.en.md` finds
  only the Academic Manager's and the Accountant's hours). `load_check.py` therefore judges the person against 40 unless
  told otherwise; ask for the limit (SKILL.md, load per person).
- Tranches: the charter releases 20%, 25%, 30% and 25% by M6 (`grep -n -i "tranche" docs/charter-package.en.md`);
  read what is held for M7 and the warranty (section 5).

Contradictions in the scope package (`docs/scope-package.en.md`) and between the packages:

- Team size: `grep -n "Team size" docs/*.md`. The scope package states that the brief assumes 4 staff while the charter is
  baselined at 5 plus a part-time developer; it says so itself, so report it as an explained difference.
- WBS order: `grep -n "^#### 1.4.1.[34] " docs/scope-package.en.md` finds 1.4.1.3 F03 before 1.4.1.4 F02 (section 2, Codes in work order).
- A rule directly under a table row: `grep -n -B1 "^---$" docs/scope-package.en.md` and look for a table row on the line above (line 210,
  under the RTM Part 1B table); `check_consistency.py` reports it as `table-rule`, and the Doc generator turns it into a stray cell.
- The appointment of the project manager: `check_consistency.py` warns `stale-m0` for sentences that tie it to M0 or to a date on or before M0 in
  a document prepared after M0.

## 7. Form layout fidelity

Reviewer instruction on the charter: "Chỉnh giống y hệt form", make it identical
to the form (thread AAACG0ldthw). What that meant in practice:

- **Printed title bar and printed page count**: `PROJECT CHARTER`, a page break
  per page, "Page N of 4".
- **Printed pairing.** Page 1 of 1.1 prints Project Sponsor beside Date Prepared
  and Project Manager beside Project Customer. Form 2.10 prints Work Package
  Name beside Code of Accounts, Description of Work beside Assumptions and
  Constraints, Milestones beside Due Dates, and a two-tier Labor / Material
  header (audit W9). The Markdown keeps a vertical Field | Content table in
  printed reading order; `scripts/md_to_docx.py` applies the side-by-side
  pairing when it renders the .docx, from the `pairs` list in
  `references/fields/<form>.json`. `tools/gdoc_form.py` does not pair fields:
  in the Google Doc it draws title bars, column widths, landscape pages and
  group header rows, the last only when the caller passes them (as
  `tools/gdoc_tab3.py` does for 2.7). Do not invent a pairing the form does
  not print.
- **Printed group headers are kept, not flattened into new labels.** 2.32
  prints Impact over Scope, Quality, Schedule and Cost in both banks; 2.7 prints
  Requirement Information and Relationship Traceability; 2.10 prints Labor and
  Material. Two runs of the skill flattened 2.32 into two different invented
  spellings ("Impact Scope", "Impact: Scope"). Use the one convention in
  `rendering.md`: `Impact: Scope`. That is the Markdown rule only. In the Doc
  the header prints as the book prints it, two rows, the group cell merged
  across its columns and every other label merged down both rows. Đại Dũng
  Nguyễn, 4 November, on the flattened 2.32: "Sai cả 2 table (không tồn tại
  trong book of form)" (both tables are wrong, they are not in the Book of
  Forms). `tools/gdoc_risk_tab.py` splits `Impact: Scope` into the two rows
  (commit 0d2f000); a Doc payload that prints `Impact: Scope` as one label is a
  defect (29 Sep E4 for Labor and Material of 2.10; V9.9).
- **No column the form does not print, unless it is named as a tailoring.**
  A register gets an ID column only if its printed form has one, or the italic
  paragraph says which form the column joins and why. An early run added
  `ID` / `S01`... to 1.3 with no reason, which added a field. The team's 1.3
  and 1.4 of 14 November carry S01 to S19 as the key that matches each row of
  1.3 to its row of 1.4, and say so; the bank 2 ID of 2.32 was added at
  Vatten's request of 5 November and is named the same way. Bank 2 of 3.1
  prints no ID either. An unexplained extra column is still a defect.
- **No `Field | Content` header row in the Doc.** The top and bottom field
  tables of 2.10 opened with a `Field | Content` row the form does not print
  (29 Sep E4, E1).
- **Each printed page and each sheet carries its title bar and page counter,
  styled one way in every tab.** No 2.10 sheet had the WBS DICTIONARY bar or
  "Page 1 of 1" (29 Sep E4); the RTM omitted the counters the WBS and the
  dictionary carry (V3.45); "Page N of M" was a different object in each tab
  (V1.63).
- **Page breaks fall at the printed page boundaries.** The charter tab had one
  page break, inside page 2 (29 Sep E3, still open on 8 November as V2.9). List
  the break positions in `doc.json` against the `page N of M` markers.
- **Form 2.9 prints its codes with the book's closing period and no
  annotations** (`1.1.`, not `1.1`; no "(major deliverable, D1, M1)" or
  "(control account)"; 29 Sep W6; Vatten's commit 6615c31). A one-cell bordered
  box around the outline still read as a table to Vatten ("Lệch format, không
  phải là bảng, viết lại thành các gạch đầu dòng", 24 September), and the
  box came back in his own commit: the request and the print pull in two
  directions, so say in the note why the box is the printed form, and leave
  the choice to the team (V3.57).
- **The 1.1 objectives box in the Doc prints each label (Scope:, Time:, Cost:,
  Other:) as a line above its two-cell row, and printed labels keep their
  colon** (29 Sep W3, W4). The Markdown keeps the grid of `rendering.md`.
- **A form the book prints landscape sits in a landscape section** (2.7, 2.10,
  2.18, 2.28, 2.32, 1.3; G6.1 for 2.28 in a portrait section).
- **Headings nest without jumps, one numbered scheme in every tab** (V1.64: H2
  to H4 jumps, tab 8 alone with no numbered H3; 29 Sep W1).
- **The title block uses the printed labels.** `Project Title` and `Date
  Prepared` on most forms, `Date` on 2.4, 2.5, 2.11, 2.33, 2.37 and 2.38,
  `Project Name` alone on 6.3, and nothing on 2.3 and 2.18. `Project:` and
  `Date prepared:` are not printed labels.
- **Exactly the printed signature blocks.** 1.1 Approvals has two columns,
  Project Manager and Sponsor or Originator, each with Signature, Name, Date.
  A third Customer column is wrong (New 5). **[script]**
- **The printed shape of the form, not a convenient one.** Form 2.9 prints an
  indented numbered outline (1 Project, 1.1 Major Deliverable, 1.1.1 Control
  Account, 1.1.1.1 Work Package). A Code | Element | Type table is a different
  form (audit E8).
- **Nothing on the form that the form does not print.** Explanatory notes under
  the milestone table and under Approvals, and an extra "PROJECT CHARTER" H3,
  were flagged (audit W6). Put explanations in a reading-convention paragraph
  before the form, or in Part 2A, not inside it.
- **Highlight marks content, never a label.** "Project Customer", "Overall
  Project Risk" and a heading were highlighted as if assumed (audit W6).
  **[script]**
- **Heading levels are uniform across pages**: every printed page marker is the
  same `####` heading; every field label is a bold table cell.
- **Tailoring is allowed but must be named.** The book permits a dictionary at
  control account level (printed page 52 (PDF page 63)). The team first kept
  the full 78-sheet form because the brief asks for forms filled "as much as
  possible"; Vatten found it "Lệch hẳn format" and "quá dài" (24 September), and
  the Doc now carries 24 control-account sheets ("dict rút gọn", commit
  3c66b64). Whichever way you go, say it once, and say what ID and Activity
  hold in the summary (package codes and names, not activity IDs; V5.5) and
  name any row the form does not print, such as a Control account total
  (V5.14). Nothing in the Doc may still cite the package sheets (V1.17).

## 8. Markup that does not survive the Doc

- `<br>` inside a table cell arrived in the Google Doc as literal text, 23
  times (audit E6). Two tags are converted: `<mark>` (yellow, uncertain) by
  every writer, and `<ins>` (green, changed in the current version) by
  `tools/gdoc_risk_tab.py` only. Any other tag, or `<ins>` in a form whose
  writer does not convert it, arrives as text. **[script]**
- A table cell cannot hold a bulleted list in Markdown. When a reviewer asks for
  bullets in a cell (thread AAACG0ldtiw), write numbered items inline, `(1) ...
  (2) ...`, in the Markdown. In the Doc each item must start its own line: the
  closing pass of the tab writers breaks the line before each item
  (`number_lines`, commit 576673c). The reply to AAACG0ldtiw promised "bullet
  thật trong ô" (real bullets in the cell) and the cell was still one paragraph
  on 8 November (V2.10, error): check a promise in the live Doc, not in the
  source.

## 9. Dates

One format per document, day without a leading zero, month in full, year:
`2 September 2026`. Reviewers flagged `02 September 2026`, `5 Jan 2027` and
`Mon 14 Sep 2026` mixed with `14 September 2026` (New 7, audit W11). A weekday
prefix is acceptable only if every date in that table carries one; the scope
package uses `Mon 14 September 2026` consistently in its dictionary. **[script]**
flags leading zeros, abbreviated months, and mixed styles within a file.

**Date Prepared moves with the content.** The RTM and WBS were dated 23
September while the WBS carried the 30 September numbering (V3.18); form 1.1
said 2 September while tab 8 cited the charter "as committed on 16 September"
(V1.38). A section dated before a change it carries is stale, and the "as
committed on" dates of all tabs agree.

**A response tied to a milestone already passed is stale.** R17 said
"re-estimate at M1" when M1 (2 October) had passed (the team's own finding in
the 8 November reply). For each "at Mn", "before Mn" in a register, compare
Mn's date with Date Prepared. `stale-m0` covers only the project manager's
appointment.

**Due Dates of 2.10 hold milestone dates, and a recurring activity is not a
milestone.** Due Dates held work windows (24 Sep W9); three "milestones" of the
governance sheet were weekly reports and reviews dated to the project end
(V5.9).

## 10. Completeness of the package

- **Every part the brief asks for is in the delivered file.** The Prompt Log
  (requirement 4) was missing from the live Doc, which would score zero (New 2,
  audit E5). Check `requirement.md` and `docs/wbs_req.md` against the headings
  of the deliverable.
- **Assumptions list is complete.** The Doc stopped at 15 while the source had 19
  (New 9). New assumptions introduced by a change (16 sponsor and customer are
  distinct, 17 rate basis, 18 app adoption, 19 SMS and hosting costs) must be
  added in the same change.
- **What reaches the Doc is what the generator emits, so audit the generator's
  output.** Tab 3 of the Doc was 108 paragraphs behind
  `docs/scope-package.en.md` (audit E9) and showed the WBS as a table (E8).
  The cause was not hand editing: the version of `tools/scope_tab3.py` that
  built the tab said in its own docstring that it "drops everything before
  Part 1" and "turns the WBS outline into a table". That lost the decomposition
  method, so the sizing rule the Doc cites was never stated in it (E7).
  Regenerating from source with that version reproduces both faults. Commit
  ff3cbb0 (25 September) changed the generator to keep the reading
  convention, the "What this document is not" note, the inputs and the
  decomposition method, and to emit the WBS as an outline; it still drops the
  rest of the front matter, including the team-size note. Before a push,
  build the payload (`python3 tools/scope_tab3.py --out <scratch>/tab3.md`)
  and audit it as well as the source. Change `docs/*.md` and push with the
  tab's writer (`references/project.md`, Doc tabs), and remove an obsolete tab
  rather than leave it alive (audit E3, W14).
- **The team edits the Doc by hand too, so a regenerated tab keeps what the
  Doc keeps.** Teammates delete paragraphs, move sections into the draft tab
  and restructure tabs: tab 3 is rebuilt with `--limit 5` minus a lead
  paragraph the team deleted, and `gdoc_schedule_tab.py --schedule-only`
  writes 4.1 alone because the change request and resource loading were moved
  to Thẻ 2 (commit 1d43601). Before a push, compare the live tab (a fresh
  `tools/gdoc_dump.py` snapshot) with the payload; a generator run must not
  restore what the team removed. The source stays the place to change content.
- **When a new form reaches the Doc, older tabs that say it does not exist are
  updated in the same push.** Tab 5 said "There is no separate cost or quality
  management plan" while tab 6 was form 2.23 (V6.21, error). Grep every tab for
  "no ... plan", "not in this report", "has not been produced".
- **Two forms said to be kept in step carry the same rows.** The RBS said it was
  "kept in step with form 2.28" and dropped one of its 19 rows (V8.2). Compare
  the row sets of 2.29 with 2.28 and of 1.3 with 1.4.
- **Every test or fix package includes the role that fixes what it tests.**
  Mobile defect fixing between M4 and M5 had no mobile developer hours (24 Sep
  W10).
- **Each tab says what its empty cells mean**: unknown, none apply, or zero.
  Agreement Information was empty in 10 of 24 sheets with no word on why
  (V5.8, V6.34).
- **The submission is one Doc under the name the brief asks for** (`4.docx` or
  `4.pdf` for group 4), with no diverged second copy (24 Sep W13, W14). The
  stale `Copy of 4.md` is not the deliverable.
- **Stakeholders include every party a risk depends on.** Now under section 1,
  People and roles, so that it is read for every stakeholder form.
- **Team size read against the brief is an interpretation**, and the note that
  explains it must travel with the document (audit W1).

## 11. How to answer a reviewer

The replies in the 16 September review follow a pattern worth reusing when the
skill is asked to respond to comments:

1. Agree or disagree in the first word ("Đồng ý", "Đã bỏ", "Đã thêm").
2. Say exactly what changed and where (section, cell, version).
3. Quote the new sentence in English when the source is English.
4. List the knock-on edits in other places (A01, exit criterion 2, RTM BR05).
5. When the reviewer's request conflicts with a fixed constraint (budget,
   duration), say which constraint, what the trade-off costs, and that the team
   decides. Do not silently pick.
6. Reply in the reviewer's language (Vietnamese threads get Vietnamese replies).

The 8 November replies on the risk register (`scratch/risk-replies.md`, posted
10 November) added four more:

7. Open with the version and date of the fix and how the change is marked in
   the Doc ("bản 1.1 (8/11/2026) ... Ô thay đổi tô nền xanh").
8. One reply per thread, numbered to match the reviewer's items. Where a point
   is unclear, ask a precise question back ("anh chỉ giúp ô cụ thể") and list
   what was not changed and why ("chưa sửa vì chưa rõ ý"), rather than guess.
9. When a reviewer says more errors remain ("còn lỗi nữa, cần xác định
   thêm"), self-audit and list what you found beyond their list.
10. Before calling a thread answered, confirm the promised change is in the
    live Doc, not only in the source (V2.10; V9.1 found tab 8's asks not yet
    pushed on 8 November).

## 12. Marking: yellow, empty, green

The brief: "in case you don't know how to write, please let the box empty; in
case you don't know the content is correct or not, please let the background
of box in yellow" (`docs/requirements.md`).

- **Each tab explains its marks once, near the top, in the same words as the
  other tabs.** Yellow was explained eight different ways and not at all in
  the Product Charter, which carries the most highlights (V1.65, V2.7; the
  user's own thread AAACHKhdaSE).
- **Yellow is judged against the brief, not against the team's own charter.**
  A figure the brief does not give is uncertain to the grader even when the
  charter states it: 1,200 students, 35 teachers, 3 branches, 60 staff-hours,
  8%, the milestone dates, unit prices, the sponsor's and customer's names
  (thread AAACHKhdaSE; V2.8, error, those figures plain on 8 November). Mark
  them where they originate. A copy in another form follows the origin (next
  rule). `house-style.md` (Never invent a value) gives the exception.
- **Highlight the uncertain value itself, the same way wherever it appears.**
  A highlight on the words that confess doubt is not a highlight on the number
  (V1.66); "60 staff-hours a month" was yellow in the purpose and plain in the
  business case table (V2.52; V6.8, V7.22).
- **Do not highlight everything.** 608 yellow dates on 2.18 page 1, M0 among
  them though the same table calls it fixed, carry no information (V4.58). A
  fixed date is plain.
- **Green marks a cell changed in this version; yellow still marks
  uncertainty; one cell can carry both.** Vatten, 5 November: "Highlight những
  chỗ thay đổi để cô biết" (highlight what changed so the lecturer can see).
  In Markdown the changed cell is wrapped in `<ins>`, outside any `<mark>`;
  the italic paragraph says so. Only `tools/gdoc_risk_tab.py` converts it
  today; another form that uses it needs the same conversion in its writer.

## 13. Versioning and visible change

**A form revised after a review opens with a Revision history table**:
Version, Date, Change, Review comment answered (the reviewer and the date of
the thread, with the points). Its last version's date equals Date Prepared,
and every changed cell is green (section 12). Vatten asked for it on 5
November ("Thêm phần quản lý version"); the 8 November audit found no tab
showing a version (V1.38, V9.2). 2.32 version 1.1 is the model
(`docs/forms/2-32-risk-register.en.md`, Revision history). The table sits above
the form with the scales, never inside it.

## 14. Doc layout and print

From the print layout audit of 14 October (the PDF export of each tab) and the
8 November audit; the tab writers in `tools/` carry each fix. Check them on
`doc.json` of a fresh snapshot or on the PDF export, not on the Markdown.

- **Header rows repeat on every page a table runs onto** (`tableHeader`, the
  writers' pinned header rows; G5.2, G5.3).
- **A row short enough for one page does not split** (`preventOverflow`).
- **The line that introduces a table stays with it** (keep-with-next on the
  paragraph before the table, past an empty paragraph; a rerun undoes the
  earlier pass, commits a7c769d, 82bd613).
- **A form opens on a new page**, so its title bar is never left at the foot
  of a page; nothing else opens a page, and no tab ends on a blank page.
- **Amounts, two-level scores ("Medium-High"), Date Prepared and the Project
  Title line do not wrap.** Wide grids in 7 to 8 pt with tight padding, prose
  tables 10 pt (commits 4228247, 03f765f, 12039da, 8f9e6ba); no text runs over
  into the next cell (G1.23).
- **Tables fit the text area** (column widths at most about 468 pt portrait,
  648 pt landscape; G5.1, G4.1).
- **An image is legible where it is placed and a grid is not printed twice.**
  Gantt text printed at about 3 pt (G1.22); page 1 of 2.18 showed the same
  304-row grid as image and table, 36 pages before the fix, 18 after (G1.27,
  commit 733ace7).
- **A cell of a printed grid holds a short label; the explanation goes in the
  reading note** (Method and Confidence Level of 2.20, commit 4228247).
- **Paragraphs have space between them**: the Doc's normal style has none, and
  the blank line between Markdown paragraphs does not survive the insert
  (commit 098a5a7).
- **The reading note says what "Page N of M" counts** when one printed page
  runs over several Doc pages.

## 15. Risk register writing and scoring (2.31, 2.32, 2.36)

Đại Dũng Nguyễn's eight points of 4 November and Vatten's thread of 5 November
on tab 8 set what the reviewers expect; version 1.1 of
`docs/forms/2-32-risk-register.en.md` answers them and is the model.
`rendering.md` (Filling 2.32) gives the Markdown shape.

- **Every risk statement reads "If CONDITION exists, EVENT may occur, leading
  to EFFECT"**, with a specific cause (BoF Table 2.29, PDF page 140 (printed
  page 129); Đại Dũng item 2: "Risk statement sai cấu trúc"; Vatten: "R1: Nói
  kỹ hơn, đang bị chung quá", too general). The charter's risks are restated
  in that structure in 2.32, and the charter keeps its short text; the italic
  paragraph says so.
- **Every risk has one owner, a role named as in 2.28, highlighted when it is
  the preparer's proposal** (item 3: "tất cả các risk đều phải có risk owner";
  V9.5, six of 18 risks with no owner).
- **Scales are defined before they are used.** With no 2.31, the register
  carries above the form the three 2.31 elements it needs: definitions of
  probability, definitions of impact by objective, and the probability and
  impact matrix, on the pattern of PMBOK 6 Table 11-1 and Figure 11-5 (item 7:
  "Cần định nghĩa mức đánh giá"). Cost levels follow the charter's budget
  authority.
- **Each Impact cell gives the level and the effect on that objective**,
  `High: A01 cannot be shown as met`, and the level matches the effect: a
  risk that fails A01 or moves go-live is not Low (item 4: "Impact phải là mô
  tả chi tiết"; Vatten on R2: "Impact để high").
- **Every printed element is filled**, Revised Probability, Impact and Score
  included, as the forecast residual risk once the response is carried out
  (PMBOK 6 section 11.5.3.3, printed page 448 (PDF page 487)), highlighted (item 5; Vatten: "Revised
  Probability: Viết lại").
- **Score names which part is probability and which impact**
  (`Medium-High`, Probability-Impact, the highest of the four impacts), and
  the priority is read from the matrix.
- **Response starts with the threat strategy**, `Mitigate: ...`, then the
  response; the strategy does not sit in Comments (the team's own finding in
  the 8 November reply).
- **Actions say what is done**: `Work package <code> <title>: <action>`, a
  colon between the package and the action, a semicolon between packages
  (Vatten: "Chưa rõ hành động là gì, mới chỉ biết vị trí ở đâu ... dùng ':'
  thay vì ','"; V9.6, error).
- **A risk is written from the customer's side** (Vatten: "R7: Paraphrase lại
  để cho khách hàng thay vì các tính năng nội bộ"), with no internal jargon,
  and no two risks share one action.
- **A response that creates work records its secondary risk** (Vatten: "R4 có
  thể dẫn đến thêm việc").
- **The work a response promises is in the schedule as stated**: "build F04
  first", "pilot for two weeks" (V1.36; V4.38, V4.3 a 3-day pilot).
- **All risks are threats** is a fact to state (pmbok-risk.md, Traps); the
  book wants opportunities considered too.

## 16. Schedule logic (2.18 and the 3.3 that moves it)

- **No critical path or float without a network.** The schedule was levelled
  without an activity list, duration estimates or a network diagram, so it
  has no dependencies and no float (V4.7); the charter's "about one week of
  float each" rests on no predecessor logic (G2.1, G3.1). Flag every "critical
  path" or "float" sentence when 2.12, 2.15 or a predecessor column is absent.
- **Fast tracking does not cross a gate the dictionary states as hard.** Tab 4
  let work start up to 5 working days before two gates the dictionary calls
  hard rules (G1.13).
- **Dividing an activity between two people is crashing**: name it, with its
  cost and the coordination assumption (V4.12).
- **A constraint or a lead time the charter states holds in the levelled
  schedule.** The mobile developer started before the forecast M2 against
  "joins after M2" (V4.14); Apple's enrolment of up to four weeks sat in a
  4-day package (V4.13).
- **A renumbering is a schedule change.** The leveller breaks ties on WBS
  codes, so the 30 September renumbering moved 209 of 304 rows and changed the
  go-live slip from 31 to 30 working days (`review/2026-09-30-schedule-v2.md`,
  lines 68 to 75 and 107 to 121). After any code change, rerun the schedule,
  diff dates and people, and recompute every schedule figure of the pending
  3.3 with the same counting rule.

## 17. WBS and dictionary structure (2.9, 2.10)

- **A control account holds two or more work packages** (PMBOK 6 section
  5.4.3.1, printed page 161 (PDF page 200); V3.3, error: two control accounts
  held one package each).
- **Work packages are named as deliverables, not activities** ("test summary
  report", not "testing"; V3.13: at least 20 of 78).
- **Level 2 shows the structure the note names.** Vatten, 24 September: "Sai
  hẳn luôn, mới có 1 phase???" (only one phase?); V3.12: the note says major
  deliverables, the names show life-cycle phases.
- **Sizing exceptions are recounted after any change, and a gate crossing is
  not an hours exception** (24 Sep E7; V3.14; V6.19, a scaled package at 7.2
  hours under the 8-hour floor).

## 18. Pending change requests across the Doc

- **While a request is undecided, every tab follows the baseline and says
  what the request would change.** The scope request of 8 October was applied
  in tabs 5 and 7 and not in 3, 4, 6 and 8, so headcount, budget, rates,
  report frequency and warranty differed between tabs (V1.61, V8.3, V8.4). A
  tab that applies a pending request is a finding unless every tab does and
  the disposition is recorded in 3.4.
- **Impacts are measured against the approved baseline.** The schedule impact
  was ticked Decrease while, against the charter, the request moved closeout
  24 days later, 5 February to 1 March 2027 (V6.1, error). Project Documents
  lists every form and criterion the request touches (V6.15, G3.3).
  `decisions.md` section 4 (While a 3.3 is pending).

## 19. Length and audience

- **Reading notes in the Doc are short, and the reviewers may want them
  gone.** Vatten, 30 September, on tab 3's Reading convention: "Nên bỏ không"
  (should we drop it?), unanswered; notes of 331 to 433 words in tabs 4 to 8
  (V4.42, V6.36, V7.20, V9.27). The 150-word limit of `rendering.md` applies to
  each Doc paragraph too; whether to drop the notes is the team's call.
- **What the brief calls short stays short.** The brief asks for a short
  requirement specification; the charter tab is about 11,200 words and its 2B
  repeats 2A almost word for word (V2.22; Vatten: "Cho ngắn").
- **A team charter states checkable working rules, not values**: who, when,
  and how it is checked, each proposal a highlighted `[TBD]` (commit b6447cc).

## 20. The reviewers and what each checks

Use these to predict a reviewer's comment and to write a reply that answers
it. `.claude/agents/doc-auditor.md` stands in for them in a whole-Doc audit.

- **The lecturer** ("cô", through the brief and through Vatten): every part of
  the brief present (the Prompt Log too), the book's forms, yellow for
  uncertain and empty for unknown, changes visible between versions.
- **Đại Dũng Nguyễn**: strict book fidelity. A table that is not in the book
  is wrong; every printed element filled; risk statements in the book's
  structure; an owner for every risk; impacts described; scales defined; one
  name per function. Expects the author to find more than he lists.
- **Vatten** (31 of the 44 threads; also commits the WBS renumbering, the 2.9
  box, the control-account dictionary and the cost estimate): whole-section
  form fidelity ("Chỉnh giống y hệt form", "Lệch hẳn format"); length ("quá
  dài", "Cho ngắn", "Nên bỏ không"); numbering and codes; money logic (warranty
  budgeted, no extra money to the PM for risk, every line proved, tranche
  split); thresholds that hand power to the customer (100% UAT); scope
  boundaries; customer-facing wording; actions that say what is done; visible
  versioning. Terse; often replies to his own comment.
- **Nguyễn Bá Hùng**: scope and focus; the project scope written out;
  success criteria resting on the key deliverables; the reduced-scope cost
  estimate with unit tests (commit a28054f).
- **Thành Trần Xuân** (main author): raises consistency, marking, dates and
  missing parts in self-review threads, and writes the team's replies in the
  section 11 pattern.
