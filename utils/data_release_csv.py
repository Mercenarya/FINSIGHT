import pandas as pd
import numpy as np
import os
import sys


#kiểm tra đường dẫn
def current_path(path:str):
    try: 
        return path if os.path.exists(path) else None
    except Exception as error:
        return f" <100> Error message - {error}"
    
#lọc và lấy giá trị của dict cho frame
def extract_list_frame(data:list):
    data_values = []
    data_keys = []
    try:
        for obj in range(len(data)):
            #nếu phần tử được duyệt là dictionary
            if isinstance(data[obj], dict):
                for key, value in data[obj].items():
                    data_keys.append(key)                    
                    data_values.append(value)
        return data_keys, data_values
    except Exception as error:
        return f"<101 - 2> Error message : {error}"
    
#lọc và lấy giá trị của dict
def extract_list(data:list):
    values_data = []
    try:
        for obj in range(len(data)):
            #nếu phần tử được duyệt là dictionary
            if isinstance(data[obj], dict):
                for key, value in data[obj].items():
                   values_data.append(value)
        return values_data
    except Exception as error:
        return f"<101 - 1> Error message : {error}"


#chuyển đổi các dũ liệu vào csv thành dữ liệu thô ban đầu
def convert_data_frame(values:list,path:str):
    try: 
       for obj in range(len(values)):
           pass

    except Exception as error:
        return f" <101> Error message - {error}"
    
if __name__ == "__main___":
    pass
