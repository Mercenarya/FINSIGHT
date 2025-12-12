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


current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(current_dir, '..')
sys.path.append(root)

build_dir = os.path.join(current_dir,'caculation','build')
sys.path.append(build_dir)


from utils.data_release_csv import extract_keys,extract_list,convert_data_frame
from utils.comm_functions import looping_json,save_to_json,seed_path
from utils.comm_functions import JSN,PATH
# from ml_pipeline.calculation.build import evaluate_module


# ev = evaluate_module.Evaluate()

#Data operators

id_class = ['01','02','10','11','20','21','22',
            '23','24','25','26','30','31','32','40',
            '50','51','52','60','61','62','70','71']


#begin assessment - functions
def convert_string(data:str):
    try:
        unidecode_key = unidecode.unidecode(input).lower()
        data = "-".join(unidecode_key.split())
        return data
    except Exception as error:
        return error


def get_ecn(driver: webdriver.Chrome, text:str) -> str:
    '''
    Lấy dữ liệu từ mục tài chính gồm
    BCTC, thông tin tài chính thông thường
    link bản báo cáo
    '''
    try:
        wait = WebDriverWait(driver, 10)
        link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, text)))
        link.click()

        time.sleep(3)
        more = wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'Xem đầy đủ')))
        more.click()
        return 'Access Finance reports'
    except Exception as error:
        return error
    
def convert_data(data:str):
    '''
    Chuyển đổi các dữ liệu bị khiếm khuyết 
    '''

#lấy theo danh mục
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
    path = "D:\BrowserDriver\Chrome\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    # service = Service(executable_path=path)
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)
    url = "https://cafef.vn/du-lieu.chn"
    driver.get(url)
    result = "Fpt"
    keyword = "Fpt"
    data = convert_string(result)

    try:
        search_engine = driver.find_element(By.ID, 'search-header')
        search_engine.send_keys(result)
        time.sleep(3)
        search_engine.send_keys(keys.Keys.ENTER)
        # btn = driver.find_element(By.CSS_SELECTOR, '.header__content__right__btn.dont-close-when-click')
        # btn.click()
        time.sleep(3)
        print(get_ecn(driver, 'Thông tin tài chính'))
        print("Check Result .... ")
        current_url = driver.current_url
        # print(convert_data(current_url))
        time.sleep(5)
        # print(convert_data(tbd))
        print(convert_sales_service_data(driver))
        time.sleep(3)
        print(current_timeline(driver))
        time.sleep(3)
        data = data_loops(id_class,driver)
        time.sleep(3)
        print("Extract to JSON ...")
       

        #lấy dữ liệu vào json riêng
        json_data = looping_json(data)
        seed_json = seed_path(JSN)
        #lưu vào mục data/json
        print(json_data)
        print("Corrected dir: ",seed_json)
        print(save_to_json(JSN, json_data))
        time.sleep(3)
        val = extract_list(data)
        tt,qq1,qq2,qq3,qq4 = extract_keys(data)
        # print(key)
        # print(val)
        print("TITLE")
        print(tt)
        print(qq1)
        print(qq2)
        time.sleep(3)
        print("Starting convert and divide data ... ")
        time.sleep(3)
        print(convert_data_frame(tt,qq1,qq2,qq3,qq4))
        # print(convert_data_frame(key,val,"D:\MCT\formweb\FinSightData\data\Raw_data.csv"))
        
    except Exception as error:
        print(error)
    finally:
        driver.quit()

