# -*- coding: utf-8 -*-

# The matasano cryptography challeges
# Set 2 / Challenge 15
# PKCS#7 padding validation

import matasanolib

str_1 = "ICE ICE BABY\x04\x04\x04\x04"
print repr(str_1)
try:
	str_1_unpad = matasanolib.pkcs7padding(str_1, 0)
	print repr(str_1_unpad)
	print "The padding is correct"
except TypeError:
	print "The padding is not correct"

print ""

str_2 = "ICE ICE BABY\x05\x05\x05\x05"
print repr(str_2)
try:
	str_2_unpad = matasanolib.pkcs7padding(str_2, 0)
	print repr(str_2_unpad)
	print "The padding is correct"
except TypeError:
	print "The padding is not correct"

print ""

str_3 = "ICE ICE BABY\x01\x02\x03\x04"
print repr(str_3)
try:
	str_3_unpad = matasanolib.pkcs7padding(str_3, 0)
	print repr(str_3_unpad)
	print "The padding is correct"
except TypeError:
	print "The padding is not correct"

print ""

str_4 = "hola carambola"
print repr(str_4)
try:
	str_4_unpad = matasanolib.pkcs7padding(str_4, 0)
	print repr(str_4_unpad)
	print "The padding is correct"
except TypeError:
	print "The padding is not correct"
