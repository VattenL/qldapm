# 3.3 Change Request, availability

*Form 3.3, A Project Manager's Book of Forms, 3rd edition, PDF pages 183 to 185 (printed pages 172 to 174). This request amends the open schedule request `3-3-change-request.en.md` of 30 September 2026 and does not overwrite it; whether to amend, replace, or fold in is the sponsor's decision, recorded in forms 3.2 and 3.4. Built from the charter as committed on 16 September 2026 and the scope package as committed on 14 October 2026. Requestor is empty, and Disposition and its Justification belong to the sponsor.*

*The figures come from `tools/level.py` run on 20 October 2026 with 6 productive hours a working day, which is 75 percent of 8, the share form 2.17 gives as typical (PDF page 84, printed page 73; equation PDF page 86, printed page 75). At 8 hours it reproduces the earlier request exactly. The tool has no option for the day length, so the run overrides its constant after import. <mark>Highlighted</mark> figures are forecasts or estimates at the charter's rate basis (assumption 17).*

#### CHANGE REQUEST, page 1 of 3

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 20 October 2026

| Field | Content |
| --- | --- |
| **Requestor** | |

**Category**

- [ ] Scope
- [ ] Quality
- [ ] Requirements
- [x] Cost
- [x] Schedule
- [x] Documents

| Field | Content |
| --- | --- |
| **Detailed Description of Proposed Change** | Replace the levelled milestone forecast of the request of Wed 30 September 2026 with the forecast of form 2.18 levelled at 75 percent availability: M1 from Fri 2 October 2026 to <mark>Thu 12 November 2026</mark>; M2 from Fri 16 October 2026 to <mark>Thu 3 December 2026</mark>; M3 from Fri 13 November 2026 to <mark>Tue 12 January 2027</mark>; M4 from Fri 11 December 2026 to <mark>Wed 24 February 2027</mark>; M5 from Fri 18 December 2026 to <mark>Mon 29 March 2027</mark>; M6 go-live from Tue 5 January 2027 to <mark>Fri 9 April 2027</mark>; M7 closeout from Fri 5 February 2027 to <mark>Mon 10 May 2027</mark>. M0 is unchanged. Keep the five full-time staff for the extra <mark>66 working days</mark> this adds to the charter dates, against 30 in the earlier request, and increase the personnel budget line to fund them. No activity, estimate, function or acceptance criterion changes. |
| **Justification for Proposed Change** | The forecast of Wed 30 September 2026 places a person up to 8 hours on every working day, which assumes they are productive for all of it. Form 2.17 says people are productive on project work about 75 percent of the time, and its equation divides effort by the percent available. At 75 percent each full-time person has about 630 productive hours in the 105 working days of the charter window, against the 800 estimated hours each carries, so the earlier forecast is a lower bound. Percent available is the book's typical value, not one measured for this team; the team confirms or replaces it, and the forecast is run again with the figure it gives. Resource leveling (PMBOK 6 section 6.5.2.3, printed page 211, PDF page 250) places every one of the 4,400 estimated hours inside a 30-hour week and divides <mark>106</mark> activities between two people, against 93 in the earlier request. |

**Impacts of Change**

**Scope**

- [ ] Increase
- [ ] Decrease
- [ ] Modify

| Field | Content |
| --- | --- |
| **Description** | None. Functions F01 to F12, deliverables D1 to D11 and the 78 work packages are unchanged. |

**Quality**

- [ ] Increase
- [ ] Decrease
- [ ] Modify

| Field | Content |
| --- | --- |
| **Description** | None to the criteria A01 to A12. System test keeps its full 556 estimated hours. One defect remains in the forecast: in the warranty month the level-of-effort package keeps its hours, and DEV2 is booked about <mark>2.19 hours a day</mark> above the 6-hour limit on 21 working days from Mon 12 April 2027 to Mon 10 May 2027, about <mark>46 hours</mark>. Resolving it would move M7 later than the date above. |

