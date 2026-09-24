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

def tea_cfb_1bit_encrypt(plaintext, key, iv):
    """1-bit CFB TEA Encryption"""
    # Convert plaintext to binary string
    plaintext_bits = ''.join(format(byte, '08b') for byte in plaintext)
    
    # Initialize shift register with IV
    shift_register = bytearray(iv)
    
    ciphertext_bits = ""
    
    # Process 1 bit at a time
    for i in range(len(plaintext_bits)):
        # Encrypt the shift register
        encrypted_block = tea_encrypt_block(bytes(shift_register), key)
        
        # Take only first bit of first byte
        keystream_byte = encrypted_block[0]
        keystream_bit = (keystream_byte >> 7) & 0x01
        
        # Get 1 plaintext bit
        plain_bit = int(plaintext_bits[i])
        
        # XOR plaintext bit with keystream bit
        cipher_bit = plain_bit ^ keystream_bit
        ciphertext_bits += str(cipher_bit)
        
        # Update shift register
        reg_int = int.from_bytes(shift_register, 'big')
        reg_int = ((reg_int << 1) & 0xFFFFFFFFFFFFFFFF) | cipher_bit
        shift_register = reg_int.to_bytes(8, 'big')
    
    # Convert ciphertext bits back to bytes
    ciphertext_bytes = bytearray()
    for i in range(0, len(ciphertext_bits), 8):
        byte_bits = ciphertext_bits[i:i+8]
        if len(byte_bits) < 8:
            byte_bits = byte_bits.ljust(8, '0')
        ciphertext_bytes.append(int(byte_bits, 2))
    
    return bytes(ciphertext_bytes)

def tea_cfb_1bit_decrypt(ciphertext, key, iv):
    """1-bit CFB TEA Decryption"""
    # Convert ciphertext to binary string
    ciphertext_bits = ''.join(format(byte, '08b') for byte in ciphertext)
    
    # Initialize shift register with IV
    shift_register = bytearray(iv)
    
    plaintext_bits = ""
    
    # Process 1 bit at a time
    for i in range(len(ciphertext_bits)):
        # Encrypt the shift register
        encrypted_block = tea_encrypt_block(bytes(shift_register), key)
        
        # Take only first bit
        keystream_byte = encrypted_block[0]
        keystream_bit = (keystream_byte >> 7) & 0x01
        
        # Get 1 ciphertext bit
        cipher_bit = int(ciphertext_bits[i])
        
        # XOR ciphertext bit with keystream bit
        plain_bit = cipher_bit ^ keystream_bit
        plaintext_bits += str(plain_bit)
        
        # Update shift register with ciphertext bits
        reg_int = int.from_bytes(shift_register, 'big')
        reg_int = ((reg_int << 1) & 0xFFFFFFFFFFFFFFFF) | cipher_bit
        shift_register = reg_int.to_bytes(8, 'big')
    
    # Convert plaintext bits back to bytes
    # Remove padding if necessary
    original_bit_length = len(plaintext_bits)
    ciphertext_bit_length = len(ciphertext) * 8
    
    if ciphertext_bit_length % 8 != 0:
        padding_bits = 8 - (ciphertext_bit_length % 8)
        if original_bit_length > padding_bits:
            plaintext_bits = plaintext_bits[:original_bit_length - padding_bits]
    
    plaintext_bytes = bytearray()
    for i in range(0, len(plaintext_bits), 8):
        byte_bits = plaintext_bits[i:i+8]
        if len(byte_bits) == 8:
            plaintext_bytes.append(int(byte_bits, 2))
    
    return bytes(plaintext_bytes)

def test_1bit_cfb():
    """Test the 1-bit CFB implementation"""
    key = b'0123456789ABCDEF'
    iv = b'INITVECT'
    plaintext = b"8931914"
    
    print("Testing 1-bit CFB TEA:")
    print(f"Key: {key.hex()}")
    print(f"IV: {iv.hex()}")
    print(f"Plaintext: {plaintext} (hex: {plaintext.hex()})")
    print(f"Plaintext bits: {len(plaintext) * 8}")
    
    ciphertext = tea_cfb_1bit_encrypt(plaintext, key, iv)
    print(f"Ciphertext (hex): {ciphertext.hex()}")
    print(f"Ciphertext bits: {len(ciphertext) * 8}")
    
    decrypted = tea_cfb_1bit_decrypt(ciphertext, key, iv)
    print(f"Decrypted: {decrypted}")
    print(f"Success: {decrypted == plaintext}")

if __name__ == "__main__":
    test_1bit_cfb()