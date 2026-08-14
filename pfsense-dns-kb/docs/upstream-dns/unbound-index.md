---
source_url: https://unbound.docs.nlnetlabs.nl/en/latest/
title: Unbound by NLnet Labs — Unbound 1.25.2 documentation
category: upstream-dns
priority: 1
pfsense_version_notes: Unbound (DNS Resolver) upstream docs index
fetched_date: 2026-08-13
converter: bs4+html2text
---

# Unbound by NLnet Labs

Unbound is a validating, recursive, caching DNS resolver. It is designed to be fast and lean and incorporates modern features based on open standards.

NLnet Labs offers [professional support and consultancy services](https://www.nlnetlabs.nl/services/contracts/) with a service-level agreement. Community support is available via our [mailing list](https://lists.nlnetlabs.nl/mailman/listinfo/unbound-users).

Unbound runs on FreeBSD, OpenBSD, NetBSD, MacOS, Linux and Microsoft Windows, with packages available for most platforms. It is included in the standard repositories of most Linux distributions. Installation and configuration is designed to be easy. Setting up a resolver for your machine or network can be done with only a few lines of configuration.

This documentation is an [open source project](https://github.com/NLnetLabs/unbound-manual/) and is edited via text files in the [reStructuredText](http://www.sphinx-doc.org/en/stable/rest.html) markup language and then compiled into a static website/offline document using [Sphinx](http://www.sphinx-doc.org) and [ReadTheDocs](https://readthedocs.org/).

We always appreciate your feedback and improvements. You can submit an issue or pull request on the [GitHub repository](https://github.com/NLnetLabs/unbound-manual/issues), or post a message on the [Unbound users](https://lists.nlnetlabs.nl/mailman/listinfo/unbound-users) mailing list. All the contents are under the permissive Creative Commons Attribution 3.0 ([CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/)) license, with attribution to NLnet Labs.

Getting Started

  * [Installation](getting-started/installation.html)
    * [Installing with a Package Manager](getting-started/installation.html#installing-with-a-package-manager)
    * [Building from source/Compiling](getting-started/installation.html#building-from-source-compiling)
    * [Testing](getting-started/installation.html#testing)
  * [Configuration](getting-started/configuration.html)
    * [chroot Configuration](getting-started/configuration.html#chroot-configuration)
    * [Username Configuration](getting-started/configuration.html#username-configuration)
    * [Network Configuration](getting-started/configuration.html#network-configuration)
    * [Testing the setup](getting-started/configuration.html#testing-the-setup)
    * [Set up Remote Control](getting-started/configuration.html#set-up-remote-control)
    * [Set up Trust Anchor (Enable DNSSEC)](getting-started/configuration.html#set-up-trust-anchor-enable-dnssec)



Use Cases

  * [Resolver for Home Networks](use-cases/home-resolver.html)
    * [Setting up Unbound](use-cases/home-resolver.html#setting-up-unbound)
    * [Testing the resolver locally](use-cases/home-resolver.html#testing-the-resolver-locally)
    * [Setting up for a single machine](use-cases/home-resolver.html#setting-up-for-a-single-machine)
    * [Setting up for the rest of the network](use-cases/home-resolver.html#setting-up-for-the-rest-of-the-network)
    * [Testing the resolver from a remote machine](use-cases/home-resolver.html#testing-the-resolver-from-a-remote-machine)
    * [Where it all comes together](use-cases/home-resolver.html#where-it-all-comes-together)
  * [Local DNS (Stub) Resolver for a Single Machine](use-cases/local-stub.html)
    * [Configuring the Local Stub resolver](use-cases/local-stub.html#configuring-the-local-stub-resolver)



Core

  * [Downstream Proxy Support](topics/core/proxy.html)
    * [PROXYv2](topics/core/proxy.html#proxyv2)
  * [Serving Stale Data](topics/core/serve-stale.html)
    * [serve-expired](topics/core/serve-stale.html#serve-expired)
    * [RFC 8767](topics/core/serve-stale.html#rfc-8767)
    * [Conclusion](topics/core/serve-stale.html#conclusion)
  * [Performance Tuning](topics/core/performance.html)
    * [Configuration](topics/core/performance.html#configuration)
    * [Using Libevent](topics/core/performance.html#using-libevent)
    * [Forked Operation](topics/core/performance.html#forked-operation)
  * [Monitoring and Reporting](topics/core/monitoring.html)
    * [Configuration](topics/core/monitoring.html#configuration)
    * [Statistics with Munin](topics/core/monitoring.html#statistics-with-munin)
    * [Statistics with Cacti](topics/core/monitoring.html#statistics-with-cacti)



Privacy

  * [Aggressive NSEC](topics/privacy/aggressive-nsec.html)
    * [Introduction](topics/privacy/aggressive-nsec.html#introduction)
    * [NSEC (Next Secure) Records](topics/privacy/aggressive-nsec.html#nsec-next-secure-records)
    * [DNSSEC Signatures on Wildcard Records](topics/privacy/aggressive-nsec.html#dnssec-signatures-on-wildcard-records)
    * [Generating NODATA Answers](topics/privacy/aggressive-nsec.html#generating-nodata-answers)
    * [Generating NXDOMAIN Answers](topics/privacy/aggressive-nsec.html#generating-nxdomain-answers)
    * [Generating Wildcard Answers](topics/privacy/aggressive-nsec.html#generating-wildcard-answers)
  * [DNS-over-HTTPS](topics/privacy/dns-over-https.html)
    * [Implementation Details](topics/privacy/dns-over-https.html#implementation-details)
    * [Using DoH](topics/privacy/dns-over-https.html#using-doh)
    * [Metrics](topics/privacy/dns-over-https.html#metrics)
  * [DNS-over-QUIC](topics/privacy/dns-over-quic.html)
    * [Configuration](topics/privacy/dns-over-quic.html#configuration)
    * [Libraries](topics/privacy/dns-over-quic.html#libraries)
    * [Test](topics/privacy/dns-over-quic.html#test)
    * [Metrics](topics/privacy/dns-over-quic.html#metrics)



Filtering

  * [Tags and Views](topics/filtering/tags-views.html)
    * [Tags](topics/filtering/tags-views.html#tags)
    * [Views](topics/filtering/tags-views.html#views)
  * [Response Policy Zones](topics/filtering/rpz.html)
    * [Introduction](topics/filtering/rpz.html#introduction)
    * [RPZ Policies](topics/filtering/rpz.html#rpz-policies)
    * [RPZ Actions](topics/filtering/rpz.html#rpz-actions)
    * [How to use RPZ with Unbound](topics/filtering/rpz.html#how-to-use-rpz-with-unbound)



Developer

  * [Unbound Library Tutorial](developer/libunbound-tutorial/index.html)
    * [Resolve a Name](developer/libunbound-tutorial/resolve-a-name.html)
    * [Setup the Context](developer/libunbound-tutorial/setup-context.html)
    * [Examine the Results](developer/libunbound-tutorial/examine-results.html)
    * [Asynchronous Lookup](developer/libunbound-tutorial/async-lookup.html)
    * [Lookup from Threads](developer/libunbound-tutorial/lookup-threads.html)
    * [DNSSEC Validate](developer/libunbound-tutorial/dnssec-validate.html)
  * [Unbound for Python](developer/python-modules.html)
    * [Pyunbound](developer/python-modules.html#pyunbound)
    * [Pythonmod](developer/python-modules.html#pythonmod)
  * [Source Code Docs](developer/doxygen-docs.html)



Manual Pages

  * [unbound(8)](manpages/unbound.html)
    * [Synopsis](manpages/unbound.html#synopsis)
    * [Description](manpages/unbound.html#description)
    * [See Also](manpages/unbound.html#see-also)
  * [unbound-checkconf(8)](manpages/unbound-checkconf.html)
    * [Synopsis](manpages/unbound-checkconf.html#synopsis)
    * [Description](manpages/unbound-checkconf.html#description)
    * [Exit Code](manpages/unbound-checkconf.html#exit-code)
    * [Files](manpages/unbound-checkconf.html#files)
    * [See Also](manpages/unbound-checkconf.html#see-also)
  * [unbound.conf(5)](manpages/unbound.conf.html)
    * [Synopsis](manpages/unbound.conf.html#synopsis)
    * [Description](manpages/unbound.conf.html#description)
    * [File Format](manpages/unbound.conf.html#file-format)
    * [Example](manpages/unbound.conf.html#example)
    * [Section Clauses](manpages/unbound.conf.html#section-clauses)
    * [Including Files](manpages/unbound.conf.html#including-files)
    * [Server Options](manpages/unbound.conf.html#server-options)
    * [Remote Control Options](manpages/unbound.conf.html#remote-control-options)
    * [Stub Zone Options](manpages/unbound.conf.html#stub-zone-options)
    * [Forward Zone Options](manpages/unbound.conf.html#forward-zone-options)
    * [Authority Zone Options](manpages/unbound.conf.html#authority-zone-options)
    * [View Options](manpages/unbound.conf.html#view-options)
    * [Python Module Options](manpages/unbound.conf.html#python-module-options)
    * [Dynamic Library Module Options](manpages/unbound.conf.html#dynamic-library-module-options)
    * [DNS64 Module Options](manpages/unbound.conf.html#dns64-module-options)
    * [NAT64 Options](manpages/unbound.conf.html#nat64-options)
    * [DNSCrypt Options](manpages/unbound.conf.html#dnscrypt-options)
    * [EDNS Client Subnet Module Options](manpages/unbound.conf.html#edns-client-subnet-module-options)
    * [Opportunistic IPsec Support Module Options](manpages/unbound.conf.html#opportunistic-ipsec-support-module-options)
    * [Cache DB Module Options](manpages/unbound.conf.html#cache-db-module-options)
    * [DNSTAP Options](manpages/unbound.conf.html#dnstap-options)
    * [Response Policy Zone Options](manpages/unbound.conf.html#response-policy-zone-options)
    * [Memory Control Example](manpages/unbound.conf.html#memory-control-example)
    * [Files](manpages/unbound.conf.html#files)
    * [See Also](manpages/unbound.conf.html#see-also)
  * [unbound-host(1)](manpages/unbound-host.html)
    * [Synopsis](manpages/unbound-host.html#synopsis)
    * [Description](manpages/unbound-host.html#description)
    * [Examples](manpages/unbound-host.html#examples)
    * [Exit Code](manpages/unbound-host.html#exit-code)
    * [See Also](manpages/unbound-host.html#see-also)
  * [libunbound(3)](manpages/libunbound.html)
    * [Synopsis](manpages/libunbound.html#synopsis)
    * [Description](manpages/libunbound.html#description)
    * [Functions](manpages/libunbound.html#functions)
    * [Result Data structure](manpages/libunbound.html#result-data-structure)
    * [Return Values](manpages/libunbound.html#return-values)
    * [See Also](manpages/libunbound.html#see-also)
  * [unbound-control(8)](manpages/unbound-control.html)
    * [Synopsis](manpages/unbound-control.html#synopsis)
    * [Description](manpages/unbound-control.html#description)
    * [Commands](manpages/unbound-control.html#commands)
    * [Exit Code](manpages/unbound-control.html#exit-code)
    * [Set Up](manpages/unbound-control.html#set-up)
    * [Statistic Counters](manpages/unbound-control.html#statistic-counters)
    * [Extended Statistics](manpages/unbound-control.html#extended-statistics)
    * [Files](manpages/unbound-control.html#files)
    * [See Also](manpages/unbound-control.html#see-also)
  * [unbound-anchor(8)](manpages/unbound-anchor.html)
    * [Synopsis](manpages/unbound-anchor.html#synopsis)
    * [Description](manpages/unbound-anchor.html#description)
    * [Exit Code](manpages/unbound-anchor.html#exit-code)
    * [Trust](manpages/unbound-anchor.html#trust)
    * [Files](manpages/unbound-anchor.html#files)
    * [See Also](manpages/unbound-anchor.html#see-also)



Reference

  * [RFC Compliance](reference/rfc-compliance.html)
  * [History](reference/history/index.html)
  * [Docs To-Do List](reference/todo.html)



# Index

  * [Index](genindex.html)



