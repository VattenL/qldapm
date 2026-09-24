#!/usr/bin/env python3
"""Write the scope baseline into a third tab of the team's Google Doc.

The target tab is found by title; with --create it is added through the Docs API when missing. This
script only fills that tab, and never touches the other tabs. It does not use 'gdoc.py replace', which re-imports the whole file through Drive and would
collapse the Doc to a single tab, destroying Thẻ 1 and Thẻ 2.

The payload is derived from docs/scope-package.en.md by tools/scope_tab3.py; nothing is authored here.

Work is split into units: one for the matrix and the structure, then one per dictionary sheet. Each
unit is checked against what the tab already contains, so an interrupted run can simply be repeated
and it will carry on where it stopped.

Run with:
    python tools/gdoc_tab3.py --doc DOC_ID --dry-run          # plan only, no credentials needed
    python tools/gdoc_tab3.py --doc DOC_ID --tab "Thẻ 3"
    python tools/gdoc_tab3.py --doc DOC_ID --limit 5          # write the first few units only
"""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import gdoc_edit as ge
import gdoc_form
import scope_tab3

# Column widths in points, for a landscape A4 page with the Doc's default margins, about 698pt of
# usable width. Without these the Doc distributes columns evenly and the prose columns of the
# traceability matrix end up the same width as its ID column.
RTM_WIDTHS = [34, 130, 62, 48, 52, 96, 70, 100, 98]
INTER_WIDTHS = [40, 160, 55, 80, 40, 160, 55, 80]
ACTIVITY_WIDTHS = [62, 190, 55, 45, 55, 65, 40, 55, 60, 65]

RTM_GROUPS = [("Requirement Information", 0, 5), ("Relationship Traceability", 5, 4)]


def sheet_is_sound(doc, tab_n, anchor):
    """True when the sheet just written has its ten-column activity table, in the right place.

    The Docs API occasionally serves a read that predates the previous write. When that happens the
    placeholder a table is built over is located at a stale index, and the table is created with the
    wrong shape and in the wrong position. It is rare, it is not deterministic, and it corrupts the
    sheet silently, so every sheet is checked before its layout is applied.
    """
    _tab_id, content = doc.tab(tab_n)
    head = ge.find_para(content, lambda s: s.strip() == anchor)
    if head is None:
        return False
    after = [el for el in ge.top_tables(content) if el["startIndex"] > head["startIndex"]]
    return any(len(ge.table_cells(el)[0]) == 10 for el in after)


def drop_from_heading(doc, tab_n, anchor):
    """Delete a heading and everything after it, so the unit can be written again."""
    tab_id, content = doc.tab(tab_n)
    head = ge.find_para(content, lambda s: s.strip() == anchor)
    if head is None:
        return False
    end = content[-1]["endIndex"] - 1
    if end > head["startIndex"]:
        doc.delete_range(tab_id, head["startIndex"], end)
    return True


def apply_layout(doc, tab_n, unit_name):
    """Give the tables of a freshly written unit the printed-form layout."""
    if unit_name == "3.1 matrices":
        gdoc_form.apply_form(doc, tab_n, "ID", "REQUIREMENTS TRACEABILITY MATRIX",
                             groups=RTM_GROUPS, widths=RTM_WIDTHS, ncols=9)
        gdoc_form.apply_form(doc, tab_n, "ID", "INTER-REQUIREMENTS TRACEABILITY MATRIX",
                             widths=INTER_WIDTHS, ncols=8)
    elif unit_name[:2] == "1.":
        tab_id, content = doc.tab(tab_n)
        table_el = gdoc_form.find_table(content, "ID", ncols=10, last=True)
        if table_el is not None:
            doc.batch(gdoc_form.column_widths(tab_id, table_el, ACTIVITY_WIDTHS))

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_DIR = os.path.expanduser("~/.config/qldapm")
SHEET_HEADING = re.compile(r"^##### (1(?:\.\d+){3} .+)$", re.M)
PHASE_HEADING = re.compile(r"^#### 3\.3\.\d+ ", re.M)


# The opening part is cut at section boundaries so that page orientation can follow the content.
# A table of nine columns of prose is unreadable in portrait, which is why the printed form 2.7 is
# landscape in the book. (name, heading prefix, landscape)
OPENING = [
    ("lead", "## 3: Scope Baseline", False),
    ("3.1 matrices", "### 3.1 ", True),
    ("3.2 method and structure", "### 3.2 ", True),
    ("3.2.3 roll-up", "#### 3.2.3 ", True),
    ("3.2.4 coverage", "#### 3.2.4 ", False),
    ("3.3 dictionary intro", "### 3.3 ", True),
]


def split_units(payload: str):
    """Return [(name, anchor, markdown, landscape)].

    The opening sections are cut where the page orientation changes; then one unit per dictionary
    sheet. A phase heading is carried by the sheet that follows it, so a resumed run never orphans
    one.
    """
    starts = [m.start() for m in SHEET_HEADING.finditer(payload)]
    if not starts:
        raise SystemExit("no dictionary sheets found in the payload")
    bounds = []
    for pos in starts:
        phase = None
        for m in PHASE_HEADING.finditer(payload, 0, pos):
            phase = m
        bounds.append(phase.start() if phase and phase.start() > (bounds[-1] if bounds else 0) else pos)

    cuts = []
    for name, prefix, landscape in OPENING:
        at = payload.find("\n" + prefix) + 1 if payload.find("\n" + prefix) >= 0 else payload.find(prefix)
        if at < 0:
            raise SystemExit("opening section %r not found in the payload" % prefix)
        cuts.append((at, name, landscape))
    cuts.sort()

    units = []
    for k, (at, name, landscape) in enumerate(cuts):
        end = cuts[k + 1][0] if k + 1 < len(cuts) else bounds[0]
        chunk = payload[at:end].rstrip() + "\n"
        anchor = chunk.splitlines()[0].lstrip("#").strip()
        units.append((name, anchor, chunk, landscape))

    for k, start in enumerate(bounds):
        end = bounds[k + 1] if k + 1 < len(bounds) else len(payload)
        chunk = payload[start:end].rstrip() + "\n"
        heading = SHEET_HEADING.search(chunk).group(1)
        units.append((heading.split()[0], heading, chunk, True))
    return units


