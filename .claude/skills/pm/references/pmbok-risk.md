# PMBOK 6 chapter 11, Project Risk Management, for the risk forms

Read this before filling 2.31 Risk Management Plan, 2.32 Risk Register, 2.33 Risk Report, 2.34 Probability and
Impact Assessment, 2.35 Probability and Impact Matrix, 2.36 Risk Data Sheet or 4.5 Risk Audit. The forms print the
boxes; chapter 11 says what each process outputs and which technique makes it. The last section lists the decisions
a project manager makes in this area, with the PMBOK technique names a proposed remedy has to carry.

## Where it is

`PMBOK6_and_Agile_Practice_Guide.pdf` at the repo root. Guide part: PDF page = printed page + 39. Short form used
from here on, so every claim keeps both numbers: **p405/444** is PMBOK 6 printed page 405, PDF page 444;
**BoF 2.32 p128/139** is Book of Forms printed page 128, PDF page 139 (PDF = printed + 11). Contents pages: PDF
pages 14 to 15. Chapter 11 is wholly in the Guide part.

| Section | Printed / PDF page |
| --- | --- |
| 11 Overview, key concepts, trends (non-event risk, resilience), tailoring, agile | 395 to 400 / 434 to 439 |
| 11.1 Plan Risk Management (11.1.3.1 plan elements p405 to 408/444 to 447; Table 11-1 p407/446; Figure 11-5 p408/447) | 401 to 408 / 440 to 447 |
| 11.2 Identify Risks (techniques p414 to 416/453 to 455; 11.2.3.1 register p417/456; 11.2.3.2 report p418/457) | 409 to 418 / 448 to 457 |
| 11.3 Perform Qualitative Risk Analysis (other parameters p423 to 424/462 to 463; matrix p425/464; outputs p427/466) | 419 to 427 / 458 to 466 |
| 11.4 Perform Quantitative Risk Analysis (when p429/468; data analysis p433 to 436/472 to 475; outputs p436/475) | 428 to 436 / 467 to 475 |
| 11.5 Plan Risk Responses (criteria p439/478; threats: escalate p442/481, avoid, transfer, mitigate and accept p443/482; opportunities p444/483; contingent p445/484; overall p445 to 446/484 to 485; selection p446/485; outputs p447 to 448/486 to 487) | 437 to 448 / 476 to 487 |
| 11.6 Implement Risk Responses | 449 to 452 / 488 to 491 |
| 11.7 Monitor Risks (determinations p454/493; reserve analysis and audits p456/495; reviews p457/496) | 453 to 458 / 492 to 497 |
| Outside the chapter: reserve analysis 7.2.2.6 p245 to 246/284 to 285 and 6.4.2.6 p202/241; management reserve 7.3.2.3 p252/291; cost baseline 7.3.3.1 p254/293; glossary | 702 to 725 / 741 to 764 |

Book of Forms, printed / PDF:

| Form | Prose | Blank form | Form | Prose | Blank form |
| --- | --- | --- | --- | --- | --- |
| 2.31 | 121 to 123 / 132 to 134 | 124 to 127 / 135 to 138 | 2.35 | 142 / 153 | 143 / 154 |
| 2.32 | 128 to 129 / 139 to 140 | 130 / 141 | 2.36 | 144 to 145 / 155 to 156 | 146 / 157 |
| 2.33 | 131 to 132 / 142 to 143 | 133 to 136 / 144 to 147 | 4.5 | 209 to 210 / 220 to 221 | 211 to 212 / 222 to 223 |
| 2.34 | 137 to 139 / 148 to 150 | 140 to 141 / 151 to 152 | 3.1, 3.2, 3.3 | 165 to 166, 168, 170 to 171 / 176 to 177, 179, 181 to 182 | 167, 169, 172 to 174 / 178, 180, 183 to 185 |

`pdftotext -layout` interleaves a vertical watermark of 1 to 3 letter lines and a "PMI Member benefit" footer;
drop them before reading. Several figures (11-1 overview, 11-5 matrix, 11-13 S-curve) flatten badly; open the PDF
page with the Read tool when the numbers matter.

## Chapter 11 terms, with the book's meaning

- **Individual project risk, overall project risk** (p397/436): an uncertain event or condition with a positive or
  negative effect on one or more objectives, against the effect of uncertainty on the project as a whole from all
  sources. Both levels are managed. **Threat, opportunity** (p397/436): negative and positive individual risks.
