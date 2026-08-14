---
source_url: https://www.netgate.com/blog/improvements-to-kea-dhcp
title: 24.08 Sneak Peek: Improvements to Kea DHCP for Improved High Availability and Unbound DNS Resolution in pfSense® Software
category: community
priority: 2
pfsense_version_notes: 24.08 Kea HA improvements
fetched_date: 2026-08-13
converter: webfetch
---

# 24.08 Sneak Peek: Improvements to Kea DHCP for Improved High Availability and Unbound DNS Resolution in pfSense® Software

**Written by:** Netgate
**Date:** August 06, 2024

> **CLAIM / VERSION CAVEAT:** This is a pre-release "sneak peek" for pfSense Plus 24.08. It announces Kea HA and Unbound DNS hostname registration as new in 24.08. These capabilities were not present in 23.09 (see the 23.09 blog). Treat feature-availability claims as scoped to 24.08+.

Netgate is excited to announce important updates to the integration of Kea DHCP into pfSense software, adding support for DHCP High Availability and improved support for registration of DHCP hostnames with the Unbound DNS Resolver. With the release of pfSense Plus software version 24.08, users who require DHCP HA support or DNS resolution of DHCP hostnames can now migrate from the ISC DHCP backend to the Kea DHCP backend.

## Why Are We Migrating?

Internet Systems Consortium [ended maintenance for ISC DHCP in September 2022](https://kb.isc.org/docs/isc-dhcp-eol-dates) and recommends that users migrate to the Kea DHCP server. By moving to Kea DHCP, we ensure that the DHCP server components of pfSense software remain current and maintained.

## Kea DHCP High Availability Benefits

When compared to ISC DHCP, Kea DHCP HA offers several advantages:

- **Simplified Setup:** Kea DHCP uses a single, global HA configuration, which is easier to set up and manage than ISC DHCP's per-interface configuration.
- **More Reliable Failover:** Kea operates in "hot standby" mode, providing more reliable failover, especially when booting a secondary node.
- **IPv6 Support:** Those using IPv6 will benefit from HA support for DHCPv6, a feature not available with ISC DHCP.
- **Improved Security:** Kea DHCP supports optional TLS encryption for HA traffic, enhancing the security of your DHCP setup.

## Kea DHCP DNS Resolution Benefits

When we designed the new method for DHCP sync to DNS, we wanted to create a more robust system. We leveraged features from both Kea and Unbound along with custom code to enable efficient updating of DNS data even with Kea DHCP HA enabled. This new approach contrasts with the resource-heavy approach that was required with ISC DHCP.

The new design for DHCP hostname resolution with Kea and Unbound has several advantages:

- **Improved Update Detection:** With Kea, pfSense software uses an extension that allows Kea itself to trigger DNS changes for lease events. With ISC DHCP, pfSense software used a dedicated daemon that monitored DHCP leases externally and triggered DNS updates based on that detection. This daemon was running and consuming resources as long as the feature was enabled, and it was not always reliable.
- **Improved HA DNS Resolution:** We extended the lease database in Kea to include the client hostname and related properties, which has the natural benefit of working seamlessly with Kea HA lease synchronization. Kea already synchronizes the entire lease database, so both HA nodes now have synchronized DNS information available. With ISC DHCP, both nodes served leases separately and the failover synchronization did not include hostnames, so each HA node had incomplete records for dynamic lease hostnames.
- **No Service Interruptions:** The new method of updating DNS records in the resolver utilizes features of Unbound for seamless updates. When a DHCP event occurs, it compares current DNS records with records associated with DHCP leases so it can determine exactly which records require updates. It then makes a minimized set of changes in a way that does not require restarting the Unbound service. The older method of integrating ISC DHCP and Unbound relied on rewriting all hostnames and restarting Unbound any time there was an update, including any time ISC DHCP issued a lease. This resulted in an interruption of DNS service any time a DNS record had to be updated.

## Migration Timeline

The migration to Kea DHCP has been ongoing for some time, and with the addition of High Availability support in pfSense Plus software version 24.08, we are approaching the final stages of this transition. Our goal is to reach feature parity between the Kea and ISC DHCP backends over the next few releases. We recommend converting to Kea DHCP once it supports all the features your specific deployment needs, ensuring a smooth transition for your network.

The initial implementation of HA for Kea DHCP will be available to pfSense Plus software customers in the upcoming 24.08 release.

## High Availability With Kea DHCP

As mentioned earlier, Kea DHCP offers several advantages over ISC DHCP. Here is how HA will work with the new Kea DHCP backend:

- **Hot Standby Mode:** Kea DHCP operates in a "hot standby" mode, where the primary node serves DHCP leases exclusively. If the primary node fails, the standby node takes over and serves leases until the primary recovers. This approach aligns well with pfSense software's general HA behavior.
- **Improved Failover Resilience:** Unlike ISC DHCP, Kea HA can serve leases from a secondary node even if it boots while the primary node is offline. This enhances the availability of your DHCP service in various failure scenarios.
- **Simplified Configuration:** Kea uses one set of global HA settings per node, vastly simplifying the configuration process compared to ISC DHCP's per-interface failover configuration.
- **Enhanced Security:** Kea uses a single address per node for all HA traffic (lease synchronization, heartbeats, etc.), typically on the Sync interface. This approach is safer and more secure as it doesn't expose HA traffic to end-user networks. Additionally, Kea supports optional TLS encryption and authentication for HA traffic, further enhancing security.
- **Improved Status Tracking:** Kea tracks HA status globally for each node, providing a more comprehensive and coherent view of the HA system state. This contrasts with ISC DHCP, which tracks HA status separately for each address pool.
- **Better Lease Management:** Kea's lease synchronization includes hostnames, ensuring more complete data consistency between nodes.
- **IPv6 Support and Flexible Communication:** Kea DHCP fully supports HA for IPv6 in DHCPv6, a feature not available in ISC DHCP. This includes XMLRPC configuration synchronization for Kea DHCPv6 settings and Router Advertisement settings between nodes. Furthermore, Kea can use either IPv4 or IPv6 for HA traffic in both DHCPv4 and DHCPv6 environments.

## Next Steps

We are sharing this information prior to the software release so you have time to prepare for the change. In the coming release, we will provide a Configuration Recipe that shows how to move your existing pfSense software HA setup from the ISC DHCP backend to the Kea DHCP backend.

Our [support team](https://www.netgate.com/tac-support-request) is ready to assist you through this transition. For pfSense CE users interested in earlier release access and dedicated support, consider [upgrading](https://shop.netgate.com/products/pfsense-software-subscription-tac-lite-support) to pfSense Plus software.

We are confident this transition to Kea DHCP will improve the customer experience, performance, and security of pfSense software. Thank you for your continued support!
