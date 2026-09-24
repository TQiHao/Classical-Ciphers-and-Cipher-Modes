# Classical-Ciphers-and-Cipher-Modes
A cryptography lab implementing classical ciphers (substitution, Kama Sutra), cryptanalysis techniques, and CFB stream cipher modes with performance analysis.

# Classical Ciphers, Cryptanalysis & Cipher Modes

A seven-task cryptography lab covering classical ciphers, statistical
cryptanalysis, and block/stream cipher modes — implemented from scratch with
performance benchmarking.

---

## Overview

This assignment builds practical familiarity with classical ciphers and
modern cipher modes by implementing each algorithm and analysing its
security properties.

---

## Tasks

### Task 1 — Cryptanalysis (2 marks)
Broke a monoalphabetic cipher and a Vigenère cipher using statistical
methods (frequency analysis, index of coincidence) with the provided
`krypto` tool. Documented each step and justification in `Report1.pdf`,
producing plaintext and key files for both ciphers.

**Skills:** Frequency analysis, Kasiski examination, Vigenère cryptanalysis.

---

### Task 2 — Keyword Substitution Cipher (2 marks)
Implemented a keyword-based substitution cipher as a command-line program.
Constructs a key from a keyword (deduplicated, then reverse-alphabet fill),
encrypts plaintext files, decrypts ciphertext files, preserves punctuation,
and handles input errors.

**Skills:** Cipher design, CLI programming, error handling.

---

### Task 3 — Analysis of `f(x) = x^k mod 26` (2 marks)
Analysed whether modular exponentiation can serve as a substitution cipher,
examining bijectivity, key space, and invertibility for various `k`.

**Skills:** Modular arithmetic, permutation analysis, cipher strength evaluation.

---

### Task 4 — Flipped Kama Sutra Cipher (2 marks)
Implemented the Kama Sutra cipher with the "flipped" rule (letter `f` is not
substituted). Generates a random keyfile, encrypts `Ptext-1.txt` to
`Ctext-3.txt`, and analyses letter-frequency distributions against the
monoalphabetic and Vigenère ciphertexts in `Report2.pdf`. Also discussed
keyless decryption of the cipher.

**Skills:** Random key generation, frequency-distribution comparison,
ciphertext-only cryptanalysis.

---

### Task 5 — 2-bit & c-bit CFB TEA (3 marks)
Implemented TEA in 2-bit CFB mode, then a c-bit variant where
`c = (sum of student number digits) mod 5`. Encrypted a student number with
both and benchmarked performance in `Task5Report.PDF`.

**Skills:** TEA block cipher, CFB mode, timing analysis.

---

### Task 6 — Synchronous Stream Cipher (2 marks)
Implemented a Fibonacci-style synchronous stream cipher over Z₂₆:
`k₁ = k`, `k₂ = k+1`, `kᵢ = kᵢ₋₁ + kᵢ₋₂ mod 26`. Encrypted
`"I LOVE WOLLONGONG"` with key 3 and decrypted `"MQJ"` with key 3.

**Skills:** Stream cipher design, keystream generation, modular arithmetic.

---

### Task 7 — Hybrid Cipher Benchmark (2 marks)
Encrypted a 200 MB document with:
1. 1-bit CFB TEA
2. The Task 6 synchronous cipher
3. A hybrid (odd chars → 1-bit CFB, even chars → synchronous cipher)

Measured and explained encryption/decryption timing differences in
`Report7.pdf`.

**Skills:** Performance benchmarking, hybrid cipher design, trade-off analysis.


