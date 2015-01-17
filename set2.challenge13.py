# -*- coding: utf-8 -*-

# The matasano cryptography challeges
# Set 2 / Challenge 12
# ECB cut-and-paste

# Imports
from ipdb import set_trace
import matasanolib
from Crypto.Cipher import AES

# A couple of functions we will be using
def parseoptions(string):
	"""
	Receive a string of option=value pairs separated by & and parse it to
	return a dictionary where the options are the keys and the values are the
	values

	Parameters
	----------
	string : a Python string
		A list of option=value pairs separated by &, for instance:
		name=joan&occupation=cool guy&weight=adecuate

	Returns
	-------
	A dictionary with the key:value pairs
	"""

	if type(string) == str:
		pass
	else:
		print("The input must be a Python string")
		raise ValueError

	optionlist = string.split("&")
	dictionary = {}
	for pair in optionlist:
		pairlist = pair.split("=")
		try:
			dictionary[pairlist[0]] = pairlist[1]
		except IndexError:
			print(pair + " is not a valid option=value pair")
			raise ValueError

	return dictionary


def generate_profile(email, key):
	"""
	Generates a sort of user profile with email address, a user id number and a
	role of "user" (as opposed to "admin", for example). The profile is
	returned encoded in k=v pairs separated by &. The user id is assigned
	randomly.

	As an example, generate_profile("johndoe@mail.com") would return the string:
		email=johndoe@mail.com&id=1000&role=user

	Parameters
	----------
	email : Python string
		An email adress. The '=' and '&' symbols are not accepted

	Returns
	-------
	A profile string as in the previous example
	"""

	# Check the input
	if type(email) == str:
		pass
	else:
		print("The input parameter must be a Python string with an " + \
			"email address")
		raise ValueError

	emaillst = email.split("&")
	if len(emaillst) > 1:
		print("The '&' character is not valid")
		raise ValueError

	emaillst = emaillst[0].split("=")
	if len(emaillst) > 1:
		print("The '=' character is not valid")
		raise ValueError

	# Check that the email is valid
	email = emaillst[0]
	if "@" not in email:
		print("Invalid mail")
		raise ValueError
	else:
		blocks = email.split("@")
		if "." not in blocks[1]:
			print("Invalid mail")
			raise ValueError

	profile = "&".join(["email="+email, "id=1000", "role=user"])

	# Encrypt the profile
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.encrypt(matasanolib.pkcs7padding(profile, len(key)))


### Main program ###

# Generate a random key
blocksize = 16
key = matasanolib.random_key(blocksize)

# Generate a user profile and encrypt it with the random key
email = "joan@gollum.cat"
cipherprofile = generate_profile(email, key)

# Now decrypt and parse it
cipher = AES.new(key, AES.MODE_ECB)
decrypted_profile = cipher.decrypt(cipherprofile)
decrypted_profile = matasanolib.pkcs7padding(decrypted_profile, 0)
decrypted_profile = parseoptions(decrypted_profile)
print(decrypted_profile)

# Now the point is to cleverly use the generate_profile with chosen inputs so
# that we can somehow generate a valid ciphertext that decrypts to a role=admin
# profile
print("")

# Take the first two blocks of this profile
crafted1 = "joan@gom.cat"
cipher1 = generate_profile(crafted1, key)

# Take the second block of this profile
crafted2 = "joan@a.comadmin\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b"
cipher2 = generate_profile(crafted2, key)

# Final cipher
finalcipher = cipher1[0:blocksize*2] + cipher2[blocksize:blocksize*2]

# Decrypt and parse the crafted cipherprofile
decrypted = cipher.decrypt(finalcipher)
decrypted = matasanolib.pkcs7padding(decrypted, 0)
decrypted = parseoptions(decrypted)
print(decrypted)