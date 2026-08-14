---
source_url: https://docs.netgate.com/pfsense/en/latest/multiwan/interfaces-and-dns.html
title: Interface and DNS Configuration | pfSense Documentation
category: pfsense-ops
priority: 2
pfsense_version_notes: 
fetched_date: 2026-08-13
converter: bs4+html2text
---

# Interface and DNS Configuration¶

The first two items to configure for Multi-WAN are interfaces and DNS.

## Interface Configuration¶

Set up the primary WAN as previously described in [Setup Wizard](../config/setup-wizard.html). Then for the additional WAN interfaces, perform the following tasks:

  * Assign the interfaces if they do not yet exist

  * Visit the **Interfaces** menu entry for each additional WAN (e.g. **Interfaces > OPT1**)

  * Enable the interface

  * Enter a suitable name, such as `WAN2`

  * Select the desired type of IP address configuration depending on the Internet connection type.

  * Enter the remaining details for the type of WAN. For example, on static IP connections, fill in the IP address, subnet mask, and add or select a gateway.




## DNS Configuration¶

DNS is critical for Internet connectivity. For multi-WAN to function correctly the firewall must always be able to resolve DNS for itself and on behalf of local clients utilizing the DNS Resolver or DNS Forwarder.

When the firewall configuration only includes DNS servers from a single WAN, an outage of that WAN results in a complete Internet outage since DNS will no longer function.

To ensure DNS resolution uses multiple WANs, consult one of the following sections:

Resolver Mode:
    

If the DNS Resolver is in resolver mode, see DNS Resolver and Multi-WAN.

Forwarding Mode:
    

If the DNS Resolver is set for **forwarding** mode, or if the DNS Forwarder is in use, then the firewall must be configured with DNS servers for each WAN as described in DNS Forwarding and Static Routes.

### DNS Resolver and Multi-WAN¶

The DNS Resolver can work with multi-WAN, but the exact configuration depends on the desired behavior and current settings, especially the chosen [DNS Resolver mode](../services/dns/resolver-modes.html).

If the DNS Resolver is using its default resolver mode, such as for environments which require DNSSEC, then it can still function with multi-WAN but requires using failover for the default gateway. See [Managing the Default Gateway](../routing/gateways.html#routing-gateways-manage-default).

Even in resolver mode if the firewall is set to use or fall back to remote DNS servers under **System > General**, **DNS Resolution Behavior** , then it is still useful to configure gateways for individual DNS servers as described in DNS Forwarding and Static Routes

### DNS Forwarding and Static Routes¶

When using the DNS Resolver in forwarding mode or the DNS Forwarder, the firewall uses its routing table to reach the configured DNS servers. This means without any static routes configured, it will only use the WAN with the default gateway to reach DNS servers.

Gateways must be selected for each DNS server defined on the firewall. This forces the firewall to use a specific WAN interface to reach a given DNS server. At least one gateway from each WAN should be selected where possible.

Note

Most ISPs prohibit recursive queries from hosts outside their network, hence the firewall must use the correct WAN interface when accessing DNS servers for a specific ISP.

DNS servers obtained from a dynamic WAN are automatically routed back out the appropriate dynamic WAN.

To configure DNS server gateways:

  * Navigate to **System > General Setup**

  * Define at least one _unique_ DNS server for each WAN

  * Select an appropriate gateway for each DNS server so it uses a specific WAN

Note

If the gateway entries for these WANs use DNS servers for their monitor IP addresses, ensure there is no conflict between those values and the selected gateways in this list.




Note

Each entry must be unique; the same DNS server cannot be entered more than once.

If using the DNS Resolver, ensure it is set for forwarding mode:

  * Navigate to **Services > DNS Resolver**

  * Check **Enable Forwarding Mode**

  * Uncheck **Enable DNSSEC Support**

  * Click **Save** , then **Apply Changes**



