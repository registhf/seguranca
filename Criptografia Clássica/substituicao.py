import numpy as np
import copy

def substituicao(textBytes, seed=1):
	np.random.seed(seed)
	
	a = [i for i in range(256)]
	b = copy.copy(a)
	np.random.shuffle(b)

	r = []
	for c in textBytes:
		r.append(b[a.index(c)])

	return r
	

def desubstituicao(textBytes, seed=1):
	np.random.seed(seed)
	
	a = [i for i in range(256)]
	b = copy.copy(a)
	np.random.shuffle(b)

	r = []
	for c in textBytes:
		r.append(a[b.index(c)])

	return r