import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

def get_min(data:list):
    min = data[0]
    for obj in range(len(data)):
        if min > data[obj]:
            min = data[obj]
    return min

def get_max(data:list):
    max = 0
    for obj in range(len(data)):
        if data[obj] > max:
            max = data[obj]
    return max

def scale_value(min,max,value):
    formula = (value - min) / (max - min)
    return formula

def get_scaled(data:list,min,max):
    scaled_data = []
    for obj in range(len(data)):
        data_scaled = scale_value(min,max,data[obj])
        scaled_data.append(data_scaled)
    return scaled_data

def get_ecdf(x):
    fg, ax = plt.subplots()
    ax.ecdf((x))
    plt.show()


if __name__ == "__main__":
    data = [10,15,22,45,30]
    min = get_min(data)
    max = get_max(data)
    print(min)
    print(max)
    data = get_scaled(data,min,max)
    get_ecdf(data)
    

