<div class="cover" markdown="1">

# LEARNING CENTER MANAGEMENT SOFTWARE

<div class="subtitle">Requirement Specification &amp; Project Charter</div>

<table>
<tr><td>Project</td><td>Development and Deployment of a Learning Center Management Software</td></tr>
<tr><td>Product name</td><td><mark>[product name — to be decided]</mark></td></tr>
<tr><td>Budget</td><td>700,000,000 VND (700 million VND)</td></tr>
<tr><td>Duration</td><td>5 months — 14 Sep 2026 to 05 Feb 2027 (20.6 weeks elapsed)</td></tr>
<tr><td>Team size</td><td>5 full-time staff (PM/BA, 3 developers, 1 QA)</td></tr>
<tr><td>Customer</td><td><mark>Đỗ Thị Bích Ngọc — owner and director of the learning center</mark></td></tr>
<tr><td>Document version</td><td>2.0</td></tr>
<tr><td>Date prepared</td><td>02 September 2026</td></tr>
</table>

</div>

<p class="note">Scope of this document: Part 1 covers the short requirement specification; Part 2 covers the project charter, first as the element list of Table 1.1 of <em>A Project Manager's Book of Forms</em> (3rd ed.), then as the four-page PROJECT CHARTER form itself; Part 3 is the prompt log required by point 4 of the assignment.</p>

<p class="note"><strong>Reading the yellow highlight.</strong> A <mark>yellow background</mark> marks content whose correctness cannot be confirmed from the assignment brief: invented customer details, estimated figures, and dates that would need checking against a real calendar or a real customer. Content without a highlight is either <em>given</em> by the brief (budget 700 million VND, duration 5 months, team of 4–6 staff) or is a deliberate design decision of this document (the function list F01–F11, the non-functional requirements N01–N08, the milestone structure). An empty box means the information was not available and no reasonable assumption could be made. All assumptions are collected in section 1.7.</p>

<div class="pagebreak"></div>

## Part 1 — Requirement Specification (short version)

### 1.1 Product description

The customer, <mark>Đỗ Thị Bích Ngọc</mark>, owns and runs a private after-school learning center with about <mark>1,200 active students, 35 teachers, and 3 branches</mark> in the same city. It teaches English, mathematics, and IT skills in fixed-length courses of 24 to 48 sessions. Today the center runs on paper registers, spreadsheets, and a group-chat channel: enrollment lists live in Excel, attendance is taken on printed sheets, tuition debt is tracked by the accountant in a separate workbook, and parents are informed by manual messages. The result is duplicated data entry, room and teacher double-booking, tuition collected late, and no reliable view of revenue or class fill rate.

The system (product name <mark>[product name — to be decided]</mark>) is a web application that replaces those spreadsheets with one shared database covering the full operating cycle of the center: course catalog, class opening and scheduling, student enrollment, attendance, tuition and payment, teacher records and teaching-hour payroll, assessment, parent notification, and management reporting. It is used from a desktop browser by center staff and from a phone browser by teachers and parents.

The project delivers the software, deploys it on a cloud server for the center, migrates the current student and course data, trains the staff, and supports the center through one month of warranty after go-live.

### 1.2 Scope

**In scope**

- A responsive web application covering the eleven functions listed in section 1.4, in Vietnamese, for the three existing branches.
- A relational database as the single source of truth for students, courses, classes, sessions, attendance, invoices, payments, and teaching hours.
- Role-based access for seven user roles (section 1.3).
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
| N01 | Performance | Staff-facing screens respond within 3 seconds at 50 concurrent staff users. The student/parent portal responds within 3 seconds at <mark>300 concurrent sessions</mark>, the assumed peak when results are published or a tuition-due notification is sent to the whole center. A report covering one term is produced within 10 seconds. |
| N02 | Capacity | The system holds at least 5,000 student records, 200 classes per term, and 3 years of session history without redesign. |
| N03 | Security | HTTPS only; passwords stored with a salted one-way hash; permission enforced on the server side for every request; personal data of students and parents handled in line with the Law on Personal Data Protection (in force from 01 January 2026) and <mark>Decree 13/2023/ND-CP, to the extent the Decree remains in effect alongside the Law</mark>. Consent for parent notification is recorded per guardian. |
| N04 | Auditability | Create, update, and delete on financial and student records are written to an immutable audit log kept for at least 3 years. |
| N05 | Availability | 99% availability between 07:00 and 22:00 local time; automated nightly backup with recovery point objective 24 hours and recovery time objective 4 hours. |
| N06 | Usability | Vietnamese user interface; the daily tasks (attendance, payment recording, enrollment) reachable within 3 clicks from the home screen; usable by staff after a half-day of training. |
| N07 | Compatibility | Latest two versions of Chrome, Edge, and Firefox on desktop; responsive layout usable on a tablet and on a phone for the teacher and parent screens. |
| N08 | Maintainability | Layered architecture, coding convention applied, deployment guide and database schema documentation delivered with the source code. |

