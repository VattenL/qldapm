# PMBOK 6 chapter 5, Project Scope Management, for the scope forms

Read this before filling 2.4 Scope Management Plan, 2.5 Requirements Management Plan, 2.6 Requirements
Documentation, 2.7 Requirements Traceability Matrix, 2.8 Project Scope Statement, 2.9 Work Breakdown
Structure, 2.10 WBS Dictionary or 4.9 Product Acceptance Form. The forms print the boxes; chapter 5 says
what each process outputs and which technique makes it. The last section lists the decisions a project
manager makes in this area, with the PMBOK technique names a proposed remedy has to carry.

## Where it is

`PMBOK6_and_Agile_Practice_Guide.pdf` at the repo root. Guide part: PDF page = printed page + 39; cite
"PMBOK 6 section 5.4.3.1, printed page 161 (PDF page 200)". Contents pages: PDF page 11. Chapter 5 is
wholly in the Guide part. Short form used from here on, so every claim keeps both numbers: **p161/200** is
PMBOK 6 printed page 161, PDF page 200; **BoF 2.8 p46/57** is Book of Forms form 2.8, printed page 46, PDF
page 57 (PDF = printed + 11).

| Section | Printed / PDF page |
| --- | --- |
| 5 Overview, key concepts (scope baseline, predictive versus adaptive), trends, tailoring, agile | 129 to 133 / 168 to 172 |
| 5.1 Plan Scope Management (5.1.3.1 scope management plan; 5.1.3.2 requirements management plan, both p137/176) | 134 to 137 / 173 to 176 |
| 5.2 Collect Requirements (techniques 5.2.2 p142 to 147/181 to 186; 5.2.3.1 p147/186; 5.2.3.2 p148/187) | 138 to 149 / 177 to 188 |
| 5.3 Define Scope (5.3.3.1 scope statement p154/193; Table 5-1 charter versus scope statement p155/194) | 150 to 155 / 189 to 194 |
| 5.4 Create WBS (5.4.2.2 decomposition p158 to 161/197 to 200; 5.4.3.1 scope baseline p161/200, dictionary p162/201) | 156 to 162 / 195 to 201 |
| 5.5 Validate Scope (5.5.3 outputs p166 to 167/205 to 206) | 163 to 167 / 202 to 206 |
| 5.6 Control Scope (scope creep p168/207; 5.6.3.3 plan updates p171/210) | 167 to 171 / 206 to 210 |

Book of Forms, prose pages then blank pages, as printed / PDF:

| Form | PMBOK process | Prose | Blank form |
| --- | --- | --- | --- |
| 2.4 | 5.1 | 30 to 31 / 41 to 42 | 32 / 43 |
| 2.5 | 5.1 | 33 to 34 / 44 to 45 | 35 to 36 / 46 to 47 |
| 2.6 | 5.2 | 37 to 38 / 48 to 49 | 39 / 50 |
| 2.7 | 5.2 | 40 to 42 / 51 to 53 | 43 to 44 / 54 to 55 |
| 2.8 | 5.3 | 45 to 46 / 56 to 57 | 47 to 48 / 58 to 59 |
| 2.9 | 5.4 | 49 to 50 / 60 to 61 | 51 / 62 |
| 2.10 | 5.4 | 52 to 54 / 63 to 65 | 55 / 66 |
| 4.9 | 5.5 | 226 / 237 | 227 / 238 |
| 3.2 Decision Log, 3.3 Change Request | route to 4.6 | 168 / 179; 170 to 171 / 181 to 182 | 169 / 180; 172 to 174 / 183 to 185 |

`pdftotext -layout` interleaves a vertical watermark of 1 to 3 letter lines and a "PMI Member benefit"
footer; drop them before reading. In the course lecture notes "chapter 5" may mean something else; for a
scope form it means PMBOK 6.

## Chapter 5 terms, with the book's meaning

