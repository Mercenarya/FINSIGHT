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


def request_connection(url:str):
    try:
        obj = requests.get(url)
        if obj.status_code == 200:
            return True
        else: return False
    except Exception as error:
        return f'Error message : {error}'
    except requests.ConnectionError as cnr:
        return f'<connection interrupted - 200>'

def convert_string(data:str):
    try:
        unidecode_key = unidecode.unidecode(data).lower()
        data = "-".join(unidecode_key.split())
        return data
    except Exception as error:
        return error


def data_list(driver:webdriver.Chrome):
    #ac_results
    try:
        # check = request_connection(url)
        # if check is True:
        wait = WebDriverWait(driver, 10)
        list = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ac_results')))
        time.sleep(3.5)
        ul = list.find_element(By.TAG_NAME,'ul')
        li = ul.find_elements(By.TAG_NAME, 'li')
        for obj in li:
            print(obj.text)

        # else:
        #     return 'No result'
            
    except Exception as error:
        return f'Error - {error}'
    

if __name__ == "__main__":
    path = "D:\BrowserDriver\Chrome\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    # service = Service(executable_path=path)
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)
    url = "https://cafef.vn/du-lieu.chn"
    driver.get(url)
    result = "VINA"
    keyword = "VINA"
    data = convert_string(result)
    


    try:
        # chờ input xuất hiện
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-header"))
        )

    
        for ch in keyword:
            search_box.send_keys(ch)
            driver.execute_script(
                """
                    var el = arguments[0];
                    var ev = new Event('keyup', { bubbles: true });
                    el.dispatchEvent(ev);
                """,search_box
            )
            time.sleep(0.2)

        # Đợi kết quả hiển thị
        time.sleep(2)
        driver.execute_script(
            '''
            let box = document.querySelector('div.ac_results');
            if (box) box.style.display = 'block';
            '''
        )
        print(data_list(driver))
            
    except Exception as error:
        print(error)
    finally:
        driver.quit()