### 1.6 Technical approach

The system is built as a web application with a layered server-side architecture and a relational database, deployed as a single application instance and a database instance on one cloud virtual server, with a second environment for staging and UAT. The delivery method is iterative: two build iterations of four weeks each, each ending in a demo to the customer, followed by user acceptance testing on the complete system. System testing overlaps the build: the functions of iteration 1 (F01–F05) are system-tested while iteration 2 is being built, so that the dedicated test milestone after feature-complete covers integration and regression only. This overlap is what makes a one-month warranty fit inside the fixed 5-month window (section 1.7). Requirements are baselined at the end of the analysis phase; later changes go through the change process defined in the charter.

### 1.7 Assumptions and constraints

**Constraints**

- Budget is fixed at 700,000,000 VND, including software, deployment, training, and warranty.
- Duration is fixed at 5 months, from 14 September 2026 to 05 February 2027. The contractual figure is 5 months; the elapsed window is 20.6 weeks (4 months 22 days), and this document plans against the dates, not the rounded figure.
- The one-month warranty must finish inside the project, so go-live is baselined a full month before project closeout, not immediately before it.
- The team is 5 full-time staff; no additional headcount is available.
- The system must be in Vietnamese and must run on the customer's existing cloud budget of one virtual server.

**Assumptions**

- The customer's center (1,200 students, 35 teachers, 3 branches) and all figures in this document are assumed for this academic exercise; no real customer data is used. Every such figure is highlighted in yellow where it appears.
- The commercial product name is not decided yet; every place that needs it is marked in yellow and filled in a later version of this document.
- The system has 52 staff users: the 35 teachers plus 17 administrative, finance, and management staff (1 Director, 3 academic managers, 9 front-desk staff across the three branches, 3 accountants, 1 IT administrator). Students and parents are counted separately and are not part of the training target.
- The Lunar New Year (Tết) of 2027 is taken to begin on 06 February 2027. Project closeout is baselined the day before, and the warranty month is placed entirely before the break so that no warranty day falls inside it. This date should be confirmed against a published lunar calendar before the schedule is committed.
- Personnel funding is contracted as 25 person-months (5 staff × 5 months). The elapsed window is shorter than 5 calendar months, so 25 person-months is the funding basis rather than a measured effort figure.
- The Academic Manager and the Accountant are available at least 4 hours per week for requirement workshops, demos, and UAT.
- The center's current Excel files are usable as the migration source and are cleaned by the center before migration.
- One third-party SMS/email gateway account is provided and paid for by the center; its API is stable and documented.
- Business rules for discounts and refunds are confirmed during the analysis phase and frozen at the requirement sign-off milestone.
- No public holiday other than the Lunar New Year break of February 2027 affects the schedule materially.

<div class="pagebreak"></div>

## Part 2 — Project Charter

### 2A. Charter elements (Table 1.1 of the Book of Forms)

#### Project purpose

The center's manual, spreadsheet-based operation costs about <mark>60 staff-hours per month</mark> in duplicated data entry, causes recurring room and teacher double-booking, and leaves roughly <mark>8% of tuition uncollected past due date</mark> because no one has a reliable debt list. The project is undertaken to remove that operational loss and to give the Director a single, current view of enrollment, revenue, and teaching capacity across the three branches, as required by the center's <mark>plan to open a fourth branch in 2027</mark>.

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
- Each of the seven user roles sees only the data and screens its role permits, and every financial or student-data change is auditable.
- The interface is in Vietnamese and usable by existing staff after a half-day of training.
- Non-functional requirements N01–N08 of section 1.5 are met.

#### Overall project risk

Overall risk is assessed as **Medium**. The technology is well understood and the domain is stable, but the budget and the go-live date are both fixed, the team is small enough that the loss of one developer moves the critical path, and the customer staff who own the business rules are only part-time available. The dominant uncertainty is requirement volatility around tuition, discount, and refund policy, which is a management decision of the center rather than a technical question. A secondary exposure is the third-party notification gateway, which the project does not control. The schedule is compressed rather than tight at the end: the fixed 5-month window must contain both delivery and a full warranty month, so go-live is baselined on 05 January 2027 and the analysis, design, and test phases carry no more than one week of float each. The Lunar New Year break of February 2027 sits immediately after project closeout and cannot absorb any overrun.

