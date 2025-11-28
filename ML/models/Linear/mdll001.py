from sklearn.preprocessing import StandardScaler,scale
from sklearn import datasets,linear_model
import pandas as pd
import numpy as np


def slope(x, y) -> float:
    if len(x) != len(y):
        raise ValueError('X and Y is not same length')
    
    mean_x = mean(x)
    mean_y = mean(y)
    num = 0
    den = 0

    for w_x,w_y in zip(x,y):
        diff_x = w_x - mean_x
        diff_y = w_y - mean_y

        num += diff_x*diff_y
        den += diff_x**2
    if den == 0:
        return 0.0

    return num / den
    
def intercept(x, y, slope) -> float:
    return mean(y) - slope*mean(x)


def mean(data:list):
    result = sum(data)/len(data)
    return result


