# DHCP ↔ DNS Registration

How do hostnames on your network end up resolvable through the firewall's DNS?
There are two mechanisms, and they behave differently between the Resolver and
the Forwarder.

## Two sources of local names

1. **Static Host Overrides** — manually defined A/AAAA/CNAME records you enter
   by hand. Available in both the Resolver
   ([Host Overrides](docs/pfsense-dns/forwarder-overrides.md)) and the
   Forwarder. These always win and are not learned dynamically.
2. **DHCP registration** — when a client gets a lease, the firewall can
   automatically register that client's name into DNS.

Source: [Host / Domain Overrides](docs/pfsense-dns/forwarder-overrides.md),
[DNS Resolver](docs/pfsense-dns/resolver.md).

## Resolver vs Forwarder behavior

- **DNS Resolver (Unbound):** register DHCP leases into the Resolver when the
  option is enabled; leases appear as local data. Host Overrides are merged on
  top.
- **DNS Forwarder (dnsmasq):** dnsmasq has tight DHCP↔DNS integration and will
  serve leased hostnames directly; Host Overrides are configured separately.

The exact toggle lives in the DHCP server settings ("Register DHCP leases in
DNS") and/or the DNS service's own "Register DHCP static mappings" option.

## Host Overrides vs DHCP registration

| | Source | Survives lease expiry? | Editable per-record? |
|---|---|---|---|
| Host Override | manual | yes (static) | yes |
| DHCP registration | lease | no (expires with lease) | no (automatic) |

Use **Host Overrides** for servers/printers/infrastructure you must always
resolve. Let **DHCP registration** cover laptops/phones that come and go.

## Cross-link: Kea DHCP

The DHCP server that hands out the leases is now **Kea** (see the sibling
`../pfsense-kea-kb/`). Its note on how Kea registers names into DNS is the
authoritative companion to this one:

- [Kea DHCP ↔ DNS registration](../pfsense-kea-kb/notes/kea-dns-registration.md)

The short version: Kea emits lease events; the DNS service (Resolver or
Forwarder) consumes them to populate local records. If registration isn't
working, check (a) the "Register DHCP leases" option is on in **both** the DHCP
server and the DNS service, and (b) the two services are actually running.

## Gotchas

- If both Resolver and Forwarder are enabled, only the active one serves the
  registered names — pick one as the LAN resolver.
- Host Overrides take precedence over (and can shadow) DHCP-registered names.
- Domain Overrides (forwarding specific domains to specific servers) are a
  third, separate mechanism — see
  [Host / Domain Overrides](docs/pfsense-dns/forwarder-overrides.md).
