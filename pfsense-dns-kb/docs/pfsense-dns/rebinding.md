---
source_url: https://docs.netgate.com/pfsense/en/latest/services/dns/rebinding.html
title: DNS Rebinding Protections | pfSense Documentation
category: pfsense-dns
priority: 2
pfsense_version_notes: 
fetched_date: 2026-08-13
converter: bs4+html2text
---

# DNS Rebinding Protections¶

pfSense® software includes built in methods of protection against [DNS rebinding attacks](https://en.wikipedia.org/wiki/DNS_rebinding).

A DNS rebinding attack is when someone with control over DNS responses for a domain feeds a client an address on the local network of the client – or even the client computer itself – as a response for a hostname in the domain controlled by the attacker. This would happen when the client requests a page in the malicious domain. Because the server run by the attacker and the hostname pointing to the client network are in the same domain from the perspective of the browser, the browser may allow scripts from the malicious server to run and access the other host. This can trigger the client to unintentionally exploit a device that would otherwise be unreachable from the Internet directly.

DNS rebinding attack protection is active by default. This behavior is controlled by the **DNS Rebind Check** option under **System > Advanced**, **Admin Access** tab.

## DNS protection¶

When active, this protection causes the DNS resolver and forwarder to strip addresses from DNS responses for local and private IP addresses which should not normally be received from public DNS servers.

Tip

This is the safest and best practice as responses to DNS queries made through _public_ DNS servers should never include _private_ IP addresses.

For a list of addresses including in this protection, see the following table:

Addresses included in DNS Rebinding Protection¶ Address | Description  
---|---  
127.0.0.0/8 | RFC 1122 Loopback Addresses (Localhost)  
10.0.0.0/8 | RFC 1918 Private Addresses  
::ffff:a00:0/104 | IPv6 Representation of 10.0.0.0/8  
172.16.0.0/12 | RFC 1918 Private Addresses  
::ffff:ac10:0/108 | IPv6 Representation of 172.16.0.0/12  
192.168.0.0/16 | RFC 1918 Private Addresses  
::ffff:a9fe:0/112 | IPv6 Representation of 192.168.0.0/16  
169.254.0.0/16 | RFC 3927 IPv4 Link Local Addresses  
::ffff:c0a8:0/112 | IPv6 Representation of 169.254.0.0/16  
fd00::/8 | RFC 4193 IPv6 Unique Local Unicast Addresses (ULA)  
fe80::/10 | RFC 4291 IPv6 Link Local Addresses  
  
There are some cases when public DNS servers give responses containing private IP addresses in replies. This may be the case for private internal hostnames under domains owned by an organization that does not use split DNS. It is also common in DNS-based block lists such as those for e-mail spam prevention (DNSBL, RBL, etc.). In these cases overrides can be set for individual domains. The exact method depends on which DNS service is active.

Note

This behavior is automatically overridden for domains in the DNS Resolver and DNS Forwarder domain override lists as the most common usage of that functionality is to resolve internal DNS hostnames.

### DNS Resolver¶

When DNS rebinding attack protection is active the [DNS Resolver](resolver.html) strips private addresses from DNS responses. Additionally, the DNSSEC validator may mark the answers as bogus. This is handled automatically using a list of `private-address` directives maintained by the firewall.

To exclude a domain from DNS rebinding protection, use the **Custom Options** box in the DNS resolver settings. Enter one domain per line in the following format, preceded by the `server:` line.
    
    
    server:
    private-domain: "example.com"
    private-domain: "dnsbl.example"
    

### DNS forwarder¶

The [DNS Forwarder](forwarder.html) uses the option `--stop-dns-rebind` by default, which rejects and logs addresses from upstream name servers which are in private address ranges.

To exclude a domain from DNS rebinding protection, use the DNS forwarder **Advanced Settings** box as follows:
    
    
    rebind-domain-ok=/example.com/
    rebind-domain-ok=/dnsbl.example/
    

Additionally, it is possible to exclude the loopback range (`127.0.0.0/8`) from protection using the DNS forwarder **Advanced Settings** box as follows:
    
    
    rebind-localhost-ok
    

Note

Rather than exclude the entire loopback range, it’s generally better to allow such responses on a per-domain basis instead.

## GUI protection¶

For those not using the DNS resolver or forwarder, and as an additional layer of checks, the GUI will block access attempts using unknown hostnames. In this case the GUI will deny access and display “Potential DNS Rebind Attack Detected”.

By default, the GUI only accepts the hostname and domain configured under **System > General Setup**. For instance if `firewall.example.com` is configured as the firewall hostname, and the GUI is loaded in a browser using `fw1.example.com`, the GUI will reject that attempt. Define additional hostnames under **System > Advanced**, **Admin Access** tab in the **Alternate Hostnames** field.

Tip

If a user encounters this error they can log into the GUI using the IP address of the firewall rather than the hostname.

If a client encounters this message when attempting to access a forwarded service (Port forward, 1:1 NAT, etc.) it indicates that the request did not match any NAT rules. From the inside of the network, this would require NAT reflection or split DNS to accomplish.

See also

[Accessing Port Forwards from Local Networks](../../recipes/port-forwards-from-local-networks.html)
