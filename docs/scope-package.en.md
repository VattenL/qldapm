# Learning Center Management Software

## Scope Baseline Package: Requirements Traceability Matrix, WBS, and WBS Dictionary

**Project:** Development and Deployment of a Learning Center Management Software
**Customer:** <mark>Private after-school learning center, three branches, one city</mark>
**Budget:** 700,000,000 VND  **Window:** <mark>14 September 2026 to 5 February 2027</mark>
**Team:** 5 full-time staff, being 1 project manager / business analyst, 3 developers, 1 QA engineer, plus <mark>one part-time mobile developer for 2.5 person-months</mark>
**Date prepared:** 23 September 2026  **Document version:** 2.0

**Team size.** The brief for this deliverable assumes 4 staff, while the charter package is
baselined at 5 full-time staff plus a part-time mobile developer, inside the 4 to 6 the original
course brief allows; this package costs to that baseline so that the two documents agree, and 4 is
read as a floor rather than a ceiling.

---

### How this document is organised

This is the second deliverable of the coursework. The first is `charter-package.en.md`, which
carries the requirement specification and the project charter. This one carries the three
scope-management artifacts named in `docs/wbs_req.md`, each reproduced from the form in *A Project
Manager's Book of Forms*, 3rd edition, field for field and in the printed field order.

| Part | Artifact | Form | Pages in the book | PMBOK 6 process |
| --- | --- | --- | --- | --- |
| Part 1 | Requirements Traceability Matrix | 2.7 | 40 to 44 | 5.2 Collect Requirements |
| Part 1B | Inter-Requirements Traceability Matrix | 2.7, page 2 of 2 | 44 | 5.2 Collect Requirements |
| Part 2 | Work Breakdown Structure | 2.9 | 49 to 51 | 5.4 Create WBS |
| Part 3 | WBS Dictionary | 2.10 | 52 to 55 | 5.4 Create WBS |

The page column carries printed page numbers of the book; the PDF page is the printed page plus 11.

The WBS and the WBS dictionary, together with the project scope statement in Part 1 of the charter
package, are the **scope baseline**.

### What this document is not

Validate Scope (5.5) and Control Scope (5.6) produce no artifact here. Both are Monitoring and
Controlling processes: Validate Scope needs verified deliverables handed over by Control Quality
(8.3), and at the time of writing the project has produced none. Change requests are outputs of
those two processes only, and they are the input to Perform Integrated Change Control (4.6). The
four planning processes 5.1 to 5.4, which are what this document covers, output no change requests.

### Inputs actually used

Per PMBOK 6 Figure 5-10, Create WBS takes the scope management plan, the project scope statement,
and the requirements documentation. The project charter is **not** a direct input to 5.4: it is an
input to 5.1, 5.2, and 5.3, and it reaches the WBS through the scope statement that those processes
produce. The requirements traceability matrix is an **output** of 5.2, not an input to 5.4; it is
updated later by 5.5 and 5.6. This document therefore builds the RTM first from the charter and the
requirement specification, and then builds the WBS from the scope statement, not from the matrix.

| Input | Where it comes from |
| --- | --- |
| Project scope statement | `charter-package.en.md` sections 1.1 to 1.6 |
| Requirements documentation | `charter-package.en.md` sections 1.1.4 (F01 to F12), 1.1.5, 1.3 (A01 to A12) |
| Scope management plan | Not produced as a separate document for this coursework; the rules it would carry are stated in the conventions below |
| Project charter (indirect) | `charter-package.en.md` Part 2A and 2B |

The date prepared, 23 September 2026, falls inside the requirements phase, so the requirements
documentation used here is the draft that is baselined at M1, and the package is re-issued against
that baseline.

The team this package costs is the charter's: 5 full-time staff plus the part-time mobile developer,
not the 4 staff the brief for this deliverable assumes. Costing to the charter baseline is what
keeps the two documents arithmetically consistent, and 6 sits inside the 4 to 6 the original course
brief allows.

### Decomposition method

**Top-down.** The charter fixes the deliverables D1 to D11 and the milestones M0 to M7 before any
work package exists, so the structure is decomposed downward from the project to the work package
rather than assembled upward from tasks. The two methods are not mixed.

**Organised by major deliverable, in life-cycle phase order.** Form 2.9 prints **Major Deliverable**
at level 2, and that is what level 2 holds here: the ten major deliverables of the project, arranged
in the order of the predictive life cycle with its two build iterations. The annotation on each
level-2 line names the charter deliverable and milestone it carries. Level 3 is the control account,
level 4 is the work package. Each work package rolls up to one and only one control account, per the
book's rule on page 50.

**One owner per work package.** Every work package names a single accountable owner. Work and review
are never owned by the same person: a review or rework package is always owned by the QA engineer or
by a developer who is not the author of the work being reviewed. Review and testing are work
packages in their own right, held in a separate assurance control account inside the phase whose
output they check, and phase 1.6 exists on top of that for the system-level test, which cannot sit
inside a single construction package.

**Work package sizing.** Every work package holds between 8 and 80 hours of effort and is controlled
inside a single milestone gate, which is the reporting period used for work-package control; the
weekly status report of 1.1.1.3 is a progress report, not the control period. Four packages sit
outside that rule, and they are named here rather than left to be found. 1.1.1.3 weekly status
reporting at 120 hours and 1.10.1.1 first warranty month support at 400 hours are level-of-effort
packages that run for the whole of their period by nature and cannot be cut into 80-hour pieces
without inventing work that is not there. 1.1.1.4 is exactly 80 and therefore inside the rule.
1.9.1.1 store accounts and signing keys is inside the hour rule at 22 hours but crosses the M2 gate,
because Apple's enrolment of a legal entity takes up to four weeks and that wait is outside the
project's control.

### Reading convention

- <mark>Yellow highlight</mark> marks content whose correctness cannot be confirmed from the brief or the
  charter, per point 3 of the assignment.
- An empty box means the field cannot be completed at this stage, not that it was overlooked.
- In Part 3, the **split** of hours and money across work packages is a first-pass estimate and carries
  a single highlighted tag once per sheet rather than cell by cell; the tag is explained in full in the
  Part 3 preamble. The **totals** it rolls up to are given by the charter and are not highlighted:
  4,400 labor hours, 539,000,000 VND of labor, 161,000,000 VND of other cost, 700,000,000 VND in all.
- Resource codes: **PM** project manager and business analyst, **DEV1**, **DEV2**, **DEV3** developers,
  **QA1** QA engineer, **MOB1** part-time mobile developer. Individual names are not filled in: the
  charter has the sponsor assigning the project manager at M0 and the team is mobilised in work package
  1.1.1.1, so the name boxes stay empty until then. DEV1 and DEV2 are the pair the charter assigns to
  scheduling and billing, and they build F04 and F06.
- Labor rates are the charter's rate mix, converted at <mark>160 hours per person-month</mark>:
  PM 162,500 VND/h, developer 118,750 VND/h, QA 93,750 VND/h, mobile developer 122,500 VND/h.

---

## Part 1: Requirements Traceability Matrix

*Form 2.7, page 1 of 2. Columns and their order are the printed ones: the Requirement Information
group is ID, Requirement, Source, Priority, Category; the Relationship Traceability group is
Business Objective, Deliverable, Verification, Validation.*

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

Three ID families are used. **BR** business requirements, taken from the charter's business case and
objectives. **FR** functional requirements, one per function F01 to F12 of the requirement
specification. **NFR** nonfunctional requirements, one per acceptance criterion A01 to A12. The
Requirement column carries a label and the charter code; the full text lives in the charter. Every
requirement is Must have: the charter requires all twelve functions accepted in UAT and all of A01
to A12 met, so nothing in the baseline is optional. The Deliverable column cites the WBS code from
Part 2 and the charter deliverable in brackets.

### Requirement Information and Relationship Traceability

| ID | Requirement | Source | Priority | Category | Business Objective | Deliverable | Verification | Validation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BR01 | Data held once and entered once | Center Director | Must have | Business | Cut duplicate data entry from <mark>60 to 15 staff-hours a month</mark>, 32,400,000 VND a year | 1.4.1.4, 1.7.1.3 (D3, D6) | Staff time log over one month after go-live shows 15 hours or fewer of re-entry | Director confirms against the closeout report, measured in the first warranty month |
| BR02 | No double-booked room, teacher, or student | Academic Manager | Must have | Business | Remove double-booking at source; not quantified in the business case | 1.4.2.3 (D3) | Zero conflicting bookings accepted in the UAT conflict test set | Academic Manager runs the conflict scenarios in UAT |
| BR03 | Overdue tuition visible and falling to <mark>3%</mark> | Accountant, Center Director | Must have | Business | Release <mark>360,000,000 VND</mark> once, save <mark>36,000,000 VND</mark> a year of carrying cost and <mark>36,000,000 VND</mark> of write-off | 1.5.1.1, 1.5.1.3 (D4) | Aged debt report shows the overdue percentage monthly; stated in the closeout report | Accountant reconciles the report against the bank and the invoice ledger |
| BR04 | Cross-branch visibility without a spreadsheet | Center Director | Must have | Business | One current cross-branch view, needed before the <mark>fourth branch in 2027</mark> | 1.5.3.1, 1.5.3.3 (D4) | Every F10 report filterable by period, branch, and course, produced within 10 seconds | Director uses the dashboard unaided in UAT |
| BR05 | Notification cost held down | Center Director | Must have | Business | Hold notification cost at <mark>13,800,000 VND</mark> a year through push rather than <mark>46,100,000 VND</mark> on SMS alone | 1.5.4.2, 1.5.2.2 (D4, D11) | F09 delivery log shows the channel mix; push share at least <mark>70% of guardians with a smartphone</mark> | Accountant checks the gateway invoice for the first warranty month |
| BR06 | Payroll derived from delivered sessions | Accountant | Must have | Business | Remove the payroll rework and the disputes it causes; not separately quantified | 1.5.1.2 (D4) | Monthly sheet reconciles to the attendance records with zero manual adjustment rows | Accountant approves one full month close during the warranty month |
| BR07 | The center runs its daily operation on the system from go-live, with the data in its own hands | Center Director | Must have | Business | The stakeholder-satisfaction objective and the exit criteria of the charter | 1.8.3.2, 1.10.2.1 (D8, D9, D10) | Training record, handover record, and the closeout report together evidence the exit criteria | Center Director confirms at closeout that the center operates on the system |
| FR01 | Authentication and role-based access control (F01) | System Administrator | Must have | Functional | Quality: A04 met | 1.4.1.1 (D3) | Each role reaches only its own screens and data in the UAT permission matrix | UAT script run by the System Administrator across all seven roles |
| FR02 | Student profile, enrollment, transfer, and withdrawal (F02) | Front-desk staff | Must have | Functional | Scope: F01 to F12 accepted; BR01 | 1.4.1.2, 1.4.1.4 (D3) | Enrollment refused in both refusal cases; refund figure matches the policy worked example | Front-desk staff enroll, transfer, and withdraw a test cohort in UAT |
| FR03 | Versioned course and curriculum catalog (F03) | Academic Manager | Must have | Functional | Scope: F01 to F12 accepted | 1.4.1.3 (D3) | A course edit leaves the definition of an opened class unchanged | Academic Manager edits a course that has open classes in UAT |
| FR04 | Class opening, scheduling, and conflict detection (F04) | Academic Manager | Must have | Functional | BR02 | 1.4.2.1, 1.4.2.3 (D3) | Every conflict case in the test set is blocked at creation or at move time | Academic Manager runs the conflict scenarios; pilot branch uses it for two weeks before M6 |
| FR05 | Attendance and make-up sessions (F05) | Teacher | Must have | Functional | Stakeholder satisfaction: <mark>90% of classes</mark> with attendance recorded in the first warranty month | 1.4.2.2 (D3) | Attendance rate figures match a hand count for a sample class over one month | Teachers mark real sessions during the pilot at one branch |
| FR06 | Tuition, invoicing, payments, and debt tracking (F06) | Front-desk staff, Accountant | Must have | Functional | BR03 | 1.5.1.1, 1.5.1.3 (D4) | Invoice totals match the policy worked examples; the aged debt list ties to the invoice ledger | Accountant reconciles one term of test invoices and payments in UAT |
| FR07 | Teacher records and teaching-hour payroll (F07) | Accountant | Must have | Functional | BR06 | 1.5.1.2 (D4) | Monthly sheet reconciles to attendance with zero manual adjustment rows | Accountant closes one test month end to end |
| FR08 | Assessment, progress reports, and course evaluation (F08) | Teacher | Must have | Functional | Scope: F01 to F12 accepted; BR07 | 1.5.2.1 (D4) | Final results match the course rule for every pass and fail boundary case | Academic Manager checks one completed course in UAT |
| FR09 | Notification and internal communication (F09) | Front-desk staff | Must have | Functional | BR03; BR05 | 1.5.2.2 (D4) | Every message carries a delivery state; failures carry a reason and are retried | Front-desk staff send each of the seven event types in UAT |
| FR10 | Reports and management dashboard (F10) | Center Director | Must have | Functional | BR04 | 1.5.3.1, 1.5.3.3 (D4) | One term's report produced within 10 seconds; figures match the underlying records | Director runs every report unaided in UAT |
| FR11 | System administration and audit (F11) | System Administrator | Must have | Functional | Quality: A05 met; BR07 | 1.5.3.2 (D4) | Every financial and student write appears in the audit log with user and timestamp | System Administrator samples the log against a scripted set of changes |
| FR12 | Android and iOS application for parents and teachers (F12) | Student / Parent, Teacher | Must have | Functional | BR05; Stakeholder satisfaction: <mark>70% of guardians with a smartphone</mark> activated by closeout | 1.4.4.1, 1.5.4.1, 1.5.4.3, 1.9.1.2 (D3, D4, D11) | Every F12 function within 3 taps; push delivery recorded in the F09 log | Parents and teachers use the application during the pilot and the first warranty month |
| NFR01 | Functional completeness in UAT (A01) | Center Director, sponsor | Must have | Acceptance | Scope: no function deferred without an approved change request; BR07 | 1.6.2.2, 1.8.3.2 (D5) | UAT pass rate at or above 99%; defect log shows no open Critical or High | UAT sign-off by the sponsor at M6 against the test set agreed at M5 |
| NFR02 | Performance thresholds (A02) | Center Director | Must have | Performance | Quality: A02 met | 1.6.1.3 (D5) | Load test report shows the 95th percentile inside each threshold | Load test witnessed by the System Administrator before UAT entry |
| NFR03 | Capacity without redesign (A03) | System Administrator | Must have | Capacity | Quality: A03 met | 1.6.1.3 (D5) | Capacity test loads the stated volumes and the performance thresholds still hold | Same load test run, at the stated data volume |
| NFR04 | Security and personal-data protection (A04) | System Administrator | Must have | Security | Quality: A04 met; BR07 | 1.3.1.1, 1.6.1.4 (D2, D5) | Security test finds no unauthorised access path and no readable stored password | Security test report reviewed and accepted before UAT entry |
| NFR05 | Auditability of financial and student writes (A05) | Accountant | Must have | Auditability | Quality: A05 met | 1.5.3.2 (D4) | Log entries cannot be altered through any interface; retention is <mark>3 years</mark> | Accountant and System Administrator attempt an edit in UAT and fail |
| NFR06 | Availability, backup, and restore (A06) | System Administrator | Must have | Availability | Quality: A06 met; BR07 | 1.8.1.2 (D7) | Restore drill completes inside 4 hours from a backup no more than 24 hours old | Restore drill witnessed by the System Administrator, twice |
| NFR07 | Degraded operation and paper fallback (A07) | Academic Manager | Must have | Continuity | Quality: A07 met; BR07 | 1.8.2.2 (D8) | Rehearsal record signed, with the catch-up entry reconciled afterwards | Rehearsal run at one branch before M6 |
| NFR08 | Usability in Vietnamese after half a day of training (A08) | Front-desk staff, Teacher | Must have | Usability | Stakeholder satisfaction: <mark>80% of the 52 staff users</mark> trained and active; BR07 | 1.3.1.4, 1.8.2.2 (D2, D8) | Click count measured on each of the three paths; training record shows the half-day format | Staff perform their daily tasks unaided the day after training |
| NFR09 | Browser and device compatibility (A09) | System Administrator | Must have | Compatibility | Quality: A09 met; BR07 | 1.6.1.1, 1.6.1.2 (D5) | Test matrix covers every listed browser and both application platforms | Cross-browser and device test run before UAT entry |
| NFR10 | Maintainability and handover (A10) | System Administrator | Must have | Maintainability | Quality: A10 met; BR07 | 1.8.2.1, 1.8.3.1 (D8, D9) | Handover checklist complete; a third party can deploy from the guide alone | System Administrator deploys to staging following only the guide |
| NFR11 | Data ownership and open-format export (A11) | Center Director | Must have | Data ownership | Quality: A11 met | 1.5.3.2 (D4) | Export runs to completion from the administrator screen and opens in a standard tool | System Administrator produces the export unaided in UAT |
| NFR12 | Mobile application published in both stores (A12) | Center Director | Must have | Mobile | Quality: A12 met; BR05 | 1.9.1.2, 1.5.4.2 (D11) | Store listings live; fallback timer verified in the delivery log | Guardians install from the public store listing during the pilot |

