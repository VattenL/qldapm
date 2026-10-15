# Decision catalog: from a project situation to the book's technique, forms and escalation

Read this when the user asks what to do, not which form to fill: "R5 happened", "we are two weeks late", "the client wants a new function",
"should we buy or build", "which form do I fill for X". It routes the request to a decision, and each decision lists the options PMBOK 6 or the
Book of Forms names with the trade-off the book states, the inputs, the calculator, the forms to write and who decides. It is built from the
Decisions sections of `pmbok-<area>.md`, the `knowledge/<form>.json` files and `book-structure.md`; open the note named in each heading for the
full entry, the project facts and the wrong move. The file has long lines and does not fit one Read: read it in parts with offset and limit, section 1,
the routing row, then only the D entries the row names; sections 4 and 5 when the answer moves a baseline or is written up.

**Citations.** `PM 6.5.2.6 p215 (PDF 254)` is PMBOK 6, section, printed page, PDF page (PDF = printed + 39). `APG 5.2.1 p51 (PDF 861)` is the
Agile Practice Guide in the same file (PDF = printed + 810). `BoF 3.3 p170 (PDF 181)` is the Book of Forms (PDF = printed + 11). A bare form
number in a Read, Write or Record cell is a pointer; its pages are in `forms-index.md` and the `citation` field of `knowledge/<form>.json`.
"Not stated in the book" means the book gives no value or criterion: the team decides and writes the reason in 3.2, never presented as the book's.

## 1. How to use it

1. **Restate the situation in one line** and find its row in section 2. A request that fits no row: use the closest decision, say so, and give
   the answer from the PMBOK area note rather than inventing a row.
2. **Read the entry** (section 3). Restate each fact the user gives (date, milestone, owner, amount) and check it against the documents; a mismatch is
   the first open question. Ask the user for each missing input before recommending; do not fill a threshold, a score, an owner or a rate
   from memory. If you cannot ask, list the questions first and give a conditional answer ("if EV is X, then Y"), never one figure built on an assumed
   input, and label every assumed value. When an input of a measure is missing, name it before anything else: SV and SPI need EV and PV of the item,
   CV and CPI need EV and AC, a forecast needs BAC as well (PM 7.4.2.2 p262 to 265 (PDF 301 to 304)). Write "PV and EV for <item> are needed to state SV and SPI",
   run no `evm`, and show no figure; the slip in days or weeks the user states is not PV or EV. Project facts (authority limits, thresholds, IDs, amounts) are read from `docs/` and the charter at the time, not copied here.
3. **Run the calculator** when the entry names one: `python3 .claude/skills/pm/scripts/pm_calc.py <subcommand> --help` (subcommands `evm`, `pert`,
   `effort-to-duration`, `analogous`, `bottom-up`, `risk-score`, `emv`, `weighted-score`, `comms-channels`, `earned-schedule`, `cpm`, `crash`, `velocity`, `cd3`,
   `reserve`, `funding`, `response-effectiveness`, `payback`; examples in the script docstring; a test keeps this list equal to `pm_calc.py --help`).
   Report inputs, formula name and result. `comms-channels`, `payback`, `cpm`, `reserve` and `funding` compute what a book names or draws but gives no
   equation for, so label them outside arithmetic aids; `response-effectiveness` computes the ratio PMBOK 6 prints in words (PM 11.5.2.8 p446 (PDF 485));
   `velocity` and `cd3` compute the Agile Practice Guide's printed definitions. Report an index as the tool prints it (four decimals), money in whole currency units, and compare a threshold on the
   unrounded figure; a two-decimal CPI of 0.8621 shown as 0.86 flatters the status, and no book states a rounding rule. A percent of BAC or of
   another base is an outside arithmetic aid, "not stated in the book" (form 4.3, PDF 214 (printed 203)): say so, and say which base it is taken of.
4. **Check the baselines.** If an option moves scope, schedule, cost, quality or a plan, it is a change: follow section 4 and say so.
5. **Present** in the shape of section 5, then offer to update the forms. Write the forms only when asked.

**Rules for every entry (team rules, not book text).** A remedy is a technique PMBOK 6 or the Book of Forms names, with its trade-off. An
estimate is never cut to fit a date or a fund: no chapter names that technique. When scope, schedule, cost and quality cannot all hold, the route
is a change request (3.3) to the sponsor. Decisions are logged in 3.2 (below). Anything beyond the project manager's authority in the charter
goes to the sponsor.

**Authority limits to read from 1.1.** D14, D15, D16, D17, D18, D26 and D30 point here. Read each limit from the charter's authority section at the time; none is a book
value and none is copied into this file. (1) The limit per single transaction. (2) The limit per reserve use, kept apart from (1). (3) The forecast overrun percent above
which the project manager escalates to the sponsor, and its base. (4) The limit on a change in total funding, scope or a milestone. (5) Which reserve the budget line names
(a contingency reserve inside the cost baseline, PM 7.2.2.6 p245 (PDF 284), or a management reserve outside it, PM 7.3.2.3 p252 (PDF 291)), which risks (IDs) may draw on it
and who approves each draw. (6) Whether every draw is a 3.3. Quote the charter's own words, say which limits the charter marks as assumed, and when it is silent ask the
sponsor and record the answer in 3.2. When the charter gives fewer distinct limits than the six points, list the limits it gives, write "not given in the
charter" against each point it does not give, ask the sponsor for those points, and never invent a split or let one limit stand for two points. In the answer list every limit of the block with the value read from the charter and whether the decision touches it,
so the sponsor sees the forecast overrun percent (3) beside the reserve limit (2) even when the question concerns only one of them; never cite only the limit that fits.

**A threshold whose base is not defined.** When the charter gives a percent "of baseline" and no word on which baseline, do not pick one: test every candidate (BAC,
planned value to date, the approved funding) and report each, or ask the sponsor which one it means. The percent is an outside arithmetic aid, "not stated in the book"
(form 4.3, PDF 214 (printed 203)). `pm_calc.py evm --threshold <percent> --base bac pv` prints the overrun against each base and marks it within or beyond.

**Worked mappings.**
- "R5 happened": rows 1 and 22. Is it an issue now (3.1)? Is the planned response triggered (D37)? Does the event break an assumption in 1.2 (D02)? Does it draw
  reserve (D18)? Who pays when a seller's price rose (D41, "Who pays")? Does the response move a baseline (D05)? Does it escalate (D30)? Then update 2.32 (the entry stays in the register: Status stays open while the response is carried
  out, Actions and Comments say it occurred and point to the 3.1 entry; D37), 3.1, 3.2 and, if lessons, 3.5.
- "We are two weeks late": rows 6 and 7. Check the stated slip against 2.10 and 2.18, measure (D15 with `evm`), test it against threshold and float (D14 step 0), read 2.18 and any 3.3 for compression already used, then D14 and D13 for the options; the answer
  is never a shorter estimate.
- "The client wants a new function": row 9. D07 decides reorder or change request, D05 classifies, D06 decides; the sponsor signs 3.3.

## 2. Routing table

PM column: section, printed page, PDF page of the process start. Forms: Read = forms to consult, Write = the main forms the decision updates, Also record = every other
form on the Record line of the row's decisions (a test keeps this column equal to the Record lines, so a form is not forgotten when the table is read alone).
Impact anchor = the form or forms to run `form_graph.py --impact <form> --depth 1` on for this row (the count line differs by form, so quote the anchor's own: 2.18 and 3.3
do not give the same count); a row that moves a baseline adds 3.3, and then the 3.3 run is quoted as well, with its "provides it" and recipient edges (2.2, 3.4, the change
control board) even when that form is not in `docs/`. Name every form the run prints, none dropped and none added.

