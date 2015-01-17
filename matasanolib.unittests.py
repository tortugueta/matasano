# -*- coding: utf-8 -*-

# Unit tests for matasanolib.py

# Imports
import unittest
import matasanolib

class Test_inttob64(unittest.TestCase):
	"""
	Test the matasanolib.intto64 function
	"""

	def setUp(self):
		"""
		Prepare data for the tests
		"""

		self.integers = range(0, 64)
		self.symbols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
			"L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
			"Y","Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
			"l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
			"y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+",
			"/"]


	def test_input(self):
		"""
		Check for correct handling of input
		"""

		self.assertRaises(ValueError, matasanolib.inttob64, 1.0)
		self.assertRaises(ValueError, matasanolib.inttob64, 'a')
		self.assertRaises(ValueError, matasanolib.inttob64, "string")
		self.assertRaises(ValueError, matasanolib.inttob64, [])
		self.assertRaises(ValueError, matasanolib.inttob64, ())

	def test_output(self):
		"""
		Check for correct output using some known (input, output) examples
		"""

		values = [matasanolib.inttob64(value) for value in self.integers]
		self.assertEqual(type(values[0]), str)
		self.assertEqual(self.symbols, values)
		self.assertEqual("BA", matasanolib.inttob64(64**1))
		self.assertEqual("BAA", matasanolib.inttob64(64**2))
		self.assertEqual("BAAA", matasanolib.inttob64(64**3))


class Test_b64toint(unittest.TestCase):
	"""
	Test the matasanolib.b64toint function
	"""

	def setUp(self):
		"""
		Prepare data for the tests
		"""

		self.integers = range(0, 64)
		self.symbols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
			"L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
			"Y","Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
			"l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
			"y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+",
			"/"]


	def test_input(self):
		"""
		Check for correct handling of input
		"""

		self.assertRaises(ValueError, matasanolib.b64toint, 1)
		self.assertRaises(ValueError, matasanolib.b64toint, 1.0)
		self.assertRaises(ValueError, matasanolib.b64toint, [])
		self.assertRaises(ValueError, matasanolib.b64toint, ())
		self.assertRaises(ValueError, matasanolib.b64toint, "abAB==")
		self.assertRaises(ValueError, matasanolib.b64toint, "ab$09")

	def test_output(self):
		"""
		Check for correct output using some known (input, output) examples
		"""

		values = [matasanolib.b64toint(symbol) for symbol in self.symbols]
		self.assertEqual(type(values[0]), int)
		self.assertEqual(self.integers, values)
		self.assertEqual(matasanolib.b64toint("BA"), 64**1)
		self.assertEqual(matasanolib.b64toint("BAA"), 64**2)
		self.assertEqual(matasanolib.b64toint("BAAA"), 64**3)


