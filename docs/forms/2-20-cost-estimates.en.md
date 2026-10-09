# 2.20 Activity Cost Estimates

**Project:** Development and Deployment of a Learning Center Management Software
**Date prepared:** 8 October 2026
**Source:** A Project Manager's Book of Forms, 3rd edition, form 2.20, PDF pages 96 to 98 (printed pages 85 to 87), and form 2.21, PDF pages 99 to 103 (printed pages 88 to 92)

The cost estimate of PMBOK 6 section 7.2 Estimate Costs [1]: what each control account of the WBS costs in people, in physical resources, and in software, with the basis of every figure. Its inputs are the ones the book lists for form 2.20 [2]. The scope baseline gives the WBS and the hours of the WBS dictionary, less the work the scope change request defers; the project schedule is the levelling of form 2.18 run on that reduced work; the resource requirements are the resource on each dictionary activity; the risk register of the charter is carried through its contingency reserve. There is no separate cost or quality management plan: the rules below stand in for the first, and the test plan of 1.3.2.1 and the criteria A01 to A12 set the test hours the dictionary already carries. There is no lessons learned register yet, which is also why the analogous section of form 2.21 is empty. Its outputs are this form, its basis of estimates in form 2.21 and the references, and the updates it proposes to the scope baseline, the resource requirements, the assumption log, and the risk register, which the scope change request `3-3-change-request-scope.en.md` carries.

This is an estimate, not a budget. Determine Budget, PMBOK 6 process 7.3, adds the estimates up period by period into the cost baseline of form 2.22, and its funding limit reconciliation, section 7.3.2.5, is where an estimate is compared with the money available [1]. The charter makes 700,000,000 VND available, and the team set a target of 650,000,000 to keep a margin under it. The full scope cannot meet it, 900,165,000 VND under the same rules, so the scope and the way the work is staffed were reduced until it could; the change request puts that reduction to the sponsor. The earned value formulas of PMBOK 6 Table 7-1 belong to Control Costs, process 7.4, and need the baseline first. Neither is in this document.

### Rules of the estimate

*Three fields of form 2.19 Cost Management Plan [2] govern how every figure below is written. The project has no separate cost management plan, so they are stated here, followed by the supplier's company rules, which decide what is and is not a project cost, and the scope this estimate covers.*

| Field | Content |
| --- | --- |
| **Units of Measure** | Labor in hours of effort, and in person-months of 160 hours, the charter's own conversion. Physical and software resources in their selling unit: seat-month, server-month, or the item. Money in VND; prices in US dollars converted at 26,170 VND per USD, the Vietcombank selling rate of October 2026 [6]. |
| **Level of Precision** | Hourly rates and every amount to the nearest 1,000 VND; hours to one decimal. Unit prices are kept as published, and the parametric worksheet multiplies them by the most likely quantity. |
| **Level of Accuracy** | -30% to +40% around the estimate, the range from the optimistic to the pessimistic inputs. That is inside the -25% to +75% PMBOK 6 gives for a rough order of magnitude and wider than the -5% to +10% of a definitive estimate [1]. The hours carry the cone of uncertainty at requirements complete [14]; the estimate is redone at M1, when the requirements are baselined. |

**Company rules.** The supplier keeps its own costs low without passing them to its staff:

1. Remote-first: the team works from home and meets at the center's branches for workshops, demos, and acceptance, so no desk is rented.
2. Staff bring their own laptops, with no allowance for wear.
3. Free tiers wherever they are enough: GitHub Free [7]; a paid seat only for the months it is used.
4. Paperless: manuals and guides are delivered in the application and as files, not printed.
5. Timesheets: the project is charged for the hours its people book on it. In weeks without project work they work on the supplier's other projects or training, and the supplier pays them in full either way; no one's pay depends on this project's hours.
6. Every statutory contribution is charged with the hour. The 13th-month salary, the market's practice [15], is paid in full by the supplier from its own revenue and is not charged to projects.
7. No overtime is planned; the levelled schedule keeps every person inside a 40-hour week.
8. The supplier's shared costs (management, human resources, accounting) and its margin are not charged to the project.

**Scope of this estimate.** F07 teacher payroll, F08 assessment and progress reports, and F12 the mobile app are deferred to a second project: the 12 work packages 1.2.3.4, 1.3.1.5, 1.4.4.1, 1.5.1.3, 1.5.2.1, 1.5.4.1, 1.5.4.2, 1.5.4.3, 1.5.4.4, 1.6.1.2, 1.9.1.1, 1.9.1.2, 684 dictionary hours. The packages that specify, design, test, or fix named build work keep the share of their hours that the build work kept bears to all of it, and two packages are made leaner:

