# -*- coding: utf-8 -*-

# Imports
import string
import numpy.random as rnd
from Crypto.Cipher import AES


# Define the base 64 alphabet, that we will use in a couple of functions. The
# definition comes from Wikipedia
b64alphabet = string.uppercase + string.lowercase + string.digits + '+' + '/'

# TODO Afegir test per la classe BlockString
class BlockString():
	"""
	Class used to represent strings that are to be understood as a sequence of
	blocks of a certain number of characters.
	"""

	def __init__(self, string, blocksize):
		"""
		Initializes de class with a certain blocksize. The blocksize can be
		changed later with the setBlockSize method

		Parameters
		----------
		string : a Python string
			The string that we want to convert to a BlockString
		blocksize : an integer
			The number of characters in each block
		"""

		self.__blocksize = blocksize
		self.__string = string
		self.__length = len(string)
		self.__numblocks = 0
		self.__calculateNumBlocks()

	def __calculateNumBlocks(self):
		"""
		Calculates the number of blocks in the string
		"""

		if self.__length % self.__blocksize == 0:
			self.__numblocks = self.__length / self.__blocksize
		else:
			self.__numblocks = (self.__length / self.__blocksize) + 1 # Divisó
																	  # entera

	def blockSize(self):
		"""
		Return the blocksize instance variable
		"""

		return self.__blocksize

	def setBlockSize(self, blocksize):
		"""
		Set a new block size (the number of blocks will be recalculated)

		Parameters
		----------
		blocksize : integer
			The new block size
		"""

		self.__blocksize = blocksize
		self.__calculateNumBlocks()

	def string(self):
		"""
		Return the string
		"""

		return self.__string

	def setString(self, string):
		"""
		Set the string. The length and number of blocks will be recalculated

		Parameters
		----------
		string : a Python string
			The new string
		"""

		self.__string = string
		self.__length = len(string)
		self.__calculateNumBlocks()

	def numblocks(self):
		"""
		Return the number of blocks
		"""

		return self.__numblocks

	def length(self):
		"""
		Return the string length
		"""

		return self.__length

	def __repr__(self):
		"""
		Each block of the string should be printed in a new line. Each line
		should be preceded by the block number.
		"""

		strrep = ""
		for (i, block) in enumerate(self):
			strrep = "".join([strrep, "%d\t%s\n" % (i, block)])

		return strrep

	def __getitem__(self, index):
		"""
		What should be returned when we index the blockstring
		"""

		if index >= self.__numblocks:
			raise IndexError
		else:
			return \
				self.__string[index*self.__blocksize:(index+1)*self.__blocksize]

	def __iter__(self):
		"""
		How the iteration process should behave
		"""

		for i in xrange(self.__numblocks):
			yield self[i]


# TODO Add tests
def strtohex(string):
	"""
	Convert a Python string to its hexadecimal representation

	Parameters
	----------
	string : a Python string
		The string we want to print in hexadecimal representation

	Returns
	-------
	A Python string with the hexadecimal representation of the input string
	"""

	hexstring = ""
	for char in string:
		hexstring = "".join([hexstring, "%02x" % ord(char)])

	return hexstring


def inttob64(integer):
	"""
	Calculate the base 64 representation of an integer.

	Parameters
	----------
	integer : a Python integer
		The integer we want to represent in base 64

	Return
	------
	A string containing the input integer in base 64 representation
	"""

	# Check for correct input
	if type(integer) == int:
		pass
	else:
		print("Input must be an integer")
		raise ValueError

	# Each time we divide by 64, the remainder of the division is the last digit
	# of the representation in base 64. Each of those remainders, in the range
	# [0, 63] gets assigned a symbol in the base 64 alphabet.
	base64string = ""
	if integer == 0:
		base64string = "A"
	else:
		while integer >= 1:
			character = b64alphabet[integer % 64]
			base64string = "".join([character, base64string])
			integer = integer/64 # Integer division (rounds to the lower int)
								 # This may change in Python 3
	return base64string


