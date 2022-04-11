# Dividend_tracker

CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Requirements
 * Recommended modules
 * Installation
 * Configuration
 * Troubleshooting
 * FAQ
 * Maintainers

Introduction
---------------------
This script will do two things:
1)Take a list of dividend yielding stocks and return some info on them, CF, CFC, and liquidity ratios, quick, current 

2)Take a list of dividend yielding stocks and a list of shares you hold, and return current dividends return (over what period, 1y, 6m)


Requirements
---------------------
Will be using urllib.request and requests to grab the ticker symbol from yahoo, pandas, numpy, os, sys, and argparse to pass thos additional parameter
We're also using the argparse, this lets up add additional argument when we call the script to pass additional parameters

Recomended modules
---------------------
Same as above


Installation
---------------------
Run the script with python3


Configuration
---------------------
To use the tracker you need a text list of ticker and name the list high_yield_ticker.txt. 

The list below is a description of what the files are used for:
all_dividends.csv-OUTPUT OF ALL Dividends for my_income.csv
dividend_history.py-DEPRECATED
dividend_tracker.py
high_yield.csv-DETAIL OUTPUT OF ALL high_yeild_ticker
high_yield_ticker.txt-INPUT of all high yield dividend to track
my_income.csv-DETAIL OUTPUT OF ALL my_income_ticker
my_income_ticker.txt-INPUT of user ticker symbol
README.md
requirements.txt-requirement to run script
share.csv-INPUT for ticker, number of shares and date purchased
sum_dividend-just a file for python code to sum dividends

Process:
## Run without argument 
Run script to collect data on your stock list (dividend_tracker.py using my list of tickers, it will use high_yield_ticker.txt for the list of ticker)
If you run without arguments, you will use the defualt file for list of ticker, high_yield_ticker.txt. You can change the file name in the code.

`python3 dividend_tracker.py
  
It will print ticker information in the console. No other arguments can be used.

## Run with argument
Running with arguments allow you to specify an input file to read, and that needs to be followed by another  argument, typically 
the export argument to export the results, df, to a csv. 

Next, read the csv file in a python shell and view/manipulate the df as needed. 
The reason is so we can do one pull and use the offline file instead of hitting the yahoo server everytime we want to see our portfolio.

`python3 div.py -inf list.of.ticker.txt -exp name.of.expfile.csv`

^Will read list of ticker and export a csv file

`python3 div.py -inf list.of.ticker.txt -sdY`

^Will read list of ticker and sort them by dividend yield and display in console



Output will be a csv file with the data from above, my_income.csv
Have a list of the stock number of shares you own and purchase date, share.csv
Import both csv files
  my = pd.read_csv('my_income.csv')
  share = pd.read_csv('share.csv')

In the dividend_tracker is function, clean_share to combine output with the list of shares and purhase date
  import dividend_tracker as dt
  df = dt.clean_share(my,share)

Next use the get_all_divided_table from the dividend_history file to get all the dividend history for your stock. This wil give you a csv file
  all_dividends.csv. If you have it already no need to run again unless old, that way you dont make too many request to Yahooa
  import dividend_history as dh
  div_his = pd.read_csv('all_divdidends.csv')

Import the divlookup module from dividend_tracker. We are going to apply this function over the df, we dont want to look df because there is a host of issues
  df['Div_Collected'] = df1.apply(lambda row : divlookup(row['Ticker'], row['Purchase_Date'])['0'].sum(), axis=1)

As of 7/31/2021, use dividend_tracker.py 

You can run it with or without the optional argument. To see acceptable argumentes use python3 div.py -h


## Once csv file exported
If you have a personal portfolio with shares you want to add them as well

`myinc = pd.read_csv('my_income.csv')`

`shares = pd.read_csv('share.csv')`

#In the div modules script you can either use cleanup_shares or cleanup_high to clean the csv files you just imported
#clean shares will take your portfolio list and number of shares and arrange the dataframe in a clean fashion
#clean high will only take the list you import and clean it the same way with no shares

import div as d

df = d.clean_shares(my,shares)

#From here you can filter as needed

## Get more specific details, more of a pandas review, slicing
`myinc[myinc['Sector']=='Real Estate'].sort_values(by='Div_Yield', ascending=False)`

`selection = myinc.loc[:, ['Ticker', 'Price', 'Shares', 'Value']]`

`h[h['Ticker'].isin(['bac','mrk'])].loc[:,['Industry','Sector', 'Ticker']]`

#To see what your potfolio allocation is by sector

import matplotlib.pyplot as plt

`myinc.groupby(['Sector']).sum().plot(kind='pie', y='Value', legend=None, autopct='%1.1f%%')`

`plt.show()`

## dividend_history
The dividend history script will get the history of the dividend in a given list. 

There are two main functions in here, plot_fig(x) and df_stat(x)

plot_fig(x) will get a list of tickers and plot the dividend and the change in dividend the stock has paid

df_stat(s) will create a data frame of the ticker and show the standard deviation as well as the dicky full, pvalue and the critical values. The df test was applied because we want to see dividend payout that has grown over the its lifetime

To use:
This will make multiple graphs of all the ticker
`python3 dividend_history.py -plt file_of_tickers` 


This will return a data frame of ticker and show sdt and results of ADF test
`python3 dividend_history.py -inf file_of_tickers` 

#Things to add
Add column for date purchase, will probably need multiple
Then create another column to sum up all dividend collected
