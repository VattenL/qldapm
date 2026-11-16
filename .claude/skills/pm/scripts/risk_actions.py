"""The Actions text of form 2.32 for each risk, from the scope package's coverage check.

The scope package says which work packages carry out each risk response in its Coverage check
table (a row such as "R1 to R12 responses | Owned by 1.1.1.4. R1 1.6.2.1 and 1.8.3.2; R2 ..."). Form 2.32
Actions takes only what a document states as actions for that risk, and a work package is written with its
title as the dictionary spells it, never as a bare code (references/rendering.md). This reads the row and the
sheet headings and prints the cell for each risk in the shape the reviewers asked for:

    Work package <code> <title>: <what is done>; Work package <code> <title>: <what is done>

a colon between the package and its action, a semicolon between packages. The action is the text the coverage
row writes after the code ("R1 1.6.2.1 (write test cases) and 1.8.3.1: run UAT"); where the row gives only
the code, nothing follows the colon and the writer fills it from a document that states the action, or
highlights it as the preparer's reading. Each such risk is listed on standard error.

    risk_actions.py docs/scope-package.en.md
    risk_actions.py docs/scope-package.en.md --risk R5

Output: one line per risk, the risk ID, a tab, the Actions text. The line of the coverage row is printed last
so the cell can be cited as such. Exit code 1 when a package code has no sheet or no coverage row exists,
2 for a usage error.
"""

import argparse
import re
import sys
from pathlib import Path

ROW = re.compile(r"^\|\s*R\d+ to R\d+ responses\s*\|(.*)\|\s*$")
HEADING = re.compile(r"^#### (\d+(?:\.\d+)+) (.+?)\s*$")
CODE = re.compile(r"\d+(?:\.\d+){2,}")


def sheet_titles(text):
    return {m.group(1): m.group(2) for m in (HEADING.match(line) for line in text.splitlines()) if m}


def coverage_row(text):
    """(line number, cell text) of the responses row of the coverage check, or None."""
    for n, line in enumerate(text.splitlines(), 1):
        m = ROW.match(line)
        if m:
            return n, m.group(1).strip()
    return None


def action_text(text):
    """The action written between one code and the next: '(write test cases) and ' or ': run UAT'."""
    text = re.sub(r"^[\s:(]+", "", text)
    text = re.sub(r"(?:\s*(?:,|\band\b))+\s*$", "", text)
    return text.strip().rstrip(")").strip()


def actions(cell, titles):
    """({risk: [(code, action text or '')]}, [codes with no sheet]) read from the cell text."""
    found, missing = {}, []
    for part in re.split(r";\s*", cell):
        m = re.match(r"^(?:Owned by [\d.]+\.\s*)?(R\d+)\s+(.*)$", part.strip().rstrip("."))
        if not m:
            continue
        body = m.group(2)
        hits = list(CODE.finditer(body))
        ends = [h.start() for h in hits[1:]] + [len(body)]
        found[m.group(1)] = [(h.group(0), action_text(body[h.end():end])) for h, end in zip(hits, ends)]
        missing += [h.group(0) for h in hits if h.group(0) not in titles]
    return found, missing


def render(packages, titles):
    return "; ".join("Work package %s %s: %s" % (c, titles[c], action) for c, action in packages if c in titles)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scope", help="the scope package Markdown")
    ap.add_argument("--risk", action="append", default=[], metavar="ID", help="only this risk (repeatable)")
    args = ap.parse_args(argv)
    try:
        text = Path(args.scope).read_text(encoding="utf-8")
    except OSError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    row = coverage_row(text)
    if row is None:
        print("no coverage row 'R1 to R12 responses' in %s: Actions stays empty" % args.scope, file=sys.stderr)
        return 1
    titles = sheet_titles(text)
    found, missing = actions(row[1], titles)
    for risk, packages in found.items():
        if not args.risk or risk in args.risk:
            print("%s\t%s" % (risk, render(packages, titles)))
            empty = [c for c, action in packages if c in titles and not action]
            if empty:
                print("%s: no action text for %s in the coverage row; write what each package does after its "
                      "colon from a document that states it, or highlight it as the preparer's reading"
                      % (risk, ", ".join(empty)), file=sys.stderr)
    print("source: %s:%d" % (args.scope, row[0]))
    for code in dict.fromkeys(missing):
        print("no sheet for %s" % code, file=sys.stderr)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
