import re
import sys


class Rebase:
    def makeRe(self, sequence):
        makeReDict = {'A': 'A', 'T': 'T', 'G': 'G', 'C': 'C', 'R': '[GA]', 'Y': '[CT]', 'M': '[AC]', 'K': '[GT]',
                           'S': '[GC]', 'W': '[AT]', 'B': '[CGT]', 'D': '[AGT]', 'H': '[ACT]', 'V': '[ACG]',
                           'N': '[ACGT]', '?': '', '^': ''}
        expression = ''
        for char in sequence:
            expression = expression + makeReDict[char]
        return expression

    def __init__(self):
        tempDictionary = {}
        rebaseData = open('link_allenz.txt')
        keys = re.findall(r'<1>[A-z.0-9]*', rebaseData.read())
        index = 0
        for key in keys:
            keys[index] = key.split('<1>')[1]
            index = index + 1
        rebaseData.seek(0, 0)
        values = re.findall(r'<5>[A-Z\^\?]*', rebaseData.read())
        index = 0
        for value in values:
            values[index] = value.split('<5>')[1]
            index = index + 1
        index = 0
        for value in values:
            tempDictionary[keys[index]] = self.makeRe(value)
            index = index + 1
        self.dictionary = {key: value for key, value in tempDictionary.items() if value is not ''} #remove enzymes with recognition sequence '?'
        rebaseData.close()

    def locateEnzyme(self, enzyme, strand):
        occurrences = []
        regRecognition = self.dictionary[enzyme]
        regular = re.compile(regRecognition)
        match = regular.search(strand)
        while match != None:
            occurrences.append([match.start(), match.end()])
            match = regular.search(strand, match.end())
        return occurrences

    def findAllEnzymes(self, strand):
        enzymes = []
        for key in self.dictionary:
            locations = self.locateEnzyme(key, strand)
            if locations != []:
                enzymes.append(key)
        return enzymes


reb = Rebase()
strand = sys.argv[1]
results = reb.findAllEnzymes(strand)
for result in results:
    print(result)
