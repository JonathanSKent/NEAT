"""
Created on Sat Dec 30 08:48:57 2017

@author: Jonathan S. Kent, University of Illinois at Urbana-Champaign
"""

import AWS
import NTSBbot
import pData
import config
import Firms
import datetime

#Returns a dictionary of the last 32 days of closing price data for all stocks
def valsDict():
    return({x:pData.getData(x, 32) for x in config.stockList})

#Returns a dictionary of yesterday's price ratios given ValsDict
def genRatios(valsD):
    return({x:(valsD[x][-1]/valsD[x][-2]) for x in valsD})

#Returns a dictionary of predictions given valsDict
def predictions(valsD):
    preds = {}
    for x in valsD:
        print("Getting prediction: " + x)
        pcs = pData.valsToPC(valsD[x])
        pcs = [str(y) for y in pcs]
        preds[x] = AWS.nPred(pcs[1:])
    return(preds)

#Collects all of the data needed to make a post, and puts it into a dictionary
def colData():
    d = {}
    print("Getting all historical data...")
    d['vals'] = valsDict()
    print("Calculating yesterday's precentage increases...")
    d['ydayPCs'] = {x:((d['vals'][x][-1]/d['vals'][x][-2])-1)*100 for x in d['vals']}
    print("Getting all predictions...")
    d['mpredsPCs'] = predictions(d['vals'])
    print("Getting predictions from yesterday...")
    d['ypredsPCs'] = Firms.getVals('y')
    print("Collecting yesterday's real values...")
    d['ydayVal'] = {x:(d['vals'][x][-2]) for x in d['vals']}
    print("Collecting today's real values...")
    d['tdayValR'] = {x:(d['vals'][x][-1]) for x in d['vals']}
    print("Calculating today's predicted values...")
    d['tdayValP'] = {x:d['ydayVal'][x]*((d['ypredsPCs'][x]/100)+1) for x in d['vals']}
    print("Calculating tomorrow's predicted values...")
    d['mdayValP'] = {x:d['tdayValR'][x]*((d['mpredsPCs'][x]/100)+1) for x in d['vals']}
    return(d)
    
#Rearranges colData into a list of dictionaries for NTSBbot.mkTable
def rearrData(ddict):
    k = []
    for x in ddict['vals']:
        print("Making dictionary: " + x)
        b = {}
        b['yca'] = pData.PCtoSPC(ddict['ydayPCs'][x])
        b['ycp'] = pData.PCtoSPC(ddict['ypredsPCs'][x])
        b['mcp'] = pData.PCtoSPC(ddict['mpredsPCs'][x])
        b['ypa'] = str(round(ddict['ydayVal'][x], 2))
        b['tpa'] = str(round(ddict['tdayValR'][x], 2))
        b['tpp'] = str(round(ddict['tdayValP'][x], 2))
        b['mpp'] = str(round(ddict['mdayValP'][x], 2))
        b['name'] = x
        k.append(b)
    return(k)

#Returns today's date as an appropriate string
def date():
    return(datetime.date.today().strftime("%B %d, %Y"))

#Executes a day of predicting stocks, updating firm values and holdings, and posting to Reddit
def day():
    data = colData()
    ratios = genRatios(data['vals'])
    for x in ['bF', 'iF', 'sbF']:
        Firms.updateFirmData(x, ratios)
    bF = Firms.updateBers(data['mpredsPCs'])
    sbF = Firms.updateSuiBers(data['mpredsPCs'])
    iF = Firms.valIndex()
    Firms.wrText('y', str(data['mpredsPCs']))
    r = rearrData(data)
    k = {'bF':bF, 'iF':iF, 'sbF':sbF}
    m = NTSBbot.mkMess(r, k)
    NTSBbot.post(date(), m)