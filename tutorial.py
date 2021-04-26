from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from fbprophet import Prophet
import yfinance as yf
import pytz
from time import strftime
%config InlineBackend.figure_format = 'retina'


data = yf.Ticker('AAPL')
aapl = data.history(period='3d', interval='1m')

mav = aapl['Close'].rolling(window=50).mean()

aapl['ds'] = aapl.index
pd.to_datetime(aapl['ds'])
aapl['ds']=aapl['ds'].dt.tz_localize(None)
aapl['y'] = aapl['Close']

jh = aapl[['ds', 'y']]
jh_model = Prophet(interval_width=0.95)
jh_model.fit(jh)
jh_forecast = jh_model.make_future_dataframe(periods=180, freq='1min')
jh_forecast = jh_model.predict(jh_forecast)


ax = mav.plot(color='red')
jh_model.plot(jh_forecast, ax=ax)
plt.show()