### Part 1B: Inter-Requirements Traceability Matrix

*Form 2.7, page 2 of 2. Each business requirement is paired with the functional or nonfunctional
requirement that implements it. Where one business requirement needs several, it appears once per
pair, which is how the printed form carries a one-to-many relationship.*

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| ID | Business Requirement | Priority | Source | ID | Technical Requirement | Priority | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BR01 | Data held once and entered once | Must have | Center Director | FR02 | Student profile and enrollment on one shared record | Must have | Front-desk staff |
| BR01 | Data held once and entered once | Must have | Center Director | FR03 | Versioned course catalog as the single definition | Must have | Academic Manager |
| BR01 | Data held once and entered once | Must have | Center Director | NFR11 | Complete open-format export owned by the center | Must have | Center Director |
| BR02 | No double-booked room, teacher, or student | Must have | Academic Manager | FR04 | Conflict detection at creation and at move time | Must have | Academic Manager |
| BR02 | No double-booked room, teacher, or student | Must have | Academic Manager | NFR02 | Conflict check inside the 3 second screen budget | Must have | Center Director |
| BR03 | Overdue tuition visible and falling to <mark>3%</mark> | Must have | Accountant | FR06 | Invoicing, payment recording, and the aged debt list | Must have | Accountant |
| BR03 | Overdue tuition visible and falling to <mark>3%</mark> | Must have | Accountant | FR09 | Tuition due and overdue notifications with a log | Must have | Front-desk staff |
| BR03 | Overdue tuition visible and falling to <mark>3%</mark> | Must have | Accountant | NFR05 | Audit log over every financial write | Must have | Accountant |
| BR04 | Cross-branch visibility without a spreadsheet | Must have | Center Director | FR10 | Reports filterable by period, branch, and course | Must have | Center Director |
| BR04 | Cross-branch visibility without a spreadsheet | Must have | Center Director | NFR02 | One term's report inside 10 seconds | Must have | Center Director |
| BR04 | Cross-branch visibility without a spreadsheet | Must have | Center Director | NFR03 | <mark>3 years</mark> of history held without redesign | Must have | System Administrator |
| BR05 | Notification cost held down | Must have | Center Director | FR12 | Application as the push channel over the same API | Must have | Student / Parent |
| BR05 | Notification cost held down | Must have | Center Director | NFR12 | Push delivery logged with SMS fallback inside 4 hours | Must have | Center Director |
| BR06 | Payroll derived from delivered sessions | Must have | Accountant | FR05 | Attendance as the single record of what was taught | Must have | Teacher |
| BR06 | Payroll derived from delivered sessions | Must have | Accountant | FR07 | Monthly teaching-hour sheet and payroll export | Must have | Accountant |
| BR06 | Payroll derived from delivered sessions | Must have | Accountant | NFR05 | Audit trail over the sheet and its approval | Must have | Accountant |
| BR07 | The center operates on the system, data in its own hands | Must have | Center Director | FR01 | Seven roles, each seeing only its own work | Must have | System Administrator |
| BR07 | The center operates on the system, data in its own hands | Must have | Center Director | FR08 | Assessment and progress reporting inside the system | Must have | Teacher |
| BR07 | The center operates on the system, data in its own hands | Must have | Center Director | FR11 | Reference data and configuration in the center's hands | Must have | System Administrator |
| BR07 | The center operates on the system, data in its own hands | Must have | Center Director | NFR01 | All twelve functions accepted in UAT | Must have | Center Director |
| BR07 | The center operates on the system, data in its own hands | Must have | Center Director | NFR04 | Personal data handled lawfully from day one | Must have | System Administrator |
| BR07 | The center operates on the system, data in its own hands | Must have | Center Director | NFR06 | Nightly backup and a proven restore | Must have | System Administrator |
| BR07 | The center operates on the system, data in its own hands | Must have | Center Director | NFR07 | Paper fallback rehearsed before go-live | Must have | Academic Manager |
| BR07 | The center operates on the system, data in its own hands | Must have | Center Director | NFR08 | Daily tasks after half a day of training | Must have | Front-desk staff |
| BR07 | The center operates on the system, data in its own hands | Must have | Center Director | NFR09 | Usable on the browsers and devices the staff own | Must have | System Administrator |
| BR07 | The center operates on the system, data in its own hands | Must have | Center Director | NFR10 | Deployable and maintainable without the supplier | Must have | System Administrator |

---

## Part 2: Work Breakdown Structure

*Form 2.9, page 1 of 1. The printed form is a numeric outline running from the project at level 1
down to work packages; that is what is reproduced here. Level 2 holds the major deliverables, in
life-cycle phase order. Control accounts are marked **CA**; every line below a control account is a
work package.*

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

```
1.        Learning Center Management Software

1.1       Project Management                                      (major deliverable)
  1.1.1     Project Governance                                    CA
    1.1.1.1   Kickoff and team mobilisation
    1.1.1.2   Project management plan and schedule baseline
    1.1.1.3   Weekly status reporting and sponsor governance
    1.1.1.4   Risk, issue, and change control

1.2       Requirements                                            (major deliverable, D1, M1)
  1.2.1     Elicitation                                           CA
    1.2.1.1   Stakeholder workshops and current-process study
    1.2.1.2   Functional requirements specification, F01 to F12
    1.2.1.3   Nonfunctional requirements specification, A01 to A12
    1.2.1.4   Exception and failure behaviour catalogue
  1.2.2     Requirements Baseline                                 CA
    1.2.2.1   Requirements traceability matrix
    1.2.2.2   Requirements peer review and rework
    1.2.2.3   Requirements acceptance and baseline
  1.2.3     Technical Preparation                                 CA
    1.2.3.1   Repository, coding convention, and build pipeline
    1.2.3.2   Notification gateway proof of concept
    1.2.3.3   Cross-platform framework proof
    1.2.3.4   User interface prototype for business validation
    1.2.3.5   Development and test environment provisioning

1.3       Design                                                  (major deliverable, D2, M2)
  1.3.1     Solution Design                                       CA
    1.3.1.1   Architecture, security, and personal-data design
    1.3.1.2   Database schema design
    1.3.1.3   Server API contract
    1.3.1.4   Web user interface design
    1.3.1.5   Mobile application design
  1.3.2     Design Assurance                                      CA
    1.3.2.1   Design review and rework
    1.3.2.2   Test plan and test strategy
    1.3.2.3   Design baseline acceptance

1.4       Construction Iteration 1                                (major deliverable, D3, M3)
  1.4.1     Core Platform                                         CA
    1.4.1.1   F01 Authentication and access control
    1.4.1.2   F02 Student profile and guardian records
    1.4.1.3   F03 Course and curriculum catalog
    1.4.1.4   F02 Enrollment, transfer, reservation, and withdrawal
  1.4.2     Scheduling and Attendance                             CA
    1.4.2.1   F04 Class opening, session calendar, and postponement
    1.4.2.2   F05 Attendance and make-up sessions
    1.4.2.3   F04 Room, teacher, and class-time conflict detection
  1.4.3     Iteration 1 Assurance                                 CA
    1.4.3.1   Iteration 1 code review and rework
    1.4.3.2   Iteration 1 testing, core platform
    1.4.3.3   Iteration 1 demo and acceptance
    1.4.3.4   Iteration 1 testing, scheduling and attendance
  1.4.4     Mobile Application Alpha                              CA
    1.4.4.1   Application alpha, parent schedule, attendance, and scores

1.5       Construction Iteration 2                                (major deliverable, D4, M4)
  1.5.1     Finance                                               CA
    1.5.1.1   F06 Invoicing, discounts, and aged debt
    1.5.1.2   F07 Teacher records and teaching-hour payroll
    1.5.1.3   F06 Payments, receipts, and unmatched payments
  1.5.2     Academic and Communication                            CA
    1.5.2.1   F08 Assessment, progress reports, and course evaluation
    1.5.2.2   F09 Notification and internal communication
  1.5.3     Management and Administration                         CA
    1.5.3.1   F10 Financial reports and export
    1.5.3.2   F11 System administration and audit
    1.5.3.3   F10 Enrollment, fill rate, and workload reports
  1.5.4     Mobile Application                                    CA
    1.5.4.1   Parent tuition, messages, and requests
    1.5.4.2   Push notification integration
    1.5.4.3   Teacher journeys
    1.5.4.4   Offline behaviour and release build
  1.5.5     Iteration 2 Assurance                                 CA
    1.5.5.1   Iteration 2 code review and rework
    1.5.5.2   Iteration 2 testing, finance and administration
    1.5.5.3   Iteration 2 acceptance, feature complete
    1.5.5.4   Iteration 2 testing, academic, notification, and mobile

1.6       Quality Assurance and Test                              (major deliverable, D5, M5)
  1.6.1     System Test                                           CA
    1.6.1.1   System test execution, web, end-to-end scenarios
    1.6.1.2   System test execution, Android and iOS
    1.6.1.3   Performance and capacity test
    1.6.1.4   Security test
    1.6.1.5   Defect fixing, scheduling, reporting, and administration
    1.6.1.6   System test execution, web, exception and failure behaviour
    1.6.1.7   Defect fixing, enrollment, tuition, and payroll
    1.6.1.8   Defect fixing, catalog, assessment, notification, and platform, with regression
  1.6.2     Test Documentation                                    CA
    1.6.2.1   UAT test set, defect log, and test summary report
    1.6.2.2   UAT entry criteria review

1.7       Data Migration                                          (major deliverable, D6, M6)
  1.7.1     Migration                                             CA
    1.7.1.1   Source data analysis and cleansing rules
    1.7.1.2   Migration scripts and trial run
    1.7.1.3   Production migration and reconciliation report
    1.7.1.4   Accountant acceptance of the reconciliation

1.8       Deployment and Handover                                 (major deliverable, D7 D8 D9, M6)
  1.8.1     Production Environment                                CA
    1.8.1.1   Cloud server and staging provisioning
    1.8.1.2   Backup configuration and restore drill
    1.8.1.3   Production deployment and go-live
  1.8.2     Training and Documentation                            CA
    1.8.2.1   User, administrator, and deployment documentation
    1.8.2.2   Staff training, paper fallback procedure, and rehearsal
  1.8.3     Handover                                              CA
    1.8.3.1   Source code, database scripts, and technical documentation handover
    1.8.3.2   User acceptance testing execution and sign-off

1.9       Mobile Application Release                              (major deliverable, D11, M6)
  1.9.1     Store Release                                         CA
    1.9.1.1   Store accounts and signing keys
    1.9.1.2   Store listings, submission, and review response

1.10      Warranty and Closeout                                   (major deliverable, D10, M7)
  1.10.1    Warranty                                              CA
    1.10.1.1  First warranty month support
    1.10.1.2  Warranty handover to the support desk
  1.10.2    Closeout                                              CA
    1.10.2.1  Closeout report, lessons learned, and final acceptance
```

### Roll-up

Ten major deliverables, twenty-four control accounts, seventy-eight work packages. Each work package
appears under exactly one control account.

| Phase | Control accounts | Work packages | Charter deliverables | Milestone | Labor hours | Labor cost (VND) | Other cost (VND) | Total (VND) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.1 Project Management | 1 | 4 | internal | M0 to M7 | 300 | 48,750,000 | 17,700,000 | 66,450,000 |
| 1.2 Requirements | 3 | 12 | D1 | M1 | 536 | 71,400,000 | 0 | 71,400,000 |
| 1.3 Design | 2 | 8 | D2 | M2 | 404 | 48,600,000 | 0 | 48,600,000 |
| 1.4 Construction Iteration 1 | 4 | 12 | D3 | M3 | 742 | 85,925,000 | 0 | 85,925,000 |
| 1.5 Construction Iteration 2 | 5 | 16 | D4 | M4 | 938 | 109,360,000 | 4,000,000 | 113,360,000 |
| 1.6 Quality Assurance and Test | 2 | 10 | D5 | M5 | 556 | 60,000,000 | 2,000,000 | 62,000,000 |
| 1.7 Data Migration | 1 | 4 | D6 | M6 | 160 | 19,375,000 | 12,000,000 | 31,375,000 |
| 1.8 Deployment and Handover | 3 | 7 | D7, D8, D9 | M6 | 200 | 25,375,000 | 59,000,000 | 84,375,000 |
| 1.9 Mobile Application Release | 1 | 2 | D11 | M6 | 90 | 11,365,000 | 3,300,000 | 14,665,000 |
| 1.10 Warranty and Closeout | 2 | 3 | D10 | M7 | 474 | 58,850,000 | 35,000,000 | 93,850,000 |
| Contingency reserve, charter budget line 6, held at project level | | | | | | | 28,000,000 | 28,000,000 |
| **Total** | **24** | **78** | **D1 to D11** | **M0 to M7** | **4,400** | **539,000,000** | **161,000,000** | **700,000,000** |

Labor hours by resource: PM 800, DEV1 800, DEV2 800, DEV3 800, QA1 800, MOB1 400. At the charter's
rate mix that is 130,000,000 + 285,000,000 + 75,000,000 + 49,000,000 = 539,000,000 VND, which is
budget line 1 of the charter exactly. The other-cost column carries charter budget lines 2 to 6 and
is allocated to the work package that spends it, except budget line 6. A reserve is money set aside
against risk, not work to be performed, so it is not a work package and has no owner, no activity,
and no hours; it is carried as its own line below the phases and is drawn only through the change
control of 1.1.1.4.

The hours are effort, not calendar loading. Several packages inside a phase run in parallel, and
four packages are exceptions to the sizing rule stated in the decomposition method: 1.1.1.3 and
1.10.1.1 are level of effort and exceed 80 hours, 1.1.1.4 is exactly 80, and 1.9.1.1 crosses the M2
gate because of Apple's four-week enrolment lead time. Levelling that effort across the calendar is
Develop Schedule, PMBOK 6 section 6.5, which produces the schedule baseline rather than the scope
baseline and is therefore not in this document; it is the work of package 1.1.1.2.

Phase 1.2 carries a Technical Preparation control account that the charter's own risk responses
require before M2: the notification gateway proof for risk R5, the cross-platform framework proof
for risk R12, the repository, convention, and environments that acceptance criterion A10 depends on,
and the prototype that tests the interface against the people who will use it. Without it the
requirements phase would hold three idle developers and the two proofs the charter demands would
have nowhere to live.

### Coverage check

