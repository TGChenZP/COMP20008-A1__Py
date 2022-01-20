#PART 1

import pandas as pd
import argparse
import math as m

#reading the data straight from the web source
data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')

#deleting all 2021 values - first compile their indicies and then use .drop to remove them all
nextyear=list()
for i in range(len(data['date'])):
    if data['date'][i][0:4] == '2021':
        nextyear.append(i)
data = data.drop(labels=nextyear)

#reset the index after removal to unify. No real use - just for aesthetics
data.index = range(0, len(data['continent']))

#manipulate the date column to create a month column (basically the new month column is removing the day from each row's 'date' column)
data['monthnum1'] = [x.split("-")[0:2] for x in data['date']]
data['month'] = [(x[0] + "-" + x[1]) for x in data['monthnum1']]

data1 = data.loc[:,['location', 'month', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']]

#preparing a dictionary detailing operations for the agg function. For 'total's, just have to look at last value of the month while for 'new's, need to look at sum of all
operations = {'total_cases': 'last', 'new_cases': lambda a:a.sum(min_count=1), 'total_deaths': 'last', 'new_deaths': lambda a:a.sum(min_count=1)}
#first cut them up via groupby and then put them back togehter - whole dataframes now one row only.
out = data1.groupby(["location", "month"]).agg(operations)
#PART ONE NOW COMPLETE - THE REQUIRED DATAFRAME IS CONTAINED IN THE VARIABLE 'out'


#PART 2

case_fatality_rate = list()

#strictly abiding to the important instructions of "do not impute missing values", if either of the new_deaths or new_cases reported nan then the case_fatality rate would return nan. The possibility of the denominator equal to 0 was also considered and if occurs will also report nan.
for i in range(len(list(out['new_deaths']))):
    if (list(out['new_deaths'])[i] == m.nan) or (list(out['new_cases'])[i] == m.nan) or (list(out['new_cases'])[i] == 0):
        case_fatality_rate.append(m.nan)
    else:
        case_fatality_rate.append(list(out['new_deaths'])[i]/list(out['new_cases'])[i])

#adding a new column to the dataframe and shuffling it to match the order as required by the instructions 
out['case_fatality_rate'] = case_fatality_rate

cols = out.columns.tolist()
cols = cols[-1:] + cols[:-1]
out = out[cols]

#print first five lines to stdout, as per instructions
print(out.head())

#read in the command line to yield the output file.
parser = argparse.ArgumentParser()
parser.add_argument('outfile', type=str)
args=parser.parse_args()

out.to_csv(args.outfile)