| # | Situation or question | Decision | Read | Write | Technique | PMBOK | Also record | Impact anchor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A listed risk occurred ("R5 happened") | D37, D18, D05, D30, D02 | 2.32, 2.36, 2.31, 2.33, 1.2 | 3.1, 2.32, 3.2; 3.3 if baseline | contingency or fallback plan, reserve analysis, assumption check in 1.2 | 11.6 p449 (PDF 488), 11.7 p453 (PDF 492), 4.1 p75 (PDF 114) | 1.2, 2.30, 2.31, 2.33, 2.36, 3.4, 4.2, 4.4, 4.5 | 2.32, 3.3 |
| 2 | New risk found; which risks first; how to score | D34 | 2.31, 2.32 | 2.32, 2.34, 2.35 | probability and impact, `risk-score` | 11.2 p409 (PDF 448), 11.3 p419 (PDF 458) | 2.31, 3.2 | 2.32 |
| 3 | Is quantitative risk analysis worth it | D35 | 2.31, 2.32 | 2.31, 2.33 | simulation, sensitivity, decision tree, `emv` | 11.4 p428 (PDF 467) | 3.2 | 2.32 |
| 4 | Pick a response for a risk or for overall risk | D36 | 2.32, 2.31, 2.35 | 2.32, 2.36, 2.33 | avoid, transfer, mitigate, accept, escalate; exploit, share, enhance; `response-effectiveness` | 11.5 p437 (PDF 476), 11.5.3.1 p447 (PDF 486) | 3.3 | 2.32, 3.3 |
| 5 | Reserve too small, or how big should it be | D17 | 2.22, 2.32, 2.20 | 2.20, 2.22, 2.31, 3.2 | reserve analysis, `reserve` | 7.2 p240 (PDF 279), 7.3 p248 (PDF 287) | 2.21, 2.36 | 2.22, 3.3 |
| 6 | We are N weeks late; forecast slip; milestone at risk | D15, D14, D13 | 2.18, 2.10, 2.11, 2.14, 4.3, 4.4 | 3.3, 3.2, 4.2, 4.3 | absorb check against threshold and float first (D14 step 0), compression already used, negative float, crashing, fast tracking, resource leveling or smoothing (D13), `evm`, `cpm` | 6.5 p205 (PDF 244), 6.6 p222 (PDF 261) | 2.18, 2.22, 2.28, 2.32, 4.1, 4.4 | 2.18, 2.22, 3.3 |
| 7 | Over budget; CPI or SPI below 1; what will it cost | D15, D16 | 2.19, 2.22, 4.4 | 4.3, 4.4, 4.2; 3.3 if baseline | variance analysis, EAC variants, TCPI, `evm` | 7.4 p257 (PDF 296), 4.5 p105 (PDF 144) | 4.1 | 2.22, 4.4, 3.3 |
| 8 | Draw on or release contingency | D18 | 2.33, 2.32, 2.22 | 3.3, 3.2, 4.2, 2.33 | reserve analysis, `reserve` | 7.4 p257 (PDF 296), 11.7 p453 (PDF 492) | 2.32, 4.4 | 2.33, 2.22, 3.3 |
| 9 | The client wants a new function or a change | D07, D05, D06 | 2.5, 2.6, 2.7, 2.8 to 2.10, 2.2 | 3.3, 3.4, 3.2 | alternatives analysis, cost-benefit, voting; change path of section 4, steps 1 to 8 | 5.6 p167 (PDF 206), 4.6 p113 (PDF 152) | 2.6, 6.2 | 3.3, 2.7, 2.8 to 2.10 (together) |
| 10 | Reorder the backlog; what enters the iteration | D07, D12 | 6.2, 6.3 | 6.2, 3.2 | value ranking, cost of delay over duration | APG 5.2.3 p52 (PDF 862), APG 5.2.6 p55 (PDF 865) | 2.6, 2.11, 2.12, 2.13, 2.14, 2.15, 3.3, 3.4, 6.3 | 6.2 |
| 11 | Is it a change or just an update; who approves | D05, D06 | 2.2, 3.3, 3.4 | 3.3, 3.4, 3.2 | change classification, CCB; change path of section 4, steps 1 to 8 | 4.6 p113 (PDF 152) | none | 3.3 |
| 12 | Deliverable ready; accept or refuse | D09 | 2.6, 2.7, 2.24, 3.6 | 4.9, 3.2, 3.6 | inspection, voting | 5.5 p163 (PDF 202), 8.3 p298 (PDF 337) | 3.3 | 4.9 |
| 13 | Defect or failed test; fix inside baseline or not | D24, D05 | 2.24, 3.6, 3.1 | 3.6, 3.1, 3.3 | root cause analysis, alternatives analysis | 8.2 p288 (PDF 327), 8.3 p298 (PDF 337) | 3.2, 3.4, 3.5 | 3.6, 3.3 |
| 14 | Who audits; how often | D23 | 2.23, 2.31, 2.37 | 3.6, 4.5, 4.7 | quality, risk, procurement audit | 8.2 p288 (PDF 327), 11.7 p453 (PDF 492), 12.3 p492 (PDF 531) | 2.23, 2.31, 3.2 | 2.23 |
| 15 | Quality standard, metric, test timing, sampling | D20, D21, D22 | 2.23, 2.24, 2.7 | 2.23, 2.24, 3.2 | cost of quality, test and inspection planning | 8.1 p277 (PDF 316) | 2.7, 2.20, 3.3 | 2.23 |
| 16 | A person leaves, is over-booked, or capacity is short | D26, D13 | 2.26, 2.28, 2.29, 2.18 | 3.3, 3.2, 3.1, 2.29 | acquisition, leveling vs smoothing | 9.3 p328 (PDF 367), 9.5 p345 (PDF 384), 6.5 p205 (PDF 244) | 2.18, 2.22, 2.26, 2.28, 2.32 | 2.28, 2.18, 3.3 |
| 17 | How many people; how long from effort | D11 | 2.16, 2.17, 2.28 | 2.17, 2.16, 2.28 | parametric, `effort-to-duration` | 6.4 p195 (PDF 234) | none | 2.17 |
| 18 | Estimate an activity or a cost; how wide a range | D10 | 2.17, 2.21, 2.19 | 2.16, 2.20, 2.17, 2.21 | analogous, parametric, three-point, bottom-up; calculators `pert`, `analogous`, `bottom-up` | 6.4 p195 (PDF 234), 7.2 p240 (PDF 279) | none | 2.17, 2.21 |
| 19 | Dependencies, lead or lag, iteration length, schedule detail | D12 | 2.11, 2.13, 2.15 | 2.11, 2.12, 2.13, 2.14 | precedence diagramming, rolling wave, time-boxing | 6.1 p179 (PDF 218), 6.3 p187 (PDF 226) | 2.15, 6.3 | 2.11 to 2.15 |
| 20 | Funds below estimates; make, buy or lease | D19 | 2.20, 2.22, 2.37 | 2.19, 3.3, 3.2 | funding limit reconciliation, make-or-buy, `funding`, `payback` | 7.3 p248 (PDF 287), 12.1 p466 (PDF 505) | 2.37 | 2.19, 2.22, 3.3 |
| 21 | Team conflict | D28 | 2.27, 3.1 | 3.1, 3.2, 2.27 | five conflict techniques | 9.5 p345 (PDF 384), 13.3 p523 (PDF 562) | 2.40 | 2.27 |
| 22 | Escalate this? to whom | D30 | 1.1, 2.30, 2.31 | 3.2, 2.32, 3.3 | escalation, authority levels | 11.5 p437 (PDF 476) | 2.30 | 2.32, 3.3 |
| 23 | Stakeholder new, silent or resisting | D31, D32 | 1.3, 1.4, 2.40 | 2.40, 1.3, 3.1 | engagement assessment matrix, root cause | 13.1 p507 (PDF 546), 13.4 p530 (PDF 569) | 1.4, 2.18, 2.30, 2.32, 3.5 | 2.40 |
| 24 | Who needs which report; how often; how many channels | D29 | 2.30, 1.3 | 2.30, 4.1, 4.2 | requirements analysis, push or pull, `comms-channels` | 10.1 p366 (PDF 405), 10.2 p379 (PDF 418) | none | 2.30 |
| 25 | Log, rank and assign an issue | D33 | 2.32, 3.1 | 3.1, 3.2 | priority and owner | 4.3 p90 (PDF 129) | 2.32, 3.5 | 3.1 |
| 26 | Make or buy; contract type | D19, D38 | 2.37, 2.38 | 2.38, 3.2 | make-or-buy, fixed price, cost-reimbursable, T&M | 12.1 p466 (PDF 505) | 2.19, 2.37, 3.3 | 2.38 |
| 27 | Which seller; weights; bid document; sole source | D39, D40 | 2.38, 2.39 | 2.39, 2.38, 3.2 | source selection, weighting, `weighted-score` | 12.1 p466 (PDF 505), 12.2 p482 (PDF 521) | 2.32, 2.37, 3.3 | 2.39 |
| 28 | Seller late, claim, amendment, payment | D41 | 4.6, 2.37, 3.4 | 4.6, 3.1, 3.3, 3.4 | performance review, claims administration | 12.3 p492 (PDF 531) | 2.37 | 4.6, 3.3 |
| 29 | Close a contract, phase or project; stop early | D42 | 1.1, 3.4, 3.1, 4.9 | 5.2, 5.1, 4.8, 3.5 | document, variance, trend analysis; early stop is documented, its criterion not stated in the book | 4.7 p121 (PDF 160) | 1.1, 3.2, 3.3, 4.9 | 5.2 |
| 30 | Lessons; retrospective | D43 | 3.5, 6.4 | 3.5, 6.4, 5.1 | knowledge vs information management | 4.4 p98 (PDF 137) | 3.2 | 3.5 |
| 31 | Approach (predictive, iterative, agile); which agile forms | D03 | 2.1, 2.3, 6.1 to 6.4 | 2.1, 2.3, 6.1, 3.2 | life cycle continuum, suitability filter | APG 3.1 p18 (PDF 828), APG X3 p125 (PDF 935) | 2.27 | 2.1 |
| 32 | An assumption failed or changed | D02 | 1.2, 2.32 | 1.2, 2.32; 3.3 if baseline | assumption and constraint analysis | 4.1 p75 (PDF 114), 11.2 p409 (PDF 448) | none | 1.2 |
| 33 | Baseline timing, thresholds, scope detail, WBS depth | D04, D08 | 2.1, 2.2, 2.4, 2.9 | 2.1, 2.11, 2.19, 2.9, 2.10 | variance threshold, decomposition | 4.2 p82 (PDF 121), 5.4 p156 (PDF 195) | 2.2, 2.4, 2.5, 2.6, 2.7, 2.8, 3.2 | 2.1, 2.11, 2.19 |
| 34 | Roles, RAM, team charter; training, assessment | D25, D27 | 2.25, 2.26, 2.27, 3.7 | 2.25, 2.26, 2.27, 3.7 | RAM, team building, performance assessment | 9.1 p312 (PDF 351), 9.4 p336 (PDF 375) | 2.29, 3.2, 3.5 | 2.26 |
| 35 | Charter changes or sponsor authority | D01 | 1.1 | 1.1, 3.3 | expert judgment | 4.1 p75 (PDF 114) | 3.2 | 1.1, 3.3 |
| 36 | Is the release date at risk on an agile project; velocity; ranking by delay | D15, D07 | 6.2, 6.3, 2.18 | 6.3, 6.2, 3.2; 3.3 if a milestone moves | velocity, burnup, cost of delay divided by duration, `velocity`, `cd3` | APG 5.4.1 p64 (PDF 874), APG Table 5-1 p59 (PDF 869) | 2.6, 3.4, 4.1, 4.2, 4.3, 4.4 | 6.3, 3.3 |
| 37 | A date is imposed before a schedule exists, or a milestone must move earlier | D14, D13 | 2.18, 2.14, 2.15, 2.11, 3.3 | 3.3, 3.2, 2.18, 2.14 | compare the date with the network finish and float first (D14 step 0), then crashing, fast tracking, resource leveling, then a request to the sponsor | 6.5.2.6 p215 (PDF 254), 6.5 p205 (PDF 244) | 2.22, 2.28, 2.32, 4.3 | 2.18, 2.14, 3.3 |
| 38 | A favourable variance: CPI or SPI above 1, ahead of schedule, unspent contingency | D15, D16, D18 | 2.19, 2.22, 2.33, 4.4 | 4.2, 4.3, 4.4, 3.2 | variance analysis, forecast before relying on it, reserve analysis, no baseline change without a 3.3 | 7.4 p257 (PDF 296), 4.6.3.2 p120 (PDF 159) | 2.32, 2.33, 3.3, 4.1 | 4.4 |
| 39 | Work or a deliverable differs from the scope baseline; do we need a revised baseline (scope, schedule or cost) | D05, D15 | 2.7, 2.8, 2.9, 2.10, 2.18, 2.22, 4.3 | 3.3, 3.4, 3.2 | variance analysis and trend analysis (Control Scope); a severe variance means a request to revise the baseline, never an absorbed change; change path of section 4, steps 1 to 8 | 5.6 p167 (PDF 206), 5.6.2.1 p170 (PDF 209), 5.6.3.3 p171 (PDF 210), 7.4.3.4 p269 (PDF 308), 6.6.3.5 p230 (PDF 269) | 4.1, 4.2, 4.3, 4.4 | 2.8 to 2.10 (together), 3.3 |
| 40 | Which form do I fill for X (a pointer, no decision) | none | forms-index.md, 1.1 to 6.4 as asked | none | `forms-index.md` and `form_graph.py <form>` for the form chosen | BoF 1.0 p1 (PDF 12), 2.0 p17 (PDF 28) | none | none: answer from `forms-index.md` and `form_graph.py <form>` of the chosen form only |

**Where this project keeps a form.** Read the project's own stand-in before a form of the table that no file in `docs/forms/` holds. 2.6 (rows 9, 12) is no form here: the
requirements are in the charter package, sections 1.1.4 Functions, 1.1.5 Exception and failure behaviour and 1.3 Product Acceptance Criteria, with the RTM 2.7 in the scope
package (`pmbok-scope.md`). 6.2 (rows 9, 10) applies only when the approach is adaptive (D03); for a predictive, baselined project the request goes to 3.3 and the backlog is not
the answer. 2.8 and 1.1 live in the charter package, 2.7, 2.9 and 2.10 in the scope package, and the other forms of the table are forms to create unless `docs/forms/` holds them.

**Which form do I fill for X (row 40).** Initiating forms 1.1 to 1.4 hold the charter, assumptions and stakeholders (BoF 1.0 p1 (PDF 12)). Planning forms 2.1
to 2.40 follow PMBOK chapter order 4 to 13 (BoF 2.0 p17 to 19 (PDF 28 to 30)): integration 2.1 to 2.3, scope 2.4 to 2.10, schedule 2.11 to 2.18, cost 2.19 to 2.22, quality
2.23 and 2.24, resources 2.25 to 2.29, communications 2.30, risk 2.31 to 2.36, procurement 2.37 to 2.39, stakeholders 2.40. Executing: issues 3.1,
decisions 3.2, change request 3.3, change log 3.4, lessons 3.5, quality audit 3.6, team assessment 3.7 (BoF 3.0 p163 to 164 (PDF 174 to 175)).
Monitoring and controlling: reports 4.1 and 4.2, variance 4.3, earned value 4.4, audits 4.5 and 4.7, contractor 4.6, closeout 4.8, acceptance
4.9 (BoF 4.0 p189 to 190 (PDF 200 to 201)). Closing 5.1 and 5.2 (BoF 5.0 p229 (PDF 240)). Agile 6.1 to 6.4 (BoF p239 (PDF 250)). "Use the forms you
need, to the degree that you need them" (BoF printed x (PDF 11)). Page ranges and printed titles: `forms-index.md`.