def b64toint(b64str):
	"""
	Convert the base64 string representation of an integer to the integer it
	represents.

	Parameters
	----------
	b64str : a Python string
		The base 64 representation of an integer

	Return
	------
	The integer represented by the input string
	"""

	# Check that the input is a Python string
	if type(b64str) == str:
		pass
	else:
		print("Input must be Python string")
		raise ValueError

	# Reverse the string so that the digit corresponding to 64^i is in index i
	# of the string
	b64str = b64str[::-1]

	# During the process, check that each character is a valid base 64 symbol
	sum = 0
	for (power, digit) in enumerate(b64str):
		if digit not in b64alphabet:
			print("Input is not a valid base 64 representation")
			raise ValueError
		else:
			sum += b64alphabet.find(digit) * 64**power

	return sum


def asciitob64(asciistr):
	"""
	Converts an ascii string to base 64 representation. 4 base 64 characters
	are assigned to each 3 ascii characters. The usual padding with '=' is used
	at the end of the string in case its length is not a multiple of 3 bytes.

	Parameters
	----------
	asciistr : an Python string
		The ascii string we want to encode as base 64

	Return
	------
	A Python string with the base 64 representation of the original string
	"""

	# Check that the input is a Python string
	if type(asciistr) == str:
		pass
	else:
		print("Input must be a Python string")
		raise ValueError

	# Add the necessary padding
	remainder = len(asciistr) % 3
	if remainder == 0:
		padding = 0
	else:
		padding = 3 - remainder
	asciistr = "".join([asciistr, chr(0) * padding])

	# Take sequentially blocks of three characters from the ascii string and
	# convert them to base 64. We treat the last block of three differently
	# because of the padding.
	b64str = ""
	for i in xrange(0, len(asciistr) - 3, 3):
		h1 = "%02x" % ord(asciistr[i])
		h2 = "%02x" % ord(asciistr[i+1])
		h3 = "%02x" % ord(asciistr[i+2])
		hexblock = "".join([h1, h2, h3])
		integer = int(hexblock, base=16)
		b64block = inttob64(integer)
		b64str = "".join([b64str, b64block])

	# For the last block:
	h1 = "%02x" % ord(asciistr[-3])
	h2 = "%02x" % ord(asciistr[-2])
	h3 = "%02x" % ord(asciistr[-1])
	hexblock = "".join([h1, h2, h3])
	integer = int(hexblock, base=16)
	tmpblock = inttob64(integer)
	if padding == 0:
		b64block = tmpblock
	elif padding == 1:
		b64block = "".join([tmpblock[0], tmpblock[1], tmpblock[2], "="])
	elif padding == 2:
		b64block = "".join([tmpblock[0], tmpblock[1], "=="])
	b64str = "".join([b64str, b64block])

	return b64str


