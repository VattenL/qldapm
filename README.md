# Learning Center Management Software: charter package

Coursework deliverable. Covers all four points of `requirement.md`. Document version 3.1.

The deliverable is Markdown. The shared Google Doc is a copy of it and is rebuilt from it, not edited by hand.

## Layout

```
docs/charter-package.en.md    English deliverable, the source of truth
docs/charter-package.vi.md    Vietnamese version, version 2.0, no longer maintained
docs/requirements.md          General (course-wide) requirement, 3 points
requirement.md                Team requirement, the same 3 points plus the prompt log
review/                       Replies to the team's review comments on the Google Doc, one file per round
tools/gdoc.py                 Google Docs and Drive API helper: comments, replies, rebuild of the Doc
tools/test_gdoc.py            Unit tests for the pure parts of the helper
tools/gdoc_edit.py            Markdown subset parser and index-safe in-place edits (blocks, cells, rows, columns)
tools/test_gdoc_edit.py       Unit tests for the parser
tools/apply_review_2026-09-16.py  Applies the version 3.1 content to the team's Doc copy in place, step by step
docs/assets/style.css         Print stylesheet, only used by the retired PDF pipeline
build/                        Old HTML and PDF output, retired
build.py                      Old Markdown to HTML to PDF pipeline, retired
```

## How the document answers the assignment

| Assignment point | Answered by | Source in the book |
| --- | --- | --- |
| 1. Requirement specification (short) | Part 1 | Form 2.8 Project Scope Statement, pages 58 to 59 |
| 2. Charter using the book's template | Part 2A and 2B | Table 1.1, pages 13 to 15; the form, pages 16 to 19 |
| 3. Fill in the form, empty or yellow where unknown | Part 2B | The form, pages 16 to 19 |
| 4. Prompt log with quality notes per version | Part 3 | Not from the book |

## Document structure

1. **Part 1, requirement specification.** Problem and scope, product, seven users and roles, twelve
   functions F01 to F12 each with a description, fourteen exception cases in 1.1.5, eleven deliverables
   D1 to D11 marked customer or internal plus the internal management deliverables, twelve acceptance
   criteria A01 to A12, product and project exclusions, constraints, and nineteen assumptions.
2. **Part 2A, charter elements.** All fourteen elements of Table 1.1 in the book's order, including
   the quantified business case, the six-month warranty terms, and the risk register R1 to R12 with a
   product or project type on each risk.
3. **Part 2B, the PROJECT CHARTER form.** The printed four-page form reproduced field for field and
   filled in, one section per printed page.
4. **Part 3, prompt log.** Twelve prompt versions with a quality assessment of each and the reason it
   was replaced, plus the lessons the sequence shows.

## Conventions

- All customer details and figures are assumptions, listed in section 1.6 and highlighted in place.
- `<mark>` is the only HTML in the file. It renders as a yellow highlight in GitHub, IDE previews, and
  most Markdown viewers, and is used per point 3 of the assignment: it marks content whose correctness
  cannot be confirmed from the brief. The file carries 87 markers. Content given by the brief (budget,
  duration, team size) and deliberate design decisions (F01 to F12, A01 to A12) are deliberately not
  marked, because they are choices rather than guesses.
- An empty box in the Part 2B form means the field cannot be completed until signing, per the same
  instruction. Only the project manager name and the signature and date fields are empty.
- Section 2B follows the printed form field for field and in the printed order. Keep the four page
  sections and their field order if the section is edited.
- Section 1.1.5 is not decoration. A requirement list that describes only success is the normal failure
  mode of this kind of document; if a function is added to 1.1.4, add what it does when it goes wrong.
- Project writing rules from `CLAUDE.md` apply: no em dashes, no emoji, no AI attribution in commits.

## Verified against the book

Text was extracted directly from `A_Project_Managers_Book_of_Forms.pdf` rather than recalled.

- **Table 1.1 element list (Part 2A).** All fourteen elements of section 1.1 are present in the book's
  order: project purpose, high-level project description, project boundaries, key deliverables,
  high-level requirements, overall project risk, project objectives and related success criteria,
  summary milestone schedule, preapproved financial resources, key stakeholder list, project approval
  requirements, project exit criteria, assigned project manager with responsibility and authority
  level, name and authority of the sponsor.
- **Four-page form (Part 2B).** All 36 printed labels are present in the printed order: 30 field names
  and the six labels of the signature block (signature, name, and date for the project manager and for
  the sponsor or originator). Note the page 1 pairing: Project Sponsor with Date Prepared, and Project
  Manager with Project Customer.
