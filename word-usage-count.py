import argparse
import re
import pathlib
from functools import cmp_to_key

filename = "filename"
parser = argparse.ArgumentParser(
    prog='Word usage',
    description='The program prints the analysis of words used in assay',
    epilog='That\'s all')
parser.add_argument("-m", "--most-used-first", action='store_true', help="Most used words will be printed first")
parser.add_argument("-s", "--short-first", action='store_true', help="Shortest words will be printed first")
parser.add_argument("-a", "--alphabet", action='store_true', help="Print words in alphabetical order")
parser.add_argument("filename", help="Full path to the essay text file")


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


dic = {}
arguments = parser.parse_args()
print(arguments)
print(arguments.short_first)
print(arguments.alphabet)
essay = pathlib.Path(arguments.filename)
with open(essay) as file:
    for l in file:
        words = list(filter(None, re.split('\W', l)))
        for w in words:
            lc = w.lower()
            if lc in dic:
                dic[lc] = dic[lc] + 1
            else:
                dic[lc] = 1

if (arguments.short_first):
    printPretty(dict(sorted(dic.items(), key=cmp_to_key(len_comparator))))
if (arguments.most_used_first):
    printPretty(dict(sorted(dic.items(), key=lambda x: x[1], reverse=True)))
if (arguments.alphabet):
    printPretty(dict(sorted(dic.items(), key=lambda x: x[0])))