**Recording applies to every entry.** 3.2 Decision Log prints ID, Category, Decision, Responsible Party, Date, Comments; Comments carries the
alternatives considered, the reason and the impact (BoF 3.2 p168 (PDF 179); blank form p169 (PDF 180); Table 3.2 names the date column Priority, the
blank form wins). The book says it is not an explicit PMBOK document (BoF 3.2 p168 (PDF 179)). Responsible Party stays empty until a document names a person; a role a document has not filled (the charter's project manager "to be assigned") does not count,
and a risk response that says "name the Accountant" or "replacement" is a response, not an owner (house-style.md); Date is the team's. The ID follows the log's own order (the book prints no scheme). **Escalation ladder.** A change affecting only
performance against a baseline is usually the project manager's decision; one that moves a baseline needs the CCB if one exists and the customer or
sponsor (PM 4.6.1.4 p117 (PDF 156)). The responsible individual is named in the plan or by the organization, usually sponsor or project manager
(PM 4.6 p115 (PDF 154)). The charter's authority section (1.1) holds the project's limits; read it each time.

## 3. Decisions

Each entry: **Options** (technique, stated trade-off, citation), **Inputs and calc**, **Record**, **Escalate**.

### D01 Authorize the project and set the project manager's authority [integration D1]
- Options: initiation comes from an entity outside the project such as a sponsor, program, PMO or portfolio body, and the charter may be developed by the sponsor or the PM in collaboration with that entity (PM 4.1 p77 (PDF 116)); that it is the sponsor's decision, not the PM's, is the project's authority rule in the charter, not book text. Expert judgment, brainstorming, focus groups, interviews, facilitation, meetings (PM 4.1.2 p79 to 80 (PDF 118 to 119)); trade-offs not stated in the book. The charter formally authorizes the project (BoF 1.1 p2 (PDF 13)) but is no contract: no consideration or money is exchanged (PM 4.1 p77 (PDF 116)).
- Inputs and calc: business case, benefits plan, agreements, stakeholders' risk thresholds (PM 4.1.1 p77 to 78 (PDF 116 to 117)); the PM only recommends changes to business documents (PM p78 (PDF 117)). Calc: none.
- Record: 1.1 (Approvals, Project Manager Authority Level, Sponsor Authority, Preapproved Financial Resources); 3.2.
- Escalate: the sponsor owns it; a later change to the charter is a 3.3.

### D02 Which assumptions and constraints to record, and who validates them [integration D2; risk 3]
- Options: no technique named. Once validated an assumption stops being one (BoF 1.2 p9 (PDF 20)); the log exists to follow each one up (BoF 1.2 p10 (PDF 21)); new ones arise in Direct and Manage Project Work (PM 4.3 p97 (PDF 136)). Assumption and constraint analysis is also a risk identification technique (PM 11.2.2 p414 to 416 (PDF 453 to 455)). Trade-offs not stated in the book.
- Inputs and calc: business case, charter constraints, estimates. Calc: none.
- Record: 1.2 (Responsible Party, Due Date, Actions, Status); an unvalidated critical assumption also goes to 2.32.
- Escalate: a baseline change forced by a failed assumption is a 3.3.

### D03 Development approach, life cycle, and which agile forms to use [integration D3; agile 1, 2; schedule 1]
- Options: predictive (low uncertainty; value arrives at the end and change is costly, APG 3.1.1 p20 (PDF 830)), iterative (feedback improves unfinished work, may take longer, "optimized for learning rather than speed", APG 3.1.2 p21 (PDF 831)), incremental (usable subsets sooner, APG 3.1.3 p22 (PDF 832)), agile, hybrid (APG Table 3-1 p18 (PDF 828); APG 3.1.6 to 3.1.9 p26 to 28 (PDF 836 to 838)). Suitability filter: nine scored questions, a discussion tool and not an inclusion gate (APG X3 p125 to 138 (PDF 935 to 948)). Change rigor follows the approach (BoF 2.2 p25 (PDF 36)). 6.1 to 6.4 may replace the charter, requirements documentation, schedule management plan and lessons register (BoF p239 (PDF 250)); a vision carries no budget or authority, so it does not replace an approved charter (BoF 1.1 p2 (PDF 13)). Tailor after using the practice as designed (APG X2.2 p119 (PDF 929)); trial a change for an iteration or two (APG X2.3 p120 (PDF 930)). The stated trade-offs are those named above; a trade-off between agile and hybrid beyond the filter's discussion: not stated in the book.
- Inputs and calc: charter constraints, high-level description, risk register; filter scores come from the team. Calc: none.
- Record: 2.1 (Project Life Cycle, Development Approaches), 2.3, 6.1 when a product vision is written (it never replaces the charter), 2.27 Other Agreements, 3.2.
- Escalate: the team decides inside baselines; a change to milestones, scope or cost is a 3.3.

### D04 When to baseline, thresholds, what is under formal control, EVM technique [integration D4; cost 7; schedule 9]
- Options: the plan is baselined once at least scope, time and cost references are set (PM 4.2 p83 (PDF 122)); when exactly is not stated in the book, only that the kick-off is usually at the end of planning and start of executing, shortly after initiation on small projects, at the start of executing on large ones, at each phase on multiphase ones (PM 4.2.2.4 p86 (PDF 125)). Threshold as percent deviation from baseline (PM 6.1.3.1 p182 (PDF 221); BoF 2.19 p83 (PDF 94)), or bands acceptable, warning, unacceptable on percent, float used or schedule reserve used (BoF 2.1 p22 (PDF 33)); a threshold is "an agreed-upon amount of variation to be allowed before some action needs to be taken" (PM 7.1.3.1 p239 (PDF 278); same wording 6.1.3.1 p182 (PDF 221)). Progress measure: weighted milestones, fixed formula, percent complete (PM 7.1 p239 (PDF 278)), level of effort (BoF 2.19 p82 (PDF 93)); trade-offs among them not stated in the book. Allowed variance shrinks as work is done (PM 7.4.2.2 p262 (PDF 301)).
- Inputs and calc: subsidiary plans and baselines, stakeholders' risk thresholds (PM 4.1.1.3 p78 (PDF 117)); the project's thresholds come from the charter and sponsor, none is invented (do not reuse a cost band as a schedule threshold); if the base of a percent is undefined, follow "A threshold whose base is not defined" in section 1. Calc: `pm_calc.py evm` measures against them.
- Record: 2.1 (Variance Threshold, Baseline Management, Baselines), 2.2 Definitions of Change, 2.11 Variance Thresholds, 2.19 Control Thresholds and Rules of Performance Measurement.
- Escalate: once baselined, change only through 4.6 (PM 4.2 p83 (PDF 122)) and from the last baseline forward (PM 4.6.3.2 p120 (PDF 159)); a threshold change is a 3.3 (PM 7.4.3.4 p269 (PDF 308)).

### D05 Is it a change, and who approves it [integration D5; scope 8; stakeholder 7; quality 10; risk 11; communications D8]
- Options: types are corrective action, preventive action, defect repair, update (PM 4.3.3.4 p96 (PDF 135)); any stakeholder may ask (PM p96 (PDF 135)). Before baselines no formal control; after, every request (PM 4.6 p115 (PDF 154)). Performance-only effects are usually the PM's decision; baseline effects need the CCB and the customer or sponsor (PM 4.6.1.4 p117 (PDF 156)). The line between a change and a revision, update or progressive elaboration is the plan's (BoF 2.2 p25 to 26 (PDF 36 to 37)). Also requests: work found outside baselines (PM 6.2.3.4 p186 (PDF 225)), risk responses (PM 11.5.3.1 p447 (PDF 486)), quality repairs (PM 8.2.3.3 p296 (PDF 335)), engagement actions (PM 13.4 p535 (PDF 574)). Absorbing it is scope creep, defined as uncontrolled expansion of scope "without adjustments to time, cost, and resources" (PM 5.6 p168 (PDF 207)). Defect repair is a named change request type (PM 4.3.3.4 p96 (PDF 135)), and Manage Quality and Control Quality call for a request when a change impacts a plan component, document or process (PM 8.2.3.3 p296 (PDF 335); 8.3.3.4 p306 (PDF 345)). Whether a repair touching none of them needs its own request: not stated in the book (PM 8.3.1.3 p301 (PDF 340)); the team writes its rule in 3.2.
- Inputs and calc: baselines, 2.2, configuration management plan, basis of estimates, RTM, risk report (PM 4.6.1 p116 to 117 (PDF 155 to 156)); the charter's authority limits. Calc: `evm` for cost and schedule effect.
- Record: 3.3 (Category plus every touched category; Impacts of Change with Increase, Decrease or Modify; BoF 3.3 p170 to 171 (PDF 181 to 182)); 3.4; 3.2.
- Escalate: anything beyond the PM's authority, or any constraint conflict, is a 3.3 to the sponsor.

### D06 Approve, defer or reject a change request [integration D6]
- Options: alternatives analysis (accept, reject or modify) and cost-benefit analysis (worth its cost) (PM 4.6.2.3 p119 (PDF 158)); voting: unanimity, majority (more than 50 percent, an odd group avoids ties), plurality (largest block, for more than two options) (PM 5.2.2.4 p144 (PDF 183)); autocratic, one person responsible (PM 4.6.2.4 p119 (PDF 158)); multicriteria decision analysis, weighted criteria give each alternative a score and rank (PM 8.1.2.4 p283 (PDF 322)). Which fits when: not stated in the book. The CCB assesses impact on time, cost, resources and risk and may propose alternatives (PM 4.6.2.5 p120 (PDF 159)); customer or sponsor approval may follow (PM 4.6 p115 (PDF 154)).
- Inputs and calc: request with cost, dates, resources, risks (PM 4.6.1.4 p117 (PDF 156)); work performance reports (PM 4.6.1.3 p117 (PDF 156)). Calc: `weighted-score` for a multicriteria matrix.
- Record: 3.3 Disposition (Approve, Defer, Reject) and Justification (BoF 3.3 p174 (PDF 185)); 3.4 Status and Disposition; 3.2 for the alternatives.
- Escalate: deferred or rejected requests are communicated to the requester (PM 4.6.3.1 p120 (PDF 159)).

### D07 A new or changed requirement: reorder or change request [agile 3, 6; scope 3, 8]
- Options: predictive, the baseline changes only through change control (PM 5 p131 (PDF 170)); adaptive, one backlog for work and change ordered by the business representative (PM X3.3.4 p671 (PDF 710)), stated trade-off: it arose where very high change overwhelmed separating requests from work; none stated for the formal route. Ordering: business value (APG Table 4-2 p41 (PDF 851)), cost of delay divided by duration (APG Table 5-1 p59 (PDF 869)), risk (PM 11 p400 (PDF 439)), capacity (APG 5.2.6 p55 (PDF 865)). Selection of requirements into scope: voting, multicriteria decision analysis, nominal group (PM 5.2.2 p144 to 145 (PDF 183 to 184); 5.3.2 p153 (PDF 192)).
- Inputs and calc: 2.5 (how requirement changes are traced), 2.6 priority, 2.7, the scope baseline, which the book defines as the scope statement 2.8, the WBS 2.9 and the WBS dictionary 2.10 together (BoF 2.9 p49 (PDF 60)), the charter's 1.1 Project Boundaries (included and excluded), and for added work 2.18 and the cost documents; who the product owner is (ask). Calc: `weighted-score` for a matrix; `cd3` ranks by cost of delay divided by duration (the Guide prints the words, no units; the product owner supplies both numbers).
- Who pays: a requested function is not an identified risk, so it is not a charge on the contingency reserve (contingency is for identified risks, PM 7.2.2.6 p245 (PDF 284)); management
  reserve is for unforeseen work inside the scope, outside the baseline (PM 7.3.2.3 p252 (PDF 291)), so a new function is not that either, and the book names no rule for who pays for a requested
  function: not stated in the book. Read which reserve the charter allows and test the charter's own words against its reserve limit (a line that sends later changes "against the reserve" does not
  fit a contingency limited to identified risks; quote both and let the sponsor decide). Put "additional funding or an approved reserve draw" in the 3.3 as an explicit option and a question to the sponsor.
- Record: 6.2 Priority and Status or 2.6 Priority; 3.3 when scope, schedule or cost moves; 3.4; 3.2.
- Escalate: a change to user-visible scope, schedule or cost is the sponsor's under the charter; D05.

### D08 Requirements technique, scope boundary, WBS depth, dictionary detail [scope 1 to 6]
- Options: interviews, focus groups, surveys, observation, workshops, prototypes, each with a stated fit, no cost comparison (PM 5.2.2 p142 to 147 (PDF 181 to 186)). Scope statement: product analysis, alternatives analysis, facilitated workshops; exclusions manage expectations (PM 5.3.2 p153 to 154 (PDF 192 to 193)). WBS level 2 by phase, deliverable or contracted subcomponent; excessive decomposition brings "nonproductive management effort" (PM 5.4.2 p159 to 160 (PDF 198 to 199)); a control account holds two or more work packages, a package sits under one account (PM p161 (PDF 200)); rolling wave for far work (PM p160 (PDF 199)); hour limits not stated in the book. Dictionary: full, summary, or none for small projects (BoF 2.10 p52 to 53 (PDF 63 to 64)). Plans formal or informal (PM 5.1 p137 (PDF 176)); 2.4 and 2.5 may combine (BoF 2.4 p30 (PDF 41)).
- Inputs and calc: charter, stakeholder register, assumptions. Calc: none; the 2.10 cost table is Labor Total = Hours x Rate, Material Total = Units x Cost (BoF 2.10 Table 2.10 p54 (PDF 65)).
- Record: 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.10; 3.2.
- Escalate: after baselining a change is a 3.3 (D05).

