# Learning Center Management Software

## Requirement Specification and Project Charter

**Project:** Development and Deployment of a Learning Center Management Software
**Budget:** 700,000,000 VND (700 million VND)
**Duration:** 5 months — 14 September 2026 to 5 February 2027 (144 days, 20.6 weeks)
**Team:** 5 full-time staff — 1 project manager / business analyst, 3 developers, 1 QA engineer
**Customer:** Đỗ Thị Bích Ngọc, owner and Director of the learning center
**Date prepared:** 2 September 2026

**How this document is organised.** Both parts follow forms from *A Project Manager's Book of Forms*, 3rd edition.

- **Part 1** answers point 1 of the assignment and follows form **2.8 Project Scope Statement** (pages 58–59 of the PDF), which is the book's free-text form for describing a project's scope: scope description, deliverables, acceptance criteria, exclusions, constraints, assumptions. The function list and its per-function descriptions sit inside the scope description, and the measurable non-functional targets sit inside the acceptance criteria, where the form expects them.
- **Part 2** answers point 2 and follows the element list of **Table 1.1 Elements of a Project Charter** (section 1.1, pages 13–15), covering all fourteen elements in the order the book gives them.

Every invented figure is collected in **1.6 Project Assumptions** rather than being scattered, so that filling the printed form (point 3) is a matter of copying from one place.

---

## Part 1 — Requirement Specification

*Form 2.8, Project Scope Statement*

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 2 September 2026

### 1.1 Project Scope Description

#### 1.1.1 The problem

The customer owns a private after-school learning center with about 1,200 active students, 35 teachers, and 3 branches in one city. It teaches English, mathematics, and IT skills in fixed-length courses of 24 to 48 sessions.

The center runs today on paper registers, Excel workbooks, and a group-chat channel. Enrollment lists live in one spreadsheet, attendance is taken on printed sheets and typed up later, tuition debt is tracked by the accountant in a separate workbook, and parents are informed by messages typed by hand. Four consequences follow, and they are the reason for the project:

- the same student data is entered two or three times, in different places, by different people;
- rooms and teachers are double-booked, because nobody can see the whole timetable at once;
- tuition is collected late, because there is no reliable list of who owes what;
- the Director cannot see revenue, class fill rate, or teaching load across the three branches without asking three people to build a spreadsheet.

#### 1.1.2 The product

A Vietnamese-language web application, used from a desktop browser by center staff and from a phone browser by teachers and parents, backed by one shared database that is the single source of truth for students, courses, classes, sessions, attendance, invoices, payments, and teaching hours.

The project delivers the software, deploys it on a cloud server, migrates the center's current data, trains the staff, and supports the center through one month of warranty after go-live.

#### 1.1.3 Users and roles

| Role | Who they are | What they do with the system |
| --- | --- | --- |
| Center Director | Owner and project sponsor | Dashboards, revenue and enrollment reports, approvals |
| Academic Manager | Runs the teaching operation | Course catalog, opening classes, scheduling, teacher assignment, assessment |
| Front-desk / Admissions staff | Reception counter at each branch | Student profiles, enrollment, invoices, recording payments, parent enquiries |
| Teacher | Teaching staff | Class roster, attendance, scores, own teaching-hour sheet |
| Accountant | Finance | Debt tracking, payment confirmation, teaching-hour payroll, financial reports |
| Student / Parent | End customer | Own schedule, attendance and score history, tuition balance, notifications |
| System Administrator | The center's IT staff | Accounts, roles, configuration, backup, audit log |

#### 1.1.4 Functions

