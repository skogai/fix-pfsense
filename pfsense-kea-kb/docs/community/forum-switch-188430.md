---
source_url: https://forum.netgate.com/topic/188430/switch-over-from-isc-dhcp-to-kea-dhcp
title: switch over from ISC DHCP to Kea DHCP
category: community
priority: 2
pfsense_version_notes: ""
fetched_date: 2026-08-13
converter: webfetch
---

# switch over from ISC DHCP to Kea DHCP

*Netgate Forum — DHCP and DNS category. Topic: 188430. 71 posts, 19 posters.*

> **CLAIM / VERSION CAVEAT:** This is an early community discussion (predates 24.08 HA and 25.03 custom config). Many complaints about missing features (static mappings, DNS registration, HA) were accurate for 23.09–24.03 but were addressed in later releases. Treat as historical sentiment, not current capability.

## netboy

I see a message "ISC DHCP has reached end-of-life and will be removed from a future version of Netgate pfSense Plus. Kea DHCP is the newer, modern DHCP distribution from ISC that includes the most-requested features."

Can I switch over to Kea from ISC? [select kea radio button] Will the change to Kea have any bearing on the DHCP leases or is it "seamless and nothing to worry about"? Do I need to be aware of any gotchas?

## Gertjan (reply to netboy)

@netboy — More than what the blog post told us? And one or two minor issues as mentioned on this forum? Not really. Probably true, ISC DHCP might get removed in late 2025 / 2026?, or just stay in pfSense, like the DNS Forwarder dnsmasq is still there, while the resolver Unbound is the default DNS solution now. That is, if no major security issues are found. Kea — the pfSense GUI front end — is still missing a lot of options and features; if you don't need them, then Kea will do just fine.

## hughbiquitous (reply to netboy)

@netboy The gotcha I ran into was that Kea does not register hostnames with DNS like ISC does. After I switched to Kea I started seeing things break if they relied on DNS resolution within my local network. I was able to just switch back to ISC and all is well for now, but I *really* hope ISC doesn't go away completely until Kea reaches feature parity.

## netboy

@hughbiquitous Thanks. I will probably continue to use ISC DHCP.

## ambrosios

Yeah KEA is super unstable right now. I've tried the switch three times — no luck. Most of my devices just stop connecting.

## johnpoz (Global Moderator)

@netboy — "before the cut-off?" before what cutoff? ISC has not stated any hard cutoff of any sort... Where is some cutoff? https://www.isc.org/blogs/isc-dhcp-eol/ — Other than the one that has already passed where the last "maint" release has been released already. "However, it is time to start thinking about a migration plan to a more modern system that is actively maintained." Which is exactly what pfsense is doing, they are moving towards kea. They even have a preview out that can provide very basic dhcp services. I would guess, a few more releases down the road kea will reach parity if not surpass the current feature set of isc and everyone will be able to migrate to kea if they so desire.

## netboy

@johnpoz Let me pose the question differently? When will KEA be stable?

## johnpoz (Global Moderator)

@netboy When it's ready, like with every release of pfsense ever in the history of pfsense. I have not seen any info about when that might be. Maybe it will be in 24.X or maybe it will be 25.X? I am sure there are many people looking forward to it.

## JKnott (reply to Gertjan)

@Gertjan — "Kea - the pfSense GUI front end - is still missing a lot of options and features, if you don't need them, then Kea will do just fine." Things like working DHCP? I tried switching today and DHCP failed completely. Other than that, it's great!

## netboy

@JKnott That is exactly my point — if DHCP is failing why have this feature which is not fully baked in?

## johnpoz (Global Moderator)

@netboy I have no idea what jknott is or was doing when he switched. But when they first released the "preview" I tested it and worked just fine if all you wanted to do was hand out an IP. Sure there are many users of pfsense that all they need is that. But I am not one of those people. Its limitations were blogged about, and in the release notes. Yeah its not quite ready for prime time. But it could serve as your dhcp server if all you wanted was "hey client asks for IP, give him one".

## netboy

@johnpoz Here is my issue. When I go to **Services > DHCP Server > LAN** I see the following message: "ISC DHCP has reached end-of-life and will be removed in a future version of Netgate pfSense Plus. Visit System > Advanced > Networking to switch DHCP backend". When I see the above message, I expect the change to Kea DHCP will be fully functional which is not the case. I am using DHCP for: Defining address pool range; Get a new IP address when new network device is connected; Defining STATIC mapping for some DHCP device. Does the existing change to kea DHCP allow me to do ALL OF THE ABOVE without issues (meaning has been tested)?

## Patch

@netboy — As has been commented many times on this forum, the message displayed by the software could have been better worded and less alarming. Users need to read the software release notes and understand what they are saying to accurately interpret the software message. That is why many users refer to the current Kea implementation in pfsense as a software preview. Please read the software release notes and earlier posts in this thread.

## JKnott (reply to johnpoz)

@johnpoz — I just enabled Kea. Later in the day, when I used my notebook, anything that required IPv4 wasn't working. On Linux, I had no IPv4 address and on Windows, I got an APIPA address. My cell phone also stopped connecting to WiFi. After going back to ISC, DHCP works again.

## ambrosios (reply to johnpoz)

@johnpoz — "I tested it and worked just fine if all you wanted to do was hand out an IP." If my network is more complicated then just needing IPs handed out, I may be grossly underestimating how complicated my network setup actually is. ISC: defaults, single subnet, a few static IPs... DHCP works fine. Switch to KEA and everything drops, never to be seen again. Granted I could spend more time on root cause, but I'm surprised to hear it worked for you. I may have to give it another go.

