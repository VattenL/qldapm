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

## File layout

- Path: `docs/forms/<number>-<slug>.en.md`, for example
  `docs/forms/2-32-risk-register.en.md`.
- No YAML front matter. The charter uses bold key/value lines under the H1, and
  `tools/gdoc_edit.py` parses that shape.
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
customer, roles, functions F01-F12, deliverables D1-D11, acceptance criteria,
assumptions A01-A12, risks R1-R12, milestones M0-M7, budget breakdown and
stakeholders.

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
`tools/gdoc.py` or `tools/gdoc_edit.py`, never hand-edited: hand edits are how
the Doc fell 108 paragraphs behind its source.
