# Learning Center Management Software

## Scope Baseline Package: Requirements Traceability Matrix, WBS, and WBS Dictionary

**Project:** Development and Deployment of a Learning Center Management Software
**Customer:** <mark>Private after-school learning center, three branches, one city</mark>
**Budget:** 700,000,000 VND  **Window:** <mark>14 September 2026 to 5 February 2027</mark>
**Team:** 5 full-time staff, being 1 project manager / business analyst, 3 developers, 1 QA engineer, plus <mark>one part-time mobile developer for 2.5 person-months</mark>
**Date prepared:** 23 September 2026  **Document version:** 1.0

---

### How this document is organised

This is the second deliverable of the coursework. The first is `charter-package.en.md`, which carries the
requirement specification and the project charter. This one carries the three scope-management artifacts
named in `docs/wbs_req.md`, each reproduced from the form in *A Project Manager's Book of Forms*, 3rd
edition, field for field and in the printed field order.

| Part | Artifact | Form | Pages in the book | PMBOK 6 process |
| --- | --- | --- | --- | --- |
| Part 1 | Requirements Traceability Matrix | 2.7 | 40 to 44 | 5.2 Collect Requirements |
| Part 1B | Inter-Requirements Traceability Matrix | 2.7, page 2 of 2 | 44 | 5.2 Collect Requirements |
| Part 2 | Work Breakdown Structure | 2.9 | 49 to 51 | 5.4 Create WBS |
| Part 3 | WBS Dictionary | 2.10 | 52 to 55 | 5.4 Create WBS |

The WBS and the WBS dictionary, together with the project scope statement in Part 1 of the charter
package, are the **scope baseline**.

### What this document is not

Validate Scope (5.5) and Control Scope (5.6) produce no artifact here. Both are Monitoring and
Controlling processes: Validate Scope needs verified deliverables handed over by Control Quality (8.3),
and at the time of writing the project has produced none. Change requests are outputs of those two
processes only, and they are the input to Perform Integrated Change Control (4.6). The four planning
processes 5.1 to 5.4, which are what this document covers, output no change requests.

### Inputs actually used

Per PMBOK 6 Figure 5-10, Create WBS takes the scope management plan, the project scope statement, and
the requirements documentation. The project charter is **not** a direct input to 5.4: it is an input to
5.1, 5.2, and 5.3, and it reaches the WBS through the scope statement that those processes produce. The
requirements traceability matrix is an **output** of 5.2, not an input to 5.4; it is updated later by 5.5
and 5.6. This document therefore builds the RTM first from the charter and the requirement
specification, and then builds the WBS from the scope statement, not from the matrix.

| Input | Where it comes from |
| --- | --- |
| Project scope statement | `charter-package.en.md` sections 1.1 to 1.6 |
| Requirements documentation | `charter-package.en.md` sections 1.1.4 (F01 to F12), 1.1.5, 1.3 (A01 to A12) |
| Scope management plan | Not produced as a separate document for this coursework; the rules it would carry are stated in the conventions below |
| Project charter (indirect) | `charter-package.en.md` Part 2A and 2B |

### Decomposition method

**Top-down.** The charter fixes the deliverables D1 to D11 and the milestones M0 to M7 before any work
package exists, so the structure is decomposed downward from the project to the work package rather than
assembled upward from tasks. The two methods are not mixed.

**Organised by life-cycle phase.** The life cycle is predictive with two build iterations, so level 2 of
the WBS is the phase. Level 3 is the control account, level 4 is the work package. Each work package
rolls up to one and only one control account, per the book's rule on page 50.

**One owner per work package.** Every work package names a single accountable owner. Work and review are
never owned by the same person: a review or rework package is always owned by someone other than the
author of the thing being reviewed. Review and testing are work packages in their own right, inside the
phase whose output they check, not a separate quality activity bolted on at the end. Phase 1.6 exists on
top of that for system-level test, which cannot sit inside a single construction package.

### Reading convention

- <mark>Yellow highlight</mark> marks content whose correctness cannot be confirmed from the brief or the
  charter, per point 3 of the assignment.
- An empty box means the field cannot be completed at this stage, not that it was overlooked.
- In Part 3, the **split** of hours and money across work packages is a first-pass estimate and is
  highlighted once per sheet rather than cell by cell. The **totals** it rolls up to are given by the
  charter and are not highlighted: 4,400 labor hours, 539,000,000 VND of labor, 161,000,000 VND of other
  cost, 700,000,000 VND in all. The split is re-estimated at M1 with the rest of the budget, which the
  charter already commits to.
- Resource codes: **PM** project manager and business analyst, **DEV1**, **DEV2**, **DEV3** developers,
  **QA1** QA engineer, **MOB1** part-time mobile developer. Individual names are not filled in: the
  charter has the sponsor assigning the project manager at M0 and the team is mobilised in work package
  1.1.1.1, so the name boxes stay empty until then. DEV1 and DEV2 are the pair the charter assigns to
  scheduling and billing, and they build F04 and F06.
- Labor rates are the charter's rate mix, converted at <mark>160 hours per person-month</mark>:
  PM 162,500 VND/h, developer 118,750 VND/h, QA 93,750 VND/h, mobile developer 122,500 VND/h.

---

## Part 1: Requirements Traceability Matrix

*Form 2.7, page 1 of 2. Columns and their order are the printed ones: the Requirement Information group
is ID, Requirement, Source, Priority, Category; the Relationship Traceability group is Business
Objective, Deliverable, Verification, Validation.*

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

Three ID families are used. **BR** business requirements, taken from the charter's business case and
objectives. **FR** functional requirements, one per function F01 to F12 of the requirement
specification. **NFR** nonfunctional requirements, one per acceptance criterion A01 to A12. The
Deliverable column cites the WBS code from Part 2 and the charter deliverable in brackets.

### Requirement Information and Relationship Traceability

| ID | Requirement | Source | Priority | Category | Business Objective | Deliverable | Verification | Validation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BR01 | The same student, class, and payment data is held once and entered once, not two or three times in separate files | Center Director | Must have | Business | Cut duplicate data entry from <mark>60 to 15 staff-hours a month</mark>, 32,400,000 VND a year recurring | 1.4.1.2, 1.7.1.3 (D3, D6) | Staff time log over one month after go-live shows 15 hours or fewer spent re-entering data | Director confirms against the closeout report; measured in the first warranty month |
| BR02 | No room, teacher, or student timetable is double-booked | Academic Manager | Must have | Business | Remove double-booking at source; not quantified in the business case | 1.4.2.1 (D3) | Zero conflicting bookings accepted by the system in the UAT conflict test set | Academic Manager runs the conflict scenarios in UAT |
| BR03 | Overdue tuition is visible and chased, and falls from <mark>8% to 3% of billed tuition</mark> | Accountant, Center Director | Must have | Business | Release <mark>360,000,000 VND</mark> once and save <mark>36,000,000 VND</mark> a year of carrying cost, plus <mark>36,000,000 VND</mark> a year of avoided write-off | 1.5.1.1 (D4) | Aged debt report shows the overdue percentage monthly; percentage stated in the closeout report | Accountant reconciles the report against the bank and the invoice ledger |
| BR04 | The Director sees enrollment, revenue, fill rate, and teaching load across all three branches without asking anyone to build a spreadsheet | Center Director | Must have | Business | One current cross-branch view, needed before the <mark>fourth branch in 2027</mark> | 1.5.3.1 (D4) | Every report in F10 filterable by period, branch, and course, produced within 10 seconds for one term | Director uses the dashboard unaided in UAT |
| BR05 | Notifying parents does not cost the center more than it saves | Center Director | Should have | Business | Hold notification cost at <mark>13,800,000 VND</mark> a year through push rather than <mark>46,100,000 VND</mark> on SMS alone | 1.5.4.2, 1.5.2.2 (D4, D11) | F09 delivery log shows the channel mix; push share at least <mark>70% of guardians with a smartphone</mark> | Accountant checks the gateway invoice for the first warranty month |
| BR06 | Teaching-hour payroll is derived from what was actually taught, not typed by hand | Accountant | Must have | Business | Remove the payroll rework and the disputes it causes; not separately quantified | 1.5.1.2 (D4) | Monthly sheet reconciles to the attendance records with zero manual adjustment rows | Accountant approves one full month close during the warranty month |
| FR01 | Authentication and role-based access control for seven roles, with account creation, password reset, and idle session timeout | System Administrator | Must have | Functional | Quality: A04 met | 1.4.1.1 (D3) | Each role reaches only its own screens and data in the UAT permission matrix | UAT script run by the System Administrator across all seven roles |
| FR02 | Student profile and enrollment, including transfer, seat reservation, withdrawal with refund calculation, and refusal on a full class or a timetable collision | Front-desk staff | Must have | Functional | Scope: F01 to F12 accepted; BR01 | 1.4.1.2 (D3) | Enrollment refused in both refusal cases; refund figure matches the policy worked example | Front-desk staff enroll, transfer, and withdraw a test cohort in UAT |
| FR03 | Course and curriculum catalog with versioning, so editing a course leaves already-opened classes unchanged | Academic Manager | Must have | Functional | Scope: F01 to F12 accepted | 1.4.1.3 (D3) | A course edit leaves the definition of an opened class unchanged | Academic Manager edits a course that has open classes in UAT |
| FR04 | Class opening from a course, generation of the session calendar, room and teacher assignment, conflict detection on room, teacher, and class time, recalculation on postponement | Academic Manager | Must have | Functional | BR02 | 1.4.2.1 (D3) | Every conflict case in the test set is blocked at creation or at move time | Academic Manager runs the conflict scenarios; pilot branch uses it for two weeks before M6 |
| FR05 | Attendance marking with four states and remarks, make-up session registration, attendance rate per student and per class | Teacher | Must have | Functional | Stakeholder satisfaction: <mark>90% of classes</mark> with attendance recorded in the first warranty month | 1.4.2.2 (D3) | Attendance rate figures match a hand count for a sample class over one month | Teachers mark real sessions during the pilot at one branch |
| FR06 | Tuition invoicing from the course fee with discount policies and installment plans, payment recording, receipts, outstanding balance, aged debt list per student, class, and branch | Front-desk staff, Accountant | Must have | Functional | BR03 | 1.5.1.1 (D4) | Invoice totals match the policy worked examples; aged debt list ties to the invoice ledger | Accountant reconciles one term of test invoices and payments in UAT |
| FR07 | Teacher records and teaching-hour payroll, aggregating delivered sessions into a monthly sheet with allowances and deductions, exported to Excel | Accountant | Must have | Functional | BR06 | 1.5.1.2 (D4) | Monthly sheet reconciles to attendance with zero manual adjustment rows | Accountant closes one test month end to end |
| FR08 | Assessment, pass or fail computation, printable progress report, class result summary, and end-of-course evaluation of course and teacher on a five-point scale | Teacher | Should have | Functional | Scope: F01 to F12 accepted | 1.5.2.1 (D4) | Final results match the course rule for every pass and fail boundary case | Academic Manager checks one completed course in UAT |
| FR09 | Notification and internal communication by email and SMS from templates, manual and scheduled sending, per-message delivery log, announcements, class notice board, and parent messages | Front-desk staff | Must have | Functional | BR05 | 1.5.2.2 (D4) | Every message carries a delivery state; failures carry a reason and are retried | Front-desk staff send each of the seven event types in UAT |
| FR10 | Reports and management dashboard, filterable by period, branch, and course, exporting to Excel and PDF | Center Director | Must have | Functional | BR04 | 1.5.3.1 (D4) | One term's report produced within 10 seconds; figures match the underlying records | Director runs every report unaided in UAT |
| FR11 | System administration and audit: reference data, configuration, backup and restore, and an audit log of every create, update, and delete on financial and student data | System Administrator | Must have | Functional | Quality: A05 met | 1.5.3.2 (D4) | Every financial and student write appears in the audit log with user and timestamp | System Administrator samples the log against a scripted set of changes |
| FR12 | Android and iOS app from one cross-platform codebase over the same API and accounts, covering the parent and teacher functions, with push as the third notification channel | Student / Parent, Teacher | Must have | Functional | BR05; Stakeholder satisfaction: <mark>70% of guardians with a smartphone</mark> activated by closeout | 1.5.4.1, 1.9.1.3 (D4, D11) | Every F12 function within 3 taps; push delivery recorded in the F09 log | Parents and teachers use the app during the pilot and the first warranty month |
| NFR01 | Functional completeness: all twelve functions accepted in UAT, at least 99% of test cases passed, no open Critical or High defect and none of any severity in the money path | Center Director, sponsor | Must have | Acceptance | Scope: no function deferred without an approved change request | 1.6.2.3, 1.8.3.2 (D5) | UAT pass rate at or above 99%; defect log shows no open Critical or High | UAT sign-off by the sponsor at M6 against the test set agreed at M5 |
| NFR02 | Staff screens respond within 3 seconds at <mark>52 concurrent staff users</mark>; parent portal within 3 seconds at <mark>300 concurrent sessions</mark>; one term's report within 10 seconds; app screens within 3 seconds on 4G | Center Director | Must have | Performance | Quality: A02 met | 1.6.1.3 (D5) | Load test report shows the 95th percentile inside each threshold | Load test witnessed by the System Administrator before UAT entry |
| NFR03 | <mark>5,000 student records, 200 classes per term, and 3 years of session history</mark> without redesign | System Administrator | Must have | Capacity | Quality: A03 met | 1.6.1.3 (D5) | Capacity test loads the stated volumes and the performance thresholds still hold | Same load test run, at the stated data volume |
| NFR04 | HTTPS only, no recoverable password storage, server-side authorisation on every request, compliance with the <mark>Law on Personal Data Protection in force from 1 January 2026</mark>, consent recorded per guardian, expiring app tokens, no unencrypted personal data cached on the device | System Administrator | Must have | Security | Quality: A04 met | 1.3.1.1, 1.6.1.4 (D2, D5) | Security test finds no unauthorised access path and no readable stored password | Security test report reviewed and accepted before UAT entry |
| NFR05 | Every create, update, and delete on financial and student records written to a log that cannot be edited and kept for at least <mark>3 years</mark> | Accountant | Must have | Auditability | Quality: A05 met | 1.5.3.2 (D4) | Log entries cannot be altered through any interface; retention setting is <mark>3 years</mark> | Accountant and System Administrator attempt an edit in UAT and fail |
| NFR06 | <mark>99% availability between 07:00 and 22:00</mark> measured monthly, nightly backup, recovery point 24 hours, recovery time 4 hours, restore demonstrated once in UAT and once in warranty | System Administrator | Must have | Availability | Quality: A06 met | 1.8.1.2 (D7) | Restore drill completes inside 4 hours from a backup no more than 24 hours old | Restore drill witnessed by the System Administrator, twice |
| NFR07 | A written paper fallback and catch-up procedure exists, is trained, and is rehearsed once before go-live | Academic Manager | Should have | Continuity | Quality: A07 met | 1.8.2.3 (D8) | Rehearsal record signed, with the catch-up entry reconciled afterwards | Rehearsal run at one branch before M6 |
| NFR08 | Vietnamese interface; attendance, payment recording, and enrollment each within 3 clicks of the home screen; daily tasks performable after half a day of training | Front-desk staff, Teacher | Must have | Usability | Stakeholder satisfaction: <mark>80% of the 52 staff users</mark> trained and active in the first month | 1.3.1.4, 1.8.2.2 (D2, D8) | Click count measured on each of the three paths; training record shows the half-day format | Staff perform their daily tasks unaided the day after training |
| NFR09 | Latest two versions of Chrome, Edge, and Firefox; usable on tablet and phone for teacher and parent screens; app on <mark>Android 10 and later and iOS 15 and later</mark>, phones only | System Administrator | Should have | Compatibility | Quality: A09 met | 1.6.1.1, 1.6.1.2 (D5) | Test matrix covers every listed browser and both app platforms | Cross-browser and device test run before UAT entry |
| NFR10 | Coding convention applied, deployment guide and schema documentation delivered with the source code | System Administrator | Should have | Maintainability | Quality: A10 met | 1.8.2.1, 1.8.3.1 (D8, D9) | Handover checklist complete; a third party can deploy from the guide alone | System Administrator deploys to staging following only the guide |
| NFR11 | A complete export of the center's data in an open format, produced by the center's own administrator without the supplier | Center Director | Must have | Data ownership | Quality: A11 met | 1.5.3.2 (D4) | Export runs to completion from the administrator screen and opens in a standard tool | System Administrator produces the export unaided in UAT |
| NFR12 | App published in both stores under the center's accounts, every F12 function within 3 taps, push delivery logged, SMS fallback for tuition messages within 4 hours of a failed push | Center Director | Must have | Mobile | Quality: A12 met; BR05 | 1.9.1.3, 1.5.4.2 (D11) | Store listings live; fallback timer verified in the delivery log | Guardians install from the public store listing during the pilot |

