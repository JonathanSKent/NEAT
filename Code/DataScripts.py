"""
Scrapes stock price information from Yahoo finance

Frankly, I don't care much for the code that I've written here.
It's just a set of quick-and-dirty scripts for collecting and
cultivating the training data for the rest of the project.
"""

from pandas_datareader import get_data_yahoo as gdy
import os
import random

def getCloseData(symbol):
    k = gdy(symbol)['Close']
    return([float(round(x, 2)) for x in k])
    
def saveData(name, data):
    s = '/home/jonathan/Desktop/AIMarket/Data'
    l = os.path.join(s, name+'.txt')
    f = open(l, 'w')
    f.write(str(data))
    f.close()
    print('Save Successful: ' + name)
    return(None)
    
def getStockList():
    s = open('StockList.txt').read()[:-1].split(', ')
    return(s)
    
def scrapeData(s = getStockList()):
    for x in s:
        print("Getting Data: " + x)
        try:
            d = getCloseData(x)
            saveData(x, str(d)[1:-1])
        except:
            print('ERROR: SOME BULLSHIT')
    print('Scraping Done')
    
def delCrap(s = getStockList()):
    for x in s:
        n = os.path.join('/home/jonathan/Desktop/AIMarket/Data', x+'.txt')
        try:
            t = open(n).read()
            l = t.split(', ')
            for y in l:
                if y == 'nan':
                    print('DELETING ' + x + ' FOR NAN')
                    os.remove(n)
                    break
            if len(l) < 50:
                print('DELETING ' + x + ' FOR LENGTH')
                os.remove(n)
                return(None)
        except:
            print('Nonexistant File')
    print('Done')
    
def realNames():
    f = open('StockList.txt', 'r+')
    s = f.read().split(', ')
    l = ""
    for x in s:
        n = os.path.join('/home/jonathan/Desktop/AIMarket/Data', x+'.txt')
        try:
            open(n)
            l += x + ', '
        except:
            print('NONEXISTANT FILE')
    f.write(l)
    
def getLens(s = getStockList()):
    d = []
    for x in s:
        d.append((x, len(open(os.path.join('/home/jonathan/Desktop/AIMarket/Data', x+'.txt')).read().split(', ')) - 40))
    return(d)
    
def getBlockCount(k = getLens()):
    return(sum([x[1] for x in k]))
    
def getRandBlockKey(d = getLens()):
    c = getBlockCount(d)
    r = random.randint(0, c)
    for x in d:
        if r > x[1]:
            r -= x[1]
        else:
            return((x[0], r))
    
def getNKeys(n):
    d = getLens()
    l = []
    while len(l) < n:
        if len(l) % 1000 == 0:
            print(100*round(len(l)/n, 4))
        k = getRandBlockKey(d)
        if not(k in l):
            l.append(k)
    return(l)

def saveKeys(keys, name):
    s = ''
    for x in keys:
        s += str(x)[1:-1] + '\n'
    open(name, 'w').write(s)
    return("Success")
    
def keyToBlockRaw(key):
    l = [float(x) for x in open(os.path.join('/home/jonathan/Desktop/AIMarket/Data', key[0]+'.txt')).read().split(', ')[key[1]:key[1]+40]]
    return(l)
    
def rawBlocksFromKeyFile(keyFile, blocksName):
    keysA = open(keyFile).read().split('\n')
    keysB = [x.split(', ') for x in keysA]
    keysC = [[x[0][1:-1], int(x[1])] for x in keysB[:-1]]
    f = open(blocksName, 'w+')
    for x in keysC:
        f.write(str(keyToBlockRaw(x))[1:-1] + '\n')
    return(keysC)

def blockToPercents(block, numDays, daysOut):
    l = []
    for x in range(numDays):
        l.append(round((((block[x+1]/block[x])-1)*100), 2))
    l.append(round((((block[numDays+daysOut]/block[numDays])-1)*100), 2))
    return(l)
    
def blockListToPercentList(blockList, percentName, numDays, daysOut):
    f = open(os.path.join('/home/jonathan/Desktop/AIMarket/Blocks', blockList)).read()
    bs = f.split('\n')
    n  = open(os.path.join('/home/jonathan/Desktop/AIMarket/TrainingData', percentName), 'w+')
    k = ""
    for x in bs[:-1]:
        b = [float(y) for y in x.split(', ')[:-1]]
        k += (str(blockToPercents(b, numDays, daysOut))[1:-1]+'\n')
    n.write(str(k)[1:-1])
    
