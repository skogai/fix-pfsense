# DNS Rebinding

DNS rebinding is an attack where a hostname initially resolves to a benign
public IP, then is re-resolved to a **private/localhost** IP to bypass
browser same-origin controls and reach internal services. pfSense protects
against this at the DNS layer.

## What the protection does

pfSense's DNS services can strip/block replies that return **RFC1918 (private)
IP addresses** for externally-resolved names, because a public hostname
normally should not resolve to an internal address. This stops a malicious
site from rebinding `evil.example.com` to `127.0.0.1` or `192.168.x.x` and
pivoting into your LAN.

Source: [DNS Rebinding Protections](docs/pfsense-dns/rebinding.md).

## The private-IP whitelist (the important knob)

The protection is too aggressive for legitimate setups, so pfSense lets you
**whitelist** domains that are allowed to return private IPs:

- **DNS Rebinding Protection** — global on/off.
- **Private IP Whitelist** (per-domain) — domains you explicitly trust to
  resolve to internal addresses (e.g. your own `*.home.arpa`, a NAS name, a
  reverse-proxy hostname). Add the domain here so its internal resolution is
  permitted.

Without the whitelist, legitimate internal-only hostnames reached via a public
DNS path will be blocked — a common cause of "my service won't resolve
internally but works by IP."

## Resolver vs Forwarder

Both the Resolver (Unbound) and Forwarder (dnsmasq) honor the rebinding
protection and the whitelist; the setting is configured per DNS service. The
[rebinding doc](docs/pfsense-dns/rebinding.md) covers the exact fields.

## Interaction with forwarding / DoT

When the Resolver forwards (including over DNS over TLS — see
[DNS over TLS](notes/dns-over-tls.md)), rebinding protection still applies to
the answers returned by the upstream. If your upstream resolver legitimately
returns private IPs for some names, whitelist those domains or you'll see
resolution failures for them.

## Gotchas

- Symptom "resolves by IP but not by name internally" → often a missing
  whitelist entry, not a DNS outage.
- Whitelist the domain, not the IP — rebinding protection keys on the name.
- Don't disable global protection to "fix" one host; whitelist the specific
  domain instead.