class Test_asciitob64(unittest.TestCase):
	"""
	Test the matasanolib.asciitob64 function
	"""

	def test_input(self):
		"""
		Check for correct handling of input
		"""

		self.assertRaises(ValueError, matasanolib.asciitob64, 1)
		self.assertRaises(ValueError, matasanolib.asciitob64, 1.0)
		self.assertRaises(ValueError, matasanolib.asciitob64, [])
		self.assertRaises(ValueError, matasanolib.asciitob64, ())

	def test_output(self):
		"""
		Check for correct output using some known (input, output) examples
		"""

		l1 = "Man is distinguished, not only by his reason, "
		l2 = "but by this singular passion from other animals, which "
		l3 = "is a lust of the mind, that by a perseverance of "
		l4 = "delight in the continued and indefatigable "
		l5 = "generation of knowledge, exceeds the short vehemence of "
		l6 = "any carnal pleasure."
		example = "".join([l1, l2, l3, l4, l5, l6])
		l1r = "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvbmx5IGJ5IGhpcyByZWFzb24sIG"
		l2r = "J1dCBieSB0aGlzIHNpbmd1bGFyIHBhc3Npb24gZnJvbSBvdGhlciBhbmltYWxz"
		l3r = "LCB3aGljaCBpcyBhIGx1c3Qgb2YgdGhlIG1pbmQsIHRoYXQgYnkgYSBwZXJzZX"
		l4r = "ZlcmFuY2Ugb2YgZGVsaWdodCBpbiB0aGUgY29udGludWVkIGFuZCBpbmRlZmF0"
		l5r = "aWdhYmxlIGdlbmVyYXRpb24gb2Yga25vd2xlZGdlLCBleGNlZWRzIHRoZSBzaG"
		l6r = "9ydCB2ZWhlbWVuY2Ugb2YgYW55IGNhcm5hbCBwbGVhc3VyZS4="
		expected = "".join([l1r, l2r, l3r, l4r, l5r, l6r])
		self.assertEqual(matasanolib.asciitob64(example), expected)

		example = "any carnal pleasure."
		expected = "YW55IGNhcm5hbCBwbGVhc3VyZS4="
		self.assertEqual(matasanolib.asciitob64(example), expected)

		example = "any carnal pleasure"
		expected = "YW55IGNhcm5hbCBwbGVhc3VyZQ=="
		self.assertEqual(matasanolib.asciitob64(example), expected)

		example = "any carnal pleasur"
		expected = "YW55IGNhcm5hbCBwbGVhc3Vy"
		self.assertEqual(matasanolib.asciitob64(example), expected)

		example = "any carnal pleasu"
		expected = "YW55IGNhcm5hbCBwbGVhc3U="
		self.assertEqual(matasanolib.asciitob64(example), expected)

		example = "any carnal pleas"
		expected = "YW55IGNhcm5hbCBwbGVhcw=="
		self.assertEqual(matasanolib.asciitob64(example), expected)

		example = "pleasure."
		expected = "cGxlYXN1cmUu"
		self.assertEqual(matasanolib.asciitob64(example), expected)

		example = "leasure."
		expected = "bGVhc3VyZS4="
		self.assertEqual(matasanolib.asciitob64(example), expected)

		example = "easure."
		expected = "ZWFzdXJlLg=="
		self.assertEqual(matasanolib.asciitob64(example), expected)

		example = "asure."
		expected = "YXN1cmUu"
		self.assertEqual(matasanolib.asciitob64(example), expected)

		example = "sure."
		expected = "c3VyZS4="
		self.assertEqual(matasanolib.asciitob64(example), expected)