## Patch (reply to JKnott)

@JKnott — "After going back to ISC, DHCP works again." Cool. So Kea DHCP is working as advertised. From https://www.netgate.com/blog/netgate-adds-kea-dhcp-to-pfsense-plus-software-version-23.09-1 — the Kea implementation lacks the following DHCP server features:

- Local DNS Resolver/Forwarder Registration for static and dynamic DHCP clients
- Remote DNS server registration
- DHCPv6 Prefix Delegation
- High Availability Failover
- Lease statistics/graphs
- Custom DHCP options

Note: If you have assigned hostnames to devices on your network using static leases, or rely on dynamic lease registration in DNS, switching to Kea DHCP results in those hostnames being ignored. The static lease configuration is kept, so switching back to ISC DHCP will restore the functionality.

## JKnott (reply to ambrosios)

@ambrosios — I have multiple subnets and any device that lives here has a static mapped IPv4 address, other than my desktop computer and pfSense, both of which have a static configuration. After I noticed it failed, I even tried rebooting pfSense, but that made no difference.

## johnpoz (Global Moderator, reply to JKnott)

@JKnott — "any device that lives here has a static mapped IPv4 address" — Well since preview of kea doesn't support those, no wonder it's not working for you. So clearly you did not read the blog or the release notes.

## johnpoz (Global Moderator)

@netboy — You can turn the warning off. It's right there in the same place you switch to kea. This is nonsense — yeah netgate is going to drop isc before kea is even at parity with feature set of isc. That makes no freaking sense at all. If you would of read the info from ISC... Its not going anywhere any time soon. They are stopping development on it, so yeah its eol. Their own wording — time to start thinking of moving. Does this mean ISC DHCP won't work anymore? No. The existing open source software will continue to function as it has, and current operators do not need to stop using ISC DHCP.

## netboy

@johnpoz Based on the discussion it appears like Kea does not support static IP address (no I have not read the release notes) — am i right?

## JKnott (reply to johnpoz)

@johnpoz — I use static mapped addresses so that I have consistent addresses.

## johnpoz (Global Moderator, reply to JKnott)

@JKnott — What does that have to do with cost of tea in china? Great I use a lot of reservations as well — what part are you not understanding that kea does not support this in pfsense as of yet.

## netboy

@johnpoz How do I interpret this statement? Kea has no support for static address OR **pfsense's kea implementation** does not support static address NOW but will support later?

## johnpoz (Global Moderator)

@netboy — the integration of kea into pfsense is not complete. Kea has support for this feature and others. It has just not been integrated into pfsense as of yet. Why do you people have such a hard time reading documentation — if you have questions on what kea can do, just head over to isc and look at the docs for kea. One of the key benefits of pfsense is they have taken what services and applications that are normally configured via just .conf files, and wrapped a gui around it. If you want to run full blown kea on your network — just fire up something else and run it there — you just won't have an easy to use "gui" to configure it.

Sample Kea host-reservation config (from Kea docs):

```json
{
  "subnet4": [
    {
      "id": 1,
      "pools": [ { "pool":  "192.0.2.1 - 192.0.2.200" } ],
      "subnet": "192.0.2.0/24",
      "interface": "eth0",
      "reservations": [
        {
          "hw-address": "1a:1b:1c:1d:1e:1f",
          "ip-address": "192.0.2.202"
        },
        {
          "duid": "0a:0b:0c:0d:0e:0f",
          "ip-address": "192.0.2.100",
          "hostname": "alice-laptop"
        }
      ]
    }
  ]
}
```

Why the kea integration into pfsense is "preview" is all the work that takes your pretty gui and writes it for you into the kea configuration has not been done yet.

## netboy

@johnpoz — The "current" message "ISC DHCP has reached end-of-life and will be removed in a future version of Netgate pfSense Plus..." does not make it "explicit" that pfsense kea has limited functionality. Pfsense must change the above message to something meaningful to say something to the effect "pfsense kea is in experimental stage and fully not implemented". You need to look at the GUI and messages with a GENERAL USER hat not a NETWORK USER imho.

## johnpoz (Global Moderator)

@netboy dude pretty sure everyone agrees the wording could of been done a bit better. Move on already.

## Wylbur (reply to Gertjan)

@Gertjan — Just commenting on your post relative to my questions on what changes. Since I do have assigned hostnames with static leases, such as our file server, our HP printer/scanner, etc., I am interested in what is happening with Kea DHCP and when it will support prior functions I use or provides an equivalent that we can migrate to "automatically" if possible.

## pulsartiger

I came across this topic when seeing the notice on my pfsense instance. Rather than create a new topic, I figure I continue the discussion to see if things have changed. I've been using pfsense for several years now and I typically do not change any settings unless necessary. If I change from ISC DHCP to Kea DHCP, is there any that needs to be done beforehand besides making a backup? Are there any other settings to change besides clicking the KEA DHCP radio button and clicking Save? If I choose to keep using ISC DHCP, is there any harm in doing so? (security issues?)

## johnpoz (Global Moderator, reply to pulsartiger)

@pulsartiger I wouldn't switch to kea yet. Just turn off the warning if it bugs you. Kea is not at feature parity yet. And no there are no real security issues with just continuing to use ISC.

*(Source truncated — remaining ~85 lines of thread not retrieved by webfetch.)*
