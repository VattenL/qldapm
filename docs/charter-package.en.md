<div class="cover" markdown="1">

# LEARNING CENTER MANAGEMENT SOFTWARE

<div class="subtitle">Requirement Specification &amp; Project Charter</div>

<table>
<tr><td>Project</td><td>Development and Deployment of a Learning Center Management Software</td></tr>
<tr><td>Product name</td><td><mark>[product name — to be decided]</mark></td></tr>
<tr><td>Budget</td><td>700,000,000 VND (700 million VND)</td></tr>
<tr><td>Duration</td><td>5 months — 14 Sep 2026 to 05 Feb 2027</td></tr>
<tr><td>Team size</td><td>5 full-time staff (PM/BA, 3 developers, 1 QA)</td></tr>
<tr><td>Customer</td><td>Đỗ Thị Bích Ngọc — owner and director of the learning center</td></tr>
<tr><td>Document version</td><td>1.0</td></tr>
<tr><td>Date prepared</td><td>02 September 2026</td></tr>
</table>

</div>

<p class="note">Scope of this document: Part 1 covers the short requirement specification; Part 2 covers the project charter, first as the element list of Table 1.1 of <em>A Project Manager's Book of Forms</em> (3rd ed.), then as the four-page PROJECT CHARTER form itself. The customer name and all figures are assumptions made for this academic exercise and are listed in section 1.7.</p>

<div class="pagebreak"></div>

## Part 1 — Requirement Specification (short version)

### 1.1 Product description

The customer, Đỗ Thị Bích Ngọc, owns and runs a private after-school learning center with about 1,200 active students, 35 teachers, and 3 branches in the same city. It teaches English, mathematics, and IT skills in fixed-length courses of 24 to 48 sessions. Today the center runs on paper registers, spreadsheets, and a group-chat channel: enrollment lists live in Excel, attendance is taken on printed sheets, tuition debt is tracked by the accountant in a separate workbook, and parents are informed by manual messages. The result is duplicated data entry, room and teacher double-booking, tuition collected late, and no reliable view of revenue or class fill rate.

The system (product name <mark>[product name — to be decided]</mark>) is a web application that replaces those spreadsheets with one shared database covering the full operating cycle of the center: course catalog, class opening and scheduling, student enrollment, attendance, tuition and payment, teacher records and teaching-hour payroll, assessment, parent notification, and management reporting. It is used from a desktop browser by center staff and from a phone browser by teachers and parents.

The project delivers the software, deploys it on a cloud server for the center, migrates the current student and course data, trains the staff, and supports the center through one month of warranty after go-live.

### 1.2 Scope

**In scope**

- A responsive web application covering the eleven functions listed in section 1.4, in Vietnamese, for the three existing branches.
- A relational database as the single source of truth for students, courses, classes, sessions, attendance, invoices, payments, and teaching hours.
- Role-based access for six user roles (section 1.3).
- Migration of current data from the center's Excel files: student profiles, course catalog, active classes, and outstanding tuition balances.
- Outbound notification to parents and teachers by email and SMS through one third-party gateway.
- Deployment on a cloud virtual server, including domain, HTTPS, and automated nightly backup.
- User manual, administrator/deployment guide, on-site training for center staff, and source-code handover.
- One month of warranty (defect correction) after go-live.

**Out of scope**

- Native mobile applications for iOS or Android. The web UI is responsive; no app-store deliverable.
- Online teaching features: live video class, content authoring, quiz engine, e-learning material streaming.
- Automated online payment gateway or e-wallet integration. The system records payments and reconciles bank-transfer references manually; it does not initiate or capture card payments.
- Integration with accounting or tax software, tax declaration, and social-insurance reporting. The system computes teaching-hour payroll figures and exports them; the accountant posts them elsewhere.
- Biometric or card-reader attendance hardware, and any hardware procurement.
- Multi-tenant SaaS operation for other centers, and any franchise-level consolidation beyond the three branches of this customer.
- Migration of historical data older than the two most recent terms.

### 1.3 Users and roles