def b64toascii(b64str):
	"""
	Converts a string with a base 64 representation to its ascii
	encoding. 3 ascii characters are assigned to each 4 base 64 characters. The
	usual padding with '=' is expected so that the string is a length multiple
	of 3.

	Parameters
	----------
	b64str : an Python string
		A base 64-encoded string

	Return
	------
	An Python string
	"""

	# Check that the input is correct
	if type(b64str) == str:
		pass
	else:
		print("Input must be a Python string")
		raise ValueError

	if len(b64str) % 4 == 0:
		pass
	else:
		print("Input string not padded correctly")
		raise ValueError

	# Take sequentially blocks of 4 characters from the base 64 string and
	# convert them to ascii. We treat the last block differently because of the
	# padding
	asciistr = ""
	for i in xrange(0, len(b64str) - 4, 4):
		newblock = b64str[i:i+4]
		for character in newblock:
			if character not in b64alphabet:
				print("Input is not a valid base 64 expression")
				raise ValueError

		integer = b64toint(newblock)
		hexblock = "%06x" % integer
		char1 = chr(int(hexblock[0:2], base=16))
		char2 = chr(int(hexblock[2:4], base=16))
		char3 = chr(int(hexblock[4:6], base=16))
		asciistr = "".join([asciistr, char1, char2, char3])

	# For the last block
	lastblock = b64str[-4:]
	if lastblock[3] == "=":
		if lastblock[2] == "=":
			# Two characters of padding: one ascii character at the output
			for char in lastblock[0:2]:
				if char not in b64alphabet:
					print("Input is not a valid base 64 expression")
					raise ValueError

			lastblock = "".join([lastblock[0:2], "AA"])
			integer = b64toint(lastblock)
			hexblock = "%06x" % integer
			char1 = chr(int(hexblock[0:2], base=16))
			char2 = ""
			char3 = ""
		else:
			# One character of padding: two ascii characters at the output
			for char in lastblock[0:3]:
				if char not in b64alphabet:
					print("Input is not a valid base 64 expression")
					raise ValueError

			lastblock = "".join([lastblock[0:3], "A"])
			integer = b64toint(lastblock)
			hexblock = "%06x" % integer
			char1 = chr(int(hexblock[0:2], base=16))
			char2 = chr(int(hexblock[2:4], base=16))
			char3 = ""
	else:
		# No padding: three ascii characters at the output
		for char in lastblock:
			if char not in b64alphabet:
				print("Input is not a valid base 64 expression")
				raise ValueError

		integer = b64toint(lastblock)
		hexblock = "%06x" % integer
		char1 = chr(int(hexblock[0:2], base=16))
		char2 = chr(int(hexblock[2:4], base=16))
		char3 = chr(int(hexblock[4:6], base=16))

	asciistr = "".join([asciistr, char1, char2, char3])
	return asciistr


def filterstring_alpha(string, fraction=0.95):
	"""
	Filters a string depending on what fraction of its composing characters are
	letters (uppercase or lowercase). If the fraction is above "fraction", then
	"true" is returned. Otherwise the return value is "false"

	Parameters
	----------
	string : a Python string
		The string we want to filter
	fraction : float (optional)
		the minimum fraction of characters in the string that must be letters
		(uppercase or lowercase) or spaces in order to return true

	Return
	------
	A boolean value
	"""

	# Check for correct input
	if type(string) == str:
		try:
			fraction = float(fraction)
			if (fraction < 0) or (fraction > 1):
				raise ValueError
		except ValueError:
			print("Second argument must be a number between 0 and 1")
			raise ValueError
	else:
		print("First argument must by a Python string")
		raise ValueError


	alpha = 0
	for character in string:
		if character.isupper() or character.islower() or character.isspace():
			alpha += 1

	if float(alpha) / len(string) >= fraction:
		return True
	else:
		return False


def hammingdist(str1, str2):
	"""
	Calculates the Hemming distance between two python strings (that is, the
	number of different bits in the binary representation of the ascii string.
	Both strings must be of	the same length.

	Parameters
	----------
	str1 : a Python string
		One of the strings we want to compare
	str2 : a Python string
		The other string we want to compare

	Returns
	-------
	The number of different bits in the two strings (Hamming distance)
	"""

	# Check that the input are actually strings and that they are of the same
	# length
	if (type(str1) == str) and (type(str2) == str):
		if len(str1) == len(str2):
			pass
		else:
			print("Both input strings must be the same length")
			raise ValueError
	else:
		print("Input must be two Python strings")
		raise ValueError

	# We will xor character-wise, count the number of ones in the xor-ed result
	# and keep a running sum of the ones we find.
	ones = 0
	for i in xrange(0, len(str1)):
		xored = ord(str1[i]) ^ ord(str2[i])
		binary = bin(xored)
		for digit in binary:
			if digit == '1':
				ones += 1

	return ones

