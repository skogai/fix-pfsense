---
source_url: https://docs.netgate.com/pfsense/en/latest/services/dhcp/ipv6.html
title: DHCPv6 Server
category: pfsense-core
priority: 1
pfsense_version_notes:
fetched_date: 2026-08-13
converter: webfetch
---

# DHCPv6 Server

The DHCPv6 server in pfSense® software allocates addresses to DHCPv6 clients and automatically configures them for network access. By default, the DHCPv6 server is enabled on the LAN interface and set to use a prefix obtained by tracking a DHCPv6 delegation from the WAN interface.

To alter the behavior of the IPv6 DHCP server, navigate to **Services > DHCPv6 Server** in the web interface. This page contains a tab for each interface capable of offering DHCPv6 service. The behavior of the IPv6 DHCP server for an interface is controlled on each tab, along with static IP address mappings and related options.

Warning

The DHCPv6 server cannot be active on any interface if the [DHCPv6 Relay](relay.html) service is in use.

Note

For clients to query DHCPv6, [Router Advertisements](ipv6-ra.html) must also be enabled and set to either *Managed* or *Assisted* mode under **Services > Router Advertisements**.

## Settings Tab

When using the Kea DHCP backend there is a **Settings** tab with global options to control DHCP server behavior not specific to a given interface. The options on the **Settings** tab are covered in [Kea Settings Tab](kea-settings.html).

## Choosing an Interface

The DHCPv6 daemon can run and be configured on interfaces with a Static IP address or interfaces which track delegated prefixes from upstream sources. If a tab for an interface is not present, check that it is enabled and configured either with a Static IPv6 address or to track a DHCPv6 type WAN which obtains a prefix delegation from an external source.

Note

The settings available on the page vary depending on the active DHCP backend (Kea or ISC DHCP). Differences are noted where applicable.

Note

DHCPv6 does not provide gateway information. [Router Advertisements](ipv6-ra.html) inform hosts on the network about available routers. DHCPv6 is for other host configuration such as DNS, delegation, and so on.

See also

See the [DNS Forwarder](../dns/forwarder.html) article for information on the default DNS server behavior.

## General Options

DHCP Backend:

This read-only field displays the current DHCP backend, either Kea DHCP or ISC DHCP.

