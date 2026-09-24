# What the team's reviewers catch

Two review rounds on this project's documents produced 60 findings:
`review/2026-09-16-doc-review.md` (26 reviewer threads, 9 new findings) and
`review/2026-09-24-doc-audit.md` (11 errors, 14 warnings). Almost none of them
were about missing fields. They were about a document that disagrees with
itself, with its sibling documents, or with the printed form, in ways a
reader notices and a generator does not.

Read this file before generating a form that reuses project facts, and before
any audit. Each lesson says what went wrong, why a reviewer cares, and how to
check it. `scripts/check_consistency.py` automates the ones marked **[script]**;
the rest need reading.

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

## 1. People and roles

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

**One person, one name, everywhere.** The old tab named the PM "Ngô Hải Đăng" on
page 1 and "Nguyễn Văn A" in the stakeholder table. Now the PM is deliberately
unnamed (assumption 15: the sponsor appoints the PM at M0), so the name box, the
stakeholder row and the signature block are all empty, in all three places.
(Thread AAACG0ldth8; New 1.)

**A field holds the value, not a description of it.** Reviewers struck
"- owner and Director of the learning center" after a sponsor's name and "- sponsor
of the learning center: 3 branches, 1,200 students, 35 teachers" after a
customer's. Facts about the center belong in 1.1.1, not repeated in a name box.
A role clause is acceptable only where it disambiguates (the Customer box keeps
"owner and Director" to tell her apart from the sponsor).

**A real person's name used for a fictional role is a question, not a fix.**
The customer carries the lecturer's name from the cover (New 8, audit W12).
Flag it to the team; do not rename on your own.

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
business owners who execute it, not to Handover under QA1).

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
(E7). Count the thing before writing the number, and name the source of any
item that does not come from the book (the 14th element, Project approval
requirements, is PMBOK 6 section 4.1.3.1).

**A rule that is cited is stated.** "Exceptions to the sizing rule" in a Doc that
never states the 8 to 80 hour rule (audit E7). If a section relies on a rule,
the rule is in the same deliverable.

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
  flags uniform columns.

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
  printed reading order; `tools/gdoc_form.py` and `scripts/md_to_docx.py`
  apply the pairing and group headers at render time. Do not invent a pairing
  the form does not print.
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
- **Tailoring is allowed but must be named.** The book permits a trimmed WBS
  dictionary (page 53); the team kept the full form because the brief asks for
  forms filled "as much as possible". Whichever way you go, say it once.

## 8. Markup that does not survive the Doc

- `<br>` inside a table cell arrived in the Google Doc as literal text, 23
  times (audit E6). `<mark>` is the only HTML the pipeline converts. **[script]**
- A table cell cannot hold a bulleted list in Markdown. When a reviewer asks for
  bullets in a cell (thread AAACG0ldtiw), write numbered items inline, `(1) ...
  (2) ...`, in the Markdown; the Doc may use real bullets.

## 9. Dates

One format per document, day without a leading zero, month in full, year:
`2 September 2026`. Reviewers flagged `02 September 2026`, `5 Jan 2027` and
`Mon 14 Sep 2026` mixed with `14 September 2026` (New 7, audit W11). A weekday
prefix is acceptable only if every date in that table carries one; the scope
package uses `Mon 14 September 2026` consistently in its dictionary. **[script]**
flags leading zeros, abbreviated months, and mixed styles within a file.

## 10. Completeness of the package

- **Every part the brief asks for is in the delivered file.** The Prompt Log
  (requirement 4) was missing from the live Doc, which would score zero (New 2,
  audit E5). Check `requirement.md` and `docs/wbs_req.md` against the headings
  of the deliverable.
- **Assumptions list is complete.** The Doc stopped at 15 while the source had 19
  (New 9). New assumptions introduced by a change (16 sponsor and customer are
  distinct, 17 rate basis, 18 app adoption, 19 SMS and hosting costs) must be
  added in the same change.
- **The Doc is regenerated from the source, not edited by hand.** Hand edits left
  the Doc 108 paragraphs behind its source and kept an obsolete tab alive
  (audit E3, E9, W14). Change `docs/*.md`, then push with `tools/gdoc.py` or
  `tools/gdoc_edit.py`.
- **Stakeholders include every party a risk depends on.** R12 depends on Apple,
  Google and the push provider, none of whom was listed (audit W5).
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