### D09 Accept or refuse a delivered deliverable [scope 7; quality 12; agile 9]
- Options: Control Quality verifies against acceptance criteria (PM 8.3.1.4 p301 (PDF 340)) and passes verified deliverables to Validate Scope (PM 8.3.3.2 p305 (PDF 344)); Validate Scope uses inspection and voting (PM 5.5.2 p166 (PDF 205)); non-accepted deliverables are documented with reasons and may become a defect-repair request (PM 5.5.3.3 p166 (PDF 205)). Validate Scope concerns acceptance, Control Quality correctness (PM 5.5 p164 (PDF 203)). Agile: team defines done and release criteria, the product owner accepts at the demonstration (APG Table 5-1 p58 (PDF 868); APG 5.2.5 p55 (PDF 865)). Chapter 8 names no accept-as-is option. The trade-off between inspection and voting: not stated in the book.
- Inputs and calc: 2.6, 2.7, 2.24, quality reports. Calc: none.
- Record: 4.9 (Acceptance Criteria, Validation Method, Sign-off; BoF 4.9 p226 (PDF 237)); 3.6; 3.2; 3.3 for defect repair.
- Escalate: accepting with a known defect is the sponsor's decision through the project's own route (charter UAT failure options).

### D10 Estimating technique for a cost or a duration, and the range [schedule 4; cost 1, 2; resource 2; agile 5]
- Options: analogous (cheaper and quicker, less accurate; most reliable when activities are similar in fact), parametric (accuracy depends on the model and data), three-point (a range; triangular for thin or judgmental data), bottom-up (when an activity cannot be estimated with confidence) (PM 6.4.2 p200 to 202 (PDF 239 to 241); PM 7.2.2 p244 (PDF 283)). Analogous and parametric need accurate history and scalable models (PM 7.3.2.4 p253 (PDF 292)). Triangular versus beta by assumed distribution (PM 7.2.2.5 p245 (PDF 284), which prints cE = (cO + 4cM + cP) / 6 for beta cost; the duration section 6.4.2.4 prints only the triangular form). Range examples -25% to +75% early and -5% to +10% later are examples (PM 7.2 p241 (PDF 280)). Agile: relative estimation and velocity, not comparable across teams (APG Table 5-1 p58 (PDF 868); APG p67 (PDF 877)). Effort of each technique not stated in the book.
- Inputs and calc: effort, calendars, assumptions, risk register, basis of estimates (PM 6.4.3.2 p204 (PDF 243)). Calc: `pm_calc.py pert` (beta mean (tO + 4tM + tP) / 6, BoF 2.17 p76 (PDF 87); triangular mean (tO + tM + tP) / 3, PM 6.4.2.4 p201 (PDF 240); no standard deviation, not stated in the book); `pm_calc.py analogous` (multiplier, BoF 2.17 p75 (PDF 86)); `pm_calc.py bottom-up` (BoF 2.21 Table 2.20 p90 (PDF 101)); parametric by `effort-to-duration` (D11).
- Record: 2.16, 2.17, 2.20, 2.21 (Weighting Equation names the formula), assumption log for the basis.
- Escalate: the book calls an estimate "a prediction that is based on the information known at a given point in time" (PM 7.2 p241 (PDF 280)); never cutting it to fit is the team rule; a baseline change is a 3.3.

### D11 How many people, how long, from effort [schedule 5; resource 9]
- Options: duration = quantity of work x labor hours per unit (PM 6.4.2.3 p200 to 201 (PDF 239 to 240)); 2.17: Effort / (quantity x percent available x performance factor) = duration, with 150 / (2 x .75 x .8) = 125 hours (BoF 2.17 p75 (PDF 86)); one person: days = hours / 8, weeks = hours / 40 (BoF 2.16 p70 (PDF 81)). The book's stated trade-off of adding people: they shorten the work, not linearly, with coordination and learning costs (PM 6.4 p197 (PDF 236)). The printed equation divides by the factor while the prose multiplies: name the reading used and tell the team (BoF 2.17 p75 (PDF 86)). Typical productive time about 75 percent (BoF 2.17 p73 (PDF 84)).
- Inputs and calc: effort hours, percent available, performance factor. Calc: `pm_calc.py effort-to-duration`.
- Record: 2.17, 2.16, 2.28 Quantity and Comments.
- Escalate: more people or hours than allocated is D26 or D14.

### D12 Schedule detail, dependencies, leads and lags, iteration length [schedule 1 to 3; agile 4]
- Options: method and detail by alternatives analysis, trade-off detail against time to keep it current (PM 6.1.2.2 p181 (PDF 220)); decomposition and rolling wave (PM 6.2.2 p185 (PDF 224)); dependencies mandatory (legal, contractual, inherent) or discretionary, to be fully documented (PM 6.3.2.2 p191 to 192 (PDF 230 to 231)); FS, FF, SS, SF (PM 6.3.2.1 p190 (PDF 229)); leads and lags only in limited circumstances (PM 6.5.2.5 p214 (PDF 253)), never in place of logic (PM 6.3.2.3 p193 (PDF 232)). Time-boxing forces essential features first (PM 6.1.3.1 p182 (PDF 221)); demonstrate at least every 2 weeks as a guideline (APG 5.2.5 p55 (PDF 865)); a release is typically 3 to 6 months (PM 6.5.2.8 p216 (PDF 255)); sprint content is fixed once it starts (BoF 6.3 p244 (PDF 255)).
- Inputs and calc: WBS, dictionary, milestones, assumptions. Calc: none; notation FS+3d, FS-3d (BoF 2.15 p67 (PDF 78)).
- Record: 2.11, 2.12, 2.13, 2.14, 2.15, 6.3, assumption log.
- Escalate: work outside the baselines, or a moved baselined milestone, is a 3.3 (PM 6.2.3.4 p186 (PDF 225)).

### D13 Resolve over-allocation [schedule 7]
- Options: leveling balances demand with supply, uses float, can change the critical path; smoothing keeps the critical path and finish date, moves activities only within float, may not optimize every resource (PM 6.5.2.3 p211 (PDF 250)). Overtime or added resources weighed against late or phased delivery, with cost-benefit analysis (PM 9.6.2.1 p356 (PDF 395)); note that 9.6 Control Resources is written for physical resources (PM 9.6 p307 (PDF 346)), so for people it is an analogy, not the book's team-capacity technique.
- A resource paid per hour or per person-month is a cost driver: extending its window or adding hours changes 2.28 and the cost baseline 2.22 (labor total is hours x rate, BoF 2.10 Table 2.10 p54 (PDF 65)), so it is a 3.3 cost and resource impact and never "no cost change". Price it with `bottom-up` or the dictionary rates. State the person's facts with their source: the window in the charter (when the person joins and leaves), the hours and rate, and the scope package roll-up line that prices them, each with file and line.
  Quote the person's labour total from the scope package (hours x rate, BoF 2.10 Table 2.10 p54 (PDF 65)), never leave the total out, and say plainly that extra hours or keeping the person past the leaving date is a resource and cost change in both pay readings: the window in 2.26 and 2.28 and the charter's person-month basis move with it, and the labour total moves with the hours, or with the months when the person is paid by the month. When the charter and the dictionary give different pay bases, or the charter is silent, write both readings in two lines and ask the sponsor which governs.
- Inputs and calc: 2.18, 2.13, calendars; the load check in `SKILL.md`. Calc: `cpm` for float on a small network. Quote a critical path only after leveling.
- Record: 2.18, 2.28, 2.22 when hours or months change; 3.3 if dates or cost move.
- Escalate: reassigning inside the team is the PM's; moved dates and cost go to the sponsor.

### D14 We are late: shorten the schedule [schedule 8, 10]
- Step 0, before any compression: (a) read 2.18 and any 3.3 for compression already used (a fast-tracking allowance per phase, activities already divided so another person helps, an approved crash) and do not offer it a second time as a fresh option; what is left is what remains of it. Compression that exists only in a pending 3.3 (a levelled 2.18, a forecast in the request) is counted as proposed, not used: show it as that request's own option, so it is neither offered twice as fresh nor assumed approved. (b) While a 3.3 is pending the slip is measured against the charter baseline, not the pending dates (section 4, "While a 3.3 is pending"). (c) Check the stated slip against the 2.10 due dates and 2.18 (the user's milestone or date can be wrong), then against what the plan already absorbs: the variance threshold in 2.11 ("an agreed-upon amount of variation to be allowed before some action needs to be taken", PM 6.1.3.1 p182 (PDF 221)), the total float of the activities on the path (the amount an activity can be delayed from its early start without delaying the project finish, PM 6.5.2.2 p210 (PDF 249)), and any allowance the charter states for this work. An allowance counts only if it names the same cause and the same milestone or gate as the slip: quote it, say which cause and gate it names,
  and test each "this other date is not affected" claim against the gates the activity feeds; an allowance written for a different cause, or one that conflicts with a time criterion on the same milestone, does not absorb the slip, so quote both statements in the 3.3
  and let the sponsor decide, choosing no reading. A slip inside them is reported and watched; testing the slip against them first is the team's order of work, not a rule the book states. Only a slip beyond them goes to the options below, and resource leveling or smoothing (D13) belongs among them when the slip comes from over-allocation, with its trade-off (leveling can change the critical path; smoothing keeps the finish date and moves work only within float, PM 6.5.2.3 p211 (PDF 250)).
  (d) A 2.18 table prints no dependencies, and a project may have no network (2.15): then `cpm` has nothing to run on. Ask for the predecessor and the successors of the slipping activity and the milestone it feeds; if the
  user cannot say, run `cpm` on an assumed chain only to give a conditional answer, label every link "assumed", and put the missing dependency first among the open questions; float computed from an assumed chain is not a finding.
  (e) A date imposed before a schedule exists, or a request to bring a milestone forward, takes this same step: compare the date with the finish and float of the network (a violated constraint or imposed date can make the total float negative,
  PM 6.5.2.6 p215 (PDF 254)), then the options below; the estimate is not shortened to reach it, and when no compression closes the gap the route is a 3.3 to the sponsor (team rule).
- Options (PM 6.5.2.6 p215 (PDF 254)): negative float analysis (named as "a helpful technique" for finding where the schedule is violated, not as a compression technique itself); crashing (least incremental cost, adds resources, critical path only, may raise cost and risk, "does not always produce a viable alternative"); fast tracking (overlap, may cost rework, coordination and quality risk, and "may also increase project costs" (PM 6.5.2.6 p215 (PDF 254))). Also adjust durations "when more resources or less scope can be arranged", discretionary logic, leads and lags (PM 6.5.2.2 p210 (PDF 249)); less scope is a scope baseline change, so it goes through 3.3 like any other; what-if scenarios (PM 6.6.2.1 p227 (PDF 266)). Both compress "without reducing the project scope" (PM 6.5.2.6 p215 (PDF 254)); no chapter names a technique that shrinks an estimate. A new target schedule when delays are "so severe" (PM 6.6.3.5 p230 (PDF 269)); that a re-baseline loses the comparison with the old plan is an inference from the baseline being "a basis for comparison to actual results" (PM 6.5.3.1 p217 (PDF 256)), not a trade-off the book states. Schedule variance analysis and schedule modifications may result in a change request to the schedule baseline (PM 6.6.3.3 p229 (PDF 268); 6.5.3.5 p220 (PDF 259)); making it the route when no compression closes the gap is the team rule.
- Inputs and calc: network, float, thresholds; for SV and SPI the PV and EV of the item (if they are not given, say they are needed, section 1 item 2, and show no figure). Calc: `pm_calc.py cpm --slip NAME=DAYS` tests a slip against float and the critical path (outside arithmetic aid; `--deadline` takes working days from day 1, or a calendar date together with `--start`); `pm_calc.py crash --option NAME NORMAL CRASHED EXTRA --needed DAYS` ranks crashing options by extra cost per day saved, critical activities only, with the team's own crashed durations and costs (outside arithmetic aid: PM 6.5.2.6 p215 (PDF 254) names the least incremental cost and prints no equation); `pm_calc.py evm` (SV, SPI) and, as the optional time-based view, `earned-schedule` (SV(t) = ES - AT, SPI(t) = ES / AT, PM Trends in Project Cost Management p233 (PDF 272); the trend is the book's, not required). SPI alone misleads, a delay off the critical path may have little effect (PM 6.6.2.1 p227 (PDF 266)).
- Record: 3.3 Schedule (Increase, Decrease, Modify, Description), 3.2, 2.18, 2.32 for risks the compression creates (PM 6.6.3.5 p230 (PDF 269)), 4.3; a calendar date for a slip with `cpm --start` and `--holiday`.
- Escalate: sponsor by 3.3, and any limit of the Authority limits block (section 1); a baseline changes only through formal change control (PM 6.5.3.1 p217 (PDF 256)).

