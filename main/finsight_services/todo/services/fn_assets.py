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
from utils.comm_functions import JSNAS,ASSET,ASSETS
# from ml_pipeline.calculation.build import evaluate_module


# ev = evaluate_module.Evaluate()

#Data operators

assets_id_class = [
    100,110,111,112,120,121,122,123,130,
    131,132,134,135,136,137,139,140,141,
    149,150,151,152,153,154,155,200,210,
    211,212,213,214,215,216,219,220,221,
    222,223,224,225,226,227,228,229,230,
    231,232,240,241,242,250,251,252,253,
    254,255,260,261,262,263,268,269,270,
    300,310,311,312,313,314,315,316,317,
    318,319,320,321,322,323,324,330,331,
    332,333,334,335,336,337,338,339,340,
    341,342,343,400,411,'411a','411b',412,413,
    414,415,416,417,418,419,420,421,'421a','421b',
    422,429,430,431,432,440,
]

# chuyển đổi các mục ID thành string
def renew_string_data(data:list):
    try:
        string_data = []
        if len(data) == 0:
            return None
        else:
            for obj in range(len(data)):
                string_data.append(str(data[obj]))
            print("String data handled")
        return string_data
    
    except Exception as error:
        return f"String data handling errors: {error}"



#begin assessment - functions
def convert_string(data:str):
    try:
        unidecode_key = unidecode.unidecode(input).lower()
        data = "-".join(unidecode_key.split())
        return data
    except Exception as error:
        return error


# (link báo cáo tài sản) https://cafef.vn/du-lieu/bao-cao-tai-chinh/B82/BSheet/2018/2/0/0/can-doi-ke-toan-cong-ty-co-phan-482.chn
# (Link báo cáo tài chính) https://cafef.vn/du-lieu/bao-cao-tai-chinh/B82/IncSta/2018/2/0/0/ket-qua-hoat-dong-kinh-doanh-cong-ty-co-phan-482.chn



def get_ecn_assets(driver: webdriver.Chrome, text:str) -> str:
    '''
    Lấy dữ liệu từ mục tài chính gồm
    BCTC, thông tin tài chính thông thường
    link bản báo cáo
    '''
    try:
        # wait = WebDriverWait(driver, 10)
        # link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, text)))
        # link.click()

        # time.sleep(3)
        # more = wait.until(EC.element_to_be_clickable((By.LINK_TEXT,'Xem đầy đủ')))
        # more.click()
        cell_elements = driver.find_element(By.XPATH, "//table/tbody/tr[19]/td[1]")

        wait = WebDriverWait(driver,10)

        colspan = cell_elements.get_attribute('colspan')

        # tạo xpath để lấy liên kết
        xpath = f"//table/tbody/tr[19]/td[@colspan='{colspan}']"

        link = wait.until(EC.element_to_be_clickable((By.XPATH,xpath)))
        link.click()
        return 'Access Assets reports'
    except Exception as error:
        return error
    
#lấy theo danh mục
def convert_assets_service_data_assets(driver:webdriver.Chrome):
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
        return f"Assets data error :  {error}"
    




#dữ liệu quý hiện tại
def current_timeline_assets(driver:webdriver.Chrome):
    tb = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID, 'tblGridData'))
    )
    timeline_row = tb.find_elements(By.CLASS_NAME, 'h_t')

    tl1 = timeline_row[0].text
    tl2 = timeline_row[1].text
    tl3 = timeline_row[2].text
    tl4 = timeline_row[3].text

    return tl1,tl2,tl3,tl4




# chuyển đổi dữ liệu
def convert_data_assets(id:str,driver:webdriver.Chrome):
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
        print(

            {
                "tt":len(tt),
                "qq1":len(q1),
                "qq2":len(q2),
                "qq3":len(q3),
                "qq4":len(q4)
            }
        )

        return tt,q1,q2,q3,q4

    except Exception as error:
        return f"Data streaming error: {error}"


# khởi tạo vòng lặp để lấy dữ liệu từng nội dung
def data_loops_assets(tube:list,driver:webdriver.Chrome):
    try:
        data = []
        
        for obj in range(len(tube)):  
            tt,q1,q2,q3,q4 = convert_data_assets(tube[obj],driver=driver)
            data.append(
                {
                    "title":tt,
                    "First":q1,
                    "Second":q2,
                    "Third":q3,
                    "Fourth":q4,
                    
                }
            )
            print(
                "Data Length in period: ",
                {
                    "tt":len(tt),
                    "qq1":len(q1),
                    "qq2":len(q2),
                    "qq3":len(q3),
                    "qq4":len(q4)
                }
            )
        return data
    except Exception as error:
        return f"Data loops error: {error}"





# if __name__ == "__main__":
#     path = "D:\BrowserDriver\Chrome\chromedriver-win64\chromedriver-win64\chromedriver.exe"

#     # service = Service(executable_path=path)
#     service = Service(ChromeDriverManager().install())

#     driver = webdriver.Chrome(service=service)
#     url = "https://cafef.vn/du-lieu.chn"
#     driver.get(url)
#     result = "Vingroup"
#     keyword = "Vingroup"
#     data = convert_string(result)

#     try:
#         search_engine = driver.find_element(By.ID, 'search-header')
#         search_engine.send_keys(result)
#         time.sleep(3)
#         search_engine.send_keys(keys.Keys.ENTER)
#         # btn = driver.find_element(By.CSS_SELECTOR, '.header__content__right__btn.dont-close-when-click')
#         # btn.click()
#         time.sleep(3)
#         print(get_ecn(driver, 'Thông tin tài chính'))
#         print("Check Result .... ")
#         current_url = driver.current_url
#         print(current_url)
#         # print(convert_data(current_url))
#         time.sleep(5)
#         # print(convert_data(tbd))
#         print("Starting loop's period")
#         time.sleep(3)
#         class_data = renew_string_data(id_class)
#         print(class_data)
#         data = data_loops(class_data,driver)
#         print(data)
#         time.sleep(3)
#         print("Extract to JSON...")

#         # lấy dữ liệu cho json riêng
#         json_data = looping_json(data=data)
#         seed_json = seed_path(JSNAS)

#         print(json_data)
#         #lưu vào mục data/json
#         print(json_data)
#         print("Corrected dir: ",seed_json)
#         print(save_to_json(JSNAS, json_data))
#         time.sleep(3)
#         val = extract_list(data)
#         tt,qq1,qq2,qq3,qq4 = extract_keys(data)
        
#         # print(key)
#         # print(val)
#         print("TITLE")
#         print(tt)
#         print(qq1)
#         print(qq2)
#         time.sleep(3)
#         print("Starting convert and divide data ... ")
#         time.sleep(3)
#         print(convert_data_frame(tt,qq1,qq2,qq3,qq4,ASSET))

       
#     except Exception as error:
#         print(error)
#     finally:
#         driver.quit()

