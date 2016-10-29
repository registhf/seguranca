import numpy as np
import operator
import sys
from os import listdir
from os.path import isfile
from dictionary import dictFromFiles
from ceasar import deceasar
from vigenere import devigenere


inputsfolder = 'testcases/inputs/'
ouputsfolder = 'testcases/outputs/'

def readbytes(file):
    bytes_len = 100 if len(sys.argv) < 2 else int(sys.argv[1])
    return np.array([b for b in open(file, 'rb').read(bytes_len)])


GLOBAL_DICT = dictFromFiles(inputsfolder)
dictionary = GLOBAL_DICT.build('forcaBrutaDict.txt')

testfiles = listdir(ouputsfolder)

total = 0
for ofile in testfiles:
    path = ouputsfolder + ofile
    if not isfile(path):
        continue
    
    outputfile = readbytes(path)
    total += 1
    N, name, cipher, key = ofile.split('.')

    if cipher not in ['vig', 'ceasar']: continue
    
    print('File:', '...' + path[-20:], end="\t| ")
    
    ranking = {}
    if cipher == 'ceasar':    
        for k in range(0, 256):
            enc = deceasar(outputfile, k)
            text = ''.join([chr(a) for a in enc])
            
            testDict = dictFromFiles()
            encDict = testDict.process(text)

            ranking[k] = GLOBAL_DICT.countEquals(encDict)    
            
        s = sorted(ranking.items(), key=operator.itemgetter(1))

        print('Most likely key:', str(s[-1][0]), ' ' * (12-len(str(s[-1][0]))), '\t: ', end="")
        print(str(round(s[-1][1]/len(GLOBAL_DICT.dictionary)*100, 3)) + '%')

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
            
        s = sorted(ranking.items(), key=operator.itemgetter(1))
            
        print('Most likely key:', str(s[-1][0]), ' ' * (12-len(str(s[-1][0]))), '\t: ', end="")
        print(str(round(s[-1][1]/len(GLOBAL_DICT.dictionary)*100, 3)) + '%')