# -*- coding: utf-8 -*-

# The matasano cryptography challeges
# Set 3 / Challenge 18
# Implement CTR, the stream cipher mode

# Imports
import matasanolib
from Crypto.Cipher import AES

def encrypt_aes_ctr_128(plaintext, key):
	"""
	Encrypt the plaintext using AES CTR mode. The implementation of the CTR
	streaming is "manual". Each block of the stream is encrypted using AES_ECB.
	The format of the nonce is:

	0 0 0 0 0 0 0 | 0 0 0 0 0 0 0 0

	The first 8 bytes are always zero. The second block of 8 bytes is the
	counter, +1 for each block, in little endian mode, that is, for the first
	three blocks the nonce would be:

	block 0: 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
	block 1: 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
	block 2: 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0

	and so on.

	Parameters
	----------
	plaintext : a Python string
		The plaintext to be encrypted
	key : a Python string
		A 16-character string that will be used as the key for the AES_ECB
		encryption of the counter

	Returns
	-------
	A Python string with the ciphertext
	"""

	# We will work in blocks
	blocksize = 16
	plaintext = matasanolib.BlockString(plaintext, blocksize)

	# Set the nonce and the initial value of the counter
	nonce = "\x00" * 8
	counter = "\x00" * 8

	# Encrypt block by block
	cipher = AES.new(key, mode=AES.MODE_ECB)
	ciphertext = ""
	for block in plaintext:
		# Encrypt the nonce + counter
		stream = "".join([nonce, counter])
		cipherstream = cipher.encrypt(stream)

		# XOR the encrypted stream with the plaintext block
		for i in xrange(len(block)):
			cipherchar = chr(ord(cipherstream[i]) ^ ord(block[i]))
			ciphertext = "".join([ciphertext, cipherchar])

		# Increase the counter
		counter = [ord(char) for char in counter]
		for i in xrange(len(counter)):
			if counter[i] < 255:
				counter[i] += 1
				break
			elif counter[i] == 255:
				counter[i] = 0
			else:
				print("Something terrible happened")
				raise ValueError
		counter = [chr(digit) for digit in counter]
		counter = "".join(counter)

	return ciphertext

def decrypt_aes_ctr_128(ciphertext, key):
	"""
	Decrypt the ciphertext using AES CTR mode. The implementation of the CTR
	streaming is "manual". Each block of the stream is encrypted using AES_ECB.

	The format of the nonce is:

	0 0 0 0 0 0 0 | 0 0 0 0 0 0 0 0

	The first 8 bytes are always zero. The second block of 8 bytes is the
	counter, +1 for each block, in little endian mode, that is, for the first
	three blocks the nonce would be:

	block 0: 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
	block 1: 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
	block 2: 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0

	and so on.

	Note that, due to the particular way in which CTR works, there is no such
	thing as "decryption", and in fact this function is exactly the same as
	encrypt_aes_ctr_128. Here we are just calling the encryption function using
	the ciphertext as the plaintext. In CTR we always encrypt the counter with
	the key. If we XOR that with the plaintext, we get the ciphertext. If
	instead we XOR that with the ciphertext, we obtain the plaintext.

	Parameters
	----------
	ciphertext : a Python string
		The ciphertext to be decrypted
	key : a Python string
		A 16-character string that will be used as the key for the AES_ECB
		encryption of the counter

	Returns
	-------
	A Python string with the plaintext

	"""

	return encrypt_aes_ctr_128(ciphertext, key)


### Solution of the challenge ###

key = "YELLOW SUBMARINE"
b64ciphertext = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/" + \
	"kXX0KSvoOLSFQ=="
ciphertext = matasanolib.b64toascii(b64ciphertext)

decrypted = decrypt_aes_ctr_128(ciphertext, key)
print decrypted