- **Risk appetite** (glossary p720/759): the uncertainty an organization or individual will accept for a reward.
  **Risk threshold** (glossary p721/760): the exposure above which risks are addressed and below which they may be
  accepted. Thresholds are measurable, per objective, and show up in the impact definitions (p398/437, p407/446).
- **Risk exposure** (glossary p721/760): aggregate potential impact of all risks at a point in time.
- **Non-event risk** (p398 to 399/437 to 438): variability risk (Monte Carlo, then reduce spread) and ambiguity risk
  (fill the knowledge gap, prototype). **Emergent risk, resilience** (p399/438): contingency for emergent risks in
  addition to a specific risk budget for known ones, flexible processes, strong change management.
- **Risk register, risk report** (glossary p721/760): the repository of risk process outputs, and the progressively
  built summary of individual risks plus the level of overall risk. Both grow through all processes (p417/456, p418/457).
- **Risk owner** (glossary p721/760): monitors the risk and selects and implements the response. Nominated in
  11.2, confirmed in 11.3 (p411/450). **RBS, risk category** (p405 to 406/444 to 445): a hierarchy of sources of risk.
- **Probability and impact matrix** (p425/464): the grid that divides risks into priority groups, one matrix per
  objective or one overall priority. **Watch list** (p423/462): low probability and impact risks kept for monitoring.
- **Other parameters** (p423 to 424/462 to 463): urgency (time to respond), proximity (time before impact),
  dormancy (time before impact is discovered), manageability, controllability, detectability, connectivity,
  strategic impact, propinquity (how much stakeholders think it matters).
- **Trigger condition** (glossary p725/764): an event or situation that indicates a risk is about to occur.
  **Contingent response, contingency plan, fallback plan** (p445/484): a response run only under predefined conditions.
- **Contingency reserve** (glossary p702/741; p245/284): time or money inside the baseline for known risks with
  active strategies; the known unknowns. **Management reserve** (glossary p710/749; p252/291): held outside the
  performance measurement baseline for unforeseen in-scope work; the unknown unknowns.
- **Secondary risk, residual risk** (glossary p722/761, p719/758): arises from implementing a response; remains
  after responses are implemented. **Risk review, risk audit** (p457/496, glossary p720/759): a meeting on response
  effectiveness; an audit of the effectiveness of the risk management process.

## How each process output maps onto the forms

A component with no box goes in the nearest box and is named in the italic reading paragraph above the form,
never inside it. Placements marked "judgement" are this note's reading, not the book's.

**2.31 from 11.1.3.1** (p405 to 408/444 to 447; BoF Table 2.28 p123/134). The plan "may include some or all".

| PMBOK 11.1.3.1 element | Form 2.31 box |
| --- | --- |
| Risk strategy; Methodology (approaches, tools, data sources) | Strategy; Methodology |
| Roles and responsibilities (lead, support, team per activity) | Roles and Responsibilities (Role, Responsibility rows) |
| Funding, including protocols for applying contingency and management reserves | Risk Management Funding; Contingency Protocols (BoF Table 2.28 has no separate protocols element, the blank form wins) |
| Timing: when and how often, activities into the schedule | Frequency and Timing |
| Risk categories, RBS or a list | Risk Categories |
| Stakeholder risk appetite as measurable thresholds per objective | Stakeholder Risk Tolerances (BoF Table 2.28 says appetite) |
| Definitions of probability and impact levels | Definitions of Probability; Definitions of Impact by Objective (Scope, Quality, Time, Cost) |
| Probability and impact matrix, with prioritization rules | Probability and Impact Matrix (page 4) |
| Tracking: how risk activities are recorded and the process audited | Risk Tracking and Audit |
| Reporting formats for register and report | No box; Methodology or Risk Tracking and Audit, judgement (BoF p121/132 lists "Risk report formats") |
| Tailoring decisions (p400/439) | No box; Methodology |

**2.32 from 11.2.3.1, 11.3.3.1, 11.5.3.3, 11.7.3.4** (p417/456, p427/466, p448/487, p458/497; BoF Table 2.29 p129/140).

