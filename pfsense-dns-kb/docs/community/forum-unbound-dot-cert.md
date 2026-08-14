---
source_url: https://forum.netgate.com/topic/155225/pfsense-unbound-dot-additional-setting-needed
title: pfSense Unbound DoT - additional setting needed? | Netgate Forum
category: community
priority: 1
pfsense_version_notes: Forum: Unbound DoT cert-validation nuance (must set TLS hostname)
fetched_date: 2026-08-13
converter: bs4+html2text
---

Your browser does not seem to support JavaScript. As a result, your viewing experience will be diminished, and you have been placed in **read-only mode**. 

Please download a browser that supports JavaScript, or enable it if it's disabled (i.e. NoScript). 

[ Introducing Netgate Nexus: Multi-Instance Management at Your Fingertips. ](https://www.netgate.com/nexus)

# 

pfSense Unbound DoT - additional setting needed?

__Scheduled __Pinned __Locked [ __Moved](/category/) [ __DHCP and DNS](/category/19/dhcp-and-dns)

[unbound](/tags/unbound)[dns resolver](/tags/dns%20resolver)[tls](/tags/tls)[config](/tags/config)

__ 3 Posts __ 2 Posters __ 2.8k Views __ 2 Watching

[__](/topic/155225.rss)

Loading More Posts __

__

  * Oldest to Newest __
  * Newest to Oldest __
  * Most Votes __



[__Reply](/compose?tid=155225)

  * Reply as topic



[Log in to reply](/login)

This topic has been deleted. Only users with topic management privileges can see it.

  * [ ![MikeV7896](/assets/uploads/profile/uid-53878/53878-profileavatar-1613917053643.png)M Offline ](/user/mikev7896)

** [MikeV7896](/user/mikev7896) **

__ last edited by MikeV7896  [](/post/923959) __

  


So... I came across this blog post on another site from 2018 regarding Unbound forwarding and how many articles about setting up DoT and Unbound are missing one thing: Certificate validity checks. What does this mean? It means that anyone could still intercept your DoT request and replace it with a response of their own, even with just a self-signed certificate, and Unbound would be none the wiser.

Here's the article: https://www.ctrl.blog/entry/unbound-tls-forwarding.html

Apparently, there are two pieces needed to completely secure Unbound DoT:

    1. Root CA Bundle (located in /etc/ssl/cert.pem)
    2. An additional piece for each forwarder line indicating the TLS domain that the server will be presenting

pfSense is already configured with #1. But #2 is the piece that is missing. Since pfSense just takes the DNS server IP addresses from System > General, it doesn't have any info regarding the domain that should be getting returned in the TLS certificate, thus not being able to fully validate that the request is coming from the server it thinks it is.

From the Unbound Config man page ([forward-addr](https://nlnetlabs.nl/documentation/unbound/unbound.conf/#forward-addr)):

> If you leave out the '#' and auth name from the forward-addr,  
>  any name is accepted. The cert must also match a CA from the  
>  tls-cert-bundle.

I'll be happy to open a feature request for this (if something similar isn't already open), adding the ability to specify DNS forwarders on the DNS Resolver settings page, including the domain name. Maybe the System > General servers could be automatically imported, but don't allow saving until the domain names are added if the "Use SSL/TLS for outgoing queries..." option is checked? But this seems like a pretty big piece missing to ensure that DoT is fully secured here.

The S in IOT stands for Security

1 Reply Last reply  __ Reply Quote __ 0 __

  * [ ![jimp](/assets/uploads/profile/uid-6930/6930-profileavatar.jpeg)J Offline ](/user/jimp)

** [jimp](/user/jimp) ** [__Rebel Alliance](/groups/rebel-alliance) [__Developer](/groups/developer) [__Netgate](/groups/employee)

__ last edited by  [](/post/924225) __

  


System > General also includes a box to define the hostname for checking the cert validity. If you don't see that, you must be on an outdated version of pfSense.

![ae326f84-d66e-4c2e-ae47-7de954098540-image.png](/assets/uploads/files/1594666984810-ae326f84-d66e-4c2e-ae47-7de954098540-image.png)

Remember: Upvote with the 👍 button for any user/post you find to be helpful, informative, or deserving of recognition!

Need help fast? [Netgate Global Support](https://www.netgate.com/support/)!

**Do not Chat/PM for help!**

1 Reply Last reply  __ Reply Quote __ 2 __

  * [ ![MikeV7896](/assets/uploads/profile/uid-53878/53878-profileavatar-1613917053643.png)M Offline ](/user/mikev7896)

** [MikeV7896](/user/mikev7896) **

__ last edited by  [](/post/924797) __

  


Thanks for that... I had seen the DNS hostname boxes, but must've missed the text below indicating that they're related to DoT. Something might want to be mentioned on the DNS Resolver page at the SSL/TLS checkbox too, that for best security the hostnames for the servers should be entered on System > General.

The S in IOT stands for Security

1 Reply Last reply  __ Reply Quote __ 0 __




__ __

  * First post __

Last post __

Go to my next post




Copyright 2026 Rubicon Communications LLC (Netgate). All rights reserved.   
[Privacy Policy](https://www.iubenda.com/privacy-policy/39208731 "Privacy Policy") · [Cookie Policy](https://www.iubenda.com/privacy-policy/39208731/cookie-policy "Cookie Policy")

Looks like your connection to Netgate Forum was lost, please wait while we try to reconnect.



