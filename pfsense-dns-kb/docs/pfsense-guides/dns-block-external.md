---
source_url: https://docs.netgate.com/pfsense/en/latest/recipes/dns-block-external.html
title: Blocking External Client DNS Queries | pfSense Documentation
category: pfsense-guides
priority: 2
pfsense_version_notes: 
fetched_date: 2026-08-13
converter: bs4+html2text
---

# Blocking External Client DNS Queries¶

This procedure configures the firewall to block DNS requests from local clients to servers outside the local network. With no other accessible DNS servers, clients are forced to send DNS requests to the DNS Resolver or DNS Forwarder on pfSense® software for resolution.

Note

Blocking is effective but does not gracefully handle the situation. Clients must manually adjust their configuration to use the firewall for DNS. Redirecting DNS requests to the firewall is a more seamless solution. See [Redirecting Client DNS Requests](dns-redirect.html) for details.

  * Navigate to **Firewall > Rules**, **LAN** tab

  * Create the block rule as the first rule in the list:

    * Click ![fa-turn-up](../_images/fa-turn-up.png) **Add** to create a new rule at the top of the list

    * Fill in the following fields on the rule:

Action:
    

_Reject_

Interface:
    

_LAN_

Protocol:
    

_TCP/UDP_

Destination:
    

_Any_

Destination Port Range:
    

_DNS (53)_

Description:
    

`Block DNS to Everything Else`

  * Create the pass rule to allow DNS to the firewall, above the block rule:

    * Click ![fa-turn-up](../_images/fa-turn-up.png) **Add** to create a new rule at the top of the list

    * Fill in the following fields on the rule:

Action:
    

_Pass_

Interface:
    

_LAN_

Protocol:
    

_TCP/UDP_

Destination:
    

_LAN Address_

Destination Port Range:
    

_DNS (53)_

Description:
    

`Pass DNS to the Firewall`

  * Click ![fa-check](../_images/fa-check.png) **Apply Changes** to reload the ruleset




When complete, there will be two rule entries that look like the following picture:

![../_images/blockdns.png](../_images/blockdns.png)

Certain local PCs could be allowed to use other DNS servers by placing a pass rule for them above the block rule.

## DNS over TLS¶

Another concern is that clients could use DNS over TLS to resolve hosts. DNS over TLS sends DNS requests over an encrypted channel on an alternate port, `853`.

This traffic can be blocked with a firewall rule for port `853` using the same procedure used for `53`. Though if the firewall will not be providing DNS over TLS service to clients, do not add the pass rule.

## DNS over HTTPS¶

Similar to DNS over TLS, clients may also use DNS over HTTPS (DoH). This is harder to block as it uses port `443`. Blocking port `443` on common public DNS servers may help (e.g. `1.1.1.1`, `8.8.8.8`).

Some browsers automatically attempt to use DNS over HTTPS because they believe it to be more secure and better for privacy, though that is not always the case. Each browser may have its own methods of disabling this feature. Firefox uses a “canary” domain `use-application-dns.net` by default if the user has not manually enabled DNS over HTTPS. If Firefox cannot resolve this name, Firefox disables DNS over HTTPS.

To prevent Firefox from using DNS over HTTPS, add the following to the DNS Resolver custom options:
    
    
    server:
    local-zone: "use-application-dns.net" always_nxdomain
    
