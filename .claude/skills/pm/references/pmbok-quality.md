# PMBOK 6 chapter 8, Project Quality Management, for the quality forms

Read this before filling 2.23 Quality Management Plan, 2.24 Quality Metrics or
3.6 Quality Audit. The forms print the boxes; chapter 8 says what goes in them
and which technique each one names, and the team expects an approach or a
remedy to carry the PMBOK name for its technique.

## Where it is

`PMBOK6_and_Agile_Practice_Guide.pdf` at the repo root. PDF page = printed
page + 39 in the Guide part, so cite "PMBOK 6 section 8.1.3.1, printed page
286 (PDF page 325)".

| Section | Printed page | PDF page |
| --- | --- | --- |
| 8 Project Quality Management, key concepts, tailoring, agile | 271 to 276 | 310 to 315 |
| 8.1 Plan Quality Management | 277 to 287 | 316 to 326 |
| 8.1.3.1 Quality management plan (its component list) | 286 | 325 |
| 8.1.3.2 Quality metrics | 287 | 326 |
| 8.2 Manage Quality (quality assurance, audits 8.2.2.5) | 288 to 297 | 327 to 336 |
| 8.3 Control Quality (inspection, testing, control charts) | 298 to 306 | 337 to 345 |

`pdftotext -layout` returns the text interleaved with a vertical watermark,
one or two letters per line ("uu", "ro", "tio", "Sa"). Drop lines that are
only such fragments and the "PMI Member benefit" footer before reading, or
the definitions read as broken.

Mind the other course material: in `Bài giảng Quản lý dự án phần mềm.pdf`,
chapter 8 is Kiểm soát dự án (project control) and chapter 9 is Quản lý chất
lượng và kết thúc dự án. "Chapter 8" for a quality form means PMBOK 6.

## How 8.1.3.1 maps onto form 2.23

PMBOK lists seven components; the form prints six boxes. The one without a
box, the quality tools, goes inside the two approach boxes, and the reading
paragraph says so.

| PMBOK 6 8.1.3.1 component | Form 2.23 box |
| --- | --- |
| Quality standards that will be used by the project | Quality Standards |
| Quality objectives of the project | Quality Objectives (Metric or Specification, Measure) |
| Quality roles and responsibilities | Quality Roles and Responsibilities |
| Project deliverables and processes subject to quality review | Deliverables and Processes Subject to Quality Review |
| Quality control and quality management activities planned | Quality Management Approach (8.2, includes audit timing and content, per Table 2.21) and Quality Control Approach (8.3) |
| Quality tools that will be used | No box; named inside the two approach boxes |
| Major procedures: nonconformance, corrective action, continuous improvement | Applicable Quality Procedures (Table 2.21 adds quality audits) |

Inputs 8.1.1 names: charter, requirements, risk and stakeholder plans, scope
baseline (whose acceptance criteria drive the cost of quality), assumption
log, requirements documentation, RTM, risk register, stakeholder register.
The book's Alignment list for 2.23 is charter, scope, requirements and
resource management plans, and procurement documents. This project has no
separate scope, requirements or resource management plan, so say in the
reading paragraph which of them exist and cite the charter and the WBS
dictionary for the rest.

## Chapter 8 terms worth using, with the book's meaning

- **Prevention over inspection** (key concepts, printed page 274): design
  quality in; it is cheaper than finding defects. The WBS's assurance control
  accounts and the exception catalogue that becomes negative test cases are
  this project's prevention.
- **Cost of quality** (8.1.2.3, Figure 8-5): prevention and appraisal costs
  (conformance) against internal and external failure costs
  (nonconformance). Warranty work is an external failure cost.
- **Manage Quality is quality assurance** (8.2): it checks the processes. A
  **quality audit** (8.2.2.5) is "a structured, independent process", usually
  by a team external to the project; scheduled or random. Form 3.6 records
  one. An audit by the project's own QA engineer is not independent; say so if
  that is what the plan proposes.
- **Control Quality** (8.3) checks the product: inspection (reviews, peer
  reviews, walkthroughs), testing, check sheets, statistical sampling,
  control charts, performance reviews. Its outputs are quality control
  measurements and **verified deliverables**, which go to Validate Scope
  (5.5). In this project that hand-off is UAT, 1.8.3.2 in the scope package.
- **Quality metric** (8.1.3.2): an attribute and how Control Quality will
  verify it. A01 to A12 are written as thresholds so each one already is a
  metric; form 2.24 adds the how.
- **Continuous improvement**: plan-do-check-act; retrospectives and lessons
  learned (8.3.2.6).

## Where this project's quality facts live

| Fact | Where |
| --- | --- |
| Product quality objectives | Acceptance criteria A01 to A12, charter section 1.3; copy them as written |
| Exception behaviour the tests must cover | Charter section 1.1.5 |
| Severity levels and response targets | Charter Part 2A, Project boundaries, Warranty terms table (Critical, High, Medium or Low) |
| Who accepts what, and the failed-UAT path | Charter Part 2A, Project approval requirements |
| Quality success criterion | Charter objectives table, Quality row: "Acceptance criteria A01 to A12 of section 1.3 met" |
| Reviews and tests as work | Scope package WBS: 1.2.2.2, 1.3.2 (design review 1.3.2.1, test plan and strategy 1.3.2.2), 1.4.3, 1.5.5, 1.6.1, 1.6.2, 1.8.3.2; each dictionary sheet's Quality Requirements and Acceptance Criteria rows |
| Gate reviews | 1.1.1.3 runs the milestone gate reviews at M1 to M7 |
| Verification per requirement | RTM in Part 1 of the scope package, Verification column |

