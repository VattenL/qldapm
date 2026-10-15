# House style for generated documents

These conventions come from `docs/charter-package.en.md`, `README.md` and
`CLAUDE.md`. A generated form that ignores them creates review work for the team
rather than saving it.

## Never invent a value

This is the rule that matters most. `CLAUDE.md` forbids hardcoded or guessed
values, and a PM document full of plausible fabrications is worse than an empty
one, because nobody can tell which numbers are real.

Three states, three markings:

| State | How to write it |
| --- | --- |
| Known from a project document or from the user | Plain text |
| Assumed, inferred or not yet confirmed | Wrap in `<mark>...</mark>` |
| Not known and not inferable | `[TBD]`, or an empty table cell where the form expects one value |

Which unknown marking to use: an empty cell for each cell of a register grid that has no source (probability, impact and score of 2.32 before a scoring
session); `[TBD]` only for a single box, or where an empty cell would read as an oversight. One document uses one of the two for the same kind of cell, and
the italic paragraph says which and why once.

`<mark>` is the only HTML allowed in these documents. `tools/gdoc.py` turns it
into a yellow highlight in the Google Doc, which is how the course requires
assumed content to be flagged, so it is load-bearing rather than decorative.

When a value is assumed, say what it was inferred from in the same cell if that
fits in a clause. A reviewer who can see the reasoning can confirm or reject it
in one pass.

### Judgement columns

Some columns hold a judgement rather than a fact. A judgement is filled only
from a source that makes it; a value you derive is inside `<mark>` and the rule
that derived it is stated once in the italic paragraph above the form. With
neither, the cell is empty and the italic paragraph says where the value will
come from.

| Column | Filled from | When no source gives it |
| --- | --- | --- |
| 1.3 Classification | 1.4 Stakeholder Analysis, or the user | Empty, with 1.4 named as its source. A first pass derived by a stated rule, inside `<mark>`, only when the user asks for one |
| 1.4 Power, Interest, Influence, Impact | the user or a stakeholder workshop | Empty |
| 2.32 and 2.36 Probability, Impact, Score | a scoring session (2.31 definitions, 2.34, 2.35) | Empty, or `[TBD]` |
| 2.32 Owner and Responsible Party, 3.1 Responsible Party, 3.2 Responsible Party | a document that names a person as the owner | Empty, and the missing owners listed as a question in the reply. A role the charter has not filled (a project manager "to be assigned") does not count, a risk response that says "name the Accountant as benefit owner" or "sponsor-approved replacement" is a response and not an owner, and the Responsible Person of a WBS dictionary sheet owns that package's work, not a risk or a decision |
| 2.32 and 3.1 Status | the register itself: a new record is Open until a document records it done or closed | Plain `Open`, not marked; say once in the italic paragraph that no response is complete yet |
| 2.6 and 2.7 Priority | the requirements documentation | Copied; if every row has one value, say why once above the table |

### Dates on a form

