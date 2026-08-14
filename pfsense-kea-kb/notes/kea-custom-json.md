# Kea Custom JSON → Kea Config-Section Mapping

pfSense® software lets administrators inject **custom JSON configuration snippets**
into the Kea DHCP backend. This is useful for features the GUI does not yet expose
(e.g. custom DHCP options, dynamic DNS, fine-tuned lease behavior, script hooks).

Primary sources:
- `docs/pfsense-core/kea-settings.md` (Custom Configuration section, mapping table)
- `docs/community/forum-custom-config-196513.md` (pfSense 25.03 examples & caveats)

## How the GUI maps snippets to Kea config sections

The Kea GUI presents custom-config fields on different pages. The system appends each
snippet to a **different top-level section** of the generated Kea configuration, based
on which page the field lives on (`docs/pfsense-core/kea-settings.md`):

| Kea GUI Page | Kea Configuration Section the snippet is merged into |
| --- | --- |
| DHCPv4 Settings | `Dhcp4` |
| DHCPv6 Settings | `Dhcp6` |
| DHCPv4/v6 interfaces (subnets) | `subnet` |
| DHCPv4/v6 Pools | `pool` |
| DHCPv4/v6 static mappings | `reservation` |

Key behaviors (`docs/pfsense-core/kea-settings.md`):
- Each snippet must be a **well-formed JSON object** and must **not** include the
  section name itself (the GUI adds it).
- Snippets are appended **after** the GUI-generated settings for that section, so
  they can both *enable new features* and *override* base configuration.
- The system **tests the configuration** before starting Kea. If the test fails with
  the custom snippet, it files a notice and attempts to start Kea **without** the
  custom snippet.

## Where the snippets live

The configuration snippets are stored in **`config.xml`**, so they are included in
backups and restored along with the rest of the Kea settings
(`docs/pfsense-core/kea-settings.md`). This means a config restore also restores your
custom JSON.

## Version caveat (community confirmation)

The `docs/community/forum-custom-config-196513.md` thread documents that the "Custom
Configuration" feature landed in **pfSense Plus 25.03** (later beta, not the early
public beta; earlier adopters needed Redmine patch #15321). Treat the exact JSON
syntax as **version-sensitive**.

### Example (from the forum thread)

Custom DHCP options on `Services / DHCP Server / Settings` (merges into `Dhcp4`):

```json
{
  "option-def": [
    { "name": "unifi", "code": 1, "space": "vendor-encapsulated-options-space", "type": "string" }
  ]
}
```

Per-interface options on `Services / DHCP Server / LAN` (merges into that interface's
`subnet`):

```json
{
  "option-data": [
    { "name": "v4-captive-portal", "data": "https://captiveportal.example.com:8003/index.php?zone=guest" }
  ]
}
```

The thread also notes that already-predefined Kea options (e.g. `v4-captive-portal`,
option 114) must **not** be redefined, and that script hooks can be placed at
`/cf/conf/kea4_scripts.d` and `/cf/conf/kea6_scripts.d`.
