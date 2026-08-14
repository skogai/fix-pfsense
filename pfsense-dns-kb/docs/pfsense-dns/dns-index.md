---
source_url: https://docs.netgate.com/pfsense/en/latest/services/dns/index.html
title: DNS | pfSense Documentation
category: pfsense-dns
priority: 1
pfsense_version_notes: 
fetched_date: 2026-08-13
converter: bs4+html2text
---

# DNS¶

DNS, or Domain Name System, is the mechanism by which a network device resolves a name like `www.example.com` to an IP address such as `198.51.100.25`, or vice versa. Clients must have functional DNS if they are to reach other devices such as servers using their hostnames or fully qualified domain names.

## DNS Resolver/Forwarder¶

These topics cover using pfSense® software to handle DNS requests from local clients as either a caching DNS resolver or forwarder. When acting as a resolver or forwarder, pfSense software will perform DNS resolution directly or hand off queries to an upstream DNS forwarding server.

  * [DNS Resolution Process](resolution-process.html)
  * [DNS Resolver](resolver.html)
  * [DNS Forwarder](forwarder.html)
  * [DNS Rebinding Protections](rebinding.html)
  * [Creating Wildcard Records in DNS Forwarder/Resolver](wildcards.html)



See also

  * [DNS Lookup](../../diagnostics/dns.html)

  * [Interface and DNS Configuration](../../multiwan/interfaces-and-dns.html)

  * [Troubleshooting DNS Resolution Issues](../../troubleshooting/dns.html)

  * [Troubleshooting the DNS Cache](../../troubleshooting/dns-cache.html)

  * [Troubleshooting DNS Queries](../../troubleshooting/dns-queries.html)




## DNS Guides¶

How to perform various tasks related to DNS.

  * [Configuring DNS over TLS](../../recipes/dns-over-tls.html)

  * [Blocking External Client DNS Queries](../../recipes/dns-block-external.html)

  * [Redirecting Client DNS Requests](../../recipes/dns-redirect.html)




## Dynamic DNS¶

[Dynamic DNS](../dyndns/index.html) updates an external DNS server with an interface IP address when it changes. This enables a firewall with a dynamic WAN such as DHCP or PPPoE to host public services even when its IP address changes periodically.
