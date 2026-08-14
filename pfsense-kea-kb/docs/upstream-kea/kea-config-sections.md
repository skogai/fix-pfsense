---
source_url: https://kb.isc.org/docs/kea-configuration-sections-explained
title: Kea Configuration Introduction
category: upstream-kea
priority: 2
pfsense_version_notes:
fetched_date: 2026-08-13
converter: webfetch
---

# Kea Configuration Introduction

Kea configuration can, at first, seem daunting. Much of this is due to the [JSON](https://en.wikipedia.org/wiki/JSON) format of the file. The configuration can be broken down into sections, however, which makes it much easier to understand. Below we provide a simple but complete configuration that includes the most common sections. This example uses DHCPv4, but the same sections can be found in DHCPv6 configurations for Kea.

More information is available in the ARM.

The [Kea Administrator Reference Manual](https://kea.readthedocs.io/en/latest/arm/intro.html) contains much more information about Kea configuration; this document is a simple introduction.

## Basic Configuration

Here is a complete Kea configuration that will run. However, it has no subnet or shared-network information; this is simply the main section where some basics are defined.

```
{
  "Dhcp4": {
    "interfaces-config": {
      "interfaces": [
        "eth0"
      ]
    },
    "control-socket": {
      "socket-type": "unix",
      "socket-name": "kea4-ctrl-socket"
    },
    "lease-database": {
      "type": "memfile",
      "persist": true,
      "name": "dhcp4.leases"
    },
    "valid-lifetime": 28800,
    "option-data": [
      {
        "name": "domain-name-servers",
        "data": "192.0.2.1, 192.0.2.2"
      }
    ]
  }
}
```

There are other configuration elements that are not shown here, but this example contains the most common elements. Shown here are things like a list of interfaces to listen on, a control socket (for use with things like the API or [Stork](https://kea.readthedocs.io/en/latest/arm/stork.html)), a lease database for storage of information about leased addresses, and global DHCP option configuration and settings.

## Client Classes

Although many might include this section with the main, there is so much additional functionality possible using client classes that we are addressing it separately (see the [Client Classification section in the ARM](https://kea.readthedocs.io/en/latest/arm/classify.html) for more details). Below is a complete configuration that Kea will load, but it is missing key sections (such as subnet).

```
{
  "Dhcp4": {
    "client-classes": [
      {
        "name": "voip",
        "test": "substring(option[60].hex,0,9) == 'SomePhone'",
        "next-server": "192.0.2.254",
        "server-hostname": "hal9000",
        "boot-file-name": "SomePhone-settings.cfg"
      }
    ]
  }
}
```

This is a very simple client class showing what might be done with a VOIP phone. There are other features that are possible with client classes, such as setting specific DHCP option data, subnet selection, and even membership in one class based on membership (or lack thereof) in another class.

What is going on in that class?

What is happening above is a VOIP phone is being added to the "voip" class based on the DHCP packet containing "SomePhone" at the beginning of Option 60 (vendor-class-identifier) and then being redirected to a TFTP server to receive a configuration file that it needs on bootup.

## Hooks

This may be the most powerful section of the configuration, because libraries that add additional functionality to Kea may be loaded here. You can write your own (using either C++ or `run_script`, which allows the execution of an external shell script) or use the included hook libraries. This is another area where [an entire section of the ARM](https://kea.readthedocs.io/en/latest/arm/hooks.html) is devoted to this one configuration section.

```
{
  "Dhcp4": {
    "hooks-libraries": [
      {
        "library": "libdhcp_lease_cmds.so"
      },
      {
        "library": "libdhcp_ha.so",
        "parameters": {
            "high-availability": [
              {
                "this-server-name": "server1",
                "mode": "hot-standby",
                "peers": [
                  {
                    "name": "server1",
                    "url": "http://192.168.56.33:8000/",
                    "role": "primary",
                    "auto-failover": true
                },
                {
                    "name": "server2",
                    "url": "http://192.168.56.66:8000/",
                    "role": "standby",
                    "auto-failover": true
                }
              ]
            }
          ]
        }
      }
    ]
  }
}
```

Kea will load the above configuration and run; however, key pieces such as subnet or shared-network are still missing. The hooks loaded above represent a typical high-availability (HA) configuration known as `hot-standby`. This mode runs a primary server while keeping the secondary updated with the allocation of leases. If the primary server goes offline, the secondary then takes over and tends to the DHCP needs of the network. ISC offers a variety of features via open source hooks; other hooks are available only to customers of ISC via either support contracts or license purchase. As Kea itself is fully open source, anyone can also write their own hooks if desired.

## Networks

This section has subnet(s) and/or shared-network(s) as needed for the network(s) to be served. A single Kea server (or HA pair) can serve several networks with multiple subnets by using the `shared-networks` concept. However, to keep things simple we show only a single subnet configuration here.

```
{
  "Dhcp4": {
    "subnet4": [
      {
        "subnet": "192.0.2.0/24",
        "pools": [
          {
            "pool": "192.0.2.1 - 192.0.2.200"
          }
        ],
        "option-data": [
          {
            "name": "routers",
            "data": "192.0.2.1"
          }
        ],
        "reservations": [
          {
            "hw-address": "1a:1b:1c:1d:1e:1f",
            "ip-address": "192.0.2.201",
            "option-data": [
              {
                "name": "domain-name-servers",
                "data": "10.1.1.202, 10.1.1.203"
              }
            ]
          }
        ]
      }
    ]
  }
}
```

If DHCP traffic is received that is appropriate for the subnet "192.0.2.0/24", then Kea allocates an address with this configuration. Note, however, that some information is missing: most importantly, only the host "1a:1b:1c:1d:1e:1f" will receive DNS servers in the response.

How would Kea select the subnet in the example above?

Kea would select the subnet "192.0.2.0/24" in the simple subnet configuration above if an interface on which it is listening has an IP address from that subnet configured and local DHCP traffic is received, or if a relay agent in that subnet relays DHCP traffic from a client to the Kea server.

## Logging

Kea offers very flexible logging options. There are basically three ways to output the logging information: `stdout`, `syslog`, and directly to a file. For output to a file, Kea uses Log4cplus, which allows some customization features; for example, file rotation is configurable. Lots of details about logging are available in the [Kea ARM](https://kea.readthedocs.io/en/latest/arm/logging.html). As with the previous examples, this simple configuration will load and run but is very simple.

```
{
  "Dhcp4": {
    "loggers": [
      {
        "name": "kea-dhcp4",
        "output_options": [
          {
            "output": "kea-dhcp4.log",
            "maxsize": 1048576,
            "maxver": 8
          }
        ],
        "severity": "INFO"
      },
      {
        "name": "kea-dhcp4.packets",
        "output_options": [
          {
            "output": "kea-dhcp4-packets.log",
            "maxver": 10
          }
        ],
        "severity": "DEBUG",
        "debuglevel": 99
      }
    ]
  }
}
```

In addition to the aforementioned three output options, there are also many options for logging categories. Logs can be organized into several files using these categories combined with the filename output option. These logs do not need to be tended-to constantly thanks to the built-in rotation possibilites.

What's the "best" way to set up logging? It depends.

When I configure logging in Kea, I almost never use the `syslog` mechanism; I prefer the finer grained control possible with using an actual file. I typically set up a separate stanza for each category of logging possible with the particular Kea daemon (example: `kea-dhcp4`) I am configuring. This way I can send them all to separate files with separate severity configurations (example: `kea-dhcp4.packets` does not produce any logs unless set to `DEBUG` severity). If I am just quickly testing something, then I add only those loggers that I need and set them all to `stdout`. This way I can run Kea by hand and watch the output directly to my terminal.

## Putting it all together

So what now? Once you have a good handle on the sections of the Kea configuration, it becomes easier to understand what is happening when looking at the configuration file. We can put all of the sections above together and we will have a working configuration that should serve some clients.

Remember, this is just an example to give you an idea of the many possibilities when configuring Kea. You may want to experiment with it to get the functionality you need. If you want more help, you may consider joining the [kea-users mailing list](https://lists.isc.org/mailman/listinfo/kea-users), or your organization may be interested in [subscribing to ISC's professional support services](https://www.isc.org/support/).

High availability

Note that if there really were a high-availability configuration as shown below, there would need to be two Kea servers. These two servers could have essentially an identical configuration, with the exception that `this-server-name` would be `server1` or `server2` as appropriate.

```
{
  "Dhcp4": {
    "interfaces-config": {
      "interfaces": [
        "eth0"
      ]
    },
    "control-socket": {
      "socket-type": "unix",
      "socket-name": "kea4-ctrl-socket"
    },
    "lease-database": {
      "type": "memfile",
      "persist": true,
      "name": "dhcp4.leases"
    },
    "valid-lifetime": 28800,
    "option-data": [
      {
        "name": "domain-name-servers",
        "data": "192.0.2.1, 192.0.2.2"
      }
    ],
    "client-classes": [
      {
        "name": "voip",
        "test": "substring(option[60].hex,0,6) == 'SomePhone'",
        "next-server": "192.0.2.254",
        "server-hostname": "hal9000",
        "boot-file-name": "SomePhone-settings.cfg"
      }
    ],
    "hooks-libraries": [
      {
        "library": "libdhcp_lease_cmds.so"
      },
      {
        "library": "libdhcp_ha.so",
        "parameters": {
            "high-availability": [
              {
                "this-server-name": "server1",
                "mode": "hot-standby",
                "peers": [
                  {
                    "name": "server1",
                    "url": "http://192.168.56.33:8000/",
                    "role": "primary",
                    "auto-failover": true
                },
                {
                    "name": "server2",
                    "url": "http://192.168.56.66:8000/",
                    "role": "standby",
                    "auto-failover": true
                }
              ]
            }
          ]
        }
      }
    ],
    "subnet4": [
      {
        "subnet": "192.0.2.0/24",
        "pools": [
          {
            "pool": "192.0.2.1 - 192.0.2.200"
          }
        ],
        "option-data": [
          {
            "name": "routers",
            "data": "192.0.2.1"
          }
        ],
        "reservations": [
          {
            "hw-address": "1a:1b:1c:1d:1e:1f",
            "ip-address": "192.0.2.201",
            "option-data": [
              {
                "name": "domain-name-servers",
                "data": "10.1.1.202, 10.1.1.203"
              }
            ]
          }
        ]
      }
    ],
    "loggers": [
      {
        "name": "kea-dhcp4",
        "output_options": [
          {
            "output": "kea-dhcp4.log",
            "maxsize": 1048576,
            "maxver": 8
          }
        ],
        "severity": "INFO"
      },
      {
        "name": "kea-dhcp4.packets",
        "output_options": [
          {
            "output": "kea-dhcp4-packets.log",
            "maxver": 10
          }
        ],
        "severity": "DEBUG",
        "debuglevel": 99
      }
    ]
  }
}
```
