# -*- coding: utf-8 -*-

# The matasano crypto challenges
# Set1 / Challenge 2
# Fixed XOR

# Input strings stored as integers
hex1 = 0x1c0111001f010100061a024b53535009181c
hex2 = 0x686974207468652062756c6c277320657965

# XOR the binary representations of those integers
xor = hex1 ^ hex2

# Now interpret the resulting integer as a hex
print '%x' % (xor)