The backend can be changed under **System > Advanced**, **Networking** tab ([Server Backend](../../config/advanced-networking.html#config-advanced-net-dhcp-backend)).

Enable:

The first setting on the tab enables or disables DHCPv6 service for the interface. To turn on DHCPv6 for the interface, check **Enable DHCPv6 server on [name] interface**. To disable the service, uncheck the box instead.

Deny unknown clients:

Controls how the DHCP server handles requests from clients which it does not know.

Note

This option is per-pool, meaning that if unknown clients are denied in the default range, another pool of IP addresses may be defined that allows clients instead.

Can be set to one of the following values:

Allow All Clients:

This is the default behavior. The DHCPv6 server will answer requests from any client requesting a lease. In most environments this is normal and acceptable behavior, but in restricted or secure environments this behavior is undesirable.

Allow known clients from any interface:

With this option set, clients with static mappings defined on any interface will receive leases from this pool. This is a more secure practice but requires much more management overhead.

Allow known clients from only this interface:

With this option set, clients with static mappings defined on this interface will receive leases from this pool. This is a more secure practice but requires much more management overhead.

Note

This will protect against low-knowledge users and people who casually plug in devices. Be aware, however, that a user with knowledge of the network could hardcode an IP address, subnet mask, gateway, and [DNS](../../glossary.html#term-DNS) which will still give them access. They could also alter/spoof their DUID to match a valid client and still obtain a lease. Where possible, couple this setting with access control in a switch that will limit access to switch ports for increased security, and turn off or disable unused switch ports.

DNS Registration:

Controls the [DNS Registration](kea-settings.html#services-kea-dhcp-settings-dns-registration) behavior of this interface.

Track Server:

Follows the default behavior for DNS Registration configured on the **Settings** tab.

Enable:

Ignores the default setting and enables DNS Registration for DHCP clients on this interface.

Disable:

Ignores the default setting and disables DNS Registration for DHCP clients on this interface.

Early DNS Registration:

Controls the [Early DNS Registration](kea-settings.html#services-kea-dhcp-settings-dns-registration) behavior of this interface.

Track Server:

Follows the default behavior for Early DNS Registration configured on the **Settings** tab.

Enable:

Ignores the default setting and enables Early DNS Registration for DHCP clients on this interface.

Disable:

Ignores the default setting and disables Early DNS Registration for DHCP clients on this interface.

## Primary Address Pool

Prefix:

A read-only field with the current prefix on this interface. If the prefix is delegated, this field also shows the WAN which supplied the tracking data and the subnet ID.

Prefix Range:

A read-only field with the total available range of addresses in the prefix.

Address Pool Range:

This field defines the start and end of an address range defining a pool from which the DHCP server will allocate addresses. This range can be as large or as small as the network needs, but it must be wholly contained within the subnet.

Addresses between the entered values, inclusive, will be used for clients which request addresses via DHCPv6.

From:

The starting address of the pool. For interfaces which obtain a prefix dynamically, the prefix itself may be omitted. The value defined in this field will be added to the prefix automatically.

Must be lower than the **To** address.

To:

The ending address of the pool. For interfaces which obtain a prefix dynamically, the prefix itself may be omitted. The value defined in this field will be added to the prefix automatically.

Must be higher than the **From** address.

Tip

Given the vast amount of space available inside even a /64, a good trick is to craft a range that restricts hosts to use an easy to remember or recognize range. For example, Inside a /64 such as `2001:db8:1:1::`, set the DHCPv6 range be: `2001:db8:1:1::d:0000` to `2001:db8:1:1::d:FFFF`, using the `d` in the second to last section of the address as a sort of shorthand for "DHCP". That example range contains 2^16 (65,536) IPs, which is extremely large by today's IPv4 standards, but only a small portion of the whole `/64`.

### Additional Pools

The **Additional Pools** section defines extra pools of addresses inside the same subnet. These pools can be used to craft sets of IPv6 addresses specifically for certain clients, or for overflow from a smaller original pool, or to split up the main pool into smaller chunks with a GAP of non-DHCPv6 IPv6 addresses in the middle of what used to be the pool.

To add a new pool, click **Add Address Pool** and the screen will switch to the pool editing view, which is nearly the same as the normal DHCPv6 options, except a few options that are not currently possible in pools are omitted. The options behave the same as the others discussed in this section. Items left blank will, by default, fall through and use the options from the main DHCPv6 range.

## DHCPv6 Prefix Delegation

Prefix delegation, covered earlier in [DHCP6 Prefix Delegation](../../network/ipv6/subnets.html#ipv6-address-allocation-dhcp-pd) and [Track Interface](../../interfaces/configure-ipv6.html#ipv6-wan-track-interface), allows automatically dividing and allocating a block of IPv6 addresses to networks that will live behind other routers and firewalls which reside downstream from this firewall (e.g. in the LAN, DMZ, etc.). Downstream devices which request a delegation can in turn use prefixes in their delegation for their LAN, VPNs, DMZ, etc. Downstream firewalls can even further delegate their own allocation to routers behind them.

Note

Most users on networks act only in a client capacity and will not need this, so it will likely remain blank.

Prefix delegation can be used to allocate `/60` chunks of a `/48` to downstream routers automatically, or many other combinations. The downstream router obtains an IPv6 address then requests a delegation, the server delegates a prefix and dynamically routes the delegated prefix to that downstream router.

Delegated Prefix:

Defines the delegation pool. This block of IPv6 addresses must be routed to this firewall by upstream routers either directly or as part of a larger allocation.

The length of this prefix must be smaller than, or equal to, the **Delegated Length**.

Warning

The deprecated ISC DHCPv6 server defined this value as a range instead of a prefix. As such, it may not be possible to set this value identically to previous configurations. However, it is much easier to specify as a prefix rather than having to calculate the start/end and check boundaries.

Delegated Length:

Sets the size of the prefix delegations allocated to clients. This must be larger than, or equal to, the prefix length of the **Delegated Prefix**.

Note

In nearly all cases this should be smaller than `/64` and not larger than or equal to `/64`. A delegated prefix with a length larger than /64 could never be properly utilized by the majority of clients. While a single `/64` delegation is valid, it is of minimal use to downstream routers as it only allows room for a single proper internal network.

For example, start with a prefix of `2001:db8::ffff:f000/52` earmarked for delegation to downstream routers. This **Delegated Prefix** has a length of `/52`. Using a **Delegated length** value of `/60` accommodates up to **256** downstream router client delegations. Each of these delegations is a contiguous `/60` block of the **Delegated Prefix**, which is equivalent to **16** subnets of size `/64`.

## Server Options

Enable:

When set, the DHCP server provides DNS servers to DHCPv6 clients upon request.

Warning

Unchecking this box disables the `dhcp6.name-servers` option. Use with caution as the resulting behavior may violate RFCs and lead to unintended client behavior.

DNS Servers:

Defines up to four DNS server IPv6 addresses which the server provides to clients. To use custom DNS Servers instead of automatic choices, fill in the DNS server IPv6 addresses.

Tip

When using the DNS Resolver or DNS forwarder in combination with high availability clustering, specify an IPv6 CARP Virtual IP address on this interface as the only DNS server.

When left empty, the firewall will automatically determine which addresses to supply to clients depending on the DNS configuration on this firewall:

-   If the firewall is using the built-in DNS Resolver or DNS Forwarder to handle DNS, leave these fields blank. It will automatically assign itself as the DNS server for client devices.
-   If the DNS Resolver or Forwarder is disabled and these fields are left blank, the firewall will pass on whichever DNS servers are defined under **System > General Setup**.

Tip

In networks with Windows servers, especially those employing Active Directory, the best practice is to use those servers for client DNS.

## Other DHCPv6 Options

Domain Name:

Specifies the domain name passed to the client to form its fully qualified hostname. If the **Domain Name** is left blank, then the domain name of the firewall it sent to the client. Otherwise, the client is sent this value.

Domain Search List:

Controls the DNS search domains that are provided to the client via DHCP. If multiple domains are present and short hostnames are desired, provide a list of domain names here, separated by a semicolon. Clients will attempt to resolve hostnames by adding the domains, in turn, from this list before trying to find them externally. If left blank, the Domain Name option is used.

Note

The **Domain Search List** is provided via DHCP option `119`. See [Using DHCP Search Domains on Windows DHCP Clients](client-search-domain.html) for details.

Default lease time:

Controls how long a lease will last when a client does not request a specific lease length. Specified in seconds, default value is `7200` seconds (2 hours)

Maximum lease time:

Limits a requested lease length to a stated maximum amount of time. Specified in seconds, default value is 86400 seconds (1 day).

Time Format Change (ISC Only):

By default, the ISC DHCP daemon maintains lease times in UTC. When this option is checked, the times on the DHCP Leases status page are converted to the local time zone defined on the firewall.

## Dynamic DNS (ISC Only)

For Dynamic DNS settings, click **Display Advanced** to the right of that field, which displays the following options:

DHCP Registration:

Check the box to enable registration of DHCP client names in DNS using an **external** DNS server (not on the firewall).

DDNS Domain:

The domain name used for registering clients in DNS

DDNS Hostnames:

When set, forces the dynamic DNS hostname to match the hostname on a static mapping instead of taking the name given by the client.

Primary DDNS Address:

The DNS server used for registering clients in DNS

Secondary DDNS Address:

The secondary DNS server used for registering clients in DNS

DNS Domain Key Name:

The name of the encryption key used for DNS registration

Key Algorithm:

The algorithm used to generate the **DDNS Domain Key Secret** value.

DDNS Domain Key Secret:

The secret for the key used for DNS registration

DDNS Client Updates:

How the DHCP server handles Forward entries when a client indicates it wishes to update DNS itself.

Allow:

Prevents DHCP from updating Forward entries, allowing the client to make the update request itself.

Deny:

Indicates that DHCP will do the updates and the client should not.

Ignore:

Specifies that DHCP will do the update and the client can also attempt the update, usually using a different domain name.

DDNS Reverse:

When set, attempts to add reverse DNS entries.

## NTP Servers

To specify NTP Servers (Network Time Protocol Servers), click the **Display Advanced** button to the right of that field, and enter IP addresses for up to four NTP servers.

## Network Booting

Enable:

Enables Network Booting options for DHCPv6

Boot File URL:

URL containing boot files.

## Custom Configuration (KEA Only)

The KEA GUI allows administrators to configure Kea directly with JSON-formatted configuration blocks. See [Custom Configuration](kea-settings.html#kea-custom-config) for details.

## Additional BOOTP/DHCP Options (ISC Only)

Other numeric DHCP options can be sent to clients using the **Additional BOOTP/DHCP Options** controls. To view these options, click **Display Advanced** in this section. To add a new option, click **Add Option**.

Number:

The DHCP option code number. IANA maintains a [list of all valid DHCP options](https://www.iana.org/assignments/bootp-dhcp-parameters/bootp-dhcp-parameters.xml).

Value:

The value associated with this numeric option and type.

Warning

When using numbered custom options, be aware that numbered options do NOT correspond exactly to the DHCP numbered options for IPv4

For more information on DHCP option numbers and types, see [https://tools.ietf.org/html/draft-ietf-dhc-v6opts-00](https://tools.ietf.org/html/draft-ietf-dhc-v6opts-00)

## Save Settings

After making changes, click **Save** before attempting to create static mappings. Changes to settings will be lost if the browser leaves this page without saving.

## DHCPv6 Static Mappings

Static mappings on DHCPv6 work differently than IPv4. On IPv4, mappings were matched and identified using the MAC address of a device. For IPv6, the designers decided that wasn't good enough, since the MAC address of a device could change, but still be the same device. Thus, the designers came up with the DHCP Unique Identifier (DUID) which in theory would be a unique ID per device without the same constraints as using MAC addresses.

### DHCP Unique Identifier (DUID)

The **DHCP Unique Identifier**, or **DUID**. The DUID of the host is generated by the operating system of the client and, in theory, will remain unique to that specific host until such time as the user forces a new DUID or the operating system is reinstalled. The DUID can range from 12 to 20 bytes, and varies depending on its type.

This field expects a DUID for a client PC in a special format, represented by pairs of hexadecimal digits, separated by colons, such as `00:01:00:01:1b:a6:e7:ab:00:26:18:1a:86:21`.

How to obtain this DUID depends on the operating system. The easiest way is to allow the device to obtain a lease via DHCPv6, and then add an entry from the DHCPv6 Leases View (Status > DHCPv6 Leases). On Windows, it can be found as DHCPv6 Client DUID in the output of `ipconfig /all`.

Note

On Windows, the DUID is generated at install time, so if a base image is used and workstations are cloned from there, they can all end up with the same DUID, and thus all end up pulling the same IPv6 address over DHCPv6.

Clear the DUID from the registry before making an image to clone, by issuing the following command:

reg delete HKLM\SYSTEM\CurrentControlSet\Services\Tcpip6\Parameters /f /v Dhcpv6DUID

That command may also be run on a working system to reset its DUID if needed.

#### DUID Format

The DUID format is listed on the page, but it roughly follows the format:

DUID-LLT - ETH -- TIME --- ---- address ----

DUID-LLT is link-layer plus time, which means it uses the link type of network interface on the system (Generally `00:01` to indicate the format, plus `00:01`, or `00:06` for Ethernet), plus the timestamp at which the DUID was generated in hex, plus the MAC address of the first NIC. It may be difficult or impossible to predict the DUID for a device. Unless the operating system has a way to look it up, it may be best to allow the client to obtain a dynamic lease and then copy the DUID from the leases view.

The DUID may be entered in colon-separated or dash-separated format.

### Static Mapping Settings

DHCPv6 Static Mappings have the following settings:

DHCP Unique Identifier:

The DUID, as discussed in [DHCP Unique Identifier (DUID)](#services-dhcpv6-staticmap-duid), using the format specified in [DUID Format](#services-dhcpv6-staticmap-duid-format).

IPv6 Address:

The IPv6 address field is needed if this will be a static IPv6 address mapping instead of only informing the DHCP server that the client is valid.

This IPv6 address is a **preference**, not a reservation. Assigning an IPv6 address here will not prevent another host from using the same IPv6 address. If the IP address is in use when this client requests a lease, the server will instead assign the client an address from the general pool. For this reason, the GUI does not allow assigning static mappings inside of pools.

See also

[Static Mappings Inside DHCP Pools](mappings-in-pools.html)

Hostname:

The hostname of the client. This does not have to match the hostname set on the client. The hostname set here will be used when registering DHCP addresses in the DNS resolver.

Description:

Cosmetic only, and available for use to help track any additional information about this entry. It could be the name of the person who uses the PC, its function, the reason it needed a static address, or the administrator who added the entry. It may also be left blank.
