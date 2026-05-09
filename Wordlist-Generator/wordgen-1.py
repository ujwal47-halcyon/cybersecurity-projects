#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║           W O R D G E N  -  Wordlist Generator           ║
║         For authorized penetration testing only          ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import sys
import readline
import itertools
import string
import time
import threading
from datetime import datetime
from pathlib import Path

# ─────────────────────────── ANSI COLORS ───────────────────────────
class C:
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"

# ─────────────────────────── BANNER ────────────────────────────────
BANNER = f"""
{C.CYAN}{C.BOLD}
██╗    ██╗ ██████╗ ██████╗ ██████╗  ██████╗ ███████╗███╗   ██╗
██║    ██║██╔═══██╗██╔══██╗██╔══██╗██╔════╝ ██╔════╝████╗  ██║
██║ █╗ ██║██║   ██║██████╔╝██║  ██║██║  ███╗█████╗  ██╔██╗ ██║
██║███╗██║██║   ██║██╔══██╗██║  ██║██║   ██║██╔══╝  ██║╚██╗██║
╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝╚██████╔╝███████╗██║ ╚████║
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═══╝
{C.RESET}
{C.YELLOW}          Targeted Wordlist Generator  v2.0{C.RESET}
{C.DIM}     For authorized penetration testing use only{C.RESET}
{C.CYAN}          Type {C.WHITE}-h{C.CYAN} for help  |  {C.WHITE}-g{C.CYAN} to generate{C.RESET}
"""

HELP_TEXT = f"""
{C.CYAN}{C.BOLD}═══════════════════  WORDGEN HELP  ═══════════════════{C.RESET}

{C.YELLOW}COMMANDS:{C.RESET}
  {C.GREEN}-g{C.RESET}  {C.DIM}/ generate{C.RESET}    Full interactive wordlist generation
  {C.GREEN}-q{C.RESET}  {C.DIM}/ quick{C.RESET}       Quick generate (minimal prompts)
  {C.GREEN}-c{C.RESET}  {C.DIM}/ config{C.RESET}      Show current session config
  {C.GREEN}-h{C.RESET}  {C.DIM}/ help{C.RESET}        Show this help menu
  {C.GREEN}clear{C.RESET}              Clear the screen
  {C.GREEN}Ctrl+C{C.RESET}             Exit WordGen (anytime)

{C.YELLOW}HOW IT WORKS:{C.RESET}
  WordGen asks questions about the target, then generates
  combinations using multiple techniques:

  {C.CYAN}Core Transforms:{C.RESET}
  {C.DIM}• Case variations     john → John, JOHN, jOhN{C.RESET}
  {C.DIM}• Leet substitutions  e→3, a→@, i→1, o→0, s→${C.RESET}
  {C.DIM}• Date formats        19990115, 1999, 0115, 15/01/99{C.RESET}
  {C.DIM}• Year sweep          john2019 … john2026{C.RESET}
  {C.DIM}• Cross-combinations  firstName+DOB, nick+phone{C.RESET}

  {C.CYAN}Indian Password Formats:{C.RESET}
  {C.DIM}• Name + special + number   Ujwal@123, Rahul#007{C.RESET}
  {C.DIM}• Name + DOB combo          Ujwal1501, rahul1999{C.RESET}
  {C.DIM}• Name + phone tail         ujwal9876, Rahul4321{C.RESET}
  {C.DIM}• Reversed name + numbers   lawju123, lehar@99{C.RESET}
  {C.DIM}• God/deity + numbers       Shiva@108, ram123!{C.RESET}
  {C.DIM}• Name + lucky no. + spec   Arjun7#, Lucky@47{C.RESET}

{C.YELLOW}OUTPUT:{C.RESET}
  Saved as {C.WHITE}./wordlists/<n>_<timestamp>.txt{C.RESET}
  Duplicates removed. Filtered by your min/max length.

{C.YELLOW}TAB COMPLETION:{C.RESET}
  Press {C.WHITE}Tab{C.RESET} to autocomplete any command.

{C.CYAN}═══════════════════════════════════════════════════════{C.RESET}
"""

