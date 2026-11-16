# The Agile Practice Guide and the adaptive sections of PMBOK 6, for forms 6.1 to 6.4

Read this before filling 6.1 Product Vision, 6.2 Product Backlog, 6.3 Release Plan or 6.4 Retrospective, or before
writing any "agile", "iteration" or "release" claim in another form. The Book of Forms says PMBOK 6 lists none of the
four as an output of a process, and only suggests where each is most useful (BoF Agile introduction, printed page 239
(PDF page 250)). So the content comes from three places: the Agile Practice Guide (second document in the PDF), the
"Considerations for Agile/Adaptive Environments" box in each PMBOK chapter 4 to 13, and the PMBOK sections that name
an agile technique. A remedy proposed to the team carries the book's name for its technique and its stated trade-off.

Citation shorthand, so each claim carries both numbers. `PM 6.5.2.8 p216 (PDF 255)` is a PMBOK 6 section, printed
page, PDF page (PDF = printed + 39). `APG 5.2.1 p50 (PDF 860)` is the Agile Practice Guide section, printed page, PDF
page (PDF = printed + 810). `BoF 6.3 p244 (PDF 255)` is a Book of Forms prose page (PDF = printed + 11; blank form
pages are in `forms-index.md`). A bare "6.3" is a Book of Forms form; PMBOK and APG sections always carry PM or APG.

## Where it is

`PMBOK6_and_Agile_Practice_Guide.pdf` holds PMBOK 6 (PDF 1 to 795) then the Agile Practice Guide (PDF 796 on).
The APG contents (roman pages i to iv, PDF 803 to 806) list printed page 1 as Introduction; PDF 811 shows that page,
so PDF = printed + 810 for the body, annexes, appendices and glossary (checked: PDF 817 is p7, 879 is p69, 960 is p150).
`pdftotext -layout` breaks both books: the APG watermark is noisier ("ctio n", "n,", "tio") and its sidebars interleave
with the body, so read a page with the Read tool when a sentence looks scrambled.

| APG section | Printed | PDF |
| --- | --- | --- |
| 2 Introduction to agile: 2.1 definable vs high-uncertainty work, 2.2 manifesto, 2.4 uncertainty and life cycle | 7 to 16 | 817 to 826 |
| 3 Life cycle selection: Table 3-1 p18; hybrids 3.1.6 to 3.1.11 p26 to 30; Table 3-2 tailoring p32 | 17 to 32 | 827 to 842 |
| 4 Agile environment: 4.2.2 role of the project manager p37; Tables 4-1, 4-2 (team, product owner) p40 to 41 | 33 to 47 | 843 to 857 |
| 5 Delivering: 5.1 charter 49; 5.2.1 retrospectives 50; 5.2.2 and 5.2.3 backlog 52; 5.2.5 and 5.2.6 55; Table 5-1 58 | 49 to 70 | 859 to 880 |
| 5.4 Measurements: burndown 62, velocity 64, earned value in agile 69 | 60 to 70 | 870 to 880 |
| 6.3 Procurement and contracts | 77 to 79 | 887 to 889 |
| Annex A1 PMBOK mapping: Table A1-2 is the per-chapter text | 89 to 95 | 899 to 905 |
| Annex A3 frameworks (Scrum A3.2, sprints of 1 month or less, p101) | 99 to 113 | 909 to 923 |
| Appendix X2 tailoring p119 to 124; X3 suitability filter tools p125 to 138; Glossary p149 to 155 | 119 to 155 | 929 to 965 |

