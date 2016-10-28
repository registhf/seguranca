from os import listdir
from os.path import isfile, exists
import re


class dictFromFiles:
    folder = ''
    dictionary = None

    def __init__(self, folder=None):
        if folder and not folder.endswith('/'):
            folder += '/'
        self.folder = folder
        self.dictionary = set([])


    def __loadDictFromCache(self, output):
        with open(output) as f:
            dic = f.read()
            self.dictionary = set(dic.split('\n'))
            print('\rDictionary length:', len(self.dictionary), 'loaded from cache', end="")


    def __loadDictFromFiles(self):
        files = sorted(listdir(self.folder))
        cnt = 1
        for ifile in files:
            if not isfile(self.folder + ifile):
                continue
            with open(self.folder + ifile, 'rb') as f:
                while 1:
                    text = f.readline()
                    if not text:
                        break
                    self.process(text)
                
                print('\rDictionary length:', len(self.dictionary), end=" | ")
                print(str(cnt) + '/' + str(len(files)), 'files', end="")
                cnt += 1


    def build(self, output=None):
        if exists(output):
            self.__loadDictFromCache(output)
        else:
            self.__loadDictFromFiles()
            if not output is None:
                with open(output, 'w') as o:
                    o.write('\n'.join(self.dictionary))

        print('...OK')
        return self.dictionary

    
    def process(self, text):
        try:
            words = re.findall(r"[^\n <>=/\+;_\-\t\(\)%'\.\"`]+", text.decode() if type(text[0]) == int else text)
            self.dictionary = self.dictionary.union(set(words))
        except UnicodeDecodeError:
            pass
        
        return self.dictionary


    def countEquals(self, otherDict):
        return len(self.dictionary.intersection(otherDict))


if __name__ == '__main__':
    d = dictFromFiles('testcases/inputs/')
    d.build('dict.txt')
