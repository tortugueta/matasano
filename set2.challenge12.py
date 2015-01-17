# -*- coding: utf-8 -*-

# The matasano cryptography challeges
# Set 2 / Challenge 12
# Byte-at-a-time ECB decryption (Simple)

# Imports
from ipdb import set_trace
import matasanolib
import numpy.random as rnd
from Crypto.Cipher import AES

# Fix the blocksize and generate a random key
blocksize = 16
key = matasanolib.random_key(blocksize)

# Define the oracle function
def oracle(string):
	"""
	This oracle function receives a string, appends another (unknown) string to
	the input string and encrypts it with an (unknown) key. For the purposes of
	this exercise, we want the key to be random, but also to be always the same
	in all the calls to the function during a given execution. Therefore, the
	random key is generated outside the oracle function and read by it as a
	global variable. The unknown appended string is what the attacker want to
	find out by feeding inputs to the oracle and examining the output.

	Parameters
	----------
	string : a Python string
		The string that will prepend the unknown string

	Return
	------
	The ciphertext corresponding to the concatenation of the input string and
	an unknown string
	"""

	# Set the unknown string. This is what the attacker wants to decrypt. Bear
	# in mind that the attacker can only call the oracle, with a certain input
	# and examine its encrypted output, but cannot see inside the code itself.
	unknown = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg" + \
	"aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq" + \
	"dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
	unknown = matasanolib.b64toascii(unknown)

	# Append the unknown to the input string
	plaintext = matasanolib.pkcs7padding("".join([string, unknown]), blocksize)

	# Encrypt
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.encrypt(plaintext)


### Find if the encryption is ECB and its blocksize ###
repetitions = 2
for candidatesize in xrange(1, 33):
	# Choose a buffer and encrypt
	bufferstr = "A" * candidatesize * repetitions
	ciphertext = oracle(bufferstr)

	# The first "repetitions" blocks should be equal if the blocksize is correct
	block1 = ciphertext[0:blocksize]
	block2 = ciphertext[blocksize:blocksize*2]
	if block1 == block2:
		print("ECB with block size = %d" % candidatesize)
		foundsize = candidatesize
		break

# Now we choose an inputstr which is a repeated character one character short
# of the block size. That means that the last character of the first block will
# be the first character of the unknown string. We create a dictionary with the
# 255 possible results for the first block, and find what is the first
# character of the unknown string. Let's assume it'a a '1'. Then, to find the
# second character, we create a dictionary with a block that is a repeated
# character two bytes short of the blocksize, plus the known first character of
# the unknown string, plus the 255 possibilities for the second character, and
# so on. The thing is, if we use a single block, we will be able to decrypt
# only the first block of the unknown string. Therefore, we do the same but
# with a controlled block that is as long as the unknown string.

# First we need to find out the length of the appended string
initial_guess = len(oracle(""))
for i in xrange(1, blocksize):
	current_length = len(oracle("a" * i))
	if current_length > initial_guess:
		offset = i
		break
length = initial_guess - offset

# Decrypt one byte at a time
evenlength = initial_guess
decrypted = ""
for position in xrange(length):
	# Build the dictionary for this round
	dictionary = {}
	bufferstr = "a" * (evenlength - (len(decrypted) + 1))
	known = "".join([bufferstr, decrypted])
	for lastchar in xrange(256):
		entry = "".join([known, chr(lastchar)])
		encrypted_entry = oracle(entry)
		dictionary[encrypted_entry[:evenlength]] = entry

	# Now encrypt without "lastchar", so that "lastchar" will be occupied by a
	# character from the unknown string that has been flushed left
	ciphertext = oracle(bufferstr)
	plaintext = dictionary[ciphertext[:evenlength]]
	newchar = plaintext[evenlength-1]
	decrypted = "".join([decrypted, newchar])
	print(decrypted)
	print("")

