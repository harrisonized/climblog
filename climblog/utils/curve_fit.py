import numpy as np
 
# Functions included in this file:
# # logistic_func

def logistic_func(x, a, b, c, d):
    return a * np.log(b * x + c) + d