| ID | Function | Primary actor | Description |
| --- | --- | --- | --- |
| F01 | Authentication and access control | System Administrator | Creates accounts, authenticates users by username and password, resets passwords, times out idle sessions, and enforces role-based permission so that each role sees only its own screens and its own data. Every account has exactly one role; staff accounts are additionally tied to one or more branches. |
| F02 | Student profile and enrollment | Front-desk staff | Records the student profile — personal data, guardian and contact details, how the student found the center, notes — and enrolls the student into an open class. Handles transfer between classes, reservation of a seat, and withdrawal with a refund calculation. Refuses an enrollment when the class is full or when the timetable collides with another class of the same student. |
| F03 | Course and curriculum catalog | Academic Manager | Defines what the center sells: course code, level, number of sessions, session length, standard tuition fee, prerequisite course, and the syllabus outline session by session. Courses are versioned, so that editing a course does not change the definition of classes that were already opened from it. |
| F04 | Class opening, scheduling, and assignment | Academic Manager | Opens a class from a course — branch, start date, weekly time slots, capacity — generates the whole session calendar from that, and assigns a room and a teacher to each session. Detects and blocks conflicts on room, on teacher, and on class time at the moment the class or session is created or moved, and recalculates the calendar when a session is postponed. |
| F05 | Attendance and make-up sessions | Teacher | Marks every student of a session present, absent with notice, absent without notice, or late, with an optional remark. Registers a make-up session in another class for an absent student, and shows the attendance rate per student and per class. |
| F06 | Tuition, invoicing, and debt tracking | Front-desk staff, Accountant | Generates the tuition invoice at enrollment from the course fee, applying the discount policies of the center — sibling, early payment, referral, promotion code — and installment plans. Records cash and bank-transfer payments against invoices, issues receipts, and maintains the outstanding balance and an aged debt list per student, per class, and per branch. |
| F07 | Teacher records and teaching-hour payroll | Accountant | Holds teacher profiles, qualifications, contract type, and pay rate per teaching hour by course level. Aggregates the sessions actually taught, taken from F05, into a monthly teaching-hour sheet per teacher, applies allowances and deductions, and exports the payroll figures to Excel. |
| F08 | Assessment and progress reports | Teacher | Records scores for the assessment items the course defines — quizzes, midterm, final, skill scores — and a comment per student. Computes the final result and pass or fail against the course rule, and produces a printable progress report per student and a result summary per class. |
| F09 | Notification to parents and teachers | Front-desk staff | Sends email and SMS from templates for the events that matter: enrollment confirmed, session reminder, absence alert, tuition due, tuition overdue, schedule changed, results published. Supports a manual send to a chosen group, a scheduled automatic send, and a log of every message with its delivery status. |
| F10 | Reports and management dashboard | Center Director | The management view: revenue and collection by period and branch, outstanding debt, new and retained student counts, class fill rate, teacher workload and teaching hours, attendance rate. Every report is filterable by period, branch, and course, and exports to Excel and PDF. |
| F11 | System administration and audit | System Administrator | Maintains the center's reference data and configuration — branches, rooms, terms, fee and discount policies, notification templates, holidays — triggers and restores backups, and keeps an audit log of every create, update, and delete on financial and student data, with the user and the timestamp. |

#### 1.1.5 Behaviour when things go wrong

The eleven functions above describe the system working normally. A learning center does not only work normally, and the cases below are part of the scope, not afterthoughts. They are specified here because a requirement list that describes only success is half a requirement list.

| Situation | Required behaviour |
| --- | --- |
| A teacher does not record attendance | The session is flagged *attendance missing* on the Academic Manager's daily exception list. Attendance can still be entered later, but a late entry is stamped as late with the name of whoever entered it, and a month containing missing attendance cannot be closed for payroll. |
| A teacher is absent on the day | The Academic Manager assigns a substitute or postpones the session. Teaching hours are credited to whoever actually taught, never to whoever was originally scheduled. Affected parents are notified automatically. |
| A class is cancelled after students have paid | One action applies the center's cancellation policy to every enrolled student, producing a refund proposal or a credit note on each balance, and records the reason. Nothing is deleted; the sessions are marked cancelled and keep their history. |
| A student withdraws mid-course | The refund is calculated from the sessions actually delivered. It is a proposal: it does not change the balance until the Accountant approves it. The seat is released. |
| A bank transfer cannot be matched to an invoice | The payment is held in an unmatched list. It is never guessed at and never discarded, and no balance moves until someone matches it. No overdue reminder is sent to a student who has an unmatched payment on file, so a parent who has already paid is never chased for the money. |
| A parent overpays or pays twice | The excess becomes a credit on the payer's account. Moving a credit between siblings needs the Accountant. Reversing a receipt is never a delete: it posts a reversing entry, and both entries stay in the audit log. |
| The SMS or email gateway fails | Every message carries a delivery state and, on failure, a reason. Failed messages are retried and then listed for manual action, and the administrator is alerted when gateway credit runs low. A notification that failed is never allowed to disappear quietly. |
| A teacher disputes the monthly teaching-hour sheet | The sheet moves through draft, confirmed by teacher, approved by Academic Manager, exported. Only approved sheets reach payroll, and the person who recorded the attendance is never the person who approves the sheet that pays for it. |
| The system is unavailable during teaching hours | The center falls back to a written paper procedure for attendance and receipts, and enters the data afterwards. Late entry is stamped as such and does not corrupt the payroll or debt figures. The fallback is part of the user manual and is rehearsed before go-live. |
| Migrated data does not reconcile with the Excel files | Migration produces a reconciliation report of every difference. Go-live requires the Accountant's written acceptance of that report, including any difference the center chooses to accept rather than correct. |

