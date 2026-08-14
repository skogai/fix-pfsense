# Resolver vs Forwarder

pfSense ships **two** DNS services. Picking the right one (and the right *mode*
within the Resolver) is the single most consequential DNS decision on the box.

## The two daemons

| | DNS Resolver | DNS Forwarder |
|---|---|---|
| Daemon | `unbound` | `dnsmasq` |
| Default since | pfSense 2.3 (Resolver on by default) | legacy / optional |
| Role | validating, recursive, caching resolver **or** forwarder | caching forwarder |
| DNSSEC | native validator | not a validator |
| DNS over TLS | yes (encrypted upstream) | no |

Sources: [DNS Resolver](docs/pfsense-dns/resolver.md),
[DNS Forwarder](docs/pfsense-dns/forwarder.md),
[DNS](docs/pfsense-dns/dns-index.md).

## Resolver: two modes

The Resolver can run as either:

- **Resolver mode** — it answers queries itself by walking the authoritative
  hierarchy (root → TLD → authoritative), validating DNSSEC along the way, and
  caching results. No upstream server is involved.
- **Forwarding mode** — it sends every query to a configured upstream resolver
  (ISP, Quad9, Cloudflare, …) and caches their answers. It does **not**
  independently validate DNSSEC in this mode.

See [DNS Resolution Process](docs/pfsense-dns/resolution-process.md) for how a
query is routed depending on which service is enabled.

## DNSSEC semantics (the key distinction)

- A **validator** (Resolver in resolver mode) cryptographically checks signed
  zones and can reject spoofed/forged answers.
- A **forwarder** (Forwarder daemon, or Resolver in forwarding mode) trusts
  whatever the upstream returns. It is not a validator.

> **Rule of thumb:** if you need DNSSEC validation, run the Resolver in
> **resolver mode**. If you forward, DNSSEC validation is effectively delegated
> to (and dependent on) the upstream.

## When to pick which

- **Resolver mode** — best default. Maximum privacy/independence, DNSSEC
  validation, no third-party DNS metadata leakage. Use when you trust the
  root zone and want the firewall to resolve authoritatively.
- **Forwarding mode (Resolver)** — use when you must use an upstream that
  provides filtering (Quad9/Cloudflare/Microsoft), or your ISP requires you to
  use its resolver. Remember: DNSSEC must be **OFF** here (see
  [DNS over TLS](notes/dns-over-tls.md)).
- **DNS Forwarder (dnsmasq)** — only if you specifically need dnsmasq features
  (e.g. its DHCP integration, simple per-client behavior) or are migrating an
  older config. It cannot do DNS over TLS or DNSSEC validation.

## Gotchas

- Running **both** Resolver and Forwarder on the same port (53) conflicts —
  enable only one, or put them on different interfaces/ports.
- In forwarding mode, leave **DNSSEC off**; a validating forwarder against an
  upstream that doesn't support it produces resolution failures.
- The Resolver is the modern default and the one that supports DNS over TLS.

See also: [DHCP ↔ DNS Registration](notes/dhcp-dns-registration.md) for how
host entries reach each daemon.
