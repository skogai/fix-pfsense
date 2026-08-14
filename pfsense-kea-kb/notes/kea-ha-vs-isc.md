# Kea HA vs ISC DHCP Failover

A synthesized comparison of how High Availability (failover) works under the **Kea**
DHCP backend versus the deprecated **ISC DHCP** backend in pfSense® software.

Primary sources:
- `docs/pfsense-ha/ha-kea-convert.md` (pfSense recipe, backend-difference table)
- `docs/upstream-kea/kea-ha-vs-isc.md` (ISC KB feature matrix)

## At a glance

| Aspect | Kea HA | ISC DHCP Failover |
| --- | --- | --- |
| HA style | **Hot Standby** — one node actively serves; standby takes over on failure | **Active/Active** — both nodes serve parts of each pool simultaneously |
| Node role | **Manual** primary/standby, set per node | Attempts **automatic** role detection via CARP VIP inspection (unreliable) |
| Secondary boots while primary offline | **Yes** — serves leases | **No** — needs to see primary first |
| DHCPv6 HA | **Yes** (plus RA XMLRPC sync) | **No** (IPv4 only) |
| HA configuration scope | **Global** per node (one set of settings) | **Per-interface** failover config |
| HA addresses | **One** address per node (best on the Sync interface) | **One** failover address **per interface** per node |
| HA transport | **IPv4 or IPv6** (either family works for DHCPv4 and DHCPv6) | **IPv4 only** |
| Copies hostnames between peers | **Yes** | **No** |
| Status granularity | **Per node** | **Per pool** |
| TLS encryption | **Optional** (encrypts HA traffic) | **None** |
| TLS / client-cert auth | **Optional** mutual TLS to authenticate peer | **None** |

## Operational implications

- **Single HA address (Sync iface).** Kea uses one HA address per node, typically
  the node's IP on the **Sync** interface. This is safer and simpler than ISC, which
  needs failover addresses and firewall rules on *every* DHCP-enabled interface
  (`docs/pfsense-ha/ha-kea-convert.md`). Only one firewall rule set (on Sync) is
  required for Kea.
- **TLS does not synchronize.** The optional TLS transport options are per-node and
  are explicitly excluded from XMLRPC configuration synchronization; each node needs
  its own certificate (`docs/pfsense-core/kea-settings.md`,
  `docs/pfsense-ha/ha-kea-convert.md`).
- **IPv4/IPv6 transport flexibility.** Kea can exchange HA data over IPv4 *or* IPv6
  peers for both DHCPv4 and DHCPv6 services; the address family of the HA link does
  not need to match the DHCP service family.
- **Hostnames replicate.** Kea's lease sync copies hostnames between peers; ISC's
  does not — relevant for DNS consistency after failover.
- **Per-node status.** Kea reports HA state globally per node with a heartbeat timer;
  ISC reports failover state per pool ("Failover Groups").

## Upstream nuance (from ISC KB)

The ISC KB feature matrix (`docs/upstream-kea/kea-ha-vs-isc.md`) adds detail beyond
the pfSense recipe:
- ISC supports a **flexible load-balance split** (e.g. 80/20, 60/40) and **pool
  rebalancing**; Kea uses a **fixed 50/50** split in load-balancing mode and does
  *not* rebalance pools (use Hot Standby to avoid the issue).
- Kea can include **unlimited backup servers** for lease replication and external
  consumers (e.g. IPAM) via its RESTful lease updates; ISC has no equivalent.
- Kea can use **database-backed** lease storage (MySQL/MariaDB, PostgreSQL) with
  native replication; ISC only uses flat lease files.
- Kea control is via **RESTful API**; ISC uses **OMAPI**.

## Migration note

HA/failover settings are **not** compatible between ISC and Kea. Converting is manual
and effectively means setting up Kea HA from scratch, though Kea's simpler model makes
it quick (`docs/pfsense-ha/ha-kea-convert.md`). ISC DHCP is deprecated and will be
removed, so converting to Kea is the recommended path.