| PMBOK 6 chapter | Tailoring considerations | Agile/adaptive considerations | Other agile text |
| --- | --- | --- | --- |
| 4 Integration | p74 (PDF 113) | p74 (113) | 1.2.4.1 life cycles p19 (58); plan holds the development approach, 4.2.3.1 p88 (127); sprint, standup, retrospective meetings 4.3.2.3 p95 (134) |
| 5 Scope | p133 (172) | p133 (172) | key concepts p131 (170); Define Scope per iteration p151 (190); user stories 5.2.2.6 p145 (184); epics to stories 5.4.2.1 p160 (199) |
| 6 Schedule | p178 (217) | p178 (217) | iterative scheduling with a backlog, on-demand scheduling p177 (216); release and iteration length 6.1.3.1 p182 (221); sprint planning 6.4.2.8 p203 (242); agile release planning 6.5.2.8 p216 (255); Control Schedule p224 (263), iteration burndown 6.6.2.1 p226 (265) |
| 7 Cost | p234 (273) | p234 (273) | none |
| 8 Quality | p276 (315) | p276 (315) | all team members, 8.2 p290 (329), 8.3 p300 (339); retrospectives 8.3.2.6 p305 (344) |
| 9 Resource | p311 (350) | p311 (350) | self-organizing teams, trends p310 (349) |
| 10 Communications | p365 (404) | p365 (404) | none |
| 11 Risk | p400 (439) | p400 (439) | Identify Risks is iterative p411 (450); qualitative analysis before each iteration p421 (460); reserve burndown 11.7.2.1 p456 (495) |
| 12 Procurement | p465 (504) | p465 (504) | APG 6.3 above |
| 13 Stakeholder | p506 (545) | p506 (545) | none |

Appendices: PM X1.9 p642 (681) says the Considerations boxes are new in the Sixth Edition; PM X3 "Agile, iterative,
adaptive, and hybrid project environments" p665 to 672 (704 to 711); PM X5 repeats the tailoring lists p679 to 684 (718 to 723).

## Key terms, with the book's meaning

- **Definable work** has proven procedures and low execution risk; **high-uncertainty work** is exploratory, with high
  change, complexity and risk, and predictive planning of the bulk of requirements up front strains (APG 2.1 p7 (817)).
- **Four life cycles** (APG Table 3-1 p18 (828)): predictive (requirements fixed, activities once, single delivery,
  goal manage cost); iterative (dynamic, repeated until correct, single delivery, goal correctness); incremental
  (dynamic, once per increment, frequent smaller deliveries, goal speed); agile (dynamic, repeated, frequent small
  deliveries, goal customer value). **Hybrid** combines them (APG 3.1.6 p26 (836); PM 1.2.4.1 p19 (58)).
- **Iteration**: a timeboxed cycle doing all the work needed to deliver value; **increment**: a functional, tested,
  accepted subset; **sprint**: Scrum's iteration (APG Glossary p152, p154 (962, 964)). The charter says "iteration".
- **Product backlog**: an ordered list of user-centric requirements; **product owner** maximizes product value and ranks
  the work by business value; **user story** is a brief description of value for a specific user; **epic**
  decomposes into stories (APG Glossary p153 to 155 (963 to 965); Table 4-2 p41 (851); PM 5.4.2.1 p160 (199)).
- **Backlog refinement** prepares stories for the next iteration (APG 5.2.3 p52 (862)); a **spike** is timeboxed
  research (APG 5.2.7 p56 (866)); **story points** rate relative work, risk and complexity (APG 5.4.1 p62 (872)).
- **Definition of ready** lets the team start a story; **definition of done** makes it ready for customer use (APG
  Glossary p151 (961)); **release criteria** are the project's own "done" (APG 5.1 p49 (859)).
- **Vision, roadmap, release plan, iteration plan** nest: vision drives roadmap, roadmap drives release plans, a release
  plan sets the iterations, an iteration plan schedules feature work (PM Figure 6-20 p216 (255)).
- **Retrospective**: a regular workshop to improve process and product; "the single most important practice" (APG
  Glossary p153 (963); 5.2.1 p50 (860)). **Starfish** is Start, Stop, Keep, More, Less; **FLAP** is Future
  Considerations, Lessons, Accomplishments, Problems (BoF 6.4 p246 (257)).
- **Project manager**: the expectations do not change, but control of detailed product planning and delivery goes to
  the team; the PM serves as a servant leader (PM 4 p74 (113); APG 4.2.3 p38 (848)).

## How the process outputs map onto the forms

BoF intro p239 (PDF 250) pairs each form with a process and a traditional partner. None has a PMBOK component list, so
each table below uses the partner's list and says which boxes it feeds. Use `references/fields/<form>.json` for labels.

**6.1 Product Vision with Develop Project Charter, PM 4.1.3.1 p81 (120), and APG 5.1 p49 (859).** The form prints four
stems; Table 6.1 names the elements in that order (BoF 6.1 p240 (251)).

