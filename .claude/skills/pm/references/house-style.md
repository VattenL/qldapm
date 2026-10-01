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
| 2.32 Owner and Responsible Party, 3.1 Responsible Party | a document that names the owner | Empty, and the missing owners listed as a question in the reply |
| 2.32 and 3.1 Status | the register itself: a new record is Open until a document records it done or closed | Plain `Open`, not marked; say once in the italic paragraph that no response is complete yet |
| 2.6 and 2.7 Priority | the requirements documentation | Copied; if every row has one value, say why once above the table |

### Dates on a form

**Date Prepared** (or **Date**) is the day the form file is written, in the
house format, not the date of the document it was built from. If the source's
version or date matters, name it in the italic paragraph ("built from the
charter as committed on 29 September 2026"). A regenerated form takes the day
it was regenerated.

## Writing

- English. `docs/charter-package.en.md` is the maintained source; the `.vi.md`
  file is retired and should not be extended.
- No em dashes. Use a comma, a semicolon or a full stop.
- No emoji anywhere.
- No decorative comment blocks or ASCII rules inside documents; `---` between
  major parts is the exception, since the charter already uses it.
- Field labels keep the book's capitalisation and wording exactly. The content
  beside them is ordinary sentence case.
- Dates: `2 September 2026`. No leading zero, month in full, one style per
  document. A weekday prefix (`Mon 14 September 2026`) only if every date in
  that table has one.
- Use the project's terms exactly as the budget defines them: the 28,000,000
  VND line is a **contingency reserve**, never a management reserve; the
  sponsor and the customer are named separately and never share a role word.

`scripts/check_consistency.py` reads the table below and reports each term in
the first column as an error, unless it is denied ("no management reserve").
Add a row here rather than a pattern in the script.

| Never write | Write instead | Why |
| --- | --- | --- |
| management reserve | contingency reserve | the 28,000,000 VND budget line is a contingency reserve |

## External parties the project depends on

A stakeholder list (1.3, 1.4, the charter's key stakeholder list) has a row for
every party a risk, a budget line or an assumption depends on, not only for the
people in the charter's stakeholder table (audit W5: R12 depends on Apple,
Google and the push provider, and no list named them). `check_consistency.py`
reads the table below: when another line of the files given names a party and
no first cell of a stakeholder list does, it warns. Add a row here when the
charter adds a supplier.

| External party | Written as | Why |
| --- | --- | --- |
| Apple, operator of the App Store | Apple; App Store | R12 store review, budget line 2 Apple Developer account, A12 |
| Google, operator of Google Play | Google Play | R12 store review, budget line 2 Google Play account, A12 |
| Push notification service | push service; push provider; push notification service | budget line 2 push service, BR05 push delivery |
| SMS and email gateway provider | gateway provider; SMS gateway; email gateway | R5, assumption 12 |
| Cloud hosting provider | hosting provider; cloud provider | budget line 2 cloud server, assumption 7 |

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

Facts that live there today: project title, budget (700,000,000 VND), duration
(5 months, 14 September 2026 to 5 February 2027), team composition, sponsor,
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

### Citing a section of another document

A form in `docs/forms/` has none of the charter's headings, so a bare "section
1.1.5" in it points nowhere. Name the document with the reference: "charter
section 1.1.5", "section 1.1.5 of the charter", or "Part 2 of
`docs/scope-package.en.md`". `check_consistency.py` accepts those three shapes
(the word charter up to three words before the number, or "of the charter" or
"of `<file>`" right after it) and checks a charter reference against the
charter's headings.

If a fact contradicts what the new form needs, report the contradiction instead
of silently choosing one. Two documents that disagree is a finding, not a
formatting problem.

The scope package, `docs/scope-package.en.md`, holds the RTM (2.7), WBS (2.9)
and 78-sheet WBS dictionary (2.10). Its totals are fixed by the charter and
`tools/check_scope.py` enforces them: 4,400 hours, 539,000,000 VND labor,
161,000,000 VND other cost, 700,000,000 VND in all. Resource codes are PM, DEV1
to DEV3, QA1 and MOB1. `docs/wbs_req.md` is the brief for that package and
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
