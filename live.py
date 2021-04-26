# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 17:08:38 2020

@author: jimbobewenhall
"""

# ipython configuration
#%matplotlib inline
#%config InlineBackend.figure_format='retina'

# import stock_info module from yahoo_fin
from yahoo_fin import stock_info as si

import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from statistics import mean
import numpy as np

# set value variables to null
xar = []
yar = []

xar_short = []
yar_short = []

# Choose variables
ticker = 'TSLA'
Estimations = True
Legend = True

def plotting():
    
    # get current price and time
    price = si.get_live_price(ticker)
    now = datetime.now()
    
    # append these values to the previously created lists
    yar.append(price)
    xar.append(now.strftime("%H:%M:%S"))
    
    yar_short.append(price)
    xar_short.append(now.strftime("%H:%M:%S"))
    
    # remove last value from list to ensure only 50 data points are displayed
    if len(xar)>50:
        xar_short.pop(0)
        yar_short.pop(0)
    
    
    return xar_short, yar_short, xar, yar, ticker, Estimations, price