| # | Main risk | Response |
| --- | --- | --- |
| R1 | Tuition, discount, and refund rules change after the requirement baseline | Freeze rules at M1 with written sign-off; route later changes through the change process against the 70 million VND reserve |
| R2 | Customer staff not available for workshops, demos, and UAT | Fixed weekly slot agreed with the sponsor at kickoff; escalate a missed slot to the sponsor within 2 working days |
| R3 | Loss or absence of a developer in a 5-person team | Pair on the scheduling and tuition modules; keep code and documentation in shared repositories; sponsor-approved replacement within 2 weeks |
| R4 | Third-party SMS/email gateway unstable or unexpectedly priced | Isolate the gateway behind one interface; validate with a proof of concept before M2; keep a second provider as fallback |
| R5 | Source Excel data too dirty to migrate | Data quality assessment at M1; the center cleans the files before M5; migration limited to the two most recent terms |
| R6 | Scheduling and conflict detection more complex than estimated | Build F04 first in iteration 1; timebox it and review at the M3 demo |
| R7 | Go-live slips and pushes the warranty month into the Lunar New Year break | Baseline go-live at M6 (05 Jan 2027), a full month before the assumed start of Tết, so the warranty month has four weeks of float ahead of the break; a forecast slip past 15 Jan 2027 is escalated to the sponsor immediately and triggers a re-plan of the warranty scope rather than a silent compression of it |
| R8 | The project manager is also the business analyst, so requirement work and management work compete for the same person | Front-load analysis into M0–M1 while management load is lowest; the QA engineer writes the test cases directly from the requirement baseline as a second reader of the requirements; escalate to the sponsor if analysis rework after M1 exceeds one week |

#### Project objectives and related success criteria

| Objective area | Objective | Success criteria |
| --- | --- | --- |
| Scope | Deliver the eleven functions F01–F11 and the ten deliverables D1–D10 | 100% of F01–F11 accepted in UAT; all ten deliverables signed off by the sponsor |
| Time | Go live by 05 January 2027 and close the project by 05 February 2027 | Go-live on or before 05 Jan 2027; no milestone finishes more than 1 week late; the warranty month runs its full 31 days before closeout |
| Cost | Deliver within 700,000,000 VND | Final cost ≤ 700 million VND; cost variance at each stage gate within ±5% of the baseline |
| Quality | Deliver a system fit for daily operation | ≥ 95% of UAT test cases pass; zero open Critical or High defects at go-live; ≤ 5 Medium defects open, each with an agreed fix date |
| Stakeholder satisfaction | The center's staff can run the operation on the system | ≥ 80% of the <mark>52 staff users</mark> trained and active in the first month, including ≥ 90% of the 17 administrative users and ≥ 75% of the 35 teachers; average user satisfaction ≥ 4 of 5 in the closeout survey; ≥ 90% of classes have attendance recorded in the system in the warranty month |

#### Summary milestone schedule

| ID | Milestone | Due date |
| --- | --- | --- |
| M0 | Project kickoff, charter approved | Mon 14 Sep 2026 |
| M1 | Requirement specification approved and baselined | Fri 02 Oct 2026 |
| M2 | Design baseline approved (architecture, database, UI) | Fri 16 Oct 2026 |
| M3 | Iteration 1 demo accepted (F01–F05) | Fri 13 Nov 2026 |
| M4 | Iteration 2 accepted — feature complete (F06–F11) | Fri 11 Dec 2026 |
| M5 | System test complete, UAT entry criteria met | Fri 18 Dec 2026 |
| M6 | UAT sign-off, data migrated, go-live and handover | Tue 05 Jan 2027 |
| M7 | Warranty complete, project closeout | Fri 05 Feb 2027 |

Go-live is deliberately placed on a Tuesday so that the first two days of live operation are fully staffed working days; the remaining milestones fall on Fridays to close a working week. The month from M6 to M7 is the warranty period, and it ends the day before the assumed start of the Lunar New Year break (section 1.7).

#### Preapproved financial resources

Total preapproved funding is **700,000,000 VND**, provided by the center from its 2026–2027 capital budget, released in four tranches against milestone acceptance: 20% at M0, 25% at M3, 30% at M4, 25% at M6.

| # | Cost category | Amount (VND) | Share | Basis |
| --- | --- | --- | --- | --- |
| 1 | Personnel — 5 staff × 5 months = 25 person-months | 490,000,000 | 70% | <mark>19.6 million VND per person-month, fully loaded</mark> |
| 2 | Infrastructure and licenses | 70,000,000 | 10% | Cloud server and staging for 12 months, domain, SSL, SMS/email gateway credits, development tools |
| 3 | Deployment, data migration, training, documentation | 70,000,000 | 10% | On-site work at 3 branches, training materials, printing |
| 4 | Management reserve (contingency) | 70,000,000 | 10% | Held by the project manager against identified risks R1–R8 |
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

#### Project approval requirements

**What constitutes project success.** The project is successful when the five objectives above (scope, time, cost, quality, stakeholder satisfaction) are met against their stated success criteria, and the system is in daily productive use by the center's staff at closeout rather than running in parallel with the old spreadsheets.