### Part 1B: Inter-Requirements Traceability Matrix

*Form 2.7, page 2 of 2. Each business requirement is paired with the functional or nonfunctional
requirement that implements it. Where one business requirement needs several, it appears once per pair,
which is how the printed form carries a one-to-many relationship.*

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| ID | Business Requirement | Priority | Source | ID | Technical Requirement | Priority | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BR01 | Data held once and entered once | Must have | Center Director | FR02 | Student profile and enrollment on one shared record | Must have | Front-desk staff |
| BR01 | Data held once and entered once | Must have | Center Director | FR03 | Versioned course catalog as the single definition of what is sold | Must have | Academic Manager |
| BR01 | Data held once and entered once | Must have | Center Director | NFR11 | Complete open-format export owned by the center | Must have | Center Director |
| BR02 | No double-booked room, teacher, or student | Must have | Academic Manager | FR04 | Conflict detection at creation and at move time | Must have | Academic Manager |
| BR02 | No double-booked room, teacher, or student | Must have | Academic Manager | NFR02 | Conflict check completes inside the 3 second screen budget | Must have | Center Director |
| BR03 | Overdue tuition visible and falling to <mark>3%</mark> | Must have | Accountant | FR06 | Invoicing, payment recording, and the aged debt list | Must have | Accountant |
| BR03 | Overdue tuition visible and falling to <mark>3%</mark> | Must have | Accountant | FR09 | Tuition due and overdue notifications with a delivery log | Must have | Front-desk staff |
| BR03 | Overdue tuition visible and falling to <mark>3%</mark> | Must have | Accountant | NFR05 | Audit log over every financial write | Must have | Accountant |
| BR04 | Cross-branch visibility without a spreadsheet | Must have | Center Director | FR10 | Reports and dashboard filterable by period, branch, course | Must have | Center Director |
| BR04 | Cross-branch visibility without a spreadsheet | Must have | Center Director | NFR02 | One term's report inside 10 seconds | Must have | Center Director |
| BR04 | Cross-branch visibility without a spreadsheet | Must have | Center Director | NFR03 | <mark>3 years</mark> of history held without redesign | Must have | System Administrator |
| BR05 | Notification cost held down | Should have | Center Director | FR12 | App as the push channel over the same API | Must have | Student / Parent |
| BR05 | Notification cost held down | Should have | Center Director | NFR12 | Push delivery logged with SMS fallback inside 4 hours | Must have | Center Director |
| BR06 | Payroll derived from delivered sessions | Must have | Accountant | FR05 | Attendance as the single record of what was taught | Must have | Teacher |
| BR06 | Payroll derived from delivered sessions | Must have | Accountant | FR07 | Monthly teaching-hour sheet and payroll export | Must have | Accountant |
| BR06 | Payroll derived from delivered sessions | Must have | Accountant | NFR05 | Audit trail over the sheet and its approval | Must have | Accountant |

---

## Part 2: Work Breakdown Structure

*Form 2.9, page 1 of 1. The printed form is a numeric outline running from the project at level 1 down
to work packages; that is what is reproduced here. Control accounts are marked **CA**; every line below
a control account is a work package.*

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

```
1.        Learning Center Management Software

1.1       Project Management                                          (major deliverable)
1.1.1       Project Governance                                        CA
1.1.1.1       Kickoff and team mobilisation
1.1.1.2       Project management plan and schedule baseline
1.1.1.3       Weekly status reporting and sponsor governance
1.1.1.4       Risk, issue, and change control
1.1.1.5       Contingency reserve

1.2       Requirements                                                (major deliverable, D1, M1)
1.2.1       Elicitation                                               CA
1.2.1.1       Stakeholder workshops and current-process study
1.2.1.2       Functional requirements specification, F01 to F12
1.2.1.3       Nonfunctional requirements specification, A01 to A12
1.2.1.4       Exception and failure behaviour catalogue
1.2.2       Requirements Baseline                                     CA
1.2.2.1       Requirements traceability matrix
1.2.2.2       Requirements peer review and rework
1.2.2.3       Requirements acceptance and baseline
1.2.3       Technical Preparation                                     CA
1.2.3.1       Development, test, and staging environment setup
1.2.3.2       Notification gateway proof of concept
1.2.3.3       Cross-platform framework proof
1.2.3.4       User interface prototype for business validation

1.3       Design                                                      (major deliverable, D2, M2)
1.3.1       Solution Design                                           CA
1.3.1.1       Architecture, security, and personal-data design
1.3.1.2       Database schema design
1.3.1.3       Server API contract
1.3.1.4       Web user interface design
1.3.1.5       Mobile application design
1.3.2       Design Assurance                                          CA
1.3.2.1       Design review and rework
1.3.2.2       Test plan and test strategy
1.3.2.3       Design baseline acceptance

1.4       Construction Iteration 1                                    (major deliverable, D3, M3)
1.4.1       Core Platform                                             CA
1.4.1.1       F01 Authentication and access control
1.4.1.2       F02 Student profile and enrollment
1.4.1.3       F03 Course and curriculum catalog
1.4.2       Scheduling and Attendance                                 CA
1.4.2.1       F04 Class opening, scheduling, and assignment
1.4.2.2       F05 Attendance and make-up sessions
1.4.3       Iteration 1 Assurance                                     CA
1.4.3.1       Iteration 1 code review and rework
1.4.3.2       Iteration 1 unit and integration testing
1.4.3.3       Iteration 1 demo and acceptance

1.5       Construction Iteration 2                                    (major deliverable, D4, M4)
1.5.1       Finance                                                   CA
1.5.1.1       F06 Tuition, invoicing, and debt tracking
1.5.1.2       F07 Teacher records and teaching-hour payroll
1.5.2       Academic and Communication                                CA
1.5.2.1       F08 Assessment, progress reports, and course evaluation
1.5.2.2       F09 Notification and internal communication
1.5.3       Management and Administration                             CA
1.5.3.1       F10 Reports and management dashboard
1.5.3.2       F11 System administration and audit
1.5.4       Mobile Application                                        CA
1.5.4.1       F12 Mobile application build
1.5.4.2       Push notification integration
1.5.5       Iteration 2 Assurance                                     CA
1.5.5.1       Iteration 2 code review and rework
1.5.5.2       Iteration 2 unit and integration testing
1.5.5.3       Iteration 2 acceptance, feature complete

1.6       Quality Assurance and Test                                  (major deliverable, D5, M5)
1.6.1       System Test                                               CA
1.6.1.1       System test execution, web
1.6.1.2       System test execution, Android and iOS
1.6.1.3       Performance and capacity test
1.6.1.4       Security test
1.6.1.5       Defect fixing and regression
1.6.2       Test Documentation                                        CA
1.6.2.1       Test cases and UAT test set
1.6.2.2       Defect log and test summary report
1.6.2.3       UAT entry criteria review

1.7       Data Migration                                              (major deliverable, D6, M6)
1.7.1       Migration                                                 CA
1.7.1.1       Source data analysis and cleansing rules
1.7.1.2       Migration scripts and trial run
1.7.1.3       Production migration and reconciliation report
1.7.1.4       Accountant acceptance of the reconciliation

1.8       Deployment and Handover                                     (major deliverable, D7 D8 D9, M6)
1.8.1       Production Environment                                    CA
1.8.1.1       Cloud server and staging provisioning
1.8.1.2       Backup configuration and restore drill
1.8.1.3       Production deployment and go-live
1.8.2       Training and Documentation                                CA
1.8.2.1       User, administrator, and deployment documentation
1.8.2.2       Staff training delivery and training record
1.8.2.3       Paper fallback procedure and rehearsal
1.8.3       Handover                                                  CA
1.8.3.1       Source code, database scripts, and technical documentation handover
1.8.3.2       User acceptance testing execution and sign-off

1.9       Mobile Application Release                                  (major deliverable, D11, M6)
1.9.1       Store Release                                             CA
1.9.1.1       Store accounts and signing keys
1.9.1.2       Store listings and release notes
1.9.1.3       Store submission and review response

1.10      Warranty and Closeout                                       (major deliverable, D10, M7)
1.10.1      Warranty                                                  CA
1.10.1.1      First warranty month support
1.10.1.2      Warranty handover to the support desk
1.10.2      Closeout                                                  CA
1.10.2.1      Closeout report and lessons learned
1.10.2.2      Final acceptance and project close
```

### Roll-up

Ten major deliverables, twenty-three control accounts, seventy work packages. Each work package appears
under exactly one control account.

| Phase | Control accounts | Work packages | Charter deliverables | Milestone | Labor hours | Labor cost (VND) | Other cost (VND) | Total (VND) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.1 Project Management | 1 | 5 | internal | M0 to M7 | 300 | 48,750,000 | 45,700,000 | 94,450,000 |
| 1.2 Requirements | 3 | 11 | D1 | M1 | 560 | 74,250,000 | 0 | 74,250,000 |
| 1.3 Design | 2 | 8 | D2 | M2 | 380 | 45,750,000 | 0 | 45,750,000 |
| 1.4 Construction Iteration 1 | 3 | 8 | D3 | M3 | 650 | 75,000,000 | 0 | 75,000,000 |
| 1.5 Construction Iteration 2 | 5 | 11 | D4 | M4 | 990 | 116,075,000 | 4,000,000 | 120,075,000 |
| 1.6 Quality Assurance and Test | 2 | 8 | D5 | M5 | 580 | 62,250,000 | 2,000,000 | 64,250,000 |
| 1.7 Data Migration | 1 | 4 | D6 | M6 | 160 | 19,375,000 | 12,000,000 | 31,375,000 |
| 1.8 Deployment and Handover | 3 | 8 | D7, D8, D9 | M6 | 200 | 25,375,000 | 59,000,000 | 84,375,000 |
| 1.9 Mobile Application Release | 1 | 3 | D11 | M6 | 90 | 11,425,000 | 3,300,000 | 14,725,000 |
| 1.10 Warranty and Closeout | 2 | 4 | D10 | M7 | 490 | 60,750,000 | 35,000,000 | 95,750,000 |
| **Total** | **23** | **70** | **D1 to D11** | **M0 to M7** | **4,400** | **539,000,000** | **161,000,000** | **700,000,000** |

Labor hours by resource: PM 800, developers 2,400, QA 800, mobile developer 400. At the charter's rate
mix that is 130,000,000 + 285,000,000 + 75,000,000 + 49,000,000 = 539,000,000 VND, which is budget
line 1 of the charter exactly. The other-cost column carries charter budget lines 2 to 6 and is
allocated to the work package that spends it, including the 28,000,000 VND contingency reserve, which is
held as its own work package rather than spread across the others.

The hours are effort, not calendar loading. Several packages inside a phase run in parallel, and some
run across phase boundaries: 1.2.3.1 and 1.6.2.1 both start early and finish late, and the warranty
phase carries the whole team because the charter puts the first warranty month inside the project.
Levelling that effort across the calendar is Develop Schedule, PMBOK 6 section 6.5, which produces the
schedule baseline rather than the scope baseline and is therefore not in this document; it is the work
of package 1.1.1.2.

Phase 1.2 carries a Technical Preparation control account that the charter's own risk responses require
before M2: the notification gateway proof for risk R5, the cross-platform framework proof for risk R12,
the environment and pipeline that acceptance criterion A10 depends on, and the prototype that tests the
interface against the people who will use it. Without it the requirements phase would hold three idle
developers and the two proofs the charter demands would have nowhere to live.

### Coverage check