| Work package | Dictionary hours | Hours kept | Share | Why |
| --- | ---: | ---: | ---: | --- |
| 1.1.1.2 Weekly status reporting and sponsor governance | 120 | 60 | 50% | status reports fortnightly instead of weekly |
| 1.2.1.2 Functional requirements specification, F01 to F12 | 72 | 44.4 | 62% | with the build work it covers |
| 1.3.1.2 Database schema design | 76 | 66.3 | 87% | with the build work it covers |
| 1.3.1.3 Server API contract | 52 | 32.1 | 62% | with the build work it covers |
| 1.3.1.4 Web user interface design | 28 | 24.4 | 87% | with the build work it covers |
| 1.5.5.1 Iteration 2 testing, finance and administration | 62 | 55.8 | 90% | with the build work it covers |
| 1.5.5.2 Iteration 2 testing, academic, notification, and mobile | 50 | 7.2 | 14% | with the build work it covers |
| 1.5.5.3 Iteration 2 code review and rework | 60 | 27.7 | 46% | with the build work it covers |
| 1.6.1.7 Defect fixing, enrollment, tuition, and payroll | 80 | 70.4 | 88% | with the build work it covers |
| 1.6.1.8 Defect fixing, catalog, assessment, notification, and platform, with regression | 80 | 55.4 | 69% | with the build work it covers |
| 1.10.1.1 First warranty month support | 400 | 160 | 40% | a support rota in the first warranty month instead of the whole team on call |

That leaves 3,239.6 of the 4,400 dictionary hours, 74%.

*Reading convention. Form 2.20 is filled at control account level, one row for each of the 21 control accounts the reduced scope keeps and one project-level row for the reserve, which the book permits, since its ID is "the WBS ID or activity ID" [2]; form 2.21 shows the work behind each row. The Resource column names the three kinds of resource the estimate covers: human, physical, and software. An hour costs the gross monthly salary plus the employer's contributions, 21.5% for social, health, and unemployment insurance [4] and 2% union fee [5], divided by 160 hours; the salary is the ITviec median for 1 to 2 years of experience [3], <mark>the seniority every role is costed at</mark>, and developers are priced as full-stack, since the team has no separate front-end or back-end developer. The rates are single figures, and the uncertainty sits in the hours: each control account's hours are the most likely value, 0.67 and 1.5 times them the optimistic and pessimistic, the cone of uncertainty at requirements complete [14], weighted (O + 4M + P) / 6 as PMBOK 6 section 7.2.2.5 gives, which is 1.0283 times the hours; every three-point row of form 2.21 uses that one weighting, which is why its Weighting Equation column repeats. The warranty support desk is an allocation and is not weighted. The project is charged by timesheet (company rule 5), so a row is the cost of its effort and there is no row for paid time without project work. Range is what a row costs at the optimistic and the pessimistic inputs, and the total's range is 449,726,000 to 905,316,000, taken with every row moving together; one standard deviation, (P - O) / 6, is 75,932,000, so the estimate plus one standard deviation, 721,941,000, is about the 84th percentile. Every amount excludes VAT, which the supplier deducts as input tax [16]. Confidence Level reads Medium where the rates are survey medians and the prices are published, and Low for an allowance carried from the charter and for a reserve that is a percentage rather than a risk analysis. Reference numbers in square brackets point to the list at the end. <mark>Highlighted</mark> content is a choice or a quantity that no source confirms. Every figure is generated by `tools/cost_estimate.py` from `scope-package.en.md`, the levelling of `tools/level.py`, and the prices it lists; change those and rerun it rather than editing this file.*

#### ACTIVITY COST ESTIMATES, page 1 of 1

| Field | Content |
| --- | --- |
| **Project Title** | Development and Deployment of a Learning Center Management Software |
| **Date Prepared** | 8 October 2026 |