| Charter item | Where the WBS delivers it |
| --- | --- |
| F01 | 1.4.1.1 |
| F02 | 1.4.1.2 profile, 1.4.1.4 enrollment |
| F03 | 1.4.1.3 |
| F04 | 1.4.2.1 scheduling, 1.4.2.3 conflict detection |
| F05 | 1.4.2.2 |
| F06 | 1.5.1.1 invoicing, 1.5.1.3 payments |
| F07 | 1.5.1.2 |
| F08 | 1.5.2.1 |
| F09 | 1.5.2.2, with push in 1.5.4.2 |
| F10 | 1.5.3.1 financial, 1.5.3.3 academic |
| F11 | 1.5.3.2 |
| F12 | 1.4.4.1, 1.5.4.1, 1.5.4.3, 1.5.4.4, released by 1.9.1.2 |
| A01 to A12 | Verified across 1.6.1.1 to 1.6.1.8 and accepted in 1.8.3.2 |
| D1 to D11 | D1 1.2.2.3; D2 1.3.2.3; D3 1.4.3.3; D4 1.5.5.3; D5 1.6.2.1; D6 1.7.1.4; D7 1.8.1.3; D8 1.8.2.2; D9 1.8.3.1; D10 1.10.1.1, 1.10.1.2, 1.10.2.1; D11 1.9.1.2 |
| M0 to M7 | 1.1.1.1, 1.2.2.3, 1.3.2.3, 1.4.3.3, 1.5.5.3, 1.6.2.2, 1.8.3.2, 1.10.2.1 |
| 1.1.5 exception behaviour | Built inside the function package that owns it, tested in 1.4.3.2, 1.4.3.4, 1.5.5.2, 1.5.5.4, and 1.6.1.6, and rehearsed in 1.8.2.2 |
| R1 to R12 responses | Owned by 1.1.1.4. R1 1.6.2.1 and 1.8.3.2; R2 1.2.1.2; R3 1.1.1.3; R4 1.4.3.1, 1.5.5.1, 1.2.3.1; R5 1.2.3.2; R6 1.7.1.1; R7 1.4.2.1 and 1.4.2.3; R8 1.8.1.3; R9 1.2.2.2 and 1.3.2.2; R10 1.8.1.3; R11 1.10.1.1; R12 1.2.3.3 and 1.9.1.1 |

---

## Part 3: WBS Dictionary

*Form 2.10, one sheet per work package, as the printed form is laid out: Page 1 of 1 per work
package. Field names and field order follow pages 52 to 55 of the book. Responsible Person is one of
the elements the book lists for the dictionary on page 52, and it carries the one-owner rule.*

Seventy-eight sheets follow, one for each work package of Part 2, grouped by phase. The Description
of Work field cites the charter rather than restating it, which page 53 of the book expressly
permits: the dictionary may reference other documents and sections rather than repeat them.

**What the tag on every sheet means.** Each sheet carries one highlighted sentence in its
Assumptions and Constraints field. It means this, in full, once rather than on every sheet: the
hours, the money, and the dates on that sheet are a first-pass estimate; the charter commits to
re-estimating the breakdown at M1 and the sheet is re-baselined then; and the totals the sheets roll
up to are the charter figures and are not themselves estimates.

**What the hours mean.** The Labor Hours column is an **effort** estimate, not a calendar loading.
The milestone dates in the Due Dates field are the charter's gates, and several packages run in
parallel inside them. Levelling the effort across the calendar is Develop Schedule, PMBOK 6 section
6.5, which is not part of the scope baseline and is not in this document; it happens in work package
1.1.1.2. The totals are fixed by the charter and the sheets roll up to them exactly:

| | Hours | Rate (VND/h) | Amount (VND) |
| --- | ---: | ---: | ---: |
| Project manager and business analyst | 800 | 162,500 | 130,000,000 |
| Developers, three | 2,400 | 118,750 | 285,000,000 |
| QA engineer | 800 | 93,750 | 75,000,000 |
| Mobile developer, part time | 400 | 122,500 | 49,000,000 |
| **Labor total** | **4,400** | | **539,000,000** |
| Other cost on the sheets, charter budget lines 2 to 5 | | | 133,000,000 |
| Contingency reserve, charter budget line 6, held at project level | | | 28,000,000 |
| **Total** | | | **700,000,000** |

### Phase 1.1 Project Management

#### 1.1.1.1 Kickoff and team mobilisation

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Kickoff and team mobilisation |
| Code of Accounts | 1.1.1.1 |
| Responsible Person | PM |
| Description of Work | Hold the kickoff with the sponsor and the Center Director, walk the approved charter through with the team, and mobilise the five full-time staff. Procure and issue the laptops, tools, and licences the team needs to start. |
| Assumptions and Constraints | The sponsor names the project manager on or before 14 September 2026, and the part-time mobile developer is not mobilised here but joins after M2. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. M0 project kickoff, charter approved, team mobilised |
| Due Dates | <mark>Mon 14 September 2026 to Fri 18 September 2026; M0 on Mon 14 September 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.1.1.1-A1 | Kickoff meeting and charter walkthrough | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| 1.1.1.1-A2 | Team onboarding, accounts, and workspace | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| 1.1.1.1-A3 | Procure and issue laptops and licences | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| 1.1.1.1-A4 | Development tools and licences | | | | | 1 | 8,700,000 | 8,700,000 | 8,700,000 |
| 1.1.1.1-A5 | Team workspace and laptops | | | | | 1 | 9,000,000 | 9,000,000 | 9,000,000 |
| | **Work package total** | | **40** | | **6,500,000** | | | **17,700,000** | **24,200,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every team member has an account, a machine, and repository access before the first workshop. |
| Acceptance Criteria | Kickoff minutes signed by the sponsor and the project manager named in writing. |
| Technical Information | Repository, issue tracker, and build account created under the supplier's organisation. |
| Agreement Information | Supplier contract for the 700,000,000 VND scope, signed before M0. |

*Page 1 of 1*
#### 1.1.1.2 Project management plan and schedule baseline

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Project management plan and schedule baseline |
| Code of Accounts | 1.1.1.2 |
| Responsible Person | PM |
| Description of Work | Produce the project management plan, the schedule baseline against M0 to M7, the resource plan, and the communication plan, and have the sponsor accept them. |
| Assumptions and Constraints | The charter milestone dates are fixed and are not renegotiated here. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Project management plan accepted by the sponsor |
| Due Dates | <mark>Mon 21 September 2026 to Fri 2 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.1.1.2-A1 | Schedule baseline and resource plan | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| 1.1.1.2-A2 | Communication and stakeholder plan | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| 1.1.1.2-A3 | Baseline review and acceptance | PM | 20 | 162,500 | 3,250,000 | | | | 3,250,000 |
| | **Work package total** | | **60** | | **9,750,000** | | | **0** | **9,750,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every charter milestone appears in the schedule with an owner and a predecessor. |
| Acceptance Criteria | Sponsor accepts the plan in writing before the requirement baseline at M1. |
| Technical Information | Resource levelling of the effort estimates in this dictionary happens here, in Develop Schedule, not in the WBS. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.1.1.3 Weekly status reporting and sponsor governance

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Weekly status reporting and sponsor governance |
| Code of Accounts | 1.1.1.3 |
| Responsible Person | PM |
| Description of Work | Produce the weekly status report to the sponsor and the Center Director for the whole project, run the milestone gate reviews at M1 to M7, and carry escalations within two working days. |
| Assumptions and Constraints | Declared level of effort: the package runs the full 21 weeks by nature and is one of the two exceptions to the 8 to 80 hour rule. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Weekly report issued every week from M0<br>2. Gate review held at each of M1 to M7 |
| Due Dates | <mark>Mon 14 September 2026 to Fri 5 February 2027, weekly</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.1.1.3-A1 | Weekly status report, 21 weeks | PM | 84 | 162,500 | 13,650,000 | | | | 13,650,000 |
| 1.1.1.3-A2 | Milestone gate reviews M1 to M7 | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| 1.1.1.3-A3 | Sponsor escalations and decision log | PM | 12 | 162,500 | 1,950,000 | | | | 1,950,000 |
| | **Work package total** | | **120** | | **19,500,000** | | | **0** | **19,500,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No week without a report; every escalation reaches the sponsor within 2 working days. |
| Acceptance Criteria | Sponsor confirms at closeout that the reporting obligation was met. |
| Technical Information | The report template is fixed at M1 so the variance series stays comparable. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.1.1.4 Risk, issue, and change control

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Risk, issue, and change control |
| Code of Accounts | 1.1.1.4 |
| Responsible Person | PM |
| Description of Work | Maintain the risk register R1 to R12 with owners and responses, run the issue log, and raise change requests into Perform Integrated Change Control with their impact assessed against the reserve. |
| Assumptions and Constraints | Change requests are outputs of the controlling processes 5.5 and 5.6, so this package raises and tracks them once the project is executing. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Risk register baselined at M1<br>2. Weekly risk review from M1 |
| Due Dates | <mark>Mon 14 September 2026 to Fri 5 February 2027, weekly</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.1.1.4-A1 | Maintain the risk register R1 to R12 | PM | 32 | 162,500 | 5,200,000 | | | | 5,200,000 |
| 1.1.1.4-A2 | Weekly risk and issue review | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| 1.1.1.4-A3 | Raise and track change requests | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| | **Work package total** | | **80** | | **13,000,000** | | | **0** | **13,000,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every risk carries an owner and a response; every change request carries an impact assessment. |
| Acceptance Criteria | Sponsor accepts the risk register at M1 and the closeout risk position at M7. |
| Technical Information | Change requests draw on the 28,000,000 VND contingency reserve held at project level in the roll-up of Part 2. The R4 pairing on scheduling and tuition is delivered through the cross-reviews in 1.4.3.1 and 1.5.5.1 and the shared repository of 1.2.3.1. |
| Agreement Information |  |

*Page 1 of 1*
### Phase 1.2 Requirements

#### 1.2.1.1 Stakeholder workshops and current-process study

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Stakeholder workshops and current-process study |
| Code of Accounts | 1.2.1.1 |
| Responsible Person | PM |
| Description of Work | Run requirement workshops with the seven roles of charter 1.1.3 and study the current paper registers, Excel workbooks, and group-chat practice. Write the workshop notes the specification is drafted from. |
| Assumptions and Constraints | The Academic Manager and the Accountant are available four hours a week, per charter assumption 10. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Workshop series complete |
| Due Dates | <mark>Mon 14 September 2026 to Tue 22 September 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.1.1-A1 | Workshops with the seven roles | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| 1.2.1.1-A2 | Current process and source document study | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| 1.2.1.1-A3 | Workshop notes and open question list | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| | **Work package total** | | **48** | | **7,800,000** | | | **0** | **7,800,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every one of the seven roles is represented in at least one workshop. |
| Acceptance Criteria | Notes confirmed by the Academic Manager and the Accountant. |
| Technical Information | The source workbooks collected here are the input to 1.7.1.1. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.2.1.2 Functional requirements specification, F01 to F12

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Functional requirements specification, F01 to F12 |
| Code of Accounts | 1.2.1.2 |
| Responsible Person | PM |
| Description of Work | Draft the twelve functions of charter 1.1.4 with a description and a primary actor for each, and walk the draft through with the business owner of each area. |
| Assumptions and Constraints | Tuition, discount, and refund rules are frozen at M1 with written sign-off, the charter response to risk R2. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Draft specification circulated<br>2. Business walkthrough complete |
| Due Dates | <mark>Thu 17 September 2026 to Tue 29 September 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.1.2-A1 | Draft F01 to F12 with descriptions and actors | PM | 56 | 162,500 | 9,100,000 | | | | 9,100,000 |
| 1.2.1.2-A2 | Walkthrough with the business owners | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| | **Work package total** | | **72** | | **11,700,000** | | | **0** | **11,700,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every function names a primary actor; no function is described only by its happy path. |
| Acceptance Criteria | Business owners confirm each function in their area before the review in 1.2.2.2. |
| Technical Information | The data model sketch that supports the twelve functions is built in 1.3.1.2. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.2.1.3 Nonfunctional requirements specification, A01 to A12

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Nonfunctional requirements specification, A01 to A12 |
| Code of Accounts | 1.2.1.3 |
| Responsible Person | PM |
| Description of Work | Draft the twelve acceptance criteria A01 to A12 of charter 1.3 as measurable thresholds and check each for technical feasibility. |
| Assumptions and Constraints | Concurrency and capacity figures come from the charter assumptions and are rechecked against real usage in the warranty month. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Nonfunctional criteria drafted and feasibility checked |
| Due Dates | <mark>Wed 23 September 2026 to Tue 29 September 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.1.3-A1 | Draft A01 to A12 as measurable thresholds | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| 1.2.1.3-A2 | Technical feasibility check | DEV3 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| | **Work package total** | | **40** | | **5,800,000** | | | **0** | **5,800,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every criterion is a measurable threshold, not a judgement. |
| Acceptance Criteria | Each criterion has a named verification method before the baseline at M1. |
| Technical Information | The thresholds become the test targets for 1.6.1.3 and 1.6.1.4. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.2.1.4 Exception and failure behaviour catalogue

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Exception and failure behaviour catalogue |
| Code of Accounts | 1.2.1.4 |
| Responsible Person | PM |
| Description of Work | Write the fourteen exception cases of charter 1.1.5 and the behaviour each of them requires. |
| Assumptions and Constraints | Exception behaviour is in scope on the same terms as the functions and is tested with the same weight. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Exception catalogue complete |
| Due Dates | <mark>Thu 24 September 2026 to Wed 30 September 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.1.4-A1 | Write the fourteen exception cases | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| 1.2.1.4-A2 | Technical review of the failure paths | DEV3 | 8 | 118,750 | 950,000 | | | | 950,000 |
| | **Work package total** | | **32** | | **4,850,000** | | | **0** | **4,850,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every function has its failure behaviour written before the baseline. |
| Acceptance Criteria | Academic Manager and Accountant confirm the operational cases in their areas. |
| Technical Information | The catalogue is the source of the negative test cases in 1.4.3.2, 1.5.5.2, and 1.6.1.6. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.2.2.1 Requirements traceability matrix

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Requirements traceability matrix |
| Code of Accounts | 1.2.2.1 |
| Responsible Person | PM |
| Description of Work | Build the requirements traceability matrix on form 2.7, tracing every business, functional, and nonfunctional requirement to an objective, a deliverable, a verification, and a validation, with the inter-requirements matrix beside it. |
| Assumptions and Constraints | The matrix is an output of Collect Requirements, so its deliverable column is completed once the WBS codes exist. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Matrix issued with the requirement baseline |
| Due Dates | <mark>Mon 28 September 2026 to Wed 30 September 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.2.1-A1 | Build the business, functional, and nonfunctional rows | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| 1.2.2.1-A2 | Complete the verification and validation columns | QA1 | 16 | 93,750 | 1,500,000 | | | | 1,500,000 |
| | **Work package total** | | **32** | | **4,100,000** | | | **0** | **4,100,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No requirement without a business objective, a deliverable, a verification, and a validation. |
| Acceptance Criteria | Matrix accepted with the requirement baseline at M1. |
| Technical Information | Maintained through execution and updated by the controlling processes 5.5 and 5.6. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.2.2.2 Requirements peer review and rework

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Requirements peer review and rework |
| Code of Accounts | 1.2.2.2 |
| Responsible Person | QA1 |
| Description of Work | Review the drafted specification against the workshop notes and the charter, record findings, and rework. The reviewer is the QA engineer, who did not write the specification. |
| Assumptions and Constraints | The QA engineer acts as the second reader of the specification, the charter response to risk R9. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Review findings closed |
| Due Dates | <mark>Wed 30 September 2026 to Thu 1 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.2.2-A1 | Requirements review against the notes and the charter | QA1 | 24 | 93,750 | 2,250,000 | | | | 2,250,000 |
| 1.2.2.2-A2 | Technical review of the data model | DEV3 | 12 | 118,750 | 1,425,000 | | | | 1,425,000 |
| 1.2.2.2-A3 | Rework of the specification | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| | **Work package total** | | **44** | | **4,975,000** | | | **0** | **4,975,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No reviewer reviews their own work; every finding is closed or explicitly accepted. |
| Acceptance Criteria | Finding list closed and signed by the reviewer before M1. |
| Technical Information |  |
| Agreement Information |  |

*Page 1 of 1*
#### 1.2.2.3 Requirements acceptance and baseline

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Requirements acceptance and baseline |
| Code of Accounts | 1.2.2.3 |
| Responsible Person | PM |
| Description of Work | Present the specification to the sponsor and the Center Director, obtain written sign-off, and baseline it. |
| Assumptions and Constraints | A slip here moves every downstream milestone, which is why it is a gate rather than a review. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. M1 requirement specification approved and baselined<br>2. D1 delivered |
| Due Dates | <mark>Fri 2 October 2026; M1 on Fri 2 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.2.3-A1 | Baseline presentation and written sign-off | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| | **Work package total** | | **8** | | **1,300,000** | | | **0** | **1,300,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The baseline is a signed document, not a circulated draft. |
| Acceptance Criteria | Signed acceptance record of D1. |
| Technical Information | The baselined version is tagged and referenced by every later change request. |
| Agreement Information | Acceptance record forms part of the supplier contract file. |