| Charter item | Where the WBS delivers it |
| --- | --- |
| F01 to F05 | 1.4.1.1, 1.4.1.2, 1.4.1.3, 1.4.2.1, 1.4.2.2 |
| F06 to F11 | 1.5.1.1, 1.5.1.2, 1.5.2.1, 1.5.2.2, 1.5.3.1, 1.5.3.2 |
| F12 | 1.5.4.1 and 1.5.4.2, released by 1.9.1.3 |
| A01 to A12 | Verified across 1.6.1.1 to 1.6.1.5 and accepted in 1.8.3.2 |
| D1 to D11 | 1.2.2.3, 1.3.2.3, 1.4.3.3, 1.5.5.3, 1.6.2.2, 1.7.1.3, 1.8.1.3, 1.8.2.1, 1.8.3.1, 1.10.2.1, 1.9.1.3 |
| M0 to M7 | 1.1.1.1, 1.2.2.3, 1.3.2.3, 1.4.3.3, 1.5.5.3, 1.6.2.3, 1.8.3.2, 1.10.2.2 |
| 1.1.5 exception behaviour | Built inside the function package that owns it, tested in 1.6.1.1, and rehearsed in 1.8.2.3 |
| R1 to R12 responses | Owned by 1.1.1.4, with the gateway proof in 1.2.3.2, the framework proof in 1.2.3.3, the store enrolment in 1.9.1.1, and the pilot and parallel running in 1.8.1.3 |

---

## Part 3: WBS Dictionary

*Form 2.10, one sheet per work package, as the printed form is laid out: Page 1 of 1 per work package.
Field names and field order follow pages 52 to 55 of the book. Responsible Person is one of the
elements the book lists for the dictionary on page 52, and it carries the one-owner rule.*

Seventy sheets follow, one for each work package of Part 2, grouped by phase.

**What the hours mean.** The Labor Hours column is an **effort** estimate, not a calendar loading. The
milestone dates in the Due Dates field are the charter's gates, and several packages run in parallel
inside them. Levelling the effort across the calendar is Develop Schedule, PMBOK 6 section 6.5, which is
not part of the scope baseline and is not in this document; it happens in work package 1.1.1.2. The
totals are fixed by the charter and the sheets roll up to them exactly:

| | Hours | Rate (VND/h) | Amount (VND) |
| --- | ---: | ---: | ---: |
| Project manager and business analyst | 800 | 162,500 | 130,000,000 |
| Developers, three | 2,400 | 118,750 | 285,000,000 |
| QA engineer | 800 | 93,750 | 75,000,000 |
| Mobile developer, part time | 400 | 122,500 | 49,000,000 |
| **Labor total** | **4,400** | | **539,000,000** |
| Other cost, charter budget lines 2 to 6 | | | 161,000,000 |
| **Total** | | | **700,000,000** |

### Phase 1.1 Project Management

#### 1.1.1.1 Kickoff and team mobilisation

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Kickoff and team mobilisation |
| Code of Accounts | 1.1.1.1 |
| Responsible Person | PM |
| Description of Work | Hold the kickoff with the sponsor and the Center Director, walk the approved charter through with the whole team, assign the project manager named by the sponsor at M0, onboard the five full-time staff, and procure and issue the laptops, development tools, and workspace the team needs to start. |
| Assumptions and Constraints | The sponsor names the project manager on or before 14 September 2026; the charter is approved before kickoff; the part-time mobile developer is not mobilised here and joins after M2. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. M0 project kickoff, charter approved, team mobilised |
| Due Dates | <mark>Mon 14 September 2026 to Fri 18 September 2026; M0 on Mon 14 September 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.1.1.1-A1 | Kickoff meeting and charter walkthrough with sponsor and Director | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| 1.1.1.1-A2 | Team onboarding, accounts, and workspace setup | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| 1.1.1.1-A3 | Procure and issue laptops, development tools, and licences | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| 1.1.1.1-A4 | Development tools and licences | | | | | 1 | 8,700,000 | 8,700,000 | 8,700,000 |
| 1.1.1.1-A5 | Team workspace and laptops | | | | | 1 | 9,000,000 | 9,000,000 | 9,000,000 |
| | **Work package total** | | **40** | | **6,500,000** | | | **17,700,000** | **24,200,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every team member has an account, a machine, and repository access before the first requirements workshop. |
| Acceptance Criteria | Kickoff minutes signed by the sponsor; the project manager is named in writing; the team roster is complete. |
| Technical Information | Repository, issue tracker, and continuous integration account created under the supplier's organisation. |
| Agreement Information | Supplier contract for the 700,000,000 VND scope, signed before M0. |

*Page 1 of 1*

#### 1.1.1.2 Project management plan and schedule baseline

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Project management plan and schedule baseline |
| Code of Accounts | 1.1.1.2 |
| Responsible Person | PM |
| Description of Work | Produce the project management plan, the schedule baseline against milestones M0 to M7, the resource plan for the six people, and the communication plan, and have the sponsor accept them. |
| Assumptions and Constraints | The milestone dates in the charter are fixed and are not renegotiated here; the plan is updated at each milestone rather than rewritten. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Project management plan accepted by the sponsor |
| Due Dates | <mark>Mon 21 September 2026 to Fri 2 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.1.1.2-A1 | Schedule baseline and resource plan | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| 1.1.1.2-A2 | Communication and stakeholder engagement plan | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| 1.1.1.2-A3 | Baseline review and acceptance with the sponsor | PM | 20 | 162,500 | 3,250,000 | | | | 3,250,000 |
| | **Work package total** | | **60** | | **9,750,000** | | | **0** | **9,750,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every charter milestone appears in the schedule with an owner and a predecessor. |
| Acceptance Criteria | Sponsor accepts the plan in writing before the requirement baseline at M1. |
| Technical Information | Resource levelling of the effort estimates in this dictionary is performed here, in Develop Schedule, not in the WBS. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.1.1.3 Weekly status reporting and sponsor governance

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Weekly status reporting and sponsor governance |
| Code of Accounts | 1.1.1.3 |
| Responsible Person | PM |
| Description of Work | Produce the weekly status report to the sponsor and the Center Director for the whole project, run the milestone gate reviews at M1 to M7, and carry escalations to the sponsor within the agreed two working days. |
| Assumptions and Constraints | The project runs 21 weeks from M0 to M7; the customer commits the Academic Manager and the Accountant for at least four hours a week each, which the fixed weekly slot depends on. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Weekly report issued every week from M0<br>2. Gate review held at each of M1 to M7 |
| Due Dates | <mark>Mon 14 September 2026 to Fri 5 February 2027, weekly</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.1.1.3-A1 | Weekly status report, 21 weeks | PM | 84 | 162,500 | 13,650,000 | | | | 13,650,000 |
| 1.1.1.3-A2 | Milestone gate reviews at M1 to M7 | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| 1.1.1.3-A3 | Sponsor escalations and decision log | PM | 12 | 162,500 | 1,950,000 | | | | 1,950,000 |
| | **Work package total** | | **120** | | **19,500,000** | | | **0** | **19,500,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No week without a report; every escalation reaches the sponsor within 2 working days of being raised. |
| Acceptance Criteria | Sponsor confirms at closeout that the reporting obligation was met. |
| Technical Information | Report template fixed at M1 and not changed mid-project, so the variance series stays comparable. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.1.1.4 Risk, issue, and change control

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Risk, issue, and change control |
| Code of Accounts | 1.1.1.4 |
| Responsible Person | PM |
| Description of Work | Maintain the risk register R1 to R12 with owners and responses, review it weekly, run the issue log, and raise change requests into Perform Integrated Change Control with their scope, cost, and schedule impact assessed against the reserve. |
| Assumptions and Constraints | Change requests are an output of the controlling processes 5.5 and 5.6, not of the planning work in this document; this package is where they are raised and tracked once the project is executing. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Risk register baselined at M1<br>2. Weekly risk review from M1 |
| Due Dates | <mark>Mon 14 September 2026 to Fri 5 February 2027, weekly</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.1.1.4-A1 | Maintain the risk register R1 to R12 | PM | 32 | 162,500 | 5,200,000 | | | | 5,200,000 |
| 1.1.1.4-A2 | Weekly risk and issue review | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| 1.1.1.4-A3 | Raise and track change requests to integrated change control | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| | **Work package total** | | **80** | | **13,000,000** | | | **0** | **13,000,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every risk carries an owner and a response; every change request carries an impact assessment before it is put to the sponsor. |
| Acceptance Criteria | Sponsor accepts the risk register at M1 and the closeout risk position at M7. |
| Technical Information | Change requests are assessed against the 28,000,000 VND contingency reserve held in 1.1.1.5. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.1.1.5 Contingency reserve

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Contingency reserve |
| Code of Accounts | 1.1.1.5 |
| Responsible Person | PM |
| Description of Work | Hold the contingency reserve of charter budget line 6 as a work package of its own rather than spreading it across the others, so that reserve use is visible. No labor is booked here; money leaves it only through an approved change request. |
| Assumptions and Constraints | The reserve is 4% of the 700,000,000 VND budget; an increase beyond it needs the sponsor's written approval, per the charter. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Reserve position reported monthly to the sponsor |
| Due Dates | <mark>Held from 14 September 2026 until closeout on 5 February 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.1.1.5-A1 | Contingency reserve, charter budget line 6 | | | | | 1 | 28,000,000 | 28,000,000 | 28,000,000 |
| | **Work package total** | | **0** | | **0** | | | **28,000,000** | **28,000,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Reserve drawn only against an approved change request, never to absorb an overrun silently. |
| Acceptance Criteria | Closeout report states how much of the reserve was used and on what. |
| Technical Information |  |
| Agreement Information |  |

*Page 1 of 1*

### Phase 1.2 Requirements

#### 1.2.1.1 Stakeholder workshops and current-process study

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Stakeholder workshops and current-process study |
| Code of Accounts | 1.2.1.1 |
| Responsible Person | PM |
| Description of Work | Run requirement workshops with the seven roles of the requirement specification, study the current paper registers, Excel workbooks, and group-chat practice, and write the workshop notes that the specification is drafted from. |
| Assumptions and Constraints | The Academic Manager and the Accountant are available four hours a week; workshops cover all three branches but are held at the main branch. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
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
| Acceptance Criteria | Notes circulated and confirmed by the Academic Manager and the Accountant. |
| Technical Information | Source Excel workbooks and the paper register formats are collected here and become the input to 1.7.1.1. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.2.1.2 Functional requirements specification, F01 to F12

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Functional requirements specification, F01 to F12 |
| Code of Accounts | 1.2.1.2 |
| Responsible Person | PM |
| Description of Work | Draft the twelve functions F01 to F12 with a description of each, sketch the data model that carries them, and walk the draft through with the business owners of each area. |
| Assumptions and Constraints | Tuition, discount, and refund rules are frozen at M1 with written sign-off, which is the charter response to risk R2. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Draft specification circulated<br>2. Business walkthrough complete |
| Due Dates | <mark>Thu 17 September 2026 to Tue 29 September 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.1.2-A1 | Draft F01 to F12 with descriptions and actors | PM | 56 | 162,500 | 9,100,000 | | | | 9,100,000 |
| 1.2.1.2-A2 | Data model sketch supporting the twelve functions | DEV3 | 24 | 118,750 | 2,850,000 | | | | 2,850,000 |
| 1.2.1.2-A3 | Walkthrough with the business owners of each area | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| | **Work package total** | | **96** | | **14,550,000** | | | **0** | **14,550,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every function names a primary actor and states what it does; no function is described only by its happy path. |
| Acceptance Criteria | Business owners confirm each function in their area before the peer review in 1.2.2.2. |
| Technical Information | Data model sketch becomes the input to the schema design in 1.3.1.2. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.2.1.3 Nonfunctional requirements specification, A01 to A12

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Nonfunctional requirements specification, A01 to A12 |
| Code of Accounts | 1.2.1.3 |
| Responsible Person | PM |
| Description of Work | Draft the twelve acceptance criteria A01 to A12 as measurable thresholds covering performance, capacity, security, auditability, availability, degraded operation, usability, compatibility, maintainability, data ownership, and the mobile application, and check each for technical feasibility. |
| Assumptions and Constraints | Concurrency and capacity figures come from the charter assumptions and are rechecked against real usage during the warranty month. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Nonfunctional criteria drafted and feasibility checked |
| Due Dates | <mark>Wed 23 September 2026 to Tue 29 September 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.1.3-A1 | Draft A01 to A12 as measurable thresholds | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| 1.2.1.3-A2 | Technical feasibility check of each threshold | DEV3 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| | **Work package total** | | **40** | | **5,800,000** | | | **0** | **5,800,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every criterion is stated as a threshold that can be measured, not as a judgement. |
| Acceptance Criteria | Each criterion has a named verification method before the baseline at M1. |
| Technical Information | Thresholds become the test targets for 1.6.1.3 and 1.6.1.4. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.2.1.4 Exception and failure behaviour catalogue

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Exception and failure behaviour catalogue |
| Code of Accounts | 1.2.1.4 |
| Responsible Person | PM |
| Description of Work | Write the fourteen exception cases of the requirement specification, covering missing attendance, teacher absence, class cancellation, mid-course withdrawal, unmatched transfers, overpayment, gateway failure, payroll disputes, system unavailability, migration mismatch, loss of connectivity, guardians without the application, store rejection, and undelivered push. |
| Assumptions and Constraints | Exception behaviour is in scope on the same terms as the functions themselves and is tested with the same weight. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Exception catalogue complete |
| Due Dates | <mark>Thu 24 September 2026 to Wed 30 September 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.1.4-A1 | Write the fourteen exception cases and their required behaviour | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| 1.2.1.4-A2 | Technical review of the failure paths | DEV3 | 8 | 118,750 | 950,000 | | | | 950,000 |
| | **Work package total** | | **32** | | **4,850,000** | | | **0** | **4,850,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every function added to the specification has its failure behaviour written before the baseline. |
| Acceptance Criteria | Academic Manager and Accountant confirm the operational cases in their areas. |
| Technical Information | The catalogue is the source of the negative test cases written in 1.6.2.1. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.2.2.1 Requirements traceability matrix

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Requirements traceability matrix |
| Code of Accounts | 1.2.2.1 |
| Responsible Person | PM |
| Description of Work | Build the requirements traceability matrix on form 2.7: business requirements from the charter business case, functional requirements from F01 to F12, nonfunctional requirements from A01 to A12, each traced to a business objective, a deliverable, a verification metric, and a validation technique, plus the inter-requirements matrix pairing business against technical requirements. |
| Assumptions and Constraints | The matrix is an output of Collect Requirements, not an input to Create WBS; the deliverable column is completed once the WBS codes exist. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
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

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Requirements peer review and rework |
| Code of Accounts | 1.2.2.2 |
| Responsible Person | QA1 |
| Description of Work | Review the drafted specification against the workshop notes and the charter, record findings, and rework the specification. The review is owned by the QA engineer, who did not write the specification; the project manager, who did, performs the rework. |
| Assumptions and Constraints | The QA engineer acts as the second reader of the specification, which is the charter response to risk R9. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Review findings closed |
| Due Dates | <mark>Wed 30 September 2026 to Thu 1 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.2.2-A1 | Requirements review against the workshop notes and the charter | QA1 | 24 | 93,750 | 2,250,000 | | | | 2,250,000 |
| 1.2.2.2-A2 | Technical review of the data model and the failure paths | DEV3 | 12 | 118,750 | 1,425,000 | | | | 1,425,000 |
| 1.2.2.2-A3 | Rework of the specification against the findings | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| | **Work package total** | | **44** | | **4,975,000** | | | **0** | **4,975,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No reviewer reviews their own work; every finding is closed or explicitly accepted before the baseline. |
| Acceptance Criteria | Finding list closed and signed by the reviewer before M1. |
| Technical Information |  |
| Agreement Information |  |

