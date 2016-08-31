import numpy as np

def transposicao(textBytes, k):
	m = []
	n = 0
	l = np.zeros(k).astype(int)
	for b in textBytes:
		if n < k:
			l[n] = b
			n += 1
		else:
			m.append(l)
			l = np.zeros(k).astype(int)
			l[0] = b
			n = 1
	
	m.append(l)
	r = []
	for l in np.array(m).T:
		for c in l:
			r.append(c)
	return np.array(r)


def detransposicao(textBytes, k):
	k = int(len(textBytes)/k)
	m = []
	n = 0
	l = np.zeros(k).astype(int)
	for b in textBytes:
		if n < k:
			l[n] = b
			n += 1
		else:
			m.append(l)
			l = np.zeros(k).astype(int)
			l[0] = b
			n = 1
	
	m.append(l)
	r = []
	for l in np.array(m).T:
		for c in l:
			r.append(c)
	return np.array(r)
