import pandas as pd
import numpy as np
from matplotlib import pyplot as plot

h = pd.read_csv('h.csv')
h['FCF_Mod'] = np.where(h['FCF'].str[-1] == 'M', h['FCF'].str[:-1].astype(float)/1000, h['FCF'].str[:-1].astype(float))
h['FCF_Key'] = h['FCF'].str[-1:]
