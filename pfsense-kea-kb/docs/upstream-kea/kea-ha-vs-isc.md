---
source_url: https://kb.isc.org/docs/aa-01617
title: Kea High Availability vs. ISC DHCP Failover
category: upstream-kea
priority: 1
pfsense_version_notes:
fetched_date: 2026-08-13
converter: webfetch
---

# Kea High Availability vs ISC DHCP Failover

#### Introduction

Kea High Availability (HA) was released along with Kea 1.4.0. Numerous improvements in the Kea server code had been applied to support this feature, but the HA functionality itself is included in the HA hook library (libdhcp_ha). The HA library addresses a common need present in many deployments, to provide a reliable and continuous DHCP service if one of the DHCP servers belonging to this deployment fails. In ISC DHCP this functionality was provided by the implementation of the DHCP Failover protocol described in the [IETF DHCP Failover Protocol draft.](https://datatracker.ietf.org/doc/html/draft-ietf-dhc-failover) The Kea HA implementation shares many design concepts with the Failover, but it is NOT a Failover implementation!

The details of the HA library design can be found in the [Kea HA Design document](https://gitlab.isc.org/isc-projects/kea/wikis/designs/High-Availability-Design). [A quickstart guide](https://kb.isc.org/docs/kea-ha-quickstart-guide) to using Kea HA is also available. The [ARM HA hook documentation](https://kea.readthedocs.io/en/kea-2.6.1/arm/hooks.html#libdhcp-ha-so-high-availability-outage-resilience-for-kea-servers) contains comprehensive information about the feature. This document focuses on highlighting major differences between features of the Kea HA library and ISC DHCP Failover. It is aimed at DHCP service administrators who are considering migration from ISC DHCP to Kea and who seek guidance on whether the Kea HA implementation is going to be suitable for their use cases.

The following table summarizes the notable differences between the two implementations. The text following the table elaborates on these differences.

#### Feature matrix

| Feature | Kea High Availability | ISC DHCP Failover |
| --- | --- | --- |
| Supported protocols | DHCPv4 and DHCPv6 | DHCPv4 |
| # of cooperating servers | 2 active + unlimited backup servers | 2 servers |
| Dispersed servers | yes (performance degradation with more dispersed servers) | yes |
| Multiple failover relationships | 1 Kea instance per relationship (Note that in 2.5.4 and 2.5.5 the [Hub and Spoke mode](https://kea.readthedocs.io/en/kea-2.6.1/arm/hooks.html#hub-and-spoke-configuration) was added) | 1 ISC DHCP instance supports multiple relationships |
| Load balancing | 50/50 split (RFC3074) | Flexible split (RFC3074) |
| Active-passive | yes | yes |
| Auto partner down | yes | yes |
| Lazy lease updates (MCLT) | no (server waits for lease update completion before responding to client) | yes (server responds to the client immediately) |
| Send lease updates to external entity | yes (via backup server mechanism or using custom hook library) | no |
| Rebalancing pools | no | yes |
| Database replication for sharing lease info | yes (optional) | no |
| Communication interruption detection | yes | yes |
| Partner failure detection by monitoring latency | by monitoring 'secs' field in DHCPv4 or "Elapsed Time" option in DHCPv6 | by monitoring 'secs' field |
| Control over the servers | via RESTful API (set HA scopes, enable/disable DHCP, on demand lease sync) | via OMAPI |

#### Supported protocols

IETF attempted to standardize two DHCP failover protocols: [DHCPv4 Failover draft](https://datatracker.ietf.org/doc/html/draft-ietf-dhc-failover), which was an Internet Draft status that expired Sept. 2003. The other one, [RFC 8156: DHCPv6 Failover](https://tools.ietf.org/html/rfc8156), was published as a Proposed Standard. ISC DHCP implemented the former, but not the latter. As such, ISC DHCP is able to provide failover for DHCPv4 only, not DHCPv6. The Kea HA solution supports both DHCPv4 and DHCPv6.

#### Number of cooperating servers

In ISC DHCP the failover relationship is between a pair (two) of servers. In Kea HA it is possible to define additional backup servers. While they are not technically participating in the HA relationship, their lease databases are kept up to date and can be used to quickly create a replacement server. However, replacing a primary or secondary server with a backup requires manual intervention from the administrator.

#### Dispersed servers

Both ISC DHCP and Kea HA support configurations in which the participating servers are not located in the same subnet, e.g. multi-site configuration where the servers are geographically dispersed. In that case, even a severe outage in the whole site should not impact the DHCP service because the server in the other site can take over the DHCP traffic. However, it must be taken into consideration that the increased latency in communication between the geographically dispersed servers increases the latency of the DHCP responses. This is because the servers wait for the completion of the lease updates before responding to the DHCP clients. This is not the case in ISC DHCP Failover as it does not wait for the completion of the lease updates.

#### Multiple failover relationships

A single instance of the ISC DHCP server can be configured to participate in multiple failover relationships, where each relationship is established with one partner server. Kea can now (as of 2.5.5) also establish multiple relationships as well. The original design is called Hub & Spoke and is documented in the [ARM](https://kea.readthedocs.io/en/latest/arm/hooks.html#hub-and-spoke-configuration). As it turns out, the design is more flexible than the ARM documentation implies. The exploration of these capabilities has been documented in another knowledge base article [here](https://kb.isc.org/docs/kea-ha-hub-spoke-experimentation). The differences between the implimentation of multiple failover relationships in ISC DHCP and Kea are limited to only supporting multiple failover relationships when using "Hot Standby" mode in the case of Kea, while ISC DHCP is able to support "Load Balancing" and multiple failover relationships. Kea does have an advantage in that backup servers may still be deployed to participate in the multiple relationships.

#### Load balancing

The Kea HA solution provides a load balancing capability with a 50/50 fixed split of the DHCP load. ISC DHCP allows for customizing the split between the failover peers (splits of 50/50, 80/20, and 60/40 are all possible). Both solutions use the technique described in [RFC 3074](https://tools.ietf.org/html/rfc3074) for load balancing.

#### Active-passive

Both ISC DHCP and Kea HA support the mode of operation in which one server is processing the entire DHCP traffic directed to the system and the partner server remains in the "standby" state, ready to take over the role of the primary server when it becomes unavailable. This mode of operation is also called "Hot Standby" in the Kea HA terms.

#### Auto partner down

Both ISC DHCP and Kea HA support automatic transition of the server to the "partner-down" state when it detects a failure of the partner. In this state the server is handling the entire DHCP traffic directed to the system. When the failing partner recovers, the lease databases are synchronized between the partners and both resume normal operation, e.g. load balancing or hot standby.

#### Lazy lease updates (MCLT)

Both IETF failover protocols are based on MCLT (or Maximum Client Lead Time), sometimes referenced to as lazy updates. This mechanism lets a server respond immediately, which improves latency, but it does so at the cost of greatly increased complexity. The lease is assigned with a very short lifetime, then an update is sent to the other server with a lifetime greater than the client requested. Once the other server confirms the lease, the client's renewal is being updated with a longer lifetime. This approach generates more traffic and causes lease lifetimes to fluctuate greatly, despite an administrator setting it to a specific value. Kea HA does not implement this complexity. It is much simpler and easier to use and understand its operation, although the price to pay for this relative simplicity is a longer response time and somewhat decreased performance. Note that as of 2.3.7, HA now defaults to multi-threaded operation and a direct connection between the two peers (see [here](https://gitlab.isc.org/isc-projects/kea/-/issues/2749)). Therefore, Kea likely outperforms ISC DHCP, even without MCLT, in most cases. Previously, the default was single threaded with communication via `kea-ctrl-agent` which created a further bottleneck.

#### Send lease updates to external entity

A relationship in ISC DHCP Failover includes two servers communicating lease changes to each other and monitoring for failures. ISC DHCP provides no easy-to-use solution to capture lease changes and replicate them to an external application. The Kea HA relationship may optionally include an unlimited number of backup servers to which lease updates are also communicated. These servers do not participate in responding to DHCP queries, but keep up-to-date lease databases and can be manually instructed to respond to DHCP queries when one or two active servers are down. The backup server lease database (or lease file) can also be used by an external application to fetch lease information. A more effective approach is to build an application which can respond to the lease updates over HTTP and appears to the Kea active servers as a backup server. An example of such application is an IPAM system being notified about new lease allocations from the active servers and performing specific actions driven by these events: local database update, monitoring of servers' throughput etc. If building an application that implements Kea RESTful interface to receive lease updates is not applicable or not practical for any reason, it is possible to implement a simple hook library to be attached to Kea active servers which generates lease updates in a custom format and send it over a custom channel.

#### Rebalancing pools

Both ISC DHCP Failover and Kea HA are capable of load balancing the DHCP traffic directed to the system. ISC DHCP is more flexible in that it allows for configuring the split of queries between the servers. Kea uses a fixed split of 50/50, i.e. roughly 50% of requests are handled by one HA peer and another 50% are handled by another peer. In both ISC DHCP and Kea, the desired split may differ from the actual split, depending on the number of clients communicating with the DHCP servers. For example, for 500 clients communicating with the servers, the load on the servers will be much closer to the configured split than for 10 clients.

In Kea HA, the pools are partitioned manually between the active servers, so it is theoretically possible that one server could run out of addresses while the other server has plenty available. ISC DHCP can rebalance the pools between the servers, so the server with more addresses can transition some of them to the server which is experiencing an address shortage. Such rebalancing is currently not supported in Kea HA. In order to make sure that the fluctuations of load balancing do not cause pool exhaustion, address pools should have greater capacity than the estimated number of clients communicating with the servers.

When using "Hot Standby" mode, no pool splitting is used and no rebalance would be necessary. The currently active server always has access to 100% of the configured address pool.

#### Database replication for sharing lease info

ISC DHCP stores lease information in the file and has no integration with external databases. Kea supports switchable lease database backends, which allow for storing lease information in the databases such as MySQL/MariaDB and PostgreSQL. Those databases support their own clustering mechanisms for high availability and scalability. Many Kea users use the data replication mechanisms provided by the databases to achieve DHCP service redundancy. In that case, two (or more) Kea servers can use their own database instances, which replicate the information to the partner's database. Alternatively, both Kea servers can be pointed to the same database instance which can be backed up by another instance. Kea HA introduces useful functionality to facilitate this architecture, as it provides load balancing as well as partner failure detection. Lease updates can be disabled in the HA hook library relying on database replication to share the lease information between the servers.

Kea HA deals with one of the major issues related to the use of database replication for redundancy, i.e. load balancing and separation of the pools to be used by the participating servers eliminate the issue whereby two servers would sometimes try to offer the same lease to the different clients. Kea 2.3.4 introduced the [Random allocator](https://gitlab.isc.org/isc-projects/kea/-/issues/969), which also potentially solves this problem without need of the HA hook. Kea 1.4.0 also corrects inaccurate lease statistics returned when multiple servers were using the same lease database. Previously, each server was returning a number of leases allocated by itself. Now lease statistics are calculated in the common database and include leases stored in this database by all servers.

#### Communication interruption detection

In both ISC DHCP and Kea HA, participating servers are continuously communicating with each other to verify if they are still operational. If the communication between the servers fails, the servers react to this by taking over the DHCP traffic of the partner to allow DHCP clients to renew and obtain new leases.

#### Partner failure detection by monitoring latency

If communication with the partner server fails, it doesn't necessarily mean that the partner is not operational. This may be caused by network partitioning between the partners and may be temporary. Therefore, both ISC DHCP and Kea HA implementations use additional measures to detect whether the partner is still operational. In DHCPv4, the servers monitor the values in the `secs` field within the packets directed to the partner server. High values of the `secs` field indicate high latency of responses (or lack of thereof) and confirm that the partner is not responding. In case of DHCPv6, the same mechanism is used, but the monitored value is the one carried in the Elapsed Time option (ISC DHCP doesn't support DHCPv6 Failover, so it doesn't use this mechanism).

It is important to note a key difference between Kea and ISC DHCP regarding failure detection and general operation. ISC DHCP failover peers will monitor all DHCP traffic regardless of current failure state. The peer that is currently not assigned to a particular DHCPv4 client, will still answer that client in the case that the `secs` field is larger than the value set in `load balance max seconds`. Kea does not implement this mechanism. A Kea HA peer will not answer any clients that are not assigned to it unless it has first entered the "communications-interrupted" state, and has subsequently encountered the required amount of unacked clients thus proceeding to the "partner-down" state. See the [ARM](https://kea.readthedocs.io/en/latest/arm/hooks.html#the-status-get-command) for details about this process.

#### Control over the servers

In Kea, communication between the partners is conducted via the RESTful API. This includes lease updates, heartbeat messages, commands to disable and enable DHCP function on the partner, and fetch/synchronize leases. The same commands can be sent to both servers by an administrator, giving the administrator control over the operation of the servers. For example, the administrator may disable DHCP functions on one server to perform manual synchronization of the lease database. In the future it is also planned to add more tight control over the HA state machine, e.g. pause the state machine in the given state. ISC DHCP also provides control over the servers via OMAPI. This, however, can be awkward to use and debug.