class Test_b64toascii(unittest.TestCase):
	"""
	Test the matasanolib.b64toascii function
	"""

	def test_input(self):
		"""
		Check the correct handling of input data
		"""

		self.assertRaises(ValueError, matasanolib.b64toascii, 3)
		self.assertRaises(ValueError, matasanolib.b64toascii, 1.0)
		self.assertRaises(ValueError, matasanolib.b64toascii, [])
		self.assertRaises(ValueError, matasanolib.b64toascii, ())
		self.assertRaises(ValueError, matasanolib.b64toascii, "$")
		self.assertRaises(ValueError, matasanolib.b64toascii, "Qqo$")
		self.assertRaises(ValueError, matasanolib.b64toascii, "Qq$=")
		self.assertRaises(ValueError, matasanolib.b64toascii, "Q$==")
		self.assertRaises(ValueError, matasanolib.b64toascii, "bGVhc3VyZS4")

	def test_output(self):
		"""
		Check for correct output using known (input, output) examples
		"""

		l1r = "TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvbmx5IGJ5IGhpcyByZWFzb24sIG"
		l2r = "J1dCBieSB0aGlzIHNpbmd1bGFyIHBhc3Npb24gZnJvbSBvdGhlciBhbmltYWxz"
		l3r = "LCB3aGljaCBpcyBhIGx1c3Qgb2YgdGhlIG1pbmQsIHRoYXQgYnkgYSBwZXJzZX"
		l4r = "ZlcmFuY2Ugb2YgZGVsaWdodCBpbiB0aGUgY29udGludWVkIGFuZCBpbmRlZmF0"
		l5r = "aWdhYmxlIGdlbmVyYXRpb24gb2Yga25vd2xlZGdlLCBleGNlZWRzIHRoZSBzaG"
		l6r = "9ydCB2ZWhlbWVuY2Ugb2YgYW55IGNhcm5hbCBwbGVhc3VyZS4="
		example = "".join([l1r, l2r, l3r, l4r, l5r, l6r])
		l1 = "Man is distinguished, not only by his reason, "
		l2 = "but by this singular passion from other animals, which "
		l3 = "is a lust of the mind, that by a perseverance of "
		l4 = "delight in the continued and indefatigable "
		l5 = "generation of knowledge, exceeds the short vehemence of "
		l6 = "any carnal pleasure."
		expected = "".join([l1, l2, l3, l4, l5, l6])
		self.assertEqual(matasanolib.b64toascii(example), expected)

		example = "YW55IGNhcm5hbCBwbGVhc3VyZS4="
		expected = "any carnal pleasure."
		self.assertEqual(matasanolib.b64toascii(example), expected)

		example = "YW55IGNhcm5hbCBwbGVhc3VyZQ=="
		expected = "any carnal pleasure"
		self.assertEqual(matasanolib.b64toascii(example), expected)

		example = "YW55IGNhcm5hbCBwbGVhc3Vy"
		expected = "any carnal pleasur"
		self.assertEqual(matasanolib.b64toascii(example), expected)

		example = "YW55IGNhcm5hbCBwbGVhc3U="
		expected = "any carnal pleasu"
		self.assertEqual(matasanolib.b64toascii(example), expected)

		example = "YW55IGNhcm5hbCBwbGVhcw=="
		expected = "any carnal pleas"
		self.assertEqual(matasanolib.b64toascii(example), expected)

		example = "cGxlYXN1cmUu"
		expected = "pleasure."
		self.assertEqual(matasanolib.b64toascii(example), expected)

		example = "bGVhc3VyZS4="
		expected = "leasure."
		self.assertEqual(matasanolib.b64toascii(example), expected)

		example = "ZWFzdXJlLg=="
		expected = "easure."
		self.assertEqual(matasanolib.b64toascii(example), expected)

		example = "YXN1cmUu"
		expected = "asure."
		self.assertEqual(matasanolib.b64toascii(example), expected)

		example = "c3VyZS4="
		expected = "sure."
		self.assertEqual(matasanolib.b64toascii(example), expected)


class Test_filterstring_alpha(unittest.TestCase):
	"""
	Test the matasanolib.filterstring_alpha function
	"""

	def test_input(self):
		"""
		Check for correct handling of the input
		"""

		self.assertRaises(ValueError, matasanolib.filterstring_alpha, 1, 0.1)
		self.assertRaises(ValueError, matasanolib.filterstring_alpha, 1.0, 0.1)
		self.assertRaises(ValueError, matasanolib.filterstring_alpha, [], 0.1)
		self.assertRaises(ValueError, matasanolib.filterstring_alpha, (), 0.1)
		self.assertRaises(ValueError, matasanolib.filterstring_alpha, "string",
			"a")
		self.assertRaises(ValueError, matasanolib.filterstring_alpha, "string",
			-5)
		self.assertRaises(ValueError, matasanolib.filterstring_alpha, "string",
			1.1)

	def test_output(self):
		"""
		Check for correct output using known (input, output) examples
		"""

		self.assertTrue(matasanolib.filterstring_alpha("string", 1))
		self.assertTrue(matasanolib.filterstring_alpha("string", 1.0))
		self.assertTrue(matasanolib.filterstring_alpha("$%&()!", 0))
		self.assertFalse(matasanolib.filterstring_alpha("$%&()!", 0.01))

