---
source_url: https://docs.netgate.com/pfsense/en/latest/services/dhcp/mappings-in-pools.html
title: Static Mappings Inside DHCP Pools
category: pfsense-core
priority: 1
pfsense_version_notes:
fetched_date: 2026-08-13
converter: webfetch
---

# Static Mappings Inside DHCP Pools

While the ISC DHCP daemon will allow a static mapping to be defined inside the DHCP range/pool in its configuration, doing so can result in unexpected behavior.

A static mapping entry in the ISC DHCP daemon **is not** a reservation, and it **does not** remove that IP address from the pool. The daemon only checks via ICMP ping to ensure that an IP address is not actively in use when making assignments. The static mapping only represents a *preference* for IP address assignment, and it **does not** prevent the daemon from assigning the IP address to other client devices when it is not actively in use by the intended device defined in the static mapping.

Example: The DHCP configuration contains a pool from `192.168.0.10` to `192.168.0.250` with a static mapping defined for `192.168.0.25`. If the device which normally has `192.168.0.25` is ever offline another device could be assigned `192.168.0.25` in its absence. When the original client device reconnects it will not be able to get `192.168.0.25` because it is currently in use, and will instead receive another random address from the pool.

Due to this behavior the best practice is to **only** make assignments **outside** the range/pool and the GUI enforces this practice.

If a use case requires assignments inside the pool and the administrators do not care about the risks involved and want to do so anyway, the input validation check can be removed from the PHP file that drives the DHCP editor page. The details of this change will not be covered in documentation.
