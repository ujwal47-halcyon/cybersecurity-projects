# Cybersecurity Projects

Personal collection of security tools built from scratch while learning.
penetration testing. Everything here is written in Python.

---

## Projects

### 1. Port Scanner
A multithreaded network scanner that identifies open ports, detects
services, grabs banners and saves scan reports.

**Features:**
- Multithreaded scanning (100 threads by default — scans 1024 ports in ~6 seconds)
- Service detection for common ports (SSH, HTTP, SMB, MySQL etc)
- Banner grabbing to identify service versions
- Optional report output to .txt file


---

### 2. Hash Cracker
A dictionary-based hash cracking tool that attempts to crack hashed
passwords using a wordlist.

---

### 3. Log Analyser
A web server log parser that automatically detects suspicious activity —
brute force attempts, directory scanning, and abnormal request volumes.

**Features:**
- Detects brute force attacks (repeated 401s from same IP)
- Detects directory scanning (repeated 404s from same IP)
- Flags high request volume from single IPs
- Status code breakdown and top path analysis
- Optional report output to .txt file

---

## Disclaimer
These tools are built for educational purposes and authorized testing only.
Never run them against systems you dont own or have explicit permission to test.

---

## Author
Ujwal Vishwanath — Cybersecurity student, REVA University
[GitHub](https://github.com/ujwal47-halcyon)
