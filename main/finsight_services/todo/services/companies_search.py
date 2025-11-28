import os
import sys

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import unidecode
import requests
import pandas as pd
import numpy as np
import os
import sys
import re
import asyncio
import time

CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(CURRENT,'..','..','..','..')
sys.path.append(ROOT)
print(ROOT)

# đồng bộ quá trình lấy danh sách kết quả tìm kiếm
async def get_ul_list_results(driver,result):
    try:
        # độ trễ 10s để đồng bộ quá trình xử lí trên trình duyệt trực tiếp
        wait = WebDriverWait(driver,10)
        # lấy ID của thanh tìm kiếm
        search_engine = wait.until(
            EC.presence_of_element_located((By.ID,'search-header'))
        )
        
        # xóa kết quả cũ ở core nhưng vẫn giữ kết quả người dùng nhập ở phần giao diện
        search_engine.clear()
        search_engine.send_keys(result)
        # set thời gian chờ đợi kết quả được lấy
        time.sleep(1)
        # lấy class chứa thông tinh danh sách kết quả tìm kiếm
        list_results = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME,'wrapper-list-search-result'))
        )
        # lấy thẻ ul duy nhất của class
        ul = list_results.find_element(By.TAG_NAME,'ul')
        # từ ul, truy xuất các kết quả bằng li
        results = ul.find_elements(By.TAG_NAME,'li')
        data = []

        for obj in range(len(results)):
            res = results[obj].text
            data.append(
                {
                    'result':f"{res}"
                }
            )
            print("="*len(res))
            print(res)
            
        return data


    except Exception as error:
        print({
                'Error':f'{error}'
            }
        )
        return []

# hàm đặc biệt trưng dụng khi gọi sang module Views của Django
# kiểm soát driver và từng lần query
async def search_result(query:str):
    options = Options() # tạo options
    service = Service(ChromeDriverManager().install()) # lấy driver trình duyệt
    options.add_argument("--headless") # dấu trình duyệt
    driver = webdriver.Chrome(service=service,options=options)
    url = 'https://cafef.vn/du-lieu.chn'
    driver.get(url)

    try:
        
        results = await get_ul_list_results(driver,query)
        return results
    except Exception as error:
        print('Search result error',f'{error}')
        return []

# options = Options() # tạo options
# service = Service(ChromeDriverManager().install()) # lấy driver trình duyệt
# options.add_argument("--headless") # dấu trình duyệt
# driver = webdriver.Chrome(service=service,options=options)
# url = 'https://cafef.vn/du-lieu.chn'
# driver.get(url)
# while True:
#     result = input("Enter companies: ")
#     asyncio.run(get_ul_list_results(driver,result))
    # asyncio.sleep(2)
    # run_procedure(driver,result)
    # driver.quit()