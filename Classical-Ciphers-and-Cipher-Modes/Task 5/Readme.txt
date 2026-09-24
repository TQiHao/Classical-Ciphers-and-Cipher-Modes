Task 5:

Implementation Details
----------------------
Student Number: 8931914
Sum of digits: 8+9+3+1+9+1+4 = 35
c = 35 mod 5 = 0

Since c = 0, we implemented 3-bit CFB TEA instead of 0-bit CFB.

Common Parameters:
- Key: b'0123456789ABCDEF' (16 bytes, hex: 30313233343536373839414243444546)
- IV: b'INITVECT' (8 bytes, hex: 494e495456454354)
- TEA constants: delta = 0x9E3779B9, 32 rounds

2-bit CFB TEA Algorithm:
- Processes data in 2-bit segments
- 56-bit plaintext requires 28 iterations
- Each iteration: TEA encryption → extract 2 MSBs → XOR → shift

3-bit CFB TEA Algorithm:
- Processes data in 3-bit segments
- 56-bit plaintext requires 19 iterations (with padding)
- Each iteration: TEA encryption → extract 3 MSBs → XOR → shift

Usage Instructions
------------------
1. Run individual implementations:
   $ python tea_cfb_2bit.py      # Test 2-bit CFB
   $ python tea_cfb_3bit.py      # Test 3-bit CFB

2. Run the main comparison script:
   $ python encrypt_student_number.py

   This script will:
   - Calculate c from student number
   - Encrypt with both 2-bit and 3-bit CFB
   - Display timing comparison
   - Optionally run performance test (1000 iterations)

3. View results:
   Results are saved to `task5_results.txt`

Encryption Results
------------------
Plaintext (student number): "8931914"

2-bit CFB Ciphertext (hex): af943d302d3b83
3-bit CFB Ciphertext (hex): b25bb4fc467bd500

Performance Comparison
----------------------
Single-run times:
- 2-bit CFB: 0.00115310 seconds
- 3-bit CFB: 0.00138880 seconds

Average times (1000 iterations):
- 2-bit CFB: 0.00110097 seconds per encryption
- 3-bit CFB: 0.00072888 seconds per encryption

Performance Analysis:
- 3-bit CFB is faster because it requires fewer iterations
- 56 bits / 2 bits/iteration = 28 iterations (2-bit CFB)
- 56 bits / 3 bits/iteration = 19 iterations (3-bit CFB)
- 28 - 19 = 9 fewer TEA encryotions per message
- Each TEA encryption = 32 rounds = significant computation savings

Key Technical Points
--------------------
1. CFB Mode Characteristics:
   - Self-synchronizing stream cipher
   - Encryption and decryption use same process
   - Previous ciphertext becomes input for next block

2. Bit-level Processing:
   - Unlike block ciphers that process 64-bit blocks, CFB processes bits
   - Allows encryption of data not aligned to block boundaries
   - Enables real-time encryption of streaming data

3. Implementation Challenges:
   - Bit manipulation requires careful handling
   - Padding needed for non-multiple bit lengths
   - Shift register management at bit level
   - Conversion between bits and bytes

Testing and Verification
------------------------
All implementations include test functions that verify:
1. Encryption/decryption round-trip correctness
2. Different ciphertexts for 2-bit vs 3-bit modes
3. Proper handling of padding bits
4. Consistent results across multiple runs