*Page 1 of 1*

#### 1.2.2.3 Requirements acceptance and baseline

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Requirements acceptance and baseline |
| Code of Accounts | 1.2.2.3 |
| Responsible Person | PM |
| Description of Work | Present the specification to the sponsor and the Center Director, obtain written sign-off, and baseline it. From this point the tuition, discount, and refund rules are frozen and changes run through the change process. |
| Assumptions and Constraints | Sign-off is obtained on the milestone date; a slip here moves every downstream milestone, which is why it is a gate. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
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
| Technical Information | The baselined version is tagged in the repository and referenced by every later change request. |
| Agreement Information | Acceptance record forms part of the supplier contract file. |

*Page 1 of 1*

#### 1.2.3.1 Development, test, and staging environment setup

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Development, test, and staging environment setup |
| Code of Accounts | 1.2.3.1 |
| Responsible Person | DEV1 |
| Description of Work | Stand up the development, test, and staging environments, the source repository, the branching convention, the build pipeline, and the coding convention that the maintainability criterion A10 requires, so that construction starts against a working pipeline rather than building one. |
| Assumptions and Constraints | Staging runs on the same cloud provider as production, which is provisioned later in 1.8.1.1; the 12-month subscription in the charter starts at provisioning, not here. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Pipeline green on an empty build |
| Due Dates | <mark>Mon 14 September 2026 to Fri 2 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.3.1-A1 | Repository, branching convention, and coding convention | DEV1 | 32 | 118,750 | 3,800,000 | | | | 3,800,000 |
| 1.2.3.1-A2 | Build and test pipeline | DEV1 | 40 | 118,750 | 4,750,000 | | | | 4,750,000 |
| 1.2.3.1-A3 | Development and test environment provisioning | DEV1 | 28 | 118,750 | 3,325,000 | | | | 3,325,000 |
| | **Work package total** | | **100** | | **11,875,000** | | | **0** | **11,875,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | A commit runs the build and the test suite without manual steps. |
| Acceptance Criteria | Every developer can build and run the system locally and on staging before M2. |
| Technical Information | Coding convention is the one referenced by acceptance criterion A10 and handed over in 1.8.3.1. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.2.3.2 Notification gateway proof of concept

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Notification gateway proof of concept |
| Code of Accounts | 1.2.3.2 |
| Responsible Person | DEV2 |
| Description of Work | Prove the email and SMS notification gateway behind a single interface before the design baseline, including the delivery-state callback and the low-credit alert, and evaluate a second provider as a fallback. |
| Assumptions and Constraints | This is the charter response to risk R5: isolate the gateway behind one interface and prove it with a proof of concept before M2, keeping a second provider as fallback. Gateway credit for development is charged to 1.5.2.2. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Gateway proof of concept accepted<br>2. Fallback provider identified |
| Due Dates | <mark>Mon 21 September 2026 to Fri 2 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.3.2-A1 | Gateway integration behind a single interface | DEV2 | 48 | 118,750 | 5,700,000 | | | | 5,700,000 |
| 1.2.3.2-A2 | Delivery-state callback and low-credit alert proof | DEV2 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.2.3.2-A3 | Second provider evaluation as fallback | DEV2 | 12 | 118,750 | 1,425,000 | | | | 1,425,000 |
| | **Work package total** | | **80** | | **9,500,000** | | | **0** | **9,500,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No gateway detail leaks outside the interface, so a provider can be swapped without touching F09. |
| Acceptance Criteria | Proof of concept demonstrated before the design baseline at M2. |
| Technical Information | The interface designed here is the one F09 is built against in 1.5.2.2. |
| Agreement Information | Gateway provider terms reviewed; contract signed by the center, not the supplier. |

*Page 1 of 1*

#### 1.2.3.3 Cross-platform framework proof

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Cross-platform framework proof |
| Code of Accounts | 1.2.3.3 |
| Responsible Person | DEV3 |
| Description of Work | Prove the chosen cross-platform framework on both Android and iOS before the design baseline, covering push registration, secure token storage, and the read-only last-synced view, so that the platform half of risk R12 is closed before any application code is committed. |
| Assumptions and Constraints | <mark>One cross-platform codebase, Flutter or React Native</mark>; the framework choice is made here and is fixed for the project. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Framework proven on Android and iOS |
| Due Dates | <mark>Mon 28 September 2026 to Fri 9 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.2.3.3-A1 | Framework spike on Android and iOS | DEV3 | 24 | 118,750 | 2,850,000 | | | | 2,850,000 |
| 1.2.3.3-A2 | Push registration and secure token storage proof | DEV3 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| | **Work package total** | | **40** | | **4,750,000** | | | **0** | **4,750,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The same codebase runs on both platforms with no platform-specific fork of the business logic. |
| Acceptance Criteria | Both platforms demonstrated before the design baseline at M2. |
| Technical Information | Closes the framework half of risk R12; the store half is closed in 1.9. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.2.3.4 User interface prototype for business validation

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | User interface prototype for business validation |
| Code of Accounts | 1.2.3.4 |
| Responsible Person | DEV2 |
| Description of Work | Build a clickable prototype of the enrollment, attendance, and payment screens so that the business owners validate the interface against their daily work before the design is baselined rather than after it is built. |
| Assumptions and Constraints | The prototype is throwaway and is not the basis of the delivered interface; it exists to expose misunderstandings early. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Prototype walkthrough with front-desk staff and teachers |
| Due Dates | <mark>Mon 28 September 2026 to Fri 9 October 2026</mark> |

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

### Phase 1.3 Design

#### 1.3.1.1 Architecture, security, and personal-data design

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Architecture, security, and personal-data design |
| Code of Accounts | 1.3.1.1 |
| Responsible Person | DEV3 |
| Description of Work | Design the application architecture, the deployment topology across the cloud server and staging, the authentication and role-based authorisation model for the seven roles, and the personal-data handling that the applicable data protection law requires, including guardian consent recording and application token expiry. |
| Assumptions and Constraints | <mark>The Law on Personal Data Protection in force from 1 January 2026</mark> applies to guardian and student data; one cloud virtual server plus staging is the whole production topology. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Architecture accepted into the design baseline |
| Due Dates | <mark>Mon 5 October 2026 to Fri 9 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.1.1-A1 | Application architecture and deployment topology | DEV3 | 36 | 118,750 | 4,275,000 | | | | 4,275,000 |
| 1.3.1.1-A2 | Security model and personal-data design | DEV3 | 24 | 118,750 | 2,850,000 | | | | 2,850,000 |
| 1.3.1.1-A3 | Architecture review with the sponsor and the System Administrator | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| | **Work package total** | | **76** | | **9,725,000** | | | **0** | **9,725,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every request authorised on the server; no design that stores a recoverable password. |
| Acceptance Criteria | Accepted at the design baseline gate in 1.3.2.3; verified later by the security test in 1.6.1.4. |
| Technical Information | Serves NFR04 and NFR11 of the traceability matrix. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.3.1.2 Database schema design

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Database schema design |
| Code of Accounts | 1.3.1.2 |
| Responsible Person | DEV1 |
| Description of Work | Design the shared database schema that is the single source of truth for students, courses, classes, sessions, attendance, invoices, payments, and teaching hours, with keys chosen so that the Excel migration in 1.7 can be reconciled record by record. |
| Assumptions and Constraints | One shared database serves the web application and the mobile application; <mark>3 years of session history</mark> is held without redesign. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Schema accepted into the design baseline |
| Due Dates | <mark>Mon 5 October 2026 to Mon 12 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.1.2-A1 | Entity and relationship design from the data model sketch | DEV1 | 36 | 118,750 | 4,275,000 | | | | 4,275,000 |
| 1.3.1.2-A2 | Key design and migration reconciliation strategy | DEV1 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| | **Work package total** | | **52** | | **6,175,000** | | | **0** | **6,175,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No entity holds data that another entity also owns; the same data is never entered in two places. |
| Acceptance Criteria | Accepted at 1.3.2.3 and proven by the trial migration in 1.7.1.2. |
| Technical Information | Schema documentation is part of the handover in 1.8.3.1. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.3.1.3 Server API contract

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Server API contract |
| Code of Accounts | 1.3.1.3 |
| Responsible Person | DEV2 |
| Description of Work | Specify the documented server API that serves the web application and the mobile application alike, covering every function of F01 to F12, with versioning, error contracts, and the authorisation rules per endpoint. |
| Assumptions and Constraints | The mobile application uses the same API and the same accounts as the web application; no function is application-only. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. API contract accepted into the design baseline |
| Due Dates | <mark>Mon 5 October 2026 to Mon 12 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.1.3-A1 | Endpoint design and error contract across F01 to F12 | DEV2 | 36 | 118,750 | 4,275,000 | | | | 4,275,000 |
| 1.3.1.3-A2 | Versioning, authorisation rules, and API documentation | DEV2 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| | **Work package total** | | **52** | | **6,175,000** | | | **0** | **6,175,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every endpoint documented before it is built; no undocumented endpoint reaches the mobile application. |
| Acceptance Criteria | Accepted at 1.3.2.3; the API documentation is handed over in 1.8.3.1. |
| Technical Information | The contract is the interface the notification gateway of 1.2.3.2 sits behind. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.3.1.4 Web user interface design

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Web user interface design |
| Code of Accounts | 1.3.1.4 |
| Responsible Person | DEV1 |
| Description of Work | Design the Vietnamese-language web interface for the staff roles, folding in the prototype findings from 1.2.3.4, with attendance, payment recording, and enrollment each reachable within three clicks of the home screen, and a layout that remains usable on a tablet. |
| Assumptions and Constraints | Staff use the web application from a desktop browser; the interface is Vietnamese only. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Web interface design accepted into the design baseline |
| Due Dates | <mark>Wed 7 October 2026 to Wed 14 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.1.4-A1 | Screen flows and layouts for the staff roles | DEV1 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
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

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Mobile application design |
| Code of Accounts | 1.3.1.5 |
| Responsible Person | DEV3 |
| Description of Work | Design the parent and teacher application for Android and iOS on the framework proven in 1.2.3.3, so that the application design is inside the M2 baseline as the charter requires. The design is done by the web team because the part-time mobile developer joins after M2 and builds against this design. |
| Assumptions and Constraints | <mark>The charter has the mobile developer joining after M2 while the M2 baseline must already contain the application design, so the design is done by DEV3 and handed to MOB1 at mobilisation.</mark> Android 10 and later, iOS 15 and later, phones only. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Application design accepted into the design baseline |
| Due Dates | <mark>Thu 8 October 2026 to Thu 15 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.1.5-A1 | Application screen design for the parent and teacher journeys | DEV3 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.3.1.5-A2 | Offline and degraded-state design for loss of connectivity | DEV3 | 8 | 118,750 | 950,000 | | | | 950,000 |
| | **Work package total** | | **28** | | **3,325,000** | | | **0** | **3,325,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every F12 function reachable within three taps of the home screen in the design. |
| Acceptance Criteria | Accepted at 1.3.2.3; built against in 1.5.4.1. |
| Technical Information | The read-only last-synced view with a timestamp is designed here, per the connectivity exception case. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.3.2.1 Design review and rework

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Design review and rework |
| Code of Accounts | 1.3.2.1 |
| Responsible Person | QA1 |
| Description of Work | Review the architecture, schema, API contract, and interface designs against the requirement baseline, cross-review the API and the schema between developers who did not write them, and rework against the findings. |
| Assumptions and Constraints | No designer reviews their own design. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Design review findings closed |
| Due Dates | <mark>Tue 13 October 2026 to Thu 15 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.2.1-A1 | Design review against the requirement baseline | QA1 | 16 | 93,750 | 1,500,000 | | | | 1,500,000 |
| 1.3.2.1-A2 | Cross-review of the schema and the architecture | DEV2 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.3.2.1-A3 | Rework coordination and finding closure | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| | **Work package total** | | **52** | | **6,475,000** | | | **0** | **6,475,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every requirement in the baseline maps to something in the design; gaps are findings, not omissions. |
| Acceptance Criteria | Finding list closed before the baseline gate at M2. |
| Technical Information |  |
| Agreement Information |  |

*Page 1 of 1*

