Task 6:

Mapping: A=0, B=1, ..., Z=25 (Z26)

Keystream Generation (k_i for i ≥ 1):
- k₁ = k mod 26
- k₂ = (k + 1) mod 26
- k_i = (k_{i-1} + k_{i-2}) mod 26 for i ≥ 3

Encryption:
c_i = (m_i + k_i) mod 26

Decryption:
m_i = (c_i - k_i) mod 26

Implementation Details
----------------------
Input: Text with spaces removed, converted to uppercase
Output: Ciphertext/plaintext as uppercase letters

Test Cases:
1. Encrypt "ILOVEWOLLONGONG" with key=3
   Result: LPVGWZJJEFXHZZD

2. Decrypt "MQJJ" with key=3
   Result: JMCY

Usage
-----
Run the script directly:
$ python encryption_and_decryption.py

Output:
Encrypt 'ILOVEWOLLONGONG' with key=3: LPVGWZJJEFXHZZD
Decrypt 'MQJJ' with key=3: JMCY