| WBS ID | Resource | Labor Costs | Physical Costs | Reserve | Estimate | Method | Assumptions/Constraints | Basis of Estimates | Range | Confidence Level |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| 1.1.1 Project Governance | Human: PM 240 h. Software: GitHub Free, 0; Figma Professional, one full seat. | 56,764,000 | 1,047,000 |  | 57,811,000 | Bottom-up; parametric rate; three-point hours; parametric prices. | Remote-first, staff on their own laptops, GitHub Free: company rules 1 to 3. <mark>Figma paid for the two design months only</mark>. <mark>Scaled</mark>: 1.1.1.2 to 50%, status reports fortnightly instead of weekly. | PM 240 h, 246.8 weighted at 230,000 VND/h [3][4][5][14]. Figma Professional, one full seat 1,047,000 [8][9][6]. | 38,031,000 to 83,847,000 | Medium |
| 1.2.1 Elicitation | Human: PM 140.4 h; DEV3 24 h. | 37,084,000 | 0 |  | 37,084,000 | Bottom-up; parametric rate; three-point hours. | Hours as the dictionary sheets give them. <mark>Scaled</mark>: 1.2.1.2 to 62%, with the build work it covers. | PM 140.4 h, 144.4 weighted at 230,000 VND/h; DEV 24 h, 24.7 weighted at 157,000 VND/h [3][4][5][14]. | 24,162,000 to 54,093,000 | Medium |
| 1.2.2 Requirements Baseline | Human: PM 32 h; DEV3 12 h; QA1 40 h. | 15,224,000 | 0 |  | 15,224,000 | Bottom-up; parametric rate; three-point hours. | Hours as the dictionary sheets give them. | PM 32 h, 32.9 weighted at 230,000 VND/h; DEV 12 h, 12.3 weighted at 157,000 VND/h; QA 40 h, 41.1 weighted at 139,000 VND/h [3][4][5][14]. | 9,918,000 to 22,206,000 | Medium |
| 1.2.3 Technical Preparation | Human: DEV1 100 h, DEV2 120 h. Software: Staging server. | 35,519,000 | 5,593,000 |  | 41,112,000 | Bottom-up; parametric rate; three-point hours; parametric prices. | The gateway proof uses a free tier. A staging server <mark>from the development environment to closeout</mark>; production runs on the center's server. Deferred: 1.2.3.4 Cross-platform framework proof. | DEV 220 h, 226.2 weighted at 157,000 VND/h [3][4][5][14]. Staging server 5,593,000 [10]. | 28,735,000 to 57,403,000 | Medium |
| 1.3.1 Solution Design | Human: PM 16 h; DEV1 69.8 h, DEV2 32.1 h, DEV3 80.9 h. | 33,292,000 | 0 |  | 33,292,000 | Bottom-up; parametric rate; three-point hours. | Design work runs on the Figma seat of 1.1.1. Deferred: 1.3.1.5 Mobile application design. <mark>Scaled</mark>: 1.3.1.2 to 87%, with the build work it covers; 1.3.1.3 to 62%, with the build work it covers; 1.3.1.4 to 87%, with the build work it covers. | PM 16 h, 16.5 weighted at 230,000 VND/h; DEV 182.8 h, 187.9 weighted at 157,000 VND/h [3][4][5][14]. | 21,692,000 to 48,562,000 | Medium |
| 1.3.2 Design Assurance | Human: PM 44 h; DEV2 20 h; QA1 80 h. | 25,071,000 | 0 |  | 25,071,000 | Bottom-up; parametric rate; three-point hours. | Hours as the dictionary sheets give them. | PM 44 h, 45.2 weighted at 230,000 VND/h; DEV 20 h, 20.6 weighted at 157,000 VND/h; QA 80 h, 82.3 weighted at 139,000 VND/h [3][4][5][14]. | 16,334,000 to 36,570,000 | Medium |
| 1.4.1 Core Platform | Human: DEV2 90 h, DEV3 120 h. | 33,904,000 | 0 |  | 33,904,000 | Bottom-up; parametric rate; three-point hours. | Hours as the dictionary sheets give them. | DEV 210 h, 215.9 weighted at 157,000 VND/h [3][4][5][14]. | 22,090,000 to 49,455,000 | Medium |
| 1.4.2 Scheduling and Attendance | Human: DEV1 140 h, DEV2 70 h. | 33,904,000 | 0 |  | 33,904,000 | Bottom-up; parametric rate; three-point hours. | Hours as the dictionary sheets give them. | DEV 210 h, 215.9 weighted at 157,000 VND/h [3][4][5][14]. | 22,090,000 to 49,455,000 | Medium |
| 1.4.3 Iteration 1 Assurance | Human: PM 30 h; DEV1 20 h, DEV3 40 h; QA1 152 h. | 38,510,000 | 0 |  | 38,510,000 | Bottom-up; parametric rate; three-point hours. | Hours as the dictionary sheets give them. | PM 30 h, 30.9 weighted at 230,000 VND/h; DEV 60 h, 61.7 weighted at 157,000 VND/h; QA 152 h, 156.3 weighted at 139,000 VND/h [3][4][5][14]. | 25,090,000 to 56,172,000 | Medium |
| 1.5.1 Finance | Human: DEV2 130 h. | 20,988,000 | 0 |  | 20,988,000 | Bottom-up; parametric rate; three-point hours. | Hours as the dictionary sheets give them. Deferred: 1.5.1.3 F07 Teacher records and teaching-hour payroll. | DEV 130 h, 133.7 weighted at 157,000 VND/h [3][4][5][14]. | 13,675,000 to 30,615,000 | Medium |
| 1.5.2 Academic and Communication | Human: DEV3 60 h. | 9,687,000 | 0 |  | 9,687,000 | Bottom-up; parametric rate; three-point hours. | Test messages go through the center's own gateway account, which the charter says the center provides. Deferred: 1.5.2.1 F08 Assessment, progress reports, and course evaluation. | DEV 60 h, 61.7 weighted at 157,000 VND/h [3][4][5][14]. | 6,311,000 to 14,130,000 | Medium |
| 1.5.3 Management and Administration | Human: DEV1 140 h. | 22,603,000 | 0 |  | 22,603,000 | Bottom-up; parametric rate; three-point hours. | Hours as the dictionary sheets give them. | DEV 140 h, 144 weighted at 157,000 VND/h [3][4][5][14]. | 14,727,000 to 32,970,000 | Medium |
| 1.5.5 Iteration 2 Assurance | Human: PM 30 h; DEV1 9.2 h; QA1 101.4 h. | 23,085,000 | 0 |  | 23,085,000 | Bottom-up; parametric rate; three-point hours. | Hours as the dictionary sheets give them. <mark>Scaled</mark>: 1.5.5.1 to 90%, with the build work it covers; 1.5.5.2 to 14%, with the build work it covers; 1.5.5.3 to 46%, with the build work it covers. | PM 30 h, 30.9 weighted at 230,000 VND/h; DEV 9.2 h, 9.5 weighted at 157,000 VND/h; QA 101.4 h, 104.3 weighted at 139,000 VND/h [3][4][5][14]. | 15,041,000 to 33,673,000 | Medium |
| 1.6.1 System Test | Human: DEV1 80 h, DEV2 70.4 h, DEV3 81.5 h; QA1 173.8 h. | 62,295,000 | 0 |  | 62,295,000 | Bottom-up; parametric rate; three-point hours. | Web system test only. Deferred: 1.6.1.2 System test execution, Android and iOS. <mark>Scaled</mark>: 1.6.1.7 to 88%, with the build work it covers; 1.6.1.8 to 69%, with the build work it covers. | DEV 231.9 h, 238.5 weighted at 157,000 VND/h; QA 173.8 h, 178.8 weighted at 139,000 VND/h [3][4][5][14]. | 40,588,000 to 90,869,000 | Medium |
| 1.6.2 Test Documentation | Human: PM 20 h; QA1 36 h. | 9,876,000 | 0 |  | 9,876,000 | Bottom-up; parametric rate; three-point hours. | Hours as the dictionary sheets give them. | PM 20 h, 20.6 weighted at 230,000 VND/h; QA 36 h, 37 weighted at 139,000 VND/h [3][4][5][14]. | 6,435,000 to 14,406,000 | Medium |
| 1.7.1 Migration | Human: PM 20 h; DEV1 120 h; QA1 20 h. | 26,963,000 | 0 |  | 26,963,000 | Bottom-up; parametric rate; three-point hours. | The center enters and cleans its own source data, as risk R6 and the project exclusions say; <mark>the migration scripts keep their dictionary hours</mark>. | PM 20 h, 20.6 weighted at 230,000 VND/h; DEV 120 h, 123.4 weighted at 157,000 VND/h; QA 20 h, 20.6 weighted at 139,000 VND/h [3][4][5][14]. | 17,568,000 to 39,330,000 | Medium |
| 1.8.1 Production Environment | Human: PM 8 h; DEV3 64 h; QA1 8 h. Physical: Go-live support and on-site presence. Software: Domain .vn first year and TLS certificate. | 13,369,000 | 8,708,000 |  | 22,077,000 | Bottom-up; parametric rate; three-point hours; parametric prices; allowance. | The certificate is free; production runs on the center's server. Go-live support kept at the charter's allowance, <mark>not checked against a published price</mark>. | PM 8 h, 8.2 weighted at 230,000 VND/h; DEV 64 h, 65.8 weighted at 157,000 VND/h; QA 8 h, 8.2 weighted at 139,000 VND/h [3][4][5][14]. Domain .vn first year and TLS certificate 708,000 [11][12]. Go-live support and on-site presence 8,000,000, allowance. | 17,160,000 to 29,500,000 | Medium; low for the allowances |
| 1.8.2 Training and Documentation | Human: PM 40 h; DEV2 16 h; QA1 8 h. Physical: Training delivery, venue, and materials; Travel to the three branches. | 13,188,000 | 15,000,000 |  | 28,188,000 | Bottom-up; parametric rate; three-point hours; allowance. | Manuals delivered in the application and as files (company rule 4). Training and travel kept at the charter's allowances, <mark>not checked against a published price</mark>, since venues and distances are not known. | PM 40 h, 41.1 weighted at 230,000 VND/h; DEV 16 h, 16.5 weighted at 157,000 VND/h; QA 8 h, 8.2 weighted at 139,000 VND/h [3][4][5][14]. Training delivery, venue, and materials 12,000,000, allowance. Travel to the three branches 3,000,000, allowance. | 23,592,000 to 34,236,000 | Medium; low for the allowances |
| 1.8.3 Handover | Human: PM 12 h; DEV2 20 h; QA1 24 h. | 9,498,000 | 0 |  | 9,498,000 | Bottom-up; parametric rate; three-point hours. | Hours as the dictionary sheets give them. | PM 12 h, 12.3 weighted at 230,000 VND/h; DEV 20 h, 20.6 weighted at 157,000 VND/h; QA 24 h, 24.7 weighted at 139,000 VND/h [3][4][5][14]. | 6,188,000 to 13,854,000 | Medium |
| 1.10.1 Warranty | Human: PM 25.6 h; DEV1 40 h, DEV2 68.8 h, DEV3 56.8 h; QA1 12.8 h; support desk 160 h. | 59,741,000 | 0 |  | 59,741,000 | Bottom-up; parametric rate; three-point hours. | Warranty months 2 to 6 at <mark>0.2 FTE for the web system</mark>, costed as developer hours rather than as the charter's lump sum; an allocation, so not weighted. <mark>Scaled</mark>: 1.10.1.1 to 40%, a support rota in the first warranty month instead of the whole team on call. | PM 25.6 h, 26.3 weighted at 230,000 VND/h; DEV 165.6 h, 170.3 weighted at 157,000 VND/h; QA 12.8 h, 13.2 weighted at 139,000 VND/h; DEV 160 h at 157,000 VND/h [3][4][5][14]. | 47,676,000 to 75,620,000 | Medium |
| 1.10.2 Closeout | Human: PM 30 h. | 7,096,000 | 0 |  | 7,096,000 | Bottom-up; parametric rate; three-point hours. | Hours as the dictionary sheets give them. | PM 30 h, 30.9 weighted at 230,000 VND/h [3][4][5][14]. | 4,623,000 to 10,350,000 | Medium |
| 1 Project, contingency reserve | Contingency reserve, charter budget line 6 |  |  | 28,000,000 | 28,000,000 | Reserve analysis [1]. | Held at project level and drawn only through change control against risks R1 to R12. <mark>Not re-derived</mark>: the register carries no probability or impact to derive it from. At the charter's 4% of the new estimate it would be 24,720,000. | Charter budget line 6. | 28,000,000 | Low |
| **Total** |  | **587,661,000** | **30,348,000** | **28,000,000** | **646,009,000** |  |  | 3,239.6 hours of work and 160 support desk hours. | **449,726,000 to 905,316,000** | Medium |

