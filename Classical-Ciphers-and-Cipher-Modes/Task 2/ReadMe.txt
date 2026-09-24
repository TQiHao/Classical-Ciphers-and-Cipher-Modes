Task 2:

1. OPEN COMMAND PROMPT (CMD)
   - Press Windows + R
   - Type "cmd"
   - Press Enter

2. NAVIGATE TO THE FOLDER
   cd "C:\Users\Qi Hao\OneDrive\Desktop\School Assignment\CSCI361\Assignment 1\Task 2"

3. CHECK FILES EXIST
   dir
   You should see: "cipher.py" (the program) and your text files

4. RUN THE PROGRAM

   TO ENCRYPT:
   python cipher.py <KEYWORD> encrypt <INPUT_FILE> <OUTPUT_FILE>

   TO DECRYPT:
   python cipher.py <KEYWORD> decrypt <INPUT_FILE> <OUTPUT_FILE>

   Example 1: Encrypt a file named "message.txt"
   python cipher.py STRAWBERRY encrypt message.txt secret.txt



Run these commands to test the program:

1. Create a test file:
   echo "HELLO WORLD ABC XYZ 123 !@#" > test.txt

2. Encrypt it:
   python cipher.py STRAWBERRY encrypt test.txt test_enc.txt

3. View encrypted result:
   type test_enc.txt

4. Decrypt it:
   python cipher.py STRAWBERRY decrypt test_enc.txt test_dec.txt

5. Verify decryption:
   type test_dec.txt


Keyword Example: "STRAWBERRY"

Step 1: Remove duplicate letters → "STRAWBEY"
Step 2: Add remaining alphabet letters in reverse (Z→A) → "STRAWBEYZVXUQPONMLKJIHGFDC"

Mapping:
Original:  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
Key:       S T R A W B E Y Z X V U Q P O N M L K J I H G F D C

Example:
HELLO → EYQQJ (encryption)
EYQQJ → HELLO (decryption)