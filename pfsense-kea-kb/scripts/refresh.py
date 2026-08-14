#!/usr/bin/env python3
"""Refresh the pfSense KEA DHCP knowledge base.

Re-fetches every source listed in sources.tsv (reusing the fetch/convert logic
from scripts/fetch_docs.py), rewrites each doc's `fetched_date` frontmatter,
and writes `freshness.tsv` (url <TAB> last_checked <TAB> status).

Modes:
  python3 refresh.py            # re-fetch all sources and refresh freshness
  python3 refresh.py --check    # only print sources last fetched >90 days ago

No external services (databases, APIs) are required; only outbound HTTPS is used
by the fetch step, which degrades gracefully (status recorded as "error") when
the network is unavailable.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(ROOT, "sources.tsv")
DOCS = os.path.join(ROOT, "docs")
FRESHNESS = os.path.join(ROOT, "freshness.tsv")

# Import helpers from the sibling fetcher.
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import fetch_docs as fd  # noqa: E402

STALE_DAYS = 90


# Map each known source_url -> local doc path by scanning frontmatter (the
# local filenames use short stems and do not equal slugify(url)).
_URL_TO_DOC = {}

def _build_url_map() -> None:
    for cat in os.listdir(DOCS):
        d = os.path.join(DOCS, cat)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(d, fn)
            m = re.search(r"^source_url:\s*(\S+)", open(p, encoding="utf-8").read(), re.M)
            if m:
                _URL_TO_DOC[m.group(1).rstrip("/")] = p

def current_doc_for(category: str, url: str) -> str | None:
    if not _URL_TO_DOC:
        _build_url_map()
    return _URL_TO_DOC.get(url) or _URL_TO_DOC.get(url.rstrip("/"))


def update_fetched_date(path: str, today: str) -> None:
    txt = open(path, encoding="utf-8").read()
    if re.search(r"^fetched_date:\s*.*$", txt, re.M):
        txt = re.sub(r"^fetched_date:\s*.*$", f"fetched_date: {today}",
                     txt, count=1, flags=re.M)
    else:
        # insert before closing --- of frontmatter
        txt = re.sub(r"^---\s*$", f"fetched_date: {today}\n---", txt,
                     count=1, flags=re.M)
    open(path, "w", encoding="utf-8").write(txt)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="only report sources fetched >90 days ago")
    args = ap.parse_args()

    rows = []
    with open(SOURCES, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            rows.append(row)

    today = dt.date.today()
    fresh_rows = []  # (url, last_checked, status)

    if args.check:
        # Read existing fetched_date from each doc (no network).
        print(f"Checking staleness (> {STALE_DAYS} days since fetch):")
        any_stale = False
        for row in rows:
            url = row["url"]
            cat = row["category"]
            path = current_doc_for(cat, url)
            fetched = "?"
            if path:
                m = re.search(r"^fetched_date:\s*(\S+)",
                              open(path, encoding="utf-8").read(), re.M)
                if m:
                    fetched = m.group(1)
            stale = False
            try:
                fd_date = dt.date.fromisoformat(fetched)
                stale = (today - fd_date).days > STALE_DAYS
            except ValueError:
                stale = True
            flag = "STALE" if stale else "ok"
            if stale:
                any_stale = True
            print(f"  [{flag}] {cat:14} {fetched:12} {url}")
            fresh_rows.append((url, fetched, "cached"))
        print("RESULT:", "stale sources found" if any_stale else "all fresh")
        # Also write freshness.tsv so it reflects cached state.
        _write_freshness(fresh_rows)
        return

    # Full refresh: re-fetch network content.
    for row in rows:
        url = row["url"]
        cat = row["category"]
        status = "error"
        try:
            html = fd.fetch_html(url)
            if html:
                title, md, conv = fd.convert(url, html)
                if conv != "NONE" and md.strip():
                    path = current_doc_for(cat, url)
                    if path:
                        update_fetched_date(path, today.isoformat())
                        status = "ok"
                    else:
                        status = "no_local_doc"
                else:
                    status = "convert_failed"
            else:
                status = "fetch_failed"
        except Exception as e:  # noqa: BLE001
            status = f"error:{e}"
        fresh_rows.append((url, today.isoformat(), status))
        print(f"  [{status}] {cat:14} {url}")

    _write_freshness(fresh_rows)
    print(f"Wrote {FRESHNESS}")


def _write_freshness(rows) -> None:
    with open(FRESHNESS, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["url", "last_checked", "status"])
        for r in rows:
            w.writerow(r)


if __name__ == "__main__":
    main()
