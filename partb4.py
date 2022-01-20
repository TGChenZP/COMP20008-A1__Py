## Part B Task 4
import re
import pandas as pd
import os
import nltk
import argparse
from nltk.stem.porter import *

#create a parser to collect keywords from command line into a list. the 2nd to 5th are optional arguments
parser = argparse.ArgumentParser()
parser.add_argument('keyword1', type=str)
parser.add_argument("keyword2", nargs="?", default="", type=str)
parser.add_argument("keyword3", nargs="?", default="", type=str)
parser.add_argument("keyword4", nargs="?", default="", type=str)
parser.add_argument("keyword5", nargs="?", default="", type=str)

args = parser.parse_args()

keywords = [args.keyword1, args.keyword2, args.keyword3, args.keyword4, args.keyword5]
keywords = [x.lower() for x in keywords]

#a helper function to process the text, first changing the whole text to lower case, then remove all punctuations and numbers, finally turn all \t and \n into spaces.
def processing(text):
    text = text.lower()

    regex = re.compile('[^a-zA-Z \\t\\n]')
    text = regex.sub(' ', text)

    regex = re.compile('[^a-zA-Z]')
    text = regex.sub(' ', text)
    
    return text

#initiate porter stemmer
porterStemmer = PorterStemmer()

#a helper function which uses porterstemmer on each word in the argument, and returns a list of stemmed words
def stem(wordlist):
    stemlist = list()
    for word in wordlist:
        StemWord = porterStemmer.stem(word)
        stemlist.append(StemWord)
    
    return stemlist

#read the output from partb1 to get a dataframe of filenames and their documentIDs
filesdf = pd.read_csv('partb1.csv')
filess = list(filesdf['filename'])
fileIDs = list(filesdf['documentID'])

#change directory so can open the files
os.chdir("./cricket")

#apply stemming to the keywords too as per requirement of the assignment
keywords = stem(keywords)
out = list()

#for each file process the text and then split it into a wordlist, then apply porterstemmer to each of the words and put them into a new wordlist, then see if each of the stemmed keywords exist in the new wordlist. If one of the stemmed keywords do not exist then that file will not be returned. Else the documentIDs will be added to a list which will be printed out as per the instructions 
for i in range(len(filess)):
    file = open(filess[i], "r")
    text = file.read()
    file.close()
    textlist = processing(text)
    textlist = textlist.split()
    
    stemlist = stem(textlist)
    stemlist.append("")
    #this is added in case there aren't 5 keywords which means "" will be recorded as keyword and hence the wordlist must       also have an empty string so no false negatives occur.
    
    inside = 1
    
    for keyword in keywords:
        if keyword not in stemlist:
            inside = 0
            break
    
    if inside:
        out.append(fileIDs[i])

#print out each item in list
for documentid in out:
    print(documentid)