#### COST ESTIMATING WORKSHEET, page 1 of 2

| Field | Content |
| --- | --- |
| **Project Title** | Development and Deployment of a Learning Center Management Software |
| **Date Prepared** | 8 October 2026 |

**Parametric Estimates**

| ID | Cost Variable | Cost per Unit | Number of Units | Cost Estimate |
| --- | --- | ---: | ---: | ---: |
| PM | Labor hour, project manager and business analyst | 230,000 | 688 | 158,242,000 |
| DEV1 DEV2 DEV3 | Labor hour, developer | 157,000 | 1,895.5 | 297,598,000 |
| 1.10.1.2 | Labor hour, warranty support desk, developer | 157,000 | 160 | 25,120,000 |
| QA1 | Labor hour, QA engineer | 139,000 | 656.1 | 91,197,000 |
| 1.1.1.1-A4 | Seat-month of Figma Professional, billed monthly | 523,400 | 2 | 1,047,000 |
| 1.2.3.2 | Month of a T1.Base 05 staging server | 799,000 | 7 | 5,593,000 |
| 1.8.1.1-A4 | Domain .vn and TLS certificate, first year | 450,000 | 1 | 450,000 |

**Analogous Estimates**

| ID | Previous Activity | Previous Cost | Current Activity | Multiplier | Cost Estimate |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

