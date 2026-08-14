---
source_url: https://www.netgate.com/blog/dns-over-tls-with-pfsense
title: DNS over TLS with pfSense
category: community
priority: 2
pfsense_version_notes: Netgate blog: DNS over TLS with pfSense
fetched_date: 2026-08-13
converter: bs4+html2text
---

This is the first blog post in our new series, _Tips and Tricks_.

[Cloudflare’s new DNS service](https://blog.cloudflare.com/announcing-1111/) has a lot of industry attention, so we wanted to offer a quick guide that covers setting up your DNS servers in pfSense®, including configuring DNS over TLS. In addition to Cloudflare DNS servers, the following guide also applies to Quad9 DNS service.

Thanks to [Unbound](https://www.unbound.net/), the built-in DNS resolver, which has been enabled by default since pfSense version 2.3, makes configuring DNS over TLS a very simple task with pfSense.

**Note:** This guide applies only to DNS resolver. Forwarding mode must be disabled in the DNS resolver settings, since the example below defines its own forwarding zone.

## Step 1

The first step ensure Cloudflare DNS servers are used even if the DNS queries are not sent over TLS (step 2). Navigate to **System > General Settings** and under **DNS servers** add IP addresses for Cloudflare DNS servers and select your WAN gateway.

[![Screen shot for DNS Server Settings](https://www.netgate.com/hubfs/Imported_Blog_Media/dns-server-settings-for-tls.png)](https://www.netgate.com/hubfs/Imported_Blog_Media/dns-server-settings-for-tls.png)

After entering the DNS IP addresses, scroll down to the bottom of the page and click **Save**. Your pfSense appliance is now using Cloudflare servers as DNS.

## Step 2

To configure the DNS resolver to send DNS queries over TLS, navigate to **Services > DNS Resolver** and on the tab **General Settings** scroll down to the **Custom Options** box. Enter the following lines (you should be able to simply copy / paste the section text block below):
    
    
    server:
    forward-zone:
    name: "."
    forward-ssl-upstream: yes
    forward-addr: 1.1.1.1@853
    forward-addr: 1.0.0.1@853
    

To use [Quad9 DNS servers](https://www.quad9.net/) instead of, or in addition to, the Cloudflare servers, change or add the following forward-addr entries in the **Custom Options** example above:
    
    
    forward-addr: 9.9.9.9@853
    forward-addr: 149.112.112.112@853
    

Feel free to mix and match the servers, you can add as many as you like, and using multiple DNS providers can help prevent an upstream outage from causing loss of DNS resolution on the firewall.

Click **Save** and you’re done! Your pfSense appliance is now sending DNS queries to Cloudflare DNS servers over TLS.

You can confirm if DNS queries are being sent over TLS by performing a packet capture on the WAN interface.

We’re using IPv4 in this guide, however Cloudflare and Quad9 also offer their DNS service for IPv6 networks. The steps in this guide should still apply if you’re using IPv6. Find the IPv6 addresses Cloudflare offers [here](https://developers.cloudflare.com/1.1.1.1/setting-up-1.1.1.1/) or Quad9 IPv6 addresses [here](https://www.quad9.net/faq/#Is_there_IPv6_support_for_Quad9).

This feature [will be available as a GUI option in pfSense 2.4.4](https://redmine.pfsense.org/issues/8388), and at that time the custom options can be removed.

That’s it for our first _Tips and Tricks_! There will be more posts coming soon about our appliances, software development, training, and much more.

  * [ Facebook Share ](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fwww.netgate.com%2Fblog%2Fdns-over-tls-with-pfsense "Share on Facebook")
  * [ Twitter Tweet ](https://twitter.com/intent/tweet?url=https%3A%2F%2Fwww.netgate.com%2Fblog%2Fdns-over-tls-with-pfsense&text=DNS+over+TLS+with+pfSense "Tweet on Twitter")
  * [ LinkedIn Share ](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fwww.netgate.com%2Fblog%2Fdns-over-tls-with-pfsense&title=DNS%20over%20TLS%20with%20pfSense&summary=This+is+the+first+blog+post+in+our+new+series%2C+Tips+and+Tricks.+Cloudflare%E2%80%99s+new+DNS+service+has+a+lot+of+industry+attention%2C+so+we+wanted+to+offer+a+quick...&source= "Share on LinkedIn")
  * [ Pinterest Pin ](https://pinterest.com/pin/create/button/?url=https%3A%2F%2Fwww.netgate.com%2Fblog%2Fdns-over-tls-with-pfsense "Pin!")
  * [ Email Email ](mailto:?subject=DNS%20over%20TLS%20with%20pfSense&body=https%3A%2F%2Fwww.netgate.com%2Fblog%2Fdns-over-tls-with-pfsense "Email")