# ─────────────────────────── TAB COMPLETION ────────────────────────
COMMANDS = ["-g", "-q", "-h", "-c", "generate", "quick", "config", "clear", "help"]

def completer(text, state):
    options = [cmd for cmd in COMMANDS if cmd.startswith(text)]
    return options[state] if state < len(options) else None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")
readline.set_completer_delims(" \t\n")

# ─────────────────────────── SPINNER ───────────────────────────────
class Spinner:
    def __init__(self, msg="Generating"):
        self.msg = msg
        self.running = False
        self.thread = None
        self.count = 0

    def _spin(self):
        frames = ["⣾","⣽","⣻","⢿","⡿","⣟","⣯","⣷"]
        i = 0
        while self.running:
            sys.stdout.write(f"\r{C.CYAN}{frames[i % len(frames)]}{C.RESET} {self.msg}... {C.YELLOW}{self.count:,}{C.RESET} words")
            sys.stdout.flush()
            time.sleep(0.08)
            i += 1

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write("\r" + " " * 60 + "\r")
        sys.stdout.flush()

# ─────────────────────────── INPUT HELPERS ─────────────────────────
def ask(prompt, required=False, default=""):
    prefix = f"{C.CYAN}[?]{C.RESET}"
    req_flag = f"{C.RED}*{C.RESET}" if required else f"{C.DIM}?{C.RESET}"
    while True:
        val = input(f"  {prefix} {req_flag} {prompt}: ").strip()
        if val:
            return val
        if not required:
            return default
        print(f"  {C.RED}[!]{C.RESET} This field is required.")

def ask_multi(prompt):
    """Ask for comma-separated or space-separated values, return list."""
    val = input(f"  {C.CYAN}[?]{C.RESET} {C.DIM}?{C.RESET} {prompt}\n  {C.DIM}(separate multiple with commas){C.RESET}: ").strip()
    if not val:
        return []
    return [v.strip() for v in val.replace(",", " ").split() if v.strip()]

def section(title):
    w = 54
    pad = (w - len(title) - 2) // 2
    print(f"\n{C.BLUE}{'─'*pad} {C.WHITE}{C.BOLD}{title}{C.RESET}{C.BLUE} {'─'*(w-pad-len(title)-2)}{C.RESET}")

# ─────────────────────────── LEET SPEAK ────────────────────────────
LEET_MAP = {
    'a': ['a', '@', '4'],
    'e': ['e', '3'],
    'i': ['i', '1', '!'],
    'o': ['o', '0'],
    's': ['s', '$', '5'],
    't': ['t', '7'],
    'b': ['b', '8'],
    'g': ['g', '9'],
    'l': ['l', '1'],
}

def leet_variants(word):
    """Generate leet speak variants (limited to avoid explosion)."""
    if not word:
        return set()
    word = word.lower()
    variants = {word}
    # Single substitutions
    for i, ch in enumerate(word):
        if ch in LEET_MAP:
            for rep in LEET_MAP[ch][1:]:  # skip original
                variants.add(word[:i] + rep + word[i+1:])
    # Full leet
    full = ""
    for ch in word:
        full += LEET_MAP.get(ch, [ch])[1] if ch in LEET_MAP and len(LEET_MAP[ch]) > 1 else ch
    if full != word:
        variants.add(full)
    return variants

# ─────────────────────────── CASE VARIANTS ─────────────────────────
def case_variants(word):
    if not word:
        return set()
    variants = {
        word.lower(),
        word.upper(),
        word.capitalize(),
        word.title(),
        word[0].upper() + word[1:].lower() if len(word) > 1 else word.upper(),
    }
    # camelBack if contains space/underscore
    if ' ' in word or '_' in word:
        parts = word.replace('_', ' ').split()
        variants.add(parts[0].lower() + ''.join(p.capitalize() for p in parts[1:]))
    return {v for v in variants if v}

