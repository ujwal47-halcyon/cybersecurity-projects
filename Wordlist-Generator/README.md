# WordGen — Targeted Wordlist Generator

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94?style=flat-square&logo=linux)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Use Case](https://img.shields.io/badge/Use%20Case-Penetration%20Testing-red?style=flat-square)

A fast, interactive, terminal-based wordlist generator built for penetration testers. WordGen takes personal information about a target and generates a highly targeted wordlist using real-world password patterns — including patterns commonly used in India.

> **For authorized penetration testing and CTF use only. Do not use against systems you do not have explicit permission to test.**

---

## Features

- **Interactive terminal UI** with tab completion and color output
- **Short command aliases** — `-g` to generate, `-h` for help, `Ctrl+C` to exit
- **Indian password format engine** — generates patterns like `Name@123`, `Rahul#786`, `Shiva@108`
- **Multiple transformation layers** — case variants, leet speak, date formats, year sweeps, cross-combinations
- **Deity/god name patterns** — ram, shiva, krishna, ganesh, durga, hanuman and more
- **Configurable min/max password length** — filter output to exactly what you need
- **Spinner with live word count** during generation
- **Auto-saves** to `./wordlists/<name>_<timestamp>.txt` — no duplicates, no fluff

---

## Demo

```
wordgen> -g

─────────── TARGET IDENTITY ───────────
  [?] * First name(s): Rahul
  [?] ? Last name(s) / Surname(s): Sharma
  [?] ? Nickname(s): rocky
  ...

─────────── PASSWORD LENGTH FILTER ───────────
  [?] ? Minimum password length (default 6): 8
  [?] ? Maximum password length (default 32): 16

  [*] Starting generation engine...
  ⣾ Generating... 14,231 words

  [✔] Done!
  [✔] Words generated : 14,231
  [✔] File size       : 168.4 KB
  [✔] Saved to        : wordlists/rahul_20260422_143012.txt
```

---

## Installation

No external dependencies. Uses Python standard library only.

```bash
# Clone the repo
git clone https://github.com/<your-username>/cybersecurity-projects.git
cd cybersecurity-projects/wordgen

# Make executable
chmod +x wordgen.py

# Run
python3 wordgen.py
```

---

## Usage

```
wordgen> -g        # Full interactive generation
wordgen> -q        # Quick generation (fewer prompts)
wordgen> -h        # Help menu
wordgen> -c        # Show current session config
wordgen> clear     # Clear screen
Ctrl+C             # Exit anytime
```

### Fields collected during generation

| Field | Description |
|---|---|
| First name | Target's first name(s) |
| Last name / Surname | Family name(s) |
| Nickname | Online handles or informal names |
| Artist / Stage name | For public figures or influencers |
| Date of birth | Accepts DD/MM/YYYY or DDMMYYYY |
| Phone number(s) | Last 3-4 digits used in pattern generation |
| Other important numbers | Lucky numbers, jersey numbers, years |
| Pet name | Common base for personal passwords |
| Other names | Partner, city, sports team, idol |
| Keywords | Hobbies, favourite things |
| Min / Max length | Filter output to a specific password length range |
| Special characters | Defaults: `! @ # $ % _ -` — customizable |

---

## How It Works

WordGen runs every input token through five transformation layers, then applies Indian-specific format patterns on top.

### Core Transforms

```
john  →  john, John, JOHN                    # case variants
john  →  j0hn, j0H N, J0HN, j@hn            # leet substitutions
15/01/1999  →  15011999, 1999, 0115, 15/01/99, 99 ...  # date formats
john  →  john2019, john2020 ... john2026     # year sweep
john + sharma  →  johnsharma, sharmajohn    # cross-combinations
```

### Indian Password Format Engine

These patterns are generated explicitly for every name variant:

```
Rahul@123       Rahul#786       rahul$108
@123Rahul       sharma_007      ROCKY@1234
luhar@99        Rahul9876       Rahul1501
Shiva@108       ram123!         Krishna#786
```

Deity names included: `ram, shiv, shiva, krishna, ganesh, durga, hanuman, vishnu, lakshmi, saraswati, kali, devi, mata, bharat, india, jai`

### Number patterns used

`123, 1234, 12345, 007, 786, 108, 101, 111, 999, 000, 420, 69, 21` + phone last 3-4 digits + user-supplied numbers

---

## Output

Wordlists are saved to a `wordlists/` folder created automatically in the same directory:

```
wordlists/
└── rahul_20260422_143012.txt
```

Each file is plain text, one password per line, with duplicates removed and entries filtered to your specified length range. Ready to pipe directly into Hydra, Hashcat, or any other tool.

```bash
# Example usage with Hydra
hydra -l admin -P wordlists/rahul_20260422_143012.txt ssh://192.168.1.1

# Example usage with Hashcat
hashcat -m 0 hashes.txt wordlists/rahul_20260422_143012.txt
```

---

## Project Structure

```
wordgen/
├── wordgen.py        # Main script
├── README.md         # This file
└── wordlists/        # Auto-created on first run
```

---

## Disclaimer

This tool is built for **authorized penetration testing, CTF challenges, and security research only**. Using this tool against systems or accounts without explicit written permission is illegal and unethical. The developer is not responsible for any misuse.

---

## Author

**Ujwal** — BCA (Cyber Security & Digital Forensics), REVA University  
GitHub: [ujwal47-halcyon](https://github.com/ujwal47-halcyon)
