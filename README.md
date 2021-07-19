# dividend_tracker
To use the tracker you need a text list of ticker and name the list high_yield_ticker.txt. 

As of 7/11/2021, use div.py not dividend_tracker.py because the urllib.request function is returning garbage values. Switching over to requests function

You can run it with or without the optional argument. To see acceptable argumentes use python3 div.py -h

## Run without argument 
If you run without arguments, you will use the defualt file for list of ticker, high_yield_ticker.txt. You can change the file name in the code.

python3 div.py
  
It will print ticker information in the console. No other arguments can be used.

## Run with argument
Running with arguments allow you to specify an input file to read, and that needs to be followed by another  argument, typically 
the export argument to export the results, df, to a csv. Next, read the csv file in a python shell and view/manipulate the df as needed. 
The reason is so we can do one pull and use the offline file instead of hitting the yahoo server everytime we want to see our portfolio.

`python3 div.py -inf list.of.ticker.txt -exp name.of.expfile.csv`

^Will read list of ticker and export a csv file

`python3 div.py -inf list.of.ticker.txt -sdY`

^Will read list of ticker and sort them by dividend yield and display in console

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