- **Product scope, project scope** (p131/170): features and functions of the product, against the work done
  to deliver them. Project scope is measured against the project management plan, product scope against the
  product requirements. **Requirement** (p131/170): a condition or capability a product, service or result
  must have to satisfy an agreement or other formally imposed specification.
- **Scope baseline** (p131/170, p161/200): the approved scope statement, WBS and WBS dictionary, changed only
  by formal change control, the basis for comparison in Validate Scope and Control Scope. Requirements
  documentation and the RTM are project documents, not part of it.
- **Predictive and adaptive** (p131/170): predictive runs Collect Requirements, Define Scope and Create WBS
  near the start and updates them through integrated change control; adaptive repeats those three plus
  Validate Scope and Control Scope in every iteration, against a backlog.
- **Work package, control account, planning package, code of accounts** (p161/200): the work package is the
  lowest WBS level, has a unique identifier, and identifiers form the code of accounts. A control account is
  a management control point where scope, budget and schedule are integrated and compared with earned value;
  it has two or more work packages and each work package belongs to one control account. A planning package
  sits between them, with known work content but no detailed schedule activities.
- **Decomposition** (p158/197): dividing deliverables into smaller parts; the work package is the level where
  cost and duration can be estimated and managed. **100 percent rule** (p161/200): the lowest levels roll up
  so nothing is left out and no extra work is performed. **Rolling wave planning** (p160/199): wait to detail
  a deliverable far in the future until it is agreed. **Progressive elaboration**: scope statement, WBS and
  dictionary get more specific as information arrives (BoF 2.8 p46/57; BoF 2.10 p52/63).
- **Verified deliverable** (p165/204): complete and checked for correctness by Control Quality. **Accepted
  deliverable** (p166/205): meets the acceptance criteria and is formally signed off by the customer or
  sponsor. Validate Scope is about acceptance, Control Quality about correctness, and Control Quality
  generally comes first (p164/203).
- **Scope creep** (p168/207): uncontrolled expansion of scope without adjustments to time, cost and resources.

## How each process output maps onto the forms

A component with no box goes in the nearest box and is named in the italic reading paragraph above the
form, never inside the form. Placements marked "judgement" are this note's reading, not the book's.

**2.4 from 5.1.3.1** (p137/176; boxes per BoF Table 2.3, p31/42).

| PMBOK 5.1.3.1 component | Form 2.4 box |
| --- | --- |
| Process for preparing the project scope statement | No box; "Scope and Requirements Integration" (how requirements reach the scope statement and WBS), judgement |
| Process that creates the WBS from the scope statement | Work Breakdown (WBS) Structure (arrangement, control account and work package guidelines) |
| Process that establishes how the scope baseline is approved and maintained | Scope Baseline Maintenance (which changes need formal change control; scope change versus revision, BoF 2.4 p30/41) |
| Process that specifies how formal acceptance is obtained | Deliverable Acceptance |
| Not a 5.1.3.1 component; BoF 2.4 p30/41 says the plan may direct what the dictionary holds | WBS Dictionary |
| Table 2.3 sixth element, project management and business analysis integration | No box on the blank form; inside Scope and Requirements Integration |

**2.5 from 5.1.3.2** (p137/176, five components; BoF Table 2.4, p34/45).

| PMBOK 5.1.3.2 component | Form 2.5 box |
| --- | --- |
| How requirements activities are planned, tracked and reported | Tracking; Reporting |
| Configuration management: how changes are initiated, impacts analysed, traced, tracked, reported; authorization levels | Configuration Management |
| Requirements prioritization process; metrics and their rationale; traceability structure | Prioritization; Metrics; Traceability Structure |
| No 5.1.3.2 component. Source: 5.2.2 techniques, 5.2.3.1 classifications and format, 5.5.1.1 (the plan says how requirements are validated, p165/204) | Collection; Analysis; Categories; Documentation; Validation |

**2.6 from 5.2.3.1** (p147 to 148/186 to 187). The PMBOK gives no field list, only readiness tests and classifications.

