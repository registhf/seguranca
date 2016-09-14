import sys
import numpy as np
from ceasar import ceasar, deceasar
from vigenere import vigenere, devigenere
from transposicao import transposicao, detransposicao
from substituicao import substituicao, desubstituicao

from os import listdir
from os.path import isfile

def readbytes(file):
	return np.array([b for b in open(file, 'rb').read()])

total = 0

ceasar_ok = 0
ceasar_total = 0

vig_ok = 0
vig_total = 0

transp_ok = 0
transp_total = 0

subs_ok = 0
subs_total = 0

testfiles = listdir('testcases/outputs')

inputfiles = {}
for ifile in listdir('testcases/inputs'):
	inputfiles[ifile[0]] = readbytes('testcases/inputs/' + ifile)


for ofile in testfiles:
	total += 1
	N, name, cipher, key = ofile.split('.')
	
	if key.startswith('key'):
		key = open('testcases/' + key, 'rb').read()

	inputfile = inputfiles[N]
	outputfile = readbytes('testcases/outputs/' + ofile)

	enc = ''
	if cipher == 'ceasar':
		ceasar_total += 1
		if key == 'X' or key == 'Y':
			print('Procurando chave do arquivo (Tem que achar: ', outputfile[0]-inputfile[0],')', ofile, '...', end="")
			sys.stdout.flush()
			for key in range(256):
				enc = ceasar(inputfile, key)
				if np.array(enc == outputfile).mean() == 1:
					print('Chave descoberta =', key)
					ceasar_ok += 1
					break
		else:
			enc = ceasar(inputfile, int(key))
			ceasar_ok += (np.array(enc == outputfile).mean() == 1)

	elif cipher == 'vig':
		vig_total += 1
		if key == 'X' or key == 'Y':
			print('Procurando chave do arquivo', ofile, '...', end="")
			sys.stdout.flush()
			sub = np.array(outputfile - inputfile)
			for k in range(1, 30):
				sys.stdout.flush()
				candidate = sub[0:k]
				full = np.array([int(x) for x in ((",".join(str(x) + ',' for x in candidate)) * (int(len(sub)/k)+1)).split(',') if len(x) > 0])[0:len(sub)]
				compare = np.array(full == sub)
				if 1-compare.mean() < 10**-2:
					print('Chave descoberta = ', "".join([chr(x) for x in candidate]))
					vig_ok += 1
					enc = vigenere(inputfile, candidate)
					break
		else:
			enc = vigenere(inputfile, key.encode('ascii'))
			vig_ok += (np.array(enc == outputfile).mean() == 1)

	elif cipher == 'transp':
		transp_total += 1
		if key == 'X' or key == 'Y':
			print('Procurando chave do arquivo', ofile, '...', end="")
			sys.stdout.flush()
			for key in range(1, 256):
				enc = transposicao(inputfile, int(key))
				if np.array(enc == outputfile).mean() == 1:
					print('Chave descoberta =', key)
					transp_ok += 1
					break
		else:
			enc = transposicao(inputfile, int(key))
			transp_ok += (np.array(enc == outputfile).mean() == 1)

	elif cipher == 'subs':
		if key == 'X' or key == 'Y':
			continue
		subs_total += 1
		enc = substituicao(inputfile, key)
		subs_ok += (np.array(enc == outputfile).mean() == 1)
	
	if np.array(enc == outputfile).mean() != 1:
		print('\nFalha no arquivo: ', ofile, '\n')	



print('\r',' '*100,'\r', end="")
print('Sucesso Ceasar:\t\t', ceasar_ok, '\t/', ceasar_total)
print('Sucesso Vigenere:\t', vig_ok, '\t/', vig_total)
print('Sucesso Transposição:\t', transp_ok, '\t/', transp_total)
print('Sucesso Substituição:\t', subs_ok, '\t/', subs_total)