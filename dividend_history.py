import urllib.request
import datetime
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import pandas as pd
import argparse
import sys


parser = argparse.ArgumentParser(description='Get dividend history and grph from file')
parser.add_argument('-inf', '--input_file', type = str, metavar = '', help = 'file fo tickers to process')
parser.add_argument('-exp', '--expot_csv', type = str, metavar = '', help = 'eport csv file name, enter after flag')
parser.add_argument('-plt', '--plot', type = str, metavar = '', help = 'plots dividend history')
args = parser.parse_args()

def ca_TA(x):
  site = 'https://finance.yahoo.com/quote/'+x+'/history?period1=448156800&period2=1619136000&interval=div%7Csplit&filter=div&frequency=1d&includeAdjustedClose=true'
  div = {}
  count=0
  anchor=0
  r = str(urllib.request.urlopen(site).read())
  while r.find('class="Ta', anchor) > 0:
    count += 1 
    start = r.find('class="Ta(c)', anchor) 
    date_string = r[start-28:start-16]
    date_time_obj = datetime.datetime.strptime(date_string,"%b %d, %Y")

    div_beg_anchor = r.find('<strong data', start)
    div_start = r.find('>', div_beg_anchor)
    div_end = r.find('</strong', div_start)
    #print('start: '+str(start))
    div_string = r[div_start+1:div_end]

    div[date_time_obj] = float(div_string)

    anchor = r.find('class="Ta(c)',anchor+1)
  
  return div

def plot_fig(x):
  for i in x:
    key = list(ca_TA(i).values()) 	#get the dividend using ca_TA() function
    v = np.diff(key)*-1  			#gets the differece in div payout period over period
 
    adfuller_results = adfuller(key) 
    one, five, ten = adfuller_results[4].values() #get the critial value at 1, 5 and 10 percent
    
    fig, ax = plt.subplots()  		#creates an empty figure to plot
    ax.plot(key[::-1], label='Div') 	#plots the $ div payout in reverse order 
    ax.plot(v[::-1], label='Div_Rate') 	#plot the diff in $ payout in reverse order
 
    ax.legend() #adds legend to the figure

    plt.text(0.20,0.7, i.capitalize() +'\n'+ 
      str('Std: '+ "%.2f" % np.std(key,ddof=0))+'\n'
        +'ADF Stat: {:.3f}'.format(adfuller_results[0])+'\n' 
        +'p-value: {:.3f}'.format(adfuller_results[1])+'\n'
        +'1% Critical: '+'{:.3f}'.format(one)+'\n'+'5% Critical: '+'{:.3f}'.format(five)+'\n'+'10% Critical: '+'{:.3f}'.format(ten)+'\n', 
        horizontalalignment='left', verticalalignment='center', transform = ax.transAxes,fontsize=12) 

    fig.savefig(i)

def df_stat(x):
  d = []
  for i in x:
    key = list(ca_TA(i).values())
    v = np.diff(key)*-1
 
    adfuller_results = adfuller(key) 
    one, five, ten = adfuller_results[4].values()

    lable = ['Comp_Name', 'STD', 'ADF_Stat','p-value','Crit_Value(1%)','Crit_Value(5%)','Crit_Value(10%)'] 
    l = [i,"%.4f" % np.std(key,ddof=0), 
            '{:.4f}'.format(adfuller_results[0]), 
            '{:.4f}'.format(adfuller_results[1]), 
            '{:.4f}'.format(one), '{:.4f}'.format(five), '{:.4f}'.format(ten)]

    d.append(l)

  df = pd.DataFrame(d,columns=['Comp_Name', 'STD', 'ADF_Stat','p-value','Crit_Value(1%)','Crit_Value(5%)','Crit_Value(10%)'])

  return df

def clean_stock_list(x):
  '''Open specified text file of ticker and puts them in a list for processing, returns list of ticker'''
  #if there is a new line at end of file script wont work properly
  #if you mess up and have a blank between commas it will also mess up
  f = open(x,'r').read().splitlines()
  f = [i.split(',') for i in f]
  f = [i.strip() for s in f for i in s]
  return set(f)

if __name__=="__main__":
  
  file = stock = ['rc', 'bac', 'xom', 'wfc', 'enb', 'mo'] 
 
  #plot_fig(stock)
  i = args.input_file
  if args.input_file: 
    print(df_stat(clean_stock_list(i)).sort_values(by='p-value'))
  elif args.plot:
    plot_fig(clean_stock_list(sys.argv[2]))
  else:
    print(df_stat(file).sort_values(by='p-value'))
 