Facts that are easy to get wrong:

- The dictionary has the **QA engineer author the test cases and execute unit
  and integration testing** (1.4.3.2, 1.5.5.2) and own the code review
  packages (1.4.3.1, 1.5.5.1), where developers cross-review code they did
  not write. Do not write that developers write the unit tests; no document
  says so.
- Iteration gates: M3 is "iteration 1 demo accepted, F01 to F05" (1.4.3.3) and
  M4 is "iteration 2 accepted, feature complete, F06 to F12" (1.5.5.3); each
  releases a payment tranche against a signed acceptance record. Neither
  package states a defect-count rule; the Critical and High rule is in the
  charter's UAT criteria and in 1.6.2.2 and 1.8.3.2.
- **UAT entry** is decided by the Project Manager (1.6.2.2: "decide whether UAT
  starts"; the charter's approval table: "QA engineer prepares; Project
  Manager approves UAT entry"). The two now agree; a sponsor role in UAT
  entry appears nowhere.
- The restore drill (1.8.1.2) is "witnessed by the administrator"; the
  charter's stakeholder is the "Center IT administrator". Write the charter's
  name.
- No work package funds an independent quality audit. Proposing one is a
  decision for the sponsor: highlight it and say it is unfunded.
- A pending scope change request does not change the plan. Build from the
  baselined charter and name, in the reading paragraph, which rows would
  change if it is approved.

## Decisions in this area

Each entry gives the decision a project manager makes in chapter 8, when it
arises, the techniques the book names with each option's stated trade-off, the
inputs and where this project keeps them, the form and field that record it,
any formula, and the common wrong move with the book's reason.

Citation form: "PMBOK 6 8.1.2.3, printed 282 (PDF 321)" for the Guide and
"BoF 3.6, printed 182 (PDF 193)" for the Book of Forms. Chapter 8 gives very
few numbers: no sample-size rule, no control-limit formula, no threshold for
when to audit. Where an entry says "not stated in the book", the team has to
decide and write the choice down as a decision, not present it as the book's.

**Recording, applies to every entry.**

- Form 3.2 Decision Log (BoF 3.2, printed 168 to 169, PDF 179 to 180) prints ID,
  Category, Decision, Responsible Party, Date, Comments. Use Category "quality";
  Comments carries the alternatives considered, the reason and the impact (BoF
  3.2 Table 3.2, printed 168, PDF 179). Table 3.2 names the fifth element
  Priority but describes it as the date the decision was made; the blank form
  prints Date, and the blank form wins. The log is not listed explicitly in the
  PMBOK Guide (BoF 3.2, printed 168, PDF 179).
- Form 3.3 Change Request (BoF 3.3, printed 170 to 174, PDF 181 to 185) is
  needed whenever a decision changes a baseline, the quality management plan or
  a process. Tick Category "Quality" plus every other category it touches
  (Scope, Cost, Schedule, Requirements, Documents); fill "Impacts of Change"
  for Quality and for each baseline moved, each with Increase, Decrease or
  Modify and a Description; the sponsor's answer goes in Disposition (Approve,
  Defer, Reject) with its Justification on the last page (BoF 3.3, printed 174,
  PDF 185). The book routes a quality change request through Perform Integrated
  Change Control (PMBOK 6 8.2.3.3, printed 296 (PDF 335); 8.3.3.4, printed 306
  (PDF 345)); the form goes to the change control board (BoF 3.3, printed 170,
  PDF 181). In this project the sponsor decides what the project manager's
  authority does not cover: user-visible scope, schedule or cost, forecast
  overrun beyond the charter's percent, reserve use beyond the charter's reserve limit (charter Part 2A,
  Assigned project manager, responsibility, and authority level).

### 1. Which quality standards apply

- **Arises:** 8.1 Plan Quality Management, at the start of planning, before
  the objectives are written. Trigger: the first draft of 2.23.
- **Techniques and trade-offs:** expert judgment in quality assurance, quality
  control, measurements, improvements and systems (PMBOK 6 8.1.2.1, printed 281
  (PDF 320)); benchmarking against comparable projects, inside or outside the
  organization, to find best practices and a basis for measuring performance
  (8.1.2.2, printed 281 (PDF 320)); interviews with experienced participants,
  held in trust and confidentiality (8.1.2.2, printed 282 (PDF 321)). The book
  states no trade-off between these three. It does state that proposed
  deliverable changes made to meet identified standards "may require cost or
  schedule adjustments and a detailed risk analysis" (8.1, printed 278 (PDF
  317)), and that the acceptance criteria "may significantly increase or
  decrease quality costs and, therefore, project costs" (8.1.1.2, printed 279
  (PDF 318)). Mandatory versus optional is the tailoring question: which
  industry standards must apply, and which government, legal or regulatory
  constraints exist (PMBOK 6 Tailoring Considerations, printed 276 (PDF 315)).
  Form 2.23 tips: where standards must be adhered to, cite the regulation or
  integrate it into organizational policy (BoF 2.23, printed 95, PDF 106).
