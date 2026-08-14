---
source_url: https://kea.readthedocs.io/en/latest/arm/ha.html
title: Kea High Availability (HA) — Page Not Found (HTTP 404)
category: upstream-kea
priority: 1
pfsense_version_notes:
fetched_date: 2026-08-13
converter: webfetch
---

# Kea High Availability (HA) — HTTP 404

The upstream URL `https://kea.readthedocs.io/en/latest/arm/ha.html` returned an
**HTTP 404 (Not Found)** when fetched on 2026-08-13.

## What happened

In current Kea documentation (Kea 3.x), the standalone `arm/ha.html` page no
longer exists. High Availability is documented as part of the hooks reference
instead. The Kea Administrator Reference Manual table of contents now links HA
content under the hooks chapter (`arm/hooks.html`), specifically the
`libdhcp_ha.so` section: "High Availability, Outage Resilience for Kea Servers."

## Where to find the HA content instead

- HA hook library (`libdhcp_ha.so`) in the Kea ARM hooks chapter:
  `https://kea.readthedocs.io/en/latest/arm/hooks.html`
- HA quick-start guide (ISC Knowledgebase):
  `https://kb.isc.org/docs/kea-ha-quickstart-guide`
- HA vs ISC DHCP failover comparison (fetched in this KB as
  `kea-ha-vs-isc.md`): `https://kb.isc.org/docs/aa-01617`

## Recommendation

Use `kea-ha-vs-isc.md` and the Kea ARM hooks documentation for High
Availability content. This stub is retained to record the 404 and avoid a broken
reference in the knowledge base.
