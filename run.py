import urllib2

url = 'https://www.sec.gov/Archives/edgar/data/757010/000075701012000025/n-qftftpe053112.htm'

#text file for html
f = open('test.txt', 'w')


#open the website
a = urllib2.urlopen(url)
html = a.readlines()



for i in range(len(html)):
    if '<TR' in html[i]:
        #flag to signal the end of tr
        notEndTR = True
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
                        data+=line[j]
                        #increment
                        j+=1

                    #replacing item with [space]
                    data = ' ' if data == '&nbsp;' else data

                    #seperator between data
                    data+=' '
                    f.write(data)
                #increment to next td
                j+=1
            #increment to next tr
            i+=1
        #TR ended
        f.write('\n')
f.close()
