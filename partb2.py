# Part B Task 2
import re
import os
import nltk
import argparse

#change directory to cricket folder so program can open relevent files
os.chdir("./cricket")

#setup the parser to receive the filename to open
parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)
args=parser.parse_args()

#because the input will be cricketxxx.txt rather than xxx.txt, the filename will have to be sliced
file = open(args.infile[-7:], "r")
text = file.read()
file.close()

#a helper function to process the text, first changing the whole text to lower case, then remove all punctuations and numbers, finally turn all \t and \n into spaces.
def processing(text):
    text = text.lower()

    regex = re.compile('[^a-zA-Z \\t\\n]')
    text = regex.sub(' ', text)

    regex = re.compile('[^a-zA-Z]')
    text = regex.sub(' ', text)
    
    return text

#apply the helper function to the textfile that has been opened as according to the command line argument
text = processing(text)

#split the text into a list of individual words and then print out
WordList = nltk.word_tokenize(text)

#print out each word in list
for word in WordList:
    print(word)