# ─────────────────────────── DATE FORMATS ──────────────────────────
def date_variants(dob):
    """Generate many date format variants from DOB string."""
    variants = set()
    if not dob:
        return variants
    dob_clean = dob.replace("/", "").replace("-", "").replace(".", "").strip()
    variants.add(dob_clean)
    # Try to parse structured date (various formats)
    for fmt in ("%d%m%Y", "%m%d%Y", "%Y%m%d", "%d%m%y", "%m%d%y"):
        try:
            dt = datetime.strptime(dob_clean, fmt)
            variants.update([
                dt.strftime("%d%m%Y"),
                dt.strftime("%m%d%Y"),
                dt.strftime("%Y%m%d"),
                dt.strftime("%d%m%y"),
                dt.strftime("%m%d%y"),
                dt.strftime("%d%m"),
                dt.strftime("%m%d"),
                dt.strftime("%Y"),
                dt.strftime("%y"),
                dt.strftime("%d"),
                dt.strftime("%m"),
                dt.strftime("%d/%m/%Y"),
                dt.strftime("%d-%m-%Y"),
                dt.strftime("%d.%m.%Y"),
            ])
            break
        except ValueError:
            continue
    # Keep raw input variants
    variants.add(dob.replace("/", "").replace("-", "").replace(".", ""))
    variants.add(dob)
    return {v for v in variants if v}

# ─────────────────────────── PATTERN GENERATOR ─────────────────────
def generate_number_patterns():
    """
    Generate standalone number-only patterns commonly used in passwords.
    Covers: all-same, sequential, birth years, dates, repeating blocks,
    phone-style, lucky numbers, culturally common Indian numbers.
    """
    nums = set()

    # ── All same digit: 111111, 222222, 000000 ────────────────────
    for d in "0123456789":
        for length in range(4, 9):
            nums.add(d * length)

    # ── Sequential ascending/descending ───────────────────────────
    for start in range(0, 10):
        for length in range(4, 10):
            asc  = "".join(str((start + i) % 10) for i in range(length))
            desc = "".join(str((start - i) % 10) for i in range(length))
            nums.add(asc)
            nums.add(desc)

    # ── Birth years: 1970–2010 ─────────────────────────────────────
    for y in range(1970, 2011):
        nums.add(str(y))
        nums.add(str(y)[2:])          # 99, 00, 01 ...

    # ── Common date fragments ──────────────────────────────────────
    # DDMM, MMDD, DDMMYY, MMDDYY
    for d in range(1, 32):
        for m in range(1, 13):
            dd = f"{d:02d}"
            mm = f"{m:02d}"
            nums.update([dd+mm, mm+dd])
    for y in range(70, 100):         # 70–99
        for d in range(1, 32):
            for m in range(1, 13):
                nums.add(f"{d:02d}{m:02d}{y:02d}")
                nums.add(f"{m:02d}{d:02d}{y:02d}")

    # ── Repeating blocks: 12121212, 34343434, 123123 ──────────────
    for block in ["12","23","34","45","56","67","78","89","90","01",
                  "13","24","36","99","11","00","69","47","21"]:
        for rep in range(2, 5):
            nums.add(block * rep)

    # ── Mirror numbers: 12344321, 56788765 ────────────────────────
    for base in ["12", "123", "1234", "12345", "56", "567", "98", "987"]:
        nums.add(base + base[::-1])
        nums.add(base[::-1] + base)

    # ── Phone-style patterns (10-digit structures) ─────────────────
    phone_bases = [
        "9999999999", "8888888888", "7777777777",
        "9876543210", "0123456789", "9000000000",
        "8000000000", "7000000000", "9876000000",
    ]
    nums.update(phone_bases)
    # Last 4/6/8 of common phone structures
    for tail in ["0000","1111","2222","3333","4321","1234","9999","0001","0007"]:
        for prefix in ["98","99","90","88","87","77","70"]:
            nums.add(prefix + tail)

    # ── Culturally significant Indian numbers ─────────────────────
    INDIAN_NUMBERS = [
        "786",          # Islamic lucky number
        "108",          # Hindu sacred number
        "1008",         # Extended sacred
        "007",          # Popular worldwide
        "420",          # Slang — IPC section
        "100",          # Police
        "101",          # Common pattern
        "143",          # I love you (pager code)
        "1947",         # Indian independence
        "1857",         # First war of independence
        "2611",         # 26/11
        "1526",         # Battle of Panipat
        "2024", "2025", "2026",
        "1234567890",
        "0987654321",
        "1122334455",
        "9876543210",
        "1111111111",
        "0000000000",
    ]
    nums.update(INDIAN_NUMBERS)

    # ── OTP / PIN style (4–6 digit all combos of common digits) ───
    common_digits = ["0","1","2","3","4","5","6","7","8","9"]
    # All 4-digit patterns with high frequency in real leaks
    high_freq_4 = [
        "0000","1111","2222","3333","4444","5555","6666","7777","8888","9999",
        "1234","4321","1212","2121","1122","2211","1221","2112","6969","6996",
        "1010","0101","2020","2002","1001","3003","4004","5005",
        "1379","1397","3197","7913",        # diagonal keypad
        "2468","8642","1357","7531",        # alternating
        "1470","2580","3690",              # keypad columns
        "0852","0258","1593","3571",
        "0000","9999","1000","2000","5000",
        "0007","0070","0700","7000",
        "4200","0420","6900","0069",
    ]
    nums.update(high_freq_4)

    # ── 6-digit common ─────────────────────────────────────────────
    high_freq_6 = [
        "123456","654321","111111","000000","123123",
        "112233","123321","121212","123654","000001",
        "159753","357159","147258","258369","369258",
        "789456","456789","789123","321654","654123",
        "100000","200000","500000","999999","888888",
        "696969","123789","987123","112358",  # Fibonacci start
    ]
    nums.update(high_freq_6)

    # ── 8-digit common ─────────────────────────────────────────────
    high_freq_8 = [
        "12345678","87654321","11111111","00000000",
        "12341234","12344321","11223344","99999999",
        "10101010","01010101","12121212","98989898",
        "13579753","24682468","11001100","10001000",
    ]
    nums.update(high_freq_8)

    return nums