*Page 1 of 1*
#### 1.2.3.1 Repository, coding convention, and build pipeline

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Repository, coding convention, and build pipeline |
| Code of Accounts | 1.2.3.1 |
| Responsible Person | DEV1 |
| Description of Work | Stand up the source repository, the branching and coding convention that acceptance criterion A10 requires, and the build and test pipeline, so that construction starts against a working pipeline rather than building one. |
| Assumptions and Constraints | The environments themselves are provisioned in 1.2.3.5, and staging in 1.8.1.1. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Pipeline green on an empty build |
| Due Dates | <mark>Mon 14 September 2026 to Fri 2 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.3.1-A1 | Repository, branching, and coding convention | DEV1 | 32 | 118,750 | 3,800,000 | | | | 3,800,000 |
| 1.2.3.1-A2 | Build and test pipeline | DEV1 | 40 | 118,750 | 4,750,000 | | | | 4,750,000 |
| | **Work package total** | | **72** | | **8,550,000** | | | **0** | **8,550,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | A commit runs the build and the test suite without manual steps. |
| Acceptance Criteria | Every developer builds and runs the system locally and on the test environment before M2, and on staging before the M3 demo. |
| Technical Information | The coding convention is the one handed over in 1.8.3.1; the shared repository is part of the charter response to risk R4. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.2.3.2 Notification gateway proof of concept

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Notification gateway proof of concept |
| Code of Accounts | 1.2.3.2 |
| Responsible Person | DEV2 |
| Description of Work | Prove the email and SMS gateway behind a single interface before the design baseline, including the delivery-state callback and the low-credit alert, and evaluate a second provider as fallback. |
| Assumptions and Constraints | This is the charter response to risk R5; gateway credit for development is charged to 1.5.2.2. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Gateway proof of concept accepted<br>2. Fallback provider identified |
| Due Dates | <mark>Mon 21 September 2026 to Fri 2 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.3.2-A1 | Gateway integration behind a single interface | DEV2 | 48 | 118,750 | 5,700,000 | | | | 5,700,000 |
| 1.2.3.2-A2 | Delivery-state callback and low-credit alert | DEV2 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.2.3.2-A3 | Second provider evaluation | DEV2 | 12 | 118,750 | 1,425,000 | | | | 1,425,000 |
| | **Work package total** | | **80** | | **9,500,000** | | | **0** | **9,500,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No gateway detail leaks outside the interface, so a provider can be swapped without touching F09. |
| Acceptance Criteria | Proof of concept demonstrated before the design baseline at M2. |
| Technical Information | The interface designed here is the one F09 is built against in 1.5.2.2. |
| Agreement Information | Gateway provider terms reviewed; the contract is signed by the center, not the supplier. |

*Page 1 of 1*
#### 1.2.3.3 Cross-platform framework proof

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Cross-platform framework proof |
| Code of Accounts | 1.2.3.3 |
| Responsible Person | DEV3 |
| Description of Work | Prove the chosen cross-platform framework on Android and iOS, covering push registration, secure token storage, and the read-only last-synced view, so the platform half of risk R12 closes before any application code is committed. |
| Assumptions and Constraints | <mark>One cross-platform codebase, Flutter or React Native</mark>, chosen here and fixed for the project. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Framework proven on Android and iOS |
| Due Dates | <mark>Mon 21 September 2026 to Fri 2 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.3.3-A1 | Framework spike on Android and iOS | DEV3 | 24 | 118,750 | 2,850,000 | | | | 2,850,000 |
| 1.2.3.3-A2 | Push registration and secure token storage | DEV3 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| | **Work package total** | | **40** | | **4,750,000** | | | **0** | **4,750,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The same codebase runs on both platforms with no fork of the business logic. |
| Acceptance Criteria | Both platforms demonstrated before the design baseline at M2. |
| Technical Information | Closes the framework half of risk R12; the store half is closed in 1.9. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.2.3.4 User interface prototype for business validation

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | User interface prototype for business validation |
| Code of Accounts | 1.2.3.4 |
| Responsible Person | DEV2 |
| Description of Work | Build a clickable prototype of the enrollment, attendance, and payment screens so the business owners validate the interface against their daily work before the design is baselined. |
| Assumptions and Constraints | The prototype is throwaway and is not the basis of the delivered interface. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Prototype walkthrough with front-desk staff and teachers |
| Due Dates | <mark>Mon 21 September 2026 to Fri 2 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.3.4-A1 | Clickable prototype of the three daily paths | DEV2 | 28 | 118,750 | 3,325,000 | | | | 3,325,000 |
| 1.2.3.4-A2 | Walkthrough with front-desk staff and teachers | DEV2 | 12 | 118,750 | 1,425,000 | | | | 1,425,000 |
| | **Work package total** | | **40** | | **4,750,000** | | | **0** | **4,750,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The three daily paths are walked by the people who will use them, not by the project team. |
| Acceptance Criteria | Prototype findings folded into the web interface design in 1.3.1.4. |
| Technical Information | Serves the three-click rule of acceptance criterion A08. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.2.3.5 Development and test environment provisioning

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Development and test environment provisioning |
| Code of Accounts | 1.2.3.5 |
| Responsible Person | DEV1 |
| Description of Work | Provision the development and test environments that the team builds and tests against from the first iteration. |
| Assumptions and Constraints | Staging and production are provisioned later in 1.8.1.1, on the same cloud provider. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Development and test environments available |
| Due Dates | <mark>Mon 14 September 2026 to Fri 2 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.3.5-A1 | Development and test environment provisioning | DEV1 | 28 | 118,750 | 3,325,000 | | | | 3,325,000 |
| | **Work package total** | | **28** | | **3,325,000** | | | **0** | **3,325,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Both environments match the target configuration of the architecture design. |
| Acceptance Criteria | Every developer runs the build on the test environment before M2. |
| Technical Information | Provisioned under the supplier's account until the production accounts are opened in 1.8.1.1. |
| Agreement Information |  |

*Page 1 of 1*
### Phase 1.3 Design

#### 1.3.1.1 Architecture, security, and personal-data design

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Architecture, security, and personal-data design |
| Code of Accounts | 1.3.1.1 |
| Responsible Person | DEV3 |
| Description of Work | Design the application architecture, the deployment topology across the cloud server and staging, the authentication and authorisation model for the seven roles, and the personal-data handling that charter criterion A04 requires. |
| Assumptions and Constraints | <mark>The Law on Personal Data Protection in force from 1 January 2026</mark> applies to guardian and student data. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Architecture accepted into the design baseline |
| Due Dates | <mark>Mon 5 October 2026 to Fri 9 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.1.1-A1 | Application architecture and deployment topology | DEV3 | 36 | 118,750 | 4,275,000 | | | | 4,275,000 |
| 1.3.1.1-A2 | Security model and personal-data design | DEV3 | 24 | 118,750 | 2,850,000 | | | | 2,850,000 |
| 1.3.1.1-A3 | Architecture review with the sponsor | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| | **Work package total** | | **76** | | **9,725,000** | | | **0** | **9,725,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every request authorised on the server; no design that stores a recoverable password. |
| Acceptance Criteria | Accepted at the design baseline in 1.3.2.3 and verified by the security test in 1.6.1.4. |
| Technical Information | Serves NFR04 and NFR11 of the traceability matrix. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.3.1.2 Database schema design

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Database schema design |
| Code of Accounts | 1.3.1.2 |
| Responsible Person | DEV1 |
| Description of Work | Sketch the data model behind F01 to F12 and design the shared database schema that is the single source of truth, with keys chosen so the migration in 1.7 reconciles record by record. |
| Assumptions and Constraints | One shared database serves web and mobile; <mark>3 years of session history</mark> is held without redesign. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Schema accepted into the design baseline |
| Due Dates | <mark>Mon 5 October 2026 to Mon 12 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.1.2-A1 | Data model sketch for the twelve functions | DEV3 | 24 | 118,750 | 2,850,000 | | | | 2,850,000 |
| 1.3.1.2-A2 | Entity and relationship design | DEV1 | 36 | 118,750 | 4,275,000 | | | | 4,275,000 |
| 1.3.1.2-A3 | Key design and migration reconciliation strategy | DEV1 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| | **Work package total** | | **76** | | **9,025,000** | | | **0** | **9,025,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No entity holds data that another entity also owns. |
| Acceptance Criteria | Accepted at 1.3.2.3 and proven by the trial migration in 1.7.1.2. |
| Technical Information | Schema documentation is part of the handover in 1.8.3.1. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.3.1.3 Server API contract

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Server API contract |
| Code of Accounts | 1.3.1.3 |
| Responsible Person | DEV2 |
| Description of Work | Specify the documented server API that serves the web application and the mobile application alike across F01 to F12, with versioning, error contracts, and per-endpoint authorisation. |
| Assumptions and Constraints | The mobile application uses the same API and the same accounts; no function is application-only. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. API contract accepted into the design baseline |
| Due Dates | <mark>Mon 5 October 2026 to Mon 12 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.1.3-A1 | Endpoint design and error contract | DEV2 | 36 | 118,750 | 4,275,000 | | | | 4,275,000 |
| 1.3.1.3-A2 | Versioning, authorisation rules, and documentation | DEV2 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| | **Work package total** | | **52** | | **6,175,000** | | | **0** | **6,175,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every endpoint is documented before it is built. |
| Acceptance Criteria | Accepted at 1.3.2.3; the API documentation is handed over in 1.8.3.1. |
| Technical Information | The contract is the interface the notification gateway of 1.2.3.2 sits behind. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.3.1.4 Web user interface design

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Web user interface design |
| Code of Accounts | 1.3.1.4 |
| Responsible Person | DEV1 |
| Description of Work | Design the Vietnamese web interface for the staff roles, folding in the prototype findings from 1.2.3.4, with attendance, payment recording, and enrollment each within three clicks of the home screen. |
| Assumptions and Constraints | Staff use the web application from a desktop browser and the interface is Vietnamese only. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Web interface design accepted into the design baseline |
| Due Dates | <mark>Wed 7 October 2026 to Wed 14 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.1.4-A1 | Screen flows and layouts for staff roles | DEV1 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.3.1.4-A2 | Navigation design against the three-click rule | DEV1 | 8 | 118,750 | 950,000 | | | | 950,000 |
| | **Work package total** | | **28** | | **3,325,000** | | | **0** | **3,325,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Click count measured on the three daily paths during design, not after build. |
| Acceptance Criteria | Accepted at 1.3.2.3; verified against NFR08 during UAT. |
| Technical Information | Supports the latest two versions of Chrome, Edge, and Firefox. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.3.1.5 Mobile application design

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Mobile application design |
| Code of Accounts | 1.3.1.5 |
| Responsible Person | DEV3 |
| Description of Work | Design the parent and teacher application on the framework proven in 1.2.3.3, so that the application design sits inside the M2 baseline as the charter requires. |
| Assumptions and Constraints | <mark>The mobile developer joins after M2, so DEV3 designs the application and hands the design over at mobilisation.</mark> <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Application design accepted into the design baseline |
| Due Dates | <mark>Thu 8 October 2026 to Thu 15 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.1.5-A1 | Application screen design for parent and teacher | DEV3 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.3.1.5-A2 | Offline and degraded-state design | DEV3 | 8 | 118,750 | 950,000 | | | | 950,000 |
| | **Work package total** | | **28** | | **3,325,000** | | | **0** | **3,325,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every F12 function is within three taps of the home screen in the design. |
| Acceptance Criteria | Accepted at 1.3.2.3; built against in 1.4.4.1 and 1.5.4. |
| Technical Information | The read-only last-synced view is designed here, per the connectivity exception case. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.3.2.1 Design review and rework

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Design review and rework |
| Code of Accounts | 1.3.2.1 |
| Responsible Person | QA1 |
| Description of Work | Review the architecture, schema, API contract, and interface designs against the requirement baseline, cross-review between developers who did not write them, and rework against the findings. |
| Assumptions and Constraints | No designer reviews their own design. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Design review findings closed |
| Due Dates | <mark>Tue 13 October 2026 to Thu 15 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.2.1-A1 | Design review against the requirement baseline | QA1 | 16 | 93,750 | 1,500,000 | | | | 1,500,000 |
| 1.3.2.1-A2 | Cross-review of the schema and architecture | DEV2 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.3.2.1-A3 | Rework coordination and finding closure | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| | **Work package total** | | **52** | | **6,475,000** | | | **0** | **6,475,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every requirement in the baseline maps to something in the design. |
| Acceptance Criteria | Finding list closed before the baseline gate at M2. |
| Technical Information |  |
| Agreement Information |  |

*Page 1 of 1*
#### 1.3.2.2 Test plan and test strategy

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Test plan and test strategy |
| Code of Accounts | 1.3.2.2 |
| Responsible Person | QA1 |
| Description of Work | Write the test plan and strategy across unit, integration, system, performance, capacity, security, and acceptance testing on web, Android, and iOS, with entry and exit criteria and the defect severity definitions the warranty terms depend on. |
| Assumptions and Constraints | The QA engineer writes from the requirement baseline as second reader, the charter response to risk R9. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Test plan accepted into the design baseline |
| Due Dates | <mark>Mon 5 October 2026 to Thu 15 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.2.2-A1 | Test plan across all levels and platforms | QA1 | 48 | 93,750 | 4,500,000 | | | | 4,500,000 |
| 1.3.2.2-A2 | Entry and exit criteria and severity definitions | QA1 | 16 | 93,750 | 1,500,000 | | | | 1,500,000 |
| 1.3.2.2-A3 | Test plan approval with the sponsor | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| | **Work package total** | | **72** | | **7,300,000** | | | **0** | **7,300,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Severity definitions match the charter warranty response targets. |
| Acceptance Criteria | Accepted at 1.3.2.3; the plan is part of D5. |
| Technical Information | The UAT test set is agreed later at M5 in 1.6.2.1 against this plan. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.3.2.3 Design baseline acceptance

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Design baseline acceptance |
| Code of Accounts | 1.3.2.3 |
| Responsible Person | PM |
| Description of Work | Present the architecture, schema, API contract, interface designs, and test plan to the customer, obtain acceptance, and baseline the design. |
| Assumptions and Constraints | Acceptance is a gate: construction does not begin against an unaccepted design. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. M2 design baseline approved, including the API contract and the application design<br>2. D2 delivered |
| Due Dates | <mark>Fri 16 October 2026; M2 on Fri 16 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.2.3-A1 | Design baseline presentation and acceptance | PM | 20 | 162,500 | 3,250,000 | | | | 3,250,000 |
| | **Work package total** | | **20** | | **3,250,000** | | | **0** | **3,250,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The baseline is signed, versioned, and tagged. |
| Acceptance Criteria | Signed acceptance record of D2. |
| Technical Information | The baselined design is the reference for every later change request. |
| Agreement Information | Acceptance record filed with the supplier contract. |

*Page 1 of 1*
### Phase 1.4 Construction Iteration 1

