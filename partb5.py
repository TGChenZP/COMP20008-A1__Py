#Part B Task 5
import re
import pandas as pd
import os
import nltk
import argparse
import math as m
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfTransformer

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

#setup porter stemmer
porterStemmer = PorterStemmer()

#helper function to change a list of words into a list of these words but stemmed
def stem(wordlist):
    stemlist = list()
    for word in wordlist:
        StemWord = porterStemmer.stem(word)
        stemlist.append(StemWord)
    
    return stemlist

#read output from partb1 and extract columns as lists
filesdf = pd.read_csv('partb1.csv')
filess = list(filesdf['filename'])
fileIDs = list(filesdf['documentID'])

os.chdir("./cricket")

#apply the stem function on the list of keywords
keywords = stem(keywords)

#implement the same steps as task 4, except this time also collecting a list of the file names that match the requirement, and also a set of all stemmed words in documents in which the key words appears in 
filteredfiles = list()
filteredIDs = list()
tfidflist = set()

for i in range(len(filess)):
    file = open(filess[i], "r")
    text = file.read()
    file.close()
    textlist = processing(text)
    textlist = textlist.split()
    
    stemlist = stem(textlist)
    stemlist.append("")
    
    inside = 1

    for keyword in keywords:
        if keyword not in stemlist:
            inside = 0
            break

    if inside:
        filteredfiles.append(filess[i])
        filteredIDs.append(fileIDs[i])
        for word in stemlist:
            #appended '' to list before, now remove it to prevent affecting final score
            if word != '':
                tfidflist.add(word)

#one of the required items to be printed out
print("documentID score")
                
#special tester in case there were no files that matched, without which if no files were matched then the tfidf module would run into an error             
if len(filteredfiles) != 0:
    tfidflist = list(tfidflist)
    
    #for every matching file collected before, open it again and then construct a tally for the occurence of each word,         which later gets changed into a list and has tfidf applied to it.
    countlist = list()
    for file in filteredfiles:
        file = open(file, "r")
        text = file.read()
        file.close()
        textlist = processing(text)
        textlist = textlist.split()

        stemlist = stem(textlist)

        temp = dict()
        for word in tfidflist:    #first initiate the tally with all words that appeared in all matching documents
            temp[word] = 0
        for word in stemlist:    #then tally
            temp[word] += 1
       
        #finally change it into a list of values which gets appended to another list which gets tfidf applied to it
        countlist.append(list(temp.values()))    
    
    #setup tfidf
    transformer = TfidfTransformer()
    
    #apply tfidf to the list of lists, now each is a vector of the document
    tfidf = transformer.fit_transform(countlist)
    tfidf = tfidf.toarray()
    
    #setup the query vector by again tallying and then tfidf
    keys = dict()
    for word in tfidflist:
        keys[word] = 0
    for word in keywords:
        #if there were less than 5 keywords then there would be keywords with value '', which need to be removed to not             affect final score
        if word != '':    
            keys[word] += 1
    keys = list(keys.values())
    keys = [x/(m.sqrt(sum([y**2 for y in keys]))) for x in keys]
    
    #helper function to calculate cosine similarity for a whole list, returning a list containing cosine similarity scores     for all documents
    def cos_sim(og, comparisons):
        cos_out = list()
        for tfidflist in comparisons:
            dot = 0
            x1 = 0
            x2 = 0
            for i in range(len(tfidflist)):
                dot += og[i] * tfidflist[i]
                x1 += (og[i])**2
                x2 += (tfidflist[i])**2
            result = dot/(x1*x2)
            cos_out.append(result)
        return cos_out

    #apply this function onto our list
    out = cos_sim(keys, tfidf)
    
    #sort the list and then print out
    sortinglist = list()
    for i in range(len(out)):
        temp = (out[i], filteredIDs[i])
        sortinglist.append(temp)
    sortinglist = sorted(sortinglist, reverse=True)

    for pair in sortinglist:
        print(f"{pair[1]:<9} {pair[0]:.4f}")