# -*- coding: utf-8 -*-

# The matasano crypto challenges
# Set 1 / Challenge 6
# Break repeating-key XOR
# TODO: something went wrong when I made changes to matasanolib. I have to
# review everything to make it work again.

import sys
sys.path.append('/home/joan/Programming/the matasano cryptography challenges/')
import matasanolib
import string
import numpy as np

# Read the file with the base64-encoded encrypted string
path = "/home/joan/Programming/the matasano cryptography challenges/" + \
	"set1.challenge6.encrypted.txt"
hfile = open(path, "r")
message = ""
for line in hfile:
	message += line.strip()

# Every 4 base64 characters take 3 bytes. Since the last character is =, we
# know that the string has been padded (see
# "https://en.wikipedia.org/wiki/Base64\") and therefore the number of
# characters in the message should be divisible by 4. We have to take care of
# the decoding of the last 4-bit block to eliminate those that belong to the
# padding.

padding = 0
if message[-1] == "=":
	padding += 1
	message = message[:-1] + 'A'
if message[-2] == "=":
	padding += 1
	message = messabe[:-2] + 'AA'

message = [message[i:i+4] for i in range(0, len(message), 4)]
message = [matasanolib.b64toint(block) for block in message]
hexmessage = ""
for block in message:
	hexmessage += '%06x' % block
if padding == 1:
	hexmessage = hexmessage[:-2]
elif padding == 2:
	hexmessage = hexmessage[:-4]

# Once we have the hex string, we can start the process of deducing the key
# length

minlength = 1
maxlength = 40
keysize_list = range(minlength, maxlength+1)
meandist_list = np.zeros(len(keysize_list), np.float64)

# For each key size under consideration (in bytes), we calculate the Hamming
# distance between contiguous blocks of size equal to that of the key. We will
# calculate the distance between all contiguous blocks and calculate the average
for (index, keysize) in enumerate(keysize_list):
	# Partition the hex string in blocks of size keysize
	partition = [hexmessage[i:i+2*keysize] for i in range(0, len(hexmessage), 2*keysize)]

	# Calculate the distance between all the contiguous pairs (except the last
	# two, because it could happen that the last one is shorter than the second
	# to last
	distances = [matasanolib.hammingdist(partition[i], partition[i+1])
		for i in range(0, len(partition)-2)]
	distances = np.array(distances)

	# Calculate the average distance normalized to the key size
	meandist = distances.sum() / np.size(distances) / (keysize * 8.0)
	meandist_list[index] = meandist

# The key size is probably the one that gives the smallest Hamming distance
minimum = np.min(meandist_list)
indexminimum = np.argmin(meandist_list)
probkeysize = keysize_list[indexminimum]

# Once we have a promising candidate to be the key size, partition the
# encrypted sequence in blocks of as many bytes as the key size

# Check that it's divisible, and if not, calculate how many padding bytes should
# be added, and add them.
messagelen = len(hexmessage) / 2
remainder = messagelen % probkeysize
if remainder != 0:
	padding = probkeysize - remainder
	hexmessage += '00' * padding
else:
	padding = 0

# Partition
partition = [hexmessage[i:i+probkeysize*2]
	for i in range(0, len(hexmessage), probkeysize*2)]

# If we create a matrix in which every row is one of those encrypted blocks,
# with a character in each column, then it's clear that each column of the
# matrix has been encrypted with the same character. Then we decrypt each column
# with a single character, trying all possible characters. When we decrypt with
# the correct character, the output will not make sense, but it will show a
# correct frequency of letters. Therefore, we can filter the results and keep
# only those that look promising. We do that for each column and in the end we
# will have a good candidate to the complete key.

for (index, block) in enumerate(partition):
	partition[index] = [int(block[i:i+2], base=16) for i in range(0, len(block), 2)]
partition = np.array(partition, np.int8)

# Decrypt each column with a repeating key of a single character. Change the
# repeating character until we get a potentially good result, and put that in
# a list.
#
# Important! Ath this point we need a bit of interactivity, adjusting the
# filtering factor to make sure that we have at least one candidate fore each
# character of the key.

# Ascii characters in integer form
keychars = np.arange(32, 127, dtype=np.int8)

# List of candidates to be characters of the key
candidates = []

for charline in partition.T:
	# List of candidates for each position
	linecandidates = []

	for keychar in keychars:
		# Decrypt the column of "partition" with a character
		charlinetxt = [chr(char) for char in charline]
		decryptedtxt = matasanolib.decrypt_repeating("".join(charlinetxt), chr(keychar))

		# Recover the decrypted string
		#decryptedtxt = ""
		#for char in decrypted:
			#decryptedtxt += chr(char)

		# Filter the text according to the percent of letters
		if matasanolib.filterstring_alpha(decryptedtxt, 0.8):
			linecandidates.append(keychar)

	candidates.append(linecandidates)

# Since typically we will have some key position with more than one possible
# candidate, generate all possible candidate keys

numclaus = np.array([len(i) for i in candidates])
numclaus = np.prod(numclaus)

llistaclaus = np.zeros((numclaus, probkeysize), np.int8)
divisions = 1
for (columna, candidats) in enumerate(candidates):
	numcandidats = len(candidats)
	divisions *= numcandidats
	for i in range(0, numclaus):
		numparticio = int(floor(i / (numclaus/divisions)))
		llistaclaus[i, columna] = candidats[numparticio % numcandidats]

# Code to print the possible keys to a file, to see if we can identify the
# good one manually. The write method converts directly the integer numpy array
# to ascii characters
harxiu = open("/home/joan/claus.txt", 'w')
for clau in llistaclaus:
	harxiu.write(clau)
	harxiu.write("\n")
harxiu.close()

# Now it only remains to decrypt the message with each and every key, and filter
# the results to keep the best.

# Start removing the padding we added to the hex string
hexmessage = hexmessage[:-(2 * padding)]

# Divide the sequence in blocks of 8 bits
intmessage = [int(hexmessage[i:i+2], base=16) for i in range(0, len(hexmessage), 2)]
intmessage = np.array(intmessage, np.int8)

# For each key, decrypt and filter. Print the result to standard output and file
arxiu = open("/home/joan/desencriptat.txt", "w")
for (idx, key) in enumerate(llistaclaus):
	decrypted = matasanolib.decrypt_repeating(intmessage, key)

	# Build the ascii string of message and key
	decryptedtxt = ""
	for character in decrypted:
		decryptedtxt += chr(character)

	keytxt = ""
	for character in key:
		keytxt += chr(character)

	# Filter
	if matasanolib.filterstring_alpha(decryptedtxt, 0.90):
		print(idx, keytxt, decryptedtxt)
		print("\n")
		arxiu.write("%d / %s\n%s\n\n" % (idx, keytxt, decryptedtxt))

arxiu.close()

# We can see that this filter is usless, because if we set it to 0.95 we get
# only one result, and it's not the correct one. If we go down to 0.94 we get
# all the results. At any rate, with only 16 results we can clearly see which
# one is the good one, "Terminator X: Bring the noise"