### 1.2 Project Deliverables

| # | Deliverable | Due at |
| --- | --- | --- |
| D1 | Requirement specification, approved and baselined | M1 |
| D2 | Design baseline: architecture, database schema, UI design | M2 |
| D3 | Iteration 1 release — F01 to F05 | M3 |
| D4 | Iteration 2 release — F06 to F11 | M4 |
| D5 | Test documentation: test plan, test cases, defect log, test summary report | M5 |
| D6 | Production data migrated and reconciled against the source files | M6 |
| D7 | Production deployment on the cloud server, with backup configured and a restore tested | M6 |
| D8 | User manual, administrator and deployment guide, trained staff with a training record | M6 |
| D9 | Source code, database scripts, and technical documentation handed over | M6 |
| D10 | Warranty period completed, closeout report and lessons learned | M7 |

### 1.3 Product Acceptance Criteria

The product is accepted when the functions of 1.1.4 and the behaviour of 1.1.5 pass user acceptance testing and the measurable criteria below are met. Each one is stated as a number with a threshold so that acceptance is a measurement rather than an opinion.

| ID | Category | Criterion |
| --- | --- | --- |
| A01 | Functional completeness | 100% of F01 to F11 accepted in UAT; at least 95% of UAT test cases passed; no open Critical or High defect; at most 5 open Medium defects, each with an agreed fix date, and none of them in the tuition, payment, or teaching-hour path |
| A02 | Performance | Staff screens respond within 3 seconds with 52 concurrent staff users; the parent portal responds within 3 seconds at 300 concurrent sessions; a report covering one term is produced within 10 seconds |
| A03 | Capacity | 5,000 student records, 200 classes per term, and 3 years of session history without redesign |
| A04 | Security | HTTPS only; passwords never stored or recoverable in readable form; every request authorised on the server; personal data handled in line with the Law on Personal Data Protection in force from 1 January 2026; notification consent recorded per guardian |
| A05 | Auditability | Every create, update, and delete on financial and student records written to an audit log that cannot be edited, kept for at least 3 years |
| A06 | Availability | 99% availability between 07:00 and 22:00, measured monthly; nightly backup with a recovery point objective of 24 hours and a recovery time objective of 4 hours; the restore demonstrated once during UAT and once during warranty |
| A07 | Degraded operation | The written paper fallback and its catch-up procedure exist, are trained, and are rehearsed once before go-live |
| A08 | Usability | Vietnamese interface; attendance, payment recording, and enrollment each reachable within 3 clicks of the home screen; a staff member can perform their daily tasks after half a day of training |
| A09 | Compatibility | The latest two versions of Chrome, Edge, and Firefox on desktop; usable layout on a tablet and on a phone for teacher and parent screens |
| A10 | Maintainability and handover | Coding convention applied; deployment guide and database schema documentation delivered with the source code |
| A11 | Data ownership | A complete export of the center's data in an open format, produced by the center's own administrator at any time without the supplier's involvement |

### 1.4 Project Exclusions

