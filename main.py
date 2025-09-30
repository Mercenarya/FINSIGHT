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
def convert_sales_service(key:str, driver:webdriver.Chrome):
    '''
    Lấy danh mục Doanh thu bán hàng và dịch vụ
    theo yêu cầu chi tiết từ users nếu họ cần
    xem rõ một mục báo cáo cụ thể ở một danh mục nào đó
    '''
    try:
        rows = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID, '01'))
        )
        title = rows.find_element(By.CSS_SELECTOR, '.b_r_c.Lever_1').text
        return title
    except Exception as error:
        return f"message : {error}"

#dữ liệu quý hiện tại
def current_timeline(driver:webdriver.Chrome):
    tb = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID, 'tblGridData'))
    )
    timeline_row = tb.find_elements(By.CLASS_NAME, 'h_t')

    tl1 = timeline_row[0]
    tl2 = timeline_row[1]
    tl3 = timeline_row[2]
    tl4 = timeline_row[3]

    return tl1,tl2,tl3,tl4


if __name__ == "__main__":
    path = "D:\BrowserDriver\Chrome\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    # service = Service(executable_path=path)
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)
    url = "https://cafef.vn/du-lieu.chn"
    driver.get(url)
    result = "B82"
    keyword = "B82"
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
    except Exception as error:
        print(error)
    finally:
        driver.quit()