**Who decides and who signs off.**

| Item to be approved | Approved by | Evidence of approval |
| --- | --- | --- |
| This charter | Center Director (sponsor) | Signature on the approval block of the charter form |
| Requirement specification (D1) | Academic Manager and Accountant for their domains; sponsor overall | Signed requirement baseline at M1 |
| Design baseline (D2) | Project Manager, reviewed with the Academic Manager for workflow fit | Signed design review record at M2 |
| Iteration releases (D3, D4) | Academic Manager (F01–F05, F08), Accountant (F06, F07), Front-desk supervisor (F02, F09) | Signed demo acceptance record at M3 and M4 |
| Test completion (D5) | QA engineer prepares; Project Manager approves UAT entry | Test summary report accepted at M5 |
| UAT result and go-live | Business owners sign their own areas; sponsor authorizes go-live | Signed UAT report and go-live authorization at M6 |
| Migrated data (D6) | Accountant, for reconciliation against the source files | Written acceptance of the reconciliation, including accepted differences |
| Handover package (D8, D9) | Center IT administrator | Signed handover record |
| Project closure (D10) | Center Director (sponsor) | Signed closeout report |

**Who accepts the final product.** The Center Director, as sponsor and owner, gives final acceptance. The sponsor may not delegate final acceptance, but relies on the written area sign-offs above and may not withhold acceptance for scope that was never in the baseline.

#### Project exit criteria

The project is closed when all of the following are met:

1. All deliverables D1–D10 are accepted in writing by the sponsor.
2. UAT is signed off with ≥ 95% of test cases passed and no open Critical or High defect.
3. The system runs in production on the center's cloud server with backup verified by a successful restore test.
4. Production data is migrated and reconciled against the source files, with differences accepted in writing by the Accountant.
5. At least 80% of the <mark>52 staff users</mark> are trained, evidenced by the training record.
6. Source code, database scripts, user manual, and administrator guide are handed over and acknowledged.
7. The one-month warranty period has ended with no open Critical or High defect.
8. The closeout report, lessons learned, and final financial reconciliation are approved, and the final invoice is settled.

The project may also be closed early by decision of the sponsor if funding is withdrawn or the business need disappears; in that case the deliverables completed to date are handed over and the project is closed with a termination report.

#### Assigned project manager, responsibility, and authority level

**Project manager:** <mark>Nguyễn Văn A</mark>, Project Manager, assigned full-time for the full 5 months.

**Responsibility:** plan, execute, monitor, and close the project; manage scope, schedule, cost, quality, risk, and communication; lead the 5-person team; act as the single point of contact for the sponsor and the center's staff; report status weekly.

**Staffing decisions:** may assign and re-assign work within the approved 5-person team, approve leave, and manage day-to-day performance. May request the replacement of a team member; the actual hiring, firing, and contractual employment decisions remain with the vendor's line management and require the sponsor's notification.

**Budget management and variance:** may commit and spend the approved budget within the baseline, including single transactions up to 20,000,000 VND and use of the 70,000,000 VND management reserve against the identified risks R1–R8. Cumulative cost variance up to 5% of the baseline is managed by the project manager; any forecast overrun beyond 5%, any use of reserve beyond 40,000,000 VND, and any change in total funding are escalated to the sponsor for approval.

**Technical decisions:** full authority over architecture, technology stack, database design, coding standards, and the internal delivery approach, provided the non-functional requirements N01–N08 and the agreed deliverables are met. Changes that affect the user-visible scope, the schedule, or the cost require the sponsor's approval through the change process.

**Conflict resolution:** resolves conflicts within the project team and between the team and the center's operational staff. Conflicts that cross organizations, change agreed scope, or remain unresolved after 5 working days are escalated to the sponsor, whose decision is final.

#### Name and authority of the sponsor

**Sponsor:** <mark>Đỗ Thị Bích Ngọc</mark>, owner and Director of the learning center.

The sponsor authorizes the project and this charter, provides and releases the 700 million VND of funding, appoints the project manager, and makes the center's staff available. The sponsor approves changes to scope, schedule, and budget beyond the project manager's authority, sets acceptable variance limits, resolves conflicts escalated by the project manager or arising between the center's departments, accepts the deliverables, and authorizes go-live and project closure. The sponsor champions the project with the center's staff and with the branch managers.

### 2B. Project charter form

<div class="formpage">

<div class="form-title">Project Charter</div>

