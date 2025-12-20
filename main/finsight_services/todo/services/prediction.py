import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import os
import sys
import asyncio
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import random
import pickle
os.add_dll_directory('D:/Msys2/ucrt64/bin')
from libs import evaluate_module_update as ev
from .analysis import extract_finance_liquidity,read_data


# cấu hình đường dẫn
CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(CURRENT,'..','..')
sys.path.append(ROOT)

RAW = os.path.join(ROOT,'data')
ASSETS = os.path.join(RAW,'raw','assets001.csv')
REPORT = os.path.join(RAW,'raw','cleandpt001.csv')
PRCASSETS = os.path.join(ROOT,'data','processed','assetsprc001.csv')
DATASET = os.path.join(ROOT,"data","dataset","liquidity_dataset.csv")
NML = os.path.join(ROOT,"data","dataset","liquidity_nml.csv")

# lấy model được huấn luyện xong
MODEL_CASH = os.path.join(ROOT,'models','lq_cash_ratio.pth')
MODEL_QUICK_CURRENT = os.path.join(ROOT,'models','lq8.pth')

# mục chuẩn hóa số liệu
CASH_SCALER = os.path.join(ROOT,'models','liquidity_scaler.pkl')
# Y_SCALER = os.path.join(ROOT,'liquidity_y_scaler.pkl')
QUICK_CURRENT_SCALER = os.path.join(ROOT,'models','liquidity_x_scaler.pkl')
RAW_DIR = os.path.abspath(os.path.join(ROOT))
RAW = os.path.join(RAW_DIR,'data','raw','cleandpt001.csv')
ASSETS = os.path.join(RAW_DIR,'data','raw','assets001.csv')


LIBS = os.path.join(ROOT, 'libs') 
MODULE_DIR = os.path.join(ROOT, 'libs') 


'''
Dự báo chỉ số quick và current
- scale: các doanh nghiệp có báo cáo tài sản < 1B
'''
class QuickCurrent(nn.Module):
    def __init__(self, input, output):
        super(QuickCurrent,self).__init__()

        # chia các tập dữ liệu thành nhiều đặc trưng học
        self.neutrals = nn.Sequential(
            nn.Linear(input,75),
            nn.ReLU(),
            nn.Dropout(0.05),

            nn.Linear(75,56),
            nn.ReLU(),
            nn.Dropout(0.05),
            
            nn.Linear(56,output),
            nn.Softplus()
        )
    def forward(self, x):
        out = self.neutrals(x)
        # ép giá trị > 0
        return out



'''
Dự báo chỉ số cash ratio
- scale: các doanh nghiệp có báo cáo tài sản < 1B
'''

class CashRatio(nn.Module):
    def __init__(self, input, output):
        super(CashRatio,self).__init__()
        self.neutrals = nn.Sequential(
            # chia thành các cụm nơ ron để học các đặc trưng
            nn.Linear(input, 75),
            nn.ReLU(),

            nn.Linear(75,56),
            nn.ReLU(),

            nn.Linear(56,output),
            nn.Softplus()
        )

    def forward(self, x):
        out = self.neutrals(x)
        return out
    


# hàm dự đoán quick và current
async def predict_lq_current_qick(input_data):
    # lấy scaler
    x_scaler = joblib.load(QUICK_CURRENT_SCALER)
    # y_scaler = joblib.load(Y_SCALER)
    input_size = 4
    output_size = 2

    # tạo mô hình
    model = QuickCurrent(
        input=input_size,
        output=output_size
    )

    model.load_state_dict(torch.load(MODEL_QUICK_CURRENT, map_location='cpu'))
    model.eval()
    data = [x/1_000_000_000 for x in input_data]
    x_df = pd.DataFrame(
        [data],
        columns=['current_assets','liabilities','cash','inventory']
    )
    # chuyển đổi vector đầu vào
    # input = np.array(x_df).reshape(1,-1)

    # scale 
    x_scaled = x_scaler.transform(x_df)
    # chuyển về tensor
    tensor_input = torch.tensor(x_scaled, dtype=torch.float32)

    # predict
    with torch.no_grad():
        pred_scaled = model(tensor_input).numpy()

    result = pred_scaled

    return {
        'current_ratio': result[0][0],
        "quick_ratio": result[0][1]
        # "cash_ratio": result[0][2],
    }


# hàm dự đoán cash ratio
async def predict_lq_cash(input_data):
    # lấy scaler
    x_scaler = joblib.load(CASH_SCALER)

    # y_scaler = joblib.load(Y_SCALER)
    input_size = 2
    output_size = 1
    # hidden_size = 75

    # tạo mô hình
    model_cash = CashRatio(
        input=input_size,
        output=output_size
    )
    model_cash.load_state_dict(torch.load(MODEL_CASH, map_location='cpu'))
    model_cash.eval()

    data =  [float(x)/1_000_000_000 for x in input_data]
    x_df = pd.DataFrame(
        [data],
        columns=['liabilities','cash']
    )
    
    # chuyển đổi vector đầu vào
    # input = np.array(x_df).reshape(1,-1)

    # scale 
    x_scaled = x_scaler.transform(x_df)
    # chuyển về tensor
    tensor_input = torch.tensor(x_scaled, dtype=torch.float32)

    # predict
    with torch.no_grad():
        pred_scaled = model_cash(tensor_input).numpy()

    result = pred_scaled

    return {
        
        "cash_ratio": result[0][0],
    }

async def get_params(quarter):
    df = await read_data(ASSETS)
    predict_value = await extract_finance_liquidity(df=df,quarter=quarter)

    data = {
        'current assets':predict_value['current assets'],
        'liabilities':predict_value['liabilities'],
        'cash':predict_value['cash'],
        'inventory':predict_value['inventory']
    }
    print("Extracted specific data: ")
    print(data)

    return data


async def total_prediction(quarter):
    df = await read_data(ASSETS)
    print(df)
    # 'current_assets','liabilities','cash','inventory'
    # 'liabilities','cash'
    data = await get_params(quarter)
    print(data)
     # ví dụ đầu vào
    example_input_cash = [data['liabilities'], data['cash']]
    example_input_qc = [data['current assets'], data['liabilities'], data['cash'],data['inventory']]

    prediction_cash = await predict_lq_cash(example_input_cash)
    print("Dự đoán thanh khoản cash_ratio:", prediction_cash)

    prediction_quick_current = await predict_lq_current_qick(example_input_qc)
    print("Dự đoán thanh khoản quick_ratio và current_ratio: ",prediction_quick_current)
    
    template = {
        "prediction":[prediction_cash,prediction_quick_current]
    }
    print(template)
    return template

# if __name__ == "__main__":
#     asyncio.run(total_prediction())
   

