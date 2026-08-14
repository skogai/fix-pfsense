---
source_url: https://docs.netgate.com/pfsense/en/latest/recipes/high-availability-kea-convert.html
title: Converting High Availability DHCP from ISC to Kea
category: pfsense-ha
priority: 1
pfsense_version_notes: Kea HA requires Plus 24.11+/CE 2.8.0+; CE 2.7.2 lacks Kea HA
fetched_date: 2026-08-13
converter: webfetch
---

# Converting High Availability DHCP from ISC to Kea

This document covers how to convert an existing pfSense® software High Availability (HA) setup from the ISC DHCP backend to the Kea DHCP backend and also explains differences in how each of these backends implements HA failover.

> **Warning**
> The ISC DHCP backend is deprecated and will eventually be removed, so converting to the Kea DHCP backend is the best practice.

> **See also**
> - Server Backend
> - High Availability Configuration Example

The Kea implementation of HA is fundamentally different from ISC and as a consequence, the HA/failover settings are not compatible between ISC DHCP and Kea DHCP. The conversion process is manual and largely the same as setting up high availability for Kea DHCP from scratch. However, since the Kea HA configuration is much simpler, it is not a lengthy or difficult process.

## DHCP Backend Differences

There are important differences in high availability operation between the ISC DHCP backend and the Kea DHCP backend, including:

- **Kea DHCP** operates HA in "hot standby" mode where the primary node serves leases exclusively unless it fails, in which case the standby node serves leases until the primary recovers. Both nodes share lease data as needed. This is similar to the HA behavior of pfSense software in general.
  **ISC DHCP** behaves closer to an "active/active" load balanced mode which has each node coordinate and serve part of each pool simultaneously and exchange lease data in both directions.

- **Kea** has a global setting declaring the role of a node as primary or standby.
  **ISC** attempts to automatically determine the role by inspecting the properties of CARP VIPs which is not always accurate.

- **Kea** HA serves leases from a secondary node if it boots while the primary node is offline.
  **ISC** fails to serve leases from a secondary unless it sees the primary node online first.

- **Kea DHCP** provides HA for IPv6 in DHCPv6.
  **ISC** is not capable of providing IPv6 HA.
  - As a part of HA for DHCPv6, XMLRPC configuration synchronization can copy Kea DHCPv6 settings between HA nodes.
  - XMLRPC configuration synchronization for Kea DHCPv6 also synchronizes Router Advertisement settings.

  > **Warning**
  > If an HA cluster had IPv6 configured separately on each node before converting to Kea, the configuration on the secondary node will be overwritten once XMLRPC configuration synchronization is enabled for DHCPv6 on the primary node. If a pool was split between two nodes in this manner, it can be combined into one large pool after converting.

- **Kea** has one set of global settings for HA per node.
  **ISC** requires per-interface failover configuration.
  - Despite being configured in different ways, XMLRPC synchronization of HA DHCP settings for Kea and ISC both automatically adjust the values needed for settings on the primary and secondary.

- **Kea** uses one address per node for HA traffic (lease synchronization, heartbeats, etc.).
  **ISC** uses manually configured failover addresses on every DHCP interface separately.
  - The best practice with Kea is to use the Sync interface for DHCP HA traffic since it uses a single address. This is safer and more secure as it does not need to flow over every interface separately where it may be exposed to end-user networks.
  - Similarly, firewall rules for Kea only need to be on one interface (e.g. Sync), where ISC DHCP may need firewall rules on every DHCP server interface.

- **Kea** can use IPv4 or IPv6 for HA traffic in both DHCPv4 and DHCPv6.
  **ISC** can only use IPv4.

- **Kea** lease synchronization copies hostnames between nodes.
  **ISC** lease synchronization does not copy hostnames.

- **Kea** tracks HA status globally for each node.
  **ISC** tracks HA status separately for each address pool.

- **Kea** can optionally encrypt HA traffic using TLS and can also optionally require a client certificate to validate it is speaking to the expected peer.
  **ISC** does not offer encryption or authentication of failover traffic.
  - The TLS settings for HA do not synchronize via XMLRPC configuration synchronization as each node may need to use different certificates.

### Backend Difference Summary

The following table summarizes the differences between the backends:

| Feature | Kea | ISC |
| --- | --- | --- |
| Supported Upstream | Yes | No (Deprecated) |
| HA Style | Hot Standby | Active/Active |
| Active/Passive Role | Manual | Automatic |
| Secondary Only Boot | Yes | No |
| DHCPv6 HA | Yes | No |
| DHCPv6+RA XMLRPC Sync | Yes | No |
| HA Config | Global | Per-Interface |
| IP Addresses for HA | One per Node | One per Interface per Node |
| HA Interfaces | Sync | All Enabled for DHCP |
| HA Transports | IPv4 or IPv6 | IPv4 Only |
| HA Copies Hostnames | Yes | No |
| HA Status | Per Node | Per Pool |
| TLS Encryption | Yes (Optional) | No |
| TLS Authentication | Yes (Optional) | No |

## Status Differences

The DHCP Lease status for failover information changed significantly between ISC DHCP and Kea DHCP.

The ISC DHCP Lease status page shows a list of **Failover Groups** at the top of the page, as described in Pool Status (HA/Failover) – ISC DHCP Only. Each pool has a state for both nodes in the group and the last time the state changed. The information is fairly plain, with only the text of the state fields changing to indicate status.

In contrast, the Kea DHCP HA status is much more user-friendly. It has moved to the bottom of the DHCP Lease status page, as shown in High Availability Status – Kea DHCP Only. The Kea DHCP HA status section includes an easy to interpret icon indicating the current state along with information about each node and its status, and a timer indicating the last received heartbeat.

## Conversion Process

### Converting DHCPv4 from ISC to Kea

- Switch the backend to Kea (Server Backend)
- Add firewall rules on the primary node Sync interface which pass IPv4 Kea HA traffic (Setup Sync Interface)
- Enable and configure Kea DHCP HA on the primary node (Configure DHCP for IPv4)
- Check the DHCP status and ensure the two nodes are communicating properly (High Availability Status – Kea DHCP Only)
- Remove any old firewall rules which explicitly passed ISC DHCP failover traffic (TCP ports `519` and `520`). These could be on interface tabs, interface group tabs, floating rules, etc.

### Adding DHCPv6 HA after switching to Kea

- Add firewall rules on the primary node Sync interface which pass IPv6 Kea HA traffic (Setup Sync Interface)
- Add an IPv6 Link-Local CARP VIP for LAN if one does not already exist, such as `fe80::1:1/64` (LAN IP Addresses)
- Enable and configure Kea DHCPv6 HA on the primary node (Configure DHCPv6 HA)
- Configure DHCPv6 interfaces to use a CARP VIP for DNS (Configure DHCPv6 Interface Settings)
- Configure Router Advertisements for HA using the link-local CARP VIP as the **RA Interface** (Configure IPv6 Router Advertisements)
- Enable XMLRPC Synchronization for DHCPv6 (Configure Configuration Synchronization (XMLRPC))
- Adjust the DHCPv6 configuration to account for changes in the pool addresses if the HA cluster had DHCPv6 configured manually without synchronization.
- Check the DHCP status and ensure the two nodes are communicating properly (High Availability Status – Kea DHCP Only)