| PMBOK content | Form 2.32 box |
| --- | --- |
| Unique identifier; structured statement separating cause and effect | ID; Risk Statement ("EVENT may occur, causing IMPACT", BoF p129/140) |
| Potential then nominated risk owner | Owner |
| Probability and impact on each objective; priority level or risk score | Probability; Impact (Scope, Quality, Schedule, Cost); Score |
| Preliminary then agreed response strategy | Response: the charter's own wording copied as written; a strategy label is the skill's reading, goes in Comments, and is recorded as judgment in 3.2 (`rendering.md`) |
| Specific actions; budget and schedule activities for the response; triggers | Actions; triggers and warning signs in Actions or Comments, judgement |
| Revised assessment after the response | Revised Probability; Impact (printed Impact, not Revised); Revised Score |
| Owner of a response action (p450/489 "owners for agreed-upon risk responses") | Responsible Party, judgement; BoF Table 2.29 has no such element |
| Current status; open or closed (BoF p129/140) | Status |
| Title, category, causes, effects, WBS reference, timing, urgency, watch list | No box; Comments, or the RBS code and WBS code inside Risk Statement, judgement |
| Contingency and fallback plans, residual and secondary risks | No box; form 2.36 |

**2.33 from 11.2.3.2, 11.3.3.1, 11.4.3.1, 11.5.3.3, 11.7.3.4** (p418/457, p427/466, p436/475, p448/487, p458/497;
BoF Table 2.30 p132/143). The report starts with sources of overall risk and a summary of individual risks.

| PMBOK content | Form 2.33 box |
| --- | --- |
| Sources and drivers of overall risk; trend; recommended responses | Overall Risk Status and Trends; Significant Drivers of Overall Risk; Recommended Responses |
| Summary of individual risks: counts, distribution, metrics, trends | Count grid (risks per matrix cell); Metrics (nine printed rows) |
| Most important individual risks; prioritized list; responses and owners | Critical Risks (Top Risks, Responses; five rows); Changes to Critical Risks. The full list stays in 2.32 (BoF p131/142 allows it as an appendix) |
| Chances of success; degree of inherent variability (range of outcomes) | Probability of Meeting Objectives (Scope, Schedule, Cost, Quality, Other); Range of Outcomes |
| S-curves, tornado, criticality, major drivers, trends, recommended responses | Quantitative Analysis Summary; Key Drivers of Variances; Proposed Responses |
| Contingency reserve needed for a confidence level; reserve analysis | Reserve Status (cost table, schedule table); Assessment of Reserve Adequacy |
| Conclusions from risk audits (p458/497) | Risk Audit Summary (events, processes, recommendations) |

If no quantitative analysis is done, BoF p131/142 says omit that content; say so in the reading paragraph.

**2.34, 2.35 from 11.1.3.1 and 11.3.2.6.** BoF p137/148: 2.34 is for a project with no risk management plan, since the
plan holds the same definitions (pages 3 and 4 of 2.31). With a plan, point to it instead of copying, or the two
texts drift. Table 11-1 (p407/446) defines three objectives; the forms print Scope, Quality, Schedule and Cost
(2.34) so Scope has no PMBOK example. Rating rules (BoF Table 2.31 p138 to 139/149 to 150) turn P and I into
High, Medium or Low, which is the zone of 2.35 and is not the numeric Score of 2.32.

**2.36 from 11.5.3.3** (p448/487; BoF Table 2.32 p145/156). One sheet per risk, an extension of the register.

| PMBOK content | Form 2.36 box |
| --- | --- |
| Risk statement, cause, status, assessment, response, revised assessment | Risk ID; Risk Description; Status; Risk Cause; bank 1 and bank 2 |
| Secondary risks; residual risks (including those deliberately accepted) | Secondary Risks; Residual Risk |
| Contingency plans and the triggers that call for them; fallback plans | Contingency Plan; Fallback Plans |
| Contingency reserve of money and time for the risk (p439/478) | Contingency Funds; Contingency Time |

**4.5 from 11.7.2.2 and 11.7.1** (p456/495, p454/493; BoF Table 4.5 p210/221). The chapter gives no audit content,
only that format and objectives are defined beforehand. The nine determinations of Monitor Risks (responses
effective, approach appropriate, policies followed, reserves adequate) are the questions the boxes answer.

| BoF 4.5 box | Source |
| --- | --- |
| Risk Event Audit (Event, Cause, Response, Comment) | Risks that occurred, from 2.32 and the issue log (3.1); Comment asks if it could have been foreseen |
| Risk Response Audit (Event, Response, Successful, Actions to Improve) | Effectiveness of implemented responses (p454/493) |
| Risk Management Process Audit (six printed processes: Followed; Tools and Techniques Used) | Plan, identify, qualitative, quantitative, responses, monitor, checked against 2.31 |
| Good Practices to Share; Areas for Improvement | Lessons learned register updates (p458/497) |

## Where this project's risk facts live

