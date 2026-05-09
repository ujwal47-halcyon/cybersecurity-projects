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
- **Indian password format engine** — `Name@123`, `Rahul#786`, `Shiva@108` and more
- **Number-only pattern engine** — sequential, date fragments, mirror, PIN, culturally significant Indian numbers
- **Mixed pattern engine** — staircase, keyboard walks, interleaved, chunked repeats
- **Multiple transformation layers** — case variants, leet speak, date formats, year sweeps, cross-combinations
- **Deity/god name patterns** — ram, shiva, krishna, ganesh, durga, hanuman and more
- **Configurable min/max password length** — filter output to exactly what you need
- **Live spinner with word count** during generation
- **Auto-saves** to `./wordlists/<name>_<timestamp>.txt` — deduped, no fluff

---

## Demo

```
wordgen> -g

─────────── TARGET IDENTITY ───────────
  [?] * First name(s): Rahul
  [?] ? Last name(s) / Surname(s): Sharma
  [?] ? Nickname(s): rocky

─────────── PASSWORD LENGTH FILTER ───────────
  [?] ? Minimum password length (default 6): 8
  [?] ? Maximum password length (default 32): 16

  [*] Starting generation engine...
  ⣾ Generating... 41,329 words

  [✔] Done!
  [✔] Words generated : 41,329
  [✔] File size       : 392.1 KB
  [✔] Saved to        : wordlists/rahul_20260509_143012.txt
```

---

## Installation

No external dependencies. Uses Python standard library only.

```bash
# Clone the repo
git clone https://github.com/ujwal47-halcyon/cybersecurity-projects.git
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
| Phone number(s) | Last 3–4 digits used in pattern generation |
| Other important numbers | Lucky numbers, jersey numbers, years |
| Pet name | Common base for personal passwords |
| Other names | Partner, city, sports team, idol |
| Keywords | Hobbies, favourite things |
| Min / Max length | Filter output to a specific password length range |
| Special characters | Defaults: `! @ # $ % _ -` — customizable |

---

## How It Works

WordGen runs every input token through multiple transformation layers, then applies three dedicated pattern engines on top.

### Core Transforms

```
john        →  john, John, JOHN                       # case variants
john        →  j0hn, J0HN, j@hn                      # leet substitutions
15/01/1999  →  15011999, 1999, 0115, 15/01/99 ...    # date formats
john        →  john2019, john2020 ... john2026        # year sweep
john+sharma →  johnsharma, sharmajohn                # cross-combinations
```

### Indian Password Format Engine

Generated explicitly for every name variant:

```
Rahul@123       Rahul#786       rahul$108
@123Rahul       sharma_007      ROCKY@1234
Rahul9876       Rahul1501       luhar@99
Shiva@108       ram123!         Krishna#786
```

Deity names: `ram, shiv, shiva, krishna, ganesh, durga, hanuman, vishnu, lakshmi, saraswati, kali, devi, mata, bharat, india, jai`

### Number-Only Pattern Engine

| Category | Examples |
|---|---|
| All same digit | `1111`, `000000`, `99999999` |
| Sequential asc/desc | `1234`, `23456`, `9876`, `876543` |
| Birth years | `1970`–`2010`, short form `85`, `99`, `01` |
| Date fragments | `1501`, `0115`, `150199`, `011599` |
| Repeating blocks | `1212`, `3434`, `121212` |
| Mirror | `123321`, `12344321`, `9889` |
| Phone-style | `9876543210`, `9000000000` |
| Indian culturally significant | `786`, `108`, `1947`, `420`, `143`, `2611` |
| 4-digit high frequency | `6969`, `1379`, `2580`, `1470`, `4321` |
| 6-digit high frequency | `123456`, `112233`, `159753`, `112358` |
| 8-digit high frequency | `12345678`, `11223344`, `12344321` |

### Mixed Pattern Engine

| Category | Examples |
|---|---|
| Staircase repeating | `1223334444`, `122333` |
| Keyboard row walks | `qwerty`, `asdfgh`, `1q2w3e4r` |
| Interleaved repeats | `112233`, `aabbcc`, `11223344` |
| Mirror | `abccba`, `12344321` |
| Chunked repeats | `123123`, `abcabc`, `qweqwe` |
| Mixed num+alpha | `a1b2c3`, `1a2b3c`, `A1B2C3` |
| PIN blocks | `1379`, `2580`, `6969`, `1010` |

---

## Output

Wordlists are saved to a `wordlists/` folder created automatically in the same directory:

```
wordlists/
└── rahul_20260509_143012.txt
```

Plain text, one password per line, duplicates removed, filtered to your length range. Ready to pipe into any tool.

```bash
# Hydra
hydra -l admin -P wordlists/rahul_20260509_143012.txt ssh://192.168.1.1

# Hashcat
hashcat -m 0 hashes.txt wordlists/rahul_20260509_143012.txt
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
