---
source_url: https://docs.netgate.com/pfsense/en/latest/services/dhcp/relay.html
title: DHCPv4 & DHCPv6 Relay
category: pfsense-core
priority: 1
pfsense_version_notes:
fetched_date: 2026-08-13
converter: webfetch
---

# DHCPv4 & DHCPv6 Relay

DHCP requests are broadcast traffic. Broadcast traffic is limited to the broadcast domain where it is initiated. To provide DHCP service on a network segment without a DHCP server, use the DHCP relay to forward those requests to a defined server on another segment.

Warning

It is not possible to run both a DHCP server and a DHCP Relay at the same time. To enable the DHCP relay, first disable the DHCP server on all interfaces.

## DHCP Relay Options

The DHCP Relay service has the following options:

Enable DHCP Relay:

*Checked* to enable the service.

Downstream Interfaces:

Select one or more local interfaces containing clients for which the service will relay requests.

CARP Status VIP:

A CARP type VIP which will be used to indicate whether the relay service will be started or stopped based on its status. For example, in an HA cluster, the service will only run when the chosen VIP is in CARP MASTER status, not when it is in BACKUP status. This ensures the HA nodes do not send conflicting relay messages.

Append circuit ID and agent ID to requests:

Check this to add a circuit ID (interface number on the firewall) and the agent ID to the DHCP request. This may be required by the DHCP server on the other side, and can help distinguish where the requests originated.

Upstream Servers:

A list of target DHCP server(s). If there is more than one upstream server, click **Add** to create more entries.

## DHCP Relay Configuration

To configure the DHCP Relay:

-   Disable the DHCP Server on each interface where the Relay will run
-   Navigate to **Services > DHCP Relay**
-   Click the tab for the interface to use with DHCP Relay
-   Configure the options as described in [DHCP Relay Options](#dhcp-relay-options).
-   Click **Save**

The DHCPv6 Relay function works identically to the DHCP Relay function for IPv4.