#### 1.4.1.1 F01 Authentication and access control

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F01 Authentication and access control |
| Code of Accounts | 1.4.1.1 |
| Responsible Person | DEV3 |
| Description of Work | Build F01 per charter 1.1.4: account creation, username and password authentication, password reset, idle session timeout, and role-based permission for the seven roles. |
| Assumptions and Constraints | Passwords are never stored or recoverable in readable form and every request is authorised on the server. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. F01 demonstrated at the iteration 1 demo |
| Due Dates | <mark>Mon 19 October 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.1.1-A1 | Account, authentication, and password reset | DEV3 | 32 | 118,750 | 3,800,000 | | | | 3,800,000 |
| 1.4.1.1-A2 | Role and branch permission model | DEV3 | 28 | 118,750 | 3,325,000 | | | | 3,325,000 |
| | **Work package total** | | **60** | | **7,125,000** | | | **0** | **7,125,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criterion A04; no screen or record reachable by a role that does not own it. |
| Acceptance Criteria | Permission matrix passes for all seven roles at the M3 demo. |
| Technical Information | The same accounts serve the mobile application through the API. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.4.1.2 F02 Student profile and guardian records

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F02 Student profile and guardian records |
| Code of Accounts | 1.4.1.2 |
| Responsible Person | DEV2 |
| Description of Work | Build the profile half of F02 per charter 1.1.4: the student profile with personal data, guardian and contact details, source, and notes. Enrollment and its refusal rules are carried by 1.4.1.4. |
| Assumptions and Constraints | Guardian consent for notification is recorded on the profile, per acceptance criterion A04. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. F02 profile demonstrated at the iteration 1 demo |
| Due Dates | <mark>Mon 19 October 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.1.2-A1 | Student profile and guardian records | DEV2 | 30 | 118,750 | 3,562,500 | | | | 3,562,500 |
| | **Work package total** | | **30** | | **3,562,500** | | | **0** | **3,562,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | One student record; the same person is never held twice. |
| Acceptance Criteria | A test cohort is created with no duplicate record. |
| Technical Information | Serves BR01 and the profile half of FR02. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.4.1.3 F03 Course and curriculum catalog

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F03 Course and curriculum catalog |
| Code of Accounts | 1.4.1.3 |
| Responsible Person | DEV3 |
| Description of Work | Build F03 per charter 1.1.4: course code, level, session count and length, standard fee, prerequisite, and syllabus, versioned so that an edit leaves already-opened classes unchanged. |
| Assumptions and Constraints | Course versioning is a hard requirement: without it historical classes change when a fee is edited. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. F03 demonstrated at the iteration 1 demo |
| Due Dates | <mark>Mon 19 October 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.1.3-A1 | Course, level, fee, and syllabus records | DEV3 | 32 | 118,750 | 3,800,000 | | | | 3,800,000 |
| 1.4.1.3-A2 | Course versioning and its effect on classes | DEV3 | 28 | 118,750 | 3,325,000 | | | | 3,325,000 |
| | **Work package total** | | **60** | | **7,125,000** | | | **0** | **7,125,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | An edit to a course leaves every already-opened class untouched. |
| Acceptance Criteria | Academic Manager edits a course with open classes and the classes do not move. |
| Technical Information | Course versions are the input to class generation in 1.4.2.1. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.4.1.4 F02 Enrollment, transfer, reservation, and withdrawal

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F02 Enrollment, transfer, reservation, and withdrawal |
| Code of Accounts | 1.4.1.4 |
| Responsible Person | DEV2 |
| Description of Work | Build the enrollment half of F02 per charter 1.1.4: enrollment into an open class, transfer, seat reservation, and withdrawal with a refund calculation, refusing a full class or a timetable collision. |
| Assumptions and Constraints | The refund rules are those frozen at M1, and a withdrawal is a proposal until the Accountant approves it. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. F02 enrollment demonstrated at the iteration 1 demo |
| Due Dates | <mark>Mon 19 October 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.1.4-A1 | Enrollment, transfer, reservation, and withdrawal | DEV2 | 40 | 118,750 | 4,750,000 | | | | 4,750,000 |
| 1.4.1.4-A2 | Refusal rules for full class and collision | DEV2 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| | **Work package total** | | **60** | | **7,125,000** | | | **0** | **7,125,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Both refusal cases are enforced by the server, not only by the screen. |
| Acceptance Criteria | A test cohort is enrolled, transferred, and withdrawn without a manual correction. |
| Technical Information | Serves BR01 and FR02; the refund proposal path is shared with 1.5.1.1. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.4.2.1 F04 Class opening, session calendar, and postponement

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F04 Class opening, session calendar, and postponement |
| Code of Accounts | 1.4.2.1 |
| Responsible Person | DEV1 |
| Description of Work | Build the scheduling half of F04 per charter 1.1.4: class opening from a course version, generation of the whole session calendar, room and teacher assignment, and recalculation on postponement. Conflict detection is carried by 1.4.2.3. |
| Assumptions and Constraints | The charter assigns this to the developer with prior scheduling experience and builds it first, timeboxed, which is the response to risk R7. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. F04 scheduling demonstrated at the iteration 1 demo |
| Due Dates | <mark>Mon 19 October 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.2.1-A1 | Class opening and session calendar generation | DEV1 | 48 | 118,750 | 5,700,000 | | | | 5,700,000 |
| 1.4.2.1-A2 | Postponement and calendar recalculation | DEV1 | 32 | 118,750 | 3,800,000 | | | | 3,800,000 |
| | **Work package total** | | **80** | | **9,500,000** | | | **0** | **9,500,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | A postponed session recalculates the calendar without losing history. |
| Acceptance Criteria | Reviewed at the M3 demo, as the charter response to risk R7 requires. |
| Technical Information | The substitute-teacher and postponement exception cases are built here. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.4.2.2 F05 Attendance and make-up sessions

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F05 Attendance and make-up sessions |
| Code of Accounts | 1.4.2.2 |
| Responsible Person | DEV2 |
| Description of Work | Build F05 per charter 1.1.4: attendance marking in four states with remarks, make-up registration, attendance rate per student and per class, the late-entry stamp, and the daily exception list. |
| Assumptions and Constraints | A month containing missing attendance cannot be closed for payroll, which is what ties this package to 1.5.1.2. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. F05 demonstrated at the iteration 1 demo |
| Due Dates | <mark>Mon 19 October 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.2.2-A1 | Attendance marking, states, and remarks | DEV2 | 30 | 118,750 | 3,562,500 | | | | 3,562,500 |
| 1.4.2.2-A2 | Make-up sessions and attendance rate reporting | DEV2 | 24 | 118,750 | 2,850,000 | | | | 2,850,000 |
| 1.4.2.2-A3 | Late-entry stamping and daily exception list | DEV2 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| | **Work package total** | | **70** | | **8,312,500** | | | **0** | **8,312,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | A late entry is stamped as late with the name of whoever entered it. |
| Acceptance Criteria | Attendance figures match a hand count for a sample class over one month. |
| Technical Information | Attendance is the only source of teaching hours in 1.5.1.2. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.4.2.3 F04 Room, teacher, and class-time conflict detection

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F04 Room, teacher, and class-time conflict detection |
| Code of Accounts | 1.4.2.3 |
| Responsible Person | DEV1 |
| Description of Work | Build the conflict half of F04 per charter 1.1.4: detect and block conflicts on room, on teacher, and on class time at the moment a class or session is created or moved. |
| Assumptions and Constraints | Timeboxed and reviewed at the M3 demo, which is the charter response to risk R7. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Conflict test set passed<br>2. Reviewed at the iteration 1 demo |
| Due Dates | <mark>Mon 19 October 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.2.3-A1 | Room, teacher, and class-time conflict detection | DEV1 | 60 | 118,750 | 7,125,000 | | | | 7,125,000 |
| | **Work package total** | | **60** | | **7,125,000** | | | **0** | **7,125,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Zero conflicting bookings accepted; the check completes inside the 3 second screen budget. |
| Acceptance Criteria | Every conflict case in the test set is blocked at creation or at move time. |
| Technical Information | Serves BR02 and FR04. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.4.3.1 Iteration 1 code review and rework

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Iteration 1 code review and rework |
| Code of Accounts | 1.4.3.1 |
| Responsible Person | QA1 |
| Description of Work | Review the iteration 1 code against the design and the coding convention and rework against the findings. Nobody reviews their own code, so the package is owned by the QA engineer rather than by an author. |
| Assumptions and Constraints | Review is a work package of its own so the effort stays visible and cannot be dropped when a build runs late. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Iteration 1 review findings closed |
| Due Dates | <mark>Mon 9 November 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.3.1-A1 | Review of F01, F02, and F03 | DEV1 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.4.3.1-A2 | Review of F04 and F05 and rework | DEV3 | 40 | 118,750 | 4,750,000 | | | | 4,750,000 |
| 1.4.3.1-A3 | Review against the test plan | QA1 | 20 | 93,750 | 1,875,000 | | | | 1,875,000 |
| | **Work package total** | | **80** | | **9,000,000** | | | **0** | **9,000,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No author reviews their own work; every finding is closed or explicitly accepted. |
| Acceptance Criteria | Finding list closed before the M3 demo. |
| Technical Information | Part of the charter response to risk R4; the coding convention is the one set in 1.2.3.1. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.4.3.2 Iteration 1 testing, core platform

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Iteration 1 testing, core platform |
| Code of Accounts | 1.4.3.2 |
| Responsible Person | QA1 |
| Description of Work | Author the test cases for F01 to F03 from the requirement baseline and execute unit and integration testing on them, including the exception cases that belong to them. |
| Assumptions and Constraints | Testing is against the requirement baseline of M1, not against what was built. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Core platform test cycle complete |
| Due Dates | <mark>Mon 2 November 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.3.2-A1 | Test case authoring for F01 to F03 | QA1 | 12 | 93,750 | 1,125,000 | | | | 1,125,000 |
| 1.4.3.2-A2 | Unit and integration execution | QA1 | 32 | 93,750 | 3,000,000 | | | | 3,000,000 |
| 1.4.3.2-A3 | Exception case execution | QA1 | 10 | 93,750 | 937,500 | | | | 937,500 |
| 1.4.3.2-A4 | Defect logging and retest | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| | **Work package total** | | **62** | | **5,812,500** | | | **0** | **5,812,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every defect carries a severity from the definitions agreed at M2. |
| Acceptance Criteria | No open Critical or High defect in F01 to F03 at the M3 demo. |
| Technical Information | Defects go into the single project defect log consolidated in 1.6.2.1. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.4.3.3 Iteration 1 demo and acceptance

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Iteration 1 demo and acceptance |
| Code of Accounts | 1.4.3.3 |
| Responsible Person | PM |
| Description of Work | Demonstrate F01 to F05 and the application alpha from 1.4.4.1 to the customer, record the acceptance decision, and close the iteration. |
| Assumptions and Constraints | The M3 milestone releases the 25% payment tranche against the signed acceptance record. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. M3 iteration 1 demo accepted, F01 to F05, with the application alpha<br>2. D3 delivered |
| Due Dates | <mark>Fri 13 November 2026; M3 on Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.3.3-A1 | Demo preparation and delivery | PM | 30 | 162,500 | 4,875,000 | | | | 4,875,000 |
| 1.4.3.3-A2 | Acceptance walkthrough against the iteration scope | QA1 | 20 | 93,750 | 1,875,000 | | | | 1,875,000 |
| | **Work package total** | | **50** | | **6,750,000** | | | **0** | **6,750,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The demo runs on staging with migrated sample data, not on a developer machine. |
| Acceptance Criteria | Signed acceptance record of D3. |
| Technical Information | Scheduling is reviewed here specifically, as the charter response to risk R7 requires. |
| Agreement Information | Acceptance record releases the M3 payment tranche. |

*Page 1 of 1*
#### 1.4.3.4 Iteration 1 testing, scheduling and attendance

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Iteration 1 testing, scheduling and attendance |
| Code of Accounts | 1.4.3.4 |
| Responsible Person | QA1 |
| Description of Work | Execute unit and integration testing on F04 and F05 against the cases written in 1.3.2.2 and the exception catalogue of 1.2.1.4. |
| Assumptions and Constraints | The conflict test set is the measure for F04 and is run in full. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Scheduling and attendance test cycle complete |
| Due Dates | <mark>Mon 2 November 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.3.4-A1 | Unit and integration execution | QA1 | 32 | 93,750 | 3,000,000 | | | | 3,000,000 |
| 1.4.3.4-A2 | Exception case execution | QA1 | 10 | 93,750 | 937,500 | | | | 937,500 |
| 1.4.3.4-A3 | Defect logging and retest | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| | **Work package total** | | **50** | | **4,687,500** | | | **0** | **4,687,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every conflict case in the test set is executed, not only the happy paths. |
| Acceptance Criteria | No open Critical or High defect in F04 and F05 at the M3 demo. |
| Technical Information | Defects go into the single project defect log consolidated in 1.6.2.1. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.4.4.1 Application alpha, parent schedule, attendance, and scores

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Application alpha, parent schedule, attendance, and scores |
| Code of Accounts | 1.4.4.1 |
| Responsible Person | MOB1 |
| Description of Work | Build the application alpha of F12 per charter 1.1.4: the parent schedule, attendance, and score journeys against the API contract, with a signed internal build. The remaining journeys are carried by 1.5.4. |
| Assumptions and Constraints | <mark>The mobile developer joins after M2 and works 2.5 person-months to M5</mark>, so the alpha is the first application deliverable. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Application alpha at the M3 demo |
| Due Dates | <mark>Mon 19 October 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.4.1-A1 | Parent schedule, attendance, and score journeys | MOB1 | 55 | 122,500 | 6,737,500 | | | | 6,737,500 |
| 1.4.4.1-A2 | Platform build, signing, and internal distribution | MOB1 | 25 | 122,500 | 3,062,500 | | | | 3,062,500 |
| | **Work package total** | | **80** | | **9,800,000** | | | **0** | **9,800,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every alpha function within three taps; no personal data cached unencrypted on the device. |
| Acceptance Criteria | Alpha demonstrated at the M3 demo in 1.4.3.3. |
| Technical Information | Built against the design of 1.3.1.5 and the API contract of 1.3.1.3. |
| Agreement Information |  |

*Page 1 of 1*
### Phase 1.5 Construction Iteration 2

#### 1.5.1.1 F06 Invoicing, discounts, and aged debt

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F06 Invoicing, discounts, and aged debt |
| Code of Accounts | 1.5.1.1 |
| Responsible Person | DEV2 |
| Description of Work | Build the invoicing half of F06 per charter 1.1.4: invoice generation from the course fee, the four discount policies, installment plans, and the aged debt list per student, class, and branch. Payments are carried by 1.5.1.3. |
| Assumptions and Constraints | The rules are those frozen at M1, and the charter assigns this to the developer with prior billing experience. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. F06 invoicing demonstrated at the iteration 2 review |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.1.1-A1 | Invoice generation, discounts, and installments | DEV2 | 48 | 118,750 | 5,700,000 | | | | 5,700,000 |
| 1.5.1.1-A2 | Aged debt list per student and branch | DEV2 | 22 | 118,750 | 2,612,500 | | | | 2,612,500 |
| | **Work package total** | | **70** | | **8,312,500** | | | **0** | **8,312,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | Invoice totals match the policy worked examples. |
| Acceptance Criteria | Accountant reconciles one term of test invoices with no manual correction. |
| Technical Information | Serves BR03 and FR06; the overdue percentage it reports is the business case measure. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.5.1.2 F07 Teacher records and teaching-hour payroll

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F07 Teacher records and teaching-hour payroll |
| Code of Accounts | 1.5.1.2 |
| Responsible Person | DEV2 |
| Description of Work | Build F07 per charter 1.1.4: teacher profiles and rates, the monthly teaching-hour sheet aggregated from delivered sessions, allowances and deductions, the approval workflow, and the Excel export. |
| Assumptions and Constraints | Hours are credited to whoever actually taught, and the person who recorded the attendance never approves the sheet. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. F07 demonstrated at the iteration 2 review |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.1.2-A1 | Teacher records, rates, and the monthly sheet | DEV2 | 18 | 118,750 | 2,137,500 | | | | 2,137,500 |
| 1.5.1.2-A2 | Sheet workflow, approval separation, and export | DEV2 | 12 | 118,750 | 1,425,000 | | | | 1,425,000 |
| | **Work package total** | | **30** | | **3,562,500** | | | **0** | **3,562,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | A month containing missing attendance cannot be closed. |
| Acceptance Criteria | Accountant closes one test month with zero manual adjustment rows. |
| Technical Information | Reads attendance from F05 only; there is no second entry path for teaching hours. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.5.1.3 F06 Payments, receipts, and unmatched payments

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F06 Payments, receipts, and unmatched payments |
| Code of Accounts | 1.5.1.3 |
| Responsible Person | DEV2 |
| Description of Work | Build the payment half of F06 per charter 1.1.4: cash and bank-transfer recording, receipts, the outstanding balance, the unmatched payment list, credits, and reversing entries. |
| Assumptions and Constraints | No overdue reminder is sent to a student with an unmatched payment on file, per charter 1.1.5. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. F06 payments demonstrated at the iteration 2 review |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.1.3-A1 | Payment recording, receipts, and balance | DEV2 | 40 | 118,750 | 4,750,000 | | | | 4,750,000 |
| 1.5.1.3-A2 | Unmatched payments, credits, and reversing entries | DEV2 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| | **Work package total** | | **60** | | **7,125,000** | | | **0** | **7,125,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | A receipt is never deleted; a reversal posts a reversing entry and both stay in the audit log. |
| Acceptance Criteria | Accountant reconciles one term of test payments, including an overpayment and a reversal. |
| Technical Information | Carries the unmatched transfer, overpayment, and reversal exception cases of charter 1.1.5. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.5.2.1 F08 Assessment, progress reports, and course evaluation

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F08 Assessment, progress reports, and course evaluation |
| Code of Accounts | 1.5.2.1 |
| Responsible Person | DEV3 |
| Description of Work | Build F08 per charter 1.1.4: score recording and comments, pass or fail computation against the course rule, the printable progress report, the class result summary, and the end-of-course evaluation. |
| Assumptions and Constraints | The pass rule is part of the course definition and is versioned with it. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. F08 demonstrated at the iteration 2 review |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.2.1-A1 | Score entry, comments, and result computation | DEV3 | 36 | 118,750 | 4,275,000 | | | | 4,275,000 |
| 1.5.2.1-A2 | Progress report and class result summary | DEV3 | 24 | 118,750 | 2,850,000 | | | | 2,850,000 |
| 1.5.2.1-A3 | End-of-course evaluation and its reporting | DEV3 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| | **Work package total** | | **80** | | **9,500,000** | | | **0** | **9,500,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every pass and fail boundary case in the test set computes correctly. |
| Acceptance Criteria | Academic Manager checks one completed course and agrees every result. |
| Technical Information | The evaluation is collected from the application as well as the web, through the same API. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.5.2.2 F09 Notification and internal communication

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F09 Notification and internal communication |
| Code of Accounts | 1.5.2.2 |
| Responsible Person | DEV3 |
| Description of Work | Build F09 per charter 1.1.4: email and SMS from templates for the seven events, manual and scheduled sending, the delivery log with retry and failure reasons, the low-credit alert, announcements, the class notice board, and parent messages. |
| Assumptions and Constraints | Built against the gateway interface proven in 1.2.3.2; <mark>4,000,000 VND of development and test gateway credit</mark> from charter budget line 2 is spent here. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. F09 demonstrated at the iteration 2 review |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.2.2-A1 | Templates, manual send, and scheduled send | DEV3 | 28 | 118,750 | 3,325,000 | | | | 3,325,000 |
| 1.5.2.2-A2 | Delivery log, retry, and low-credit alert | DEV3 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.5.2.2-A3 | Announcements, notice board, and parent messages | DEV3 | 12 | 118,750 | 1,425,000 | | | | 1,425,000 |
| 1.5.2.2-A4 | Development and test gateway credit | | | | | 1 | 4,000,000 | 4,000,000 | 4,000,000 |
| | **Work package total** | | **60** | | **7,125,000** | | | **4,000,000** | **11,125,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No failed notification is dropped without a record. |
| Acceptance Criteria | Front-desk staff send each of the seven event types and every message carries a delivery state. |
| Technical Information | Push becomes the third channel when 1.5.4.2 lands; SMS stays the fallback. |
| Agreement Information | Gateway credit purchased under the center's own account with the provider. |

