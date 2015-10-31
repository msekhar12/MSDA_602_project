import pandas as pd
from pandas import Series,DataFrame
import math
import os
import csv
import re

import seaborn as sns
import matplotlib.pyplot as plt

#Install the following package (seaborn), using the command "conda install seaborn"

def clear_scr():
    '''Clears the screen
    '''
#To accommodate all Operating systems, I am using 2 commands
    try:
        unused_var = os.system('clear')
        unused_var = os.system('cls')
    except:
        pass

def read_file():
    '''Reads the supplied file, and returns a DataFrame'''
    clear_scr()

    s = raw_input("\nEnter File location. To quit, press ENTER on blank input\n ==>")    

    while True:
        if s == '':
            print '\n\nGood Bye'
            sys.exit()
        
        try:
            file_reader = csv.reader(open(s),delimiter = ',', quoting = csv.QUOTE_NONE)
        except:
            print "\nThe given file location is incorrect. Enter file's location (complete path) again or EXIT to quit\n"
            s = raw_input("==>")
            continue
        else:
            break

    disease  = list()
    county = list()
    year = list()
    sex = list()
    count = list()
    population = list()
    rate = list()

    #Skip the first line, since it is a heading.
    file_reader.next()
    
    for line in file_reader:
        line_len = len(line)
        if(line_len > 7):
            d = line[0:line_len - 6]
            d = ','.join(d)
            disease.append(d)
        else:
            disease.append(line[0])

        rate.append(float(line[-1]))
        population.append(int(line[-2]))
        count.append(int(line[-3]))
        sex.append(line[-4])
        year.append(int(line[-5]))
        county.append(line[-6])

        
    df = DataFrame()
    

    df['disease'] = disease
    df['county'] = county
    df['year'] = year
    df['sex'] = sex
    df['count'] = count
    df['population'] = population
    df['rate'] = rate

    return (df)


if __name__ == '__main__':

    #Read the file first!!
    diseases_df =  read_file()
    print diseases_df.head()
#    print diseases_df[diseases_df['sex'] == 'Total']
    l_diseases_total = diseases_df[diseases_df['sex'] == 'Total']
    print l_diseases_total.head()
    #The groupby do not return a data frame by default. The following operation will get a data frame. Observe that it also assigns a column name to the sum column
    l_diseases_total = DataFrame({'sum' : l_diseases_total.groupby(['year','disease'])['count'].sum()}).reset_index()
    #DataFrame({'count' : df1.groupby( [ "Name", "City"] ).size()}).reset_index()
    print l_diseases_total

    #Let us pivot the data frame in such a way that the diseases will be columns, years will be rows, and the data will be the sum
    l_diseases_total = l_diseases_total.pivot(index = 'year', columns='disease', values = 'sum')
    l_diseases_total[l_diseases_total.isnull()] = 0
    print l_diseases_total

    #Let us get the correlation.
    corrmat = l_diseases_total.corr()
    corrmat = corrmat[corrmat > 0.95]
    corrmat[corrmat.isnull()] = 0
    sns.set(context="paper", font="monospace")
    f, ax = plt.subplots(figsize=(30, 20))
    sns.heatmap(corrmat, vmax=.8, square=True)
    #print corrmat.columns.get_level_values("disease")
    diseases = corrmat.columns.get_level_values("disease")
    print diseases
    for i, disease in enumerate(diseases):
        print str(i) + " " + disease
        if i and disease != diseases[i - 1]:
          ax.axhline(len(disease) - i, c="w")
          ax.axvline(i, c="w")
    f.tight_layout()
    sns.plt.show()  

##import seaborn as sns
##import matplotlib.pyplot as plt
##sns.set(context="paper", font="monospace")
##
### Load the datset of correlations between cortical brain networks
##df = sns.load_dataset("brain_networks", header=[0, 1, 2], index_col=0)
##corrmat = df.corr()
##
### Set up the matplotlib figure
##f, ax = plt.subplots(figsize=(12, 9))
##
### Draw the heatmap using seaborn
##sns.heatmap(corrmat, vmax=.8, square=True)
##
### Use matplotlib directly to emphasize known networks
##networks = corrmat.columns.get_level_values("network")
##for i, network in enumerate(networks):
##    if i and network != networks[i - 1]:
##        ax.axhline(len(networks) - i, c="w")
##        ax.axvline(i, c="w")
##f.tight_layout()
    
#    l = Series((HTTP_DF['origin']))
#    l = l.value_counts()

#    clear_scr()
    
#    print "\n"
#    print "Questions"
##    print "---------"
##    print "Question:1."
##    print "-----------"
##    print "Which hostname or IP address made the most requests?"
##    print "Answer:"
##    print "-------"
##    print "The MAXIMUM number of requests were made by '%s'.\nFrom this address, a total of %d requests were made" % (l.idxmax(),l.max())
##    print "\n"
##
##    l = HTTP_DF.groupby(['origin'])['bytes_transferred'].sum()
##    print "Question:2."
##    print "-----------"
##    print "Which hostname or IP address received the most total bytes from the server?  How many bytes did it receive?"
##    print "Answer:"
##    print "-------"
##    print "The MAXIMUM number of bytes were received by '%s'. This address has received a total of %d bytes." % (l.idxmax(), l.max())
##    print "\n"
##    
##
##    l = Series((HTTP_DF['hour']))
##    l = l.value_counts()
##
##    print "Question:3."
##    print "-----------"
##    print "During what hour was the server the busiest in terms of requests?"
##    print "Answer:"
##    print "-------"
##    print "The MAXIMUM number of requests were made in the hour '%s'.\nIn this hour, a total of %d requests were made" % (l.idxmax(),l.max())
##
##    l = HTTP_DF[HTTP_DF['url'].str.contains('.gif',case=False)]['url']
##    l = l.value_counts()
##    print "\n"
##  
##    print "Question:4."
##    print "-----------"
##    print "Which .gif image was downloaded the most during the day?"
##    print "Answer:"
##    print "-------"
##    print "The MAXIMUM number of downloads were made for the image '%s'.\nThis image was downloaded %d times" % (l.idxmax(),l.max())    
##
##    l = HTTP_DF[HTTP_DF['retcode'] != 200]['retcode']
##    
##    print "\n"
##    print "Question:5."
##    print "-----------"
##    print "What HTTP reply codes were sent other than 200?"
##    print "Answer:"
##    print "-------"
##    print "The following return codes (other than 200) wrere sent:"
##    print l.unique()
