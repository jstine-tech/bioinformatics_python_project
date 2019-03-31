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
        keys = re.findall(r'<1>[A-z]*', rebaseData.read())
        values = re.finadall(r'<5>[A-z\^\?]*', rebaseData.read())
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





