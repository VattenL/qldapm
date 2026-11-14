# The project: what exists, where, and what disagrees

State on 14 November 2026: repo at commit 55df70b (branch `stakeholder-register`), live
Doc `4.md` snapshotted the same day with `tools/gdoc_dump.py`. This file is the map a review
starts from, not the truth: the team and its teammates edit the sources and the Doc between
reviews. Before you cite any line, figure or status below, re-read it where it lives (the
line numbers are those of that commit) and take a fresh snapshot of the Doc. A row that no
longer matches is dropped, not reported; a new disagreement is reported even if it is not
here. Update this file when a review settles something.

The project: development and deployment of a learning center management software (web
system plus a mobile app) for a private after-school center with three branches, by a
team of five full-time plus a part-time mobile developer, 700,000,000 VND, 14 September
2026 to 5 February 2027. Coursework of group 04; the brief is in `requirement.md` (repo
root), `docs/requirements.md` and `docs/wbs_req.md`.

## Contents

1. What the brief asks for
2. Deliverables, sources, Doc tabs and writers
3. Branches that hold a different version
4. Settled decisions (not findings)
5. ID families and key figures, with every place they appear
6. Pending change requests and who follows them
7. Disagreements found on 14 November 2026
8. Comment threads
9. Forms named but not produced
10. Snapshot, compare, push

## 1. What the brief asks for

- `requirement.md` lines 6 to 12: (1) a short requirement specification (description,
  scope, list of functions with a description of each), (2) the project charter on the
  book's template, "@16--19.pdf", the form on PDF pages 16 to 19 (printed pages 5 to 8), (3) fill as much as possible, leave a box empty when you
  do not know how to write it, yellow background when unsure, (4) a prompt log: every
  prompt version, its quality and why it changed. Project size 700 million VND, 5 months.
- `docs/requirements.md`: points 1 to 3 only; "4 to 6 staffs ... in 3 to 8 months".
- `docs/wbs_req.md`: RTM, WBS and WBS dictionary from the Book of Forms, the same yellow and
  empty rule, "send docx file with name: group ID.docx/pdf" (`4.docx` or `4.pdf`), 4 staff
  in 4 to 6 months. `docs/wbs_notes.md`: every work package 8 to 80 hours, none longer than
  one reporting period.
- No brief text is in the repo for the schedule, cost, quality, resource, risk and
  stakeholder deliverables. Ask the user for it before judging those tabs against a brief.

## 2. Deliverables, sources, Doc tabs and writers

Doc `4.md` has 9 tabs. Each tab is written from its source by a writer in `tools/`; the
team also edits the Doc by hand (`review-lessons.md` section 10), so compare the live tab
with the payload before any push.

