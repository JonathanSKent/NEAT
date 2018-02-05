"""
Contains configuration information
"""
#Reddit Bot
clientID = "[Redacted]"
clientSecret = "[Redacted]"
username = "NTSBbot"
password = "[Redacted]"
user_agent = "Poster Bot"

#AWS
aws_a_k = '[Redacted]'
aws_s_a_k = '[Redacted]'
aws_reg = 'us-east-1'
mlmodid = '[Redacted]'
mlep = 'https://realtime.machinelearning.us-east-1.amazonaws.com'

#Formatting
header = "Stock|Yesterday's Price|Change|Today's Price|Change|Tomorrow's Price\n:--|--:|--:|:--:|--:|--:\n"

#List of stocks
stockList = ['GOOGL', 'NTDOY', 'AMZN', 'FB', 'TSLA', 'NFLX', 'HPQ', 'AAPL', 'MSFT', 'EA', 'AABA', 'ATVI', 'DIS', 'COST', 'VIA', 'TWX', 'CMG', 'MON', 'NVDA', 'INTC', 'AMD']

#Filenames for saving firm/prediction data
files = {
        'bF':"BersData.txt",
        'iF':"IndexData.txt",
        'sbF':"SuiBersData.txt",
        'y':"YesterdayPredictions.txt"
        } 
