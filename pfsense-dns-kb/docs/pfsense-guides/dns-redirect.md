---
source_url: https://docs.netgate.com/pfsense/en/latest/recipes/dns-redirect.html
title: Redirecting Client DNS Requests | pfSense Documentation
category: pfsense-guides
priority: 2
pfsense_version_notes: 
fetched_date: 2026-08-13
converter: bs4+html2text
---

# Redirecting Client DNS Requests¶

To restrict client DNS to only the DNS Resolver or Forwarder on pfSense® software, use a port forward to capture all client DNS requests.

Note

Either The DNS Resolver or DNS Forwarder must be active, and it must bind to and answer queries on _Localhost_ , or _All_ interfaces.

See also

  * [Blocking External Client DNS Queries](dns-block-external.html#dns-block-external)

  * [Blocking Web Sites Using DNS](block-websites.html#blocksites-dns)




The following example uses the LAN interface, but the same technique will work with any local interface.

  * Navigate to **Firewall > NAT**, **Port Forward** tab

  * Click ![fa-turn-up](../_images/fa-turn-up.png) **Add** to create a new rule

  * Fill in the following fields on the port forward rule:

Interface:
    

_LAN_

Protocol:
    

_TCP/UDP_

Destination:
    

**Invert Match** _checked_ , _LAN Address_

Destination Port Range:
    

_DNS (53)_

Redirect Target IP:
    

`127.0.0.1`

Redirect Target Port:
    

_DNS (53)_

Description:
    

`Redirect DNS`

NAT Reflection:
    

_Disable_




When complete, the port forward must appear as follows:

![../_images/redirect_dns_port_forward.png](../_images/redirect_dns_port_forward.png)

Note

If DNS requests to other DNS servers are blocked, such as by following [Blocking External Client DNS Queries](dns-block-external.html), ensure the rule to pass DNS to `127.0.0.1` is above any rule that blocks DNS.

With this port forward in place, DNS requests from local clients to **any** external IP address will result in the query being answered by the firewall itself. Access to other DNS servers on port 53 is impossible.

Tip

This can be adapted to allow access to only a specific set of DNS servers by changing the Destination network from “LAN Address” to an alias containing the allowed DNS servers. The **Invert match** box should remain checked.

Warning

Clients using DNS over TLS or DNS over HTTPS could circumvent this protection. Redirecting or blocking port `853` may help with DNS over TLS, depending on the clients.

See [Blocking External Client DNS Queries](dns-block-external.html) for additional advice.