| Role | Who they are | Main use of the system |
| --- | --- | --- |
| Center Director | Owner / sponsor | Dashboards, revenue and enrollment reports, approvals |
| Academic Manager | Runs the teaching operation | Course catalog, opening classes, scheduling, teacher assignment, assessment oversight |
| Front-desk / Admissions staff | Reception counter | Student profiles, enrollment, invoices, payment recording, parent enquiries |
| Teacher | Teaching staff | Class roster, attendance, scores, own teaching-hour sheet |
| Accountant | Finance | Tuition debt tracking, payment confirmation, teaching-hour payroll figures, financial reports |
| Student / Parent | End customer | Personal schedule, attendance and score history, tuition balance, notifications |
| System Administrator | IT staff of the center | Accounts, roles, configuration, backup, audit log |

### 1.4 Function list

<div class="fnlist" markdown="1">

| ID | Function | Primary actor | Description |
| --- | --- | --- | --- |
| F01 | Authentication and access control | System Administrator | Account creation, login with username/password, password reset, session timeout, and role-based permission so each role sees only its own screens and data. Every account belongs to exactly one role and, for staff, to one or more branches. |
| F02 | Student profile and enrollment | Front-desk staff | Records a student profile (personal data, guardian and contact details, source of lead, notes) and enrolls the student into an opened class. Handles transfer between classes, reservation, withdrawal with refund calculation, and prevents enrollment when the class is full or the schedule collides with another class of the same student. |
| F03 | Course and curriculum catalog | Academic Manager | Defines the course offering: course code, level, number of sessions, session length, standard tuition fee, prerequisite course, and syllabus outline per session. Courses are versioned so classes opened earlier keep the definition they were opened with. |
| F04 | Class opening, scheduling, and assignment | Academic Manager | Opens a class from a course (branch, start date, weekly time slots, capacity), generates the full session calendar, and assigns a room and a teacher to each session. Detects and blocks conflicts on room, teacher, and class time; supports session postponement and re-scheduling with automatic recalculation of the calendar. |
| F05 | Attendance and make-up sessions | Teacher | Marks each student of a session as present, absent with notice, absent without notice, or late, with an optional remark. Supports registering a make-up session in another class for an absent student and shows the attendance rate per student and per class. |
| F06 | Tuition, invoicing, and debt tracking | Front-desk staff / Accountant | Generates a tuition invoice on enrollment from the course fee, applying discount policies (sibling, early payment, referral, promotion code) and installment plans. Records cash and bank-transfer payments against invoices, issues receipts, and maintains the outstanding balance and an aged debt list per student, class, and branch. |
| F07 | Teacher records and teaching-hour payroll | Accountant | Keeps teacher profiles, qualifications, contract type, and pay rate per teaching hour by course level. Aggregates taught sessions from F05 into a monthly teaching-hour sheet per teacher, applies allowances and deductions, and exports the payroll figures to Excel for the accountant. |
| F08 | Assessment and progress reports | Teacher | Records scores for the assessment items defined by the course (quizzes, midterm, final, skill scores) and comments per student. Computes the final result and pass/fail against the course rule, and produces a printable progress report per student and a result summary per class. |
| F09 | Notification to parents and teachers | Front-desk staff | Sends email and SMS messages from templates for the events that matter: enrollment confirmation, session reminder, absence alert, tuition due and overdue, schedule change, and result published. Supports manual send to a selected group, scheduled automatic send, and a log of every message with its delivery status. |
| F10 | Reports and management dashboard | Center Director | Provides the management view: revenue and collection by period and branch, outstanding debt, new and retained student counts, class fill rate, teacher workload and teaching hours, and attendance rate. Every report is filterable by period, branch, and course, and exportable to Excel and PDF. |
| F11 | System administration and audit | System Administrator | Manages the reference data and configuration of the center (branches, rooms, terms, fee and discount policies, notification templates, holidays), triggers and restores backups, and keeps an audit log of every create, update, and delete on financial and student data with user and timestamp. |

</div>

### 1.5 Non-functional requirements

| ID | Category | Requirement |
| --- | --- | --- |
| N01 | Performance | Any screen responds within 3 seconds at 50 concurrent users; a report over one term is produced within 10 seconds. |
| N02 | Capacity | The system holds at least 5,000 student records, 200 classes per term, and 3 years of session history without redesign. |
| N03 | Security | HTTPS only; passwords stored with a salted one-way hash; permission enforced on the server side for every request; personal data of students handled in line with Decree 13/2023/ND-CP on personal data protection. |
| N04 | Auditability | Create, update, and delete on financial and student records are written to an immutable audit log kept for at least 3 years. |
| N05 | Availability | 99% availability between 07:00 and 22:00 local time; automated nightly backup with recovery point objective 24 hours and recovery time objective 4 hours. |
| N06 | Usability | Vietnamese user interface; the daily tasks (attendance, payment recording, enrollment) reachable within 3 clicks from the home screen; usable by staff after a half-day of training. |
| N07 | Compatibility | Latest two versions of Chrome, Edge, and Firefox on desktop; responsive layout usable on a tablet and on a phone for the teacher and parent screens. |
| N08 | Maintainability | Layered architecture, coding convention applied, deployment guide and database schema documentation delivered with the source code. |