<table class="form">
<tr><td class="label">Project Title:</td><td>Development and Deployment of a Learning Center Management Software — product name <mark>[product name — to be decided]</mark></td><td class="label">Date Prepared:</td><td>02 September 2026</td></tr>
<tr><td class="label">Project Sponsor:</td><td><mark>Đỗ Thị Bích Ngọc — owner and Director of the learning center</mark></td><td class="label">Project Customer:</td><td><mark>Đỗ Thị Bích Ngọc — the learning center (3 branches, 1,200 students, 35 teachers)</mark></td></tr>
<tr><td class="label">Project Manager:</td><td colspan="3"><mark>Nguyễn Văn A</mark> — Project Manager, assigned full-time for the 5-month duration</td></tr>
</table>

<table class="form">
<tr><td class="label">Project Purpose:</td><td>The center is run on paper and spreadsheets, which costs about <mark>60 staff-hours a month</mark> in duplicated data entry, causes recurring room and teacher double-booking, and leaves roughly <mark>8% of tuition uncollected past due date</mark>. The project removes that operational loss and gives the Director one current view of enrollment, revenue, and teaching capacity across the three branches, as required by the <mark>plan to open a fourth branch in 2027</mark>.</td></tr>

<tr><td class="label">High-Level Project Description:</td><td>Analyze, design, build, test, and deploy a Vietnamese-language web application managing the full operating cycle of the center — courses, classes and scheduling, students and enrollment, attendance, tuition and payments, teachers and teaching-hour payroll, assessment, notification, and management reporting — with migration from the current Excel files, staff training, and one month of warranty. Iterative delivery in two build iterations plus UAT, by 5 staff, in 5 months, for 700 million VND.</td></tr>

<tr><td class="label">Project Boundaries:</td><td><strong>Included:</strong> functions F01–F11 for the three existing branches; migration of the two most recent terms; deployment on one cloud virtual server; training; documentation; one month of warranty.<br><br><strong>Excluded:</strong> native mobile apps; online teaching, video, and e-learning content; automated payment gateway or e-wallet; accounting, tax, and social-insurance integration; attendance hardware and any hardware procurement; multi-tenant use by other centers; data older than two terms.<br><br>The project ends at the closeout meeting after the warranty month; ongoing operation and hosting pass to the center.</td></tr>

<tr><td class="label">Key Deliverables:</td><td>D1 Approved requirement specification · D2 Design baseline (architecture, database, UI) · D3 Iteration 1 release (F01–F05) · D4 Iteration 2 release (F06–F11) · D5 Test documentation and test summary report · D6 Migrated and reconciled production data · D7 Production deployment with backup configured · D8 User manual, administrator guide, and trained staff · D9 Source code, database scripts, technical documentation · D10 Closeout report and lessons learned</td></tr>

<tr><td class="label">High-Level Requirements:</td><td>One integrated database with no duplicate data entry across the eleven functional areas · Conflict detection blocking room, teacher, and student schedule collisions at class and session creation · Tuition invoices generated from course fee and discount policy, with outstanding debt visible per student, class, and branch · Teaching hours derived from recorded attendance and exportable for payroll · Automatic notification of reminders, absence, tuition due, and results, with a delivery log · Role-based access for seven roles and an audit trail on all financial and student data · Vietnamese interface usable after a half-day of training · Non-functional requirements N01–N08 (performance, capacity, security, audit, availability, usability, compatibility, maintainability)</td></tr>

<tr><td class="label">Overall Project Risk:</td><td><strong>Medium.</strong> Technology and domain are well understood, but budget and duration are both fixed, and the 5-month window must contain delivery <em>and</em> a full one-month warranty, which compresses analysis, design, and test to no more than one week of float each. The 5-person team is small enough that losing one developer moves the critical path, the project manager is also the business analyst, and the customer staff who own the business rules are only part-time available. Dominant uncertainty: volatility of tuition, discount, and refund policy. The Lunar New Year break of February 2027 falls immediately after closeout and can absorb no overrun. Risks R1–R8 are identified with responses and covered by a 70 million VND reserve.</td></tr>
</table>

<div class="page-of">Page 1 of 4</div>

</div>

<div class="formpage">

<div class="form-title">Project Charter</div>

<table class="form">
<tr><th style="width:14%">&nbsp;</th><th style="width:43%">Project Objectives</th><th style="width:43%">Success Criteria</th></tr>

<tr><td class="label">Scope:</td><td>Deliver the eleven functions F01–F11 and the ten deliverables D1–D10 defined for the three branches.</td><td>100% of F01–F11 accepted in UAT; all ten deliverables signed off by the sponsor; no function deferred without an approved change request.</td></tr>

<tr><td class="label">Time:</td><td>Go live by 05 January 2027 and close the project by 05 February 2027, within the 5-month window starting 14 September 2026, with the full warranty month contained inside that window.</td><td>Go-live on or before 05 Jan 2027; no milestone M1–M7 finishes more than 1 week later than the baseline date; the warranty period runs its full 31 days before closeout.</td></tr>

