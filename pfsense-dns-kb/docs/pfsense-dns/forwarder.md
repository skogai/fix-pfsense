---
source_url: https://docs.netgate.com/pfsense/en/latest/services/dns/forwarder.html
title: DNS Forwarder | pfSense Documentation
category: pfsense-dns
priority: 1
pfsense_version_notes: DNS Forwarder = dnsmasq
fetched_date: 2026-08-13
converter: bs4+html2text
---

# DNS Forwarder¶

The DNS Forwarder in pfSense® software utilizes the `dnsmasq` daemon, which is a caching DNS forwarder.

Unlike the DNS Resolver, the DNS Forwarder can only act in a forwarding role. It is not capable of acting as a resolver.

The DNS Forwarder uses [DNS Servers](../../config/general.html#general-dns-servers) configured at **System > General Setup** and those obtained automatically from an ISP for dynamically configured WAN interfaces (DHCP, PPPoE, etc.).

See also

  * [DNS Resolution Process](resolution-process.html)

  * [DNS Rebinding Protections](rebinding.html)




Note

This service is disabled by default. The [DNS Resolver](resolver.html) (`unbound`) is the default DNS service.

The DNS Forwarder remains enabled on upgraded installations where it was active before the upgrade.

DNS Forwarder Configuration

  * [DNS Forwarder Configuration](forwarder-config.html)
  * [Host Overrides](forwarder-overrides.html)
  * [Domain Overrides](forwarder-overrides.html#domain-overrides)



## DNS Forwarder Behavior¶

By default, the DNS Forwarder queries all DNS servers at once, and it uses and caches only the first response it receives. This results in much faster DNS service from a client perspective, and can help smooth over problems that stem from DNS servers which are intermittently slow or have high latency, especially in Multi-WAN environments. This behavior can be disabled by activating the **Query DNS servers sequentially** option.

See also

  * [Interface and DNS Configuration](../../multiwan/interfaces-and-dns.html)



