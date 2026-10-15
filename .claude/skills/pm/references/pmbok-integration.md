# PMBOK 6 chapter 4, Project Integration Management, for the integration forms

Read this before filling 1.1 Project Charter, 1.2 Assumption Log, 2.1 Project
Management Plan, 2.2 Change Management Plan, 2.3 Project Roadmap, 3.2 Decision
Log, 3.3 Change Request, 3.4 Change Log, 3.5 Lessons Learned Register, 4.2
Project Status Report, 5.1 Lessons Learned Summary or 5.2 Project or Phase
Closeout. The forms print the boxes; chapter 4 says what each output carries and
which technique decides it. A remedy or a ruling in these forms carries the
PMBOK name of its technique, and when the constraints cannot all hold the route
is a change request (3.3) to the sponsor, never a cut to an estimate.

## Where it is

`PMBOK6_and_Agile_Practice_Guide.pdf` at the repo root. PDF page = printed page
+ 39 in the Guide part. Cite "PMBOK 6 section 4.6.1.4, printed page 117 (PDF page
156)". Text extraction is cleaner without `-layout` (`pdftotext -f N -l N`),
then drop lines of three characters or fewer and the "PMI Member benefit" footer.
The Agile Practice Guide is not used here; chapter 4 gives its agile view on
printed page 74.

| Section | Printed page | PDF page |
| --- | --- | --- |
| 4 intro and process list; key concepts; trends; tailoring and agile | 69 to 74 | 108 to 113 |
| 4.1 Develop Project Charter (4.1.3.1 charter components, 4.1.3.2 assumption log) | 75 to 81 | 114 to 120 |
| 4.2 Develop Project Management Plan (baselining 83; kick-off 86) | 82 to 89 | 121 to 128 |
| 4.2.3.1 plan components 86 to 88; Table 4-1 plan versus project documents 89 | 86 to 89 | 125 to 128 |
| 4.3 Direct and Manage Project Work (4.3.3.3 issue log, 4.3.3.4 change requests: 96) | 90 to 97 | 129 to 136 |
| 4.4 Manage Project Knowledge (4.4.3.1 lessons learned register: 104) | 98 to 105 | 137 to 144 |
| 4.5 Monitor and Control Project Work (4.5.1.3 work performance information 109; 4.5.2.2 data analysis 111; 4.5.3.1 reports 112) | 105 to 113 | 144 to 152 |
| 4.6 Perform Integrated Change Control (discussion 115; 4.6.1.4 117; 4.6.2.3 and 4.6.2.4 119; 4.6.3 outputs 120) | 113 to 120 | 152 to 159 |
| 4.7 Close Project or Phase (closure activities 123; 4.7.3.3 final report 127 to 128) | 121 to 128 | 160 to 167 |
| Glossary: assumption, baseline 699; change control, CCB, change log, change management plan 700; configuration management plan, constraint 701 | 699 to 701 | 738 to 740 |
| Used by cross reference: 1.2.6 business documents, Table 1-5 | 29 | 68 |
| 5.2.2.4 voting; 8.1.2.3 cost-benefit; 8.1.2.4 multicriteria; 9.2.2.5 alternatives analysis | 144; 282; 283; 325 | 183; 321; 322; 364 |
| 7.3.2.3 management reserve; 7.3.3.1 cost baseline; 7.4.2.2 earned value | 252; 254; 261 to 264 | 291; 293; 300 to 303 |

Book of Forms (PDF page = printed page + 11): 1.1 PDF 13 to 15 (printed 2 to 4),
blank 16 to 19 (5 to 8); 1.2 PDF 20 to 21 (9 to 10), blank 22 (11); 2.1 PDF 31
to 33 (20 to 22), blank 34 to 35 (23 to 24); 2.2 PDF 36 to 37 (25 to 26), blank
38 (27); 2.3 PDF 39 (28), sample 40 (29); 3.2 PDF 179 (168), blank 180 (169);
3.3 PDF 181 to 182 (170 to 171), blank 183 to 185 (172 to 174); 3.4 PDF 186 to
187 (175 to 176), blank 188 (177); 3.5 PDF 189 to 190 (178 to 179), blank 191
(180); 4.2 PDF 207 to 208 (196 to 197), blank 209 to 212 (198 to 201); 5.1 PDF
240 to 243 (229 to 232), blank 244 to 245 (233 to 234); 5.2 PDF 246 to 247 (235
to 236), blank 248 to 249 (237 to 238).