#### 1.3.2.2 Test plan and test strategy

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Test plan and test strategy |
| Code of Accounts | 1.3.2.2 |
| Responsible Person | QA1 |
| Description of Work | Write the test plan and test strategy covering unit, integration, system, performance, capacity, security, and user acceptance testing across web, Android, and iOS, with entry and exit criteria for each level and the defect severity definitions the warranty terms depend on. |
| Assumptions and Constraints | The QA engineer writes from the requirement baseline as a second reader, which is the charter response to risk R9. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Test plan accepted into the design baseline |
| Due Dates | <mark>Mon 5 October 2026 to Thu 15 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.3.2.2-A1 | Test plan across all levels and platforms | QA1 | 48 | 93,750 | 4,500,000 | | | | 4,500,000 |
| 1.3.2.2-A2 | Entry and exit criteria and defect severity definitions | QA1 | 16 | 93,750 | 1,500,000 | | | | 1,500,000 |
| 1.3.2.2-A3 | Test plan approval with the sponsor | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| | **Work package total** | | **72** | | **7,300,000** | | | **0** | **7,300,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Severity definitions match the warranty response targets in the charter, so the same word means the same thing after go-live. |
| Acceptance Criteria | Accepted at 1.3.2.3; the plan is part of D5. |
| Technical Information | The UAT test set is agreed later at M5 in 1.6.2.1 against this plan. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.3.2.3 Design baseline acceptance

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Design baseline acceptance |
| Code of Accounts | 1.3.2.3 |
| Responsible Person | PM |
| Description of Work | Present the architecture, schema, API contract, web interface, application design, and test plan to the customer, obtain acceptance, and baseline the design. |
| Assumptions and Constraints | Acceptance is a gate: construction does not begin against an unaccepted design. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
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

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | F01 Authentication and access control |
| Code of Accounts | 1.4.1.1 |
| Responsible Person | DEV3 |
| Description of Work | Build account creation, username and password authentication, password reset, idle session timeout, and role-based permission for the seven roles, with each account tied to exactly one role and staff accounts tied to one or more branches. |
| Assumptions and Constraints | Passwords are never stored or recoverable in readable form; every request is authorised on the server, not in the browser. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. F01 demonstrated at the iteration 1 demo |
| Due Dates | <mark>Mon 19 October 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.1.1-A1 | Account, authentication, and password reset | DEV3 | 32 | 118,750 | 3,800,000 | | | | 3,800,000 |
| 1.4.1.1-A2 | Role and branch permission model with server-side authorisation | DEV3 | 28 | 118,750 | 3,325,000 | | | | 3,325,000 |
| | **Work package total** | | **60** | | **7,125,000** | | | **0** | **7,125,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criterion A04; no screen or record reachable by a role that does not own it. |
| Acceptance Criteria | Permission matrix passes for all seven roles at the M3 demo. |
| Technical Information | Implements NFR01 and NFR04; the same accounts serve the mobile application through the API. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.4.1.2 F02 Student profile and enrollment

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | F02 Student profile and enrollment |
| Code of Accounts | 1.4.1.2 |
| Responsible Person | DEV2 |
| Description of Work | Build the student profile with guardian and contact details, enrollment into an open class, transfer between classes, seat reservation, and withdrawal with a refund calculation, refusing enrollment when the class is full or the timetable collides with another class of the same student. |
| Assumptions and Constraints | The refund calculation follows the center's policy as frozen at M1; a withdrawal produces a proposal and does not move the balance until the Accountant approves it. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. F02 demonstrated at the iteration 1 demo |
| Due Dates | <mark>Mon 19 October 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.1.2-A1 | Student profile and guardian records | DEV2 | 30 | 118,750 | 3,562,500 | | | | 3,562,500 |
| 1.4.1.2-A2 | Enrollment, transfer, reservation, and withdrawal | DEV2 | 40 | 118,750 | 4,750,000 | | | | 4,750,000 |
| 1.4.1.2-A3 | Refusal rules for full class and timetable collision | DEV2 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| | **Work package total** | | **90** | | **10,687,500** | | | **0** | **10,687,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | Both refusal cases are enforced by the server, not only by the screen. |
| Acceptance Criteria | A test cohort is enrolled, transferred, and withdrawn without a manual correction. |
| Technical Information | Serves BR01 and FR02; the refund proposal path is shared with 1.5.1.1. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.4.1.3 F03 Course and curriculum catalog

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | F03 Course and curriculum catalog |
| Code of Accounts | 1.4.1.3 |
| Responsible Person | DEV3 |
| Description of Work | Build the course catalog with code, level, session count, session length, standard fee, prerequisite, and session-by-session syllabus, versioned so that editing a course does not change the definition of classes already opened from it. |
| Assumptions and Constraints | Course versioning is a hard requirement, not an enhancement: without it, historical classes change retroactively when a fee is edited. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. F03 demonstrated at the iteration 1 demo |
| Due Dates | <mark>Mon 19 October 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.1.3-A1 | Course, level, fee, and syllabus records | DEV3 | 32 | 118,750 | 3,800,000 | | | | 3,800,000 |
| 1.4.1.3-A2 | Course versioning and its effect on opened classes | DEV3 | 28 | 118,750 | 3,325,000 | | | | 3,325,000 |
| | **Work package total** | | **60** | | **7,125,000** | | | **0** | **7,125,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | An edit to a course leaves every already-opened class untouched. |
| Acceptance Criteria | Academic Manager edits a course with open classes and the classes do not move. |
| Technical Information | Course versions are the input to the class generation in 1.4.2.1. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.4.2.1 F04 Class opening, scheduling, and assignment

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | F04 Class opening, scheduling, and assignment |
| Code of Accounts | 1.4.2.1 |
| Responsible Person | DEV1 |
| Description of Work | Build class opening from a course version with branch, start date, weekly slots, and capacity, generate the whole session calendar, assign a room and a teacher per session, detect and block conflicts on room, on teacher, and on class time at creation and at move time, and recalculate the calendar when a session is postponed. |
| Assumptions and Constraints | The charter assigns this to a developer with prior scheduling experience and builds it first in iteration 1, timeboxed, which is the response to risk R7. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. F04 demonstrated at the iteration 1 demo<br>2. Conflict test set passed |
| Due Dates | <mark>Mon 19 October 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.2.1-A1 | Class opening and session calendar generation | DEV1 | 48 | 118,750 | 5,700,000 | | | | 5,700,000 |
| 1.4.2.1-A2 | Room, teacher, and class-time conflict detection | DEV1 | 60 | 118,750 | 7,125,000 | | | | 7,125,000 |
| 1.4.2.1-A3 | Postponement and calendar recalculation | DEV1 | 32 | 118,750 | 3,800,000 | | | | 3,800,000 |
| | **Work package total** | | **140** | | **16,625,000** | | | **0** | **16,625,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Zero conflicting bookings accepted; conflict checking completes inside the 3 second screen budget. |
| Acceptance Criteria | Every conflict case in the test set is blocked; reviewed at the M3 demo as the charter requires. |
| Technical Information | Serves BR02 and FR04; the substitute-teacher and postponement exception cases are built here. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.4.2.2 F05 Attendance and make-up sessions

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | F05 Attendance and make-up sessions |
| Code of Accounts | 1.4.2.2 |
| Responsible Person | DEV2 |
| Description of Work | Build attendance marking with the four states and an optional remark, make-up session registration in another class, the attendance rate per student and per class, the late-entry stamp, and the daily exception list of sessions with missing attendance. |
| Assumptions and Constraints | A month containing missing attendance cannot be closed for payroll, which is what ties this package to 1.5.1.2. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. F05 demonstrated at the iteration 1 demo |
| Due Dates | <mark>Mon 19 October 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.2.2-A1 | Attendance marking, states, and remarks | DEV2 | 30 | 118,750 | 3,562,500 | | | | 3,562,500 |
| 1.4.2.2-A2 | Make-up sessions and attendance rate reporting | DEV2 | 24 | 118,750 | 2,850,000 | | | | 2,850,000 |
| 1.4.2.2-A3 | Late-entry stamping and the daily exception list | DEV2 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| | **Work package total** | | **70** | | **8,312,500** | | | **0** | **8,312,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | A late entry is stamped as late with the name of whoever entered it; nothing is silently backdated. |
| Acceptance Criteria | Attendance figures match a hand count for a sample class over one month. |
| Technical Information | Attendance is the only source of teaching hours in 1.5.1.2; there is no second entry path. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.4.3.1 Iteration 1 code review and rework

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Iteration 1 code review and rework |
| Code of Accounts | 1.4.3.1 |
| Responsible Person | DEV1 |
| Description of Work | Review the iteration 1 code against the design and the coding convention, and rework against the findings. Nobody reviews their own code: the developer who built the scheduling module reviews the core platform, and the developer who built the core platform reviews scheduling and attendance. |
| Assumptions and Constraints | Review is a work package, not an activity inside each build package, so that review effort is visible and cannot be quietly dropped when a build runs late. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Iteration 1 review findings closed |
| Due Dates | <mark>Mon 9 November 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.3.1-A1 | Review of F01, F02, and F03 by the scheduling developer | DEV1 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.4.3.1-A2 | Review of F04 and F05 and rework of the findings | DEV3 | 40 | 118,750 | 4,750,000 | | | | 4,750,000 |
| 1.4.3.1-A3 | Review against the test plan and the acceptance criteria | QA1 | 20 | 93,750 | 1,875,000 | | | | 1,875,000 |
| | **Work package total** | | **80** | | **9,000,000** | | | **0** | **9,000,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No author reviews their own work; every finding is closed or explicitly accepted before the demo. |
| Acceptance Criteria | Finding list closed before the M3 demo. |
| Technical Information | Coding convention is the one set in 1.2.3.1 and required by acceptance criterion A10. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.4.3.2 Iteration 1 unit and integration testing

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Iteration 1 unit and integration testing |
| Code of Accounts | 1.4.3.2 |
| Responsible Person | QA1 |
| Description of Work | Execute unit and integration testing across F01 to F05, including the exception cases that belong to them, log defects against the severity definitions, and retest after fixes. |
| Assumptions and Constraints | Testing is against the requirement baseline of M1, not against what was built. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Iteration 1 test cycle complete |
| Due Dates | <mark>Mon 2 November 2026 to Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.3.2-A1 | Unit and integration test execution across F01 to F05 | QA1 | 64 | 93,750 | 6,000,000 | | | | 6,000,000 |
| 1.4.3.2-A2 | Exception case testing for the iteration 1 functions | QA1 | 20 | 93,750 | 1,875,000 | | | | 1,875,000 |
| 1.4.3.2-A3 | Defect logging and retest | QA1 | 16 | 93,750 | 1,500,000 | | | | 1,500,000 |
| | **Work package total** | | **100** | | **9,375,000** | | | **0** | **9,375,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every defect carries a severity from the definitions agreed at M2. |
| Acceptance Criteria | No open Critical or High defect in F01 to F05 at the M3 demo. |
| Technical Information | Test results feed the defect log that becomes part of D5 in 1.6.2.2. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.4.3.3 Iteration 1 demo and acceptance

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Iteration 1 demo and acceptance |
| Code of Accounts | 1.4.3.3 |
| Responsible Person | PM |
| Description of Work | Demonstrate F01 to F05 and the application alpha to the customer, record the acceptance decision, and close the iteration. |
| Assumptions and Constraints | The M3 milestone releases the 25% payment tranche against the signed acceptance record. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. M3 iteration 1 demo accepted, F01 to F05, with the application alpha<br>2. D3 delivered |
| Due Dates | <mark>Fri 13 November 2026; M3 on Fri 13 November 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.4.3.3-A1 | Demo preparation and delivery to the customer | PM | 30 | 162,500 | 4,875,000 | | | | 4,875,000 |
| 1.4.3.3-A2 | Acceptance walkthrough against the iteration scope | QA1 | 20 | 93,750 | 1,875,000 | | | | 1,875,000 |
| | **Work package total** | | **50** | | **6,750,000** | | | **0** | **6,750,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The demo runs on the staging environment with migrated sample data, not on a developer machine. |
| Acceptance Criteria | Signed acceptance record of D3. |
| Technical Information | Scheduling is reviewed here specifically, as the charter response to risk R7 requires. |
| Agreement Information | Acceptance record releases the M3 payment tranche. |

*Page 1 of 1*

### Phase 1.5 Construction Iteration 2

#### 1.5.1.1 F06 Tuition, invoicing, and debt tracking

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | F06 Tuition, invoicing, and debt tracking |
| Code of Accounts | 1.5.1.1 |
| Responsible Person | DEV2 |
| Description of Work | Build tuition invoice generation at enrollment from the course fee with the sibling, early payment, referral, and promotion discount policies and installment plans, cash and bank-transfer payment recording, receipts, the outstanding balance, and the aged debt list per student, class, and branch, together with the unmatched payment list, the credit and reversal behaviour, and the rule that no overdue reminder is sent to a student with an unmatched payment on file. |
| Assumptions and Constraints | The rules are those frozen at M1; the charter assigns this to a developer with prior billing experience. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. F06 demonstrated at the iteration 2 review |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.1.1-A1 | Invoice generation, discount policies, and installments | DEV2 | 48 | 118,750 | 5,700,000 | | | | 5,700,000 |
| 1.5.1.1-A2 | Payment recording, receipts, and outstanding balance | DEV2 | 40 | 118,750 | 4,750,000 | | | | 4,750,000 |
| 1.5.1.1-A3 | Aged debt list per student, class, and branch | DEV2 | 22 | 118,750 | 2,612,500 | | | | 2,612,500 |
| 1.5.1.1-A4 | Unmatched payments, credits, and reversing entries | DEV2 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| | **Work package total** | | **130** | | **15,437,500** | | | **0** | **15,437,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | A receipt is never deleted; a reversal posts a reversing entry and both stay in the audit log. |
| Acceptance Criteria | Accountant reconciles one term of test invoices and payments with no manual correction. |
| Technical Information | Serves BR03 and FR06; the overdue percentage it reports is the measure the business case rests on. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.5.1.2 F07 Teacher records and teaching-hour payroll

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | F07 Teacher records and teaching-hour payroll |
| Code of Accounts | 1.5.1.2 |
| Responsible Person | DEV2 |
| Description of Work | Build teacher profiles, qualifications, contract type, and pay rate per teaching hour by course level, aggregate the sessions actually taught into a monthly teaching-hour sheet, apply allowances and deductions, run the draft, confirmed, approved, exported workflow, and export the payroll figures to Excel. |
| Assumptions and Constraints | Hours are credited to whoever actually taught, never to whoever was scheduled; the person who recorded the attendance never approves the sheet that pays for it. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. F07 demonstrated at the iteration 2 review |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.1.2-A1 | Teacher records, rates, and the monthly sheet | DEV2 | 18 | 118,750 | 2,137,500 | | | | 2,137,500 |
| 1.5.1.2-A2 | Sheet workflow, approval separation, and Excel export | DEV2 | 12 | 118,750 | 1,425,000 | | | | 1,425,000 |
| | **Work package total** | | **30** | | **3,562,500** | | | **0** | **3,562,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | A month containing missing attendance cannot be closed. |
| Acceptance Criteria | Accountant closes one test month end to end with zero manual adjustment rows. |
| Technical Information | Reads attendance from F05 only; there is no second entry path for teaching hours. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.5.2.1 F08 Assessment, progress reports, and course evaluation

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | F08 Assessment, progress reports, and course evaluation |
| Code of Accounts | 1.5.2.1 |
| Responsible Person | DEV3 |
| Description of Work | Build score recording for the assessment items a course defines, the per-student comment, the final result and pass or fail computation against the course rule, the printable progress report, the class result summary, and the end-of-course evaluation of course and teacher on a five-point scale with a free comment, reported per class and per teacher. |
| Assumptions and Constraints | The pass rule is part of the course definition and is versioned with it. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
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
| Technical Information | The evaluation is collected from the mobile application as well as the web, through the same API. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.5.2.2 F09 Notification and internal communication

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | F09 Notification and internal communication |
| Code of Accounts | 1.5.2.2 |
| Responsible Person | DEV3 |
| Description of Work | Build email and SMS sending from templates for the seven events, manual sending to a chosen group, scheduled automatic sending, the delivery log with a state and a failure reason per message, retry and manual action for failures, the low-credit alert, announcements, the per-class notice board, and messages between a parent and the front desk, all in the same log. |
| Assumptions and Constraints | Built against the gateway interface proven in 1.2.3.2. Development and test gateway credit of 4,000,000 VND from charter budget line 2 is spent here. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. F09 demonstrated at the iteration 2 review |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.2.2-A1 | Templates, manual send, and scheduled send | DEV3 | 28 | 118,750 | 3,325,000 | | | | 3,325,000 |
| 1.5.2.2-A2 | Delivery log, retry, failure reasons, and low-credit alert | DEV3 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.5.2.2-A3 | Announcements, class notice board, and parent messages | DEV3 | 12 | 118,750 | 1,425,000 | | | | 1,425,000 |
| 1.5.2.2-A4 | Development and test gateway credit | | | | | 1 | 4,000,000 | 4,000,000 | 4,000,000 |
| | **Work package total** | | **60** | | **7,125,000** | | | **4,000,000** | **11,125,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No failed notification is dropped without a record. |
| Acceptance Criteria | Front-desk staff send each of the seven event types and every message carries a delivery state. |
| Technical Information | Push becomes the third channel when 1.5.4.2 lands; SMS stays the fallback for guardians without the application. |
| Agreement Information | Gateway credit purchased under the center's own account with the provider. |

