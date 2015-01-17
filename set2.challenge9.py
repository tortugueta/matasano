# -*- coding: utf-8 -*-

# The matasano cryptography challeges
# Set 2 / Challenge 9
# Implement PKCS#7 padding

def pkcs7padding(string, blocksize):
	"""
	Adds pkcs#7 padding to a string.

	Parameters
	----------
	string : a Python string
		The string we want to pad
	blocksize : a Python integer
		The blocksize we want to apply to the string

	Return
	------
	A Python string padded to blocksize bytes
	"""

	# Check the input
	if type(string) == str:
		if type(blocksize) == int:
			pass
		else:
			print("The second argument must be an integer")
			raise ValueError
	else:
		print("The first argument must be a Python string")
		raise ValueError

	extrachars = len(string) % blocksize
	paddingnum = blocksize - extrachars
	paddingchar = chr(paddingnum)
	paddingstr = paddingchar * paddingnum
	paddedstr = "".join([string, paddingstr])

	return paddedstr


string = "YELLOW SUBMARINE"
padded = pkcs7padding(string, 20)

unpaddedstr = ""
for character in string:
	hexchar = '%02x' % ord(character)
	unpaddedstr = "".join([unpaddedstr, hexchar])

paddedstr = ""
for character in padded:
	hexchar = '%02x' % ord(character)
	paddedstr = "".join([paddedstr, hexchar])

print(unpaddedstr)
print(paddedstr)