| Deliverable | Form | Source | Doc tab | Writer | Date printed | State on 14 Nov |
| --- | --- | --- | --- | --- | --- | --- |
| Requirement specification | stands in for 2.8 | `docs/charter-package.en.md` Part 1 | Product Charter (t.0), section 1 | `tools/apply_review_2026-09-16.py` (in place); `tools/gdoc.py replace` rebuilds a whole Doc | v3.1, 2 Sep 2026 | In step except section 7, C1, C2, C18 |
| Project charter, 14 elements and the 4-page form | 1.1 | charter Part 2A and 2B | Product Charter, section 2 | as above | v3.1, 2 Sep 2026 | In step except C1, C2, C18 |
| Prompt log | none | charter Part 3, V1 to V12 | none | none | | Source only: missing from the Doc (thread AAACHKhdaR0) |
| Vietnamese charter | 1.1 | `docs/charter-package.vi.md` | none | none | translation of v2.0 | Stale, not submitted |
| Old charter v2 | 1.1 | none | Thẻ 2 (t.nbjliyn2vu5v) | none | 2 Sep 2026 | Team-labelled draft, "không thuộc bài nộp"; contradicts v3.1 (C11) |
| RTM and inter-RTM | 2.7 | `docs/scope-package.en.md` Part 1 | 3: Scope Baseline (t.wxcbbj3wlvae), 3.1 | `tools/gdoc_tab3.py` with `tools/scope_tab3.py`; `tools/gdoc_scope_sync.py --step rtm` | v2.0, 23 Sep 2026 | In step: 31 rows, BR01 to BR07, FR01 to FR12, NFR01 to NFR12 |
| WBS | 2.9 | scope package Part 2 | tab 3, 3.2 | `tools/gdoc_tab3.py --limit 5` | 23 Sep 2026 | In step, 30 September numbering |
| WBS dictionary, 78 work package sheets | 2.10 | scope package Part 3 | none | `tools/gdoc_tab3.py`, `gdoc_scope_sync.py --step dictionary` | 23 Sep 2026 | Source only |
| WBS dictionary, 24 control account sheets | 2.10 tailored (book printed page 52 (PDF page 63)) | generated from the scope package, no file | tab 3 section 3.3 and tab "dict rút gọn" (t.375i05tu2o20) | `tools/dict_summary.py` | 30 Sep 2026 | In the Doc twice, byte-identical (C12) |
| Project schedule | 2.18 | `docs/forms/2-18-project-schedule.en.md` (from `tools/schedule.py`) | 4: Project Schedule (t.d52waryg1bmk), 4.1 | `tools/gdoc_schedule_tab.py --clear --schedule-only` | 30 Sep 2026 | In step; its "Resource loading after levelling" is not in tab 4 |
| Resource loading after levelling | not a form | 2.18 file, end | Thẻ 2 | moved there by hand | 29 Sep run | Stale (C4) |
| Schedule change request | 3.3 | `docs/forms/3-3-change-request.en.md` | Thẻ 2 "4.2 Change Request" | `tools/gdoc_schedule_tab.py` | repo 30 Sep, Doc 29 Sep | Only in the draft tab, older version (C3, C5) |
| Availability change request | 3.3 | branch `availability-75` only | none | none | 20 Oct 2026 | Branch only |
| Cost estimates and worksheet | 2.20, 2.21 | `docs/forms/2-20-cost-estimates.en.md` (from `tools/cost_estimate.py`) | 5: Cost Estimation (t.kpth2qbkxhyb), 5.1 to 5.6 | `tools/gdoc_cost_tab.py` | 8 Oct 2026 | In step |
| Scope and cost change request | 3.3 | `docs/forms/3-3-change-request-scope.en.md` | tab 5, 5.7 | `tools/gdoc_cost_tab.py` | 8 Oct 2026 | In step |
| Quality management plan | 2.23 | `docs/forms/2-23-quality-management-plan.en.md` | 6: Quality Management Plan (t.5lg547qmn9m2) | `tools/gdoc_quality_tab.py` | 10 Oct 2026 | In step |
| Team charter | 2.27 | `docs/forms/2-27-team-charter.en.md` | 7: Resource Plan (t.3i2nc9lxeswv), 7.1 | `tools/gdoc_resource_tab.py` | Doc 29 Oct; HEAD file 20 Oct | Doc follows `origin/resource-tab`, not HEAD (section 3, C7) |
| Resource requirements | 2.28 | `docs/forms/2-28-resource-requirements.en.md` | tab 7, 7.2 | as above | as above | as above |
| Resource breakdown structure | 2.29 | `docs/forms/2-29-resource-breakdown-structure.en.md` | tab 7, 7.3 | as above | as above | as above |
| Risk register | 2.32 | `docs/forms/2-32-risk-register.en.md` | 8: Risk Register (t.vc0cf7jmw7mu) | `tools/gdoc_risk_tab.py` | v1.1, 8 Nov 2026 | In step: R1 to R18, scales, revision history |
| Stakeholder register and analysis | 1.3, 1.4 | `docs/forms/1-3-stakeholder-register.en.md`, `docs/forms/1-4-stakeholder-analysis.en.md` | planned "9: Stakeholders" | `tools/gdoc_stakeholder_tab.py` | 14 Nov 2026 | Source only on 14 Nov |
| Submission file | none | none | none | none | | Missing: `4.docx` or `4.pdf` |
| Explainers | none | `docs/scope-package.eli5.vi.md`, `docs/project-schedule-explained.vi.html` | none | none | | Not for submission |

## 3. Branches that hold a different version

Read a branch file with `git show <branch>:<path>`.

- `origin/resource-tab` (29 Oct, espi) rewrites 2.27, 2.28 and 2.29 to the reduced scope of
  the pending scope request (no mobile developer, PM 688 h, warranty support 0.2 FTE,
  status reports every two weeks) and adds `docs/pm-skill-guide.vi.md`. The Doc's tab 7 is
  this version. Local `resource-tab` and HEAD keep the 20 October full-scope versions, and
  forms 1.3 and 1.4 were built from those. Which version the team keeps is the team's call.
