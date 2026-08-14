---
source_url: https://docs.netgate.com/pfsense/en/latest/troubleshooting/dhcp-offline-leases.html
title: Troubleshooting Offline DHCP Leases
category: pfsense-ops
priority: 3
pfsense_version_notes: ""
fetched_date: 2026-08-13
converter: webfetch
---

# Troubleshooting Offline DHCP Leases

The **Status > DHCP Leases** page only reports clients as "online" if the MAC address for a given system appears in the ARP table on the firewall. This can be verified by checking **Diagnostics > ARP Table**.

Systems which have not communicated with or via the firewall in the past few minutes will appear as offline.

To check a system, try to ping it from **Diagnostics > Ping**. Even if the system does not respond to ping, that action will cause the system to appear in the ARP table if it is on the network, and would thus show online in the DHCP Leases list.

The [Arping Package](../packages/arping.html) may also be of interest. It is available under **System > Packages**. The [Nmap package](../packages/nmap.html) can also be used to perform an ARP-based subnet scan to locate online hosts even if they don't respond to ICMP.