| Printed stem (Table 6.1 element) | Draws on |
| --- | --- |
| We are developing this product for ____. (Target customer) | charter Key stakeholder list; APG 5.1 "Who benefits and how?" |
| To respond to the following need(s): (Needs) | charter Project purpose, objectives, high-level requirements; APG 5.1 "Why are we doing this project?" |
| This product responds to those needs by providing the following: (Product and key attributes) | High-level project description, boundaries, key deliverables; Table 6.1 adds functional, nonfunctional and top-level requirements |
| Customers will buy this product because: (Key benefit) | business case benefit (PM 4.1.1.1 p77 (116) input; charter Project purpose) |

No box: budget, milestones, risk, approval requirements, exit criteria, authority, sponsor, and APG 5.1 "What does done
mean?" and "How are we going to work together?" (release criteria and working agreements). They stay in 1.1 and 2.27;
a vision is not a substitute for them (decision 2).

**6.2 Product Backlog with Collect Requirements, PM 5.2.3.1 p147 (186) and 5.2.3.2 p148 (187), and APG 5.2.2 p52 (862).**
Columns ID, Summary Description, Priority, Story, Status (BoF 6.2 p242 (253)). Prose: "tracks ... the release they will
be incorporated into", yet the blank form prints no release column.

| Needed | Where it goes |
| --- | --- |
| Release or iteration of each item | Tailoring Tips add a sprint column (BoF 6.2 p242 (253)); name the added column in the reading paragraph |
| Story points, user type, category | Same Tailoring Tips, as added columns |
| Source, acceptance criteria, owner, verification, requirement class (business, stakeholder, solution, transition, project, quality; PM 5.2.3.1 p147 to 148 (186 to 187)) | No box; keep them in 2.6 and 2.7, and cite the ID |
| User story text | Story column, or the name of a story kept elsewhere (Table 6.2) |

**6.3 Release Plan with Plan Schedule Management, PM 6.1.3.1 p182 (221), and Agile release planning, PM 6.5.2.8 p216 (255).**
Prints Project Name (not Project Title), Release Goal, Sprint 1 to Sprint 4 columns, Team 1 to Team 4 lanes, User Story
notes. No box for the release dates that Table 6.3 lists, no date prepared, no page footer.

| Needed | Where it goes |
| --- | --- |
| Release dates (a timeline or milestone marker, Table 6.3) | Reading paragraph, or the Tailoring Tips timeline; milestones stay in 2.14 |
| Release and iteration length (PM 6.1.3.1 p182 (221)) | 2.11 Schedule Methodology; the sprint columns of 6.3 show the result |
| Release schedule, typically 3 to 6 months (PM 6.5.2.8 p216 (255)) | 6.3 columns; the full schedule is 2.18 |
| Lanes by team or work stream (Tailoring Tips) | Rename lanes in the reading paragraph; do not print invented team names |

**6.4 Retrospective with Manage Project Knowledge, PM 4.4.3.1 p104 (143), and APG 5.2.1 p50 (860).** Boxes Start, Stop,
Keep, More, Less (BoF 6.4 p246 (257)). The 4.4.3.1 register holds category, description, impact, recommendations and
proposed actions: those are 3.5's columns, not 6.4's. No box for the iteration or date, the owner of an action, or how
the improvement will be measured (APG 5.2.1 p51 (861)); put them in the reading paragraph or carry the chosen
actions to 3.5. A FLAP layout, or colour coding by technical, process, people, environment, is tailoring to name.

## Where this project's facts live

No project document under `docs/` holds a vision, backlog, release plan or retrospective, or uses the words story,
backlog, sprint or retrospective. Do not invent them; build each from the sources below.