- **Native mobile applications** for iOS or Android. The web interface is responsive; there is no app-store deliverable.
- **Online teaching**: live video class, content authoring, quiz engine, streaming of e-learning material.
- **Automated payment**: no payment gateway, card capture, or e-wallet integration. The system records payments and reconciles bank-transfer references manually.
- **Accounting, tax, and social-insurance integration.** The system computes teaching-hour payroll figures and exports them; the accountant posts them elsewhere.
- **Attendance hardware** — biometric readers, card readers — and any hardware procurement.
- **Serving other companies.** Adding a fourth branch of this customer is *not* excluded: branches are configuration data in F11, so the branch planned for 2027 can be created by the center's own administrator. What is excluded is multi-tenant operation for other centers and consolidation across separate legal entities.
- **Historical data older than the two most recent terms.**
- **Support and maintenance after the warranty month.** The budget pays for hosting for 12 months, but the supplier's obligation to correct defects ends with the warranty month unless a separate support agreement is signed. Twelve months of hosting and one month of support are easy to confuse, so they are separated here deliberately.

### 1.5 Project Constraints

- **Budget** is fixed at 700,000,000 VND and covers software, deployment, migration, training, and warranty.
- **Duration** is fixed: 14 September 2026 to 5 February 2027, which is 144 days, or 20.6 weeks. The contract says five months; this document plans against the dates, not the rounded figure.
- **The warranty month must finish inside the project.** Go-live is therefore baselined a full month before closeout, not immediately before it. This constraint drives the whole schedule.
- **Team size is 5** full-time staff. No additional headcount is available, and the project manager is also the business analyst.
- **The system must be in Vietnamese** and must run within the center's existing cloud budget of one virtual server plus a staging environment.
- **The Lunar New Year break** begins immediately after closeout and can absorb no overrun.

### 1.6 Project Assumptions

Every invented figure in this document is listed here. None of them is given by the assignment brief, which supplies only the budget, the duration, and the team size.

| # | Assumption |
| --- | --- |
| 1 | The center has 1,200 active students, 35 teachers, and 3 branches. No real customer data is used; this is an academic exercise. |
| 2 | There are 52 staff users: the 35 teachers plus 17 administrative, finance, and management staff — 1 Director, 3 academic managers, 9 front-desk staff across the three branches, 3 accountants, 1 IT administrator. Students and parents are counted separately and are not part of the training target. |
| 3 | The parent portal peaks at about 300 concurrent sessions, when results are published or a tuition notice goes to the whole center. |
| 4 | Annual tuition turnover is about 7,200,000,000 VND — 1,200 students at about 6,000,000 VND a year. |
| 5 | Manual duplicate data entry costs about 60 staff-hours a month, at a fully loaded cost of about 60,000 VND a staff-hour. |
| 6 | About 8% of tuition sits past its due date, and about 1% of turnover is eventually written off. |
| 7 | The cost of carrying overdue money is taken at 10% a year, and hosting after the first 12 months at about 25,000,000 VND a year. |
| 8 | The Lunar New Year of 2027 begins on 6 February 2027. Closeout is baselined the day before. This should be checked against a published lunar calendar before the schedule is committed. |
| 9 | Personnel funding is contracted as 25 person-months, being 5 staff for 5 months. The elapsed window is shorter than five calendar months, so this is a funding basis rather than a measured effort figure. |
| 10 | The Academic Manager and the Accountant are each available at least 4 hours a week for workshops, demos, and UAT. |
| 11 | The center's Excel files are usable as the migration source and are cleaned by the center before migration. |
| 12 | One SMS and email gateway account is provided and paid for by the center, and its API is stable and documented. |
| 13 | Discount and refund rules are confirmed during analysis and frozen at requirement sign-off. |
| 14 | No public holiday other than the Lunar New Year break affects the schedule materially. |
| 15 | The commercial product name is not yet decided. |

---

## Part 2 — Project Charter

*All fourteen elements of Table 1.1, Elements of a Project Charter, in the order the book lists them*

### Project purpose

The center is run on paper and spreadsheets. That costs about 60 staff-hours a month in duplicate data entry, causes recurring room and teacher double-booking, and leaves about 8% of tuition sitting past its due date because nobody has a reliable debt list. The project removes that operational loss and gives the Director one current view of enrollment, revenue, and teaching capacity across three branches — which the center needs before it opens a fourth branch in 2027.

**The business case.** Three losses. Two can be quantified honestly; one cannot.

