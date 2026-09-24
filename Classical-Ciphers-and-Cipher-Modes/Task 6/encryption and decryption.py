def char_to_num(c):
    return ord(c) - ord('A')

def num_to_char(n):
    return chr(n + ord('A'))

def keystream(k, length):
    ks = []
    if length >= 1:
        ks.append(k % 26)
    if length >= 2:
        ks.append((k + 1) % 26)
    for i in range(2, length):
        ks.append((ks[i-1] + ks[i-2]) % 26)
    return ks

def encrypt(plaintext, k):
    plaintext = plaintext.replace(" ", "").upper()
    ks = keystream(k, len(plaintext))
    ciphertext = ""
    for i, ch in enumerate(plaintext):
        m = char_to_num(ch)
        c = (m + ks[i]) % 26
        ciphertext += num_to_char(c)
    return ciphertext

def decrypt(ciphertext, k):
    ciphertext = ciphertext.upper()
    ks = keystream(k, len(ciphertext))
    plaintext = ""
    for i, ch in enumerate(ciphertext):
        c = char_to_num(ch)
        m = (c - ks[i]) % 26
        plaintext += num_to_char(m)
    return plaintext

# Example usage:
if __name__ == "__main__":
    # Encrypt "ILOVEWOLLONGONG" with k=3
    plain = "ILOVEWOLLONGONG"
    key = 3
    cipher = encrypt(plain, key)
    print("Encrypt 'ILOVEWOLLONGONG' with key=3:")
    print(cipher)

    # Decrypt "MQJJ" with k=3
    cipher2 = "MQJJ"
    plain2 = decrypt(cipher2, key)
    print("\nDecrypt 'MQJJ' with key=3:")
    print(plain2)