| Fact | Where |
| --- | --- |
| Product, need, benefit (6.1) | Charter Part 2A Project purpose with its business case table; 1.1.1 problem, 1.1.2 product, 1.1.3 users and roles, high-level requirements; customer is the Center Director (Key stakeholder list) |
| Requirement items (6.2) | Scope package Part 1: BR01 to BR07, FR01 to FR12, NFR01 to NFR12; charter 1.1.4 (F01 to F12), 1.1.5, 1.3 (A01 to A12). Every item is Must have, so Priority carries no order |
| Release content (6.3) | Charter D3 (F01 to F05) and D4 (F06 to F12), summary milestone schedule M0 to M7; Part 3 of the scope package, phases 1.4 and 1.5 (control accounts 1.4.1, 1.4.2, 1.4.4, 1.5.1 to 1.5.4), phase 1.9 |
| Iteration dates | Dictionary Due Dates of the iteration packages (phases 1.4 and 1.5); every package of an iteration is due at its end; read the dates there |
| Dates that may move | `docs/forms/2-18-project-schedule.en.md` levelled forecast; `docs/forms/3-3-change-request.en.md` is undecided, so build from the baselined charter and name the rows that would change |
| Who accepts an iteration | Charter Project approval requirements: Academic Manager, Accountant, Front-desk supervisor; Head Teacher for F12; signed demo acceptance record at M3 and M4 |
| Authority over iteration content | Charter authority section, Technical decisions: PM "decides the content of each iteration within the approved scope"; user-visible scope, schedule, cost go to the sponsor |
| Capacity and risks | Charter Resources preassigned (full-time and part-time people, with the part-time person's window); the risks whose responses shape the iterations (read R2, R7, R9, R12 as written); the reserve budget line |
| Lessons learned | Only 1.10.2.1 (closeout report, lessons learned, D10); no package names a retrospective, refinement or release planning |

## Traps

- **Three "6"s.** BoF forms 6.1 to 6.4 are the Agile group; PMBOK 6 is Schedule Management; APG Section 6 is
  Organizational Considerations. **Two "Appendix X3"s**: PM X3 is agile, iterative, adaptive and hybrid environments
  (p665 (704)); APG X3 is the suitability filter tools (p125 (935)), and APG 3.1 p18 (828) points at the PM one.
- APG p55 (865) and p60 (870) cite "Section 4.10" for value management and examples; the APG contents end section 4 at
  4.3.7 (contents, roman page ii (PDF 804)). Do not cite 4.10.
- **Considerations boxes advise, they do not require** ("often", "may", "can"): write "PMBOK 6 notes", not "requires".
- **The charter is a hybrid, not agile.** Requirements are baselined at M1, rules frozen (R2), change goes to the sponsor,
  payment follows signed acceptance, and UAT is one system-level pass. By PM 1.2.4.1 p19 (58) predictive for what is
  fixed and adaptive for what is evolving is hybrid; by APG 3.1.7 p27 (837) calling that "agile" would mislead.
- **Four-week iterations, one demo each.** Guideline: demonstrate at least every two weeks (APG 5.2.5 p55 (865));
  Scrum's sprint is 1 month or less (APG A3.2 p101 (911)). Do not print a two-week sprint in 6.3; none is planned.
- **Velocity needs history.** A stable velocity can take four to eight iterations (APG 5.4.1 tip p64 (874)); this
  project has two build iterations and no recorded velocity. Do not forecast by velocity or write story-point totals.
- **Two SPIs.** PM 7.4.2.2 p263 (302) defines SPI = EV/PV in money; APG p69 (879) defines it on features. Say which
  basis a report uses; form 4.4 prints PV, EV, AC rows in money.
- **Priority.** Every RTM row is Must have, so copying it into 6.2 gives one value in every row. Table 6.2 allows a
  rank 1, 2, 3 or high, medium, low; the order is a decision (decision 3), shown as marked.
- **Retrospective cadence.** BoF 6.4 p246 (257) says "end of every sprint"; with two iterations that is two, plus
  any the team adds (APG 5.2.1 p51 (861)). It feeds 3.5 and 5.1; it is not them. Capacity differs by iteration (the
  mobile developer leaves after M5): plan only what fits (APG 5.2.6 p55 (865)).

## Decisions in this area

Citations as above. "Record" names the printed form and box; a decision with no Formula line has none in the book.
A change to the charter's milestones, scope or cost goes through 3.3 Change Request to the sponsor and is logged in
3.2 and 3.4; that is the project rule and the charter's authority section, not an APG rule.

### Decision 1 Development approach for the project and each deliverable, and tailoring a practice
- **When:** Develop Project Charter and Plan Scope Management; again when an area proves unstable (PM 5 p133 (172)).
- **Techniques and trade-offs:** APG Table 3-1 p18 (828) and the continuum p19 (829). Predictive: low uncertainty, but
  value arrives at the end and change costs (APG 3.1.1 p20 (830)). Iterative: feedback improves unfinished work but may
  take longer, "optimized for learning rather than speed" (3.1.2 p21 (831)). Incremental: usable subsets sooner
  (3.1.3 p22 (832)). Agile: both, earlier return (p19 (829)). Hybrids: APG 3.1.6 to 3.1.9 p26 to 28 (836 to 838).
  **Suitability filter** (APG X3 p125 to 138 (935 to 948)): nine questions on culture, team and project, scored 1 to
  10 by the group, plotted on a radar chart; centre is agile, middle hybrid, outside predictive; the text gives no
  numeric zone limit; it is a discussion tool, "should not be used as definitive inclusion or exclusion gates" (X3.6 p138 (948)).
  Tailoring a practice: use the approach as designed first, tailor after success with it (X2.2 p119 (929)), trial a
  change for an iteration or two and judge it at a retrospective (X2.3 p120 (930)), "beware of taking things away"
  (X2.4.1 p121 (931)); premature, haphazard tailoring "can minimize the effects of the approach" (APG 2.2 p12 (822)).
- **Inputs:** charter 1.5 constraints (fixed budget and dates), the high-level description ("Delivery is iterative: two
  build iterations ... followed by UAT"), R2, R7, approval requirements. No filter scores exist; ask the team.
- **Record:** 2.1 Development Approaches (Deliverable, Development Approach) and Project Life Cycle; 2.27 Team Charter
  (Other Agreements) for tailored practices; 3.2 Decision Log.
- **Wrong move:** agile for its own sake, "agile for the sake of agile" (APG 3.1.10 p29 (839)); calling a
  plan agile while estimation, assignment and tracking stay predictive (APG 3.1.7 p27 (837)); or dropping retrospectives
  as unpopular, which the APG says removes the activity that improves the process (X2.2 p119 (929)).

### Decision 2 Which of 6.1 to 6.4 to produce, and whether each replaces its traditional partner
- **When:** Develop Project Charter, Collect Requirements, Plan Schedule Management, Manage Project Knowledge (BoF p239 (250)).
- **Techniques:** the book says "may": 6.1 before or instead of a charter on smaller projects; 6.2 in place of or in
  addition to requirements documentation; 6.3 in place of a schedule management plan or as a high-level schedule on
  small projects; 6.4 in place of or in parallel with the lessons learned register. No trade-off is stated.
- **Inputs:** 1.1 charter (signed form 2B), 2.6, 2.7, 2.11, 2.18, 3.5 exist or are planned; scope package Part 1.
- **Record:** the italic reading paragraph of each form, and 3.2.
- **Wrong move:** letting 6.1 stand in for the charter here. The charter "formally authorizes the existence of a project"
  and carries budget, approval requirements, exit criteria and authority (PM 4.1.3.1 p81 (120)); a vision has none.

### Decision 3 Order of the backlog, and what enters the next iteration
- **When:** before each iteration: refinement (APG 5.2.3 p52 (862)), planning (APG 5.2.6 p55 (865); PM 6.4.2.8 p203
  (242)); trigger: iteration start, a new request, a risk change.
- **Techniques:** the product owner ranks by business value (APG Table 4-2 p41 (851)); rank by "cost of delay divided
  by duration (CD3)" for badly ordered items (Table 5-1 p59 (869)); consider risk when choosing content (PM 11 p400
  (439)); fit to capacity (APG 5.2.6 p55 (865)); spike an unclear dependency (APG 5.2.3 p53 (863)). Detailed scope is
  approved at the start of each iteration (PM 5 p131 (170)); the book states no trade-off between ranking models.
- **Inputs:** RTM priorities (all Must have, so no order), the split into deliverables D3 and D4, R7. Who is the product owner is not
  recorded: ask. The charter gives the PM the content of each iteration within approved scope; Academic Manager is
  "main requirement source and UAT lead", which is not ordering authority.
- **Record:** 6.2 Priority and Status; 3.2 for the ranking rule. Moving a function across the D3 and D4 deliverable line changes
  what a signed milestone covers: 3.3 to the sponsor.
- **Formula:** CD3 = cost of delay / duration (the APG prints the words; units not stated).
- **Wrong move:** no product ownership; the team "may create features that are not appreciated" and waste effort
  (APG Table 4-2 p41 (851)). Over-preparing is the other sign: refinement above about 1 hour a week (APG 5.2.3 p53 (863)).

### Decision 4 Iteration length, demonstration cadence, and what each release holds
- **When:** Plan Schedule Management ("Release and iteration length", PM 6.1.3.1 p182 (221)); release content after the
  vision and backlog are started and after each iteration (BoF 6.3 p244 (255)).
- **Techniques and trade-offs:** time-boxing forces essential features first and limits scope creep (PM 6.1.3.1 p182
  (221)); demonstrate at least every 2 weeks as a general guideline (APG 5.2.5 p55 (865)); Table 3-2 p32 (842): use a
  cadence for steady or sporadic demand. Repeating the process groups per iteration "incurs overhead" (PM X3.2.1 p667
  (706)). Agile release planning (PM 6.5.2.8 p216 (255)): a release is typically 3 to 6 months, iterations per release
  from business goals, dependencies, impediments; rolling wave planning (PM 6.2.2.3 p185 (224)). Trade-off: sprint
  content is fixed once it starts (BoF 6.3 p244 (255)).
- **Inputs:** two 4-week iterations in the dictionary, one gate each; charter M3 and M4, M5 (UAT entry, app submitted),
  M6 (go-live), pilot F01 to F06 two weeks before M6; the levelled forecast moves the dates; the backlog.
- **Record:** 2.11 Schedule Methodology (no box for iteration length); 6.3 Release Goal and sprint columns; 2.14; 2.18.
- **Wrong move:** no demonstration for four weeks, since "a team that does not demonstrate or release cannot learn fast
  enough" (APG 5.2.5 p55 (865)); or moving M3, M4 or M6 through the release plan, when a baseline changes only by
  formal change control (PM 6.5.3.1 p217 (256)).

### Decision 5 Estimating and forecasting
- **When:** iteration planning breaks stories into tasks in hours and checks them against capacity (PM 6.4.2.8 p203
  (242)); cost estimates are lightweight when scope is undefined, detailed only for the short term (PM 7 p234 (273)).
- **Techniques and trade-offs:** relative estimation with story points, splitting stories, spiking (APG Table 5-1 p58
  (868)); velocity (p64 (874)). Relative estimates cannot compare teams or add velocity across teams (p67 (877)).
- **Inputs:** dictionary hours and rates (scope package roll-up); no story points exist.
- **Record:** 6.2 (estimate column is a Tailoring Tip); 2.16, 2.20 keep the hour and cost estimates; 3.2.
- **Formula:** velocity = sum of the story point sizes of the features actually completed in this iteration (APG 5.4.1
  p64 (874)). Worked examples, not equations: 500 points left at 50 points an iteration is about 10 iterations; 30
  stories at a 3-day average cycle time is 90 business days (p61 (871)).
- **Is the release date at risk.** Run `pm_calc.py velocity --completed <points per iteration...> --remaining <points>`: it prints each
  iteration's velocity, the average, and the iterations remaining as the Guide's worked example computes them (an outside arithmetic aid; the
  Guide prints the definition and an example, not an equation). The Guide's tip: it can take four to eight iterations to reach a stable
  velocity (APG p64 (874)), and the tool says so when fewer are given. Compare the iterations remaining with the iterations left before the
  charter date; a shortfall is a forecast, and a baseline moves only by a 3.3. Rank what stays in by `pm_calc.py cd3` (cost of delay
  divided by duration, APG Table 5-1 p59 (869)), with the numbers supplied by the product owner. Routing: decisions.md row 36.
- **Wrong move:** cutting estimates to fit. PM 7 p234 (273) names scope and schedule, not the estimate, as what is
  "more often adjusted" under a strict budget; on this project that is a change request (3.3), not a quiet trim.

### Decision 6 A new or changed requirement: reprioritize or raise a change request
- **When:** Control Scope and Perform Integrated Change Control; a request or defect arrives.
- **Techniques:** adaptive work keeps one backlog for work and change, ordered by the business representative with
  the team's technical input (PM X3.3.4 p671 (710)); a predictive baseline changes only through change control (PM 5
  p131 (170)). Trade-off: the single backlog arose where very high change overwhelmed any attempt to separate change
  requests from planned work (PM X3.3.4); none is stated for the formal route.