*Page 1 of 1*

#### 1.5.3.1 F10 Reports and management dashboard

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | F10 Reports and management dashboard |
| Code of Accounts | 1.5.3.1 |
| Responsible Person | DEV1 |
| Description of Work | Build the management view: revenue and collection by period and branch, outstanding debt, new and retained student counts, class fill rate, teacher workload and teaching hours, and attendance rate, every report filterable by period, branch, and course and exportable to Excel and PDF. |
| Assumptions and Constraints | Reports read the same records the operational screens write; there is no separate reporting copy of the data. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. F10 demonstrated at the iteration 2 review |
| Due Dates | <mark>Mon 16 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.3.1-A1 | Revenue, collection, and outstanding debt reporting | DEV1 | 32 | 118,750 | 3,800,000 | | | | 3,800,000 |
| 1.5.3.1-A2 | Enrollment, retention, fill rate, and workload reporting | DEV1 | 34 | 118,750 | 4,037,500 | | | | 4,037,500 |
| 1.5.3.1-A3 | Filters and Excel and PDF export | DEV1 | 24 | 118,750 | 2,850,000 | | | | 2,850,000 |
| | **Work package total** | | **90** | | **10,687,500** | | | **0** | **10,687,500** |

| Field | Content |
| --- | --- |
| Quality Requirements | A report covering one term is produced within 10 seconds. |
| Acceptance Criteria | Director runs every report unaided in UAT and the figures match the underlying records. |
| Technical Information | Serves BR04 and FR10; this is the package the fourth-branch decision depends on. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.5.3.2 F11 System administration and audit

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | F11 System administration and audit |
| Code of Accounts | 1.5.3.2 |
| Responsible Person | DEV1 |
| Description of Work | Build the reference data and configuration screens for branches, rooms, terms, fee and discount policies, notification templates, and holidays, backup triggering and restore, the audit log of every create, update, and delete on financial and student data with user and timestamp, and the complete data export the center can run itself. |
| Assumptions and Constraints | The audit log cannot be edited through any interface and is retained for <mark>3 years</mark>. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
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
| Technical Information | Serves NFR05 and NFR11; the export is what makes the data ownership criterion real. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.5.4.1 F12 Mobile application build

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | F12 Mobile application build |
| Code of Accounts | 1.5.4.1 |
| Responsible Person | MOB1 |
| Description of Work | Build the Android and iOS application from one cross-platform codebase against the design from 1.3.1.5 and the API contract from 1.3.1.3: for a parent the child schedule, attendance and score history, tuition balance and invoices, messages, make-up request, transfer confirmation, evaluation, and re-enrollment request; for a teacher today's sessions and rosters, attendance marking while online, score entry, the teaching-hour sheet, and class announcements. |
| Assumptions and Constraints | <mark>2.5 person-months of mobile developer effort between mobilisation after M2 and M5</mark>; staff functions stay on the web and no function is application-only. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Application alpha at the iteration 1 demo<br>2. Feature complete at the iteration 2 review |
| Due Dates | <mark>Mon 19 October 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.4.1-A1 | Parent journeys against the API contract | MOB1 | 110 | 122,500 | 13,475,000 | | | | 13,475,000 |
| 1.5.4.1-A2 | Teacher journeys against the API contract | MOB1 | 90 | 122,500 | 11,025,000 | | | | 11,025,000 |
| 1.5.4.1-A3 | Offline and degraded-state behaviour and last-synced view | MOB1 | 40 | 122,500 | 4,900,000 | | | | 4,900,000 |
| 1.5.4.1-A4 | Platform build, signing, and internal distribution | MOB1 | 40 | 122,500 | 4,900,000 | | | | 4,900,000 |
| | **Work package total** | | **280** | | **34,300,000** | | | **0** | **34,300,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every F12 function within three taps; no personal data cached unencrypted on the device. |
| Acceptance Criteria | Feature complete at M4 and submitted to both stores at M5. |
| Technical Information | Same API and same accounts as the web application; attendance marking and payment confirmation are disabled while offline. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.5.4.2 Push notification integration

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Push notification integration |
| Code of Accounts | 1.5.4.2 |
| Responsible Person | MOB1 |
| Description of Work | Add push as the third notification channel next to email and SMS, registering devices, delivering the F09 events, logging delivery state in the same F09 log, and falling back to SMS for tuition due and overdue messages four hours after a failed push. |
| Assumptions and Constraints | <mark>Push service on the free tier</mark>, per charter budget line 2; guardians without the application continue to receive SMS. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Push channel demonstrated at the iteration 2 review |
| Due Dates | <mark>Mon 30 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.4.2-A1 | Device registration and push delivery in the application | MOB1 | 40 | 122,500 | 4,900,000 | | | | 4,900,000 |
| 1.5.4.2-A2 | Server-side channel selection, logging, and SMS fallback timer | DEV3 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| | **Work package total** | | **60** | | **7,275,000** | | | **0** | **7,275,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Push delivery state is logged exactly as email and SMS are; the fallback timer is four hours. |
| Acceptance Criteria | A failed push produces an SMS within four hours in the test log. |
| Technical Information | This package is what holds the notification cost at the business case figure rather than the SMS-only figure. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.5.5.1 Iteration 2 code review and rework

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Iteration 2 code review and rework |
| Code of Accounts | 1.5.5.1 |
| Responsible Person | QA1 |
| Description of Work | Review the iteration 2 code against the design, the coding convention, and the money-path rules, and rework against the findings. The tuition and payroll code is reviewed by a developer who did not write it. |
| Assumptions and Constraints | The money path carries the tightest acceptance rule in the charter, so it is reviewed twice: once here and once in the security and system test. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Iteration 2 review findings closed |
| Due Dates | <mark>Mon 7 December 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.5.1-A1 | Cross-review of the tuition and payroll code | DEV1 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.5.5.1-A2 | Review against the test plan and the money-path rules | QA1 | 40 | 93,750 | 3,750,000 | | | | 3,750,000 |
| | **Work package total** | | **60** | | **6,125,000** | | | **0** | **6,125,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No author reviews their own code; no finding on the money path is left open. |
| Acceptance Criteria | Finding list closed before the M4 acceptance. |
| Technical Information |  |
| Agreement Information |  |

*Page 1 of 1*

#### 1.5.5.2 Iteration 2 unit and integration testing

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Iteration 2 unit and integration testing |
| Code of Accounts | 1.5.5.2 |
| Responsible Person | QA1 |
| Description of Work | Execute unit and integration testing across F06 to F12 including their exception cases, on web and on both mobile platforms, log defects, and retest after fixes. |
| Assumptions and Constraints | The mobile application is tested on real devices, using the two test phones bought in 1.6.1.2. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Iteration 2 test cycle complete |
| Due Dates | <mark>Mon 30 November 2026 to Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.5.2-A1 | Unit and integration test execution across F06 to F12 | QA1 | 60 | 93,750 | 5,625,000 | | | | 5,625,000 |
| 1.5.5.2-A2 | Exception case testing including the money-path cases | QA1 | 24 | 93,750 | 2,250,000 | | | | 2,250,000 |
| 1.5.5.2-A3 | Defect logging and retest | QA1 | 16 | 93,750 | 1,500,000 | | | | 1,500,000 |
| | **Work package total** | | **100** | | **9,375,000** | | | **0** | **9,375,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No open defect of any severity in the tuition, payment, or teaching-hour path. |
| Acceptance Criteria | Feature-complete criteria met at M4. |
| Technical Information | Results feed the defect log in 1.6.2.2. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.5.5.3 Iteration 2 acceptance, feature complete

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Iteration 2 acceptance, feature complete |
| Code of Accounts | 1.5.5.3 |
| Responsible Person | PM |
| Description of Work | Demonstrate F06 to F12 to the customer, record the acceptance decision, and declare the system feature complete. |
| Assumptions and Constraints | The M4 milestone releases the 30% payment tranche against the signed acceptance record. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. M4 iteration 2 accepted, feature complete, F06 to F12<br>2. D4 delivered |
| Due Dates | <mark>Fri 11 December 2026; M4 on Fri 11 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.5.5.3-A1 | Demo preparation and delivery to the customer | PM | 30 | 162,500 | 4,875,000 | | | | 4,875,000 |
| 1.5.5.3-A2 | Feature-complete walkthrough against F01 to F12 | QA1 | 20 | 93,750 | 1,875,000 | | | | 1,875,000 |
| | **Work package total** | | **50** | | **6,750,000** | | | **0** | **6,750,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Feature complete means every function of F01 to F12 is present and testable, not that every defect is closed. |
| Acceptance Criteria | Signed acceptance record of D4. |
| Technical Information |  |
| Agreement Information | Acceptance record releases the M4 payment tranche. |

*Page 1 of 1*

### Phase 1.6 Quality Assurance and Test

