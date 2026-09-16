# Learning Center Management Software

## Requirement Specification and Project Charter

**Project:** Development and Deployment of a Learning Center Management Software
**Budget:** 700,000,000 VND (700 million VND)
**Duration:** 5 months, 14 September 2026 to 5 February 2027 (144 days, 20.6 weeks)
**Team:** 5 full-time staff, being 1 project manager / business analyst, 3 developers, 1 QA engineer
**Sponsor:** <mark>Dr. Nguyễn Mạnh Hùng</mark>
**Customer:** <mark>Đỗ Thị Bích Ngọc, owner and Director of the learning center</mark>
**Date prepared:** 2 September 2026
**Document version:** 3.0
**Prepared by:** ________________________________  (name, student ID, class)

### How this document is organised

All three parts follow *A Project Manager's Book of Forms*, 3rd edition.

| Part | Answers | Source in the book |
| --- | --- | --- |
| Part 1 | Point 1, requirement specification | Form 2.8 Project Scope Statement, pages 58 to 59 |
| Part 2A | Point 2, charter content | Table 1.1 Elements of a Project Charter, section 1.1, pages 13 to 15 |
| Part 2B | Points 2 and 3, the charter itself | The four-page PROJECT CHARTER form, pages 16 to 19 |
| Part 3 | Point 4, prompt log | Not from the book |

Part 1 uses form 2.8 because it is the book's free-text form for describing scope: scope description, deliverables, acceptance criteria, exclusions, constraints, assumptions. The function list and the per-function descriptions sit inside the scope description, and the measurable non-functional targets sit inside the acceptance criteria, where the form expects them. Page 14 of the book explicitly supports pairing the scope statement with the charter on a small project.

Part 2A covers all fourteen charter elements in the order the book lists them. Part 2B then reproduces the printed four-page form field for field and fills it in, so the charter exists in the prescribed layout as well as in the element order.

### Contents

**Part 1, Requirement Specification.** 1.1 Project scope description (the problem, the product, users and roles, functions F01 to F11, exception and failure behaviour). 1.2 Project deliverables D1 to D10. 1.3 Product acceptance criteria A01 to A11. 1.4 Project exclusions. 1.5 Project constraints. 1.6 Project assumptions.

**Part 2, Project Charter.** 2A Charter elements, all fourteen in the book's order, including the business case, the risk register R1 to R10, the milestone schedule, and the budget. 2B The PROJECT CHARTER form, filled in, four pages.

**Part 3, Prompt Log.** 3.1 Version history V1 to V11. 3.2 The prompts, with a quality assessment of each. 3.3 What the sequence shows.

### Reading convention

Two conventions are used, both required by point 3 of the assignment.

- <mark>Yellow highlight</mark> marks content whose correctness cannot be confirmed from the assignment brief. The brief supplies only the budget, the duration, and the team size. Everything else is an assumption made to produce a complete document, and every such figure is also listed in section 1.6.
- An **empty box** in the Part 2B form means the field cannot be completed at this stage rather than that it was overlooked. Three kinds of box are empty: the project manager's name, which the sponsor assigns at M0; the signature boxes; and the signature dates. All three are completed on signing.

Content that comes from the brief, and deliberate design decisions such as the function set F01 to F11, are not highlighted. They are choices, not guesses.

---

## Part 1: Requirement Specification

*Form 2.8, Project Scope Statement*

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 2 September 2026

### 1.1 Project Scope Description

#### 1.1.1 The problem

The customer owns a private after-school learning center with <mark>about 1,200 active students, 35 teachers, and 3 branches in one city</mark>. It teaches <mark>English, mathematics, and IT skills</mark> in fixed-length courses of <mark>24 to 48 sessions</mark>. The learners are school-age students, <mark>aged 6 to 18</mark>, who attend after school and at weekends; the center runs no preschool programme, and the system is scoped to these learners at these three branches.

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
| Center Director | Owner of the center, and the project's customer | Dashboards, revenue and enrollment reports, approvals |
| Academic Manager | Runs the teaching operation | Course catalog, opening classes, scheduling, teacher assignment, assessment; assigns substitutes and postpones sessions, approves teaching-hour sheets, reviews the daily exception list |
| Front-desk / Admissions staff | Reception counter at each branch | Student profiles, enrollment, invoices, recording payments, parent enquiries; handles make-up and re-enrollment requests and sends the notifications of F09 |
| Teacher | Teaching staff | Class roster, attendance, scores and progress comments, session notes and a per-class report, announcements and messages to parents, own teaching-hour sheet, the end-of-course evaluation of their classes |
| Accountant | Finance | Debt tracking, payment confirmation, matching of unmatched bank transfers, approval of refund proposals, teaching-hour payroll and the monthly payroll close, financial reports |
| Student / Parent | End customer | Own schedule, attendance and score history, tuition balance, notifications and messages to the front desk, make-up session request, bank-transfer confirmation with reference, re-enrollment request, end-of-course evaluation of the course and the teacher |
| System Administrator | The center's IT staff | Accounts, roles, configuration, backup, audit log |

#### 1.1.4 Functions

| ID | Function | Primary actor | Description |
| --- | --- | --- | --- |
| F01 | Authentication and access control | System Administrator | Creates accounts, authenticates users by username and password, resets passwords, times out idle sessions, and enforces role-based permission so that each role sees only its own screens and its own data. Every account has exactly one role; staff accounts are additionally tied to one or more branches. |
| F02 | Student profile and enrollment | Front-desk staff | Records the student profile (personal data, guardian and contact details, how the student found the center, notes) and enrolls the student into an open class. Handles transfer between classes, reservation of a seat, and withdrawal with a refund calculation. Refuses an enrollment when the class is full or when the timetable collides with another class of the same student. |
| F03 | Course and curriculum catalog | Academic Manager | Defines what the center sells: course code, level, number of sessions, session length, standard tuition fee, prerequisite course, and the syllabus outline session by session. Courses are versioned, so that editing a course does not change the definition of classes that were already opened from it. |
| F04 | Class opening, scheduling, and assignment | Academic Manager | Opens a class from a course (branch, start date, weekly time slots, capacity), generates the whole session calendar from that, and assigns a room and a teacher to each session. Detects and blocks conflicts on room, on teacher, and on class time at the moment the class or session is created or moved, and recalculates the calendar when a session is postponed. |
| F05 | Attendance and make-up sessions | Teacher | Marks every student of a session present, absent with notice, absent without notice, or late, with an optional remark. Registers a make-up session in another class for an absent student, and shows the attendance rate per student and per class. |
| F06 | Tuition, invoicing, and debt tracking | Front-desk staff, Accountant | Generates the tuition invoice at enrollment from the course fee, applying the discount policies of the center (sibling, early payment, referral, promotion code) and installment plans. Records cash and bank-transfer payments against invoices, issues receipts, and maintains the outstanding balance and an aged debt list per student, per class, and per branch. |
| F07 | Teacher records and teaching-hour payroll | Accountant | Holds teacher profiles, qualifications, contract type, and pay rate per teaching hour by course level. Aggregates the sessions actually taught, taken from F05, into a monthly teaching-hour sheet per teacher, applies allowances and deductions, and exports the payroll figures to Excel. |
| F08 | Assessment, progress reports, and course evaluation | Teacher | Records scores for the assessment items the course defines (quizzes, midterm, final, skill scores) and a comment per student. Computes the final result and pass or fail against the course rule, and produces a printable progress report per student and a result summary per class. At the end of each course collects an evaluation of the course and the teacher from students and parents, on a fixed five-point scale with a free comment, and reports it per class and per teacher to the Academic Manager. |
| F09 | Notification and internal communication | Front-desk staff | Sends email and SMS from templates for the events that matter: enrollment confirmed, session reminder, absence alert, tuition due, tuition overdue, schedule changed, results published. Supports a manual send to a chosen group, a scheduled automatic send, and a log of every message with its delivery status. Carries the center's internal communication in the same place: announcements from the Academic Manager to teachers and staff, a per-class notice board from the teacher to the parents of that class, and messages between a parent and the front desk, all kept in the same log. |
| F10 | Reports and management dashboard | Center Director | The management view: revenue and collection by period and branch, outstanding debt, new and retained student counts, class fill rate, teacher workload and teaching hours, attendance rate. Every report is filterable by period, branch, and course, and exports to Excel and PDF. |
| F11 | System administration and audit | System Administrator | Maintains the center's reference data and configuration (branches, rooms, terms, fee and discount policies, notification templates, holidays), triggers and restores backups, and keeps an audit log of every create, update, and delete on financial and student data, with the user and the timestamp. |

