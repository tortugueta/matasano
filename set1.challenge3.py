# -*- coding: utf-8 -*-

# The matasano crypto challenges
# Set 1 / Challenge 3
# Single-byte XOR cipher

import sys
sys.path.append('/home/joan/Programming/the matasano cryptography challenges/')
import matasanolib

# The string we have initially is the hex representation of a string of bits
# that has been encrypted XORing with a single ascii character, repeated as
# many times as necessary to match the length of the plaintext string. Remember
# that every 8-bit block (two hex digits) correspond to a single ascii character
cipherhex = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
cipherhex = [cipherhex[i:i+2] for i in range(0, len(cipherhex), 2)]
cipherint = [int(char, base=16) for char in cipherhex]
numchars = len(cipherhex)/2

# For each candidate charcter to be the key (take the list of printable
# characters of the ascii table and generate them directly as a hex literal),
# XOR it with each and every one of the characters in the ciphertext.
for key in range(0x20, 0x7e + 1):
	asciikey = chr(key)
	decipheredint = [character ^ key for character in cipherint]
	decipheredtext = ""
	for character in decipheredint:
		decipheredtext += chr(character)

	# Filter the sentence we get to eliminate those with many non-letter
	# characters
	if matasanolib.filterstring_alpha(decipheredtext):
		print(asciikey, decipheredtext)

# That should print a list of candidates short enough that we can manually
# select which one is the correct key.