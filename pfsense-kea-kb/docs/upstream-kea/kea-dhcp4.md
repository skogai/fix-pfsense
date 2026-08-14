---
source_url: https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
title: 8. The DHCPv4 Server
category: upstream-kea
priority: 2
pfsense_version_notes:
fetched_date: 2026-08-13
converter: webfetch
---

# 8. The DHCPv4 Server

## 8.1. Starting and Stopping the DHCPv4 Server

It is recommended that the Kea DHCPv4 server be started and stopped using [keactrl](https://kea.readthedocs.io/en/latest/man/keactrl.8.html#std-iscman-keactrl) (described in [Managing Kea with keactrl](https://kea.readthedocs.io/en/latest/arm/keactrl.html#keactrl)); however, it is also possible to run the server directly via the [kea-dhcp4](https://kea.readthedocs.io/en/latest/man/kea-dhcp4.8.html#std-iscman-kea-dhcp4) command, which accepts the following command-line switches:

* `-c file` \- specifies the configuration file. This is the only mandatory switch.
* `-d` \- specifies whether the server logging should be switched to debug/verbose mode. In verbose mode, the logging severity and debuglevel specified in the configuration file are ignored; "debug" severity and the maximum debuglevel (99) are assumed. The flag is convenient for temporarily switching the server into maximum verbosity, e.g. when debugging.
* `-p server-port` \- specifies the local UDP port on which the server listens. This is only useful during testing, as a DHCPv4 server listening on ports other than the standard ones is not able to handle regular DHCPv4 queries.
* `-P client-port` \- specifies the remote UDP port to which the server sends all responses. This is only useful during testing, as a DHCPv4 server sending responses to ports other than the standard ones is not able to handle regular DHCPv4 queries.
* `-t file` \- specifies a configuration file to be tested. [kea-dhcp4](https://kea.readthedocs.io/en/latest/man/kea-dhcp4.8.html#std-iscman-kea-dhcp4)loads it, checks it, and exits. During the test, log messages are printed to standard output and error messages to standard error. The result of the test is reported through the exit code (0 = configuration looks OK, 1 = error encountered). The check is not comprehensive; certain checks are possible only when running the server.
* `-T file` \- specifies a configuration file to be tested. [kea-dhcp4](https://kea.readthedocs.io/en/latest/man/kea-dhcp4.8.html#std-iscman-kea-dhcp4)loads it, checks it, and exits. It performs extra checks beyond what `-t`offers, such as establishing database connections (for the lease backend, host reservations backend, configuration backend, and forensic logging backend), loading hook libraries, parsing hook-library configurations, etc. It does not open UNIX or TCP/UDP sockets, lock files, nor does it open or rotate files, as any of these actions could interfere with a running process on the same machine.
* `-v` \- displays the Kea version and exits.
* `-V` \- displays the Kea extended version with additional parameters and exits. The listing includes the versions of the libraries dynamically linked to Kea.
* `-W` \- displays the Kea configuration report and exits. The report is a copy of the `config.report` file produced by `meson setup`; it is embedded in the executable binary.  
The contents of the `config.report` file may also be accessed by examining certain libraries in the installation tree or in the source tree.  
# from installation using libkea-process.so  
$ strings ${prefix}/lib/libkea-process.so | sed -n 's/;;;; //p'  
# from sources using libkea-process.so  
$ strings src/lib/process/.libs/libkea-process.so | sed -n 's/;;;; //p'  
# from sources using libkea-process.a  
$ strings src/lib/process/.libs/libcfgrpt.a | sed -n 's/;;;; //p'  
# from sources using libcfgrpt.a  
$ strings src/lib/process/cfgrpt/.libs/libcfgrpt.a | sed -n 's/;;;; //p'
* `-X` \- As of Kea 3.0, disables security restrictions. The server will still check for violations but will emit warning logs when they are found rather than fail with an error. Please see [Kea Runtime Security Policy Checking](https://kea.readthedocs.io/en/latest/arm/security.html#sec-kea-runtime-security-policy-checking) for details.
* `-F` \- As of Kea 3.3.0, makes the server exit immediately on any fatal error detected when executing API commands. Default behavior (parameter not set) is to just log the error and continue, making it possible for an administrator to intervene and fix the issue without restarting the server.

Note

Kea packages provided on [ISC's Cloudsmith repositories](https://cloudsmith.io/~isc/repos) include service files prepared for easy overrides that add command-line switches to the server.

For **systemd** based distributions, the override file should be located in `/etc/systemd/system/isc-kea-dhcp4-server.service.d/`(or for RPM packages `/etc/systemd/system/kea-dhcp4.service.d/`) directory and have a `.conf` extension.

Example file contents:

[Service]
Environment="KEA_DHCP4_OPTIONS=-F -X"

For **OpenRC** based distributions, the override file must be `/etc/conf.d/kea-dhcp4`.

Example file contents:

options="-F -d"

On startup, the server detects available network interfaces and attempts to open UDP sockets on all interfaces listed in the configuration file. Since the DHCPv4 server opens privileged ports, it requires root access; this daemon must be run as root.

During startup, the server attempts to create a PID file of the form: `[pidfile_dir]/[conf name].kea-dhcp4.pid` where:

* `pidfile_dir` \- is `[prefix]/[localstatedir]/run/kea` where `prefix` and `localstatedir` are the values passed into meson setup using `--prefix` and `--localstatedir` which default to `/usr/local` and `var` respectively. So the whole `pidfile_dir` defaults to `/usr/local/var`. Note that this value may be overridden at runtime by setting the environment variable `KEA_PIDFILE_DIR` intended primarily for testing purposes.
* `conf name`: The configuration file name used to start the server, minus all preceding paths and the file extension. For example, given a pathname of `/usr/local/etc/kea/myconf.txt`, the portion used would be `myconf`.

If the file already exists and contains the PID of a live process, the server issues a `DHCP4_ALREADY_RUNNING` log message and exits. It is possible, though unlikely, that the file is a remnant of a system crash and the process to which the PID belongs is unrelated to Kea. In such a case, it would be necessary to manually delete the PID file.

The server can be stopped using the `kill` command. When running in a console, the server can also be shut down by pressing Ctrl-c. Kea detects the key combination and shuts down gracefully.

The reconfiguration of each Kea server is triggered by the SIGHUP signal. When a server receives the SIGHUP signal it rereads its configuration file and, if the new configuration is valid, uses the new configuration. If the new configuration proves to be invalid, the server retains its current configuration; however, in some cases a fatal error message is logged indicating that the server is no longer providing any service: a working configuration must be loaded as soon as possible.

## 8.2. DHCPv4 Server Configuration

### 8.2.1. Introduction

This section explains how to configure the Kea DHCPv4 server using a configuration file.

Before DHCPv4 is started, its configuration file must be created. The basic configuration is as follows:

{
# DHCPv4 configuration starts on the next line
"Dhcp4": {

# First we set up global values
    "valid-lifetime": 4000,
    "renew-timer": 1000,
    "rebind-timer": 2000,

# Next we set up the interfaces to be used by the server.
    "interfaces-config": {
        "interfaces": [ "eth0" ]
    },

# And we specify the type of lease database
    "lease-database": {
        "type": "memfile",
        "persist": true,
        "name": "/var/lib/kea/dhcp4.leases"
    },

# Finally, we list the subnets from which we will be leasing addresses.
    "subnet4": [
        {
            "id": 1,
            "subnet": "192.0.2.0/24",
            "pools": [
                {
                    "pool": "192.0.2.1 - 192.0.2.200"
                }
            ]
        }
    ]
# DHCPv4 configuration ends with the next line
}

}

The following paragraphs provide a brief overview of the parameters in the above example, along with their format. Subsequent sections of this chapter go into much greater detail for these and other parameters.

The lines starting with a hash (#) are comments and are ignored by the server; they do not impact its operation in any way.

The configuration starts in the first line with the initial opening curly bracket (or brace). Each configuration must contain an object specifying the configuration of the Kea module using it. In the example above, this object is called `Dhcp4`.

The `Dhcp4` configuration starts with the `"Dhcp4": {` line and ends with the corresponding closing brace (in the above example, the brace after the last comment). Everything defined between those lines is considered to be the `Dhcp4` configuration.

In general, the order in which those parameters appear does not matter, but there are two caveats. The first one is that the configuration file must be well-formed JSON, meaning that the parameters for any given scope must be separated by a comma, and there must not be a comma after the last parameter. When reordering a configuration file, moving a parameter to or from the last position in a given scope may also require moving the comma. The second caveat is that it is uncommon — although legal JSON — to repeat the same parameter multiple times. If that happens, the last occurrence of a given parameter in a given scope is used, while all previous instances are ignored. This is unlikely to cause any confusion as there are no real-life reasons to keep multiple copies of the same parameter in the configuration file.

The first few DHCPv4 configuration elements define some global parameters. `valid-lifetime` defines how long the addresses (leases) given out by the server are valid; the default is for a client to be allowed to use a given address for 4000 seconds. (Note that integer numbers are specified as is, without any quotes around them.) `renew-timer` and `rebind-timer` are values (also in seconds) that define the T1 and T2 timers that govern when the client begins the renewal and rebind processes.

Note

The lease valid lifetime is expressed as a triplet with minimum, default, and maximum values using configuration entries `min-valid-lifetime`, `valid-lifetime`, and `max-valid-lifetime`. Since Kea 1.9.5, these values may be specified in client classes. The procedure the server uses to select which lifetime value to use is as follows:

If the client query is a BOOTP query, the server always uses the infinite lease time (e.g. 0xffffffff). Otherwise, the server must determine which configured triplet to use by first searching all classes assigned to the query, and then the subnet selected for the query.

Classes are searched in the order they were assigned to the query; the server uses the triplet from the first class that specifies it. If no classes specify the triplet, the server uses the triplet specified by the subnet selected for the client. If the subnet does not explicitly specify it, the server next looks at the subnet's shared-network (if one exists), then for a global specification, and finally the global default.

If the client requested a lifetime value via DHCP option 51, then the lifetime value used is the requested value bounded by the configured triplet. In other words, if the requested lifetime is less than the configured minimum, the configured minimum is used; if it is more than the configured maximum, the configured maximum is used. If the client did not provide a requested value, the lifetime value used is the triplet default value.

Note

Both `renew-timer` and `rebind-timer`are optional. The server only sends `rebind-timer` to the client, via DHCPv4 option code 59, if it is less than `valid-lifetime`; and it only sends `renew-timer`, via DHCPv4 option code 58, if it is less than `rebind-timer` (or `valid-lifetime` if `rebind-timer` was not specified). In their absence, the client should select values for T1 and T2 timers according to [RFC 2131](https://datatracker.ietf.org/doc/html/rfc2131). See section [Sending T1 (Option 58) and T2 (Option 59)](#dhcp4-t1-t2-times)for more details on generating T1 and T2.

The `interfaces-config` map specifies the network interfaces on which the server should listen to DHCP messages. The `interfaces` parameter specifies a list of network interfaces on which the server should listen. Lists are opened and closed with square brackets, with elements separated by commas. To listen on two interfaces, the `interfaces-config` element should look like this:

{
"interfaces-config": {
    "interfaces": [ "eth0", "eth1" ]
},
...
}

The next lines define the lease database, the place where the server stores its lease information. This particular example tells the server to use memfile, which is the simplest and fastest database backend. It uses an in-memory database and stores leases on disk in a CSV (comma-separated values) file. This is a very simple configuration example; usually the lease database configuration is more extensive and contains additional parameters. Note that `lease-database` is an object and opens up a new scope, using an opening brace. Its parameters (just one in this example: `type`) follow. If there were more than one, they would be separated by commas. This scope is closed with a closing brace. As more parameters for the `Dhcp4` definition follow, a trailing comma is present.

Finally, we need to define a list of IPv4 subnets. This is the most important DHCPv4 configuration structure, as the server uses that information to process clients' requests. It defines all subnets from which the server is expected to receive DHCP requests. The subnets are specified with the `subnet4` parameter. It is a list, so it starts and ends with square brackets. Each subnet definition in the list has several attributes associated with it, so it is a structure and is opened and closed with braces. At a minimum, a subnet definition must have at least two parameters: `subnet`, which defines the whole subnet; and `pools`, which is a list of dynamically allocated pools that are governed by the DHCP server.

The example contains a single subnet. If more than one were defined, additional elements in the `subnet4` parameter would be specified and separated by commas. For example, to define three subnets, the following syntax would be used:

{
"subnet4": [
    {
        "id": 1,
        "pools": [ { "pool":  "192.0.2.1 - 192.0.2.200" } ],
        "subnet": "192.0.2.0/24"
    },
    {
        "id": 2,
        "pools": [ { "pool": "192.0.3.100 - 192.0.3.200" } ],
        "subnet": "192.0.3.0/24"
    },
    {
        "id": 3,
        "pools": [ { "pool": "192.0.4.1 - 192.0.4.254" } ],
        "subnet": "192.0.4.0/24"
    }
],
...
}

Note that indentation is optional and is used for aesthetic purposes only. In some cases it may be preferable to use more compact notation.

After all the parameters have been specified, there are two contexts open: `global` and `Dhcp4`; thus, two closing curly brackets must be used to close them.

### 8.2.2. Lease Storage

All leases issued by the server are stored in the lease database. There are three database backends available: memfile (the default), MySQL, PostgreSQL.

#### 8.2.2.1. Memfile - Basic Storage for Leases

The server is able to store lease data in different repositories. Larger deployments may elect to store leases in a database; [Lease Database Configuration](#database-configuration4) describes this option. In typical smaller deployments, though, the server stores lease information in a CSV file rather than a database. As well as requiring less administration, an advantage of using a file for storage is that it eliminates a dependency on third-party database software.

The configuration of the memfile backend is controlled through the `Dhcp4`/`lease-database` parameters. The `type` parameter is mandatory and specifies which storage for leases the server should use, through the `"memfile"` value. The following list gives additional optional parameters that can be used to configure the memfile backend.

* `persist`: controls whether the new leases and updates to existing leases are written to the file. It is strongly recommended that the value of this parameter be set to `true` at all times during the server's normal operation. Not writing leases to disk means that if a server is restarted (e.g. after a power failure), it will not know which addresses have been assigned. As a result, it may assign new clients addresses that are already in use. The value of `false` is mostly useful for performance-testing purposes. The default value of the `persist` parameter is `true`, which enables writing lease updates to the lease file.
* `name`: specifies the lease file in which new leases and lease updates are recorded. The default value for this parameter is `"[kea-install-dir]/var/lib/kea/kea-leases4.csv"`.

Note

As of Kea 2.7.9, lease files may only be loaded from the data directory determined during compilation: `"[kea-install-dir]/var/lib/kea"`. This path may be overridden at startup by setting the environment variable `KEA_DHCP_DATA_DIR` to the desired path. If a path other than this value is used in `name`, Kea will emit an error and refuse to start or, if already running, log an unrecoverable error. For ease of use in specifying a custom file name simply omit the path component from `name`.

* `lfc-interval`: specifies the interval, in seconds, at which the server will perform a lease file cleanup (LFC). This removes redundant (historical) information from the lease file and effectively reduces the lease file size. The cleanup process is described in more detail later in this section. The default value of the `lfc-interval` is `3600`. A value of `0` disables the LFC.
* `max-row-errors`: specifies the number of row errors before the server stops attempting to load a lease file. When the server loads a lease file, it is processed row by row, each row containing a single lease. If a row is flawed and cannot be processed correctly the server logs it, discards the row, and goes on to the next row. This parameter can be used to set a limit on the number of such discards that can occur, after which the server abandons the effort and exits. The default value of `0` disables the limit and allows the server to process the entire file, regardless of how many rows are discarded.

An example configuration of the memfile backend is presented below:

"Dhcp4": {
    "lease-database": {
        "type": "memfile",
        "persist": true,
        "name": "kea-leases4.csv",
        "lfc-interval": 1800,
        "max-row-errors": 100
    }
}

This configuration selects `kea-leases4.csv` as the storage for lease information and enables persistence (writing lease updates to this file). It also configures the backend to perform a periodic cleanup of the lease file every 1800 seconds (30 minutes) and sets the maximum number of row errors to 100.

#### 8.2.2.2. Why Is Lease File Cleanup Necessary?

It is important to know how the lease file contents are organized to understand why the periodic lease file cleanup is needed. Every time the server updates a lease or creates a new lease for a client, the new lease information must be recorded in the lease file. For performance reasons, the server does not update the existing client's lease in the file, as this would potentially require rewriting the entire file. Instead, it simply appends the new lease information to the end of the file; the previous lease entries for the client are not removed. When the server loads leases from the lease file, e.g. at server startup, it assumes that the latest lease entry for the client is the valid one. Previous entries are discarded, meaning that the server can reconstruct accurate information about the leases even though there may be many lease entries for each client. However, storing many entries for each client results in a bloated lease file and impairs the performance of the server's startup and reconfiguration, as it needs to process a larger number of lease entries.

Lease file cleanup (LFC) removes all previous entries for each client and leaves only the latest ones. The interval at which the cleanup is performed is configurable, and it should be selected according to the frequency of lease renewals initiated by the clients. The more frequent the renewals, the smaller the value of `lfc-interval` should be. Note, however, that the LFC takes time and thus it is possible (although unlikely) that, if the `lfc-interval` is too short, a new cleanup may be started while the previous one is still running. The server would recover from this by skipping the new cleanup when it detected that the previous cleanup was still in progress, but it implies that the actual cleanups will be triggered more rarely than the configured interval. Moreover, triggering a new cleanup adds overhead to the server, which is not able to respond to new requests for a short period of time when the new cleanup process is spawned. Therefore, it is recommended that the `lfc-interval` value be selected in a way that allows the LFC to complete the cleanup before a new cleanup is triggered.

Lease file cleanup is performed by a separate process (in the background) to avoid a performance impact on the server process. To avoid conflicts between two processes using the same lease files, the LFC process starts with Kea opening a new lease file; the actual LFC process operates on the lease file that is no longer used by the server. There are also other files created as a side effect of the lease file cleanup. The detailed description of the LFC process is located later in this Kea Administrator's Reference Manual: [The LFC Process](https://kea.readthedocs.io/en/latest/arm/lfc.html#kea-lfc).

#### 8.2.2.3. Lease Database Configuration

Note

Lease database access information must be configured for the DHCPv4 server, even if it has already been configured for the DHCPv6 server. The servers store their information independently, so each server can use a separate database or both servers can use the same database.

Note

Kea requires the database timezone to match the system timezone. For more details, see [First-Time Creation of the MySQL Database](https://kea.readthedocs.io/en/latest/arm/admin.html#mysql-database-create) and [First-Time Creation of the PostgreSQL Database](https://kea.readthedocs.io/en/latest/arm/admin.html#pgsql-database-create).

Lease database configuration is controlled through the `Dhcp4`/`lease-database` parameters. The database type must be set to `memfile`, `mysql` or `postgresql`, e.g.:

"Dhcp4": { "lease-database": { "type": "mysql", ... }, ... }

Next, the name of the database to hold the leases must be set; this is the name used when the database was created (see [First-Time Creation of the MySQL Database](https://kea.readthedocs.io/en/latest/arm/admin.html#mysql-database-create) or [First-Time Creation of the PostgreSQL Database](https://kea.readthedocs.io/en/latest/arm/admin.html#pgsql-database-create)).

For MySQL or PostgreSQL:

"Dhcp4": { "lease-database": { "name": "database-name" , ... }, ... }

If the database is located on a different system from the DHCPv4 server, the database host name must also be specified:

"Dhcp4": { "lease-database": { "host": "remote-host-name", ... }, ... }

Normally, the database is on the same machine as the DHCPv4 server. In this case, set the value to the empty string:

"Dhcp4": { "lease-database": { "host" : "", ... }, ... }

Should the database use a port other than the default, it may be specified as well:

"Dhcp4": { "lease-database": { "port" : 12345, ... }, ... }

Should the database be located on a different system, the administrator may need to specify a longer interval for the connection timeout:

"Dhcp4": { "lease-database": { "connect-timeout" : timeout-in-seconds, ... }, ... }

The default value of five seconds should be more than adequate for local connections. If a timeout is given, though, it should be an integer greater than zero.

The maximum number of times the server automatically attempts to reconnect to the lease database after connectivity has been lost may be specified:

"Dhcp4": { "lease-database": { "max-reconnect-tries" : number-of-tries, ... }, ... }

If the server is unable to reconnect to the database after making the maximum number of attempts, the server will exit. A value of 0 (the default) disables automatic recovery and the server will exit immediately upon detecting a loss of connectivity (MySQL and PostgreSQL only).

The number of milliseconds the server waits between attempts to reconnect to the lease database after connectivity has been lost may also be specified:

"Dhcp4": { "lease-database": { "reconnect-wait-time" : number-of-milliseconds, ... }, ... }

The default value for MySQL and PostgreSQL is 0, which disables automatic recovery and causes the server to exit immediately upon detecting the loss of connectivity.

"Dhcp4": { "lease-database": { "on-fail" : "stop-retry-exit", ... }, ... }

The possible values are:

* `stop-retry-exit` \- disables the DHCP service while trying to automatically recover lost connections, and shuts down the server on failure after exhausting `max-reconnect-tries`. This is the default value for the lease backend, the host backend, and the configuration backend.
* `serve-retry-exit` \- continues the DHCP service while trying to automatically recover lost connections, and shuts down the server on failure after exhausting `max-reconnect-tries`.
* `serve-retry-continue` \- continues the DHCP service and does not shut down the server even if the recovery fails. This is the default value for forensic logging.

Note

Automatic reconnection to database backends is configured individually per backend; this allows users to tailor the recovery parameters to each backend they use. We suggest that users enable it either for all backends or none, so behavior is consistent.

Losing connectivity to a backend for which reconnection is disabled results (if configured) in the server shutting itself down. This includes cases when the lease database backend and the hosts database backend are connected to the same database instance.

It is highly recommended not to change the `stop-retry-exit` default setting for the lease manager, as it is critical for the connection to be active while processing DHCP traffic. Change this only if the server is used exclusively as a configuration tool.

"Dhcp4": { "lease-database": { "retry-on-startup" : true, ... }, ... }

During server startup, the inability to connect to any of the configured backends is considered fatal only if `retry-on-startup` is set to `false`(the default). A fatal error is logged and the server exits, based on the idea that the configuration should be valid at startup. Exiting to the operating system allows nanny scripts to detect the problem. If `retry-on-startup` is set to `true`, the server starts reconnection attempts even at server startup or on reconfigure events, and honors the action specified in the `on-fail` parameter.

The host parameter is used by the MySQL and PostgreSQL backends.

Finally, the credentials of the account under which the server will access the database should be set:

"Dhcp4": {
    "lease-database": {
        "user": "user-name",
        "password": "1234",
        ...
    },
    ...
}

If there is no password to the account, set the password to the empty string `""`. (This is the default.)

#### 8.2.2.4. Tuning Database Timeouts

In rare cases, reading or writing to the database may hang. This can be caused by a temporary network issue, or by misconfiguration of the proxy server switching the connection between different database instances. These situations are rare, but users have reported that Kea sometimes hangs while performing database IO operations. Setting appropriate timeout values can mitigate such issues.

MySQL exposes two distinct connection options to configure the read and write timeouts. Kea's corresponding `read-timeout` and `write-timeout`configuration parameters specify the timeouts in seconds. For example:

"Dhcp4": { "lease-database": { "read-timeout" : 10, "write-timeout": 20, ... }, ... }

Setting these parameters to 0 is equivalent to not specifying them, and causes the Kea server to establish a connection to the database with the MySQL defaults. In this case, Kea waits indefinitely for the completion of the read and write operations.

MySQL versions earlier than 5.6 do not support setting timeouts for read and write operations. Moreover, the `read-timeout` and `write-timeout`parameters can only be specified for the MySQL backend; setting them for any other backend database type causes a configuration error.

To set a timeout in seconds for PostgreSQL, use the `tcp-user-timeout`parameter. For example:

"Dhcp4": { "lease-database": { "tcp-user-timeout" : 10, ... }, ... }

Specifying this parameter for other backend types causes a configuration error.

Note

The timeouts described here are only effective for TCP connections. Please note that the MySQL client library used by the Kea servers typically connects to the database via a UNIX domain socket when the `host` parameter is `localhost`, but establishes a TCP connection for `127.0.0.1`.

Since Kea.2.7.4, the libdhcp\_mysql.so hook library must be loaded in order to store leases in the MySQL Lease Database Backend. Specify the lease backend hook library location:

"Dhcp4": { "hooks-libraries": [
    {
        // the MySQL lease backend hook library required for lease storage.
        "library": "libdhcp_mysql.so"
    }, ... ], ... }

Since Kea.2.7.4, the libdhcp\_pgsql.so hook library must be loaded in order to store leases in the PostgreSQL Lease Database Backend. Specify the lease backend hook library location.

"Dhcp4": { "hooks-libraries": [
    {
        // the PostgreSQL lease backend hook library required for lease storage.
        "library": "libdhcp_pgsql.so"
    }, ... ], ... }

### 8.2.3. Hosts Storage

Kea is also able to store information about host reservations in the database. The hosts database configuration uses the same syntax as the lease database. In fact, the Kea server opens independent connections for each purpose, be it lease or hosts information, which gives the most flexibility. Kea can keep leases and host reservations separately, but can also point to the same database. Currently the supported hosts database types are MySQL and PostgreSQL.

The following configuration can be used to configure a connection to MySQL:

"Dhcp4": {
    "hosts-databases": [ {
        "type": "mysql",
        "name": "kea",
        "user": "kea",
        "password": "1234",
        "host": "localhost",
        "port": 3306
    } ]
}

Depending on the database configuration, many of the parameters may be optional.

Please note that usage of hosts storage is optional. A user can define all host reservations in the configuration file, and that is the recommended way if the number of reservations is small. However, when the number of reservations grows, it is more convenient to use host storage. Please note that both storage methods (the configuration file and one of the supported databases) can be used together. If hosts are defined in both places, the definitions from the configuration file are checked first and external storage is checked later, if necessary.

Host information can be placed in multiple stores. Operations are performed on the stores in the order they are defined in the configuration file, although this leads to a restriction in ordering in the case of a host reservation addition; read-only stores must be configured after a (required) read-write store, or the addition will fail.

Note

Kea requires the database timezone to match the system timezone. For more details, see [First-Time Creation of the MySQL Database](https://kea.readthedocs.io/en/latest/arm/admin.html#mysql-database-create) and [First-Time Creation of the PostgreSQL Database](https://kea.readthedocs.io/en/latest/arm/admin.html#pgsql-database-create).

#### 8.2.3.1. DHCPv4 Hosts Database Configuration

Hosts database configuration is controlled through the `Dhcp4`/`hosts-databases` parameters. If enabled, the type of database must be set to a valid type e.g. `mysql` or `postgresql`.

"Dhcp4": { "hosts-databases": [ { "type": "mysql", ... } ], ... }

Since the multiple-storage extension the database configurations must be placed in a `hosts-databases` list.

Note

The previous keyword `hosts-database` which takes one database configuration only is deprecated and will be rejected by a future release. It is translated to `hosts-databases` when returned by `config-get`or output by `config-write`.

Next, the name of the database to hold the reservations must be set; this is the name used when the lease database was created (see [Supported Backends](https://kea.readthedocs.io/en/latest/arm/admin.html#supported-databases) for instructions on how to set up the desired database type):

"Dhcp4": { "hosts-databases": [ { "name": "database-name" , ... } ], ... }

If the database is located on a different system than the DHCPv4 server, the database host name must also be specified:

"Dhcp4": { "hosts-databases": [ { "host": remote-host-name, ... } ], ... }

Normally, the database is on the same machine as the DHCPv4 server. In this case, set the value to the empty string:

"Dhcp4": { "hosts-databases": [ { "host" : "", ... } ], ... }

Should the database use a port different than the default, it may be specified as well:

"Dhcp4": { "hosts-databases": [ { "port" : 12345, ... } ], ... }

The maximum number of times the server automatically attempts to reconnect to the host database after connectivity has been lost may be specified:

"Dhcp4": { "hosts-databases": [ { "max-reconnect-tries" : number-of-tries, ... } ], ... }

If the server is unable to reconnect to the database after making the maximum number of attempts, the server will exit. A value of 0 (the default) disables automatic recovery and the server will exit immediately upon detecting a loss of connectivity (MySQL and PostgreSQL only).

The number of milliseconds the server waits between attempts to reconnect to the host database after connectivity has been lost may also be specified:

"Dhcp4": { "hosts-databases": [ { "reconnect-wait-time" : number-of-milliseconds, ... } ], ... }

The default value for MySQL and PostgreSQL is 0, which disables automatic recovery and causes the server to exit immediately upon detecting the loss of connectivity.

"Dhcp4": { "hosts-databases": [ { "on-fail" : "stop-retry-exit", ... } ], ... }

The possible values are:

* `stop-retry-exit` \- disables the DHCP service while trying to automatically recover lost connections. Shuts down the server on failure after exhausting `max-reconnect-tries`. This is the default value for MySQL and PostgreSQL.
* `serve-retry-exit` \- continues the DHCP service while trying to automatically recover lost connections. Shuts down the server on failure after exhausting `max-reconnect-tries`.
* `serve-retry-continue` \- continues the DHCP service and does not shut down the server even if the recovery fails.

Note

Automatic reconnection to database backends is configured individually per backend. This allows users to tailor the recovery parameters to each backend they use. We suggest that users enable it either for all backends or none, so behavior is consistent.

Losing connectivity to a backend for which reconnection is disabled results (if configured) in the server shutting itself down. This includes cases when the lease database backend and the hosts database backend are connected to the same database instance.

"Dhcp4": { "hosts-databases": [ { "retry-on-startup" : true, ... } ], ... }

During server startup, the inability to connect to any of the configured backends is considered fatal only if `retry-on-startup` is set to `false`(the default). A fatal error is logged and the server exits, based on the idea that the configuration should be valid at startup. Exiting to the operating system allows nanny scripts to detect the problem. If `retry-on-startup` is set to `true`, the server starts reconnection attempts even at server startup or on reconfigure events, and honors the action specified in the `on-fail` parameter.

Finally, the credentials of the account under which the server will access the database should be set:

"Dhcp4": {
    "hosts-databases": [ {
        "user": "user-name",
        "password": "1234",
        ...
    } ],
    ...
}

If there is no password to the account, set the password to the empty string `""`. (This is the default.)

If the same host is configured both in-file and in-database, Kea does not issue a warning, as it would if both were specified in the same data source. Instead, the host configured in-file has priority over the one configured in-database.

#### 8.2.3.2. Using Read-Only Databases for Host Reservations With DHCPv4

In some deployments, the user whose name is specified in the database backend configuration may not have write privileges to the database. This is often required by the policy within a given network to secure the data from being unintentionally modified. In many cases administrators have deployed inventory databases, which contain substantially more information about the hosts than just the static reservations assigned to them. The inventory database can be used to create a view of a Kea hosts database and such a view is often read-only.