| Loss today | Value today | What the project changes |
| --- | --- | --- |
| Duplicate data entry | 60 hours a month at 60,000 VND = 43,200,000 VND a year | Falls to 15 hours a month: **32,400,000 VND a year, recurring** |
| Tuition sitting overdue | 8% of 7,200,000,000 VND = 576,000,000 VND overdue at any moment | Cut to 3%: releases **360,000,000 VND once**, then saves the cost of carrying it, about **36,000,000 VND a year** at 10% |
| Tuition eventually written off | 1% of turnover = 72,000,000 VND a year | Halved by chasing debt earlier: **36,000,000 VND a year, recurring** |
| Double-booking and lost class slots | Not measured by the center | Removed at source by the conflict check in F04, and left out of the calculation rather than estimated |

The overdue balance is a **stock, not a flow**. Cutting it from 8% to 3% releases the money once; only the carrying cost and the avoided write-off recur. Treating that release as an annual benefit would overstate the case roughly fourfold, so it is not treated that way here.

| | Amount |
| --- | --- |
| One-off cost | 700,000,000 VND, plus about 25,000,000 VND a year of hosting after the first 12 months |
| One-off benefit, first year | 360,000,000 VND released from overdue tuition |
| Recurring benefit | 104,400,000 VND a year — 32.4 staff time, 36.0 carrying cost, 36.0 write-off |
| Cumulative net | year 1 −235.6M, year 2 −156.2M, year 3 −76.8M, year 4 **+2.6M** |

Payback therefore falls in the **fourth year**, not the second; on recurring benefit alone it would be close to nine years. That is the honest number, and it is why the cash case is a sanity check rather than the argument. The real justification is strategic: the center cannot open a fourth branch on spreadsheets that already fail at three, and today it cannot see its own revenue or fill rate at all.

**Who owns the benefit.** Software does not collect tuition; people do. An aged debt list changes nothing unless somebody works it. The Accountant owns the tuition benefit, the front-desk supervisor owns the calls, and the Director reviews the overdue percentage monthly from go-live. Without that process change the project delivers a very accurate report of the same 8% — which is risk R10.

### High-level project description

Analyse, design, build, test, and deploy a Vietnamese-language web application managing the full operating cycle of a learning center — courses, classes and scheduling, students and enrollment, attendance, tuition and payments, teachers and teaching-hour payroll, assessment, notification, and management reporting — together with migration from the center's Excel files, staff training, and one month of warranty after go-live. Delivery is iterative: two build iterations, each ending in a demo, followed by user acceptance testing on the whole system. Five staff, five months, 700 million VND.

### Project boundaries

**Included:** functions F01 to F11 and the exception behaviour of section 1.1.5, for the three existing branches; migration of the two most recent terms; deployment on one cloud virtual server with a staging environment; training; documentation; one month of warranty.

**Excluded:** as listed in section 1.4 — native mobile apps, online teaching, payment gateways, accounting and tax integration, attendance hardware, service to other companies, data older than two terms, and support after the warranty month.

The project ends at the closeout meeting after the warranty month. Operating and hosting the system after that is the center's responsibility.

**Warranty terms.** The warranty month covers correction of defects against the accepted baseline. It is not a month of free change requests; enhancements raised during it are recorded for a later project. Response targets, counted from the center's report between 07:00 and 22:00:

| Severity | Meaning | Response | Workaround or fix |
| --- | --- | --- | --- |
| Critical | Money path or attendance unusable, or data lost | 2 working hours | 1 working day |
| High | A function unusable with no reasonable workaround | 1 working day | 5 working days |
| Medium or Low | Everything else | 2 working days | By agreement, or listed as a known issue at closeout |

A Critical or High defect still open at the end of the warranty month blocks closeout.

### Key deliverables

D1 to D10 as listed in section 1.2: requirement specification, design baseline, two iteration releases, test documentation, migrated and reconciled data, production deployment with a tested restore, user and administrator documentation with trained staff, source code and technical documentation, and the closeout report.

### High-level requirements

