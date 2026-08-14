---
source_url: https://docs.netgate.com/pfsense/en/latest/services/dhcp/kea-settings.html
title: Kea Settings Tab
category: pfsense-core
priority: 1
pfsense_version_notes:
fetched_date: 2026-08-13
converter: webfetch
---

# Kea Settings Tab

When using the Kea DHCP backend ([Server Backend](../../config/advanced-networking.html#config-advanced-net-dhcp-backend)) there is a **Settings** tab with global options to control DHCP server behavior not specific to a given interface.

Note

There are separate pages for DHCPv4 and DHCPv6, and they operate independently. However, the options on each page are identical otherwise. Differences between DHCPv4 and DHCPv6, if any, are noted when appropriate.

## General Settings

### DHCP Client DNS Registration with the DNS Resolver

The DNS Registration options control the default Kea behavior for registering DHCP client hostnames with the [DNS Resolver](../dns/resolver.html) so that other clients using this firewall for DNS resolution can resolve these hostnames.

This implementation with Kea works with both DHCPv4 and DHCPv6 client lease data.

Note

When using the Kea DHCP daemon, pfSense software dynamically updates these hostnames with the DNS Resolver without restarting the daemon. DNS updates are seamless and not disruptive, unlike the previous implementation with the ISC DHCP daemon.

Kea DNS Registration also respects the domain name configured in DHCP settings for an interface or static mapping. If no domain is set in the DHCP lease, it falls back to checking for a search domain or, as a last resort, the domain name configured on the firewall.

DNS updates are also kept up-to-date between High Availability failover peers.

DNS Registration:

Controls the default DNS Registration behavior on all interfaces with DHCP enabled. When checked, Kea will automatically register hostnames from DHCP leases on all interfaces with the DNS Resolver by default.

The setting can be overridden on a per-interface basis in either direction. This allows selectively enabling or disabling DNS Registration for specific interfaces as needed.

Early DNS Registration:

Controls whether Kea will register hostnames from DHCP static mappings with the DNS Resolver at startup by default. The setting can be overridden on a per-interface basis in either direction.

When unchecked, Kea does not register the hostname until the client requests a DHCP lease.

With this setting enabled a client does not need to have DHCP enabled for its hostname to be available via the DNS Resolver. This was the default behavior of the ISC DHCP daemon when it performed DNS registration.

## High Availability

The **High Availability** section of the page configures the daemon for high availability failover with a peer. This operates in "Hot Standby" mode where one node hands out addresses and they both share lease data while monitoring the other peer. If the active primary node becomes unresponsive, the standby node will take over handing out leases to clients. As the two nodes share lease data, failover is seamless and clients can obtain addresses so long as one of the two nodes is online and functional.

Note

Most of these settings will synchronize via XMLRPC configuration synchronization, except for the TLS Transport options which are per-node options and do not synchronize.

The **High Availability** section contains the following options:

Enable:

When checked, enables hot-standby high availability (HA) for Kea DHCP services.

Node Role:

Chooses the role for this node when performing high availability.

Primary:

This node will serve leases for clients when both nodes are online and functioning properly.

Standby:

This node will only serve leases when the primary node is down.

Local Name:

The name of this device, such as its hostname.

Local Address:

The IP address of this node upon which it will listen for failover data from the peer.

Note

This is typically the local IP address on the Sync interface.

The address family of this IP address does not need to match the address family of the DHCP service. Both DHCPv4 and DHCPv6 can exchange HA data with IPv4 or IPv6 peers.

Remote Name:

The name of the remote peer, such as its hostname.

Remote Address:

The IP address where the remote peer is listening for failover data from this node.

Note

This is typically the IP address of the Sync interface on the peer.

The address family of this IP address does not need to match the address family of the DHCP service. Both DHCPv4 and DHCPv6 can exchange HA data with IPv4 or IPv6 peers.

When these settings synchronize via XMLRPC configuration synchronization, the values are swapped – the secondary node is configured with the opposite settings so it will have appropriate settings from its frame of reference.

### Advanced Options

Heartbeat Delay:

Specifies a duration in milliseconds between sending the last heartbeat and the next heartbeat. Default value is `10000` (10 seconds).

The heartbeats are sent periodically to gather the status of the partner and to verify whether the partner is still operating.

Max Response Delay:

Specifies a duration in milliseconds since the last successful communication with the partner, after which the server assumes that communication with the partner is interrupted. Default value is `60000` (60 seconds).

Warning

This duration should be greater than the heartbeat delay.

Max Ack Delay:

Specifies the maximum time in milliseconds for the client to try to communicate with the DHCP server, after which this server assumes that the client failed to communicate with the DHCP server (is "unacked"). Default value is `60000` (60 seconds).

Max Unacked Clients:

Specifies how many unacknowledged clients are allowed before this server assumes that the partner is offline and transitions to the `partner-down` state. Default value is `0` (takes over immediately).

Warning

Do not set this higher than the typical number of clients which would make a DHCP request in a short time frame. Otherwise, clients can be left without an address until additional clients also fail to obtain addresses, which could be a significant amount of time on a small or quiet network. See [Secondary Does Not Enter partner-down State](../../troubleshooting/ha-dhcp-failover.html#troubleshooting-ha-dhcp-no-partner-down) for more details.

Max Rejected Updates:

Specifies how many lease updates for distinct clients can fail, due to a conflict between the lease and the partner configuration or state, before the server transitions to the terminated state. Default value is `10`.

These settings synchronize as-is over XMLRPC configuration synchronization.

### TLS Transport

Configures optional encryption and certificate-based authentication to protect the DHCP HA data exchanged between failover peers.

These settings **do not** synchronize over XMLRPC configuration synchronization.

Enable:

When checked, enables TLS encryption for DHCP HA data requests. This encrypts the lease data and heartbeat traffic exchanged between the peers.

Server Certificate:

The certificate to use for the local DHCP HA server.

Mutual TLS:

When checked, configures the Kea HA client to send a client certificate which allows the peer to verify that it is communicating with the expected client.

This ensures that only authorized peers can communicate with the DHCP HA services.

Client Certificate:

The client certificate which identifies this node.

## Custom Configuration

The KEA GUI allows administrators to configure Kea directly with JSON-formatted configuration snippets. The Kea GUI in pfSense software does not implement some features or options which are possible directly in Kea. As the Kea GUI develops further, the GUI will be capable of configuring more of these features. These snippets allow administrators more control in the meantime.

Tip

These snippets can be used to add functionality such as custom DHCP options, dynamic DNS registration, and fine-tune lease behavior.

These fields are present on each Kea page and the system adds the contents of each configuration snippet to a different section of the Kea configuration file based on the Kea configuration page:

| Kea GUI Page | Kea Configuration Section |
| --- | --- |
| DHCPv4 Settings | `Dhcp4` |
| DHCPv6 Settings | `Dhcp6` |
| DHCPv4/v6 interfaces | `subnet` |
| DHCPv4/v6 Pools | `pool` |
| DHCPv4/v6 static mappings | `reservation` |

Warning

These configuration fields must contain well-formed JSON objects and must not include the name of the section itself.

The system adds these snippets to the Kea configuration after the settings from the GUI for each section. So not only can these snippets enable new features, but they also allow administrators to modify or override the base configuration.

These configuration snippets are held in `config.xml`, so they are backed up and restored along with other Kea settings.

The system tests the configuration before attempting to start Kea. If the configuration test fails with the custom snippets, the system files a notice alerting administrators to the problem, then it attempts to start Kea without including the custom configuration snippets.

See also

See the following forum thread for configuration snippet examples and discussion: [https://forum.netgate.com/topic/196513/adding-custom-configuration-in-kea-dhcp-server-with-pfsense-25-03](https://forum.netgate.com/topic/196513/adding-custom-configuration-in-kea-dhcp-server-with-pfsense-25-03)