class Test_hammingdist(unittest.TestCase):
	"""
	Test the matasanolib.hammingdist function
	"""

	def test_input(self):
		"""
		Test the correct handling of the input
		"""

		self.assertRaises(ValueError, matasanolib.hammingdist, 1, "str")
		self.assertRaises(ValueError, matasanolib.hammingdist, 1.0, "str")
		self.assertRaises(ValueError, matasanolib.hammingdist, [], "str")
		self.assertRaises(ValueError, matasanolib.hammingdist, (), "str")
		self.assertRaises(ValueError, matasanolib.hammingdist, "str", 1,)
		self.assertRaises(ValueError, matasanolib.hammingdist, "str", 1.0)
		self.assertRaises(ValueError, matasanolib.hammingdist, "str", [])
		self.assertRaises(ValueError, matasanolib.hammingdist, "str", ())
		self.assertRaises(ValueError, matasanolib.hammingdist, "len4", "len 5")

	def test_output(self):
		"""
		Test for correct output using known (input, output) examples
		"""

		example1 = "this is a test"
		example2 = "wokka wokka!!!"
		expected = 37
		self.assertEqual(matasanolib.hammingdist(example1, example2), expected)


class Test_pkcs7padding(unittest.TestCase):
	"""
	Thest the matasanolib.pkcs7padding function
	"""

	def test_input(self):
		"""
		Test the correct handling of the input
		"""

		self.assertRaises(ValueError, matasanolib.pkcs7padding, 1, 1)
		self.assertRaises(ValueError, matasanolib.pkcs7padding, 1.0, 1)
		self.assertRaises(ValueError, matasanolib.pkcs7padding, [], 1)
		self.assertRaises(ValueError, matasanolib.pkcs7padding, (), 1)
		self.assertRaises(ValueError, matasanolib.pkcs7padding, "string",
			"strong")
		self.assertRaises(ValueError, matasanolib.pkcs7padding, "string", 1.0)
		self.assertRaises(ValueError, matasanolib.pkcs7padding, "string", -1)
		self.assertRaises(ValueError, matasanolib.pkcs7padding, "string", [])
		self.assertRaises(ValueError, matasanolib.pkcs7padding, "string", ())


	def test_output(self):
		"""
		Check for the correctness of the result by comparing to known results
		"""

		example = "string"
		size = 6
		expected = "string\x06\x06\x06\x06\x06\x06"
		self.assertEqual(matasanolib.pkcs7padding(example, size), expected)
		self.assertEqual(matasanolib.pkcs7padding(expected, 0), example)

		size = 7
		expected = "string\x01"
		self.assertEqual(matasanolib.pkcs7padding(example, size), expected)
		self.assertEqual(matasanolib.pkcs7padding(expected, 0), example)

		size = 8
		expected = "string\x02\x02"
		self.assertEqual(matasanolib.pkcs7padding(example, size), expected)
		self.assertEqual(matasanolib.pkcs7padding(expected, 0), example)

		size = 5
		expected = "string\x04\x04\x04\x04"
		self.assertEqual(matasanolib.pkcs7padding(example, size), expected)
		self.assertEqual(matasanolib.pkcs7padding(expected, 0), example)

		size = 4
		expected = "string\x02\x02"
		self.assertEqual(matasanolib.pkcs7padding(example, size), expected)
		self.assertEqual(matasanolib.pkcs7padding(expected, 0), example)

		example = "This is an unpadded string"
		self.assertEqual(matasanolib.pkcs7padding(example, 0), example)

