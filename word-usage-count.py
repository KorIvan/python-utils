import argparse
import pathlib
import os
import re
import textwrap
from functools import cmp_to_key
from docx import Document

FORMAT = "{:<6}{:<24}"
FORMAT_LENGTH = 30

FILENAME = "filename"
parser = argparse.ArgumentParser(
    prog='Word usage',
    description='The program prints the analysis of words used in assay',
    epilog='That\'s all')
parser.add_argument("-m", "--most-used-first", action='store_true', help="Most used words will be printed first")
parser.add_argument("-s", "--short-first", action='store_true', help="Shortest words will be printed first")
parser.add_argument("-a", "--alphabet", action='store_true', help="Print words in alphabetical order")
parser.add_argument("filename", help="Full path to the essay text file")

common_ignore = {'the', 'to', 'of', 'and', 'in', 'that', 'are', 'this', 'they'}


def calculate_window_width():
    try:
        return os.get_terminal_size().columns
    except IOError:
        print("Unable to adjust word wrap for terminal simulators")
        return FORMAT_LENGTH * 3


WINDOW_WIDTH = calculate_window_width()


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


def append_to_dict(i, dic, k, v):
    if i in dic:
        dic[i] += FORMAT.format(v, k)
    else:
        dic[i] = FORMAT.format(v, k)


def printPretty(dictionary):
    header = FORMAT.format('Count', 'Word')
    columns = WINDOW_WIDTH // FORMAT_LENGTH  # a single column width
    rows = len(dictionary) // columns
    wide_header = ''
    for i in range(columns):
        wide_header += header
    print(wide_header)
    total = len(dictionary)
    i = 0
    print_dic = {}
    for k, v in dictionary.items():
        append_to_dict(i, print_dic, k, v)
        if i < rows:
            i += 1
        else:
            i = 0
    for line in print_dic.values():
        print(line)


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

    def is_meta(self, paragraph):
        if paragraph.runs[0].italic:
            return True
        return False

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
        is_meta_done = False
        doc = Document(self.filePath)
        for l in doc.paragraphs:
            if self.is_meta(l):
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
print(textwrap.fill(essayAnalysis.get_meta(), WINDOW_WIDTH))
print("Total word count:", sum(essayAnalysis.get_dic().values()))
if arguments.short_first:
    printPretty(dict(sorted(essayAnalysis.get_dic().items(), key=cmp_to_key(len_comparator))))
if arguments.most_used_first:
    printPretty(dict(sorted(essayAnalysis.get_dic().items(), key=lambda x: x[1], reverse=True)))
if arguments.alphabet:
    printPretty(dict(sorted(essayAnalysis.get_dic().items(), key=lambda x: x[0])))
