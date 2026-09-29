# Format audit, 29 September 2026

Document audited: Google Doc `4.md` (`1OTrxc3-L_t_NQcNiMG0EzwVsMU8Ftb7WFKuPSxHYgTw`), read through the Docs API on 29 September 2026, three tabs: Product Charter, Thẻ 2, 3: Scope Baseline. 289 tables in all: 39 in Product Charter (18 of them the one-cell boxes of form 1.1), 10 in Thẻ 2, and 240 in 3: Scope Baseline, of which 234 are the three tables of each of the 78 dictionary sheets.

Standard: the printed forms of *A Project Manager's Book of Forms*, 3rd edition, read as page images: 1.1 Project Charter (PDF pages 16 to 19), 2.7 Requirements Traceability Matrix (54 to 55), 2.9 Work Breakdown Structure (62), 2.10 WBS Dictionary (66). Part 1 of the charter tab follows form 2.8 Project Scope Statement.

Method: every table was checked by script for its row and column count, header cells, merged cells, cell shading, highlighted labels, and the order of its field labels. Every cell was compared with the repo sources `docs/charter-package.en.md` and `docs/scope-package.en.md` on branch `schedule`. Page breaks, heading styles and outline indentation were read from the document structure.

## Errors

These contradict the printed form, the brief, or the repo source.

**E1. Tab "Thẻ 2" is still the old v2 charter, and its layout departs from form 1.1.** Its content contradicts tab 1: F01 to F11, a 70,000,000 VND management reserve, the sponsor described as owner and Director. Its layout does too: every box sits in a Field | Content table whose header row the form does not print, Project Manager Authority Level is a table row with an empty cell, and Approvals has three columns (Sponsor, Project Manager, Customer) where the form prints two (Project Manager, Sponsor or Originator). Delete or hide the tab before submission. This was E3 on 24 September.

**E2. The Prompt Log is still missing.** Requirement 4 of the brief asks for every prompt version with its quality and the reason for each revision. The source has it as Part 3 of `charter-package.en.md`; no tab of the Doc carries it. This was E5.

**E3. The charter form's four pages are not four pages.** Form 1.1 prints four pages, each under the PROJECT CHARTER title bar with "Page N of 4". Tab 1 has one page break, and it falls inside page 2, between the objectives table and the Summary Milestones table. Pages 1, 3 and 4 start wherever the text before them ends, so printed page 2 is split over two sheets and pages 3 and 4 run on. Thẻ 2 has breaks in other places (after page 3's financial box and after Approvals). Put a page break before each page marker and none inside a page.

**E4. Form 2.10 layout, on all 78 dictionary sheets (234 tables).** Every sheet has the same three tables, which is consistent, but not the printed layout:
- The printed form puts two fields side by side: Work Package Name beside Code of Accounts, Description of Work beside Assumptions and Constraints, and Milestones beside Due Dates. The Doc lists them one under another in a two-column table.
- The printed activity table has a two-row header. The first row carries the group labels Labor (over Hours, Rate, Total) and Material (over Units, Cost, Total). ID, Activity, Resource and Total Cost span both rows. The Doc has a single header row reading Labor Hours, Labor Rate, Labor Total and so on.
- The top and bottom field tables each open with a "Field | Content" row that the form does not print.
- No sheet has the WBS DICTIONARY title bar or "Page 1 of 1". The source has "*Page 1 of 1*" under each sheet; it did not survive the push.

The RTM tables in the same tab do carry the printed title bar as a merged, shaded first row, so tab 3 treats its forms two ways. Reviewer thread AAACHhmz-Cw ("Lệch hẳn format"). This was W9, and it is raised to an error here because it is a direct departure from the printed form on the largest part of the Doc.

**E5. Tab 1 has fallen behind its source in four cells.**
- 1.1.3 Users and roles, Center Director: the Doc says "Owner and project sponsor", which merges the two people the charter keeps apart (assumption 16). The source says "Owner of the center, and the project's customer".
- 1.2 Project Deliverables, D4: the Doc says "Iteration 2 release, F06 to F11". The source, M4, the form's Key Deliverables box and WBS 1.5 all say F06 to F12. This was E4.
- 1.1.3, Teacher and Student / Parent: the Doc has the older wording, with the F12 functions appended after "also", where the source has merged them.

Re-push tab 1 from the source rather than editing these cells by hand.

**E6. Three printed labels are highlighted as if their content were uncertain.** "Project Customer" and "Overall Project Risk" on form page 1, and the heading "1.6 Project Assumptions". The highlight marks uncertain content, per point 3 of the brief, never a label. This was part of W6.

