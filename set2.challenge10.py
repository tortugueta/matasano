# -*- coding: utf-8 -*-

# The matasano cryptography challeges
# Set 2 / Challenge 10
# Implement CBC mode

filepath = "/home/joan/Programming/the matasano cryptography challenges/"

# Imports
import sys
sys.path.append(filepath)
import matasanolib
from Crypto.Cipher import AES

# Fix the blocksize, the key and the initialization vector
blocksize = 16
key = "YELLOW SUBMARINE"
iv = "\x00" * blocksize
msg = "hola-carambolab/hola-carambolab/nopadejada"
msg = matasanolib.pkcs7padding(msg, blocksize)

# Check that the sizes are good
if (len(key) != blocksize) or (len(iv) != blocksize):
	print("Key size does not match the intended block size")
	raise ValueError

# Generate the AES cipher for ECB mode
cipher = AES.new(key, AES.MODE_ECB)

# Begin the encryption process
ciphertext = ""

# Encrypt de first block
plaintext = msg[0:blocksize]
previous = iv
xored = matasanolib.encrypt_repeating(plaintext, previous)
ciphertextblock = cipher.encrypt(xored)
ciphertext = "".join([ciphertext, ciphertextblock])

# Encrypt the remainging blocks
for i in xrange(blocksize, len(msg), blocksize):
	plaintext = msg[i:i+blocksize]
	previous = ciphertextblock
	xored = matasanolib.encrypt_repeating(plaintext, previous)
	ciphertextblock = cipher.encrypt(xored)
	ciphertext = "".join([ciphertext, ciphertextblock])

# Encode in base 64 for pretty printing
ciphertext_b64 = matasanolib.asciitob64(ciphertext)

print(ciphertext)
print("")
print(ciphertext_b64)