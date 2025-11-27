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

current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(current_dir, '..')
sys.path.append(root)

build_dir = os.path.join(current_dir,'caculation','build')
sys.path.append(build_dir)


from utils.data_release_csv import extract_keys,extract_list,convert_data_frame
from utils.comm_functions import looping_json,save_to_json,seed_path
from utils.comm_functions import JSNAS,ASSET,ASSETS
from utils.comm_functions import JSNRP,RAW
# lấy các hàm xử lí từ ASSETS
from fn_assets import assets_id_class,renew_string_data,convert_string
from fn_assets import get_ecn_assets,data_loops_assets,looping_json,seed_path
# lấy các hàm xử lí từ BCTC
from fn_reports import reports_id_class,convert_data_reports,convert_sales_service_data_reports,current_timeline_reports
from fn_reports import get_ecn_reports,data_loops_reports,looping_json,seed_path





# lấy báo cáo tài chính tổng thế
def get_finance_reports(driver,result):
    try:
        wait = WebDriverWait(driver,10)

        search_engine = wait.until(
            EC.presence_of_element_located((By.ID, 'search-header'))
        )
        search_engine.send_keys(result)
        time.sleep(3)
        search_engine.send_keys(keys.Keys.ENTER)
        # btn = driver.find_element(By.CSS_SELECTOR, '.header__content__right__btn.dont-close-when-click')
        # btn.click()
        time.sleep(3)
        print(get_ecn_reports(driver, 'Thông tin tài chính'))
        print("Check Result .... ")
      
        time.sleep(5)
        
        print(convert_sales_service_data_reports(driver))
        time.sleep(3)
        print(current_timeline_reports(driver))
        time.sleep(3)
        data = data_loops_reports(reports_id_class,driver)
        time.sleep(3)
        print("Extract to JSON ...")
       

        #lấy dữ liệu vào json riêng
        json_data = looping_json(data)
        seed_json = seed_path(JSNRP)
        #lưu vào mục data/json
        print(json_data)
        print("Corrected dir: ",seed_json)
        print(save_to_json(JSNRP, json_data))
        time.sleep(3)
        tt,qq1,qq2,qq3,qq4 = extract_keys(data)
        print("TITLE")
        print(tt)
        print(qq1)
        print(qq2)
        time.sleep(3)
        print("Starting convert and divide data ... ")
        time.sleep(3)
        print(convert_data_frame(tt,qq1,qq2,qq3,qq4,RAW))
    except asyncio.TimeoutError:
        print("Async timeout")
        return
    except asyncio.IncompleteReadError:
        print("Async general Incompleted")
    except Exception as err:
        print(f"Finance Assets general errors : {err}")






# lấy báo cáo về mục tài sản
def get_finance_assets(driver,result):
    try:
        wait = WebDriverWait(driver,10)

        search_engine = wait.until(
            EC.presence_of_element_located((By.ID, 'search-header'))
        )
        search_engine.send_keys(result)
        time.sleep(3)
        search_engine.send_keys(keys.Keys.ENTER)
        # btn = driver.find_element(By.CSS_SELECTOR, '.header__content__right__btn.dont-close-when-click')
        # btn.click()
        time.sleep(3)
        print(get_ecn_assets(driver, 'Thông tin tài chính'))
        print("Check Result .... ")
        
        time.sleep(5)
       
        print("Starting loop's period")
        time.sleep(3)
        class_data = renew_string_data(assets_id_class)
        print(class_data)
        data = data_loops_assets(class_data,driver)
        print(data)
        time.sleep(3)
        print("Extract to JSON...")

        # lấy dữ liệu cho json riêng
        json_data = looping_json(data=data)
        seed_json = seed_path(JSNAS)

        print(json_data)
        #lưu vào mục data/json
        print(json_data)
        print("Corrected dir: ",seed_json)
        print(save_to_json(JSNAS, json_data))
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
        print(convert_data_frame(tt,qq1,qq2,qq3,qq4,ASSET))
    except asyncio.TimeoutError:
        print("Async timeout")
        return
    except asyncio.IncompleteReadError:
        print("Async general Incompleted")
    except Exception as err:
        print(f"Finance Reports general errors : {err}")

def run_procedure(driver,result):
    # reports
    url = 'https://cafef.vn/du-lieu.chn'
    driver.execute_script("window.open('about:blank','_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    get_finance_reports(driver=driver,result=result)


    # assets
    url = 'https://cafef.vn/du-lieu.chn'
    driver.execute_script("window.open('about:blank','_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    get_finance_assets(driver=driver,result=result)
    
    

if __name__ == "__main__":
    options = Options()
    service = Service(ChromeDriverManager().install())
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service,options=options)
    
    result = "CTR"
    
    run_procedure(driver,result=result)
    driver.quit()