#### 1.1.5 Exception and failure behaviour

The eleven functions above describe the system working normally. The cases below define what the system must do when it does not, and they are in scope on the same terms as the functions themselves.

| Situation | Required behaviour |
| --- | --- |
| A teacher does not record attendance | The session is flagged *attendance missing* on the Academic Manager's daily exception list. Attendance can still be entered later, but a late entry is stamped as late with the name of whoever entered it, and a month containing missing attendance cannot be closed for payroll. |
| A teacher is absent on the day | The Academic Manager assigns a substitute or postpones the session. Teaching hours are credited to whoever actually taught, never to whoever was originally scheduled. Affected parents are notified automatically. |
| A class is cancelled after students have paid | One action applies the center's cancellation policy to every enrolled student, producing a refund proposal or a credit note on each balance, and records the reason. The sessions are marked cancelled and keep their history; nothing is deleted. |
| A student withdraws mid-course | The refund is calculated from the sessions actually delivered. It is a proposal: it does not change the balance until the Accountant approves it. The seat is released. |
| A bank transfer cannot be matched to an invoice | The payment is held in an unmatched list. It is neither guessed at nor discarded, and no balance moves until someone matches it. No overdue reminder is sent to a student who has an unmatched payment on file, so that a parent who has already paid is not chased for the money. |
| A parent overpays or pays twice | The excess becomes a credit on the payer's account. Moving a credit between siblings needs the Accountant. Reversing a receipt is not a delete: it posts a reversing entry, and both entries stay in the audit log. |
| The SMS or email gateway fails | Every message carries a delivery state and, on failure, a reason. Failed messages are retried and then listed for manual action, and the administrator is alerted when gateway credit runs low. No failed notification is dropped without a record. |
| A teacher disputes the monthly teaching-hour sheet | The sheet moves through draft, confirmed by teacher, approved by Academic Manager, exported. Only approved sheets reach payroll, and the person who recorded the attendance is never the person who approves the sheet that pays for it. |
| The system is unavailable during teaching hours | The center falls back to a written paper procedure for attendance and receipts, and enters the data afterwards. Late entry is stamped as such and does not corrupt the payroll or debt figures. The fallback is part of the user manual and is rehearsed before go-live. |
| Migrated data does not reconcile with the Excel files | Migration produces a reconciliation report of every difference. Go-live requires the Accountant's written acceptance of that report, including any difference the center chooses to accept rather than correct. |

### 1.2 Project Deliverables

| # | Deliverable | Due at |
| --- | --- | --- |
| D1 | Requirement specification, approved and baselined | M1 |
| D2 | Design baseline: architecture, database schema, UI design | M2 |
| D3 | Iteration 1 release, F01 to F05 | M3 |
| D4 | Iteration 2 release, F06 to F11 | M4 |
| D5 | Test documentation: test plan, test cases, defect log, test summary report | M5 |
| D6 | Production data migrated and reconciled against the source files | M6 |
| D7 | Production deployment on the cloud server, with backup configured and a restore tested | M6 |
| D8 | User manual, administrator and deployment guide, trained staff with a training record | M6 |
| D9 | Source code, database scripts, and technical documentation handed over | M6 |
| D10 | Warranty period completed, closeout report and lessons learned | M7 |

### 1.3 Product Acceptance Criteria

The product is accepted when the functions of 1.1.4 and the behaviour of 1.1.5 pass user acceptance testing and the measurable criteria below are met. Each criterion is stated as a threshold, so that acceptance can be measured rather than judged.

| ID | Category | Criterion |
| --- | --- | --- |
| A01 | Functional completeness | 100% of F01 to F11 accepted in UAT; at least 95% of UAT test cases passed; no open Critical or High defect; at most 5 open Medium defects, each with an agreed fix date, and none of them in the tuition, payment, or teaching-hour path |
| A02 | Performance | Staff screens respond within 3 seconds with <mark>52 concurrent staff users</mark>; the parent portal responds within 3 seconds at <mark>300 concurrent sessions</mark>; a report covering one term is produced within 10 seconds |
| A03 | Capacity | <mark>5,000 student records, 200 classes per term, and 3 years of session history</mark> without redesign |
| A04 | Security | HTTPS only; passwords never stored or recoverable in readable form; every request authorised on the server; personal data handled in line with the <mark>Law on Personal Data Protection in force from 1 January 2026</mark>; notification consent recorded per guardian |
| A05 | Auditability | Every create, update, and delete on financial and student records written to an audit log that cannot be edited, kept for at least <mark>3 years</mark> |
| A06 | Availability | <mark>99% availability between 07:00 and 22:00</mark>, measured monthly; nightly backup with a recovery point objective of 24 hours and a recovery time objective of 4 hours; the restore demonstrated once during UAT and once during warranty |
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
- **Attendance hardware** such as biometric and card readers, and any hardware procurement.
- **Serving other companies.** Adding a fourth branch of this customer is *not* excluded: branches are configuration data in F11, so the <mark>branch planned for 2027</mark> can be created by the center's own administrator. What is excluded is multi-tenant operation for other centers and consolidation across separate legal entities.
- **Preschool programmes and learners under 6.** The center's courses are for school-age learners; nothing in the system is designed for a kindergarten.
- **Historical data older than the two most recent terms.**
- **Support and maintenance after the warranty month.** The budget pays for hosting for 12 months, but the supplier's obligation to correct defects ends with the warranty month unless a separate support agreement is signed. The 12 months of hosting and the 1 month of support are separate commitments and are listed separately here.
- **Project exclusions**, as distinct from the product exclusions above. The project does not procure or pay for the cloud or gateway subscriptions beyond the first 12 months; does not clean the source Excel files, which the center does (assumption 11); does not recruit, restructure, or manage the center's staff; does not operate the system after handover; and does not train parents beyond the user guide and the onboarding message.

### 1.5 Project Constraints

- **Budget** is fixed at 700,000,000 VND and covers software, deployment, migration, training, and warranty.
- **Duration** is fixed: <mark>14 September 2026 to 5 February 2027</mark>, which is 144 days, or 20.6 weeks. The brief says five months; this document plans against the dates, not the rounded figure.
- **The warranty month must finish inside the project.** Go-live is therefore baselined a full month before closeout, not immediately before it. This constraint drives the whole schedule.
- **Team size is 5** full-time staff. No additional headcount is available, and the project manager is also the business analyst.
- **The system must be in Vietnamese** and must run within the center's <mark>existing cloud budget of one virtual server plus a staging environment</mark>.
- **The Lunar New Year break** begins immediately after closeout and can absorb no overrun.

