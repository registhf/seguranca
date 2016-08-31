import numpy as np
import copy

def substituicao(textBytes, key):	
	a = [i for i in range(256)]
	
	r = []
	for c in textBytes:
		r.append(key[a.index(c)])

	return r
	

def desubstituicao(textBytes, key):	
	a = [i for i in range(256)]
	
	r = []
	for c in textBytes:
		r.append(a[key.index(c)])

	return r