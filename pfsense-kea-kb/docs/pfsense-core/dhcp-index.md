---
source_url: https://docs.netgate.com/pfsense/en/latest/services/dhcp/index.html
title: DHCP
category: pfsense-core
priority: 1
pfsense_version_notes:
fetched_date: 2026-08-13
converter: webfetch
---

# DHCP

Dynamic Host Configuration Protocol (DHCP), allows a device such as pfSense® software to dynamically allocate IP addresses to clients from predefined pools of addresses. DHCP also sends configuration information to clients such as a gateway, DNS servers, domain name, and other useful settings.

There are currently two available DHCP backends: Kea DHCP and ISC DHCP. Kea is more modern and under active development, ISC DHCP is deprecated and will be removed in future versions of pfSense software. The backend can be changed under **System > Advanced**, **Networking** tab ([Server Backend](../../config/advanced-networking.html#config-advanced-net-dhcp-backend)).

-   [Kea Settings Tab](kea-settings.html)
-   [DHCPv4 Server](ipv4.html)
-   [DHCPv6 Server](ipv6.html)
-   [DHCPv4 & DHCPv6 Relay](relay.html)
-   [Using DHCP Search Domains on Windows DHCP Clients](client-search-domain.html)
-   [Static Mappings Inside DHCP Pools](mappings-in-pools.html)

See also

-   [DHCPv4 Status](../../monitoring/status/dhcp-ipv4.html)
-   [DHCPv6 Status](../../monitoring/status/dhcp-ipv6.html)
-   [DHCP Logs](../../monitoring/logs/dhcp.html)
-   [Troubleshooting DHCPv6 Client XID Mismatches](../../troubleshooting/dhcpv6-xid-mismatch.html)
-   [Troubleshooting Offline DHCP Leases](../../troubleshooting/dhcp-offline-leases.html)
