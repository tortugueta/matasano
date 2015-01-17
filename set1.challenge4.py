# -*- coding: utf-8 -*-

# The matasano crypto challenges
# Set 1 / Challenge 4
# Detect single-character XOR

import sys
sys.path.append('/home/joan/Programming/the matasano cryptography challenges/')
import matasanolib

# Read the messages list from a file
file = open('/home/joan/Programming/the matasano cryptography challenges/set1.challenge4.keylist', 'r')
messagelist = []
for message in file:
	messagelist.append(message.strip())

# Try one-char decryption in each and every one of the messages
claus = range(0x20, 0x7e + 1)
for (index, message) in enumerate(messagelist):
	# Divide the messages in characters
	message = [message[i:i+2] for i in range(0, len(message), 2)]
	message = [int(character, base=16) for character in message]

	# Decrypt with each key
	for key in claus:
		decrypted = [character ^ key for character in message]
		decryptedtxt = ""
		for character in decrypted:
			decryptedtxt += chr(character)

	# Filter according to fraction of characters being actual letters
		if matasanolib.filterstring_alpha(decryptedtxt):
			print(index, chr(key), decryptedtxt)

# We should get a reduced list of possible candidates from which to manually
# pick the correct one