| Fact | Where |
| --- | --- |
| R1 to R12 with Type (Product or Project) and Response | `charter-package.en.md` Part 2A "Overall project risk" table; copy as written |
| Overall rating Medium and its drivers (fixed budget and date, one week of float per phase, PM is also BA, volatile tuition rules, go-live four weeks before the Lunar New Year) | Same section; Part 2B charter form, Overall Project Risk |
| Probability, Impact, Score, Owner, Status, revised values | Nowhere. No document scores a risk or names an owner (R11 names the Accountant as benefit owner only). Leave empty, house-style table |
| Objectives with measurable limits: Time, Cost, Quality, scope | Charter Part 2A "Project objectives and related success criteria"; read the cost, schedule and quality limits and the acceptance criteria there |
| Contingency reserve | The reserve budget line (amount and share of the budget are in the charter table), inside the cost baseline, which risks may draw on it and through what; scope package Part 2 roll-up and 1.1.1.4 Technical Information |
| Management reserve; schedule reserve | None. Charter: no further funding committed, an increase needs the sponsor's written approval. No schedule reserve is named; the charter cites about one week of float in analysis, design and test, and R12 absorbs two weeks |
| PM authority, escalation limits | Charter Part 2A "Assigned project manager, responsibility, and authority level": the limit per transaction; the reserve limit, the forecast overrun percent, and any change to user-visible scope, schedule or cost that go to the sponsor (read each there) |
| Risk work, cadence, acceptance | Scope package 1.1.1.4 (its hours and cost are on the sheet): register baselined at M1, weekly risk review from M1, sponsor accepts the register at M1 and the closeout risk position at M7; 1.10.2.1 closeout report carries reserve use and final risk position |
| Responses already built as work | Scope package: R5 in 1.2.3.2 and R12 in 1.2.3.3 (Technical Preparation), R6 in 1.7.1.1, R8 and R10 in 1.8.1.3, R12 stores in 1.9.1.1, R11 in 1.10.1.1 |
| Assumptions, constraints, estimates | Charter 1.5 and 1.6; scope package Part 3 estimates are first-pass, re-baselined at M1 |
| Pending change | `docs/forms/3-3-change-request.en.md` (read which milestones it moves and which risks it lists as updated); until the sponsor approves, build from the charter dates |
| Existing risk forms | List `docs/forms/` now, it is the truth (SKILL.md step 3) |

## Traps

- **Names differ between the books.** BoF 4.5 prose and Table 4.5 (p209 to 210/220 to 221) say Control Risks and
  list the PMBOK 5 process names; PMBOK 6 11.7 is Monitor Risks (p453/492). The blank form prints Monitor and
  Control Risks, Perform Qualitative Assessment, Perform Quantitative Assessment. Use the printed labels.
- **Three example scales disagree and all are examples.** Very High probability is over 70% in Table 11-1 (p407/446),
  80% or higher in BoF Table 2.28 (p123/134) and Table 2.31 (p138/149). Never mix them; derive the project's from its
  appetite and write it once in 2.31.
- **Time or Schedule.** 2.31 prints Time, 2.32 and 2.36 print Schedule, 2.33 prints Schedule. One objective, labels as printed.
- **2.32 bank 2 prints Impact; 2.36 bank 2 prints Revised Impact.** Bank 2 of 2.32 has no ID column.
- **2.35 prints no axis titles and no legend**, only grey tones. State the reading once (rows probability, columns
  impact, as Figure 11-5 p408/447) and take zone meaning from the 2.34 rating rules or 2.31; do not invent a legend.
- **Owner and Responsible Party are two boxes.** 2.32 has Owner in bank 1 and Responsible Party in bank 2; BoF Table 2.32
  (p145/156) defines Responsible Party as the person managing the risk. Do not fill both with the same text by default.
- **Contingency reserve is not management reserve** (p252/291, glossary p702/741 and p710/749). The charter form 2B
  page 2 Cost row still says "management reserve use reported monthly" (charter-package.en.md line 464); the budget has only a contingency reserve.
  Flag it in every audit and never repeat it as correct.
- **Plan "does not usually change"** (BoF p121/132) against revisiting at a phase change, a scope change or a
  review of effectiveness (p402/441). Re-issue 2.31 with a new Date Prepared when a 3.3 changes the baselines.
- **A risk that occurs is also an issue** (p457/496; BoF 3.1 p165/176: issues "can also arise from a risk event that has occurred"). The 2.32 entry stays in the register: its
  Status takes the book's values, open or closed (BoF Table 2.29 p129/140), and stays open while the response is carried out; Actions and Comments
  record that it occurred and point to the 3.1 entry, which repeats the ID and the risk statement. Closing is the PM's decision, recorded in 3.2; no
  further rule is stated in the book. (An earlier version of this note said the entry leaves the register; the book does not say so.)
