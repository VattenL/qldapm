# Auditing a generated form and the push pipeline

Read this when a document is generated rather than typed (form 2.18 by `tools/schedule.py`, the Doc tabs by the
`tools/gdoc_*` writers), or when documents are about to go to the team's Google Doc. A hand edit to a generated
file is lost on the next run, so the audit finds the defect and the Needs line names the generator or the
source document to change.

## Is the committed generated form current

`tools/schedule.py` has no `--out`: it writes into `docs/`. Regenerate it in a scratch copy and compare, so
`docs/` is never touched. The `--prepared` date is the form's own Date Prepared, as `YYYY-MM-DD`.

```bash
S=<scratchpad>/regen
mkdir -p $S/docs/forms $S/docs/assets
cp -R tools $S/tools
cp docs/scope-package.en.md docs/charter-package.en.md $S/docs/
uv run --with matplotlib $S/tools/schedule.py --prepared 2026-09-29
diff $S/docs/forms/2-18-project-schedule.en.md docs/forms/2-18-project-schedule.en.md
```

No output from `diff` means the committed file is what the generator emits from the current sources. Run each
command on its own and report each exit code. Then audit the file as an ordinary document:

```bash
python3 .claude/skills/pm/scripts/check_schedule.py docs/forms/2-18-project-schedule.en.md \
    --charter docs/charter-package.en.md --scope docs/scope-package.en.md
```

`check_schedule.py` is the mechanical form of the sequence and load checks: a review, approval, acceptance,
sign-off, walkthrough or verification that finishes before the work it checks (the rows are leads; read both),
rows dated inside a break the charter rules out, and booked hours per person against the hours the cost
estimate prices, with the difference priced at the dictionary rates. It also finds a closeout before the warranty it
closes and a go-live before the UAT ends. It does not see the rest (a test of a function before its build, a use of
something no row has created yet), which are read by the recipe in `audit-template.md` (Used before it exists). A pending
3.3 explains a date or an hour total (`--explained hours`), never an order: `--explained sequence=REASON` needs the reason
the order changed.

View every generated image (the Gantt pages, the milestone chart, the histogram) with the Read tool: a chart can
disagree with the table it was drawn from. `references/load-check.md` covers hours per week; it assumes
dictionary dates and `tools/level.py`, so it does not check the levelled schedule's load.

## Auditing the push pipeline

What reaches the Doc is what the generator emits. Tab 3 of the Doc once fell 108 paragraphs behind its source
because the generator dropped them, not because anyone edited the Doc (`review-lessons.md` section 10). So audit
the payload as well as the source:

| Part of the Doc | Payload built by | Written by |
| --- | --- | --- |
| Whole document (one tab only) | `tools/gdoc.py` (Markdown to HTML) | `gdoc.py replace` or `import-html` |
| Scope baseline tab | `python3 tools/scope_tab3.py --out <scratch>/tab3.md` | `tools/gdoc_tab3.py`, `tools/gdoc_scope_sync.py` |
| Schedule tab (2.18, 3.3) | `gdoc_schedule_tab.build()` | `tools/gdoc_schedule_tab.py` |
| Charter tab (1.1 and its package) | `docs/charter-package.en.md` itself; its HTML is `uv run --with markdown python3 -c "import sys; sys.path.insert(0, 'tools'); import gdoc; print(gdoc.md_to_html(open('docs/charter-package.en.md', encoding='utf-8').read(), 'charter'))" > <scratch>/charter.html` | `gdoc.py replace` or `import-html` |