- `availability-75` (20 Oct): the availability change request, nowhere else.
- `pm-skill`: this skill. Older branches carry an older copy of `.claude/skills/pm`; run
  the checks from the `pm-skill` copy (`git archive pm-skill .claude/skills/pm` into a
  scratch folder) when the working branch is behind.
- `main` is at 2 September and has merged nothing since.

## 4. Settled decisions (not findings)

- The project manager's name is empty on purpose (thread AAACG0ldth8; assumption 15).
- The WBS uses the numbering of 30 September (Vatten, commit 073aefa); review records keep
  the old codes.
- Viettel IDC is the cloud hosting provider, as the team stated on 20 October 2026.
- Thẻ 2 is the team's draft, outside the submission: audit it only when asked, and report
  a submitted tab that depends on it (C5).
- The scope change request of 8 October only proposes deferring F07, F08 and F12 and the
  leaner rates; read its Disposition before calling a tab that keeps or drops them wrong,
  and report the mismatch either way (section 6).
- The Doc's WBS dictionary is the control account summary (Vatten's trim, 30 September).
- The risk register shape of version 1.1 answers Đại Dũng Nguyễn's and Vatten's threads
  (`review-lessons.md` section 15).

## 5. ID families and key figures, with every place they appear

Use this as the list of places to compare, not as the values to copy.

**ID families.** F01 to F12 functions; D1 to D11 deliverables (D10 internal); A01 to A12
acceptance criteria (never assumptions); assumptions 1 to 19; R1 to R12 in the charter, R1
to R18 in 2.32 (R13 to R16 from document analysis, R17 and R18 from the scope request);
M0 to M7 milestones; BR01 to BR07, FR01 to FR12, NFR01 to NFR12 (31 RTM rows); S01 to S20
stakeholders (1.3 and 1.4); budget lines 1 to 6; exit criteria 1 to 10; company rules 1 to
8 (2.20); activity IDs `<WBS code>-A<n>`; prompt versions V1 to V12. Thẻ 2 still has F01 to
F11, D1 to D10, A01 to A11, R1 to R10. `README.md` says 30 RTM rows and BR01 to BR06 and
scope package version 1.0 (the file is 2.0 with 31 rows); the charter's Contents says V1 to
V11 (its table runs to V12).

**Budget.** 700,000,000 VND everywhere (charter title block and budget table, scope roll-up,
2.20, scope request, 1.3, tabs 0, 2, 5). Released 20% at M0, 25% at M3, 30% at M4, 25% at
M6. Lines: 1 personnel 539,000,000; 2 infrastructure, licences and store 42,000,000; 3
facilities, equipment and travel 14,000,000; 4 deployment, migration, training and
documents 42,000,000; 5 warranty months 2 to 6 35,000,000; 6 contingency reserve
28,000,000 (4%, against R1 to R12; the PM may draw up to 20,000,000 before escalating). No
management reserve; form 2B's Cost criterion still says "management reserve use reported
monthly". Team target 650,000,000 (2.20 and the scope request only).

**Cost estimate.** 646,009,000 VND at reduced scope (labor 587,661,000, physical 30,348,000,
reserve 28,000,000; 3,239.6 hours plus 160 support desk hours; range 449,726,000 to
905,316,000); full scope under the same rules 900,165,000. Vatten's estimate of 7 October:
1,450,419,000 and 1,735,946,000 with paid idle months. Rates: charter 19,600,000 per
person-month (PM 26,000,000, developer 19,000,000, QA 15,000,000), scope package hourly at
160 h per person-month (PM 162,500, DEV 118,750, QA 93,750, MOB 122,500), 2.20 hourly at the
ITviec median (PM 230,000, DEV 157,000, QA 139,000); the last replaces assumption 17 only if
the scope request is approved.

**Hours and structure.** 4,400 labor hours (PM, DEV1, DEV2, DEV3, QA1 800 each, MOB1 400),
27.5 person-months (25 core plus 2.5 mobile); 10 major deliverables, 24 control accounts,
78 work packages; three packages outside 8 to 80 hours (1.1.1.2 120 h, 1.10.1.1 400 h,
1.9.1.1 crosses M2). Levelled bookings (30 September run): PM 661, DEV1 874, DEV2 932, DEV3
846.9, QA1 770, MOB1 316; 93 divided activities.