- One integrated database, with the same data never entered in two places.
- Room, teacher, and student timetable conflicts detected and blocked at the moment a class or session is created or moved.
- Tuition invoices generated from the course fee and the discount policy, with outstanding debt visible per student, class, and branch at any time.
- Teaching hours derived from recorded attendance rather than typed by hand, and exportable for payroll.
- Parents and teachers notified automatically for reminders, absence, tuition due, and results, with a delivery log.
- Each of the seven roles sees only what its role permits, and every change to financial or student data is auditable.
- The exception behaviour of section 1.1.5 delivered and tested with the same weight as the functions.
- A Vietnamese interface usable by existing staff after half a day of training.
- The acceptance criteria A01 to A11 of section 1.3 met.

### Overall project risk

**Medium.** The technology is well understood and the domain is stable. What raises the risk is that budget and end date are both fixed while the five-month window must contain delivery *and* a full warranty month, which leaves analysis, design, and test about one week of float each. The team is small enough that losing one developer moves the critical path, the project manager is also the business analyst, and the customer staff who own the business rules are only part-time available. The dominant uncertainty is the volatility of tuition, discount, and refund policy, which is a management decision of the center rather than a technical question. The exposure the center feels most directly is go-live itself: three branches switch over on one day, mid-term, four weeks before the Lunar New Year break, which can absorb no overrun.

| # | Risk | Response |
| --- | --- | --- |
| R1 | Tuition, discount, and refund rules change after the requirement baseline | Freeze the rules at M1 with written sign-off; route later changes through the change process against the reserve |
| R2 | Customer staff not available for workshops, demos, and UAT | Fixed weekly slot agreed with the sponsor at kickoff; a missed slot escalated to the sponsor within 2 working days |
| R3 | Loss or absence of a developer in a team of five | Pair on the scheduling and tuition modules; keep code and documentation in shared repositories; sponsor-approved replacement within 2 weeks |
| R4 | Notification gateway unstable or unexpectedly priced | Isolate it behind one interface; prove it with a proof of concept before M2; keep a second provider as fallback |
| R5 | Source Excel data too dirty to migrate | Assess data quality at M1; the center cleans the files before M5; migration limited to the two most recent terms |
| R6 | Scheduling and conflict detection harder than estimated | Build F04 first in iteration 1, timeboxed, and review it at the M3 demo |
| R7 | Go-live slips and pushes the warranty month into the Lunar New Year break | Baseline go-live at M6, a full month before the break; escalate to the sponsor immediately on a forecast slip past 15 January 2027, and re-plan the warranty rather than silently compress it |
| R8 | The project manager is also the business analyst, so analysis and management compete for one person | Front-load analysis into M0–M1 while management load is lowest; the QA engineer writes test cases from the requirement baseline as a second reader; escalate if analysis rework after M1 exceeds one week |
| R9 | Go-live fails and the center cannot run its evening classes | Pilot F01–F06 at one branch for the two weeks before M6; keep the spreadsheets in deliberate parallel for two weeks after go-live; rehearse the paper fallback; agree written rollback criteria that the center itself can invoke |
| R10 | The system is delivered but the tuition benefit never appears, because nobody works the debt list | Name the Accountant as benefit owner at M0; report the overdue percentage to the Director monthly from go-live; state the actual percentage in the closeout report |

### Project objectives and related success criteria

| Objective area | Objective | Success criteria |
| --- | --- | --- |
| Scope | Deliver F01 to F11 and D1 to D10 for the three branches | 100% of F01–F11 accepted in UAT; all ten deliverables signed off by the sponsor; no function deferred without an approved change request |
| Time | Go live by 5 January 2027 and close by 5 February 2027 | Go-live on or before 5 January 2027; no milestone more than 1 week late; the warranty period runs its full 31 days before closeout |
| Cost | Deliver the whole scope within 700,000,000 VND | Final cost at or below 700,000,000 VND; variance at each stage gate within ±5% of baseline; reserve use reported monthly |
| Quality | A system fit for daily operation from the first day | Acceptance criteria A01 to A11 of section 1.3 met |
| Stakeholder satisfaction | The center runs its daily operation on the system, not on spreadsheets | At least 80% of the 52 staff users trained and active in the first month, including at least 90% of the 17 administrative users and 75% of the 35 teachers; average user satisfaction at least 4 of 5 in the closeout survey; at least 90% of classes with attendance recorded in the system during the warranty month |