**Three-Point Estimates**

| ID | Optimistic Cost | Most Likely Cost | Pessimistic Cost | Weighting Equation | Expected Cost Estimate |
| --- | ---: | ---: | ---: | --- | ---: |
| PM, labor hours, 688 h | 106,022,000 | 158,242,000 | 237,363,000 | (O + 4M + P) / 6 | 162,725,000 |
| DEV1 DEV2 DEV3, labor hours, 1,895.5 h | 199,390,000 | 297,598,000 | 446,396,000 | (O + 4M + P) / 6 | 306,030,000 |
| QA1, labor hours, 656.1 h | 61,102,000 | 91,197,000 | 136,795,000 | (O + 4M + P) / 6 | 93,781,000 |
| 1.8.1.1-A4, Domain .vn first year and TLS certificate | 450,000 | 450,000 | 2,000,000 | (O + 4M + P) / 6 | 708,000 |

#### BOTTOM-UP COST ESTIMATING WORKSHEET, page 2 of 2

| Field | Content |
| --- | --- |
| **Project Title** | Development and Deployment of a Learning Center Management Software |
| **Date Prepared** | 8 October 2026 |

| ID | Labor Hours | Labor Rate | Total Labor | Material | Supplies | Equipment | Travel | Other Direct Costs | Indirect Costs | Reserve | Estimate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1.1.1 PM 240 h | 246.8 | 230,000 | 56,764,000 |  |  |  |  |  |  |  | 56,764,000 |
| 1.1.1.1-A4 Figma Professional, one full seat |  |  |  |  |  |  |  | 1,047,000 |  |  | 1,047,000 |
| 1.2.1 PM 140.4 h | 144.4 | 230,000 | 33,209,000 |  |  |  |  |  |  |  | 33,209,000 |
| 1.2.1 DEV3 24 h | 24.7 | 157,000 | 3,875,000 |  |  |  |  |  |  |  | 3,875,000 |
| 1.2.2 PM 32 h | 32.9 | 230,000 | 7,569,000 |  |  |  |  |  |  |  | 7,569,000 |
| 1.2.2 DEV3 12 h | 12.3 | 157,000 | 1,937,000 |  |  |  |  |  |  |  | 1,937,000 |
| 1.2.2 QA1 40 h | 41.1 | 139,000 | 5,718,000 |  |  |  |  |  |  |  | 5,718,000 |
| 1.2.3 DEV1 100 h, DEV2 120 h | 226.2 | 157,000 | 35,519,000 |  |  |  |  |  |  |  | 35,519,000 |
| 1.2.3.2 Staging server |  |  |  |  |  |  |  | 5,593,000 |  |  | 5,593,000 |
| 1.3.1 PM 16 h | 16.5 | 230,000 | 3,784,000 |  |  |  |  |  |  |  | 3,784,000 |
| 1.3.1 DEV1 69.8 h, DEV2 32.1 h, DEV3 80.9 h | 187.9 | 157,000 | 29,508,000 |  |  |  |  |  |  |  | 29,508,000 |
| 1.3.2 PM 44 h | 45.2 | 230,000 | 10,407,000 |  |  |  |  |  |  |  | 10,407,000 |
| 1.3.2 DEV2 20 h | 20.6 | 157,000 | 3,229,000 |  |  |  |  |  |  |  | 3,229,000 |
| 1.3.2 QA1 80 h | 82.3 | 139,000 | 11,435,000 |  |  |  |  |  |  |  | 11,435,000 |
| 1.4.1 DEV2 90 h, DEV3 120 h | 215.9 | 157,000 | 33,904,000 |  |  |  |  |  |  |  | 33,904,000 |
| 1.4.2 DEV1 140 h, DEV2 70 h | 215.9 | 157,000 | 33,904,000 |  |  |  |  |  |  |  | 33,904,000 |
| 1.4.3 PM 30 h | 30.9 | 230,000 | 7,096,000 |  |  |  |  |  |  |  | 7,096,000 |
| 1.4.3 DEV1 20 h, DEV3 40 h | 61.7 | 157,000 | 9,687,000 |  |  |  |  |  |  |  | 9,687,000 |
| 1.4.3 QA1 152 h | 156.3 | 139,000 | 21,727,000 |  |  |  |  |  |  |  | 21,727,000 |
| 1.5.1 DEV2 130 h | 133.7 | 157,000 | 20,988,000 |  |  |  |  |  |  |  | 20,988,000 |
| 1.5.2 DEV3 60 h | 61.7 | 157,000 | 9,687,000 |  |  |  |  |  |  |  | 9,687,000 |
| 1.5.3 DEV1 140 h | 144 | 157,000 | 22,603,000 |  |  |  |  |  |  |  | 22,603,000 |
| 1.5.5 PM 30 h | 30.9 | 230,000 | 7,096,000 |  |  |  |  |  |  |  | 7,096,000 |
| 1.5.5 DEV1 9.2 h | 9.5 | 157,000 | 1,488,000 |  |  |  |  |  |  |  | 1,488,000 |
| 1.5.5 QA1 101.4 h | 104.3 | 139,000 | 14,501,000 |  |  |  |  |  |  |  | 14,501,000 |
| 1.6.1 DEV1 80 h, DEV2 70.4 h, DEV3 81.5 h | 238.5 | 157,000 | 37,446,000 |  |  |  |  |  |  |  | 37,446,000 |
| 1.6.1 QA1 173.8 h | 178.8 | 139,000 | 24,849,000 |  |  |  |  |  |  |  | 24,849,000 |
| 1.6.2 PM 20 h | 20.6 | 230,000 | 4,730,000 |  |  |  |  |  |  |  | 4,730,000 |
| 1.6.2 QA1 36 h | 37 | 139,000 | 5,146,000 |  |  |  |  |  |  |  | 5,146,000 |
| 1.7.1 PM 20 h | 20.6 | 230,000 | 4,730,000 |  |  |  |  |  |  |  | 4,730,000 |
| 1.7.1 DEV1 120 h | 123.4 | 157,000 | 19,374,000 |  |  |  |  |  |  |  | 19,374,000 |
| 1.7.1 QA1 20 h | 20.6 | 139,000 | 2,859,000 |  |  |  |  |  |  |  | 2,859,000 |
| 1.8.1 PM 8 h | 8.2 | 230,000 | 1,892,000 |  |  |  |  |  |  |  | 1,892,000 |
| 1.8.1 DEV3 64 h | 65.8 | 157,000 | 10,333,000 |  |  |  |  |  |  |  | 10,333,000 |
| 1.8.1 QA1 8 h | 8.2 | 139,000 | 1,144,000 |  |  |  |  |  |  |  | 1,144,000 |
| 1.8.1.1-A4 Domain .vn first year and TLS certificate |  |  |  |  |  |  |  | 708,000 |  |  | 708,000 |
| 1.8.1.3-A4 Go-live support and on-site presence |  |  |  |  |  |  | 8,000,000 |  |  |  | 8,000,000 |
| 1.8.2 PM 40 h | 41.1 | 230,000 | 9,461,000 |  |  |  |  |  |  |  | 9,461,000 |
| 1.8.2 DEV2 16 h | 16.5 | 157,000 | 2,583,000 |  |  |  |  |  |  |  | 2,583,000 |
| 1.8.2 QA1 8 h | 8.2 | 139,000 | 1,144,000 |  |  |  |  |  |  |  | 1,144,000 |
| 1.8.2.2-A4 Training delivery, venue, and materials |  |  |  |  | 12,000,000 |  |  |  |  |  | 12,000,000 |
| 1.8.2.2-A5 Travel to the three branches |  |  |  |  |  |  | 3,000,000 |  |  |  | 3,000,000 |
| 1.8.3 PM 12 h | 12.3 | 230,000 | 2,838,000 |  |  |  |  |  |  |  | 2,838,000 |
| 1.8.3 DEV2 20 h | 20.6 | 157,000 | 3,229,000 |  |  |  |  |  |  |  | 3,229,000 |
| 1.8.3 QA1 24 h | 24.7 | 139,000 | 3,431,000 |  |  |  |  |  |  |  | 3,431,000 |
| 1.10.1 PM 25.6 h | 26.3 | 230,000 | 6,055,000 |  |  |  |  |  |  |  | 6,055,000 |
| 1.10.1 DEV1 40 h, DEV2 68.8 h, DEV3 56.8 h | 170.3 | 157,000 | 26,736,000 |  |  |  |  |  |  |  | 26,736,000 |
| 1.10.1 QA1 12.8 h | 13.2 | 139,000 | 1,830,000 |  |  |  |  |  |  |  | 1,830,000 |
| 1.10.1 support desk 160 h | 160 | 157,000 | 25,120,000 |  |  |  |  |  |  |  | 25,120,000 |
| 1.10.2 PM 30 h | 30.9 | 230,000 | 7,096,000 |  |  |  |  |  |  |  | 7,096,000 |
| 1 Contingency reserve |  |  |  |  |  |  |  |  |  | 28,000,000 | 28,000,000 |
| **Total** | **3,491.4** |  | **587,661,000** |  | **12,000,000** |  | **11,000,000** | **7,348,000** |  | **28,000,000** | **646,009,000** |