## Chapter 4 terms worth using, with the book's meaning

- **Integration** is the project manager's own accountability and cannot be
  delegated or transferred (key concepts, printed page 72). It is choosing
  between competing demands and alternatives and tailoring the processes
  (printed page 69).
- **Project charter** formally authorizes the project and gives the project
  manager authority over organizational resources. It is not a contract, because
  no consideration or money changes hands in making it (4.1, printed page 77).
- **Business case** and **benefits management plan** are business documents. The
  project manager feeds the charter from them and may recommend changes but does
  not update them (4.1.1.1, printed pages 77 to 78; Table 1-5, printed page 29).
- **Assumption** is a planning factor taken as true without proof; **constraint**
  is a limiting factor (Glossary, printed pages 699 and 701). The assumption log
  records both for the whole life cycle (4.1.3.2, printed page 81).
- **Baseline** is the approved version of a work product that changes only
  through formal change control (Glossary, printed page 699). The plan must be
  baselined for at least scope, time and cost; before that it may be updated
  freely, afterwards only through 4.6 (4.2, printed page 83).
- **Plan versus documents** (Table 4-1, printed page 89): subsidiary plans,
  baselines, change management plan, configuration management plan, life cycle
  and development approach belong to the plan; registers, logs, estimates,
  schedule and reports are project documents. A plan component changes only by
  change request (4.3.3.5, printed page 97); a document needs one only if the plan
  puts it under formal change control (4.2.2.1, page 85; 4.6.3.3, page 120).
- **Work performance data** are raw observations; compared with the plan and its
  thresholds they become **work performance information**, which a **work
  performance report** packages to prompt decisions (4.3.3.2 printed page 95;
  4.5.1.3 printed page 109; 4.5.3.1 printed page 112).
- **Change request**: a formal proposal to modify any document, deliverable or
  baseline; any stakeholder may raise one; it may be optional or legally or
  contractually mandatory; types are corrective action, preventive action,
  defect repair and updates (4.3.3.4, printed page 96).
- **Change control board (CCB)**: a formally chartered group that reviews,
  approves, delays or rejects changes and records and communicates the decision
  (Glossary, printed page 700). The **change management plan** establishes it
  and its authority. **Configuration management** is a separate plan: which items
  are controlled and recorded (4.2.3.1, printed page 88; 4.6.2.2, printed page 118).
- **Approved change request** has three possible dispositions, approved, deferred
  or rejected; the change log records every one (4.6.3.1 and 4.6.3.2, printed page 120).
- **Explicit versus tacit knowledge** (4.4, printed page 100). The **lessons
  learned register** is created early and updated throughout; at the end it moves
  to the organization's **lessons learned repository** (4.4.3.1, printed page 104).
- **Final report** summarizes performance at closure; **final product
  transition** hands the result to the operating group (4.7.3, printed page 127).

## How each process output maps onto the forms

Labels come from `references/fields/<form>.json`. "No box" rows say where the
content goes; name that place in the italic reading paragraph.

**4.1.3.1 Project charter (printed page 81, PDF 120) onto 1.1** (form text: PDF 13 to 15, printed 2 to 4)

| PMBOK component | Form 1.1 box | If no box |
| --- | --- | --- |
| Project purpose | Project Purpose | |
| Measurable objectives and success criteria | Project Objectives, Success Criteria (rows Scope, Time, Cost, Other) | Quality and stakeholder satisfaction go in Other |
| Overall project risk | Overall Project Risk | |
| Summary milestone schedule | Summary Milestones, Due Date | |
| High-level description, boundaries, key deliverables | High-Level Project Description; Project Boundaries; Key Deliverables | |
| High-level requirements | High-Level Requirements | |
| Preapproved financial resources | Preapproved Financial Resources | |
| Key stakeholder list | Stakeholder(s), Role | |
| Project exit criteria | Project Exit Criteria | |
| Assigned project manager, responsibility, authority level | Project Manager in the title block; Staffing Decisions; Budget Management and Variance; Technical Decisions; Conflict Resolution | Responsibility has no box: open the first authority box with it, or keep it in the project's 2A text |
| Name and authority of the sponsor | Sponsor Authority; Project Sponsor in the title block | |
| Project approval requirements (what is success, who decides, who signs) | No box; Approvals prints signature, name and date only | Success definition in Project Exit Criteria; who accepts in Sponsor Authority; the rest stays in charter Part 2A |