- **A contingent response needs a trigger the team writes.** The book gives no numeric trigger (p445/484) and 2.36 has no trigger box: the Contingency
  Plan element says the plan starts "if specific events occur, such as missing an intermediate milestone" (BoF Table 2.32 p145/156). The charter's
  responses name none, so list the trigger as an open question for the risk owner; never write that it has fired. The "Revised" columns of 2.32 change
  only after the response is carried out.
- **All twelve risks are threats.** The book wants opportunities too (p395/434). None identified is a fact to state, not to invent.
- **Escalate has a book meaning** (p442/481): ownership passes outside the project, and the team stops monitoring.
  The charter uses "escalate to the sponsor" for a decision inside project governance (R3, R8; R9 escalates without naming to whom); say which.
- **Charter dates in responses go stale.** a response that names a date or a break (R8 does) must be copied as written
  and report the conflict if 3.3 is approved.
- **No work package funds a risk audit** and the PM owns the register, so a PM-run 4.5 is not independent (11.7.2.2
  points to the audit of 8.2.2.5, "structured, independent", p456/495 and `pmbok-quality.md`). Report it as unfunded.

## Decisions in this area

Formulas the chapter and the forms give, exactly; everything else below is "not stated in the book".

| Formula | Variables, units, source |
| --- | --- |
| Score = Probability x Impact | Scale values from 2.31, no unit; "can be multiplied" p408/447; BoF Table 2.29 p129/140. Relative scoring combines labels (high-low) |
| Figure 11-5 example values | Probability 0.10, 0.30, 0.50, 0.70, 0.90; impact 0.05, 0.10, 0.20, 0.40, 0.80 (p408/447); an example only |
| Nonlinear impact (example) | Very Low .5, Low 1, Medium 2, High 4, Very High 8 (BoF 2.35 p142/153) |
| Objective weights (example) | Weights sum to 100 percent: schedule 40, scope 20, quality 20, cost 20 (BoF 2.35 p142/153); no weighted-score equation is printed |
| EMV of a branch = sum of probability x net path value | Net path value = payoff minus cost along the path; the decision takes the larger EMV: .60 ($80M) + .40 (-$30M) = $36M and .60 ($70M) + .40 ($10M) = $46M (p435/474) |
| Cost effectiveness = (change in impact level) / (implementation cost) | Both in money when the impact can be monetised; higher is better (p446/485) |
| Criticality index | Frequency, usually a percentage, with which an element is on the critical path across simulation runs (p434/473); no equation printed |
| Contingency reserve | A percentage of the estimated cost, a fixed number, or from quantitative analysis (p245/284); schedule: a percentage of the activity duration or a fixed number of work periods (p202/241) |
| Reserve status | Total, Used to Date, Used This Period, Remaining Reserve (BoF 2.33 p133 to 136/144 to 147); Remaining = Total minus Used to Date is the reading of the labels, not printed |
| This project | The reserve line over the budget gives the share (both amounts are in the charter budget table); no derivation from the listed risks exists |

### 1. How heavy the risk process is, and whether it is written down
- **Arises:** 11.1, "once or at predefined points" (p401/440); before M1 when the register is baselined (1.1.1.4). Revisit at a phase change, a significant scope change or after a review of effectiveness (p402/441).
- **Techniques and trade-offs:** Expert judgment; stakeholder analysis for appetite; Meetings with a facilitator (p404/443). Tailor by size, complexity, importance, development approach (p400/439). BoF p121/132: small project, simplified register, 3 x 3 matrix, risk in the status report; large, a granular matrix, quantitative assessment, audits, reports; agile, risk at each iteration start and retrospective. Matrix size 3 x 3 small, 5 x 5 medium, 10 x 10 large (BoF p137/148, p142/153). The cost of detail is not quantified.
- **Inputs, kept in:** charter risks and rating (2A), stakeholder list, the other plans (scope package; no separate plan exists). Organizational thresholds and templates: not in `docs/`, ask.
- **Recorded in:** 2.31 all boxes; 3.2 for the tailoring choices (matrix size, quantitative or not).
- **Wrong move:** copying a large-project process, or none. The plan exists so "the degree, type, and visibility of risk management are proportionate" (p401/440).

