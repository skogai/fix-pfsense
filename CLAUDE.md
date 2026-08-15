# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repo layout

This repo (`aldervall/fix-pfsense`) is a workspace for pfSense-related tooling and documentation, not a single buildable project. It has no root-level build/test/lint commands.

- `pfsense-dns-kb/` — offline, git-versioned Markdown knowledge base for pfSense DNS (Unbound resolver, dnsmasq forwarder). Tracked in this repo.
- `pfsense-kea-kb/` — offline knowledge base for pfSense's Kea DHCP backend. Tracked in this repo.
- `pfsense-mcp-server/` — a fork of `gensecaihq/pfsense-mcp-server` (MCP server exposing the pfSense REST API v2 as tools). This is its **own independent git repository** (separate `origin`, ignored by this repo's `.gitignore` via `**/.git/`) — it is not tracked or committed here. See `pfsense-mcp-server/CLAUDE.md` for its build/test/lint commands and conventions.

Each knowledge base (`pfsense-dns-kb`, `pfsense-kea-kb`) has a `scripts/search.sh` for ripgrep-based search over its docs, and an `INDEX.md` / `index.json` for browsing its contents. Start with the KB's own README for reading order before making edits.
