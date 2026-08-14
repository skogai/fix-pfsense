---
source_url: https://docs.netgate.com/pfsense/en/latest/services/dns/resolution-process.html
title: DNS Resolution Process | pfSense Documentation
category: pfsense-dns
priority: 1
pfsense_version_notes: 
fetched_date: 2026-08-13
converter: bs4+html2text
---

# DNS Resolution Process¶

Every DNS query must be resolved. Depending on which DNS service is in use on the firewall and its configuration, this resolution may happen locally, or it may happen on an upstream forwarding server. The [DNS Resolver](resolver.html) can act in either a resolver or forwarder role, while the [DNS Forwarder](forwarder.html) can only act as a forwarder.

Note

Some of the concepts and processes in this document are simplified to make them easier to understand.

## Terms¶

The terms used in this section have specific meanings, though some terms are frequently used interchangeably or in ambiguous ways. The following definitions cover roles involved in DNS resolution and how they process queries.

Client:
    

A device that wants to translate a hostname into an IP address. This could be a PC, handheld device, a server, etc.

A client will typically be configured with one or more forwarding DNS servers to which it will send DNS queries.

DNS Server:
    

A server involved in handling DNS queries. The term “DNS server” is ambiguous because a server involved in DNS can act in one or more specific roles which differ significantly. Used generally, this may refer to servers handling unknown or multiple types of DNS queries.

The term “DNS Server” can also vary based on context. When talking about clients it usually refers to upstream forwarders or resolvers. When talking about resolvers or DNS infrastructure it usually refers to authoritative DNS servers. Where possible, it is best to use a more specific term.

Forwarder:
    

A forwarder is a type of DNS server which accepts recursive queries from clients and makes its own queries to an upstream DNS server, which could be another forwarder or a resolver. A forwarder will typically cache results, so clients get faster responses for frequently resolved queries.

Note

A forwarder does not perform DNS resolution itself, it passes a query along to another forwarder or resolver unless it has the answer in its cache.

Resolver:
    

A DNS server acting as a resolver will accept recursive queries from clients and/or forwarders and perform DNS resolution by making iterative queries to root and authoritative DNS servers in search of an answer. Like a forwarder it will typically cache results for increased performance.

A resolver maintains a list of root servers in its “root hints” list. Resolvers will typically ship with a stock list but update it periodically from a trusted source.

Root Server:
    

Authoritative name servers which serve queries for the DNS root zone (`.`). Though it is held as a short list of servers (`a.root-servers.net` through `m.root-servers.net`) there are hundreds of servers worldwide handling the requests.

These servers are a starting point for queries and will direct resolvers to authoritative DNS servers for zones which can answer their queries.

Glue Records:
    

Entries in domain name registries which associate specific authoritative DNS servers with a domain name. These are used by the DNS servers for a TLD to determine which servers are authorized to answer queries for a given domain name.

Authoritative Server:
    

A name server which has direct knowledge of hosts in a zone and the proper responses for queries. This could be for one or more domain names, subdomains, and so on. It could be run by a company operating a domain directly, a dedicated DNS provider, or a hosting company on their behalf.

An authoritative server will not make queries of its own to locate an answer. Instead, it will either respond with a direct answer to the query or point the resolver to another authoritative server.

Recursive Query:
    

A query for which the answer is not local to the forwarder or resolver. A forwarder or resolver will in turn make a query to another server to obtain an answer.

It is recursive in that if a forwarding server does not know the answer the _forwarding server_ makes a recursive query to another upstream forwarder or resolver to obtain the answer, which is then passed back to a client. The client and every forwarder involved each only make one query upstream until the query eventually reaches a resolver.

Recursive queries can be handled by forwarders or resolvers.

Iterative Query:
    

A query where a resolver asks a root or authoritative server for either a direct answer or for information about how to find the answer.

If the response points the resolver to another authoritative server, the _resolver_ will send an additional query to that server. This process is repeated until the resolver obtains a final answer from an authoritative server. The answer is then passed back to the host which queried the resolver.

This process is iterative, rather than recursive, as each query is performed by the resolver and the _resolver_ takes further action depending upon the result. The authoritative servers do not make queries of their own, they only give answers they know locally which may be the answer to a query or a pointer to another source.

## DNS Resolution Steps¶

This is a somewhat simplified version of the process that takes place when a client attempts to resolve a hostname.

  * The client checks its own DNS configuration to see how it should handle queries. This typically involves a local `hosts` file and a list of servers which it will contact to resolve queries.

Note

Some operating systems use additional methods for resolving names which are not a part of this process, such as mDNS or NBNS. These methods are omitted from this document but may occur before clients contact remote DNS servers. Check the operating system documentation for details.

Local DNS configuration on the client may also include a default domain name which it will append to hostnames to form a fully qualified domain name (FQDN) for a DNS query.

  * The client looks in its own `hosts` file to see if a local answer exists. If it does, the answer is used. If it does not, it proceeds to the next step.

  * The client contacts the first server in its list and sends a query. If it does not receive a response, it will query the next server in the list.

The client does not need to know or care if this server is a forwarder or resolver. Either way it gets an answer to its query.

  * If the server contacted by the client is a forwarder, the forwarder will make a query to one of its own configured upstream DNS servers.

As with a client these upstream servers could be additional forwarders or resolvers. If the upstream server is a forwarder, this step is repeated recursively until the query reaches a resolver.

  * Once the query reaches a resolver, the resolver attempts to track down the answer by making iterative queries to servers in an attempt to track down a definitive answer.

  * The resolver consults its list of [root DNS servers](https://www.iana.org/domains/root/servers) in the hints file and contacts one to locate information on how to proceed.

  * The resolver asks a root DNS server for information about the top level domain (TLD) in the requested FQDN (e.g. `.com`).

  * The root DNS server returns a list of authoritative servers which have information about the TLD.

  * The resolver queries one of the TLD servers from the response to ask about the domain name.

  * The TLD servers consult glue records under the TLD to locate one or more authoritative DNS servers which can answer queries for the domain.

  * The TLD server returns the list of authoritative DNS servers to the resolver.

  * The resolver contacts one of the authoritative DNS servers for a domain and asks for a response to the original query.

If the query is for an FQDN in a subdomain this may result in more steps as the authoritative server may tell the resolver to contact a different authoritative server which has knowledge of the subdomain. This process will be repeated until the resolver reaches the authoritative server with the answer to the query.

  * The authoritative DNS server for the domain or subdomain responds to the resolver with the answer to the query.

  * The resolver passes the response back to the host which submitted the request. The resolver may opt to cache the response.

  * If the request came from a forwarder, it is passed back again to the host which submitted the request. The forwarder may opt to cache the response.

If multiple forwarding servers were involved in the query this step is repeated until it reaches the original source of the query.

  * The response to the query arrives back at the client.




All of this can happen quite fast. Even with multiple servers involved the entire process can be completed in fractions of a second.
