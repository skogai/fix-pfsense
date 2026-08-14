---
source_url: https://docs.netgate.com/pfsense/en/latest/monitoring/status/dhcp-ipv6.html
title: DHCPv6 Status
category: pfsense-ops
priority: 3
pfsense_version_notes: ""
fetched_date: 2026-08-13
converter: webfetch
---

# DHCPv6 Status

The current contents of the DHCPv6 lease database and related information are viewable at **Status > DHCPv6 leases**.

The page contains multiple sections with information about leases. The exact information and layout depends on the selected DHCP backend.

## DHCPv6 Leases

This section of the page lists DHCPv6 client leases and their properties, including:

- **Status:** The first column with no header contains two icons indicating the current status of the lease. Hover over the icon for a tooltip explaining the meaning of the icon.
- **Lease Type:** An icon indicating the type of DHCP lease assigned to this client, which can be one of:
  - **Static:** This lease entry is from a static DHCP mapping entry.
  - **Active:** A current lease from an active client.
  - **Expired:** A lease which has expired because a client did not renew it before its expiration time.
  - **Online:** An icon indicating whether the device is currently "online" as determined by the contents of the ARP table.
    - If a system shows online, then it has recently tried to communicate to or through this firewall.
    - A host marked as offline may be powered on and working, but it has not attempted communication to or through the firewall recently.
- **IPv6 Address:** IPv6 address assigned to the client by DHCP, or static mapping address.
- **DHCP Unique Identifier (DUID):** The **DHCP Unique Identifier** (DUID) of this client.
  - The DUID is meant to be unique *per device*.
  - IPv6 hosts are identified by a combination of the IAID and DUID.

> **Note**
> Due to variances in DHCPv6 clients between operating systems and manufacturers some DUID values are sized differently than others.

- **Hostname:** The hostname of the client (if known).
- **Start/End:** The beginning and end times of the DHCP lease.

> **Note**
> For static mappings the page prints `n/a` as static mapping leases do not have a start or end time, and they do not expire.

- **Actions:** Icons to take action on this lease. See Actions for details.

> **Note**
> This list only contains information on leases handed out by DHCPv6. If a client assigns itself an address some other way (e.g. SLAAC) it cannot be listed on this page.

### Search

The search box filters the contents of the **Leases** table based on keyword matching.

Enter a search string or UNIX regular expression into the box and click **Search** to filter the list to only matching records.

By default, the search looks at text from all fields in the lease record, but this can be limited to specific fields using the drop-down list.

### Actions

#### Add static mapping
To create a static mapping from a dynamic lease, click the icon to the right of the lease. This pre-fills the DUID of the client into the **Edit static mapping** screen.

> **See also**
> DHCPv6 Static Mappings

#### Edit static mapping
Entries for existing static mappings have the icon which takes the user to the page to edit that specific entry.

#### Wake on LAN Integration
Click to create a WOL entry for the MAC address.

> **See also**
> Wake on LAN

#### Delete a lease
While viewing the leases, an expired or inactive lease may be manually deleted by clicking the icon at the end of its line. This option is not available for active or static leases, only for offline or expired leases.

## Delegated Prefixes

When **Prefix Delegation** is enabled, the bottom of the page lists delegated prefixes and their routing.

Entries for each delegated prefix include the following information:

- **IPv6 Prefix:** The IPv6 prefix and length which the firewall has delegated to a DHCPv6 client.
- **Routed To:** The IPv6 address to which the firewall is routing the IPv6 prefix. The target address will match one of the leases in the list at the top of the screen.
- **IAID/DUID:** The IAID+DUID combination will match one of the leases in the list at the top of the screen and identifies the host to which the firewall is routing this prefix.
- **Start/End:** The start and end time of this delegation. If the client renews its delegation request, the times will update accordingly.
- **State:** The status of the delegation, which can be one of:
  - **Active:** A current delegation to an active client.
  - **Expired:** A delegation which has expired because a client did not renew it before its expiration time.

## Pool Usage Summary

The **Lease Utilization** section summarizes pool usage, giving a count of leases used in each pool configured in the DHCPv6 server.

## View inactive leases

By default, the page lists active and static leases. Clicking **Show all configured leases** makes the page display all leases, including inactive and expired leases.

To reduce the view back to normal, click **Show active and static leases only**.

## Clear DHCP Leases

The **Clear all DHCPv6 leases** button stops the DHCPv6 daemon, removes the entire lease database, and then starts the daemon again.

This does not remove static DHCPv6 mappings, only dynamic leases.

## High Availability Status – Kea DHCP Only

Failover status for Kea DHCP is in a section at the bottom of the DHCP and DHCPv6 Leases pages. The failover status works identically for both DHCP and DHCPv6, so refer to High Availability Status – Kea DHCP Only for details on how the failover status operates.
