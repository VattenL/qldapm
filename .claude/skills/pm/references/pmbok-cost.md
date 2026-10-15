# PMBOK 6 chapter 7, Project Cost Management, for the cost forms

Read this before filling 2.19 Cost Management Plan, 2.20 Activity Cost Estimates, 2.21 Cost Estimating Worksheet, 2.22 Cost
Baseline, 4.3 Variance Analysis or 4.4 Earned Value Analysis. The forms print the boxes; chapter 7 says what goes in them and
which technique names each decision. 4.3 also holds schedule (chapter 6) and quality (chapter 8, `pmbok-quality.md`) variance;
this note covers its Cost Variance section. 2.22 is a chart, so look at its blank page (PDF 105) too.

Cites: PMBOK as "7.2.2.6, 245 (PDF 284)" (section, printed page, PDF page); Book as "PDF 99 (printed 88)".

## Where it is

`PMBOK6_and_Agile_Practice_Guide.pdf`; PDF page = printed page + 39 in the Guide part (contents pages: chapter 7 at printed 231).

| Section | Printed page | PDF page |
| --- | --- | --- |
| 7 overview and Figure 7-1; key concepts, earned schedule, tailoring, agile | 231 to 234 | 270 to 273 |
| 7.1 Plan Cost Management; 7.1.3.1 cost management plan components | 235 to 239; 238 to 239 | 274 to 278; 277 to 278 |
| 7.2 Estimate Costs; techniques 7.2.2.2 to 7.2.2.5; 7.2.2.6 reserve analysis, cost of quality | 240 to 247; 244 to 245; 245 | 279 to 286; 283 to 284; 284 |
| 7.2.3.1 cost estimates, 7.2.3.2 basis of estimates | 246 to 247 | 285 to 286 |
| 7.3 Determine Budget; 7.3.2.3 management reserve, 7.3.2.5 funding limits | 248 to 256; 252 to 253 | 287 to 295; 291 to 292 |
| 7.3.3.1 cost baseline, Figures 7-8 and 7-9; 7.3.3.2 funding requirements | 254 to 255; 256 | 293 to 294; 295 |
| 7.4 Control Costs; EVA, variance, trend, forecasting, reserve analysis (7.4.2.2) | 257 to 270; 261 to 265 | 296 to 309; 300 to 304 |
| 7.4.2.3 TCPI and Table 7-1 (all EVM formulas); 7.4.3 outputs | 266 to 267; 268 to 270 | 305 to 306; 307 to 309 |
| Related 4.5.2.2 data analysis (root cause, variance, trend); 4.5.3.2 change requests | 111 to 112 | 150 to 151 |

Book (PDF = printed + 11), prose then blank: 2.19 PDF 93 to 94 (printed 82 to 83), PDF 95 (printed 84); 2.20 PDF 96 to 97 (printed 85
to 86), PDF 98 (printed 87); 2.21 PDF 99 to 101 (printed 88 to 90), PDF 102 to 103 (printed 91 to 92); 2.22 PDF 104 (printed 93),
PDF 105 (printed 94); 4.3 PDF 213 to 214 (printed 202 to 203), PDF 215 to 216 (printed 204 to 205); 4.4 PDF 217 to 218 (printed 206
to 207), PDF 219 (printed 208); 3.2 blank PDF 180 (printed 169); 3.3 PDF 181 to 182 (printed 170 to 171), blank PDF 183 to 185 (172 to 174).

`pdftotext -layout` interleaves a vertical watermark and a "PMI Member benefit" footer; drop those lines. The text prints
equations with an en dash; write an ASCII hyphen. "Chapter 7" here is PMBOK 6, not the course lecture numbering.

## Chapter 7 terms, with the book's meaning

- **Cost baseline** (7.3.3.1, 254, PDF 293): approved time-phased budget, with contingency reserves and without management
  reserves; changed only by formal change control; with EVM it is the performance measurement baseline, whose total is the BAC
  (7.4.2.2, 261, PDF 300). **Project budget** = baseline + management reserve (254, PDF 293); funding requirements likewise (256, PDF 295).
