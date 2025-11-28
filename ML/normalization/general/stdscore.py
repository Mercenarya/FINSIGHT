import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


def means(data:list):
    noo = len(data)
    return sum(data)/noo

def standard_deviation(data:list,mean):
    formula =  sum([np.pow((value - mean),2) for value in data])/len(data)
    return np.sqrt(formula)

def normalization(data:list,mean,devi):
    formula = [(x-mean)/devi for x in data ]
    return formula

if __name__ == "__main__":
    x = [2, 3, 4, 5, 6]
    mean = means(x)
    data = standard_deviation(x,mean)
    print(round(data,2))
    norm = normalization(x,mean,data)
    obj = [round(value,2) for value in norm]
    print(obj)
    
    