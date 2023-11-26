import argparse
import re
import pathlib

filename = "filename"
parser = argparse.ArgumentParser(
    prog='Word usage',
    description='The program prints the analysis of words used in assay',
    epilog='That\'s all')
parser.add_argument("-m", "--most-used-first", action='store_true', help="Most used words will be printed first")
parser.add_argument("-s", "--short-first", action='store_true', help="Shortest words will be printed first")
parser.add_argument("-a", "--alphabet", action='store_true', help="Print words in alphabetical order")
parser.add_argument("filename", help="Full path to the essay text file")

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
    printPretty(dict(sorted(dic.items(), key= lambda word: len(word[0]))))
if (arguments.most_used_first):
    print(dic.items())
    printPretty(dict(sorted(dic.items(), key=lambda x: x[1], reverse=True)))

