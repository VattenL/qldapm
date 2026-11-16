# PMBOK 6 chapter 13, Project Stakeholder Management, for the stakeholder forms

Read this before filling 1.3 Stakeholder Register, 1.4 Stakeholder Analysis, 2.40 Stakeholder Engagement Plan or
3.1 Issue Log. Chapter 13 gives no component list for the engagement plan and no field list for the issue log, so
those boxes come from the Book of Forms tables. The last section lists the decisions a project manager makes here,
with the PMBOK technique names a proposed remedy has to carry.

## Where it is

`PMBOK6_and_Agile_Practice_Guide.pdf` at the repo root. Guide part: PDF page = printed page + 39. Short form used
from here on, so every claim keeps both numbers: **p507/546** is PMBOK 6 printed page 507, PDF page 546; **BoF
2.40 p158/169** is Book of Forms form 2.40, printed page 158, PDF page 169 (PDF = printed + 11). Contents pages:
PDF page 16. Chapter 13 is wholly in the Guide part.

| Section | Printed / PDF page |
| --- | --- |
| 13 Overview, Figure 13-1, key concepts, trends, tailoring, agile/adaptive | 503 to 506 / 542 to 545 |
| 13.1 Identify Stakeholders (inputs 509 to 510/548 to 549; techniques 511 to 514/550 to 553; outputs 514 to 515/553 to 554) | 507 to 515 / 546 to 554 |
| 13.1.3.1 Stakeholder register (its content list) | 514 / 553 |
| 13.2 Plan Stakeholder Engagement (update triggers 518/557; techniques 520 to 522/559 to 561; matrix and Figure 13-6 521 to 522/560 to 561) | 516 to 522 / 555 to 561 |
| 13.2.3.1 Stakeholder engagement plan (one paragraph, no component list) | 522 / 561 |
| 13.3 Manage Stakeholder Engagement (techniques 526 to 528/565 to 567; outputs 528 to 529/567 to 568) | 523 to 529 / 562 to 568 |
| 13.4 Monitor Stakeholder Engagement (techniques 533 to 535/572 to 574; outputs 535 to 536/574 to 575) | 530 to 536 / 569 to 575 |
| Related, outside the chapter: 4.3.3.3 Issue log, 4.3.3.4 Change requests | 96 / 135 |
| Related: 9.5.2.1 Conflict management (five techniques) | 348 to 349 / 387 to 388 |

Book of Forms, prose pages then blank pages, as printed / PDF:

| Form | PMBOK process | Prose | Blank form |
| --- | --- | --- | --- |
| 1.3 | 13.1 (output) | 12 to 13 / 23 to 24 | 14 / 25 |
| 1.4 | 13.1 (tool: stakeholder analysis) | 15 / 26 | 16 / 27 |
| 2.40 | 13.2 (output) | 158 to 159 / 169 to 170 | 160 to 161 / 171 to 172 |
| 3.1 | 4.3 (output); chapter 13 reads and updates it | 165 to 166 / 176 to 177 | 167 / 178 |
| 3.2 Decision Log, 3.3 Change Request | route for decisions and changes | 168 / 179; 170 to 171 / 181 to 182 | 169 / 180; 172 to 174 / 183 to 185 |

`pdftotext -layout` interleaves a vertical watermark of 1 to 3 letter lines and a "PMI Member benefit" footer;
drop them before reading. "Chapter 13" for a stakeholder form means PMBOK 6, not the lecture notes.

## Chapter 13 terms, with the book's meaning

- **Stakeholder** (glossary p723/762; section 1.6 of the Standard, p550/589): an individual, group or
  organization that may affect, be affected by, or perceive itself to be affected by a decision, activity or
  outcome. May be internal or external, actively or passively involved, or unaware of the project.
- **Iterative** (p505/544): identification, prioritization and engagement are described once but reviewed
  routinely, at least at a phase change, when stakeholders join or leave, and on significant organizational change.
  Start "as soon as possible after the project charter has been approved" (p504/543).