- **Inputs:** charter success criterion "no function deferred without an approved change request"; PM authority;
  the reserve and the limit above which its use goes to the sponsor, both read from the charter (and marked assumed where the charter marks them).
- **Record:** 6.2 Status; 3.3, 3.4, 3.2 for anything touching scope, schedule or cost.
- **Wrong move:** swapping stories in and out silently because agile "welcomes change"; the baseline changes only by
  formal change control (PM 6.5.3.1 p217 (256)).

### Decision 7 Which progress measures to report
- **When:** each iteration and each weekly report (charter: status weekly); Control Schedule (PM 6.6 p224 (263)).
- **Techniques and trade-offs:** iteration burndown (PM 6.6.2.1 p226 (265)); burnup shows scope change (APG p63 to 64
  (873 to 874)); burndown can dispirit the team and prompt rushing past acceptance criteria (p63 (873)); flow
  measures lead, cycle, response time (p64 (874)); earned value on finished features (p67 (877)). Percent done and
  traffic lights hide a "watermelon" project (p60 (870)).
- **Inputs:** none recorded; charter targets: no milestone more than 1 week late, variance within plus or minus 5% at
  each stage gate.
- **Record:** 4.2 Project Status Report; 4.4 Earned Value Analysis Report; 4.3 Variance Analysis.
- **Formulas:** in agile terms, SPI = completed features / planned features and CPI = earned value / actual costs, EV
  being the value of completed features to date (APG Figure 5-6 and text p69 (879)); example 25 of 30 points is
  25/30 = 0.83, and $2.2M / $2.8M = 0.79. PMBOK: CPI = EV/AC, SPI = EV/PV (PM 7.4.2.2 p263 (302)).
