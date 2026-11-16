# 1.4 Stakeholder Analysis

*Form 1.4, A Project Manager's Book of Forms, 3rd edition, PDF page 27 (printed page 16), filled with the stakeholder analysis of PMBOK 6 section 13.1.2.3, printed page 512 (PDF page 551), and represented as a grid by the stakeholder mapping of PMBOK 6 section 13.1.2.4, printed pages 512 to 513 (PDF pages 551 to 552). The rows are the twenty stakeholders of form 1.3 Stakeholder Register, with the same IDs and names; the ID column is not printed on the form and is added so that the two forms can be matched.*

*The stakeholders of this project are few and their relationships simple, so the analysis uses the two-by-two grid of the book's first tailoring tip, PDF page 26 (printed page 15), with two levels each for Interest and Influence, defined below. Attitude uses the book's three classes, friend, neutral, and foe, from the description of Classification in Table 1.3, PDF page 24 (printed page 13). Each cell gives the level and the reason for it. No stakeholder has yet been interviewed, so every level is the preparer's reading from the charter and the risk register and is highlighted; as PMBOK 6 section 13.1.3.4, printed page 515, advises, these readings are entered in form 1.2 Assumption Log as assumption 20.*

## Levels

| Level | Interest | Influence |
| --- | --- | --- |
| High | <mark>The stakeholder's daily work, money, or data changes with the outcome, or the stakeholder works on the project</mark> | <mark>The stakeholder signs an approval of the charter's approval requirements; or controls the funding, the team, or a resource the project cannot replace in time; or can stop a deliverable by store review or by law</mark> |
| Low | <mark>The stakeholder is affected only after go-live, or only through a service contract</mark> | <mark>None of the above</mark> |

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 14 November 2026

| ID | Name or Role | Interest | Influence | Attitude |
| --- | --- | --- | --- | --- |
| S01 | <mark>Dr. Nguyễn Mạnh Hùng</mark>, sponsor | <mark>High: releases the 700,000,000 VND and gives final acceptance</mark> | <mark>High: approves changes beyond the project manager's authority, authorises go-live, and may close the project early</mark> | <mark>Friend: authorised the project and the charter</mark> |
| S02 | <mark>Đỗ Thị Bích Ngọc</mark>, owner and Center Director, customer | <mark>High: the center's daily operation moves onto the system</mark> | <mark>High: commits the business owners, the data, the server, the gateway account, and the store accounts, and confirms the operation at closeout</mark> | <mark>Friend: owns the business need the project serves</mark> |
| S03 | Branch managers | <mark>High: their branch switches over on one day, mid-term, and its staff are trained and supported at the branch</mark> | <mark>Low: no approval in the charter in the branch role, which the academic managers hold besides their own (assumption 2); the Center Director commits the center's staff</mark> | <mark>Neutral: no document records their view; the charter has the sponsor champion the project with them</mark> |
| S04 | Academic Manager | <mark>High: the teaching operation is scheduled in the system, and the role works on the project 4 hours a week</mark> | <mark>High: signs the requirement baseline, the iteration releases, and UAT for this area</mark> | <mark>Neutral: gains a timetable without double booking, but gives 4 hours a week on top of the daily job (R3)</mark> |
| S05 | Accountant | <mark>High: tuition, debt, and payroll move into the system, and the role owns the tuition benefit</mark> | <mark>High: signs the requirement baseline and UAT for this area and accepts the migrated data</mark> | <mark>Neutral: gains the aged debt list, but gives 4 hours a week and must freeze the rules at M1 (R2, R3)</mark> |
| S06 | Front-desk / Admissions supervisor | <mark>High: enrollment and payment recording at the three branches change</mark> | <mark>High: signs demo acceptance of its functions at M3 and M4, and of F12</mark> | <mark>Neutral: no document records this role's view</mark> |
| S07 | Head Teacher | <mark>High: the teachers' daily screens change</mark> | <mark>High: signs F12 acceptance at M4</mark> | <mark>Neutral: no document records this role's view</mark> |
| S08 | Teachers | <mark>High: attendance, scores, and the teaching-hour sheet move into the system</mark> | <mark>Low: no approval; represented by the Head Teacher</mark> | <mark>Neutral: risk R15 expects some to keep working on paper and spreadsheets</mark> |
| S09 | Students and parents | <mark>Low: affected only after go-live, when the app and the notices reach them</mark> | <mark>Low: no approval; their use of the app drives the benefit of R16, not the deliverables</mark> | <mark>Neutral: not yet aware of the project</mark> |
| S10 | Center IT administrator | <mark>High: operates the system after handover</mark> | <mark>High: signs the handover record of D8 and D9</mark> | <mark>Neutral: no document records this role's view</mark> |
| S11 | Project Manager | <mark>High: runs the project full time</mark> | <mark>High: decides within the authority the charter grants</mark> | <mark>Friend: accountable for the project's success</mark> |
| S12 | Development team: DEV1, DEV2, DEV3, MOB1, QA1 | <mark>High: does the work</mark> | <mark>High: losing one member moves the critical path (R4)</mark> | <mark>Friend: committed to the project before planning started</mark> |
| S13 | Supplier line management | <mark>Low: one contract among the supplier's work</mark> | <mark>High: keeps hiring, firing, and the replacement of a team member (R4)</mark> | <mark>Neutral: no document records its view</mark> |
| S14 | Supplier support desk | <mark>Low: works only after closeout</mark> | <mark>Low: no approval within the project</mark> | <mark>Neutral: no document records its view</mark> |
| S15 | Notification gateway provider | <mark>Low: affected only through the center's account</mark> | <mark>High: instability or a price change delays F09 (R5)</mark> | <mark>Neutral: a supplier bound by its service terms</mark> |
| S16 | Viettel IDC | <mark>Low: affected only through a 12-month subscription</mark> | <mark>High: the server carries A02 and A06 (R14)</mark> | <mark>Neutral: a supplier bound by its service terms</mark> |
| S17 | Apple (App Store) | <mark>Low: one app among many in review</mark> | <mark>High: can reject or delay the iOS app (R12)</mark> | <mark>Neutral: applies its review rules</mark> |
| S18 | Google (Google Play) | <mark>Low: one app among many in review</mark> | <mark>High: can reject or delay the Android app (R12)</mark> | <mark>Neutral: applies its review rules</mark> |
| S19 | Push notification service provider | <mark>Low: affected only through a free-tier account</mark> | <mark>Low: a failed push falls back to SMS within 4 hours (A12)</mark> | <mark>Neutral: a supplier bound by its service terms</mark> |
| S20 | <mark>State authority enforcing the Law on Personal Data Protection</mark> | <mark>Low: not aware of the project</mark> | <mark>High: the law decides how the personal data of children and guardians is handled (A04, R13)</mark> | <mark>Neutral: applies the law</mark> |

## Interest and influence grid

The grid places each row of the form by its two levels. The name in each quadrant is the conventional response for that quadrant of a two-by-two grid, carried into the Classification column of form 1.3 and to be used by form 2.40 Stakeholder Engagement Plan; it is the preparer's reading.

| | Low interest | High interest |
| --- | --- | --- |
| **High influence** | <mark>Keep satisfied: S13, S15, S16, S17, S18, S20</mark> | <mark>Manage closely: S01, S02, S04, S05, S06, S07, S10, S11, S12</mark> |
| **Low influence** | <mark>Monitor: S09, S14, S19</mark> | <mark>Keep informed: S03, S08</mark> |
