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
  (5.5). In this project that hand-off is UAT, 1.8.3.1 in the scope package.
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
| Reviews and tests as work | Scope package WBS: 1.2.2.2, 1.3.2 (test plan 1.3.2.1), 1.4.3, 1.5.5, 1.6.1, 1.6.2; each dictionary sheet's Quality Requirements and Acceptance Criteria rows |
| Gate reviews | 1.1.1.2 runs the milestone gate reviews at M1 to M7 |
| Verification per requirement | RTM in Part 1 of the scope package, Verification column |

Facts that are easy to get wrong:

- The dictionary has the **QA engineer execute unit and integration
  testing** (1.4.3.1, 1.4.3.2, 1.5.5.1, 1.5.5.2), not the developers. Do not
  write that developers write the unit tests; no document says so.
- Iteration gates differ: M3 requires no open Critical or High defect in F01
  to F03 (1.4.3.1); M4 requires "feature-complete criteria" (1.5.5.1,
  1.5.5.2).
- **UAT entry** is approved by the Project Manager in the charter's approval
  table ("QA engineer prepares; Project Manager approves UAT entry"), while
  1.6.2.2 says "Sponsor and QA engineer agree UAT entry". Follow the charter
  in a plan and report the difference.
- The restore drill is signed by the "System Administrator" in 1.8.1.2; the
  charter's stakeholder is the "Center IT administrator". Same person by
  assumption 2 (1 IT administrator); write the charter's name.
- No work package funds an independent quality audit. Proposing one is a
  decision for the sponsor: highlight it and say it is unfunded.
- A pending scope change request does not change the plan. Build from the
  baselined charter and name, in the reading paragraph, which rows would
  change if it is approved.