- **Inputs:** government regulations and application-area rules, standards and
  guidelines (8.1.1.4, printed 280 (PDF 319)); the organizational quality
  management system, templates and lessons-learned repository (8.1.1.5,
  printed 281 (PDF 320)); assumption log for quality assumptions and
  constraints (8.1.1.3, printed 280 (PDF 319)); scope baseline acceptance
  criteria. Here: A04 names the Law on Personal Data Protection (marked as an
  assumption) and A09 names browser and OS versions, both in charter section
  1.3; A10 names "coding convention". No ISO, IEEE or other named standard
  appears in the charter or the scope package, so the Quality Standards box is
  a list of those facts and nothing more unless the sponsor supplies one.
- **Recorded in:** 2.23 box Quality Standards (BoF 2.23 Table 2.21, printed 96
  (PDF 107): "ISO standards, IEEE, or some other regulatory or industry body").
  Log the choice in 3.2. A standard that adds work moves the WBS and cost: 3.3.
- **Formula:** none.
- **Wrong move:** pasting well-known standards into the box. The box lists what
  this project is bound by; the book says the standards are "usually
  industry or product driven" (BoF 2.23 Table 2.21, printed 96 (PDF 107)) and the plan must
  be consistent with the organization's own quality policies (BoF 2.23, printed
  95, PDF 106). A named standard no one will check is a promise the audit in
  decision 8 will find broken.

### 2. Which quality objectives and metrics to set, and at what threshold

- **Arises:** 8.1, when requirements are stable enough to measure; 2.24 is
  "generally determined as the requirements are developed" (BoF 2.24, printed
  99, PDF 110).
- **Techniques and trade-offs:** multicriteria decision analysis (a
  prioritization matrix): criteria are prioritized and weighted, each
  alternative gets a score, and alternatives are ranked; in this process it
  prioritizes quality metrics (8.1.2.4, printed 283 (PDF 322)); matrix diagrams
  show relationship strength to find the key metrics (8.1.2.5, printed 284 (PDF
  323)); cost-benefit analysis compares the cost of each quality step with its
  expected benefit (8.1.2.3, printed 282 (PDF 321)). The book gives no weights
  and no cut-off score, so the criteria and weights are the team's to state.
  Quality and grade are separate: a low-grade product with few features can be
  fine if it is high quality; a high-grade product with many defects is not
  (Key concepts, printed 274 (PDF 313)). Choosing the level of each is a
  trade-off the project manager and team manage (same page). Adding a metric
  adds Control Quality effort; tolerating a looser one raises failure cost
  (decision 3).
- **Inputs:** charter objectives and approval requirements, requirements
  documentation, RTM, stakeholder register, risk register, scope baseline
  (8.1.1, printed 279 to 280 (PDF 318 to 319)). Here: acceptance criteria A01
  to A12 in charter section 1.3 (already thresholds), the Quality row of the
  charter objectives table, the RTM Verification column in the scope package,
  and the severity table in the warranty terms.
- **Recorded in:** 2.23 Quality Objectives (Metric or Specification, Measure);
  2.24 Quality Metrics (ID, Item, Metric, Measurement Method; ID may be the WBS
  or activity ID, BoF 2.24 Table 2.22, printed 99 (PDF 110)). A metric is "a
  project or product attribute and how the Control Quality process will verify
  compliance to it" (8.1.3.2, printed 287 (PDF 326)), so an empty Measurement
  Method means it is not yet a metric.
- **Formula:** none for the objectives. The book's own metric examples include
  "cost performance measured by CPI" (8.1.3.2, printed 287 (PDF 326)); the
  formula is in chapter 7, not here: CPI = EV / AC, where EV is earned value and
  AC is actual cost, both in currency, CPI is a ratio with no unit, and above
  1.0 means under planned cost (PMBOK 6 7.4.2.2 table, printed 267 (PDF 306)).
- **Wrong move:** listing an objective with no measurement method, or setting
  a threshold nobody can verify. Metrics are "consulted in the manage quality
  process" and then measured in Control Quality "to determine if the result is
  acceptable or if corrective action or rework is required" (BoF 2.24, printed
  99, PDF 110); an objective that cannot be measured cannot trigger either.
  Also wrong: using the metric to hide a grade gap, such as passing a low-grade
  build as high quality (Key concepts, printed 274 (PDF 313)).

### 3. How much to invest in prevention and appraisal against failure cost

- **Arises:** 8.1 Plan Quality Management, when the quality activities are sized
  and priced; again when a failure cost appears (a defect found in UAT or in
  warranty).