Project Customer and Date Prepared are title-block labels that 4.1.3.1 does not list.

**4.1.3.2 Assumption log (printed page 81) onto 1.2** (PDF 20 to 21, printed 9 to 10). PMBOK gives no field list ("not stated in the book"); the eight columns are the Book's Table 1.2.

| PMBOK content | Form 1.2 column | If no box |
| --- | --- | --- |
| Assumptions and constraints, high level from the business case, lower level raised during the project | ID, Category, Assumption/Constraint | Source (business case, team, sponsor) goes in Comments |
| Validation of an assumption | Responsible Party, Due Date, Actions | |
| Status (Book: active, transferred, closed) | Status | |
| Constraints | Same table, or a separate log on a very large project (Book tailoring tip) | |

Later processes add and close rows: 4.3.3.6 (printed page 97), read by 4.5.1.2 (page 108) and 4.7.1.3 (page 124).

**4.2.3.1 Project management plan (printed pages 86 to 88, PDF 125 to 127) onto 2.1 and 2.2** (2.1: PDF 31 to 33; 2.2: PDF 36 to 37)

| PMBOK component | Form box | If no box |
| --- | --- | --- |
| Scope, schedule, cost, quality, resource, communications, risk, procurement, stakeholder engagement plans | 2.1 Subsidiary Management Plans rows Scope, Time, Cost, Quality, Resource, Communications, Risk, Procurement, Stakeholder | |
| Requirements management plan; configuration management plan | No row | Other Plans (the Book does not say where) |
| Change management plan | Other Plans, and its own form 2.2 | |
| Scope, schedule, cost baselines; performance measurement baseline | 2.1 Baselines (attach); the three Baseline Management boxes | Performance measurement baseline: attach, name it |
| Project life cycle | Project Life Cycle (Phase with Key Activities, Key Deliverables; Phase with Reviews, Entry Criteria, Exit Criteria) | Entry criteria: not described in chapter 4, Book Table 2.1 only |
| Development approach | Development Approaches | |
| Management reviews | Reviews column | |
| Variance thresholds (PMBOK 4.5.1.3, page 109, says they live in the plan) | Scope, Schedule, Cost Variance Threshold | |
| Change management plan content: how requests are authorized and incorporated; CCB roles and authority (4.2.3.1; 4.6.1.1, page 116; 4.6.2.5, page 120) | 2.2 Change Management Approach; Change Control Board (Name, Role, Responsibility, Authority) | |
| Change request steps (4.6.2.2, page 119: identify, document, decide, track) | 2.2 Change request submittal, tracking, review, disposition | Mapping is a reading: submittal covers identify and document, tracking covers track, review and disposition cover decide |
| Which documents are under formal change control (4.2.2.1, page 85) | 2.2 Project document changes | Configuration items, status, audit (4.6.2.2): no 2.2 box; Book tip allows one combined plan |
| 2.3 Project Roadmap | Approach; Life Cycle Phases; Timeline | The Book says PMBOK 6 lists no roadmap output (PDF 39, printed 28); it draws on 4.2.3.1 life cycle and reviews and on the milestone list |

**Change requests and decisions: 4.3.3.4 (page 96), 4.5.3.2 (page 112), 4.6.1.4 (page 117), 4.6.3 (page 120) onto 3.3, 3.4, 3.2**

| PMBOK content | Form box | If no box |
| --- | --- | --- |
| Requestor; reason | 3.3 Requestor; Justification for Proposed Change | |
| Type: corrective, preventive, defect repair, update; mandatory or optional | No box (Category prints Scope, Quality, Requirements, Cost, Schedule, Documents) | Name the type in Detailed Description of Proposed Change; the Book allows a mandatory-or-discretionary check box as tailoring |
| Impact: cost of the change, changed dates, resource requirements, risks (4.6.1.4) | Cost, Schedule descriptions | Resource requirements and risks have no box: Cost or Schedule Description, Project Documents, Comments |
| Impact on project documents | Project Documents label inside the Stakeholder Impact box | |
| Approved, deferred, rejected | 3.3 Disposition and Justification; 3.4 Disposition | 3.4 Status (Book Table 3.4: open, pending, closed) has no PMBOK source |
| Change log: list of changes and status; every disposition recorded (4.6.3.2) | 3.4 ID, Category, Description of Change, Requestor, Submission Date, Status, Disposition | |
| Decisions generally | 3.2 ID, Category, Decision, Responsible Party, Date, Comments | PMBOK has no decision log (Book PDF 179, printed 168); alternatives and reason go in Comments |

