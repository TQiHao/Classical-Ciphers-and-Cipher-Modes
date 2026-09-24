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

def generate_keystream_sync(key, iv, length_bytes):
    """
    Generate keystream for synchronous cipher
    Uses counter mode-like approach
    """
    keystream = bytearray()
    
    # Use IV as initial counter
    counter = bytearray(iv)
    
    # Generate enough keystream bytes
    while len(keystream) < length_bytes:
        # Encrypt the counter
        encrypted_block = tea_encrypt_block(bytes(counter), key)
        keystream.extend(encrypted_block)
        
        # Increment counter (64-bit big-endian integer)
        counter_int = int.from_bytes(counter, 'big')
        counter_int = (counter_int + 1) & 0xFFFFFFFFFFFFFFFF
        counter = counter_int.to_bytes(8, 'big')
    
    # Trim to exact length needed
    return bytes(keystream[:length_bytes])

def tea_sync_encrypt(plaintext, key, iv):
    """Synchronous stream cipher encryption using TEA"""
    # Generate keystream
    keystream = generate_keystream_sync(key, iv, len(plaintext))
    
    # XOR plaintext with keystream
    ciphertext = bytearray()
    for p, k in zip(plaintext, keystream):
        ciphertext.append(p ^ k)
    
    return bytes(ciphertext)

def tea_sync_decrypt(ciphertext, key, iv):
    """Synchronous stream cipher decryption (same as encryption)"""
    # Synchronous cipher: decryption is identical to encryption
    return tea_sync_encrypt(ciphertext, key, iv)

def test_sync_cipher():
    """Test the synchronous cipher implementation"""
    key = b'0123456789ABCDEF'  # 16 bytes
    iv = b'INITVECT'  # 8 bytes
    plaintext = b"8931914"
    
    print("Testing Synchronous TEA Cipher:")
    print(f"Key: {key.hex()}")
    print(f"IV: {iv.hex()}")
    print(f"Plaintext: {plaintext} (hex: {plaintext.hex()})")
    
    ciphertext = tea_sync_encrypt(plaintext, key, iv)
    print(f"Ciphertext (hex): {ciphertext.hex()}")
    
    decrypted = tea_sync_decrypt(ciphertext, key, iv)
    print(f"Decrypted: {decrypted}")
    print(f"Decrypted matches original: {decrypted == plaintext}")

if __name__ == "__main__":
    test_sync_cipher()