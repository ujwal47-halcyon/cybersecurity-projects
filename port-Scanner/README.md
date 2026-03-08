# Port Scanner

- A TCP port scanner built in Python using raw sockets — my first cybersecurity project.

## What it does
- Takes a target IP or hostname and a port range as input
- Attempts a TCP connection on each port
- Reports which ports are open

## How to run
```bash
python port_scanner.py
```

## Example output
```
Target   : scanme.nmap.org
Ports    : 1 - 1024
[OPEN]  Port 22
[OPEN]  Port 80
Scan complete. 2 open port(s) found.
```

## Concepts learned
- How TCP connections work
- Network reconnaissance basics
- Python socket library
- How tools like Nmap work under the hood

## Legal disclaimer
- Only scan hosts you own or have explicit permission to scan.
scanme.nmap.org is a legal practice target provided by the Nmap project.