def tab_index_by_title(doc, title: str):
    for n, (name, _tab_id, _content) in enumerate(doc.tabs()):
        if name.strip() == title.strip():
            return n
    have = ", ".join(repr(t[0]) for t in doc.tabs())
    raise SystemExit(
        "no tab named %r in this Doc; tabs present: %s\n"
        "Run again with --create to add it." % (title, have))


def tab_headings(doc, tab_n: int):
    """The heading paragraphs already in the tab, as a set of their plain text.

    Matching on headings only, and on the whole heading rather than on the code it starts with,
    keeps a code that merely appears in the structure table of section 3.2 from being mistaken for
    the dictionary sheet that carries it.
    """
    out = set()
    for el in ge.top_paragraphs(doc.content(tab_n)):
        style = el["paragraph"].get("paragraphStyle", {}).get("namedStyleType", "")
        if style.startswith("HEADING"):
            out.add(ge.para_text(el).strip())
    return out


def end_of_tab(doc, tab_n: int) -> int:
    """Index of the start of the trailing paragraph, which is where new content is appended."""
    return doc.content(tab_n)[-1]["endIndex"] - 1


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--doc", required=True)
    p.add_argument("--tab", default="Thẻ 3")
    p.add_argument("--md", default=str(ROOT / "docs" / "scope-package.en.md"))
    p.add_argument("--token", default=os.path.join(DEFAULT_DIR, "token.json"))
    p.add_argument("--create", action="store_true", help="add the tab when the Doc has none by that title")
    p.add_argument("--clear", action="store_true",
                   help="empty the target tab before writing; only that tab is touched")
    p.add_argument("--limit", type=int, default=0, help="write at most this many units")
    p.add_argument("--sleep", type=float, default=1.0, help="seconds between units, to stay inside quota")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args(argv)

    payload = scope_tab3.build(pathlib.Path(a.md).read_text(encoding="utf-8"))
    units = split_units(payload)
    tables = sum(1 for u in units for b in ge.parse_blocks(u[2]) if b["type"] == "table")
    print("payload: %d characters, %d units, %d tables, about %d write calls"
          % (len(payload), len(units), tables, tables * 2 + len(units)))

    if a.dry_run:
        for name, anchor, chunk, landscape in units[:10]:
            print("  unit %-24s %-9s %5d chars  %s"
                  % (name, "landscape" if landscape else "portrait", len(chunk), anchor[:50]))
        if len(units) > 10:
            print("  ... and %d more units" % (len(units) - 10))
        print("dry run: nothing written")
        return 0

    import gdoc

    creds = gdoc.load_creds(pathlib.Path(a.token))
    doc = ge.Doc(gdoc.docs(creds), a.doc)
    if a.create and a.tab.strip() not in [t[0].strip() for t in doc.tabs()]:
        doc.batch([{"addDocumentTab": {"tabProperties": {"title": a.tab}}}])
        doc.refresh()
        print("  created tab %r" % a.tab)
    tab_n = tab_index_by_title(doc, a.tab)
    print("writing into tab %d (%r) of %r" % (tab_n, a.tab, a.doc))

    if a.clear:
        tab_id, content = doc.tab(tab_n)
        end = content[-1]["endIndex"] - 1
        if end > 1:
            doc.delete_range(tab_id, 1, end)
            print("  cleared %d characters from %r" % (end - 1, a.tab))
        else:
            print("  %r is already empty" % a.tab)

    written = 0
    orientation = False  # the tab starts portrait
    for name, anchor, chunk, landscape in units:
        if anchor in tab_headings(doc, tab_n):
            print("  skip %-24s already present" % name)
            orientation = landscape
            continue
        if a.limit and written >= a.limit:
            print("  stopping at the --limit of %d units; run again to continue" % a.limit)
            break
        tab_id, _content = doc.tab(tab_n)
        flipped = landscape != orientation
        if flipped:
            doc.batch([gdoc_form.section_break(tab_id, end_of_tab(doc, tab_n), landscape)])
        start = end_of_tab(doc, tab_n)
        end = doc.insert_markdown(tab_n, start, chunk)
        if flipped:
            tab_id, _content = doc.tab(tab_n)
            doc.batch([gdoc_form.flip(tab_id, start, min(end, end_of_tab(doc, tab_n)), landscape)])
            orientation = landscape
        if name[:2] == "1." and not sheet_is_sound(doc, tab_n, anchor):
            print("  retry %-24s written table came back malformed" % name)
            drop_from_heading(doc, tab_n, anchor)
            time.sleep(2.0)
            doc.refresh()
            doc.insert_markdown(tab_n, end_of_tab(doc, tab_n), chunk)
            if not sheet_is_sound(doc, tab_n, anchor):
                raise SystemExit("%s still malformed after one retry; stopping before more damage"
                                 % name)
        apply_layout(doc, tab_n, name)
        written += 1
        print("  wrote %-24s %-9s (%d of %d, %d API calls)"
              % (name, "landscape" if landscape else "portrait", written, len(units), doc.calls))
        if a.sleep:
            time.sleep(a.sleep)
    print("done: %d units written, %d API calls" % (written, doc.calls))
    return 0


if __name__ == "__main__":
    sys.exit(main())
