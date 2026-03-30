# Log Analyser

A Python tool that parses web server access logs (Apache/Nginx format)
and flags suspicious activity automatically.

Built because real SOC analysts spend a lot of time doing exactly this —
manually digging through logs looking for patterns that indicate an attack.
This automates the boring part.

---

## What it detects

| Threat | How | Threshold |
|--------|-----|-----------|
| Brute Force | Too many 401s from same IP | 10+ attempts |
| Directory Scanning | Too many 404s from same IP | 15+ errors |
| High Request Volume | Unusual number of requests from one IP | 20+ requests |

---

## Usage
```bash
py log_analyser.py <logfile> [-r]
```

**Examples:**
```bash
# Analyse a log file
py log_analyser.py access.log

# Analyse and save report
py log_analyser.py access.log -r
```

---

## Sample Output
```
=======================================================
  Log Analysis Report
  File     : sample.log
  Time     : 2026-03-30 11:32:55
=======================================================

  Total Requests : 29
  Unique IPs     : 4

  --- Status Code Breakdown ---
  200 : 4 requests
  401 : 11 requests
  404 : 14 requests

  --- Top 5 Most Active IPs ---
  192.168.1.2 : 14 requests
  192.168.1.3 : 11 requests

  --- Suspicious Activity Detected ---

  [!] Possible Brute Force
      IP     : 192.168.1.3
      Detail : 11 failed auth attempts (401s)
=======================================================
```

---

## What the detections mean

**Brute Force (401s)** — An IP repeatedly hitting a login endpoint and
failing authentication. Classic credential stuffing or password spraying.
In a real environment this IP would get blocked at the firewall.

**Directory Scanning (404s)** — An IP requesting many paths that dont
exist. This is exactly what tools like Gobuster do — trying common
directory names hoping something responds. Seeing this in logs means
someone is actively mapping the application.

**High Request Volume** — Could be a scanner, a bot, or a DoS attempt.
Worth investigating regardless.

---

## Disclaimer

For educational purposes and authorized testing only.