**Status, knowledge, closure**

| PMBOK content | Form box | If no box |
| --- | --- | --- |
| 4.5.3.1 reports: progress and status; earned value graphs, trend lines, forecasts, reserve burndown, defect histograms, risk summaries | 4.2 accomplishment, variance, impact, funds, corrective or preventive action boxes | Graphs, forecasts, reserve burndown: attach or tailor (Book: dashboards); earned value goes to 4.4 |
| 4.5.3.2 change requests from the period | No box | Book tip: summarise and point to the change log |
| 4.5.3.4 new risks, new issues, lessons | New Risks Identified; Issues | Lessons: Book tip, field feeding 3.5 |
| 4.4.3.1 lessons: category, description; may add impact, recommendations, proposed actions | 3.5 ID, Category, Trigger, Lesson, Responsible Party, Comments | Impact, recommendation and action go in Lesson and Comments |
| 4.7.3.1 final lessons register: benefits, business case accuracy, life cycles, risk and issue, stakeholder, other processes | 5.1 rows and Risks and Issues | Benefits, business case accuracy, life cycle: row Other (a reading) |
| 4.7.3.4 lessons learned repository | 5.1 is the summary stored in it (Book PDF 241, printed 230) | |
| 4.7.3.3 final report: description; scope objectives, criteria, evidence; quality objectives, verification, milestone dates; cost objectives, acceptable range, actuals, reasons; validation; benefits and degree; business needs; risks and issues | 5.2 Project Description; Performance Summary Scope and Quality rows; Variances Time and Cost rows; Benefits Management; Business Needs; Risks and Issues | Acceptable cost range: Cost row Comments; validation: Quality How Met from form 4.9 |
| 4.7.3.2 final product transition; closure activities (release staff, close accounts, archive, stakeholder satisfaction) | No box | Closeout report text or the project's own closeout checklist |

## Where this project's facts live

| Form | Where |
| --- | --- |
| 1.1 | `docs/charter-package.en.md` Part 2A (headings follow 4.1.3.1 order) and Part 2B (the printed form). 2A and 2B differ in places; copy from 2B for a form |
| 1.2 | Charter section 1.6, assumptions 1 to 19, and section 1.5 constraints. No owner, due date, action or status exists for any row: leave them empty |
| 2.1 | No document. Life cycle: milestones M0 to M7 (2A) and WBS phases 1.1 to 1.10 (scope package Part 2). Baselines: scope = charter Part 1 plus WBS plus dictionary (scope package, how organised); cost = 2A budget lines 1 to 6; schedule = charter dates, form 2.18 unbaselined. Thresholds: 2A Cost criterion, PM Budget Management and Variance. Plan work package 1.1.1.2 |
| 2.2 | No document. Authority in 2A (Budget Management and Variance, Technical Decisions, Sponsor Authority); R2 response; work package 1.1.1.4; no CCB named anywhere |
| 2.3 | No document. Charter 2A milestones; `docs/forms/2-18-project-schedule.en.md` page 2 milestone chart |
| 3.2 | No document. Work package 1.1.1.3, activity A3 "Sponsor escalations and decision log"; sponsor options on failed UAT in 2A approval requirements |
| 3.3 | `docs/forms/3-3-change-request.en.md` (re-baseline of M1 to M7 to the levelled 2.18; disposition empty) |
| 3.4 | No document; the request above is the first row |
| 3.5 | No document. Closeout work package 1.10.2.1; internal deliverable "lessons learned" at M7 |
| 4.2 | No document. Work package 1.1.1.3 (weekly report to sponsor and Center Director, template fixed at M1); charter section 1.2 internal deliverables |
| 5.1, 5.2 | No document. Work package 1.10.2.1; 2A exit criteria 1 to 10, benefit table and owner (Accountant), R11; deliverable D10 |

