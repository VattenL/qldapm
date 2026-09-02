# Learning Center Management Software — charter package

Covers requirement 1 (requirement specification) and requirement 2 (project charter) of `requirement.md`.
Requirements 3 and 4 are not addressed yet.

## Layout

```
docs/charter-package.en.md    English source (Markdown, source of truth)
docs/charter-package.vi.md    Vietnamese source, same structure
docs/assets/style.css         A4 print stylesheet
build/charter-package.en.pdf  16 pages; charter form = pages 13-16
build/charter-package.vi.pdf  16 pages; charter form = pages 13-16
build.py                      Markdown -> HTML -> PDF
```

Each document has two parts:

1. **Requirement specification (short)** — product description, scope in/out, users and roles, 11 functions
   F01–F11 with descriptions, non-functional requirements N01–N08, technical approach, assumptions and constraints.
2. **Project charter** — first every element of Table 1.1 of *A Project Manager's Book of Forms* (3rd ed.),
   then the four-page PROJECT CHARTER form itself, filled and paginated to exactly 4 pages.

## Rebuilding the PDFs

```bash
pip install markdown        # only needed once
python build.py             # build every docs/*.md
python build.py en          # build only the English one
```

The pipeline renders the Markdown to a standalone HTML file with the CSS inlined, then prints it with
headless Chrome (`--print-to-pdf`). No LaTeX or Pandoc needed.

## Notes for later work

- All customer details and figures are assumptions, listed in section 1.7 of each document.
- `style.css` already defines `.unsure` / `<mark>` as a yellow background, ready for requirement 3
  ("leave the box background yellow when unsure").
- Keep the English and Vietnamese files structurally identical (same headings, same table rows) so they diff cleanly.