- **Techniques and trade-offs:** cost of quality (COQ), with four groups:
  prevention and appraisal costs (conformance, spent during the project to
  avoid failures) against internal failure costs (found by the project team,
  for example rework and scrap) and external failure costs (found by the
  customer, for example liabilities, warranty work, lost business)
  (8.1.2.3, printed 282 (PDF 321); Figure 8-5, printed 283 (PDF 322)). Trade-off
  as stated: "The optimal COQ is one that reflects the appropriate balance for
  investing in the cost of prevention and appraisal to avoid failure costs";
  beyond the optimum, "additional prevention/appraisal costs" are "neither
  beneficial nor cost effective" (same pages). Cost-benefit analysis: each
  quality activity's cost against its expected benefit (less rework, higher
  productivity, lower costs, stakeholder satisfaction, profitability)
  (8.1.2.3, printed 282 (PDF 321)). Flowcharts with branching probabilities can
  estimate "the expected monetary value for the conformance and nonconformance
  work" (8.1.2.5, printed 284 (PDF 323)). The five levels of quality
  management run from letting the customer find defects (most expensive:
  warranty issues, recalls, reputation, rework), through detecting and
  correcting before delivery (appraisal and internal failure costs), through
  using assurance to correct the process, to designing quality in and building
  a quality culture (Key concepts, printed 275 (PDF 314)). Prevention is
  preferred over inspection because "the cost of preventing mistakes is
  generally much less than the cost of correcting mistakes" found by
  inspection or in use (Key concepts, printed 274 (PDF 313)). The COQ over a
  product's life is often decided by program or portfolio management, the PMO
  or operations, because the project is temporary (same page).
- **Inputs:** the scope baseline and its acceptance criteria (8.1.1.2, printed
  279 (PDF 318)); risk register (8.1.1.3, printed 280 (PDF 319)); historical
  databases and lessons learned (8.1.1.5, printed 281 (PDF 320)). Here:
  prevention and appraisal are the design, review and test work packages
  (1.2.2.2, 1.3.2, 1.4.3, 1.5.5, 1.6.1, 1.6.2) and the QA1 hours inside them;
  the external-failure side is the warranty period and the budget line that funds it (charter
  Part 2A, read the amount there), and Figure 8-5 lists warranty work as an external failure
  cost; the funded buffer for the listed risks is the contingency
  reserve budget line. No document states a defect-cost or failure-rate
  estimate, so the optimum cannot be computed; say "not stated" rather than
  inventing one.
- **Recorded in:** 2.23 Quality Management Approach and Quality Control
  Approach; cost lines in the cost estimates, which 2.23 provides information to
  (BoF 2.23, printed 95, PDF 106). If it adds or removes quality work after
  baselining, that is a change to the scope, schedule or cost baseline (8.2.3.4,
  printed 297 (PDF 336)): 3.3 with Quality, Cost and Schedule impacts, plus
  3.2.
- **Formula:** none stated in chapter 8. COQ is described as groups of cost and
  an optimum, not as an equation, and the expected monetary value is named but
  not defined here.
- **Wrong move:** cutting prevention or appraisal to save budget or days.
  The book's two examples: meeting the schedule "by rushing planned quality
  inspections may result in undetected errors, decreased profits, and increased
  post-implementation risks", and meeting requirements by overworking the team
  raises attrition, errors and rework (Key concepts, printed 273 (PDF 312)).
  The route when budget, date and quality cannot all hold is a change request
  (3.3) to the sponsor, not a silent cut.

### 4. Which deliverables and processes go under quality review

- **Arises:** 8.1, when 2.23 is drafted, and each time the scope baseline changes.
- **Techniques and trade-offs:** test and inspection planning decides how to
  test or inspect each deliverable and how to meet the performance and
  reliability goal; tests are industry dependent, with alpha and beta tests
  named for software (8.1.2.6, printed 285 (PDF 324)). The type, amount and
  extent of tests per requirement depend on "the nature of the project, time,
  budget, and other constraints" (8.3.2.4, printed 303 (PDF 342)), so the
  trade-off is coverage against those constraints; the book gives no coverage
  threshold. "Percentage of requirements covered by the test plan" is the
  book's example of a coverage metric (8.1.3.2, printed 287 (PDF 326)). Checklists
  used later must "incorporate the acceptance criteria included in the scope
  baseline" (8.2.2.1, printed 292 (PDF 331)). A tailoring question: do quality,
  requirements and scope stay one aspect (small project) or separate roles
  (BoF 2.23, printed 95, PDF 106).
- **Inputs:** scope baseline (WBS and acceptance criteria), RTM ("links product
  requirements to deliverables and helps to ensure each requirement is tested"
  (8.1.1.3, printed 280 (PDF 319))), risk register. Here: D1 to D11 in charter
  section 1.2, the RTM Verification column, the dictionary Quality Requirements
  and Acceptance Criteria rows, and the exception catalogue in charter 1.1.5.
- **Recorded in:** 2.23 Deliverables and Processes Subject to Quality Review
  (Deliverables, Processes); the processes column holds the processes "that
  require verification or validation" (BoF 2.23 Table 2.21, printed 96 (PDF
  107)). Quality requirements the planning adds go into the RTM (8.1.3.4,
  printed 287 (PDF 326)). A WBS dictionary addition is a baseline change:
  3.3 (8.1.3.3, printed 287 (PDF 326)).