### D15 Respond to a cost or schedule variance [integration D7; cost 9; schedule 9; communications 4; agile 7]
- Options: root cause, alternatives, cost-benefit, trend, variance and earned value analysis (PM 4.5.2.2 p111 (PDF 150)); action is corrective, preventive or defect repair (PM 4.5.3.2 p112 (PDF 151)); a negative CV is often hard to recover (PM 7.4.2.2 p262 (PDF 301)); too severe a variance means a change request to revise the baseline (PM 7.4.3.4 p269 (PDF 308)). Raw data mean nothing until compared with budget, work done and thresholds (PM 4.5.1.3 p109 (PDF 148)). Agile: burndown can dispirit the team (APG p63 (PDF 873)); story points without finished features measure capacity (APG p66 (PDF 876)); velocity is the sum of the story points of the features actually completed in an iteration, and it can take four to eight iterations to reach a stable velocity (APG 5.4.1 p64 (PDF 874)); the Guide's worked example is about 500 points left at 50 points an iteration, about 10 iterations (APG p61 (PDF 871)). Relative cost of options not stated in the book.
- A favourable variance (positive CV "under planned cost", positive SV "ahead of schedule", PM Table 7-1 p267 (PDF 306)) is reported and compared with the same thresholds; it does not move a baseline, which changes only from the last baseline
  forward after an approved request (PM 4.6.3.2 p120 (PDF 159)). Forecast before relying on it (D16): the present-CPI EAC assumes it continues and the budgeted-rate EAC does not. Releasing contingency is a reserve analysis (D18), not a variance result.
  The book gives no rule for spending a saving, so adding scope with it is a change (D07, 3.3).
- Work or a deliverable that differs from the scope baseline (row 39): Control Scope compares the baseline with the actual results by variance analysis and trend analysis and decides whether corrective or preventive action is appropriate
  (PM 5.6.2.1 p170 (PDF 209)); a scope, schedule or cost variance can be so severe that a revised baseline is needed to give a realistic basis for performance measurement (PM 5.6.3.3 p171 (PDF 210)). The revised baseline is a change
  request through section 4, never an absorbed change (scope creep, D05). The threshold for "so severe": not stated in the book; the charter's variance limits are the project's, and the sponsor decides.
- Inputs and calc: work performance data, thresholds (an undefined base: section 1; test the overrun with `evm --threshold`). Calc: `pm_calc.py velocity` for an agile release (average and iterations remaining are outside aids; say how many iterations of history), `pm_calc.py evm` (SV = EV - PV, CV = EV - AC, SPI = EV / PV, CPI = EV / AC, VAC = BAC - EAC; PM 7.4.2.2 p262 to 263 (PDF 301 to 302)).
- Record: 4.1, 4.2 (Root Cause, Planned Corrective or Preventive Action, Impact to Overall Budget or Contingency Funds), 4.3, 4.4; 3.3 if a baseline moves.
- Escalate: a forecast overrun beyond the charter's percent, and any other limit of the Authority limits block (section 1), goes to the sponsor; state the base of the percent.

### D16 Forecast the final cost; is the BAC still reachable [cost 10; communications 5]
- Options (PM 7.4.2.2 p264 to 265 (PDF 303 to 304)): bottom-up (most common); budgeted rate (accepts results so far, improvement only when supported by risk analysis); present CPI (experience continues); CPI and SPI together (when schedule drives effort; 80/20 or 50/50 weights are judgment). Compare with the manual figure (PM 7.1 p239 (PDF 278)). TCPI above 1.0 is harder; reachable is "a judgment call" on risk, time and technical performance, no threshold stated (PM 7.4.2.3 p266 (PDF 305)). Always show the budgeted-rate EAC beside the present-CPI EAC and state each one's assumption: the budgeted rate accepts the variance to date as not repeated, so it is the optimistic figure unless risk analysis supports the improvement; the present-CPI EAC assumes the cumulative CPI continues. The book gives no rule for choosing; the PM selects one with a written justification (BoF 4.4 p207 (PDF 218)) and says which is the central case and why.
- Inputs and calc: cumulative PV, EV, AC, BAC. Calc: `pm_calc.py evm` (EAC = AC + (BAC - EV); BAC / CPI; AC + (BAC - EV) / (CPI x SPI); ETC = EAC - AC; TCPI).
- Record: 4.4 (EAC rows, Selected EAC, Justification, TCPI; BoF 4.4 p207 (PDF 218)), 4.2; 3.3 if the baseline must move. The blank 4.4 prints two EAC rows, EAC w/CPI and EAC w/ CPI*SPI, then Selected EAC, Justification, and Explanation (blank form p208 (PDF 219)); the budgeted-rate and a bottom-up EAC have no printed row, so write that figure and the reason for choosing it in Selected EAC, Justification, and Explanation.
- Escalate: an overrun beyond the charter's percent or any other limit of the Authority limits block (section 1); state the base of the percent.

### D17 Hold a reserve, and how large [cost 3, 4; schedule 6; risk 8]
- Options: contingency is a percentage, a fixed number, or from quantitative analysis, for identified risks only, "clearly identified" and reducible (PM 7.2.2.6 p245 (PDF 284)); schedule contingency a percentage of duration or fixed work periods (PM 6.4.2.6 p202 (PDF 241)), aggregated where paths converge (PM 6.5.2.1 p209 (PDF 248)); simulation gives finish probabilities (PM 6.5.2.4 p213 to 214 (PDF 252 to 253)); quantitative analysis can size reserve for a confidence level (PM 11.4 p436 (PDF 475)). Management reserve sits outside the baseline for unforeseen in-scope work, and each use is an approved baseline change (PM 7.3.2.3 p252 (PDF 291); p254 (PDF 293)). The percentage, a criterion for choosing, and the cost of holding it are not stated in the book.
- Inputs and calc: risk register with scores. Calc: `pm_calc.py emv` gives expected value of identified risks as an input; summing it into a reserve is the team's method, not a book rule. Once a reserve exists, `pm_calc.py reserve` compares what is left with the expected value of the open risks (D18).
- Record: 2.20 Reserve, 2.21, 2.22, 2.31 Risk Management Funding and Contingency Protocols, 2.36, 3.2.
- Escalate: creating a management reserve is the sponsor's by 3.3; a reserve use beyond the limits of the Authority limits block (section 1) is the sponsor's too.

