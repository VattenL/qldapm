# PMBOK 6 chapter 6, Project Schedule Management, for forms 2.11 to 2.18

Read this before filling 2.11 Schedule Management Plan, 2.12 Activity List, 2.13 Activity Attributes, 2.14
Milestone List, 2.15 Network Diagram, 2.16 Duration Estimates, 2.17 Duration Estimating Worksheet or 2.18
Project Schedule. The forms print the boxes; chapter 6 says what goes in them and which technique decides
each one. A remedy proposed to the team carries the PMBOK name of its technique and its stated trade-off.

Citation shorthand used here, so each claim carries both numbers: `PM 6.4.2.6 p202 (PDF 241)` is PMBOK 6
section, printed page, then PDF page (PDF = printed + 39). `BoF 2.17 p73 (PDF 84)` is the Book of Forms,
printed page, then PDF page (PDF = printed + 11; every form's pages are in `forms-index.md`). A bare form
number such as "2.17" is a Book of Forms form; a PMBOK section is always written "PM".

## Where it is

`PMBOK6_and_Agile_Practice_Guide.pdf` at the repo root. `pdftotext -layout` returns the text interleaved
with a vertical watermark of one to three letters per line and a "PMI Member benefit" footer; drop those
lines before reading. This note does not use the Agile Practice Guide part.

| Section | Printed page | PDF page |
| --- | --- | --- |
| 6 intro, Figure 6-1; key concepts, trends, tailoring, agile | 173 to 178 | 212 to 217 |
| 6.1 Plan Schedule Management; 6.1.3.1 component list on 181 to 182 | 179 to 182 | 218 to 221 |
| 6.2 Define Activities; outputs 6.2.3 on 185 to 186 | 183 to 186 | 222 to 225 |
| 6.3 Sequence Activities; PDM 189 to 190, dependencies 191 to 192, leads and lags 192 to 193, outputs 194 | 187 to 194 | 226 to 233 |
| 6.4 Estimate Activity Durations; techniques 200 to 203, outputs 203 to 204 | 195 to 204 | 234 to 243 |
| 6.5 Develop Schedule; techniques 209 to 216, outputs 217 to 221 | 205 to 221 | 244 to 260 |
| 6.6 Control Schedule; techniques 226 to 228, outputs 228 to 230 | 222 to 230 | 261 to 269 |
| Equations kept in other chapters: beta cost (7.2.2.4), SV and SPI (7.4.2.2), earned schedule | 245; 262 to 263; 233 | 284; 301 to 302; 272 |

Two numbering traps. The Book of Forms Agile forms are 6.1 to 6.4 (6.2 is the Product Backlog); PMBOK 6.2
is Define Activities. And PM 6.5 p207 (PDF 246) says schedule maintenance is "described in Section 6.7";
chapter 6 has no 6.7, the process is Control Schedule 6.6.

## Chapter 6 terms worth using, with the book's meaning

- **Activity** versus **work package**: activities are the effort to complete a work package (PM 6.2.2.2 p185
  (PDF 224)). **Rolling wave planning**: near-term work in detail, later work at a higher level, a form of
  progressive elaboration (PM 6.2.2.3 p185 (PDF 224)).
- **Milestone**: a significant point or event with zero duration, mandatory (contract) or optional (historical
  information) (PM 6.2.3.3 p186 (PDF 225)).
- **PDM relationships**: finish-to-start (the most used), finish-to-finish, start-to-start, start-to-finish
  (very rarely used) (PM 6.3.2.1 p190 (PDF 229)). **Mandatory** (hard logic) versus **discretionary** (soft
  logic), **internal** versus **external** dependencies (PM 6.3.2.2 p191 to 192 (PDF 230 to 231)).
- **Lead** advances a successor against its predecessor; **lag** delays it. A lead is often a negative lag
  in software (PM 6.3.2.3 p192 to 193 (PDF 231 to 232)). **Path convergence** is an activity with more than one
  predecessor, **divergence** more than one successor, and both carry more risk (PM 6.3.3.1 p194 (PDF 233)).
- **Duration** is the number of work periods an activity needs with the estimated resources and calendars;
  it excludes lags (PM 6.4 p195 to 197 (PDF 234 to 236); PM 6.4.3.1 p203 (PDF 242)). **Basis of estimates** is
  the support showing how it was derived (PM 6.4.3.2 p204 (PDF 243)).
- **Critical path**: the longest path, the shortest possible project duration, least total float, usually
  zero. **Total float**: how long an activity can slip from early start without delaying the finish or
  violating a constraint. **Free float**: the slip that does not delay a successor's early start. **Negative
  float**: a late-date constraint violated by duration and logic (PM 6.5.2.2 p210 (PDF 249)).
- **Resource leveling** adjusts dates to resource supply and can change the critical path; **resource
  smoothing** keeps the critical path and spends only free and total float (PM 6.5.2.3 p211 (PDF 250)).
- **What-if analysis**, **simulation** (Monte Carlo) (PM 6.5.2.4 p213 (PDF 252)); **crashing** adds resources,
  **fast tracking** overlaps activities normally in sequence (PM 6.5.2.6 p215 (PDF 254)).
- **Contingency reserve** (schedule reserve): duration inside the schedule baseline for identified accepted
  risks. **Management reserve**: for unknown unknowns, outside the baseline (PM 6.4.2.6 p202 (PDF 241)).
- **Schedule baseline**: the approved schedule model, changed only by formal change control (PM 6.5.3.1 p217
  (PDF 256)). **Control thresholds**, **SV**, **SPI** (PM 6.1.3.1 p182 (PDF 221)).

## How each process's output maps onto the forms

PMBOK names components; the form prints boxes. Where a component has no box, the right-hand column says where
it goes. Anything that must stay outside the printed form goes in the italic reading paragraph above it.

| PMBOK component | Form box | If no box |
| --- | --- | --- |
| **2.11 from PM 6.1.3.1 p181 to 182 (PDF 220 to 221)** | | |
| Schedule model development: method and tool | Schedule Methodology; Scheduling Tools | |
| Release and iteration length (time boxes) | none | Schedule Methodology; BoF 2.11 tailoring p56 (PDF 67) |
| Level of accuracy (may include contingency); units of measure | Level of Accuracy; Units of Measure | |
| Organizational procedures links (WBS is the framework) | Organizational Procedure Links | |
| Schedule model maintenance | Schedule Updates | |
| Control thresholds, usually percentage deviations | Variance Thresholds | |
| Rules of performance measurement (EVM, percent complete, SV, SPI) | none | beside Variance Thresholds; BoF 2.11 tailoring p56 (PDF 67) |
| Reporting formats and frequency | Schedule Reporting and Format | |
| How reserve is used (PM 6.6.1.1 p224 (PDF 263)) | none | Schedule Updates |
| **2.12 from PM 6.2.3.1 p185 (PDF 224)** | | |
| Activity identifier; scope of work description | ID; Activity; Description of Work | |
| WBS ID (PM 6.2.3.2 p186 (PDF 225)) | none on 2.12 or 2.13 | carry it inside ID (the dictionary's `1.1.1.2-A1`) |
| **2.13 from PM 6.2.3.2 p186 (PDF 225)** | | |
| Predecessors, successors, relationships, leads and lags | the Predecessors, Relationship, Lead or Lag, Successor columns | |
| Resource requirements | Number and Type of Team Resources Required; Skill Requirements; Required Resources | |
| Imposed dates and constraints; assumptions; place of work; type of effort | Imposed Dates or Other Constraints (one box); Assumptions; Location of Performance; Type of Effort | |
| Duration estimate (PM 6.4.3.3 p204 (PDF 243)) | none | lives on 2.16, same ID |
| Project calendar the activity uses; dependency attributes (mandatory or discretionary, internal or external) | none | Assumptions; the 2.15 narrative |
| **2.14 from PM 6.2.3.3 p186 (PDF 225)** | | |
| Milestone, mandatory or optional | Milestone; Milestone Description; Type | |
| Scheduled date (PM 6.3.1.2 p188 (PDF 227)) | none; no ID column either (BoF 2.14 p65 (PDF 76)) | date in 2.18; the M-number inside Milestone |
| **2.15 from PM 6.3.3.1 p194 (PDF 233)** | | |
| Summary narrative of the sequencing approach and any unusual sequence | none | reading paragraph above the form |
| **2.16 from PM 6.4.3.1 and 6.4.3.2 p203 to 204 (PDF 242 to 243)** | | |
| Duration estimate and the effort behind it | Duration Estimate; Effort Hours | |
| Range, confidence level, assumptions, constraints, risks (basis of estimates) | none | reading paragraph, 2.17 columns, assumption log (PM 6.4.3.3 p204 (PDF 243)) |
| **2.17 from PM 6.4.2 p200 to 202 (PDF 239 to 241)** | | |
| Parametric, analogous, three-point (one sub-table each); bottom-up, reserve and alternatives analysis (none) | sub-tables | name the other technique in the reading paragraph |
| **2.18 from PM 6.5.3 p217 to 220 (PDF 256 to 259)** | | |
| Project schedule: bar chart, milestone chart, network diagram | page 1 Gantt (ID, WBS, Task Name, Start, Finish); page 2 milestone chart (ID, Task Name, Finish) | |
| Schedule baseline (approved version) | none | status of the schedule, stated in the reading paragraph |
| Schedule data: histograms, alternative schedules, applied reserves; project calendars | none | reading paragraph; a separate section marked as not printed |

PM 6.5.1 p207 to 208 (PDF 246 to 247) lists the inputs of 2.18; BoF 2.18 p78 (PDF 89) adds the scope statement.

## Where this project's facts live

List `docs/forms/` now, it is the truth (SKILL.md step 3). Forms 2.11 to 2.17, a scope management plan, a development
approach and a network diagram are forms to create unless it holds them (scope package "Inputs actually used"). Say so, do not cite them.

| Fact | Where |
| --- | --- |
| Milestones M0 to M7 and their charter dates | `docs/charter-package.en.md`, Part 2A "Summary milestone schedule" and form 1.1 page 3 |
| The fixed duration; whether the first warranty month is inside the project; what the charter says of the break that follows closeout; the team and the part-time person | charter section 1.5 |
| Assumptions 8 (when the break starts), 9 (person-months as a funding basis), 10 (part-time availability of the customer staff), 14 (no other holiday), 18 (store review time) | charter section 1.6 |
| Schedule risks R3, R4, R7, R8, R9, R12 (R8 escalates on the forecast go-live date it names); the float the charter claims | charter Part 2A "Overall project risk" |
| Time objective "no milestone more than 1 week late"; schedule changes beyond the PM go to the sponsor, who "sets acceptable variance limits" | charter Part 2A objectives, project manager and sponsor sections |
| The contingency reserve is a cost line; whether any schedule reserve is stated | charter budget line 6 |
| Activities (rows `<package>-A<n>`), resource, effort hours (effort, not calendar loading), per-package Due Dates, hours per person-month; levelling happens in 1.1.1.2 | `docs/scope-package.en.md` Part 3 and "Reading convention" |
| Levelled forecast: its reading paragraph states the hours a working day, the excluded days, whether the break is in the calendar, the divided activities and the fast-tracking allowance | `tools/level.py`, `docs/forms/2-18-project-schedule.en.md` |
| The forecast milestone dates and the working days they move, awaiting the sponsor | `docs/forms/3-3-change-request.en.md` |

## Traps

- **Pending 3.3.** While a 3.3 is undecided the charter is the baseline and a second request on the same milestones is cross-referenced to it;
  whether to amend, replace or fold in is not stated in the book (decisions.md section 4).
- **Forecast is not baseline.** The levelled dates are a forecast until the sponsor approves 3.3; the baseline
  changes only by formal change control (PM 6.5.3.1 p217 (PDF 256)). The charter's milestone schedule is an
  input to 6.1 (PM 6.1.1.1 p180 (PDF 219)), not the schedule baseline, which Develop Schedule produces.
- **Schedule built before its inputs.** PM 6.5.1.2 p207 (PDF 246) lists the activity list and network diagrams
  as inputs, and every activity but the first and last needs a predecessor and a successor (PM 6.3 p188 (PDF
  227)). 2.12 and 2.15 do not exist, so 2.18 keeps gate order, not logic; "critical path" or "float" claims
  (the charter's "about one week of float") have no network behind them.
- **CPM ignores resources; the schedule does not.** CPM runs "without regard for any resource limitations"
  (PM 6.5.2.2 p210 (PDF 249)). Leveling "can often cause the original critical path to change" (PM 6.5.2.3
  p211 (PDF 250)); the 31 working days of 3.3 is what leveling did, not float consumed.
- **Dividing an activity between two people** (the levelling helper rule) adds resources. Doubling them does
  not halve the time (PM 6.4 p197 (PDF 236)); crashing "does not always produce a viable alternative and may
  result in increased risk and/or cost" (PM 6.5.2.6 p215 (PDF 254)). The 97 divisions assume no coordination
  loss; say so.
- **Fast tracking across a gate** "may result in rework and increased risk"; review discretionary dependencies
  first (PM 6.5.2.6 p215 (PDF 254); PM 6.3.2.2 p191 (PDF 230)). Charter funding follows milestone acceptance and
  no document says whether a gate is mandatory or discretionary: mark [TBD].
- **Duration excludes lags** (PM 6.4.3.1 p203 (PDF 242)); leads and lags "should not replace schedule logic"
  (PM 6.3.2.3 p193 (PDF 232)); a lag is not float (BoF 2.15 p67 (PDF 78)). A package's Due Dates window is a gate
  relation, not an activity duration; duration comes from 2.16 and 2.17.
- **The 2.17 parametric equation contradicts its own prose.** The performance factor row says a skilled
  resource is .8 and "you multiply the effort hours times" it (BoF 2.17 p75 (PDF 86)), so skilled is faster; the
  printed equation divides by it and its example gives 125 hours, where multiplying gives
  150 x .8 / (2 x .75) = 80. Which governs is not stated in the book. Name the reading used in the reading
  paragraph; a skilled resource must not come out slower (a consistency check, not a book rule).
- **Two three-point equations.** PM 6.4.2.4 p201 (PDF 240) prints only the triangular one for duration, for
  "insufficient historical data" or judgmental data; 2.17 prints the beta one as "common" and says the project's
  needs decide (BoF 2.17 p73 (PDF 84); p76 (PDF 87)). The Weighting Equation column names the one used. On the
  book's sample, triangular gives (20 + 25 + 36) / 3 = 27 days and beta gives 26.
- **Reserve vocabulary.** The reserve budget line is a cost contingency reserve; charter form 2B's Cost row says
  "management reserve use reported monthly", a source error to report, not copy. Float is not a schedule reserve.
- **SPI alone misleads**: it measures all work, so critical path performance is checked too (PM 7.4.2.2 p263
  (PDF 302)). The 5 percent in the charter is a cost band, not a schedule threshold.

## Decisions in this area

**D1. Scheduling method, tool, and whether to time-box.**
- When: 6.1, once or at predefined points (PM 6.1 p179 (PDF 218)); trigger is an approved charter and a known
  development approach (PM 6.1.1 p180 (PDF 219)).
- Techniques: alternatives analysis (PM 6.1.2.2 p181 (PDF 220)) on method or mix, detail, wave length and review
  frequency; trade-off stated: the detail needed to manage against the time to keep it current. Iterative
  scheduling "welcomes changes"; on-demand scheduling pulls work and suits incremental sustainment (PM p177
  (PDF 216)).
- Inputs: charter milestones, scope baseline, development approach (no document; the scope package says
  predictive with two build iterations). Recorded in: 2.11 Schedule Methodology, Scheduling Tools; 2.1
  Development Approaches. Formula: none.
- Wrong move: a schedule more detailed than the team can keep current (the trade-off above).

**D2. Level of accuracy, units, and how deep to define activities now.**
- When: accuracy and units in 6.1; activities in 6.2, "throughout the project" (PM 6.2 p183 (PDF 222)); trigger
  is a work package entering the near term, or elaboration finding work outside the baselines.
- Techniques: decomposition, with team members involved for better accuracy (PM 6.2.2.2 p185 (PDF 224)); rolling
  wave planning, near-term detail and later summary (PM 6.2.2.3 p185 (PDF 224)).
- Inputs: WBS and dictionary, `docs/scope-package.en.md` Parts 2 and 3. Recorded in: 2.11 Level of Accuracy,
  Units of Measure; 2.12 rows; 3.3 for work outside the baselines. Formula: none.
- Wrong move: adding newly found work straight into the baseline; the book routes it as a change request
  through integrated change control (PM 6.2.3.4 p186 (PDF 225)).

**D3. Dependencies, leads, lags and constraints.**
- When: 6.3, throughout; trigger is an activity list with attributes, and again before any fast tracking.
- Techniques: precedence diagramming with FS, FF, SS, SF (PM 6.3.2.1 p190 (PDF 229)); dependency determination
  (PM 6.3.2.2 p191 to 192 (PDF 230 to 231)): mandatory is legal, contractual or inherent; discretionary "should be
  fully documented since they can create arbitrary total float values and can limit later scheduling options".
  Leads and lags only in limited circumstances (PM 6.5.2.5 p214 (PDF 253)).
- Inputs: activity list and attributes, assumption log, milestone list (PM 6.3.1.2 p188 (PDF 227)); here the
  charter gates and dictionary Due Dates, the only logic recorded.
- Recorded in: 2.13 Predecessors, Relationship, Lead or Lag, Successor, Imposed Dates or Other Constraints,
  Assumptions; 2.15; 2.14 Type; assumption log (1.2).
- Formula: notation only. Lag FS+3d, lead FS-3d (BoF 2.15 p67 (PDF 78)); "SS+10" (PM p193 (PDF 232)).
- Wrong move: a lead or lag in place of logic (PM 6.3.2.3 p193 (PDF 232)); a tool constraint treated as a
  mandatory dependency (PM 6.3.2.2 p191 (PDF 230)); two relationships between one pair or a closed loop, "not
  recommended" (PM 6.3.2.1 p190 (PDF 229)).

**D4. Which estimating technique for each activity.**
- When: 6.4, throughout; trigger is an activity with attributes and resources.
- Techniques (PM 6.4.2 p200 to 202 (PDF 239 to 241)): analogous, cheaper and quicker but less accurate, for little
  detail, "most reliable" when activities are similar "in fact and not just in appearance"; parametric, higher
  accuracy depending on the model and its data; three-point, gives a range, triangular for thin or judgmental
  data; bottom-up, decompose an activity not estimable "with a reasonable degree of confidence", then aggregate.
- Inputs: dictionary effort, resource calendars and requirements, assumption log, risk register, lessons learned
  (PM 6.4.1.2 p198 to 199 (PDF 237 to 238)). No document names the technique behind the first-pass hours:
  write [TBD], never a technique nobody used.
- Recorded in: 2.17 sub-table; 2.16 Effort Hours, Duration Estimate; assumption log for the basis.
- Formulas, variables defined:
  - Parametric: duration = quantity of work x labor hours per unit of work; 1,000 meters at 25 meters per hour
    is 40 hours (PM 6.4.2.3 p200 to 201 (PDF 239 to 240)).
  - 2.17 parametric: Effort / (quantity x percent available x performance factor) = duration. Effort in hours,
    quantity in people, percent available as a fraction, factor 1.0 average, .8 skilled, 1.2 less skilled;
    150 / (2 x .75 x .8) = 125 hours (BoF 2.17 p75 (PDF 86)); see the trap on its direction.
  - Analogous: multiplier = current size / previous size; duration = previous duration x multiplier; 200 / 160 =
    1.25, 10 days x 1.25 = 12.5 days (BoF 2.17 p75 (PDF 86)).
  - Three-point, tO, tM, tP, tE in one unit: tE = (tO + tM + tP) / 3 (PM 6.4.2.4 p201 (PDF 240)); tE = (tO + 4tM
    + tP) / 6 (BoF 2.17 p76 (PDF 87)); (20 + 4(25) + 36) / 6 = 26 days.
  - One person, effort to elapsed time: days = hours / 8; weeks = hours / 40 (BoF 2.16 p70 (PDF 81)).
- Wrong move: an analogous estimate from a project that only looks alike (reason above); estimates that include
  lags (PM 6.4.3.1 p203 (PDF 242)); no basis of estimates (PM 6.4.3.2 p204 (PDF 243)).

**D5. How many people on an activity.**
- When: 6.4 and 6.5; trigger is an activity too long for its gate or a person over-allocated.
- Techniques: duration factors (PM 6.4 p197 (PDF 236)): diminishing returns, number of resources, technology,
  staff motivation (student syndrome, Parkinson's law); alternatives analysis of resource capability and
  compression (PM 6.4.2.6 p202 (PDF 241)). Trade-off: more people shorten it, not linearly, and add
  coordination and risk.
- Inputs: resource calendars, requirements, team assignments; here assumptions 9, 10, 17 and the sheets.
- Recorded in: 2.13 Number and Type of Team Resources Required, Skill Requirements; 2.17 Resource Quantity,
  % Available. Formula: the 2.17 parametric one; the book gives none for diminishing returns.
- Wrong move: doubling people to halve the time; the book's reasons are knowledge transfer, learning curve and
  coordination (PM 6.4 p197 (PDF 236)).

**D6. Whether to hold a schedule reserve, and how large.**
- When: 6.4 estimating and 6.5 network analysis; trigger is an identified accepted risk, or converging paths.
- Techniques: reserve analysis (PM 6.4.2.6 p202 (PDF 241)): contingency reserve is "a percentage of the estimated
  activity duration or a fixed number of work periods", may be aggregated, and may be used, reduced or
  eliminated as information firms up; management reserve is outside the baseline and, by contract terms, its use
  may need a baseline change. Network analysis: aggregate reserves where paths converge or diverge, reserve or
  respond for high-risk or long-lead critical path work (PM 6.5.2.1 p209 (PDF 248)). Risk enters as the "expected
  or mean risk impact" (PM 6.5.1.2 p208 (PDF 247)); simulation gives finish-date probabilities, such as 10 percent
  by 13 May and 90 percent by 28 May (PM 6.5.2.4 p213 to 214 (PDF 252 to 253)).
- Inputs: risk register (charter R3, R4, R7, R8, R9, R12), assumptions 8 and 18.
- Recorded in: 2.16 or 2.18 as applied reserve (PM 6.5.3.3 p220 (PDF 259)); 2.11 Level of Accuracy and Schedule
  Updates for use rules; 3.2 for the decision. Formula: none for the size; only the two forms above.
- Wrong move: a reserve hidden in activity durations; "Contingency should be clearly identified in the schedule
  documentation" (PM 6.4.2.6 p202 (PDF 241)).

**D7. Resolving over-allocation: leveling or smoothing.**
- When: 6.5 before baselining, and 6.6 on a forecast overrun; trigger is a person booked above available hours
  (`tools/level.py` reports it).
- Techniques (PM 6.5.2.3 p211 (PDF 250)): leveling balances demand with supply, uses available float, can change
  the critical path; smoothing keeps the critical path and finish date, moves activities only within free and
  total float, and "may not be able to optimize all resources".
- Inputs: resource calendars and requirements, 2.13 resource boxes; here the dictionary and the 8-hour day.
- Recorded in: 2.18; changed requirements (PM 6.5.3.7 p221 (PDF 260)); 3.3 if dates move. Formula: none.
- Wrong move: quoting a pre-leveling critical path or float after leveling (PM 6.5.2.3 p211 (PDF 250)).

**D8. Shortening the schedule when constraints cannot all hold.**
- When: 6.5 with negative float, or 6.6 on a slip; trigger is a baseline or imposed date the logic misses.
- Step 0, absorb check: verify the stated slip against the due dates in 2.10 and 2.18 (a work package the user places at one milestone may belong to
  another), then compare it with the variance threshold in 2.11 (PM 6.1.3.1 p182 (PDF 221)), the total float on the path (PM 6.5.2.2 p210
  (PDF 249)) and any allowance the charter states for the work (here the charter risk row whose response allows an app slip, read beside the
  time criterion in the charter; when the two disagree, report the tension and do not pick a reading). Testing the slip against them before compressing is the
  team's order of work, not a book rule. `pm_calc.py cpm --slip` does the float arithmetic once a network exists.
- Resource cost of a window: a resource priced per hour or per person-month (here the part-time mobile developer: read the person-months from the charter, the hours and the rate from the scope package roll-up)
  costs money for every hour added or month kept (hours times rate is the line in the scope package roll-up), so a longer window or more hours is a cost and resource change on 2.28 and 2.22, never "no
  cost change" (BoF 2.10 Table 2.10 p54 (PDF 65): Labor Total = Hours x Rate).
- Techniques (PM 6.5.2.6 p215 (PDF 254)): negative float analysis; crashing, least incremental cost by adding
  resources, critical path only, may raise cost and risk; fast tracking, overlap, may cost rework,
  coordination, quality risk and money. Negative float analysis is "a helpful technique" for finding where
  the logic violates the date, not a compression technique itself. Also adjust durations "when more
  resources or less scope can be arranged", discretionary logic, or leads and lags (PM 6.5.2.2 p210
  (PDF 249)); less scope is a scope baseline change, so it goes through 3.3 like any other.
- Inputs: network (absent here), 2.13, the charter risk row whose response names a trigger date for the go-live (read the date there).
- Recorded in: 3.3 Schedule (Increase, Decrease, Modify, Description); 3.2; 2.18; the risk register for risks
  the compression creates (PM 6.6.3.5 p230 (PDF 269)). Formula: none.
- Wrong move: cutting an estimate to fit a date. Compression is done "without reducing the project scope" (PM
  6.5.2.6 p215 (PDF 254)) and chapter 6 names no technique that shrinks an estimate. A schedule modification
  may result in a change request (PM 6.5.3.5 p220 (PDF 259); 6.6.3.3 p229 (PDF 268)); making it the route
  when no compression closes the gap, a change request (3.3) to the sponsor, is the team rule.

**D9. Variance thresholds and the trigger for action.**
- When: set in 6.1, applied in 6.6 at each status date; trigger is a variance past a threshold.
- Techniques: thresholds as percentage deviations from baseline (PM 6.1.3.1 p182 (PDF 221)), or percent from
  baseline, float used, or any schedule reserve used, in bands acceptable, warning, unacceptable (BoF 2.1 p22
  (PDF 33)); earned value analysis, performance reviews, trend and variance analysis, critical path (PM 6.6.2
  p226 to 227 (PDF 265 to 266)).
- Inputs: baseline, work performance data; here the charter's "no milestone more than 1 week late", R8's date
  and the sponsor's authority to set limits. No activity or package level schedule threshold is recorded: ask
  the sponsor, do not reuse the cost band.
- Recorded in: 2.11 Variance Thresholds; 2.1 Schedule Variance Threshold, Schedule Baseline Management; 4.3
  Schedule Variance (Planned Result, Actual Result, Variance, Root Cause, Planned Response); 4.4.
- Formulas: SV = EV - PV and SPI = EV / PV; EV and PV in currency, SPI unitless, below 1.0 means less work done
  than planned (PM 7.4.2.2 p262 to 263 (PDF 301 to 302); BoF 4.4 p207 (PDF 218)). Earned schedule: SV = ES - AT,
  SPI = ES / AT, in time units (PM p233 (PDF 272)).
- Wrong move: acting on SPI alone; a delay off the critical path "may have little effect", a shorter one on a
  critical or near-critical activity "may require immediate action" (PM 6.6.2.1 p227 (PDF 266)).

**D10. Re-baselining, and escalating a forecast slip.**
- When: 6.6; trigger is a variance past the unacceptable threshold, a trigger date in a charter risk response, or elaboration that
  moves a baselined milestone.
- Techniques: corrective or preventive action; adjust leads and lags and compress the remaining work (PM 6.6.2.5
  to 6.6.2.6 p228 (PDF 267)); what-if scenarios (PM 6.6.2.1 p227 (PDF 266)); when delays are "so severe", a new
  target schedule (PM 6.6.3.5 p230 (PDF 269)). Trade-off: each compression carries its D8 cost. That a
  re-baseline loses the comparison with the old plan is an inference from the baseline being "a basis for
  comparison to actual results" (PM 6.5.3.1 p217 (PDF 256)), not a trade-off the book states.
- Inputs: the forecast, the baseline; the decider beyond the PM is the sponsor (charter Part 2A).
  Recorded in: 3.3 Schedule box and Disposition; 3.2 Decision Log; 2.18; 4.3. Formula: none.
- Wrong move: re-baselining to erase a variance. The baseline "can be changed only through formal change control
  procedures and is used as a basis for comparison to actual results" (PM 6.5.3.1 p217 (PDF 256)).