### 1.6 Technical approach

The system is built as a web application with a layered server-side architecture and a relational database, deployed as a single application instance and a database instance on one cloud virtual server, with a second environment for staging and UAT. The delivery method is iterative: two build iterations of four to five weeks, each ending in a demo to the customer, followed by user acceptance testing on the complete system. Requirements are baselined at the end of the analysis phase; later changes go through the change process defined in the charter.

### 1.7 Assumptions and constraints

**Constraints**

- Budget is fixed at 700,000,000 VND, including software, deployment, training, and warranty.
- Duration is fixed at 5 months, from 14 September 2026 to 05 February 2027, with go-live required before the Lunar New Year break.
- The team is 5 full-time staff; no additional headcount is available.
- The system must be in Vietnamese and must run on the customer's existing cloud budget of one virtual server.

**Assumptions**

- The customer's center (1,200 students, 35 teachers, 3 branches) and all figures in this document are assumed for this academic exercise; no real customer data is used.
- The commercial product name is not decided yet; every place that needs it is marked in yellow and filled in a later version of this document.
- The Academic Manager and the Accountant are available at least 4 hours per week for requirement workshops, demos, and UAT.
- The center's current Excel files are usable as the migration source and are cleaned by the center before migration.
- One third-party SMS/email gateway account is provided and paid for by the center; its API is stable and documented.
- Business rules for discounts and refunds are confirmed during the analysis phase and frozen at the requirement sign-off milestone.
- No public holiday other than the Lunar New Year break of February 2027 affects the schedule materially.

<div class="pagebreak"></div>

## Part 2 — Project Charter

### 2A. Charter elements (Table 1.1 of the Book of Forms)

#### Project purpose

The center's manual, spreadsheet-based operation costs about 60 staff-hours per month in duplicated data entry, causes recurring room and teacher double-booking, and leaves roughly 8% of tuition uncollected past due date because no one has a reliable debt list. The project is undertaken to remove that operational loss and to give the Director a single, current view of enrollment, revenue, and teaching capacity across the three branches, as required by the center's plan to open a fourth branch in 2027.

#### High-level project description

Analyze, design, build, test, and deploy a Vietnamese-language web application that manages the full operating cycle of a learning center — courses, classes and scheduling, students and enrollment, attendance, tuition and payments, teachers and teaching-hour payroll, assessment, parent notification, and management reporting — together with data migration from the center's current Excel files, staff training, and one month of post-go-live warranty. Delivery is iterative, in two build iterations followed by user acceptance testing, by a team of 5 within 5 months and 700 million VND.

#### Project boundaries

Included: the eleven functions F01–F11 of section 1.4 for the three existing branches, data migration of the two most recent terms, deployment on one cloud virtual server, training, documentation, and one month of warranty.

Excluded: native mobile apps; online teaching, video, and e-learning content; automated payment gateway or e-wallet integration; accounting, tax, and social-insurance integration; attendance hardware and any hardware procurement; multi-tenant operation for other centers; historical data older than two terms.

The project ends at the closeout meeting after the warranty month; ongoing operation and hosting of the system are the center's responsibility.

#### Key deliverables

| # | Deliverable | Delivered at |
| --- | --- | --- |
| D1 | Software requirement specification, approved and baselined | M1 |
| D2 | Design baseline: architecture, database schema, UI design | M2 |
| D3 | Iteration 1 release: F01–F05 (access control, students, courses, scheduling, attendance) | M3 |
| D4 | Iteration 2 release: F06–F11 (tuition, payroll, assessment, notification, reports, administration) | M4 |
| D5 | Test documentation: test plan, test cases, defect log, test summary report | M5 |
| D6 | Migrated production data, verified against the source files | M6 |
| D7 | Production deployment on the cloud server, with backup configured | M6 |
| D8 | User manual, administrator and deployment guide, trained staff (training record) | M6 |
| D9 | Source code, database scripts, and technical documentation handed over | M6 |
| D10 | Warranty period completed, closeout report and lessons learned | M7 |

