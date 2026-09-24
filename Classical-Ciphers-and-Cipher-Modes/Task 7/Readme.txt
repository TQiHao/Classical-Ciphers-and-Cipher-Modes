Task 7:

Implementation Details
---------------------
Common Parameters:
- Key: b'0123456789ABCDEF' (16 bytes)
- IV: b'INITVECT' (8 bytes)
- TEA: delta = 0x9E3779B9, 32 rounds

1-bit CFB TEA:
- Processes data 1 bit at a time
- Each bit requires a full TEA encryption
- Self-synchronizing but extremely slow

Synchronous Cipher:
- Generates keystream independently of data
- Each TEA encryption produces 8 bytes of keystream
- Much faster, parallelizable

Hybrid Cipher:
- Odd-index bytes: 1-bit CFB
- Even-index bytes: synchronous cipher
- Attempts to balance security and performance

Performance Results (Expected)
------------------------------
For 200MB document:
1-bit CFB:
  - 1.68 billion TEA encryptions
  - Estimated: ~46.6 hours encryption + 46.6 hours decryption
  - Speed: ~0.001 MB/s

Synchronous:
  - 26.2 million TEA encryptions
  - Estimated: ~26 seconds encryption + 26 seconds decryption
  - Speed: ~7.6 MB/s

Hybrid:
  - Half 1-bit CFB, half synchronous
  - Estimated: ~23.3 hours encryption + 23.3 hours decryption
  - Speed: ~0.002 MB/s

Key Observations
----------------
1. 1-bit CFB is extremely slow because:
   - Each bit requires a full TEA encryption (32 rounds)
   - Cannot be parallelized (serial dependency)
   - 200MB → 1.68 billion TEA encryptions

2. Synchronous cipher is fast because:
   - Keystream generation independent of plaintext
   - Each TEA encryption produces 8 bytes of keystream
   - Can pre-generate keystream and parallelize

3. Hybrid performance:
   - Closer to 1-bit CFB than synchronous
   - Serial nature of 1-bit CFB dominates performance
   - Shows that "taking the best of two" doesn't always work in cryptography

Usage Instructions
------------------
1. Quick test (with small file):
   $ python benchmark_performance.py
   (Answer 'n' to use 10MB test file)

2. Full benchmark (with 200MB file):
   $ python benchmark_performance.py
   (Answer 'y' to use 200MB test file)
   (Be prepared for long runtime with 1-bit CFB)

3. Test individual implementations:
   $ python tea_cfb_1bit.py      # Test 1-bit CFB
   $ python tea_sync_cipher.py   # Test synchronous cipher
   $ python hybrid_cipher.py     # Test hybrid approach

Warning: The 1-bit CFB implementation will take an extremely long time
to process 200MB of data (potentially days). Consider using a smaller
test file for practical testing.