*Page 1 of 1*
#### 1.5.3.1 F10 Financial reports and export

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F10 Financial reports and export |
| Code of Accounts | 1.5.3.1 |
| Responsible Person | DEV1 |
| Description of Work | Build the financial half of F10 per charter 1.1.4: revenue and collection by period and branch, outstanding debt, and the filters and Excel and PDF export used by every F10 report. Academic reporting is carried by 1.5.3.3. |
| Assumptions and Constraints | Reports read the same records the operational screens write; there is no separate reporting copy. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. F10 financial reporting demonstrated at the iteration 2 review |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.3.1-A1 | Revenue, collection, and outstanding debt reporting | DEV1 | 32 | 118,750 | 3,800,000 | | | | 3,800,000 |
| 1.5.3.1-A2 | Filters and Excel and PDF export | DEV1 | 24 | 118,750 | 2,850,000 | | | | 2,850,000 |
| | **Work package total** | | **56** | | **6,650,000** | | | **0** | **6,650,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | A report covering one term is produced within 10 seconds. |
| Acceptance Criteria | Director runs the financial reports unaided and the figures match the records. |
| Technical Information | Serves BR04 and FR10. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.5.3.2 F11 System administration and audit

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F11 System administration and audit |
| Code of Accounts | 1.5.3.2 |
| Responsible Person | DEV1 |
| Description of Work | Build F11 per charter 1.1.4: reference data and configuration, backup triggering and restore, the audit log over every financial and student write, and the complete data export the center runs itself. |
| Assumptions and Constraints | The audit log cannot be edited through any interface and is retained for <mark>3 years</mark>. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. F11 demonstrated at the iteration 2 review |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.3.2-A1 | Reference data and configuration screens | DEV1 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.5.3.2-A2 | Audit log over financial and student writes | DEV1 | 18 | 118,750 | 2,137,500 | | | | 2,137,500 |
| 1.5.3.2-A3 | Administrator data export in an open format | DEV1 | 12 | 118,750 | 1,425,000 | | | | 1,425,000 |
| | **Work package total** | | **50** | | **5,937,500** | | | **0** | **5,937,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criteria A05 and A11; an attempt to edit the log fails from every interface. |
| Acceptance Criteria | System Administrator produces the export unaided and fails to alter a log entry. |
| Technical Information | Serves NFR05 and NFR11 of the traceability matrix. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.5.3.3 F10 Enrollment, fill rate, and workload reports

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | F10 Enrollment, fill rate, and workload reports |
| Code of Accounts | 1.5.3.3 |
| Responsible Person | DEV1 |
| Description of Work | Build the academic half of F10 per charter 1.1.4: new and retained student counts, class fill rate, teacher workload and teaching hours, and attendance rate. |
| Assumptions and Constraints | These are the reports the fourth-branch decision rests on. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. F10 academic reporting demonstrated at the iteration 2 review |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.3.3-A1 | Enrollment, retention, fill rate, and workload | DEV1 | 34 | 118,750 | 4,037,500 | | | | 4,037,500 |
| | **Work package total** | | **34** | | **4,037,500** | | | **0** | **4,037,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every figure ties to the underlying enrollment and attendance records. |
| Acceptance Criteria | Director runs the reports unaided in UAT. |
| Technical Information | Uses the filters and the export built in 1.5.3.1. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.5.4.1 Parent tuition, messages, and requests

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Parent tuition, messages, and requests |
| Code of Accounts | 1.5.4.1 |
| Responsible Person | MOB1 |
| Description of Work | Build the remaining parent journeys of F12 per charter 1.1.4: tuition balance and invoices, messages to the front desk, make-up request, bank-transfer confirmation, evaluation, and re-enrollment request. |
| Assumptions and Constraints | Staff functions stay on the web and no function is application-only. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Parent journeys feature complete at the iteration 2 review |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.4.1-A1 | Tuition balance, invoices, and transfer confirmation | MOB1 | 40 | 122,500 | 4,900,000 | | | | 4,900,000 |
| 1.5.4.1-A2 | Messages, make-up, evaluation, and re-enrollment | MOB1 | 30 | 122,500 | 3,675,000 | | | | 3,675,000 |
| | **Work package total** | | **70** | | **8,575,000** | | | **0** | **8,575,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every F12 parent function is within three taps of the home screen. |
| Acceptance Criteria | Parent journeys feature complete at M4. |
| Technical Information | Built against the API contract of 1.3.1.3; extends the alpha of 1.4.4.1. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.5.4.2 Push notification integration

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Push notification integration |
| Code of Accounts | 1.5.4.2 |
| Responsible Person | MOB1 |
| Description of Work | Add push as the third F09 channel: device registration, delivery of the F09 events, delivery state in the same log, and SMS fallback four hours after a failed push on tuition messages. |
| Assumptions and Constraints | <mark>Push service on the free tier</mark>, per charter budget line 2. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Push channel demonstrated at the iteration 2 review |
| Due Dates | <mark>Mon 30 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.4.2-A1 | Device registration and push delivery | MOB1 | 40 | 122,500 | 4,900,000 | | | | 4,900,000 |
| 1.5.4.2-A2 | Server-side channel selection and fallback timer | DEV3 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| | **Work package total** | | **60** | | **7,275,000** | | | **0** | **7,275,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Push delivery state is logged exactly as email and SMS are; the fallback timer is four hours. |
| Acceptance Criteria | A failed push produces an SMS within four hours in the test log. |
| Technical Information | This is what holds notification cost at the business case figure rather than the SMS-only figure. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.5.4.3 Teacher journeys

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Teacher journeys |
| Code of Accounts | 1.5.4.3 |
| Responsible Person | MOB1 |
| Description of Work | Build the teacher journeys of F12 per charter 1.1.4: today's sessions and rosters, attendance marking while online, score entry, the teaching-hour sheet, and class announcements. |
| Assumptions and Constraints | Attendance marking and payment confirmation are disabled while offline, per charter 1.1.5. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Teacher journeys feature complete at the iteration 2 review |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.4.3-A1 | Today's sessions, rosters, and attendance marking | MOB1 | 44 | 122,500 | 5,390,000 | | | | 5,390,000 |
| 1.5.4.3-A2 | Score entry, teaching-hour sheet, and announcements | MOB1 | 36 | 122,500 | 4,410,000 | | | | 4,410,000 |
| | **Work package total** | | **80** | | **9,800,000** | | | **0** | **9,800,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every F12 teacher function is within three taps of the home screen. |
| Acceptance Criteria | Teacher journeys feature complete at M4. |
| Technical Information | Writes through the same API as the web, so there is no second attendance path. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.5.4.4 Offline behaviour and release build

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Offline behaviour and release build |
| Code of Accounts | 1.5.4.4 |
| Responsible Person | MOB1 |
| Description of Work | Build the offline and degraded-state behaviour with the read-only last-synced view, and produce the store-ready release build with signing and internal distribution. |
| Assumptions and Constraints | The application does not queue attendance or payments while offline; it shows the last synced data read-only, per charter 1.4. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Release build ready for submission at M5 |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.4.4-A1 | Offline behaviour with last-synced view | MOB1 | 40 | 122,500 | 4,900,000 | | | | 4,900,000 |
| 1.5.4.4-A2 | Store-ready release build and distribution | MOB1 | 26 | 122,500 | 3,185,000 | | | | 3,185,000 |
| | **Work package total** | | **66** | | **8,085,000** | | | **0** | **8,085,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The last-synced view shows its timestamp and disables the write actions. |
| Acceptance Criteria | Release build installed and exercised on both test phones before submission. |
| Technical Information | The build submitted in 1.9.1.2 is the one produced here. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.5.5.1 Iteration 2 code review and rework

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Iteration 2 code review and rework |
| Code of Accounts | 1.5.5.1 |
| Responsible Person | QA1 |
| Description of Work | Review the iteration 2 code against the design, the coding convention, and the money-path rules, and rework against the findings. The tuition and payroll code is reviewed by a developer who did not write it. |
| Assumptions and Constraints | The money path carries the tightest acceptance rule in the charter, so it is reviewed here and again in the system test. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Iteration 2 review findings closed |
| Due Dates | <mark>Mon 7 December 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.5.1-A1 | Cross-review of the tuition and payroll code | DEV1 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.5.5.1-A2 | Review against the test plan and money path | QA1 | 40 | 93,750 | 3,750,000 | | | | 3,750,000 |
| | **Work package total** | | **60** | | **6,125,000** | | | **0** | **6,125,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No author reviews their own code; no finding on the money path is left open. |
| Acceptance Criteria | Finding list closed before the M4 acceptance. |
| Technical Information | Part of the charter response to risk R4, pairing on scheduling and tuition. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.5.5.2 Iteration 2 testing, finance and administration

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Iteration 2 testing, finance and administration |
| Code of Accounts | 1.5.5.2 |
| Responsible Person | QA1 |
| Description of Work | Author the test cases for F06, F07, F10, and F11 and execute unit and integration testing on them, including the money-path exception cases. |
| Assumptions and Constraints | No open defect of any severity is tolerated in the tuition, payment, or teaching-hour path. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Finance and administration test cycle complete |
| Due Dates | <mark>Mon 30 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.5.2-A1 | Test case authoring for F06, F07, F10, F11 | QA1 | 12 | 93,750 | 1,125,000 | | | | 1,125,000 |
| 1.5.5.2-A2 | Unit and integration execution | QA1 | 30 | 93,750 | 2,812,500 | | | | 2,812,500 |
| 1.5.5.2-A3 | Money-path exception case execution | QA1 | 12 | 93,750 | 1,125,000 | | | | 1,125,000 |
| 1.5.5.2-A4 | Defect logging and retest | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| | **Work package total** | | **62** | | **5,812,500** | | | **0** | **5,812,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every money-path exception case of charter 1.1.5 is executed. |
| Acceptance Criteria | Feature-complete criteria met for the finance functions at M4. |
| Technical Information | Defects go into the single project defect log consolidated in 1.6.2.1. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.5.5.3 Iteration 2 acceptance, feature complete

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Iteration 2 acceptance, feature complete |
| Code of Accounts | 1.5.5.3 |
| Responsible Person | PM |
| Description of Work | Demonstrate F06 to F12 to the customer, record the acceptance decision, and declare the system feature complete. |
| Assumptions and Constraints | The M4 milestone releases the 30% payment tranche against the signed acceptance record. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. M4 iteration 2 accepted, feature complete, F06 to F12<br>2. D4 delivered |
| Due Dates | <mark>Fri 11 December 2026; M4 on Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.5.3-A1 | Demo preparation and delivery | PM | 30 | 162,500 | 4,875,000 | | | | 4,875,000 |
| 1.5.5.3-A2 | Feature-complete walkthrough against F01 to F12 | QA1 | 20 | 93,750 | 1,875,000 | | | | 1,875,000 |
| | **Work package total** | | **50** | | **6,750,000** | | | **0** | **6,750,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Feature complete means every function is present and testable, not that every defect is closed. |
| Acceptance Criteria | Signed acceptance record of D4. |
| Technical Information |  |
| Agreement Information | Acceptance record releases the M4 payment tranche. |

*Page 1 of 1*
#### 1.5.5.4 Iteration 2 testing, academic, notification, and mobile

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Iteration 2 testing, academic, notification, and mobile |
| Code of Accounts | 1.5.5.4 |
| Responsible Person | QA1 |
| Description of Work | Execute unit and integration testing on F08, F09, and F12 on the web and on both mobile platforms, including their exception cases. |
| Assumptions and Constraints | The application is tested on real devices, using the two test phones bought in 1.6.1.2. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Academic, notification, and mobile test cycle complete |
| Due Dates | <mark>Mon 30 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.5.4-A1 | Execution on web and both mobile platforms | QA1 | 30 | 93,750 | 2,812,500 | | | | 2,812,500 |
| 1.5.5.4-A2 | Exception case execution | QA1 | 12 | 93,750 | 1,125,000 | | | | 1,125,000 |
| 1.5.5.4-A3 | Defect logging and retest | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| | **Work package total** | | **50** | | **4,687,500** | | | **0** | **4,687,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | Push, SMS fallback, and the offline state are each executed on a real device. |
| Acceptance Criteria | Feature-complete criteria met for F08, F09, and F12 at M4. |
| Technical Information | Defects go into the single project defect log consolidated in 1.6.2.1. |
| Agreement Information |  |

*Page 1 of 1*
### Phase 1.6 Quality Assurance and Test

