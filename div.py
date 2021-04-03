import urllib.request
import pandas as pd
import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Get stock data from file of tickers')
#parser.add_argument('-d','--div_yield', type=str, metavar = '', help='sort the dividend yield highest to lowest')
#parser.add_argument('-sd','--sort_div', metavar = '',  action='store_true', help='sort by dividend yield highest to lowest')
parser.add_argument('-inf','--input_file', type=str, metavar = '', help='file of tickers to process')
parser.add_argument('-exp','--export_csv', type=str, metavar = '', help='expot csv file name, enter name after flag')
group = parser.add_mutually_exclusive_group()
group.add_argument('-sdY','--sort_div', action='store_true', help='sort by dividend yield highest to lowest')
group.add_argument('-si','--sort_indust', action='store_true', help='sort by industry')
args = parser.parse_args()


def site(x):
  d =  {}
  site = 'https://finance.yahoo.com/quote/'+x+'?p='+x+'&.tsrc=fin-srch'
  request = str(urllib.request.urlopen(site).read())
  d['Ticker'] = x
  
  name = {'name':'pageData":{"title', 'title':'title', 'find_end':')', 'beg':8, 'end': 1} 
  industry = {'name': 'address1', 'title':'industry', 'find_end':',', 'beg':11, 'end':-1}
  sector = {'name': 'zip":', 'title':'sector', 'find_end':',', 'beg':9, 'end':-1} 
  div_yield = {'name': 'dividendYield":', 'title':'fmt', 'find_end':',', 'beg':6, 'end':-2} 
  ex_div = {'name': 'exDividendDate":', 'title':'fmt', 'find_end':',', 'beg':6, 'end':-2} 
  price_to_book = {'name': 'priceToBook":', 'title':'fmt', 'find_end':',', 'beg':6, 'end':-2} 
  div_rate = {'name': 'dividendRate":', 'title':'fmt', 'find_end':',', 'beg':6, 'end':-2} 
  
  label = ['Comp_Name', 'Industry', 'Sector', 'Div_Yield', 'Div_Rate','Ex_Div', 'Price2Book']
  l = [name , industry, sector, div_yield, div_rate, ex_div, price_to_book]  #need to add a try to handle stocks with no div
  for i,e  in zip(l, label):
    anchor = request.find(i.get('name'))
    find_cat = request.find(i.get('title'), anchor)
    find_end = request.find(i.get('find_end'), find_cat)
    if request.find('}',request.find('{', anchor)) - request.find('{',anchor) < 2 and e == 'Price2Book':
      d[e] = 0
    else:
      final = request[find_cat+i.get('beg'):find_end+i.get('end')]
      d[e] = final.strip('"')
   
  return d

def clean_stock_list(x):
  #if there is a new line at end of file script wont work properly 
  #if you mess up and have a blank between commas it will also mess up 
  f = open(x,'r').read().splitlines()
  f = [i.split(',') for i in f]
  f = [i.strip() for s in f for i in s]
  return f

def create_table(x):
  pan = pd.DataFrame()
  for i in x:
    pan = pan.append(site(i), ignore_index=True)
  return pan
 
def sort_div(x):
    print(x.sort_values(by=['Div_Yield']))

def sort_indust(x):
    print(x.sort_values(by=['Industry']))

def exp_csv(x):  
    #create_table(clean_stock_list(file)).to_csv(args.export_csv, index='True')
    x.to_csv(args.export_csv, index='True')
 
if __name__=="__main__":
  #reference:https://www.geeksforgeeks.org/command-line-interface-programming-python/
  #reference:https://www.youtube.com/watch?v=cdblJqEUDNo
  '''This program takes a list of tickers and return dividend information on each.
  All parser argument have to be used with the input_file flag. If ran with no flag
  default file high_yield.txt will be used'''
  #add fof and cagr
  file = 'high_yield.txt' 
  i = args.input_file
  if args.sort_div:
    sort_div(create_table(clean_stock_list(i)))
  elif args.sort_indust:
    sort_indust(create_table(clean_stock_list(i)))
  elif args.export_csv:
    exp_csv(create_table(clean_stock_list(i)))
  else: 
    print(create_table(clean_stock_list(file)))


