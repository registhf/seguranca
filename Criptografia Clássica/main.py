import sys
import numpy as np
from ceasar import ceasar, deceasar
from vigenere import vigenere, devigenere
from transposicao import transposicao, detransposicao
from substituicao import substituicao, desubstituicao

if len(sys.argv) < 3:
	print('USE: python main.py file.txt N')
	exit(0)

k = int(sys.argv[2])
textBytes = np.array([b for b in open(sys.argv[1], 'rb').read()])


print('-- Ceasar:')
c = ceasar(textBytes, k)
dc = deceasar(c, k)
print('' . join(chr(i) for i in c))
print('' . join(chr(i) for i in dc))


print('\n-- Vigenere:')
v = vigenere(textBytes, [k, k+1])
dv = devigenere(v, [k, k+1])
print('' . join(chr(i) for i in v))
print('' . join(chr(i) for i in dv))


print('\n-- Transposição:')
t = transposicao(textBytes, k)
dt = detransposicao(t, k)
print('' . join(chr(i) for i in t))
print('' . join(chr(i) for i in dt))


# O k passado aqui é a seed do np.random, usado para gerar
# o alfabeto para a substituição
print('\n-- Substituição:')
s = substituicao(textBytes, k)
ds = desubstituicao(s, k)
print('' . join(chr(i) for i in s))
print('' . join(chr(i) for i in ds))