#### 1.6.1.1 System test execution, web, end-to-end scenarios

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | System test execution, web, end-to-end scenarios |
| Code of Accounts | 1.6.1.1 |
| Responsible Person | QA1 |
| Description of Work | Execute the end-to-end system test of the web application across F01 to F12 on staging with migrated sample data, against the test plan accepted at M2. Exception behaviour is carried by 1.6.1.6. |
| Assumptions and Constraints | System test starts once the system is feature complete at M4 and runs against staging, not against developer machines. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Web end-to-end test cycle complete |
| Due Dates | <mark>Mon 14 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.1.1-A1 | End-to-end scenario execution across F01 to F12 | QA1 | 64 | 93,750 | 6,000,000 | | | | 6,000,000 |
| | **Work package total** | | **64** | | **6,000,000** | | | **0** | **6,000,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every scenario of the test plan is executed and recorded. |
| Acceptance Criteria | Exit criteria of the test plan met for the web functions. |
| Technical Information | Covers NFR09 for the latest two versions of Chrome, Edge, and Firefox. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.6.1.2 System test execution, Android and iOS

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | System test execution, Android and iOS |
| Code of Accounts | 1.6.1.2 |
| Responsible Person | QA1 |
| Description of Work | Execute the system test of the application on real Android and iOS devices, covering the parent and teacher journeys, push delivery, the SMS fallback, and the offline and degraded states. |
| Assumptions and Constraints | <mark>Two test phones, one Android and one iOS</mark>, are bought for this from charter budget line 3. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Mobile system test cycle complete |
| Due Dates | <mark>Mon 14 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.1.2-A1 | Parent and teacher journey execution | QA1 | 40 | 93,750 | 3,750,000 | | | | 3,750,000 |
| 1.6.1.2-A2 | Push, SMS fallback, and offline state execution | QA1 | 20 | 93,750 | 1,875,000 | | | | 1,875,000 |
| 1.6.1.2-A3 | Test phones, one Android and one iOS | | | | | 2 | 1,000,000 | 2,000,000 | 2,000,000 |
| | **Work package total** | | **60** | | **5,625,000** | | | **2,000,000** | **7,625,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criterion A09 for Android 10 and later and iOS 15 and later. |
| Acceptance Criteria | Exit criteria met on both platforms before store submission at M5. |
| Technical Information | Devices are handed to the center with the equipment at closeout. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.6.1.3 Performance and capacity test

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Performance and capacity test |
| Code of Accounts | 1.6.1.3 |
| Responsible Person | QA1 |
| Description of Work | Load test the staff screens, the parent portal, the term report, and the application screens at the stated concurrency and data volume, and report the 95th percentile against each threshold. |
| Assumptions and Constraints | <mark>52 concurrent staff users, 300 concurrent parent sessions, 5,000 student records, 200 classes per term, and 3 years of history</mark>, from charter criteria A02 and A03. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Performance and capacity report issued |
| Due Dates | <mark>Mon 14 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.1.3-A1 | Load and capacity test execution | QA1 | 40 | 93,750 | 3,750,000 | | | | 3,750,000 |
| 1.6.1.3-A2 | Test data generation at the stated volumes | DEV3 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| | **Work package total** | | **60** | | **6,125,000** | | | **0** | **6,125,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The report states the 95th percentile, not the average. |
| Acceptance Criteria | Every threshold met, or a fix agreed before UAT entry. |
| Technical Information | Serves NFR02 and NFR03 of the traceability matrix. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.6.1.4 Security test

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Security test |
| Code of Accounts | 1.6.1.4 |
| Responsible Person | QA1 |
| Description of Work | Test endpoint authorisation against the role matrix, password storage, HTTPS-only transport, consent recording, token expiry, and device caching, per charter criterion A04. |
| Assumptions and Constraints | A finding here blocks UAT entry rather than being carried into the warranty month. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Security test report issued |
| Due Dates | <mark>Mon 14 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.1.4-A1 | Authorisation and transport testing | QA1 | 20 | 93,750 | 1,875,000 | | | | 1,875,000 |
| 1.6.1.4-A2 | Credential, consent, token, and storage checks | DEV3 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| | **Work package total** | | **40** | | **4,250,000** | | | **0** | **4,250,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criterion A04; no unauthorised access path found. |
| Acceptance Criteria | Report reviewed and accepted before UAT entry at M5. |
| Technical Information | The audit log built in 1.5.3.2 is checked here for tamper resistance. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.6.1.5 Defect fixing, scheduling, reporting, and administration

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Defect fixing, scheduling, reporting, and administration |
| Code of Accounts | 1.6.1.5 |
| Responsible Person | DEV1 |
| Description of Work | Fix the system, performance, and security test defects in the scheduling, reporting, and administration areas, which this developer owns. |
| Assumptions and Constraints | Sized from the defect rate assumed in the test plan and the first thing re-estimated if the rate differs. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. No open Critical or High defect in these areas at UAT entry |
| Due Dates | <mark>Mon 14 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.1.5-A1 | Defect fixing in scheduling, reporting, administration | DEV1 | 80 | 118,750 | 9,500,000 | | | | 9,500,000 |
| | **Work package total** | | **80** | | **9,500,000** | | | **0** | **9,500,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No fix is signed off by the person who wrote it; verification runs in 1.6.1.8. |
| Acceptance Criteria | UAT entry criteria met for these areas at M5. |
| Technical Information |  |
| Agreement Information |  |

*Page 1 of 1*
#### 1.6.1.6 System test execution, web, exception and failure behaviour

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | System test execution, web, exception and failure behaviour |
| Code of Accounts | 1.6.1.6 |
| Responsible Person | QA1 |
| Description of Work | Execute the fourteen exception and failure cases of charter 1.1.5 against the web application on staging. |
| Assumptions and Constraints | Exception behaviour is tested with the same weight as the functions themselves. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Exception behaviour test cycle complete |
| Due Dates | <mark>Mon 14 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.1.6-A1 | Exception and failure behaviour execution | QA1 | 36 | 93,750 | 3,375,000 | | | | 3,375,000 |
| | **Work package total** | | **36** | | **3,375,000** | | | **0** | **3,375,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every one of the fourteen exception cases is executed, not a sample of them. |
| Acceptance Criteria | Exit criteria of the test plan met for the exception behaviour. |
| Technical Information | The cases come from the catalogue written in 1.2.1.4. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.6.1.7 Defect fixing, enrollment, tuition, and payroll

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Defect fixing, enrollment, tuition, and payroll |
| Code of Accounts | 1.6.1.7 |
| Responsible Person | DEV2 |
| Description of Work | Fix the system, performance, and security test defects in the enrollment, tuition, and payroll areas, which this developer owns. |
| Assumptions and Constraints | The money path carries no open defect of any severity at UAT entry. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. No open defect in the money path at UAT entry |
| Due Dates | <mark>Mon 14 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.1.7-A1 | Defect fixing in enrollment, tuition, and payroll | DEV2 | 80 | 118,750 | 9,500,000 | | | | 9,500,000 |
| | **Work package total** | | **80** | | **9,500,000** | | | **0** | **9,500,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No fix is signed off by the person who wrote it; verification runs in 1.6.1.8. |
| Acceptance Criteria | UAT entry criteria met for the money path at M5. |
| Technical Information |  |
| Agreement Information |  |

*Page 1 of 1*
#### 1.6.1.8 Defect fixing, catalog, assessment, notification, and platform, with regression

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Defect fixing, catalog, assessment, notification, and platform, with regression |
| Code of Accounts | 1.6.1.8 |
| Responsible Person | DEV3 |
| Description of Work | Fix the defects in the catalog, assessment, notification, and platform areas, and run the regression cycle that verifies every fix batch from 1.6.1.5, 1.6.1.7, and this package. |
| Assumptions and Constraints | The regression cycle is run by the QA engineer, never by the developer who wrote the fix. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Regression cycle clean at UAT entry |
| Due Dates | <mark>Mon 14 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.1.8-A1 | Defect fixing in catalog, assessment, and platform | DEV3 | 60 | 118,750 | 7,125,000 | | | | 7,125,000 |
| 1.6.1.8-A2 | Regression cycle and fix verification | QA1 | 20 | 93,750 | 1,875,000 | | | | 1,875,000 |
| | **Work package total** | | **80** | | **9,000,000** | | | **0** | **9,000,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No open Critical or High defect, and none of any severity in the money path. |
| Acceptance Criteria | UAT entry criteria met at M5. |
| Technical Information | The regression suite is handed over with the source code in 1.8.3.1. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.6.2.1 UAT test set, defect log, and test summary report

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | UAT test set, defect log, and test summary report |
| Code of Accounts | 1.6.2.1 |
| Responsible Person | QA1 |
| Description of Work | Agree the user acceptance test set with the business owners, consolidate the defect log kept by the test packages into one project log with its trend report, and write the test summary report. |
| Assumptions and Constraints | The charter requires the UAT test set to be agreed and signed at M5, and acceptance is measured against that set and nothing else. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. UAT test set agreed and signed at M5<br>2. D5 test documentation complete |
| Due Dates | <mark>Mon 14 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.2.1-A1 | UAT test set agreement with business owners | QA1 | 16 | 93,750 | 1,500,000 | | | | 1,500,000 |
| 1.6.2.1-A2 | Defect log consolidation and trend report | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| 1.6.2.1-A3 | Test summary report | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| | **Work package total** | | **32** | | **3,000,000** | | | **0** | **3,000,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every function and every exception case has at least one test case in the set. |
| Acceptance Criteria | Signed acceptance record of D5, with the test set attached. |
| Technical Information | Test case authoring itself sits in 1.4.3.2 and 1.5.5.2, next to the code it covers. |
| Agreement Information | Signed test set is attached to the acceptance record of D5. |

*Page 1 of 1*
#### 1.6.2.2 UAT entry criteria review

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | UAT entry criteria review |
| Code of Accounts | 1.6.2.2 |
| Responsible Person | PM |
| Description of Work | Review the system, performance, capacity, and security results against the UAT entry criteria of the test plan, confirm the store submission has been made, and decide whether UAT starts. |
| Assumptions and Constraints | Entering UAT with open Critical or High defects would move the failure into the customer's own acceptance window, so this is a gate rather than a review. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. M5 system test complete on web, Android, and iOS; UAT entry criteria met; application submitted to both stores |
| Due Dates | <mark>Fri 18 December 2026; M5 on Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.2.2-A1 | Entry criteria review and go decision | PM | 20 | 162,500 | 3,250,000 | | | | 3,250,000 |
| 1.6.2.2-A2 | Evidence pack for the entry decision | QA1 | 4 | 93,750 | 375,000 | | | | 375,000 |
| | **Work package total** | | **24** | | **3,625,000** | | | **0** | **3,625,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The decision is recorded with the evidence it rested on. |
| Acceptance Criteria | Sponsor and QA engineer agree UAT entry. |
| Technical Information |  |
| Agreement Information |  |

*Page 1 of 1*
### Phase 1.7 Data Migration

#### 1.7.1.1 Source data analysis and cleansing rules

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Source data analysis and cleansing rules |
| Code of Accounts | 1.7.1.1 |
| Responsible Person | DEV1 |
| Description of Work | Analyse the center's Excel workbooks and paper registers for the two most recent terms, assess data quality at M1, and draft the cleansing and mapping rules the migration scripts implement. |
| Assumptions and Constraints | The center cleans the source files before M5, per charter assumption 11, and the rules are confirmed before the trial run. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Data quality assessed at M1<br>2. Cleansing and mapping rules drafted |
| Due Dates | <mark>Mon 28 September 2026 to Fri 2 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.7.1.1-A1 | Source data quality assessment | PM | 12 | 162,500 | 1,950,000 | | | | 1,950,000 |
| 1.7.1.1-A2 | Cleansing and mapping rule definition | DEV1 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| | **Work package total** | | **32** | | **4,325,000** | | | **0** | **4,325,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every source field maps to a target field or is explicitly dropped with a reason. |
| Acceptance Criteria | Rules agreed with the Accountant and the Academic Manager before the trial run. |
| Technical Information | This package is the charter response to risk R6. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.7.1.2 Migration scripts and trial run

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Migration scripts and trial run |
| Code of Accounts | 1.7.1.2 |
| Responsible Person | DEV1 |
| Description of Work | Build the migration scripts, run a full trial migration into staging, and reconcile the trial result against the source files record by record. |
| Assumptions and Constraints | <mark>12,000,000 VND of external data-entry support</mark> from charter budget line 4 covers the records the center cannot supply in machine-readable form. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Trial migration reconciled on staging |
| Due Dates | <mark>Mon 21 December 2026 to Thu 31 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.7.1.2-A1 | Migration script development | DEV1 | 40 | 118,750 | 4,750,000 | | | | 4,750,000 |
| 1.7.1.2-A2 | Trial run into staging and correction | DEV1 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.7.1.2-A3 | Trial reconciliation review | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| 1.7.1.2-A4 | External data-entry support | | | | | 1 | 12,000,000 | 12,000,000 | 12,000,000 |
| | **Work package total** | | **68** | | **7,875,000** | | | **12,000,000** | **19,875,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The trial produces the same reconciliation report the production run will produce. |
| Acceptance Criteria | Trial differences explained or corrected before the production run. |
| Technical Information | Uses the key design from 1.3.1.2, which is what makes record-by-record reconciliation possible. |
| Agreement Information | Data-entry support engaged under a short-form supplier agreement. |

*Page 1 of 1*
#### 1.7.1.3 Production migration and reconciliation report

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Production migration and reconciliation report |
| Code of Accounts | 1.7.1.3 |
| Responsible Person | DEV1 |
| Description of Work | Run the migration into production and produce the reconciliation report listing every difference between the migrated data and the source files. |
| Assumptions and Constraints | A failed run falls back to the spreadsheets, which stay in parallel for two weeks after go-live. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. D6 production data migrated and reconciled |
| Due Dates | <mark>Mon 4 January 2027 to Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.7.1.3-A1 | Production migration run | DEV1 | 24 | 118,750 | 2,850,000 | | | | 2,850,000 |
| 1.7.1.3-A2 | Reconciliation report production | DEV1 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| 1.7.1.3-A3 | Reconciliation verification | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| | **Work package total** | | **48** | | **5,500,000** | | | **0** | **5,500,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every difference appears in the report; none is silently corrected. |
| Acceptance Criteria | Report complete and handed to the Accountant for acceptance in 1.7.1.4. |
| Technical Information | Serves BR01: after this package the system, not the spreadsheets, holds the data. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.7.1.4 Accountant acceptance of the reconciliation

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Accountant acceptance of the reconciliation |
| Code of Accounts | 1.7.1.4 |
| Responsible Person | PM |
| Description of Work | Obtain the Accountant's written acceptance of the reconciliation report, including any difference the center chooses to accept rather than correct. |
| Assumptions and Constraints | Go-live requires this acceptance, per charter exit criterion 4. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Reconciliation accepted in writing |
| Due Dates | <mark>Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.7.1.4-A1 | Reconciliation walkthrough and written acceptance | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| 1.7.1.4-A2 | Acceptance evidence filing | QA1 | 4 | 93,750 | 375,000 | | | | 375,000 |
| | **Work package total** | | **12** | | **1,675,000** | | | **0** | **1,675,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance names the differences accepted rather than accepting them silently. |
| Acceptance Criteria | Signed acceptance record of D6. |
| Technical Information |  |
| Agreement Information | Acceptance record filed with the supplier contract. |

*Page 1 of 1*
### Phase 1.8 Deployment and Handover

#### 1.8.1.1 Cloud server and staging provisioning

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Cloud server and staging provisioning |
| Code of Accounts | 1.8.1.1 |
| Responsible Person | DEV3 |
| Description of Work | Provision the production cloud virtual server and the staging environment, the domain, and the SSL certificate, and harden both to the security design. |
| Assumptions and Constraints | <mark>Cloud server and staging for 12 months at 24,000,000 VND, domain and SSL at 2,000,000 VND</mark> from charter budget line 2; later subscriptions are a charter exclusion. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Production and staging environments available |
| Due Dates | <mark>Mon 19 October 2026 to Fri 23 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.8.1.1-A1 | Production and staging provisioning and hardening | DEV3 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| 1.8.1.1-A2 | Domain, SSL, and HTTPS-only configuration | DEV3 | 8 | 118,750 | 950,000 | | | | 950,000 |
| 1.8.1.1-A3 | Cloud server and staging, 12 months | | | | | 1 | 24,000,000 | 24,000,000 | 24,000,000 |
| 1.8.1.1-A4 | Domain and SSL certificate | | | | | 1 | 2,000,000 | 2,000,000 | 2,000,000 |
| | **Work package total** | | **24** | | **2,850,000** | | | **26,000,000** | **28,850,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | HTTPS only, per acceptance criterion A04; staging matches production in configuration. |
| Acceptance Criteria | Both environments reachable and hardened before the first deployment. |
| Technical Information | Accounts are opened in the center's name so that they survive handover. |
| Agreement Information | Cloud subscription contracted in the center's name, 12 months from provisioning. |

