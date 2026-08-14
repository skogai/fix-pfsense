---
source_url: https://forum.netgate.com/topic/196513/adding-custom-configuration-in-kea-dhcp-server-with-pfsense-25-03
title: Adding Custom Configuration in Kea DHCP Server
category: community
priority: 1
pfsense_version_notes: Custom JSON config examples; version-sensitive (pfSense 25.03)
fetched_date: 2026-08-13
converter: webfetch
---

# Adding Custom Configuration in Kea DHCP Server

*Netgate Forum — DHCP and DNS category. Topic: 196513. 31 posts, 11 posters.*

> **CLAIM / VERSION CAVEAT:** This thread is about the pfSense Plus 25.03 "Custom Configuration" feature for Kea. The feature was NOT in the early 25.03 public beta; it landed in a later beta (e.g. 25.03.b.20250306.0140). Earlier adopters needed a Redmine patch (#15321). Treat the JSON syntax as version-sensitive.

## marcosm (Netgate employee) — Original Post

Similarly to how custom configuration is possible with the DNS Resolver and OpenVPN services, the pfSense+ 25.03 release brings custom configuration support for the Kea-backed DHCP Server. A common setting used with the deprecated ISC DHCP Server is "Custom DHCP Options". The following is a quick guide on how the same can be accomplished with the "Custom Configuration" setting for Kea.

Note: DHCP options which are already defined in Kea, such as `v4-captive-portal` (option 114), must not be re-defined in the custom configuration. The Kea manual (see "List of standard DHCPv4 options configurable by an administrator") lists these predefined options.

Here's an example that configures option 114 and option 43 with two vendors (unifi and an example from the Kea manual). Option 43 is a bit special and requires additional definition. Note that option 114 may require additional configuration in Captive Portal (e.g. for RFC8908 support).

In `Services / DHCP Server / Settings` add the following:

```json
{
  "option-def": [
    {
      "name": "unifi",
      "code": 1,
      "space": "vendor-encapsulated-options-space",
      "type": "string"
    },
    {
      "name": "examplevendor",
      "code": 2,
      "space": "vendor-encapsulated-options-space",
      "type": "record",
      "array": false,
      "record-types": "ipv4-address, uint16, string"
    }
  ]
}
```

In `Services / DHCP Server / LAN` add the following:

```json
{
  "option-data": [
    {
      "name": "vendor-encapsulated-options"
    },
    {
      "name": "unifi",
      "space": "vendor-encapsulated-options-space",
      "csv-format": false,
      "data": "0xc0000203"
    },
    {
      "name": "examplevendor",
      "space": "vendor-encapsulated-options-space",
      "csv-format": true,
      "data": "192.0.2.3, 123, Hello World"
    },
    {
      "name": "v4-captive-portal",
      "data": "https://captiveportal.example.com:8003/index.php?zone=guest"
    }
  ]
}
```

It is also possible to add script hooks to Kea. Scripts are stored at `/cf/conf/kea4_scripts.d` and `/cf/conf/kea6_scripts.d`.

**Other examples:**

The logging verbosity can be adjusted per logger, e.g. to show leases. See: https://kea.readthedocs.io/en/stable/arm/logging.html#id3

```json
{
  "loggers": [
    {
      "name": "kea-dhcp4.leases",
      "output_options": [
        {
          "output": "syslog"
        }
      ],
      "severity": "INFO"
    }
  ]
}
```

Lease release requests can be ignored like so:

```json
{
  "client-classes": [
    {
      "name": "DROP",
      "test": "pkt4.msgtype==7"
    }
  ]
}
```

A DHCP static mapping can have the gateway omitted:

```json
{
  "option-data": [
    {
      "name": "routers",
      "data": ""
    }
  ]
}
```

## marcosm (side-note)

Side-note: here's a helpful tool to validate the JSON data syntax before adding it to the custom configuration: https://string.is/json-formatter

## jaysee3

Hi, I have just updated to the latest beta of pfSense+ 25.03, but I do not see where I could add these in **Services / DHCP Server / Settings** or **Services / DHCP Server / LAN**. I'm sure I'm missing something basic or a critical step somewhere, but I don't know what. Besides setting the **Server Backend** to **Kea DHCP**, is there anything else I need to do? Thanks.

## patient0 (reply to jaysee3)

@jaysee3 Mmh, never used this feature and went looking for it. It doesn't show for me neither (on 25.03-BETA). It is not in the "High Availability" section and below that section is nothing.

## Gertjan (reply to jaysee3)

@jaysee3 — your 25.03 dates from early February, so the functionality isn't in our Beta, but in the new beta, not yet available. As referenced in this thread (see above), go see here: https://forum.netgate.com/topic/190373/feature-15321-shows-how-to-use-option-114-in-kea/8, install the patch mentioned here: Redmine #15321. Then you'll see the custom config box at the bottom of: Services > DHCP Server > Settings. Or wait a while for a new, more recent beta to become available.

## jaysee3 (follow-up)

So in the post before mine, @EDaleH, mentioned this in the linked thread: "See Adding Custom Configuration in Kea DHCP Server with pfSense+ 25.03 for current information on Plus release 25.03. Now that options are directly supported, the patch will no longer be required. The syntax is the same as it was for the patch." So I assumed that to be true. Considering this is a different thread and without that context (patch), it would be nice to have confirmation either way (RE: patch required). I've come full circle. In the Redmine link, I see this post referenced, so can assume it's required.

## jaysee3 (follow-up 2)

Meant to edit the original post for clarity but waited too long. The comment from @EDaleH about not needing the patch was a little confusing, but I've come full circle. In the Redmine link, I see our/this post referenced, so can assume it's required. With that said, I've applied the latest patch by Dale, but I only see 1 **Custom Option** input box under **Services/DHCP Server/Settings** (for the option-def). I don't see the corresponding input box for under each interface (for the option-data) mention by the OP. I have tried to put both definitions and data in that one box but it doesn't seem to work.

## Gertjan (reply to jaysee3)

@jaysee3 — "I don't see the corresponding input box for under each interface" — That's correct. The custom box contains settings that are global. The json text is very picky about the syntax, it has to be correct, or it is discarded. That's why a json-formatter validator is proposed. It won't test the validity though. The patch and parameters work fine for me. On my captive portal interface, "opt2", the "v4-captive-portal" option is sent (the rfc8910 login URL). On my LAN interface, "custom-option-vendor" is sent, with the data "0104C0A80106" = 192.168.1.6.

## marcosm (Netgate employee)

The change for custom configuration isn't available in the current public beta build. It will be available once we release a new public beta build. When that happens, I suggest removing the old custom configuration then reverting the patch before upgrading. Once upgraded, follow the guide in the OP — the syntax is slightly different.

## jaysee3

@marcosm Awesome. Thank you.

## jaysee3 (reply to Gertjan)

@Gertjan switching type from string to binary did the trick for me. Not sure why type string wasn't working for me. Thanks for all the help.

## Gertjan (reply to jaysee3)

@jaysee3 — I've found out the same thing and that's why I'm using 'binary' instead of 'string'. That said, I use this "code 43" for my Unifi devices, so they can find the controller. It seems they need the 'binary' format. For other devices that use this option 43, the format might be different.

## EDaleH (reply to marcosm)

As of the March 5th 25.03 Beta release: The purpose of this reply is to clarify RFC8910 / DHCP 114 syntax to support smart devices, in particular the iPhone under Captive Portal.

@marcosm said: "In Services / DHCP Server / Settings add the following:"

For DHCP 114, it is already defined in Kea as "v4-captive-portal" so no entry needs to be made at all here. I did however have to enter a JSON from the sample, save it, then delete it and save it again before the JSON entry box showed up on the individual Captive Portal's DHCP configuration screen. I mention it here in case anyone has the same problem.

@marcosm said: "In Services / DHCP Server / LAN add the following:"

I do not have captive portals on the LAN, all of mine are on OPT1 VLANs so go to the correct Captive Portal in Services, DHCP Server, scroll to the bottom and add to the JSON Configuration box something like the following:

```json
{
  "option-data":  [
      {
        "name": "v4-captive-portal",
        "data":  "https://sub.your-domain.com:8003/rfc8910.php?zone=vlan10"
      }
    ]
}
```

The rfc8910.php file can be found in Redmine #15904 as RFC8910-w-allowed-MAC-IP-fix.php. It must be renamed to rfc8910.php and placed into /usr/local/captiveportal to work with the above example. Be careful to reference the correct port and vlan for your portal when creating the above JSON.

## Gertjan (reply to EDaleH)

@EDaleH Example: I've 5 "Unifi UB Pro 6" APs on a pfSense, OPT1 network, which is a captive portal. There are also 2 of these "Unifi UB Pro 6" on my pfSense LAN for wireless company devices.

I've chosen to use the DHCP method of announcing the IP of the UNIFI controller, so I need to create a

```json
{
  "option-def": [
    {
      "space": "dhcp4",
      "name": "custom-option-vendor",
      "code": 43,
      "type": "binary"
    }
  ]
}
```

on the main Services > DHCP Server > Settings page.

On the Services > DHCP Server > LAN page:

```json
{
  "option-data":  [
      {
        "name": "custom-option-vendor",
        "data": "0104C0A80106"
      }
    ]
}
```

where "0104C0A80106" stands for the IP 192.168.1.6, the IP of my Unifi controller.

The Services > DHCP Server > PORTAL (OPT1) which hosts the captive portal: Here I announce the RFC8910 method — and also the Unifi controller location:

```json
{
  "option-data":  [
      {
        "name": "v4-captive-portal",
        "data":  "https://portal.bhf.tld:8003/rfc8910.php?zone=cpzone1"
      },
      {
        "name": "custom-option-vendor",
        "data": "0104C0A80106"
      }
    ]
}
```

Btw: "cpzone1" is the name of the captive portal zone present on the OPT interface, 8003 is the port I used for this interface.

The latest pfSense Beta version 25.03.b.20250306.0140 offers two new things here: There is now a Custom JSON Configuration general config section, valid for the entire DHCP scope, and a Custom JSON Configuration for each interface. Whatever you enter in the Custom JSON Configuration section is sanity-checked using "lint", and not taken into account when issues (syntax errors) are found. Be aware: if errors are found, the manually entered data into a Custom JSON Configuration isn't used, so the server will start without it and you'll have a system notification asking you to look at the system log, where you will find, for example:

> /services_dhcp.php: The command '/usr/local/sbin/kea-dhcp4 -t /usr/local/etc/kea/kea-dhcp4.conf' returned exit code '1', the output was 'Syntax check failed with: /usr/local/etc/kea/kea-dhcp4.conf:114.25-29: got unexpected keyword "lan" in pools map.'

so you'll know there was a "Syntax check failed". Double check your JSON structure. The good thing here is, if there was a JSON error, the DHCPv4 still runs, not leaving you without DHCP active.

## marcosm (Netgate employee)

The space `vendor-encapsulated-options-space` is set up differently; `code` specifies the sub-option and the length can be omitted. Hence what would previously be defined in the ISC DHCP GUI as `0104c0000203` can be specified as either `c0000203` or `0xc0000203` (the hex prefix is optional). To get this value, use an IP to hex converter. However, missing from the example in the OP was `"csv-format": false` (referenced in the Kea docs) — I've updated the example accordingly.

## FCS001FCS (reply to Gertjan)

@Gertjan I have a test minipc system I just installed pfSense CE 2.8 beta and want to go with KEA DHCP but need to inform my 2 Unifi Mini Flex Switches via the DHCP-Option 43 for a Unifi Network Controller that is on another sub-net. It worked with ISC on CE 2.7 so wanted to have the same function using KEA. I followed as best I could your examples and think it works. I did not find any "php-frm" errors in the General Log after a Reboot, so can I assume it works? How can I check that the Option 43 is actually sent/working?

## Gertjan (reply to FCS001FCS)

@FCS001FCS — "How can I check that the Option 43 is actually sent/working?" That's the easy part. Ask it! Here: Select the interface (e.g. your LAN), View options: High, Protocol: UDP, Ports: 67 and 68, and hit Start. Fire up your favorite SSH client (e.g. Putty), SSH into your Unifi AP on LAN. Type `info` to see more, `ps | grep 'dhcp'` to see the dhcp client config file. From the unifi command line, type `reboot`. You can also remove the power for a moment.

Now you'll see the pfSense capture showing the result. The answer from Kea includes:

```
Vendor-Option (43), length 6: 1.4.192.168.1.6
```

and I presume this is the 'encoded' ("1" for IPv4, "4" for 4 bytes and 192.168.1.6 which is my controller IP).

A even better test would be: instead of rebooting your AP, reset it with the button on the back. This will wipe all internal AP settings, and it should find all the correct settings when doing its initial DHCP request.

Be aware of the Plan B: Resolver settings, Host Overrides. If the DHCP method didn't work out, the DNS method is used: it searches for the "unifi" host name and uses that IP as the controller IP.

## FCS001FCS (reply to Gertjan)

@Gertjan Excellent, that worked great! I setup the packet capture as you detailed and ran it, then for good measure, unplugged and plugged the LAN RJ45 to the Flex-Mini Switch. In the packet capture I got exactly as you stated, the "Vendor Option (43)" but with the IP of my Unifi Network Controller. Thanks for the confirmation and I hope others going to KEA on pfSense CE 2.8 Beta can find this thread to also help them out. BTW, the Unifi USW Flex-Mini (old 1G version) is one of the only Unifi Switches that does not have SSH capability, so the DHCP Option 43 is the only way to set the "Inform" IP for an out of sub-network Unifi Controller.

## Gertjan (reply to FCS001FCS)

@FCS001FCS If the "Flex-Mini Switch" doesn't have SSH ... not an issue. It probably still supports DNS. So it will request the "unifi" host name, thus finding your controller's IP.

## FCS001FCS

FYI — Just for confirmation, I factory reset the 2 USW Flex Mini Switches to see if they would be available for adoption again in the Unifi Controller. One showed up after some restarts. The other would just not show up as adoptable. I ended up removing that switch from the Controller and adopting it fresh. I do not think it was a KEA issue, as I checked with the Packet Capture process and the DHCP Option 43 seemed to have been set in the switches, but the Controller just did not see it. So, if someone else is in a similar situation, maybe a fresh start for the Unifi Controller may be the easiest approach. Note: Your mileage may vary. All working now in my test setup, so happy days.

## pescew

How can we define custom client-classes options? I tried this but seems to have no effect:

```json
{
    "client-classes": [
        {
            "name": "UEFI-64-1-1",
            "test": "((substring(option[vendor-class-identifier].hex,0,20) == 'PXEClient:Arch:00007') and ((option[user-class].exists) and (substring(option[user-class].text,0,7) == 'iVentoy'))",
            "boot-file-name": "iventoy_loader_16000_uefi",
            "next-server": "172.26.2.18"
        },
        {
            "name": "UEFI-64-1-2",
            "test": "(substring(option[vendor-class-identifier].hex,0,20) == 'PXEClient:Arch:00007')",
            "boot-file-name": "efi64/syslinux.efi",
            "next-server": "172.26.2.19"
        },
        {
            "name": "Legacy",
            "test": "(substring(option[vendor-class-identifier].hex,0,20) == 'PXEClient:Arch:00000')",
            "boot-file-name": "pxelinux.0",
            "next-server": "172.26.2.19"
        }
    ]
}
```

## marcosm (Netgate employee, reply to pescew)

@pescew The structure is correct. A quick test here shows there's an issue with the first item (seen in the DHCP logs). Removing it and keeping only "UEFI-64-1-2" and "Legacy" lets Kea start.

## pescew (reply to marcosm)

@marcosm Thanks for the quick reply, I didn't realize that info was in the log. After cleaning up the parenthesis on that line it's working perfectly and PXE booting. I still need to troubleshoot the user-class rule to get the chain-loading working but that should be easy from here.

## Gertjan (reply to pescew)

@pescew Yeah, more '(' then ')', that's normally not a good sign.

## Garet Jax

@Gertjan Thank you brother. All your suggestions worked great. I joined the forums just to tell you so.

## cobordism

Is this also the place where I would add additional routes to DHCP responses? "Classless static routes". Context: My laptop has a VPN client active that has a 'local network access' option for accessing things like printers and NAS on the local network, bypassing the VPN. However this only works when there is a corresponding entry in the routing table. It does not work across local subnets. So if I have a 192.168.1.0/24 and a 192.168.2.0/24 network, I will not be able to access one from the other while VPN is active. The workaround is to manually add a route to my laptop.

*(Source truncated — remaining ~161 lines of thread not retrieved by webfetch.)*
