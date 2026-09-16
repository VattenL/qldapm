#!/usr/bin/env python3
"""Google Docs and Drive API helper for the charter package.

Run with:
    uv run --with google-api-python-client,google-auth-oauthlib,markdown tools/gdoc.py CMD ...

Subcommands:
    auth            OAuth consent in the browser; stores a refresh token outside the repo.
    comments        List the comment threads of a Doc with the text each one is anchored to.
    get             Save documents.get for all tabs as JSON; --marks lists yellow runs and cells.
    post            Post replies and new comments from a review JSON file. Idempotent.
    render          Render a review JSON file as Markdown.
    delete-comment  Delete one comment thread, for test comments.
    import-html     Convert a Markdown file to HTML and create a new Google Doc from it.

Nothing here names a document, a folder, or a repo path; every identifier is an
argument. The client JSON and the token default to ~/.config/qldapm/ and must
never be committed.

Review JSON format (a list):
    {"thread": COMMENT_ID, "location": ..., "reviewer": ..., "reply": TEXT}
    {"new": true, "location": ..., "quote": TEXT, "content": TEXT}
A reply is posted on its thread; a new item becomes an unanchored comment whose
text starts with "[location]" and quotes the passage it refers to.
"""

from __future__ import annotations

import argparse
import http.server
import io
import json
import os
import pathlib
import re
import sys
import urllib.parse
import webbrowser

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]
REDIRECT = "http://localhost:8765/callback"
COMMENT_FIELDS = (
    "comments(id,author(displayName),createdTime,resolved,content,"
    "quotedFileContent(value),anchor,replies(id,author(displayName),content,createdTime)),"
    "nextPageToken"
)
DEFAULT_DIR = os.path.expanduser("~/.config/qldapm")


# ---------------------------------------------------------------- auth

def load_creds(token_path: pathlib.Path):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    if not token_path.exists():
        sys.exit(f"no token at {token_path}; run 'auth' first")
    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path.write_text(creds.to_json())
    return creds


def cmd_auth(a):
    from google_auth_oauthlib.flow import Flow

    client_path, token_path = pathlib.Path(a.client), pathlib.Path(a.token)
    if not client_path.exists():
        sys.exit(f"client JSON not found at {client_path}")
    flow = Flow.from_client_secrets_file(str(client_path), scopes=SCOPES, redirect_uri=REDIRECT)
    url, _state = flow.authorization_url(access_type="offline", prompt="consent")
    result = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            if parsed.path != "/callback" or "code" not in params:
                self.send_response(404)
                self.end_headers()
                return
            result["code"] = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Authorised. You can close this tab.")

        def log_message(self, *_args):
            pass

    server = http.server.HTTPServer(("localhost", 8765), Handler)
    print("Opening the browser for consent:", url, flush=True)
    webbrowser.open(url)
    while "code" not in result:
        server.handle_request()
    server.server_close()
    flow.fetch_token(code=result["code"])
    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(flow.credentials.to_json())
    os.chmod(token_path, 0o600)
    print("Token saved to", token_path)


def drive(creds):
    from googleapiclient.discovery import build

    return build("drive", "v3", credentials=creds, cache_discovery=False)


def docs(creds):
    from googleapiclient.discovery import build

    return build("docs", "v1", credentials=creds, cache_discovery=False)


# ---------------------------------------------------------------- comments

def list_comments(creds, doc_id):
    svc = drive(creds)
    out, token = [], None
    while True:
        resp = svc.comments().list(
            fileId=doc_id, fields=COMMENT_FIELDS, pageSize=100,
            includeDeleted=False, pageToken=token,
        ).execute()
        out.extend(resp.get("comments", []))
        token = resp.get("nextPageToken")
        if not token:
            break
    return out


def cmd_comments(a, creds):
    comments = list_comments(creds, a.doc)
    if a.json:
        print(json.dumps(comments, ensure_ascii=False, indent=1))
        return
    print(f"{len(comments)} comment thread(s)")
    for c in comments:
        quote = (c.get("quotedFileContent") or {}).get("value", "").replace("\n", " ")
        print(
            f"- {c['id']} | {c['author']['displayName']} | resolved={c.get('resolved')} | "
            f"quote={quote[:70]!r} | {c['content'][:60]!r} | replies={len(c.get('replies', []))}"
        )


def first_line(text: str) -> str:
    text = (text or "").strip()
    return text.splitlines()[0].strip() if text else ""


