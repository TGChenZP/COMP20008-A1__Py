#PART 1

import matplotlib.pyplot as plt
import pandas as pd
import argparse
import math as m

#setup parser to read command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('outfile1', type=str)
parser.add_argument('outfile2', type=str)
args=parser.parse_args()

#read data from the server again - would have liked to use csv output from part 1 but no guarentee of testing order
data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')

#deleting all 2021 values - first compile their indicies and then use .drop to remove them all
nextyear=list()
for i in range(len(data['date'])):
    if data['date'][i][0:4] == '2021':
        nextyear.append(i)
data = data.drop(labels=nextyear)

#using groupby to turn all the data into one row per location (similar code to part 1)
operations = {'total_cases': 'last', 'new_cases': lambda a:a.sum(min_count=1), 'total_deaths': 'last', 'new_deaths': lambda a:a.sum(min_count=1)}
out = data.groupby(["location"]).agg(operations)

#calculating the case fatality rate of each location in year 2020 and adding it to the dataframe
case_fatality_rate = list()
for i in range(len(list(out['new_deaths']))):
    if (list(out['new_deaths'])[i] == m.nan) or (list(out['new_cases'])[i] == m.nan) or (list(out['new_cases'])[i] == 0):
        case_fatality_rate.append(m.nan)
    else:
        case_fatality_rate.append(list(out['new_deaths'])[i]/list(out['new_cases'])[i])
        
out['case_fatality_rate'] = case_fatality_rate

#creating a column called colour where each location gets a different colour assigned to it - for scatter plot purposes later
locat = list(out['new_deaths'])

colour = list()
for i in range(len(locat)):
    colour.append((i)/len(locat))

out['color'] = colour

#plot the first scatter plot and save the output to the first argument of the command line
plt.scatter(out['new_cases'], out['case_fatality_rate'], c=out['color'])
plt.title('2020 COVID Case Fatality Rate to New Cases')
plt.grid(True)
plt.xlabel("New Cases")
plt.ylabel("Case Fatality Rate")

plt.show()
plt.savefig(args.outfile1)

#clear the graph in preparation for the second part
plt.clf()


#PART 2
#create a new list of logged values of new_cases
logcase = list()
for x in out['new_cases']:
    if x > 0:
        logcase.append(m.log(x)/m.log(10))
    else:
        logcase.append(0)

#plot the second scatter plot and save the output to the second argument of the command line 
plt.scatter(logcase, out['case_fatality_rate'], c=out['color'])
plt.title('2020 COVID Case Fatality Rate to Log10 of New Cases')
plt.grid(True)
plt.xlim(0,8) #for a better glimpse at the data
plt.xlabel("Log10 of New Cases")
plt.ylabel("Case Fatality Rate")

plt.show()
plt.savefig(args.outfile2)