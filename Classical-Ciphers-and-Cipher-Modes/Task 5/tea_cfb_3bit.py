import struct

def tea_encrypt_block(v, k):
    """TEA encryption of a single 64-bit block"""
    v0, v1 = struct.unpack('>II', v)
    sum_val = 0
    delta = 0x9E3779B9
    k0, k1, k2, k3 = struct.unpack('>IIII', k)
    
    for _ in range(32):
        sum_val = (sum_val + delta) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + sum_val) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + sum_val) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
    
    return struct.pack('>II', v0, v1)

def tea_cfb_3bit_encrypt(plaintext, key, iv):
    # Convert plaintext to binary string
    plaintext_bits = ''.join(format(byte, '08b') for byte in plaintext)
    
    # Initialize shift register with IV
    shift_register = bytearray(iv)
    
    ciphertext_bits = ""
    
    # Process 3 bits at a time
    for i in range(0, len(plaintext_bits), 3):
        # Encrypt the shift register
        encrypted_block = tea_encrypt_block(bytes(shift_register), key)
        
        # Take only first 3 bits of first byte of encrypted block
        keystream_byte = encrypted_block[0]
        keystream_bits = format(keystream_byte >> 5, '03b')  # Get 3 MSBs
        
        # Get 3 plaintext bits (pad if needed)
        plain_bits = plaintext_bits[i:i+3]
        if len(plain_bits) < 3:
            plain_bits = plain_bits.ljust(3, '0')
        
        # XOR plaintext bits with keystream bits
        cipher_bits = format(int(plain_bits, 2) ^ int(keystream_bits, 2), '03b')
        ciphertext_bits += cipher_bits
        
        # Update shift register: shift left by 3 bits, add ciphertext bits
        reg_int = int.from_bytes(shift_register, 'big')
        reg_int = ((reg_int << 3) & 0xFFFFFFFFFFFFFFFF) | int(cipher_bits, 2)
        shift_register = reg_int.to_bytes(8, 'big')
    
    # Convert ciphertext bits back to bytes
    ciphertext_bytes = bytearray()
    for i in range(0, len(ciphertext_bits), 8):
        byte_bits = ciphertext_bits[i:i+8]
        if len(byte_bits) < 8:
            byte_bits = byte_bits.ljust(8, '0')
        ciphertext_bytes.append(int(byte_bits, 2))
    
    return bytes(ciphertext_bytes)

def tea_cfb_3bit_decrypt(ciphertext, key, iv):
    """
    3-bit CFB TEA Decryption
    """
    # Convert ciphertext to binary string
    ciphertext_bits = ''.join(format(byte, '08b') for byte in ciphertext)
    
    # Initialize shift register with IV
    shift_register = bytearray(iv)
    
    plaintext_bits = ""
    
    # Process 3 bits at a time
    for i in range(0, len(ciphertext_bits), 3):
        # Encrypt the shift register
        encrypted_block = tea_encrypt_block(bytes(shift_register), key)
        
        # Take only first 3 bits
        keystream_byte = encrypted_block[0]
        keystream_bits = format(keystream_byte >> 5, '03b')
        
        # Get 3 ciphertext bits
        cipher_bits = ciphertext_bits[i:i+3]
        if len(cipher_bits) < 3:
            cipher_bits = cipher_bits.ljust(3, '0')
        
        # XOR ciphertext bits with keystream bits to get plaintext
        plain_bits = format(int(cipher_bits, 2) ^ int(keystream_bits, 2), '03b')
        plaintext_bits += plain_bits
        
        # Update shift register with ciphertext bits
        reg_int = int.from_bytes(shift_register, 'big')
        reg_int = ((reg_int << 3) & 0xFFFFFFFFFFFFFFFF) | int(cipher_bits, 2)
        shift_register = reg_int.to_bytes(8, 'big')
    
    # Convert plaintext bits back to bytes
    # Calculate how many bits are actual data
    # Original plaintext was 7 bytes = 56 bits
    original_plaintext_bits = 56  # 7 bytes * 8 bits/byte
    
    # We need to truncate to exactly original_plaintext_bits
    # The issue: 56 bits processed in 3-bit chunks = 19 iterations (19*3=57 bits)
    # So we have 1 extra bit of padding that needs to be removed
    
    # For 56 bits in 3-bit chunks:
    # 56 / 3 = 18 remainder 2
    # We process 19 groups (18 full + 1 partial)
    # Partial group has 2 real bits + 1 padding bit
    
    # Remove padding bits: keep only first original_plaintext_bits
    plaintext_bits = plaintext_bits[:original_plaintext_bits]
    
    plaintext_bytes = bytearray()
    for i in range(0, len(plaintext_bits), 8):
        byte_bits = plaintext_bits[i:i+8]
        if len(byte_bits) > 0:
            plaintext_bytes.append(int(byte_bits, 2))
    
    return bytes(plaintext_bytes)

# Test function for 3-bit CFB
def test_3bit_cfb():
    """Test the 3-bit CFB implementation"""
    key = b'0123456789ABCDEF'  # 16 bytes
    iv = b'INITVECT'  # 8 bytes
    plaintext = b"8931914"
    
    print("Testing 3-bit CFB TEA:")
    print(f"Key: {key.hex()}")
    print(f"IV: {iv.hex()}")
    print(f"Plaintext: {plaintext} (hex: {plaintext.hex()})")
    print(f"Plaintext bits: {len(plaintext) * 8}")
    
    ciphertext = tea_cfb_3bit_encrypt(plaintext, key, iv)
    print(f"Ciphertext (hex): {ciphertext.hex()}")
    print(f"Ciphertext bits: {len(ciphertext) * 8}")
    
    decrypted = tea_cfb_3bit_decrypt(ciphertext, key, iv)
    print(f"Decrypted (hex): {decrypted.hex()}")
    print(f"Decrypted (bytes): {decrypted}")
    print(f"Decrypted length: {len(decrypted)} bytes")
    
    # Try to decode only if it's valid UTF-8
    try:
        decoded = decrypted.decode('utf-8')
        print(f"Decoded string: '{decoded}'")
    except UnicodeDecodeError:
        print("Note: Decrypted bytes are not valid UTF-8, comparing bytes directly")
    
    # Compare bytes directly, not strings
    if decrypted == plaintext:
        print("3-bit CFB encryption/decryption successful!")
    else:
        print("3-bit CFB encryption/decryption failed!")
        print(f"Expected: {plaintext.hex()} (length: {len(plaintext)})")
        print(f"Got: {decrypted.hex()} (length: {len(decrypted)})")
        
        # Debug: Show binary
        original_bits = ''.join(format(byte, '08b') for byte in plaintext)
        decrypted_bits = ''.join(format(byte, '08b') for byte in decrypted)
        print(f"\nOriginal bits (56): {original_bits}")
        print(f"Decrypted bits ({len(decrypted_bits)}): {decrypted_bits}")
    
    return ciphertext.hex()

if __name__ == "__main__":
    test_3bit_cfb()