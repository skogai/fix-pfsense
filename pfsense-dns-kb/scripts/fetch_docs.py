#!/usr/bin/env python3
"""Fetch and clean pfSense DNS documentation into local Markdown.

Reads sources.tsv (url <TAB> category <TAB> priority <TAB> pfsense_version_notes
<TAB> slug), fetches each URL, strips site chrome, and writes a clean Markdown
file under docs/<category>/<slug>.md with YAML frontmatter.

The `slug` column drives the output basename (e.g. `resolver.md`,
`dns-over-tls.md`); if absent, a short slug is derived from the URL path
(`index.html` -> `<parent>-index`). This mirrors the sibling pfsense-kea-kb
naming so both KBs stay consistent and greppable.

Converter fallback chain (first available wins):
  1. requests + beautifulsoup4 + html2text
  2. pandoc -f html -t markdown   (if pandoc on PATH)
  3. lynx -dump / w3m -dump       (if on PATH)

Usage:
  python3 fetch_docs.py                 # fetch everything
  python3 fetch_docs.py --only upstream-dns
  python3 fetch_docs.py --dry-run       # fetch exactly 1 URL
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(ROOT, "sources.tsv")
DOCS = os.path.join(ROOT, "docs")
FAILED = os.path.join(ROOT, "failed.tsv")


def slugify(url: str) -> str:
    """Fallback short slug from the URL path.

    `index.html` -> `<parent>-index`; otherwise the last path segment stem.
    """
    path = url.split("#")[0].rstrip("/")
    seg = path.split("/")[-1]
    if seg in ("", "index.html"):
        parent = path.split("/")[-2] if len(path.split("/")) > 1 else "page"
        return f"{parent}-index"
    return seg.replace(".html", "")


def fetch_html(url: str, timeout: int = 20) -> str | None:
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (kb-fetcher)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
        for enc in ("utf-8", "latin-1"):
            try:
                return raw.decode(enc)
            except UnicodeDecodeError:
                continue
        return raw.decode("utf-8", "replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        print(f"  ! fetch failed: {url} ({e})", file=sys.stderr)
        return None


def strip_with_bs4(html: str):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    for sel in [
        "script", "style", "nav", "footer", "#sidebar", "#topnav",
        ".related", ".footer", ".sphinxsidebar", "header",
    ]:
        for node in soup.select(sel):
            node.decompose()
    main = soup.find("article") or soup.find("div", class_="document") or soup.body
    title = soup.title.get_text(strip=True) if soup.title else ""
    text = main.get_text("\n") if main else soup.get_text("\n")
    return title, text


def convert(url: str, html: str):
    # 1. bs4 + html2text
    try:
        from bs4 import BeautifulSoup  # noqa: F401

        title, _text = strip_with_bs4(html)
        try:
            import html2text

            # Strip site chrome BEFORE conversion so nav/footer/header text
            # does not leak into the Markdown output.
            soup = BeautifulSoup(html, "html.parser")
            for sel in [
                "script", "style", "nav", "footer", "#sidebar", "#topnav",
                ".related", ".footer", ".sphinxsidebar", "header",
            ]:
                for node in soup.select(sel):
                    node.decompose()
            main = (
                soup.find("article")
                or soup.find("div", class_="document")
                or soup.body
            )
            h = html2text.HTML2Text()
            h.body_width = 0
            md = h.handle(str(main)) if main else h.handle(str(soup))
            return title, md, "bs4+html2text"
        except Exception:
            _, text = strip_with_bs4(html)
            return title, text, "bs4+text"
    except Exception:
        pass
    # 2. pandoc
    if shutil.which("pandoc"):
        try:
            p = subprocess.run(
                ["pandoc", "-f", "html", "-t", "markdown"],
                input=html.encode(), capture_output=True, timeout=30,
            )
            if p.returncode == 0:
                return "", p.stdout.decode("utf-8", "replace"), "pandoc"
        except Exception:
            pass
    # 3. lynx / w3m
    for cmd in (["lynx", "-dump"], ["w3m", "-dump"]):
        if shutil.which(cmd[0]):
            try:
                p = subprocess.run(cmd + [url], capture_output=True, timeout=30)
                if p.returncode == 0:
                    return "", p.stdout.decode("utf-8", "replace"), cmd[0]
            except Exception:
                pass
    return "", "", "NONE"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="only fetch this category")
    ap.add_argument("--dry-run", action="store_true", help="fetch exactly 1 URL")
    args = ap.parse_args()

    rows = []
    with open(SOURCES, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            rows.append(row)
    if args.only:
        rows = [r for r in rows if r["category"] == args.only]
    if args.dry_run:
        rows = rows[:1]

    os.makedirs(DOCS, exist_ok=True)
    failed = []
    for row in rows:
        url = row["url"]
        cat = row["category"]
        slug = row.get("slug") or slugify(url)
        print(f"Fetching [{cat}] {url} -> {slug}.md")
        html = fetch_html(url)
        if not html:
            failed.append((url, "fetch_error"))
            continue
        title, md, conv = convert(url, html)
        if conv == "NONE":
            failed.append((url, "no_converter"))
            continue
        outdir = os.path.join(DOCS, cat)
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, slug + ".md")
        today = dt.date.today().isoformat()
        front = (
            f"---\n"
            f"source_url: {url}\n"
            f"title: {title}\n"
            f"category: {cat}\n"
            f"priority: {row.get('priority', '')}\n"
            f"pfsense_version_notes: {row.get('pfsense_version_notes', '')}\n"
            f"fetched_date: {today}\n"
            f"converter: {conv}\n"
            f"---\n\n"
        )
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(front + md)
        print(f"  -> wrote {outpath} (converter={conv})")

    with open(FAILED, "w", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["url", "reason"])
        for u, reason in failed:
            w.writerow([u, reason])
    print(f"Done. {len(failed)} failed -> {FAILED}")


if __name__ == "__main__":
    main()
