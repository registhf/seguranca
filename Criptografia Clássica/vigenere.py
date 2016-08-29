import sys
import numpy as np

def vigenere(textBytes, keys=[]):
	k = 0
	r = []
	for b in textBytes:
		r.append((b + 256 + keys[k]) % 256)
		k = k+1 if k+1 < len(keys) else 0
	return r

def devigenere(textBytes, keys=[]):
	k = 0
	r = []
	for b in textBytes:
		r.append((b + 256 - keys[k]) % 256)
		k = k+1 if k+1 < len(keys) else 0
	return r