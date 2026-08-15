---
name: kb-search
description: Search the offline pfSense DNS and Kea DHCP knowledge bases (pfsense-dns-kb/, pfsense-kea-kb/) for troubleshooting, configuration, or reference answers. Use when the user asks a pfSense DNS (Unbound/dnsmasq) or Kea DHCP question.
---

This workspace has two offline, git-versioned Markdown knowledge bases:

- `pfsense-dns-kb/` — pfSense DNS Resolver (Unbound) and DNS Forwarder (dnsmasq)
- `pfsense-kea-kb/` — pfSense Kea DHCP backend (and its relationship to the deprecated ISC DHCP backend)

To answer a question:

1. Pick the relevant KB based on subject (DNS vs DHCP).
2. Search it with the KB's own script, run from the KB's root directory:
   ```bash
   ./scripts/search.sh "<query>"
   ```
   Both scripts wrap ripgrep over `docs/` (and `notes/` for the DNS KB); `pfsense-dns-kb`'s falls back to `grep -r` if `rg` is missing, `pfsense-kea-kb`'s requires `rg` on PATH.
3. For a broader browse instead of a keyword search, check `INDEX.md` (human-readable) or `index.json` (machine-readable) at the KB root, and the KB's own `README.md` for recommended reading order.
4. Read the matched doc(s) under `docs/` or `notes/` directly and answer from their contents — these KBs exist so answers can come from local, curated sources instead of a live web search.

Check `freshness.tsv` at the KB root if source recency matters — it tracks when each source was last checked against upstream.