**Milestones.**

| ID | Charter | Levelled forecast, 30 Sep (2.18, schedule request) | Doc request, 29 Sep (Thẻ 2) | 75% availability |
| --- | --- | --- | --- | --- |
| M0 | Mon 14 Sep 2026 | unchanged | unchanged | unchanged |
| M1 | Fri 2 Oct 2026 | Wed 28 Oct 2026 | Wed 28 Oct 2026 | Thu 12 Nov 2026 |
| M2 | Fri 16 Oct 2026 | Thu 12 Nov 2026 | Thu 12 Nov 2026 | Thu 3 Dec 2026 |
| M3 | Fri 13 Nov 2026 | Thu 10 Dec 2026 | Thu 10 Dec 2026 | Tue 12 Jan 2027 |
| M4 | Fri 11 Dec 2026 | Tue 12 Jan 2027 | Wed 13 Jan 2027 | Wed 24 Feb 2027 |
| M5 | Fri 18 Dec 2026 | Fri 5 Feb 2027 | Mon 8 Feb 2027 | Mon 29 Mar 2027 |
| M6 go-live | Tue 5 Jan 2027 | Tue 16 Feb 2027 | Wed 17 Feb 2027 | Fri 9 Apr 2027 |
| M7 closeout | Fri 5 Feb 2027 | Fri 19 Mar 2027 | Mon 22 Mar 2027 | Mon 10 May 2027 |

The reduced-scope levelling of 2.20 gives closeout 1 March 2027 with no M1 to M6 dates.
Warranty: six months from go-live, the first inside the project, months 2 to 6 to 5 July
2027 (about 9 October 2027 under the availability request). Lunar New Year assumed to start
6 February 2027. Today's date against these: M0 to M3 of the charter have passed by 14
November 2026, so any "at M1" or "before M2" action is stale (`review-lessons.md` section 9).

**People.** Sponsor Dr. Nguyễn Mạnh Hùng; customer Đỗ Thị Bích Ngọc, owner and Center
Director, who carries the lecturer's name (thread AAACHKhdaSM, a team question). Roles and
codes: Project manager (PM), also business analyst; Developer 1 to 3 (DEV1 to DEV3); QA
engineer (QA1); Mobile developer (MOB1), part-time 2.5 person-months, joins after M2. The
reduced 2.28 drops MOB1 and adds a support desk row.

**External parties.** Apple and Google (store review, R12), push notification provider,
SMS and email gateway provider, cloud hosting provider (Viettel IDC from 20 October;
`house-style.md`, External parties).

## 6. Pending change requests and who follows them

None of the three has a Disposition. While they are pending, every document follows the
charter and says what the request would change (`review-lessons.md` section 18).

| Request | Changes | Must follow if approved | Already applied (a finding while pending) |
| --- | --- | --- | --- |
| Schedule, 30 Sep (`docs/forms/3-3-change-request.en.md`) | M1 to M7 to the levelled forecast; five full-time staff for 30 more working days; budget line 1 up about 147,000,000 | charter milestones, Time criterion, budget line 1 and total, tranches; dictionary due dates; R8, R9; 2.18 becomes the baseline | 2.18 holds the forecast, labelled not baselined. The Doc has only the 29 Sep version, in Thẻ 2 |
| Scope and cost, 8 Oct (`docs/forms/3-3-change-request-scope.en.md`) | defer F07, F08, F12 (D11 and A12 leave, D4 becomes F06 and F09 to F11); fortnightly reports; warranty months 2 to 6 at 0.2 FTE, 160 h; ITviec rates replace assumption 17; company rules into the assumptions; the center provides the production server, gateway account and data entry; budget re-cut to 646,009,000; closeout 1 Mar 2027 | charter (functions, D4, D11, A01, A02, A09, A12, budget, assumption 17, Resources preassigned, business case, tranches); 2.32 (R6 raised, two new risks); scope package and `tools/check_scope.py`; 2.18 re-levelled; 2.20 becomes the basis of 2.22 | 2.32 adds R17 and R18; `origin/resource-tab` 2.27 to 2.29 and the Doc's tab 7 apply the reduction (C7) |
| Availability, 20 Oct (`availability-75` only) | amends the schedule request: levels at 6 productive hours a day (75%); M7 Mon 10 May 2027; 66 extra working days; DEV2 over the limit on 21 days, unresolved; cost about 323,400,000 on a person-month reading or none on an hours reading | as the schedule request, plus assumption 14 and 2.28 percent available | none |