| PMBOK 5.2.3.1 content | Form 2.6 box |
| --- | --- |
| Classifications: business, stakeholder, solution (functional, nonfunctional), transition and readiness, project, quality | Category |
| Unambiguous (measurable and testable) | Acceptance Criteria; Test or Verification |
| Traceable | ID, linked through form 2.7 |
| Complete, consistent, acceptable to key stakeholders | No box; a check before baselining (decision 3); Stakeholder names who must accept |

**2.7 from 5.2.3.2** (p148 to 149/187 to 188; BoF Tables 2.6 and 2.7, p42/53).

| PMBOK 5.2.3.2 item | Form 2.7 box |
| --- | --- |
| Unique identifier; textual description; source; priority | ID; Requirement; Source; Priority |
| Trace to business needs, goals, objectives and to project objectives | Business Objective (Figure 5-7 has a column for each; the form has one) |
| Trace to project scope and WBS deliverables | Deliverable |
| Trace to test strategy and scenarios; how the requirement is validated | Verification (metric); Validation (technique) |
| Trace high-level to more detailed requirements | Page 2, Inter-Requirements Traceability Matrix |
| Trace to product design and development | No box |
| Rationale, owner, version, status, status date, stability, complexity, acceptance criteria | No box on 2.7. Acceptance criteria live in 2.6 and 4.9, status in 4.9; the rest are a named tailoring or omitted |
| After Validate Scope, the method used and the outcome (5.5.3.4, p167/206) | No box; outcome in 4.9 Status and Comments |

**2.8 from 5.3.3.1** (p154/193; BoF Table 2.8, p46/57).

| PMBOK 5.3.3.1 component | Form 2.8 box |
| --- | --- |
| Product scope description (the statement covers project and product scope) | Project Scope Description |
| Deliverables; acceptance criteria; project exclusions | Project Deliverables; Product Acceptance Criteria; Project Exclusions |
| Assumptions and constraints (first sentence of 5.3.3.1; assumptions also go to the assumption log, 5.3.3.2, p155/194) | Project Constraints; Project Assumptions (page 2 only) |

**2.9 from 5.4.2.2 and 5.4.3.1.** The blank form is an outline whose placeholder words are Project, Major
Deliverable, Control Account, Work Package (BoF 2.9 p51/62). Level 2 is the organising choice: phases (Figure
5-13), major deliverables (Figure 5-14) or contracted subcomponents (p159/198). A planning package has no
printed line; if used it sits between a control account and its work packages and the reading paragraph names
it. The printed outline codes are the identification codes of 5.4.2.2.

**2.10 from the 5.4.3.1 dictionary list** (p162/201; boxes per BoF Table 2.10, p54/65).

| PMBOK dictionary item | Form 2.10 box |
| --- | --- |
| Code of account identifier; description of work; assumptions and constraints; schedule milestones | Code of Accounts; Description of Work; Assumptions and Constraints; Milestones with Due Dates |
| Associated schedule activities; resources required; cost estimates | Cost table: ID, Activity, Resource, Labor (Hours, Rate, Total), Material (Units, Cost, Total), Total Cost |
| Quality requirements; acceptance criteria; technical references; agreement information | Quality Requirements; Acceptance Criteria; Technical Information; Agreement Information |
| Responsible organization (BoF 2.10 p52/63 lists "organization or person") | No box, and the fields note says do not add one. Name the owner in Description of Work, or name an extra row as a tailoring |
| Not a PMBOK item | Work Package Name |

**4.9 from 5.5.** Inputs: verified deliverables, requirements documentation, RTM (p165/204). Outputs:
accepted deliverables, work performance information, change requests, document updates (p166 to 167/205 to 206).

