# DNS over TLS

DNS over TLS (DoT) encrypts DNS queries between pfSense and an upstream
resolver so intermediate parties cannot read them. On pfSense this is a
**DNS Resolver (Unbound) feature only** — the DNS Forwarder (dnsmasq) does not
support it.

## Two related but distinct ideas

1. **Encrypted upstream** — the Resolver forwards queries to an upstream over
   TLS instead of plaintext 53. Configured under **Services > DNS Resolver >
   General > DNS over TLS Servers** (or the "TLS Query Forwarding" option).
2. **DoT server on the firewall** — making the Resolver itself answer client
   queries over TLS (rare; mostly for roaming clients). The recipe focuses on
   #1.

Source: [Configuring DNS over TLS](docs/pfsense-guides/dns-over-tls.md),
[Blog: DNS over TLS with pfSense](docs/community/blog-dns-over-tls.md).

## How to enable (encrypted upstream)

- Enable the DNS Resolver.
- Enable **DNS Query Forwarding** (forwarding mode) — DoT is an upstream
  transport, so the Resolver must forward.
- Add a **DNS over TLS Server** entry: the upstream IP and port (usually 853),
  plus the provider's TLS hostname for certificate validation.
- Use a DNS resolver that supports DoT (Quad9 `9.9.9.9`, Cloudflare
  `1.1.1.1`, Google `8.8.8.8`, etc.).

## Version caveats (record these)

- **Resolver-only.** DNS over TLS is not available in the DNS Forwarder.
- **DNSSEC must be OFF in forwarding mode.** A validating forwarder against an
  upstream that doesn't return validated records breaks resolution. Turn
  DNSSEC off when you enable DoT forwarding. (See
  [Resolver vs Forwarder](notes/resolver-vs-forwarder.md).)

## The cert-validation gotcha (forum/155225)

A well-known Netgate forum thread
([pfSense Unbound DoT — additional setting needed](docs/community/forum-unbound-dot-cert.md))
documents a critical pitfall:

> If you configure the DoT upstream **without** setting the TLS **hostname**,
> Unbound will accept **any** certificate — the connection is encrypted but
> **not authenticated**. You are protected from passive eavesdroppers but not
> from an active MITM presenting a self-signed cert.

**Fix:** always populate the TLS **hostname** field to match the upstream's
certificate (e.g. `dns.quad9.net`, `cloudflare-dns.com`, `dns.google`). Without
it, DoT gives confidentiality but not authenticity. The companion thread
[Configure DoT in 2.4.4](docs/community/forum-dns-over-tls.md) walks through the
same setup.

## Verification

After enabling, confirm queries leave on 853/TCP (not 53/UDP) and that the
upstream cert validates. Use **Diagnostics > DNS Lookup** and a packet capture
on the WAN to confirm TLS rather than plaintext.

See also: [Resolver vs Forwarder](notes/resolver-vs-forwarder.md) for the
forwarding-mode trade-off, and [DNS Rebinding](notes/dns-rebinding.md) for the
private-IP whitelist that interacts with forwarded resolution.
