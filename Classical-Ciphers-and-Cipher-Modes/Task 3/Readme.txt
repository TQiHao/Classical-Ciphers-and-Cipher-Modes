Task 3:

Question Analysis:
The task asks whether the function f(x) = x^k (mod 26) can be used as a cipher where k > 1 is the key and x is a letter to be encrypted (with A=0, B=1, ..., Z=25).

Key Findings (Summary):
- The function f(x) = x^k (mod 26) cannot be used as a cipher for k > 1
- Reason: Not all x ∈ {0,1,...,25} have unique inverses under this encryption
- The modulus 26 is composite (2×13), so many elements share factors with 26
- Elements that share factors with 26 (like 0, 13, etc.) cause collisions
- Example: x=13 always maps to 13 regardless of k
- Example with k=3: both x=1 and x=3 map to 1
- For a function to be a valid cipher, it must be a bijection (one-to-one and onto)
- Since f(x) = x^k (mod 26) is not a bijection for any k > 1, it cannot be used as a cipher

Full Analysis:
See Report3.docx for complete mathematical justification with examples and detailed explanation.

Note:
This submission contains only the analysis/documentation for Task 3. No executable program is required for this theoretical task.