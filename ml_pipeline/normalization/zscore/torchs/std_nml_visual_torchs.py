import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import asyncio

# configuration
CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(CURRENT,'..','..','..','..')
RAW = os.path.join(ROOT,'data','raw','cleanedpt001.csv')


# xử lí các kiểu dữ liệu ngoại lệ
def replace_datatype(obj):

    if isinstance(obj, str):
        return float(obj.replace(',',''))
    if isinstance(obj, (int,float)):
        return obj
    return 0.0
    

# đọc dữ liệu từ csv gốc 
def read_data(filename:str):
    try:
        if os.path.exists(filename):
            print("Exists path : ",filename)
            df = pd.read_csv(filename)
            # chuyển đổi các giá trị NaN thành 0
            cleandt = df.replace(np.nan, 0)
            return cleandt
        else: return None
    except OSError as oserr:
        return f"OS error : {oserr}"
    except Exception as error:
        return f"General error : {error}"
    

    
def normlization(df,columns):
    try:
        
        # lấy giá trị của columns cụ thể
        data = df[[columns]].values

        # stdscore == Z-score()
        scaler_std = StandardScaler()

        # chuẩn hóa các giá trị đầu vào
        nml_std = scaler_std.fit_transform(data)
        # trà về flattern (1D Arrays)
        return nml_std.flatten()


    except Exception as error:
        return f"Normalization Error {error}" 



# Hiển thị quá trình chuẩn hóa dữ liệu ( sử dụng đồng bộ )
async def chart_point_recieve(x_point):
    # kiểm tra điều kiện giá trị đầu vào
    if not isinstance(x_point,list) and not isinstance(x_point, np.ndarray):
        print("x_point is not an array")
        return
    
    else:
        '''
        Hiển thị quá trình chuẩn hóa theo thời gian thực 
        - datapoint : chứa dữ liệu được chuẩn hóa
        - countpoint : ghi lại số lượng chuẩn hóa theo đợt
        '''
        datapoint = []
        countpoint = []
        for obj in range(len(x_point)):
            datapoint.append(x_point[obj])
            countpoint.append(obj+1)
            plt.ion()
            plt.xlabel = "Phase number"
            plt.ylabel = "Normalized values"
            plt.plot(countpoint,datapoint, marker="o")
            plt.draw()
            plt.pause(1)
            print(f"Phase {obj+1} - values : {x_point[obj]}")

    
# đồng bộ quá trình chạy 
async def update_nml_data(x_point):
    await chart_point_recieve(x_point)
    await asyncio.sleep(1)



if __name__ == "__main__":
    try:
        prc_data = read_data(RAW)
        # chuẩn hóa dữ liệu mẫu ở cột quarter 1 của các nội dung BCTC
        prc_data['Quarter 1'] = prc_data['Quarter 1'].apply(replace_datatype)
        print(prc_data['Quarter 1'])
        # lấy kích thươcs dữ liệu
        data_length = len(prc_data['Quarter 1'])
        print("Data Length : ",data_length)
        x_point = normlization(prc_data,'Quarter 1')
        print(list(x_point))
        
        asyncio.run(update_nml_data(x_point))
    except asyncio.exceptions.CancelledError:
        print("Cancled running for Async errors")
    except asyncio.exceptions as ascerror:
        print("Async error : ",ascerror)
    except Exception as error:
        print("General errors : ",error)