---

### Paid time without booked work

None is charged. The charter commits the five full-time staff to the project "before planning starts" and makes them "not renegotiable"; company rule 5 keeps that commitment, since each of them is available to the project whenever its schedule needs them, and charges the project only for the hours they book. The levelled schedule of the reduced work runs 5.63 months, 14 September 2026 to 1 March 2027, 901.5 hours a person; the rest of each person's time is the supplier's, spent on its other projects or training and paid by it:

| Person | Hours booked, weighted | Hours in the levelled window | Hours the supplier carries |
| --- | ---: | ---: | ---: |
| PM | 707.5 | 901.5 | 194 |
| DEV1 | 739.4 | 901.5 | 162.1 |
| DEV2 | 655.3 | 901.5 | 246.2 |
| DEV3 | 554.5 | 901.5 | 347 |
| QA1 | 674.7 | 901.5 | 226.8 |

Had the five been paid by the month over that window instead, the option the estimate of 7 October 2026 priced separately, the project would carry those hours too.

### Estimate against the charter: for the team to decide

This estimate does not change the charter, the scope package, or their checker, which still hold the full scope and the 700,000,000 VND baseline. The reduction goes to the sponsor in `3-3-change-request-scope.en.md`, because deferring functions is the sponsor's decision.

| Charter budget line | Charter (VND) | This estimate (VND) | Difference (VND) |
| --- | ---: | ---: | ---: |
| Personnel | 539,000,000 | 562,541,000 | 23,541,000 |
| Infrastructure, licences, store accounts | 42,000,000 | 7,348,000 | -34,652,000 |
| Facilities, equipment, travel | 14,000,000 | 3,000,000 | -11,000,000 |
| Deployment, migration, training, documentation | 42,000,000 | 20,000,000 | -22,000,000 |
| Warranty and support, months 2 to 6 | 35,000,000 | 25,120,000 | -9,880,000 |
| Contingency reserve | 28,000,000 | 28,000,000 | 0 |
| **Total** | **700,000,000** | **646,009,000** | **-53,991,000** |