#### 1.6.1.1 System test execution, web

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | System test execution, web |
| Code of Accounts | 1.6.1.1 |
| Responsible Person | QA1 |
| Description of Work | Execute the system test on the web application across F01 to F12 and the fourteen exception cases, end to end on staging with migrated sample data, against the test plan accepted at M2. |
| Assumptions and Constraints | System test starts once the system is feature complete at M4 and runs against the staging environment, not against developer machines. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Web system test cycle complete |
| Due Dates | <mark>Mon 14 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.1.1-A1 | End-to-end scenario execution across F01 to F12 | QA1 | 64 | 93,750 | 6,000,000 | | | | 6,000,000 |
| 1.6.1.1-A2 | Exception and failure behaviour execution | QA1 | 36 | 93,750 | 3,375,000 | | | | 3,375,000 |
| | **Work package total** | | **100** | | **9,375,000** | | | **0** | **9,375,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every one of the fourteen exception cases is executed, not only the functions. |
| Acceptance Criteria | Exit criteria of the test plan met for the web application. |
| Technical Information | Covers NFR09 for the latest two versions of Chrome, Edge, and Firefox. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.6.1.2 System test execution, Android and iOS

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | System test execution, Android and iOS |
| Code of Accounts | 1.6.1.2 |
| Responsible Person | QA1 |
| Description of Work | Execute the system test on the mobile application on real Android and iOS devices, covering the parent and teacher journeys, push delivery, the SMS fallback, and the offline and degraded states. |
| Assumptions and Constraints | Two test phones, one Android and one iOS, are bought for this from charter budget line 3. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Mobile system test cycle complete |
| Due Dates | <mark>Mon 14 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.1.2-A1 | Parent and teacher journey execution on both platforms | QA1 | 40 | 93,750 | 3,750,000 | | | | 3,750,000 |
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

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Performance and capacity test |
| Code of Accounts | 1.6.1.3 |
| Responsible Person | QA1 |
| Description of Work | Load test the staff screens at the stated concurrency, the parent portal at its concurrency, the term report, and the application screens, at the full data volume of the capacity criterion, and report the 95th percentile against each threshold. |
| Assumptions and Constraints | <mark>52 concurrent staff users, 300 concurrent parent sessions, 5,000 student records, 200 classes per term, and 3 years of history</mark>, all from the charter acceptance criteria. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Performance and capacity report issued |
| Due Dates | <mark>Mon 14 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.1.3-A1 | Load and capacity test execution and reporting | QA1 | 40 | 93,750 | 3,750,000 | | | | 3,750,000 |
| 1.6.1.3-A2 | Test data generation at the stated volumes | DEV3 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| | **Work package total** | | **60** | | **6,125,000** | | | **0** | **6,125,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criteria A02 and A03; the report states the 95th percentile, not the average. |
| Acceptance Criteria | Every threshold met, or a fix agreed before UAT entry. |
| Technical Information | Serves NFR02 and NFR03 of the traceability matrix. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.6.1.4 Security test

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Security test |
| Code of Accounts | 1.6.1.4 |
| Responsible Person | QA1 |
| Description of Work | Test the authorisation of every endpoint against the role matrix, check that no password is stored or recoverable in readable form, confirm HTTPS-only transport, check consent recording and token expiry, and confirm that no personal data is cached unencrypted on the device. |
| Assumptions and Constraints | Testing is against the security design from 1.3.1.1; a finding here blocks UAT entry rather than being carried into warranty. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Security test report issued |
| Due Dates | <mark>Mon 14 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.1.4-A1 | Authorisation and transport testing | QA1 | 20 | 93,750 | 1,875,000 | | | | 1,875,000 |
| 1.6.1.4-A2 | Credential, consent, token, and device-storage checks | DEV3 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| | **Work package total** | | **40** | | **4,250,000** | | | **0** | **4,250,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criterion A04; no unauthorised access path found. |
| Acceptance Criteria | Report reviewed and accepted before UAT entry at M5. |
| Technical Information | Serves NFR04; the audit log built in 1.5.3.2 is checked here for tamper resistance. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.6.1.5 Defect fixing and regression

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Defect fixing and regression |
| Code of Accounts | 1.6.1.5 |
| Responsible Person | DEV1 |
| Description of Work | Fix the defects raised by the system, performance, and security tests, and run the regression cycle after each fix batch. Each defect is fixed by the developer who owns that area, and the fix is retested by the QA engineer, never signed off by the person who wrote it. |
| Assumptions and Constraints | This package carries the fix effort for the whole system test phase; it is sized from the defect rate assumed in the test plan and is the first thing re-estimated if the rate differs. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. No open Critical or High defect at UAT entry |
| Due Dates | <mark>Mon 14 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.1.5-A1 | Defect fixing in scheduling, reporting, and administration | DEV1 | 80 | 118,750 | 9,500,000 | | | | 9,500,000 |
| 1.6.1.5-A2 | Defect fixing in enrollment, tuition, and payroll | DEV2 | 80 | 118,750 | 9,500,000 | | | | 9,500,000 |
| 1.6.1.5-A3 | Defect fixing in catalog, assessment, notification, and platform | DEV3 | 60 | 118,750 | 7,125,000 | | | | 7,125,000 |
| 1.6.1.5-A4 | Regression cycle and fix verification | QA1 | 20 | 93,750 | 1,875,000 | | | | 1,875,000 |
| | **Work package total** | | **240** | | **28,000,000** | | | **0** | **28,000,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | No open Critical or High defect, and no open defect of any severity in the tuition, payment, or teaching-hour path. |
| Acceptance Criteria | UAT entry criteria met at M5. |
| Technical Information | The regression suite built here is handed over with the source code in 1.8.3.1. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.6.2.1 Test cases and UAT test set

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Test cases and UAT test set |
| Code of Accounts | 1.6.2.1 |
| Responsible Person | QA1 |
| Description of Work | Write the test cases from the requirement baseline and the exception catalogue, and agree the user acceptance test set with the business owners, which is the set acceptance is measured against. |
| Assumptions and Constraints | The charter requires the UAT test set to be agreed and signed at M5; acceptance is measured against that set and nothing else. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. UAT test set agreed and signed at M5 |
| Due Dates | <mark>Mon 19 October 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.2.1-A1 | Test case authoring from the requirement baseline | QA1 | 24 | 93,750 | 2,250,000 | | | | 2,250,000 |
| 1.6.2.1-A2 | UAT test set agreement with the business owners | QA1 | 16 | 93,750 | 1,500,000 | | | | 1,500,000 |
| | **Work package total** | | **40** | | **3,750,000** | | | **0** | **3,750,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every function and every exception case has at least one test case. |
| Acceptance Criteria | Test set signed by the Academic Manager, the Accountant, and the sponsor. |
| Technical Information | This set is the measure for acceptance criterion A01 and the 99% threshold. |
| Agreement Information | Signed test set is attached to the acceptance record of D5. |

*Page 1 of 1*

#### 1.6.2.2 Defect log and test summary report

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Defect log and test summary report |
| Code of Accounts | 1.6.2.2 |
| Responsible Person | QA1 |
| Description of Work | Maintain the defect log through both iterations and the system test, and produce the test summary report that completes the test documentation deliverable. |
| Assumptions and Constraints | The defect log is one log for the whole project, not one per phase, so that trends are visible. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. D5 test documentation complete |
| Due Dates | <mark>Mon 19 October 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.2.2-A1 | Defect log maintenance and trend reporting | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| 1.6.2.2-A2 | Test summary report | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| | **Work package total** | | **16** | | **1,500,000** | | | **0** | **1,500,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Every defect carries a severity, an owner, a state, and a fix or an agreed fix date. |
| Acceptance Criteria | Signed acceptance record of D5. |
| Technical Information | Open defects at closeout are listed as known issues in the closeout report. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.6.2.3 UAT entry criteria review

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | UAT entry criteria review |
| Code of Accounts | 1.6.2.3 |
| Responsible Person | PM |
| Description of Work | Review the system test, performance, capacity, and security results against the UAT entry criteria of the test plan, confirm the store submission has been made, and decide whether UAT starts. |
| Assumptions and Constraints | Entering UAT with open Critical or High defects would move the failure into the customer's own acceptance window, so this is a gate rather than a review. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. M5 system test complete on web, Android, and iOS; UAT entry criteria met; application submitted to both stores |
| Due Dates | <mark>Fri 18 December 2026; M5 on Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.6.2.3-A1 | Entry criteria review and go decision | PM | 20 | 162,500 | 3,250,000 | | | | 3,250,000 |
| 1.6.2.3-A2 | Evidence pack for the entry decision | QA1 | 4 | 93,750 | 375,000 | | | | 375,000 |
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

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Source data analysis and cleansing rules |
| Code of Accounts | 1.7.1.1 |
| Responsible Person | DEV1 |
| Description of Work | Analyse the center's Excel workbooks and paper registers for the two most recent terms, assess data quality, and write the cleansing and mapping rules that the migration scripts implement. |
| Assumptions and Constraints | Migration is limited to the two most recent terms; cleaning the source data is the center's responsibility, per the charter exclusions, and is done before M5. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Data quality assessed at M1<br>2. Cleansing and mapping rules agreed |
| Due Dates | <mark>Mon 28 September 2026 to Fri 18 December 2026</mark> |

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

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Migration scripts and trial run |
| Code of Accounts | 1.7.1.2 |
| Responsible Person | DEV1 |
| Description of Work | Build the migration scripts, run a full trial migration into staging, and reconcile the trial result against the source files record by record so that the production run is a repeat of a proven procedure rather than a first attempt. |
| Assumptions and Constraints | External data-entry support of 12,000,000 VND from charter budget line 4 covers the records the center cannot supply in machine-readable form. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Trial migration reconciled on staging |
| Due Dates | <mark>Mon 21 December 2026 to Thu 31 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.7.1.2-A1 | Migration script development | DEV1 | 40 | 118,750 | 4,750,000 | | | | 4,750,000 |
| 1.7.1.2-A2 | Trial run into staging and defect correction | DEV1 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.7.1.2-A3 | Trial reconciliation review | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| 1.7.1.2-A4 | External data-entry support for non-machine-readable records | | | | | 1 | 12,000,000 | 12,000,000 | 12,000,000 |
| | **Work package total** | | **68** | | **7,875,000** | | | **12,000,000** | **19,875,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The trial produces the same reconciliation report the production run will produce. |
| Acceptance Criteria | Trial differences explained or corrected before the production run. |
| Technical Information | Uses the key design from 1.3.1.2, which is what makes record-by-record reconciliation possible. |
| Agreement Information | Data-entry support engaged under a short-form supplier agreement. |

*Page 1 of 1*

#### 1.7.1.3 Production migration and reconciliation report

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Production migration and reconciliation report |
| Code of Accounts | 1.7.1.3 |
| Responsible Person | DEV1 |
| Description of Work | Run the migration into production and produce the reconciliation report listing every difference between the migrated data and the source files. |
| Assumptions and Constraints | The production run happens in the go-live window and is rehearsed by the trial run; a failed run falls back to the spreadsheets, which stay in parallel for two weeks. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
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

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Accountant acceptance of the reconciliation |
| Code of Accounts | 1.7.1.4 |
| Responsible Person | PM |
| Description of Work | Obtain the Accountant's written acceptance of the reconciliation report, including any difference the center chooses to accept rather than correct, which is the charter's condition for go-live. |
| Assumptions and Constraints | Go-live requires this acceptance; without it the migration is not complete regardless of what the scripts did. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Reconciliation accepted in writing |
| Due Dates | <mark>Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.7.1.4-A1 | Reconciliation walkthrough and written acceptance | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| 1.7.1.4-A2 | Acceptance evidence filing | QA1 | 4 | 93,750 | 375,000 | | | | 375,000 |
| | **Work package total** | | **12** | | **1,675,000** | | | **0** | **1,675,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance is written, and names the differences accepted rather than accepting them silently. |
| Acceptance Criteria | Signed acceptance record of D6. |
| Technical Information |  |
| Agreement Information | Acceptance record filed with the supplier contract. |

*Page 1 of 1*

### Phase 1.8 Deployment and Handover

#### 1.8.1.1 Cloud server and staging provisioning

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Cloud server and staging provisioning |
| Code of Accounts | 1.8.1.1 |
| Responsible Person | DEV3 |
| Description of Work | Provision the production cloud virtual server and the staging environment, the domain, and the SSL certificate, and harden both to the security design. |
| Assumptions and Constraints | <mark>Cloud server and staging for 12 months at 24,000,000 VND, domain and SSL at 2,000,000 VND</mark>, from charter budget line 2. Subscriptions beyond 12 months are a charter exclusion and become the center's cost. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
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

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Backup configuration and restore drill |
| Code of Accounts | 1.8.1.2 |
| Responsible Person | DEV3 |
| Description of Work | Configure the nightly backup to the recovery point objective, and demonstrate a restore inside the recovery time objective, once during UAT and once during the warranty month. |
| Assumptions and Constraints | Recovery point objective 24 hours and recovery time objective 4 hours, from acceptance criterion A06. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Restore demonstrated during UAT<br>2. Restore demonstrated during warranty |
| Due Dates | <mark>Mon 21 December 2026 to Tue 5 January 2027, repeated in the warranty month</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.8.1.2-A1 | Backup configuration and schedule | DEV3 | 16 | 118,750 | 1,900,000 | | | | 1,900,000 |
| 1.8.1.2-A2 | Restore drill witnessed by the System Administrator | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| | **Work package total** | | **24** | | **2,650,000** | | | **0** | **2,650,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | A restore from a backup no more than 24 hours old completes inside 4 hours. |
| Acceptance Criteria | Both drills recorded and signed by the System Administrator. |
| Technical Information | Serves NFR06; the drill procedure is part of the administrator guide in 1.8.2.1. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.8.1.3 Production deployment and go-live

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Production deployment and go-live |
| Code of Accounts | 1.8.1.3 |
| Responsible Person | DEV3 |
| Description of Work | Deploy the accepted release to production, run the pilot of F01 to F06 at one branch for the two weeks before go-live, switch all three branches over, and keep the spreadsheets running in parallel for two weeks afterwards. |
| Assumptions and Constraints | Go-live support of 8,000,000 VND from charter budget line 4 covers the switchover weekend and on-site presence at the three branches. Go-live falls on a Tuesday so that live operation begins with two fully staffed working days. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Pilot at one branch complete<br>2. M6 go-live<br>3. D7 production deployment delivered |
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
| Technical Information | This package carries the charter responses to risks R10 and R8. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.8.2.1 User, administrator, and deployment documentation

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | User, administrator, and deployment documentation |
| Code of Accounts | 1.8.2.1 |
| Responsible Person | DEV2 |
| Description of Work | Write the Vietnamese user manual for the staff roles, the administrator guide covering configuration, backup, restore, and the audit log, and the deployment guide that lets a third party deploy the system from the guide alone. |
| Assumptions and Constraints | Documentation production of 10,000,000 VND from charter budget line 4 covers translation review, screenshots, and printing. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Documentation delivered as part of D8 |
| Due Dates | <mark>Mon 14 December 2026 to Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.8.2.1-A1 | User manual for the staff roles | DEV2 | 10 | 118,750 | 1,187,500 | | | | 1,187,500 |
| 1.8.2.1-A2 | Administrator and deployment guide | DEV2 | 6 | 118,750 | 712,500 | | | | 712,500 |
| 1.8.2.1-A3 | Documentation review and translation check | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| 1.8.2.1-A4 | Documentation production, translation review, and printing | | | | | 1 | 10,000,000 | 10,000,000 | 10,000,000 |
| | **Work package total** | | **32** | | **4,500,000** | | | **10,000,000** | **14,500,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criterion A10: a third party deploys to staging following only the guide. |
| Acceptance Criteria | System Administrator deploys to staging from the guide without help. |
| Technical Information | The paper fallback procedure from 1.8.2.3 is part of the user manual. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.8.2.2 Staff training delivery and training record

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Staff training delivery and training record |
| Code of Accounts | 1.8.2.2 |
| Responsible Person | PM |
| Description of Work | Train the center's staff by role in half-day sessions at the three branches, and keep the training record that the stakeholder satisfaction objective is measured against. |
| Assumptions and Constraints | <mark>52 staff users, being 35 teachers and 17 administrative staff</mark>; training delivery of 12,000,000 VND and travel to the three branches of 3,000,000 VND, from charter budget lines 4 and 3. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Training complete at all three branches<br>2. D8 delivered |
| Due Dates | <mark>Mon 21 December 2026 to Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.8.2.2-A1 | Training delivery by role at the three branches | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| 1.8.2.2-A2 | Training delivery, venue, and materials | | | | | 1 | 12,000,000 | 12,000,000 | 12,000,000 |
| 1.8.2.2-A3 | Travel to the three branches | | | | | 1 | 3,000,000 | 3,000,000 | 3,000,000 |
| | **Work package total** | | **16** | | **2,600,000** | | | **15,000,000** | **17,600,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | A staff member performs their daily tasks after half a day of training, per acceptance criterion A08. |
| Acceptance Criteria | Signed acceptance record of D8, with the training record attached. |
| Technical Information | Target is <mark>80% of staff trained and active in the first month, being 90% of administrative users and 75% of teachers</mark>. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.8.2.3 Paper fallback procedure and rehearsal

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Paper fallback procedure and rehearsal |
| Code of Accounts | 1.8.2.3 |
| Responsible Person | PM |
| Description of Work | Write the paper procedure for attendance and receipts when the system is unavailable, write the catch-up procedure for entering that data afterwards, train it, and rehearse it once at one branch before go-live. |
| Assumptions and Constraints | Late entry is stamped as late and does not corrupt the payroll or the debt figures, which is what makes the fallback safe to use. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Fallback rehearsed before go-live |
| Due Dates | <mark>Mon 21 December 2026 to Fri 2 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.8.2.3-A1 | Fallback and catch-up procedure authoring and training | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| 1.8.2.3-A2 | Rehearsal at one branch and reconciliation of the catch-up entry | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| | **Work package total** | | **16** | | **2,050,000** | | | **0** | **2,050,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criterion A07; the rehearsal record is signed and the catch-up entry reconciles. |
| Acceptance Criteria | Rehearsal complete before M6. |
| Technical Information | The procedure is part of the user manual, not a separate sheet that gets lost. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.8.3.1 Source code, database scripts, and technical documentation handover

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Source code, database scripts, and technical documentation handover |
| Code of Accounts | 1.8.3.1 |
| Responsible Person | DEV2 |
| Description of Work | Hand over the source code, the database scripts, the schema documentation, the API documentation, the regression suite, the coding convention, and the repository access, so that the center is not locked to the supplier after the warranty. |
| Assumptions and Constraints | Handover is to the center's System Administrator and is complete at go-live, not at closeout. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. D9 handover complete |
| Due Dates | <mark>Mon 28 December 2026 to Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.8.3.1-A1 | Handover pack assembly and repository transfer | DEV2 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.8.3.1-A2 | Handover walkthrough with the System Administrator | PM | 4 | 162,500 | 650,000 | | | | 650,000 |
| | **Work package total** | | **24** | | **3,025,000** | | | **0** | **3,025,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Handover checklist complete; nothing on it is marked to follow. |
| Acceptance Criteria | Signed acceptance record of D9. |
| Technical Information | Signing keys for the mobile application are handed over separately in 1.9.1.1. |
| Agreement Information | Handover record filed with the supplier contract. |

