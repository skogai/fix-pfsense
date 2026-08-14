---
source_url: https://www.isc.org/dhcp_migration/
title: Migrating to Kea from ISC DHCP
category: upstream-kea
priority: 2
pfsense_version_notes:
fetched_date: 2026-08-13
converter: webfetch
---

# Migrating to Kea from ISC DHCP

Resources for System Administrators

### Kea Migration Assistant (KeaMA) tool

The [Kea Migration Assistant](https://dhcp.isc.org) is a tool that will partially translate a working configuration for ISC DHCP to an equivalent configuration for Kea. It is not possible to automatically translate the entire configuration, so the result will require some manual fix-ups. This tool is available [on-line](https://dhcp.isc.org), or you can download the [source code](https://gitlab.isc.org/isc-projects/keama), install a [package](https://cloudsmith.io/~isc/repos/keama/packages/), or run a [Docker](https://cloudsmith.io/~isc/repos/keama/packages/).

## Why Migrate?

ISC ceased maintaining ISC DHCP [in 2022](https://www.isc.org/blogs/isc-dhcp-eol/). The software may continue to work in your environment indefinitely, but at some point you will need to upgrade the operating system on the servers running dhcpd, and you may encounter problems. It is impossible to predict when this will happen, so it is important to develop a migration plan as soon as possible.

The [Kea DHCP server](https://www.isc.org/kea/) is a completely new design, which benefited from some lessons learned from supporting ISC DHCP for nearly three decades.

-   Many optional features are implemented as [hook libraries](https://kea.readthedocs.io/en/latest/arm/hooks.html), and the DHCPv4, DHCPv6, and Dynamic DNS applications are separate packages, so you need only install the software you plan to use.
-   The extensive [Kea API](https://kea.readthedocs.io/en/latest/arm/ctrl-channel.html) supports integration into your existing management systems and online reconfiguration.
-   Components that are frequently modified, such as host reservations and subnets, can optionally be stored in a common off-the-shelf database, separate from the main Kea configuration file, using [premium hooks](https://www.isc.org/shop/).
-   Kea supports a simpler [high availability](https://kea.readthedocs.io/en/latest/arm/hooks.html?highlight=high%20availability#ha-high-availability-outage-resilience-for-kea-servers) mode [in place of the DHCPv4 failover draft](https://kb.isc.org/docs/aa-01617) implemented by ISC DHCP. The Kea HA mode works equally well for both DHCPv4 and DHCPv6.
-   Kea is multi-threaded, and offers much [higher performance](https://reports.kea.isc.org) than ISC DHCP on modern computers.
-   There is an [Administrative Reference Manual](https://kea.readthedocs.io/en/latest/) for Kea (ISC DHCP just had man pages).
-   There is an open source monitoring and configuration tool, called [Stork](https://stork.isc.org), for Kea users.

Migration provides an opportunity to learn more about aspects of your network and your DHCP configuration that may not have been touched in a while. As a result, your configuration may become simpler and cleaner. Migration also gives you a chance to document the new configuration, something which can often get overlooked.

![A flock of birds in the sky, flying to the right](/images/chris-briggs-V72Hk6LjjjI-unsplash.jpg)

Photo by [Chris Briggs](https://unsplash.com/@cgbriggs19) on Unsplash

## Planning Your Migration

Ideally, the best time to undertake a migration is when you already have other changes going on, and it will be less disruptive to try something new. For example, if you have already planned major infrastructure changes, you are adding new office locations, switching to a new network server OS, or attempting to achieve new networked application security goals, any of those might present a good opportunity for migration.

Since migration can be a daunting process, ISC recommends several small- to mid-sized migrations over time rather than one large migration. One way to get a quick idea of how hard it might be for you to migrate, is to try our [**hosted KeaMA tool**](https://dhcp.isc.org) for translating an ISC DHCP dhcpd.conf file to a Kea configuration file. This doesn’t require any committment and is easy - and the result will indicate how straightforward migrating that DHCP server will be.

### Recommended Steps for a Successful Migration

1.  Review the current network design and DHCP configuration file(s).
2.  Set up an experimental Kea server in a non-production environment to familiarize yourself with the software.
3.  Review the [Kea documentation](https://kea.readthedocs.io/en/latest/) to decide whether you want to use any features implemented in hook libraries. Acquire any [premium hook libraries](https://www.isc.org/shop/) you plan to use.
4.  If you have a very simple deployment, take a look at our [template configuration for a single-site organization](https://kb.isc.org/docs/single-site-organization).
5.  Determine which segment of the network to migrate first. Frequently administrators will choose a network with fewer human users (e.g. a server segment) and fewer legacy devices, which may have non-standard requirements and behavior.
6.  Use the [**Kea Migration Assistant on-line**](https://dhcp.isc.org) or download and [run Kea Migration Assistant locally](https://gitlab.isc.org/isc-projects/dhcp/-/wikis/kea-migration-assistant) to prepare a rough initial configuration file for the new server from the existing ISC DHCP configuration file.
7.  Review and modify the configuration file produced by the tool, paying particular attention to the configuration of backup or load-balancing partner services, and client classification and option configuration. The Kea Migration Assistant will add log messages for any sections of the ISC DHCP configuration it could not translate: review the linked descriptions of differences between the two applications from your KeaMA log messages. Load the resulting candidate configuration into a Kea instance and run the configuration checkers to ensure you have a valid Kea configuration.
8.  Test the resulting Kea configuration in a non-production environment, using the software and OS versions you plan to deploy. ISC’s [perfdhcp](https://kea.readthedocs.io/en/kea-2.2.0/man/perfdhcp.8.html?highlight=perfdhcp) tool may be helpful for generating simulated client traffic for testing.
9.  Schedule the cutover for an off-peak, lower-traffic time and notify users (if that is your process).
10.  Translate your current valid DHCP leases into the Kea lease file format using the [KeaMA Lease tool](https://gitlab.isc.org/isc-projects/keama-leases). Load the resulting lease file into your target Kea server.
11.  Cutover by some combination of lowering the lease lifetimes for the devices that will be migrating, re-configuring your relays to relay to the new DHCP server, moving the subnets to be migrated to the new server, or entirely decommissioning the old server.
12.  Some more steps here (we don’t know everything!)
13.  Verification, documentation
14.  Rinse and repeat with other network segments

## Resources

The best resource is often other users. We highly recommend asking for advice on the [kea-users mailing list](https://lists.isc.org/mailman/listinfo/kea-users) and/or the [dhcp-users mailing list](https://lists.isc.org/mailman/listinfo/dhcp-users).

### Kea Configuration Differences

For a complete list of the known ISC DHCP configuration elements that do not translate cleanly to an equivalent Kea configuration, search in the [Kea project repository for issues tagged with the “migration” label](https://gitlab.isc.org/isc-projects/kea/-/issues/?sort=created_date&state=opened&label_name%5B%5D=migration&first_page_size=20).

The major configuration areas that will likely require redesign are the failover or high-availability solution, client classification, and host reservations. Kea has an alternative to the DHCPv4 failover draft implemented in ISC DHCP: the Kea feature is called “High Availability,” and it works equally well for both DHCPv4 and DHCPv6. Kea does support client classification, but there is no equivalent for ISC DHCP’s hyper-flexible permit/deny scripting language. The option inheritance hierarchy in Kea is different than in ISC DHCP, and the configuration for custom vendor-specific options is also different. Kea has robust support for host reservations, but it is different from ISC DHCP’s. In ISC DHCP all host reservations are global; in Kea, host reservations are by default per-subnet, although global host reservations are also supported.

The following Knowledgebase articles may help with understanding Kea functionality compared with ISC DHCP’s older features:

-   [Kea High Availability vs ISC DHCP Failover (comparison)](https://kb.isc.org/docs/aa-01617)
-   [Kea Configuration Introduction](https://kb.isc.org/docs/kea-configuration-sections-explained)
-   [Understanding Client Classification in Kea](https://kb.isc.org/docs/understanding-client-classification)
-   [Kea Logging for ISC DHCP Administrators](https://kb.isc.org/docs/isc-dhcp-logging-compared-to-kea)

### Kea Migration Assistant - DHCP Configuration

ISC has developed the [**Kea Migration Assistant**](https://dhcp.isc.org) (KeaMA) tool to make it easier for users to translate their configuration files from one format to the other. KeaMA is a branch of the legacy ISC DHCP server and is available in a [separate public repository](https://gitlab.isc.org/isc-projects/keama/-/blob/master/README.md). It takes the existing local ISC DHCP configuration and outputs it as a Kea JSON configuration. As mentioned above, some configuration elements cannot be translated by machine, and will require hand-editing. These are noted in the logs, with links to issues in ISC’s GitLab that explain the issue. See this KB article on [Migrating from ISC DHCP to Kea using the KeaMA tool](https://kb.isc.org/docs/migrating-from-isc-dhcp-to-kea-dhcp-using-the-migration-assistant).

Administrators need to run the tool once each for IPv6 and IPv4 configurations; KeaMA produces separate output files for each. KeaMA provides diagnostic messages when a direct translation is not available or possible, and provides a link to the related Kea GitLab issue.

The Kea Migration Assistant is included as part of the most recent ISC DHCP versions. It can be built from source or installed as a pre-compiled package from ISC’s package repository. There is also an experimental Docker file.

-   [Kea Migration Assistant packages](https://cloudsmith.io/~isc/repos/keama/packages/)
-   [Kea Migration Assistant sources](https://gitlab.isc.org/isc-projects/keama/-/blob/master/README.md)
-   [Kea Migration Assistant Dockerfile](https://cloudsmith.io/~isc/repos/keama/packages/)

### Kea Migration Assistant - Leases

This experimental Python script takes an ISC DHCP lease file as input, and outputs the same leases in the Kea lease file format. The leases then need to be loaded into the target Kea server. Note that depending on how much time elapses during this process, some of the leases may expire during the migration period. The 2023 video below includes a demonstration of the lease migration tool (scroll to the end of the recording for the demo).

-   [Kea Migration Assistant - leases repository](https://gitlab.isc.org/isc-projects/keama-leases)

### Video tutorials

ISC has conducted several webinars in an effort to help users migrating from ISC DHCP to Kea.

-   [Migrating to Kea from ISC DHCP - 2020](https://youtube.com/watch?v=kEZ4P3NAibI) This video, the 6th in a 2020 series on using the Kea DHCP server, focuses on how to migrate to Kea from ISC DHCP. Carsten Strotmann explains how to build and use the KeaMA configuration migration tool.
-   [Migrating to Kea from ISC DHCP - 2023](https://youtu.be/m-EchdH6_rA) This 2023 video focuses on the higher-level planning for a migration, and includes a demonstration of the lease migration tool.
-   [NANOG 88 Lightening talk/demo of the hosted Kea Migration Assistant](https://www.youtube.com/watch?v=AIbh5IcQfXo)
-   [Creating a Kea configuration from an ISC DHCP configuration - 2019](https://www.youtube.com/watch?v=V7CllOP4q2s) In this video, Alan Clegg covers using the KeaMA utility to create a Kea configuration from an ISC DHCP configuration.
-   [NANOG 76 talk on DHCP Migration to Kea](https://www.youtube.com/watch?v=2FMDAAF52sw)
