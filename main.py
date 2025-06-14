# Import tools from the cryptography library for real encryption
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64  #libraries


# --------------------------
# PART 1: Caesar Cipher Decryption
# --------------------------

# This function will try all 26 Caesar cipher shifts
# It will help me guess the original message

def caesar_brute_force(ciphertext):
    for shift in range(26):  # Try every shift from 0 to 25
        result = ""  # Start with an empty string for the result

        # For me to be able to do math operations on letters I need to convert them into digits.
        # Therefore, before I continue I wanted to remind myself that In ASCII encoding:
        # 65 = 'A' (uppercase A)
        # 97 = 'a' (lowercase a)
        # These are important reference points in ASCII:
        # Uppercase letters A-Z are ASCII values 65-90 - so total  of 26 lower case letters in English alphabet
        # Lowercase letters a-z are ASCII values 97-122 - so total of 26 upper case letters in English alphabet

        for char in ciphertext:  # Go through each character in the message
            if char.isupper():  # If the letter is a capital letter
                # Convert character to number (A = 65), subtract the shift, use module operation to wrap, then back to letter
                result += chr((ord(char) - shift - 65) % 26 + 65)
            elif char.islower():  # If the letter is a small letter
                result += chr((ord(char) - shift - 97) % 26 + 97)
            else:
                result += char  # If it's not a letter (like space or period), keep it the same

        print("Shift", shift, ":", result)  # Show the result for this shift


# Encrypted message to test
cipher = "Hvs Eiwqy Pfckb Tcl Xiadg Cjsf Hvs Zonm Rcu."

# Run the function to try all Caesar cipher keys
caesar_brute_force(cipher)

# --------------------------
# PART 2: Caesar Cipher on one word (mznxpz)
# --------------------------

# This function will try to decrypt one word using Caesar cipher
# I will use it to find the hidden word in 'mznxpz'

print()
print("Part 2")  # for output clarity.
print()


def caesar_brute_word(word):
    for shift in range(26):  # Try all 26 possible shifts
        result = ""  # Start with an empty string

        for char in word:  # Go through each letter in the word
            result += chr((ord(char) - shift - 97) % 26 + 97)  # Shift the letter back and wrap if needed

        print("Shift", shift, ":", result)  # Show the result for this shift


cipher_word = "mznxpz"  # The encrypted word
caesar_brute_word(cipher_word)  # Shift 21 - rescue. rescue and secure are anagrams of each other so
# Secure must be answered to Part 2 of this second exercise.


# --------------------------
# PART 3: XOR Decryption with Base64
# --------------------------

print()
print("Part 3: XOR Decryption")
print()

# The passphrase I recovered from Part 2 (anagram of "rescue")
passphrase = "secure"

# The base64 encoded ciphertext
base64_ciphertext = "Jw0KBlIMAEUXHRdFKyoxVRENEgkPEBwCFkQ="

# Step 1: Decode the base64 string to get raw bytes
raw_ciphertext = base64.b64decode(base64_ciphertext)
print("Base64 decoded bytes:", raw_ciphertext)


# Step 2: XOR decrypt using the passphrase
def xor_decrypt(ciphertext_bytes, key):
    decrypted_text = ""  # Empty string to build our result

    # Go through each byte in the encrypted data
    for i in range(len(ciphertext_bytes)):
        # Find which letter from our key to use (repeat key if needed)
        key_position = i % len(key)  # This wraps around when - reach the end of the key
        key_char = key[key_position]  # Get the character from the key

        # Convert key character to number and XOR with cipher byte
        key_number = ord(key_char)  # Turn letter into ASCII number
        cipher_byte = ciphertext_bytes[i]  # Get the encrypted byte

        # Do the XOR operation to decrypt
        decrypted_byte = cipher_byte ^ key_number

        # Turn the decrypted number back into a letter
        decrypted_char = chr(decrypted_byte)
        decrypted_text = decrypted_text + decrypted_char  # Add to our result

    return decrypted_text


# Do the XOR decryption
decrypted_message = xor_decrypt(raw_ciphertext, passphrase)
print("Decrypted message: " + decrypted_message)

# Show the XOR process step by step so you can see what happens
print()
print("XOR process:")
for i in range(len(raw_ciphertext)):
    key_position = i % len(passphrase)  # Which key character to use
    key_char = passphrase[key_position]  # Get that character
    key_number = ord(key_char)  # Turn it into a number
    cipher_byte = raw_ciphertext[i]  # Get the encrypted byte
    decrypted_byte = cipher_byte ^ key_number  # XOR them together

    # Try to make a readable character (if it's not readable, show ?)
    if decrypted_byte >= 32 and decrypted_byte <= 126:
        decrypted_char = chr(decrypted_byte)
    else:
        decrypted_char = '?'

    print("Position " + str(i) + ": " + str(cipher_byte) + " XOR " + str(key_number) + " (" + key_char + ") = " + str(
        decrypted_byte) + " ('" + decrypted_char + "')")

# --------------------------
# SUMMARY / DISCUSSION
# --------------------------
# The Quick Brown Fox Jumps Over The Lazy Dog. This is the solution for the first task at shift 14.
# This means that for each letter needs to go backward by 14 letters to get to the correct letter.
# For example, from H to T. There are 26 letters total in the alphabet. 26-14 = 12. Therefore,
# the original encryption used shift 12 --> from T to H.

# Why is Caesar cipher not safe?
# Because it has only 25 possible keys, anyone can guess the correct one very fast.
# As we can see a modern computer can try all 25 keys in less than a second.

# Where might it still be used?
#  Old computer systems that gave weak and old chips that can only handle simple calculations.
#  Caesar cipher is also excellent way to introduce students to basic cryptographic concepts and algorithms and then
# build on top of that more advanced concepts for example - AES.

# Final decrypted message from XOR:
print()
print("=> Final Answer: '" + decrypted_message + "'")