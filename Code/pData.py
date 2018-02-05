"""
Handles pulling and cleaning up data from Yahoo Finance
"""

import urllib.request
from bs4 import BeautifulSoup as bs

#Given a stock tag and a number of days, returns the closing price for the last x days
def getData(name, num):
    print("Getting data: " + name)
    data = []
    url = "https://finance.yahoo.com/quote/" + name + "/history/"
    rows = bs(urllib.request.urlopen(url).read(), "lxml").findAll('table')[0].tbody.findAll('tr')
    for each_row in rows:
        divs = each_row.findAll('td')
        if divs[1].span.text  != 'Dividend':
            data.append(float(divs[4].span.text.replace(',','')))
    data = data[:num]
    data.reverse()
    return (data)

#Given a list of n floats, returns a list of n-1 percentage changes
def valsToPC(data):
    return([round((((data[x+1]/data[x])-1)*100), 3) for x in range(len(data)-1)])

#Formats floats representing percentages into nice strings
def PCtoSPC(i):
    if(i<0):
        return(str(round(i, 3))+"%")
    else:
        return("+"+str(round(i, 3))+"%")
    
#Formats a float of dollars into a nice string
def fance(i):
    return('${:,.2f}'.format(i))