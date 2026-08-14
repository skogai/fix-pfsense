---
source_url: https://docs.netgate.com/pfsense/en/latest/diagnostics/dns.html
title: DNS Lookup | pfSense Documentation
category: pfsense-ops
priority: 3
pfsense_version_notes: 
fetched_date: 2026-08-13
converter: bs4+html2text
---

# DNS Lookup¶

**Diagnostics > DNS Lookup** performs simple forward and reverse DNS queries. These queries obtain information about an IP address or hostname and also test the DNS servers configured on the firewall ([DNS Server Settings](../config/general.html#general-dns-settings)).

To perform a DNS Lookup:

  * Navigate to **Diagnostics > DNS Lookup**

  * Enter a **Hostname** or IP address to query

  * Click ![fa-search](../_images/fa-search.png) **Lookup**




The page displays the results of the DNS query along with timing information and options.

## DNS servers included in testing¶

The page will query a specific set of DNS servers. This set depends upon the [DNS Server Settings](../config/general.html#general-dns-settings) under **System > General**.

The page will test against `127.0.0.1` if the DNS Resolver or DNS Forwarder are active and the [DNS Resolution Behavior](../config/general.html#general-dns-resolution) setting is not set to ignore local DNS.

The page will test each of the [DNS Servers](../config/general.html#general-dns-servers) from the list at **System > General**.

The page will also test DNS servers from dynamic WANs if **DNS Server Override** is set and the firewall has obtained servers from dynamic sources.

Note

The [DNS Resolver mode](../services/dns/resolver-modes.html) does not impact the behavior of this test. Even in resolver mode the individual DNS servers are tested as described above.

## Results¶

The **Results** panel contains addresses returned by the DNS query along with the record type.

Underneath the results is a table containing the resolution **Timings** per server. This shows how fast each of the configured DNS servers responded to the specified query, or if they never responded.

The **More Information** panel contains links to ping and traceroute functions on the firewall for this host.

## Aliases¶

The GUI can also create a [firewall alias](../firewall/aliases.html) from the results of the DNS Lookup query.

Click ![fa-plus](../_images/fa-plus.png) **Add alias** to create an alias containing the results of the query.

The name of the alias is the text entered for the DNS query but with `.` characters replaced by `_`. For example, a DNS lookup for `example.com` results in an alias named `example_com`.

If an alias already exists with that name, the button is labeled **Update Alias** instead. That version of the button will replace the contents of the existing alias with the current results of the DNS lookup.