- **Contingency reserve** (7.2.2.6, 245, PDF 284): inside the baseline, for identified risks ("known-unknowns"). **Management
  reserve** (7.3.2.3, 252, PDF 291): outside the baseline, inside the budget, for unforeseen in-scope work ("unknown unknowns");
  using it adds it to the baseline through an approved change.
- **Control account** (7.1.3.1, 239, PDF 278): the WBS component used for cost accounting, with a code linked to the accounts.
- **Variance analysis** (7.4.2.2, 262, PDF 301): explains cause, impact and corrective actions of cost, schedule and at-completion
  variances. **Trend analysis** (263, PDF 302): performance over time, BAC against EAC. **Earned schedule** (233, PDF 272): optional.
- **AC** must be defined like PV and EV (direct hours only, direct costs only, or all costs); EV cannot exceed the PV authorised
  for a component (261, PDF 300).
- **Cost estimate** (241, PDF 280): a prediction from information known at the time; staff hours or days may replace currency.

## Mapping the process outputs onto the boxes

**7.1.3.1 onto 2.19** (238 to 239, PDF 277 to 278). Eight components, eight boxes in the same order (`fields/2.19.json`): Units
of Measure, Level of Precision (rounding, "US$995.59 to US$1,000"), Level of Accuracy (range, "±10%", may include contingencies),
Organizational Procedure Links (WBS, control account codes), Control Thresholds, Rules of Performance Measurement (measurement
points, EVM technique, EAC equations), Cost Reporting and Format, Additional Details (strategic funding, exchange-rate procedure,
cost recording procedure). No box: the Book's prose adds the estimating, time-phased budget and monitoring processes, level of
authority and funding limitations (PDF 93, printed 82). Name the three processes in the reading paragraph (7.2 to 7.4 feeding
2.20 to 2.22, 4.3, 4.4), put funding limits in Additional Details, cite the charter for authority. Table 2.17 says "Cost reporting
information and format"; the blank form's "Cost Reporting and Format" wins (PDF 94, printed 83).

**7.2.3 onto 2.20** (246 to 247, PDF 285 to 286; Table 2.18, PDF 97, printed 86). The blank form orders Method, Assumptions/
Constraints, Basis of Estimates, and prints "WBS ID" where Table 2.18 says "ID".

| PMBOK item | 2.20 column |
| --- | --- |
| Resource applied | Resource |
| Direct labor, outsourced resources | Labor Costs |
| Materials, equipment, supplies, services, facilities, IT | Physical Costs |
| Contingency for identified risks | Reserve (Estimate = labor + physical + reserve) |
| How developed | Method, Basis of Estimates |
| Assumptions made; known constraints | Assumptions/Constraints |
| Identified risks included in the estimate | No box; name the risk IDs in Assumptions/Constraints |
| Range (for example US$10,000 (±10%)); confidence level | Range; Confidence Level |
| Management reserve for unplanned work | No box, not in Estimate; it sits above the baseline |
| Indirect costs, financing, inflation, exchange rates | No column; the Book says add them if included (PDF 96, printed 85), else say so in Basis of Estimates |
| Updates to assumption log, lessons learned, risk register | No box; update those documents |

**2.21** holds the arithmetic behind Estimate, one table per technique (PDF 102 to 103, printed 91 to 92): Parametric, Analogous,
Three-Point (Optimistic, Most Likely, Pessimistic Cost, Weighting Equation, Expected Cost Estimate; PMBOK names them cO, cM, cP,
cE) and a bottom-up page (Labor Hours to Estimate, with Indirect Costs and Reserve, the answers to the unmapped 2.20 items). The
bottom-up page has no Resource box; take it from 2.20.

