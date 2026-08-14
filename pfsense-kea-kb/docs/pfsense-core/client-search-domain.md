---
source_url: https://docs.netgate.com/pfsense/en/latest/services/dhcp/client-search-domain.html
title: Using DHCP Search Domains on Windows DHCP Clients
category: pfsense-core
priority: 1
pfsense_version_notes:
fetched_date: 2026-08-13
converter: webfetch
---

# Using DHCP Search Domains on Windows DHCP Clients

The DNS Search Domain functionality present in the DHCP Server settings in pfSense® software is only implemented in some DHCP clients; pfSense software uses the standard DHCP option `119` mechanism to deliver the search domains to clients which request them.

Microsoft finally added the ability to utilize option `119` in Windows 10 version 1803 released in April 2018. Older versions of the Microsoft Windows DHCP client **do not** request option `119`, so no matter which DHCP server is used, clients running older versions of Microsoft Windows can never receive or use a search domain list from DHCP. Upgrade clients to a current Windows release to use this functionality.

Tip

If older clients must use these settings, and they cannot be upgraded, the setting can be pushed via GPO instead of DHCP.

Sources:

-   [https://docs.microsoft.com/en-us/windows-server/networking/technologies/dhcp/what-s-new-in-dhcp#new-dhcp-client-side-features-in-the-windows-10-april-2018-update](https://docs.microsoft.com/en-us/windows-server/networking/technologies/dhcp/what-s-new-in-dhcp#new-dhcp-client-side-features-in-the-windows-10-april-2018-update)
-   [http://social.technet.microsoft.com/Forums/en-US/winserverNIS/thread/9ba77f86-4708-42ca-a193-2a01b813ec27/](http://social.technet.microsoft.com/Forums/en-US/winserverNIS/thread/9ba77f86-4708-42ca-a193-2a01b813ec27/)
-   [http://social.technet.microsoft.com/Forums/en-US/winserverNIS/thread/7ba59619-3484-43fa-8585-a2d69ccd00df/](http://social.technet.microsoft.com/Forums/en-US/winserverNIS/thread/7ba59619-3484-43fa-8585-a2d69ccd00df/)
-   [http://technet.microsoft.com/en-us/library/dd572752%28v=office.13%29.aspx](http://technet.microsoft.com/en-us/library/dd572752%28v=office.13%29.aspx) (See comments)
-   [http://serverfault.com/questions/37417/which-dhcp-client-os-support-dhcp-option-119-domain-suffix-search](http://serverfault.com/questions/37417/which-dhcp-client-os-support-dhcp-option-119-domain-suffix-search)