<tr><td class="label">Cost:</td><td>Deliver the whole scope within the preapproved 700,000,000 VND, including software, deployment, training, and warranty.</td><td>Final cost ≤ 700,000,000 VND; cost variance at each stage gate within ±5% of the baseline; management reserve use reported monthly.</td></tr>

<tr><td class="label">Other:</td><td><strong>Quality:</strong> deliver a system fit for daily operation from day one.<br><br><strong>Stakeholder satisfaction:</strong> the center's staff run the daily operation on the system, not on spreadsheets.</td><td>≥ 95% of UAT test cases pass; zero open Critical or High defects at go-live; ≤ 5 Medium defects open, each with an agreed fix date.<br><br>≥ 80% of the <mark>52 staff users</mark> trained and active in the first month; average user satisfaction ≥ 4 of 5 in the closeout survey; ≥ 90% of classes have attendance recorded in the system during the warranty month.</td></tr>
</table>

<table class="form">
<tr><th style="width:72%">Summary Milestones</th><th style="width:28%">Due Date</th></tr>
<tr><td>M0 — Project kickoff; charter approved and team mobilized</td><td>Mon 14 Sep 2026</td></tr>
<tr><td>M1 — Requirement specification approved and baselined</td><td>Fri 02 Oct 2026</td></tr>
<tr><td>M2 — Design baseline approved (architecture, database schema, UI design)</td><td>Fri 16 Oct 2026</td></tr>
<tr><td>M3 — Iteration 1 demo accepted: F01–F05</td><td>Fri 13 Nov 2026</td></tr>
<tr><td>M4 — Iteration 2 accepted, feature complete: F06–F11</td><td>Fri 11 Dec 2026</td></tr>
<tr><td>M5 — System test complete; UAT entry criteria met</td><td>Fri 18 Dec 2026</td></tr>
<tr><td>M6 — UAT sign-off, data migrated, go-live and handover</td><td>Tue 05 Jan 2027</td></tr>
<tr><td>M7 — Warranty period complete; project closeout</td><td>Fri 05 Feb 2027</td></tr>
<tr><td colspan="2" style="font-style:italic">M6 to M7 is the one-month warranty period. Go-live is on a Tuesday so that live operation begins with two fully staffed working days.</td></tr>
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
<tr><td><mark>Đỗ Thị Bích Ngọc</mark> — owner and Center Director</td><td>Sponsor: funds the project, approves the charter, scope changes, and final acceptance</td></tr>
<tr><td>Academic Manager</td><td>Business owner for courses, classes, scheduling, assessment; key requirement source and UAT lead</td></tr>
<tr><td>Accountant</td><td>Business owner for tuition, debt, and teaching-hour payroll; UAT participant</td></tr>
<tr><td>Front-desk / Admissions supervisor</td><td>Business owner for enrollment and payment recording; represents the daily users</td></tr>
<tr><td>Head Teacher (teacher representative)</td><td>Represents 35 teachers for attendance, scores, and teaching-hour screens</td></tr>
<tr><td>Students and parents</td><td>End users of schedule, result, and tuition views; recipients of notifications</td></tr>
<tr><td>Center IT administrator</td><td>Receives the system at handover; operates accounts, backup, and hosting afterwards</td></tr>
<tr><td><mark>Nguyễn Văn A</mark> — Project Manager</td><td>Plans, executes, and controls the project; single point of contact for the sponsor</td></tr>
<tr><td>Development team (3 developers, 1 QA)</td><td>Analysis, design, build, test, deployment, documentation</td></tr>
<tr><td>SMS / email gateway provider</td><td>External supplier of the notification channel</td></tr>
<tr><td>Cloud hosting provider</td><td>External supplier of the production and staging environment</td></tr>
</table>

<table class="form">
<tr><td class="label">Project Exit Criteria:</td><td>1. All deliverables D1–D10 accepted in writing by the sponsor. 2. UAT signed off with ≥ 95% of test cases passed and no open Critical or High defect. 3. System running in production with backup verified by a successful restore test. 4. Production data migrated and reconciled against the source files, differences accepted in writing by the Accountant. 5. At least 80% of the <mark>52 staff users</mark> trained, evidenced by the training record. 6. Source code, database scripts, user manual, and administrator guide handed over and acknowledged. 7. One-month warranty ended with no open Critical or High defect. 8. Closeout report, lessons learned, and final financial reconciliation approved, and final invoice settled.<br><br>Early closure by sponsor decision (withdrawn funding or lost business need) hands over the completed deliverables and closes the project with a termination report.</td></tr>
</table>