**7.3.3 onto 2.22.** The form prints only a sample S-curve (cumulative cost, periods 1 to 7; PDF 104, printed 93), no boxes. Keep a
table behind the curve: period, planned cost, cumulative. The curve is the cost baseline: activity estimates plus activity
contingency roll into work packages, then control accounts (Figure 7-8, 255, PDF 294); periods come from the schedule (7.3.1.2,
250, PDF 289), form 2.18. Contingency is inside the curve; management reserve and funding requirements sit above it (Book tip,
PDF 104, printed 93; Figure 7-9) and have no box, so give them the reading paragraph or a second series.

**4.3 and 4.4.** Variance analysis is cause, impact, corrective action (262, PDF 301). 4.3 Cost Variance (Planned Result, Actual
Result, Variance, Root Cause, Planned Response) takes cause into Root Cause and corrective or preventive action into Planned
Response; impact has no box in 4.3 (the Book's tip suggests a field for the implications of continued variance, PDF 213, printed 202;
4.4 has Schedule Impact and Budget Impact). 4.4 rows are the PV, EV, AC, SV, CV, SPI, CPI of Table 7-1 (267, PDF 306) plus the Book's percent rows and Overall Status.
VAC, ETC, the bottom-up EAC and the EAC at the budgeted rate have no row of their own. Writing them in "Selected EAC, Justification,
and Explanation" is the skill's house convention, not stated in the book, which only asks to choose a method, calculate it and justify it
(BoF 4.4 p207 (PDF 218)). Use the full printed row labels of `extract_form.py 4.4 --fields` (Planned value (PV), Earned value (EV), Actual
cost (AC), Schedule variance (SV), Cost variance (CV), Schedule performance index (SPI), Cost performance index (CPI), Percent planned,
Percent earned, Percent spent), never "PV, EV, AC" or "SV, CV". Leave the printed "Estimates at Completion (EAC)" header row empty. Table 4.4
has no row for BAC or Overall Status and the book gives no Overall Status scale (searched BoF 4.4, 206 to 207, PDF 217 to 218): state the wording the report uses, or leave it for the PM.
Root Cause of Schedule Variance, Root Cause of Cost Variance, Schedule Impact and Budget Impact need the team's judgement: leave each empty or `[TBD]` and ask. The Budget impact element asks for the impact on the budget, contingency
funds and reserves "and any intended actions to address the variance" (BoF Table 4.4 p207 (PDF 218)), which are the PM's and the sponsor's choice, so no forecast total, escalation decision or reserve effect is drafted into it, and a cause
written in a pending 3.3 is not this variance's cause until the team confirms it. A computed forecast goes only in a field the form prints for it: the two EAC rows, Selected EAC, Justification, and Explanation (with ETC and VAC), TCPI and the
percent rows; a percent overrun against a threshold has no field and stays in the reply. A proposed Budget Impact text, if asked for, goes in the reply outside the form block as a proposal. A negative claim carries the pages searched.
Ask which baseline the BAC and the charter's percent refer to: the book's BAC is the total planned value (PM 7.4.2.2 p261 (PDF 300)), the
cost baseline includes the contingency reserves of its work packages and excludes management reserves (PM 7.3.3.1 p254 (PDF 293)), so say
whether the contingency reserve is inside the BAC you used. Budgeted-rate EAC: say beside the figure that it accepts the
variance to date and assumes the rest is done at the budgeted rate, which PMBOK 6 allows after unfavorable performance only when risk
analysis supports it (PM 7.4.2.2 p265 (PDF 304)).

## Where this project's cost facts live

No document records an actual cost or a progress measure, so AC, EV and all of 4.3 and 4.4 stay empty or `[TBD]` until a source gives
them. List `docs/forms/` now, it is the truth (SKILL.md step 3).

