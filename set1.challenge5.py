# -*- coding: utf-8 -*-

# The matasano crypto challenges
# Set 1 / Challenge 5
# Implement repeating-key XOR

import sys
sys.path.append('/home/joan/Programming/matasano/')
import matasanolib

msg = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = "ICE"
keylength = len(key)

# To encrypt the message using the repetition of ICE as a key, we xor(B, I),
# xor(u, C), xor(r, E), xor(n, I)... Given a character of the message, in order
# to know which character of the key corresponds to it, we calculate the
# equivalence class module "length of the key" to which the index of the
# character belongs

enclist = []
for (index, character) in enumerate(msg):
	enclist.append(ord(character) ^ ord(key[index % keylength]))

# Once I have a list with each character encrypted, I can print it as a hex
# string or ascii string
#
# IMPORTANT!!! When we build the hex string, mind the following: each character
# takes 8 bits, which is two hex characters. If the 4-bit block to the left (the
# leftmost character of those two hex characters) is 0, by default this 0 will
# not be printed in the hex representation. If we are printing an indivdual
# character this is acceptable, but when we are concatenating the string of
# characters we need that zero to the left, because it matters when we have the
# whole string together.
#
# So when we want to print a character in its hex representation, it's important
# to use the %02x code to make sure that the printed representation will use
# two digits, padding with a zero to left in case that the representation needs
# only one digit.
hexstring = ''
asciistring = ''
for character in enclist:
	hexstring += '%02x' % character
	asciistring += chr(character)

print(hexstring)
print(asciistring)

# Also bear in mind that, once encrypted, some of the characters are not
# printable in ascii, which means that we would lose those bytes after printing
# to screen because they just would not be printed. To make printed versions of
# the encrypted messages it's best to use a hex or base64 representation.
