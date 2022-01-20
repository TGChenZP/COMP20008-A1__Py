## Part B Task 1

import re
import pandas as pd
import os
import argparse

#change directory to cricket file to access txt files
os.chdir("./cricket")

#get a list of directory and sort them (to make sure later on they are inputted into dataframe in sorted order)
ls = (os.listdir())
ls = sorted(ls)

#setup the regex pattern to match and return the IDs. Assumes Greedy search.
pattern = r'[a-zA-Z]{4}-\d{3}[a-zA-Z]?'

#read all relevent files in the directory and append their document name and document id to separate lists
filenames = list()
docID = list()
for i in ls:
    if i[-4:] == ".txt" and i[:3].isdigit() and len(i) == 7:        #in case there are other files in the directory
        file = open(i, 'r')
        text = file.read()
        file.close()
        filenames.append(i)
        ID = re.findall(pattern, text)
        docID.append(ID[0])

#create a dataframe using the two lists        
out = pd.DataFrame({"filename": filenames, "documentID": docID})
out = out.set_index('filename')

#change directory back out to parent (origin) to save output file to there
os.chdir("..")

#setup the parser and save the csv file to variable name
parser = argparse.ArgumentParser()
parser.add_argument('outfile', type=str)
args=parser.parse_args()

out.to_csv(args.outfile)