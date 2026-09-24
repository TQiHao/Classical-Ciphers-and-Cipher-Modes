Task 4:

Installation and Setup
----------------------
1. Ensure Python 3 is installed on your system
2. Make the script executable:
   $ chmod +x Kamasutra.py
3. Or use the provided Makefile:
   $ make

Usage Instructions
------------------
Generate a new key:
  $ python Kamasutra.py -k keyfile.txt

Encrypt a file:
  $ python Kamasutra.py -e keyfile.txt plaintext.txt ciphertext.txt

Decrypt a file:
  $ python Kamasutra.py -d keyfile.txt ciphertext.txt plaintext.txt

Key File Format
---------------
The key file contains one letter pair per line. For example:
  ay    (means 'a' encrypts to 'y' and 'y' encrypts to 'a')
  bo    (means 'b' encrypts to 'o' and 'o' encrypts to 'b')
  ... etc.

Each letter appears exactly twice in the file - once as the first character
and once as the second character of a pair.

Testing
-------
Run the test suite using the Makefile:
  $ make test

This will:
1. Generate a new key
2. Encrypt Ptext-1.txt to Ctext-3.txt
3. Decrypt Ctext-3.txt back to plaintext
4. Verify the decrypted text matches the original

Example
-------
Plaintext:  "hello world"
Encryption: Based on key pairings, each letter (except 'f') is replaced
            with its paired letter

See Report4.pdf for:
- Frequency analysis comparisons with Caesar and Vigenère ciphers
- Statistical properties of the ciphertext
- Implementation details and code explanation
- Visual comparisons of letter frequency distributions
