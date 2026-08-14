---
source_url: https://docs.netgate.com/pfsense/en/latest/services/dns/forwarder-overrides.html
title: Host Overrides | pfSense Documentation
category: pfsense-dns
priority: 2
pfsense_version_notes: Host Overrides / Domain Overrides (DNS Forwarder)
fetched_date: 2026-08-13
converter: bs4+html2text
---

# Host Overrides¶

Host override entries provide a means to configure customized DNS entries. The configuration is identical to [Host Overrides](resolver-host-overrides.html#dns-host-overrides) in the DNS Resolver, refer there for details. The main difference is that overrides in the DNS Forwarder can only contain a single address per entry.

# Domain Overrides¶

Domain overrides configure an alternate DNS server to use for resolving a specific domain. The configuration is similar to [Domain Overrides](resolver-domain-overrides.html#dns-domain-overrides) in the DNS Resolver, but there are a few differences:

IP Address:
    

This field can be used in one of three ways to control how the DNS Forwarder handles queries for the given **Domain** :

  * To specify the IP Address of a DNS server to which the DNS Forwarder will send queries for hostnames in the **Domain**.

  * To override another entry by entering `#`.

For example, to forward `example.com` to `192.2.66.2`, but have `lab.example.com` forward on to the standard name servers, enter a `#` in this field.

  * To prevent non-local lookups by entering a `!`.

If host override entries exist for `www.example.org` and `mail.example.org`, but other lookups for hosts under example.org must not be forwarded on to remote DNS servers, enter a `!` in this field.



Source IP:
    

The source IP address that the DNS Forwarder will use when sending queries to the DNS server in this domain override.

This field is optional and primarily used to contact a DNS server across a VPN where the VPN requires queries to have a specific source.
