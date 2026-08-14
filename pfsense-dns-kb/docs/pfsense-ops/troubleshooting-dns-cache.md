---
source_url: https://docs.netgate.com/pfsense/en/latest/troubleshooting/dns-cache.html
title: Troubleshooting the DNS Cache | pfSense Documentation
category: pfsense-ops
priority: 3
pfsense_version_notes: 
fetched_date: 2026-08-13
converter: bs4+html2text
---

# Troubleshooting the DNS Cache¶

## DNS Resolver¶

To fully clear the DNS Resolver cache, restart the `unbound` daemon:

  * Navigate to **Status > Services**

  * Find `unbound` in the list

  * Click ![fa-arrow-rotate-right](../_images/fa-arrow-rotate-right.png) (restart) or click ![fa-stop-circle](../_images/fa-stop-circle.png) (stop) then ![fa-play-circle](../_images/fa-play-circle.png) (start)




Restarting the daemon will clear the internal cache, but client PCs may still have cached responses.

Alternately, issue a `reload` command using the CLI which will flush the cache without stopping the daemon:
    
    
    unbound-control -c /var/unbound/unbound.conf reload
    

To selectively clear the DNS Resolver cache at the command line, run:
    
    
    unbound-control -c /var/unbound/unbound.conf flush <name>
    

Where `<name>` is a domain name or hostname to be cleared.

Inspect the contents of the cache from the command line using:
    
    
    unbound-control -c /var/unbound/unbound.conf dump_cache
    

## DNS Forwarder¶

To clear the DNS Forwarder cache, restart the `dnsmasq` daemon:

  * Navigate to **Status > Services**

  * Find `dnsmasq` in the list

  * Click ![fa-arrow-rotate-right](../_images/fa-arrow-rotate-right.png) (restart) or click ![fa-stop-circle](../_images/fa-stop-circle.png) (stop) then ![fa-play-circle](../_images/fa-play-circle.png) (start)




Restarting the daemon will clear the internal cache, but client PCs may still have cached responses.

## Client DNS Cache¶

The DNS cache on a Windows PC may be cleaned from a command prompt or **Start > Run**:
    
    
    ipconfig /flushdns
    

This may need to be executed from an Administrator command prompt on Windows Vista and later.

Other operating systems will surely have other means to clear the DNS resolver cache. For example, Ubuntu-based distributions also use _dnsmasq_ , and it may be restarted using:
    
    
    sudo service network-manager restart
    

Browsers also have their own internal DNS caches separate from the OS. Close and re-open the browser if none of the above help.

As a last resort, rebooting/restarting a client will surely clear any locally cached data.