*Page 1 of 1*

#### 1.8.3.2 User acceptance testing execution and sign-off

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | User acceptance testing execution and sign-off |
| Code of Accounts | 1.8.3.2 |
| Responsible Person | QA1 |
| Description of Work | Run user acceptance testing with the business owners against the test set agreed at M5, record the result per test case, and obtain the sign-off that gates go-live. |
| Assumptions and Constraints | Acceptance is measured against the agreed set: at least 99% of cases passed, the remainder defects that do not affect operation, each logged with an agreed fix date. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. UAT sign-off obtained<br>2. M6 UAT signed off, go-live and handover |
| Due Dates | <mark>Mon 21 December 2026 to Tue 5 January 2027; M6 on Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.8.3.2-A1 | UAT execution with the business owners | QA1 | 24 | 93,750 | 2,250,000 | | | | 2,250,000 |
| 1.8.3.2-A2 | Acceptance decision and sign-off with the sponsor | PM | 8 | 162,500 | 1,300,000 | | | | 1,300,000 |
| | **Work package total** | | **32** | | **3,550,000** | | | **0** | **3,550,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criterion A01; no open Critical or High defect and none of any severity in the money path. |
| Acceptance Criteria | Sponsor signs the acceptance record; a failed UAT puts the three charter options to the sponsor within two working days. |
| Technical Information | This is the Validate Scope point of the project: deliverables verified by Control Quality are accepted here. |
| Agreement Information | Sign-off releases the final 25% payment tranche. |

*Page 1 of 1*

### Phase 1.9 Mobile Application Release

#### 1.9.1.1 Store accounts and signing keys

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Store accounts and signing keys |
| Code of Accounts | 1.9.1.1 |
| Responsible Person | MOB1 |
| Description of Work | Open the Google Play and Apple Developer accounts in the center's name, configure the signing keys and their custody, and hand the credentials to the center's System Administrator. |
| Assumptions and Constraints | <mark>Apple Developer 2,600,000 VND a year and Google Play 700,000 VND once</mark>, from charter budget line 2. Apple's enrolment of a legal entity can take up to <mark>four weeks</mark>, so the accounts are opened at M1. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Store accounts active<br>2. Signing keys in the center's custody |
| Due Dates | <mark>Fri 2 October 2026 to Fri 30 October 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.9.1.1-A1 | Store account enrolment in the center's name | MOB1 | 10 | 122,500 | 1,225,000 | | | | 1,225,000 |
| 1.9.1.1-A2 | Signing key generation, custody, and handover | MOB1 | 6 | 122,500 | 735,000 | | | | 735,000 |
| 1.9.1.1-A3 | Enrolment coordination with the center | PM | 6 | 162,500 | 975,000 | | | | 975,000 |
| 1.9.1.1-A4 | Apple Developer and Google Play account fees | | | | | 1 | 3,300,000 | 3,300,000 | 3,300,000 |
| | **Work package total** | | **22** | | **2,935,000** | | | **3,300,000** | **6,235,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Accounts are in the center's name, so the applications survive the end of the supplier relationship. |
| Acceptance Criteria | Credentials and keys accepted by the System Administrator. |
| Technical Information | Opening at M1 is the charter response to the enrolment half of risk R12. |
| Agreement Information | Store terms accepted by the center as the account holder. |

*Page 1 of 1*

#### 1.9.1.2 Store listings and release notes

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Store listings and release notes |
| Code of Accounts | 1.9.1.2 |
| Responsible Person | MOB1 |
| Description of Work | Prepare the Vietnamese store listings, screenshots, privacy declarations, and release notes for both stores, including the data-collection disclosures the stores require. |
| Assumptions and Constraints | The privacy declarations must match the personal-data design from 1.3.1.1; a mismatch is a common cause of store rejection. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Listings ready for submission |
| Due Dates | <mark>Mon 7 December 2026 to Fri 18 December 2026</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.9.1.2-A1 | Listing copy, screenshots, and privacy declarations | MOB1 | 16 | 122,500 | 1,960,000 | | | | 1,960,000 |
| 1.9.1.2-A2 | Release notes and versioning | MOB1 | 8 | 122,500 | 980,000 | | | | 980,000 |
| 1.9.1.2-A3 | Listing review with the Center Director | PM | 4 | 162,500 | 650,000 | | | | 650,000 |
| | **Work package total** | | **28** | | **3,590,000** | | | **0** | **3,590,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Declarations match what the application actually collects. |
| Acceptance Criteria | Director approves the listings before submission. |
| Technical Information |  |
| Agreement Information |  |

*Page 1 of 1*

#### 1.9.1.3 Store submission and review response

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Store submission and review response |
| Code of Accounts | 1.9.1.3 |
| Responsible Person | MOB1 |
| Description of Work | Submit the application to Google Play and the App Store at M5 and answer the store review, so that the application is live in both stores at go-live. |
| Assumptions and Constraints | <mark>A store review takes at most one week; the mobile developer's engagement closes after the first review response rather than exactly at M5.</mark> Go-live does not depend on the application: a store slip of up to two weeks after M6 is absorbed without moving M6. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Application submitted at M5<br>2. Application live in both stores at M6<br>3. D11 delivered |
| Due Dates | <mark>Fri 18 December 2026 to Tue 5 January 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.9.1.3-A1 | Submission to both stores | MOB1 | 16 | 122,500 | 1,960,000 | | | | 1,960,000 |
| 1.9.1.3-A2 | Review response and resubmission if required | MOB1 | 24 | 122,500 | 2,940,000 | | | | 2,940,000 |
| | **Work package total** | | **40** | | **4,900,000** | | | **0** | **4,900,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Acceptance criterion A12; every F12 function within three taps in the published build. |
| Acceptance Criteria | Signed acceptance record of D11. |
| Technical Information | If a store rejects or delays, go-live proceeds on the web and the guardian onboarding message is sent when the application is live. |
| Agreement Information | Applications published under the center's store accounts. |

*Page 1 of 1*

### Phase 1.10 Warranty and Closeout

#### 1.10.1.1 First warranty month support

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | First warranty month support |
| Code of Accounts | 1.10.1.1 |
| Responsible Person | PM |
| Description of Work | Deliver the first warranty month with the full team inside the project: correct defects against the accepted baseline to the charter response targets, run the second restore drill, support the parallel running of the spreadsheets for the first two weeks, and report the overdue percentage to the Director. |
| Assumptions and Constraints | The warranty runs six months from go-live on the web application and the mobile application alike; the first month is inside the project and is delivered by the full team. It is not six months of free change requests: enhancements are recorded for a later project. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Parallel running ended after two weeks<br>2. Second restore drill complete<br>3. First warranty month complete |
| Due Dates | <mark>Wed 6 January 2027 to Fri 5 February 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.10.1.1-A1 | Defect correction in scheduling, reporting, and administration | DEV1 | 140 | 118,750 | 16,625,000 | | | | 16,625,000 |
| 1.10.1.1-A2 | Defect correction in enrollment, tuition, and payroll | DEV2 | 140 | 118,750 | 16,625,000 | | | | 16,625,000 |
| 1.10.1.1-A3 | Defect correction in catalog, assessment, notification, and the application | DEV3 | 100 | 118,750 | 11,875,000 | | | | 11,875,000 |
| 1.10.1.1-A4 | Warranty coordination, response tracking, and Director reporting | PM | 24 | 162,500 | 3,900,000 | | | | 3,900,000 |
| 1.10.1.1-A5 | Retest of warranty fixes | QA1 | 12 | 93,750 | 1,125,000 | | | | 1,125,000 |
| | **Work package total** | | **416** | | **50,150,000** | | | **0** | **50,150,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Critical responded within 2 working hours and worked around within 1 working day; High within 1 and 5 working days; the money path carries no open defect. |
| Acceptance Criteria | A Critical or High defect still open at the end of the month blocks closeout. |
| Technical Information | The overdue percentage reported here is the first measurement of the business case benefit, and names the Accountant as benefit owner per risk R11. |
| Agreement Information | Warranty obligation of the supplier contract, months 1 to 6 from go-live. |

*Page 1 of 1*

#### 1.10.1.2 Warranty handover to the support desk

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Warranty handover to the support desk |
| Code of Accounts | 1.10.1.2 |
| Responsible Person | PM |
| Description of Work | Hand warranty months 2 to 6 to the supplier's support desk with the defect history, the known issues, the response targets, and the escalation path, and fund that period from charter budget line 5. |
| Assumptions and Constraints | <mark>Months 2 to 6 are delivered after closeout at about 0.35 full-time equivalent, funded by charter budget line 5 at 35,000,000 VND, running to 5 July 2027.</mark> <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. Warranty handover accepted by the support desk<br>2. Warranty runs to 5 July 2027 |
| Due Dates | <mark>Mon 1 February 2027 to Fri 5 February 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.10.1.2-A1 | Handover pack, known issues, and escalation path | PM | 16 | 162,500 | 2,600,000 | | | | 2,600,000 |
| 1.10.1.2-A2 | Support desk briefing and system walkthrough | DEV3 | 20 | 118,750 | 2,375,000 | | | | 2,375,000 |
| 1.10.1.2-A3 | Known-issue list verification | QA1 | 8 | 93,750 | 750,000 | | | | 750,000 |
| 1.10.1.2-A4 | Warranty support, months 2 to 6 after go-live | | | | | 1 | 35,000,000 | 35,000,000 | 35,000,000 |
| | **Work package total** | | **44** | | **5,725,000** | | | **35,000,000** | **40,725,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The same severity definitions and response targets apply after closeout as during the project. |
| Acceptance Criteria | Support desk accepts the handover before closeout; a Critical or High open at the end of month 6 is reported to the sponsor with a fix date. |
| Technical Information |  |
| Agreement Information | Warranty terms of the supplier contract, months 2 to 6. |

*Page 1 of 1*

#### 1.10.2.1 Closeout report and lessons learned

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Closeout report and lessons learned |
| Code of Accounts | 1.10.2.1 |
| Responsible Person | PM |
| Description of Work | Write the closeout report covering scope delivered against D1 to D11, cost against the 700,000,000 VND baseline, reserve use, the final risk position, the measured overdue percentage, the user satisfaction survey, and the lessons learned. |
| Assumptions and Constraints | The report states the actual overdue percentage rather than the target, which is the charter's own test of whether the benefit appeared. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. D10 closeout report and lessons learned delivered |
| Due Dates | <mark>Mon 25 January 2027 to Fri 5 February 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.10.2.1-A1 | Closeout report and lessons learned | PM | 20 | 162,500 | 3,250,000 | | | | 3,250,000 |
| | **Work package total** | | **20** | | **3,250,000** | | | **0** | **3,250,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | The report states what was not achieved as plainly as what was. |
| Acceptance Criteria | Sponsor accepts D10 at the closeout meeting. |
| Technical Information | Known issues open at closeout are listed here with their agreed fix dates. |
| Agreement Information |  |

*Page 1 of 1*

#### 1.10.2.2 Final acceptance and project close

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 23 September 2026

| Field | Content |
| --- | --- |
| Work Package Name | Final acceptance and project close |
| Code of Accounts | 1.10.2.2 |
| Responsible Person | PM |
| Description of Work | Hold the closeout meeting, obtain final acceptance, close the contract administratively, and end the project. |
| Assumptions and Constraints | The project ends at the closeout meeting after the first warranty month; warranty months 2 to 6 continue as a funded obligation after the project has closed. <mark>The hours, the money, and the dates on this sheet are a first-pass estimate and are re-baselined at M1; the totals they roll up to are the charter figures.</mark> |
| Milestones | 1. M7 first warranty month complete, warranty handover, project closeout |
| Due Dates | <mark>Fri 5 February 2027; M7 on Fri 5 February 2027</mark> |

| ID | Activity | Resource | Labor Hours | Labor Rate | Labor Total | Material Units | Material Cost | Material Total | Total Cost |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.10.2.2-A1 | Closeout meeting and final acceptance | PM | 10 | 162,500 | 1,625,000 | | | | 1,625,000 |
| | **Work package total** | | **10** | | **1,625,000** | | | **0** | **1,625,000** |

| Field | Content |
| --- | --- |
| Quality Requirements | Final acceptance is signed; nothing is left as an informal understanding. |
| Acceptance Criteria | Signed final acceptance record closing D1 to D11. |
| Technical Information | Operating and hosting the system is the center's responsibility from handover. |
| Agreement Information | Contract closed administratively; the warranty obligation survives closure. |

*Page 1 of 1*