- **Second charter template (cross-check, not a target format).** The document was also checked against
  the worked charter example in Rita Mulcahy's *PMP Exam Prep*, which is not in this repository. Part 2B
  was deliberately not rewritten into that template: the assignment names the Book of Forms form, and
  PMBOK 6 section 4.1.3.1 lists the same fourteen elements Part 2A already follows.

## Internal consistency

Checked and holding as of version 3.1:

- Budget lines 539 + 42 + 14 + 42 + 35 + 28 = 700,000,000 VND; 27.5 person-months at 19,600,000 = 539,000,000;
  the infrastructure line itemises to 42,000,000.
- Milestone payments 20 + 25 + 30 + 25 = 100%.
- 14 Sep 2026 to 5 Feb 2027 = 144 days; M6 to M7 = 31 days; warranty 5 Jan to 5 Jul 2027 = 6 months;
  every milestone falls on the weekday stated.
- Staff base 35 teachers + 17 administrative = 52; the 80% training target reconciles with the 90% and
  75% sub-targets. Team of five plus one part-time mobile developer for 2.5 person-months, six people,
  inside the 4 to 6 the brief allows.
- Business case: notification cost 46.1M a year on SMS alone, 13.8M with push through the app; recurring
  benefit 90.6M a year net; one-off release 360M; cumulative net by year -249.4, -186.4, -123.4, -60.4,
  +2.6, so payback falls in year 5. The overdue balance is treated as a stock, not a flow.
- Function, deliverable, criterion, and risk ranges are F01 to F12, D1 to D11, A01 to A12, R1 to R12
  everywhere outside the historical statements of Part 3.

## Google Doc

The team's shared copy is Google Doc `1OTrxc3-L_t_NQcNiMG0EzwVsMU8Ftb7WFKuPSxHYgTw`. Review comments
on it are answered from the JSON files in `review/` and posted with `tools/gdoc.py`; the Markdown next
to each JSON is rendered from it for reading on GitHub.

Setup, once per machine:

1. In Google Cloud Console, an OAuth web client with redirect URI `http://localhost:8765/callback` and
   the scopes `https://www.googleapis.com/auth/documents` and `https://www.googleapis.com/auth/drive`
   on the consent screen (the account must be a test user while the app is unverified).
2. Save the client JSON as `~/.config/qldapm/client_secret.json`. It is never committed; `.gitignore`
   covers it and the token.

```bash
gdoc() { uv run --with google-api-python-client,google-auth-oauthlib,markdown tools/gdoc.py "$@"; }
gdoc auth                                                      # browser consent, once
gdoc comments --doc DOC_ID                                     # threads with the text each is anchored to
gdoc post --doc DOC_ID --review review/2026-09-16-doc-review.json --dry-run
gdoc post --doc DOC_ID --review review/2026-09-16-doc-review.json
gdoc render --review review/2026-09-16-doc-review.json --out review/2026-09-16-doc-review.md --title "..."
gdoc get --doc DOC_ID --out /tmp/doc.json --marks              # structure, and which runs and cells are shaded
gdoc import-html --md docs/charter-package.en.md --title "Charter package v3.1"   # new Doc from the source
gdoc replace --doc DOC_ID --md docs/charter-package.en.md --title "..."        # overwrite a Doc's content (version history keeps the old one)
python3 tools/apply_review_2026-09-16.py --doc DOC_ID --md docs/charter-package.en.md --dry-run   # in-place edits, tabs and comments kept
python3 -m unittest tools/test_gdoc.py
```

`post` is idempotent: a reply or comment whose first line already exists on the Doc is skipped.
`import-html` always creates a new Doc and never touches the reviewed one; `replace` and the apply script edit a
Doc in place (the apply script re-reads the Doc after every batch and skips steps already applied); comments are made through the
Drive API because the Docs API comment requests are still in Google's developer preview.

## History

Version 3.1 answers the team's review of 10 September 2026: 26 comments on the shared Doc, each traced to
a change or to a written reason in `review/2026-09-16-doc-review.md`, plus nine findings the reviewers
had not flagged. The largest changes are the mobile app F12, the six-month warranty, the budget re-cut,
the risk register with product and project types, and the 99 percent acceptance threshold. Part 3, V12,
records the round.

Version 3.0 restored two sections that version 2.1 had deleted: the filled four-page form and the
prompt log. Graded against `docs/requirements.md`, version 2.1 scored 49 out of 100, because it had
substituted the Table 1.1 element list for the prescribed form and dropped the fill-in requirement
entirely. Part 3, V10 and V11 record what happened and why.

## Vietnamese file

`docs/charter-package.vi.md` is the version 2.0 print-format translation. It still contains the `<div>`
and HTML-table constructs the English file has dropped, and it carries none of the changes from V7
onward. It is kept for reference only. If a Vietnamese deliverable is needed, retranslate from the
current English file rather than patching it.
