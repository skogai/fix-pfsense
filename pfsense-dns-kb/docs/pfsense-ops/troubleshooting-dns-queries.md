---
source_url: https://docs.netgate.com/pfsense/en/latest/troubleshooting/dns-queries.html
title: Troubleshooting DNS Queries | pfSense Documentation
category: pfsense-ops
priority: 3
pfsense_version_notes: 
fetched_date: 2026-08-13
converter: bs4+html2text
---

# Troubleshooting DNS Queries¶

An administrator may need to troubleshoot issues with certain queries to the DNS Resolver (Unbound) or DNS Forwarder (dnsmasq). In such cases it can be helpful to view the queries received by the firewall and to see the responses generated.

For the DNS Resolver this can be accomplished by adding the following keyword to the **Custom Options** box on a new line:
    
    
    server:
    log-queries: yes
    

For the DNS Forwarder, add this line to the **Advanced Options** box:
    
    
    log-queries
    

When saved, the DNS Resolver or Forwarder will begin logging the received queries and their replies, along with information about the result. The messages vary depending on the daemon. The DNS Forwarder logs whether an answer was pulled from the cache, but the DNS Resolver does not log extra data for queries answered from the cache.

Here are some examples of exchanges that might find in the query log:

A query using the DNS Resolver in forwarding mode to a system DNS server using DNS over TLS (not answered from the cache):
    
    
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] info: 192.168.1.100 daisy.ubuntu.com. A IN
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] debug: validator[module 0] operate: extstate:module_state_initial event:module_event_new
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] info: validator operate: query daisy.ubuntu.com. A IN
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] debug: iterator[module 1] operate: extstate:module_state_initial event:module_event_pass
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] info: resolving daisy.ubuntu.com. A IN
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] info: processQueryTargets: daisy.ubuntu.com. A IN
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] info: sending query: daisy.ubuntu.com. A IN
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] debug: sending to target: <.> 9.9.9.9#853
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] debug: cache memory msg=16528 rrset=16528 infra=3485 val=16644
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] debug: iterator[module 1] operate: extstate:module_wait_reply event:module_event_reply
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] info: iterator operate: query daisy.ubuntu.com. A IN
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] info: response for daisy.ubuntu.com. A IN
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] info: reply from <.> 9.9.9.9#853
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] info: query response was ANSWER
    Oct  5 15:16:46 fw1 unbound[96103]: [96103:0] info: finishing processing for daisy.ubuntu.com. A IN
    

A query to the DNS Forwarder where the response was given from the DNS cache:
    
    
    Dec  3 08:56:46 dnsmasq[1068]: query[A] dnl-14.geo.kaspersky.com from 10.0.10.128
    Dec  3 08:56:46 dnsmasq[1068]: cached dnl-14.geo.kaspersky.com is 4.28.136.39
    

A cached negative response from the DNS Forwarder:
    
    
    Dec  3 08:56:49 dnsmasq[1068]: query[A] wpad.example.com from 192.0.2.5
    Dec  3 08:56:49 dnsmasq[1068]: cached wpad.example.com is NXDOMAIN-IPv4
    

A query to the DNS Forwarder where the reply cannot be sent because of an improper client IP address (subnet ID, invalid IP address):
    
    
    Dec  3 08:49:21 dnsmasq[1068]: query[A] teredo.ipv6.microsoft.com from 192.0.2.0
    Dec  3 08:49:21 dnsmasq[1068]: forwarded teredo.ipv6.microsoft.com to 8.8.8.8
    Dec  3 08:49:21 dnsmasq[1068]: forwarded teredo.ipv6.microsoft.com to 8.8.4.4
    Dec  3 08:49:21 dnsmasq[1068]: reply teredo.ipv6.microsoft.com.nsatc.net is 157.56.144.215
    Dec  3 08:49:21 dnsmasq[1068]: failed to send packet: Permission denied
    