### 1.6 Project Assumptions

Every assumed figure in this document is listed here. None of them is given by the assignment brief, which supplies only the budget, the duration, and the team size. Each is highlighted where it appears in the text.

| # | Assumption |
| --- | --- |
| 1 | The center has 1,200 active students aged 6 to 18, 35 teachers, and 3 branches, and runs no preschool programme. No real customer data is used; this is an academic exercise. |
| 2 | There are 52 staff users: the 35 teachers plus 17 administrative, finance, and management staff, being 1 Director, 3 academic managers, 9 front-desk staff across the three branches, 3 accountants, and 1 IT administrator. Students and parents are counted separately and are not part of the training target. |
| 3 | The parent portal peaks at about 300 concurrent sessions, when results are published or a tuition notice goes to the whole center. |
| 4 | Annual tuition turnover is about 7,200,000,000 VND, being 1,200 students at about 6,000,000 VND a year. |
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
| 15 | The commercial product name and the project manager's name are not yet decided. |
| 16 | The sponsor and the customer are two different people. The sponsor's organisational relationship to the learning center is not stated, because it was not specified; the charter defines his authority rather than his affiliation. Funding is released by the sponsor against the center's capital budget. |

---

## Part 2: Project Charter

### 2A. Charter elements

*All fourteen elements of Table 1.1, Elements of a Project Charter, in the order the book lists them*

#### Project purpose

The center is run on paper and spreadsheets. That costs about <mark>60 staff-hours a month</mark> in duplicate data entry, causes recurring room and teacher double-booking, and leaves about <mark>8% of tuition</mark> sitting past its due date because nobody has a reliable debt list. The project removes that operational loss and gives the Director one current view of enrollment, revenue, and teaching capacity across three branches, which the center needs before it opens a <mark>fourth branch in 2027</mark>.

**The business case.** The center loses money in three ways today. Two of them can be quantified from the assumptions in section 1.6; the third cannot be quantified from anything the center currently measures, and is therefore left out of the calculation rather than estimated.

| Loss today | Value today | What the project changes |
| --- | --- | --- |
| Duplicate data entry | 60 hours a month at 60,000 VND = 43,200,000 VND a year | Falls to 15 hours a month: 32,400,000 VND a year, recurring |
| Tuition sitting overdue | 8% of 7,200,000,000 VND = 576,000,000 VND overdue at any moment | Cut to 3%: releases 360,000,000 VND once, then saves the cost of carrying it, about 36,000,000 VND a year at 10% |
| Tuition eventually written off | 1% of turnover = 72,000,000 VND a year | Halved by chasing debt earlier: 36,000,000 VND a year, recurring |
| Double-booking and lost class slots | Not measured by the center | Removed at source by the conflict check in F04, and excluded from the calculation |

The overdue balance is a stock, not a flow. Cutting it from 8% to 3% releases the money once; only the carrying cost and the avoided write-off recur. Treating that release as an annual benefit would overstate the case by roughly a factor of four, so it is treated as a one-off below.

| | Amount |
| --- | --- |
| One-off cost | 700,000,000 VND, plus about 25,000,000 VND a year of hosting after the first 12 months |
| One-off benefit, first year | 360,000,000 VND released from overdue tuition |
| Recurring benefit | 104,400,000 VND a year: 32.4 staff time, 36.0 carrying cost, 36.0 write-off |
| Cumulative net | year 1 -235.6M, year 2 -156.2M, year 3 -76.8M, year 4 +2.6M |

Payback therefore falls in the fourth year, not the second; on recurring benefit alone it would be close to nine years. The cash case is a sanity check rather than the main argument for the project. The main justification is strategic: the center cannot open a fourth branch on spreadsheets that already fail at three, and today it has no visibility of its own revenue or fill rate.

**Who owns the benefit.** An aged debt list does not collect tuition on its own; somebody has to work it. The Accountant owns the tuition benefit, the front-desk supervisor owns the calls, and the Director reviews the overdue percentage monthly from go-live. Without that process change the project delivers an accurate report of the same 8%, which is risk R10.

#### High-level project description

Analyse, design, build, test, and deploy a Vietnamese-language web application managing the full operating cycle of a learning center: courses, classes and scheduling, students and enrollment, attendance, tuition and payments, teachers and teaching-hour payroll, assessment, notification, and management reporting. The project also covers migration from the center's Excel files, staff training, and one month of warranty after go-live. Delivery is iterative: two build iterations, each ending in a demo, followed by user acceptance testing on the whole system. Five staff, five months, 700 million VND.

#### Project boundaries

**Included:** functions F01 to F11 and the exception behaviour of section 1.1.5, for the school-age learners of the three existing branches; migration of the two most recent terms; deployment on one cloud virtual server with a staging environment; training; documentation; one month of warranty.

**Excluded:** as listed in section 1.4, being native mobile apps, online teaching, payment gateways, accounting and tax integration, attendance hardware, service to other companies, preschool learners, data older than two terms, and support after the warranty month; and the project-level exclusions of the same section: subscriptions beyond 12 months, cleaning of the source data, staffing and organisation of the center, and operation after handover.

The project ends at the closeout meeting after the warranty month. Operating and hosting the system after that is the center's responsibility.

**Warranty terms.** The warranty month covers correction of defects against the accepted baseline. It is not a month of free change requests; enhancements raised during it are recorded for a later project. Response targets, counted from the center's report between 07:00 and 22:00:

| Severity | Meaning | Response | Workaround or fix |
| --- | --- | --- | --- |
| Critical | Money path or attendance unusable, or data lost | 2 working hours | 1 working day |
| High | A function unusable with no reasonable workaround | 1 working day | 5 working days |
| Medium or Low | Everything else | 2 working days | By agreement, or listed as a known issue at closeout |

A Critical or High defect still open at the end of the warranty month blocks closeout.

#### Key deliverables

D1 to D10 as listed in section 1.2: requirement specification, design baseline, two iteration releases, test documentation, migrated and reconciled data, production deployment with a tested restore, user and administrator documentation with trained staff, source code and technical documentation, and the closeout report.

#### High-level requirements

- One integrated database, with the same data never entered in two places.
- Room, teacher, and student timetable conflicts detected and blocked at the moment a class or session is created or moved.
- Tuition invoices generated from the course fee and the discount policy, with outstanding debt visible per student, class, and branch at any time.
- Teaching hours derived from recorded attendance rather than typed by hand, and exportable for payroll.
- Parents and teachers notified automatically for reminders, absence, tuition due, and results, with a delivery log; internal announcements and parent messages carried in the same channel.
- Each of the seven roles sees only what its role permits, and every change to financial or student data is auditable.
- The exception behaviour of section 1.1.5 delivered and tested with the same weight as the functions.
- A Vietnamese interface usable by existing staff after half a day of training.
- The acceptance criteria A01 to A11 of section 1.3 met.

#### Overall project risk

**Medium.** The technology is well understood and the domain is stable. What raises the risk is that budget and end date are both fixed while the five-month window must contain delivery *and* a full warranty month, which leaves analysis, design, and test about one week of float each. The team is small enough that losing one developer moves the critical path, the project manager is also the business analyst, and the customer staff who own the business rules are only part-time available. The dominant uncertainty is the volatility of tuition, discount, and refund policy, which is a management decision of the center rather than a technical question. The exposure the center feels most directly is go-live itself: three branches switch over on one day, mid-term, four weeks before the Lunar New Year break, which can absorb no overrun.

