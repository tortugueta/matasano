# -*- coding: utf-8 -*-

# The matasano crypto challenges
# Set 1 / Challenge 1
# Convert hex to base64

import string

# Save the hex string as an integer
integer = 0x49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d

# Every time integer is divided by 64, the remainder is a base64 digit (starting
# in the last). We interpret each reminder, a number in the range [0, 63], using
# the base64 alphabet

alphabet = string.uppercase + string.lowercase + string.digits + '+' + '/'

base64string = ''
while integer >= 1:
	character = alphabet[integer % 64]
	base64string = ''.join([character, base64string])
	integer = integer/64 # Integer division

print(base64string)
