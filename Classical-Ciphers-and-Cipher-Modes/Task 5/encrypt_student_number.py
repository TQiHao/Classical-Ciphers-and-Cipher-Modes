import time
from tea_cfb_2bit import tea_cfb_2bit_encrypt
from tea_cfb_3bit import tea_cfb_3bit_encrypt

def calculate_c():
    """Calculate c = sum of digits mod 5"""
    student_number = "8931914"
    digits_sum = sum(int(d) for d in student_number)
    c = digits_sum % 5
    return student_number, digits_sum, c

def encrypt_and_compare():
    """Encrypt student number with both methods and compare times"""
    student_number, digits_sum, c = calculate_c()
    
    # Fixed key and IV for consistency
    key = b'0123456789ABCDEF'  # 16 bytes
    iv = b'INITVECT'  # 8 bytes
    plaintext = student_number.encode()
    
    print("=" * 70)
    print("TASK FIVE: CFB TEA ENCRYPTION OF STUDENT NUMBER")
    print("=" * 70)
    print(f"Student Number: {student_number}")
    print(f"Sum of digits: {digits_sum}")
    print(f"c = {digits_sum} mod 5 = {c}")
    print(f"\nSince c = {c}, implementing 3-bit CFB instead of {c}-bit CFB")
    
    print("\n" + "=" * 70)
    print("PART 2: 2-bit CFB TEA Encryption")
    print("=" * 70)
    
    # Time 2-bit CFB encryption
    start_time_2bit = time.perf_counter()
    ciphertext_2bit = tea_cfb_2bit_encrypt(plaintext, key, iv)
    end_time_2bit = time.perf_counter()
    time_2bit = end_time_2bit - start_time_2bit
    
    print(f"Plaintext: {plaintext.decode()}")
    print(f"Key (hex): {key.hex()}")
    print(f"IV (hex): {iv.hex()}")
    print(f"Ciphertext (hex): {ciphertext_2bit.hex()}")
    print(f"Encryption Time: {time_2bit:.8f} seconds")
    
    print("\n" + "=" * 70)
    print("PART 3: 3-bit CFB TEA Encryption (since c = 0)")
    print("=" * 70)
    
    # Time 3-bit CFB encryption
    start_time_3bit = time.perf_counter()
    ciphertext_3bit = tea_cfb_3bit_encrypt(plaintext, key, iv)
    end_time_3bit = time.perf_counter()
    time_3bit = end_time_3bit - start_time_3bit
    
    print(f"Plaintext: {plaintext.decode()}")
    print(f"Key (hex): {key.hex()}")
    print(f"IV (hex): {iv.hex()}")
    print(f"Ciphertext (hex): {ciphertext_3bit.hex()}")
    print(f"Encryption Time: {time_3bit:.8f} seconds")
    
    print("\n" + "=" * 70)
    print("TIME COMPARISON")
    print("=" * 70)
    print(f"2-bit CFB Encryption Time: {time_2bit:.8f} seconds")
    print(f"3-bit CFB Encryption Time: {time_3bit:.8f} seconds")
    
    time_difference = time_3bit - time_2bit
    percentage_diff = (time_difference / time_2bit) * 100 if time_2bit > 0 else 0
    
    if time_3bit < time_2bit:
        print(f"\n3-bit CFB is FASTER by {abs(time_difference):.8f} seconds ({abs(percentage_diff):.2f}%)")
        print("\nReason: 3-bit CFB processes 3 bits per iteration instead of 2 bits,")
        print("requiring fewer iterations (19 vs 28) to encrypt the same data.")
    else:
        print(f"\n3-bit CFB is SLOWER by {abs(time_difference):.8f} seconds ({abs(percentage_diff):.2f}%)")
    
    print("\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print("Total bits in '8931914' (7 characters × 8 bits = 56 bits):")
    print("- 2-bit CFB: 56 bits / 2 bits per iteration = 28 iterations")
    print("- 3-bit CFB: 56 bits / 3 bits per iteration = 19 iterations (with padding)")
    print("\nEach iteration requires a full TEA encryption (32 rounds).")
    print("Fewer iterations = less overhead = faster encryption.")
    
    # Return results for report
    return {
        'student_number': student_number,
        'digits_sum': digits_sum,
        'c': c,
        'ciphertext_2bit': ciphertext_2bit.hex(),
        'ciphertext_3bit': ciphertext_3bit.hex(),
        'time_2bit': time_2bit,
        'time_3bit': time_3bit,
        'time_difference': time_difference
    }

def performance_test():
    """Run multiple iterations for more accurate timing"""
    print("\n" + "=" * 70)
    print("PERFORMANCE TEST (1000 iterations)")
    print("=" * 70)
    
    student_number = "8931914"
    key = b'0123456789ABCDEF'
    iv = b'INITVECT'
    plaintext = student_number.encode()
    
    # Time 2-bit CFB
    start = time.perf_counter()
    for _ in range(1000):
        tea_cfb_2bit_encrypt(plaintext, key, iv)
    end = time.perf_counter()
    avg_time_2bit = (end - start) / 1000
    
    # Time 3-bit CFB
    start = time.perf_counter()
    for _ in range(1000):
        tea_cfb_3bit_encrypt(plaintext, key, iv)
    end = time.perf_counter()
    avg_time_3bit = (end - start) / 1000
    
    print(f"Average 2-bit CFB time: {avg_time_2bit:.8f} seconds")
    print(f"Average 3-bit CFB time: {avg_time_3bit:.8f} seconds")
    
    if avg_time_3bit < avg_time_2bit:
        print(f"\n✓ 3-bit CFB is consistently faster by {(avg_time_2bit - avg_time_3bit):.8f} seconds per encryption")
    else:
        print(f"\n✗ Unexpected: 2-bit CFB is faster")
    
    return avg_time_2bit, avg_time_3bit

if __name__ == "__main__":
    results = encrypt_and_compare()
    print("\n" + "-" * 70)
    
    # Optional: Run performance test
    run_perf_test = input("\nRun performance test (1000 iterations)? (y/n): ")
    if run_perf_test.lower() == 'y':
        avg_2bit, avg_3bit = performance_test()
        
        # Save results to file
        with open('task5_results.txt', 'w') as f:
            f.write("TASK 5 RESULTS\n")
            f.write("=" * 50 + "\n")
            f.write(f"Student Number: {results['student_number']}\n")
            f.write(f"Sum of digits: {results['digits_sum']}\n")
            f.write(f"c = {results['digits_sum']} mod 5 = {results['c']}\n")
            f.write(f"\n2-bit CFB Ciphertext: {results['ciphertext_2bit']}\n")
            f.write(f"3-bit CFB Ciphertext: {results['ciphertext_3bit']}\n")
            f.write(f"\nSingle-run Times:\n")
            f.write(f"  2-bit CFB: {results['time_2bit']:.8f} seconds\n")
            f.write(f"  3-bit CFB: {results['time_3bit']:.8f} seconds\n")
            f.write(f"\nPerformance Test (1000 iterations):\n")
            f.write(f"  Avg 2-bit CFB: {avg_2bit:.8f} seconds\n")
            f.write(f"  Avg 3-bit CFB: {avg_3bit:.8f} seconds\n")
        
        print("\nResults saved to 'task5_results.txt'")
    
    print("\n" + "=" * 70)
    print("Task Five completed successfully!")
    print("=" * 70)