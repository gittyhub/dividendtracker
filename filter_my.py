import pandas as pd
import numpy as np
from matplotlib import pyplot as plot

my = pd.read_csv('my.csv')
shares = pd.read_csv('share.csv')
my = my.join(shares.set_index('Ticker'), on='Ticker')
my['Value'] = my['Price']*my['Shares']
my.loc[my['Ticker']=='mcn', ['Industry','Sector']]=['Asset Management','Financial Services']
my['FCF_Mod'] = np.where(my['FCF'].str[-1] == 'M', my['FCF'].str[:-1].astype(float)/1000, my['FCF'].str[:-1].astype(float))
my['FCF_Key'] = my['FCF'].str[-1:]
