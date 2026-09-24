#!/usr/bin/env python3
import sys
import random
import os

def generate_keypair():
    """
    Generates a random Kama Sutra key pairing (26 letters, each paired with another).
    'f' is paired but will be skipped during encryption/decryption.
    Returns a dictionary mapping each letter to its partner.
    """
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    random.shuffle(alphabet)
    pairs = {}
    
    # Pair first half with second half
    half = len(alphabet) // 2
    first_half = alphabet[:half]
    second_half = alphabet[half:]
    
    for i in range(half):
        a = first_half[i]
        b = second_half[i]
        pairs[a] = b
        pairs[b] = a
    
    # Ensure all letters are in the dictionary (should be 26 entries)
    return pairs

def save_key(key, filename):
    """Save key to a file in alphabet order for readability."""
    with open(filename, 'w') as f:
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            f.write(f"{letter}{key[letter]}\n")

def load_key(filename):
    """Load key from file."""
    key = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) == 2:
                a, b = line[0], line[1]
                key[a] = b
                key[b] = a
    return key

def encrypt(plaintext, key):
    """Encrypt plaintext using Kama Sutra cipher, skipping 'f'."""
    ciphertext = []
    for ch in plaintext:
        if ch == 'f' or ch not in key:  # 'f' is not replaced
            ciphertext.append(ch)
        else:
            ciphertext.append(key[ch])
    return ''.join(ciphertext)

def decrypt(ciphertext, key):
    """Decrypt ciphertext (same as encrypt in this cipher)."""
    return encrypt(ciphertext, key)  # Symmetric cipher

def process_file(input_file, output_file, key, mode='encrypt'):
    """Read input file, encrypt/decrypt, write to output file."""
    try:
        with open(input_file, 'r') as f:
            text = f.read().strip().lower()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    if mode == 'encrypt':
        result = encrypt(text, key)
    else:  # decrypt
        result = decrypt(text, key)
    
    with open(output_file, 'w') as f:
        f.write(result)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  kamasutra -k <keyfile.txt>")
        print("  kamasutra -e <keyfile.txt> <plaintext.txt> <ciphertext.txt>")
        print("  kamasutra -d <keyfile.txt> <ciphertext.txt> <plaintext.txt>")
        sys.exit(1)
    
    option = sys.argv[1]
    
    if option == '-k' and len(sys.argv) == 3:
        keyfile = sys.argv[2]
        key = generate_keypair()
        save_key(key, keyfile)
        print(f"Key generated and saved to {keyfile}")
    
    elif option == '-e' and len(sys.argv) == 5:
        _, _, keyfile, plaintext, ciphertext = sys.argv
        key = load_key(keyfile)
        process_file(plaintext, ciphertext, key, 'encrypt')
        print(f"Encryption complete. Ciphertext saved to {ciphertext}")
    
    elif option == '-d' and len(sys.argv) == 5:
        _, _, keyfile, ciphertext, plaintext = sys.argv
        key = load_key(keyfile)
        process_file(ciphertext, plaintext, key, 'decrypt')
        print(f"Decryption complete. Plaintext saved to {plaintext}")
    
    else:
        print("Invalid arguments. Check usage.")
        sys.exit(1)

if __name__ == '__main__':
    main()