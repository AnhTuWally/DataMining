#!/usr/bin/env python
import urllib2, tkFileDialog
import os

def getText(url = 'https://www.sec.gov/Archives/edgar/data/757010/000075701012000025/0000757010-12-000025.txt', fileOut = None):
    #text file for html
    
    f = fileOut if fileOut else file( str(os.getcwd()+'/'+'output.txt'), 'w')
    #f = open('output', 'w')

    #open the website
    a = urllib2.urlopen(url)
    html = a.readlines()

    #initialize rowIndent
    rowIndent = 0
    nextIndent = 0


    #data collected
    meta = False

    accNum = False

    dt = False

    comName = False

    #header
    f.write('accession_num' +'\t'+ 'report_dt' + '\t' + '\t' + 'number_shares'+ '\t' + 'value'+ '\n')

    #Initial editing
    for i in range(len(html)):
        #gathering meta data
        if not meta:
            metadata = html[i].split('\t')
            if 'ACCESSION NUMBER' in html[i] and not accNum:
                accNum = metadata.pop()
                if accNum.endswith('\n'):
                    accNum=accNum[:-1]

            if ('OF REPORT' in html[i]) and not dt:
                dt = metadata.pop()
                if dt.endswith('\n'):
                    dt=dt[:-1]
                #format the day string
                dt = dt[4:6] + '/' + dt[-2:] + '/' + dt[:4]

            #company name
            if ('COMPANY' in html[i] and 'NAME' in html[i]) and not comName:
                comName = metadata.pop()
                if comName.endswith('\n'):
                    comName=comName[:-1]

            #all metadata are collected
            if accNum and dt and comName:
                f.write(accNum + '\t' + dt + '\t' + comName + '\n')
                meta = accNum + '\t' + dt + '\t'

        #reached the end of the html file
        if '</HTML>' in html[i].upper():
            #break out of the for loop
            break
        #handle exception during parsings
        try:
            #find <TR tag, which stands for the beginning of each table row
            if '<TR' in html[i].upper():
                #flag to signal the end of tr
                notEndTR = True
                #store the data from each row
                row = ''
                #iterate through the whole <TR
                while notEndTR:
                    #Read each line of the html
                    line = html[i]
                    #check if the tag </TR> is in the line, ending each row
                    notEndTR = '</TR>' not in line.upper() #termination condition
                    #Processing the line
                    for j in range(len(line)):
                        data = '' #empty string that store the data
                        #detect the data
                        if line[j] == '>':
                            #avoid writing >
                            if j < len(line)-1: j+=1

                            while line[j] != '<' and j < len(line)-1:
                                #delete the dorlar sign
                                if line[j] == '$':
                                    pass
                                else:
                                    data+=line[j]
                                #increment
                                j+=1

                            #deleting the &nbsp;
                            data = '' if data == '&nbsp;' else data

                            #seperator between data
                            if '&nbsp;' not in line and '$' not in line:
                                if data !='':
                                    #print data
                                    data = '\t' + data
                            #add data to row
                            row += data
                        #increment to next td
                        j+=1

                    #found an indentation mark
                    if 'TEXT-INDENT:' in html[i].upper():
                        startIndent = html[i].find('TEXT-INDENT:')+13
                        endIndent = html[i].find('pt')
                        #update Indentation of the current indent
                        rowIndent = float(html[i][startIndent:endIndent])
                        #print rowIndent
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
                #split row into tuple for data processing
                rowArray = row.split('\t')
                if rowArray[0]:
                    #reset valid data
                    validData = True
                    #find the number data at the end of each row
                    if len(rowArray) >= 2:
                        data1 = rowArray.pop()
                        data2 = rowArray.pop()
                        try:
                            int(data1[0])
                            int(data2[0])
                        except ValueError:
                            #if the thrid and fourth row is not a number, thus no need to process this data
                            validData = False
                        #rejoin the number data
                        data3 = '\t' + data2 + '\t' + data1
                        data4 = ' '.join(rowArray)
                        #rebuild the row
                        row = data4 + data3
                        #split the data again for information
                        rowArray = row.split('\t')
                    if validData:
                        #If there is a row less than 2
                        if len(rowArray) < 2:
                            #indentation fix, if the next indentation is bigger than the current indentation
                            if rowIndent < nextIndent:
                                fix = True
                                firstRow = True
                                #the change is too big, this is a change in page
                                if abs(rowIndent - nextIndent) < 100:
                                    #cumulative prefix
                                    if row not in prefix:
                                        prefix += row + ' '
                            else:
                                #pass if the row indentation is too big, signify the change of page
                                if abs(rowIndent - nextIndent) > 100:
                                    pass
                                else:
                                    #new data set, reset everything
                                    row += '\n'
                                    fix = False
                                    prefix = ''
                                    firstRow = False
                        #If the row array is not less than 2, but it need to be fixed
                        elif fix:
                            #fixing the row indentation of data set
                            row = prefix + row + '\n'
                            #ignore page changes
                            if 1 < abs(rowIndent - nextIndent) < 100:
                                fix = False
                                prefix = ''
                        else:
                            #no indentation difference
                            row += '\n'
                            prefix = ''

                        #dont'r write the first row of indentation
                        if firstRow:
                            firstRow = False
                            pass
                        else:
                            if len(rowArray) > 2:
                                f.write(meta + row)
                                #f.write(row)
        except IndexError:
            #handeling the mess at the end of text file
            print 'Error'
            break
    f.close()

if __name__ == '__main__':
    getText()