Where the difference comes from, in the order it arises:

| Step | Amount (VND) | Running total (VND) |
| --- | ---: | ---: |
| Charter total | 700,000,000 | 700,000,000 |
| Work deferred or made leaner, 3,239.6 of the 4,400 dictionary hours kept, at the charter's rate mix | -140,596,000 | 559,404,000 |
| The hours kept at the market median for 1 to 2 years instead of the charter's rate mix (assumption 17) | 148,632,000 | 708,036,000 |
| The same hours weighted for the cone of uncertainty | 15,505,000 | 723,541,000 |
| Warranty months 2 to 6, 160 hours at a developer's rate instead of the lump sum | -9,880,000 | 713,661,000 |
| Physical and software: the charter's lines 2 to 4 less what is deferred, what moves to the center, and what the company rules remove | -67,652,000 | 646,009,000 |

What the charter funded that this estimate does not charge:

| Item | Amount (VND) | Why it is not a project cost |
| --- | ---: | --- |
| Production server, 12 months | 14,400,000 | the center provides the cloud virtual server (charter, Resources preassigned) [10] |
| Development and test gateway credits | 4,000,000 | the center provides and pays its gateway account (same place, and assumption 12); the charter's own figure [13] |
| Documentation printing | 10,000,000 | company rule 4, paperless; the charter's allowance |
| External data entry | 12,000,000 | the center enters and cleans its own source data, as risk R6 and the project exclusions say; the charter's allowance |
| Workspace |  | company rule 1, remote-first |
| Laptops |  | company rule 2, staff bring their own |
| GitHub Team |  | company rule 3, GitHub Free |
| Weeks without project work |  | company rule 5, timesheets |
| 13th-month salary |  | company rule 6, paid by the supplier |

The production server and the gateway credits are costs the charter itself places on the center, and the change request asks the sponsor to confirm that and correct budget line 2, which also funds them. The store accounts leave with F12.

Proposed updates to other documents, carried by the change request and not made here: the scope reduction in the charter, the WBS, the dictionary, and the traceability matrix; assumption 17 replaced by the rates of form 2.21 page 1 and their source; the company rules added to the assumptions; new project risks, that a team costed at 1 to 2 years needs more hours than the dictionary gives, and that the weighted hours overrun the levelled window; budget line 2 and the Resources preassigned paragraph made to agree on hosting and the gateway account.

### References

All web pages read on 7 October 2026. Prices are as the page showed them that day.