- **Formula:** none.
- **Wrong move:** listing a deliverable that has no metric, or choosing the
  list without the risk register. Table 2.21 describes the box as the key
  deliverables "that have metrics or measures associated with quality
  objectives" (BoF 2.23, printed 96, PDF 107), and the register holds the
  "threats and opportunities that may impact quality requirements"; risks
  found while planning go back into it (8.1.1.3, printed 280 (PDF 319); 8.1.3.4,
  printed 287 (PDF 326)).

### 5. When in the life cycle to test and inspect

- **Arises:** 8.1 (the plan) and 8.3 (each cycle); in this project at each
  iteration end and again before UAT entry.
- **Techniques and trade-offs:** test as components become available and at
  the end ("Early testing helps identify nonconformance problems and helps
  reduce the cost of fixing the nonconforming components") (8.3.2.4, printed
  303 (PDF 342)); in waterfall projects control happens at specific times near
  the end of a phase or project, in agile it is done by all team members
  throughout (8.3, printed 300 (PDF 339)); agile practice builds frequent
  quality and review steps in and works in small batches, which "aim to uncover
  inconsistencies and quality issues earlier in the project life cycle when the
  overall costs of change are lower" (Agile considerations, printed 276 (PDF
  315)). The book states the benefit of early testing and no cost for it; the
  cost of repeating tests is not stated in the book.
- **Inputs:** schedule and iteration plan; quality metrics; test and evaluation
  documents from Manage Quality (8.2.3.2, printed 296 (PDF 335)). Here: the
  charter's milestone table M1 to M7 and the iteration demo packages 1.4.3.3
  and 1.5.5.3, with the test packages inside each iteration.
- **Recorded in:** 2.23 Quality Control Approach (timing) and Quality
  Management Approach (timing and content of audits, BoF 2.23 Table 2.21,
  printed 96 (PDF 107)). Moving a test into an earlier or later window moves
  schedule: 3.3 with Schedule impact.
- **Formula:** none.
- **Wrong move:** leaving all testing to one block before acceptance. The book
  says early testing reduces the cost of fixing (8.3.2.4, printed 303 (PDF
  342)), and a schedule squeeze that removes planned inspections risks
  undetected errors (Key concepts, printed 273 (PDF 312)).

### 6. Sampling or full inspection

- **Arises:** 8.1, when the control approach is written ("Sample frequency and
  sizes should be determined during the Plan Quality Management process",
  8.3.2.1, printed 303 (PDF 342)); in 8.3 when results suggest the plan was
  wrong. Also in quality reports, where "100% inspection" is listed among
  recommended corrective actions (8.2.3.1, printed 296 (PDF 335)).
- **Techniques and trade-offs:** statistical sampling "involves choosing part
  of a population of interest for inspection (for example, selecting 10
  engineering drawings at random from a list of 75)" to measure controls and
  verify quality (8.3.2.1, printed 303 (PDF 342)); full inspection of the whole
  population, named only as "100% inspection" (8.2.3.1, printed 296 (PDF 335)).
  Attribute sampling (conforms or does not) is distinct from variable sampling
  (rated on a continuous scale of conformity) (Key concepts, printed 274 (PDF
  313)). The book states no trade-off between sampling and full inspection, no
  sample-size rule, no confidence level and no acceptance number: not stated in
  the book. Do not borrow them without naming the outside source. Inspection
  itself is "the examination of a work product to determine if it conforms to
  documented standards" and may be called review, peer review, audit or
  walkthrough (8.3.2.3, printed 303 (PDF 342)); check sheets (tally sheets)
  collect attribute data on defects (8.3.2.1, printed 302 (PDF 341)).