#### High-level requirements

- The system manages the eleven functional areas F01–F11 of section 1.4 as one integrated database, with no re-entry of the same data in two places.
- Room, teacher, and student schedule conflicts are detected and blocked at the moment a class or session is created or moved.
- Tuition invoices are generated from the course fee and discount policy, and outstanding debt is visible per student, class, and branch at any time.
- Teaching hours are derived from recorded attendance, not entered by hand, and exportable for payroll.
- Parents and teachers are notified automatically for reminders, absence, tuition due, and results, with a delivery log.
- Each of the six user roles sees only the data and screens its role permits, and every financial or student-data change is auditable.
- The interface is in Vietnamese and usable by existing staff after a half-day of training.
- Non-functional requirements N01–N08 of section 1.5 are met.

#### Overall project risk

Overall risk is assessed as **Medium**. The technology is well understood and the domain is stable, but the budget and the go-live date are both fixed, the team is small enough that the loss of one developer moves the critical path, and the customer staff who own the business rules are only part-time available. The dominant uncertainty is requirement volatility around tuition, discount, and refund policy, which is a management decision of the center rather than a technical question. A secondary exposure is the third-party notification gateway, which the project does not control. The Lunar New Year break of February 2027 removes any schedule float after go-live.

| # | Main risk | Response |
| --- | --- | --- |
| R1 | Tuition, discount, and refund rules change after the requirement baseline | Freeze rules at M1 with written sign-off; route later changes through the change process against the 70 million VND reserve |
| R2 | Customer staff not available for workshops, demos, and UAT | Fixed weekly slot agreed with the sponsor at kickoff; escalate a missed slot to the sponsor within 2 working days |
| R3 | Loss or absence of a developer in a 5-person team | Pair on the scheduling and tuition modules; keep code and documentation in shared repositories; sponsor-approved replacement within 2 weeks |
| R4 | Third-party SMS/email gateway unstable or unexpectedly priced | Isolate the gateway behind one interface; validate with a proof of concept before M2; keep a second provider as fallback |
| R5 | Source Excel data too dirty to migrate | Data quality assessment at M1; the center cleans the files before M5; migration limited to the two most recent terms |
| R6 | Scheduling and conflict detection more complex than estimated | Build F04 first in iteration 1; timebox it and review at the M3 demo |
| R7 | Go-live slips into the Lunar New Year break | Deploy at M6, one week before the break; a slip beyond it delays go-live by three weeks and is escalated to the sponsor immediately |

#### Project objectives and related success criteria

| Objective area | Objective | Success criteria |
| --- | --- | --- |
| Scope | Deliver the eleven functions F01–F11 and the ten deliverables D1–D10 | 100% of F01–F11 accepted in UAT; all ten deliverables signed off by the sponsor |
| Time | Go live by 29 January 2027 and close the project by 05 February 2027 | Go-live on or before 29 Jan 2027; no milestone finishes more than 1 week late |
| Cost | Deliver within 700,000,000 VND | Final cost ≤ 700 million VND; cost variance at each stage gate within ±5% of the baseline |
| Quality | Deliver a system fit for daily operation | ≥ 95% of UAT test cases pass; zero open Critical or High defects at go-live; ≤ 5 Medium defects open, each with an agreed fix date |
| Stakeholder satisfaction | The center's staff can run the operation on the system | ≥ 80% of the 25 staff users trained and active in the first month; average user satisfaction ≥ 4 of 5 in the closeout survey; ≥ 90% of classes have attendance recorded in the system in the warranty month |

#### Summary milestone schedule

| ID | Milestone | Due date |
| --- | --- | --- |
| M0 | Project kickoff, charter approved | 14 Sep 2026 |
| M1 | Requirement specification approved and baselined | 02 Oct 2026 |
| M2 | Design baseline approved (architecture, database, UI) | 23 Oct 2026 |
| M3 | Iteration 1 demo accepted (F01–F05) | 20 Nov 2026 |
| M4 | Iteration 2 accepted — feature complete (F06–F11) | 25 Dec 2026 |
| M5 | System test complete, UAT entry criteria met | 15 Jan 2027 |
| M6 | UAT sign-off, data migrated, go-live and handover | 29 Jan 2027 |
| M7 | Warranty complete, project closeout | 05 Feb 2027 |