*Page 1 of 1*
#### 1.8.1.2 Backup configuration and restore drill

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Backup configuration and restore drill |
| Code of Accounts | 1.8.1.2 |
| Responsible Person | DEV3 |
| Description of Work | Configure the nightly backup to the 24-hour recovery point objective and demonstrate a restore inside the 4-hour recovery time objective during UAT. |
| Assumptions and Constraints | The second drill that criterion A06 requires is delivered inside the warranty month in 1.10.1.1. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Restore demonstrated during UAT |
| Due Dates | <mark>Mon 21 December 2026 to Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.8.1.2-A1 | Backup configuration and schedule | DEV3 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| 1.8.1.2-A2 | Restore drill witnessed by the administrator | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| | **Work package total** | | **24** | | **2,650,000** | | | **0** | **2,650,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | A restore from a backup no more than 24 hours old completes inside 4 hours. |
| Acceptance Criteria | Drill recorded and signed by the System Administrator. |
| Technical Information | Serves NFR06; the drill procedure is part of the administrator guide in 1.8.2.1. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.8.1.3 Production deployment and go-live

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Production deployment and go-live |
| Code of Accounts | 1.8.1.3 |
| Responsible Person | DEV3 |
| Description of Work | Deploy the accepted release to production, pilot F01 to F06 at one branch for the two weeks before go-live, switch all three branches over, and keep the spreadsheets in parallel for two weeks afterwards. |
| Assumptions and Constraints | <mark>8,000,000 VND of go-live support</mark> from charter budget line 4 covers the switchover weekend and on-site presence at the three branches. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Pilot at one branch complete<br>2. M6 go-live<br>3. D7 delivered |
| Due Dates | <mark>Mon 21 December 2026 to Tue 5 January 2027; M6 on Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.8.1.3-A1 | Pilot deployment and support at one branch | DEV3 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| 1.8.1.3-A2 | Production deployment and switchover | DEV3 | 8 | 118,750 | 950,000 | | | | 950,000 |
| 1.8.1.3-A3 | Go-live coordination across the three branches | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| 1.8.1.3-A4 | Go-live support and on-site presence | | | | | 1 | 8,000,000 | 8,000,000 | 8,000,000 |
| | **Work package total** | | **32** | | **4,150,000** | | | **8,000,000** | **12,150,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Written rollback criteria exist that the center itself can invoke. |
| Acceptance Criteria | Signed acceptance record of D7. |
| Technical Information | This package carries the charter responses to risks R8 and R10. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.8.2.1 User, administrator, and deployment documentation

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | User, administrator, and deployment documentation |
| Code of Accounts | 1.8.2.1 |
| Responsible Person | DEV2 |
| Description of Work | Write the Vietnamese user manual for the staff roles, the administrator guide covering configuration, backup, restore, and the audit log, and the deployment guide, together with the in-app guide and the guardian onboarding message of charter budget line 4. |
| Assumptions and Constraints | <mark>10,000,000 VND of documentation production</mark> from charter budget line 4 covers translation review, screenshots, and printing. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Documentation delivered as part of D8 |
| Due Dates | <mark>Mon 14 December 2026 to Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.8.2.1-A1 | User manual for the staff roles | DEV2 | 10 | 118,750 | 1,187,500 | | | | 1,187,500 |
| 1.8.2.1-A2 | Administrator and deployment guide | DEV2 | 6 | 118,750 | 712,500 | | | | 712,500 |
| 1.8.2.1-A3 | Documentation review and translation check | PM | 12 | 162,500 | 1,950,000 | | | | 1,950,000 |
| 1.8.2.1-A4 | In-app guide and guardian onboarding message | PM | 4 | 162,500 | 650,000 | | | | 650,000 |
| 1.8.2.1-A5 | Documentation production, translation, and printing | | | | | 1 | 10,000,000 | 10,000,000 | 10,000,000 |
| | **Work package total** | | **32** | | **4,500,000** | | | **10,000,000** | **14,500,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criterion A10: a third party deploys to staging following only the guide. |
| Acceptance Criteria | System Administrator deploys to staging from the guide without help. |
| Technical Information | The paper fallback procedure written in 1.8.2.2 is part of the user manual. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.8.2.2 Staff training, paper fallback procedure, and rehearsal

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Staff training, paper fallback procedure, and rehearsal |
| Code of Accounts | 1.8.2.2 |
| Responsible Person | PM |
| Description of Work | Train the center's staff by role in half-day sessions at the three branches and keep the training record, and write, train, and rehearse the paper fallback and catch-up procedure before go-live. |
| Assumptions and Constraints | <mark>52 staff users, being 35 teachers and 17 administrative staff</mark>; training delivery of 12,000,000 VND and travel of 3,000,000 VND from charter budget lines 4 and 3. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Training complete at all three branches<br>2. Fallback rehearsed before go-live<br>3. D8 delivered |
| Due Dates | <mark>Mon 21 December 2026 to Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.8.2.2-A1 | Training delivery by role at three branches | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| 1.8.2.2-A2 | Fallback and catch-up procedure and training | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| 1.8.2.2-A3 | Rehearsal at one branch and reconciliation | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| 1.8.2.2-A4 | Training delivery, venue, and materials | | | | | 1 | 12,000,000 | 12,000,000 | 12,000,000 |
| 1.8.2.2-A5 | Travel to the three branches | | | | | 1 | 3,000,000 | 3,000,000 | 3,000,000 |
| | **Work package total** | | **32** | | **4,650,000** | | | **15,000,000** | **19,650,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criteria A07 and A08; a staff member performs daily tasks after half a day of training. |
| Acceptance Criteria | Signed acceptance record of D8, with the training and rehearsal records attached. |
| Technical Information | Serves NFR07 and NFR08; the procedure lives in the user manual, not on a separate sheet. |
| Agreement Information |  |

*Page 1 of 1*
#### 1.8.3.1 Source code, database scripts, and technical documentation handover

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Source code, database scripts, and technical documentation handover |
| Code of Accounts | 1.8.3.1 |
| Responsible Person | DEV2 |
| Description of Work | Hand over the source code, the database scripts, the schema and API documentation, the regression suite, the coding convention, and repository access, so that the center is not locked to the supplier after the warranty. |
| Assumptions and Constraints | Handover is to the center's System Administrator and is complete at go-live, not at closeout. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. D9 handover complete |
| Due Dates | <mark>Mon 28 December 2026 to Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.8.3.1-A1 | Handover pack assembly and repository transfer | DEV2 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.8.3.1-A2 | Handover walkthrough with the administrator | PM | 4 | 162,500 | 650,000 | | | | 650,000 |
| | **Work package total** | | **24** | | **3,025,000** | | | **0** | **3,025,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Handover checklist complete; nothing on it is marked to follow. |
| Acceptance Criteria | Signed acceptance record of D9. |
| Technical Information | Signing keys for the mobile application are handed over separately in 1.9.1.1. |
| Agreement Information | Handover record filed with the supplier contract. |

*Page 1 of 1*
#### 1.8.3.2 User acceptance testing execution and sign-off

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | User acceptance testing execution and sign-off |
| Code of Accounts | 1.8.3.2 |
| Responsible Person | QA1 |
| Description of Work | Run user acceptance testing with the business owners against the test set agreed at M5, record the result per test case, and obtain the sign-off that gates go-live. |
| Assumptions and Constraints | Acceptance is measured against the agreed set: at least 99% of cases passed and no open Critical or High defect. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. UAT sign-off obtained<br>2. M6 UAT signed off, go-live and handover |
| Due Dates | <mark>Mon 21 December 2026 to Tue 5 January 2027; M6 on Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.8.3.2-A1 | UAT execution with the business owners | QA1 | 24 | 93,750 | 2,250,000 | | | | 2,250,000 |
| 1.8.3.2-A2 | Acceptance decision and sign-off with sponsor | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| | **Work package total** | | **32** | | **3,550,000** | | | **0** | **3,550,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criterion A01; nothing open in the money path. |
| Acceptance Criteria | Sponsor signs the acceptance record; a failed UAT puts the three charter options to the sponsor within two working days. |
| Technical Information | This is the Validate Scope point of the project. |
| Agreement Information | Sign-off releases the final 25% payment tranche. |

*Page 1 of 1*
### Phase 1.9 Mobile Application Release

#### 1.9.1.1 Store accounts and signing keys

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Store accounts and signing keys |
| Code of Accounts | 1.9.1.1 |
| Responsible Person | DEV3 |
| Description of Work | Open the Google Play and Apple Developer accounts in the center's name, configure the signing keys and their custody, and hand the credentials to the center's System Administrator. |
| Assumptions and Constraints | <mark>Apple Developer 2,600,000 VND a year and Google Play 700,000 VND once</mark>, from charter budget line 2. The package crosses the M2 gate only because Apple's enrolment of a legal entity takes up to <mark>four weeks</mark> and is outside the project's control; MOB1 is not mobilised until after M2, so the M1 enrolment is DEV3's work. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Store accounts active<br>2. Signing keys in the center's custody |
| Due Dates | <mark>Fri 2 October 2026 to Fri 30 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.9.1.1-A1 | Store account enrolment in the center's name | DEV3 | 10 | 118,750 | 1,187,500 | | | | 1,187,500 |
| 1.9.1.1-A2 | Signing key generation, custody, and handover | DEV3 | 6 | 118,750 | 712,500 | | | | 712,500 |
| 1.9.1.1-A3 | Enrolment coordination with the center | PM | 6 | 162,500 | 975,000 | | | | 975,000 |
| 1.9.1.1-A4 | Apple Developer and Google Play fees | | | | | 1 | 3,300,000 | 3,300,000 | 3,300,000 |
| | **Work package total** | | **22** | | **2,875,000** | | | **3,300,000** | **6,175,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Accounts are in the center's name, so the applications survive the end of the supplier relationship. |
| Acceptance Criteria | Credentials and keys accepted by the System Administrator. |
| Technical Information | Opening at M1 is the charter response to the enrolment half of risk R12. |
| Agreement Information | Store terms accepted by the center as the account holder. |

*Page 1 of 1*
#### 1.9.1.2 Store listings, submission, and review response

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Store listings, submission, and review response |
| Code of Accounts | 1.9.1.2 |
| Responsible Person | MOB1 |
| Description of Work | Prepare the Vietnamese store listings, screenshots, privacy declarations, release notes, and versioning, submit to both stores at M5, and answer the store review until the application is live. |
| Assumptions and Constraints | <mark>A store review takes at most one week</mark>; go-live does not depend on the application and a store slip of up to two weeks after M6 is absorbed without moving M6. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Application submitted at M5<br>2. Application live in both stores at M6<br>3. D11 delivered |
| Due Dates | <mark>Mon 7 December 2026 to Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.9.1.2-A1 | Listing copy, screenshots, and privacy declarations | MOB1 | 16 | 122,500 | 1,960,000 | | | | 1,960,000 |
| 1.9.1.2-A2 | Release notes and versioning | MOB1 | 8 | 122,500 | 980,000 | | | | 980,000 |
| 1.9.1.2-A3 | Submission to both stores | MOB1 | 16 | 122,500 | 1,960,000 | | | | 1,960,000 |
| 1.9.1.2-A4 | Review response and resubmission | MOB1 | 24 | 122,500 | 2,940,000 | | | | 2,940,000 |
| 1.9.1.2-A5 | Listing review with the Director | PM | 4 | 162,500 | 650,000 | | | | 650,000 |
| | **Work package total** | | **68** | | **8,490,000** | | | **0** | **8,490,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criterion A12; the declarations match what the application collects and every F12 function is within three taps in the published build. |
| Acceptance Criteria | Signed acceptance record of D11. |
| Technical Information | The build submitted is the release build produced in 1.5.4.4. |
| Agreement Information | Applications published under the center's store accounts. |

*Page 1 of 1*
### Phase 1.10 Warranty and Closeout

#### 1.10.1.1 First warranty month support

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | First warranty month support |
| Code of Accounts | 1.10.1.1 |
| Responsible Person | PM |
| Description of Work | Deliver the first warranty month inside the project: correct defects against the accepted baseline to the charter response targets, run the second restore drill, support the two-week parallel run, and report the overdue percentage to the Director. |
| Assumptions and Constraints | Declared level of effort: the package runs the whole warranty month with the full team and is the second exception to the 8 to 80 hour rule. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Parallel running ended after two weeks<br>2. Second restore drill complete<br>3. First warranty month complete, part of D10 |
| Due Dates | <mark>Wed 6 January 2027 to Fri 5 February 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.10.1.1-A1 | Defect correction in scheduling and reporting | DEV1 | 100 | 118,750 | 11,875,000 | | | | 11,875,000 |
| 1.10.1.1-A2 | Defect correction in enrollment, tuition, payroll | DEV2 | 172 | 118,750 | 20,425,000 | | | | 20,425,000 |
| 1.10.1.1-A3 | Defect correction in catalog, assessment, and app | DEV3 | 92 | 118,750 | 10,925,000 | | | | 10,925,000 |
| 1.10.1.1-A4 | Warranty coordination and Director reporting | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| 1.10.1.1-A5 | Retest of warranty fixes | QA1 | 12 | 93,750 | 1,125,000 | | | | 1,125,000 |
| | **Work package total** | | **400** | | **48,250,000** | | | **0** | **48,250,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Critical responded within 2 working hours and worked around within 1 working day; High within 1 and 5 working days. |
| Acceptance Criteria | A Critical or High defect still open at the end of the month blocks closeout. |
| Technical Information | The overdue percentage reported here is the first measurement of the business case benefit, per risk R11. |
| Agreement Information | Warranty obligation of the supplier contract, months 1 to 6 from go-live. |

*Page 1 of 1*
#### 1.10.1.2 Warranty handover to the support desk

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Warranty handover to the support desk |
| Code of Accounts | 1.10.1.2 |
| Responsible Person | PM |
| Description of Work | Hand warranty months 2 to 6 to the supplier's support desk with the defect history, the known issues, the response targets, and the escalation path, funded from charter budget line 5. |
| Assumptions and Constraints | <mark>Months 2 to 6 run after closeout at about 0.35 full-time equivalent, 35,000,000 VND, to 5 July 2027.</mark> <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. Warranty handover accepted by the support desk<br>2. D10 warranty handover delivered |
| Due Dates | <mark>Mon 1 February 2027 to Fri 5 February 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.10.1.2-A1 | Handover pack, known issues, and escalation | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| 1.10.1.2-A2 | Support desk briefing and walkthrough | DEV3 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.10.1.2-A3 | Known-issue list verification | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| 1.10.1.2-A4 | Warranty support, months 2 to 6 | | | | | 1 | 35,000,000 | 35,000,000 | 35,000,000 |
| | **Work package total** | | **44** | | **5,725,000** | | | **35,000,000** | **40,725,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The same severity definitions and response targets apply after closeout as during the project. |
| Acceptance Criteria | Support desk accepts the handover before closeout. |
| Technical Information |  |
| Agreement Information | Warranty terms of the supplier contract, months 2 to 6. |

*Page 1 of 1*
#### 1.10.2.1 Closeout report, lessons learned, and final acceptance

| Field | Content |
| --- | --- |
| Project Title | Development and Deployment of a Learning Center Management Software |
| Date Prepared | 23 September 2026 |
| Work Package Name | Closeout report, lessons learned, and final acceptance |
| Code of Accounts | 1.10.2.1 |
| Responsible Person | PM |
| Description of Work | Write the closeout report covering scope against D1 to D11, cost against the baseline, reserve use, the final risk position, the measured overdue percentage, the lessons learned, and the written decision on support after the warranty of charter exit criterion 9. Hold the closeout meeting, obtain final acceptance with the final financial reconciliation and invoice of exit criterion 10, and close the project. |
| Assumptions and Constraints | The report states the actual overdue percentage rather than the target, which is the charter's own test of whether the benefit appeared. <mark>First-pass estimate, re-baselined at M1.</mark> |
| Milestones | 1. D10 closeout report and lessons learned delivered<br>2. M7 first warranty month complete, warranty handover, project closeout |
| Due Dates | <mark>Mon 25 January 2027 to Fri 5 February 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.10.2.1-A1 | Closeout report and lessons learned | PM | 20 | 162,500 | 3,250,000 | | | | 3,250,000 |
| 1.10.2.1-A2 | Closeout meeting and final acceptance | PM | 10 | 162,500 | 1,625,000 | | | | 1,625,000 |
| | **Work package total** | | **30** | | **4,875,000** | | | **0** | **4,875,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The report states what was not achieved as plainly as what was. |
| Acceptance Criteria | Signed final acceptance record closing D1 to D11. |
| Technical Information | Known issues open at closeout are listed with their agreed fix dates. |
| Agreement Information | Contract closed administratively; the warranty obligation survives closure. |

*Page 1 of 1*