<table class="form">
<tr><td class="label" colspan="2">Project Manager Authority Level:</td></tr>
<tr><td class="label">Staffing Decisions:</td><td>Assigns and re-assigns work within the approved 5-person team, approves leave, and manages day-to-day performance. May request replacement of a team member, with the sponsor notified; hiring, firing, and contractual employment decisions remain with the vendor's line management.</td></tr>
<tr><td class="label">Budget Management and Variance:</td><td>Commits and spends within the approved baseline, including single transactions up to 20,000,000 VND and use of the 70,000,000 VND management reserve against risks R1–R8. Manages cumulative cost variance up to ±5% of the baseline. Escalates to the sponsor any forecast overrun beyond 5%, any reserve use beyond 40,000,000 VND, and any change in total funding.</td></tr>
</table>

<div class="page-of">Page 3 of 4</div>

</div>

<div class="formpage">

<div class="form-title">Project Charter</div>

<table class="form">
<tr><td class="label">Technical Decisions:</td><td>Full authority over architecture, technology stack, database design, coding standards, tooling, and the internal delivery approach, provided that non-functional requirements N01–N08 and the agreed deliverables are met. Decides the content of each iteration within the approved scope. Any decision that changes user-visible scope, the schedule, or the cost goes to the sponsor through the change process.</td></tr>

<tr><td class="label">Conflict Resolution:</td><td>Resolves conflicts within the project team and between the team and the center's operational staff, including priority conflicts over staff availability. Conflicts that cross organizations, alter agreed scope, or remain unresolved after 5 working days are escalated to the sponsor, whose decision is final. Disputes with external suppliers are handled through the applicable service agreement.</td></tr>

<tr><td class="label">Sponsor Authority:</td><td><mark>Đỗ Thị Bích Ngọc</mark>, owner and Director of the learning center, authorizes the project and this charter, provides and releases the 700 million VND of funding, appoints the project manager, and makes the center's staff available. Approves changes to scope, schedule, and budget beyond the project manager's authority; sets acceptable variance limits; resolves escalated and inter-department conflicts; accepts deliverables; authorizes go-live and project closure; champions the project with staff and branch managers.</td></tr>
</table>

<table class="form">
<tr><td class="label" colspan="2">Approvals:</td></tr>
<tr><td style="height:60pt">Project Manager Signature</td><td style="height:60pt">Sponsor or Originator Signature</td></tr>
<tr><td>Project Manager Name: <mark>Nguyễn Văn A</mark></td><td>Sponsor or Originator Name: <mark>Đỗ Thị Bích Ngọc</mark></td></tr>
<tr><td>Date: ______________________</td><td>Date: ______________________</td></tr>
</table>

<div class="page-of">Page 4 of 4</div>

</div>

<div class="pagebreak"></div>

## Part 3 — Prompt Log

This part answers point 4 of the assignment: every prompt version used to produce this document, an assessment of what each version produced, and the reason each one had to be replaced.

The pattern across the six versions is consistent. Prompts that described the *document* produced fluent text that was wrong in checkable ways. Prompts that described the *constraints and the source* produced text that could be verified. The largest single gain came from asking for an adversarial audit rather than asking for more content.

### 3.1 Version history

<div class="fnlist" markdown="1">

| V | Intent | Quality of the result | Why it was replaced |
| --- | --- | --- | --- |
| V1 | Get a first draft of anything usable | Generic and unusable. Read like a textbook chapter about charters rather than a charter for this project. | No project constraints in the prompt, so nothing was anchored |
| V2 | Anchor the draft in the assignment's real numbers | Correct scale, still shapeless. The function list appeared and was reasonable. | Structure came from the model's habits, not from the prescribed form |
| V3 | Force the structure of the Book of Forms | Right structure, prose too vague to check. Success criteria were adjectives, not numbers. | Vague success criteria are unmarkable; measurable values were needed |
| V4 | Make every claim measurable and produce the Vietnamese version | The version this audit was run against. Fluent, complete-looking, internally inconsistent. | Fluency masked four contradictions that no generative prompt would surface |
| V5 | Find the errors instead of adding content | Highest-value prompt of the whole set. Found a schedule that contradicted its own warranty. | Audit only — the fixes still had to be requested |
| V6 | Apply every finding to both languages at once | Produced this version 2.0 | Current |

</div>

### 3.2 The prompts

#### V1 — first draft

> Write a project charter for a learning center management software project.

**Quality: poor.** Roughly 600 words of generic material — "the project will deliver value to stakeholders", milestones named "Phase 1" through "Phase 4", no figures. Nothing in it was specific enough to be either right or wrong.

**Why replaced:** the prompt contained no budget, no duration, no team size, and no customer. With nothing to anchor to, the output described the *idea* of a charter instead of this project.

#### V2 — constraints added

> Write a project charter for "Development and Deployment of a Learning Center Management Software". Budget 700 million VND, duration 5 months, team of 5. The customer is a private after-school learning center. Include a requirement specification with a list of functions and a description of each function.

