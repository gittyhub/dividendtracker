# dividentracker
To use the tracker you need a text list of ticker and name the list high_yield.txt. 

You can run it with or without the optional argument. To see acceptable argumentes use python3 div.py -h

## Run without argument 
If you run without arguments, you will use the defualt file for list of ticker, high_yield.txt. You can change the file name in the code.

python3 div.py list.of.ticker.txt
  
It will print ticker information in the console. No other arguments can be used.

## Run with argument
Running with arguments allow you to specify an input file to read, and that needs to be followed by another  argument, typically the export argument to export the results, df, to a csv. Next, read the csv file in a python shell and view/manipulate the df as needed. The reason is so we can do one pull and avoid overloading the yahoo server.

python3 div.py -inf list.of.ticker.txt -exp name.of.expfile.csv

^Will read list of ticker and export a csv file

python3 div.py -inf list.of.ticker.txt -sdY

^Will read list of ticker and sort them by dividend yield and display in console

## Once csv file exported
If you have a personal portfolio with shares you want to add

myinc = pd.read_csv('myincome.csv')
shares = pd.read_csv('share.csv')

myinc = myinc.join(shares.set_index('Ticker'), on='Ticker')

myinc.groupby(['Sector'].sum().plot(kind='pie', y='Value', legend=None, autopct='%1.1%%f')

plt.show()

## Get more specific details, more of a pandas review
myinc[myinc['Sector']=='Real Estate'].sort_values(by='Div_Yield', ascending=False)
selection = myinc.loc[:, ['Ticker', 'Price', 'Shares', 'Value']]
