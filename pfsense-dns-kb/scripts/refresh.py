#!/usr/bin/env python3
"""Refresh pfSense DNS docs and track freshness.

Re-fetches every source in sources.tsv, rewrites docs/<cat>/<slug>.md with an
updated `fetched_date`, and writes freshness.tsv (url, last_checked, status).

--check : do not re-fetch; report sources whose last_checked is older than
          --stale-days (default 90). Exits non-zero if any are stale.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import sys

import fetch_docs as fd

ROOT = fd.ROOT
FRESH = os.path.join(ROOT, "freshness.tsv")
STALE_DAYS = 90


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report stale sources only")
    ap.add_argument("--stale-days", type=int, default=STALE_DAYS)
    args = ap.parse_args()

    rows = []
    with open(fd.SOURCES, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            rows.append(r)

    if args.check:
        cur: dict[str, str] = {}
        if os.path.exists(FRESH):
            with open(FRESH, encoding="utf-8") as f:
                for r in csv.DictReader(f, delimiter="\t"):
                    cur[r["url"]] = r["last_checked"]
        today = dt.date.today()
        print(f"Stale check (>{args.stale_days}d):")
        any_stale = False
        for r in rows:
            lc = cur.get(r["url"], "?")
            try:
                age = (today - dt.date.fromisoformat(lc)).days
            except Exception:
                age = -1
            flag = "STALE" if age > args.stale_days else "ok"
            if flag == "STALE":
                any_stale = True
            print(f"  [{flag}] {r['url']} (last_checked={lc}, {age}d)")
        sys.exit(1 if any_stale else 0)

    failed: list[tuple[str, str]] = []
    for r in rows:
        url = r["url"]
        cat = r["category"]
        slug = r.get("slug") or fd.slugify(url)
        html = fd.fetch_html(url)
        if not html:
            failed.append((url, "fetch_error"))
            continue
        title, md, conv = fd.convert(url, html)
        if conv == "NONE":
            failed.append((url, "no_converter"))
            continue
        outdir = os.path.join(fd.DOCS, cat)
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, slug + ".md")
        today = dt.date.today().isoformat()
        front = (
            f"---\n"
            f"source_url: {url}\n"
            f"title: {title}\n"
            f"category: {cat}\n"
            f"priority: {r.get('priority', '')}\n"
            f"pfsense_version_notes: {r.get('pfsense_version_notes', '')}\n"
            f"fetched_date: {today}\n"
            f"converter: {conv}\n"
            f"---\n\n"
        )
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(front + md)

    fset = {u for u, _ in failed}
    with open(FRESH, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["url", "last_checked", "status"])
        for r in rows:
            w.writerow([r["url"], dt.date.today().isoformat(),
                        "dead" if r["url"] in fset else "ok"])

    print(f"Refreshed {len(rows) - len(failed)}; {len(failed)} failed -> {FRESH}")


if __name__ == "__main__":
    main()