| # | Risk | Response |
| --- | --- | --- |
| R1 | Tuition, discount, and refund rules change after the requirement baseline | Freeze the rules at M1 with written sign-off; route later changes through the change process against the reserve |
| R2 | Customer staff not available for workshops, demos, and UAT | Fixed weekly slot agreed with the sponsor at kickoff; a missed slot escalated to the sponsor within 2 working days |
| R3 | Loss or absence of a developer in a team of five | Pair on the scheduling and tuition modules; keep code and documentation in shared repositories; sponsor-approved replacement within 2 weeks |
| R4 | Notification gateway unstable or unexpectedly priced | Isolate it behind one interface; prove it with a proof of concept before M2; keep a second provider as fallback |
| R5 | Source Excel data too dirty to migrate | Assess data quality at M1; the center cleans the files before M5; migration limited to the two most recent terms |
| R6 | Scheduling and conflict detection harder than estimated | Build F04 first in iteration 1, timeboxed, and review it at the M3 demo |
| R7 | Go-live slips and pushes the warranty month into the Lunar New Year break | Baseline go-live at M6, a full month before the break; escalate to the sponsor immediately on a forecast slip past 15 January 2027, and re-plan the warranty rather than compress it silently |
| R8 | The project manager is also the business analyst, so analysis and management compete for one person | Front-load analysis into M0 to M1 while management load is lowest; the QA engineer writes test cases from the requirement baseline as a second reader; escalate if analysis rework after M1 exceeds one week |
| R9 | Go-live fails and the center cannot run its evening classes | Pilot F01 to F06 at one branch for the two weeks before M6; keep the spreadsheets in deliberate parallel for two weeks after go-live; rehearse the paper fallback; agree written rollback criteria that the center itself can invoke |
| R10 | The system is delivered but the tuition benefit never appears, because nobody works the debt list | Name the Accountant as benefit owner at M0; report the overdue percentage to the Director monthly from go-live; state the actual percentage in the closeout report |

#### Project objectives and related success criteria

| Objective area | Objective | Success criteria |
| --- | --- | --- |
| Scope | Deliver F01 to F11 and D1 to D10 for the three branches | 100% of F01 to F11 accepted in UAT; all ten deliverables signed off by the sponsor; no function deferred without an approved change request |
| Time | Go live by 5 January 2027 and close by 5 February 2027 | Go-live on or before 5 January 2027; no milestone more than 1 week late; the warranty period runs its full 31 days before closeout |
| Cost | Deliver the whole scope within 700,000,000 VND | Final cost at or below 700,000,000 VND; variance at each stage gate within plus or minus 5% of baseline; reserve use reported monthly |
| Quality | A system fit for daily operation from the first day | Acceptance criteria A01 to A11 of section 1.3 met |
| Stakeholder satisfaction | The center runs its daily operation on the system, not on spreadsheets | At least 80% of the <mark>52 staff users</mark> trained and active in the first month, including at least 90% of the 17 administrative users and 75% of the 35 teachers; average user satisfaction at least 4 of 5 in the closeout survey; at least 90% of classes with attendance recorded in the system during the warranty month |

#### Summary milestone schedule

| ID | Milestone | Due date |
| --- | --- | --- |
| M0 | Project kickoff, charter approved, team mobilised | <mark>Mon 14 Sep 2026</mark> |
| M1 | Requirement specification approved and baselined | <mark>Fri 2 Oct 2026</mark> |
| M2 | Design baseline approved | <mark>Fri 16 Oct 2026</mark> |
| M3 | Iteration 1 demo accepted, F01 to F05 | <mark>Fri 13 Nov 2026</mark> |
| M4 | Iteration 2 accepted, feature complete, F06 to F11 | <mark>Fri 11 Dec 2026</mark> |
| M5 | System test complete, UAT entry criteria met | <mark>Fri 18 Dec 2026</mark> |
| M6 | UAT signed off, data migrated, go-live and handover | <mark>Tue 5 Jan 2027</mark> |
| M7 | Warranty complete, project closeout | <mark>Fri 5 Feb 2027</mark> |

One branch pilots F01 to F06 in the two weeks before M6, and the spreadsheets keep running in deliberate parallel for two weeks after go-live. Go-live falls on a Tuesday so that live operation begins with two fully staffed working days; the other milestones fall on Fridays to close a working week. M6 to M7 is the warranty month, and it ends the day before the assumed start of the Lunar New Year break.

#### Preapproved financial resources

Total **700,000,000 VND**, from the center's <mark>2026 to 2027 capital budget</mark>, released against milestone acceptance: <mark>20% at M0, 25% at M3, 30% at M4, 25% at M6</mark>. No further funding is committed; an increase requires the sponsor's written approval.

| # | Category | Amount (VND) | Share | Basis |
| --- | --- | --- | --- | --- |
| 1 | Personnel, 25 person-months | 490,000,000 | 70% | <mark>19,600,000 VND per person-month, fully loaded</mark> |
| 2 | Infrastructure and licences | 70,000,000 | 10% | Cloud server and staging for 12 months, domain, SSL, gateway credits, development tools |
| 3 | Deployment, migration, training, documentation | 70,000,000 | 10% | On-site work at three branches, training materials, printing |
| 4 | Management reserve | 70,000,000 | 10% | Held by the project manager against risks R1 to R10 |
| | **Total** | **700,000,000** | **100%** | |

**Resources preassigned.** Five full-time staff are committed before planning starts and are not renegotiable: the project manager who also acts as business analyst, three developers, and one QA engineer. <mark>Two of the developers are assigned specifically for prior work on scheduling and billing, and are the pair that builds F04 and F06.</mark> On the customer side the Center Director commits the Academic Manager and the Accountant for at least four hours a week each, one cloud virtual server, and one paid notification gateway account, and the sponsor holds her to that commitment.

#### Key stakeholder list

| Stakeholder | Role in the project |
| --- | --- |
| <mark>Dr. Nguyễn Mạnh Hùng</mark> | Sponsor: authorises the project and this charter, releases the funding, approves scope changes beyond the project manager's authority, gives final acceptance |
| <mark>Đỗ Thị Bích Ngọc</mark>, owner and Center Director | Customer: owns the business need, commits the center's staff and data to the project, and takes the system into daily operation |
| Academic Manager | Business owner for courses, classes, scheduling, assessment; main requirement source and UAT lead |
| Accountant | Business owner for tuition, debt, and payroll; owner of the tuition benefit; UAT participant |
| Front-desk / Admissions supervisor | Business owner for enrollment and payment recording; represents the daily users |
| Head Teacher | Represents the 35 teachers for attendance, scores, and teaching-hour screens |
| Students and parents | End users of schedule, result, and tuition views; recipients of notifications |
| Center IT administrator | Receives the system at handover; operates accounts, backup, and hosting afterwards |
| Project Manager | Plans, executes, and controls the project; single point of contact for the sponsor |
| Development team, 3 developers and 1 QA | Analysis, design, build, test, deployment, documentation |
| Notification gateway provider | External supplier of the SMS and email channel |
| Cloud hosting provider | External supplier of the production and staging environment |

#### Project approval requirements

**What counts as success.** The five objectives above are met against their criteria, and at closeout the center is running its daily operation on the system. The two-week parallel run immediately after go-live is planned and is not a failure; failure would be the center still depending on its spreadsheets at closeout.

