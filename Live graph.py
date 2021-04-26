import matplotlib.pyplot as plt
import matplotlib.animation
import live
import numpy as np#
import pandas as pd
from statistics import mean
from yahoo_fin import stock_info as si

from labellines import labelLine, labelLines

# create plot
fig, (ax, ax2, ax3) = plt.subplots(1,3)

def animate(i):
    xs, ys, xar, yar, ticker, Estimations = live.plotting()
    xs = (xs)
    ys = (ys)

    # set up pandas dataframe to analyse data from
    df = pd.DataFrame(columns=['Date','Price','ma'])
    df['Date']=xar
    df['Price']=yar
    
    # calculate the rolling average for the last 50 data points
    df['ma'] = df.rolling(10).mean()
    x=df['ma'].tolist()
    x=x[-50:]
    
    # calculate line of best fit
    xs2 = []
    for i in range(len(xs)):
        xs2.append(i)
    
    xs2 = np.array(xs2, dtype=np.float64)
    ys2 = np.array(ys, dtype=np.float64)
    
    m = (((mean(xs2)*mean(ys2)) - mean(xs2*ys2)) /
         ((mean(xs2)*mean(xs2)) - mean(xs2*xs2)))
    
    b = mean(ys2) - m*mean(xs2)
    
    regression_line = [(m*np.int64(x))+b for x in range(len(xs))]
    
    if m > 0:
        DIC = 'green'
    elif m == 0:
        DIC = 'black'
    else:
        DIC = 'red'
    
    # Find and plot daily upper and lower limits
    table = si.get_quote_table(ticker, dict_result=False)
    limits = table.iloc[6]['value']
    low, high = np.array(limits.split(' - '), dtype=np.float64)
    
    # fetch analyst info
    analyst = si.get_analysts_info(ticker)
    EPS_revisions = analyst['EPS Revisions']
    EPS_trend = analyst['EPS Trend']
    Earnings_estimate = analyst['Earnings Estimate']
    Earnings_history = analyst['Earnings History']
    Growth_estimate = analyst['Growth Estimates']
    Revenue_estimate = analyst['Revenue Estimate']
    
    Growth_estimate_current = np.array(Growth_estimate.iloc[0][ticker].replace('%',''), dtype=np.float64)
    Growth_estimate_future = np.array(Growth_estimate.iloc[1][ticker].replace('%',''), dtype=np.float64)
    Surprise_history = np.array(Earnings_history.iloc[3][-1].replace('%',''), dtype=np.float64)
    Earnings_estimate_low = np.array(Earnings_estimate.iloc[2][-4], dtype=np.float64)
    Earnings_estimate_high = np.array(Earnings_estimate.iloc[3][-4], dtype=np.float64)
    
    Growth_estimate_current = ((Growth_estimate_current/100)+1)*ys[-1]
    Growth_estimate_future = ((Growth_estimate_future/100)+1)*ys[-1]
    Surprise_low = ys[-1]-(( Surprise_history/100)*ys[-1])
    Earnings_estimate_high = Earnings_estimate_high*ys[-1]
    Earnings_estimate_low = Earnings_estimate_low*ys[-1]

    ax.clear()
    ax.plot(xs, ys)

    if Estimations is True:
        ax3.axhline(y=low, xmin=0, xmax=1, color='orange', label='Low today')
        ax3.axhline(y=high, xmin=0, xmax=1, color='orange', label='High today')
        ax3.axhline(y=Growth_estimate_current, xmin=0, xmax=1, color='red', label='Groth estimate')
        ax3.axhline(y=Growth_estimate_future, xmin=0, xmax=1, color='red', label='Growth estimate future')
        ax3.axhline(y=Surprise_low, xmin=0, xmax=1, color='blue', label='Surprise low')
        ax3.axhline(y=Earnings_estimate_high, xmin=0, xmax=1, color='black', label='Earnings estimate high')
        ax3.axhline(y=Earnings_estimate_low, xmin=0, xmax=1, color='black', label='Earnings estimate low')
        ax3.plot(xs,ys, color=DIC)
  
    ax.plot(regression_line, color=DIC)
    ax.plot(x)

    ax2.plot(xar, yar, color=DIC)
    
ani = matplotlib.animation.FuncAnimation(fig, animate, interval =100, cache_frame_data=False)
plt.show()
