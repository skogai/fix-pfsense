# Kea DNS Registration (seamless DNS Resolver updates)

How the **Kea** DHCP backend registers client hostnames with the pfSense® DNS
Resolver, and how it differs from the old ISC DHCP behavior.

Primary source: `docs/pfsense-core/kea-settings.md` (Kea Settings Tab → DHCP Client
DNS Registration with the DNS Resolver).

## Seamless, no daemon restart

With Kea, pfSense software dynamically updates the DNS Resolver with client hostnames
**without restarting the Kea daemon**. DNS updates are seamless and non-disruptive
(`docs/pfsense-core/kea-settings.md`).

This is a deliberate improvement over the **ISC DHCP** implementation, where DNS
registration changes were disruptive (effectively required a daemon restart). Kea
avoids that.

## Domain fallback behavior

Kea DNS Registration respects the domain configured in the DHCP settings for an
interface or static mapping. If no domain is set on the DHCP lease, the resolver falls
back in this order (`docs/pfsense-core/kea-settings.md`):

1. The **DHCP lease's** domain (interface or static-mapping domain).
2. A configured **search domain**.
3. As a last resort, the **firewall's** configured domain name.

## HA peer sync

DNS updates are kept up to date **between High Availability failover peers**
(`docs/pfsense-core/kea-settings.md`). Combined with Kea HA's hostname replication
(see `notes/kea-ha-vs-isc.md`), this means a client's hostname remains resolvable
after a failover event.

## Controlling registration

Two global controls exist on the Kea Settings tab (`docs/pfsense-core/kea-settings.md`):

- **DNS Registration** — default behavior for all interfaces with DHCP enabled. When
  checked, Kea automatically registers hostnames from DHCP leases on all interfaces.
  Can be **overridden per-interface** in either direction.
- **Early DNS Registration** — when checked, Kea registers hostnames from **static
  mappings** at startup (so a client need not have DHCP enabled for its hostname to be
  resolvable). When unchecked, the hostname is only registered once the client
  requests a lease. This matches the old ISC default behavior of registering at
  startup. Also overridable per-interface.

Works for both **DHCPv4 and DHCPv6** lease data.