| To be approved | Approved by | Evidence |
| --- | --- | --- |
| This charter | <mark>Dr. Nguyễn Mạnh Hùng</mark>, as sponsor | Signature on the charter form in section 2B |
| Requirement specification (D1) | Academic Manager and Accountant for their areas; sponsor overall | Signed requirement baseline at M1 |
| Design baseline (D2) | Project Manager, reviewed with the Academic Manager for workflow fit | Signed design review record at M2 |
| Iteration releases (D3, D4) | Academic Manager, Accountant, and Front-desk supervisor for their functions | Signed demo acceptance record at M3 and M4 |
| Test completion (D5) | QA engineer prepares; Project Manager approves UAT entry | Test summary report accepted at M5 |
| UAT result and go-live | Business owners sign their own areas; sponsor authorises go-live | Signed UAT report and go-live authorisation at M6 |
| Migrated data (D6) | Accountant, for reconciliation against the source files | Written acceptance of the reconciliation, including accepted differences |
| Handover package (D8, D9) | Center IT administrator | Signed handover record |
| Project closure (D10) | Sponsor, on the Center Director's confirmation that the center is operating on the system | Signed closeout report |

**If UAT does not pass.** A pass rate below 95%, or any open Critical or High defect, means go-live is not authorised. Within two working days the project manager puts three options to the sponsor: correct and re-test with go-live delayed, stating exactly how many days of warranty that costs; go live against a written, sponsor-signed list of accepted defects with fix dates; or go live for part of the scope with the rest deferred to a change request. Without a signed decision from the sponsor, the system does not go live.

**Who accepts the final product.** The sponsor gives final acceptance. It cannot be delegated, but it rests on the written area sign-offs above and on the Center Director's confirmation, as customer, that the center is running its daily operation on the system. Acceptance cannot be withheld for scope that was never in the baseline.

#### Project exit criteria

The project closes when all of the following are true.

1. All deliverables D1 to D10 accepted in writing by the sponsor.
2. UAT signed off with at least 95% of test cases passed and no open Critical or High defect.
3. The system running in production with backup verified by a successful restore test.
4. Production data migrated and reconciled, with any differences accepted in writing by the Accountant.
5. At least 80% of the <mark>52 staff users</mark> trained, evidenced by the training record.
6. Source code, database scripts, user manual, and administrator guide handed over and acknowledged.
7. The warranty month ended with no open Critical or High defect.
8. The paper fallback procedure and the full data export both demonstrated to the center and in its hands.
9. A written decision taken on support after the warranty month, either a support agreement or an explicit decision to operate the system unaided.
10. Closeout report, lessons learned, and final financial reconciliation approved, and the final invoice settled.

The sponsor may also close the project early if funding is withdrawn or the business need disappears. In that case the completed deliverables are handed over and the project closes with a termination report.

#### Assigned project manager, responsibility, and authority level

**Project manager:** <mark>name to be assigned by the sponsor at M0</mark>, assigned full time for the whole five months, acting also as business analyst.

**Responsibility.** Plan, execute, monitor, and close the project; manage scope, schedule, cost, quality, risk, and communication; lead the team of five; act as the single point of contact for the sponsor and the center's staff; report status weekly.

**Staffing decisions.** May assign and re-assign work within the approved team of five, approve leave, and manage day-to-day performance. May request the replacement of a team member, with the sponsor notified. Hiring, firing, and contractual employment decisions remain with the supplier's line management.

**Budget management and variance.** May commit and spend within the approved baseline, including <mark>single transactions up to 20,000,000 VND</mark> and use of the 70,000,000 VND reserve against risks R1 to R10. Manages cumulative cost variance up to 5% of baseline. Escalates to the sponsor any forecast overrun beyond 5%, <mark>any reserve use beyond 40,000,000 VND</mark>, and any change in total funding.

**Technical decisions.** Full authority over architecture, technology stack, database design, coding standards, tooling, and the internal delivery approach, provided the acceptance criteria and the agreed deliverables are met, and decides the content of each iteration within the approved scope. Anything that changes user-visible scope, the schedule, or the cost goes to the sponsor through the change process.

**Conflict resolution.** Resolves conflicts within the team and between the team and the center's operational staff, including competing claims on staff availability. Conflicts that cross organisations, alter agreed scope, or remain unresolved after <mark>five working days</mark> go to the sponsor, whose decision is final. Disputes with external suppliers follow the applicable service agreement.

#### Name and authority of the sponsor

**Sponsor:** <mark>Dr. Nguyễn Mạnh Hùng</mark>

**Customer:** <mark>Đỗ Thị Bích Ngọc, owner and Director of the learning center.</mark>

The sponsor and the customer are two different people, and the charter keeps their authority separate. The sponsor authorises the project and this charter, releases the 700 million VND, and appoints the project manager. The sponsor approves changes to scope, schedule, and budget beyond the project manager's authority, sets acceptable variance limits, resolves conflicts escalated by the project manager, accepts the deliverables, and authorises go-live and project closure.

The customer owns the business need and the operation the system will run. The Center Director makes the center's staff and data available, nominates the business owners who sign for their own areas, and confirms at closeout that the center is operating on the system. Where a decision is about what the center needs, it is the customer's; where it is about whether the project continues, is funded, or is accepted, it is the sponsor's. The sponsor champions the project with the center's staff and with the branch managers.

---

### 2B. PROJECT CHARTER form

*The printed four-page form, pages 16 to 19 of A Project Manager's Book of Forms, 3rd edition. Field names and field order are reproduced exactly as printed. Highlighted content is assumed rather than given; empty boxes are fields that cannot be completed until signing.*

#### PROJECT CHARTER, page 1 of 4

| Field | Content |
| --- | --- |
| **Project Title** | Development and Deployment of a Learning Center Management Software. Product name: <mark>not yet decided</mark> |
| **Project Sponsor** | <mark>Dr. Nguyễn Mạnh Hùng</mark> |
| **Date Prepared** | 2 September 2026 |
| **Project Manager** | |
| **Project Customer** | <mark>Đỗ Thị Bích Ngọc, owner and Director of the learning center: 3 branches, 1,200 active students, 35 teachers</mark> |

