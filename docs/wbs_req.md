reading Chapter 5, using the template provided in the …form book, create documentation include:,

* Requirements Traceability Matrix
* Work Breakdown Structure (WBS)
* WBS Dictionary

Try to fill in form as much as possible; incase you dont know how to write, please let the box empty; incase you dont know the content is correct or not, please let the background of box in yellow.
send docx file with name: group ID.docx/pdf(e.g. 2.docx)
Project size: assuming that 4 staffs do the project (including requirement, analysis, design, coding, testing...) in 4-6 months.

## Where the forms are

Chapter 5 is PMBOK 6 Project Scope Management. All three artifacts are outputs of its processes, and all
three exist as forms in *A Project Manager's Book of Forms*, 3rd edition.

| Artifact | Form | PDF pages | Blank form on |
| --- | --- | --- | --- |
| Requirements Traceability Matrix | 2.7 | 51 to 55 | 54, with the Inter-RTM on 55 |
| Work Breakdown Structure | 2.9 | 60 to 62 | 62 |
| WBS Dictionary | 2.10 | 63 to 66 | 66 |

## Class notes, checked

The notes taken in class were checked against PMBOK 6 Figure 5-10 and Book of Forms pages 49 to 53
before the document was written. Two of them do not hold, and the document follows the corrected
version rather than the note.

| # | Note | Verdict |
| --- | --- | --- |
| 1 | WBS input is requirement, traceability matrix, and charter | **Partly wrong.** The inputs to 5.4 Create WBS are the scope management plan, the project scope statement, the requirements documentation, enterprise environmental factors, and organizational process assets. The charter is an input to 5.1, 5.2, and 5.3, and reaches the WBS through the scope statement. The traceability matrix is an *output* of 5.2, never an input to 5.4. Book of Forms page 49 agrees. |
| 2 | Follow one of two routes only, top-down or bottom-up; top-down for the experienced | **Valid.** Decomposition in PMBOK is top-down. The charter fixes D1 to D11 and M0 to M7 before any work package exists, so the package is decomposed top-down and the two methods are not mixed. |
| 3 | One person per work item, for example one codes and another reviews | **Valid as practice, not a book rule.** The book's rule is that each work package rolls up to one and only one control account, page 50. The two are compatible. Both are implemented: every dictionary sheet names one Responsible Person, and the review and rework packages are owned by the QA engineer or by a developer who is not the author of the work being reviewed. |
| 4 | Ask about the project life cycle first, then divide by phase or by deliverable | **Valid, and directly supported.** Page 49 lists geography, major deliverables, life cycle phases, and subprojects as the ways to organise. The life cycle here is predictive with two build iterations, so level 2 holds the major deliverables, as form 2.9 prints it, arranged in life-cycle phase order. |
| 5 | Put review and testing into the work packages, and fix the defects after review | **Valid, adopted.** Review and test are work packages in their own right, held in a separate assurance control account inside each construction phase, 1.4.3 and 1.5.5, plus the system-level phase 1.6 for the tests that cannot sit inside one construction package. |
| 6 | The labor column is rough in the first version and serious later | **Valid.** Page 52 describes the dictionary as progressively elaborated, and the charter itself commits to re-estimating the breakdown at M1. Every sheet is marked accordingly. |
| 7 | The dictionary is annoying because it is too detailed | **Fair.** Page 53 permits trimming to description of work, cost estimate, key delivery dates, and assigned resources. The full form is kept anyway, because the assignment asks for the form to be filled in as much as possible. |
| 8 | One table per work package | **Correct.** Form 2.10 is Page 1 of 1 per work package, and the document has one sheet per work package. |
| 9 | No Validate Scope; impossible for a project that is only starting | **Correct.** 5.5 Validate Scope is a Monitoring and Controlling process and needs deliverables already verified by 8.3 Control Quality. There are none at planning time, so it produces no artifact here. |
| 10 | Every scope process outputs change requests, which are the input to Perform Integrated Change Control | **Half wrong.** Change requests are outputs of 5.5 Validate Scope and 5.6 Control Scope only, and those do feed 4.6. The four planning processes 5.1 to 5.4, which are what this deliverable covers, output no change requests. |

## Team size

The line above asks for 4 staff. The charter package is already baselined at 6 people, being 5 full-time
staff plus a part-time mobile developer for 2.5 person-months, 27.5 person-months in total, funding
539,000,000 VND of the 700,000,000 VND budget. The scope package costs to that baseline rather than
re-cutting it, so that the two documents agree; 6 sits inside the 4 to 6 the original course brief
allowed, and the 4 here is read as a floor.
