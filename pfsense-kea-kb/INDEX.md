# pfSense KEA DHCP Knowledge Base — Index

A local mirror of pfSense and upstream Kea DHCP documentation, focused on the **Kea** DHCP backend. This file lists every imported doc with a one-line summary. The machine-readable mirror is `index.json`; the human guide is `README.md`.

## pfsense-core

| Doc | Title | Category | Summary |
| --- | --- | --- | --- |
| [docs/pfsense-core/dhcp-index.md](docs/pfsense-core/dhcp-index.md) | DHCP | pfsense-core | Index/overview of pfSense DHCP docs, including choosing the ISC vs Kea backend. |
| [docs/pfsense-core/kea-settings.md](docs/pfsense-core/kea-settings.md) | Kea Settings Tab | pfsense-core | Global Kea options: DNS Resolver registration, High Availability (hot standby), optional TLS, and custom JSON snippets. |
| [docs/pfsense-core/ipv4.md](docs/pfsense-core/ipv4.md) | DHCPv4 Server | pfsense-core | Per-interface Kea DHCPv4 configuration: pools, options, static mappings, and failover. |
| [docs/pfsense-core/ipv6.md](docs/pfsense-core/ipv6.md) | DHCPv6 Server | pfsense-core | Per-interface Kea DHCPv6 configuration, including Router Advertisement coordination. |
| [docs/pfsense-core/relay.md](docs/pfsense-core/relay.md) | DHCPv4 & DHCPv6 Relay | pfsense-core | Forward DHCP(v4/v6) requests to an upstream or external DHCP server via the relay agent. |
| [docs/pfsense-core/client-search-domain.md](docs/pfsense-core/client-search-domain.md) | Using DHCP Search Domains on Windows DHCP Clients | pfsense-core | How to push DNS search domains to Windows clients through DHCP options. |
| [docs/pfsense-core/mappings-in-pools.md](docs/pfsense-core/mappings-in-pools.md) | Static Mappings Inside DHCP Pools | pfsense-core | Reserve fixed IP addresses for clients within an existing dynamic pool range. |

## pfsense-ops

| Doc | Title | Category | Summary |
| --- | --- | --- | --- |
| [docs/pfsense-ops/advanced-networking.md](docs/pfsense-ops/advanced-networking.md) | Networking | pfsense-ops | System > Advanced > Networking settings, including the Server Backend (ISC/Kea) selector. |
| [docs/pfsense-ops/monitoring-status-dhcp-ipv4.md](docs/pfsense-ops/monitoring-status-dhcp-ipv4.md) | DHCPv4 Status | pfsense-ops | View active DHCPv4 leases and the Kea/ISC high-availability failover status. |
| [docs/pfsense-ops/monitoring-status-dhcp-ipv6.md](docs/pfsense-ops/monitoring-status-dhcp-ipv6.md) | DHCPv6 Status | pfsense-ops | View active DHCPv6 leases and delegated prefixes. |
| [docs/pfsense-ops/monitoring-logs-dhcp.md](docs/pfsense-ops/monitoring-logs-dhcp.md) | DHCP Logs | pfsense-ops | Where DHCP system logs live and how to read them when debugging. |
| [docs/pfsense-ops/troubleshooting-dhcpv6-xid-mismatch.md](docs/pfsense-ops/troubleshooting-dhcpv6-xid-mismatch.md) | Troubleshooting DHCPv6 Client XID Mismatches | pfsense-ops | Diagnose relay/transaction-ID (XID) mismatches seen in DHCPv6. |
| [docs/pfsense-ops/troubleshooting-dhcp-offline-leases.md](docs/pfsense-ops/troubleshooting-dhcp-offline-leases.md) | Troubleshooting Offline DHCP Leases | pfsense-ops | Why leases report as offline and how to resolve the condition. |

## pfsense-ha

| Doc | Title | Category | Summary |
| --- | --- | --- | --- |
| [docs/pfsense-ha/ha-kea-convert.md](docs/pfsense-ha/ha-kea-convert.md) | Converting High Availability DHCP from ISC to Kea | pfsense-ha | Step-by-step conversion of HA DHCP from ISC to Kea, with a backend-difference table. |

## upstream-kea

| Doc | Title | Category | Summary |
| --- | --- | --- | --- |
| [docs/upstream-kea/kea-arm-index.md](docs/upstream-kea/kea-arm-index.md) | Kea Administrator Reference Manual | upstream-kea | Landing/index page for the upstream Kea ARM documentation. |
| [docs/upstream-kea/kea-ha.md](docs/upstream-kea/kea-ha.md) | Kea High Availability (HA) — Page Not Found (HTTP 404) | upstream-kea | Known 404 stub; points to the Kea HA hooks chapter in the ARM. Expected/intentionally short. |
| [docs/upstream-kea/kea-config.md](docs/upstream-kea/kea-config.md) | 6. Kea Configuration | upstream-kea | Upstream Kea ARM introduction to the Kea configuration system. |
| [docs/upstream-kea/kea-dhcp4.md](docs/upstream-kea/kea-dhcp4.md) | 8. The DHCPv4 Server | upstream-kea | Upstream Kea ARM reference for the Kea DHCPv4 server (hooks, options, config). |
| [docs/upstream-kea/keama-migration.md](docs/upstream-kea/keama-migration.md) | Migrating from ISC DHCP to Kea DHCP using the Migration Assistant | upstream-kea | Using the KeaMA tool to convert ISC dhcpd configurations into Kea format. |
| [docs/upstream-kea/isc-dhcp-migration.md](docs/upstream-kea/isc-dhcp-migration.md) | Migrating to Kea from ISC DHCP | upstream-kea | ISC's general guidance for migrating from ISC DHCP to Kea. |
| [docs/upstream-kea/kea-ha-vs-isc.md](docs/upstream-kea/kea-ha-vs-isc.md) | Kea High Availability vs. ISC DHCP Failover | upstream-kea | Feature-by-feature comparison of Kea HA against ISC DHCP failover. |
| [docs/upstream-kea/kea-config-sections.md](docs/upstream-kea/kea-config-sections.md) | Kea Configuration Introduction | upstream-kea | Explains the structure and top-level sections of a Kea configuration file. |

## community

| Doc | Title | Category | Summary |
| --- | --- | --- | --- |
| [docs/community/forum-custom-config-196513.md](docs/community/forum-custom-config-196513.md) | Adding Custom Configuration in Kea DHCP Server | community | Community examples of pfSense 25.03 custom JSON config snippets for Kea. |
| [docs/community/forum-switch-188430.md](docs/community/forum-switch-188430.md) | switch over from ISC DHCP to Kea DHCP | community | Community discussion thread on migrating from ISC DHCP to Kea. |
| [docs/community/blog-improvements-kea-dhcp.md](docs/community/blog-improvements-kea-dhcp.md) | 24.08 Sneak Peek: Improvements to Kea DHCP… | community | Netgate blog on 24.08 Kea HA improvements and Unbound DNS resolution. |
| [docs/community/blog-kea-23-09.md](docs/community/blog-kea-23-09.md) | Netgate Adds Kea DHCP to pfSense Plus Software Version 23.09 | community | Announcement introducing Kea DHCP in pfSense Plus 23.09. |