| Field | Content |
| --- | --- |
| **Project Purpose** | The center operates on paper registers, Excel workbooks, and a group-chat channel. This costs about <mark>60 staff-hours a month</mark> in duplicate data entry, causes recurring room and teacher double-booking, and leaves about <mark>8% of tuition</mark> past its due date because no reliable debt list exists. The project removes that operational loss and gives the Director one current view of enrollment, revenue, and teaching capacity across the three branches, which is a precondition for the <mark>fourth branch planned for 2027</mark>. Quantified business case in section 2A: recurring benefit 104,400,000 VND a year, one-off release 360,000,000 VND, payback in the fourth year. |
| **High-Level Project Description** | Analyse, design, build, test, and deploy a Vietnamese-language web application covering the full operating cycle of the center: courses, classes and scheduling, students and enrollment, attendance, tuition and payments, teachers and teaching-hour payroll, assessment, notification, and management reporting. Includes migration from the current Excel files, staff training, and one month of warranty after go-live. Iterative delivery: two build iterations, each closing with a demo, then user acceptance testing on the whole system. Five staff, five months, 700,000,000 VND. |
| **Project Boundaries** | **Included:** functions F01 to F11 and the exception behaviour of section 1.1.5, for the school-age learners of the three existing branches; migration of the two most recent terms; deployment on one cloud virtual server with a staging environment; training; documentation; one month of warranty. **Excluded:** native mobile applications; online teaching, video, and e-learning content; payment gateway and e-wallet integration; accounting, tax, and social-insurance integration; attendance hardware and any hardware procurement; multi-tenant operation for other centers; preschool learners; data older than the two most recent terms; support after the warranty month. Project exclusions: subscriptions beyond 12 months, cleaning of the source data, staffing and organisation of the center, operation after handover, parent training beyond the user guide. Adding a fourth branch of this customer is not excluded, since branches are configuration data in F11. The project ends at the closeout meeting after the warranty month; operation and hosting then pass to the center. |
| **Key Deliverables** | D1 Approved requirement specification. D2 Design baseline: architecture, database schema, UI design. D3 Iteration 1 release, F01 to F05. D4 Iteration 2 release, F06 to F11. D5 Test documentation and test summary report. D6 Migrated and reconciled production data. D7 Production deployment with backup configured and a restore tested. D8 User manual, administrator and deployment guide, trained staff with a training record. D9 Source code, database scripts, technical documentation. D10 Closeout report and lessons learned. |
| **High-Level Requirements** | One integrated database, with the same data never entered in two places. Room, teacher, and student timetable conflicts detected and blocked when a class or session is created or moved. Tuition invoices generated from the course fee and the discount policy, with outstanding debt visible per student, class, and branch. Teaching hours derived from recorded attendance and exportable for payroll. Automatic notification of reminders, absence, tuition due, and results, with a delivery log; internal announcements and parent messages in the same channel. Role-based access for the seven roles, with an audit trail on all financial and student data. Vietnamese interface usable after half a day of training. Acceptance criteria A01 to A11 of section 1.3 met, covering functional completeness, performance, capacity, security, auditability, availability, degraded operation, usability, compatibility, maintainability, and data ownership. |
| **Overall Project Risk** | **Medium.** Technology and domain are well understood, but budget and end date are both fixed, and the five-month window must contain delivery *and* a full warranty month, leaving analysis, design, and test about one week of float each. The five-person team is small enough that losing one developer moves the critical path; the project manager is also the business analyst; the customer staff who own the business rules are only part-time available. Dominant uncertainty: volatility of tuition, discount, and refund policy, which is a management decision of the center. Largest single exposure: go-live itself, with three branches switching over on one day, mid-term, four weeks before the Lunar New Year break, which can absorb no overrun. Risks R1 to R10 carry named responses and are covered by a 70,000,000 VND management reserve. |

#### PROJECT CHARTER, page 2 of 4

| | Project Objectives | Success Criteria |
| --- | --- | --- |
| **Scope** | Deliver the eleven functions F01 to F11 and the ten deliverables D1 to D10 for the three branches. | 100% of F01 to F11 accepted in UAT; all ten deliverables signed off by the sponsor; no function deferred without an approved change request. |
| **Time** | Go live by <mark>5 January 2027</mark> and close the project by <mark>5 February 2027</mark>, within the five-month window starting <mark>14 September 2026</mark>, with the full warranty month contained inside that window. | Go-live on or before 5 January 2027; no milestone M1 to M7 more than 1 week later than baseline; the warranty period runs its full 31 days before closeout. |
| **Cost** | Deliver the whole scope within the preapproved 700,000,000 VND, including software, deployment, migration, training, and warranty. | Final cost at or below 700,000,000 VND; cost variance at each stage gate within plus or minus 5% of baseline; management reserve use reported monthly. |
| **Other** | **Quality:** a system fit for daily operation from the first day. **Stakeholder satisfaction:** the center runs its daily operation on the system, not on spreadsheets. | At least 95% of UAT test cases passed; no open Critical or High defect at go-live; at most 5 open Medium defects, each with an agreed fix date and none in the tuition, payment, or teaching-hour path. At least 80% of the <mark>52 staff users</mark> trained and active in the first month, including at least 90% of the 17 administrative users and 75% of the 35 teachers; average user satisfaction at least 4 of 5 in the closeout survey; at least 90% of classes with attendance recorded in the system during the warranty month. |

| Summary Milestones | Due Date |
| --- | --- |
| M0 Project kickoff, charter approved, team mobilised | <mark>Mon 14 Sep 2026</mark> |
| M1 Requirement specification approved and baselined | <mark>Fri 2 Oct 2026</mark> |
| M2 Design baseline approved: architecture, database schema, UI design | <mark>Fri 16 Oct 2026</mark> |
| M3 Iteration 1 demo accepted: F01 to F05 | <mark>Fri 13 Nov 2026</mark> |
| M4 Iteration 2 accepted, feature complete: F06 to F11 | <mark>Fri 11 Dec 2026</mark> |
| M5 System test complete, UAT entry criteria met | <mark>Fri 18 Dec 2026</mark> |
| M6 UAT signed off, data migrated, go-live and handover | <mark>Tue 5 Jan 2027</mark> |
| M7 Warranty complete, project closeout | <mark>Fri 5 Feb 2027</mark> |

M6 to M7 is the one-month warranty period. Go-live falls on a Tuesday so that live operation begins with two fully staffed working days. One branch pilots F01 to F06 for the two weeks before M6, and the spreadsheets run in deliberate parallel for two weeks after go-live.

#### PROJECT CHARTER, page 3 of 4

| Field | Content |
| --- | --- |
| **Preapproved Financial Resources** | Total **700,000,000 VND** from the center's <mark>2026 to 2027 capital budget</mark>, released against milestone acceptance: <mark>20% at M0, 25% at M3, 30% at M4, 25% at M6</mark>. Breakdown: personnel, 25 person-months, 490,000,000 (70%); infrastructure and licences, 70,000,000 (10%); deployment, migration, training, documentation, 70,000,000 (10%); management reserve, 70,000,000 (10%). No further funding is committed; an increase requires the sponsor's written approval. |

| Stakeholder(s) | Role |
| --- | --- |
| <mark>Dr. Nguyễn Mạnh Hùng</mark> | Sponsor: authorises the project and this charter, releases the funding, approves scope changes, gives final acceptance |
| <mark>Đỗ Thị Bích Ngọc</mark>, owner and Center Director | Customer: owns the business need, commits the center's staff and data, takes the system into daily operation |
| Academic Manager | Business owner for courses, classes, scheduling, assessment; main requirement source and UAT lead |
| Accountant | Business owner for tuition, debt, and teaching-hour payroll; owner of the tuition benefit; UAT participant |
| Front-desk / Admissions supervisor | Business owner for enrollment and payment recording; represents the daily users |
| Head Teacher, teacher representative | Represents the 35 teachers for attendance, scores, and teaching-hour screens |
| Students and parents | End users of schedule, result, and tuition views; recipients of notifications |
| Center IT administrator | Receives the system at handover; operates accounts, backup, and hosting afterwards |
| Project Manager | Plans, executes, and controls the project; single point of contact for the sponsor |
| Development team, 3 developers and 1 QA engineer | Analysis, design, build, test, deployment, documentation |
| SMS and email gateway provider | External supplier of the notification channel |
| Cloud hosting provider | External supplier of the production and staging environment |

| Field | Content |
| --- | --- |
| **Project Exit Criteria** | 1. All deliverables D1 to D10 accepted in writing by the sponsor. 2. UAT signed off with at least 95% of test cases passed and no open Critical or High defect. 3. System running in production with backup verified by a successful restore test. 4. Production data migrated and reconciled, with any differences accepted in writing by the Accountant. 5. At least 80% of the <mark>52 staff users</mark> trained, evidenced by the training record. 6. Source code, database scripts, user manual, and administrator guide handed over and acknowledged. 7. The warranty month ended with no open Critical or High defect. 8. Paper fallback procedure and full data export both demonstrated to the center and in its hands. 9. A written decision taken on support after the warranty month. 10. Closeout report, lessons learned, and final financial reconciliation approved, and the final invoice settled. Early closure by sponsor decision, on withdrawn funding or lost business need, hands over the completed deliverables and closes the project with a termination report. |

