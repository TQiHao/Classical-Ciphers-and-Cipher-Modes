import struct
from tea_cfb_1bit import tea_cfb_1bit_encrypt, tea_cfb_1bit_decrypt
from tea_sync_cipher import generate_keystream_sync

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

def hybrid_encrypt(plaintext, key, iv):
    """
    Hybrid encryption:
    - Odd bytes (1-indexed): 1-bit CFB
    - Even bytes (1-indexed): Synchronous cipher
    """
    ciphertext = bytearray(len(plaintext))
    
    # Pre-generate keystream for synchronous portions
    keystream = generate_keystream_sync(key, iv, len(plaintext))
    
    # Initialize CFB shift register
    cfb_shift_register = bytearray(iv)
    
    # Process each byte
    for i in range(len(plaintext)):
        if i % 2 == 0:  # Even index (0, 2, 4, ...) → 1-bit CFB
            # Convert byte to bits
            byte_bits = format(plaintext[i], '08b')
            
            # Process each bit with CFB
            cipher_byte_bits = ""
            for bit_pos in range(8):
                # Encrypt the shift register
                encrypted_block = tea_encrypt_block(bytes(cfb_shift_register), key)
                
                # Get keystream bit
                keystream_byte = encrypted_block[0]
                keystream_bit = (keystream_byte >> 7) & 0x01
                
                # Get plaintext bit
                plain_bit = int(byte_bits[bit_pos])
                
                # XOR
                cipher_bit = plain_bit ^ keystream_bit
                cipher_byte_bits += str(cipher_bit)
                
                # Update shift register
                reg_int = int.from_bytes(cfb_shift_register, 'big')
                reg_int = ((reg_int << 1) & 0xFFFFFFFFFFFFFFFF) | cipher_bit
                cfb_shift_register = reg_int.to_bytes(8, 'big')
            
            # Store cipher byte
            ciphertext[i] = int(cipher_byte_bits, 2)
        else:  # Odd index → synchronous cipher
            ciphertext[i] = plaintext[i] ^ keystream[i]
    
    return bytes(ciphertext)

def hybrid_decrypt(ciphertext, key, iv):
    """
    Hybrid decryption
    """
    plaintext = bytearray(len(ciphertext))
    
    # Pre-generate keystream for synchronous portions
    keystream = generate_keystream_sync(key, iv, len(ciphertext))
    
    # Initialize CFB shift register
    cfb_shift_register = bytearray(iv)
    
    # Process each byte
    for i in range(len(ciphertext)):
        if i % 2 == 0:  # Even index → 1-bit CFB
            # Convert cipher byte to bits
            cipher_byte_bits = format(ciphertext[i], '08b')
            
            # Process each bit with CFB
            plain_byte_bits = ""
            for bit_pos in range(8):
                # Encrypt the shift register
                encrypted_block = tea_encrypt_block(bytes(cfb_shift_register), key)
                
                # Get keystream bit
                keystream_byte = encrypted_block[0]
                keystream_bit = (keystream_byte >> 7) & 0x01
                
                # Get ciphertext bit
                cipher_bit = int(cipher_byte_bits[bit_pos])
                
                # XOR
                plain_bit = cipher_bit ^ keystream_bit
                plain_byte_bits += str(plain_bit)
                
                # Update shift register with ciphertext bit
                reg_int = int.from_bytes(cfb_shift_register, 'big')
                reg_int = ((reg_int << 1) & 0xFFFFFFFFFFFFFFFF) | cipher_bit
                cfb_shift_register = reg_int.to_bytes(8, 'big')
            
            # Store plain byte
            plaintext[i] = int(plain_byte_bits, 2)
        else:  # Odd index → synchronous cipher
            plaintext[i] = ciphertext[i] ^ keystream[i]
    
    return bytes(plaintext)

def test_hybrid():
    """Test the hybrid cipher implementation"""
    key = b'0123456789ABCDEF'
    iv = b'INITVECT'
    plaintext = b"8931914"
    
    print("Testing Hybrid Cipher (1-bit CFB + Synchronous):")
    print(f"Key: {key.hex()}")
    print(f"IV: {iv.hex()}")
    print(f"Plaintext: {plaintext} (hex: {plaintext.hex()})")
    
    ciphertext = hybrid_encrypt(plaintext, key, iv)
    print(f"Ciphertext (hex): {ciphertext.hex()}")
    
    decrypted = hybrid_decrypt(ciphertext, key, iv)
    print(f"Decrypted: {decrypted}")
    print(f"Success: {decrypted == plaintext}")

if __name__ == "__main__":
    test_hybrid()