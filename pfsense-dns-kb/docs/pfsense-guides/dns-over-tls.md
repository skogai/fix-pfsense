---
source_url: https://docs.netgate.com/pfsense/en/latest/recipes/dns-over-tls.html
title: Configuring DNS over TLS | pfSense Documentation
category: pfsense-guides
priority: 1
pfsense_version_notes: DNS over TLS is Resolver-only; DNSSEC off in forwarding mode
fetched_date: 2026-08-13
converter: bs4+html2text
---

# Configuring DNS over TLS¶

Several popular public DNS providers provide encrypted DNS service using DNS over TLS. This prevents intermediate parties from viewing the content of DNS queries and can also assure that DNS is being provided by the expected DNS servers.

## Requirements¶

This feature is only implemented in the [DNS Resolver](../services/dns/resolver.html). If the firewall is currently using the [DNS Forwarder](../services/dns/forwarder.html), convert to the DNS Resolver before starting this procedure.

Pick a DNS over TLS upstream provider, such as a private upstream DNS server or a public service like Cloudflare, Quad9, or Google public DNS. Note the addresses of the servers and their associated hostnames.

## Configure DNS Servers¶

First, configure the DNS servers on the firewall.

Warning

When the firewall uses DNS over TLS, **every** DNS server the firewall uses **must** provide DNS over TLS service.

  * Navigate to **System > General**

  * Locate the **DNS Server Settings** Section

  * Add or replace entries in the **DNS Servers** section such that only the chosen DNS over TLS servers are in the list

Address:
    

IP address of an upstream DNS Server providing DNS over TLS service (e.g. `1.1.1.1`).

Hostname:
    

Hostname of the same upstream DNS Server in the **Address** field, used for TLS certificate validation (e.g. `cloudflare-dns.com`).

Warning

The hostname is technically optional but dangerous to omit. The DNS Resolver must have the hostname to validate that the correct server is providing a given response. The response is still encrypted without the hostname, but the DNS Resolver has no way to validate the response to determine if the query was intercepted and answered by a third party server (Man-in-the-Middle attack).

  * Click ![fa-plus](../_images/fa-plus.png) **Add DNS Server** and repeat the previous step as needed for each available DNS server

  * Uncheck **Allow DNS server list to be overridden by DHCP/PPP on WAN**

DNS servers obtained dynamically may not provide DNS over TLS.

  * Set **DNS Resolution Behavior** to _Use local DNS (127.0.0.1), ignore remote DNS Servers_

This makes the firewall itself use only the DNS Resolver, and it will not attempt to contact the DNS servers directly. This prevents DNS requests from the firewall being leaked unencrypted on port `53` if the resolver is temporarily unavailable ([DNS Resolution Behavior](../config/general.html#general-dns-resolution)).

  * Click **Save**




Use Example DNS Server list for DNS over TLS from Cloudflare as a reference for the settings on the page.

![../_images/dot-servers.png](../_images/dot-servers.png)

Example DNS Server list for DNS over TLS from Cloudflare¶

## Enable DNS over TLS for Forwarded Queries¶

Next, configure the DNS Resolver to use DNS over TLS for outgoing queries.

  * Navigate to **Services > DNS Resolver**

  * Uncheck **Enable DNSSEC Support**

Note

DNSSEC is not generally compatible with forwarding mode, with or without DNS over TLS.

  * Check **Enable Forwarding Mode**

  * Check **Use SSL/TLS for outgoing DNS Queries to Forwarding Servers**

  * Click **Save**

  * Click **Apply Changes**




Use Example DNS Resolver configuration for outgoing DNS over TLS as a reference for the settings on the page.

![../_images/dot-settings.png](../_images/dot-settings.png)

Example DNS Resolver configuration for outgoing DNS over TLS¶

The DNS Resolver will now send queries to all upstream forwarding DNS servers using SSL/TLS on the default port of `853`.

## Testing DNS over TLS¶

There are several ways to validate that outbound queries are using DNS over TLS.

  * Test via **Diagnostics > DNS Lookup** ([DNS Lookup](../diagnostics/dns.html)) and ensure the results from `127.0.0.1` are correct.

  * Check for states using port `853` going to the DNS servers in the configuration ([Firewall States](../monitoring/status/firewall-states.html)) like those in Example State Table contents for DNS over TLS queries.

  * Packet capture port `853` ([Packet Capturing](../diagnostics/packetcapture/index.html)) and inspect the capture in Wireshark. The contents of the query are not visible, but the TLS exchange is, and any TLS errors in negotiation should be visible in the capture.


![../_images/dot-states.png](../_images/dot-states.png)

Example State Table contents for DNS over TLS queries¶

## Enable DNS over TLS Server (optional)¶

The DNS Resolver can also act as a DNS over TLS server, though this function **does not** affect outbound/forwarded queries, so this section is optional.

Enable this feature only when _local clients_ may need to communicate with the _DNS Resolver_ using DNS over TLS queries.

  * Navigate to **Services > DNS Resolver**

  * Check **Respond to incoming SSL/TLS queries from local clients**

  * Select a valid server certificate in **SSL/TLS Certificate**

Note

Clients may reject this certificate if it is self-signed, consider using a certificate from [ACME](../packages/acme/index.html).

  * Leave **SSL/TLS Listen Port** at the default (empty or `853`)

  * Click **Save**

  * Click **Apply Changes**




Use Example DNS Resolver configuration for acting as a DNS over TLS Server as a reference for the settings on the page.

Now the DNS Resolver will listen for DNS over TLS queries from local clients on TCP port `853`.

![../_images/dot-service.png](../_images/dot-service.png)

Example DNS Resolver configuration for acting as a DNS over TLS Server¶

## Caveats¶

Clients can make their own connections to DNS over TLS servers, so block them on TCP/UDP ports `53` and `853` to ensure they only query the DNS Resolver ([Blocking External Client DNS Queries](dns-block-external.html)).

Redirecting DNS over TLS queries to the DNS Resolver may or may not work, depending on the clients. Set up the DNS over TLS server and add port forward redirects for TCP/UDP ports `53` and `853` to redirect DNS queries to the firewall ([Redirecting Client DNS Requests](dns-redirect.html)).

Note

Though clients may reject the DNS over TLS server certificate since it would not match their intended server, this could still have the intended result. The client may fall back to traditional DNS queries if DNS over TLS validation fails.