class Test_encrypt_repeating(unittest.TestCase):
	"""
	Test the matasanolib.encrypt_repeating function
	"""

	def test_input(self):
		"""
		Check the correct handling of the input
		"""

		self.assertRaises(ValueError, matasanolib.encrypt_repeating, 1, "str")
		self.assertRaises(ValueError, matasanolib.encrypt_repeating, 1.0, "str")
		self.assertRaises(ValueError, matasanolib.encrypt_repeating, [], "str")
		self.assertRaises(ValueError, matasanolib.encrypt_repeating, (), "str")
		self.assertRaises(ValueError, matasanolib.encrypt_repeating, "str", 1)
		self.assertRaises(ValueError, matasanolib.encrypt_repeating, "str", 1.0)
		self.assertRaises(ValueError, matasanolib.encrypt_repeating, "str", [])
		self.assertRaises(ValueError, matasanolib.encrypt_repeating, "str", ())

	def test_output(self):
		"""
		Check the correctness of the output using known (input, output) examples
		"""

		message = "Burning 'em, if you ain't quick and nimble\n" + \
			"I go crazy when I hear a cymbal"
		key = "ICE"
		expected_asc = '\x0b67\'*+.cb,.ii*#i:*<c$ -b=c4<*&"c$\'\'e\'*(+/ ' + \
			'C\ne.,e*1$3:e>+ \'c\x0ci+ (1e(c&0.\'(/'
		expected_b64 = "CzY3JyorLmNiLC5paSojaToqPGMkIC1iPWM0PComImMkJydlJyo" + \
			"oKy8gQwplLixlKjEkMzplPisgJ2MMaSsgKDFlKGMmMC4nKC8="
		self.assertEqual(matasanolib.encrypt_repeating(message, key),
			expected_asc)
		self.assertEqual(matasanolib.encrypt_repeating(message, key, True),
			expected_b64)


class Test_decrypt_repeating(unittest.TestCase):
	"""
	Test the matasanolib.decrypt_repeating function
	"""

	def test_input(self):
		"""
		Check the correct handling of the input
		"""

		self.assertRaises(ValueError, matasanolib.decrypt_repeating, 1, "str")
		self.assertRaises(ValueError, matasanolib.decrypt_repeating, 1.0, "str")
		self.assertRaises(ValueError, matasanolib.decrypt_repeating, [], "str")
		self.assertRaises(ValueError, matasanolib.decrypt_repeating, (), "str")
		self.assertRaises(ValueError, matasanolib.decrypt_repeating, "str", 1)
		self.assertRaises(ValueError, matasanolib.decrypt_repeating, "str", 1.0)
		self.assertRaises(ValueError, matasanolib.decrypt_repeating, "str", [])
		self.assertRaises(ValueError, matasanolib.decrypt_repeating, "str", ())

	def test_output(self):
		"""
		Check for the correctness of the output using known (input, output)
		examples
		"""

		message = "Burning 'em, if you ain't quick and nimble\n" + \
			"I go crazy when I hear a cymbal"
		key = "ICE"
		ciphertxt = '\x0b67\'*+.cb,.ii*#i:*<c$ -b=c4<*&"c$\'\'e\'*(+/ ' + \
			'C\ne.,e*1$3:e>+ \'c\x0ci+ (1e(c&0.\'(/'
		self.assertEqual(matasanolib.decrypt_repeating(ciphertxt, key),
			message)


class Test_encrypt_aes_cbc_128(unittest.TestCase):
	"""
	Test the matasanolib.encrypt_aes-cbc-128 function
	"""

	def test_input(self):
		"""
		Check the correct handling of the input
		"""

		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, 1,
			"yellow submarine",	"\x00" * 16)
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, 1.0,
			"yellow submarine", "\x00" * 16)
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, [],
			"yellow submarine",	"\x00" * 16)
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, (),
			"yellow submarine",	"\x00" * 16)
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, "s",
			1, "\x00" * 16)
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, "s",
			1.0, "\x00" * 16)
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, "s",
			[], "\x00" * 16)
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, "s",
			(), "\x00" * 16)
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, "s",
			"yellow submarine", 1)
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, "s",
			"yellow submarine", 1.0)
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, "s",
			"yellow submarine", [])
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, "s",
			"yellow submarine", ())
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, "s",
			"not long enough", "\x00" * 16)
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, "s",
			"this is too long a key", "\x00" * 16)
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, "s",
			"yellow submarine", "too short iv")
		self.assertRaises(ValueError, matasanolib.encrypt_aes_cbc_128, "s",
			"yellow submarine", "this iv is clearly too long")




	def test_output(self):
		"""
		Check for correct output using known (input, output) examples
		"""

		key = "yellow submarine"
		iv = "\x00" * 16
		msg = "This is a stupid test string. Nothing imaginative."
		expected = "nQ4U9XZkeZCopaGYCYH9qhVJ3ZQucDuDrZDmOxVw6DoaEEIh1oZrvCx" + \
			"wDr40+5lQwvTnLnYaJ14jzZ/Fr0/vPw=="
		self.assertEqual(matasanolib.encrypt_aes_cbc_128(msg, key, iv, True),
			expected)

