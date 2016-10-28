from os import listdir
from os.path import isfile
from dictionary import dictFromFiles
import numpy as np
import operator
from ceasar import ceasar

inputsfolder = 'testcases/inputs/'
ouputsfolder = 'testcases/outputs/'

def readbytes(file):
    return np.array([b for b in open(file, 'rb').read(50)])

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
    
    if cipher == 'ceasar':
        print('Breaking:', path, end="\t| ")
        
        ranking = {}
        for k in range(0, 256):
            enc = ceasar(outputfile, k)
            text = ''.join([chr(a) for a in enc])
            
            testDict = dictFromFiles()
            encDict = testDict.process(text)

            ranking[k] = GLOBAL_DICT.countEquals(encDict)

        s = sorted(ranking.items(), key=operator.itemgetter(1))
        
        print('Most likely key:', str(256-s[-1][0]) + ',', '\t: ', end="")
        print(str(round(s[-1][1]/len(GLOBAL_DICT.dictionary)*100, 3)) + '%')