### 2. Thresholds, scales and scoring scheme
- **Arises:** 11.1.3.1 (p407 to 408/446 to 447); the workshop "may start by reviewing and confirming the probability and impact scales" (p426/465).
- **Options:** three levels for a simple process, five for a detailed one (p407/446); descriptive or numeric; a matrix per objective, or one priority by combining objectives or taking the highest (p425/464); linear or doubling scores, objective weights, tighter ranges for a critical objective, cut-offs tuned to appetite (BoF p137/148, p142/153). Threats and opportunities share one matrix with positive impact definitions for opportunities (p408/447).
- **Inputs, kept in:** appetite as measurable limits per objective (p407/446). The project's nearest limits are the charter objectives (cost variance per gate, milestone slip, acceptance criteria, UAT pass rate) and the reserve limit in the authority block. A stated risk appetite is not in `docs/`; ask the sponsor.
- **Recorded in:** 2.31 Stakeholder Risk Tolerances, Definitions of Probability, Definitions of Impact by Objective, Probability and Impact Matrix; 2.34 and 2.35 only if no plan holds them; 3.2.
- **Formula:** Score = Probability x Impact, with the example values above.
- **Wrong move:** pasting a book example as the definitions. The definitions "reflect the risk appetite and thresholds" of the stakeholders (p407/446), and the three books' examples disagree.

### 3. How to identify risks
- **Arises:** 11.2, "throughout the project" (p409/448); first for the M1 register, then at each cycle the plan sets (p411/450) and each risk review.
- **Techniques and trade-offs:** brainstorming (comprehensive but ideas arrive not fully formed); checklists (quick, but "impossible to build an exhaustive one" and not a substitute for identification); interviews (trust and confidentiality); root cause analysis (from a problem or benefit statement); assumption and constraint analysis (inaccuracy, instability, inconsistency, incompleteness); SWOT; document analysis (inconsistency between documents signals risk); prompt lists (RBS, and PESTLE, TECOP, VUCA for overall risk); risk workshop (p414 to 416/453 to 455). Expert bias is to be taken into account (p414/453).
- **Inputs, kept in:** assumptions 1 to 19 and constraints (charter 1.5, 1.6); WBS (scope package Part 2, the framework p412/451); estimates (Part 3, first-pass); issue log (3.1, none yet); agreements for the SMS gateway and hosting; lessons learned.
- **Recorded in:** 2.32 ID, Risk Statement, Owner, Response (preliminary); the charter assumption list when an assumption changes (p418/457).
- **Wrong move:** one technique only, or a statement without a format. A "consistent format should be used for risk statements" (p411/450); BoF gives "EVENT may occur, causing IMPACT" (p129/140).

### 4. Which risks get attention first, who owns them, which go on the watch list
- **Arises:** 11.3, "regularly" per the plan, in agile before each iteration (p421/460).
- **Techniques and trade-offs:** risk data quality assessment (weighted score over completeness, objectivity, relevancy, timeliness; poor data may mean gathering better data, p423/462); probability and impact assessment by interview or meeting, assumptions recorded; other parameters for "a more robust prioritization" (p424/463); risk categorization (p425/464); matrix, or a bubble chart when more than two parameters (p425 to 426/464 to 465). Assessments are subjective and biased, so the facilitator corrects for bias (p420/459).
- **Inputs, kept in:** R1 to R12, scales from 2.31, stakeholder list for owners. Scores and owners do not exist yet; a scoring session produces them.
- **Recorded in:** 2.32 Owner, Probability, Impact, Score; 2.35; watch list in Comments (no box); 2.34 rating.
- **Formula:** Score = Probability x Impact.
- **Wrong move:** no owner. Each risk gets one who plans the response and reports progress (p421/460, p426/465). Guessing scores is also wrong here (house-style).

### 5. Which risks to analyse quantitatively, or none
- **Arises:** 11.4, only if the plan requires it (p429/468); after 11.3, and again after 11.5 to test whether responses reduce overall risk (p429/468).
- **Options:** the chapter lists projects where it is likely appropriate: large or complex, strategically important, contractual, or a key stakeholder requires it; it needs high-quality data and a sound scope, schedule and cost baseline, specialised software and expertise, and costs time and money (p429/468). Candidate risks are those the qualitative step judged to have significant potential to affect objectives (p429/468); no score cut-off is stated. Techniques: simulation (Monte Carlo on cost, or on network and durations), sensitivity analysis (tornado), decision tree (EMV), influence diagrams, with distributions or probabilistic branches and correlation (p432 to 436/471 to 475). BoF p131/142: many projects omit it.
- **Inputs, kept in:** baselines and first-pass estimates (scope package Parts 2 and 3, charter milestones); numeric P and I (missing). The schedule re-baseline in 3.3 is pending, so there is not yet a sound schedule baseline.
- **Recorded in:** 2.31 Methodology and Risk Tracking and Audit (whether, how often, who); 2.33 page 3; 3.2 if the decision is not to.
- **Formula:** EMV and criticality index above.
- **Wrong move:** a simulation on thin data. The analysis "depends on the availability of high-quality data" and a sound baseline (p429/468).