1. PMI. *A Guide to the Project Management Body of Knowledge, 6th edition, chapter 7 Project Cost Management: 7.2 Estimate Costs, 7.2.2.5 three-point estimating, 7.2.2.6 reserve analysis, 7.2.3.2 basis of estimates, and 7.3.2.5 funding limit reconciliation*. PMBOK6_and_Agile_Practice_Guide.pdf in the team repository. Used: Process, inputs and outputs, techniques, beta formula, contents of the basis of estimates, accuracy ranges, reconciliation of the estimate with a funding limit.
2. C. S. Dionisio. *A Project Manager's Book of Forms, 3rd edition, forms 2.19 Cost Management Plan, 2.20 Cost Estimates, 2.21 Cost Estimating Worksheet, 3.3 Change Request*. PDF pages 93 to 103 and 181 to 185 (printed pages 82 to 92 and 170 to 174). Used: Printed fields of the forms; the rules table takes three fields of form 2.19.
3. ITviec. *Vietnam IT Salary and Recruitment Market Report 2025-2026, 1,839 respondents surveyed in 2025, monthly median salary by position and years of experience*. https://itviec.com/report/vietnam-it-salary-and-recruitment-market. Used: Medians for 1 to 2 years: Project Leader/Manager 29.85, Full-stack Developer 20.35, QA-QC 18, Mobile Developer 28.8 million VND a month; for 3 to 4 years, priced only as an alternative in the change request: 48.4, 34.5, 24.4, 29.05.
4. MISA AMIS. *Ty le dong BHXH 2026, published 18 September 2026, citing the Law on Social Insurance 2024 and Decree 158/2025/ND-CP*. https://amis.misa.vn/?p=292831. Used: Employer share 21.5%: retirement 14, sickness 3, accident 0.5, health 3, unemployment 1; contribution ceiling 50,600,000 VND a month from 1 July 2026.
5. Thu Vien Phap Luat. *Quy dinh ve kinh phi cong doan 2%, Law on Trade Unions 2024, article 29, point b of clause 1*. https://thuvienphapluat.vn/ma-so-thue/phap-luat-thue/quy-dinh-ve-kinh-phi-cong-doan-2-o-van-ban-nao-49584-225246.html. Used: Union fee 2% of the payroll on which social insurance is paid, due whether or not a union exists.
6. Vietnam.vn. *Ti gia USD hom nay 5.10: Vietcombank ban ra 26.170 dong/USD*. https://www.vietnam.vn/ti-gia-usd-hom-nay-5-10-vietcombank-ban-ra-26-170-dong-usd. Used: 26,170 VND per USD, the rate every dollar price here is converted at.
7. GitHub. *Pricing*. https://github.com/pricing. Used: Free plan for organizations: unlimited private repositories and collaborators, 2,000 Actions minutes a month, 0 USD.
8. Figma. *Pricing*. https://www.figma.com/pricing/. Used: Professional plan, full seat.
9. CostBench. *Figma pricing 2026*. https://costbench.com/software/design/figma/. Used: Professional full seat 16 USD a month billed annually, 20 USD billed monthly.
10. WHTop. *Viettel IDC plans T2.Gen 02 and T1.Base 05, updated 20 April 2026*. https://www.whtop.com/plans/viettelidc.com.vn/147281 and https://www.whtop.com/plans/viettelidc.com.vn/147277. Used: T1.Base 05 at 799,000 VND a month for staging; T2.Gen 02 at 1,200,000 VND a month for production, which the center provides; VAT not included.
11. VnEconomy. *Ten mien .vn cap 2 mot ky tu co phi duy tri len toi 40 trieu dong/nam, on Circular 20/2023/TT-BTC*. https://vneconomy.vn/ten-mien-vn-cap-2-mot-ky-tu-co-phi-duy-tri-len-toi-40-trieu-dong-nam.htm. Used: .vn second-level domain: registration 100,000 VND once, maintenance 350,000 VND a year.
12. Let's Encrypt. *About Let's Encrypt*. https://letsencrypt.org/about/. Used: TLS certificates free of charge, renewed automatically.
13. Advertising Vietnam. *5 sai lam pho bien khi trien khai SMS brandname cho chuoi ban le*. https://advertisingvietnam.com/article/5-sai-lam-pho-bien-khi-trien-khai-sms-brandname-cho-chuoi-ban-le. Used: SMS brandname 600 to 800 VND a message.
14. S. McConnell. *Software Development's Cone of Uncertainty, Construx best practices white paper, version 1, January 2010*. https://www.construx.com/wp-content/uploads/2019/02/CxWhitePaper_ConeOfUncertainty.pdf. Used: Figure 1: estimates by skilled estimators fall within 0.67x to 1.5x of the outcome at Requirements Complete, 0.5x to 2x at Approved Product Definition.
15. VnExpress. *Nganh IT am tham thuong Tet*. https://vnexpress.net/nganh-it-am-tham-thuong-tet-3529076.html. Used: A 13th-month salary is common practice at IT employers in Viet Nam.
16. MISA. *Khau tru thue GTGT la gi? Dieu kien khau tru thue GTGT dau vao moi nhat, on the Law on VAT 48/2024/QH15, article 14*. https://sme.misa.vn/345365/khau-tru-thue-gtgt/. Used: A business on the deduction method deducts the input VAT on goods and services it uses for taxable business.
