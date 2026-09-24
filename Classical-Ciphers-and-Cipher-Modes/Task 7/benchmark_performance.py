import time
import os
from tea_cfb_1bit import tea_cfb_1bit_encrypt, tea_cfb_1bit_decrypt
from tea_sync_cipher import tea_sync_encrypt, tea_sync_decrypt
from hybrid_cipher import hybrid_encrypt, hybrid_decrypt

def create_test_file(filename, size_mb):
    """Create a test file of specified size"""
    size_bytes = size_mb * 1024 * 1024
    chunk_size = 1024 * 1024  # 1MB
    
    print(f"Creating test file: {filename} ({size_mb}MB)...")
    
    with open(filename, 'wb') as f:
        for i in range(size_mb):
            # Write different patterns to avoid compression
            data = bytes([(i + j) % 256 for j in range(chunk_size)])
            f.write(data)
            if (i + 1) % 20 == 0:
                print(f"  Created {(i + 1)}/{size_mb} MB...")
    
    print(f"Test file created: {filename}")

def benchmark_mode(filename, encrypt_func, decrypt_func, mode_name, key, iv):
    """Benchmark a single encryption mode"""
    print(f"\n{'='*60}")
    print(f"Benchmarking: {mode_name}")
    print(f"{'='*60}")
    
    # Read file
    with open(filename, 'rb') as f:
        data = f.read()
    
    file_size_mb = len(data) / (1024 * 1024)
    print(f"File size: {file_size_mb:.2f} MB")
    
    # Encryption benchmark
    print("\nEncrypting...")
    start_time = time.time()
    ciphertext = encrypt_func(data, key, iv)
    encrypt_time = time.time() - start_time
    
    print(f"Encryption time: {encrypt_time:.2f} seconds")
    print(f"Encryption speed: {file_size_mb / encrypt_time:.2f} MB/s")
    
    # Decryption benchmark
    print("\nDecrypting...")
    start_time = time.time()
    decrypted = decrypt_func(ciphertext, key, iv)
    decrypt_time = time.time() - start_time
    
    print(f"Decryption time: {decrypt_time:.2f} seconds")
    print(f"Decryption speed: {file_size_mb / decrypt_time:.2f} MB/s")
    
    # Verification
    if decrypted == data:
        print("✓ Verification: PASSED")
    else:
        print("✗ Verification: FAILED")
        # Check for first mismatch
        for i in range(min(len(data), len(decrypted))):
            if data[i] != decrypted[i]:
                print(f"First mismatch at byte {i}: {data[i]:02x} != {decrypted[i]:02x}")
                break
    
    return encrypt_time, decrypt_time

def main():
    # Configuration
    TEST_FILE_SMALL = "test_10mb.bin"  # For quick testing
    TEST_FILE_LARGE = "test_200mb.bin"  # For final benchmark
    KEY = b'0123456789ABCDEF'
    IV = b'INITVECT'
    
    print("CRYPTOGRAPHY PERFORMANCE BENCHMARK")
    print("="*60)
    
    # Use smaller file for initial testing
    use_large_file = input("Use 200MB file for benchmarking? (y/n, n uses 10MB): ").lower() == 'y'
    
    if use_large_file:
        test_file = TEST_FILE_LARGE
        file_size = 200
    else:
        test_file = TEST_FILE_SMALL
        file_size = 10
    
    # Create test file if needed
    if not os.path.exists(test_file):
        create_test_file(test_file, file_size)
    
    # Run benchmarks
    results = {}
    
    # 1-bit CFB
    results['1bit_cfb'] = benchmark_mode(
        test_file, tea_cfb_1bit_encrypt, tea_cfb_1bit_decrypt, 
        "1-bit CFB TEA", KEY, IV
    )
    
    # Synchronous Cipher
    results['sync'] = benchmark_mode(
        test_file, tea_sync_encrypt, tea_sync_decrypt,
        "Synchronous Cipher", KEY, IV
    )
    
    # Hybrid Cipher
    results['hybrid'] = benchmark_mode(
        test_file, hybrid_encrypt, hybrid_decrypt,
        "Hybrid Cipher (1-bit CFB + Synchronous)", KEY, IV
    )
    
    # Print summary
    print(f"\n{'='*60}")
    print("PERFORMANCE SUMMARY")
    print(f"{'='*60}")
    print(f"{'Mode':<30} {'Encrypt (s)':<15} {'Decrypt (s)':<15} {'Total (s)':<15}")
    print(f"{'-'*75}")
    
    for mode_name, (enc_time, dec_time) in results.items():
        total_time = enc_time + dec_time
        if mode_name == '1bit_cfb':
            display_name = '1-bit CFB'
        elif mode_name == 'sync':
            display_name = 'Synchronous'
        else:
            display_name = 'Hybrid'
        
        print(f"{display_name:<30} {enc_time:<15.2f} {dec_time:<15.2f} {total_time:<15.2f}")
    
    # Save results to file
    with open('report7_results.txt', 'w') as f:
        f.write("PERFORMANCE BENCHMARK REPORT\n")
        f.write("="*50 + "\n\n")
        f.write(f"Test File: {test_file} ({file_size}MB)\n")
        f.write(f"Key: {KEY.hex()}\n")
        f.write(f"IV: {IV.hex()}\n\n")
        
        f.write("RESULTS:\n")
        f.write("-"*50 + "\n")
        for mode_name, (enc_time, dec_time) in results.items():
            if mode_name == '1bit_cfb':
                name = '1-bit CFB'
            elif mode_name == 'sync':
                name = 'Synchronous Cipher'
            else:
                name = 'Hybrid Cipher'
            
            f.write(f"{name}:\n")
            f.write(f"  Encryption: {enc_time:.2f} seconds\n")
            f.write(f"  Decryption: {dec_time:.2f} seconds\n")
            f.write(f"  Total: {enc_time + dec_time:.2f} seconds\n\n")
        
        # Analysis
        f.write("\nANALYSIS:\n")
        f.write("-"*50 + "\n")
        f.write("1. 1-bit CFB is extremely slow because:\n")
        f.write("   - Each bit requires a full TEA encryption (32 rounds)\n")
        f.write(f"   - For {file_size}MB: {file_size*1024*1024*8:,} TEA encryptions\n\n")
        
        f.write("2. Synchronous cipher is fast because:\n")
        f.write("   - Each TEA encryption produces 8 bytes of keystream\n")
        f.write(f"   - Only {file_size*1024*1024//8:,} TEA encryptions needed\n\n")
        
        f.write("3. Hybrid approach performance:\n")
        f.write("   - Combines both methods: 50% 1-bit CFB, 50% synchronous\n")
        f.write("   - Expected to be about halfway between both extremes\n")
        f.write("   - In practice, synchronous portion dominates due to parallelism\n")
    
    print(f"\nResults saved to 'report7_results.txt'")

if __name__ == "__main__":
    main()