- **Wrong move:** measuring story points without finished features; it measures capacity and breaks "working product is
  the primary measure of progress" (APG p66 (876)).

### Decision 8 Retrospective: when, how many actions, what carries on
- **When:** each iteration end; also at a release, after more than a few weeks, when work is stuck, or at a milestone
  (APG 5.2.1 p51 (861)); PM 8.3.2.6 p305 (344).
- **Techniques and trade-offs:** starfish or FLAP (BoF 6.4 p246 (257)); data, then root causes, countermeasures, action
  plan; limit actions to team capacity and measure each (APG 5.2.1 p51 (861)); capture no more than three items (Table 5-1
  p59 (869)). Trying too many improvements and finishing none is "much worse" than fewer completed (p51).
- **Inputs:** nothing recorded; no package funds one, so state where its time sits or raise a change request.
- **Record:** 6.4 columns; chosen actions to 3.5 (Lesson, Responsible Party); 5.1 and 5.2 at closeout.
- **Wrong move:** a blame session (APG 5.2.1 p51 (861): "not about blame").

### Decision 9 Ready, done and acceptance of an iteration release
- **When:** each demonstration; Validate Scope is repeated per iteration (PM 5 p131 (170)).
- **Techniques:** the team defines "done" with acceptance criteria and adds release criteria; "ready" for refined
  stories (APG Table 5-1 p58 (868); 5.1 p50 (860)); the product owner accepts or declines stories at the demonstration
  (APG 5.2.5 p55 (865)).