## Traps

- The charter is issued by the initiator or sponsor, though the sponsor or the
  project manager may develop it (4.1, printed page 77; 4.1.3.1, page 81). The
  Project Manager box is empty in 2B because the sponsor names the PM by 14
  September 2026 (work package 1.1.1.1); PMBOK wants the PM named before planning
  starts (page 77), and planning work package 1.1.1.2 starts 21 September, so
  that agrees.
- The charter's Cost criterion in 2B page 2 says "management reserve use reported
  monthly" and 2A says "reserve use". Budget line 6 is a contingency reserve inside
  the cost baseline; a management reserve sits outside it and needs an approved
  baseline change to be used (7.3.2.3, printed page 252; 7.3.3.1, printed page 254).
- The scope package says change requests are outputs of 5.5 and 5.6 only. PMBOK
  says many processes produce them, 4.3 and 4.5 among them (4.3.3.4, page 96;
  4.5.3.2, page 112; 4.6.1.4, page 117).
- Form 2.1 asks for acceptable, warning and unacceptable bands. The charter has
  two: inside the PM's 5 percent, and escalate beyond it. Do not invent the
  middle band; the sponsor "sets acceptable variance limits" (Sponsor Authority).
  The Book's 0 to 5, 5 to 10, over 10 percent is only its example (PDF 33,
  printed 22).
- No document names a CCB, a configuration management plan, or which documents are
  under formal change control (4.2.2.1, printed page 85). Work package 1.1.1.2
  names the plan, schedule, resource and communication plans only. Leave those
  boxes empty and ask; do not assign the sponsor as CCB without saying it is a proposal.
- Work package 1.1.1.2 says the charter dates are "not renegotiated", yet request
  3.3 re-baselines them. PMBOK allows free updates only before a baseline exists
  (printed pages 83, 115). Say which date set is the baseline today; the sponsor decides.
- Lessons are planned only at M7. PMBOK creates the register early and updates it
  throughout, captured by the people doing the work (4.4.3.1, printed page 104).
  A 5.1 built from a register that was never kept is memory, say so.
- 5.2 benefits: at M7 the overdue percentage can be measured, not the full benefit.
  PMBOK wants the degree achieved and an estimate of future realization when
  benefits are unmet at close (4.7.3.3, printed page 128). State actual versus target.
- Closing needs the issue log to show no open issue and the risk report no open
  risk (4.7.1.3, printed pages 124 to 125). Exit criterion 7 covers defects only.
- Two registers for one decision: a change disposition lives in the change log
  (4.6.3.2, page 120). Copy it into 3.2 verbatim or not at all.
- The status report is compiled from team member reports (Book PDF 207); no team
  member status report (form 4.1) exists in docs, so say what the weekly report was compiled from.
- The Book's Table 3.2 names the date column Priority; the blank form prints Date.

## Decisions in this area

**D1. Authorize the project and set the project manager's authority**
- Arises: 4.1, once or at predefined points; the project is initiated by an entity outside it (sponsor, program, PMO or portfolio body) and the charter may be developed by the sponsor or the PM in collaboration with that entity (printed page 77). That it is the sponsor's decision and not the PM's is the project's rule from the charter's authority section, not book text.
- Techniques: expert judgment; data gathering by brainstorming, focus groups, interviews; conflict management, facilitation, meeting management; meetings (4.1.2, printed pages 79 to 80). Trade-offs: not stated in the book.
- Inputs: business case, benefits plan, agreements, stakeholders' risk thresholds (4.1.1, printed pages 77 to 78). Here: charter Part 1, 2A purpose and business case, section 1.5.
- Records: 1.1 Approvals, Project Manager Authority Level boxes, Sponsor Authority, Preapproved Financial Resources; a later change to the charter is a 3.3.
- Formula: none.
- Wrong move: treating the charter as a contract, or the PM editing the business case. The book: no consideration or money is exchanged (page 77); business documents are not project documents, the PM may only recommend (page 78).