### D18 Draw on, release or request more reserve [cost 8; risk 12; communications 6; agile 10]
- Options: reserve analysis monitors whether reserves are still needed; use for planned responses, remove unused contingency, add or release savings from captured opportunities, request more when new analysis shows a need (PM 7.4.2.2 p265 (PDF 304)); compare remaining contingency with remaining risk, shown as a burndown (PM 11.7.2.1 p456 (PDF 495)). Contingency is for identified risks (PM 7.2.2.6 p245 (PDF 284)); unforeseen work belongs to management reserve (PM p252 (PDF 291)). Say which reserve the budget line names and report a different charter wording as a source error (section 5, item 11). Unspent contingency is released by reserve analysis, and a favourable variance is not unspent contingency; neither moves the baseline without a 3.3 (PM 4.6.3.2 p120 (PDF 159)).
- Reserve draw: read the Authority limits block (section 1), points 1 to 6, and 2.22 at the time; write the word the budget line uses (contingency or management). If the charter requires change control for every draw, each draw is a 3.3 and only the approver changes with the amount; if it is silent, ask the sponsor and record the answer in 3.2. The cost of monitoring a reserve and a trade-off among the uses of a saving: not stated in the book.
- Inputs and calc: risk register, reserve balance (2.33 Reserve Status: Total, Used to Date, Used This Period, Remaining Reserve; BoF 2.33 p133 to 136 (PDF 144 to 147)). Calc: `pm_calc.py reserve --contingency X --used Y --risk ID=PROBABILITY:IMPACT` compares the remaining contingency with the expected value of the open risks (outside arithmetic aid; the book describes the comparison and may show it as a burndown, PM 11.7.2.1 p456 (PDF 495), and prints no rule for adequate, so the verdict is the team's).
- Record: 3.3 per draw where the charter requires, 3.2, 4.2, 4.4 Budget Impact (BoF 4.4 p207 (PDF 218)), 2.32, 2.33.
- Escalate: a draw above a limit of the Authority limits block (section 1) goes to the sponsor; so does a forecast overrun beyond its percent.

### D19 Estimates exceed funds; make, buy or lease [cost 5, 6; procurement 1]
- Options: funding limit reconciliation, rescheduling work to level expenditure, trade-off moved dates (PM 7.3.2.5 p253 (PDF 292)); alternatives analysis of making, purchasing, renting or leasing resources (PM 7.1.2.2 p238 (PDF 277)) and of the cost, schedule, resource and quality impacts of buying versus making (PM 7.2.2.6 p245 (PDF 284); see also PM 7.2 p241 (PDF 280)); self-funding, equity, debt (PM 7.1.2.2 p238 (PDF 277)); make-or-buy analysis weighs skills, specialized and independent expertise, permanent obligations and risk, and may use payback, ROI, IRR, NPV or benefit/cost, no criterion picks among them (PM 12.1 p473 (PDF 512)); managing a purchase costs money (the cost baseline includes the costs of managing the procurement and sellers, PM 12.2.1.1 p484 (PDF 523)). On adaptive projects with strict budgets "the scope and schedule are more often adjusted to stay within cost constraints" (PM 7 p234 (PDF 273)), which is a baseline change and so a 3.3. Only integrated change control raises the budget (PM 7.4 p259 (PDF 298)).
- Inputs and calc: estimates, funding table, 2.22 curve. Calc: `pm_calc.py funding --tranche NAME=AMOUNT --through NAME --spent AMOUNT` compares the funds released by tranche with the cost to date (outside arithmetic aid; the book shows funding as steps against the cost baseline, PM 7.3.3.2 p256 (PDF 295) and Figure 7-9 p255 (PDF 294), and prints no equation); `pm_calc.py payback --investment X --net N1 N2 ...` (outside arithmetic aid; payback analysis is named, PM 7 p233 (PDF 272), PM 12.1.2.3 p473 (PDF 512), and no equation is printed; whole periods, undiscounted). Say so in the answer.
- Record: 2.19 Additional Details, 2.37 Assumptions and Constraints, 3.2 (PM 12.1.3.6 p479 (PDF 518)), 3.3.
- Escalate: sponsor by 3.3; cutting the estimate is not a technique.

### D20 Quality standards, objectives, metrics, and changing them [quality 1, 2, 13]
- Options: expert judgment, benchmarking, interviews (PM 8.1.2 p281 to 282 (PDF 320 to 321)); multicriteria analysis, matrix diagrams, cost-benefit (PM 8.1.2 p282 to 284 (PDF 321 to 323)); the book gives no weights or cut-off. Quality and grade differ (PM p274 (PDF 313)). A metric is an attribute plus how Control Quality verifies it (PM 8.1.3.2 p287 (PDF 326)). 2.23 is "developed once and is not usually changed" (BoF 2.23 p95 (PDF 106)), yet the approach may change "due to the actual results" by change request (PM 8.2.3.4 p297 (PDF 336)). Never edit a threshold to make a failing result pass.
- Inputs and calc: regulations, quality system, acceptance criteria, RTM. Calc: none.
- Record: 2.23 (Quality Standards, Quality Objectives, Approaches), 2.24, 2.7; 3.2.
- Escalate: an acceptance-criteria change is a scope-baseline decision: 3.3 to the sponsor.

### D21 Prevention against failure cost; what to review; when to test [quality 3, 4, 5]
- Options: cost of quality weighs prevention and appraisal against internal and external failure; past the optimum extra spend is "neither beneficial nor cost effective" (PM 8.1.2.3 p282 to 283 (PDF 321 to 322)); cost-benefit; flowcharts with EMV (PM 8.1.2.5 p284 (PDF 323)); test and inspection planning (PM 8.1.2.6 p285 (PDF 324)); early testing cuts the cost of fixing (PM 8.3.2.4 p303 (PDF 342)); agile builds frequent review steps in (PM p276 (PDF 315)). The stated trade-off is the optimum above, and no coverage threshold or defect-cost estimate is in the book. Rushing inspections risks undetected errors (PM p273 (PDF 312)).
- Inputs and calc: scope baseline, risk register. Calc: `emv` only where a branching probability is given (the book names EMV here, p284 (PDF 323), without defining it).
- Record: 2.23 (Deliverables and Processes Subject to Quality Review), 2.24, 2.20; quality work added or removed after baselining: 3.3 (PM 8.2.3.4 p297 (PDF 336)).
- Escalate: when budget, date and quality cannot all hold, 3.3 to the sponsor.

### D22 Sampling or full inspection; control or specification limits [quality 6, 7]
- Options: statistical sampling, size and frequency set in planning (PM 8.3.2.1 p303 (PDF 342)), or 100% inspection (PM 8.2.3.1 p296 (PDF 335)); attribute against variable sampling (PM p274 (PDF 313)). Specification limits come from requirements; control limits come from statistical calculation and show natural capability (PM 8.3.2.5 p304 (PDF 343)). Sample size, confidence, run rules, limit width, and a sampling-versus-full trade-off: not stated in the book; do not borrow without naming the source.
- Inputs and calc: metrics, population size, tolerance. Calc: none.
- Record: 2.24 Measurement Method (sample or full run), 2.23 Quality Control Approach (frequency).
- Escalate: sample to full after baselining: 3.2, and 3.3 if cost or schedule moves.

### D23 Audit: who, how independent, how often [quality 8; procurement 13; risk 12]
- Options: a quality audit is structured, independent and usually run by a team external to the project; scheduled or random (PM 8.2.2.5 p294 to 295 (PDF 333 to 334)); stated benefit lower cost of quality and higher acceptance; risk audits with format and objectives defined beforehand (PM 11.7 p456 (PDF 495)); procurement audits depend on independence and credibility (PM 12 p494 (PDF 533); PM 12.3.2.5 p498 (PDF 537)). Frequency and the cost of scheduled against random: not stated in the book. The QA engineer's own check is inspection, not an audit (PM 8.3.2.3 p303 (PDF 342)).
- Inputs and calc: quality plan, earlier audits, lessons. Calc: none.
- Record: 3.6 (BoF 3.6 p182 to 183 (PDF 193 to 194)), 4.5, 4.7, 2.23, 2.31 Risk Tracking and Audit, 3.2.
- Escalate: an unfunded audit is new work: 3.3 with Cost and Schedule impact.

### D24 A nonconforming deliverable and its cause [quality 9, 11]
- Options: the plan holds what to do with nonconforming products (PM 8.2.1.1 p290 (PDF 329)); rework, defect repair, 100% inspection (PM 8.2.3.1 p296 (PDF 335)); choose by alternatives analysis (PM 8.2.2.2 p292 (PDF 331)) or multicriteria analysis on life cycle cost, schedule, satisfaction, risk (PM 8.2.2.3 p293 (PDF 332)). Cause: root cause analysis (PM 8.2.2.2 p292 (PDF 331)), fishbone, affinity, flowchart, histogram, scatter (PM 8.2.2.4 p293 (PDF 332)); six-step problem solving (PM 8.2.2.7 p295 (PDF 334)); PDCA and Six Sigma (PM 8.2.2.8 p296 (PDF 335)); no rule picks one. Removing all root causes stops recurrence.
- Inputs and calc: control measurements, defect log, severity. Calc: none.
- Record: 3.6 Deficiencies or Defects with action, owner, due date (BoF 3.6 p181 (PDF 192)); 3.1 (PM 8.3.3.6 p306 (PDF 345)); 3.5; 3.2.
- Escalate: 3.3 when a plan component, document or process is impacted (PM 8.2.3.3 p296 (PDF 335)).

### D25 Roles, RAM and team charter [resource 1, 8]
- Options: hierarchical, matrix, text formats (PM 9.1.2.2 p316 (PDF 355)); RAM at work package, control account or activity level (BoF 2.25 p101 to 102 (PDF 112 to 113)); one accountable person per task (PM p317 (PDF 356)); the team develops its charter (PM 9.1 p320 (PDF 359)); its decision rule states the PM's relative power, voting and when decisions reopen (BoF 2.27 p110 (PDF 121)). Cost of detail not stated in the book.
- Inputs and calc: WBS, dictionary, 1.3. Calc: none.
- Record: 2.25, 2.26, 2.27, 2.29 (resource types and categories behind the estimates), 3.2.
- Escalate: authority limits come from 1.1.

### D26 Acquire a role; staffing change; too little capacity [resource 3, 7]
- Options: pre-assignment, multicriteria analysis, negotiation, virtual teams (PM 9.3.2 p332 to 333 (PDF 371 to 372)); failure to acquire hits schedule, budget, quality and risk, and the manager documents the impact of any substitute (PM 9.3 p330 (PDF 369)). Capacity: overtime or added resources weighed against late delivery with cost-benefit analysis, problem solving and negotiation (PM 9.6.2.1 to 9.6.2.3 p356 to 357 (PDF 395 to 396)), but 9.6 Control Resources is written for physical resources (PM 9.6 p307 (PDF 346)), so for people it is an analogy; also D13 and D14. Staffing changes can disrupt the project (PM 9.5 p350 (PDF 389)). A trade-off among pre-assignment, negotiation and virtual teams: not stated in the book.
- Inputs and calc: 2.18 loading, cost baseline. Calc: `effort-to-duration` for the effect on duration.
- Record: 2.26, 2.28, 2.29 when the kind or category of resource changes, 2.32, 3.1, 3.2; 3.3 when the cost baseline or schedule moves (PM 9.3.3.4 p334 (PDF 373)).
- Escalate: reassignment inside the team is the PM's; a baseline effect or a limit of the Authority limits block (section 1) goes to the sponsor.

### D27 Team development and assessment [resource 4, 6]
- Options: colocation, virtual team (reduced costs and more skilled resources, PM 9.4.2.2 p340 (PDF 379); the challenges are mainly in communication, PM 9 trends p311 (PDF 350)), team building, recognition (works only for a need the person values), training, assessments (PM 9.4.2 p340 to 342 (PDF 379 to 381)); assessment indicators skills, competencies, turnover, cohesiveness (PM 9.4.3.1 p343 (PDF 382)). Interval and thresholds: not stated in the book.
- Inputs and calc: 2.26, 2.27, lessons. Calc: none.
- Record: 2.26 Training Requirements, Rewards and Recognition, Team Development; 3.7 (comments justify the rating, BoF 3.7 p185 (PDF 196)); 3.5.
- Escalate: extra cost is a 3.3 if the cost baseline moves.

### D28 Handle a conflict [resource 5; stakeholder 9]
- Options: withdraw, smooth, compromise ("occasionally results in a lose-lose situation"), force (win-lose, for an emergency), collaborate (consensus, can be win-win) (PM 9.5.2 p349 (PDF 388)); factors importance, intensity, time pressure, relative power (PM p348 (PDF 387)); team members first, then PM facilitates, then formal procedures (PM 9.5.2.1 p348 (PDF 387)); negotiation for support or agreement (PM 13.3.2.3 p527 (PDF 566)). Days before escalating: not stated in the book.
- Inputs and calc: 2.27 process, issue log. Calc: none.
- Record: 3.1 Final Resolution, 3.2, 2.27 Conflict Resolution Process, 2.40 if the plan changes.
- Escalate: by the rule in 2.27 and the charter.

### D29 Who needs which information, how and how often [communications 1 to 3]
- Options: communication requirements analysis combines the type and format of information with the value of that information (PM 10.1.2.2 p369 (PDF 408)); interactive (real time), push (assures distribution, not understanding), pull (recipient acts) (PM 10.1 p374 (PDF 413)); confidential content needs added security and a named releaser (PM p371, 377 (PDF 410, 416)); reports regular or on exception, level of detail adapted (PM 10.2 p385 (PDF 424)). Intervals and a channel-count formula: not stated in the book.
- Inputs and calc: 1.3, 2.40 gaps, availability. Calc: `pm_calc.py comms-channels` (outside arithmetic aid, label it so).
- Record: 2.30 (Stakeholder, Information, Method, Timing or Frequency, Constraints), 4.1, 4.2.
- Escalate: a baselined plan changes by 3.3 (D05).

### D30 Escalate, and to whom [communications 7; risk 10]
- Options: the escalate response when a threat or opportunity is outside project scope or beyond PM authority (PM 11.5.2 p442 (PDF 481); p444 (PDF 483)); the PM decides whom to notify, the recipient must accept ownership, the level matches the affected objective, and the team stops monitoring it. 4.1 and 4.2 may get an escalation field (BoF 4.1 p191 (PDF 202)). No threshold or time in the book; the choice among levels of authority is not stated in the book, and the project's own levels are in the charter.
- Inputs and calc: the charter's authority and escalation rules (the Authority limits block, section 1). Calc: none.
- Record: 2.32 Response (Escalate), Status, Comments (accepting party, date); 3.2; 2.30.
- Escalate: sponsor approval of a baseline change is D06, and the project keeps the risk.

### D31 Identify, classify and prioritise stakeholders [stakeholder 1 to 3]
- Options: identification by expert judgment, questionnaires, brainstorming, document analysis, meetings (PM 13.1.2 p511 to 514 (PDF 550 to 553)), repeated at each phase and on significant change (PM p508 (PDF 547)); power/interest grid for small projects or simple relationships (PM p512 (PDF 551)), cube as a refinement of the grids and salience for large complex communities (PM p513 (PDF 552)); BoF 1.4 puts the 3 x 3 cube with larger projects (BoF 1.4 p15 (PDF 26)); prioritise highest interest and influence first; engagement matrix with current C and desired D (PM 13.2 p521 to 522 (PDF 560 to 561)). Scoring, cut-off and gap that needs action: not stated in the book.
- Inputs and calc: charter, agreements, logs. Unsourced ratings are assumptions (PM p515 (PDF 554)). Calc: none.
- Record: 1.3, 1.4, 2.40 (C, D), assumption log.
- Escalate: a plan change is a 3.3.

### D32 Engagement approach, plan formality, off-plan response [stakeholder 4 to 6]
- Options: root cause, assumption analysis, benchmarking, mind mapping (PM 13.2.2 p520 to 521 (PDF 559 to 560)); in 13.3 feedback, conflict management, negotiation, observation (PM p526 to 527 (PDF 565 to 566)); plan formal or informal, small projects may fold into the register (PM p522 (PDF 561); BoF 2.40 p158 (PDF 169)); revise on four triggers (PM p518 (PDF 557)). Off plan: alternatives, root cause, stakeholder analysis, multicriteria analysis, voting (PM 13.4.2 p533 to 534 (PDF 572 to 573)); corrective or preventive action is a change request (PM p535 (PDF 574)). Costs not stated in the book.
- Inputs and calc: 1.3, 1.4, 2.40, logs. Calc: `weighted-score` for multicriteria.
- Record: 2.40, 1.3, 3.1, 2.32, 3.5; 2.30 and 2.18 must agree.
- Escalate: 3.3 to the sponsor.

### D33 Issue log: what, how urgent, who, by when [stakeholder 8]
- Options: an issue is a current condition or a risk event that has occurred (BoF 3.1 p165 (PDF 176)); priority examples urgent, high, medium, low (BoF Table 3.1 p166 (PDF 177)); no scale or response time is stated, and a trade-off among the examples is not stated in the book. One assigned person; Res. Date is the deadline.
- Inputs and calc: 2.32, 4.1, 4.2. Calc: none.
- Record: 3.1; 2.32 must agree; 3.2; 3.5.
- Escalate: D30.

### D34 Risk process weight, scales, identification, prioritisation [risk 1 to 4]
- Options: tailor to size and complexity (PM 11 p400 (PDF 439)); matrix 3 x 3 small, 5 x 5 medium, 10 x 10 large (BoF 2.34 p137 (PDF 148); BoF 2.35 p142 (PDF 153)); scales three or five levels reflecting stakeholder appetite (PM 11.1.3.1 p407 (PDF 446)). Identification: brainstorming, checklists, interviews, root cause, assumption analysis, SWOT, document analysis, prompt lists, workshop (PM 11.2.2 p414 to 416 (PDF 453 to 455)); statement "EVENT may occur, causing IMPACT" (BoF 2.32 p129 (PDF 140)). Prioritisation: data quality assessment, probability and impact, categorisation (PM 11.3.2 p423 to 426 (PDF 462 to 465)); assessments are biased and each risk gets one owner (PM p420 to 421 (PDF 459 to 460)). Which identification or prioritisation technique fits which project, and the matrix size by project size beyond the examples: not stated in the book.
- Inputs and calc: assumptions, scales from 2.31. Calc: `pm_calc.py risk-score` (Score = Probability x Impact, PM 11.1.3.1 p408 (PDF 447)); Figure 11-5 values are an example. Never guess a score.
- Record: 2.31, 2.32, 2.34, 2.35, 3.2.
- Escalate: D30.

### D35 Quantitative analysis, or none [risk 5]
- Options: only if the plan requires it; likely for large, complex, strategic or contractual projects; needs good data, sound baselines, software and expertise, and costs time, the book's stated trade-off (PM 11.4 p429 (PDF 468)); simulation, sensitivity, decision tree, influence diagrams (PM p432 to 436 (PDF 471 to 475)). No score cut-off in the book. Many projects omit it (BoF 2.33 p131 (PDF 142)).
- Inputs and calc: baselines, numeric probability and impact. Calc: `pm_calc.py emv` (branch EMV = sum of probability x net path value, PM p435 (PDF 474)).
- Record: 2.31 Methodology, 2.33, 3.2.
- Escalate: none.

### D36 Response strategy for a risk and for overall risk [risk 6, 7]
- Options: threats escalate (PM 11.5.2.4 p442 (PDF 481)); avoid, transfer (premium), mitigate, accept (active reserve or passive review) (PM 11.5.2.4 p443 (PDF 482)); opportunities exploit, share, enhance, accept, escalate (PM 11.5.2.5 p444 (PDF 483)); overall risk, five similar strategies (PM p445 to 446 (PDF 484 to 485)). Choose by alternatives analysis, cost-benefit or multicriteria analysis on cost, effectiveness, timing, secondary risks (PM p446 (PDF 485)). A response is appropriate, cost-effective, realistic, agreed and owned (PM p439 (PDF 478)). Summing the register is not overall risk (PM p397 (PDF 436)).
- Fit and trade-off of each threat strategy, all five in the options table (PM 11.5.2.4 p442 to 443 (PDF 481 to 482)): escalate, when the threat is outside the project scope or beyond the PM's authority; avoid, for high-priority threats with high probability and a large negative impact, and its examples include "extending the schedule" or "reducing scope", which are baseline changes and so go to 3.3; transfer, shifts ownership to a third party and "often involves payment of a risk premium"; mitigate, reduces probability or impact, and early action "is often more effective than trying to repair the damage after the threat has occurred"; accept, for low-priority threats or where addressing it is not possible or not cost-effective, active with a reserve or passive. A mixed response carries one label per part (avoid, mitigate or fallback), each taken from the book's own wording below.
- Classifying a mixed response, part by part with the book's words: action to "isolate the project objectives from the risk's impact" is listed under avoid (PM 11.5.2.4 p443 (PDF 482)), so a response that isolates the work behind one interface is avoid by the book, not mitigate; prototype development, more tests and "designing redundancy into a system" are listed under mitigate (PM p443 (PDF 482)), so a proof of concept is mitigate; a second provider used only if the first fails is a contingent response, a fallback plan (PM 11.5.2.6 p445 (PDF 484); BoF 2.36 p145 (PDF 156)). A label for the response as a whole is not stated in the book (PM 11.5.2.4 p442 to 443 (PDF 481 to 482)); record the part-by-part labels in 3.2. In the options table keep the five strategies as rows; put do nothing and the 3.3 route on separate lines under it.
- Who pays when the seller's price rises or a pass-through cost appears (the project's own subscription or a gateway price): read the agreement price type in 2.37 and 2.38, the assumption log (1.2) and the exclusions, then apply the book's description of the type. Firm fixed price is set at the outset and not subject to change unless the scope of work changes; fixed price incentive fee has a ceiling above which the seller bears the cost; fixed price with economic price adjustment allows predefined adjustments for conditions such as inflation or commodity cost; cost-reimbursable pays the seller's legitimate actual costs plus a fee (PM 12.1.1.6 p471 to 472 (PDF 510 to 511)). Contracts allocate a risk to the party most able to manage it, and the buyer accepts the risks the contractors cannot control (PM 12 trends p463 (PDF 502)). For a cost that no agreement of the project covers, who pays is not stated in the book: quote the assumption or exclusion of the project that settles it, and if the cost baseline must move it is a 3.3 to the sponsor (D18 for the reserve).
- Inputs and calc: scored register, reserve. Calc: `weighted-score` for a matrix; `pm_calc.py response-effectiveness --option NAME IMPACT_BEFORE IMPACT_AFTER COST` computes cost effectiveness = change in impact level / implementation cost, the ratio the book prints in words (PM 11.5.2.8 p446 (PDF 485)); the levels and the cost are the team's, and the book gives no threshold.
- Record: 2.32 (Response, Actions, Revised columns, Responsible Party), 2.36 (Responses, Secondary Risks, Residual Risk), 2.33; 3.3 if a baseline moves (PM 11.5.3.1 p447 (PDF 486)).
- Escalate: D30. A response that changes the cost or schedule baseline or a plan (a paid second provider, a re-plan) is a change request to the sponsor on 3.3 (PM 11.5.3.1 p447 (PDF 486)); the route is never to trim an estimate to pay for it (team rule).

