"""
Handles formatting and posting updates to Reddit
"""

import praw
import config
import pData

r = praw.Reddit(client_id=config.clientID, 
                client_secret=config.clientSecret,
                password=config.password,
                user_agent=config.user_agent,
                username=config.username)

r.read_only = False

#Posts text to r/NotTooSeriousBusiness with the appropriate title and body
def post(title, body):
    print("Attempting to post...")
    try:
        r.subreddit("NotTooSeriousBusiness").submit(title, selftext=body)
        print("Post successful")
    except:
        print("Post failed")

#Formats a dictionary containing one stock's data into a line on a Reddit table
def fmat(dictDat):
    line1 = dictDat['name']+'|'+dictDat['ypa']+'|'+dictDat['yca']+'|'+dictDat['tpa']+'↘||'
    line2 = 'Prediction||'+dictDat['ycp']+'|'+dictDat['tpp']+'|↖'+dictDat['mcp']+'|'+dictDat['mpp']
    return(line1+'\n'+line2+'\n')

#Given a list of dictionaries, formats them into a Reddit table
def mkTable(dictDats):
    table = config.header
    for x in dictDats:
        table += fmat(x)
    return(table)

#Given the list of dictionaries and the values of the funds, returns a formatted post body
def mkMess(dictDats, firmVals):
    a = "\n\nBerseker Fund Value: " + pData.fance(firmVals['bF'])
    b = "\n\nIndex Fund Value: " + pData.fance(firmVals['iF'])
    c = "\n\nSuicidal Berserker Fund Value: " + pData.fance(firmVals['sbF'])
    return(mkTable(dictDats) + a + b + c)