- **Inputs:** metrics, the population size, tolerance for error, the risk
  register. Here: the UAT test set agreed at M5 (1.6.2.1) is the population for
  A01, and A01 measures a pass rate over it (at least 99% of cases), so it is a
  full run of an agreed set, not a sample; the audit-log check in FR11 of the
  scope package RTM ("System Administrator samples the log against a scripted
  set of changes") is a sample. A01 also allows no open defect of any severity
  in the tuition, payment and teaching-hour path; the book states no rule that
  links how critical a path is to how deep the inspection goes: not stated in
  the book.
- **Recorded in:** 2.24 Measurement Method (the "method of measuring, including
  any equipment or procedures", BoF 2.24 Table 2.22, printed 99 (PDF 110))
  states the sample or the full run; 2.23 Quality Control Approach states the
  frequency. Changing from sample to full inspection after baselining changes
  effort: 3.2, and 3.3 if cost or schedule moves.
- **Formula:** none stated.
- **Wrong move:** fixing the sample size or frequency at inspection time, or
  after seeing results. The book puts both decisions in planning (8.3.2.1,
  printed 303 (PDF 342)).

### 7. Control limits or specification limits: when to take corrective action

- **Arises:** 8.3 Control Quality, when a repetitive process produces
  measurable output and a chart is kept; the decision is where the action
  points are set, in 8.1.
- **Techniques and trade-offs:** control charts determine "whether or not a
  process is stable or has predictable performance". Upper and lower
  specification limits "are based on the requirements" and are the maximum and
  minimum allowed. Upper and lower control limits are different: they come from
  "standard statistical calculations" and establish the process's natural
  capability. The project manager and stakeholders may use the calculated
  limits "to identify the points at which corrective action will be taken to
  prevent performance that remains outside the control limits" (8.3.2.5,
  printed 304 (PDF 343)). Tolerances are the specified range of acceptable
  results; control limits bound the common variation of a statistically stable
  process (Key concepts, printed 274 (PDF 313)). Charts are used most for
  repetitive manufacturing, and may also monitor cost and schedule variances,
  volume and frequency of scope changes (8.3.2.5, printed 304 (PDF 343)). Other
  analysis in the same step: performance reviews compare planned metrics with
  actuals (8.3.2.2, printed 303 (PDF 342)); histograms show defects by source
  or component; scatter diagrams plot planned against actual (8.3.2.5, printed
  304 (PDF 343)). The book states no run rule, no limit width and no number of
  points before action: not stated in the book.
- **Inputs:** quality metrics, work performance data (8.3.1.5, printed 301 (PDF
  340)), the specification from the requirement. Here: A02 response times and
  A06 availability are thresholds taken from requirements, that is
  specification limits. The book says control charts are used most often for
  repetitive activities and "may" monitor management results, so whether to
  keep one here is the team's call.
- **Recorded in:** 2.24 Metric and Measurement Method (state which limits are
  specification limits and which are control limits); results in the quality
  control measurements, in the format the quality management plan gives
  (8.3.3.1, printed 305 (PDF 344)).
- **Formula:** control limits are computed by "standard statistical
  calculations" that chapter 8 does not write out. Not stated in the book.
- **Wrong move:** treating the specification limit as the control limit.
  The book says they are different (8.3.2.5, printed 304 (PDF 343)): the first
  comes from the requirements, the second from the process's own natural
  capability, so staying inside one says nothing about the other.

### 8. Who audits, how independent, and how often

- **Arises:** 8.1, when the audit timing and content go in 2.23; 8.2 when an
  audit is run; triggers named in the book: scheduled or random (8.2.2.5,
  printed 295 (PDF 334)).
- **Techniques and trade-offs:** a quality audit is "a structured, independent
  process" to determine whether activities comply with organizational and
  project policies, processes and procedures; it "is usually conducted by a team
  external to the project, such as the organization's internal audit
  department, PMO, or by an auditor external to the organization" (8.2.2.5,
  printed 294 (PDF 333)). It may be scheduled or random, and internal or
  external (printed 295 (PDF 334)). Its stated aims: find good and best
  practices, nonconformity, gaps and shortcomings; share practices; help
  improve processes; record contributions in lessons learned. The stated benefit
  is that correcting the deficiencies "should result in a reduced cost of
  quality and an increase in sponsor or customer acceptance" (printed 295 (PDF
  334)). Audits can also confirm that approved changes, corrective actions,
  defect repairs and preventive actions were implemented (printed 295 (PDF
  334)). Form 3.6 tailoring: audits may carry lessons for other projects or
  track implementation of approved changes and corrective or preventive actions
  (BoF 3.6, printed 181, PDF 192). The book states no frequency, and no
  trade-off in cost between scheduled and random: not stated in the book.
  Manage Quality may use the organization's quality assurance department for
  failure analysis, design of experiments and improvement (8.2, printed 290
  (PDF 329)); the book offers it as a resource and says nothing about whether
  it is independent of a given project.
- **Inputs:** quality management plan, results from previous audits, lessons
  learned repository (8.2.1.3, printed 291 (PDF 330)). Here: no work package
  funds an independent audit; the QA engineer is a project member, so a review
  by QA1 is a Control Quality inspection, not an independent audit.
- **Recorded in:** 2.23 Quality Management Approach ("timing and content of
  project and product quality audits", BoF 2.23 Table 2.21, printed 96 (PDF
  107)) and Applicable Quality Procedures (quality audits); each audit on 3.6:
  Project Auditor, Audit Date, Area Audited (seven boxes), Good Practices from
  Similar Projects, Areas for Improvement, Deficiencies or Defects (ID, Defect,
  Action, Responsible Party, Due Date), Comments (BoF 3.6, printed 183, PDF 194;
  Table 3.6, printed 182, PDF 193). An unfunded audit is new work: 3.3 with Cost
  and Schedule impact, the sponsor decides.
- **Formula:** none.
- **Wrong move:** calling a peer review or the QA engineer's own check an
  audit. The book defines an audit as independent and usually external to the
  project (8.2.2.5, printed 294 (PDF 333)); work by the project's own QA staff
  is Control Quality inspection (8.3.2.3, printed 303 (PDF 342)).

### 9. What to do with a nonconforming deliverable

- **Arises:** 8.3 when inspection or testing fails a metric; 8.2 when an audit
  finds a deficiency.
