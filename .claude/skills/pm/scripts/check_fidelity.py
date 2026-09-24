"""Check a generated form against the printed form it claims to reproduce.

Reports printed field labels that are missing from the Markdown, and labels that
appear out of printed order. Order matters because the book's forms are read
top to bottom by people who know them.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
EXTRACT = SKILL_DIR / "scripts" / "extract_form.py"

NOISE = re.compile(
    r"^(page \d+ of \d+|project title:?|date prepared:?|project title|date prepared)$", re.I)


def printed_labels(form, pdf=None):
    cmd = [sys.executable, str(EXTRACT), form, "--blank"]
    if pdf:
        cmd += ["--pdf", pdf]
    text = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    labels, seen = [], set()
    for line in text.splitlines():
        if line.startswith("#"):
            continue
        for part in re.split(r"\s{3,}|(?<=:)\s+", line):
            s = part.strip().strip(":").strip()
            if len(s) < 3 or NOISE.match(s):
                continue
            if not re.match(r"^[A-Za-z][A-Za-z0-9 /&,'()%.-]*$", s):
                continue
            if s.lower() in seen:
                continue
            seen.add(s.lower())
            labels.append(s)
    return labels


def locate(body, label):
    """Where the label sits in the document, -1 if absent.

    A bold cell label is the strong signal, so look for that first. Plain text
    is matched on word boundaries, otherwise short labels such as Date and Cost
    match inside ordinary prose and every later field looks out of order.
    """
    low = label.lower()
    for pattern in (r"\*\*" + re.escape(low) + r":?\*\*", r"\b" + re.escape(low) + r"\b"):
        m = re.search(pattern, body)
        if m:
            return m.start()
    return -1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("markdown", type=Path)
    ap.add_argument("form", help="form number, for example 2.32")
    ap.add_argument("--pdf")
    args = ap.parse_args()

    body = args.markdown.read_text(encoding="utf-8").lower()
    labels = printed_labels(args.form, args.pdf)

    missing, positions = [], []
    for label in labels:
        at = locate(body, label)
        if at < 0:
            missing.append(label)
        else:
            positions.append((label, at))

    out_of_order = [
        b for (a, pa), (b, pb) in zip(positions, positions[1:]) if pb < pa
    ]

    print(f"{len(labels) - len(missing)}/{len(labels)} printed labels present")
    for label in missing:
        print(f"  missing: {label}")
    for label in out_of_order:
        print(f"  out of printed order: {label}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
