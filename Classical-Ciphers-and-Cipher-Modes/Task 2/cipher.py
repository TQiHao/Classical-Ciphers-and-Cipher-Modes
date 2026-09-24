import sys
import os

def generate_key(keyword):
    # Generate the substitution key from a keyword.
    seen = set()
    key_chars = []
    
    # Add keyword letters (uppercase)
    for char in keyword.upper():
        if 'A' <= char <= 'Z' and char not in seen:
            key_chars.append(char)
            seen.add(char)
    
    # Append remaining letters in reverse order (Z to A)
    for char_code in range(ord('Z'), ord('A') - 1, -1):
        char = chr(char_code)
        if char not in seen:
            key_chars.append(char)
    
    return ''.join(key_chars)

def create_cipher_maps(keyword):
    # Create encryption and decryption dictionaries.
    key = generate_key(keyword)
    
    # Create encryption map (A->S, B->T, etc.)
    encrypt_map = {}
    decrypt_map = {}
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    for i in range(26):
        plain_char = alphabet[i]
        cipher_char = key[i]
        encrypt_map[plain_char] = cipher_char
        decrypt_map[cipher_char] = plain_char
    
    return encrypt_map, decrypt_map

def process_file(input_file, output_file, keyword, encrypt=True):
    # Process a file for encryption or decryption.
    try:
        encrypt_map, decrypt_map = create_cipher_maps(keyword)
        
        with open(input_file, 'r') as f_in:
            text = f_in.read()
        
        result = []
        
        for char in text:
            if 'A' <= char.upper() <= 'Z':
                upper_char = char.upper()
                if encrypt:
                    cipher_char = encrypt_map[upper_char]
                else:
                    cipher_char = decrypt_map[upper_char]
                
                result.append(cipher_char if char.isupper() else cipher_char.lower())
            else:
                result.append(char)
        
        with open(output_file, 'w') as f_out:
            f_out.write(''.join(result))
        
        return True
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    if len(sys.argv) != 5:
        print("Usage:")
        print("  python cipher.py <keyword> encrypt <input_file> <output_file>")
        print("  python cipher.py <keyword> decrypt <input_file> <output_file>")
        print("\nExample:")
        print("  python cipher.py STRAWBERRY encrypt message.txt encrypted.txt")
        print("  python cipher.py STRAWBERRY decrypt encrypted.txt decrypted.txt")
        return
    
    keyword = sys.argv[1]
    mode = sys.argv[2].lower()
    input_file = sys.argv[3]
    output_file = sys.argv[4]
    
    if mode not in ['encrypt', 'decrypt']:
        print("Error: Mode must be 'encrypt' or 'decrypt'")
        return
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        return
    
    if mode == 'encrypt':
        print(f"Encrypting '{input_file}' to '{output_file}'...")
        success = process_file(input_file, output_file, keyword, encrypt=True)
        if success:
            print("Encryption complete!")
            key = generate_key(keyword)
            print(f"Key alphabet: {key}")
    else:
        print(f"Decrypting '{input_file}' to '{output_file}'...")
        success = process_file(input_file, output_file, keyword, encrypt=False)
        if success:
            print("Decryption complete!")

if __name__ == "__main__":
    main()