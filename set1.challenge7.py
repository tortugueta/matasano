# -*- coding: utf-8 -*-

# The matasano cryptography challeges
# Set 1 / Challenge 7
# AES in ECB mode

# Imports
import sys
sys.path.append("/home/joan/Programming/matasano/")
import matasanolib
import numpy as np
from Crypto.Cipher import AES

key = "YELLOW SUBMARINE" # 16-character key (128 bits)

# Read encrypted file
filepath = "/home/joan/Programming/matasano/" + \
	"set1.challenge7.encrypted.txt"
filehandler = open(filepath, "r")
b64str = ""
for line in filehandler:
	b64str += line.strip()

# Convert b64 to ascii, because our function expects an ascii string. Remember
# that every four b64 characters correspond to three ascii characters. I
# assume that the padding is correct (we can check that the length is divisible
# by 4)
blocklst = [b64str[i:i+4] for i in range(0, len(b64str), 4)]
blocklst = [matasanolib.b64toint(block) for block in blocklst]
blocklst = ['%06x' % block for block in blocklst]
asciistr = ""
for block in blocklst:
	asciistr += chr(int(block[0:2], base=16)) + \
		chr(int(block[2:4], base=16)) + \
		chr(int(block[4:6], base=16))
# print(asciistr)

# Generate the cipher
cipher = AES.new(key, AES.MODE_ECB)

# Decrypt
plaintxt = cipher.decrypt(asciistr)
print(plaintxt)