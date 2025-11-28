import numpy as np
import pandas as pd
import sklearn
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import os
import sys
import threading

# mẫy mô hình hồi quy tuyến tính


'''Tạo đường dẫn tới dữ liệu thô ,
 nhằm mục đích chuẩn hóa số liệu và lọc dữ liệu'''
# đường dẫn hiện tại
ORIGIN = os.path.dirname(os.path.abspath(__file__))
# đường dẫn dự án
ROOT = os.path.join(ORIGIN,'..','..')
# đường đẫn đến dữ liệu thô
RAW = os.path.join(ROOT,'data','raw','cleanedpt001.csv')
# đường dẫn đến xử liệu đã được xử lí
PRC = os.path.join(ROOT,'data','processed','processed.csv')


# lớp dự đoán tài chính
class ProfitChange:
    def __init__(self,data,define,):
        pass
    # tạo phiên luồng theo số lượng sesssion
    def thread_prcss(session:int):
        pass


    


# kiểm tra và lấy dữ liệu
def read_data(file:str):
    try:
        if os.path.exists(file):
            print("Exists path")
            df = pd.read_csv(file, encoding='utf-8')
            # thay các giá trị nan thành 0
            cleand_dt = df.replace(np.nan, 0)
            return cleand_dt
        else:
            print(f"None Path {file}")
            return None
    except Exception as error:
        return f"ERROR : {error}"

# lọc các dữ liệu string và chuyển sang dạng số
def type_detect(data):
    digit_type = []
    for obj in range(len(data)):
        if isinstance(data[obj], (int,float)):
            digit_type.append(float(data[obj]))

        # điều kiện lọc dũ liệu
        if isinstance(data[obj],str):
            cleant = data[obj].replace(',','')
            digit_type.append(float(cleant))

    return digit_type

# lọc theo số liệu chỉ định (internal data)
def type_detect_internal(define,num:int,start:int,end:int):
    cleanpt = define.iloc[num, start:end ].replace(',','',regex=True).astype(float)
    return cleanpt
            


# bộ lọc dữ liệu - file
def filters_file(file:str):
    try:
        df = read_data(file)
        
        '''
        các tiện hàm hỗ trợ bộ lọc sẽ được trưng
        dụng ở ngoài, đảm bảo 
        '''  
        
        # trích các cột " Quý "
        title = df['Title']
        quarter_1 = df['Quarter 1']
        quarter_2 = df['Quarter 2']
        quarter_3 = df['Quarter 3']
        quarter_4 = df['Quarter 4']

        # chuyển đổi string (lọc và ép kiểu)
        q1 = type_detect(quarter_1)
        q2 = type_detect(quarter_2)
        q3 = type_detect(quarter_3)
        q4 = type_detect(quarter_4)

        # mẫu dữ liệu - Dict
        templates ={
            'Title':title,
            'quarter_1':q1,
            'quarter_2':q2,
            'quarter_3':q3,
            'quarter_4':q4   
        }

        return templates
    
    except Exception as error:
        return f"ERROR : {error}"


# lọc giá trị theo hàng để so khớp dữ liệu gốc
def frame_filters(data,num:int):
    try:
        df = read_data(data)
        row = df.iloc[num]
        # col = df.loc['quarter_4']
        return row
    except Exception as error:
        return f"ERROR Frame Fill : {error}"




# chuẩn hóa các giá trị theo Z-score
def normalize_score(data:list):
    

    # trung bình cộng
    noo = len(data)
    means = sum(data)/noo

    # standard devi
    std_devi_fml = sum([(value - means)**2 for value in data ])/noo
    std_devi = np.sqrt(std_devi_fml)

    #chuẩn hóa bước cuối (Z-score)
    formula = [(x-means)/std_devi for x in data]
    return formula

def chart_perform(x,y):
    pass


# huấn luyện ban đầu
def training_lnr():
    '''
    Mẫu thử data dự đoán lợi nhuận
    trong tương lai thong qua 3 giá trị
    - doanh thu
    - lợi nhuận
    - Giá vốn
    '''
    # lấy dữ liệu chuẩn hóa
    df = pd.read_csv(PRC)
    
    # đầu ra dữ liệu (quý gần nhất - quý 4)
    revenue = df.iloc[2,1:5].values.reshape(-1,1)
    capit = df.iloc[3,1:5].values.reshape(-1,1)
    pft = df.iloc[18,1:5].values.reshape(-1,1)


    #tạo vector - xây dựng output (2 đặc trưng: x - y )
    '''Dùng quý 1 đến quý 3 để huấn luyện
    dữ liệu , sau đó dùng quý 4 để dự đoán
    giá trị lợi nhuận cho quý tiếp theo'''
    x_train = np.hstack((revenue[:3], capit[:3])) 
    y_train = pft[:3].ravel()

    x_test = np.array([[float(revenue[3].item()), float(capit[3].item())]])
    # Mô hình huấn luyện
    model = linear_model.LinearRegression()
    model.fit(X=x_train,y=y_train)
    
    # dự đoán lợi nhuận
    next_quarter = model.predict(x_test)
    # chuyển đổi giá trị tiền tệ thật 
    raw = pd.read_csv(RAW)
    mean_pft = type_detect_internal(raw,18,1,5)
    std_pft = type_detect_internal(raw,18,1,5)
    
    # công thức chuyển đổi lại giá trị (x=z⋅σ+μ)
    real_nq = (next_quarter[0] * std_pft.std()) + mean_pft.mean()


    data = pd.DataFrame(
        {
            'Revenue':revenue.flatten(),
            'Capital':capit.flatten(),
            'Profit':pft.flatten()
        }
    )
    # kết quả dự đoán lợi nhuận
    result = {
        'Next Quarter (Profit) : ':real_nq
    }

    return data,result





# chuyển các dữ liệu chuẩn hóa vào một csv đặc thù
def nml_data_modified(tt:list, q1:list, q2:list, q3:list, q4:list):
    try:
        data = {
            'Title':tt, # title ( nội dung riêng biệt ko chuẩn hóa)
            'quarter_1':q1, # giá trị quý  của các nội dung đã chuẩn hóa
            'quarter_2':q2, # giá trị quý  của các nội dung đã chuẩn hóa
            'quarter_3':q3, # giá trị quý  của các nội dung đã chuẩn hóa
            'quarter_4':q4 # giá trị quý  của các nội dung đã chuẩn hóa
        }
        df = pd.DataFrame(
            data=data
        )
        # chuyển thư mục chứa đựng dữ liệu xử lí
        df.to_csv(PRC,encoding='utf-8',index=False)
        return df

    except Exception as error:
        return f'DATA MODIFIED ERROR : {error}'




if __name__ == "__main__":
    
    # lấy các dữ liệu chỉ định từ mục dữ liệu đã xử lí
    revenue = frame_filters(PRC,0)
    print(revenue)
    
    print("--"*100)
    data,result = training_lnr()
    print(data)
    print(result)
    print("--"*100)









    
        
    
    