### Summary milestone schedule

| ID | Milestone | Due date |
| --- | --- | --- |
| M0 | Project kickoff, charter approved, team mobilised | Mon 14 Sep 2026 |
| M1 | Requirement specification approved and baselined | Fri 2 Oct 2026 |
| M2 | Design baseline approved | Fri 16 Oct 2026 |
| M3 | Iteration 1 demo accepted — F01 to F05 | Fri 13 Nov 2026 |
| M4 | Iteration 2 accepted, feature complete — F06 to F11 | Fri 11 Dec 2026 |
| M5 | System test complete, UAT entry criteria met | Fri 18 Dec 2026 |
| M6 | UAT signed off, data migrated, go-live and handover | Tue 5 Jan 2027 |
| M7 | Warranty complete, project closeout | Fri 5 Feb 2027 |

One branch pilots F01 to F06 in the two weeks before M6, and the spreadsheets keep running in deliberate parallel for two weeks after go-live. Go-live falls on a Tuesday so that live operation begins with two fully staffed working days; the other milestones fall on Fridays to close a working week. M6 to M7 is the warranty month, and it ends the day before the assumed start of the Lunar New Year break.

### Preapproved financial resources

Total **700,000,000 VND**, from the center's 2026–2027 capital budget, released against milestone acceptance: 20% at M0, 25% at M3, 30% at M4, 25% at M6. No further funding is committed; an increase requires the sponsor's written approval.

| # | Category | Amount (VND) | Share | Basis |
| --- | --- | --- | --- | --- |
| 1 | Personnel — 25 person-months | 490,000,000 | 70% | 19,600,000 VND per person-month, fully loaded |
| 2 | Infrastructure and licences | 70,000,000 | 10% | Cloud server and staging for 12 months, domain, SSL, gateway credits, development tools |
| 3 | Deployment, migration, training, documentation | 70,000,000 | 10% | On-site work at three branches, training materials, printing |
| 4 | Management reserve | 70,000,000 | 10% | Held by the project manager against risks R1 to R10 |
| | **Total** | **700,000,000** | **100%** | |

**Resources preassigned.** Five full-time staff are committed before planning starts and are not renegotiable: the project manager who also acts as business analyst, three developers, and one QA engineer. Two of the developers are assigned specifically for prior work on scheduling and billing, and are the pair that builds F04 and F06. On the customer side the sponsor commits the Academic Manager and the Accountant for at least four hours a week each, one cloud virtual server, and one paid notification gateway account.

### Key stakeholder list

| Stakeholder | Role in the project |
| --- | --- |
| Center Director | Sponsor: funds the project, approves the charter and scope changes, gives final acceptance |
| Academic Manager | Business owner for courses, classes, scheduling, assessment; main requirement source and UAT lead |
| Accountant | Business owner for tuition, debt, and payroll; owner of the tuition benefit; UAT participant |
| Front-desk / Admissions supervisor | Business owner for enrollment and payment recording; represents the daily users |
| Head Teacher | Represents the 35 teachers for attendance, scores, and teaching-hour screens |
| Students and parents | End users of schedule, result, and tuition views; recipients of notifications |
| Center IT administrator | Receives the system at handover; operates accounts, backup, and hosting afterwards |
| Project Manager | Plans, executes, and controls the project; single point of contact for the sponsor |
| Development team — 3 developers, 1 QA | Analysis, design, build, test, deployment, documentation |
| Notification gateway provider | External supplier of the SMS and email channel |
| Cloud hosting provider | External supplier of the production and staging environment |

### Project approval requirements

**What counts as success.** The five objectives above are met against their criteria, and at closeout the center is running its daily operation on the system. The two-week parallel run immediately after go-live is planned and is not a failure; failure would be the center still depending on its spreadsheets at closeout.

