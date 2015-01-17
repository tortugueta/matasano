# -*- coding: utf-8 -*-

# The matasano cryptography challeges
# Set 1 / Challenge 7
# AES in ECB mode

# Imports
import sys
sys.path.append("/home/joan/Programming/the matasano cryptography challenges/")
import matasanolib
import numpy as np
from Crypto.Cipher import AES

key = "YELLOW SUBMARINE" # Clau de 16 caràcers, és a dir 128 bits

# Llegim l'arxiu encriptat
filepath = "/home/joan/Programming/the matasano cryptography challenges/" + \
	"set1.challenge7.encrypted.txt"
filehandler = open(filepath, "r")
b64str = ""
for line in filehandler:
	b64str += line.strip()
# print(b64str)

# Hem de convertir aquesta cadena base 64 en ascii, perquè la funció de
# desencriptar espera una cadena ascii com a input. Recordem que cada 4
# caràcters base 64 corresponen a 3 caràcters ascii. Assumim que la cadena
# té el padding adequat (podem comprovar que la longitud és divisible per 4)
blocklst = [b64str[i:i+4] for i in range(0, len(b64str), 4)]
blocklst = [matasanolib.b64toint(block) for block in blocklst]
blocklst = ['%06x' % block for block in blocklst]
asciistr = ""
for block in blocklst:
	asciistr += chr(int(block[0:2], base=16)) + \
		chr(int(block[2:4], base=16)) + \
		chr(int(block[4:6], base=16))
# print(asciistr)

# Generem el cipher
cipher = AES.new(key, AES.MODE_ECB)

# Desencriptem
plaintxt = cipher.decrypt(asciistr)
print(plaintxt)