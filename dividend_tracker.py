import urllib.request
import pandas as pd
import os
import sys
import argparse
import time
import requests
import numpy as np

parser = argparse.ArgumentParser(description='Get stock data from file of tickers')
parser.add_argument('-inf','--input_file', type=str, metavar = '', help='file of tickers to process')
parser.add_argument('-exp','--export_csv', type=str, metavar = '', help='expot csv file name, enter name after flag')
group = parser.add_mutually_exclusive_group()
group.add_argument('-sdY','--sort_div', action='store_true', help='sort by dividend yield highest to lowest')
group.add_argument('-si','--sort_indust', action='store_true', help='sort by industry')
args = parser.parse_args()

header = {'User-agent':'Mozilla/5.0'}

def site(x):
  d =  {}
  site = 'https://finance.yahoo.com/quote/'+x+'?p='+x+'&.tsrc=fin-srch'
  #request = str(urllib.request.urlopen(site).read())
  request = str(requests.get(site,headers=header).content)
  d['Ticker'] = x
  
  name = {'name':'pageData":{"title', 'title':'title', 'find_end':')', 'beg':8, 'end': 1} 
  industry = {'name': 'address1', 'title':'industry', 'find_end':',', 'beg':11, 'end':-1}
  sector = {'name': 'zip":', 'title':'sector', 'find_end':',', 'beg':9, 'end':-1} 
  div_yield = {'name': 'dividendYield":', 'title':'fmt', 'find_end':',', 'beg':6, 'end':-3} 
  ex_div = {'name': 'exDividendDate":', 'title':'fmt', 'find_end':',', 'beg':6, 'end':-2} 
  price_to_book = {'name': 'priceToBook":', 'title':'fmt', 'find_end':',', 'beg':6, 'end':-2} 
  div_rate = {'name': 'dividendRate":', 'title':'fmt', 'find_end':',', 'beg':6, 'end':-2} 
  quickRatio = {'name': 'quickRatio":', 'title':'fmt', 'find_end':',', 'beg':6, 'end':-2} 
  totalCashPerShare = {'name': 'totalCashPerShare":', 'title':'fmt', 'find_end':',', 'beg':6, 'end':-2} 
  currentPrice = {'name': 'currentPrice":', 'title':'fmt', 'find_end':',', 'beg':6, 'end':-2} 
  
  label = ['Comp_Name', 'Industry', 'Sector', 'Div_Yield', 'Div_Rate','Ex_Div', 'Price2Book', 'QuickRatio', 'Tot.Cash/Share', 'Price']
  l = [name , industry, sector, div_yield, div_rate, ex_div, price_to_book, quickRatio, totalCashPerShare, currentPrice] 
  for i,e  in zip(l, label):
    anchor = request.find(i.get('name'))
    find_cat = request.find(i.get('title'), anchor)
    find_end = request.find(i.get('find_end'), find_cat)
    #if request.find('}',request.find('{', anchor)) - request.find('{',anchor) < 2 and e == 'Price2Book':
    if request.find('}',request.find('{', anchor)) - request.find('{',anchor) < 2:
      d[e] = 0
    else:
      final = request[find_cat+i.get('beg'):find_end+i.get('end')]
      d[e] = final.strip('"')
   
  return d


def cashFlow1(y):
  '''Goes to yahoo cash flow page and gets cashflow of each company. Returns all cf as a dataframe'''
  #Can not add this function to site because it will only do a few before returning 0 cf. 
  #Running it sepearately and joining it after works best
  d =  {}
  for x in y:
    site = 'https://finance.yahoo.com/quote/'+x+'/cash-flow?p='+x
    request = str(requests.get(site,headers=header).content)
    s = request.find('annualFreeCashFlow')  
    e = request.find(']', s)
    f = request[s+20:e+1]
    fs= f.strip('[]').split(',')
    fcf = fs[-1].find(':')
    fcf_beg = fs[-1].find('"',fcf)
    fcf_end = fs[-1].find('"',fcf+2)
    d[x] = fs[-1][fcf_beg+1:fcf_end]
 
  df = pd.DataFrame.from_dict(d, columns=['FCF'], orient='index') 
  df.reset_index(inplace=True)
  df = df.rename(columns = {'index':'Ticker'})
  return df

def clean_stock_list(x):
  '''Open specified text file of ticker and puts them in a list for processing, returns list of ticker'''
  #if there is a new line at end of file script wont work properly 
  #if you mess up and have a blank between commas it will also mess up 
  f = open(x,'r').read().splitlines()
  f = [i.split(',') for i in f]
  f = [i.strip() for s in f for i in s]
  return set(f)

def create_table(x):
  '''Takes a list of tickers, grabs data needed, and appends them to a dataframe'''
  pan = pd.DataFrame()
  for i in x:
    pan = pan.append(site(i), ignore_index=True)
  return pan
 
def sort_div(x):
  print(x.sort_values(by=['Div_Yield']))

def sort_indust(x):
  print(x.sort_values(by=['Industry']))

def exp_csv(x):  
  #create_table(clean_stock_list(file)).to_csv(args.export_csv, index='False')
  x.to_csv(args.export_csv, index=False)


def cleanup_high(x):
  x['M_FCF'] = np.where(x['FCF'].str[-1] == 'M', x['FCF'].str[:-1].astype(float)/1000, x['FCF'].str[:-1].astype(float))
  col_loc = list(x.columns).index('FCF')
  MFCF = x.pop('M_FCF')
  x.insert(col_loc,'M_FCF',MFCF) #going to pop FCF but just incase it matters later
  #x.drop(['FCF'], axis=1)
  return x
 
 
def cleanup_shares(x,s):
  clean_df = x.loc[x['Ticker'] != 'gmlpf']
  clean_df = clean_df.join(s.set_index('Ticker'), on='Ticker')
  clean_df['Value'] = clean_df['Price']*clean_df['Shares']
  clean_df.loc[clean_df['Ticker']=='mcn', 'Industry'] = 'Asset Management'   
  clean_df.loc[clean_df['Ticker']=='mcn', 'Sector'] = 'Financial Services'  

  clean_df['M_FCF'] = np.where(clean_df['FCF'].str[-1] == 'M', clean_df['FCF'].str[:-1].astype(float)/1000, clean_df['FCF'].str[:-1].astype(float))
  col_loc = list(x.columns).index('FCF')
  MFCF = clean_df.pop('M_FCF')
  clean_df.insert(col_loc-1,'M_FCF',MFCF) #going to pop FCF but just incase it matters later
  #clean_df.drop(['FCF'], axis=1)
  return clean_df

def divlookup(t,d):
  return div_his[div_his['1']==t & (div_hist['index']>'2020-01-01')]  
   
if __name__=="__main__":
  #reference:https://www.geeksforgeeks.org/command-line-interface-programming-python/
  #reference:https://www.youtube.com/watch?v=cdblJqEUDNo
  '''This program takes a list of tickers and return dividend information on each.
  All parser argument have to be used with the input_file flag. If ran with no flag
  default file high_yield.txt will be used'''

  #add fof and cagr
  #file = 'high_yield.txt' 
  file = 'high_yield_ticker.txt' 
  i = args.input_file
  if args.sort_div:
    sort_div(create_table(clean_stock_list(i)))
  elif args.sort_indust:
    sort_indust(create_table(clean_stock_list(i)))
  elif args.export_csv:
    j = cashFlow1(clean_stock_list(i))
    s = create_table(clean_stock_list(i))
    df = s.join(j.set_index('Ticker'), on='Ticker')
    exp_csv(df)
  else: 
    print(create_table(clean_stock_list(file)))