A decision on any of them is recorded in 3.2 Decision Log and 3.4 Change Log, neither of
which exists yet.

## 7. Disagreements found on 14 November 2026

Re-check each before reporting it. None has been decided by the team.

- **C1 Sponsor and Center Director.** The charter source keeps them apart (assumption 16);
  tab 0's role table calls the Center Director "Owner and project sponsor"; Thẻ 2 names
  the sponsor "owner and Director of the learning center", lists him as Customer, and puts
  his name under Customer in Approvals.
- **C2 Iteration 2 scope.** Source D4 "F06 to F12"; tab 0 D4 "F06 to F11" while M4 in the
  same tab says F06 to F12.
- **C3 Schedule request, repo against Doc.** Repo 30 Sep: M6 Tue 16 Feb, M7 Fri 19 Mar
  2027, 30 working days, 93 divided activities, about 147,000,000. Doc (Thẻ 2) 29 Sep: M6
  Wed 17 Feb, M7 Mon 22 Mar 2027, 31 days, 97, about 152,000,000.
- **C4 Resource loading.** 2.18 source against the Thẻ 2 copy (29 Sep run).
- **C5 Submitted tabs cite a request that is not submitted.** Tab 4 cites "section 4.2";
  tabs 5 and 8 cite "the schedule change request of 30 September 2026"; only Thẻ 2 has a
  4.2, of 29 September.
- **C6 Closeout.** Five dates in circulation: 5 Feb (charter), 19 Mar (2.18 and tab 5),
  22 Mar (Thẻ 2), 1 Mar (reduced scope), 10 May 2027 (availability); 2.32's scales still
  measure schedule impact against go-live on 5 January 2027.
- **C7 Resource plan versions.** HEAD 2.27 to 2.29 (20 Oct, full scope) against
  `origin/resource-tab` and tab 7 (29 Oct, reduced scope). Tab 7 applies the pending
  request while tabs 6 and 8 and forms 1.3, 1.4 follow the charter; 1.3 rows S12, S14, S15,
  S16 carry the HEAD figures (MOB1 and test phones, 0.35 FTE and 35,000,000, gateway credit
  4,000,000, server 24,000,000 paid by the project).
- **C8 Who pays the production server.** Charter budget line 2 funds cloud server and
  staging for 12 months (24,000,000) while Resources preassigned says the Center Director
  commits one cloud virtual server; 2.20 and the scope request say the center provides it;
  `origin/resource-tab` 2.28 "provided and paid for by the center"; HEAD 2.28 and 1.3 say
  the project pays.
- **C9 Status report frequency.** Weekly (charter, 2.27 HEAD, 2.23, 1.3) against every two
  weeks (2.27 on `origin/resource-tab`, tab 7, scope request, 2.20).
- **C10 Warranty support.** 0.35 FTE and 35,000,000 (charter, tabs 0 and 3, HEAD 2.28,
  2.29, 1.3) against 0.2 FTE, 160 h, 25,120,000 (2.20, tab 5, tab 7): the second is the
  pending request's figure.
- **C11 Thẻ 2 against charter v3.1.** F01 to F11, D1 to D10, A01 to A11, R1 to R10, UAT at
  least 95% (v3.1: 99%), 70,000,000 management reserve (v3.1: 28,000,000 contingency), one
  month of warranty (v3.1: six), native mobile apps excluded (v3.1: F12 in scope), three
  Approvals columns (the form prints two).
- **C12 Tab 3 describes itself wrongly.** Its section 3.3 says "section 3.3 does the first,
  with 78 sheets", but holds the 24 control account sheets, identical to "dict rút gọn".
- **C13 README against the files** (scope package version and RTM count; deliverable list
  stops at four).
- **C14 Charter Contents** says V1 to V11; the prompt log runs to V12.
- **C15 Closeout before the warranty month.** Package 1.10.2.1 "Closeout report, lessons
  learned, and final acceptance" runs 15 to 17 Feb 2027 while the first warranty month
  1.10.1.1 runs to 19 Mar 2027 and M7 is 19 Mar (exit criterion 7 needs the warranty month
  first). `check_schedule.py` reports closeout before its warranty.
- **C16 Availability window.** Reduced 2.28 says full-time 14 Sep 2026 to 1 Mar 2027; the
  charter ends 5 Feb 2027; the full-scope forecast 19 Mar 2027.