**Quality: fair.** The numbers propagated correctly and the eleven functions F01–F11 appeared here in close to their final form — this part of the output survived to version 2.0 almost unchanged. But the charter section was a flat sequence of headings chosen by the model.

**Why replaced:** the assignment does not ask for *a* charter, it asks for the charter form from a named book. Structure invented by the model scores nothing against a prescribed template.

#### V3 — structure imposed

> Use the charter elements of Table 1.1 of A Project Manager's Book of Forms (3rd edition), then reproduce the four-page PROJECT CHARTER form itself and fill it in. Keep the requirement specification as Part 1 and the charter as Part 2.

**Quality: good structurally, weak in content.** Both the element list (2A) and the four-page form (2B) appeared, correctly separated. But the content stayed soft: the quality objective read "deliver a high-quality system", and the exit criteria read "the customer is satisfied".

**Why replaced:** unmeasurable criteria cannot be assessed by a marker, and they hide risk. "The customer is satisfied" has no failure condition.

#### V4 — measurability and the Vietnamese version

> Every success criterion must be a number with a threshold and a measurement point. Add a risk register with responses, a milestone schedule with real dates, and a cost breakdown that sums exactly to 700 million VND. Then produce a Vietnamese version with identical structure — same headings, same table rows, so the two files diff cleanly.

**Quality: high on the surface, and this is the important entry in the log.** Everything asked for arrived: the budget reconciled exactly (490 + 70 + 70 + 70 = 700), the milestones all landed on Fridays, the risk register had real responses, and the two language files matched line for line.

It was also wrong in four ways that no amount of re-reading it as a *reader* would surface:

1. The document promised a one-month warranty and scheduled seven days for it.
2. It claimed six user roles and listed seven.
3. It set a training target of 25 staff users at a center it had already given 35 teachers.
4. It specified 50 concurrent users for a system whose own role table gives 1,200 students and their parents a login.

**Why replaced:** this is the failure mode worth recording. The prompt asked for internal consistency and the output *looked* internally consistent. Generative prompts optimize for a document that reads well; they do not cross-check a claim in section 1.2 against a table in section 1.3. Asking the same prompt again, or asking "check your work", reproduces the same blind spots because the same reading process produced them.

#### V5 — audit instead of generation

> Do a deep audit of the document, scoped to a year-4 university assignment. Check every number against every other number. Check the schedule arithmetic against the stated durations. List what contradicts what, ranked by how likely a marker is to notice, and say what you could not verify.

**Quality: the highest-value prompt in the set.** It produced no new document text at all, and it found all four contradictions above, plus a missing Table 1.1 element and two soft numbers.

Three things made it work, and they generalize:

- **It asked for contradictions, not improvements.** "Improve this" returns more prose. "What contradicts what" returns a list of defects.
- **It named the audience.** "Year-4 assignment" set the bar at what a marker actually checks — countable claims, arithmetic, dates — rather than at industrial project management.
- **It required an admission of ignorance.** Asking what could *not* be verified surfaced that the charter form had never been compared against the book, which had been silently assumed since V3.

**Why replaced:** an audit produces findings, not fixes. Applying them was a separate step, deliberately kept separate so that the findings could be reviewed before anything was rewritten.

#### V6 — apply the findings

> Fix all of them, then refine.

**Quality: adequate, because V5 had already done the thinking.** The prompt is short only because the audit it depends on was specific. The same three words issued after V4, with no audit in between, would have produced another fluent revision of the same broken schedule.

Applied in this version: the schedule was re-baselined so that go-live moved from 29 January to 05 January 2027 and the warranty month became real; six/seven was corrected in three places per language; the training base became 52 with a stated composition; N01 was split into a staff figure and a parent-portal figure; the missing *project approval requirements* element was added to section 2A; and the yellow-highlight convention was applied to the invented figures instead of being declared and left unused.

### 3.3 What the sequence shows

<div class="fnlist" markdown="1">

| Lesson | Evidence from this log |
| --- | --- |
| Constraints beat instructions | V1 to V2: adding four numbers did more than any amount of "be detailed" |
| Name the source, do not describe it | V2 to V3: "Table 1.1 of the Book of Forms" produced the right structure immediately |
| Demand thresholds, not adjectives | V3 to V4: "a number with a threshold and a measurement point" removed every unmarkable criterion |
| Fluency is not correctness | V4: the most polished version was the one with four contradictions in it |
| Auditing is a different task from writing | V5: found in one pass what four generative prompts had accumulated |
| Ask what could not be verified | V5: surfaced that the printed form itself had never been checked — still open, below |

</div>

**Still open.** The four-page form in Part 2B was reconstructed from the charter-element list; it was not read field by field from pages 16–19 of *A Project Manager's Book of Forms*. Its field set should be compared against the printed form before submission. If the book's form carries a field this document omits, that field must be added; if it omits one this document includes, the extra should be removed rather than kept.