- **Inputs:** A01 to A12 (charter 1.3); dictionary Acceptance Criteria rows; M3 gate "no open Critical or High defect in
  F01 to F03" (1.4.3.2); approvers in the charter table.
- **Record:** 4.9 Formal Acceptance Form (Acceptance Criteria, Validation Method, Sign-off); 2.27 Team Charter; 6.2 Status.
- **Wrong move:** calling work done below its acceptance criteria to meet the burndown (APG p63 (873)).

### Decision 10 Risk per iteration and the reserve
- **When:** qualitative analysis before each iteration (PM 11.3 p421 (460)); risks identified, analysed and managed in
  every iteration (PM 11 p400 (439)); reserve analysis each period (PM 11.7.2.1 p456 (495)).
- **Techniques:** pick iteration content by risk exposure; spike for unknown dependencies (APG 5.2.3 p53 (863)); compare
  contingency reserve left with risk left, shown as a burndown (PM p456 (495)). Response strategy choice is PM 11.5
  and is unchanged by agile; not covered here.
- **Inputs:** the charter risk register and the budget line for the contingency reserve, read at the time.
- **Record:** 2.32; 2.31 Frequency and Timing (state "before each iteration"); 3.3 per reserve draw.
- **Wrong move:** analysing risk only at the start; the PM chapter says it is repeated each iteration (p400 (439)).
