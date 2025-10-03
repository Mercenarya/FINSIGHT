from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import unidecode
import requests
import pandas as pd
import numpy as np
import os
import sys
import re
import json

#lớp dữ liệu doanh thu
class Revenue:
    def __init__(self,title,q1,q2,q3,q4,timeline:list):
        self.title = title
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.timeline = timeline

    # dữ liệu dạng dict
    def get_data(self):
        return {
            "title":self.title,
            "First":self.q1,
            "Second":self.q2,
            "Third":self.q3,
            "Fourth":self.q4,
            "Timeline":self.timeline
        }
    
    def __repr__(self):
        return f"< Revenue {self.title} : {self.q1} - {self.q2} - {self.q3} - {self.q4} - Timeline: {self.timeline}"

id_class = ['01','02','10','11','20','21','22','23','24','25','26','30','31','32','40','50','51','52','60','61','62','70','71']
'''
['01','02','10','11','20','21','22','23','24','25','26','30','31','32','40','50','51','52','60','61','62','70','71']
'''

def resfresh_data(driver:webdriver.Chrome):
    '''
    Tải lại dữ liệu báo cáo từ trangm
    nhằm cập nhật các thông số, biểu đồ và 
    các dữ liệu sửa đổi mới nhất
    '''
    pass

#dữ liệu quý hiện tại
def current_timeline(driver:webdriver.Chrome):
    
    tb = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID, 'tblGridData'))
    )
    timeline_row = tb.find_elements(By.CLASS_NAME, 'h_t')

    tl1 = timeline_row[0].text
    tl2 = timeline_row[1].text
    tl3 = timeline_row[2].text
    tl4 = timeline_row[3].text

    return tl1,tl2,tl3,tl4


#dữ liệu quý trước
def previous_timeline(driver:webdriver.Chrome):
    try:
        button = driver.find_element(By.XPATH, "//img[@alt='Xem dữ liệu trước']/parent::a")
        button.click()
        print("Switch timeline to previous ... ")
    except Exception as error:
        return f"previous timeline err - {error}"

#dữ liệu quý tiếp
def next_timeline(driver:webdriver.Chrome):
    try:
        button = driver.find_element(By.XPATH, "//img[@alt='Xem dữ liệu tiếp']/parent::a")
        button.click()
        print("Switch timeline to next ...")
    except Exception as error:
        return f"nex timeline err - {error}"


def convert_sales_service_data(driver:webdriver.Chrome):
    try:
        '''
        Lấy thông tin số liệu của doanh thu bán 
        hàng và dịch vụ từ doanh nghiệp theo
        Class chỉ định 
        '''
        # data = []
        rows = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, '01'))
        )
        qrt = rows.find_elements(By.TAG_NAME, "td")

        tt = qrt[0].text
        q1 = qrt[1].text
        q2 = qrt[2].text
        q3 = qrt[3].text
        q4 = qrt[4].text


        return tt,q1,q2,q3,q4
    except Exception as error:
        return f"Sale data error :  {error}"

def convert_prediction_data(driver:webdriver.Chrome):
    try:

        '''
        Lấy thông tin về các khoản khấu trừ
        theo quý, tương tự như quy trình lấy
        dữ liệu ở doanh thu
        '''
        rows = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, '02'))
        )
        qrt = rows.find_elements(By.TAG_NAME, 'td')

        tt = qrt[0].text
        q1 = qrt[1].text
        q2 = qrt[2].text
        q3 = qrt[3].text
        q4 = qrt[4].text

        return tt,q1,q2,q3,q4

    except Exception as error:
        return f"Prediction data error: {error}"


def convert_data(id:str,driver:webdriver.Chrome):
    '''
    Bộ chuyển đổi dữ liệu, sử dụng
    cho việc lấy dữ liệu theo thẻ ID 
    tag_name , rút gọn khả năng xây dựng dữ liệu
    '''
    try:
        rows = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, f'{id}'))
        )
        qrt = rows.find_elements(By.TAG_NAME, 'td')
        tt = qrt[0].text
        q1 = qrt[1].text
        q2 = qrt[2].text
        q3 = qrt[3].text
        q4 = qrt[4].text

        return tt,q1,q2,q3,q4

    except Exception as error:
        return f"Data streaming error: {error}"

def data_loops(tube:list,driver:webdriver.Chrome):
    data = []

    for obj in range(len(tube)):  
        tt,q1,q2,q3,q4 = convert_data(tube[obj],driver=driver)
        data.append(
            {
                "title":tt,
                "First":q1,
                "Second":q2,
                "Third":q3,
                "Fourth":q4,
                
            }
        )
    return data




if __name__ == "__main__":
    pass