def generate_fixed_patterns():
    """
    Generate number/alphabet patterns people actually use in passwords.
    Covers: repeat-stair, sequential, mirror, keyboard walks, alpha equivalents.
    """
    patterns = set()

    # ── Staircase repeating: 1223334444, 1222333444455555 ──────────
    # Each digit repeated n times: 1x1, 2x2, 3x3 ...
    for length in range(4, 9):          # staircase depth
        p = ""
        for n in range(1, length + 1):
            p += str(n % 10) * n
        patterns.add(p)
    # Variants: starting digit varies
    for start in range(0, 5):
        p = ""
        for n in range(1, 6):
            p += str((start + n - 1) % 10) * n
        patterns.add(p)

    # ── Uniform repeats: 1111, 2222, aaaa, 11111111 ───────────────
    for ch in "0123456789abcdefghijklmnopqrstuvwxyz":
        for rep in range(4, 9):
            patterns.add(ch * rep)

    # ── Sequential ascending: 1234, 12345, 123456, 1234567, 12345678
    for start in range(0, 8):
        for length in range(4, 9):
            p = "".join(str((start + i) % 10) for i in range(length))
            patterns.add(p)
    # Descending: 9876, 987654, 9876543210
    for start in range(9, 1, -1):
        for length in range(4, 9):
            p = "".join(str((start - i) % 10) for i in range(length))
            patterns.add(p)

    # ── Alphabet sequential: abcd, efgh, abcdef, xyzabc ──────────
    alpha = "abcdefghijklmnopqrstuvwxyz"
    for start in range(0, 23):
        for length in range(4, 8):
            p = "".join(alpha[(start + i) % 26] for i in range(length))
            patterns.add(p)
            patterns.add(p.upper())

    # ── Mirror/palindrome: 12344321, abccba, 123321 ───────────────
    for base in ["123", "1234", "12345", "abc", "abcd", "abcde",
                 "321", "987", "xyz"]:
        patterns.add(base + base[::-1])       # 123321
        patterns.add(base[::-1] + base)       # 321123

    # ── Interleaved repeats: 112233, 11223344, aabbcc ─────────────
    for length in range(2, 6):
        # Numbers: 112233445566
        p_num = "".join(str(i % 10) * 2 for i in range(1, length + 3))
        patterns.add(p_num)
        # Alpha: aabbccdd
        p_alp = "".join(alpha[i % 26] * 2 for i in range(length + 2))
        patterns.add(p_alp)
        patterns.add(p_alp.upper())

    # ── Keyboard row walks ─────────────────────────────────────────
    kb_rows = [
        "qwertyuiop", "asdfghjkl", "zxcvbnm",
        "qwerty", "asdfgh", "zxcvbn",
        "1qaz2wsx", "1q2w3e4r", "1q2w3e",
        "qazwsx", "qazwsxedc",
        "poiuytrewq", "lkjhgfdsa",           # reversed rows
    ]
    for row in kb_rows:
        for length in range(4, len(row) + 1):
            patterns.add(row[:length])
            patterns.add(row[:length].upper())
            patterns.add(row[:length].capitalize())

    # ── Mixed number+alpha staircase: a1b2c3, 1a2b3c ─────────────
    for length in range(3, 7):
        p1 = "".join(alpha[i % 26] + str((i + 1) % 10) for i in range(length))
        p2 = "".join(str((i + 1) % 10) + alpha[i % 26] for i in range(length))
        patterns.add(p1)
        patterns.add(p2)
        patterns.add(p1.upper())

    # ── Common PIN-style blocks people append to names ────────────
    PIN_BLOCKS = [
        "0000", "1111", "2222", "3333", "4444", "5555",
        "6666", "7777", "8888", "9999",
        "1234", "4321", "0123", "1010", "2020",
        "6969", "1122", "2211", "1221", "2112",
        "1001", "2002", "3003",
        "1379", "2580", "1357",  # diagonal keypad patterns
        "1470", "2580", "3690",  # vertical keypad columns
    ]
    patterns.update(PIN_BLOCKS)

    # ── Chunked repeats: 123123, 456456, abcabc ───────────────────
    for chunk in ["123", "456", "789", "012", "321", "abc",
                  "xyz", "qwe", "asd", "zxc"]:
        patterns.add(chunk * 2)
        patterns.add(chunk * 3)
        patterns.add(chunk.upper() * 2)

    return patterns


