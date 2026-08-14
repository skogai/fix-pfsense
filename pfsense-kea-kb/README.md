# pfSense KEA DHCP Knowledge Base

A **local, offline knowledge base** for operating the **Kea DHCP** backend in pfSense®
software (and its relationship to the deprecated ISC DHCP backend and upstream Kea).

It contains 26 imported Markdown documents from three source families:

- **pfsense-core / pfsense-ops / pfsense-ha** — Netgate pfSense documentation
- **upstream-kea** — the upstream ISC Kea Administrator Reference Manual (ARM) and ISC migration guides
- **community** — Netgate forum threads and Netgate blog posts about Kea

The goal is to make Kea DHCP operable without a live internet connection: searching,
reading, and synthesizing notes all work from this folder.

## Reading Order

Start with concepts, then configuration, then HA/migration, then troubleshooting:

1. **Concepts** — `docs/pfsense-core/dhcp-index.md`, `docs/pfsense-ops/advanced-networking.md` (Server Backend selector)
2. **Kea Settings** — `docs/pfsense-core/kea-settings.md`
3. **IPv4 / IPv6** — `docs/pfsense-core/ipv4.md`, `docs/pfsense-core/ipv6.md`
4. **Relay** — `docs/pfsense-core/relay.md`
5. **HA conversion** — `docs/pfsense-ha/ha-kea-convert.md`
6. **Upstream Kea ARM** — `docs/upstream-kea/kea-arm-index.md`, `kea-config.md`, `kea-config-sections.md`, `kea-dhcp4.md`
7. **Migration** — `docs/upstream-kea/keama-migration.md`, `isc-dhcp-migration.md`
8. **Troubleshooting** — `docs/pfsense-ops/monitoring-*.md`, `docs/pfsense-ops/troubleshooting-*.md`
9. **Community** — `docs/community/*.md`

Synthesized notes that tie the sources together live in [`notes/`](notes/):
`kea-ha-vs-isc.md`, `kea-custom-json.md`, `kea-dns-registration.md`.

## How To Use

- **Search** the whole KB:
  ```sh
  ./scripts/search.sh "Kea HA"
  ```
  (wraps `rg`/ripgrep; case-insensitive, shows filenames + matching lines)

- **Refresh** sources and update freshness:
  ```sh
  python3 scripts/refresh.py          # re-fetch all sources
  python3 scripts/refresh.py --check  # list sources fetched >90 days ago
  ```

- **Optional HTML site** (requires `pip install mkdocs`):
  ```sh
  mkdocs build
  ```
  The `mkdocs.yml` config is provided but optional.

## File Layout

```
INDEX.md        Human-readable index of all 26 docs (grouped by category)
index.json      Machine-readable mirror of INDEX.md
README.md       This guide
sources.tsv     Source URL / category / priority table (feed for fetch/refresh)
docs/           The 26 imported Markdown files (frontmatter + content)
notes/          Synthesized comparison/reference notes
scripts/        search.sh (ripgrep wrapper) and refresh.py (fetcher/freshness)
QA-REPORT.md    Quality-assurance checks run at build time
```

> Git init/commit is handled by the user in a shell; this KB is designed to be
> committed as-is.
