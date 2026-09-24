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

def tea_cfb_2bit_encrypt(plaintext, key, iv):
    # Convert plaintext to binary string
    plaintext_bits = ''.join(format(byte, '08b') for byte in plaintext)
    
    # Initialize shift register with IV
    shift_register = bytearray(iv)
    
    ciphertext_bits = ""
    
    # Process 2 bits at a time
    for i in range(0, len(plaintext_bits), 2):
        # Encrypt the shift register
        encrypted_block = tea_encrypt_block(bytes(shift_register), key)
        
        # Take only first 2 bits of first byte of encrypted block
        keystream_byte = encrypted_block[0]
        keystream_bits = format(keystream_byte >> 6, '02b')  # Get 2 MSBs
        
        # Get 2 plaintext bits (pad if needed)
        plain_bits = plaintext_bits[i:i+2]
        if len(plain_bits) < 2:
            plain_bits = plain_bits.ljust(2, '0')
        
        # XOR plaintext bits with keystream bits
        cipher_bits = format(int(plain_bits, 2) ^ int(keystream_bits, 2), '02b')
        ciphertext_bits += cipher_bits
        
        # Update shift register: shift left by 2 bits, add ciphertext bits
        reg_int = int.from_bytes(shift_register, 'big')
        reg_int = ((reg_int << 2) & 0xFFFFFFFFFFFFFFFF) | int(cipher_bits, 2)
        shift_register = reg_int.to_bytes(8, 'big')
    
    # Convert ciphertext bits back to bytes
    ciphertext_bytes = bytearray()
    for i in range(0, len(ciphertext_bits), 8):
        byte_bits = ciphertext_bits[i:i+8]
        if len(byte_bits) < 8:
            byte_bits = byte_bits.ljust(8, '0')
        ciphertext_bytes.append(int(byte_bits, 2))
    
    return bytes(ciphertext_bytes)

def tea_cfb_2bit_decrypt(ciphertext, key, iv):
    """
    2-bit CFB TEA Decryption
    """
    # Convert ciphertext to binary string
    ciphertext_bits = ''.join(format(byte, '08b') for byte in ciphertext)
    
    # Initialize shift register with IV
    shift_register = bytearray(iv)
    
    plaintext_bits = ""
    
    # Process 2 bits at a time
    for i in range(0, len(ciphertext_bits), 2):
        # Encrypt the shift register
        encrypted_block = tea_encrypt_block(bytes(shift_register), key)
        
        # Take only first 2 bits
        keystream_byte = encrypted_block[0]
        keystream_bits = format(keystream_byte >> 6, '02b')
        
        # Get 2 ciphertext bits
        cipher_bits = ciphertext_bits[i:i+2]
        if len(cipher_bits) < 2:
            cipher_bits = cipher_bits.ljust(2, '0')
        
        # XOR ciphertext bits with keystream bits to get plaintext
        plain_bits = format(int(cipher_bits, 2) ^ int(keystream_bits, 2), '02b')
        plaintext_bits += plain_bits
        
        # Update shift register with ciphertext bits (not plaintext!)
        reg_int = int.from_bytes(shift_register, 'big')
        reg_int = ((reg_int << 2) & 0xFFFFFFFFFFFFFFFF) | int(cipher_bits, 2)
        shift_register = reg_int.to_bytes(8, 'big')
    
    # Convert plaintext bits back to bytes
    # Calculate how many bits are actual data (remove padding)
    original_bit_length = len(plaintext_bits)
    
    # Remove padding bits from plaintext_bits
    # The actual plaintext length in bits is based on the original plaintext
    # For 7 bytes (56 bits), 56 % 2 = 0, so no padding needed
    # But we need to handle general case
    
    # Calculate original plaintext bits from ciphertext
    # Each ciphertext bit corresponds to one plaintext bit in CFB mode
    ciphertext_bit_length = len(ciphertext) * 8
    
    # The number of plaintext bits is the same as ciphertext bits in CFB
    # But we process 2 bits at a time, so we might have extra padding bits
    if ciphertext_bit_length % 2 != 0:
        padding_bits = 2 - (ciphertext_bit_length % 2)
        # Remove padding bits from the end
        plaintext_bits = plaintext_bits[:original_bit_length - padding_bits]
    
    # Also, if the original plaintext wasn't a multiple of 8 bits,
    # we need to remove extra bits at byte boundaries
    # For student number "8931914" (7 bytes = 56 bits), no issue
    
    plaintext_bytes = bytearray()
    for i in range(0, len(plaintext_bits), 8):
        byte_bits = plaintext_bits[i:i+8]
        if len(byte_bits) > 0:
            plaintext_bytes.append(int(byte_bits, 2))
    
    return bytes(plaintext_bytes)

# Test function for 2-bit CFB
def test_2bit_cfb():
    """Test the 2-bit CFB implementation"""
    key = b'0123456789ABCDEF'  # 16 bytes
    iv = b'INITVECT'  # 8 bytes
    plaintext = b"8931914"
    
    print("Testing 2-bit CFB TEA:")
    print(f"Key: {key.hex()}")
    print(f"IV: {iv.hex()}")
    print(f"Plaintext: {plaintext} (hex: {plaintext.hex()})")
    print(f"Plaintext bits: {len(plaintext) * 8}")
    
    ciphertext = tea_cfb_2bit_encrypt(plaintext, key, iv)
    print(f"Ciphertext (hex): {ciphertext.hex()}")
    print(f"Ciphertext bits: {len(ciphertext) * 8}")
    
    decrypted = tea_cfb_2bit_decrypt(ciphertext, key, iv)
    print(f"Decrypted (hex): {decrypted.hex()}")
    print(f"Decrypted (bytes): {decrypted}")
    
    # Try to decode only if it's valid UTF-8
    try:
        decoded = decrypted.decode('utf-8')
        print(f"Decoded string: '{decoded}'")
    except UnicodeDecodeError:
        print("Note: Decrypted bytes might have padding, comparing bytes directly")
    
    # Compare bytes directly, not strings
    if decrypted == plaintext:
        print("2-bit CFB encryption/decryption successful!")
    else:
        print("2-bit CFB encryption/decryption failed!")
        print(f"Expected bytes: {plaintext.hex()}")
        print(f"Got bytes: {decrypted.hex()}")
        print(f"Expected length: {len(plaintext)}")
        print(f"Got length: {len(decrypted)}")
    
    return ciphertext.hex()

if __name__ == "__main__":
    test_2bit_cfb()