| PMBOK 5.5 content | Form 4.9 column |
| --- | --- |
| Requirement and identifier from the requirements documentation; acceptance criteria; how it is validated (RTM) | ID; Requirement; Acceptance Criteria; Validation Method |
| Accepted or not accepted (5.5.3.2) | Status |
| Reasons a deliverable was not accepted (5.5.3.3, p166/205) | Comments (a column BoF Table 4.9, p226/237, does not list) |
| Formal sign-off by the customer or sponsor (5.5.3.1) | Sign-off |
| Change request for defect repair of a non-accepted deliverable | No column; raise form 3.3 and cite its ID in Comments |

## Where this project's scope facts live

| Form | Where in `docs/` | Note |
| --- | --- | --- |
| 2.4, 2.5 | No separate document. Rules are scattered: `scope-package.en.md` "Decomposition method", "Reading convention", "Inputs actually used" (says no separate scope management plan); charter Part 2A "Assigned project manager, responsibility, and authority level" and "Project approval requirements"; work packages 1.1.1.4, 1.8.3.2 | The book allows an informal plan or a combined 2.4 and 2.5 (BoF 2.4 p30/41); the rules must still exist in writing |
| 2.6 | No form. Charter sections 1.1.4 (F01 to F12), 1.1.5 (exception behaviour), 1.3 (A01 to A12) | `docs/requirements.md` is the course brief, not a requirements list |
| 2.7 | `scope-package.en.md` Part 1 and Part 1B (BR, FR, NFR families) | Every Priority is Must have; the reading paragraph says why, once. Output of 5.2, built before the WBS |
| 2.8 | `charter-package.en.md` Part 1: 1.1 description, 1.2 deliverables D1 to D11, 1.3 criteria A01 to A12, 1.4 exclusions, 1.5 constraints, 1.6 assumptions 1 to 19; charter-level versions in Part 2A | Table 5-1 (p155/194): the charter is high-level, the statement elaborates it; the two must agree |
| 2.9 | `scope-package.en.md` Part 2 (10 major deliverables, 24 control accounts, 78 work packages), "Roll-up", "Coverage check" | Level 2 is major deliverables in life-cycle order |
| 2.10 | `scope-package.en.md` Part 3, one sheet per work package | Totals fixed by the charter (hours, labor, other cost, budget); `tools/check_scope.py` enforces them |
| 4.9 | No form. Charter Part 2A "Project approval requirements" (who signs what, with evidence) and "Project exit criteria"; "Coverage check" for the work package that delivers each of D1 to D11; 1.8.3.2 | 1.8.3.2 is "the Validate Scope point of the project"; its sign-off releases the final 25% tranche |
| 3.3, 3.2 | `docs/forms/3-3-change-request.en.md` (the schedule re-baseline); no decision log yet | Reserve draws go through change control, work package 1.1.1.4 |

## Traps

- **Inputs to Create WBS** (Figure 5-10, p156/195): scope management plan, project scope statement,
  requirements documentation, enterprise environmental factors, organizational process assets. The charter
  is an input to 5.1 to 5.3, not 5.4; the RTM is an output of 5.2, not an input to 5.4.
- **The 8 to 80 hour rule is not in the book.** It is a class note (`docs/wbs_notes.md`) adopted as the
  project's own rule. The book says the level is "guided by the degree of control needed" (p158/197) and
  gives no hour range; do not cite PMBOK for it.
