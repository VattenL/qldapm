"""Build PDFs from the Markdown sources in docs/.

Pipeline: Markdown -> standalone HTML (CSS inlined) -> PDF via headless Chrome.
Markdown files are the source of truth and are never modified or removed.

Usage:
    python build.py            # build every docs/*.md
    python build.py en         # build only docs/charter-package.en.md
"""

import pathlib
import subprocess
import sys
import urllib.parse
import urllib.request

import markdown

ROOT = pathlib.Path(__file__).parent
DOCS = ROOT / "docs"
BUILD = ROOT / "build"
CSS = DOCS / "assets" / "style.css"

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def find_chrome():
    for path in CHROME_CANDIDATES:
        if pathlib.Path(path).exists():
            return path
    raise SystemExit("No Chrome/Edge binary found; cannot render PDF.")


def render(md_path: pathlib.Path) -> pathlib.Path:
    text = md_path.read_text(encoding="utf-8")
    body = markdown.markdown(
        text,
        extensions=["tables", "attr_list", "md_in_html", "sane_lists"],
    )
    lang = "vi" if md_path.name.endswith(".vi.md") else "en"
    title = md_path.stem
    html = HTML_TEMPLATE.format(
        lang=lang,
        title=title,
        css=CSS.read_text(encoding="utf-8"),
        body=body,
    )
    html_path = BUILD / (md_path.stem + ".html")
    html_path.write_text(html, encoding="utf-8")
    return html_path


def to_pdf(html_path: pathlib.Path, chrome: str) -> pathlib.Path:
    pdf_path = html_path.with_suffix(".pdf")
    url = urllib.parse.urljoin("file:", urllib.request.pathname2url(str(html_path)))
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=5000",
        f"--print-to-pdf={pdf_path}",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if not pdf_path.exists():
        sys.stderr.write(result.stdout + result.stderr)
        raise SystemExit(f"Chrome failed to produce {pdf_path}")
    return pdf_path


def main():
    BUILD.mkdir(exist_ok=True)
    chrome = find_chrome()
    wanted = sys.argv[1:]
    sources = sorted(DOCS.glob("*.md"))
    if wanted:
        sources = [p for p in sources if any(w in p.name for w in wanted)]
    if not sources:
        raise SystemExit("No matching Markdown files in docs/.")
    for md_path in sources:
        html_path = render(md_path)
        pdf_path = to_pdf(html_path, chrome)
        size_kb = pdf_path.stat().st_size / 1024
        print(f"{md_path.name} -> {pdf_path.name} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
