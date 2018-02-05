"""
Handles interacting with and updating information on the different firms
"""

import config
import json

#Gets the text from a file as a string, given a code string
def getText(f):
    return(open(config.files[f], "r").read())

#Converts a string representation of a dictionary into a dictionary
def convStrToDict(string):
    return(json.loads(string.replace("'", '"')))

#Returns the saved dictionary in a file given a code string for that file
def getVals(f):
    return(convStrToDict(getText(f)))

#Writes a string to a file labeled by a code string
def wrText(f, text):
    return(open(config.files[f], "w").write(text))

#Given the dictionary of yesterday's price ratios, updates the values of a firm's holdings
def updateFirmData(f, ratios):
    currData = getVals(f)
    for x in currData:
        currData[x] *= ratios[x]
    wrText(f, str(currData))
    return(currData)

#Updates the Berserker Firm's holdings given predictions, returning the total holdings
def updateBers(predictions):
    d = getVals('bF')
    c = sum([d[x] for x in d])
    n = ""
    m = -100.0
    for x in predictions:
        if predictions[x] > m:
            m = predictions[x]
            n = x
    dn = {y:0 for y in d}
    dn[n] = c
    wrText('bF', str(dn))
    return(c)

#Same as the last one, but for the Suicidal Berserker Firm
def updateSuiBers(predictions):
    d = getVals('sbF')
    c = sum([d[x] for x in d])
    n = ""
    m = 100.0
    for x in predictions:
        if predictions[x] < m:
            m = predictions[x]
            n = x
    dn = {y:0 for y in d}
    dn[n] = c
    wrText('sbF', str(dn))
    return(c)

#Returns the current value of the Index fund
def valIndex():
    d = getVals('iF')
    return(sum([d[x] for x in d]))