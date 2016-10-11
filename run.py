#!/usr/bin/env python
import urllib2
import re

url = 'https://www.sec.gov/Archives/edgar/data/757010/000075701012000025/n-qftftpe053112.htm'

#text file for html
f = open('test.txt', 'w')


#open the website
a = urllib2.urlopen(url)
html = a.readlines()


#Initial editing
for i in range(len(html)):
    if '<TR' in html[i]:
        #flag to signal the end of tr
        notEndTR = True
        count = 0
        row = ''
        while notEndTR:
            line = html[i]
            #check if the tag </TR> is in the line
            notEndTR = '</TR>' not in line #termination condition
            #Processing the line
            for j in range(len(line)):
                data = '' #empty string that store the data
                #detect the data
                if line[j] == '>':
                    #avoid writing >
                    if j < len(line)-1: j+=1

                    while line[j] != '<' and j < len(line)-1:
                        #f.write(line[j])

                        #delete the dorlar sign
                        if line[j] == '$':
                            pass
                        else:
                            data+=line[j]
                        #increment
                        j+=1

                    #replacing item with [space]
                    data = '' if data == '&nbsp;' else data
                    #seperator between data
                    if '&nbsp;' not in line and '$' not in line:
                        if data !='':
                            #print data
                            data = '\t' + data
                    row += data
                    #f.write(data)
                #increment to next td
                j+=1
            #increment to next tr
            i+=1
        #TR ended
        if row and row[0]=='\t':
            row = row[1:]

        rowArray = row.split('\t')
        if rowArray[0]:
            if len(rowArray) > 2:
                data1 = rowArray.pop()
                data2 = rowArray.pop()
                data3 = '\t' + data1 + '\t' + data2
                data4 = ' '.join(rowArray)
                row = data4 + data3
            row+='\n'
            f.write(row)
f.close()

f1 = open('test.txt', 'r')
f2 = open('test2.txt', 'w')

lines = f1.readlines()

f1.close()
f2.close()