### D37 Trigger a contingency plan; review cadence [risk 9, 12]
- Options: a contingent response needs sufficient warning, and its triggering events "should be defined and tracked" (PM 11.5.2.6 p445 (PDF 484)); the book gives no numeric trigger, and the charter sets none for the project's responses unless its text says so. Form 2.36 has no trigger box: the Contingency Plan element says the plan starts "if specific events occur, such as missing an intermediate milestone" (BoF Table 2.32 p145 (PDF 156)), so the trigger is written there. If no trigger is written, list it as an open question for the risk owner and never write that a trigger has fired; the "Revised" columns of 2.32 change only after the response has been carried out; the register holds triggers, warning signs, contingency and fallback plans (PM p448 (PDF 487)); contingency plan for an accepted risk, fallback when other strategies fail (BoF 2.36 p145 (PDF 156)); technical performance analysis and risk reviews (PM 11.7 p456 to 457 (PDF 495 to 496)). Cadence: not stated in the book. "No action is taken" is the named common failure (PM p450 (PDF 489)).
- Inputs and calc: register triggers. Calc: none.
- A response whose due date falls before a milestone that a pending 3.3 moves: date the response against the charter milestone, name the pending 3.3 date beside it, and ask the sponsor which governs; a rule for this case is not stated in the book (PM 4.6 p115 (PDF 154)), and a pending request does not change the baseline (section 4, "While a 3.3 is pending").
- When the risk occurs: the book says a risk review identifies "issues that have arisen as the result of risks that have occurred" and closes outdated risks (PM 11.7.2.3 p457 (PDF 496)), and issues "can also arise from a risk event that has occurred and must now be dealt with" (BoF 3.1 p165 (PDF 176)). The 2.32 entry stays in the register (nothing in the book removes it); its Status takes the book's values, open or closed (BoF Table 2.29 p129 (PDF 140)), and stays open while the response is carried out; Actions and Comments record that it occurred, the date and the 3.1 entry. The 3.1 entry uses the same ID and risk statement text. Closing it is the PM's decision, recorded in 3.2; the book states no further rule.
- Record: 2.36 Contingency Plan, Fallback Plans; 2.32 Actions, Status and Comments; 3.1 once it occurs; 2.31 Frequency and Timing; 2.33 Reserve Status; 4.5.
- Escalate: reserve draw is D18; baseline effect is D05.

### D38 Contract type and incentive [procurement 2]
- Options: fixed price (FFP; FPIF with a ceiling; FPEPA) when requirements are well defined; cost-reimbursable (CPFF, CPIF sharing by a prenegotiated formula, CPAF with the buyer's subjective award) when scope is expected to change; T&M for staff augmentation or when a precise SOW cannot be written quickly (PM 12.1 p471 to 472 (PDF 510 to 511)). Fixed price for evolving work is the mismatch (PM p476 (PDF 515)); each type's stated fit is the trade-off, and no cost comparison among the types is given.
- Inputs and calc: requirements stability, SOW. Calc: none.
- Record: 2.38 Contract Type and Incentive or Award Fee table; 3.2.
- Escalate: the PM is typically not authorized to sign (PM p460 (PDF 499)).

### D39 Delivery method, selection method, criteria and weights [procurement 3 to 5]
- Options: delivery methods and phases with knowledge transfer (PM 12.1.3.2 p476 (PDF 515)); more than one seller mitigates a seller's failure (PM 12.2 p485 (PDF 524)); least cost, qualifications only, quality-based, quality and cost-based, sole source, fixed budget, each with a stated condition (PM 12.1 p473 to 474 (PDF 512 to 513)). Weights sum to 100 percent, Score = Weight x Rating, highest total wins (BoF 2.39 p155 (PDF 166)); include life cycle cost (PM p478 (PDF 517)). No rule for choosing weights; fix them before seeing proposals.
- Inputs and calc: requirements, strategy. Calc: `pm_calc.py weighted-score`.
- Record: 2.38, 2.39, 3.2.
- Escalate: sole source needs a 3.2 justification; complex high-value awards need senior approval (PM 12.2 p488 (PDF 527)).

### D40 Independent estimate, bid document, roles, timing, risk allocation [procurement 6 to 10]
- Options: independent estimate as a benchmark, a big gap may mean a deficient SOW (PM 12.1.3.7 p479 (PDF 518)); RFI, RFQ, RFP by the question asked (PM p477 (PDF 516)); bidder conference, advertising (PM 12.2 p487 (PDF 526)); decentralized or centralized purchasing (PM p462 (PDF 501)); long-lead items ordered early (PM p464 (PDF 503)); each risk to the party best able to manage it, bonds and insurance (PM p463 (PDF 502); p475 (PDF 514)). Costs of an estimate or a bond: not stated in the book.
- Inputs and calc: SOW, milestones, register. Calc: none.
- Record: 2.37 (Independent Estimates, Timing, Roles, Risk Management), 2.32, 3.2; 3.3 when a purchase date moves the baseline (PM p490 (PDF 529)).
- Escalate: negotiation and signing by the authorized person (PM p488 (PDF 527)).

### D41 Payments, amendments, seller variance and claims [procurement 11, 12]
- Options: agreement components (PM 12.2 p489 (PDF 528)); payment tied to output, not inputs (PM 12.3 p494 (PDF 533)); amend only by mutual written consent and approve before implementing (PM p494 (PDF 533); p496 (PDF 535)); performance review, earned value, trend, inspection (PM 12.3.2 p498 (PDF 537)); claims by negotiation, else ADR; a seller delay may need a baseline update (PM p500 (PDF 539)); an unrecorded constructive change can become a claim (PM p499 (PDF 538)). Cheapest remedy not stated in the book.
- Who pays for a seller's price rise or a pass-through cost: follow the "Who pays" paragraph of D36 (price type in 2.37 and 2.38, assumptions, exclusions, the book's description of each type, PM 12.1.1.6 p471 to 472 (PDF 510 to 511)); the book says contractor and material costs can change with fluctuating prices and need to be incorporated into the cost baseline (PM 12.3.3.5 p500 (PDF 539)), that an agreement is amended by mutual consent, typically in writing (PM p494 (PDF 533)), and that procurement changes are documented and approved before they are implemented (PM p496 (PDF 535)); the cost baseline update is a 3.3.
- Inputs and calc: 4.6, agreements. Calc: `pm_calc.py evm` on seller data.
- Record: 4.6 (Claims or Disputes; no cost forecast on a fixed price, BoF 4.6 p214 (PDF 225)), 3.1, 3.3, 3.4, 2.37.
- Escalate: contract changes go through 3.3 and the authorized signer.

