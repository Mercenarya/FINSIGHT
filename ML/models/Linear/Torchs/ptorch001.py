import pandas as pd
import numpy as np
import os
import torch
import torch.nn as nn
from torch.autograd import Variable
from sklearn.preprocessing import MinMaxScaler, StandardScaler

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


class LNR(nn.Module):
    def __init__(self, input, output):
        # kế thừa module nn
        super(LNR,self).__init__()

        self.linear = nn.Linear(input,output)

    def forward(self,x):
        return self.linear(x)
    
# model
inp = 1
outnp = 1
model = LNR(inp,outnp)

# mse
mse = nn.MSELoss()

learning_rate = 0.001
optimizer = torch.optim.SGD(model.parameters(), learning_rate)


# chuẩn hóa số liệu
def normalize(data):
    scaler = StandardScaler()
    nml = scaler.fit_transform(data)
    return nml

    

# áp dụng Pytorch vào LNR ( y = x*w +b)
'''
ÁP dụng tính toán cho các bài toán dự đoán lợi
nhuận của doanh nghiệp ở mức cơ bản và trung bình
'''
arr = [
    [300000,220000,100000],#revenue
    [65000,700000,500000], #capital
    [450000,210000,50000] #Profit
]

data = np.array(arr)
print("Type : ",data.dtype)
print("Shape : ",np.shape(data))
tensor = torch.tensor(data)
print("Tensor type : ",tensor.type())
print("Tensor shape : ",np.shape(tensor))

model = model.float()


x_data = torch.tensor(arr[0],dtype=torch.float32)
y_data = torch.tensor(arr[2],dtype=torch.float32)

# chuyển đổi về numpy
x_data_np = x_data.numpy().reshape(-1,1)
y_data_np = y_data.numpy().reshape(-1,1)

# chuẩn hóa các giá trị
x_data_scaled = normalize(x_data_np)
y_data_scaled = normalize(y_data_np)

# chuyển đổi từ numpy sang lại tensor
x_data = torch.from_numpy(x_data_scaled).float()
y_data = torch.from_numpy(y_data_scaled).float()

# huấn luyện mô hình
epoc_list = []
epoch = 1000
for ep in range(epoch):

    # tối ưu hóa 
    optimizer.zero_grad()

    # lấy kết quả 
    results = model(x_data)

    # tính toán mức độ mất mát - loss
    loss = mse(results, y_data)

    loss.backward()

    optimizer.step()

    epoc_list.append(loss.data)

    if (ep % 100 == 0):
        print(f"Epoch {ep} LOSS : {loss.data}")










