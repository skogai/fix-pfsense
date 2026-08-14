# pfSense DNS Knowledge Base

A local, offline, git-versioned Markdown knowledge base for **pfSense DNS** —
the **DNS Resolver (Unbound)** and **DNS Forwarder (dnsmasq)** subsystems plus
their surrounding ops, troubleshooting, recipes, upstream references, and
community threads. This is the DNS sibling of `../pfsense-kea-kb/`.

## What's inside

- `docs/pfsense-dns/` — Resolver, Forwarder, resolution process, rebinding, wildcards, overrides
- `docs/pfsense-ops/` — diagnostics, interfaces-and-DNS, troubleshooting
- `docs/pfsense-guides/` — DNS over TLS, block/redirect external DNS recipes
- `docs/upstream-dns/` — Unbound + dnsmasq upstream references
- `docs/community/` — Netgate blog/forum threads (version-caveated)
- `notes/` — synthesized deep-dives (resolver vs forwarder, DoT, DHCP↔DNS, rebinding)
- `scripts/` — `fetch_docs.py` (import), `refresh.py` (re-fetch + freshness), `search.sh` (ripgrep)
- `sources.tsv` — the 22 curated URLs · `INDEX.md` — full doc index · `index.json` — machine index · `freshness.tsv` — last-checked

## Reading order (recommended)

1. **Concepts**
   - [DNS](docs/pfsense-dns/dns-index.md)
   - [DNS Resolution Process](docs/pfsense-dns/resolution-process.md)
2. **Resolver vs Forwarder**
   - [DNS Resolver](docs/pfsense-dns/resolver.md)
   - [DNS Forwarder](docs/pfsense-dns/forwarder.md)
   - [Note: Resolver vs Forwarder](notes/resolver-vs-forwarder.md)
3. **Rebinding / Wildcards / Overrides**
   - [DNS Rebinding Protections](docs/pfsense-dns/rebinding.md)
   - [Wildcard Records](docs/pfsense-dns/wildcards.md)
   - [Host / Domain Overrides](docs/pfsense-dns/forwarder-overrides.md)
4. **DNS over TLS**
   - [Configuring DNS over TLS](docs/pfsense-guides/dns-over-tls.md)
   - [Note: DNS over TLS](notes/dns-over-tls.md)
5. **Operations / Troubleshooting**
   - [DNS Lookup](docs/pfsense-ops/diag-dns.md)
   - [Interfaces and DNS](docs/pfsense-ops/interfaces-and-dns.md)
   - [Troubleshooting DNS](docs/pfsense-ops/troubleshooting-dns.md)
   - [Troubleshooting DNS Cache](docs/pfsense-ops/troubleshooting-dns-cache.md)
   - [Troubleshooting DNS Queries](docs/pfsense-ops/troubleshooting-dns-queries.md)
6. **Guides / Recipes**
   - [Blocking External Client DNS Queries](docs/pfsense-guides/dns-block-external.md)
   - [Redirecting Client DNS Requests](docs/pfsense-guides/dns-redirect.md)
7. **Upstream references**
   - [Unbound (index)](docs/upstream-dns/unbound-index.md)
   - [unbound.conf(5)](docs/upstream-dns/unbound-conf.md)
   - [dnsmasq (doc)](docs/upstream-dns/dnsmasq-doc.md)
   - [dnsmasq(8)](docs/upstream-dns/dnsmasq-man.md)
8. **Community**
   - [Blog: DNS over TLS with pfSense](docs/community/blog-dns-over-tls.md)
   - [Forum: Unbound DoT cert-validation gotcha](docs/community/forum-unbound-dot-cert.md)
   - [Forum: Configure DoT in 2.4.4](docs/community/forum-dns-over-tls.md)
9. **Notes**
   - [Resolver vs Forwarder](notes/resolver-vs-forwarder.md)
   - [DNS over TLS](notes/dns-over-tls.md)
   - [DHCP ↔ DNS Registration](notes/dhcp-dns-registration.md)
   - [DNS Rebinding](notes/dns-rebinding.md)

## Searching

```bash
./scripts/search.sh "forwarding mode"
./scripts/search.sh "DNS over TLS" -i
```

Requires `ripgrep` (`rg`); falls back to `grep -r` if absent.

## Keeping it fresh

```bash
python3 scripts/refresh.py            # re-fetch all sources, update fetched_date
python3 scripts/refresh.py --check    # report sources older than 90 days
```

## Optional: browse as a site (MkDocs)

`mkdocs.yml` is provided. If MkDocs is installed:

```bash
pip install mkdocs mkdocs-material   # or: pip install --break-system-packages mkdocs
mkdocs build --strict                # or: mkdocs serve
```

`notes/`, `README.md`, and `INDEX.md` live outside `docs/` by design (they are
KB meta, not imported pages); `mkdocs.yml` references them via `docs_dir: .`.

## Scope notes

- **In scope:** pfSense DNS Resolver/Forwarder + cross-linked ops/troubleshooting/recipes + upstream Unbound/dnsmasq + community.
- **Out of scope:** Dynamic DNS (`services/dyndns/*`, deferred to its own KB), RAG/vector search, LLM summarization, editing any pfSense box.
- **Version caveats** are recorded per-source in frontmatter and in the notes (e.g. DNS over TLS is Resolver-only; DNSSEC must be OFF in forwarding mode; Unbound DoT cert-validation gotcha).
