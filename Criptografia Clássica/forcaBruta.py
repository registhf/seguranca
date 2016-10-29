import numpy as np
import operator
from os import listdir
from os.path import isfile
from dictionary import dictFromFiles
from ceasar import deceasar
from vigenere import devigenere
from transposicao import detransposicao
from time import time


inputsfolder = 'testcases/inputs/'
ouputsfolder = 'testcases/outputs/'

def readbytes(file, cipher):
    return np.array(
        [b for b in open(file, 'rb').read(550 if cipher != 'transp' else None)]
    )


GLOBAL_DICT = dictFromFiles(inputsfolder)
dictionary = GLOBAL_DICT.build('forcaBrutaDict.txt')

testfiles = sorted(listdir(ouputsfolder))

total = 0
for ofile in testfiles:
    path = ouputsfolder + ofile
    if not isfile(path):
        continue
    
    start = time()
    total += 1
    N, name, cipher, key = ofile.split('.')
    
    outputfile = readbytes(path, cipher)

    if cipher not in ['vig', 'ceasar', 'transp']: continue
    
    print('File:', '...' + path[-20:], end="\t| ")
    
    ranking = {}
    if cipher == 'ceasar':    
        for k in range(0, 256):
            enc = deceasar(outputfile, k)
            text = ''.join([chr(a) for a in enc])
            
            testDict = dictFromFiles()
            encDict = testDict.process(text)

            ranking[k] = GLOBAL_DICT.countEquals(encDict)    
            
    elif cipher == 'vig':
        with open('vigDict.keys') as v:
            vigKeys = set(v.read().split('\n'))
            combo = set()
            for v in vigKeys:
                for u in vigKeys:
                    if v == u: continue
                    combo.add(v+u)
            vigKeys = vigKeys.union(combo)

        for k in vigKeys:
            enc = devigenere(outputfile, [int(a) for a in k.encode()])

            text = ''.join([chr(a) for a in enc])
        
            testDict = dictFromFiles()
            encDict = testDict.process(text)

            ranking[k] = GLOBAL_DICT.countEquals(encDict)

    elif cipher == 'transp':
        for k in range(1, 256):
            enc = detransposicao(outputfile, k)
            text = ''.join([chr(a) for a in enc])
            
            testDict = dictFromFiles()
            encDict = testDict.process(text)

            ranking[k] = GLOBAL_DICT.countEquals(encDict) 

            
    s = sorted(ranking.items(), key=operator.itemgetter(1))
        
    percent = str(round(s[-1][1]/len(GLOBAL_DICT.dictionary)*100, 3))
    elapsed = str(round((time()-start), 3)) + 's'
    
    print('Most likely key:', str(s[-1][0]), ' ' * (15-len(str(s[-1][0]))), end="")
    print(percent + '%', ' ' * (8-len(percent)), '| time:', ' ' * (9-len(elapsed)), elapsed)