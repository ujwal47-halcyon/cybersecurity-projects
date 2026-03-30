# Port Scanner

A multithreaded network port scanner written in Python. Built as part of
my penetration testing learning journey — started as a basic TCP scanner
and upgraded with threading, banner grabbing and report output.

---

## What it does

Points at a target IP, spins up 100 threads and scans ports concurrently.
For each open port it tries to grab the service banner to identify what
version is running. Results can be saved to a report file.

Without threading, scanning 1024 ports took ~17 minutes.
After adding threading it takes ~6 seconds. Thats the difference.

---

## Features

- Multithreaded scanning (default 100 threads, adjustable)
- Detects common services by port number (SSH, HTTP, SMB, MySQL, RDP etc)
- Banner grabbing to fingerprint service versions
- Clean scan output with timestamps
- Optional .txt report output

---

## Usage
```bash
py port-Scanner.py <target-ip> [options]
```

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `-s` | Start port | 1 |
| `-e` | End port | 1024 |
| `-t` | Number of threads | 100 |
| `-r` | Save report to file | Off |

**Examples:**
```bash
# Basic scan
py port-Scanner.py 127.0.0.1

# Custom port range
py port-Scanner.py 192.168.1.1 -s 1 -e 65535

# Save report
py port-Scanner.py 127.0.0.1 -s 1 -e 1024 -r
```

---

## Sample Output
```
==================================================
  Target   : 127.0.0.1
  Ports    : 1 - 1024
  Threads  : 100
  Started  : 2026-03-30 10:44:17
==================================================

  [OPEN] Port 135 (Unknown)
  [OPEN] Port 445 (SMB)

==================================================
  Scan complete. 2 open ports found.
  Finished : 2026-03-30 10:44:23
==================================================
```

---

## What the results mean

- **Port 135** — Windows RPC. Present on every Windows machine by default.
- **Port 445** — SMB (Server Message Block). Windows file sharing protocol.
  Notable because this is the port exploited by EternalBlue/WannaCry.
  Seeing it open is a reminder that open ports are attack surface.

---

## Disclaimer

For educational purposes and authorized testing only. Never scan systems
you dont own or have explicit permission to test.
