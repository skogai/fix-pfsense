---
source_url: https://docs.netgate.com/pfsense/en/latest/services/dhcp/ipv4.html
title: DHCPv4 Server
category: pfsense-core
priority: 1
pfsense_version_notes:
fetched_date: 2026-08-13
converter: webfetch
---

# DHCPv4 Server

The DHCPv4 server in pfSense® software allocates addresses to IPv4 DHCP clients and automatically configures them for network access. By default, the DHCPv4 server is enabled on the LAN interface and configured to serve addresses in the LAN subnet (e.g. `192.168.1.0/24`).

To alter the behavior of the IPv4 DHCP server, navigate to **Services > DHCP Server** in the web interface. This page contains a tab for each interface capable of offering DHCPv4 service. The behavior of the IPv4 DHCP server for an interface is controlled on each tab, along with static IP address mappings and related options.

Warning

The DHCPv4 server cannot be active on any interface if the [DHCPv4 Relay](relay.html) service is in use.

## Settings Tab

When using the Kea DHCP backend there is a **Settings** tab with global options to control DHCP server behavior not specific to a given interface. The options on the **Settings** tab are covered in [Kea Settings Tab](kea-settings.html).

## Choosing an Interface

The DHCP configuration page contains a tab for each interface with a static IP address. Each interface has its own separate DHCP server configuration, and they may be enabled or disabled independently of one another. Before making any changes, visit the tab for the correct interface.

Note

The settings available on the page vary depending on the active DHCP backend (Kea or ISC DHCP). Differences are noted where applicable.

## General Options

DHCP Backend:

This read-only field displays the current DHCP backend, either Kea DHCP or ISC DHCP.

