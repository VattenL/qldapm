# 2.27 Team Charter

*Form 2.27, A Project Manager's Book of Forms, 3rd edition, PDF pages 122 to 123 (printed pages 111 to 112); PMBOK 6 section 9.1.3.2, printed pages 319 to 320 (PDF pages 358 to 359). Built from the charter as committed on 16 September 2026, the scope package as committed on 14 October 2026, and the cost estimate of 8 October 2026, form 2.20, whose company rules and reduced scope it follows. A box that prints numbered lines is one cell with its entries written inline. Plain text is copied from the charter or from the company rules of form 2.20; highlighted text is a working rule proposed for the team to confirm at kickoff, because the book says the charter works best when the team develops it. Every rule names a time, a channel, or a person, so that a team member can tell whether it was kept. The signature lines are empty. Form 2.26 does not exist yet, so nothing was compared with it.*

**Project Title:** Development and Deployment of a Learning Center Management Software
**Date Prepared:** 29 October 2026

#### TEAM CHARTER, page 1 of 2

| Field | Content |
| --- | --- |
| **Team Values and Principles** | (1) Each work package has one owner, the Responsible Person of its dictionary sheet. (2) A forecast slip or overrun is reported to the project manager on the day it is seen, and the plan is re-planned rather than compressed silently. (3) Hours are booked in the timesheet in the week they are worked, and the project is charged only for booked hours (company rule 5). (4) The week is 40 hours and no overtime is planned (company rule 7); <mark>a task that would need overtime is raised to the project manager as a schedule issue, not absorbed by the person who owns it.</mark> |
| **Meeting Guidelines** | (1) The Academic Manager and the Accountant attend workshops, demos, and UAT in a fixed weekly slot agreed with the sponsor at kickoff, at least 4 hours a week each; a missed slot is escalated to the sponsor within 2 working days. (2) Each build iteration closes with a demo, accepted in a signed demo acceptance record. (3) <mark>Team meeting online every Monday at 09:00, at most 30 minutes: what was finished, what is planned, what is blocked. The project manager sends the agenda by 17:00 on the Friday before and the notes, with each action, its owner, and its date, by 12:00 on the Monday.</mark> (4) <mark>A written stand-up in the team chat by 09:30 on the other working days, one line each for done, next, and blocked, instead of a daily call.</mark> (5) The team works remotely (company rule 1) and meets in person only at the center's branches, for workshops, demos, UAT, training, and go-live. |
| **Communication Guidelines** | (1) The project manager is the single point of contact for the sponsor and the center's staff. (2) The project manager reports status to the sponsor every two weeks, the reporting rate form 2.20 costs for work package 1.1.1.2. (3) <mark>A question in the team chat is answered within 4 working hours; a blocker is also said at once in the chat, not kept for the Monday meeting.</mark> (4) <mark>A decision is recorded as a GitHub issue or in the meeting notes on the day it is made; a decision that exists only in chat does not count.</mark> (5) Code and documents are kept only in the team's shared GitHub repositories, never on a personal machine alone (risk R4). |
| **Decision-Making Process** | The project manager decides architecture, technology stack, database design, coding standards, tooling, the internal delivery approach, and the content of each iteration within the approved scope; assigns and re-assigns work within the approved team, approves leave, and manages day-to-day performance; and commits and spends within the approved baseline, including single transactions up to <mark>20,000,000 VND</mark> and the contingency reserve against risks R1 to R12. A decision that changes user-visible scope, the schedule, or the cost goes to the sponsor through the change process, form 3.3, as does any forecast overrun beyond 5%, any reserve use beyond <mark>20,000,000 VND</mark>, and any change in total funding. A baselined decision on scope, schedule, or cost is reopened only by a change request. Voting procedure: <mark>there is no vote. The Responsible Person of the work package proposes, anyone affected comments, and the project manager decides within 1 working day; a dissent is written into the decision record next to the decision.</mark> When any other decision may be revisited: <mark>at the planning of the next iteration, or earlier when a new fact shows that the decision puts an acceptance criterion A01 to A12 or a milestone at risk.</mark> |

#### TEAM CHARTER, page 2 of 2

| Field | Content |
| --- | --- |
| **Conflict Resolution Process** | The project manager resolves conflicts within the team and between the team and the center's operational staff, including competing claims on staff availability. A conflict that crosses organisations, alters agreed scope, or remains unresolved after <mark>five working days</mark> goes to the sponsor, whose decision is final. Disputes with external suppliers follow the applicable service agreement. <mark>Two team members first settle a disagreement between themselves, in a call on the same day; when they cannot, the project manager decides after hearing both.</mark> When a conflict is tabled for later discussion: <mark>it goes on the agenda of the next Monday team meeting, with its owner and the date it was raised, and to the sponsor if it is still open five working days after it was raised.</mark> |
| **Other Agreements** | (1) DEV1 and DEV2 build F04 and F06 together and pair on those modules, so that each can carry the other's work (risk R4). (2) The QA engineer reads the requirement baseline as a second reader (risk R9). (3) <mark>Every merge request is reviewed by another developer before it is merged, within 1 working day of the request; no one approves their own work, as in the dictionary, where no review activity is owned by the author of what is reviewed.</mark> (4) <mark>This charter is reviewed at M1, when the estimate is redone on the baselined requirements, and whenever a team member joins or leaves.</mark> |

| Signature | Date |
| --- | --- |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
| | |
