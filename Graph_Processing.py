import numpy as np
from statistics import mean
import pandas as pd
import math
from csaps import csaps
import scipy as sp
from scipy.signal import find_peaks
from scipy import stats

# region Global variables
old = 0
biggest_dif = 1
yar = []
money=1000
buy=False
# endregion

def regression_line(xs2, ys2, price):
    if len(xs2) > 50:
        xs2 = xs2[-50:]
        ys2 = ys2[-50:]
    
    ### Calculate the m and c values (y=mx+c) ###
    m = (((mean(xs2)*mean(ys2)) - mean(xs2*ys2)) /
         ((mean(xs2)*mean(xs2)) - mean(xs2*xs2)))

    c = mean(ys2) - m*mean(xs2)

    ### Collect the y values for each corresponding x value ###
    y = [(m*np.int64(x))+c for x in xs2]
    
    y = [price if math.isnan(x) else x for x in y]

    return y

def moving_average(y, price):
    number_series = pd.Series(y)
    windows = number_series.rolling(50)
    moving_averages = windows.mean()
    
    moving_list = moving_averages.tolist()
    
    moving_list = [price if math.isnan(x) else x for x in moving_list]
    
    return moving_list

def directional_index(xarn, y, price):
    global old
    global biggest_dif
    global yar
    global yi

    yar_percent = []
    
    difference = y[-1]-old
    
    if difference != price:
        yar.append(difference)
        if difference >= 0:
            if difference > biggest_dif:
                biggest_dif = difference
                for x in yar:
                    yar_percent.append((x/biggest_dif)*100)
            else:
                for x in yar:
                    yar_percent.append((x/biggest_dif)*100)
        else:
            if difference > biggest_dif:
                    biggest_dif = difference
            for x in yar:
                if x < 0:
                    yar_percent.append(yar_percent[-1]+((x/biggest_dif)*100))
                else:
                    yar_percent.append((x/biggest_dif)*100)

    else:
        yar.append(0)
        yar_percent.append(0)
        
    yar_percent = [0 if math.isnan(x) else x for x in yar_percent]
    
    num_series = pd.Series(yar_percent)
    window = num_series.rolling(10)
    mov_av = window.mean()
    
    mov_list = mov_av.tolist()
    
    mov_list = [0 if math.isnan(x) else x for x in mov_list]
    
    if len(xarn) >= 2:
        xi = np.linspace(xarn[0], xarn[-1], len(xarn))
        yi = csaps(xarn, np.array(mov_list), xi, smooth=0.0001)
    else:
        yi = [0,0]
    
            
    old = y[-1]
    
    return yi

def prediction_model(xam,y,price):
    global yi
    height = []
    
    peaks, _= find_peaks(yi)
    distance = [y-x for x, y in zip(peaks[:-1], peaks[1:])]
    
    if len(distance) > 2:
        average_distance = sum(distance)/len(distance)
        deviation = ((100*np.std(distance))/(sum(distance)/len(distance)))/100

    if len(distance) > 5:
        start_point = peaks[-1]
        for x in peaks:
            height.append(yi[x])
            
        average_height = sum(height)/len(height)
        
        return average_distance, start_point, deviation, average_height, peaks
    
    else:
        return

def buy_sell(yar, slope, price):
    global money
    global buy
    if slope > 0:
        if (yar[-1]) > 0 and buy ==  False:
            if (yar[-2]) > 0 and buy == False:
                money = money-(10*price)
                buy = True
            elif buy == True:
                money = money+(10*price)
                buy = False
            else:
                return money
        elif buy == True and (yar[-2]) < 0:
            money = money+(10*price)
            buy = False
        else:
            return money
    elif buy ==True:
        money = money+(10*price)
        buy = False
    else:
        return money
    
    return money

