# QA-REPORT

Final QA for the `pfsense-dns-kb` knowledge base. Generated 2026-08-13.

## Checks

### 1. Source coverage (sources.tsv → docs/)
- `sources.tsv` declares **22** curated URLs across 5 categories.
- Imported docs: **22** (`find docs -name '*.md' | wc -l` → 22).
- `failed.tsv` exists and lists **0** failures (all sources fetched 200).
- **Result: PASS** — every URL is either imported or in `failed.tsv`.

### 2. Non-empty / no stubs
- No imported `.md` is empty or <2KB. The smallest genuine pages
  (`resolver.md` 1095 B, `forwarder.md` 1840 B) are real pfSense landing pages
  (intro + sub-page links), not stubs.
- No `TODO`/`FIXME`/placeholder text in any doc.
- **Result: PASS**.

### 3. Chrome-free
- `rg -l "Was this page helpful|Give Feedback|Netgate Logo|Sphinx sidebar" docs/`
  returns nothing.
- The fetch pipeline strips `script/style/nav/footer/header/#sidebar` before
  conversion, so Sphinx chrome does not leak into Markdown.
- **Result: PASS**.

### 4. Index completeness
- `INDEX.md` lists all 22 docs (path, title, category, summary).
- `index.json` loads cleanly (`json.load` → 22 docs) and mirrors INDEX.md.
- Cross-check: indexed paths == actual `docs/**/*.md` paths (0 missing).
- **Result: PASS**.

### 5. Retrieval works
- `./scripts/search.sh "forwarding mode"` returns hits in
  `troubleshooting-dns.md`, `interfaces-and-dns.md`, `dns-over-tls.md`.
- `python3 scripts/refresh.py --check` runs and reports all 22 sources
  `ok` (last_checked 2026-08-13, 0 days old).
- `rg` for "Unbound", "forwarding mode", "DNS over TLS" all return expected hits.
- **Result: PASS**.

## Deliverables present
- `docs/` — 22 imported docs (pfsense-dns ×7, pfsense-ops ×5, pfsense-guides ×3,
  upstream-dns ×4, community ×3)
- `notes/` — 4 synthesized notes (resolver-vs-forwarder, dns-over-tls,
  dhcp-dns-registration, dns-rebinding)
- `scripts/` — fetch_docs.py, refresh.py, search.sh
- `sources.tsv`, `INDEX.md`, `README.md`, `index.json`, `freshness.tsv`,
  `mkdocs.yml`, `.gitignore`, `QA-REPORT.md`

## Version caveats recorded
- DNS over TLS is **Resolver-only** (not in the Forwarder).
- DNSSEC must be **OFF** in forwarding mode.
- Unbound DoT cert-validation gotcha (forum/155225): omit the TLS hostname and
  any cert is accepted — recorded in `notes/dns-over-tls.md` and the community
  doc frontmatter.

## Scope fidelity
- In scope: pfSense DNS Resolver/Forwarder + ops/troubleshooting/recipes +
  upstream Unbound/dnsmasq + community.
- Out of scope (correctly excluded): Dynamic DNS (`services/dyndns/*`),
  RAG/vector search, LLM summarization, box editing.

## Final verdict
**ALL 5 CHECKS PASS.** Knowledge base is complete, offline, git-versioned, and
retrievable.