- **Stakeholder analysis** (13.1.2.3, p512/551): yields a list of stakeholders with position, role on the project,
  "stakes", expectations, attitudes (levels of support) and interest in information. A stake is a combination of
  interest, rights (legal or moral), ownership, knowledge and contribution.
- **Stakeholder mapping** (13.1.2.4, p512 to 513/551 to 552): power/interest, power/influence or impact/influence
  grid; stakeholder cube (grids combined in three dimensions); salience model (power, urgency, legitimacy, or
  proximity for the team); directions of influence (upward, downward, outward, sideward); prioritization.
- **Engagement levels** (13.2.2.5, p521/560): unaware, resistant, neutral, supportive, leading, as BoF Table 2.36
  (p159/170) repeats. **Stakeholder engagement assessment matrix** compares current (C) with desired (D)
  (p521 to 522/560 to 561); D is the level "the project team has assessed as essential to ensure project success".
- **Engagement gap** (p522/561): the gap between C and D "will direct the level of communications necessary";
  closing it is "an essential element of monitoring stakeholder engagement". No numeric gap is defined.
- **Issue** (BoF 3.1 p165/176): a current condition that could affect the objectives, a point in dispute, or a
  risk event that has occurred and must now be dealt with. PMBOK 4.3.3.3 (p96/135): problems, gaps,
  inconsistencies or conflicts that occur unexpectedly and require action.

## How each process output maps onto the forms

A component with no box goes in the nearest box and is named in the italic reading paragraph above the form,
never inside the form. Placements marked "judgement" are this note's reading, not the book's.

**1.3 from 13.1.3.1** (p514/553; boxes per BoF Table 1.3, p13/24; blank form p14/25 prints six columns, no ID).

| PMBOK 13.1.3.1 content | Form 1.3 box |
| --- | --- |
| Identification: name; organizational position; role on the project | Name (a position or organization may stand in until the name is known); Position/Role |
| Identification: location and contact details | Contact Information (Table 1.3 names phone, email, physical address); location has no box of its own, judgement: inside Contact Information |
| Assessment: major requirements; expectations | Requirements (high-level needs); Expectations (main expectations) |
| Assessment: potential for influencing outcomes; phase of the life cycle with the most influence or impact | No box. Influence lives in 1.4; the phase is a named tailoring or goes in Expectations, judgement |
| Classification: internal/external, impact/influence/power/interest, upward/downward/outward/sideward, or another model | Classification (Table 1.3 examples: friend, foe, neutral; or high, medium, low impact). Fill from 1.4 |

**External suppliers (Apple, Google, the push or gateway provider, the host).** Take Requirements and Expectations only from a charter assumption, risk,
budget line or exclusion that names the party, copied as written; otherwise leave the box empty or `[TBD]` and say in the reply that no source states it.
Never write a dependency in your own words ("needs the gateway to be stable") and never reword it as a requirement. Splitting one source sentence between
the two boxes: Requirements takes the high-level need (what the party must provide or do), Expectations takes the main expectation of the project towards
it (when, how well); Table 1.3 prints "high-level needs" and "main expectations" (BoF Table 1.3 p13 (PDF 24)). Worked example from assumption 12 ("One SMS and email gateway account is provided and paid for by the center, and its API is stable and documented"): for the
gateway provider, Requirements copies the clause "its API is stable and documented" and Expectations stays empty, because the assumption states the need and not a main expectation;
the account being paid for by the center is the center's obligation and goes on the center's row, not here. Ratings in Classification stay empty or inside `<mark>` (house-style.md).

