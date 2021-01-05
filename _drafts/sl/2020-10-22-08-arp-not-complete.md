---
layout: post
date: 10-22-2020
title: ARP poisoning Lab
category: 
author: 
tags: 
mathjax: 
---

ARP cache poisoning or ARP spoofing described in a [Wikipedia article](https://en.wikipedia.org/wiki/ARP_spoofing)

As usual with our network challenges, we use docker-compose to set up our network

```yaml
version: '3'

services:
  alice:
    image: thierrysans/alice:arp-spoofing
    container_name: alice
    networks:
      legitimate:
        ipv4_address: 10.0.0.2
    cap_add:
      - NET_ADMIN

  mallory:
      image: thierrysans/mallory:arp-spoofing
      container_name: mallory
      tty: true
      restart: always
      cap_add:
        - NET_ADMIN
        - SYS_ADMIN
      volumes:
          - .:/shared
      networks:
        legitimate:
          ipv4_address: 10.0.0.3
        malicious:
          ipv4_address: 10.0.1.3
  
  wireshark:
    image: thierrysans/wireshark:malicious-gateway
    container_name: wireshark
    tty: true
    network_mode: service:alice

networks:
  legitimate:
    driver: bridge
    ipam:
      config:
        - subnet: 10.0.0.0/24
  malicious:
    driver: bridge
    ipam:
      config:
        - subnet: 10.0.1.0/24
```

we have a similar setup [as usual]()
for pulling images

We have Alice simply trying to connect similar to a [previous post]()

```javascript
const request = require('request');

const url = "http://welcome.seclab.space/";

const TIMEOUT = 5000

var do_request = function(){
    request.get({url: url, timeout: TIMEOUT}, function (err, response, body) {
        if (err) return console.log(err);
        if (response.statusCode != 200) return console.log("[" + response.statusCode + "]");
        console.log("[" + response.statusCode + "] " + body);
        var words = body.trim().split(' ');
        if (words[words.length-1] === "DarkLab"){
            console.log(" ==>  sending the flag");
            request.get({url: url + "?flag=mallory-is-on-the-local-network", timeout: TIMEOUT});
        }
    });
};

setInterval(do_request, TIMEOUT);
```

running `docker-compose up alice` we see Alice connects to the
website no problem.

Now for the attack, running
`docker exec -it mallory bash` we get an interactive shell for mallory. we fist go into our shared
directory and run `route` to see the IP routing table

```
root@mallory:/shared# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         10.0.1.1        0.0.0.0         UG    0      0        0 eth1
10.0.0.0        0.0.0.0         255.255.255.0   U     0      0        0 eth0
10.0.1.0        0.0.0.0         255.255.255.0   U     0      0        0 eth1
```


```
root@mallory:/shared# arp
Address                  HWtype  HWaddress           Flags Mask            Iface
10.0.0.1                 ether   02:42:6a:03:98:2f   C                     eth0
10.0.0.2                 ether   02:42:0a:00:00:02   C                     eth0
10.0.1.1                 ether   02:42:28:56:56:e3   C                     eth1
```

two takeaways here are that we're on the same network as the target Alice who is at
`10.0.0.2` and that the address for the access point is `10.0.0.1`. Our goal is to
tell the acces point that we're the client IP has our MAC address:

```
root@mallory:/shared# 
```



We left off at trying to get Mallory to redirect properly

https://linuxhint.com/arp_spoofing_using_man_in_the_middle_attack/