- **Techniques and trade-offs:** the quality management plan holds "what to do
  with nonconforming products and what corrective action to implement"
  (8.2.1.1, printed 290 (PDF 329)); the quality report recommends corrective
  actions "including rework, defect/bugs repair, 100% inspection, and more"
  (8.2.3.1, printed 296 (PDF 335)). To choose between options, alternatives
  analysis evaluates identified options to pick the most appropriate quality
  approach (8.2.2.2, printed 292 (PDF 331)), and multicriteria decision analysis
  can weigh the product's "life cycle cost, schedule, stakeholder satisfaction,
  and risks associated with resolving product defects" (8.2.2.3, printed 293
  (PDF 332)). Repairs are verified by inspection ("Inspections also are used
  to verify defect repairs", 8.3.2.3, printed 303 (PDF 342)) and, once approved
  as change requests, "retested, and certified as correct" (8.3.1.3, printed
  301 (PDF 340)). Chapter 8 names no accept-as-is option; formal acceptance
  belongs to Validate Scope (decision 12), so a decision to ship with a known
  defect is not a chapter 8 technique. This project's own route for that is in the charter: "If UAT does
  not pass", three options to the sponsor within two working days, a signed list
  of accepted defects with fix dates being one of them.
- **Inputs:** quality control measurements, defect log, severity table, risk
  report (8.2.1.2, printed 291 (PDF 330)). Here: warranty severity table in the
  charter (Critical, High, Medium or Low, with response targets), the defect
  log kept by the test packages and consolidated in 1.6.2.1.
- **Recorded in:** 3.6 Deficiencies or Defects (ID, Defect, Action, Responsible
  Party, Due Date): "action items, a responsible party, and be assigned a due
  date for compliance" (BoF 3.6, printed 181 (PDF 192)); the issue log (8.3.3.6,
  printed 306 (PDF 345): "a deliverable that does not meet the quality
  requirements is documented as an issue"); the choice among options in 3.2.
- **Formula:** none.
- **Wrong move:** logging a defect with no owner or date, or fixing the symptom.
  The book requires an action, owner and date on each (BoF 3.6, printed 181
  (PDF 192)) and says the problem does not recur once all root causes are
  removed (8.2.2.2, printed 292 (PDF 331)).

### 10. Fix inside the baseline, or raise a change request

- **Arises:** 8.2 and 8.3 outputs, whenever a finding, defect or improvement is
  logged.
- **Rule the book gives:** if a change "impact[s] any of the components of the
  project management plan, project documents, or project or product management
  processes", the project manager "should submit a change request and follow
  the Perform Integrated Change Control process" (8.2.3.3, printed 296 (PDF
  335)); Control Quality says the same for changes that may affect plan
  components or project documents (8.3.3.4, printed 306 (PDF 345)). Plan
  components that may need a change request: quality management plan, scope,
  schedule and cost baselines (8.2.3.4, printed 297 (PDF 336)); the plan itself
  may change "due to the actual results" (same page). "Any change to the project
  management plan goes through the organization's change control process via a
  change request" (8.1.3.3, printed 287 (PDF 326)). Approved change requests
  include "defect repairs, revised work methods, and revised schedules" and
  their implementation "should be verified, confirmed for completeness,
  retested, and certified as correct" (8.3.1.3, printed 301 (PDF 340)), with an approved-change-requests review
  meeting to check partial changes (8.3.2.6, printed 305 (PDF 344)).
- **What the book leaves open:** it lists defect repairs among approved change
  requests (8.3.1.3, printed 301 (PDF 340)) and sets the submission trigger at
  impact on a plan component, a project document or a management process
  (above). It does not say whether a repair that touches none of them needs its
  own change request, and gives no numeric trigger: not stated in the book.
  The team therefore states its own rule as a decision in 3.2. A rule that fits
  the book and this charter: a repair inside a baselined package is recorded on
  3.6 and the issue log; a finding that adds work, moves a date, changes a
  metric or an acceptance criterion, or changes the quality plan goes on 3.3.
  The money and authority limits are the charter's (recording note above).
- **Techniques and trade-offs:** alternatives analysis and multicriteria
  decision analysis (decision 9) set out the options for the change request's
  Impacts of Change. The impact fields exist so the cost and schedule of the
  fix are visible before the board decides (BoF 3.3 Table 3.3, printed 171 (PDF
  182): schedule impact "and whether it will change the critical path").
- **Inputs and records:** audit and test findings; 3.6, 3.3, change log and
  3.2; tailoring tip: a "mandatory or discretionary" box and an "implications of
  not making the change" field may be added (BoF 3.3, printed 170 (PDF 181)).
- **Formula:** none.
- **Wrong move:** treating a baseline change as a quiet quality fix. A new audit,
  a longer test window or an extra review package changes the schedule or cost
  baseline (8.2.3.4, printed 297 (PDF 336)); doing it without a change request
  skips the change control process that, by the chapter, every plan change
  follows (8.1.3.3, printed 287 (PDF 326)).

### 11. Which cause to attack, and with which technique

- **Arises:** 8.2 after an audit finding or a Control Quality failure; in
  retrospectives (8.3.2.6, printed 305 (PDF 344)).