### 6. Response strategy for one threat or opportunity
- **Arises:** 11.5 after prioritisation; the owner plans a response for every risk "sufficiently important" (p439/478).
- **Options and stated trade-offs, threats** (escalate p442/481; avoid, transfer, mitigate, accept p443/482): avoid (high-priority, high-probability, large-impact threats; may change the plan, extend the schedule or reduce scope); transfer (shifts ownership, usually a risk premium; insurance, bonds, warranties, agreements); mitigate (early action beats repair; fewer complex processes, more tests, prototypes, redundancy); accept (low priority, or no cost-effective alternative; active means a contingency reserve, passive means periodic review); escalate (decision 10). The avoid text includes action to "isolate the project objectives from the risk's impact", while the mitigate text includes prototypes, more tests and "designing redundancy into a system" (p443/482): a mixed response (isolate behind one interface, prove with a proof of concept, keep a second provider) is classified part by part, the book gives no rule for a mix, and the label is judgment recorded in 3.2. A second provider used only if the first fails is a contingent response or fallback plan (p445/484). **Opportunities** (p444/483): exploit (raise probability to 100%), share (premium), enhance (more resources to finish early), accept, escalate.
- **Choosing:** alternatives analysis; cost-benefit analysis when the impact can be monetised; multicriteria decision analysis over cost of response, effectiveness, resource availability, timing (urgency, proximity, dormancy), impact level, effect on related risks, secondary risks (p446/485). A response must be appropriate, cost-effective, realistic, agreed and owned (p439/478). Large projects may use optimisation or real options (p439/478).
- **Inputs, kept in:** R1 to R12 current responses (charter 2A, not labelled with a strategy name); contingency reserve; schedule and team assignments (scope package); several responses already exist as work packages, so cite the package.
- **Recorded in:** 2.32 Response (the charter's wording, no label added; a strategy label goes in Comments), Actions, Revised columns, Responsible Party; 2.36 Responses, Secondary Risks, Residual Risk; response work added to the schedule (p448/487).
- **Formula:** cost effectiveness = (change in impact level) / (implementation cost).
- **Wrong move:** an unnamed or unowned response. "Unsuitable risk responses can have the converse effect" (p439/478). Cutting estimates is not a strategy in 11.5.2.4.

### 7. Response to overall project risk
- **Arises:** when overall exposure is outside the thresholds, from 11.4 results or a justified judgement (p445/484); the charter rates it Medium with no analysis behind it.
- **Options** (p445 to 446/484 to 485): avoid (remove high-risk scope, or cancel only if the level "is, and will remain, unacceptable"); exploit (add high-benefit scope, or widen thresholds with stakeholder agreement); transfer or share (third party, joint venture, subcontract, a premium); mitigate or enhance (replan, change scope and boundaries, priority, resources, delivery times); accept (an overall contingency reserve, or periodic review).
- **Inputs, kept in:** charter 2A overall project risk, thresholds from decision 2.
- **Recorded in:** 2.33 Overall Risk Status and Trends, Significant Drivers, Recommended Responses; 3.3 when scope, boundaries or dates change; 3.2.
- **Wrong move:** summing the register. Overall risk arises from "all sources of uncertainty" (p397/436) and only quantitative analysis is "the only reliable method" to assess it (p429/468).

### 8. Contingency reserve for cost and time, and the management reserve question
- **Arises:** estimating (7.2, 6.4), budget (7.3), after 11.5 and at each reserve analysis in 11.7 (p456/495).
- **Options:** a percentage, a fixed number, or quantitative methods, at any level from activity to project (p245/284); schedule likewise, aggregated and "clearly identified in the schedule documentation" (p202/241); quantitative analysis can give "amount of contingency reserve needed to provide a specified level of confidence" (p436/475). As information improves the contingency reserve can be used, reduced or eliminated (p245/284, p202/241). Management reserve covers unknown unknowns, sits outside the cost baseline, and its use is an approved baseline change (p252/291, p254/293). Resilience adds reserve for emergent risks besides the specific risk budget (p399/438). No percentage or confidence level is stated; BoF p142/153 says many red-zone risks need more contingency, time and budget.
- **Inputs, kept in:** budget line 6 and its roll-up; R1 to R12 with scores (missing). This project has no management reserve and no named schedule reserve; creating either is a sponsor decision by 3.3.
- **Recorded in:** 2.31 Risk Management Funding and Contingency Protocols (who may draw, how much, through what); 2.36 Contingency Funds and Contingency Time; 2.33 Reserve Status; 3.2 for the sizing method.
- **Formula:** contingency = percentage x estimated cost, or a fixed number (PM 7.2.2.6 p245 (PDF 284)); the project's share is the reserve line divided by the budget, read from the charter table.
- **Wrong move:** a reserve with no link to risks. Contingency is "allocated for identified risks" (p245/284), so the reserve should be derived from R1 to R12 or labelled a percentage allowance with the date it will be derived.

### 9. When to trigger a contingency plan
- **Arises:** a contingent response is planned in 11.5 "if it is believed that there will be sufficient warning" and run in 11.7 (p445/484).
- **Techniques:** contingent response strategies; trigger conditions "should be defined and tracked" (p445/484); register entries for triggers, warning signs, contingency and fallback plans (p448/487); technical performance analysis (p456/495). BoF p145/156: a contingency plan applies when the risk or residual risk is accepted; a fallback plan when other strategies fail. No numeric trigger is given.
- **Inputs, kept in:** charter responses with triggers: R3 missed slot, R4 replacement after a loss, R8 forecast slip past the date it names, R9 analysis rework beyond the time it names after M1, R12 app slip up to the time it names, R1 UAT failure (options to the sponsor within the time it names); read each trigger as written.
- **Recorded in:** 2.36 Contingency Plan (trigger and action), Fallback Plans; 2.32 Actions and Status; an issue in 3.1 once the risk has occurred.
- **Wrong move:** a contingency plan with no tracked trigger, or for a risk that gives no warning, where the book does not offer it.

### 10. When to escalate
- **Arises:** 11.5 when the team or sponsor agrees a threat or opportunity is outside project scope, or the response would exceed the PM's authority (p442/481, p444/483).
- **Procedure:** the PM decides whom to notify and communicates; the relevant party must accept ownership; escalate to the level matching the affected objective; after escalation the project team does not monitor it, though the register may record it.
- **Inputs, kept in:** charter PM authority limits (table above) and the sponsor's authority ("Name and authority of the sponsor").
- **Recorded in:** 2.32 Response (Escalate), Status, Comments with the accepting party and date; 3.2.
- **Wrong move:** using Escalate for what the sponsor merely approves. Sponsor approval of a baseline change is decision 11 and the project keeps the risk.

### 11. A response changes a baseline
- **Arises:** 11.5.3.1, 11.6.3.1, 11.7.3.2: responses and corrective or preventive actions "may result in a change request" to the cost and schedule baselines or other plan parts (p447/486, p451/490, p457/496); examples of avoid that do so are extending the schedule or reducing scope (p443/482).
- **Options:** a reserve draw is a 3.3 where the charter requires change control for every draw (read the reserve budget line and the authority block); a draw inside the project manager's limit without a request only if the charter says draws need none, and when it is silent ask the sponsor and record the answer in 3.2. A response that moves a baseline is a 3.3 to the sponsor. When constraints cannot all hold the route is a change request, never trimmed estimates.
- **Recorded in:** 3.3 (Category, Impacts of Change, Disposition); 3.2; the 2.32 Comments cite the 3.3 ID.
- **Wrong move:** changing the plan without a request. "Any change to the project management plan goes through the organization's change control process via a change request" (p447/486).

### 12. Review cadence, reserve adequacy and audit
- **Arises:** 11.7 "throughout the project" (p453/492); cadence and audit frequency are set in 2.31, and the PM ensures audits happen (p456/495).
- **Techniques:** risk reviews, in a status meeting or dedicated (p457/496); reserve analysis comparing remaining contingency with remaining risk, shown as a burndown chart (p456/495); technical performance analysis; risk audits with format and objectives defined beforehand. No cadence is stated.
- **Inputs, kept in:** weekly review from M1 (1.1.1.4-A2); reserve use; work performance data. An audit budget: none.
- **Recorded in:** 2.31 Frequency and Timing, Risk Tracking and Audit; 2.32 revised columns and Status; 2.33 Metrics, Reserve Status, Assessment of Reserve Adequacy; 4.5.
- **Wrong move:** documenting responses and not acting. "no action is taken to manage the risk" is the book's named common problem (p450/489).
