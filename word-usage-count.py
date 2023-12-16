import argparse
import pathlib
import re
import os
from functools import cmp_to_key
from docx import Document

filename = "filename"
parser = argparse.ArgumentParser(
    prog='Word usage',
    description='The program prints the analysis of words used in assay',
    epilog='That\'s all')
parser.add_argument("-m", "--most-used-first", action='store_true', help="Most used words will be printed first")
parser.add_argument("-s", "--short-first", action='store_true', help="Shortest words will be printed first")
parser.add_argument("-a", "--alphabet", action='store_true', help="Print words in alphabetical order")
parser.add_argument("filename", help="Full path to the essay text file")

common_ignore = {'the', 'to', 'of', 'and', 'in', 'that', 'are', 'this', 'they'}


def alphabet_comparator(x, y):
    if x > y:
        return 1
    elif x < y:
        return -1
    else:
        return 0


def len_comparator(x, y):
    wordX = x[0]
    wordY = y[0]
    if len(wordX) > len(wordY):
        return 1
    elif len(wordX) < len(wordY):
        return -1
    else:
        return alphabet_comparator(wordX, wordY)


def printPretty(dictionary):
    print("{:<8} {:<15}".format('Count', 'Word'))
    for k, v in dictionary.items():
        print("{:<8} {:<15}".format(v, k))


def is_meta_start(line):
    return '<--' in line


def is_meta_end(line):
    return '-->' in line


class Essay:
    meta = ''
    dic = {}

    def get_meta(self):
        return self.meta

    def get_dic(self):
        return self.dic

    def __init__(self, filePath):
        self.filePath = filePath

    def parseFile(self):
        if (self.filePath.suffix == '.txt'):
            self.parseTextFile()
        else:
            self.parseDocxFile()

    def extractMeta(self):
        pass

    def parseTextFile(self):
        is_meta = False
        with open(self.filePath) as file:
            for l in file:
                if is_meta_start(l):
                    is_meta = True
                    continue
                if is_meta_end(l):
                    is_meta = False
                if is_meta:
                    self.meta += l
                    continue
                words = list(filter(None, re.split('\W', l)))
                for w in words:
                    lc = w.lower()
                    if lc in self.dic:
                        self.dic[lc] = self.dic[lc] + 1
                    else:
                        self.dic[lc] = 1

    def parseDocxFile(self):
        is_meta = False
        doc = Document(self.filePath)
        for l in doc.paragraphs:
            if is_meta_start(l.text):
                is_meta = True
                continue
            if is_meta_end(l.text):
                is_meta = False
            if is_meta:
                self.meta += l.text
                continue
            words = list(filter(None, re.split('\W', l.text)))
            for w in words:
                lc = w.lower()
                if lc in self.dic:
                    self.dic[lc] = self.dic[lc] + 1
                else:
                    self.dic[lc] = 1


arguments = parser.parse_args()
essayPath = pathlib.Path(arguments.filename)
essayAnalysis = Essay(essayPath)
essayAnalysis.parseFile()
if (arguments.short_first):
    printPretty(dict(sorted(essayAnalysis.get_dic().items(), key=cmp_to_key(len_comparator))))
if (arguments.most_used_first):
    printPretty(dict(sorted(essayAnalysis.get_dic().items(), key=lambda x: x[1], reverse=True)))
if (arguments.alphabet):
    printPretty(dict(sorted(essayAnalysis.get_dic().items(), key=lambda x: x[0])))