#### Preapproved financial resources

Total preapproved funding is **700,000,000 VND**, provided by the center from its 2026–2027 capital budget, released in four tranches against milestone acceptance: 20% at M0, 25% at M3, 30% at M4, 25% at M6.

| # | Cost category | Amount (VND) | Share | Basis |
| --- | --- | --- | --- | --- |
| 1 | Personnel — 5 staff × 5 months = 25 person-months | 490,000,000 | 70% | 19.6 million VND per person-month, fully loaded |
| 2 | Infrastructure and licenses | 70,000,000 | 10% | Cloud server and staging for 12 months, domain, SSL, SMS/email gateway credits, development tools |
| 3 | Deployment, data migration, training, documentation | 70,000,000 | 10% | On-site work at 3 branches, training materials, printing |
| 4 | Management reserve (contingency) | 70,000,000 | 10% | Held by the project manager against identified risks R1–R7 |
| | **Total** | **700,000,000** | **100%** | |

#### Key stakeholder list

| Stakeholder | Role in the project |
| --- | --- |
| Center Director | Sponsor; funds the project, approves the charter, scope changes, and final acceptance |
| Academic Manager | Primary business owner for courses, classes, scheduling, and assessment; key requirement source and UAT lead |
| Accountant | Business owner for tuition, debt, and teaching-hour payroll; UAT participant |
| Front-desk / Admissions supervisor | Business owner for enrollment and payment recording; represents the daily users |
| Teacher representative (Head Teacher) | Represents 35 teachers for attendance, scores, and teaching-hour screens |
| Students and parents | End users of the schedule, result, and tuition views; recipients of notifications |
| Center IT administrator | Receives the system at handover; operates accounts, backup, and hosting afterwards |
| Project Manager | Plans, executes, and controls the project; single point of contact for the sponsor |
| Development team (3 developers, 1 QA) | Analysis, design, build, test, deployment, and documentation |
| SMS / email gateway provider | External supplier of the notification channel |
| Cloud hosting provider | External supplier of the production and staging environment |

#### Project exit criteria

The project is closed when all of the following are met:

1. All deliverables D1–D10 are accepted in writing by the sponsor.
2. UAT is signed off with ≥ 95% of test cases passed and no open Critical or High defect.
3. The system runs in production on the center's cloud server with backup verified by a successful restore test.
4. Production data is migrated and reconciled against the source files, with differences accepted in writing by the Accountant.
5. At least 80% of the 25 staff users are trained, evidenced by the training record.
6. Source code, database scripts, user manual, and administrator guide are handed over and acknowledged.
7. The one-month warranty period has ended with no open Critical or High defect.
8. The closeout report, lessons learned, and final financial reconciliation are approved, and the final invoice is settled.

The project may also be closed early by decision of the sponsor if funding is withdrawn or the business need disappears; in that case the deliverables completed to date are handed over and the project is closed with a termination report.

#### Assigned project manager, responsibility, and authority level

**Project manager:** Nguyen Van A, Project Manager, assigned full-time for the full 5 months.

**Responsibility:** plan, execute, monitor, and close the project; manage scope, schedule, cost, quality, risk, and communication; lead the 5-person team; act as the single point of contact for the sponsor and the center's staff; report status weekly.

**Staffing decisions:** may assign and re-assign work within the approved 5-person team, approve leave, and manage day-to-day performance. May request the replacement of a team member; the actual hiring, firing, and contractual employment decisions remain with the vendor's line management and require the sponsor's notification.

**Budget management and variance:** may commit and spend the approved budget within the baseline, including single transactions up to 20,000,000 VND and use of the 70,000,000 VND management reserve against the identified risks R1–R7. Cumulative cost variance up to 5% of the baseline is managed by the project manager; any forecast overrun beyond 5%, any use of reserve beyond 40,000,000 VND, and any change in total funding are escalated to the sponsor for approval.

**Technical decisions:** full authority over architecture, technology stack, database design, coding standards, and the internal delivery approach, provided the non-functional requirements N01–N08 and the agreed deliverables are met. Changes that affect the user-visible scope, the schedule, or the cost require the sponsor's approval through the change process.

**Conflict resolution:** resolves conflicts within the project team and between the team and the center's operational staff. Conflicts that cross organizations, change agreed scope, or remain unresolved after 5 working days are escalated to the sponsor, whose decision is final.

