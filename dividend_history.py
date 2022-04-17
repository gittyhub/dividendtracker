import urllib.request
import datetime
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import pandas as pd
import argparse
import sys
import requests



parser = argparse.ArgumentParser(description='Get dividend history and grph from file')
parser.add_argument('-inf', '--input_file', type = str, metavar = '', help = 'file fo tickers to process')
parser.add_argument('-exp', '--expot_csv', type = str, metavar = '', help = 'eport csv file name, enter after flag')
parser.add_argument('-plt', '--plot', type = str, metavar = '', help = 'plots dividend history')
args = parser.parse_args()

header = {'User-agent':'Mozilla/5.0'}

def ca_TA(x): 
  site = 'https://finance.yahoo.com/quote/{}/history?period1=448156800&period2=1649203200&interval=capitalGain%7Cdiv%7Csplit&filter=div&frequency=1mo&includeAdjustedClose=true'.format(x) 
  div = {} 
  count=0 
  anchor=0 
  r = str(requests.get(site,headers=header).content) 
  while r.find('class="Ta(start) Py(10px)"', anchor) > 0: 
    count += 1 
    start = r.find('class="Ta(start) Py(10px)"', anchor) 
    date_string = r[start-28:start-16]  
    date_time_obj = datetime.datetime.strptime(date_string,"%b %d, %Y") 

    div_beg_anchor = r.find('<strong', start) 
    div_start = r.find('>', div_beg_anchor) 
    div_end = r.find('</strong', div_start) 
    div_string = r[div_start+1:div_end] 

    div[date_time_obj] = [float(div_string),x ]

    anchor = r.find('class="Ta(start) Py(10px)',anchor+1) 

  return div 

#This takes the list of tickers and goes out to Yahoo and does a request on each ticker, multiple hits to server
def plot_fig(x): 
    for i in x:  
      try:
        key = list(ca_TA(i).values())       #get the dividend using ca_TA() function 
        v = np.diff([x[0] for x in key])*-1                 #gets the differece in div payout period over period 
     
        adfuller_results = adfuller(v) 
        one, five, ten = adfuller_results[4].values() #get the critial value at 1, 5 and 10 percent 
     
        fig, ax = plt.subplots()            #creates an empty figure to plot 
        ax.plot([x[0] for x in key][::-1], label='Div')     #plots the $ div payout in reverse order 
        ax.plot(v[::-1], label='Div_Rate')  #plot the diff in $ payout in reverse order 
       
        ax.legend() #adds legend to the figure 
       
        plt.text(0.20,0.7, i.capitalize() +'\n'+ 
          str('Std: '+ "%.2f" % np.std([x[0] for x in key],ddof=0))+'\n' 
            +'ADF Stat: {:.3f}'.format(adfuller_results[0])+'\n' 
            +'p-value: {:.3f}'.format(adfuller_results[1])+'\n' 
            +'1% Critical: '+'{:.3f}'.format(one)+'\n'+'5% Critical: '+'{:.3f}'.format(five)+'\n'+'10% Critical: '+'{:.3f}'.format(ten)+'\n', 
            horizontalalignment='left', verticalalignment='center', transform = ax.transAxes,fontsize=12) 
     
        fig.savefig(i) 
        fig.clf()
        plt.close()
      except Exception as e:
        print('Remove this ticker from list:'+i)
        print(e)
        continue

#This function will plot the data from the all_dividend.csv file after all_dividend function is ran
def plot_figAll(x):
    all = pd.read_csv(x)
    cc = ['Date', 'Dividend','Ticker']
    all.columns=cc 
    u = all.Ticker.unique()
    for i in u:
      try:
        key = all[all.Ticker==i].Dividend       #get the dividend using ca_TA() function
        v = np.diff(all[all.Ticker==i].Dividend)*1                 #gets the differece in div payout period over period

        adfuller_results = adfuller(v)
        one, five, ten = adfuller_results[4].values() #get the critial value at 1, 5 and 10 percent

        fig, ax = plt.subplots()            #creates an empty figure to plot
        ax.plot(key[::-1], label='Div')      #plots the $ div payout in reverse order
        ax.plot(v[::-1], label='Div_Rate')  #plot the diff in $ payout in reverse order

        ax.legend() #adds legend to the figure

        plt.text(0.20,0.7, 'nly' +'\n'+
          str('Std: '+ "%.2f" % np.std(key,ddof=0))+'\n'
          +'ADF Stat: {:.3f}'.format(adfuller_results[0])+'\n'
          +'p-value: {:.3f}'.format(adfuller_results[1])+'\n'
          +'1% Critical: '+'{:.3f}'.format(one)+'\n'+'5% Critical: '+'{:.3f}'.format(five)+'\n'+'10% Critical: '+'{:.3f}'.format(ten)+'\n',
          horizontalalignment='left', verticalalignment='center', transform = ax.transAxes,fontsize=12)
        fig.savefig(i)
        fig.clf()
        plt.close()
      except Exception as e:
        print('Remove this ticker from list:'+i)
        print(e)

def df_stat(x):
  d = []
  for i in x:
    try:
      key = [x[0] for x in list(ca_TA(i).values())]
      v = np.diff(key)*-1
 
      adfuller_results = adfuller(key) 
      one, five, ten = adfuller_results[4].values()

      lable = ['Comp_Name', 'STD', 'ADF_Stat','p-value','Crit_Value(1%)','Crit_Value(5%)','Crit_Value(10%)'] 
      l = [i,"%.4f" % np.std(key,ddof=0), 
              '{:.4f}'.format(adfuller_results[0]), 
              '{:.4f}'.format(adfuller_results[1]), 
              '{:.4f}'.format(one), '{:.4f}'.format(five), '{:.4f}'.format(ten)]

      d.append(l)
    except Exception as e:
      print('Remove this ticker from list:'+i)
      print(e)
      continue

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

def get_all_dividend_table(x):
  df1 = pd.DataFrame()
  sl = clean_stock_list(x)
  for i in sl:
    div_dic = ca_TA(i)
    dc = pd.DataFrame(div_dic).T.reset_index()
    df1 = df1.append(dc)
  df1.to_csv('all_dividends.csv',index=False)

#all_div[(all_div['index']>'2020-01-31') & (all_div['1']=='enb')]['0'].sum()

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
 

