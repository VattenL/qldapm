# Learning Center Management Software — charter package

Covers all four requirements of `requirement.md`. Document version 2.0.

## Layout

```
docs/charter-package.en.md    English source (Markdown, source of truth)
docs/charter-package.vi.md    Vietnamese source, same structure
docs/assets/style.css         A4 print stylesheet
build/charter-package.en.pdf  26 pages; charter form = pages 17-20
build/charter-package.vi.pdf  25 pages; charter form = pages 16-19
build.py                      Markdown -> HTML -> PDF
```

Each document has three parts:

1. **Requirement specification (short)** — product description, scope in/out, users and roles, 11 functions
   F01–F11 with descriptions, non-functional requirements N01–N08, technical approach, assumptions and constraints.
2. **Project charter** — first every element of Table 1.1 of *A Project Manager's Book of Forms* (3rd ed.),
   then the four-page PROJECT CHARTER form itself, filled and paginated to exactly 4 pages.
3. **Prompt log** — six prompt versions with a quality assessment of each and the reason it was replaced.

## Rebuilding the PDFs

```bash
pip install markdown        # only needed once
python build.py             # build every docs/*.md
python build.py en          # build only the English one
```

The pipeline renders the Markdown to a standalone HTML file with the CSS inlined, then prints it with
headless Chrome (`--print-to-pdf`). No LaTeX or Pandoc needed.

## Conventions

- All customer details and figures are assumptions, listed in section 1.7 of each document.
- `<mark>` renders as a yellow background (`style.css`) and is used per requirement 3: it marks content whose
  correctness cannot be confirmed from the brief. Content given by the brief (budget, duration, team size) and
  deliberate design decisions (F01–F11, N01–N08) are deliberately *not* marked. Both files carry 30 markers.
  The convention is explained to the reader in the header note of each document.
- Keep the English and Vietnamese files structurally identical so they diff cleanly. Both are currently
  526 lines / 36 headings / 118 table rows / 30 markers / 4 form pages. Check parity after any edit:

  ```bash
  for f in docs/charter-package.*.md; do
    printf "%s: lines=%s headings=%s rows=%s marks=%s\n" "$f" \
      "$(grep -c '' $f)" "$(grep -c '^#' $f)" "$(grep -c '^|' $f)" "$(grep -o '<mark>' $f | wc -l)"
  done
  ```

- The charter form must stay exactly 4 physical pages. After rebuilding, confirm the "Page N of 4" labels land
  on four consecutive PDF pages; adding rows to the form tables can silently push it to 5.

## Open item

The four-page form in Part 2B was reconstructed from the charter-element list. It has **not** been compared
field-by-field against pages 16–19 of `A_Project_Managers_Book_of_Forms.pdf`. Do that before submission and
reconcile any field the printed form has and this one lacks, or vice versa. This is also flagged at the end of
Part 3 in both documents.
