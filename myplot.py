# myplot.py ### bokeh serve --show myplot.py ###

from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.driving import linear
from bokeh.models import Span
from yahoo_fin import stock_info as si
import numpy as np
from Graph_Processing import *

# region Create Graph and lines
p = figure(plot_width=800, plot_height=800)
r1 = p.line([], [], color="firebrick", line_width=2)
r2 = p.line([], [], color="orange", line_width=2)
r3 = p.line([], [], color="yellow", line_width=2)

ds1 = r1.data_source
ds2 = r2.data_source
ds3 = r3.data_source
# endregion

# region Create second graph for directional indicator
### Create second graph for directional indicator ###
p2 = figure(plot_width=800, plot_height=800)
s1 = p2.line([], [], color='green', line_width=2)
s2 = p2.line([], [], color='green', line_width=2)

ss1 = s1.data_source
ss2 = s2.data_source

x_axis = Span(location=0, dimension='width', line_color='black', line_alpha=0.4, line_width=2)
p2.add_layout(x_axis)
# endregion

# region Create a third graph to show accuracy of predictions
p3 = figure(plot_width=800, plot_height=800)
# endregion

# region global Variables
c = row(p, p2, p3)
step_count =[]
x_point = []
y_point = []
pred_peak = []
peaktpeak = []
# endregion

# region Choose stock ticker
ticker = 'MSFT'
# endregion

@linear()
def update(step):
    # region Get stock price
    price = si.get_live_price(ticker)
    # endregion

    # region Add new price to graph
    ds1.data['x'].append(step)
    ds1.data['y'].append(price)
    ds1.trigger('data', ds1.data, ds1.data)
    # endregion

    # region Create new list of x and y values
    xs2 = [(xs2.append(i) for i in range(len(ds1.data['x'])))]

    xs2 = np.array(ds1.data['x'], dtype=np.float64)
    ys2 = np.array(ds1.data['y'], dtype=np.float64)
    # endregion

    # region Create master list of step
    step_count.append(step)
    # endregion

    # region Add values to our line of best fit
    ds2.data['x'].append(step)
    if len(xs2) > 50:
        ds2.data['x'] = ds2.data['x'][-50:]
    ds2.data['y'] = regression_line(xs2,ys2,price)
    ds2.trigger('data', ds2.data, ds2.data)
    # endregion

    # region Add values to our moving average line
    ds3.data['x'].append(step)
    ds3.data['y'] = moving_average(ys2,price)
    ds3.trigger('data', ds3.data, ds3.data)
    # endregion

    # region Add values to our Directional indicator
    ss1.data['x'].append(step)
    ss1.data['y'] = directional_index(step_count, ys2, price)
    ss1.trigger('data', ss1.data, ss1.data)
    # endregion

    # region Plot prediction data
    try:
        x_distance, x_start, deviation, av_height, peaks = prediction_model(xs2,ys2,price)
        next_peak = Span(location=x_start+x_distance, dimension='height', line_color='green', line_alpha=0.1, line_width=2, line_dash='dashed')
        p2.scatter(x_start+x_distance, av_height, marker='circle', fill_color='red')

        p2.scatter(x_start, deviation, marker='square', fill_color='blue')
        
        x_point.append(x_start+x_distance)
        y_point.append(av_height)
        par = np.polyfit(x_point, y_point, 1, full=True)
        slope = par[0][0]
        intercept = par[0][1]
        y_predicted = [slope*i+intercept for i in x_point]
        
        ss2.data['x'] = x_point
        ss2.data['y'] = y_predicted
        ss2.trigger('data', ss2.data, ss2.data)

        p2.add_layout(next_peak)
        
        next_peak_corrected = Span(location=x_start+x_distance, dimension='height', line_color='green', line_alpha=0.1, line_width=2, line_dash='dashed')
        p.add_layout(next_peak_corrected)
        print(buy_sell(ss1.data['y'], slope, price))
        
        pred_peak.append(x_start+x_distance)
        accuracy = abs(pred_peak[-2], peaks[-1])
        
        p3.scatter(pred_peak[-2], accuracy, marker='circle')
        
    except TypeError:
        pass
    # endregion

# region Create HTML and Callback
### Create root file ###
curdoc().add_root(c)

### Add a periodic callback to be run every 500 milliseconds ###
curdoc().add_periodic_callback(update, 100)
# endregion