- **Work packages are deliverables, not activities** (p157/196: work "refers to work products or
  deliverables that are the result of activity and not to the activity itself"). Names such as "Kickoff and
  team mobilisation" or "Weekly status reporting" read as activities; check each one.
- **Control accounts need two or more work packages** (p161/200). In Part 2 of the scope package, 1.4.4 and
  1.10.2 each hold one (1.4.4.1, 1.10.2.1). Report it; the fix (add a package, merge into a neighbour, or use
  a planning package) changes the baseline and goes to the sponsor.
- **Unprinted box on 2.10.** The scope package adds a Responsible Person row. Its Part 3 preamble names it,
  the allowed route, but `check_fidelity.py` lists it as an unprinted label.
- **Acceptance is not testing** (p164/203). Test execution in 1.6.1 is Control Quality; the sign-offs of 1.6.2
  and 1.8.3.2 are Validate Scope. Do not write "accepted" in a test report.
- **Change requests come from 5.5 and 5.6 only among the scope processes** (Figure 5-1, p130/169); 5.1 to 5.4
  output none. BoF 3.3 p170/181 says a request can come from almost any process; both hold, and neither
  lets a planning artifact raise one.
- **Printed labels beat PMBOK wording**: 2.8 prints "Product Acceptance Criteria" and "Project Scope
  Description"; 2.7 prints Priority before Category; 4.9 prints Comments. Use the printed ones.
- **No document defines "scope change versus revision" or a scope-variance threshold.** The book asks the
  scope management plan for the first (BoF 2.4 p30/41) and states no value for the second (5.6.2.1,
  p170/209). The only thresholds in `docs/` are cost: the cumulative variance limit, and the reserve use limit above
  which the sponsor decides (charter, PM authority; read both there).
- **Product versus project**: a fourth branch is why the center wants the system, not work the project does;
  exclusions come in two lists (`review-lessons.md` section 4). A pending change request does not change the
  baseline; build 2.8 to 2.10 from the approved versions and say which rows 3.3 would change.

## Decisions in this area

Chapter 5 states no numeric threshold and no equation. The only arithmetic is the form 2.10 cost table (BoF
Table 2.10, p54/65): **Labor Total = Hours x Rate** (hours; rate in VND per hour; result VND); **Material
Total = Units x Cost** (units; cost in VND per unit; VND); **Total Cost = Labor Total + Material Total + any
other costs of the work package** (VND). The 100 percent rule (p161/200) is stated in words: the lowest
levels roll up, nothing left out, nothing extra. Majority is "more than 50%" of the group (p144/183); the
nominal group technique votes privately, "usually" on a scale of 1 to 5, 5 highest (p145/184). BoF Table 2.4 (p34/45) gives an
illustration, not a rule: a 150 lb requirement designed to 120 percent is 180 lb.

### 1. How formal and how separate the scope and requirements plans are

- **Arises:** 5.1 Plan Scope Management, once or at predefined points (p134/173), after the charter.
- **Techniques and trade-offs:** Expert judgment; alternatives analysis (compares ways to collect, elaborate, validate and control, p136/175); Meetings. The plan may be "formal or informal, broadly framed or highly detailed" (p137/176). Form tailoring: combine 2.4 with 2.5 on smaller projects; add a test and evaluation plan on larger ones; add release and iteration plans if agile (BoF 2.4 p30/41). Adaptive repeats five processes per iteration, predictive does not (p131/170).
- **Inputs, kept in:** charter; development approach and life cycle (scope package "Decomposition method": predictive with two build iterations); quality management plan (`pmbok-quality.md`).
- **Recorded in:** 2.4 (five boxes), 2.5 (eleven boxes); 3.2 for the choice to combine them.
- **Wrong move:** leaving the rules unwritten because the project is small. The plan "provides guidance and direction on how scope will be managed throughout the project" (p134/173).

### 2. Which requirements-gathering technique, for which stakeholders

- **Arises:** 5.2 Collect Requirements, once or at predefined points (p138/177).
- **Techniques and stated fit (p142 to 147/181 to 186):** interviews (individual; also for confidential information); focus groups (prequalified stakeholders, conversational); questionnaires and surveys (varied audiences, quick turnaround, dispersed respondents, statistical analysis); benchmarking; document analysis; observation (users who find it hard to articulate needs); facilitated workshops, JAD, QFD, user stories (build trust, surface issues earlier, reconcile differences); prototypes (feedback cycles until requirements are complete enough to design). No cost or duration comparison is stated.
- **Inputs, kept in:** assumption log (charter 1.6), stakeholder register (charter key stakeholder list), business case, agreements, lessons learned.
- **Recorded in:** 2.5 Collection; 2.6 Stakeholder and Test or Verification; here work packages 1.2.1.1 and 1.2.3.4.
- **Wrong move:** settling on abstract discussion. Prototypes let stakeholders "experiment with a model of the final product rather than being limited to discussing abstract representations" (p147/186).

### 3. Which requirements enter the scope, in what priority, and when they are ready to baseline

- **Arises:** 5.3 Define Scope after 5.2; priority set in 5.2 and the 2.5 Prioritization box; baselining here is work package 1.2.2.3 at milestone M1.
- **Techniques and trade-offs:** voting (unanimity: everyone agrees; majority: more than 50%, an odd group size avoids a tie; plurality: largest block, used when more than two options; autocratic: one individual decides, p144/183); multicriteria decision analysis (decision matrix over criteria such as requirements, schedule, budget, resources, p153/192); alternatives analysis; nominal group technique (p144 to 145/183 to 184). Risk responses may reduce or change scope (p152/191). Readiness test, not a named technique: unambiguous (measurable and testable), traceable, complete, consistent, acceptable to key stakeholders (p147/186).
- **Inputs, kept in:** 2.6; risk register (charter R1 to R12); charter objectives and constraints (1.5); acceptance criteria A01 to A12 (charter 1.3, written as thresholds).
- **Recorded in:** 2.6 Priority, Acceptance Criteria, Test or Verification; 2.7 Verification and Validation; 2.8 Project Scope Description; 3.2 (Decision, Responsible Party, Date). After baselining, a change is a 3.3 (Category Requirements or Scope).
- **Wrong move:** treating everything collected as scope: "all the requirements identified in Collect Requirements may not be included"; Define Scope selects the final ones (p151/190). Some are non-negotiable, such as regulatory ones (BoF 2.5 Table 2.4, p34/45). An untestable requirement cannot be validated, since Validate Scope compares results to the requirement (p165/204).

### 4. What is in scope and what is explicitly out

- **Arises:** 5.3 Define Scope; the statement builds on the charter's deliverables, assumptions and constraints (p151/190).
- **Techniques:** Expert judgment; alternatives analysis (ways to meet requirements and charter objectives); facilitation (workshops for a common view of boundaries); product analysis (p153/192). No trade-off is stated.
- **Inputs, kept in:** charter Part 2A "Project boundaries" (Included, Excluded) and sections 1.4 to 1.6; risk register.
- **Recorded in:** 2.8 Project Exclusions, Project Constraints, Project Assumptions; new assumptions also in the assumption log (charter 1.6).
- **Wrong move:** leaving exclusions implicit. Stating them "helps manage stakeholders' expectations and can reduce scope creep" (p154/193). Form 2.8 wants what is out for the product and the project (BoF Table 2.8, p46/57); keep the two lists apart.

### 5. How to arrange the WBS, how far to decompose, where the control accounts sit

- **Arises:** 5.4 Create WBS, once or at predefined points (p156/195); the step "verifying that the degree of decomposition is appropriate" (p158/197).
- **Techniques and trade-offs:** decomposition; top-down, organization-specific guidelines, WBS templates; bottom-up to group subcomponents; level 2 by phase, by major deliverable, or with contracted subcomponents (p159/198); BoF 2.9 adds geography and subprojects, outline for large projects, org chart for small (p49/60); no ranking, "the needs of the project" decide. More detail "enhances" planning, management and control, but excessive decomposition brings "nonproductive management effort, inefficient use of resources, decreased efficiency in performing the work, and difficulty aggregating data" (p160/199). Branches may stop at different levels. Test: components "necessary and sufficient" for the parent (p160/199). Far-future work: rolling wave planning (p160/199). Planning package: known content, no detailed activities (p161/200). Hour limits: not stated in the book.
- **Inputs, kept in:** 2.4 WBS box, 2.8, 2.6; charter D1 to D11 and M0 to M7; scope package "Decomposition method", Part 2, "Roll-up", "Coverage check".
- **Recorded in:** 2.9 outline (Control Account and Work Package lines); 2.4 Work Breakdown (WBS) Structure; 3.2; a change after baseline is a 3.3.
- **Wrong move:** a control account with one work package, or a work package under two. The book: two or more, and "each work package is associated with a single control account" (p161/200). Also naming packages after activities (p157/196).

### 6. How much to put in the WBS dictionary, and when

- **Arises:** 5.4 output; filled as estimating processes finish ("most of the information ... is created by other processes and added ... at a later stage", p162/201).
- **Options (BoF 2.10 p52 to 53/63 to 64):** full form per work package; summary at control account level; only description of work, cost estimate, key dates and assigned resources; none for small projects; reference other documents for technical, quality and agreement information; mini statement of work for outsourced deliverables.
- **Inputs, kept in:** activity list, milestone list, resource requirements, cost estimates, quality metrics (BoF 2.10 p52/63); scope package Part 3 and the sheet tag "first-pass estimate, re-baselined at M1".
- **Recorded in:** 2.4 WBS Dictionary box (level of detail); 2.10 boxes. Arithmetic: the three cost-table formulas above.
- **Wrong move:** presenting first-pass hours as final. The dictionary is "progressively elaborated" and its inputs are "more detailed than for the WBS" (BoF 2.10 p52/63).

### 7. Accept or refuse a delivered deliverable

- **Arises:** 5.5 Validate Scope, "periodically throughout the project as needed" (p163/202), after Control Quality has verified a deliverable.
- **Techniques:** inspection (measuring, examining, validating; reviews, walkthroughs, p166/205); voting when the team and other stakeholders validate (p166/205). Accepted deliverables go to Close Project or Phase; non-accepted ones are documented with reasons and may need a change request for defect repair into integrated change control (p166/205).
- **Inputs, kept in:** 2.6, 2.7 Validation, 2.4 Deliverable Acceptance, quality reports (8.2); charter approval table, "If UAT does not pass" (three options to the sponsor within two working days) and "Acceptance cannot be withheld for scope that was never in the baseline".
- **Recorded in:** 4.9 Status, Comments, Sign-off; 3.3 for defect repair; 2.7 updated with method and outcome (p167/206).
- **Wrong move:** asking for acceptance of an unverified deliverable, or calling test results acceptance. Validate Scope is "primarily concerned with acceptance", Control Quality "with correctness" (p164/203).

### 8. Is a request or deviation a scope change; when to re-baseline

- **Arises:** 5.6 Control Scope, "throughout the project" (p167/206), on any request or variance.
- **Techniques and trade-offs:** variance analysis (baseline against actual: within the threshold, or corrective or preventive action); trend analysis (improving or deteriorating) (p170/209). Every requested change and recommended action goes through Perform Integrated Change Control (p168/207). Re-baselining: approved changes go into the scope baseline, and "scope variances can be so severe that a revised scope baseline is needed to provide a realistic basis for performance measurement" (p171/210), with consequent changes to the schedule, cost and performance measurement baselines. The threshold is not stated in the book.
- **Inputs, kept in:** scope baseline (2.8 to 2.10), 2.6, 2.7, work performance data; charter PM authority ("anything that changes user-visible scope, the schedule, or the cost goes to the sponsor"); reserve in budget line 6, drawn only through change control.
- **Recorded in:** 3.3 (Category, Impacts of Change, Disposition by the sponsor); 3.2 for a decision inside PM authority; revised 2.8 to 2.10 with a new Date Prepared.
- **Wrong move:** absorbing the request, which is scope creep (p168/207); or re-estimating to keep the old baseline credible. Any plan change goes by change request (p171/210); cutting estimates is not a technique in the chapter, and when constraints cannot all hold the route is a change request (3.3) to the sponsor.