**Internal stakeholders (the center's own staff and the sponsor).** The same rule, with the objectives as the extra source. Requirements takes the high-level need that the
charter's objectives, success criteria or function list state for the group by name, copied as written; Expectations takes an expectation the charter states for
that group (the sponsor's expectations come from the objectives and success criteria the sponsor signs). When the charter states neither for a group, leave the box
empty or `[TBD]` and ask; do not derive a need from what the role does. The user-role table (charter 1.1.3) says what a role does, not what it needs (BoF Table 1.3
prints "high-level needs", p13 (PDF 24)), so it is a source for the Name and Position/Role boxes only. The RTM Source column (scope package Part 1, form 2.7) names who asked for each requirement, so it is a source of
Requirements for a group whose role name matches a register row exactly, copied as written; when the RTM names a role the register spells differently or lacks, leave Requirements empty and ask, and match nothing by guess. A title the user gives that the charter does not use
("front-desk supervisor", "head teacher") is not mapped to a charter role: ask which charter role it is, or keep the user's title and mark it. A requirement that names no
stakeholder belongs to no row; list it as a question. Objectives that name no group are not a requirement of any one row.

Inputs 13.1.1 names: charter (key stakeholder list), business case and benefits management plan, communications
and engagement plans, change log, issue log, requirements documentation, agreements (the parties are
stakeholders), EEF, OPA (p509 to 510/548 to 549). BoF 1.3 p12/23 lists charter and procurement documents; the
register also "receives" from 1.4 (BoF 1.3 p13/24 Alignment: charter, 1.4, 2.40).

**1.4 from 13.1.2.3 and 13.1.2.4.** Stakeholder analysis is a tool of 13.1, not an output (BoF 1.4 p15/26), so the
book makes no output claim for the form. Boxes per BoF Table 1.4 (p15/26); blank form p16/27 prints four columns.

| PMBOK content | Form 1.4 box |
| --- | --- |
| The list of stakeholders | Name or Role (name, organization or group) |
| Interest (a stake); concern about outcomes | Interest (level of concern for the project) |
| Power, authority, influence, ability to cause change | Influence (degree to which the stakeholder can drive outcomes); the book's prose example says "power" and the table says Influence |
| Attitudes (levels of support) | Attitude (degree of support); the prose example rates friend or foe |
| Rights, ownership, knowledge, contribution; urgency, legitimacy, proximity; direction of influence; the grid or cube picture | No box (the blank form prints only the table). A named tailoring, or the 1.3 Expectations text, judgement |

**2.40 from 13.2.3.1 and 13.2.2.5.** 13.2.3.1 (p522/561) is one paragraph: a component of the project management
plan, "formal or informal and highly detailed or broadly framed", that "may include" strategies or approaches for
individuals or groups. It lists no components. The boxes follow BoF Table 2.36 (p159/170) and the blank form
(p160 to 161/171 to 172), which prints no heading over the first table.

| Source | Form 2.40 box |
| --- | --- |
| 13.2.2.5 matrix, Figure 13-6 (p522/561); BoF "desired and current engagement level of key stakeholders" (p158/169) | First table: Stakeholder, then C and D marked under Unaware, Resistant, Neutral, Supportive, Leading; the legend prints below it. Where C and D coincide, Figure 13-6 puts both letters in one cell |
| BoF "scope and impact of change to stakeholders" (p158/169); Table 2.36 "Stakeholder changes" | Pending Stakeholder Changes (pending additions, deletions, changes, with the impact) |
| BoF "interrelationships and potential overlap" (p158/169) | Stakeholder Relationships; a relationship map is a tailoring tip (p158/169) |
| 13.2.3.1 "strategies or approaches" | Stakeholder Engagement Approach (Stakeholder, Approach) |
| BoF "methods for updating and refining the plan" (p158/169); triggers p518/557 | No box; say in the reading paragraph when the plan is revisited |
| Prioritization of stakeholders (13.2.2.4, p521/560) | No box; the order of the rows, stated in the reading paragraph |

Receives from (BoF p158/169): charter, assumption, change and issue logs, register, resource, communications and
risk plans, schedule, risk register; 13.2.1 adds agreements, EEF (stakeholder risk appetites) and OPA (p518 to
520/557 to 559). Provides to: requirements documentation, quality plan, communications plan, register. Alignment:
register, communications plan, schedule (BoF p159/170).

**3.1 from 4.3.3.3** (p96/135; boxes per BoF Table 3.1, p166/177; blank form p167/178, two banks, no ID in bank 2).

| PMBOK 4.3.3.3 data | Form 3.1 box |
| --- | --- |
| Issue type; description; priority | Type; Issue Description; Priority |
| Who is assigned; target resolution date; status; final solution | Responsible Party; Res. Date (a target date, "date by which the issue needs to be resolved"); Status (open or closed); Final Resolution |
| Who raised the issue and when | No box; BoF tailoring tip "add information on the source of the issue" (p165/176) |
| Not in 4.3.3.3 | Issue ID; Impact on Objectives (which objectives, how much); Comments |
| Stakeholders affected or needed to resolve (resolving issues needs communication with the stakeholders affected, p519/558; p525/564) | No box; BoF tailoring tip adds a field (p165/176). Name it as a tailoring in the reading paragraph |

Other flows in chapter 13: each of 13.1, 13.3 and 13.4 may update the issue log (p515/554, p529/568, p536/575). 13.1
also updates the assumption log (power, interest and engagement are "based on assumptions"; constraints on dealing
with a stakeholder go there too) and the risk register, and may change the requirements, communications, risk and
engagement plans by change request (13.1.3.3, p515/554). 13.3 feeds the change log, issue log, lessons learned
register and stakeholder register (p529/568).

## Where this project's stakeholder facts live

List `docs/forms/` now, it is the truth (SKILL.md step 3): 1.3, 1.4, 2.40 and 3.1 are forms to create unless it holds them (the charter holds 1.3 as a stand-in section). Read, do not edit.

| Fact | Where |
| --- | --- |
| Key stakeholder list, 12 rows | `charter-package.en.md` Part 2A "Key stakeholder list" and form 1.1 page 3 "Stakeholder(s)" table. Two copies whose wording differs (gateway provider, Head Teacher); `house-style.md`: copy from 2B, name the copy, report the difference |
| Sponsor and customer are two people | Charter 2A "Name and authority of the sponsor", assumption 16; `review-lessons.md` section 1. Two rows, never merged. The PM is unnamed (assumption 15): write the position in Name, never a person |
| External parties no list names | `house-style.md` "External parties the project depends on" (Apple, Google); R12; budget line 2. Add a row for each |
| Stakeholder requirements and expectations | Charter 1.1.3 seven user roles (the 1.2.1.1 workshops run with them) and 1.1.4 functions by role; scope package Part 1 RTM Source column; objectives table row "Stakeholder satisfaction" with its criteria; BR07, NFR08 |
| Stakeholder assumptions | Charter 1.6: 1, 2 (52 staff users), 10 (Academic Manager and Accountant 4 hours a week), 16, 18 |
| Stakeholder risks and escalation | R3 (customer staff unavailable, escalate within 2 working days), R4, R9, R11 (benefit owner), R12; charter 2A authority level, "Conflict resolution": five working days, then the sponsor, whose decision is final |
| Interest, Influence, Attitude, C and D levels | Not recorded anywhere. `house-style.md`: leave empty, name the workshop or user as the source; a first pass derived by a stated rule goes in `<mark>` only if the user asks |
| Where the work sits | 1.2.1.1 workshops; 1.1.1.2-A2 "Communication and stakeholder plan" (16 hours, PM); 1.1.1.3 weekly status, escalations and "decision log"; 1.1.1.4 "run the issue log"; 1.8.2.2 training |
| Window of 1.1.1.2 (holds A2) | Dictionary: Mon 21 Sep to Fri 2 Oct 2026. Levelled `forms/2-18-project-schedule.en.md`: package 13 to 26 Oct, A2 19 to 21 Oct 2026, adopted only if the pending `forms/3-3-change-request.en.md` is approved. Build from the dictionary, report the difference |
| Stakeholder Impact on a change | `forms/3-3-change-request.en.md` page 2 marks High risk for the Center Director and business owners; that is the printed box to use for a stakeholder effect |

## Traps

- **13.2.3.1 has no component list.** Do not cite "PMBOK 13.2.3.1 lists" for the four 2.40 boxes. They come from BoF
  Table 2.36 (p159/170), and the blank form wins over the prose labels (fields note of 2.40).
- **Three different scales, never mixed.** 1.3 Classification (friend, foe, neutral, or impact levels), 1.4
  Attitude (support, friend or foe), 2.40 C and D (unaware to leading). A friend is not necessarily "leading".
  Say which scale each column uses.
- **Power, influence, impact.** BoF 1.4 prose says power, its table says Influence; PMBOK 13.1.2.4 (p512/551)
  gives power/interest, power/influence and impact/influence grids; 13.2.2.4 (p521/560) says "most interest and the
  highest influence". The book does not reconcile them. Use the printed label Influence and say what it means once.
- **Cross-reference slips in the chapter.** 13.4.2.3 (p534/573) points the matrix to "13.2.2.3"; it is 13.2.2.5.
  13.4.3.4 (p536/575) cites the lessons learned register as 4.3.3.1 and the stakeholder register as "13.1.12-13.1";
  13.3.1.2 (p525/564) gives 4.4.3.1 and 13.1.3.1. Cite the corrected sections.
- **3.1 Res. Date is a deadline** (BoF Table 3.1 p166/177), not the closing date; Status and Final Resolution show the
  close. 3.1 is an output of process 4.3 (BoF p165/176); chapter 13 only reads and updates it, and the book gives it
  no "provides to" list.
- **A pending change request does not change the baseline.** A new stakeholder or a stakeholder's request is a
  change request first (p514/553, p528/567); the register may be updated, the plan changes by request (p529/568).
- **Sponsor is not customer.** Separate rows with separate C and D; the sponsor funds, approves changes and
  accepts, the customer owns the need. Build 1.3 from the charter list plus the external parties, not from one copy.
- **Satisfaction figures are not engagement levels.** The book treats stakeholder satisfaction as a project objective
  (p505/544); the charter's criteria (80% of staff users trained, 4 of 5 survey average) are measures of it, not C or D marks.

## Decisions in this area

Chapter 13 states no equation, score, numeric gap, review interval or escalation time, so **formulas recorded:
none**. The project's own figures: an unresolved conflict goes to the sponsor after five working days (charter);
R3 and status escalations within 2 working days.

### 1. Who is a stakeholder, and when to run identification again

- **Arises:** 13.1; first before or with the charter, then "at the start of each phase and when a significant
  change" occurs (p508/547), and on the triggers of p505/544.
- **Techniques:** expert judgment (p511/550); questionnaires and surveys; brainstorming and brain writing
  (individual thought before the group session, p511/550); document analysis; meetings (p514/553). Cost or
  reach comparison: not stated in the book.
- **Inputs, kept in:** charter key stakeholder list, agreements (their parties are stakeholders), change and issue
  logs, requirements documentation (p509 to 510/548 to 549). Here: charter 2A and 1.1.3, house-style external
  parties, R12, budget line 2, 1.2.1.1 workshop notes.
- **Recorded in:** 1.3, one row per party; a change to a plan is a 3.3 first; assumptions go to charter 1.6.
- **Wrong move:** a one-time list copied from the charter. Reason: the process is iterative and "performed
  periodically" (p507/546, p505/544).

### 2. Which classification model, and how each stakeholder rates

- **Arises:** 13.1 stakeholder analysis and mapping (p512 to 513/551 to 552).
- **Techniques:** power/interest, power/influence or impact/influence grid, "useful for small projects or for
  projects with simple relationships" (p512/551); cube, a refinement that "improves the depiction of the
  stakeholder community as a multidimensional entity" (p513/552); salience model (power, urgency, legitimacy),
  useful for large complex communities and for "determining the relative importance" (p513/552); directions of
  influence. BoF 1.4 tailoring: 2 x 2 grid for homogeneous stakeholders, 3 x 3 cube for larger projects (p15/26).
- **Inputs, kept in:** charter, procurement documents, workshop notes. Here: nothing rated yet.
- **Recorded in:** 1.4 Interest, Influence, Attitude; 1.3 Classification (must agree, BoF p13/24); the basis in
  the assumption log, since such information is "based on assumptions" (p515/554).
- **Wrong move:** rating from memory. Reason: unsourced ratings are assumptions and belong in the assumption log
  (p515/554); `house-style.md` leaves them empty.

### 3. Which stakeholders to prioritise, and the desired engagement level

- **Arises:** 13.1.2.4 (p513/552); 13.2 decision making and matrix (p521 to 522/560 to 561), once the register exists.
- **Techniques:** prioritization/ranking, "may be necessary" with many stakeholders, changing membership or complex
  relationships (p513/552); those with the most interest and highest influence "are often prioritized at the top" (p521/560).
  Stakeholder engagement assessment matrix: D is the level "essential to ensure project success" and the gap "will
  direct the level of communications necessary" (p522/561). Scoring method, cut-off and the gap that needs action:
  not stated in the book. Risk thresholds and stakeholder risk appetites help choose the strategy mix (p518/557).
- **Inputs, kept in:** 1.3, 1.4, charter objectives and success criteria (p518/557), risk register owners and
  affected parties (p519/558), risk management plan. Here: R3, R11, R12.
- **Recorded in:** 2.40 first table, one C and one D per stakeholder (same cell when equal), row order stated in the
  reading paragraph, reason for D in the Approach box. **Formula:** none; the gap is a difference of levels on the
  printed scale, no number defined.
- **Wrong move:** D = Leading for everyone, or D left unset. Reason: D is what success needs, and with no D the gap
  that directs effort and that 13.4 tracks cannot be read (p522/561); the 13.1 benefit is "the appropriate focus for
  engagement" (p507/546).

### 4. The engagement approach for each stakeholder

- **Arises:** 13.2, carried out in 13.3.
- **Techniques:** root cause analysis ("underlying reasons for the level of support", p521/560); assumption and
  constraint analysis; benchmarking against world-class projects (p520/559); mind mapping; expert judgment. In 13.3:
  feedback, conflict management, cultural awareness, negotiation, observation/conversation, political awareness
  (p526 to 527/565 to 566), ground rules from the team charter (p528/567). Trade-offs: not stated in the book.
- **Inputs, kept in:** 1.3, 1.4, communications management plan (strategies are both input and recipient,
  p518/557), resource plan, schedule, change and issue logs.
- **Recorded in:** 2.40 Stakeholder Engagement Approach; actions in 2.30 and dates in 2.18 (both must agree,
  BoF p159/170).
- **Wrong move:** one generic approach. Reason: the plan rests on each stakeholder's "needs, expectations,
  interests, and potential impact" (p516/555), and the cause of low support differs per person.

### 5. How formal the plan is, and when it is revised

- **Arises:** 13.2; the tailoring tips of BoF 2.40 (p158/169).
- **Options:** formal or informal, detailed or broad (p522/561); a small project may fold the plan into the register;
  many stakeholders, complex interactions or high-risk stakeholders need a robust plan (BoF p158/169). Factors:
  diversity, complexity of relationships, communication technology (p506/545). Adaptive: engage directly and invite
  stakeholders to reviews (p506/545). Revise on four triggers: new phase; organization or industry change; new,
  departed or re-ranked stakeholders; outputs of change, risk or issue management (p518/557).
- **Inputs, kept in:** development approach (scope package "Decomposition method"); stakeholder count.
- **Recorded in:** 2.40 with a new Date Prepared (a change to the baselined plan goes by request, p529/568); the
  choice to fold it into 1.3 in 3.2; the reading paragraph names the tailoring.
- **Wrong move:** a plan written once. Reason: it is "reviewed and updated regularly as the stakeholder community
  changes" (p518/557).

### 6. How to respond when engagement is off plan

- **Arises:** 13.4, throughout (p530/569); trigger: work performance data (p532/571) read against D.
- **Techniques:** alternatives analysis (options to respond to variances); root cause analysis; stakeholder
  analysis (position of each now) (p533/572); multicriteria decision analysis (criteria "prioritized and weighted");
  voting (select the best response) (p534/573; voting types at p144/183, see `pmbok-scope.md`). Costs: not stated.
- **Inputs, kept in:** 2.40, 1.3, 3.1, lessons learned register, communications sent, risk register.
- **Recorded in:** 2.40, 1.3, 3.1, 2.32, 3.5 updated; work performance information compares C with D (p535/574);
  a corrective or preventive action is a change request, 3.3 (p535/574); 3.2 for a decision inside PM authority.
- **Wrong move:** a fix without the cause. Reason: root cause analysis finds "the basic underlying reason" that
  engagement is "not having the planned effect" (p533/572).

### 7. Does a stakeholder request or plan update need a change request

- **Arises:** 13.1.3.2, 13.3.3.1, 13.4.3.2 and every plan update (p514/553, p528/567, p535/574).
- **Rule:** all change requests go to Perform Integrated Change Control 4.6 (p528/567); the first identification
  yields none (p514/553); "any project stakeholder may request a change" (4.3.3.4, p96/135); managing engagement
  can surface scope changes (p528/567). Any change to the project management plan goes by change request (p529/568).
- **Inputs, kept in:** scope baseline (2.8 to 2.10), change log, charter authority ("anything that changes
  user-visible scope, the schedule, or the cost goes to the sponsor").
- **Recorded in:** 3.3 (Category, Impacts of Change, Stakeholder Impact, Disposition by the sponsor); then 3.4.
- **Wrong move:** absorbing the request or editing the baseline. Reason: the book routes every plan change
  through change control (p529/568); with constraints in conflict the route is a 3.3 to the sponsor.

### 8. What goes on the issue log, how urgent, who owns it, by when

- **Arises:** 4.3 creates the log (p96/135); 13.1, 13.3, 13.4 add to it; trigger: a current condition or dispute, or
  a risk event that has occurred (BoF p165/176).
- **Options:** priority examples urgent, high, medium, low (BoF Table 3.1, p166/177); no scale, threshold or
  response time is stated. One assigned person per issue; Res. Date is the deadline. Stakeholder concerns are logged
  with assigned action items (p525/564).
- **Inputs, kept in:** 2.32; status reports 4.1 and 4.2 (new issues also go on the log, BoF p192/203, p197/208);
  1.3 for who is affected. Here: owners and dates come from the sponsor and team; a new record is plain Open.
- **Recorded in:** 3.1; a baseline change from it is a 3.3; the decision in 3.2; the lesson in 3.5; 3.1 must
  agree with 2.32, 3.2, 3.5 (BoF p165/176).
- **Wrong move:** keeping a realised risk only in the risk register. Reason: an issue is a risk event that "has
  occurred and must now be dealt with" and the two logs must agree (BoF p165/176).

### 9. Handling a stakeholder conflict, and when to escalate

- **Arises:** 13.3, "conflicts resolved in a timely manner" (p527/566); sources: scarce resources, scheduling
  priorities, work styles (p348/387).
- **Techniques (p349/388):** withdraw/avoid (postpones); smooth/accommodate (keeps harmony, concedes);
  compromise/reconcile ("occasionally results in a lose-lose situation"); force/direct (win-lose, for an emergency);
  collaborate/problem solve (consensus, can be win-win); negotiation for "support or agreement" (p527/566). Order:
  early and usually in private; team members first, then the PM facilitates; formal procedures if disruption
  continues. Days before escalation: not stated in the book.
- **Inputs, kept in:** 3.1, 2.40, ground rules in 2.27. Here: charter 2A, five working days then the sponsor, and
  at once when the conflict crosses organizations or changes scope.
- **Recorded in:** 3.1 (Final Resolution), 3.2 (outcome), 2.40 Approach if the plan changes.
- **Wrong move:** forcing or avoiding by default. Reason: force is win-lose, avoidance only postpones, and the book
  wants conflict addressed early (p348 to 349/387 to 388).