| To be approved | Approved by | Evidence |
| --- | --- | --- |
| This charter | Center Director, as sponsor | Signature on the charter form |
| Requirement specification (D1) | Academic Manager and Accountant for their areas; sponsor overall | Signed requirement baseline at M1 |
| Design baseline (D2) | Project Manager, reviewed with the Academic Manager for workflow fit | Signed design review record at M2 |
| Iteration releases (D3, D4) | Academic Manager, Accountant, and Front-desk supervisor for their functions | Signed demo acceptance record at M3 and M4 |
| Test completion (D5) | QA engineer prepares; Project Manager approves UAT entry | Test summary report accepted at M5 |
| UAT result and go-live | Business owners sign their own areas; sponsor authorises go-live | Signed UAT report and go-live authorisation at M6 |
| Migrated data (D6) | Accountant, for reconciliation against the source files | Written acceptance of the reconciliation, including accepted differences |
| Handover package (D8, D9) | Center IT administrator | Signed handover record |
| Project closure (D10) | Center Director, as sponsor | Signed closeout report |

**If UAT does not pass.** A pass rate below 95%, or any open Critical or High defect, means go-live is not authorised. Within two working days the project manager puts three options to the sponsor: correct and re-test with go-live delayed, stating exactly how many days of warranty that costs; go live against a written, sponsor-signed list of accepted defects with fix dates; or go live for part of the scope with the rest deferred to a change request. Silence is not acceptance — without a signed decision, the system does not go live.

**Who accepts the final product.** The Center Director, as sponsor and owner. Final acceptance cannot be delegated, but it rests on the written area sign-offs above, and it cannot be withheld for scope that was never in the baseline.

### Project exit criteria

The project closes when all of the following are true.

1. All deliverables D1 to D10 accepted in writing by the sponsor.
2. UAT signed off with at least 95% of test cases passed and no open Critical or High defect.
3. The system running in production with backup verified by a successful restore test.
4. Production data migrated and reconciled, with any differences accepted in writing by the Accountant.
5. At least 80% of the 52 staff users trained, evidenced by the training record.
6. Source code, database scripts, user manual, and administrator guide handed over and acknowledged.
7. The warranty month ended with no open Critical or High defect.
8. The paper fallback procedure and the full data export both demonstrated to the center and in its hands.
9. A written decision taken on support after the warranty month — either a support agreement or an explicit decision to operate the system unaided.
10. Closeout report, lessons learned, and final financial reconciliation approved, and the final invoice settled.

The sponsor may also close the project early if funding is withdrawn or the business need disappears. In that case the completed deliverables are handed over and the project closes with a termination report.

### Assigned project manager, responsibility, and authority level

**Project manager:** assigned full time for the whole five months, acting also as business analyst.

**Responsibility.** Plan, execute, monitor, and close the project; manage scope, schedule, cost, quality, risk, and communication; lead the team of five; act as the single point of contact for the sponsor and the center's staff; report status weekly.

**Staffing decisions.** May assign and re-assign work within the approved team of five, approve leave, and manage day-to-day performance. May request the replacement of a team member, with the sponsor notified. Hiring, firing, and contractual employment decisions remain with the supplier's line management.

**Budget management and variance.** May commit and spend within the approved baseline, including single transactions up to 20,000,000 VND and use of the 70,000,000 VND reserve against risks R1 to R10. Manages cumulative cost variance up to 5% of baseline. Escalates to the sponsor any forecast overrun beyond 5%, any reserve use beyond 40,000,000 VND, and any change in total funding.

**Technical decisions.** Full authority over architecture, technology stack, database design, coding standards, tooling, and the internal delivery approach, provided the acceptance criteria and the agreed deliverables are met, and decides the content of each iteration within the approved scope. Anything that changes user-visible scope, the schedule, or the cost goes to the sponsor through the change process.

**Conflict resolution.** Resolves conflicts within the team and between the team and the center's operational staff, including competing claims on staff availability. Conflicts that cross organisations, alter agreed scope, or remain unresolved after five working days go to the sponsor, whose decision is final. Disputes with external suppliers follow the applicable service agreement.

### Name and authority of the sponsor

**Sponsor:** Đỗ Thị Bích Ngọc, owner and Director of the learning center.

The sponsor authorises the project and this charter, provides and releases the 700 million VND, appoints the project manager, and makes the center's staff available. The sponsor approves changes to scope, schedule, and budget beyond the project manager's authority, sets acceptable variance limits, resolves conflicts escalated by the project manager or arising between departments, accepts the deliverables, and authorises go-live and project closure. The sponsor champions the project with the center's staff and with the branch managers.
