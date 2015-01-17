# -*- coding: utf-8 -*-

# The matasano cryptography challeges
# Set 1 / Challenge 8
# Detect AES in ECB mode

# Imports
import sys
path = "/home/joan/Programming/the matasano cryptography challenges/"
sys.path.append(path)
import matasanolib
import numpy as np
from Crypto.Cipher import AES
import matplotlib.pyplot as plt

keylength = 16
keylengthbits = keylength * 8
arxiu = open(path + "set1.challenge8.encrypted.txt")
distancelist = []
cipherlist = []
for (lindex, line) in enumerate(arxiu):
	cipherlist.append(line.strip())
	padding, blocklist = matasanolib.partstr(line.strip(), 'hex', keylength)

	# Calculate mean Hamming distance between blocks
	distances = []
	for i in range(0, len(blocklist)-1):
		for j in range(i+1, len(blocklist)):
			distance = matasanolib.hammingdist(blocklist[i], blocklist[j]) \
				/ float(keylengthbits)
			distances.append(distance)

	distances = np.array(distances)
	meandist = distances.sum() / np.size(distances)
	distancelist.append(meandist)

distancelist = np.array(distancelist)

# Plot the Hamming distances to see if we can clearly identify a minimum
plt.plot(distancelist)
plt.xlabel("Ciphertext index")
plt.ylabel("Mean Hamming distance between contiguous blocks")
plt.title("Block size " + str(keylength) + " bytes")
plt.axis([0, np.size(distancelist), 0, distancelist.max()*1.1])
plt.grid(True)
plt.show()

# Plot a histogram of the distances. We can easily see if there is some point
# clearly outside the bulk of the distribution
numbins = 100
plt.hist(distancelist, numbins)
plt.xlabel("Hamming distance")
plt.ylabel("Distribution")
plt.title("Block size " + str(keylength) + " bytes")
plt.grid(True)
plt.show()

# Let's focus now on the relevant ciphertext
ciphertext = cipherlist[distancelist.argmin()]

# Break the ciphertext in blocks of lengh equal to the lengh of the key and put
# it in matrix form.
padding, blocklist = matasanolib.partstr(ciphertext, 'hex', keylength)
for block in blocklist:
	print(block)