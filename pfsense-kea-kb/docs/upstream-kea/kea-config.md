---
source_url: https://kea.readthedocs.io/en/latest/arm/config.html
title: 6. Kea Configuration
category: upstream-kea
priority: 2
pfsense_version_notes:
fetched_date: 2026-08-13
converter: webfetch
---

# 6. Kea Configuration

Kea uses JSON structures to represent server configurations. The following sections describe how the configuration structures are organized.

## 6.1. JSON Configuration

JSON is the notation used throughout the Kea project. The most obvious usage is for the configuration file, but JSON is also used for sending commands over the Management API (see [Management API](https://kea.readthedocs.io/en/latest/arm/ctrl-channel.html#ctrl-channel)) and for communicating between DHCP servers and the DDNS update daemon.

Typical usage assumes that the servers are started from the command line, either directly or using a script, e.g. [keactrl](https://kea.readthedocs.io/en/latest/man/keactrl.8.html#std-iscman-keactrl). The configuration file is specified upon startup using the `-c` parameter.

### 6.1.1. JSON Syntax

Configuration files for the DHCPv4, DHCPv6, DDNS and NETCONF modules are defined in an extended JSON format. Basic JSON is defined in [RFC 7159](https://datatracker.ietf.org/doc/html/rfc7159) and [ECMA 404](https://www.ecma-international.org/publications/standards/Ecma-404.htm). In particular, the only boolean values allowed are true or false (all lowercase). The capitalized versions (True or False) are not accepted.

Even though the JSON standard (ECMA 404) does not require JSON objects (i.e. name/value maps) to have unique entries, Kea implements them using a C++ STL map with unique entries. Therefore, if there are multiple values for the same name in an object/map, the last value overwrites previous values. Since Kea 1.9.0, configuration file parsers raise a syntax error in such cases.

Kea components use extended JSON with additional features allowed:

* Shell comments: any text after the hash (#) character is ignored.
* C comments: any text after the double slashes (//) character is ignored.
* Multiline comments: any text between /\* and \*/ is ignored. This comment can span multiple lines.
* File inclusion: JSON files can include other JSON files by using a statement of the form <?include "file.json"?>.
* Extra commas: to remove the inconvenience of errors caused by leftover commas after making changes to configuration. While parsing, a warning is printed with the location of the comma to give the user the ability to correct a potential mistake.

Warning

These features are meant to be used in a JSON configuration file. Their usage in any other way may result in errors.

The configuration file consists of a single object (often colloquially called a map) started with a curly bracket. It comprises only one of the "Dhcp4", "Dhcp6", "DhcpDdns", or "Netconf" objects. It is possible to define additional elements but they will be ignored.

A very simple configuration for DHCPv4 could look like this:

# The whole configuration starts here.
{
    # DHCPv4 specific configuration starts here.
    "Dhcp4": {
        "interfaces-config": {
            "interfaces": [ "eth0" ],
            "dhcp-socket-type": "raw"
        },
        "valid-lifetime": 4000,
        "renew-timer": 1000,
        "rebind-timer": 2000,
        "subnet4": [{
           "pools": [ { "pool": "192.0.2.1-192.0.2.200" } ],
           "subnet": "192.0.2.0/24",
           "id": 1
        }],

       # Now loggers are inside the DHCPv4 object.
       "loggers": [{
            "name": "*",
            "severity": "DEBUG"
        }]
    }

# The whole configuration structure ends here.
}

More examples are available in the installed `share/doc/kea/examples`directory.

To avoid repetition of mostly similar structures, examples in the rest of this guide will showcase only the subset of parameters appropriate for a given context. For example, when discussing the IPv6 subnets configuration in DHCPv6, only subnet6 parameters will be mentioned. It is implied that the remaining elements (the global map that holds Dhcp6) are present, but they are omitted for clarity. Usually, locations where extra parameters may appear are denoted by an ellipsis (...).

### 6.1.2. Comments and User Context

Shell, C, or C++ style comments are all permitted in the JSON configuration file if the file is used locally. This is convenient and works in simple cases where the configuration is kept statically using a local file. However, since comments are not part of JSON syntax, most JSON tools detect them as errors. Another problem with them is that once Kea loads its configuration, the shell, C, and C++ style comments are ignored. If commands such as [config-get](https://kea.readthedocs.io/en/latest/arm/ctrl-channel.html#std-isccmd-config-get) or [config-write](https://kea.readthedocs.io/en/latest/arm/ctrl-channel.html#std-isccmd-config-write) are used, those comments are lost. An example of such comments was presented in the previous section.

Historically, to address the problem, Kea code allowed the use of comment strings as valid JSON entities. This had the benefit of being retained through various operations (such as [config-get](https://kea.readthedocs.io/en/latest/arm/ctrl-channel.html#std-isccmd-config-get)), or allowing processing by JSON tools. An example JSON comment looks like this:

"Dhcp4": {
    "subnet4": [{
        "id": 1,
        "subnet": "192.0.2.0/24",
        "pools": [{ "pool": "192.0.2.10 - 192.0.2.20" }],
        "comment": "second floor"
    }]
}

However, the facts that the comment could only be a single line, and that it was not possible to add any other information in a more structured form, were frustrating. One specific example was a request to add floor levels and building numbers to subnets. This was one of the reasons why the concept of user context was introduced. It allows adding an arbitrary JSON structure to most Kea configuration structures.

This has a number of benefits compared to earlier approaches. First, it is fully compatible with JSON tools and Kea commands. Second, it allows storing simple comment strings, but it can also store much more complex data, such as multiple lines (as a string array), extra typed data (such as floor numbers being actual numbers), and more. Third, the data is exposed to hooks, so it is possible to develop third-party hooks that take advantage of that extra information. An example user context looks like this:

"Dhcp4": {
    "subnet4": [{
        "id": 1,
        "subnet": "192.0.2.0/24",
        "pools": [{ "pool": "192.0.2.10 - 192.0.2.20" }],
        "user-context": {
            "comment": "second floor",
            "floor": 2
        }
    }]
}

User contexts can store an arbitrary data file as long as it has valid JSON syntax and its top-level element is a map (i.e. the data must be enclosed in curly brackets). However, some hook libraries may expect specific formatting; please consult the specific hook library documentation for details.

The user-context mechanism has superseded the JSON comment capabilities; ISC encourages administrators to use user context instead of the older mechanisms. To promote this way of storing comments, Kea converts JSON comments to user context on the fly.

However, if the configuration uses the old JSON comment method, the [config-get](https://kea.readthedocs.io/en/latest/arm/ctrl-channel.html#std-isccmd-config-get) command returns a slightly modified configuration. It is not uncommon for a call for [config-set](https://kea.readthedocs.io/en/latest/arm/ctrl-channel.html#std-isccmd-config-set) followed by [config-get](https://kea.readthedocs.io/en/latest/arm/ctrl-channel.html#std-isccmd-config-get) to receive a slightly different structure. The best way to avoid this problem is simply to abandon JSON comments and use user context.

Kea supports user contexts at the following levels: global scope, interfaces configuration, multi-threading, shared networks, subnets, client classes, option data and definitions, pools, prefix delegation pools, host reservations, control socket, HTTP header, authentication, clients, queue control, DHCP-DDNS, loggers, leases, and server ID. These are supported in both DHCPv4 and DHCPv6, with the exception of prefix delegation pools and server ID, which are DHCPv6 only.

User context can be added and edited in structures supported by commands.

We encourage Kea users to utilize these functions to store information used by other systems and custom hooks.

For example, the [subnet4-update](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-isccmd-subnet4-update) command can be used to add user context data to an existing subnet.

{
"subnet4": [ {
   "id": 1,
   "subnet": "10.20.30.0/24",
   "user-context": {
      "building": "Main",
      "floor": 1
      }
 } ]
 }

The same can be done with many other commands, like [lease6-add](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-isccmd-lease6-add), etc.

Kea also uses user context to store non-standard data. Currently, only [Storing Extended Lease Information](https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#dhcp4-store-extended-info) uses this feature.

When enabled, it adds the ISC key in `user-context` to differentiate automatically added content.

Example of relay information stored in a lease:

{
"arguments": {
   "client-id": "42:42:42:42:42:42:42:42",
   "cltt": 12345678,
   "fqdn-fwd": false,
   "fqdn-rev": true,
   "hostname": "myhost.example.com.",
   "hw-address": "08:08:08:08:08:08",
   "ip-address": "192.0.2.1",
   "state": 0,
   "subnet-id": 44,
   "valid-lft": 3600,
   "user-context": {
      "ISC": {
      "relays": [
      {
            "hop": 2,
            "link": "2001:db8::1",
            "peer": "2001:db8::2"
      },
      {
            "hop": 1,
            "link": "2001:db8::3",
            "options": "0x00C800080102030405060708",
            "peer": "2001:db8::4"
      }]
      }
   }
}
}

User context can store configuration for multiple hooks and comments at once.

For a discussion about user context used in hooks, see [User Contexts in Hooks](https://kea.readthedocs.io/en/latest/arm/hooks.html#user-context-hooks).

### 6.1.3. Simplified Notation

It is sometimes convenient to refer to a specific element in the configuration hierarchy. Each hierarchy level is separated by a slash. If there is an array, a specific instance within that array is referenced by a number in square brackets (with numbering starting at zero). For example, in the above configuration the valid-lifetime in the Dhcp4 component can be referred to as Dhcp4/valid-lifetime, and the pool in the first subnet defined in the DHCPv4 configuration as Dhcp4/subnet4\[0\]/pool.

### 6.1.4. Configuration Files Inclusion

The parser provides the ability to include files. The syntax was chosen to look similar to how Apache includes PHP scripts in HTML code. This particular syntax was chosen to emphasize that the include directive is an additional feature and not a part of JSON syntax.

The inclusion is implemented as a stack of files. You can use the include directive in nested includes. Up to ten nesting levels are supported. This arbitrarily chosen limit is protection against recursive inclusions.

The include directive has the form:

<?include "[PATH]"?>

The _\[PATH\]_ pattern should be replaced with an absolute path or a path relative to the current working directory at the time the Kea process was launched.

To include one file from another, use the following syntax:

{
   "Dhcp6": {
      "interfaces-config": {
         "interfaces": [ "*" ]},
      "preferred-lifetime": 3000,
      "rebind-timer": 2000,
      "renew-timer": 1000,
      <?include "subnets.json"?>
      "valid-lifetime": 4000
   }
}

where the content of "subnets.json" may be:

{
"subnet4": [
   {
      "id": 123,
      "subnet": "192.0.2.0/24"
   },
   {
      "id": 234,
      "subnet": "192.0.3.0/24"
   },
   {
      "id": 345,
      "subnet": "10.0.0.0/8"
   }
],
...
}

## 6.2. Kea Configuration Backend

### 6.2.1. Applicability

The Kea Configuration Backend (CB or config backend) gives Kea servers the ability to store almost all of their configuration in one or more databases.

Potential features and benefits include:

* Re-use of identical configuration sections across multiple Kea servers
* A "single source of truth" for all Kea servers
* All configuration done through an API with real-time logic checks
* Easier integration with third-party tools or in-house automation
* Database architecture provides concurrency, consistency, and atomicity
* The ability to mine the database for statistics and reporting
* Use of database replication for real-time fault-tolerance

Potential drawbacks include:

* Significant up-front effort to prepare integration and/or automation
* Supported scenarios require use of API for most configuration
* The API is only available to ISC customers with a paid support contract
* Incompatible with some uses, software, and scenarios

Note

Use of a database for storage of leases and/or host reservations is possible without using the CB. See the `host-databases` and `lease-database` config directives.

#### 6.2.1.1. Example Scenario

Consider a large organization with many sites, each with a pair of Kea servers deployed in a high availability (HA) configuration. Typically such deployments use standardized configurations, leading to similar config parameters for every site. The members of each HA pair are often almost exactly the same, differing only by name. Often installations of this size will feature a high level of automation, including provisioning and management systems.

The CB is ideal for such deployments. While some effort is required to integrate with the provisioning automation, once accomplished, deployment of new Kea servers can be nearly automatic. A small "stub" JSON config, identical for every server, can be used, and all remaining configuration (shared networks, subnets, pools, etc.) loaded from the central CB database. Any updates to the central CB database are automatically propagated to all Kea instances. The CB becomes the "single source of truth" for DHCP throughout the organization.

### 6.2.2. Limitations and Warnings

#### 6.2.2.1. Availability

[libdhcp\_cb\_cmds.so](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-ischooklib-libdhcp%5Fcb%5Fcmds.so) is available only to ISC customers with a paid support contract. For more information on subscription options, please complete the form at <https://www.isc.org/contact>. While it is theoretically possible to use the CB without this hook, this is neither supported nor recommended.

#### 6.2.2.2. Preparation is Required

The Configuration Backend is not a "plug-and-play" solution. Supported scenarios require use of the CB API commands. Configuration information must be loaded into the CB database using the API for the CB to have any effect. The general intent is for the CB to be integrated as part of a larger provisioning solution. Please do not define `config-databases` unless you have done the necessary preparation work.

#### 6.2.2.3. Database Management

The only supported method for managing the contents of the CB database is through the [libdhcp\_cb\_cmds.so](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-ischooklib-libdhcp%5Fcb%5Fcmds.so) hook, which provides API commands for config backends. As a practical matter, to use the CB, you must do almost all Kea configuration through the CB API.

While it is theoretically possible to use the CB without the API (using tools such as MySQL Workbench or the command-line MySQL client), these avenues are neither recommended nor supported.

#### 6.2.2.4. Config Conflicts

We strongly recommend against mixing configuration information from the CB and JSON config file. In other words, do not use both JSON config declarations and CB to configure the same types of objects. Ideally, when using the CB, the Kea config files should contain the absolute bare minimum necessary, with everything else coming from the CB.

Using both CB and JSON as a source of configuration risks conflicting definitions. Such conflicts are confusing at best, and usually lead to undesired behavior or errors from Kea.

In the event of a conflict, configuration instructions from the CB database generally take precedence over instructions from a JSON file.

In certain carefully-controlled scenarios, it may be technically possible to use both. For example, defining one subnet in a JSON file and a second (different) subnet in the CB database would not conflict. However, other structures are replaced entirely. For example, if client classes are defined in the CB database, the DHCP server disregards any client classes defined in the JSON file.

In short, if you are using the CB, you should use only the CB.

#### 6.2.2.5. Incompatible Software

API commands which modify Kea's configuration (other than the CB API) are contraindicated. This includes the [libdhcp\_subnet\_cmds.so](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-ischooklib-libdhcp%5Fsubnet%5Fcmds.so) hook. Its APIs modify Kea's in-memory configuration, and the modifications can only be made persistent by using `config-write` to write a new JSON config file.

The [Stork](https://stork.readthedocs.io) management suite does not currently support the CB. Stork makes all configuration changes through API avenues which expect to write changes into JSON config file. Support for the CB is planned for a future release of Stork.

In certain carefully-controlled scenarios, it may be possible to use these tools with the CB. Namely, if they are used in strictly "read-only" fashion, to retrieve Kea information, but never to modify it. However, no protection against accidental modification is provided, so this is not recommended.

#### 6.2.2.6. Limitations

Currently, the Kea CB has the following limitations:

* It is only supported for MySQL and PostgreSQL databases.
* It is only supported for the DHCPv4 and DHCPv6 daemons; the D2 daemon, and the NETCONF daemon cannot be configured from the database.
* Only certain DHCP configuration parameters can be set in the database: global parameters, option definitions, global options, client classes, shared networks, and subnets. Other configuration parameters must be sourced from a JSON configuration file.

#### 6.2.2.7. Custom Options

Using custom option formats requires creating definitions for these options. Suppose a user wishes to set option data in the configuration backend. In that case, we recommend specifying the definition for that option in the configuration backend as well. It is essential when multiple servers are managed via the configuration backend, and may differ in their configurations. The option data parser can search for an option definition appropriate for the server for which the option data is specified.

In a single-server deployment, or when all servers share the same configuration file information, it is possible to specify option definitions in the configuration files and option data in the configuration backend. The server receiving a command to set option data must have a valid definition in its configuration file, even when it sets option data for another server.

It is not supported to specify option definitions in the configuration backend and the corresponding option data in the server configuration files.

### 6.2.3. Components

The Kea Configuration Backend solution consists of the CB modules (hook libraries), the CB commands API (its own hook library), the external database software (MySQL or PostgreSQL), the database schema, and the Kea configuration information stored in the database.

In this documentation, the term "Configuration Backend" may also refer to the particular Kea module providing support for that database type. For example, the MySQL Configuration Backend, [libdhcp\_mysql.so](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-ischooklib-libdhcp%5Fmysql.so), provides a complete set of functions to manage and fetch the configuration information from a MySQL database. The PostgreSQL Configuration Backend, [libdhcp\_pgsql.so](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-ischooklib-libdhcp%5Fpgsql.so), is the corresponding module for PostgreSQL. Similarly, the term "database" is used to refer to either a MySQL or PostgreSQL database.

The CB commands API provides a complete set of commands to manage Kea configuration information, as stored within the database. This API is implemented in its own hook library, [libdhcp\_cb\_cmds.so](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-ischooklib-libdhcp%5Fcb%5Fcmds.so). This library can be attached to both DHCPv4 and DHCPv6 server instances. It simplifies many typical operations, such as listing, adding, retrieving, and deleting global parameters, shared networks, subnets, pools, options, option definitions, and client classes. In addition, it provides essential business logic that ensures the logical integrity of the data. All CB API commands start with `remote-`. See [libdhcp\_cb\_cmds.so: Configuration Backend Commands](https://kea.readthedocs.io/en/latest/arm/hooks.html#hooks-cb-cmds) for more information.

Installation and maintenance of external database software is beyond the scope of this manual.

The database schema is typically installed via the [kea-admin](https://kea.readthedocs.io/en/latest/man/kea-admin.8.html#std-iscman-kea-admin) tool. See [Installation](#cb-install) for more information. The raw schema creation scripts are [dhcpdb\_create.mysql](https://gitlab.isc.org/isc-projects/kea/blob/master/src/share/database/scripts/mysql/dhcpdb%5Fcreate.mysql)and [dhcpdb\_create.pgsql](https://gitlab.isc.org/isc-projects/kea/blob/master/src/share/database/scripts/pgsql/dhcpdb%5Fcreate.pgsql).

Use the CB commands API to populate the database with Kea configuration information.

Related design documents are available in our GitLab:

* [CB Design](https://gitlab.isc.org/isc-projects/kea/-/wikis/Designs/configuration-in-db-design)
* [Client Classes in CB Design](https://gitlab.isc.org/isc-projects/kea/-/wikis/Designs/client-classes-in-cb)

### 6.2.4. Installation

To use either Configuration Backend, the appropriate module library ([libdhcp\_mysql.so](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-ischooklib-libdhcp%5Fmysql.so) or [libdhcp\_pgsql.so](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-ischooklib-libdhcp%5Fpgsql.so)) must be compiled during the Kea build. The `-D` switch specifies which database module to build, if any: `-D mysql=enabled` or `-D postgresql=enabled`. The appropriate database client libraries and header files must be installed prior to build. See [DHCP Database Installation and Configuration](https://kea.readthedocs.io/en/latest/arm/install.html#dhcp-install-configure) for more information on building Kea with database support. ISC's Kea packaging, as well as some third-party distributions, provide separate packages for each database type.

The database server hosting the CB tables must be prepared with the Kea schema. When upgrading an existing Kea installation, the database schema may also need to be upgraded. The [kea-admin](https://kea.readthedocs.io/en/latest/man/kea-admin.8.html#std-iscman-kea-admin) tool can be used to more easily apply the schema, as described in [The kea-admin Tool](https://kea.readthedocs.io/en/latest/arm/admin.html#kea-admin).

At runtime, the DHCP servers must be configured to load the module, in the `hooks-libraries` section. A `config-databases` directive must then be used to instruct Kea to load configuration using the database backend. The DHCPv4 and DHCPv6 server-specific configurations of the CB, as well as the list of supported configuration parameters, can be found in [Configuration Backend in DHCPv4](https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#dhcp4-cb)and [Configuration Backend in DHCPv6](https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html#dhcp6-cb), respectively.

Once installation is completed, the CB commands API can be used to populate the database with Kea configuration information.

### 6.2.5. Configuration Sharing and Server Tags

The configuration database is designed to store configuration information for multiple Kea servers. Depending on the use case, the entire configuration may be shared by all servers; parts of the configuration may be shared by multiple servers and the rest of the configuration may be different for these servers; or each server may have its own non-shared configuration.

The configuration elements in the database are associated with the servers by "server tags." The server tag is an arbitrary string holding the name of the Kea server instance. The tags of the DHCPv4 and DHCPv6 servers are independent in the database, i.e. the same server tag can be created for both the DHCPv4 and the DHCPv6 server. The value is configured using the `server-tag` parameter in the `Dhcp4` or `Dhcp6` scope. The current server tag can be checked with the [server-tag-get](https://kea.readthedocs.io/en/latest/arm/ctrl-channel.html#std-isccmd-server-tag-get) command.

The server definition, which consists of the server tag and the server description, must be stored in the configuration database prior to creating the dedicated configuration for that server. In cases when all servers use the same configuration, e.g. a pair of servers running as High Availability peers, there is no need to configure the server tags for these servers in the database.

Commands which contain the logical server all are applied to all servers connecting to the database. The all server cannot be deleted or modified, and it is not returned among other servers as a result of the [remote-server4-get-all](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-isccmd-remote-server4-get-all) and [remote-server6-get-all](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-isccmd-remote-server6-get-all) commands.

In most cases, there are no server tags defined in the configuration database; all connecting servers get the same configuration regardless of the server tag they use. The server tag that a particular Kea instance presents to the database to fetch its configuration is specified in the Kea configuration file, using the config-control map (please refer to the [Enabling the Configuration Backend](https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#dhcp4-cb-json) and [Enabling the Configuration Backend](https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html#dhcp6-cb-json) for details). All Kea instances presenting the same server tag to the configuration database are given the same configuration.

It is the administrator's choice whether multiple Kea instances use the same server tag or each Kea instance uses a different server tag. There is no requirement that the instances running on the same physical or virtual machine use the same server tag. It is even possible to configure the Kea server without assigning it a server tag. In such a case the server will be given the configuration specified for allservers.

To differentiate between different Kea server configurations, a list of the server tags used by the servers must be stored in the database. For the DHCPv4 and DHCPv6 servers, this can be done using the [remote-server4-set](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-isccmd-remote-server4-set) and [remote-server6-set](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-isccmd-remote-server6-set) commands. The server tags can then be used to associate the configuration information with the servers. However, it is important to note that some DHCP configuration elements may be associated with multiple server tags (known as "shareable" elements), while other configuration elements may be associated with only one server tag ("non-shareable" elements). The [Configuration Backend in DHCPv4](https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html#dhcp4-cb)and [Configuration Backend in DHCPv6](https://kea.readthedocs.io/en/latest/arm/dhcp6-srv.html#dhcp6-cb) sections list the DHCP-specific shareable and non-shareable configuration elements; however, in this section we briefly explain the differences between them.

A shareable configuration element is one which has some unique property identifying it, and which may appear only once in the database. An example of a shareable DHCP element is a subnet instance: the subnet is a part of the network topology and we assume that any particular subnet may have only one definition within this network. Each subnet has two unique identifiers: the subnet identifier and the subnet prefix. The subnet identifier is used in Kea to uniquely identify the subnet within the network and to connect it with other configuration elements, e.g. in host reservations. Some commands provided by [libdhcp\_cb\_cmds.so](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-ischooklib-libdhcp%5Fcb%5Fcmds.so) allow the subnet information to be accessed by either subnet identifier or prefix, and explicitly prohibit using the server tag to access the subnet. This is because, in general, the subnet definition is associated with multiple servers rather than a single server. In fact, it may even be associated with no servers (unassigned). Still, the unassigned subnet has an identifier and prefix which can be used to access the subnet.

A shareable configuration element may be associated with multiple servers, one server, or no servers. Deletion of the server which is associated with the shareable element does not cause the deletion of the shareable element. It merely deletes the association of the deleted server with the element.

Unlike a shareable element, a non-shareable element must not be explicitly associated with more than one server and must not exist after the server is deleted (must not remain unassigned). A non-shareable element only exists within the context of the server. An example of a non-shareable element in DHCP is a global parameter, e.g. renew-timer. The renew timer is the value to be used by a particular server and only this server. Other servers may have their respective renew timers set to the same or different values. The renew timer parameter has no unique identifier by which it could be accessed, modified, or otherwise used. Global parameters like the renew timer can be accessed by the parameter name and the tag of the server for which they are configured. For example, the [remote-global-parameter4-get](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-isccmd-remote-global-parameter4-get) and [remote-global-parameter6-get](https://kea.readthedocs.io/en/latest/arm/hooks.html#std-isccmd-remote-global-parameter6-get) commands allow the value of the global parameter to be fetched by the parameter name and the server name. Getting the global parameter only by its name (without specifying the server tag) is not possible, because there may be many global parameters with a given name in the database.

When the server associated with a non-shareable configuration element is deleted, the configuration element is automatically deleted from the database along with the server because the non-shareable element must be always assigned to a server (or the logical server all).

The terms "shareable" and "non-shareable" only apply to associations with user-defined servers; all configuration elements associated with the logical server all are by definition shareable. For example: the renew-timer associated with all servers is used by all servers connecting to the database which do not have their specific renew timers defined. In a special case, when none of the configuration elements are associated with user-defined servers, the entire configuration in the database is shareable because all its pieces belong to all servers.

Note

Be very careful when associating configuration elements with different server tags. The configuration backend does not protect against some possible misconfigurations that may arise from the wrong server tags' assignments. For example: if a shared network is assigned to one server and the subnets belonging to this shared network to another server, the servers will fail upon trying to fetch and use this configuration. The server fetching the subnets will be aware that the subnets are associated with the shared network, but the shared network will not be found by this server since it doesn't belong to it. In such a case, both the shared network and the subnets should be assigned to the same set of servers.