#### Name and authority of the sponsor

**Sponsor:** Đỗ Thị Bích Ngọc, owner and Director of the learning center.

The sponsor authorizes the project and this charter, provides and releases the 700 million VND of funding, appoints the project manager, and makes the center's staff available. The sponsor approves changes to scope, schedule, and budget beyond the project manager's authority, sets acceptable variance limits, resolves conflicts escalated by the project manager or arising between the center's departments, accepts the deliverables, and authorizes go-live and project closure. The sponsor champions the project with the center's staff and with the branch managers.

### 2B. Project charter form

<div class="formpage">

<div class="form-title">Project Charter</div>

<table class="form">
<tr><td class="label">Project Title:</td><td>Development and Deployment of a Learning Center Management Software — product name <mark>[product name — to be decided]</mark></td><td class="label">Date Prepared:</td><td>02 September 2026</td></tr>
<tr><td class="label">Project Sponsor:</td><td>Đỗ Thị Bích Ngọc — owner and Director of the learning center</td><td class="label">Project Customer:</td><td>Đỗ Thị Bích Ngọc — the learning center (3 branches, 1,200 students, 35 teachers)</td></tr>
<tr><td class="label">Project Manager:</td><td colspan="3">Nguyen Van A — Project Manager, assigned full-time for the 5-month duration</td></tr>
</table>

<table class="form">
<tr><td class="label">Project Purpose:</td><td>The center is run on paper and spreadsheets, which costs about 60 staff-hours a month in duplicated data entry, causes recurring room and teacher double-booking, and leaves roughly 8% of tuition uncollected past due date. The project removes that operational loss and gives the Director one current view of enrollment, revenue, and teaching capacity across the three branches, as required by the plan to open a fourth branch in 2027.</td></tr>

<tr><td class="label">High-Level Project Description:</td><td>Analyze, design, build, test, and deploy a Vietnamese-language web application managing the full operating cycle of the center — courses, classes and scheduling, students and enrollment, attendance, tuition and payments, teachers and teaching-hour payroll, assessment, notification, and management reporting — with migration from the current Excel files, staff training, and one month of warranty. Iterative delivery in two build iterations plus UAT, by 5 staff, in 5 months, for 700 million VND.</td></tr>

<tr><td class="label">Project Boundaries:</td><td><strong>Included:</strong> functions F01–F11 for the three existing branches; migration of the two most recent terms; deployment on one cloud virtual server; training; documentation; one month of warranty.<br><br><strong>Excluded:</strong> native mobile apps; online teaching, video, and e-learning content; automated payment gateway or e-wallet; accounting, tax, and social-insurance integration; attendance hardware and any hardware procurement; multi-tenant use by other centers; data older than two terms.<br><br>The project ends at the closeout meeting after the warranty month; ongoing operation and hosting pass to the center.</td></tr>

<tr><td class="label">Key Deliverables:</td><td>D1 Approved requirement specification · D2 Design baseline (architecture, database, UI) · D3 Iteration 1 release (F01–F05) · D4 Iteration 2 release (F06–F11) · D5 Test documentation and test summary report · D6 Migrated and reconciled production data · D7 Production deployment with backup configured · D8 User manual, administrator guide, and trained staff · D9 Source code, database scripts, technical documentation · D10 Closeout report and lessons learned</td></tr>

<tr><td class="label">High-Level Requirements:</td><td>One integrated database with no duplicate data entry across the eleven functional areas · Conflict detection blocking room, teacher, and student schedule collisions at class and session creation · Tuition invoices generated from course fee and discount policy, with outstanding debt visible per student, class, and branch · Teaching hours derived from recorded attendance and exportable for payroll · Automatic notification of reminders, absence, tuition due, and results, with a delivery log · Role-based access for six roles and an audit trail on all financial and student data · Vietnamese interface usable after a half-day of training · Non-functional requirements N01–N08 (performance, capacity, security, audit, availability, usability, compatibility, maintainability)</td></tr>

<tr><td class="label">Overall Project Risk:</td><td><strong>Medium.</strong> Technology and domain are well understood, but budget and go-live date are both fixed and the Lunar New Year break of February 2027 removes schedule float after go-live. The 5-person team is small enough that losing one developer moves the critical path, and the customer staff who own the business rules are only part-time available. Dominant uncertainty: volatility of tuition, discount, and refund policy. Risks R1–R7 are identified with responses and covered by a 70 million VND reserve.</td></tr>
</table>

