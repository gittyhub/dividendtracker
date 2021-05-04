# dividend_tracker
To use the tracker you need a text list of ticker and name the list high_yield.txt. 

You can run it with or without the optional argument. To see acceptable argumentes use python3 div.py -h

## Run without argument 
If you run without arguments, you will use the defualt file for list of ticker, high_yield.txt. You can change the file name in the code.

python3 div.py list.of.ticker.txt
  
It will print ticker information in the console. No other arguments can be used.

## Run with argument
Running with arguments allow you to specify an input file to read, and that needs to be followed by another  argument, typically 
the export argument to export the results, df, to a csv. Next, read the csv file in a python shell and view/manipulate the df as needed. 
The reason is so we can do one pull and avoid overloading the yahoo server.

python3 div.py -inf list.of.ticker.txt -exp name.of.expfile.csv

^Will read list of ticker and export a csv file

python3 div.py -inf list.of.ticker.txt -sdY

^Will read list of ticker and sort them by dividend yield and display in console

## Once csv file exported
If you have a personal portfolio with shares you want to add

myinc = pd.read_csv('myincome.csv')
shares = pd.read_csv('share.csv')
myinc = myinc.join(shares.set_index('Ticker'), on='Ticker')
myinc['Value'] = myinc['Price']*myinc['Shares']
#myinc.drop(['Unnamed: 0'], axis=1, inplace=True)

#For some reason mcn is not picking up sector in the script, let updat manually until we can fix, find location of mcn
myinc.at[6, 'Sector'] = 'Financial Services'
myinc.replace({'Industry':{'0':'Asset Management'}})

myinc.groupby(['Sector']).sum().plot(kind='pie', y='Value', legend=None, autopct='%1.1f%%')

plt.show()

## Get more specific details, more of a pandas review
myinc[myinc['Sector']=='Real Estate'].sort_values(by='Div_Yield', ascending=False)
#For some reason mcn is not picking up sector in the script, let updat manually until we can fix, find location of mcn
myinc.at[6, 'Sector'] = 'Financial Services'
selection = myinc.loc[:, ['Ticker', 'Price', 'Shares', 'Value']]
h[h['Ticker'].isin(['bac','mrk'])].loc[:,['Industry','Sector', 'Ticker']]

#For the high yield after you have imported the csv file
#If you want to convert the FCF to numeric for easy sorting

s = pd.read_csv('high.csv')
s.drop('Unnamed: 0', 'Comp_Name', inplace=True, axis=1)
#Extract from 'FCF' column the last character to check for M or B
#Then if M divide by 1000 else take all but the last character from FCF column
s['d'] = np.where(s['FCF'].str[-1] == 'M', s['FCF'].str[:-1].astype(float)/1000, s['FCF'].str[:-1].astype(float))

#Sort by your new column
s['d'] = np.where(s['FCF'].str[-1] == 'M', s['FCF'].str[:-1].astype(float)/1000, s['FCF].str[:-1].astype(float))

#dividend_history
The dividend history script will get the history of the dividend in a given list. 

There are two main functions in here, plot_fig(x) and df_stat(x)

plot_fig(x) will get a list of tickers and plot the dividend and the change in dividend the stock has paid

df_stat(s) will create a data frame of the ticker and show the standard deviation as well as the dicky full, pvalue and the critical values. The df test was applied because we want to see dividend payout that has grown over the its lifetime

To use:
This will make multiple graphs of all the ticker
`python3 dividend_history.py -plt file_of_tickers` 


This will return a data frame of ticker and show sdt and results of ADF test
`python3 dividend_history.py -inf file_of_tickers` 
