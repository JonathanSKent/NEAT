This folder contains data

* RawPriceData.zip contains a few thousand .txt files, with the raw 
  closing prices of the given stock in chronological order.
  
* StockList.csv contains the symbols for every stock in the dataset,
  to make manipulating the data a bit easier.

* ENKeys are .txts with each line being a unique key, representing
  a unique block of raw data from which to generate a block of
  training data. Each ENKeys file containe 10^N keys, from 1,000
  to 1,000,000.

* ENBlocks are .txts containing the blocks of data pulled using the
  keys from ENKeys. I have included only N = 3, 4 as 5 and 6 are 
  rather large.