# ─────────────────────────── CORE GENERATOR ────────────────────────
COMMON_SUFFIXES = [
    "123", "1234", "12345", "123456",
    "007", "101", "111", "000", "999",
    "1", "2", "3", "69", "21",
    "!", "!!", "@", "#", "!@#",
    "$", "$$", "!1", "@1", "1!"
]

COMMON_PREFIXES = [
    "!", "@", "#", "1", "123", "0"
]

SPECIAL_COMBOS = [
    "!", "@", "#", "$", "%", "^", "&", "*",
    "!@", "@#", "#$", "!@#", "@#$",
    "123!", "!123", "1!", "@2", "#3"
]

def expand_words(raw_words):
    """Generate all variants from a list of base words."""
    expanded = set()
    for w in raw_words:
        if not w:
            continue
        expanded.update(case_variants(w))
        expanded.update(leet_variants(w))
        for cv in list(case_variants(w)):
            expanded.update(leet_variants(cv))
    return {w for w in expanded if w}

def combine_with_affixes(words, extra_numbers, special_chars, spinner):
    """Attach numbers/specials to all word variants."""
    result = set(words)
    built_suffixes = list(COMMON_SUFFIXES)
    built_prefixes = list(COMMON_PREFIXES)

    for n in extra_numbers:
        built_suffixes.extend([n, n[::-1], n + "!", "!" + n])
        built_prefixes.append(n)

    for sp in special_chars:
        built_suffixes.extend([sp, sp * 2])
        built_prefixes.append(sp)

    built_suffixes.extend(SPECIAL_COMBOS)

    for word in list(words):
        spinner.count = len(result)
        for suf in built_suffixes:
            result.add(word + suf)
        for pre in built_prefixes:
            result.add(pre + word)
        for sp in special_chars:
            result.add(word + sp)
            result.add(sp + word)

    return result