class Test_decrypt_aes_cbc_128(unittest.TestCase):
	"""
	Test the matasanolib.decrypt_aes-cbc-128 function
	"""

	def test_input(self):
		"""
		Check the correct handling of the input
		"""

		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, 1,
			"yellow submarine",	"\x00" * 16)
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, 1.0,
			"yellow submarine", "\x00" * 16)
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, [],
			"yellow submarine",	"\x00" * 16)
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, (),
			"yellow submarine",	"\x00" * 16)
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, "s",
			1, "\x00" * 16)
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, "s",
			1.0, "\x00" * 16)
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, "s",
			[], "\x00" * 16)
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, "s",
			(), "\x00" * 16)
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, "s",
			"yellow submarine", 1)
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, "s",
			"yellow submarine", 1.0)
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, "s",
			"yellow submarine", [])
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, "s",
			"yellow submarine", ())
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, "s",
			"not long enough", "\x00" * 16)
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, "s",
			"this is too long a key", "\x00" * 16)
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, "s",
			"yellow submarine", "too short iv")
		self.assertRaises(ValueError, matasanolib.decrypt_aes_cbc_128, "s",
			"yellow submarine", "this iv is clearly too long")


	def test_output(self):
		"""
		Check for correct output using known (input, output) examples
		"""

		key = "yellow submarine"
		iv = "\x00" * 16
		msg = "This is a stupid test string. Nothing imaginative."
		encrypted = matasanolib.encrypt_aes_cbc_128(msg, key, iv)
		self.assertEqual(matasanolib.decrypt_aes_cbc_128(encrypted, key, iv),
			msg)


class Test_random_key(unittest.TestCase):
	"""
	Test the matasanolib.random_key function
	"""

	def test_input(self):
		"""
		There is no input to test
		"""

		self.assertRaises(ValueError, matasanolib.random_key, -1)
		self.assertRaises(ValueError, matasanolib.random_key, 1.0)
		self.assertRaises(ValueError, matasanolib.random_key, [])
		self.assertRaises(ValueError, matasanolib.random_key, ())

	def test_output(self):
		"""
		Check for correctness of the output
		"""

		key = matasanolib.random_key(16)
		self.assertEqual(len(key), 16)

		key = matasanolib.random_key(0)
		self.assertEqual(len(key),  0)


class Test_blackbox_ecb_cbc_128(unittest.TestCase):
	"""
	Test the matasanolib.blackbox_ecb_cbc function
	"""

	def test_input(self):
		"""
		Check handling of the input
		"""

		self.assertRaises(ValueError, matasanolib.blackbox_ecb_cbc_128, 1)
		self.assertRaises(ValueError, matasanolib.blackbox_ecb_cbc_128, 1.0)
		self.assertRaises(ValueError, matasanolib.blackbox_ecb_cbc_128, [])
		self.assertRaises(ValueError, matasanolib.blackbox_ecb_cbc_128, ())

	def test_output(self):
		"""
		Check output
		"""

		msg = "a" * 64
		ciphertext = matasanolib.blackbox_ecb_cbc_128(msg)
		self.assertEqual(type(ciphertext), str)


################################################################################



if __name__ == '__main__':
    unittest.main()
