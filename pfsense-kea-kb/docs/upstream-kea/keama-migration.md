---
source_url: https://kb.isc.org/docs/migrating-from-isc-dhcp-to-kea-dhcp-using-the-migration-assistant
title: Migrating from ISC DHCP to Kea DHCP using the Migration Assistant
category: upstream-kea
priority: 1
pfsense_version_notes:
fetched_date: 2026-08-13
converter: webfetch
---

# Migrating from ISC DHCP to Kea DHCP using the Migration Assistant

#### Migration is hard – so why do it?

ISC announced in 2022 that it was [no longer maintaining ISC DHCP](https://www.isc.org/blogs/isc-dhcp-eol/). Users of the ISC DHCP server should consider migrating to another software system before their DHCP deployment stops working. At some point, a version for your current operating system may no longer be available, or it may no longer work. We recommend planning for a migration off of the EOL dhcpd before that happens.

Migration is also an opportunity to learn more about aspects of your network and your DHCP configuration that may not have been touched in a while. As a result, your configuration may become simpler and cleaner. Migration also gives you a chance to document the new configuration, something which can often get overlooked.

Since migration can be a daunting process, ISC recommends several small- to mid-sized migrations over time rather than one large migration.

#### When is the best time to migrate?

Ideally, the best time to undertake a migration is when you already have other changes going on, and it will be less disruptive to try something new. For example, if you have already planned major infrastructure changes, you are already adding new office locations, or your existing infrastructure is reaching its End of Life, it may make sense to use those changes as an opportunity to migrate.

#### How should I start the migration from ISC DHCP to Kea?

First, begin by documenting and reviewing your existing configuration.

Then, evaluate the different Kea options. Kea offers several features that are not available in ISC DHCP, such as the ability to use database backends, high availability, and IPv6 deployment. Read about the options and decide which ones are likely to be most useful for your environment. Full details about all the features available in Kea can be found on our website, at [https://www.isc.org/kea](https://www.isc.org/kea) or in the [Kea Administrator Reference Manual](https://kea.readthedocs.io/en/latest/index.html).

#### So how do I migrate from ISC DHCP to Kea DHCP?

1. It is, of course, possible to rewrite the configuration file manually; however, ISC has developed the Kea Migration Assistant (or "KeaMA") tool to make it easier for users to translate their configuration files from one format to the other. (See below for more details about KeaMA.)
2. Once you have a working Kea configuration file, it is essential to test it in a lab environment for both functionality and performance.
3. When your lab testing is complete, you can migrate the leases. An [experimental lease migration tool](https://gitlab.isc.org/isc-projects/keama-leases) is available for this purpose.
4. Finally, perform the cutover to Kea. We recommend enabling small pieces at a time, during off-hours, to minimize end-user disruption.

There are several important differences between ISC DHCP and Kea, which you will need to consider as you plan and execute your migration:

1. Server failover, which was available in ISC DHCP, is not implemented in Kea. The Kea High-Availability hooks library offers similar functionality if that is a desired feature for your organization. There is a [knowledgebase article](/v1/docs/aa-01617) that specifically compares the Kea vs ISC DHCP failover functionality in depth.
2. Option inheritance scoping is different between ISC DHCP and Kea, so administrators will need to manage that difference.

There are also several new Kea features that you may want to implement:

1. **Configuration backend**, which offers the ability to store configurations in a database and apply them to servers from there, instead of locally on each server.
2. **Host reservations** used to be kept in a leases file or DHCP configuration, but now can be stored in a database backend.
3. A **lease database** was previously stored in logfile format, with new leases added to the end; Kea now allows you to keep leases in a database for simplified management.

#### So what does the Kea Migration Assistant do?

KeaMA, the Kea Migration Assistant, is a branch of the legacy ISC DHCP server that takes the existing ISC DHCP configuration language and outputs it as a Kea JSON configuration. The project repository is available in the DHCP code tree at [https://gitlab.isc.org/isc-projects/dhcp/tree/master/keama](https://gitlab.isc.org/isc-projects/dhcp/tree/master/keama).

Administrators need to run it once each for IPv6 and IPv4 configurations; KeaMA produces separate output files for each.

KeaMA provides diagnostic messages when a direct translation is not available or possible, and provides a link to the [related Kea GitLab issue.](https://gitlab.isc.org/isc-projects/kea/-/milestones/6) For example, in the image below, the error message (indicated here in red) refers the user to GitLab issue #245 for additional information.

![image.png](https://cdn.document360.io/956e37e2-5ec0-4942-8b27-35533899f099/Images/Documentation/image%2826%29.png)

Many issues can be resolved by just looking at the error message and reference number that come up in KeaMA; however, there are some configuration options that don’t translate directly from ISC DHCP to Kea, and which will need to be addressed manually.

The new Kea configuration file will be more verbose than the old ISC DHCP one. Kea MA can handle ISC DHCP configurations with multiple include files.

Basic compile/run instructions for KeaMA may be found at [https://gitlab.isc.org/isc-projects/dhcp/tree/master/keama](https://gitlab.isc.org/isc-projects/dhcp/tree/master/keama). Note that KeaMA is also provided as a package in ISC's [Cloudsmith repository](https://cloudsmith.io/~isc/repos/keama/packages/). e.g. `curl -1sLf \ 'https://dl.cloudsmith.io/public/isc/keama/setup.rpm.sh' \ | sudo -E bash`

### Webinars

ISC has conducted several webinars on the topic of migrating from ISC DHCP to Kea. Recordings are available on the [ISC YouTube channel](https://www.youtube.com/@ISCdotorg/videos)

[2020 webinar by Carsten Strotman](https://youtu.be/kEZ4P3NAibI) [2019 webinar by Alan Clegg](https://www.youtube.com/watch?v=V7CllOP4q2s).

## Related

- [Kea High Availability vs ISC DHCP Failover](/aa-01617.md)