def cross_combine(word_groups, spinner, limit=3):
    """Cross-combine words from different groups (name+dob, name+nick, etc.)."""
    result = set()
    flat_groups = [list(g) for g in word_groups if g]

    # Pairs
    for i, g1 in enumerate(flat_groups):
        for j, g2 in enumerate(flat_groups):
            if i >= j:
                continue
            for a in g1[:80]:  # cap to avoid explosion
                for b in g2[:80]:
                    result.add(a + b)
                    result.add(b + a)
                    result.add(a + "_" + b)
                    result.add(a + "." + b)
                    spinner.count += 1

    return result

# ─────────────────────────── QUESTION FLOW ─────────────────────────
def run_questionnaire(quick=False):
    data = {}

    section("TARGET IDENTITY")
    data['first_name']  = ask_multi("First name(s)")
    data['last_name']   = ask_multi("Last name(s) / Surname(s)")
    data['nickname']    = ask_multi("Nickname(s)")
    data['artist_name'] = ask_multi("Artist / stage name(s)")

    section("DATES & NUMBERS")
    dob_raw = input(f"  {C.CYAN}[?]{C.RESET} {C.DIM}?{C.RESET} Date of birth (DD/MM/YYYY or DDMMYYYY): ").strip()
    data['dob'] = dob_raw
    data['phone'] = ask_multi("Phone number(s)")
    data['extra_numbers'] = ask_multi("Other important numbers (lucky no., jersey, year, etc.)")

    section("NAMES & RELATIONS")
    data['pet_name']    = ask_multi("Pet name(s)")
    data['other_names'] = ask_multi("Other important names (partner, idol, city, team, etc.)")

    section("PASSWORD LENGTH FILTER")
    try:
        min_len = int(input(f"  {C.CYAN}[?]{C.RESET} {C.DIM}?{C.RESET} Minimum password length {C.DIM}(default 6){C.RESET}: ").strip() or 6)
        max_len = int(input(f"  {C.CYAN}[?]{C.RESET} {C.DIM}?{C.RESET} Maximum password length {C.DIM}(default 32){C.RESET}: ").strip() or 32)
    except ValueError:
        print(f"  {C.YELLOW}[!]{C.RESET} Invalid input, using defaults (6–32).")
        min_len, max_len = 6, 32
    data['min_len'] = min_len
    data['max_len'] = max_len

    section("SPECIAL CHARACTERS")
    print(f"  {C.DIM}Common special chars in passwords: ! @ # $ % ^ & * _ - ={C.RESET}")
    sp_input = input(f"  {C.CYAN}[?]{C.RESET} {C.DIM}?{C.RESET} Include custom special chars (press Enter for defaults): ").strip()
    data['special_chars'] = list(sp_input) if sp_input else list("!@#$%_-")

    if not quick:
        section("ADVANCED")
        data['keywords'] = ask_multi("Any other keywords (hobbies, favourite things, etc.)")
    else:
        data['keywords'] = []

    return data

