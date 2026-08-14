---
source_url: https://docs.netgate.com/pfsense/en/latest/services/dns/wildcards.html
title: Creating Wildcard Records in DNS Forwarder/Resolver | pfSense Documentation
category: pfsense-dns
priority: 3
pfsense_version_notes: 
fetched_date: 2026-08-13
converter: bs4+html2text
---

# Creating Wildcard Records in DNS Forwarder/Resolver¶

A wildcard DNS record resolves `<anything>.example.com` to a single IP address, which can be useful in certain cases.

## DNS Resolver (Unbound)¶

To create a wildcard entry the DNS Resolver (Unbound), use the following directives in the custom options box:
    
    
    server:
    local-zone: "example.com" redirect
    local-data: "example.com 86400 IN A 192.168.1.54"
    

That makes any host under `example.com` resolve to `192.168.1.54`. For example, `www.example.com`, `thissitedoesnotexist.example.com`, `mystuff.example.com`, and so on.

If there are existing **Host Override** or **Domain Override** entries for the same domain, these custom options may not function as expected. When overrides are present, the zone will already be defined but with a different zone type set. For domains associated with host overrides, the default behavior of the local zones can be altered with the **System Domain Local Zone Type** setting in the [DNS Resolver Configuration](resolver-config.html).

## DNS Forwarder (dnsmasq)¶

To create a wildcard entry in the DNS Forwarder, use the following directives in the advanced options:
    
    
    address=/example.com/192.168.1.54
    

If a specific host override is set for example:
    
    
    specific.example.com 192.168.1.100
    knownhost.example.com 192.168.1.101
    

Then those would be returned when doing a query for those hosts, only when no specific host has been specified in the host overrides would the advanced wildcard entry be used.

To resolve the domain to an IP address:
    
    
    example.com 192.168.1.45
    

Leave the host field blank in the host overrides. So if the query is now for `example.com` the forwarder will return `192.168.1.45`. If a client requests `knownhost.example.com` then `192.168.1.101` would be returned instead.

If a blank hostname `example.com` host override entry has not been created, then a query for `example.com` would return the wildcard IP address set in the advanced option.

If a client queries for `madeupname.example.com` then since no specific host record for `madeupname` exists in the host overrides. The forwarder will return the wildcard entry of `192.168.1.54`.