The backend can be changed under **System > Advanced**, **Networking** tab ([Server Backend](../../config/advanced-networking.html#config-advanced-net-dhcp-backend)).

Enable:

The first setting on the tab enables or disables DHCP service for the interface. To turn on DHCP for the interface, check **Enable DHCP server on [name] interface**. To disable the service, uncheck the box instead.

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

This will protect against low-knowledge users and people who casually plug in devices. Be aware, however, that a user with knowledge of the network could hardcode an IP address, subnet mask, gateway, and [DNS](../../glossary.html#term-DNS) which will still give them access. They could also alter/spoof their MAC address to match a valid client and still obtain a lease. Where possible, couple this setting with static ARP entries, access control in a switch that will limit MAC addresses to certain switch ports for increased security, and turn off or disable unused switch ports.

Ignore Denied Clients (ISC Only):

When checked, the ISC DHCP daemon will ignore denied clients rather than responding with a rejection message.

Note

This option is not compatible with high availability failover.

Ignore Client Identifiers:

When set, the DHCP server will not record a unique identifier (UID) in client lease data if present in the client DHCP request.

This option may be useful when a client can dual boot using different client identifiers but the same hardware (MAC) address.

With the Kea DHCP backend, if a client does not send correct and matching client identifier values for all of its requests, checking this box can avoid log messages such as `ALLOC_ENGINE_V4_DISCOVER_ADDRESS_CONFLICT` for lease database entries which are not actually conflicting.

Note

This server behavior violates the official DHCP specification.

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

Subnet:

A read-only field with the current subnet on this interface.

Subnet Range:

The range of available addresses inside the interface subnet, for reference and to help determine the desired range for DHCP clients. The network address and broadcast address are excluded, but interface addresses and Virtual IP addresses are not excluded.

Address Pool Range:

This defines the DHCP address range, also referred to as the Scope or Pool. This range can be as large or as small as the network needs, but it must be wholly contained within the subnet.

Addresses between the entered values, inclusive, will be used for clients which request addresses via DHCP.

From:

The starting address of the pool.

Must be lower than the **To** address.

To:

The ending address of the pool.

Must be higher than the **From** address.

Note

The default LAN DHCP range is based off of the subnet for the default LAN IP address. It is `192.168.1.100` to `192.168.1.199`.

### Additional Pools

The **Additional Pools** section defines extra pools of addresses inside the same subnet. These pools can be used to craft sets of IP addresses specifically for certain clients, or for overflow from a smaller original pool, or to split up the main pool into smaller chunks with a GAP of non-DHCP IP addresses in the middle of what used to be the pool. A combination of the MAC Address Control options may be used to guide clients from the same manufacturer into a specific pool, such as VoIP phones.

To add a new pool, click **Add Address Pool** and the screen will switch to the pool editing view, which is nearly the same as the normal DHCP options, except a few options that are not currently possible in pools are omitted. The options behave the same as the others discussed in this section. Items left blank will, by default, fall through and use the options from the main DHCP range.

Note

See the MAC Address Control section below for specifics on directing clients into or away from pools.

## Server Options

WINS Servers:

Defines up to two WINS Servers (Windows Internet Name Service) which the server provides to clients.

Note

WINS is deprecated, but still active on some legacy networks.

DNS Servers:

Defines up to four DNS server IP addresses which the server provides to clients. To use custom DNS Servers instead of automatic choices, fill in the DNS server IP addresses.

Tip

When using the DNS Resolver or DNS forwarder in combination with high availability clustering, specify a CARP Virtual IP address on this interface as the only DNS server.

When left empty, the firewall will automatically determine which addresses to supply to clients depending on the DNS configuration on this firewall:

-   If the firewall is using the built-in DNS Resolver or DNS Forwarder to handle DNS, leave these fields blank. It will automatically assign itself as the DNS server for client devices.
-   If the DNS Resolver or Forwarder is disabled and these fields are left blank, the firewall will pass on whichever DNS servers are defined under **System > General Setup**.

Tip

In networks with Windows servers, especially those employing Active Directory, the best practice is to use those servers for client DNS.

## OMAPI (ISC Only)

Options for OMAPI service provided by the DHCP server, which allows querying and controlling the DHCP server remotely.

OMAPI Port:

Set the port that OMAPI will listen on. The default port is `7911`, leave blank to disable.

Only the first OMAPI configuration is used, configurations on other interface tabs are ignored.

OMAPI Key:

Enter a key matching the selected **Key Algorithm** to secure connections to the OMAPI endpoint.

Generate New Key:

When checked, generates a new key based on the selected algorithm when the settings are saved.

Key Algorithm:

The algorithm used to generate the OMAPI key.

## Other DHCP Options

Gateway:

This may also be left blank if this firewall is acting as the gateway for the network on this interface. If that is not the case, fill in the IP address for the gateway to be used by clients on this interface. When using CARP, fill in the CARP Virtual IP address on this interface here.

Domain Name:

Specifies the domain name passed to the client to form its fully qualified hostname. If the **Domain Name** is left blank, then the domain name of the firewall it sent to the client. Otherwise, the client is sent this value.

Domain Search List:

Controls the DNS search domains that are provided to the client via DHCP. If multiple domains are present and short hostnames are desired, provide a list of domain names here, separated by a semicolon. Clients will attempt to resolve hostnames by adding the domains, in turn, from this list before trying to find them externally. If left blank, the Domain Name option is used.

Note

The **Domain Search List** is provided via DHCP option `119`. Compatibility with this option varies by Operating System and version. See [Using DHCP Search Domains on Windows DHCP Clients](client-search-domain.html).

Default lease time:

Controls how long a lease will last when a client does not request a specific lease length. Specified in seconds, default value is `7200` seconds (2 hours)

Maximum lease time:

Limits a requested lease length to a stated maximum amount of time. Specified in seconds, default value is 86400 seconds (1 day).

Failover Peer IP (ISC Only):

If this firewall is part of a High Availability failover cluster, enter the real IP address of the other node in this subnet here.

Do not enter a CARP Virtual IP address.

Note

When **Failover Peer IP** is configured in a High Availability setup, the failover node should be available when the service is started to allow lease pool information to be synchronized; failing this, the DHCPD service will not respond to DHCPDISOVER requests.

Static ARP (ISC Only):

This checkbox works similar to denying unknown MAC addresses from obtaining leases, but takes it a step further in that it also restricts any unknown MAC address from communicating with this firewall. This stops would-be abusers from hardcoding an unused address on this subnet, circumventing DHCP restrictions.

Note

When using static ARP, all systems that need to communicate with the firewall must be listed in static mappings before activating this option, especially the system being used to connect to the firewall GUI. Also be aware that this option may prevent people from hardcoding an IP address and talking to the firewall, but it does not prevent them from reaching each other on the local network segment.

Time Format Change (ISC Only):

By default, the ISC DHCP daemon maintains lease times in UTC. When this option is checked, the times on the DHCP Leases status page are converted to the local time zone defined on the firewall.

Statistics Graphs (ISC Only):

This option, disabled by default, activates RRD graphing for monitoring the DHCP pool utilization.

Ping Check (ISC Only):

When checked, the DHCP server will attempt to ping a client address before allocation to ensure it is not in use by another device.

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

## MAC Address Control

For MAC Address Control, click **Display Advanced** to show the lists of allowed and denied client MAC addresses. Each list is comma-separated and contains portions of MAC addresses. For example, a group of VoIP phones from the same manufacturer may all start with the MAC address `aa:bb:cc`. This can be leveraged to give groups of devices or users separate DHCP options.

Allow:

A list of MAC Addresses to allow in this pool. If a MAC address is in this text box, then all others will be denied except the MAC address specified here.

Deny:

A list of MAC Addresses to deny from this pool. If a MAC address is in this list, then all others are allowed.

The best practice is to use a combination of these lists to get the desired result, such as: In the main pool, leave **Allow** blank and set **Deny** to `aa:bb:cc`. Then in the VoIP pool, allow `aa:bb:cc`. If that extra step is not taken to allow the MAC prefix in the additional pool, then other non-VoIP phone clients could receive IP addresses from that pool, which may lead to undesired behavior.

This behavior may also be used to prevent certain devices from receiving a DHCP response. For example to prevent Example brand printers from receiving a DHCP address, if MAC addresses all start with `ee:ee:ee`, then place that in the deny list of each pool.

## NTP Servers

To specify NTP Servers (Network Time Protocol Servers), click the **Display Advanced** button to the right of that field, and enter IP addresses for up to four NTP servers.

## TFTP Server

Click the **Display Advanced** button next to **TFTP** to display the TFTP server option. The value in the TFTP Server box, if desired, must be an IP address or hostname of a TFTP server. This is most often used for VoIP phones, and may also be referred to as "option 66" in other documentation for VoIP and DHCP.

## LDAP URI

Click the **Display Advanced** button next to **LDAP** to display the **LDAP Server URI** option. **LDAP Server URI** will send an LDAP server URI to the client if requested. This may also be referred to as DHCP option 95. It takes the form of a fully qualified LDAP URI, such as `ldap://ldap.example.com/dc=example,dc=com`. This option can help clients using certain kinds of systems, such as Open Directory, to find their server.

## Network Booting

These options control how the DHCP server will direct clients to boot over the network (e.g. PXE).

Warning

Both a filename and a boot server must be configured for this to function properly. For UEFI & ARM to boot properly, all five filenames and a configured boot server are required.

Enable:

Enables Network Booting options for DHCPv4.

Next Server:

The IPv4 address from which boot images are available.

Default BIOS File Name:

Filename to use when a client does not specify an architecture, such as for legacy BIOS booting.

UEFI 32 bit File Name:

Filename to supply for 32-bit UEFI clients.

UEFI 64 bit File Name:

Filename to supply for 64-bit UEFI clients.

ARM 32 bit File Name:

Filename to supply for 32-bit ARM clients.

ARM 64 bit File Name:

Filename to supply for 64-bit ARM clients.

UEFI HTTPBoot URL:

URL to boot files for clients capable of booting using the HTTPBoot method. Must be in the format `http://<server-name>/<firmware-path>`.

Root Path:

String to target a specific device as the client's root filesystem device, such as `iscsi:<server-name>:<protocol>:<port>:<LUN>:<target-name>`.

## Custom Configuration (KEA Only)

The KEA GUI allows administrators to configure Kea directly with JSON-formatted configuration blocks. See [Custom Configuration](kea-settings.html#kea-custom-config) for details.

## Additional BOOTP/DHCP Options (ISC Only)

Other numeric DHCP options can be sent to clients using the **Additional BOOTP/DHCP Options** controls. To view these options, click **Display Advanced** in this section. To add a new option, click **Add Custom Option**.

Number:

The DHCP option code number. IANA maintains a [list of all valid DHCP options](https://www.iana.org/assignments/bootp-dhcp-parameters/bootp-dhcp-parameters.xml).

Type:

The choices and formats for each type may be a little counter-intuitive, but the labels are used directly from the DHCP daemon.

The proper uses and formats are:

Text:

Free-form text to be sent in reply, such as `http://www.example.com/wpad/wpad.dat` or `Example Company`.

String:

A string of hexadecimal digits separated by a colon, such as `c0:a8:05:0c`.

Boolean:

Either `true` or `false`.

Unsigned 8, 16, or 32-bit Integer:

A positive Integer that will fit within the given data size, such as `86400`.

Signed 8, 16, or 32-bit Integer:

A positive or negative Integer that will fit within the given data size, such as `-512`.

IP address or host:

An IP address such as `192.168.1.1` or a hostname such as `www.example.com`.

Value:

The value associated with this numeric option and type.

For more information on which options take a specific type or format, see the linked list above from the IANA.

Note

When using numbered custom options, be careful of the type. Some will be OK on text/string, but others are not.

For example, DHCP options for code `132` (and presumably `133`) for VLAN ID must be set for a type of unsigned integer `32`.

## Save Settings

After making changes, click **Save** before attempting to create static mappings. Changes to settings will be lost if the browser leaves this page without saving.

## Static Mappings

Static DHCP mappings express a preference for which IP address will be assigned to a given client based on its MAC address. In a network where unknown clients are denied, this also serves as a list of "known" clients which are allowed to receive leases or have static ARP entries. Static mappings can be added in one of two ways:

-   From this screen, click **Add Static Mapping**.
-   From the DHCP leases view, click on a lease row.

On this screen, only the **MAC address** is necessary.

MAC Address:

The client MAC address which identifies a host. This can be used to deliver customized options on this page. Alternately, by entering only the MAC address it will be added to the list of known clients for use when the **Deny unknown clients** option is set.

Note

Client MAC address can be obtained from a command prompt on most platforms. On many UNIX-based or UNIX-work-alike operating systems including macOS, typing `ifconfig -a` will show the MAC address for each interface. On Linux, use `ip link`. On Windows, `ipconfig /all` will show the MAC address. The MAC address may also sometimes be found upon a sticker on the network card, or near the network jack for integrated adapters. For hosts on the same subnet, the MAC can be determined by pinging the IP address of the host and then running `arp -a`.

Client Identifier:

An optional ID sent by the client to identify itself as per [RFC 2132](https://www.rfc-editor.org/rfc/rfc2132.html#section-9.14). This is used for matching, similar to the MAC address, it does not set a value for the client.

IP Address:

The IP address field is needed if this will be a static IP address mapping instead of only informing the DHCP server that the client is valid.

This IP address is a **preference**, not a reservation. Assigning an IP address here will not prevent another host from using the same IP address. If the IP address is in use when this client requests a lease, the server will instead assign the client an address from the general pool. For this reason, the GUI does not allow assigning static mappings inside of pools.

See also

[Static Mappings Inside DHCP Pools](mappings-in-pools.html)

Hostname:

The hostname of the client. This does not have to match the hostname set on the client. The hostname set here will be used when registering DHCP addresses in the DNS resolver.

Description:

Cosmetic only, and available for use to help track any additional information about this entry. It could be the name of the person who uses the PC, its function, the reason it needed a static address, or the administrator who added the entry. It may also be left blank.

ARP Table Static Entry:

If checked, this entry will receive a static ARP entry in the OS tying this IP address to this MAC address.

Note

If this option is used rather than using the global static ARP option, it does not prevent that MAC address from using other IP addresses, it only prevents other MAC addresses from using this IP address. In other words, it prevents another machine from using that IP address to reach the firewall, but it doesn't stop the user from changing their own IP address to something different.

The remaining options available to set for this client are the same in behavior to the ones found earlier in this section for the main DHCP settings.

Click **Save** to finish editing the static mapping and return to the DHCP Server configuration page.