def validate_review(review) -> None:
    if not isinstance(review, list) or not review:
        raise ValueError("review must be a non-empty list")
    for i, item in enumerate(review):
        if "thread" in item:
            missing = [k for k in ("thread", "location", "reviewer", "reply") if not item.get(k)]
        elif item.get("new"):
            missing = [k for k in ("location", "quote", "content") if not item.get(k)]
        else:
            raise ValueError(f"item {i}: neither a thread reply nor a new comment")
        if missing:
            raise ValueError(f"item {i}: missing {missing}")


def new_comment_text(item) -> str:
    return f"[{item['location']}] {item['content']}"


def plan_posts(review, threads):
    """Decide what to post. threads: {id: comment}. Returns (actions, skipped)."""
    actions, skipped = [], []
    existing_first_lines = {first_line(c.get("content", "")) for c in threads.values()}
    for item in review:
        if "thread" in item:
            t = threads.get(item["thread"])
            if t is None:
                raise KeyError(f"thread {item['thread']} not found on the document")
            fl = first_line(item["reply"])
            if any(first_line(r.get("content", "")) == fl for r in t.get("replies", [])):
                skipped.append(("reply", item["thread"], fl))
            else:
                actions.append(("reply", item["thread"], item["reply"], None))
        else:
            content = new_comment_text(item)
            fl = first_line(content)
            if fl in existing_first_lines:
                skipped.append(("comment", "", fl))
            else:
                actions.append(("comment", "", content, item.get("quote")))
    return actions, skipped


def cmd_post(a, creds):
    review = json.load(open(a.review, encoding="utf-8"))
    validate_review(review)
    threads = {c["id"]: c for c in list_comments(creds, a.doc)}
    actions, skipped = plan_posts(review, threads)
    for kind, thread, text in skipped:
        print(f"skip {kind:8} {thread} {text[:60]!r}")
    svc = drive(creds)
    for kind, thread, text, quote in actions:
        print(f"{kind:13} {thread} {first_line(text)[:60]!r}")
        if a.dry_run:
            continue
        if kind == "reply":
            svc.replies().create(fileId=a.doc, commentId=thread, body={"content": text}, fields="id").execute()
        else:
            body = {"content": text}
            if quote:
                body["quotedFileContent"] = {"value": quote, "mimeType": "text/plain"}
            svc.comments().create(fileId=a.doc, body=body, fields="id").execute()
    verb = "would post" if a.dry_run else "posted"
    print(f"{verb} {len(actions)}, skipped {len(skipped)}")


def render_review(review, title: str) -> str:
    validate_review(review)
    out = [f"# {title}", ""]
    out.append("Replies are posted on the reviewer's thread; new findings are separate comments prefixed with their location.")
    out.append("")
    n = 0
    for item in review:
        if "thread" in item:
            n += 1
            out += [f"## {n}. {item['location']}", "", f"Thread `{item['thread']}`. Reviewer: {item['reviewer']}", "", item["reply"], ""]
    m = 0
    for item in review:
        if item.get("new"):
            m += 1
            out += [f"## New {m}. {item['location']}", "", f"Quoted: {item['quote']}", "", item["content"], ""]
    return "\n".join(out)


def cmd_render(a):
    review = json.load(open(a.review, encoding="utf-8"))
    pathlib.Path(a.out).write_text(render_review(review, a.title), encoding="utf-8")
    print("wrote", a.out)


def cmd_delete_comment(a, creds):
    drive(creds).comments().delete(fileId=a.doc, commentId=a.comment).execute()
    print("deleted", a.comment)


# ---------------------------------------------------------------- document structure

def iter_marks(elements):
    """Yield ('run', text) for shaded text runs and ('cell', text) for shaded table cells."""
    for el in elements or []:
        if "paragraph" in el:
            for pe in el["paragraph"].get("elements", []):
                run = pe.get("textRun")
                if run and run.get("textStyle", {}).get("backgroundColor"):
                    yield ("run", run.get("content", "").strip())
        elif "table" in el:
            for row in el["table"].get("tableRows", []):
                for cell in row.get("tableCells", []):
                    if cell.get("tableCellStyle", {}).get("backgroundColor", {}).get("color"):
                        text = "".join(
                            pe.get("textRun", {}).get("content", "")
                            for e2 in cell.get("content", []) if "paragraph" in e2
                            for pe in e2["paragraph"].get("elements", [])
                        )
                        yield ("cell", text.strip())
                    yield from iter_marks(cell.get("content", []))
        elif "tableOfContents" in el:
            yield from iter_marks(el["tableOfContents"].get("content", []))


