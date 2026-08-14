---
source_url: https://www.netgate.com/blog/netgate-adds-kea-dhcp-to-pfsense-plus-software-version-23.09-1
title: Netgate Adds Kea DHCP to pfSense Plus Software Version 23.09
category: community
priority: 3
pfsense_version_notes: Kea introduced in pfSense Plus 23.09
fetched_date: 2026-08-13
converter: webfetch
---

# Netgate Adds Kea DHCP to pfSense Plus Software Version 23.09

**Written by:** Bill Rathbone
**Date:** November 06, 2023

> **CLAIM / VERSION CAVEAT:** This is the original announcement that Kea was added as an opt-in feature in pfSense Plus 23.09. The listed "missing features" (DNS registration, HA, custom options, etc.) were accurate for 23.09 but were added in later releases (DNS/HA in 24.08; custom config in 25.03). Treat the feature list as version 23.09-specific.

Netgate® has begun the migration of pfSense® Plus software to [Kea DHCP](https://www.isc.org/kea/) as a replacement for ISC DHCP, starting with release version 23.09. Kea DHCP is initially available as an opt-in feature, allowing users to test it with their own networks. It will become the default in a future release.

## Why the change is necessary

The Internet Systems Consortium (ISC) distributes two full-featured, open-source, standards-based DHCP servers: Kea DHCP and ISC DHCP. ISC announced the End of Life (EOL) of the ISC DHCP server, and ended maintenance on it [at the end of 2022](https://www.isc.org/blogs/isc-dhcp-eol/).

Kea is newer, includes all the most-requested features, and is designed for a more modern network environment. Netgate has successfully used the Kea DHCP server in its TNSR software for a number of years.

## Managing an incremental transition

Kea DHCP has been added as an opt-in feature in this release of pfSense Plus software in order to allow users to test and validate the functionality in their own networks. Netgate's developers worked to minimize disruption by using the same DHCP user interface and settings as the legacy ISC DHCP server uses. This means essentially replicating the pfSense DHCP feature set with the entirely new Kea DHCP backend, despite having a different configuration format and entirely different control interface. We view it as important during the transition period that users can easily switch between the ISC and Kea DHCP servers in pfSense by using the same configuration file and settings.

Basic functionality is present in version 23.09, but the Kea implementation lacks the following DHCP server features:

- Local DNS Resolver/Forwarder Registration for static and dynamic DHCP clients
- Remote DNS server registration
- DHCPv6 Prefix Delegation
- High Availability Failover
- Lease statistics/graphs
- Custom DHCP options

Note: If you have assigned hostnames to devices on your network using static leases, or rely on dynamic lease registration in DNS, switching to Kea DHCP results in those hostnames being ignored. The static lease configuration is kept, so switching back to ISC DHCP will restore the functionality.

Netgate will transition to Kea DHCP as the default DHCP server in pfSense Plus software once integration is complete, and the deprecated ISC DHCP server will eventually be removed.

## How to enable the Kea DHCP server

You can switch to the Kea DHCP server by:

- Navigating to **System > Advanced**
- Choosing the **Networking** tab
- Changing the new **Server Backend** radio button in the **DHCP Options** section to "**Kea DHCP**"

Switching back to the ISC DHCP server is done by following the same steps, but selecting "ISC DHCP (LEGACY)" as the Server Backend instead.

## Summary

Our commitment to the open-source community and to our customers drives Netgate to continue to innovate. The migration to Kea DHCP is essential, and the work required in pfSense Plus software to support its integration is complex. Release 23.09, which offers Kea DHCP as an opt-in feature, is the first step in the process of making pfSense Plus a more powerful product with as little disruption to users as possible.

## Where to Learn More

- pfSense Plus Release Notes for version 23.09: https://docs.netgate.com/pfsense/en/latest/releases/23-09.html
- ISC's Kea DHCP overview and documentation: https://www.isc.org/kea/
