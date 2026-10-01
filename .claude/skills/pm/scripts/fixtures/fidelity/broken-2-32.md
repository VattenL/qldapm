# 2.32 Risk Register

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 24 September 2026
**Source:** A Project Manager's Book of Forms, 3rd edition, form 2.32, printed pages 128 to 130

*How to read this register.* The printed form is one page with its columns in two banks. Both banks are reproduced below as two tables in printed order; the ID column is repeated at the start of the second bank so that each row can be read across, and the printed Impact heading spans the Scope, Quality, Schedule and Cost columns in both banks. Risk statements and responses for R1 to R12 are copied unchanged from the Overall project risk element of the charter package, and the Product or Project type the charter gives each risk is carried in Comments. Actions name the work packages of the scope package that carry each response, and Responsible Party is the Responsible Person of those packages, using the scope package's resource codes. Probability, the four Impact columns, Score and all revised values are empty because the risks have not been scored yet; until they are, the 28,000,000 VND contingency reserve of charter budget line 6 is a 4% allowance rather than a figure derived from these risks, and the charter re-estimates its budget breakdown at M1. Owner is empty because the charter names no risk owner; WBS dictionary package 1.1.1.4 requires every risk to carry an owner when this register is baselined at M1. Status is highlighted as assumed: no response has been recorded as complete, so every risk is taken to be open.

| ID | Risk Statement | Probability | Owner | Impact Scope | Impact Quality | Impact Schedule | Impact Cost | Score | Response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | The delivered system does not meet the acceptance criteria A01 to A12, so the center cannot run its operation on it and the objectives are missed | | | | | | | | Agree the UAT test set with the business owners at M5 and measure acceptance against it; pilot F01 to F06 at one branch before M6; gate go-live on A01; if UAT fails, put the three options of the approval requirements to the sponsor within two working days |
| R2 | Tuition, discount, and refund rules change after the requirement baseline | | | | | | | | Freeze the rules at M1 with written sign-off; route later changes through the change process against the reserve |
| R3 | Customer staff not available for workshops, demos, and UAT | | | | | | | | Fixed weekly slot agreed with the sponsor at kickoff; a missed slot escalated to the sponsor within 2 working days |
| R4 | Loss or absence of a developer, or of the part-time mobile developer | | | | | | | | Pair on the scheduling and tuition modules; keep code and documentation in shared repositories; sponsor-approved replacement within 2 weeks |
| R5 | Notification gateway unstable or unexpectedly priced | | | | | | | | Isolate it behind one interface; prove it with a proof of concept before M2; keep a second provider as fallback |
| R6 | Source Excel data too dirty to migrate | | | | | | | | Assess data quality at M1; the center cleans the files before M5; migration limited to the two most recent terms |
| R7 | Scheduling and conflict detection harder than estimated | | | | | | | | Build F04 first in iteration 1, timeboxed, and review it at the M3 demo |
| R8 | Go-live slips and pushes the first warranty month into the Lunar New Year break | | | | | | | | Baseline go-live at M6, a full month before the break; escalate to the sponsor immediately on a forecast slip past 15 January 2027, and re-plan the warranty rather than compress it silently |
| R9 | The project manager is also the business analyst, so analysis and management compete for one person | | | | | | | | Front-load analysis into M0 to M1 while management load is lowest; the QA engineer writes test cases from the requirement baseline as a second reader; escalate if analysis rework after M1 exceeds one week |
| R10 | Go-live fails and the center cannot run its evening classes | | | | | | | | Pilot F01 to F06 at one branch for the two weeks before M6; keep the spreadsheets in deliberate parallel for two weeks after go-live; rehearse the paper fallback; agree written rollback criteria that the center itself can invoke |
| R11 | The system is delivered but the tuition benefit never appears, because nobody works the debt list | | | | | | | | Name the Accountant as benefit owner at M0; report the overdue percentage to the Director monthly from go-live; state the actual percentage in the closeout report |
| R12 | A store rejects or delays the app, or the cross-platform framework fails on one platform | | | | | | | | Open the store accounts in the center's name at M1; prove the framework on both platforms before M2; submit at M5; go-live does not depend on the app, and an app slip of up to two weeks after M6 is absorbed without moving M6 |

| ID | Revised Probability | Impact Scope | Impact Quality | Impact Schedule | Impact Cost | Revised Score | Responsible Party | Actions | Comments |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | | | | | | | QA1 | 1.6.2.1 UAT test set, defect log, and test summary report; 1.8.3.2 User acceptance testing execution and sign-off | <mark>Open</mark> | Product risk |
| R2 | | | | | | | PM | 1.2.1.2 Functional requirements specification, F01 to F12 | <mark>Open</mark> | Product risk |
| R3 | | | | | | | PM | 1.1.1.3 Weekly status reporting and sponsor governance | <mark>Open</mark> | Project risk |
| R4 | | | | | | | DEV1, QA1 | 1.2.3.1 Repository, coding convention, and build pipeline; 1.4.3.1 Iteration 1 code review and rework; 1.5.5.1 Iteration 2 code review and rework | <mark>Open</mark> | Project risk |
| R5 | | | | | | | DEV2 | 1.2.3.2 Notification gateway proof of concept | <mark>Open</mark> | Project risk |
| R6 | | | | | | | DEV1 | 1.7.1.1 Source data analysis and cleansing rules | <mark>Open</mark> | Product risk |
| R7 | | | | | | | DEV1 | 1.4.2.1 F04 Class opening, session calendar, and postponement; 1.4.2.3 F04 Room, teacher, and class-time conflict detection | <mark>Open</mark> | Project risk |
| R8 | | | | | | | DEV3 | 1.8.1.3 Production deployment and go-live | <mark>Open</mark> | Project risk |
| R9 | | | | | | | QA1 | 1.2.2.2 Requirements peer review and rework; 1.3.2.2 Test plan and test strategy | <mark>Open</mark> | Project risk |
| R10 | | | | | | | DEV3 | 1.8.1.3 Production deployment and go-live | <mark>Open</mark> | Product risk |
| R11 | | | | | | | PM | 1.10.1.1 First warranty month support | <mark>Open</mark> | Product risk |
| R12 | | | | | | | DEV3 | 1.2.3.3 Cross-platform framework proof; 1.9.1.1 Store accounts and signing keys | <mark>Open</mark> | Project risk |
