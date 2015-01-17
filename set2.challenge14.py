# -*- coding: utf-8 -*-

# The matasano cryptography challeges
# Set 2 / Challenge 14
# Byte-at-a-time ECB decryption (harder)

# Imports
from ipdb import set_trace
import matasanolib
import numpy.random as rnd
from Crypto.Cipher import AES

blocksize = 16

# Generate a random key and the cipher
key = matasanolib.random_key(blocksize)

# Generate a random prefix
maxlength = 256 # bytes
prefix_length = rnd.randint(maxlength)
prefix = ""
for i in xrange(prefix_length):
	prefix = "".join([prefix, chr(rnd.randint(256))])

# Define the oracle function
def oracle(string):
	"""
	This oracle function receives a string, appends another (unknown) string to
	the input string and prepends a yet another (unknown) string, and finally
	encrypts it with an (unknown) key. For the purposes of this exercise, we
	want the key to be random, but also to be always the same in all the calls
	to the function during a given execution, and the same for the prepended
	string. Therefore, the random key and random pre-string are generated
	outside the oracle function and read by it as a	global variable. The
	unknown appended string is what the attacker wants to find out by feeding
	different inputs to the oracle and examining the output.

	Parameters
	----------
	string : a Python string
		The string that will be inserted between the unknown strings.

	Return
	------
	The ciphertext corresponding to the concatenation of the random pre-string,
	the input string and the unknown string
	"""

	# Set the unknown string. This is what the attacker wants to decrypt. Bear
	# in mind that the attacker can only call the oracle with a certain input
	# and examine its encrypted output, but cannot see inside the code itself.
	unknown = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg" + \
	"aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq" + \
	"dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
	unknown = matasanolib.b64toascii(unknown)

	# Concatenate all the strings
	plaintext = matasanolib.pkcs7padding("".join([prefix, string, unknown]),
		blocksize)

	# Encrypt
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.encrypt(plaintext)


# First we need to find the length of the random prefix. We assume that we
# already have found out that the block size is 16 bytes and the mode of
# operation is ECB (this can be done as in challege 12.
# To find out the length of the random prefix, we generate three blocks of "a".
# That will give us the following, in general:
#
# ****************|***aaaaaaaaaaaaa|aaaaaaaaaaaaaaaa|aaaaaaaaaaaaaaaa|aaauuuuuuuuuuuuu|uuuuuuuuuuuuuuuu|
#
# Here, the * are the unknown prefix, the 'a' our three controlled blocks, and
# the 'u' the unknown message. If the prefix occupies a whole number of blocks,
# we would see three equal blocks in the ciphertext corresponding to our 'a's,
# and we can clearly identify where the prefix ends and therefore its length.
# In general it will end at half a block. What we do is add 'a's to our
# controlled input until we get three full equal blocks. In the example above
# this will happen when we add 13 'a's. That means that the prefix ends 13
# bytes before the beginning of the first of our equal blocks.

# Find length of the random prefix
controlled = "a" * 3 * blocksize
ciphertext = oracle(controlled)

ciphertext_bl = matasanolib.BlockString(ciphertext, blocksize)

for index in xrange(1, ciphertext_bl.numblocks()):
	if ciphertext_bl[index] == ciphertext_bl[index-1]:
		first_index = index - 1
		break

for i in xrange(blocksize):
	controlled = "a" * (3 * blocksize + i)
	ciphertext = oracle(controlled)
	ciphertext_bl = matasanolib.BlockString(ciphertext, blocksize)
	if ciphertext_bl[first_index + 2] == ciphertext_bl[first_index]:
		offset = i
		break

prefix_length = first_index * blocksize - offset

# Find length of the unknown
initial_guess = len(oracle(""))
for i in xrange(1, blocksize):
	current_length = len(oracle("a" * i))
	if current_length > initial_guess:
		padding = i
		break

unknown_length = initial_guess - prefix_length - padding

# Operate as in challenge 12 to decrypt one byte at a time

# How many characters do we need to make the prefix fill a whole number of
# blocks
controlled_length = unknown_length + \
	blocksize - ((prefix_length + unknown_length) % blocksize)

decrypted = ""
for position in xrange(unknown_length):
	# Build the dictionary for this round
	dictionary = {}
	controlled = "a" * (controlled_length - (len(decrypted) + 1))
	known = "".join([controlled, decrypted])
	for lastchar in xrange(256):
		entry = "".join([known, chr(lastchar)])
		encrypted_entry = oracle(entry)
		dictionary[encrypted_entry[:prefix_length + len(known) + 1]] = entry

	# Now encrypt without "lastchar", so that "lastchar" will be occupied by a
	# character from the unknown string that has been flushed left
	ciphertext = oracle(controlled)
	plaintext = dictionary[ciphertext[:prefix_length + len(known) + 1]]
	newchar = plaintext[-1]
	decrypted = "".join([decrypted, newchar])
	print(decrypted)
	print("")


#set_trace()