#### CHANGE REQUEST, page 2 of 3

**Requirements**

- [ ] Increase
- [ ] Decrease
- [ ] Modify

| Field | Content |
| --- | --- |
| **Description** | None. The requirement baseline is signed at the new M1 instead of 2 October 2026. |

**Cost**

- [x] Increase
- [ ] Decrease
- [ ] Modify

| Field | Content |
| --- | --- |
| **Description** | Two readings, and the sponsor says which governs. On the charter's person-month basis (assumption 9) the 66 extra working days are 3.3 person-months at 20 working days a month, for the five full-time staff at the rate mix of 26,000,000 (project manager), 3 x 19,000,000 (developers) and 15,000,000 (QA engineer), 98,000,000 VND a month: <mark>about 323,400,000 VND</mark>, against 147,000,000 in the earlier request. The Lunar New Year break falls inside the forecast and is not in the calendar; if it removes five working days it adds <mark>about 24,500,000 VND</mark>. On an hours basis the hours stay 4,400, the labour total is hours times rate and does not change, and only the elapsed time grows. The mobile developer's work fits inside the funded 2.5 person-months. The 28,000,000 VND contingency reserve cannot cover either reading, so budget line 1 and the 700,000,000 VND total need the sponsor's decision. |

**Schedule**

- [x] Increase
- [ ] Decrease
- [ ] Modify

| Field | Content |
| --- | --- |
| **Description** | Go-live moves by <mark>66 working days</mark> to <mark>Fri 9 April 2027</mark> and closeout to <mark>Mon 10 May 2027</mark>. Warranty months 2 to 6, which run six months from go-live, end about <mark>Sat 9 October 2027</mark> instead of Mon 5 July 2027. The critical path is not recomputed here. Go-live and the first warranty month move after the Lunar New Year break instead of before it, which the charter chose to avoid, and the forecast now runs into late April and early May, where public holidays that the calendar does not hold fall; assumption 14 no longer holds. The risk R8 trigger of Fri 15 January 2027 is already passed. |

**Stakeholder Impact**

- [x] High risk
- [ ] Low risk
- [ ] Medium risk

| Field | Content |
| --- | --- |
| **Description** | The Center Director and the business owners switch three branches over in April instead of January and keep the spreadsheets running until then. The sponsor funds more person-months. Tuition, discount and refund rules frozen at M1 wait longer before go-live, which raises risk R2. |
| **Project Documents** | Charter: summary milestone schedule (2A and form 1.1 page 3), the Time success criterion, budget line 1 and the total, the payment tranches tied to M3, M4 and M6, assumption 14, and the warranty end. Scope package: the Due Dates field of the 78 dictionary sheets and the resource on the divided activities. Risk register: R2, R8 and R9. Form 2.18 becomes the schedule baseline once decided. Form 2.28: percent available in Assumptions. |

| Field | Content |
| --- | --- |
| **Comments** | Alternatives weighed, all from PMBOK 6 section 6.5.2.6, printed page 215 (PDF page 254): (1) crashing; the earlier request sized it at about 750 hours and <mark>about 93,000,000 VND</mark> at 8 hours a day, which no longer holds, and the charter allows no further headcount (charter section 1.5); (2) fast tracking by up to 5 working days a phase, which the forecast already uses and which cannot be offered a second time; (3) reducing scope through a separate request, the scope request of 8 October 2026 being the one open; (4) re-estimating the hours down to fit the dates, rejected because compression is done without reducing the work and no chapter names shortening an estimate as a technique (searched PMBOK 6 section 6.5.2, printed pages 209 to 216, PDF pages 248 to 255). The levelled plan again starts work up to 5 working days before its gate. |

#### CHANGE REQUEST, page 3 of 3

**Disposition**

- [ ] Approve
- [ ] Defer
- [ ] Reject

| Field | Content |
| --- | --- |
| **Justification** | |