| Fact | Where |
| --- | --- |
| The budget, its lines with their basis, the funding tranches and the milestones that release them, any statement that no further funding is committed | Charter `#### Preapproved financial resources`; form 1.1 page 3 |
| The reserve budget line: which reserve it is, whether it sits inside the baseline, which risks may draw on it and through what; whether any management reserve exists | Same table; `review-lessons.md` section 5; then the term search of `decisions.md` section 1 over every copy, because the Cost success criterion words it differently |
| Risks R1 to R12 | Charter `#### Overall project risk` |
| Cost criterion: the budget ceiling, the variance limit per stage gate, how reserve use is reported (the criterion may word the reserve differently from the budget line: report both wordings, `decisions.md` section 5) | Charter `#### Project objectives and related success criteria` |
| Authority: every limit of the block, with the ones the charter marks assumed | Charter `#### Assigned project manager, responsibility, and authority level` |
| Rates per hour for each resource code and the hours per person-month they are derived from | Scope package "Reading convention"; charter assumption 17 |
| Activity estimates (Resource, Labor Hours, Rate, Total, Material, Total Cost), 78 work packages; control accounts and codes | Scope package Part 3 sheets; Part 2 outline (CA marks); source for 2.20 and the 2.21 bottom-up page |
| Roll-up: control accounts, hours, labor, other cost and the reserve held at project level | Scope package Part 2 "Roll-up"; `python3 tools/check_scope.py` |
| Time phasing, levelled dates, milestones M0 to M7 | `docs/forms/2-18-project-schedule.en.md`, `python3 tools/level.py`; charter |
| A pending cost increase in a 3.3, and whether the reserve can cover it | `docs/forms/3-3-change-request.en.md` page 2, Cost; read the file, the figure changes |
| Precision, accuracy, range, confidence, EVM technique, report format and frequency | Not stated in any document read; ask, do not fill |

- Every dictionary sheet says its hours, money and dates are a first-pass estimate re-baselined at M1, while the totals are the
  charter's (scope package Part 3 preamble). A 2.20 row built from a sheet is a first-pass bottom-up figure: give it no high
  confidence and do not call it definitive (accuracy rises as the project progresses, 7.2, 241, PDF 280).
