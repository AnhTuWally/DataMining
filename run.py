#!/usr/bin/env python
import urllib2

url = 'https://www.sec.gov/Archives/edgar/data/757010/000075701012000025/n-qftftpe053112.htm'

#text file for html
f = open('test.txt', 'w')


#open the website
a = urllib2.urlopen(url)
html = a.readlines()

#initialize rowIndent
rowIndent = 0
nextIndent = 0

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

            #found an indentation mark
            if 'TEXT-INDENT:' in html[i]:
                startIndent = html[i].find('TEXT-INDENT:')+13
                endIndent = html[i].find('pt')
                #update Indentation of the current indent
                rowIndent = float(html[i][startIndent:endIndent])
                print rowIndent
                try:
                    #find the next indentation
                    nx = i+1
                    while 'TEXT-INDENT:' not in html[nx]:
                        nx+=1

                    #print html[nx]
                    startIndent = html[nx].find('TEXT-INDENT:')+13
                    endIndent = html[nx].find('pt')
                    #update Indentation of the current indent
                    nextIndent = float(html[nx][startIndent:endIndent])
                except IndexError:
                    nextIndent = rowIndent

            #increment to next tr
            i+=1

        #TR ended
        if row and row[0]=='\t':
            row = row[1:]

        rowArray = row.split('\t')
        if rowArray[0]:
            validData = True
            if len(rowArray) >= 2:
                data1 = rowArray.pop()
                data2 = rowArray.pop()
                try:
                    int(data1[0])
                    int(data2[0])
                except ValueError:
                    validData = False
                data3 = '\t' + data1 + '\t' + data2
                data4 = ' '.join(rowArray)
                row = data4 + data3
                rowArray = row.split('\t')
            if validData:
                #If there is a row less than 2
                if len(rowArray) < 2:
                    #indentation fix
                    if rowIndent < nextIndent:
                        fix = True
                        firstRow = True
                    else:
                        row += '\n'
                        fix = False
                        firstRow = False
                    prefix = row + ' '
                #If the row array is not less than 2, but it need to be fixed
                elif fix:
                    row = prefix + row + '\n'
                    if abs(rowIndent - nextIndent) > 1 :
                        fix = False
                else:
                    row += '\n'

                #dont'r write the first row of indentation
                if firstRow:
                    firstRow = False
                    pass
                else:
                    f.write(row)
f.close()
