# -*- coding: utf-8 -*-

# The matasano cryptography challeges
# Set 2 / Challenge 11
# An ECB/CBC detection oracle

# Imports
import matasanolib
import numpy.random as rnd
from Crypto.Cipher import AES

# Select an appropriate message that will give away ECB mode
blocksize = 16
numblocks = 4
msg = "a" * numblocks * blocksize

# Encrypt the message with the random blackbox
ciphertext = matasanolib.blackbox_ecb_cbc_128(msg)

# Programatically check that there are equal blocks. The 2nd, 3rd and 4th
# blocks should be the same
hexstring = ""
for character in ciphertext:
	hexstring = "".join([hexstring, "%02x" % ord(character)])

for i in xrange(0, len(hexstring), blocksize*2):
	print(hexstring[i:i+blocksize*2])

block2 = hexstring[blocksize*2:blocksize*4]
block3 = hexstring[blocksize*4:blocksize*6]
block4 = hexstring[blocksize*6:blocksize*8]
if block2 == block3 == block4:
	print("ECB mode")
else:
	print("CBC mode")
