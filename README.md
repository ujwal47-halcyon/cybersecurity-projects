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
- Optional report output to .txt file.


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

---

## WordGen — Targeted Wordlist Generator

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=flat-square&logo=linux)

A fast, interactive, terminal-based wordlist generator for penetration testers. Takes personal info about a target and generates a highly targeted wordlist using real-world password patterns — including patterns commonly used in India.

> For authorized penetration testing and CTF use only.

### Features

- Interactive terminal UI with tab completion and color output
- Short command aliases — `-g` to generate, `-h` for help, `Ctrl+C` to exit
- **Indian password format engine** — `Name@123`, `Rahul#786`, `Shiva@108` and more
- Case variants, leet speak, date formats, year sweeps, cross-combinations
- Deity/god name patterns — ram, shiva, krishna, ganesh, durga, hanuman...
- Configurable min/max password length filter
- Live spinner with word count during generation
- Auto-saves to `./wordlists/<name>_<timestamp>.txt` — deduped, clean output

### Usage

```bash
python3 wordgen.py
```

```
wordgen> -g        # Full interactive generation
wordgen> -q        # Quick generation
wordgen> -h        # Help
wordgen> -c        # Show session config
Ctrl+C             # Exit anytime
```

### Output

```
wordlists/
└── rahul_20260422_143012.txt    # plain text, one password per line
```

Ready to pipe into Hydra, Hashcat, or any other tool.

```bash
hydra -l admin -P wordlists/rahul_20260422_143012.txt ssh://192.168.1.1
hashcat -m 0 hashes.txt wordlists/rahul_20260422_143012.txt
```

**[→ View Tool](https://github.com/ujwal47-halcyon/cybersecurity-projects/tree/main/Wordlist-Generator)**

---

## Disclaimer
These tools are built for educational purposes and authorized testing only.
Never run them against systems you dont own or have explicit permission to test.

---

## Author
Ujwal Vishwanath — Cybersecurity student, REVA University
[GitHub](https://github.com/ujwal47-halcyon)