<div class="page-of">Page 1 of 4</div>

</div>

<div class="formpage">

<div class="form-title">Project Charter</div>

<table class="form">
<tr><th style="width:14%">&nbsp;</th><th style="width:43%">Project Objectives</th><th style="width:43%">Success Criteria</th></tr>

<tr><td class="label">Scope:</td><td>Deliver the eleven functions F01–F11 and the ten deliverables D1–D10 defined for the three branches.</td><td>100% of F01–F11 accepted in UAT; all ten deliverables signed off by the sponsor; no function deferred without an approved change request.</td></tr>

<tr><td class="label">Time:</td><td>Go live by 29 January 2027 and close the project by 05 February 2027, within the 5-month window starting 14 September 2026.</td><td>Go-live on or before 29 Jan 2027; no milestone M1–M7 finishes more than 1 week later than the baseline date.</td></tr>

<tr><td class="label">Cost:</td><td>Deliver the whole scope within the preapproved 700,000,000 VND, including software, deployment, training, and warranty.</td><td>Final cost ≤ 700,000,000 VND; cost variance at each stage gate within ±5% of the baseline; management reserve use reported monthly.</td></tr>

<tr><td class="label">Other:</td><td><strong>Quality:</strong> deliver a system fit for daily operation from day one.<br><br><strong>Stakeholder satisfaction:</strong> the center's staff run the daily operation on the system, not on spreadsheets.</td><td>≥ 95% of UAT test cases pass; zero open Critical or High defects at go-live; ≤ 5 Medium defects open, each with an agreed fix date.<br><br>≥ 80% of the 25 staff users trained and active in the first month; average user satisfaction ≥ 4 of 5 in the closeout survey; ≥ 90% of classes have attendance recorded in the system during the warranty month.</td></tr>
</table>

<table class="form">
<tr><th style="width:72%">Summary Milestones</th><th style="width:28%">Due Date</th></tr>
<tr><td>M0 — Project kickoff; charter approved and team mobilized</td><td>14 Sep 2026</td></tr>
<tr><td>M1 — Requirement specification approved and baselined</td><td>02 Oct 2026</td></tr>
<tr><td>M2 — Design baseline approved (architecture, database schema, UI design)</td><td>23 Oct 2026</td></tr>
<tr><td>M3 — Iteration 1 demo accepted: F01–F05</td><td>20 Nov 2026</td></tr>
<tr><td>M4 — Iteration 2 accepted, feature complete: F06–F11</td><td>25 Dec 2026</td></tr>
<tr><td>M5 — System test complete; UAT entry criteria met</td><td>15 Jan 2027</td></tr>
<tr><td>M6 — UAT sign-off, data migrated, go-live and handover</td><td>29 Jan 2027</td></tr>
<tr><td>M7 — Warranty period complete; project closeout</td><td>05 Feb 2027</td></tr>
</table>

<div class="page-of">Page 2 of 4</div>

</div>

<div class="formpage">

<div class="form-title">Project Charter</div>

<table class="form">
<tr><td class="label">Preapproved Financial Resources:</td><td>Total <strong>700,000,000 VND</strong> from the center's 2026–2027 capital budget, released against milestone acceptance: 20% at M0, 25% at M3, 30% at M4, 25% at M6.<br><br>Personnel (25 person-months) 490,000,000 · Infrastructure and licenses 70,000,000 · Deployment, migration, training, documentation 70,000,000 · Management reserve 70,000,000.<br><br>No further funding is committed; an increase requires the sponsor's written approval.</td></tr>
</table>

