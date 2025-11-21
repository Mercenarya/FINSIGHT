import pandas as pd
import numpy as np
import os
import sys
import datetime


current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(current_dir, '..')
sys.path.append(root)

from utils.comm_functions import save_to_csv,seed_path,save_to_json,looping_json
# from utils.comm_functions import PATH,JSNRP,JSNAS


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


#lọc và lấy dữ liệu theo keys , values
def extract_keys(data:list):
    
    #silos ( các list chuyên biệt )
    tt = []
    qt1 = []
    qt2 = []
    qt3 = []
    qt4 = []

    


    try:
        
        for obj in range(len(data)):
            if isinstance(data[obj], dict):
                
                # lấy các giá trị extract từ phần tử duyệt được - 
                # phần này dành cho dataframe để xử lí csv
                title = data[obj].get("title")
                q1 = data[obj].get("First")
                q2 = data[obj].get("Second")
                q3 = data[obj].get("Third")
                q4 = data[obj].get("Fourth")
                
                #thêm các giá trị extract từ dict vào mỗi silos (các list riêng)
                tt.append(title)
                qt1.append(q1)
                qt2.append(q2)
                qt3.append(q3)
                qt4.append(q4)
        

        return tt,qt1,qt2,qt3,qt4
    except Exception as error:
        print(
            {
                "tt":len(tt),
                "qq1":len(qt1),
                "qq2":len(qt2),
                "qq3":len(qt3),
                "qq4":len(qt4)
            }
        )
        return f"<101 - 1> Error message : {error}"





#chuyển đổi các dũ liệu vào csv thành dữ liệu thô ban đầu
def convert_data_frame(tt:list,qq1:list,qq2:list,
                       qq3:list,qq4:list,path:str):
    try: 
        '''
        data_len đảm nhiệm vai trò là kiếm chứng
        lượng dữ liệu nạp vào từng silos trước đó
        nếu 1 trong các silos dữ liệu ko cân bằng với 
        4 dữ liệu còn lại thì sẽ dẫn đến lỗi ở mặt 
        chuyển đổi dữ liệu của pandas 
        '''
        #trực quan lượng dữ liệu
        data_len = {
            "Title" : len(tt),
            "QQ1" : len(qq1),
            "QQ2" : len(qq2),
            "QQ3" : len(qq3),
            "QQ4" : len(qq4)
        }

        # chia cột dữ liệu
        data = {
            "time: ":datetime.datetime.now(),
            "Title":tt,
            "Quarter 1": qq1,
            "Quarter 2": qq2,
            "Quarter 3": qq3,
            "Quarter 4": qq4
        }

        df = pd.DataFrame(data)
        print(seed_path(path))
        print(save_to_csv(
            path,df
        ))
        return df


    except Exception as error:
        return f" <101> Error message - {error}"
    
if __name__ == "__main___":
    pass