# ─────────────────────────── GENERATE ──────────────────────────────
def generate_wordlist(data, quick=False):
    spinner = Spinner("Generating")

    # Collect all raw tokens
    all_names = (
        data.get('first_name', []) +
        data.get('last_name', []) +
        data.get('nickname', []) +
        data.get('artist_name', []) +
        data.get('pet_name', []) +
        data.get('other_names', []) +
        data.get('keywords', [])
    )
    phones    = data.get('phone', [])
    extra_num = data.get('extra_numbers', [])
    sp_chars  = data.get('special_chars', [])
    dob       = data.get('dob', '')

    print(f"\n  {C.CYAN}[*]{C.RESET} Expanding words...")
    spinner.start()

    # Base word sets
    name_words  = expand_words(all_names)
    date_words  = date_variants(dob)
    num_words   = set(phones + extra_num)
    for n in phones + extra_num:
        num_words.update(case_variants(n))

    # Combine with affixes
    combined = set()
    combined.update(name_words)
    combined.update(date_words)
    combined.update(num_words)
    combined = combine_with_affixes(name_words, extra_num + phones, sp_chars, spinner)

    # Cross combinations (names × dates × phones)
    groups = [
        list(expand_words(data.get('first_name', [])))[:60],
        list(expand_words(data.get('last_name', [])))[:60],
        list(date_words)[:40],
        list(num_words)[:40],
    ]
    if not quick:
        groups.extend([
            list(expand_words(data.get('nickname', [])))[:40],
            list(expand_words(data.get('artist_name', [])))[:40],
        ])

    cross = cross_combine(groups, spinner)
    combined.update(cross)

    # Add phones + extra numbers raw
    combined.update(phones)
    combined.update(extra_num)

    # Add common years appended to names
    current_year = datetime.now().year
    years = [str(y) for y in range(current_year - 35, current_year + 1)]
    for w in list(name_words)[:200]:
        for yr in years:
            combined.add(w + yr)
            combined.add(w + yr[-2:])

    # ── Indian password format patterns ────────────────────────────
    # Extremely common in India: Name@123, Name#007, Name_1999, etc.
    IN_SPECIALS  = ["@", "#", "$", "_", "!", ".", "*"]
    IN_NUMBERS   = ["123", "1234", "12345", "007", "786", "108",
                    "101", "111", "999", "000", "420", "69", "21",
                    "1", "2", "3", "7", "9"]
    # Append phone last 4 and last 3 digits
    for ph in phones:
        if len(ph) >= 4:
            IN_NUMBERS.append(ph[-4:])
            IN_NUMBERS.append(ph[-3:])

    base_names = list(expand_words(
        data.get('first_name', []) +
        data.get('last_name', []) +
        data.get('nickname', [])
    ))[:120]

    for nm in base_names:
        rev = nm[::-1]
        for sp in IN_SPECIALS:
            for num in IN_NUMBERS:
                # Name@123  Name#007
                combined.add(nm + sp + num)
                # @123Name  #007Name
                combined.add(sp + num + nm)
                # Name123@  Name007#
                combined.add(nm + num + sp)
                # Reversed: lawju@123
                combined.add(rev + sp + num)
        # Name + DOB fragments directly (Ujwal1501, Ujwal1999)
        for dv in list(date_words)[:10]:
            combined.add(nm + dv)
            combined.add(dv + nm)
        # Name + lucky/extra numbers directly
        for en in extra_num + phones:
            tail = en[-4:] if len(en) >= 4 else en
            combined.add(nm + tail)
            combined.add(nm.capitalize() + tail)

    # ── Number-only patterns ───────────────────────────────────────
    combined.update(generate_number_patterns())

    # ── Number & alphabet patterns ─────────────────────────────────
    pattern_words = generate_fixed_patterns()
    combined.update(pattern_words)
    # Also combine patterns as suffixes on base names
    short_patterns = [p for p in pattern_words if 3 <= len(p) <= 6][:120]
    for nm in base_names[:60]:
        for pat in short_patterns:
            combined.add(nm + pat)
            combined.add(nm.capitalize() + pat)

    # God/deity names common in Indian passwords
    DEITIES = ["ram", "shiv", "shiva", "krishna", "ganesh", "durga",
               "hanuman", "vishnu", "lakshmi", "saraswati", "kali",
               "devi", "mata", "bharat", "india", "jai"]
    for deity in DEITIES:
        for sp in IN_SPECIALS:
            for num in ["108", "786", "007", "123", "1", "21"]:
                combined.add(deity + sp + num)
                combined.add(deity.capitalize() + sp + num)
                combined.add(deity.upper() + num)

    # Filter: user-defined length range
    min_len = data.get('min_len', 6)
    max_len = data.get('max_len', 32)
    final = sorted({w for w in combined if min_len <= len(w) <= max_len})
    spinner.stop()
    return final