**E7. One RTM ID carries different text on the two pages of form 2.7.**
- On page 1, NFR02 is "Performance thresholds (A02)". On page 2 it is "Conflict check inside the 3 second screen budget" and "One term's report inside 10 seconds".
- BR03's Source is "Accountant, Center Director" on page 1 and "Accountant" on page 2.

The same ID has to read the same on both pages. This was part of W7.

## Warnings

These are weak points a reviewer or grader may raise.

**W1. Heading styles on the charter form are uneven.**
- There are two titles: "2B. PROJECT CHARTER form" and an extra "PROJECT CHARTER" heading, both H3.
- The page 1 marker is body text, while the markers for pages 2 to 4 are H3.
- "Project Manager Authority Level" is an H4, while every other printed label is bold body text. The form prints it as a plain label.

This was part of W6.

**W2. Two notes sit inside the form.** A paragraph under the Summary Milestones table on page 2 and another under Approvals on page 4. Neither is printed on form 1.1. Move them into a reading note before the form, or into 2A. This was part of W6.

**W3. Page 1 does not pair its fields.** The form prints Project Sponsor beside Date Prepared and Project Manager beside Project Customer. The Doc stacks each label over its own one-cell box. The printed labels also end with a colon ("Project Title:"), and the Doc's do not.

**W4. The objectives table on page 2 is shaped differently.** The form prints the label (Scope:, Time:, Cost:, Other:) as a line above each two-cell row. The Doc uses a 5 x 3 table with the labels in a first column. The content is the same; the shape is not.

**W5. "Management reserve" is still on form page 2.** The Cost success criterion says "management reserve use reported monthly". 2A says "reserve use reported monthly", and budget line 6 is a contingency reserve. This was part of W2.

**W6. The WBS outline adds text the form does not print.** Form 2.9 writes its codes with a closing period ("1.1."); the Doc writes "1.1". The annotations "(major deliverable, D1, M1)" and "(control account)" are not printed, although they echo the form's placeholder labels. Low weight.

**W7. Date formats are still mixed in tab 1.** "Mon 14 Sep 2026" in both milestone tables, "14 September 2026" in the text, and "Mon 14 September 2026" in tab 3. The source has the same mix. This was W11.

**W8. The Responsible Person row is not on the printed form, and the Doc no longer says why.** It is valid, because the book's element list on page 52 names the responsible organization or person. The source says so in its Part 3 preamble, but that sentence is not in the Doc.

## Status of the 24 September findings

| Finding | Now |
| --- | --- |
| E3 Thẻ 2 stale | Open, E1 above |
| E4 D4 F06 to F11 | Open, E5 above |
| E5 Prompt Log missing | Open, E2 above |
| E6 literal `<br>` in tab 3 | Fixed: none left |
| E7 sizing rule not stated | Fixed: rule and the two named exceptions are in 3.2.1 |
| E8 WBS as a table | Fixed: outline indented 0, 18, 36, 54 pt by level |
| E9 tab 3 behind source | Fixed: tab 3 matches the source cell for cell |
| E10 NFR01 "Center Director, sponsor" | Fixed: Source reads Center Director |
| W2 management reserve wording | Open, W5 above |
| W6 form 1.1 layout | Open, E6, W1 and W2 above |
| W7 RTM one ID, one text | Open, E7 above |
| W9 form 2.10 layout | Open, E4 above |
| W11 mixed dates | Open, W7 above |

## What passed

- Every printed field of form 1.1 is present in tab 1, in printed order. Approvals has the two printed columns, Project Manager and Sponsor or Originator, over Signature, Name and Date.
- Part 1 follows form 2.8 Project Scope Statement: sections 1.1 to 1.6 are the six printed fields in printed order.
- Form 2.7 page 1 has the printed title bar, the two group headers merged over five and four columns, and the nine printed columns in order. Page 2 has its title bar and the eight printed columns in order. The uniform Priority column is explained above the matrix.
- Form 2.9 is a numbered outline, indented by level, from the project down to 78 work packages.
- All 78 dictionary sheets have the same three tables, with the printed field labels in printed order, codes and names matching the outline, one Date Prepared, and no highlighted label.
- Tab 3 matches `docs/scope-package.en.md` cell for cell, apart from section references rewritten for the Doc.
- No literal `<br>`, no em dash and no emoji in any tab.

## Not in the Doc yet

The project schedule (form 2.18) and change request (form 3.3) on branch `schedule` have not been pushed. If they are, 3.2.3 and the 3.3 preamble, which say levelling "is not in this report", need a sentence pointing to them.