- **C17 Team size against the brief.** 4 staff in 4 to 6 months (`docs/wbs_req.md`) against
  six people costed; explained in both files, not settled with the lecturer.
- **C18 Yellow in tab 0 differs from the source.** Ten assumed figures not yellow in the Doc
  (1,200 students, 35 teachers, 3 branches, subjects, 24 to 48 sessions, A03 volumes, A05
  "3 years", A06 "99%", the header names) and three headings yellow only in the Doc.
- Older items still to re-check: `review-lessons.md` section 6, "Open on 15 October 2026".

## 8. Comment threads

44 threads on 14 November, 1 resolved; no thread on tabs 4, 5, 6, 7 or "dict rút gọn". List
them with `tools/gdoc.py comments --doc <id>` or read `comments-by-tab.json` of a snapshot.

- **No reply from anyone but the author (15):** Vatten's AAACHhmz-DA (objective coding
  table, "Cho ngắn"), AAACHhmz-Cw (dictionary off format, too long), AAACHhmz-Cc (2.9 not a
  table, one phase, numbering), AAACHxbsu3Y (drop the reading convention?), AAACHhmz-Cs and
  AAACHhmz-Co (informational "Đã có"); the user's self-review threads of 16 September
  AAACHKhdaR0 (Prompt Log missing, still true), AAACHKhdaSM (customer named after the
  lecturer, still true), AAACHKhdaR4 and AAACHKhdaR8 and AAACHKhdaSA (Thẻ 2 faults,
  unchanged), AAACHKhdaSE (yellow convention, partly), AAACHKhdaSI (date formats, now
  fixed), AAACHKhdaRw and AAACHKhdaSQ (now fixed). A fixed thread still open is closed with
  a short reply saying where it was fixed.
- **Answered, waiting on the reviewer:** Đại Dũng Nguyễn's 2.32 thread of 4 November (which
  cell of the table is wrong, if not the header) and Vatten's of 5 November (what he
  disagrees with in R3; what "Cost out of scope" means). Both replies posted 10 November.
- **Answered on 16 September, never resolved:** the 26 threads of the first review
  (`review/2026-09-16-doc-review.md`). Thread AAACG0ldtiY (warranty at least 6 months) is
  answered, but Thẻ 2 still says one month.

## 9. Forms named but not produced

Missing against the brief: the prompt log in the Doc, the 78-sheet dictionary in the Doc
(or a stated reason for the summary), the `4.docx` or `4.pdf` submission file. Named by the
project's own documents as not yet produced: scope management plan, requirements and
resource management plans, procurement documents; activity list 2.12 and network diagram
2.15 (so no critical path, `review-lessons.md` section 16); cost management plan 2.19 and
cost baseline 2.22; resource calendars 2.26; risk management plan 2.31 (2.32 defines its
scales instead); stakeholder engagement plan 2.40; assumption log 1.2; decision log 3.2 and
change log 3.4 (needed the day a request is decided); quality audit 3.6; lessons learned
register; communications management plan, due at M1 as an internal deliverable.

## 10. Snapshot, compare, push

```bash
python3 tools/gdoc_dump.py --doc <doc id> --out <scratch>/snap     # read only: tabs/*.txt, comments-by-tab.json, doc.json, index.json
python3 tools/gdoc.py comments --doc <doc id>                      # threads with their anchors
python3 tools/gdoc.py auth                                         # when the refresh token has expired (invalid_grant)
```

The user gives the Doc ID; never write it into a file. In a tab file `<mark>` is yellow.
For a whole-Doc audit use the `audit-doc` workflow with the `doc-auditor` agent
(`.claude/workflows/audit-doc.js`, `.claude/agents/doc-auditor.md`): it snapshots the Doc,
unpacks this skill from branch `pm-skill`, audits each tab through form and content lenses,
lets skeptics refute findings, and renders the report with `tools/audit_report.py`. Running
it is a large multi-agent job; ask the user first. Each tab writer has its own flags
(`--create`, `--clear`, `--finish`, `--layout`); read its docstring, and audit the payload
(`push-audit.md`) and the live tab before a push. A tab write takes 10 to 20 minutes. To see
print layout, export the tab as PDF:
`https://docs.google.com/document/d/<id>/export?format=pdf&tab=<tab id>` with the OAuth
token.