**D2. Which assumptions and constraints to record, and who validates them**
- Arises: 4.1 first; new ones in 4.3 (printed page 97); read by 4.5 and 4.7.
- Techniques: none named. The book: assumptions are validated and then stop being assumptions (Book PDF 20, printed 9). Trade-offs: not stated in the book.
- Inputs: business case, charter section 1.5 and 1.6, estimates. Here: charter 1.6, assumptions 1 to 19.
- Records: 1.2 Responsible Party, Due Date, Actions, Status; a baseline change a failed assumption forces goes to 3.3.
- Formula: none.
- Wrong move: leaving an assumption without owner, due date or action. The book: the log exists to follow each one up (Book PDF 21, printed 10), and it feeds the schedule, estimates and risk register (Book PDF 20, printed 9).

**D3. Life cycle, development approach and management reviews**
- Arises: 4.2 planning, tailored per project (4.1 tailoring, printed page 74; 4.2.3.1, page 88).
- Techniques: expert judgment on tailoring and on dependencies between processes (4.2.2.1, page 85); predictive (scope known and stable) versus adaptive (scope evolving) versus iterative or incremental (Book Table 2.1, PDF 32). Trade-offs: the Book ties change rigor to the choice, rigorous for predictive, evolving scope allowed for adaptive (Book PDF 36); PMBOK delegates detailed planning to the team in adaptive work (page 74).
- Inputs: charter, outputs of other planning processes. Here: M0 to M7, iterations at M3 and M4, WBS 1.1 to 1.10.
- Records: 2.1 Project Life Cycle, Development Approaches, Reviews; 2.3 Life Cycle Phases.
- Formula: none.
- Wrong move: a phase gate with no entry or exit criteria written down. Chapter 4 gives none, so say "not stated in the book" and take them from the charter exit criteria and the milestone list.

**D4. When to baseline, thresholds, and what is under formal control**
- Arises: the plan should be baselined, defining at least the scope, time and cost references (printed page 83); the book gives no rule for when. The kick-off is usually associated with the end of planning and start of executing (printed page 86): small projects shortly after initiation, large projects at the start of executing, multiphase at each phase.
- Techniques: expert judgment on configuration level and which documents are controlled (page 85); brainstorming, checklists, focus groups, interviews (page 85). Trade-offs: not stated in the book.
- Inputs: subsidiary plans and baselines from every planning process, stakeholders' expectations and risk thresholds (4.1.1.3, page 78; 4.3.1.4, page 93). Here: scope package, charter budget, 2A criteria.
- Records: 2.1 Variance Threshold and Baseline Management boxes, Baselines; 2.2 Definitions of Change. Example band only: cost 0 to 5, 5 to 10, over 10 percent (Book PDF 33).
- Formula: none in chapter 4; variance is reported with the 7.4.2.2 formulas under D7.
- Wrong move: rebaselining without a request once baselined, or changing history to hide a variance. The book: once baselined, change only through 4.6 (page 83); baselines change from the last baseline forward and past performance is not changed (4.6.3.2, page 120).

**D5. Classify a change request and choose its approval level**
- Arises: 4.3 or 4.5 or any controlling process finds a gap; any stakeholder may ask (page 96).
- Techniques: type is corrective action, preventive action, defect repair or update (page 96). Level: a change affecting only performance against a baseline is usually the PM's decision; one that moves a baseline needs the CCB if one exists and the customer or sponsor (4.6.1.4, page 117). Revision versus change (Book PDF 33): a revision needs less approval.
- Inputs: baselines, change management plan, configuration management plan, basis of estimates, requirements traceability matrix, risk report (4.6.1, pages 116 to 117). Here: 2A authority, scope package.
- Records: 3.3 Category, Impacts of Change, Description; 3.4 Category, Status; 2.2 Definitions of Change.
- Formula: none.
- Wrong move: implementing before disposition. The book: only approved changes enter a revised baseline (page 117), and approved requests are carried out by 4.3 (page 120).