- With no management reserve, baseline and budget coincide. This is inferred from line 6 ("inside the cost
  baseline") and the absence of another reserve; say so once.
- A pending change request changes nothing. Build from the baselined charter and scope package and name which rows 3.3 would change
  (line 1, the total, the tranches tied to M3, M4 and M6).

## Traps

- **Spend is not performance.** Spending without the value of work done "has little value" (7.4, 259, PDF 298). Table 4.3 compares planned
  costs with actual costs expended (PDF 214, printed 203); the PMBOK cost variance is CV = EV - AC. Without formal EVA the plain comparison
  is accepted (262, PDF 301); say in the reading paragraph which one the form uses.
- **SPI is not a date.** It covers all work; analyse the critical path too (263, PDF 302). SV ends at zero at completion (262, PDF 301).
- **Cumulative, not period.** EAC uses cumulative CPI and SPI (265, PDF 304); use the cumulative column of 4.4.
- **4.4 prints two EAC rows and one TCPI row**, Table 4.4 gives two TCPI formulas (PDF 218, printed 207); say which basis the row uses. The budgeted-rate and a bottom-up EAC have no printed row on the blank form (PDF 219, printed 208): put the figure and the reason in Selected EAC, Justification, and Explanation.
- **A TCPI toward the EAC of the present CPI equals the CPI, and toward the budgeted-rate EAC it is 1**, because each EAC assumes exactly that efficiency (outside arithmetic from the formulas on PDF 305, printed 266, not a sentence of the book): it measures the forecast, not the effort left against the BAC. Quote the Table 7-1 words (harder, same, easier to complete) for the TCPI toward the BAC; `pm_calc.py evm` leaves the words off those two rows and says why.
- **Garbled print.** The Book shows "cE = ( cO + c4M + cP ) /6" (PDF 100, printed 89); use the PMBOK form (245, PDF 284). Percent planned,
  earned and spent are Book formulas (PDF 218, printed 207), not PMBOK text.
- **Contingency, never "management reserve"** for line 6 (`house-style.md`), though 7.2.3.1 (246, PDF 285) lets estimates carry both. The charter's Cost success criterion still words the report as "management reserve use reported monthly" (charter form 2B). Before writing that the budget line and the success criterion agree, or that a document names no management reserve, run `grep -n -i "management reserve\|contingency reserve" docs/*.md docs/forms/*.md` (variants from the `house-style.md` table), quote each hit with file and line, and report a mismatch as a source error for the sponsor; never smooth it over, and never decide from one read (`decisions.md` section 1).
- **Agile paragraph is no licence to cut estimates.** Under a strict budget it adjusts scope and schedule (234, PDF 273), and this
  project is predictive.
- **Reserve in Estimate.** 2.20's Estimate includes reserve (Table 2.18); the charter holds the reserve at project level, so show
  it as its own line, as the scope package roll-up does.

## Formulas

Variables: cO, cM, cP optimistic, most likely, pessimistic cost; cE expected cost; PV, EV, AC, BAC, EAC, ETC, VAC, CV, SV in the plan's
currency (VND here); CPI, SPI, TCPI ratios; ES earned schedule, AT actual time.

| Formula | Source |
| --- | --- |
| Triangular cE = (cO + cM + cP) / 3; beta cE = (cO + 4cM + cP) / 6 | 7.2.2.5, 245 (PDF 284); beta also form 2.21, PDF 99 (printed 88) |
| Parametric: Cost Estimate = Number of Units x Cost per Unit | form 2.21 Table 2.19, PDF 100 (printed 89) |
| Analogous: Multiplier = Current Activity / Previous Activity; Cost Estimate = Previous Cost x Multiplier | same; PMBOK gives no equation |
| Bottom-up: Total Labor = Labor Hours x Labor Rate; Estimate = Total Labor + Material + Supplies + Equipment + Travel + Other Direct Costs + Indirect Costs + Reserve | form 2.21 Table 2.20, PDF 101 (printed 90) |
| CV = EV - AC; SV = EV - PV; VAC = BAC - EAC | 7.4.2.2, 262 (PDF 301); Table 7-1, 267 (PDF 306) |
| CPI = EV/AC; SPI = EV/PV | 7.4.2.2, 263 (PDF 302) |
| EAC = AC + Bottom-up ETC | 7.4.2.2, 264 (PDF 303) |
| EAC = AC + (BAC - EV), future work at the budgeted rate | 7.4.2.2, 265 (PDF 304) |
| EAC = BAC / CPI, future work at the present cumulative CPI | 7.4.2.2, 265 (PDF 304) |
| EAC = AC + [(BAC - EV) / (CPI x SPI)], schedule also drives the work | 7.4.2.2, 265 (PDF 304) |
| ETC = EAC - AC, or ETC = Reestimate | Table 7-1, 267 (PDF 306) |
| TCPI = (BAC - EV) / (BAC - AC) to meet BAC; TCPI = (BAC - EV) / (EAC - AC) to meet the approved EAC | 7.4.2.3, 266 (PDF 305) |
| Percent planned = PV/BAC; percent earned = EV/BAC; percent spent = AC/BAC | form 4.4 Table 4.4, PDF 218 (printed 207) |
| Earned schedule: SV(t) = ES - AT; SPI(t) = ES/AT | 233 (PDF 272) |

Reading (Table 7-1, 267, PDF 306): CV, VAC, SV above zero and CPI, SPI above 1.0 are favorable; TCPI above 1.0 means harder to complete.
CPI/SPI weighting such as 80/20 or 50/50 is judgment (265, PDF 304). No number is given at which a TCPI is unreachable: it is "a
judgment call based on risk, time remaining in the project, and technical performance" (266, PDF 305).

## Decisions in this area

Team rule for all of them: a remedy is a technique PMBOK 6 or the Book names, with its trade-off; an estimate is never cut to fit a date
or a fund; when constraints cannot all hold, the route is a change request (form 3.3, PDF 183 to 185, printed 172 to 174) to the sponsor,
with the decision in the Decision Log (3.2: ID, Category, Decision, Responsible Party, Date, Comments). Say it in words whenever a recovery or a
response needs money or time beyond the baseline: this is a change request (3.3) to the sponsor (analysis of project performance may result in a change request to the cost and schedule baselines, 7.4.3.3, 269, PDF 308;
a response to a risk, 11.5.3.1, 447, PDF 486), and trimming or cutting estimates to absorb it is not a technique in the book (searched 7.4.2, 260 to 268, PDF 299 to 307; 6.5.2, 209 to 216, PDF 248 to 255; 6.6.2, 226 to 228, PDF 265 to 267).

### D1 Estimating technique per work package, and the three-point equation
- **When:** Estimate Costs (7.2), at planning and whenever scope or assumptions change.
- **Techniques:** analogous, a previous project's scope, cost, size; a high-level estimate when detail is missing (PDF 99, printed 88).
  Parametric, "higher levels of accuracy depending on the sophistication and underlying data" (7.2.2.3, 244, PDF 283). Bottom-up, every
  work package in detail then rolled up, called the most accurate (PDF 99, printed 88), its accuracy depends on item size (7.2.2.4, 244,
  PDF 283); its effort is not stated in the book. Analogous and parametric are reliable only with accurate history, quantifiable
  parameters, scalable models (7.3.2.4, 253, PDF 292). Three-point adds uncertainty and risk and yields a range (7.2.2.5, 244, PDF 283);
  triangular versus beta depends on the assumed distribution (245, PDF 284), no other criterion stated. Voting engages the team
  (7.2.2.8, 246, PDF 285).
- **Inputs:** scope package Parts 2 and 3, form 2.18, R1 to R12; no history of an earlier project was found in `docs/`.
- **Records:** 2.20 Method, Basis of Estimates; 2.21 table of the technique; Weighting Equation box.
- **Formula:** three-point, parametric, analogous, bottom-up rows above.
- **Wrong move:** a single-point figure for an uncertain item; the book says single points improve by considering uncertainty and risk
  (244, PDF 283). Analogous or parametric with no sound history fails the 7.3.2.4 condition.

### D2 Level of precision, level of accuracy, range per estimate
- **When:** Plan Cost Management (7.1); revisited as estimates are refined.
- **Techniques:** precision follows "scope of the activities and magnitude of the project", accuracy is the acceptable range (238, PDF 277).
  The book's examples are -25% to +75% at initiation and -5% to +10% later (241, PDF 280); rolling wave with accuracy per period
  (PDF 94, printed 83; tip PDF 97, printed 86). The cost of a tighter range is not stated in the book.
- **Inputs:** charter re-estimate point at M1; no document states the project's precision or accuracy, so ask.
- **Records:** 2.19 Level of Precision, Level of Accuracy; 2.20 Range, Confidence Level.
- **Formula:** none; a range is written "US$10,000 (±10%)" (247, PDF 286).
- **Wrong move:** presenting a first-pass figure as definitive; estimates "should be reviewed and refined" (241, PDF 280). The book's example
  percentages are not the project's thresholds.

### D3 Size and level of the contingency reserve
- **When:** Estimate Costs reserve analysis (7.2.2.6, 245, PDF 284); Determine Budget.
- **Techniques:** a percentage of the estimate, a fixed number, or quantitative analysis methods, at any level from activity to project;
  covers identified risks only; may be used, reduced or eliminated as information improves. No selection criterion or percentage is
  stated. Quantitative risk analysis can report the "amount of contingency reserve needed to provide a specified level of confidence"
  (11.4.3.1, 436, PDF 475), with no method for reaching a figure given there.
- **Inputs:** the risks the charter lists (charter 2A); the reserve budget line and its share of the budget.
- **Records:** 2.20 Reserve; 2.21 bottom-up Reserve; inside the 2.22 curve; 2.19 Level of Accuracy if it includes contingencies.
- **Formula:** none in the book; the link from R1 to R12 to the amount is not yet written down.
- **Wrong move:** hiding contingency in padded estimates; it "should be clearly identified in cost documentation" (245, PDF 284). A reserve
  asserted without risk linkage is the reviewers' warning in `review-lessons.md` section 5.

### D4 Whether to hold a management reserve, and the draw on the funds beyond the baseline
- **When:** Determine Budget (7.3.2.3, 252, PDF 291); that the sponsor decides is the charter's authority rule, not stated in PMBOK 6.
- **Techniques:** withhold an amount outside the baseline for unforeseen in-scope work; it stays in the budget and funding requirements and
  each use needs an approved change to the baseline (252, PDF 291; 254, PDF 293). The cost of holding it is not stated in the book.
- **Inputs:** charter budget table (none held), sponsor authority (2A).
- **Records:** 3.2 for the sponsor's decision; 3.3 for each use; amount above the 2.22 curve; charter budget.
- **Formula:** project budget = cost baseline + management reserve (254, PDF 293).
- **Wrong move:** calling the contingency reserve a management reserve, or drawing a reserve without a change; the baseline moves only by formal
  change control (254, PDF 293).

### D5 Estimates and funds disagree, or funds arrive in steps
- **When:** Determine Budget, and whenever estimates or the schedule move.
- **Techniques:** funding limit reconciliation, reschedule work to level expenditure by imposing date constraints (7.3.2.5, 253, PDF 292),
  trade-off moved dates. Alternatives analysis of make, buy, rent, lease across cost, schedule, resource, quality (245, PDF 284). Reserve
  analysis (D3, D4). Otherwise a change request, since only Perform Integrated Change Control raises the budget (259, PDF 298; 7.4.3.3, 269,
  PDF 308). Influence on cost is greatest early, so define scope early (231, PDF 270). Cutting the estimate is not a technique.
- **Inputs:** charter funding table and tranches; 2.22 curve; 2.18; pending 3-3.
- **Records:** 2.19 Additional Details; 3.3 (Category Cost, Schedule; Impacts of Change; Project Documents); 3.2.
- **Formula:** none.
- **Wrong move:** fitting estimates to the fund; an estimate is a prediction from known information (241, PDF 280).

### D6 Make, buy, lease, funding source, and spend on quality
- **When:** Plan Cost Management (7.1.2.2, 238, PDF 277) and Estimate Costs (cost of quality, 245, PDF 284).
- **Techniques:** self-funding, equity, debt; make, purchase, rent, lease (238, PDF 277). Weigh extra conformance spend against the cost of
  nonconformance, and short-term savings against later problems (245, PDF 284); 8.1.2.3 in `pmbok-quality.md`. Per-option trade-offs are
  not stated beyond these impacts.
- **Inputs:** charter line 2 and project exclusions (cloud, gateway, store accounts); assurance work packages (1.2.2, 1.3.2, 1.4.3, 1.5.5, 1.6).
- **Records:** 2.19 Additional Details; 2.20 Assumptions/Constraints, Basis of Estimates; 3.2.
- **Formula:** none.
- **Wrong move:** pricing only the purchase or cutting reviews to save cost; limiting design reviews cuts project cost but can raise the
  product's operating cost (233, PDF 272).

### D7 Control thresholds, measurement points, EVM technique, reporting
- **When:** Plan Cost Management; changed only by change request (7.4.3.4, 269, PDF 308).
- **Techniques:** thresholds as percent deviation from baseline (PDF 94, printed 83); measure at work package or control account; weighted
  milestones, fixed-formula, percent complete (239, PDF 278), and level of effort (tip, PDF 93, printed 82); trade-offs between them are not
  stated. Acceptable variance shrinks as work is done (262, PDF 301). Without EVM, delete that field (tip, PDF 93, printed 82).
- **Inputs:** charter Cost criterion and authority limits; control accounts; weekly status 1.1.1.3.
- **Records:** 2.19 Control Thresholds, Rules of Performance Measurement, Cost Reporting and Format.
- **Formula:** the EAC equations chosen are written in Rules of Performance Measurement (239, PDF 278).
- **Wrong move:** a threshold with no action; it is the variation allowed "before some action needs to be taken" (239, PDF 278).

### D8 Draw on, or release, the contingency reserve
- **When:** Control Costs reserve analysis (7.4.2.2, 265, PDF 304); trigger: an identified risk occurs and its response costs money, or its
  window ends without the event.
- **Techniques:** use for risk responses as planned; add savings from captured opportunities to contingency or take them out as margin;
  remove unused contingency; request more when analysis shows a need (265, PDF 304); no trade-off stated. Charter escalation: reserve use
  above the reserve limit the charter gives goes to the sponsor.
- **Inputs:** risk register; the reserve balance; charter authority.
- **Records:** 3.3 per draw (charter: through change control), 3.2; 4.4 Budget Impact (PDF 218, printed 207); update 2.32 when variance crosses
  or may cross the threshold (7.4.3.5, 270, PDF 309).
- **Formula:** none for the balance in the book.
- **Wrong move:** spending contingency on work no identified risk covers; it is for identified risks (245, PDF 284), unforeseen work belongs
  to management reserve (252, PDF 291).

### D9 Responding to a cost variance
- **When:** Control Costs, each period and stage gate, when CV or CPI crosses the 2.19 threshold.
- **Techniques:** root cause analysis (4.5.2.2, 111, PDF 150); corrective action, preventive action or defect repair (4.5.3.2, 112, PDF 151),
  chosen by alternatives or cost-benefit analysis (111, PDF 150). If variance is too severe, a change request revises the cost baseline "to
  provide a realistic basis for performance measurement" (269, PDF 308). Negative CV is often hard to recover (262, PDF 301). Relative cost of
  the options is not stated (searched 4.5.2, 111, PDF 150; 4.5.3, 112, PDF 151; 7.4.2.2, 262 to 267, PDF 301 to 306).
- **Inputs:** 4.4 figures, risk register, status reports; none recorded yet.
- **Records:** 4.3 Cost Variance; 4.4 Root Cause of Cost Variance, Budget Impact; 3.3 and 3.2 when a baseline changes.
- **Formula:** CV = EV - AC; CPI = EV/AC; VAC = BAC - EAC.
- **Wrong move:** letting unapproved change into reported cost; cost control prevents it (259, PDF 298).

### D10 Which EAC to report, and when the BAC is no longer viable
- **When:** Control Costs forecasting, each period (7.4.2.2, 263, PDF 302).
- **Techniques:** bottom-up EAC, the most common (264, PDF 303); EAC at the budgeted rate, which accepts performance to date and assumes
  improvement "only when supported by project risk analysis"; at the present CPI, if experience continues; with CPI and SPI, most useful when
  the schedule drives the remaining effort (265, PDF 304). Compare calculated EACs with the bottom-up one as a validity check (239, PDF 278).
  If the BAC is not viable, consider the forecasted EAC, which once approved may replace BAC in TCPI (266, PDF 305).
- **Inputs:** cumulative PV, EV, AC (none yet); BAC.
- **Reply wording and layout.** Quote the Table 7-1 phrases as `pm_calc.py evm` prints them (over planned cost, behind schedule, harder to complete); "over budget" is not the
  book's status word (267, PDF 306). With cumulative figures only, fill the Current Period Cumulative column of 4.4 and leave Current Reporting Period and Past Period
  Cumulative empty, and say so (BoF 4.4 p207 (PDF 218); the blank form prints the three columns, PDF 219 (printed 208)). 4.4 prints no ETC or VAC row, so state them
  inside the Selected EAC, Justification, and Explanation cell with their formulas (ETC = EAC - AC, VAC = BAC - EAC, 262 to 265, PDF 301 to 304), not in a row of their own.
  Percent overrun against a threshold is an outside arithmetic aid and is not stated in the book (BoF 4.3 p203 (PDF 214)); name its base.
- **Records:** 4.4 EAC rows, Selected EAC, Justification, and Explanation, TCPI; forecast to stakeholders (7.4.3.2, 269, PDF 308); escalate
  a forecast overrun above the charter's percent.
- **Formula:** the EAC, ETC and TCPI rows above.
- **Wrong move:** assuming recovery without support (265, PDF 304); TCPI above 1.0 means harder (267, PDF 306). Writing the forecast into Budget Impact or Root Cause instead of the EAC rows (see 4.3 and 4.4 above).