| Project Manager Authority Level | |
| --- | --- |
| **Staffing Decisions** | Assigns and re-assigns work within the approved five-person team, approves leave, and manages day-to-day performance. May request replacement of a team member, with the sponsor notified. Hiring, firing, and contractual employment decisions remain with the supplier's line management. |
| **Budget Management and Variance** | Commits and spends within the approved baseline, including <mark>single transactions up to 20,000,000 VND</mark> and use of the 70,000,000 VND management reserve against risks R1 to R10. Manages cumulative cost variance up to 5% of baseline. Escalates to the sponsor any forecast overrun beyond 5%, <mark>any reserve use beyond 40,000,000 VND</mark>, and any change in total funding. |

#### PROJECT CHARTER, page 4 of 4

| Field | Content |
| --- | --- |
| **Technical Decisions** | Full authority over architecture, technology stack, database design, coding standards, tooling, and the internal delivery approach, provided that acceptance criteria A01 to A11 and the agreed deliverables are met. Decides the content of each iteration within the approved scope. Any decision that changes user-visible scope, the schedule, or the cost goes to the sponsor through the change process. |
| **Conflict Resolution** | Resolves conflicts within the project team and between the team and the center's operational staff, including competing claims on staff availability. Conflicts that cross organisations, alter agreed scope, or remain unresolved after <mark>five working days</mark> are escalated to the sponsor, whose decision is final. Disputes with external suppliers follow the applicable service agreement. |
| **Sponsor Authority** | <mark>Dr. Nguyễn Mạnh Hùng</mark> authorises the project and this charter, releases the 700,000,000 VND, and appoints the project manager. Approves changes to scope, schedule, and budget beyond the project manager's authority; sets acceptable variance limits; resolves conflicts escalated by the project manager; accepts the deliverables; authorises go-live and project closure; champions the project with the center's staff and branch managers. The customer, <mark>Đỗ Thị Bích Ngọc</mark> as owner and Center Director, is a separate authority: she owns the business need, makes the center's staff and data available, nominates the business owners who sign for their own areas, and confirms at closeout that the center is operating on the system. |

**Approvals**

| | Project Manager | Sponsor or Originator |
| --- | --- | --- |
| **Signature** | | |
| **Name** | | <mark>Dr. Nguyễn Mạnh Hùng</mark> |
| **Date** | | |

The printed form carries a signature, a name, and a date for the Project Manager and for the Sponsor or Originator. The project manager is <mark>appointed by the sponsor at M0</mark> and is therefore not yet named, so that box is left empty, as are all signature and date boxes, which are completed on signing.

---

## Part 3: Prompt Log

*This part answers point 4 of the team assignment: every prompt version used to produce this document, an assessment of what each version produced, and the reason each one had to be replaced.*

The pattern across the versions is consistent. Prompts that described the *document* produced fluent text that was wrong in checkable ways. Prompts that described the *constraints and the source* produced text that could be verified. The largest single gain came from asking for an adversarial audit rather than asking for more content. The largest single loss came from a rewrite that improved the prose and silently deleted two graded sections.

### 3.1 Version history

| V | Intent | Quality of the result | Why it was replaced |
| --- | --- | --- | --- |
| V1 | Get a first draft of anything usable | Generic and unusable. Read like a textbook chapter about charters rather than a charter for this project. | No project constraints in the prompt, so nothing was anchored |
| V2 | Anchor the draft in the assignment's real numbers | Correct scale, still shapeless. The function list appeared and was reasonable. | Structure came from the model's habits, not from the prescribed form |
| V3 | Force the structure of the Book of Forms | Right structure, prose too vague to check. Success criteria were adjectives, not numbers. | Vague success criteria are unmarkable; measurable values were needed |
| V4 | Make every claim measurable and produce the Vietnamese version | Fluent, complete-looking, internally inconsistent. | Fluency masked four contradictions that no generative prompt would surface |
| V5 | Find the errors instead of adding content | Highest-value prompt of the set. Found a schedule that contradicted its own warranty. | Audit only: the fixes still had to be requested |
| V6 | Apply every finding to both languages at once | Produced version 2.0 | Left the printed form unverified against the book |
| V7 | Close the open item from V6 by checking the form against the book | Confirmed the field set and found one layout error | Verification only, no content change |
| V8 | Cross-check the charter against a second published template | Exposed two content gaps, both filled | Comparison only, no format change |
| V9 | Read the document as the paying customer, not as a marker | One arithmetic correction and seven additions | Content complete; presentation then rewritten |
| V10 | Rewrite the English file as clean, pure Markdown | Better prose, and a serious regression: two graded sections deleted | Dropped the filled form and the prompt log, failing assignment points 2, 3 and 4 |
| V11 | Grade against the brief, then restore what V10 removed | Produced this version | Current |

### 3.2 The prompts

#### V1: first draft

> Write a project charter for a learning center management software project.

**Quality: poor.** Roughly 600 words of generic material: "the project will deliver value to stakeholders", milestones named "Phase 1" through "Phase 4", no figures. Nothing in it was specific enough to be either right or wrong.

**Why replaced:** the prompt contained no budget, no duration, no team size, and no customer. With nothing to anchor to, the output described the *idea* of a charter instead of this project.

#### V2: constraints added

> Write a project charter for "Development and Deployment of a Learning Center Management Software". Budget 700 million VND, duration 5 months, team of 5. The customer is a private after-school learning center. Include a requirement specification with a list of functions and a description of each function.

**Quality: fair.** The numbers propagated correctly and the eleven functions F01 to F11 appeared here in close to their final form. This part of the output survived to the current version almost unchanged. But the charter section was a flat sequence of headings chosen by the model.

**Why replaced:** the assignment does not ask for *a* charter, it asks for the charter form from a named book. Structure invented by the model scores nothing against a prescribed template.

#### V3: structure imposed

> Use the charter elements of Table 1.1 of A Project Manager's Book of Forms (3rd edition), then reproduce the four-page PROJECT CHARTER form itself and fill it in. Keep the requirement specification as Part 1 and the charter as Part 2.

**Quality: good structurally, weak in content.** Both the element list (2A) and the four-page form (2B) appeared, correctly separated. But the content stayed soft: the quality objective read "deliver a high-quality system", and the exit criteria read "the customer is satisfied".

**Why replaced:** unmeasurable criteria cannot be assessed by a marker, and they hide risk. "The customer is satisfied" has no failure condition.

#### V4: measurability and the Vietnamese version

> Every success criterion must be a number with a threshold and a measurement point. Add a risk register with responses, a milestone schedule with real dates, and a cost breakdown that sums exactly to 700 million VND. Then produce a Vietnamese version with identical structure, same headings, same table rows, so the two files diff cleanly.

**Quality: high on the surface, and this is the important entry in the log.** Everything asked for arrived: the budget reconciled exactly (490 + 70 + 70 + 70 = 700), the milestones all landed on Fridays, the risk register had real responses, and the two language files matched line for line.

It was also wrong in four ways that no amount of re-reading it as a *reader* would surface:

1. The document promised a one-month warranty and scheduled seven days for it.
2. It claimed six user roles and listed seven.
3. It set a training target of 25 staff users at a center it had already given 35 teachers.
4. It specified 50 concurrent users for a system whose own role table gives 1,200 students and their parents a login.

**Why replaced:** this is the failure mode worth recording. The prompt asked for internal consistency and the output *looked* internally consistent. Generative prompts optimise for a document that reads well; they do not cross-check a claim in one section against a table in another. Asking the same prompt again, or asking "check your work", reproduces the same blind spots because the same reading process produced them.