def iter_tabs(doc):
    tabs = doc.get("tabs")
    if not tabs:
        yield doc.get("title", ""), doc.get("body", {}).get("content", [])
        return
    stack = list(tabs)
    while stack:
        tab = stack.pop(0)
        title = tab.get("tabProperties", {}).get("title", "")
        yield title, tab.get("documentTab", {}).get("body", {}).get("content", [])
        stack = list(tab.get("childTabs", [])) + stack


def cmd_get(a, creds):
    doc = docs(creds).documents().get(documentId=a.doc, includeTabsContent=True).execute()
    pathlib.Path(a.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", a.out, "revision", doc.get("revisionId"))
    if a.marks:
        for title, content in iter_tabs(doc):
            marks = list(iter_marks(content))
            print(f"tab {title!r}: {sum(1 for k, _ in marks if k == 'run')} shaded runs, {sum(1 for k, _ in marks if k == 'cell')} shaded cells")
            for kind, text in marks:
                print(f"  {kind}: {text[:80]!r}")


# ---------------------------------------------------------------- import

PAGE_HEADING = re.compile(r"<h4>(PROJECT CHARTER, page \d of 4)</h4>")


def md_to_html(md_text: str, title: str) -> str:
    import markdown

    body = markdown.markdown(md_text, extensions=["tables", "sane_lists"])
    body = body.replace("<mark>", '<span style="background-color:#ffff00">').replace("</mark>", "</span>")
    body = PAGE_HEADING.sub(r'<div style="page-break-before:always"></div><h4>\1</h4>', body)
    return (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        f"<title>{title}</title></head><body>{body}</body></html>"
    )


def cmd_import_html(a, creds):
    from googleapiclient.http import MediaIoBaseUpload

    parts = []
    if a.cover:
        parts.append(pathlib.Path(a.cover).read_text(encoding="utf-8"))
        parts.append('<div style="page-break-before:always"></div>')
    parts.append(pathlib.Path(a.md).read_text(encoding="utf-8"))
    html = md_to_html("\n\n".join(parts), a.title)
    if a.html_out:
        pathlib.Path(a.html_out).write_text(html, encoding="utf-8")
    media = MediaIoBaseUpload(io.BytesIO(html.encode("utf-8")), mimetype="text/html", resumable=False)
    body = {"name": a.title, "mimeType": "application/vnd.google-apps.document"}
    if a.parent:
        body["parents"] = [a.parent]
    created = drive(creds).files().create(body=body, media_body=media, fields="id,webViewLink").execute()
    print(created["webViewLink"])


# ---------------------------------------------------------------- cli

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--client", default=os.path.join(DEFAULT_DIR, "client_secret.json"))
    p.add_argument("--token", default=os.path.join(DEFAULT_DIR, "token.json"))
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("auth")
    s = sub.add_parser("comments"); s.add_argument("--doc", required=True); s.add_argument("--json", action="store_true")
    s = sub.add_parser("get"); s.add_argument("--doc", required=True); s.add_argument("--out", required=True); s.add_argument("--marks", action="store_true")
    s = sub.add_parser("post"); s.add_argument("--doc", required=True); s.add_argument("--review", required=True); s.add_argument("--dry-run", action="store_true")
    s = sub.add_parser("render"); s.add_argument("--review", required=True); s.add_argument("--out", required=True); s.add_argument("--title", required=True)
    s = sub.add_parser("delete-comment"); s.add_argument("--doc", required=True); s.add_argument("--comment", required=True)
    s = sub.add_parser("import-html"); s.add_argument("--doc", required=False, help="unused; kept for symmetry")
    s.add_argument("--md", required=True); s.add_argument("--cover"); s.add_argument("--title", required=True)
    s.add_argument("--parent", help="Drive folder id"); s.add_argument("--html-out", help="also write the HTML here")

    a = p.parse_args(argv)
    if a.cmd == "auth":
        return cmd_auth(a)
    if a.cmd == "render":
        return cmd_render(a)
    creds = load_creds(pathlib.Path(a.token))
    return {
        "comments": cmd_comments, "get": cmd_get, "post": cmd_post,
        "delete-comment": cmd_delete_comment, "import-html": cmd_import_html,
    }[a.cmd](a, creds)


if __name__ == "__main__":
    main()