# TODO Modificar test per reflexar que si blocksize és 0 i el padding de la
# cadena no és correcte, ha de llençar una excepció
def pkcs7padding(string, blocksize):
	"""
	Adds pkcs#7 padding to a string. If blocksize is 0, then the function will
	actually remove the padding bytes from the end of the string if the padding
	is correct, or throw an exeption if the padding is not correct.

	Parameters
	----------
	string : a Python string
		The string we want to pad
	blocksize : a Python integer
		The blocksize we want to apply to the string. If set to 0, then the
		funcion will remove the padding.

	Return
	------
	A Python string padded to blocksize bytes, or an unpadded Python string if
	blocksize is 0
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

	if blocksize > 0:
		# Add the padding
		extrachars = len(string) % blocksize
		paddingnum = blocksize - extrachars
		paddingchar = chr(paddingnum)
		paddingstr = paddingchar * paddingnum
		paddedstr = "".join([string, paddingstr])

		return paddedstr
	elif blocksize == 0:
		# We are supposed to remove the padding. First check that the padding
		# is correct and if it is, remove it.
		lastchar_num = ord(string[-1])
		padding = string[-lastchar_num:]
		if padding == string[-1] * lastchar_num:
			return string[:-lastchar_num]
		else:
			raise TypeError
	else:
		print("The blocksize must be a positive integer")
		raise ValueError


def encrypt_repeating(message, key, base64=False):
	"""
	Encrypts a string with a repeating key. The message and the key are Python
	strings.

	Parameters
	----------
	message : Python string
		The message to be encrypted
	key : Python string
		The password that will be used as encryption key
	base64 : a boolean (optional)
		If true, the encrypted message will be encoded in base64. The default
		setting (false) outputs the encrypted message in its ascii
		representation

	Returns
	-------
	An Python string with the encrypted message. By default the output is the
	ascii representation of the encrypted message. If the base64 option is set
	to true, the output will be encoded as a base64 string
	"""

	# Check the input
	if (type(message) == str) and (type(key) == str):
		pass
	else:
		print("Message and key must be Python strings")
		raise ValueError

	# We xor sequentially every character of the message with a character
	# of the key. When we reach the end of the key we go back to its first
	# character
	encrypted = ""
	blocksize = len(key)
	for (index, character) in enumerate(message):
		encchar = chr(ord(character) ^ ord(key[index % blocksize]))
		encrypted = "".join([encrypted, encchar])

	if base64:
		return asciitob64(encrypted)
	else:
		return encrypted


def decrypt_repeating(message, key):
	"""
	Decrypts a string with a repeating key. The message and the key are Python
	strings. The algorithm for decryption and encryption is completely
	symmetrical, so this function actually calls the encrypt_repeating function

	Parameters
	----------
	message : Python string
		The ascii representation of the encrypted message
	key : Python string
		The password that will be used as encryption key

	Returns
	-------
	An Python string with the decrypted message.
	"""

	return encrypt_repeating(message, key, base64=False)


def encrypt_aes_cbc_128(message, key, iv, base64=False):
	"""
	Encrypts a Python string using AES in CBC mode and a 128 bit key. The CBC
	mode has been implemented "by hand", repeatedly calling the AES encryption
	algorithm found in the crypto++ library (Python bindings in pycryptopp).
	The function is called in ECB mode for each block, and the xor with the
	ciphertext of the previous block is done by hand.

	Parameters
	----------
	message : Python string
		The message to be encrypted
	key : Python string
		A 16 character python string that will be used as the key
	iv : Python string
		The initialization vector of the CBC mode
	base64 : (optional) boolean
		If true, the output ciphertext will be encoded in base 64. The default
		is false.

	Returns
	-------
	The encrypted message, by default as an ascii string.
	"""

	# Check the input
	blocksize = 16
	if (type(message) == str) and (type(key) == str) and (type(iv) == str):
		if (len(key) == blocksize) and (len(iv) == blocksize):
			pass
		else:
			print("The key and the initialization vector must be 16 bytes long")
			raise ValueError
	else:
		print("The message, key and initialization vector must be Python " + \
			"strings")
		raise ValueError

	# Padding of the message to make its length a multiple of the block size
	msg = pkcs7padding(message, blocksize)

	# Generate the AES cipher in ECB mode and encrypt. We have special code for
	# the first block because of the initialization vector
	cipher = AES.new(key, AES.MODE_ECB)
	ciphertext = ""

	# First block
	plaintext = msg[0:blocksize]
	previous = iv
	xored = encrypt_repeating(plaintext, previous)
	ciphertextblock = cipher.encrypt(xored)
	ciphertext = "".join([ciphertext, ciphertextblock])

	# Remainging blocks
	for i in xrange(blocksize, len(msg), blocksize):
		plaintext = msg[i:i+blocksize]
		previous = ciphertextblock
		xored = encrypt_repeating(plaintext, previous)
		ciphertextblock = cipher.encrypt(xored)
		ciphertext = "".join([ciphertext, ciphertextblock])

	# Encode in base 64 for pretty printing if requested
	if base64:
		return asciitob64(ciphertext)
	else:
		return ciphertext


def decrypt_aes_cbc_128(ciphertext, key, iv):
	"""
	Decrypts a ciphertext that has been encrypted with AES in CBC mode. The CBC
	mode has been implemented "by hand" by repeatedly calling the AES
	encryption algorithm of the crypto++ library in ECB mode on each block of
	the ciphertext.

	Parameters
	----------
	ciphertext : Python string
		The ascii representation of the ciphertext
	key : Python string
		A 16 character Python string used as the key
	iv : Python string
		The initialization vector

	Returns
	-------
	A Python string with the plaintext.
	"""

	# Check the input
	blocksize = 16
	if (type(ciphertext) == str) and (type(key) == str) and (type(iv) == str):
		if (len(key) == blocksize) and (len(iv) == blocksize):
			pass
		else:
			print("The key and the initialization vector must be 16 bytes long")
			raise ValueError
	else:
		print("The ciphertext, key and initialization vector must be " + \
			"Python strings")
		raise ValueError

	# Generate the AES cipher in ECB mode and decrypt. We have special code for
	# the first block because of the initialization vector
	cipher = AES.new(key, AES.MODE_ECB)
	plaintext = ""

	# First block
	previous = iv
	cipherblock = ciphertext[0:blocksize]
	xored = cipher.decrypt(cipherblock)
	plainblock = decrypt_repeating(xored, previous)
	plaintext = "".join([plaintext, plainblock])

	# Remainging blocks
	for i in xrange(blocksize, len(ciphertext), blocksize):
		previous = cipherblock
		cipherblock = ciphertext[i:i+blocksize]
		xored = cipher.decrypt(cipherblock)
		plainblock = decrypt_repeating(xored, previous)
		plaintext = "".join([plaintext, plainblock])

	# Remove the pkcs7 padding from the plaintext
	return pkcs7padding(plaintext, 0)


# TODO Afegir unittests
def encrypt_aes_ctr_128(plaintext, key):
	"""
	Encrypt the plaintext using AES CTR mode. The implementation of the CTR
	streaming is "manual". Each block of the stream is encrypted using AES_ECB.
	The format of the nonce is:

	0 0 0 0 0 0 0 | 0 0 0 0 0 0 0 0

	The first 8 bytes are always zero. The second block of 8 bytes is the
	counter, +1 for each block, in little endian mode, that is, for the first
	three blocks the nonce would be:

	block 0: 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
	block 1: 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
	block 2: 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0

	and so on.

	Parameters
	----------
	plaintext : a Python string
		The plaintext to be encrypted
	key : a Python string
		A 16-character string that will be used as the key for the AES_ECB
		encryption of the counter

	Returns
	-------
	A Python string with the ciphertext
	"""

	# We will work in blocks
	blocksize = 16
	plaintext = BlockString(plaintext, blocksize)

	# Set the nonce and the initial value of the counter
	nonce = "\x00" * 8
	counter = "\x00" * 8

	# Encrypt block by block
	cipher = AES.new(key, mode=AES.MODE_ECB)
	ciphertext = ""
	for block in plaintext:
		# Encrypt the nonce + counter
		stream = "".join([nonce, counter])
		cipherstream = cipher.encrypt(stream)

		# XOR the encrypted stream with the plaintext block
		for i in xrange(len(block)):
			cipherchar = chr(ord(cipherstream[i]) ^ ord(block[i]))
			ciphertext = "".join([ciphertext, cipherchar])

		# Increase the counter
		counter = [ord(char) for char in counter]
		for i in xrange(len(counter)):
			if counter[i] < 255:
				counter[i] += 1
				break
			elif counter[i] == 255:
				counter[i] = 0
			else:
				print("Something terrible happened")
				raise ValueError
		counter = [chr(digit) for digit in counter]
		counter = "".join(counter)

	return ciphertext


# TODO Afegir unittests
def decrypt_aes_ctr_128(ciphertext, key):
	"""
	Decrypt the ciphertext using AES CTR mode. The implementation of the CTR
	streaming is "manual". Each block of the stream is encrypted using AES_ECB.

	The format of the nonce is:

	0 0 0 0 0 0 0 | 0 0 0 0 0 0 0 0

	The first 8 bytes are always zero. The second block of 8 bytes is the
	counter, +1 for each block, in little endian mode, that is, for the first
	three blocks the nonce would be:

	block 0: 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
	block 1: 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
	block 2: 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0

	and so on.

	Note that, due to the particular way in which CTR works, there is no such
	thing as "decryption", and in fact this function is exactly the same as
	encrypt_aes_ctr_128. Here we are just calling the encryption function using
	the ciphertext as the plaintext. In CTR we always encrypt the counter with
	the key. If we XOR that with the plaintext, we get the ciphertext. If
	instead we XOR that with the ciphertext, we obtain the plaintext.

	Parameters
	----------
	ciphertext : a Python string
		The ciphertext to be decrypted
	key : a Python string
		A 16-character string that will be used as the key for the AES_ECB
		encryption of the counter

	Returns
	-------
	A Python string with the plaintext

	"""

	return encrypt_aes_ctr_128(ciphertext, key)


def random_key(length):
	"""
	Generates a random characters sequence to be used as a key.

	Parameters
	----------
	length : integer
		The length of the random key

	Returns
	-------
	A random 16-character Python string
	"""

	# Check the input
	if (type(length) == int) and (length >= 0):
		pass
	else:
		print("The length must be a nonnegative integer")
		raise ValueError

	key = ""
	rnd.seed()
	for i in xrange(length):
		key = "".join([key, chr(rnd.randint(0,  256))])

	return key


def blackbox_ecb_cbc_128(plaintext):
	"""
	This function prepends and appends a random string between 5 and 10
	characters long (length random too), and then encrypts randomly in ECB or
	CBC mode. In the case of CBC, the initialization vector is chosen randomly
	and in both cases the encryption key is chosen randomly

	Parameters
	----------
	plaintext : Python string
		The message we want to encrypt

	Returns
	-------
	A python string with the ascii representation of the encrypted message
	"""

	# Check input
	if type(plaintext) == str:
		pass
	else:
		print("Input must be a Python string")
		raise ValueError

	# Generate the random key
	blocksize = 16
	key = random_key(blocksize)

	# Add between 5 and 10 characters (random amount) at the beginning and the
	# end of the plaintext
	rnd.seed()
	prependnum = rnd.randint(5, 11)
	prependstring = ""
	for i in xrange(prependnum):
		prependstring = "".join([prependstring, chr(rnd.randint(256))])

	appendnum = rnd.randint(5, 11)
	appendstring = ""
	for i in xrange(appendnum):
		appendstring = "".join([appendstring, chr(rnd.randint(256))])

	plaintext = "".join([prependstring, plaintext, appendstring])
	plaintext = pkcs7padding(plaintext, blocksize)

	# Decide randomly between ECB and CBC.
	rnd.seed()
	cbc = rnd.randint(2)
	if cbc:
		# Encrypt using CBC mode with a random IV
		iv = random_key(blocksize)
		cipher = AES.new(key, IV=iv, mode=AES.MODE_CBC)
		ciphertext = cipher.encrypt(plaintext)
	else:
		# Encrypt using EBC mode
		cipher = AES.new(key, AES.MODE_ECB)
		ciphertext = cipher.encrypt(plaintext)

	return ciphertext
