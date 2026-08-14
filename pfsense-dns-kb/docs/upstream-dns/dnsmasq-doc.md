---
source_url: https://thekelleys.org.uk/dnsmasq/doc.html
title: Dnsmasq - network services for small networks.
category: upstream-dns
priority: 2
pfsense_version_notes: dnsmasq (DNS Forwarder) overview
fetched_date: 2026-08-13
converter: bs4+html2text
---

![](http://www.thekelleys.org.uk/dnsmasq/images/icon.png) | 

# Dnsmasq

| ![](http://www.thekelleys.org.uk/dnsmasq/images/icon.png)  
---|---|---  
Dnsmasq provides network infrastructure for small networks: DNS, DHCP, router advertisement and network boot. It is designed to be lightweight and have a small footprint, suitable for resource constrained routers and firewalls. It has also been widely used for tethering on smartphones and portable hotspots, and to support virtual networking in virtualisation frameworks. Supported platforms include Linux (with glibc and uclibc), Android, *BSD, and Mac OS X. Dnsmasq is included in most Linux distributions and the ports systems of FreeBSD, OpenBSD and NetBSD. Dnsmasq provides full IPv6 support. 

The DNS subsystem provides a local DNS server for the network, with forwarding of all query types to upstream recursive DNS servers and caching of common record types (A, AAAA, CNAME and PTR, also DNSKEY and DS when DNSSEC is enabled). 
* Local DNS names can be defined by reading /etc/hosts, by importing names from the DHCP subsystem, or by configuration of a wide range of useful record types.
* Upstream servers can be configured in a variety of convenient ways, including dynamic configuration as these change on moving upstream network. 
* Authoritative DNS mode allows local DNS names may be exported to zone in the global DNS. Dnsmasq acts as authoritative server for this zone, and also provides zone transfer to secondaries for the zone, if required.
* DNSSEC validation may be performed on DNS replies from upstream nameservers, providing security against spoofing and cache poisoning.
* Specified sub-domains can be directed to their own upstream DNS servers, making VPN configuration easy.
* Internationalised domain names are supported. 

The DHCP subsystem supports DHCPv4, DHCPv6, BOOTP and PXE. 
* Both static and dynamic DHCP leases are supported, along with stateless mode in DHCPv6.
* The PXE system is a full PXE server, supporting netboot menus and multiple architecture support. It includes proxy-mode, where the PXE system co-operates with another DHCP server.
* There is a built in read-only TFTP server to support netboot.
* Machines which are configured by DHCP have their names automatically included in the DNS and the names can specified by each machine or centrally by associating a name with a MAC address or UID in the dnsmasq configuration file.

The Router Advertisement subsystem provides basic autoconfiguration for IPv6 hosts. It can be used stand-alone or in conjunction with DHCPv6. 
* The M and O bits are configurable, to control hosts' use of DHCPv6.
* Router advertisements can include the RDNSS option.
* There is a mode which uses name information from DHCPv4 configuration to provide DNS entries for autoconfigured IPv6 addresses which would otherwise be anonymous.

For extra compactness, unused features may be omitted at compile time. 

## Get code.

[Download](http://www.thekelleys.org.uk/dnsmasq/) dnsmasq here. The tarball includes this documentation, source, and [manpage](docs/dnsmasq-man.html). There is also a [ CHANGELOG](CHANGELOG) and a [FAQ](docs/FAQ). Dnsmasq has a git repository which contains the complete release history of version 2 and development history from 2.60. You can [browse](http://thekelleys.org.uk/gitweb/?p=dnsmasq.git;a=summary) the repo, or get a copy using git protocol with the command 
    
    
    git clone git://thekelleys.org.uk/dnsmasq.git 

or 
    
    
    git clone http://thekelleys.org.uk/git/dnsmasq.git 

## License.

Dnsmasq is distributed under the GPL, version 2 or version 3 at your discretion. See the files COPYING and COPYING-v3 in the distribution for details. 

## Contact.

There is a dnsmasq mailing list at [ http://lists.thekelleys.org.uk/mailman/listinfo/dnsmasq-discuss](http://lists.thekelleys.org.uk/mailman/listinfo/dnsmasq-discuss) which should be the first location for queries, bugreports, suggestions etc. The list is mirrored, with a search facility, at [ https://www.mail-archive.com/dnsmasq-discuss@lists.thekelleys.org.uk/](https://www.mail-archive.com/dnsmasq-discuss@lists.thekelleys.org.uk/). You can contact me at [simon@thekelleys.org.uk](mailto:simon@thekelleys.org.uk). 

## Donations.

Dnsmasq is mainly written and maintained by Simon Kelley. For most of its life, dnsmasq has been a spare-time project. These days I'm working on it as my main activity. I don't have an employer or anyone who pays me regularly to work on dnsmasq. If you'd like to make a contribution towards my expenses, please use the donation button below.  ![](https://www.paypalobjects.com/en_GB/i/scr/pixel.gif)
