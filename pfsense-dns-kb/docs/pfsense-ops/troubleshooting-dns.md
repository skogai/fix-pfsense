---
source_url: https://docs.netgate.com/pfsense/en/latest/troubleshooting/dns.html
title: Troubleshooting DNS Resolution Issues | pfSense Documentation
category: pfsense-ops
priority: 2
pfsense_version_notes: 
fetched_date: 2026-08-13
converter: bs4+html2text
---

# Troubleshooting DNS Resolution Issues¶

Working DNS resolution is critical for functional access to the Internet.

## Test connectivity¶

Before diagnosing DNS issues with pfSense® software specifically, start with [Troubleshooting Network Connectivity](connectivity.html) to ensure the firewall has a proper networking configuration and working connectivity. Specifically, ensure the firewall can reach hosts on the Internet by IP address and that clients can reach the both the firewall and hosts on the Internet by IP address.

## Check DNS service¶

First check which DNS service is enabled on the firewall and how it is configured.

The default configuration uses the [DNS Resolver](../services/dns/resolver.html) in resolver mode ([DNS Resolver Mode](../services/dns/resolver-modes.html)). This mode does not require specific [DNS Servers](../config/general.html#general-dns-servers), it queries the root DNS servers and other authoritative servers directly ([DNS Resolution Process](../services/dns/resolution-process.html)).

Installations upgraded from versions before the DNS Resolver became the default may be using the [DNS Forwarder](../services/dns/forwarder.html), which requires [DNS Servers](../config/general.html#general-dns-servers) to be entered under **System > General Setup** or to be acquired from a dynamic WAN such as DHCP or PPPoE. The DNS Resolver can also operate in this manner if set to forwarding mode.

Whichever service is active, check if it is running under **Status > Services**.

If the DNS Resolver is active, but the firewall is unable to resolve hostnames, the problem is usually a lack of working WAN connectivity. Aside from that, one possibility is that the WAN or upstream network gear does not properly pass DNS traffic in a way that is compatible with DNSSEC. Disable DNSSEC in the [DNS Resolver Configuration](../services/dns/resolver-config.html) to see resolution functions without DNSSEC. It is also possible that the ISP filters or rate limits DNS requests and/or requires the use of specific DNS servers. In that case, configure [DNS Servers](../config/general.html#general-dns-servers) and then activate forwarding mode in the [DNS Resolver Configuration](../services/dns/resolver-config.html).

## Check DNS Servers¶

If the DNS Resolver is in forwarding mode, or the DNS Forwarder is active, then check if the firewall has DNS servers defined and ensure it can reach its DNS servers.

The firewall [DNS Server Settings](../config/general.html#general-dns-settings) are under **System > General Setup**, and DNS servers obtained from dynamic WANs are also visible at **Status > Interfaces**. The best practice is to define at least two DNS servers. If there are multiple WANs, there should be at least one DNS server per WAN with an appropriate gateway set ([Interface and DNS Configuration](../multiwan/interfaces-and-dns.html#multiwan-dns)).

Perform a [Ping](../diagnostics/ping.html) test to check if the firewall can reach the DNS servers.

Note

Not all DNS servers respond to ICMP ping requests, so a failure here does not necessarily indicate a problem. Proceed to the next test to check if they respond to a DNS query.

## Check Firewall DNS¶

Perform a [DNS Lookup](../diagnostics/dns.html) test to check if the firewall can resolve a hostname. The page will report the results of the query, which servers responded, and how fast they responded.

If using the DNS Resolver in resolver mode without DNS servers configured, then only `127.0.0.1` may be listed. So long as the query received the expected response, that is normal. If no response was received, ensure the DNS Resolver service is running. If it is running, disable DNSSEC and try again, or try forwarding mode. If either of those work, then the ISP may be restricting or redirecting DNS queries.

If DNS Servers are configured on the firewall or obtained from dynamic WANs, the DNS lookup page lists them and whether they responded.

If using the DNS Resolver in forwarding mode or the DNS Forwarder, the individual DNS server responses are important. If any of the servers did not respond, investigate them and potentially replace them with working servers.

If none of the servers respond, check the WAN connectivity ([Troubleshooting Network Connectivity](connectivity.html)) and double-check the DNS server IP addresses. If the firewall can reach the gateway address at the ISP, but not the DNS servers, double-check the server IP addresses. If the DNS servers are obtained via DHCP or PPPoE and the firewall cannot reach them, contact the ISP. If all else fails, consider using a public DNS service such as Google public DNS, Quad9, or CloudFlare on the firewall instead of the DNS servers provided by the ISP. If those are already in use, The ISP may be restricting DNS queries so the only choice may be to use the ISP DNS servers.

## Check Client DNS¶

If DNS works from the firewall but not from a client PC, it could be the DNS Resolver or Forwarder configuration on the firewall, the client configuration, or firewall rules.

Out of the box, the DNS Resolver handles DNS queries for clients behind the firewall. Older upgraded configurations may have the DNS Forwarder active in the same capacity.

If the client PCs are configured with DHCP, they will receive the IP address of the firewall interface to which they are connected as a DNS server, unless that is manually changed. For example, if a PC is on the LAN interface, and the firewall LAN IP address is `192.168.1.1`, then the client DNS server should also be `192.168.1.1`.

If the DNS Resolver and DNS Forwarder are disabled, adjust the DNS servers which get assigned to DHCP clients under **Services > DHCP Server**. Normally when the DNS Resolver and DNS Forwarder are disabled, the system DNS servers are assigned directly to the clients, but if that is not the case in practice for this setup, define them in the DHCP settings. If the client PC is not configured for DHCP, be sure it has the proper DNS servers set in its local configuration. This could be the LAN IP address of the firewall or an alternate set of working internal or external DNS servers.

Another possibility for DNS working from the firewall but not a local client is an overly strict firewall rule on the LAN. Check **Status > System Logs**, on the **Firewall** tab. If blocked connections appear in the log from the local client trying to reach a DNS server, then add a firewall rule at the top of the LAN rules for that interface which will allow connections to the DNS servers on **TCP and UDP** port `53`. If the client uses DNS over TLS, allow port `853` as well.