**Date Prepared** (or **Date**) is the day the form file is written, in the
house format, not the date of the document it was built from. If the source's
version or date matters, name it in the italic paragraph ("built from the
charter as committed on 29 September 2026"). A regenerated form takes the day
it was regenerated. A blank template has no document date, so its Date Prepared
stays empty (SKILL.md step 4); the day is written when the form is filled. When
the form is built from a charter that is committed in git, name the commit date
in the italic paragraph in the same words; when the charter has uncommitted
changes, say "built from the charter as it stood on <today>, not yet committed".

## Writing

- English. `docs/charter-package.en.md` is the maintained source; the `.vi.md`
  file is retired, stale (it still calls its reserve line a management reserve for
  R1 to R8, where the maintained file has R1 to R12 and a contingency reserve) and
  is never quoted or extended. An answer in Vietnamese keeps the book's English
  labels and form numbers beside the Vietnamese words (table below).
- No em dashes. Use a comma, a semicolon or a full stop.
- No emoji anywhere.
- No decorative comment blocks or ASCII rules inside documents; `---` between
  major parts is the exception, since the charter already uses it.
- Field labels keep the book's capitalisation and wording exactly. The content
  beside them is ordinary sentence case.
- Dates: `2 September 2026`. No leading zero, month in full, one style per
  document. A weekday prefix (`Mon 14 September 2026`) only if every date in
  that table has one.
- Use the project's terms exactly as the budget defines them: the reserve
  budget line is a **contingency reserve**, never a management reserve; the
  sponsor and the customer are named separately and never share a role word.

`scripts/check_consistency.py` reads the table below and reports each term in
the first column as an error, unless it is denied ("no management reserve").
Add a row here rather than a pattern in the script.

| Never write | Write instead | Why |
| --- | --- | --- |
| management reserve | contingency reserve | the reserve budget line is a contingency reserve |

### Vietnamese terms

A reply in Vietnamese writes the printed label as the book prints it, then the Vietnamese word. These renderings are the skill's, not the book's; the charter's own
Vietnamese wording, where one exists in a maintained file, wins. Rules for the whole reply: every form title and number stays in English as printed, with the Vietnamese in brackets after it
(`Change Log (nhật ký thay đổi)`, `2.7 Requirements Traceability Matrix (ma trận truy vết yêu cầu)`), and no title is dropped or only translated; the technique names and the printed field labels stay
in English; the Vietnamese keeps its diacritics, as the maintained charter and the Doc do (write them in full); a page is written
"trang in 215 (trang PDF 254)".

| Book term | Vietnamese in a reply | Note |
| --- | --- | --- |
| Change Request (form 3.3) | yêu cầu thay đổi | the form name stays "Change Request" |
| contingency reserve | quỹ dự phòng rủi ro (contingency reserve) | inside the cost baseline, for identified risks |
| management reserve | dự phòng quản lý (management reserve) | outside the cost baseline; the project's money is not this |
| baseline | đường cơ sở | scope, schedule and cost baselines |
| variance threshold | ngưỡng sai lệch | read from the charter or 2.1, never invented |
| float (total float) | thời gian dự trữ (float) | |
| crashing | đẩy nhanh bằng thêm nguồn lực (crashing) | keep the English technique name |
| fast tracking | thực hiện chồng lấn (fast tracking) | keep the English technique name |
| resource leveling, resource smoothing | cân bằng nguồn lực, làm mượt nguồn lực | keep the English technique names |
| BAC, PV, EV, AC, CV, SV, CPI, SPI, EAC, ETC, VAC, TCPI | keep the abbreviation, then the Vietnamese once: chỉ số hiệu suất chi phí (CPI), chỉ số hiệu suất tiến độ (SPI), ước tính khi hoàn thành (EAC), chỉ số hiệu suất cần đạt (TCPI) | the Table 7-1 words stay as printed in English beside it (over planned cost, behind schedule, harder to complete) |
| critical path, schedule compression | đường găng, nén tiến độ | keep the technique names crashing and fast tracking |
| risk register, risk response | sổ đăng ký rủi ro (Risk Register), biện pháp ứng phó rủi ro | the form name stays "Risk Register" |
| avoid, transfer, mitigate, accept, escalate | tránh, chuyển giao, giảm thiểu, chấp nhận, báo cáo lên cấp trên | keep the English strategy name in brackets; opportunities: exploit, share, enhance |
| contingency plan, fallback plan | kế hoạch dự phòng (contingency plan), kế hoạch thay thế (fallback plan) | keep the English names |
| change control board | hội đồng kiểm soát thay đổi (change control board) | the charter names none here: say so, invent none |
| Issue Log, Decision Log | nhật ký vấn đề, nhật ký quyết định | the form names stay in English |

## External parties the project depends on

A stakeholder list (1.3, 1.4, the charter's key stakeholder list) has a row for
every party a risk, a budget line or an assumption depends on, not only for the
people in the charter's stakeholder table (audit W5: R12 depends on Apple,
Google and the push provider, and no list named them). `check_consistency.py`
reads the table below: when another line of the files given names a party and
no first cell of a stakeholder list does, it warns. Add a row here when the
charter adds a supplier.

| External party | Written as | Why | Position or role in 1.3 |
| --- | --- | --- | --- |
| Apple, operator of the App Store | Apple; App Store | R12 store review, budget line 2 Apple Developer account, A12 | Operator of the App Store |
| Google, operator of Google Play | Google Play; Google | R12 store review, budget line 2 Google Play account, A12 | Operator of Google Play |
| Push notification service | push service; push provider; push notification service | budget line 2 push service, BR05 push delivery | Push notification service provider |
| SMS and email gateway provider | gateway provider; SMS gateway; email gateway | R5, assumption 12 | SMS and email gateway provider |
| Cloud hosting provider | hosting provider; cloud provider | budget line 2 cloud server, assumption 7 | Cloud hosting provider |

### Form 1.3 Stakeholder Register: fill rules

- **Requirements and Expectations come from the charter's sentences, copied as written.** The sponsor's Expectations cell holds the sponsor's own success criteria or objectives from the charter's objectives table, each as written and no more
  than the charter says; a long cell is the charter's length, so add nothing and do not summarise.
- **When the charter's group name differs from the register's rows** (the charter says "Parents and teachers" where the rows are "Students and parents" and "Head Teacher"), put a sentence in the row whose role it names and
  split a group only where the sentence itself names the roles; otherwise leave the cell empty and list the mapping as a question. Never copy one sentence into two rows without saying so in the italic paragraph.
- **Marking.** A cell copied from an assumption, a budget line or a risk is copied text, not marked; a value inferred or derived (a classification, a trimmed summary) is inside `<mark>`. Trimming a source phrase is not copying as
  written: copy the whole phrase, or mark the trimmed cell and name the source.
- **Position or role of an external party** is the last column of the table above, so two runs write the same words.

## File layout

- Path: `docs/forms/<number>-<slug>.en.md`, for example
  `docs/forms/2-32-risk-register.en.md`.
- No YAML front matter. The two package documents,
  `docs/charter-package.en.md` and `docs/scope-package.en.md`, open with bold
  key/value metadata under the H1 (`**Project:**`, `**Date prepared:**`), and
  `tools/gdoc_edit.py` parses that shape. That is allowed only there, because
  a package is not a form. A form file in `docs/forms/` has no metadata lines:
  its only bold lines under the H1 are the printed title block
  (`**Project Title:**`, `**Date Prepared:**`, or `**Date:**` where that is
  what the form prints), none at all where the form prints none (2.3, 2.18),
  and the citation goes in the italic paragraph. So `**Project:**`, `**Date
  prepared:**` or `**Source:**` in a form file is a defect, generated or not;
  `check_fidelity.py` lists them as unprinted labels. See `rendering.md`.
  The first forms in `docs/forms/` (2-18 and 3-3) predate
  this rule and carry those three lines. That is a known tailoring of the older
  files: a new form follows the printed labels, and an audit reports the older
  files as a warning that names this rule, not as an error.
- Heading levels: `#` document title, `##` major part, `###` numbered section,
  `####` printed page boundary (`FORM NAME, page N of M`).
- Pipe tables throughout, with a `| --- |` separator row. Keep them readable in
  raw Markdown; do not pad cells to align columns.

## Consistency with what already exists

Before writing, read the project facts out of `docs/charter-package.en.md`.
`tools/gdoc_edit.py` already parses this exact subset, so import it rather than
writing a second parser:

```python
import sys; sys.path.insert(0, "tools")
from gdoc_edit import section, first_table, table_by_first_cell, field_map
md = open("docs/charter-package.en.md").read()
facts = field_map(first_table(section(md, "#### PROJECT CHARTER, page 1 of 4",
                                      "#### PROJECT CHARTER, page 2 of 4")))
```

Facts that live there: project title, budget, duration (start and end dates),
team composition, sponsor,
customer, roles, functions F01-F12, deliverables D1-D11, acceptance criteria
A01-A12 (section 1.3), assumptions 1-19 (section 1.6, numbered without a
letter), risks R1-R12, milestones M0-M7, budget breakdown and stakeholders.
`A` stands for acceptance criterion, never for assumption; an assumption is
cited as "assumption 18".

Where the registers are, so nobody searches:

| Facts | Heading in `docs/charter-package.en.md` | Shape |
| --- | --- | --- |
| Risks R1 to R12 | `#### Overall project risk` in Part 2A | columns `# \| Type \| Risk \| Response`: the ID column is headed `#`, and Type (Product or Project) is a column no printed risk form has |
| Milestones M0 to M7 | `#### Summary milestone schedule` in Part 2A, and form 1.1 page 3 in 2B | weekday dates |
| Budget lines 1 to 6 | `#### Preapproved financial resources` in Part 2A | `# \| Category \| Amount (VND) \| Share \| Basis` |
| Stakeholders | `#### Key stakeholder list` in Part 2A, and the Stakeholder(s) table on form 1.1 page 3 in 2B | two copies that differ in wording; see "When a source disagrees with itself" |
| Assumptions 1 to 19 | `### 1.6 Project Assumptions` in Part 1 | `# \| Assumption` |

### When a source disagrees with itself

The charter carries some facts twice, in Part 2A and in the printed form of
Part 2B, and the two copies do not always match (2A's stakeholder list says
"Notification gateway provider" and "Head Teacher", 2B's says "SMS and email
gateway provider" and "Head Teacher, teacher representative"). Copy from the
copy that belongs to the form your form aligns with, which for a form built
from the charter is the printed form in 2B; say in the italic paragraph which
copy you used; and report the difference to the user as a finding. Do not
merge the two wordings.

### Citing the books in a document

Write a PMBOK section as `PMBOK 6 section 11.5.2.1, printed page 442 (PDF page
481)` and a Book of Forms page as `Book of Forms form 2.32, PDF page 141
(printed page 130)`; both page numbers, always. `check_consistency.py` does not
treat a section number in a clause that names PMBOK, the Guide or the Book of
Forms as a section of the project document, even with a page in between.

### Citing a section of another document

A form in `docs/forms/` has none of the charter's headings, so a bare "section
1.1.5" in it points nowhere. Name the document with the reference: "charter
section 1.1.5", "section 1.1.5 of the charter", or "Part 2 of
`docs/scope-package.en.md`". `check_consistency.py` accepts those three shapes
(the word charter up to three words before the number, or "of the charter" or
"of `<file>`" right after it) and checks a charter reference against the
charter's headings. The reference word is "section" or "Part"; a letter belongs to
the number (`2B`), so "section 2B" in a form warns (a form has no such heading)
while "Part 2B of the charter" passes. When a reference warns, rewrite it in one of
the three shapes rather than silencing it.

If a fact contradicts what the new form needs, report the contradiction instead
of silently choosing one. Two documents that disagree is a finding, not a
formatting problem.

The scope package, `docs/scope-package.en.md`, holds the RTM (2.7), WBS (2.9)
and 78-sheet WBS dictionary (2.10). Its totals are fixed by the charter and
`tools/check_scope.py` enforces them (hours, labor, other cost and the budget
in all). Resource codes are PM, DEV1 to DEV3, QA1 and MOB1. `docs/wbs_req.md` is the brief for that package and
records which class notes were checked against the book.

When the Markdown changes, the Google Doc is regenerated from it with
`tools/gdoc.py` or `tools/gdoc_edit.py`, never hand-edited. Regenerating is not
a guarantee, though: the Doc's tab 3 fell 108 paragraphs behind its source
(audit E9) because the generator, `tools/scope_tab3.py`, dropped everything
before Part 1 and turned the WBS outline into a table (audit E8), not because
anyone edited the Doc. Commit ff3cbb0 changed it to keep four front sections
and emit the outline, and it still drops the rest of the front matter by
design. So before a push, build the payload locally (`python3
tools/scope_tab3.py --out <scratch>/tab3.md`) and read or check that, not
only the source.