# ─────────────────────────── SAVE ──────────────────────────────────
def save_wordlist(words, target_hint="target"):
    folder = Path("wordlists")
    folder.mkdir(exist_ok=True)
    safe_name = "".join(c for c in target_hint if c.isalnum() or c in "_-").lower() or "target"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = folder / f"{safe_name}_{ts}.txt"

    print(f"  {C.CYAN}[*]{C.RESET} Writing to disk...")
    t0 = time.time()
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(words) + "\n")
    elapsed = time.time() - t0

    size_kb = filename.stat().st_size / 1024
    print(f"\n  {C.GREEN}[✔]{C.RESET} {C.BOLD}Done!{C.RESET}")
    print(f"  {C.GREEN}[✔]{C.RESET} Words generated : {C.WHITE}{len(words):,}{C.RESET}")
    print(f"  {C.GREEN}[✔]{C.RESET} File size       : {C.WHITE}{size_kb:.1f} KB{C.RESET}")
    print(f"  {C.GREEN}[✔]{C.RESET} Write time      : {C.WHITE}{elapsed:.3f}s{C.RESET}")
    print(f"  {C.GREEN}[✔]{C.RESET} Saved to        : {C.CYAN}{filename}{C.RESET}\n")
    return filename

# ─────────────────────────── MAIN LOOP ─────────────────────────────
def show_config(data):
    if not data:
        print(f"\n  {C.YELLOW}[!]{C.RESET} No session data yet. Run {C.WHITE}generate{C.RESET} first.\n")
        return
    section("CURRENT SESSION CONFIG")
    for k, v in data.items():
        val = ', '.join(v) if isinstance(v, list) else (v or f"{C.DIM}(empty){C.RESET}")
        print(f"  {C.CYAN}{k:<20}{C.RESET} {val}")
    print()

def main():
    os.system("clear")
    print(BANNER)
    session_data = {}

    while True:
        try:
            cmd = input(f"{C.MAGENTA}wordgen{C.RESET}{C.DIM}>{C.RESET} ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n  {C.CYAN}[*]{C.RESET} Goodbye.\n")
            sys.exit(0)

        if not cmd:
            continue

        elif cmd in ("-h", "help"):
            print(HELP_TEXT)

        elif cmd == "clear":
            os.system("clear")
            print(BANNER)

        elif cmd in ("-c", "config"):
            show_config(session_data)

        elif cmd in ("-g", "generate", "-q", "quick"):
            quick = (cmd in ("-q", "quick"))
            print(f"\n  {C.CYAN}[*]{C.RESET} {'Quick' if quick else 'Full'} generation mode")
            print(f"  {C.DIM}Press Enter to skip optional fields.{C.RESET}\n")
            try:
                session_data = run_questionnaire(quick=quick)
            except KeyboardInterrupt:
                print(f"\n  {C.YELLOW}[!]{C.RESET} Aborted.\n")
                continue

            print(f"\n  {C.CYAN}[*]{C.RESET} Starting generation engine...")
            try:
                words = generate_wordlist(session_data, quick=quick)
            except KeyboardInterrupt:
                print(f"\n  {C.YELLOW}[!]{C.RESET} Generation interrupted.\n")
                continue

            # Use first available name as filename hint
            hints = (
                session_data.get('first_name', []) +
                session_data.get('last_name', []) +
                session_data.get('artist_name', [])
            )
            hint = hints[0] if hints else "target"
            save_wordlist(words, hint)

        else:
            print(f"  {C.RED}[!]{C.RESET} Unknown command: {C.WHITE}{cmd}{C.RESET}")
            print(f"  {C.DIM}Type {C.WHITE}-h{C.RESET}{C.DIM} for available commands.{C.RESET}\n")

# ─────────────────────────── ENTRY ─────────────────────────────────
if __name__ == "__main__":
    main()