**D6. Approve, defer or reject a change request**
- Arises: 4.6 after a request carries cost, date, resource and risk information (page 117); the responsible individual is named in the plan or by the organization, usually sponsor or PM (page 115).
- Techniques and stated features: alternatives analysis (accept, reject or modify) and cost-benefit analysis (is it worth its cost) (4.6.2.3, page 119); voting: unanimity means everyone agrees, majority means over 50 percent and an odd group avoids ties, plurality means the largest block decides, used when more than two options (5.2.2.4, page 144); autocratic: one person is responsible (page 119); multicriteria decision analysis: weighted criteria give each alternative a score and a rank (8.1.2.4, page 283). Further trade-offs: not stated in the book.
- Inputs: the request, work performance reports (resource availability, schedule and cost data, earned value, burn charts, 4.6.1.3), risk report. Here: sponsor authority in 2B page 4.
- Records: 3.3 Disposition (Approve, Defer, Reject) and Justification; 3.4 Disposition; 3.2 if kept as a decision. Updating a baseline needs the matching plan update.
- Formula: none.
- Wrong move: closing a constraint gap by cutting an estimate or silently compressing. The book: changes made without regard to overall objectives raise overall project risk, which is why 4.6 weighs them in an integrated way (page 113). The route is a 3.3 to the sponsor.

**D7. Respond to a variance: corrective, preventive or defect repair**
- Arises: 4.5, whenever work performance information compared with the plan exceeds a variance threshold (page 109).
- Techniques: alternatives analysis picks the corrective or preventive action; cost-benefit analysis picks the cheapest effective one; root cause analysis finds why; trend analysis forecasts and supports preventive action; variance analysis compares planned with actual across cost, time, technical and resources together; earned value analysis integrates scope, schedule, cost (4.5.2.2 and 4.5.2.3, page 111); voting may decide. Trade-offs: not stated in the book.
- Inputs: work performance information, cost and schedule forecasts, basis of estimates, thresholds in 2.1, lessons register. Here: thresholds in 2A.
- Records: 4.2 Root Cause of Variances, Impact to Upcoming Milestones or Project Due Date, Impact to Overall Budget or Contingency Funds, Planned Corrective or Preventive Action; a baseline effect becomes 3.3.
- Formulas (7.4.2.2, plain minus sign): SV = EV - PV (page 262); CV = EV - AC (page 262); VAC = BAC - EAC (page 262); SPI = EV/PV (page 263); CPI = EV/AC (page 263). EV earned value, PV planned value, AC actual cost, BAC budget at completion, EAC estimate at completion, all in VND here; SPI and CPI have no unit; SPI below 1.0 means less work done than planned, CPI below 1.0 means a cost overrun on the work done. Chapter 4 itself gives no formula.
- Wrong move: reading a figure without its context. The book: funds spent alone say nothing until compared with budget, work done and thresholds (4.5.1.3, page 109).

**D8. What knowledge to capture and how to share it**
- Arises: 4.4 throughout; register created early (page 104); closure moves it to the repository.
- Techniques: knowledge management, which connects people (networking, communities of practice, workshops, work shadowing, storytelling, page 103), versus information management, which codifies explicit knowledge (register, library, PMIS, page 103). Stated trade-off: codified knowledge shares easily but lacks context and gets misread; tacit knowledge keeps context but is hard to write down (page 100); face-to-face builds the trust that sharing needs (page 103).
- Inputs: plan, lessons register, team assignments, resource breakdown structure, stakeholder register, deliverables (4.4.1). Here: no register yet.
- Records: 3.5 Category, Trigger, Lesson, Responsible Party; 5.1 at close.
- Formula: none.
- Wrong move: believing knowledge management is documenting, or collecting lessons only at the end. The book names both as misconceptions (page 100).

**D9. Close a phase or the project, or end it early**
- Arises: 4.7 at the end of a phase or project; early if the charter's exit conditions to close or cancel are met (4.1.3.1; 4.7, page 123).
- Techniques: document analysis, regression analysis, trend analysis, variance analysis; expert judgment; meetings to confirm acceptance and exit criteria (4.7.2, pages 126 to 127). Trade-offs: not stated in the book.
- Inputs: charter, plan, accepted deliverables, change log, issue log, risk report, lessons register, business case and benefits plan, agreements (4.7.1). Here: 2A exit criteria 1 to 10, M7.
- Records: 5.2 all boxes; 5.1; 1.1 Project Exit Criteria is the test; an early stop needs documented reasons and a transfer of finished and unfinished work (page 123, page 128).
- Formula: none; variance analysis here compares plan with final result.
- Wrong move: closing with open issues or risks, or reporting a target as achieved. The book: the issue log must show none open and the risk report none open (pages 124 to 125); unmet benefits are reported with the degree reached and a future estimate (page 128).
