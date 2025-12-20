import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import os
import sys

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




def read_data(filename:str):
    try:
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            df.replace(np.nan, 0)
        return df

    except Exception as error:
        return f'error : {error}'

def training_pt():
    df = read_data(PRC)
    # đầu ra dữ liệu (Quý gần nhất - quý 4)
    revenue = df.iloc[2,1:5].values.reshape(-1,1)
    capit = df.iloc[3,1:5].values.reshape(-1,1)
    pft = df.iloc[18,1:5].values.reshape(-1,1)

    x_train = np.hstack((revenue[:3], capit[:3]))
    y_train = pft[:3].ravel()


    







def training_lnr():
    df = read_data(PRC)
    # đầu ra dữ liệu (quý gần nhất - quý 4)
    revenue = df.iloc[2,1:5].values.reshape(-1,1)
    capit = df.iloc[3,1:5].values.reshape(-1,1)
    pft = df.iloc[18,1:5].values.reshape(-1,1)


    x_train = np.hstack((revenue[:3], capit[:3]))
    y_train = pft[:3].ravel()

    # chuyển đổi sang tensor
    X = tf.constant(x_train, dtype=tf.float32)
    Y = tf.constant(y_train, dtype=tf.float32)

    # lấy kích thước dữ liệu
    n = len(x_train)


    W = tf.Variable(np.random.normal(shape=(2,1)), name='Weight')
    B = tf.Variable(np.random.normal(shape=(2,1)), name='Bias')

    LNR = 0.01
    EPC = 1000

    # Khởi tạo tối ưu hóa
    optimizer = tf.optimizers.SGD(learning_rate=LNR)

    # hàm dự đoán
    def predict(X, W, B):
        return tf.matmul(X,W) + B
    

    # hàm mất mát - sai số trung bình MSE 
    def loss_fn(y_true, y_pred):
        # giảm thiểu sai số bình phương
        return tf.reduce_mean(tf.square(y_true - y_pred))
    
    '''bắt đầu quy trình huấn luyện'''

    for epoch in range(EPC):
        with tf.GradientTape() as tape:
            # tính toán dự đoán 
            y_pred = predict(X , W , B)
            # tính giá trị mất mát
            current_loss = loss_fn(Y, y_pred)

        # đạo hàm hàm mất mát W và B
        gradients = tape.gradient(current_loss , [W , B])

        # cập nhật giá trị W và B ( thuật toán Gradient Descent)
        optimizer.apply_gradients(zip(gradients, [W,B]))

        # giá trị mất mát sau mỗi lần học
        if (epoch + 1) % 100 == 0:
            print(f"Epoch {epoch}, loss: {current_loss}")

        print("TOTAL")
        print(f"Weight (Revenue,Capital): {W}")
        print(f"Bias : {B}")

        x_test = np.hstack((revenue[3:].item(), capit[3:].item() )).astype(np.float32)
        X_test = tf.constant(x_test, dtype=tf.float32)

        if len(X_test) > 0:
            predictions = predict(X_test, W, B)
            print("Forecast for Profit in next quarter : ",predictions)

if __name__ == "__main__":
    training = training_lnr()
    print(training)