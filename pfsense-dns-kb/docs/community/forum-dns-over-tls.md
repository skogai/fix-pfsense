---
source_url: https://forum.netgate.com/topic/136076/how-to-configure-dns-over-tls-in-2-4-4
title: How to configure DNS over TLS in 2.4.4? | Netgate Forum
category: community
priority: 3
pfsense_version_notes: Forum: DNS over TLS discussion (DNSSEC vs forwarding)
fetched_date: 2026-08-13
converter: bs4+html2text
---

Your browser does not seem to support JavaScript. As a result, your viewing experience will be diminished, and you have been placed in **read-only mode**. 

Please download a browser that supports JavaScript, or enable it if it's disabled (i.e. NoScript). 

[ Introducing Netgate Nexus: Multi-Instance Management at Your Fingertips. ](https://www.netgate.com/nexus)

# 

How to configure DNS over TLS in 2.4.4?

__Scheduled __Pinned __Locked [ __Moved](/category/) [ __DHCP and DNS](/category/19/dhcp-and-dns)

__ 5 Posts __ 3 Posters __ 1.6k Views __ 4 Watching

[__](/topic/136076.rss)

Loading More Posts __

__

  * Oldest to Newest __
  * Newest to Oldest __
  * Most Votes __



[__Reply](/compose?tid=136076)

  * Reply as topic



[Log in to reply](/login)

This topic has been deleted. Only users with topic management privileges can see it.

  * [ ![wgstarks](/assets/uploads/profile/uid-99522/99522-profileavatar.jpeg)W Offline ](/user/wgstarks)

** [wgstarks](/user/wgstarks) **

__ last edited by wgstarks  [](/post/792640) __

  


I've read [the Netgate blog post regarding enabling this feature in 2.4.3](https://www.netgate.com/blog/dns-over-tls-with-pfsense.html). At the end of the post it states that custom options will not be necessary in 2.4.4. Not exactly sure what is necessary though.

I entered the Cloudflare and Quad9 servers in DNS Server settings.

![alt text](http://i67.tinypic.com/wwmfeh.jpg)

I'm a little vague on what the check for DNS Resolver settings though.

![alt text](http://i63.tinypic.com/imv4pf.jpg)

![alt text](http://i66.tinypic.com/2s8g1f5.jpg)

Box: SG-4200

1 Reply Last reply  __ Reply Quote __ 0 __

  * [ T Offline ](/user/thenarc)

** [TheNarc](/user/thenarc) **

__ last edited by TheNarc  [](/post/792674) __

  


If you want the firewall itself to only use the DNS servers that you specify in System > General, then you'll want to uncheck the "Allow DNS server list to be overridden by DHCP/PPP on WAN" option.

For DNS over TLS, you need to put unbound into forwarding mode. Check the "Enable Forwarding Mode" and "Use SSL/TLS for outgoing DNS Queries to Forwarding Servers" options. 2.4.3 didn't have that latter check box, and instead you needed to add custom options for DNS over TLS, so that's what the post you mention was referring to.

P ![wgstarks](/assets/uploads/profile/uid-99522/99522-profileavatar.jpeg)W 2 Replies Last reply  __ Reply Quote __ 2 __

  * [ P Offline ](/user/p3r)

** [P3R](/user/p3r) ** [__@TheNarc](/post/792674)

__ last edited by P3R  [](/post/792705) __

  


[@thenarc](/user/thenarc) said in [How to configure DNS over TLS in 2.4.4?](/post/792674):

> For DNS over TLS, you need to put unbound into forwarding mode.

In the blog post it's specifically mentioned that forwarding mode "must be disabled".

1 Reply Last reply  __ Reply Quote __ 0 __

  * [ T Offline ](/user/thenarc)

** [TheNarc](/user/thenarc) **

__ last edited by  [](/post/792751) __

  


That's only because in the blog post, which applies to 2.4.3, you put it into forwarding mode using custom options.

1 Reply Last reply  __ Reply Quote __ 1 __

  * [ ![wgstarks](/assets/uploads/profile/uid-99522/99522-profileavatar.jpeg)W Offline ](/user/wgstarks)

** [wgstarks](/user/wgstarks) ** [__@TheNarc](/post/792674)

__ last edited by  [](/post/792907) __

  


[@thenarc](/user/thenarc)  
Thanks for the info.

Box: SG-4200

1 Reply Last reply  __ Reply Quote __ 0 __




__ __

  * First post __

Last post __

Go to my next post




Copyright 2026 Rubicon Communications LLC (Netgate). All rights reserved.   
[Privacy Policy](https://www.iubenda.com/privacy-policy/39208731 "Privacy Policy") · [Cookie Policy](https://www.iubenda.com/privacy-policy/39208731/cookie-policy "Cookie Policy")

Looks like your connection to Netgate Forum was lost, please wait while we try to reconnect.