<table class="form">
<tr><th style="width:38%">Stakeholder(s)</th><th style="width:62%">Role</th></tr>
<tr><td>Đỗ Thị Bích Ngọc — owner and Center Director</td><td>Sponsor: funds the project, approves the charter, scope changes, and final acceptance</td></tr>
<tr><td>Academic Manager</td><td>Business owner for courses, classes, scheduling, assessment; key requirement source and UAT lead</td></tr>
<tr><td>Accountant</td><td>Business owner for tuition, debt, and teaching-hour payroll; UAT participant</td></tr>
<tr><td>Front-desk / Admissions supervisor</td><td>Business owner for enrollment and payment recording; represents the daily users</td></tr>
<tr><td>Head Teacher (teacher representative)</td><td>Represents 35 teachers for attendance, scores, and teaching-hour screens</td></tr>
<tr><td>Students and parents</td><td>End users of schedule, result, and tuition views; recipients of notifications</td></tr>
<tr><td>Center IT administrator</td><td>Receives the system at handover; operates accounts, backup, and hosting afterwards</td></tr>
<tr><td>Nguyen Van A — Project Manager</td><td>Plans, executes, and controls the project; single point of contact for the sponsor</td></tr>
<tr><td>Development team (3 developers, 1 QA)</td><td>Analysis, design, build, test, deployment, documentation</td></tr>
<tr><td>SMS / email gateway provider</td><td>External supplier of the notification channel</td></tr>
<tr><td>Cloud hosting provider</td><td>External supplier of the production and staging environment</td></tr>
</table>

<table class="form">
<tr><td class="label">Project Exit Criteria:</td><td>1. All deliverables D1–D10 accepted in writing by the sponsor. 2. UAT signed off with ≥ 95% of test cases passed and no open Critical or High defect. 3. System running in production with backup verified by a successful restore test. 4. Production data migrated and reconciled against the source files, differences accepted in writing by the Accountant. 5. At least 80% of the 25 staff users trained, evidenced by the training record. 6. Source code, database scripts, user manual, and administrator guide handed over and acknowledged. 7. One-month warranty ended with no open Critical or High defect. 8. Closeout report, lessons learned, and final financial reconciliation approved, and final invoice settled.<br><br>Early closure by sponsor decision (withdrawn funding or lost business need) hands over the completed deliverables and closes the project with a termination report.</td></tr>
</table>

<table class="form">
<tr><td class="label" colspan="2">Project Manager Authority Level:</td></tr>
<tr><td class="label">Staffing Decisions:</td><td>Assigns and re-assigns work within the approved 5-person team, approves leave, and manages day-to-day performance. May request replacement of a team member, with the sponsor notified; hiring, firing, and contractual employment decisions remain with the vendor's line management.</td></tr>
<tr><td class="label">Budget Management and Variance:</td><td>Commits and spends within the approved baseline, including single transactions up to 20,000,000 VND and use of the 70,000,000 VND management reserve against risks R1–R7. Manages cumulative cost variance up to ±5% of the baseline. Escalates to the sponsor any forecast overrun beyond 5%, any reserve use beyond 40,000,000 VND, and any change in total funding.</td></tr>
</table>

<div class="page-of">Page 3 of 4</div>

</div>

<div class="formpage">

<div class="form-title">Project Charter</div>

<table class="form">
<tr><td class="label">Technical Decisions:</td><td>Full authority over architecture, technology stack, database design, coding standards, tooling, and the internal delivery approach, provided that non-functional requirements N01–N08 and the agreed deliverables are met. Decides the content of each iteration within the approved scope. Any decision that changes user-visible scope, the schedule, or the cost goes to the sponsor through the change process.</td></tr>

<tr><td class="label">Conflict Resolution:</td><td>Resolves conflicts within the project team and between the team and the center's operational staff, including priority conflicts over staff availability. Conflicts that cross organizations, alter agreed scope, or remain unresolved after 5 working days are escalated to the sponsor, whose decision is final. Disputes with external suppliers are handled through the applicable service agreement.</td></tr>

<tr><td class="label">Sponsor Authority:</td><td>Đỗ Thị Bích Ngọc, owner and Director of the learning center, authorizes the project and this charter, provides and releases the 700 million VND of funding, appoints the project manager, and makes the center's staff available. Approves changes to scope, schedule, and budget beyond the project manager's authority; sets acceptable variance limits; resolves escalated and inter-department conflicts; accepts deliverables; authorizes go-live and project closure; champions the project with staff and branch managers.</td></tr>
</table>

<table class="form">
<tr><td class="label" colspan="2">Approvals:</td></tr>
<tr><td style="height:60pt">Project Manager Signature</td><td style="height:60pt">Sponsor or Originator Signature</td></tr>
<tr><td>Project Manager Name: Nguyen Van A</td><td>Sponsor or Originator Name: Đỗ Thị Bích Ngọc</td></tr>
<tr><td>Date: ______________________</td><td>Date: ______________________</td></tr>
</table>

<div class="page-of">Page 4 of 4</div>

</div>
