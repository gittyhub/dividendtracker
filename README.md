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
There are two scripts we to be used here:
dividend_tracker.py 
dividend_history.py

There will also be three input files the user will need to fill out:
high_yield_ticker.txt
my_income_ticker.txt
shares.csv

#Input files
These input files will have to be filled out by the user. 
high_yielding_ticker.txt should contain all dividends the user wishes to track
my_income_ticker.txt should contain all divided the user want to track/own in their portfolio
shares.csv is the number of shares the user wants to track/own in conjunction with my_income_ticker.txt

#dividend_yield_ticker.txt
This script will do two things:
1)Take a list of dividend yielding stocks and return some info on them, CF, CFC, and liquidity ratios, quick, current 
  a)Print data to console
  b)Export data to csv file

2)Take a list of dividend yielding stocks and a list of shares you hold, and return current dividends return (over what period, 1y, 6m)

#dividend_history.py
1)With the list of dividend stocks from my_income_ticker.txt, graph the historical dividend payout for the stocks

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

The list below is a description of what the files are used for if available:
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
#1)Take a list of dividend yielding stocks and return some info on them, CF, CFC, and liquidity ratios, quick, current 
If the scrip it not working, check the function that looks up the ticker and make sure that the find function is looking for the
anchors correctly. Usually Yahoo will change the tags we need for the anchor

##1a-Print to console no arguments
Run script to collect data on your stock list (dividend_tracker.py will use high_yield_ticker.txt for the list of ticker)
If you run without arguments, you will use the defualt file for list of ticker, high_yield_ticker.txt. You can change the file name in the code

python3 dividend_tracker.py
  
It will print ticker information in the console. No other arguments can be used.

##1a-Print to console with arguments
Running with arguments allow you to allows you to provide different flags for the arguments. You can specify an input/output file to read the 
tickers and output for the data. There is also an option to print the data to console, run python3 dividend_tracker.py -h to get the list. 

This will hit Yahoo site everytime you run, best to use on small new ticker list
Even better would be to get the output, and in python shell do your editing

python3 dividend_tracker.py -inf list.of.ticker.txt -sdY

^Will read list of ticker and sort them by dividend yield and display in console

##1b-Export ticker data to csv file
To do this you will need to use several argument flags, the -inf for the list of tickers you want to look up and -exp for the export of the file name you wish to export. From here you can fire up a python shell and import the csv file into pandas and do your analytics there. This is 
perfered way because we can do one pull and use the offline file instead of hitting the yahoo server everytime we want to 
see our portfolio.

This will make a request to Yahoo for each of the ticker

python3 dividend_tracker.py -inf high_yield_ticker.txt -exp high_yield_ticker_output.csv

^Will read list of ticker and export a csv file

Fire up your shell and run your analysis as needed 

#2)Take a list of dividend yielding stocks and a list of shares you hold, and return current dividends return (over what period, 1y, 6m)
##Track your own portfolio with number of shares
You can use a list of your own stock holding to see how it is performing. 
Input your holdings into my_income_ticker.txt
Run the python script with my_income_ticker.txt as the input file and specify and export file
The export file my_income.csv will have all the data pulled from Yahoo

python3 dividend_tracker.py -inf my_income_ticker.txt -exp my_income_output.csv

Fill out the info into share.csv

Import both csv files. Your going to merge all your stock data from Yahoo and the number of share you filled out in share.csv. From here 
on out, you will be using this file, it WILL NOT hit Yahoo again


my = pd.read_csv('my_income_output.csv')
share = pd.read_csv('share.csv')

In the dividend_tracker is function, clean_share to combine output with the list of shares and purhase date

In the div_tracker modules script you can either use cleanup_shares or cleanup_high to clean the csv files you just imported
clean shares will take your portfolio list and number of shares and arrange the dataframe in a clean fashion
clean high will only take the list you import and clean it the same way with no shares

import dividend_tracker as dt
df = dt.cleanup_shares(my,share)

Next use the get_all_divided_table function from the dividend_history file to get all the dividend history for your stock. This wil give you a csv file
all_dividends.csv 

*If you have it already no need to run again unless old, that way you dont make too many request to Yahoo. First time using dividend_history.py
import dividend_history as dh
dh.get_all_dividend_table('my_income_ticker.txt')

#Export is all_dividends.csv
*4/7/2022
*Why do we have dividend_history.py and dividend_tracker.py, can we just use dividend_history.py?
*One is to track dividends and provided data on each company, dividend_tracker and the other is to get historical data, dividend_history.py

import dividend_history as dh
div_his = pd.read_csv('all_dividends.csv')

Import the divlookup module from dividend_tracker. We are going to apply this function over the df, we dont want to look df because there is a host of issues
Be sure to modify the dividend_history.py script to change the range on period you want to pull in the dividend

#df['Div_Collected'] = df.apply(lambda row : divlookup(row['Ticker'], row['Purchase_Date'])['0'].sum(), axis=1)
#4/10/2022-add a date range instead of taking hard code from function
df['Div_Collected'] = df.apply(lambda row : dt.divlookup(row['Ticker'], div_his)['0'].sum(), axis=1)
df['Total_Dividend'] = df.Div_Collected*df.Shares

#From here you can filter as needed

## Get more specific details, more of a pandas review, slicing
my[my['Sector']=='Real Estate'].sort_values(by='Div_Yield', ascending=False)

selection = df.loc[:, ['Ticker', 'Price', 'Shares', 'Value']]

h[h['Ticker'].isin(['bac','mrk'])].loc[:,['Industry','Sector', 'Ticker']]

To see what your potfolio allocation is by sector

import matplotlib.pyplot as plt

df.groupby(['Sector']).sum().plot(kind='pie', y='Value', legend=None, autopct='%1.1f%%')
plt.show()

## dividend_history
The dividend history script will get the history of the dividend in a given list. 
There are two main functions in here, plot_fig(x) and df_stat(x)

plot_fig(x) will get a list of tickers and plot the dividend and the change in dividend the stock has paid

df_stat(s) will create a data frame of the ticker and show the standard deviation as well as the dicky full, pvalue and the critical values. The df test was applied because we want to see dividend payout that has grown over the its lifetime

To use:
This will make multiple graphs of all the ticker
python3 dividend_history.py -plt high_yield_ticker.txt


This will return a data frame of ticker and show sdt and results of ADF test
python3 dividend_history.py -inf high_yield_ticker.txt

#Things to add
Add column for date purchase, will probably need multiple
#4/10/2022-add a date range instead of taking hard code from function

#PRACTICAL
1. Get you list of tickers
2. Run this. inf is your input file of tickers, and the exp is your export file of the data you want to pull
`python3 dividend_tracker.py -inf ameritrade_holdings.txt -exp ameritrade_output.csv
3. Once you get your data, do your analysis in the interpreter 
import pandas as pd
import numpy as np
import os
import dividend_tracker as dt
import matplotlib.pyplot as plt
my = pd.read_csv('ameritrade_output.csv')
share = pd.read_csv('ameritrade_share.csv')
df = dt.cleanup_shares(my,share)
df.sort_values(by=['Div_Yield'],ascending=False)[['Comp_Name','Div_Yield','Price2Book','QuickRatio','Tot.Cash/Share','M_FCF']]

df.groupby(['Sector']).sum().plot(kind='pie', y='Value', legend=None, autopct='%1.1f%%')
plt.show()