#### V5: audit instead of generation

> Do a deep audit of the document, scoped to a year-4 university assignment. Check every number against every other number. Check the schedule arithmetic against the stated durations. List what contradicts what, ranked by how likely a marker is to notice, and say what you could not verify.

**Quality: the highest-value prompt in the set.** It produced no new document text at all, and it found all four contradictions above, plus a missing Table 1.1 element and two soft numbers.

Three things made it work, and they generalise:

- **It asked for contradictions, not improvements.** "Improve this" returns more prose. "What contradicts what" returns a list of defects.
- **It named the audience.** "Year-4 assignment" set the bar at what a marker actually checks, being countable claims, arithmetic, and dates, rather than at industrial project management.
- **It required an admission of ignorance.** Asking what could *not* be verified surfaced that the charter form had never been compared against the book, which had been silently assumed since V3.

**Why replaced:** an audit produces findings, not fixes. Applying them was a separate step, deliberately kept separate so that the findings could be reviewed before anything was rewritten.

#### V6: apply the findings

> Fix all of them, then refine.

**Quality: adequate, because V5 had already done the thinking.** The prompt is short only because the audit it depends on was specific. The same three words issued after V4, with no audit in between, would have produced another fluent revision of the same broken schedule.

Applied in this version: the schedule was re-baselined so that go-live moved from 29 January to 5 January 2027 and the warranty month became real; six versus seven roles was corrected in three places per language; the training base became 52 with a stated composition; the performance figure was split into a staff figure and a parent-portal figure; the missing *project approval requirements* element was added to section 2A; and the yellow-highlight convention was applied to the assumed figures instead of being declared and left unused.

**Why replaced:** it closed every finding except one. V5 had reported that the four-page form in 2B was reconstructed from the element list and had never been read field by field from pages 16 to 19. That item was carried forward as explicitly open.

#### V7: verify the form against the book

*The verbatim prompt for this version was not recorded at the time. Its effect is documented in the repository README.*

**Quality: verification only, and it closed the item V6 left open.** Section 2B was compared field by field against pages 16 to 19 of the book. The field set matched. One layout error was found and corrected: the printed page 1 pairs **Project Sponsor** with **Date Prepared** and **Project Manager** with **Project Customer**, whereas the document had paired Title with Date Prepared and Sponsor with Customer.

**Why replaced:** verification changes no content. The next question was whether the charter's *content* was complete, not whether its layout matched.

#### V8: cross-check against a second template

*The verbatim prompt for this version was not recorded at the time. Its effect is documented in the repository README.*

**Quality: useful as a gap finder, correctly rejected as a format.** The document was compared against the worked charter example in Rita Mulcahy's *PMP Exam Prep*, which uses a different section list. Section 2B was deliberately **not** rewritten into that template: the assignment names the Book of Forms, and the fourteen elements of section 2A already match PMBOK 6 section 4.1.3.1. The comparison exposed two genuine content gaps, both filled: a quantified **business case** and an explicit **resources preassigned** statement.

**Why replaced:** the comparison was against a marker's checklist. It had not been read from the customer's point of view.

#### V9: read it as the customer

*The verbatim prompt for this version was not recorded at the time. Its effect is documented in the repository README.*

**Quality: one correction and seven additions, and the correction mattered most.** V8 had counted the release of overdue tuition (360,000,000 VND) as a *recurring annual* benefit and claimed payback in under two years. It is a stock, not a flow: cutting overdue tuition from 8% to 3% releases the money **once**, and only the carrying cost and the avoided write-off recur. Corrected to a recurring benefit of about 104,400,000 VND a year, a one-off release of 360,000,000 VND, and payback in the fourth year. The document states the error rather than quietly swapping the number.

Also added: the exception requirements now in section 1.1.5; degraded operation and data ownership as acceptance criteria; the warranty response matrix; R9 for go-live failure and R10 for an unrealised benefit; the UAT failure path with three named options; and a fix to a scope contradiction where the exclusions read as if a fourth branch were out of scope while the fourth branch was the stated reason for buying the system.

**Why replaced:** the content was now complete, but the file still carried print-format HTML from the retired PDF pipeline. The next prompt targeted presentation.

#### V10: rewrite as clean Markdown

*Committed as `6421d5d`, "feat: new eng md version".*

**Quality: better prose, and the worst regression in the log.** The rewrite genuinely improved the document as prose: it dropped the `<div>` wrappers and HTML tables, renumbered the sections onto form 2.8 for Part 1, and consolidated every assumed figure into one table.

It also deleted two graded sections without saying so:

1. **Section 2B, the filled four-page form**, together with all 71 yellow markers. This is the artefact that assignment points 2 and 3 actually ask for.
2. **Part 3, the prompt log**, which is the whole of team assignment point 4.

The result read better and scored far worse. Graded against the general requirement it came to 49 out of 100: full marks on the requirement specification, partial marks on the charter because the element list from pages 13 to 15 had been substituted for the prescribed form on pages 16 to 19, and zero on the fill-in-the-form requirement because no form remained in the file. It also left a dangling reference in its own introduction, telling the reader that consolidating the assumptions made "filling the printed form (point 3)" easier, while containing no printed form.

**Why replaced:** a rewrite that optimises for how a document reads will happily delete a section that exists only because a rubric asks for it. Prose quality and rubric coverage are different objectives, and nothing in the prompt protected the second one.

#### V11: grade first, then restore

> Read the general requirement and the team requirement, and check whether the document follows them. Grade the current charter document against the general requirement as an ultra strict lecturer.

**Quality: the grading step is what made the regression visible.** Asking for a grade against the brief, rather than for a cleanup, surfaced the two missing sections immediately. The cleanup that had been requested first would have polished a document that was failing two of the three graded requirements, and would not have revealed why.

Applied in this version: section 2B restored and, for the first time, written directly from the field list extracted from pages 16 to 19 of the book rather than reconstructed from the element list; Part 3 restored and extended to V11; the yellow convention reapplied across both parts and explained at the top; the project manager name and the signature and date fields left deliberately empty, per the instruction to leave a box empty when its content is not known; the dangling reference to point 3 resolved; and the em dashes, minus signs, and plus-or-minus signs removed to satisfy the project's own writing rules.

**Why current:** the document now answers all four points of the assignment in the prescribed form.

### 3.3 What the sequence shows

| Lesson | Evidence from this log |
| --- | --- |
| Constraints beat instructions | V1 to V2: adding four numbers did more than any amount of "be detailed" |
| Name the source, do not describe it | V2 to V3: "Table 1.1 of the Book of Forms" produced the right structure immediately |
| Demand thresholds, not adjectives | V3 to V4: "a number with a threshold and a measurement point" removed every unmarkable criterion |
| Fluency is not correctness | V4: the most polished version was the one with four contradictions in it |
| Auditing is a different task from writing | V5: found in one pass what four generative prompts had accumulated |
| Ask what could not be verified | V5 to V7: surfaced that the printed form had never been checked, and V7 then checked it |
| Verify against the source, not against a memory of it | V11: the form was finally built from text extracted from pages 16 to 19, not from the element list |
| A rewrite is not a safe operation | V10: deleted two graded sections while improving the prose, and said nothing |
| Grade before polishing | V11: a request to clean up would have preserved a failing structure |

**Still open.** Nothing in the English file. The Vietnamese file `charter-package.vi.md` is a translation of version 2.0 and carries none of the changes from V7 onward. If a Vietnamese deliverable is required, it should be retranslated from this file rather than patched.
