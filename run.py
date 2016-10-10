import urllib2

url = 'https://www.sec.gov/Archives/edgar/data/757010/000075701012000025/n-qftftpe053112.htm'

#open the website
a = urllib2.urlopen(url)
html = url.read()