1. Build the payload into the scratchpad without credentials. Prefix every Python run that imports from `tools/` with
   `PYTHONDONTWRITEBYTECODE=1`, or the import writes `tools/__pycache__` into a tree an audit must not change:
   `python3 tools/scope_tab3.py --out <scratch>/tab3.md`;
   `PYTHONDONTWRITEBYTECODE=1 python3 -c "import sys; sys.path.insert(0, 'tools'); import gdoc_schedule_tab as g; print(g.build())" > <scratch>/schedule-tab.md`;
   `python3 tools/gdoc_tab3.py --doc DOC_ID_NOT_GIVEN --dry-run` or
   `python3 tools/gdoc_schedule_tab.py --doc DOC_ID_NOT_GIVEN --dry-run` for the units. A dry run needs no credentials, but
   argparse still wants a `--doc` value: write the literal placeholder `DOC_ID_NOT_GIVEN`, which no Doc has, and never a
   guessed Doc ID (SKILL.md, step 7). With no Doc ID given, say in Method that the live Doc and its comments were not audited.
2. Compare the payload's headings with the source's, and list what the generator drops, renames or adds. A rule,
   reading note or label that the source states and the payload drops is an error if the Doc relies on it.
   The charter has no generator between the source and the Doc: the Markdown is the payload, and the conversion only adds
   the page breaks before each `PROJECT CHARTER, page N of 4` heading and turns `<mark>` into a yellow span. Count the
   `page-break-before` divs in the HTML (4 on 15 October 2026) and the `<span style="background-color:#ffff00">` spans
   against the `<mark>` count of the source.
3. Run `check_fidelity.py` and `check_consistency.py` on the payload too (for a payload that holds two forms, such as
   2.18 with 3.3, run `check_fidelity.py` once per form with `--section` and `--end`: the schedule tab's headings are
   `--section "4.1 Project Schedule" --end "4.2 Change Request"` for the 2.18 half (8 of 8 labels, with the
   resource table's headers listed as unprinted) and `--section "4.2 Change Request"` for the 3.3 half. The 3.3 half
   returns about 3 of 50 labels, which is expected and not a defect: the tab writes the form as label and value pairs
   and puts each checkbox group on one line, which the checker does not read. Audit that half against the committed
   `docs/forms/3-3-change-request.en.md`, which passes 44 of 50 for the same reason (its six missing labels are the
   checkbox groups written on one line). The scope tab (`<scratch>/tab3.md`) takes `check_fidelity.py <tab3.md> 2.7 --section "3.1 Requirements Traceability Matrix" --end "3.2 Work Breakdown Structure" --flattened`,
   `... 2.9 --section "3.2 Work Breakdown Structure" --end "3.2.3 Roll-up"` (ending later takes in the Roll-up table and lists labels that are not 2.9's) and `... 2.10 --flattened`. Run `check_consistency.py` once
   on the whole payload; the `form-note` warning for the 3.3 half is the 3.3 page prose between its page headings and
   is expected to be listed, with `section-ref`): a generator can add a label the printed
   form does not carry. A tab payload gives `section-ref` warnings of the kind "section 3.3 is not here but in
   <source file>" (the payload refers to a section that lives in a source file or another tab); they were
   2, 3, 3.3 and 4 for the schedule and scope tabs. Read each, list the ones that are only cross-document
   pointers as expected, and do not count them as defects.
4. Check the markup against the subset `tools/gdoc_edit.py` parses (headings `#` to `####`, paragraphs, `- ` and
   `1. ` items, `> ` quotes, pipe tables, `---` (only after a blank line: a `---` directly under a table row is read as a rule by
`gdoc_edit.parse_blocks` but rendered as a stray `---` cell by `gdoc.md_to_html`; `check_consistency.py` reports it as `table-rule`), `**bold**`, `*italic*`, `` `code` ``, `<mark>`). Anything else
   arrives in the Doc as literal text, as `<br>` did 23 times. `gdoc.py replace` re-imports the whole file and
   collapses a multi-tab Doc to one tab, so it is never the way to update the team's Doc.
5. After a push, `tools/gdoc.py get --doc <id> --out <scratch>/doc.json --marks` lists the highlighted runs;
   their count should match the `<mark>` spans in the payload.

The Google tools need `uv run --with google-api-python-client,google-auth-oauthlib,markdown`.
