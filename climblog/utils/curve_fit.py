import datetime as dt
import numpy as np
import matplotlib.dates as mdates
from scipy.optimize import curve_fit

 
# Functions included in this file:
# # logistic_func

def logistic_func(x, a, b, c, d):
    return a * np.log(b * x + c) + d


def curve_fit_logistic_boundary(df, x:'%Y-%m-%d', y:int, p0=None):
    """Get logistic function parameters for boundary
    """

    # filter non-increasing grades
    while True:
        num_rows = len(df)
        df = df[(df[y]-df[y].shift().fillna(0) > 0)]
        if len(df) == num_rows:
            break

    popt, pcov = curve_fit(
        logistic_func,
        df[x].map(lambda x: dt.datetime.strptime(x, "%Y-%m-%d")).map(lambda x: mdates.date2num(x)),
        df[y],
        p0=p0
    )
    return popt