- **Techniques and trade-offs:** root cause analysis finds "the basic
  underlying reason that causes a variance, defect, or risk"; one root cause can
  underlie several, and removing all root causes stops recurrence (8.2.2.2,
  printed 292 (PDF 331)). Representations: cause-and-effect (fishbone, why-why,
  Ishikawa) diagrams to find the main cause; affinity diagrams to group
  potential causes; flowcharts to show the steps leading to a defect;
  histograms to rank causes or count defects per deliverable; matrix diagrams;
  scatter diagrams (8.2.2.4, printed 293 (PDF 332)). Process analysis finds
  non-value-added steps (8.2.2.2, printed 292 (PDF 331)). Structured problem
  solving has six elements: define the problem, identify the root cause,
  generate solutions, choose the best, implement, verify effectiveness
  (8.2.2.7, printed 295 (PDF 334)). Improvement tools: plan-do-check-act and Six
  Sigma, "two of the most common" (8.2.2.8, printed 296 (PDF 335)). The book gives
  no rule for which to choose.
- **Inputs:** quality control measurements, defect log, audit findings,
  lessons learned. Here: the defect log (1.6.2.1) and retrospectives.
- **Recorded in:** 3.6 Areas for Improvement ("the specific improvements or
  measurements that need to be achieved", BoF 3.6 Table 3.6, printed 182 (PDF
  193)); the lessons learned register (8.2.3.5, printed 297 (PDF 336)); the
  chosen fix in 3.2.
- **Formula:** none.
- **Wrong move:** repairing each defect without a cause. The book says the
  problem does not recur once all root causes are removed (8.2.2.2, printed 292
  (PDF 331)).

### 12. Whether a deliverable is verified and released to Validate Scope

- **Arises:** 8.3 at the end of each deliverable's tests; in this project at
  the iteration demos (M3, M4), UAT entry (1.6.2.2) and UAT (1.8.3.2).
- **Techniques and trade-offs:** inspection of deliverables against the
  acceptance criteria in the scope statement (8.3.1.4, printed 301 (PDF 340));
  performance reviews compare metrics with actuals (8.3.2.2, printed 303 (PDF
  342)). Output: verified deliverables, which "become an input to the Validate
  Scope process (Section 5.5) for formalized acceptance"; changed deliverables
  are "inspected, and reverified" (8.3.3.2, printed 305 (PDF 344)). Control
  Quality demonstrates "with reliable data, that the sponsor's and/or
  customer's acceptance criteria have been met" (printed 299 (PDF 338)). The
  book states no pass threshold of its own; the threshold is the project's
  acceptance criteria, here A01 (at least 99% of UAT cases passed, no open
  Critical or High defect).
- **Recorded in:** quality control measurements in the plan's format (8.3.3.1,
  printed 305 (PDF 344)); work performance information, which lists requirements
  fulfillment, causes of rejection, rework, status of metrics (8.3.3.3, printed
  305 (PDF 344)); 2.24 Metric; decision in 3.2.
- **Formula:** none.
- **Wrong move:** sending unverified work to acceptance to protect a date.
  The purpose of Control Quality is to verify that deliverables meet the
  requirements before final acceptance (8.3, printed 298 (PDF 337)); an
  acceptance window used to find defects moves the failure into the customer's
  own time (this project's 1.6.2.2 states the same reason for a UAT entry gate).

### 13. Whether to change the quality plan or the metrics mid-project

- **Arises:** 8.2 or 8.3 when results show the agreed approach does not work;
  when requirements change.
- **Techniques and trade-offs:** 2.23 "is developed once and is not usually
  changed" (BoF 2.23, printed 95, PDF 106); 2.24 is developed once if
  requirements are stable and evolves if they change (BoF 2.24, printed 99, PDF
  110). The Guide allows the approach to be modified "due to the actual
  results", through a change request (8.2.3.4, printed 297 (PDF 336); 8.3.3.5,
  printed 306 (PDF 345)). The plan should also be reviewed early so decisions
  rest on accurate information, with benefits named as a sharper focus on the
  value proposition, lower costs and fewer schedule overruns from rework
  (8.1.3.1, printed 286 (PDF 325)). Tailoring: on small projects metrics,
  requirements and specifications are considered the same thing (BoF 2.24,
  printed 99, PDF 110), which is the case for keeping A01 to A12 and 2.24
  aligned instead of duplicating them.
- **Inputs:** quality control measurements, audit results, lessons learned,
  the change log.
- **Recorded in:** 3.3 for a plan or baseline change; 3.2 for the decision;
  the new version of 2.23 or 2.24 carries a changed row only if the board
  approved it.
- **Formula:** none.
- **Wrong move:** editing the plan or a threshold to make a failing result
  pass. Plan changes go through change control (8.1.3.3, printed 287 (PDF
  326)); the threshold is the project's acceptance criterion, whose change is a
  scope-baseline decision for the sponsor.

### Formulas in this area

Chapter 8 gives no equation of its own. The only formula the entries use is
the chapter 7 definition below, which chapter 8 names as a metric example.

| Formula | Variables | Source |
| --- | --- | --- |
| CPI = EV / AC | EV earned value, AC actual cost, both in currency; CPI a unitless ratio; above 1.0 is under planned cost | PMBOK 6 7.4.2.2 table, printed 267 (PDF 306); named as a metric in 8.1.3.2, printed 287 (PDF 326) |

Named in chapter 8 but not given with a formula: cost of quality (8.1.2.3),
expected monetary value (8.1.2.5), statistical sampling size (8.3.2.1), control
limits (8.3.2.5). Say "not stated in the book" for each when a form asks for it.
