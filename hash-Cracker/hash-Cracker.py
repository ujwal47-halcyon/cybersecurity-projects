import hashlib
import sys

def hash_word(word, algorithm):
    """Hash a single word using the given algorithm."""
    h = hashlib.new(algorithm)
    h.update(word.encode('utf-8'))
    return h.hexdigest()

def crack(target_hash, wordlist_path, algorithm='md5'):
    """Try every word in the wordlist until we find a match."""
    print(f"\n[*] Target hash : {target_hash}")
    print(f"[*] Algorithm   : {algorithm}")
    print(f"[*] Wordlist    : {wordlist_path}")
    print(f"[*] Cracking...\n")

    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for count, line in enumerate(f):
                word = line.strip()
                if hash_word(word, algorithm) == target_hash:
                    print(f"[CRACKED] Password found: '{word}'")
                    print(f"[*] Found after {count+1} attempts.")
                    return word
                if count % 100000 == 0 and count != 0:
                    print(f"[*] Tried {count} passwords...")

    except FileNotFoundError:
        print(f"[ERROR] Wordlist not found: {wordlist_path}")
        sys.exit(1)

    print("[FAILED] Password not found in wordlist.")
    return None

# --- Entry point ---
if __name__ == "__main__":
    print("=== Hash Cracker ===")
    print("Algorithms: md5, sha1, sha256")
    algo = input("Algorithm: ").strip().lower()
    target = input("Enter hash to crack: ").strip()
    wordlist = input("Path to wordlist (or press Enter for rockyou.txt): ").strip()
    if not wordlist:
        wordlist = "rockyou.txt"
    crack(target, wordlist, algo)