### D42 Close a contract, phase or project; stop early [integration D9; procurement 14]
- Options: document, regression, trend, variance analysis and meetings to confirm acceptance and exit criteria (PM 4.7.2 p126 to 127 (PDF 165 to 166)); no open issues or risks (PM p124 to 125 (PDF 163 to 164)); early stop needs documented reasons and transfer of work (PM p123, 128 (PDF 162, 167)); contract closes after disputes resolved, product accepted, final payments made (BoF 4.8 p222 (PDF 233); PM 12.3 p499 (PDF 538)); 4.8 may fold into 5.2 (BoF 4.8 p222 (PDF 233)); unmet benefits reported with degree reached (PM p128 (PDF 167)). Stopping early: the book prints the procedure to investigate and document the reasons for actions taken if a project is terminated before completion (PM 4.7 p123 (PDF 162)), and closure documents that say why it was terminated and formalize the transfer of finished and unfinished deliverables (PM 4.7.3.4 p128 (PDF 167)). When to stop or continue, the criterion and the trade-off between them: not stated in the book.
- Inputs and calc: charter exit criteria, logs, acceptance. Calc: none.
- Record: 5.2, 5.1, 4.8, 4.9, 3.5; 1.1 exit criteria are the test; an early stop is a charter change, so 3.3 and 3.2 carry the reasons.
- Escalate: the sponsor accepts closure and decides an early stop, by 3.3 (D01: a change to the charter is a 3.3); the PM documents the reasons and the transfer.

### D43 Knowledge, lessons, retrospective [integration D8; agile 8]
- Options: knowledge management connects people, information management codifies (PM 4.4 p103 (PDF 142)); codified knowledge lacks context, tacit knowledge is hard to write down (PM p100 (PDF 139)); capture throughout (PM p100 (PDF 139)). Retrospective each iteration, also at a release, a milestone or when stuck (APG 5.2.1 p51 (PDF 861)); limit actions to capacity (APG p51 (PDF 861)); no more than three items (APG Table 5-1 p59 (PDF 869)); starfish or FLAP (BoF 6.4 p246 (PDF 257)); the book states no trade-off between the retrospective formats (not stated in the book).
- Inputs and calc: logs, reports. Calc: none.
- Record: 3.5, 6.4, 5.1; 3.2.
- Escalate: none.

## 4. Integrated change control path

Use for every decision that changes a baseline, a plan or a controlled document. The process runs from start to completion and the project
manager is ultimately responsible (PM 4.6 p115 (PDF 154)). The section is PM 4.6, printed pages 113 to 120 (PDF pages 152 to 159). State these
steps in order when you answer, and say whether the charter names a change control board; if it names none, the sponsor decides what the
charter gives the sponsor (D06), and no board is invented.

**Order to state, as a numbered list of eight:** (1) trigger and scope; (2) the request on 3.3; (3) impact analysis of time, cost, resources and risk (PM 4.6.2.5 p120 (PDF 159)); (4) the decision (approve, defer or reject) with its
Justification on page 3 of 3.3; (5) the record in 3.4, where the row is completed with Status and Disposition; (6) tell the requester; (7) implement; (8) update the affected documents. The book tracks a change in the log "from the change request through the
final decision" (BoF 3.4 p175 (PDF 186)) with Status open, pending or closed (Table 3.4 p176 (PDF 187)), so a row may exist while the request is pending; writing the row once the decision is made is the team's convention, not a book rule,
and no reason beyond that convention is given for it. Do not fold the requester and the implementation into the options.

1. **Trigger and scope.** Any stakeholder may ask, at any time; a verbal ask is written down and entered in the change system. Before baselines,
   no formal control; once baselined, every request goes through (PM 4.6 p115 (PDF 154)). Which artifacts are controlled: configuration management
   plan (PM p115 (PDF 154)); what counts as a change rather than a revision: 2.2 Definitions of Change (BoF 2.2 p25 to 26 (PDF 36 to 37)). When the charter already fixes the scope and 2.8 to 2.10 are not baselined yet, there is no scope baseline to compare with and
   the book asks for no formal control before baselines; the charter's Project Boundaries are still signed, and the project's own rule (D01) sends a charter change
   to 3.3 and the sponsor. Whether to raise a 3.3 before the baselines exist is the team's judgment, recorded in 3.2.
2. **Request.** Complete 3.3, whose blank form prints (PDF 183 to 185, printed 172 to 174): Requestor; Category (Scope, Quality, Requirements, Cost, Schedule, Documents);
   Detailed Description of Proposed Change; Justification for Proposed Change; Impacts of Change, five areas (Scope, Quality, Requirements, Cost, Schedule), each marked
   Increase, Decrease or Modify with a Description, and Table 3.3 asks whether the critical path changes under Schedule; Stakeholder Impact (High risk, Low risk, Medium
   risk) with a Description and Project Documents; Comments; on page 3 the Disposition (Approve, Defer, Reject) and its Justification. Prose: BoF 3.3 p170 to 171
   (PDF 181 to 182). Include cost, dates, resources and risks (PM 4.6.1.4 p117 (PDF 156)). Stakeholder Impact and Project Documents are not Increase, Decrease or Modify areas.
3. **Impact analysis.** Inputs: change management plan, configuration plan, baselines, basis of estimates, RTM, risk report, performance reports
   (PM 4.6.1 p116 to 117 (PDF 155 to 156)). Most changes touch time, cost, resources or risk (PM 4.6.2.5 p120 (PDF 159)).
4. **Decision.** Techniques of D06. CCB (formally chartered, roles in 2.2) reviews, then customer or sponsor approval unless they are in the CCB
   (PM 4.6 p115 (PDF 154); BoF 2.2 p25 (PDF 36)). Outcome approved, deferred or rejected, recorded on 3.3 Disposition and Justification (BoF 3.3 p174 (PDF 185)).
5. **Record.** 3.4 row: ID, Category (from 3.3), Description of Change, Requestor, Submission Date, Status (open, pending, closed), Disposition
   (BoF 3.4 p175 to 176 (PDF 186 to 187); blank p177 (PDF 188)); every disposition goes in the change log (PM 4.6.3.1 p120 (PDF 159)). The book opens the log entry
   with the request (Status open or pending) and completes it at the decision (Status closed, Disposition approved, deferred or rejected); the team's convention writes the row at the decision. The
   alternatives and reason go in 3.2 Comments.
6. **Communicate.** Deferred and rejected requests go back to the requester; CCB decisions are documented and communicated for follow-up (PM 4.6.2.5
   p120 (PDF 159)).
7. **Implement.** Approved requests are carried out by Direct and Manage Project Work (PM 4.6.3.1 p120 (PDF 159)); repairs are verified, retested and
   certified (PM 8.3.1.3 p301 (PDF 340)); a contract change is written and approved first (PM 12.3.1.5 p496 (PDF 535)).
8. **Update.** Change only the formally controlled plan components and documents the change touches; baselines change from the last baseline
   forward and past performance is not changed (PM 4.6.3.2 to 4.6.3.3 p120 (PDF 159)). Project convention: give each updated form a new Date Prepared and update forms
   that must agree (alignment lists in `knowledge/<form>.json`). Do not edit a baseline first and ask later.

Project rule, not book text: with no authority to absorb it, the answer to a constraint conflict is a 3.3 to the sponsor, never a trimmed estimate.

**While a 3.3 is pending.** The charter stays the baseline until the request is approved. The book says that once the project is baselined, change requests go through the change process
(PM 4.6 p115 (PDF 154)) and that baselines change only from the last baseline forward (PM 4.6.3.2 p120 (PDF 159)). The skill's reading, not a sentence of the book: a forecast, a levelled date or a
proposed figure in a pending 3.3 changes nothing until the request is approved. A second request on the same baseline is cross-referenced to the open
one in its Description; whether to amend the open request, replace it or fold the new one in is not stated in the book, so it is a CCB or sponsor decision recorded in 3.2 and
3.4, and the earlier request is never silently overwritten or duplicated.

## 5. Recommendation format

Present a decision in this order, in the user's language, plain text, no emoji, no em dash and no en dash (a hyphen inside a compound word or an ID such as
1.1.1.3-A1 is fine):

1. **Situation.** One or two sentences with the facts and where each came from (document and section). List the unknowns as questions.
2. **Constraint check.** Which of scope, schedule, cost, quality, resources, risk is binding; which baselines an option touches; whether the PM's
   authority covers it.
3. **Options.** A table: option, technique name with citation, the book's stated trade-off (or "not stated in the book"), baseline effect.
   For other decisions include the do-nothing and the change-request options when relevant. Never an option that shrinks an estimate. A risk response table has exactly the five threat
   strategies of D36 as rows, with the trade-off of each, and labels each part of a mixed response with the book's wording (isolation is avoid, PM p443 (PDF 482)); do nothing and the 3.3 route go on separate
   lines under the table. A compression table says what 2.18 or a 3.3 already used (D14 step 0), counting compression that exists only in a pending 3.3 as proposed.
4. **Recommendation.** One option and the reason tied to the situation. Mark judgment calls where the book gives no criterion. When the recommended action has a trigger-based fallback, add at most one
   contingency option after the recommendation, with its trigger and who decides; do not present three equal options.
5. **Calculator output.** Inputs, formula name, result, units, and the label "outside arithmetic aid" where the book states no formula.
6. **What the team must decide.** Each open question, who decides (PM, sponsor, CCB), and what the choice changes.
7. **Forms to update.** The form, the printed field, and the log entry (3.2 always; 3.3 and 3.4 when a baseline moves), the three forms to write first named first. Run `form_graph.py --impact <anchor> --depth 1` only on the anchor of the path chosen
   (section 2), and on 3.3 separately only when a baseline move is the recommendation or the question names 3.3; a row with no anchor (row 40) needs `forms-index.md` and `form_graph.py <form>` of the chosen form only. Name each form once across runs; quote that run's own count line, paste the forms that exist in `docs/` and the stand-in sections the run marks, name every other form the run prints as a form to
   create or update later (none dropped, none added: a form that is not in the output is not named), and for 3.3 state its "provides it" and recipient edges (2.2, 3.4, the change
   control board) even when they are not in `docs/`; if nothing exists, say "nothing to compare". Give the prose pages and the blank-form pages of a form separately, each with both numbers: 3.3 prose PDF 181 to 182
   (printed 170 to 171), blank PDF 183 to 185 (printed 172 to 174); 3.4 prose PDF 186 to 187 (printed 175 to 176), blank PDF 188 (printed 177). The impact run lists what the form provides to; for a form the question names,
   also give what it receives from (the "receives from" line the run prints, or `form_graph.py <form>`), so both directions are reported. Offer to draft them.
8. **Citations.** Every page mention in a reply needs the printed and the PDF number together ("p443 (PDF 482)"), also in a table cell or a pointer; a bare "p443" or a
   bare "PDF 181" is wrong. In Vietnamese write "trang in 215 (trang PDF 254)" (PM 6.5.2.6, "muc 6.5.2.6"). A claim about the book with no page gets "not stated in the book" and the section searched with both pages, never "the book prints no X" alone. `check_pages.py` flags a reply file that breaks this (errors for a bare page, warnings for a section with no page). Ask before writing any file.
9. **When you could not ask.** Put the questions first, then the conditional answer, then the assumed values labelled as assumed.
10. **Length.** Answer the question first. A narrow question (one status figure, which form) gets the result, the three forms to write first and the book citations, with one line offering the full impact list; the full
    seven-part format is for a decision that moves a baseline or asks for options. Do not repeat a form in several sections, and do not restate a table in prose.
11. **Reserve wording.** When a reserve is cited or a form carries a reserve figure, say in one line which reserve the budget line names and, if the charter's success criterion words it differently (for example "management reserve use"),
    report both wordings as a source error for the sponsor to resolve; copy neither as the other.

**Drafts.** A request such as "what do I write" or "what do I tell the sponsor" asks for the text in the reply, not for a file. For a message to the sponsor use five
lines: the decision needed; the options with their effects on scope, schedule and cost; the recommendation and why; the date the answer is needed by (ask the user,
never invent it); who signs. For a 3.3 draft, fill the printed fields in printed order (section 4, step 2), leave Requestor, Date Prepared and the page 3 Disposition
and Justification to the people who hold them, and leave any value the documents do not give empty or `[TBD]`. "What goes in form 4.4" is answered the same way: map each result to the printed label in the reply, and write no file unless asked.
