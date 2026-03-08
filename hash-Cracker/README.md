# Hash Cracker

- A dictionary-based password hash cracker built in Python.

# What it does
- Takes a hashed password and a wordlist as input
- Hashes each word in the wordlist and compares it to the target
- Reports the plaintext password if found

# How to run
```bash
python hash_cracker.py
```

# Supported algorithms
- MD5
- SHA1
- SHA256

# Concepts learned
- How hashing works
- Why MD5 is broken for passwords
- Dictionary attacks
- How real attackers crack leaked password databases

# Note
Requires a wordlist (rockyou.txt recommended). For educational use only.
