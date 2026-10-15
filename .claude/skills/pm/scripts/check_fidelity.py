"""Check a Markdown form against the labels its printed form carries.

The expected labels come from references/fields/<form>.json, built into the
shapes references/rendering.md prescribes: title-block lines, table header
cells (a grouped column as `Group: Label`, a caption group as a bold line above
the table), bold field and row labels, checkbox labels and their task-list
options, signature columns and rows. Only those positions are read in the
Markdown: table header cells, a bold label that opens a line or a table row,
the first cell of every row of a `Field | Content` table (bold or not), a
heading whose text, less a leading section number, is a printed label (the
charter writes form 2.8 as `### 1.1 Project Scope Description`), and task-list
items. Body prose is never matched, so a field called Cost is not found in a
sentence about cost.

Three findings are reported separately: printed labels that are missing,
printed labels present but out of printed order, and unprinted labels (a header
cell or bold label that the form does not print; the columns rendering.md
gives the table behind a picture are not reported). The check exits 1 on a
missing or out-of-order label; unprinted labels are reported only.

    check_fidelity.py docs/forms/2-32-risk-register.en.md 2.32
    check_fidelity.py docs/scope-package.en.md 2.9 --section "Part 2:" --end "Roll-up"
    check_fidelity.py docs/scope-package.en.md 2.7 --section "Part 1B" --page 2 --flattened
    check_fidelity.py --list 2.32

--flattened accepts a grouped header written without its colon: the child label alone
("Category" for "Requirement Information: Category", only when no other group has that
child) or the group and child joined by a space ("Labor Rate" for "Labor: Rate", as the
2.10 sheets write it). The accepted labels are listed and are not reported as unprinted.
--ignore-tables skips the headers of a table none of whose labels the form prints, the document's own
table inside a free-text box (a roles table in 2.8); it counts the tables skipped, and a table that
carries any printed label is still the form's and still reported.
--page N checks only the labels of printed page N of a form with several pages, for a
document that writes one page apart (the 2.7 second page in Part 1B); a later page's
repeated title block is not required, since the project writes it once.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from new_form import underlying_header

SKILL_DIR = Path(__file__).resolve().parent.parent
FIELDS = SKILL_DIR / "references" / "fields"

SEPARATOR = re.compile(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
TASK = re.compile(r"^[-*+]\s+\[[ xX]\]\s+(.*)$")
BOLD_START = re.compile(r"^\*\*(.+?)\*\*")
BOLD_CELL = re.compile(r"^\*\*(.+?)\*\*\s*:?$")
PLACEHOLDER = re.compile(r"^(Etc\.|.*[A-Za-z] \d+(\s.*)?)$")
# A section number before a heading's text: "1.1 ", "1.1.", "2B. ", "Part 1: ".
HEADING_NUMBER = re.compile(r"^(?:Part\s+)?\d+(?:\.\d+)*[A-Z]?[.:]?\s+")
STRUCTURAL = {("Field", "Content")}


@dataclass
class Slot:
    """One label the printed form carries, and the shape the Markdown gives it."""
    text: str
    shape: str  # a key of SHAPES
    where: str
    checked: bool = True
    in_first_column: bool = False  # a row label printed inside the first headed column

    @property
    def cls(self):
        return "option" if self.shape == "option" else "label"


SHAPES = {
    "title": "**{}:** value",
    "field": "| **{}** | value |",
    "bold": "**{}**",
    "checklabel": "**{}:** (bold line above its boxes)",
    "caption": "**{}** (bold line directly above the table)",
    "row": "| **{}** | ... | (row label)",
    "option": "- [ ] {}",
    "skip": "{}",
}


@dataclass
class Cand:
    """One label position found in the Markdown; table is the header line of the table it sits in."""
    text: str
    cls: str
    line: int
    structural: bool = False
    table: int = 0


def fail(message):
    print(message, file=sys.stderr)
    raise SystemExit(2)


def load_spec(form, fields_dir=FIELDS):
    form = form.strip().replace("-", ".")
    path = Path(fields_dir) / f"{form}.json"
    if not path.exists():
        fail(f"no field spec for form {form!r} at {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def heading_text(text):
    """A printed text block is a heading label unless it is a sentence or an outline."""
    text = text.strip()
    return bool(text) and "\n" not in text and "____" not in text and text[-1] not in ".:"


def label_slots(labels, where, shape):
    return [Slot(label, shape, where, checked=not PLACEHOLDER.match(label))
            for label in labels if label]


def table_slots(block, where):
    columns = block["columns"]
    out = []
    if len(columns) == 1 and isinstance(columns[0], dict):
        out.append(Slot(columns[0]["group"], "caption", where))
        columns = columns[0]["columns"]
    header = []
    for col in columns:
        if isinstance(col, dict):
            header += ["%s: %s" % (col["group"], child) for child in col["columns"]]
        else:
            header.append(col)
    rows = label_slots(block.get("row_labels", []), where, "row")
    for slot in rows:
        slot.in_first_column = bool(block.get("row_label_column"))
    return out + label_slots(header, where, "header") + rows


def blocks(spec, only_page=None):
    """The expected labels as (where, slots) pairs in printed order; only_page keeps one printed page."""
    out = []
    if spec["title_block"] and only_page in (None, 1):
        out.append(("title block", label_slots(spec["title_block"], "title block", "title")))
    for page in spec["pages"]:
        n = page["page"]
        if only_page is not None and n != only_page:
            continue
        if n > 1 and page.get("title_block") and spec["title_block"] and only_page is None:
            where = "page %d, title block" % n
            out.append((where, label_slots(spec["title_block"], where, "title")))
        for block in page["blocks"]:
            kind = block["type"]
            where = "page %d, %s" % (n, kind)
            if kind == "table":
                where = "page %d, table, bank %d" % (n, block["bank"])
                slots = table_slots(block, where)
            elif kind == "fields":
                slots = label_slots(block["labels"], where, "field")
            elif kind == "text" and heading_text(block["text"]):
                slots = [Slot(block["text"].strip(), "bold", where)]
            elif kind == "text":
                first = block["text"].strip().splitlines()[0]
                slots = [Slot("printed text, not checked: " + first, "skip", where, checked=False)]
            elif kind == "checkboxes":
                slots = [Slot(block["label"], "checklabel", where)]
                slots += label_slots(block["options"], where, "option")
            elif kind == "signatures":
                slots = label_slots(block["columns"], where, "header")
                slots += label_slots(block["rows"], where, "row")
            else:
                slots = [Slot(kind + ", not checked", "skip", where, checked=False)]
            out.append((where, slots))
    return out


def expected(spec, only_page=None):
    return [s for _, slots in blocks(spec, only_page) for s in slots if s.checked]


def all_labels(spec):
    """Labels not to report as unprinted: every label the form prints, groups
    included, and the columns rendering.md gives the table behind a picture."""
    return {s.text for _, slots in blocks(spec) for s in slots if s.shape != "skip"} | {
        g["group"] for p in spec["pages"] for b in p["blocks"] if b["type"] == "table"
        for g in b["columns"] if isinstance(g, dict)} | set(underlying_header(spec))


def norm(text):
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.I)
    text = re.sub(r"</?mark>", "", text)
    text = re.sub(r"\\(.)", r"\1", text)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text.rstrip(":").strip()


def loose(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def cells(row):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|") and not row.endswith("\\|"):
        row = row[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", row)]


def region(lines, spec, section=None, until=None):
    """The lines that hold the form: [start, end).

    With --section, the part under the first heading containing that text, to
    the next heading of the same or a higher level; with --end as well, it stops
    sooner, at the first later heading containing the --end text (the Roll-up
    and Coverage check under the scope package's Part 2 are not form 2.9). A
    file whose H1 names the form is checked from the top, so unprinted lines
    above the first page heading are seen. Otherwise the form starts at its
    `page 1 of N` heading. It ends at the first heading shallower than the page
    headings after the last page, or at the end of the file.
    """
    if section:
        for i, line in enumerate(lines):
            m = HEADING.match(line)
            if m and section.lower() in m.group(2).lower():
                level = len(m.group(1))
                for j in range(i + 1, len(lines)):
                    n = HEADING.match(lines[j])
                    if n and (len(n.group(1)) <= level or (until and until.lower() in n.group(2).lower())):
                        return i, j
                return i, len(lines)
        fail(f"no heading contains {section!r}")
    titles = {spec["printed_title"]} | {p["printed_title"] for p in spec["pages"] if "printed_title" in p}
    names = "|".join(re.escape(t) for t in sorted(titles, key=len, reverse=True))
    page = re.compile(r"^(#{1,6})\s+(?:%s),\s*page\s+\d+\s+of\s+\d+\s*$" % names, re.I)
    pages = [i for i, line in enumerate(lines) if page.match(line)]
    h1 = next((line for line in lines if line.startswith("# ")), "")
    names_form = re.match(r"^#\s+%s(?!\.?\d)" % re.escape(spec["form"]), h1)
    start = 0 if names_form or not pages else pages[0]
    end = len(lines)
    if pages:
        level = len(page.match(lines[pages[-1]]).group(1))
        for j in range(pages[-1] + 1, len(lines)):
            m = HEADING.match(lines[j])
            if m and len(m.group(1)) < level:
                end = j
                break
    return start, end


def scan(lines, start, end, printed=frozenset()):
    """Label positions in [start, end), plus every plain line for hints.

    printed is the set of labels the form prints; a heading counts as a label
    position only when its text, less a section number, is one of them, so the
    document's own headings are never reported as unprinted labels.
    """
    found, plain = [], []
    fence = italic = False
    i = start
    while i < end:
        s = lines[i].strip()
        if s.startswith("```") or s.startswith("~~~"):
            fence = not fence
            i += 1
            continue
        if fence:
            i += 1
            continue
        if not s:
            italic = False
            i += 1
            continue
        if s.startswith("*") and not s.startswith("**") and not s.startswith("* "):
            italic = True
        if italic:
            i += 1
            continue
        if s.startswith("|") and i + 1 < end and SEPARATOR.match(lines[i + 1].strip()):
            header = [norm(c) for c in cells(s)]
            structural = tuple(header) in STRUCTURAL
            found += [Cand(c, "label", i + 1, structural, i + 1) for c in header if c]
            top = i + 1
            i += 2
            while i < end and lines[i].strip().startswith("|"):
                first = cells(lines[i])[0]
                m = BOLD_CELL.match(re.sub(r"</?mark>", "", first).strip())
                if m and norm(m.group(1)):
                    found.append(Cand(norm(m.group(1)), "label", i + 1, table=top))
                elif structural and norm(first):
                    # A Field | Content table holds a label in every first cell, bold or not.
                    found.append(Cand(norm(first), "label", i + 1, table=top))
                i += 1
            continue
        h = HEADING.match(s)
        if h:
            text = norm(HEADING_NUMBER.sub("", norm(h.group(2))))
            if text in printed:
                found.append(Cand(text, "label", i + 1))
            i += 1
            continue
        m = TASK.match(s)
        if m:
            found.append(Cand(norm(m.group(1)), "option", i + 1))
        else:
            m = BOLD_START.match(s)
            if m and norm(m.group(1)):
                found.append(Cand(norm(m.group(1)), "label", i + 1))
            elif not HEADING.match(s) and not s.startswith("|"):
                plain.append(Cand(norm(s), "plain", i + 1))
        i += 1
    return found, plain


def align(exp, cand):
    """Longest common subsequence, each label matched to its earliest place."""
    n, m = len(exp), len(cand)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        row, below = dp[i], dp[i + 1]
        e = exp[i]
        for j in range(m - 1, -1, -1):
            c = cand[j]
            if e.text == c.text and e.cls == c.cls:
                row[j] = below[j + 1] + 1
            else:
                row[j] = max(below[j], row[j + 1])
    pairs, i, j = {}, 0, 0
    while i < n and j < m:
        e, c = exp[i], cand[j]
        if e.text == c.text and e.cls == c.cls and dp[i][j] == dp[i + 1][j + 1] + 1:
            pairs[i] = j
            i, j = i + 1, j + 1
        elif dp[i][j + 1] == dp[i][j]:
            j += 1
        else:
            i += 1
    return pairs


@dataclass
class Result:
    total: int
    missing: list
    disorder: list
    extra: list
    start: int
    end: int
    flattened: list = field(default_factory=list)
    ignored: int = 0  # tables inside boxes skipped by --ignore-tables

    @property
    def failed(self):
        return bool(self.missing or self.disorder)


def flat_spellings(spec):
    """{group: {child: [spellings]}} of the printed grouped headers, preferred first: the group and child joined
    by a space, then the child alone when no other group has it."""
    groups = {}
    for p in spec["pages"]:
        for b in p["blocks"]:
            if b["type"] == "table":
                for col in b["columns"]:
                    if isinstance(col, dict):
                        groups.setdefault(col["group"], []).extend(col["columns"])
    count = {}
    for children in groups.values():
        for child in set(children):
            count[child] = count.get(child, 0) + 1
    return {group: {child: ["%s %s" % (group, child)] + ([child] if count[child] == 1 else [])
                    for child in children} for group, children in groups.items()}


def check(markdown, spec, section=None, until=None, flat_groups=False, only_page=None, ignore_tables=False):
    lines = markdown.splitlines()
    start, end = region(lines, spec, section, until)
    printed = all_labels(spec)
    found, plain = scan(lines, start, end, printed)
    exp = expected(spec, only_page)
    pairs = align(exp, found)
    used = set(pairs.values())

    disorder, unplaced = [], []
    for i, slot in enumerate(exp):
        if i in pairs:
            continue
        j = next((k for k, c in enumerate(found) if k not in used
                  and c.text == slot.text and c.cls == slot.cls), None)
        if j is None:
            unplaced.append(slot)
        else:
            used.add(j)
            disorder.append((slot, found[j].line))

    missing, cited = [], set()
    for slot in unplaced:
        pool = [c for k, c in enumerate(found) if k not in used] + plain
        near = next((c for c in pool if id(c) not in cited and loose(c.text) == loose(slot.text)), None)
        note = ""
        if near is not None:
            cited.add(id(near))
            shape = "as a plain line" if near.cls == "plain" else "as %r" % near.text
            note = "written %s on line %d" % (shape, near.line)
        missing.append((slot, note))

    flattened, accepted = [], set()
    if flat_groups:
        # A grouped header written without its colon, as its child label alone ("Category" for
        # "Requirement Information: Category") or as group and child joined ("Labor Rate"): reported
        # on its own line, and not a failure.
        spellings = flat_spellings(spec)
        labels = {c.text for c in found if c.cls == "label"}
        kept = []
        for slot, note in missing:
            group, _, child = slot.text.partition(": ") if slot.shape == "header" else ("", "", "")
            hit = next((x for x in spellings.get(group, {}).get(child, []) if x in labels), None)
            if hit:
                flattened.append((slot, note))
                accepted.add(hit)
            else:
                kept.append((slot, note))
        missing = kept

    placeholders = any(not s.checked and s.shape != "skip" for _, b in blocks(spec) for s in b)
    by_loose = {loose(t): t for t in printed}
    # A table none of whose labels the form prints is the document's own table inside a free-text box
    # (a roles table in 2.8, say); its headers are content, not labels the form lacks.
    own = {c.table for c in found if c.table and (c.text in printed or c.text in accepted)}
    boxed = {c.table for c in found if c.table and c.table not in own and not c.structural}
    extra = []
    for k, c in enumerate(found):
        if k in used or c.structural or c.text in printed or c.text in accepted:
            continue
        if ignore_tables and c.table in boxed:
            continue
        if placeholders and c.cls == "label" and lines[c.line - 1].lstrip().startswith("|"):
            continue
        note = by_loose.get(loose(c.text))
        extra.append((c, "printed as %r" % note if note else ""))
    return Result(len(exp), missing, disorder, extra, start, end, [slot for slot, _ in flattened],
                  len(boxed & {c.table for c in found if c.table}) if ignore_tables else 0)


def report(result, spec, name):
    ok = result.total - len(result.missing) - len(result.disorder)
    print("%s %s, %s lines %d to %d" % (spec["form"], spec["name"], name, result.start + 1, result.end))
    print("%d/%d printed labels present in printed order" % (ok, result.total))
    if result.flattened:
        print("grouped headers written without the colon (%d), accepted by --flattened:" % len(result.flattened))
        for slot in result.flattened:
            print("  %s: %s" % (slot.where, slot.text))
    if result.missing:
        print("missing (%d):" % len(result.missing))
        for slot, note in result.missing:
            print("  %s: %s%s" % (slot.where, slot.text, " (%s)" % note if note else ""))
    if result.disorder:
        print("out of printed order (%d):" % len(result.disorder))
        for slot, line in result.disorder:
            print("  %s: %s (line %d)" % (slot.where, slot.text, line))
    if result.ignored:
        print("%d table(s) inside boxes ignored by --ignore-tables: none of their labels is printed, so their "
              "headers are content (name them in the reading paragraph)" % result.ignored)
    if result.extra:
        # One line per distinct label, so 78 dictionary sheets do not print one label 78 times.
        groups = {}
        for cand, note in result.extra:
            groups.setdefault((cand.text, note), []).append(cand.line)
        print("unprinted labels (%d, %d distinct), reported only:" % (len(result.extra), len(groups)))
        for (text, note), at in groups.items():
            more = ", and %d more" % (len(at) - 1) if len(at) > 1 else ""
            print("  line %d%s: %s%s" % (at[0], more, text, " (%s)" % note if note else ""))


def list_labels(spec):
    """Print the expected labels in the Markdown shapes rendering.md gives them."""
    pages = spec["page_count"]
    print("%s %s (%s, %d page%s)" % (spec["form"], spec["name"], spec["kind"], pages, "" if pages == 1 else "s"))
    for where, slots in blocks(spec):
        print(where)
        header = [s for s in slots if s.shape == "header"]
        corner = "| " if any(s.shape == "row" and not s.in_first_column for s in slots) else ""
        for slot in slots:
            if slot.shape != "header":
                note = "" if slot.checked or slot.shape == "skip" else " (placeholder, not checked)"
                print("  " + SHAPES[slot.shape].format(slot.text) + note)
            elif slot is header[0]:
                print("  %s| %s |" % (corner, " | ".join(h.text for h in header)))
                loose_ones = [h.text for h in header if not h.checked]
                if loose_ones:
                    print("  (placeholders, not checked: %s)" % ", ".join(loose_ones))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markdown", nargs="?", type=Path)
    ap.add_argument("form", help="form number, for example 2.32")
    ap.add_argument("--list", action="store_true", help="print the expected labels and exit")
    ap.add_argument("--section", help="check only the part under the first heading containing this text")
    ap.add_argument("--end", metavar="TEXT",
                    help="with --section, stop at the first later heading containing this text")
    ap.add_argument("--flattened", action="store_true",
                    help="accept a grouped header written as its child label alone and list those labels; for "
                         "the project's RTM in the scope package, which flattens the printed group header")
    ap.add_argument("--ignore-tables", action="store_true",
                    help="do not report the headers of a table none of whose labels the form prints: the "
                         "document's own table inside a free-text box (a roles table in 2.8)")
    ap.add_argument("--page", type=int, metavar="N",
                    help="check only the labels of printed page N of the form (a later page's repeated title "
                         "block is not required)")
    ap.add_argument("--fields", type=Path, default=FIELDS, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    spec = load_spec(args.form, args.fields)
    if args.list:
        list_labels(spec)
        return 0
    if args.markdown is None:
        ap.error("a Markdown file is required unless --list is given")
    if args.end and not args.section:
        ap.error("--end needs --section")
    if args.page is not None and not 1 <= args.page <= spec["page_count"]:
        ap.error("%s has %d printed page%s" % (spec["form"], spec["page_count"], "" if spec["page_count"] == 1 else "s"))
    result = check(args.markdown.read_text(encoding="utf-8"), spec, args.section, args.end, args.flattened,
                   args.page, args.ignore_tables)
    report(result, spec, args.markdown.name)
    return 1 if result.failed else 0


if __name__ == "__main__":
    sys.exit(main())
